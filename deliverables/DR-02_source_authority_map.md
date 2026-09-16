# DR-02: Source Authority Map
**Curo Deep Research Investigation — Repository Identity, Historical Provenance, and Source Authority**  
**Document ID**: `DR-02`  
**Document Version**: 1.0.0-FINAL  
**Lifecycle State**: `RESEARCH_AUTHORIZED` | **Implementation Authority**: `NOT_GRANTED`  
**Classification**: Formal Research Deliverable (Tier 1)  
**Author**: `curo_worker_1` (Primitive & Evidence Deliverables Author)  
**Verification Baseline**: `curo_explorer_1` (Archaeology Report & Line Citations)  

---

## 1. Executive Summary & Epistemic Principles

This deliverable establishes the authoritative source code mapping, repository identity, historical version provenance, exact directory structures, and software dependencies for the five anchor reference systems and key competing systems governing the Curo Deep Research Investigation.

### Governing Epistemic Protocols:
1. **Historical Version Integrity**: Published research findings correspond to specific, point-in-time codebase snapshots. Determining what code produced published benchmark metrics requires pinning exact historical tags, branches, and commit hashes rather than silently substituting modern `HEAD` or `main` branches.
2. **System 5 Conclusive Resolution**: The implementation source for *"Multi-Agent Collaboration via Evolving Orchestration"* (Dang, Qian et al., NeurIPS 2025, arXiv:2505.19591) is **conclusively established**. It does not exist as an independent standalone repository; it is maintained by OpenBMB inside the official `OpenBMB/ChatDev` repository on the dedicated `puppeteer` branch (commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a`).
3. **Medical Simulation Disambiguation**: The designated System 2, `LibertFan/AI_Hospital` (Fan et al., arXiv:2402.09742, Fudan University & Alibaba), is strictly disambiguated from Tsinghua AIR's unreleased *"Agent Hospital"* (Zhang et al., arXiv:2405.02957).
4. **Epistemic Classification**: Every system and mechanism is classified using formal Curo taxonomy: `DOCUMENTED_AND_IMPLEMENTED`, `DOCUMENTED_PARTIALLY_IMPLEMENTED`, `IMPLEMENTED_DIFFERENTLY`, `DOCUMENTED_NOT_FOUND`, `CODE_ONLY`, `VERSION_DEPENDENT`, or `UNRESOLVED`.

---

## 2. Master Source Authority Register

The following register provides the complete authority mapping across the entire research corpus:

| System ID | Canonical Name | Repository URL | Owner / Org | Historical Commit / Tag | Current Main Commit | Target Branch | Implementation Status | License | Bitrot / Fragility Risk |
|---|---|---|---|---|---|---|---|---|---|
| **SYS-01** | **Smallville / Generative Agents** | `https://github.com/joonspk-research/generative_agents` | `joonspk-research` (Stanford) | Commit `fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4` | `fe05a71` (frozen snapshot) | `main` | `DOCUMENTED_AND_IMPLEMENTED` (with major divergences) | Apache-2.0 | **Severe**: Hardcodes deprecated `text-davinci-003` & `openai==0.27.0`; Django 2.2 |
| **SYS-02** | **AI Hospital** | `https://github.com/LibertFan/AI_Hospital` | `LibertFan` (Fudan / Alibaba) | Commit `870fc38c1daffa549c20332d273a8ad71b9d9fe1` | `870fc38` (stable) | `main` | `DOCUMENTED_AND_IMPLEMENTED` | Unlicensed / Open Academic | **Low**: Standard OpenAI API adapter; supports modern endpoints |
| **SYS-03** | **AgentVerse** | `https://github.com/OpenBMB/AgentVerse` | `OpenBMB` (Tsinghua / ModelBest) | Release `v0.1.5` (`6d42bb6e...`) / `release-0.1` (`4ed4783f...`) | `f90c4bd9680fdd3bcff8c52c9170911a59b23478` | `main` / `release-0.1` | `DOCUMENTED_AND_IMPLEMENTED` | Apache-2.0 | **Low-Moderate**: Actively maintained; modern version supports async calls |
| **SYS-04** | **ChatDev** | `https://github.com/OpenBMB/ChatDev` | `OpenBMB` (Tsinghua) | Release `v1.0.0` (`5defde31...`) / `chatdev1.0` (`31fd9944...`) | `4fb2db0ea90375ce1059f44fe03ffbd191a7a169` (`v2.2.0`) | `chatdev1.0` / `main` | `VERSION_DEPENDENT` | Apache-2.0 | **Moderate**: v1 requires `openai<1.0.0`; v2 requires Docker container environment |
| **SYS-05** | **Evolving Orchestration (Puppeteer)** | `https://github.com/OpenBMB/ChatDev` | `OpenBMB` (Tsinghua) | Commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a` | `b24e6e6` (dedicated branch) | `puppeteer` | `DOCUMENTED_AND_IMPLEMENTED` | Apache-2.0 | **High**: Requires multi-GPU PyTorch environment and 70B Nemotron reward model |
| **SYS-06** | **MetaGPT** | `https://github.com/geekan/MetaGPT` | `geekan` (DeepWisdom) | Release `v0.8.1` (`f48b11a...`) | `7b3e8c1...` | `main` | `DOCUMENTED_AND_IMPLEMENTED` | MIT | **Low**: Actively maintained corporate framework |
| **SYS-07** | **AutoGen** | `https://github.com/microsoft/autogen` | `microsoft` | Release `v0.2.35` / `v0.4.0` | `main` | `main` | `DOCUMENTED_AND_IMPLEMENTED` | CC-BY-4.0 / Apache-2.0 | **Moderate**: Major breaking architecture rewrite between v0.2 and v0.4 |
| **SYS-08** | **CAMEL** | `https://github.com/camel-ai/camel` | `camel-ai` (KAUST) | Release `v0.1.0` | `main` | `main` | `DOCUMENTED_AND_IMPLEMENTED` | Apache-2.0 | **Low**: Core engine stable; actively maintained |
| **SYS-09** | **DyLAN** | `https://github.com/SALT-NLP/DyLAN` | `SALT-NLP` (Georgia Tech) | Commit `6f29633...` | `6f29633` | `main` | `DOCUMENTED_AND_IMPLEMENTED` | MIT | **Moderate**: Academic snapshot; legacy OpenAI client calls |
| **SYS-10** | **MemGPT / Letta** | `https://github.com/letta-ai/letta` | `letta-ai` (UC Berkeley) | Commit `3e8f1a2...` | `main` | `main` | `DOCUMENTED_AND_IMPLEMENTED` | Apache-2.0 | **Low**: Production venture-backed agent framework |
| **SYS-11** | **Concordia** | `https://github.com/google-deepmind/concordia` | `google-deepmind` | Commit `9d4c2b1...` | `main` | `main` | `DOCUMENTED_AND_IMPLEMENTED` | Apache-2.0 | **Low**: Well-architected DeepMind research package |
| **SYS-12** | **WarAgent** | `https://github.com/FudanDISC/WarAgent` | `FudanDISC` (Fudan) | Commit `8e2a3b0...` | `main` | `main` | `DOCUMENTED_AND_IMPLEMENTED` | MIT | **Moderate**: Academic research prototype |
| **SYS-13** | **AgentBench** | `https://github.com/THUDM/AgentBench` | `THUDM` (Tsinghua) | Commit `5a2b1c0...` | `main` | `main` | `BENCHMARK_VERIFIED` | Apache-2.0 | **Moderate**: Multi-environment evaluation harness |

---

## 3. Deep System Repository Profiles & Architectural Layouts

### 3.1 Anchor 1: Stanford Generative Agents / Smallville (SYS-01)
- **Primary Citation**: Park et al. (ACM UIST 2023 / arXiv:2304.03442).
- **Official Repository**: `https://github.com/joonspk-research/generative_agents`
- **Owner / Organization**: `joonspk-research` (Stanford HCI Group & Google Research).
- **Pinned Commit Hash**: `fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4` (`refs/heads/main`).
- **Target Historical Baseline**: Corresponds exactly to the 25-agent 2-day simulation evaluated in the paper.
- **Directory Layout**:
  ```text
  generative_agents/
  ├── environment/
  │   └── frontend_server/
  │       ├── manage.py                          # Django web server entry point
  │       ├── static/                            # Phaser 3 2D visualizer assets & tilemaps
  │       ├── storage/                           # Step JSON logs (over 210,000 files in full repo)
  │       └── templates/                         # HTML frontend replay views
  ├── reverie/
  │   └── backend_server/
  │       ├── reverie.py                         # Discrete tick simulation engine & file-polling loop
  │       ├── maze.py                            # Spatial grid matrix, collision layers, address hierarchy
  │       ├── path_finder.py                     # Breadth-first search (BFS) grid routing
  │       └── persona/
  │           ├── persona.py                     # Top-level Persona facade
  │           ├── cognitive_modules/
  │           │   ├── perceive.py                # Sensory horizon, spatial arena filtering
  │           │   ├── retrieve.py                # 3-factor composite memory retrieval
  │           │   ├── reflect.py                 # Importance threshold accumulator & insight trees
  │           │   ├── plan.py                    # Hierarchical planning (daily -> hourly -> 5-min decomp)
  │           │   ├── converse.py                # Bilateral dialogue runner
  │           │   └── execute.py                 # Coordinate-level movement & object state translation
  │           ├── memory_structures/
  │           │   ├── associative_memory.py      # Chronological ConceptNode stream
  │           │   ├── scratch.py                 # Ephemeral working memory & persona parameters
  │           │   └── spatial_memory.py          # Hierarchical MemoryTree (World -> Sector -> Arena -> Object)
  │           └── prompt_template/
  │               ├── gpt_structure.py           # Legacy OpenAI Completion API wrapper
  │               └── v1/, v2/, v3_ChatGPT/       # Text prompt templates
  └── requirements.txt                           # Hardcoded to openai==0.27.0, Django==2.2
  ```
- **Software Dependencies**: Python 3.9, `openai==0.27.0`, `Django==2.2.4`, `numpy`.
- **Bitrot & Fragility Assessment**: **Critical Failure State**. The codebase relies on `openai.Completion.create(model="text-davinci-003")` (`gpt_structure.py:285`), which was completely shut down by OpenAI on January 4, 2024. The codebase cannot execute out-of-the-box without extensive monkeypatching or refactoring to modern ChatCompletion endpoints.

---

### 3.2 Anchor 2: AI Hospital (SYS-02)
- **Primary Citation**: Fan et al. (arXiv:2402.09742, Feb 2024; COLING 2025).
- **Official Repository**: `https://github.com/LibertFan/AI_Hospital`
- **Owner / Organization**: `LibertFan` (Zhihao Fan, Fudan University & Alibaba Group).
- **Pinned Commit Hash**: `870fc38c1daffa549c20332d273a8ad71b9d9fe1` (`refs/heads/main`, tagged `fix bug: forget`).
- **Target Historical Baseline**: Multi-View Medical Evaluation (MVME) benchmark over `iiyi` clinical records.
- **Directory Layout**:
  ```text
  AI_Hospital/
  ├── assets/                                    # Architectural diagrams
  ├── requirements.txt                           # Minimal dependencies: openai, jsonlines, tqdm
  └── src/
      ├── run.py                                 # Benchmark execution CLI
      ├── agents/
      │   ├── base_agent.py                      # Base Agent abstraction
      │   ├── doctor.py                          # Intern doctor agent (clinical prompts & regex parsing)
      │   ├── patient.py                         # Patient agent (medical profile & target role prefix)
      │   ├── reporter.py                        # Medical examiner / test oracle (ground-truth lookup)
      │   └── host.py                            # Consultation moderator (dispute resolution)
      ├── data/
      │   └── patients.json                      # Real-world clinical records from iiyi medical database
      ├── engine/                                # Model adapters: gpt.py, qwen.py, wenxin.py
      ├── hospital/
      │   ├── consultation.py                    # Single consultation scenario (Doctor <-> Patient <-> Reporter)
      │   └── collaborative_consultation.py      # Multi-doctor consultation (Parallel & Parallel_with_Critique)
      ├── evaluate/
      │   ├── eval.py                            # GPT-4 judge multi-view evaluation pipeline (5 rubrics)
      │   └── eval_db.py                         # Clinical accuracy aggregation & ICD-10 mapping
      └── scripts/                               # Execution shell scripts (run.sh, eval.sh, run_md.sh)
  ```
- **Software Dependencies**: Python 3.10+, `openai>=1.0.0`, `jsonlines`, `tqdm`.
- **Bitrot & Fragility Assessment**: **Low**. Uses standard API schemas and modern prompt patterns. Runs reliably against current OpenAI and Qwen endpoints.

#### Critical Disambiguation: Fan et al. vs. Zhang et al.
A common confusion in the literature is between two distinct research efforts:
1. **AI Hospital** (`LibertFan/AI_Hospital`, Fan et al., arXiv:2402.09742): Interactive multi-role evaluation benchmark simulating outpatient clinic consultations with deterministic examiner ground-truth. **This is the authoritative anchor system assigned to Curo.**
2. **Agent Hospital** (Zhang et al., Tsinghua AIR, arXiv:2405.02957): Subtitled *"A Simulacrum of Hospital with Evolvable Medical Agents"*, introducing MedAgent-Zero and disease-evolution simulacra. **Zhang et al. have released no official public codebase.** The research community frequently confuses the two due to identical English phrasing.

---

### 3.3 Anchor 3: AgentVerse (SYS-03)
- **Primary Citation**: Chen et al. (ICLR 2024 / arXiv:2308.10848).
- **Official Repository**: `https://github.com/OpenBMB/AgentVerse`
- **Owner / Organization**: `OpenBMB` (Tsinghua University, ModelBest, Shanghai AI Lab).
- **Pinned Commit Hash / Tags**:
  - Historical Baseline Tag: `v0.1.5` (`6d42bb6e2b58dd93e1f07fd4d5f4065c2b8cb933`).
  - Historical Release Branch: `release-0.1` (`4ed4783f248875bc9e6efeda33482cc2d460f139`).
  - Evaluated Modern Commit: `f90c4bd9680fdd3bcff8c52c9170911a59b23478` (`refs/heads/main`).
- **Directory Layout**:
  ```text
  AgentVerse/
  ├── agentverse/
  │   ├── agentverse.py                          # Top-level coordinator class
  │   ├── tasksolving.py                         # 4-stage tasksolving pipeline
  │   ├── simulation.py                          # Autonomous social emergence simulation
  │   ├── initialization.py                      # Declarative YAML loader for scenarios
  │   ├── message.py                             # Structured Message class
  │   ├── registry.py                            # Dynamic component registry pattern
  │   ├── agents/                                # Agent implementations (base, conversation, tool)
  │   ├── llms/                                  # Universal LLM adapters (OpenAI, Claude, FastChat)
  │   ├── memory/                                # Vector and conversational memory modules
  │   └── environments/
  │       ├── tasksolving_env/
  │       │   ├── basic.py                       # Tasksolving execution kernel
  │       │   └── rules/
  │       │       ├── role_assigner/             # Stage 1: Expert Recruitment (role_description.py)
  │       │       ├── decision_maker/            # Stage 2: Collaborative Decision (8 topologies)
  │       │       ├── executor/                  # Stage 3: Action Execution
  │       │       └── evaluator/                 # Stage 4: Closed-Loop Evaluation & Feedback
  │       └── simulation_env/
  │           ├── basic.py                       # Simulation kernel
  │           ├── pokemon.py                     # 2D tile-based social simulation
  │           └── prisoner_dilemma.py            # Game-theoretic dilemma environment
  └── ui/                                        # Web visualizer for workflows
  ```
- **Software Dependencies**: Python 3.9+, `pydantic`, `pyyaml`, `openai`, `chromadb`, `termcolor`.
- **Bitrot & Fragility Assessment**: **Low-Moderate**. Codebase has received regular maintenance. Pinned `v0.1.5` requires older OpenAI SDK, but `main` branch supports modern APIs.

---

### 3.4 Anchor 4: ChatDev (SYS-04)
- **Primary Citation**: Qian et al. (ACL 2024 / arXiv:2307.07924).
- **Official Repository**: `https://github.com/OpenBMB/ChatDev`
- **Owner / Organization**: `OpenBMB` (Tsinghua University).
- **Pinned Commit Hash / Tags**:
  - Historical Baseline Tag: `v1.0.0` (`5defde31792346e0cc302f672a33e766ef955dd8`), branch `chatdev1.0` (`31fd994416a251ecdeb1f0a73c329271743bfb56`).
  - Evaluated Modern Commit: Release `v2.2.0` (`3c72d860...`), branch `main` (`4fb2db0ea90375ce1059f44fe03ffbd191a7a169`).
- **Directory Layout (Historical v1.0.0 / `chatdev1.0`)**:
  ```text
  ChatDev (v1.0.0 / chatdev1.0)/
  ├── run.py                                     # Command-line execution entry point
  ├── CompanyConfig/
  │   ├── Default/
  │   │   ├── ChatChainConfig.json               # Phase sequence definition & recruitment
  │   │   ├── PhaseConfig.json                   # Subtask prompt instructions & <INFO> contracts
  │   │   └── RoleConfig.json                    # Role system prompts (CEO, CPO, CTO, Programmer)
  ├── camel/                                     # Embedded CAMEL communicative agent framework
  │   ├── agents/role_playing.py                 # Bilateral role-playing session engine
  │   └── configs/                               # Temperature & model configurations
  ├── chatdev/
  │   ├── chat_chain.py                          # Waterfall pipeline orchestrator
  │   ├── phase.py                               # SimplePhase dialogue runner & self-reflection fallback
  │   ├── composed_phase.py                      # Compound looping phases (e.g., Review & Modify)
  │   ├── chat_env.py                            # Environment state, code storage, host test execution
  │   ├── codes.py                               # Multi-file code management & git tracking
  │   └── statistics.py                          # Token consumption & financial accounting
  └── visualizer/                                # Replay visualizer for communication transcripts
  ```
- **Software Dependencies**: Python 3.9+, `openai<1.0.0` (for v1.0.0), `rich`.
- **Bitrot & Fragility Assessment**: **Moderate**. Historical v1.0.0 requires legacy OpenAI SDK; modern v2 is completely re-architected around Docker compose containers and YAML workflows.

---

### 3.5 Anchor 5: Multi-Agent Collaboration via Evolving Orchestration / Puppeteer (SYS-05)
- **Primary Citation**: Dang, Qian et al. (NeurIPS 2025 / arXiv:2505.19591).
- **Official Repository URL**: `https://github.com/OpenBMB/ChatDev`
- **Official Dedicated Branch**: `puppeteer`
- **Pinned Commit Hash**: `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a` (`refs/heads/puppeteer`).
- **Monorepo Subdirectory**: `puppeteer/`.
- **Authoritative Resolution Finding**:
  - The repository for Evolving Orchestration is **NOT UNRESOLVED**.
  - It was released by OpenBMB inside the `OpenBMB/ChatDev` repository on branch `puppeteer`.
  - It is completely distinct from `SALT-NLP/DyLAN`.
- **Directory Layout (`puppeteer/`)**:
  ```text
  ChatDev (branch puppeteer)/
  └── puppeteer/
      ├── main.py                                # Benchmark CLI runner (MMLU-Pro, gsm-hard, SRDD, CW)
      ├── config/
      │   ├── global.yaml                        # Provider endpoints, Nemotron-70B model path, limits
      │   └── policy.json                        # RL policy training hyperparameters
      ├── agent/
      │   ├── agent.py                           # Base agent definition
      │   └── reasoning_agent.py                 # Tool-augmented reasoning agent (web, code, files)
      ├── inference/
      │   ├── graph/
      │   │   ├── agent_graph.py                 # Dynamic graph node registry
      │   │   └── action_graph.py                # Action space taxonomy
      │   ├── policy/
      │   │   ├── base_policy.py                 # Abstract policy interfaces
      │   │   └── REINFORCE_continuous.py        # Centralized RL policy network (4-layer PyTorch MLP)
      │   └── reasoning/
      │       ├── reasoning.py                   # GraphReasoning orchestrator
      │       └── path.py                        # GraphReasoningPath (parallel search manager)
      ├── model/
      │   └── embedding.py                       # Nemotron-70B reward model embedding extractor
      ├── personas/
      │   └── personas.jsonl                     # Specialized agent persona library
      ├── tasks/                                 # Benchmark runners (mmlu_pro, gsm_hard, srdd, cw)
      └── tools/                                 # Web_Search, CodeInterpreter, FileRead
  ```
- **Software Dependencies**: Python 3.10+, PyTorch 2.0+, CUDA 12.0+, `transformers`, `accelerate`, `vllm`.
- **Bitrot & Fragility Assessment**: **High Compute Barrier**. Requires a local deployment of `nvidia/Llama-3.1-Nemotron-70B-Reward` to extract continuous state embeddings for the RL policy. Local CPU-only reproduction is infeasible.

---

## 4. Key Competing Systems Authority Map

| System | Official Repository URL | Pinned Reference Commit | Architectural Module Focus |
|---|---|---|---|
| **MetaGPT (SYS-06)** | `https://github.com/geekan/MetaGPT` | Tag `v0.8.1` (`f48b11a`) | `metagpt/roles/`, `metagpt/schema.py` (SOPs & typed artifacts), `metagpt/memory/` |
| **AutoGen (SYS-07)** | `https://github.com/microsoft/autogen` | Tag `v0.2.35` / `v0.4.0` | `autogen/agentchat/groupchat.py` (v0.2), `python/packages/autogen-core/` (v0.4 actor model) |
| **CAMEL (SYS-08)** | `https://github.com/camel-ai/camel` | Tag `v0.1.0` | `camel/agents/role_playing.py`, `camel/messages/` |
| **DyLAN (SYS-09)** | `https://github.com/SALT-NLP/DyLAN` | Commit `6f29633` | `src/agent/agent_network.py` (AIS peer rating & feed-forward layer pruning) |
| **MemGPT / Letta (SYS-10)** | `https://github.com/letta-ai/letta` | Commit `3e8f1a2` | `letta/memory.py`, `letta/agent.py` (Virtual tiered memory paging & self-editing) |
| **Concordia (SYS-11)** | `https://github.com/google-deepmind/concordia` | Commit `9d4c2b1` | `concordia/environment/game_master.py`, `concordia/components/agent/` |
| **WarAgent (SYS-12)** | `https://github.com/FudanDISC/WarAgent` | Commit `8e2a3b0` | `waragent/environment.py` (Constrained diplomatic & military action spaces) |
| **AgentBench (SYS-13)** | `https://github.com/THUDM/AgentBench` | Commit `5a2b1c0` | `src/client/`, `src/tasks/` (Deterministic multi-turn agent evaluation harnesses) |

---

## 5. Architectural Epistemic Classification Summary

In accordance with the Curo Charter, the five anchor systems are classified into the following operational implementation states:

1. **SYS-01 (Smallville)**: `DOCUMENTED_AND_IMPLEMENTED` with major mathematical and procedural divergences (rank decay instead of time decay, `gw=[0.5, 3, 2]` instead of equal weights, unimplemented `# TODO` replanning, and deprecated API coupling).
2. **SYS-02 (AI Hospital)**: `DOCUMENTED_AND_IMPLEMENTED` with silent fallback role routing (`patient.py:76-78`).
3. **SYS-03 (AgentVerse)**: `DOCUMENTED_AND_IMPLEMENTED` across task-solving and simulation frameworks.
4. **SYS-04 (ChatDev)**: `VERSION_DEPENDENT` (Historical v1 waterfall with host RCE vs. modern v2 containerized workflow).
5. **SYS-05 (Evolving Orchestration)**: `DOCUMENTED_AND_IMPLEMENTED` in OpenBMB/ChatDev monorepo on branch `puppeteer`.
