r"""
Empirical Adversarial Challenge Test Suite for EXP-AB-01-COMP Master Audit
Location: E:\projects\simlab\audits\EXP-AB-01-COMP\test_audit_challenger.py
Author: audit_challenger_1 (Empirical Challenger Agent)

This test suite executes rigorous empirical stress tests on the statistical claims
and non-inferiority adjudication in AUDIT_EXP_AB_01_COMP.md:
1. Sub-population analysis (RECENCY_SENSITIVE, RELEVANCE_DOMINANT, TEMPORAL_CONFLICT)
2. Adversarial bootstrap resampling (10,000 iterations) and permutation testing
3. Outlier sensitivity and robust location estimation (trimmed means, winsorized means, jackknife, top-k deletion)
"""

import json
import math
import numpy as np
import pytest
import scipy.stats as stats
from scipy.stats import mstats

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = str(ROOT_DIR / "phase3_execution" / "SimLab_MemBench_500.json")
TELEMETRY_PATH = str(ROOT_DIR / "phase4_execution" / "telemetry" / "exp_ab_01_comp" / "exp_ab_01_comp_telemetry.jsonl")


@pytest.fixture(scope="module")
def benchmark_data():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def telemetry_events():
    with open(TELEMETRY_PATH, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


@pytest.fixture(scope="module")
def parsed_data(benchmark_data, telemetry_events):
    queries = benchmark_data["queries"]
    q_type = {q["query_id"]: q["type"] for q in queries}
    
    by_cond = {}
    for e in telemetry_events:
        c = e["condition_code"]
        if c not in by_cond:
            by_cond[c] = {}
        by_cond[c][e["query_id"]] = e
        
    return {
        "queries": queries,
        "q_type": q_type,
        "by_cond": by_cond,
    }


# ==============================================================================
# 1. SUB-POPULATION EMPIRICAL ANALYSIS
# ==============================================================================

def test_subcohort_recency_sensitive(parsed_data):
    """Test A4 vs A7 on RECENCY_SENSITIVE sub-cohort (N=40)."""
    queries = [q for q in parsed_data["queries"] if q["type"] == "RECENCY_SENSITIVE"]
    assert len(queries) == 40
    
    a4 = np.array([parsed_data["by_cond"]["A4"][q["query_id"]]["reciprocal_rank"] for q in queries])
    a7 = np.array([parsed_data["by_cond"]["A7"][q["query_id"]]["reciprocal_rank"] for q in queries])
    diffs = a4 - a7
    
    mean_a4 = float(np.mean(a4))
    mean_a7 = float(np.mean(a7))
    mean_diff = float(np.mean(diffs))
    std_diff = float(np.std(diffs, ddof=1))
    se_diff = std_diff / np.sqrt(len(diffs))
    cohen_d = mean_diff / std_diff
    
    t_stat, p_val = stats.ttest_rel(a4, a7)
    
    assert round(mean_a4, 4) == 0.7229
    assert round(mean_a7, 4) == 0.0904
    assert round(mean_diff, 4) == 0.6325
    assert round(cohen_d, 4) == 1.8550
    assert p_val < 1e-13
    assert np.all(diffs > 0), "A4 must win 100% of RECENCY_SENSITIVE queries (40/40)"


def test_subcohort_temporal_conflict(parsed_data):
    """Test A4 vs A7 on TEMPORAL_CONFLICT sub-cohort (N=20)."""
    queries = [q for q in parsed_data["queries"] if q["type"] == "TEMPORAL_CONFLICT"]
    assert len(queries) == 20
    
    a4 = np.array([parsed_data["by_cond"]["A4"][q["query_id"]]["reciprocal_rank"] for q in queries])
    a7 = np.array([parsed_data["by_cond"]["A7"][q["query_id"]]["reciprocal_rank"] for q in queries])
    diffs = a4 - a7
    
    mean_a4 = float(np.mean(a4))
    mean_a7 = float(np.mean(a7))
    mean_diff = float(np.mean(diffs))
    std_diff = float(np.std(diffs, ddof=1))
    cohen_d = mean_diff / std_diff
    
    t_stat, p_val = stats.ttest_rel(a4, a7)
    
    assert round(mean_a4, 4) == 1.0000
    assert round(mean_a7, 4) == 0.1549
    assert round(mean_diff, 4) == 0.8451
    assert round(cohen_d, 4) == 6.9672
    assert p_val < 1e-17
    assert np.all(diffs > 0), "A4 must win 100% of TEMPORAL_CONFLICT queries (20/20)"


def test_subcohort_relevance_dominant_subpopulation_reversal(parsed_data):
    """
    CRITICAL CHALLENGE TEST: Test A4 vs A7 on RELEVANCE_DOMINANT sub-cohort (N=40).
    Demonstrates that A4 does NOT outperform A7 in every sub-cohort!
    In RELEVANCE_DOMINANT, A4 is significantly INFERIOR to A7.
    """
    queries = [q for q in parsed_data["queries"] if q["type"] == "RELEVANCE_DOMINANT"]
    assert len(queries) == 40
    
    a4 = np.array([parsed_data["by_cond"]["A4"][q["query_id"]]["reciprocal_rank"] for q in queries])
    a7 = np.array([parsed_data["by_cond"]["A7"][q["query_id"]]["reciprocal_rank"] for q in queries])
    diffs = a4 - a7
    
    mean_a4 = float(np.mean(a4))
    mean_a7 = float(np.mean(a7))
    mean_diff = float(np.mean(diffs))
    std_diff = float(np.std(diffs, ddof=1))
    se_diff = std_diff / np.sqrt(len(diffs))
    cohen_d = mean_diff / std_diff
    
    t_stat, p_val = stats.ttest_rel(a4, a7)
    
    # Assert exact empirical values showing A4 < A7
    assert round(mean_a4, 4) == 0.0277
    assert round(mean_a7, 4) == 0.0675
    assert round(mean_diff, 4) == -0.0398
    assert round(cohen_d, 4) == -1.3285
    assert t_stat < -8.0
    assert p_val < 1e-9
    
    # Non-inferiority test of A4 vs A7 (margin delta = 0.02)
    # H0: mean_diff <= -0.02 vs H1: mean_diff > -0.02
    t_ni = (mean_diff - (-0.02)) / se_diff
    p_ni = 1.0 - stats.t.cdf(t_ni, df=len(diffs)-1)
    assert p_ni > 0.999, "A4 non-inferiority to A7 must be decisively rejected for RELEVANCE_DOMINANT"
    
    # Wins vs Losses: A7 wins 32/40 (80%), A4 wins only 8/40 (20%)
    wins_a4 = int(np.sum(diffs > 0))
    losses_a4 = int(np.sum(diffs < 0))
    assert wins_a4 == 8
    assert losses_a4 == 32


# ==============================================================================
# 2. ADVERSARIAL BOOTSTRAP & PERMUTATION TESTS
# ==============================================================================

def test_adversarial_bootstrap_10000_resamples(parsed_data):
    """
    Run 10,000 bootstrap resamples of paired differences between A4 and A7.
    Assert that the empirical 99.857% Lower Confidence Bound is strictly greater than 0.0.
    """
    qids = [q["query_id"] for q in parsed_data["queries"]]
    a4 = np.array([parsed_data["by_cond"]["A4"][qid]["reciprocal_rank"] for qid in qids])
    a7 = np.array([parsed_data["by_cond"]["A7"][qid]["reciprocal_rank"] for qid in qids])
    diffs = a4 - a7
    n = len(diffs)
    
    np.random.seed(42)
    B = 10000
    boot_indices = np.random.randint(0, n, size=(B, n))
    boot_diffs = diffs[boot_indices]
    boot_means = np.mean(boot_diffs, axis=1)
    
    # Alpha Bonferroni = 0.01 / 7 = 0.00142857 -> 0.142857% percentile
    alpha_bonf = 0.01 / 7.0
    pct_bonf = alpha_bonf * 100.0
    
    lcb_95_boot = float(np.percentile(boot_means, 5.0))
    lcb_99_boot = float(np.percentile(boot_means, 1.0))
    lcb_bonf_boot = float(np.percentile(boot_means, pct_bonf))
    min_boot_mean = float(np.min(boot_means))
    
    assert lcb_bonf_boot > 0.27, f"Bootstrap Bonferroni LCB ({lcb_bonf_boot:.4f}) must exceed 0.27"
    assert min_boot_mean > 0.25, f"Minimum bootstrap mean ({min_boot_mean:.4f}) must exceed 0.25"
    assert np.sum(boot_means <= 0.0) == 0, "Zero bootstrap resamples may be <= 0.0"
    assert np.sum(boot_means <= -0.02) == 0, "Zero bootstrap resamples may be <= -0.02"


def test_permutation_test_paired_exchangeability(parsed_data):
    """
    Execute 50,000 Monte Carlo sign-flip permutations under H0: exchangeability of A4 and A7.
    Assert that empirical p-value is < 1e-4.
    """
    qids = [q["query_id"] for q in parsed_data["queries"]]
    a4 = np.array([parsed_data["by_cond"]["A4"][qid]["reciprocal_rank"] for qid in qids])
    a7 = np.array([parsed_data["by_cond"]["A7"][qid]["reciprocal_rank"] for qid in qids])
    diffs = a4 - a7
    observed_mean = np.mean(diffs)
    
    np.random.seed(42)
    P = 50000
    signs = np.random.choice([-1, 1], size=(P, len(diffs)))
    perm_means = np.mean(diffs * signs, axis=1)
    p_perm = np.mean(perm_means >= observed_mean)
    
    assert p_perm == 0.0, f"Observed mean ({observed_mean:.4f}) is never exceeded under null permutation"
    assert np.max(perm_means) < 0.25, "Maximum null permuted mean must be far below observed delta"


# ==============================================================================
# 3. OUTLIER SENSITIVITY & ROBUST LOCATION ESTIMATION
# ==============================================================================

def test_outlier_robust_location_estimates(parsed_data):
    """
    Verify robust estimators of paired difference (trimmed, winsorized, median).
    Ensures that A4's advantage is not driven by a few massive outliers.
    """
    qids = [q["query_id"] for q in parsed_data["queries"]]
    a4 = np.array([parsed_data["by_cond"]["A4"][qid]["reciprocal_rank"] for qid in qids])
    a7 = np.array([parsed_data["by_cond"]["A7"][qid]["reciprocal_rank"] for qid in qids])
    diffs = a4 - a7
    
    trim_05 = stats.trim_mean(diffs, 0.05)
    trim_10 = stats.trim_mean(diffs, 0.10)
    trim_20 = stats.trim_mean(diffs, 0.20)
    iq_mean = stats.trim_mean(diffs, 0.25)
    median_val = float(np.median(diffs))
    
    assert round(trim_05, 4) == 0.4012
    assert round(trim_10, 4) == 0.3943
    assert round(trim_20, 4) == 0.3751
    assert round(iq_mean, 4) == 0.3610
    assert round(median_val, 4) == 0.3036
    
    # Even the interquartile mean (50% of data trimmed) exceeds +0.36
    assert iq_mean > 0.35


def test_jackknife_leave_one_out_influence(parsed_data):
    """Verify that no single query exerts undue influence on the mean difference."""
    qids = [q["query_id"] for q in parsed_data["queries"]]
    a4 = np.array([parsed_data["by_cond"]["A4"][qid]["reciprocal_rank"] for qid in qids])
    a7 = np.array([parsed_data["by_cond"]["A7"][qid]["reciprocal_rank"] for qid in qids])
    diffs = a4 - a7
    n = len(diffs)
    
    jack_means = [np.mean(np.delete(diffs, i)) for i in range(n)]
    min_jack = float(np.min(jack_means))
    max_jack = float(np.max(jack_means))
    swing = max_jack - min_jack
    
    assert min_jack > 0.4000
    assert max_jack < 0.4120
    assert swing < 0.0120, "Maximum leave-one-out influence must be under 0.012 MRR"


def test_adversarial_sequential_top_win_deletion(parsed_data):
    """
    Stress-test: sequentially drop the top-k largest A4 wins.
    Assert that even after dropping 30 top wins (nearly half of all A4 wins),
    the Bonferroni Lower Confidence Bound remains strictly positive (> 0.0).
    """
    qids = [q["query_id"] for q in parsed_data["queries"]]
    a4 = np.array([parsed_data["by_cond"]["A4"][qid]["reciprocal_rank"] for qid in qids])
    a7 = np.array([parsed_data["by_cond"]["A7"][qid]["reciprocal_rank"] for qid in qids])
    diffs = a4 - a7
    
    sorted_diffs = np.sort(diffs)
    
    # Drop top 10 wins (N=90 remaining)
    sub_10 = sorted_diffs[:-10]
    mean_10 = np.mean(sub_10)
    se_10 = np.std(sub_10, ddof=1) / np.sqrt(len(sub_10))
    lcb_bonf_10 = mean_10 - stats.t.ppf(1 - 0.01/7.0, df=len(sub_10)-1) * se_10
    assert round(mean_10, 4) == 0.3423
    assert lcb_bonf_10 > 0.20
    
    # Drop top 30 wins (N=70 remaining)
    sub_30 = sorted_diffs[:-30]
    mean_30 = np.mean(sub_30)
    se_30 = np.std(sub_30, ddof=1) / np.sqrt(len(sub_30))
    lcb_bonf_30 = mean_30 - stats.t.ppf(1 - 0.01/7.0, df=len(sub_30)-1) * se_30
    assert round(mean_30, 4) == 0.1743
    assert lcb_bonf_30 > 0.06
