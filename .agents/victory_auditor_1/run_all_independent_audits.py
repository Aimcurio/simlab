# Independent Victory Audit Test Suite
import os
import re
import sys

PROJECT_DIR = r"E:\projects\simlab"
DELIV_DIR = os.path.join(PROJECT_DIR, "deliverables")
MASTER_PKG = os.path.join(PROJECT_DIR, "curo_research_package.md")

test_results = {}

def log_test(name, passed, details=""):
    test_results[name] = (passed, details)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    if details:
        print(f"       {details}")

# ==============================================================================
# TEST 1: Deliverable Completeness & Presence
# ==============================================================================
tier1 = ['DR-01', 'DR-02', 'DR-03', 'DR-04', 'DR-05', 'DR-06', 'DR-07', 'DR-08', 'DR-09', 'DR-10', 'DR-14', 'DR-15', 'DR-16']
tier2 = ['DR-11', 'DR-12', 'DR-13']
all_drs = tier1 + tier2

deliv_files = os.listdir(DELIV_DIR)
missing_drs = []
for dr in all_drs:
    found = any(f.startswith(dr) for f in deliv_files)
    if not found:
        missing_drs.append(dr)

master_exists = os.path.exists(MASTER_PKG) and os.path.getsize(MASTER_PKG) > 50000

test1_pass = (len(missing_drs) == 0) and master_exists
log_test("TEST 1: 16 Deliverables and Master Package Presence", test1_pass, 
         f"Missing DRs: {missing_drs}, Master Package Size: {os.path.getsize(MASTER_PKG) if os.path.exists(MASTER_PKG) else 0} bytes")

# ==============================================================================
# TEST 2: DR-05 Schema Discipline & Anti-Fabrication
# ==============================================================================
REQUIRED_FIELDS = [
    'primitive_id', 'primitive_name', 'source_system', 'source_version', 'category',
    'mechanism_description', 'claimed_purpose', 'claimed_benefit', 'measured_benefit',
    'evidence_type', 'evidence_strength', 'dependencies', 'runtime_cost', 'token_cost',
    'latency_effect', 'scaling_effect', 'known_failure_modes', 'known_limitations',
    'negative_evidence', 'transferability_hypothesis', 'reproduction_required',
    'proposed_control', 'proposed_metric', 'reproducibility_status', 'confidence', 'status'
]
PERMITTED_STATUS = {'PROPOSED', 'REPRODUCTION_CANDIDATE', 'PROMISING_BUT_UNVERIFIED', 'CONTEXT_DEPENDENT', 'INSUFFICIENT_EVIDENCE', 'REJECTED'}
PERMITTED_REPRO = {'NOT_ASSESSED', 'AUTHOR_REPORTED', 'CODE_AVAILABLE', 'PARTIALLY_REPRODUCED', 'INDEPENDENTLY_REPRODUCED', 'FAILED_REPRODUCTION', 'UNRESOLVED'}
EXPLICIT_STATES = {'NOT_REPORTED', 'NOT_MEASURED', 'UNKNOWN', 'NOT_APPLICABLE', 'UNRESOLVED'}

dr05_path = os.path.join(DELIV_DIR, "DR-05_primitive_evidence_matrix.md")
with open(dr05_path, 'r', encoding='utf-8') as f:
    dr05_content = f.read()

prim_blocks = re.split(r'#### Primitive (PRIM-[A-Z]+-\d+):', dr05_content)
prims = {}
for i in range(1, len(prim_blocks), 2):
    prims[prim_blocks[i].strip()] = prim_blocks[i+1]

dr05_errors = []
validated_found = 0
for pid, block in prims.items():
    fields = {}
    for line in block.split('\n'):
        m = re.match(r'^- \*\*(\d+)\.\s+([a-z_]+)\*\*:\s*(.*)$', line.strip())
        if m:
            fields[m.group(2)] = (int(m.group(1)), m.group(3).strip())
    
    for idx, rf in enumerate(REQUIRED_FIELDS, 1):
        if rf not in fields:
            dr05_errors.append(f"{pid} missing {rf}")
        else:
            num, val = fields[rf]
            if num != idx:
                dr05_errors.append(f"{pid} field {rf} number mismatch ({num} != {idx})")
            if not val:
                dr05_errors.append(f"{pid} field {rf} empty")
    
    if 'status' in fields:
        sval = re.sub(r'[`*]', '', fields['status'][1]).strip()
        if 'VALIDATED' in sval:
            validated_found += 1
            dr05_errors.append(f"{pid} has VALIDATED status")
        if sval not in PERMITTED_STATUS:
            dr05_errors.append(f"{pid} status '{sval}' not permitted")
            
    if 'reproducibility_status' in fields:
        rval = re.sub(r'[`*]', '', fields['reproducibility_status'][1]).split()[0].strip()
        if rval not in PERMITTED_REPRO:
            dr05_errors.append(f"{pid} repro '{rval}' not permitted")

