# Scientific Audit Report: EXP-AB-01-COMP
## Focus: Reflection Mechanics (R5), Phase 3/4 Compatibility (R7), Primitive Evidence Status (R8), and Forward Constraints (R9)

**Experiment Target**: `EXP-AB-01-COMP` (Memory Component Ablation)  
**Primitive Under Test**: `PR-COG-01` (Generative Agent Cognitive Architecture / Memory Stream)  
**Auditor**: `audit_explorer_3` (Read-Only Exploration Agent)  
**Authority State**: `PHASE_4_EXECUTION_AUTHORIZED` | `EXECUTION_AUTHORITY: GRANTED_LIMITED_PHASE_4` | `ARCHITECTURE_STATUS: UNFROZEN` | `FINAL_SIMLAB_IMPLEMENTATION: NOT_GRANTED` | `PRIMITIVE_ADJUDICATION: NOT_AUTHORIZED`  
**Evaluation Date**: 2026-09-16  
**Benchmark Dataset**: `SimLab-MemBench-500.json` (SHA-256: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800`)  
**Raw Telemetry File**: `E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_telemetry.jsonl` (SHA-256: `9eb6846b017f76883418e3703dd9f0111182e8dc8a0ea03bb5cd32dd27337eac`)  
**Results File**: `E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_results.json`  

---

## Executive Summary of Audit Explorer 3 Findings

1. **R5 (Reflection Failure Analysis)**:
   Condition A8 (`TRI_FACTOR_REFLECTION`) suffered total retrieval collapse ($\text{MRR} = 0.0325$, $\text{NDCG@5} = 0.0000$) with 100% Rank-1 crowding (100/100 queries) and 100% saturation of top-five slots (500/500 slots occupied by reflections). This failure is classified definitively as an **`IMPLEMENTATION_DEFECT`** in `run_exp_ab_01_comp.py:72`, where synthetic reflection nodes were assigned a hardcoded `importance: 8.5`. Because all 500 episodic memories in `SimLab-MemBench-500` have importance in $[4.01, 6.00]$ (mean $5.0029$), min-max normalization squashed all episodic memories into $[0.0, 0.4432]$ while reflections monopolized $1.0000$. Under $\gamma = 0.3$, reflections received an unearned score advantage of $\ge +0.1670$. In Counterfactual Experiment 1, setting reflection importance to $5.0$ completely eliminated crowding ($0\%$ Rank-1 crowding, $0/500$ top-5 slots) and restored MRR to $0.0929$, disproving the hypothesis of a fundamental cognitive primitive failure.
2. **R7 (Phase 3 / Phase 4 Compatibility)**:
   The collapse of condition A7 ($\text{MRR} = 0.0941$) relative to Phase 3 `T-AltWeight` ($\text{MRR} = 0.2403$) is **NOT** an empirical contradiction, data corruption, or implementation divergence. It is strictly **A DIFFERENT WEIGHT REGIME** caused by an errant parameter swap in `AS-03_memory_ablation_plan.md:30`: AS-03 specified A7 as $(0.2, 0.5, 0.3)$, whereas Phase 3 `T-AltWeight` executed $(0.3, 0.5, 0.2)$. When Phase 4's continuous simplex sweep evaluated Phase 3's exact weights $(0.3, 0.5, 0.2)$, it produced an identical $\text{MRR} = \mathbf{0.2403}$ and $\text{NDCG@5} = \mathbf{0.2140}$, replicating Phase 3 to four decimal places. Formal `PHASE3_PHASE4_EVIDENCE_CONFLICT` is **NOT WARRANTED** at the empirical data level. However, Phase 4 component ablation fundamentally updates our epistemic understanding: importance was already acting as noise in Phase 3, and removing it entirely ($A4$, $\gamma=0$) boosts MRR to $0.5002$.
3. **R8 (Primitive Evidence Status)**:
   Updating strictly Criterion B (`ABLATION_EVIDENCE`) for `PR-COG-01`: The status is formally updated to **`COMPONENT_NOT_NECESSARY_UNDER_TESTED_CONDITIONS`**. Condition A4 (recency + relevance) outperformed full tri-factor A7 by $\Delta = +0.4061$ ($p = 2.14 \times 10^{-9}$), and the entire $\gamma = 0.0$ boundary in the continuous simplex sweep dominated all points with $\gamma > 0$ (peaking at $\text{MRR} = 0.6036$). Architecture status remains strictly **`UNFROZEN`**, and global primitive adjudication remains **`NOT_AUTHORIZED`**.
4. **R9 (Forward Constraints)**:
   Five operational negative constraints (`NC-71` through `NC-75`) are codified to govern future simulation phases: prohibiting cross-distribution min-max normalization, requiring reflection admission controls and candidate eligibility partitioning, banning hardcoded synthetic attribute constants, enforcing directional statistical interpretation, and mandating programmatic parameter verification.

---

# Section E: Reflection Mechanism Analysis (Requirement R5)

### 1. Empirical Phenomenon in Condition A8
Condition A8 was designed in `AS-03` to evaluate the impact of introducing synthesized reflection nodes into the memory store. It evaluated the full tri-factor scoring function ($\alpha = 0.2, \beta = 0.5, \gamma = 0.3$) across an augmented pool of 600 memories (500 base episodic memories + 100 synthesized reflection nodes) against the 100 standardized benchmark queries.

The observed telemetry in `exp_ab_01_comp_results.json` records catastrophic performance degradation:
- **Mean Reciprocal Rank (MRR)**: $0.0325 \pm 0.0101$ ($95\%\text{ CI}: [0.0305, 0.0345]$), representing a statistically significant collapse relative to A7 ($\Delta \text{MRR} = -0.0616, W = 146.0, p = 2.81 \times 10^{-16}$).
- **NDCG@5**: $0.0000 \pm 0.0000$ (zero ground-truth targets retrieved in top 5 across any query).
- **Temporal Inversion Rate**: $0.0\%$ (all top-5 positions occupied by reflections with identical or ordered timestamps).
- **False Retrieval Rate**: $1.0000$ ($100.0\%$).
- **Top-1 Reflection Crowding**: $100 / 100$ queries ($100.0\%$).
- **Queries with Reflection in Top-5**: $100 / 100$ queries ($100.0\%$).
- **Total Reflection Slots in Top-5**: $500 / 500$ slots ($100.0\%$).
- **Mean Target Memory Rank**: $34.04$ (Minimum rank: $21$, Maximum rank: $61$, Median: $32.0$). Ground-truth episodic targets were completely expelled from the top-20 retrieval positions across all 100 episodes.

### 2. Multi-Dimensional Component Audit: Reflection vs. Episodic Nodes

To isolate the causal mechanism behind this 100% crowding, we audited the distributions of all four scoring attributes across the 500 episodic records and 100 reflection records:

| Attribute Dimension | Episodic Nodes ($N=500$) | Reflection Nodes ($N=100$) | Mathematical Disparity / Mechanism |
|:---|:---|:---|:---|
| **Raw Importance ($s_{imp}$)** | Min: $4.0100$<br/>Max: $6.0000$<br/>Mean: $5.0029 \pm 0.5733$ | Min: $8.5000$<br/>Max: $8.5000$<br/>Mean: $8.5000 \pm 0.0000$ | **$+6.10\sigma$ Outlier Disparity**: Reflection importance was hardcoded to $8.5000$ in `run_exp_ab_01_comp.py:72`, exceeding the maximum episodic memory by $+2.5000$ points. |
| **Normalized Importance ($\hat{s}_{imp}$)** | Min: $0.0000$<br/>Max: $0.4432$<br/>Mean: $0.2211 \pm 0.1277$ | Min: $1.0000$<br/>Max: $1.0000$<br/>Mean: $1.0000 \pm 0.0000$ | **Min-Max Distortion**: Under pool min-max normalization, every reflection node receives $\hat{s}_{imp} = 1.0000$, whereas all episodic memories are compressed into $[0.0, 0.4432]$. |
| **Weighted Importance ($\gamma \hat{s}_{imp}$)** | Mean: $0.0663$<br/>Max: $0.1330$ | Constant: **$0.3000$** | **$+0.1670$ Unearned Advantage**: With $\gamma = 0.3$, reflection nodes receive an automatic, unearned floor advantage of $\ge +0.1670$ over every episodic candidate on a $[0, 1.0]$ score scale. |
| **Raw Recency ($s_{rec}$)** | Min: $0.6970$<br/>Max: $0.9964$<br/>Mean: $0.8379 \pm 0.0872$ | Min: $0.7072$<br/>Max: $0.9964$<br/>Mean: $0.8440 \pm 0.0877$ | **Timestamp Selection**: Each reflection node was assigned `latest_t = max(cluster)` (`run_exp_ab_01_comp.py:65`), conferring high recency. |
| **Cosine Similarity ($s_{rel}$)** | Min: $-0.2151$<br/>Max: $0.9991$<br/>Mean: $0.1820 \pm 0.3830$ | Min: $-0.1323$<br/>Max: $0.9948$<br/>Mean: $0.1876 \pm 0.3926$ | **Centroid Smoothing**: Reflection embeddings are normalized centroids of 5 episodic vectors (`run_exp_ab_01_comp.py:63-64`), yielding high semantic similarity across cluster queries. |
| **Candidate Eligibility** | Eligible for all 100 queries | Injected unconditionally into pool | **Zero Admission Control**: All 100 reflections were concatenated into `memories_a8` (`line 147`) without eligibility filters or relevance thresholds. |
| **Ground-Truth Targets** | 100 targets ($100\%$) | **0 targets ($0\%$)** | **Target Ineligibility**: Zero queries in `SimLab-MemBench-500` target reflection nodes. Retrieving a reflection is always scored as a failure. |

### 3. Evidentiary Logic Chain: How the Failure Unfolded
1. **Observation 1 (`run_exp_ab_01_comp.py:72`)**: The reflection generation loop hardcodes `'importance': 8.5` for all 100 reflection nodes.
2. **Observation 2 (`audit_distributions.py`)**: All 500 episodic memories in `SimLab-MemBench-500.json` have importance scores strictly between $4.01$ and $6.00$ (mean $5.0029$).
3. **Observation 3 (`run_exp_ab_01_comp.py:89`)**: Min-max normalization is performed across the concatenated pool ($N=600$):
   $$\text{norm\_imp}(x) = \frac{x - 4.01}{8.5 - 4.01} = \frac{x - 4.01}{4.49}$$
   This assigns $\text{norm\_imp} = 1.0000$ to all reflection nodes, while the highest possible episodic memory achieves only $(6.00 - 4.01) / 4.49 = 0.4432$.
4. **Observation 4 (`run_exp_ab_01_comp.py:92-95`)**: Under A8 weights ($\alpha=0.2, \beta=0.5, \gamma=0.3$), the importance component contributes $\gamma \cdot \text{norm\_imp} = 0.3 \times 1.0 = 0.3000$ to reflections, but at most $0.3 \times 0.4432 = 0.1330$ to episodic memories.
5. **Observation 5**: Even if an episodic memory has perfect cosine similarity ($s_{rel} = 1.0 \implies 0.5 \times 1.0 = 0.5000$) and perfect recency ($s_{rec} = 1.0 \implies 0.2 \times 1.0 = 0.2000$), its maximum possible score is $0.2000 + 0.5000 + 0.1330 = 0.8330$. Meanwhile, a reflection node matching the same topic needs only moderate relevance ($s_{rel} \ge 0.70$) and recent timestamp ($s_{rec} \ge 0.90$) to achieve $0.1800 + 0.3500 + 0.3000 = 0.8300$, easily outscoring almost all episodic memories. For query 0, reflection node `refl_0_19` achieved a total score of $0.9978$, whereas the best episodic memory was pushed to rank 11.
6. **Observation 6 (`run_exp_ab_01_comp.py:147`)**: Reflection nodes were injected into the general candidate pool without query-routing, admission gates, or type filters, while the benchmark queries exclusively target episodic memories.

### 4. Counterfactual Empirical Experiments

To rigorously disentangle the root cause, we executed three controlled counterfactual experiments on the exact benchmark dataset:

```text
+---------------------------------------------------------------------------------------------------------------+
|                                      COUNTERFACTUAL REFLECTION EXPERIMENTS                                    |
+---------------------------------------------------------------------------------------------------------------+
| Experiment Condition                      | Mean MRR | Top-1 Crowding | Top-5 Refl Slots | Target Rank (Mean) |
+---------------------------------------------------------------------------------------------------------------+
| Baseline A7 (Episodic Only, 500 mems)     |  0.0941  |      N/A       |       N/A        |        16.82       |
| Observed A8 (8.5 Imp, 600 mems)           |  0.0325  |  100/100 (100%)|  500/500 (100%)  |        34.04       |
| CF-1: Realistic Imp (imp = 5.0)           |  0.0929  |    0/100 (0.0%)|    0/500 (0.0%)  |        17.11       |
| CF-2: Zero Imp (alpha=0.3, beta=0.7, g=0) |  0.3536  |   76/100 (76%) |  208/500 (41.6%) |         7.84       |
| CF-3: Target Eligibility Overlap          |    N/A   |       N/A      |   0 / 100 (0.0%) |         N/A        |
+---------------------------------------------------------------------------------------------------------------+
```

- **Counterfactual 1 (Realistic Importance Calibration, `imp = 5.0`)**:
  When reflection importance was set to $5.0$ (matching the episodic distribution mean), Rank-1 reflection crowding dropped from $100\%$ to **$0.0\%$**, total reflection nodes in top-5 dropped from $500/500$ to **$0/500$**, and MRR recovered from $0.0325$ to **$0.0929$** (matching A7's $0.0941$).
- **Counterfactual 2 (Zero Importance Weighting, $\gamma = 0.0$)**:
  When importance was removed entirely ($\alpha=0.3, \beta=0.7, \gamma=0.0$), MRR rose to $0.3536$. However, $76\%$ Rank-1 crowding persisted because cluster centroid embeddings and max timestamps still gave reflections an unfair advantage on purely episodic queries in the absence of admission control.

### 5. Definitive Failure Classification

We evaluate the evidence against the five permitted classification categories:

1. **`REAL_PRIMITIVE_FAILURE` — FALSIFIED**:
   The failure is not inherent to the cognitive primitive of reflection. In Smallville (Park et al. 2023), reflections are higher-level thoughts scored dynamically by LLMs on a 1–10 scale and retrieved to answer synthetic questions. Counterfactual 1 proves that when reflection importance is calibrated to match the episodic scale, the catastrophic 100% crowding vanishes completely ($0/100$).
2. **`IMPLEMENTATION_DEFECT` — CONFIRMED (PRIMARY CLASSIFICATION)**:
   The primary root cause is an implementation defect in the execution harness (`run_exp_ab_01_comp.py:72`). The author arbitrarily hardcoded `'importance': 8.5` for synthetic reflection nodes, creating an out-of-distribution outlier ($+6.10\sigma$) relative to the benchmark's $[4.01, 6.00]$ episodic range. Furthermore, the implementation lacked basic admission control, concatenating reflections directly into an episodic-only retrieval pool without query eligibility filtering.
3. **`SCORING_SCALE_ARTIFACT` — SECONDARY CONTRIBUTORY MECHANISM**:
   Min-max normalization squashing episodic memories into $[0.0, 0.4432]$ was the mathematical mechanism through which the hardcoded defect expressed itself. However, min-max normalization did not create the outlier; the implementation defect created the outlier.
4. **`BENCHMARK_ARTIFACT` — SECONDARY CONTRIBUTORY FACTOR**:
   `SimLab-MemBench-500` is an episodic-only benchmark where $0/100$ queries target reflections. Dumping reflections into a benchmark where they are strictly ineligible as targets creates a structural penalty, though the 100% crowding was driven by the 8.5 scalar.
5. **`UNRESOLVED_MECHANISM` — FALSIFIED**:
   The causal mechanism is completely resolved and verified through reproducible counterfactual execution.

**Formal Determination**: **`IMPLEMENTATION_DEFECT`** (with `SCORING_SCALE_ARTIFACT` as its mathematical symptom and `BENCHMARK_ARTIFACT` as an uncalibrated evaluation confound).

---

# Section G: Phase 3 / Phase 4 Compatibility (Requirement R7)

### 1. The Apparent Contradiction
In Phase 3 RP-01 (`EXP-RP01-RECENCY-V1`), tuned tri-factor memory retrieval (`T-AltWeight`, $\alpha=0.3, \beta=0.5, \gamma=0.2$) was certified as a success:
$$\text{MRR} = 0.2403 \pm 0.3401, \quad \text{NDCG@5} = 0.2140 \pm 0.3724, \quad \Delta \text{MRR} = +0.1685 \text{ vs } B0\text{-Historical } (p < 0.001)$$
Primitive `PR-COG-01` was updated to `SUPPORTED_WITH_CONSTRAINTS` (`curo_phase3_execution_package.md:291`).

In Phase 4 EXP-AB-01-COMP, condition A7 (`FULL_TRI_FACTOR`), intended to represent the full tri-factor architecture, yielded:
$$\text{MRR} = 0.0941 \pm 0.0738, \quad \text{NDCG@5} = 0.0450 \pm 0.1363, \quad \text{False Retrieval Rate} = 100.0\%$$
This produced an apparent collapse of $-0.1462$ MRR between Phase 3 and Phase 4 on the identical benchmark dataset (`SimLab-MemBench-500`, SHA-256: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800`).

