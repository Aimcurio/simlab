# AS-13: Cost, Token & Compute Budget
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Projected Resource Budget for Phase 4 Execution

Phase 4 utilizes the **Minimum Ablation Principle** to isolate causal factors with minimal token spend:

| Experiment Code | Target Primitive | Experimental Conditions | Estimated Runs ($N$) | Avg Tokens / Run | Total Tokens | Estimated API Spend |
|:---|:---|:---|:---|:---|:---|:---|
| **EXP-AB-01-COMP** | `PR-COG-01` (Memory Comp) | 8 scoring variants | 800 evaluations | 0 (Offline vectors) | 0 | **$0.00** |
| **EXP-ST-01-SCALE** | `PR-COG-01` (Memory Stress) | 5 scale levels $\times$ 4 noise types| 2,000 evaluations | 0 (Offline vectors) | 0 | **$0.00** |
| **EXP-AB-02-REP** | `PR-ORG-01` (Private Info Rep)| 2 conditions ($B3$ vs $B1-SC$) | 540 episodes | 8,400 tokens | 4.54M tokens | **$2.75** |
| **EXP-AB-02-ASYM** | `PR-ORG-01` (Asymmetry Sweep)| 5 asymmetry levels | 750 episodes | 8,400 tokens | 6.30M tokens | **$3.80** |
| **EXP-ST-02-STATE** | `PR-ORG-01` (State Stress) | 5 population levels | 500 episodes | 6,200 tokens | 3.10M tokens | **$1.85** |
| **EXP-AB-03-FACT** | `PR-ORG-02` (SOP Factorial) | 4 factorial cells | 400 task runs | 12,000 tokens | 4.80M tokens | **$2.90** |
| **EXP-ST-03-SOP** | `PR-ORG-02` (SOP Stress) | 5 task ambiguity levels | 250 task runs | 14,000 tokens | 3.50M tokens | **$2.10** |
| **EXP-AB-04-FEAT** | `PR-ORG-03` (Routing Feature)| 7 heuristic variants | 630 task runs | 2,400 tokens | 1.51M tokens | **$0.90** |
| **EXP-ST-04-SHIFT** | `PR-ORG-03` (Routing Stress) | 4 shift levels | 400 task runs | 2,600 tokens | 1.04M tokens | **$0.65** |
| **Contingency** | Re-run reserve / buffer | Pre-registered buffer | - | - | 3.00M tokens | **$1.85** |
| **TOTALS** | - | - | **6,270 runs** | - | **27.79M tokens** | **$17.80 USD** |

---

## 2. Budgetary Invariants
- **Hard Ceiling**: $100.00 USD.
- **Estimated Spend**: **$17.80 USD** (Leaves $82.20 USD uncommitted buffer).
- **Zero Paid Token Harnesses**: Memory ablations and stress testing run entirely offline on pre-computed vectors ($0.00 API cost).
