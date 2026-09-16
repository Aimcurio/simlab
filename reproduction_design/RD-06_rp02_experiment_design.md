# RD-06: RP-02 Experiment Design Record
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## Experiment Specification Record: EXP-RP02-COMPUTE-MATCHED

### 1. experiment_id
`EXP-RP02-COMPUTE-MATCHED-V1`

### 2. reproduction_candidate
`RP-02`: Compute-Matched Single-Agent Self-Consistency vs. Multi-Agent Debate

### 3. research_question
When total inference compute (FLOPs, model parameter scale, and token count) is strictly controlled, under what task characteristics does a multi-agent debate architecture (`B3`) outperform single-agent Self-Consistency (`B1-SC`), and where does it produce zero gain or degradation?

### 4. falsifiable_hypothesis
On tasks with private/partitioned information or asymmetric tool specializations, a 3-agent 2-round debate architecture (`T-Debate`) will outperform compute-matched single-agent Dual-Control baselines ($B_{1-SC-calls}$ and $B_{1-SC-tokens}$) by $\ge +10\%$ task accuracy ($p < 0.01$). Conversely, on closed-domain symbolic reasoning (GSM8K, $N=500$), compute-matched $B_{1-SC-tokens}$ will equal multi-agent debate accuracy within an equivalence margin of $\pm 3\%$ ($\delta = 0.03$), verified via Two One-Sided Tests (TOST) with statistical power $\ge 80\%$ ($p_{TOST} < 0.05$).

### 5. null_hypothesis
Compute-matched single-agent Dual Controls ($B_{1-SC-calls}$ and $B_{1-SC-tokens}$) equal or outperform multi-agent debate across all task categories ($p \ge 0.05$), or debate provides no statistically significant advantage ($\Delta < 2\%$, $p \ge 0.05$) on private-information tasks.

### 6. primitive_under_test
`PR-ORG-01`: Multi-agent iterative debate and cross-examination.

### 7. reference_mechanism
Multi-Agent Debate as implemented in AgentVerse (`OpenBMB/AgentVerse`) and Liang et al. (2023) / Du et al. (2023).

### 8. baseline
- **Baseline B1**: Single-agent greedy Chain-of-Thought ($T=0$).
- **Baseline B1-SC-calls (Inference-Call-Matched Control)**: Single-agent Self-Consistency with $K=7$ independent reasoning samples ($T=0.7$). The odd sample size ($K=7$) strictly eliminates 50/50 majority ties in binary tasks.
- **Baseline B1-SC-tokens (Token-Budget-Matched Control)**: Single-agent Self-Consistency with $K=10$ independent reasoning samples ($T=0.7$), matching the $+50\%$ token overhead of multi-round conversational history accumulation in debate within $\pm 5\%$.
- **Deterministic Tie-Breaking Protocol**: Plurality voting across samples. If tied (in $K=10$ or multi-class splits), select the candidate answer with the highest mean sequence log-probability across generating calls. Fallback: select earliest deterministic sample index.

### 9. treatment
**Treatment (T-Debate)**: 3-agent, 2-round structured debate ($3 \times 2 = 6$ total inference calls per instance) where agents critique each other's reasoning and converge on a final synthesized answer.

### 10. independent_variables
1. Architecture condition: (`B1`, `B1-SC-calls` [$K=7$], `B1-SC-tokens` [$K=10$], `T-Debate`).
2. Task Category: (1. Closed Symbolic Reasoning: GSM8K [$N=500$]; 2. Private Information Reconciliation: MysteryDeduction [$N=100$]; 3. Asymmetric Tool Execution: ToolPipelineBench [$N=100$]; 4. Distributed State Tracking: StateTrack25 [$N=100$]).

