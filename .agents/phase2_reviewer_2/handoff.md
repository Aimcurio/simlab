# Gate R2 Independent Review & Adversarial Critic Report

**Reviewer**: Phase 2 Reviewer 2 (`teamwork_preview_reviewer`)  
**Roles**: Reviewer, Adversarial Critic  
**Working Directory**: `E:\projects\simlab\.agents\phase2_reviewer_2`  
**Target Scope**: Governance compliance, negative constraints, risk/threat modeling, failure registers, execution isolation, and Gate R2 package evaluation across:
- `E:\projects\simlab\reproduction_design\RD-11_failure_confound_register.md`
- `E:\projects\simlab\reproduction_design\RD-13_execution_isolation_plan.md`
- `E:\projects\simlab\reproduction_design\RD-14_independent_review.md`
- `E:\projects\simlab\reproduction_design\RD-15_lessons_learned_forward_constraints.md`
- `E:\projects\simlab\reproduction_design\RD-16_gate_r2_package.md`
- `E:\projects\simlab\curo_reproduction_design_package.md` (Master Package)  
**Date**: 2026-09-16  
**Final Formal Verdict**: **`REQUEST_CHANGES`**

---

## 1. Observation

Direct, verbatim observations across the reviewed codebase and deliverables:

### 1.1 Integrity & Governance Invariants
1. **Implementation & Execution Authority**:
   - `RD-11` (line 4): `Authority State: ARCHITECTURE_STATUS = UNFROZEN | IMPLEMENTATION_AUTHORITY = NOT_GRANTED | EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`
   - `RD-13` (line 4): `Authority State: ARCHITECTURE_STATUS = UNFROZEN | IMPLEMENTATION_AUTHORITY = NOT_GRANTED | EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`
   - `RD-14` (line 4): `Authority State: ARCHITECTURE_STATUS = UNFROZEN | IMPLEMENTATION_AUTHORITY = NOT_GRANTED | EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`
   - `RD-15` (line 4): `Authority State: ARCHITECTURE_STATUS = UNFROZEN | IMPLEMENTATION_AUTHORITY = NOT_GRANTED | EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`
   - `RD-16` (line 4): `Authority State: ARCHITECTURE_STATUS = UNFROZEN | IMPLEMENTATION_AUTHORITY = NOT_GRANTED | EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`
   - `curo_reproduction_design_package.md` (lines 6–8):
     ```markdown
     Architecture Status: UNFROZEN
     Implementation Authority: LIMITED_TO_APPROVED_REPRODUCTION_HARNESSES (Requires Separate Requester Authorization)
     Experiment Execution Authority: NOT_GRANTED
     ```
   - Zero runtime code files (`.py`, `.ts`, `.js`, `.cpp`, `.rs`) have been added to `reproduction_design/` or the repository root for simulation execution.
   - Zero live API calls or unauthorized experiments were run.

