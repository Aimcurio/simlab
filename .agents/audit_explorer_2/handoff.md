# Formal Handoff Report: EXP-AB-01-COMP Bounded Scientific Audit (R4 & R6)
**Agent**: `audit_explorer_2`  
**Working Directory**: `E:\projects\simlab\.agents\audit_explorer_2`  
**Date**: 2026-09-16  
**Parent Agent**: `ccb019c3-7ae2-4986-91b3-9649436f5fc8` (parent)  
**Report Artifact**: `E:\projects\simlab\.agents\audit_explorer_2\report.md`  

---

## 1. Observation

1. **Weight Configuration Integrity (AS-03 vs Code vs Telemetry)**:
   - File: `E:\projects\simlab\ablation_design\AS-03_memory_ablation_plan.md`, Section 2 lines 24–31.
   - Code: `E:\projects\simlab\run_exp_ab_01_comp.py`, lines 154–161.
   - Results: `E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_results.json`, `condition_summaries`.
   - Executed values:
     - A1: `[1.0, 0.0, 0.0]`, Expected: `[1.0, 0.0, 0.0]` (Match: `True`)
     - A2: `[0.0, 1.0, 0.0]`, Expected: `[0.0, 1.0, 0.0]` (Match: `True`)
     - A3: `[0.0, 0.0, 1.0]`, Expected: `[0.0, 0.0, 1.0]` (Match: `True`)
     - A4: `[0.3, 0.7, 0.0]`, Expected: `[0.3, 0.7, 0.0]` (Match: `True`)
     - A5: `[0.5, 0.0, 0.5]`, Expected: `[0.5, 0.0, 0.5]` (Match: `True`)
     - A6: `[0.0, 0.7, 0.3]`, Expected: `[0.0, 0.7, 0.3]` (Match: `True`)
     - A7: `[0.2, 0.5, 0.3]`, Expected: `[0.2, 0.5, 0.3]` (Match: `True`)
     - A8: `[0.2, 0.5, 0.3]`, Expected: `[0.2, 0.5, 0.3]` (Match: `True`)

2. **Cryptographic Hashes & Telemetry Verification**:
   - Dataset `SimLab_MemBench_500.json`: SHA-256 = `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800` (100 queries, 500 memories).
   - Telemetry `exp_ab_01_comp_telemetry.jsonl`: SHA-256 = `9eb6846b017f76883418e3703dd9f0111182e8dc8a0ea03bb5cd32dd27337eac` (800 events).
   - Results JSON: `exp_ab_01_comp_results.json`: SHA-256 = `a9a6b185347209774a3f25c7efc862bc7d00f6ee4f828a2524a2cb5e5ae1be67`.

3. **Performance Metrics across Conditions**:
   - A1 (`RECENCY_ONLY`): MRR $= 0.2756 \pm 0.3173$, NDCG@5 $= 0.3538$, Inversion $= 0.0\%$, FalseRet $= 88.0\%$.
   - A2 (`RELEVANCE_ONLY`): MRR $= 0.5130 \pm 0.4355$, NDCG@5 $= 0.5262$, Inversion $= 54.3\%$, FalseRet $= 60.0\%$.
   - A3 (`IMPORTANCE_ONLY`): MRR $= 0.0086 \pm 0.0072$, NDCG@5 $= 0.0000$, Inversion $= 50.0\%$, FalseRet $= 100.0\%$.
   - A4 (`RECENCY_RELEVANCE`): MRR $= 0.5002 \pm 0.4481$, NDCG@5 $= 0.5170$, Inversion $= 24.1\%$, FalseRet $= 58.0\%$. Target median rank $= 2.5$.
   - A5 (`RECENCY_IMPORTANCE`): MRR $= 0.0205 \pm 0.0183$, NDCG@5 $= 0.0000$, Inversion $= 30.0\%$, FalseRet $= 100.0\%$.
   - A6 (`RELEVANCE_IMPORTANCE`): MRR $= 0.1695 \pm 0.2848$, NDCG@5 $= 0.1691$, Inversion $= 42.6\%$, FalseRet $= 92.0\%$.
   - A7 (`FULL_TRI_FACTOR`): MRR $= 0.0941 \pm 0.0738$, NDCG@5 $= 0.0450$, Inversion $= 46.4\%$, FalseRet $= 100.0\%$. Target median rank $= 13.0$, target min rank $= 3.0$.
   - A8 (`TRI_FACTOR_REFLECTION`): MRR $= 0.0325 \pm 0.0101$, NDCG@5 $= 0.0000$, Inversion $= 0.0\%$, FalseRet $= 100.0\%$. 100% Rank-1 reflection crowding, 500/500 top-5 slots occupied by reflections. Target median rank $= 32.0$.

