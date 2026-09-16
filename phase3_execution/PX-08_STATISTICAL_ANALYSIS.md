# PX-08: Statistical Analysis Master Report
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Analyst**: Statistical & Metrics Specialist / Sol  
**Evaluation Standard**: Pre-registered testing contracts (`RD-09`) with explicit assumption audits and Layer B numerical verification.  

---

## 1. Master Statistical Matrix (Recomputed from Immutable Telemetry)

| Experiment | Primary Comparison | Preregistered Statistical Test | Distributional Assumption Check | Test Statistic | p-value | Recomputed Effect Size (Raw Numerator/Denominator) | Formal Outcome |
|---|---|---|---|---|---|---|---|
| **RP-01** | Corrected Recency vs Inverted Rank | Paired Wilcoxon Signed-Rank Test | Continuous paired differences; non-normal | $W = 1735.0$ | $p = 6.59 \times 10^{-3}$ | Inversion: $74.5\% \to 41.0\%$ ($74.5/100 \to 41.0/100$); $\Delta \text{MRR} = +0.0446$ | `PARTIALLY_SUPPORTED` (Equal weights sub-threshold) |
| **RP-01 (Alt)**| Tuned Weights vs Inverted Rank | Paired Wilcoxon Signed-Rank Test | Continuous paired differences; non-normal | $W = 1463.0$ | $p = 2.60 \times 10^{-4}$ | $\Delta \text{MRR} = +0.1685$ ($0.2403$ vs $0.0718$); $d = 0.88$ | `SUPPORTED` (Exceeds $+0.15$ threshold) |
| **RP-03** | Phase SOPs vs Unrestricted Chat (Tokens) | Paired Wilcoxon Test | Right-skewed token spend; paired tasks | $W = 0.0$ | $p = 1.78 \times 10^{-15}$ | $49.17\%$ token reduction ($557,068 / 1,133,027$) | `SUPPORTED` (Exceeds $\ge 30\%$ savings) |
| **RP-03 (Pass)**| Phase SOPs vs Unrestricted Chat (Pass Rate) | Paired Wilcoxon Test | Paired continuous score $[0, 1]$ | $W = 189.0$ | $p = 3.89 \times 10^{-2}$ | $+6.15\%$ pass rate ($86.87\%$ vs $80.72\%$) | `SUPPORTED` |
| **RP-02** | Debate vs Token-Matched B1-SC (GSM8K)| TOST Equivalence Test ($\delta = \pm 0.03$) | Clustered binomial binary success | $t_1 = 3.42, t_2 = 0.65$ | $p_{TOST} = 0.741$ | $+4.40\%$ difference ($446/500$ vs $424/500$, $95\%\text{ CI}: [+0.16\%, +8.64\%]$) | `VERIFIED_WITH_CORRECTION` (Diff exceeds $+3\%$ margin) |
| **RP-02 (Priv)**| Debate vs B1-SC (Private Info) | Binomial McNemar Exact Test | Paired binary deduction success | $b=27, c=13$ | $p = 1.92 \times 10^{-2}$ | $+14.0\%$ accuracy gain ($87/100$ vs $73/100$) | `SUPPORTED` (Exceeds $+12\%$ threshold) |
| **RP-04** | Heuristic Router vs Static Topology | **Preregistered Fallback**: Kruskal-Wallis + Mann-Whitney U | Shapiro-Wilk $p < 10^{-4}$ (Violated ANOVA normality) | $U = 3000.0$ | $p = 1.03 \times 10^{-6}$ | $27.80\%$ token savings ($95,256 / 342,707$); Acc: $90/100$ vs $92/100$ ($-2.0\%$) | `SUPPORTED` (STOP_ESCALATION invoked) |

---

## 2. Methodological Rigor & Assumption Compliance

1. **RP-04 Normality Violation & Fallback**:
   - The Statistical Analyst confirmed that token distributions across heterogeneous tasks violate Gaussian normality ($p < 10^{-4}$). As mandated by Phase 3 Section 16, the pre-registered non-parametric fallback (**Kruskal-Wallis omnibus test**, $H = 55.98, p = 4.28 \times 10^{-12}$) was automatically invoked rather than an ungrounded ANOVA.
2. **RP-02 TOST Reconciliation**:
   - Pre-registered equivalence bound was $\delta = \pm 0.03$. On GSM8K ($N=500$), multi-agent debate achieved $89.2\%$ ($446/500$) vs $B1-SC-tokens$ $84.8\%$ ($424/500$), yielding a $+4.4\%$ gain. Because $+4.4\% > +3.0\%$, the upper one-sided test failed to reject ($p = 0.741$). This proves that while debate does not exhibit large collaborative surplus on closed reasoning, it also does not strictly fall within $\pm 3\%$ of $B1-SC$.
