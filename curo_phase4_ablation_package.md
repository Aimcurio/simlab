# CURO SIMLAB — PHASE 4 COMPLETE ABLATION & STRESS TEST SPECIFICATION PACKAGE
> **Compiled Master Document**
> **Lifecycle State**: PHASE_4_DESIGN_COMPLETE
> **Design Gate**: PHASE_4_DESIGN_GATE (Alias: GATE_R4D)
> **Adjudication Gate Status**: GATE_R4 strictly reserved for post-ablation/stress execution adjudication
> **Architecture Status**: UNFROZEN
> **Final SimLab Implementation Authority**: NOT_GRANTED
> **Phase 4 Execution Authority**: NOT_GRANTED

---

# AS-01: Ablation Priority Matrix
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  
**Evaluation Standard**: Qualitative multi-criteria ranking across 8 governance dimensions.  

---

## 1. Prioritization Methodology

Phase 4 ablations and stress tests are prioritized according to:
1. **Architecture Importance**: Impact on eventual 25+ agent persistent simulator design.
2. **Phase 3 Uncertainty**: Degree of statistical ambiguity or sub-threshold outcome in Phase 3.
3. **Failure Severity**: Risk of catastrophic simulation failure (e.g. context explosion, consensus collapse, silent memory corruption).
4. **Cost & Latency**: Feasibility within the $100.00 hard budget ceiling and execution time limits.
5. **Scientific Discriminability**: Ability to isolate the exact causal mechanism behind observed effects.
6. **Transferability**: Relevance across diverse NPC cognitive and organizational domains.
7. **Interaction Risk**: Likelihood of confounding interactions when combined with other primitives.
8. **Falsification Power**: Ability to disprove popular but ungrounded multi-agent literature assumptions.

Qualitative Priority Classes: `CRITICAL`, `HIGH_VALUE`, `USEFUL`, `DEFER`, `REJECT`.

---

## 2. Priority Ranking Table

