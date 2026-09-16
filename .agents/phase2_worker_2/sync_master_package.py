import os

repo_dir = r"E:\projects\simlab"
rd_dir = os.path.join(repo_dir, "reproduction_design")
master_pkg_path = os.path.join(repo_dir, "curo_reproduction_design_package.md")

deliverables = [
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
    "RD-16_gate_r2_package.md"
]

header = """# Curo SimLab: Phase 2 Reproduction Design & Experimental Roadmap
## Master Experimental Specification & Gate R2 Package
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Lifecycle State**: `GATE_R2_COMPLETE`  
**Gate R2 Outcome**: `READY_FOR_REPRODUCTION_EXECUTION`  
**Architecture Status**: `UNFROZEN`  
**Implementation Authority**: `NOT_GRANTED (Prospective Phase 3: LIMITED_TO_APPROVED_REPRODUCTION_HARNESSES, Subject to Separate Requester Authorization)`  
**Experiment Execution Authority**: `NOT_GRANTED`  
**Evaluation Date**: 2026-09-16  

================================================================================
TABLE OF CONTENTS
================================================================================
1. RD-01: Reproduction Priority Matrix
2. RD-02: Candidate-to-Unknown Mapping
3. RD-03: Experimental Hypothesis Register
4. RD-04: Baseline & Compute-Matching Specification
5. RD-05: RP-01 Experiment Design Record (Smallville Memory Recency/Retrieval)
6. RD-06: RP-02 Experiment Design Record (Compute-Matched Single vs Multi-Agent Debate)
7. RD-07: RP-03 Experiment Design Record (Structured Phase Boundaries / ChatDev)
8. RD-08: RP-04 Experiment Design Record (Dynamic Orchestration / ChatDev:puppeteer)
9. RD-09: Metrics & Evaluation Contract
10. RD-10: Reproducibility & Telemetry Contract
11. RD-11: Failure / Confound Register
12. RD-12: Cost / Token / Latency Budget
13. RD-13: Execution Isolation Plan
14. RD-14: Independent Substantive Review
15. RD-15: Lessons Learned & Operational Forward Constraints (NC-01 to NC-30)
16. RD-16: Gate R2 Package & Formal Decision

================================================================================
"""

parts = [header]

for filename in deliverables:
    filepath = os.path.join(rd_dir, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing required deliverable: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()
    section_divider = f"""



================================================================================
# DELIVERABLE: {filename}
================================================================================

{content}
"""
    parts.append(section_divider)

full_master_package = "".join(parts) + "\n"

with open(master_pkg_path, "w", encoding="utf-8") as f:
    f.write(full_master_package)

print(f"SUCCESS: compiled {len(deliverables)} deliverables into {master_pkg_path}")
print(f"Total size: {len(full_master_package)} characters, {len(full_master_package.encode('utf-8'))} bytes")
