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
        self._rework_queue: List[Dict[str, Any]] = []
        self._in_flight_tasks: Dict[str, Dict[str, Any]] = {}
        self._completed_count: int = 0

    def observe(self, state: Dict[str, Any], incoming_messages: List[Any], current_tick: int) -> Dict[str, Any]:
        """Inspect mailbox for assignments, criticisms, or updates."""
        criticisms = []

        for msg in incoming_messages:
            content = msg.content or {}
            msg_type = content.get("type")
            if msg_type in ("ASSIGN_TASK", "REASSIGN_TASK"):
                task = content.get("task") or {"task_id": content.get("task_id")}
                tid = task.get("task_id")
                # Deduplicate: only append if not already in queue, rework, or in-flight
                if tid and not any(t.get("task_id") == tid for t in self._task_queue):
                    if tid not in self._in_flight_tasks and (not self.current_task or self.current_task.get("task_id") != tid):
                        self._task_queue.append(task)
            elif msg_type == "REVIEW_FEEDBACK":
                criticisms.append(content)
                if content.get("verdict") == "REJECTED":
                    tid = content.get("task_id")
                    if tid and not any(r.get("task_id") == tid for r in self._rework_queue):
                        self._rework_queue.append(content)

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
        env_tasks = {t["task_id"]: t for t in observation.get("tasks", [])}

        # 0. Reconcile in-flight tasks and current_task against authoritative environment state
        for tid in list(self._in_flight_tasks.keys()):
            env_t = env_tasks.get(tid)
            if env_t:
                if env_t.get("status") in ("COMPLETED", "FAILED"):
                    del self._in_flight_tasks[tid]
                elif env_t.get("assigned_worker") and env_t.get("assigned_worker") != self.agent_id:
                    del self._in_flight_tasks[tid]

        if self.current_task:
            cid = self.current_task.get("task_id")
            env_c = env_tasks.get(cid)
            if env_c:
                if env_c.get("status") in ("COMPLETED", "FAILED"):
                    self.current_task = None
                elif env_c.get("assigned_worker") and env_c.get("assigned_worker") != self.agent_id:
                    self.current_task = None

        # Filter task queue to drop already completed, failed, or alien-owned tasks
        filtered_queue = []
        for t in self._task_queue:
            tid = t.get("task_id")
            env_t = env_tasks.get(tid)
            if env_t:
                if env_t.get("status") in ("COMPLETED", "FAILED"):
                    continue
                if env_t.get("status") in ("IN_PROGRESS", "EXECUTED") and env_t.get("assigned_worker") != self.agent_id:
                    continue
            filtered_queue.append(t)
        self._task_queue = filtered_queue

        # 1. Check for Preemption: If Critic rework is pending and current_task is a different in-flight task
        if self._rework_queue:
            next_rework_tid = self._rework_queue[0].get("task_id")
            if self.current_task and self.current_task.get("task_id") != next_rework_tid:
                # Suspend current in-flight task without losing its execution stage!
                cur_id = self.current_task.get("task_id")
                self._in_flight_tasks[cur_id] = self.current_task
                self.current_task = None

        # 2. Priority 1: Handle Critic Rework Queue
        if self._rework_queue or (self.current_task and self.current_task.get("_rework")):
            if not self.current_task:
                crit = self._rework_queue.pop(0)
                task_id = crit.get("task_id")
                unrecoverable = crit.get("unrecoverable", False)
                retry_count = crit.get("retry_count", 0) + 1
                feedback = crit.get("feedback", "")

                if unrecoverable or retry_count > 3:
                    self._in_flight_tasks.pop(task_id, None)
                    return AgentAction(
                        action_type="FAIL_TASK",
                        target=task_id,
                        parameters={
                            "task_id": task_id,
                            "worker_id": self.agent_id,
                            "reason": feedback or "MAX_RETRIES_EXCEEDED"
                        },
                        rationale=f"Task {task_id} failed: {feedback or 'Max retries exceeded'}."
                    )

                orig_task = None
                if task_id in env_tasks:
                    orig_task = dict(env_tasks[task_id])
                elif task_id in self._in_flight_tasks:
                    orig_task = dict(self._in_flight_tasks[task_id])
                else:
                    orig_task = {"task_id": task_id}

                try:
                    rework_val, rework_meta = evaluate_functional_task(orig_task)
                except (ValueError, TypeError, ZeroDivisionError) as err:
                    self._in_flight_tasks.pop(task_id, None)
                    return AgentAction(
                        action_type="FAIL_TASK",
                        target=task_id,
                        parameters={
                            "task_id": task_id,
                            "worker_id": self.agent_id,
                            "reason": str(err)
                        },
                        rationale=f"Task {task_id} recalculation failed: {err}."
                    )

                orig_task["_rework"] = True
                orig_task["_rework_val"] = rework_val
                orig_task["_meta"] = rework_meta
                orig_task["_retry_count"] = retry_count
                orig_task["_feedback"] = feedback
                orig_task["_executed"] = False
                orig_task["_submitted"] = False
                self.current_task = orig_task

            task_id = self.current_task.get("task_id")
            if not self.current_task.get("_executed"):
                self.current_task["_executed"] = True
                self.current_task["_result_value"] = self.current_task["_rework_val"]
                return AgentAction(
                    action_type="EXECUTE_TASK",
                    target=task_id,
                    parameters={
                        "task_id": task_id,
                        "worker_id": self.agent_id,
                        "correction_applied": True,
                        "retry_count": self.current_task.get("_retry_count", 1),
                        "value": self.current_task["_rework_val"],
                        "metadata": self.current_task.get("_meta", {})
                    },
                    rationale=f"Reworking task {task_id} after Critic rejection: {self.current_task.get('_feedback')}."
                )
            else:
                result_val = self.current_task.get("_result_value")
                if result_val is None:
                    result_val = self.current_task.get("_rework_val")
                computed_result = {
                    "task_id": task_id,
                    "worker_id": self.agent_id,
                    "result_value": result_val,
                    "complexity_weight": self.current_task.get("complexity_weight", 1.0),
                    "metadata": self.current_task.get("_meta", {})
                }
                self.current_task["_submitted"] = True
                self._in_flight_tasks[task_id] = self.current_task
                self.current_task = None
                self._completed_count += 1
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
                    rationale=f"Completed rework for task {task_id}; submitting to {self.critic_id} for review."
                )

        # 3. Priority 2: Resume In-Flight Suspended Tasks (already accepted, awaiting execution or submission)
        if not self.current_task:
            for tid, t in list(self._in_flight_tasks.items()):
                if not t.get("_submitted"):
                    self.current_task = t
                    break

        if self.current_task:
            task = self.current_task
            task_id = task.get("task_id")
            if not task.get("_executed"):
                task["_executed"] = True
                if not task.get("requirements") and task_id in env_tasks:
                    task.update({
                        k: v for k, v in env_tasks[task_id].items()
                        if k not in task or not task[k]
                    })
                try:
                    result_val, meta = evaluate_functional_task(task)
                except (ValueError, TypeError, ZeroDivisionError) as err:
                    self.current_task = None
                    return AgentAction(
                        action_type="FAIL_TASK",
                        target=task_id,
                        parameters={
                            "task_id": task_id,
                            "worker_id": self.agent_id,
                            "reason": str(err)
                        },
                        rationale=f"Execution failed for task {task_id}: {err}."
                    )
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
            elif not task.get("_submitted"):
                task["_submitted"] = True
                result_val = task.get("_result_value")
                computed_result = {
                    "task_id": task_id,
                    "worker_id": self.agent_id,
                    "result_value": result_val,
                    "complexity_weight": task.get("complexity_weight", 1.0),
                    "metadata": task.get("_meta", {})
                }
                self.current_task = None
                self._completed_count += 1
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

        # 4. Priority 3: Pick up new task assignment from queue if idle
        while self._task_queue:
            candidate = self._task_queue.pop(0)
            task_id = candidate.get("task_id")
            env_t = env_tasks.get(task_id)

            if env_t:
                if env_t.get("status") in ("COMPLETED", "FAILED"):
                    continue
                if env_t.get("status") in ("IN_PROGRESS", "EXECUTED") and env_t.get("assigned_worker") != self.agent_id:
                    continue
                candidate.update({
                    k: v for k, v in env_t.items()
                    if k not in candidate or not candidate[k]
                })

            candidate["_accepted"] = True
            candidate["_executed"] = False
            candidate["_submitted"] = False
            self.current_task = candidate
            self._in_flight_tasks[task_id] = candidate

            # If task was already marked IN_PROGRESS with this worker assigned, execute directly
            if env_t and env_t.get("status") == "IN_PROGRESS" and env_t.get("assigned_worker") == self.agent_id:
                candidate["_executed"] = True
                result_val, meta = evaluate_functional_task(candidate)
                candidate["_result_value"] = result_val
                candidate["_meta"] = meta
                return AgentAction(
                    action_type="EXECUTE_TASK",
                    target=task_id,
                    parameters={
                        "task_id": task_id,
                        "worker_id": self.agent_id,
                        "value": result_val,
                        "metadata": meta
                    },
                    rationale=f"Executing already-assigned in-progress task {task_id}."
                )

            return AgentAction(
                action_type="ACCEPT_TASK",
                target=task_id,
                parameters={"task_id": task_id, "worker_id": self.agent_id},
                rationale=f"Accepting assignment for task {task_id}."
            )

        # 5. Standby
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
            "rework_queue": [dict(t) for t in self._rework_queue],
            "in_flight_tasks": {k: dict(v) for k, v in self._in_flight_tasks.items()},
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
        self._rework_queue = [dict(t) for t in data.get("rework_queue", [])]
        self._in_flight_tasks = {k: dict(v) for k, v in data.get("in_flight_tasks", {}).items()}
        self._completed_count = data.get("completed_count", 0)
        self.specialization = data.get("specialization", self.specialization)
        self.critic_id = data.get("critic_id", self.critic_id)
        self.coordinator_id = data.get("coordinator_id", self.coordinator_id)
