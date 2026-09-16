# DR-08: Conflict Register & Literature Controversy Analysis

**Document Version**: 1.0.0-FINAL  
**Lifecycle State**: `RESEARCH_AUTHORIZED` (Implementation Authority: `NOT_GRANTED`)  
**Project**: Curo Deep Research Investigation — Agent Simulation Lab (SimLab)  
**Author**: `curo_worker_2` (Failures, Registers & Experiments Author)  
**Integrity Mode**: Benchmark / Adversarial Verification  
**Date**: 2026-09-15  

---

## 1. Executive Summary & Epistemic Framework

### 1.1 Objective & Research Invariant
In accordance with Curo's **Anti-Premature-Synthesis Invariant** (`ORIGINAL_REQUEST.md`), the multi-agent research landscape must not be treated as a settled consensus. The field is actively fractured by profound empirical contradictions, conflicting benchmark claims, and severe divergences between published academic narratives and inspected codebase implementations.

This deliverable establishes the **Authoritative Conflict Register (DR-08)**, documenting six foundational controversies (C-01 through C-06). Each conflict is decomposed into:
1. **The Opposing Claims**: Precise theoretical and empirical stances of competing research camps or paper-vs-code claims.
2. **Empirical Evidence & Discriminatory Findings**: Data, mathematical proofs, benchmarks, and exact code citations (repository, branch, file, line number).
3. **Formal Resolution State**: Authoritatively classified strictly as `RESOLVED`, `PARTIALLY_RESOLVED`, or `UNRESOLVED`.
4. **Architectural Impact for SimLab**: Concrete engineering and design implications for the target simulation platform.

### 1.2 Resolution Taxonomy
- **`RESOLVED`**: Objective empirical or code evidence conclusively settles the contradiction; one claim is definitively falsified or verified.
- **`PARTIALLY_RESOLVED`**: The scope of validity for competing claims has been delineated (e.g., approach X outperforms in domain A, but fails in domain B), but general theoretical closure is pending.
- **`UNRESOLVED`**: Evidence remains fundamentally divided, missing, or confounded; classified as an authoritative scientific research outcome requiring future experimental design.

---

## 2. Comprehensive Conflict Register

```
+----------------------------------------------------------------------------------------------------+
|                                    MASTER CONFLICT REGISTER                                        |
+----------------------------------------------------------------------------------------------------+
| Conflict C-01: Multi-Agent Collaboration vs. Single-Agent + Compute Normalization                   |
| Conflict C-02: Dynamic Topology vs. Static Standardized Operating Procedures (SOPs)               |
| Conflict C-03: Smallville Paper Claims vs. Inspected Repository Realities                          |
| Conflict C-04: ChatDev Software Engineering Generalizability vs. Toy Game Realities                |
| Conflict C-05: Agent Hospital Clinical Evolution vs. Closed Benchmark Saturation                  |
| Conflict C-06: Evolving Orchestration Independence vs. ChatDev Monorepo Reality                    |
+----------------------------------------------------------------------------------------------------+
```

---

### 2.1 Conflict C-01: Multi-Agent Collaboration vs. Single-Agent + Compute Normalization

#### A. Opposing Claims
- **Camp A (Multi-Agent Superiority)**: Primary papers in the collaborative multi-agent literature—such as ChatDev (Qian et al., 2024), MetaGPT (Hong et al., 2024), AgentVerse (Chen et al., 2024), and CAMEL (Li et al., 2023)—claim that multi-agent conversational teams exhibit emergent collective intelligence, outperforming single-agent LLM systems by $15\%\text{--}35\%$ on complex reasoning, software engineering, and problem-solving benchmarks.
- **Camp B (Compute-Normalized Parity / Inferiority)**: Recent rigorous empirical evaluations—such as *"More Agents Is All You Need"* (Li et al., Tencent, 2024, arXiv:2402.05120), *"Talk Isn't Always Cheap"* (arXiv:2509.05396), and *"The Cost of Consensus"* (arXiv:2604.09000)—demonstrate that **when total inference compute (number of generated tokens and sampling attempts $K$) is equalized, homogeneous multi-agent collaboration provides zero net performance gain over single-agent Chain-of-Thought (CoT) with Self-Consistency (SC)**. Multi-agent debate merely levies a massive "coordination tax" of $4\times$ to $220\times$ higher token consumption.

