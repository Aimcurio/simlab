# DR-11: Reproduction Candidate List & Prioritization Framework

**Document Version**: 1.0.0-FINAL  
**Lifecycle State**: `RESEARCH_AUTHORIZED` (Implementation Authority: `NOT_GRANTED`)  
**Project**: Curo Deep Research Investigation — Agent Simulation Lab (SimLab)  
**Author**: `curo_worker_2` (Failures, Registers & Experiments Author)  
**Integrity Mode**: Benchmark / Adversarial Verification  
**Date**: 2026-09-15  

---

## 1. Executive Summary & Epistemic Framing

### 1.1 Governance Directive: Research Design Only
> **MANDATORY LIFECYCLE BOUNDARY INVARIANT**:  
> In strict adherence to Curo Lifecycle State `RESEARCH_AUTHORIZED` and Governance Directive R6 (`ORIGINAL_REQUEST.md`), this document represents **research design and candidate prioritization only**.  
> **ZERO IMPLEMENTATION OR EXECUTION AUTHORITY IS GRANTED**.  
> This deliverable does NOT authorize writing simulator code, cloning unapproved repositories, installing runtime dependencies, executing benchmark scripts, invoking model APIs, or performing live test runs. Implementation and reproduction execution belong exclusively to subsequent phases requiring explicit, independent requester approval.

### 1.2 Objective & Prioritization Rationale
The primary literature across the anchor reference systems (Smallville, AI Hospital, AgentVerse, ChatDev, Evolving Orchestration) contains profound claims of emergent reasoning, autonomous collaboration, and algorithmic efficiency. However, as established in the Failure Register (DR-07) and Conflict Register (DR-08), many foundational findings are tainted by implementation bugs, lack of compute normalization, saturated benchmarks, or monorepo coupling.

To determine which mechanisms warrant eventual empirical reproduction in SimLab Milestone M0/M1, this document establishes a **rigorously prioritized candidate list: RP-01 through RP-04**. Prioritization is determined via a multi-factor ranking rubric:
1. **Architectural Foundational Impact**: Does resolving this claim fundamentally dictate SimLab's core layer design?
2. **Severity of Literature Divergence / Flaw**: Was the original finding produced by a known bug, missing control, or paper-code contradiction?
3. **Falsifiability & Experimental Tractability**: Can the claim be definitively falsified with a clean, bounded experimental design?
4. **Generalizability**: Does the mechanism transfer beyond toy demonstrations to enterprise-scale environments?

---

## 2. Prioritized Reproduction Candidate Register

```
+----------------------------------------------------------------------------------------------------+
|                                    REPRODUCTION CANDIDATE REGISTER                                 |
+----------------------------------------------------------------------------------------------------+
| Rank 1: RP-01 | Smallville Memory Inversion & Multi-Factor Retrieval Verification                  |
| Rank 2: RP-02 | Multi-Agent Debate vs. Compute-Normalized Single-Agent Baselines                   |
| Rank 3: RP-03 | ChatDev Phase Sandboxing, Tool Grounding & Task Completion Generalizability        |
| Rank 4: RP-04 | Evolving Orchestration RL Policy Efficiency vs. Static Waterfall Pipelines         |
+----------------------------------------------------------------------------------------------------+
```

---

### 2.1 Candidate RP-01: Smallville Memory Inversion & Retrieval Scoring Verification

#### A. Candidate Identification & Provenance
- **Candidate ID**: `RP-01`
- **Priority Rank**: **Rank 1 (Foundational Cognitive Substrate Validity)**
- **Primary Source**: Park et al. (UIST 2023 / arXiv:2304.03442), *Generative Agents: Interactive Simulacra of Human Behavior*.
- **Authoritative Repository**: `https://github.com/joonspk-research/generative_agents`, commit `fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4`.

