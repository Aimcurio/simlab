"""DEF-12 Targeted Remediation and Adversarial Qualification Test Suite.

Authoritative verification for:
- Exact zero computational outputs (orthogonal cosine similarity, zero anomalies, zero deltas).
- Negative dot products, negative cosine similarities, and negative coordinate deltas.
- Large-magnitude results beyond former (0, 500] bounds.
- Rejection of superficially plausible in-range results (e.g. 42 for a task requiring 120).
- Acceptance of legitimate 42 without spurious rejection.
- Invalid numeric representations (NaN, inf, booleans masquerading as numbers).
- Undefined cosine similarity for zero-length and zero-norm vectors.
- Critic rejection and Worker recalculation behavior without fabricated fallbacks.
- Coordinator completion correctness without concealing mathematical failures.
- Multi-worker execution, preemption, checkpoint restoration, and deterministic replay.
"""

import copy
import math
import numpy as np
import pytest

from simlab.core.kernel import SimulationKernel
from simlab.core.replay import ReplayEngine
from simlab.agents.base import AgentAction
from simlab.agents.coordinator import CoordinatorAgent
from simlab.agents.worker import WorkerAgent
from simlab.agents.critic import CriticAgent
from simlab.agents.models import (
    evaluate_functional_task,
    validate_and_convert_number,
    validate_and_convert_vector,
)
from simlab.environment.cooperative_task import CooperativeTaskEnvironment


# ==============================================================================
# 1. Exact Zero Outputs
# ==============================================================================

def test_def12_exact_zero_outputs_preserved_and_approved():
    """DEF-12: Zero-valued results across operations are preserved and approved without 42 substitution."""
    tasks = [
        {
            "task_id": "z_cos",
            "name": "Orthogonal Cosine Similarity",
            "status": "PENDING",
            "requirements": {
                "operation": "cosine_similarity",
                "vec_a": [1.0, 0.0],
                "vec_b": [0.0, 1.0]
            }
        },
        {
            "task_id": "z_anom",
            "name": "Zero Anomaly Count",
            "status": "PENDING",
            "requirements": {
                "operation": "anomaly_count",
                "inputs": [10.0, 10.0, 10.0],
                "threshold": 2.0
            }
        },
        {
            "task_id": "z_delta",
            "name": "Zero Coordinate Delta",
            "status": "PENDING",
            "requirements": {
                "operation": "delta",
                "start": 15.5,
                "end": 15.5
            }
        },
        {
            "task_id": "z_dot",
            "name": "Orthogonal 3D Dot Product",
            "status": "PENDING",
            "requirements": {
                "operation": "dot_product",
                "vec_a": [1.0, 0.0, 0.0],
                "vec_b": [0.0, 1.0, 0.0]
            }
        },
        {
            "task_id": "z_sum",
            "name": "Balanced Zero Sum",
            "status": "PENDING",
            "requirements": {
                "operation": "sum",
                "inputs": [10.5, -10.5]
            }
        },
        {
            "task_id": "z_reconcile",
            "name": "Zero Record Difference",
            "status": "PENDING",
            "requirements": {
                "operation": "record_reconcile",
                "records_a": ["id_1", "id_2"],
                "records_b": ["id_2", "id_1"]
            }
        }
    ]

    kernel = SimulationKernel(seed=42)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=5.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", ["worker_1"]))
    kernel.register_agent(WorkerAgent("worker_1"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=35)
    assert res.is_completed is True
    assert "ALL_TASKS_COMPLETED" in res.termination_reason

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}

    expected_zeros = {
        "z_cos": 0.0,
        "z_anom": 0,
        "z_delta": 0,
        "z_dot": 0,
        "z_sum": 0,
        "z_reconcile": 0
    }

    for tid, exp in expected_zeros.items():
        t = task_map[tid]
        assert t["status"] == "COMPLETED", f"Task {tid} status is {t.get('status')}"
        assert t["result_value"] == exp, f"Task {tid} expected {exp}, got {t.get('result_value')}"
        assert t["result_value"] != 42, f"Task {tid} was incorrectly substituted with fallback 42"


# ==============================================================================
# 2. Negative Dot Products, Cosine Similarities, and Coordinate Deltas
# ==============================================================================

