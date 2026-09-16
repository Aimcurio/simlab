# Handoff Report: Phase 2 Challenger 2 — Adversarial Stress-Test of RP-03, RP-04, RD-11, and RD-13

**Agent Identity**: Phase 2 Challenger 2 (`teamwork_preview_challenger`)  
**Working Directory**: `E:\projects\simlab\.agents\phase2_challenger_2`  
**Parent Agent**: `ad8aab38-3a5a-4df9-ba8c-eadca41edcc6` (parent)  
**Lifecycle State**: `REPRODUCTION_DESIGN` (Phase 2)  
**Timestamp**: 2026-09-16T09:44:00Z  

---

## Executive Verdict

### **VERDICT: REQUEST_CHANGES**

**Overall Risk Assessment**: **HIGH**

While the reproduction design package (`RD-01` through `RD-16`) demonstrates exceptional ambition and structural rigor, adversarial stress-testing reveals **critical statistical power deficits, construct validity failures, threshold loopholes, and isolation vulnerabilities** across `RD-07` (RP-03), `RD-08` (RP-04), `RD-11` (Failure Register), and `RD-13` (Execution Isolation Plan). Advancing to `READY_FOR_REPRODUCTION_EXECUTION` without addressing these flaws would produce invalid, unreplicable, or false-positive experimental outcomes.

---

## 1. Observation

Direct empirical observations, verbatim text citations, and local script verification outputs:

### 1.1 RP-03 (RD-07: Phase Boundaries & ChatDev SOPs)
1. **Sample Size & Falsification Thresholds**:
   - `RD-07:69-72`: "$N = 50$ distinct programming tasks $\times$ 3 conditions = 150 experimental runs."
   - `RD-07:80-81`: "Equal or higher unit test pass rate ($\Delta \text{Pass} \ge 0\%$)".
   - `RD-07:85`: "failure_threshold: Token reduction $< 10\%$, or `T-PhaseSOP` test pass rate is $> 10\%$ worse than `Control B` due to inability to iterate backwards across phase boundaries."
   - `RD-09:42`: "All experiments must achieve a minimum statistical power of $1 - \beta = 0.80$ at significance level $\alpha = 0.01$."
2. **Empirical Power Test for RP-03 McNemar Test ($N=50, \alpha=0.01$)**:
   - Executed via `scipy.stats` in local Python verification harness:
     - For $\Delta = 0.05$ (5% drop in pass rate), discordant pairs $n_d = 10$: $\text{Power} = \mathbf{0.0091}$ ($< 1\%$).
     - For $\Delta = 0.10$ (10% drop in pass rate), discordant pairs $n_d = 10$: $\text{Power} = \mathbf{0.0563}$ ($5.6\%$).
     - For $\Delta = 0.10$, discordant pairs $n_d = 15$: $\text{Power} = \mathbf{0.0794}$ ($7.9\%$).
     - For $\Delta = 0.15$ (15% drop in pass rate), discordant pairs $n_d = 10$: $\text{Power} = \mathbf{0.2631}$ ($26.3\%$).
   - *Observation*: At $N=50$, the probability of committing a Type II error (failing to detect a 10% drop in pass rate) is **$> 92\%$**.
3. **Task Suite Misalignment**:
   - `RD-07:69`: "`SimLab-CodeSOP-50`: A benchmark of 50 standalone Python programming specifications with deterministic unit test suites (derived from HumanEval and MBPP subsets requiring multi-step design and test writing)."
   - `RD-07:36`: Treatment deploys 4 corporate roles: Phase 1 (Demand Analysis, CEO) $\to$ Phase 2 (Architecture Design, CTO) $\to$ Phase 3 (Code Implementation, Programmer) $\to$ Phase 4 (Code Review & Testing, Reviewer).
   - HumanEval and MBPP problems are 5-to-20 line standalone algorithmic functions with a single function signature.
