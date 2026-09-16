# RD-03: Experimental Hypothesis Register
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. Governance & Falsification Discipline

Every reproduction candidate in SimLab Phase 2 must be anchored by a strictly falsifiable alternative hypothesis ($H_1$) paired with a precise null hypothesis ($H_0$). 
Experiments are structured to falsify $H_0$ only when empirical evidence exceeds pre-registered statistical and effect-size thresholds under compute-matched controls. If $H_0$ cannot be rejected, the candidate mechanism receives `NO_MEASURABLE_BENEFIT` or `HARMFUL`, which is treated as an authoritative, successful scientific finding.

---

## 2. Hypothesis Register

### RP-01: Smallville Memory Recency Retrieval
- **Research Question**: Does mathematically corrected temporal recency decay in simulation hours ($s_{rec} = 0.995^{\Delta t_{hours}}$) improve retrieval precision and rank correlation on a memory benchmark compared to (a) the historical rank-index inverted implementation (`retrieve.py:145-146`), (b) a no-recency baseline (`B0-NoRecency`, $\alpha=0, \beta=3.0, \gamma=2.0$), and (c) linear recency decay?
- **Alternative Hypothesis ($H_1$)**: Corrected exponential recency decay ($s_{rec} = 0.995^{\Delta t_{hours}}$, half-life $138.28$ hours; per-tick decay $0.995^{1/360} \approx 0.9999861$) with calibrated code weights ($\alpha=0.5, \beta=3.0, \gamma=2.0$) yields a statistically significant increase in Mean Reciprocal Rank (MRR $\ge +0.15$) and Normalized Discounted Cumulative Gain (NDCG@5 $\ge +0.18$) compared to both historical inverted and no-recency baselines ($p < 0.0025$, Paired Wilcoxon signed-rank test).
- **Null Hypothesis ($H_0$)**: Corrected exponential recency decay produces no statistically significant difference or worse retrieval quality ($\Delta \text{MRR} < +0.05$ or $p \ge 0.05$) compared to no-recency retrieval or simple linear decay.
- **Success Threshold**: MRR increase $\ge +0.15$ over both historical and no-recency baselines; NDCG@5 $\ge 0.82$ on recency-sensitive queries ($p < 0.0025$).
- **Failure Threshold**: MRR improvement $< +0.05$ over no-recency baseline ($p \ge 0.05$), or retrieval latency increases by $> 50\%$.
- **Inconclusive Threshold (`INCONCLUSIVE_SUB_THRESHOLD`)**: $\Delta \text{MRR} \in [+0.05, +0.15)$ over `B0-NoRecency`. Mandatory decision rule: Default to simpler baseline (`B0-NoRecency` plus a lightweight discrete FIFO recency buffer), rejecting continuous mathematical recency decay.

### RP-02: Compute-Matched Single vs Multi-Agent Debate
- **Research Question**: Under the Dual-Control Protocol ($B_{1-SC-calls}$ at $K=7$ and $B_{1-SC-tokens}$ at $K=10$), does multi-agent debate (`T-Debate`) outperform single-agent Self-Consistency on private-information and asymmetric tool tasks, while showing equivalence on closed-domain symbolic reasoning (GSM8K, $N=500$)?
- **Alternative Hypothesis ($H_1$)**: Multi-agent debate achieves $\ge +10\%$ higher task accuracy ($p < 0.01$, Binomial GLMM / McNemar) than compute-matched Dual-Control baselines on private-information and asymmetric tool tasks, but demonstrates statistical equivalence within an equivalence margin of $\pm 3\%$ ($\delta = 0.03$) on closed symbolic reasoning (GSM8K, $N=500$) under Two One-Sided Tests (TOST, $p_{TOST} < 0.05$, statistical power $\ge 80\%$).
- **Null Hypothesis ($H_0$)**: Compute-matched single-agent Dual Controls ($B_{1-SC-calls}$ and $B_{1-SC-tokens}$) equal or exceed multi-agent debate across all task categories ($p \ge 0.05$), or debate shows no advantage ($\Delta < +2\%$) on private-information tasks.
- **Success Threshold**: Multi-agent debate demonstrates $\ge +10\%$ accuracy advantage on private-information and tool-asymmetric tasks under matched compute, AND equivalence is confirmed on GSM8K within $[-0.03, +0.03]$ ($p_{TOST} < 0.05$).
- **Failure Threshold**: $B_{1-SC-tokens}$ matches or beats debate across all 4 categories ($p \ge 0.05$), or debate exhibits False Consensus Rate $> 20\%$.
- **Inconclusive Threshold (`INCONCLUSIVE_SUB_THRESHOLD`)**: Debate accuracy advantage on private-information tasks is in $[+2\%, +10\%)$, or the GSM8K $90\%$ CI crosses the $\pm 3\%$ margin. Mandatory decision rule: Default to simpler baseline (`B1` or `B1-SC-calls`), rejecting debate due to lack of demonstrated superiority under compute matching.