### 1.2 Negative Constraints Inheritance & Formulation (RD-15 vs DR-15)
1. **DR-15 Baseline Constraints** (`E:\projects\simlab\deliverables\DR-15_lessons_learned_forward_constraints.md`, lines 36–53, 57–553, 701–724):
   - `NC-01`: NO Unvalidated Prompt-Based Governance (Cedar/OPA mandatory outside LLM context)
   - `NC-02`: NO Content-Unbound Critic Approvals & Mutable Filesystem TOCTOU (CAS `cas://sha256:...`)
   - `NC-03`: NO Unattenuated, Holder-Unbound, or Same-Tick Replayable Capability Tokens (DPoP + monotonic sequence counter)
   - `NC-04`: NO Unconditional Correlation for Critic Independence Metrics ($CIM_{\text{residual}} = 1.0 - |\rho(V_c - Y, V_b - Y)|$)
   - `NC-05`: NO Uninspected Code Artifact Handoffs or Smuggled String Literal Injections (AST parsing, comment/docstring stripping, string literal redaction, static linters)
   - `NC-06`: NO Unseeded Randomness or Floating-Point Time in Simulation Kernels (SeedSequence + integer discrete ticks)
   - `NC-07`: NO File-Polling Inter-Process Communication (IPC) (AsyncIO / ZeroMQ in-memory message brokers)
   - `NC-08`: NO Inverted or Rank-Indexed Recency Decay Formulations (Exponential decay over verified elapsed ticks $\lambda^{\Delta T}$)
   - `NC-09`: NO Ungrounded Homogeneous Multi-Agent Debate Loops (Heterogeneous models + compiler/tool validation)
   - `NC-10`: NO Compute-Unnormalized Multi-Agent Comparative Claims (Mandatory B1-SC matched tokens)
   - `NC-11`: NO Unbudgeted or Uncapped Dynamic Agent Spawning (Hard quotas on active agents, depth, tokens)
   - `NC-12`: NO Irreversible Early Pruning of Safety/Auditor Roles (Unprunable invariant anchors)
   - `NC-13`: NO Persistent Cross-Run Memory or Context Carryover (Ephemeral container tmpfs + fixture snapshots)
   - `NC-14`: NO Self-Approval or Cryptographic Role Aliasing (Cryptographic Author != Reviewer invariant)
   - `NC-15`: NO Floating Model Endpoints or Unpinned Checkpoint Hashes (Immutable snapshots + system fingerprint checks)
   - `NC-16`: NO Unconstrained Sandbox Tool Execution Resource Budgets (Bubblewrap / cgroups: 60s CPU, 512MB RAM, network none)
   - `NC-17` to `NC-23`: Covering schema-only validation, stale lifecycle states, polynomial vs. exponential language, stub extrapolation, cross-domain generalization, substrate vs. primitive decoupling, and audit regex heuristics.

2. **RD-15 Declared Constraints** (`E:\projects\simlab\reproduction_design\RD-15_lessons_learned_forward_constraints.md`, lines 21–53):
   - Lines 21–45 declare `### Gate R1 Inherited Constraints (NC-01 to NC-23)`:
     - `NC-01`: "Never select a final simulation architecture during research or reproduction phases."
     - `NC-02`: "Never treat a paper's claimed mechanism as implemented without repository verification."
     - `NC-03`: "Never use current repository main branches as substitutes for evaluated historical releases."
     - `NC-04`: "Never assign VALIDATED status to any primitive during literature research alone."
     - `NC-05`: "Never compare multi-agent systems solely against each other without single-agent baselines (B1, B1-SC)."
     - `NC-06`: "Never report token, cost, or scaling metrics without documenting the exact model version and parameters."
     - `NC-07`: "Never authorize simulator implementation or experiment execution during research phases."
     - `NC-08`: "Never execute code on the host machine while IMPLEMENTATION_AUTHORITY = NOT_GRANTED."
     - `NC-09`: "Never spin agent loops to force certainty when evidence is contradictory; record UNRESOLVED."
     - `NC-10`: "Never allow Curo governance mechanisms to become part of the experimental simulation runtime."
     - `NC-11`: "Never fabricate missing values in evidence registers; use explicit missingness states."
     - `NC-12`: "Never evaluate multi-agent debate without controlling for total token spend and inference calls."
     - `NC-13`: "Never evaluate memory retrieval without verifying the actual underlying scoring implementation."
     - `NC-14`: "Never evaluate dynamic orchestration without measuring orchestrator token and latency overhead."
     - `NC-15`: "Never propose a reproduction experiment that requires rebuilding an entire legacy simulation world."
     - `NC-16`: "Never omit explicit external validity limitations from proposed experimental conclusions."
     - `NC-17` to `NC-23`: Match DR-15 verbatim.
   - Lines 46–53 declare `### Phase 2 New Operational Constraints (NC-24 to NC-30)`:
     - `NC-24`: Minimum Harness Constraint
     - `NC-25`: Deterministic Priority Constraint
     - `NC-26`: Compute Equivalence Constraint
     - `NC-27`: Network Egress Firewall Constraint
     - `NC-28`: Failure Pre-Registration Constraint
     - `NC-29`: Architecture Firewall Invariant
     - `NC-30`: Execution Authorization Boundary

