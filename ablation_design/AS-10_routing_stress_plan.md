# AS-10: Routing Stress Plan
**Experiment ID**: `EXP-ST-04-SHIFT`  
**Target Primitive**: `PR-ORG-03` (Dynamic Agent Routing & Orchestration)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question & Invariant Role of High-Tier Routers

### 1.1 Preservation of Phase 3 Stopping-Rule Invariants
In Phase 3, heuristic routing delivered $27.80\%$ token savings with only $-2.0\%$ accuracy degradation, triggering `STOP_ESCALATION_VALID`. In strict accordance with `NC-43`, `NC-50`, and `NC-59`:
- **`LLM_ROUTER` = `NOT_TESTED_DUE_TO_STOPPING_RULE`**
- **`LEARNED_PUPPETEER_ROUTING` = `NOT_TESTED_DUE_TO_STOPPING_RULE`**

Phase 4 preserves these statuses as non-inferior stopping-rule classifications. Under no circumstances will neural or Puppeteer routers be tested merely for completeness, curiosity, or exhaustive benchmarking. Phase 4 may authorize testing them **ONLY IF**:
1. `HEURISTIC_ROUTING` fails pre-registered stress criteria (accuracy degradation $> 10.0\%$ and under-activation $> 15.0\%$); **OR**
2. A specific, formally approved requester hypothesis explicitly mandates a direct head-to-head comparison.

---

## 2. Stress-Matrix Explosion Controls (`SCREEN -> ESCALATE -> INTERACTION_TEST`)

To prevent combinatorial explosion across multi-agent routing dimensions, stress testing follows a staged protocol:
- **Stage A (Screening)**: Test 1 factor at a time (Distribution Shift alone, then Adversarial Deception alone). Maximum 1–2 factors active.
- **Stage B (Escalation)**: Governed by dual-criterion decision rule combining practical degradation and statistical evidence. Escalation to higher stress severity occurs **IF AND ONLY IF**:
  1. A preregistered practical degradation threshold is crossed (`practical_degradation_threshold`); **OR**
  2. Statistical evidence demonstrates a material effect (`statistical_threshold`); **OR**
  3. A mechanistically important failure anomaly appears (e.g. chronic under-activation on critical constraints).
  *Anti-Pattern*: Do not require $p < \alpha$ as the sole trigger, and do not escalate on trivial statistical noise.
- **Stage C (Interaction Testing)**: Factorial interaction evaluated only between confirmed vulnerabilities.

### Experiment Metadata Contract:
- `number_of_active_factors`: 1 active factor during Stage A screening (Domain Shift); 2 active factors in Stage B escalation (Domain Shift + Prompt Length Deception).
- `reason_for_combination`: Mechanistic vulnerability testing — evaluates whether syntactic heuristics fail when concise length is paired with out-of-domain vocabulary.
- `interaction_hypothesis`: Short adversarial prompts will induce under-activation, but syntactic constraint multiplicity ($f_3$) will prevent catastrophic misrouting.
- `statistical_threshold`: Paired McNemar $p < 0.01$ demonstrating material degradation ($\Delta \ge 5.0\%$).
- `warning_threshold` (Practical Degradation): Routing accuracy drop $> 5.0\%$ below Static Topology (advisory engineering degradation warning; does not trip architectural escalation).
- `escalation_threshold`: Routing accuracy drop $> 10.0\%$ below Static Topology ($p < 0.01$) **OR** under-activation rate $> 15.0\%$. (Canonical preregistered routing escalation threshold per `NC-69` and `AS-09` to justify learned router escalation).
- `failure_threshold` (Severe Collapse): Under-activation rate $> 20.0\%$ (trips `AF-06` hard abort and router triage).
- `mechanistic_failure_trigger`: Router systematically fails a specific class of expert domains (e.g. complete starvation of logic specialists on concise adversarial prompts) even when sample size is insufficient for formal significance. Must be explicitly logged, identify the observed failure mechanism, justify bounded follow-up, and not permit unrestricted exploratory expansion.
- `escalation_rule`: Escalate from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE of the following preregistered triggers is satisfied:
  1. **Preregistered Escalation Trigger**: Canonical `escalation_threshold` is crossed (accuracy drop $> 10.0\%$ OR under-activation rate $> 15.0\%$); **OR**
  2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < 0.01$, $\Delta \ge 5.0\%$); **OR**
  3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears (e.g. systematic expert domain starvation) justifying bounded follow-up.
  *Practical-Significance Discipline*: Escalating solely on statistical significance ($p < \alpha$) when the observed degradation is below the canonical material effect threshold ($\Delta < 5.0\%$, i.e. observed effect delta $< 0.05$) is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.
