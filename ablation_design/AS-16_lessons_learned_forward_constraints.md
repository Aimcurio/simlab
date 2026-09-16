# AS-16: Lessons Learned & Operational Forward Constraints
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Phase**: Phase 4 Ablation & Stress Test Design  

---

## 1. Retrospective on Phase 4 Design & Governing Principles

1. **The Minimum Ablation Principle**: Ablation studies must isolate exactly one architectural mechanism at a time. Conflating prompt changes with context boundary shifts obscures causality.
2. **Power-First Sample Size Determination**: Arbitrary sample sizes produce statistically inconclusive outcomes (as observed in Phase 3 RP-02 where $N=100$ yielded $p=0.0192 > 0.01$). Phase 4 sample sizes must derive from mathematical power calculations ($1-eta \ge 0.85$).
3. **The Complexity Burden Rule**: Architectural complexity is guilty until proven innocent. Escalating to neural or learned orchestration (Puppeteer) is prohibited unless heuristic routing demonstrably fails pre-registered stress thresholds.

---

## 2. Cumulative Operational Negative Constraints Master Register (NC-01 through NC-60)

All subsequent SimLab phases must strictly consume and enforce these sixty binding negative forward constraints:

### 2.1 Gate R1 Technical & Architectural Constraints (NC-01 to NC-16)
- `NC-01`: **NO Unvalidated Prompt-Based Governance**: Never use natural language prompts for access control; enforce via deterministic Cedar/OPA policy engines.
- `NC-02`: **NO Content-Unbound Critic Approvals & Mutable Filesystem TOCTOU**: Approvals must bind SHA-256 hashes with Ed25519 signatures and immutable CAS URIs.
- `NC-03`: **NO Unattenuated, Holder-Unbound, or Same-Tick Replayable Capability Tokens**: Capability tokens require DPoP public key binding and monotonic sequence counters.
- `NC-04`: **NO Unconditional Correlation for Critic Independence Metrics**: Evaluate conditional independence of residual errors given ground truth ($CIM_{\text{residual}}$).
- `NC-05`: **NO Uninspected Code Artifact Handoffs or Smuggled String Literal Injections**: AST sanitization and string literal token replacement before critic evaluation.
- `NC-06`: **NO Unseeded Randomness or Floating-Point Time in Simulation Kernels**: Discrete integer ticks and pinned `SeedSequence` PRNGs.
- `NC-07`: **NO File-Polling Inter-Process Communication (IPC)**: In-memory async message queues (ZeroMQ/AsyncIO) only.
- `NC-08`: **NO Inverted or Rank-Indexed Recency Decay Formulations**: Exponential decay over verified elapsed simulation ticks ($\lambda^{\Delta T}$).
- `NC-09`: **NO Ungrounded Homogeneous Multi-Agent Debate Loops**: Require model heterogeneity and deterministic validation tools at each round.
- `NC-10`: **NO Compute-Unnormalized Multi-Agent Comparative Claims**: Mandatory single-agent control ($B1-SC$) matched at equal token spend $\pm 10\%$.
- `NC-11`: **NO Unbudgeted or Uncapped Dynamic Agent Spawning**: Hard static ceilings on agent count, tree depth, and total tokens.
- `NC-12`: **NO Irreversible Early Pruning of Safety/Auditor Roles**: Safety and verification roles must be declared `unprunable: true`.
- `NC-13`: **NO Persistent Cross-Run Memory or Context Carryover**: Ephemeral execution containers with tmpfs memory mounts purged post-run.
- `NC-14`: **NO Self-Approval or Cryptographic Role Aliasing**: Cryptographic invariant: $\operatorname{AuthorIdentity} \neq \operatorname{ReviewerIdentity}$.
- `NC-15`: **NO Floating Model Endpoints or Unpinned Checkpoint Hashes**: Exact immutable snapshot dates and system fingerprint validation.
- `NC-16`: **NO Unconstrained Sandbox Tool Execution Resource Budgets**: Enforce strict CPU timeout (60s), RSS (512MB), and `--network none`.

