"""Tests for Causal Hash-Chained Event Logging and Replay Engine."""

import pytest
from simlab.core.logging import CausalEventLogger
from simlab.core.replay import ReplayEngine
from simlab.scenarios import ScenarioLoader


def test_causal_event_logger_integrity():
    logger = CausalEventLogger(run_id="run_test_01")
    logger.log_event(tick=0, actor_id="sys", action="INIT")
    logger.log_event(tick=1, actor_id="a1", action="DECIDE", inputs={"x": 10})
    logger.log_event(tick=2, actor_id="a2", action="APPROVE", parent_event_id="ev_01")

    assert len(logger) == 3
    valid, err = logger.verify_chain()
    assert valid is True
    assert err is None


def test_causal_event_logger_detects_tampering():
    logger = CausalEventLogger(run_id="run_test_02")
    logger.log_event(tick=0, actor_id="sys", action="INIT")
    logger.log_event(tick=1, actor_id="a1", action="DECIDE", inputs={"x": 10})
    logger.log_event(tick=2, actor_id="a2", action="APPROVE")

    # Adversarial tampering: modify an input payload in event 1
    logger._events[1]["inputs"]["x"] = 9999

    valid, err = logger.verify_chain()
    assert valid is False
    assert "Tampered event" in err or "Broken chain" in err


def test_deterministic_simulation_and_replay_equivalence():
    """Verify that two simulation runs with identical seeds produce identical event traces."""
    loader = ScenarioLoader()
    config = loader.load_scenario("cooperative_pipeline")

    # Run 1
    k1, _ = loader.build_simulation(config, seed=42)
    res1 = k1.run(max_ticks=20)
    events1 = k1.logger.to_list()

    # Run 2 with same seed
    k2, _ = loader.build_simulation(config, seed=42)
    res2 = k2.run(max_ticks=20)
    events2 = k2.logger.to_list()

    # Replay comparison
    replay = ReplayEngine(events1)
    is_identical, discrepancies = replay.compare_traces(events2)

    assert is_identical is True, f"Discrepancies found: {discrepancies}"
    assert res1.terminal_state_hash == res2.terminal_state_hash
    assert res1.total_ticks == res2.total_ticks


def test_state_replay_positive_control():
    """Verify that replaying recorded event actions reconstructs exact terminal state."""
    loader = ScenarioLoader()
    config = loader.load_scenario("cooperative_pipeline")
    k, _ = loader.build_simulation(config, seed=42)
    res = k.run(max_ticks=20)

    replay = ReplayEngine(k.logger.to_list())
    valid, err, final_state = replay.replay_state(
        scenario_identifier_or_config="cooperative_pipeline",
        expected_terminal_hash=res.terminal_state_hash
    )

    assert valid is True
    assert err is None
    assert final_state["completed_count"] == 3
    assert final_state["energy"] == 70.0


def test_negative_control_valid_hash_chain_tampered_terminal_hash():
    """Negative Control 1: Event chain is cryptographically valid, but claimed terminal hash is forged."""
    loader = ScenarioLoader()
    config = loader.load_scenario("cooperative_pipeline")
    k, _ = loader.build_simulation(config, seed=42)
    res = k.run(max_ticks=20)

    replay = ReplayEngine(k.logger.to_list())

    # 1. Merely valid event chain checks out
    chain_valid, chain_err = replay.verify_integrity()
    assert chain_valid is True
    assert chain_err is None

    # 2. State replay catches forged/mismatched terminal state hash
    forged_terminal_hash = "deadbeef" * 8
    state_valid, state_err, _ = replay.replay_state(
        scenario_identifier_or_config="cooperative_pipeline",
        expected_terminal_hash=forged_terminal_hash
    )
    assert state_valid is False
    assert "hash mismatch" in state_err.lower()


def test_negative_control_recomputed_valid_chain_divergent_state():
    """Negative Control 2: Event chain hashes are recomputed (valid chain) but action was fabricated."""
    loader = ScenarioLoader()
    config = loader.load_scenario("cooperative_pipeline")
    k, _ = loader.build_simulation(config, seed=42)
    res = k.run(max_ticks=20)

    genuine_events = k.logger.to_list()
    genuine_terminal_hash = res.terminal_state_hash

    # Fabricate an event: omit the last APPROVE_TASK action
    # and recompute all downstream event hashes from that point
    fabricated_events = [dict(e) for e in genuine_events]
    # Find an APPROVE_TASK event and change its action to STANDBY
    for ev in fabricated_events:
        if ev.get("action") == "APPROVE_TASK":
            ev["action"] = "STANDBY"
            ev["inputs"] = {"parameters": {}}
            break

    # Recompute hashes from scratch so the hash chain is 100% mathematically valid
    from simlab.core.logging import CausalEventLogger
    rebuilder = CausalEventLogger(run_id="recomputed_run")
    for ev in fabricated_events:
        rebuilder.log_event(
            tick=ev["tick"],
            actor_id=ev["actor_id"],
            action=ev["action"],
            inputs=ev.get("inputs"),
            outcome=ev.get("outcome"),
            event_type=ev.get("event_type", "AGENT_ACTION"),
            parent_event_id=ev.get("parent_event_id")
        )

    replay_fabricated = ReplayEngine(rebuilder.to_list())

    # The hash chain is 100% VALID:
    chain_valid, chain_err = replay_fabricated.verify_integrity()
    assert chain_valid is True, f"Recomputed chain should be valid, got {chain_err}"

    # BUT state replay MUST FAIL against the reported terminal state:
    state_valid, state_err, _ = replay_fabricated.replay_state(
        scenario_identifier_or_config="cooperative_pipeline",
        expected_terminal_hash=genuine_terminal_hash
    )
    assert state_valid is False
    assert "hash mismatch" in state_err.lower()


def test_negative_control_cross_scenario_replay():
    """Negative Control 3: Valid trace from scenario A replayed against scenario B fails state replay."""
    loader = ScenarioLoader()
    cfg_crisis = loader.load_scenario("resource_crisis")
    k, _ = loader.build_simulation(cfg_crisis, seed=42)
    res = k.run(max_ticks=15)

    replay = ReplayEngine(k.logger.to_list())

    # Chain is valid for resource_crisis
    assert replay.verify_integrity()[0] is True

    # Replaying crisis events against cooperative_pipeline scenario fails
    state_valid, state_err, _ = replay.replay_state(
        scenario_identifier_or_config="cooperative_pipeline",
        expected_terminal_hash=res.terminal_state_hash
    )
    assert state_valid is False
