"""Cooperative Problem-Solving Environment with Shared Resource Constraints."""

import copy
from typing import Any, Dict, List, Optional
from simlab.agents.base import AgentAction
from simlab.core.state import EnvironmentState


class CooperativeTaskEnvironment:
    """
    Simulates a collaborative mission under shared resource limits:
    - Maintains backlog of tasks requiring information gathering and compute
    - Tracks shared resource depletion (energy, bandwidth, budget)
    - Manages task lifecycle (PENDING -> IN_PROGRESS -> EXECUTED -> COMPLETED / FAILED)
    """

    def __init__(
        self,
        tasks: Optional[List[Dict[str, Any]]] = None,
        initial_energy: float = 100.0,
        initial_bandwidth: float = 100.0,
        initial_budget: float = 50.0,
        energy_cost_per_task: float = 10.0,
        bandwidth_cost_per_message: float = 2.0
    ):
        self.initial_energy = initial_energy
        self.initial_bandwidth = initial_bandwidth
        self.initial_budget = initial_budget
        self.energy_cost_per_task = energy_cost_per_task
        self.bandwidth_cost_per_message = bandwidth_cost_per_message
        self.kernel: Optional[Any] = None

        raw_tasks = copy.deepcopy(list(tasks or [
            {"task_id": "task_01", "name": "Telemetry Ingestion", "difficulty": "LOW", "status": "PENDING", "complexity_weight": 1.0},
            {"task_id": "task_02", "name": "Anomaly Detection", "difficulty": "MEDIUM", "status": "PENDING", "complexity_weight": 1.5},
            {"task_id": "task_03", "name": "Decision Synthesis", "difficulty": "HIGH", "status": "PENDING", "complexity_weight": 2.0},
        ]))

        self.state = EnvironmentState({
            "tasks": raw_tasks,
            "energy": initial_energy,
            "bandwidth": initial_bandwidth,
            "budget": initial_budget,
            "completed_count": 0,
            "failed_count": 0,
            "total_tasks": len(raw_tasks),
            "status": "INITIALIZED"
        })

    def attach_to_kernel(self, kernel: Any) -> None:
        """Bind environment state and action handlers to a simulation kernel."""
        self.kernel = kernel
        kernel.state = self.state

        kernel.register_action_handler("ACCEPT_TASK", self._handle_accept_task)
        kernel.register_action_handler("EXECUTE_TASK", self._handle_execute_task)
        kernel.register_action_handler("SUBMIT_FOR_REVIEW", self._handle_submit_review)
        kernel.register_action_handler("APPROVE_TASK", self._handle_approve_task)

        kernel.add_termination_predicate(self._check_termination)

    def _handle_accept_task(self, action: AgentAction, tick: int) -> Dict[str, Any]:
        task_id = action.parameters.get("task_id", action.target)
        worker_id = action.parameters.get("worker_id", "unknown")
        tasks = self.state.get("tasks", [])

        for t in tasks:
            if t["task_id"] == task_id and t["status"] in ("PENDING", "FAILED"):
                was_failed = (t["status"] == "FAILED")
                t["status"] = "IN_PROGRESS"
                t["assigned_worker"] = worker_id
                t["started_tick"] = tick
                if was_failed:
                    failed = max(0, self.state.get("failed_count", 0) - 1)
                    self.state.set("failed_count", failed)
                self.state.set("tasks", tasks)
                return {"task_id": task_id, "status": "IN_PROGRESS"}

        return {"task_id": task_id, "status": "NOT_FOUND_OR_NOT_PENDING"}

    def _handle_execute_task(self, action: AgentAction, tick: int) -> Dict[str, Any]:
        task_id = action.parameters.get("task_id", action.target)
        worker_id = action.parameters.get("worker_id", "unknown")
        tasks = self.state.get("tasks", [])

        current_energy = self.state.get("energy", 0.0)
        if current_energy < self.energy_cost_per_task:
            for t in tasks:
                if t["task_id"] == task_id:
                    t["status"] = "FAILED"
                    t["failure_reason"] = "ENERGY_DEPLETED"
                    self.state.set("tasks", tasks)
                    failed = self.state.get("failed_count", 0) + 1
                    self.state.set("failed_count", failed)
                    break
            return {"error": "ENERGY_DEPLETED", "status": "FAILED"}

        for t in tasks:
            if t["task_id"] == task_id:
                if t.get("status") == "COMPLETED":
                    return {"task_id": task_id, "status": "ALREADY_COMPLETED"}
                if t.get("status") == "EXECUTED" and not action.parameters.get("correction_applied", False):
                    return {"task_id": task_id, "status": "ALREADY_EXECUTED"}
                if t.get("assigned_worker") and t.get("assigned_worker") != worker_id:
                    return {"task_id": task_id, "status": "REJECTED_UNAUTHORIZED_WORKER"}
                self.state.set("energy", max(0.0, current_energy - self.energy_cost_per_task))
                t["status"] = "EXECUTED"
                val = action.parameters.get("value")
                if val is not None:
                    t["result_value"] = val
                elif "result_value" not in t:
                    t["result_value"] = 42
                t["executed_by"] = worker_id
                t["executed_tick"] = tick
                if "metadata" in action.parameters:
                    t["metadata"] = action.parameters["metadata"]
                self.state.set("tasks", tasks)
                return {"task_id": task_id, "status": "EXECUTED"}

        return {"task_id": task_id, "status": "NOT_FOUND"}

    def _handle_submit_review(self, action: AgentAction, tick: int) -> Dict[str, Any]:
        content = action.parameters.get("content", {})
        task_id = content.get("task_id")
        recipient = action.parameters.get("recipient_id", action.target)
        worker_id = action.parameters.get("worker_id", "worker")

        if self.kernel and recipient:
            self.kernel.message_bus.send(
                sender_id=worker_id,
                recipient_id=recipient,
                content=content,
                current_tick=tick
            )

        return {"action": "FORWARDED_TO_CRITIC", "target": recipient, "task_id": task_id}

    def _handle_approve_task(self, action: AgentAction, tick: int) -> Dict[str, Any]:
        task_id = action.parameters.get("task_id", action.target)
        tasks = self.state.get("tasks", [])

        for t in tasks:
            if t["task_id"] == task_id:
                if t.get("status") == "COMPLETED":
                    return {"task_id": task_id, "status": "ALREADY_COMPLETED"}
                if t.get("status") != "EXECUTED":
                    return {"task_id": task_id, "status": f"REJECTED_UNEXECUTED_TASK:{t.get('status')}"}
                t["status"] = "COMPLETED"
                t["approved_by"] = action.parameters.get("critic_id", "critic")
                t["approved_tick"] = tick
                if "value" in action.parameters:
                    t["result_value"] = action.parameters["value"]
                completed = self.state.get("completed_count", 0) + 1
                self.state.set("completed_count", completed)
                self.state.set("tasks", tasks)

                # Notify coordinator
                if self.kernel:
                    self.kernel.message_bus.send(
                        sender_id=action.parameters.get("critic_id", "critic"),
                        recipient_id="coordinator",
                        content={"type": "TASK_COMPLETED", "task_id": task_id},
                        current_tick=tick
                    )

                return {"task_id": task_id, "status": "COMPLETED"}

        return {"task_id": task_id, "status": "NOT_FOUND"}

    def _check_termination(self, kernel: Any) -> Optional[str]:
        completed = self.state.get("completed_count", 0)
        total = self.state.get("total_tasks", 0)

        if total > 0 and completed >= total:
            return f"ALL_TASKS_COMPLETED ({completed}/{total})"

        energy = self.state.get("energy", 0.0)
        if energy <= 0.0:
            return "RESOURCE_DEPLETED (energy=0)"

        return None
