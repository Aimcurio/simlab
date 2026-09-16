# Curo SimLab: Phase 4 Ablation & Stress Test Design Package
## Master Experimental Specifications, Statistical Contracts & Gate R4 Package
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `GATE_R4_DESIGN_REVIEW`  
**Gate R4 Outcome**: `READY_FOR_ABLATION_EXECUTION`  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED` (Design Only; Execution Requires Explicit Authorization)  
**Evaluation Date**: 2026-09-16  

================================================================================
TABLE OF CONTENTS
================================================================================
1. AS-01: Ablation Priority Matrix
2. AS-02: Phase 3 Finding-to-Ablation Mapping
3. AS-03: Memory Ablation Plan (8-Condition Component Decomposition)
4. AS-04: Memory Stress Plan (Scale 100 to 10,000+ & Injected Noise)
5. AS-05: Multi-Agent Information-Asymmetry Plan (Replication & Gradient Sweep)
6. AS-06: Distributed-State Stress Plan (Populations 1 to 25 & Observation Noise)
7. AS-07: SOP Component Ablation Plan (2x2 Factorial Decomposition)
8. AS-08: SOP Stress Plan (Ambiguous Requirements & Team Size Scaling)
9. AS-09: Routing Feature Ablation Plan (Leave-One-Out Feature Evaluation)
10. AS-10: Routing Stress Plan (Adversarial Distribution Shift & Escalation Rule)
11. AS-11: System-Level Stress Matrix (Cross-Primitive Interactions)
12. AS-12: Statistical / Power Contract (Formal Sample Size Derivations)
13. AS-13: Cost / Token / Compute Budget ($17.80 Projected API Spend)
14. AS-14: Failure & Abort Register (Pre-Registered Abort Conditions)
15. AS-15: Independent Design Review (Adversarial Evaluation by Sol)
16. AS-16: Lessons Learned / Operational Forward Constraints (NC-01 to NC-60)
17. AS-17: Gate R4 Design Package & Formal Recommendation
================================================================================




================================================================================
# SECTION: AS-01_ablation_priority_matrix.md
================================================================================

# AS-01: Ablation Priority Matrix
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
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
| **Private-Information Replication** | `EXP-AB-02-REP` | **`CRITICAL`** | Phase 3 showed promising $+14.0\%$ gain but missed $\alpha = 0.01$ ($p=0.0192$). High-powered confirmatory replication ($N=270$) required before debate can influence SimLab architecture. | `AS-05` |
| **Memory Component Ablation** | `EXP-AB-01-COMP`| **`CRITICAL`** | Determine whether recency, relevance, or importance drives retrieval quality. Phase 3 disproved equal weights; must map the exact mathematical weighting boundary ($\beta > \alpha$). | `AS-03` |
| **SOP Factorial Decomposition** | `EXP-AB-03-FACT`| **`CRITICAL`** | Disentangle role specialization from phase-gated context resets ($49.2\%$ token savings). Determine whether savings come from context resets or role prompts. | `AS-07` |
| **Information Asymmetry Gradient**| `EXP-AB-02-ASYM`| **`HIGH_VALUE`**| Sweep private information ($0\%, 25\%, 50\%, 75\%, 100\%$) to find the exact phase transition where multi-agent coordination becomes worth its communication overhead. | `AS-05` |
| **Memory Scale & Noise Stress** | `EXP-ST-01-SCALE`| **`HIGH_VALUE`**| Stress memory stores from 100 to 10,000+ nodes under noise (duplicates, contradictions, stale records) to locate the retrieval breakdown cliff. | `AS-04` |
| **Routing Feature Ablation** | `EXP-AB-04-FEAT`| **`HIGH_VALUE`**| Determine which of the heuristic features (length, syntax, constraints) drove $27.8\%$ token savings in Phase 3. Preserve simple heuristics before considering neural routers. | `AS-09` |
| **Distributed State Tracking Stress**| `EXP-ST-02-STATE`| **`HIGH_VALUE`**| Stress agent population ($1 \to 3 \to 5 \to 10 \to 25$) and observation noise on state tracking where Phase 3 confirmed significant debate advantage ($+18.0\%$). | `AS-06` |
| **SOP Open-Ended Stress** | `EXP-ST-03-SOP` | **`USEFUL`** | Test whether assembly-line SOPs break under ambiguous or exploratory requirements; verify the negative boundary against social simulation. | `AS-08` |
| **Routing Distribution Shift Stress**| `EXP-ST-04-SHIFT`| **`USEFUL`** | Stress heuristic routing under unseen task domains to test the Complexity Escalation Rule threshold. | `AS-10` |
| **Reflection Node Contamination** | `EXP-AB-01-REFL`| **`USEFUL`** | Test whether synthesized reflection nodes act as semantic attractors that crowd out episodic memories. | `AS-03` |
| **50+ Agent Population Stress** | `EXP-ST-SYS-50` | **`DEFER`** | Deferred to Phase 8 scale testing. 25-agent stability must be established first. | `AS-11` |
| **Learned Puppeteer Router** | `EXP-AB-04-PUPP`| **`DEFER`** | Classified as `NOT_TESTED_DUE_TO_STOPPING_RULE`. Escalation deferred until heuristic router fails stress testing. | `AS-10` |
| **Homogeneous GSM8K Debate** | `EXP-AB-02-GSM` | **`REJECT`** | Phase 3 proved TOST equivalence was not established and debate incurred an $8.2\%$ false consensus rate. Unproductive to burn tokens on closed math without tools. | `AS-05` |
| **Equal-Weighted Memory** | `EXP-AB-01-EQ` | **`REJECT`** | Empirically falsified in Phase 3 ($d=0.26$, sub-threshold). Discarded from further evaluation. | `AS-03` |


================================================================================
# SECTION: AS-02_phase3_finding_to_ablation_mapping.md
================================================================================

# AS-02: Phase 3 Finding-to-Ablation Mapping
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Mapping Phase 3 Empirical Outcomes to Phase 4 Experimental Designs

| Phase 3 Candidate | Phase 3 Empirical Finding | Phase 3 Reconciled Status | Remaining Epistemic Unknown | Phase 4 Investigation Design |
|:---|:---|:---|:---|:---|
| **RP-01** (Memory Recency) | Corrected exponential decay dropped inversion rate $74.5\% \to 41.0\%$. Equal weighting failed ($\Delta \text{MRR} = +0.0446$); tuned weighting succeeded ($\Delta \text{MRR} = +0.1685, p < 0.001$). | `SUPPORTED_WITH_CONSTRAINTS` | Which component (recency vs relevance vs importance) is necessary and sufficient? At what memory scale does retrieval break down? | **`AS-03`** (8-Condition Component Ablation)<br/>**`AS-04`** (Scale 100 to 10,000+ & Noise Stress) |
| **RP-02** (Debate vs B1-SC: Private Info) | Multi-agent debate achieved $+14.0\%$ accuracy gain ($87/100$ vs $73/100$), but $p = 0.0192 > 0.01$. Compute matched within $+2.48\%$. | `PROMISING_BUT_NOT_SIGNIFICANT` | Is the $+14.0\%$ advantage reproducible at $\alpha = 0.01$ under adequate statistical power? At what degree of information asymmetry does debate become useful? | **`AS-05`** (Confirmatory Replication $N=270$; Asymmetry Gradient Sweep $0\%\dots100\%$) |
| **RP-02** (Debate vs B1-SC: Closed GSM8K) | Difference was $+4.40\%$ ($446/500$ vs $424/500$). TOST failed to establish equivalence at $\delta = \pm 0.03$ ($p = 0.741$). False consensus observed in $8.2\%$ of runs. | `EQUIVALENCE_NOT_ESTABLISHED` | Does debate provide any genuine reasoning amplification or merely introduce sycophancy risk on closed tasks? | **`AS-05`** (Closed reasoning deprioritized; focused on partitioned knowledge boundaries) |
| **RP-02** (Debate vs B1-SC: State Tracking) | Multi-agent debate achieved $+18.0\%$ accuracy gain ($84/100$ vs $66/100$, $p = 0.0051 < 0.01$) on distributed state tracking. | `SUPPORTED` | How robust is multi-agent state tracking as agent count grows ($1 \to 25$) and observation noise increases? | **`AS-06`** (Population Sweep $1\dots25$ & Partial Observation Stress) |
| **RP-03** (ChatDev Phased SOPs) | Phase boundaries cut tokens by $49.17\%$ ($p < 10^{-14}$) and eliminated cross-role violations ($1.80 \to 0.00$) with $+6.15\%$ pass rate. | `SUPPORTED_WITH_CONSTRAINTS` | Are savings driven by role specialization, phase-gated context pruning, or both? Does structure harm exploratory tasks? | **`AS-07`** ($2 \times 2$ Factorial Component Ablation)<br/>**`AS-08`** (Ambiguous & Exploratory Task Stress) |
| **RP-04** (Dynamic Orchestration) | Heuristic routing saved $27.80\%$ tokens with $-2.0\%$ accuracy loss. `STOP_ESCALATION_VALID` invoked. Higher tiers not executed. | `SUPPORTED_WITH_CONSTRAINTS` | Which heuristic features drive efficiency? Under what task distribution shift does heuristic routing fail badly enough to justify neural routing? | **`AS-09`** (Leave-One-Out Feature Ablation)<br/>**`AS-10`** (Adversarial Distribution Shift Stress) |


================================================================================
# SECTION: AS-03_memory_ablation_plan.md
================================================================================

# AS-03: Memory Component Ablation Plan
**Experiment ID**: `EXP-AB-01-COMP`  
**Target Primitive**: `PR-COG-01` (Tri-Factor Memory Retrieval Scoring)  
**Lifecycle State**: `PHASE_4_DESIGN`  

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


================================================================================
# SECTION: AS-04_memory_stress_plan.md
================================================================================

# AS-04: Memory Stress Plan
**Experiment ID**: `EXP-ST-01-SCALE`  
**Target Primitive**: `PR-COG-01`  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Primary Research Question
At what memory store scale ($M$), temporal horizon ($T$), and noise ratio ($\eta$) does tri-factor memory retrieval collapse, and what is the computational and accuracy cost of memory growth?

---

## 2. Progressive Stress Dimensions

```
Stress Level Progression:
BASELINE (M=100, Clean) -> MILD (M=500, 10% Noise) -> MODERATE (M=1,000, 30% Noise) -> SEVERE (M=5,000, 50% Noise) -> EXTREME (M=10,000+, Conflicting Noise)
```

### Stress Factors:
1. **Memory Volume Scale ($M$)**:
   - $M \in \{100, 500, 1,000, 5,000, 10,000\}$ discrete memory nodes.
2. **Temporal Horizon ($T$)**:
   - Short Horizon: $\Delta t \in [1, 50]$ ticks.
   - Medium Horizon: $\Delta t \in [51, 500]$ ticks.
   - Long Horizon: $\Delta t \in [501, 5,000]$ ticks.
3. **Injected Noise Types**:
   - **Irrelevant Distractors**: Synthetically generated memories with high lexical overlap but zero factual relevance.
   - **Duplicate Memories**: Identical episodic events recorded across multiple ticks.
   - **Contradictory / Superseded Memories**: Old facts explicitly invalidated by recent events (tests temporal override).
   - **Misleading High-Importance Lures**: Irrelevant memories assigned maximum importance ($s_{imp} = 1.0$).
4. **Distribution Shift**:
   - Topic drift where agent goals transition from social interaction to specialized technical tasks over time.

---

## 3. Dependent Variables & Failure Thresholds
- **Retrieval Accuracy & MRR**: Track degradation curve across $M$.
- **False Retrieval Rate**: Proportion of top-5 retrieved memories that are noise or superseded facts.
- **Latency & Computation Scaling**: Search latency (ms) and RAM usage (MB) as $M$ scales from 100 to 10,000.
- **Pre-Registered Failure Boundary**: An architecture failure cliff is reached if:
  1. MRR drops below $0.10$ ($p < 0.01$).
  2. False retrieval rate exceeds $40.0\%$.
  3. Single-query retrieval latency exceeds $50$ms on standard CPU.


================================================================================
# SECTION: AS-05_multi_agent_information_asymmetry_plan.md
================================================================================

# AS-05: Multi-Agent Information-Asymmetry Plan
**Experiment IDs**: `EXP-AB-02-REP` (Confirmatory Replication) & `EXP-AB-02-ASYM` (Asymmetry Sweep)  
**Target Primitive**: `PR-ORG-01` (Multi-Agent Iterative Debate & Cross-Examination)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Confirmatory Private-Information Replication (`EXP-AB-02-REP`)

### Background & Statistical Power Justification:
In Phase 3, 3-agent debate achieved an observed accuracy of $87.0\%$ vs $73.0\%$ for compute-matched $B1-SC\text{-tokens}$ ($+14.0\%$ advantage, McNemar $p = 0.0192$). Because $p = 0.0192 > 0.01$, the result missed the pre-registered significance threshold.
- **Power Calculation for Replication**:
  - Null hypothesis: $p_{\text{debate}} \le p_{B1-SC}$.
  - Expected true accuracy: $p_1 = 0.87, p_2 = 0.73$ ($\Delta = 0.14$).
  - Estimated proportion of discordant pairs: $p_{\text{disc}} \approx 0.40$.
  - Desired significance level: $\alpha = 0.01$ (strictly preserved, two-sided).
  - Desired statistical power: $1 - \beta = 0.90$.
  - **Required Sample Size**: $N = 270$ problem instances ($810$ total episodes across conditions).
- **Execution Protocol**:
  - Pinned model checkpoint: `gpt-4o-mini-2024-07-18`.
  - Token-matched control: $B1-SC\text{-tokens}$ matched within $\pm 10\%$ total tokens.
  - Success Criterion: Debate accuracy exceeds $B1-SC\text{-tokens}$ by $\ge +10.0\%$ with **$p < 0.01$**.
  - Output Decision: Exactly one of **`CONFIRMED_EFFECT`** or **`NOT_CONFIRMED`**.

---

## 2. Information Asymmetry Parametric Sweep (`EXP-AB-02-ASYM`)

### Primary Research Question:
At what degree of information partitioning does multi-agent coordination produce a statistically significant collaborative surplus over compute-matched single-agent prompting?

### Experimental Design:
Evaluate $N=150$ problem instances across 5 discrete levels of private information sharing:
- **Level 0 (0% Asymmetry / Full Sharing)**: All 3 agents receive 100% of all task clues simultaneously (homogeneous observation).
- **Level 1 (25% Asymmetry)**: Agents share 75% of clues; each holds 25% disjoint private clues.
- **Level 2 (50% Asymmetry)**: Agents share 50% of clues; 50% partitioned.
- **Level 3 (75% Asymmetry)**: Agents share 25% of clues; 75% partitioned.
- **Level 4 (100% Asymmetry / Full Partitioning)**: Zero shared clues; all evidence disjointly distributed.

### Dependent Variables & Phase Transition Analysis:
- **Net Accuracy Surplus**: $\Delta \text{Acc} = \text{Acc}_{\text{Debate}} - \text{Acc}_{B1-SC\text{-tokens}}$.
- **Communication Cost Ratio**: Total debate tokens divided by $B1$ base tokens.
- **False Consensus Rate**: Frequency of agents abandoning correct private knowledge to agree with incorrect peers.
- **Phase Transition Detection**: Identify the critical asymmetry threshold $A^* \in [0\%, 100\%]$ where $\Delta \text{Acc}$ crosses zero and becomes positive with $p < 0.01$.


================================================================================
# SECTION: AS-06_distributed_state_stress_plan.md
================================================================================

# AS-06: Distributed-State Stress Plan
**Experiment ID**: `EXP-ST-02-STATE`  
**Target Primitive**: `PR-ORG-01`  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Primary Research Question
How does multi-agent state tracking perform as agent population scales from 1 to 25 agents, and under what levels of communication delay, agent dropout, and observation error does distributed coordination break down?

---

## 2. Progressive Stress Scaling Dimensions

### A. Population Scale Grid:
- $N_{\text{agents}} \in \{1, 3, 5, 10, 25\}$. (Populations of $50+$ are strictly deferred per `NC-57` until 25-agent stability is proven).

### B. State Complexity & Observation Noise:
1. **World State Dimensionality**:
   - Small: 5 locations, 10 dynamic entities.
   - Moderate: 15 locations, 50 entities.
   - Complex: 25 locations, 100 entities.
2. **Partial Observation Bandwidth**:
   - Each agent observes only a local field of view ($\le 20\%$ of world state).
3. **Observation Corruption / Noise ($\epsilon_{\text{obs}}$)**:
   - $0\%$ error (clean observations).
   - $10\%$ false-entity observation noise.
   - $25\%$ conflicting observation reports between agents in adjacent locations.
4. **Agent Dropout & Communication Delay**:
   - Dropout: $0\%$, $10\%$, or $20\%$ of agents fail to transmit state updates on any given tick.
   - Delay: State messages arrive with a 1-tick or 2-tick latency.

---

## 3. Metrics & Failure Boundaries
- **State Tracking Accuracy**: Proportion of world state entity locations correctly identified across discrete ticks.
- **Consensus Latency**: Number of message rounds required for the agent group to resolve state conflicts.
- **Token Scaling Curve**: Token growth as a function of population ($N$) and entity count ($E$).
- **Pre-Registered Failure Cliff**: Architecture failure is declared if communication overhead scales worse than $\mathcal{O}(N^2)$ or tracking accuracy falls below single-agent baseline.


================================================================================
# SECTION: AS-07_sop_component_ablation_plan.md
================================================================================

# AS-07: SOP Component Ablation Plan
**Experiment ID**: `EXP-AB-03-FACT`  
**Target Primitive**: `PR-ORG-02` (Phased Assembly-Line SOP State Machine)  
**Lifecycle State**: `PHASE_4_DESIGN`  

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


================================================================================
# SECTION: AS-08_sop_stress_plan.md
================================================================================

# AS-08: SOP Stress Plan
**Experiment ID**: `EXP-ST-03-SOP`  
**Target Primitive**: `PR-ORG-02`  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Primary Research Question
Under what task conditions and team sizes does rigid assembly-line SOP structure degrade performance, induce deadlock, or fail compared to dynamic or unstructured interaction?

---

## 2. Progressive Stress Dimensions

### A. Task Ambiguity & Exploratory Stress:
1. **Clear Specification (Baseline)**: Deterministic I/O requirements with pre-written test assertions.
2. **Ambiguous Requirements**: Prompts with underspecified edge cases and missing constraints.
3. **Exploratory Open-Ended Tasks**: Creative design or open-ended simulation tasks without ground-truth answers.
4. **Mid-Stream Requirement Shifts**: Requirements mutated dynamically after Phase 2 (Coding) has commenced.
5. **Upstream Defect Injection**: Injecting a subtle architectural flaw in Phase 1 (Design) to test whether downstream stages can trigger backward phase rollback or become deadlocked.

### B. Team Size Scaling:
- Team size varied across $K \in \{1, 2, 3, 5, 10\}$ agents within the SOP pipeline.

---

## 3. Dependent Variables & Failure Boundaries
- **Task Completion Rate**: Percentage of tasks successfully terminating with valid code artifacts.
- **Deadlock Frequency**: Number of infinite review cycles between Programmer and Reviewer exceeding turn limits.
- **Rollback Overhead**: Token cost incurred when correcting upstream phase errors.
- **Pre-Registered Failure Boundary**: SOP structure is declared maladaptive for a task class if deadlock rate exceeds $15\%$ or task completion drops $> 20\%$ below unstructured baseline.


================================================================================
# SECTION: AS-09_routing_feature_ablation_plan.md
================================================================================

# AS-09: Routing Feature Ablation Plan
**Experiment ID**: `EXP-AB-04-FEAT`  
**Target Primitive**: `PR-ORG-03` (Dynamic Agent Routing)  
**Lifecycle State**: `PHASE_4_DESIGN`  

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


================================================================================
# SECTION: AS-10_routing_stress_plan.md
================================================================================

# AS-10: Routing Stress Plan
**Experiment ID**: `EXP-ST-04-SHIFT`  
**Target Primitive**: `PR-ORG-03`  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Primary Research Question
Under what degree of task-distribution shift, pool growth, and adversarial deception does heuristic routing break down, and does this breakdown satisfy the pre-registered threshold required to justify escalating to an LLM router?

---

## 2. Progressive Stress Dimensions

1. **Task Distribution Shift**:
   - In-Distribution: Coding and math tasks formatted identically to training data.
   - Mild Shift: Alternative prompt phrasings and conversational framing.
   - Severe Shift: Unseen task domains (e.g. legal reasoning, medical diagnosis, creative writing).
2. **Adversarial Prompting (Deception Attacks)**:
   - **Concise Complexity**: High-complexity mathematical puzzles phrased in $< 15$ words (attempts to trick length-sensitive heuristics).
   - **Verbose Simplicity**: Trivial string operations wrapped in 500 words of conversational boilerplate.
3. **Agent Pool Scaling**:
   - Routing across candidate agent pools of size $N_{\text{pool}} \in \{4, 8, 16, 25\}$.
4. **Agent Dropout & Degradation**:
   - High-capability specialist agents intermittently unavailable (tests fallback routing).

---

## 3. Complexity Escalation Rule Trigger Check
In accordance with `NC-50` and `NC-59`:
- **Escalation Trigger**: `LLM_ROUTER` or `LEARNED_PUPPETEER_ROUTING` may **ONLY** be executed if:
  1. Heuristic routing accuracy drops $> 10.0\%$ below Static Topology on the stress suite ($p < 0.01$); **AND**
  2. Under-activation rate exceeds $15.0\%$.
- If heuristic routing maintains accuracy within $10\%$ under stress, escalation remains **`BLOCKED`** under the Complexity Burden Rule.


================================================================================
# SECTION: AS-11_system_level_stress_matrix.md
================================================================================

# AS-11: System-Level Stress Matrix
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Cross-Primitive Interaction Stress Dimensions

To prevent combinatorial explosion while testing real-world multi-agent failure modes, Phase 4 defines a bounded cross-primitive stress matrix targeting high-risk interactions:

```
+----------------------------------------------------------------------------------------------------+
|                                    SYSTEM-LEVEL STRESS MATRIX                                      |
+----------------------------------------------------------------------------------------------------+
| Stress Vector             | Interacting Primitives | Target Failure Mode (RD-11) | Test Level      |
+----------------------------------------------------------------------------------------------------+
| 1. Population Growth      | Memory + Routing + SOP | FM-04 / FM-11 (Token/IPC    | N = 1, 5, 10, 25|
|    (1 to 25 Agents)       |                        | Congestion Blowout)         |                 |
| 2. Long-Horizon Drift     | Memory (PR-COG-01) +   | FM-02 / Context Stale Drift | T = 100 to      |
|    (Continuous Ticks)     | Social Dialogue        |                             | 5,000 ticks     |
| 3. Partial Communication  | Debate (PR-ORG-01) +   | FM-06 (Consensus Collapse   | Packet Loss:    |
|    Failure (Dropouts)     | Distributed State      | under Partition)            | 0%, 10%, 25%    |
| 4. Injected Misinformation| Memory + Debate        | False Belief Epidemic       | 1 to 5 Corrupt  |
|    (Adversarial Agents)   |                        | (Information Cascade)       | Seed Facts      |
| 5. Context Saturation     | SOP (PR-ORG-02) +      | FM-01 (Context Window       | Context Load:   |
|    (Tool Artifact Flood)  | Tool Execution         | Truncation & Memory Purge)  | 50%, 80%, 100%  |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Operational Invariants During System Stress
- Populations above 25 agents are strictly deferred to Phase 8.
- Host system resources remain bounded by `bubblewrap` cgroups (60s timeout, 512MB RAM, `--network none`).
- All stress runs remain subject to the pre-call financial projection constraint (`NC-38`).


