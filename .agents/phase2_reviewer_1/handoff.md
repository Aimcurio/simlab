# Phase 2 Reviewer 1: Independent Methodological & Statistical Review Report

**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Lifecycle State**: `GATE_R1_COMPLETE -> REPRODUCTION_DESIGN_AUTHORIZED`  
**Reviewer**: Phase 2 Reviewer 1 (`teamwork_preview_reviewer`)  
**Working Directory**: `E:\projects\simlab\.agents\phase2_reviewer_1`  
**Date**: 2026-09-16T09:45:00Z  
**Canonical Scope**: `RD-01`, `RD-02`, `RD-03`, `RD-04`, `RD-05`, `RD-06`, `RD-07`, `RD-08`, `RD-09`, `RD-10`, `RD-12`  

---

# Executive Summary & Formal Verdict

**VERDICT**: **`REQUEST_CHANGES`**

### Summary of Review
The Phase 2 reproduction design suite (`RD-01` through `RD-12`) represents a major methodological advance over published multi-agent literature:
- It strictly adheres to the **Minimum Experiment Principle** (testing isolated mechanisms via micro-harnesses rather than building monolithic simulation engines).
- It enforces a **Deterministic-First Measurement Hierarchy** (Levels 1 and 2 prioritized over subjective LLM judges).
- It completely populates the **35-field Experiment Specification Record schema** across all four candidates (`RP-01` to `RP-04`) with zero placeholder tokens (`TODO`, `TBD`, `PLACEHOLDER`).
- It firmly maintains the Curo governance firewall (`ARCHITECTURE_STATUS = UNFROZEN`, `IMPLEMENTATION_AUTHORITY = NOT_GRANTED`, `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`).

However, **adversarial stress-testing and statistical verification have revealed two Critical/Major methodological contradictions and three Major statistical flaws** that will cause experimental invalidity or false-negative results if executed as written:
1. **Mathematical Incompatibility in Compute Matching (RP-02)**: The simultaneous requirement of $K=6$ inference calls AND $\pm 10\%$ token parity between 3-agent 2-round debate and single-agent Self-Consistency ($B_{1-SC}$) is mathematically impossible. Multi-round debate accumulates conversational history, resulting in a $+50.0\%$ token inflation over single-turn $B_{1-SC}$ ($K=6$).
2. **Even $K=6$ Majority Tie Instability (RP-02)**: Configured with even $K=6$, $B_{1-SC}$ experiences a $18.5\%$ to $31.3\%$ tie probability under majority voting, which introduces arbitrary variance in the absence of a pre-registered tie-breaking protocol.
3. **Statistical Power Collapse on GSM8K Equivalence ($N=100$, RP-02)**: The two-sided equivalence margin of $\pm 3\%$ ($\delta = 0.03$) on $N=100$ GSM8K tasks has **$0.0\%$ statistical power** under TOST; the 90% confidence interval half-width ($\pm 6.4\%$) is more than double the margin.
4. **Inappropriate Test Specifications on Matched Binary Data (RP-02, RP-04)**: Applying standard linear Two-Way ANOVA (RP-02) and standard Pearson Chi-square (RP-04) to paired binary outcomes violates normality, homoscedasticity, and sample independence.
5. **Cost Arithmetic Undercount (RD-12)**: Total API expenditure is understated by $\approx 21\%$ ($\$43.20$ actual vs $\$34.50$ stated for RP-02; $\$63.50$ total vs $\$52.25$ stated).

These issues must be resolved before Gate R2 can be approved for execution readiness.

---

# Component 1: Observations

Direct verbatim observations from the reviewed deliverables:

