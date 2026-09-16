# PX-04: RP-03 Raw Results Report
**Experiment ID**: `EXP-RP03-PHASE-BOUNDARIES-V1`  
**Primitive**: `PR-ORG-02` (Phased Assembly-Line SOP State Machine)  
**Dataset**: `SimLab-CodeSOP-50` (SHA-256: `692044615497aecf0b9b22cd1996d14f1d082e39ee5ad8ae236164329d1ac097`)  
**Telemetry File**: `telemetry/rp03/rp03_raw_telemetry.jsonl` (SHA-256: `e4a7ef3d0b35318321004a34ce46b74610bc7ff30693096ebe090d7fc99a1487`)  
**Evaluation Scope**: 50 unique coding tasks x 3 conditions = 150 condition-runs  

---

## 1. Experimental Condition Aggregate Summary

| Experimental Condition | Unit Test Pass Rate | Mean Tokens per Task | Conversational Turns | Defect Count | Duplicated Work Events | Cross-Role Violations |
|---|---|---|---|---|---|---|
| **Control A (Single Agent)** | 79.88% | 2017 | 3.1 | 1.48 | 0.00 | 0.00 |
| **Control B (Unrestricted Chat)** | 80.72% | 22661 | 13.0 | 1.50 | 2.24 | 1.80 |
| **Treatment (Phase-Bounded SOP)** | **86.87%** | **11519** | **5.3** | **0.96** | **0.32** | **0.00** |

---

## 2. Resource & Efficiency Accounting

- **Token Reduction**: Phase-Bounded SOP achieved a **49.17% token reduction** compared to Unrestricted Multi-Agent Chat ($p = 1.7764e-15$, Wilcoxon signed-rank test).
- **Turn Efficiency**: Conversational turns dropped from 13.0 turns in free chat to 5.3 bounded turns in the SOP state machine.
- **Cross-Role Containment**: Cross-role violations dropped from 1.80 per task in unrestricted chat to **0.00** in the phase-bounded SOP.
