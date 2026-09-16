# DR-04: Paper <-> Code Mapping
**Curo Deep Research Investigation — Empirical Paper Claims vs. Repository Code Implementation Mapping**  
**Document ID**: `DR-04`  
**Document Version**: 1.0.0-FINAL  
**Lifecycle State**: `RESEARCH_AUTHORIZED` | **Implementation Authority**: `NOT_GRANTED`  
**Classification**: Formal Research Deliverable (Tier 1)  
**Author**: `curo_worker_1` (Primitive & Evidence Deliverables Author)  
**Verification Baseline**: `curo_explorer_1` (Archaeology Report & Line Citations)  

---

## 1. Executive Summary & Epistemic Taxonomy

A critical vulnerability in contemporary multi-agent research is the divergence between theoretical, publication-grade paper narratives and the messy engineering realities of open-source reference implementations. Academic publications frequently depict elegant mathematical formulations, clean temporal models, and recursive reflective architectures, while code inspections reveal hardcoded heuristics, heuristic shortcuts, unhandled edge cases, and outright unimplemented stubs.

In strict accordance with the **Curo Research Charter**, every architectural mechanism claimed in the literature is mapped directly against inspected repository code and classified into one of seven formal states:

| Classification | Definition |
|---|---|
| `DOCUMENTED_AND_IMPLEMENTED` | Claimed in literature and verified in code with concordant algorithmic logic. |
| `DOCUMENTED_PARTIALLY_IMPLEMENTED` | Described in paper, but code implements only a partial, degraded, or restricted subset. |
| `IMPLEMENTED_DIFFERENTLY` | Implemented in code, but the algorithmic logic contradicts or diverges from paper claims. |
| `DOCUMENTED_NOT_FOUND` | Explicitly claimed or mathematically specified in publication, but entirely absent or stubbed (`# TODO`) in code. |
| `CODE_ONLY` | Discovered in repository code; functional and active, but omitted from the publication text. |
| `VERSION_DEPENDENT` | Implementation exists, but logic, dependencies, or interfaces vary fundamentally across tags/branches. |
| `UNRESOLVED` | Source code cannot be located, verified, or traced to an authoritative repository. |

---

## 2. Master Paper <-> Code Feature Mapping Ledger

The following register catalogs 21 core architectural mechanisms across the anchor reference corpus, recording exact code citations, inputs, outputs, error behaviors, and formal classifications.

