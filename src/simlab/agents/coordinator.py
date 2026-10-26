"""Coordinator / Orchestrator Agent Implementation."""

import copy
from typing import Any, Dict, List, Optional
from simlab.agents.base import AgentAction, BaseAgent
from simlab.agents.models import DeterministicRuleBackend, ModelBackend


class CoordinatorAgent(BaseAgent):
    """
    Coordinates multi-agent workflows:
    - Analyzes task backlog in environment state
    - Assigns tasks to appropriate workers based on capabilities
    - Monitors worker progress and handles failures
    """

    def __init__(
        self,
        agent_id: str = "coordinator",
        managed_workers: Optional[List[str]] = None,
        backend: Optional[ModelBackend] = None,
        max_working_memory: int = 30
    ):
        super().__init__(
            agent_id=agent_id,
            role="Coordinator",
            capabilities=["task_assignment", "progress_monitoring", "resource_governance"],
            objectives=["Complete all scenario tasks with minimal coordination latency and zero unhandled failures."],
            max_working_memory=max_working_memory
        )
        self.managed_workers = list(managed_workers or ["worker_1", "worker_2"])
        self.backend = backend or DeterministicRuleBackend()
        self._assigned_tasks: Dict[str, str] = {}  # task_id -> worker_id

    def observe(self, state: Dict[str, Any], incoming_messages: List[Any], current_tick: int) -> Dict[str, Any]:
        """Filter environment state to identify pending tasks and worker reports."""
        tasks = state.get("tasks", [])
        pending_tasks = [t for t in tasks if t.get("status") == "PENDING"]
        in_progress_tasks = [t for t in tasks if t.get("status") == "IN_PROGRESS"]
        completed_tasks = [t for t in tasks if t.get("status") == "COMPLETED"]

        # Parse worker messages
        worker_reports = []
        for msg in incoming_messages:
            worker_reports.append({
                "sender": msg.sender_id,
                "content": msg.content,
                "sent_tick": msg.sent_tick
            })

        return {
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "worker_reports": worker_reports,
            "available_workers": list(self.managed_workers),
            "shared_budget": state.get("budget", 100),
        }

    def decide(self, observation: Dict[str, Any], current_tick: int) -> AgentAction:
        """Assign pending tasks or issue status report."""
        pending = observation["pending_tasks"]
        workers = observation["available_workers"]
        reports = observation["worker_reports"]

        # Check for completed or failed reports from workers
        for rep in reports:
            content = rep.get("content", {})
            if content.get("status") == "FAILED":
                failed_task_id = content.get("task_id")
                # Reassign failed task to another worker
                alt_worker = [w for w in workers if w != rep["sender"]]
                target_w = alt_worker[0] if alt_worker else rep["sender"]
                return AgentAction(
                    action_type="SEND_MESSAGE",
                    target=target_w,
                    parameters={
                        "recipient_id": target_w,
                        "content": {
                            "type": "REASSIGN_TASK",
                            "task_id": failed_task_id,
                            "original_error": content.get("error")
                        }
                    },
                    rationale=f"Reassigning failed task {failed_task_id} to {target_w} after failure in {rep['sender']}."
                )

        # Assign pending tasks that have not yet been assigned
        unassigned_pending = [t for t in pending if t["task_id"] not in self._assigned_tasks]

        if unassigned_pending and workers:
            task_to_assign = copy.deepcopy(unassigned_pending[0])
            # Round-robin worker selection
            worker_idx = len(self._assigned_tasks) % len(workers)
            target_worker = workers[worker_idx]
            task_id = task_to_assign["task_id"]

            self._assigned_tasks[task_id] = target_worker
            return AgentAction(
                action_type="SEND_MESSAGE",
                target=target_worker,
                parameters={
                    "recipient_id": target_worker,
                    "content": {
                        "type": "ASSIGN_TASK",
                        "task": task_to_assign
                    }
                },
                rationale=f"Assigning task {task_id} to worker {target_worker}."
            )

        # If no pending tasks, check if everything is complete
        if not pending and not observation["in_progress_tasks"]:
            return AgentAction(
                action_type="STANDBY",
                parameters={"status": "ALL_TASKS_COMPLETE"},
                rationale="All tasks assigned and completed. Standing by."
            )

        return AgentAction(
            action_type="STANDBY",
            parameters={"status": "WAITING_FOR_WORKERS"},
            rationale="Awaiting progress reports from active workers."
        )

    def snapshot(self) -> Dict[str, Any]:
        """Create serializable coordinator snapshot."""
        snap = super().snapshot()
        snap.update({
            "assigned_tasks": dict(self._assigned_tasks),
            "managed_workers": list(self.managed_workers),
        })
        return snap

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore coordinator state from snapshot."""
        super().restore(data)
        self._assigned_tasks = dict(data.get("assigned_tasks", {}))
        self.managed_workers = list(data.get("managed_workers", self.managed_workers))
