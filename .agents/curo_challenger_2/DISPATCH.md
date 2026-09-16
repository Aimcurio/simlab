# Task Assignment — curo_challenger_2 (Adversarial Governance & Experiment Challenger)

## Mission
Adversarially challenge the governance mechanisms, failure modes (DR-07), negative constraints (DR-15), and reproduction experiment designs (DR-11, DR-12) in the Curo Deep Research Investigation.

## Mandatory Reading & Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Deliverables to Challenge:
  - `E:\projects\simlab\deliverables\DR-07_failure_register.md`
  - `E:\projects\simlab\deliverables\DR-08_conflict_register.md`
  - `E:\projects\simlab\deliverables\DR-11_reproduction_candidate_list.md`
  - `E:\projects\simlab\deliverables\DR-12_proposed_experiment_matrix.md`
  - `E:\projects\simlab\deliverables\DR-15_lessons_learned_forward_constraints.md`

## Challenge Objectives
1. **Governance Exploitation & TOCTOU**: Probe whether Cedar/OPA policies and Macaroons are vulnerable to approval replay or bearer exfiltration unless cryptographic content hashes and DPoP holder binding are strictly enforced (per NC-08, NC-09).
2. **Reproduction Experiment Validity (DR-12)**: Challenge whether EXP-001, EXP-002, and EXP-003 have sufficient statistical power, cluster-robust controls, and genuine falsifiability.
3. **Operational Negative Constraints (DR-15)**: Verify that NC-01 through NC-12 are complete and not easily bypassed.
4. **Boundary Invariants**: Verify that NO code execution or simulation runtime building is authorized or implied.

## Deliverable
Write your adversarial challenge report and verdict (`APPROVE` or `REQUEST_CHANGES`) to:
`E:\projects\simlab\.agents\curo_challenger_2\challenge_report.md`
and write your handoff report to:
`E:\projects\simlab\.agents\curo_challenger_2\handoff.md`.
Notify orchestrator via `send_message` when complete.

## 2026-09-15T20:26:47Z
You are curo_challenger_2, serving as Adversarial Governance & Experiment Challenger for the Curo Deep Research Investigation.
Working Directory: E:\projects\simlab\.agents\curo_challenger_2
Authoritative Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read lines under header ## 2026-09-15T20:06:10Z first)
Task Assignment: E:\projects\simlab\.agents\curo_challenger_2\DISPATCH.md

Challenge governance, failures, and experiment designs in DR-07, DR-08, DR-11, DR-12, and DR-15:
- Probe Cedar/OPA TOCTOU vulnerabilities and Macaroon bearer token replay (check if NC-08/09 mitigate).
- Challenge EXP-001, EXP-002, EXP-003 power calculations and falsifiability.
- Challenge completeness of negative forward constraints NC-01 through NC-12.
- Verify strict enforcement that no code execution or simulation runtime building is authorized.

Deliver challenge report and verdict (APPROVE / REQUEST_CHANGES) to:
E:\projects\simlab\.agents\curo_challenger_2\challenge_report.md
and handoff report to:
E:\projects\simlab\.agents\curo_challenger_2\handoff.md.
Notify orchestrator via send_message when complete.