4. **Component Distributions and Correlation with Ground-Truth Target Label** ($N = 50,000$ query-memory pairs):
   - Cosine relevance correlation with binary target label: Pearson $r = +0.0932$ ($p = 7.60 \times 10^{-97}$), Spearman $\rho = +0.0740$.
   - Recency decay correlation with binary target label: Pearson $r = +0.0482$ ($p = 4.15 \times 10^{-27}$), Spearman $\rho = +0.0464$.
   - Importance score correlation with binary target label: Pearson $r = \mathbf{+0.0182}$ ($p = 4.54 \times 10^{-5}$), Spearman $\rho = \mathbf{+0.0185}$, $R^2 = \mathbf{0.00033}$.
   - Target memory importance: mean $= 5.2364 \pm 0.4583$, range $[4.28, 5.83]$.
   - Distractor memory importance: mean $= 5.0024 \pm 0.5734$, range $[4.01, 6.00]$.
   - Distractors with higher importance than target: mean $= 188.4$ memories per query ($37.8\%$ of pool).
   - Recency-sensitive queries: target importance mean $= 5.0500$; distractors higher $= 234.6$ ($47.0\%$).
   - Temporal-conflict queries: target importance mean $= 5.0500$; distractors higher $= 234.6$ ($47.0\%$).