### 2. Systematic Audit of Potential Discrepancy Sources

We audited all four potential causes:
1. **Benchmark Regime Divergence**:
   - Both experiments executed against `E:\projects\simlab\phase3_execution\SimLab_MemBench_500.json`.
   - Verified SHA-256 digest: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800` in both Phase 3 (`PX-02:217`) and Phase 4 (`run_exp_ab_01_comp.py:22`).
   - Query count ($100$), memory count ($500$), query vectors, and ground truth target IDs are identical.
   - Result: **Zero Benchmark Divergence**.
2. **Retrieval Implementation Divergence**:
   - Both harnesses compute cosine similarity via dot product of unit-normalized embeddings.
   - Both compute recency via exponential decay: $s_{rec} = 0.995^{72.0 - t}$.
   - Both apply min-max normalization per query.
   - Result: **Zero Implementation Divergence**.
3. **Weight Regime Discrepancy**:
   - Phase 3 `T-AltWeight` weights (`PX-02:230`):
     $$\alpha = 0.3 \text{ (recency)}, \quad \beta = 0.5 \text{ (relevance)}, \quad \gamma = 0.2 \text{ (importance)}$$
   - Phase 4 `A7` weights (`AS-03:30`, `run_exp_ab_01_comp.py:160`):
     $$\alpha = 0.2 \text{ (recency)}, \quad \beta = 0.5 \text{ (relevance)}, \quad \gamma = 0.3 \text{ (importance)}$$
   - **Audit Discovery**: `AS-03_memory_ablation_plan.md:30` labeled A7 as the "Reconciled Phase 3 tuned weighting configuration," but swapped the recency and importance weights ($\alpha: 0.3 \to 0.2$, $\gamma: 0.2 \to 0.3$).

### 3. Simplex Sweep Proof of Exact Mathematical Replication
To verify whether Phase 4 replicates Phase 3 when executed at the identical weight coordinates, we queried the Phase 4 continuous 2D simplex sweep ($66$ points, step $0.1$) in `exp_ab_01_comp_results.json`:

```python
# Phase 4 Simplex Sweep Point: alpha=0.3, beta=0.5, gamma=0.2
{
  "alpha": 0.3,
  "beta": 0.5,
  "gamma": 0.2,
  "mrr_mean": 0.24028868538868536,
  "mrr_std": 0.34183802579945555,
  "ndcg5_mean": 0.21401588713748293
}
```

- **Phase 3 `T-AltWeight` MRR**: $0.2403 \pm 0.3401$, NDCG@5: $0.2140$
- **Phase 4 Simplex Point `(0.3, 0.5, 0.2)` MRR**: $0.240289$, NDCG@5: $0.214016$
- **Numerical Difference**: $< 0.00002$ (Exact match within rounding precision).

This proves conclusively that:
1. Phase 4 reproduces Phase 3 with **100% numerical fidelity**.
2. There is **zero data corruption, zero code breakage, and zero benchmark divergence**.
3. The collapse of condition A7 was caused entirely by shifting from $(\alpha=0.3, \beta=0.5, \gamma=0.2)$ to $(\alpha=0.2, \beta=0.5, \gamma=0.3)$.

### 4. Why Shifting Gamma from 0.2 to 0.3 Collapses Retrieval
As audited in `audit_importance_bias.py`:
- In `SimLab-MemBench-500`, importance scores are non-discriminative noise with respect to query intent: on average, **$188.4$ out of $500$ memories ($37.7\%$)** have higher importance than the ground truth target.
- Pure importance retrieval ($A3$, $\gamma=1.0$) yields $\text{MRR} = 0.0086$ (near zero).
- At $\gamma = 0.2$ and $\alpha = 0.3$, relevance and recency are strong enough to maintain $\text{MRR} = 0.2403$.
- When $\gamma$ is raised to $0.3$ and $\alpha$ is reduced to $0.2$, importance noise crosses the tipping point where distractors overwhelm the target, collapsing MRR to $0.0941$.

### 5. Epistemic Reconciliation & Conflict Determination
- **Is `PHASE3_PHASE4_EVIDENCE_CONFLICT` required?**
  **NO**, a formal data conflict record is **NOT WARRANTED**. The experimental data across Phase 3 and Phase 4 is completely consistent, verified by the exact match of point $(0.3, 0.5, 0.2)$.
- **Epistemic Update**:
  While the numbers are consistent, the **interpretation** of the primitive is fundamentally updated:
  - Phase 3 established that tuned tri-factor $(0.3, 0.5, 0.2)$ outperformed equal weights $(1, 1, 1)$, but Phase 3 never ablated importance ($\gamma = 0$).
  - Phase 4 performed that ablation: removing importance ($A4$, $\alpha=0.3, \beta=0.7, \gamma=0.0$) surged MRR to **$0.5002$**, and the simplex sweep revealed the global optimum at $(\alpha=0.7, \beta=0.3, \gamma=0.0)$ with $\text{MRR} = \mathbf{0.6036}$.
  - Therefore, the $0.2403$ MRR achieved in Phase 3 was not aided by importance; it was held back by importance.

---

# Section H: PR-COG-01 Evidence Update (Requirement R8)

### 1. Governance Scope & Authority Boundary
In strict accordance with Curo SimLab lifecycle governance (`AS-18_primitive_advancement_contract.md` and Phase 4 execution constraints):
- **Criterion B (`ABLATION_EVIDENCE`) ONLY** is updated in this evaluation.
- Criteria A, C, D, E, F, and G are **NOT** adjudicated here.
- Global primitive adjudication is strictly **NOT_AUTHORIZED** (reserved for `GATE_R4`).
- SimLab Implementation Authority remains strictly **`NOT_GRANTED`**.
- Architecture Status remains strictly **`UNFROZEN`**.

### 2. Formal Evaluation of Criterion B (Ablation Evidence)

According to `AS-18:36-39`:
> **Criterion B: Ablation Evidence**  
> *Requirement*: The component claimed to matter must demonstrate a statistically significant, measurable contribution relative to a valid, compute-matched control ($\Delta > 0, p < \alpha$).  
> *Falsification Standard*: If ablating the component produces negligible difference ($\Delta \le \text{margin}$) or if performance is driven entirely by a confounding factor, the primitive's standalone causal claim is falsified.

#### Empirical Ablation Evidence from EXP-AB-01-COMP:
1. **Direct Component Comparison (A4 vs. A7)**:
   - Condition A7 (Full Tri-Factor: Recency + Relevance + Importance): $\text{MRR} = 0.0941 \pm 0.0738$.
   - Condition A4 (Ablated: Recency + Relevance Only, $\gamma=0.0$): $\text{MRR} = 0.5002 \pm 0.4481$.
   - Observed Delta: $\Delta \text{MRR}_{A4 - A7} = \mathbf{+0.4061}$ ($95\%\text{ CI}: [+0.3209, +0.4913]$).
   - Paired Wilcoxon Test: $W = 784.0, p = 2.1356 \times 10^{-9}$ (Statistically significant at Bonferroni-corrected $\alpha = 0.0014$).
   - Cohen's $d$: $+0.9342$ (Very large effect size in favor of ablated condition).
2. **Hypothesis Testing Outcomes**:
   - Preregistered Null Hypothesis $H_0$ ("Importance is strictly necessary: $\text{MRR}_{A7} - \text{MRR}_{A4} \ge +0.05$"): **REJECTED** ($p = 2.14 \times 10^{-9}$).
   - Preregistered Non-Inferiority Hypothesis $H_1$ ("A4 is non-inferior to A7 within $\Delta \le 0.02$"): **CONFIRMED** (A4 is vastly superior by $+0.4061$).
3. **Simplex Sweep Evidence**:
   - Across all 66 points on the weighting simplex, every point on the $\gamma = 0.0$ boundary outperformed internal points with $\gamma > 0$.
   - Global maximum: $\alpha=0.7, \beta=0.3, \gamma=0.0$ ($\text{MRR} = 0.6036$).
   - Global minimum: $\alpha=0.0, \beta=0.0, \gamma=1.0$ ($\text{MRR} = 0.0086$).
4. **Reflection Component Ablation (A8)**:
   - Condition A8 ($\text{MRR} = 0.0325$) suffered 100% Rank-1 crowding due to an implementation defect.

### 3. Criterion B Status Determination

Evaluating the permitted status values:
- `SUPPORTED`: **REJECTED**. The claimed component (prompt-based importance) does not demonstrate $\Delta > 0$.
- `SUPPORTED_WITH_CONSTRAINTS`: **REJECTED**. Importance is not supported even with constraints; it is actively detrimental.
- `MECHANISTIC_FAILURE_UNDER_INVESTIGATION`: Applicable to A8 reflection implementation, but the core ablation of importance is fully resolved.
- `EVIDENCE_CONFLICT`: **REJECTED**. Phase 3 and Phase 4 are mathematically congruent.
- **`COMPONENT_NOT_NECESSARY_UNDER_TESTED_CONDITIONS` — CONFIRMED**:
  The empirical ablation evidence conclusively falsifies the necessity of prompt-based importance scoring for offline episodic memory retrieval. Removing importance scores yields a $+0.4061$ MRR improvement ($+431\%$ relative gain).

```text
================================================================================
CRITERION B (ABLATION_EVIDENCE) FORMAL STATUS UPDATE:
Primitive: PR-COG-01 (Generative Agent Memory Stream / Retrieval Scoring)
Evaluated Component: Prompt-Based Importance Scoring (gamma * s_imp)
Updated Status: COMPONENT_NOT_NECESSARY_UNDER_TESTED_CONDITIONS
Causal Claim Bound: Under standardized offline episodic memory retrieval (SimLab-MemBench-500),
eliminating prompt-based importance scores causes no degradation in retrieval precision (MRR),
and significantly improves ranking quality by removing non-discriminative salience noise.
Architecture Status: STRICTLY UNFROZEN
================================================================================
```

---

# Section I: Lessons Learned / Forward Constraints (Requirement R9)

In accordance with Phase 4 governance (`AS-16_lessons_learned_forward_constraints.md`), the audit team codifies five new, binding operational negative constraints (`NC-71` through `NC-75`):

### `NC-71`: NO Cross-Distribution Min-Max Normalization Across Disparate Memory Classes
- **Violation Observed**: In `run_exp_ab_01_comp.py:89`, min-max normalization was computed globally across a concatenated pool of 500 episodic memories ($s_{imp} \in [4.01, 6.00]$) and 100 reflection nodes ($s_{imp} = 8.50$). This artificially compressed all episodic memory scores into $[0.0, 0.4432]$ while granting reflections $1.0000$.
- **Binding Forward Constraint**: Execution harnesses and production retrieval pipelines must **NEVER** apply naive global min-max normalization across heterogeneous memory record types (e.g. episodic events, synthesized reflections, agent profile facts) or across features containing artificial constants. Implementers must apply either: (a) separate per-class normalization prior to fusion, (b) robust rank-based normalization (quantile transformation), or (c) standardized z-score scaling with distribution trimming.

### `NC-72`: NO Unconditional Reflection Pool Injection Without Admission Controls
- **Violation Observed**: In `run_exp_ab_01_comp.py:147`, 100 synthesized reflection nodes were injected unconditionally into the retrieval candidate pool for 100 queries that exclusively sought episodic ground-truth facts, resulting in 100% Rank-1 crowding and 500/500 top-five slot saturation.
- **Binding Forward Constraint**: Synthesized reflection nodes, abstract summaries, and high-level agent thoughts must **NEVER** be injected unconditionally into general memory retrieval candidate pools. Future simulation harnesses must implement explicit **reflection admission controls**:
  1. *Query Intent Gating*: Directing episodic queries ("When did X happen?") strictly to episodic memory streams, reserving reflection nodes for synthetic, thematic, or planning queries ("What is Klaus's opinion of Y?").
  2. *Retrieval Capacity Quotas*: Enforcing a maximum reflection quota in retrieved contexts (e.g. at most 1 reflection slot in top-5).
  3. *Tiered Candidate Eligibility*: Requiring reflection nodes to pass an elevated relevance threshold before entering candidate consideration.

### `NC-73`: NO Hardcoded Synthetic Node Attribute Constants in Experiment Harnesses
- **Violation Observed**: In `run_exp_ab_01_comp.py:72`, the harness implementer hardcoded `'importance': 8.5` for all reflection nodes, creating a $+6.10\sigma$ outlier relative to the benchmark episodic memories.
- **Binding Forward Constraint**: Micro-benchmark and ablation harnesses must **NEVER** hardcode static attribute constants for synthetic or composite cognitive entities. Any generated reflection, summary, or plan node must either:
  1. Inherit statistical properties dynamically from its constituent source nodes (e.g. cluster mean or median importance); OR
  2. Be scored dynamically through the identical calibrated prompt pipeline and temperature settings used to score primary records.

### `NC-74`: Mandatory Directional Statistical Interpretation Discipline
- **Violation Observed**: A simplistic statistical check might observe that the difference between A4 and A7 has a minuscule p-value ($p = 2.14 \times 10^{-9}$) and erroneously conclude that "the null hypothesis was rejected, proving that importance has a significant effect." In reality, A4 *outperformed* A7 by $+0.4061$ MRR; the component's effect was overwhelmingly *harmful*.
- **Binding Forward Constraint**: Evaluators must **NEVER** infer confirmation of an architectural necessity hypothesis or reject non-inferiority based solely on a two-sided test yielding $p < \alpha$. Every reporting agent must explicitly decompose statistical findings into:
  1. Effect Direction (Treatment $>$ Control vs. Treatment $<$ Control);
  2. Effect Magnitude (Absolute $\Delta$ and Cohen's $d$);
  3. One-Sided Confidence Intervals against the preregistered margin;
  4. Falsification Sign: A statistically significant negative contribution ($\Delta < 0, p < \alpha$) must be formally logged as empirical falsification of component necessity, not as generic "significance."

### `NC-75`: Programmatic Configuration-to-Specification Parameter Provenance
- **Violation Observed**: In `AS-03:30`, condition A7 was mislabeled as the "Reconciled Phase 3 tuned weighting configuration" while specifying weights $(0.2, 0.5, 0.3)$ instead of Phase 3's $(0.3, 0.5, 0.2)$, causing an apparent collapse from $0.2403$ to $0.0941$.
- **Binding Forward Constraint**: Every execution harness must programmatically validate that executed parameter configurations match the frozen design specification and flag any divergence from upstream phase configurations. Cross-phase comparative conditions must assert parameter identity in preflight checks (`assert executed_weights == phase3_reference_weights`) before launch.

---

## Summary Table of Audit Deliverable Cross-References

| Section | Audit Topic | Primary Finding | Reference Documents |
|:---|:---|:---|:---|
| **Section E** | Reflection Mechanism Analysis | Classified as **`IMPLEMENTATION_DEFECT`** (`run_exp_ab_01_comp.py:72`, hardcoded `8.5` importance). Proven by Counterfactual 1 (MRR restored to 0.0929, 0% crowding). | `audit_reflection_mechanics.py`, `audit_reflection_deep.py` |
| **Section G** | Phase 3 / 4 Compatibility | **`DIFFERENT_WEIGHT_REGIME`** ($(0.2, 0.5, 0.3)$ vs $(0.3, 0.5, 0.2)$). Simplex point $(0.3, 0.5, 0.2)$ replicates Phase 3 exactly ($0.2403$). Formal data conflict rejected. | `curo_phase3_execution_package.md:230`, `exp_ab_01_comp_results.json` |
| **Section H** | PR-COG-01 Evidence Update | Criterion B updated to **`COMPONENT_NOT_NECESSARY_UNDER_TESTED_CONDITIONS`** ($A4$ outperforms $A7$ by $+0.4061$). Architecture remains strictly **`UNFROZEN`**. | `AS-18:36`, `AS-03:49` |
| **Section I** | Forward Constraints | Codified **`NC-71`** (Normalization), **`NC-72`** (Reflection Admission), **`NC-73`** (Synthetic Constants), **`NC-74`** (Directional Testing), **`NC-75`** (Weight Provenance). | `AS-16:85` |