| Candidate / Target | Target ID | Priority Class | Primary Rationale & Falsification Target | Target Deliverable |
|:---|:---|:---|:---|:---|
| **Private-Information Replication** | `EXP-AB-02-REP` | **`CRITICAL`** | Phase 3 showed promising $+14.0\%$ gain but missed $\alpha = 0.01$ ($p=0.0192$). Confirmatory replication subject to strict immutability contract (12 frozen fields; sample size via power analysis discounting winner's curse). | `AS-05`, `AS-12` |
| **Memory Component Ablation** | `EXP-AB-01-COMP`| **`CRITICAL`** | Determine whether recency, relevance, or importance drives retrieval quality. Phase 3 disproved equal weights; must map the exact mathematical weighting boundary ($\beta > \alpha$). Bound to causal claim discipline. | `AS-03`, `AS-18` |
| **SOP Factorial Decomposition** | `EXP-AB-03-FACT`| **`CRITICAL`** | Disentangle role specialization from phase-gated context resets ($49.2\%$ token savings). Determine whether savings come from context resets or role prompts. Bound to causal claim discipline. | `AS-07`, `AS-18` |
| **Information Asymmetry Gradient**| `EXP-AB-02-ASYM`| **`HIGH_VALUE`**| Sweep private information ($0\%, 25\%, 50\%, 75\%, 100\%$) to find the exact phase transition where multi-agent coordination becomes worth its communication overhead. Bound by explosion screening rules. | `AS-05`, `AS-11` |
| **Memory Scale & Noise Stress** | `EXP-ST-01-SCALE`| **`HIGH_VALUE`**| Stress memory stores from 100 to 10,000+ nodes under noise (duplicates, contradictions, stale records) to locate retrieval breakdown cliff. Governed by Stress Termination Contract. | `AS-04`, `AS-14` |
| **Routing Feature Ablation** | `EXP-AB-04-FEAT`| **`HIGH_VALUE`**| Determine which heuristic features (length, syntax, constraints) drove $27.8\%$ token savings in Phase 3. Preserve simple heuristics; enforce Complexity Burden Rule. | `AS-09`, `AS-10` |
| **Distributed State Tracking Stress**| `EXP-ST-02-STATE`| **`HIGH_VALUE`**| Stress agent population ($1 \to 3 \to 5 \to 10 \to 25$) and observation noise on state tracking where Phase 3 confirmed significant debate advantage ($+18.0\%$). Factorial interaction bounded by Stage C controls. | `AS-06`, `AS-11` |
| **SOP Open-Ended Stress** | `EXP-ST-03-SOP` | **`USEFUL`** | Test whether assembly-line SOPs break under ambiguous or exploratory requirements; verify negative boundary against social simulation. Bounded by early stop rules. | `AS-08`, `AS-14` |
| **Routing Distribution Shift Stress**| `EXP-ST-04-SHIFT`| **`USEFUL`** | Stress heuristic routing under unseen task domains to test Complexity Escalation Rule threshold. Governed by SCREEN $\to$ ESCALATE $\to$ INTERACTION_TEST protocol. | `AS-10`, `AS-11` |
| **Reflection Node Contamination** | `EXP-AB-01-REFL`| **`USEFUL`** | Test whether synthesized reflection nodes act as semantic attractors that crowd out episodic memories. Offline vector evaluation. | `AS-03`, `AS-18` |
| **50+ Agent Population Stress** | `EXP-ST-SYS-50` | **`DEFER`** | Deferred to Phase 8 scale testing. 25-agent stability must be established first. | `AS-11` |
| **Learned Puppeteer Router** | `EXP-AB-04-PUPP`| **`DEFER`** | Classified strictly as `NOT_TESTED_DUE_TO_STOPPING_RULE`. Escalation authorized ONLY if heuristic routing fails preregistered stress criteria or approved hypothesis requires comparison. | `AS-10` |
| **Homogeneous GSM8K Debate** | `EXP-AB-02-GSM` | **`REJECT`** | Phase 3 proved TOST equivalence was not established and debate incurred an $8.2\%$ false consensus rate. Unproductive to burn tokens on closed math without tools. | `AS-05` |
| **Equal-Weighted Memory** | `EXP-AB-01-EQ` | **`REJECT`** | Empirically falsified in Phase 3 ($d=0.26$, sub-threshold). Discarded from further evaluation. | `AS-03` |

---

## 3. Governance Cross-References & Gate Constraints
- **Design Gate Clarification**: Pre-execution certification belongs strictly to `PHASE_4_DESIGN_GATE`. Post-execution outcome adjudication is reserved for `GATE_R4`.
- **Stress-Matrix Explosion Rules**: Combinatorial expansion across the 8 stress dimensions is strictly prohibited; all tests must follow the `SCREEN -> ESCALATE -> INTERACTION_TEST` protocol (`AS-11`).
- **Primitive Advancement Invariant**: Advancement to final Primitive Adjudication requires satisfying all seven criteria (A through G) in the Primitive Advancement Contract (`AS-18`).



---

# AS-02: Phase 3 Finding-to-Ablation Mapping
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Mapping Phase 3 Empirical Outcomes to Phase 4 Experimental Designs

| Phase 3 Candidate | Phase 3 Empirical Finding | Phase 3 Reconciled Status | Remaining Epistemic Unknown | Phase 4 Investigation Design |
|:---|:---|:---|:---|:---|
| **RP-01** (Memory Recency) | Corrected exponential decay dropped inversion rate $74.5\% \to 41.0\%$. Equal weighting failed ($\Delta \text{MRR} = +0.0446$); tuned weighting succeeded ($\Delta \text{MRR} = +0.1685, p < 0.001$). | `SUPPORTED_WITH_CONSTRAINTS` | Which component (recency vs relevance vs importance) is necessary and sufficient? At what memory scale does retrieval break down? | **`AS-03`** (8-Condition Component Ablation; bound to 5-field Causal Claim Discipline)<br/>**`AS-04`** (Scale 100 to 10,000+ & Noise Stress; bound to Stress Termination Contract) |
| **RP-02** (Debate vs B1-SC: Private Info) | Multi-agent debate achieved $+14.0\%$ accuracy gain ($87/100$ vs $73/100$), but $p = 0.0192 > 0.01$. Compute matched within $+2.48\%$. | `PROMISING_BUT_NOT_SIGNIFICANT` | Is the $+14.0\%$ advantage reproducible at $\alpha = 0.01$ under adequate statistical power? At what degree of information asymmetry does debate become useful? | **`AS-05`** (Confirmatory Replication $N=300$; bound to 12-field Immutability Contract; Asymmetry Gradient Sweep $0\%\dots100\%$) |
| **RP-02** (Debate vs B1-SC: Closed GSM8K) | Difference was $+4.40\%$ ($446/500$ vs $424/500$). TOST failed to establish equivalence at $\delta = \pm 0.03$ ($p = 0.741$). False consensus observed in $8.2\%$ of runs. | `EQUIVALENCE_NOT_ESTABLISHED` | Does debate provide any genuine reasoning amplification or merely introduce sycophancy risk on closed tasks? | **`AS-05`** (Closed reasoning deprioritized; focused on partitioned knowledge boundaries; anti-sycophancy constraints) |
| **RP-02** (Debate vs B1-SC: State Tracking) | Multi-agent debate achieved $+18.0\%$ accuracy gain ($84/100$ vs $66/100$, $p = 0.0051 < 0.01$) on distributed state tracking. | `SUPPORTED` | How robust is multi-agent state tracking as agent count grows ($1 \to 25$) and observation noise increases? | **`AS-06`** (Population Sweep $1\dots25$ & Partial Observation Stress; Stage C interaction controls) |
| **RP-03** (ChatDev Phased SOPs) | Phase boundaries cut tokens by $49.17\%$ ($p < 10^{-14}$) and eliminated cross-role violations ($1.80 \to 0.00$) with $+6.15\%$ pass rate. | `SUPPORTED_WITH_CONSTRAINTS` | Are savings driven by role specialization, phase-gated context pruning, or both? Does structure harm exploratory tasks? | **`AS-07`** ($2 \times 2$ Factorial Component Ablation; Causal Claim Discipline)<br/>**`AS-08`** (Ambiguous & Exploratory Task Stress; Termination Contract) |
| **RP-04** (Dynamic Orchestration) | Heuristic routing saved $27.80\%$ tokens with $-2.0\%$ accuracy loss. `STOP_ESCALATION_VALID` invoked. Higher tiers not executed. | `SUPPORTED_WITH_CONSTRAINTS` | Which heuristic features drive efficiency? Under what task distribution shift does heuristic routing fail badly enough to justify neural routing? | **`AS-09`** (Leave-One-Out Feature Ablation)<br/>**`AS-10`** (Adversarial Distribution Shift Stress; Complexity Escalation Rule preserved) |

---

## 2. Invariant Epistemic Governance
- **Confirmatory Replication Immutability**: RP-02 replication requires exact adherence to the 12 frozen protocol fields (`AS-05`). Any modification converts the classification to `AMENDED_REPLICATION` requiring `EXPERIMENT_AMENDMENT_REQUIRED`.
- **Advancement Prerequisite**: No Phase 3 finding automatically promotes a primitive to final architecture. Advancement to Primitive Adjudication requires satisfying all seven criteria (A through G) defined in `AS-18`.



---

# AS-03: Memory Component Ablation Plan
**Experiment ID**: `EXP-AB-01-COMP`  
**Target Primitive**: `PR-COG-01` (Tri-Factor Memory Retrieval Scoring)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
Which specific mathematical components and weighting strategies of the tri-factor memory retrieval scoring function ($s = \alpha s_{rec} + \beta s_{rel} + \gamma s_{imp}$) are causally responsible for high retrieval precision, and does adding synthesized reflection nodes improve or contaminate retrieval?

---

## 2. Experimental Design (8 Controlled Conditions)

All conditions run against the standardized `SimLab-MemBench-500` benchmark ($N=100$ recency-sensitive, relevance-dominant, and conflict queries). All embeddings are pre-computed using pinned text embedding vectors. Zero runtime LLM inference calls are required.

| Condition Code | Condition Name | Scoring Formulation | Theoretical Purpose | Success / Falsification Criteria |
|:---|:---|:---|:---|:---|
| **A1** | `RECENCY_ONLY` | $s = s_{rec} = \lambda^{\Delta t}$ | Isolate temporal decay without semantic grounding. | Falsify whether pure recency produces coherent retrieval. |
| **A2** | `RELEVANCE_ONLY` | $s = s_{rel} = \cos(\mathbf{q}, \mathbf{m})$ | Traditional dense vector similarity baseline. | Benchmark baseline for pure semantic search. |
| **A3** | `IMPORTANCE_ONLY`| $s = s_{imp} = \text{score}_{\text{prompt}}$ | Static salience retrieval. | Falsify whether high-importance memories alone suffice. |
| **A4** | `RECENCY_RELEVANCE`| $s = 0.3 s_{rec} + 0.7 s_{rel}$ | Test temporal decay combined strictly with semantics. | Measure whether importance is an unnecessary parameter. |
| **A5** | `RECENCY_IMPORTANCE`| $s = 0.5 s_{rec} + 0.5 s_{imp}$ | Non-semantic heuristic retrieval. | Falsify non-vector retrieval mechanisms. |
| **A6** | `RELEVANCE_IMPORTANCE`| $s = 0.7 s_{rel} + 0.3 s_{imp}$ | Standard RAG with static priority weighting. | Test whether temporal decay is strictly necessary. |
| **A7** | `FULL_TRI_FACTOR` | $s = 0.2 s_{rec} + 0.5 s_{rel} + 0.3 s_{imp}$ | Reconciled Phase 3 tuned weighting configuration. | Benchmark for full tri-factor interaction. |
| **A8** | `TRI_FACTOR_REFLECTION`| A7 scoring over memory store including $20\%$ synthesized reflection nodes | Evaluate reflection impact on retrieval. | Test whether reflection nodes boost NDCG or crowd out ground-truth episodic memories. |

---

## 3. Weighting Simplex Sweep
In addition to discrete conditions A1–A8, a continuous 2D simplex grid search over normalized weights $\alpha + \beta + \gamma = 1.0$ (step size $\Delta = 0.1$, 66 grid points) will be evaluated across all queries to map the exact mathematical boundary where $\beta$ ceases to dominate and retrieval degrades.

---

## 4. Primary Metrics & Hypotheses
- **Primary Metric**: Mean Reciprocal Rank (MRR) and NDCG@5.
- **Hypothesis ($H_1$)**: Condition A4 (`RECENCY_RELEVANCE`) achieves non-inferior MRR compared to A7 (`FULL_TRI_FACTOR`) within $\Delta \le 0.02$, proving that static importance scores add negligible marginal value over semantics and recency.
- **Null Hypothesis ($H_0$)**: Importance weighting is strictly necessary ($\text{MRR}_{A7} - \text{MRR}_{A4} \ge +0.05, p < 0.0025$).
- **Statistical Test**: Paired Wilcoxon signed-rank test with Bonferroni correction ($\alpha = 0.01 / 7 = 0.0014$).

---

## 5. Causal Claim Discipline
- `causal_claim_supported`: "Removing prompt-based importance scores from tri-factor memory retrieval produces no statistically significant degradation in MRR ($\Delta \text{MRR} \le 0.02$) under offline semantic retrieval across the tested queries."
- `causal_claim_not_supported`: "Prompt-based importance scoring is universally useless across all cognitive agent simulation architectures."
- `tested_context`: Standardized 500-node episodic memory store, cosine similarity dense embeddings, exponential tick decay ($\lambda = 0.995$).
- `untested_context`: Dynamic multi-agent social games with real-time goal revisions, stores $> 10,000$ memories, graph-structured knowledge stores.
- `interaction_risks`: When importance weighting is eliminated, synthesized reflection nodes may lose tie-breaking salience against dense episodic distractors.



---

# AS-04: Memory Stress Plan
**Experiment ID**: `EXP-ST-01-SCALE`  
**Target Primitive**: `PR-COG-01` (Tri-Factor Memory Retrieval Scoring)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
At what memory store scale ($M$), temporal horizon ($T$), and noise ratio ($\eta$) does tri-factor memory retrieval collapse, and what is the computational and accuracy cost of memory growth?

---

## 2. Stress-Matrix Explosion Controls (`SCREEN -> ESCALATE -> INTERACTION_TEST`)

- **Stage A (Screening)**: Evaluate Memory Scale alone ($M \in \{100, 500, 1000\}$) and Noise alone ($\eta \in \{0\%, 10\%, 30\%\}$).
- **Stage B (Escalation)**: Escalate to combined $M \times \eta$ only across confirmed sensitivity ranges.

### Experiment Metadata Contract:
- `number_of_active_factors`: 2 active factors (Store Volume $M$ + Noise Ratio $\eta$).
- `reason_for_combination`: High store volume increases vector crowding, which magnifies semantic interference from lexical distractors.
- `interaction_hypothesis`: Retrieval precision exhibits a non-linear cliff when memory size exceeds $1,000$ nodes in the presence of $\ge 30\%$ distractor noise.
- `maximum_stress_level`: `SEVERE` ($M=5,000$, 50% noise).
- `early_stop_rule`: Terminate experiment immediately if single-query CPU latency exceeds $50$ms or if false retrieval rate crosses $40.0\%$.

---

## 3. Stress Progression & Termination Contract

### 3.1 Pre-Registered Stress Levels:
1. **`BASELINE`**: $M=100$ nodes, 0% noise, short temporal horizon ($\Delta t \le 50$).
2. **`MILD`**: $M=500$ nodes, 10% distractor noise, medium horizon ($\Delta t \le 500$).
3. **`MODERATE`**: $M=1,000$ nodes, 30% noise (duplicates + contradictory facts), medium horizon.
4. **`SEVERE`**: $M=5,000$ nodes, 50% noise (including misleading high-importance lures), long horizon ($\Delta t \le 5,000$).

### 3.2 Quantitative Threshold Contracts:
- `statistical_threshold`: Degradation significance at $\alpha = 0.01$ across $N \ge 100$ queries per condition, demonstrating a material statistical effect.
- `practical_degradation_threshold`: MRR drops $> 20.0\%$ from baseline OR single-query retrieval CPU latency exceeds $20$ms.
- `failure_threshold`: MRR drops below $0.10$ ($p < 0.01$) **OR** false retrieval rate exceeds $40.0\%$. (Establishes the primitive's operational capacity boundary).
- `mechanistic_failure_trigger`: Memory corruption causes deterministic stale retrieval, key invariant collapse, or catastrophic semantic index poisoning under distractor lures even when sample size is insufficient for formal significance. Must be explicitly logged, identify the observed failure mechanism, justify the bounded follow-up, and not permit unrestricted exploratory expansion.
- `escalation_rule`: Escalate from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE of the following preregistered triggers is satisfied:
  1. **Practical Degradation Trigger**: `practical_degradation_threshold` or `failure_threshold` is crossed ($\Delta \text{MRR} > 20.0\%$ or latency $> 20$ms); **OR**
  2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < 0.01$); **OR**
  3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears (e.g. deterministic stale retrieval) justifying bounded follow-up.
  *Practical-Significance Discipline*: Escalating solely on statistical significance ($p < \alpha$) when the observed effect is operationally trivial ($\Delta \text{MRR} < 5.0\%$, latency shift $< 2$ms) is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.
- `early_stop_rule`: Terminate experiment immediately if single-query CPU latency exceeds $50$ms or if false retrieval rate crosses $40.0\%$.
- `abort_threshold`: Single-query retrieval latency $> 100$ms or memory footprint $> 1.0$ GB RAM ($AF-05$).
- `recovery_threshold`: Pruning superseded memories restores MRR to within $10\%$ of clean baseline.

### 3.3 Termination Invariant
Testing must stop when:
1. The failure boundary is established;
2. Safety or host resource constraints are reached; **OR**
3. Further stress cannot alter the architectural conclusion.

Do not execute to extreme levels ($10,000+$ nodes) unless `MODERATE` stress is survived (`NC-54`).



---

# AS-05: Multi-Agent Information-Asymmetry Plan
**Experiment IDs**: `EXP-AB-02-REP` (Confirmatory Replication) & `EXP-AB-02-ASYM` (Asymmetry Sweep)  
**Target Primitive**: `PR-ORG-01` (Multi-Agent Iterative Debate & Cross-Examination)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Confirmatory Private-Information Replication (`EXP-AB-02-REP`)

### 1.1 Phase 3 Empirical Background
In Phase 3, 3-agent debate on private-information tasks achieved an observed accuracy of $87.0\%$ vs $73.0\%$ for compute-matched single-agent $B1-SC\text{-tokens}$ ($+14.0\%$ advantage, McNemar $p = 0.0192$). Because $p = 0.0192 > \alpha = 0.01$, the result was formally classified as **`PROMISING_BUT_NOT_SIGNIFICANT`**. Phase 4 specifies a higher-powered confirmatory replication.

### 1.2 Confirmatory Replication Immutability Contract
To maintain absolute epistemic validity and prevent post-hoc protocol drift, the replication run must preserve all material experimental parameters without alteration. The following twelve fields are declared **strictly immutable**:

| # | Protocol Dimension | Immutable Field | Binding Specification in Replication (`EXP-AB-02-REP`) |
|:---|:---|:---|:---|
| 1 | **Hypothesis** | `hypothesis` | 3-agent cross-examination debate achieves superior accuracy over compute-matched single-agent self-consistency ($B1-SC$) on partitioned private information. |
| 2 | **Null Hypothesis** | `null_hypothesis` | $H_0: p_{\text{debate}} \le p_{B1-SC}$ (Debate accuracy is less than or equal to $B1-SC$ control accuracy). |
| 3 | **Effect Definition** | `effect_definition` | Net accuracy difference: $\Delta = \text{Accuracy}(\text{Debate}) - \text{Accuracy}(B1-SC\text{-tokens})$. |
| 4 | **Primary Outcome** | `primary_outcome` | Binary task success (1/0) verified against deterministic ground truth clue unification assertions. |
| 5 | **Task Generation** | `task_generation_process` | Procedural private-information puzzle generator (`SimLab-PrivateInfo-Gen-v1`) with identical clue distribution schemas and random seed sequence. |
| 6 | **Model & Version** | `model_version` | Exact pinned model checkpoint: `gpt-4o-mini-2024-07-18` verified via `system_fingerprint`. Zero endpoint floating. |
| 7 | **Prompt Structure** | `prompt_structure` | Identical 3-round cross-examination debate prompt templates and identical $B1-SC$ chain-of-thought prompt templates. |
| 8 | **Compute Matching** | `compute_matching_rule` | $B1-SC\text{-tokens}$ control matched within $\pm 10\%$ of total debate tokens consumed per instance (`NC-10`, `NC-26`). |
| 9 | **Statistical Test** | `primary_statistical_test`| Two-sided paired McNemar test on discordant task pairs. |
| 10| **Significance Level** | `alpha` | Strict $\alpha = 0.01$ (anti-alpha-inflation rule `NC-47`). |
| 11| **Multi-Comparison** | `multiple_comparison_policy`| Single pre-registered primary hypothesis; zero post-hoc subgroup alpha expenditure. |
| 12| **Stopping Rule** | `stopping_rule` | Fixed sample size stopping rule; zero continuous monitoring or peek-and-stop adjustments. |

**Immutability Governance Rule**:
- **Sample size ($N$)** may change **ONLY** as determined by formal preregistered power analysis.
- If **ANY** other material element (fields 1–12) is altered, the run **MUST NOT** be classified as `CONFIRMATORY_REPLICATION`. It must be classified as **`AMENDED_REPLICATION`**, and requires an explicit **`EXPERIMENT_AMENDMENT_REQUIRED`** governance exception.

### 1.3 Independent Power Analysis Verification & Correction (`POWER_CALCULATION_CORRECTED`)
An independent mathematical recomputation of the paired binary McNemar design reveals that the provisional figure of $N=300$ is under-powered for a conservative effect size of $\Delta = +0.100$. Under the empirical Phase 3 discordance rate ($p_{\text{disc}} = 0.40$), $N=300$ achieves only $56.5\%$ two-sided power against $\Delta = +0.100$, with an MDE of $+14.0\%$.

To guarantee $90\%$ statistical power against the conservative effect threshold ($\Delta \ge +0.100$) while hedging against winner's curse and regression to the mean, the sample size is mathematically corrected as follows:

| Parameter | Specification | Empirical / Methodological Grounding |
|:---|:---|:---|
| **Expected Discordant-Pair Rate** | $p_{\text{disc}} = \mathbf{0.400}$ ($40.0\%$) | Phase 3 empirical count: $b=27, c=13 \implies b+c = 40/100$ discordant pairs. |
| **Expected b Proportion (Debate wins)** | $b = \mathbf{0.250}$ ($25.0\%$) | Derived from $(p_{\text{disc}} + \Delta) / 2 = (0.40 + 0.10) / 2$. |
| **Expected c Proportion (B1-SC wins)** | $c = \mathbf{0.150}$ ($15.0\%$) | Derived from $(p_{\text{disc}} - \Delta) / 2 = (0.40 - 0.10) / 2$. |
| **Effect Assumption ($\Delta$)** | $\Delta_{\text{conservative}} = \mathbf{+0.100}$ ($+10.0\%$) | Applies a **$28.5\%$ shrinkage discount** to the Phase 3 observed point estimate ($+14.0\%$). |
| **Significance Level ($\alpha$)** | $\alpha = \mathbf{0.010}$ | Strictly preserved significance standard (`NC-47`). |
| **Statistical Power ($1 - \beta$)** | $1 - \beta = \mathbf{0.900}$ ($90.0\%$) | Minimizes Type II error on primary architecture gatekeeper. |
| **One-Sided / Two-Sided Status** | **Two-Sided** ($z_{\alpha/2} = 2.576$) | Preserves conservative two-sided inference. (One-sided $z=2.326$ yields $N_{\text{base}}=516$). |
| **Multiple-Comparison Adjustment** | None ($\alpha = 0.01$ dedicated) | Single primary confirmatory hypothesis; zero subgroup alpha expenditure. |
| **Power Calculation Method** | `ASYMPTOTIC_MCNEMAR_POWER_APPROXIMATION` | Connor (1987) / Lachin (1992) normal approximation formula. Independently verified via `EXACT_BINOMIAL_MCNEMAR_POWER` ($92.35\%$ achieved) and `SIMULATION_BASED_PAIRED_POWER` ($92.36\%$ achieved). |
| **Base Sample-Size Formula** | Asymptotic Approximation ($N_{\text{base}}$) | $N_{\text{base}} = \frac{\left(z_{\alpha/2}\sqrt{p_{\text{disc}}} + z_{\beta}\sqrt{p_{\text{disc}} - \Delta^2}\right)^2}{\Delta^2} = \frac{(2.576\sqrt{0.40} + 1.282\sqrt{0.39})^2}{0.01} = \mathbf{591 \text{ pairs}}$. |
| **Invalid-Run Allowance** | $+10.0\%$ buffer ($+59$ pairs) | Over-recruitment buffer covering parsing failures, API drops, or timeouts. |
| **Resulting Minimum Sample Size** | $\mathbf{N = 650 \text{ problem instances}}$ | **$1,300$ paired episodes** ($650$ Debate runs vs $650$ compute-matched $B1-SC$ runs). |
| **Minimum Detectable Effect (MDE)** | $\text{MDE} = \mathbf{+9.6\%}$ ($0.096$) | Smallest true effect detectable with $90\%$ probability at $\alpha=0.01$ under $N=650$. |

**Replication Decision Rule**:
- If $\Delta \ge +10.0\%$ with paired McNemar $p < 0.01$: **`CONFIRMED_EFFECT`** (Triggers status transition `CONFIRMED_BY_PHASE4_REPLICATION` under `AS-18` Criterion A2).
- If $\Delta < +10.0\%$ or $p \ge 0.01$: **`NOT_CONFIRMED`** (Debate fails confirmatory replication; primitive remains sub-threshold).


---

## 2. Causal Claim Discipline

In accordance with Phase 4 epistemic standards, experimental outcomes must not make unbounded claims of multi-agent superiority:
- **`causal_claim_supported`**: "Iterative multi-agent cross-examination debate causally improves clue unification and solution accuracy relative to compute-matched single-agent prompting when task-critical information is partitioned disjointly across participants under the tested context."
- **`causal_claim_not_supported`**: "Multi-agent debate is universally superior to single-agent prompting, or debate provides inherent reasoning amplification on closed, non-partitioned tasks."
- **`tested_context`**: 3-agent homogeneous model (`gpt-4o-mini-2024-07-18`), 3-round structured turn-taking, partitioned factual clues ($\le 5$ clues per agent), deterministic verification.
- **`untested_context`**: Open-ended socio-political dialogue, populations $> 3$ agents, heterogeneous model pairings, environments with real-time tool feedback.
- **`interaction_risks`**: Increased token cost ($3\times$ to $5\times$ base), sycophancy cascade risk where correct private clues are overridden by majority error ($8.2\%$ observed in Phase 3 GSM8K).

---

## 3. Information Asymmetry Parametric Sweep (`EXP-AB-02-ASYM`)

### 3.1 Research Objective & Stress-Matrix Controls
Identify the exact phase transition where multi-agent coordination generates a statistically significant accuracy surplus over single-agent compute-matched baselines.

**Explosion Controls & Experiment Metadata**:
- `number_of_active_factors`: 1 active factor (Asymmetry Partition Ratio).
- `reason_for_combination`: Single-factor isolation; combinatorial multi-factor interaction is deferred to Stage C.
- `interaction_hypothesis`: Net debate surplus ($\Delta \text{Acc}$) is strictly non-positive at $0\%$ asymmetry and monotonically increases with asymmetry, crossing into positive significance only when private information $\ge 50\%$.
- `maximum_stress_level`: $100\%$ asymmetry (full clue partitioning).
- `early_stop_rule`: Abort sweep if false consensus rate exceeds $35\%$ or communication cost exceeds $6.0\times$ single-agent tokens.

### 3.2 Five Asymmetry Levels
Evaluated across $N = 100$ instances per level ($500$ total instances, $1,500$ episodes):
- **Level 0 (0% Asymmetry - Full Sharing)**: 100% of clues shared; 0% private.
- **Level 1 (25% Asymmetry)**: 75% shared clues; 25% disjoint private clues.
- **Level 2 (50% Asymmetry)**: 50% shared; 50% disjoint private clues.
- **Level 3 (75% Asymmetry)**: 25% shared; 75% disjoint private clues.
- **Level 4 (100% Asymmetry - Full Partition)**: 0% shared; 100% disjoint private clues.

### 3.3 Stress Progression, Escalation & Termination Contract
- `BASELINE`: Level 0 (0% asymmetry). Expected surplus: $\Delta \le 0.0\%$.
- `MILD`: Level 1 (25% asymmetry).
- `MODERATE`: Level 2 (50% asymmetry).
- `SEVERE`: Level 4 (100% asymmetry).
- **Threshold Contracts**:
  - `statistical_threshold`: Paired McNemar test on discordant pairs achieves $p < 0.01$ with material net surplus $\Delta \ge +5.0\%$.
  - `practical_degradation_threshold`: Communication token ratio $> 4.5\times$ single-agent tokens with net surplus $\Delta < +3.0\%$ **OR** false consensus rate $> 20.0\%$.
  - `failure_threshold`: False consensus rate $\ge 35.0\%$ **OR** net accuracy loss $\Delta \le -5.0\%$ relative to single-agent baseline.
  - `mechanistic_failure_trigger`: Sycophancy cascade where majority agent overrides a correct private clue holder, resulting in collective failure even when sample size is insufficient for formal significance. Explicitly logged, bounded follow-up only.
  - `escalation_rule`: Escalate from Level 1/2 to higher asymmetry levels if ANY ONE trigger is met: (A) practical surplus appears ($\Delta \ge +5.0\%$) or token degradation occurs; (B) statistical evidence demonstrates material effect ($p < 0.01$); OR (C) mechanistic failure trigger appears. Escalation on trivial effect size ($\Delta < 1.0\%$) is prohibited.
  - `early_stop_rule`: Abort sweep if false consensus rate exceeds $35\%$ or communication cost exceeds $6.0\times$ single-agent tokens.
  - `abort_threshold`: Rate of empty or invalid debate outputs $> 10.0\%$.
  - `recovery_threshold`: Post-debate accuracy rebounds to match or exceed best individual agent clue holder.
- **Stopping Invariant**: Halt testing immediately once the phase transition boundary $A^*$ is established or budget threshold is reached; do not run redundant stress levels once the mathematical curve is identified.




---

# AS-06: Distributed-State Stress Plan
**Experiment ID**: `EXP-ST-02-STATE`  
**Target Primitive**: `PR-ORG-01` (Multi-Agent Debate & Cross-Examination)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
How does multi-agent state tracking perform as agent population scales from 1 to 25 agents, and under what levels of communication delay, agent dropout, and observation error does distributed coordination break down?

---

## 2. Stress-Matrix Explosion Controls (`SCREEN -> ESCALATE -> INTERACTION_TEST`)

- **Stage A (Screening)**: Population scaling alone ($N \in \{1, 3, 5, 10\}$) under zero noise.
- **Stage B (Escalation)**: Escalate to $N=25$ and introduce partial observation bandwidth ($\le 20\%$).
- **Stage C (Interaction Testing)**: Factorial evaluation of Population ($N=10, 25$) $\times$ Observation Noise ($\epsilon \in \{0\%, 10\%, 25\%\}$) to evaluate consensus breakdown.

### Experiment Metadata Contract:
- `number_of_active_factors`: 2 active factors (Population Size $N$ + Observation Error $\epsilon_{\text{obs}}$).
- `reason_for_combination`: Multi-agent consensus mechanisms behave differently when both participant count and observational uncertainty increase simultaneously.
- `interaction_hypothesis`: Communication overhead scales polynomially ($\mathcal{O}(N^2)$) under clean observations, but diverges into exponential message amplification when observation noise exceeds $20\%$.
- `maximum_stress_level`: `SEVERE` ($N=25$, 25% observation corruption, 10% agent dropout).
- `early_stop_rule`: Terminate experiment immediately if token consumption scales worse than $\mathcal{O}(N^2)$ or if tracking accuracy drops below compute-matched single-agent baseline.

---

## 3. Stress Progression & Termination Contract

### 3.1 Pre-Registered Stress Levels:
1. **`BASELINE`**: $N=1$ agent (baseline state tracking), full observation, 0% noise.
2. **`MILD`**: $N=3$ agents, partial observation ($33\%$ FOV each), 0% error.
3. **`MODERATE`**: $N=10$ agents, partial observation ($10\%$ FOV), 10% false-entity noise, 1-tick message delay.
4. **`SEVERE`**: $N=25$ agents, partial observation ($5\%$ FOV), 25% contradictory reports, 10% agent dropout. (50+ agents strictly deferred per `NC-57`).

### 3.2 Quantitative Threshold Contracts:
- `statistical_threshold`: Accuracy difference significant at $\alpha = 0.01$ across $N \ge 50$ episodes per population level, demonstrating a material statistical effect.
- `practical_degradation_threshold`: Tracking accuracy drops $> 10.0\%$ below nominal debate baseline OR IPC token overhead exceeds $3\times$ single-agent tokens.
- `failure_threshold`: Tracking accuracy drops below single-agent control ($< 66.0\%$) **OR** consensus latency exceeds $8$ debate rounds.
- `mechanistic_failure_trigger`: Agent dropout creates unrecoverable state divergence, broadcast loop deadlock, or split-brain world models even when sample size is insufficient for formal significance. Must be explicitly logged, identify the observed failure mechanism, justify the bounded follow-up, and not permit unrestricted exploratory expansion.
- `escalation_rule`: Escalate from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE of the following preregistered triggers is satisfied:
  1. **Practical Degradation Trigger**: `practical_degradation_threshold` or `failure_threshold` is crossed (accuracy loss $> 10.0\%$, overhead $> 3\times$, or latency $> 8$ rounds); **OR**
  2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < 0.01$); **OR**
  3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears (e.g. unrecoverable state divergence under dropout) justifying bounded follow-up.
  *Practical-Significance Discipline*: Escalating solely on statistical significance ($p < \alpha$) when the observed effect is operationally trivial (tracking accuracy loss $< 2.0\%$, token shift $< 5\%$) is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.
