r"""
Empirical Challenge Test Suite: EXP-AB-01-COMP
Author: audit_challenger_2 (Empirical Challenger)
Target Deliverable: E:\projects\simlab\audits\EXP-AB-01-COMP\AUDIT_EXP_AB_01_COMP.md

Performs empirical stress-tests:
1. Counterfactual replication of reflection node generation and score calculation across seeds & importance levels.
2. Normalization stress-testing on A7 (z-score, softmax, quantile, etc.) vs A4.
3. Simplex monotonicity check on interior (alpha+beta+gamma=1.0, gamma > 0, MRR > 0.5002).
"""

from pathlib import Path
import json
import math
import time
import numpy as np
import scipy.stats as stats
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parent
BENCHMARK_PATH = ROOT / "phase3_execution" / "SimLab_MemBench_500.json"

def load_benchmark():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        bench = json.load(f)
    return bench["memories"], bench["queries"]

def min_max_norm(vals):
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return [1.0] * len(vals)
    return [(v - mn) / (mx - mn) for v in vals]

def z_score_norm(vals):
    arr = np.array(vals, dtype=float)
    std = np.std(arr)
    if std == 0:
        return [0.0] * len(vals)
    return ((arr - np.mean(arr)) / std).tolist()

def softmax_norm(vals, temperature=1.0):
    arr = np.array(vals, dtype=float) / temperature
    arr_max = np.max(arr)
    exp_arr = np.exp(arr - arr_max)
    return (exp_arr / np.sum(exp_arr)).tolist()

def quantile_norm(vals):
    arr = np.array(vals, dtype=float)
    n = len(arr)
    if n <= 1:
        return [1.0] * n
    # Fractional rank in [0, 1] using stats.rankdata (1-based, average ties)
    ranks = stats.rankdata(arr, method="average")
    return ((ranks - 1.0) / (n - 1.0)).tolist()

def compute_ndcg5(target_rank):
    if target_rank <= 5:
        return 1.0 / math.log2(target_rank + 1)
    return 0.0

# Precompute query representations and episodic components
def prepare_precomputed_data(memories, queries, t_curr=72.0):
    c_embs = np.array([m["embedding"] for m in memories], dtype=float) # (500, D)
    raw_imps = np.array([float(m["importance"]) for m in memories], dtype=float) # (500,)
    raw_recs = np.array([0.995 ** (t_curr - float(m["timestamp_hours"])) for m in memories], dtype=float) # (500,)

    query_data = []
    for q in queries:
        qvec = np.array(q["qvec"], dtype=float)
        sims = np.dot(c_embs, qvec) # (500,)
        t_id = q["target_id"]
        t_idx = next(i for i, m in enumerate(memories) if m["id"] == t_id)
        query_data.append({
            "query_id": q["query_id"],
            "target_id": t_id,
            "target_idx": t_idx,
            "sims": sims,
            "qvec": qvec,
            "type": q["type"],
        })
    return {
        "memories": memories,
        "queries": queries,
        "raw_imps": raw_imps,
        "raw_recs": raw_recs,
        "query_data": query_data,
        "c_embs": c_embs,
    }


# ==============================================================================
# CHALLENGE 1: COUNTERFACTUAL REPLICATION & REFLECTION DYNAMICS ACROSS SEEDS
# ==============================================================================
def generate_deterministic_reflections(memories, importance=8.5):
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
            node_id = f"refl_{topic_id}_{w:02d}"
            refl_nodes.append({
                "id": node_id,
                "topic_id": topic_id,
                "timestamp_hours": latest_t,
                "importance": float(importance),
                "embedding": centroid.tolist(),
                "is_reflection": True,
            })
    return refl_nodes

