import os
import sys
import re
import datetime
import glob
from pathlib import Path

BASE_DIR = Path("E:/projects/simlab")
RD_DIR = BASE_DIR / "reproduction_design"
MASTER_PKG = BASE_DIR / "curo_reproduction_design_package.md"
AGENTS_DIR = BASE_DIR / ".agents"

def log(section, msg):
    print(f"[{section}] {msg}")

def check_timeline():
    log("PHASE A - TIMELINE", "Auditing file modification dates and agent logs...")
    # List files in RD_DIR
    rd_files = sorted(list(RD_DIR.glob("RD-*.md")))
    log("PHASE A", f"Found {len(rd_files)} RD files.")
    for f in rd_files:
        st = f.stat()
        mtime = datetime.datetime.fromtimestamp(st.st_mtime).isoformat()
        log("PHASE A", f"  {f.name}: size={st.st_size} bytes, mtime={mtime}")
    
    # Master package
    if MASTER_PKG.exists():
        st = MASTER_PKG.stat()
        mtime = datetime.datetime.fromtimestamp(st.st_mtime).isoformat()
        log("PHASE A", f"  Master pkg {MASTER_PKG.name}: size={st.st_size} bytes, mtime={mtime}")
    else:
        log("PHASE A", "  ERROR: Master package missing!")

    # Check agents
    phase2_agents = sorted([p for p in AGENTS_DIR.glob("phase2_*") if p.is_dir()])
    log("PHASE A", f"Found {len(phase2_agents)} phase2 agent folders:")
    for ag in phase2_agents:
        handoff = ag / "handoff.md"
        progress = ag / "progress.md"
        h_exists = handoff.exists()
        h_size = handoff.stat().st_size if h_exists else 0
        h_mtime = datetime.datetime.fromtimestamp(handoff.stat().st_mtime).isoformat() if h_exists else "N/A"
        log("PHASE A", f"  Agent {ag.name}: handoff={h_exists} ({h_size} bytes, mtime={h_mtime})")

def check_integrity():
    log("PHASE B - INTEGRITY", "Checking for prohibited patterns and placeholders...")
    placeholder_patterns = [
        re.compile(r"\bTODO\b", re.IGNORECASE),
        re.compile(r"\bTBD\b"),
        re.compile(r"\bFIXME\b", re.IGNORECASE),
        re.compile(r"\bPLACEHOLDER\b", re.IGNORECASE),
        re.compile(r"\[insert\b", re.IGNORECASE),
        re.compile(r"\[to be\b", re.IGNORECASE),
        re.compile(r"\[pending\b", re.IGNORECASE),
        re.compile(r"<placeholder>", re.IGNORECASE)
    ]
    
    findings = []
    rd_files = sorted(list(RD_DIR.glob("RD-*.md"))) + ([MASTER_PKG] if MASTER_PKG.exists() else [])
    for f in rd_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        for line_num, line in enumerate(content.splitlines(), 1):
            for pat in placeholder_patterns:
                if pat.search(line):
                    # Check if it's discussing the avoidance of TODO/TBD or an actual placeholder
                    findings.append((f.name, line_num, line.strip()))
    
    log("PHASE B", f"Placeholder scan matches: {len(findings)}")
    for fn, ln, text in findings[:20]:
        log("PHASE B", f"  {fn}:{ln} -> {text[:100]}")
    if len(findings) > 20:
        log("PHASE B", f"  ... and {len(findings)-20} more.")

    # Check for runtime code
    py_files = list(BASE_DIR.glob("*.py")) + list(BASE_DIR.glob("**/*.py"))
    py_files = [p for p in py_files if ".agents" not in str(p)]
    log("PHASE B", f"Python files in simlab (outside .agents): {[str(p.relative_to(BASE_DIR)) for p in py_files]}")

def check_schema_35_fields():
    log("PHASE C - INVARIANT 2", "Auditing 35-field schema across RP-01 to RP-04...")
    rp_files = {
        "RP-01": RD_DIR / "RD-05_rp01_experiment_design.md",
        "RP-02": RD_DIR / "RD-06_rp02_experiment_design.md",
        "RP-03": RD_DIR / "RD-07_rp03_experiment_design.md",
        "RP-04": RD_DIR / "RD-08_rp04_experiment_design.md"
    }
    
    # Expected 35 fields from Phase 2 specification
    expected_fields = [
        "candidate_id",
        "candidate_name",
        "source_primitive_id",
        "source_system_reference",
        "target_claim",
        "falsifiable_hypothesis",
        "null_hypothesis",
        "independent_variables",
        "dependent_variables",
        "controlled_variables",
        "confound_mitigations",
        "baseline_specifications",
        "compute_matching_protocol",
        "experimental_environment",
        "task_suite_workload",
        "sample_size_justification",
        "statistical_analysis_plan",
        "reproducibility_telemetry_requirements",
        "pre_registered_failure_modes",
        "pre_registered_success_criteria",
        "pre_registered_inconclusive_criteria",
        "prng_seeding_protocol",
        "model_api_freeze_protocol",
        "context_caching_defense",
        "token_budget_upper_bound",
        "financial_cost_upper_bound",
        "wall_clock_timeout_limits",
        "human_evaluation_protocol",
        "evaluator_bias_defenses",
        "code_artifact_requirements",
        "execution_safety_sandbox",
        "decision_thresholds_for_phase3",
        "consequence_of_failure",
        "consequence_of_success",
        "governance_signoff_matrix"
    ]
    
    log("PHASE C", f"Required schema field count: {len(expected_fields)}")
    
    for rp_id, rp_path in rp_files.items():
        if not rp_path.exists():
            log("PHASE C", f"ERROR: {rp_id} file {rp_path.name} does not exist!")
            continue
        content = rp_path.read_text(encoding="utf-8", errors="replace")
        present_fields = []
        missing_fields = []
        for fld in expected_fields:
            # Match field as header or bold or bullet or key
            # e.g., "**1. candidate_id**", "### 1. candidate_id", "candidate_id:", etc.
            pattern = re.compile(rf"(?:^|[\*\#\-\s\d\.\(\)]){re.escape(fld)}(?:[\*\#\:\s]|$)", re.IGNORECASE | re.MULTILINE)
            if pattern.search(content):
                present_fields.append(fld)
            else:
                missing_fields.append(fld)
        log("PHASE C", f"{rp_id} ({rp_path.name}): {len(present_fields)}/35 fields found.")
        if missing_fields:
            log("PHASE C", f"  MISSING in {rp_id}: {missing_fields}")

