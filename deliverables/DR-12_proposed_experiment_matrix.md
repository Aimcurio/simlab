# DR-12: Proposed Experiment Matrix & Falsifiable Research Designs

**Document Version**: 1.0.0-FINAL  
**Lifecycle State**: `RESEARCH_AUTHORIZED` (Implementation Authority: `NOT_GRANTED`)  
**Project**: Curo Deep Research Investigation — Agent Simulation Lab (SimLab)  
**Author**: `curo_worker_2` (Failures, Registers & Experiments Author)  
**Integrity Mode**: Benchmark / Adversarial Verification  
**Date**: 2026-09-15  

---

## ⚠️ MANDATORY LIFECYCLE DISCLAIMER & AUTHORITY BOUNDARY ⚠️

> **STRICT PROHIBITION — RESEARCH DESIGN ONLY — ZERO EXECUTION AUTHORIZATION**  
> In strict conformance with Curo Lifecycle State `RESEARCH_AUTHORIZED` and Governance Directive R6 (`ORIGINAL_REQUEST.md`):  
> 1. This document constitutes **theoretical experimental designs and methodological specifications only**.  
> 2. **ZERO IMPLEMENTATION OR EXECUTION AUTHORITY IS GRANTED**.  
> 3. Under NO circumstances does this deliverable authorize:  
>    - Writing or modifying simulation runtime code or agent execution scripts;  
>    - Cloning external repositories or setting up sandbox environments;  
>    - Installing system dependencies, containers, or Python virtual environments;  
>    - Invoking commercial or open-weight foundation model APIs;  
>    - Running benchmarks, pilot trials, or collecting empirical data.  
> 4. The Core Invariant holds: **RESEARCH_DESIGN != IMPLEMENTATION_AUTHORIZATION**.  
> Advancing from experimental design to live execution belongs strictly to subsequent lifecycle phases (Milestones M3–M5) and requires independent, explicit approval from the Human Requester.

---

## 1. Executive Summary & Epistemic Framework

### 1.1 Experimental Objectives
To support the future scientific program of the Agent Simulation Lab (SimLab), this deliverable specifies three rigorous, falsifiable experimental protocols:
- **EXP-001: Organizational Topology & Coordination Tax** (Comparing Hierarchical Coordinator vs. Decentralized Peer-to-Peer vs. Compute-Normalized Single-Agent Self-Consistency B1-SC).
- **EXP-002: Double-Blind Independent Critic vs. Sycophantic In-Group Review** (Evaluating reviewer isolation, AST sanitization, and vulnerability detection).
- **EXP-003: Robustness under Fault Injection: Dynamic Pruning vs. Static SOP** (Full factorial $2 \times 3$ design evaluating topological collapse under early vs. late runtime faults).

### 1.2 Methodological & Statistical Discipline
To prevent the statistical and epistemic flaws prevalent in published multi-agent literature, all three experimental designs incorporate:
1. **The Smallest Falsifying Experiment**: Formulating the minimal test capable of decisively disproving the primary hypothesis.
2. **Cluster-Aware Statistical Models**: Guarding against **pseudoreplication** (treating repeated runs on the same benchmark problem as independent samples) by utilizing **Linear Mixed-Effects Models (LMM)** with random intercepts for problem instances.
3. **Formal Statistical Power Calculations**: Exact non-central distribution calculations guaranteeing power $1 - \beta \ge 0.85$ at $\alpha = 0.05$ or $\alpha = 0.01$.
4. **Explicit Negative Boundary Statements**: Delineating what the experiment **COULD** demonstrate versus what it **COULD NOT** demonstrate, and enumerating **forbidden, non-justified conclusions**.

---

## 2. Comprehensive Experimental Designs

```
+----------------------------------------------------------------------------------------------------+
|                                    PROPOSED EXPERIMENT MATRIX                                      |
+----------------------------------------------------------------------------------------------------+
| EXP-001: Architectural Topology & Coordination Tax (Centralized vs Decentralized vs B1-SC)        |
| EXP-002: Double-Blind Independent Critic vs. Sycophantic In-Group Review                          |
| EXP-003: Robustness under Fault Injection: Dynamic Pruning (DyLAN) vs. Static SOP (MetaGPT)        |
+----------------------------------------------------------------------------------------------------+
```