5. **Near-Target Decomposition in Condition A7**:
   - Target score mean $= 0.8375 \pm 0.0605$ (Sim contrib: $0.4957$, Rec contrib: $0.1568$, Imp contrib: $0.1849$).
   - Rank-1 distractor score mean $= 0.9359 \pm 0.0192$ (Sim contrib: $0.4811$, Rec contrib: $0.1670$, Imp contrib: $0.2878$).
   - $\Delta \text{Sim} = +0.0147$ (Target leads).
   - $\Delta \text{Rec} = -0.0102$ (Distractor leads).
   - $\Delta \text{Imp} = \mathbf{-0.1029}$ (Distractor leads by 7.0x the target's semantic lead).
   - Net score margin: $\Delta \text{Total} = -0.0985$. Target max score margin across all 100 queries is $-0.0255$.

6. **Continuous Simplex Sweep Monotonicity**:
   - $\gamma = 0.0$: Mean MRR $= 0.5232$ (Peak at $\alpha=0.7, \beta=0.3, \gamma=0.0 \to \text{MRR} = 0.6036$).
   - $\gamma = 0.1$: Mean MRR $= 0.3718$.
   - $\gamma = 0.2$: Mean MRR $= 0.2601$.
   - $\gamma = 0.3$: Mean MRR $= 0.1547$.
   - $\gamma = 0.5$: Mean MRR $= 0.0547$.
   - $\gamma = 1.0$: Mean MRR $= 0.0086$.

7. **Reflection Incommensurability in A8**:
   - Episodic importance range: $[4.01, 6.00]$.
   - Reflection node importance: $8.50$.
   - Min-max normalized importance: Episodic max $= (6.0 - 4.01)/(8.5 - 4.01) = 0.4432$. Reflection $= 1.0000$.
   - Guaranteed structural importance advantage for reflections at $\gamma=0.3$: $+0.1670$.

---

## 2. Logic Chain

1. **Step 1 (Configuration Audit)**: Comparing the executed parameters against `AS-03` confirms that every condition executed the exact preregistered weights and pool configurations. Dataset and telemetry SHA-256 hashes are verified bit-for-bit. Therefore, `EXPERIMENT_CONFIGURATION_DRIFT` did not occur.
2. **Step 2 (Falsification of Operational Defect Hypotheses)**:
   - Scale inversion is disproven because raw and normalized correlations are $+0.999$ to $+1.000$, and sorting is strictly descending.
   - Code weight application error is disproven by direct inspection of lines 92–95 in `run_exp_ab_01_comp.py`.
   - Duplicate crowding is disproven because all 500 episodic memories have unique IDs and cosine similarities $< 0.9809$.
   - Label leakage is disproven because target ID is accessed only after sorting to look up the rank.
   - Tie-breaking artifacts are disproven because in continuous conditions (A2, A4, A7), exactly 0 / 100 queries experienced score ties.
3. **Step 3 (Identification of the A7 Failure Mechanism)**:
   - In offline retrieval, static importance has near-zero correlation with ground-truth relevance ($r = +0.0182$, $R^2 = 0.00033$).
   - In a 500-memory pool, 37.8% of distractors have higher static importance than the target memory.
   - In the local semantic cluster of candidate memories ($\cos > 0.90$), the target's semantic lead over the best distractor is modest ($+0.0147$ at $\beta=0.5$).
   - When $\gamma=0.3$ is assigned to importance, a distractor with high importance ($5.8 - 6.0$) gains a $+0.1029$ score bonus over the target.
   - Because $0.1029 > 0.0147$, this orthogonal noise completely overpowers the semantic signal, pushing the target out of Rank 1 in 100% of queries.
4. **Step 4 (Validation of A4 Superiority)**:
   - In Condition A4, setting $\gamma=0.0$ removes the orthogonal noise term entirely.
   - Increasing $\beta$ from $0.5$ to $0.7$ strengthens semantic discrimination.
   - Combined with recency ($\alpha=0.3$), A4 achieves MRR $0.5002$, demonstrating that importance is an actively harmful parameter in this retrieval regime.
5. **Step 5 (Identification of the A8 Reflection Failure)**:
   - Assigning reflection nodes an out-of-distribution importance score ($8.50$ vs episodic $\le 6.00$) combined with per-query global min-max normalization artificially suppresses all episodic memories to normalized importance $\le 0.4432$.
   - Reflection nodes gain a guaranteed $+0.1670$ score bonus, capturing 100% of top ranks and causing complete episodic memory starvation.

---

## 3. Caveats

1. **Benchmark Scope**: Findings are established on `SimLab-MemBench-500` (500 episodic memories, 100 queries, 3 query types, $\lambda=0.995$, $t_{curr}=72.0$). They reflect static offline dense vector retrieval. They do not evaluate dynamic real-time social simulations where importance scores may be updated interactively or conditioned on specific agent goals.
2. **Heuristic Generation**: The prompt-based importance scores in `SimLab-MemBench-500` are bounded in $[4.01, 6.00]$ and were generated offline. Whether importance scores generated by a live frontier model (e.g. GPT-4o / Claude 3.5 Sonnet) would exhibit higher correlation with downstream relevance remains an open question for future benchmarks.
3. **Alternative Normalization**: While min-max normalization was audited, alternative normalization schemes (such as z-score normalization, rank-based reciprocal rank fusion, or independent index retrieval) were not tested in the Phase 4 execution run.

---

## 4. Conclusion

1. **R6 Verdict**: `NO_EXPERIMENT_CONFIGURATION_DRIFT`. The experiment executed the preregistered AS-03 design with 100% fidelity. All cryptographic hashes match.
2. **R4 Mechanistic Verdict**: The collapse of A7 (MRR $0.0941$) relative to A4 (MRR $0.5002$) is an authentic mathematical failure caused by **Scale Incommensurability and Orthogonal Noise Amplification** in the presence of low ground-truth importance correlation ($r = +0.0182$).
3. **R4 Reflection Verdict**: The collapse of A8 (MRR $0.0325$, 100% crowding) is a **SCORING_SCALE_ARTIFACT and IMPLEMENTATION_DEFECT** resulting from global min-max normalization over an out-of-distribution salience score ($8.50$ vs $4.01-6.00$).
4. **Deliverables Ready**: Draft Section D (Score-Distribution Audit) and Draft Section F (Configuration Integrity Check) are fully drafted and incorporated into `E:\projects\simlab\.agents\audit_explorer_2\report.md`.

---

## 5. Verification Method

To independently verify all findings, run the following commands in PowerShell from `E:\projects\simlab`:

1. **Verify Hashes and Weight Configuration Match (R6)**:
   ```powershell
   python .agents/audit_explorer_2/audit_r6_weights.py
   ```
   *Expected Output*: `Overall Weight Configuration Match: True`, `Drift Determination: NO_EXPERIMENT_CONFIGURATION_DRIFT`, all hashes match.

2. **Verify Component Distributions and A1–A8 Quantile Tables (R4)**:
   ```powershell
   python .agents/audit_explorer_2/comprehensive_r4_r6_audit.py
   python .agents/audit_explorer_2/format_tables.py
   ```
   *Expected Output*: Exact quantiles matching Tables D-1, D-2, D-3, and D-4 in `report.md`.

3. **Verify Correlation and A7 Near-Target Distractor Decomposition (R4)**:
   ```powershell
   python .agents/audit_explorer_2/audit_a7_anatomy.py
   ```
   *Expected Output*: Pearson $r = +0.018236$, Target Sim lead $= +0.0147$, Distractor Imp lead $= +0.1029$, Net Delta $= -0.0985$.

4. **Verify 8 Failure Mode Falsification Diagnoses**:
   ```powershell
   python .agents/audit_explorer_2/audit_failure_modes.py
   ```
   *Expected Output*: Falsification of scale inversion, label leakage, weight errors, duplicate crowding; confirmation of local scale dominance, normalization distortion, reflection dominance, and benchmark bias.

5. **Verify Simplex Sweep Gradients**:
   ```powershell
   python .agents/audit_explorer_2/simplex_gradients.py
   ```
   *Expected Output*: Monotonic MRR collapse across $\gamma \in [0.0, 1.0]$.
