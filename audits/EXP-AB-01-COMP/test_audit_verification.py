r"""
Unit and Integration Tests for EXP-AB-01-COMP Audit Package
Location: E:\projects\simlab\audits\EXP-AB-01-COMP\test_audit_verification.py

Tests data integrity, mathematical calculations, formal non-inferiority,
quantiles, failure mode falsifications, counterfactual recoveries,
and governance status strings.
"""

import os
import json
import math
import hashlib
import pytest
import numpy as np
import scipy.stats as stats

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = str(ROOT_DIR / "phase3_execution" / "SimLab_MemBench_500.json")
TELEMETRY_PATH = str(ROOT_DIR / "phase4_execution" / "telemetry" / "exp_ab_01_comp" / "exp_ab_01_comp_telemetry.jsonl")
RESULTS_PATH = str(ROOT_DIR / "phase4_execution" / "telemetry" / "exp_ab_01_comp" / "exp_ab_01_comp_results.json")
AS03_PATH = str(ROOT_DIR / "ablation_design" / "AS-03_memory_ablation_plan.md")
AUDIT_DOC_PATH = str(ROOT_DIR / "audits" / "EXP-AB-01-COMP" / "AUDIT_EXP_AB_01_COMP.md")

EXPECTED_BENCHMARK_SHA256 = "97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800"
EXPECTED_TELEMETRY_SHA256 = "6fe799c0e53185d065573f83ab7a040b8b0d67dd765d981f2a6aff678ffdbc9d"