1. **Token Parity vs. Call Parity Invariant (`RD-04:31-33`, `RD-06:52-53`)**:
   - `RD-04:31-33`:
     > $$\text{Tokens}(B_{1-SC}) \approx \text{Tokens}(T_{MA}) \quad \pm 10\%$$
     > $$\text{Inference Calls}(B_{1-SC}) \approx \text{Inference Calls}(T_{MA}) \quad \pm 10\%$$
   - `RD-06:52-53`:
     > `- Total inference calls normalized: B1-SC (K=6 calls) vs T-Debate (3 agents x 2 rounds = 6 calls).`  
     > `- Total token expenditure window constrained to ±10%.`
   - `RD-06:33`:
     > `Baseline B1-SC (Compute-Matched Control): Single-agent Self-Consistency with K independent reasoning samples (T=0.7) where K exactly matches the total inference calls of the multi-agent debate treatment, aggregated via majority voting.`

2. **Equivalence Hypothesis & Sample Allocation on GSM8K (`RD-06:20`, `RD-06:71`)**:
   - `RD-06:20`:
     > `Conversely, on closed-domain symbolic reasoning (GSM8K/MATH), compute-matched B1-SC will equal or exceed multi-agent debate accuracy within a ±3% margin.`
   - `RD-06:71`:
     > `100 problems from GSM8K (Closed Symbolic Reasoning).`
   - `RD-06:86`:
     > `Confirmation of hypothesis that T-Debate provides <= 2% advantage on GSM8K under matched compute.`

3. **Statistical Test Specifications (`RD-06:80`, `RD-07:75`, `RD-08:79`)**:
   - `RD-06:80`:
     > `Two-way ANOVA evaluating interaction effect between Architecture Condition and Task Category.`
   - `RD-07:75`:
     > `Paired t-test or Wilcoxon signed-rank test on token consumption and test pass rates.`
   - `RD-08:79-80`:
     > `One-way ANOVA with Tukey HSD post-hoc test on token consumption.`  
     > `Chi-square test on task accuracy proportions.`

4. **Resource Consumption Modeling (`RD-12:17`, `RD-12:22`)**:
   - `RD-12:17`:
     > `EXP-RP02-COMPUTE-MATCHED | 3 conditions | N=400 | Total 1,200 episodes | 6 calls/ep | 7,200 calls | 800 / 400 avg tokens | 8,640,000 tokens | Est. Cost: $34.50`
   - `RD-12:22`:
     > `Cost Basis: Standard commercial API pricing for gpt-4o-2024-08-06 ($2.50 / 1M prompt, $10.00 / 1M completion)`

5. **Deterministic Measurement Hierarchy (`RD-09:12-21`)**:
   - `RD-09:16-19`:
     > `Level 1: Deterministic Truth | Unit test pass, exact match, regex assertions, syntax validity`  
     > `Level 2: Algorithmic Ranking | MRR, NDCG@K, recall@K, precision@K, edit distance, AST equivalence`  
     > `Level 3: System Telemetry | Token count, inference call count, wall latency, memory usage`  
     > `Level 4: Auxiliary LLM Judge | Permitted ONLY as secondary analysis with multi-judge consensus`

6. **35-Field Schema Completeness**:
   - `RD-05` (RP-01): 35 numbered section headers present (`1. experiment_id` through `35. execution_authority`). Zero placeholder strings.
   - `RD-06` (RP-02): 35 numbered section headers present. Zero placeholder strings.
   - `RD-07` (RP-03): 35 numbered section headers present. Zero placeholder strings.
   - `RD-08` (RP-04): 35 numbered section headers present. Zero placeholder strings.

---

# Component 2: Logic Chain

### Step 1: Token Parity Impossibility Proof in RP-02
- **From Observation 1**: In `EXP-RP02`, Treatment $T_{Debate}$ comprises 3 agents over 2 rounds.
  - Round 1: 3 agents each receive base prompt $C_0$ and generate output $L$. Input tokens = $3 C_0$; output tokens = $3 L$.
  - Round 2: 3 agents each receive base prompt $C_0$ plus all 3 prior outputs ($3 L$). Input tokens = $3(C_0 + 3L) = 3 C_0 + 9 L$; output tokens = $3 L$.
  - Total $T_{Debate}$ tokens = $(3 C_0 + 3 L) + (3 C_0 + 9 L + 3 L) = 6 C_0 + 15 L$.
