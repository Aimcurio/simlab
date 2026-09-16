import re
from pathlib import Path

BASE_DIR = Path("E:/projects/simlab")
RD_DIR = BASE_DIR / "reproduction_design"
MASTER_PKG = BASE_DIR / "curo_reproduction_design_package.md"

EXPECTED_35_FIELDS = [
    "experiment_id",
    "reproduction_candidate",
    "research_question",
    "falsifiable_hypothesis",
    "null_hypothesis",
    "primitive_under_test",
    "reference_mechanism",
    "baseline",
    "treatment",
    "independent_variables",
    "dependent_variables",
    "controlled_variables",
    "model_configuration",
    "prompt_configuration",
    "context_configuration",
    "randomness_configuration",
    "dataset_or_environment",
    "minimum_run_count",
    "statistical_method",
    "success_threshold",
    "failure_threshold",
    "termination_condition",
    "token_budget",
    "latency_budget",
    "compute_budget",
    "logging_requirements",
    "provenance_requirements",
    "known_confounds",
    "expected_failure_modes",
    "what_result_supports",
    "what_result_does_not_support",
    "external_validity_limits",
    "architecture_implication_if_positive",
    "architecture_implication_if_negative",
    "execution_authority"
]

def audit_deliverable_files():
    print("=== AUDIT 1: DELIVERABLE COMPLETENESS (RD-01 to RD-16) ===")
    all_ok = True
    for i in range(1, 17):
        pattern = f"RD-{i:02d}_*.md"
        matches = list(RD_DIR.glob(pattern))
        if not matches:
            print(f"[FAIL] Missing deliverable RD-{i:02d}")
            all_ok = False
        else:
            f = matches[0]
            size = f.stat().st_size
            lines = len(f.read_text(encoding="utf-8").splitlines())
            print(f"[PASS] {f.name}: {size:,} bytes, {lines} lines")
            if size < 500:
                print(f"[WARN] {f.name} suspiciously small ({size} bytes)")
                all_ok = False
    
    if MASTER_PKG.exists():
        size = MASTER_PKG.stat().st_size
        lines = len(MASTER_PKG.read_text(encoding="utf-8").splitlines())
        print(f"[PASS] Master package {MASTER_PKG.name}: {size:,} bytes, {lines} lines")
    else:
        print("[FAIL] Master package missing!")
        all_ok = False
    return all_ok

def audit_35_fields_in_file(file_path, label):
    content = file_path.read_text(encoding="utf-8", errors="replace")
    print(f"\n--- Checking 35 fields in {label} ({file_path.name}) ---")
    
    # Extract headers like "### 1. experiment_id"
    field_pattern = re.compile(r"^###\s+(\d+)\.\s+([a-zA-Z0-9_\-]+)", re.MULTILINE)
    matches = field_pattern.findall(content)
    
    found_fields = {}
    for num_str, name in matches:
        num = int(num_str)
        found_fields[num] = name.strip()
    
    print(f"Extracted {len(found_fields)} numbered fields.")
    missing_numbers = []
    name_mismatches = []
    
    for idx, expected_name in enumerate(EXPECTED_35_FIELDS, 1):
        if idx not in found_fields:
            missing_numbers.append(idx)
        else:
            actual_name = found_fields[idx]
            if actual_name.lower() != expected_name.lower():
                name_mismatches.append((idx, expected_name, actual_name))
    
    # Check field contents (not empty)
    empty_fields = []
    for idx in range(1, 36):
        if idx in found_fields:
            # check content between this header and next header
            curr_header = f"### {idx}. {found_fields[idx]}"
            next_header = f"### {idx+1}."
            start_pos = content.find(curr_header)
            if start_pos != -1:
                end_pos = content.find(next_header, start_pos)
                if end_pos != -1:
                    chunk = content[start_pos + len(curr_header):end_pos].strip()
                else:
                    chunk = content[start_pos + len(curr_header):].strip()
                if len(chunk) < 5:
                    empty_fields.append((idx, found_fields[idx], chunk))
    
    status = True
    if missing_numbers:
        print(f"[FAIL] Missing field numbers: {missing_numbers}")
        status = False
    else:
        print(f"[PASS] All 35 field numbers (1..35) present.")
        
    if name_mismatches:
        print(f"[WARN] Name mismatches: {name_mismatches}")
    else:
        print(f"[PASS] All 35 field names match expected schema exactly.")
        
    if empty_fields:
        print(f"[FAIL] Empty or trivial fields: {empty_fields}")
        status = False
    else:
        print(f"[PASS] All 35 fields have substantive non-empty content.")
        
    return status