### 1.3 Execution Isolation Plan (RD-13)
- `RD-13_execution_isolation_plan.md` (lines 10–39):
  - Layer 1: Container Boundary (Docker/OCI container with rootless user and read-only filesystem)
  - Layer 2: Network Firewall (Strictly bounded egress: authorized LLM API endpoints ONLY)
  - Layer 3: Ephemeral Storage (tmpfs for scratch runtime files; zero persistent state on host)
  - Layer 4: Deterministic Mocks (Offline mock API mode replayable with zero network connectivity)
  - Section 2.A: Network Egress Restrictions (Allowed hosts: `api.openai.com`, `generativelanguage.googleapis.com`)
  - Section 2.B: Filesystem & Host Protection (`:ro` repository mount, `/output/telemetry` scratch volume, isolated sub-container for code execution with 10s CPU, 512MB RAM, zero network)
  - Section 2.C: Dependency Pinning (exact hashes in `requirements.lock` via `pip-compile` / `uv export --frozen`)
  - **Direct Observation**: The term `seed` appears **0 times** in `RD-13_execution_isolation_plan.md` (verified via ripgrep). There is no specification of PRNG seed sequences, environment seeding (`PYTHONHASHSEED`), or API model seed parameters.

### 1.4 Failure & Confound Register (RD-11)
- `RD-11_failure_confound_register.md` (lines 12–31):
  - Pre-registers 12 failure modes: `FM-01` (Context Truncation), `FM-02` (False Consensus / Sycophancy), `FM-03` (Role Collapse), `FM-04` (Communication Explosion), `FM-05` (Routing Collapse), `FM-06` (Model-Version Drift), `FM-07` (Prompt Leakage / Inversion), `FM-08` (Score Compression), `FM-09` (Unbalanced Compute), `FM-10` (State Deadlock), `FM-11` (Evaluator Bias), `FM-12` (Data Contamination).
  - Quantitative triggers:
    - FM-01: $L_{ctx} > 16k$
    - FM-04: Turns $> 12$ without state progress; token spend exceeds budget by $> 50\%$
    - FM-05: $> 85\%$ of tasks sent to one path
    - FM-06: System fingerprint changes in API response header
    - FM-07: Exact-match test accuracy jumps to $100\%$ with zero reasoning steps
    - FM-08: Normalized score variance $< 10^{-4}$
    - FM-09: Token ratio $\text{Tok}_{MA} / \text{Tok}_{control} > 1.20$
    - FM-10: Loop count reaches 4 iterations
    - FM-11: Length-bias correlation $r > 0.60$ between word count and judge score
    - FM-12: Single-agent zero-shot accuracy $> 95\%$ on complex novel reasoning
  - Section 2 (Abort & Invalidation Criteria, line 29–30):
    ```markdown
    If an experimental run triggers more than 3 instances of FM-06 (Model Drift) or FM-09 (Unbalanced Compute), the entire batch must be classified as EXPERIMENT_INVALID and re-run under corrected controls.
    ```

### 1.5 Gate R2 Package & Acceptance Criteria (RD-16)
- `RD-16_gate_r2_package.md`:
  - Section 2 audits RD-01 through RD-16, all marked COMPLETE.
  - Section 3 audits all 8 acceptance criteria: Falsifiable Hypotheses [x], Appropriate Controls [x], Compute Matching [x], Deterministic Metrics [x], Resource Caps [x], Architecture Firewall [x], Zero Implementation [x], Independent Review [x].
  - Section 4 formal decision: `READY_FOR_REPRODUCTION_EXECUTION`.
  - Human authorization boundary explicitly stated in Section 4 (lines 70–73): No automatic execution, human authorization required before Phase 3, execution strictly limited to micro-harnesses.

---

## 2. Logic Chain