- In $B_{1-SC}$ with $K=6$:
  - 6 independent CoT calls each receive base prompt $C_0$ and generate output $L$.
  - Total $B_{1-SC}$ tokens = $6(C_0 + L) = 6 C_0 + 6 L$.
- For $T_{Debate}$ to satisfy the $\pm 10\%$ token parity rule ($\text{Tokens}(T_{Debate}) \le 1.10 \times \text{Tokens}(B_{1-SC})$):
  $$6 C_0 + 15 L \le 1.10(6 C_0 + 6 L) = 6.6 C_0 + 6.6 L \implies 8.4 L \le 0.6 C_0 \implies L \le \frac{0.6}{8.4} C_0 = \frac{C_0}{14}$$
- **From Observation 4**: In `RD-12`, budgeted parameters are $C_0 = 800$ prompt tokens and $L = 400$ completion tokens.
  - Here, $\frac{C_0}{14} = \frac{800}{14} \approx 57.1$ tokens. But actual $L = 400 \gg 57.1$.
  - Total $T_{Debate}$ tokens = $6(800) + 15(400) = 4,800 + 6,000 = 10,800$ tokens.
  - Total $B_{1-SC}$ tokens = $6(800 + 400) = 7,200$ tokens.
  - Ratio = $\frac{10,800}{7,200} = 1.500$ (**Debate consumes $+50.0\%$ more tokens**).
- **Conclusion**: It is mathematically impossible to maintain $K=6$ inference call parity AND $\pm 10\%$ token parity simultaneously under realistic generation lengths. This directly violates the core compute-matching invariant of `RD-04`.

### Step 2: Proof of Tie Probability under Even $K=6$ Sampling
- **From Observation 1**: $B_{1-SC}$ evaluates $K=6$ independent samples with majority voting over binary answers.
- For a problem with ground-truth correctness probability $p$, an exact 3-3 tie occurs with probability:
  $$P(\text{Tie}) = \binom{6}{3} p^3 (1-p)^3 = 20 \cdot p^3 (1-p)^3$$
  - At $p = 0.50$: $P(\text{Tie}) = 20 \cdot (0.125)(0.125) = 0.3125$ ($31.25\%$).
  - At $p = 0.60$: $P(\text{Tie}) = 20 \cdot (0.216)(0.064) = 0.2765$ ($27.65\%$).
  - At $p = 0.70$: $P(\text{Tie}) = 20 \cdot (0.343)(0.027) = 0.1852$ ($18.52\%$).
- In almost 1 out of 4 to 1 out of 3 instances, majority voting will deadlock.
- `RD-06` lacks any tie-breaking specification. If broken by random coin flip, noise is injected; if broken by first sample, order bias is injected.
- Odd sample sizes ($K=5, 7, 9$) have zero probability of binary ties.

### Step 3: Statistical Power Derivation for TOST Equivalence on GSM8K ($N=100$)
- **From Observation 2**: `RD-06` hypothesizes that $B_{1-SC}$ equals multi-agent debate within $\pm 3\%$ ($\delta = 0.03$) on $N=100$ GSM8K problems.
- To prove equivalence in a Two One-Sided Tests (TOST) framework at $\alpha = 0.05$, the two-sided $90\%$ confidence interval for the paired difference $\Delta = p_{debate} - p_{B1-SC}$ must lie entirely within $[-\delta, +\delta] = [-0.03, +0.03]$.
- Let $d_i \in \{-1, 0, 1\}$ be the paired accuracy difference for problem $i$. Under $H_0$ (true $\Delta = 0$), the variance of differences is determined by the discordance rate $p_{disc} = P(y_{debate} \neq y_{B1-SC})$.
- On reasoning benchmarks, empirical discordance between debate and CoT is typically $p_{disc} \in [0.10, 0.20]$.
- Standard error of the mean difference is $SE = \sqrt{\frac{p_{disc}}{N}}$.
  - For $p_{disc} = 0.15$ and $N = 100$: $SE = \sqrt{\frac{0.15}{100}} = 0.03873$.
  - The $90\%$ confidence interval half-width is $z_{0.95} \times SE = 1.6449 \times 0.03873 = \mathbf{0.0637}$ ($\mathbf{\pm 6.37\%}$).
