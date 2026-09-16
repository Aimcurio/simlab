# AS-09: Routing Feature Ablation Plan
**Experiment ID**: `EXP-AB-04-FEAT`  
**Target Primitive**: `PR-ORG-03` (Dynamic Agent Routing)  
**Lifecycle State**: `PHASE_4_DESIGN`  

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
