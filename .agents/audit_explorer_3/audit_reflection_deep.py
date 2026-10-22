import json
import numpy as np

with open(r"E:\projects\simlab\phase3_execution\SimLab_MemBench_500.json", "r", encoding="utf-8") as f:
    bench = json.load(f)

memories = bench["memories"]
queries = bench["queries"]

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
            'timestamp_hours': latest_t,
            'importance': 8.5,
            'embedding': centroid.tolist(),
            'is_reflection': True
        })

all_mems = memories + refl_nodes

refl_sims = []
epis_sims = []
t_curr = 72.0

for q in queries:
    qvec = np.array(q['qvec'])
    for r in refl_nodes:
        refl_sims.append(float(np.dot(qvec, np.array(r['embedding']))))
    for m in memories:
        epis_sims.append(float(np.dot(qvec, np.array(m['embedding']))))

refl_recs = [0.995 ** (t_curr - r['timestamp_hours']) for r in refl_nodes]
epis_recs = [0.995 ** (t_curr - m['timestamp_hours']) for m in memories]

print("=== RAW COMPARISON: REFLECTION VS EPISODIC ===")
print(f"Reflection Count: {len(refl_nodes)}, Episodic Count: {len(memories)}")
print(f"Reflection Importance: min={min(r['importance'] for r in refl_nodes)}, max={max(r['importance'] for r in refl_nodes)}, mean={np.mean([r['importance'] for r in refl_nodes]):.4f}, std={np.std([r['importance'] for r in refl_nodes]):.4f}")
print(f"Episodic Importance:   min={min(m['importance'] for m in memories)}, max={max(m['importance'] for m in memories)}, mean={np.mean([m['importance'] for m in memories]):.4f}, std={np.std([m['importance'] for m in memories]):.4f}")
print(f"Reflection Recency:    min={min(refl_recs):.4f}, max={max(refl_recs):.4f}, mean={np.mean(refl_recs):.4f}, std={np.std(refl_recs):.4f}")
print(f"Episodic Recency:      min={min(epis_recs):.4f}, max={max(epis_recs):.4f}, mean={np.mean(epis_recs):.4f}, std={np.std(epis_recs):.4f}")
print(f"Reflection Cosine Sim: min={min(refl_sims):.4f}, max={max(refl_sims):.4f}, mean={np.mean(refl_sims):.4f}, std={np.std(refl_sims):.4f}")
print(f"Episodic Cosine Sim:   min={min(epis_sims):.4f}, max={max(epis_sims):.4f}, mean={np.mean(epis_sims):.4f}, std={np.std(epis_sims):.4f}")

# Normalized score comparison per query
def min_max_norm(vals):
    mn, mx = min(vals), max(vals)
    if mx == mn: return [1.0]*len(vals)
    return [(v - mn) / (mx - mn) for v in vals]

# In A8 scoring: alpha=0.2, beta=0.5, gamma=0.3
all_imps = [m['importance'] for m in all_mems]
norm_imps = min_max_norm(all_imps)

refl_total_scores = []
epis_total_scores = []
target_ranks = []
refl_in_top5 = []
refl_rank1 = []

for q_idx, q in enumerate(queries):
    qvec = np.array(q['qvec'])
    sims = [float(np.dot(qvec, np.array(m['embedding']))) for m in all_mems]
    recs = [0.995 ** (t_curr - m['timestamp_hours']) for m in all_mems]
    norm_sims = min_max_norm(sims)
    norm_recs = min_max_norm(recs)
    
    scores = [0.2*r + 0.5*s + 0.3*imp for r, s, imp in zip(norm_recs, norm_sims, norm_imps)]
    
    ranked_indices = sorted(range(len(all_mems)), key=lambda i: scores[i], reverse=True)
    t_id = q['target_id']
    t_cand_idx = next(i for i, m in enumerate(all_mems) if m['id'] == t_id)
    t_rank = ranked_indices.index(t_cand_idx) + 1
    target_ranks.append(t_rank)
    
    top5 = ranked_indices[:5]
    refl_top5_count = sum(1 for i in top5 if all_mems[i].get('is_reflection', False))
    refl_in_top5.append(refl_top5_count)
    refl_rank1.append(all_mems[ranked_indices[0]].get('is_reflection', False))

print("\n=== A8 RETRIEVAL BEHAVIOR ===")
print(f"Mean Target Rank: {np.mean(target_ranks):.2f}")
print(f"Target Rank min={min(target_ranks)}, max={max(target_ranks)}, median={np.median(target_ranks)}")
print(f"MRR: {np.mean([1.0/r for r in target_ranks]):.4f}")
print(f"Rank-1 Reflection Crowding: {sum(refl_rank1)}/{len(queries)} ({sum(refl_rank1)/len(queries)*100:.1f}%)")
print(f"Total Reflection Nodes in Top-5 across all queries: {sum(refl_in_top5)} / {5 * len(queries)}")

