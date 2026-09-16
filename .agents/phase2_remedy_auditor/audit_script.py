import os
import re
import sys

SIMLAB_ROOT = r"E:\projects\simlab"
RD_DIR = os.path.join(SIMLAB_ROOT, "reproduction_design")
MASTER_PKG = os.path.join(SIMLAB_ROOT, "curo_reproduction_design_package.md")
AGENTS_DIR = os.path.join(SIMLAB_ROOT, ".agents")

print("=== STARTING COMPREHENSIVE FORENSIC AUDIT ===")

# CHECK 1: ZERO RUNTIME CODE AUDIT
print("\n--- CHECK 1: ZERO RUNTIME CODE AUDIT ---")
forbidden_extensions = {".c", ".cpp", ".rs", ".go", ".java", ".js", ".ts", ".sh", ".bat", ".ps1"}
forbidden_dirs = {"smallville", "chatdev", "agent_hospital", "agentverse", "engine", "simulator", "src", "app"}

non_agent_files = []
for root, dirs, files in os.walk(SIMLAB_ROOT):
    if ".agents" in root:
        continue
    for f in files:
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, SIMLAB_ROOT)
        non_agent_files.append((rel_path, full_path))

print(f"Total non-agent files in workspace: {len(non_agent_files)}")
for rel_path, full_path in sorted(non_agent_files):
    size = os.path.getsize(full_path)
    mtime = os.path.getmtime(full_path)
    print(f"  {rel_path} ({size} bytes)")

# Check for forbidden extensions in workspace
code_files = [r for r, f in non_agent_files if os.path.splitext(r)[1].lower() in forbidden_extensions or (os.path.splitext(r)[1].lower() == '.py' and r != 'test_empirical_challenges.py')]
print(f"Code files with forbidden extensions in non-agent workspace: {code_files}")

# Inspect test_empirical_challenges.py
test_py = os.path.join(SIMLAB_ROOT, "test_empirical_challenges.py")
if os.path.exists(test_py):
    with open(test_py, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"test_empirical_challenges.py size: {len(content)} chars. First 3 lines:")
    for line in content.splitlines()[:3]:
        print(f"    {line}")
    mtime = os.path.getmtime(test_py)
    print(f"test_empirical_challenges.py mtime: {mtime}")

# Check RD files extensions
rd_files = os.listdir(RD_DIR) if os.path.exists(RD_DIR) else []
non_md_in_rd = [f for f in rd_files if not f.endswith(".md")]
print(f"reproduction_design file count: {len(rd_files)}. Non-md files: {non_md_in_rd}")

# Check forbidden directories
found_forbidden_dirs = []
for d in forbidden_dirs:
    if os.path.exists(os.path.join(SIMLAB_ROOT, d)):
        found_forbidden_dirs.append(d)
print(f"Forbidden engine directories found: {found_forbidden_dirs}")


# CHECK 2: ZERO UNAUTHORIZED EXECUTION AUDIT
print("\n--- CHECK 2: ZERO UNAUTHORIZED EXECUTION AUDIT ---")
exec_extensions = {".log", ".jsonl", ".sqlite", ".sqlite3", ".db", ".pkl", ".bin", ".npy", ".npz", ".pt", ".pth"}
found_exec_files = []
for root, dirs, files in os.walk(SIMLAB_ROOT):
    # Allow git if any, but check workspace
    if ".git" in root:
        continue
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in exec_extensions:
            found_exec_files.append(os.path.relpath(os.path.join(root, f), SIMLAB_ROOT))

print(f"Execution/telemetry files found ({len(found_exec_files)}): {found_exec_files}")

# Check for .env or credentials
cred_patterns = [r"\.env", r".*credential.*", r".*secret.*", r".*key.*"]
found_creds = []
for root, dirs, files in os.walk(SIMLAB_ROOT):
    if ".git" in root:
        continue
    for f in files:
        for p in cred_patterns:
            if re.match(p, f, re.IGNORECASE) and not f.endswith(".md") and not f.endswith(".py"):
                found_creds.append(os.path.relpath(os.path.join(root, f), SIMLAB_ROOT))
print(f"Potential credential files found: {found_creds}")

# Check execution_authority declarations in RD-05 to RD-08
for num in ["05", "06", "07", "08"]:
    fname = [f for f in rd_files if f.startswith(f"RD-{num}")][0]
    fpath = os.path.join(RD_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"###\s+35\.\s*execution_authority.*?\n+(.*?)\n", text, re.IGNORECASE)
    auth_val = m.group(1).strip() if m else "NOT_FOUND"
    print(f"  {fname}: execution_authority = {auth_val}")