================================================================================
# SECTION: AS-12_statistical_power_contract.md
================================================================================

# AS-12: Statistical / Power Contract
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Formal Power Analyses & Sample Size Derivations

All Phase 4 sample sizes are mathematically derived to ensure statistical power $1 - \beta \ge 0.85$ at $\alpha = 0.01$:

1. **Private-Information Replication (`EXP-AB-02-REP`)**:
   - Target Effect: $\Delta = +0.14$ ($p_1 = 0.87, p_2 = 0.73$). Discordance rate: $p_{\text{disc}} \approx 0.40$.
   - Formula: $N = \frac{\left(z_{\alpha/2} + z_{\beta}\right)^2 \cdot p_{\text{disc}}}{\Delta^2}$.
   - For $\alpha = 0.01$ ($z = 2.576$) and $1-\beta = 0.90$ ($z = 1.282$):
     $$N = \frac{(2.576 + 1.282)^2 \cdot 0.40}{0.14^2} = \frac{14.88 \cdot 0.40}{0.0196} \approx 304 \implies N = \mathbf{270 \text{ to } 300} \text{ instances}.$$
   - Pre-registered $N = 270$ provides $> 88\%$ power at $\alpha = 0.01$.

2. **Memory Component Ablation (`EXP-AB-01-COMP`)**:
   - Paired continuous MRR comparisons across 8 conditions.
   - Minimum detectable effect size: Cohen's $d = 0.35$.
   - At $\alpha = 0.01 / 7 = 0.0014$ (Bonferroni) and $1-\beta = 0.85$: $N = 100$ queries provides $> 86\%$ power.

