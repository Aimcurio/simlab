# Phase 2 Reproduction Design & Experimental Roadmap Plan

## Mission
Advance Curo SimLab into bounded reproduction design (Phase 2). Produce complete, publication-grade deliverables RD-01 through RD-16 in `E:\projects\simlab\reproduction_design\`, compile the master package `curo_reproduction_design_package.md`, conduct independent review, adversarial challenge, and forensic audit, and evaluate at Gate R2.

## Operational Milestones

### Milestone 1: Deliverable Survey & Schema Audit
- Dispatch Explorers to inspect existing RD-01 through RD-16 and `curo_reproduction_design_package.md`.
- Verify all 35 required fields in the Experiment Specification Record schema across RP-01 (RD-05), RP-02 (RD-06), RP-03 (RD-07), RP-04 (RD-08).
- Verify alignment with Phase 1 deliverables (DR-01 through DR-16, especially DR-11, DR-12, DR-15).
- Verify strict governance compliance: `ARCHITECTURE_STATUS = UNFROZEN`, `IMPLEMENTATION_AUTHORITY = NOT_GRANTED`, `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`.

### Milestone 2: Worker Refinement & Deliverable Completeness
- Dispatch Worker(s) to address any findings from Milestone 1, ensuring all 16 deliverables (RD-01 to RD-16) and the master package are publication-grade, fully populated, and meet all acceptance criteria.
- Ensure the Minimum Experiment Principle (isolated harnesses, zero full simulation rebuilds), deterministic-first measurement, pre-registered failure thresholds, and strict compute-matched controls are rigorously embedded.

### Milestone 3: Independent Review & Adversarial Challenge
- Dispatch 2 independent Reviewers (`teamwork_preview_reviewer`) to evaluate experimental rigor, statistical power, confound controls, and baseline matching.
- Dispatch 2 adversarial Challengers (`teamwork_preview_challenger`) to stress-test failure modes, confound vulnerabilities, sample sizes, and falsifiability.

### Milestone 4: Forensic Integrity Audit
- Dispatch Forensic Auditor (`teamwork_preview_auditor`) to verify:
  - Zero source code or runtime implementation files created.
  - Zero live API calls or benchmark runs executed.
  - No synthetic/fabricated experimental results.
  - Strict preservation of Curo governance boundaries.

### Milestone 5: Gate R2 Synthesis & Reporting
- Compile Gate R2 package evaluation.
- Synthesize all findings and gate verdicts in `GATE_STATUS.md` and `handoff.md`.
- Submit formal victory/completion notification to Sentinel.
