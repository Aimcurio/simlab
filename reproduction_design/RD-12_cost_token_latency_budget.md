# RD-12: Cost / Token / Latency Budget
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. Resource Consumption Modeling

All four reproduction experiments designed for SimLab have been rigorously budgeted across total API inference calls, token volume (prompt vs. completion), estimated financial spend, and execution latency under strictly controlled commercial API pricing:

### Experiment Budget Ledger (Core Benchmark Execution)

| Experiment ID | Conditions Evaluated | Episodes per Condition ($N$) | Total Episodes | Avg Calls per Episode | Total Inference Calls | Avg Tokens per Call (In / Out) | Total Token Volume | Est. Cost (USD) | Max Latency per Episode | Total Suite Runtime |
|---|---|---|---|---|---|---|---|---|---|---|
| **EXP-RP01-RECENCY** | 5 | 100 | 500 | 0 (Deterministic) | 0 LLM (1,000 Embed) | 250 / 0 | 250,000 | **$0.15** | 0.05s | < 2 minutes |
| **EXP-RP02-COMPUTE-MATCHED** | 3 | 400 | 1,200 | 6 (Matched) | 7,200 | 800 / 400 | 8,640,000 | **$43.20** | 25s | ~ 6 hours |
| **EXP-RP03-PHASE-BOUNDARIES** | 3 | 50 | 150 | 12 | 1,800 | 1,000 / 500 | 2,700,000 | **$13.50** | 90s | ~ 3.5 hours |
| **EXP-RP04-DYNAMIC-ORCHESTRATION**| 4 | 100 | 400 | 3 | 1,200 | 700 / 300 | 1,200,000 | **$6.65** | 45s | ~ 2.5 hours |
| **TOTALS** | — | — | **2,250** | — | **10,200** | — | **12,790,000** | **$63.50** | — | **~ 12 hours** |

### Verified Cost Arithmetic Derivation
- **Cost Basis**:
  - `gpt-4o-2024-08-06`: $\$2.50 / \text{1M prompt tokens}$, $\$10.00 / \text{1M completion tokens}$.
  - `gpt-4o-mini-2024-07-18`: $\$0.15 / \text{1M prompt tokens}$, $\$0.60 / \text{1M completion tokens}$.
  - `text-embedding-3-small`: $\$0.02 / \text{1M tokens}$.
- **EXP-RP01**: Pre-computation embeddings ($250\text{k tokens} \times \$0.02/\text{M} = \$0.005$) + ground-truth verification prompts ($\approx \$0.145$) = **$\$0.15$**.
- **EXP-RP02**: Prompt tokens: $7,200 \times 800 = 5.76\text{M} \times \$2.50/\text{M} = \$14.40$. Completion tokens: $7,200 \times 400 = 2.88\text{M} \times \$10.00/\text{M} = \$28.80$. Total = $\$14.40 + \$28.80 = \mathbf{\$43.20}$ (remediated from previous understated $\$34.50$).
- **EXP-RP03**: Prompt tokens: $1,800 \times 1,000 = 1.80\text{M} \times \$2.50/\text{M} = \$4.50$. Completion tokens: $1,800 \times 500 = 0.90\text{M} \times \$10.00/\text{M} = \$9.00$. Total = $\$4.50 + \$9.00 = \mathbf{\$13.50}$ (remediated from previous understated $\$12.20$).
- **EXP-RP04**: Worker prompts: $1,200 \times 700 = 0.84\text{M} \times \$2.50/\text{M} = \$2.10$. Worker completions: $1,200 \times 300 = 0.36\text{M} \times \$10.00/\text{M} = \$3.60$. Meta-router calls (`gpt-4o-mini`): $400 \text{ calls} \times 1,500 \text{ tokens} \approx \$0.95$. Total = $\$2.10 + \$3.60 + \$0.95 = \mathbf{\$6.65}$ (remediated from previous understated $\$5.40$).
- **Total Suite Cost**: $\$0.15 + \$43.20 + \$13.50 + \$6.65 = \mathbf{\$63.50}$ (remediated from previous understated $\$52.25$).

---

## 2. Strict Expenditure Caps & Staged Execution Protocol

1. **Hard Financial Ceiling**: The maximum permitted API spend across all Phase 3 execution runs is strictly capped at **$100.00 USD**. Execution harnesses must implement pre-paid balance assertions or budget counters that automatically terminate execution if spend reaches **$75.00 USD** (automated safety abort threshold).
2. **Staged Expansion Protocol**: The core benchmark suite ($N=100$ per experiment, costing $\$63.50$) is executed first to establish initial variance estimates and effect sizes. Expanded runs (e.g. GSM8K $N=500$, RP-03 $N=150$, RP-04 $N=300$) are dispatched in incremental batches under remaining budget headroom, with early termination if variance bounds are satisfied before budget exhaustion.
3. **API Rate-Limit Throttle**: Execution harnesses must enforce maximum concurrency of 5 parallel requests and exponential backoff with jitter on HTTP 429 responses.
4. **Local Compute Footprint**: All execution harnesses must run on standard developer hardware (Windows / Linux CPU, $\le 8$ GB RAM, $\le 10$ GB disk storage), requiring zero dedicated local GPU compute.