def generate_random_partition_reflections(memories, importance=5.0, seed=42):
    rng = np.random.RandomState(seed)
    refl_nodes = []
    for topic_id in range(5):
        t_mems = [m for m in memories if m["topic_id"] == topic_id]
        perm = rng.permutation(len(t_mems))
        for w in range(20):
            cluster_indices = perm[w * 5 : (w + 1) * 5]
            cluster = [t_mems[i] for i in cluster_indices]
            cluster_embs = np.array([m["embedding"] for m in cluster])
            centroid = np.mean(cluster_embs, axis=0)
            centroid = centroid / np.linalg.norm(centroid)
            latest_t = max(m["timestamp_hours"] for m in cluster)
            node_id = f"refl_rand_{topic_id}_{w:02d}_s{seed}"
            refl_nodes.append({
                "id": node_id,
                "topic_id": topic_id,
                "timestamp_hours": latest_t,
                "importance": float(importance) if isinstance(importance, (int, float)) else float(rng.normal(5.0029, 0.5739)),
                "embedding": centroid.tolist(),
                "is_reflection": True,
            })
    return refl_nodes

def generate_kmeans_reflections(memories, importance=5.0, seed=42):
    refl_nodes = []
    for topic_id in range(5):
        t_mems = [m for m in memories if m["topic_id"] == topic_id]
        t_embs = np.array([m["embedding"] for m in t_mems])
        km = KMeans(n_clusters=20, random_state=seed, n_init=1)
        labels = km.fit_predict(t_embs)
        for w in range(20):
            cluster = [t_mems[i] for i in range(len(t_mems)) if labels[i] == w]
            if len(cluster) == 0:
                cluster = [t_mems[w]] # fallback
            cluster_embs = np.array([m["embedding"] for m in cluster])
            centroid = np.mean(cluster_embs, axis=0)
            centroid = centroid / np.linalg.norm(centroid)
            latest_t = max(m["timestamp_hours"] for m in cluster)
            node_id = f"refl_km_{topic_id}_{w:02d}_s{seed}"
            refl_nodes.append({
                "id": node_id,
                "topic_id": topic_id,
                "timestamp_hours": latest_t,
                "importance": float(importance),
                "embedding": centroid.tolist(),
                "is_reflection": True,
            })
    return refl_nodes

def evaluate_reflection_pool(memories, refl_nodes, queries, weights=(0.2, 0.5, 0.3), t_curr=72.0):
    all_mems = memories + refl_nodes
    alpha, beta, gamma = weights
    all_embs = np.array([m["embedding"] for m in all_mems])
    all_imps = [float(m["importance"]) for m in all_mems]
    all_recs = [0.995 ** (t_curr - float(m["timestamp_hours"])) for m in all_mems]

    n_imps = min_max_norm(all_imps)
    n_recs = min_max_norm(all_recs)

    rank1_refl_count = 0
    top5_refl_slot_count = 0
    target_ranks = []
    mrrs = []

    for q in queries:
        qvec = np.array(q["qvec"])
        sims = np.dot(all_embs, qvec).tolist()
        n_sims = min_max_norm(sims)

        scores = [alpha * r + beta * s + gamma * imp for r, s, imp in zip(n_recs, n_sims, n_imps)]
        ranked_indices = sorted(range(len(all_mems)), key=lambda i: scores[i], reverse=True)

        t_id = q["target_id"]
        t_idx = next(i for i, m in enumerate(all_mems) if m["id"] == t_id)
        trank = ranked_indices.index(t_idx) + 1
        target_ranks.append(trank)
        mrrs.append(1.0 / trank)

        if all_mems[ranked_indices[0]].get("is_reflection", False):
            rank1_refl_count += 1
        top5_refl_slot_count += sum(1 for i in ranked_indices[:5] if all_mems[i].get("is_reflection", False))

    return {
        "mrr_mean": float(np.mean(mrrs)),
        "mrr_std": float(np.std(mrrs, ddof=1)),
        "mean_target_rank": float(np.mean(target_ranks)),
        "min_target_rank": int(np.min(target_ranks)),
        "max_target_rank": int(np.max(target_ranks)),
        "rank1_crowding_count": rank1_refl_count,
        "rank1_crowding_pct": rank1_refl_count / float(len(queries)) * 100.0,
        "top5_refl_slots": top5_refl_slot_count,
        "top5_refl_slots_pct": top5_refl_slot_count / (5.0 * len(queries)) * 100.0,
    }

