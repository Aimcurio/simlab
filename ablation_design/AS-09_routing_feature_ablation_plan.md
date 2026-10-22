# AS-09: Routing Feature Ablation Plan
**Experiment ID**: `EXP-AB-04-FEAT`  
**Target Primitive**: `PR-ORG-03` (Dynamic Agent Routing & Orchestration)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
Which specific features in the multi-feature heuristic routing function are necessary to maintain $\ge 25\%$ token savings while preserving $\le 3\%$ accuracy loss compared to static full topology?

---

## 2. Leave-One-Out Feature Ablation Design

Evaluated on `SimLab-HeteroBench-300` ($N=300$ tasks, 70/30 train/test split):

### Heuristic Feature Space:
- $f_1$: **Estimated Query Length & Token Count** (lexical volume).
- $f_2$: **Syntax Complexity Indicators** (presence of code blocks, formal logic, multi-step clauses).
- $f_3$: **Constraint Multiplicity** (number of explicit requirements or negative constraints).
- $f_4$: **Domain Keyword Specificity** (specialized technical vocabulary).
- $f_5$: **Task Type Taxonomy** (classification into Simple, Moderate, Complex).

### Evaluated Conditions:
- **H-Full**: Complete multi-feature heuristic router ($f_1 + f_2 + f_3 + f_4 + f_5$).
- **H-Minus-1**: Omit query length ($f_1$).
- **H-Minus-2**: Omit syntax complexity ($f_2$).
- **H-Minus-3**: Omit constraint multiplicity ($f_3$).
- **H-Minus-4**: Omit domain keywords ($f_4$).
- **H-Minus-5**: Omit task type classification ($f_5$).
- **H-Minimal**: Minimal 2-feature heuristic router ($f_2 + f_3$).

---

## 3. Primary Metrics & Success Thresholds
- **Test Set Accuracy**: Accuracy on 90 held-out test tasks.
- **Net System Token Savings**: Relative to Static Full Topology.
- **Under-Activation Rate**: Complex tasks incorrectly routed to a single agent.
- **Success Criterion**: Identify the minimal feature subset that maintains $\ge 25\%$ token savings with $\le 3.0\%$ accuracy degradation.
- **Critical Feature Boundary (Escalation Threshold)**: An ablated feature is classified as strictly indispensable if its removal trips the pre-registered routing escalation threshold codified in `AS-10`, `AS-15`, and `NC-69`: accuracy degradation $> 10.0\%$ relative to Static Topology **OR** under-activation rate $> 15.0\%$.

---


## 4. Causal Claim Discipline
- `causal_claim_supported`: "Removing syntactic complexity ($f_2$) or constraint multiplicity ($f_3$) from the heuristic router causes a statistically significant degradation in routing accuracy ($> 3.0\%, p < 0.01$) relative to the full heuristic router on held-out tasks."
- `causal_claim_not_supported`: "Heuristic routing with these features is universally superior to static routing or neural routing across all unseen domains."
- `tested_context`: Multi-agent code/math queries with varying length and constraint counts, 4 specialist agent types, deterministic verification.
- `untested_context`: Continuous high-frequency real-time dialogue, open-ended conversational roleplay, dynamically expanding agent pools $> 25$.
- `interaction_risks`: Combining short query length ($f_1$) with complex multi-clause logic ($f_2$) risks under-activating specialist agents if weights are not balanced.

