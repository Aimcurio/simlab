# Independent Review & Adversarial Audit Report: EXP-AB-01-COMP

**Reviewer**: `audit_reviewer_1` (Reviewer & Adversarial Critic)  
**Target Deliverable**: `E:\projects\simlab\audits\EXP-AB-01-COMP\AUDIT_EXP_AB_01_COMP.md`  
**Supporting Verification Suite**: `E:\projects\simlab\audits\EXP-AB-01-COMP\test_audit_verification.py` & `verify_audit.py`  
**Governing Baseline**: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (Prompt `## 2026-09-16T21:54:00Z`)  
**Date**: 2026-09-16  
**Final Verdict**: **`APPROVE`**

---

## 1. Executive Summary & Audit Verdict

This independent review and adversarial evaluation rigorously inspected Sections A, B, C, J, and K of `AUDIT_EXP_AB_01_COMP.md`, executed the complete verification test harness, and performed independent mathematical recalculations directly from immutable raw telemetry and benchmark files.

### Formal Verdict: **`APPROVE`**

The audit deliverable is **exemplary, mathematically sound, forensically rigorous, and publication-grade**. It decisively corrects the flawed statistical reporting of the execution harness, proves non-inferiority and statistical superiority beyond any mathematical ambiguity, uncovers the exact causal mechanisms behind retrieval collapse and reflection crowding, correctly assigns Gate Decision `STAGE_4A_MECHANISTIC_INVESTIGATION_REQUIRED`, and codifies binding forward constraints.

No integrity violations, hardcoded test results, facade implementations, or unauthorized shortcuts were found. All claims were verified against raw data.

---

## 2. Statistical Adjudication Correction (Sections A & B)

### 2.1 Harness Defect Identification
The review examined lines 280–286 of `run_exp_ab_01_comp.py` and lines 96–108 of `exp_ab_01_comp_results.json`:
1. **The Scalar Comparison Flaw**: The execution harness evaluated non-inferiority using a naive scalar check `a4_delta >= -0.02`. This point-estimate comparison ignores sample variance, standard error, and degrees of freedom.
2. **Directional Conflation in Null Hypothesis Testing**: In evaluating $H_0: \text{MRR}_{A7} - \text{MRR}_{A4} \ge +0.05$, the harness reported $p = 2.1356 \times 10^{-9}$ as the rationale for rejection. That p-value was generated from a standard two-sided Wilcoxon test of $\text{diff} = 0$. Rejection was not due to treatment success in the hypothesized direction, but because Condition A7 suffered a massive directional collapse ($\Delta = -0.4061$ MRR).