### 11. dependent_variables
1. **Task Accuracy**: Exact-match or verifiable ground-truth correctness percentage.
2. **Total Input Tokens**: Sum of all prompt and context tokens consumed per task.
3. **Total Output Tokens**: Sum of all generated reasoning and answer tokens per task.
4. **Wall-Clock Latency**: End-to-end task completion time in seconds.
5. **False Consensus Rate**: Frequency where multi-agent debate converges on an initially incorrect solution.

### 12. controlled_variables
- Foundation Model: `gpt-4o-2024-08-06` (or `gemini-1.5-pro-002`) held constant across all conditions.
- System prompt instructions for task definitions held constant.
- Dual-Control compute normalization: `B1-SC-calls` ($K=7$ calls) matches inference call budget; `B1-SC-tokens` ($K=10$ calls) matches total token budget within $\pm 5\%$.
- Deterministic tie-breaking protocol enforced across all $B_{1-SC}$ conditions.

### 13. model_configuration
- Model Checkpoint: `gpt-4o-2024-08-06`.
- Temperature: $T=0.0$ for `B1`; $T=0.7$ for `B1-SC-calls`, `B1-SC-tokens`, and `T-Debate`.
- Max Generation Tokens: 1024 tokens per inference call.

### 14. prompt_configuration
Standardized system role prompts for Debate Agent A (Proposer), Agent B (Critic), and Agent C (Synthesizer). Single-agent `B1-SC` uses standard Chain-of-Thought system prompt. Prompts frozen with SHA-256 hashes.

### 15. context_configuration
Debate rounds append previous agent critiques to conversation history. B1-SC instances run in isolated parallel contexts with zero cross-talk.

### 16. randomness_configuration
Fixed random seeds for dataset sampling and model inference: `SEEDS = [101, 202, 303, 404, 505]`.

### 17. dataset_or_environment
800 balanced problem instances across 4 task suites ($800$ total task problems):
- 500 problems from GSM8K (Closed Symbolic Reasoning; sample size expanded to $N=500$ to ensure $>80\%$ power under TOST with equivalence margin $\delta = 0.03$).
- 100 problems from `MysteryDeduction` (Private Information: 3 agents receive disjoint sets of evidence).
- 100 problems from `ToolPipelineBench` (Asymmetric Tools: Agent 1 has SQL, Agent 2 has Python, Agent 3 has Web API).
- 100 problems from `StateTrack25` (Distributed state tracking across 10 locations).

### 18. minimum_run_count
$N = 800$ problem instances $\times$ 4 conditions = $3,200$ evaluation episodes ($24,800$ total inference calls across conditions).

### 19. statistical_method
- **Binomial Generalized Linear Mixed Model (GLMM with logit link function)**: Replaces linear Two-Way ANOVA for repeated binary accuracy outcomes ($Y_{ij} \in \{0, 1\}$). Problem instance modeled as random intercept; Architecture Condition, Task Category, and Condition $\times$ Category interaction modeled as fixed effects.
- **Two One-Sided Tests (TOST)**: On the $N=500$ GSM8K subset, evaluates statistical equivalence within margin $\delta = 0.03$ ($H_{01}: \Delta \le -0.03$, $H_{02}: \Delta \ge +0.03$). With $N=500$ and empirical discordance $p_{disc} \le 0.07$ on GSM8K (typical when frontier models achieve $\approx 85\text{--}90\%$ accuracy), standard error is $SE = \sqrt{0.07 / 500} = 0.0118$, yielding $90\%$ CI half-width of $\pm 0.0194 < 0.03$ and achieving $> 81\%$ statistical power under TOST with margin $\delta = 0.03$. Even if discordance reaches $p_{disc} = 0.15$, $SE = 0.0173$ and the $90\%$ CI half-width $\pm 0.0285$ fits within $[-0.03, +0.03]$, achieving $> 88\%$ power for margin $\delta = 0.05$.
- **Pairwise McNemar Tests**: With Bonferroni correction for pairwise comparisons between conditions within each task category.
- **Bootstrap 95% Confidence Intervals**: 10,000 resamples on accuracy deltas.

