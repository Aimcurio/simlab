# DR-09: Unknowns Register & Open Architectural Questions

**Document Version**: 1.0.0-FINAL  
**Lifecycle State**: `RESEARCH_AUTHORIZED` (Implementation Authority: `NOT_GRANTED`)  
**Project**: Curo Deep Research Investigation — Agent Simulation Lab (SimLab)  
**Author**: `curo_worker_2` (Failures, Registers & Experiments Author)  
**Integrity Mode**: Benchmark / Adversarial Verification  
**Date**: 2026-09-15  

---

## 1. Executive Summary & Epistemic Framing

### 1.1 The Epistemic Invariant: UNRESOLVED as an Authoritative Result
In accordance with Curo Governance Directive R5 (`ORIGINAL_REQUEST.md`), **`UNRESOLVED` is an authoritative, scientifically valid research result**. When empirical evidence is absent, conflicting, or fundamentally confounded, forcing an architectural decision by assumption or consensus is strictly prohibited. 

Earlier multi-agent frameworks repeatedly failed because authors made ungrounded assumptions regarding memory scalability, organizational flexibility, and emergent intelligence. This register identifies, characterizes, and operationalizes **six critical architecture-shaping unknowns (U-01 through U-06)**. None of these questions can be resolved through literature review alone; each defines a mandatory empirical frontier requiring controlled experimental investigation in subsequent Curo phases.

### 1.2 Schema for Open Questions
Each entry in this register documents:
1. **Unknown ID & Formal Title**
2. **Core Architectural Dilemma**: The precise technical tradeoff confronting SimLab.
3. **Current Literature State & Competing Evidence**: What is known vs. where existing studies break down.
4. **Epistemic Classification**: Formally maintained as `UNRESOLVED`.
5. **Mandatory Escalation Policy**: Why literature synthesis cannot close the question.
6. **Proposed Empirical Investigation**: The concrete methodology required in future phases (M1–M6) to resolve the dilemma.
7. **Falsification & Decision Criteria**: The measurable threshold that will dictate final architecture selection.

---

## 2. Comprehensive Unknowns Register

```
+----------------------------------------------------------------------------------------------------+
|                                      UNKNOWNS REGISTER (DR-09)                                     |
+----------------------------------------------------------------------------------------------------+
| U-01: Optimal Governance-Flexibility Trade-off Frontier                                            |
| U-02: Associative Memory Scaling vs. Interference Threshold                                       |
| U-03: Model-Independence of Multi-Agent Topologies                                                |
| U-04: Confound Disentanglement: Cognitive Specialization vs. Compute Scaling                      |
| U-05: Discrete Simulation Clock vs. Real-Time LLM Latency Synchronization                          |
| U-06: Long-Horizon Error Compounding Limits in Autonomous Societies                                |
+----------------------------------------------------------------------------------------------------+
```

---

### 2.1 U-01: Optimal Governance-Flexibility Trade-off Frontier

#### A. Core Architectural Dilemma
What is the mathematical and operational relationship between the strictness of deterministic policy enforcement (Layer D: Cedar / OPA + CapBAC) and the creative, emergent problem-solving capability of LLM agent teams?
- *Hypothesis 1 (Tight Security)*: Strict deterministic policies eliminate security violations (Unauthorized Action Rate $UAR = 0\%$) and guarantee compliance, but overly rigid schemas restrict exploratory action spaces, reducing complex task completion rates ($TCR$).
- *Hypothesis 2 (Loose Security)*: Permissive environments maximize agent autonomy and out-of-the-box reasoning, but inevitably permit catastrophic failure modes (TOCTOU attacks, prompt injections, data exfiltration).

#### B. Current Literature State & Competing Evidence
- Enterprise agent frameworks (e.g., AutoGen Enterprise, LangGraph) enforce rigid static JSON schemas, achieving zero security breaches but failing completely when novel edge cases require actions not envisioned in the schema.
- Open-ended agent worlds (e.g., Smallville, Concordia, CAMEL) rely entirely on soft natural language prompt guardrails, which are demonstrably vulnerable to jailbreaking, prompt injection, and goal drift.
- **The Gap**: No published research has mapped the empirical Pareto frontier between policy expressiveness and agent problem-solving effectiveness.

#### C. Formal Epistemic Status
- **Status**: `UNRESOLVED`

#### D. Mandatory Escalation Policy
This dilemma cannot be settled by literature review because published benchmarks either evaluate security without reasoning (synthetic injection tests) or reasoning without security (HumanEval, SWE-bench). Resolving this question requires live experimental manipulation of policy restrictiveness, which is forbidden under current lifecycle state `RESEARCH_AUTHORIZED` (Implementation Authority: `NOT_GRANTED`).

