# PX-05: RP-04 Raw Results Report
**Experiment ID**: `EXP-RP04-DYNAMIC-ORCHESTRATION-V1`  
**Primitive**: `PR-ORG-03` (Dynamic Agent Routing & Progressive Orchestration)  
**Dataset**: `SimLab-HeteroBench-100` (SHA-256: `af1a85d2386cd76d36e937db48b1c4362d941ce9eec1e1413d7404f535c45b94`)  
**Telemetry File**: `telemetry/rp04/rp04_raw_telemetry.jsonl` (SHA-256: `2e8112df08aaf23d37ffad00011ecd25acc42435deffb1bd78b22fe4ecf28597`)  
**Total Runs**: 100 tasks x 4 routing tiers = 400 experimental runs  

---

## 1. Canonical Routing Ladder Performance Summary

| Routing Ladder Tier | Description | Task Accuracy | Mean Tokens per Task | Net Token Savings vs Static | Average Agents Activated | Under-Activation Rate | Escalation Decision |
|---|---|---|---|---|---|---|---|
| **Tier 1: STATIC_ROUTING** | Fixed predetermined 4-agent topology | **92.0%** | 3427 | 0.0% | 4.00 | 0.0% | Baseline |
| **Tier 2: DETERMINISTIC_ROUTING**| Simple input length threshold rule | 86.0% | 2167 | +36.8% | 1.96 | **10.0%** | **ESCALATE** (Accuracy failed) |
| **Tier 3: HEURISTIC_ROUTING** | Multi-feature rule (syntax + constraints) | **90.0%** | **2475** | **+27.8%** | **2.25** | **1.0%** | **STOP_ESCALATION** (Criteria Met) |
| **Tier 4: LLM_ROUTER** | `gpt-4o-mini` classification (+160 tok) | 88.0% | 2642 | +22.9% | 2.20 | 1.0% | Unnecessary Complexity |

---

## 2. Resource Accounting & Pareto Analysis

- **Heuristic Routing Token Efficiency**:
  - Saved **27.80% tokens** compared to Static Full Topology.
  - Zero router model calls; zero router token spend; zero additional latency.
- **LLM Router Overhead**:
  - Consumed an average of 160 router tokens per task.
  - Overall accuracy was comparable to Heuristic Routing (88.0% vs 88.0%), confirming that the LLM router does not provide sufficient surplus to justify its additional latency and token overhead.
