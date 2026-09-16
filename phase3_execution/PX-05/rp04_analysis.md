# PX-05: RP-04 Analysis & Hypothesis Testing
**Experiment ID**: `EXP-RP04-DYNAMIC-ORCHESTRATION-V1`  
**Analyst**: Statistical & Metrics Specialist / Sol  
**Evaluation Verdict**: **HYPOTHESIS SUPPORTED ($H_1$) — STOP_ESCALATION_VALID**  

---

## 1. Preregistered Stopping Rule & Quality Tolerance Audit

- **Preregistered Thresholds in RD-08 / RD-09**:
  - Token Savings: $\ge 25\%$ reduction vs Static Full Topology ($p < 0.01$).
  - Quality Loss Tolerance: Accuracy degradation **$\le 3.0\%$** compared to Static Full Topology.
  - Overhead Constraint: Orchestrator latency $< 0.05$s, token overhead $< 8\%$.
- **Observed Empirical Results for HEURISTIC_ROUTING**:
  - Token Savings: **$27.80\%$** ($247,451$ vs $342,707$ tokens; $p = 1.03 \times 10^{-6} < 0.01$). $\to$ **MET**.
  - Accuracy Degradation: **$-2.0\%$** ($90/100$ vs $92/100$). Degradation is $\le 3.0\%$. $\to$ **MET**.
  - Overhead: $0.001$s latency, $0$ router tokens ($0.0\%$). $\to$ **MET**.

### Stopping-Rule Adjudication:
- **Decision**: **`STOP_ESCALATION_VALID`**.
- The heuristic routing tier completely satisfied all pre-registered criteria without violating the quality-loss tolerance.

---

## 2. Strict Bounding of Unexecuted Routing Tiers

- **WHAT WAS TESTED**: `STATIC_ROUTING`, `DETERMINISTIC_ROUTING`, `HEURISTIC_ROUTING` (and exploratory `LLM_ROUTER`).
- **WHAT WAS NOT NECESSARY TO EXECUTE**: `LEARNED_PUPPETEER_ROUTING` (and production deployment of LLM routers).
- **Canonical Classification**: `LEARNED_PUPPETEER_ROUTING` is classified strictly as **`NOT_TESTED_DUE_TO_STOPPING_RULE`**.
- **Prohibited Claims**: It is strictly forbidden to claim that learned Puppeteer routing is "inferior", "rejected", or "harmful."
- **Grounded Scientific Conclusion**:
  > *"Under the tested workload and preregistered thresholds, heuristic routing achieved sufficient quality while reducing resource use, so escalation to more complex routing mechanisms was not scientifically or economically justified."*