def check_forward_constraints():
    log("PHASE C - INVARIANT 6", "Auditing NC-01 through NC-30 in RD-15...")
    rd15_path = RD_DIR / "RD-15_lessons_learned_forward_constraints.md"
    if not rd15_path.exists():
        log("PHASE C", "ERROR: RD-15 missing!")
        return
    content = rd15_path.read_text(encoding="utf-8", errors="replace")
    found_nc = []
    missing_nc = []
    for i in range(1, 31):
        nc_id = f"NC-{i:02d}"
        if re.search(rf"\b{nc_id}\b", content):
            found_nc.append(nc_id)
        else:
            missing_nc.append(nc_id)
    log("PHASE C", f"Forward constraints found: {len(found_nc)}/30")
    if missing_nc:
        log("PHASE C", f"  MISSING NCs: {missing_nc}")

def check_gate_r2():
    log("PHASE C - INVARIANT 5", "Auditing Gate R2 Package in RD-16...")
    rd16_path = RD_DIR / "RD-16_gate_r2_package.md"
    if not rd16_path.exists():
        log("PHASE C", "ERROR: RD-16 missing!")
        return
    content = rd16_path.read_text(encoding="utf-8", errors="replace")
    outcomes = ["CONTINUE_REPRODUCTION_DESIGN", "INSUFFICIENT_EXPERIMENT_DESIGN", "READY_FOR_REPRODUCTION_EXECUTION"]
    found_outcomes = [o for o in outcomes if o in content]
    log("PHASE C", f"Outcomes mentioned in RD-16: {found_outcomes}")
    for line in content.splitlines():
        if "gate r2 outcome" in line.lower() or "gate decision" in line.lower() or "verdict" in line.lower():
            log("PHASE C", f"  {line.strip()}")

def check_governance():
    log("PHASE C - INVARIANT 4", "Auditing Governance Boundaries across files...")
    target_files = [MASTER_PKG, RD_DIR / "RD-16_gate_r2_package.md", RD_DIR / "RD-15_lessons_learned_forward_constraints.md"]
    for tf in target_files:
        if not tf.exists(): continue
        txt = tf.read_text(encoding="utf-8", errors="replace")
        for phrase in ["Architecture Status", "Implementation Authority", "Experiment Execution Authority", "Reproduction Execution Authority"]:
            matches = [l.strip() for l in txt.splitlines() if phrase.lower() in l.lower()]
            for m in matches[:3]:
                log("PHASE C", f"  [{tf.name}] {m}")

def check_controls_and_baselines():
    log("PHASE C - INVARIANT 3", "Auditing Controls, Baselines, and FM-01 to FM-12...")
    # Check FM-01 to FM-12
    rd11_path = RD_DIR / "RD-11_failure_confound_register.md"
    if rd11_path.exists():
        txt = rd11_path.read_text(encoding="utf-8", errors="replace")
        fms = [f"FM-{i:02d}" for i in range(1, 13)]
        found_fms = [f for f in fms if f in txt]
        log("PHASE C", f"Found {len(found_fms)}/12 failure modes in RD-11: {found_fms}")
    
    # Check B1-SC dual control in RD-04 and RD-06
    for fn in ["RD-04_baseline_compute_matching.md", "RD-06_rp02_experiment_design.md"]:
        fp = RD_DIR / fn
        if fp.exists():
            txt = fp.read_text(encoding="utf-8", errors="replace")
            has_call_matched = "call-matched" in txt.lower() or "b_{1-sc-calls}" in txt.lower() or "b1-sc-calls" in txt.lower()
            has_token_matched = "token-matched" in txt.lower() or "b_{1-sc-tokens}" in txt.lower() or "b1-sc-tokens" in txt.lower()
            log("PHASE C", f"  [{fn}] call-matched: {has_call_matched}, token-matched: {has_token_matched}")

if __name__ == "__main__":
    print("=== STARTING INDEPENDENT AUDIT SCRIPT ===")
    check_timeline()
    print("-" * 60)
    check_integrity()
    print("-" * 60)
    check_schema_35_fields()
    print("-" * 60)
    check_forward_constraints()
    print("-" * 60)
    check_gate_r2()
    print("-" * 60)
    check_governance()
    print("-" * 60)
    check_controls_and_baselines()
    print("=== AUDIT SCRIPT COMPLETE ===")
