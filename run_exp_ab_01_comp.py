"""
Curo SimLab Phase 4 Live Execution Harness
Experiment: EXP-AB-01-COMP (Memory Component Ablation)
Target Primitive: PR-COG-01 (Tri-Factor Memory Retrieval Scoring)
Authority State:
  Lifecycle: PHASE_4_EXECUTION_AUTHORIZED
  Execution Authority: GRANTED_LIMITED_PHASE_4
  Architecture Status: UNFROZEN
  Final SimLab Implementation: NOT_GRANTED
  Primitive Adjudication: NOT_AUTHORIZED
"""

import json
import hashlib
import time
import math
import numpy as np
import scipy.stats as stats
import os
from pathlib import Path
from typing import Optional

from audits.governance_firewall import assert_execution_permitted, GovernanceFirewallBlockedError
from simlab.memory.scoring import min_max_norm
from simlab.governance.permissions import OperationTier
from simlab.governance.firewall import GovernanceManager

REPO_ROOT = Path(__file__).resolve().parent
BENCHMARK_PATH = str(REPO_ROOT / "phase3_execution" / "SimLab_MemBench_500.json")
EXPECTED_DATASET_SHA256 = "97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800"
TELEMETRY_DIR = str(REPO_ROOT / "phase4_execution" / "telemetry" / "exp_ab_01_comp")
TELEMETRY_FILE = os.path.join(TELEMETRY_DIR, "exp_ab_01_comp_telemetry.jsonl")
RESULTS_JSON = os.path.join(TELEMETRY_DIR, "exp_ab_01_comp_results.json")

def verify_dataset_hash():
    with open(BENCHMARK_PATH, "rb") as f:
        data = f.read()
    h = hashlib.sha256(data).hexdigest()
    assert h == EXPECTED_DATASET_SHA256, f"Dataset hash mismatch: got {h}, expected {EXPECTED_DATASET_SHA256}"
    print(f"[PASS] Dataset integrity verified: SHA-256 = {h}")

def compute_ndcg5(target_rank):
    if target_rank <= 5:
        return 1.0 / math.log2(target_rank + 1)
    return 0.0

def compute_temporal_inversion_rate(top5_indices, candidate_memories):
    inversions = 0
    total_pairs = 0
    for i in range(len(top5_indices)):
        for j in range(i + 1, len(top5_indices)):
            total_pairs += 1
            if candidate_memories[top5_indices[i]]['timestamp_hours'] < candidate_memories[top5_indices[j]]['timestamp_hours']:
                inversions += 1
    return inversions / float(total_pairs) if total_pairs > 0 else 0.0

def generate_reflection_nodes(memories):
    reflection_nodes = []
    for topic_id in range(5):
        t_mems = [m for m in memories if m['topic_id'] == topic_id]
        t_mems.sort(key=lambda x: x['timestamp_hours'])
        for w in range(20):
            cluster = t_mems[w * 5 : (w + 1) * 5]
            cluster_embs = np.array([m['embedding'] for m in cluster])
            centroid = np.mean(cluster_embs, axis=0)
            centroid = centroid / np.linalg.norm(centroid)
            latest_t = max(m['timestamp_hours'] for m in cluster)
            node_id = f"refl_{topic_id}_{w:02d}"
            reflection_nodes.append({
                'id': node_id,
                'topic_id': topic_id,
                'topic': f"topic_{topic_id}",
                'timestamp_hours': latest_t,
                'importance': 8.5,
                'embedding': centroid.tolist(),
                'is_reflection': True
            })
    return reflection_nodes

