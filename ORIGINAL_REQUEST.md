# Original User Request

## 2026-09-07T21:00:03Z

A deep technical research and architecture investigation to determine whether Stanford Smallville is the right substrate for a controlled multi-agent experimentation laboratory, and to produce a complete design package for a reusable Agent Simulation Lab.

Working directory: E:\projects\simlab

## Source Access
The research team may access:
- GitHub repositories (read-only code inspection)
- arXiv and peer-reviewed papers
- Official project documentation and READMEs

Do not rely on marketing material, unsourced blog commentary, or unverified demonstrations.

---

## Requirements

### R1. Reconstruct the Original Smallville Architecture
Produce an authoritative architecture reconstruction of Stanford Generative Agents / Smallville, clearly distinguishing between what the paper describes, what the codebase implements, what is inferred, and what later forks added. Include: world/environment, agent lifecycle, perception, memory, retrieval, reflection, planning, dialogue, action selection, spatial representation, time progression, persistence, frontend/backend boundaries, model/API dependencies, configuration, and reproducibility characteristics. Produce a structured architecture map or diagram.

### R2. Evaluate Smallville as a Substrate and Produce a KEEP/WRAP/REFACTOR/REPLACE Matrix
Analyze Smallville's architectural strengths and weaknesses specifically as a foundation for the proposed Agent Simulation Lab. Produce a matrix covering all major subsystems. Pay particular attention to: old model/API coupling, observability limitations, scalability, reproducibility, deterministic control, prompt-driven behavior, hidden state, memory contamination, experiment repeatability, testability, and modularity.

### R3. Survey Modern Successors, Forks, and Related Systems
Research projects released after or influenced by Generative Agents / Smallville, spanning: multi-agent simulation, social agent environments, agent benchmarks, LLM-based societies, multi-agent software engineering, RL environments, organizational simulations, role-based agent frameworks, local-model recreations, and agent memory systems. For each: identify what problem it solves, what it improved over Smallville, what design ideas are worth borrowing, what should not be copied, and whether its implementation is reusable. Produce a comparison matrix.

### R4. Design the Target Agent Simulation Lab Architecture
Propose a target architecture with clearly separated concerns: (A) Environment Layer, (B) Agent Cognition Layer, (C) Organizational Layer (roles, teams, hierarchy, objectives, responsibilities, resources, delegation, reporting), (D) Authority/Governance Layer (MAY/MUST/CANNOT rules that do NOT rely solely on prompt instructions — explain how enforcement technically works), (E) Experiment Harness (reproducible scenario definitions as data), (F) Fault Injection Layer, (G) Critic/Reviewer Loop (independent critic pattern with preserved independence), (H) Observability/Event Layer (structured raw events independent of LLM summaries), (I) Analysis/Observatory Layer.

### R5. Research and Specify the Metrics Framework
For every proposed metric (task completion rate, solution quality, time to completion, token usage, communication volume, delegation accuracy, unauthorized-action rate, escalation rate, reviewer catch rate, rework, failure recovery time, robustness, evidence completeness, human intervention rate, and others found in current research): explain what it measures, why it matters, how it is calculated, whether it is deterministic or model-judged, how it could be gamed, and what safeguards are needed.

### R6. Threat-Model the Experimental Platform
Perform a serious failure-mode analysis covering: agents gaming metrics, critic collusion, evaluator bias, prompt leakage, memory contamination, hallucinated authority, role drift, self-approval, communication loops, runaway token usage, experiment cross-contamination, model/version invalidation, non-reproducibility, insufficient sample sizes, hidden environmental state, incomplete event capture, and overclaiming results. For each: description, severity, likelihood, detectability, mitigation, and whether prevention should be deterministic or probabilistic.

### R7. Investigate Reproducibility Limits
Research what reproducibility can realistically mean for LLM-driven agents. Distinguish between: exact replay, state replay, configuration replay, statistically comparable reruns, deterministic environment replay, and nondeterministic cognition replay. Recommend which parameters must be captured with every experiment run. Do not claim deterministic reproducibility where it is impossible.

### R8. Compare Refactor Strategies and Give a Recommendation
Evaluate at least three approaches: (A) Fork and incrementally refactor Stanford Smallville, (B) Use a modern Smallville-compatible fork as foundation, (C) Rebuild cleanly while preserving Smallville concepts. For each: engineering effort, technical debt, research validity, maintainability, extensibility, observability, testability, reproducibility, model portability, future scaling. Give a final recommendation.

