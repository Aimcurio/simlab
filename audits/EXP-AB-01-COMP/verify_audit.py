r"""
EXP-AB-01-COMP Master Audit Verification Script
Location: E:\projects\simlab\audits\EXP-AB-01-COMP\verify_audit.py
"""

import os
import sys
import json
import math
import hashlib
from pathlib import Path
import numpy as np
import scipy.stats as stats

REPO_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = REPO_ROOT / "phase3_execution" / "SimLab_MemBench_500.json"
TELEMETRY_PATH = REPO_ROOT / "phase4_execution" / "telemetry" / "exp_ab_01_comp" / "exp_ab_01_comp_telemetry.jsonl"
RESULTS_PATH = REPO_ROOT / "phase4_execution" / "telemetry" / "exp_ab_01_comp" / "exp_ab_01_comp_results.json"
AS03_PATH = REPO_ROOT / "ablation_design" / "AS-03_memory_ablation_plan.md"

EXPECTED_BENCHMARK_SHA256 = "97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800"
EXPECTED_TELEMETRY_SHA256 = "6fe799c0e53185d065573f83ab7a040b8b0d67dd765d981f2a6aff678ffdbc9d"


def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def min_max_norm(vals):
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return [1.0] * len(vals)
    return [(v - mn) / (mx - mn) for v in vals]


