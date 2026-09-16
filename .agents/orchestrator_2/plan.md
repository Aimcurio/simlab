# Plan — Curo Deep Research Investigation (Gate R1)

## Executive Objective
Execute the Curo Deep Research Investigation to build an unassailable evidence base across the Five Anchor Reference Systems (Smallville, Agent Hospital, AgentVerse, ChatDev, and Multi-Agent Collaboration via Evolving Orchestration) plus materially relevant competing approaches (MetaGPT, AutoGen, CAMEL, DyLAN, etc.). Deliver complete Tier 1 (DR-01–DR-10, DR-14–DR-16) and Tier 2 (DR-11–DR-13) deliverables, enforce strict evidence discipline, and conduct the Gate R1 evaluation.

## Governing Constraints & Boundaries
1. **Anti-Premature-Synthesis Invariant**: Evidence base only; no premature architecture selection; architecture remains UNFROZEN.
2. **Lifecycle & Authority**: Current state is `RESEARCH_AUTHORIZED`. `IMPLEMENTATION_AUTHORITY = NOT_GRANTED`. No code execution or simulation runtime building.
3. **Curo Boundary**: Curo governs specification, lifecycle, evidence discipline. Curo must NOT become the NPC brain, simulation runtime, memory substrate, or benchmark target.
4. **Schema Completeness**: All 26 schema fields in DR-05. Zero primitives with `VALIDATED` status. Permitted missing states: `UNKNOWN`, `NOT_REPORTED`, `NOT_MEASURED`, `NOT_APPLICABLE`, `UNRESOLVED`.
5. **Permitted Gate R1 Outcomes**: Strictly one of `CONTINUE_RESEARCH`, `INSUFFICIENT_EVIDENCE`, `READY_FOR_REPRODUCTION_DESIGN`.
6. **Baselines**: B0 (Deterministic), B1 (Single LLM), B2 (Multi-Independent LLM), B3 (Fixed-Role Multi-Agent), B4 (Adaptive Multi-Agent).

---

## Phases & Verifiable Milestones

### Phase 0: Survey & Repository Archaeology (Explorers / Spec Miners)
- **Agent curo_explorer_1 (Repository Archaeologist / Spec Miner)**:
  - Map the 5 anchor systems:
    1. Generative Agents / Smallville (`joonspk-research/generative_agents`)
    2. Agent Hospital (`LibertFan/AI_Hospital`)
    3. AgentVerse (`OpenBMB/AgentVerse`)
    4. ChatDev (`OpenBMB/ChatDev`)
    5. Multi-Agent Collaboration via Evolving Orchestration (DyLAN / dynamic orchestration literature & repos)
  - Historical version integrity: identify exact branches, tags, commit hashes, code file paths, line numbers.
  - Classify mechanisms: `DOCUMENTED_AND_IMPLEMENTED`, `DOCUMENTED_PARTIALLY_IMPLEMENTED`, `IMPLEMENTED_DIFFERENTLY`, `DOCUMENTED_NOT_FOUND`, `CODE_ONLY`, `VERSION_DEPENDENT`, `UNRESOLVED`.
- **Agent curo_explorer_2 (Researcher / Evidence Analyst)**:
  - Primitive extraction across Cognition, Organization, Communication, Learning, Simulation, and Governance.
  - Document all 26 fields per primitive candidate.
  - Record Mechanism/Model Confound Controls: foundation model version, prompts, context window, token spend, retrieval, sample sizes, run counts, seeds.
  - Baseline analysis against B0–B4.
- **Agent curo_explorer_3 (Failure Analyst / Red Team)**:
  - Deep dive on negative results, failure modes, literature contradictions, and edge cases.
  - Compile raw inputs for DR-07 (Failure Register), DR-08 (Conflict Register), and DR-09 (Unknowns Register).
  - Define operational negative forward constraints for DR-15.
  - Outline reproduction candidate experiments for DR-11 and DR-12 (design only).

### Phase 1: Deliverables Assembly (Workers)
- **Worker 1 & Worker 2**:
  - Author full Tier 1 deliverables:
    - DR-01: Research Corpus Ledger
    - DR-02: Source Authority Map
    - DR-03: System Architecture Profiles
    - DR-04: Paper <-> Code Mapping
    - DR-05: Primitive Evidence Matrix (all 26 fields per record, zero VALIDATED)
    - DR-06: System Comparison Matrix
    - DR-07: Failure Register
    - DR-08: Conflict Register
    - DR-09: Unknowns Register
    - DR-10: Candidate Baseline Matrix
    - DR-14: Research Synthesis
    - DR-15: Lessons Learned (Forward Constraints)
    - DR-16: Research Gate Package
  - Author Tier 2 deliverables (Provisional):
    - DR-11: Reproduction Candidate List
    - DR-12: Proposed Experiment Matrix
    - DR-13: Cost / Latency / Scaling Analysis
  - Deliverables stored in `E:\projects\simlab\deliverables\` and summarized in `E:\projects\simlab\curo_research_package.md`.

### Phase 2: Independent Review & Adversarial Challenge
- **Reviewer 1 & Reviewer 2**:
  - Reviewer 1: Audit DR-01 through DR-08 for claim normalization, citation integrity, schema conformance, and anti-premature synthesis.
  - Reviewer 2: Audit DR-09 through DR-16 for baseline rigor, negative forward constraints, and reproduction experiment boundaries.
- **Challenger 1 & Challenger 2**:
  - Challenger 1: Adversarial challenge to primitive claims, confound disentanglement, and baseline comparisons.
  - Challenger 2: Stress-test reproduction designs (DR-12) and forward constraints (DR-15).

### Phase 3: Forensic Audit & Gate R1 Evaluation
- **Forensic Auditor (`teamwork_preview_auditor`)**:
  - Systematic integrity check: anti-fabrication check on all 26 fields of DR-05, zero primitives with VALIDATED status, verification of code citations and line numbers, verification that UNRESOLVED is used where evidence is missing.
- **Gatekeeper Evaluation**:
  - Compile `GATE_STATUS.md`.
  - Check all Gate R1 criteria. Formulate formal Gate R1 decision strictly among permitted values (`CONTINUE_RESEARCH`, `INSUFFICIENT_EVIDENCE`, `READY_FOR_REPRODUCTION_DESIGN`).
  - Report complete package to parent Sentinel and human user.
