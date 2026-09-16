# Task Assignment — curo_auditor_1 (Forensic Integrity Auditor)

## Mission
Conduct an independent forensic integrity audit of the entire Curo Deep Research Investigation deliverables package (DR-01 through DR-16 and `curo_research_package.md`).

## Mandatory Reading & Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- All deliverables in `E:\projects\simlab\deliverables\` (DR-01 through DR-16)
- Master deliverable `E:\projects\simlab\curo_research_package.md`

## Forensic Audit Checks
1. **DR-05 Anti-Fabrication & Schema Completeness Check**:
   - Audit all 28 primitive records in `DR-05_primitive_evidence_matrix.md`.
   - Verify that every record has all 26 schema fields present.
   - Verify that NO primitive has received `VALIDATED` status. (Permitted: PROPOSED, REPRODUCTION_CANDIDATE, PROMISING_BUT_UNVERIFIED, CONTEXT_DEPENDENT, INSUFFICIENT_EVIDENCE, REJECTED).
   - Verify that missing data strictly uses permitted values (`UNKNOWN`, `NOT_REPORTED`, `NOT_MEASURED`, `NOT_APPLICABLE`, `UNRESOLVED`). Check for fabricated numbers.
2. **Code Reference Integrity Check**:
   - Audit code citations in `DR-02`, `DR-04`, `DR-05`: verify commit hashes, branches (`puppeteer` branch for System 5 in `OpenBMB/ChatDev`), file paths, and line citations.
   - Confirm disambiguation of Fan et al. `AI_Hospital` vs Zhang et al. `Agent Hospital`.
3. **Curo Boundary & Lifecycle Invariants**:
   - Verify `CURRENT_LIFECYCLE_STATE = RESEARCH_AUTHORIZED`.
   - Verify `IMPLEMENTATION_AUTHORITY = NOT_GRANTED`.
   - Verify `ARCHITECTURE_STATUS = UNFROZEN`.
   - Verify that Curo is NOT used as an NPC brain, simulation runtime, memory substrate, or benchmark target.
   - Verify that Gate R1 recommendation in DR-16 is strictly one of: `CONTINUE_RESEARCH`, `INSUFFICIENT_EVIDENCE`, or `READY_FOR_REPRODUCTION_DESIGN`.

## Hard Veto Rule
If any integrity violation, fabricated metric, unauthorized code execution, premature architecture freezing, or schema omission is detected, you MUST report `INTEGRITY VIOLATION` / `FAIL`. Otherwise report `CLEAN` / `PASS`.

## Deliverable
Write your forensic audit report and verdict to:
`E:\projects\simlab\.agents\curo_auditor_1\audit_report.md`
and write your handoff report to:
`E:\projects\simlab\.agents\curo_auditor_1\handoff.md`.
Notify orchestrator via `send_message` when complete.

## 2026-09-15T20:26:47Z

<USER_REQUEST>
You are curo_auditor_1, serving as Forensic Integrity Auditor for the Curo Deep Research Investigation.
Working Directory: E:\projects\simlab\.agents\curo_auditor_1
Authoritative Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read lines under header ## 2026-09-15T20:06:10Z first)
Task Assignment: E:\projects\simlab\.agents\curo_auditor_1\DISPATCH.md

Conduct a thorough forensic integrity audit across all deliverables in E:\projects\simlab\deliverables\ (DR-01 to DR-16) and E:\projects\simlab\curo_research_package.md:
1. Audit all 28 primitives in DR-05 for all 26 schema fields. Ensure ZERO primitives have VALIDATED status. Check for fabricated values vs permitted explicit states (UNKNOWN, NOT_REPORTED, etc.).
2. Audit code citations, repository commit hashes, branches (OpenBMB/ChatDev:puppeteer), and line numbers.
3. Audit lifecycle invariants: CURRENT_LIFECYCLE_STATE = RESEARCH_AUTHORIZED, IMPLEMENTATION_AUTHORITY = NOT_GRANTED, ARCHITECTURE_STATUS = UNFROZEN, Curo boundary preserved, Gate R1 recommendation strictly permitted.

HARD VETO: If any integrity violation or cheating is detected, report INTEGRITY VIOLATION / FAIL. Otherwise report CLEAN / PASS.

Deliver audit report and verdict to:
E:\projects\simlab\.agents\curo_auditor_1\audit_report.md
and handoff report to:
E:\projects\simlab\.agents\curo_auditor_1\handoff.md.
Notify orchestrator via send_message when complete.
</USER_REQUEST>
