"""Functional Qualification Regression Test Suite.

Verifies fixes for defects identified during SimLab independent functional qualification:
- UC-01: Dynamic multi-agent computation on unfamiliar functional inputs (no hardcoded answers).
- UC-07: Critic rejection -> Worker rework -> Resubmission -> Approval & completion.
- ATK-01: Tail-truncated / interrupted simulation log detection in ReplayEngine.
- ATK-03: Rejection of forged APPROVE_TASK on unexecuted PENDING tasks.
- ATK-04A: Bit-for-bit mid-run snapshot/restore determinism across worker, coordinator, and critic.
- ATK-04B: Cryptographic tampering rejection on state restore.
- ATK-05: FaultInjector attach_fault_injector crash scheduling and resource drain execution.
- ATK-08: Sandbox credential scrubbing against arbitrary sensitive patterns.
"""

import json
import os
import pytest

from simlab.core.kernel import SimulationKernel
from simlab.core.replay import ReplayEngine
from simlab.environment.cooperative_task import CooperativeTaskEnvironment
from simlab.agents.coordinator import CoordinatorAgent
from simlab.agents.worker import WorkerAgent
from simlab.agents.critic import CriticAgent
from simlab.faults.injector import FaultInjector
from simlab.scenarios.loader import ScenarioLoader
from simlab.isolation.sandbox import SubprocessSandbox


def test_regression_worker_functional_computation_uc01():
    """UC-01: Worker dynamically computes weighted sum instead of hardcoding 42."""
    k = SimulationKernel(seed=101)
    env = CooperativeTaskEnvironment(tasks=[{
        "task_id": "uc01",
        "name": "Weighted Telemetry Aggregation",
        "status": "PENDING",
        "requirements": {
            "operation": "weighted_sum",
            "inputs": [12.5, 8.0, 19.5, 4.0],
            "weights": [0.2, 0.3, 0.4, 0.1]
        }
    }])
    env.attach_to_kernel(k)
    k.register_agent(CoordinatorAgent("coordinator", ["worker_1"]))
    k.register_agent(WorkerAgent("worker_1"))
    k.register_agent(CriticAgent("critic"))
    
    k.run(max_ticks=15)
    t_out = env.state.get("tasks")[0]
    
    assert t_out.get("status") == "COMPLETED"
    assert t_out.get("result_value") == 13.1


def test_regression_critic_rejection_recovery_uc07():
    """UC-07: Critic rejection triggers worker rework, resubmission, and final approval."""
    k7 = SimulationKernel(seed=101)
    env7 = CooperativeTaskEnvironment(tasks=[{
        "task_id": "uc07",
        "name": "Corrupt Submission Recovery",
        "status": "PENDING",
    }])
    env7.attach_to_kernel(k7)
    w7 = WorkerAgent("worker_1")
    c7 = CriticAgent("critic")
    k7.register_agent(w7)
    k7.register_agent(c7)

    # Initial invalid/negative execution
    k7._action_handlers["ACCEPT_TASK"](
        type("Act", (), {"parameters": {"task_id": "uc07", "worker_id": "worker_1"}, "target": "uc07"})(), 0
    )
    k7._action_handlers["EXECUTE_TASK"](
        type("Act", (), {"parameters": {"task_id": "uc07", "worker_id": "worker_1", "value": -99}, "target": "uc07"})(), 1
    )
    k7.message_bus.send("worker_1", "critic", {
        "type": "SUBMIT_FOR_REVIEW",
        "task_id": "uc07",
        "submission": {"task_id": "uc07", "worker_id": "worker_1", "result_value": -99}
    }, current_tick=1)

    k7.run(max_ticks=15)
    t7_out = env7.state.get("tasks")[0]

    assert t7_out.get("status") == "COMPLETED"
    assert t7_out.get("result_value") == 42
    assert env7.state.get("completed_count") == 1


def test_regression_replay_tail_truncation_detection_atk01():
    """ATK-01: Tail-truncated events.jsonl without completion marker is caught by verify_integrity."""
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")
    k_rep, _ = loader.build_simulation(cfg, seed=42)
    k_rep.run(max_ticks=20)
    full_events = k_rep.logger.to_list()
    
    # Complete run verifies successfully
    rep_full = ReplayEngine(full_events)
    full_valid, full_err = rep_full.verify_integrity()
    assert full_valid is True
    assert full_err is None

    # Truncated trace fails verification
    truncated_events = full_events[:-5]
    rep_trunc = ReplayEngine(truncated_events)
    trunc_valid, trunc_err = rep_trunc.verify_integrity()
    assert trunc_valid is False
    assert "truncated" in trunc_err.lower() or "missing" in trunc_err.lower()