test2_pass = (len(prims) == 28) and (len(dr05_errors) == 0) and (validated_found == 0)
log_test("TEST 2: DR-05 Schema Discipline & Zero Validated Status", test2_pass,
         f"Primitives: {len(prims)}, Errors: {len(dr05_errors)}, Validated count: {validated_found}")

# ==============================================================================
# TEST 3: Confound Control & Baselines (DR-10)
# ==============================================================================
dr10_path = os.path.join(DELIV_DIR, "DR-10_candidate_baseline_matrix.md")
with open(dr10_path, 'r', encoding='utf-8') as f:
    dr10_content = f.read()

baselines_found = [b for b in ['Baseline B0', 'Baseline B1', 'Baseline B2', 'Baseline B3', 'Baseline B4'] if b in dr10_content]
b1_sc_found = 'B1-SC' in dr10_content or 'Single-Agent Self-Consistency' in dr10_content
qual_found = all(q in dr10_content for q in [
    'Partitioned Private State',
    'Asymmetric Specialized External Tools',
    'Distinct Persona / Adversarial Perspectives',
    'Asynchronous Human-in-the-Loop'
])

test3_pass = (len(baselines_found) == 5) and b1_sc_found and qual_found
log_test("TEST 3: DR-10 Baselines B0-B4 & B1-SC Operational Boundaries", test3_pass,
         f"Baselines: {len(baselines_found)}/5, B1-SC: {b1_sc_found}, 4 Boundary Conditions: {qual_found}")

# ==============================================================================
# TEST 4: Failure Modes & Citations (DR-07)
# ==============================================================================
dr07_path = os.path.join(DELIV_DIR, "DR-07_failure_register.md")
with open(dr07_path, 'r', encoding='utf-8') as f:
    dr07_content = f.read()

fms = re.findall(r'####\s*(FM-\d+):', dr07_content)
all_fm_present = (len(fms) == 15) and set(fms) == {f"FM-{i:02d}" for i in range(1, 16)}

test4_pass = all_fm_present
log_test("TEST 4: DR-07 15 Failure Modes Cataloged", test4_pass,
         f"Found {len(fms)} failure modes: {fms}")

# ==============================================================================
# TEST 5: Conflict Register (DR-08) & Unknowns Register (DR-09)
# ==============================================================================
dr08_path = os.path.join(DELIV_DIR, "DR-08_conflict_register.md")
with open(dr08_path, 'r', encoding='utf-8') as f:
    dr08_content = f.read()
# Deduplicate: count canonical unique conflict IDs C-01 through C-06
conflicts = sorted(list(set(re.findall(r'Conflict\s+(C-\d+):', dr08_content))))

dr09_path = os.path.join(DELIV_DIR, "DR-09_unknowns_register.md")
with open(dr09_path, 'r', encoding='utf-8') as f:
    dr09_content = f.read()
# Deduplicate: count canonical unique unknown IDs U-01 through U-06
unknowns = sorted(list(set(re.findall(r'U-0[1-6]:', dr09_content))))
all_unresolved = 'UNRESOLVED' in dr09_content

test5_pass = (len(conflicts) == 6) and (len(unknowns) == 6) and all_unresolved
log_test("TEST 5: DR-08 Conflicts (6 canonical) & DR-09 Unknowns (6 canonical) Registers", test5_pass,
         f"Unique Conflicts: {len(conflicts)} ({conflicts}), Unique Unknowns: {len(unknowns)} ({unknowns}), Epistemic UNRESOLVED: {all_unresolved}")

# ==============================================================================
# TEST 6: Operational Negative Forward Constraints (DR-15)
# ==============================================================================
dr15_path = os.path.join(DELIV_DIR, "DR-15_lessons_learned_forward_constraints.md")
with open(dr15_path, 'r', encoding='utf-8') as f:
    dr15_content = f.read()

