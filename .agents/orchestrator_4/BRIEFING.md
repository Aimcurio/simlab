# BRIEFING — 2026-09-16T21:55:00Z

## Mission
Conduct a bounded scientific audit of CURO SIMLAB EXP-AB-01-COMP before dispatching the next Phase 4 experiment, distinguishing real mechanisms from implementation defects, benchmark artifacts, or measurement errors.

## 🔒 My Identity
- Archetype: Project Orchestrator (orchestrator_4)
- Roles: orchestrator, user_liaison, human_reporter, successor
- Working directory: E:\projects\simlab\.agents\orchestrator_4
- Original parent: Sentinel (parent)
- Original parent conversation ID: 8d881230-7435-4c9e-adbb-cd7efc3f3369

## 🔒 My Workflow
- **Pattern**: Project Pattern (Orchestrator hierarchy, Survey -> Decompose & Delegate / Iteration Loop)
- **Scope document**: E:\projects\simlab\.agents\orchestrator_4\SCOPE.md
1. **Decompose**:
   - Phase 1: Deep technical investigation & evidence gathering (3 Explorers in parallel mapping the statistical data, telemetry, codebase, score distributions, and reflection failure).
   - Phase 2: Synthesis and audit report authoring (Worker drafting deliverable `E:\projects\simlab\audits\EXP-AB-01-COMP\AUDIT_EXP_AB_01_COMP.md`).
   - Phase 3: Independent Review and Adversarial Verification (2 Reviewers + 2 Challengers).
   - Phase 4: Forensic Integrity Audit (teamwork_preview_auditor verifying authenticity, zero fabricated outputs, strict adherence to invariants).
   - Phase 5: Orchestrator Gate evaluation and final handoff to Sentinel.
2. **Dispatch & Execute**:
   - Direct iteration loop across Explorers, Worker, Reviewers, Challengers, and Auditor.
3. **On failure**:
   - Retry: nudge stuck agent or re-send task
   - Replace: spawn fresh agent with partial progress
   - Skip: proceed without (only if non-critical; auditor is NEVER skipped)
   - Redistribute: split stuck agent's remaining work
   - Redesign: re-partition decomposition
   - Escalate: report to Sentinel (last resort)
4. **Succession**:
   - Threshold: 16 spawns. When threshold reached and all subagents complete, write handoff.md, cancel timers, spawn successor, record successor ID.
- **Work items**:
  1. Survey & Technical Investigation [pending]
  2. Master Audit Report Authoring [pending]
  3. Independent Review & Empirical Challenge [pending]
  4. Forensic Integrity Audit [pending]
  5. Gate Evaluation & Sentinel Reporting [pending]
- **Current phase**: 1
- **Current focus**: Work item 1 (Survey & Technical Investigation)

## 🔒 Key Constraints
- NEVER write, modify, or create source code files directly.
- NEVER run build/test commands yourself — require workers to do so.
- NEVER investigate or explore the problem at the code level — dispatch Explorers for technical investigation.
- You MAY use file-editing tools ONLY for metadata/state files (.md) in your .agents/ folder.
- R1. PRESERVE OBSERVED RESULTS: Treat existing raw results as immutable evidence. Do not rewrite or suppress MRR scores (A2: 0.5130, A4: 0.5002, A7: 0.0941, A3: 0.0086, A8: 0.0325). Preserve all hashes, telemetry, seeds, and run IDs. Do not rerun unless defect requires preregistered corrective rerun. Do not advance to another Phase 4 experiment.
- R2. CORRECT NON-INFERIORITY ADJUDICATION: Verify preregistered non-inferiority procedure for A4 vs A7. Report statistic, bound, alpha, decision. Do not infer formal non-inferiority from a two-sided Wilcoxon p-value alone.
- R3. CORRECT IMPORTANCE-NECESSITY INTERPRETATION: Address contradiction that A4 outperformed A7 by ~+0.4061 MRR. Explain using effect direction, magnitude, CI, and statistical test.
- R4. MECHANISTIC FAILURE AUDIT: Inspect score distributions (min, max, mean, variance, quantiles). Test scale dominance, scale inversion, normalization mismatch, weight error, reflection dominance, duplicate crowding, label leakage, benchmark bias.
- R5. REFLECTION FAILURE ANALYSIS: Determine why A8 produced 100% Rank-1 crowding, 100/100 queries affected, all top-five slots occupied by reflections. Classify failure.
- R6. VALIDATE WEIGHT CONFIGURATIONS: Verify A1-A8 configurations match AS-03 preregistration. If mismatch, output EXPERIMENT_CONFIGURATION_DRIFT and stop.
- R7. CHECK PHASE 3 COMPATIBILITY: Compare with Phase 3 RP-01 findings. Record PHASE3_PHASE4_EVIDENCE_CONFLICT if necessary.
- R8. PRIMITIVE EVIDENCE STATUS: Update only Criterion B (ABLATION_EVIDENCE) for PR-COG-01. Do not adjudicate globally. Do not freeze architecture.
- R9. LESSONS LEARNED: Capture validated lessons as forward constraints.
- R10. GATE TO NEXT EXPERIMENT: Return exactly one of 4 permitted statuses.
- Zero tolerance for integrity violations: Forensic audit is a binary veto.
- Never reuse a subagent after handoff — always spawn fresh.