### 2.2 Independent Verification of Statistical Tests
Using raw telemetry (`exp_ab_01_comp_telemetry.jsonl`, SHA-256: `9eb6846b017f76883418e3703dd9f0111182e8dc8a0ea03bb5cd32dd27337eac`), the paired differences $d_i = \text{MRR}_{A4, i} - \text{MRR}_{A7, i}$ across all $N = 100$ queries were recalculated:
- Mean Paired Difference ($\bar{d}$): **$+0.406085$** (MRR$_{A4} = 0.500228$, MRR$_{A7} = 0.094143$)
- Sample Standard Deviation ($s_d$): **$0.434689$**
- Standard Error ($\text{SE} = s_d / \sqrt{100}$): **$0.043469$**
- Standardized Effect Size (Cohen's $d = \bar{d} / s_d$): **$+0.9342$** (Very large effect)
- Degrees of Freedom ($df$): **$99$**

#### One-Sided Paired t-Tests for Non-Inferiority:
Testing $H_0: \mu_d \le -\delta$ vs. $H_1: \mu_d > -\delta$ where $t = (\bar{d} + \delta) / \text{SE}$:
- **Margin $\delta = 0.02$**:
  $$t = \frac{0.406085 - (-0.02)}{0.043469} = 9.8021, \quad p = 1.1102 \times 10^{-16}$$
- **Margin $\delta = 0.05$**:
  $$t = \frac{0.406085 - (-0.05)}{0.043469} = 10.4922, \quad p < 10^{-16} \approx 0.0000$$

#### One-Sided Shifted Wilcoxon Signed-Rank Tests:
Testing ranks of $(d_i + \delta)$:
- **Margin $\delta = 0.02$**: $W = \mathbf{4394.0}, \quad p = \mathbf{6.4934 \times 10^{-11}}$
- **Margin $\delta = 0.05$**: $W = \mathbf{4752.0}, \quad p = \mathbf{9.4090 \times 10^{-15}}$

#### Exact Lower Confidence Bounds (LCB):
$$\text{LCB}_{1-\alpha} = \bar{d} - t_{\text{crit}, \alpha, 99} \times \text{SE}$$
- **95% One-Sided LCB ($\alpha = 0.05, t_{\text{crit}} = 1.660391$)**: **$+0.333910$**
- **99% One-Sided LCB ($\alpha = 0.01, t_{\text{crit}} = 2.364606$)**: **$+0.303299$**
- **Bonferroni LCB ($\alpha = 0.00142857, t_{\text{crit}} = 3.058991$)**: **$+0.273114$**

### 2.3 Mathematical Proof of Verdict String
The verdict string **`NON_INFERIORITY_FORMALLY_CONFIRMED_SUPERIORITY_OBSERVED`** is mathematically proven:
1. Non-inferiority requires proving $\mu_d > -\delta$. Since $p < 10^{-10}$ across both margins $\delta \in \{0.02, 0.05\}$ and both parametric and non-parametric tests, non-inferiority is conclusively confirmed.
2. Superiority requires proving $\mu_d > 0.0$. Testing against margin $\delta = 0.0$ yields $t = 9.3420$ ($p = 1.55 \times 10^{-15}$) and one-sided Wilcoxon $W = 4266.0$ ($p = 1.07 \times 10^{-9}$).
3. Because the Bonferroni-adjusted Lower Confidence Bound ($+0.273114$) strictly exceeds zero, Condition A4 is guaranteed to be superior to Condition A7 by at least $+0.2731$ MRR with $99.86\%$ confidence, controlling family-wise error rate at $\alpha = 0.01$ across all 7 comparisons.

---

## 3. Importance-Necessity Interpretation (Section C)

### 3.1 Verification of Effect Size & Magnitude
- **Absolute Paired Advantage**: $\Delta \text{MRR} = +0.4061$
- **Relative Gain**: $(0.5002 - 0.0941) / 0.0941 = \mathbf{+431.35\%}$ (reported as $+431.3\%$)
- **Cohen's $d$**: $+0.9342$ ($> 0.80$, categorized as a very large effect)
- **95% Two-Sided Confidence Interval**: $[+0.3209, +0.4913]$

### 3.2 Verification of Distractor Importance Dominance
Inspection of `SimLab-MemBench-500.json` ($N=500$ memories, $100$ queries) confirms:
- Mean number of distractors with higher importance than the ground-truth target: **$188.4$ out of $500$** (**$37.7\%$**).
- When stratified by query category:
  - **Recency-Sensitive Queries ($N=40$)**: Target importance is low ($5.050$), resulting in **$234.6$ distractors ($46.9\%$)** possessing higher importance than the target.
  - **Temporal-Conflict Queries ($N=20$)**: Similarly, **$234.6$ distractors ($46.9\%$)** have higher importance.
  - **Relevance-Dominant Queries ($N=40$)**: $119.2$ distractors ($23.8\%$) have higher importance.
- Point-biserial correlation between static importance and target status across 50,000 query-memory evaluations:
  $$r = +0.0182 \quad (p = 4.54 \times 10^{-5}, R^2 = 0.00033)$$
  Static importance accounts for only $0.03\%$ of target relevance variance.

### 3.3 Verification of Causal Mechanics
The audit deliverable accurately identifies why static importance degrades retrieval under min-max normalization:
1. **Near-Target Competition**: In semantic dense retrieval, the target memory has cosine similarity $\approx 0.9792$, while top semantic distractors have $\approx 0.9446$. At weight $\beta = 0.5$, the target's semantic advantage is $+0.0147$.
2. **Noise Amplification**: A distractor with high static importance ($5.92$ vs target $5.24$) obtains a normalized importance advantage of $+0.1029$ at weight $\gamma = 0.3$.
3. **The 7:1 Ratio**: The distractor's static importance advantage is **7.0 times larger** than the target's semantic advantage ($0.1029 / 0.0147 \approx 7.0$). In 100% of queries under A7, distractors outscore the target, driving median rank down to 13.0 and mean MRR to 0.0941.
4. **Category Breakdown Verification**:
  - Recency-Sensitive: A4 MRR = $0.7229$ vs A7 MRR = $0.0904$ ($\Delta = -0.6325$)
  - Temporal-Conflict: A4 MRR = $1.0000$ vs A7 MRR = $0.1549$ ($\Delta = -0.8451$)
  - Relevance-Dominant: A2 MRR = $1.0000$ vs A6 MRR = $0.3838$ ($\Delta = -0.6162$)

---

## 4. Stage 4A Decision (Section J) and Next Approved Action (Section K)

### 4.1 Exhaustive Adjudication of the Four Permitted Options
The audit evaluated the 4 permitted outcomes under Requirement R10:

| Candidate Status | Audit Evaluation | Reviewer Finding |
|:---|:---:|:---|
| `STAGE_4A_RESULT_VALID_NEXT_EXPERIMENT_ALLOWED` | **REJECTED** | **Validly Rejected**. Advancing to `EXP-AB-02-REP` while Condition A7 collapsed by 81% and Condition A8 suffered 100% reflection crowding would violate the Curo Invariant: *"Extreme effects must be treated as evidence to be mechanistically diagnosed, not automatic truth."* |
| `STAGE_4A_CORRECTIVE_RERUN_REQUIRED` | **REJECTED** | **Validly Rejected**. No hardware crashes, seed errors, or configuration drift occurred. Hashes match bit-for-bit, and execution was 100% deterministic ($0 runtime LLM calls). Rerunning without design amendments would deterministically replicate the exact same numbers. |
| `STAGE_4A_EVIDENCE_CONFLICT_REQUIRES_REVIEW` | **REJECTED** (Resolved) | **Validly Resolved**. The apparent tension with Phase 3 RP-01 ($0.2403$ vs $0.0941$) was proved to be a parameter transposition in AS-03 ($(0.3, 0.5, 0.2)$ vs $(0.2, 0.5, 0.3)$). Phase 4 simplex sweep replicated Phase 3 to four decimal places ($0.240289$). |
| `STAGE_4A_MECHANISTIC_INVESTIGATION_REQUIRED` | **APPROVED** | **Strictly Warranted**. Two distinct mechanisms require formal diagnosis: (1) min-max scale compression across orthogonal distractors, and (2) reflection node scale dominance (+6.10$\sigma$) and absence of admission controls. |

### 4.2 Next Approved Action (Section K)
Section K correctly prescribes:
1. Protocol `MI-01` (Mechanistic Investigation Protocol) focusing on score normalization compatibility (z-score, softmax, rank) and reflection admission controls (query intent gating, quotas).
2. Binding negative constraints `NC-71` through `NC-75`.
3. Maintenance of strict governance invariants: Implementation Authority `NOT_GRANTED`, Architecture Status `UNFROZEN`, and `EXP-AB-02-REP` advancement **STRICTLY BLOCKED** until Gate R4A approves `MI-01`.

---

## 5. Adversarial Challenge & Stress-Testing

As an adversarial critic, four challenge scenarios were tested to probe for failure modes or unstated assumptions:

### Challenge 1: Normality Assumption Violation
- **Stress Test**: Executed a Shapiro-Wilk test on paired differences $d_i = \text{MRR}_{A4, i} - \text{MRR}_{A7, i}$.
- **Result**: $W = 0.8065, p = 3.9322 \times 10^{-10}$. Normality is strongly rejected due to bounded, discrete reciprocal ranks.
- **Defense / Counter-Verification**:
  1. The audit deliverable anticipated this non-normality and conducted shifted Wilcoxon signed-rank tests ($p = 6.49 \times 10^{-11}$).
  2. An independent 100,000-sample bootstrap lower confidence bound analysis was conducted:
     - Bootstrap 95% LCB: **$+0.335069$** (parametric: $+0.333910$)
     - Bootstrap 99% LCB: **$+0.305694$** (parametric: $+0.303299$)
     - Bootstrap Bonferroni LCB: **$+0.279659$** (parametric: $+0.273114$)
  3. **Verdict**: The parametric t-distribution bounds are actually slightly *more conservative* than non-parametric bootstrap percentiles. The superiority conclusion is completely robust.

### Challenge 2: Non-Inferiority Margin Sensitivity
- **Stress Test**: Tested whether the non-inferiority verdict depends on the choice of margin $\delta$.
- **Result**: Even setting $\delta = 0.00$ (a pure superiority test), $t = 9.3420$ ($p = 1.55 \times 10^{-15}$) and Wilcoxon $W = 4266.0$ ($p = 1.07 \times 10^{-9}$).
- **Verdict**: The verdict is immune to margin choice within $[0.00, 0.10]$.

### Challenge 3: Score Tie Sensitivity
- **Stress Test**: Tested whether sorting direction or tie-breaking order in `run_exp_ab_01_comp.py` altered the ranks.
- **Result**: In Conditions A4 and A7, exactly **0 out of 100 queries** contain identical scores among candidate memories.
- **Verdict**: Tie-breaking rules have zero impact on the A4 vs A7 comparison.

### Challenge 4: Integrity Violation Audit
- **Stress Test**: Scanned `verify_audit.py`, `test_audit_verification.py`, and `AUDIT_EXP_AB_01_COMP.md` for hardcoded answers, dummy mocks, or skipped execution paths.
- **Result**:
  - Test suite loads full JSON and JSONL datasets.
  - Cryptographic hashes match the raw files.
  - All metrics are calculated via NumPy/SciPy from raw arrays.
  - Full counterfactual simulation of 600 memories and 100 queries is executed dynamically in test 6.
- **Verdict**: Zero integrity violations detected.

---

## 6. Verification Test Suite Execution Results

Both mandatory verification commands were executed and passed cleanly:

1. **`python E:\projects\simlab\audits\EXP-AB-01-COMP\verify_audit.py`**
   - Output: `ALL AUDIT RE-CALCULATIONS AND VERIFICATIONS PASSED 100% SUCCESSFULLY.`
   - Exit Code: `0`
2. **`pytest E:\projects\simlab\audits\EXP-AB-01-COMP\test_audit_verification.py`**
   - Output: `8 passed in 1.15s`
   - Exit Code: `0`

---

## 7. Review Summary & Finding Classification

- **Critical Findings**: None.
- **Major Findings**: None.
- **Minor Findings**: None.
- **Commendations**:
  - Exemplary biostatistical rigor in replacing naive scalar checks with shifted hypothesis tests and Bonferroni-adjusted Lower Confidence Bounds.
  - Thorough mechanistic diagnosis distinguishing the implementation defect in A8 (hardcoded 8.5 importance) from the mathematical scale incommensurability in A7.
  - Flawless reconciliation of Phase 3 vs Phase 4 parameter configurations via continuous 2D simplex sweep.
  - Adherence to all Curo SimLab governance invariants and forward constraints.

**Final Recommendation**: **`APPROVE`** without reservations. Deliverable `AUDIT_EXP_AB_01_COMP.md` is certified for progression to Stage 4A Gate Adjudication.
