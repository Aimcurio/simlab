# AS-03: Memory Component Ablation Plan
**Experiment ID**: `EXP-AB-01-COMP`  
**Target Primitive**: `PR-COG-01` (Tri-Factor Memory Retrieval Scoring)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
Which specific mathematical components and weighting strategies of the tri-factor memory retrieval scoring function ($s = \alpha s_{rec} + \beta s_{rel} + \gamma s_{imp}$) are causally responsible for high retrieval precision, and does adding synthesized reflection nodes improve or contaminate retrieval?

---

## 2. Experimental Design (8 Controlled Conditions)

All conditions run against the standardized `SimLab-MemBench-500` benchmark ($N=100$ recency-sensitive, relevance-dominant, and conflict queries). All embeddings are pre-computed using pinned text embedding vectors. Zero runtime LLM inference calls are required.

| Condition Code | Condition Name | Scoring Formulation | Theoretical Purpose | Success / Falsification Criteria |
|:---|:---|:---|:---|:---|
| **A1** | `RECENCY_ONLY` | $s = s_{rec} = \lambda^{\Delta t}$ | Isolate temporal decay without semantic grounding. | Falsify whether pure recency produces coherent retrieval. |
| **A2** | `RELEVANCE_ONLY` | $s = s_{rel} = \cos(\mathbf{q}, \mathbf{m})$ | Traditional dense vector similarity baseline. | Benchmark baseline for pure semantic search. |
| **A3** | `IMPORTANCE_ONLY`| $s = s_{imp} = \text{score}_{\text{prompt}}$ | Static salience retrieval. | Falsify whether high-importance memories alone suffice. |
| **A4** | `RECENCY_RELEVANCE`| $s = 0.3 s_{rec} + 0.7 s_{rel}$ | Test temporal decay combined strictly with semantics. | Measure whether importance is an unnecessary parameter. |
| **A5** | `RECENCY_IMPORTANCE`| $s = 0.5 s_{rec} + 0.5 s_{imp}$ | Non-semantic heuristic retrieval. | Falsify non-vector retrieval mechanisms. |
| **A6** | `RELEVANCE_IMPORTANCE`| $s = 0.7 s_{rel} + 0.3 s_{imp}$ | Standard RAG with static priority weighting. | Test whether temporal decay is strictly necessary. |
| **A7** | `FULL_TRI_FACTOR` | $s = 0.2 s_{rec} + 0.5 s_{rel} + 0.3 s_{imp}$ | Reconciled Phase 3 tuned weighting configuration. | Benchmark for full tri-factor interaction. |
| **A8** | `TRI_FACTOR_REFLECTION`| A7 scoring over memory store including $20\%$ synthesized reflection nodes | Evaluate reflection impact on retrieval. | Test whether reflection nodes boost NDCG or crowd out ground-truth episodic memories. |

---

## 3. Weighting Simplex Sweep
In addition to discrete conditions A1–A8, a continuous 2D simplex grid search over normalized weights $\alpha + \beta + \gamma = 1.0$ (step size $\Delta = 0.1$, 66 grid points) will be evaluated across all queries to map the exact mathematical boundary where $\beta$ ceases to dominate and retrieval degrades.

---

## 4. Primary Metrics & Hypotheses
- **Primary Metric**: Mean Reciprocal Rank (MRR) and NDCG@5.
- **Hypothesis ($H_1$)**: Condition A4 (`RECENCY_RELEVANCE`) achieves non-inferior MRR compared to A7 (`FULL_TRI_FACTOR`) within $\Delta \le 0.02$, proving that static importance scores add negligible marginal value over semantics and recency.
- **Null Hypothesis ($H_0$)**: Importance weighting is strictly necessary ($\text{MRR}_{A7} - \text{MRR}_{A4} \ge +0.05, p < 0.0025$).
- **Statistical Test**: Paired Wilcoxon signed-rank test with Bonferroni correction ($\alpha = 0.01 / 7 = 0.0014$).

---

## 5. Causal Claim Discipline
- `causal_claim_supported`: "Removing prompt-based importance scores from tri-factor memory retrieval produces no statistically significant degradation in MRR ($\Delta \text{MRR} \le 0.02$) under offline semantic retrieval across the tested queries."
- `causal_claim_not_supported`: "Prompt-based importance scoring is universally useless across all cognitive agent simulation architectures."
- `tested_context`: Standardized 500-node episodic memory store, cosine similarity dense embeddings, exponential tick decay ($\lambda = 0.995$).
- `untested_context`: Dynamic multi-agent social games with real-time goal revisions, stores $> 10,000$ memories, graph-structured knowledge stores.
- `interaction_risks`: When importance weighting is eliminated, synthesized reflection nodes may lose tie-breaking salience against dense episodic distractors.