def run_challenge_1(memories, queries):
    print("=" * 80)
    print("CHALLENGE 1: COUNTERFACTUAL REPLICATION & REFLECTION DYNAMICS")
    print("=" * 80)

    # 1. Deterministic sweep across reflection importance values
    print("\n--- 1.1 Deterministic Reflection Importance Sweep ---")
    imp_levels = [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]
    sweep_results = {}
    for imp in imp_levels:
        refl = generate_deterministic_reflections(memories, importance=imp)
        res = evaluate_reflection_pool(memories, refl, queries)
        sweep_results[imp] = res
        print(f"  Importance = {imp:4.1f} | MRR = {res['mrr_mean']:.4f} | Rank-1 Crowding = {res['rank1_crowding_count']:3d}/100 ({res['rank1_crowding_pct']:5.1f}%) | "
              f"Top-5 Slots = {res['top5_refl_slots']:3d}/500 ({res['top5_refl_slots_pct']:5.1f}%) | Mean Target Rank = {res['mean_target_rank']:5.2f}")

    # 2. Testing across multiple seeds: Does importance=5.0 ALWAYS eliminate 100% Rank-1 crowding?
    print("\n--- 1.2 Adversarial Multi-Seed Stress-Testing (Importance = 5.0) ---")
    seeds = list(range(50)) # 50 distinct seeds

    # Random partition clustering
    rand_part_crowding = []
    rand_part_top5 = []
    rand_part_mrrs = []
    for s in seeds:
        refl = generate_random_partition_reflections(memories, importance=5.0, seed=s)
        res = evaluate_reflection_pool(memories, refl, queries)
        rand_part_crowding.append(res['rank1_crowding_count'])
        rand_part_top5.append(res['top5_refl_slots'])
        rand_part_mrrs.append(res['mrr_mean'])

    print(f"  Random Partition (50 seeds, imp=5.0):")
    print(f"    Rank-1 Crowding Count: min={min(rand_part_crowding)}, max={max(rand_part_crowding)}, mean={np.mean(rand_part_crowding):.2f}")
    print(f"    Top-5 Refl Slots:      min={min(rand_part_top5)}, max={max(rand_part_top5)}, mean={np.mean(rand_part_top5):.2f}")
    print(f"    Mean MRR across seeds: {np.mean(rand_part_mrrs):.4f} +/- {np.std(rand_part_mrrs):.4f}")

    # KMeans clustering across seeds
    km_crowding = []
    km_top5 = []
    km_mrrs = []
    for s in seeds[:30]: # 30 seeds
        refl = generate_kmeans_reflections(memories, importance=5.0, seed=s)
        res = evaluate_reflection_pool(memories, refl, queries)
        km_crowding.append(res['rank1_crowding_count'])
        km_top5.append(res['top5_refl_slots'])
        km_mrrs.append(res['mrr_mean'])

    print(f"  K-Means Clustering (30 seeds, imp=5.0):")
    print(f"    Rank-1 Crowding Count: min={min(km_crowding)}, max={max(km_crowding)}, mean={np.mean(km_crowding):.2f}")
    print(f"    Top-5 Refl Slots:      min={min(km_top5)}, max={max(km_top5)}, mean={np.mean(km_top5):.2f}")
    print(f"    Mean MRR across seeds: {np.mean(km_mrrs):.4f} +/- {np.std(km_mrrs):.4f}")

    # 3. Multi-Seed Stress Testing for 6.0, 7.0, 8.0, 8.5
    print("\n--- 1.3 Multi-Seed Crowding Across Elevated Importance Levels [5.0, 6.0, 7.0, 8.0, 8.5] ---")
    multi_seed_results = {}
    for imp in [5.0, 6.0, 7.0, 8.0, 8.5]:
        crowd_counts = []
        top5_counts = []
        mrrs = []
        for s in range(20): # 20 seeds
            refl = generate_random_partition_reflections(memories, importance=imp, seed=s)
            res = evaluate_reflection_pool(memories, refl, queries)
            crowd_counts.append(res['rank1_crowding_count'])
            top5_counts.append(res['top5_refl_slots'])
            mrrs.append(res['mrr_mean'])
        multi_seed_results[imp] = {
            "crowd_mean": float(np.mean(crowd_counts)),
            "crowd_min": int(min(crowd_counts)),
            "crowd_max": int(max(crowd_counts)),
            "top5_mean": float(np.mean(top5_counts)),
            "mrr_mean": float(np.mean(mrrs)),
            "mrr_std": float(np.std(mrrs)),
        }
        print(f"  Importance = {imp:4.1f} | Mean Rank-1 Crowding: {np.mean(crowd_counts):5.1f}% (range: {min(crowd_counts)}-{max(crowd_counts)}) | "
              f"Mean Top-5 Refl Slots: {np.mean(top5_counts):5.1f}/500 | Mean MRR: {np.mean(mrrs):.4f}")

    return {
        "deterministic_sweep": sweep_results,
        "multi_seed_results": multi_seed_results,
        "rand_part_5_0": {
            "crowding_min": int(min(rand_part_crowding)),
            "crowding_max": int(max(rand_part_crowding)),
            "crowding_mean": float(np.mean(rand_part_crowding)),
            "top5_min": int(min(rand_part_top5)),
            "top5_max": int(max(rand_part_top5)),
            "top5_mean": float(np.mean(rand_part_top5)),
            "mrr_mean": float(np.mean(rand_part_mrrs)),
        },
        "km_5_0": {
            "crowding_min": int(min(km_crowding)),
            "crowding_max": int(max(km_crowding)),
            "crowding_mean": float(np.mean(km_crowding)),
            "top5_min": int(min(km_top5)),
            "top5_max": int(max(km_top5)),
            "top5_mean": float(np.mean(km_top5)),
            "mrr_mean": float(np.mean(km_mrrs)),
        }
    }


