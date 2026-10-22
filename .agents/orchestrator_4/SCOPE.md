# Scope: EXP-AB-01-COMP Bounded Scientific Audit

## Architecture
- Context: CURO SIMLAB EXP-AB-01-COMP Phase 4 memory ablation experiment audit.
- Target Deliverable: `E:\projects\simlab\audits\EXP-AB-01-COMP\AUDIT_EXP_AB_01_COMP.md` and supporting audit artifacts in `E:\projects\simlab\audits\EXP-AB-01-COMP\`.
- Raw Evidence Sources:
  - Telemetry: `E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_results.json` and `exp_ab_01_comp_telemetry.jsonl`
  - Preregistration Contracts: `E:\projects\simlab\ablation_design\` (`AS-01` through `AS-18`), `curo_phase4_ablation_package.md`
  - Phase 3 Context: `E:\projects\simlab\phase3_execution\`, `curo_phase3_execution_package.md`, `reproduction_design\` (`RD-01` through `RD-16`)
  - Execution Scripts: `E:\projects\simlab\run_exp_ab_01_comp.py`, audit helper scripts in `E:\projects\simlab\`

## Feature Inventory
| # | Feature / Requirement | Description | Milestone | Source |
|---|-----------------------|-------------|-----------|--------|
| 1 | R1: Preserve Observed Results | Treat existing raw results as immutable (A2: 0.5130, A4: 0.5002, A7: 0.0941, A3: 0.0086, A8: 0.0325). No un-prescribed reruns. | M1, M2, M4 | ORIGINAL_REQUEST §R1 |
| 2 | R2: Non-Inferiority Verification | Audit A4 vs A7 non-inferiority against preregistration margin (-0.05). Report statistic, bound, alpha, decision. | M1, M2 | ORIGINAL_REQUEST §R2 |
| 3 | R3: Importance-Necessity Interpretation | Address A4 outperforming A7 by ~+0.4061 MRR using effect direction, magnitude, CI, and test. Explain directional failure. | M1, M2 | ORIGINAL_REQUEST §R3 |
| 4 | R4: Mechanistic Failure Audit | Distribution inspections of importance, relevance, recency. Test scale dominance, scale inversion, normalizations, weights, ties, etc. | M1, M2 | ORIGINAL_REQUEST §R4 |
| 5 | R5: Reflection Failure Analysis | Analyze A8 100% Rank-1 crowding, 100/100 queries affected, top-5 occupied by reflection nodes. Classify failure mechanism. | M1, M2 | ORIGINAL_REQUEST §R5 |
| 6 | R6: Validate Weight Configurations | Match executed weights vs AS-03 preregistration. Check for EXPERIMENT_CONFIGURATION_DRIFT. | M1, M2 | ORIGINAL_REQUEST §R6 |
| 7 | R7: Phase 3 / Phase 4 Compatibility | Compare tri-factor collapse with Phase 3 RP-01 findings. Check for PHASE3_PHASE4_EVIDENCE_CONFLICT. | M1, M2 | ORIGINAL_REQUEST §R7 |
| 8 | R8: PR-COG-01 Evidence Update | Update Criterion B (ABLATION_EVIDENCE) only. Do not adjudicate globally. Architecture UNFROZEN. | M1, M2 | ORIGINAL_REQUEST §R8 |
| 9 | R9: Lessons Learned & Forward Constraints | Capture validated lessons as forward constraints (scale compatibility, admission controls, directional interpretation). | M1, M2 | ORIGINAL_REQUEST §R9 |
| 10 | R10: Gate to Next Experiment | Return exactly one of 4 permitted statuses for Stage 4A. | M1, M2, M5 | ORIGINAL_REQUEST §R10 |
| 11 | Deliverable Sections A–K | Produce complete AUDIT_EXP_AB_01_COMP.md with all required sections A through K. | M2, M3, M4 | ORIGINAL_REQUEST §Required Output Sections |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Survey & Technical Investigation | 3 Explorers examine statistical data, score distributions, code logic, reflection mechanics, and contracts | none | PLANNED |
| M2 | Master Audit Report Authoring | Worker synthesizes findings into `AUDIT_EXP_AB_01_COMP.md` and supporting data | M1 | PLANNED |
| M3 | Independent Review & Adversarial Challenge | 2 Reviewers + 2 Challengers verify rigor, edge cases, calculations, and empirical claims | M2 | PLANNED |
| M4 | Forensic Integrity Audit | Forensic Auditor checks for zero fabricated data, clean evidence, adherence to invariants | M3 | PLANNED |
| M5 | Gate Evaluation & Sentinel Handoff | Orchestrator evaluates verdicts, writes handoff, reports to Sentinel | M4 | PLANNED |

## Interface Contracts
- Input: Existing telemetry in `E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\` and design docs in `E:\projects\simlab\ablation_design\`.
- Output: Authoritative report at `E:\projects\simlab\audits\EXP-AB-01-COMP\AUDIT_EXP_AB_01_COMP.md` with sections A through K.
- Verification: Scripts must be executed by Workers/Challengers/Auditors to verify calculations, distributions, and classifications.