4. **Conflated Timeout Metrics**:
   - `RD-07:47`: "Deadlock / Timeout Rate: Tasks terminating due to maximum turn exhaustion without a final artifact."
   - `RD-13:35`: "Code Execution Sandbox: Tasks requiring dynamic code execution... run within an isolated sub-container with CPU, memory, and timeout limits (10s CPU limit, 512MB RAM, zero network interface)."
   - Neither document specifies how a 10s container timeout (e.g. from generated `while True:`) is distinguished from an LLM turn-limit deadlock (16 turns).

### 1.2 RP-04 (RD-08: Dynamic Orchestration & Puppeteer RL Policy)
1. **Sample Size & Degradation Thresholds**:
   - `RD-08:75-76`: "$N = 100$ tasks $\times$ 4 conditions = 400 experimental runs."
   - `RD-08:23`: "routing errors reduce overall task success rate by $\ge 8\%$ compared to the fixed topology baseline `B3`."
   - `RD-08:85`: "Overall accuracy degradation $\le 3\%$ compared to `B3`."
   - `RD-08:70-73`: `SimLab-HeteroBench-100` split into 40 Simple, 30 Moderate, 30 Complex tasks.
2. **Empirical Power Test for RP-04 Proportions ($N=100, \alpha=0.01$)**:
   - Executed via `scipy.stats` in local Python verification harness:
     - For $\Delta = 0.03$ (3% degradation), baseline $p_1 = 0.85$: $\text{Power} = \mathbf{0.0232}$ ($2.3\%$).
     - For $\Delta = 0.05$ (5% degradation): $\text{Power} = \mathbf{0.0498}$ ($5.0\%$).
     - For $\Delta = 0.08$ (8% degradation, the null threshold): $\text{Power} = \mathbf{0.1272}$ ($12.7\%$).
     - For $\Delta = 0.10$ (10% degradation): $\text{Power} = \mathbf{0.2077}$ ($20.8\%$).
   - Complex task stratum ($n = 30$, $\alpha = 0.05$):
     - For $\Delta = 0.15$ (15% drop on complex tasks): $\text{Power} = \mathbf{0.2216}$ ($22.2\%$).
   - *Observation*: EXP-RP04 has an $87.3\%$ Type II error rate against its own null hypothesis threshold ($\Delta = 0.08$).
3. **Missing Compute-Matched Single-Agent Control**:
   - `RD-08:31-34`: Compares only against `Baseline B3 (Fixed Full Topology)` and `Baseline B0-Heuristic (Rule Router)`.
   - `RD-04:18, 30-34`: Mandates `B1-SC` compute-matched control for all multi-agent claims. `B1-SC` is omitted from `RD-08`.
4. **Budget & Call Count Discrepancy**:
   - `RD-12:19`: EXP-RP04 modeled as "Avg Calls per Episode: 3 | Total Inference Calls: 1,200 | Total Token Volume: 1,200,000".
   - Condition 1 (`B3`) requires 4 calls per episode $\times$ 100 = 400 calls.
   - Condition 3 (`T1`) requires 1 router call + (1 to 4 worker calls) = 320 calls.
   - Condition 4 (`T2`, `ChatDev:puppeteer`) evaluates intermediate artifacts dynamically across 4 phases, requiring 4 to 8 calls per task = 500+ calls.
   - Actual required calls exceed 1,440 calls ($> 20\%$ above modeled 1,200).

### 1.3 RD-11 (Failure and Confound Register)
1. **FM-05 (Routing Collapse)**:
   - `RD-11:18`: "Class imbalance in router outputs ($> 85\%$ of tasks sent to one path)".
   - Ground truth in `SimLab-HeteroBench-100` is 40% Simple, 30% Moderate, 30% Complex.
   - Local statistical test: A router sending 84% to SOLO has $\chi^2 = 80.67$ ($p = 3.04 \times 10^{-18}$) against expected counts $(40, 30, 30)$, but does NOT trigger FM-05 because $84\% \le 85\%$. Even a 65% SOLO collapse has $\chi^2 = 26.46$ ($p = 1.80 \times 10^{-6}$) and escapes detection.