- `early_stop_rule`: Terminate experiment immediately if token consumption scales worse than $\mathcal{O}(N^2)$ or if tracking accuracy drops below compute-matched single-agent baseline.
- `abort_threshold`: Episode token spend exceeds $50,000$ tokens or debate loop exceeds $16$ turns ($AF-04$).
- `recovery_threshold`: Central state broadcast restores accuracy to $\ge 90.0\%$.

### 3.3 Termination Invariant
Testing must stop when:
1. The failure boundary is established;
2. Budget ceilings or token runaway limits are reached; **OR**
3. Further stress cannot alter the architectural conclusion.

Do not run to maximum population ($N=25$) under `SEVERE` noise if failure occurs at `MODERATE` ($N=10$) (`NC-54`).



---

# AS-07: SOP Component Ablation Plan
**Experiment ID**: `EXP-AB-03-FACT`  
**Target Primitive**: `PR-ORG-02` (Phased Assembly-Line SOP State Machine)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
In structured collaboration workflows (ChatDev), what proportion of the observed $49.2\%$ token savings and role-violation suppression is causally attributable to semantic role prompts versus phase-gated context pruning?

---

## 2. Experimental Design ($2 \times 2$ Factorial + Boundary Controls)

All conditions evaluate $N=100$ modular and multi-file programming tasks from `SimLab-CodeSOP-150`.

```
FACTORIAL MATRIX:
                | Roles = OFF (Homogeneous) | Roles = ON (Specialized)
----------------+---------------------------+-------------------------
Phases = OFF    | C0: Unrestricted Chat     | C1: Roles Only
Phases = ON     | C2: Phases Only           | C3: Roles + Phases (Standard SOP)
```

### Detailed Condition Specifications:
- **C0 (`UNRESTRICTED_CHAT`)**: Homogeneous agents, shared conversational context, no phase gates.
- **C1 (`ROLES_ONLY`)**: Specialized persona system prompts (CEO, CTO, Programmer, Reviewer) operating in an unconstrained shared chat history.
- **C2 (`PHASES_ONLY`)**: Homogeneous agents executing sequential phase transitions (Design $\to$ Code $\to$ Test) with clean context handoffs between phases.
- **C3 (`ROLES_AND_PHASES`)**: Standard ChatDev architecture (specialized roles + phase-gated context resets).
- **C4 (`ROLES_PHASES_CRITIC`)**: C3 supplemented with an independent adversarial critic role at each phase boundary.
- **C5 (`ARTIFACT_HANDOFF_NO_CHAT`)**: Zero multi-turn dialogue. Agents communicate strictly via structured immutable file artifacts (spec.json, code.py, test.py) passed directly to the next stage.

---

## 3. Primary Metrics & Statistical Contract
- **Token Efficiency**: Total tokens consumed per completed task.
- **Unit Test Pass Rate**: Percentage of pytest assertions passing.
- **Cross-Role Violations**: Count of turns where an agent assumes or executes another role's responsibilities.
- **Statistical Method**: Two-Way ANOVA on token consumption with main effects for $\text{Roles}$ and $\text{Phases}$, plus $\text{Roles} \times \text{Phases}$ interaction term (with Kruskal-Wallis non-parametric fallback if normality fails).
- **Pre-Registered Hypothesis ($H_1$)**: The main effect of $\text{Phases}$ accounts for $\ge 70\%$ of total token variance, proving that context boundary management, rather than role prompting, drives efficiency.

---

## 4. Causal Claim Discipline
- `causal_claim_supported`: "Sequential phase gating with context boundary resets causally accounts for the primary reduction ($\ge 70\%$) in token consumption and cross-role violations relative to unrestricted multi-turn dialogue on the evaluated code tasks."
- `causal_claim_not_supported`: "Assembly-line SOP structures and persona prompting are universally optimal across all software development or multi-agent tasks."
- `tested_context`: Modular Python programming tasks ($\le 250$ LOC), 4 distinct roles (CEO, CTO, Coder, Tester), sequential waterfall phase transitions.
- `untested_context`: Highly interdependent circular refactoring, real-time UI/UX design, emergent multi-agent social interactions.
- `interaction_risks`: Overly rigid phase boundaries prevent downstream feedback from correcting upstream architectural design bugs without costly rollback loops.



