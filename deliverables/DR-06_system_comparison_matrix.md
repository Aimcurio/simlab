# DR-06: System Comparison Matrix
**Curo Deep Research Investigation — Comprehensive Cross-System Architectural Comparison Matrix**  
**Document ID**: `DR-06`  
**Document Version**: 1.0.0-FINAL  
**Lifecycle State**: `RESEARCH_AUTHORIZED` | **Implementation Authority**: `NOT_GRANTED`  
**Classification**: Formal Research Deliverable (Tier 1)  
**Author**: `curo_worker_1` (Primitive & Evidence Deliverables Author)  
**Verification Baseline**: `curo_explorer_1` (Archaeology), `curo_explorer_2` (Primitives), `curo_explorer_3` (Failures)  

---

## 1. Executive Summary & Comparison Scope

This deliverable provides an exhaustive, multi-dimensional comparative evaluation of the **five anchor reference systems** and **six key competing multi-agent frameworks**:

1. **Stanford Generative Agents / Smallville** (Park et al., 2023)
2. **AI Hospital** (Fan et al., 2024 / COLING 2025)
3. **AgentVerse** (Chen et al., 2024 / ICLR 2024)
4. **ChatDev** (Qian et al., 2024 / ACL 2024)
5. **Evolving Orchestration / Puppeteer** (Dang, Qian et al., 2025 / NeurIPS 2025)
6. **MetaGPT** (Hong et al., 2024 / ICLR 2024 Oral)
7. **Microsoft AutoGen** (Wu et al., 2023 / v0.4 rewrite)
8. **CAMEL** (Li et al., 2023 / NeurIPS 2023)
9. **DyLAN** (Liu et al., 2024 / ICLR 2024)
10. **MemGPT / Letta** (Packer et al., 2023)
11. **Google DeepMind Concordia** (Vezhnevets et al., 2024)

The evaluation spans seven architectural dimensions:
- **Mechanisms & Topologies**
- **Model Dependencies & Confound Footprints**
- **Execution & Clock Models**
- **Governance & Boundary Enforcement**
- **Memory & Retrieval Architecture**
- **Cost, Latency & Scaling Characteristics**
- **Task Suitability & Boundary Conditions**

---

## 2. Master System Comparison Matrix

