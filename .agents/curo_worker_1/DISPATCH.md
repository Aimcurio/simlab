# Task Assignment — curo_worker_1 (Evidence & Primitive Deliverables Author)

## Mission
Author Tier 1 deliverables DR-01, DR-02, DR-03, DR-04, DR-05, DR-06, and DR-10 for the Curo Deep Research Investigation.

## Mandatory Reading & Inputs
- Authoritative User Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Explorer 1 Archaeology Report: `E:\projects\simlab\.agents\curo_explorer_1\archaeology_report.md`
- Explorer 2 Primitive Analysis Report: `E:\projects\simlab\.agents\curo_explorer_2\primitive_analysis.md`
- Explorer 3 Failure Analysis Report: `E:\projects\simlab\.agents\curo_explorer_3\failure_analysis.md`

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Lifecycle State & Authority Boundaries
- Current Lifecycle State: `RESEARCH_AUTHORIZED`
- Implementation Authority: `NOT_GRANTED` (Strict prohibition: no code writing, simulation runtime implementation, dependency installation, or benchmark execution).
- Core Invariant: RESEARCH_DESIGN != IMPLEMENTATION_AUTHORIZATION.

## Assigned Deliverables & Exclusively Owned Target Files
1. `E:\projects\simlab\deliverables\DR-01_research_corpus_ledger.md`:
   - Complete ledger of the 5 anchor systems + materially relevant competing approaches (MetaGPT, AutoGen, CAMEL, DyLAN, MemGPT/Letta, Concordia, AgentBench).
   - Inclusion rationale, paper metadata, author affiliations, publication venue/year.
2. `E:\projects\simlab\deliverables\DR-02_source_authority_map.md`:
   - Repository identity, official URLs, historical commit hashes, release tags, branches.
   - Conclusively map System 5 to `OpenBMB/ChatDev` branch `puppeteer` (commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a`).
   - Disambiguate Fan et al. `AI_Hospital` vs Zhang et al. `Agent Hospital`.
3. `E:\projects\simlab\deliverables\DR-03_system_architecture_profiles.md`:
   - Deep structural profiles of all 5 anchor systems + key competitors across layers: Environment, Agent Cognition, Organization, Governance, Simulation, Communication.
4. `E:\projects\simlab\deliverables\DR-04_paper_code_mapping.md`:
   - Paper claims vs inspected repository code with exact file paths and line numbers.
   - Classification: DOCUMENTED_AND_IMPLEMENTED, DOCUMENTED_PARTIALLY_IMPLEMENTED, IMPLEMENTED_DIFFERENTLY, DOCUMENTED_NOT_FOUND, CODE_ONLY, VERSION_DEPENDENT, UNRESOLVED.
   - Documented divergences (Smallville retrieval weights `gw=[0.5, 3, 2]` vs paper claims, rank decay vs game hours, unimplemented `# TODO` replanning, AI Hospital role fallback, ChatDev host subprocess execution).
5. `E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md`:
   - All 28 primitives extracted by Explorer 2 across Cognition, Organization, Communication, Learning, Simulation, Governance.
   - MUST contain all 26 schema fields per record.
   - Explicit states: UNKNOWN, NOT_REPORTED, NOT_MEASURED, NOT_APPLICABLE, UNRESOLVED for missing data. Zero synthetic guessing.
   - STRICT INVARIANT: ZERO primitives with `VALIDATED` status.
6. `E:\projects\simlab\deliverables\DR-06_system_comparison_matrix.md`:
   - Comprehensive cross-system comparison matrix across architectural mechanisms, model dependencies, execution models, and governance.
7. `E:\projects\simlab\deliverables\DR-10_candidate_baseline_matrix.md`:
   - Formal operational definitions of B0 (Deterministic), B1 (Single LLM), B2 (Multi-Independent LLM), B3 (Fixed-Role Multi-Agent), B4 (Adaptive).
   - Comparison matrix and task suitability boundaries.

## Deliverable Handoff
Author all 7 deliverable markdown files under `E:\projects\simlab\deliverables\`.
Write your handoff report to:
`E:\projects\simlab\.agents\curo_worker_1\handoff.md`.
Use `send_message` to notify the orchestrator when all files are authored.

## 2026-09-15T20:19:08Z
<USER_REQUEST>
You are curo_worker_1, serving as Primitive & Evidence Deliverables Author for the Curo Deep Research Investigation.
Working Directory: E:\projects\simlab\.agents\curo_worker_1
Authoritative User Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read especially the section ## 2026-09-15T20:06:10Z).
Detailed Task Assignment: E:\projects\simlab\.agents\curo_worker_1\DISPATCH.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Core Inputs:
- E:\projects\simlab\.agents\curo_explorer_1\archaeology_report.md
- E:\projects\simlab\.agents\curo_explorer_1\handoff.md
- E:\projects\simlab\.agents\curo_explorer_2\primitive_analysis.md
- E:\projects\simlab\.agents\curo_explorer_2\handoff.md
- E:\projects\simlab\.agents\curo_explorer_3\failure_analysis.md

Your exclusive authoring assignment:
1. E:\projects\simlab\deliverables\DR-01_research_corpus_ledger.md
2. E:\projects\simlab\deliverables\DR-02_source_authority_map.md
3. E:\projects\simlab\deliverables\DR-03_system_architecture_profiles.md
4. E:\projects\simlab\deliverables\DR-04_paper_code_mapping.md
5. E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md (All 28 primitives, all 26 fields, zero VALIDATED status!)
6. E:\projects\simlab\deliverables\DR-06_system_comparison_matrix.md
7. E:\projects\simlab\deliverables\DR-10_candidate_baseline_matrix.md

Write each file in publication-grade detail. Deliver your handoff report to:
E:\projects\simlab\.agents\curo_worker_1\handoff.md
and notify the orchestrator via send_message when complete.
</USER_REQUEST>