def test_def12_negative_mathematical_results():
    """DEF-12: Negative outputs are recognized as valid and verified against independent oracles."""
    tasks = [
        {
            "task_id": "neg_dot",
            "name": "Opposing Dot Product",
            "status": "PENDING",
            "requirements": {
                "operation": "dot_product",
                "vec_a": [2.0, 3.0],
                "vec_b": [-1.0, -2.0]  # 2*(-1) + 3*(-2) = -8
            }
        },
        {
            "task_id": "neg_cos",
            "name": "Antiparallel Cosine Similarity",
            "status": "PENDING",
            "requirements": {
                "operation": "cosine_similarity",
                "vec_a": [1.0, 0.0],
                "vec_b": [-1.0, 0.0]  # cos = -1.0
            }
        },
        {
            "task_id": "neg_delta",
            "name": "Decreasing Coordinate Delta",
            "status": "PENDING",
            "requirements": {
                "operation": "delta",
                "start": 50.0,
                "end": 20.0  # 20 - 50 = -30
            }
        },
        {
            "task_id": "neg_affine",
            "name": "Negative Linear Transformation",
            "status": "PENDING",
            "requirements": {
                "operation": "affine",
                "base": 10.0,
                "scale": -3.0,
                "offset": -5.0  # 10 * (-3) + (-5) = -35
            }
        }
    ]

    kernel = SimulationKernel(seed=101)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=5.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", ["worker_1"]))
    kernel.register_agent(WorkerAgent("worker_1"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=25)
    assert res.is_completed is True

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    assert task_map["neg_dot"]["result_value"] == -8
    assert task_map["neg_cos"]["result_value"] == -1.0
    assert task_map["neg_delta"]["result_value"] == -30
    assert task_map["neg_affine"]["result_value"] == -35


# ==============================================================================
# 3. Large-Magnitude Results Beyond Former Bounds (0, 500]
# ==============================================================================

def test_def12_large_magnitudes_beyond_bounds():
    """DEF-12: Results outside the former (0, 500] interval are approved when mathematically correct."""
    tasks = [
        {
            "task_id": "large_pos_sum",
            "name": "Large Positive Sum",
            "status": "PENDING",
            "requirements": {
                "operation": "sum",
                "inputs": [1000.0, 2500.0, 4500.0]  # 8000
            }
        },
        {
            "task_id": "large_dot",
            "name": "Large Vector Dot Product",
            "status": "PENDING",
            "requirements": {
                "operation": "dot_product",
                "vec_a": [1000.0, 2000.0],
                "vec_b": [3000.0, 4000.0]  # 3,000,000 + 8,000,000 = 11,000,000
            }
        },
        {
            "task_id": "large_neg_sum",
            "name": "Large Negative Sum",
            "status": "PENDING",
            "requirements": {
                "operation": "sum",
                "inputs": [-2000.0, -8000.0]  # -10000
            }
        }
    ]

    kernel = SimulationKernel(seed=202)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=5.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", ["worker_1"]))
    kernel.register_agent(WorkerAgent("worker_1"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=20)
    assert res.is_completed is True

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    assert task_map["large_pos_sum"]["result_value"] == 8000
    assert task_map["large_dot"]["result_value"] == 11000000
    assert task_map["large_neg_sum"]["result_value"] == -10000


# ==============================================================================
# 4. Rejection of Superficially Plausible In-Range Results
# ==============================================================================

def test_def12_rejection_of_superficially_plausible_in_range_values():
    """DEF-12: Critic rejects in-range wrong results (e.g. 42 for 120.0), forces rework, and accepts ground truth."""
    tasks = [
        {
            "task_id": "oracle_audit",
            "name": "Targeted Calculation",
            "status": "PENDING",
            "requirements": {
                "operation": "sum",
                "inputs": [50.0, 70.0]  # Ground truth is 120.0
            }
        }
    ]

    kernel = SimulationKernel(seed=303)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=100.0, energy_cost_per_task=10.0)
    env.attach_to_kernel(kernel)

    w = WorkerAgent("worker_1")
    c = CriticAgent("critic")
    kernel.register_agent(CoordinatorAgent("coordinator", ["worker_1"]))
    kernel.register_agent(w)
    kernel.register_agent(c)

    # Inject worker accepting and executing with superficially plausible value 42
    kernel._action_handlers["ACCEPT_TASK"](
        type("Act", (), {"parameters": {"task_id": "oracle_audit", "worker_id": "worker_1"}, "target": "oracle_audit"})(), 0
    )
    kernel._action_handlers["EXECUTE_TASK"](
        type("Act", (), {"parameters": {"task_id": "oracle_audit", "worker_id": "worker_1", "value": 42}, "target": "oracle_audit"})(), 0
    )

    # Submit 42 to critic (42 is within old bounds (0, 500], but mathematically incorrect!)
    kernel.message_bus.send("worker_1", "critic", {
        "type": "SUBMIT_FOR_REVIEW",
        "task_id": "oracle_audit",
        "submission": {"task_id": "oracle_audit", "worker_id": "worker_1", "result_value": 42}
    }, current_tick=0)

    # Run kernel: Critic rejects 42 because oracle is 120, Worker re-evaluates and submits 120
    kernel.run(max_ticks=15)

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    assert task_map["oracle_audit"]["status"] == "COMPLETED"
    assert task_map["oracle_audit"]["result_value"] == 120, "Must be true ground truth 120, not 42"
    assert c._rejections_count >= 1, "Critic must have rejected the incorrect value 42"
    assert c._approvals_count >= 1, "Critic must have approved the recomputed 120"


# ==============================================================================
# 5. Legitimate Result of 42 is Accepted Without Discrimination
# ==============================================================================

def test_def12_legitimate_result_of_42_is_accepted():
    """DEF-12: A valid calculation yielding 42 is approved on first attempt without rejection."""
    tasks = [
        {
            "task_id": "legit_42_sum",
            "name": "Legitimate 42 via Sum",
            "status": "PENDING",
            "requirements": {
                "operation": "sum",
                "inputs": [40.0, 2.0]  # Mathematically 42
            }
        },
        {
            "task_id": "legit_42_delta",
            "name": "Legitimate 42 via Delta",
            "status": "PENDING",
            "requirements": {
                "operation": "delta",
                "start": 8.0,
                "end": 50.0  # Mathematically 42
            }
        }
    ]

    kernel = SimulationKernel(seed=404)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=100.0, energy_cost_per_task=10.0)
    env.attach_to_kernel(kernel)

    critic = CriticAgent("critic")
    kernel.register_agent(CoordinatorAgent("coordinator", ["worker_1"]))
    kernel.register_agent(WorkerAgent("worker_1"))
    kernel.register_agent(critic)

    res = kernel.run(max_ticks=15)
    assert res.is_completed is True

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    assert task_map["legit_42_sum"]["result_value"] == 42
    assert task_map["legit_42_delta"]["result_value"] == 42
    # Verify zero rejections occurred: 42 was accepted on first pass!
    assert critic._rejections_count == 0
    assert critic._approvals_count == 2


