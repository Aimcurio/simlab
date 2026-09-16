# BRIEFING — 2026-09-15T20:26:47Z

## Mission
Adversarially challenge the empirical claims, statistical models, primitive rankings, baseline comparisons (B0-B4), and confound controls in the Curo Deep Research Investigation (DR-05, DR-06, DR-10, DR-13, DR-14).

## 🔒 My Identity
- Archetype: Empirical Challenger
- Roles: critic, specialist
- Working directory: E:\projects\simlab\.agents\curo_challenger_1
- Original parent: 3d79cf01-2554-4325-a08a-4860a5867124
- Milestone: Gate R1 Research Review
- Instance: 1 of 1

## 🔒 Key Constraints
- Review-only — do NOT modify deliverable files directly; deliver adversarial challenge report and handoff.
- Empirical verification mandatory: write and run tests/scripts to mathematically and empirically verify or refute claims.
- If you cannot reproduce a bug/finding empirically, it does not count.
- Invariant: RESEARCH_DESIGN != IMPLEMENTATION_AUTHORIZATION.
- No ungrounded claims: all findings backed by direct execution, calculation, or literature evidence.

## Current Parent
- Conversation ID: 3d79cf01-2554-4325-a08a-4860a5867124
- Updated: 2026-09-15T20:26:47Z

## Review Scope
- **Files to review**:
  - `E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md`
  - `E:\projects\simlab\deliverables\DR-06_system_comparison_matrix.md`
  - `E:\projects\simlab\deliverables\DR-10_candidate_baseline_matrix.md`
  - `E:\projects\simlab\deliverables\DR-13_cost_latency_scaling_analysis.md`
  - `E:\projects\simlab\deliverables\DR-14_research_synthesis.md`
- **Interface contracts**: `ORIGINAL_REQUEST.md`, `PROJECT.md`
- **Review criteria**: Empirical validity, mathematical rigor, baseline fairness, confound separation, scaling fidelity.

## Key Decisions Made
- Executed empirical test suite `E:\projects\simlab\test_empirical_challenges.py` covering:
  1. Token-normalized Multi-Agent Debate vs B1-SC (Self-Consistency) across Binomial and Beta-Binomial models.
  2. Smallville `retrieve.py` rank decay ($0.99^i$) sorting order, min-max inversion, and Spearman rank correlation with `gw=[0.5, 3, 2]` vs `gw=[1, 1, 1]`.
  3. Algorithmic complexity derivation audit of DR-13 §4.1 line 179.
  4. 2x2 Factorial ANOVA variance decomposition of foundation model scale vs multi-agent architecture across HumanEval and GSM8K.
- Final Review Verdict: REQUEST_CHANGES (due to mathematical derivation error in DR-13 §4.1 underestimating debate token complexity by 2.8x-5.9x, and requiring domain boundary qualifications on B1-SC superiority).

## Attack Surface
- **Hypotheses tested**:
  - H1: Multi-agent debate yields no statistically significant advantage over B1-SC at equal token spend. -> CONFIRMED for homogeneous closed-context reasoning (B1-SC achieves 89.3% vs MAD 85.6% at equal 7,500 tokens). CAVEAT: Does not hold for heterogeneous agents with partitioned private data.
  - H2: Smallville's `retrieve.py` implementation causes an exact mathematical inversion of recency (oldest=1.0, newest=0.0) under chronological sorting, and `gw=[0.5, 3, 2]` suppresses recency influence. -> CONFIRMED. Oldest node receives normalized 1.0, newest receives 0.0 for all $N \ge 2$. Under `gw=[1, 1, 1]`, Spearman correlation with true recency is $\rho = -0.5437$; `gw=[0.5, 3, 2]` suppressed this to $\rho = -0.1044$ while elevating relevance to $\rho = 0.6902$.
  - H3: Complexity claims ($O(N \cdot M)$, $O(V^2)$) represent upper-bound worst-case rather than average-case, or miss token saturation bounds. -> FOUND DERIVATION BUG IN DR-13: DR-13 claimed $\sum N(rL) = O(N \cdot R^2)$, omitting peer context accumulation. True broadcast debate complexity is $O(N^2 \cdot R^2 \cdot L)$, underestimating token cost by 2.78x-5.87x.
  - H4: Reported benchmark gains in systems like ChatDev or Agent Hospital are primarily model scale / prompt engineering confounds rather than architectural primitives. -> CONFIRMED via 2x2 ANOVA. Model upgrade accounts for 76.3% of variance on HumanEval and 80.8% on GSM8K; multi-agent architecture accounts for only 16.2%-18.9%.
- **Vulnerabilities found**:
  1. DR-13 §4.1 line 179 mathematical formula error ($O(N \cdot R^2)$ vs true $O(N^2 \cdot R^2)$).
  2. DR-10 / DR-14 overgeneralized claim on B1-SC superiority omitting heterogeneous agent exception.
- **Untested angles**: Full long-horizon multi-day drift under continuous streaming.

## Loaded Skills
- Python verification test harness (`E:\projects\simlab\test_empirical_challenges.py`).

## Artifact Index
- `E:\projects\simlab\.agents\curo_challenger_1\BRIEFING.md` — persistent memory
- `E:\projects\simlab\.agents\curo_challenger_1\progress.md` — heartbeat and progress tracker
- `E:\projects\simlab\.agents\curo_challenger_1\challenge_report.md` — adversarial challenge report
- `E:\projects\simlab\.agents\curo_challenger_1\handoff.md` — 5-component handoff report
- `E:\projects\simlab\test_empirical_challenges.py` — executable verification test suite
