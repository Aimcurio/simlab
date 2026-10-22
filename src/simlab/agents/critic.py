"""Critic / Independent Reviewer Agent Implementation."""

from typing import Any, Dict, List, Optional
from simlab.agents.base import AgentAction, BaseAgent
from simlab.agents.models import DeterministicRuleBackend, ModelBackend


class CriticAgent(BaseAgent):
    """
    Independent reviewer agent that enforces double-blind quality and correctness:
    - Receives task submissions from workers
    - Validates deliverables against objective specifications
    - Rejects invalid deliverables with constructive feedback
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

    def observe(self, state: Dict[str, Any], incoming_messages: List[Any], current_tick: int) -> Dict[str, Any]:
        """Collect all submissions awaiting verification."""
        submissions = []
        for msg in incoming_messages:
            content = msg.content or {}
            if content.get("type") == "SUBMIT_FOR_REVIEW":
                submissions.append({
                    "sender": msg.sender_id,
                    "task_id": content.get("task_id"),
                    "submission": content.get("submission", {}),
                    "sent_tick": msg.sent_tick
                })

        return {
            "pending_submissions": submissions,
            "environment_state_hash": state.get("state_hash", ""),
            "review_criteria": {
                "require_positive_value": True,
                "max_allowed_value": 500
            }
        }

    def decide(self, observation: Dict[str, Any], current_tick: int) -> AgentAction:
        """Evaluate pending submission and emit APPROVE or REJECT."""
        subs = observation.get("pending_submissions", [])
        if not subs:
            return AgentAction(
                action_type="STANDBY",
                rationale="No deliverables pending review. Monitoring state."
            )

        # Inspect the first pending deliverable
        sub = subs[0]
        self._reviews_performed += 1
        worker_id = sub["sender"]
        task_id = sub["task_id"]
        data = sub.get("submission", {})

        result_val = data.get("result_value", 0)

        # Verification Invariant: Result value must be positive and within reasonable bounds
        is_valid = (result_val > 0 and result_val <= 500)

        # Intentional adversarial check: if strict_mode is True and task is marked corrupt
        if data.get("is_corrupt", False):
            is_valid = False

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
                rationale=f"Deliverable for {task_id} passed independent verification (value={result_val})."
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
                        "feedback": f"Value {result_val} violated domain constraints. Must be in range (0, 500].",
                        "suggested_value": 42
                    }
                },
                rationale=f"Rejecting submission for {task_id} due to invalid output {result_val}."
            )
