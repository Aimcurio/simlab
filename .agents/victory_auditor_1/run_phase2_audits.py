"""
Curo SimLab Phase 2 Deterministic Verification Audit Suite
Audits all 16 deliverables (RD-01 to RD-16), 35-field schemas, and Curo authority boundaries.
"""

import os
import re
import sys

RD_DIR = r"E:\projects\simlab\reproduction_design"
MASTER_PKG = r"E:\projects\simlab\curo_reproduction_design_package.md"

REQUIRED_DELIVERABLES = [
    "RD-01_reproduction_priority_matrix.md",
    "RD-02_candidate_unknown_mapping.md",
    "RD-03_experimental_hypothesis_register.md",
    "RD-04_baseline_compute_matching.md",
    "RD-05_rp01_experiment_design.md",
    "RD-06_rp02_experiment_design.md",
    "RD-07_rp03_experiment_design.md",
    "RD-08_rp04_experiment_design.md",
    "RD-09_metrics_evaluation_contract.md",
    "RD-10_reproducibility_telemetry_contract.md",
    "RD-11_failure_confound_register.md",
    "RD-12_cost_token_latency_budget.md",
    "RD-13_execution_isolation_plan.md",
    "RD-14_independent_review.md",
    "RD-15_lessons_learned_forward_constraints.md",
    "RD-16_gate_r2_package.md",
]

SCHEMA_35_FIELDS = [
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
    "execution_authority",
]

def test_deliverable_presence():
    print("TEST SUITE 1: Deliverable File Presence & Size")
    missing = []
    too_small = []
    for f in REQUIRED_DELIVERABLES:
        path = os.path.join(RD_DIR, f)
        if not os.path.exists(path):
            missing.append(f)
        else:
            size = os.path.getsize(path)
            if size < 1000:
                too_small.append((f, size))
            else:
                print(f"  [PASS] {f} ({size} bytes)")
    assert not missing, f"Missing deliverables: {missing}"
    assert not too_small, f"Deliverables too small: {too_small}"
    assert os.path.exists(MASTER_PKG), "Missing master package curo_reproduction_design_package.md"
    print(f"  [PASS] Master package present ({os.path.getsize(MASTER_PKG)} bytes)\n")

def test_35_field_schemas():
    print("TEST SUITE 2: 35-Field Experiment Specification Schema Audit")
    exp_files = [
        "RD-05_rp01_experiment_design.md",
        "RD-06_rp02_experiment_design.md",
        "RD-07_rp03_experiment_design.md",
        "RD-08_rp04_experiment_design.md",
    ]
    for f in exp_files:
        path = os.path.join(RD_DIR, f)
        with open(path, "r", encoding="utf-8") as inf:
            content = inf.read()
        missing_fields = []
        for idx, field in enumerate(SCHEMA_35_FIELDS, 1):
            pattern = rf"(?:###\s+{idx}\.\s+{field}|`?{field}`?:)"
            if not re.search(pattern, content, re.IGNORECASE):
                # fallback check
                if field not in content:
                    missing_fields.append(field)
        if missing_fields:
            print(f"  [FAIL] {f} missing {len(missing_fields)} fields: {missing_fields}")
            assert False, f"{f} missing required schema fields"
        else:
            print(f"  [PASS] {f}: All 35 schema fields verified present")
    print()

def test_authority_invariants():
    print("TEST SUITE 3: Curo Authority & Lifecycle Invariants Audit")
    exp_files = [
        "RD-05_rp01_experiment_design.md",
        "RD-06_rp02_experiment_design.md",
        "RD-07_rp03_experiment_design.md",
        "RD-08_rp04_experiment_design.md",
    ]
    for f in exp_files:
        path = os.path.join(RD_DIR, f)
        with open(path, "r", encoding="utf-8") as inf:
            content = inf.read()
        # Verify execution_authority is NOT_GRANTED
        match = re.search(r"###\s+35\.\s+execution_authority\s*\n+`?([A-Z_]+)`?", content)
        assert match, f"Could not parse execution_authority in {f}"
        val = match.group(1)
        assert val == "NOT_GRANTED", f"{f} execution_authority is '{val}', expected 'NOT_GRANTED'"
        print(f"  [PASS] {f}: execution_authority == NOT_GRANTED")

    # Verify Gate R2 package outcome
    gate_r2_path = os.path.join(RD_DIR, "RD-16_gate_r2_package.md")
    with open(gate_r2_path, "r", encoding="utf-8") as inf:
        gate_content = inf.read()
    assert "READY_FOR_REPRODUCTION_EXECUTION" in gate_content, "RD-16 missing outcome READY_FOR_REPRODUCTION_EXECUTION"
    assert "UNFROZEN" in gate_content, "RD-16 missing ARCHITECTURE_STATUS: UNFROZEN"
    assert "GATE_R2_COMPLETE" in gate_content, "RD-16 missing LIFECYCLE_STATE: GATE_R2_COMPLETE"
    print("  [PASS] RD-16 Gate R2 Package: Lifecycle & Outcome verified canonical")
    print()

def test_forward_constraints():
    print("TEST SUITE 4: Operational Forward Constraints Audit (NC-01 through NC-30)")
    rd15_path = os.path.join(RD_DIR, "RD-15_lessons_learned_forward_constraints.md")
    with open(rd15_path, "r", encoding="utf-8") as inf:
        content = inf.read()
    for i in range(1, 31):
        tag = f"NC-{i:02d}"
        assert tag in content, f"Missing negative constraint {tag} in RD-15"
    print("  [PASS] All 30 forward constraints (NC-01 through NC-30) verified present\n")

def test_zero_simulation_code():
    print("TEST SUITE 5: Zero Simulator Code / Firewall Audit")
    # Verify no simulation engines or game environments created in simlab root
    forbidden_dirs = ["smallville", "chatdev", "agent_hospital", "agentverse", "engine", "simulator"]
    for d in forbidden_dirs:
        path = os.path.join(r"E:\projects\simlab", d)
        assert not os.path.exists(path), f"Forbidden implementation directory found: {path}"
    print("  [PASS] Zero simulator runtime directories found; firewall intact\n")

def run_all():
    print("=" * 70)
    print("STARTING CURO SIMLAB PHASE 2 INDEPENDENT DETERMINISTIC AUDIT")
    print("=" * 70)
    test_deliverable_presence()
    test_35_field_schemas()
    test_authority_invariants()
    test_forward_constraints()
    test_zero_simulation_code()
    print("=" * 70)
    print("ALL 5 PHASE 2 AUDIT SUITES PASSED (100% VERIFIED)")
    print("=" * 70)

if __name__ == "__main__":
    run_all()