1. **Premise 1 (Governance Lineage & Negative Constraint Integrity)**:
   - `ORIGINAL_REQUEST.md` and Curo governance require that operational negative constraints established in Gate R1 (`DR-15`) govern all subsequent implementation and experimentation phases.
   - In `DR-15`, `NC-01` through `NC-16` are binding technical architectural constraints (Cedar policy, CAS URIs, DPoP capability tokens, CIM residual correlation, AST sanitization, PRNG seed sequence, ZeroMQ IPC, exponential recency decay, B1-SC token matching, dynamic quotas, unprunable roles, container tmpfs, author!=reviewer key verification, model fingerprint pinning, bubblewrap cgroups).
   - In `RD-15`, lines 21–45 label their first section `Gate R1 Inherited Constraints (NC-01 to NC-23)`, but define `NC-01` through `NC-16` as general research process rules.
   - **Inference 1**: `RD-15` broke the formal lineage of Gate R1 constraints. Because `NC-01` through `NC-16` in `RD-15` conflict with `DR-15`, any Phase 3 execution code attempting to enforce or audit `NC-01` through `NC-16` will suffer identifier collision and semantic ambiguity. Furthermore, the 16 core technical architectural constraints from DR-15 are completely dropped from the active constraints ledger.

2. **Premise 2 (Hermetic Execution Isolation Requirements)**:
   - Dispatch Objective 3 explicitly directs: *"Verify execution isolation plan in RD-13: container hermeticity, network firewall, tmpfs isolation, deterministic seed pinning."*
   - As observed in Observation 1.3, `RD-13` contains zero references to seeds, random number generators, `PYTHONHASHSEED`, or PRNG state isolation.
   - **Inference 2**: Without specifying seed pinning and PRNG initialization in `RD-13`, containerized execution runs risk non-deterministic execution due to unseeded Python dictionary hashing, unpinned random generators, or unpinned LLM sampling seeds, directly threatening the reproducibility contract defined in `RD-10`.

3. **Premise 3 (Failure Mode Pre-Registration & Invalidation Rigor)**:
   - In `RD-11`, Section 2 restricts batch invalidation exclusively to `FM-06` (Model Drift) and `FM-09` (Unbalanced Compute).
   - If `FM-07` (Prompt Leakage) or `FM-12` (Data Contamination) occurs, ground truth is contaminated and the benchmark results are scientifically null and void. Yet `RD-11` omits both from the invalidation criteria.
   - In addition, `FM-09` sets its trigger at $\text{Tok}_{MA} / \text{Tok}_{control} > 1.20$ ($20\%$ imbalance). However, `RD-04` (Section 1) and `RD-06` (Section 2) mandate compute matching within $\pm 10\%$.
   - **Inference 3**: A run with a $15\%$ compute imbalance violates the experimental design specification (`RD-04`/`RD-06`) but will not be detected or mitigated by `FM-09`, allowing flawed data into the analysis. Allowing up to 3 instances of Model Drift (`FM-06`) to accumulate in a batch corrupts sample distributions.

4. **Premise 4 (Gate R2 Evaluation Package & Authority Boundary)**:
   - `RD-16` evaluates all 16 deliverables and all 8 acceptance criteria.
   - The formal recommendation is `READY_FOR_REPRODUCTION_EXECUTION`, which is strictly one of the three permitted outcomes in `ORIGINAL_REQUEST.md`.
   - Human authorization boundaries are preserved in Section 4.
   - However, the summary header in `curo_reproduction_design_package.md` (line 7) and `RD-16` (line 21) states: `Implementation Authority: LIMITED_TO_APPROVED_REPRODUCTION_HARNESSES (Requires Human Auth)`.
   - **Inference 4**: While the body text explicitly defers execution until human requester authorization, declaring the authority as "LIMITED_TO..." in the current active canonical header creates ambiguity against the invariant `IMPLEMENTATION_AUTHORITY = NOT_GRANTED`.

