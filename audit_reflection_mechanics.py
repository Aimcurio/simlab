import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
with open(ROOT / "phase3_execution" / "SimLab_MemBench_500.json", "r", encoding="utf-8") as f:
    bench = json.load(f)

memories = bench["memories"]
queries = bench["queries"]

# Generate the 100 reflection nodes as in A8
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
print(f"Total memories in A8: {len(all_mems)}")

# Check min-max normalization impact on episodic memories when 8.5 is included:
eps_imps = [m['importance'] for m in memories]
all_imps = [m['importance'] for m in all_mems]
print(f"Episodic importance range: [{min(eps_imps)}, {max(eps_imps)}]")
print(f"Augmented importance range: [{min(all_imps)}, {max(all_imps)}]")

# For query 0:
q0 = queries[0]
qvec = np.array(q0['qvec'])
sims = [float(np.dot(qvec, np.array(m['embedding']))) for m in all_mems]
recs = [0.995 ** (72.0 - m['timestamp_hours']) for m in all_mems]

def norm(vals):
    mn, mx = min(vals), max(vals)
    return [(v - mn) / (mx - mn) for v in vals]

n_sims = norm(sims)
n_recs = norm(recs)
n_imps = norm(all_imps)

# Look at A7 weights (alpha=0.2, beta=0.5, gamma=0.3):
scores = [0.2*r + 0.5*s + 0.3*imp for r, s, imp in zip(n_recs, n_sims, n_imps)]

# Inspect top 10 scored nodes:
top10_idx = sorted(range(len(all_mems)), key=lambda i: scores[i], reverse=True)[:10]
print("\nTop 10 Nodes for Query 0 under A8:")
for rank, idx in enumerate(top10_idx, 1):
    m = all_mems[idx]
    is_refl = m.get('is_reflection', False)
    print(f"Rank {rank:2d}: ID={m['id']:<15} | is_refl={is_refl} | TotalScore={scores[idx]:.4f} | imp_norm={n_imps[idx]:.4f} | sim_norm={n_sims[idx]:.4f} | rec_norm={n_recs[idx]:.4f}")

# What if gamma = 0.0 (no importance in A8)?
scores_no_imp = [0.3*r + 0.7*s for r, s in zip(n_recs, n_sims)]
top10_no_imp = sorted(range(len(all_mems)), key=lambda i: scores_no_imp[i], reverse=True)[:10]
print("\nTop 10 Nodes for Query 0 under A8 with NO IMPORTANCE (gamma=0, alpha=0.3, beta=0.7):")
for rank, idx in enumerate(top10_no_imp, 1):
    m = all_mems[idx]
    is_refl = m.get('is_reflection', False)
    print(f"Rank {rank:2d}: ID={m['id']:<15} | is_refl={is_refl} | TotalScore={scores_no_imp[idx]:.4f} | sim_norm={n_sims[idx]:.4f} | rec_norm={n_recs[idx]:.4f}")
