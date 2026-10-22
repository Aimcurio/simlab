import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
with open(ROOT / "phase3_execution" / "SimLab_MemBench_500.json", "r", encoding="utf-8") as f:
    bench = json.load(f)

memories = bench["memories"]
queries = bench["queries"]

imps = np.array([m["importance"] for m in memories])

distractors_higher_importance = []
for q in queries:
    t_id = q["target_id"]
    t_imp = next(m["importance"] for m in memories if m["id"] == t_id)
    higher_count = sum(1 for m in memories if m["importance"] > t_imp)
    distractors_higher_importance.append(higher_count)

print("Number of distractors with HIGHER importance than the target:")
print(f"Mean count: {np.mean(distractors_higher_importance):.1f} / 500 memories ({np.mean(distractors_higher_importance)/500*100:.1f}%)")
print(f"Min count:  {np.min(distractors_higher_importance)}")
print(f"Max count:  {np.max(distractors_higher_importance)}")
print(f"Median count: {np.median(distractors_higher_importance)}")