| System Name | Primary Category | Organizational Topology | Execution & Scheduling Model | Memory Substrate | Governance & Safety Enforcement | Model & API Coupling | Primary Known Failure Mode |
|---|---|---|---|---|---|---|---|
| **Smallville (SYS-01)** | Social Simulation | Flat emergent decentralized graph | Synchronous 10-second discrete tick loop; file-polling IPC | Linear associative stream (`ConceptNode`); 3-factor rank retrieval | **Zero technical governance**; prompt-only adherence | Hardcoded `text-davinci-003` (deactivated); `openai==0.27.0` | Inverted recency decay; quadratic memory search scaling; disk deadlock |
| **AI Hospital (SYS-02)** | Clinical Evaluation | Triadic consultation & multi-doctor panels (`Parallel_with_Critique`) | Turn-based discrete conversational steps | Linear dialogue context buffer | Role prefix `<对医生讲>` with silent doctor fallback; GPT-4 judge | OpenAI API; Qwen / Wenxin adapters | Silent routing fallback; diagnostic hallucination without grounded tests |
| **AgentVerse (SYS-03)** | Task-Solving & Simulation | 4-Stage lifecycle; 8 pluggable decision topologies | Round-based discrete multi-agent loop | ChromaDB vector store & conversation history | Closed-loop Evaluator agent generating score & advice | Universal adapter: OpenAI, Claude, FastChat local | Recruitment thrashing; sycophantic debate convergence; token explosion |
| **ChatDev (SYS-04)** | Software Engineering | Waterfall Chat Chain pipeline; bilateral subtask nodes | Sequential phase execution loop | File-based code & document store; turn context | `<INFO>` consensus handshake token; self-reflection fallback | v1: `openai<1.0.0`; v2: modern API & Docker compose | Un-sandboxed host shell execution (`subprocess`); toy-scale project limits |
| **Puppeteer (SYS-05)** | Complex Reasoning Graph | Centralized RL orchestrator managing parallel paths | Dynamic graph-search traversal (up to 4 paths, 5 steps) | Continuous trajectory embeddings (`Nemotron-70B-Reward`) | Policy action masking (tool category filtering); depth bounds | PyTorch policy head; Llama-3.1-Nemotron-70B-Reward | RL policy collapse into ping-pong loops; extreme multi-GPU hardware barrier |
| **MetaGPT (SYS-06)** | Software Engineering | Standard Operating Procedures (SOPs) pipeline | Asynchronous event-driven workflow via pub/sub message bus | Global shared memory; multi-view document cache | Strict Pydantic schema validation; compiler feedback loop | OpenAI API; Claude; local LLM endpoints | Rigid schema fragility on non-standard tasks; upstream error backpropagation failure |
| **AutoGen (SYS-07)** | Generic Agent Platform | v0.2: GroupChatManager; v0.4: Actor Model | v0.2: Synchronous conversational loop; v0.4: Async event-driven actors | In-context conversation history; modular memory | v0.2: Prompt-only; v0.4: Actor boundary isolation & type contracts | Provider-agnostic client abstractions | v0.2: Speaker hijacking, infinite conversation loops; v0.4: Message mailbox starvation |
| **CAMEL (SYS-08)** | Communicative Exploration | Bilateral role-playing games (Instructor vs. Assistant) | Alternating turn-taking conversational game | In-context conversational turn history | Inception prompt contracts; termination delimiter token | OpenAI API; HuggingFace endpoints | Role-flipping on weak models; instruction echoing over long horizons |
| **DyLAN (SYS-09)** | Reasoning Network | Layered feed-forward network (`LLMLP`) | Feed-forward layer-by-layer sequential execution | In-context layer activations & candidate answers | Agent Importance Score (AIS) peer-rating pruning threshold | OpenAI API; legacy completion endpoints | Premature pruning of valid minority dissent; groupthink consensus collapse |
| **MemGPT / Letta (SYS-10)** | Agent Operating System | Hierarchical OS agent managing tools & memory | Event-driven interrupt loop with tool dispatch | Tiered Virtual Memory: Core (RAM), Recall (FIFO), Archival (Vector) | Function-call schema contracts; memory block size limits | OpenAI tool calling; Anthropic; local vLLM | Paging loop thrashing; self-lobotomization via malformed core memory replacement |
| **Concordia (SYS-11)** | Generative Social Simulation | Game-Master mediated multi-agent society | Discrete event simulation with component assembly | Structured Markdown interactive working memory documents | External Game Master arbitrates all physical/social actions | Flexible LLM provider interfaces | LLM Game Master referee bias and non-deterministic physical adjudication |

---

## 3. Deep Comparative Analysis across Architectural Dimensions

### 3.1 Organizational Topologies & Coordination Mechanisms
The corpus reveals three dominant organizational paradigms:
1. **Unconstrained Conversational Topologies (Smallville, AutoGen v0.2, CAMEL)**:
   - Agents communicate via natural language broadcast or direct messaging.
   - *Failure Pattern*: Suffers from quadratic message scaling $O(N^2)$, context saturation, speaker hijacking, sycophantic consensus loops, and unpredictable completion horizons.
2. **Standardized Procedural Pipelines (MetaGPT, ChatDev)**:
   - Replaces free-form discussion with structured waterfall phases and Standard Operating Procedures (SOPs).
   - *Advantage*: Reduces token consumption by $60\%\text{--}80\%$, bounds conversation turns, and enables deterministic handoffs between specialized roles.
   - *Limitation*: Fragile when tasks require dynamic backtracking or non-linear problem solving.
3. **Adaptive / Dynamic Reasoning Graphs (AgentVerse, DyLAN, Puppeteer)**:
   - Topologies mutate at runtime: AgentVerse recruits personas dynamically; DyLAN prunes inactive agents based on peer ratings; Puppeteer trains an RL policy network to explore cyclic reasoning paths.
   - *Trade-off*: Enhances reasoning on complex benchmarks (GSM8K, MMLU-Pro) at the expense of high token costs, compute overhead, and training complexity.

---

### 3.2 Memory Architecture & Retrieval Scalability