### 2.2 Gate R1 Methodological & Process Constraints (NC-17 to NC-23)
- `NC-17`: **No Schema-Only Validation**: Require substantive independent review beyond syntactic checks.
- `NC-18`: **Canonical Lifecycle Transition**: State updates must occur atomically upon gate closure.
- `NC-19`: **Strict Mathematical Language**: Distinguish polynomial ($\mathcal{O}(N^2)$) from exponential scaling.
- `NC-20`: **Comprehensive Code Verification**: Trace complete call trees before claiming an implementation gap.
- `NC-21`: **Bounded Benchmark Generalization**: Do not generalize closed reasoning results to social multi-agent simulations.
- `NC-22`: **Substrate vs. Primitive Decoupling**: Separate legacy framework rejection from underlying cognitive primitive validity.
- `NC-23`: **Truth-Driven Audit Assertions**: Query canonical registers dynamically rather than hardcoding regex assumptions.

### 2.3 Gate R2 Reproduction Design Constraints (NC-24 to NC-30)
- `NC-24`: **Minimum Harness Constraint**: Build minimal micro-benchmarks ($\le 300$ lines), never full game worlds.
- `NC-25`: **Deterministic Priority Constraint**: Deterministic assertions and tests always take precedence over subjective LLM judges.
- `NC-26`: **Compute Equivalence Constraint**: Multi-agent comparisons require both call-matched and token-matched $B1-SC$ controls.
- `NC-27`: **Network Egress Firewall & Zero Data Retention**: API calls must pass `store: false` to prevent benchmark leakage.
- `NC-28`: **Failure Pre-Registration Constraint**: Automated run invalidation on model drift (`FM-06`), prompt leakage (`FM-07`), or data contamination (`FM-12`).
- `NC-29`: **Architecture Firewall Invariant**: Reproduction harnesses must not dictate final SimLab schemas; architecture remains `UNFROZEN`.
- `NC-30`: **Execution Authorization Boundary**: Never proceed to execution without explicit requester approval.

### 2.4 Gate R3 Controlled Execution Constraints (NC-31 to NC-40)
- `NC-31`: **Relevance Dominance Invariant**: Never implement memory retrieval scoring where recency or importance weights equal or exceed semantic relevance ($\beta$ must be $\ge 2\alpha$).
- `NC-32`: **Debate Scope Constraint**: Never deploy multi-agent debate for closed symbolic reasoning; restrict debate strictly to partitioned-information, asymmetric-tool, or distributed-observation tasks.
- `NC-33`: **Domain-Scoped SOP Constraint**: Never impose assembly-line sequential SOP phase gates on open-ended emergent social interactions.
- `NC-34`: **Heuristic-First Routing Constraint**: Never deploy neural or reinforcement-learned agent routing without first demonstrating that static and multi-feature heuristic routers fail.
- `NC-35`: **Dual-Control Matching Constraint**: Every future multi-agent evaluation must include both call-matched and token-matched single-agent controls ($B1-SC$).
- `NC-36`: **Non-Parametric Token Audit Constraint**: Always test token distributions for normality; use Kruskal-Wallis or Mann-Whitney U when token data is skewed.
- `NC-37`: **Complexity Burden Invariant**: The burden of proof belongs to additional architectural complexity. If a simpler baseline satisfies success thresholds, halt escalation immediately.
- `NC-38`: **Pre-Call Projection Constraint**: Every execution harness must compute projected spend before every paid call to prevent budget overrun.
- `NC-39`: **Model Pinned Fingerprint Invariant**: Never execute experiments against unpinned model checkpoints; track provider system fingerprints.
- `NC-40`: **Phase 4 Authorization Boundary**: Never proceed to Phase 4 ablation testing without explicit, separate human requester authorization.