# ==============================================================================
# 6. Malformed Inputs, Booleans Masquerading as Numbers, and NaN / Inf Handling
# ==============================================================================

def test_def12_malformed_numeric_representations_rejected():
    """DEF-12: Booleans, NaN, Inf, and malformed inputs are rejected with TypeError/ValueError."""
    # Booleans masquerading as numbers
    with pytest.raises(TypeError, match="boolean value"):
        validate_and_convert_number(True)
    with pytest.raises(TypeError, match="boolean value"):
        validate_and_convert_number(False)
    with pytest.raises(TypeError, match="boolean value"):
        evaluate_functional_task({"requirements": {"operation": "sum", "inputs": [True, 1.0]}})

    # NaN and Infinities
    with pytest.raises(ValueError, match="NaN"):
        validate_and_convert_number(float("nan"))
    with pytest.raises(ValueError, match="NaN"):
        evaluate_functional_task({"requirements": {"operation": "sum", "inputs": [float("nan"), 10.0]}})
    with pytest.raises(ValueError, match="Infinite"):
        validate_and_convert_number(float("inf"))
    with pytest.raises(ValueError, match="Infinite"):
        evaluate_functional_task({"requirements": {"operation": "sum", "inputs": [float("-inf"), 10.0]}})

    # Non-numeric string
    with pytest.raises(TypeError, match="Cannot parse numeric"):
        validate_and_convert_number("not_a_number")

    # Mismatched vector dimensions in dot_product
    with pytest.raises(ValueError, match="dimension mismatch"):
        evaluate_functional_task({
            "requirements": {
                "operation": "dot_product",
                "vec_a": [1.0, 2.0],
                "vec_b": [1.0, 2.0, 3.0]
            }
        })

    # Singular matrix in linear_solve
    with pytest.raises(ValueError, match="singular"):
        evaluate_functional_task({
            "requirements": {
                "operation": "linear_solve",
                "matrix_a": [[1.0, 1.0], [1.0, 1.0]],
                "vector_b": [2.0, 2.0]
            }
        })


