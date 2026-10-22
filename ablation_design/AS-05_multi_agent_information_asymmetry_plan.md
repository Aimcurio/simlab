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


