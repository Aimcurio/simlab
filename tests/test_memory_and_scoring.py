"""Tests for Memory, Scoring, Normalization, and Ablation."""

import pytest
import numpy as np
from simlab.memory import (
    min_max_norm,
    z_score_norm,
    softmax_norm,
    cosine_similarity,
    MemoryStream,
    MemoryAblationRunner,
)


def test_min_max_norm_tie_handling_defect_remediation():
    """
    CRITICAL DEFECT TEST (SIM-06):
    Previous implementation mapped identical values to 1.0.
    Remediated implementation must map identical values to neutral baseline (0.0).
    """
    uniform_zeros = [0.0, 0.0, 0.0]
    normed = min_max_norm(uniform_zeros)
    assert normed == [0.0, 0.0, 0.0]

    uniform_fives = [5.0, 5.0, 5.0]
    normed_fives = min_max_norm(uniform_fives)
    assert normed_fives == [0.0, 0.0, 0.0]


def test_min_max_norm_edge_cases():
    # Empty
    assert min_max_norm([]) == []
    # Single element
    assert min_max_norm([42.0]) == [0.0]
    # Standard range
    standard = min_max_norm([10.0, 20.0, 30.0])
    assert standard == [0.0, 0.5, 1.0]
    # Negative values
    negs = min_max_norm([-10.0, 0.0, 10.0])
    assert negs == [0.0, 0.5, 1.0]


def test_cosine_similarity_edge_cases():
    # Identical
    assert pytest.approx(cosine_similarity([1.0, 0.0], [1.0, 0.0])) == 1.0
    # Orthogonal
    assert pytest.approx(cosine_similarity([1.0, 0.0], [0.0, 1.0])) == 0.0
    # Zero vector
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_memory_stream_capacity_and_retrieval():
    stream = MemoryStream(capacity=3)
    stream.add("Memory 1", timestamp_hours=1.0, importance=5.0, embedding=[1.0, 0.0])
    stream.add("Memory 2", timestamp_hours=2.0, importance=7.0, embedding=[0.0, 1.0])
    stream.add("Memory 3", timestamp_hours=3.0, importance=8.0, embedding=[0.7, 0.7])
    assert len(stream) == 3

    # Add 4th -> FIFO eviction of Memory 1
    stream.add("Memory 4", timestamp_hours=4.0, importance=9.0, embedding=[1.0, 0.0])
    assert len(stream) == 3
    mem_ids = [m.text for m in stream._memories]
    assert "Memory 1" not in mem_ids
    assert "Memory 4" in mem_ids

    # Retrieve relevant to [1.0, 0.0]
    results = stream.retrieve(query_embedding=[1.0, 0.0], current_time_hours=5.0, top_k=2)
    assert len(results) == 2
    # Memory 4 should rank highest (most recent and highest relevance)
    top_item, score = results[0]
    assert top_item.text == "Memory 4"


def test_ablation_missing_target_safety_defect_remediation():
    """
    CRITICAL DEFECT TEST (SIM-05):
    Query referencing a non-existent target ID must NOT raise ValueError.
    """
    runner = MemoryAblationRunner(
        memories=[
            {"id": "mem_01", "timestamp_hours": 10.0, "importance": 5.0, "embedding": [1.0, 0.0]},
            {"id": "mem_02", "timestamp_hours": 20.0, "importance": 8.0, "embedding": [0.0, 1.0]},
        ],
        current_time_hours=25.0
    )

    # Target mem_99 does NOT exist in memory pool
    res = runner.evaluate_query(
        query={"query_id": "q1", "target_id": "mem_99", "qvec": [1.0, 0.0]},
        weights=(0.3, 0.5, 0.2)
    )

    assert res["target_found"] is False
    assert res["reciprocal_rank"] == 0.0
    assert res["query_id"] == "q1"