### R9. Propose a Phased Implementation Roadmap
Define milestones M0–M6: M0 Baseline Reproduced, M1 Instrumented, M2 Governed, M3 Experimentable, M4 Comparable, M5 Adversarial, M6 Research Lab. For each milestone: required capabilities, acceptance criteria, tests, evidence artifacts, dependencies, major risks.

### R10. Design Three Initial Experiments
At least one comparing centralized coordinator vs decentralized agent teams. At least one comparing builder-only vs builder + independent critic. At least one involving injected misinformation or controlled failure. For each: hypothesis, independent variable, dependent variables, controls, scenario, number of runs, metrics, expected failure modes, evidence needed, and what conclusions would and would not be justified.

---

## Evidence Discipline

Every significant conclusion must be classified explicitly as one of:
- **FACT** — directly supported by authoritative sources or inspected code
- **INFERENCE** — reasonable conclusion derived from evidence
- **PROPOSAL** — recommended design choice not yet validated
- **OPEN QUESTION** — requires implementation, experimentation, or requester decision

Prefer: primary research papers, official repositories, source code, official documentation, peer-reviewed papers, reputable technical publications. Where sources disagree, explain the disagreement. Use citations throughout.

---

## Acceptance Criteria

### Research Quality
- [ ] Smallville architecture reconstruction cites the original paper (Park et al. 2023) and inspects actual codebase — not described from memory
- [ ] KEEP/WRAP/REFACTOR/REPLACE matrix covers at minimum: memory subsystem, planning/reflection loop, spatial/environment layer, dialogue system, persistence layer, API/model interface, frontend/backend boundary, time model
- [ ] Modern systems survey covers at minimum 8 distinct projects across at least 4 categories (simulation, benchmarking, software-engineering agents, memory systems)
- [ ] Every claim is labeled FACT / INFERENCE / PROPOSAL / OPEN QUESTION

### Architecture Completeness
- [ ] Target architecture explicitly specifies how authority/governance enforcement works technically (not just "via prompt")
- [ ] Experiment harness specification is detailed enough that a developer could begin implementation from it
- [ ] Fault injection layer proposes at least 6 distinct injection mechanisms with technical implementation notes
- [ ] Observability event model defines a concrete schema (fields, types, event categories) for structured event capture

### Metrics Rigor
- [ ] At least 12 distinct metrics specified with full analysis (measurement method, gaming risk, safeguard)
- [ ] Every metric is clearly labeled as deterministic or model-judged
- [ ] At least one metric addresses critic/reviewer independence specifically

### Threat Model Depth
- [ ] At least 15 failure modes analyzed
- [ ] Every failure mode includes severity, likelihood, detectability, mitigation
- [ ] At least 5 failure modes have deterministic prevention mechanisms specified

### Reproducibility Honesty
- [ ] Reproducibility section explicitly states what cannot be made deterministic and why
- [ ] Parameter capture list is complete and operational (could be checked off before each run)

### Experimental Design Rigor
- [ ] All three experiments have explicit hypotheses, independent variables, dependent variables, and controls
- [ ] Each experiment defines a minimum number of runs with justification
- [ ] Each experiment explicitly states what conclusions would NOT be justified from the results

### Output Completeness
- [ ] Final document includes all 18 required sections (executive verdict through sources)
- [ ] Sources section includes at minimum 15 cited works with full references

---

## Required Output Structure

The research package must contain:
1. Executive verdict
2. Smallville architecture reconstruction
3. Strengths and weaknesses
4. KEEP / WRAP / REFACTOR / REPLACE matrix
5. Modern successor/fork comparison
6. Recommended target architecture
7. Organizational and governance model
8. Experiment-harness specification
9. Observability/event model
10. Metrics specification
11. Threat model
12. Reproducibility strategy
13. Refactor strategy comparison
14. Recommended implementation roadmap
15. First three experimental designs
16. Open architectural decisions
17. Research gaps
18. Sources

## Delivery Format

The research package must be delivered as a **single comprehensive Markdown document** saved to the working directory (E:\projects\simlab\research_package.md), with:
- Embedded Mermaid diagrams for architecture maps
- Markdown tables for matrices and comparisons
- Inline citations throughout (not just a bibliography at the end)
- All 18 required output sections in order

