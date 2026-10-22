"""Bounded Message Bus and Communication Subsystem."""

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class MailboxFullPolicy(str, Enum):
    """Behavior when an agent mailbox exceeds maximum capacity."""
    DROP_OLDEST = "DROP_OLDEST"
    REJECT_NEW = "REJECT_NEW"


@dataclass
class Message:
    """Inter-agent message."""
    message_id: str
    sender_id: str
    recipient_id: str
    channel: str
    content: Dict[str, Any]
    sent_tick: int
    delivery_tick: int
    dropped: bool = False
    delivered: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "channel": self.channel,
            "content": self.content,
            "sent_tick": self.sent_tick,
            "delivery_tick": self.delivery_tick,
            "dropped": self.dropped,
            "delivered": self.delivered,
            "metadata": self.metadata,
        }


class MessageBus:
    """Bounded, ordered message bus with mailbox limits and channels."""

    def __init__(self, max_mailbox_size: int = 50, full_policy: MailboxFullPolicy = MailboxFullPolicy.REJECT_NEW):
        self.max_mailbox_size = max(1, max_mailbox_size)
        self.full_policy = full_policy
        self._mailboxes: Dict[str, List[Message]] = {}
        self._in_flight: List[Message] = []
        self._subscriptions: Dict[str, Set[str]] = {}  # channel -> set of agent_ids
        self._total_messages_sent: int = 0
        self._total_messages_delivered: int = 0
        self._total_messages_dropped: int = 0

    @property
    def total_messages_routed(self) -> int:
        return self._total_messages_delivered

    def register_agent(self, agent_id: str) -> None:
        """Initialize an agent mailbox."""
        if agent_id not in self._mailboxes:
            self._mailboxes[agent_id] = []

    def subscribe(self, agent_id: str, channel: str) -> None:
        """Subscribe an agent to a broadcast channel."""
        self.register_agent(agent_id)
        if channel not in self._subscriptions:
            self._subscriptions[channel] = set()
        self._subscriptions[channel].add(agent_id)

    def send(
        self,
        sender_id: str,
        recipient_id: str,
        content: Dict[str, Any],
        current_tick: int,
        delay_ticks: int = 0,
        channel: str = "direct",
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Message]:
        """
        Send a message directly or broadcast to a channel.
        Messages are scheduled for delivery at (current_tick + delay_ticks).
        """
        delivery_tick = current_tick + max(0, delay_ticks)
        created_messages: List[Message] = []

        if recipient_id == "broadcast" or channel != "direct":
            # Broadcast to channel subscribers
            recipients = self._subscriptions.get(channel, set())
            target_ids = [r for r in recipients if r != sender_id]
        else:
            target_ids = [recipient_id]

        for target in target_ids:
            self.register_agent(target)
            self._total_messages_sent += 1
            msg = Message(
                message_id=f"msg_{sender_id}_{target}_t{current_tick}_{self._total_messages_sent:04d}",
                sender_id=sender_id,
                recipient_id=target,
                channel=channel,
                content=content,
                sent_tick=current_tick,
                delivery_tick=delivery_tick,
                metadata=metadata or {}
            )
            self._in_flight.append(msg)
            created_messages.append(msg)

        return created_messages

    def deliver_in_flight(self, current_tick: int) -> List[Message]:
        """Deliver all messages whose delivery_tick has arrived."""
        delivered_this_tick: List[Message] = []
        remaining_in_flight: List[Message] = []

        for msg in self._in_flight:
            if msg.delivery_tick <= current_tick:
                # Deliver to recipient mailbox
                target_box = self._mailboxes.setdefault(msg.recipient_id, [])
                if len(target_box) >= self.max_mailbox_size:
                    if self.full_policy == MailboxFullPolicy.DROP_OLDEST:
                        dropped = target_box.pop(0)
                        dropped.dropped = True
                        self._total_messages_dropped += 1
                        msg.delivered = True
                        target_box.append(msg)
                        delivered_this_tick.append(msg)
                        self._total_messages_delivered += 1
                    else:  # REJECT_NEW
                        msg.dropped = True
                        self._total_messages_dropped += 1
                else:
                    msg.delivered = True
                    target_box.append(msg)
                    delivered_this_tick.append(msg)
                    self._total_messages_delivered += 1
            else:
                remaining_in_flight.append(msg)

        self._in_flight = remaining_in_flight
        return delivered_this_tick

    def receive(self, agent_id: str) -> List[Message]:
        """Fetch and drain all delivered messages from an agent's mailbox."""
        if agent_id not in self._mailboxes:
            return []
        messages = list(self._mailboxes[agent_id])
        self._mailboxes[agent_id].clear()
        return messages

    # Alias for API compatibility
    retrieve_inbox = receive

    def peek(self, agent_id: str) -> List[Message]:
        """Inspect mailbox messages without draining."""
        return list(self._mailboxes.get(agent_id, []))

    def get_stats(self) -> Dict[str, Any]:
        """Return bus throughput and queue metrics."""
        return {
            "total_sent": self._total_messages_sent,
            "total_delivered": self._total_messages_delivered,
            "total_dropped": self._total_messages_dropped,
            "in_flight_count": len(self._in_flight),
            "mailboxes": {k: len(v) for k, v in self._mailboxes.items()}
        }

    def snapshot(self) -> Dict[str, Any]:
        """Capture message bus snapshot."""
        return {
            "max_mailbox_size": self.max_mailbox_size,
            "full_policy": self.full_policy.value,
            "mailboxes": {k: [m.to_dict() for m in v] for k, v in self._mailboxes.items()},
            "in_flight": [m.to_dict() for m in self._in_flight],
            "subscriptions": {k: list(v) for k, v in self._subscriptions.items()},
            "stats": self.get_stats()
        }

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore message bus state."""
        self.max_mailbox_size = data["max_mailbox_size"]
        self.full_policy = MailboxFullPolicy(data["full_policy"])
        self._subscriptions = {k: set(v) for k, v in data["subscriptions"].items()}
        self._mailboxes = {
            k: [Message(**m) for m in v]
            for k, v in data["mailboxes"].items()
        }
        self._in_flight = [Message(**m) for m in data["in_flight"]]
        stats = data.get("stats", {})
        self._total_messages_sent = stats.get("total_sent", 0)
        self._total_messages_delivered = stats.get("total_delivered", 0)
        self._total_messages_dropped = stats.get("total_dropped", 0)