2. **FM-09 (Unbalanced Compute)**:
   - `RD-11:22`: "Token ratio $\text{Tok}_{MA} / \text{Tok}_{control} > 1.20$".
   - `RD-04:32-33`: Mandates compute matching within $\pm 10\%$ ($0.90 \le \text{ratio} \le 1.10$).
   - FM-09 permits a 20% disparity, allows reverse disparity ($\text{ratio} < 0.90$) without limit, and is omitted for RP-03 and RP-04.
3. **FM-07 (Prompt Leakage / Inversion)**:
   - `RD-11:20`: Lists vulnerable experiments as "RP-01, RP-02" only, omitting RP-03 and RP-04.
   - Trigger: "Exact-match test accuracy jumps to 100% with zero reasoning steps".
4. **FM-11 (Evaluator Bias)**:
   - `RD-11:24`: Trigger is "Length-bias correlation $r > 0.60$ between word count and judge score".
   - At $N = 100$, an $r = 0.50$ explains $25\%$ of judge variance and has $t = 5.72, p = 1.18 \times 10^{-7}$, but fails to trigger FM-11.
5. **Section 2 Abort Criteria**:
   - `RD-11:30`: Mandates batch invalidation ONLY if $> 3$ instances of FM-06 or FM-09 occur. Repeated instances of FM-01, FM-05, FM-07, or FM-10 do not invalidate a batch.

### 1.4 RD-13 (Execution Isolation Plan)
1. **Container Breakout Vulnerability in Sub-Container Architecture**:
   - `RD-13:16, 35`: Specifies a "rootless container" spawning an "isolated sub-container with CPU, memory, and timeout limits".
   - Spawning a nested container inside rootless OCI requires either mounting `/var/run/docker.sock` (which gives host root privilege) or `--privileged` DinD, destroying host containment.
2. **Commercial API Data Retention**:
   - `RD-13:28-30`: Whitelists `api.openai.com` and `generativelanguage.googleapis.com` without mandating Zero Data Retention (`store: false`) or data-opt-out headers.

---

## 2. Logic Chain

Step-by-step adversarial reasoning from direct observations to conclusions:

```
[Obs 1.1.1, 1.1.2] $N=50$ gives McNemar power < 8% for 10% pass rate drop
  --> [Inference 1] Rigid phase gates could cause severe regression bugs that go undetected 92% of the time
  --> [Conclusion 1] RP-03 cannot validly claim "equal or superior pass rates" under its current sample size.

[Obs 1.1.3] SimLab-CodeSOP-50 uses 10-20 line HumanEval/MBPP functions
  --> [Inference 2] 4 corporate roles (CEO, CTO, Coder, Reviewer) on a 1-function task is an artificial construct
  --> [Inference 3] CEO/CTO prompts add pure coordination noise without testing real architectural phase handoffs
  --> [Conclusion 2] RP-03 suffers from severe construct validity failure and benchmark ceiling effects.

[Obs 1.2.1, 1.2.2] $N=100$ gives proportion test power of 12.7% for 8% accuracy drop
  --> [Inference 4] Null hypothesis threshold (8% drop) will almost never be rejected
  --> [Conclusion 3] RP-04 has near-zero sensitivity to routing misclassifications and under-activations.

[Obs 1.2.3] RD-08 compares dynamic routing only to fixed waterfall B3, omitting B1-SC
  --> [Inference 5] Full 4-agent waterfall on 1-line regex tasks is a manufactured strawman
  --> [Inference 6] Single-agent B1 or B1-SC could achieve lower token spend and equal accuracy
  --> [Conclusion 4] RP-04 claims of token efficiency are confounded by baseline selection.

[Obs 1.3.1] FM-05 uses > 85% single-class trigger, but 84% SOLO has chi^2 = 80.67 (p = 3e-18)
  --> [Inference 7] Severe routing collapse will pass undetected as normal execution
  --> [Conclusion 5] FM-05 detection threshold is scientifically indefensible.

[Obs 1.3.2, 1.3.5] FM-09 trigger allows 20% disparity vs 10% contract; Section 2 aborts only on FM-06/09
  --> [Inference 8] Experiments violating compute parity or suffering massive prompt leakage remain valid
  --> [Conclusion 6] RD-11 provides false assurance while allowing compromised batches to advance.

[Obs 1.4.1] Sub-container execution inside rootless container requires docker.sock or privileged DinD
  --> [Inference 9] Host isolation is compromised or execution will fail during Phase 3 implementation
  --> [Conclusion 7] RD-13 contains an unviable container architecture.
```