---

# AS-08: SOP Stress Plan
**Experiment ID**: `EXP-ST-03-SOP`  
**Target Primitive**: `PR-ORG-02` (Phased Assembly-Line SOP State Machine)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
Under what task conditions and team sizes does rigid assembly-line SOP structure degrade performance, induce deadlock, or fail compared to dynamic or unstructured interaction?

---

## 2. Stress-Matrix Explosion Controls (`SCREEN -> ESCALATE -> INTERACTION_TEST`)

- **Stage A (Screening)**: Test Task Ambiguity alone (Clear $\to$ Ambiguous $\to$ Exploratory).
- **Stage B (Escalation)**: Test Upstream Defect Injection under ambiguous tasks.
- **Stage C (Interaction Testing)**: Factorial evaluation of Task Ambiguity $\times$ Dynamic Requirement Shift.

### Experiment Metadata Contract:
- `number_of_active_factors`: 2 active factors (Task Ambiguity Level + Mid-Stream Requirement Shift).
- `reason_for_combination`: Waterfall pipelines exhibit hysteresis: changes introduced after code phase commencement test rollback state machines.
- `interaction_hypothesis`: Rigid phase gates prevent downstream stages from negotiating ambiguities, resulting in infinite Reviewer-Coder deadlock loops.
- `maximum_stress_level`: `SEVERE` (Mid-stream requirement mutation + injected upstream architecture flaw).
- `early_stop_rule`: Terminate experiment immediately if deadlock frequency exceeds $15.0\%$ or task completion drops $> 20.0\%$ below unstructured chat.

---

## 3. Stress Progression & Termination Contract

### 3.1 Pre-Registered Stress Levels:
1. **`BASELINE`**: Deterministic specifications with explicit I/O examples and pre-written pytest assertions.
2. **`MILD`**: Ambiguous requirements with missing edge cases and implicit dependencies.
3. **`MODERATE`**: Exploratory tasks lacking closed ground-truth answers (e.g. game balancing, creative simulation design).
4. **`SEVERE`**: Dynamic requirement shifts introduced after Phase 2 (Coding) begins, combined with upstream defect injection in Phase 1 (Design).

### 3.2 Quantitative Threshold Contracts:
- `statistical_threshold`: Deadlock rate and completion differences significant at $\alpha = 0.01$ across $N \ge 50$ tasks per condition, demonstrating a material statistical effect.
- `practical_degradation_threshold`: Turn count per phase exceeds $10$ turns OR rollback token cost $> 50\%$ of base task tokens.
- `failure_threshold`: Review loop deadlock rate exceeds $15.0\%$ **OR** task completion rate drops $> 20.0\%$ below baseline. (Establishes negative boundary for SOP applicability).
- `mechanistic_failure_trigger`: SOP state machine deadlocks under a specific failure condition (e.g. infinite Coder-Reviewer ping-pong, cyclic rollback traps, or irreversible transition failure) even when sample size is insufficient for formal significance. Must be explicitly logged, identify the observed failure mechanism, justify the bounded follow-up, and not permit unrestricted exploratory expansion.
- `escalation_rule`: Escalate from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE of the following preregistered triggers is satisfied:
  1. **Practical Degradation Trigger**: `practical_degradation_threshold` or `failure_threshold` is crossed (deadlock rate $> 15.0\%$, completion loss $> 20.0\%$, or turns $> 10$); **OR**
  2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < 0.01$); **OR**
  3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears (e.g. cyclic phase deadlock) justifying bounded follow-up.
  *Practical-Significance Discipline*: Escalating solely on statistical significance ($p < \alpha$) when the observed effect is operationally trivial (deadlock rate delta $< 1.0\%$, turn count delta $< 0.5$ turns) is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.
- `early_stop_rule`: Terminate experiment immediately if deadlock frequency exceeds $15.0\%$ or task completion drops $> 20.0\%$ below unstructured chat.
- `abort_threshold`: Reviewer/Coder review loop exceeds $16$ turns in $>15\%$ of tasks ($AF-03$).
- `recovery_threshold`: Explicit backward phase rollback recovers passing code in $\ge 80.0\%$ of defects.

### 3.3 Termination Invariant
Testing must stop when:
1. The negative task boundary for rigid SOPs is established;
2. Safety or budget limits are reached; **OR**
3. Further stress cannot alter the architectural conclusion.

Do not run to maximum team size ($K=10$) under `SEVERE` ambiguity once failure is established at $K=3$ (`NC-54`).



---

# AS-09: Routing Feature Ablation Plan
**Experiment ID**: `EXP-AB-04-FEAT`  
**Target Primitive**: `PR-ORG-03` (Dynamic Agent Routing & Orchestration)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
Which specific features in the multi-feature heuristic routing function are necessary to maintain $\ge 25\%$ token savings while preserving $\le 3\%$ accuracy loss compared to static full topology?

---

## 2. Leave-One-Out Feature Ablation Design

Evaluated on `SimLab-HeteroBench-300` ($N=300$ tasks, 70/30 train/test split):

### Heuristic Feature Space:
- $f_1$: **Estimated Query Length & Token Count** (lexical volume).
- $f_2$: **Syntax Complexity Indicators** (presence of code blocks, formal logic, multi-step clauses).
- $f_3$: **Constraint Multiplicity** (number of explicit requirements or negative constraints).
- $f_4$: **Domain Keyword Specificity** (specialized technical vocabulary).
- $f_5$: **Task Type Taxonomy** (classification into Simple, Moderate, Complex).

### Evaluated Conditions:
- **H-Full**: Complete multi-feature heuristic router ($f_1 + f_2 + f_3 + f_4 + f_5$).
- **H-Minus-1**: Omit query length ($f_1$).
- **H-Minus-2**: Omit syntax complexity ($f_2$).
- **H-Minus-3**: Omit constraint multiplicity ($f_3$).
- **H-Minus-4**: Omit domain keywords ($f_4$).
- **H-Minus-5**: Omit task type classification ($f_5$).
- **H-Minimal**: Minimal 2-feature heuristic router ($f_2 + f_3$).

---

## 3. Primary Metrics & Success Thresholds
- **Test Set Accuracy**: Accuracy on 90 held-out test tasks.
- **Net System Token Savings**: Relative to Static Full Topology.
- **Under-Activation Rate**: Complex tasks incorrectly routed to a single agent.
- **Success Criterion**: Identify the minimal feature subset that maintains $\ge 25\%$ token savings with $\le 3.0\%$ accuracy degradation.
- **Critical Feature Boundary (Escalation Threshold)**: An ablated feature is classified as strictly indispensable if its removal trips the pre-registered routing escalation threshold codified in `AS-10`, `AS-15`, and `NC-69`: accuracy degradation $> 10.0\%$ relative to Static Topology **OR** under-activation rate $> 15.0\%$.

---


## 4. Causal Claim Discipline
- `causal_claim_supported`: "Removing syntactic complexity ($f_2$) or constraint multiplicity ($f_3$) from the heuristic router causes a statistically significant degradation in routing accuracy ($> 3.0\%, p < 0.01$) relative to the full heuristic router on held-out tasks."
- `causal_claim_not_supported`: "Heuristic routing with these features is universally superior to static routing or neural routing across all unseen domains."
- `tested_context`: Multi-agent code/math queries with varying length and constraint counts, 4 specialist agent types, deterministic verification.
- `untested_context`: Continuous high-frequency real-time dialogue, open-ended conversational roleplay, dynamically expanding agent pools $> 25$.
- `interaction_risks`: Combining short query length ($f_1$) with complex multi-clause logic ($f_2$) risks under-activating specialist agents if weights are not balanced.



---

# AS-10: Routing Stress Plan
**Experiment ID**: `EXP-ST-04-SHIFT`  
**Target Primitive**: `PR-ORG-03` (Dynamic Agent Routing & Orchestration)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question & Invariant Role of High-Tier Routers

### 1.1 Preservation of Phase 3 Stopping-Rule Invariants
In Phase 3, heuristic routing delivered $27.80\%$ token savings with only $-2.0\%$ accuracy degradation, triggering `STOP_ESCALATION_VALID`. In strict accordance with `NC-43`, `NC-50`, and `NC-59`:
- **`LLM_ROUTER` = `NOT_TESTED_DUE_TO_STOPPING_RULE`**
- **`LEARNED_PUPPETEER_ROUTING` = `NOT_TESTED_DUE_TO_STOPPING_RULE`**

Phase 4 preserves these statuses as non-inferior stopping-rule classifications. Under no circumstances will neural or Puppeteer routers be tested merely for completeness, curiosity, or exhaustive benchmarking. Phase 4 may authorize testing them **ONLY IF**:
1. `HEURISTIC_ROUTING` fails pre-registered stress criteria (accuracy degradation $> 10.0\%$ and under-activation $> 15.0\%$); **OR**
2. A specific, formally approved requester hypothesis explicitly mandates a direct head-to-head comparison.

---

## 2. Stress-Matrix Explosion Controls (`SCREEN -> ESCALATE -> INTERACTION_TEST`)

To prevent combinatorial explosion across multi-agent routing dimensions, stress testing follows a staged protocol:
- **Stage A (Screening)**: Test 1 factor at a time (Distribution Shift alone, then Adversarial Deception alone). Maximum 1–2 factors active.
- **Stage B (Escalation)**: Governed by dual-criterion decision rule combining practical degradation and statistical evidence. Escalation to higher stress severity occurs **IF AND ONLY IF**:
  1. A preregistered practical degradation threshold is crossed (`practical_degradation_threshold`); **OR**
  2. Statistical evidence demonstrates a material effect (`statistical_threshold`); **OR**
  3. A mechanistically important failure anomaly appears (e.g. chronic under-activation on critical constraints).
  *Anti-Pattern*: Do not require $p < \alpha$ as the sole trigger, and do not escalate on trivial statistical noise.
- **Stage C (Interaction Testing)**: Factorial interaction evaluated only between confirmed vulnerabilities.

### Experiment Metadata Contract:
- `number_of_active_factors`: 1 active factor during Stage A screening (Domain Shift); 2 active factors in Stage B escalation (Domain Shift + Prompt Length Deception).
- `reason_for_combination`: Mechanistic vulnerability testing — evaluates whether syntactic heuristics fail when concise length is paired with out-of-domain vocabulary.
- `interaction_hypothesis`: Short adversarial prompts will induce under-activation, but syntactic constraint multiplicity ($f_3$) will prevent catastrophic misrouting.
- `statistical_threshold`: Paired McNemar $p < 0.01$ demonstrating material degradation ($\Delta \ge 5.0\%$).
- `warning_threshold` (Practical Degradation): Routing accuracy drop $> 5.0\%$ below Static Topology (advisory engineering degradation warning; does not trip architectural escalation).
- `escalation_threshold`: Routing accuracy drop $> 10.0\%$ below Static Topology ($p < 0.01$) **OR** under-activation rate $> 15.0\%$. (Canonical preregistered routing escalation threshold per `NC-69` and `AS-09` to justify learned router escalation).
- `failure_threshold` (Severe Collapse): Under-activation rate $> 20.0\%$ (trips `AF-06` hard abort and router triage).
- `mechanistic_failure_trigger`: Router systematically fails a specific class of expert domains (e.g. complete starvation of logic specialists on concise adversarial prompts) even when sample size is insufficient for formal significance. Must be explicitly logged, identify the observed failure mechanism, justify bounded follow-up, and not permit unrestricted exploratory expansion.
- `escalation_rule`: Escalate from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE of the following preregistered triggers is satisfied:
  1. **Preregistered Escalation Trigger**: Canonical `escalation_threshold` is crossed (accuracy drop $> 10.0\%$ OR under-activation rate $> 15.0\%$); **OR**
  2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < 0.01$, $\Delta \ge 5.0\%$); **OR**
  3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears (e.g. systematic expert domain starvation) justifying bounded follow-up.
  *Practical-Significance Discipline*: Escalating solely on statistical significance ($p < \alpha$) when the observed degradation is below the canonical material effect threshold ($\Delta < 5.0\%$, i.e. observed effect delta $< 0.05$) is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.
- `early_stop_rule`: Terminate experiment immediately if heuristic routing satisfies the failure boundary or if 3 consecutive evaluation batches show zero routing accuracy changes.

### 2.1 Formal Amendment Record: PHASE4_ESCALATION_RULE_AMENDMENT
- `amendment_id`: `PHASE4_ESCALATION_RULE_AMENDMENT`
- `previous_rule`: `accuracy_drop > 10.0% (p < 0.01) AND under_activation_rate > 15.0%` (Historical commit `5d7b1ab`).
- `new_rule`: Multi-trigger disjunctive rule with practical-significance discipline (Trigger A: Practical Degradation OR Trigger B: Statistical Evidence of Material Effect $\Delta \ge 5.0\%$ OR Trigger C: Bounded Mechanistic Failure Trigger).
- `reason_for_change`: The historical AND-pair conjunctive rule is an anti-pattern for stress testing; requiring both statistical significance and extreme practical failure simultaneously blinds the screening harness to severe operational degradation (e.g. 18% under-activation without p-value convergence) and delays triage.
- `scientific_rationale`: Screening experiments must escalate upon discovering either a material practical sensitivity, a statistically sound degradation with non-trivial effect size, or an overt mechanistic failure. Practical failure does not require statistical significance to matter, and statistical significance does not make a trivial effect operationally important.
- `governance_rationale`: Eliminates ambiguity between screening rules and adjudication standards, ensuring execution harnesses evaluate explicit, non-conflicting operational criteria across all tiers.
- `affected_artifacts`: `AS-09`, `AS-10`, `AS-11`, `AS-14`, `AS-15`, `AS-16`, `AS-17`, `curo_phase4_ablation_package.md`.
- `reviewer`: Dr. Sol (Independent Senior Reviewer & Failure Analyst).
- `approval_state`: `APPROVED_FOR_EXECUTION_READINESS`.
- `effective_version`: Phase 4 Design Hardened v2.4.
- `effective_commit`: Canonical pre-execution checkpoint.
- `superseded_rule_status`: `SUPERSEDED_RULE` (Historical provenance preserved from commit `5d7b1ab`; non-operative).

