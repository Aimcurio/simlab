# Task Assignment — curo_reviewer_2 (Research Reviewer: DR-09 to DR-16 & Master Package)

## Mission
Independently review, audit, and adversarially challenge Tier 1 and Tier 2 deliverables DR-09 through DR-16 and the master package `curo_research_package.md` of the Curo Deep Research Investigation.

## Mandatory Reading & Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Deliverables to Review:
  - `E:\projects\simlab\deliverables\DR-09_unknowns_register.md`
  - `E:\projects\simlab\deliverables\DR-10_candidate_baseline_matrix.md`
  - `E:\projects\simlab\deliverables\DR-11_reproduction_candidate_list.md`
  - `E:\projects\simlab\deliverables\DR-12_proposed_experiment_matrix.md`
  - `E:\projects\simlab\deliverables\DR-13_cost_latency_scaling_analysis.md`
  - `E:\projects\simlab\deliverables\DR-14_research_synthesis.md`
  - `E:\projects\simlab\deliverables\DR-15_lessons_learned_forward_constraints.md`
  - `E:\projects\simlab\deliverables\DR-16_research_gate_package.md`
  - `E:\projects\simlab\curo_research_package.md`

## Review Criteria
1. **Baseline Rigor (DR-10)**: Verify operational definitions of B0, B1, B2, B3, B4. Ensure cognitive biases ("more agents = better", etc.) are explicitly guarded against.
2. **Reproduction Experiment Boundaries (DR-11, DR-12)**: Verify that experiments are DESIGN ONLY with ZERO execution authorization. Ensure smallest falsifying experiments, explicit limitations, and non-justified conclusions are stated.
3. **Operational Negative Forward Constraints (DR-15)**: Verify that NC-01 through NC-12 are concrete, actionable, and binding.
4. **Lifecycle & Gate R1 Criteria (DR-16)**: Verify lifecycle state is `RESEARCH_AUTHORIZED`, `IMPLEMENTATION_AUTHORITY = NOT_GRANTED`, architecture status is `UNFROZEN`, Curo boundary invariant is preserved, and Gate R1 recommendation is strictly one of `CONTINUE_RESEARCH`, `INSUFFICIENT_EVIDENCE`, or `READY_FOR_REPRODUCTION_DESIGN`.
5. **Master Package Completeness**: Verify that `curo_research_package.md` accurately synthesizes all findings.

## Deliverable
Write your comprehensive review report and verdict (`APPROVE` or `REQUEST_CHANGES`) to:
`E:\projects\simlab\.agents\curo_reviewer_2\review_report.md`
and write your handoff report to:
`E:\projects\simlab\.agents\curo_reviewer_2\handoff.md`.
Notify orchestrator via `send_message` when complete.

## 2026-09-15T20:26:47Z
Review DR-09 through DR-16 in E:\projects\simlab\deliverables\ and E:\projects\simlab\curo_research_package.md:
- Verify DR-09 unknowns (UNRESOLVED status).
- Verify DR-10 baselines B0 through B4 and bias guards.
- Verify DR-11 and DR-12 reproduction designs (DESIGN ONLY, zero execution authorization, explicit limitations).
- Verify DR-13 cost/latency/scaling analysis.
- Verify DR-14 research synthesis (architecture UNFROZEN).
- Verify DR-15 operational negative forward constraints NC-01 through NC-12.
- Verify DR-16 Gate R1 package and recommendation (strictly CONTINUE_RESEARCH, INSUFFICIENT_EVIDENCE, or READY_FOR_REPRODUCTION_DESIGN).
- Verify master curo_research_package.md completeness.

Deliver review report and verdict (APPROVE / REQUEST_CHANGES) to:
E:\projects\simlab\.agents\curo_reviewer_2\review_report.md
and handoff report to:
E:\projects\simlab\.agents\curo_reviewer_2\handoff.md.
Notify orchestrator via send_message when complete.