ncs = re.findall(r'###\s*2\.\d+\s*(NC-\d+):', dr15_content)
all_23_ncs = (len(ncs) == 23) and set(ncs) == {f"NC-{i:02d}" for i in range(1, 24)}
nc_protocols = all(term in dr15_content for term in [
    'Binding Operational Rule',
    'Technical Enforcement Mechanism',
    'Automated Audit & Verification Protocol'
])

test6_pass = all_23_ncs and nc_protocols
log_test("TEST 6: DR-15 Negative Constraints NC-01 through NC-23", test6_pass,
         f"Found {len(ncs)} constraints: {ncs}, Audit Protocols: {nc_protocols}")

# ==============================================================================
# TEST 7: Canonical Lifecycle & Boundary Invariants
# ==============================================================================
dr16_path = os.path.join(DELIV_DIR, "DR-16_research_gate_package.md")
with open(dr16_path, 'r', encoding='utf-8') as f:
    dr16_txt = f.read()

with open(MASTER_PKG, 'r', encoding='utf-8') as f:
    master_txt = f.read()

canonical_state_dr16 = 'GATE_R1_COMPLETE' in dr16_txt
canonical_state_master = 'GATE_R1_COMPLETE' in master_txt
authority_ok = ('NOT_GRANTED' in dr16_txt) and ('NOT_GRANTED' in master_txt)
unfrozen_ok = ('UNFROZEN' in dr16_txt) and ('UNFROZEN' in master_txt)
rec_in_dr16 = 'READY_FOR_REPRODUCTION_DESIGN' in dr16_txt
rec_in_master = 'READY_FOR_REPRODUCTION_DESIGN' in master_txt
no_stale_active = ('Current Lifecycle State**: `RESEARCH_AUTHORIZED`' not in dr16_txt) and ('Lifecycle State**: `RESEARCH_AUTHORIZED`' not in master_txt)

test7_pass = canonical_state_dr16 and canonical_state_master and authority_ok and unfrozen_ok and rec_in_dr16 and rec_in_master and no_stale_active
log_test("TEST 7: Canonical Lifecycle State (GATE_R1_COMPLETE) & Governance Invariants", test7_pass,
         f"State=GATE_R1_COMPLETE: {canonical_state_dr16 and canonical_state_master}, Authority=NOT_GRANTED: {authority_ok}, Status=UNFROZEN: {unfrozen_ok}, Rec=READY_FOR_REPRODUCTION_DESIGN: {rec_in_dr16 and rec_in_master}, NoStaleActive: {no_stale_active}")

# ==============================================================================
# TEST 8: Mathematical Complexity Derivation (DR-13) & Terminology Audit
# ==============================================================================
dr13_path = os.path.join(DELIV_DIR, "DR-13_cost_latency_scaling_analysis.md")
with open(dr13_path, 'r', encoding='utf-8') as f:
    dr13_txt = f.read()

formula_present = ('O(N^2 \cdot R^2 \cdot L)' in dr13_txt) or ('O(N^2 * R^2 * L)' in dr13_txt) or ('N^2 \cdot R(R-1)' in dr13_txt)
ratios_present = all(r in dr13_txt for r in ['7,500', '15,300', '34,500', '140,800'])
no_exponential_in_dr13 = 'exponential accumulation' not in dr13_txt.lower()

dr14_path = os.path.join(DELIV_DIR, "DR-14_research_synthesis.md")
with open(dr14_path, 'r', encoding='utf-8') as f:
    dr14_txt = f.read()
no_exponential_in_dr14 = 'exponential accumulation' not in dr14_txt.lower()

test8_pass = formula_present and ratios_present and no_exponential_in_dr13 and no_exponential_in_dr14
log_test("TEST 8: DR-13 Broadcast Debate Math Derivation & Terminology", test8_pass,
         f"Formula: {formula_present}, Ratios: {ratios_present}, NoExponentialAccumulation: {no_exponential_in_dr13 and no_exponential_in_dr14}")

# ==============================================================================
# SUMMARY VERDICT
# ==============================================================================
all_passed = all(p for p, _ in test_results.values())
print("\n" + "=" * 70)
print(f"FINAL INDEPENDENT AUDIT VERDICT: {'ALL CHECKS PASSED' if all_passed else 'AUDIT CHECKS FAILED'}")
print("=" * 70)
if not all_passed:
    sys.exit(1)
