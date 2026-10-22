# AS-07: SOP Component Ablation Plan
**Experiment ID**: `EXP-AB-03-FACT`  
**Target Primitive**: `PR-ORG-02` (Phased Assembly-Line SOP State Machine)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Primary Research Question
In structured collaboration workflows (ChatDev), what proportion of the observed $49.2\%$ token savings and role-violation suppression is causally attributable to semantic role prompts versus phase-gated context pruning?

---

## 2. Experimental Design ($2 \times 2$ Factorial + Boundary Controls)

All conditions evaluate $N=100$ modular and multi-file programming tasks from `SimLab-CodeSOP-150`.

```
FACTORIAL MATRIX:
                | Roles = OFF (Homogeneous) | Roles = ON (Specialized)
----------------+---------------------------+-------------------------
Phases = OFF    | C0: Unrestricted Chat     | C1: Roles Only
Phases = ON     | C2: Phases Only           | C3: Roles + Phases (Standard SOP)
```

### Detailed Condition Specifications:
- **C0 (`UNRESTRICTED_CHAT`)**: Homogeneous agents, shared conversational context, no phase gates.
- **C1 (`ROLES_ONLY`)**: Specialized persona system prompts (CEO, CTO, Programmer, Reviewer) operating in an unconstrained shared chat history.
- **C2 (`PHASES_ONLY`)**: Homogeneous agents executing sequential phase transitions (Design $\to$ Code $\to$ Test) with clean context handoffs between phases.
- **C3 (`ROLES_AND_PHASES`)**: Standard ChatDev architecture (specialized roles + phase-gated context resets).
- **C4 (`ROLES_PHASES_CRITIC`)**: C3 supplemented with an independent adversarial critic role at each phase boundary.
- **C5 (`ARTIFACT_HANDOFF_NO_CHAT`)**: Zero multi-turn dialogue. Agents communicate strictly via structured immutable file artifacts (spec.json, code.py, test.py) passed directly to the next stage.

---

## 3. Primary Metrics & Statistical Contract
- **Token Efficiency**: Total tokens consumed per completed task.
- **Unit Test Pass Rate**: Percentage of pytest assertions passing.
- **Cross-Role Violations**: Count of turns where an agent assumes or executes another role's responsibilities.
- **Statistical Method**: Two-Way ANOVA on token consumption with main effects for $\text{Roles}$ and $\text{Phases}$, plus $\text{Roles} \times \text{Phases}$ interaction term (with Kruskal-Wallis non-parametric fallback if normality fails).
- **Pre-Registered Hypothesis ($H_1$)**: The main effect of $\text{Phases}$ accounts for $\ge 70\%$ of total token variance, proving that context boundary management, rather than role prompting, drives efficiency.

---

## 4. Causal Claim Discipline
- `causal_claim_supported`: "Sequential phase gating with context boundary resets causally accounts for the primary reduction ($\ge 70\%$) in token consumption and cross-role violations relative to unrestricted multi-turn dialogue on the evaluated code tasks."
- `causal_claim_not_supported`: "Assembly-line SOP structures and persona prompting are universally optimal across all software development or multi-agent tasks."
- `tested_context`: Modular Python programming tasks ($\le 250$ LOC), 4 distinct roles (CEO, CTO, Coder, Tester), sequential waterfall phase transitions.
- `untested_context`: Highly interdependent circular refactoring, real-time UI/UX design, emergent multi-agent social interactions.
- `interaction_risks`: Overly rigid phase boundaries prevent downstream feedback from correcting upstream architectural design bugs without costly rollback loops.

