"""Memory Retrieval Ablation Experiment Runner."""

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from simlab.memory.scoring import (
    calculate_recency_decay,
    calculate_tri_factor_scores,
    cosine_similarity,
    min_max_norm,
)


@dataclass
class AblationConditionResult:
    """Statistical summary of an ablation condition."""
    condition_code: str
    condition_name: str
    weights: Tuple[float, float, float]
    mrr_mean: float
    mrr_std: float
    ndcg5_mean: float
    temporal_inversion_rate: float
    total_queries: int
    unresolved_queries: int = 0


class MemoryAblationRunner:
    """Executes controlled parameter sweeps and component ablations on memory pools."""

    DEFAULT_CONDITIONS = [
        {"code": "A1", "name": "RECENCY_ONLY", "weights": (1.0, 0.0, 0.0)},
        {"code": "A2", "name": "RELEVANCE_ONLY", "weights": (0.0, 1.0, 0.0)},
        {"code": "A3", "name": "IMPORTANCE_ONLY", "weights": (0.0, 0.0, 1.0)},
        {"code": "A4", "name": "RECENCY_RELEVANCE", "weights": (0.3, 0.7, 0.0)},
        {"code": "A5", "name": "RECENCY_IMPORTANCE", "weights": (0.5, 0.0, 0.5)},
        {"code": "A6", "name": "RELEVANCE_IMPORTANCE", "weights": (0.0, 0.7, 0.3)},
        {"code": "A7", "name": "FULL_TRI_FACTOR", "weights": (0.2, 0.5, 0.3)},
    ]

    def __init__(self, memories: List[Dict[str, Any]], current_time_hours: float = 72.0):
        self.memories = list(memories)
        self.current_time_hours = current_time_hours

    @staticmethod
    def compute_ndcg5(target_rank: int) -> float:
        """Normalized Discounted Cumulative Gain at rank 5."""
        if target_rank <= 5:
            return 1.0 / math.log2(target_rank + 1)
        return 0.0

    @staticmethod
    def compute_temporal_inversion_rate(top5_indices: List[int], memories: List[Dict[str, Any]]) -> float:
        """Ratio of chronological inversions among top-5 retrieved memories."""
        inversions = 0
        total_pairs = 0
        for i in range(len(top5_indices)):
            for j in range(i + 1, len(top5_indices)):
                total_pairs += 1
                t_i = memories[top5_indices[i]].get("timestamp_hours", 0.0)
                t_j = memories[top5_indices[j]].get("timestamp_hours", 0.0)
                if t_i < t_j:
                    inversions += 1
        return inversions / float(total_pairs) if total_pairs > 0 else 0.0

    def evaluate_query(
        self,
        query: Dict[str, Any],
        weights: Tuple[float, float, float]
    ) -> Dict[str, Any]:
        """
        Evaluate single retrieval query safely against memory pool.
        Handles missing target IDs gracefully without throwing ValueError.
        """
        target_id = query.get("target_id")
        qvec = query.get("qvec", [])
        alpha, beta, gamma = weights

        recencies = [
            calculate_recency_decay(self.current_time_hours - m.get("timestamp_hours", 0.0))
            for m in self.memories
        ]
        relevances = [
            cosine_similarity(qvec, m.get("embedding", []))
            for m in self.memories
        ]
        importances = [
            float(m.get("importance", 5.0))
            for m in self.memories
        ]

        scores = calculate_tri_factor_scores(
            recencies=recencies,
            relevances=relevances,
            importances=importances,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            norm_fn=min_max_norm
        )

        ranked_indices = sorted(range(len(self.memories)), key=lambda i: scores[i], reverse=True)

        # Defensive lookup: search for target memory index
        target_cand_idx = None
        for idx, m in enumerate(self.memories):
            if m.get("id") == target_id or m.get("memory_id") == target_id:
                target_cand_idx = idx
                break

        if target_cand_idx is None:
            # Target missing from candidate pool: report unresolved rather than crashing
            return {
                "query_id": query.get("query_id", "unknown"),
                "target_id": target_id,
                "target_found": False,
                "target_rank": len(self.memories),
                "reciprocal_rank": 0.0,
                "ndcg5": 0.0,
                "temporal_inversion_rate": 0.0
            }

        target_rank = ranked_indices.index(target_cand_idx) + 1
        top5 = ranked_indices[:5]

        return {
            "query_id": query.get("query_id", "unknown"),
            "target_id": target_id,
            "target_found": True,
            "target_rank": target_rank,
            "reciprocal_rank": 1.0 / target_rank,
            "ndcg5": self.compute_ndcg5(target_rank),
            "temporal_inversion_rate": self.compute_temporal_inversion_rate(top5, self.memories)
        }

    def run_condition(
        self,
        condition_code: str,
        condition_name: str,
        weights: Tuple[float, float, float],
        queries: List[Dict[str, Any]]
    ) -> AblationConditionResult:
        """Run all queries for a single condition."""
        results = [self.evaluate_query(q, weights) for q in queries]
        mrrs = [r["reciprocal_rank"] for r in results]
        ndcgs = [r["ndcg5"] for r in results]
        inversions = [r["temporal_inversion_rate"] for r in results]
        unresolved = sum(1 for r in results if not r["target_found"])

        return AblationConditionResult(
            condition_code=condition_code,
            condition_name=condition_name,
            weights=weights,
            mrr_mean=float(np.mean(mrrs)) if mrrs else 0.0,
            mrr_std=float(np.std(mrrs, ddof=1)) if len(mrrs) > 1 else 0.0,
            ndcg5_mean=float(np.mean(ndcgs)) if ndcgs else 0.0,
            temporal_inversion_rate=float(np.mean(inversions)) if inversions else 0.0,
            total_queries=len(queries),
            unresolved_queries=unresolved
        )

    def run_all(self, queries: List[Dict[str, Any]]) -> List[AblationConditionResult]:
        """Run standard 7 ablation conditions across all queries."""
        summaries = []
        for cond in self.DEFAULT_CONDITIONS:
            res = self.run_condition(
                condition_code=cond["code"],
                condition_name=cond["name"],
                weights=cond["weights"],
                queries=queries
            )
            summaries.append(res)
        return summaries