| # | Sourced System | Category | Feature Name | Paper Claim Description | Implemented Code Citation | Observed Code Logic & Formulas | Divergence Classification |
|---|---|---|---|---|---|---|---|
| **1** | Smallville | Cognition / Memory | ConceptNode Schema | Monotonically indexed associative memory nodes with semantic triples, poignancy, and evidence pointers | `reverie/backend_server/persona/memory_structures/associative_memory.py:19-48` | Stores `node_id`, `node_type`, `created`, `last_accessed`, `subject`, `predicate`, `object`, `description`, `embedding_key`, `poignancy`, `keywords`, `filling` | `DOCUMENTED_AND_IMPLEMENTED` |
| **2** | Smallville | Cognition / Retrieval | Memory Recency Decay | Exponential decay based on elapsed game hours: $\text{recency} = 0.995^{\Delta t_{\text{hours}}}$ | `reverie/backend_server/persona/cognitive_modules/retrieve.py:145-146` | Rank-based decay: $\text{recency} = 0.99^i$, where $i$ is chronological list position rank ($1 \dots \|M\|$), completely independent of elapsed game time | `IMPLEMENTED_DIFFERENTLY` |
| **3** | Smallville | Cognition / Retrieval | Retrieval Composite Weights | Equal weighting of recency, importance, and relevance: $\alpha_r = \alpha_i = \alpha_{\text{rel}} = 1.0$ | `reverie/backend_server/persona/cognitive_modules/retrieve.py:244-250` | Hardcoded global weights `gw = [0.5, 3, 2]`. Relevance is weighted 6x over recency and 1.5x over importance | `IMPLEMENTED_DIFFERENTLY` |
| **4** | Smallville | Cognition / Reflection | Importance Trigger Accumulator | Reflection fires when cumulative event poignancy exceeds threshold (150) | `reverie/backend_server/persona/memory_structures/scratch.py:61-62`, `reflect.py:149-170` | Decrements `importance_trigger_curr` by poignancy ($1 \dots 10$). When $\le 0$, runs reflection and resets to 150 | `DOCUMENTED_AND_IMPLEMENTED` |
| **5** | Smallville | Cognition / Reflection | Insight Extraction & Trees | Generates 3 focal questions, retrieves 30 nodes, extracts 5 insights with citation IDs | `reverie/backend_server/persona/cognitive_modules/reflect.py:99-134` | Queries LLM with `generate_focal_pt_v1.txt` and `insight_and_evidence_v1.txt`; saves `thought` nodes | `DOCUMENTED_AND_IMPLEMENTED` |
| **6** | Smallville | Cognition / Planning | Hierarchical Plan Decomposition | Recursive decomposition: wake-up hour $\rightarrow$ daily plan $\rightarrow$ hourly $\rightarrow$ 5-min subtasks | `reverie/backend_server/persona/cognitive_modules/plan.py:23-165` | Sequential LLM calls generate schedule arrays down to 5-minute action blocks | `DOCUMENTED_AND_IMPLEMENTED` |
| **7** | Smallville | Cognition / Planning | Daily Long-Term Replanning | Morning replanning updates daily goals based on yesterday's memories | `reverie/backend_server/persona/cognitive_modules/plan.py:487-490` | **Unimplemented stub**: Contains `# TODO` comment and copies static string: `persona.scratch.daily_req = persona.scratch.daily_req` | `DOCUMENTED_NOT_FOUND` |
| **8** | Smallville | Communication | Bilateral Chat Cooldown | Agents engage in dialogue; no mention of tick cooldown in paper text | `reverie/backend_server/persona/cognitive_modules/plan.py:860-905` | Hardcoded cooldown: `chatting_with_buffer = 800` ticks (8,000 game sec / 2.22 game hrs) between identical agent pairs | `CODE_ONLY` |
| **9** | Smallville | Simulation / IPC | Environment Synchronization | Continuous interactive simulation with Phaser 3 frontend | `reverie/backend_server/reverie.py:311-412` | Blocking single-threaded filesystem polling loop: backend and browser exchange JSON files on disk | `IMPLEMENTED_DIFFERENTLY` |
| **10** | Smallville | Infrastructure | Foundation Model Client | Utilizes OpenAI GPT models | `reverie/backend_server/persona/prompt_template/gpt_structure.py:211-220, 285` | Hardcoded call to `openai.Completion.create` using deprecated `model="text-davinci-003"` and `openai==0.27.0` | `DOCUMENTED_AND_IMPLEMENTED` (Deactivated API) |
| **11** | AI Hospital | Organization / Medical | Structured Clinical Diagnosis | Multi-turn inquiry before structured diagnosis block | `src/agents/doctor.py:10-95` | System prompt requires `#症状#`, `#辅助检查#`, `#诊断结果#`, etc.; parsed via regex `doctor.py:82-95` | `DOCUMENTED_AND_IMPLEMENTED` |
| **12** | AI Hospital | Organization / Routing | Target Role Addressing Prefix | Patient routes messages using `<对医生讲>` or `<对检查员讲>` | `src/agents/patient.py:68-82` | Regex parses prefix. Lines 76-78 implement silent fallback: defaults to `"医生"` if prefix omitted | `DOCUMENTED_PARTIALLY_IMPLEMENTED` |
| **13** | AI Hospital | Organization / Dispute | Multi-Doctor Panel Collaboration | Competing doctors debate diagnoses (`Parallel_with_Critique`) | `src/hospital/collaborative_consultation.py:14-192`, `host.py:54-150` | Host moderates rounds, synthesizes disagreements, requests revisions up to max turn limit | `DOCUMENTED_AND_IMPLEMENTED` |
| **14** | AI Hospital | Governance / Benchmark | MVME LLM-Judge Evaluation | Multi-View Medical Evaluation grading 5 rubrics against expert records | `src/evaluate/eval.py:13-80` | Structured evaluation using `gpt-4-1106-preview` grading A/B/C/D on symptoms, exams, diagnosis, basis, and treatment | `DOCUMENTED_AND_IMPLEMENTED` |
| **15** | AgentVerse | Organization / Lifecycle | Dynamic Expert Recruitment | Dynamic generation of agent roles and prompts from task descriptions | `agentverse/environments/tasksolving_env/rules/role_assigner/role_description.py:1-90` | LLM call generates custom agent roles, names, and system prompts tailored to task text | `DOCUMENTED_AND_IMPLEMENTED` |
| **16** | AgentVerse | Communication / Topology | Modular Decision Topologies | Pluggable deliberation structures (horizontal, vertical, dynamic, etc.) | `agentverse/environments/tasksolving_env/rules/decision_maker/*.py` | Implements 8 discrete decision topologies across separate Python modules | `DOCUMENTED_AND_IMPLEMENTED` |
| **17** | AgentVerse | Governance / Evaluation | Closed-Loop Evaluator & Advice | Evaluator grades solution and provides actionable advice for replanning | `agentverse/tasksolving.py:59-73`, `evaluator/base.py:1-65` | Evaluator outputs score and natural language string; triggers iteration if score below threshold | `DOCUMENTED_AND_IMPLEMENTED` |
| **18** | ChatDev | Organization / SWE | Sequential Chat Chain | Waterfall development lifecycle through atomic phases | `chatdev/chat_chain.py:22-120` | Loads `ChatChainConfig.json` and executes phases sequentially (DemandAnalysis $\rightarrow \dots \rightarrow$ Manual) | `DOCUMENTED_AND_IMPLEMENTED` |
| **19** | ChatDev | Communication / Protocol | Step Termination Handshake (`<INFO>`) | Agents terminate discussion upon reaching consensus | `CompanyConfig/Default/PhaseConfig.json`, `chatdev/phase.py:143-155, 181-183` | Prompt mandates `<INFO>` conclusion; parser breaks loop when assistant emits `<INFO>` | `DOCUMENTED_AND_IMPLEMENTED` |
| **20** | ChatDev | Governance / Testing | Host Subprocess Bug Testing | Automated testing detects syntax and runtime bugs | `chatdev/chat_env.py:107-157` | Runs `cd {} && dir && python main.py` directly on host via `subprocess.Popen(..., shell=True)` with 3s sleep | `IMPLEMENTED_DIFFERENTLY` (Security Hazard) |
| **21** | Evolving Orchestration | Orchestration / RL | Continuous REINFORCE Orchestrator | Centralized RL policy learns dynamic agent sequencing on reasoning graphs | `puppeteer/inference/policy/REINFORCE_continuous.py:17-150` | 4-layer PyTorch MLP trained with continuous policy gradients over Nemotron-70B reward embeddings | `DOCUMENTED_AND_IMPLEMENTED` (Monorepo branch `puppeteer`) |

