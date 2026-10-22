"""Associative Memory Stream with Retrieval and Capacity Management."""

import uuid
from typing import Any, Dict, List, Optional, Sequence, Tuple

from simlab.memory.item import MemoryItem
from simlab.memory.scoring import (
    calculate_recency_decay,
    calculate_tri_factor_scores,
    cosine_similarity,
    min_max_norm,
)


class MemoryStream:
    """
    Cognitive episodic memory stream:
    - Bounded capacity with FIFO or importance-based retention
    - Tri-factor retrieval: Recency decay, semantic relevance, and subjective importance
    - Access frequency and reflection tagging
    """

    def __init__(self, capacity: int = 500, decay_rate: float = 0.995):
        self.capacity = max(1, capacity)
        self.decay_rate = decay_rate
        self._memories: List[MemoryItem] = []

    @property
    def size(self) -> int:
        """Current number of stored memories."""
        return len(self._memories)

    def add(
        self,
        text: Any,
        timestamp_hours: float = 0.0,
        importance: float = 1.0,
        embedding: Optional[Sequence[float]] = None,
        is_reflection: bool = False,
        memory_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryItem:
        """Append a new memory item to stream with capacity eviction."""
        if isinstance(text, MemoryItem):
            item = text
        else:
            mem_id = memory_id or f"mem_{uuid.uuid4().hex[:8]}"
            item = MemoryItem(
                memory_id=mem_id,
                text=str(text),
                timestamp_hours=float(timestamp_hours),
                importance=float(max(1.0, min(10.0, importance))),
                embedding=list(embedding) if embedding else None,
                last_accessed_hours=float(timestamp_hours),
                is_reflection=is_reflection,
                metadata=metadata or {}
            )
        self._memories.append(item)

        # Capacity management: FIFO eviction
        while len(self._memories) > self.capacity:
            self._memories.pop(0)

        return item

    def retrieve(
        self,
        query_embedding: Sequence[float],
        current_time_hours: float,
        top_k: int = 5,
        alpha: float = 0.3,
        beta: float = 0.5,
        gamma: float = 0.2,
        decay_rate: Optional[float] = None
    ) -> List[Tuple[MemoryItem, float]]:
        """
        Retrieve top_k memories scored by tri-factor weights.
        Returns list of (MemoryItem, score) ordered by score descending.
        """
        if not self._memories:
            return []

        active_decay = decay_rate if decay_rate is not None else self.decay_rate
        recencies: List[float] = []
        relevances: List[float] = []
        importances: List[float] = []

        for m in self._memories:
            # Recency
            delta_t = max(0.0, current_time_hours - m.timestamp_hours)
            rec = calculate_recency_decay(delta_t, active_decay)
            recencies.append(rec)

            # Relevance
            if m.embedding and query_embedding:
                rel = cosine_similarity(query_embedding, m.embedding)
            else:
                rel = 0.0
            relevances.append(rel)

            # Importance
            importances.append(m.importance)

        scores = calculate_tri_factor_scores(
            recencies=recencies,
            relevances=relevances,
            importances=importances,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            norm_fn=min_max_norm
        )

        ranked = sorted(
            zip(self._memories, scores),
            key=lambda x: x[1],
            reverse=True
        )

        top_results = ranked[:top_k]
        # Update last_accessed on retrieved memories
        for item, _ in top_results:
            item.last_accessed_hours = current_time_hours
            item.access_count += 1

        return top_results

    def __len__(self) -> int:
        return len(self._memories)

    def to_list(self) -> List[Dict[str, Any]]:
        """Return all memories as serializable dictionaries."""
        return [m.to_dict() for m in self._memories]


# Backward/alternative naming compatibility
AssociativeMemoryStream = MemoryStream