## 2026-09-15T20:06:10Z

<USER_REQUEST>
Curo Deep Research Investigation: Primitive Discovery, Failure Analysis, and Architecture Evidence Base using Five Anchor Reference Systems Plus Materially Relevant Competing Approaches

Working directory: E:\projects\simlab
Integrity mode: benchmark

================================================================================
1. GOVERNING RESEARCH PRINCIPLE & MISSION
================================================================================

Anti-Premature-Synthesis Invariant:
The objective of this research phase is not to select or justify a pre-existing multi-agent architecture. It is to construct an evidence base from which our own architecture may later emerge. Reference systems are to be decomposed into candidate primitives, claims are to be checked against implementation evidence where possible, failures and contradictions receive equal standing with positive results, and no primitive advances solely because it is novel, popular, elegant, recent, or present in multiple papers. Architecture synthesis remains out of scope until candidate primitives survive later reproduction, baseline comparison, ablation, and controlled experimentation.

Anchor Corpus & Search Boundaries:
The five named systems (Generative Agents / Smallville, Agent Hospital, AgentVerse, ChatDev, and Multi-Agent Collaboration via Evolving Orchestration) serve as the authoritative anchor corpus, not the exhaustive search boundary. Additional primary sources may be added when they introduce a competing mechanism, stronger evidence, independent reproduction, contradictory result, or materially newer approach. Every added source must be entered into DR-01 with an explicit inclusion rationale. Uncontrolled literature sprawl is forbidden: every new source must materially affect at least one research question, primitive candidate, failure mode, baseline, conflict, or unknown.

================================================================================
2. CURO LIFECYCLE & AUTHORITY BOUNDARY
================================================================================

Lifecycle Progression:
PLANNING -> RESEARCH_DESIGN -> REQUESTER_APPROVAL -> RESEARCH_AUTHORIZED -> RESEARCHING -> RESEARCH_REVIEW -> GATE_R1

- Current Lifecycle State: RESEARCH_AUTHORIZED
- Implementation Authority: NOT_GRANTED
- Architecture Status: UNFROZEN
- Core Invariant: RESEARCH_DESIGN != IMPLEMENTATION_AUTHORIZATION

Permitted Gate R1 Outcomes:
Gate R1 may output strictly one of the following decisions:
1. CONTINUE_RESEARCH
2. INSUFFICIENT_EVIDENCE
3. READY_FOR_REPRODUCTION_DESIGN

Gate R1 does not and cannot authorize controlled experiments or implementation. Reproduction design and experiment execution belong to later, separately authorized phases that require explicit, independent requester approval before work begins.

Curo Boundary Invariant:
Curo governs specification, authority, lifecycle, evidence discipline, validation, provenance, escalation, deterministic state transitions, approvals, and lessons learned.
Curo must NOT become:
- The NPC cognition engine / brain;
- The simulation runtime engine;
- The agent memory substrate;
- The orchestration algorithm under evaluation;
- The game/virtual environment;
- The benchmark target.

If any proposed architecture causes Curo itself to become part of the mechanism being experimentally compared, it must be flagged as a severe experimental confound.

================================================================================
3. EXPLICIT ROLE AUTHORITY BOUNDARIES
================================================================================

To prevent role bleed, self-certification, and ungrounded assumptions, team members must operate strictly within their defined authority:

- Researcher:
  May: Discover primary sources; summarize evidence; identify candidate primitives; propose falsifiable hypotheses.
  May Not: Approve architecture; resolve conflicts by assumption; authorize implementation.

- Repository Archaeologist:
  May: Establish repository identity; identify branches, tags, and commit hashes; map paper claims to source code; record exact file paths and line numbers.
  May Not: Make architecture recommendations based solely on code presence; infer runtime behavior without code/runtime evidence.

- Evidence Analyst:
  May: Normalize claims; assign evidence classes; assess evidence strength; maintain evidence matrices and audit ledgers.
  May Not: Convert INFERRED claims into architectural requirements; silently resolve contradictory evidence.

- Failure Analyst / Red Team:
  May: Actively search for negative results, confounds, contrary evidence, failure modes, and hidden assumptions; disconfirm dominant interpretations.
  May Not: Ignore edge-case failures; dismiss literature contradictions; assume reported paper metrics represent generalizable performance.

