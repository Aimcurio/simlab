import json
import numpy as np
import scipy.stats as stats

BENCHMARK_PATH = r"E:\projects\simlab\phase3_execution\SimLab_MemBench_500.json"
with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
    bench = json.load(f)

memories = bench["memories"]
queries = bench["queries"]

def min_max_norm(vals):
    mn, mx = min(vals), max(vals)
    if mx == mn: return [1.0] * len(vals)
    return [(v - mn) / (mx - mn) for v in vals]

# 1. Ground truth target correlation with importance
# For each query, target has label=1, all other 499 memories have label=0.
# We can pool all (query, memory) pairs = 50,000 pairs.
labels = []
imp_values = []
rec_values = []
sim_values = []
norm_imp_values = []
norm_rec_values = []
norm_sim_values = []

m_embs = np.array([m["embedding"] for m in memories])
raw_imps = [m["importance"] for m in memories]
norm_imps = min_max_norm(raw_imps)

raw_recs = [0.995 ** (72.0 - m["timestamp_hours"]) for m in memories]
norm_recs = min_max_norm(raw_recs)

for q in queries:
    qvec = np.array(q["qvec"])
    sims = np.dot(m_embs, qvec).tolist()
    n_sims = min_max_norm(sims)
    t_id = q["target_id"]
    for idx, m in enumerate(memories):
        is_target = 1 if m["id"] == t_id else 0
        labels.append(is_target)
        imp_values.append(raw_imps[idx])
        rec_values.append(raw_recs[idx])
        sim_values.append(sims[idx])
        norm_imp_values.append(norm_imps[idx])
        norm_rec_values.append(norm_recs[idx])
        norm_sim_values.append(n_sims[idx])

labels = np.array(labels)
imp_values = np.array(imp_values)
rec_values = np.array(rec_values)
sim_values = np.array(sim_values)
norm_imp_values = np.array(norm_imp_values)
norm_rec_values = np.array(norm_rec_values)
norm_sim_values = np.array(norm_sim_values)

print("=" * 80)
print("CORRELATION WITH GROUND TRUTH TARGET LABEL (N = 50,000 query-memory pairs)")
print("=" * 80)
for name, vals in [
    ("Raw Importance", imp_values),
    ("Normalized Importance", norm_imp_values),
    ("Raw Recency", rec_values),
    ("Normalized Recency", norm_rec_values),
    ("Raw Cosine Similarity", sim_values),
    ("Normalized Cosine Similarity", norm_sim_values),
]:
    p_r, p_p = stats.pearsonr(vals, labels)
    s_r, s_p = stats.spearmanr(vals, labels)
    pb_r, pb_p = stats.pointbiserialr(labels, vals)
    print(f"{name:<30}: Pearson r = {p_r:+.6f} (p={p_p:.4e}) | Spearman rho = {s_r:+.6f} (p={s_p:.4e}) | Point-Biserial r = {pb_r:+.6f}")

# Target vs Non-target statistics
target_mask = (labels == 1)
dist_mask = (labels == 0)

print("\nTarget vs Distractor Summary Statistics:")
print(f"Target Importance:     mean={imp_values[target_mask].mean():.4f}, std={imp_values[target_mask].std():.4f}, min={imp_values[target_mask].min():.4f}, max={imp_values[target_mask].max():.4f}")
print(f"Distractor Importance: mean={imp_values[dist_mask].mean():.4f}, std={imp_values[dist_mask].std():.4f}, min={imp_values[dist_mask].min():.4f}, max={imp_values[dist_mask].max():.4f}")
print(f"Target Normalized Imp:     mean={norm_imp_values[target_mask].mean():.4f}, std={norm_imp_values[target_mask].std():.4f}")
print(f"Distractor Normalized Imp: mean={norm_imp_values[dist_mask].mean():.4f}, std={norm_imp_values[dist_mask].std():.4f}")

# How many distractors have higher importance than the target?
distractors_higher = []
distractors_higher_by_query_type = {"RECENCY_SENSITIVE": [], "RELEVANCE_DOMINANT": [], "TEMPORAL_CONFLICT": []}

for q in queries:
    t_id = q["target_id"]
    t_imp = next(m["importance"] for m in memories if m["id"] == t_id)
    higher_cnt = sum(1 for m in memories if m["id"] != t_id and m["importance"] > t_imp)
    distractors_higher.append(higher_cnt)
    distractors_higher_by_query_type[q["type"]].append(higher_cnt)

print(f"\nDistractors with strictly higher importance than target (out of 499 distractors):")
print(f"  Overall: mean={np.mean(distractors_higher):.1f} ({np.mean(distractors_higher)/499*100:.1f}%), min={np.min(distractors_higher)}, max={np.max(distractors_higher)}")
for qt, cnts in distractors_higher_by_query_type.items():
    print(f"  {qt:<20}: mean={np.mean(cnts):.1f} ({np.mean(cnts)/499*100:.1f}%), min={np.min(cnts)}, max={np.max(cnts)}")

