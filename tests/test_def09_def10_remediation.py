"""DEF-09 and DEF-10 Targeted Remediation and Adversarial Qualification Test Suite.

Authoritative verification for:
- DEF-09: Complete, version-aware checkpoint decision trace persistence, isolation,
  malformed rejection, and repeated resume determinism.
- DEF-10: Worker task preemption preservation, competing assignment handling,
  multiple rejection collision resilience, and task conservation invariants.
"""

import copy
import json
import pytest

from simlab.core.kernel import SimulationKernel
from simlab.core.bus import MessageBus
from simlab.core.logging import CausalEventLogger
from simlab.core.state import EnvironmentState
from simlab.core.replay import ReplayEngine
from simlab.agents.base import AgentAction, BaseAgent
from simlab.agents.worker import WorkerAgent
from simlab.agents.coordinator import CoordinatorAgent
from simlab.agents.critic import CriticAgent
from simlab.environment.cooperative_task import CooperativeTaskEnvironment
from simlab.scenarios.loader import ScenarioLoader


# ==============================================================================
# DEF-09: Checkpoint Decision-Trace Loss Verification
# ==============================================================================

def test_def09_decision_trace_complete_restoration_eliminates_11_vs_7():
    """DEF-09: Mid-run checkpoint restore completely preserves decision traces without 11-vs-7 loss."""
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")

    # 1. Control Run: Uninterrupted
    k_ctrl, env_ctrl = loader.build_simulation(cfg, seed=777)
    res_ctrl = k_ctrl.run(max_ticks=25)
    ctrl_traces_coord = k_ctrl.agents["coordinator"].get_decision_traces()
    ctrl_traces_worker = k_ctrl.agents["worker_1"].get_decision_traces()
    ctrl_traces_critic = k_ctrl.agents["critic"].get_decision_traces()

    # Verify baseline control length is 11
    assert len(ctrl_traces_coord) == 11, f"Expected 11 control traces, got {len(ctrl_traces_coord)}"

    # 2. Resumed Run: Interrupt at tick 4
    k_act, _ = loader.build_simulation(cfg, seed=777)
    for _ in range(4):
        k_act.step()
    checkpoint_snap = k_act.snapshot()

    # Restore in fresh simulation instance
    k_res, env_res = loader.build_simulation(cfg, seed=777)
    k_res.restore(checkpoint_snap)
    res_res = k_res.run(max_ticks=25)

    res_traces_coord = k_res.agents["coordinator"].get_decision_traces()
    res_traces_worker = k_res.agents["worker_1"].get_decision_traces()
    res_traces_critic = k_res.agents["critic"].get_decision_traces()

    # 3. Decision trace conservation assertions: eliminated the 11-vs-7 discrepancy
    assert len(res_traces_coord) == 11, f"Expected 11 resumed coordinator traces, got {len(res_traces_coord)}"
    assert len(res_traces_worker) == len(ctrl_traces_worker)
    assert len(res_traces_critic) == len(ctrl_traces_critic)

    # 4. Bit-for-bit equivalence across all agents' decision traces
    assert res_traces_coord == ctrl_traces_coord
    assert res_traces_worker == ctrl_traces_worker
    assert res_traces_critic == ctrl_traces_critic

    # 5. Deterministic continuation equivalence
    assert res_res.terminal_state_hash == res_ctrl.terminal_state_hash
    assert res_res.total_ticks == res_ctrl.total_ticks


def test_def09_repeated_checkpoint_resume_cycles():
    """DEF-09: Repeated checkpoint/resume cycles preserve full audit history and determinism."""
    loader = ScenarioLoader()
    cfg = loader.load_scenario("cooperative_pipeline")

    # Control
    k_ctrl, _ = loader.build_simulation(cfg, seed=42)
    res_ctrl = k_ctrl.run(max_ticks=20)
    ctrl_traces = k_ctrl.agents["coordinator"].get_decision_traces()

    # Cycle 1: Run to tick 2, checkpoint
    k1, _ = loader.build_simulation(cfg, seed=42)
    for _ in range(2):
        k1.step()
    snap1 = k1.snapshot()

    # Cycle 2: Restore into k2, run to tick 5, checkpoint
    k2, _ = loader.build_simulation(cfg, seed=42)
    k2.restore(snap1)
    for _ in range(3):
        k2.step()
    snap2 = k2.snapshot()

    # Cycle 3: Restore into k3, run to completion
    k3, _ = loader.build_simulation(cfg, seed=42)
    k3.restore(snap2)
    res3 = k3.run(max_ticks=20)

    res3_traces = k3.agents["coordinator"].get_decision_traces()

    assert len(res3_traces) == len(ctrl_traces)
    assert res3_traces == ctrl_traces
    assert res3.terminal_state_hash == res_ctrl.terminal_state_hash