# ==============================================================================
# 7. Undefined Cosine Similarity for Zero-Length and Zero-Norm Vectors
# ==============================================================================

def test_def12_undefined_cosine_similarity():
    """DEF-12: Cosine similarity for zero-length or zero-norm vectors raises explicit ValueError."""
    # Zero-length vectors
    with pytest.raises(ValueError, match="zero-length"):
        evaluate_functional_task({
            "requirements": {
                "operation": "cosine_similarity",
                "vec_a": [],
                "vec_b": []
            }
        })

    # Zero-norm vector (division by zero norm)
    with pytest.raises(ValueError, match="zero-norm"):
        evaluate_functional_task({
            "requirements": {
                "operation": "cosine_similarity",
                "vec_a": [0.0, 0.0],
                "vec_b": [1.0, 0.0]
            }
        })


# ==============================================================================
# 8. Critic Representation vs Oracle Verification & No 42 Suggestions
# ==============================================================================

def test_def12_critic_no_fabricated_suggestions_and_oracle_validation():
    """DEF-12: Critic rejection does NOT suggest 42 and distinguishes representation from correctness."""
    critic = CriticAgent("critic")
    state = {
        "tasks": [
            {
                "task_id": "task_sqrt_approx",
                "requirements": {
                    "operation": "delta",
                    "start": 10.0,
                    "end": 0.0  # Oracle is -10.0
                }
            }
        ]
    }

    # 1. Observe state to learn task contracts
    obs = critic.observe(state, incoming_messages=[], current_tick=0)
    assert obs["review_criteria"]["disallow_fabricated_fallbacks"] is True

    # 2. Worker submits wrong answer (e.g. 50.0)
    class WrongSubmissionMsg:
        sender_id = "worker_1"
        content = {
            "type": "SUBMIT_FOR_REVIEW",
            "task_id": "task_sqrt_approx",
            "submission": {"task_id": "task_sqrt_approx", "result_value": 50.0}
        }
        sent_tick = 1

    obs = critic.observe(state, incoming_messages=[WrongSubmissionMsg()], current_tick=1)
    act = critic.decide(obs, current_tick=1)

    assert act.action_type == "SEND_MESSAGE"
    content = act.parameters["content"]
    assert content["verdict"] == "REJECTED"
    # CRITICAL: No fabricated value 42 suggested!
    assert "suggested_value" not in content, "Critic must not suggest arbitrary fallback 42"
    assert "does not match authoritative oracle" in content["feedback"]


# ==============================================================================
# 9. Coordinator Truthful Completion Reporting (No Concealed Failures)
# ==============================================================================

def test_def12_coordinator_truthfully_reports_failures():
    """DEF-12: Coordinator does not report ALL_TASKS_COMPLETE when mathematical failures occur."""
    tasks = [
        {
            "task_id": "valid_task",
            "name": "Valid Math Task",
            "status": "PENDING",
            "requirements": {"operation": "sum", "inputs": [10.0, 20.0]}
        },
        {
            "task_id": "uncomputable_task",
            "name": "Zero-Length Cosine Similarity",
            "status": "PENDING",
            "requirements": {"operation": "cosine_similarity", "vec_a": [], "vec_b": []}
        }
    ]

    kernel = SimulationKernel(seed=505)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=100.0, energy_cost_per_task=10.0)
    env.attach_to_kernel(kernel)

    coord = CoordinatorAgent("coordinator", ["worker_1"])
    kernel.register_agent(coord)
    kernel.register_agent(WorkerAgent("worker_1"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=25)

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}

    # Valid task completed
    assert task_map["valid_task"]["status"] == "COMPLETED"
    assert task_map["valid_task"]["result_value"] == 30

    # Uncomputable task explicitly failed
    assert task_map["uncomputable_task"]["status"] == "FAILED"
    assert "zero-length" in task_map["uncomputable_task"]["failure_reason"]

    # Termination reason must truthfully report failures, NOT claim all completed
    assert "TASKS_TERMINATED_WITH_FAILURES" in res.termination_reason
    assert "ALL_TASKS_COMPLETED" not in res.termination_reason

    # Coordinator decision traces must NOT report ALL_TASKS_COMPLETE
    final_traces = coord.get_decision_traces()
    all_statuses = [tr.get("parameters", {}).get("status") for tr in final_traces]
    assert "ALL_TASKS_COMPLETE" not in all_statuses, "Coordinator must not report ALL_TASKS_COMPLETE when failures exist"

    # When observing the resolved state with failures, coordinator truthfully reports TASKS_FAILED
    post_obs = coord.observe(env.state.to_dict(), [], res.total_ticks + 1)
    post_act = coord.decide(post_obs, res.total_ticks + 1)
    assert post_act.parameters.get("status") == "TASKS_FAILED"
    assert post_act.parameters.get("failed_count") == 1
    assert "uncomputable_task" in post_act.parameters.get("failed_tasks", [])


