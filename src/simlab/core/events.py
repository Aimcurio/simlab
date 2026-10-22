"""Simulation Events and Deterministic Priority Queue."""

import heapq
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional
import uuid


class EventType(str, Enum):
    """Canonical event types for simulation logging and dispatch."""
    TICK_START = "TICK_START"
    TICK_END = "TICK_END"
    AGENT_DECISION = "AGENT_DECISION"
    AGENT_ACTION = "AGENT_ACTION"
    MESSAGE_SENT = "MESSAGE_SENT"
    MESSAGE_DELIVERED = "MESSAGE_DELIVERED"
    ENVIRONMENT_UPDATE = "ENVIRONMENT_UPDATE"
    FAULT_INJECTED = "FAULT_INJECTED"
    SIMULATION_END = "SIMULATION_END"


class EventPriority(IntEnum):
    """Event dispatch priority. Lower integer values execute earlier."""
    CRITICAL_SYSTEM = 0
    ENVIRONMENT_TRANSITION = 1
    AGENT_DECISION = 2
    AGENT_ACTION = 3
    MESSAGE_DELIVERY = 4
    OBSERVATION = 5
    DIAGNOSTIC = 6


@dataclass(order=True)
class Event:
    """Simulation Event with deterministic priority ordering."""
    # Heap comparison fields
    tick: int
    priority: int
    sequence_id: int

    # Non-comparison fields
    event_id: str = field(compare=False)
    event_type: str = field(compare=False)
    actor_id: str = field(compare=False)
    payload: Dict[str, Any] = field(default_factory=dict, compare=False)
    parent_event_id: Optional[str] = field(default=None, compare=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to serializable dictionary."""
        return {
            "event_id": self.event_id,
            "tick": self.tick,
            "priority": self.priority,
            "sequence_id": self.sequence_id,
            "event_type": self.event_type,
            "actor_id": self.actor_id,
            "payload": self.payload,
            "parent_event_id": self.parent_event_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Reconstruct event from dictionary."""
        return cls(
            tick=data["tick"],
            priority=data["priority"],
            sequence_id=data["sequence_id"],
            event_id=data["event_id"],
            event_type=data["event_type"],
            actor_id=data["actor_id"],
            payload=data.get("payload", {}),
            parent_event_id=data.get("parent_event_id"),
        )


class EventQueue:
    """Deterministic event queue using min-heap ordered by (tick, priority, sequence_id)."""

    def __init__(self):
        self._heap: List[Event] = []
        self._sequence_counter: int = 0

    def schedule(
        self,
        tick: int,
        event_type: str,
        actor_id: str,
        payload: Optional[Dict[str, Any]] = None,
        priority: EventPriority = EventPriority.AGENT_ACTION,
        parent_event_id: Optional[str] = None,
        event_id: Optional[str] = None
    ) -> Event:
        """Schedule a new event into the priority queue."""
        self._sequence_counter += 1
        ev_id = event_id or f"evt_{tick:05d}_{self._sequence_counter:05d}"
        ev = Event(
            tick=tick,
            priority=int(priority),
            sequence_id=self._sequence_counter,
            event_id=ev_id,
            event_type=event_type,
            actor_id=actor_id,
            payload=payload or {},
            parent_event_id=parent_event_id
        )
        heapq.heappush(self._heap, ev)
        return ev

    def peek(self) -> Optional[Event]:
        """Peek at the earliest event without removing it."""
        if not self._heap:
            return None
        return self._heap[0]

    def pop(self) -> Optional[Event]:
        """Pop the earliest event."""
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def events_for_tick(self, tick: int) -> List[Event]:
        """Extract all events scheduled for a specific tick."""
        matching: List[Event] = []
        while self._heap and self._heap[0].tick <= tick:
            ev = heapq.heappop(self._heap)
            matching.append(ev)
        return matching

    def is_empty(self) -> bool:
        """Return True if no events remain in queue."""
        return len(self._heap) == 0

    def __len__(self) -> int:
        return len(self._heap)

    def snapshot(self) -> Dict[str, Any]:
        """Snapshot current event queue state."""
        return {
            "sequence_counter": self._sequence_counter,
            "events": [ev.to_dict() for ev in sorted(self._heap)]
        }

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore event queue from snapshot."""
        self._sequence_counter = data["sequence_counter"]
        self._heap = [Event.from_dict(d) for d in data["events"]]
        heapq.heapify(self._heap)
