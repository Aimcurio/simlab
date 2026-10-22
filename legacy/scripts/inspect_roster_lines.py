with open(r"E:\projects\simlab\curo_phase4_ablation_package.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "EXP-AB-02-REP" in l or "EXP-AB-01-REFL" in l:
        print(f"{i+1}: {l.strip()}")