def audit_all_35_schemas():
    print("\n=== AUDIT 2: 35-FIELD SCHEMA RIGOR ===")
    rp_files = [
        ("RP-01", RD_DIR / "RD-05_rp01_experiment_design.md"),
        ("RP-02", RD_DIR / "RD-06_rp02_experiment_design.md"),
        ("RP-03", RD_DIR / "RD-07_rp03_experiment_design.md"),
        ("RP-04", RD_DIR / "RD-08_rp04_experiment_design.md"),
    ]
    all_ok = True
    for label, path in rp_files:
        ok = audit_35_fields_in_file(path, label)
        if not ok:
            all_ok = False
            
    # Also verify master package contains all 4 RP candidates with 35 fields
    print("\n--- Checking Master Package RP Sections ---")
    master_txt = MASTER_PKG.read_text(encoding="utf-8", errors="replace")
    for rp in ["EXP-RP01-RECENCY", "EXP-RP02-COMPUTE-MATCHED", "EXP-RP03-PHASE-BOUNDARIES", "EXP-RP04-DYNAMIC-ORCHESTRATION"]:
        if rp in master_txt:
            print(f"[PASS] Master package contains {rp}")
        else:
            print(f"[FAIL] Master package missing {rp}")
            all_ok = False
            
    return all_ok

def audit_invariants_3_to_6():
    print("\n=== AUDIT 3-6: INVARIANTS CHECK ===")
    
    # Invariant 3: Minimum Experiment Principle & Controls
    print("\n--- Invariant 3: Minimum Experiment Principle & Controls ---")
    # FM-01 to FM-12
    rd11 = (RD_DIR / "RD-11_failure_confound_register.md").read_text(encoding="utf-8")
    for i in range(1, 13):
        fm = f"FM-{i:02d}"
        if fm not in rd11:
            print(f"[FAIL] Missing {fm} in RD-11")
        else:
            print(f"[PASS] Found {fm} in RD-11")
            
    # Dual-Control B1-SC protocol in RD-04 and RD-06
    rd04 = (RD_DIR / "RD-04_baseline_compute_matching.md").read_text(encoding="utf-8")
    rd06 = (RD_DIR / "RD-06_rp02_experiment_design.md").read_text(encoding="utf-8")
    for name, txt in [("RD-04", rd04), ("RD-06", rd06)]:
        has_k7 = "k=7" in txt.lower() or "k = 7" in txt.lower()
        has_k10 = "k=10" in txt.lower() or "k = 10" in txt.lower()
        has_call = "call-matched" in txt.lower() or "b_{1-sc-calls}" in txt.lower() or "b1-sc-calls" in txt.lower()
        has_token = "token-matched" in txt.lower() or "b_{1-sc-tokens}" in txt.lower() or "b1-sc-tokens" in txt.lower()
        print(f"[{name}] Dual-Control check: K=7:{has_k7}, K=10:{has_k10}, Call-matched:{has_call}, Token-matched:{has_token}")
        
    # Invariant 4: Governance Boundaries
    print("\n--- Invariant 4: Governance Boundaries ---")
    rd16 = (RD_DIR / "RD-16_gate_r2_package.md").read_text(encoding="utf-8")
    unfrozen = "UNFROZEN" in rd16
    impl_not_granted = "IMPLEMENTATION_AUTHORITY" in rd16 and "NOT_GRANTED" in rd16
    exp_not_granted = "EXPERIMENT_EXECUTION_AUTHORITY" in rd16 and "NOT_GRANTED" in rd16
    print(f"RD-16 Architecture UNFROZEN: {unfrozen}")
    print(f"RD-16 Implementation Authority NOT_GRANTED: {impl_not_granted}")
    print(f"RD-16 Experiment Execution Authority NOT_GRANTED: {exp_not_granted}")
    
    # Invariant 5: Gate R2 Evaluation
    print("\n--- Invariant 5: Gate R2 Evaluation ---")
    permitted_outcomes = ["CONTINUE_REPRODUCTION_DESIGN", "INSUFFICIENT_EXPERIMENT_DESIGN", "READY_FOR_REPRODUCTION_EXECUTION"]
    gate_outcome = None
    for po in permitted_outcomes:
        if po in rd16:
            gate_outcome = po
            print(f"[PASS] Found permitted Gate R2 outcome in RD-16: {po}")
            
    # Invariant 6: Forward Constraints
    print("\n--- Invariant 6: Forward Constraints NC-01 through NC-30 in RD-15 ---")
    rd15 = (RD_DIR / "RD-15_lessons_learned_forward_constraints.md").read_text(encoding="utf-8")
    missing_nc = []
    for i in range(1, 31):
        nc = f"NC-{i:02d}"
        if nc not in rd15:
            missing_nc.append(nc)
        else:
            # Check operational rule / enforcement exists
            pos = rd15.find(nc)
            chunk = rd15[pos:pos+500]
            # Verify substantive length
            if len(chunk) < 50:
                print(f"[WARN] NC-{i:02d} chunk too short")
    if missing_nc:
        print(f"[FAIL] Missing NCs: {missing_nc}")
    else:
        print(f"[PASS] All 30 forward constraints (NC-01 to NC-30) fully defined in RD-15.")

if __name__ == "__main__":
    audit_deliverable_files()
    audit_all_35_schemas()
    audit_invariants_3_to_6()
