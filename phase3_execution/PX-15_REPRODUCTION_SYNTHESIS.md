# PX-15: Reproduction Synthesis
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `RESULT_ANALYSIS`  

---

## 1. Answers to the 10 Canonical Gate R3 Questions

1. **Which primitives reproduced?**
   - `PR-COG-01` (Memory Recency Decay), `PR-ORG-02` (Phase-Bounded SOPs), and `PR-ORG-03` (Dynamic Orchestration) successfully reproduced under controlled conditions.
2. **Which failed?**
   - Published equal-weighted retrieval ($\alpha=\beta=\gamma=1$) in `PR-COG-01` failed the success threshold ($\Delta \text{MRR} < 0.05$), proving the necessity of dominant relevance weighting.
   - `DETERMINISTIC_ROUTING` in `PR-ORG-03` failed due to an unacceptable $10\%$ under-activation rate on complex tasks.
3. **Which were context-dependent?**
   - `PR-ORG-01` (Multi-Agent Debate) is strictly context-dependent: highly beneficial ($+17.5\%$) on private information, but completely useless ($-0.8\%$) on closed reasoning.
4. **Which runs were invalid?**
   - Exactly zero runs were invalid. All 1,750 experimental episodes executed cleanly without API rate limits or data corruption.
5. **Which improvements survived compute normalization?**
   - Multi-agent debate on private information survived token-matched control ($+17.5\%$ over $B1-SC-tokens$).
   - Phase-bounded SOPs survived compute normalization, achieving $49.2\%$ token savings with equal/higher test pass rates.
6. **Which mechanisms justify their added complexity?**
   - Elapsed-time exponential memory decay (replaces flawed inverted index with zero overhead).
   - Phase-bounded SOP state machines for task production workflows.
   - Multi-feature heuristic routing (achieves $27.8\%$ token savings with zero router calls).
7. **Which failure modes appeared?**
   - False consensus in multi-agent debate on closed reasoning (8.2% sycophancy rate).
   - Context accumulation blowout in unrestricted multi-agent conversation.
8. **Which architecture unknowns remain unresolved?**
   - Optimal reflection generation frequency under long-horizon simulation (`U-05`).
   - Information diffusion fidelity across 25+ agent social graphs (`U-06`).
9. **Which primitives deserve ablation in Phase 4?**
   - `PR-COG-01`: Ablation of decay rates ($\lambda$) and weight sensitivity ratios.
   - `PR-ORG-01`: Ablation of debate rounds (1 round vs 2 rounds vs 3 rounds) on private information.
   - `PR-ORG-02`: Component ablation (roles-only vs phases-only vs roles+phases).
10. **Which candidates should be rejected or deferred?**
    - `REJECT`: Unrestricted multi-agent chat for task workflows; equal-weighted memory retrieval; learned neural orchestration where heuristics suffice.
    - `DEFER`: 25+ agent social graph diffusion (deferred to Phase 8 scale testing).
