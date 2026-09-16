# Task Assignment — curo_remedy_worker_1 (Remediation Author: DR-12, DR-13, DR-15)

## Mission
Apply required empirical and governance remediations from Challengers 1 and 2 to deliverables DR-12, DR-13, and DR-15.

## Mandatory Reading & Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Challenger 1 Handoff & Report: `E:\projects\simlab\.agents\curo_challenger_1\handoff.md`, `E:\projects\simlab\.agents\curo_challenger_1\challenge_report.md`
- Challenger 2 Handoff & Report: `E:\projects\simlab\.agents\curo_challenger_2\handoff.md`, `E:\projects\simlab\.agents\curo_challenger_2\challenge_report.md`
- Files to Edit:
  - `E:\projects\simlab\deliverables\DR-12_proposed_experiment_matrix.md`
  - `E:\projects\simlab\deliverables\DR-13_cost_latency_scaling_analysis.md`
  - `E:\projects\simlab\deliverables\DR-15_lessons_learned_forward_constraints.md`

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Lifecycle State & Authority Boundaries
- Current Lifecycle State: `RESEARCH_AUTHORIZED`
- Implementation Authority: `NOT_GRANTED` (Strict prohibition: no code writing, simulation runtime implementation, dependency installation, or benchmark execution).
- Core Invariant: RESEARCH_DESIGN != IMPLEMENTATION_AUTHORIZATION.

## Required Modifications
1. **DR-13 (Cost / Latency / Scaling Analysis)**:
   - In Section 4.1, replace the token scaling formula for multi-agent broadcast debate. Correct the formula from $O(N \cdot R^2)$ to $O(N^2 \cdot R^2 \cdot L)$ where $N$ is number of agents, $R$ is debate rounds, and $L$ is average message length. Provide the explicit closed-form derivation accounting for peer context accumulation across rounds:
     $$T_{\text{debate}} = \sum_{r=1}^R \sum_{i=1}^N \left( C_{\text{sys}} + (r-1) \cdot N \cdot L + L \right) = N \cdot R \cdot C_{\text{sys}} + \frac{N^2 \cdot R(R-1)}{2} \cdot L + N \cdot R \cdot L \in O(N^2 \cdot R^2 \cdot L)$$
2. **DR-12 (Proposed Experiment Matrix)**:
   - In EXP-001 (§2.1):
     * Update sample size: expand from 30 tasks to at least 72 distinct SWE-bench tasks with 5 random seeds ($N_{\text{runs}} \ge 360$ per condition, total $N = 1080$) to guarantee true power $\ge 85\%$ at $p_1 = 0.15$ with ICC $\rho = 0.15$ ($n_{\text{eff}} \ge 225$).
     * Add formal Two One-Sided Tests (TOST) non-inferiority framework ($\delta = 0.05$) to guard against the "affirming the null" fallacy.
   - In EXP-002 (§2.2):
     * Correct Cochran's Q test power model: clarify that degrees of freedom depend on matched blocks, requiring at least 56 distinct security vulnerability tasks ($N_{\text{blocks}} \ge 279$ at 5 seeds) to achieve $80\%$ power at $\alpha=0.01$ and $w=0.25$.
   - In EXP-003 (§2.3):
     * Mandate Firth's penalized likelihood estimation for binary recovery ($FRR$) logistic regression to eliminate quasi-complete separation divergence in zero-failure cells.
3. **DR-15 (Lessons Learned / Operational Negative Forward Constraints)**:
   - Clarify NC-02 (Cedar TOCTOU): mandate that approvals must be verified against digital signatures and content-addressable storage URIs (`cas://sha256:...`).
   - Clarify NC-03 (Macaroon DPoP): mandate monotonic per-agent sequence counters ($Seq_{\text{agent}}$) to prevent same-tick replay.
   - In NC-05: extend AST inspection to string literals to prevent injection smuggling.
   - Add 4 binding operational negative constraints:
     * `NC-13`: Cross-Run Memory & Context Isolation (Strict prohibition on shared state or memory carryover across runs).
     * `NC-14`: Anti-Self-Approval Invariant (An agent role cannot approve its own work product or PR).
     * `NC-15`: Model Endpoint & Weight Hash Pinning (Strict prohibition on floating endpoints; must pin exact snapshot or model weight hash).
     * `NC-16`: Sandbox Tool Execution Resource Caps (Mandatory CPU, memory, timeout, and network isolation limits on all agent tool executions).

## Deliverable Handoff
Modify all 3 markdown files under `E:\projects\simlab\deliverables\`.
Write handoff report to:
`E:\projects\simlab\.agents\curo_remedy_worker_1\handoff.md`.

## 2026-09-15T20:34:05Z

You are curo_remedy_worker_1, serving as Remediation Author for DR-12, DR-13, and DR-15.
Working Directory: E:\projects\simlab\.agents\curo_remedy_worker_1
Authoritative Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read lines under header ## 2026-09-15T20:06:10Z first)
Task Assignment: E:\projects\simlab\.agents\curo_remedy_worker_1\DISPATCH.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Core Inputs:
- E:\projects\simlab\.agents\curo_challenger_1\challenge_report.md
- E:\projects\simlab\.agents\curo_challenger_2\challenge_report.md

Execute the required remediations:
1. In DR-13 (§4.1): correct broadcast debate token scaling formula to O(N^2 * R^2 * L) with closed-form derivation.
2. In DR-12: update EXP-001 sample size to >=72 SWE-bench tasks (N_runs >= 360 per condition) with TOST non-inferiority; update EXP-002 to >=56 tasks (N_blocks >= 279); update EXP-003 with Firth's penalized likelihood.
3. In DR-15: clarify NC-02 (content-addressable storage cas://sha256:...) and NC-03 (monotonic sequence counter); extend NC-05 to string literals; add NC-13, NC-14, NC-15, NC-16.

Deliver handoff report to:
E:\projects\simlab\.agents\curo_remedy_worker_1\handoff.md
and notify orchestrator via send_message when complete.
