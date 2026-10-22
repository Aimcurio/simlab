r"""
Empirical Challenge Verification Tests: EXP-AB-01-COMP
Author: audit_challenger_2 (Adversarial Empirical Challenger)
Location: E:\projects\simlab\audits\EXP-AB-01-COMP\test_challenger_empirical.py

Asserts:
1. Reflection crowding dynamics across seeds & importance levels [5.0, 6.0, 7.0, 8.0, 8.5].
2. Normalization stress-testing (Softmax rescuing A7 absolute score vs within-scheme comparison to A4).
3. Simplex true global optimum (alpha=0.06, beta=0.94, gamma=0.0 -> MRR=0.7535) and interior points beating A4.
"""

import os
import json
import math
import numpy as np
import pytest

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = str(ROOT_DIR / "phase3_execution" / "SimLab_MemBench_500.json")
CHALLENGE_RESULTS_PATH = str(ROOT_DIR / "empirical_challenge_results.json")


@pytest.fixture(scope="module")
def challenge_results():
    assert os.path.exists(CHALLENGE_RESULTS_PATH), "Run challenge_empirical_tests.py first!"
    with open(CHALLENGE_RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_reflection_importance_5_0_eliminates_crowding_across_all_seeds(challenge_results):
    """Assert that reflection importance = 5.0 eliminates 100% Rank-1 crowding across all 80 seeds."""
    c1 = challenge_results["challenge_1"]
    # Deterministic CF-1
    assert c1["deterministic_sweep"]["5.0"]["rank1_crowding_count"] == 0
    assert c1["deterministic_sweep"]["5.0"]["top5_refl_slots"] == 0
    assert round(c1["deterministic_sweep"]["5.0"]["mrr_mean"], 4) == 0.0929

    # Multi-seed Random Partition (50 seeds)
    assert c1["rand_part_5_0"]["crowding_max"] == 0
    assert c1["rand_part_5_0"]["top5_max"] == 0

    # Multi-seed K-Means (30 seeds)
    assert c1["km_5_0"]["crowding_max"] == 0
    assert c1["km_5_0"]["top5_max"] == 0


def test_reflection_importance_phase_transition(challenge_results):
    """Assert sharp phase transition: 5.0 -> 0%, 5.5 -> 15%, 6.0-8.5 -> 100% crowding."""
    sweep = challenge_results["challenge_1"]["deterministic_sweep"]
    assert sweep["5.0"]["rank1_crowding_pct"] == 0.0
    assert sweep["5.5"]["rank1_crowding_pct"] == 15.0
    assert sweep["6.0"]["rank1_crowding_pct"] == 100.0
    assert sweep["7.0"]["rank1_crowding_pct"] == 100.0
    assert sweep["8.0"]["rank1_crowding_pct"] == 100.0
    assert sweep["8.5"]["rank1_crowding_pct"] == 100.0

    multi = challenge_results["challenge_1"]["multi_seed_results"]
    for imp_str in ["6.0", "7.0", "8.0", "8.5"]:
        assert multi[imp_str]["crowd_mean"] == 100.0
        assert multi[imp_str]["top5_mean"] == 500.0


def test_normalization_a7_rescue_vs_a4_dominance(challenge_results):
    """Assert that softmax normalization boosts A7 > 0.5002, but A4 strictly dominates A7 in every matched scheme."""
    c2 = challenge_results["challenge_2"]
    max_a7 = c2["max_a7_mrr"]
    assert max_a7 > 0.5002, "Softmax normalization boosts A7 above 0.5002"
    assert round(max_a7, 4) == 0.6705

    # But within every matched scheme, A4 outperforms A7
    assert c2["a4_minmax"]["mrr_mean"] > c2["a7_minmax"]["mrr_mean"]
    assert c2["a4_zscore"]["mrr_mean"] > c2["a7_zscore"]["mrr_mean"]
    assert c2["a4_quantile"]["mrr_mean"] > c2["a7_quantile"]["mrr_mean"]
    assert c2["a4_raw"]["mrr_mean"] > c2["a7_raw"]["mrr_mean"]

    for tau_str, pair in c2["softmax_results"].items():
        assert pair["a4"]["mrr_mean"] > pair["a7"]["mrr_mean"]

    for tau_str, pair in c2["softmax_minmax_results"].items():
        assert pair["a4"]["mrr_mean"] > pair["a7"]["mrr_mean"]


def test_simplex_true_global_optimum(challenge_results):
    """Assert that true global optimum is at (alpha=0.06, beta=0.94, gamma=0.0) -> MRR=0.7535, falsifying 0.6036."""
    c3 = challenge_results["challenge_3"]
    best = c3["best_overall"]
    assert round(best["alpha"], 2) == 0.06
    assert round(best["beta"], 2) == 0.94
    assert round(best["gamma"], 2) == 0.00
    assert round(best["mrr"], 4) == 0.7535


def test_simplex_interior_points_beating_a4(challenge_results):
    """Assert that exactly 390 interior points (gamma > 0) beat A4 MRR of 0.5002."""
    c3 = challenge_results["challenge_3"]
    assert c3["interior_points_gt_a4_count"] == 390
    best_int = c3["best_interior"]
    assert round(best_int["alpha"], 2) == 0.07
    assert round(best_int["beta"], 2) == 0.92
    assert round(best_int["gamma"], 2) == 0.01
    assert round(best_int["mrr"], 4) == 0.7449
