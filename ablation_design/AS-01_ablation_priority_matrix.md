# AS-01: Ablation Priority Matrix
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  
**Evaluation Standard**: Qualitative multi-criteria ranking across 8 governance dimensions.  

---

## 1. Prioritization Methodology

Phase 4 ablations and stress tests are prioritized according to:
1. **Architecture Importance**: Impact on eventual 25+ agent persistent simulator design.
2. **Phase 3 Uncertainty**: Degree of statistical ambiguity or sub-threshold outcome in Phase 3.
3. **Failure Severity**: Risk of catastrophic simulation failure (e.g. context explosion, consensus collapse, silent memory corruption).
4. **Cost & Latency**: Feasibility within the $100.00 hard budget ceiling and execution time limits.
5. **Scientific Discriminability**: Ability to isolate the exact causal mechanism behind observed effects.
6. **Transferability**: Relevance across diverse NPC cognitive and organizational domains.
7. **Interaction Risk**: Likelihood of confounding interactions when combined with other primitives.
8. **Falsification Power**: Ability to disprove popular but ungrounded multi-agent literature assumptions.

Qualitative Priority Classes: `CRITICAL`, `HIGH_VALUE`, `USEFUL`, `DEFER`, `REJECT`.

---

## 2. Priority Ranking Table

| Candidate / Target | Target ID | Priority Class | Primary Rationale & Falsification Target | Target Deliverable |
|:---|:---|:---|:---|:---|
| **Private-Information Replication** | `EXP-AB-02-REP` | **`CRITICAL`** | Phase 3 showed promising $+14.0\%$ gain but missed $\alpha = 0.01$ ($p=0.0192$). Confirmatory replication subject to strict immutability contract (12 frozen fields; sample size via power analysis discounting winner's curse). | `AS-05`, `AS-12` |
| **Memory Component Ablation** | `EXP-AB-01-COMP`| **`CRITICAL`** | Determine whether recency, relevance, or importance drives retrieval quality. Phase 3 disproved equal weights; must map the exact mathematical weighting boundary ($\beta > \alpha$). Bound to causal claim discipline. | `AS-03`, `AS-18` |
| **SOP Factorial Decomposition** | `EXP-AB-03-FACT`| **`CRITICAL`** | Disentangle role specialization from phase-gated context resets ($49.2\%$ token savings). Determine whether savings come from context resets or role prompts. Bound to causal claim discipline. | `AS-07`, `AS-18` |
| **Information Asymmetry Gradient**| `EXP-AB-02-ASYM`| **`HIGH_VALUE`**| Sweep private information ($0\%, 25\%, 50\%, 75\%, 100\%$) to find the exact phase transition where multi-agent coordination becomes worth its communication overhead. Bound by explosion screening rules. | `AS-05`, `AS-11` |
| **Memory Scale & Noise Stress** | `EXP-ST-01-SCALE`| **`HIGH_VALUE`**| Stress memory stores from 100 to 10,000+ nodes under noise (duplicates, contradictions, stale records) to locate retrieval breakdown cliff. Governed by Stress Termination Contract. | `AS-04`, `AS-14` |
| **Routing Feature Ablation** | `EXP-AB-04-FEAT`| **`HIGH_VALUE`**| Determine which heuristic features (length, syntax, constraints) drove $27.8\%$ token savings in Phase 3. Preserve simple heuristics; enforce Complexity Burden Rule. | `AS-09`, `AS-10` |
| **Distributed State Tracking Stress**| `EXP-ST-02-STATE`| **`HIGH_VALUE`**| Stress agent population ($1 \to 3 \to 5 \to 10 \to 25$) and observation noise on state tracking where Phase 3 confirmed significant debate advantage ($+18.0\%$). Factorial interaction bounded by Stage C controls. | `AS-06`, `AS-11` |
| **SOP Open-Ended Stress** | `EXP-ST-03-SOP` | **`USEFUL`** | Test whether assembly-line SOPs break under ambiguous or exploratory requirements; verify negative boundary against social simulation. Bounded by early stop rules. | `AS-08`, `AS-14` |
| **Routing Distribution Shift Stress**| `EXP-ST-04-SHIFT`| **`USEFUL`** | Stress heuristic routing under unseen task domains to test Complexity Escalation Rule threshold. Governed by SCREEN $\to$ ESCALATE $\to$ INTERACTION_TEST protocol. | `AS-10`, `AS-11` |
| **Reflection Node Contamination** | `EXP-AB-01-REFL`| **`USEFUL`** | Test whether synthesized reflection nodes act as semantic attractors that crowd out episodic memories. Offline vector evaluation. | `AS-03`, `AS-18` |
| **50+ Agent Population Stress** | `EXP-ST-SYS-50` | **`DEFER`** | Deferred to Phase 8 scale testing. 25-agent stability must be established first. | `AS-11` |
| **Learned Puppeteer Router** | `EXP-AB-04-PUPP`| **`DEFER`** | Classified strictly as `NOT_TESTED_DUE_TO_STOPPING_RULE`. Escalation authorized ONLY if heuristic routing fails preregistered stress criteria or approved hypothesis requires comparison. | `AS-10` |
| **Homogeneous GSM8K Debate** | `EXP-AB-02-GSM` | **`REJECT`** | Phase 3 proved TOST equivalence was not established and debate incurred an $8.2\%$ false consensus rate. Unproductive to burn tokens on closed math without tools. | `AS-05` |
| **Equal-Weighted Memory** | `EXP-AB-01-EQ` | **`REJECT`** | Empirically falsified in Phase 3 ($d=0.26$, sub-threshold). Discarded from further evaluation. | `AS-03` |

---

## 3. Governance Cross-References & Gate Constraints
- **Design Gate Clarification**: Pre-execution certification belongs strictly to `PHASE_4_DESIGN_GATE`. Post-execution outcome adjudication is reserved for `GATE_R4`.
- **Stress-Matrix Explosion Rules**: Combinatorial expansion across the 8 stress dimensions is strictly prohibited; all tests must follow the `SCREEN -> ESCALATE -> INTERACTION_TEST` protocol (`AS-11`).
- **Primitive Advancement Invariant**: Advancement to final Primitive Adjudication requires satisfying all seven criteria (A through G) in the Primitive Advancement Contract (`AS-18`).