- Since the half-width ($6.37\%$) exceeds the target margin ($3.0\%$), the confidence interval width is $12.74\% > 6.00\%$.
- **Conclusion**: The empirical statistical power to confirm equivalence within $\pm 3\%$ with $N=100$ is **$0.0\%$**. A true equivalent result will be falsely rejected as non-equivalent 100% of the time. To achieve $\ge 80\%$ power with $p_{disc} = 0.15$, the minimum required sample size is:
  $$N \ge \left(\frac{z_{0.95} + z_{0.80}}{\delta}\right)^2 p_{disc} = \left(\frac{1.6449 + 0.8416}{0.03}\right)^2 (0.15) \approx \mathbf{1,030 \text{ tasks}}$$

### Step 4: Verification of Statistical Test Models
- **From Observation 3**:
  - `RD-06` specifies Two-Way ANOVA for Task Accuracy across Architecture Condition and Task Category. Task accuracy is a binary indicator $Y \in \{0, 1\}$. Linear ANOVA assumes normally distributed, homoscedastic errors. Applying it to binary repeated measures produces biased $F$-tests and out-of-bounds predicted probabilities. The appropriate model is a **Generalized Linear Mixed Model (GLMM) with a logit link function** (as specified in Phase 1 DR-12 section 2.1).
  - `RD-08` specifies a standard Pearson Chi-square test for task accuracy across 4 conditions on `SimLab-HeteroBench-100`. Because all 4 conditions evaluate the *exact same 100 tasks*, the observations are matched/paired. Pearson Chi-square assumes independent samples, which deflates standard errors and yields invalid $p$-values. The appropriate non-parametric test for binary data across $k > 2$ matched blocks is **Cochran's Q test**, followed by post-hoc pairwise McNemar tests with Bonferroni correction.

### Step 5: Cost Modeling Verification
- **From Observation 4**:
  - Pricing: $\$2.50 / \text{M prompt tokens}$, $\$10.00 / \text{M completion tokens}$.
  - EXP-RP02: 7,200 calls $\times$ 800 prompt = 5.76M tokens $\to 5.76 \times \$2.50 = \$14.40$.
  - EXP-RP02: 7,200 calls $\times$ 400 completion = 2.88M tokens $\to 2.88 \times \$10.00 = \$28.80$.
  - True EXP-RP02 Cost = $\$14.40 + \$28.80 = \mathbf{\$43.20}$.
  - Reported cost in `RD-12` is $\mathbf{\$34.50}$ (understated by $\$8.70$, or $25.2\%$).
  - Similarly, EXP-RP03 true cost is $\$4.50 + \$9.00 = \$13.50$ (reported as $\$12.20$).
  - Total true suite cost = $\mathbf{\$63.50}$ (reported as $\$52.25$).

---

# Component 3: Caveats

1. **Safety Margin on Budget**: Although the true cost ($\$63.50$) is higher than reported ($\$52.25$), it remains comfortably below the $\$75.00$ auto-abort limit and $\$100.00$ hard budget ceiling in `RD-12`. This is an arithmetic modeling defect, not an operational solvency risk.
2. **Deterministic Primitives are Sound**: `RP-01` (Smallville Memory Recency Decay) is methodologically outstanding. It uses zero LLM calls during retrieval, features a deterministic 500-query benchmark, and uses appropriate paired non-parametric tests (Wilcoxon signed-rank with Bonferroni correction).
3. **Execution Isolation & Governance**: `RD-10`, `RD-13`, and `RD-15` provide exemplary provenance, telemetry schemas, and hermetic container isolation plans.

---

# Component 4: Findings & Adversarial Challenges

## Methodological & Statistical Findings

