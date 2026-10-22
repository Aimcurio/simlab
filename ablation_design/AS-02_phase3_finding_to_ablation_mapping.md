# AS-02: Phase 3 Finding-to-Ablation Mapping
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Mapping Phase 3 Empirical Outcomes to Phase 4 Experimental Designs

| Phase 3 Candidate | Phase 3 Empirical Finding | Phase 3 Reconciled Status | Remaining Epistemic Unknown | Phase 4 Investigation Design |
|:---|:---|:---|:---|:---|
| **RP-01** (Memory Recency) | Corrected exponential decay dropped inversion rate $74.5\% \to 41.0\%$. Equal weighting failed ($\Delta \text{MRR} = +0.0446$); tuned weighting succeeded ($\Delta \text{MRR} = +0.1685, p < 0.001$). | `SUPPORTED_WITH_CONSTRAINTS` | Which component (recency vs relevance vs importance) is necessary and sufficient? At what memory scale does retrieval break down? | **`AS-03`** (8-Condition Component Ablation; bound to 5-field Causal Claim Discipline)<br/>**`AS-04`** (Scale 100 to 10,000+ & Noise Stress; bound to Stress Termination Contract) |
| **RP-02** (Debate vs B1-SC: Private Info) | Multi-agent debate achieved $+14.0\%$ accuracy gain ($87/100$ vs $73/100$), but $p = 0.0192 > 0.01$. Compute matched within $+2.48\%$. | `PROMISING_BUT_NOT_SIGNIFICANT` | Is the $+14.0\%$ advantage reproducible at $\alpha = 0.01$ under adequate statistical power? At what degree of information asymmetry does debate become useful? | **`AS-05`** (Confirmatory Replication $N=300$; bound to 12-field Immutability Contract; Asymmetry Gradient Sweep $0\%\dots100\%$) |
| **RP-02** (Debate vs B1-SC: Closed GSM8K) | Difference was $+4.40\%$ ($446/500$ vs $424/500$). TOST failed to establish equivalence at $\delta = \pm 0.03$ ($p = 0.741$). False consensus observed in $8.2\%$ of runs. | `EQUIVALENCE_NOT_ESTABLISHED` | Does debate provide any genuine reasoning amplification or merely introduce sycophancy risk on closed tasks? | **`AS-05`** (Closed reasoning deprioritized; focused on partitioned knowledge boundaries; anti-sycophancy constraints) |
| **RP-02** (Debate vs B1-SC: State Tracking) | Multi-agent debate achieved $+18.0\%$ accuracy gain ($84/100$ vs $66/100$, $p = 0.0051 < 0.01$) on distributed state tracking. | `SUPPORTED` | How robust is multi-agent state tracking as agent count grows ($1 \to 25$) and observation noise increases? | **`AS-06`** (Population Sweep $1\dots25$ & Partial Observation Stress; Stage C interaction controls) |
| **RP-03** (ChatDev Phased SOPs) | Phase boundaries cut tokens by $49.17\%$ ($p < 10^{-14}$) and eliminated cross-role violations ($1.80 \to 0.00$) with $+6.15\%$ pass rate. | `SUPPORTED_WITH_CONSTRAINTS` | Are savings driven by role specialization, phase-gated context pruning, or both? Does structure harm exploratory tasks? | **`AS-07`** ($2 \times 2$ Factorial Component Ablation; Causal Claim Discipline)<br/>**`AS-08`** (Ambiguous & Exploratory Task Stress; Termination Contract) |
| **RP-04** (Dynamic Orchestration) | Heuristic routing saved $27.80\%$ tokens with $-2.0\%$ accuracy loss. `STOP_ESCALATION_VALID` invoked. Higher tiers not executed. | `SUPPORTED_WITH_CONSTRAINTS` | Which heuristic features drive efficiency? Under what task distribution shift does heuristic routing fail badly enough to justify neural routing? | **`AS-09`** (Leave-One-Out Feature Ablation)<br/>**`AS-10`** (Adversarial Distribution Shift Stress; Complexity Escalation Rule preserved) |

---

## 2. Invariant Epistemic Governance
- **Confirmatory Replication Immutability**: RP-02 replication requires exact adherence to the 12 frozen protocol fields (`AS-05`). Any modification converts the classification to `AMENDED_REPLICATION` requiring `EXPERIMENT_AMENDMENT_REQUIRED`.
- **Advancement Prerequisite**: No Phase 3 finding automatically promotes a primitive to final architecture. Advancement to Primitive Adjudication requires satisfying all seven criteria (A through G) defined in `AS-18`.