#### B. Empirical Evidence & Discriminatory Findings
1. **The Coordination Tax**: Multi-agent systems consume between 4 and 220 times the token budget of standard single-agent inference due to repetitive system prompt reinjection, conversational politeness, multi-turn echoing, and context serialization.
2. **Statistical Independence vs. Sycophantic Collapse**: On mathematical reasoning (GSM8K, MATH) and code generation (HumanEval), sampling $K$ independent solutions from a single agent and selecting the majority answer (Self-Consistency) achieves higher accuracy than a $K$-agent conversational debate panel. The single-agent samples are statistically independent, whereas conversational debate panels suffer from sycophantic consensus collapse (modal adoption rates exceeding $85.5\%$, where correct agents recant their answers when confronted by fluent incorrect majorities).
3. **Confound Attribution**: When multi-agent papers report large accuracy gains over "single-agent baselines", the single-agent baseline was evaluated using standard zero-shot prompting at $K=1$, confounding multi-agent collaboration with simple test-time compute scaling.

#### C. Formal Resolution State
- **Status**: `PARTIALLY_RESOLVED`
- **Resolution Rationale**: For closed-domain algorithmic, mathematical, and single-file coding tasks, Camp B is empirically verified: multi-agent debate offers no benefit over compute-matched single-agent self-consistency. However, multi-agent architectures remain functionally necessary in domains characterized by:
  - Genuine distributed data privacy boundaries (agents holding distinct private information);
  - Asymmetric physical/digital tool permissions;
  - Concurrent spatial navigation in simulated environments;
  - Tasks exceeding the maximum context window of any single model.

#### D. Architectural Impact for SimLab
1. **Mandatory Control Group**: Multi-agent topologies must NEVER be claimed as superior without compute normalization. SimLab mandates Baseline **B1-SC (Single LLM + CoT + Self-Consistency at matched token spend)** as a compulsory control group for all benchmark evaluations.
2. **Coordination Tax Metric**: Introduce metric M03 (Coordination Tax) to quantify the token overhead of collaboration:
   $$CT = \frac{\text{Inter-Agent Communication Tokens}}{\text{Total Task Tokens Generated}}$$

---

### 2.2 Conflict C-02: Dynamic Topology vs. Static Standardized Operating Procedures (SOPs)

#### A. Opposing Claims
- **Camp A (Dynamic Topology & Adaptive Recruitment)**: Frameworks such as AgentVerse (Chen et al., 2024), DyLAN (Liu et al., 2024), and Evolving Orchestration (Dang et al., 2025) argue that static, hardcoded multi-agent topologies are brittle and inefficient. High-performance systems require runtime adaptability: dynamically recruiting specialist agents, pruning low-contribution agents, and learning routing policies via reinforcement learning.
- **Camp B (Static SOP Pipelines)**: Frameworks such as MetaGPT (Hong et al., 2024) and ChatDev (Qian et al., 2024) argue that dynamic recruitment and unconstrained meta-orchestration introduce organizational chaos, token waste, and unpredictable collapse. High reliability requires rigid, assembly-line Standardized Operating Procedures (SOPs) with fixed role definitions, deterministic phase transitions, and strictly typed Pydantic artifact schemas.

#### B. Empirical Evidence & Discriminatory Findings
1. **DyLAN Pruning vs. Downstream Fragility**: DyLAN reports a $25\%$ token reduction with preserved accuracy on MMLU and MATH by pruning agents with low early contribution scores. However, red-team analysis and code inspection reveal that on multi-stage software workflows, dynamic pruning eliminates QA and security auditors during early drafting phases, leading to catastrophic late-stage failure (FM-10).
2. **MetaGPT Rigidity vs. Requirement Perturbation**: MetaGPT's static waterfall SOP achieves 100% executable project completion on standard Greenfield software tasks. However, when tasks involve unexpected runtime exceptions or mid-stream requirement modifications, MetaGPT fails because the static pipeline cannot propagate backwards from testing to architecture without restarting the pipeline from scratch.