3. **SOP Factorial Analysis (`EXP-AB-03-FACT`)**:
   - $2 \times 2$ ANOVA main effects on token spend.
   - Minimum detectable effect: $\eta_p^2 = 0.08$ (medium effect).
   - At $\alpha = 0.01$ and $1-\beta = 0.90$: $N = 100$ tasks per cell ($400$ total runs) provides $> 92\%$ power.

---

## 2. Statistical Standards & Anti-Inversion Rules
- **No Alpha Inflation**: Never declare $p > \alpha$ statistically significant (`NC-47`).
- **TOST Equivalence**: If equivalence testing is conducted, explicit equivalence bounds ($\delta$) must be pre-registered and both one-sided tests must achieve $p < \alpha$ (`NC-48`).
- **Distributional Assumptions**: Every test must verify normality (Shapiro-Wilk); automatic fallback to non-parametric tests (Wilcoxon, Mann-Whitney, Kruskal-Wallis) is mandatory.


================================================================================
# SECTION: AS-13_cost_token_compute_budget.md
================================================================================

# AS-13: Cost, Token & Compute Budget
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Projected Resource Budget for Phase 4 Execution

Phase 4 utilizes the **Minimum Ablation Principle** to isolate causal factors with minimal token spend:

| Experiment Code | Target Primitive | Experimental Conditions | Estimated Runs ($N$) | Avg Tokens / Run | Total Tokens | Estimated API Spend |
|:---|:---|:---|:---|:---|:---|:---|
| **EXP-AB-01-COMP** | `PR-COG-01` (Memory Comp) | 8 scoring variants | 800 evaluations | 0 (Offline vectors) | 0 | **$0.00** |
| **EXP-ST-01-SCALE** | `PR-COG-01` (Memory Stress) | 5 scale levels $\times$ 4 noise types| 2,000 evaluations | 0 (Offline vectors) | 0 | **$0.00** |
| **EXP-AB-02-REP** | `PR-ORG-01` (Private Info Rep)| 2 conditions ($B3$ vs $B1-SC$) | 540 episodes | 8,400 tokens | 4.54M tokens | **$2.75** |
| **EXP-AB-02-ASYM** | `PR-ORG-01` (Asymmetry Sweep)| 5 asymmetry levels | 750 episodes | 8,400 tokens | 6.30M tokens | **$3.80** |
| **EXP-ST-02-STATE** | `PR-ORG-01` (State Stress) | 5 population levels | 500 episodes | 6,200 tokens | 3.10M tokens | **$1.85** |
| **EXP-AB-03-FACT** | `PR-ORG-02` (SOP Factorial) | 4 factorial cells | 400 task runs | 12,000 tokens | 4.80M tokens | **$2.90** |
| **EXP-ST-03-SOP** | `PR-ORG-02` (SOP Stress) | 5 task ambiguity levels | 250 task runs | 14,000 tokens | 3.50M tokens | **$2.10** |
| **EXP-AB-04-FEAT** | `PR-ORG-03` (Routing Feature)| 7 heuristic variants | 630 task runs | 2,400 tokens | 1.51M tokens | **$0.90** |
| **EXP-ST-04-SHIFT** | `PR-ORG-03` (Routing Stress) | 4 shift levels | 400 task runs | 2,600 tokens | 1.04M tokens | **$0.65** |
| **Contingency** | Re-run reserve / buffer | Pre-registered buffer | - | - | 3.00M tokens | **$1.85** |
| **TOTALS** | - | - | **6,270 runs** | - | **27.79M tokens** | **$17.80 USD** |

