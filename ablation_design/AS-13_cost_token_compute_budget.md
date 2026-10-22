# AS-13: Cost, Token & Compute Budget
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Projected Resource Budget for Phase 4 Execution

Phase 4 utilizes the **Minimum Ablation Principle** to isolate causal factors with minimal token spend:

| Experiment Code | Target Primitive | Experimental Conditions | Estimated Runs ($N$) | Avg Tokens / Run | Total Tokens | Estimated API Spend |
|:---|:---|:---|:---|:---|:---|:---|
| **EXP-AB-01-COMP** | `PR-COG-01` (Memory Comp) | 8 scoring variants | 800 evaluations | 0 (Offline vectors) | 0 | **$0.00** |
| **EXP-ST-01-SCALE** | `PR-COG-01` (Memory Stress) | 5 scale levels $\times$ 4 noise types| 2,000 evaluations | 0 (Offline vectors) | 0 | **$0.00** |
| **EXP-AB-02-REP** | `PR-ORG-01` (Private Info Rep)| 2 conditions ($B3$ vs $B1-SC$) | 1,300 episodes ($N=650$) | 8,400 tokens | 10.92M tokens | **$6.60** |
| **EXP-AB-02-ASYM** | `PR-ORG-01` (Asymmetry Sweep)| 5 asymmetry levels | 750 episodes | 8,400 tokens | 6.30M tokens | **$3.80** |
| **EXP-ST-02-STATE** | `PR-ORG-01` (State Stress) | 5 population levels | 500 episodes | 6,200 tokens | 3.10M tokens | **$1.85** |
| **EXP-AB-03-FACT** | `PR-ORG-02` (SOP Factorial) | 4 factorial cells | 400 task runs | 12,000 tokens | 4.80M tokens | **$2.90** |
| **EXP-ST-03-SOP** | `PR-ORG-02` (SOP Stress) | 5 task ambiguity levels | 250 task runs | 14,000 tokens | 3.50M tokens | **$2.10** |
| **EXP-AB-04-FEAT** | `PR-ORG-03` (Routing Feature)| 7 heuristic variants | 630 task runs | 2,400 tokens | 1.51M tokens | **$0.90** |
| **EXP-ST-04-SHIFT** | `PR-ORG-03` (Routing Stress) | 4 shift levels | 400 task runs | 2,600 tokens | 1.04M tokens | **$0.65** |
| **Contingency** | Re-run reserve / buffer | Pre-registered buffer | - | - | 2.50M tokens | **$1.55** |
| **TOTALS** | - | - | **7,030 runs** | - | **33.67M tokens** | **$20.35 USD** |

---

## 2. Canonical Budget Hierarchy & Semantics Reconciliation

To prevent confusion between operational abort triggers, experiment limits, advisory warnings, and global ceilings, the budgetary governance hierarchy is codified into four discrete, mutually exclusive levels:

| Level | Scope | Threshold Name | Value | Semantic Role | Source | Trigger Action | Override Allowed? | Authority Required for Change |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LEVEL 1** | Phase 4 Program | `PHASE4_BUDGET_WARNING_THRESHOLD` | **$35.00 USD** | `WARNING_THRESHOLD` | `AS-13` §2 | Advisory financial engineering notice: flags $>70\%$ drift above projected baseline; non-blocking. | **NO** | Senior Reviewer (Sol) |
| **LEVEL 2** | Per-Experiment | `EXP_BUDGET_LIMIT` (per plan) | **Per Matrix** (e.g. `EXP-AB-02-REP`: $6.60, `EXP-AB-02-ASYM`: $3.80) | `EXPERIMENT_BUDGET_LIMIT` | `AS-13` §1 | Pre-call projection check (`NC-38`); halts individual experiment if projected spend exceeds allocated budget. | **NO** | Requester Formal Amendment |
| **LEVEL 3** | Phase 4 Execution | `PHASE4_BUDGET_ABORT_THRESHOLD` | **$50.00 USD** | `ABORT_THRESHOLD` | `AS-14` (`AF-01`), `AS-11` §3.2 | Automated hard circuit breaker: immediately HALTS all Phase 4 execution runs and triggers emergency triage. | **NO** | Human Requester Only |
| **LEVEL 4** | Global Project | `GLOBAL_API_HARD_CEILING` | **$100.00 USD** | `GLOBAL_HARD_CEILING` | `AS-13` §2, `NC-38` | Hard environmental stop across all project phases; immediate API key revocation and container kill. | **STRICTLY NO** | Human Requester Formal Action |

### Budget Reconciliation Invariants:
1. **Scope Distinction**: `PHASE4_BUDGET_ABORT_THRESHOLD` ($50.00 USD) and `GLOBAL_API_HARD_CEILING` ($100.00 USD) govern fundamentally different operational scopes. Phase 4 execution stops at $50.00 USD even though the broader project ceiling remains $100.00 USD.
2. **Stricter Limit Controls**: The stricter Phase 4 limit ($50.00 USD) strictly controls Phase 4 execution runs. The remaining $50.00 buffer under the global ceiling must NOT be interpreted as permission to continue Phase 4 live execution.
3. **No Semantic Aliasing**: No two budget controls share the same semantic label or operational scope.
4. **Zero Paid Token Harnesses**: Memory ablations and stress testing run entirely offline on pre-computed vectors ($0.00 API cost).
5. **Pre-Call Financial Projection**: Every live call must compute projected cost and enforce stopping limits before dispatch (`NC-38`, `AF-01`).



