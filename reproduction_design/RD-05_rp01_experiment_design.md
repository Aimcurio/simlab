# RD-05: RP-01 Experiment Design Record
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## Experiment Specification Record: EXP-RP01-RECENCY

### 1. experiment_id
`EXP-RP01-RECENCY-V1`

### 2. reproduction_candidate
`RP-01`: Smallville Memory Recency / Retrieval Scoring Function

### 3. research_question
Does mathematically corrected exponential temporal recency decay improve retrieval precision and temporal ranking correlation on a memory benchmark compared to: (1) the historical rank-index inverted implementation in Smallville (`retrieve.py:145-146`), (2) a no-recency baseline ($\alpha=0, \beta=1, \gamma=1$), and (3) linear recency decay?

### 4. falsifiable_hypothesis
Corrected exponential temporal recency decay evaluated in elapsed simulation hours ($s_{rec} = 0.995^{\Delta t_{hours}}$, half-life $t_{1/2} = \ln(0.5)/\ln(0.995) \approx 138.28\text{ hours}$) using calibrated weights ($\alpha=0.5, \beta=3.0, \gamma=2.0$) will produce a statistically significant increase in Mean Reciprocal Rank (MRR $\ge +0.15$) and Normalized Discounted Cumulative Gain (NDCG@5 $\ge +0.18$) compared to both the historical inverted implementation (`B0-Historical`) and no-recency baseline (`B0-NoRecency`) ($p < 0.0025$, Paired Wilcoxon signed-rank test) across a standardized suite of 100 memory retrieval queries.

### 5. null_hypothesis
Corrected exponential recency decay yields no statistically significant difference or worse retrieval rank quality (MRR $\Delta < +0.05$, $p \ge 0.01$) compared to the no-recency baseline or historical inverted implementation.

### 6. primitive_under_test
`PR-COG-01`: Tri-factor memory retrieval scoring ($s = \alpha \cdot s_{rec} + \beta \cdot s_{rel} + \gamma \cdot s_{imp}$).

### 7. reference_mechanism
Stanford Generative Agents (`joonspk-research/generative_agents`, commit `e295484`), specifically `reverie/backend_server/persona/cognitive_modules/retrieve.py:145-146` and lines `244-250`.

### 8. baseline
- **Primary Baseline (B0-Historical)**: Smallville historical implementation where candidate memories are ordered chronologically and assigned normalized recency scores $s_{rec} = \text{rank} / N$, causing older memories to receive higher recency scores.
- **Secondary Baseline (B0-NoRecency)**: Pure relevance and importance retrieval ($s = 0.6 \cdot s_{rel} + 0.4 \cdot s_{imp}$, zero recency weighting).

### 9. treatment
- **Primary Treatment (T-Corrected-Calibrated)**: Mathematically sound temporal decay scoring where $\Delta t = t_{current} - t_{created}$ in elapsed simulation hours ($s_{rec} = 0.995^{\Delta t_{hours}}$), translated to 10-second simulation ticks via $\Delta t_{hours} = \Delta t_{ticks} / 360$ (or per-tick decay factor $\gamma_{tick} = 0.995^{1/360} \approx 0.9999861$). Evaluated using Smallville's calibrated code weights ($\alpha=0.5, \beta=3.0, \gamma=2.0$) where semantic relevance strictly dominates recency.
- **Ablation Condition (T-Corrected-Equal)**: Evaluates the published equal weights ($\alpha=1.0, \beta=1.0, \gamma=1.0$) to quantify the retrieval degradation on non-temporal queries when recency is allowed to overpower semantic relevance.

### 10. independent_variables
Recency scoring algorithm formulation (Levels: `B0_HISTORICAL_INVERTED`, `B0_NO_RECENCY`, `T_CORRECTED_CALIBRATED`, `T_CORRECTED_EQUAL`, `T_LINEAR_DECAY`).

### 11. dependent_variables
1. **MRR (Mean Reciprocal Rank)**: Position of the ground-truth target memory in the ranked retrieval list.
2. **NDCG@5**: Normalized Discounted Cumulative Gain for the top 5 retrieved records against graded temporal relevance annotations.
3. **Temporal Inversion Rate**: Percentage of retrieved pairs where an older, equally relevant memory is ranked above a strictly newer memory.
4. **Retrieval Latency**: Execution time per retrieval query in milliseconds.

### 12. controlled_variables
- Memory database content (fixed 500-record synthetic episodic memory dataset covering a 72-hour simulated timeline).
- Embedding model for cosine similarity calculation (fixed: `text-embedding-3-small`).
- Query strings and target ground-truth relevance rankings (frozen JSON benchmark).
- Importance scores (pre-calculated and frozen across all conditions).
- Hardware execution environment (single isolated CPU thread, zero network calls during scoring).
- Normalization safeguard: $\epsilon = 10^{-6}$ added to min-max denominator to prevent division-by-zero on identical timestamps.

### 13. model_configuration
Deterministic retrieval scoring harness: Zero LLM inference calls during retrieval. Memory embeddings pre-computed with `text-embedding-3-small` (dimension: 1536), zero temperature, deterministic vector cosine distance.

