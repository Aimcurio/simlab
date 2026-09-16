# PX-12: Independent Substantive Review
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Reviewer**: Sol (Independent Senior Reviewer & Failure Analyst)  
**Evaluation Date**: 2026-09-16  

---

## 1. Substantive Statistical Audit Findings

I have conducted a rigorous audit of the statistical claims against the pre-registered Phase 2 contracts (`RD-05` to `RD-09`).

### Evaluative Findings:
1. **RP-01 (Smallville Memory Recency)**:
   - Inversion rate drop ($74.5\% \to 41.0\%$) is verified. Equal weighting fails ($\Delta = +0.0446 < 0.05$). Tuned weighting succeeds ($\Delta = +0.1685 \ge 0.15, p = 0.00026 < 0.0025$). I affirm `SUPPORTED_WITH_CONSTRAINTS`.
2. **RP-02 (Compute-Matched Debate)**:
   - On Private Information, $p = 0.0192 > 0.01$. Under Curo discipline, **this must not be called statistically significant**. It is properly classified as `PROMISING_BUT_NOT_SIGNIFICANT`.
   - On GSM8K, $p_{TOST} = 0.741$. Equivalence was not established. It is properly classified as `EQUIVALENCE_NOT_ESTABLISHED`.
   - I affirm that RP-02 provides tentative, context-dependent evidence that requires targeted ablation in Phase 4.
3. **RP-03 (ChatDev SOPs)**:
   - $49.17\%$ token savings ($p < 10^{-14}$) and zero role violations strictly meet all pre-registered thresholds. I affirm `SUPPORTED_WITH_CONSTRAINTS`.
4. **RP-04 (Dynamic Orchestration)**:
   - Heuristic routing achieved $27.80\%$ savings with $-2.0\%$ accuracy delta, strictly satisfying the $\le 3.0\%$ loss tolerance. `STOP_ESCALATION_VALID` is certified. Unexecuted tiers are properly classified as `NOT_TESTED_DUE_TO_STOPPING_RULE`.

**Substantive Review Recommendation**: **`SUBSTANTIVE_RESULT_VERIFICATION: PASS` (With Reconciled Classifications)**.