### 2.2 Canonical Executable-Style Routing Escalation Logic
```python
def should_escalate_routing_stress(
    routing_accuracy_drop: float,
    routing_under_activation: float,
    statistical_p_value: float,
    observed_effect_delta: float,
    approved_mechanistic_failure_logged: bool
) -> bool:
    # Trigger A: Practical Degradation Trigger
    practical_degradation_trigger = (
        (routing_accuracy_drop > 0.10) or
        (routing_under_activation > 0.15)
    )
    
    # Trigger B: Statistical Trigger with Material Effect Size (>= 5.0%)
    # Enforces practical-significance discipline: sub-threshold effects (delta < 0.05) cannot trip Trigger B
    statistical_trigger = (
        (statistical_p_value < 0.01) and
        (observed_effect_delta >= 0.05)  # ROUTING_STATISTICAL_TRIGGER_EFFECT_THRESHOLD = 5.0%
    )
    
    # Trigger C: Bounded Mechanistic Failure Trigger
    mechanistic_failure_trigger = approved_mechanistic_failure_logged

    # Escalation Rule: Disjunctive Multi-Trigger
    return practical_degradation_trigger or statistical_trigger or mechanistic_failure_trigger
```


---

## 3. Stress Progression, Justification & Termination Contract

### 3.1 Pre-Registered Stress Levels
1. **`BASELINE`**: In-distribution code generation and GSM8K math problems formatted identically to training distributions.
2. **`MILD`**: Conversational paraphrasing and syntactic style mutations of standard in-distribution tasks.
3. **`MODERATE`**: Unseen task domains (legal contract analysis, medical diagnostic queries, multi-hop temporal logic).
4. **`SEVERE`**: Adversarial Deception Attacks:
   - *Concise Complexity*: High-difficulty reasoning problems compressed into $< 15$ words.
   - *Verbose Simplicity*: Elementary string manipulation buried within $> 500$ words of conversational padding.

### 3.2 Scientific & Operational Justification of Routing Escalation Thresholds
The escalation triggers (`accuracy loss > 10.0%` and `under-activation > 15.0%`) were established prior to Phase 4 execution based on explicit operational principles:
- **Accuracy Loss Threshold ($> 10.0\%$)**:
  - *Baseline Context*: In Phase 3, heuristic routing achieved $27.80\%$ token savings with only $-2.0\%$ accuracy degradation relative to static full broadcast.
  - *Operational Rationale*: Heuristic routing is justified strictly by token savings without material quality degradation. A $10.0\%$ accuracy degradation represents a $5\times$ expansion of baseline error loss, erasing more utility than the $27.8\%$ token savings provide.
  - *Statistical Rationale*: On a benchmark of $N=100$ held-out tasks, an accuracy drop $> 10.0\%$ achieves statistical significance at $\alpha = 0.01$ ($p < 0.01$).
- **Under-Activation Threshold ($> 15.0\%$)**:
  - *Operational Rationale*: Under-activation occurs when complex multi-step tasks requiring specialist multi-agent interaction are erroneously routed to a single baseline agent. In autonomous simulations, under-activating specialist roles causes silent downstream task corruption. An under-activation rate $> 15.0\%$ means more than 1 in 7 complex tasks are misrouted, exceeding acceptable fault tolerance for autonomous execution kernels (`NC-01`, `NC-34`).

### 3.3 Quantitative Threshold Contracts
- `statistical_threshold`: Paired McNemar $p < 0.01$ with meaningful effect size ($\Delta \ge 5.0\%$).
- `warning_threshold`: Routing accuracy drop $> 5.0\%$ below Static Topology (advisory degradation warning).
- `escalation_threshold`: Routing accuracy drop $> 10.0\%$ below Static Topology ($p < 0.01$) **OR** under-activation rate exceeds **$15.0\%$**. (Canonical preregistered architectural escalation threshold per `NC-50`, `NC-69`, and `AS-09`).
- `failure_threshold`: Heuristic under-activation rate exceeds **$20.0\%$** (`AF-06`, severe routing collapse tripping hard abort).
- `mechanistic_failure_trigger`: Router systematically starves a specialist domain class (e.g. 0% activation on concise logic prompts) even when sample size is insufficient for formal significance. Must be explicitly logged, bounded follow-up only, no unrestricted expansion.
- `escalation_rule`: Authorize progression from Mild to Moderate/Severe when canonical `escalation_threshold` is crossed (accuracy drop $> 10.0\%$ or under-activation $> 15.0\%$), or `statistical_threshold` is satisfied (paired McNemar $p < 0.01$ and $\Delta \ge 5.0\%$), or `mechanistic_failure_trigger` appears. Escalation on sub-threshold effect size ($\Delta < 5.0\%$, i.e. observed effect delta $< 0.05$) is strictly prohibited under Trigger B.
- `abort_threshold`: Router parsing or syntactic extraction errors exceed $5.0\%$ of queries.
- `recovery_threshold`: Fallback to static topology broadcast restores accuracy to within $1.0\%$ of full static baseline.

### 3.4 Termination Invariant
Testing must stop when:
1. The failure boundary is established;
2. Safety or financial budget limits are reached ($AF-01$, $AF-06$); **OR**
3. Further stress cannot change the architectural conclusion.

Do not run to maximum stress merely because the level exists (`NC-54`).




---

# AS-11: System-Level Stress Matrix & Explosion Control Protocol
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Enforceable Stress-Matrix Explosion Control Rule

Combinatorial expansion across multi-agent simulation parameters generates exponential token costs without commensurate scientific clarity. The principle of avoiding combinatorial explosion is hereby converted into an **enforceable governance rule**:

$$\text{SCREEN} \longrightarrow \text{ESCALATE} \longrightarrow \text{INTERACTION\_TEST}$$

### 1.1 Staged Execution Protocol:
1. **Stage A — Screening**:
   - Test **no more than 1–2 stress factors simultaneously**.
   - Purpose: Rapidly filter benign operational parameters from active vulnerability vectors.
2. **Stage B — Escalation**:
   - Escalation is governed by a preregistered dual-criterion decision rule combining **practical degradation** and **statistical evidence**.
   - Escalation to higher stress severity is justified **IF AND ONLY IF** at least one of the following triggers is satisfied:
     - **Trigger A (Practical Degradation)**: A preregistered practical degradation threshold or failure threshold is crossed ([EXAMPLE_ONLY]: illustrative across primitives, e.g. latency $>20$ms, token blowout $>3\times$, completion drop $\ge 10.0\%$; canonical values defined in `AS-04`, `AS-06`, `AS-08`, `AS-10`); **OR**
     - **Trigger B (Statistical Evidence of Material Effect)**: Statistical testing demonstrates a material effect ($p < \alpha$ **AND** the effect size is practically meaningful, $\Delta \ge \Delta_{\text{practical}}$); **OR**
     - **Trigger C (Mechanistic Failure Signal)**: A mechanistically important failure anomaly appears ([EXAMPLE_ONLY]: illustrative, e.g. deadlock loop, silent state divergence, or memory overwrite) that requires bounded follow-up investigation.
   - **Anti-Patterns Strictly Prohibited**:
     - *Prohibition 1*: Requiring $p < \alpha$ as the sole trigger for continued stress testing is forbidden.
     - *Prohibition 2*: Escalating based solely on a tiny, practically trivial difference that achieves statistical significance merely due to sample size is forbidden.
   - Benign dimensions showing neither practical degradation nor statistical significance remain frozen at Baseline.
3. **Stage C — Interaction Testing**:
   - Use factorial interaction tests **only when Stage A screening evidence suggests interaction or when there is a strong mechanistic reason** ([EXAMPLE_ONLY]: e.g. state consensus under network partition).

### 1.2 Cartesian Product Prohibition Invariant
Creating an unconstrained Cartesian product across the eight multi-agent stress dimensions:
1. Agent Count ($N \in \{1, 3, 5, 10, 25\}$)
2. Memory Size ($M \in \{100, 1k, 5k, 10k\}$)
3. Noise ($\eta \in \{0\%, 10\%, 30\%, 50\%\}$)
4. Latency ($\tau \in \{0, 1, 2\text{ ticks}\}$)
5. Tool Failure ($\epsilon_{\text{tool}} \in \{0\%, 5\%, 15\%\}$)
6. Context Pressure ($\rho \in \{50\%, 80\%, 100\%\}$)
7. Distribution Shift (In-domain, Mild, Severe)
8. Communication Load (Low, Medium, High)

is **STRICTLY PROHIBITED** without explicit, written requester authorization. ($5 \times 4 \times 4 \times 3 \times 3 \times 3 \times 3 \times 3 = 58,320$ cells $\implies > \$15,000$ spend; rejected under `NC-38` and `NC-54`).

### 1.3 Mandatory Governance Fields for Stress Experiments
Every Phase 4 stress experiment must explicitly distinguish and declare:
- `number_of_active_factors`: Integer count of simultaneously varied dimensions ($\le 2$ in Stage A).
- `reason_for_combination`: Explicit mechanistic rationale explaining why these factors must interact.
- `interaction_hypothesis`: Formal statement predicting the non-linear coupling effect between factors.
- `maximum_stress_level`: Highest stress intensity authorized for execution (`BASELINE`, `MILD`, `MODERATE`, `SEVERE`).
- `statistical_threshold`: Formal significance level and test specification demonstrating a material statistical effect ([EXAMPLE_ONLY]: illustrative template, e.g. $\alpha = 0.01, \Delta \ge 5.0\%$; see per-primitive plans).
- `practical_degradation_threshold`: Quantitative operational performance drop that warrants engineering concern or escalation ([EXAMPLE_ONLY]: illustrative template, e.g. $> 10.0\%$ drop, $> 20$ms latency, $> 3\times$ token overhead; see per-primitive plans).
- `failure_threshold`: Operating boundary where simulation stability or task accuracy collapses ([EXAMPLE_ONLY]: illustrative template, e.g. $\ge 30.0\%$ drop, $>15.0\%$ deadlock rate; see per-primitive plans).
- `mechanistic_failure_trigger`: Explicitly logged scientifically important failure mode ([EXAMPLE_ONLY]: illustrative, e.g. unrecoverable state divergence, domain starvation, deterministic stale retrieval, cyclic deadlock) requiring bounded follow-up even when sample size is insufficient for formal significance.
- `escalation_rule`: Authorizes progression from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE trigger is satisfied: (A) Practical Degradation, (B) Statistical Evidence, OR (C) Mechanistic Failure Trigger. Escalation solely on $p < \alpha$ when the effect is operationally trivial is strictly prohibited.
- `early_stop_rule`: Deterministic condition that immediately halts runs before reaching maximum stress.

---


## 2. Bounded System-Level Stress Matrix Table

```
+-------------------------------------------------------------------------------------------------------------------------------+
| Stress Vector             | Active Factors (<=2) | Interacting Primitives | Failure Mode | Interaction Hypothesis             |
+-------------------------------------------------------------------------------------------------------------------------------+
| 1. Population Growth      | 1 Factor:            | Memory + Routing + SOP | FM-04 / FM-11| IPC token overhead scales          |
|    (1 to 25 Agents)       | Agent Count          |                        | (Token Blow) | polynomial, not exponential.       |
| 2. Long-Horizon Drift     | 1 Factor:            | Memory (PR-COG-01) +   | FM-02        | Retrieval precision collapses      |
|    (Continuous Ticks)     | Temporal Horizon     | Social Dialogue        | (Drift)      | after 1,000 ticks without pruning. |
| 3. Network Partition      | 2 Factors:           | Debate (PR-ORG-01) +   | FM-06        | Partial observation + dropout      |
|    (Delay + Dropouts)     | Packet Loss + Latency| Distributed State      | (Consensus)  | breaks convergence non-linearly.   |
| 4. Injected Contamination | 2 Factors:           | Memory + Debate        | False Belief | Corrupt seed facts multiply via    |
|    (Adversarial Seeds)    | Corrupt Seeds + Vol  |                        | Cascade      | reflection nodes if unvalidated.   |
| 5. Context Saturation     | 2 Factors:           | SOP (PR-ORG-02) +      | FM-01        | Artifact size + multi-turn depth   |
|    (Artifact Flood)       | Load % + Artifact KB | Tool Execution         | (Truncation) | causes silent truncation in Phase 2|
+-------------------------------------------------------------------------------------------------------------------------------+
```

---

## 3. System Stress Termination Contract

For every system stress vector, the execution harness must pre-register discrete stress tiers and quantitative thresholds:

### 3.1 Four Pre-Registered Stress Levels
1. **`BASELINE`**: Nominal operating envelope ($N \le 3$, $M \le 100$, 0% noise, 0% dropouts).
2. **`MILD`**: Minor operational friction ($N=5$, $M=500$, 10% noise, 1-tick delay).
3. **`MODERATE`**: Real-world challenging conditions ($N=10$, $M=1,000$, 25% noise, 10% dropouts).
4. **`SEVERE`**: Near-boundary stress ($N=25$, $M=5,000$, 50% noise, 25% dropouts).