### Finding 1 [CRITICAL] — Mathematical Incompatibility in Compute Matching (RP-02)
- **Where**: `RD-04:31-33`, `RD-06:33`, `RD-06:52-53`.
- **Why**: Multi-agent debate accumulates prior conversational turns in round 2 prompts, causing a $+50.0\%$ token inflation ($10,800$ tokens vs $7,200$ tokens) over single-turn $B_{1-SC}$ ($K=6$). Demanding both $K=6$ calls AND $\pm 10\%$ token parity is mathematically impossible.
- **Remediation**: Split the baseline control in `RD-04` and `RD-06` into a **Dual-Control Protocol**:
  1. **$B_{1-SC-calls}$ ($K=6$)**: Inference-call-matched control ($6$ calls, unpadded prompts).
  2. **$B_{1-SC-tokens}$ ($K=9$)**: Token-matched control ($9$ calls, equalizing total token budget within $\pm 5\%$).
  This allows researchers to determine whether debate gains stem from multi-agent interaction or simply from higher total token spend.

### Finding 2 [MAJOR] — Even $K=6$ Majority Tie Deadlock (RP-02)
- **Where**: `RD-06:33`, `RD-06:52`.
- **Why**: An even number of samples ($K=6$) produces an exact 3-3 tie in $18.5\%$ to $31.3\%$ of binary tasks. In the absence of an explicit tie-breaking rule, non-deterministic or biased voting occurs.
- **Remediation**: Set $K=7$ for call matching or $K=9$ for token matching. If $K=6$ is retained, pre-register a deterministic tie-breaker (e.g. highest average log-probability or a compute-matched single-turn verifier prompt).

### Finding 3 [MAJOR] — Zero Statistical Power for GSM8K Equivalence Margin (RP-02)
- **Where**: `RD-03:26`, `RD-06:20`, `RD-06:70-71`.
- **Why**: Demonstrating equivalence within $\pm 3\%$ ($\delta = 0.03$) on $N=100$ tasks has **$0.0\%$ power** under TOST because the $90\%$ CI half-width ($\pm 6.4\%$) is more than double the margin.
- **Remediation**:
  - Option A (Recommended): Expand the GSM8K test set from $N=100$ to $N=500$ problems, and set the equivalence margin to $\delta = 0.05$ (5 percentage points), achieving power $\ge 85\%$.
  - Option B: Reframe the hypothesis from two-sided equivalence to non-inferiority ($B_{1-SC} \ge T_{Debate} - 0.05$).

### Finding 4 [MAJOR] — Inappropriate Statistical Tests for Repeated Binary Outcomes (RP-02, RP-04)
- **Where**: `RD-06:80`, `RD-08:79`.
- **Why**: Linear Two-Way ANOVA (RP-02) and standard Pearson Chi-square (RP-04) violate normality, homoscedasticity, and independence on repeated-measures binary benchmark data.
- **Remediation**:
  - In `RD-06`: Replace Two-Way ANOVA with a **Generalized Linear Mixed Model (GLMM) with a logit link function** (`lme4::glmer` or `statsmodels.Binomial`), specifying random intercepts for problem instances.
  - In `RD-08`: Replace Pearson Chi-square with **Cochran's Q test** across the 4 matched conditions, followed by pairwise McNemar tests with Bonferroni correction ($\alpha = 0.01 / 6 = 0.00167$).

### Finding 5 [MINOR] — API Cost Understatement in RD-12
- **Where**: `RD-12:17`, `RD-12:20`.
- **Why**: Arithmetic undercount of completion tokens at $\$10.00/\text{M}$ results in $\$34.50$ stated vs $\$43.20$ actual for RP-02, and $\$52.25$ stated vs $\$63.50$ actual overall.
- **Remediation**: Update `RD-12` budget table with corrected calculations ($5.76\text{M} \times \$2.50 + 2.88\text{M} \times \$10.00 = \$43.20$).

### Finding 6 [MINOR] — Unmapped Inconclusive "Dead Zones" in Falsification Thresholds
- **Where**: `RD-03`, `RD-05:80-88`, `RD-06:84-91`, `RD-07:79-86`, `RD-08:83-90`.
- **Why**: Gaps exist between success and failure thresholds (e.g. RP-01: $\Delta \text{MRR} \in [+0.05, +0.15]$; RP-03: token reduction $\in [10\%, 25\%]$).
- **Remediation**: Codify an explicit `INCONCLUSIVE_SUB_THRESHOLD` outcome state mapping to baseline retention under the Minimum Experiment Principle.

