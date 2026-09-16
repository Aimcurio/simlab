# RD-07: RP-03 Experiment Design Record
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## Experiment Specification Record: EXP-RP03-PHASE-BOUNDARIES

### 1. experiment_id
`EXP-RP03-PHASE-BOUNDARIES-V1`

### 2. reproduction_candidate
`RP-03`: Structured Phase Boundaries & Assembly-Line SOPs (ChatDev)

### 3. research_question
Does restricting multi-agent collaboration to formal, phase-bounded state transitions (Sequential Standard Operating Procedures) reduce semantic hallucination cascades, duplicated work, and token consumption compared to unrestricted multi-agent conversation, holding models, prompts, roles, and tools strictly constant?

### 4. falsifiable_hypothesis
Enforcing sequential phase boundaries (Demand Analysis $\to$ Architecture Design $\to$ Code Implementation $\to$ Code Review & Testing) will reduce total token consumption by $\ge 25\%$ and reduce defect/error cycles by $\ge 25\%$ ($p < 0.01$, Paired Wilcoxon test) compared to unrestricted multi-agent conversation (`Control B`) on a standardized 150-task software implementation suite (`SimLab-CodeSOP-150`), while maintaining non-inferior unit test pass rates ($\Delta \text{Pass} \ge -3\%$, evaluated via McNemar's test with $>80\%$ statistical power at $\alpha=0.01$).

### 5. null_hypothesis
Structured phase boundaries produce no statistically significant reduction in token spend ($< 10\%$) or defect cycles compared to unrestricted conversation, or induce state-transition rigidity that lowers unit test pass rates by $> 10\%$ ($p < 0.01$).

### 6. primitive_under_test
`PR-ORG-02`: Phased assembly-line organizational structure (SOP state machine).

### 7. reference_mechanism
ChatDev (`OpenBMB/ChatDev`, commit `d512a87`), specifically the `ChatChain` phase-transition engine and `RolePlay` conversational SOPs.

### 8. baseline
- **Control A (Single Agent)**: Single LLM agent with iterative self-reflection and tool access.
- **Control B (Unrestricted Multi-Agent Chat)**: 4 agents (CEO, CTO, Programmer, Reviewer) in a shared conversational channel without phase boundaries, free to speak and exchange messages until consensus or turn limit.

### 9. treatment
**Treatment (T-PhaseSOP)**: The identical 4 agents operating strictly under a sequential phase-gated finite state machine: Phase 1 (Demand Analysis) $\to$ Phase 2 (Architecture Design) $\to$ Phase 3 (Code Implementation) $\to$ Phase 4 (Code Review & Testing), with formal entry/exit gate artifacts.

### 10. independent_variables
Organizational Communication Structure: (`SINGLE_AGENT`, `UNRESTRICTED_CHAT`, `PHASE_BOUNDED_SOP`).

### 11. dependent_variables
1. **Unit Test Pass Rate**: Percentage of pre-defined unit tests passing on the generated code.
2. **Total Tokens Consumed**: Sum of prompt and completion tokens per task.
3. **Conversational Turns**: Number of agent message exchanges before task completion.
4. **Duplicated Work Ratio**: Count of repeated code implementations or identical suggestions.
5. **Cross-Role Contamination**: Frequency of agents performing tasks outside their designated role (e.g. CEO writing Python code).
6. **Conversational Deadlock Rate**: Tasks terminating due to maximum turn exhaustion (16 turns) without emitting a completed code artifact (`CONVERSATIONAL_DEADLOCK_ERROR`).
7. **Sandbox Execution Timeout Rate**: Generated code exceeding container execution limits ($10\text{s CPU}$ / infinite loops, `SANDBOX_TIMEOUT_ERROR`).

### 12. controlled_variables
- Foundation Model: `gpt-4o-2024-08-06` held constant across all conditions.
- Agent Role Personas and System Instructions identical in Control B and Treatment.
- Execution Environment: Isolated Python 3.11 sandbox with identical dependencies.
- Turn Limit: Maximum 16 total conversational turns across both multi-agent conditions.

### 13. model_configuration
`gpt-4o-2024-08-06`, Temperature $T=0.2$, top_p=0.95, Max Tokens per turn: 1500.

### 14. prompt_configuration
Frozen role prompts for CEO, CTO, Programmer, Reviewer extracted from ChatDev release configurations. SHA-256 recorded.

### 15. context_configuration
- Control B: Monolithic appended chat log up to 16k context window.
- Treatment: Phase-scoped contexts; agents only receive the summary artifact from the prior phase, preventing context accumulation blowout.

### 16. randomness_configuration
Fixed random seed `SEED=20260916` for execution order and test harness execution.

### 17. dataset_or_environment
`SimLab-CodeSOP-150`: A balanced benchmark of $N=150$ distinct programming tasks designed to ensure construct validity for a 4-role hierarchy:
- 75 Modular Python Tasks: Multi-step algorithmic and data structure specifications requiring formal requirements decomposition and test writing.
- 75 Multi-File Repository Tasks: Derived from a curated SWE-bench Lite mini-subset (real multi-file Python packages where Demand Analysis [CEO], Architecture/Interface Design [CTO], Implementation [Programmer], and Review/Unit Tests [Reviewer] are genuine architectural artifacts rather than superficial prompt chatter on single functions).

### 18. minimum_run_count
$N = 150$ distinct programming tasks $\times$ 3 conditions = 450 experimental runs.

### 19. statistical_method
- Paired Wilcoxon signed-rank test on token consumption and turn count between `T-PhaseSOP` and `Control B`.
- McNemar's test for paired binary pass/fail outcomes across conditions ($\alpha = 0.01$, achieving $> 80\%$ statistical power at $N=150$).
- Fisher's exact test for conversational deadlock and sandbox timeout proportions.
- Effect size: Cohen's $d$ and Cliff's Delta.

### 20. success_threshold
- $\ge 25\%$ lower token consumption in `T-PhaseSOP` vs `Control B` ($p < 0.01$).
- Equal or non-inferior unit test pass rate ($\Delta \text{Pass} \ge -3\%, p < 0.01$).
- Cross-role contamination reduced by $> 80\%$.

### 21. failure_threshold
- Token reduction $< 10\%$, or `T-PhaseSOP` test pass rate is $> 10\%$ worse than `Control B` due to inability to iterate backwards across phase boundaries ($p < 0.01$).
- **Inconclusive Outcome Rule (`INCONCLUSIVE_SUB_THRESHOLD`)**: If token reduction is between $10\%$ and $25\%$, or pass rate degradation is in $[-10\%, -3\%)$, the result is flagged as `INCONCLUSIVE_SUB_THRESHOLD`. Pre-registered default: SimLab defaults to simpler baseline (`Control A` single agent or unconstrained shared channel), rejecting rigid phase machinery due to insufficient efficiency margins.

### 22. termination_condition
All 150 tasks completed across all 3 conditions, or 16 turns reached per task.

### 23. token_budget
$450 \text{ runs} \times 12 \text{ turns} \times 1,500 \text{ tokens} \approx 8,100,000$ tokens (budget managed under the $100.00 ceiling).

### 24. latency_budget
$< 90$ seconds per task; total benchmark suite execution $< 6$ hours.

### 25. compute_budget
Local sandbox execution for unit tests; $< 2$ GB RAM, standard multi-core CPU.

### 26. logging_requirements
Structured execution logs capturing: `task_id`, `condition`, `turn_index`, `sender_role`, `recipient_role`, `phase_name`, `message_content`, `code_snapshot`, `test_results`, `tokens_in`, `tokens_out`, `latency_ms`.

### 27. provenance_requirements
Git repository hash, Docker container digest for execution sandbox, test assertion logs saved as raw JSON.

### 28. known_confounds
Phase transition rigidities: Tasks requiring rapid back-and-forth debugging between Programmer and Tester may be penalized by rigid sequential phase gates.

### 29. expected_failure_modes
- Phase deadlock: Reviewer repeatedly rejecting code without actionable feedback, exhausting turn budget.
- Context amnesia: Phase summary stripping crucial architectural details needed in later phases.

### 30. what_result_supports
If positive: Validates that formal phase-bounded SOPs drastically curb multi-agent coordination tax and context explosion in structured production workflows.

### 31. what_result_does_not_support
Does NOT prove that open-ended social simulations (like Smallville towns) should use assembly-line phase gates for daily social interactions.

### 32. external_validity_limits
Valid for structured task-oriented software and reasoning workflows. Does not generalize to emergent social behaviors.

### 33. architecture_implication_if_positive
SimLab will adopt an explicit Phase-Gated Orchestration Protocol for multi-agent task execution and code generation modules.

### 34. architecture_implication_if_negative
SimLab will favor flexible blackboard or shared message-bus architectures with dynamic conversational turn-taking, avoiding rigid state-machine transitions.

### 35. execution_authority
`NOT_GRANTED`