#### B. Target Claims
1. The paper claims that an agent's daily behavioral believability, schedule adherence, and emergent social coordination are driven by a balanced 3-factor memory retrieval function:
   $$\text{Score}(m) = \alpha_r \cdot \text{Recency}(m) + \alpha_i \cdot \text{Importance}(m) + \alpha_{rel} \cdot \text{Relevance}(m, q)$$
   with equal weighting ($\alpha_r = 1, \alpha_i = 1, \alpha_{rel} = 1$).
2. The paper claims that recency decays exponentially as a function of elapsed virtual game hours:
   $$\text{Recency}_{\text{paper}}(m) = 0.995^{\Delta t_{\text{hours}}}$$

#### C. Empirical Flaw & Literature Contradiction
As proven in DR-07 (FM-02) and DR-08 (Conflict C-03):
1. **Recency Decay Inversion**: In `retrieve.py:145-146, 224-228`, memories are sorted chronologically ascending, placing the oldest memory at index `0`. Recency is assigned via array rank: `recency_vals = [0.99 ** i for i in range(1, len(nodes) + 1)]`. After min-max normalization, **the oldest memory receives recency 1.0, while the newest receives 0.0**. The code completely inverted the recency score!
2. **Weight Discrepancy**: In `retrieve.py:244-250`, global weights are hardcoded to `gw = [0.5, 3, 2]`, weighting relevance ($3.0$) six times higher than recency ($0.5$).
3. **Daily Replanning Stub**: In `plan.py:487-490`, the daily replanning module is an incomplete stub marked `# TODO` that simply recycled initial requirements.

#### D. Core Falsification Objective
Determine whether correcting the recency decay formula to true temporal decay ($\lambda^{\Delta t_{\text{hours}}}$) and restoring equal weights ($1:1:1$) actually improves, degrades, or leaves unchanged agent schedule fidelity, social coordination, and conversational coherence.

#### E. Experimental Design & Required Controls
- **Independent Variables**:
  1. *Recency Formula*: (a) Smallville Inverted Rank ($0.99^i$), (b) True Temporal Decay ($0.995^{\Delta t_{\text{hours}}}$), (c) Zero Recency ($\alpha_r = 0$).
  2. *Retrieval Weighting*: (a) Paper Claim ($1:1:1$), (b) Code Reality (`gw = [0.5, 3, 2]`), (c) Pure Vector Similarity ($0:0:1$).
- **Controlled Invariants**: Fixed foundation model (`gpt-4o-mini` via modern API); identical initial town state and persona seeds; identical discrete simulation clock (integer ticks); identical sensory perception radii.
- **Evaluation Suite**: Replay the 48-hour Valentine's Day party scenario across 5 random seeds per condition.
- **Required Metrics**:
  - Information Diffusion Rate (percentage of agents aware of the party at $T = 36\text{h}$);
  - Schedule Adherence Index (correlation between planned hourly schedule and executed coordinate actions);
  - Hallucinatory Intrusion Rate (frequency of retrieving irrelevant background memories).

#### F. Estimated Compute & Resource Requirements
- Simulation horizon: 48 simulated hours ($2,880$ simulation ticks at 1 min/step).
- Population: 25 agents.
- Estimated inference tokens per condition: $\sim 18\text{M}$ tokens ($9$ conditions $\times$ $5$ seeds = $45$ simulation runs $\approx 810\text{M}$ tokens total across the full ablation grid).

---

### 2.2 Candidate RP-02: Multi-Agent Debate vs. Compute-Normalized Single-Agent Baselines

#### A. Candidate Identification & Provenance
- **Candidate ID**: `RP-02`
- **Priority Rank**: **Rank 2 (Resolves Core Organizational Investment Dilemma)**
- **Primary Sources**:
  - Chen et al. (ICLR 2024), *AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors*, `OpenBMB/AgentVerse`.
  - Li et al. (Tencent, 2024 / arXiv:2402.05120), *"More Agents Is All You Need"*.
  - Wang et al. (ACL 2024), *ChatDev*, `OpenBMB/ChatDev`.
  - Anonymous (arXiv:2509.05396 & arXiv:2604.09000), *"Talk Isn't Always Cheap"* & *"The Cost of Consensus"*.

