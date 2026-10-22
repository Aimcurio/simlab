with open(r"E:\projects\simlab\ablation_design\AS-04_memory_stress_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

for term in ["alpha", "beta", "gamma", "0.3", "0.7", "0.2", "0.5", "baseline", "winning", "adaptive", "selection", "EXP-AB-01"]:
    count = text.lower().count(term.lower())
    print(f"Term '{term}': count = {count}")
