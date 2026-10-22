"""Discrete-Event Simulation Kernel."""

import random
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from simlab.agents.base import AgentAction, BaseAgent
from simlab.core.bus import MessageBus
from simlab.core.clock import SimulationClock
from simlab.core.events import Event, EventPriority, EventQueue
from simlab.core.logging import CausalEventLogger
from simlab.core.state import EnvironmentState


@dataclass
class StepResult:
    """Summary of operations during one simulation tick."""
    tick: int
    events_processed: int
    messages_delivered: int
    actions_executed: List[Dict[str, Any]] = field(default_factory=list)
    state_hash: str = ""
    is_terminal: bool = False
    termination_reason: Optional[str] = None


@dataclass
class RunResult:
    """Consolidated summary of an entire simulation run."""
    run_id: str
    seed: int
    total_ticks: int
    terminal_state_hash: str
    is_completed: bool
    termination_reason: str
    total_events: int
    total_messages: int
    resource_usage: Dict[str, Any]
    final_state: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to serializable dictionary."""
        return {
            "run_id": self.run_id,
            "seed": self.seed,
            "total_ticks": self.total_ticks,
            "terminal_state_hash": self.terminal_state_hash,
            "is_completed": self.is_completed,
            "status": "COMPLETED" if self.is_completed else "STOPPED",
            "termination_reason": self.termination_reason,
            "total_events": self.total_events,
            "total_messages": self.total_messages,
            "resource_usage": self.resource_usage,
            "final_state": self.final_state,
        }

    def __getitem__(self, key: str) -> Any:
        if key == "status":
            return "COMPLETED" if self.is_completed else "STOPPED"
        return getattr(self, key)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key) or key == "status"


class SimulationKernel:
    """Authoritative discrete-event simulation kernel with seed control."""

    def __init__(
        self,
        seed: int = 42,
        tick_duration_seconds: float = 1.0,
        max_mailbox_size: int = 50,
        run_id: Optional[str] = None,
        clock: Optional[SimulationClock] = None,
        bus: Optional[MessageBus] = None,
        env: Optional[EnvironmentState] = None,
        logger: Optional[CausalEventLogger] = None
    ):
        self.seed = seed
        self.rng = random.Random(seed)

        self.clock = clock or SimulationClock(tick_duration_seconds=tick_duration_seconds)
        self.event_queue = EventQueue()
        self.message_bus = bus or MessageBus(max_mailbox_size=max_mailbox_size)
        self.state = env if env is not None else EnvironmentState()
        self.logger = logger or CausalEventLogger(run_id=run_id)

        self.agents: Dict[str, BaseAgent] = {}
        self._action_handlers: Dict[str, Callable[[AgentAction, int], Dict[str, Any]]] = {}
        self._termination_predicates: List[Callable[["SimulationKernel"], Optional[str]]] = []
        self.fault_injector: Optional[Any] = None

        self.resource_ledger: Dict[str, float] = {
            "total_ticks": 0,
            "actions_executed": 0,
            "messages_sent": 0,
            "messages_delivered": 0,
            "tokens_consumed": 0.0,
            "compute_cost_usd": 0.0,
        }

    @property
    def current_tick(self) -> int:
        return self.clock.current_tick

    @property
    def bus(self) -> MessageBus:
        """Alias for message_bus."""
        return self.message_bus

    def get_state_hash(self) -> str:
        """Return the SHA-256 hash of the authoritative environment state."""
        return self.state.compute_hash()

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Retrieve registered agent by ID."""
        return self.agents.get(agent_id)

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent into the simulation."""
        self.agents[agent.agent_id] = agent
        self.message_bus.register_agent(agent.agent_id)
        self.logger.log_event(
            tick=self.current_tick,
            actor_id="system",
            action="AGENT_REGISTERED",
            inputs={"agent_id": agent.agent_id, "role": agent.role},
            event_type="SYSTEM"
        )

    def register_action_handler(self, action_type: str, handler: Callable[[AgentAction, int], Dict[str, Any]]) -> None:
        """Register a handler for environment state transitions triggered by agent actions."""
        self._action_handlers[action_type] = handler

    def attach_fault_injector(self, fault_injector: Any) -> None:
        """Attach a deterministic fault injector to intercept execution."""
        self.fault_injector = fault_injector

    def add_termination_predicate(self, predicate: Callable[["SimulationKernel"], Optional[str]]) -> None:
        """Add a custom termination condition check (returns reason string or None)."""
        self._termination_predicates.append(predicate)

    def check_termination(self, max_ticks: Optional[int] = None) -> Optional[str]:
        """Check if any termination condition is satisfied."""
        if max_ticks is not None and self.current_tick >= max_ticks:
            return f"MAX_TICKS_REACHED ({max_ticks})"

        for predicate in self._termination_predicates:
            reason = predicate(self)
            if reason:
                return reason

        return None

    def step(self) -> StepResult:
        """Execute one complete discrete simulation tick."""
        current_tick = self.current_tick
        self.resource_ledger["total_ticks"] = current_tick + 1

        # 1. Deliver pending in-flight messages whose delivery_tick has arrived
        delivered_msgs = self.message_bus.deliver_in_flight(current_tick)
        self.resource_ledger["messages_delivered"] += len(delivered_msgs)
        for d_msg in delivered_msgs:
            self.logger.log_event(
                tick=current_tick,
                actor_id=d_msg.sender_id,
                action="MESSAGE_DELIVERED",
                inputs={"recipient": d_msg.recipient_id, "message_id": d_msg.message_id},
                event_type="MESSAGE_DELIVERED"
            )

        # 2. Process all events scheduled for this tick
        tick_events = self.event_queue.events_for_tick(current_tick)
        events_processed_count = len(tick_events)
        for ev in tick_events:
            self.logger.log_event(
                tick=current_tick,
                actor_id=ev.actor_id,
                action=ev.event_type,
                inputs=ev.payload,
                event_type="DISPATCHED_EVENT",
                parent_event_id=ev.parent_event_id
            )

        # 3. Agent Lifecycle: each active agent perceives incoming messages and decides
        executed_actions: List[Dict[str, Any]] = []

        # Sort agents by ID for deterministic loop order
        sorted_agent_ids = sorted(self.agents.keys())
        for a_id in sorted_agent_ids:
            agent = self.agents[a_id]
            if not agent.is_active:
                continue

            if self.fault_injector and hasattr(self.fault_injector, "is_agent_crashed"):
                if self.fault_injector.is_agent_crashed(a_id, current_tick):
                    self.logger.log_event(
                        tick=current_tick,
                        actor_id=a_id,
                        action="FAULT_AGENT_CRASHED",
                        inputs={},
                        event_type="FAULT"
                    )
                    continue

            incoming = self.message_bus.receive(a_id)
            action = agent.step(
                current_tick=current_tick,
                environment_state=self.state,
                incoming_messages=incoming,
                bus=self.message_bus,
                logger=self.logger
            )

            if action is not None:
                self.resource_ledger["actions_executed"] += 1
                action_record = {
                    "agent_id": a_id,
                    "action_type": action.action_type,
                    "target": action.target,
                    "parameters": action.parameters,
                    "rationale": action.rationale,
                }

                # Dispatch to handler if registered
                handler = self._action_handlers.get(action.action_type)
                if handler:
                    outcome = handler(action, current_tick)
                    action_record["outcome"] = outcome
                else:
                    # Default: message sending or pass
                    if action.action_type == "SEND_MESSAGE":
                        recipient = action.parameters.get("recipient_id", action.target)
                        content = action.parameters.get("content", {})
                        delay = action.parameters.get("delay_ticks", 0)
                        channel = action.parameters.get("channel", "direct")

                        if self.fault_injector and hasattr(self.fault_injector, "should_drop_message"):
                            if self.fault_injector.should_drop_message(a_id, recipient, current_tick):
                                self.logger.log_event(
                                    tick=current_tick,
                                    actor_id=a_id,
                                    action="FAULT_MESSAGE_DROPPED",
                                    inputs={"recipient": recipient},
                                    event_type="FAULT"
                                )
                                continue

                        if self.fault_injector and hasattr(self.fault_injector, "get_message_delay"):
                            delay += self.fault_injector.get_message_delay(current_tick)

                        sent = self.message_bus.send(
                            sender_id=a_id,
                            recipient_id=recipient,
                            content=content,
                            current_tick=current_tick,
                            delay_ticks=delay,
                            channel=channel
                        )
                        self.resource_ledger["messages_sent"] += len(sent)
                        action_record["messages_sent_count"] = len(sent)
                        for s_msg in sent:
                            self.logger.log_event(
                                tick=current_tick,
                                actor_id=a_id,
                                action="MESSAGE_SENT",
                                inputs={"recipient": recipient, "message_id": s_msg.message_id, "content": content},
                                event_type="MESSAGE_SENT"
                            )

                executed_actions.append(action_record)

        # 4. Check termination
        term_reason = self.check_termination()
        is_terminal = term_reason is not None

        # 5. Snapshot state hash for tick
        current_state_hash = self.state.compute_hash()

        # 6. Advance clock to next tick
        self.clock.advance(1)

        return StepResult(
            tick=current_tick,
            events_processed=events_processed_count,
            messages_delivered=len(delivered_msgs),
            actions_executed=executed_actions,
            state_hash=current_state_hash,
            is_terminal=is_terminal,
            termination_reason=term_reason
        )

    def run(self, max_ticks: int = 50) -> RunResult:
        """Run the simulation loop until completion or max_ticks."""
        termination_reason = "RUNNING"

        while self.current_tick < max_ticks:
            step_res = self.step()
            if step_res.is_terminal:
                termination_reason = step_res.termination_reason or "TERMINATED"
                break
        else:
            termination_reason = f"MAX_TICKS_REACHED ({max_ticks})"

        bus_stats = self.message_bus.get_stats()
        self.resource_ledger["total_messages"] = bus_stats["total_sent"]
        self.resource_ledger["dropped_messages"] = bus_stats["total_dropped"]

        return RunResult(
            run_id=self.logger.run_id,
            seed=self.seed,
            total_ticks=self.current_tick,
            terminal_state_hash=self.state.compute_hash(),
            is_completed=True,
            termination_reason=termination_reason,
            total_events=len(self.logger),
            total_messages=bus_stats["total_sent"],
            resource_usage=dict(self.resource_ledger),
            final_state=self.state.to_dict()
        )

    def snapshot(self) -> Dict[str, Any]:
        """Produce full simulation snapshot for checkpointing."""
        return {
            "seed": self.seed,
            "clock": self.clock.snapshot(),
            "event_queue": self.event_queue.snapshot(),
            "message_bus": self.message_bus.snapshot(),
            "state": self.state.snapshot(),
            "agents": {k: a.snapshot() for k, a in self.agents.items()},
            "resource_ledger": dict(self.resource_ledger),
            "latest_event_hash": self.logger.latest_hash
        }

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore simulation state from snapshot."""
        self.seed = data["seed"]
        self.clock.restore(data["clock"])
        self.event_queue.restore(data["event_queue"])
        self.message_bus.restore(data["message_bus"])
        self.state.restore(data["state"])
        for k, agent_data in data["agents"].items():
            if k in self.agents:
                self.agents[k].restore(agent_data)
        self.resource_ledger = dict(data["resource_ledger"])