### 2.5 Gate R3 Post-Reconciliation Statistical Integrity Constraints (NC-41 to NC-51)
- `NC-41`: **Layered Verification Separation Invariant**: Deterministic package audits verify artifact presence and schema integrity only; they do not prove scientific truth or validate substantive mathematical conclusions. Layer A and Layer B must always remain distinct.
- `NC-42`: **Lifecycle Adjudication Decoupling**: Deterministic audit completion certifies `DETERMINISTIC_AUDIT: PASS` and readiness for adjudication, not `GATE_COMPLETE`. Gate closure requires explicit substantive adjudication.
- `NC-43`: **Stopping-Rule Non-Inferiority Invariant**: Invoking a pre-registered stopping rule (e.g. `STOP_ESCALATION`) establishes that further complexity was unjustified for the evaluated workload; it does not prove that unexecuted treatments are inferior, harmful, or rejected. Unexecuted treatments must be classified strictly as `NOT_TESTED_DUE_TO_STOPPING_RULE`.
- `NC-44`: **Raw Provenance Traceability Constraint**: Every reported aggregate percentage or effect size must remain strictly traceable to raw numerators, denominators, and sample sizes in immutable telemetry. Provisional narrative estimates must never be substituted for empirical counts.
- `NC-45`: **Rigorous Equivalence Specification**: Claims of equivalence must specify explicit pre-registered equivalence bounds ($\delta$) and report both one-sided tests (TOST), confidence intervals, and power.
- `NC-46`: **Mandatory External Validity Delimitation**: Every architecture-relevant finding must be accompanied by explicit negative boundaries stating what the result does *not* support and where generalization is forbidden.
- `NC-47`: **Statistical Significance Threshold Integrity**: Never declare a result statistically significant if the empirical p-value exceeds the pre-registered significance threshold ($p > \alpha$). Large effect sizes that fail the pre-registered alpha must be classified as `PROMISING_BUT_NOT_SIGNIFICANT` or `INSUFFICIENT_EVIDENCE`.
- `NC-48`: **Equivalence Test Discipline (Anti-TOST-Inversion)**: Never interpret a failed equivalence test ($p_{TOST} \ge \alpha$) as evidence of equivalence. Furthermore, absence of established equivalence is not evidence of difference or superiority; classify strictly as `EQUIVALENCE_NOT_ESTABLISHED`.
- `NC-49`: **Prohibition on Post-Hoc Threshold Adjustment**: Evaluators and researchers must never lower alpha, expand equivalence margins ($\delta$), or alter stopping criteria after observing experimental data. Pre-registered thresholds outrank attractive results.
- `NC-50`: **Grounded Stopping-Rule Documentation**: Stopping-rule invocations (e.g. `STOP_ESCALATION`) must cite the exact pre-registered cost, quality, and overhead thresholds and verify that quality-loss tolerances were strictly respected.
- `NC-51`: **Statistical-First Narrative Alignment**: Narrative conclusions, executive summaries, and walkthroughs must derive directly and conservatively from canonical statistical test outcomes, never inflating tentative or sub-threshold empirical findings into ungrounded claims of victory.

### 2.6 Phase 4 Ablation & Stress Design Constraints (NC-52 to NC-60)
- `NC-52`: **Power-Driven Sample Size Invariant**: Never select sample sizes arbitrarily for replication or ablation studies; sample size ($N$) must derive from formal statistical power calculations ($1-eta \ge 0.85$) based on observed effect sizes and variance.
- `NC-53`: **Univariate Ablation Priority**: Every component ablation must isolate and manipulate exactly one architectural variable at a time, holding all prompts, models, parameters, and budgets constant. Multivariant changes are forbidden unless an explicit factorial interaction design is pre-registered.
- `NC-54`: **Progressive Stress Escalation Constraint**: Stress testing must progress incrementally through discrete levels (Baseline $	o$ Mild $	o$ Moderate $	o$ Severe) and must halt immediately once a failure boundary is established. Burning compute beyond the failure cliff is prohibited.
- `NC-55`: **Non-Universal Generalization Invariant**: Never extrapolate a micro-benchmark ablation result into a global architectural claim. Every experimental finding must be explicitly bounded to its tested domain, scale, and workload.
- `NC-56`: **Information Asymmetry Quantification**: Multi-agent collaboration must not be evaluated without an explicit, quantifiable metric of information partitioning or tool specialization. Homogeneous shared-context debate must not be presumed to generate collaborative surplus.
- `NC-57`: **Scale-Bounded Stress Testing**: Stress testing of agent populations must follow empirical justification ($1 	o 3 	o 5 	o 10 	o 25$). Testing 50+ agent populations is forbidden during Phase 4 unless 25-agent workloads demonstrate sustained surplus.
- `NC-58`: **SOP Context Boundary Decoupling**: In structured collaboration evaluations, implementers must explicitly distinguish the effect of semantic role specialization from the effect of phase-gated context resets.
- `NC-59`: **Routing Escalation Burden**: Complex neural or learned meta-orchestrators (e.g. Puppeteer) must never be deployed unless multi-feature heuristic routing empirically fails pre-registered stress thresholds.
- `NC-60`: **Phase 4 Execution Firewall**: The completion and certification of Phase 4 design (`PHASE_4_DESIGN`) strictly authorizes design specifications; it does NOT grant execution authority. Live experiment execution requires separate, explicit human requester authorization.