- Research Reviewer:
  Must: Independently challenge synthesis, primitive rankings, unsupported cognitive leaps, and proposed reproduction candidates.
  Boundary: Must be strictly independent of the agent who authored the primary synthesis. Cannot rubber-stamp unverified claims.

- Curo Gatekeeper:
  May: Verify lifecycle state transitions, evidence discipline, schema completeness, and whether Gate R1 criteria are met.
  May Not: Substitute missing evidence; act as technical adjudicator on substantive claims; authorize implementation without requester approval.

- Requester (Human Authority):
  Sole authority to approve scope expansion, advance past Gate R1, authorize reproduction design, authorize implementation, or freeze architecture.

================================================================================
4. RESEARCH REQUIREMENTS
================================================================================

R1. Reference Corpus Archaeology & Implementation Source Mapping
Map each of the five anchor reference systems to its authoritative implementation source where one can be verified:
1. Generative Agents / Smallville (joonspk-research/generative_agents)
2. Agent Hospital (LibertFan/AI_Hospital)
3. AgentVerse (OpenBMB / dynamic recruitment)
4. ChatDev (OpenBMB/ChatDev)
5. Multi-Agent Collaboration via Evolving Orchestration (Explicitly resolve implementation source/version rather than assuming an independent repository)

Repository & Version Rules:
- If an authoritative implementation repository, branch, tag, or commit can be verified, record it.
- Historical Version Integrity: The historically relevant implementation version must be preferred over current main when determining what code corresponds to the published results. Current implementations may be analyzed separately but must not be silently substituted for the evaluated historical implementation.
- If the implementation is located within another repository, branch, or monorepo package, record that explicitly.
- If no authoritative implementation can be established, classify the implementation evidence as UNRESOLVED and record the gap.
- Do not substitute an unofficial, third-party implementation merely to satisfy completeness.
- Classify every mechanism under: DOCUMENTED_AND_IMPLEMENTED, DOCUMENTED_PARTIALLY_IMPLEMENTED, IMPLEMENTED_DIFFERENTLY, DOCUMENTED_NOT_FOUND, CODE_ONLY, VERSION_DEPENDENT, or UNRESOLVED.

R2. Primitive Extraction Protocol (DR-05)
Decompose systems into candidate primitives across: Cognition, Organization, Communication, Learning, Simulation, and Governance.

Schema Discipline & Anti-Fabrication Rule:
Every Primitive Evidence Record must contain all 26 required schema fields:
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
24. reproducibility_status
25. confidence
26. status

Field Presence vs. Value Integrity: Every field must be present. Where evidence is unavailable or not reported in the primary literature, explicit states must be used: UNKNOWN, NOT_REPORTED, NOT_MEASURED, NOT_APPLICABLE, or UNRESOLVED.
Reproducibility Status Values: Permitted values for reproducibility_status are:
NOT_ASSESSED, AUTHOR_REPORTED, CODE_AVAILABLE, PARTIALLY_REPRODUCED, INDEPENDENTLY_REPRODUCED, FAILED_REPRODUCTION, or UNRESOLVED.
Prohibited Inferences: Never fabricate or guess values for token_cost, runtime_cost, latency_effect, scaling_effect, reproducibility_status, or measured_benefit.
Permitted Status Values: PROPOSED, REPRODUCTION_CANDIDATE, PROMISING_BUT_UNVERIFIED, CONTEXT_DEPENDENT, INSUFFICIENT_EVIDENCE, REJECTED.
No primitive may receive VALIDATED status during literature research alone.

R3. Mechanism / Model Confound Control
To prevent attributing foundation model capabilities or high compute to architectural mechanisms, every major comparative claim must record:
- Foundation model family, exact version, and parameter scale;
- Prompt strategy, template structure, and temperature;
- Context window allocation and memory pruning;
- Number of inference calls and total token budget / spend;
- Available tools and environment observation bandwidth;
- Retrieval mechanism, sample sizes, run counts, random seeds, and stopping criteria.
The team must explicitly distinguish improvements caused by architecture/mechanisms from improvements caused by stronger models, larger context, more inference calls, or higher token budgets. If the confound cannot be cleanly separated from the text/code, classify the claim accordingly.