### 3.2 Four Governing Threshold Contracts
- `failure_threshold`: The point where simulation stability or task accuracy collapses ([EXAMPLE_ONLY]: illustrative, $\ge 30\%$ drop in primary metric or fatal exception rate $> 10\%$; see specific contracts in `AS-04`, `AS-06`, `AS-08`, `AS-10`). Establishing this boundary is the primary goal of stress testing.
- `degradation_threshold`: The point where performance degrades significantly ([EXAMPLE_ONLY]: illustrative, $> 10\%$ drop; see specific contracts in `AS-04`, `AS-06`, `AS-08`, `AS-10`) but remains recoverable.
- `abort_threshold`: Safety, budget, or infrastructure invariant violation ($AF-01$ cumulative spend $>\$50$, host RAM $>1\text{ GB}$, CPU timeout $>60\text{s}$).
- `recovery_threshold`: The system's ability to self-heal or return to baseline accuracy once stress factor is removed.

### 3.3 Termination Invariants
Testing **MUST STOP** immediately when:
1. A definitive failure boundary is established;
2. Safety or budget limits are reached; **OR**
3. Further stress cannot alter the architectural conclusion.

Running to `SEVERE` merely because the level exists is strictly prohibited (`NC-54`).



---

# AS-12: Statistical / Power Contract
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Mandatory 8-Field Power Analysis Specification (Confirmatory Replication)

For any confirmatory Phase 4 experiment—specifically the high-powered RP-02 replication (`EXP-AB-02-REP`)—an independent mathematical audit (`POWER_CALCULATION_CORRECTED`) establishes the following binding statistical parameters:

| # | Statistical Dimension | Value in `EXP-AB-02-REP` | Formal Methodological Justification |
|:---|:---|:---|:---|
| 1 | **Expected Effect Size** | $\Delta_{\text{expected}} = \mathbf{+0.100}$ ($+10.0\%$) | Conservative lower-bound estimate; applies a **$28.5\%$ shrinkage discount** to Phase 3 observed point estimate ($+14.0\%$) to hedge against winner's curse. |
| 2 | **Discordant Pairs Breakdown** | $p_{\text{disc}} = \mathbf{0.400}$, $b = \mathbf{0.250}$, $c = \mathbf{0.150}$ | Derived from Phase 3 empirical counts ($b=27, c=13$ out of 100); $b = (0.40 + 0.10)/2 = 0.25$, $c = (0.40 - 0.10)/2 = 0.15$. |
| 3 | **Power Target ($1 - \beta$)** | $\mathbf{0.900}$ ($90.0\%$ Statistical Power) | Minimizes Type II error risk on primary architectural gatekeeper. |
| 4 | **Significance Level ($\alpha$)** | $\alpha = \mathbf{0.010}$ (Two-Sided, $z = 2.576$) | Strictly preserved; zero alpha relaxation permitted (`NC-47`). |
| 5 | **Power Method Classification** | `ASYMPTOTIC_MCNEMAR_POWER_APPROXIMATION` (Connor 1987 / Lachin 1992) | $N_{\text{base}} = \frac{\left(z_{\alpha/2}\sqrt{p_{\text{disc}}} + z_{\beta}\sqrt{p_{\text{disc}} - \Delta^2}\right)^2}{\Delta^2} = \frac{(2.576\sqrt{0.40} + 1.282\sqrt{0.39})^2}{0.01} = \mathbf{591 \text{ pairs}}$. |
| 6 | **Dropout / Invalid Allowance** | $+10.0\%$ Over-Recruitment Buffer | Buffer covers parsing timeouts or API drops: $N = \lceil 591 \times 1.10 \rceil = \mathbf{650 \text{ problem instances}}$ ($1,300$ paired episodes). |
| 7 | **Multiple-Comparison Policy** | Single Pre-Registered Primary Outcome | $\alpha = 0.01$ dedicated entirely to primary accuracy outcome; exploratory metrics evaluated under Benjamini-Hochberg FDR $q=0.05$. |
| 8 | **Minimum Detectable Effect (MDE)** | $\text{MDE} = \mathbf{+9.6\%}$ ($0.096$) | The smallest true accuracy surplus detectable with $90\%$ probability at $\alpha = 0.01$ under $N=650$. |

**Independent Power Method Verification (`POWER_CALCULATION_VERIFIED`)**:
- **Method Classification**: The sample-size formulation is an asymptotic normal approximation, classified canonically as `ASYMPTOTIC_MCNEMAR_POWER_APPROXIMATION`. It must not be labeled "exact."
- **Exact Binomial Verification (`EXACT_BINOMIAL_MCNEMAR_POWER`)**: Minimum base $N$ for exact two-sided conditional power $\ge 0.900$ is $N_{\text{base}} = 605$ (Power = $90.05\%$). At $N = 650$ instances (including buffer), exact conditional power achieved is **$92.35\%$**.
- **Simulation Verification (`SIMULATION_BASED_PAIRED_POWER`)**: Monte Carlo simulation of $100,000$ paired binary multinomial draws confirms empirical power of **$92.36\%$** at $\alpha = 0.01$.
- **Audit Conclusion**: $N = 650$ ($1,300$ paired episodes) is rigorously verified to deliver $>92\%$ power against the conservative $\Delta = +10.0\%$ target, eliminating under-powering risk. Recorded status: **`POWER_CALCULATION_VERIFIED`**.


---

## 2. Power Specifications for Component Ablations

1. **Memory Component Ablation (`EXP-AB-01-COMP`)**:
   - Primary metric: Continuous Mean Reciprocal Rank (MRR) and NDCG@5 across 8 conditions.
   - Target Effect Size: Cohen's $d = 0.35$ (small-to-medium effect).
   - Alpha & Correction: Family-wise error rate controlled via Bonferroni correction: $\alpha_{\text{adjusted}} = 0.01 / 7 = 0.0014$.
   - Sample Size: $N = 100$ standardized queries from `SimLab-MemBench-500` achieves $86.4\%$ power.
   
2. **SOP Factorial Analysis (`EXP-AB-03-FACT`)**:
   - Design: $2 \times 2$ Factorial ANOVA (Roles $\times$ Phases) on token consumption.
   - Minimum Detectable Effect: Partial eta-squared $\eta_p^2 = 0.08$.
   - Alpha & Power: $\alpha = 0.01$, $1 - \beta = 0.90$.
   - Sample Size: $N = 100$ tasks per cell ($400$ total task runs) achieves $92.1\%$ power.

3. **Routing Feature Ablation (`EXP-AB-04-FEAT`)**:
   - Design: Leave-one-out feature evaluation across 7 variants on 90 held-out test tasks.
   - Non-Inferiority Margin: $\Delta_{\text{margin}} \le 3.0\%$ accuracy loss relative to Static Topology.
   - Statistical Test: Paired one-sided non-inferiority t-test at $\alpha = 0.01$, power $85\%$.

---

## 3. Winner's Curse & Effect-Size Inflation Mitigation Rule
- **Prohibition on Raw Phase 3 Extrapolation**: Evaluators are strictly prohibited from setting confirmatory sample sizes based purely on the observed Phase 3 point estimate when that estimate was exploratory or marginally significant.
- **Mandatory Inflation Discount**: All confirmatory sample size models must apply a minimum $25\%$ effect shrinkage discount or use the lower bound of the empirical $90\%$ confidence interval from prior phases.

---

## 4. Confirmatory Replication Immutability Governance
- In accordance with `AS-05`, the 12 material dimensions of `EXP-AB-02-REP` are declared **frozen and immutable**.
- Sample size ($N$) may vary only as prescribed by the power calculations above.
- If any material dimension is altered, the run must be designated **`AMENDED_REPLICATION`** and triggers **`EXPERIMENT_AMENDMENT_REQUIRED`**.



---

# AS-13: Cost, Token & Compute Budget
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Projected Resource Budget for Phase 4 Execution

Phase 4 utilizes the **Minimum Ablation Principle** to isolate causal factors with minimal token spend:

| Experiment Code | Target Primitive | Experimental Conditions | Estimated Runs ($N$) | Avg Tokens / Run | Total Tokens | Estimated API Spend |
|:---|:---|:---|:---|:---|:---|:---|
| **EXP-AB-01-COMP** | `PR-COG-01` (Memory Comp) | 8 scoring variants | 800 evaluations | 0 (Offline vectors) | 0 | **$0.00** |
| **EXP-ST-01-SCALE** | `PR-COG-01` (Memory Stress) | 5 scale levels $\times$ 4 noise types| 2,000 evaluations | 0 (Offline vectors) | 0 | **$0.00** |
| **EXP-AB-02-REP** | `PR-ORG-01` (Private Info Rep)| 2 conditions ($B3$ vs $B1-SC$) | 1,300 episodes ($N=650$) | 8,400 tokens | 10.92M tokens | **$6.60** |
| **EXP-AB-02-ASYM** | `PR-ORG-01` (Asymmetry Sweep)| 5 asymmetry levels | 750 episodes | 8,400 tokens | 6.30M tokens | **$3.80** |
| **EXP-ST-02-STATE** | `PR-ORG-01` (State Stress) | 5 population levels | 500 episodes | 6,200 tokens | 3.10M tokens | **$1.85** |
| **EXP-AB-03-FACT** | `PR-ORG-02` (SOP Factorial) | 4 factorial cells | 400 task runs | 12,000 tokens | 4.80M tokens | **$2.90** |
| **EXP-ST-03-SOP** | `PR-ORG-02` (SOP Stress) | 5 task ambiguity levels | 250 task runs | 14,000 tokens | 3.50M tokens | **$2.10** |
| **EXP-AB-04-FEAT** | `PR-ORG-03` (Routing Feature)| 7 heuristic variants | 630 task runs | 2,400 tokens | 1.51M tokens | **$0.90** |
| **EXP-ST-04-SHIFT** | `PR-ORG-03` (Routing Stress) | 4 shift levels | 400 task runs | 2,600 tokens | 1.04M tokens | **$0.65** |
| **Contingency** | Re-run reserve / buffer | Pre-registered buffer | - | - | 2.50M tokens | **$1.55** |
| **TOTALS** | - | - | **7,030 runs** | - | **33.67M tokens** | **$20.35 USD** |

---

## 2. Canonical Budget Hierarchy & Semantics Reconciliation

To prevent confusion between operational abort triggers, experiment limits, advisory warnings, and global ceilings, the budgetary governance hierarchy is codified into four discrete, mutually exclusive levels:

| Level | Scope | Threshold Name | Value | Semantic Role | Source | Trigger Action | Override Allowed? | Authority Required for Change |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LEVEL 1** | Phase 4 Program | `PHASE4_BUDGET_WARNING_THRESHOLD` | **$35.00 USD** | `WARNING_THRESHOLD` | `AS-13` §2 | Advisory financial engineering notice: flags $>70\%$ drift above projected baseline; non-blocking. | **NO** | Senior Reviewer (Sol) |
| **LEVEL 2** | Per-Experiment | `EXP_BUDGET_LIMIT` (per plan) | **Per Matrix** (e.g. `EXP-AB-02-REP`: $6.60, `EXP-AB-02-ASYM`: $3.80) | `EXPERIMENT_BUDGET_LIMIT` | `AS-13` §1 | Pre-call projection check (`NC-38`); halts individual experiment if projected spend exceeds allocated budget. | **NO** | Requester Formal Amendment |
| **LEVEL 3** | Phase 4 Execution | `PHASE4_BUDGET_ABORT_THRESHOLD` | **$50.00 USD** | `ABORT_THRESHOLD` | `AS-14` (`AF-01`), `AS-11` §3.2 | Automated hard circuit breaker: immediately HALTS all Phase 4 execution runs and triggers emergency triage. | **NO** | Human Requester Only |
| **LEVEL 4** | Global Project | `GLOBAL_API_HARD_CEILING` | **$100.00 USD** | `GLOBAL_HARD_CEILING` | `AS-13` §2, `NC-38` | Hard environmental stop across all project phases; immediate API key revocation and container kill. | **STRICTLY NO** | Human Requester Formal Action |

### Budget Reconciliation Invariants:
1. **Scope Distinction**: `PHASE4_BUDGET_ABORT_THRESHOLD` ($50.00 USD) and `GLOBAL_API_HARD_CEILING` ($100.00 USD) govern fundamentally different operational scopes. Phase 4 execution stops at $50.00 USD even though the broader project ceiling remains $100.00 USD.
2. **Stricter Limit Controls**: The stricter Phase 4 limit ($50.00 USD) strictly controls Phase 4 execution runs. The remaining $50.00 buffer under the global ceiling must NOT be interpreted as permission to continue Phase 4 live execution.
3. **No Semantic Aliasing**: No two budget controls share the same semantic label or operational scope.
4. **Zero Paid Token Harnesses**: Memory ablations and stress testing run entirely offline on pre-computed vectors ($0.00 API cost).
5. **Pre-Call Financial Projection**: Every live call must compute projected cost and enforce stopping limits before dispatch (`NC-38`, `AF-01`).





---

# AS-14: Failure & Abort Register & Stress Termination Contract
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Pre-Registered Failure Modes & Abort Conditions

