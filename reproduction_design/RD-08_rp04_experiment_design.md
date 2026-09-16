# RD-08: RP-04 Experiment Design Record
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## Experiment Specification Record: EXP-RP04-DYNAMIC-ORCHESTRATION

### 1. experiment_id
`EXP-RP04-DYNAMIC-ORCHESTRATION-V1`

### 2. reproduction_candidate
`RP-04`: Dynamic Agent Orchestration vs. Fixed Topology Escalation

### 3. research_question
Does dynamic selective agent activation (via heuristic or LLM-based meta-orchestration) outperform a fixed multi-agent topology (`B3`) in task completion quality per token spent across heterogeneous tasks, or does orchestrator overhead exceed the savings from selective activation?

### 4. falsifiable_hypothesis
Across a heterogeneous workload containing simple, moderate, and complex tasks, progressive routing escalation (`T-LLMRouter` and `T-Evolving`) will achieve $\ge 95\%$ of fixed-topology task accuracy while reducing total system token consumption by $\ge 25\%$ ($p < 0.01$) compared to fixed-topology `B3` on a 300-task benchmark (`SimLab-HeteroBench-300`), and will demonstrate superior Pareto efficiency over both `B0-Heuristic` and compute-matched single-agent `B1-SC` on a strictly held-out test split.

### 5. null_hypothesis
Dynamic routing meta-overhead (meta-prompts, routing inference calls, and misrouting recovery) equals or exceeds the token savings of skipped agent activations, or routing errors reduce overall task success rate by $\ge 8\%$ compared to the fixed topology baseline `B3`.

### 6. primitive_under_test
`PR-ORG-03`: Dynamic agent recruitment and routing orchestrator.

### 7. reference_mechanism
Evolving Orchestration as implemented in `OpenBMB/ChatDev:puppeteer` (commit `b24e6e6`).

### 8. baseline
- **Baseline B1-SC (Compute-Matched Single Agent Control)**: Single model sampled $K$ times with majority voting/best-of-N verifier, compute-matched to equal the average token expenditure of `B3`/`T-Dynamic`.
- **Baseline B3 (Fixed Full Topology)**: Every task unconditionally activates all 4 agents (Router, Analyst, Implementer, Verifier) in full sequence.
- **Baseline B0-Heuristic (Rule Router)**: Deterministic regex/keyword classifier routes tasks to (1) Single Agent, (2) Dual Agent, or (3) Full Team based on input length and predefined task keywords.

### 9. treatment
- **Treatment 1 (T-LLMRouter)**: Lightweight LLM classifier (`gpt-4o-mini`) predicts minimal required agent subgraph before dispatching execution.
- **Treatment 2 (T-Evolving)**: `ChatDev:puppeteer` dynamic routing mechanism where an orchestrator agent monitors intermediate artifacts and dynamically spawns or halts downstream agent roles.

### 10. independent_variables
Orchestration Strategy: (`B1_SC`, `B3_FIXED`, `B0_HEURISTIC`, `T1_LLM_ROUTER`, `T2_DYNAMIC_PUPPETEER`).

### 11. dependent_variables
1. **End-to-End Task Accuracy**: Task verification pass rate against deterministic tests.
2. **Total Token Spend**: Sum of meta-orchestrator tokens + worker agent tokens per task.
3. **Agent Activation Count**: Average number of distinct agents invoked per task.
4. **Under-Activation Rate**: Percentage of tasks that failed because a necessary specialist agent was omitted.
5. **Over-Activation Rate**: Percentage of simple tasks that activated unneeded agents.
6. **Orchestrator Overhead Fraction**: $\text{Tokens}_{orchestrator} / \text{Tokens}_{total}$.

### 12. controlled_variables
- Worker Agent models: `gpt-4o-2024-08-06` constant across all conditions.
- Worker Agent role system prompts constant across conditions.
- Evaluation task set identical across all conditions.
- Evaluation sandbox and test verification scripts identical.

### 13. model_configuration
- Worker Agents: `gpt-4o-2024-08-06`, $T=0.2$.
- LLM Router: `gpt-4o-mini-2024-07-18`, $T=0.0$, max tokens 150.

### 14. prompt_configuration
Router prompt: Few-shot classification prompt mapping task descriptions to agent subgraphs `['SOLO', 'PAIR', 'FULL_TEAM']`. Worker prompts frozen.

### 15. context_configuration
Router receives only the initial task prompt. Activated workers receive their specific task slice.