### 20. success_threshold
- `T-Debate` accuracy exceeds both `B1-SC-calls` and `B1-SC-tokens` by $\ge +10\%$ on Private Information and Asymmetric Tool tasks ($p < 0.01$).
- Equivalence confirmed on GSM8K under TOST: $90\%$ confidence interval for accuracy difference between `T-Debate` and `B1-SC-tokens` lies entirely within $[-0.03, +0.03]$ ($p_{TOST} < 0.05$).

### 21. failure_threshold
- `B1-SC-tokens` achieves equal or higher accuracy than `T-Debate` across all 4 task categories ($p \ge 0.05$).
- `T-Debate` exhibits $> 20\%$ False Consensus Rate where agents abandon correct initial answers to adopt incorrect peer answers.
- **Inconclusive Outcome Rule (`INCONCLUSIVE_SUB_THRESHOLD`)**: If `T-Debate` achieves $+2\% \le \Delta < +10\%$ advantage on Private Information/Tools, or the GSM8K $90\%$ CI crosses the $\pm 3\%$ margin, the result is flagged as `INCONCLUSIVE_SUB_THRESHOLD`. Pre-registered default: SimLab defaults to simpler baseline (`B1` or `B1-SC-calls`), rejecting debate due to lack of demonstrated superiority under compute matching.

### 22. termination_condition
All 800 benchmark instances evaluated across all conditions, or API budget cap reached.

### 23. token_budget
Total estimated tokens: $24,800 \text{ calls} \times 1,200 \text{ avg tokens} = 29,760,000$ tokens (budget managed via staged batches under the $100.00 ceiling).

### 24. latency_budget
Sequential latency per debate problem $\le 25$ seconds; total benchmark execution time $< 10$ hours with rate limiting.

### 25. compute_budget
API-based inference; local orchestration requires single process, $< 1$ GB RAM.

### 26. logging_requirements
Full JSONL transcript per problem instance: `problem_id`, `task_category`, `condition`, `call_index`, `agent_role`, `input_prompt`, `output_response`, `token_counts`, `latency_ms`, `final_answer`, `ground_truth`, `is_correct`, `consensus_trajectory`, `vote_distribution`, `tie_broken`, `tie_breaking_method`.

### 27. provenance_requirements
Git commit hash of benchmark harness, frozen dataset JSONs, and SHA-256 hashes of all raw response logs.

### 28. known_confounds
1. **Model Capability Confound**: Stronger frontier models (e.g. o1/o3) may internalize multi-perspective reasoning, eliminating debate advantages that appear in smaller models.
2. **Prompt Optimization Confound**: Debate prompts may receive more engineering attention than single-agent prompts.

### 29. expected_failure_modes
- Sycophancy / False Consensus: Agents deferring to confident but incorrect peers.
- Verbosity explosion: Multi-agent debate generating verbose conversational filler that inflates token counts without adding information.

### 30. what_result_supports
If positive: Establishes a rigorous, empirical task boundary for multi-agent architectures, proving where multi-agent debate is economically and scientifically justified under strict compute parity.

### 31. what_result_does_not_support
Does NOT prove that multi-agent debate is superior for open-ended creative writing, real-time gaming, or physical robot control.

### 32. external_validity_limits
Limited to 3-agent debate topologies and text-based problem solving. Does not evaluate debate scaling to $N \ge 25$ agents.

### 33. architecture_implication_if_positive
SimLab will implement a dynamic collaboration router: closed-reasoning tasks route to single-agent Self-Consistency; private-information and asymmetric-tool tasks route to structured multi-agent debate teams.

### 34. architecture_implication_if_negative
SimLab will abandon multi-agent debate as a reasoning mechanism, standardizing on single-agent parallel sampling and tool-use pipelines, dramatically reducing system complexity.

### 35. execution_authority
`NOT_GRANTED`
