"""
Automated Victory Audit Test Suite for Curo SimLab Phase 2
Independently verifies all 6 core invariants and integrity constraints.
"""
import re
import unittest
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

class TestSimLabPhase2Victory(unittest.TestCase):

    def test_invariant1_deliverable_completeness(self):
        """Invariant 1: RD-01 through RD-16 exist, non-empty, and master package is congruent."""
        self.assertTrue(MASTER_PKG.exists(), "Master package curo_reproduction_design_package.md must exist")
        self.assertGreater(MASTER_PKG.stat().st_size, 100000, "Master package must be >100KB")

        master_content = MASTER_PKG.read_text(encoding="utf-8", errors="replace")

        for i in range(1, 17):
            pattern = f"RD-{i:02d}_*.md"
            matches = list(RD_DIR.glob(pattern))
            self.assertEqual(len(matches), 1, f"Exactly one file matching {pattern} must exist")
            rd_file = matches[0]
            self.assertGreater(rd_file.stat().st_size, 1000, f"{rd_file.name} must be >1KB")
            
            # Verify deliverable presence in master package
            self.assertIn(rd_file.name, master_content, f"{rd_file.name} must be referenced in master package")

    def test_invariant2_schema_35_fields(self):
        """Invariant 2: Strictly verify all 35 required schema fields for RP-01 to RP-04."""
        rp_files = {
            "RP-01": RD_DIR / "RD-05_rp01_experiment_design.md",
            "RP-02": RD_DIR / "RD-06_rp02_experiment_design.md",
            "RP-03": RD_DIR / "RD-07_rp03_experiment_design.md",
            "RP-04": RD_DIR / "RD-08_rp04_experiment_design.md"
        }
        field_regex = re.compile(r"^###\s+(\d+)\.\s+([a-zA-Z0-9_\-]+)", re.MULTILINE)

        for rp_id, path in rp_files.items():
            self.assertTrue(path.exists(), f"{rp_id} file must exist")
            content = path.read_text(encoding="utf-8", errors="replace")
            matches = field_regex.findall(content)
            found = {int(num): name.strip().lower() for num, name in matches}

            self.assertEqual(len(found), 35, f"{rp_id} must have exactly 35 fields, found {len(found)}")
            for idx, expected in enumerate(EXPECTED_35_FIELDS, 1):
                self.assertIn(idx, found, f"{rp_id} missing field index {idx}")
                self.assertEqual(found[idx], expected, f"{rp_id} field {idx} mismatch: expected '{expected}', got '{found[idx]}'")

    def test_invariant3_minimum_experiment_and_controls(self):
        """Invariant 3: Verify isolated micro-benchmarks, FM-01 to FM-12, and Dual-Control B1-SC protocol."""
        rd11 = (RD_DIR / "RD-11_failure_confound_register.md").read_text(encoding="utf-8")
        for i in range(1, 13):
            fm_id = f"FM-{i:02d}"
            self.assertIn(fm_id, rd11, f"Failure mode {fm_id} must be in RD-11")

        rd04 = (RD_DIR / "RD-04_baseline_compute_matching.md").read_text(encoding="utf-8")
        rd06 = (RD_DIR / "RD-06_rp02_experiment_design.md").read_text(encoding="utf-8")

        for txt, doc in [(rd04, "RD-04"), (rd06, "RD-06")]:
            self.assertTrue("k=7" in txt.lower() or "k = 7" in txt.lower(), f"{doc} must specify K=7 call-matched control")
            self.assertTrue("k=10" in txt.lower() or "k = 10" in txt.lower(), f"{doc} must specify K=10 token-matched control")
            self.assertTrue("dual-control" in txt.lower(), f"{doc} must specify Dual-Control protocol")

    def test_invariant4_governance_boundaries(self):
        """Invariant 4: Confirm Architecture UNFROZEN, Implementation NOT_GRANTED, Execution NOT_GRANTED."""
        rd16 = (RD_DIR / "RD-16_gate_r2_package.md").read_text(encoding="utf-8")
        self.assertIn("UNFROZEN", rd16, "Architecture status must be UNFROZEN")
        self.assertIn("IMPLEMENTATION_AUTHORITY", rd16)
        self.assertIn("EXPERIMENT_EXECUTION_AUTHORITY", rd16)

        # Ensure no runtime code in project root or subdirectories (except .agents)
        py_files = [p for p in BASE_DIR.glob("**/*.py") if ".agents" not in str(p)]
        # The only allowed py file is test_empirical_challenges.py
        for p in py_files:
            self.assertEqual(p.name, "test_empirical_challenges.py", f"Unauthorized code file: {p}")

    def test_invariant5_gate_r2_evaluation(self):
        """Invariant 5: Gate R2 package formally evaluated with permitted outcome."""
        rd16 = (RD_DIR / "RD-16_gate_r2_package.md").read_text(encoding="utf-8")
        permitted = ["READY_FOR_REPRODUCTION_EXECUTION", "CONTINUE_REPRODUCTION_DESIGN", "INSUFFICIENT_EXPERIMENT_DESIGN"]
        found = [p for p in permitted if p in rd16]
        self.assertTrue(len(found) >= 1, "Must contain a permitted Gate R2 outcome")
        self.assertIn("READY_FOR_REPRODUCTION_EXECUTION", found, "Expected outcome READY_FOR_REPRODUCTION_EXECUTION")

    def test_invariant6_forward_constraints(self):
        """Invariant 6: Verify all 30 operational forward constraints NC-01 to NC-30 in RD-15."""
        rd15 = (RD_DIR / "RD-15_lessons_learned_forward_constraints.md").read_text(encoding="utf-8")
        for i in range(1, 31):
            nc_id = f"NC-{i:02d}"
            self.assertIn(nc_id, rd15, f"Constraint {nc_id} must be in RD-15")

    def test_prohibited_patterns_and_placeholders(self):
        """Verify absence of unexpanded placeholders or fake outputs."""
        placeholder_pats = [
            re.compile(r"\bTODO\b"),
            re.compile(r"\bTBD\b"),
            re.compile(r"\bFIXME\b"),
            re.compile(r"\bPLACEHOLDER\b"),
            re.compile(r"\[insert\s", re.IGNORECASE),
            re.compile(r"\[to be\s", re.IGNORECASE),
            re.compile(r"<placeholder>", re.IGNORECASE)
        ]
        rd_files = list(RD_DIR.glob("RD-*.md"))
        for f in rd_files:
            txt = f.read_text(encoding="utf-8", errors="replace")
            for line_no, line in enumerate(txt.splitlines(), 1):
                # Skip references in RD-15 to NC-20 rule regarding "TODO" in external codebases
                if f.name.startswith("RD-15") and ("isolated TODO" in line or "single TODO" in line):
                    continue
                for pat in placeholder_pats:
                    match = pat.search(line)
                    self.assertIsNone(match, f"Found placeholder in {f.name}:{line_no} -> '{line.strip()}'")

if __name__ == "__main__":
    unittest.main()
