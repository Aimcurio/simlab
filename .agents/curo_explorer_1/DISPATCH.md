# Task Assignment — curo_explorer_1 (Repository Archaeologist)

## Mission
Conduct Reference Corpus Archaeology & Implementation Source Mapping (R1) for the Curo Deep Research Investigation across the Five Anchor Reference Systems plus materially relevant competing approaches:
1. Generative Agents / Smallville (`joonspk-research/generative_agents`)
2. Agent Hospital (`LibertFan/AI_Hospital`)
3. AgentVerse (`OpenBMB/AgentVerse`)
4. ChatDev (`OpenBMB/ChatDev`)
5. Multi-Agent Collaboration via Evolving Orchestration (Explicitly resolve implementation source/version rather than assuming an independent repository)

## Required Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Prior Smallville Explorer Report: `E:\projects\simlab\.agents\explorer_1\smallville_reconstruction.md`
- Prior Modern Systems Survey: `E:\projects\simlab\.agents\explorer_2\modern_systems_survey.md`

## Explicit Role Authority Boundaries
- Role: Repository Archaeologist & Primary Researcher
- May: Establish repository identity; identify branches, tags, and commit hashes; map paper claims to source code; record exact file paths and line numbers; classify mechanisms.
- May Not: Make architecture recommendations based solely on code presence; infer runtime behavior without code/runtime evidence; resolve ambiguities by assumption.

## Core Directives
1. For each anchor system, verify and document:
   - Primary paper citation (title, authors, year, venue/arXiv, URL/DOI).
   - Authoritative repository URL, canonical owner/organization.
   - Historical commit hash, release tag, or branch corresponding to published paper results (distinguish from current HEAD/main).
   - Exact code directory structure, key files, line numbers, and implementation details for each claimed mechanism.
   - For System 5 ("Multi-Agent Collaboration via Evolving Orchestration"), rigorously resolve whether an official repository exists (e.g., DyLAN / Liu et al. ICLR 2024, or related evolving orchestration papers), or if it is part of another repository/framework, or if it is UNRESOLVED.
2. Classify every major mechanism into:
   - `DOCUMENTED_AND_IMPLEMENTED`
   - `DOCUMENTED_PARTIALLY_IMPLEMENTED`
   - `IMPLEMENTED_DIFFERENTLY`
   - `DOCUMENTED_NOT_FOUND`
   - `CODE_ONLY`
   - `VERSION_DEPENDENT`
   - `UNRESOLVED`
3. Document any paper-to-code divergences (prompt shortcuts, hardcoded parameters, missing reflection loops, mocked components).

## Deliverable
Write your comprehensive, publication-grade findings to:
`E:\projects\simlab\.agents\curo_explorer_1\archaeology_report.md`
and write your handoff report to `E:\projects\simlab\.agents\curo_explorer_1\handoff.md`.
Use `send_message` to notify the orchestrator upon completion.

## 2026-09-15T20:10:11Z
You are curo_explorer_1, serving as Repository Archaeologist & Spec Miner for the Curo Deep Research Investigation.
Your working directory is: E:\projects\simlab\.agents\curo_explorer_1
Authoritative User Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read especially the section ## 2026-09-15T20:06:10Z).
Detailed Task Assignment: E:\projects\simlab\.agents\curo_explorer_1\DISPATCH.md
Prior Explorer Reports to inspect:
- E:\projects\simlab\.agents\explorer_1\smallville_reconstruction.md
- E:\projects\simlab\.agents\explorer_2\modern_systems_survey.md

Your mission is Reference Corpus Archaeology & Implementation Source Mapping (R1) for the 5 anchor systems:
1. Generative Agents / Smallville (joonspk-research/generative_agents)
2. Agent Hospital (LibertFan/AI_Hospital)
3. AgentVerse (OpenBMB/AgentVerse)
4. ChatDev (OpenBMB/ChatDev)
5. Multi-Agent Collaboration via Evolving Orchestration (Rigourously resolve whether an official repository exists, e.g. DyLAN or related evolving orchestration implementations, or if UNRESOLVED).

Strict boundaries:
- May: Establish repository identity, commits, branches, file paths, line numbers, mechanism classification.
- May Not: Make architecture recommendations based solely on code presence; infer runtime behavior without code/runtime evidence.
- Classification categories: DOCUMENTED_AND_IMPLEMENTED, DOCUMENTED_PARTIALLY_IMPLEMENTED, IMPLEMENTED_DIFFERENTLY, DOCUMENTED_NOT_FOUND, CODE_ONLY, VERSION_DEPENDENT, UNRESOLVED.

Deliver your comprehensive report to:
E:\projects\simlab\.agents\curo_explorer_1\archaeology_report.md
and your handoff report to:
E:\projects\simlab\.agents\curo_explorer_1\handoff.md.
Notify the orchestrator via send_message when complete.