R4. Baseline Discipline (DR-10)
Multi-agent and adaptive systems must not be compared solely against one another. Every mechanism must be evaluated against the simplest relevant baseline:
- B0: Deterministic Agent (rule-based / state machine, zero LLM reasoning)
- B1: Single LLM Agent (zero multi-agent collaboration)
- B2: Multiple Independent LLM Agents (shared environment, no orchestrated collaboration)
- B3: Fixed-Role Multi-Agent System (static topology and hand-assigned roles)
- B4: Candidate Adaptive System (dynamic recruitment, evolving orchestration, or dynamic memory)
Explicitly guard against cognitive biases: "more agents = better", "more communication = better", "more reflection = better", "more memory = better", or "higher token spend = architectural improvement".

R5. Research Escalation Policy
When evidence is ambiguous or contradictory, the team must escalate rather than force a conclusion.
Mandatory Escalation Triggers:
- Authoritative paper and repository implementation materially conflict;
- Historical commit/tag/branch cannot be established with reasonable confidence;
- A mechanism cannot be disentangled from underlying model capability;
- Benchmark artifacts are missing or unreproducible;
- Resolving an evidence question would require executing code while IMPLEMENTATION_AUTHORITY = NOT_GRANTED;
- A substantive claim depends primarily on secondary sources;
- Literature contains materially contradictory results;
- A newly discovered system materially alters the multi-agent design space;
- Cost, latency, or scaling claims cannot be supported by available evidence.
Permitted Escalation Resolution States: RESOLVED, PARTIALLY_RESOLVED, UNRESOLVED, INSUFFICIENT_EVIDENCE.
Core Rule: UNRESOLVED is an authoritative, valid scientific research result. No researcher may spin loops to force certainty.

R6. Reproduction Experiment Design Boundaries (DR-11 & DR-12)
DR-11 (Reproduction Candidates) and DR-12 (Proposed Experiment Matrix) are research design documents only.
Strict Prohibition: They do NOT authorize coding, simulator implementation, repository modification, dependency installation, environment setup, benchmark execution, model API calls for experiments, controlled runs, or performance testing.
Every proposed experiment in DR-12 must explicitly state:
- The smallest experiment capable of falsifying the hypothesis;
- What the experiment could demonstrate vs. what it could not demonstrate;
- External validity limitations;
- Model-specific and environment-specific limitations;
- Unresolved confounds.

R7. Lessons Learned as Forward Constraints (DR-15)
DR-15 must not be a generic narrative retrospective. It must deliver concrete, operational forward constraints for subsequent Curo phases:
- Disproven assumptions;
- Misleading source claims;
- Paper/code divergences;
- Failed research approaches and measurement pitfalls;
- Unnecessary complexities and token/cost traps;
- Explicit negative constraints that future agents and phases must strictly follow.

================================================================================
5. EVIDENCE CLASSIFICATION SYSTEM
================================================================================

Every factual or analytical claim must be tagged with its formal evidence class:
- DOCUMENTED: Explicitly stated in peer-reviewed publication or authoritative preprint. Does not imply implemented.
- CODE_OBSERVED: Verified directly in authoritative source code (with file and line citation). Does not imply runtime efficacy.
- RUNTIME_OBSERVED: Reported from live execution logs or interactive sessions in the reference work.
- BENCHMARK_VERIFIED: Confirmed by standardized benchmark datasets with reported metrics. Does not imply generalizability across domains.
- INDEPENDENTLY_REPRODUCED: Validated by external third-party researchers on separate codebases.
- CONTRADICTED: Directly disputed or disproven by alternative papers, code inspection, or empirical baselines.
- INFERRED: Logical deduction from evidence. May generate a hypothesis; cannot support architecture selection or requirements.
- UNRESOLVED: Evidence is conflicting, missing, or untraceable.

================================================================================
6. DELIVERABLE COMPLETENESS & GATE R1 CRITERIA
================================================================================

Tier 1: Required Substantively Complete at Gate R1
- DR-01: Research Corpus Ledger
- DR-02: Source Authority Map
- DR-03: System Architecture Profiles
- DR-04: Paper <-> Code Mapping
- DR-05: Primitive Evidence Matrix (all 26 fields per record)
- DR-06: System Comparison Matrix
- DR-07: Failure Register
- DR-08: Conflict Register
- DR-09: Unknowns Register
- DR-10: Candidate Baseline Matrix
- DR-14: Research Synthesis
- DR-15: Lessons Learned (Forward Constraints)
- DR-16: Research Gate Package (Gate R1 evaluation)

