import json
import math
import numpy as np
import scipy.stats as stats
import os

BENCHMARK_PATH = r"E:\projects\simlab\phase3_execution\SimLab_MemBench_500.json"
RESULTS_PATH = r"E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_results.json"
TELEMETRY_PATH = r"E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_telemetry.jsonl"
AS03_PATH = r"E:\projects\simlab\ablation_design\AS-03_memory_ablation_plan.md"

with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
    bench = json.load(f)

memories = bench["memories"]
queries = bench["queries"]

# Generate reflection nodes as in harness
refl_nodes = []
for topic_id in range(5):
    t_mems = [m for m in memories if m['topic_id'] == topic_id]
    t_mems.sort(key=lambda x: x['timestamp_hours'])
    for w in range(20):
        cluster = t_mems[w * 5 : (w + 1) * 5]
        cluster_embs = np.array([m['embedding'] for m in cluster])
        centroid = np.mean(cluster_embs, axis=0)
        centroid = centroid / np.linalg.norm(centroid)
        latest_t = max(m['timestamp_hours'] for m in cluster)
        refl_nodes.append({
            'id': f"refl_{topic_id}_{w:02d}",
            'topic_id': topic_id,
            'topic': f"topic_{topic_id}",
            'timestamp_hours': latest_t,
            'importance': 8.5,
            'embedding': centroid.tolist(),
            'is_reflection': True
        })

memories_a8 = memories + refl_nodes

def min_max_norm(vals):
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return [1.0] * len(vals)
    return [(v - mn) / (mx - mn) for v in vals]

print("=" * 80)
print("PART 1: COMPONENT SCORE DISTRIBUTIONS (RAW & NORMALIZED)")
print("=" * 80)

# Base memories (500)
base_imps = [m["importance"] for m in memories]
base_times = [m["timestamp_hours"] for m in memories]
base_recs = [0.995 ** (72.0 - t) for t in base_times]

# Augmented memories A8 (600)
a8_imps = [m["importance"] for m in memories_a8]
a8_times = [m["timestamp_hours"] for m in memories_a8]
a8_recs = [0.995 ** (72.0 - t) for t in a8_times]

def get_stats(arr, name=""):
    a = np.array(arr)
    q = np.percentile(a, [0, 25, 50, 75, 90, 95, 99, 100])
    return {
        "name": name,
        "count": len(a),
        "min": float(np.min(a)),
        "max": float(np.max(a)),
        "mean": float(np.mean(a)),
        "var": float(np.var(a, ddof=1)),
        "std": float(np.std(a, ddof=1)),
        "q0": float(q[0]),
        "q25": float(q[1]),
        "q50": float(q[2]),
        "q75": float(q[3]),
        "q90": float(q[4]),
        "q95": float(q[5]),
        "q99": float(q[6]),
        "q100": float(q[7]),
    }

print("Base Raw Importance:", get_stats(base_imps, "Base Raw Imp"))
print("Base Raw Recency:   ", get_stats(base_recs, "Base Raw Rec"))
print("A8 Raw Importance:  ", get_stats(a8_imps, "A8 Raw Imp"))
print("A8 Raw Recency:     ", get_stats(a8_recs, "A8 Raw Rec"))

# Per-query similarities
all_cosines = []
target_cosines = []
distractor_cosines = []
m_embs = np.array([m["embedding"] for m in memories])

for q in queries:
    qvec = np.array(q["qvec"])
    sims = np.dot(m_embs, qvec)
    all_cosines.extend(sims)
    t_id = q["target_id"]
    for idx, m in enumerate(memories):
        if m["id"] == t_id:
            target_cosines.append(sims[idx])
        else:
            distractor_cosines.append(sims[idx])

print("All Cosine Similarities (50,000):       ", get_stats(all_cosines, "All Cosines"))
print("Target Cosine Similarities (100):       ", get_stats(target_cosines, "Target Cosines"))
print("Distractor Cosine Similarities (49,900):", get_stats(distractor_cosines, "Distractor Cosines"))

print("\n" + "=" * 80)
print("PART 2: COMBINED SCORES PER CONDITION A1 - A8")
print("=" * 80)

CONDITIONS = [
    ("A1", "RECENCY_ONLY", (1.0, 0.0, 0.0), memories),
    ("A2", "RELEVANCE_ONLY", (0.0, 1.0, 0.0), memories),
    ("A3", "IMPORTANCE_ONLY", (0.0, 0.0, 1.0), memories),
    ("A4", "RECENCY_RELEVANCE", (0.3, 0.7, 0.0), memories),
    ("A5", "RECENCY_IMPORTANCE", (0.5, 0.0, 0.5), memories),
    ("A6", "RELEVANCE_IMPORTANCE", (0.0, 0.7, 0.3), memories),
    ("A7", "FULL_TRI_FACTOR", (0.2, 0.5, 0.3), memories),
    ("A8", "TRI_FACTOR_REFLECTION", (0.2, 0.5, 0.3), memories_a8),
]