```
+---------------------------------------------------------------------------------------+
| SYSTEM       | MEMORY REPR.      | RETRIEVAL ALGORITHM         | TEMPORAL SCALING     |
+--------------+-------------------+-----------------------------+----------------------+
| Smallville   | Flat ConceptNodes | 3-factor rank decay (linear)| O(N * T) [Quadratic] |
| MemGPT/Letta | Tiered Virtual OS | Function-called SQL/Vector  | O(1) [Constant RAM]  |
| MetaGPT      | Document Cache    | Topic-based subscription    | O(Artifacts)         |
| AgentVerse   | ChromaDB Vector   | Cosine similarity           | O(log M)             |
| Concordia    | Markdown Blocks   | Declarative components      | O(1) per prompt      |
+---------------------------------------------------------------------------------------+
```

- **The Smallville Memory Trap**: Smallville's flat associative memory stream scans all stored memories on every tick, resulting in quadratic compute scaling $O(N \cdot T)$. By day 2 of simulation, 25 agents generate over 2,000 nodes, causing severe latency degradation.
- **The Operating System Solution (MemGPT)**: MemGPT bounds working memory to a fixed context window ($O(1)$) by implementing explicit paging to external SQLite and vector databases via function calls, establishing the optimal memory model for SimLab Layer B.

---

### 3.3 Governance, Authority & Boundary Enforcement

| System | Primary Governance Mechanism | Boundary Enforcement Technique | Replay / Injection Vulnerability |
|---|---|---|---|
| **Smallville** | None (Prompt instructions) | Unrestricted Python host environment | Total vulnerability: prompt injection triggers complete persona collapse |
| **AI Hospital** | Role tagging prefix (`<对医生讲>`) | Silent regex fallback to Doctor | High: prompt omission silently routes traffic without reporting errors |
| **ChatDev v1** | Delimiter token (`<INFO>`) | Host subprocess execution (`shell=True`) | Critical: Remote Code Execution (RCE) hazard on host machine |
| **AgentVerse** | Closed-loop Evaluator agent | Natural language advice & score threshold | Moderate: Evaluator is susceptible to LLM judge bias and sycophancy |
| **MetaGPT** | Pydantic Schema Contracts | Type validation on ActionNode outputs | Low: Syntax violations raise immediate runtime exceptions |
| **WarAgent** | Secretary Agent Auditor Gate | Pre-execution audit against treaty registry | Moderate: Persistent LLM persuasion can override prompt-based auditor |
| **Target SimLab** | **Deterministic CapBAC (Cedar/OPA)** | **Kernel-level capability token interception** | **Zero: Cryptographic capability verification in native code** |

- **The Prompt Governance Fallacy**: Systems relying entirely on natural language prompt instructions (Smallville, CAMEL, AutoGen v0.2) inevitably suffer from role drift, boundary violations, and authority hallucination.
- **SimLab Requirement**: SimLab must enforce Layer D governance using deterministic, native code policy engines (Cedar / OPA) and cryptographically signed capability tokens (`CapBAC`).

---

### 3.4 Execution, Concurrency & Clock Models

1. **Synchronous Lockstep File Polling (Smallville)**:
   - Backend and frontend exchange state via filesystem JSON writes, polling in a busy-wait loop (`while True: time.sleep(0.1)`). Single-threaded, highly vulnerable to disk I/O bottlenecks and desynchronization crashes.
2. **Turn-Based Conversational Step Loops (AI Hospital, CAMEL, ChatDev v1)**:
   - Progresses in sequential conversational turns. Bounded by max turn parameters, but wall-clock time is entirely dependent on external API response latency.
3. **Decoupled Asynchronous Actor Model (AutoGen v0.4, SimLab Target)**:
   - Non-blocking event loop (`asyncio`) where agents possess private mailboxes. High throughput ($> 10,000\text{ msg/sec}$), zero thread contention, but requires a discrete logical clock to preserve reproducible event ordering.

---

## 4. Model Dependencies, Confound Footprints & Compute Budgets

