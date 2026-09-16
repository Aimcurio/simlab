# AS-05: Multi-Agent Information-Asymmetry Plan
**Experiment IDs**: `EXP-AB-02-REP` (Confirmatory Replication) & `EXP-AB-02-ASYM` (Asymmetry Sweep)  
**Target Primitive**: `PR-ORG-01` (Multi-Agent Iterative Debate & Cross-Examination)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Confirmatory Private-Information Replication (`EXP-AB-02-REP`)

### Background & Statistical Power Justification:
In Phase 3, 3-agent debate achieved an observed accuracy of $87.0\%$ vs $73.0\%$ for compute-matched $B1-SC\text{-tokens}$ ($+14.0\%$ advantage, McNemar $p = 0.0192$). Because $p = 0.0192 > 0.01$, the result missed the pre-registered significance threshold.
- **Power Calculation for Replication**:
  - Null hypothesis: $p_{\text{debate}} \le p_{B1-SC}$.
  - Expected true accuracy: $p_1 = 0.87, p_2 = 0.73$ ($\Delta = 0.14$).
  - Estimated proportion of discordant pairs: $p_{\text{disc}} \approx 0.40$.
  - Desired significance level: $\alpha = 0.01$ (strictly preserved, two-sided).
  - Desired statistical power: $1 - \beta = 0.90$.
  - **Required Sample Size**: $N = 270$ problem instances ($810$ total episodes across conditions).
- **Execution Protocol**:
  - Pinned model checkpoint: `gpt-4o-mini-2024-07-18`.
  - Token-matched control: $B1-SC\text{-tokens}$ matched within $\pm 10\%$ total tokens.
  - Success Criterion: Debate accuracy exceeds $B1-SC\text{-tokens}$ by $\ge +10.0\%$ with **$p < 0.01$**.
  - Output Decision: Exactly one of **`CONFIRMED_EFFECT`** or **`NOT_CONFIRMED`**.

---

## 2. Information Asymmetry Parametric Sweep (`EXP-AB-02-ASYM`)

### Primary Research Question:
At what degree of information partitioning does multi-agent coordination produce a statistically significant collaborative surplus over compute-matched single-agent prompting?

### Experimental Design:
Evaluate $N=150$ problem instances across 5 discrete levels of private information sharing:
- **Level 0 (0% Asymmetry / Full Sharing)**: All 3 agents receive 100% of all task clues simultaneously (homogeneous observation).
- **Level 1 (25% Asymmetry)**: Agents share 75% of clues; each holds 25% disjoint private clues.
- **Level 2 (50% Asymmetry)**: Agents share 50% of clues; 50% partitioned.
- **Level 3 (75% Asymmetry)**: Agents share 25% of clues; 75% partitioned.
- **Level 4 (100% Asymmetry / Full Partitioning)**: Zero shared clues; all evidence disjointly distributed.

### Dependent Variables & Phase Transition Analysis:
- **Net Accuracy Surplus**: $\Delta \text{Acc} = \text{Acc}_{\text{Debate}} - \text{Acc}_{B1-SC\text{-tokens}}$.
- **Communication Cost Ratio**: Total debate tokens divided by $B1$ base tokens.
- **False Consensus Rate**: Frequency of agents abandoning correct private knowledge to agree with incorrect peers.
- **Phase Transition Detection**: Identify the critical asymmetry threshold $A^* \in [0\%, 100\%]$ where $\Delta \text{Acc}$ crosses zero and becomes positive with $p < 0.01$.