print("\n" + "=" * 80)
print("ANATOMY OF A7 DISTRACTORS THAT BEAT THE TARGET")
print("=" * 80)
# In A7 (0.2, 0.5, 0.3):
# Target never gets rank 1. Let's look at the rank 1 distractor for each query:
rank1_components = {
    "rec_contrib": [], # 0.2 * norm_rec
    "sim_contrib": [], # 0.5 * norm_sim
    "imp_contrib": [], # 0.3 * norm_imp
    "total_score": [],
    "raw_imp": [],
    "raw_sim": [],
    "raw_rec": [],
}
target_components_a7 = {
    "rec_contrib": [],
    "sim_contrib": [],
    "imp_contrib": [],
    "total_score": [],
    "raw_imp": [],
    "raw_sim": [],
    "raw_rec": [],
}

for q in queries:
    qvec = np.array(q["qvec"])
    sims = np.dot(m_embs, qvec).tolist()
    n_sims = min_max_norm(sims)
    
    sc = [0.2 * r + 0.5 * s + 0.3 * imp for r, s, imp in zip(norm_recs, n_sims, norm_imps)]
    t_id = q["target_id"]
    t_idx = next(i for i, m in enumerate(memories) if m["id"] == t_id)
    
    ranked_idx = sorted(range(len(memories)), key=lambda i: sc[i], reverse=True)
    top1_idx = ranked_idx[0]
    
    target_components_a7["rec_contrib"].append(0.2 * norm_recs[t_idx])
    target_components_a7["sim_contrib"].append(0.5 * n_sims[t_idx])
    target_components_a7["imp_contrib"].append(0.3 * norm_imps[t_idx])
    target_components_a7["total_score"].append(sc[t_idx])
    target_components_a7["raw_imp"].append(raw_imps[t_idx])
    target_components_a7["raw_sim"].append(sims[t_idx])
    target_components_a7["raw_rec"].append(raw_recs[t_idx])
    
    rank1_components["rec_contrib"].append(0.2 * norm_recs[top1_idx])
    rank1_components["sim_contrib"].append(0.5 * n_sims[top1_idx])
    rank1_components["imp_contrib"].append(0.3 * norm_imps[top1_idx])
    rank1_components["total_score"].append(sc[top1_idx])
    rank1_components["raw_imp"].append(raw_imps[top1_idx])
    rank1_components["raw_sim"].append(sims[top1_idx])
    rank1_components["raw_rec"].append(raw_recs[top1_idx])

print(f"Target in A7:")
print(f"  Total Score:   mean={np.mean(target_components_a7['total_score']):.4f} +/- {np.std(target_components_a7['total_score']):.4f}")
print(f"  Sim Contrib:   mean={np.mean(target_components_a7['sim_contrib']):.4f} (from raw sim mean {np.mean(target_components_a7['raw_sim']):.4f})")
print(f"  Rec Contrib:   mean={np.mean(target_components_a7['rec_contrib']):.4f} (from raw rec mean {np.mean(target_components_a7['raw_rec']):.4f})")
print(f"  Imp Contrib:   mean={np.mean(target_components_a7['imp_contrib']):.4f} (from raw imp mean {np.mean(target_components_a7['raw_imp']):.4f})")

print(f"\nRank-1 Distractor in A7:")
print(f"  Total Score:   mean={np.mean(rank1_components['total_score']):.4f} +/- {np.std(rank1_components['total_score']):.4f}")
print(f"  Sim Contrib:   mean={np.mean(rank1_components['sim_contrib']):.4f} (from raw sim mean {np.mean(rank1_components['raw_sim']):.4f})")
print(f"  Rec Contrib:   mean={np.mean(rank1_components['rec_contrib']):.4f} (from raw rec mean {np.mean(rank1_components['raw_rec']):.4f})")
print(f"  Imp Contrib:   mean={np.mean(rank1_components['imp_contrib']):.4f} (from raw imp mean {np.mean(rank1_components['raw_imp']):.4f})")

diff_sim = np.mean(target_components_a7['sim_contrib']) - np.mean(rank1_components['sim_contrib'])
diff_rec = np.mean(target_components_a7['rec_contrib']) - np.mean(rank1_components['rec_contrib'])
diff_imp = np.mean(target_components_a7['imp_contrib']) - np.mean(rank1_components['imp_contrib'])
diff_tot = np.mean(target_components_a7['total_score']) - np.mean(rank1_components['total_score'])

print(f"\nComponent Advantage of Target vs Rank-1 Distractor:")
print(f"  Delta Sim (0.5*norm_sim): {diff_sim:+.4f} (Target leads by +{diff_sim:.4f})")
print(f"  Delta Rec (0.2*norm_rec): {diff_rec:+.4f} ({'Target leads' if diff_rec > 0 else 'Distractor leads'} by {abs(diff_rec):.4f})")
print(f"  Delta Imp (0.3*norm_imp): {diff_imp:+.4f} (Distractor leads by +{abs(diff_imp):.4f}!)")
print(f"  Net Total Score Delta:    {diff_tot:+.4f} (Distractor beats Target by {abs(diff_tot):.4f})")