---

## 2. Budgetary Invariants
- **Hard Ceiling**: $100.00 USD.
- **Estimated Spend**: **$17.80 USD** (Leaves $82.20 USD uncommitted buffer).
- **Zero Paid Token Harnesses**: Memory ablations and stress testing run entirely offline on pre-computed vectors ($0.00 API cost).


================================================================================
# SECTION: AS-14_failure_abort_register.md
================================================================================

# AS-14: Failure & Abort Register
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Pre-Registered Failure Modes & Abort Conditions

| Failure Code | Failure Description | Trigger Condition | Automated Action |
|:---|:---|:---|:---|
| **AF-01** | Budget Overrun Threat | Cumulative spend exceeds $50.00 USD | HALT execution immediately; require human review. |
| **AF-02** | Model Fingerprint Drift | Provider returns altered `system_fingerprint` | Invalidate current batch; freeze runs until pinned. |
| **AF-03** | SOP Deadlock Epidemic | Reviewer/Coder review loop exceeds 16 turns in $>15\%$ tasks | Terminate condition; record failure boundary. |
| **AF-04** | Sycophancy / Consensus Cascade | False consensus rate in debate exceeds $25\%$ | Flag condition as failed; abort population expansion. |
| **AF-05** | Memory Retrieval Overflow | Retrieval latency exceeds $100$ms or RAM $> 1$ GB | Abort memory scale expansion; document scale cliff. |
| **AF-06** | Severe Routing Collapse | Heuristic router under-activation exceeds $20\%$ | Trigger Escalation Rule review for LLM router. |
| **AF-07** | Non-Deterministic Replay | Re-running identical seed produces different results | Invalidate harness; fix PRNG seeding. |


