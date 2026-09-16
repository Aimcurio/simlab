# RD-02: Candidate-to-Unknown Mapping
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. Architectural Unknowns Register (Gate R1 Baseline)

Gate R1 established six primary architecture-shaping unknowns (`U-01` through `U-06`) recorded in `DR-09_unknowns_register.md`:
- **`U-01`**: Smallville Recency vs. Relevance Weighting Impact on Long-Horizon Coherence.
- **`U-02`**: Value of Multi-Agent Collaboration vs. Compute-Matched Single-Agent Baselines (`B1-SC`).
- **`U-03`**: Coordination Overhead vs. Error Suppression in Structured Phase Boundaries (ChatDev SOPs).
- **`U-04`**: Cost/Benefit Threshold for Dynamic Orchestration vs. Static Multi-Agent Topologies (`B3`).
- **`U-05`**: Optimal Reflection Frequency and Memory Growth Boundaries Under Long-Horizon Simulation.
- **`U-06`**: Information Diffusion Fidelity and Cascade Failures in 25+ Agent Social Graphs.

---

## 2. Direct Mapping Matrix

| Reproduction Candidate | Targeted Unknown | Specific Uncertainty Resolved | How the Experiment Informs SimLab Architecture | Permitted Inferences if Hypothesis Supported | Prohibited Overgeneralizations |
|---|---|---|---|---|---|
| **RP-01** | **U-01** | Does exponential temporal recency decay actually improve retrieval quality compared to no recency, linear recency, or inverted recency? | Determines whether SimLab's memory substrate requires a continuous recency scoring function or if cosine similarity + importance ranking is sufficient. | Supports implementing corrected exponential temporal decay in SimLab memory indexer. | Cannot justify claims about full agent social behavior, planning quality, or reflection dynamics. |
| **RP-02** | **U-02** | Under what specific task topologies (closed reasoning, shared-state, private info, asymmetric tools) does multi-agent debate outperform compute-matched single-agent `B1-SC`? | Directly governs when SimLab should deploy multi-agent debate vs. single-agent parallel sampling, preventing wasteful multi-agent overhead. | Identifies exact task boundaries where multi-agent architecture provides genuine collaborative surplus. | Cannot justify that multi-agent systems are universally superior or universally inferior. |
| **RP-03** | **U-03** | Does strict conversational phase-bounding (ChatDev SOPs) reduce hallucination cascades and duplicated work enough to offset the token coordination tax? | Informs SimLab's inter-agent communication layer: whether to enforce deterministic state-machine SOPs, free-form message buses, or hybrid channels. | Supports enforcing strict role-gated communication phases for collaborative production workflows. | Cannot infer optimal communication topology for open-ended social simulation or emergent dialogue. |
| **RP-04** | **U-04** | At what task complexity and agent count does dynamic agent activation outperform static topology (`B3`), and does LLM routing outperform simple heuristic routing? | Determines whether SimLab's runtime engine requires a dynamic meta-orchestrator or if deterministic static routing topologies should be standard. | Establishes the empirical threshold where dynamic routing earns its latency and token overhead. | Cannot justify deploying reinforcement-learned orchestrators without prior heuristic validation. |

---

## 3. Secondary & Long-Horizon Unknowns Coverage

- **`U-05` (Reflection Frequency & Memory Growth)**: Directly informed by `RP-01` retrieval baselines. Once retrieval mechanics are verified in `RP-01`, reflection ablation is scheduled for Phase 4.
- **`U-06` (Social Graph Diffusion Fidelity)**: Depends on both `RP-01` (memory retention) and `RP-03` (communication structure). Bounded to Phase 8 scale testing ($N \ge 25$) after foundational primitives are adjudicated.