| Failure Code | Failure Description | Threshold Category | Trigger Condition | Automated Action |
|:---|:---|:---|:---|:---|
| **AF-01** | Hard Budget Overrun Threat | `abort_threshold` | Cumulative API spend exceeds **$50.00 USD** | HALT execution immediately; trigger emergency review. |
| **AF-02** | Model Fingerprint Drift | `abort_threshold` | Provider returns altered `system_fingerprint` | Invalidate current batch; freeze runs until pinned. |
| **AF-03** | SOP Deadlock Epidemic | `failure_threshold` | Reviewer/Coder review loop exceeds 16 turns in $>15\%$ tasks | Terminate condition; record failure boundary. |
| **AF-04** | Sycophancy / Consensus Cascade| `failure_threshold` | False consensus rate in debate exceeds **$25.0\%$** | Flag condition as failed; abort population expansion. |
| **AF-05** | Memory Retrieval Overflow | `abort_threshold` | Retrieval latency $> 100$ms or RSS RAM $> 1.0$ GB | Abort memory scale expansion; document scale cliff. |
| **AF-06** | Severe Routing Collapse | `failure_threshold` | Heuristic under-activation exceeds **$20.0\%$** | Trip Complexity Escalation Rule for router review. |
| **AF-07** | Non-Deterministic Replay | `abort_threshold` | Re-running identical PRNG seed produces divergent output | Invalidate run harness; fix RNG seeding sequence. |
| **AF-08** | Task Degradation Floor | `degradation_threshold`| Primary accuracy metric drops $> 10.0\%$ below control | Log degradation warning; evaluate recovery threshold. |
| **AF-09** | Consensus Recovery Failure | `recovery_threshold` | Re-introducing full state fails to restore consensus $>90\%$ | Declare unrecoverable distributed state breakdown. |

---

## 2. Universal Stress Experiment Termination Contract

For every stress experiment across memory, multi-agent debate, SOP pipelines, and routing, the execution harness must strictly adhere to the following termination contract:

### 2.1 Four Operational Tiers:
- **`BASELINE`**: Nominal load; validates baseline operation.
- **`MILD`**: Low-level stress; checks for unexpected sensitivity.
- **`MODERATE`**: Realistic stress; identifies performance degradation.
- **`SEVERE`**: Near-cliff stress; locates the definitive failure boundary.

### 2.2 Binding Stop Rules & Multi-Trigger Escalation Protocol:
The execution harness **MUST TERMINATE** testing immediately upon encountering any of the following three conditions:
1. **Failure Boundary Established**: When the experimental metric crosses the pre-registered `failure_threshold` and establishes the operational envelope of the primitive.
2. **Safety or Budget Ceiling Reached**: When `abort_threshold` triggers ($AF-01$ budget, $AF-02$ drift, $AF-05$ memory/latency).
3. **Epistemic Invariance**: When further stress execution cannot alter the architectural conclusion (e.g. if a primitive fails at `MODERATE`, testing `SEVERE` is prohibited).

### 2.3 Multi-Trigger Escalation & Practical-Significance Discipline
Escalation across tiers (`SCREEN` $\to$ `ESCALATE` $\to$ `INTERACTION_TEST`) is authorized when **ANY ONE** of the three preregistered triggers is satisfied:
1. **Practical Degradation Trigger**: `practical_degradation_threshold` or `failure_threshold` is crossed.
2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < \alpha$ with meaningful effect size).
3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears that requires bounded follow-up even when sample size is insufficient for formal significance.

**Mechanistic Failure Trigger Governance Rules**:
- Must be explicitly logged with timestamp, run ID, and environmental parameters.
- Must identify the observed causal failure mechanism (e.g. agent dropout state divergence, deterministic stale retrieval, cyclic SOP deadlock, specialist starvation).
- Must justify the bounded follow-up experiment.
- Strictly does not permit unrestricted exploratory expansion or arbitrary compute burning.

**Practical-Significance Discipline**:
Escalating solely because $p < \alpha$ when the observed effect is operationally trivial is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.

**Anti-Waste Invariant**: Never execute tests up to maximum stress merely because the tier exists in the matrix (`NC-54`). Compute must be conserved for discriminative evaluations.

---

## 3. Secure Execution Architecture & Network Isolation Model

To reconcile the requirement for `--network none` container isolation (`NC-16`) with live provider API evaluation (`NC-39`), the execution runtime enforces a two-tier brokered architecture:

```
+-----------------------------------------------------------------------------------------------+
|                                ISOLATED EXPERIMENT CONTAINER                                  |
|  - Network Namespace: --network none (Zero Direct Internet Access)                             |
|  - Host Isolation: No provider credentials, no environment secrets, ephemeral tmpfs mounts   |
|  - Capabilities: Reads immutable inputs; writes only approved telemetry & result paths       |
+-----------------------------------------------------------------------------------------------+
                                               |
                                               | Structured Local Request (Unix Domain Socket / Local IPC)
                                               v
+-----------------------------------------------------------------------------------------------+
|                                 CONTROLLED INFERENCE BROKER                                   |
|  - Location: Separate trusted host process / gateway daemon                                   |
|  - Security: Holds provider API credentials; enforces strict credential boundary              |
|  - Pre-Call Checks: Enforces per-experiment budget and Phase 4 $50.00 abort ceiling (AF-01)   |
|  - Validation: Pinned model snapshot check; logs provider system_fingerprint (AF-02)          |
|  - Rate & Token Limits: Enforces max token caps and concurrency governors                     |
+-----------------------------------------------------------------------------------------------+
                                               |
                                               | Outbound Egress: HTTPS (Port 443) Only
                                               v
+-----------------------------------------------------------------------------------------------+
|                                  ALLOWLISTED MODEL API                                        |
|  - Authorized Providers: Provider-pinned endpoints only                                       |
|  - Egress Audit Log: Every request/response hash, token count, and latency logged             |
+-----------------------------------------------------------------------------------------------+
```

### 3.1 Egress Policy Specification
- `allowed_provider_domains`: Explicit allowlist (e.g. `generativelanguage.googleapis.com`, `api.openai.com`, or configured local mock endpoint).
- `allowed_ports`: 443 (HTTPS) only from Inference Broker.
- `credential_owner`: Controlled Inference Broker exclusively. Worker containers possess zero credentials.
- `request_broker`: Local IPC / authenticated Unix domain socket crossing the isolation boundary.
- `network_namespace`: Experiment workers run with `--network none`. Direct egress from workers is blocked at kernel level.
- `firewall_policy`: Strict deny-all for worker namespace; outbound allowlist strictly restricted to provider endpoints for Inference Broker.
- `egress_audit_log`: Append-only cryptographic ledger recording timestamp, `run_id`, `request_hash`, `prompt_hash`, `system_fingerprint`, and token usage.

### 3.2 Model Drift Circuit Breaker Protocol (`AF-02`)
For every paid or live inference call, the broker captures:
`provider`, `model_id`, `model_version/snapshot`, `system_fingerprint`, `request_hash`, `prompt_hash`, `run_id`, `response_id`, `token_usage`.
If the provider returns an altered `system_fingerprint` during a controlled experiment, the broker raises `STOP_VERSION_DRIFT`, halts run dispatch, and invalidates the batch.

### 3.3 Pre-Call Budget Projection Protocol (`AF-01`)
Before dispatching any outbound model call:
1. Compute projected token spend: $\text{Cost}_{\text{proj}} = \text{Current}_{\text{spend}} + \text{EstCall}_{\text{cost}}$.
2. Check against `EXP_BUDGET_LIMIT` (Level 2) and `PHASE4_BUDGET_ABORT_THRESHOLD` ($50.00 USD, Level 3).
3. If projected spend exceeds either threshold, the call is blocked immediately without dispatch.




---

# AS-15: Independent Design Review
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate Under Review**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Reviewer**: Sol (Independent Senior Reviewer & Failure Analyst)  
**Evaluation Date**: 2026-09-16  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Substantive Layer B Evaluation of Phase 4 Experimental Designs

I have conducted an independent adversarial audit (Layer B: Substantive Design Review) of the hardened Phase 4 ablation and stress test specifications (`AS-01` through `AS-18`).

### Substantive Review Across Required Dimensions:

1. **Replication Purity (12-Field Immutability Contract)**:
   - Evaluated `AS-05` and `AS-16` (`NC-62`). The 12-field immutability contract (`hypothesis`, `null_hypothesis`, `effect_definition`, `primary_outcome`, `task_generation_process`, `model_version`, `prompt_structure`, `compute_matching_rule`, `primary_statistical_test`, `alpha`, `multiple_comparison_policy`, `stopping_rule`) prevents methodological drift. Any parameter divergence is pre-registered to force an immediate `AMENDED_REPLICATION` classification and halt execution until amended.

2. **Power Method Classification & Independent N Verification (`POWER_CALCULATION_VERIFIED`)**:
   - Evaluated `AS-05`, `AS-12`, and `AS-13`. The power derivation is accurately reclassified as an `ASYMPTOTIC_MCNEMAR_POWER_APPROXIMATION` (Connor 1987 / Lachin 1992 normal approximation) and must not be termed "exact."
   - Independent verification confirms that $N=650$ ($1,300$ paired episodes, including $+10\%$ buffer) achieves $>92\%$ power against conservative $\Delta=+0.10$ under $40\%$ discordance:
     - `EXACT_BINOMIAL_MCNEMAR_POWER`: Exact conditional binomial power is **$92.35\%$** (minimum base $N$ for $90\%$ power is $N=605$).
     - `SIMULATION_BASED_PAIRED_POWER`: Monte Carlo simulation ($100,000$ trials) yields **$92.36\%$** empirical power at $\alpha=0.01$.
   - Sizing to $N=650$ is formally confirmed: **`POWER_CALCULATION_VERIFIED`**.

3. **Memory Ablation Isolation (`PR-COG-01`)**:
   - Evaluated `AS-03` and `AS-04`. Retrieval ablation uses offline, deterministic vector embeddings with zero paid token spend ($0.00 API cost). Counterfactual scoring comparisons isolate recency, relevance, and importance without confounding from generation variance.

4. **Multi-Trigger Stress Escalation & Practical-Significance Discipline (`SCREEN -> ESCALATE -> INTERACTION_TEST`)**:
   - Evaluated `AS-04`, `AS-06`, `AS-08`, `AS-10`, and `AS-11`. The escalation rule is correctly upgraded from a restrictive AND-pair to a preregistered multi-trigger OR-rule. Escalation is authorized when ANY ONE trigger is met: (A) Practical Degradation Trigger; (B) Statistical Trigger; OR (C) Mechanistic Failure Trigger.
   - **Protection Against Trivial-But-Significant Escalation**: The protocol strictly forbids escalating solely because $p < \alpha$ when the observed difference is operationally trivial. Statistical and practical evidence serve as complementary signals, not a mandatory conjunction.
   - **Bounded Mechanistic Failure Trigger**: A scientifically important failure mode (e.g. unrecoverable state divergence, domain starvation, deterministic stale retrieval, cyclic SOP deadlock) justifies bounded follow-up even when sample size is insufficient for formal significance. Mechanistic triggers must be explicitly logged, identify the specific causal failure mechanism, justify the bounded follow-up, and strictly prohibit unrestricted exploratory expansion.

5. **SOP Factorial Isolation (`PR-ORG-02`)**:
   - Evaluated `AS-07` and `AS-08`. The $2 \times 2$ factorial matrix separates rigid phase gating from structured communication. Pre-registered deadlock detection ($AF-03$) prevents unbounded reviewer-coder loops.

6. **Routing Threshold Verification & Escalation Rule Evolution (`PR-ORG-03`)**:
   - Evaluated `AS-09`, `AS-10`, `AS-11`, `AS-14`, and `AS-16`. The canonical preregistered routing escalation thresholds are confirmed as $> 10.0\%$ accuracy loss and $> 15.0\%$ under-activation (reaffirming commit `5d7b1ab` and `NC-69`), while severe collapse abort remains $> 20.0\%$ (`AF-06`).
   - The intermediate un-amended $8.0\%$ under-activation draft value has been purged from escalation criteria and classified as `THRESHOLD_DRIFT_CORRECTED`.
   - **Escalation Rule Reconciliation (`PHASE4_ESCALATION_RULE_AMENDMENT`)**: I have reviewed the transition from the historical conjunctive rule (`accuracy drop > 10% AND under-activation > 15%`, commit `5d7b1ab`) to the multi-trigger disjunctive rule (Trigger A: Practical Degradation OR Trigger B: Statistical Evidence OR Trigger C: Bounded Mechanistic Failure). This is a legitimate, sound methodological hardening that prevents screening blindness; it is not post-hoc data manipulation. The historical rule is properly classified as `SUPERSEDED_RULE`.
   - **Practical Significance Discipline Consistency**: The statistical trigger executable rule requires `observed_effect_delta >= 0.05` ($5.0\%$), and explanatory text referencing $\Delta < 1.0\%$ has been corrected to align with the canonical $5.0\%$ material degradation floor (`DOCUMENTATION_DRIFT_CORRECTED`). Outcome: **`ROUTING_RULE_CONSISTENCY_PASS`**.

7. **Primitive Advancement Contract Governance (`AS-18`)**:
   - Evaluated `AS-18`. The dual-track Criterion A resolution (A1 for Phase 3 supported primitives, A2 for confirmatory replication at $\alpha=0.01$ and $\Delta \ge +10.0\%$) resolves the governance contradiction for RP-02. Historical Phase 3 evidence is strictly preserved as `PROMISING_BUT_NOT_SIGNIFICANT` while establishing an objective path to `CONFIRMED_BY_PHASE4_REPLICATION`.