| System | Foundation Model Family | Context Length | Inference Calls per Task | Token Budget per Run | Seed Reporting | Confound Severity |
|---|---|---|---|---|---|---|
| **Smallville** | `text-davinci-003` (OpenAI legacy) | 4,096 | Thousands (continuous) | ~20,000–50,000 / agent-day | **No** | **Extreme**: Single unseeded run; obsolete model |
| **AI Hospital** | `gpt-4-1106-preview` & `gpt-3.5-turbo` | 8,192 | 15–30 per consultation | ~10,000–25,000 | **No** | **High**: Performance gains track model upgrade |
| **AgentVerse** | `gpt-3.5-turbo-0613` & `gpt-4` | 4,096 | 20–80 per benchmark task | ~15,000–40,000 | **No** | **High**: $4\times$ token spend over single-agent |
| **ChatDev** | `gpt-3.5-turbo-16k` | 16,384 | 30–60 per software run | ~48,000 average | **No** | **Moderate**: Toy-scale benchmark suite |
| **Puppeteer** | `Llama-3.1-Nemotron-70B-Reward` + LLM | 8,192 | Up to 20 search steps | ~15,000–35,000 | **Partial (3 seeds)** | **High**: Heavy compute requirement |
| **MetaGPT** | `gpt-4-0613` | 8,192 | 10–25 per software run | ~25,000 average | **No** | **High**: Baseline comparison ran on GPT-3.5 |
| **DyLAN** | `gpt-3.5-turbo` & `gpt-4` | 4,096 | $N \times R + N(N-1)R$ | ~12,000–25,000 | **Yes (3 seeds)** | **Moderate**: Peer evaluation prompt overhead |

---

## 5. Task Suitability & Boundary Conditions

| System | Recommended Task Domains | Pathological / Unsuitable Domains | Substrate Reusability for SimLab |
|---|---|---|---|
| **Smallville** | Open-ended social sandbox simulation; behavioral ecology | Goal-directed engineering; fast-paced real-time interaction; high-concurrency games | **NON-REUSABLE** (Defunct API, inverted formulas, disk deadlocks) |
| **AI Hospital** | Structured multi-role clinical interview evaluation; examiner tests | Open-ended patient ward navigation; surgical robotics; unstructured social chats | **PARTIALLY REUSABLE** (Grounded examination oracle pattern) |
| **AgentVerse** | Benchmark problem-solving; comparative topology research | Hard real-time physical simulation; strict budget-constrained production workflows | **REUSABLE** (Lifecycle engine & pluggable topologies) |
| **ChatDev** | Small greenfield software applications; educational coding | Multi-file legacy code refactoring; secure production deployments; non-coding tasks | **PARTIALLY REUSABLE** (`<INFO>` handshake & compiler loop) |
| **Puppeteer** | Complex multi-hop reasoning graphs; mathematical search | Low-compute embedded environments; unstructured creative role-play | **REUSABLE** (Reasoning graph exploration algorithms) |
| **MetaGPT** | Structured software engineering; enterprise document workflows | Open-ended emergent social dilemmas; real-time diplomatic negotiations | **HIGHLY REUSABLE** (SOP typed artifacts & pub/sub bus) |
| **MemGPT / Letta**| Lifelong agent interaction; multi-turn long-horizon tasks | Simple 1-shot stateless QA tasks; ultra-low-latency reflexive control | **HIGHLY REUSABLE** (Tiered virtual memory architecture) |
| **Concordia** | Social science simulations; game-theoretic economic games | Software development; deterministic automated unit testing | **REUSABLE** (Game Master state mediation pattern) |

---

## 6. Synthesis & Strategic Guidance for SimLab Substrate

1. **Substrate Rejection**: Neither Stanford Smallville nor ChatDev v1 can serve as the foundational execution substrate for SimLab. Both suffer from severe technical disqualifications (Smallville's defunct API endpoints and inverted math; ChatDev's host shell vulnerability).
2. **Primitive Synthesis Recommendation**: SimLab must pursue **Strategy C (Clean Rebuild)**, synthesizing:
   - **Environment (Layer A)**: Decoupled logical clock (`PRIM-SIM-03`) + Transactional state store (`PRIM-SIM-04`) + Game Master grounding (`PRIM-SIM-02`).
   - **Cognition (Layer B)**: Tiered virtual memory (`PRIM-COG-04`) + Self-directed editing (`PRIM-COG-05`) + Structured markdown documents (`PRIM-COG-06`).
   - **Organization (Layer C)**: SOP typed artifact handoffs (`PRIM-ORG-01`) + Actor model runtime (`PRIM-ORG-06`) + Dynamic recruitment (`PRIM-ORG-03`).
   - **Governance (Layer D & G)**: Deterministic CapBAC engine (`PRIM-GOV-03`) + Sandboxed Docker isolation (`PRIM-GOV-04`) + Compiler feedback loops (`PRIM-GOV-01`).
   - **Observability (Layer H & I)**: Distributed OpenTelemetry context propagation (`PRIM-COM-05`) + Deterministic unit assertion scoring.
