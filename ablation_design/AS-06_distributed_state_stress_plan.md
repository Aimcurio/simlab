# AS-06: Distributed-State Stress Plan
**Experiment ID**: `EXP-ST-02-STATE`  
**Target Primitive**: `PR-ORG-01` (Multi-Agent Debate & Cross-Examination)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
How does multi-agent state tracking perform as agent population scales from 1 to 25 agents, and under what levels of communication delay, agent dropout, and observation error does distributed coordination break down?

---

## 2. Stress-Matrix Explosion Controls (`SCREEN -> ESCALATE -> INTERACTION_TEST`)

- **Stage A (Screening)**: Population scaling alone ($N \in \{1, 3, 5, 10\}$) under zero noise.
- **Stage B (Escalation)**: Escalate to $N=25$ and introduce partial observation bandwidth ($\le 20\%$).
- **Stage C (Interaction Testing)**: Factorial evaluation of Population ($N=10, 25$) $\times$ Observation Noise ($\epsilon \in \{0\%, 10\%, 25\%\}$) to evaluate consensus breakdown.

### Experiment Metadata Contract:
- `number_of_active_factors`: 2 active factors (Population Size $N$ + Observation Error $\epsilon_{\text{obs}}$).
- `reason_for_combination`: Multi-agent consensus mechanisms behave differently when both participant count and observational uncertainty increase simultaneously.
- `interaction_hypothesis`: Communication overhead scales polynomially ($\mathcal{O}(N^2)$) under clean observations, but diverges into exponential message amplification when observation noise exceeds $20\%$.
- `maximum_stress_level`: `SEVERE` ($N=25$, 25% observation corruption, 10% agent dropout).
- `early_stop_rule`: Terminate experiment immediately if token consumption scales worse than $\mathcal{O}(N^2)$ or if tracking accuracy drops below compute-matched single-agent baseline.

---

## 3. Stress Progression & Termination Contract

### 3.1 Pre-Registered Stress Levels:
1. **`BASELINE`**: $N=1$ agent (baseline state tracking), full observation, 0% noise.
2. **`MILD`**: $N=3$ agents, partial observation ($33\%$ FOV each), 0% error.
3. **`MODERATE`**: $N=10$ agents, partial observation ($10\%$ FOV), 10% false-entity noise, 1-tick message delay.
4. **`SEVERE`**: $N=25$ agents, partial observation ($5\%$ FOV), 25% contradictory reports, 10% agent dropout. (50+ agents strictly deferred per `NC-57`).

### 3.2 Quantitative Threshold Contracts:
- `statistical_threshold`: Accuracy difference significant at $\alpha = 0.01$ across $N \ge 50$ episodes per population level, demonstrating a material statistical effect.
- `practical_degradation_threshold`: Tracking accuracy drops $> 10.0\%$ below nominal debate baseline OR IPC token overhead exceeds $3\times$ single-agent tokens.
- `failure_threshold`: Tracking accuracy drops below single-agent control ($< 66.0\%$) **OR** consensus latency exceeds $8$ debate rounds.
- `mechanistic_failure_trigger`: Agent dropout creates unrecoverable state divergence, broadcast loop deadlock, or split-brain world models even when sample size is insufficient for formal significance. Must be explicitly logged, identify the observed failure mechanism, justify the bounded follow-up, and not permit unrestricted exploratory expansion.
- `escalation_rule`: Escalate from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE of the following preregistered triggers is satisfied:
  1. **Practical Degradation Trigger**: `practical_degradation_threshold` or `failure_threshold` is crossed (accuracy loss $> 10.0\%$, overhead $> 3\times$, or latency $> 8$ rounds); **OR**
  2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < 0.01$); **OR**
  3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears (e.g. unrecoverable state divergence under dropout) justifying bounded follow-up.
  *Practical-Significance Discipline*: Escalating solely on statistical significance ($p < \alpha$) when the observed effect is operationally trivial (tracking accuracy loss $< 2.0\%$, token shift $< 5\%$) is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.
- `early_stop_rule`: Terminate experiment immediately if token consumption scales worse than $\mathcal{O}(N^2)$ or if tracking accuracy drops below compute-matched single-agent baseline.
- `abort_threshold`: Episode token spend exceeds $50,000$ tokens or debate loop exceeds $16$ turns ($AF-04$).
- `recovery_threshold`: Central state broadcast restores accuracy to $\ge 90.0\%$.

### 3.3 Termination Invariant
Testing must stop when:
1. The failure boundary is established;
2. Budget ceilings or token runaway limits are reached; **OR**
3. Further stress cannot alter the architectural conclusion.

Do not run to maximum population ($N=25$) under `SEVERE` noise if failure occurs at `MODERATE` ($N=10$) (`NC-54`).