def test_def09_malformed_checkpoint_rejection_and_trace_isolation():
    """DEF-09: Verify strict schema validation on restore and trace deep isolation."""
    worker = WorkerAgent(agent_id="w_test")
    obs = {"summary": "test_obs"}
    act = AgentAction(action_type="TEST_ACT", target="t1", parameters={"val": 10})
    worker.record_decision_trace(0, obs, act)
    snap = worker.snapshot()

    # Validation: version and counts recorded
    assert snap["version"] == 1
    assert snap["decision_traces_count"] == 1
    assert len(snap["decision_traces"]) == 1

    # 1. Trace deep isolation: mutating snapshot must not mutate agent
    snap["decision_traces"][0]["action_type"] = "MUTATED_ACTION"
    assert worker.get_decision_traces()[0]["action_type"] == "TEST_ACT"

    # 2. Reject non-dict snapshot
    with pytest.raises(ValueError, match="must be a dict"):
        worker.restore("invalid_string_snapshot")

    # 3. Reject non-list decision_traces
    bad_snap_1 = copy.deepcopy(snap)
    bad_snap_1["decision_traces"] = "not_a_list"
    with pytest.raises(ValueError, match="'decision_traces' must be a list"):
        worker.restore(bad_snap_1)

    # 4. Reject non-dict elements in decision_traces
    bad_snap_2 = copy.deepcopy(snap)
    bad_snap_2["decision_traces"] = ["not_a_dict_entry"]
    with pytest.raises(ValueError, match="must be a dict"):
        worker.restore(bad_snap_2)

    # 5. Reject mismatched decision_traces_count
    bad_snap_3 = copy.deepcopy(snap)
    bad_snap_3["decision_traces_count"] = 999  # Actual len is 1
    with pytest.raises(ValueError, match="decision_traces_count"):
        worker.restore(bad_snap_3)


# ==============================================================================
# DEF-10: Worker Preemption and Task Conservation Verification
# ==============================================================================

def test_def10_worker_preemption_rework_preserves_inflight_tasks():
    """DEF-10: Preemption by Critic rejection preserves accepted in-flight task to completion."""
    tasks = [
        {"task_id": "t1_dot", "name": "Dot Product", "status": "PENDING", "requirements": {"operation": "dot_product", "vec_a": [3, 4], "vec_b": [2, 1]}},
        {"task_id": "t2_cos", "name": "Cosine Sim (triggers rework)", "status": "PENDING", "requirements": {"operation": "cosine_similarity", "vec_a": [1, 0], "vec_b": [0, 1]}},
        {"task_id": "t3_aff", "name": "Affine Transform", "status": "PENDING", "requirements": {"operation": "affine", "base": 12, "scale": 4.5, "offset": 7.5}},
        {"task_id": "t4_pipe", "name": "Pipeline Reduce (preempted in-flight)", "status": "PENDING", "requirements": {"operation": "pipeline_reduce", "reduce_op": "product", "inputs": [2.5, 4.0, 3.0]}},
        {"task_id": "t5_anom", "name": "Anomaly Count", "status": "PENDING", "requirements": {"operation": "anomaly_count", "threshold": 2.0, "inputs": [10.0, 100.0]}},
    ]

    k = SimulationKernel(seed=888)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=10.0)
    env.attach_to_kernel(k)

    k.register_agent(CoordinatorAgent("coordinator", ["worker_math", "worker_stats"]))
    k.register_agent(WorkerAgent("worker_math", specialization="math"))
    k.register_agent(WorkerAgent("worker_stats", specialization="stats"))
    k.register_agent(CriticAgent("critic"))

    # Run full scenario
    res = k.run(max_ticks=25)
    task_map = {t["task_id"]: t for t in env.state.get("tasks")}

    # Assertions for DEF-10 fix:
    # 1. Pipeline successfully completed all tasks
    assert res.is_completed is True
    assert "ALL_TASKS_COMPLETED" in res.termination_reason

    # 2. The previously preempted task (t4_pipe) completed with correct ground truth 30.0
    assert task_map["t4_pipe"]["status"] == "COMPLETED"
    assert task_map["t4_pipe"]["result_value"] == 30

    # 3. All 5 tasks completed cleanly without ghost in-progress tasks
    for tid, t in task_map.items():
        assert t["status"] == "COMPLETED", f"Task {tid} failed to complete: status={t.get('status')}"


