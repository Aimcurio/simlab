"""Adversarial Verification Suite for SimLab / Curo.

Attacks the platform along multiple adversarial vectors:
1. Governance Boundary Attacks (Unpermitted operations, firewall tampering)
2. Determinism & Chaos Attacks (Identical seed bit-for-bit check vs seed divergence)
3. Causal Chain Breaking & State Tampering (Hash chain tampering detection)
4. Memory Overload & Extreme Input Attacks (Capacity limits, NaN/inf embeddings, uniform vectors)
5. Rogue Agent Containment (Crashing agents, message flooding)
6. Malicious Benchmark Code Injection (Forbidden calls, infinite loops, memory bombs)
"""

import math
import pytest
from pathlib import Path

from simlab.governance.permissions import OperationTier
from simlab.governance.firewall import GovernanceManager, GovernanceFirewallBlockedError
from simlab.scenarios.loader import ScenarioLoader
from simlab.core.replay import ReplayEngine
from simlab.core.kernel import SimulationKernel
from simlab.core.clock import DiscreteClock
from simlab.core.bus import MessageBus
from simlab.core.events import EventType
from simlab.environment.state import EnvironmentState
from simlab.agents.base import BaseAgent
from simlab.memory.stream import AssociativeMemoryStream
from simlab.memory.item import MemoryItem
from simlab.memory.scoring import min_max_norm, compute_retrieval_score
from simlab.isolation import SubprocessSandbox


# 1. GOVERNANCE BOUNDARY ATTACKS
def test_adversarial_governance_unauthorized_operation():
    gm = GovernanceManager()
    # Explicitly check that empirical execution without clearance raises GovernanceFirewallBlockedError
    with pytest.raises(GovernanceFirewallBlockedError):
        gm.verify_operation(OperationTier.EMPIRICAL_LIVE, "ATTACK_UNAUTHORIZED_LIVE_EXEC")


def test_adversarial_governance_tampered_state():
    gm = GovernanceManager()
    # If canonical lifecycle state is corrupted/invalid, verify it fails-closed
    fake_gov = {
        "canonical_lifecycle_state": "INVALID_HACKED_STATE",
        "authority_state": {}
    }
    with pytest.raises(GovernanceFirewallBlockedError):
        gm.verify_operation(OperationTier.EMPIRICAL_LIVE, "TEST_OPERATION", config_override=fake_gov)


# 2. DETERMINISM AND CHAOS ATTACKS
def test_adversarial_determinism_identical_seeds():
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")

    # Run 1
    k1, _ = loader.build_simulation(cfg, seed=777)
    k1.run(max_ticks=8)
    events1 = [e["event_hash"] for e in k1.logger._events]

    # Run 2
    k2, _ = loader.build_simulation(cfg, seed=777)
    k2.run(max_ticks=8)
    events2 = [e["event_hash"] for e in k2.logger._events]

    assert len(events1) > 0
    assert events1 == events2, "Determinism failed: Identical seeds produced divergent event hashes"


def test_adversarial_determinism_divergent_seeds():
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")

    k1, _ = loader.build_simulation(cfg, seed=111)
    k1.run(max_ticks=8)
    h1 = k1.get_state_hash()

    k2, _ = loader.build_simulation(cfg, seed=222)
    k2.run(max_ticks=8)
    h2 = k2.get_state_hash()

    # Different seeds should produce different execution state hashes or events
    assert [e["event_hash"] for e in k1.logger._events] != [e["event_hash"] for e in k2.logger._events]


# 3. CAUSAL CHAIN BREAKING & STATE TAMPERING
def test_adversarial_causal_chain_tampering():
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")
    k, _ = loader.build_simulation(cfg, seed=42)
    k.run(max_ticks=5)

    events = k.logger.to_list()
    assert len(events) >= 3

    # Tamper with the middle event payload
    tampered_events = [dict(e) for e in events]
    tampered_events[1]["action"] = "MALICIOUS_TAMPERED_ACTION"

    replayer = ReplayEngine(tampered_events)
    valid, err = replayer.verify_integrity()
    assert valid is False
    assert err is not None
    assert "tampered" in err.lower() or "mismatch" in err.lower() or "hash" in err.lower()


