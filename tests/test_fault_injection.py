"""Tests for Deterministic Fault Injector."""

import pytest
from simlab.core.kernel import SimulationKernel
from simlab.faults import FaultInjector, FaultType
from simlab.agents.worker import WorkerAgent


def test_message_drop_injection():
    kernel = SimulationKernel(seed=10)
    # 100% loss rate
    fault = FaultInjector(seed=10, message_loss_rate=1.0)
    fault.attach_to_kernel(kernel)

    kernel.message_bus.register_agent("a1")
    kernel.message_bus.register_agent("a2")

    sent = kernel.message_bus.send("a1", "a2", {"text": "hello"}, current_tick=0)
    assert len(sent) == 0  # Dropped!
    assert len(fault.history) == 1
    assert fault.history[0].fault_type == FaultType.MESSAGE_LOSS


def test_message_delay_injection():
    kernel = SimulationKernel(seed=10)
    # 3 ticks extra delay
    fault = FaultInjector(seed=10, extra_delay_ticks=3)
    fault.attach_to_kernel(kernel)

    kernel.message_bus.register_agent("a1")
    kernel.message_bus.register_agent("a2")

    sent = kernel.message_bus.send("a1", "a2", {"text": "hello"}, current_tick=1, delay_ticks=0)
    assert len(sent) == 1
    assert sent[0].delivery_tick == 4  # 1 + 0 + 3


def test_agent_crash_injection():
    kernel = SimulationKernel(seed=42)
    w = WorkerAgent(agent_id="w1")
    kernel.register_agent(w)

    # Schedule crash at tick 2
    fault = FaultInjector(seed=42, crash_schedule={"w1": 2})
    fault.attach_to_kernel(kernel)

    assert w.is_active is True
    kernel.step()  # tick 0
    assert w.is_active is True
    kernel.step()  # tick 1
    assert w.is_active is True
    kernel.step()  # tick 2 -> crash
    assert w.is_active is False