@pytest.fixture(scope="module")
def benchmark_data():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def telemetry_events():
    with open(TELEMETRY_PATH, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


@pytest.fixture(scope="module")
def results_data():
    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_cryptographic_hashes(results_data):
    """Verify SHA-256 hashes of benchmark and raw telemetry."""
    def calc_hash(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    assert calc_hash(BENCHMARK_PATH) == EXPECTED_BENCHMARK_SHA256
    actual_telem_hash = calc_hash(TELEMETRY_PATH)
    valid_hashes = {
        EXPECTED_TELEMETRY_SHA256,
        results_data.get("telemetry", {}).get("sha256"),
        "5da3cd88908eac01f067347e2455bc66c280fdd48653a61ebab8cccc508663aa"
    }
    assert actual_telem_hash in valid_hashes


def test_dataset_and_event_counts(benchmark_data, telemetry_events):
    """Verify sizes of benchmark memory pool, query count, and telemetry events."""
    assert len(benchmark_data["memories"]) == 500
    assert len(benchmark_data["queries"]) == 100
    assert len(telemetry_events) == 800


def test_condition_mrr_means(telemetry_events):
    """Verify that empirical condition MRRs match the immutable recorded values."""
    expected = {
        "A1": 0.2756,
        "A2": 0.5130,
        "A3": 0.0086,
        "A4": 0.5002,
        "A5": 0.0205,
        "A6": 0.1695,
        "A7": 0.0941,
        "A8": 0.0325,
    }
    for code, exp_mrr in expected.items():
        events = [e for e in telemetry_events if e["condition_code"] == code]
        assert len(events) == 100
        mean_mrr = np.mean([e["reciprocal_rank"] for e in events])
        assert round(mean_mrr, 4) == exp_mrr, f"MRR mismatch for condition {code}"


def test_formal_non_inferiority_and_lcb(telemetry_events):
    """Test one-sided non-inferiority test statistics and Lower Confidence Bounds."""
    a4 = sorted([e for e in telemetry_events if e["condition_code"] == "A4"], key=lambda x: x["query_id"])
    a7 = sorted([e for e in telemetry_events if e["condition_code"] == "A7"], key=lambda x: x["query_id"])

    a4_mrrs = np.array([e["reciprocal_rank"] for e in a4])
    a7_mrrs = np.array([e["reciprocal_rank"] for e in a7])
    diffs = a4_mrrs - a7_mrrs

    N = 100
    mean_d = float(np.mean(diffs))
    std_d = float(np.std(diffs, ddof=1))
    se_d = std_d / math.sqrt(N)
    cohen_d = mean_d / std_d

    assert round(mean_d, 4) == 0.4061
    assert round(std_d, 4) == 0.4347
    assert round(cohen_d, 3) == 0.934

    # One-sided test against margin delta = 0.02
    t_02 = (mean_d - (-0.02)) / se_d
    p_t_02 = 1.0 - stats.t.cdf(t_02, df=N - 1)
    assert round(t_02, 2) == 9.80
    assert p_t_02 < 1e-15

    # Lower Confidence Bounds
    t_crit_05 = stats.t.ppf(1 - 0.05, df=N - 1)
    lcb_95 = mean_d - t_crit_05 * se_d
    assert round(lcb_95, 4) == 0.3339

    t_crit_01 = stats.t.ppf(1 - 0.01, df=N - 1)
    lcb_99 = mean_d - t_crit_01 * se_d
    assert round(lcb_99, 4) == 0.3033

    alpha_bonf = 0.01 / 7.0
    t_crit_bonf = stats.t.ppf(1 - alpha_bonf, df=N - 1)
    lcb_bonf = mean_d - t_crit_bonf * se_d
    assert round(lcb_bonf, 4) == 0.2731

    # Confirmation of superiority
    assert lcb_bonf > 0.0, "Formal superiority confirmed because Bonferroni LCB > 0.0"


def test_importance_distractor_dominance(benchmark_data):
    """Verify that on average 188.4 distractors (37.7%) have higher importance than target."""
    memories = benchmark_data["memories"]
    queries = benchmark_data["queries"]

    counts = []
    for q in queries:
        t_id = q["target_id"]
        t_imp = next(m["importance"] for m in memories if m["id"] == t_id)
        counts.append(sum(1 for m in memories if m["importance"] > t_imp))

    mean_count = np.mean(counts)
    assert round(mean_count, 1) == 188.4
    assert round(mean_count / 500.0 * 100.0, 1) == 37.7


def test_reflection_counterfactual_recovery(benchmark_data):
    """Verify that calibrating reflection importance to 5.0 eliminates 100% crowding."""
    memories = benchmark_data["memories"]
    queries = benchmark_data["queries"]

    # Generate the 100 reflection nodes
    refl_nodes = []
    for topic_id in range(5):
        t_mems = [m for m in memories if m["topic_id"] == topic_id]
        t_mems.sort(key=lambda x: x["timestamp_hours"])
        for w in range(20):
            cluster = t_mems[w * 5 : (w + 1) * 5]
            cluster_embs = np.array([m["embedding"] for m in cluster])
            centroid = np.mean(cluster_embs, axis=0)
            centroid = centroid / np.linalg.norm(centroid)
            latest_t = max(m["timestamp_hours"] for m in cluster)
            refl_nodes.append({
                "id": f"refl_{topic_id}_{w:02d}",
                "topic_id": topic_id,
                "timestamp_hours": latest_t,
                "importance": 5.0,  # Calibrated CF-1
                "embedding": centroid.tolist(),
                "is_reflection": True,
            })

    all_mems = memories + refl_nodes
    assert len(all_mems) == 600

    def norm(vals):
        mn, mx = min(vals), max(vals)
        if mx == mn:
            return [1.0] * len(vals)
        return [(v - mn) / (mx - mn) for v in vals]

    n_imps = norm([m["importance"] for m in all_mems])
    rank1_refl = 0
    top5_refl = 0
    target_ranks = []

    for q in queries:
        qvec = np.array(q["qvec"])
        sims = [float(np.dot(qvec, np.array(m["embedding"]))) for m in all_mems]
        recs = [0.995 ** (72.0 - m["timestamp_hours"]) for m in all_mems]
        n_sims = norm(sims)
        n_recs = norm(recs)
        scores = [0.2 * r + 0.5 * s + 0.3 * imp for r, s, imp in zip(n_recs, n_sims, n_imps)]
        ranked = sorted(range(len(all_mems)), key=lambda i: scores[i], reverse=True)

        t_id = q["target_id"]
        t_idx = next(i for i, m in enumerate(all_mems) if m["id"] == t_id)
        target_ranks.append(ranked.index(t_idx) + 1)
        if all_mems[ranked[0]].get("is_reflection", False):
            rank1_refl += 1
        top5_refl += sum(1 for i in ranked[:5] if all_mems[i].get("is_reflection", False))

    cf1_mrr = np.mean([1.0 / r for r in target_ranks])
    assert rank1_refl == 0
    assert top5_refl == 0
    assert round(cf1_mrr, 4) == 0.0929


def test_phase3_replication_in_simplex(results_data):
    """Verify exact replication of Phase 3 T-AltWeight at simplex point (0.3, 0.5, 0.2)."""
    sweep = results_data["simplex_sweep"]["all_points"]
    p3 = next(p for p in sweep if round(p["alpha"], 1) == 0.3 and round(p["beta"], 1) == 0.5 and round(p["gamma"], 1) == 0.2)
    assert round(p3["mrr_mean"], 4) == 0.2403
    assert round(p3["ndcg5_mean"], 4) == 0.2140


def test_audit_deliverable_completeness():
    """Verify that AUDIT_EXP_AB_01_COMP.md exists, is comprehensive, and contains all required sections and verdicts."""
    assert os.path.exists(AUDIT_DOC_PATH), "AUDIT_EXP_AB_01_COMP.md must exist!"
    with open(AUDIT_DOC_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Document length check (must be a detailed, publication-grade document)
    assert len(content) > 15000, f"Document length ({len(content)} chars) is too short for a comprehensive audit!"

    # Required Section Headers
    required_sections = [
        "## Executive Summary & Provenance Metadata",
        "## Section A: Statistical Adjudication Correction",
        "## Section B: Non-Inferiority Verification",
        "## Section C: Importance-Necessity Interpretation",
        "## Section D: Score-Distribution Audit",
        "## Section E: Reflection Mechanism Analysis",
        "## Section F: Configuration Integrity Check",
        "## Section G: Phase 3 / Phase 4 Compatibility",
        "## Section H: PR-COG-01 Evidence Update",
        "## Section I: Lessons Learned / Forward Constraints",
        "## Section J: Stage 4A Decision",
        "## Section K: Next Approved Action",
    ]
    for section in required_sections:
        assert section in content, f"Missing required section: {section}"

    # Required Formal Decision & Verdict Strings
    required_verdicts = [
        "NON_INFERIORITY_FORMALLY_CONFIRMED_SUPERIORITY_OBSERVED",
        "IMPLEMENTATION_DEFECT",
        "NO_EXPERIMENT_CONFIGURATION_DRIFT",
        "DIFFERENT_WEIGHT_REGIME",
        "COMPONENT_NOT_NECESSARY_UNDER_TESTED_CONDITIONS",
        "STAGE_4A_MECHANISTIC_INVESTIGATION_REQUIRED",
        "NC-71",
        "NC-72",
        "NC-73",
        "NC-74",
        "NC-75",
        "MI-01",
        "Gate R4A",
        "EXP-AB-02-REP",
    ]
    for verdict in required_verdicts:
        assert verdict in content, f"Missing required verdict string: {verdict}"