# CHECK 3: ANTI-FABRICATION & ANTI-CHEATING AUDIT
print("\n--- CHECK 3: ANTI-FABRICATION & ANTI-CHEATING AUDIT ---")
# Check placeholder tokens across all RD files and master package
forbidden_tokens = ["TODO", "TBD", "FIXME", "placeholder", "xxx"]
placeholder_findings = []

target_files_to_check = [(os.path.join(RD_DIR, f), f) for f in rd_files if f.endswith(".md")]
target_files_to_check.append((MASTER_PKG, "curo_reproduction_design_package.md"))

for path, name in target_files_to_check:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        for tok in forbidden_tokens:
            # Case insensitive search for tokens
            matches = re.finditer(r"\b" + re.escape(tok) + r"\b", line, re.IGNORECASE)
            for match in matches:
                matched_str = match.group(0)
                placeholder_findings.append({
                    "file": name,
                    "line_num": idx,
                    "token": tok,
                    "matched": matched_str,
                    "content": line.strip()
                })

print(f"Placeholder token occurrences found: {len(placeholder_findings)}")
for p in placeholder_findings:
    print(f"  [{p['file']}:{p['line_num']}] matched '{p['matched']}': {p['content']}")

# Check 35 schema fields in RD-05..RD-08
schema_check_results = {}
for num in ["05", "06", "07", "08"]:
    fname = [f for f in rd_files if f.startswith(f"RD-{num}")][0]
    fpath = os.path.join(RD_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    fields = [int(m.group(1)) for m in re.finditer(r"###\s+(\d+)\.", text)]
    missing = [i for i in range(1, 36) if i not in fields]
    schema_check_results[fname] = {
        "field_count": len(fields),
        "missing_fields": missing,
        "first_field": fields[0] if fields else None,
        "last_field": fields[-1] if fields else None
    }
    print(f"  {fname}: {len(fields)}/35 fields present. Missing: {missing}")


# CHECK 4: MASTER PACKAGE CONGRUENCE
print("\n--- CHECK 4: MASTER PACKAGE CONGRUENCE ---")
with open(MASTER_PKG, "r", encoding="utf-8") as f:
    master_content = f.read()

print(f"Master package length: {len(master_content)} characters, {len(master_content.splitlines())} lines")

congruence_results = {}
for f in sorted(rd_files):
    if not f.endswith(".md"):
        continue
    fpath = os.path.join(RD_DIR, f)
    with open(fpath, "r", encoding="utf-8") as file_handle:
        file_content = file_handle.read().strip()
    
    # Check exact substring
    is_exact_substring = file_content in master_content
    
    # If not exact substring, find where differences are
    congruence_results[f] = {
        "length": len(file_content),
        "exact_in_master": is_exact_substring
    }
    print(f"  {f} ({len(file_content)} chars): in master = {is_exact_substring}")


# CHECK 5: GOVERNANCE INVARIANT AUDIT
print("\n--- CHECK 5: GOVERNANCE INVARIANT AUDIT ---")
# Check ARCHITECTURE_STATUS, IMPLEMENTATION_AUTHORITY, EXPERIMENT_EXECUTION_AUTHORITY
gov_findings = {}
for path, name in target_files_to_check:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    
    arch_frozen = re.findall(r"ARCHITECTURE_STATUS\s*[:=]\s*(\w+)", text, re.IGNORECASE)
    impl_auth = re.findall(r"IMPLEMENTATION_AUTHORITY\s*[:=]\s*([^\n\r]+)", text, re.IGNORECASE)
    exp_auth = re.findall(r"EXPERIMENT_EXECUTION_AUTHORITY\s*[:=]\s*([^\n\r]+)", text, re.IGNORECASE)
    
    gov_findings[name] = {
        "arch_status": arch_frozen,
        "impl_auth": impl_auth,
        "exp_auth": exp_auth
    }

print("Governance check sample (RD-01, RD-05, RD-16, Master):")
for k in ["RD-01_reproduction_priority_matrix.md", "RD-05_rp01_experiment_design.md", "RD-16_gate_r2_package.md", "curo_reproduction_design_package.md"]:
    if k in gov_findings:
        print(f"  {k}: {gov_findings[k]}")

# Check any occurrence of "FROZEN" not preceded by "UN"
frozen_violations = []
for path, name in target_files_to_check:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        # Look for ARCHITECTURE_STATUS = FROZEN or similar
        m = re.search(r"ARCHITECTURE_STATUS\s*[:=]\s*(?<!UN)FROZEN\b", line, re.IGNORECASE)
        if m:
            frozen_violations.append((name, idx, line.strip()))
print(f"Frozen violations found: {frozen_violations}")

print("\n=== AUDIT RUN COMPLETED ===")
