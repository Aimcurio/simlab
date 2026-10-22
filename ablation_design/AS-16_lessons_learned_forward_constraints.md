# AS-16: Lessons Learned & Operational Forward Constraints
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

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

#### 2.6 Phase 4 Ablation & Stress Design Constraints (NC-52 to NC-60)
- `NC-52`: **Power-Driven Sample Size Invariant**: Never select sample sizes arbitrarily for replication or ablation studies; sample size ($N$) must derive from formal statistical power calculations ($1- \beta \ge 0.85$) based on observed effect sizes and variance.
- `NC-53`: **Univariate Ablation Priority**: Every component ablation must isolate and manipulate exactly one architectural variable at a time, holding all prompts, models, parameters, and budgets constant. Multivariant changes are forbidden unless an explicit factorial interaction design is pre-registered.
- `NC-54`: **Progressive Stress Escalation Constraint**: Stress testing must progress incrementally through discrete levels (Baseline $\to$ Mild $\to$ Moderate $\to$ Severe) and must halt immediately once a failure boundary is established. Burning compute beyond the failure cliff is prohibited.
- `NC-55`: **Non-Universal Generalization Invariant**: Never extrapolate a micro-benchmark ablation result into a global architectural claim. Every experimental finding must be explicitly bounded to its tested domain, scale, and workload.
- `NC-56`: **Information Asymmetry Quantification**: Multi-agent collaboration must not be evaluated without an explicit, quantifiable metric of information partitioning or tool specialization. Homogeneous shared-context debate must not be presumed to generate collaborative surplus.
- `NC-57`: **Scale-Bounded Stress Testing**: Stress testing of agent populations must follow empirical justification ($1 \to 3 \to 5 \to 10 \to 25$). Testing 50+ agent populations is forbidden during Phase 4 unless 25-agent workloads demonstrate sustained surplus.
- `NC-58`: **SOP Context Boundary Decoupling**: In structured collaboration evaluations, implementers must explicitly distinguish the effect of semantic role specialization from the effect of phase-gated context resets.
- `NC-59`: **Routing Escalation Burden**: Complex neural or learned meta-orchestrators (e.g. Puppeteer) must never be deployed unless multi-feature heuristic routing empirically fails pre-registered stress thresholds.
- `NC-60`: **Phase 4 Execution Firewall**: The completion and certification of Phase 4 design (`PHASE_4_DESIGN`) strictly authorizes design specifications; it does NOT grant execution authority. Live experiment execution requires separate, explicit human requester authorization.

