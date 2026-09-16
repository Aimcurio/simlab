# Task Assignment: Explorer 1 — Smallville Deconstruction & Substrate Evaluation

## Working Directory
`E:\projects\simlab\.agents\explorer_1`

## Authoritative Reference
`E:\projects\simlab\.agents\ORIGINAL_REQUEST.md`

## Mission & Requirements
Investigate and reconstruct the Stanford Generative Agents (Smallville) architecture, codebase, and substrate evaluation.
1. Reconstruct the Smallville architecture (Park et al. 2023, `joonspk-research/generative_agents`). Distinguish what the paper describes, what the codebase implements, what is inferred, and what later forks added.
   - World/environment, agent lifecycle, perception, associative memory stream & retrieval (recency, importance, relevance score formulas), reflection & tree of thought, hierarchical planning, dialogue, action selection, spatial representation (world-sector-arena-object tree), time progression (discrete ticks), persistence (storage/save states), frontend/backend boundaries (Django + Phaser), model/API dependencies (legacy OpenAI Completion API text-davinci-003, prompt engineering), configuration, and reproducibility characteristics.
   - Provide rich Mermaid diagrams mapping the architecture and data flows.
2. Evaluate Smallville as a Substrate with a comprehensive KEEP / WRAP / REFACTOR / REPLACE Matrix across all major subsystems:
   - Memory subsystem
   - Planning/reflection loop
   - Spatial/environment layer
   - Dialogue system
   - Persistence layer
   - API/model interface
   - Frontend/backend boundary
   - Time model
   Evaluate against lab requirements: old model/API coupling, observability limitations, scalability, reproducibility, deterministic control, prompt-driven behavior, hidden state, memory contamination, experiment repeatability, testability, and modularity.
3. Compare Refactor Strategies (R8):
   - Strategy A: Fork and incrementally refactor Stanford Smallville
   - Strategy B: Use a modern Smallville-compatible fork as foundation
   - Strategy C: Rebuild cleanly while preserving Smallville concepts
   Evaluate across 10 dimensions: engineering effort, technical debt, research validity, maintainability, extensibility, observability, testability, reproducibility, model portability, future scaling. Deliver a definitive recommendation with rationale.

## Output Deliverable
Write your exhaustive investigation report to `E:\projects\simlab\.agents\explorer_1\smallville_reconstruction.md` and your handoff to `E:\projects\simlab\.agents\explorer_1\handoff.md`.
Classify every claim explicitly as FACT, INFERENCE, PROPOSAL, or OPEN QUESTION with academic and codebase citations.
