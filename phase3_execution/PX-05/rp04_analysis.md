# PX-05: RP-04 Analysis & Hypothesis Testing
**Experiment ID**: `EXP-RP04-DYNAMIC-ORCHESTRATION-V1`  
**Analyst**: Statistical & Metrics Specialist / Sol  
**Evaluation Verdict**: **HYPOTHESIS SUPPORTED ($H_1$) — ESCALATION HALTED AT HEURISTIC TIER**  

---

## 1. Statistical Discipline & Preregistered Fallback Execution

### Normality Audit
- Shapiro-Wilk test on token distributions across routing tiers returned $p < 10^{-4}$ (Right-skewed token distribution).
- As mandated by Phase 3 Section 16, **the preregistered non-parametric fallback was automatically invoked**:
  - **Kruskal-Wallis Omnibus Test**: $H = 55.98, p = 4.28 \times 10^{-12}$ (Statistically significant difference in token consumption across routing tiers).
  - **Pairwise Mann-Whitney U Test** (Heuristic vs Static): $U = 3000.0$, $p = 1.0313 \times 10^{-6}$ (Significant token reduction).

---

## 2. Progressive Complexity Rule & Bounded Stopping-Rule Interpretation

1. **Failure of Deterministic Tier**:
   - `DETERMINISTIC_ROUTING` relied on simplistic query length rules, leading to an unacceptable **10.0% under-activation rate** on complex, concise tasks. Accuracy dropped to 86.0%, violating the $\le 3\%$ margin. Escalation to Heuristic tier was required.
2. **Success of Heuristic Tier**:
   - `HEURISTIC_ROUTING` achieved **90.0% accuracy** (within 2.0% of Static Topology: $90/100$ vs $92/100$) while achieving **27.80% token savings** ($247,451$ vs $342,707$ tokens, $p < 10^{-6}$).
   - Under-activation rate was contained to 1.0%.
3. **Application of the Complexity Burden Rule**:
   - The pre-registered protocol mandates: *"If heuristic routing is sufficient: STOP_ESCALATION. Do not deploy LLM or learned routing unnecessarily."*
   - Because `HEURISTIC_ROUTING` satisfied the pre-registered success criteria ($\ge 25\%$ token savings, $\le 3\%$ accuracy drop), the project invoked **`STOP_ESCALATION`**.

### Explicit Boundaries on Routing Conclusions:
- **WHAT WAS TESTED**: `STATIC_ROUTING`, `DETERMINISTIC_ROUTING`, `HEURISTIC_ROUTING` (and exploratory `LLM_ROUTER`).
- **WHAT WAS NOT NECESSARY TO EXECUTE**: `LEARNED_PUPPETEER_ROUTING` (and deploying LLM routers in production).
- **Classification**: `LEARNED_PUPPETEER_ROUTING` is formally classified as **`NOT_TESTED_DUE_TO_STOPPING_RULE`**, not `REJECTED`, `HARMFUL`, or `INFERIOR`.
- **Grounded Conclusion**: "Under the tested workload and preregistered thresholds, heuristic routing achieved sufficient quality while reducing resource use, so escalation to more complex routing mechanisms was not scientifically or economically justified."
