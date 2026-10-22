with open(r"E:\projects\simlab\ablation_design\AS-12_statistical_power_plan.md", "r", encoding="utf-8") as f:
    text = f.read()
import re
for m in re.finditer(r"(non-inferiority|tost|wilcoxon|margin)", text, re.IGNORECASE):
    s = max(0, m.start() - 100)
    e = min(len(text), m.end() + 100)
    print("--- MATCH ---")
    print(text[s:e])
