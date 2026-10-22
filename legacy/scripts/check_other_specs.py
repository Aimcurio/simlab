import os

for f in ["AS-01_ablation_priority_matrix.md", "AS-11_system_level_stress_matrix.md", "AS-18_primitive_advancement_contract.md"]:
    path = os.path.join(r"E:\projects\simlab\ablation_design", f)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fp:
            text = fp.read()
            for kw in ["adaptive", "EXP-ST-01", "surviving", "winning"]:
                if kw in text:
                    print(f"File {f}: found '{kw}'")