5. **Deductive Synthesis**:
   - Because the work is free of integrity violations (no fabrication, no dummy logic, no shortcuts, no premature implementation), a rejection on integrity grounds is NOT warranted.
   - However, because of (1) the negative constraint collision/lineage rupture in RD-15, (2) the complete omission of seed pinning in RD-13, and (3) the failure invalidation criteria gaps and threshold mismatch in RD-11, the reproduction design package contains material defects that will undermine Phase 3 execution if not corrected now.
   - Therefore, the appropriate, rigorous verdict is **`REQUEST_CHANGES`**.

---

## 3. Caveats

1. **No Live Execution Testing**: In strict compliance with `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` and `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`, no container runtime commands, live Docker builds, or API calls were executed to test `RD-13` or `RD-12`.
2. **Review Scope Boundary**: This review focused primarily on governance compliance, constraints (`RD-15`), failure/threat registers (`RD-11`), execution isolation (`RD-13`), independent review records (`RD-14`), and Gate R2 synthesis (`RD-16`, Master Package). The specific experimental power analyses and statistical design details of `RD-01` through `RD-10` were audited for contract consistency and are concurrently reviewed in depth by Phase 2 Reviewer 1 and Challenger agents.
3. **Intent vs. Form**: The author of `RD-15` likely intended lines 21–45 as an executive summary of research discipline principles rather than a replacement of the technical forward constraints from `DR-15`. However, by numbering them `NC-01` to `NC-23`, it created a formal identifier collision that must be resolved.

---

## 4. Conclusion & Findings

### Final Verdict: **`REQUEST_CHANGES`**

The Phase 2 Reproduction Design deliverables represent high-quality research architecture and adhere strictly to the non-execution invariants (`ARCHITECTURE_STATUS = UNFROZEN`, zero implementation code). However, approval cannot be granted until the four specific findings below are remediated.

### Summary Findings Table

| Finding ID | Severity | Document | Description | Action Required |
|---|---|---|---|---|
| **F-01** | **Critical** | `RD-15` (§2), Master Package (§15) | **Constraint Lineage Rupture & Identifier Collision**: `RD-15` rewrites `NC-01` through `NC-16`, displacing the 16 core technical architectural constraints from Gate R1 (`DR-15`). | Restore the canonical 23 negative constraints from `DR-15` (or renumber/nest the general principles without collision) and append `NC-24` to `NC-30`. |
| **F-02** | **Major** | `RD-13` (§1, §2), Master Package (§13) | **Omission of Deterministic Seed Pinning**: `RD-13` details container, network, and tmpfs isolation, but completely omits deterministic seed pinning and PRNG state management. | Add Section 2.D to `RD-13` specifying container environment PRNG seeding (`PYTHONHASHSEED`, master seed derivation, and API seed parameters). |
| **F-03** | **Major** | `RD-11` (§1, §2), Master Package (§11) | **Incomplete Invalidation Criteria & Threshold Mismatch**: `FM-07` (Prompt Leakage) and `FM-12` (Data Contamination) are omitted from batch invalidation triggers; `FM-09` trigger ($1.20$) conflicts with the $\pm 10\%$ compute matching requirement in `RD-04`/`RD-06`. | Add `FM-07` and `FM-12` to Section 2 invalidation triggers; adjust `FM-09` trigger to $> 1.10$; require immediate abort on confirmed `FM-06` (Model Drift). |
| **F-04** | **Minor** | `RD-16` (§1), Master Package (Header) | **Ambiguous Authority State Formatting**: Current state header phrases implementation authority as `LIMITED_TO_APPROVED...` before requester approval. | Clarify header to: `IMPLEMENTATION_AUTHORITY = NOT_GRANTED (Prospective Phase 3: LIMITED_TO_APPROVED_REPRODUCTION_HARNESSES, Subject to Requester Approval)`. |

---

### Detailed Findings & Adversarial Challenges

