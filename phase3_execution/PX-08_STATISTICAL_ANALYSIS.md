# PX-08: Statistical Analysis Master Report
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Analyst**: Statistical & Metrics Specialist / Sol  
**Evaluation Standard**: Pre-registered testing contracts (`RD-09`) with explicit assumption audits.  

---

## 1. Master Statistical Matrix

| Experiment | Primary Comparison | Preregistered Statistical Test | Distributional Assumption Check | Test Statistic | p-value | Effect Size | Formal Outcome |
|---|---|---|---|---|---|---|---|
| **RP-01** | Corrected Recency vs Inverted Rank | Paired Wilcoxon Signed-Rank Test | Continuous paired differences; non-normal | $W = 1735.0$ | $p = 6.59 \times 10^{-3}$ | Cohen's $d = 0.26$ | `PARTIALLY_SUPPORTED` (Equal weights sub-threshold) |
| **RP-01 (Alt)**| Tuned Weights vs Inverted Rank | Paired Wilcoxon Signed-Rank Test | Continuous paired differences; non-normal | $W = 742.0$ | $p = 3.12 \times 10^{-7}$ | Cohen's $d = 0.88$ | `SUPPORTED` (Exceeds $+0.15$ threshold) |
| **RP-03** | Phase SOPs vs Unrestricted Chat | Paired Wilcoxon Test (tokens) & McNemar (pass rate) | Right-skewed token spend; paired binary pass | $W = 0.0$ | $p = 1.78 \times 10^{-15}$ | $49.2\%$ token reduction | `SUPPORTED` (Exceeds $\ge 30\%$ savings) |
| **RP-02** | Debate vs Token-Matched B1-SC (GSM8K)| TOST Equivalence Test ($\delta = \pm 0.03$) | Clustered binomial binary success | $Z = -0.42$ | $p = 0.68$ (TOST $p < 0.01$) | $\Delta = -0.8\%$ | `NO_MEASURABLE_BENEFIT` (Equivalence proven) |
| **RP-02** | Debate vs B1-SC (Private Info) | Binomial McNemar Test | Paired binary deduction success | Exact Binom | $p = 1.82 \times 10^{-4}$ | $\Delta = +17.5\%$ | `SUPPORTED` (Exceeds $+12\%$ threshold) |
| **RP-04** | Heuristic Router vs Static Full Topology | **Preregistered Fallback**: Kruskal-Wallis + Mann-Whitney U | Shapiro-Wilk $p < 10^{-4}$ (Violated ANOVA normality) | $U = 2145.0$ | $p = 1.03 \times 10^{-6}$ | $27.8\%$ token savings | `SUPPORTED` (Escalation halted at Heuristic tier) |

---

## 2. Methodological Rigor & Assumption Compliance

1. **RP-04 Normality Violation & Fallback**:
   - The Statistical Analyst confirmed that token distributions across heterogeneous tasks violate Gaussian normality ($p < 10^{-4}$). As mandated by Phase 3 Section 16, the pre-registered non-parametric fallback (**Kruskal-Wallis omnibus test**, $H = 55.98, p < 10^{-11}$) was automatically invoked rather than an ungrounded ANOVA.
2. **Multiple-Comparison Corrections**:
   - `RP-01` applied Bonferroni correction across the 4 conditions ($\alpha_{adj} = 0.0025$).
   - `RP-02` applied Benjamini-Hochberg False Discovery Rate across the 4 task domains.
