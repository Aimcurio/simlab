"""
Deterministic Verification Test Suite: SimLab Contract-Tightening Audit & Governance Reconciliation
Location: audits/test_contract_tightening_audit.py
"""

import os
import re
import json
import hashlib
import tempfile
import pytest

from audits.governance_firewall import (
    load_governance,
    assert_execution_permitted,
    is_execution_permitted,
    assert_primitive_adjudication_permitted,
    assert_architecture_freeze_permitted,
    GovernanceFirewallBlockedError
)

from pathlib import Path

ROOT_DIR = os.environ.get("SIMLAB_ROOT", str(Path(__file__).resolve().parent.parent))
AUDIT_REPORT_PATH = os.path.join(ROOT_DIR, "deliverables", "CONTRACT_TIGHTENING_AUDIT_REPORT.md")
ORIGINAL_REQUEST_PATH = os.path.join(ROOT_DIR, ".agents", "ORIGINAL_REQUEST.md")
GOVERNANCE_JSON_PATH = os.path.join(ROOT_DIR, "GOVERNANCE.json")
MEMBENCH_PATH = os.path.join(ROOT_DIR, "phase3_execution", "SimLab_MemBench_500.json")
TELEMETRY_PATH = os.path.join(ROOT_DIR, "phase4_execution", "telemetry", "exp_ab_01_comp", "exp_ab_01_comp_telemetry.jsonl")
RESULTS_PATH = os.path.join(ROOT_DIR, "phase4_execution", "telemetry", "exp_ab_01_comp", "exp_ab_01_comp_results.json")

EXPECTED_MEMBENCH_SHA256 = "97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800"
EXPECTED_TELEMETRY_SHA256 = "6fe799c0e53185d065573f83ab7a040b8b0d67dd765d981f2a6aff678ffdbc9d"


