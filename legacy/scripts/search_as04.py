with open(r"E:\projects\simlab\curo_phase4_ablation_package.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r"AS-04", text)]
for idx in matches[:10]:
    start = max(0, idx - 100)
    end = min(len(text), idx + 200)
    print("--- MATCH ---")
    print(text[start:end])
