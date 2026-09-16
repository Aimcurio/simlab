# AS-01: Ablation Priority Matrix
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
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
| **Private-Information Replication** | `EXP-AB-02-REP` | **`CRITICAL`** | Phase 3 showed promising $+14.0\%$ gain but missed $\alpha = 0.01$ ($p=0.0192$). High-powered confirmatory replication ($N=270$) required before debate can influence SimLab architecture. | `AS-05` |
| **Memory Component Ablation** | `EXP-AB-01-COMP`| **`CRITICAL`** | Determine whether recency, relevance, or importance drives retrieval quality. Phase 3 disproved equal weights; must map the exact mathematical weighting boundary ($\beta > \alpha$). | `AS-03` |
| **SOP Factorial Decomposition** | `EXP-AB-03-FACT`| **`CRITICAL`** | Disentangle role specialization from phase-gated context resets ($49.2\%$ token savings). Determine whether savings come from context resets or role prompts. | `AS-07` |
| **Information Asymmetry Gradient**| `EXP-AB-02-ASYM`| **`HIGH_VALUE`**| Sweep private information ($0\%, 25\%, 50\%, 75\%, 100\%$) to find the exact phase transition where multi-agent coordination becomes worth its communication overhead. | `AS-05` |
| **Memory Scale & Noise Stress** | `EXP-ST-01-SCALE`| **`HIGH_VALUE`**| Stress memory stores from 100 to 10,000+ nodes under noise (duplicates, contradictions, stale records) to locate the retrieval breakdown cliff. | `AS-04` |
| **Routing Feature Ablation** | `EXP-AB-04-FEAT`| **`HIGH_VALUE`**| Determine which of the heuristic features (length, syntax, constraints) drove $27.8\%$ token savings in Phase 3. Preserve simple heuristics before considering neural routers. | `AS-09` |
| **Distributed State Tracking Stress**| `EXP-ST-02-STATE`| **`HIGH_VALUE`**| Stress agent population ($1 \to 3 \to 5 \to 10 \to 25$) and observation noise on state tracking where Phase 3 confirmed significant debate advantage ($+18.0\%$). | `AS-06` |
| **SOP Open-Ended Stress** | `EXP-ST-03-SOP` | **`USEFUL`** | Test whether assembly-line SOPs break under ambiguous or exploratory requirements; verify the negative boundary against social simulation. | `AS-08` |
| **Routing Distribution Shift Stress**| `EXP-ST-04-SHIFT`| **`USEFUL`** | Stress heuristic routing under unseen task domains to test the Complexity Escalation Rule threshold. | `AS-10` |
| **Reflection Node Contamination** | `EXP-AB-01-REFL`| **`USEFUL`** | Test whether synthesized reflection nodes act as semantic attractors that crowd out episodic memories. | `AS-03` |
| **50+ Agent Population Stress** | `EXP-ST-SYS-50` | **`DEFER`** | Deferred to Phase 8 scale testing. 25-agent stability must be established first. | `AS-11` |
| **Learned Puppeteer Router** | `EXP-AB-04-PUPP`| **`DEFER`** | Classified as `NOT_TESTED_DUE_TO_STOPPING_RULE`. Escalation deferred until heuristic router fails stress testing. | `AS-10` |
| **Homogeneous GSM8K Debate** | `EXP-AB-02-GSM` | **`REJECT`** | Phase 3 proved TOST equivalence was not established and debate incurred an $8.2\%$ false consensus rate. Unproductive to burn tokens on closed math without tools. | `AS-05` |
| **Equal-Weighted Memory** | `EXP-AB-01-EQ` | **`REJECT`** | Empirically falsified in Phase 3 ($d=0.26$, sub-threshold). Discarded from further evaluation. | `AS-03` |
