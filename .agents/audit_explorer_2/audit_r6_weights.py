import json
import hashlib
import os

AS03_PATH = r"E:\projects\simlab\ablation_design\AS-03_memory_ablation_plan.md"
RESULTS_PATH = r"E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_results.json"
HARNESS_PATH = r"E:\projects\simlab\run_exp_ab_01_comp.py"

with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    res = json.load(f)

# Expected weights from AS-03 Section 2:
# Condition Code | Condition Name | Scoring Formulation
# A1: RECENCY_ONLY -> s = s_rec = lambda^Delta t -> (1.0, 0.0, 0.0)
# A2: RELEVANCE_ONLY -> s = s_rel = cos(q, m) -> (0.0, 1.0, 0.0)
# A3: IMPORTANCE_ONLY -> s = s_imp = score_prompt -> (0.0, 0.0, 1.0)
# A4: RECENCY_RELEVANCE -> s = 0.3 s_rec + 0.7 s_rel -> (0.3, 0.7, 0.0)
# A5: RECENCY_IMPORTANCE -> s = 0.5 s_rec + 0.5 s_imp -> (0.5, 0.0, 0.5)
# A6: RELEVANCE_IMPORTANCE -> s = 0.7 s_rel + 0.3 s_imp -> (0.0, 0.7, 0.3)
# A7: FULL_TRI_FACTOR -> s = 0.2 s_rec + 0.5 s_rel + 0.3 s_imp -> (0.2, 0.5, 0.3)
# A8: TRI_FACTOR_REFLECTION -> A7 scoring over memory store including 20% synthesized reflection nodes -> (0.2, 0.5, 0.3)

EXPECTED = {
    "A1": {"name": "RECENCY_ONLY", "weights": [1.0, 0.0, 0.0], "pool": "base (500)"},
    "A2": {"name": "RELEVANCE_ONLY", "weights": [0.0, 1.0, 0.0], "pool": "base (500)"},
    "A3": {"name": "IMPORTANCE_ONLY", "weights": [0.0, 0.0, 1.0], "pool": "base (500)"},
    "A4": {"name": "RECENCY_RELEVANCE", "weights": [0.3, 0.7, 0.0], "pool": "base (500)"},
    "A5": {"name": "RECENCY_IMPORTANCE", "weights": [0.5, 0.0, 0.5], "pool": "base (500)"},
    "A6": {"name": "RELEVANCE_IMPORTANCE", "weights": [0.0, 0.7, 0.3], "pool": "base (500)"},
    "A7": {"name": "FULL_TRI_FACTOR", "weights": [0.2, 0.5, 0.3], "pool": "base (500)"},
    "A8": {"name": "TRI_FACTOR_REFLECTION", "weights": [0.2, 0.5, 0.3], "pool": "augmented (600: 500 base + 100 refl)"},
}

executed_summaries = res["condition_summaries"]

print("=" * 100)
print(f"{'Condition':<10} | {'Condition Name':<23} | {'Expected Weights (AS-03)':<25} | {'Executed Weights (Harness)':<25} | {'Match?':<6}")
print("-" * 100)

all_match = True
for code in ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"]:
    exp = EXPECTED[code]
    exec_entry = executed_summaries[code]
    exec_weights = [round(w, 2) for w in exec_entry["weights"]]
    exp_weights = [round(w, 2) for w in exp["weights"]]
    
    match = (exp_weights == exec_weights) and (exp["name"] == exec_entry["condition_name"])
    if not match:
        all_match = False
    print(f"{code:<10} | {exp['name']:<23} | {str(exp['weights']):<25} | {str(exec_weights):<25} | {str(match):<6}")

print("-" * 100)
print(f"Overall Weight Configuration Match: {all_match}")
drift_status = "EXPERIMENT_CONFIGURATION_DRIFT_DETECTED" if not all_match else "NO_EXPERIMENT_CONFIGURATION_DRIFT"
print(f"Drift Determination: {drift_status}")

# Also verify telemetry integrity and dataset SHA256:
print("\nDataset & Telemetry Integrity:")
print(f"Dataset SHA-256 in Results:   {res['dataset']['sha256']}")
expected_ds_sha = "97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800"
actual_ds_sha = hashlib.sha256(open(r"E:\projects\simlab\phase3_execution\SimLab_MemBench_500.json", "rb").read()).hexdigest()
print(f"Actual Dataset SHA-256:       {actual_ds_sha} -> Match: {actual_ds_sha == expected_ds_sha}")

telemetry_path = res['telemetry']['file']
actual_tel_sha = hashlib.sha256(open(telemetry_path, "rb").read()).hexdigest()
print(f"Recorded Telemetry SHA-256:   {res['telemetry']['sha256']}")
print(f"Actual Telemetry SHA-256:     {actual_tel_sha} -> Match: {actual_tel_sha == res['telemetry']['sha256']}")
print(f"Recorded Telemetry Events:    {res['telemetry']['event_count']} -> Actual: {sum(1 for _ in open(telemetry_path, 'r', encoding='utf-8'))}")
