import os
import re

SIMLAB_ROOT = r"E:\projects\simlab"
AGENTS_DIR = os.path.join(SIMLAB_ROOT, ".agents")
RD_DIR = os.path.join(SIMLAB_ROOT, "reproduction_design")

print("=== DEEP DIVE 1: AGENTS DIRECTORY CODE & ARTIFACT AUDIT ===")
agent_files = []
agent_code_files = []
agent_exec_artifacts = []
for root, dirs, files in os.walk(AGENTS_DIR):
    for f in files:
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, SIMLAB_ROOT)
        ext = os.path.splitext(f)[1].lower()
        if ext in {".py", ".sh", ".ps1", ".bat", ".exe", ".js", ".ts", ".c", ".cpp"}:
            agent_code_files.append((rel_path, full_path, os.path.getsize(full_path)))
        if ext in {".log", ".jsonl", ".sqlite", ".db", ".csv", ".tsv"}:
            agent_exec_artifacts.append((rel_path, full_path, os.path.getsize(full_path)))

print(f"Code files in .agents: {len(agent_code_files)}")
for r, p, s in agent_code_files:
    print(f"  {r} ({s} bytes)")

print(f"Execution/log artifacts in .agents: {len(agent_exec_artifacts)}")
for r, p, s in agent_exec_artifacts:
    print(f"  {r} ({s} bytes)")


print("\n=== DEEP DIVE 2: AUTHENTICITY & SUBSTANCE OF RD-05 TO RD-08 ===")
for exp_num in ["05", "06", "07", "08"]:
    fname = [f for f in os.listdir(RD_DIR) if f.startswith(f"RD-{exp_num}")][0]
    fpath = os.path.join(RD_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"\n--- {fname} (Length: {len(text)} chars, {len(text.splitlines())} lines) ---")
    
    # Extract Experiment ID, Name, Target Mechanism, Hypothesis H1, Hypothesis H0, Sample Size, Success Threshold, Failure Threshold
    def get_section(num, title):
        pattern = rf"###\s+{num}\.\s*{title}.*?\n+(.*?)(?=\n###|\Z)"
        m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return m.group(1).strip() if m else "NOT_FOUND"

    print(f"  ID: {get_section(1, 'experiment_id')}")
    print(f"  Name: {get_section(2, 'experiment_name')}")
    print(f"  Target Primitive: {get_section(3, 'target_primitive_id')}")
    print(f"  Hypothesis H1: {get_section(6, 'falsifiable_hypothesis_h1')[:120]}...")
    print(f"  Sample Size: {get_section(14, 'sample_size_statistical_power')[:120]}...")
    print(f"  Success Threshold: {get_section(21, 'pre_registered_success_threshold')[:120]}...")
    print(f"  Failure Threshold: {get_section(22, 'pre_registered_failure_threshold')[:120]}...")
    print(f"  Inconclusive Sub-threshold: {get_section(23, 'inconclusive_outcome_handling')[:120]}...")
    print(f"  Execution Authority: {get_section(35, 'execution_authority')}")


print("\n=== DEEP DIVE 3: GATE R2 SPECIFICATION IN RD-16 ===")
rd16_path = os.path.join(RD_DIR, "RD-16_gate_r2_package.md")
with open(rd16_path, "r", encoding="utf-8") as f:
    rd16_text = f.read()

for heading in ["Lifecycle State", "Formal Gate Outcome", "Permitted Gate R2 Outcomes", "Implementation Authority", "Experiment Execution Authority", "Reproduction Execution Authority"]:
    m = re.search(rf"\*\*({heading})\*\*[:\s]+([^\n\r]+)", rd16_text, re.IGNORECASE)
    if m:
        print(f"  {m.group(1)}: {m.group(2)}")
    else:
        # try regex for table or list
        m2 = re.search(rf"\|\s*\*\*?{heading}\*\*?\s*\|\s*([^\|]+)\|", rd16_text, re.IGNORECASE)
        if m2:
            print(f"  {heading}: {m2.group(1).strip()}")
        else:
            print(f"  {heading}: NOT_FOUND")


print("\n=== DEEP DIVE 4: CURO BOUNDARY INVARIANTS ===")
# Check for any boundary violations where Curo is proposed to be simulator, engine, npc, etc.
curo_boundary_violations = []
for f in os.listdir(RD_DIR):
    if not f.endswith(".md"):
        continue
    with open(os.path.join(RD_DIR, f), "r", encoding="utf-8") as file_handle:
        for idx, line in enumerate(file_handle, 1):
            if re.search(r"Curo\s+(?:is|serves as|acts as|becomes)\s+(?:the\s+)?(?:NPC|simulator|engine|runtime|substrate|environment|benchmark target)", line, re.IGNORECASE):
                curo_boundary_violations.append((f, idx, line.strip()))
print(f"Curo boundary violations found: {curo_boundary_violations}")

print("\n=== DEEP DIVE COMPLETED ===")
