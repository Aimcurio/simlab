# AS-11: System-Level Stress Matrix & Explosion Control Protocol
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Enforceable Stress-Matrix Explosion Control Rule

Combinatorial expansion across multi-agent simulation parameters generates exponential token costs without commensurate scientific clarity. The principle of avoiding combinatorial explosion is hereby converted into an **enforceable governance rule**:

$$\text{SCREEN} \longrightarrow \text{ESCALATE} \longrightarrow \text{INTERACTION\_TEST}$$

### 1.1 Staged Execution Protocol:
1. **Stage A — Screening**:
   - Test **no more than 1–2 stress factors simultaneously**.
   - Purpose: Rapidly filter benign operational parameters from active vulnerability vectors.
2. **Stage B — Escalation**:
   - Escalation is governed by a preregistered dual-criterion decision rule combining **practical degradation** and **statistical evidence**.
   - Escalation to higher stress severity is justified **IF AND ONLY IF** at least one of the following triggers is satisfied:
     - **Trigger A (Practical Degradation)**: A preregistered practical degradation threshold or failure threshold is crossed ([EXAMPLE_ONLY]: illustrative across primitives, e.g. latency $>20$ms, token blowout $>3\times$, completion drop $\ge 10.0\%$; canonical values defined in `AS-04`, `AS-06`, `AS-08`, `AS-10`); **OR**
     - **Trigger B (Statistical Evidence of Material Effect)**: Statistical testing demonstrates a material effect ($p < \alpha$ **AND** the effect size is practically meaningful, $\Delta \ge \Delta_{\text{practical}}$); **OR**
     - **Trigger C (Mechanistic Failure Signal)**: A mechanistically important failure anomaly appears ([EXAMPLE_ONLY]: illustrative, e.g. deadlock loop, silent state divergence, or memory overwrite) that requires bounded follow-up investigation.
   - **Anti-Patterns Strictly Prohibited**:
     - *Prohibition 1*: Requiring $p < \alpha$ as the sole trigger for continued stress testing is forbidden.
     - *Prohibition 2*: Escalating based solely on a tiny, practically trivial difference that achieves statistical significance merely due to sample size is forbidden.
   - Benign dimensions showing neither practical degradation nor statistical significance remain frozen at Baseline.
3. **Stage C — Interaction Testing**:
   - Use factorial interaction tests **only when Stage A screening evidence suggests interaction or when there is a strong mechanistic reason** ([EXAMPLE_ONLY]: e.g. state consensus under network partition).

### 1.2 Cartesian Product Prohibition Invariant
Creating an unconstrained Cartesian product across the eight multi-agent stress dimensions:
1. Agent Count ($N \in \{1, 3, 5, 10, 25\}$)
2. Memory Size ($M \in \{100, 1k, 5k, 10k\}$)
3. Noise ($\eta \in \{0\%, 10\%, 30\%, 50\%\}$)
4. Latency ($\tau \in \{0, 1, 2\text{ ticks}\}$)
5. Tool Failure ($\epsilon_{\text{tool}} \in \{0\%, 5\%, 15\%\}$)
6. Context Pressure ($\rho \in \{50\%, 80\%, 100\%\}$)
7. Distribution Shift (In-domain, Mild, Severe)
8. Communication Load (Low, Medium, High)

is **STRICTLY PROHIBITED** without explicit, written requester authorization. ($5 \times 4 \times 4 \times 3 \times 3 \times 3 \times 3 \times 3 = 58,320$ cells $\implies > \$15,000$ spend; rejected under `NC-38` and `NC-54`).

### 1.3 Mandatory Governance Fields for Stress Experiments
Every Phase 4 stress experiment must explicitly distinguish and declare:
- `number_of_active_factors`: Integer count of simultaneously varied dimensions ($\le 2$ in Stage A).
- `reason_for_combination`: Explicit mechanistic rationale explaining why these factors must interact.
- `interaction_hypothesis`: Formal statement predicting the non-linear coupling effect between factors.
- `maximum_stress_level`: Highest stress intensity authorized for execution (`BASELINE`, `MILD`, `MODERATE`, `SEVERE`).
- `statistical_threshold`: Formal significance level and test specification demonstrating a material statistical effect ([EXAMPLE_ONLY]: illustrative template, e.g. $\alpha = 0.01, \Delta \ge 5.0\%$; see per-primitive plans).
- `practical_degradation_threshold`: Quantitative operational performance drop that warrants engineering concern or escalation ([EXAMPLE_ONLY]: illustrative template, e.g. $> 10.0\%$ drop, $> 20$ms latency, $> 3\times$ token overhead; see per-primitive plans).
- `failure_threshold`: Operating boundary where simulation stability or task accuracy collapses ([EXAMPLE_ONLY]: illustrative template, e.g. $\ge 30.0\%$ drop, $>15.0\%$ deadlock rate; see per-primitive plans).
- `mechanistic_failure_trigger`: Explicitly logged scientifically important failure mode ([EXAMPLE_ONLY]: illustrative, e.g. unrecoverable state divergence, domain starvation, deterministic stale retrieval, cyclic deadlock) requiring bounded follow-up even when sample size is insufficient for formal significance.
- `escalation_rule`: Authorizes progression from `SCREEN` to `ESCALATE` (and `INTERACTION_TEST`) when ANY ONE trigger is satisfied: (A) Practical Degradation, (B) Statistical Evidence, OR (C) Mechanistic Failure Trigger. Escalation solely on $p < \alpha$ when the effect is operationally trivial is strictly prohibited.
- `early_stop_rule`: Deterministic condition that immediately halts runs before reaching maximum stress.

