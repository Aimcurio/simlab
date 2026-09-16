# DR-03: System Architecture Profiles
**Curo Deep Research Investigation — Deep Structural Profiles across Anchor & Competing Systems**  
**Document ID**: `DR-03`  
**Document Version**: 1.0.0-FINAL  
**Lifecycle State**: `RESEARCH_AUTHORIZED` | **Implementation Authority**: `NOT_GRANTED`  
**Classification**: Formal Research Deliverable (Tier 1)  
**Author**: `curo_worker_1` (Primitive & Evidence Deliverables Author)  
**Verification Baseline**: `curo_explorer_1` (Archaeology Report & Line Citations), `curo_explorer_2` (Primitive Catalog)  

---

## 1. Architectural Decomposition Framework

To evaluate multi-agent architectures objectively and prepare the evidence base for the **Agent Simulation Lab (SimLab)**, each anchor system and key competitor is analyzed across six fundamental architectural layers:

```
+-----------------------------------------------------------------------------------+
| 1. ENVIRONMENT LAYER   | Spatial representation, state persistence, physics/tools |
| 2. COGNITION LAYER     | Memory streams, retrieval, reflection, planning, prompts |
| 3. ORGANIZATION LAYER  | Roles, hierarchy, delegation, topologies, lifecycle      |
| 4. GOVERNANCE LAYER    | Authority rules, validation, gating, sandboxing, safety  |
| 5. SIMULATION LAYER    | Clock model, scheduling, synchronization, IPC, scaling   |
| 6. COMMUNICATION LAYER | Protocols, message formats, routing, consensus handshakes|
+-----------------------------------------------------------------------------------+
```

---

## 2. Anchor System 1: Stanford Generative Agents / Smallville

### 2.1 Overview & Architectural Identity
- **Reference**: Park et al. (ACM UIST 2023 / arXiv:2304.03442).
- **Codebase**: `joonspk-research/generative_agents` (commit `fe05a71`).
- **Core Paradigm**: Open-ended social sandbox simulation of 25 autonomous agents inhabiting a 2D tile-world ("the Ville").

### 2.2 Layer-by-Layer Architectural Profile

#### Layer 1: Environment Layer
- **Spatial Topology**: 2D tile grid matrix parsed from CSV files by `reverie/backend_server/maze.py:19-120`. Spatial address tree organized into 4 hierarchical levels:
  $$\text{World} \longrightarrow \text{Sector} \longrightarrow \text{Arena} \longrightarrow \text{Game Object}$$
  (e.g., `the Ville : Hobbs Cafe : cafe : refrigerator`).
- **Object State**: Game objects possess textual state descriptions (`"is_occupied"`, `"is_cooking"`, `"is_idle"`).
- **Routing**: Pathfinding uses an unoptimized Breadth-First Search (BFS) flood-fill algorithm (`reverie/backend_server/path_finder.py:12-85`) returning coordinate paths `[(x_1, y_1), (x_2, y_2), \dots]`. Collision layers prevent tile overlap.

#### Layer 2: Agent Cognition Layer
- **Memory Architecture**: Monolithic associative memory stream (`associative_memory.py:19-48`) storing chronological `ConceptNode` instances representing events, thoughts, and dialogues.
  - Node Schema: `node_id`, `node_type`, `created`, `last_accessed`, `subject`, `predicate`, `object`, `description`, `embedding_key`, `poignancy`, `keywords`, `filling`.
  - Hierarchy: Thoughts point to supporting memory IDs in `filling`; `depth = 1 + max(parent depths)`.
- **Retrieval Engine**: 3-factor composite ranking (`retrieve.py:199-271`):
  $$\text{Score}(m) = \alpha_{\text{rec}} \cdot \text{Recency}(m) + \alpha_{\text{imp}} \cdot \text{Poignancy}(m) + \alpha_{\text{rel}} \cdot \text{Relevance}(m, q)$$
  - *Divergence*: Code implements list-rank decay $\text{Recency} = 0.99^i$ (`retrieve.py:145-146`), not paper's game-hour decay $0.995^{\Delta t}$.
  - *Divergence*: Global factor weights are hardcoded as `gw = [0.5, 3, 2]` (`retrieve.py:244-250`), weighting relevance $6\times$ over recency.