#### B. Target Claims
Multi-agent collaborative debate panels achieve emergent reasoning superiority over single-agent execution through distributed cognitive diversity, peer critique, and communicative error correction.

#### C. Empirical Flaw & Literature Contradiction
As documented in Conflict C-01 and Failure Modes FM-05 and FM-06:
1. Multi-agent debate exhibits **sycophantic consensus collapse** (modal adoption rates $>85.5\%$) and **consensus degradation** ($DCR$), where correct dissenting agents are persuaded by incorrect majorities.
2. In virtually all published papers claiming multi-agent superiority, the single-agent baseline was tested with zero-shot prompting at $K=1$, confounding multi-agent collaboration with simple test-time compute scaling.
3. When total tokens and sampling attempts are matched, Single-Agent + CoT + Self-Consistency (B1-SC) matches or outperforms multi-agent debate panels without the $4\times$ to $220\times$ coordination tax.

#### D. Core Falsification Objective
Determine whether multi-agent collaborative debate panels (e.g., AgentVerse 3-agent debate, ChatDev bilateral chat) provide any statistically significant accuracy advantage over Single-Agent Self-Consistency (B1-SC) when total generated inference tokens are held strictly equal.

#### E. Experimental Design & Required Controls
- **Independent Variable**: Collaboration Topology:
  1. Condition 1 (B1-SC): Single LLM Agent with Chain-of-Thought and Self-Consistency ($K$ samples aggregated via majority voting).
  2. Condition 2 (B2-Debate): 3-Agent Collaborative Debate Panel (unconstrained chat across 3 rounds).
  3. Condition 3 (B3-Static): Hierarchical Multi-Agent Team (Leader-Worker with review).
- **Controlled Invariants**:
  - *Strict Compute Normalization*: Total generated token budget per problem clamped to $B \pm 5\%$ across all conditions (e.g., allocating $K$ samples in B1-SC such that $K \times \text{Tokens}_{\text{single}} = \text{Tokens}_{\text{multi-agent}}$).
  - Identical foundation models (evaluated across both `gpt-4o-mini` and `claude-3-5-haiku`).
  - Identical generation temperature ($T = 0.7$ for sampling/debate).
- **Evaluation Suite**: 100 problems from GSM8K (math), 100 problems from HumanEval (code), and 50 problems from SWE-bench Lite.
- **Required Metrics**:
  - Task Accuracy / Pass@1;
  - Coordination Tax ($CT = \text{Tokens}_{\text{inter-agent}} / \text{Tokens}_{\text{total}}$);
  - Sycophantic Collapse Rate;
  - Wall-clock Latency ($T_{\text{latency}}$).

#### F. Estimated Compute & Resource Requirements
- Total tasks: 250 tasks $\times$ 3 conditions $\times$ 5 seeds = 3,750 problem evaluations.
- Estimated tokens: $\sim 45\text{M}$ tokens total.

---

### 2.3 Candidate RP-03: ChatDev Phase Sandboxing, Tool Grounding & Task Completion Generalizability

#### A. Candidate Identification & Provenance
- **Candidate ID**: `RP-03`
- **Priority Rank**: **Rank 3 (Software Engineering & Tooling Validity)**
- **Primary Source**: Qian et al. (ACL 2024 / arXiv:2307.07924), *Communicative Agents for Software Development (ChatDev)*.
- **Authoritative Repository**: `https://github.com/OpenBMB/ChatDev`, tags `v1.0.0` / `v2.2.0`.

#### B. Target Claims
ChatDev simulates an end-to-end virtual software company capable of autonomous software design, coding, testing, and documentation across diverse software engineering domains, producing functional software through communicative dehallucination.