def evaluate_query(query, candidates, weights, condition_code, t_curr=72.0):
    t0 = time.perf_counter()
    qvec = np.array(query['qvec'])
    alpha, beta, gamma = weights

    c_embs = np.array([m['embedding'] for m in candidates])
    sims = np.dot(c_embs, qvec).tolist()
    imps = [float(m['importance']) for m in candidates]
    recs = [0.995 ** (t_curr - m['timestamp_hours']) for m in candidates]

    norm_sims = min_max_norm(sims)
    norm_imps = min_max_norm(imps)
    norm_recs = min_max_norm(recs)

    scores = [
        alpha * r + beta * s + gamma * imp
        for r, s, imp in zip(norm_recs, norm_sims, norm_imps)
    ]

    latency_ms = (time.perf_counter() - t0) * 1000.0

    ranked_indices = sorted(range(len(candidates)), key=lambda idx: scores[idx], reverse=True)
    target_id = query['target_id']
    
    target_cand_idx = None
    for idx, m in enumerate(candidates):
        if m['id'] == target_id:
            target_cand_idx = idx
            break

    if target_cand_idx is not None and target_cand_idx in ranked_indices:
        target_rank = ranked_indices.index(target_cand_idx) + 1
    else:
        target_rank = len(candidates) + 1
    reciprocal_rank = 1.0 / target_rank
    ndcg5 = compute_ndcg5(target_rank)
    top5_indices = ranked_indices[:5]
    temporal_inversion = compute_temporal_inversion_rate(top5_indices, candidates)
    false_retrieval = 1 if target_rank > 1 else 0

    top1_is_reflection = bool(candidates[ranked_indices[0]].get('is_reflection', False))
    reflection_count_top5 = sum(1 for idx in top5_indices if candidates[idx].get('is_reflection', False))

    return {
        "experiment_id": "EXP-AB-01-COMP",
        "condition_code": condition_code,
        "query_id": query['query_id'],
        "query_type": query['type'],
        "target_id": target_id,
        "target_rank": target_rank,
        "reciprocal_rank": reciprocal_rank,
        "ndcg5": ndcg5,
        "temporal_inversion_rate": temporal_inversion,
        "false_retrieval": false_retrieval,
        "latency_ms": latency_ms,
        "top1_is_reflection": top1_is_reflection,
        "reflection_count_top5": reflection_count_top5,
    }