### 14. prompt_configuration
Not applicable for vector retrieval scoring. Ground-truth relevance and importance labels generated via pre-registered few-shot prompt with `gpt-4o-2024-08-06` at temperature $T=0.0$ and human-verified prior to experiment run.

### 15. context_configuration
Fixed memory store of 500 discrete episodic records covering a 72-hour simulated timeline. Retrieval candidate window set to $K=30$, final returned set $M=5$.

### 16. randomness_configuration
Deterministic execution: Fixed seed `SEED=20260916`. Embedding distances and mathematical decay functions are 100% deterministic.

### 17. dataset_or_environment
`SimLab-MemBench-500`: A curated, isolated memory dataset containing 500 timestamped episodic events across 5 simulated days, accompanied by 100 standardized queries categorized into:
- 40 Recency-Sensitive Queries (e.g., "What was the most recent update on the project?").
- 40 Relevance-Dominant Queries (e.g., "What is the agent's core background in chemistry?").
- 20 Temporal-Relevance Conflict Queries (where an older event has high semantic match, but a newer event explicitly supersedes it).

### 18. minimum_run_count
$N = 100$ discrete queries per condition across 5 conditions ($500$ total evaluation runs).

### 19. statistical_method
- Paired Wilcoxon signed-rank test comparing MRR and NDCG@5 between `T-Corrected-Calibrated` and `B0-Historical`, as well as against `B0-NoRecency`.
- Bonferroni correction for multi-baseline comparisons ($\alpha = 0.01 / 4 = 0.0025$).
- Cohen's $d$ and Cliff's Delta effect size calculation.

### 20. success_threshold
- Statistically significant increase in MRR ($\Delta \text{MRR} \ge +0.15, p < 0.0025$) for `T-Corrected-Calibrated` over both `B0-Historical` and `B0-NoRecency`.
- NDCG@5 $\ge 0.82$ on recency-sensitive queries.
- Temporal Inversion Rate drops from $> 45\%$ (historical) to $< 5\%$ (treatment).

### 21. failure_threshold
- MRR improvement of `T-Corrected-Calibrated` over `B0-NoRecency` is $< +0.05$ ($p \ge 0.05$).
- NDCG@5 on conflict queries shows no significant improvement over random ranking.
- **Inconclusive Outcome Rule (`INCONCLUSIVE_SUB_THRESHOLD`)**: If MRR improvement falls in the sub-threshold zone $[+0.05, +0.15)$, the outcome is flagged as `INCONCLUSIVE_SUB_THRESHOLD`. Pre-registered default: SimLab defaults to the simpler baseline (`B0-NoRecency` supplemented by a lightweight FIFO recency buffer), rejecting continuous exponential mathematical decay as unnecessary cognitive overhead.

### 22. termination_condition
Completion of all 100 query evaluations across all 5 conditions, or unhandled NaN/overflow in decay normalization.

### 23. token_budget
Zero runtime LLM tokens (deterministic harness). Total pre-computation budget for embeddings and ground-truth verification: $< 150,000$ tokens ($\approx \$0.10$).

### 24. latency_budget
Total execution time for full 500-query benchmark harness $< 60$ seconds on standard CPU.

### 25. compute_budget
Single local process, $< 500$ MB RAM, zero GPU compute required.

### 26. logging_requirements
Structured JSONL telemetry recording: `query_id`, `condition`, `retrieved_memory_ids`, `retrieved_scores_breakdown` ($s_{rec}, s_{rel}, s_{imp}$), `computed_mrr`, `computed_ndcg`, `execution_time_ms`.

### 27. provenance_requirements
All code, datasets, embeddings, and query definitions version-controlled in Git; SHA-256 digests recorded for dataset files and scoring scripts.

### 28. known_confounds
1. Embedding semantic similarity variance dominating recency differences if weight ratios ($\alpha, \beta, \gamma$) are uncalibrated.
2. Query formulation bias favoring recency over semantic relevance.

### 29. expected_failure_modes
- Score scale compression: If candidate scores are clustered in $[0.95, 1.0]$, normalization may amplify micro-noise.
- Recency overpowering relevance on complex queries, causing agents to retrieve irrelevant recent trivia.

### 30. what_result_supports
If positive: Demonstrates that corrected exponential recency decay provides statistically superior temporal memory retrieval in isolation and confirms the Smallville code defect compromised its published retrieval claims.

### 31. what_result_does_not_support
Does NOT prove that agents will plan better, form higher-quality social relationships, or avoid long-horizon hallucinations in a complete 25+ agent simulation.

### 32. external_validity_limits
Results valid for episodic text memory retrieval up to 1,000 records. Does not generalize to million-record vector databases with hierarchical HNSW indexing.

### 33. architecture_implication_if_positive
SimLab memory substrate will implement parameterized exponential temporal decay ($s = e^{-\lambda \Delta t}$) with dynamic query-type weight modulation ($\alpha_{query}, \beta_{query}, \gamma_{query}$), discarding Smallville's rank-index scoring.

### 34. architecture_implication_if_negative
SimLab will eliminate the continuous recency scoring component entirely, relying on pure semantic relevance plus discrete recency filters (e.g., top-K recent buffer), saving mathematical scoring overhead.

### 35. execution_authority
`NOT_GRANTED`
