"""SimLab — Controlled, Reproducible, Observable Multi-Agent Experimentation Platform."""

__version__ = "0.2.0"

from simlab.core.kernel import SimulationKernel, StepResult, RunResult
from simlab.core.clock import SimulationClock, DiscreteClock
from simlab.core.bus import MessageBus, Message, MailboxFullPolicy
from simlab.core.events import Event, EventQueue, EventPriority, EventType
from simlab.core.logging import CausalEventLogger
from simlab.core.replay import ReplayEngine
from simlab.core.state import EnvironmentState

__all__ = [
    "__version__",
    "SimulationKernel",
    "StepResult",
    "RunResult",
    "SimulationClock",
    "DiscreteClock",
    "MessageBus",
    "Message",
    "MailboxFullPolicy",
    "Event",
    "EventQueue",
    "EventPriority",
    "EventType",
    "CausalEventLogger",
    "ReplayEngine",
    "EnvironmentState",
]
