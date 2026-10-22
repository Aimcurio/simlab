import os

files_to_check = [
    r"E:\projects\simlab\curo_phase4_ablation_package.md",
    r"E:\projects\simlab\ablation_design\AS-01_ablation_priority_matrix.md",
    r"E:\projects\simlab\deliverables\DR-11_reproduction_candidate_list.md"
]

for f in files_to_check:
    if os.path.exists(f):
        print(f"=== {f} ===")
        with open(f, "r", encoding="utf-8") as fp:
            c = fp.read()
            for exp in ["EXP-AB-02-REP", "EXP-AB-01-REFL", "EXP-AB-01-COMP"]:
                print(f"  Count of {exp}: {c.count(exp)}")