## Current Parent
- Conversation ID: 8d881230-7435-4c9e-adbb-cd7efc3f3369
- Updated: 2026-09-16T21:55:00Z

## Key Decisions Made
- Established 5-milestone orchestration workflow for the Bounded Scientific Audit.
- Target deliverable: `E:\projects\simlab\audits\EXP-AB-01-COMP\AUDIT_EXP_AB_01_COMP.md`.
- Dispatch 3 parallel Explorers:
  - Explorer 1: Focus on Statistical Adjudication (R2, R3, R10), Non-inferiority math, Wilcoxon tests, CI, and AS-12 / AS-03 contracts.
  - Explorer 2: Focus on Mechanistic Failure & Score Distributions (R4, R6), weights, normalizations, telemetry inspections, and script logic.
  - Explorer 3: Focus on Reflection Mechanism & Phase 3 Compatibility (R5, R7, R8, R9), PR-COG-01 Criterion B status, and forward constraints.

## Team Roster
| Agent | Type | Work Item | Status | Conv ID |
|-------|------|-----------|--------|---------|
| audit_explorer_1 | teamwork_preview_explorer | Survey R1, R2, R3, R10 (Stats & Non-inferiority) | completed | f428bd88-3271-44a3-81b0-3fdf32b4e1cb |
| audit_explorer_2 | teamwork_preview_explorer | Survey R4, R6 (Score Distributions & Weights) | completed | 0ab8a9a8-01ab-4728-99e9-78a7828b7e3b |
| audit_explorer_3 | teamwork_preview_explorer | Survey R5, R7, R8, R9 (Reflection & Phase 3) | completed | 9eaa92a0-96ab-4aeb-b6b3-c0a2221d3555 |
| audit_worker_1 | teamwork_preview_worker | Master Deliverable Authoring (AUDIT_EXP_AB_01_COMP.md) | completed | b67420d1-5ac0-4745-a410-eaa2d8824453 |
| audit_reviewer_1 | teamwork_preview_reviewer | Review Sections A, B, C, J, K | completed | eea9be97-b406-487c-ada0-a6a10b38455b |
| audit_reviewer_2 | teamwork_preview_reviewer | Review Sections D, E, F, G, H, I | in-progress | 5292f7e9-0b1b-407f-bb24-0a5e13572c97 |
| audit_challenger_1 | teamwork_preview_challenger | Statistical & Sub-cohort Stress Testing | completed | a582b0e8-e555-4413-85f1-93fce593c1d0 |
| audit_challenger_2 | teamwork_preview_challenger | Reflection & Normalization Stress Testing | completed | 403b5ebf-001e-4d5a-80bd-319e3855a69f |
| audit_forensic_auditor | teamwork_preview_auditor | Integrity Forensics & Invariants Audit | completed | b16c80ae-eccf-4539-a774-5d0d33df84ee |
| remedy_worker_1 | teamwork_preview_worker | Remediation of Challenger empirical findings | in-progress | 4d58f250-ef33-484e-a575-65eba7c7c1ce |

## Succession Status
- Succession required: no
- Spawn count: 10 / 16
- Pending subagents: 4d58f250-ef33-484e-a575-65eba7c7c1ce
- Predecessor: none
- Successor: not yet spawned

## Active Timers
- Heartbeat cron: task-38
- Safety timer: none

## Artifact Index
- `E:\projects\simlab\.agents\orchestrator_4\DISPATCH.md` — Authoritative dispatch instructions
- `E:\projects\simlab\.agents\orchestrator_4\BRIEFING.md` — Persistent working memory and state
- `E:\projects\simlab\.agents\orchestrator_4\progress.md` — Milestone progress and liveness tracking
- `E:\projects\simlab\.agents\orchestrator_4\SCOPE.md` — Detailed project scope and milestone breakdown
