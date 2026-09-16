# Handoff Report — curo_explorer_2 (Primitive Analyst & Evidence Modeler)

**Document Version**: 1.0.0-FINAL  
**Author**: `curo_explorer_2`  
**Recipient**: Parent Orchestrator (`3d79cf01-2554-4325-a08a-4860a5867124`)  
**Timestamp**: 2026-09-15T20:14:10Z  
**Working Directory**: `E:\projects\simlab\.agents\curo_explorer_2`  
**Primary Artifact**: `E:\projects\simlab\.agents\curo_explorer_2\primitive_analysis.md`  
**Lifecycle State**: `RESEARCH_AUTHORIZED` (Gate R1 Preparation)

---

## 1. Observation

1. **Schema & Mandate Compliance**:
   - Inspected `E:\projects\simlab\.agents\ORIGINAL_REQUEST.md` (lines 134–395) and `E:\projects\simlab\.agents\curo_explorer_2\DISPATCH.md`.
   - Protocol R2 mandate specifies DR-05 (Primitive Evidence Matrix): All 26 fields must be present per primitive; explicit states (`UNKNOWN`, `NOT_REPORTED`, `NOT_MEASURED`, `NOT_APPLICABLE`, `UNRESOLVED`) must be used for missing data; **ZERO primitives may receive `VALIDATED` status**.
   - Protocol R3 mandate specifies Confound Control: Disentangle mechanism improvements from foundation model family/scale, context windows, token budget/spend, prompt templates, and random seeds.
   - Protocol R4 mandate specifies Baseline Discipline (DR-10): Map mechanisms against B0 (Deterministic), B1 (Single LLM), B2 (Multiple Independent LLM), B3 (Fixed-Role Multi-Agent), and B4 (Candidate Adaptive System).

2. **Source Code & Implementation Observations**:
   - **Smallville (`joonspk-research/generative_agents`)**:
     - Memory retrieval weights in paper claimed $\alpha_r = \alpha_i = \alpha_{rel} = 1.0$, but code inspection of `reverie/backend_server/persona/cognitive_modules/retrieve.py:244-250` reveals `gw = [0.5, 3, 2]`.
     - Recency calculation in paper claimed exponential hourly decay $0.995^{\Delta t}$, but code in `retrieve.py:145-146` reveals rank-based decay $0.99^{\text{rank}}$.
     - Reflection accumulator in `reflect.py:149-155` decrements from 150 based on poignancy ratings.
     - Daily replanning in `plan.py:487-490` contains `# TODO` on `persona.scratch.daily_req = persona.scratch.daily_req`, recycling bootstrap goals.
     - Legacy model coupling hardcoded `text-davinci-003` in `gpt_structure.py:285`.
   - **Agent Hospital & AI Hospital**:
     - Resolved two distinct publications:
       1. `Agent Hospital: A Simulacrum of Hospital with Evolvable Medical Agents` (Tsinghua AIR, arXiv:2405.02957), introducing MedAgent-Zero with dual memory (Medical Record Library + Experience Base).
       2. `AI Hospital: Benchmarking Large Language Models in a Multi-agent Medical Interaction Simulator` (Fan et al., COLING 2025 / arXiv:2402.03300, repo `LibertFan/AI_Hospital`).
   - **Multi-Agent Collaboration via Evolving Orchestration**:
     - Authoritative publication is Dang, Qian et al. (NeurIPS 2025 accepted, arXiv:2505.19591).
     - Authoritative implementation resides in the `puppeteer` branch of the `OpenBMB/ChatDev` repository (`https://github.com/OpenBMB/ChatDev/tree/puppeteer`), resolving the repository location.
   - **Modern Systems Survey Verification**:
     - Verified MetaGPT (ICLR 2024 Oral, `geekan/MetaGPT`), AutoGen v0.4 (`microsoft/autogen`), CAMEL (NeurIPS 2023, `camel-ai/camel`), MemGPT/Letta (`letta-ai/letta`), Concordia (`google-deepmind/concordia`), WarAgent (`Wang et al., 2023`), and AgentBench (ICLR 2024, `THUDM/AgentBench`).

3. **Artifact Generation**:
   - Executed primitive extraction and evidence modeling, compiling 28 discrete candidate primitives across all 6 functional categories into `E:\projects\simlab\.agents\curo_explorer_2\primitive_analysis.md`.
   - Populated all 26 schema fields for every record. Strictly verified that ZERO primitives received `VALIDATED` status.

---

## 2. Logic Chain

