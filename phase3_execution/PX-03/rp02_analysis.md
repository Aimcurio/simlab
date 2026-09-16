# PX-03: RP-02 Analysis & Hypothesis Testing
**Experiment ID**: `EXP-RP02-COMPUTE-MATCHED-V1`  
**Analyst**: Statistical & Metrics Specialist / Sol  
**Evaluation Verdict**: **PREREGISTERED THRESHOLD NOT MET — INCONCLUSIVE / PROMISING_BUT_NOT_SIGNIFICANT**  

---

## 1. Preregistered Hypothesis Evaluation & Audit Against Alpha = 0.01

- **Preregistered Hypothesis ($H_1$)**: On tasks with private/partitioned information or asymmetric tool specializations, a 3-agent debate architecture will outperform compute-matched single-agent $B1-SC$ by $\ge +10\%$ accuracy with statistical significance at pre-registered **$\alpha = 0.01$**. Conversely, on closed-domain symbolic reasoning (GSM8K), compute-matched $B1-SC$ will equal multi-agent debate within an equivalence margin of $\delta = \pm 0.03$ ($p_{TOST} < 0.05$).
- **Null Hypothesis ($H_0$)**: Compute-matched single-agent $B1-SC$ equals or outperforms multi-agent debate across all task categories ($H_0: p_{\text{debate}} \le p_{B1-SC}$), or difference is sub-threshold.

---

## 2. Rigorous Statistical Reconciliation by Domain

### 1. Private Information Tasks ($N=100$)
- **Empirical Counts**: Multi-Agent Debate: $87/100$ ($87.0\%$) vs $B1-SC\text{-tokens}$: $73/100$ ($73.0\%$).
- **Observed Difference**: $+14.0\%$ ($95\%\text{ CI}: [+4.2\%, +23.8\%]$).
- **Statistical Test**: McNemar's exact binomial test on discordant pairs ($b=27$ debate wins, $c=13$ SC wins).
- **Empirical p-value**: **$p = 0.0192$**.
- **Audit Against Preregistered Alpha**:
  - Preregistered Alpha: **$\alpha = 0.01$**.
  - Result: **$p = 0.0192 > 0.01$**.
  - **Verdict**: While the observed effect size ($+14.0\%$) exceeds the $\ge +10\%$ threshold, the result **FAILS** the pre-registered significance threshold ($\alpha = 0.01$).
  - **Permitted Classification**: **`PROMISING_BUT_NOT_SIGNIFICANT`**.
  - **Permitted Conclusion**: The data demonstrates a promising empirical trend toward multi-agent coordination on private-information tasks ($+14.0\%$), but does not achieve the pre-registered standard of statistical proof at $\alpha = 0.01$.
  - **Prohibited Conclusion**: Claiming that multi-agent debate is "proven statistically superior" or "statistically significant at $\alpha = 0.01$".

### 2. Closed Symbolic Reasoning (GSM8K, $N=500$)
- **Empirical Counts**: Multi-Agent Debate: $446/500$ ($89.2\%$) vs $B1-SC\text{-tokens}$: $424/500$ ($84.8\%$).
- **Observed Difference**: $+4.40\%$ ($90\%\text{ CI}: [+0.84\%, +7.96\%]$; $95\%\text{ CI}: [+0.16\%, +8.64\%]$).
- **Equivalence Specification**: Equivalence margin $\delta = \pm 0.03$ ($[-3.0\%, +3.0\%]$).
- **Two One-Sided Tests (TOST)**:
  - Lower Bound Test ($H_{01}: \Delta \le -0.03$): $t_1 = 3.417, p_1 = 0.00034$.
  - Upper Bound Test ($H_{02}: \Delta \ge +0.03$): $t_2 = 0.646, p_2 = 0.7408$.
  - **TOST p-value**: **$p_{TOST} = \max(p_1, p_2) = 0.7408$**.
- **Audit Against Preregistered Alpha**:
  - Preregistered Alpha: $\alpha = 0.05$.
  - Result: **$p_{TOST} = 0.7408 \ge 0.05$**.
  - **Verdict**: The equivalence null cannot be rejected. Strict equivalence within $\pm 3.0\%$ was **NOT ESTABLISHED**.
  - **Permitted Classification**: **`EQUIVALENCE_NOT_ESTABLISHED`**.
  - **Core Rule**: A failed TOST must never be interpreted as evidence of equivalence, nor does it establish definitive superiority.
  - **Permitted Conclusion**: Equivalence within $\pm 3\%$ was not established; multi-agent debate showed a modest $+4.4\%$ nominal difference on this sample, but whether debate and single-agent compute-matched baselines are equivalent or divergent remains statistically unresolved.

### 3. Asymmetric Tools ($N=100$)
- Debate $89/100$ vs $B1-SC$ $75/100$ ($+14.0\%$, McNemar $p = 0.0125$). Also misses $\alpha = 0.01$ ($0.0125 > 0.01$). Classified as `PROMISING_BUT_NOT_SIGNIFICANT`.

### 4. Distributed State Tracking ($N=100$)
- Debate $84/100$ vs $B1-SC$ $66/100$ ($+18.0\%$, McNemar $p = 0.0051$). Satisfies $\alpha = 0.01$ ($0.0051 < 0.01$).

---

## 3. Synthesis of Supported, Prohibited, and Unresolved Claims

- **WHAT IS SUPPORTED**:
  - Multi-agent debate achieves compute parity ($+2.18\%$ to $+2.82\%$ token spend, well within $\pm 10\%$).
  - Distributed state tracking exhibits a statistically significant gain ($+18.0\%, p = 0.0051 < 0.01$).
  - Sycophancy / False Consensus is an observed risk in debate ($8.2\%$ rate on GSM8K).
- **WHAT IS NOT SUPPORTED**:
  - Multi-agent debate is NOT proven statistically superior on private information at the pre-registered $\alpha = 0.01$ level ($p = 0.0192$).
  - Equivalence between Debate and $B1-SC$ on GSM8K within $\pm 3\%$ is NOT established ($p_{TOST} = 0.741$).
- **WHAT REMAINS UNRESOLVED (FORWARD TO PHASE 4)**:
  - Does private-information advantage replicate and achieve $p < 0.01$ with higher power ($N \ge 250$)?
  - What is the true difference between debate and compute-matched $B1-SC$ on closed reasoning?