8. **Cost Modeling & Budget Hierarchy Reconciliation**:
   - Evaluated `AS-13` and `AS-14`. Incorporating $N=650$ ($1,300$ episodes) increases `EXP-AB-02-REP` spend to $\$6.60$, bringing total projected Phase 4 spend to **$20.35 USD**.
   - **Budget Hierarchy Disambiguation**: The relationship between the **$50.00 USD** Phase 4 execution abort threshold (`AF-01`, `PHASE4_BUDGET_ABORT_THRESHOLD`) and the **$100.00 USD** overarching project ceiling (`GLOBAL_API_HARD_CEILING`, `NC-38`) is verified as structurally sound. They govern different operational scopes: Phase 4 execution halts at $50.00 USD (leaving a $>2.45\times$ safety margin over estimated $20.35 USD spend) while the broader program ceiling is $100.00 USD. No ambiguity exists.

9. **Stopping Rules & Abort Register (`AS-14`)**:
   - Evaluated `AS-14`. Hard stop triggers ($AF-01$ financial runway, $AF-02$ provider degradation, $AF-03$ deadlock, $AF-04$ token runaway, $AF-05$ memory leak) enforce automated safety boundaries with clear post-abort triage.

10. **External Validity & Causal Claim Discipline**:
    - Evaluated `AS-01`, `AS-02`, and `AS-16`. The mandatory 5-field causal claim format (`claim_id`, `mechanistic_claim`, `scope_boundary`, `counterfactual_contrast`, `falsification_condition`) prevents over-generalization from synthetic benchmarks to real-world deployment.

11. **Combinatorial Explosion Risk Mitigation**:
    - Evaluated `AS-11`. The explicit prohibition of the unconstrained Cartesian product ($58,320$ cells) and the mandatory 5-field metadata contract (`number_of_active_factors`, `reason_for_combination`, `interaction_hypothesis`, `maximum_stress_level`, `early_stop_rule`) successfully eliminate the risk of compute or analysis collapse.

12. **Network Isolation & Brokered Live API Execution**:
    - Evaluated `AS-14` §3. Reconciling container network isolation (`--network none`, `NC-16`) with live model provider evaluation (`NC-39`) via a two-tier brokered architecture (Isolated Container $\to$ Controlled Inference Broker $\to$ Model API) provides airtight credential protection, pre-call budget gating, and model fingerprint drift tracking without disabling isolation. Outcome: **`NETWORK_EXECUTION_CONTRACT_PASS`**.

---

## 2. Formal Independent Review Verdict

- **Layer B Substantive Contract Review Verdict**: **`SUBSTANTIVE_CONTRACT_REVIEW_PASS`**
- **Specific Technical Verdicts**:
  - `ROUTING_RULE_CONSISTENCY_PASS`
  - `NETWORK_EXECUTION_CONTRACT_PASS`
- **Evaluated Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)
- **Recommended Gate Outcome**: **`READY_FOR_ABLATION_EXECUTION`** (Subject to Requester Authorization)

### Binding Governance Invariants:
1. **Design Only Certified**: Certification applies exclusively to experimental protocols, statistical specifications, and governance contracts.
2. **Zero Execution Authority**: No code execution, paid model calls, or stress runs are authorized (`Phase 4 Execution Authority: NOT_GRANTED`).
3. **Architecture Unfrozen**: Architecture remains strictly exploratory (`Architecture Status: UNFROZEN`).
4. **Implementation Not Granted**: SimLab implementation authority remains strictly `NOT_GRANTED`.



---

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



---

# AS-17: Phase 4 Design Gate Package & Formal Recommendation
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN` $\to$ `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Evaluation Date**: 2026-09-16  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Executive Gate Clarification & Lifecycle Disambiguation

The pre-execution design gate is formally disambiguated from post-execution adjudication:
- **Canonical Design Gate**: **`PHASE_4_DESIGN_GATE`** (Alias: `GATE_R4D`).
- **Post-Execution Gate**: **`GATE_R4`** is strictly reserved for the adjudication gate following live Phase 4 ablation and stress execution and independent adversarial review.

### Allowed Design Gate Outcomes:
1. **`CONTINUE_PHASE4_DESIGN`**: Design specifications require further theoretical refinement or power modeling.
2. **`INSUFFICIENT_ABLATION_DESIGN`**: Proposed experimental designs fail methodological, statistical, or budget standards.
3. **`READY_FOR_ABLATION_EXECUTION`**: Design specifications, statistical contracts, failure registers, and explosion controls are certified complete and hardened.

---

## 2. Executive Gate Evaluation

The Phase 4 design program has established a complete, methodologically rigorous ablation and stress-testing roadmap across all four reproduced primitives (`AS-01` through `AS-18`), adhering strictly to the **Minimum Ablation Principle**, **Power-Driven Sample Size Derivation**, the **Complexity Burden Rule**, and **Stress-Matrix Explosion Controls**.

```
+----------------------------------------------------------------------------------------------------+
|                               PHASE 4 DESIGN GATE CANONICAL STATE                                  |
+----------------------------------------------------------------------------------------------------+
| Lifecycle State:             PHASE_4_DESIGN_COMPLETE                                               |
| Design Gate:                 PHASE_4_DESIGN_GATE                                                   |
| Decision:                    READY_FOR_ABLATION_EXECUTION                                          |
| Architecture:                UNFROZEN                                                             |
| Final SimLab Implementation: NOT_GRANTED                                                          |
| Phase 4 Execution Authority: NOT_GRANTED                                                          |
| Next Action:                 REQUESTER AUTHORIZATION REQUIRED                                      |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. Formal Gate Recommendation

### Formal Decision: **`READY_FOR_ABLATION_EXECUTION`**

### Invariants & Execution Halt:
1. **Design Only Certified**: This gate certifies the scientific, statistical, and operational validity of deliverables `AS-01` through `AS-18`.
2. **Zero Execution Authorized**: No experiments, paid model calls, or simulation runtime code have been or may be executed without separate, explicit authorization from the human requester.
3. **Architecture Remains Unfrozen**: All findings remain empirical evidence; zero architecture decisions are frozen.
4. **Final SimLab Implementation Authority**: `NOT_GRANTED`.

---

## 4. Final Curo Invariant

> **Reproduction establishes that an effect may exist.**  
> **Ablation identifies which component contributes to it.**  
> **Stress testing establishes its operating envelope.**  
> **Primitive Adjudication may advance only evidence that survives all three under preregistered criteria.**  
>  
> *Practical failure does not require statistical significance to matter.*  
> *Statistical significance does not make a trivial effect operationally important.*  
> *Stress escalation must respond to either meaningful degradation, strong statistical evidence, or a bounded mechanistically important failure signal.*  
> *Statistical methods must be named according to what they actually compute.*



---

# AS-18: Primitive Advancement Contract
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: PHASE_4_DESIGN  
**Design Gate**: PHASE_4_DESIGN_GATE (Alias: GATE_R4D)  
**Adjudication Gate Status**: GATE_R4 strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: UNFROZEN  
**Final SimLab Implementation Authority**: NOT_GRANTED  
**Phase 4 Execution Authority**: NOT_GRANTED  

---

## 1. Purpose & Pre-Execution Binding Rule

To maintain absolute epistemic discipline and prevent post-hoc outcome rationalization, this contract defines the **minimum evidentiary threshold** required for any multi-agent primitive to advance to Primitive Adjudication (GATE_R4).

**Core Governance Rule**:
All advancement rules must be codified **PRIOR** to Phase 4 execution. Evaluators are strictly forbidden from inventing, relaxing, or altering advancement criteria after experimental results are observed (NC-49, NC-66).

---

## 2. Seven Mandatory Primitive Advancement Criteria (A through G)

A cognitive or organizational primitive may advance to Primitive Adjudication **ONLY IF ALL SEVEN** of the following criteria are verified:

### Criterion A: Reproduction Evidence & Lineage Continuity
- **Requirement**: Reproduction evidence must be satisfied by either:
  - **A1 (Direct Phase 3 Qualification)**: A qualifying Phase 3 empirical status of `SUPPORTED` or `SUPPORTED_WITH_CONSTRAINTS`; **OR**
  - **A2 (Phase 4 Preregistered Confirmatory Replication)**: For primitives whose Phase 3 status was `PROMISING_BUT_NOT_SIGNIFICANT` (specifically `PR-ORG-01` / RP-02 private-information coordination), a preregistered `CONFIRMATORY_REPLICATION` (`EXP-AB-02-REP`) that successfully achieves its approved primary statistical threshold ($\alpha = 0.01$, two-sided) and minimum effect-size threshold ($\Delta \ge +10.0\%$).
- **Evidence-Status Transition Rule**:
  - If A2 succeeds, the governance harness explicitly records an immutable status transition from `PROMISING_BUT_NOT_SIGNIFICANT` to `CONFIRMED_BY_PHASE4_REPLICATION`:
    $$\text{PROMISING\_BUT\_NOT\_SIGNIFICANT} \longrightarrow \text{CONFIRMED\_BY\_PHASE4\_REPLICATION}$$
  - The historical Phase 3 finding is **NEVER** retroactively altered, rewritten, or erased. Historical evidence lineage is strictly preserved across all audit layers.
- **Falsification Standard**: Primitives whose Phase 3 findings resulted in `REJECT` or unmitigated `EQUIVALENCE_NOT_ESTABLISHED` (e.g. homogeneous GSM8K debate without tools), or whose Phase 4 confirmatory replication fails to meet the pre-registered $\alpha = 0.01$ and $\Delta \ge +10.0\%$ thresholds (`NOT_CONFIRMED`), are disqualified from advancement.


### Criterion B: Ablation Evidence
- **Requirement**: The component claimed to matter must demonstrate a statistically significant, measurable contribution relative to a valid, compute-matched control ($\Delta > 0, p < lpha$).
- **Falsification Standard**: If ablating the component produces negligible difference ($\Delta \le 	ext{margin}$) or if performance is driven entirely by a confounding factor (e.g. role prompts having zero effect when context boundary is ablated in SOPs), the primitive's standalone causal claim is falsified.

### Criterion C: Stress Evidence
- **Requirement**: The primitive must survive at least one pre-defined non-trivial stress regime (e.g. MODERATE stress under partial observation, memory noise, or distribution shift) without catastrophic accuracy collapse.
- **Falsification Standard**: If the primitive collapses immediately upon transitioning from clean BASELINE to MILD/MODERATE stress, it cannot advance as an architectural building block.

### Criterion D: Failure Boundary Documentation
- **Requirement**: The specific operating limits, degradation points, and failure cliff conditions under which the primitive breaks down must be empirically mapped and documented in the failure register.
- **Falsification Standard**: Unbounded claims of universal functionality or absence of a demonstrated failure boundary disqualify the primitive from advancement.

### Criterion E: Cost / Complexity Justification
- **Requirement**: The net performance benefit must remain positive and meaningful after accounting for token consumption, API latency, operational complexity, and implementation maintenance burden (NC-37).
- **Falsification Standard**: If a primitive delivers $+2\%$ accuracy but incurs 	imes$ token overhead or introduces severe synchronization bottlenecks, the Complexity Burden Rule blocks advancement.

### Criterion F: Confound Status
- **Requirement**: Zero unresolved critical confounds or benchmark artifacts (e.g. token mismatches, data leakage, prompt cues, unpinned models) may invalidate the interpretation of the results.
- **Falsification Standard**: Any experiment exhibiting model fingerprint drift (AF-02) or un-normalized compute (NC-10) is invalidated.

### Criterion G: External Validity Delimitation
- **Requirement**: The supported operating domain and unsupported domain must be explicitly delineated with negative boundaries (NC-46, NC-55).
- **Falsification Standard**: Primitives lacking explicit negative boundary statements are disqualified.

---

## 3. Non-Advancement Classifications

If a primitive fails any of the seven mandatory criteria, it **MUST NOT** advance to Primitive Adjudication. It must be classified strictly as one of the following five pre-registered outcomes:

| Classification | Definition & Evidentiary Trigger | Lifecycle Action |
|:---|:---|:---|
| **SUPPORTED_WITH_CONSTRAINTS** | The primitive survives Criteria A, B, C, D, and F, but has restricted operational boundaries (Criterion G) or tight cost constraints (Criterion E). | Advanced conditionally; final SimLab design must enforce strict runtime guardrails. |
| **CONTEXT_DEPENDENT** | The primitive demonstrates clear benefit under specific conditions (e.g. partitioned private knowledge) but shows zero benefit or negative utility elsewhere (e.g. homogeneous closed tasks). | Advanced for specialized workflows only; prohibited from global default deployment. |
| **DEFER** | The primitive requires higher-scale or cross-phase testing (e.g. 50+ agent populations deferred to Phase 8) or depends on unresolved upstream primitives. | Held in freeze; zero SimLab implementation code authorized until dependencies clear. |
| **REJECT** | The primitive fails Criterion B (ablation shows no causal contribution) or Criterion C (immediate collapse under stress), or was empirically falsified in Phase 3. | Discarded permanently from SimLab architecture. |
| **INSUFFICIENT_EVIDENCE** | Experimental runs were compromised by confounds, under-powering ( > lpha$ on non-replicated effects), or failure triggers (-01$ to -07$). | Requires protocol redesign or amendment under EXPERIMENT_AMENDMENT_REQUIRED. |

---

## 4. Final Curo Invariant

> **Reproduction establishes that an effect may exist.**  
> **Ablation identifies which component contributes to it.**  
> **Stress testing establishes its operating envelope.**  
> **Primitive Adjudication may advance only evidence that survives all three under preregistered criteria.**


---

