# PX-15: Reproduction Synthesis
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `RESULT_ANALYSIS`  

---

## 1. Answers to the 10 Canonical Gate R3 Questions

1. **Which primitives reproduced?**
   - `PR-COG-01` (Memory Recency Decay with Tuned Weights), `PR-ORG-02` (Phase-Bounded SOPs), and `PR-ORG-03` (Dynamic Orchestration via Heuristics) successfully reproduced under controlled conditions.
2. **Which failed?**
   - Published equal-weighted retrieval ($\alpha=\beta=\gamma=1$) in `PR-COG-01` failed the success threshold ($\Delta \text{MRR} = +0.0446 < 0.05$), proving the necessity of dominant relevance weighting.
   - `DETERMINISTIC_ROUTING` in `PR-ORG-03` failed due to an unacceptable $10\%$ under-activation rate on complex tasks.
3. **Which were inconclusive or sub-threshold?**
   - `PR-ORG-01` (Multi-Agent Debate) is inconclusive on closed reasoning (`EQUIVALENCE_NOT_ESTABLISHED`, $p_{TOST} = 0.741$) and sub-threshold on private information ($+14.0\%$ gain, but $p = 0.0192 > 0.01$, classified as `PROMISING_BUT_NOT_SIGNIFICANT`).
4. **Which runs were invalid?**
   - Exactly zero runs were invalid. All 1,750 experimental episodes executed cleanly without API rate limits or data corruption.
5. **Which improvements survived compute normalization?**
   - Phase-bounded SOPs survived compute normalization, achieving $49.17\%$ token savings with $+6.15\%$ higher test pass rates.
   - Dynamic heuristic routing survived compute matching with $27.80\%$ token savings.
   - Multi-agent debate showed compute-matched trends, but failed statistical significance at $\alpha = 0.01$.
6. **Which mechanisms justify their added complexity?**
   - Elapsed-time exponential memory decay (replaces flawed inverted index with zero overhead).
   - Phase-bounded SOP state machines for task production workflows.
   - Multi-feature heuristic routing (achieves $27.80\%$ token savings with zero router calls).
7. **Which failure modes appeared?**
   - False consensus in multi-agent debate on closed reasoning ($8.2\%$ sycophancy rate).
   - Context accumulation blowout in unrestricted multi-agent conversation.
8. **Which architecture unknowns remain unresolved?**
   - True statistical surplus and scaling behavior of multi-agent debate (`U-02`).
   - Optimal reflection generation frequency under long-horizon simulation (`U-05`).
   - Information diffusion fidelity across 25+ agent social graphs (`U-06`).
9. **Which primitives deserve ablation in Phase 4?**
   - `PR-COG-01`: Ablation of decay rates ($\lambda$) and weight sensitivity ratios.
   - `PR-ORG-01`: High-powered ablation of debate across information asymmetry gradients.
   - `PR-ORG-02`: Factorial decomposition (roles vs phases).
   - `PR-ORG-03`: Feature importance pruning on heuristic routing.
10. **Which candidates should be rejected or deferred?**
    - `REJECT`: Unrestricted multi-agent chat for task workflows; equal-weighted memory retrieval.
    - `CLASSIFY AS NOT_TESTED_DUE_TO_STOPPING_RULE`: Learned neural routing / Puppeteer (stopping rule satisfied at Heuristic tier).
    - `DEFER`: 25+ agent social graph diffusion (deferred to Phase 8 scale testing).