### 2.7 Phase 4 Design Hardening & Epistemic Governance Constraints (NC-61 to NC-70)
- `NC-61`: **Canonical Gate Disambiguation Invariant**: The pre-execution design certification gate is designated `PHASE_4_DESIGN_GATE` (alias: `GATE_R4D`) with allowed outcomes `CONTINUE_PHASE4_DESIGN`, `INSUFFICIENT_ABLATION_DESIGN`, and `READY_FOR_ABLATION_EXECUTION`. The identifier `GATE_R4` is strictly reserved for post-ablation and stress testing execution adjudication.
- `NC-62`: **Confirmatory Replication Immutability Contract**: Any experiment designated as a confirmatory replication (specifically `EXP-AB-02-REP`, $N=650$ instances / $1,300$ paired episodes) must freeze twelve core methodological fields: hypothesis, null hypothesis, effect definition, primary outcome, task generation process, model/version, prompt structure, compute matching rule, primary statistical test, alpha, multiple-comparison policy, and stopping rule. Only sample size ($N$) may be adjusted via preregistered power analysis. Any alteration to these twelve fields automatically reclassifies the study as `AMENDED_REPLICATION` and triggers `EXPERIMENT_AMENDMENT_REQUIRED`.
- `NC-63`: **Multi-Trigger Stress Escalation & Practical-Significance Rule**: Stress testing must follow the three-stage protocol: $\text{SCREEN} \to \text{ESCALATE} \to \text{INTERACTION\_TEST}$. Stage A testing is capped at $\le 2$ simultaneous factors. Generating an unconstrained Cartesian product across the eight stress dimensions ($58,320$ potential cells) is strictly prohibited. Escalation across tiers is authorized when ANY ONE of three preregistered triggers is satisfied: (A) Practical Degradation Trigger (practical degradation or failure threshold crossed); (B) Statistical Trigger (material effect under preregistered test); OR (C) Mechanistic Failure Trigger (scientifically important failure mode explicitly logged with identified causal mechanism and justified bounded follow-up; zero unrestricted expansion). Escalating solely because $p < \alpha$ when the observed effect is operationally trivial is strictly prohibited.
- `NC-64`: **Mandatory Stress Metadata Declaration**: Every stress experiment must declare five mandatory governance metadata fields: `number_of_active_factors`, `reason_for_combination`, `interaction_hypothesis`, `maximum_stress_level`, and `early_stop_rule`.
- `NC-65`: **Stress Termination Contract & Anti-Waste Rule**: Every stress protocol must preregister four discrete stress tiers (`BASELINE`, `MILD`, `MODERATE`, `SEVERE`) and define four quantitative thresholds (`failure_threshold`, `degradation_threshold`, `abort_threshold`, `recovery_threshold`). Testing must halt immediately when the failure boundary is mapped, a safety/budget limit is reached, or further testing cannot alter the architectural conclusion. Testing to maximum stress merely because the level exists is prohibited.
- `NC-66`: **Primitive Advancement Seven-Criteria Gate**: Prior to Phase 4 execution, advancement of any primitive to Primitive Adjudication requires satisfying all seven criteria: Reproduction Evidence (A: A1 Phase 3 supported OR A2 Phase 4 confirmatory replication at $\alpha=0.01$ and $\Delta \ge +10.0\%$, transitioning `PROMISING_BUT_NOT_SIGNIFICANT` $\to$ `CONFIRMED_BY_PHASE4_REPLICATION`), Ablation Evidence (B), Stress Evidence (C), Failure Boundary (D), Cost/Complexity (E), Confound Status (F), and External Validity (G). Primitives failing any criterion must be categorized as `SUPPORTED_WITH_CONSTRAINTS`, `CONTEXT_DEPENDENT`, `DEFER`, `REJECT`, or `INSUFFICIENT_EVIDENCE`. Post-hoc rule modification after observing data is strictly forbidden.
- `NC-67`: **Causal Claim Discipline Invariant**: Ablation findings support only bounded causal attribution under tested conditions (e.g. "Removing X reduced Y under Z"). They never justify universal claims of necessity. Every ablation must publish five explicit claim bounds: `causal_claim_supported`, `causal_claim_not_supported`, `tested_context`, `untested_context`, and `interaction_risks`.
- `NC-68`: **Power Method Classification & Winner's Curse Discounting**: Confirmatory power calculations must never use raw exploratory point estimates from prior phases without accounting for winner's curse and regression to the mean (minimum $25\%$ shrinkage discount, e.g. Phase 3 $\Delta=+14\%$ discounted by $28.5\%$ to $\Delta=+10\%$, yielding $N=650$ instances). Power methods must be named accurately according to what they actually compute: the asymptotic normal derivation is classified as `ASYMPTOTIC_MCNEMAR_POWER_APPROXIMATION` (not "exact"), and must be independently verified via `EXACT_BINOMIAL_MCNEMAR_POWER` and `SIMULATION_BASED_PAIRED_POWER`.
- `NC-69`: **Router Stopping-Rule Preservation Firewall**: `LLM_ROUTER` and `LEARNED_PUPPETEER_ROUTING` remain classified as `NOT_TESTED_DUE_TO_STOPPING_RULE`. They must not be tested for completeness. Testing them is authorized only if `HEURISTIC_ROUTING` fails preregistered stress criteria under canonical amendment `PHASE4_ESCALATION_RULE_AMENDMENT` (Trigger A: accuracy loss $> 10\%$ OR under-activation $> 15\%$; Trigger B: $p < 0.01$ with $\Delta \ge 5.0\%$; Trigger C: bounded mechanistic failure trigger). The historical conjunctive rule from commit `5d7b1ab` (`accuracy loss > 10% AND under-activation > 15%`) is classified as `SUPERSEDED_RULE`.
- `NC-70`: **Curo Core Lifecycle Invariant**: Reproduction establishes that an effect may exist; Ablation identifies which component contributes to it; Stress testing establishes its operating envelope; Primitive Adjudication may advance only evidence that survives all three under preregistered criteria.