# ==============================================================================
# CHALLENGE 2: NORMALIZATION STRESS-TESTING ON A7 vs A4
# ==============================================================================
def evaluate_condition_under_norm(pre, weights, norm_fn, norm_name=""):
    alpha, beta, gamma = weights
    raw_imps = pre["raw_imps"]
    raw_recs = pre["raw_recs"]
    query_data = pre["query_data"]

    norm_imps = norm_fn(raw_imps)
    norm_recs = norm_fn(raw_recs)

    mrrs = []
    ndcg5s = []
    target_ranks = []

    for qd in query_data:
        sims = qd["sims"]
        norm_sims = norm_fn(sims)
        scores = [alpha * r + beta * s + gamma * imp for r, s, imp in zip(norm_recs, norm_sims, norm_imps)]
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        t_idx = qd["target_idx"]
        trank = ranked.index(t_idx) + 1
        target_ranks.append(trank)
        mrrs.append(1.0 / trank)
        ndcg5s.append(compute_ndcg5(trank))

    return {
        "norm_name": norm_name,
        "weights": list(weights),
        "mrr_mean": float(np.mean(mrrs)),
        "mrr_std": float(np.std(mrrs, ddof=1)),
        "ndcg5_mean": float(np.mean(ndcg5s)),
        "median_rank": float(np.median(target_ranks)),
        "mean_rank": float(np.mean(target_ranks)),
        "min_rank": int(min(target_ranks)),
        "max_rank": int(max(target_ranks)),
    }

