# Task Assignment — curo_explorer_2 (Primitive Analyst & Evidence Modeler)

## Mission
Execute Primitive Extraction Protocol (R2), Mechanism/Model Confound Control (R3), and Baseline Discipline (R4) for the Curo Deep Research Investigation across the Five Anchor Reference Systems plus key competitors (MetaGPT, AutoGen, CAMEL, DyLAN, etc.).

## Required Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Prior Modern Systems Survey: `E:\projects\simlab\.agents\explorer_2\modern_systems_survey.md`
- Prior Smallville Reconstruction: `E:\projects\simlab\.agents\explorer_1\smallville_reconstruction.md`

## Explicit Role Authority Boundaries
- Role: Evidence Analyst & Primitive Researcher
- May: Decompose systems into candidate primitives; extract all 26 schema fields; normalize claims; assign evidence classes; assess evidence strength; document confound controls and baselines.
- May Not: Convert INFERRED claims into architectural requirements; assign VALIDATED status to any primitive; fabricate or guess values for missing data (use explicit UNKNOWN, NOT_REPORTED, NOT_MEASURED, NOT_APPLICABLE, or UNRESOLVED).

## Core Directives
1. Deconstruct candidate primitives across 6 functional categories:
   - Cognition (memory stream, reflection, planning, self-refinement, etc.)
   - Organization (hierarchical dispatch, role-based SOPs, dynamic recruitment, evolving topology, etc.)
   - Communication (structured dialogue, debate, publish-subscribe, broadcast, blackboard)
   - Learning (cross-episode memory, experience accumulation, case-based doctor learning)
   - Simulation (spatial grid, discrete tick event loops, environmental affords)
   - Governance (deterministic rule checking, static schema gates, capability boundaries)
2. Every primitive MUST contain all 26 required schema fields:
   1. primitive_id
   2. primitive_name
   3. source_system
   4. source_version
   5. category
   6. mechanism_description
   7. claimed_purpose
   8. claimed_benefit
   9. measured_benefit
   10. evidence_type
   11. evidence_strength
   12. dependencies
   13. runtime_cost
   14. token_cost
   15. latency_effect
   16. scaling_effect
   17. known_failure_modes
   18. known_limitations
   19. negative_evidence
   20. transferability_hypothesis
   21. reproduction_required
   22. proposed_control
   23. proposed_metric
   24. reproducibility_status (NOT_ASSESSED, AUTHOR_REPORTED, CODE_AVAILABLE, PARTIALLY_REPRODUCED, INDEPENDENTLY_REPRODUCED, FAILED_REPRODUCTION, UNRESOLVED)
   25. confidence
   26. status (PROPOSED, REPRODUCTION_CANDIDATE, PROMISING_BUT_UNVERIFIED, CONTEXT_DEPENDENT, INSUFFICIENT_EVIDENCE, REJECTED. NO VALIDATED!)
3. Mechanism / Model Confound Control (R3):
   Record foundation model family, exact version, context window, token budget/spend, prompt templates, retrieval mechanism, sample sizes, run counts, random seeds. Disentangle mechanism improvement from model capability/compute.
4. Baseline Discipline (R4):
   Map mechanisms against B0 (Deterministic), B1 (Single LLM), B2 (Multi-Independent LLM), B3 (Fixed-Role Multi-Agent), B4 (Adaptive).

## Deliverable
Write your comprehensive evidence findings to:
`E:\projects\simlab\.agents\curo_explorer_2\primitive_analysis.md`
and write your handoff report to `E:\projects\simlab\.agents\curo_explorer_2\handoff.md`.

## 2026-09-15T20:10:11Z
You are curo_explorer_2, serving as Primitive Analyst & Evidence Modeler for the Curo Deep Research Investigation.
Your working directory is: E:\projects\simlab\.agents\curo_explorer_2
Authoritative User Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read especially the section ## 2026-09-15T20:06:10Z).
Detailed Task Assignment: E:\projects\simlab\.agents\curo_explorer_2\DISPATCH.md
Prior Reports to inspect:
- E:\projects\simlab\.agents\explorer_2\modern_systems_survey.md
- E:\projects\simlab\.agents\explorer_1\smallville_reconstruction.md

Your mission is Primitive Extraction Protocol (R2), Confound Control (R3), and Baseline Discipline (R4) across the 5 anchor systems + competing approaches (MetaGPT, AutoGen, CAMEL, etc.):
1. Extract candidate primitives across Cognition, Organization, Communication, Learning, Simulation, Governance.
2. Every primitive MUST contain all 26 schema fields (DR-05). Explicitly use UNKNOWN, NOT_REPORTED, NOT_MEASURED, NOT_APPLICABLE, UNRESOLVED where data is absent. ZERO primitives may receive VALIDATED status.
3. Mechanism/Model Confound Control: Record model family, exact version, context window, token budget/spend, prompt templates, retrieval, sample sizes, run counts, seeds.
4. Baseline Discipline: Map mechanisms against B0, B1, B2, B3, B4.

Deliver your comprehensive report to:
E:\projects\simlab\.agents\curo_explorer_2\primitive_analysis.md
and your handoff report to:
E:\projects\simlab\.agents\curo_explorer_2\handoff.md.
Notify the orchestrator via send_message when complete.
