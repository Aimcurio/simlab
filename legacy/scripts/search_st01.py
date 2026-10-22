with open(r"E:\projects\simlab\curo_phase4_ablation_package.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r"EXP-ST-01-SCALE", text)]
for idx in matches:
    start = max(0, idx - 150)
    end = min(len(text), idx + 250)
    print("--- MATCH ---")
    print(text[start:end])