def main(mock_mode: bool = False, output_dir: Optional[str] = None):
    if mock_mode:
        GovernanceManager().check_authorization(OperationTier.DETERMINISTIC_MOCK_EXPERIMENT, "EXP-AB-01-COMP")
    else:
        assert_execution_permitted()
    print("=" * 80)
    print("CURO SIMLAB: EXP-AB-01-COMP LIVE EXECUTION HARNESS")
    print("=" * 80)

    verify_dataset_hash()

    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        bench = json.load(f)

    memories = bench['memories']
    queries = bench['queries']
    refl_nodes = generate_reflection_nodes(memories)
    memories_a8 = memories + refl_nodes

    print(f"Standard Memory Pool: {len(memories)} nodes")
    print(f"Augmented Memory Pool (A8): {len(memories_a8)} nodes (including {len(refl_nodes)} reflection nodes)")
    print(f"Queries: {len(queries)}")

    CONDITIONS = [
        {"code": "A1", "name": "RECENCY_ONLY", "weights": (1.0, 0.0, 0.0), "pool": memories},
        {"code": "A2", "name": "RELEVANCE_ONLY", "weights": (0.0, 1.0, 0.0), "pool": memories},
        {"code": "A3", "name": "IMPORTANCE_ONLY", "weights": (0.0, 0.0, 1.0), "pool": memories},
        {"code": "A4", "name": "RECENCY_RELEVANCE", "weights": (0.3, 0.7, 0.0), "pool": memories},
        {"code": "A5", "name": "RECENCY_IMPORTANCE", "weights": (0.5, 0.0, 0.5), "pool": memories},
        {"code": "A6", "name": "RELEVANCE_IMPORTANCE", "weights": (0.0, 0.7, 0.3), "pool": memories},
        {"code": "A7", "name": "FULL_TRI_FACTOR", "weights": (0.2, 0.5, 0.3), "pool": memories},
        {"code": "A8", "name": "TRI_FACTOR_REFLECTION", "weights": (0.2, 0.5, 0.3), "pool": memories_a8},
    ]

    all_telemetry = []
    condition_summaries = {}

    print("\n--- EXECUTING 8 CONTROLLED CONDITIONS (800 EPISODES) ---")
    for cond in CONDITIONS:
        code = cond['code']
        name = cond['name']
        weights = cond['weights']
        pool = cond['pool']

        cond_results = []
        for q in queries:
            res = evaluate_query(q, pool, weights, code)
            res['condition_name'] = name
            res['weights'] = list(weights)
            all_telemetry.append(res)
            cond_results.append(res)

        mrrs = [r['reciprocal_rank'] for r in cond_results]
        ndcg5s = [r['ndcg5'] for r in cond_results]
        invs = [r['temporal_inversion_rate'] for r in cond_results]
        frs = [r['false_retrieval'] for r in cond_results]
        lats = [r['latency_ms'] for r in cond_results]

        types = ["RECENCY_SENSITIVE", "RELEVANCE_DOMINANT", "TEMPORAL_CONFLICT"]
        strat = {}
        for t in types:
            t_mrrs = [r['reciprocal_rank'] for r in cond_results if r['query_type'] == t]
            t_ndcg5s = [r['ndcg5'] for r in cond_results if r['query_type'] == t]
            strat[t] = {
                "count": len(t_mrrs),
                "mrr_mean": float(np.mean(t_mrrs)),
                "mrr_std": float(np.std(t_mrrs)),
                "ndcg5_mean": float(np.mean(t_ndcg5s)),
                "ndcg5_std": float(np.std(t_ndcg5s)),
            }

        mrr_mean = float(np.mean(mrrs))
        mrr_std = float(np.std(mrrs, ddof=1))
        ci95_margin = 1.96 * (mrr_std / math.sqrt(len(mrrs)))

        condition_summaries[code] = {
            "condition_code": code,
            "condition_name": name,
            "weights": list(weights),
            "pool_size": len(pool),
            "episodes": len(cond_results),
            "mrr_mean": mrr_mean,
            "mrr_std": mrr_std,
            "mrr_ci95": [mrr_mean - ci95_margin, mrr_mean + ci95_margin],
            "ndcg5_mean": float(np.mean(ndcg5s)),
            "ndcg5_std": float(np.std(ndcg5s, ddof=1)),
            "temporal_inversion_rate_mean": float(np.mean(invs)),
            "false_retrieval_rate": float(np.mean(frs)),
            "latency_ms_mean": float(np.mean(lats)),
            "latency_ms_std": float(np.std(lats, ddof=1)),
            "stratified": strat,
            "raw_mrrs": mrrs,
            "raw_ndcg5s": ndcg5s,
        }

        if code == "A8":
            refl_top1 = sum(1 for r in cond_results if r['top1_is_reflection'])
            refl_top5 = sum(1 for r in cond_results if r['reflection_count_top5'] > 0)
            refl_top5_total = sum(r['reflection_count_top5'] for r in cond_results)
            condition_summaries[code]["reflection_metrics"] = {
                "top1_reflection_crowding_count": refl_top1,
                "top1_reflection_crowding_pct": refl_top1 / len(cond_results),
                "queries_with_reflection_in_top5_count": refl_top5,
                "queries_with_reflection_in_top5_pct": refl_top5 / len(cond_results),
                "total_reflection_slots_in_top5": refl_top5_total,
                "mean_reflection_slots_per_query": refl_top5_total / len(cond_results),
            }

        print(f"  [{code}] {name:<23}: MRR = {mrr_mean:.4f} +/- {mrr_std:.4f} | NDCG@5 = {condition_summaries[code]['ndcg5_mean']:.4f} | Inversion = {condition_summaries[code]['temporal_inversion_rate_mean'] * 100:.1f}% | FalseRet = {condition_summaries[code]['false_retrieval_rate'] * 100:.1f}%")

    print("\n--- STATISTICAL COMPARISONS AGAINST A7 (FULL_TRI_FACTOR) ---")
    a7_mrrs = condition_summaries["A7"]["raw_mrrs"]
    comparisons = {}
    bonferroni_alpha = 0.01 / 7.0

    for code in ["A1", "A2", "A3", "A4", "A5", "A6", "A8"]:
        cond_mrrs = condition_summaries[code]["raw_mrrs"]
        delta_mrr = condition_summaries[code]["mrr_mean"] - condition_summaries["A7"]["mrr_mean"]

        diffs = [c - a for c, a in zip(cond_mrrs, a7_mrrs)]
        diff_mean = float(np.mean(diffs))
        diff_std = float(np.std(diffs, ddof=1)) if np.std(diffs, ddof=1) > 0 else 1e-9

        nonzero_diffs = [d for d in diffs if d != 0.0]
        if len(nonzero_diffs) > 0:
            stat_w, p_val = stats.wilcoxon(cond_mrrs, a7_mrrs, alternative='two-sided')
        else:
            stat_w, p_val = 0.0, 1.0

        cohen_d = diff_mean / diff_std if diff_std > 0 else 0.0
        ci_err = 1.96 * (diff_std / math.sqrt(len(diffs)))
        sig = p_val < bonferroni_alpha

        comparisons[code] = {
            "comparison": f"{code} vs A7",
            "delta_mrr": delta_mrr,
            "diff_mean": diff_mean,
            "diff_std": diff_std,
            "diff_ci95": [diff_mean - ci_err, diff_mean + ci_err],
            "wilcoxon_w": float(stat_w),
            "p_value": float(p_val),
            "bonferroni_alpha": bonferroni_alpha,
            "statistically_significant": sig,
            "cohens_d": float(cohen_d),
        }

        print(f"  {code} vs A7: Delta MRR = {delta_mrr:+.4f} | W = {stat_w:7.1f} | p = {p_val:.4e} | d = {cohen_d:+.4f} | Sig(adj) = {sig}")

    print("\n--- HYPOTHESIS EVALUATION (AS-03) ---")
    a4_delta = comparisons["A4"]["delta_mrr"]
    a4_p = comparisons["A4"]["p_value"]
    h1_non_inferior = (a4_delta >= -0.02)
    h0_satisfied = (condition_summaries["A7"]["mrr_mean"] - condition_summaries["A4"]["mrr_mean"]) >= 0.05 and a4_p < 0.0025

    print(f"  A4 vs A7 MRR Delta: {a4_delta:+.4f}")
    print(f"  Hypothesis H1 (Non-inferiority within Delta <= 0.02): {'CONFIRMED' if h1_non_inferior else 'REJECTED'}")
    print(f"  Null Hypothesis H0 (Importance strictly necessary Delta >= +0.05): {'ACCEPTED' if h0_satisfied else 'REJECTED'}")

    print("\n--- CONTINUOUS 2D WEIGHT SIMPLEX SWEEP (alpha + beta + gamma = 1.0, step=0.1, 66 points) ---")
    simplex_points = []
    for a_i in range(11):
        for b_i in range(11 - a_i):
            c_i = 10 - a_i - b_i
            alpha = round(a_i * 0.1, 1)
            beta = round(b_i * 0.1, 1)
            gamma = round(c_i * 0.1, 1)
            simplex_points.append((alpha, beta, gamma))

    simplex_results = []
    t_start_sweep = time.perf_counter()
    for alpha, beta, gamma in simplex_points:
        mrrs = []
        ndcg5s = []
        for q in queries:
            qvec = np.array(q['qvec'])
            sims = np.dot(np.array([m['embedding'] for m in memories]), qvec).tolist()
            imps = [m['importance'] for m in memories]
            recs = [0.995 ** (72.0 - m['timestamp_hours']) for m in memories]
            n_sims = min_max_norm(sims)
            n_imps = min_max_norm(imps)
            n_recs = min_max_norm(recs)
            sc = [alpha * r + beta * s + gamma * imp for r, s, imp in zip(n_recs, n_sims, n_imps)]
            target_matches = [i for i, m in enumerate(memories) if m['id'] == q['target_id']]
            if target_matches:
                t_idx = target_matches[0]
                rk = sorted(range(len(memories)), key=lambda i: sc[i], reverse=True).index(t_idx) + 1
            else:
                rk = len(memories) + 1
            mrrs.append(1.0 / rk)
            ndcg5s.append(compute_ndcg5(rk))
        simplex_results.append({
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
            "mrr_mean": float(np.mean(mrrs)),
            "mrr_std": float(np.std(mrrs, ddof=1)),
            "ndcg5_mean": float(np.mean(ndcg5s)),
        })

    sweep_time = time.perf_counter() - t_start_sweep
    print(f"  Completed 66 simplex points (6,600 query evaluations) in {sweep_time:.2f}s")

    best_simplex = max(simplex_results, key=lambda x: x['mrr_mean'])
    worst_simplex = min(simplex_results, key=lambda x: x['mrr_mean'])
    print(f"  Optimal Simplex Point: alpha={best_simplex['alpha']}, beta={best_simplex['beta']}, gamma={best_simplex['gamma']} -> MRR={best_simplex['mrr_mean']:.4f}")
    print(f"  Worst Simplex Point:   alpha={worst_simplex['alpha']}, beta={worst_simplex['beta']}, gamma={worst_simplex['gamma']} -> MRR={worst_simplex['mrr_mean']:.4f}")

    beta_gradient = {}
    for b_val in sorted(list(set(p['beta'] for p in simplex_results))):
        pts = [p for p in simplex_results if p['beta'] == b_val]
        beta_gradient[str(b_val)] = {
            "mean_mrr": float(np.mean([p['mrr_mean'] for p in pts])),
            "max_mrr": float(np.max([p['mrr_mean'] for p in pts])),
            "min_mrr": float(np.min([p['mrr_mean'] for p in pts])),
        }

    print(f"\n--- WRITING IMMUTABLE TELEMETRY ({len(all_telemetry)} events) ---")
    target_dir = output_dir or TELEMETRY_DIR
    target_telemetry = os.path.join(target_dir, "exp_ab_01_comp_telemetry.jsonl")
    target_results = os.path.join(target_dir, "exp_ab_01_comp_results.json")

    os.makedirs(target_dir, exist_ok=True)
    temp_telemetry = target_telemetry + ".tmp"
    with open(temp_telemetry, "w", encoding="utf-8") as f:
        for ev in all_telemetry:
            f.write(json.dumps(ev) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_telemetry, target_telemetry)

    telemetry_sha256 = hashlib.sha256(open(target_telemetry, "rb").read()).hexdigest()
    telemetry_bytes = os.path.getsize(target_telemetry)
    print(f"  Telemetry File: {target_telemetry}")
    print(f"  Telemetry Bytes: {telemetry_bytes}")
    print(f"  Telemetry SHA-256: {telemetry_sha256}")

    cleaned_summaries = {}
    for k, v in condition_summaries.items():
        c_copy = dict(v)
        c_copy.pop("raw_mrrs", None)
        c_copy.pop("raw_ndcg5s", None)
        cleaned_summaries[k] = c_copy

    consolidated_output = {
        "experiment_id": "EXP-AB-01-COMP",
        "experiment_title": "Memory Component Ablation",
        "primitive": "PR-COG-01",
        "dataset": {
            "name": "SimLab-MemBench-500",
            "path": BENCHMARK_PATH,
            "sha256": EXPECTED_DATASET_SHA256,
            "query_count": len(queries),
            "memory_count_base": len(memories),
            "memory_count_a8": len(memories_a8),
        },
        "governance": {
            "lifecycle": "PHASE_4_EXECUTION_AUTHORIZED",
            "execution_authority": "GRANTED_LIMITED_PHASE_4",
            "architecture_status": "UNFROZEN",
            "final_simlab_implementation": "NOT_GRANTED",
            "primitive_adjudication": "NOT_AUTHORIZED",
            "paid_api_calls": 0,
            "runtime_usd_spend": 0.00,
        },
        "telemetry": {
            "file": TELEMETRY_FILE,
            "event_count": len(all_telemetry),
            "byte_size": telemetry_bytes,
            "sha256": telemetry_sha256,
        },
        "condition_summaries": cleaned_summaries,
        "comparisons_vs_a7": comparisons,
        "hypothesis_testing": {
            "h1_non_inferiority_a4_vs_a7": {
                "threshold_delta": 0.02,
                "observed_delta": a4_delta,
                "verdict": "CONFIRMED" if h1_non_inferior else "REJECTED",
            },
            "h0_importance_necessity": {
                "threshold_delta": 0.05,
                "observed_delta": condition_summaries["A7"]["mrr_mean"] - condition_summaries["A4"]["mrr_mean"],
                "p_value": a4_p,
                "verdict": "REJECTED" if not h0_satisfied else "ACCEPTED",
            },
        },
        "simplex_sweep": {
            "total_points": len(simplex_results),
            "best_point": best_simplex,
            "worst_point": worst_simplex,
            "beta_gradient": beta_gradient,
            "all_points": simplex_results,
        },
    }

    temp_results = target_results + ".tmp"
    with open(temp_results, "w", encoding="utf-8") as f:
        json.dump(consolidated_output, f, indent=2, default=str)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_results, target_results)

    results_sha256 = hashlib.sha256(open(target_results, "rb").read()).hexdigest()
    print(f"  Results JSON: {target_results} (SHA-256: {results_sha256})")

    print("\n" + "=" * 80)
    print("EXP-AB-01-COMP EXECUTION COMPLETE")
    print("TELEMETRY PIPELINE: PHASE4_EXECUTION_PIPELINE_PASS")
    print("=" * 80)

if __name__ == "__main__":
    import sys
    is_mock = "--mock" in sys.argv or "--tier=mock" in sys.argv
    main(mock_mode=is_mock)