Tier 2: Required Draft / Provisional at Gate R1
- DR-11: Reproduction Candidate List (provisional ranking)
- DR-12: Proposed Experiment Matrix (falsifiable designs without execution authorization)
- DR-13: Cost / Latency / Scaling Analysis (bounded to reported literature; explicit UNKNOWN for unmeasured regimes)

================================================================================
ACCEPTANCE CRITERIA
================================================================================

Research Rigor & Implementation Mapping:
- All five reference systems are mapped to their authoritative implementation source where one can be verified. Where no authoritative source can be established, the gap is classified as UNRESOLVED with supporting rationale and zero unsupported substitutions.
- The historically relevant implementation version is preferred over current main when determining what code corresponds to published findings.
- Code citations cite exact repository branches, commit hashes, file paths, and line numbers.
- Paper-to-code divergences (e.g. prompt shortcuts, hardcoded parameters, missing reflection steps) are documented with exact source references.

Primitive Extraction & Registers:
- Every Primitive Evidence Record in DR-05 contains all 26 schema fields. Unavailable or unmeasured metrics use explicit UNKNOWN / NOT_REPORTED states; no synthetic numbers are fabricated.
- reproducibility_status is documented for every primitive using permitted values (NOT_ASSESSED, AUTHOR_REPORTED, etc.).
- Zero primitives in DR-05 receive VALIDATED status.
- Confound controls explicitly document model scale, context, prompt strategy, and token spend for all major comparative claims.
- Failure Register (DR-07) and Conflict Register (DR-08) document failure modes, negative results, and literature disagreements with required discriminatory evidence.
- Unknowns Register (DR-09) tracks architecture-shaping questions without premature closure.

Baselines & Experimental Governance:
- Baselines B0 through B4 are formally defined with operational boundaries.
- DR-11 and DR-12 are designated as experiment designs only, with zero code execution, benchmark runs, or implementation authorized.
- Every proposed experiment in DR-12 includes explicit limitations stating what conclusions would not be justified.

Gate Deliverables & Lifecycle Invariant:
- All Tier 1 deliverables (DR-01-DR-10, DR-14-DR-16) are substantively complete; Tier 2 deliverables (DR-11-DR-13) are cleanly structured as provisional proposals.
- DR-15 provides actionable forward constraints to prevent recurring mistakes in future phases.
- Gate R1 recommendation is formulated strictly as CONTINUE_RESEARCH, INSUFFICIENT_EVIDENCE, or READY_FOR_REPRODUCTION_DESIGN.
- No simulation runtime code is written; architecture remains completely unfrozen; Curo governance boundaries are strictly preserved.
</USER_REQUEST>

## 2026-09-16T09:29:40Z

<USER_REQUEST>
Curo SimLab — Phase 2 Reproduction Design & Experimental Roadmap
Project: Persistent 25+ Agent Simulation Laboratory
Working directory: E:\projects\simlab
Integrity mode: benchmark

Current Canonical State:
Lifecycle State: GATE_R1_COMPLETE -> REPRODUCTION_DESIGN_AUTHORIZED
Gate R1 Outcome: READY_FOR_REPRODUCTION_DESIGN
Architecture Status: UNFROZEN
Implementation Authority: NOT_GRANTED
Experiment Execution Authority: NOT_GRANTED
Reproduction Execution Authority: NOT_GRANTED

Governing Mission & Invariants:
Advance Curo SimLab into bounded reproduction design (Phase 2).
Produce complete deliverables RD-01 through RD-16 in E:\projects\simlab\reproduction_design\ and evaluate at Gate R2.
Strictly adhere to the 35-field Experiment Specification Record schema for all four reproduction candidates (RP-01 through RP-04).
Apply the Minimum Experiment Principle (isolated harnesses, zero full simulation rebuilds), deterministic-first measurement, pre-registered failure thresholds, and strict compute-matched controls.
Architecture must remain strictly UNFROZEN. Implementation and execution authority remain NOT_GRANTED.
Gate R2 permitted outcomes: CONTINUE_REPRODUCTION_DESIGN, INSUFFICIENT_EXPERIMENT_DESIGN, READY_FOR_REPRODUCTION_EXECUTION.
</USER_REQUEST>