---

## 3. Adversarial Challenges (Detailed Threat Matrix)

### [CRITICAL] Challenge 1: Severe Statistical Power Deficit in RP-03 and RP-04
- **Assumption Challenged**: That $N=50$ (RP-03) and $N=100$ (RP-04) satisfy `RD-09`'s statistical standard ($1-\beta \ge 0.80$ at $\alpha=0.01$).
- **Attack Scenario**: 
  - In RP-03, rigid phase boundaries prevent the Programmer and Reviewer from resolving back-and-forth edge cases, causing a real 10% drop in unit test pass rates ($p_1 = 0.85 \to p_2 = 0.75$). Because McNemar's test power is only $5.6\%$, the experiment yields $p > 0.05$. The researchers claim "SOP phase boundaries maintain pass rate parity while saving tokens," publishing a Type II false negative.
  - In RP-04, the LLM router misclassifies complex tasks as simple, causing an 8% accuracy drop. With power of only $12.7\%$, the failure threshold is never triggered.
- **Blast Radius**: Erroneous architectural adoption of rigid phase machines or fragile routing policies in SimLab.
- **Mitigation**:
  - For RP-03: Expand sample size to at least **$N = 250$ tasks**, or reformulate the primary metric as continuous test assertion pass percentage evaluated via paired Wilcoxon signed-rank test.
  - For RP-04: Expand sample size to at least **$N = 300$ tasks** ($100$ per complexity tier) or apply a non-inferiority TOST framework with equivalence margin $\delta = 0.05$.

### [HIGH] Challenge 2: Construct Validity Failure in RP-03 Task Benchmark
- **Assumption Challenged**: That `SimLab-CodeSOP-50` (derived from HumanEval/MBPP) is representative of multi-agent software engineering workflows.
- **Attack Scenario**: A CEO agent is asked to perform "Demand Analysis" for `def has_close_elements(numbers: List[float], threshold: float) -> bool:`. The CEO and CTO spend 800 tokens rephrasing the 2-sentence prompt. In the unrestricted baseline (`Control B`), the CEO and Programmer engage in verbose conversational chat about a 5-line loop. In `T-PhaseSOP`, the phase artifact truncates this chat. The token savings observed in `T-PhaseSOP` is entirely an artifact of avoiding absurd corporate role chatter on trivial algorithms, NOT evidence that phase gates improve real software engineering.
- **Blast Radius**: Results cannot generalize to repository-level software development or agent simulations.
- **Mitigation**: Replace HumanEval/MBPP with a curated multi-file benchmark suite requiring real architectural design: **SWE-bench Lite (curated 50-task mini subset)** or multi-file Python packages where architecture and interface boundaries are genuine artifacts.