- `early_stop_rule`: Terminate experiment immediately if heuristic routing satisfies the failure boundary or if 3 consecutive evaluation batches show zero routing accuracy changes.

### 2.1 Formal Amendment Record: PHASE4_ESCALATION_RULE_AMENDMENT
- `amendment_id`: `PHASE4_ESCALATION_RULE_AMENDMENT`
- `previous_rule`: `accuracy_drop > 10.0% (p < 0.01) AND under_activation_rate > 15.0%` (Historical commit `5d7b1ab`).
- `new_rule`: Multi-trigger disjunctive rule with practical-significance discipline (Trigger A: Practical Degradation OR Trigger B: Statistical Evidence of Material Effect $\Delta \ge 5.0\%$ OR Trigger C: Bounded Mechanistic Failure Trigger).
- `reason_for_change`: The historical AND-pair conjunctive rule is an anti-pattern for stress testing; requiring both statistical significance and extreme practical failure simultaneously blinds the screening harness to severe operational degradation (e.g. 18% under-activation without p-value convergence) and delays triage.
- `scientific_rationale`: Screening experiments must escalate upon discovering either a material practical sensitivity, a statistically sound degradation with non-trivial effect size, or an overt mechanistic failure. Practical failure does not require statistical significance to matter, and statistical significance does not make a trivial effect operationally important.
- `governance_rationale`: Eliminates ambiguity between screening rules and adjudication standards, ensuring execution harnesses evaluate explicit, non-conflicting operational criteria across all tiers.
- `affected_artifacts`: `AS-09`, `AS-10`, `AS-11`, `AS-14`, `AS-15`, `AS-16`, `AS-17`, `curo_phase4_ablation_package.md`.
- `reviewer`: Dr. Sol (Independent Senior Reviewer & Failure Analyst).
- `approval_state`: `APPROVED_FOR_EXECUTION_READINESS`.
- `effective_version`: Phase 4 Design Hardened v2.4.
- `effective_commit`: Canonical pre-execution checkpoint.
- `superseded_rule_status`: `SUPERSEDED_RULE` (Historical provenance preserved from commit `5d7b1ab`; non-operative).

### 2.2 Canonical Executable-Style Routing Escalation Logic
```python
def should_escalate_routing_stress(
    routing_accuracy_drop: float,
    routing_under_activation: float,
    statistical_p_value: float,
    observed_effect_delta: float,
    approved_mechanistic_failure_logged: bool
) -> bool:
    # Trigger A: Practical Degradation Trigger
    practical_degradation_trigger = (
        (routing_accuracy_drop > 0.10) or
        (routing_under_activation > 0.15)
    )
    
    # Trigger B: Statistical Trigger with Material Effect Size (>= 5.0%)
    # Enforces practical-significance discipline: sub-threshold effects (delta < 0.05) cannot trip Trigger B
    statistical_trigger = (
        (statistical_p_value < 0.01) and
        (observed_effect_delta >= 0.05)  # ROUTING_STATISTICAL_TRIGGER_EFFECT_THRESHOLD = 5.0%
    )
    
    # Trigger C: Bounded Mechanistic Failure Trigger
    mechanistic_failure_trigger = approved_mechanistic_failure_logged

    # Escalation Rule: Disjunctive Multi-Trigger
    return practical_degradation_trigger or statistical_trigger or mechanistic_failure_trigger
```


---

## 3. Stress Progression, Justification & Termination Contract

