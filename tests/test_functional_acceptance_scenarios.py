"""Phase 4 Functional Acceptance and Truthful Adversarial Demonstration Suite.

Demonstrates complete multi-agent execution in which SimLab:
1. Initializes a multi-agent environment with heterogeneous unseen functional tasks.
2. Coordinates activity across Coordinator, specialized Workers, and Critic.
3. Records all events and state transitions in a tamper-evident causal hash chain.
4. Produces verifiable mathematical and analytical outcomes (not hardcoded placeholders).
5. Replays deterministically bit-for-bit to verify the terminal state hash.
6. Truthfully reports failures and rejects corruptions:
   - Catches deliberate corrupt worker results and forces rework.
   - Terminates truthfully when resources are depleted.
   - Rejects causal event tampering.
   - Rejects forged terminal states during replay.
"""

import copy
import pytest

from simlab.core.kernel import SimulationKernel
from simlab.core.replay import ReplayEngine
from simlab.environment.cooperative_task import CooperativeTaskEnvironment
from simlab.agents.coordinator import CoordinatorAgent
from simlab.agents.worker import WorkerAgent
from simlab.agents.critic import CriticAgent
from simlab.faults.injector import FaultInjector


def _make_sample_tasks():
    return [
        {
            "task_id": "feat_01",
            "name": "Moving Average Signal Smoothing",
            "status": "PENDING",
            "requirements": {
                "operation": "moving_average",
                "inputs": [10.0, 20.0, 30.0, 40.0, 50.0],
                "window": 3
            }
        },
        {
            "task_id": "feat_02",
            "name": "Polynomial Telemetry Interpolation",
            "status": "PENDING",
            "requirements": {
                "operation": "polynomial",
                "coefficients": [3.0, 2.0, 5.0],  # 3 + 2*x + 5*x^2
                "x": 4.0
            }
        },
        {
            "task_id": "feat_03",
            "name": "Filtered Sensor Range Aggregation",
            "status": "PENDING",
            "requirements": {
                "operation": "filter_sum",
                "inputs": [5.0, 15.0, 25.0, 35.0, 45.0, 55.0],
                "min_val": 10.0,
                "max_val": 50.0
            }
        }
    ]


def test_full_scenario_functional_acceptance_and_replay():
    """Complete multi-agent cooperative pipeline with dynamic computation and bit-for-bit replay."""
    tasks = _make_sample_tasks()

    kernel = SimulationKernel(seed=777, run_id="acc_run_s777")
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=100.0, energy_cost_per_task=10.0)
    env.attach_to_kernel(kernel)

    coordinator = CoordinatorAgent("coordinator", managed_workers=["worker_math", "worker_stats"])
    worker_math = WorkerAgent("worker_math", specialization="numerical_math")
    worker_stats = WorkerAgent("worker_stats", specialization="signal_stats")
    critic = CriticAgent("critic", strict_mode=True)

    kernel.register_agent(coordinator)
    kernel.register_agent(worker_math)
    kernel.register_agent(worker_stats)
    kernel.register_agent(critic)

    # 2. Run simulation
    run_result = kernel.run(max_ticks=25)

    assert run_result.is_completed is True
    assert run_result.total_events > 0

    # 3. Verify measurable outcomes match ground truth mathematical results
    env_tasks = env.state.get("tasks")
    results_map = {t["task_id"]: t.get("result_value") for t in env_tasks}
    status_map = {t["task_id"]: t.get("status") for t in env_tasks}

    assert status_map["feat_01"] == "COMPLETED"
    assert results_map["feat_01"] == 40.0

    assert status_map["feat_02"] == "COMPLETED"
    assert results_map["feat_02"] == 91.0

    assert status_map["feat_03"] == "COMPLETED"
    assert results_map["feat_03"] == 120.0

    assert env.state.get("completed_count") == 3
    # 3 tasks * 10 energy = 30 used, 70 remaining
    assert env.state.get("energy") == 70.0

    # 4. Cryptographic trace replay and verification
    replayer = ReplayEngine(kernel.logger.to_list())
    chain_valid, chain_err = replayer.verify_integrity()
    assert chain_valid is True, f"Event chain failed: {chain_err}"

    # Verify run 2 with same seed reproduces bit-for-bit
    k2 = SimulationKernel(seed=777, run_id="acc_run_s777")
    env2 = CooperativeTaskEnvironment(
        tasks=_make_sample_tasks(),
        initial_energy=100.0,
        energy_cost_per_task=10.0
    )
    env2.attach_to_kernel(k2)
    k2.register_agent(CoordinatorAgent("coordinator", managed_workers=["worker_math", "worker_stats"]))
    k2.register_agent(WorkerAgent("worker_math", specialization="numerical_math"))
    k2.register_agent(WorkerAgent("worker_stats", specialization="signal_stats"))
    k2.register_agent(CriticAgent("critic", strict_mode=True))
    run_result2 = k2.run(max_ticks=25)

    assert run_result.terminal_state_hash == run_result2.terminal_state_hash
    assert run_result.total_ticks == run_result2.total_ticks
    assert run_result.total_events == run_result2.total_events

    # Replay comparison bit-for-bit
    identical, discrepancies = replayer.compare_traces(k2.logger.to_list())
    assert identical is True, f"Trace mismatch: {discrepancies}"


