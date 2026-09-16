# Task Assignment — curo_challenger_1 (Empirical & Statistical Challenger)

## Mission
Adversarially challenge the empirical claims, statistical models, primitive rankings, baseline comparisons (B0-B4), and confound controls in the Curo Deep Research Investigation.

## Mandatory Reading & Inputs
- Authoritative Request: `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (read lines under header `## 2026-09-15T20:06:10Z` first)
- Deliverables to Challenge:
  - `E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md`
  - `E:\projects\simlab\deliverables\DR-06_system_comparison_matrix.md`
  - `E:\projects\simlab\deliverables\DR-10_candidate_baseline_matrix.md`
  - `E:\projects\simlab\deliverables\DR-13_cost_latency_scaling_analysis.md`
  - `E:\projects\simlab\deliverables\DR-14_research_synthesis.md`

## Challenge Objectives
1. **Coordination Tax & Compute Normalization**: Empirically and mathematically evaluate the claim that Single-Agent + Self-Consistency (B1-SC) matches or outperforms multi-agent debate when token budgets are equalized.
2. **Smallville Mathematical Decay & Sorting**: Check whether the inverted recency decay in Smallville (`retrieve.py`) mathematically favors older memories, and whether relevance weighting completely dominates recency.
3. **Complexity Scaling**: Challenge the algorithmic complexity claims ($O(N \cdot M)$ memory retrieval, $O(V^2)$ communication, token budgets).
4. **Confound Disentanglement**: Challenge whether reported literature gains can be attributed to model upgrades (GPT-3.5 -> GPT-4) rather than multi-agent architecture.

## Deliverable
Write your empirical challenge report and verdict (`APPROVE` or `REQUEST_CHANGES`) to:
`E:\projects\simlab\.agents\curo_challenger_1\challenge_report.md`
and write your handoff report to:
`E:\projects\simlab\.agents\curo_challenger_1\handoff.md`.

## 2026-09-15T20:26:47Z
You are curo_challenger_1, serving as Empirical & Statistical Challenger for the Curo Deep Research Investigation.
Working Directory: E:\projects\simlab\.agents\curo_challenger_1
Authoritative Request: E:\projects\simlab\.agents\ORIGINAL_REQUEST.md (read lines under header ## 2026-09-15T20:06:10Z first)
Task Assignment: E:\projects\simlab\.agents\curo_challenger_1\DISPATCH.md

Challenge empirical claims in DR-05, DR-06, DR-10, DR-13, and DR-14:
- Challenge multi-agent debate vs Single-Agent + Self-Consistency (B1-SC) token-normalized performance.
- Challenge Smallville mathematical decay inversion and relevance weight dominance (retrieve.py).
- Challenge complexity scaling claims (O(N*M), O(V^2)) and token spend coordination tax.
- Challenge confound attribution (model scale vs architecture).

Deliver challenge report and verdict (APPROVE / REQUEST_CHANGES) to:
E:\projects\simlab\.agents\curo_challenger_1\challenge_report.md
and handoff report to:
E:\projects\simlab\.agents\curo_challenger_1\handoff.md.
Notify orchestrator via send_message when complete.