- **Reflection Subsystem**: Triggered via an importance counter (`scratch.py:61-62`) initialized at 150. Decremented by LLM-judged poignancy ($1 \dots 10$) per perceived event (`reflect.py:149-170`). When $\le 0$, queries LLM for 3 focal questions, retrieves top-30 memories, extracts 5 high-level insights, and saves them as `thought` nodes.
- **Planning Loop**: Hierarchical decomposition (`plan.py:23-165`): wake-up time $\rightarrow$ daily plan $\rightarrow$ hourly schedule $\rightarrow$ 5-minute task breakdowns.
  - *Divergence*: Code contains `# TODO` in `plan.py:487-490`, copying static initial requirements rather than updating goals each morning.

#### Layer 3: Organizational Layer
- **Topology**: Completely flat, decentralized social graph.
- **Roles**: Handcrafted persona profiles defined in bootstrap files (`persona/personas/<name>/bootstrap_memory/scratch.json`).
- **Delegation**: No formal delegation, task assignment, or organizational authority exists. Information and plans spread organically through casual conversation.

#### Layer 4: Governance Layer
- **Mechanism**: **Zero Technical Governance**.
- **Enforcement**: Entirely dependent on natural language prompt compliance.
- **Sandboxing**: None. Python script executes with full operating system permissions.
- **Failure Handling**: Parsing errors fall back to raw string dumps or default idle states.

#### Layer 5: Simulation Layer
- **Clock & Stepping**: Discrete tick simulation (`reverie.py:74-84`). Time progresses in fixed steps: `sec_per_step = 10` seconds per tick.
- **Synchronization & IPC**: Single-threaded file-polling lockstep loop (`reverie.py:311-412`). The backend writes movement data to `storage/<sim>/movement/<step>.json` and halts in a `while True` loop waiting for the Django frontend browser to write `storage/<sim>/environment/<step>.json`.
- **Scaling Limit**: $O(N \cdot M)$ memory retrieval compute. With 25 agents, disk I/O bottlenecks and sequential API calls restrict simulation execution speed to a fraction of real time.

#### Layer 6: Communication Layer
- **Interaction Format**: Bilateral agent conversations (`converse.py:76-150`).
- **Modes**: `agent_chat_v1` (batch multi-turn generation) and `agent_chat_v2` (turn-by-turn role-swapping up to 8 turns).
- **Anti-Looping Buffer**: `plan.py:860-905` enforces an 800-tick (8,000 game seconds) conversational cooldown between identical agent pairs to prevent repetitive conversational lockups.

---

## 3. Anchor System 2: AI Hospital

### 3.1 Overview & Architectural Identity
- **Reference**: Fan et al. (arXiv:2402.09742, Feb 2024 / COLING 2025).
- **Codebase**: `LibertFan/AI_Hospital` (commit `870fc38`).
- **Core Paradigm**: Interactive multi-role clinical diagnostic simulation and benchmark for evaluating LLM doctors under realistic hospital constraints.

### 3.2 Layer-by-Layer Architectural Profile

#### Layer 1: Environment Layer
- **Domain World**: Outpatient hospital consultation room.
- **State Repository**: Real-world patient electronic medical records (`src/data/patients.json`, sourced from the Chinese `iiyi` medical dataset).
- **Tool / Database Grounding**: The Medical Examiner (`Reporter` agent, `src/agents/reporter.py:6-60`) serves as a deterministic oracle accessing ground-truth clinical examination results (`#查体#`, `#辅助检查#`).

#### Layer 2: Agent Cognition Layer
- **Agent Roles**: Specialized system prompts for:
  - `Doctor` (`src/agents/doctor.py`): Inquires symptoms, requests lab tests, produces structured diagnosis.
  - `Patient` (`src/agents/patient.py`): Answers questions based on medical profile (present illness, medical history, personal history).
  - `Reporter` (`src/agents/reporter.py`): Discloses objective examination findings.
  - `Host` (`src/agents/host.py`): Coordinates multi-doctor panels.
