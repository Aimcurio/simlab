# RD-04: Baseline & Compute-Matching Specification
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. Reference Baseline Taxonomy

To prevent naive claims that multi-agent systems outperform single models due to architectural superiority rather than raw compute or sampling volume, all reproduction experiments must benchmark against the standardized baseline hierarchy established in Gate R1:

```
+----------------------------------------------------------------------------------------------------+
|                                    STANDARDIZED BASELINE HIERARCHY                                 |
+----------------------------------------------------------------------------------------------------+
| B0: Deterministic Agent       | Rule-based state machine, zero LLM reasoning                       |
| B1: Single LLM Agent          | Zero multi-agent collaboration, single-turn or simple CoT          |
| B1-SC: Compute-Matched Single | Single model sampled N times (Self-Consistency) matching MA tokens |
| B2: Multiple Independent LLMs | Multiple agents in shared environment, zero communication          |
| B3: Fixed-Role Multi-Agent    | Static topology, pre-assigned roles, fixed communication graph     |
| B4: Dynamic Adaptive System   | Dynamic recruitment, routing orchestrators, evolving graph         |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Compute-Matching Protocol & Invariants

### Core Invariant: Total Token & FLOP Equivalence
> **Compute-Normalization Rule**:  
> No multi-agent treatment ($T_{MA}$) may be claimed superior to a single-agent architecture ($B_1$) unless compared against a compute-matched single-agent control ($B_{1-SC}$) receiving an equivalent total inference budget.

### The Token Parity vs. Call Parity Confound in Multi-Round Debate
In multi-round multi-agent debate (e.g. 3 agents across 2 rounds), later rounds carry previous agents' outputs in their prompt contexts. For problem prompt length $C_0$ and response length $L$:
- **Treatment ($T_{Debate}$)**: Round 1 consumes $3(C_0 + L)$. Round 2 passes all 3 prior outputs into each agent's context, consuming $3(C_0 + 3L + L) = 3 C_0 + 12 L$. Total tokens: $T_{Debate} = 6 C_0 + 15 L$.
- **Single-Turn Self-Consistency ($B_{1-SC}$ with $K$ calls)**: Total tokens: $T_{B1-SC} = K(C_0 + L)$. For $K=6$, $T_{B1-SC} = 6 C_0 + 6 L$.
Under realistic reasoning lengths ($C_0 = 800$, $L = 400$), $T_{Debate} = 10,800$ tokens while $T_{B1-SC(K=6)} = 7,200$ tokens, meaning debate incurs a $+50.0\%$ token inflation over call-matched $K=6$. Holding both $K=6$ inference calls AND $\pm 10\%$ token parity simultaneously is mathematically impossible.

### The Dual-Control Protocol (EXP-RP02)
To eliminate this confound and determine whether debate gains stem from multi-agent interaction or simply from higher total token spend, SimLab institutes a **Dual-Control Protocol**:
1. **$B_{1-SC-calls}$ ($K=7$ calls)**: Inference-Call-Matched Control. Uses $K=7$ independent reasoning paths ($T=0.7$). The odd sample size $K=7$ strictly eliminates 50/50 binary ties under majority voting (which occurs in up to $31.3\%$ of cases under even $K=6$).
2. **$B_{1-SC-tokens}$ ($K=10$ calls)**: Token-Budget-Matched Control. Uses $K=10$ independent reasoning paths ($T=0.7$), equalizing total token expenditure with 3-agent 2-round debate within $\pm 5\%$ ($10 \times 1,200 = 12,000$ tokens vs $10,800$ tokens).

### Deterministic Tie-Breaking Rules
For all Self-Consistency ($B_{1-SC}$) baseline voting aggregations:
1. **Primary Rule (Plurality Voting)**: The candidate answer receiving the highest vote count among the $K$ samples is selected.
2. **Deterministic Tie-Breaker (Confidence Log-Probability)**: In the event of an exact vote tie (possible with $K=10$, or when $K=7$ splits across $\ge 3$ distinct answers), the tie is broken deterministically by selecting the tied answer candidate whose generating samples have the highest mean sequence log-probability:
   $$\bar{\ell}(A) = \frac{1}{|S_A|} \sum_{s \in S_A} \left( \frac{1}{|Tokens(s)|} \sum_{t \in Tokens(s)} \log P(t) \right)$$
3. **Fallback Rule (Lowest Sample Index)**: If log-probabilities are identical or unavailable, select the candidate answer that appeared earliest among the deterministic sample indices ($j \in \{1, \dots, K\}$). Random coin flips are strictly prohibited.

---

## 3. Baseline Configuration Matrix for Phase 2 Experiments

| Experiment | Target Primitive | Primary Baseline | Secondary Baseline | Treatment ($T$) | Compute-Matching Control |
|---|---|---|---|---|---|
| **RP-01** | Memory Recency Decay | **B0-Historical**: Smallville inverted rank index (`retrieve.py:145-146`) | **B0-NoRecency**: Relevance + Importance only ($\alpha=0, \beta=3.0, \gamma=2.0$) | **T-Corrected**: Exponential temporal decay ($s = 0.995^{\Delta t_{hours}}$) | Deterministic retrieval: 0 LLM calls during retrieval; compute identical across runs |
| **RP-02** | Multi-Agent Debate | **B1**: Single agent greedy CoT ($T=0$) | **B1-SC-calls**: $K=7$ calls, odd sample size | **T-Debate**: 3-agent 2-round structured debate ($B3$, 6 calls) | **Dual-Control**: Both $B_{1-SC-calls}$ ($K=7$) and $B_{1-SC-tokens}$ ($K=10$) |
| **RP-03** | Structured Phase SOPs | **B1**: Single agent with multi-turn self-refinement | **B3-Unrestricted**: Multi-agent chat without phase boundaries | **T-PhaseSOP**: Multi-agent phase-gated state machine (ChatDev SOP) | Call-matched: Maximum interaction turns capped at 16 across both B3 and T-PhaseSOP; $N=150$ tasks |
| **RP-04** | Dynamic Orchestration | **B3**: Static full topology (all 4 agents activated every task) | **B0-Heuristic**: Rule-based keyword/task-type router | **T-LLMRouter** & **T-Evolving**: Selective meta-orchestrators | **B1-SC**: Single-agent compute-matched control (N=300 tasks; 70/30 train/test split) |

---

## 4. Stopping Conditions, Confound Enforcement & Inconclusive States
1. **Context Window Saturation**: If any agent's context window exceeds $75\%$ of capacity, prune using deterministic FIFO sliding window; record truncation count as a confound.
2. **Deadlock / Infinite Loop Guard**: Maximum rounds capped at $R_{max} = 10$ (or 16 conversational turns in RP-03). If an experiment reaches this ceiling without completion, flag as `CONVERSATIONAL_DEADLOCK_ERROR`.
3. **Execution Sandbox Limits**: Distinct from conversational deadlocks, isolated code execution limits are enforced at $10\text{s CPU}$, $512\text{ MB RAM}$, and zero network interface. Code exceeding these bounds is flagged as `SANDBOX_TIMEOUT_ERROR`.
4. **Prompt Drift Guard**: All prompt templates must be SHA-256 hashed and version-controlled before execution design is finalized.
5. **Pre-Registered Default for Inconclusive Outcomes**: If an experimental outcome falls within the `INCONCLUSIVE_SUB_THRESHOLD` zone between pre-registered success and failure thresholds, the governance rule mandates defaulting to the simpler, lower-compute baseline (Minimum Experiment Principle).