def test_regression_unexecuted_task_approval_rejected_atk03():
    """ATK-03: Critic attempting to approve a PENDING unexecuted task is rejected."""
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")
    rebuilder_k, rebuilder_env = loader.build_simulation(cfg, seed=42)
    
    approve_outcome = rebuilder_k._action_handlers["APPROVE_TASK"](
        type("Act", (), {"parameters": {"task_id": "task_01", "critic_id": "critic"}, "target": "task_01"})(), 1
    )
    
    assert approve_outcome.get("status") != "COMPLETED"
    assert "REJECTED" in approve_outcome.get("status") or "INVALID" in approve_outcome.get("status")
    assert rebuilder_env.state.get("tasks")[0]["status"] == "PENDING"


def test_regression_midrun_snapshot_restore_determinism_atk04a():
    """ATK-04A: Checkpoint/restore mid-run produces exact bit-for-bit terminal hash match."""
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")
    k_uninterrupted, _ = loader.build_simulation(cfg, seed=42)
    res_uninterrupted = k_uninterrupted.run(max_ticks=20)

    k_snap, _ = loader.build_simulation(cfg, seed=42)
    for _ in range(3):
        k_snap.step()
    snap = k_snap.snapshot()

    k_restored, _ = loader.build_simulation(cfg, seed=42)
    k_restored.restore(snap)
    res_restored = k_restored.run(max_ticks=20)

    assert res_uninterrupted.terminal_state_hash == res_restored.terminal_state_hash
    assert res_uninterrupted.total_ticks == res_restored.total_ticks
    assert res_uninterrupted.final_state == res_restored.final_state


def test_regression_tampered_snapshot_rejection_atk04b():
    """ATK-04B: State snapshot tampering is detected and rejected with ValueError."""
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")
    k_snap, _ = loader.build_simulation(cfg, seed=42)
    for _ in range(3):
        k_snap.step()
    snap = k_snap.snapshot()

    tampered_snap = json.loads(json.dumps(snap))
    tampered_snap["state"]["data"]["energy"] = 999999.0

    k_tamper, _ = loader.build_simulation(cfg, seed=42)
    with pytest.raises(ValueError, match="tampering"):
        k_tamper.restore(tampered_snap)


def test_regression_attach_fault_injector_crashes_and_drains_atk05():
    """ATK-05: FaultInjector attached via kernel hooks correctly deactivates agents and drains resources."""
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")
    k_fault, env_fault = loader.build_simulation(cfg, seed=42)
    fi = FaultInjector(
        seed=42,
        crash_schedule={"worker_1": 0},
        resource_drain_schedule={0: {"energy": 25.0}}
    )
    k_fault.attach_fault_injector(fi)
    k_fault.step()

    assert not k_fault.get_agent("worker_1").is_active
    assert env_fault.state.get("energy") == 75.0


def test_regression_sandbox_credential_scrubbing_atk08():
    """ATK-08: Sandbox regex credential scrubbing removes non-whitelisted sensitive tokens."""
    os.environ["CUSTOM_SECRET_TOKEN"] = "secret-value-123"
    os.environ["DB_PASSWORD"] = "hunter2"
    os.environ["AUTH_HEADER_BEARER"] = "bearer-secret-xyz"
    try:
        sb = SubprocessSandbox(timeout_seconds=2.0)
        sb_res = sb.run_code(
            "import os\nprint(os.environ.get('CUSTOM_SECRET_TOKEN'), os.environ.get('DB_PASSWORD'), os.environ.get('AUTH_HEADER_BEARER'))"
        )
        assert "secret-value-123" not in sb_res.stdout
        assert "hunter2" not in sb_res.stdout
        assert "bearer-secret-xyz" not in sb_res.stdout
        assert "None None None" in sb_res.stdout
    finally:
        os.environ.pop("CUSTOM_SECRET_TOKEN", None)
        os.environ.pop("DB_PASSWORD", None)
        os.environ.pop("AUTH_HEADER_BEARER", None)