---

### 2.1 Experiment EXP-001: Organizational Topology & Coordination Tax

#### A. Formal Hypothesis & TOST Equivalence Framework
Multi-agent collaborative topologies (Hierarchical Centralized Coordinator vs. Decentralized Peer-to-Peer) do not achieve a statistically significant higher Task Completion Rate ($TCR$) than a Single-Agent with Self-Consistency baseline (B1-SC) when total inference token spend is held strictly equal (demonstrating statistical non-inferiority / equivalence within margin $\delta = 0.05$), while multi-agent topologies incur a significantly higher Coordination Tax ($CT \ge 35\%$) and quadratic wall-clock latency.

**Guard against "Affirming the Null"**: In classical null-hypothesis testing, failure to reject $H_0$ ($p > 0.05$) does not prove equivalence. To prevent affirming the null, the primary performance comparison is formalized under a **Two One-Sided Tests (TOST)** non-inferiority and equivalence framework with equivalence margin $\delta = 0.05$ (5 percentage points):
$$H_{01}: TCR_{\text{multi}} - TCR_{\text{B1-SC}} \le -\delta \quad \text{vs.} \quad H_{a1}: TCR_{\text{multi}} - TCR_{\text{B1-SC}} > -\delta$$
$$H_{02}: TCR_{\text{multi}} - TCR_{\text{B1-SC}} \ge \delta \quad \text{vs.} \quad H_{a2}: TCR_{\text{multi}} - TCR_{\text{B1-SC}} < \delta$$
B1-SC non-inferiority is demonstrated if $H_{01}$ is rejected at $\alpha = 0.05$. Bidirectional equivalence is established if and only if both $H_{01}$ and $H_{02}$ are rejected (or the two-sided $90\%$ confidence interval for the difference $\Delta TCR$ falls entirely within $[-\delta, +\delta] = [-0.05, +0.05]$).

#### B. Smallest Falsifying Experiment
Evaluate three organizational conditions on a curated subset of at least **72 distinct software maintenance tasks** from SWE-bench Lite:
- **Condition 1 (B1-SC Control)**: Single LLM Agent using Chain-of-Thought, sampled $K=5$ independent times per task with temperature $T=0.7$; majority voting across unit-test passing candidate patches. Total tokens matched to Condition 2.
- **Condition 2 (B3-Hierarchical)**: Centralized Hierarchical Team (1 Project Manager / Dispatcher, 1 Software Architect, 1 Programmer, 1 Code Reviewer) communicating via structured artifact handoffs.
- **Condition 3 (B2-Decentralized)**: Decentralized Team of 4 peer agents communicating over an open publish/subscribe message bus with round-robin speaking order.
- **Sample Allocation**: At least 72 distinct tasks $\times$ 5 seeds per task = 360 runs per condition ($N_{\text{runs}} \ge 360$ per condition, $N = 1,080$ total experimental observations across the 3 conditions).

#### C. Variables & Controlled Invariants
- **Independent Variable**: Organizational Collaboration Topology (Single-Agent B1-SC, Hierarchical B3, Decentralized B2).
- **Dependent Variables**:
  1. *Task Completion Rate* ($TCR \in [0, 1]$): Deterministic binary metric; patch passes 100% of hidden regression and evaluation tests.
  2. *Total Generated Tokens* ($Tokens_{\text{total}}$): Sum of prompt and completion tokens across all inference calls.
  3. *Coordination Tax* ($CT \in [0, 1]$):
     $$CT = \frac{Tokens_{\text{inter\_agent\_communication}}}{Tokens_{\text{total}}}$$
     where communication tokens represent dialogue, routing instructions, and peer handoffs (defined as $0.0$ for B1-SC).
  4. *Wall-Clock Turn Latency* ($T_{\text{latency}}$): Elapsed seconds to final patch emission.
- **Controlled Invariants**:
  - *Identical Foundation Model*: Fixed to `gpt-4o-mini-2024-07-18` (or `claude-3-5-haiku-20241022`).
  - *Strict Token Budget Clamping*: Total tokens per task instance clamped to $B_{\text{budget}} \le 120,000$ tokens across all conditions. If an architecture exhausts $B_{\text{budget}}$ before emitting a patch, execution is halted and scored as $TCR = 0$.
  - *Identical Sandbox & Environment*: Pinned Docker container with identical Python virtual environment, git repository state, and bash execution timeout (60s).