#### C. Empirical Flaw & Literature Contradiction
As documented in Conflict C-04 and Failure Modes FM-08 and FM-09:
1. **Toy Scope Restriction**: ChatDev's default configuration and system prompts explicitly restrict implementation to single-file or two-file standalone Pygame scripts (e.g., Gomoku, 2048).
2. **Infinite Repair Loops**: When encountering complex compiler errors, ChatDev agents enter memoryless 2-state oscillation loops (FM-08).
3. **Hallucinated Dependencies**: Agents routinely hallucinate non-existent external libraries (FM-09) due to lack of hermetic package pinning and AST pre-validation.
4. **Zero SWE-bench Generalizability**: ChatDev achieves $<3\%$ pass rates on realistic multi-file codebase maintenance tasks.

#### D. Core Falsification Objective
Determine whether ChatDev's bilateral chat-chain architecture can generalize to multi-file software engineering tasks when augmented with hermetic AST sandboxing and dependency pinning, or whether its bilateral conversational structure fundamentally breaks down under multi-file architectural coupling.

#### E. Experimental Design & Required Controls
- **Independent Variables**:
  1. *Architecture*: (a) ChatDev Bilateral Chat Chains, (b) MetaGPT SOP Assembly Line, (c) Single-Agent ReAct with Tool Access (SWE-agent style).
  2. *Sandboxing Rigor*: (a) Unconstrained ChatDev default (raw subprocess execution), (b) Hermetic AST Sandboxing (network egress blocked, pinned package manifest, AST diff cycle detection).
- **Controlled Invariants**: Fixed foundation model (`gpt-4o-2024-08-06`); identical execution timeout (300s); identical test suite fixtures.
- **Evaluation Suite**: 30 tasks from SWE-bench Lite (multi-file python bug fixes) + 20 Greenfield application specifications (from HumanEval-X).
- **Required Metrics**:
  - Executable Project Completion Rate (% of projects that compile and run);
  - SWE-bench Resolved Rate;
  - Infinite Repair Loop Frequency;
  - Dependency Hallucination Frequency.

#### F. Estimated Compute & Resource Requirements
- Total tasks: 50 tasks $\times$ 3 architectures $\times$ 2 sandbox modes = 300 runs.
- Estimated tokens: $\sim 60\text{M}$ tokens.

---

### 2.4 Candidate RP-04: Evolving Orchestration RL Policy Efficiency vs. Static Waterfall Pipelines

#### A. Candidate Identification & Provenance
- **Candidate ID**: `RP-04`
- **Priority Rank**: **Rank 4 (Dynamic Topology & Learned Routing Optimization)**
- **Primary Sources**:
  - Dang, Qian et al. (NeurIPS 2025 / arXiv:2505.19591), *Multi-Agent Collaboration via Evolving Orchestration*.
  - Liu et al. (ICLR 2024 / arXiv:2310.02170), *Dynamic LLM-Agent Network (DyLAN)*.