def run_full_verification():
    print("=" * 80)
    print("CURO SIMLAB EXP-AB-01-COMP: MASTER AUDIT VERIFICATION HARNESS")
    print("=" * 80)

    # 1. Cryptographic Hash Verification
    print("\n[STEP 1] Verifying Cryptographic Hashes & Telemetry Immutability...")
    bench_hash = sha256_file(BENCHMARK_PATH)
    telem_hash = sha256_file(TELEMETRY_PATH)
    print(f"  Benchmark SHA-256: {bench_hash} (Match: {bench_hash == EXPECTED_BENCHMARK_SHA256})")
    print(f"  Telemetry SHA-256: {telem_hash} (Match: {telem_hash == EXPECTED_TELEMETRY_SHA256})")
    assert bench_hash == EXPECTED_BENCHMARK_SHA256, "Benchmark SHA-256 mismatch!"
    assert telem_hash == EXPECTED_TELEMETRY_SHA256, "Telemetry SHA-256 mismatch!"

    # Load Data
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        bench = json.load(f)
    memories = bench["memories"]
    queries = bench["queries"]

    with open(TELEMETRY_PATH, "r", encoding="utf-8") as f:
        events = [json.loads(line) for line in f]

    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        results = json.load(f)

    assert len(memories) == 500
    assert len(queries) == 100
    assert len(events) == 800
    print(f"  Loaded 500 memories, 100 queries, and 800 telemetry events cleanly.")

    # 2. Condition MRR Summaries Verification
    print("\n[STEP 2] Verifying Condition MRRs...")
    condition_mrrs = {}
    expected_means = {
        "A1": 0.2756,
        "A2": 0.5130,
        "A3": 0.0086,
        "A4": 0.5002,
        "A5": 0.0205,
        "A6": 0.1695,
        "A7": 0.0941,
        "A8": 0.0325,
    }
    for c in ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"]:
        c_events = [e for e in events if e["condition_code"] == c]
        c_events.sort(key=lambda x: x["query_id"])
        mrrs = [e["reciprocal_rank"] for e in c_events]
        mrr_mean = float(np.mean(mrrs))
        condition_mrrs[c] = (mrrs, mrr_mean)
        print(f"  Condition {c}: Mean MRR = {mrr_mean:.4f} (Expected: {expected_means[c]:.4f})")
        assert round(mrr_mean, 4) == expected_means[c], f"MRR mean mismatch for {c}"

    # 3. Non-Inferiority Verification & Formal Hypothesis Testing
    print("\n[STEP 3] Verifying Formal Non-Inferiority & Lower Confidence Bounds (A4 vs A7)...")
    a4_mrrs = np.array(condition_mrrs["A4"][0])
    a7_mrrs = np.array(condition_mrrs["A7"][0])
    diffs = a4_mrrs - a7_mrrs

    N = len(diffs)
    mean_diff = float(np.mean(diffs))
    std_diff = float(np.std(diffs, ddof=1))
    se_diff = std_diff / math.sqrt(N)
    cohen_d = mean_diff / std_diff

    # Non-inferiority against margin delta = 0.02
    margin_02 = 0.02
    t_stat_02 = (mean_diff - (-margin_02)) / se_diff
    p_val_t_02 = 1.0 - stats.t.cdf(t_stat_02, df=N - 1)

    # Shifted Wilcoxon against -0.02
    shifted_diffs_02 = diffs - (-margin_02)
    nonzero_02 = shifted_diffs_02[shifted_diffs_02 != 0]
    w_stat_02, p_val_w_02 = stats.wilcoxon(nonzero_02, alternative="greater")

    # Non-inferiority against margin delta = 0.05
    margin_05 = 0.05
    t_stat_05 = (mean_diff - (-margin_05)) / se_diff
    p_val_t_05 = 1.0 - stats.t.cdf(t_stat_05, df=N - 1)

    # Shifted Wilcoxon against -0.05
    shifted_diffs_05 = diffs - (-margin_05)
    nonzero_05 = shifted_diffs_05[shifted_diffs_05 != 0]
    w_stat_05, p_val_w_05 = stats.wilcoxon(nonzero_05, alternative="greater")

    # Lower Confidence Bounds
    t_crit_05 = stats.t.ppf(1 - 0.05, df=N - 1)
    lcb_95 = mean_diff - t_crit_05 * se_diff

    t_crit_01 = stats.t.ppf(1 - 0.01, df=N - 1)
    lcb_99 = mean_diff - t_crit_01 * se_diff

    alpha_bonf = 0.01 / 7.0
    t_crit_bonf = stats.t.ppf(1 - alpha_bonf, df=N - 1)
    lcb_bonf = mean_diff - t_crit_bonf * se_diff

    print(f"  Paired Mean Difference (A4 - A7): +{mean_diff:.6f}")
    print(f"  Paired Std Dev:                   {std_diff:.6f}")
    print(f"  Standard Error (SE):              {se_diff:.6f}")
    print(f"  Cohen's d:                        +{cohen_d:.4f}")
    print(f"  [Margin delta=0.02] t = {t_stat_02:.4f}, p = {p_val_t_02:.4e}; Wilcoxon W = {w_stat_02:.1f}, p = {p_val_w_02:.4e}")
    print(f"  [Margin delta=0.05] t = {t_stat_05:.4f}, p = {p_val_t_05:.4e}; Wilcoxon W = {w_stat_05:.1f}, p = {p_val_w_05:.4e}")
    print(f"  95% One-Sided LCB (alpha=0.05):    +{lcb_95:.6f}")
    print(f"  99% One-Sided LCB (alpha=0.01):    +{lcb_99:.6f}")
    print(f"  Bonferroni LCB (alpha=0.001429):   +{lcb_bonf:.6f}")

    assert round(mean_diff, 4) == 0.4061
    assert round(std_diff, 4) == 0.4347
    assert round(cohen_d, 3) == 0.934
    assert round(t_stat_02, 2) == 9.80
    assert round(t_stat_05, 2) == 10.49
    assert round(lcb_95, 4) == 0.3339
    assert round(lcb_99, 4) == 0.3033
    assert round(lcb_bonf, 4) == 0.2731
    assert lcb_bonf > 0.0, "Superiority confirmed because Bonferroni LCB > 0.0!"

    # 4. Component Score Distribution & Distractor Importance Dominance
    print("\n[STEP 4] Verifying Score Distributions & Distractor Importance Bias...")
    imps = np.array([m["importance"] for m in memories])
    times = np.array([m["timestamp_hours"] for m in memories])
    recs = 0.995 ** (72.0 - times)

    print(f"  Raw Importance: min={imps.min():.4f}, max={imps.max():.4f}, mean={imps.mean():.4f}, std={imps.std():.4f}")
    print(f"  Raw Recency:    min={recs.min():.4f}, max={recs.max():.4f}, mean={recs.mean():.4f}, std={recs.std():.4f}")

    target_imps = []
    distractors_higher = []
    m_embs = np.array([m["embedding"] for m in memories])

    target_sims = []
    distractor_sims = []
    all_target_indicators = []
    all_importance_scores = []

    for q in queries:
        t_id = q["target_id"]
        t_imp = next(m["importance"] for m in memories if m["id"] == t_id)
        target_imps.append(t_imp)
        higher_count = sum(1 for m in memories if m["importance"] > t_imp)
        distractors_higher.append(higher_count)

        qvec = np.array(q["qvec"])
        sims = np.dot(m_embs, qvec)
        for idx, m in enumerate(memories):
            all_importance_scores.append(m["importance"])
            if m["id"] == t_id:
                target_sims.append(sims[idx])
                all_target_indicators.append(1)
            else:
                distractor_sims.append(sims[idx])
                all_target_indicators.append(0)

    mean_distractors_higher = float(np.mean(distractors_higher))
    pct_distractors_higher = (mean_distractors_higher / 500.0) * 100.0
    print(f"  Mean distractors with higher importance than target: {mean_distractors_higher:.1f} ({pct_distractors_higher:.1f}%)")
    assert round(mean_distractors_higher, 1) == 188.4
    assert round(pct_distractors_higher, 1) == 37.7

    # Point-biserial correlation between static importance and target indicator
    r_imp, p_imp = stats.pointbiserialr(all_target_indicators, all_importance_scores)
    r2_imp = r_imp ** 2
    print(f"  Pearson r(importance, target indicator): +{r_imp:.4f} (p = {p_imp:.4e}, R^2 = {r2_imp:.5f})")
    assert round(r_imp, 4) == 0.0182

    # 5. Reflection Failure Analysis & Counterfactuals
    print("\n[STEP 5] Verifying Reflection Mechanics & Counterfactual Experiments...")
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
                "importance": 8.5,
                "embedding": centroid.tolist(),
                "is_reflection": True,
            })

    all_mems_a8 = memories + refl_nodes
    assert len(all_mems_a8) == 600

    # Test baseline A8 crowding
    norm_imps_a8 = min_max_norm([m["importance"] for m in all_mems_a8])
    a8_target_ranks = []
    a8_rank1_refl = 0
    a8_top5_refl_slots = 0

    for q in queries:
        qvec = np.array(q["qvec"])
        sims = [float(np.dot(qvec, np.array(m["embedding"]))) for m in all_mems_a8]
        recs = [0.995 ** (72.0 - m["timestamp_hours"]) for m in all_mems_a8]
        n_sims = min_max_norm(sims)
        n_recs = min_max_norm(recs)
        scores = [0.2 * r + 0.5 * s + 0.3 * imp for r, s, imp in zip(n_recs, n_sims, norm_imps_a8)]
        ranked_indices = sorted(range(len(all_mems_a8)), key=lambda i: scores[i], reverse=True)

        t_id = q["target_id"]
        t_cand_idx = next(i for i, m in enumerate(all_mems_a8) if m["id"] == t_id)
        a8_target_ranks.append(ranked_indices.index(t_cand_idx) + 1)
        if all_mems_a8[ranked_indices[0]].get("is_reflection", False):
            a8_rank1_refl += 1
        a8_top5_refl_slots += sum(1 for i in ranked_indices[:5] if all_mems_a8[i].get("is_reflection", False))

    print(f"  Observed A8: Rank-1 Crowding = {a8_rank1_refl}/100 ({a8_rank1_refl}%), Top-5 Slots = {a8_top5_refl_slots}/500 ({a8_top5_refl_slots/5:.1f}%)")
    assert a8_rank1_refl == 100
    assert a8_top5_refl_slots == 500

    # Counterfactual 1: Reflection importance = 5.0
    all_mems_cf1 = [dict(m) for m in all_mems_a8]
    for m in all_mems_cf1:
        if m.get("is_reflection"):
            m["importance"] = 5.0
    norm_imps_cf1 = min_max_norm([m["importance"] for m in all_mems_cf1])

    cf1_target_ranks = []
    cf1_rank1_refl = 0
    cf1_top5_refl_slots = 0

    for q in queries:
        qvec = np.array(q["qvec"])
        sims = [float(np.dot(qvec, np.array(m["embedding"]))) for m in all_mems_cf1]
        recs = [0.995 ** (72.0 - m["timestamp_hours"]) for m in all_mems_cf1]
        n_sims = min_max_norm(sims)
        n_recs = min_max_norm(recs)
        scores = [0.2 * r + 0.5 * s + 0.3 * imp for r, s, imp in zip(n_recs, n_sims, norm_imps_cf1)]
        ranked_indices = sorted(range(len(all_mems_cf1)), key=lambda i: scores[i], reverse=True)

        t_id = q["target_id"]
        t_cand_idx = next(i for i, m in enumerate(all_mems_cf1) if m["id"] == t_id)
        cf1_target_ranks.append(ranked_indices.index(t_cand_idx) + 1)
        if all_mems_cf1[ranked_indices[0]].get("is_reflection", False):
            cf1_rank1_refl += 1
        cf1_top5_refl_slots += sum(1 for i in ranked_indices[:5] if all_mems_cf1[i].get("is_reflection", False))

    cf1_mrr = float(np.mean([1.0 / r for r in cf1_target_ranks]))
    print(f"  CF-1 (imp=5.0): MRR = {cf1_mrr:.4f}, Rank-1 Crowding = {cf1_rank1_refl}/100 (0%), Top-5 Slots = {cf1_top5_refl_slots}/500 (0%)")
    assert cf1_rank1_refl == 0
    assert cf1_top5_refl_slots == 0
    assert round(cf1_mrr, 4) == 0.0929

    # Counterfactual 2: No importance weighting on A8 pool (alpha=0.3, beta=0.7, gamma=0.0)
    cf2_target_ranks = []
    cf2_rank1_refl = 0
    cf2_top5_refl_slots = 0
    for q in queries:
        qvec = np.array(q["qvec"])
        sims = [float(np.dot(qvec, np.array(m["embedding"]))) for m in all_mems_a8]
        recs = [0.995 ** (72.0 - m["timestamp_hours"]) for m in all_mems_a8]
        n_sims = min_max_norm(sims)
        n_recs = min_max_norm(recs)
        scores = [0.3 * r + 0.7 * s for r, s in zip(n_recs, n_sims)]
        ranked_indices = sorted(range(len(all_mems_a8)), key=lambda i: scores[i], reverse=True)
        t_id = q["target_id"]
        t_cand_idx = next(i for i, m in enumerate(all_mems_a8) if m["id"] == t_id)
        cf2_target_ranks.append(ranked_indices.index(t_cand_idx) + 1)
        if all_mems_a8[ranked_indices[0]].get("is_reflection", False):
            cf2_rank1_refl += 1
        cf2_top5_refl_slots += sum(1 for i in ranked_indices[:5] if all_mems_a8[i].get("is_reflection", False))

    cf2_mrr = float(np.mean([1.0 / r for r in cf2_target_ranks]))
    print(f"  CF-2 (gamma=0.0): MRR = {cf2_mrr:.4f}, Rank-1 Crowding = {cf2_rank1_refl}/100 ({cf2_rank1_refl}%), Top-5 Slots = {cf2_top5_refl_slots}/500 ({cf2_top5_refl_slots/5:.1f}%)")
    assert round(cf2_mrr, 4) == 0.3536
    assert cf2_rank1_refl == 76
    assert cf2_top5_refl_slots == 208

    # Counterfactual 3: Target overlap check
    all_target_ids = set(q["target_id"] for q in queries)
    refl_ids = set(r["id"] for r in refl_nodes)
    overlap = all_target_ids.intersection(refl_ids)
    print(f"  CF-3: Target ID overlap between queries and reflection nodes: {len(overlap)} (Expected: 0)")
    assert len(overlap) == 0

    # 6. Phase 3 Replication in Simplex Sweep
    print("\n[STEP 6] Verifying Exact Phase 3 Replication in 66-point Simplex Sweep...")
    simplex_points = results["simplex_sweep"]["all_points"]
    assert len(simplex_points) == 66
    p3_point = next(p for p in simplex_points if round(p["alpha"], 1) == 0.3 and round(p["beta"], 1) == 0.5 and round(p["gamma"], 1) == 0.2)
    print(f"  Phase 3 Simplex Point (0.3, 0.5, 0.2): MRR = {p3_point['mrr_mean']:.6f}, NDCG@5 = {p3_point['ndcg5_mean']:.6f}")
    assert round(p3_point["mrr_mean"], 4) == 0.2403
    assert round(p3_point["ndcg5_mean"], 4) == 0.2140

    # Global simplex maximum:
    max_point = max(simplex_points, key=lambda p: p["mrr_mean"])
    print(f"  Global Simplex Maximum: alpha={max_point['alpha']}, beta={max_point['beta']}, gamma={max_point['gamma']} -> MRR = {max_point['mrr_mean']:.4f}")
    assert max_point["alpha"] == 0.7 and max_point["beta"] == 0.3 and max_point["gamma"] == 0.0
    # Save verified summary
    summary_out = {
        "experiment_id": "EXP-AB-01-COMP",
        "target_primitive": "PR-COG-01",
        "audit_verdict": "STAGE_4A_MECHANISTIC_INVESTIGATION_REQUIRED",
        "non_inferiority_verdict": "NON_INFERIORITY_FORMALLY_CONFIRMED_SUPERIORITY_OBSERVED",
        "configuration_integrity": "NO_EXPERIMENT_CONFIGURATION_DRIFT",
        "phase_compatibility": "DIFFERENT_WEIGHT_REGIME",
        "primitive_evidence_status": "COMPONENT_NOT_NECESSARY_UNDER_TESTED_CONDITIONS",
        "paired_difference_a4_a7": {
            "mean": mean_diff,
            "std": std_diff,
            "se": se_diff,
            "cohen_d": cohen_d,
            "lcb_95": lcb_95,
            "lcb_99": lcb_99,
            "lcb_bonferroni": lcb_bonf,
            "t_stat_02": t_stat_02,
            "p_val_t_02": p_val_t_02,
            "w_stat_02": float(w_stat_02),
            "p_val_w_02": float(p_val_w_02),
        },
        "condition_mrrs": {c: v[1] for c, v in condition_mrrs.items()},
        "reflection_counterfactuals": {
            "observed_a8_crowding_pct": 100.0,
            "cf1_imp_5_0_crowding_pct": 0.0,
            "cf1_imp_5_0_mrr": cf1_mrr,
            "cf2_gamma_0_0_mrr": cf2_mrr,
        },
        "forward_constraints": ["NC-71", "NC-72", "NC-73", "NC-74", "NC-75"],
        "next_action": "MI-01",
    }
    summary_path = os.path.join(os.path.dirname(__file__), "audit_verification_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_out, f, indent=2)
    print(f"\n  Saved audit verification summary to: {summary_path}")

    print("\n" + "=" * 80)
    print("ALL AUDIT RE-CALCULATIONS AND VERIFICATIONS PASSED 100% SUCCESSFULLY.")
    print("=" * 80)


if __name__ == "__main__":
    run_full_verification()
