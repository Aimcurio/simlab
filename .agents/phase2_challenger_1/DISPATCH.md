# DISPATCH: Phase 2 Challenger 1

- **Role**: Code-executing Adversarial Verifier (`teamwork_preview_challenger`)
- **Working Directory**: `E:\projects\simlab\.agents\phase2_challenger_1`
- **Assigned Scope**: Adversarial stress-testing of experimental designs for RP-01 (Smallville Memory Recency) and RP-02 (Debate vs B1-SC):
  - `E:\projects\simlab\reproduction_design\RD-05_rp01_experiment_design.md`
  - `E:\projects\simlab\reproduction_design\RD-06_rp02_experiment_design.md`
  - `E:\projects\simlab\reproduction_design\RD-03_experimental_hypothesis_register.md`
  - `E:\projects\simlab\reproduction_design\RD-04_baseline_compute_matching.md`
- **Context Files**:
  - `E:\projects\simlab\ORIGINAL_REQUEST.md` (MANDATORY: read first)
  - `E:\projects\simlab\deliverables\DR-12_proposed_experiment_matrix.md`

## Adversarial Challenge Objectives:
1. Stress-test RP-01 recency test: Could query selection bias or embedding similarity variance create false positives or negatives? Are the 100 queries adequately balanced? Is the exponential decay parameter ($\lambda=0.995$) sensitive to simulation timescale?
2. Stress-test RP-02 debate vs B1-SC: Is the $\pm 10\%$ token parity realistic? Does B1-SC with $K=6$ adequately represent compute equivalence? Could consensus collapse or majority voting bias distort findings? Is the TOST equivalence margin ($[-0.03, +0.03]$) appropriate?
3. Stress-test pre-registered failure thresholds: Are they falsifiable? Could an ambiguous result slip through?
4. Governance boundary check: You may write and execute mathematical/statistical verification scripts locally in your working directory to verify power math or formulas, but you MUST NOT execute benchmark LLM API calls or build runtime simulation code.

Produce your structured challenge handoff report at:
`E:\projects\simlab\.agents\phase2_challenger_1\handoff.md`
Your handoff MUST state an explicit verdict: `APPROVE` or `REQUEST_CHANGES`.

## 2026-09-16T09:40:03Z
You are Phase 2 Challenger 1 for Curo SimLab.
Working directory: E:\projects\simlab\.agents\phase2_challenger_1
Authoritative Request: E:\projects\simlab\ORIGINAL_REQUEST.md (MANDATORY: read first before starting work).
Dispatch Instructions: E:\projects\simlab\.agents\phase2_challenger_1\DISPATCH.md

Your task is to adversarially stress-test experimental designs for RP-01 (Smallville Memory Recency) and RP-02 (Debate vs B1-SC):
- E:\projects\simlab\reproduction_design\RD-05_rp01_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-06_rp02_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-03_experimental_hypothesis_register.md
- E:\projects\simlab\reproduction_design\RD-04_baseline_compute_matching.md

Adversarial Objectives:
1. Stress-test RP-01 recency test: Could query selection bias or embedding similarity variance create false positives or negatives? Are the 100 queries adequately balanced? Is the exponential decay parameter (lambda=0.995) sensitive to simulation timescale?
2. Stress-test RP-02 debate vs B1-SC: Is the +/- 10% token parity realistic? Does B1-SC with K=6 adequately represent compute equivalence? Could consensus collapse or majority voting bias distort findings? Is the TOST equivalence margin ([-0.03, +0.03]) appropriate?
3. Stress-test pre-registered failure thresholds: Are they falsifiable? Could an ambiguous result slip through?
4. Governance boundary check: You may write and execute mathematical/statistical verification scripts locally in your working directory to verify power math or formulas, but you MUST NOT execute benchmark LLM API calls or build runtime simulation code.

Produce your structured challenge report at:
E:\projects\simlab\.agents\phase2_challenger_1\handoff.md
Your handoff MUST state an explicit verdict: APPROVE or REQUEST_CHANGES.
When complete, send a message to parent with your verdict and summary.