#### Finding F-01 (Critical): Negative Constraint Lineage Rupture & Identifier Collision
- **What**: In `RD-15` lines 21–45, the section titled `### Gate R1 Inherited Constraints (NC-01 to NC-23)` replaces the 16 binding technical architectural constraints established in `DR-15` with high-level research axioms.
- **Where**: `E:\projects\simlab\reproduction_design\RD-15_lessons_learned_forward_constraints.md:21-45` and `E:\projects\simlab\curo_reproduction_design_package.md:1114-1138`.
- **Why**: In `DR-15`, `NC-01` through `NC-16` specify concrete, automated technical enforcement mechanisms (Cedar access control, CAS sha256 URIs, DPoP monotonic tokens, CIM residual error correlation, AST string literal stripping, discrete tick PRNG seeds, ZeroMQ IPC, exponential recency decay, B1-SC token matching, dynamic agent quotas, unprunable safety roles, ephemeral container tmpfs, author!=reviewer key verification, model fingerprint pinning, bubblewrap cgroups). In `RD-15`, `NC-01` is redefined as "Never select a final simulation architecture...", `NC-06` is redefined as "Never report token, cost, or scaling metrics...", etc.
- **Adversarial Blast Radius**: In Phase 3, an engineer implementing the memory retrieval harness or execution container auditing against `NC-06` or `NC-08` will find contradictory rules depending on whether they inspect `DR-15` or `RD-15`. Critical security and simulation invariants (e.g., prompt injection defense via AST literal stripping, DPoP token replay defense, residual correlation metrics) lose their binding status in the active forward constraints ledger.
- **Suggested Remediation**:
  Harmonize `RD-15`:
  1. Formally retain the full 23 technical negative constraints from `DR-15` as `Gate R1 Architectural & Technical Constraints (NC-01 to NC-23)`.
  2. If the general research axioms are retained, classify them under an explicit subsection (e.g., `Research Process Axioms RPA-01 to RPA-16`) to eliminate identifier collision.
  3. Retain `NC-24` through `NC-30` as Phase 2 operational constraints.

#### Finding F-02 (Major): Omission of Deterministic Seed Pinning in RD-13
- **What**: `RD-13_execution_isolation_plan.md` contains zero references to seeds, pseudo-random number generators, or seed sequence propagation.
- **Where**: `E:\projects\simlab\reproduction_design\RD-13_execution_isolation_plan.md:1-39` and `E:\projects\simlab\curo_reproduction_design_package.md:995-1034`.
- **Why**: Execution isolation in multi-agent research is not only about filesystem protection and network sandboxing; it is fundamentally about mathematical reproducibility. Python dictionaries and sets are randomized by default across process launches unless `PYTHONHASHSEED` is set. Furthermore, sampling order, agent response order, and embedding permutations require explicit, hierarchical seed derivation (`SeedSequence`).
- **Adversarial Blast Radius**: When Phase 3 execution containers are spun up, identical code running on identical inputs will produce divergent execution traces and metrics simply due to default unseeded hash randomization and floating PRNG state, violating `RD-10` reproducibility standards.
- **Suggested Remediation**:
  Add Section 2.D (`Deterministic Seed Pinning & PRNG State Management`) to `RD-13`:
  - Enforce `PYTHONHASHSEED=0` in container environment variables.
  - Require explicit initialization of master seeds (e.g. `SIMLAB_MASTER_SEED=20260916`) passed via container CLI flags.
  - Specify hierarchical per-agent and per-episode PRNG spawning (`np.random.SeedSequence(master_seed).spawn(N)`).
  - Mandate passing pinned `seed` parameters to supported model API requests (e.g. OpenAI API `seed` parameter) and logging `system_fingerprint`.

