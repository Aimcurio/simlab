# AS-10: Routing Stress Plan
**Experiment ID**: `EXP-ST-04-SHIFT`  
**Target Primitive**: `PR-ORG-03`  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Primary Research Question
Under what degree of task-distribution shift, pool growth, and adversarial deception does heuristic routing break down, and does this breakdown satisfy the pre-registered threshold required to justify escalating to an LLM router?

---

## 2. Progressive Stress Dimensions

1. **Task Distribution Shift**:
   - In-Distribution: Coding and math tasks formatted identically to training data.
   - Mild Shift: Alternative prompt phrasings and conversational framing.
   - Severe Shift: Unseen task domains (e.g. legal reasoning, medical diagnosis, creative writing).
2. **Adversarial Prompting (Deception Attacks)**:
   - **Concise Complexity**: High-complexity mathematical puzzles phrased in $< 15$ words (attempts to trick length-sensitive heuristics).
   - **Verbose Simplicity**: Trivial string operations wrapped in 500 words of conversational boilerplate.
3. **Agent Pool Scaling**:
   - Routing across candidate agent pools of size $N_{\text{pool}} \in \{4, 8, 16, 25\}$.
4. **Agent Dropout & Degradation**:
   - High-capability specialist agents intermittently unavailable (tests fallback routing).

---

## 3. Complexity Escalation Rule Trigger Check
In accordance with `NC-50` and `NC-59`:
- **Escalation Trigger**: `LLM_ROUTER` or `LEARNED_PUPPETEER_ROUTING` may **ONLY** be executed if:
  1. Heuristic routing accuracy drops $> 10.0\%$ below Static Topology on the stress suite ($p < 0.01$); **AND**
  2. Under-activation rate exceeds $15.0\%$.
- If heuristic routing maintains accuracy within $10\%$ under stress, escalation remains **`BLOCKED`** under the Complexity Burden Rule.