#### D. Power Analysis & Statistical Discipline (Correcting for Binary Metric & Pseudoreplication)
- **The Clustering Confound**: Multiple runs ($S=5$) on the same task instance exhibit intra-cluster correlation. Treating repeated seeds as independent samples commits pseudoreplication and artificially inflates degrees of freedom.
- **Statistical Model**: Generalized Linear Mixed-Effects Model (GLMM) with a logit link function for binary $TCR$:
  $$\operatorname{logit}(P(TCR_{ij} = 1)) = \beta_0 + \beta_1 \cdot \text{Topology}_{ij} + u_i + \epsilon_{ij}$$
  where $u_i \sim \mathcal{N}(0, \sigma_u^2)$ is the random intercept for task instance $i \in \{1 \dots 72\}$, and $j \in \{1 \dots 5\}$ indexes the random seed.
- **Binary Metric Power Correction**: Task Completion Rate is a discrete binary proportion ($TCR \in \{0, 1\}$) with variance $\sigma^2 = p(1 - p)$. On SWE-bench Lite, baseline single-agent pass rates average $p_1 \approx 0.15$. The legacy power calculation misapplied continuous Cohen's $d$, falsely claiming $88.4\%$ power with $n_{\text{eff}} \approx 57.7$; exact calculation for two-sample proportions reveals that $n_{\text{eff}} = 57.7$ achieves only **$48.8\%$ power** (Type II error rate $> 51\%$).
- **Sample Size Derivation**: To guarantee statistical power $1 - \beta \ge 0.85$ to detect $\Delta TCR = 0.15$ ($p_1 = 0.15 \to p_2 = 0.30$) at $\alpha = 0.05$, the required effective sample size per condition is:
  $$n_{\text{eff\_required}} = \frac{\left(z_{0.975}\sqrt{2\bar{p}(1-\bar{p})} + z_{0.85}\sqrt{p_1(1-p_1) + p_2(1-p_2)}\right)^2}{\Delta^2} \approx 137.6 \text{ per condition}$$
  With intra-cluster correlation $\rho = 0.15$ across $S = 5$ random seeds, the cluster design effect is $DE = 1 + (S - 1)\rho = 1 + 4(0.15) = 1.60$.
  Expanding from 30 to at least **72 distinct SWE-bench tasks** ($N_{\text{runs}} = 72 \times 5 = 360$ runs per condition, $N = 1,080$ total) yields:
  $$n_{\text{eff}} = \frac{M \cdot S}{DE} = \frac{72 \cdot 5}{1.60} = \frac{360}{1.60} = \mathbf{225 \text{ per condition}}$$
  With $n_{\text{eff}} = 225$, true power exceeds **$95\%$** ($1 - \beta \ge 0.95$). Even under an extreme conservative clustering assumption of $\rho = 0.40$ ($DE = 2.60$), $n_{\text{eff}} = 360 / 2.60 = 138.5 \ge 137.6$, strictly guaranteeing true power **$\ge 85\%$**.

#### E. What the Experiment COULD and COULD NOT Demonstrate
- **Could Demonstrate**:
  - Whether decomposing code maintenance into multiple communicating agents yields any problem-solving benefit over compute-matched stochastic sampling from a single model.
  - The precise empirical coordination tax levied by multi-agent communication on complex tasks.
- **Could NOT Demonstrate**:
  - The absolute ceiling of multi-agent capabilities under infinite compute.
  - Performance on tasks requiring genuine physical/digital concurrency or distributed private data.
- **Explicit Non-Justified Conclusions**:
  - *Forbidden Conclusion 1*: "Multi-agent systems are inherently useless for software engineering." (The experiment evaluates homogeneous models on SWE-bench Lite; it does not evaluate heterogeneous frontier ensembles with specialized tools).
  - *Forbidden Conclusion 2*: "Centralized coordination is universally superior to decentralized collaboration." (Result is bounded to software bug localization).
