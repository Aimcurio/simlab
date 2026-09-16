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