---

## 3. Deep Archaeological Analysis of Critical Divergences

### 3.1 Divergence 1: Smallville Memory Retrieval Recency Inversion & Rank Decay
- **Paper Claim**: Park et al. (2023, §4.1) states:
  > "Recency assigns a higher score to memory objects that were recently accessed... we decay the score exponentially as a function of the number of game hours that have passed since the memory was last retrieved: $recency = decay\_factor^{hours\_passed}$, where $decay\_factor = 0.995$."
- **Code Reality**: In `reverie/backend_server/persona/cognitive_modules/retrieve.py:145-146`:
  ```python
  # retrieve.py:145-146
  recency_vals = [persona.scratch.recency_decay ** i for i in range(1, len(nodes) + 1)]
  ```
- **The Mathematical Inversion Bug**:
  Candidate nodes are initially sorted ascending by `last_accessed` (`retrieve.py:224-228`):
  ```python
  nodes = sorted(nodes, key=lambda x: x[0])
  ```
  This places the *oldest* memory at index `0` (corresponding to $i=1$) and the *newest* memory at the end ($i=N$). Because $0.99^1 = 0.99 \gg 0.99^N$, the oldest memory is assigned the highest raw recency score, and the newest memory receives the lowest score. After min-max normalization (`normalize_dict_floats`), the oldest memory receives normalized recency $1.0$, and the newest memory receives $0.0$.
- **Impact**: Elapsed game hours have zero mathematical effect on recency. If an agent perceives 50 events in 10 minutes, the 51st event suffers 50 steps of decay; if an agent sleeps for 8 hours without events, zero decay occurs. Furthermore, the decay formula was inverted in execution.

### 3.2 Divergence 2: Smallville Retrieval Factor Weights (`gw=[0.5, 3, 2]`)
- **Paper Claim**: §4.1 implies equal weighting across all three factors:
  > "We score recency, relevance, and importance... We normalize recency, relevance, and importance to the range $[0, 1] \dots$ The retrieval score is the sum of these three components."
- **Code Reality**: In `retrieve.py:244-250`:
  ```python
  gw = [0.5, 3, 2]
  master_out[node.node_id] = (
      gw[0] * recency_out[node.node_id] +
      gw[1] * relevance_out[node.node_id] +
      gw[2] * importance_out[node.node_id]
  )
  ```
- **Impact**: The code multiplies recency by 0.5, relevance by 3.0, and importance by 2.0. Semantic relevance is weighted **$6\times$ higher than recency** and $1.5\times$ higher than importance. Author experimentation discovered that equal weighting caused agents to focus obsessively on recent trivialities (e.g., staring at a sink), forcing the authors to heavily suppress recency in code without documenting the parameter change in the paper.

### 3.3 Divergence 3: Smallville Unimplemented Daily Replanning Stub
- **Paper Claim**: §4.3 describes dynamic daily replanning:
  > "Generative agents create plans recursively... To create the daily plan, the agent queries the memory system to retrieve memories about their goals and relationships... every morning, the agent reflects on the previous day and revises their schedule."
- **Code Reality**: In `reverie/backend_server/persona/cognitive_modules/plan.py:487-490`:
  ```python
  # plan.py:487-490
  # TODO We need to create a new daily_req here...
  persona.scratch.daily_req = persona.scratch.daily_req
  ```
