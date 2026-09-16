# RD-11: Failure / Confound Register
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. Pre-Registered Failure Modes & Detection Protocols

To prevent post-hoc rationalization of experimental failures, SimLab pre-registers twelve systemic failure modes with quantitative detection triggers and mandatory abort conditions:

| Failure Code | Failure Mode | Vulnerable Experiments | Root Cause Mechanism | Detection Trigger / Operational Symptom | Pre-Registered Mitigation Protocol |
|---|---|---|---|---|---|
| **FM-01** | **Context Truncation** | RP-02, RP-03 | Message accumulation exceeding model context window ($L_{ctx} > 16k$) | Truncation flag emitted in telemetry; agent output references missing context | Enforce strict FIFO sliding context window or structured phase summary |
| **FM-02** | **False Consensus / Sycophancy** | RP-02 | Agent abandons correct private knowledge to agree with confident majority | Majority vote shifts from correct in Round 1 to incorrect in Round 2 | Log opinion drift trajectory; penalize ungrounded capitulation in metrics |
| **FM-03** | **Role Collapse** | RP-03, RP-04 | Specialized agents generate generic conversational filler or perform illegal tasks | Cross-role contamination detected via keyword/action regex audit | Reject and re-prompt out-of-role messages; count as role-collapse defect |
| **FM-04** | **Communication Explosion** | RP-02, RP-03 | Unbounded conversational loops generating quadratic token growth | Turns $> 12$ without state progress; token spend exceeds budget by $> 50\%$ | Hard turn limiter ($T_{max}=16$); abort episode and flag as `DEADLOCK` |
| **FM-05** | **Routing Collapse** | RP-04 | Router defaults to monolithic full team or single agent unconditionally | Path imbalance where single path > 65% of tasks, or Chi-Square Goodness-of-Fit test against expected task distribution rejects at $p < 0.001$ ($\chi^2 > 13.82, df=2$) | Trigger router calibration check; log routing collapse defect; fall back to heuristic baseline `B0-Heuristic` |
| **FM-06** | **Model-Version Drift** | All Experiments | Provider silently updates API weights during evaluation window | System fingerprint changes in API response header or snapshot retirement | Assert exact model fingerprint matching; immediate batch invalidation |
| **FM-07** | **Prompt Leakage / Inversion** | RP-01, RP-02, RP-03, RP-04 | Target answers, test solutions, or rubrics accidentally embedded in prompt | Exact-match test accuracy jumps to $100\%$ with zero reasoning steps, or test ground-truth tokens detected in prompt text | Automated prompt scanner screening ground-truth tokens in prompt text; immediate zero-tolerance batch invalidation |
| **FM-08** | **Score Compression / Normalization Error** | RP-01 | Normalized scores clustered in narrow band ($[0.98, 1.0]$), amplifying noise | Normalized score variance $< 10^{-4}$ across candidate memory items | Apply non-linear rank transformation or temperature scaling before combination |
| **FM-09** | **Unbalanced Compute** | RP-02, RP-03, RP-04 | Multi-agent treatment receives unbalanced tokens compared to single-agent control | Token ratio $|\text{Tok}_{MA} / \text{Tok}_{control} - 1.0| > 0.10$ (i.e. ratio $> 1.10$ or $< 0.90$) | Re-scale control sample count $K$ (e.g. $B_{1-SC-tokens}$ with $K=10$) or adjust turns to restore compute parity within $\pm 10\%$ |
| **FM-10** | **State Deadlock** | RP-03 | Phase gate reviewer repeatedly rejects implementation without feedback | Loop count between Coder and Reviewer reaches 4 iterations | Force escalation to orchestrator; record task as phase deadlock |
| **FM-11** | **Evaluator Bias** | RP-02, RP-03 | Auxiliary LLM judge favors verbose multi-agent answers over concise answers | Length-bias correlation $r > 0.35$ between word count and judge score ($p < 0.001$ at $N \ge 100$) | Length-normalize text or demote LLM judge; mandate deterministic unit tests as primary judge |
| **FM-12** | **Data Contamination** | RP-02, RP-03, RP-04 | Public benchmark instances memorized during pre-training | Single-agent zero-shot accuracy $> 95\%$ on complex novel reasoning, or benchmark hash collision | Inject synthetic perturbations / variable renaming; immediate batch invalidation |

---

## 2. Abort & Invalidation Criteria

To preserve absolute scientific validity, the experiment execution harness must enforce a strict, two-tier automated abort gate:

### A. Immediate Zero-Tolerance Invalidation Gate (Threshold: $\ge 1$ Confirmed Occurrence)
Any experimental batch or condition triggering even a single confirmed occurrence of any of the following fatal integrity breaches is immediately aborted, tagged `EXPERIMENT_INVALID`, and quarantined:
1. **FM-06 (Model-Version Drift)**: Upstream vendor system fingerprint changes from registered baseline snapshot.
2. **FM-07 (Prompt Leakage / Inversion)**: Ground-truth test code, answer keys, or evaluation rubrics detected in LLM context.
3. **FM-12 (Data Contamination)**: Memorized benchmark answers detected or unperturbed public test instances exposed.

### B. Statistical & Variance Invalidation Gate
An experimental batch or condition must be halted and marked `EXPERIMENT_INVALID` if:
1. **FM-09 (Unbalanced Compute)**: More than 2 episodes ($>2$) in a batch violate the $\pm 10\%$ compute parity envelope ($0.90 \le \text{Tok}_{MA} / \text{Tok}_{control} \le 1.10$).
2. **Systemic Failure Accumulation**: More than 3 instances ($>3$) of ANY registered failure mode (e.g. FM-01, FM-02, FM-03, FM-04, FM-05, FM-08, FM-10, FM-11) accumulate within an experimental run.

All aborted runs emit structured `ABORT_EVENT` telemetry with full stack traces, parameter manifests, and token usage ledgers to Layer H before teardown.
