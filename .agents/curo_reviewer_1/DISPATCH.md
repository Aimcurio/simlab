# Task Assignment — curo_reviewer_1 (Research Reviewer: DR-01 to DR-08)

## Mission
Independently review, audit, and adversarially challenge Tier 1 deliverables DR-01 through DR-08 of the Curo Deep Research Investigation.

## Mandatory Reading & Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Deliverables to Review:
  - `E:\projects\simlab\deliverables\DR-01_research_corpus_ledger.md`
  - `E:\projects\simlab\deliverables\DR-02_source_authority_map.md`
  - `E:\projects\simlab\deliverables\DR-03_system_architecture_profiles.md`
  - `E:\projects\simlab\deliverables\DR-04_paper_code_mapping.md`
  - `E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md`
  - `E:\projects\simlab\deliverables\DR-06_system_comparison_matrix.md`
  - `E:\projects\simlab\deliverables\DR-07_failure_register.md`
  - `E:\projects\simlab\deliverables\DR-08_conflict_register.md`

## Review Criteria
1. **DR-05 Schema Invariant**: Verify that every single primitive record contains all 26 required fields. Confirm that zero primitives receive `VALIDATED` status. Verify that unmeasured or unavailable data strictly uses `UNKNOWN`, `NOT_REPORTED`, `NOT_MEASURED`, `NOT_APPLICABLE`, or `UNRESOLVED`.
2. **Repository Archaeology & Source Integrity**: Verify that System 5 is conclusively mapped to `OpenBMB/ChatDev:puppeteer` (commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a`). Verify the disambiguation of Fan et al. `AI_Hospital` vs Zhang et al. `Agent Hospital`.
3. **Paper-to-Code Mapping (DR-04)**: Verify code citations, file paths, line numbers, and mechanism classifications.
4. **Failure & Conflict Registers (DR-07, DR-08)**: Verify that failure modes (15) and conflicts (6) are documented with evidence, mechanisms, and mitigations.
5. **Anti-Premature-Synthesis**: Verify that no primitive is promoted or selected as a finalized architecture.

## Deliverable
Write your comprehensive review report and verdict (`APPROVE` or `REQUEST_CHANGES`) to:
`E:\projects\simlab\.agents\curo_reviewer_1\review_report.md`
and write your handoff report to:
`E:\projects\simlab\.agents\curo_reviewer_1\handoff.md`.
Notify orchestrator via `send_message` when complete.

## 2026-09-15T20:26:47Z
You are curo_reviewer_1, serving as Research Reviewer for DR-01 through DR-08 of the Curo Deep Research Investigation.
Working Directory: E:\projects\simlab\.agents\curo_reviewer_1
Authoritative Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read lines under header ## 2026-09-15T20:06:10Z first)
Task Assignment: E:\projects\simlab\.agents\curo_reviewer_1\DISPATCH.md

Review DR-01 through DR-08 in E:\projects\simlab\deliverables\:
- Verify DR-05 schema completeness: all 28 primitives, all 26 fields, ZERO VALIDATED status, explicit missing states.
- Verify DR-02 repository archaeology (System 5 in OpenBMB/ChatDev:puppeteer commit b24e6e6, AI Hospital vs Agent Hospital).
- Verify DR-04 code paths, line numbers, and mechanism classifications.
- Verify DR-07 (15 failure modes) and DR-08 (6 conflict controversies).
- Verify Anti-Premature-Synthesis Invariant.

Deliver review report and verdict (APPROVE / REQUEST_CHANGES) to:
E:\projects\simlab\.agents\curo_reviewer_1\review_report.md
and handoff report to:
E:\projects\simlab\.agents\curo_reviewer_1\handoff.md.
Notify orchestrator via send_message when complete.