## 2026-09-16T21:54:00Z

<USER_REQUEST>
# Teamwork Project Prompt

Perform a bounded scientific audit of CURO SIMLAB EXP-AB-01-COMP before dispatching the next Phase 4 experiment, distinguishing real mechanisms from implementation defects, benchmark artifacts, or measurement errors.

Working directory: `E:\projects\simlab\audits\EXP-AB-01-COMP`
Integrity mode: development

## Requirements

### R1. PRESERVE OBSERVED RESULTS
Treat the existing raw results as immutable evidence. Do not rewrite or suppress the existing MRR scores (A2: 0.5130, A4: 0.5002, A7: 0.0941, A3: 0.0086, A8: 0.0325). Preserve all hashes, telemetry, seeds, and run IDs. Do not rerun the experiment unless the audit identifies a defect requiring a preregistered corrective rerun. Do not advance to another Phase 4 experiment.

### R2. CORRECT NON-INFERIORITY ADJUDICATION
Verify the preregistered non-inferiority procedure for A4 vs A7. Determine if a formal one-sided non-inferiority test or confidence-bound comparison against the preregistered margin was performed. If yes, report the statistic, bound, alpha, and decision. If no, use `NON_INFERIORITY_DIRECTION_SUPPORTED_PENDING_FORMAL_TEST` or similar. Do not infer formal non-inferiority from a two-sided Wilcoxon p-value alone.

### R3. CORRECT IMPORTANCE-NECESSITY INTERPRETATION
Address the contradiction that A4 (recency+relevance) outperformed A7 (full tri-factor) by ~+0.4061 MRR. Explain the result using effect direction, effect magnitude, confidence interval, and statistical test. Do not claim the hypothesis is rejected simply because p is very small; explain the directional failure of the full tri-factor condition.

### R4. MECHANISTIC FAILURE AUDIT
Inspect importance, relevance, and recency score distributions (min, max, mean, variance, quantiles). Verify normalization method, sign/direction semantics, weight application, score combination, tie handling, sorting direction, rank construction, and candidate-set construction. Specifically test for scale dominance, scale inversion, normalization mismatch, weight application error, reflection score dominance, duplicate crowding, label leakage, and benchmark bias. Do not assume; test them.

### R5. REFLECTION FAILURE ANALYSIS
Determine why A8 produced 100% Rank-1 crowding, 100/100 queries affected, and all top-five slots occupied by reflection nodes. Inspect differences in relevance, importance, recency, embedding similarity, metadata, eligibility, and duplication rate between reflection nodes and ordinary nodes. Classify as REAL_PRIMITIVE_FAILURE, IMPLEMENTATION_DEFECT, BENCHMARK_ARTIFACT, SCORING_SCALE_ARTIFACT, or UNRESOLVED_MECHANISM.

### R6. VALIDATE WEIGHT CONFIGURATIONS
Verify that every A1-A8 configuration exactly matches AS-03 preregistration (especially A4 = recency+relevance, A7 = full tri-factor, A8 = A7 + reflection). Record expected_weights, executed_weights, and match?. If any mismatch exists, output `EXPERIMENT_CONFIGURATION_DRIFT` and stop progression.

### R7. CHECK PHASE 3 COMPATIBILITY
Compare this result with Phase 3 RP-01 findings. Determine if the Phase 4 tri-factor collapse is consistent, a different weight regime, a different benchmark regime, a different retrieval implementation, or a true contradiction. Do not silently reconcile. Record `PHASE3_PHASE4_EVIDENCE_CONFLICT` if necessary.

### R8. PRIMITIVE EVIDENCE STATUS
Update only Criterion B (ABLATION_EVIDENCE) for PR-COG-01. Do not adjudicate globally. Do not freeze architecture. Use statuses: SUPPORTED, SUPPORTED_WITH_CONSTRAINTS, COMPONENT_NOT_NECESSARY_UNDER_TESTED_CONDITIONS, MECHANISTIC_FAILURE_UNDER_INVESTIGATION, or EVIDENCE_CONFLICT.

### R9. LESSONS LEARNED
Capture validated lessons as forward constraints (e.g., scale compatibility, reflection admission controls, directional interpretation). Only promote lessons actually supported by the audit.

