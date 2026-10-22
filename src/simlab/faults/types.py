"""Fault Injection Types and Configurations."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class FaultType(str, Enum):
    """Types of controlled faults supported by SimLab."""
    MESSAGE_DELAY = "MESSAGE_DELAY"
    MESSAGE_LOSS = "MESSAGE_LOSS"
    AGENT_CRASH = "AGENT_CRASH"
    ACTION_FAILURE = "ACTION_FAILURE"
    OBSERVATION_CORRUPTION = "OBSERVATION_CORRUPTION"
    RESOURCE_DRAIN = "RESOURCE_DRAIN"


@dataclass
class FaultRecord:
    """Record of an activated fault injection event."""
    fault_type: FaultType
    tick: int
    target: str
    details: Dict[str, Any] = field(default_factory=dict)
