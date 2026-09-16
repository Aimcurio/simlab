# PX-02: RP-01 Raw Results Report
**Experiment ID**: `EXP-RP01-RECENCY-V1`  
**Primitive**: `PR-COG-01` (Memory Recency / Retrieval Scoring)  
**Dataset**: `SimLab-MemBench-500` (SHA-256: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800`)  
**Telemetry File**: `telemetry/rp01/rp01_raw_telemetry.jsonl` (SHA-256: `c2b967ea83b668d9b31421141c7038cf45fc41c604eb60976cb02f43c56dbb59`)  
**Evaluation Runs**: 100 queries across 4 conditions (400 total retrieval episodes)  
**Deterministic Compute Spend**: 0 LLM API calls, $0.00 USD runtime spend  

---

## 1. Aggregate Metric Summary Table

| Condition | Description | Mean MRR | Std Dev MRR | Mean NDCG@5 | Std Dev NDCG@5 | Temporal Inversion Rate | Target in Top-5 (%) |
|---|---|---|---|---|---|---|---|
| **B0-Historical** | Smallville inverted rank recency (`retrieve.py:145-146`) | **0.0718** | 0.0993 | **0.0740** | 0.1703 | **74.50%** | 16.0% |
| **B0-NoRecency** | Pure relevance + importance ($\alpha=0, \beta=1, \gamma=1$) | **0.1514** | 0.2811 | **0.1305** | 0.3079 | **44.50%** | 16.0% |
| **T-AltWeight** | Exponential decay with tuned weights ($\alpha=0.3, \beta=0.5, \gamma=0.2$) | **0.2403** | 0.3401 | **0.2140** | 0.3724 | **42.10%** | 28.0% |
| **T-Corrected** | Exponential decay ($s = 0.995^{\Delta t}$), published equal weights | **0.1164** | 0.1228 | **0.0852** | 0.1966 | **41.00%** | **16.0%** |

---

## 2. Query Stratification Breakdown (Mean MRR)

| Query Category | Query Count | B0-Historical MRR | B0-NoRecency MRR | T-AltWeight MRR | T-Corrected MRR | Relative Gain (T-Corr vs B0-Hist) |
|---|---|---|---|---|---|---|
| **Recency-Sensitive** | 40 | 0.0182 | 0.0240 | 0.3050 | **0.1407** | **+673.7%** |
| **Relevance-Dominant** | 40 | 0.1510 | 0.3407 | 0.0433 | **0.0416** | **+-72.4%** |
| **Temporal-Conflict** | 20 | 0.0204 | 0.0278 | 0.5048 | **0.2174** | **+963.4%** |