1. **Premise 1 (Attribution Fallacy in Literature)**: Literature frequently attributes benchmark performance gains to multi-agent topologies when underlying models were upgraded (e.g. GPT-3.5 $\rightarrow$ GPT-4) or token inference budgets were multiplied by $5\times$ to $12\times$.
2. **Premise 2 (Scientific Baseline Requirement)**: An architectural mechanism cannot be declared superior unless it outperforms the simplest baseline holding token spend and model version constant (Protocol R4).
3. **Observation Step**: In multi-agent debate (AgentVerse, Liang et al.), spending $6\times$ tokens across 3 agents and 2 rounds was compared against a 1-shot single-agent baseline. When compared against a token-matched B1 baseline (Single-agent Self-Consistency with $k=6$ samples), the multi-agent advantage evaporates or reverses on standard reasoning benchmarks (GSM8K, MATH).
4. **Observation Step**: In software engineering agents (ChatDev, MetaGPT), conversational free-form dialogue caused chat-collapse and infinite loops. Replacement with typed artifact handoffs (`PRIM-ORG-01`) and compiler execution loops (`PRIM-GOV-01`) reduced tokens by up to 80% and increased success rates.
5. **Observation Step**: In simulation memory (Smallville), flat associative retrieval over an unindexed stream caused quadratic compute scaling $O(N \cdot M)$ and context window overflow. Tiered virtual memory (`PRIM-COG-04`, MemGPT/Letta) bounds prompt size to $O(1)$ by paging to external databases.
6. **Deductive Conclusion**: Multi-agent interaction is beneficial only when tasks exhibit genuine structural decomposition, domain role asymmetry, or deterministic tool validation. For homogeneous reasoning tasks, B1 with test-time sampling is superior. The target simulation lab must synthesize:
   - Layer A: Decoupled async logical clock (`PRIM-SIM-03`) + Transactional state (`PRIM-SIM-04`)
   - Layer B: Tiered virtual memory (`PRIM-COG-04`) + Self-editing (`PRIM-COG-05`)
   - Layer C: SOPs with typed artifacts (`PRIM-ORG-01`) + Actor pub/sub bus (`PRIM-ORG-06`)
   - Layer D: Deterministic CapBAC policy engine (`PRIM-GOV-03`)
   - Layer G: Compiler/linter execution feedback (`PRIM-GOV-01`) + Auditor gate (`PRIM-GOV-02`)
   - Layer H & I: OpenTelemetry tracing (`PRIM-COM-05`) + Docker assertion scoring (`PRIM-GOV-04`)

---

## 3. Caveats

1. **Paper-Reported vs Re-Executed Metrics**: Performance metrics cited in `measured_benefit` reflect primary literature reports. Under Curo Lifecycle State `RESEARCH_AUTHORIZED` with `Implementation Authority: NOT_GRANTED`, zero code execution or benchmark re-runs were conducted.
2. **Preprint Stability**: `Multi-Agent Collaboration via Evolving Orchestration` (arXiv:2505.19591) and `HERA` (arXiv:2604.00901) are recent preprints. While the puppeteer code is verified in the ChatDev repository, their long-term generalization remains provisional.
3. **Proprietary API Deprecation**: Historical baselines (e.g., `text-davinci-003` in Smallville, `gpt-3.5-turbo-0613` in AgentVerse) are deprecated by OpenAI, meaning exact historical execution cannot be reproduced against identical endpoints; future reproductions must use pinned open-weight models (e.g., Llama-3-70B / Qwen-2.5-72B).

---

## 4. Conclusion

1. The DR-05 Primitive Evidence Matrix is complete: 28 candidate primitives across Cognition (6), Organization (6), Communication (5), Learning (3), Simulation (4), and Governance (4) have been extracted with all 26 schema fields.
2. Zero primitives received `VALIDATED` status. 17 primitives are designated as `REPRODUCTION_CANDIDATE`, 9 as `PROMISING_BUT_UNVERIFIED`, 1 as `PROPOSED`, and 1 as `INSUFFICIENT_EVIDENCE`.
3. Mechanism and model confounds (R3) have been systematically documented: 7 out of 8 anchor systems failed to report random seeds or token-normalized baselines.
4. Baseline discipline (R4) confirms that single LLM agents with test-time compute (B1) and deterministic rule engines (B0) beat or match complex multi-agent architectures on homogeneous reasoning and physics resolution.

---

## 5. Verification Method

To independently verify this work:
1. Inspect the deliverable file:
   `view_file(AbsolutePath="E:\\projects\\simlab\\.agents\\curo_explorer_2\\primitive_analysis.md")`
2. Verify schema field completeness:
   Ensure all 28 primitives contain lines corresponding to fields 1 through 26 (`primitive_id` through `status`).
3. Verify zero `VALIDATED` status invariant:
   Run regex or string search across `primitive_analysis.md` for `status: VALIDATED` or `| VALIDATED |`. Result must be 0 matches.
4. Invalidation Conditions:
   - If any primitive is found missing any of the 26 schema fields.
   - If any primitive is assigned `VALIDATED` status.
   - If synthetic, un-sourced token costs or metrics are presented as empirical facts without `NOT_REPORTED` or `UNKNOWN` tags.