---

# Verification Checklist Audit

| Item | Requirement | Verification Finding | Status |
|---|---|---|---|
| **1. Compute-Matched Baselines** | B0 to B4 defined; B1-SC matching with $K=6$, $\pm 10\%$ token parity | Hierarchy defined, but $K=6$ calls and $\pm 10\%$ token parity are mathematically incompatible in RP-02 (+50% token inflation in debate). Even $K=6$ causes ties. | **FAILED** (Finding 1, 2) |
| **2. Statistical Testing Framework** | Non-parametric tests, corrections, effect sizes, power | RP-01 is sound (Wilcoxon + Bonferroni). RP-02 misapplies ANOVA and has 0% TOST power on GSM8K. RP-04 misapplies Pearson Chi-square to matched blocks. | **FAILED** (Finding 3, 4) |
| **3. Deterministic Measurement Hierarchy** | Level 1/2 priority over subjective LLM judges | 100% compliant. Levels 1/2 prioritized across all 4 experiments; zero primary LLM judging. | **PASSED** |
| **4. Minimum Experiment Principle** | Isolated micro-harnesses, zero full simulation rebuilds | 100% compliant. RP-01 to RP-04 isolate primitives into minimal benchmarks without simulation rebuilds. | **PASSED** |
| **5. 35-Field Schema Completeness** | All 35 fields populated; zero placeholders | 100% compliant. All 35 fields present in RD-05, RD-06, RD-07, RD-08 without TODO/TBD tokens. | **PASSED** |

---

# Component 5: Verification Method

To independently verify the observations and mathematical findings in this report:

1. **Verify Token Parity Incompatibility (Finding 1)**:
   - Run Python derivation:
     ```python
     C0, L = 800, 400
     b1sc_tokens = 6 * (C0 + L) # 7,200
     debate_tokens = 6 * C0 + 15 * L # 10,800
     ratio = debate_tokens / b1sc_tokens # 1.50 (+50.0%)
     assert ratio > 1.10, "Violates +-10% token parity"
     ```
2. **Verify Even $K=6$ Tie Probability (Finding 2)**:
   - Run SciPy binomial calculation:
     ```python
     from scipy.stats import binom
     p_tie = binom.pmf(3, 6, 0.60) # 0.27648 (27.65%)
     ```
3. **Verify TOST Power Collapse on GSM8K (Finding 3)**:
   - Run Two One-Sided Tests confidence interval check:
     ```python
     import math
     N, p_disc, delta = 100, 0.15, 0.03
     se = math.sqrt(p_disc / N)
     ci_half_width = 1.644853 * se # 0.0637 (6.37%)
     assert ci_half_width > delta, "90% CI cannot fit in [-0.03, +0.03]"
     ```
4. **Inspect Files for Schema & Hierarchy Compliance**:
   - `RD-05:10-131`, `RD-06:10-134`, `RD-07:10-128`, `RD-08:10-132` (Verify 35 fields).
   - `RD-09:12-21` (Verify Level 1-4 hierarchy).

---

# Final Recommendation

The design package must be returned for revision with the following action items:
1. **Update RD-04 and RD-06**: Adopt a Dual-Control baseline ($B_{1-SC-calls}$ at $K=6$ and $B_{1-SC-tokens}$ at $K=9$) and specify odd $K$ or deterministic tie-breaking.
2. **Update RD-06**: Expand GSM8K evaluation to $N=500$ (or widen margin to $\pm 5\%$) and replace Two-Way ANOVA with binomial GLMM.
3. **Update RD-08**: Replace Pearson Chi-square with Cochran's Q test.
4. **Update RD-12**: Correct API cost arithmetic from $\$34.50$ to $\$43.20$ for RP-02 and total from $\$52.25$ to $\$63.50$.
5. **Update RD-03 and RD-05–RD-08**: Define `INCONCLUSIVE_SUB_THRESHOLD` outcome mapping.
