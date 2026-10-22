# AS-08: SOP Stress Plan
**Experiment ID**: `EXP-ST-03-SOP`  
**Target Primitive**: `PR-ORG-02` (Phased Assembly-Line SOP State Machine)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
Under what task conditions and team sizes does rigid assembly-line SOP structure degrade performance, induce deadlock, or fail compared to dynamic or unstructured interaction?

---

## 2. Stress-Matrix Explosion Controls (`SCREEN -> ESCALATE -> INTERACTION_TEST`)

- **Stage A (Screening)**: Test Task Ambiguity alone (Clear $\to$ Ambiguous $\to$ Exploratory).
- **Stage B (Escalation)**: Test Upstream Defect Injection under ambiguous tasks.
- **Stage C (Interaction Testing)**: Factorial evaluation of Task Ambiguity $\times$ Dynamic Requirement Shift.

### Experiment Metadata Contract:
- `number_of_active_factors`: 2 active factors (Task Ambiguity Level + Mid-Stream Requirement Shift).
- `reason_for_combination`: Waterfall pipelines exhibit hysteresis: changes introduced after code phase commencement test rollback state machines.
- `interaction_hypothesis`: Rigid phase gates prevent downstream stages from negotiating ambiguities, resulting in infinite Reviewer-Coder deadlock loops.
- `maximum_stress_level`: `SEVERE` (Mid-stream requirement mutation + injected upstream architecture flaw).
- `early_stop_rule`: Terminate experiment immediately if deadlock frequency exceeds $15.0\%$ or task completion drops $> 20.0\%$ below unstructured chat.

---

## 3. Stress Progression & Termination Contract

### 3.1 Pre-Registered Stress Levels:
1. **`BASELINE`**: Deterministic specifications with explicit I/O examples and pre-written pytest assertions.
2. **`MILD`**: Ambiguous requirements with missing edge cases and implicit dependencies.
3. **`MODERATE`**: Exploratory tasks lacking closed ground-truth answers (e.g. game balancing, creative simulation design).
4. **`SEVERE`**: Dynamic requirement shifts introduced after Phase 2 (Coding) begins, combined with upstream defect injection in Phase 1 (Design).

### 3.2 Quantitative Threshold Contracts:
- `statistical_threshold`: Deadlock rate and completion differences significant at $\alpha = 0.01$ across $N \ge 50$ tasks per condition, demonstrating a material statistical effect.
- `practical_degradation_threshold`: Turn count per phase exceeds $10$ turns OR rollback token cost $> 50\%$ of base task tokens.
- `failure_threshold`: Review loop deadlock rate exceeds $15.0\%$ **OR** task completion rate drops $> 20.0\%$ below baseline. (Establishes negative boundary for SOP applicability).
- `mechanistic_failure_trigger`: SOP state machine deadlocks under a specific failure condition (e.g. infinite Coder-Reviewer ping-pong, cyclic rollback traps, or irreversible transition failure) even when sample size is insufficient for formal significance. Must be explicitly logged, identify the observed failure mechanism, justify the bounded follow-up, and not permit unrestricted exploratory expansion.
- `escalation_rule`: Escalate from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE of the following preregistered triggers is satisfied:
  1. **Practical Degradation Trigger**: `practical_degradation_threshold` or `failure_threshold` is crossed (deadlock rate $> 15.0\%$, completion loss $> 20.0\%$, or turns $> 10$); **OR**
  2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < 0.01$); **OR**
  3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears (e.g. cyclic phase deadlock) justifying bounded follow-up.
  *Practical-Significance Discipline*: Escalating solely on statistical significance ($p < \alpha$) when the observed effect is operationally trivial (deadlock rate delta $< 1.0\%$, turn count delta $< 0.5$ turns) is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.
- `early_stop_rule`: Terminate experiment immediately if deadlock frequency exceeds $15.0\%$ or task completion drops $> 20.0\%$ below unstructured chat.
- `abort_threshold`: Reviewer/Coder review loop exceeds $16$ turns in $>15\%$ of tasks ($AF-03$).
- `recovery_threshold`: Explicit backward phase rollback recovers passing code in $\ge 80.0\%$ of defects.

### 3.3 Termination Invariant
Testing must stop when:
1. The negative task boundary for rigid SOPs is established;
2. Safety or budget limits are reached; **OR**
3. Further stress cannot alter the architectural conclusion.

Do not run to maximum team size ($K=10$) under `SEVERE` ambiguity once failure is established at $K=3$ (`NC-54`).