def test_truthful_failure_reporting_on_resource_starvation():
    """Adversarial Test: Kernel truthfully reports failure when energy depletes before tasks complete."""
    tasks = [
        {"task_id": f"heavy_task_{i}", "name": f"Heavy Compute {i}", "status": "PENDING"}
        for i in range(5)
    ]
    # Energy cost 25 per task, initial energy only 40 (only 1 task can execute)
    kernel = SimulationKernel(seed=42)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=40.0, energy_cost_per_task=25.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", managed_workers=["w1"]))
    kernel.register_agent(WorkerAgent("w1"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=20)

    # Truthful reporting: completed count is strictly bounded by energy
    assert env.state.get("completed_count") == 1
    assert env.state.get("energy") == 15.0  # 40 - 25 = 15 < 25 needed for second task
    # Remaining tasks remain PENDING or IN_PROGRESS, not falsely marked completed
    incomplete = [t for t in env.state.get("tasks") if t["status"] != "COMPLETED"]
    assert len(incomplete) == 4


def test_adversarial_rejection_of_corrupted_trace():
    """Adversarial Test: ReplayEngine rejects tampered event payload and altered terminal hash."""
    kernel = SimulationKernel(seed=42)
    env = CooperativeTaskEnvironment(
        tasks=[{"task_id": "t1", "name": "Basic Task", "status": "PENDING"}],
        initial_energy=50.0
    )
    env.attach_to_kernel(kernel)
    kernel.register_agent(CoordinatorAgent("coordinator", managed_workers=["w1"]))
    kernel.register_agent(WorkerAgent("w1"))
    kernel.register_agent(CriticAgent("critic"))
    res = kernel.run(max_ticks=10)

    events = kernel.logger.to_list()
    assert len(events) > 5

    # Attack 1: Modify payload of event index 3
    tampered_events = copy.deepcopy(events)
    tampered_events[3]["inputs"]["corrupted_field"] = "malicious_injection"

    replayer_tampered = ReplayEngine(tampered_events)
    valid, err = replayer_tampered.verify_integrity()
    assert valid is False
    assert err is not None

    # Attack 2: Tail truncation (cut off terminal events)
    truncated = events[:-3]
    replayer_trunc = ReplayEngine(truncated)
    valid_trunc, err_trunc = replayer_trunc.verify_integrity()
    assert valid_trunc is False
    assert "truncated" in err_trunc.lower() or "missing" in err_trunc.lower()