- **Diagnostic Parsing**: Doctor output is parsed via regular expressions (`doctor.py:82-95`) extracting `#症状#`, `#辅助检查#`, `#诊断结果#`, `#诊断依据#`, and `#治疗方案#`.

#### Layer 3: Organizational Layer
- **Consultation Modes**:
  1. `Single Consultation` (`src/hospital/consultation.py`): Triadic interaction between 1 Doctor, 1 Patient, and 1 Reporter.
  2. `Collaborative Consultation` (`src/hospital/collaborative_consultation.py`): Multi-doctor panel operating under `Parallel` (independent opinions aggregated by Host) or `Parallel_with_Critique` (doctors critique peers' diagnoses before Host synthesis).

#### Layer 4: Governance Layer
- **Information Disclosure Gate**: The patient is forbidden from directly revealing their disease diagnosis; only the Reporter can release objective lab findings when explicitly queried.
- **Routing Protocol**: Patient responses prepend destination tags (`<对医生讲>` or `<对检查员讲>`).
  - *Vulnerability*: `patient.py:76-78` implements a silent fallback defaulting to `"医生"` if the tag is missing, hiding prompt non-compliance.
- **Evaluation Gate**: Multi-View Medical Evaluation (MVME) pipeline (`src/evaluate/eval.py:13-80`) uses `gpt-4-1106-preview` as a structured judge evaluating 5 clinical rubrics (A/B/C/D).

#### Layer 5: Simulation Layer
- **Stepping Model**: Discrete conversational turns per consultation session.
- **Termination**: Session concludes when the Doctor outputs the structured diagnosis block or when the maximum turn threshold (default: 15 turns) is reached.
- **State Persistence**: Transcripts and intermediate diagnoses are recorded to JSONL files in `src/outputs/`.

#### Layer 6: Communication Layer
- **Routing**: Directed message exchange mediated by the scenario orchestrator (`Scenario.Consultation`).
- **Format**: Semi-structured natural language with XML-style role routing prefixes.

---

## 4. Anchor System 3: AgentVerse

### 4.1 Overview & Architectural Identity
- **Reference**: Chen et al. (ICLR 2024 / arXiv:2308.10848).
- **Codebase**: `OpenBMB/AgentVerse` (tag `v0.1.5`, commit `6d42bb6`).
- **Core Paradigm**: Flexible multi-agent framework featuring a 4-stage adaptive task-solving lifecycle and modular social simulation environments.

### 4.2 Layer-by-Layer Architectural Profile

#### Layer 1: Environment Layer
- **Dual Environments**:
  1. `Tasksolving Environment` (`agentverse/environments/tasksolving_env/`): Benchmark problem spaces (math, coding, logic).
  2. `Simulation Environment` (`agentverse/environments/simulation_env/`): 2D tile-world (`pokemon.py`), Game-theoretic arenas (`prisoner_dilemma.py`), and software teams (`sde_team.py`).
- **State & Memory**: Vector storage powered by ChromaDB (`agentverse/memory/vector.py`) alongside chronological text memory (`agentverse/memory/conversation.py`).

#### Layer 2: Agent Cognition Layer
- **LLM Abstraction**: Universal provider adapters (`agentverse/llms/`) supporting OpenAI, Anthropic Claude, and local open-source models via FastChat.
- **Memory Management**: Agents retrieve relevant prior dialogue turns and environment descriptions via semantic vector search or recency windows.

#### Layer 3: Organizational Layer (The 4-Stage Lifecycle)
- **Lifecycle Engine** (`agentverse/tasksolving.py:59-73`):
  1. **Stage 1: Dynamic Recruitment** (`role_assigner/role_description.py:1-90`): Generates custom agent personas and system prompts dynamically based on task descriptions.
  2. **Stage 2: Collaborative Decision Making** (`decision_maker/`): Executes multi-agent deliberation across 8 modular topologies:
     - `horizontal.py`: Equal peer-to-peer discussion.
     - `vertical.py`: Hierarchical manager-worker delegation.
     - `dynamic.py`: Contextual next-speaker selection.
     - `brainstorming.py`: Divergent idea generation.
     - `central.py`: Single leader broadcast.
     - `concurrent.py`: Independent parallel execution without communication.
     - `horizontal_tool.py`: Tool-augmented peer discussion.
     - `vertical_solver_first.py`: Solver drafts solution; critic reviews.
  3. **Stage 3: Action Execution** (`executor/`): Executes actions, invokes tools, or runs code.
  4. **Stage 4: Evaluation & Feedback** (`evaluator/`): Evaluates outputs and returns feedback.

#### Layer 4: Governance Layer
- **Closed-Loop Feedback Gate**: The Evaluator module (`evaluator/base.py`) grades candidate solutions. If the score falls below a success threshold, it outputs structured natural language `advice` and triggers a replanning or re-recruitment cycle.
- **Execution Limits**: Bounded by `max_rounds` parameter in configuration YAML.

#### Layer 5: Simulation Layer
- **Execution Loop**: Synchronous round-based progression.
- **Configuration Engine**: Declarative YAML files (`agentverse/initialization.py`) defining agents, environments, decision rules, and evaluation criteria.

#### Layer 6: Communication Layer
- **Message Abstraction**: Structured `Message` dataclass (`agentverse/message.py`) containing `content`, `sender`, `receiver`, and metadata.
- **Transmission**: Mediated by environment rule modules implementing broadcast, unicast, or filtered subscriptions.

---

## 5. Anchor System 4: ChatDev

### 5.1 Overview & Architectural Identity
- **Reference**: Qian et al. (ACL 2024 / arXiv:2307.07924).
- **Codebase**: `OpenBMB/ChatDev` (tag `v1.0.0`, commit `5defde31`).
- **Core Paradigm**: Communicative software development company executing sequential waterfall development through bilateral agent dialogue games.

### 5.2 Layer-by-Layer Architectural Profile

#### Layer 1: Environment Layer
- **Virtual Software Company**: Agents interact with file-based code stores (`chatdev/codes.py`) and documentation registries (`chatdev/documents.py`).
- **Execution Testing**: `chatdev/chat_env.py:107-157` (`exist_bugs`) executes generated software to verify whether syntax or runtime exceptions occur.
  - *Hazard*: Historical v1.0.0 executes code directly on the host machine using `subprocess.Popen("python main.py", shell=True)` without container sandboxing.

#### Layer 2: Agent Cognition Layer
- **Role Specialization**: Pre-configured corporate roles defined in `CompanyConfig/Default/RoleConfig.json` (Chief Executive Officer, Chief Product Officer, Chief Technology Officer, Programmer, Code Reviewer, Quality Assurance Tester).
- **Dialogue Framing**: Embedded CAMEL framework (`camel/agents/role_playing.py`) using inception prompts to ground agent personas.

#### Layer 3: Organizational Layer (Chat Chain Waterfall)
- **Pipeline Orchestrator** (`chatdev/chat_chain.py:22-120`):
  $$\text{Demand Analysis} \rightarrow \text{Language Choice} \rightarrow \text{Coding} \rightarrow \text{Code Complete} \rightarrow \text{Code Review} \rightarrow \text{Testing} \rightarrow \text{Manual}$$
- **Phase Abstraction**:
  - `SimplePhase` (`chatdev/phase.py`): Bilateral dialogue between two assigned roles (e.g., CEO and CPO).
  - `ComposedPhase` (`chatdev/composed_phase.py`): Looping sub-cycles (e.g., Programmer and Reviewer iterating until code passes review).

#### Layer 4: Governance Layer
- **Step Termination Protocol**: Prompts require agents to signal consensus by concluding utterances with `<INFO> <conclusion>` (`CompanyConfig/Default/PhaseConfig.json`). The engine detects `<INFO>` (`phase.py:143-155`) to break dialogue loops cleanly.
- **Communicative Dehallucination**: If agents fail to reach `<INFO>` consensus within `chat_turn_limit`, `phase.py:166-210` executes `self_reflection`, concatenating the conversation and forcing a single LLM call to extract the final artifact.

#### Layer 5: Simulation Layer
- **Execution Engine**: Synchronous waterfall pipeline.
- **Telemetry**: `chatdev/statistics.py` records token consumption, API calls, and cost accounting.

#### Layer 6: Communication Layer
- **Bilateral Communicative Inversion**: At each phase, one agent is designated `Instructor` and the other `Assistant`. They converse in turn-taking alternation until agreement is reached.

---

## 6. Anchor System 5: Evolving Orchestration / Puppeteer

### 6.1 Overview & Architectural Identity
- **Reference**: Dang, Qian et al. (NeurIPS 2025 / arXiv:2505.19591).
- **Codebase**: `OpenBMB/ChatDev` (branch `puppeteer`, commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a`).
- **Core Paradigm**: Dynamic multi-agent reasoning coordination governed by a centralized Reinforcement Learning policy network exploring an evolving reasoning graph.

### 6.2 Layer-by-Layer Architectural Profile

#### Layer 1: Environment Layer
- **Benchmark Arenas**: Integrated tasks across MMLU-Pro, GSM-Hard, Software Requirement Development Dataset (SRDD), and Creative Writing (`puppeteer/tasks/`).
- **Tool Suite**: Reasoning agents integrate external tools (`puppeteer/tools/`): `Web_Search`, `CodeInterpreter`, and `FileRead`.

#### Layer 2: Agent Cognition Layer
- **Puppet Agents**: Specialized tool-using reasoning agents (`puppeteer/agent/reasoning_agent.py:22-120`). Implements `_compress_data` (`reasoning_agent.py:100-140`) to summarize prior tool observations before passing into subsequent prompts.
- **State Representation**: `puppeteer/model/embedding.py` extracts dense token embeddings from the representation layer of `nvidia/Llama-3.1-Nemotron-70B-Reward` to encode evolving reasoning trajectories.

#### Layer 3: Organizational Layer (Learned Orchestrator)
- **Centralized Orchestrator**: The "Puppeteer" coordinates specialized worker agents ("puppets") across a dynamic reasoning graph (`puppeteer/inference/reasoning/reasoning.py:23-100`).
- **Parallel Search**: Explores up to `max_parallel_paths: 4` in parallel (`puppeteer/inference/reasoning/path.py:15-180`), stepping each path up to `max_step_num: 5` nodes.

#### Layer 4: Governance Layer
- **Policy Masking**: If tool access is disabled, Chroma search filters queries with `where={"category": "reasoning"}` (`reasoning_agent.py:76-80`), constraining agent selection to valid capabilities.
- **Step Bounding**: Hard limits on search depth and parallel branch count prevent runaway execution loops.

#### Layer 5: Simulation Layer
- **RL Policy Network**: 4-layer PyTorch MLP (`puppeteer/inference/policy/REINFORCE_continuous.py:17-41`):
  $$\text{Linear}(d_{in}, 512) \rightarrow \text{ReLU} \rightarrow \text{Linear}(512, 128) \rightarrow \text{ReLU} \rightarrow \text{Linear}(128, 32) \rightarrow \text{ReLU} \rightarrow \text{Linear}(32, d_{out}) \rightarrow \text{Softmax}$$
- **Policy Gradient Optimization**: Continuous REINFORCE with baseline subtraction and KL-divergence regularization (`REINFORCE_continuous.py:43-150`).

#### Layer 6: Communication Layer
- **Topology**: Hub-and-spoke star network. The centralized Puppeteer orchestrator selects the next puppet, dispatches context, receives the result, and computes the next transition.

---

## 7. Key Competing Systems Architectural Profiles

### 7.1 MetaGPT (SYS-06)
- **Reference**: Hong et al. (ICLR 2024 Oral / arXiv:2308.00352).
- **Core Innovation**: Standardized Operating Procedures (SOPs) with typed, schema-validated artifact handoffs (`metagpt/schema.py`).
- **Architectural Distinction**: Replaces unconstrained natural language chat with structured documents (PRDs, System Architecture Designs, Task Lists). Implements a pub/sub message bus (`metagpt/memory/`) where agents subscribe to specific document types, eliminating 80% of communication noise and token overhead.

### 7.2 Microsoft AutoGen (SYS-07)
- **Reference**: Wu et al. (arXiv:2308.08155); AutoGen v0.4 rewrite.
- **Core Innovation**: Conversable agent abstraction with flexible conversation programming.
- **Architectural Distinction**: v0.2 used a centralized `GroupChatManager` with dynamic LLM speaker selection, which suffered from speaker hijacking and infinite loops. v0.4 completely re-architected the system into an event-driven Actor Model (`autogen-core`) with asynchronous message passing, distributed runtime execution, and deterministic routing.

### 7.3 CAMEL (SYS-08)
- **Reference**: Li et al. (NeurIPS 2023 / arXiv:2303.17760).
- **Core Innovation**: Inception prompting and communicative bilateral role-playing games.
- **Architectural Distinction**: Formulates collaboration as a two-agent game where an AI Assistant and AI User guide each other toward task completion without human intervention.

### 7.4 DyLAN (SYS-09)
- **Reference**: Liu et al. (ICLR 2024 / arXiv:2310.02170).
- **Core Innovation**: Dynamic LLM-Agent Network using peer rating and unsupervised layer pruning.
- **Architectural Distinction**: Arranges agents into feed-forward layers (`LLMLP`). At each layer, agents rate peers' responses to compute an Agent Importance Score (AIS). Low-scoring agents are pruned in subsequent layers without requiring centralized RL training or reward models.

### 7.5 MemGPT / Letta (SYS-10)
- **Reference**: Packer et al. (arXiv:2310.08560).
- **Core Innovation**: LLM as Operating System; tiered virtual memory paging.
- **Architectural Distinction**: Treats the LLM context window as RAM and provides explicit function calls for agents to page memories between Core Memory (in-context), Recall Memory (FIFO event log), and Archival Memory (vector database). Solves Smallville's quadratic memory retrieval bottleneck.

### 7.6 Google DeepMind Concordia (SYS-11)
- **Reference**: Vezhnevets et al. (arXiv:2312.03664).
- **Core Innovation**: Game-master mediated generative social simulation.
- **Architectural Distinction**: Introduces a formal "Game Master" abstraction that mediates physical laws, social institutions, and environment transitions, separating environment physics from agent mental state.

---

## 8. Cross-System Architectural Comparison Matrix

| Architectural Dimension | Smallville (SYS-01) | AI Hospital (SYS-02) | AgentVerse (SYS-03) | ChatDev (SYS-04) | Puppeteer (SYS-05) | MetaGPT (SYS-06) |
|---|---|---|---|---|---|---|
| **Environment Substrate** | 2D tile grid matrix | Clinic EMR database | Pluggable (2D / task) | File store & host OS | Benchmarks & tools | Workspace filesystem |
| **Memory Architecture** | Associative `ConceptNode` stream | Dialogue history | Chroma vector & text | Dialogue history | Reward model embeddings | Global memory & document cache |
| **Retrieval Mechanism** | 3-factor rank decay (`gw=[0.5,3,2]`) | None (direct context) | Vector cosine similarity | None (direct context) | Trajectory vector dot product | Schema-filtered subscription |
| **Organizational Topology** | Flat emergent graph | Triad / Expert panel | 8 pluggable topologies | Waterfall Chat Chain | Dynamic RL reasoning graph | SOP artifact pipeline |
| **Role Assignment** | Static bootstrap JSON | Static clinical roles | Dynamic LLM recruitment | Static corporate roles | Dynamic learned selection | Static software roles |
| **Governance Engine** | None (prompt-only) | Role prefix `<对医生讲>` | Evaluator score & advice | `<INFO>` handshake token | Policy masking & step bounds | Pydantic schema validation |
| **Execution Sandboxing** | None (host execution) | None (API only) | None / Optional | Host shell (`subprocess`) | Local tool execution | Subprocess execution |
| **Simulation Clock** | Discrete 10s tick loop | Conversational turn | Round-based loop | Sequential phase loop | Graph search traversal | Asynchronous pipeline |
| **IPC / Synchronization** | File-polling lockstep | Scenario orchestrator | Python memory calls | Python memory calls | Python memory / PyTorch | Asyncio pub/sub bus |
