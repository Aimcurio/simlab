import json
import numpy as np

with open(r"E:\projects\simlab\phase3_execution\SimLab_MemBench_500.json", "r", encoding="utf-8") as f:
    bench = json.load(f)

memories = bench["memories"]
queries = bench["queries"]

# Check for identical scores
def min_max_norm(vals):
    mn, mx = min(vals), max(vals)
    if mx == mn: return [1.0] * len(vals)
    return [(v - mn) / (mx - mn) for v in vals]

for cond_name, (a, b, c) in [("A1", (1,0,0)), ("A2", (0,1,0)), ("A3", (0,0,1)), ("A4", (0.3, 0.7, 0)), ("A7", (0.2, 0.5, 0.3))]:
    ties_count = 0
    for q in queries:
        qvec = np.array(q["qvec"])
        sims = np.dot(np.array([m["embedding"] for m in memories]), qvec)
        imps = [m["importance"] for m in memories]
        recs = [0.995 ** (72.0 - m["timestamp_hours"]) for m in memories]
        sc = [a*r + b*s + c*imp for r, s, imp in zip(min_max_norm(recs), min_max_norm(sims), min_max_norm(imps))]
        if len(sc) != len(set(sc)):
            ties_count += 1
    print(f"Condition {cond_name}: queries with at least one score tie: {ties_count} / 100")