# ==============================================================================
# 10. Multi-Worker Execution, Preemption, Checkpoint Restore & Replay Determinism
# ==============================================================================

def test_def12_multiworker_preemption_checkpoint_and_replay_determinism():
    """DEF-12: Full integration test with heterogeneous zero/negative/large tasks, preemption, and bit-for-bit replay."""
    tasks = [
        {"task_id": "t1_zero", "name": "Orthogonal Cos", "status": "PENDING", "requirements": {"operation": "cosine_similarity", "vec_a": [1, 0], "vec_b": [0, 1]}},
        {"task_id": "t2_neg", "name": "Negative Delta", "status": "PENDING", "requirements": {"operation": "delta", "start": 100, "end": 25}},
        {"task_id": "t3_large", "name": "Large Sum", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [2500, 3500]}},
        {"task_id": "t4_legit42", "name": "Legitimate 42", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [40, 2]}},
        {"task_id": "t5_anom", "name": "Zero Anomaly", "status": "PENDING", "requirements": {"operation": "anomaly_count", "inputs": [5.0, 5.0, 5.0], "threshold": 2.0}},
    ]

    # 1. Control Run
    k_ctrl = SimulationKernel(seed=789)
    env_ctrl = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=10.0)
    env_ctrl.attach_to_kernel(k_ctrl)
    k_ctrl.register_agent(CoordinatorAgent("coordinator", ["w1", "w2"]))
    k_ctrl.register_agent(WorkerAgent("w1", specialization="math"))
    k_ctrl.register_agent(WorkerAgent("w2", specialization="stats"))
    k_ctrl.register_agent(CriticAgent("critic"))

    res_ctrl = k_ctrl.run(max_ticks=30)
    assert res_ctrl.is_completed is True
    assert "ALL_TASKS_COMPLETED" in res_ctrl.termination_reason

    ctrl_tasks = {t["task_id"]: t for t in env_ctrl.state.get("tasks")}
    assert ctrl_tasks["t1_zero"]["result_value"] == 0.0
    assert ctrl_tasks["t2_neg"]["result_value"] == -75
    assert ctrl_tasks["t3_large"]["result_value"] == 6000
    assert ctrl_tasks["t4_legit42"]["result_value"] == 42
    assert ctrl_tasks["t5_anom"]["result_value"] == 0

    # 2. Causal Replay Verification: replay bit-for-bit
    replayer = ReplayEngine(k_ctrl.logger.to_list())
    valid_chain, chain_err = replayer.verify_integrity()
    assert valid_chain is True, f"Causal integrity failed: {chain_err}"

    # 3. Checkpoint & Resume Equivalence
    k_res = SimulationKernel(seed=789)
    env_res = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=10.0)
    env_res.attach_to_kernel(k_res)
    k_res.register_agent(CoordinatorAgent("coordinator", ["w1", "w2"]))
    k_res.register_agent(WorkerAgent("w1", specialization="math"))
    k_res.register_agent(WorkerAgent("w2", specialization="stats"))
    k_res.register_agent(CriticAgent("critic"))

    # Step 5 ticks then checkpoint
    for _ in range(5):
        k_res.step()
    checkpoint_snap = k_res.snapshot()

    # Restore in new kernel instance and finish
    k_res2 = SimulationKernel(seed=789)
    env_res2 = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=10.0)
    env_res2.attach_to_kernel(k_res2)
    k_res2.register_agent(CoordinatorAgent("coordinator", ["w1", "w2"]))
    k_res2.register_agent(WorkerAgent("w1", specialization="math"))
    k_res2.register_agent(WorkerAgent("w2", specialization="stats"))
    k_res2.register_agent(CriticAgent("critic"))
    k_res2.restore(checkpoint_snap)

    res_res2 = k_res2.run(max_ticks=30)
    assert res_res2.terminal_state_hash == res_ctrl.terminal_state_hash
    assert res_res2.total_ticks == res_ctrl.total_ticks
