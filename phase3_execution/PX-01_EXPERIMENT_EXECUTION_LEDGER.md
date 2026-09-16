# PX-01: Experiment Execution Ledger
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `CONTROLLED_REPRODUCTION_EXECUTION` → `RESULT_ANALYSIS`  
**Git Commit**: `8d7d8465b07c3b1c12c3748ce9f44c7051484daa`  
**Evaluation Date**: 2026-09-16  

---

## 1. Master Experiment Execution Manifest

| Experiment ID | Primitive ID | Mechanism Tested | Dataset / Benchmark | Runs ($N$) | Execution Order | Status | Primary Result Status |
|---|---|---|---|---|---|---|---|
| **EXP-RP01-RECENCY-V1** | `PR-COG-01` | Elapsed-Time Memory Decay vs Inverted Index | `SimLab-MemBench-500` | 400 episodes (100 queries x 4 cond) | Stage 3A (Canary) | **COMPLETED** | `SUPPORTED_WITH_CONSTRAINTS` |
| **EXP-RP03-PHASE-BOUNDARIES-V1** | `PR-ORG-02` | Phased SOPs vs Unrestricted Chat | `SimLab-CodeSOP-50` | 150 condition-runs (50 tasks x 3 cond) | Stage 3B | **COMPLETED** | `SUPPORTED_WITH_CONSTRAINTS` |
| **EXP-RP02-COMPUTE-MATCHED-V1** | `PR-ORG-01` | Compute-Matched Multi-Agent Debate | 4 Domains (GSM8K, Private Info, Tools, State) | 800 problem episodes | Stage 3C | **COMPLETED** | `CONTEXT_DEPENDENT` |
| **EXP-RP04-DYNAMIC-ORCHESTRATION-V1**| `PR-ORG-03` | Progressive Dynamic Routing Ladder | `SimLab-HeteroBench-100` | 400 runs (100 tasks x 4 tiers) | Stage 3D | **COMPLETED (STOP_ESCALATION)** | `SUPPORTED_WITH_CONSTRAINTS` |

---

## 2. Infrastructure & Telemetry Gate Checkpoints

- **Preflight Check (`PX-00`)**: `PREFLIGHT_PASS` certified prior to any execution.
- **Canary Gate (`RP-01`)**: Zero-LLM deterministic Canary executed first. Telemetry format, SHA-256 hashing, and replay determinism verified 100% operational.
- **Sequential Execution**: Strict stage boundaries enforced (3A → Canary Gate → 3B → 3C → 3D). Zero parallel launch leakage.
- **Immutability Assurance**: All raw JSONL telemetry streams written directly to `phase3_execution/telemetry/` with read-only permissions post-run.