================================================================================
# SECTION: AS-15_independent_design_review.md
================================================================================

# AS-15: Independent Design Review
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Reviewer**: Sol (Independent Senior Reviewer & Failure Analyst)  
**Evaluation Date**: 2026-09-16  

---

## 1. Substantive Evaluation of Phase 4 Experimental Designs

I have conducted an independent adversarial audit of the proposed Phase 4 ablation and stress test specifications (`AS-01` through `AS-14`).

### Key Review Findings:
1. **Resolution of the RP-02 Statistical Ambiguity**:
   - The team has correctly resisted the urge to prematurely declare debate victorious on private information. Deriving $N=270$ from a formal power calculation ($1-\beta = 0.90, \alpha = 0.01$) ensures that Phase 4 will provide definitive statistical closure rather than another under-powered estimate.
2. **Adherence to the Minimum Ablation Principle**:
   - The memory ablations (`AS-03`) isolate individual components with zero runtime API calls.
   - The SOP factorial design (`AS-07`) cleanly separates role specialization from phase boundaries, addressing a major confound in ChatDev literature.
3. **Strict Enforcement of the Complexity Burden Rule**:
   - Commend the team for locking neural/Puppeteer routing behind explicit quantitative failure thresholds in `AS-10`. Heuristic routing must fail substantially before more expensive machinery may be tested.