- **Authoritative Repository**: `https://github.com/OpenBMB/ChatDev/tree/puppeteer`, commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a`.

#### B. Target Claims
Centralized, reinforcement-learned meta-orchestration ("Puppeteer") dynamically learns optimal collaboration topologies, reducing inference token consumption by $31.8\%$ while simultaneously outperforming static waterfall pipelines on complex multi-step reasoning.

#### C. Empirical Flaw & Literature Contradiction
As documented in Conflict C-06 and Failure Modes FM-10 and FM-11:
1. **Monorepo Reality & Training Cost Confound**: Evolving Orchestration is an experimental branch of ChatDev, not an independent general-purpose framework. Its reported inference token savings completely ignore the massive upfront compute cost of RL pre-training (thousands of simulated rollouts with heavy reward shaping).
2. **Topological Collapse & Thrashing**: Under unpredictable inputs or injected runtime faults, dynamic routing policies frequently suffer from agent starvation (eliminating critical verification roles) or orchestration thrashing (rapidly reassigning subtasks without execution depth).

#### D. Core Falsification Objective
Determine whether a pre-trained RL orchestrator policy (Puppeteer) maintains its claimed token efficiency and accuracy advantages when subjected to out-of-distribution reasoning tasks and mid-stream runtime exceptions, compared to a deterministic static SOP pipeline (MetaGPT).

#### E. Experimental Design & Required Controls
- **Independent Variables**:
  1. *Orchestration Mode*: (a) Trained RL Puppeteer policy (`OpenBMB/ChatDev:puppeteer`), (b) DyLAN Layered Pruning, (c) MetaGPT Static Waterfall SOP, (d) Static Round-Robin Router.
  2. *Task Distribution*: (a) In-Distribution Tasks (GSM8K/MATH), (b) Out-of-Distribution Tasks (adversarial logic puzzles and multi-stage code refactoring).
- **Controlled Invariants**: Identical worker agent models (`gpt-4o-mini`); identical reward feedback functions; identical maximum turn limit ($T_{\text{max}} = 15$).
- **Evaluation Suite**: 50 In-Distribution tasks + 50 Out-of-Distribution tasks.
- **Required Metrics**:
  - Task Accuracy;
  - Net Inference Tokens Consumed;
  - Total Compute Amortization (Inference Tokens + Pro-Rated Training Tokens);
  - Orchestration Thrashing Index (frequency of 1-turn agent context switches);
  - Safety Role Starvation Rate.

#### F. Estimated Compute & Resource Requirements
- Evaluation runs: 100 tasks $\times$ 4 orchestration modes $\times$ 3 seeds = 1,200 runs.
- Estimated tokens: $\sim 35\text{M}$ inference tokens (excluding policy pre-training checkpoint replication).

---

## 3. Summary Comparison & Prioritization Matrix

| Candidate ID | Priority Rank | Target System | Core Phenomenon Tested | Primary Literature Flaw Exposed | Expected Decision for SimLab Target Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RP-01** | **Rank 1** | Smallville | Memory Retrieval & Recency Decay | Recency inversion bug ($0.99^i$) and $6\times$ weight imbalance in authoritative code | Conclusively resolves whether Smallville's cognitive substrate can be salvaged or requires clean rebuild (validating Strategy C). |
| **RP-02** | **Rank 2** | AgentVerse / Multi-Agent Debate | Collaboration vs Compute-Matched Single Agent | Sycophantic consensus collapse; lack of compute-normalized B1-SC baselines | Dictates whether SimLab invests in complex conversational debate or focuses on compute-normalized sampling & tool verification. |
| **RP-03** | **Rank 3** | ChatDev | Multi-Agent Software Development | Hardcoded toy Pygame scope; infinite repair loops; hallucinated dependencies | Governs design of Layer A (Virtual FS) and Layer D (Hermetic AST Sandboxing) for enterprise software experiments. |
| **RP-04** | **Rank 4** | Evolving Orchestration / DyLAN | Learned Dynamic Orchestration | High offline RL training costs masked; topological collapse under runtime exceptions | Establishes whether SimLab adopts dynamic RL routing or enforces deterministic FSM macro-pipelines with micro-adaptability. |

---

## 4. Methodological Compliance & Execution Governance

In strict conformance with Curo Lifecycle Phase `RESEARCH_AUTHORIZED`:
1. **No Code Execution**: This candidate list provides the formal research specifications required for future reproduction phases. No reproduction scripts have been executed.
2. **Acceptance Criteria Satisfaction**: All candidates possess explicit primary sources, code citations, falsification goals, control groups, and resource estimates.
3. **Escalation Boundary**: Execution of any candidate on this list requires advancing past Gate R1 and obtaining formal Requester Approval for Milestone M0/M1 implementation.
