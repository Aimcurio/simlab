# AS-04: Memory Stress Plan
**Experiment ID**: `EXP-ST-01-SCALE`  
**Target Primitive**: `PR-COG-01` (Tri-Factor Memory Retrieval Scoring)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
At what memory store scale ($M$), temporal horizon ($T$), and noise ratio ($\eta$) does tri-factor memory retrieval collapse, and what is the computational and accuracy cost of memory growth?

---

## 2. Stress-Matrix Explosion Controls (`SCREEN -> ESCALATE -> INTERACTION_TEST`)

- **Stage A (Screening)**: Evaluate Memory Scale alone ($M \in \{100, 500, 1000\}$) and Noise alone ($\eta \in \{0\%, 10\%, 30\%\}$).
- **Stage B (Escalation)**: Escalate to combined $M \times \eta$ only across confirmed sensitivity ranges.

### Experiment Metadata Contract:
- `number_of_active_factors`: 2 active factors (Store Volume $M$ + Noise Ratio $\eta$).
- `reason_for_combination`: High store volume increases vector crowding, which magnifies semantic interference from lexical distractors.
- `interaction_hypothesis`: Retrieval precision exhibits a non-linear cliff when memory size exceeds $1,000$ nodes in the presence of $\ge 30\%$ distractor noise.
- `maximum_stress_level`: `SEVERE` ($M=5,000$, 50% noise).
- `early_stop_rule`: Terminate experiment immediately if single-query CPU latency exceeds $50$ms or if false retrieval rate crosses $40.0\%$.

---

## 3. Stress Progression & Termination Contract

### 3.1 Pre-Registered Stress Levels:
1. **`BASELINE`**: $M=100$ nodes, 0% noise, short temporal horizon ($\Delta t \le 50$).
2. **`MILD`**: $M=500$ nodes, 10% distractor noise, medium horizon ($\Delta t \le 500$).
3. **`MODERATE`**: $M=1,000$ nodes, 30% noise (duplicates + contradictory facts), medium horizon.
4. **`SEVERE`**: $M=5,000$ nodes, 50% noise (including misleading high-importance lures), long horizon ($\Delta t \le 5,000$).

### 3.2 Quantitative Threshold Contracts:
- `statistical_threshold`: Degradation significance at $\alpha = 0.01$ across $N \ge 100$ queries per condition, demonstrating a material statistical effect.
- `practical_degradation_threshold`: MRR drops $> 20.0\%$ from baseline OR single-query retrieval CPU latency exceeds $20$ms.
- `failure_threshold`: MRR drops below $0.10$ ($p < 0.01$) **OR** false retrieval rate exceeds $40.0\%$. (Establishes the primitive's operational capacity boundary).
- `mechanistic_failure_trigger`: Memory corruption causes deterministic stale retrieval, key invariant collapse, or catastrophic semantic index poisoning under distractor lures even when sample size is insufficient for formal significance. Must be explicitly logged, identify the observed failure mechanism, justify the bounded follow-up, and not permit unrestricted exploratory expansion.
- `escalation_rule`: Escalate from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE of the following preregistered triggers is satisfied:
  1. **Practical Degradation Trigger**: `practical_degradation_threshold` or `failure_threshold` is crossed ($\Delta \text{MRR} > 20.0\%$ or latency $> 20$ms); **OR**
  2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < 0.01$); **OR**
  3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears (e.g. deterministic stale retrieval) justifying bounded follow-up.
  *Practical-Significance Discipline*: Escalating solely on statistical significance ($p < \alpha$) when the observed effect is operationally trivial ($\Delta \text{MRR} < 5.0\%$, latency shift $< 2$ms) is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.
- `early_stop_rule`: Terminate experiment immediately if single-query CPU latency exceeds $50$ms or if false retrieval rate crosses $40.0\%$.
- `abort_threshold`: Single-query retrieval latency $> 100$ms or memory footprint $> 1.0$ GB RAM ($AF-05$).
- `recovery_threshold`: Pruning superseded memories restores MRR to within $10\%$ of clean baseline.

### 3.3 Termination Invariant
Testing must stop when:
1. The failure boundary is established;
2. Safety or host resource constraints are reached; **OR**
3. Further stress cannot alter the architectural conclusion.

Do not execute to extreme levels ($10,000+$ nodes) unless `MODERATE` stress is survived (`NC-54`).

