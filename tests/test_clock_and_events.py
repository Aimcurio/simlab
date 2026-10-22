"""Tests for SimulationClock and EventQueue."""

import pytest
from simlab.core.clock import SimulationClock
from simlab.core.events import EventQueue, EventPriority


def test_simulation_clock_progression():
    clock = SimulationClock(tick_duration_seconds=0.5, initial_tick=0)
    assert clock.current_tick == 0
    assert clock.virtual_time_seconds == 0.0

    clock.advance(3)
    assert clock.current_tick == 3
    assert clock.virtual_time_seconds == 1.5

    snap = clock.snapshot()
    clock.advance(2)
    assert clock.current_tick == 5

    clock.restore(snap)
    assert clock.current_tick == 3

    clock.reset()
    assert clock.current_tick == 0


def test_event_queue_priority_and_ordering():
    eq = EventQueue()
    
    # Schedule out of order
    e3 = eq.schedule(tick=5, event_type="ACTION", actor_id="agent_1", priority=EventPriority.AGENT_ACTION)
    e1 = eq.schedule(tick=1, event_type="CRITICAL", actor_id="system", priority=EventPriority.CRITICAL_SYSTEM)
    e2 = eq.schedule(tick=1, event_type="OBSERVE", actor_id="agent_2", priority=EventPriority.OBSERVATION)

    assert len(eq) == 3

    # Tick 1 critical should pop first
    first = eq.pop()
    assert first.event_id == e1.event_id
    assert first.tick == 1
    assert first.priority == EventPriority.CRITICAL_SYSTEM

    # Tick 1 observe second
    second = eq.pop()
    assert second.event_id == e2.event_id
    assert second.tick == 1

    # Tick 5 action third
    third = eq.pop()
    assert third.event_id == e3.event_id
    assert third.tick == 5

    assert eq.is_empty()


def test_event_queue_snapshot_restore():
    eq = EventQueue()
    eq.schedule(tick=2, event_type="A", actor_id="a1")
    eq.schedule(tick=4, event_type="B", actor_id="a2")
    
    snap = eq.snapshot()
    eq.pop()
    assert len(eq) == 1

    eq.restore(snap)
    assert len(eq) == 2
    ev = eq.pop()
    assert ev.tick == 2