### 16. randomness_configuration
Fixed random seed `SEED=20260916`.

### 17. dataset_or_environment
`SimLab-HeteroBench-300`: A curated suite of $N=300$ tasks of varying complexity (expanded from 100 to ensure $>80\%$ power):
- 120 Simple Tasks (e.g., string manipulation, regex formatting, simple queries — solvable by 1 agent).
- 90 Moderate Tasks (e.g., algorithm implementation with test verification — requires 2 agents).
- 90 Complex Tasks (e.g., multi-file refactoring, constraint satisfaction — requires full 4-agent team).
- **Strict 70/30 Train/Test Split**: 210 tasks allocated for router prompt optimization and few-shot prompt tuning; 90 held-out tasks strictly reserved for blind evaluation to prevent router overfitting.

### 18. minimum_run_count
$N = 300$ tasks $\times$ 5 conditions = 1,500 experimental runs.

### 19. statistical_method
- **Cochran's Q Test**: Evaluates differences in binary task success proportions across all 5 matched conditions on the identical tasks.
- **Post-Hoc Pairwise McNemar's Tests**: With Bonferroni correction ($\alpha = 0.01 / 10 = 0.001$).
- **Repeated-Measures ANOVA / Friedman Test**: With post-hoc Tukey/Nemenyi tests on total token consumption.
- **Pareto Efficiency Frontier Analysis**: Accuracy vs. Token Spend across conditions.

### 20. success_threshold
- Net system token savings $\ge 25\%$ for `T-LLMRouter` vs `B3` ($p < 0.01$).
- Overall accuracy degradation $\le 3\%$ compared to `B3` on the held-out test split.
- Orchestrator token overhead $< 8\%$ of total spend.
- Non-inferior accuracy compared to compute-matched `B1-SC` with $\ge 15\%$ token savings.

### 21. failure_threshold
- Net token savings $< 5\%$, or Under-Activation Rate $> 10\%$ leading to task failures ($p < 0.01$).
- **Inconclusive Outcome Rule (`INCONCLUSIVE_SUB_THRESHOLD`)**: If net token savings falls between $5\%$ and $25\%$ without statistically significant accuracy degradation, or accuracy degradation is in $[3\%, 8\%)$, the result is flagged as `INCONCLUSIVE_SUB_THRESHOLD`. Pre-registered default: SimLab defaults to simpler baseline (`B0-Heuristic` or static `B1-SC` / `B3`), avoiding complex meta-orchestrators and dynamic routing machinery.

### 22. termination_condition
Completion of all 300 tasks across all 5 conditions.

### 23. token_budget
$1,500 \text{ runs} \times 2,500 \text{ avg tokens} \approx 3,750,000$ tokens (budget managed under the $100.00 ceiling).

### 24. latency_budget
Average latency per task $< 45$ seconds; total suite $< 6$ hours.

### 25. compute_budget
Local execution sandbox; $< 2$ GB RAM, standard CPU.

### 26. logging_requirements
Structured telemetry recording: `task_id`, `complexity_label`, `condition`, `router_decision`, `router_tokens`, `activated_agents`, `worker_tokens`, `total_tokens`, `task_success`, `failure_reason`, `latency_ms`.

### 27. provenance_requirements
Git commit hash of router harness, frozen benchmark task definitions, and SHA-256 logs.

### 28. known_confounds
Over-fitting router prompts to benchmark task phrasing.

### 29. expected_failure_modes
- Router misclassification: Categorizing complex tasks as simple, causing downstream worker failure.
- Cascading escalation: Failed simple routing triggering multi-round error recovery that consumes more tokens than full fixed topology.

### 30. what_result_supports
If positive: Demonstrates that progressive dynamic orchestration provides significant Pareto efficiency gains on heterogeneous workloads.

### 31. what_result_does_not_support
Does NOT prove that complex reinforcement-learned routing algorithms are required when a lightweight LLM router or heuristic succeeds.

### 32. external_validity_limits
Valid for discrete heterogeneous task batches. Does not evaluate real-time continuous dynamic recruitment in 25+ persistent agent simulations.

### 33. architecture_implication_if_positive
SimLab will implement a progressive two-tier router (heuristic filter $\to$ fast LLM classifier) in its agent dispatch system.

### 34. architecture_implication_if_negative
SimLab will standardize on static, predictable agent topologies, eliminating router complexity and meta-agent failure modes.

### 35. execution_authority
`NOT_GRANTED`
