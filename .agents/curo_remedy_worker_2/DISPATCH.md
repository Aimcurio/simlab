# Task Assignment — curo_remedy_worker_2 (Remediation Author: DR-10, DR-14, Master Package)

## Mission
Apply required baseline boundary qualifications and cross-document synchronizations to DR-10, DR-14, and `curo_research_package.md`.

## Mandatory Reading & Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Challenger 1 Handoff & Report: `E:\projects\simlab\.agents\curo_challenger_1\handoff.md`, `E:\projects\simlab\.agents\curo_challenger_1\challenge_report.md`
- Challenger 2 Handoff & Report: `E:\projects\simlab\.agents\curo_challenger_2\handoff.md`, `E:\projects\simlab\.agents\curo_challenger_2\challenge_report.md`
- Reviewer 2 Findings: `E:\projects\simlab\.agents\curo_reviewer_2\handoff.md`
- Files to Edit:
  - `E:\projects\simlab\deliverables\DR-10_candidate_baseline_matrix.md`
  - `E:\projects\simlab\deliverables\DR-14_research_synthesis.md`
  - `E:\projects\simlab\curo_research_package.md`

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Lifecycle State & Authority Boundaries
- Current Lifecycle State: `RESEARCH_AUTHORIZED`
- Implementation Authority: `NOT_GRANTED` (Strict prohibition: no code writing, simulation runtime implementation, dependency installation, or benchmark execution).
- Core Invariant: RESEARCH_DESIGN != IMPLEMENTATION_AUTHORIZATION.

## Required Modifications
1. **DR-10 (Candidate Baseline Matrix)**:
   - In Section 3 and Section 4, add explicit boundary qualification to the Single-Agent Self-Consistency (B1-SC) equivalence finding:
     * Explicitly state that B1-SC matches or outperforms multi-agent debate on homogeneous, closed-context reasoning tasks (e.g., GSM8K, MATH, HumanEval) where all agents share the same foundation model and prompt context.
     * Clarify that B1-SC does NOT substitute for multi-agent systems in environments with partitioned private state, asymmetric specialized external tools, distinct persona perspectives, or asynchronous human-in-the-loop interaction.
2. **DR-14 (Research Synthesis)**:
   - Synchronize Section 3 and Section 4 with the B1-SC boundary qualification above.
   - Synchronize debate token scaling formula to $O(N^2 \cdot R^2 \cdot L)$ in Section 4.
3. **curo_research_package.md (Master Package)**:
   - Harmonize Section 11 Reproduction Candidates table: ensure RP-03 and RP-04 labels match DR-11 (`RP-03: ChatDev Phase Sandboxing & Task Completion`, `RP-04: Evolving Orchestration RL Policy Efficiency`).
   - Harmonize Section 12 Experiment Matrix: update EXP-001 to $72$ tasks ($N \ge 360$ per condition) with TOST non-inferiority, and EXP-002 to $56$ tasks ($N \ge 279$).
   - Harmonize Section 13 Token Scaling: update debate token scaling formula to $O(N^2 \cdot R^2 \cdot L)$.
   - Harmonize Section 15 Negative Forward Constraints: add NC-13 (Cross-Run Memory Isolation), NC-14 (Anti-Self-Approval Invariant), NC-15 (Model Endpoint Pinning), and NC-16 (Sandbox Tool Execution Resource Caps).

## Deliverable Handoff
Modify all 3 markdown files.
Write handoff report to:
`E:\projects\simlab\.agents\curo_remedy_worker_2\handoff.md`.
Notify orchestrator via `send_message` when complete.

## 2026-09-15T20:34:05Z
You are curo_remedy_worker_2, serving as Remediation Author for DR-10, DR-14, and curo_research_package.md.
Working Directory: E:\projects\simlab\.agents\curo_remedy_worker_2
Authoritative Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read lines under header ## 2026-09-15T20:06:10Z first)
Task Assignment: E:\projects\simlab\.agents\curo_remedy_worker_2\DISPATCH.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Core Inputs:
- E:\projects\simlab\.agents\curo_challenger_1\challenge_report.md
- E:\projects\simlab\.agents\curo_challenger_2\challenge_report.md
- E:\projects\simlab\.agents\curo_reviewer_2\review_report.md

Execute the required remediations:
1. In DR-10 & DR-14: qualify B1-SC scope (homogeneous closed reasoning vs heterogeneous partitioned data/tools).
2. In DR-14: update broadcast debate formula to O(N^2 * R^2 * L).
3. In curo_research_package.md: harmonize Section 11 RP-03/RP-04 labels; harmonize Section 12 task counts (72 for EXP-001, 56 for EXP-002); harmonize Section 13 debate formula; harmonize Section 15 to include NC-13 through NC-16.

Deliver handoff report to:
E:\projects\simlab\.agents\curo_remedy_worker_2\handoff.md
and notify orchestrator via send_message when complete.
