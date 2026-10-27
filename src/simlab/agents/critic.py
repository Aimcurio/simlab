"""Critic / Independent Reviewer Agent Implementation."""

import copy
import math
from typing import Any, Dict, List, Optional
import numpy as np

from simlab.agents.base import AgentAction, BaseAgent
from simlab.agents.models import DeterministicRuleBackend, ModelBackend, evaluate_functional_task


class CriticAgent(BaseAgent):
    """
    Independent reviewer agent that enforces double-blind quality and correctness:
    - Receives task submissions from workers
    - Validates deliverables against objective specifications and independent oracles
    - Rejects invalid deliverables with constructive feedback (without fabricated values)
    - Directly commits verified deliverables to environment state upon approval
    """

    def __init__(
        self,
        agent_id: str = "critic",
        coordinator_id: str = "coordinator",
        strict_mode: bool = True,
        backend: Optional[ModelBackend] = None,
        max_working_memory: int = 25
    ):
        super().__init__(
            agent_id=agent_id,
            role="Critic / Reviewer",
            capabilities=["independent_review", "contract_validation", "invariant_auditing"],
            objectives=["Prevent defective or unvalidated worker submissions from contaminating environment state."],
            max_working_memory=max_working_memory
        )
        self.coordinator_id = coordinator_id
        self.strict_mode = strict_mode
        self.backend = backend or DeterministicRuleBackend()
        self._reviews_performed: int = 0
        self._approvals_count: int = 0
        self._rejections_count: int = 0
        self._submission_queue: List[Dict[str, Any]] = []
        self._task_contracts: Dict[str, Dict[str, Any]] = {}

    def observe(self, state: Dict[str, Any], incoming_messages: List[Any], current_tick: int) -> Dict[str, Any]:
        """Collect all submissions awaiting verification and track task requirements."""
        for t in state.get("tasks", []):
            tid = t.get("task_id")
            if tid:
                self._task_contracts[tid] = copy.deepcopy(t)

        for msg in incoming_messages:
            content = msg.content or {}
            if content.get("type") == "SUBMIT_FOR_REVIEW":
                sub_item = {
                    "sender": msg.sender_id,
                    "task_id": content.get("task_id"),
                    "submission": content.get("submission", {}),
                    "sent_tick": msg.sent_tick
                }
                if not any(s.get("task_id") == sub_item["task_id"] and s.get("sender") == sub_item["sender"] for s in self._submission_queue):
                    self._submission_queue.append(sub_item)

        return {
            "pending_submissions": list(self._submission_queue),
            "environment_state_hash": state.get("state_hash", ""),
            "review_criteria": {
                "mode": "contract_grounded_oracle_verification",
                "allow_legitimate_zero": True,
                "allow_negative_values": True,
                "allow_large_magnitudes": True,
                "disallow_fabricated_fallbacks": True
            }
        }

    def decide(self, observation: Dict[str, Any], current_tick: int) -> AgentAction:
        """Evaluate pending submission against mathematical contract and emit APPROVE or REJECT."""
        if not self._submission_queue:
            return AgentAction(
                action_type="STANDBY",
                rationale="No deliverables pending review. Monitoring state."
            )

        # Inspect the first pending deliverable in FIFO queue
        sub = self._submission_queue.pop(0)
        self._reviews_performed += 1
        worker_id = sub["sender"]
        task_id = sub["task_id"]
        data = sub.get("submission", {})

        result_val = data.get("result_value")
        is_corrupt = data.get("is_corrupt", False)

        is_valid = True
        unrecoverable = False
        rejection_reason = ""

        # 1. Representation validity checks
        if is_corrupt:
            is_valid = False
            rejection_reason = "Deliverable marked corrupt by integrity check."
        elif result_val is None:
            is_valid = False
            rejection_reason = "Missing result value in worker submission."
        elif isinstance(result_val, bool):
            is_valid = False
            rejection_reason = f"Invalid numeric representation: boolean {result_val} is not accepted as a number."
        elif not isinstance(result_val, (int, float, np.number)):
            is_valid = False
            rejection_reason = f"Invalid result type: expected numeric scalar, got {type(result_val).__name__}."
        elif not math.isfinite(float(result_val)):
            is_valid = False
            rejection_reason = f"Non-finite numeric result: {result_val} (NaN or Inf)."

        # 2. Check task contract
        task_contract = self._task_contracts.get(task_id, {})
        req = task_contract.get("requirements", {})
        op = req.get("operation") or task_contract.get("operation")

        if is_valid and op:
            # Domain bounds check on valid numeric representation
            f_res = float(result_val)
            if op == "cosine_similarity":
                if f_res < -1.0 - 1e-6 or f_res > 1.0 + 1e-6:
                    is_valid = False
                    rejection_reason = f"Result {result_val} violates cosine similarity domain bounds [-1.0, 1.0]."
            elif op in ("anomaly_count", "record_reconcile"):
                if f_res < 0:
                    is_valid = False
                    rejection_reason = f"Result {result_val} violates non-negativity constraint for {op}."
                elif not f_res.is_integer():
                    is_valid = False
                    rejection_reason = f"Result {result_val} for {op} must be an integer count."
            elif op in ("variance", "std", "range"):
                if f_res < -1e-6:
                    is_valid = False
                    rejection_reason = f"Result {result_val} violates non-negativity constraint for {op}."

        # 3. Independent oracle verification
        if is_valid:
            if op:
                try:
                    oracle_val, _ = evaluate_functional_task(task_contract)
                    if isinstance(oracle_val, int) and isinstance(result_val, int):
                        matches = (result_val == oracle_val)
                    else:
                        matches = math.isclose(float(result_val), float(oracle_val), rel_tol=1e-5, abs_tol=1e-6)

                    if not matches:
                        is_valid = False
                        rejection_reason = (
                            f"Computational verification failed: result {result_val} "
                            f"does not match authoritative oracle {oracle_val}."
                        )
                except (ValueError, TypeError, ZeroDivisionError) as err:
                    is_valid = False
                    unrecoverable = True
                    rejection_reason = f"Task contract mathematical failure: {err}"
            else:
                expected_val = req.get("expected_value", task_contract.get("default_value", 42))
                if isinstance(expected_val, (int, float)):
                    if isinstance(expected_val, int) and isinstance(result_val, int):
                        matches = (result_val == expected_val)
                    else:
                        matches = math.isclose(float(result_val), float(expected_val), rel_tol=1e-5, abs_tol=1e-6)
                    if not matches:
                        is_valid = False
                        rejection_reason = f"Result {result_val} does not match expected legacy value {expected_val}."

        if is_valid:
            self._approvals_count += 1
            return AgentAction(
                action_type="APPROVE_TASK",
                target=task_id,
                parameters={
                    "task_id": task_id,
                    "worker_id": worker_id,
                    "critic_id": self.agent_id,
                    "verdict": "APPROVED",
                    "value": result_val
                },
                rationale=f"Deliverable for {task_id} passed independent oracle verification (value={result_val})."
            )
        else:
            self._rejections_count += 1
            return AgentAction(
                action_type="SEND_MESSAGE",
                target=worker_id,
                parameters={
                    "recipient_id": worker_id,
                    "content": {
                        "type": "REVIEW_FEEDBACK",
                        "task_id": task_id,
                        "verdict": "REJECTED",
                        "feedback": rejection_reason,
                        "unrecoverable": unrecoverable
                    }
                },
                rationale=f"Rejecting submission for {task_id}: {rejection_reason}."
            )

    def snapshot(self) -> Dict[str, Any]:
        """Create serializable critic snapshot."""
        snap = super().snapshot()
        snap.update({
            "reviews_performed": self._reviews_performed,
            "approvals_count": self._approvals_count,
            "rejections_count": self._rejections_count,
            "strict_mode": self.strict_mode,
            "coordinator_id": self.coordinator_id,
            "submission_queue": [dict(s) for s in self._submission_queue],
            "task_contracts": copy.deepcopy(self._task_contracts),
        })
        return snap

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore critic state from snapshot."""
        super().restore(data)
        self._reviews_performed = data.get("reviews_performed", 0)
        self._approvals_count = data.get("approvals_count", 0)
        self._rejections_count = data.get("rejections_count", 0)
        self.strict_mode = data.get("strict_mode", self.strict_mode)
        self.coordinator_id = data.get("coordinator_id", self.coordinator_id)
        self._submission_queue = [dict(s) for s in data.get("submission_queue", [])]
        self._task_contracts = copy.deepcopy(data.get("task_contracts", {}))