- **External Validity Limitations**: Bounded to Python code maintenance; results do not generalize to open-ended creative writing or social dilemma simulations.
- **Unresolved Confounds**: Differences in system prompt phrasing between single-agent ReAct and multi-agent roles cannot be perfectly normalized without altering role semantics.

---

### 2.2 Experiment EXP-002: Double-Blind Independent Critic vs. Sycophantic In-Group Review

#### A. Formal Hypothesis
A double-blind, AST-sanitized independent critic architecture (Layer G) achieves a significantly lower Vulnerability Escape Rate ($VER$) and higher Residual Independence ($CIM_{\text{residual}}$) than a conversational, in-group peer review loop (ChatDev/AgentVerse style), which suffers from sycophantic consensus collapse when reviewing security-sensitive code.

#### B. Smallest Falsifying Experiment
Evaluate three review architectures on at least **56 distinct software patch tasks** seeded with subtle, realistic security vulnerabilities (CWE-89 SQL Injection, CWE-79 Cross-Site Scripting, CWE-22 Path Traversal):
- **Condition 1 (No Review Baseline)**: Builder Agent generates patch and immediately deploys (B1 single agent).
- **Condition 2 (Conversational In-Group Review)**: Builder Agent and Reviewer Agent share the same multi-turn chat context. The reviewer reviews the patch and engages in dialogue with the builder.
- **Condition 3 (Double-Blind Independent Critic - Layer G)**: Builder Agent submits patch. The harness strips author metadata, normalizes the AST, removes comments/docstrings (preventing prompt hijacking), and passes the sanitized diff to an isolated critic with zero shared memory.
- **Sample Allocation**: At least 56 distinct security tasks $\times$ 5 seeds = 280 matched blocks ($N_{\text{blocks}} \ge 279$). Total experimental runs $= 280 \times 3 = 840$ total runs (280 runs per condition).

#### C. Variables & Controlled Invariants
- **Independent Variable**: Reviewer Isolation Architecture (No Review, In-Group Conversational, Double-Blind Independent).
- **Dependent Variables**:
  1. *Vulnerability Escape Rate* ($VER \in [0, 1]$):
     $$VER = \frac{\text{Vulnerabilities Merged to Master}}{\text{Total Ground-Truth Vulnerabilities Present}}$$
  2. *Reviewer Catch Rate* ($RCR = 1.0 - VER$).
  3. *False Positive Rejection Rate* ($FPR \in [0, 1]$): Benign code flagged as vulnerable.
  4. *Residual Critic Independence Metric* ($CIM_{\text{residual}}$):
     $$CIM_{\text{residual}} = 1.0 - |\rho(V_c - Y, V_b - Y)|$$
     measuring the independence of critic errors $V_c - Y$ from builder errors $V_b - Y$ given ground truth $Y \in \{0, 1\}$.
- **Controlled Invariants**:
  - Identical Builder model (`gpt-4o-mini`) and Critic model (`gpt-4o-mini`).
  - Identical security review prompt guidelines (CWE detection checklist).
  - Pinned seeds for code generation and review.

#### D. Power Analysis & Statistical Discipline (Correcting Matched Block Parameter in Cochran's Q Test)
- **Statistical Test**: Cochran's Q test (for paired binary vulnerability detection across $k = 3$ matched conditions) and McNemar's test for post-hoc pairwise condition comparisons.
- **Cochran's Q Test Sample Size & Non-Centrality Parameter**:
  In Cochran's Q test evaluating $k$ repeated binary treatments, degrees of freedom depend strictly on treatment levels: $df = k - 1 = 3 - 1 = 2$.
  Crucially, the sample size parameter entering the non-centrality parameter $\lambda = N \cdot w^2$ of the asymptotic non-central $\chi^2$ distribution represents the number of **matched blocks** ($N_{\text{blocks}}$), NOT the total count of individual cell entries ($N_{\text{blocks}} \times k$).
  In the legacy design ($30 \text{ tasks} \times 5 \text{ seeds} = 150 \text{ matched blocks}$), substituting $N_{\text{blocks}} = 150$ into the non-central $\chi^2$ distribution for medium effect size $w = 0.25$ and stringent significance level $\alpha = 0.01$ reveals:
  $$\lambda = N_{\text{blocks}} \cdot w^2 = 150 \cdot (0.25)^2 = 9.375$$
  $$\chi^2_{\text{crit}}(0.99, df=2) = 9.2103$$
  $$\text{Power} = 1 - F_{\text{ncx2}}(9.2103, df=2, \lambda=9.375) = \mathbf{0.5770} \quad (\mathbf{57.7\%})$$
  The legacy claim of $>0.99$ power was an artifact of conflating total cell runs ($450$) with matched blocks ($150$). If task clustering is fully collapsed to $N = 30$ tasks, power drops to an unacceptable $7.8\%$.
