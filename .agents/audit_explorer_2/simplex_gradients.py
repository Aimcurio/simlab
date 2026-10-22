import json
import numpy as np

RESULTS_PATH = r"E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_results.json"
with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    res = json.load(f)

all_pts = res["simplex_sweep"]["all_points"]

print("Gamma Gradient across 66 Simplex Points:")
print(f"{'Gamma':<8} | {'Count':<6} | {'Mean MRR':<10} | {'Max MRR':<10} | {'Min MRR':<10}")
print("-" * 55)
for g in sorted(list(set(p["gamma"] for p in all_pts))):
    pts = [p for p in all_pts if p["gamma"] == g]
    mrrs = [p["mrr_mean"] for p in pts]
    print(f"{g:<8.1f} | {len(pts):<6} | {np.mean(mrrs):<10.4f} | {np.max(mrrs):<10.4f} | {np.min(mrrs):<10.4f}")

print("\nAlpha Gradient across 66 Simplex Points:")
print(f"{'Alpha':<8} | {'Count':<6} | {'Mean MRR':<10} | {'Max MRR':<10} | {'Min MRR':<10}")
print("-" * 55)
for a in sorted(list(set(p["alpha"] for p in all_pts))):
    pts = [p for p in all_pts if p["alpha"] == a]
    mrrs = [p["mrr_mean"] for p in pts]
    print(f"{a:<8.1f} | {len(pts):<6} | {np.mean(mrrs):<10.4f} | {np.max(mrrs):<10.4f} | {np.min(mrrs):<10.4f}")
