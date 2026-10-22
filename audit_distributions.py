import json
from pathlib import Path
import numpy as np
import scipy.stats as stats

ROOT = Path(__file__).resolve().parent
with open(ROOT / "phase3_execution" / "SimLab_MemBench_500.json", "r", encoding="utf-8") as f:
    bench = json.load(f)

memories = bench["memories"]
queries = bench["queries"]

print("=== 1. RAW COMPONENT DISTRIBUTIONS (500 MEMORIES) ===")
imps = np.array([m["importance"] for m in memories])
times = np.array([m["timestamp_hours"] for m in memories])
t_curr = 72.0
recs = 0.995 ** (t_curr - times)

# Raw importance stats
print(f"Raw Importance: min={imps.min():.4f}, max={imps.max():.4f}, mean={imps.mean():.4f}, std={imps.std():.4f}, range={imps.max()-imps.min():.4f}")
print(f"Raw Recency:    min={recs.min():.4f}, max={recs.max():.4f}, mean={recs.mean():.4f}, std={recs.std():.4f}, range={recs.max()-recs.min():.4f}")
print(f"Raw Times (h):  min={times.min():.4f}, max={times.max():.4f}, mean={times.mean():.4f}, std={times.std():.4f}")

# Quantiles
print("Importance quantiles (0, 25, 50, 75, 100):", np.percentile(imps, [0, 25, 50, 75, 100]))
print("Recency quantiles    (0, 25, 50, 75, 100):", np.percentile(recs, [0, 25, 50, 75, 100]))

# Cosine similarities across all 100 queries x 500 memories
m_embs = np.array([m["embedding"] for m in memories])
all_sims = []
target_sims = []
non_target_sims = []

for q in queries:
    qvec = np.array(q["qvec"])
    sims = np.dot(m_embs, qvec)
    all_sims.extend(sims)
    t_id = q["target_id"]
    for idx, m in enumerate(memories):
        if m["id"] == t_id:
            target_sims.append(sims[idx])
        else:
            non_target_sims.append(sims[idx])

all_sims = np.array(all_sims)
target_sims = np.array(target_sims)
non_target_sims = np.array(non_target_sims)

print(f"\nAll Cosine Sims:    min={all_sims.min():.4f}, max={all_sims.max():.4f}, mean={all_sims.mean():.4f}, std={all_sims.std():.4f}, range={all_sims.max()-all_sims.min():.4f}")
print(f"Target Cosine Sims: min={target_sims.min():.4f}, max={target_sims.max():.4f}, mean={target_sims.mean():.4f}, std={target_sims.std():.4f}")
print(f"Non-target Sims:    min={non_target_sims.min():.4f}, max={non_target_sims.max():.4f}, mean={non_target_sims.mean():.4f}, std={non_target_sims.std():.4f}")

# Now let's check NORMALIZATION behavior per query!
def min_max_norm(vals):
    mn, mx = min(vals), max(vals)
    if mx == mn: return [1.0]*len(vals)
    return [(v - mn) / (mx - mn) for v in vals]

# Per-query min-max ranges
norm_sim_ranges = []
norm_imp_ranges = []
norm_rec_ranges = []

# Check correlations between components:
corr_imp_target = []
corr_rec_target = []

# Target importance stats
target_imps = []
for q in queries:
    t_id = q["target_id"]
    t_m = [m for m in memories if m["id"] == t_id][0]
    target_imps.append(t_m["importance"])
target_imps = np.array(target_imps)

print(f"\nTarget Memories Importance: min={target_imps.min():.4f}, max={target_imps.max():.4f}, mean={target_imps.mean():.4f}, std={target_imps.std():.4f}")
print(f"All Memories Importance:    min={imps.min():.4f}, max={imps.max():.4f}, mean={imps.mean():.4f}, std={imps.std():.4f}")

# Stratified targets importance:
for t in ["RECENCY_SENSITIVE", "RELEVANCE_DOMINANT", "TEMPORAL_CONFLICT"]:
    t_q = [q for q in queries if q["type"] == t]
    t_q_imps = [next(m["importance"] for m in memories if m["id"] == q["target_id"]) for q in t_q]
    print(f"  Target Importance for {t:<20}: mean={np.mean(t_q_imps):.4f}, min={np.min(t_q_imps):.4f}, max={np.max(t_q_imps):.4f}")
