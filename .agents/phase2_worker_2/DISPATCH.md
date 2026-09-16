# DISPATCH: Phase 2 Remediation Worker 2

- **Role**: Versatile Worker (`teamwork_preview_worker`)
- **Working Directory**: `E:\projects\simlab\.agents\phase2_worker_2`
- **Assigned Deliverables**:
  - `E:\projects\simlab\reproduction_design\RD-11_failure_confound_register.md`
  - `E:\projects\simlab\reproduction_design\RD-13_execution_isolation_plan.md`
  - `E:\projects\simlab\reproduction_design\RD-14_independent_review.md`
  - `E:\projects\simlab\reproduction_design\RD-15_lessons_learned_forward_constraints.md`
  - `E:\projects\simlab\reproduction_design\RD-16_gate_r2_package.md`
  - `E:\projects\simlab\curo_reproduction_design_package.md` (Master Package)

## Context & Input Reports:
- `E:\projects\simlab\ORIGINAL_REQUEST.md` (MANDATORY: read first)
- Reviewer 2 Handoff: `E:\projects\simlab\.agents\phase2_reviewer_2\handoff.md`
- Challenger 2 Handoff: `E:\projects\simlab\.agents\phase2_challenger_2\handoff.md`
- Gate R1 DR-15: `E:\projects\simlab\deliverables\DR-15_lessons_learned_forward_constraints.md`

## Mandatory Warning:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Remediation Tasks:
1. **Constraint Lineage Restoration in RD-15**:
   - Restore the 16 core technical architectural constraints established in Gate R1 (`DR-15`: NC-01 through NC-16) in full fidelity (Cedar policies, CAS URIs, DPoP tokens, residual CIM formula, AST literal redaction, ZeroMQ IPC, dynamic quotas, unprunable roles, container tmpfs, bubblewrap cgroups).
   - Number the new Phase 2 reproduction constraints as NC-17 through NC-24 (or NC-17 to NC-30) cleanly without collision.
2. **Deterministic Seed Pinning in RD-13**:
   - Add explicit PRNG seed pinning specifications: `numpy.random.SeedSequence`, `torch.manual_seed`, and `PYTHONHASHSEED`.
   - Specify rootless container execution with gVisor sandbox / seccomp profile rather than privileged DinD.
   - Mandate `store: false` parameter on all API client calls to prevent benchmark data contamination / model provider training ingestion.
3. **Failure Register Invalidation Triggers in RD-11**:
   - Adjust FM-05 collapse threshold from $>85\%$ to $>65\%$ (or $\chi^2$ goodness-of-fit $p < 0.01$).
   - Fix FM-09 compute threshold to $1.10$ ($10\%$ imbalance) to match the compute contract.
   - Add FM-07 (Prompt Leakage) and FM-12 (Data Contamination) to Section 2 abort gate triggers.
4. **Governance Headers in RD-16 & Master Package**:
   - Ensure `Implementation Authority: NOT_GRANTED` is unambiguous and not weakened by premature phrases like `LIMITED_TO_APPROVED...`.
   - Update criteria verification in RD-16 reflecting remediated sample sizes and dual controls.
5. **Master Package Synchronization (`curo_reproduction_design_package.md`)**:
   - Once all RD files (RD-01 to RD-16) are remediated by Worker 1 and Worker 2, compile and synchronize `curo_reproduction_design_package.md` so that it incorporates all 16 deliverables with 100% congruence.

When finished, produce a detailed handoff report at:
`E:\projects\simlab\.agents\phase2_worker_2\handoff.md`

## 2026-09-16T09:46:59Z

You are Phase 2 Remediation Worker 2 for Curo SimLab.
Working directory: E:\projects\simlab\.agents\phase2_worker_2
Authoritative Request: E:\projects\simlab\ORIGINAL_REQUEST.md (MANDATORY: read first).
Dispatch Instructions: E:\projects\simlab\.agents\phase2_worker_2\DISPATCH.md

Your task is to remediate the governance, constraint lineage, failure register, seed pinning, and master package synchronization issues identified by Reviewer 2 and Challenger 2 across:
- E:\projects\simlab\reproduction_design\RD-11_failure_confound_register.md
- E:\projects\simlab\reproduction_design\RD-13_execution_isolation_plan.md
- E:\projects\simlab\reproduction_design\RD-14_independent_review.md
- E:\projects\simlab\reproduction_design\RD-15_lessons_learned_forward_constraints.md
- E:\projects\simlab\reproduction_design\RD-16_gate_r2_package.md
- E:\projects\simlab\curo_reproduction_design_package.md (Master Package)

Mandatory Warning: DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work.

Execute all remediation tasks in DISPATCH.md:
1. RD-15: Restore Gate R1 technical constraints NC-01 through NC-16 in full fidelity and append Phase 2 reproduction constraints NC-17 to NC-24 with clean numbering.
2. RD-13: Add deterministic seed pinning (numpy SeedSequence, torch.manual_seed, PYTHONHASHSEED), rootless container with gVisor/seccomp, store: false on API calls.
3. RD-11: Adjust FM-05 threshold (>65%), fix FM-09 threshold to 1.10 (10%), add FM-07 and FM-12 to Section 2 abort gate triggers.
4. RD-16: Ensure Implementation Authority: NOT_GRANTED is unambiguous; update criteria verification with remediated sample sizes and dual controls.
5. Master Package: Synchronize curo_reproduction_design_package.md so all 16 deliverables are 100% congruent with the updated individual files.

Produce your handoff report at:
E:\projects\simlab\.agents\phase2_worker_2\handoff.md
When complete, send a message to parent with your summary.

