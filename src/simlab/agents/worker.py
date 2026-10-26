"""Worker / Specialist Agent Implementation."""

from typing import Any, Dict, List, Optional
from simlab.agents.base import AgentAction, BaseAgent
from simlab.agents.models import DeterministicRuleBackend, ModelBackend, evaluate_functional_task


class WorkerAgent(BaseAgent):
    """
    Executes domain tasks:
    - Receives task assignments via message bus
    - Gathers required information and applies cognitive policy
    - Executes environmental state transitions
    - Submits work output to Critic for independent verification
    """

    def __init__(
        self,
        agent_id: str,
        specialization: str = "general_computation",
        critic_id: str = "critic",
        coordinator_id: str = "coordinator",
        backend: Optional[ModelBackend] = None,
        max_working_memory: int = 20
    ):
        super().__init__(
            agent_id=agent_id,
            role=f"Worker ({specialization})",
            capabilities=["task_execution", specialization, "self_reporting"],
            objectives=["Execute assigned tasks correctly while observing resource bounds."],
            max_working_memory=max_working_memory
        )
        self.specialization = specialization
        self.critic_id = critic_id
        self.coordinator_id = coordinator_id
        self.backend = backend or DeterministicRuleBackend()
        self.current_task: Optional[Dict[str, Any]] = None
        self._task_queue: List[Dict[str, Any]] = []
        self._completed_count: int = 0

    def observe(self, state: Dict[str, Any], incoming_messages: List[Any], current_tick: int) -> Dict[str, Any]:
        """Inspect mailbox for assignments, criticisms, or updates."""
        criticisms = []

        for msg in incoming_messages:
            content = msg.content or {}
            msg_type = content.get("type")
            if msg_type in ("ASSIGN_TASK", "REASSIGN_TASK"):
                task = content.get("task") or {"task_id": content.get("task_id")}
                self._task_queue.append(task)
            elif msg_type == "REVIEW_FEEDBACK":
                criticisms.append(content)

        return {
            "criticisms": criticisms,
            "resources": {
                "energy": state.get("energy", 100),
                "bandwidth": state.get("bandwidth", 100)
            },
            "environment_info": state.get("task_data", {}),
            "tasks": state.get("tasks", [])
        }

    def decide(self, observation: Dict[str, Any], current_tick: int) -> AgentAction:
        """Process criticisms, start assigned tasks, or execute current task."""
        # 1. Handle critic feedback first
        criticisms = observation.get("criticisms", [])
        for crit in criticisms:
            if crit.get("verdict") == "REJECTED":
                # Critic rejected our previous work, retry with corrected parameters
                task_id = crit.get("task_id")
                rework_val = crit.get("suggested_value", 42)

                orig_task = None
                for env_t in observation.get("tasks", []):
                    if env_t.get("task_id") == task_id:
                        orig_task = dict(env_t)
                        break
                if not orig_task:
                    orig_task = {"task_id": task_id}

                if orig_task.get("requirements"):
                    calc_val, _ = evaluate_functional_task(orig_task)
                    if isinstance(calc_val, (int, float)) and 0 < calc_val <= 500:
                        rework_val = calc_val

                orig_task["_executed"] = True
                orig_task["_result_value"] = rework_val
                orig_task["_reworked"] = True
                self.current_task = orig_task

                return AgentAction(
                    action_type="EXECUTE_TASK",
                    target=task_id,
                    parameters={
                        "task_id": task_id,
                        "worker_id": self.agent_id,
                        "correction_applied": True,
                        "retry_count": crit.get("retry_count", 0) + 1,
                        "value": rework_val
                    },
                    rationale=f"Reworking task {task_id} after Critic rejection: {crit.get('feedback')}."
                )

        # 2. Pick up new task assignment if idle
        if not self.current_task and self._task_queue:
            self.current_task = self._task_queue.pop(0)
            task_id = self.current_task.get("task_id")
            # If task details were sparse, enrich from environment tasks
            if not self.current_task.get("requirements") and "tasks" in observation:
                for env_t in observation["tasks"]:
                    if env_t.get("task_id") == task_id:
                        self.current_task.update({
                            k: v for k, v in env_t.items()
                            if k not in self.current_task or not self.current_task[k]
                        })
                        break

            return AgentAction(
                action_type="ACCEPT_TASK",
                target=task_id,
                parameters={"task_id": task_id, "worker_id": self.agent_id},
                rationale=f"Accepting assignment for task {task_id}."
            )

        # 3. If currently holding a task, execute computation then notify Critic
        if self.current_task:
            task = self.current_task
            task_id = task.get("task_id")
            if not task.get("_executed"):
                task["_executed"] = True
                # Enrich from env if needed
                if not task.get("requirements") and "tasks" in observation:
                    for env_t in observation["tasks"]:
                        if env_t.get("task_id") == task_id:
                            task.update({
                                k: v for k, v in env_t.items()
                                if k not in task or not task[k]
                            })
                            break

                result_val, meta = evaluate_functional_task(task)
                task["_result_value"] = result_val
                task["_meta"] = meta
                return AgentAction(
                    action_type="EXECUTE_TASK",
                    target=task_id,
                    parameters={
                        "task_id": task_id,
                        "worker_id": self.agent_id,
                        "value": result_val,
                        "metadata": meta
                    },
                    rationale=f"Executing computation for task {task_id}."
                )
            else:
                self.current_task = None
                self._completed_count += 1
                result_val = task.get("_result_value", 42)
                computed_result = {
                    "task_id": task_id,
                    "worker_id": self.agent_id,
                    "result_value": result_val,
                    "complexity_weight": task.get("complexity_weight", 1.0),
                    "metadata": task.get("_meta", {})
                }
                return AgentAction(
                    action_type="SUBMIT_FOR_REVIEW",
                    target=self.critic_id,
                    parameters={
                        "recipient_id": self.critic_id,
                        "worker_id": self.agent_id,
                        "content": {
                            "type": "SUBMIT_FOR_REVIEW",
                            "task_id": task_id,
                            "submission": computed_result,
                            "worker_id": self.agent_id
                        }
                    },
                    rationale=f"Completed computation for task {task_id}; submitting to {self.critic_id} for review."
                )

        # Idle standby
        return AgentAction(
            action_type="STANDBY",
            parameters={"worker_id": self.agent_id},
            rationale="No active task assignment. Standing by."
        )

    def snapshot(self) -> Dict[str, Any]:
        """Create serializable worker snapshot."""
        snap = super().snapshot()
        snap.update({
            "current_task": dict(self.current_task) if self.current_task else None,
            "task_queue": [dict(t) for t in self._task_queue],
            "completed_count": self._completed_count,
            "specialization": self.specialization,
            "critic_id": self.critic_id,
            "coordinator_id": self.coordinator_id,
        })
        return snap

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore worker state from snapshot."""
        super().restore(data)
        self.current_task = dict(data["current_task"]) if data.get("current_task") else None
        self._task_queue = [dict(t) for t in data.get("task_queue", [])]
        self._completed_count = data.get("completed_count", 0)
        self.specialization = data.get("specialization", self.specialization)
        self.critic_id = data.get("critic_id", self.critic_id)
        self.coordinator_id = data.get("coordinator_id", self.coordinator_id)