### 3.1 Pre-Registered Stress Levels
1. **`BASELINE`**: In-distribution code generation and GSM8K math problems formatted identically to training distributions.
2. **`MILD`**: Conversational paraphrasing and syntactic style mutations of standard in-distribution tasks.
3. **`MODERATE`**: Unseen task domains (legal contract analysis, medical diagnostic queries, multi-hop temporal logic).
4. **`SEVERE`**: Adversarial Deception Attacks:
   - *Concise Complexity*: High-difficulty reasoning problems compressed into $< 15$ words.
   - *Verbose Simplicity*: Elementary string manipulation buried within $> 500$ words of conversational padding.

### 3.2 Scientific & Operational Justification of Routing Escalation Thresholds
The escalation triggers (`accuracy loss > 10.0%` and `under-activation > 15.0%`) were established prior to Phase 4 execution based on explicit operational principles:
- **Accuracy Loss Threshold ($> 10.0\%$)**:
  - *Baseline Context*: In Phase 3, heuristic routing achieved $27.80\%$ token savings with only $-2.0\%$ accuracy degradation relative to static full broadcast.
  - *Operational Rationale*: Heuristic routing is justified strictly by token savings without material quality degradation. A $10.0\%$ accuracy degradation represents a $5\times$ expansion of baseline error loss, erasing more utility than the $27.8\%$ token savings provide.
  - *Statistical Rationale*: On a benchmark of $N=100$ held-out tasks, an accuracy drop $> 10.0\%$ achieves statistical significance at $\alpha = 0.01$ ($p < 0.01$).
- **Under-Activation Threshold ($> 15.0\%$)**:
  - *Operational Rationale*: Under-activation occurs when complex multi-step tasks requiring specialist multi-agent interaction are erroneously routed to a single baseline agent. In autonomous simulations, under-activating specialist roles causes silent downstream task corruption. An under-activation rate $> 15.0\%$ means more than 1 in 7 complex tasks are misrouted, exceeding acceptable fault tolerance for autonomous execution kernels (`NC-01`, `NC-34`).

### 3.3 Quantitative Threshold Contracts
- `statistical_threshold`: Paired McNemar $p < 0.01$ with meaningful effect size ($\Delta \ge 5.0\%$).
- `warning_threshold`: Routing accuracy drop $> 5.0\%$ below Static Topology (advisory degradation warning).
- `escalation_threshold`: Routing accuracy drop $> 10.0\%$ below Static Topology ($p < 0.01$) **OR** under-activation rate exceeds **$15.0\%$**. (Canonical preregistered architectural escalation threshold per `NC-50`, `NC-69`, and `AS-09`).
- `failure_threshold`: Heuristic under-activation rate exceeds **$20.0\%$** (`AF-06`, severe routing collapse tripping hard abort).
- `mechanistic_failure_trigger`: Router systematically starves a specialist domain class (e.g. 0% activation on concise logic prompts) even when sample size is insufficient for formal significance. Must be explicitly logged, bounded follow-up only, no unrestricted expansion.
- `escalation_rule`: Authorize progression from Mild to Moderate/Severe when canonical `escalation_threshold` is crossed (accuracy drop $> 10.0\%$ or under-activation $> 15.0\%$), or `statistical_threshold` is satisfied (paired McNemar $p < 0.01$ and $\Delta \ge 5.0\%$), or `mechanistic_failure_trigger` appears. Escalation on sub-threshold effect size ($\Delta < 5.0\%$, i.e. observed effect delta $< 0.05$) is strictly prohibited under Trigger B.
- `abort_threshold`: Router parsing or syntactic extraction errors exceed $5.0\%$ of queries.
- `recovery_threshold`: Fallback to static topology broadcast restores accuracy to within $1.0\%$ of full static baseline.

### 3.4 Termination Invariant
Testing must stop when:
1. The failure boundary is established;
2. Safety or financial budget limits are reached ($AF-01$, $AF-06$); **OR**
3. Further stress cannot change the architectural conclusion.

Do not run to maximum stress merely because the level exists (`NC-54`).