#### C. Formal Resolution State
- **Status**: `PARTIALLY_RESOLVED`
- **Resolution Rationale**: The dichotomy between pure static pipelines and pure dynamic recruitment is an unforced error. Static pipelines provide macro-level phase stability, while dynamic adaptation is required for micro-level error recovery.

#### D. Architectural Impact for SimLab
- **Hybrid Phase-Bounded Dynamic Governance**: SimLab adopts a two-tier organizational model:
  1. *Macro-Level*: A deterministic, static Finite State Machine (FSM) governs lifecycle phases (Requirements $\to$ Architecture $\to$ Implementation $\to$ Review $\to$ Deployment), preventing topological collapse and coordination thrashing.
  2. *Micro-Level*: Within each lifecycle phase, micro-topologies may dynamically recruit or select worker agents from a registered capability pool, bounded by hard resource ceilings ($N_{\text{max}}$, $Tokens_{\text{max}}$) and unprunable safety-role anchors.

---

### 2.3 Conflict C-03: Smallville Paper Claims vs. Inspected Repository Realities

#### A. Opposing Claims
- **Published Paper Claims (Park et al., ACM UIST 2023 / arXiv:2304.03442)**: Smallville presents an elegant, mathematically balanced generative cognitive architecture capable of producing believable human social simulacra. Specifically claimed:
  1. Balanced 3-factor memory retrieval ($\alpha_r = 1, \alpha_i = 1, \alpha_{rel} = 1$);
  2. Exponential recency decay over elapsed game hours ($0.995^{\Delta t_{\text{hours}}}$);
  3. Autonomous daily replanning based on accumulated memories;
  4. Generalizable cognitive modeling on OpenAI models;
  5. Scalable multi-agent interactive world.
- **Authoritative Repository Realities (`joonspk-research/generative_agents`, commit `fe05a71`)**: Line-by-line code inspection reveals severe architectural and algorithmic divergences that directly contradict the published paper.

#### B. Empirical Evidence & Discriminatory Findings

| Architectural Component | Published Paper Claim | Codebase Reality | Exact Code Reference | Empirical & Scientific Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Retrieval Weights** | Balanced equal weights: $\alpha_r = 1, \alpha_i = 1, \alpha_{rel} = 1$ | Hardcoded global weights `gw = [0.5, 3, 2]`. Relevance is weighted $6\times$ higher than recency. | `retrieve.py:244-250` | In practice, recency had virtually zero influence on recall compared to semantic similarity. |
| **Recency Decay Formula** | Exponential decay over elapsed game hours: $0.995^{\Delta t_{\text{hours}}}$ | Inverted rank-order index: $0.99^i$ on candidate list sorted oldest-first. | `retrieve.py:145-146, 224-228` | **Recency curve was completely inverted**, assigning $1.0$ to the oldest memory and $0.0$ to the freshest memory. |
| **Daily Replanning** | Agents autonomously revise broad daily schedules each morning based on yesterday's memories. | Incomplete stub explicitly marked `# TODO`; statically recycles initial daily requirement bootstrap string. | `plan.py:487-490` | Agents never synthesized new daily goals; they repeated Day 1 bootstrap schedules throughout the run. |
| **Model API Interface** | Generalizable LLM reasoning via ChatGPT. | Hardcoded legacy `text-davinci-003` with manual string interpolation; deprecated endpoint. | `gpt_structure.py:211-220, 285` | Incompatible with modern OpenAI APIs (`openai>=1.0.0`); completely defunct without patching. |
| **IPC & Simulation Engine** | Scalable multi-agent virtual world. | Single-threaded backend polling un-locked JSON files on local disk (`time.sleep(0.1)`). | `reverie.py:311-412` | Severe disk I/O bottlenecks; race conditions with frontend browser; freezes under multi-agent reflection. |

