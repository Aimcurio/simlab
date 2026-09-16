import os
import re

deliv_dir = r"E:\projects\simlab\deliverables"
files = [os.path.join(deliv_dir, f) for f in os.listdir(deliv_dir)]
files.append(r"E:\projects\simlab\curo_research_package.md")

print(f"Auditing lifecycle invariants across {len(files)} files...")

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, encoding="utf-8") as f:
        text = f.read()

    # 1. Lifecycle State
    assert "RESEARCH_AUTHORIZED" in text, f"{fname} missing RESEARCH_AUTHORIZED"
    
    # 2. Implementation Authority
    assert "NOT_GRANTED" in text, f"{fname} missing NOT_GRANTED"
    
    # 3. Check for any unauthorized execution or code writing claims
    assert not re.search(r"IMPLEMENTATION_AUTHORITY\s*=\s*GRANTED", text, re.IGNORECASE), f"{fname} has GRANTED authority!"

# 4. Check Architecture Status in DR-14, DR-16, and curo_research_package.md
for doc in ["DR-14_research_synthesis.md", "DR-16_research_gate_package.md"]:
    with open(os.path.join(deliv_dir, doc), encoding="utf-8") as f:
        t = f.read()
        assert "UNFROZEN" in t, f"{doc} missing UNFROZEN architecture status"

with open(r"E:\projects\simlab\curo_research_package.md", encoding="utf-8") as f:
    t = f.read()
    assert "UNFROZEN" in t, "curo_research_package.md missing UNFROZEN architecture status"

# 5. Check Gate R1 recommendation in DR-16 and curo_research_package.md
permitted_outcomes = {"CONTINUE_RESEARCH", "INSUFFICIENT_EVIDENCE", "READY_FOR_REPRODUCTION_DESIGN"}

with open(os.path.join(deliv_dir, "DR-16_research_gate_package.md"), encoding="utf-8") as f:
    dr16 = f.read()
    assert "READY_FOR_REPRODUCTION_DESIGN" in dr16, "DR-16 missing READY_FOR_REPRODUCTION_DESIGN"

with open(r"E:\projects\simlab\curo_research_package.md", encoding="utf-8") as f:
    crp = f.read()
    assert "READY_FOR_REPRODUCTION_DESIGN" in crp, "curo_research_package.md missing READY_FOR_REPRODUCTION_DESIGN"

print("SUCCESS: All lifecycle invariants, architecture statuses, and Gate R1 recommendations verified!")