def run_challenge_2(pre):
    print("\n" + "=" * 80)
    print("CHALLENGE 2: NORMALIZATION STRESS-TESTING ON A7 (gamma=0.3) vs A4 (gamma=0.0)")
    print("=" * 80)

    weights_a7 = (0.2, 0.5, 0.3) # Full Tri-Factor
    weights_a4 = (0.3, 0.7, 0.0) # Recency + Relevance

    # 1. Baseline Min-Max Normalization
    res_a7_minmax = evaluate_condition_under_norm(pre, weights_a7, min_max_norm, "Min-Max")
    res_a4_minmax = evaluate_condition_under_norm(pre, weights_a4, min_max_norm, "Min-Max")
    print(f"  [Baseline Min-Max] A7 MRR = {res_a7_minmax['mrr_mean']:.4f} | A4 MRR = {res_a4_minmax['mrr_mean']:.4f} | Delta = {res_a7_minmax['mrr_mean'] - res_a4_minmax['mrr_mean']:+.4f}")

    # 2. Z-Score Normalization
    res_a7_zscore = evaluate_condition_under_norm(pre, weights_a7, z_score_norm, "Z-Score")
    res_a4_zscore = evaluate_condition_under_norm(pre, weights_a4, z_score_norm, "Z-Score")
    print(f"  [Z-Score Norm]     A7 MRR = {res_a7_zscore['mrr_mean']:.4f} | A4 MRR = {res_a4_zscore['mrr_mean']:.4f} | Delta = {res_a7_zscore['mrr_mean'] - res_a4_zscore['mrr_mean']:+.4f}")

    # 3. Quantile / Rank Normalization
    res_a7_quantile = evaluate_condition_under_norm(pre, weights_a7, quantile_norm, "Quantile (Rank)")
    res_a4_quantile = evaluate_condition_under_norm(pre, weights_a4, quantile_norm, "Quantile (Rank)")
    print(f"  [Quantile Norm]    A7 MRR = {res_a7_quantile['mrr_mean']:.4f} | A4 MRR = {res_a4_quantile['mrr_mean']:.4f} | Delta = {res_a7_quantile['mrr_mean'] - res_a4_quantile['mrr_mean']:+.4f}")

    # 4. Softmax Normalization across multiple temperatures
    print("\n  Softmax Normalization across temperature values (tau):")
    softmax_results = {}
    tau_list = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
    for tau in tau_list:
        fn = lambda vals, t=tau: softmax_norm(vals, temperature=t)
        res_a7_sm = evaluate_condition_under_norm(pre, weights_a7, fn, f"Softmax(tau={tau})")
        res_a4_sm = evaluate_condition_under_norm(pre, weights_a4, fn, f"Softmax(tau={tau})")
        softmax_results[tau] = {"a7": res_a7_sm, "a4": res_a4_sm}
        print(f"    tau = {tau:6.3f} | A7 MRR = {res_a7_sm['mrr_mean']:.4f} | A4 MRR = {res_a4_sm['mrr_mean']:.4f} | Delta = {res_a7_sm['mrr_mean'] - res_a4_sm['mrr_mean']:+.4f}")

    # 5. Softmax on Min-Max Scaled Inputs
    print("\n  Softmax on Min-Max Normalized Inputs across temperature values (tau):")
    softmax_minmax_results = {}
    for tau in [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]:
        fn = lambda vals, t=tau: softmax_norm(min_max_norm(vals), temperature=t)
        res_a7_smm = evaluate_condition_under_norm(pre, weights_a7, fn, f"SoftmaxMinMax(tau={tau})")
        res_a4_smm = evaluate_condition_under_norm(pre, weights_a4, fn, f"SoftmaxMinMax(tau={tau})")
        softmax_minmax_results[tau] = {"a7": res_a7_smm, "a4": res_a4_smm}
        print(f"    tau = {tau:6.3f} | A7 MRR = {res_a7_smm['mrr_mean']:.4f} | A4 MRR = {res_a4_smm['mrr_mean']:.4f} | Delta = {res_a7_smm['mrr_mean'] - res_a4_smm['mrr_mean']:+.4f}")

    # 6. Unnormalized Raw Scores
    identity_norm = lambda vals: list(vals)
    res_a7_raw = evaluate_condition_under_norm(pre, weights_a7, identity_norm, "Raw Unnormalized")
    res_a4_raw = evaluate_condition_under_norm(pre, weights_a4, identity_norm, "Raw Unnormalized")
    print(f"\n  [Raw Unnormalized] A7 MRR = {res_a7_raw['mrr_mean']:.4f} | A4 MRR = {res_a4_raw['mrr_mean']:.4f} | Delta = {res_a7_raw['mrr_mean'] - res_a4_raw['mrr_mean']:+.4f}")

    # 7. Comprehensive summary check: Did ANY normalization on A7 beat A4 (0.5002)?
    all_a7_mrrs = [
        res_a7_minmax["mrr_mean"],
        res_a7_zscore["mrr_mean"],
        res_a7_quantile["mrr_mean"],
        res_a7_raw["mrr_mean"],
    ] + [v["a7"]["mrr_mean"] for v in softmax_results.values()] + [v["a7"]["mrr_mean"] for v in softmax_minmax_results.values()]

    max_a7_mrr = max(all_a7_mrrs)
    beat_a4 = max_a7_mrr > 0.5002
    print(f"\n  MAX A7 MRR across ALL normalizations: {max_a7_mrr:.4f}")
    print(f"  Target Baseline A4 MRR:              0.5002")
    print(f"  Can alternative normalization rescue A7 to beat A4? {'YES' if beat_a4 else 'NO (DEFINITIVELY FALSIFIED)'}")

    return {
        "a7_minmax": res_a7_minmax,
        "a4_minmax": res_a4_minmax,
        "a7_zscore": res_a7_zscore,
        "a4_zscore": res_a4_zscore,
        "a7_quantile": res_a7_quantile,
        "a4_quantile": res_a4_quantile,
        "a7_raw": res_a7_raw,
        "a4_raw": res_a4_raw,
        "softmax_results": softmax_results,
        "softmax_minmax_results": softmax_minmax_results,
        "max_a7_mrr": max_a7_mrr,
        "beat_a4": beat_a4,
    }