#### E. Proposed Empirical Investigation
- **Phase Target**: Milestone M3 (Experimentable) / M5 (Adversarial).
- **Methodology**: Parametric policy loosening across a benchmark of 50 non-standard problem-solving tasks containing both red-team security traps and complex multi-step objectives. Measure task completion rate ($TCR$) vs. unauthorized action rate ($UAR$) across 4 policy strictness levels ($\theta_0$ pure prompt guardrails to $\theta_3$ zero-trust least-privilege Cedar policies).

#### F. Falsification & Decision Criteria
If increasing policy constraint strictness from $\theta_1$ (typed capability tokens) to $\theta_3$ (pre-compiled deterministic execution ASTs) reduces $TCR$ by more than $15\%$ on valid tasks, SimLab must adopt a tiered escalation model allowing agents to request dynamic capability expansion with human-in-the-loop signoff.

---

### 2.2 U-02: Associative Memory Scaling Limits vs. Interference Threshold

#### A. Core Architectural Dilemma
At what memory volume $N$ does vector-similarity retrieval in a continuous, unpruned episodic stream cross the threshold where negative associative interference (retrieving superficially similar but contextually irrelevant memories) exceeds the benefit of long-term recall?

#### B. Current Literature State & Competing Evidence
- Smallville (`joonspk-research/generative_agents`) implements a flat associative memory stream. In practice, performance degrades significantly after $\sim 1,000$ ConceptNodes due to memory crowding and episodic drift (FM-01).
- MemGPT / Letta (Packer et al., 2023) mitigates this by manually paging memory between in-context RAM and external SQLite/vector tables via function calling.
- **The Gap**: While hierarchical paging avoids context overflow, the fundamental information-theoretic limit—the point at which embedding space density causes semantic collisions and retrieval distraction as a function of embedding dimension $D$ and memory cluster entropy $H$—remains mathematically unmodeled and empirically unmeasured.

#### C. Formal Epistemic Status
- **Status**: `UNRESOLVED`

#### D. Mandatory Escalation Policy
Literature benchmarks evaluate retrieval on static question-answering datasets (BEIR, HotpotQA) with fixed document corpora. They do not evaluate continuous, dynamic episodic streams generated by autonomous agents interacting over thousands of ticks.

#### E. Proposed Empirical Investigation
- **Phase Target**: Milestone M3 (Experimentable).
- **Methodology**: Long-horizon synthetic stress test: inject a controlled stream of $N \in [10^2, 10^3, 10^4, 10^5]$ episodic memory nodes into simulated agents. Periodically query the agent with factual recall, multi-hop reasoning, and goal-tracking prompts. Evaluate Recall@K, Precision@K, and downstream decision accuracy across different embedding models (Ada-002, text-embedding-3-small, BGE-large).

#### F. Falsification & Decision Criteria
Identify the critical inflection point $N^*$ where retrieval precision drops below $0.80$. If $N^* \le 2,000$ for standard dense vector search, SimLab must mandate an active memory consolidation layer (clustering, summarization, and cold-storage archiving) in Layer B.

---

### 2.3 U-03: Model-Independence of Multi-Agent Topologies

