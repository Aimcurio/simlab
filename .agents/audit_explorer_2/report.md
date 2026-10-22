# Bounded Scientific Audit: EXP-AB-01-COMP
## Sub-Investigation Report: Requirements R4 (Mechanistic Failure Audit) and R6 (Weight Configuration Integrity)
**Agent**: `audit_explorer_2` (Explorer / Auditor)  
**Date**: 2026-09-16  
**Working Directory**: `E:\projects\simlab\.agents\audit_explorer_2`  
**Dataset**: `SimLab-MemBench-500` (SHA-256: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800`)  
**Telemetry File**: `exp_ab_01_comp_telemetry.jsonl` (SHA-256: `9eb6846b017f76883418e3703dd9f0111182e8dc8a0ea03bb5cd32dd27337eac`, 800 events)  
**Results File**: `exp_ab_01_comp_results.json` (SHA-256: `a9a6b185347209774a3f25c7efc862bc7d00f6ee4f828a2524a2cb5e5ae1be67`)  

---

## 1. Executive Summary & Verdicts

This report provides the complete, empirically grounded investigation of **Requirement R4 (Mechanistic Failure Audit)** and **Requirement R6 (Validate Weight Configurations)** for the post-execution audit of `EXP-AB-01-COMP` (`PR-COG-01` Tri-Factor Retrieval Ablation).

### Summary of Key Findings:
1. **R6 Integrity Verdict**: `NO_EXPERIMENT_CONFIGURATION_DRIFT`.
   - All 8 conditions (A1 through A8) executed in `run_exp_ab_01_comp.py` and recorded in `exp_ab_01_comp_results.json` and `exp_ab_01_comp_telemetry.jsonl` strictly match the AS-03 preregistration.
   - Specifically: A4 executed at $(\alpha=0.3, \beta=0.7, \gamma=0.0)$, A7 executed at $(\alpha=0.2, \beta=0.5, \gamma=0.3)$, and A8 executed at $(\alpha=0.2, \beta=0.5, \gamma=0.3)$ over the augmented memory store containing 100 synthesized reflection nodes (20%).
   - All dataset and telemetry hashes are bit-for-bit immutable and intact.

2. **R4 Mechanistic Verdict: The Tri-Factor Collapse in A7 (MRR 0.0941 vs A4 MRR 0.5002) is a Benchmark-Coupled Orthogonal Noise Amplification Failure**:
   - The collapse of A7 is **NOT** caused by scale inversion, code bugs, tie-breaking artifacts, or label leakage.
   - The root cause is that **prompt-assigned static importance is virtually uncorrelated with ground-truth query relevance** (Pearson $r = +0.0182$, $p = 4.54 \times 10^{-5}$, $R^2 = 0.00033$).
   - In the candidate pool of 500 memories, **an average of 188.4 distractors (37.8%) have higher importance than the ground-truth target memory**.
   - In the crucial top-10% semantic neighborhood (where distractors share the same topic as the target and have cosine similarities $\sim 0.945$ vs target $\sim 0.979$), the target's semantic score advantage at $\beta=0.5$ is only $+0.0147$. However, the distractor's importance advantage at $\gamma=0.3$ is $+0.1029$ (**7.0x larger than the semantic margin**).
   - In condition A7, in **100% of queries (100/100)**, the target memory was beaten by at least one distractor (score margin max is $-0.0255$). The target never ranked #1 or #2 in any query under A7 (minimum rank was 3.0, median 13.0).
   - In contrast, Condition A4 drops importance entirely ($\gamma = 0.0$) and elevates semantic relevance to $\beta=0.7$. Without importance noise, the semantic and recency signals cleanly separate the target, delivering MRR 0.5002 (median rank 2.5).
   - Across the 66-point weight simplex sweep, the mean MRR strictly and monotonically degrades as importance weight $\gamma$ increases: from $0.5232$ at $\gamma=0.0$, collapsing down to $0.0086$ at $\gamma=1.0$.

3. **R4 Reflection Failure in A8 (MRR 0.0325, 100% Crowding)**:
   - Diagnosed as a combination of **Normalization Mismatch** and **Reflection Score Dominance**.
   - Episodic memories have importance scores bounded in $[4.01, 6.00]$. Reflection nodes were synthesized with static importance $= 8.50$.
   - Per-query min-max normalization over the augmented pool $[4.01, 8.50]$ compresses all episodic memories into normalized importance $\le 0.4432$, while giving reflection nodes $1.0000$.
   - This creates a structural $+0.1670$ score bonus for reflection nodes. Because reflection nodes are centroids of recent episodic clusters, their recency is high and their semantic similarity to topic queries is high. As a result, reflection nodes captured 100% of Rank-1 slots (100/100) and 100% of Top-5 slots (500/500), completely crowding out ground-truth episodic memories.

---

## 2. R6: Validate Weight Configurations & Configuration Integrity

### 2.1 Preregistration Comparison Table (AS-03 vs Harness Execution)
Every condition from AS-03 (`ablation_design/AS-03_memory_ablation_plan.md`, Section 2) was checked against the harness (`run_exp_ab_01_comp.py`, lines 154–162) and telemetry results (`exp_ab_01_comp_results.json`, `condition_summaries`):

| Condition Code | Condition Name | AS-03 Expected Weights $(\alpha, \beta, \gamma)$ | Executed Weights in Harness / Results | Memory Pool Structure | Match? |
|:---|:---|:---|:---|:---|:---:|
| **A1** | `RECENCY_ONLY` | $(1.0, 0.0, 0.0)$ | $[1.0, 0.0, 0.0]$ | Base Pool (500 memories) | **TRUE** |
| **A2** | `RELEVANCE_ONLY` | $(0.0, 1.0, 0.0)$ | $[0.0, 1.0, 0.0]$ | Base Pool (500 memories) | **TRUE** |
| **A3** | `IMPORTANCE_ONLY` | $(0.0, 0.0, 1.0)$ | $[0.0, 0.0, 1.0]$ | Base Pool (500 memories) | **TRUE** |
| **A4** | `RECENCY_RELEVANCE` | $(0.3, 0.7, 0.0)$ | $[0.3, 0.7, 0.0]$ | Base Pool (500 memories) | **TRUE** |
| **A5** | `RECENCY_IMPORTANCE` | $(0.5, 0.0, 0.5)$ | $[0.5, 0.0, 0.5]$ | Base Pool (500 memories) | **TRUE** |
| **A6** | `RELEVANCE_IMPORTANCE` | $(0.0, 0.7, 0.3)$ | $[0.0, 0.7, 0.3]$ | Base Pool (500 memories) | **TRUE** |
| **A7** | `FULL_TRI_FACTOR` | $(0.2, 0.5, 0.3)$ | $[0.2, 0.5, 0.3]$ | Base Pool (500 memories) | **TRUE** |
| **A8** | `TRI_FACTOR_REFLECTION` | $(0.2, 0.5, 0.3)$ | $[0.2, 0.5, 0.3]$ | Augmented Pool (600 memories: 500 base + 100 refl) | **TRUE** |

### 2.2 Telemetry & Dataset Integrity Audit
- **Benchmark Dataset**: `E:\projects\simlab\phase3_execution\SimLab_MemBench_500.json`
  - Expected SHA-256: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800`
  - Computed SHA-256: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800`
  - Integrity Verdict: **MATCH (VERIFIED)**
- **Telemetry File**: `E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_telemetry.jsonl`
  - Expected SHA-256: `9eb6846b017f76883418e3703dd9f0111182e8dc8a0ea03bb5cd32dd27337eac`
  - Computed SHA-256: `9eb6846b017f76883418e3703dd9f0111182e8dc8a0ea03bb5cd32dd27337eac`
  - Event Count: 800 events (100 queries $\times$ 8 conditions)
  - Integrity Verdict: **MATCH (VERIFIED)**
- **Results File**: `E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_results.json`
  - SHA-256: `a9a6b185347209774a3f25c7efc862bc7d00f6ee4f828a2524a2cb5e5ae1be67`
  - Event Count: 8 condition summaries, 7 comparison records, 66 simplex sweep points.
  - Integrity Verdict: **MATCH (VERIFIED)**

### 2.3 Configuration Drift Adjudication
- **Verdict**: `NO_EXPERIMENT_CONFIGURATION_DRIFT`.
- All condition names, weight triplets, decay parameters ($\lambda = 0.995$), time horizon ($t_{curr} = 72.0$), candidate pool sizes, and metric functions conform strictly and without deviation to the AS-03 experimental plan.

---

## 3. R4: Mechanistic Failure Audit

### 3.1 Subsystem Mechanics Verification

| Subsystem Component | Implementation in `run_exp_ab_01_comp.py` | Audit Finding & Verification | Integrity Classification |
|:---|:---|:---|:---|
| **Normalization Method** | `min_max_norm(vals)` (lines 34–38) applies linear scaling to $[0.0, 1.0]$ per query over candidate pool. | Verified. When $\max = \min$, returns $1.0$. Stretches component ranges to uniform $[0, 1]$ bounds. | **IMPLEMENTED AS SPECIFIED** (creates dynamic range distortion in A8) |
| **Sign / Direction Semantics** | Higher timestamp $\to$ higher recency; higher cosine similarity $\to$ higher relevance; higher prompt score $\to$ higher importance. | Verified. Pearson correlations with raw values are all $+0.999$ to $+1.000$. Higher scores consistently represent "more recent", "more similar", "more important". | **CORRECT DIRECTION** (No scale inversion) |
| **Weight Application** | `scores = [alpha * r + beta * s + gamma * imp ...]` (lines 92–95) | Verified. Linear weighted sum implemented cleanly without unintended scaling coefficients or offsets. | **CORRECT APPLICATION** |
| **Score Combination** | Pointwise linear combination over $[0, 1]$ normalized arrays. | Verified. Score array length equals candidate pool length. All values bounded in $[0.0, 1.0]$ when weights sum to 1. | **MATHEMATICALLY SOUND** |
| **Tie Handling** | Python standard `sorted(..., reverse=True)` (line 99). | Timsort is stable. Tie occurrence: A1 (100/100 queries tied due to discrete timestamps), A3 (100/100 queries tied due to discrete importance), **A2, A4, A7 (0/100 queries tied)**. In continuous float combinations with relevance, ties do not occur. | **NON-IMPACTING FOR A4/A7** |
| **Sorting Direction** | `reverse=True` (line 99) sorts descending (highest score at index 0). | Verified. Rank 1 corresponds to $\max(\text{score})$. Target rank found via `.index(target_cand_idx) + 1`. | **CORRECT DIRECTION** |
| **Rank Construction** | 1-based indexing; $\text{RR} = 1.0 / \text{rank}$; $\text{NDCG@5} = 1.0 / \log_2(\text{rank} + 1)$ if $\text{rank} \le 5$ else $0.0$. | Verified. Standard evaluation formulas. | **CORRECT CONSTRUCTION** |
| **Candidate-Set Construction** | Exhaustive pool evaluation: 500 episodic memories for A1–A7; 600 memories for A8 (500 episodic + 100 reflection). | Verified. No ANN truncation, filtering, or pre-selection biases. Ground-truth target memory present in every candidate set. | **EXHAUSTIVE & VALID** |

---

### 3.2 Raw and Normalized Component Score Distributions

Across the 500 base episodic memories and the 100 benchmark queries:
- **Raw Importance**:
  - Pool ($N=500$): Min $= 4.0100$, Max $= 6.0000$, Mean $= 5.0029$, Variance $= 0.3293$, Std $= 0.5739$.
  - Quantiles (0, 25, 50, 75, 90, 95, 99, 100): $[4.010, 4.518, 5.035, 5.480, 5.801, 5.900, 5.980, 6.000]$.
  - Normalized Importance: Min $= 0.0000$, Max $= 1.0000$, Mean $= 0.4989$, Variance $= 0.0832$, Std $= 0.2881$.
- **Raw Recency ($s_{rec} = 0.995^{72.0 - t}$)**:
  - Pool ($N=500$): Min $= 0.6970$, Max $= 0.9964$, Mean $= 0.8379$, Variance $= 0.0076$, Std $= 0.0873$.
  - Quantiles (0, 25, 50, 75, 90, 95, 99, 100): $[0.6970, 0.7622, 0.8334, 0.9113, 0.9614, 0.9788, 0.9928, 0.9964]$.
  - Normalized Recency: Min $= 0.0000$, Max $= 1.0000$, Mean $= 0.4706$, Variance $= 0.0850$, Std $= 0.2913$.
- **Cosine Relevance ($s_{rel} = \cos(\mathbf{q}, \mathbf{m})$)**:
  - All Pairs ($N=50,000$): Min $= -0.2151$, Max $= 0.9991$, Mean $= 0.1820$, Variance $= 0.1467$, Std $= 0.3830$.
  - Target Memories ($N=100$): Min $= 0.9338$, Max $= 0.9991$, Mean $= 0.9792$, Variance $= 0.0004$, Std $= 0.0202$.
  - Distractor Memories ($N=49,900$): Min $= -0.2151$, Max $= 0.9925$, Mean $= 0.1804$, Variance $= 0.1457$, Std $= 0.3817$.
  - Normalized Relevance (per query): Min $= 0.0000$, Max $= 1.0000$, Mean $= 0.3056$, Variance $= 0.1088$, Std $= 0.3298$.

---

### 3.3 Condition-by-Condition Score Distribution Tables (A1–A8)

#### Table 1: Overall Candidate Pool Score Distributions (100 queries $\times$ candidate pool size)
| Condition | Min | Q25 | Q50 (Median) | Mean | Q75 | Q95 | Max | Variance | Std Dev |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A1 (RECENCY_ONLY)** | 0.0000 | 0.2176 | 0.4555 | 0.4706 | 0.7156 | 0.9411 | 1.0000 | 0.0849 | 0.2913 |
| **A2 (RELEVANCE_ONLY)** | 0.0000 | 0.1163 | 0.1569 | 0.3056 | 0.2254 | 0.9788 | 1.0000 | 0.1088 | 0.3298 |
| **A3 (IMPORTANCE_ONLY)** | 0.0000 | 0.2550 | 0.5151 | 0.4989 | 0.7387 | 0.9497 | 1.0000 | 0.0830 | 0.2881 |
| **A4 (RECENCY_RELEVANCE)** | 0.0076 | 0.1835 | 0.2749 | 0.3551 | 0.3890 | 0.8868 | 0.9992 | 0.0610 | 0.2469 |
| **A5 (RECENCY_IMPORTANCE)**| 0.0152 | 0.3342 | 0.4808 | 0.4848 | 0.6452 | 0.8344 | 0.9328 | 0.0428 | 0.2069 |
| **A6 (RELEVANCE_IMPORTANCE)**| 0.0075 | 0.1956 | 0.2872 | 0.3636 | 0.3884 | 0.8925 | 0.9970 | 0.0608 | 0.2465 |
| **A7 (FULL_TRI_FACTOR)** | 0.0203 | 0.2552 | 0.3544 | 0.3966 | 0.4815 | 0.8087 | 0.9623 | 0.0383 | 0.1956 |
| **A8 (TRI_FACTOR_REFLECTION)**| 0.0193 | 0.2028 | 0.2867 | 0.3527 | 0.4886 | 0.7359 | 1.0000 | 0.0399 | 0.1997 |

#### Table 2: Ground-Truth Target Memory Score Distributions (100 queries)
| Condition | Min | Q25 | Q50 (Median) | Mean | Q75 | Q95 | Max | Variance | Std Dev |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A1** | 0.4605 | 0.4605 | 1.0000 | 0.7842 | 1.0000 | 1.0000 | 1.0000 | 0.0706 | 0.2656 |
| **A2** | 0.9594 | 0.9830 | 0.9983 | 0.9915 | 1.0000 | 1.0000 | 1.0000 | 0.0001 | 0.0116 |
| **A3** | 0.1357 | 0.5176 | 0.6281 | 0.6163 | 0.7437 | 0.9146 | 0.9146 | 0.0536 | 0.2315 |
| **A4** | 0.8381 | 0.8381 | 0.9798 | 0.9293 | 0.9949 | 0.9988 | 0.9992 | 0.0056 | 0.0751 |
| **A5** | 0.4312 | 0.6021 | 0.6875 | 0.7002 | 0.7940 | 0.8719 | 0.8719 | 0.0157 | 0.1254 |
| **A6** | 0.7321 | 0.8467 | 0.8757 | 0.8789 | 0.9231 | 0.9744 | 0.9744 | 0.0050 | 0.0706 |
| **A7** | 0.7127 | 0.8152 | 0.8590 | 0.8375 | 0.8755 | 0.9115 | 0.9223 | 0.0037 | 0.0608 |
| **A8** | 0.6455 | 0.7066 | 0.7172 | 0.7325 | 0.7673 | 0.7831 | 0.7980 | 0.0017 | 0.0418 |

#### Table 3: Target Retrieval Ranks and Score Margins ($\text{Score}_{\text{target}} - \max(\text{Score}_{\text{distractor}})$)
| Condition | Target Rank Min | Target Rank Median | Target Rank Mean | Target Rank Max | Mean Score Margin | Max Score Margin | Mean MRR | NDCG@5 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A1** | 1.0 | 5.0 | 101.0 | 250.0 | -0.2158 | 0.0000 | 0.2756 | 0.3538 |
| **A2** | 1.0 | 2.0 | 22.5 | 98.0 | +0.0053 | +0.0527 | 0.5130 | 0.5262 |
| **A3** | 39.0 | 182.0 | 191.7 | 426.0 | -0.3837 | -0.0854 | 0.0086 | 0.0000 |
| **A4** | 1.0 | 2.5 | 15.5 | 42.0 | -0.0439 | +0.0335 | 0.5002 | 0.5170 |
| **A5** | 16.0 | 102.0 | 100.0 | 293.0 | -0.2325 | -0.0609 | 0.0205 | 0.0000 |
| **A6** | 1.0 | 33.5 | 31.9 | 84.0 | -0.0938 | +0.0263 | 0.1695 | 0.1691 |
| **A7** | **3.0** | **13.0** | **19.4** | **54.0** | **-0.0985** | **-0.0255** | **0.0941** | **0.0450** |
| **A8** | **21.0** | **32.0** | **34.0** | **61.0** | **-0.2569** | **-0.1969** | **0.0325** | **0.0000** |

---

### 3.4 In-Depth Analysis: Why A7 Collapsed (MRR 0.0941) vs A4 (MRR 0.5002)

#### 3.4.1 Empirical Correlation with Ground-Truth Target Relevance
We evaluated the point-biserial, Pearson, and Spearman correlations between each component score and the binary target indicator ($Y=1$ for the ground-truth target, $Y=0$ for the 499 distractors) across all $N = 50,000$ query-memory instances:

| Component | Pearson Correlation $r$ | $p$-value | Spearman Rank Correlation $\rho$ | Variance Explained ($R^2$) |
|:---|:---:|:---:|:---:|:---:|
| **Cosine Relevance ($s_{rel}$)** | **+0.0932** | $7.60 \times 10^{-97}$ | +0.0740 | 0.87% |
| **Recency Decay ($s_{rec}$)** | **+0.0482** | $4.15 \times 10^{-27}$ | +0.0464 | 0.23% |
| **Static Importance ($s_{imp}$)** | **+0.0182** | $4.54 \times 10^{-5}$ | +0.0185 | **0.03%** |

**Observation**: Static importance possesses practically zero mutual information or correlation with ground-truth relevance ($r = 0.0182$). It explains only 0.03% of the target identity variance.

#### 3.4.2 The Distractor-Amplifier Phenomenon
In SimLab-MemBench-500:
- The target memory importance mean is $5.2364 \pm 0.4583$.
- The distractor memory importance mean is $5.0024 \pm 0.5734$ (ranging from $4.0100$ to $6.0000$).
- Because the distractor pool contains 499 memories and importance has a standard deviation of $0.57$, **an average of 188.4 distractors per query (37.8% of the memory store) have an importance score strictly higher than the target memory**.
- For recency-sensitive queries, target memories have mean importance $5.0500$, meaning **234.6 distractors (47.0%) have higher importance than the target**.
- For temporal-conflict queries, target memories have mean importance $5.0500$, meaning **234.6 distractors (47.0%) have higher importance than the target**.

#### 3.4.3 Decomposition of the Near-Target Competition
Why does a $+0.0182$ noise term collapse retrieval so violently? The answer lies in the **local score margin** between the target and the top distractors in the semantic neighborhood:
In condition A7 ($\alpha=0.2, \beta=0.5, \gamma=0.3$):
- **Target Memory**:
  - Semantic contribution ($\beta \cdot s_{rel}$): $0.5 \times 0.9914 = 0.4957$ (raw cosine $= 0.9792$)
  - Recency contribution ($\alpha \cdot s_{rec}$): $0.2 \times 0.7842 = 0.1568$ (raw recency $= 0.9318$)
  - Importance contribution ($\gamma \cdot s_{imp}$): $0.3 \times 0.6163 = 0.1849$ (raw importance $= 5.2364$)
  - **Total Target Score**: $0.8375 \pm 0.0605$
- **Rank-1 Distractor Memory**:
  - Semantic contribution: $0.5 \times 0.9622 = 0.4811$ (raw cosine $= 0.9446$)
  - Recency contribution: $0.2 \times 0.8350 = 0.1670$ (raw recency $= 0.9470$)
  - Importance contribution: $0.3 \times 0.9594 = \mathbf{0.2878}$ (raw importance $= 5.9192$)
  - **Total Distractor Score**: $0.9359 \pm 0.0192$

**Component Margin Breakdown**:
$$\Delta \text{Relevance} = 0.4957 - 0.4811 = \mathbf{+0.0147} \quad (\text{Target leads by } 0.0147)$$
$$\Delta \text{Recency} = 0.1568 - 0.1670 = -0.0102 \quad (\text{Distractor leads by } 0.0102)$$
$$\Delta \text{Importance} = 0.1849 - 0.2878 = \mathbf{-0.1029} \quad (\text{Distractor leads by } 0.1029)$$
$$\Delta \text{Total Score} = 0.8375 - 0.9359 = \mathbf{-0.0985} \quad (\text{Distractor beats Target by } 0.0985)$$

**The Causal Mechanism**:
The distractor's importance advantage ($+0.1029$) is **7.0 times larger** than the target's semantic relevance advantage ($+0.0147$). By lowering $\beta$ from $0.7$ (in A4) to $0.5$ (in A7), the semantic discriminatory margin was compressed. Simultaneously, allocating $\gamma=0.3$ opened an ungrounded importance noise window of up to $+0.3000$. Among the dozens of distractors in the same topic cluster having high semantic similarity ($\cos \approx 0.94$), any distractor with high prompt importance ($5.8 - 6.0$) inevitably leaps over the target memory.
Consequently, **in 100 out of 100 queries in A7, the target memory was pushed out of Rank 1**. The maximum score margin across all 100 queries was $-0.0255$, and the median target rank was pushed down to 13.0.

#### 3.4.4 Continuous Weight Simplex Sweep Evidence
The 66-point 2D simplex sweep ($\alpha + \beta + \gamma = 1.0$, step size $0.1$) provides definitive empirical confirmation of the distractor-amplifier mechanism:
- **Optimal Simplex Point**: $(\alpha=0.7, \beta=0.3, \gamma=0.0) \to \text{MRR} = \mathbf{0.6036}$ (NDCG@5 $= 0.6000$)
- **Worst Simplex Point**: $(\alpha=0.0, \beta=0.0, \gamma=1.0) \to \text{MRR} = \mathbf{0.0086}$ (NDCG@5 $= 0.0000$)
- **Monotonic Degradation with Gamma**:
  - $\gamma = 0.0$ ($N=11$ points): Mean $\text{MRR} = \mathbf{0.5232}$ (Max $= 0.6036$)
  - $\gamma = 0.1$ ($N=10$ points): Mean $\text{MRR} = 0.3718$ (Max $= 0.4555$)
  - $\gamma = 0.2$ ($N=9$ points): Mean $\text{MRR} = 0.2601$ (Max $= 0.4078$)
  - $\gamma = 0.3$ ($N=8$ points): Mean $\text{MRR} = 0.1547$ (Max $= 0.2322$)
  - $\gamma = 0.4$ ($N=7$ points): Mean $\text{MRR} = 0.0875$ (Max $= 0.1514$)
  - $\gamma = 0.5$ ($N=6$ points): Mean $\text{MRR} = 0.0547$ (Max $= 0.0809$)
  - $\gamma = 0.6$ ($N=5$ points): Mean $\text{MRR} = 0.0391$ (Max $= 0.0544$)
  - $\gamma = 0.7$ ($N=4$ points): Mean $\text{MRR} = 0.0284$ (Max $= 0.0416$)
  - $\gamma = 0.8$ ($N=3$ points): Mean $\text{MRR} = 0.0212$ (Max $= 0.0333$)
  - $\gamma = 0.9$ ($N=2$ points): Mean $\text{MRR} = 0.0171$ (Max $= 0.0254$)
  - $\gamma = 1.0$ ($N=1$ point): Mean $\text{MRR} = \mathbf{0.0086}$ (Max $= 0.0086$)

Every $+0.1$ increment in $\gamma$ monotonically degrades mean MRR across the entire simplex. Importance acts strictly as a destructive noise injector under offline vector retrieval.

---

### 3.5 Systematic Falsification Tests for 8 Specific Failure Modes

| Failure Mode | Test Hypothesis | Empirical Test Method & Evidence | Verdict | Classification |
|:---|:---|:---|:---:|:---|
| **1. Scale Dominance** | One component numerically overwhelms total score variance across the board. | Variance across 500 nodes: $Var(s_{rel})=0.1088$ ($0.25 \times Var = 0.0272$), $Var(s_{rec})=0.0850$ ($0.04 \times Var = 0.0034$), $Var(s_{imp})=0.0832$ ($0.09 \times Var = 0.0075$). Globally, relevance has highest variance. However, in the local semantic neighborhood ($\cos > 0.90$), relevance variance collapses to $0.0004$, allowing importance variance ($0.0832$) to dominate. | **LOCAL DOMINANCE CONFIRMED** | **PRIMITIVE INTERACTION ARTIFACT** |
| **2. Scale Inversion** | Decay or scoring operates in reverse (older nodes or lower relevance get higher scores). | Pearson $r$ between raw timestamp and normalized recency is $+0.9989$. Correlation between raw importance and normalized importance is $+1.0000$. Correlation between cosine similarity and normalized relevance is $+1.0000$. Sorting order is strictly descending (`reverse=True`). | **FALSIFIED** | **NO DEFECT** |
| **3. Normalization Mismatch** | Min-max normalization produces incompatible dynamic ranges between components or conditions. | In A1–A7, all components are cleanly scaled to $[0.0, 1.0]$. In **A8**, adding reflection nodes with importance $8.50$ (vs episodic range $[4.01, 6.00]$) compresses all episodic memories into $[0.0, 0.4432]$ while pinning reflection nodes at $1.0000$. | **CONFIRMED IN A8** (Falsified in A1-A7) | **SCORING_SCALE_ARTIFACT** |
| **4. Weight Application Error** | Scoring code misapplies weights or inverts linear formulation. | Code inspection of `run_exp_ab_01_comp.py` lines 92–95 confirms exact formulation $\alpha r + \beta s + \gamma imp$. Weights match AS-03 exactly. | **FALSIFIED** | **NO DEFECT** |
| **5. Reflection Score Dominance** | Reflection nodes crowd out episodic nodes due to elevated composite scores. | In A8, reflection nodes occupy 100% of Rank-1 slots (100/100) and 100% of Top-5 slots (500/500). Mean reflection score $= 0.9894$ vs target score $= 0.7325$ (reflection leads by $+0.2569$). Component breakdown shows reflection leads by $+0.2181$ on importance and $+0.0432$ on recency. | **CONFIRMED** | **IMPLEMENTATION_DEFECT & SCORING_SCALE_ARTIFACT** |
| **6. Duplicate Crowding** | Duplicate or identical memory embeddings crowd out targets. | Base memory pool has 500 unique IDs. Max pairwise cosine similarity between non-identical episodic nodes is $0.9809$. Zero identical vector duplicates exist ($0 > 0.9999$). | **FALSIFIED** | **NO DEFECT** |
| **7. Label Leakage** | Target ID or ground-truth label leaks into score calculation. | Code inspection confirms `evaluate_query` computes scores strictly from `qvec` and candidate metadata. `target_id` is accessed exclusively on line 100 after score computation and sorting are completed. | **FALSIFIED** | **NO DEFECT** |
| **8. Benchmark Bias** | Benchmark assigns static importance uncorrelated with ground-truth relevance. | Target importance mean is $5.2364$ vs pool mean $5.0029$. Pearson $r = +0.0182$ ($R^2 = 0.00033$). For recency-sensitive and conflict queries, target importance ($5.0500$) is indistinguishable from background pool. | **CONFIRMED** | **BENCHMARK_ARTIFACT** |

---

## 4. Draft Section D: Score-Distribution Audit

*(The following is the full, standalone draft text formatted for Section D of the master Bounded Scientific Audit report)*

### Section D: Score-Distribution Audit

#### D.1 Executive Verdict on Component Scoring Mechanics
The score-distribution audit of `EXP-AB-01-COMP` demonstrates that the empirical collapse of Condition A7 (Full Tri-Factor: MRR $0.0941$) relative to Condition A4 (Recency + Relevance: MRR $0.5002$) is an authentic mathematical consequence of combining a high-precision semantic similarity vector with an orthogonal, ungrounded scalar noise term (static prompt importance). 

The audit evaluated telemetry across 800 execution episodes (100 queries $\times$ 8 conditions) against the standardized `SimLab-MemBench-500` benchmark. The scoring pipeline correctly implemented 1-based ranking, descending sort direction, linear weight combination, and per-query min-max normalization. No code-level implementation bugs, scale inversions, label leakages, or tie-breaking artifacts exist in the A1–A7 execution pipeline.

#### D.2 Component Score Distributions (Raw vs Normalized)
Table D-1 presents the distributional parameters of the three retrieval components across the base episodic memory pool ($N=500$) and the query test set ($N=100$, 50,000 evaluations):

**Table D-1: Component Distribution Parameters (Base Memory Pool)**
| Component | Metric | Min | Q25 | Q50 (Median) | Mean | Q75 | Q95 | Max | Variance | Std Dev |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Importance ($s_{imp}$)** | Raw (prompt scale) | 4.0100 | 4.5175 | 5.0350 | 5.0029 | 5.4800 | 5.9000 | 6.0000 | 0.3293 | 0.5739 |
| | Min-Max Normalized | 0.0000 | 0.2550 | 0.5151 | 0.4989 | 0.7387 | 0.9497 | 1.0000 | 0.0832 | 0.2881 |
| **Recency ($s_{rec}$)** | Raw ($\lambda^{\Delta t}, \lambda=0.995$) | 0.6970 | 0.7622 | 0.8334 | 0.8379 | 0.9113 | 0.9788 | 0.9964 | 0.0076 | 0.0873 |
| | Min-Max Normalized | 0.0000 | 0.2176 | 0.4555 | 0.4706 | 0.7156 | 0.9411 | 1.0000 | 0.0850 | 0.2913 |
| **Relevance ($s_{rel}$)** | Raw Cosine (Distractors) | -0.2151 | -0.0375 | 0.0104 | 0.1804 | 0.0840 | 0.9572 | 0.9925 | 0.1457 | 0.3817 |
| | Raw Cosine (Targets) | 0.9338 | 0.9604 | 0.9865 | 0.9792 | 0.9984 | 0.9990 | 0.9991 | 0.0004 | 0.0202 |
| | Min-Max Normalized (Pool) | 0.0000 | 0.1163 | 0.1569 | 0.3056 | 0.2254 | 0.9788 | 1.0000 | 0.1088 | 0.3298 |

#### D.3 Comprehensive Condition Score Distributions (Conditions A1 through A8)
Table D-2 summarizes the overall score distributions across all candidate memories, Table D-3 reports the score distributions for ground-truth target memories, and Table D-4 presents target retrieval ranks and competitive score margins.

**Table D-2: Overall Score Distribution Across Candidate Pool (100 Queries $\times$ Pool Size)**
| Condition | Weights $(\alpha, \beta, \gamma)$ | Min | Q25 | Q50 | Mean | Q75 | Q95 | Max | Variance | Std Dev |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A1 (RECENCY_ONLY)** | $(1.0, 0.0, 0.0)$ | 0.0000 | 0.2176 | 0.4555 | 0.4706 | 0.7156 | 0.9411 | 1.0000 | 0.0849 | 0.2913 |
| **A2 (RELEVANCE_ONLY)** | $(0.0, 1.0, 0.0)$ | 0.0000 | 0.1163 | 0.1569 | 0.3056 | 0.2254 | 0.9788 | 1.0000 | 0.1088 | 0.3298 |
| **A3 (IMPORTANCE_ONLY)** | $(0.0, 0.0, 1.0)$ | 0.0000 | 0.2550 | 0.5151 | 0.4989 | 0.7387 | 0.9497 | 1.0000 | 0.0830 | 0.2881 |
| **A4 (RECENCY_RELEVANCE)** | $(0.3, 0.7, 0.0)$ | 0.0076 | 0.1835 | 0.2749 | 0.3551 | 0.3890 | 0.8868 | 0.9992 | 0.0610 | 0.2469 |
| **A5 (RECENCY_IMPORTANCE)** | $(0.5, 0.0, 0.5)$ | 0.0152 | 0.3342 | 0.4808 | 0.4848 | 0.6452 | 0.8344 | 0.9328 | 0.0428 | 0.2069 |
| **A6 (RELEVANCE_IMPORTANCE)** | $(0.0, 0.7, 0.3)$ | 0.0075 | 0.1956 | 0.2872 | 0.3636 | 0.3884 | 0.8925 | 0.9970 | 0.0608 | 0.2465 |
| **A7 (FULL_TRI_FACTOR)** | $(0.2, 0.5, 0.3)$ | 0.0203 | 0.2552 | 0.3544 | 0.3966 | 0.4815 | 0.8087 | 0.9623 | 0.0383 | 0.1956 |
| **A8 (TRI_FACTOR_REFLECTION)**| $(0.2, 0.5, 0.3)$ | 0.0193 | 0.2028 | 0.2867 | 0.3527 | 0.4886 | 0.7359 | 1.0000 | 0.0399 | 0.1997 |

**Table D-3: Target Memory Score Distributions (100 Queries)**
| Condition | Min | Q25 | Q50 | Mean | Q75 | Q95 | Max | Target Variance | Target Std |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A1** | 0.4605 | 0.4605 | 1.0000 | 0.7842 | 1.0000 | 1.0000 | 1.0000 | 0.0706 | 0.2656 |
| **A2** | 0.9594 | 0.9830 | 0.9983 | 0.9915 | 1.0000 | 1.0000 | 1.0000 | 0.0001 | 0.0116 |
| **A3** | 0.1357 | 0.5176 | 0.6281 | 0.6163 | 0.7437 | 0.9146 | 0.9146 | 0.0536 | 0.2315 |
| **A4** | 0.8381 | 0.8381 | 0.9798 | 0.9293 | 0.9949 | 0.9988 | 0.9992 | 0.0056 | 0.0751 |
| **A5** | 0.4312 | 0.6021 | 0.6875 | 0.7002 | 0.7940 | 0.8719 | 0.8719 | 0.0157 | 0.1254 |
| **A6** | 0.7321 | 0.8467 | 0.8757 | 0.8789 | 0.9231 | 0.9744 | 0.9744 | 0.0050 | 0.0706 |
| **A7** | 0.7127 | 0.8152 | 0.8590 | 0.8375 | 0.8755 | 0.9115 | 0.9223 | 0.0037 | 0.0608 |
| **A8** | 0.6455 | 0.7066 | 0.7172 | 0.7325 | 0.7673 | 0.7831 | 0.7980 | 0.0017 | 0.0418 |

**Table D-4: Target Ranks, Score Margins, and Benchmark Performance**
| Condition | Target Rank Min | Target Rank Median | Target Rank Mean | Target Rank Max | Mean Margin ($\Delta s$) | Max Margin ($\Delta s$) | MRR | NDCG@5 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A1** | 1.0 | 5.0 | 101.0 | 250.0 | -0.2158 | 0.0000 | 0.2756 | 0.3538 |
| **A2** | 1.0 | 2.0 | 22.5 | 98.0 | +0.0053 | +0.0527 | 0.5130 | 0.5262 |
| **A3** | 39.0 | 182.0 | 191.7 | 426.0 | -0.3837 | -0.0854 | 0.0086 | 0.0000 |
| **A4** | 1.0 | 2.5 | 15.5 | 42.0 | -0.0439 | +0.0335 | 0.5002 | 0.5170 |
| **A5** | 16.0 | 102.0 | 100.0 | 293.0 | -0.2325 | -0.0609 | 0.0205 | 0.0000 |
| **A6** | 1.0 | 33.5 | 31.9 | 84.0 | -0.0938 | +0.0263 | 0.1695 | 0.1691 |
| **A7** | **3.0** | **13.0** | **19.4** | **54.0** | **-0.0985** | **-0.0255** | **0.0941** | **0.0450** |
| **A8** | **21.0** | **32.0** | **34.0** | **61.0** | **-0.2569** | **-0.1969** | **0.0325** | **0.0000** |

#### D.4 Mechanistic Failure Diagnosis: The Tri-Factor Collapse in A7
The statistical comparison between A4 and A7 reveals a massive, statistically significant degradation ($\Delta \text{MRR} = -0.4061$, Wilcoxon $W = 784.0$, $p = 2.14 \times 10^{-9}$, Cohen's $d = -0.9342$). The causal explanation is established through three mathematical facts:

1. **Near-Zero Semantic Information in Importance**: Pearson correlation between static importance and ground-truth target relevance is $r = +0.0182$ ($p = 4.54 \times 10^{-5}$, $R^2 = 0.00033$). Static importance is essentially orthogonal noise with respect to query intent.
2. **Abundance of High-Importance Distractors**: Across the 500-node pool, an average of $188.4$ distractors ($37.8\%$) possess higher importance than the target memory.
3. **Local Scale Incommensurability in Near-Target Neighborhoods**: In the dense semantic cluster surrounding a query, competing distractors on the same topic have cosine similarities of $\sim 0.945$, while the target has $\sim 0.979$. At $\beta=0.5$, the target's semantic margin is only $+0.0147$. In contrast, distractors with high static importance ($5.8 - 6.0$) gain an importance score advantage of $+0.1029$ at $\gamma=0.3$. Because $+0.1029$ is **7.0 times larger** than $+0.0147$, the importance noise term completely swamps semantic discrimination. In 100% of queries under A7, the target is defeated by distractors, resulting in a maximum target rank of 3.0 and median rank of 13.0.

In Condition A4, setting $\gamma=0.0$ eliminates this noise term, allowing semantic relevance ($\beta=0.7$) and recency ($\alpha=0.3$) to correctly position the target at median rank 2.5 (MRR $0.5002$).

#### D.5 Reflection Contamination Diagnosis in Condition A8
Condition A8 collapsed to MRR $0.0325$ with 100% Rank-1 crowding ($100/100$ queries) and 100% Top-5 crowding ($500/500$ slots). The mechanism is an implementation and scale artifact:
- Synthesized reflection nodes were assigned static importance $= 8.50$, far exceeding the episodic distribution $[4.01, 6.00]$.
- Min-max normalization over $[4.01, 8.50]$ compressed all episodic memories into $[0.0, 0.4432]$, while granting reflection nodes $1.0000$.
- With $\gamma=0.3$, reflection nodes received a guaranteed $+0.1670$ structural score bonus over the best episodic memory.
- Clustered centroid embeddings and recent timestamps endowed reflection nodes with both high cosine relevance and high recency.
- Reflection nodes consequently formed an impenetrable score barrier, completely suppressing ground-truth episodic recall.

---

## 5. Draft Section F: Configuration Integrity Check

*(The following is the full, standalone draft text formatted for Section F of the master Bounded Scientific Audit report)*

### Section F: Configuration Integrity Check

#### F.1 Purpose and Audit Protocol
The purpose of Section F is to verify whether the executed experiment `EXP-AB-01-COMP` conformed strictly to the preregistered experimental protocol defined in `AS-03: Memory Component Ablation Plan` (`E:\projects\simlab\ablation_design\AS-03_memory_ablation_plan.md`). 

Under Curo research governance, any undeclared deviation in scoring formulation, component weights, baseline definitions, candidate pool construction, or benchmark data constitutes `EXPERIMENT_CONFIGURATION_DRIFT`, requiring an immediate halt to the experimentation lifecycle.

#### F.2 Preregistered vs Executed Configuration Ledger
Table F-1 compares the preregistered requirements from AS-03 against the executed configurations from `run_exp_ab_01_comp.py`, validated against the immutable telemetry ledger `exp_ab_01_comp_telemetry.jsonl` and summary output `exp_ab_01_comp_results.json`.

**Table F-1: Experimental Configuration Verification Matrix**
| Condition Code | Condition Name | Theoretical Purpose | AS-03 Expected Weights $(\alpha, \beta, \gamma)$ | Executed Weights in Harness / Results | Memory Pool Structure | Integrity Match? |
|:---:|:---|:---|:---:|:---:|:---|:---:|
| **A1** | `RECENCY_ONLY` | Isolate temporal decay without semantic grounding | $(1.0, 0.0, 0.0)$ | $[1.0, 0.0, 0.0]$ | Base Pool (500 nodes) | **TRUE** |
| **A2** | `RELEVANCE_ONLY` | Traditional dense vector similarity baseline | $(0.0, 1.0, 0.0)$ | $[0.0, 1.0, 0.0]$ | Base Pool (500 nodes) | **TRUE** |
| **A3** | `IMPORTANCE_ONLY` | Static salience retrieval baseline | $(0.0, 0.0, 1.0)$ | $[0.0, 0.0, 1.0]$ | Base Pool (500 nodes) | **TRUE** |
| **A4** | `RECENCY_RELEVANCE` | Test temporal decay combined strictly with semantics | $(0.3, 0.7, 0.0)$ | $[0.3, 0.7, 0.0]$ | Base Pool (500 nodes) | **TRUE** |
| **A5** | `RECENCY_IMPORTANCE`| Non-semantic heuristic retrieval | $(0.5, 0.0, 0.5)$ | $[0.5, 0.0, 0.5]$ | Base Pool (500 nodes) | **TRUE** |
| **A6** | `RELEVANCE_IMPORTANCE`| Standard RAG with static priority weighting | $(0.0, 0.7, 0.3)$ | $[0.0, 0.7, 0.3]$ | Base Pool (500 nodes) | **TRUE** |
| **A7** | `FULL_TRI_FACTOR` | Reconciled Phase 3 tuned weighting configuration | $(0.2, 0.5, 0.3)$ | $[0.2, 0.5, 0.3]$ | Base Pool (500 nodes) | **TRUE** |
| **A8** | `TRI_FACTOR_REFLECTION`| A7 scoring over memory store with 20% reflections | $(0.2, 0.5, 0.3)$ | $[0.2, 0.5, 0.3]$ | Augmented Pool (600 nodes) | **TRUE** |

#### F.3 Cryptographic Artifact and Execution Invariant Verification
1. **Benchmark Integrity**:
   - Dataset Path: `E:\projects\simlab\phase3_execution\SimLab_MemBench_500.json`
   - Preregistered SHA-256: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800`
   - Executed SHA-256: `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800`
   - **Verification Status**: Bit-for-bit identical (Zero benchmark drift).

2. **Telemetry Ledger Integrity**:
   - Telemetry Path: `E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_telemetry.jsonl`
   - Recorded SHA-256: `9eb6846b017f76883418e3703dd9f0111182e8dc8a0ea03bb5cd32dd27337eac`
   - Computed SHA-256: `9eb6846b017f76883418e3703dd9f0111182e8dc8a0ea03bb5cd32dd27337eac`
   - Event Count: Exactly 800 events recorded (100 queries $\times$ 8 conditions).
   - **Verification Status**: Bit-for-bit identical (Zero telemetry tampering or data loss).

3. **Continuous Simplex Sweep Integrity**:
   - Grid Definition: $\alpha + \beta + \gamma = 1.0$ at step size $\Delta = 0.1$.
   - Executed Points: Exactly 66 grid points evaluated across all 100 queries (6,600 query evaluations).
   - **Verification Status**: Fully compliant with AS-03 Section 3.

#### F.4 Formal Adjudication on Configuration Drift
- **Adjudication**: `NO_EXPERIMENT_CONFIGURATION_DRIFT`.
- **Finding**: The execution harness `run_exp_ab_01_comp.py` faithfully and flawlessly executed the experimental design mandated by AS-03. The empirical results (including the severe collapse of A7 and A8) represent the genuine mathematical behavior of the preregistered scoring configurations under the tested benchmark, rather than an operational or procedural artifact of experimental drift.

---

## 6. Forward Constraints & Methodological Lessons Learned

From this investigation of R4 and R6, the following forward constraints must be codified for subsequent experimentation:

1. **Forward Constraint FC-RET-01: Scale Incommensurability Guard**:
   - Never combine high-precision dense vector similarities ($\cos \in [-1, 1]$ with narrow top-tier variance) with discrete or synthetic heuristic scores (e.g., prompt importance $\in [1, 10]$) using arbitrary fixed weights.
   - When heuristic scores have low correlation with target relevance ($r < 0.10$), allocating heuristic weight $\gamma \ge 0.10$ causes the heuristic variance to swamp the semantic margin, destroying retrieval precision.
2. **Forward Constraint FC-RET-02: Normalization Range Integrity for Heterogeneous Memory Pools**:
   - Min-max normalization must never be applied globally across heterogeneous node types (e.g., episodic vs reflection nodes) when those node types have different intrinsic score scales.
   - Out-of-distribution salience values (such as reflection importance $= 8.50$ vs episodic $\le 6.00$) cause catastrophic normalization distortion that suppresses the base memory store.
3. **Forward Constraint FC-RET-03: Reflection Admission & Scoring Isolation**:
   - Reflection nodes must not enter the primary episodic retrieval pipeline as unconstrained candidate competitors.
   - Reflection nodes must either:
     - (a) Compete in a segregated secondary index with independent thresholding;
     - (b) Have their importance scores calibrated to the identical distribution as episodic memories; or
     - (c) Serve strictly as query routing / expansion mechanisms rather than direct memory replacements.
4. **Forward Constraint FC-RET-04: Non-Inferiority Testing Protocol**:
   - In ablation designs where a simpler baseline (A4: Recency + Relevance) outperforms the full multi-factor configuration (A7), report the effect direction and magnitude explicitly. Do not conflate two-sided rejection of the null with formal one-sided non-inferiority without bounding the lower confidence interval against the preregistered margin.
