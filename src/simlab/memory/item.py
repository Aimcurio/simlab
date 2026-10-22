"""Memory Item Data Model."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class MemoryItem:
    """Individual episodic memory record."""
    memory_id: str
    text: str = ""
    timestamp_hours: float = 0.0
    importance: float = 1.0
    embedding: Optional[List[float]] = None
    last_accessed_hours: float = 0.0
    access_count: int = 0
    is_reflection: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    content: Optional[str] = None

    def __post_init__(self):
        if self.content and not self.text:
            self.text = self.content
        elif self.text and not self.content:
            self.content = self.text

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to serializable dictionary."""
        return {
            "memory_id": self.memory_id,
            "text": self.text,
            "timestamp_hours": self.timestamp_hours,
            "importance": self.importance,
            "embedding": self.embedding,
            "last_accessed_hours": self.last_accessed_hours,
            "access_count": self.access_count,
            "is_reflection": self.is_reflection,
            "metadata": self.metadata,
        }