### [HIGH] Challenge 3: Manufactured Strawman & Missing B1-SC Control in RP-04
- **Assumption Challenged**: That comparing dynamic routing against a fixed 4-agent waterfall (`B3`) proves architectural superiority.
- **Attack Scenario**: On 40 simple tasks, a single agent (`B1` with greedy decoding or `B1-SC` with 3 samples) solves the tasks using 300–800 tokens with 100% accuracy. `T-LLMRouter` uses 150 router tokens + 450 agent tokens = 600 tokens. On complex tasks, `B1-SC` spends 2,400 tokens and matches the accuracy of `T-LLMRouter`. Across the entire benchmark, `B1-SC` beats both `B3` and `T-LLMRouter` in Pareto efficiency. By omitting `B1-SC`, the experiment conceals that multi-agent routing is inferior to a compute-matched single model.
- **Blast Radius**: Violation of Directive R4, RD-04, and NC-05; false attribution of gains to multi-agent routing.
- **Mitigation**: Mandate **`Baseline B1-SC` (Compute-Matched Single Agent)** as a mandatory control in `RD-08`.

### [HIGH] Challenge 4: FM-05 and FM-09 Detection Threshold Loopholes in RD-11
- **Assumption Challenged**: That FM-05 ($> 85\%$ class imbalance) and FM-09 ($> 1.20$ token ratio) reliably detect experimental invalidity.
- **Attack Scenario**: 
  - A biased router routes 84% of tasks to `SOLO`, causing 44 out of 60 moderate/complex tasks to fail. Because $84\% \le 85\%$, FM-05 does not fire, and the failure is logged as ordinary experimental variance.
  - A multi-agent treatment receives 19% more tokens than the control ($1.19\times$). Even though `RD-04` mandates parity within $\pm 10\%$, FM-09 does not fire ($1.19 \le 1.20$), and the experiment is declared valid.
  - An experiment experiences 15 instances of FM-07 (Prompt Leakage). Because Section 2 only aborts on FM-06 and FM-09, the corrupted run is accepted as valid.
- **Blast Radius**: Acceptance of corrupted data, invalidating SimLab empirical findings.
- **Mitigation**:
  - Replace FM-05 threshold with a **Chi-Square Goodness-of-Fit test** ($\chi^2 > 13.82, df=2, p < 0.001$).
  - Tighten FM-09 to a two-sided test: $|\text{Tok}_{MA} / \text{Tok}_{control} - 1.0| > 0.10$.
  - Update Section 2 Abort Criteria to invalidate batches triggering $> 0$ instances of FM-07 (zero tolerance for prompt leakage) or $> 3$ instances of ANY registered failure mode.

### [HIGH] Challenge 5: Docker Socket Security & Sub-Container Execution in RD-13
- **Assumption Challenged**: That an "isolated sub-container" can be spawned securely inside a rootless container.
- **Attack Scenario**: During Phase 3 execution, the harness attempts to spawn a nested Docker container to run generated Python unit tests. To enable this, the developer mounts `/var/run/docker.sock` into the container. Untrusted Python code generated by `gpt-4o` (or an adversarial prompt injection) executes a command communicating with the Docker socket, escaping the container to execute arbitrary commands as `root` on the host machine.
- **Blast Radius**: Host machine compromise, security boundary failure.
- **Mitigation**: Replace nested Docker sub-containers with in-container process sandboxing using **Linux user namespaces and cgroups** (e.g., `nsjail` or `bubblewrap` with seccomp-bpf, `RLIMIT_CPU=10s`, `RLIMIT_AS=512MB`, and dropped network capabilities).

### [MEDIUM] Challenge 6: Commercial API Benchmark Leakage in RD-13
- **Assumption Challenged**: That network egress filtering alone prevents benchmark leakage.
- **Attack Scenario**: Live evaluation requests containing benchmark tasks and ground-truth unit tests are sent to `api.openai.com`. Without explicit zero-data-retention headers (`store: false`), OpenAI logs the prompts for model retraining. In future model releases, the benchmark is contaminated.
- **Blast Radius**: Permanent benchmark obsolescence.
- **Mitigation**: Mandate `store: false` parameter in all API calls and verify enterprise Zero Data Retention (ZDR) status in `RD-13`.

---

## 4. Stress Test Results Summary