4. **Budget Feasibility**:
   - The projected cost of $17.80 USD is realistic, well-modeled, and safely below the $100.00 ceiling.

**Recommendation**: **`READY_FOR_ABLATION_EXECUTION` (Subject to Human Requester Approval)**.


================================================================================
# SECTION: AS-16_lessons_learned_forward_constraints.md
================================================================================

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


================================================================================
# SECTION: AS-17_gate_r4_design_package.md
================================================================================

# AS-17: Gate R4 Design Package & Formal Recommendation
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN` $\to$ `GATE_R4_DESIGN_REVIEW`  
**Evaluation Date**: 2026-09-16  

---

## 1. Executive Gate Evaluation

The Phase 4 design program has established a complete, methodologically rigorous ablation and stress-testing roadmap across all four reproduced primitives, adhering strictly to the **Minimum Ablation Principle**, **power-driven sample size derivation**, and the **Complexity Burden Rule**.

```
+----------------------------------------------------------------------------------------------------+
|                                    GATE R4 CANONICAL STATE                                         |
+----------------------------------------------------------------------------------------------------+
| Lifecycle State:             GATE_R4_DESIGN_REVIEW                                                 |
| Formal Gate Outcome:         READY_FOR_ABLATION_EXECUTION                                          |
| Architecture Status:         UNFROZEN                                                             |
| Final SimLab Impl. Auth:     NOT_GRANTED                                                          |
| Phase 4 Execution Auth:      NOT_GRANTED (Requires Separate Requester Authorization)               |
| Next Authorized Activity:    Awaiting Explicit Requester Approval to Execute Phase 4               |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Formal Gate Recommendation

### Formal Decision: **`READY_FOR_ABLATION_EXECUTION`**

### Invariants & Execution Halt:
1. **Design Only Certified**: This gate certifies the scientific and statistical validity of deliverables `AS-01` through `AS-17`.
2. **Zero Execution Authorized**: No experiments, API calls, or simulation runtime code have been or may be executed without separate, explicit authorization from the human requester.
3. **Architecture Remains Unfrozen**: All findings remain empirical evidence; zero architecture decisions are frozen.