- **Corrected Sample Size Derivation**:
  To achieve power $\ge 80\%$ (and target $90\%$) under $\alpha = 0.01$ and $w = 0.25$:
  - Achieving $80\%$ power requires $N_{\text{blocks}} \ge 232$ ($\lambda = 14.50$, power $= 0.812$).
  - Achieving $90\%$ power requires $N_{\text{blocks}} \ge 279$ ($\lambda = 17.4375$, power $= 0.902$).
  Therefore, EXP-002 expands from 30 to at least **56 distinct security vulnerability tasks** evaluated across 5 random seeds:
  $$N_{\text{blocks}} = 56 \times 5 = \mathbf{280 \ge 279 \text{ matched blocks}}$$
  This generates $280 \times 3 = 840$ total runs, guaranteeing statistical power of **$1 - \beta = 0.903 > 0.90$** (and strictly $> 80\%$) at $\alpha = 0.01$.

#### E. What the Experiment COULD and COULD NOT Demonstrate
- **Could Demonstrate**:
  - Whether context isolation and AST comment-stripping prevent sycophantic peer collusion and prompt injection attacks during code review.
  - The empirical validity of the corrected $CIM_{\text{residual}}$ metric over the broken unconditional $CIM$ formula.
- **Could NOT Demonstrate**:
  - Whether an LLM critic can detect novel zero-day cryptographic vulnerabilities outside its pre-training data.
- **Explicit Non-Justified Conclusions**:
  - *Forbidden Conclusion 1*: "Independent LLM critics completely eliminate software vulnerabilities." (LLM critics have non-zero false negative rates on novel logic bugs).
  - *Forbidden Conclusion 2*: "Stripping comments never harms code review." (Comment stripping eliminates adversarial prompt injections, but may obscure legitimate algorithmic documentation, slightly inflating $FPR$).
- **External Validity Limitations**: Bounded to web/database vulnerabilities (CWE-89, 79, 22); may not generalize to concurrent race conditions or hardware-level memory safety.
- **Unresolved Confounds**: In-group reviewers consume more tokens due to conversation; token spend is not equalized between Condition 2 and Condition 3 (Condition 3 is strictly cheaper).

---

### 2.3 Experiment EXP-003: Robustness under Fault Injection: Dynamic Pruning vs. Static SOP

#### A. Formal Hypothesis
Dynamic agent pruning frameworks (DyLAN / Evolving Orchestration) exhibit catastrophic failure (topological collapse, FM-10) under late-stage runtime fault injection compared to static SOP pipelines (MetaGPT), because unsupervised dynamic heuristics prematurely prune inactive verification specialists during early workflow phases.

#### B. Smallest Falsifying Experiment
A full factorial $2 \times 3$ experimental design evaluating two multi-agent architectures across three fault injection schedules:
- **Factor A (Architecture)**:
  1. *Dynamic Topology (DyLAN)*: Layered DAG with dynamic agent importance scoring and low-contribution pruning threshold $\tau = 0.20$.
  2. *Static SOP (MetaGPT)*: Fixed 5-role assembly line (Product Manager $\to$ Architect $\to$ Project Manager $\to$ Engineer $\to$ QA Tester) with unprunable phase gates.
- **Factor B (Fault Injection Schedule)**:
  1. *Schedule 0 (Control)*: Clean baseline (zero injected faults).
  2. *Schedule 1 (Early Fault)*: Corrupted requirements prompt injected at Step 1 (syntactically malformed feature specification).
  3. *Schedule 2 (Late Fault)*: Injected runtime syntax exception and environment dependency error at Step 4 (simulating a broken database driver).
