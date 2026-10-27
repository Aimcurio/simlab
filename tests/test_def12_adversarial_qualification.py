"""Independent Adversarial Qualification Suite for DEF-12.

Conducted by: Independent Principal Multi-Agent Systems Engineer,
Mathematical Correctness Specialist, and Adversarial Software Qualification Lead.

This suite provides deep adversarial testing across all mathematical operations,
domain boundaries, type representations, worker retry/exhaustion paths,
critic oracle verification, coordinator truthful completion authority,
and multi-agent lifecycle invariants.
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
# 1. Independent Mathematical Oracle for Comprehensive Operations
# ==============================================================================

class IndependentMathOracle:
    """Independent ground-truth oracle constructed separately from SimLab implementation."""

    @staticmethod
    def eval(req: dict):
        op = req.get("operation")
        inputs = req.get("inputs", [])

        if op == "cosine_similarity":
            a = np.array(req["vec_a"], dtype=float)
            b = np.array(req["vec_b"], dtype=float)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            if len(a) == 0 or len(b) == 0:
                raise ValueError("zero-length")
            if norm_a == 0 or norm_b == 0:
                raise ValueError("zero-norm")
            cos = float(np.dot(a, b) / (norm_a * norm_b))
            return round(max(-1.0, min(1.0, cos)), 6)

        elif op == "anomaly_count":
            thresh = float(req.get("threshold", 2.0))
            if thresh < 0:
                raise ValueError("negative threshold")
            if not inputs:
                return 0
            arr = np.array(inputs, dtype=float)
            std = np.std(arr, ddof=0)
            if std == 0.0:
                return 0
            z = np.abs((arr - np.mean(arr)) / std)
            return int(np.sum(z > thresh))

        elif op in ("delta", "linear_difference"):
            start = float(req.get("start", inputs[0] if inputs else 0.0))
            end = float(req.get("end", inputs[1] if len(inputs) > 1 else 0.0))
            res = round(end - start, 6)
            return int(res) if res.is_integer() else res

        elif op == "dot_product":
            a = np.array(req.get("vec_a", inputs[0] if inputs else []), dtype=float)
            b = np.array(req.get("vec_b", inputs[1] if len(inputs) > 1 else []), dtype=float)
            if len(a) != len(b):
                raise ValueError("mismatch")
            if len(a) == 0:
                raise ValueError("zero-length")
            res = round(float(np.dot(a, b)), 6)
            return int(res) if res.is_integer() else res

        elif op == "linear_solve":
            A = np.array(req["matrix_a"], dtype=float)
            b = np.array(req["vector_b"], dtype=float)
            if A.ndim != 2 or A.shape[0] != A.shape[1] or len(b) != A.shape[0]:
                raise ValueError("shape mismatch")
            if math.isclose(np.linalg.det(A), 0.0, abs_tol=1e-12):
                raise ValueError("singular")
            sol = np.linalg.solve(A, b)
            res = round(float(np.sum(sol)), 6)
            return int(res) if res.is_integer() else res

        elif op == "polynomial":
            coeffs = [float(c) for c in req.get("coefficients", inputs)]
            x = float(req.get("x", 1.0))
            total = sum(c * (x ** i) for i, c in enumerate(coeffs))
            res = round(total, 6)
            return int(res) if res.is_integer() else res

        elif op == "sum":
            res = round(sum(float(x) for x in inputs), 6) if inputs else 0
            return int(res) if isinstance(res, float) and res.is_integer() else res

        elif op == "mean":
            res = round(sum(float(x) for x in inputs) / len(inputs), 6) if inputs else 0.0
            return int(res) if isinstance(res, float) and res.is_integer() else res

        elif op == "variance":
            ddof = int(req.get("ddof", 0))
            res = round(float(np.var([float(x) for x in inputs], ddof=ddof)), 6) if len(inputs) > ddof else 0.0
            return int(res) if isinstance(res, float) and res.is_integer() else res

        elif op == "std":
            ddof = int(req.get("ddof", 0))
            res = round(float(np.std([float(x) for x in inputs], ddof=ddof)), 6) if len(inputs) > ddof else 0.0
            return int(res) if isinstance(res, float) and res.is_integer() else res

        raise ValueError(f"Unknown op {op}")


# ==============================================================================
# 2. Comprehensive Exhaustive Zero Results
# ==============================================================================

def test_adversarial_exhaustive_zero_valued_operations():
    """Adversarial qualification: ALL mathematical operations yielding exact 0 must be approved unchanged."""
    cases = [
        # (task_id, requirements, expected_oracle)
        ("adv_cos_4d_ortho", {"operation": "cosine_similarity", "vec_a": [0, 1, 0, 0], "vec_b": [1, 0, 0, 0]}, 0.0),
        ("adv_cos_3d_ortho", {"operation": "cosine_similarity", "vec_a": [0, 0, 5], "vec_b": [3, -2, 0]}, 0.0),
        ("adv_anom_identical", {"operation": "anomaly_count", "inputs": [42.0, 42.0, 42.0, 42.0], "threshold": 1.0}, 0),
        ("adv_anom_within_thresh", {"operation": "anomaly_count", "inputs": [10.0, 11.0, 10.5, 9.5], "threshold": 3.0}, 0),
        ("adv_delta_zero", {"operation": "delta", "start": -250.75, "end": -250.75}, 0),
        ("adv_dot_zero", {"operation": "dot_product", "vec_a": [2, -4], "vec_b": [4, 2]}, 0),
        ("adv_sum_zero", {"operation": "sum", "inputs": [-1000, 500, 500]}, 0),
        ("adv_mean_zero", {"operation": "mean", "inputs": [-30.0, 0.0, 30.0]}, 0),
        ("adv_variance_zero", {"operation": "variance", "inputs": [9.0, 9.0, 9.0]}, 0),
        ("adv_std_zero", {"operation": "std", "inputs": [17.5, 17.5, 17.5]}, 0),
        ("adv_poly_zero", {"operation": "polynomial", "coefficients": [-8.0, 2.0], "x": 4.0}, 0),  # -8 + 2*4 = 0
        ("adv_weighted_sum_zero", {"operation": "weighted_sum", "inputs": [10, 20], "weights": [2, -1]}, 0),
        ("adv_filter_sum_zero", {"operation": "filter_sum", "inputs": [10, -10, 50], "max_val": 20}, 0),
        ("adv_linear_solve_zero", {"operation": "linear_solve", "matrix_a": [[2.0, 1.0], [1.0, 2.0]], "vector_b": [0.0, 0.0]}, 0),
    ]

    tasks = [
        {"task_id": cid, "name": cid, "status": "PENDING", "requirements": req}
        for cid, req, _ in cases
    ]

    kernel = SimulationKernel(seed=12345)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=500.0, energy_cost_per_task=5.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", ["w1", "w2"]))
    kernel.register_agent(WorkerAgent("w1"))
    kernel.register_agent(WorkerAgent("w2"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=60)
    assert res.is_completed is True, f"Simulation incomplete: {res.termination_reason}"
    assert "ALL_TASKS_COMPLETED" in res.termination_reason

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    for cid, req, exp in cases:
        t = task_map[cid]
        assert t["status"] == "COMPLETED", f"Task {cid} failed with status {t.get('status')}"
        actual = t["result_value"]
        assert actual == exp or math.isclose(actual, exp, abs_tol=1e-5), f"Task {cid}: expected {exp}, got {actual}"
        # Independent oracle confirmation
        oracle_exp = IndependentMathOracle.eval(req) if req["operation"] != "filter_sum" and req["operation"] != "weighted_sum" else exp
        assert actual == oracle_exp or math.isclose(actual, oracle_exp, abs_tol=1e-5)


# ==============================================================================
# 3. Exhaustive Negative & Large-Magnitude Results
# ==============================================================================

def test_adversarial_negative_and_extreme_magnitude_operations():
    """Adversarial qualification: Negative and large magnitude values must never be truncated or rejected."""
    cases = [
        ("adv_neg_cos_antiparallel", {"operation": "cosine_similarity", "vec_a": [0, -5], "vec_b": [0, 10]}, -1.0),
        ("adv_neg_cos_obtuse", {"operation": "cosine_similarity", "vec_a": [1, 1], "vec_b": [-1, 0]}, round(-1.0 / math.sqrt(2), 6)),
        ("adv_neg_dot", {"operation": "dot_product", "vec_a": [-10, 2], "vec_b": [5, -3]}, -56),
        ("adv_neg_delta", {"operation": "delta", "start": 1000.0, "end": -500.0}, -1500),
        ("adv_neg_poly", {"operation": "polynomial", "coefficients": [0.0, 0.0, 1.0], "x": -5.0}, 25),
        ("adv_neg_poly_val", {"operation": "polynomial", "coefficients": [-100.0, 1.0], "x": 10.0}, -90),
        ("adv_large_sum", {"operation": "sum", "inputs": [100_000_000, 250_000_000, 650_000_000]}, 1_000_000_000),
        ("adv_large_neg_sum", {"operation": "sum", "inputs": [-500_000_000, -750_000_000]}, -1_250_000_000),
        ("adv_large_dot", {"operation": "dot_product", "vec_a": [1_000_000, 2_000_000], "vec_b": [3_000_000, 4_000_000]}, 11_000_000_000_000),
        ("adv_linear_solve_neg", {"operation": "linear_solve", "matrix_a": [[1.0, 0.0], [0.0, 1.0]], "vector_b": [-15.0, -25.0]}, -40),
    ]

    tasks = [
        {"task_id": cid, "name": cid, "status": "PENDING", "requirements": req}
        for cid, req, _ in cases
    ]

    kernel = SimulationKernel(seed=999)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=500.0, energy_cost_per_task=5.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", ["w1"]))
    kernel.register_agent(WorkerAgent("w1"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=50)
    assert res.is_completed is True
    assert "ALL_TASKS_COMPLETED" in res.termination_reason

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    for cid, req, exp in cases:
        t = task_map[cid]
        assert t["status"] == "COMPLETED"
        actual = t["result_value"]
        assert math.isclose(actual, exp, rel_tol=1e-5, abs_tol=1e-5), f"Task {cid}: expected {exp}, got {actual}"


# ==============================================================================
# 4. Strict Type Safety & Malformed Numeric Injection
# ==============================================================================

def test_adversarial_malformed_types_and_infinities():
    """Adversarial qualification: Booleans, NaN, Inf, non-numeric strings must fail-closed."""
    # Booleans are explicitly rejected
    with pytest.raises(TypeError, match="boolean value"):
        validate_and_convert_number(True)
    with pytest.raises(TypeError, match="boolean value"):
        validate_and_convert_number(False)
    with pytest.raises(TypeError, match="boolean value"):
        validate_and_convert_vector([1.0, False])

    # NaN and Inf
    with pytest.raises(ValueError, match="NaN"):
        validate_and_convert_number(float("nan"))
    with pytest.raises(ValueError, match="NaN"):
        validate_and_convert_number(np.nan)
    with pytest.raises(ValueError, match="Infinite"):
        validate_and_convert_number(float("inf"))
    with pytest.raises(ValueError, match="Infinite"):
        validate_and_convert_number(float("-inf"))

    # Strings representing NaN and Inf
    with pytest.raises(ValueError, match="NaN"):
        validate_and_convert_number("nan")
    with pytest.raises(ValueError, match="Infinite"):
        validate_and_convert_number("inf")
    with pytest.raises(ValueError, match="Infinite"):
        validate_and_convert_number("-infinity")

    # Domain errors in operations
    with pytest.raises(ValueError, match="zero-norm"):
        evaluate_functional_task({"requirements": {"operation": "cosine_similarity", "vec_a": [0, 0, 0], "vec_b": [1, 2, 3]}})

    with pytest.raises(ValueError, match="zero-length"):
        evaluate_functional_task({"requirements": {"operation": "cosine_similarity", "vec_a": [], "vec_b": []}})

    with pytest.raises(ValueError, match="dimension mismatch"):
        evaluate_functional_task({"requirements": {"operation": "cosine_similarity", "vec_a": [1, 2], "vec_b": [1, 2, 3]}})

    with pytest.raises(ValueError, match="singular"):
        evaluate_functional_task({"requirements": {"operation": "linear_solve", "matrix_a": [[2, 4], [1, 2]], "vector_b": [1, 2]}})

    with pytest.raises(ValueError, match="non-negative"):
        evaluate_functional_task({"requirements": {"operation": "anomaly_count", "inputs": [1, 2, 3], "threshold": -0.5}})

    with pytest.raises(ValueError, match="at least 1"):
        evaluate_functional_task({"requirements": {"operation": "moving_average", "inputs": [1, 2, 3], "window": 0}})

    with pytest.raises(ValueError, match="Unsupported operation"):
        evaluate_functional_task({"requirements": {"operation": "unsupported_math_op_xyz"}})


# ==============================================================================
# 5. Critic Oracle Verification & No Fabricated Value Injection
# ==============================================================================

def test_adversarial_critic_rejection_payloads_never_contain_42():
    """Adversarial qualification: Critic feedback never suggests 42 and strictly enforces contracts."""
    critic = CriticAgent("critic")
    state = {
        "tasks": [
            {"task_id": "t_audit", "requirements": {"operation": "sum", "inputs": [10.0, 90.0]}},
            {"task_id": "t_cos", "requirements": {"operation": "cosine_similarity", "vec_a": [1, 0], "vec_b": [0, 1]}}
        ]
    }
    critic.observe(state, [], 0)

    # 1. Worker submits wrong value 42 for task requiring 100
    class MsgWrongVal:
        sender_id = "worker_1"
        content = {
            "type": "SUBMIT_FOR_REVIEW",
            "task_id": "t_audit",
            "submission": {"task_id": "t_audit", "result_value": 42}
        }
        sent_tick = 1

    obs = critic.observe(state, [MsgWrongVal()], 1)
    act = critic.decide(obs, 1)
    assert act.action_type == "SEND_MESSAGE"
    content = act.parameters["content"]
    assert content["verdict"] == "REJECTED"
    assert "suggested_value" not in content, "Critic must NOT inject arbitrary suggested_value"
    assert "42" not in str(content.get("suggested_value", ""))

    # 2. Worker submits out-of-domain cosine similarity (e.g. 1.2)
    class MsgDomainViolation:
        sender_id = "worker_1"
        content = {
            "type": "SUBMIT_FOR_REVIEW",
            "task_id": "t_cos",
            "submission": {"task_id": "t_cos", "result_value": 1.2}
        }
        sent_tick = 2

    obs = critic.observe(state, [MsgDomainViolation()], 2)
    act = critic.decide(obs, 2)
    assert act.action_type == "SEND_MESSAGE"
    content = act.parameters["content"]
    assert content["verdict"] == "REJECTED"
    assert "violates cosine similarity domain bounds" in content["feedback"]
    assert "suggested_value" not in content


# ==============================================================================
# 6. Worker Retry, Correction, and Exhaustion Paths
# ==============================================================================

def test_adversarial_worker_exhaustion_on_repeated_rejection():
    """Adversarial qualification: When rework is rejected > 3 times in kernel, Worker emits FAIL_TASK."""
    class AlwaysRejectingCritic(CriticAgent):
        """Mock critic that always rejects worker submission with incremented retry count."""
        def __init__(self, agent_id="critic"):
            super().__init__(agent_id=agent_id)
            self.rejection_calls = 0

        def decide(self, observation, current_tick):
            if not self._submission_queue:
                return AgentAction(action_type="STANDBY")
            sub = self._submission_queue.pop(0)
            self.rejection_calls += 1
            worker_id = sub["sender"]
            task_id = sub["task_id"]
            return AgentAction(
                action_type="SEND_MESSAGE",
                target=worker_id,
                parameters={
                    "recipient_id": worker_id,
                    "content": {
                        "type": "REVIEW_FEEDBACK",
                        "task_id": task_id,
                        "verdict": "REJECTED",
                        "retry_count": self.rejection_calls,
                        "unrecoverable": False,
                        "feedback": f"Adversarial persistent rejection #{self.rejection_calls}"
                    }
                }
            )

    tasks = [{"task_id": "t_persist_fail", "name": "Persistent Failure Task", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [1, 2]}}]

    kernel = SimulationKernel(seed=888)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=5.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", ["w1"]))
    worker = WorkerAgent("w1")
    kernel.register_agent(worker)
    kernel.register_agent(AlwaysRejectingCritic("critic"))

    res = kernel.run(max_ticks=30)

    # Must terminate with failures because retries exhausted
    assert "TASKS_TERMINATED_WITH_FAILURES" in res.termination_reason
    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    assert task_map["t_persist_fail"]["status"] == "FAILED"
    assert "Adversarial persistent rejection" in task_map["t_persist_fail"]["failure_reason"]



# ==============================================================================
# 7. Coordinator Authority & Truthful Completion Reporting
# ==============================================================================

def test_adversarial_coordinator_never_reports_complete_on_partial_failure():
    """Adversarial qualification: In mixed success/failure scenarios, coordinator reports TASKS_FAILED."""
    tasks = [
        {"task_id": "task_good_1", "name": "Good 1", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [10, 20]}},
        {"task_id": "task_bad", "name": "Bad Math", "status": "PENDING", "requirements": {"operation": "cosine_similarity", "vec_a": [0, 0], "vec_b": [1, 1]}},
        {"task_id": "task_good_2", "name": "Good 2", "status": "PENDING", "requirements": {"operation": "delta", "start": 5, "end": 5}},  # 0.0
    ]

    kernel = SimulationKernel(seed=777)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=10.0)
    env.attach_to_kernel(kernel)

    coord = CoordinatorAgent("coordinator", ["worker_1", "worker_2"])
    kernel.register_agent(coord)
    kernel.register_agent(WorkerAgent("worker_1"))
    kernel.register_agent(WorkerAgent("worker_2"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=30)

    # Must terminate with failures
    assert "TASKS_TERMINATED_WITH_FAILURES" in res.termination_reason
    assert "ALL_TASKS_COMPLETED" not in res.termination_reason

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    assert task_map["task_good_1"]["status"] == "COMPLETED"
    assert task_map["task_good_1"]["result_value"] == 30

    assert task_map["task_good_2"]["status"] == "COMPLETED"
    assert task_map["task_good_2"]["result_value"] == 0

    assert task_map["task_bad"]["status"] == "FAILED"
    assert "zero-norm" in task_map["task_bad"]["failure_reason"]

    # Post-run observation by Coordinator must state TASKS_FAILED
    final_obs = coord.observe(env.state.to_dict(), [], res.total_ticks + 1)
    final_act = coord.decide(final_obs, res.total_ticks + 1)
    assert final_act.parameters.get("status") == "TASKS_FAILED"
    assert final_act.parameters.get("failed_count") == 1
    assert "task_bad" in final_act.parameters.get("failed_tasks")


# ==============================================================================
# 8. Multi-Worker Concurrency, Preemption, Checkpoint Restore & Replay
# ==============================================================================

def test_adversarial_multiworker_checkpoint_and_replay_determinism():
    """Adversarial qualification: Complex heterogeneous tasks maintain bit-for-bit replay and snapshot restoration."""
    tasks = [
        {"task_id": "m_zero_cos", "status": "PENDING", "requirements": {"operation": "cosine_similarity", "vec_a": [1, 0, 0], "vec_b": [0, 1, 0]}},
        {"task_id": "m_neg_delta", "status": "PENDING", "requirements": {"operation": "delta", "start": 500, "end": 100}},
        {"task_id": "m_large_sum", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [50_000, 75_000]}},
        {"task_id": "m_zero_anom", "status": "PENDING", "requirements": {"operation": "anomaly_count", "inputs": [10.0, 10.0, 10.0], "threshold": 2.0}},
        {"task_id": "m_legit_42", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [21, 21]}},
    ]

    # Baseline run
    k_base = SimulationKernel(seed=4321)
    env_base = CooperativeTaskEnvironment(tasks=tasks, initial_energy=300.0, energy_cost_per_task=10.0)
    env_base.attach_to_kernel(k_base)
    k_base.register_agent(CoordinatorAgent("coordinator", ["w1", "w2", "w3"]))
    k_base.register_agent(WorkerAgent("w1"))
    k_base.register_agent(WorkerAgent("w2"))
    k_base.register_agent(WorkerAgent("w3"))
    k_base.register_agent(CriticAgent("critic"))

    res_base = k_base.run(max_ticks=35)
    assert res_base.is_completed is True
    assert "ALL_TASKS_COMPLETED" in res_base.termination_reason

    # Causal Replay
    replayer = ReplayEngine(k_base.logger.to_list())
    valid_chain, chain_err = replayer.verify_integrity()
    assert valid_chain is True, f"Causal integrity broken: {chain_err}"

    # Checkpoint restore halfway through
    k_res = SimulationKernel(seed=4321)
    env_res = CooperativeTaskEnvironment(tasks=tasks, initial_energy=300.0, energy_cost_per_task=10.0)
    env_res.attach_to_kernel(k_res)
    k_res.register_agent(CoordinatorAgent("coordinator", ["w1", "w2", "w3"]))
    k_res.register_agent(WorkerAgent("w1"))
    k_res.register_agent(WorkerAgent("w2"))
    k_res.register_agent(WorkerAgent("w3"))
    k_res.register_agent(CriticAgent("critic"))

    for _ in range(4):
        k_res.step()
    snap = k_res.snapshot()

    # Restore in new kernel
    k_res2 = SimulationKernel(seed=4321)
    env_res2 = CooperativeTaskEnvironment(tasks=tasks, initial_energy=300.0, energy_cost_per_task=10.0)
    env_res2.attach_to_kernel(k_res2)
    k_res2.register_agent(CoordinatorAgent("coordinator", ["w1", "w2", "w3"]))
    k_res2.register_agent(WorkerAgent("w1"))
    k_res2.register_agent(WorkerAgent("w2"))
    k_res2.register_agent(WorkerAgent("w3"))
    k_res2.register_agent(CriticAgent("critic"))
    k_res2.restore(snap)

    res_restored = k_res2.run(max_ticks=35)
    assert res_restored.terminal_state_hash == res_base.terminal_state_hash
    assert res_restored.total_ticks == res_base.total_ticks


# ==============================================================================
# 9. Critic Rejection of Corrupt, Malformed, and Unauthoritative Submissions
# ==============================================================================

def test_adversarial_critic_rejects_corrupt_and_malformed_submissions():
    """Adversarial qualification: Critic rejects NaN, Inf, boolean, None, string, and corrupt flags."""
    critic = CriticAgent("critic")
    state = {
        "tasks": [
            {"task_id": "t_math", "requirements": {"operation": "sum", "inputs": [10.0, 20.0]}}
        ]
    }
    critic.observe(state, [], 0)

    invalid_submissions = [
        ({"is_corrupt": True, "result_value": 30.0}, "corrupt"),
        ({"result_value": None}, "Missing result value"),
        ({"result_value": True}, "boolean"),
        ({"result_value": False}, "boolean"),
        ({"result_value": float("nan")}, "NaN or Inf"),
        ({"result_value": float("inf")}, "NaN or Inf"),
        ({"result_value": float("-inf")}, "NaN or Inf"),
        ({"result_value": "thirty"}, "expected numeric scalar"),
        ({"result_value": 42}, "does not match authoritative oracle"),
    ]

    for idx, (sub_data, expected_err_sub) in enumerate(invalid_submissions):
        msg = type("Msg", (), {
            "sender_id": "worker_1",
            "content": {
                "type": "SUBMIT_FOR_REVIEW",
                "task_id": "t_math",
                "submission": dict(sub_data, task_id="t_math")
            },
            "sent_tick": idx + 1
        })()
        obs = critic.observe(state, [msg], idx + 1)
        act = critic.decide(obs, idx + 1)
        assert act.action_type == "SEND_MESSAGE"
        content = act.parameters["content"]
        assert content["verdict"] == "REJECTED"
        assert expected_err_sub.lower() in content["feedback"].lower(), f"Sub {sub_data}: expected {expected_err_sub} in {content['feedback']}"
        assert "suggested_value" not in content, "Critic must NEVER suggest arbitrary fallback values"


# ==============================================================================
# 10. Upstream Dependency Propagation with Zero and Negative Intermediate Values
# ==============================================================================

def test_adversarial_upstream_dependency_propagation():
    """Adversarial qualification: Zero and negative intermediate values propagate through upstream results."""
    # Simulation where worker evaluates functional tasks with upstream dependencies
    upstream_map = {
        "step_1_zero": 0.0,
        "step_2_neg": -50.0,
        "step_3_pos": 150.0
    }

    downstream_sum_task = {
        "task_id": "step_4_downstream_sum",
        "requirements": {
            "operation": "sum",
            "depends_on": ["step_1_zero", "step_2_neg", "step_3_pos"],
            "upstream_results": upstream_map
        }
    }

    res_sum, meta_sum = evaluate_functional_task(downstream_sum_task)
    assert res_sum == 100, f"Expected 0.0 + (-50.0) + 150.0 = 100, got {res_sum}"

    downstream_reduce_prod = {
        "task_id": "step_5_downstream_prod",
        "requirements": {
            "operation": "pipeline_reduce",
            "reduce_op": "product",
            "depends_on": ["step_1_zero", "step_2_neg", "step_3_pos"],
            "upstream_results": upstream_map
        }
    }
    res_prod, _ = evaluate_functional_task(downstream_reduce_prod)
    assert res_prod == 0.0, f"Expected 0.0 * (-50.0) * 150.0 = 0.0, got {res_prod}"


# ==============================================================================
# 11. Fault Injection Resiliency with Deterministic Replay
# ==============================================================================

def test_adversarial_fault_injection_message_delays_resilience():
    """Adversarial qualification: Workflow with message delays reaches correct mathematical outcome and replays."""
    from simlab.faults import FaultInjector

    tasks = [
        {"task_id": "flt_cos", "name": "Ortho Cos", "status": "PENDING", "requirements": {"operation": "cosine_similarity", "vec_a": [1, 0], "vec_b": [0, 1]}},
        {"task_id": "flt_delta", "name": "Neg Delta", "status": "PENDING", "requirements": {"operation": "delta", "start": 80, "end": 20}},
        {"task_id": "flt_sum", "name": "Zero Sum", "status": "PENDING", "requirements": {"operation": "sum", "inputs": [25, -25]}}
    ]

    kernel = SimulationKernel(seed=555)
    fault = FaultInjector(seed=555, extra_delay_ticks=1)
    fault.attach_to_kernel(kernel)

    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=5.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", ["w1"]))
    kernel.register_agent(WorkerAgent("w1"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=40)
    assert res.is_completed is True
    assert "ALL_TASKS_COMPLETED" in res.termination_reason

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    assert task_map["flt_cos"]["result_value"] == 0.0
    assert task_map["flt_delta"]["result_value"] == -60
    assert task_map["flt_sum"]["result_value"] == 0

    # Causal Replay verification under fault injection
    replayer = ReplayEngine(kernel.logger.to_list())
    valid_chain, chain_err = replayer.verify_integrity()
    assert valid_chain is True, f"Causal integrity failed: {chain_err}"