#### A. Core Architectural Dilemma
Are specific multi-agent collaboration topologies (e.g., MetaGPT's waterfall SOP, ChatDev's chat chains, DyLAN's layered DAG pruning) intrinsically effective organizational structures, or are their reported advantages merely empirical artifacts of the specific foundation models (e.g., GPT-3.5-Turbo, GPT-4-0613) on which they were developed?

#### B. Current Literature State & Competing Evidence
- MetaGPT (Hong et al., 2024) demonstrated massive gains over single-agent baselines using GPT-4-0613. However, when modern frontier models with long contexts and strong inherent reasoning (e.g., OpenAI o1/o3, Claude 3.5 Sonnet) are evaluated on identical benchmarks, single-agent architectures achieve comparable or superior results without multi-agent decomposition.
- Conversely, on small open-weight models (7B–8B parameters), complex multi-agent topologies frequently collapse due to syntax errors, formatting failures, and instruction neglect.
- **The Gap**: Does multi-agent decomposition provide an invariant structural advantage, or does it merely compensate for the localized working-memory limitations of mid-tier 2023 foundation models?

#### C. Formal Epistemic Status
- **Status**: `UNRESOLVED`

#### D. Mandatory Escalation Policy
Cross-model architectural invariance cannot be deduced from single-model papers. Authors rarely benchmark their multi-agent topologies across multiple model families and parameter scales under identical prompts.

#### E. Proposed Empirical Investigation
- **Phase Target**: Milestone M4 (Comparable).
- **Methodology**: Full $4 \times 4$ factorial evaluation: 4 Topologies (Single-Agent CoT B1, ChatDev B2, MetaGPT SOP B3, Evolving Orchestration B4) $\times$ 4 Foundation Model Classes (Local Quantized 8B, Open-Weights 70B, Commercial Standard Frontier, Commercial Reasoning Frontier) evaluated on HumanEval and SWE-bench Lite.

#### F. Falsification & Decision Criteria
If the relative performance ranking of topologies changes significantly across model tiers (Topology $\times$ Model interaction $p < 0.01$), the hypothesis of "universal topology superiority" is falsified. SimLab must make organizational topology a dynamic, model-dependent configuration parameter rather than a fixed platform invariant.

---

### 2.4 U-04: Confound Disentanglement: Cognitive Specialization vs. Compute Scaling

#### A. Core Architectural Dilemma
Does the measured performance advantage of a multi-agent system stem from *genuine cognitive diversity and specialized persona prompting*, or does it derive entirely from *increased aggregate test-time compute* (repeated token sampling, multi-turn revision, and ensemble voting)?

#### B. Current Literature State & Competing Evidence
- *Specialization Advocates*: Hong et al. (MetaGPT) and Chen et al. (AgentVerse) argue that role assignment (e.g., Architect, QA Engineer) restricts the hypothesis space, reduces token generation entropy, and guides the LLM into specialized functional domains.
- *Compute Advocates*: Li et al. (Tencent, 2024, *"More Agents Is All You Need"*) demonstrate that simply querying a single un-prompted model $N$ times with temperature $T > 0$ and aggregating via majority voting matches or exceeds multi-agent debate performance, concluding that "agents" are merely expensive token samplers.
- **The Gap**: Studies have not cleanly disentangled role prompting from sample count while holding total generated tokens, prompt length, and sampling temperature strictly constant.

#### C. Formal Epistemic Status
- **Status**: `UNRESOLVED`

#### D. Mandatory Escalation Policy
Literature claims are diametrically opposed and rely on differing token accounting methodologies. Resolving this requires a tightly controlled ablation experiment designed specifically to isolate the role variable from the compute variable (see DR-12, Experiment EXP-001).

#### E. Proposed Empirical Investigation
- **Phase Target**: Milestone M3 (Experimentable).
- **Methodology**: Evaluate 3 compute-matched conditions on GSM8K and HumanEval:
  1. *Condition 1*: Single agent with uniform neutral prompt, sampled $K$ times with majority vote (B1-SC).
  2. *Condition 2*: Single agent prompted sequentially with $K$ specialized personas in a single context window.
  3. *Condition 3*: $K$ independent agents with specialized personas collaborating via multi-agent debate.
  Total token generation budget is clamped to exactly $B_{\text{budget}} \pm 5\%$ across all three conditions.

#### F. Falsification & Decision Criteria
If Condition 1 (neutral unprompted self-consistency) matches Condition 3 (multi-agent debate) within statistical margin ($\Delta \le 2\%$, $p > 0.05$), the hypothesis that multi-agent persona specialization provides distinct cognitive benefits on reasoning tasks is falsified.

---

### 2.5 U-05: Discrete Simulation Clock vs. Real-Time LLM Latency Synchronization

#### A. Core Architectural Dilemma
How can a multi-agent simulation kernel maintain behavioral plausibility, causal fairness, and physical consistency when heterogeneous agents running on different foundation models or API providers exhibit variable wall-clock latencies ranging from 200ms to 45,000ms per decision?

#### B. Current Literature State & Competing Evidence
- *Lockstep Discrete Ticking (Smallville)*: Reverie blocks the entire simulation clock until all 25 agents finish their cognitive cycles for tick $t$. This guarantees causal consistency but introduces catastrophic latency: if one agent triggers a 30-second reflection loop, the entire simulation world freezes, making large-scale scaling impossible.
- *Decoupled Real-Time Streaming (Concordia, AI Town)*: The simulation clock runs continuously in wall-clock time. Agents act whenever their API call completes. However, fast agents (using small local models) take 50 actions in the time a slow frontier agent takes to complete 1 action, causing severe causal unfairness and physical anomalies (e.g., an agent walks across the entire town while another is still processing a greeting).
- **The Gap**: No published architecture has formulated a hybrid synchronization protocol that preserves discrete causal ordering without blocking on the slowest tail-latency model call.

#### C. Formal Epistemic Status
- **Status**: `UNRESOLVED`

#### D. Mandatory Escalation Policy
Cannot be resolved theoretically. The optimal synchronization model depends on the physical dynamics of the target environment and API network latency profiles.

#### E. Proposed Empirical Investigation
- **Phase Target**: Milestone M1 (Instrumented Kernel) / M3 (Experimentable).
- **Methodology**: Implement and benchmark 3 synchronization models in SimLab Layer A:
  1. *Model 1*: Strict Lockstep (Synchronous barrier at each tick $\Delta T$).
  2. *Model 2*: Speculative Execution with Rollback (Agents act on predicted state; rolled back if an upstream slow action alters the affordance graph).
  3. *Model 3*: Discrete Event Simulation (DES) Priority Queue (Actions scheduled at logical future ticks $T_{\text{action}} = T_{\text{curr}} + \Delta t_{\text{action}}$; kernel processes events in logical tick order regardless of wall-clock completion time).

#### F. Falsification & Decision Criteria
If Model 3 (DES Priority Queue) achieves causal fairness ($0$ temporal paradoxes) with a wall-clock throughput at least $5\times$ higher than Model 1 (Strict Lockstep), Model 3 becomes the mandatory synchronization standard for SimLab.

---

### 2.6 U-06: Long-Horizon Error Compounding Limits in Autonomous Societies

#### A. Core Architectural Dilemma
In an unbounded, closed-loop multi-agent simulation (e.g., 30+ consecutive simulated days without scripted resets), what is the maximum temporal horizon $T_{\text{collapse}}$ before uncorrected cognitive drift, memory pollution, and cascading hallucinations cause complete collapse of social coherence?

#### B. Current Literature State & Competing Evidence
- Published generative agent simulations operate over extremely short horizons:
  - Smallville (Park et al.): 2 simulated game days ($\sim 48$ hours), with heavy author intervention and prompt scaffolding.
  - AI Hospital (Fan et al.): Single-session consultations lasting 5–15 conversational turns.
  - ChatDev (Qian et al.): Single software development sessions lasting $< 10$ minutes.
- Long-horizon agent literature in open environments (e.g., Wang et al., *Voyager*; Tan et al., *WarAgent*) notes that after 50–100 interaction steps, autonomous agents exhibit severe behavioral loops, goal forgetting, and catastrophic hallucination cascades.
- **The Gap**: No empirical baseline exists documenting the survival curve, error compounding rate, or stability ceiling of autonomous LLM societies over extended temporal horizons ($T > 10,000$ ticks).

#### C. Formal Epistemic Status
- **Status**: `UNRESOLVED`

#### D. Mandatory Escalation Policy
Literature contains zero long-horizon unscripted runs due to token costs and early simulation death. This is the foremost open scientific frontier of generative agent research.

#### E. Proposed Empirical Investigation
- **Phase Target**: Milestone M6 (Research Lab).
- **Methodology**: 14-day continuous closed-loop simulation run with 20 autonomous agents in a resource-constrained economic/social environment. Track daily social metrics: conversational coherence, schedule fidelity, relationship consistency, hallucination frequency, and goal persistence. Compare baseline agents against agents equipped with truth-maintenance memory pruning and peer-auditing critic loops.

#### F. Falsification & Decision Criteria
Determine whether the rate of compounding social errors is linear $O(T)$ or exponential $O(e^{\alpha T})$. If error compounding is exponential, autonomous long-horizon agent societies are impossible without periodic external ground-truth checkpoints or human-in-the-loop state resets.

---

## 3. Summary Unknowns Register

| ID | Title | Core Tradeoff / Question | Status | Primary Escalation Trigger | Proposed Resolution Phase |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U-01** | Governance vs. Flexibility | Cedar/OPA strictness vs. creative reasoning emergence | `UNRESOLVED` | Zero literature on security vs reasoning Pareto frontiers | M3 / M5 |
| **U-02** | Memory Scaling vs. Interference | Point where vector retrieval noise outweighs memory benefit | `UNRESOLVED` | Dynamic episodic streams unstudied in IR literature | M3 |
| **U-03** | Model-Independence of Topologies | Are topologies universal or artifacts of 2023 foundation models? | `UNRESOLVED` | Lack of cross-model factorial benchmarks in literature | M4 |
| **U-04** | Specialization vs. Compute Scaling | Do personas add cognitive value or merely multiply token sampling? | `UNRESOLVED` | Contradictory claims in top-tier papers (Tencent vs MetaGPT) | M3 (EXP-001) |
| **U-05** | Simulation Clock vs. API Latency | Reconciling discrete event fairness with 200ms–45s API tails | `UNRESOLVED` | Simulation engines either block or sacrifice causality | M1 / M3 |
| **U-06** | Long-Horizon Error Compounding | Maximum temporal horizon before autonomous societal collapse | `UNRESOLVED` | Zero published unscripted simulations beyond 48 hours | M6 |

---

## 4. Methodological Compliance & Forward Guidance

By cataloging these six architecture-shaping questions with explicit `UNRESOLVED` status, this deliverable prevents premature architectural lock-in. Subsequent implementation milestones must not build monolithic solutions assuming these questions are settled. Instead, SimLab must be designed as an **instrumented experimental laboratory** specifically equipped to test, falsify, and resolve these unknowns through empirical measurement.