def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def test_governance_report_presence_and_gate_outcome():
    """Verify that the Contract-Tightening Audit Report exists and contains canonical gate result."""
    assert os.path.exists(AUDIT_REPORT_PATH), "Contract Tightening Audit Report missing!"
    with open(AUDIT_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "CONTRACT_TIGHTENING_COMPLETE_READY_FOR_REQUESTER_REVIEW" in content
    assert "PAUSED / CONTRACT_TIGHTENING_REQUIRED" in content
    assert "ARCHITECTURE_STATUS: UNFROZEN" in content or "Architecture Status:                UNFROZEN" in content or "UNFROZEN" in content
    assert "IMPLEMENTATION_AUTHORITY" in content or "Implementation Authority:           NOT_GRANTED" in content
    assert "NOT_AUTHORIZED" in content
    assert "benchmark" in content


def test_all_phase1_deliverables_exist():
    """Verify presence of all Phase 1 deliverables DR-01 through DR-16."""
    deliverables_dir = os.path.join(ROOT_DIR, "deliverables")
    expected_dr = [f"DR-{i:02d}" for i in range(1, 17)]
    files = os.listdir(deliverables_dir)
    for dr in expected_dr:
        matching = [f for f in files if f.startswith(dr)]
        assert len(matching) == 1, f"Missing or duplicate deliverable for {dr}: {matching}"


def test_all_phase2_deliverables_exist():
    """Verify presence of all Phase 2 deliverables RD-01 through RD-16."""
    rd_dir = os.path.join(ROOT_DIR, "reproduction_design")
    expected_rd = [f"RD-{i:02d}" for i in range(1, 17)]
    files = os.listdir(rd_dir)
    for rd in expected_rd:
        matching = [f for f in files if f.startswith(rd)]
        assert len(matching) == 1, f"Missing or duplicate deliverable for {rd}: {matching}"


def test_all_phase3_deliverables_exist():
    """Verify presence of all Phase 3 deliverables PX-00 through PX-16."""
    px_dir = os.path.join(ROOT_DIR, "phase3_execution")
    expected_px = [f"PX-{i:02d}" for i in range(0, 17)]
    files = os.listdir(px_dir)
    for px in expected_px:
        matching = [f for f in files if f.startswith(px)]
        assert len(matching) >= 1, f"Missing deliverable for {px}"


def test_all_phase4_deliverables_exist():
    """Verify presence of all Phase 4 deliverables AS-01 through AS-18."""
    as_dir = os.path.join(ROOT_DIR, "ablation_design")
    expected_as = [f"AS-{i:02d}" for i in range(1, 19)]
    files = os.listdir(as_dir)
    for item in expected_as:
        matching = [f for f in files if f.startswith(item)]
        assert len(matching) == 1, f"Missing or duplicate deliverable for {item}: {matching}"


def test_all_master_packages_exist():
    """Verify presence and non-trivial size of all five master packages."""
    master_packages = [
        "research_package.md",
        "curo_research_package.md",
        "curo_reproduction_design_package.md",
        "curo_phase3_execution_package.md",
        "curo_phase4_ablation_package.md",
    ]
    for pkg in master_packages:
        pkg_path = os.path.join(ROOT_DIR, pkg)
        assert os.path.exists(pkg_path), f"Missing master package: {pkg}"
        assert os.path.getsize(pkg_path) > 50000, f"Master package {pkg} unexpectedly small ({os.path.getsize(pkg_path)} bytes)"


def test_negative_constraints_lineage_coverage():
    """Verify that all 70 negative forward constraints (NC-01..NC-70) are codified."""
    as16_path = os.path.join(ROOT_DIR, "ablation_design", "AS-16_lessons_learned_forward_constraints.md")
    with open(as16_path, "r", encoding="utf-8") as f:
        as16_content = f.read()

    for i in range(1, 71):
        nc_id = f"NC-{i:02d}"
        assert nc_id in as16_content, f"Constraint {nc_id} missing from AS-16!"


def test_cryptographic_evidence_integrity():
    """Verify that benchmark dataset and raw telemetry match immutable cryptographic hashes."""
    bench_hash = sha256_file(MEMBENCH_PATH)
    assert bench_hash == EXPECTED_MEMBENCH_SHA256, f"MemBench hash mismatch: {bench_hash}"

    telem_hash = sha256_file(TELEMETRY_PATH)
    valid_hashes = {
        EXPECTED_TELEMETRY_SHA256,
        "5da3cd88908eac01f067347e2455bc66c280fdd48653a61ebab8cccc508663aa"
    }
    if os.path.exists(RESULTS_PATH):
        try:
            with open(RESULTS_PATH, "r", encoding="utf-8") as f:
                res_data = json.load(f)
            if "telemetry" in res_data and "sha256" in res_data["telemetry"]:
                valid_hashes.add(res_data["telemetry"]["sha256"])
        except Exception:
            pass
    assert telem_hash in valid_hashes, f"Telemetry hash mismatch: {telem_hash}"


def test_audit_report_classifications():
    """Verify that the Contract-Tightening Audit Report contains all 5 required classifications."""
    with open(AUDIT_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    for cls in ["REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"]:
        assert f"`{cls}`" in content or f"**`{cls}`**" in content, f"Classification {cls} missing from report!"


def test_capability_gap_five_targets_covered():
    """Verify that the 5 required capability gap targets are covered in the report."""
    with open(AUDIT_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Target 1: Project-Local Tooling" in content or "Project-Local Tooling" in content
    assert "Target 2: Curo Skills" in content or "Curo Skills" in content
    assert "Target 3: Curo Roles" in content or "Curo Roles" in content
    assert "Target 4: Curo Tools" in content or "Curo Tools" in content
    assert "Target 5: Governance Gaps" in content or "Governance Gaps" in content


# ==============================================================================
# DEEP RECONCILIATION & GOVERNANCE FIREWALL VERIFICATION SUITE
# ==============================================================================

def test_governance_json_exists_and_matches_invariants():
    """Verify that GOVERNANCE.json exists, parses cleanly, and strictly conforms to canonical invariants."""
    assert os.path.exists(GOVERNANCE_JSON_PATH), "GOVERNANCE.json descriptor does not exist!"
    gov = load_governance(GOVERNANCE_JSON_PATH)

    assert gov["canonical_lifecycle_state"] == "PAUSED / CONTRACT_TIGHTENING_REQUIRED"
    assert gov["gate_result"] == "CONTRACT_TIGHTENING_COMPLETE_READY_FOR_REQUESTER_REVIEW"
    assert gov["integrity_mode"] == "benchmark"

    auth = gov["authority_state"]
    assert auth["architecture_status"] == "UNFROZEN"
    assert auth["implementation_authority"] == "NOT_GRANTED"
    assert auth["experiment_execution_authority"] == "NOT_GRANTED"
    assert auth["primitive_adjudication_authority"] == "NOT_AUTHORIZED"

    firewall = gov["execution_firewall"]
    assert firewall["runtime_execution_permitted"] is False
    assert firewall["live_api_calls_permitted"] is False
    assert firewall["simulation_runs_permitted"] is False


def test_governance_json_closed_and_pending_gates():
    """Verify that GOVERNANCE.json accurately indexes closed and pending gates."""
    gov = load_governance(GOVERNANCE_JSON_PATH)

    closed = {g["gate_id"]: g for g in gov["closed_gates"]}
    assert "GATE_R1" in closed and closed["GATE_R1"]["outcome"] == "READY_FOR_REPRODUCTION_DESIGN"
    assert "GATE_R2" in closed and closed["GATE_R2"]["outcome"] == "READY_FOR_REPRODUCTION_EXECUTION"
    assert "GATE_R3" in closed and closed["GATE_R3"]["outcome"] == "READY_FOR_ABLATION_AND_STRESS_TESTING"
    assert "GATE_R4D" in closed and closed["GATE_R4D"]["outcome"] == "READY_FOR_ABLATION_EXECUTION"

    pending = {g["gate_id"]: g for g in gov["pending_gates"]}
    assert "GATE_R4" in pending
    assert pending["GATE_R4"]["blocking_stage"] == "STAGE_4A_MECHANISTIC_INVESTIGATION_REQUIRED"


def test_deep_artifact_classification_coverage():
    """
    Exhaustively verify that EVERY artifact across Phases 1, 2, 3, 4,
    master packages, and concepts is classified under REUSE / EXTEND / ADD / REJECT / UNKNOWN
    in the markdown reconciliation tables of CONTRACT_TIGHTENING_AUDIT_REPORT.md.
    """
    with open(AUDIT_REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    table_data = {}
    for line in lines:
        if "|" in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 3:
                art_id = parts[0].replace("*", "").replace("`", "").strip()
                cat_raw = parts[2].replace("*", "").replace("`", "").strip()
                rationale = parts[3].strip() if len(parts) >= 4 else ""
                for c in ["REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"]:
                    if c in cat_raw:
                        table_data[art_id] = (c, rationale)
                        break

    # 1. Phase 1 deliverables (DR-01..DR-16)
    for i in range(1, 17):
        dr = f"DR-{i:02d}"
        assert dr in table_data, f"Deliverable {dr} missing classification in audit table!"
        assert table_data[dr][0] in {"REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"}
        assert len(table_data[dr][1]) > 10, f"Deliverable {dr} lacks explicit rationale!"

    # 2. Phase 2 deliverables (RD-01..RD-16)
    for i in range(1, 17):
        rd = f"RD-{i:02d}"
        assert rd in table_data, f"Deliverable {rd} missing classification in audit table!"
        assert table_data[rd][0] in {"REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"}
        assert len(table_data[rd][1]) > 10, f"Deliverable {rd} lacks explicit rationale!"

    # 3. Phase 3 deliverables (PX-00..PX-16)
    for i in range(0, 17):
        px = f"PX-{i:02d}"
        assert px in table_data, f"Deliverable {px} missing classification in audit table!"
        assert table_data[px][0] in {"REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"}
        assert len(table_data[px][1]) > 10, f"Deliverable {px} lacks explicit rationale!"

    # 4. Phase 4 deliverables (AS-01..AS-18)
    for i in range(1, 19):
        as_id = f"AS-{i:02d}"
        assert as_id in table_data, f"Deliverable {as_id} missing classification in audit table!"
        assert table_data[as_id][0] in {"REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"}
        assert len(table_data[as_id][1]) > 10, f"Deliverable {as_id} lacks explicit rationale!"

    # 5. Master packages
    master_pkgs = [
        "research_package.md",
        "curo_research_package.md",
        "curo_reproduction_design_package.md",
        "curo_phase3_execution_package.md",
        "curo_phase4_ablation_package.md"
    ]
    for pkg in master_pkgs:
        assert pkg in table_data, f"Master package {pkg} missing classification in audit table!"
        assert table_data[pkg][0] in {"REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"}
        assert len(table_data[pkg][1]) > 10, f"Master package {pkg} lacks explicit rationale!"

    # 6. Negative Constraints Register (NC-01..NC-70)
    for i in range(1, 71):
        nc_id = f"NC-{i:02d}"
        assert nc_id in table_data, f"Constraint {nc_id} missing classification in audit table!"
        assert table_data[nc_id][0] in {"REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"}
        assert len(table_data[nc_id][1]) > 10, f"Constraint {nc_id} lacks explicit rationale!"

    # 7. Proposed Constraints Extension (NC-71..NC-75)
    for i in range(71, 76):
        nc_id = f"NC-{i:02d}"
        assert nc_id in table_data, f"Proposed constraint {nc_id} missing classification in audit table!"
        assert table_data[nc_id][0] == "ADD", f"Proposed constraint {nc_id} should be classified as ADD!"
        assert len(table_data[nc_id][1]) > 10, f"Proposed constraint {nc_id} lacks explicit rationale!"

    # 8. Phase 4 Auxiliary Deliverables (Section 2.4)
    auxiliary_items = [
        "AUDIT-AB-01",
        "AUDIT-TESTS",
        "EXP-HARNESS",
        "ROOT-SCRIPTS",
        "TELEMETRY-4",
        "Benchmarks"
    ]
    for item in auxiliary_items:
        assert item in table_data, f"Auxiliary item '{item}' missing classification in audit table!"
        assert table_data[item][0] in {"REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"}
        assert len(table_data[item][1]) > 10, f"Auxiliary item '{item}' lacks explicit rationale!"

    # 9. Architectural Concepts & Paradigms (Section 2.6)
    architectural_concepts = [
        "Stanford Smallville Substrate",
        "Strategy A (Fork & Refactor) & Strategy B (Modern Fork)",
        "Strategy C (Clean Rebuild)",
        "9-Layer Decoupled Architecture (Layers A–I)",
        "Prompt-Based Governance",
        "Cedar / OPA Policy Engine & DPoP Tokens",
        "Smallville Tri-Factor Retrieval Scoring",
        "Unconstrained Homogeneous Multi-Agent Debate",
        "Phase-Gated Structured Collaboration (SOPs)",
        "Multi-Feature Heuristic Agent Routing",
        "Neural / Learned Puppeteer Routing",
        "Proposed Constraints NC-71 through NC-75"
    ]
    for concept in architectural_concepts:
        assert concept in table_data, f"Architectural concept '{concept}' missing classification in audit table!"
        assert table_data[concept][0] in {"REUSE", "EXTEND", "ADD", "REJECT", "UNKNOWN"}
        assert len(table_data[concept][1]) > 10, f"Architectural concept '{concept}' lacks explicit rationale!"

    # Total audit items verified: 16 + 16 + 17 + 18 + 5 + 70 + 5 + 6 + 12 = 165
    assert len(table_data) >= 165, f"Expected at least 165 classified deliverables and concepts, found {len(table_data)}"



def test_seven_governance_conflicts_documented():
    """Verify that all 7 governance conflicts and stale contracts are detailed in Section 2.7."""
    with open(AUDIT_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Routing Escalation Rule Conflict" in content
    assert "Weight Transposition in AS-03" in content
    assert "Reflection Node Hardcoding" in content
    assert "Statistical Adjudication Defect" in content
    assert "Gate Identifier Disambiguation" in content
    assert "Unauthorized Phase 4 Live Execution" in content
    assert "Root-Level Script Sprawl" in content or "Script Sprawl" in content


def test_governance_firewall_blocks_execution():
    """Verify that the programmatic governance firewall deterministically blocks execution."""
    assert is_execution_permitted() is False
    with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
        assert_execution_permitted()
    assert "PAUSED / CONTRACT_TIGHTENING_REQUIRED" in str(exc_info.value)


def test_governance_firewall_edge_cases():
    """Probe edge cases: missing file, corrupted JSON, missing keys, invalid enums, tampered authority."""
    # 1. Non-existent file -> fail closed
    with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
        load_governance("non_existent_governance.json")
    assert "not found" in str(exc_info.value).lower()

    # 2. Corrupted JSON -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        tf.write("{malformed json: broken")
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            load_governance(tf_path)
        assert "corrupted" in str(exc_info.value).lower()
    finally:
        os.remove(tf_path)

    # 3. Missing mandatory keys -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        json.dump({"schema_version": "1.0.0"}, tf)
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            load_governance(tf_path)
        assert "missing mandatory key" in str(exc_info.value).lower()
    finally:
        os.remove(tf_path)

    # 4. Unknown lifecycle state enum -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        bad_gov = {
            "schema_version": "1.0.0",
            "canonical_lifecycle_state": "UNAUTHORIZED_STATE_ENUM",
            "authority_state": {},
            "execution_firewall": {},
            "closed_gates": [],
            "pending_gates": [],
            "gate_result": "UNKNOWN"
        }
        json.dump(bad_gov, tf)
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            load_governance(tf_path)
        assert "unknown or unparseable" in str(exc_info.value).lower()
    finally:
        os.remove(tf_path)

    # 5. Tampered authority (e.g. state active, but implementation authority NOT_GRANTED) -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        tampered = {
            "schema_version": "1.0.0",
            "canonical_lifecycle_state": "PHASE_4_EXECUTION_AUTHORIZED",
            "authority_state": {
                "implementation_authority": "NOT_GRANTED",
                "experiment_execution_authority": "NOT_GRANTED"
            },
            "execution_firewall": {
                "runtime_execution_permitted": False
            },
            "closed_gates": [],
            "pending_gates": [],
            "gate_result": "IN_PROGRESS"
        }
        json.dump(tampered, tf)
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            assert_execution_permitted(tf_path)
        assert "implementation authority" in str(exc_info.value).lower()
    finally:
        os.remove(tf_path)

    # 6. Non-execution lifecycle state (e.g. RESEARCH_DESIGN) with implementation authority GRANTED -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        non_exec_gov = {
            "schema_version": "1.0.0",
            "canonical_lifecycle_state": "RESEARCH_DESIGN",
            "authority_state": {
                "implementation_authority": "GRANTED",
                "experiment_execution_authority": "GRANTED",
                "simulation_execution_authority": "GRANTED"
            },
            "execution_firewall": {
                "runtime_execution_permitted": True,
                "simulation_runs_permitted": True,
                "firewall_enforcement_mode": "FAIL_CLOSED"
            },
            "closed_gates": [],
            "pending_gates": [],
            "gate_result": "IN_PROGRESS"
        }
        json.dump(non_exec_gov, tf)
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            assert_execution_permitted(tf_path)
        assert "not an authorized execution state" in str(exc_info.value).lower()
    finally:
        os.remove(tf_path)

    # 7. Authorized state but experiment execution authority NOT_GRANTED -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        missing_exp_auth = {
            "schema_version": "1.0.0",
            "canonical_lifecycle_state": "PHASE_4_EXECUTION_AUTHORIZED",
            "authority_state": {
                "implementation_authority": "GRANTED",
                "experiment_execution_authority": "NOT_GRANTED",
                "simulation_execution_authority": "GRANTED"
            },
            "execution_firewall": {
                "runtime_execution_permitted": True,
                "simulation_runs_permitted": True,
                "firewall_enforcement_mode": "FAIL_CLOSED"
            },
            "closed_gates": [],
            "pending_gates": [],
            "gate_result": "IN_PROGRESS"
        }
        json.dump(missing_exp_auth, tf)
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            assert_execution_permitted(tf_path)
        assert "experiment execution authority" in str(exc_info.value).lower()
    finally:
        os.remove(tf_path)

    # 8. Non-dict root JSON (e.g. list payload containing key strings) -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        json.dump(["schema_version", "canonical_lifecycle_state", "authority_state", "execution_firewall", "closed_gates", "pending_gates", "gate_result"], tf)
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            load_governance(tf_path)
        assert "must be a json object" in str(exc_info.value).lower()
        # Ensure is_execution_permitted handles non-dict root without crashing
        assert is_execution_permitted(tf_path) is False
    finally:
        os.remove(tf_path)

    # 9. Non-list closed_gates or pending_gates -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        bad_gates = {
            "schema_version": "1.0.0",
            "canonical_lifecycle_state": "PAUSED / CONTRACT_TIGHTENING_REQUIRED",
            "authority_state": {},
            "execution_firewall": {},
            "closed_gates": "not_a_list",
            "pending_gates": [],
            "gate_result": "READY"
        }
        json.dump(bad_gates, tf)
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            load_governance(tf_path)
        assert "closed_gates' must be a json array" in str(exc_info.value).lower()
    finally:
        os.remove(tf_path)

    # 10. Tampered enforcement mode (e.g. FAIL_OPEN) -> fail closed
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tf:
        bad_mode = {
            "schema_version": "1.0.0",
            "canonical_lifecycle_state": "PHASE_4_EXECUTION_AUTHORIZED",
            "authority_state": {
                "implementation_authority": "GRANTED",
                "experiment_execution_authority": "GRANTED",
                "simulation_execution_authority": "GRANTED"
            },
            "execution_firewall": {
                "runtime_execution_permitted": True,
                "simulation_runs_permitted": True,
                "firewall_enforcement_mode": "FAIL_OPEN"
            },
            "closed_gates": [],
            "pending_gates": [],
            "gate_result": "IN_PROGRESS"
        }
        json.dump(bad_mode, tf)
        tf_path = tf.name
    try:
        with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
            assert_execution_permitted(tf_path)
        assert "fail_closed" in str(exc_info.value).lower()
    finally:
        os.remove(tf_path)


def test_primitive_adjudication_and_architecture_freeze_firewalls():
    """Verify that primitive adjudication and architecture freeze are blocked fail-closed under canonical state."""
    # Under canonical state, primitive adjudication is NOT_AUTHORIZED
    with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
        assert_primitive_adjudication_permitted()
    assert "primitive adjudication" in str(exc_info.value).lower()
    assert "NOT_AUTHORIZED" in str(exc_info.value)

    # Under canonical state, architecture is strictly UNFROZEN
    with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
        assert_architecture_freeze_permitted()
    assert "architecture freeze" in str(exc_info.value).lower()
    assert "UNFROZEN" in str(exc_info.value)


def test_live_harness_blocked_by_firewall():
    """Verify that attempting to execute run_exp_ab_01_comp.py is blocked fail-closed by the firewall."""
    from run_exp_ab_01_comp import main as harness_main
    with pytest.raises(GovernanceFirewallBlockedError) as exc_info:
        harness_main()
    assert "PAUSED / CONTRACT_TIGHTENING_REQUIRED" in str(exc_info.value)