---


## 2. Bounded System-Level Stress Matrix Table

```
+-------------------------------------------------------------------------------------------------------------------------------+
| Stress Vector             | Active Factors (<=2) | Interacting Primitives | Failure Mode | Interaction Hypothesis             |
+-------------------------------------------------------------------------------------------------------------------------------+
| 1. Population Growth      | 1 Factor:            | Memory + Routing + SOP | FM-04 / FM-11| IPC token overhead scales          |
|    (1 to 25 Agents)       | Agent Count          |                        | (Token Blow) | polynomial, not exponential.       |
| 2. Long-Horizon Drift     | 1 Factor:            | Memory (PR-COG-01) +   | FM-02        | Retrieval precision collapses      |
|    (Continuous Ticks)     | Temporal Horizon     | Social Dialogue        | (Drift)      | after 1,000 ticks without pruning. |
| 3. Network Partition      | 2 Factors:           | Debate (PR-ORG-01) +   | FM-06        | Partial observation + dropout      |
|    (Delay + Dropouts)     | Packet Loss + Latency| Distributed State      | (Consensus)  | breaks convergence non-linearly.   |
| 4. Injected Contamination | 2 Factors:           | Memory + Debate        | False Belief | Corrupt seed facts multiply via    |
|    (Adversarial Seeds)    | Corrupt Seeds + Vol  |                        | Cascade      | reflection nodes if unvalidated.   |
| 5. Context Saturation     | 2 Factors:           | SOP (PR-ORG-02) +      | FM-01        | Artifact size + multi-turn depth   |
|    (Artifact Flood)       | Load % + Artifact KB | Tool Execution         | (Truncation) | causes silent truncation in Phase 2|
+-------------------------------------------------------------------------------------------------------------------------------+
```

---

## 3. System Stress Termination Contract

For every system stress vector, the execution harness must pre-register discrete stress tiers and quantitative thresholds:

### 3.1 Four Pre-Registered Stress Levels
1. **`BASELINE`**: Nominal operating envelope ($N \le 3$, $M \le 100$, 0% noise, 0% dropouts).
2. **`MILD`**: Minor operational friction ($N=5$, $M=500$, 10% noise, 1-tick delay).
3. **`MODERATE`**: Real-world challenging conditions ($N=10$, $M=1,000$, 25% noise, 10% dropouts).
4. **`SEVERE`**: Near-boundary stress ($N=25$, $M=5,000$, 50% noise, 25% dropouts).

### 3.2 Four Governing Threshold Contracts
- `failure_threshold`: The point where simulation stability or task accuracy collapses ([EXAMPLE_ONLY]: illustrative, $\ge 30\%$ drop in primary metric or fatal exception rate $> 10\%$; see specific contracts in `AS-04`, `AS-06`, `AS-08`, `AS-10`). Establishing this boundary is the primary goal of stress testing.
- `degradation_threshold`: The point where performance degrades significantly ([EXAMPLE_ONLY]: illustrative, $> 10\%$ drop; see specific contracts in `AS-04`, `AS-06`, `AS-08`, `AS-10`) but remains recoverable.
- `abort_threshold`: Safety, budget, or infrastructure invariant violation ($AF-01$ cumulative spend $>\$50$, host RAM $>1\text{ GB}$, CPU timeout $>60\text{s}$).
- `recovery_threshold`: The system's ability to self-heal or return to baseline accuracy once stress factor is removed.

### 3.3 Termination Invariants
Testing **MUST STOP** immediately when:
1. A definitive failure boundary is established;
2. Safety or budget limits are reached; **OR**
3. Further stress cannot alter the architectural conclusion.

Running to `SEVERE` merely because the level exists is strictly prohibited (`NC-54`).

