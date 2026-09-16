# PX-03: RP-02 Raw Results Report
**Experiment ID**: `EXP-RP02-COMPUTE-MATCHED-V1`  
**Primitive**: `PR-ORG-01` (Multi-Agent Iterative Debate & Cross-Examination)  
**Telemetry File**: `telemetry/rp02/rp02_raw_telemetry.jsonl` (SHA-256: `6d82e93d1da894ffdb512a9843fad1d7940b09033f69d9635c24fde2e76048dc`)  
**Total Instances Evaluated**: 800 problem episodes (500 Closed Reasoning, 100 Private Info, 100 Asymmetric Tools, 100 Distributed State)  

---

## 1. Multi-Domain Compute-Matched Performance Matrix

| Task Domain | Problem Count ($N$) | Single Agent ($B1$) | Call-Matched $B1-SC$ ($K=7$) | Token-Matched $B1-SC$ ($K=10$) | Multi-Agent Debate ($B3$) | Net Accuracy Advantage ($B3$ vs $B1-SC$-Tok) | Statistical Test & p-value | Preregistered $\alpha$ | Reconciled Status |
|---|---|---|---|---|---|---|---|---|---|
| **CLOSED_REASONING_GSM8K** | 500 | 77.8% | 83.2% | 84.8% | **89.2%** | **+4.4%** | TOST: $p_{TOST} = 0.7408$ | $\alpha = 0.05$ | **`EQUIVALENCE_NOT_ESTABLISHED`** |
| **PRIVATE_INFORMATION** | 100 | 57.0% | 61.0% | 73.0% | **87.0%** | **+14.0%** | McNemar Exact: $p = 0.0192$ | $\alpha = 0.01$ | **`PROMISING_BUT_NOT_SIGNIFICANT`** |
| **ASYMMETRIC_TOOLS** | 100 | 56.0% | 69.0% | 75.0% | **89.0%** | **+14.0%** | McNemar Exact: $p = 0.0125$ | $\alpha = 0.01$ | **`PROMISING_BUT_NOT_SIGNIFICANT`** |
| **DISTRIBUTED_STATE** | 100 | 68.0% | 77.0% | 66.0% | **84.0%** | **+18.0%** | McNemar Exact: $p = 0.0051$ | $\alpha = 0.01$ | **`SUPPORTED`** |

---

## 2. Compute-Matching Parity Verification

- **Token Budget Balance**:
  - `B1-SC-TOKENS` Average Token Spend: 8,300 tokens per problem.
  - `B3-DEBATE` Average Token Spend: 8,500 tokens per problem.
  - Total Token Disparity: **+2.41%** (Well within the mandatory $\pm 10\%$ tolerance window).
- **False Consensus Rate in Debate**:
  - On Closed Reasoning, in 8.2% of problems an initially correct agent was persuaded to adopt an incorrect peer consensus.
  - On Private Information, cross-examination corrected peer blind spots in 24.5% of problems.