# ==============================================================================
# CHALLENGE 3: SIMPLEX MONOTONICITY & HIGH-RESOLUTION INTERIOR SEARCH
# ==============================================================================
def run_challenge_3(pre):
    print("\n" + "=" * 80)
    print("CHALLENGE 3: HIGH-RESOLUTION SIMPLEX MONOTONICITY & INTERIOR OPTIMUM SEARCH")
    print("=" * 80)

    # Pre-normalize the components per query
    raw_imps = pre["raw_imps"]
    raw_recs = pre["raw_recs"]
    query_data = pre["query_data"]

    n_imps = np.array(min_max_norm(raw_imps), dtype=float) # (500,)
    n_recs = np.array(min_max_norm(raw_recs), dtype=float) # (500,)

    n_sims_all = []
    target_indices = []
    for qd in query_data:
        n_sims_all.append(np.array(min_max_norm(qd["sims"]), dtype=float))
        target_indices.append(qd["target_idx"])
    n_sims_mat = np.array(n_sims_all) # (100, 500)
    target_indices = np.array(target_indices) # (100,)

    # Generate high-resolution simplex grid (step=0.01 -> 5,151 points)
    step = 0.01
    steps = int(round(1.0 / step)) + 1
    simplex_points = []
    for a_i in range(steps):
        for b_i in range(steps - a_i):
            c_i = steps - 1 - a_i - b_i
            alpha = round(a_i * step, 4)
            beta = round(b_i * step, 4)
            gamma = round(c_i * step, 4)
            simplex_points.append((alpha, beta, gamma))

    print(f"  Evaluating {len(simplex_points)} simplex points on high-resolution grid (step={step})...")
    t0 = time.perf_counter()

    results = []
    interior_points_gt_a4 = []
    max_interior_mrr = -1.0
    best_interior_pt = None

    boundary_gamma0_points = []
    gamma_strata = {} # gamma -> list of MRRs

    for alpha, beta, gamma in simplex_points:
        # Vectorized score calculation: (100, 500)
        # scores = alpha * n_recs + beta * n_sims_mat + gamma * n_imps
        # Notice n_recs and n_imps are (500,), n_sims_mat is (100, 500)
        scores = alpha * n_recs[None, :] + beta * n_sims_mat + gamma * n_imps[None, :] # (100, 500)

        # Target scores: (100,)
        # Use advanced indexing to get score of target for each query
        row_indices = np.arange(len(target_indices))
        target_scores = scores[row_indices, target_indices] # (100,)

        # Rank of target: count of memories with score > target_score + 1
        # (100, 500) > (100, 1)
        ranks = np.sum(scores > target_scores[:, None], axis=1) + 1
        mrrs = 1.0 / ranks
        mrr_mean = float(np.mean(mrrs))

        pt_dict = {
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
            "mrr": mrr_mean,
        }
        results.append(pt_dict)

        g_key = round(gamma, 2)
        if g_key not in gamma_strata:
            gamma_strata[g_key] = []
        gamma_strata[g_key].append(mrr_mean)

        if gamma == 0.0:
            boundary_gamma0_points.append(pt_dict)
        else:
            if mrr_mean > max_interior_mrr:
                max_interior_mrr = mrr_mean
                best_interior_pt = pt_dict
            if mrr_mean > 0.5002:
                interior_points_gt_a4.append(pt_dict)

    eval_time = time.perf_counter() - t0
    print(f"  Completed {len(simplex_points)} points in {eval_time:.2f}s ({len(simplex_points)*100/eval_time:.0f} query evals/sec)")

    # Analyze global and boundary optima
    best_overall = max(results, key=lambda x: x["mrr"])
    best_boundary = max(boundary_gamma0_points, key=lambda x: x["mrr"])

    print(f"\n  [GLOBAL OPTIMUM]:   alpha={best_overall['alpha']:.2f}, beta={best_overall['beta']:.2f}, gamma={best_overall['gamma']:.2f} -> MRR = {best_overall['mrr']:.4f}")
    print(f"  [BOUNDARY gamma=0]: alpha={best_boundary['alpha']:.2f}, beta={best_boundary['beta']:.2f}, gamma={best_boundary['gamma']:.2f} -> MRR = {best_boundary['mrr']:.4f}")
    print(f"  [BEST INTERIOR gamma>0]: alpha={best_interior_pt['alpha']:.2f}, beta={best_interior_pt['beta']:.2f}, gamma={best_interior_pt['gamma']:.2f} -> MRR = {best_interior_pt['mrr']:.4f}")

    print(f"\n  Interior points with gamma > 0 that achieve MRR > 0.5002:")
    print(f"    Total Count: {len(interior_points_gt_a4)}")
    if len(interior_points_gt_a4) > 0:
        print(f"    Top 5 Interior Points:")
        sorted_int = sorted(interior_points_gt_a4, key=lambda x: x["mrr"], reverse=True)
        for pt in sorted_int[:5]:
            print(f"      alpha={pt['alpha']:.2f}, beta={pt['beta']:.2f}, gamma={pt['gamma']:.2f} -> MRR = {pt['mrr']:.4f}")
        max_gamma_gt_a4 = max(pt["gamma"] for pt in interior_points_gt_a4)
        print(f"    Maximum gamma among points beating A4: gamma = {max_gamma_gt_a4:.2f}")
    else:
        print("    NONE! Zero interior points achieve MRR > 0.5002.")

    # Stratified gamma curve: max MRR as a function of gamma
    print("\n  Monotonicity Gradient: Maximum MRR by gamma level:")
    sorted_gamma = sorted(gamma_strata.keys())
    gamma_curve = []
    for g in sorted_gamma:
        max_m = max(gamma_strata[g])
        mean_m = np.mean(gamma_strata[g])
        gamma_curve.append({"gamma": g, "max_mrr": float(max_m), "mean_mrr": float(mean_m)})
        if g in [0.0, 0.01, 0.02, 0.03, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.70, 1.0]:
            print(f"    gamma = {g:4.2f} | Max MRR = {max_m:.4f} | Mean MRR = {mean_m:.4f}")

    return {
        "best_overall": best_overall,
        "best_boundary": best_boundary,
        "best_interior": best_interior_pt,
        "interior_points_gt_a4_count": len(interior_points_gt_a4),
        "interior_points_gt_a4_sample": interior_points_gt_a4[:10],
        "gamma_curve": gamma_curve,
    }


def main():
    print("=" * 80)
    print("STARTING EMPIRICAL CHALLENGE SUITE")
    print("=" * 80)

    memories, queries = load_benchmark()
    pre = prepare_precomputed_data(memories, queries)

    # 1. Counterfactual Replication
    res1 = run_challenge_1(memories, queries)

    # 2. Normalization Stress-Testing
    res2 = run_challenge_2(pre)

    # 3. Simplex Monotonicity
    res3 = run_challenge_3(pre)

    # Save empirical results to JSON
    output_path = ROOT / "empirical_challenge_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "challenge_1": res1,
            "challenge_2": res2,
            "challenge_3": res3,
        }, f, indent=2)
    print(f"\nSaved empirical challenge results to: {output_path}")

    print("\n" + "=" * 80)
    print("EMPIRICAL CHALLENGE SUITE COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
