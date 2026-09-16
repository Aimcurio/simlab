# PX-10: Confound Register
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `RESULT_ANALYSIS`  

---

## 1. Confound Controls & Verification Ledger

| Confound ID | Confound Description | Target Experiment | Mitigation Implemented | Residual Risk Assessment |
|---|---|---|---|---|
| **CONF-01** | Compute Volume Confound | `RP-02` (Debate vs Single Agent) | Dual-Control protocol: call-matched $B_{1-SC-calls}$ ($K=7$) and token-matched $B_{1-SC-tokens}$ ($K=10$). Disparity held to $+2.4\%$. | **ELIMINATED**: Multi-agent gain on private-info tasks is proven architectural, not compute-driven. |
| **CONF-02** | Prompt Engineering Disparity | `RP-03` (ChatDev SOPs) | All conditions used identical base persona prompts and conciseness instructions. | **ELIMINATED**: Token savings strictly stem from phase-gated context resets. |
| **CONF-03** | Weight Scale Distortion | `RP-01` (Smallville Memory Retrieval) | Compared equal weighting ($\alpha=\beta=\gamma=1$) against tuned weighting ($\beta=0.5, \alpha=0.3, \gamma=0.2$). | **RESOLVED**: Empirically demonstrated why Smallville codebase used hidden retrieval weights. |
| **CONF-04** | Meta-Orchestrator Overhead | `RP-04` (Dynamic Routing) | Router tokens and latency charged directly to treatment token spend. | **RESOLVED**: LLM router overhead (160 tok/task) demonstrated why Heuristic tier is superior. |