def test_def10_multiple_critic_rejections_and_queued_rework():
    """DEF-10: Multiple Critic rejections in rapid succession are queued and resolved without loss."""
    tasks = [
        {"task_id": "r1", "name": "Task R1", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [10, 20]}},
        {"task_id": "r2", "name": "Task R2", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [30, 40]}},
    ]
    k = SimulationKernel(seed=99)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=100.0)
    env.attach_to_kernel(k)
    w = WorkerAgent("worker_1")
    c = CriticAgent("critic")
    k.register_agent(w)
    k.register_agent(c)

    # Simulate both tasks executed with negative values (-1, -2) and submitted
    for tid, val in [("r1", -1), ("r2", -2)]:
        k._action_handlers["ACCEPT_TASK"](
            type("Act", (), {"parameters": {"task_id": tid, "worker_id": "worker_1"}, "target": tid})(), 0
        )
        k._action_handlers["EXECUTE_TASK"](
            type("Act", (), {"parameters": {"task_id": tid, "worker_id": "worker_1", "value": val}, "target": tid})(), 0
        )
        k.message_bus.send("worker_1", "critic", {
            "type": "SUBMIT_FOR_REVIEW",
            "task_id": tid,
            "submission": {"task_id": tid, "worker_id": "worker_1", "result_value": val}
        }, current_tick=0)

    # Run kernel: Critic rejects both deliverables, Worker reworks both in succession
    k.run(max_ticks=20)
    task_map = {t["task_id"]: t for t in env.state.get("tasks")}

    assert task_map["r1"]["status"] == "COMPLETED"
    assert task_map["r1"]["result_value"] == 30  # Ground truth sum(10, 20)
    assert task_map["r2"]["status"] == "COMPLETED"
    assert task_map["r2"]["result_value"] == 70  # Ground truth sum(30, 40)
    assert env.state.get("completed_count") == 2


def test_def10_competing_assignments_and_kernel_ownership_enforcement():
    """DEF-10: Multiple workers racing for same task; kernel enforces ownership and prevents duplicate execution."""
    tasks = [
        {"task_id": "race_task", "name": "Contested Task", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [5, 5]}}
    ]
    k = SimulationKernel(seed=12)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=100.0, energy_cost_per_task=10.0)
    env.attach_to_kernel(k)

    w1 = WorkerAgent("w1")
    w2 = WorkerAgent("w2")
    c = CriticAgent("critic")
    k.register_agent(w1)
    k.register_agent(w2)
    k.register_agent(c)

    # Both workers receive assignment for race_task
    k.message_bus.send("coord", "w1", {"type": "ASSIGN_TASK", "task": tasks[0]}, current_tick=0)
    k.message_bus.send("coord", "w2", {"type": "ASSIGN_TASK", "task": tasks[0]}, current_tick=0)

    # Step tick 0: w1 accepts first (alphabetical order w1 < w2)
    step0 = k.step()
    task_now = env.state.get("tasks")[0]
    assert task_now["status"] == "IN_PROGRESS"
    assert task_now["assigned_worker"] == "w1"

    # Verify unauthorized execution is strictly rejected by kernel
    unauth_act = AgentAction(
        action_type="EXECUTE_TASK",
        target="race_task",
        parameters={"task_id": "race_task", "worker_id": "w2", "value": 10}
    )
    outcome = k._action_handlers["EXECUTE_TASK"](unauth_act, 1)
    assert outcome["status"] == "REJECTED_UNAUTHORIZED_WORKER"

    # Finish run: w1 executes and completes without interference or duplicate execution
    k.run(max_ticks=10)
    final_task = env.state.get("tasks")[0]
    assert final_task["status"] == "COMPLETED"
    assert final_task["result_value"] == 10
    # Energy deducted exactly once (initial 100 - 10 = 90.0)
    assert env.state.get("energy") == 90.0


def test_def10_task_conservation_under_energy_depletion():
    """DEF-10: Conservation of accepted tasks: uncompletable tasks explicitly fail without ghost states."""
    tasks = [
        {"task_id": "t_ok", "name": "Feasible Task", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [1, 2]}},
        {"task_id": "t_starve", "name": "Starved Task", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [3, 4]}},
    ]
    # Provision only enough energy for 1 task (10.0 needed per task, 15.0 total provided)
    k = SimulationKernel(seed=55)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=15.0, energy_cost_per_task=10.0)
    env.attach_to_kernel(k)

    k.register_agent(CoordinatorAgent("coordinator", ["w1"]))
    k.register_agent(WorkerAgent("w1"))
    k.register_agent(CriticAgent("critic"))

    k.run(max_ticks=20)
    task_map = {t["task_id"]: t for t in env.state.get("tasks")}

    # Task 1 must be COMPLETED
    assert task_map["t_ok"]["status"] == "COMPLETED"
    assert task_map["t_ok"]["result_value"] == 3

    # Task 2 attempted with insufficient energy (5.0 < 10.0): must transition to FAILED
    # and must NOT remain trapped as an indefinite ghost IN_PROGRESS task!
    assert task_map["t_starve"]["status"] == "FAILED"
    assert task_map["t_starve"]["failure_reason"] == "ENERGY_DEPLETED"

    # Task conservation invariant: completed + failed == total attempted
    completed = env.state.get("completed_count")
    failed = env.state.get("failed_count")
    assert completed == 1
    assert failed == 1
    assert completed + failed == len(tasks)