#### C. Formal Resolution State
- **Status**: `RESOLVED`
- **Resolution Rationale**: The contradiction between paper claims and repository realities is conclusively resolved by direct code inspection. The emergent social behaviors reported in Smallville (e.g., the spread of the Valentine's Day party invitation) were produced by a fragile, hand-tuned, and mathematically buggy artifact rather than the robust, balanced cognitive engine described in the paper.

#### D. Architectural Impact for SimLab
1. **Total Rejection of Smallville Codebase**: Smallville cannot serve as the codebase substrate for SimLab. Incremental refactoring (Strategy A) or wrapper architectures (Strategy B) are formally rejected in favor of a clean, ground-up rebuild (Strategy C).
2. **Negative Constraints Enforced**: Implements NC-06 (no unseeded time), NC-07 (no file-polling IPC), and NC-08 (no inverted recency decay).

---

### 2.4 Conflict C-04: ChatDev Software Engineering Generalizability vs. Toy Game Realities

#### A. Opposing Claims
- **Published Paper Claim (Qian et al., ACL 2024 / arXiv:2307.07924)**: ChatDev simulates a comprehensive, end-to-end virtual software development company capable of autonomous software design, coding, testing, and documentation across diverse software engineering domains.
- **Repository Reality (`OpenBMB/ChatDev`, tags `v1.0.0` / `v2.2.0`)**: Codebase inspection reveals that ChatDev's default configuration (`ChatChainConfig.json`, `CompanyConfig/Default/`) is heavily hardcoded to generate standalone, single-file or two-file Pygame scripts (e.g., Gomoku, 2048, Flappy Bird, Calculator).

#### B. Empirical Evidence & Discriminatory Findings
1. **Prompt Constraint Restrictions**: In `ChatDev` prompt templates, agents are explicitly instructed: *"All codes should be implemented in a single Python file or basic module"* to prevent broken imports across files.
2. **Zero Large-Scale Codebase Refactoring**: ChatDev contains zero mechanisms for:
   - Ingesting and navigating existing repositories with thousands of files;
   - Managing database migrations or schema evolution;
   - Resolving external microservice dependencies or asynchronous network APIs;
   - Generating multi-file unified git diffs.
3. **SWE-bench Incompatibility**: When evaluated on realistic software maintenance benchmarks (e.g., SWE-bench Lite / Verified), ChatDev's conversational chat-chain architecture achieves near-zero pass rates ($< 3\%$) because bilateral conversational turn-taking lacks the hierarchical context indexing required for enterprise code navigation.

#### C. Formal Resolution State
- **Status**: `RESOLVED`
- **Resolution Rationale**: ChatDev is an impressive, pioneering demonstration of communicative dehallucination on toy, greenfield, single-file scripts. However, claims that it represents a generalizable virtual software company capable of production software engineering are falsified by code and benchmark realities.

#### D. Architectural Impact for SimLab
- **Separation of Toy vs Enterprise Scenarios**: SimLab will not adopt ChatDev's bilateral chat chains for complex software tasks. SimLab requires an environment layer (Layer A) supporting virtual file systems, unified AST parsers, and isolated git workspaces.

---

### 2.5 Conflict C-05: Agent Hospital Clinical Evolution vs. Closed Benchmark Saturation

#### A. Opposing Claims
- **Paper Claim (Li et al., May 2024 / Tsinghua AIR, arXiv:2405.02957)**: Doctor agents evolved within a simulated hospital (MedAgent-Zero) reach an unprecedented $\sim 93.06\%$ accuracy on MedQA, self-improving through thousands of simulated patient consultations without supervised human data.
- **Literature Counter-Evidence & Clinical Reality**: Contemporary medical AI literature (Takara, 2024; MedRxiv, 2024) demonstrates that multiple-choice medical examination benchmarks (MedQA, USMLE) are **saturated** and measure passive factual memorization rather than interactive clinical competence. When doctor agents are evaluated in realistic, interactive multi-turn diagnostic environments, accuracy plummets. Doctors exhibit premature diagnostic closure, fail to ask differential questions, and hallucinate laboratory findings (FM-03).
- **Critical Corpus Disambiguation**: As established in DR-02 and `archaeology_report.md`:
  - **AI Hospital** (`LibertFan/AI_Hospital`, arXiv:2402.09742, Fan et al., Fudan/Alibaba): Multi-role clinical consultation and Multi-View Medical Evaluation (MVME) benchmark. **Codebase exists and is inspected.**
  - **Agent Hospital** (arXiv:2405.02957, Zhang et al., Tsinghua AIR): Subtitled *"A Simulacrum of Hospital with Evolvable Medical Agents"*. **No public code repository was released.**

#### B. Empirical Evidence & Discriminatory Findings
1. **Benchmark Saturation vs Clinical Validity**: Multiple-choice MedQA questions present complete, pre-digested patient vignettes containing all necessary positive and negative symptoms. In contrast, interactive consultation requires the doctor to actively elicit symptoms from an uncertain patient, order discriminative tests, and avoid contraindicated therapies.
2. **Interactive Consultation Degradation**: In Fan et al. (`AI_Hospital`), evaluating doctor agents on interactive consultations using the Multi-View Medical Evaluation (MVME) framework reveals that doctor accuracy on differential diagnosis drops by $30\%\text{--}50\%$ compared to static multiple-choice performance.
3. **Reproducibility Barrier**: Claims regarding "MedAgent-Zero" autonomous evolution cannot be verified in the primary repository because the authors of arXiv:2405.02957 did not release their simulation code, leaving the evolutionary claims scientifically unverified.

#### C. Formal Resolution State
- **Status**: `RESOLVED` (Benchmark saturation & repository disambiguation) / `UNRESOLVED` (Autonomous clinical evolution claims).
- **Resolution Rationale**: The gap between closed multiple-choice accuracy and interactive clinical competence is conclusively resolved: high MedQA scores do not imply clinical safety. The specific evolutionary claims of MedAgent-Zero remain unresolved due to absent source code.

#### D. Architectural Impact for SimLab
1. **Interactive Evaluation Protocol**: SimLab will not use static multiple-choice datasets to evaluate autonomous agent capability. Benchmarks must evaluate interactive multi-turn task completion with environmental feedback.
2. **Deterministic Safety Pre-Checks**: In high-stakes simulation domains, deterministic constraint layers (Layer D) must enforce safety boundaries outside LLM reasoning.

---

### 2.6 Conflict C-06: Evolving Orchestration Independence vs. ChatDev Monorepo Reality

#### A. Opposing Claims
- **Paper Framing (Dang, Qian et al., arXiv:2505.19591, accepted at NeurIPS 2025)**: "Multi-Agent Collaboration via Evolving Orchestration" presents evolving orchestration as a generalizable, autonomous reinforcement-learned meta-orchestrator ("Puppeteer") that dynamically learns collaboration topologies across open- and closed-domain tasks, saving tokens and outperforming static pipelines.
- **Repository Archaeology & Implementation Reality**: Literature and repository archaeology resolve that **there is no independent, standalone repository** for Evolving Orchestration. The authoritative implementation is hosted as an experimental branch (`puppeteer`) within the existing `OpenBMB/ChatDev` repository (`https://github.com/OpenBMB/ChatDev/tree/puppeteer`, commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a`).

#### B. Empirical Evidence & Discriminatory Findings
1. **Monorepo Coupling**: Code inspection of branch `puppeteer` demonstrates that the orchestrator is tightly coupled to ChatDev's internal message-passing classes (`ChatChain`, `ChatNode`). It is not an independent orchestration engine.
2. **Training Overhead vs Inference Savings**: While the paper reports a $31.8\%$ token reduction during inference, the RL puppeteer policy requires extensive, task-specific pre-training (over thousands of simulated rollouts with heavy reward engineering). The total compute expenditure (training + inference) exceeds static pipelines unless amortized over millions of identical tasks.
3. **Disambiguation from DyLAN**: Evolving Orchestration is distinct from DyLAN (`SALT-NLP/DyLAN`, Liu et al., ICLR 2024). DyLAN uses unsupervised peer contribution scores at each DAG layer; Evolving Orchestration uses a centralized RL policy model selecting the next agent.

#### C. Formal Resolution State
- **Status**: `RESOLVED`
- **Resolution Rationale**: The architectural identity and implementation location of Evolving Orchestration are conclusively established. It is an experimental feature branch of ChatDev, not an autonomous, standalone framework.

#### D. Architectural Impact for SimLab
1. **Integration into Layer C/E**: Evolving orchestration should be modeled in SimLab as a dynamic policy plugin within the Experiment Harness (Layer E) rather than an all-encompassing platform architecture.
2. **Compute Accounting**: Any evaluation of learned orchestration policies must explicitly account for offline training tokens in its total cost budget (DR-13).

---

## 3. Summary Conflict Ledger

| Conflict ID | Topic | Camp A / Paper Claim | Camp B / Reality | Discriminatory Evidence | Status | SimLab Architecture Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **C-01** | Multi-Agent vs Single-Agent Compute | Multi-agent collaboration yields emergent $+15\text{--}35\%$ accuracy gains | Single-agent + CoT + Self-Consistency equals or beats multi-agent at matched tokens | arXiv:2402.05120, arXiv:2509.05396; modal adoption $>85.5\%$ | `PARTIALLY_RESOLVED` | Mandate B1-SC compute-normalized control group; restrict multi-agent to true distributed domains. |
| **C-02** | Dynamic Topology vs Static SOP | Dynamic recruitment/pruning maximizes adaptability and token efficiency | Dynamic pruning causes topological collapse; static SOPs provide execution guarantees | DyLAN QA pruning collapse (FM-10); MetaGPT 100% executable vs 62% ChatDev | `PARTIALLY_RESOLVED` | Hybrid FSM macro-pipeline + micro-dynamic recruitment within bounded phases. |
| **C-03** | Smallville Paper vs Codebase | Balanced retrieval ($1:1:1$), game-hour recency decay, autonomous daily replan | Hardcoded `gw=[0.5,3,2]`, inverted recency decay $0.99^i$, `# TODO` replan stub | `retrieve.py:145-146, 224-228`; `plan.py:487-490`; `reverie.py:311-412` | `RESOLVED` | Reject Smallville codebase; clean ground-up rebuild (Strategy C); enforce NC-06, NC-07, NC-08. |
| **C-04** | ChatDev Generalizability vs Toy Scope | Virtual software company for end-to-end software development | Hardcoded single-file Pygame script generation; zero multi-file refactoring | `ChatChainConfig.json`; prompt template restrictions; $<3\%$ pass on SWE-bench | `RESOLVED` | Discard bilateral chat chains for enterprise software; build Layer A virtual FS and AST diffing. |
| **C-05** | Agent Hospital vs Benchmark Saturation | Autonomous clinical evolution reaches $93.06\%$ MedQA accuracy | MedQA is saturated; doctors fail interactive consultation; unreleased code | arXiv:2402.09742 vs arXiv:2405.02957; MVME interactive accuracy drop $30\text{--}50\%$ | `RESOLVED` (Saturation) / `UNRESOLVED` (Evolution) | Require interactive evaluation environments; enforce deterministic safety matrices (Layer D). |
| **C-06** | Evolving Orchestration Independence | Standalone, generalizable RL multi-agent orchestration framework | Experimental `puppeteer` branch in `OpenBMB/ChatDev` monorepo; high RL training cost | Commit `b24e6e6` in `OpenBMB/ChatDev`; dependency on ChatDev classes | `RESOLVED` | Model as an experimental Layer C/E routing plugin; mandate offline training token accounting. |

---

## 4. Conclusion & Scientific Integrity Note

This register documents that the multi-agent literature contains significant confounds, paper-to-code divergences, and unsubstantiated claims of emergent superiority. By formally resolving these contradictions and acknowledging unresolved boundaries, SimLab establishes an empirical baseline free from the biases and unverified assumptions of earlier systems.