### R10. GATE TO NEXT EXPERIMENT
Return exactly one of the following statuses. Do not automatically execute the next experiment:
- STAGE_4A_RESULT_VALID_NEXT_EXPERIMENT_ALLOWED
- STAGE_4A_CORRECTIVE_RERUN_REQUIRED
- STAGE_4A_MECHANISTIC_INVESTIGATION_REQUIRED
- STAGE_4A_EVIDENCE_CONFLICT_REQUIRES_REVIEW

## Acceptance Criteria

### Execution Constraints
- [ ] No experiments were rerun unless explicitly triggered by a preregistered corrective rerun finding.
- [ ] No advancement to subsequent Phase 4 experiments occurred.
- [ ] The "CURO INVARIANT" was respected: Extreme effects were treated as evidence to be mechanistically diagnosed, not automatic truth.

### Required Output Sections
- [ ] A. Statistical Adjudication Correction
- [ ] B. Non-Inferiority Verification
- [ ] C. Importance-Necessity Interpretation
- [ ] D. Score-Distribution Audit
- [ ] E. Reflection Mechanism Analysis
- [ ] F. Configuration Integrity Check
- [ ] G. Phase 3 / Phase 4 Compatibility
- [ ] H. PR-COG-01 Evidence Update
- [ ] I. Lessons Learned / Forward Constraints
- [ ] J. Stage 4A Decision
</USER_REQUEST>

## 2026-09-17T01:17:39Z

<USER_REQUEST>
This is a single self-contained fix; keep it small and focused. Small focused team for governance contract reconciliation, provenance audit, and capability-gap mapping.

Conduct a comprehensive contract-tightening audit and governance reconciliation for the Agent Simulation Lab (SimLab / Smallville-derived 25+ agent simulation project) against current Curo governance contracts. The project state is canonically set to PAUSED / CONTRACT_TIGHTENING_REQUIRED. No implementation, experimentation, or simulation execution may proceed.

Working directory: E:\projects\simlab
Integrity mode: benchmark

## Requirements

### R1. Verify Current Project Lifecycle and Authority Boundaries
Confirm exact lifecycle states, closed gates (Gates R1, R2, R3, R4D), pending gates (Gate R4), unfrozen architecture status, and requester HITL authority boundaries.

### R2. Reconcile Existing Artifacts Across All Phases
Perform an artifact-by-artifact audit covering Phase 1 (DR-01..DR-16), Phase 2 (RD-01..RD-16), Phase 3 (PX-00..PX-16), Phase 4 (AS-01..AS-18, NC-01..NC-70), and master packages, classifying each under REUSE / EXTEND / ADD / REJECT / UNKNOWN.

### R3. Enforce Epistemic and Provenance Separation
Verify clean separation between empirical evidence, interpretation, hypotheses, design decisions, and implementation authority. Ensure no model-local artifact has silently become canonical.

### R4. Identify Governance, Validation, and Capability Gaps
Map missing validation controls, missing provenance controls, capability gaps (mapped to project-local, Curo skills, Curo roles, Curo tools, and governance gaps), and provide a minimum contract-tightening plan.

## Acceptance Criteria

### Comprehensive Reconciliation
- [ ] Project state verified as PAUSED / CONTRACT_TIGHTENING_REQUIRED.
- [ ] Authority state audited: Architecture strictly UNFROZEN, implementation NOT_GRANTED, primitive adjudication NOT_AUTHORIZED.
- [ ] Complete inventory of all existing artifacts across Gates R1, R2, R3, R4 compiled.
- [ ] Every artifact/concept classified as REUSE / EXTEND / ADD / REJECT / UNKNOWN with explicit rationale.
- [ ] Governance conflicts and stale/superseded contracts identified.
- [ ] Missing authority, validation, and provenance controls documented.
- [ ] Lessons-learned register (NC-01..NC-70) audited for forward constraint binding.
- [ ] Capability-gap register populated across the 5 required targets.
- [ ] Minimum contract-tightening changes and proposed reconciliation sequence formulated.
- [ ] Gate result returned: CONTRACT_TIGHTENING_COMPLETE_READY_FOR_REQUESTER_REVIEW.
- [ ] Execution remains strictly PAUSED.
</USER_REQUEST>