| Scenario / Test | Target Component | Expected Robust Behavior | Observed / Predicted Actual Behavior | Pass / Fail |
|---|---|---|---|---|
| **RP-03 McNemar Power ($\Delta=0.10, N=50$)** | `RD-07` | Statistical Power $\ge 0.80$ at $\alpha=0.01$ | Power $= \mathbf{0.0794}$ (Type II error $> 92\%$) | **FAIL** |
| **RP-03 Paired Token Power ($d=0.30, N=50$)** | `RD-07` | Statistical Power $\ge 0.80$ at $\alpha=0.01$ | Power $= \mathbf{0.2995}$ (Type II error $> 70\%$) | **FAIL** |
| **RP-04 Proportion Power ($\Delta=0.08, N=100$)** | `RD-08` | Statistical Power $\ge 0.80$ at $\alpha=0.01$ | Power $= \mathbf{0.1272}$ (Type II error $> 87\%$) | **FAIL** |
| **RP-04 Complex Stratum Power ($\Delta=0.15, N=30$)**| `RD-08` | Statistical Power $\ge 0.80$ at $\alpha=0.05$ | Power $= \mathbf{0.2216}$ (Type II error $> 77\%$) | **FAIL** |
| **FM-05 Chi-Square Test (84% SOLO Collapse)** | `RD-11` | Detection trigger fires on severe collapse | Trigger fails to fire ($84\% \le 85\%$; $\chi^2=80.67$) | **FAIL** |
| **FM-09 Compute Parity Assertion (1.19x ratio)** | `RD-11` | Flag violation of $\pm 10\%$ parity | Trigger fails to fire ($1.19 \le 1.20$) | **FAIL** |
| **FM-11 Evaluator Correlation ($r=0.50, N=100$)** | `RD-11` | Flag large evaluator length bias | Trigger fails to fire ($0.50 \le 0.60; p = 1.18 \times 10^{-7}$)| **FAIL** |
| **Nested Sandbox Spawning** | `RD-13` | Hermetic rootless isolation | Requires docker.sock or privileged DinD | **FAIL** |

---

## 5. Unchallenged Areas

The following components were inspected and found to be methodologically sound, requiring no modifications:
1. **RP-01 & RP-02 Experimental Architecture**: `RD-05` and `RD-06` exhibit rigorous controls, well-calibrated metrics (MRR/NDCG and GSM8K exact match), and appropriate baseline compute matching.
2. **Deterministic-First Measurement Philosophy (`RD-09`)**: The four-level measurement hierarchy correctly demotes subjective LLM judges to auxiliary status.
3. **Telemetry & Provenance Contract (`RD-10`)**: Unified JSONL schema and SHA-256 recording satisfy strict provenance requirements.
4. **Hard Resource Expenditure Ceiling (`RD-12`)**: The $100.00 hard financial cap and exponential backoff throttle provide adequate resource safety.

---

## 6. Caveats

1. **Analytical & Mathematical Scope**: Power calculations assume standard normal/binomial asymptotic distributions and McNemar discordant pair distributions. If unit test pass rate in RP-03 is measured as a continuous percentage of assertions passed rather than a binary pass/fail per task, a paired Wilcoxon signed-rank test will achieve higher power for medium effect sizes ($d \ge 0.50$), but still falls short for subtle degradations ($d \le 0.30$).
2. **Heuristic Simplicity**: We did not evaluate whether an untuned regex heuristic could match an LLM router on novel unseen domains; the challenge is bounded to the 100 tasks of `SimLab-HeteroBench-100`.
3. **Execution Prohibition**: In strict compliance with Governance Directive R6 and `ORIGINAL_REQUEST.md`, no benchmark code, agent execution, or API calls were performed. All stress tests were conducted via theoretical threat modeling and mathematical/statistical simulation.

---

## 7. Conclusion & Required Modifications

Advancing Gate R2 to `READY_FOR_REPRODUCTION_EXECUTION` is premature. The following **mandatory modifications** must be completed before Gate R2 can be approved:

### Actionable Remediation Items:
1. **Remediate RP-03 (`RD-07`)**:
   - Expand sample size from $N=50$ to at least **$N=150$ tasks**, or reformulate the primary pass metric to continuous assertion pass percentage with pre-registered non-inferiority margins.
   - Replace or augment `SimLab-CodeSOP-50` with a curated multi-file benchmark (**SWE-bench Lite mini-subset**) to evaluate genuine architectural phase handoffs.
   - Explicitly separate execution sandbox CPU/memory timeouts (10s) from agent turn-deadlock timeouts (16 turns).
2. **Remediate RP-04 (`RD-08`)**:
   - Mandate **`Baseline B1-SC` (Compute-Matched Single Agent)** as a mandatory comparison baseline.
   - Define an explicit 70/30 train/test split or held-out evaluation set for `SimLab-HeteroBench-100` to prevent router prompt overfitting.
   - Specify the recovery/escalation protocol for misrouted tasks and update `RD-12` call counts to account for multi-phase dynamic routing decisions ($1,440+$ calls).
3. **Remediate Failure Register (`RD-11`)**:
   - Replace FM-05 trigger with a **Chi-Square Goodness-of-Fit test** ($\chi^2 > 13.82, p < 0.001$).
   - Harmonize FM-09 with `RD-04`: trigger on two-sided $|\text{Tok}_{MA} / \text{Tok}_{control} - 1.0| > 0.10$, and extend FM-09 to RP-03 and RP-04.
   - Lower FM-11 correlation threshold to $r > 0.35$.
   - Register FM-07 (Prompt Leakage) for RP-03 and RP-04, and set abort threshold to zero tolerance.
   - Update Section 2 Abort Criteria to invalidate batches on $> 3$ occurrences of ANY registered failure mode.
4. **Remediate Isolation Plan (`RD-13`)**:
   - Replace nested Docker sub-containers with **Linux process-level sandboxing** (`nsjail` / `bubblewrap` with seccomp-bpf and zero network).
   - Mandate zero-data-retention (`store: false`) headers for all API requests.
   - Mandate per-episode scratch volume / tmpfs purging.

---

## 8. Verification Method

To independently verify the empirical findings and power calculations reported in this handoff:

1. **Verify RP-03 and RP-04 Statistical Power**:
   Run the following Python command in any standard Python 3.10+ environment with `scipy` and `numpy`:
   ```bash
   python -c "import scipy.stats as stats; print('RP-03 McNemar Power (d=0.10, n_d=10):', 1 - stats.binom.cdf(stats.binom.ppf(0.995, 10, 0.5), 10, 0.75) + stats.binom.cdf(stats.binom.ppf(0.005, 10, 0.5)-1, 10, 0.75))"
   ```
   *Expected output*: `Power = 0.0563`.
2. **Verify FM-05 Chi-Square Sensitivity**:
   ```bash
   python -c "import scipy.stats as stats; import numpy as np; print('Chi2 for 84% SOLO:', stats.chisquare([84, 8, 8], [40, 30, 30]))"
   ```
   *Expected output*: `Power / Chi2 = 80.67, pvalue = 3.04e-18`.
3. **Verify FM-11 Length Correlation Significance**:
   ```bash
   python -c "import scipy.stats as stats; import numpy as np; r=0.50; n=100; t=r*np.sqrt((n-2)/(1-r**2)); print('t =', t, 'p =', 2*(1-stats.t.cdf(t, n-2)))"
   ```
   *Expected output*: `t = 5.72, p = 1.18e-07`.
4. **Inspect Deliverable Source Lines**:
   - `RD-07`: Lines 69-72, 80-85.
   - `RD-08`: Lines 23, 31-34, 75-76, 85.
   - `RD-11`: Lines 18, 20, 22, 24, 30.
   - `RD-13`: Lines 16, 28-30, 35.

---
*Report certified by Phase 2 Challenger 2 (`teamwork_preview_challenger`).*