### RP-03: Structured Phase Boundaries / ChatDev SOPs
- **Research Question**: Does restricting inter-agent communication to formal, phase-bounded assembly-line state transitions (SOPs) reduce task defect rates and token expenditure compared to unrestricted multi-agent conversation (`Control B`) while solving $N=150$ modular and multi-file software engineering tasks?
- **Alternative Hypothesis ($H_1$)**: Structured phase boundaries (`T-PhaseSOP`) yield a $\ge 25\%$ reduction in token consumption and $\ge 25\%$ reduction in defect cycles ($p < 0.01$, Paired Wilcoxon) compared to unrestricted multi-agent chat on `SimLab-CodeSOP-150` (75 modular + 75 SWE-bench Lite mini multi-file tasks), while maintaining non-inferior unit test pass rates ($\Delta \text{Pass} \ge -3\%$, McNemar $p < 0.01$, power $\ge 80\%$).
- **Null Hypothesis ($H_0$)**: Structured phase boundaries produce no significant token reduction ($< 10\%$) or defect reduction, or induce rigid deadlocks reducing unit test pass rate by $> 10\%$ ($p < 0.01$).
- **Success Threshold**: $\ge 25\%$ token reduction and non-inferior test pass rate ($\Delta \text{Pass} \ge -3\%, p < 0.01$).
- **Failure Threshold**: Token reduction $< 10\%$, or test pass rate drops by $> 10\%$ due to state-transition failures.
- **Inconclusive Threshold (`INCONCLUSIVE_SUB_THRESHOLD`)**: Token reduction is in $[10\%, 25\%)$, or pass rate degradation is in $[-10\%, -3\%)$. Mandatory decision rule: Default to simpler baseline (`Control A` single agent or unconstrained shared channel), rejecting rigid phase-gated state machines.

### RP-04: Dynamic Orchestration / ChatDev:puppeteer
- **Research Question**: Does dynamic selective agent recruitment via an LLM or heuristic meta-orchestrator outperform a static fixed topology (`B3`) and compute-matched single-agent control (`B1-SC`) in task quality per token spend on a 300-task heterogeneous workload?
- **Alternative Hypothesis ($H_1$)**: Across `SimLab-HeteroBench-300` (120 simple, 90 moderate, 90 complex tasks; evaluated on a strictly held-out 70/30 test split), progressive routing escalation (`T-LLMRouter` and `T-Evolving`) achieves $\ge 95\%$ of fixed-topology `B3` task accuracy while reducing system token consumption by $\ge 25\%$ ($p < 0.01$), and achieves Pareto superiority over both `B0-Heuristic` and compute-matched `B1-SC` (evaluated via Cochran's Q test and post-hoc McNemar tests).
- **Null Hypothesis ($H_0$)**: Dynamic routing token overhead equals or exceeds token savings from skipped agent roles, or routing errors decrease task quality by $\ge 8\%$ compared to fixed topology `B3`.
- **Success Threshold**: Net token savings $\ge 25\%$ with task accuracy degradation $\le 3\%$ compared to `B3` on the held-out test split, and non-inferior accuracy compared to `B1-SC`.
- **Failure Threshold**: Net token savings $< 5\%$, or routing misclassifications cause Under-Activation Rate $> 10\%$ leading to task failures.
- **Inconclusive Threshold (`INCONCLUSIVE_SUB_THRESHOLD`)**: Net token savings is in $[5\%, 25\%)$ without statistically significant accuracy degradation, or accuracy degradation is in $[3\%, 8\%)$. Mandatory decision rule: Default to simpler baseline (`B0-Heuristic` or static `B1-SC` / `B3`), avoiding complex meta-orchestration.