- **Sample Allocation**: 12 distinct programming tasks $\times$ 6 factorial cells = 72 experimental runs ($n = 12$ runs per cell).

#### C. Variables & Controlled Invariants
- **Independent Variables**: Architecture (Dynamic vs. Static) $\times$ Fault Injection Schedule (None, Early, Late).
- **Dependent Variables**:
  1. *Failure Recovery Rate* ($FRR \in [0, 1]$): Fraction of injected faults successfully diagnosed and repaired without human intervention.
  2. *Final Task Completion Rate* ($TCR \in [0, 1]$): Executable code passing functional test suites.
  3. *Topological Integrity Score* ($TIS \in [0, 1]$): Fraction of registered audit/QA roles surviving and active in the final execution layer.
  4. *Token Churn per Recovery* ($Tokens_{\text{recovery}}$): Additional tokens consumed resolving the injected exception.
- **Controlled Invariants**:
  - Identical base foundation model (`gpt-4o-mini`).
  - Identical fault payloads: deterministic string mutations for Early Fault; deterministic mock exception injection for Late Fault.
  - Identical execution timeout per run (300s).

#### D. Power Analysis & Statistical Discipline (Mandating Firth's Penalized Likelihood for Binary Recovery)
- **Statistical Models**:
  1. *Continuous Metrics* ($TIS$, $Tokens_{\text{recovery}}$): Evaluated via Two-Way Factorial Analysis of Variance (ANOVA).
  2. *Binary Metric* ($FRR \in \{0, 1\}$): Evaluated via Logistic Regression with interaction terms:
     $$\operatorname{logit}(P(FRR = 1)) = \beta_0 + \beta_1 \text{Arch} + \beta_2 \text{Fault} + \beta_3 (\text{Arch} \times \text{Fault})$$
- **Mandatory Firth's Penalized Likelihood Estimation**:
  In factorial fault-injection designs with $n = 12$ runs per cell, standard Maximum Likelihood Estimation (MLE) for logistic regression suffers catastrophic failure when cells experience zero failures or zero recoveries (e.g., Static SOP under Clean Baseline achieves 100% recovery, or Dynamic Pruning under Late Fault achieves 0% recovery). This condition, known as **quasi-complete separation** (Heinze & Schemper, 2002), causes standard MLE estimates $\hat{\beta}$ to diverge to $\pm \infty$, standard errors to explode, and Wald test $p$-values to become dangerously uninformative ($p \to 1.0$).
  To guarantee valid statistical inference, EXP-003 **mandates Firth's penalized likelihood estimation** (Firth, 1993). The penalized log-likelihood incorporates the Jeffreys invariant prior:
  $$L^*(\beta) = L(\beta) + \frac{1}{2} \log |I(\beta)|$$
  where $I(\beta)$ is the Fisher information matrix. The penalized score equations $\tilde{U}(\beta) = U(\beta) + a(\beta) = 0$ introduce a finite bias-correction vector $a_j = \frac{1}{2} \operatorname{tr}(I^{-1} \frac{\partial I}{\partial \beta_j})$ that eliminates first-order small-sample bias ($O(n^{-1})$), guarantees finite, bounded parameter estimates $\hat{\beta}_{\text{Firth}}$, and yields valid Profile Penalized Likelihood Ratio test statistics even in zero-event or monotone separation cells.
- **Degrees of Freedom**:
  - Factor A (Arch): $df = 2 - 1 = 1$.
  - Factor B (Fault): $df = 3 - 1 = 2$.
  - Interaction ($\text{Arch} \times \text{Fault}$): $df = 1 \times 2 = 2$.
  - Error: $df = 72 - 6 = 66$.
- **Exact Power Calculation**:
  - Prior studies using $n = 10$ per cell ($N = 60$) achieved an interaction power of only $0.7744 < 0.80$ (Challenger 2 Finding 1.4).
  - Expanding to **$n = 12$ runs per cell ($N = 72$ total runs)** increases the non-centrality parameter to $\lambda = N \cdot f^2 = 72 \cdot (0.40)^2 = 11.52$.
  - For large effect size $f = 0.40$ and $\alpha = 0.05$, exact power for the interaction term is:
    $$1 - \beta = \mathbf{0.8527} > 0.80$$
    satisfying strict scientific rigor standards.

