# Reference Corpus Archaeology & Implementation Source Mapping Report (R1)
**Curo Deep Research Investigation — Reference Corpus Mapping & Spec Mining**  
**Document Version**: 1.0.0-FINAL  
**Author**: `curo_explorer_1` (Repository Archaeologist & Spec Miner)  
**Lifecycle State**: `RESEARCH_AUTHORIZED` | **Implementation Authority**: `NOT_GRANTED`  
**Date**: 2026-09-15  
**Working Directory**: `E:\projects\simlab\.agents\curo_explorer_1`

---

## 1. Executive Summary & Corpus Authority Map (DR-02)

This report establishes the authoritative implementation mapping, repository identity, historical version provenance, exact code directory layout, file paths, line numbers, paper-to-code divergences, and formal mechanism classifications for the **Five Anchor Reference Systems** governing the Curo Deep Research Investigation.

In accordance with the governing research directives:
1. **Historical Version Integrity**: Historical versions corresponding to published empirical results are prioritized and distinguished from modern `HEAD`/`main` branches.
2. **System 5 Resolution**: The implementation source for *"Multi-Agent Collaboration via Evolving Orchestration"* has been **conclusively resolved**. It is hosted in the official `OpenBMB/ChatDev` repository on the dedicated branch `puppeteer` (commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a`). It is **NOT UNRESOLVED**, and it is distinct from the related dynamic network framework DyLAN (`SALT-NLP/DyLAN`, Liu et al., ICLR 2024).
3. **Medical Simulation Disambiguation**: The designated System 2, `LibertFan/AI_Hospital` (commit `870fc38c1daffa549c20332d273a8ad71b9d9fe1`), corresponds to Fan et al. (arXiv:2402.09742, Feb 2024), *"AI Hospital: Interactive Evaluation and Collaboration of Large Language Models as Intern Doctors for Clinical Diagnosis"*. It is rigorously distinguished from Zhang et al. (arXiv:2405.02957, May 2024), *"Agent Hospital: A Simulacrum of Hospital with Evolvable Medical Agents"*, which has no public code repository released.
4. **Epistemic Discipline**: Every mechanism is assigned one of seven formal classification states: `DOCUMENTED_AND_IMPLEMENTED`, `DOCUMENTED_PARTIALLY_IMPLEMENTED`, `IMPLEMENTED_DIFFERENTLY`, `DOCUMENTED_NOT_FOUND`, `CODE_ONLY`, `VERSION_DEPENDENT`, or `UNRESOLVED`.

### Master Anchor Authority Register

| # | System Name | Canonical Primary Paper Citation | Authoritative Repository URL | Canonical Org / Owner | Historical Target (Paper Results) | Evaluated HEAD Commit | Implementation Status |
|---|-------------|----------------------------------|------------------------------|-----------------------|-----------------------------------|-----------------------|-----------------------|
| **1** | **Generative Agents / Smallville** | Park et al. (Oct 2023), *Generative Agents: Interactive Simulacra of Human Behavior*, ACM UIST '23 / arXiv:2304.03442 | `https://github.com/joonspk-research/generative_agents` | `joonspk-research` (Stanford / Google) | Commit `fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4` (branch `main`) | `fe05a71` (repo frozen since release) | `DOCUMENTED_AND_IMPLEMENTED` (with major algorithmic divergences) |
| **2** | **AI Hospital** (Assigned as Agent Hospital) | Fan et al. (Feb 2024), *AI Hospital: Interactive Evaluation and Collaboration of LLMs as Intern Doctors for Clinical Diagnosis*, arXiv:2402.09742 | `https://github.com/LibertFan/AI_Hospital` | `LibertFan` (Fudan University & Alibaba Group) | Commit `870fc38c1daffa549c20332d273a8ad71b9d9fe1` (branch `main`) | `870fc38` | `DOCUMENTED_AND_IMPLEMENTED` |
| **3** | **AgentVerse** | Chen et al. (May 2024), *AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors*, ICLR 2024 / arXiv:2308.10848 | `https://github.com/OpenBMB/AgentVerse` | `OpenBMB` (Tsinghua University / ModelBest) | Release Tag `v0.1.5` (`6d42bb6e...`) / branch `release-0.1` (`4ed4783f...`) | `f90c4bd9680fdd3bcff8c52c9170911a59b23478` (`main`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **4** | **ChatDev** | Qian et al. (Aug 2024), *Communicative Agents for Software Development*, ACL 2024 / arXiv:2307.07924 | `https://github.com/OpenBMB/ChatDev` | `OpenBMB` (Tsinghua University) | Release Tag `v1.0.0` (`5defde31...`) / branch `chatdev1.0` (`31fd9944...`) | `4fb2db0ea90375ce1059f44fe03ffbd191a7a169` (`main` v2.2.0) | `VERSION_DEPENDENT` (v1 waterfall vs v2 workflow) |
| **5** | **Multi-Agent Collaboration via Evolving Orchestration** | Dang, Qian et al. (Dec 2025), *Multi-Agent Collaboration via Evolving Orchestration*, NeurIPS 2025 / arXiv:2505.19591 | `https://github.com/OpenBMB/ChatDev` (branch `puppeteer`) | `OpenBMB` / Tsinghua University | Branch `puppeteer`, commit `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a` | `b24e6e6` | `DOCUMENTED_AND_IMPLEMENTED` (in ChatDev monorepo) |

---

## 2. System 1: Stanford Generative Agents / Smallville

### 2.1 Repository Identity & Version Provenance
- **Primary Paper**: Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. In *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23)*, October 29–November 1, 2023, San Francisco, CA. DOI: [10.1145/3586183.3606763](https://doi.org/10.1145/3586183.3606763). arXiv: [2304.03442](https://arxiv.org/abs/2304.03442).
- **Authoritative Repository**: `https://github.com/joonspk-research/generative_agents`
- **Canonical Organization**: `joonspk-research`
- **Historical Commit**: `fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4` (branch `main`). The repository is effectively an archival snapshot; no subsequent tags or active release branches exist.
- **License**: Apache-2.0.

### 2.2 Directory Layout & Key Modules
```text
generative_agents/
├── environment/
│   └── frontend_server/
│       ├── manage.py                          # Django server management script
│       ├── static/                            # Phaser 3 visualizer assets, sprites, tilemaps
│       ├── storage/                           # Historical simulation step JSON logs
│       └── templates/                         # HTML replay views (demo.html, main_script.html)
├── reverie/
│   └── backend_server/
│       ├── reverie.py                         # Discrete tick simulation engine & file-polling IPC
│       ├── maze.py                            # 2D grid matrix parser, collision layer, address tree
│       ├── path_finder.py                     # Unoptimized BFS flood-fill grid routing
│       ├── global_methods.py                  # Helper functions for filesystem persistence & math
│       └── persona/
│           ├── persona.py                     # Central Persona facade class
│           ├── cognitive_modules/
│           │   ├── perceive.py                # Sensory horizon, arena filtering, poignancy scoring
│           │   ├── retrieve.py                # 3-factor composite memory retrieval
│           │   ├── reflect.py                 # Importance threshold accumulator & insight trees
│           │   ├── plan.py                    # Hierarchical planning (daily -> hourly -> 5-min decomp)
│           │   ├── converse.py                # Bilateral agent dialogue loops (v1 batch & v2 iterative)
│           │   └── execute.py                 # Grounding LLM intent into maze coordinate actions
│           ├── memory_structures/
│           │   ├── associative_memory.py      # Chronological ConceptNode stream & embedding index
│           │   ├── scratch.py                 # Ephemeral working memory, identity, daily requirements
│           │   └── spatial_memory.py          # MemoryTree 4-level spatial mental map
│           └── prompt_template/
│               ├── gpt_structure.py           # Legacy OpenAI SDK wrapper & string interpolation
│               └── v1/, v2/, v3_ChatGPT/       # Raw prompt template text files
└── requirements.txt                           # Hardcoded to openai==0.27.0, Django==2.2
```

### 2.3 Mechanism Deconstruction & Exact Line Citations
1. **Associative Memory Stream (`ConceptNode`)**:
   - Class definition: `reverie/backend_server/persona/memory_structures/associative_memory.py:19-48`.
   - Node schema: `node_id`, `node_type` (`event`, `thought`, `chat`), `depth`, `created`, `expiration`, `last_accessed`, `subject`, `predicate`, `object`, `description`, `embedding_key`, `poignancy`, `keywords`, `filling`.
   - Evidence pointers: `associative_memory.py:207-212`. For `thought` nodes, `filling` stores a list of supporting observation/thought `node_id`s, and `depth = 1 + max(parent depths)`.
2. **Memory Retrieval Scoring & Rank Decay**:
   - Core scoring function: `reverie/backend_server/persona/cognitive_modules/retrieve.py:199-271` (`new_retrieve`).
   - Divergence in Recency: `retrieve.py:145-146`. Formula implemented is $\text{recency} = 0.99^i$, where $i$ is chronological list position rank ($1 \dots |M|$), **not** game hours passed ($0.995^{\Delta t_{hours}}$) as published in paper §4.1.
   - Divergence in Weights: `retrieve.py:244-250`. Global multiplier vector `gw = [0.5, 3, 2]` multiplies recency, relevance, and importance. Published paper claimed equal weights ($\alpha_r = \alpha_i = \alpha_{rel} = 1$). Relevance is weighted 6x higher than recency in code.
   - Min-Max Normalization: `retrieve.py:70-104` (`normalize_dict_floats`).
3. **Reflection Subsystem & Importance Accumulator**:
   - Accumulator initialization: `reverie/backend_server/persona/memory_structures/scratch.py:61-62` (`importance_trigger_max = 150`, `importance_trigger_curr = 150`).
   - Trigger decrement: `reverie/backend_server/persona/cognitive_modules/reflect.py:149-170`. Each perceived event decrements the counter by its LLM-judged poignancy ($1 \dots 10$). When `importance_trigger_curr <= 0`, reflection fires and resets to 150.
   - Reflection generation: `reflect.py:99-134` (`run_reflect`). Queries LLM for 3 focal questions (`generate_focal_pt_v1.txt`), retrieves top 30 nodes per question, queries LLM for 5 high-level insights with evidence citations (`insight_and_evidence_v1.txt`), parses citations into `thought` nodes.
4. **Hierarchical Planning**:
   - Decompositions: `reverie/backend_server/persona/cognitive_modules/plan.py:23-165`. Generates wake-up hour (`generate_wake_up_hour`), broad daily schedule (`generate_first_daily_plan`), hourly schedule (`generate_hourly_schedule`), and sub-hourly tasks (`generate_task_decomp`).
   - Incomplete Replanning Bug: `plan.py:487-490`. In `_long_term_planning`, the new-day branch explicitly has `# TODO` and recycles static initial daily requirements: `persona.scratch.daily_req = persona.scratch.daily_req`. Daily replanning from accumulated memories was never completed.
5. **Dialogue & Synchronization**:
   - Dialogue loops: `reverie/backend_server/persona/cognitive_modules/converse.py:76-150`. Implements `agent_chat_v1` (batch script) and `agent_chat_v2` (iterative turn-by-turn swapping roles up to 8 turns).
   - Cooldown buffer: `plan.py:860-905`. Sets `chatting_with_buffer = 800` simulation ticks (8,000 game seconds / 2.22 game hours) to prevent endless conversational loops.
6. **Simulation Engine & Lockstep File IPC**:
   - Discrete clock: `reverie/backend_server/reverie.py:74-84`. `sec_per_step = 10` seconds per tick.
   - Lockstep File Polling: `reverie.py:311-412`. Backend writes agent movement to `storage/<sim_code>/movement/<step>.json`; loops while waiting for frontend browser to write `storage/<sim_code>/environment/<step>.json`. Introduced severe disk I/O bottlenecks and race conditions.
7. **Model API Coupling**:
   - Model client: `reverie/backend_server/persona/prompt_template/gpt_structure.py:211-220, 285`. Hardcodes `openai.Completion.create` with `model="text-davinci-003"` (deactivated by OpenAI on January 4, 2024).

---

## 3. System 2: Agent Hospital (`LibertFan/AI_Hospital`)

### 3.1 Repository Identity & Critical Disambiguation
- **Primary Paper**: Fan, Z., Tang, J., Chen, W., Wang, S., Wei, Z., Xi, J., Huang, F., & Zhou, J. (2024). *AI Hospital: Interactive Evaluation and Collaboration of LLMs as Intern Doctors for Clinical Diagnosis*. arXiv: [2402.09742](https://arxiv.org/abs/2402.09742) [cs.CL] (February 14, 2024).
- **Authoritative Repository**: `https://github.com/LibertFan/AI_Hospital`
- **Canonical Organization / Owner**: `LibertFan` (Zhihao Fan, School of Computer Science, Fudan University & Alibaba Group).
- **Historical Commit**: `870fc38c1daffa549c20332d273a8ad71b9d9fe1` (September 13, 2024, tagged `fix bug: forget`).
- **Critical Disambiguation**: In the literature, two separate papers bear the title or moniker "Agent Hospital":
  1. **AI Hospital** (`LibertFan/AI_Hospital`, arXiv:2402.09742, Fan et al., Fudan/Alibaba): Focuses on interactive multi-role clinical diagnosis (Doctor, Patient, Medical Examiner, Host) and the Multi-View Medical Evaluation (MVME) benchmark. **This is the codebase designated by the user dispatch.**
  2. **Agent Hospital** (arXiv:2405.02957, Zhang et al., Tsinghua University AIR): Subtitled *"A Simulacrum of Hospital with Evolvable Medical Agents"* (introducing SEAL and MedAgent-Zero). **This paper has released no official public codebase.**

### 3.2 Directory Layout & Key Modules
```text
AI_Hospital/
├── assets/                                    # Architectural workflow diagrams
├── requirements.txt                           # Minimal dependencies: openai, jsonlines, tqdm
└── src/
    ├── run.py                                 # Main execution entry point
    ├── agents/
    │   ├── base_agent.py                      # Abstract Base Agent class
    │   ├── doctor.py                          # Intern doctor agent (system prompts & regex parsing)
    │   ├── patient.py                         # Patient agent (medical history & target role tagging)
    │   ├── reporter.py                        # Medical examiner / test database administrator
    │   └── host.py                            # Consultation moderator (manages doctor debates)
    ├── data/
    │   └── patients.json                      # Sourced medical records from iiyi clinical dataset
    ├── engine/                                # Provider adapters: gpt.py, qwen.py, wenxin.py, etc.
    ├── hospital/
    │   ├── consultation.py                    # Single doctor-patient consultation scenario
    │   └── collaborative_consultation.py      # Multi-doctor consultation & dispute resolution
    ├── evaluate/
    │   ├── eval.py                            # GPT-4 judge multi-view evaluation pipeline
    │   └── eval_db.py                         # Accuracy aggregation & ICD-10 clinical evaluation
    ├── outputs/                               # Recorded evaluation JSONL logs
    ├── scripts/                               # Shell scripts: run.sh, eval.sh, run_md.sh
    └── utils/                                 # Class registry and logging utilities
```

### 3.3 Mechanism Deconstruction & Exact Line Citations
1. **Multi-Role Clinical Interaction Architecture**:
   - Single Doctor Consultation: `src/hospital/consultation.py:14-167` (`Scenario.Consultation`).
   - Doctor Agent: `src/agents/doctor.py:10-95`. System prompt instructs doctor not to diagnose prematurely, ask one short question at a time, order examinations, and provide structured diagnosis (`#症状#`, `#辅助检查#`, `#诊断结果#`, `#诊断依据#`, `#治疗方案#`).
   - Structured Regex Parsing: `doctor.py:82-95` (`parse_diagnosis`). Extracts clinical sections via regular expressions (`\#{}\#(.*?)\n\#`).
   - Patient Agent: `src/agents/patient.py:5-82` (`Agent.Patient.GPT`). System prompt injects profile, present illness (`现病史`), past history (`既往史`), personal history (`个人史`).
   - Role Addressing Protocol: `patient.py:68-82` (`parse_role_content`). Patient parses destination prefix: `<对医生讲>` routes utterance to Doctor; `<对检查员讲>` routes to Reporter.
   - Fallback Shortcut: `patient.py:76-78`. If patient prompt forgets prefix, code silently falls back to Doctor rather than throwing an error or enforcing schema compliance.
2. **Medical Examiner / Database Admin (`Reporter`)**:
   - Class definition: `src/agents/reporter.py:6-60` (`Agent.Reporter.GPT`).
   - Grounded Test Disclosure: `reporter.py:40-58` (`speak`). When patient or doctor requests an examination, reporter searches the patient's ground-truth record for `#查体#` and `#辅助检查#`. If not found, returns `"- xxx: 无异常"`.
3. **Multi-Doctor Collaborative Consultation & Dispute Resolution**:
   - Orchestrator: `src/hospital/collaborative_consultation.py:14-192` (`Scenario.CollaborativeConsultation`).
   - Discussion Modes: Line 74 exposes two modes: `Parallel` (independent opinions aggregated by host) and `Parallel_with_Critique` (doctors critique peer diagnoses).
   - Host Moderator: `src/agents/host.py:54-150` (`summarize_diagnosis`, `summarize_symptom_and_examination`). Host aggregates opinions from Doctor A, B, etc., presents differences, and requests revision.
4. **Multi-View Medical Evaluation (MVME) Benchmark**:
   - Evaluation script: `src/evaluate/eval.py:13-80` (`Evaluator`).
   - GPT-4 Judge: Uses `gpt-4-1106-preview` (`eval.py:40`) as an LLM judge evaluating 5 clinical dimensions against expert records on an A/B/C/D scale:
     1. Patient symptoms grasped
     2. Medical examination completeness
     3. Diagnostic consistency
     4. Diagnostic basis consistency
     5. Treatment plan consistency

---

## 4. System 3: AgentVerse (`OpenBMB/AgentVerse`)

### 4.1 Repository Identity & Version Provenance
- **Primary Paper**: Chen, W., Su, Y., Zuo, J., Yang, C., Yuan, C., Chan, C.-M., Yu, H., Qin, Y., Lu, Y., Yin, S., Shen, J., Li, D., Peng, H., Yang, Z., Cai, D., Zhou, J., Yang, Y., Lin, D., Liu, Z., & Sun, M. (2024). *AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors*. In *International Conference on Learning Representations (ICLR 2024)*. arXiv: [2308.10848](https://arxiv.org/abs/2308.10848) [cs.CL].
- **Authoritative Repository**: `https://github.com/OpenBMB/AgentVerse`
- **Canonical Organization**: `OpenBMB`
- **Historical Release Tags & Commits**:
  - Paper baseline tag: `v0.1.5` (commit `6d42bb6e2b58dd93e1f07fd4d5f4065c2b8cb933`) and `v0.1.8` (commit `7739cba39b8f4f4d17b70810a2ed92a79afdc425`).
  - Historical release branch: `release-0.1` (commit `4ed4783f248875bc9e6efeda33482cc2d460f139`).
  - Current main commit: `f90c4bd9680fdd3bcff8c52c9170911a59b23478` (September 2024, async OpenAI fixes).
- **License**: Apache-2.0.

### 4.2 Directory Layout & Key Modules
```text
AgentVerse/
├── agentverse/
│   ├── agentverse.py                          # Top-level coordinator class
│   ├── tasksolving.py                         # 4-stage closed-loop task-solving pipeline
│   ├── simulation.py                          # Social emergence simulation pipeline
│   ├── initialization.py                      # Declarative YAML loader for agents & environments
│   ├── message.py                             # Structured Message class
│   ├── registry.py                            # Dynamic class registry pattern
│   ├── agents/                                # Agent implementations (base, conversation, tool)
│   ├── llms/                                  # Universal LLM adapters (OpenAI, Claude, local models)
│   ├── memory/                                # Vector and conversational memory modules
│   └── environments/
│       ├── base.py                            # Base environment interface
│       ├── tasksolving_env/
│       │   ├── basic.py                       # Tasksolving execution kernel
│       │   └── rules/
│       │       ├── role_assigner/             # Stage 1: Expert Recruitment
│       │       ├── decision_maker/            # Stage 2: Collaborative Decision Making (8 topologies)
│       │       ├── executor/                  # Stage 3: Action Execution
│       │       └── evaluator/                 # Stage 4: Closed-Loop Evaluation & Advice
│       └── simulation_env/
│           ├── basic.py                       # Social simulation engine
│           ├── pokemon.py                     # 2D tile-based social simulation (Smallville successor)
│           ├── prisoner_dilemma.py            # Game-theoretic dilemma environment
│           ├── sde_team.py                    # Software development team simulation
│           └── rules/                         # Modular rules: describer, order, selector, updater
└── ui/                                        # Web visualizer for simulation and task workflows
```

### 4.3 Mechanism Deconstruction & Exact Line Citations
1. **Dual Operating Framework (Task-Solving vs. Simulation)**:
   - Framework split: `agentverse/agentverse.py:20-66`. High-level coordinator dynamically branches into `TaskSolving` (`agentverse/tasksolving.py`) or `Simulation` (`agentverse/simulation.py`).
2. **Four-Stage Task-Solving Lifecycle**:
   - Loop execution: `agentverse/tasksolving.py:59-73` (`run`).
   - Iterative feedback mechanism: `tasksolving.py:65-68`. Passes `advice` and `previous_plan` across cycles:
     $$\text{step}(advice, previous\_plan) \longrightarrow (result, advice, previous\_plan, logs, success)$$
3. **Stage 1: Dynamic Expert Recruitment**:
   - Module: `agentverse/environments/tasksolving_env/rules/role_assigner/role_description.py:1-90`.
   - Generates customized agent personas and system prompts tailored to specific task descriptions rather than maintaining fixed agent rosters.
4. **Stage 2: Collaborative Decision Making (8 Communication Topologies)**:
   - Implementations: `agentverse/environments/tasksolving_env/rules/decision_maker/`:
     - `horizontal.py:1-45`: Decentralized peer-to-peer discussion where all agents contribute equally.
     - `vertical.py:1-55`: Hierarchical coordinator-worker structure.
     - `dynamic.py:1-70`: Context-dependent next-speaker selection.
     - `brainstorming.py:1-60`: Divergent idea generation.
     - `central.py:1-50`: Single leader broadcast.
     - `concurrent.py:1-75`: Independent parallel execution without communication.
     - `horizontal_tool.py:1-85`: Tool-augmented decentralized communication.
     - `vertical_solver_first.py:1-90`: Solver proposes preliminary draft; critic reviews and revises.
5. **Stage 4: Automated Closed-Loop Evaluation**:
   - Evaluator module: `agentverse/environments/tasksolving_env/rules/evaluator/base.py:1-65` and `basic.py:1-60`.
   - Generates quantitative score and actionable natural language `advice`. If score falls below threshold, triggers replanning or role reassignment.
6. **Social Simulation Environment (`pokemon.py`)**:
   - Class: `agentverse/environments/simulation_env/pokemon.py:1-240`.
   - Direct conceptual adaptation of Smallville's 2D grid world; agents move across coordinates, perceive local areas, and enter dynamic conversations.

---

## 5. System 4: ChatDev (`OpenBMB/ChatDev`)

### 5.1 Repository Identity & Version Provenance
- **Primary Paper**: Qian, C., Cong, X., Yang, C., Chen, W., Su, Y., Xu, J., Liu, Z., & Sun, M. (2024). *Communicative Agents for Software Development*. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024)*, August 11–16, 2024, Bangkok, Thailand. arXiv: [2307.07924](https://arxiv.org/abs/2307.07924) [cs.SE].
- **Authoritative Repository**: `https://github.com/OpenBMB/ChatDev`
- **Canonical Organization**: `OpenBMB`
- **Historical Release Tag**: `v1.0.0` (commit `5defde31792346e0cc302f672a33e766ef955dd8` / `acb93cf3d15cec5b9ee6eec0850ddd3932164329`), branch `chatdev1.0` (commit `31fd994416a251ecdeb1f0a73c329271743bfb56`). This version corresponds exactly to the published ACL 2024 paper results.
- **Modern Main Version**: Release `v2.2.0` (commit `3c72d860...`), branch `main` (commit `4fb2db0ea90375ce1059f44fe03ffbd191a7a169`).
- **Version Architecture Shift**: ChatDev v1 was a sequential, waterfall Chat Chain driven by CAMEL bilateral dialogue games and JSON configurations. ChatDev v2 introduced Docker compose runtimes, MCP (Model Context Protocol) tool servers, YAML declarative schemas (`yaml_template/`), and an asynchronous event engine (`runtime/`).

### 5.2 Directory Layout (Historical v1.0.0 / `chatdev1.0`)
```text
ChatDev (v1.0.0 / chatdev1.0)/
├── run.py                                     # Command-line entry point
├── CompanyConfig/
│   ├── Default/
│   │   ├── ChatChainConfig.json               # Phase sequence definition & recruitment parameters
│   │   ├── PhaseConfig.json                   # Subtask prompt instructions & termination contracts
│   │   └── RoleConfig.json                    # Role system prompts (CEO, CPO, CTO, Programmer, etc.)
│   └── Human/                                 # Human-in-the-loop configuration variants
├── camel/                                     # Embedded CAMEL communicative agent framework
│   ├── agents/role_playing.py                 # Bilateral role-playing session engine
│   └── configs/                               # LLM temperature & context configurations
├── chatdev/
│   ├── chat_chain.py                          # Waterfall pipeline orchestrator
│   ├── phase.py                               # SimplePhase dialogue runner & self-reflection fallback
│   ├── composed_phase.py                      # Compound looping phases (e.g., Review & Modify)
│   ├── chat_env.py                            # Environment state, code storage, host test execution
│   ├── codes.py                               # Code file extraction and git commit tracking
│   ├── documents.py                           # Requirement & manual documentation storage
│   └── statistics.py                          # Token consumption and financial cost accounting
└── visualizer/                                # Replay visualizer for communication logs
```

### 5.3 Mechanism Deconstruction & Exact Line Citations
1. **Chat Chain Waterfall Architecture**:
   - Pipeline manager: `chatdev/chat_chain.py:22-120` (`ChatChain`).
   - Phase sequence loaded from `CompanyConfig/Default/ChatChainConfig.json`:
     $$\text{DemandAnalysis} \rightarrow \text{LanguageChoose} \rightarrow \text{Coding} \rightarrow \text{CodeComplete} \rightarrow \text{CodeReview} \rightarrow \text{Test} \rightarrow \text{EnvironmentDoc} \rightarrow \text{Manual}$$
2. **Dual-Role Communicative Inversion**:
   - Dialogue session: `chatdev/phase.py:98-164`. Instantiates CAMEL `RolePlaying` session between an `Instructor` (user role) and `Assistant` (assistant role).
3. **Deterministic Step Termination Handshake (`<INFO>`)**:
   - Contract definition: `CompanyConfig/Default/PhaseConfig.json:17, 30, 152, 212`. Prompts mandate: `"any of us must actively terminate the discussion by replying with only one line, which starts with a single word <INFO>..."`.
   - Termination break: `chatdev/phase.py:143-155`.
     ```python
     if role_play_session.assistant_agent.info:
         seminar_conclusion = assistant_response.msg.content
         break
     ```
   - Parsing conclusion: `phase.py:181-183`. Strips termination tag: `seminar_conclusion.split("<INFO>")[-1]`.
4. **Communicative Dehallucination via Self-Reflection**:
   - Fallback reflection: `chatdev/phase.py:166-210` (`self_reflection`). If dialogue turns expire without reaching unanimous `<INFO>` consensus, the entire transcript is concatenated and fed into an LLM call querying for the final answer.
5. **Host-Based Code Execution & Vulnerability**:
   - Execution check: `chatdev/chat_env.py:107-157` (`exist_bugs`).
   - Host Command: Line 115 runs `cd {} && dir && python main.py` directly on the host machine using `subprocess.Popen(..., shell=True)` with a 3-second sleep (`time.sleep(3)`).
   - Omission: No Docker sandboxing, network isolation, or filesystem virtualization existed in v1.0.0.

---

## 6. System 5: Multi-Agent Collaboration via Evolving Orchestration & DyLAN Disambiguation

### 6.1 Authoritative Repository Resolution
- **Primary Paper**: Dang, Y., Qian, C., et al. (2025). *Multi-Agent Collaboration via Evolving Orchestration*. Accepted at *Thirty-ninth Conference on Neural Information Processing Systems (NeurIPS 2025)*. arXiv: [2505.19591](https://arxiv.org/abs/2505.19591).
- **Authoritative Repository URL**: `https://github.com/OpenBMB/ChatDev`
- **Specific Dedicated Branch**: `puppeteer`
- **Canonical Organization / Owner**: `OpenBMB` / Tsinghua University (lead author Chen Qian).
- **Historical Commit**: `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a` (branch `puppeteer`).
- **Monorepo Subdirectory**: `puppeteer/`.
- **Authoritative Resolution Finding**:
  - The repository for Evolving Orchestration is **NOT UNRESOLVED**.
  - It does **NOT** exist as a standalone repository named `evolving-orchestration`.
  - It was released by the authors inside the official `OpenBMB/ChatDev` repository on branch `puppeteer`.

### 6.2 Rigorous Contrast with DyLAN
A common point of ambiguity in the multi-agent literature is confusing *Multi-Agent Collaboration via Evolving Orchestration* with *Dynamic LLM-Agent Network (DyLAN)*:
- **DyLAN** (Liu, Peng, Cheng, Shen, Gao, & Zhou, ICLR 2024, arXiv:2310.02170):
  - Repository: `https://github.com/SALT-NLP/DyLAN` (commit `6f29633`).
  - Architecture: Models multi-agent interaction as a layered feed-forward network (`LLMLP` / `LLM_Neuron`).
  - Pruning / Evolution Mechanism: Unsupervised peer-rating. Agents prompt-rate peer responses to compute an Agent Importance Score (AIS); the lowest-scoring agents are pruned across successive layers. **No centralized controller or RL policy is used.**
- **Evolving Orchestration / Puppeteer** (Dang, Qian et al., NeurIPS 2025, arXiv:2505.19591):
  - Repository: `OpenBMB/ChatDev` (branch `puppeteer`).
  - Architecture: A centralized orchestrator ("Puppeteer") dynamically sequences specialized worker agents ("puppets") across parallel exploration paths in an adaptive reasoning graph.
  - Evolution Mechanism: Trained via **Reinforcement Learning** (Continuous REINFORCE policy gradient) over reward-model token embeddings (`nvidia/Llama-3.1-Nemotron-70B-Reward`). Can discover cyclic reasoning topologies.

### 6.3 Directory Layout of `puppeteer/` (ChatDev branch `puppeteer`)
```text
ChatDev (branch puppeteer)/
└── puppeteer/
    ├── main.py                                # Benchmark CLI runner (MMLU-Pro, gsm-hard, SRDD, CW)
    ├── config/
    │   ├── global.yaml                        # LLM provider endpoints, Nemotron-70B model path, graph limits
    │   └── policy.json                        # RL policy training hyperparameters (lr, gamma, kl_loss)
    ├── agent/
    │   ├── agent.py                           # Base agent definition
    │   ├── reasoning_agent.py                 # Tool-augmented reasoning agent (web search, code, files)
    │   └── register/                          # Global agent registry
    ├── inference/
    │   ├── graph/
    │   │   ├── agent_graph.py                 # Topological graph node registry
    │   │   └── action_graph.py                # Action taxonomy and embedding collection
    │   ├── policy/
    │   │   ├── base_policy.py                 # Abstract policy interfaces (LLMPolicy, LearningPolicy)
    │   │   └── REINFORCE_continuous.py        # Centralized RL policy network (4-layer MLP & gradient update)
    │   └── reasoning/
    │       ├── reasoning.py                   # GraphReasoning orchestrator
    │       └── path.py                        # GraphReasoningPath (parallel search path manager)
    ├── model/
    │   └── embedding.py                       # RewardModelTokenRepresentation (Nemotron-70B embedding extractor)
    ├── personas/
    │   └── personas.jsonl                     # Library of predefined agent roles and reasoning patterns
    ├── prompts/                               # System prompts and action selection templates
    ├── tasks/                                 # Benchmark runners (mmlu_pro, gsm_hard, srdd, creative_writing)
    └── tools/                                 # Web_Search, CodeInterpreter, FileRead
```

### 6.4 Mechanism Deconstruction & Exact Line Citations
1. **Centralized Reinforcement Learning Orchestrator**:
   - Policy Network: `puppeteer/inference/policy/REINFORCE_continuous.py:17-41` (`MLP_PolicyNetwork`). A 4-layer PyTorch MLP:
     $$\text{Linear}(d_{in}, 512) \rightarrow \text{ReLU} \rightarrow \text{Linear}(512, 128) \rightarrow \text{ReLU} \rightarrow \text{Linear}(128, 32) \rightarrow \text{ReLU} \rightarrow \text{Linear}(32, d_{out}) \rightarrow \text{Softmax}$$
   - Policy Optimization: `REINFORCE_continuous.py:43-150` (`ContinuousREINFORCE`). Updates policy weights using policy gradient with baseline subtraction and KL divergence penalty (`lambda_kl_loss`).
2. **State Representation via Reward Model Embeddings**:
   - Module: `puppeteer/model/embedding.py` and `REINFORCE_continuous.py:74`.
   - Uses `nvidia/Llama-3.1-Nemotron-70B-Reward` token representation layer to project evolving trajectory text into a dense vector input for the policy network.
3. **Dynamic Graph Reasoning & Parallel Path Exploration**:
   - Graph Orchestrator: `puppeteer/inference/reasoning/reasoning.py:23-100` (`GraphReasoning`).
   - Path manager: `puppeteer/inference/reasoning/path.py:15-180` (`GraphReasoningPath`).
   - Bounds: Explores up to `max_parallel_paths: 4` in parallel, stepping each path up to `max_step_num: 5` nodes. At each node, the policy selects the optimal puppet agent to execute the next reasoning step.
4. **Tool-Augmented Reasoning Puppet Agents**:
   - Agent implementation: `puppeteer/agent/reasoning_agent.py:22-120` (`Reasoning_Agent`).
   - Integrates `Web_Search` (`tools/web_search.py`), `CodeInterpreter` (`tools/code_interpreter.py`), and `FileRead` (`tools/file_read.py`).
   - Data compression: `reasoning_agent.py:36, 100-140` (`_compress_data`). Compresses prior tool observation outputs before injecting into subsequent puppet prompts.

---

## 7. Cross-System Synthesis & Comprehensive Classification Ledger (DR-04)

### 7.1 Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via | Formal Classification |
|---|----------|---------|-------------|--------|---------|----------------|----------------|-----------------------|
| **1** | Cognition / Memory | ConceptNode Schema | Monotonically indexed associative memory node with semantic triple, poignancy, and evidence pointers | Raw percept, chat, or thought text | Structured `ConceptNode` stored in `AssociativeMemory` | Silently ignores invalid triples | `joonspk-research/generative_agents` (`associative_memory.py:19-48`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **2** | Cognition / Memory | Retrieval Composite Scoring | 3-factor memory ranking combining recency, relevance, and importance | Query embedding, candidate memory stream, global weights `gw=[0.5, 3, 2]` | Top-K `ConceptNode` instances with updated `last_accessed` | Returns empty list if memory stream is empty | `joonspk-research/generative_agents` (`retrieve.py:199-271`) | `IMPLEMENTED_DIFFERENTLY` |
| **3** | Cognition / Reflection | Importance Trigger Accumulator | Reflection trigger decremented by LLM poignancy ratings from baseline 150 | Event poignancy integer ($1 \dots 10$) | Triggers `run_reflect()` when $\le 0$ and resets to 150 | If poignancy parsing fails, defaults to 1 | `joonspk-research/generative_agents` (`scratch.py:61-62`, `reflect.py:149-170`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **4** | Cognition / Planning | Hierarchical Plan Decomposition | Multi-tier schedule breakdown from wake-up hour to daily, hourly, and 5-min subtasks | Persona traits, daily requirements, current time | Array of planned actions with start times and durations | Falls back to generic idle action | `joonspk-research/generative_agents` (`plan.py:23-165`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **5** | Cognition / Planning | Daily Long-Term Replanning | Daily synthesis of prior day's memories to update goals and requirements | Prior day memories, existing daily requirements | Revised `daily_req` and status | **Omitted**: Code contains `# TODO` and recycles static string | `joonspk-research/generative_agents` (`plan.py:487-490`) | `DOCUMENTED_NOT_FOUND` |
| **6** | Communication | Bilateral Chatting Cooldown | 800-tick cooldown buffer preventing repeated dialogue between same agent pair | Agent ID, partner ID, current tick | Sets `chatting_with_buffer = 800` | Resets on tick progression | `joonspk-research/generative_agents` (`plan.py:860-905`) | `CODE_ONLY` |
| **7** | Simulation / IPC | Lockstep File-System Polling | Inter-process synchronization between backend and frontend via JSON file creation | `step.json` files in `storage/` directory | Discrete tick progression | Infinite loop / deadlock if file write fails or hangs | `joonspk-research/generative_agents` (`reverie.py:311-412`) | `IMPLEMENTED_DIFFERENTLY` |
| **8** | Organization / Medical | Structured Clinical Diagnosis | Doctor agent prompts enforcing multi-turn inquiry before structured diagnosis output | Multi-turn dialogue history with patient and medical records | Extracted diagnosis dictionary (`症状`, `辅助检查`, `诊断结果`, etc.) | Regex failure leaves fields empty | `LibertFan/AI_Hospital` (`doctor.py:10-95`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **9** | Organization / Medical | Target Role Addressing Prefix | Patient prepends `<对医生讲>` or `<对检查员讲>` to route utterance | Natural language patient response string | Dispatched message to Doctor or Reporter agent | Silently falls back to Doctor if prefix is omitted | `LibertFan/AI_Hospital` (`patient.py:68-82`) | `DOCUMENTED_PARTIALLY_IMPLEMENTED` |
| **10** | Organization / Medical | Multi-Doctor Dispute Resolution | Host-moderated discussion between competing doctor agents (`Parallel_with_Critique`) | Individual doctor diagnostic outputs | Consensus diagnosis report | If max turns reached, outputs latest host summary | `LibertFan/AI_Hospital` (`collaborative_consultation.py:14-192`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **11** | Benchmarking / Medical | MVME LLM-Judged Evaluation | GPT-4-based evaluation of clinical performance across 5 rubrics against expert records | Doctor diagnosis report, ground-truth patient medical record | Grade A/B/C/D per dimension | Throws API exception if key missing or rate-limited | `LibertFan/AI_Hospital` (`eval.py:13-80`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **12** | Organization / Topology | Dynamic Expert Recruitment | Generates specialized agent roles and system prompts dynamically from task descriptions | Natural language task specification | Customized agent configurations and prompts | Falls back to default generic agent | `OpenBMB/AgentVerse` (`role_description.py:1-90`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **13** | Communication / Topology | Multi-Topology Decision Makers | Pluggable communication structures (horizontal, vertical, dynamic, brainstorming, etc.) | Agent list, incoming messages, environment state | Aggregated decisions or next-speaker selection | Starvation or loop if consensus not reached | `OpenBMB/AgentVerse` (`decision_maker/*.py`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **14** | Governance / Evaluation | Closed-Loop Evaluator & Advice | Evaluator agent generates quantitative score and actionable natural language guidance | Intermediate plan, task criteria, round count | Score float, advice string, replan trigger | Halts when `max_rounds` reached | `OpenBMB/AgentVerse` (`tasksolving.py:59-73`, `evaluator/base.py`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **15** | Organization / SWE | Sequential Chat Chain | Waterfall development lifecycle decomposed into sequential atomic phases | User software prompt, `ChatChainConfig.json` | Generated multi-file software codebase | Pipeline aborts if phase raises unhandled exception | `OpenBMB/ChatDev` v1 (`chat_chain.py:22-120`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **16** | Communication / Protocol | Asymmetric Dialogue Inversion | Bilateral subtask execution with designated Instructor and Assistant roles | Phase prompt, role prompts, user objective | Co-developed intermediate artifact | Turn limit truncation (default 10 turns) | `OpenBMB/ChatDev` v1 (`phase.py:98-164`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **17** | Communication / Protocol | Termination Handshake (`<INFO>`) | Special token delimiter signaling unanimous mutual agreement and phase completion | Agent message containing `<INFO> <conclusion>` | Terminates dialogue loop and extracts conclusion | Triggers self-reflection fallback if `<INFO>` absent | `OpenBMB/ChatDev` v1 (`phase.py:143-155, 181-183`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **18** | Evaluation / Testing | Host Subprocess Test Execution | Directly executes generated software on host machine to detect runtime exceptions | Generated Python files directory | `(bool, str)` tuple indicating bug presence and traceback | Truncates execution after 3s sleep | `OpenBMB/ChatDev` v1 (`chat_env.py:107-157`) | `IMPLEMENTED_DIFFERENTLY` |
| **19** | Orchestration / RL | Continuous REINFORCE Orchestrator | Centralized PyTorch MLP policy trained with policy gradient to sequence reasoning agents | Reward model state embeddings, graph state | Probability distribution over puppet agents | Clamps action probabilities; falls back to uniform | `OpenBMB/ChatDev` branch `puppeteer` (`REINFORCE_continuous.py:43-150`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **20** | Orchestration / Search | Parallel Path Graph Reasoning | Explores up to 4 parallel reasoning paths across up to 5 steps per path | Task question, initial global info, agent graph | Final synthesized answer from best completed path | Discards failed paths; terminates on max steps | `OpenBMB/ChatDev` branch `puppeteer` (`reasoning.py:23-100`, `path.py`) | `DOCUMENTED_AND_IMPLEMENTED` |
| **21** | Orchestration / State | Reward Model Representation | Dense text representation using Llama-3.1-Nemotron-70B-Reward model weights | Trajectory token sequence | Feature vector input for policy MLP | Raises error if model weights not found at path | `OpenBMB/ChatDev` branch `puppeteer` (`model/embedding.py`, `global.yaml:52`) | `DOCUMENTED_AND_IMPLEMENTED` |

---

### 7.2 Edge Cases & Observed Divergences

| # | Feature | Tested / Inspected Input | Observed Behavior in Implementation | Conflicting Claim or Impact |
|---|---------|--------------------------|-------------------------------------|-----------------------------|
| **1** | Memory Recency Decay | Elapsed game time $\Delta t = 24\text{ hours}$ | Code uses chronological list index $i$: $\text{recency} = 0.99^i$ (`retrieve.py:145-146`). Real elapsed time has zero impact on recency decay. | Paper §4.1 claimed exponential decay based on game hours passed: $0.995^{\text{hours}}$. |
| **2** | Retrieval Weights | Equal component weighting ($\alpha_r = \alpha_i = \alpha_{rel} = 1$) | Code applies hardcoded global weights `gw = [0.5, 3, 2]` (`retrieve.py:244-250`). Relevance is weighted 6x over recency and 1.5x over importance. | Paper claimed equal weighting of all three factors. Equal weighting failed in author testing. |
| **3** | Daily Replanning Loop | Start of new simulation day tick rollover | `_long_term_planning` has `# TODO` and recycles static initial daily requirement (`plan.py:487-490`). | Paper claimed agents revise daily plans every morning based on yesterday's memories. |
| **4** | Patient Role Addressing | Patient response string omitting `<对医生讲>` or `<对检查员讲>` | Regex check fails; code silently falls back to `speak_to = "医生"` (`patient.py:77`). | System relies on prompt compliance; silently masks routing hallucinations without reporting error. |
| **5** | Code Review Termination | Programmer and Reviewer fail to reach consensus after 10 turns | Dialogue loop breaks on `chat_turn_limit`; executes `self_reflection` prompt forcing LLM to output conclusion (`phase.py:166-180`). | Prevents infinite loop, but conclusion is synthesized by a 3rd LLM call rather than mutual agreement. |
| **6** | Software Bug Testing | Malicious or non-terminating generated code | Executes directly on host machine via `subprocess.Popen("python main.py", shell=True)` (`chat_env.py:115`). Kills process after arbitrary 3-second sleep (`time.sleep(3)`). | Severe security hazard (RCE vulnerability on host); misses long-running bugs or initialization hangs. |
| **7** | Orchestrator Action Masking | Puppet agent proposed does not support required external tool | Query filters Chroma collection with `where={"category": "reasoning"}` if external tools disabled (`reasoning_agent.py:76-80`). | Gracefully degrades to pure reasoning mode when external tools are unavailable. |
| **8** | File IPC Desynchronization | Frontend browser tab closed or delayed during backend simulation | Backend executes `while True: if check_if_file_exists(curr_env_file): break; time.sleep(0.1)` (`reverie.py:380-400`). | Simulation hangs indefinitely waiting for frontend file creation; zero timeout or headless recovery. |

---

## 8. Paper-to-Code Divergences, Hardcoded Shortcuts, and Omissions

Across the five anchor repositories, our code archaeology revealed major systemic divergences between the theoretical descriptions in published research papers and the actual engineering realities in code:

### 1. The Smallville Retrieval & Planning Discrepancy
- **Rank Decay vs. Time Decay**: The paper's mathematical formulation ($recency = decay^{hours\_passed}$) gives the impression of a physically grounded temporal model. The implementation (`retrieve.py:145-146`) computes $0.99^i$ based solely on the list position index of the memory node. If an agent perceives 50 events in 10 minutes, the 51st event suffers 50 steps of decay; if an agent sleeps for 8 hours without events, zero decay occurs.
- **Hidden Global Weighting**: The code authors discovered that equal weights caused agents to focus obsessively on recent trivialities (e.g., staring at a refrigerator). To force believable behavior, they hardcoded `gw = [0.5, 3, 2]` (`retrieve.py:244-250`), heavily prioritizing semantic cosine relevance over recency.
- **Unimplemented Replanning**: The daily planning cycle celebrated in the paper as establishing long-term behavioral coherence was never completed in the code (`plan.py:487-490`). The code contains an explicit `# TODO` comment and simply copies the initial bootstrap requirements forward each morning.

### 2. The Agent Hospital Identity & Architecture Reality
- **Literature Confusion**: The academic community frequently conflates the Fudan/Alibaba *AI Hospital* (`LibertFan/AI_Hospital`, Feb 2024) with Tsinghua AIR's *Agent Hospital* (Zhang et al., May 2024). The user dispatch designated `LibertFan/AI_Hospital`. Our archaeology confirms that `LibertFan/AI_Hospital` is a lightweight evaluation benchmark built on standard chat completions and regex string parsing, rather than a spatial or evolutionary multi-agent simulation.
- **Silent Fallback Routing**: When simulating patient communication across multiple hospital departments, the architecture relies on prompt-based prefix adherence (`<对医生讲>`). In `patient.py:76-78`, failure to produce this prefix is silently forgiven by defaulting to the doctor, hiding prompt non-compliance from benchmark telemetry.

### 3. ChatDev Execution Sandbox Absence
- **Paper Claim**: The ACL 2024 paper describes an automated testing phase where the system validates software execution and iteratively debugs compiler and runtime errors.
- **Code Reality**: In historical v1.0.0 (`chat_env.py:107-157`), code execution is completely un-sandboxed. The Python script spawns `subprocess.Popen("python main.py", shell=True)` directly on the host operating system, waits 3 seconds (`time.sleep(3)`), and checks if `Traceback` appears in `stderr`. If an agent generates code containing malicious shell commands, network exfiltration, or infinite loops, the host system is directly exposed. (This fragility was resolved in ChatDev v2 via Docker compose containers).

### 4. System 5 Evolving Orchestration Resolution
- **Monorepo Discovery**: Multiple researchers have struggled to locate the code for *"Multi-Agent Collaboration via Evolving Orchestration"* because no independent GitHub repository exists under that title. Our investigation conclusively established that the authors committed the full system into `OpenBMB/ChatDev` on the `puppeteer` branch (`commit b24e6e6bd00bb04d317e0447cb7acb1e4973c83a`).
- **Heavyweight Dependencies**: The policy requires an untrained base reward model (`nvidia/Llama-3.1-Nemotron-70B-Reward`) to extract continuous token embeddings (`puppeteer/model/embedding.py`), making local execution of the RL policy prohibitive without multi-GPU infrastructure.

---

## 9. Reproducibility & Historical Integrity Audit

| System | Canonical Repo URL | Historical Commit / Tag | Modern HEAD Commit | Dependency Fragility / Bitrot Severity | Standalone Reproduction Viability |
|---|---|---|---|---|---|
| **Smallville** | `joonspk-research/generative_agents` | `fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4` | `fe05a71` (identical) | **Severe**: Hardcodes `openai==0.27.0` and `text-davinci-003` (deactivated Jan 2024). Django 2.2 deprecated. Cannot run without monkeypatching API calls. | **Non-Viable without API Refactoring** |
| **AI Hospital** | `LibertFan/AI_Hospital` | `870fc38c1daffa549c20332d273a8ad71b9d9fe1` | `870fc38` (identical) | **Low**: Standard `openai` SDK, supports modern base URLs and API keys. | **Viable** (requires OpenAI or compatible API keys) |
| **AgentVerse** | `OpenBMB/AgentVerse` | `v0.1.5` (`6d42bb6e...`) | `f90c4bd9` (`main`) | **Low-Medium**: Actively maintained; modern versions support async client and local models. | **Highly Viable** |
| **ChatDev** | `OpenBMB/ChatDev` | `v1.0.0` (`5defde31...`) | `4fb2db0e` (`main` v2.2.0) | **Moderate**: v1.0.0 requires legacy `openai<1.0.0`; modern v2 requires Docker and modern tool APIs. | **Viable on branch `chatdev1.0` or `main`** |
| **Evolving Orchestration** | `OpenBMB/ChatDev` (branch `puppeteer`) | `b24e6e6bd00bb04d317e0447cb7acb1e4973c83a` | `b24e6e6` | **High**: Requires PyTorch, CUDA GPU, and local copy of 70B reward model (`Llama-3.1-Nemotron-70B-Reward`). | **Viable on GPU cluster; Compute-Constrained on local machines** |

---

## 10. Conclusion & Forward Guidance for Gate R1

1. **Substrate Disqualification**: Neither raw Smallville (`joonspk-research/generative_agents`) nor historical ChatDev v1 (`OpenBMB/ChatDev`) can serve as an off-the-shelf experimental substrate for SimLab. Smallville is rendered inoperable by defunct OpenAI endpoints and lockstep file polling; ChatDev v1 lacks sandboxing and is constrained to software waterfall pipelines.
2. **System 5 Resolution**: The question of whether an official repository exists for *Multi-Agent Collaboration via Evolving Orchestration* is **RESOLVED** (`OpenBMB/ChatDev`, branch `puppeteer`). It is **NOT UNRESOLVED**.
3. **Architectural Primitives to Extract**:
   - Smallville: Associative memory stream (`ConceptNode`), importance-based reflection accumulation.
   - AgentVerse: Dynamic 4-stage lifecycle (Recruitment $\rightarrow$ Collaborative Decision $\rightarrow$ Execution $\rightarrow$ Evaluation) and pluggable decision topologies.
   - AI Hospital: Multi-role dispute resolution and grounded factual examiner (`Reporter`).
   - ChatDev: Grounded compiler feedback loop and explicit termination handshakes (`<INFO>`).
   - Evolving Orchestration / Puppeteer: Dynamic reasoning graph exploration and learned policy-driven agent sequencing.