# Now what if reflections had REALISTIC importance (e.g. mean of cluster, or 5.0)?
print("\n=== COUNTERFACTUAL EXPERIMENT 1: Realistic Reflection Importance (imp = 5.0) ===")
all_mems_cf1 = [dict(m) for m in all_mems]
for m in all_mems_cf1:
    if m.get('is_reflection'):
        m['importance'] = 5.0

all_imps_cf1 = [m['importance'] for m in all_mems_cf1]
norm_imps_cf1 = min_max_norm(all_imps_cf1)

target_ranks_cf1 = []
refl_in_top5_cf1 = []
refl_rank1_cf1 = []

for q in queries:
    qvec = np.array(q['qvec'])
    sims = [float(np.dot(qvec, np.array(m['embedding']))) for m in all_mems_cf1]
    recs = [0.995 ** (t_curr - m['timestamp_hours']) for m in all_mems_cf1]
    norm_sims = min_max_norm(sims)
    norm_recs = min_max_norm(recs)
    scores = [0.2*r + 0.5*s + 0.3*imp for r, s, imp in zip(norm_recs, norm_sims, norm_imps_cf1)]
    ranked_indices = sorted(range(len(all_mems_cf1)), key=lambda i: scores[i], reverse=True)
    t_id = q['target_id']
    t_cand_idx = next(i for i, m in enumerate(all_mems_cf1) if m['id'] == t_id)
    target_ranks_cf1.append(ranked_indices.index(t_cand_idx) + 1)
    refl_rank1_cf1.append(all_mems_cf1[ranked_indices[0]].get('is_reflection', False))
    refl_in_top5_cf1.append(sum(1 for i in ranked_indices[:5] if all_mems_cf1[i].get('is_reflection', False)))

print(f"MRR with imp=5.0: {np.mean([1.0/r for r in target_ranks_cf1]):.4f}")
print(f"Rank-1 Reflection Crowding with imp=5.0: {sum(refl_rank1_cf1)}/{len(queries)} ({sum(refl_rank1_cf1)/len(queries)*100:.1f}%)")
print(f"Total Reflection Nodes in Top-5: {sum(refl_in_top5_cf1)} / 500")

# Counterfactual 2: No importance weighting (gamma=0, alpha=0.3, beta=0.7) on A8 pool
print("\n=== COUNTERFACTUAL EXPERIMENT 2: A4 Weights on A8 Pool (alpha=0.3, beta=0.7, gamma=0.0) ===")
target_ranks_cf2 = []
refl_in_top5_cf2 = []
refl_rank1_cf2 = []

for q in queries:
    qvec = np.array(q['qvec'])
    sims = [float(np.dot(qvec, np.array(m['embedding']))) for m in all_mems]
    recs = [0.995 ** (t_curr - m['timestamp_hours']) for m in all_mems]
    norm_sims = min_max_norm(sims)
    norm_recs = min_max_norm(recs)
    scores = [0.3*r + 0.7*s for r, s in zip(norm_recs, norm_sims)]
    ranked_indices = sorted(range(len(all_mems)), key=lambda i: scores[i], reverse=True)
    t_id = q['target_id']
    t_cand_idx = next(i for i, m in enumerate(all_mems) if m['id'] == t_id)
    target_ranks_cf2.append(ranked_indices.index(t_cand_idx) + 1)
    refl_rank1_cf2.append(all_mems[ranked_indices[0]].get('is_reflection', False))
    refl_in_top5_cf2.append(sum(1 for i in ranked_indices[:5] if all_mems[i].get('is_reflection', False)))

print(f"MRR with alpha=0.3, beta=0.7, gamma=0: {np.mean([1.0/r for r in target_ranks_cf2]):.4f}")
print(f"Rank-1 Reflection Crowding: {sum(refl_rank1_cf2)}/{len(queries)} ({sum(refl_rank1_cf2)/len(queries)*100:.1f}%)")
print(f"Total Reflection Nodes in Top-5: {sum(refl_in_top5_cf2)} / 500")

# Counterfactual 3: What if queries could legitimately target reflections, or reflection admission control?
print("\n=== COUNTERFACTUAL EXPERIMENT 3: Ground Truth Eligibility Analysis ===")
print("Are reflection node IDs ever present in queries target_id?")
all_target_ids = set(q['target_id'] for q in queries)
refl_ids = set(r['id'] for r in refl_nodes)
overlap = all_target_ids.intersection(refl_ids)
print(f"Overlap between benchmark targets and reflection nodes: {len(overlap)} (Expected: 0)")