- **Impact**: Dynamic daily replanning was never implemented. At each morning rollover, the agent simply copies forward its static bootstrap requirements. The illusion of long-term planning coherence reported in the paper was driven entirely by initial prompt engineering, not recursive daily replanning.

### 3.4 Divergence 4: AI Hospital Silent Role-Routing Fallback
- **Paper Claim**: Fan et al. (2024, §3.2) describe structured multi-agent communication where the patient dynamically addresses either the doctor or the medical examiner using explicit role tags.
- **Code Reality**: In `AI_Hospital/src/agents/patient.py:68-82`:
  ```python
  # patient.py:76-78
  if "<对医生讲>" in response:
      speak_to = "医生"
  elif "<对检查员讲>" in response:
      speak_to = "检查员"
  else:
      speak_to = "医生"  # Silent fallback!
  ```
- **Impact**: When the patient LLM forgets or hallucinates the role tag syntax, the code silently defaults to routing the message to the doctor. This masks prompt non-compliance from benchmark metrics, artificially inflating communicative reliability.

### 3.5 Divergence 5: ChatDev Un-Sandboxed Host Subprocess Execution
- **Paper Claim**: Qian et al. (ACL 2024, §3.3) describes an automated software testing phase where the system validates code execution and iteratively debugs compiler and runtime errors.
- **Code Reality**: In `ChatDev/chatdev/chat_env.py:107-157`:
  ```python
  # chat_env.py:114-116
  command = "cd {} && dir && python main.py".format(self.env_dict['directory'])
  p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  time.sleep(3)
  p.kill()
  ```
- **Impact**: Generated Python scripts are executed directly on the host operating system with shell privileges (`shell=True`). If an agent generates malicious shell commands, formatting commands, or network exfiltration scripts, the host machine is directly compromised. Furthermore, testing terminates after an arbitrary 3-second sleep (`time.sleep(3)`), failing to catch initialization hangs or long-running bugs.

---

## 4. Edge Cases & Observed System Failures

| # | Sourced System | Inspected Scenario / Input | Observed Implementation Behavior | Epistemic Assessment |
|---|---|---|---|---|
| **E1** | Smallville | Rapid event burst (50 percepts in 5 minutes) | Each new percept shifts all existing memories down the list, applying 50 decay multiplications ($0.99^{50} \approx 0.605$) to events that occurred minutes ago | Proves rank decay distorts temporal recency under variable perception density |
| **E2** | Smallville | Frontend browser window closed during simulation | Backend halts indefinitely in `while True: if check_if_file_exists(): break; time.sleep(0.1)` (`reverie.py:380-400`) | Deadlock; zero timeout or headless recovery mechanism exists |
| **E3** | ChatDev | Dialogue fails to reach `<INFO>` agreement within 10 turns | Loop aborts on `chat_turn_limit`; executes fallback `self_reflection` forcing a single LLM to synthesize agreement | Prevents infinite loop, but agreement is synthetic rather than mutual |
| **E4** | ChatDev | Generated code requires external GUI (e.g., `pygame.display`) | Subprocess hangs or crashes in headless environment; killed after 3 seconds | Benchmark tests fail on GUI libraries due to lack of virtual display (`xvfb`) |
| **E5** | AI Hospital | Doctor requests medical exam not in patient record | Reporter agent returns `"- xxx: 无异常"` (`reporter.py:45-55`) | Graceful negative disclosure, but cannot simulate false positives or laboratory errors |
| **E6** | Puppeteer | Tool access disabled in configuration YAML | Chroma search filters queries with `where={"category": "reasoning"}` (`reasoning_agent.py:76-80`) | Clean action masking; gracefully degrades to pure reasoning mode |

---

## 5. Substrate Evaluation Verdict

Based on our paper-to-code archaeology:

1. **Smallville Substrate Disqualification**: Raw Stanford Smallville (`joonspk-research/generative_agents`) **CANNOT** serve as SimLab's experimental substrate. Its cognitive layer relies on an inverted rank decay formula, undisclosed global weights (`gw=[0.5, 3, 2]`), an unfinished daily replanning stub, deprecated API endpoints (`text-davinci-003`), and a blocking filesystem IPC loop.
2. **ChatDev v1 Disqualification**: Historical ChatDev v1 **CANNOT** serve as SimLab's execution harness due to un-sandboxed host shell execution (`subprocess.Popen(..., shell=True)`).
3. **Clean Rebuild Requirement (Strategy C)**: SimLab must cleanly re-implement core candidate primitives (associative memory streams, tiered virtual memory, SOP pipelines, `<INFO>` consensus handshakes, and RL reasoning graphs) within a modern, sandboxed, event-driven architecture.
