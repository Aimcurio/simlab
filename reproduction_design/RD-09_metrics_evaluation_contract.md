# RD-09: Metrics & Evaluation Contract
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. Governing Evaluation Philosophy: Deterministic Measurement First

To eliminate evaluator bias, sycophancy, and uncalibrated model judging, SimLab enforces a strict measurement hierarchy across all Phase 2 reproduction designs and subsequent phases:

```
+----------------------------------------------------------------------------------------------------+
|                                DETERMINISTIC MEASUREMENT HIERARCHY                                 |
+----------------------------------------------------------------------------------------------------+
| Level 1: Deterministic Truth  | Unit test pass, exact match, regex assertions, syntax validity    |
| Level 2: Algorithmic Ranking  | MRR, NDCG@K, recall@K, precision@K, edit distance, AST equivalence |
| Level 3: System Telemetry     | Token count, inference call count, wall latency, memory usage      |
| Level 4: Auxiliary LLM Judge  | Permitted ONLY as secondary analysis with multi-judge consensus     |
+----------------------------------------------------------------------------------------------------+
```

### Invariant on LLM Judges
> **Evaluator Invariant**:  
> No primary hypothesis in SimLab may depend solely or primarily on an LLM evaluator if a Level 1, 2, or 3 measurement is scientifically possible. If an LLM judge is used as a secondary metric, it must employ a frozen rubric, temperature $T=0.0$, position-permutation de-biasing, and an inter-annotator agreement threshold (Cohen's $\kappa \ge 0.75$).

---

## 2. Metric Specifications by Reproduction Candidate

| Experiment ID | Primary Metric (Deterministic) | Secondary Metric (Telemetry) | Auxiliary Metric (Judge) | Success Criterion | Falsification / Failure Threshold | Inconclusive Default Rule |
|---|---|---|---|---|---|---|
| **EXP-RP01-RECENCY** | **MRR & NDCG@5**: Exact rank of ground-truth target memory in ranked output | **Temporal Inversion Rate**: Fraction of older memories ranked above newer identical-relevance memories | N/A (Zero LLM judging) | $\Delta \text{MRR} \ge +0.15, p < 0.0025$ (Calibrated weights $\alpha=0.5, \beta=3.0, \gamma=2.0$) | $\Delta \text{MRR} < +0.05, p \ge 0.05$ over `B0-NoRecency` | `INCONCLUSIVE_SUB_THRESHOLD` ($[+0.05, +0.15)$): Default to `B0-NoRecency` + discrete buffer |
| **EXP-RP02-COMPUTE-MATCHED** | **Task Accuracy**: Exact-match on GSM8K ($N=500$); ground-truth state match on deduction & tool suites | **Compute Efficiency**: Accuracy per $10^5$ tokens under Dual-Control ($K=7$ calls, $K=10$ tokens) | **False Consensus Rate**: Tracking convergence onto initially incorrect solutions | $\ge +10\%$ accuracy advantage on private-info/tools ($p < 0.01$) AND GSM8K TOST within $[-0.03, +0.03]$ | $B_{1-SC-tokens}$ equals/beats debate across all tasks ($p \ge 0.05$), or False Consensus $> 20\%$ | `INCONCLUSIVE_SUB_THRESHOLD` ($[+2\%, +10\%)$): Default to simpler baseline (`B1` / `B1-SC-calls`) |
| **EXP-RP03-PHASE-BOUNDARIES** | **Unit Test Pass Rate**: Automated execution in isolated Python sandbox ($N=150$) | **Token & Turn Efficiency**: Total tokens consumed and conversational turns to completion | **Cross-Role Contamination**: Automated regex audit for out-of-role actions | $\ge 25\%$ token reduction with non-inferior pass rate ($\Delta \text{Pass} \ge -3\%, p < 0.01$) | Token reduction $< 10\%$, or pass rate drops $> 10\%$ ($p < 0.01$) | `INCONCLUSIVE_SUB_THRESHOLD` (Tokens $[10\%, 25\%)$): Default to simpler baseline (`Control A` / chat) |
| **EXP-RP04-DYNAMIC-ORCHESTRATION** | **Task Success Rate**: Deterministic test suite pass across heterogeneous tasks ($N=300$) | **Pareto Efficiency**: System token savings and Router Overhead Fraction ($\text{Tok}_{orch} / \text{Tok}_{total}$) | **Routing Error Rates**: Under-activation vs. over-activation frequencies | $\ge 25\%$ token savings with held-out accuracy drop $\le 3\%$ vs `B3`, and non-inferior to `B1-SC` | Net token savings $< 5\%$, or under-activation $> 10\%$ ($p < 0.01$) | `INCONCLUSIVE_SUB_THRESHOLD` (Savings $[5\%, 25\%)$): Default to simpler baseline (`B0-Heuristic` / `B1-SC`) |

---

## 3. Statistical Testing & Power Analysis Standards

1. **Statistical Power**: All experiments must achieve a minimum statistical power of $1 - \beta = 0.80$ at significance level $\alpha = 0.01$ (or $\alpha = 0.05$ for TOST equivalence).
2. **Hypothesis Testing Methods**:
   - **Continuous Paired Metrics (MRR, Token Spend, Latency)**: Paired Wilcoxon signed-rank test (non-parametric).
   - **Binary Repeated-Measures Across Conditions (GLMM)**: For multi-factorial binary accuracy (RP-02), a Binomial Generalized Linear Mixed Model with a logit link function (`lme4::glmer` or `statsmodels.Binomial`) is mandatory, modeling task instance as a random effect and architecture conditions and task categories as fixed effects.
   - **Matched Multi-Condition Binary Comparisons (Cochran's Q)**: For $k \ge 3$ matched binary treatments evaluating identical tasks (RP-04), Cochran's Q test is mandatory, followed by post-hoc pairwise McNemar tests with Bonferroni correction ($\alpha = 0.01 / \binom{k}{2}$).
   - **Equivalence Testing (TOST)**: For equivalence claims (RP-02 GSM8K), Two One-Sided Tests (TOST) at margin $\delta = 0.03$ are mandatory, requiring the $90\%$ confidence interval to fall strictly within $[-\delta, +\delta]$.
   - **Independent Group Comparisons**: Fisher's exact test for independent categorical failure proportions.
3. **Effect Size Reporting**: Every comparison must report Cohen's $d$ (parametric), Cliff's $\delta$ (non-parametric), or Odds Ratios (GLMM), accompanied by 95% bootstrap confidence intervals ($10,000$ resamples).
4. **Pre-Registered Default for Inconclusive Outcomes**: If an observed effect falls between the pre-registered success and failure thresholds (`INCONCLUSIVE_SUB_THRESHOLD`), the experimental protocol mandates defaulting to the simpler, lower-compute baseline under the Minimum Experiment Principle.