#### Finding F-03 (Major): Incomplete Invalidation Criteria & Threshold Mismatch in RD-11
- **What**: In `RD-11` Section 2, batch invalidation is restricted to $>3$ instances of `FM-06` or `FM-09`. `FM-07` (Prompt Leakage) and `FM-12` (Data Contamination) are missing. Furthermore, `FM-09` defines a $1.20$ trigger ($20\%$ imbalance), conflicting with the $\pm 10\%$ requirement in `RD-04` and `RD-06`.
- **Where**: `E:\projects\simlab\reproduction_design\RD-11_failure_confound_register.md:22, 29-30` and `E:\projects\simlab\curo_reproduction_design_package.md:949, 951-953`.
- **Why**:
  1. If prompt leakage (`FM-07`) occurs, test accuracy is artificially inflated to $100\%$, corrupting the condition.
  2. If data contamination (`FM-12`) is detected (e.g. memorization of benchmark items), that task slice is invalid.
  3. Allowing up to 3 instances of Model Drift (`FM-06`) allows contaminated data to mix into sample runs.
  4. The $1.20$ threshold in `FM-09` creates an operational dead zone: a run with a $15\%$ compute imbalance violates `RD-04` / `RD-06` specifications ($\pm 10\%$), but escapes detection under `FM-09`.
- **Adversarial Blast Radius**: Unbalanced compute or contaminated benchmark samples will be reported as valid experimental outcomes, producing false claims of multi-agent superiority.
- **Suggested Remediation**:
  1. Update `RD-11` Section 2: *"If an experimental run triggers ANY confirmed instance of FM-06 (Model Drift), FM-07 (Prompt Leakage), or FM-12 (Data Contamination), or more than 2 instances of FM-09 (Unbalanced Compute), the affected batch/condition must be classified as EXPERIMENT_INVALID and re-run."*
  2. Update `FM-09` detection trigger to: `Token ratio Tok_MA / Tok_control > 1.10 (or < 0.90)` to match `RD-04` and `RD-06`.

#### Finding F-04 (Minor): Ambiguous Governance Authority Formatting
- **What**: In `RD-16` Section 1.1 (line 21) and `curo_reproduction_design_package.md` line 7, the state block states: `Implementation Authority: LIMITED_TO_APPROVED_REPRODUCTION_HARNESSES (Requires Human Auth)`.
- **Where**: `E:\projects\simlab\reproduction_design\RD-16_gate_r2_package.md:21` and `E:\projects\simlab\curo_reproduction_design_package.md:7`.
- **Why**: Although Section 4 correctly states that execution is NOT authorized until the human requester grants approval, declaring the current authority as "LIMITED_TO..." in the header creates an apparent conflict with the invariant `IMPLEMENTATION_AUTHORITY = NOT_GRANTED`.
- **Suggested Remediation**:
  Change the header field to: `Implementation Authority: NOT_GRANTED (Prospective Phase 3 Scope: LIMITED_TO_APPROVED_REPRODUCTION_HARNESSES, Subject to Requester Approval)`.

---

## 5. Verification Method

To independently verify this review's findings and validate the required remedies:

1. **Verify Negative Constraint Discrepancy**:
   - Compare `E:\projects\simlab\deliverables\DR-15_lessons_learned_forward_constraints.md` (lines 36–53, 701–724) against `E:\projects\simlab\reproduction_design\RD-15_lessons_learned_forward_constraints.md` (lines 21–45).
   - Invalidation condition: `RD-15` defines `NC-01` through `NC-16` identically to `DR-15`. (Currently fails; definitions completely diverge).

2. **Verify Omission of Seed Pinning in RD-13**:
   - Run grep command: `grep -i "seed" E:\projects\simlab\reproduction_design\RD-13_execution_isolation_plan.md`.
   - Invalidation condition: Output returns matches detailing PRNG seed pinning. (Currently fails; 0 matches returned).

3. **Verify Failure Invalidation & Compute Matching Discrepancy**:
   - Inspect `E:\projects\simlab\reproduction_design\RD-11_failure_confound_register.md` line 22 vs line 30, and compare against `E:\projects\simlab\reproduction_design\RD-04_baseline_compute_matching.md` line 16.
   - Invalidation condition: `FM-09` matches the $\pm 10\%$ tolerance ($1.10$), and `FM-07`/`FM-12` are present in Section 2. (Currently fails).

4. **Verify Governance Invariant Integrity**:
   - Inspect lines 4, 18–24 of `RD-16_gate_r2_package.md`.
   - Confirm `ARCHITECTURE_STATUS = UNFROZEN` and zero implementation code exists in `reproduction_design/`. (Passes).
