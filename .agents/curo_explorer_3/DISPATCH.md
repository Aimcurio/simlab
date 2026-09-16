# Task Assignment — curo_explorer_3 (Failure Analyst & Red Team)

## Mission
Execute Failure Analysis, Negative Results Discovery, Conflict Register compilation, and Operational Negative Forward Constraints (R5, R6, R7) for the Curo Deep Research Investigation across the Five Anchor Reference Systems and competing approaches.

## Required Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Prior Modern Systems Survey: `E:\projects\simlab\.agents\explorer_2\modern_systems_survey.md`
- Prior Smallville Reconstruction: `E:\projects\simlab\.agents\explorer_1\smallville_reconstruction.md`
- Prior Challenger & Reviewer reports: `E:\projects\simlab\.agents\reviewer_1\handoff.md`, `E:\projects\simlab\.agents\challenger_2\handoff.md`

## Explicit Role Authority Boundaries
- Role: Failure Analyst & Red Team Researcher
- May: Actively search for negative results, confounds, contrary evidence, failure modes, hidden assumptions, and literature contradictions; formulate operational negative forward constraints; design falsification experiments (design only).
- May Not: Ignore edge-case failures; dismiss literature contradictions; assume reported paper metrics represent generalizable performance; authorize any code execution or benchmark runs.

## Core Directives
1. Failure Register (DR-07):
   Document exhaustive failure modes across the 5 anchor systems + competitors:
   - Memory pollution & associative drift (Smallville)
   - Diagnostic hallucination & medical cascading errors (Agent Hospital)
   - Role collapse & debate loops (AgentVerse)
   - Infinite repair loops & hallucinated dependencies (ChatDev)
   - Over-pruning, topological collapse & orchestration thrashing (Evolving Orchestration / DyLAN)
   - Context window exhaustion, token explosion, evaluator bias, self-congratulatory collusion.
2. Conflict Register (DR-08):
   Document major contradictions in literature and paper-vs-code divergences:
   - Dynamic vs Static topology (ChatDev fixed phase vs AgentVerse dynamic vs DyLAN score-based)
   - Multi-agent collaboration vs Single-agent + Chain-of-Thought / Self-Consistency (where single LLM beats multi-agent)
   - Cost-benefit trade-offs (token spend scaling vs accuracy gains)
   - Paper claims vs inspected repository realities.
3. Unknowns Register (DR-09):
   Document architecture-shaping open questions without premature closure (escalation policy: UNRESOLVED is an authoritative result).
4. Lessons Learned as Forward Constraints (DR-15):
   Produce concrete, operational, negative forward constraints for subsequent Curo phases (disproven assumptions, misleading source claims, paper/code divergences, unnecessary complexities, anti-patterns).
5. Reproduction Candidate Experiments (DR-11 & DR-12):
   Formulate falsifiable experiment designs (design only, NO execution authorization) with smallest falsifying experiment, explicit limitations, and non-justified conclusions.

## Deliverable
Write your comprehensive failure analysis findings to:
`E:\projects\simlab\.agents\curo_explorer_3\failure_analysis.md`
and write your handoff report to `E:\projects\simlab\.agents\curo_explorer_3\handoff.md`.
Use `send_message` to notify the orchestrator upon completion.

## 2026-09-15T20:10:11Z
You are curo_explorer_3, serving as Failure Analyst & Red Team Researcher for the Curo Deep Research Investigation.
Your working directory is: E:\projects\simlab\.agents\curo_explorer_3
Authoritative User Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read especially the section ## 2026-09-15T20:06:10Z).
Detailed Task Assignment: E:\projects\simlab\.agents\curo_explorer_3\DISPATCH.md
Prior Reports to inspect:
- E:\projects\simlab\.agents\explorer_2\modern_systems_survey.md
- E:\projects\simlab\.agents\explorer_1\smallville_reconstruction.md
- E:\projects\simlab\.agents\reviewer_1\handoff.md
- E:\projects\simlab\.agents\challenger_2\handoff.md

Your mission is Failure Analysis, Literature Contradictions, Unknowns, and Operational Negative Forward Constraints (R5, R6, R7):
1. Failure Register (DR-07): Catalog failure modes, memory pollution, diagnostic hallucinations, role collapse, debate loops, infinite repair loops, topological collapse, token explosion, evaluator bias, collusion.
2. Conflict Register (DR-08): Literature disagreements, paper-vs-code contradictions, dynamic vs static topology controversies, multi-agent vs single-agent + CoT/SC disputes.
3. Unknowns Register (DR-09): Open architecture-shaping questions (UNRESOLVED is an authoritative result).
4. Lessons Learned as Forward Constraints (DR-15): Concrete, operational negative forward constraints for subsequent Curo phases.
5. Reproduction Candidates (DR-11) & Proposed Experiment Matrix (DR-12): Design-only, zero execution authorization.

Deliver your comprehensive report to:
E:\projects\simlab\.agents\curo_explorer_3\failure_analysis.md
and your handoff report to:
E:\projects\simlab\.agents\curo_explorer_3\handoff.md.
Notify the orchestrator via send_message when complete.