cond_stats = {}

for code, name, (alpha, beta, gamma), pool in CONDITIONS:
    all_scores = []
    target_scores = []
    distractor_scores = []
    target_ranks = []
    top1_scores = []
    score_margins = [] # target_score - top_distractor_score
    
    p_embs = np.array([m["embedding"] for m in pool])
    p_imps = [float(m["importance"]) for m in pool]
    p_recs = [0.995 ** (72.0 - m["timestamp_hours"]) for m in pool]
    
    norm_imps = min_max_norm(p_imps)
    norm_recs = min_max_norm(p_recs)
    
    for q in queries:
        qvec = np.array(q["qvec"])
        sims = np.dot(p_embs, qvec).tolist()
        norm_sims = min_max_norm(sims)
        
        sc = [
            alpha * r + beta * s + gamma * imp
            for r, s, imp in zip(norm_recs, norm_sims, norm_imps)
        ]
        all_scores.extend(sc)
        
        # target
        t_id = q["target_id"]
        t_idx = next(i for i, m in enumerate(pool) if m["id"] == t_id)
        t_score = sc[t_idx]
        target_scores.append(t_score)
        
        # ranked
        ranked_idx = sorted(range(len(pool)), key=lambda i: sc[i], reverse=True)
        t_rank = ranked_idx.index(t_idx) + 1
        target_ranks.append(t_rank)
        
        top1_idx = ranked_idx[0]
        top1_scores.append(sc[top1_idx])
        
        # distractor scores
        d_scores = [sc[i] for i in range(len(pool)) if i != t_idx]
        distractor_scores.extend(d_scores)
        top_d_score = max(d_scores)
        score_margins.append(t_score - top_d_score)
        
    cond_stats[code] = {
        "code": code,
        "name": name,
        "weights": (alpha, beta, gamma),
        "pool_size": len(pool),
        "all_score_stats": get_stats(all_scores, f"{code} All Scores"),
        "target_score_stats": get_stats(target_scores, f"{code} Target Scores"),
        "distractor_score_stats": get_stats(distractor_scores, f"{code} Distractor Scores"),
        "score_margin_stats": get_stats(score_margins, f"{code} Score Margins"),
        "target_rank_stats": get_stats(target_ranks, f"{code} Target Ranks"),
        "mean_mrr": float(np.mean([1.0 / r for r in target_ranks])),
    }
    
    print(f"\nCondition {code} ({name}) [weights: {alpha}, {beta}, {gamma}]:")
    print(f"  All Scores:        min={cond_stats[code]['all_score_stats']['min']:.4f}, max={cond_stats[code]['all_score_stats']['max']:.4f}, mean={cond_stats[code]['all_score_stats']['mean']:.4f}, std={cond_stats[code]['all_score_stats']['std']:.4f}, var={cond_stats[code]['all_score_stats']['var']:.4f}")
    print(f"  Target Scores:     min={cond_stats[code]['target_score_stats']['min']:.4f}, max={cond_stats[code]['target_score_stats']['max']:.4f}, mean={cond_stats[code]['target_score_stats']['mean']:.4f}, std={cond_stats[code]['target_score_stats']['std']:.4f}")
    print(f"  Distractor Scores: min={cond_stats[code]['distractor_score_stats']['min']:.4f}, max={cond_stats[code]['distractor_score_stats']['max']:.4f}, mean={cond_stats[code]['distractor_score_stats']['mean']:.4f}, std={cond_stats[code]['distractor_score_stats']['std']:.4f}")
    print(f"  Score Margins:     min={cond_stats[code]['score_margin_stats']['min']:.4f}, max={cond_stats[code]['score_margin_stats']['max']:.4f}, mean={cond_stats[code]['score_margin_stats']['mean']:.4f}, std={cond_stats[code]['score_margin_stats']['std']:.4f}")
    print(f"  Target Ranks:      min={cond_stats[code]['target_rank_stats']['min']:.1f}, median={cond_stats[code]['target_rank_stats']['q50']:.1f}, mean={cond_stats[code]['target_rank_stats']['mean']:.1f}, max={cond_stats[code]['target_rank_stats']['max']:.1f}")
    print(f"  Mean MRR:          {cond_stats[code]['mean_mrr']:.4f}")

# Save json of cond_stats
with open(r"E:\projects\simlab\.agents\audit_explorer_2\condition_distributions.json", "w") as f:
    json.dump(cond_stats, f, indent=2)

print("\nSaved condition_distributions.json successfully.")
