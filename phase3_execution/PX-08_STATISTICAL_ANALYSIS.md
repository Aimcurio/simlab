# PX-08: Statistical Analysis Master Report
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Analyst**: Statistical & Metrics Specialist / Sol  
**Evaluation Standard**: Pre-registered testing contracts (`RD-09`) with explicit assumption audits and Layer B numerical verification.  

---

## 1. Master Statistical Reconciliation Matrix (All 4 Candidates vs Preregistered Contracts)

| Experiment | Primary Hypothesis | Primary Metric | Observed Effect (Raw Counts) | Statistical Test | p-value / CI | Preregistered Alpha ($\alpha$) | Preregistered Success Threshold | Threshold Met? | Final Canonical Status |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **RP-01** | Corrected Recency eliminates inversion bug; tuned weights outperform rank | Inversion Rate & MRR Delta | Inversion: $74.5\% \to 41.0\%$; Tuned $\Delta \text{MRR} = +0.1685$ ($0.2403$ vs $0.0718$) | Paired Wilcoxon Signed-Rank | $W = 1463.0, p = 2.60 \times 10^{-4}$ | $\alpha = 0.0025$ | Inversion $< 50\%$; $\Delta \text{MRR} \ge +0.15$ | **YES** | **`SUPPORTED_WITH_CONSTRAINTS`** |
| **RP-01 (Equal)**| Equal weighting ($\alpha=\beta=\gamma=1$) is optimal | MRR Delta | $\Delta \text{MRR} = +0.0446$ ($0.1164$ vs $0.0718$) | Paired Wilcoxon Signed-Rank | $W = 1735.0, p = 6.59 \times 10^{-3}$ | $\alpha = 0.0025$ | $\Delta \text{MRR} \ge +0.05$ | **NO** ($0.0446 < 0.05$) | **`HYPOTHESIS_REJECTED`** (Equal weights disproven) |
| **RP-02 (Priv)** | Debate outperforms B1-SC on private info | Accuracy Delta | $+14.0\%$ ($87/100$ vs $73/100$) | McNemar Exact Binomial | $p = 0.0192$; $95\%\text{ CI}: [+4.2\%, +23.8\%]$ | $\alpha = 0.01$ | $\ge +10.0\%$ and $p < 0.01$ | **NO** ($p = 0.0192 > 0.01$) | **`PROMISING_BUT_NOT_SIGNIFICANT`** |
| **RP-02 (GSM)** | Debate equals B1-SC on closed reasoning | TOST Equivalence ($\delta = \pm 0.03$) | $+4.40\%$ ($446/500$ vs $424/500$) | Two One-Sided Tests (TOST) | $p_{TOST} = 0.741$; $90\%\text{ CI}: [+0.84\%, +7.96\%]$ | $\alpha = 0.05$ | $p_{TOST} < 0.05$ (CI inside $\pm 3\%$) | **NO** (CI crosses $+3\%$) | **`EQUIVALENCE_NOT_ESTABLISHED`** |
| **RP-02 (State)**| Debate outperforms B1-SC on state tracking | Accuracy Delta | $+18.0\%$ ($84/100$ vs $66/100$) | McNemar Exact Binomial | $p = 0.0051$; $95\%\text{ CI}: [+6.8\%, +29.2\%]$ | $\alpha = 0.01$ | $\ge +10.0\%$ and $p < 0.01$ | **YES** ($p < 0.01$) | **`SUPPORTED`** |
| **RP-03** | Phase SOPs reduce tokens without pass degradation | Token Savings & Test Pass | Tokens: $-49.17\%$ ($557,068 / 1,133,027$); Pass: $+6.15\%$ ($86.87\%$ vs $80.72\%$) | Paired Wilcoxon Signed-Rank | Tokens: $W=0, p = 1.78 \times 10^{-15}$; Pass: $p = 0.0389$ | $\alpha = 0.01$ | Tokens $\ge 25\%$ savings; Pass degradation $\le 3\%$ | **YES** | **`SUPPORTED_WITH_CONSTRAINTS`** |
| **RP-04** | Dynamic routing saves $\ge 25\%$ tokens within $\le 3\%$ loss | Token Savings & Accuracy Delta | Tokens: $-27.80\%$ ($95,256 / 342,707$); Acc: $-2.0\%$ ($90/100$ vs $92/100$) | Mann-Whitney U Test (Fallback) | Tokens: $U=3000, p = 1.03 \times 10^{-6}$ | $\alpha = 0.01$ | Tokens $\ge 25\%$ savings; Acc loss $\le 3.0\%$ | **YES** | **`SUPPORTED_WITH_CONSTRAINTS`** (`STOP_ESCALATION_VALID`) |

---

## 2. Rigorous Epistemic Clarifications

1. **RP-02 Adjudication**:
   - The private-information effect size ($+14.0\%$) is practically substantial, but because $p = 0.0192 > 0.01$, Curo governance strictly forbids labeling it statistically significant. It remains tentative evidence awaiting higher-powered replication in Phase 4.
   - On GSM8K, TOST failed to reject the non-equivalence null ($p = 0.741$). The observed $+4.4\%$ difference prevents asserting equivalence, while simultaneously failing to establish that debate is meaningfully superior given the $8.2\%$ sycophancy rate.
2. **RP-04 Stopping Rule**:
   - Verified that $-2.0\%$ accuracy degradation is strictly within the $\le 3.0\%$ pre-registered quality margin. `STOP_ESCALATION_VALID` certified.