#### E. What the Experiment COULD and COULD NOT Demonstrate
- **Could Demonstrate**:
  - Whether dynamic pruning heuristics introduce structural fragility by eliminating critical validator roles prior to exception occurrence.
  - The comparative resilience of static SOP pipelines when confronting unexpected runtime failures.
- **Could NOT Demonstrate**:
  - Whether an idealized, perfectly trained RL orchestrator (with billions of pre-training tokens) could theoretically learn to anticipate faults.
- **Explicit Non-Justified Conclusions**:
  - *Forbidden Conclusion 1*: "Dynamic agent networks should never be used." (Dynamic networks may remain superior for open-ended brainstorming where failure recovery is unnecessary).
  - *Forbidden Conclusion 2*: "Static SOPs are immune to failures." (Static SOPs struggle with early-stage requirement corruptions that require backward pipeline cycles).
- **External Validity Limitations**: Bounded to algorithmic programming tasks; does not evaluate physical robot execution or medical triage.
- **Unresolved Confounds**: The pruning threshold $\tau = 0.20$ in DyLAN is an empirical hyperparameter; different thresholds may alter survival rates.

---

## 3. Master Experiment Matrix Summary

| Experiment ID | Title | Core Falsification Target | Design & Model | Sample Size & Power | Primary Limitations | Non-Justified Conclusion Guard |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP-001** | Organizational Topology & Coordination Tax | Multi-agent collaboration does not beat B1-SC at matched tokens; levies $>35\%$ coordination tax. | 3 Conditions (Single B1-SC, Hierarchical B3, Decentralized B2); GLMM + TOST non-inferiority ($\delta=0.05$). | $N = 1,080$ ($72 \text{ tasks} \times 5 \text{ seeds}$); $n_{\text{eff}} \ge 225$ ($\rho=0.15$); Power $> 0.95$ ($\ge 0.85$ under $\rho=0.40$). | Bounded to SWE-bench code maintenance; prompt semantics cannot be 100% equalized. | Cannot conclude multi-agent systems are useless across all domains. |
| **EXP-002** | Independent Critic vs. In-Group Review | In-group review suffers sycophantic collapse; double-blind AST critic minimizes vulnerability escape. | 3 Conditions (No Review, In-Group, Double-Blind); Cochran's Q & McNemar's paired test. | $N_{\text{blocks}} = 280 \ge 279$ ($56 \text{ tasks} \times 5 \text{ seeds}$, total $N=840$); Power $= 0.903 > 0.90$ ($\alpha=0.01$). | Bounded to known CWE vulnerabilities; comment stripping may slightly elevate FPR. | Cannot conclude LLM critics eliminate 100% of zero-day vulnerabilities. |
| **EXP-003** | Dynamic Pruning vs. Static SOP Fault Robustness | Dynamic pruning causes topological collapse under late faults; static SOPs maintain auditor survival. | $2 \times 3$ Full Factorial ANOVA + Firth's Penalized Likelihood Logistic Regression. | $N = 72$ ($12 \text{ runs/cell}$); Error $df=66$; Interaction Power $= 0.8527 > 0.80$. | Bounded to algorithmic coding; DyLAN pruning threshold $\tau$ is a sensitive hyperparameter. | Cannot conclude static SOPs are globally superior for unconstrained tasks. |

---

## 4. Execution Governance & Gate R1 Attestation

This Proposed Experiment Matrix satisfies all requirements established in `ORIGINAL_REQUEST.md` (R6 and R10). Every experiment features explicit hypotheses, controlled baselines, cluster-aware statistical power models, concrete limitations, and forbidden non-justified conclusions.

> **FINAL REMINDER**:  
> In accordance with Curo Lifecycle State `RESEARCH_AUTHORIZED`, this document is a **theoretical design specification only**.  
> **ZERO EXPERIMENT EXECUTION OR CODE WRITING IS AUTHORIZED**.  
> Gate R1 may only authorize advancing to formal reproduction design; live benchmark execution remains strictly prohibited until explicit subsequent authorization.
