"""Deterministic Fault Injector for Multi-Agent Resilience Testing."""

import random
from typing import Any, Dict, List, Optional
from simlab.faults.types import FaultRecord, FaultType


class FaultInjector:
    """
    Controlled, seed-reproducible fault injector:
    - Message loss (probabilistic drop)
    - Message latency (extra delay ticks)
    - Agent crash / timeout
    - Tool/action execution failures
    - Resource depletion shock
    """

    def __init__(
        self,
        seed: int = 42,
        message_loss_rate: float = 0.0,
        extra_delay_ticks: int = 0,
        crash_schedule: Optional[Dict[str, int]] = None,  # agent_id -> tick
        action_failure_rate: float = 0.0,
        resource_drain_schedule: Optional[Dict[int, Dict[str, float]]] = None  # tick -> {resource: amount}
    ):
        self.seed = seed
        self.rng = random.Random(seed)
        self.message_loss_rate = max(0.0, min(1.0, message_loss_rate))
        self.extra_delay_ticks = max(0, extra_delay_ticks)
        self.crash_schedule = dict(crash_schedule or {})
        self.action_failure_rate = max(0.0, min(1.0, action_failure_rate))
        self.resource_drain_schedule = dict(resource_drain_schedule or {})

        self.history: List[FaultRecord] = []

    def should_drop_message(self, sender: str, recipient: str, tick: int) -> bool:
        """Evaluate if message should be dropped due to network partition/loss."""
        if self.message_loss_rate <= 0.0:
            return False
        drop = self.rng.random() < self.message_loss_rate
        if drop:
            self.history.append(FaultRecord(
                fault_type=FaultType.MESSAGE_LOSS,
                tick=tick,
                target=f"{sender}->{recipient}",
                details={"loss_rate": self.message_loss_rate}
            ))
        return drop

    def get_message_delay(self, tick: int) -> int:
        """Calculate extra message delivery latency."""
        if self.extra_delay_ticks > 0:
            self.history.append(FaultRecord(
                fault_type=FaultType.MESSAGE_DELAY,
                tick=tick,
                target="message_bus",
                details={"added_delay": self.extra_delay_ticks}
            ))
        return self.extra_delay_ticks

    def should_crash_agent(self, agent_id: str, tick: int) -> bool:
        """Check if agent should be crashed at this tick."""
        crash_tick = self.crash_schedule.get(agent_id)
        if crash_tick is not None and tick >= crash_tick:
            self.history.append(FaultRecord(
                fault_type=FaultType.AGENT_CRASH,
                tick=tick,
                target=agent_id,
                details={"scheduled_crash_tick": crash_tick}
            ))
            return True
        return False

    def should_fail_action(self, action_type: str, actor_id: str, tick: int) -> bool:
        """Check if action execution fails probabilistically."""
        if self.action_failure_rate <= 0.0:
            return False
        fail = self.rng.random() < self.action_failure_rate
        if fail:
            self.history.append(FaultRecord(
                fault_type=FaultType.ACTION_FAILURE,
                tick=tick,
                target=f"{actor_id}:{action_type}",
                details={"failure_rate": self.action_failure_rate}
            ))
        return fail

    def apply_resource_drains(self, state: Any, tick: int) -> Dict[str, float]:
        """Apply scheduled resource shocks to environment state."""
        drain = self.resource_drain_schedule.get(tick)
        if not drain:
            return {}

        applied: Dict[str, float] = {}
        for res, amount in drain.items():
            curr = state.get(res, 0.0)
            new_val = max(0.0, curr - amount)
            state.set(res, new_val)
            applied[res] = amount
            self.history.append(FaultRecord(
                fault_type=FaultType.RESOURCE_DRAIN,
                tick=tick,
                target=res,
                details={"drained_amount": amount, "new_value": new_val}
            ))
        return applied

    def attach_to_kernel(self, kernel: Any) -> None:
        """Hook fault injector into kernel message bus and step cycle."""
        # Wrap message bus send
        original_send = kernel.message_bus.send

        def fault_wrapped_send(
            sender_id: str,
            recipient_id: str,
            content: Dict[str, Any],
            current_tick: int,
            delay_ticks: int = 0,
            channel: str = "direct",
            metadata: Optional[Dict[str, Any]] = None
        ):
            # Check message drop
            if self.should_drop_message(sender_id, recipient_id, current_tick):
                return []
            extra = self.get_message_delay(current_tick)
            return original_send(
                sender_id=sender_id,
                recipient_id=recipient_id,
                content=content,
                current_tick=current_tick,
                delay_ticks=delay_ticks + extra,
                channel=channel,
                metadata=metadata
            )

        kernel.message_bus.send = fault_wrapped_send

        # Wrap step to check agent crashes & resource drains
        original_step = kernel.step

        def fault_wrapped_step():
            current_tick = kernel.current_tick
            # Apply crashes
            for a_id, agent in kernel.agents.items():
                if self.should_crash_agent(a_id, current_tick):
                    agent.set_active(False)
            # Apply resource drains
            self.apply_resource_drains(kernel.state, current_tick)
            return original_step()

        kernel.step = fault_wrapped_step