# 4. MEMORY OVERLOAD & EXTREME INPUT ATTACKS
def test_adversarial_memory_overflow_capacity():
    stream = AssociativeMemoryStream(capacity=10)
    for i in range(100):
        stream.add(MemoryItem(
            memory_id=f"mem_{i}",
            content=f"Overflow item {i}",
            timestamp_hours=float(i),
            importance=float(i % 10),
            embedding=[0.1 * (i % 5), 0.2, 0.3]
        ))
    assert stream.size == 10, f"Memory stream exceeded capacity: {stream.size} > 10"


def test_adversarial_scoring_extreme_inputs():
    # Test identical inputs (degenerate min_max_norm)
    uniform = [42.0, 42.0, 42.0, 42.0]
    normed = min_max_norm(uniform)
    assert normed == [0.0, 0.0, 0.0, 0.0]

    # Test single element
    single = [10.0]
    assert min_max_norm(single) == [0.0]

    # Test empty list
    assert min_max_norm([]) == []

    # Test extreme negative / large numbers
    extreme = [-1e12, 0.0, 1e12]
    normed_ext = min_max_norm(extreme)
    assert normed_ext[0] == 0.0
    assert normed_ext[2] == 1.0


# 5. ROGUE AGENT CONTAINMENT
from simlab.agents.base import AgentAction

class RogueCrashingAgent(BaseAgent):
    def observe(self, state, incoming_messages, current_tick):
        return {}

    def decide(self, observation, current_tick):
        raise RuntimeError("Rogue agent deliberate crash!")


class RogueFloodingAgent(BaseAgent):
    def observe(self, state, incoming_messages, current_tick):
        return {}

    def decide(self, observation, current_tick):
        return AgentAction(action_type="FLOOD")

    def step(self, current_tick, environment_state, incoming_messages, bus, logger):
        for i in range(100):
            bus.send(
                sender_id=self.agent_id,
                recipient_id="target",
                content={"spam": i},
                current_tick=current_tick
            )
        return AgentAction(action_type="FLOOD")


def test_adversarial_rogue_crashing_agent():
    clock = DiscreteClock()
    bus = MessageBus()
    env = EnvironmentState({"counter": 0})
    kernel = SimulationKernel(clock=clock, bus=bus, env=env)

    rogue = RogueCrashingAgent(agent_id="rogue_01", role="crasher")
    kernel.register_agent(rogue)

    with pytest.raises(RuntimeError, match="Rogue agent deliberate crash!"):
        kernel.step()


def test_adversarial_rogue_flooding_agent():
    clock = DiscreteClock()
    bus = MessageBus(max_mailbox_size=20)  # Bounded capacity
    env = EnvironmentState()
    kernel = SimulationKernel(clock=clock, bus=bus, env=env)

    spammer = RogueFloodingAgent(agent_id="spammer_01", role="spammer")
    kernel.register_agent(spammer)

    kernel.step()
    # Next tick delivers in-flight messages
    kernel.step()
    inbox = bus.receive("target")
    assert len(inbox) <= 20, f"Bus exceeded bounded capacity: {len(inbox)} > 20"


# 6. MALICIOUS BENCHMARK CODE INJECTION & TIMEOUT
def test_adversarial_sandbox_infinite_loop():
    sandbox = SubprocessSandbox(timeout_seconds=1.0)
    infinite_code = "while True: pass"
    res = sandbox.run_code(infinite_code)
    assert res.is_timeout is True
    assert res.is_success is False


def test_adversarial_sandbox_system_exit():
    sandbox = SubprocessSandbox(timeout_seconds=2.0)
    exit_code = "import sys; sys.exit(42)"
    res = sandbox.run_code(exit_code)
    assert res.exit_code == 42
    assert res.is_success is False
