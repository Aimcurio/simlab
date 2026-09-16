# RD-01: Reproduction Priority Matrix
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. Evaluation Methodology & Dimensions

Candidate reproductions identified during Gate R1 are prioritized across eight standardized operational dimensions:
1. **Architecture Impact**: Extent to which the empirical result alters foundational substrate design choices for SimLab (e.g. memory pipeline, communication topology, agent orchestration).
2. **Evidence Uncertainty**: Degree of contradiction, code divergence, or unmeasured claims in the primary literature.
3. **Failure Severity**: Systemic risk to SimLab if an invalid mechanism is naively adopted (e.g., exponential token blowout, silent memory corruption, coordination collapse).
4. **Cost to Reproduce**: Token, compute, engineering, and infrastructure spend required to construct a valid isolated harness.
5. **Isolation Feasibility**: Ability to test the primitive in an isolated micro-benchmark without building a complex multi-agent simulation or game world.
6. **Measurement Quality**: Availability of deterministic, ground-truth metrics (e.g., accuracy, rank correlation, state assertions) vs. subjective LLM judging.
7. **Transferability to SimLab**: Relevance of the mechanism to persistent, multi-agent long-horizon simulations ($N \ge 25$).
8. **Dependency on Other Primitives**: Whether the experiment requires other unverified primitives as prerequisites.

### Qualitative Classification Standard
- **`CRITICAL_TO_RESOLVE`**: Must be tested before any architecture synthesis. High architectural impact, high failure severity, high isolation feasibility.
- **`HIGH_VALUE`**: Substantially informs architecture choices; should be scheduled in Phase 3.
- **`USEFUL`**: Provides secondary optimizations or empirical boundaries; deferred to Phase 4 ablations.
- **`DEFER`**: Low isolation feasibility or heavy dependency on other unverified substrates; deferred until a reference build exists.
- **`REJECT`**: Disqualified by Gate R1 code archaeology, irreproducible foundation, or fundamental architectural invalidity.

---

## 2. Reproduction Priority Matrix

| Candidate ID | Target Primitive / Mechanism | Source System | Arch Impact | Evidence Uncertainty | Failure Severity | Cost to Repr. | Isolation Feas. | Measurement Quality | Transferability | Dep. on Primitives | Priority Class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **RP-01** | Temporal Recency Decay vs. Rank Inversion in Memory Retrieval | Generative Agents (Smallville) | High | Critical (Code Defect) | High | Minimal | Very High | Deterministic (MRR/NDCG) | High | None | **CRITICAL_TO_RESOLVE** |
| **RP-02** | Compute-Matched Single-Agent Self-Consistency vs. Multi-Agent Debate | General / Multi-System (B1-SC vs B3) | Critical | High (Confounds) | Critical | Moderate | High | Deterministic (Task Accuracy) | Critical | None | **CRITICAL_TO_RESOLVE** |
| **RP-03** | Structured Phase Boundaries & SOPs vs. Unrestricted Communication | ChatDev | High | High (Coord. Tax) | High | Moderate | High | Deterministic + Telemetry | High | None | **CRITICAL_TO_RESOLVE** |
| **RP-04** | Dynamic Agent Orchestration vs. Fixed Topology Escalation | ChatDev:puppeteer (Evolving Orchestration) | High | High (Unverified) | High | Moderate | High | Deterministic + Routing Telemetry | High | None | **CRITICAL_TO_RESOLVE** |
| **RP-05** | Reflection Frequency & Synthesis Triggers | Smallville / Agent Hospital | Moderate | High | Moderate | Moderate | Moderate | Mixed (Semantic Quality) | High | RP-01 | **HIGH_VALUE** (Phase 4) |
| **RP-06** | Role Specialization via Knowledge Bases / EHR | Agent Hospital | Moderate | Moderate | Low | Moderate | Moderate | Benchmark Accuracy (MedQA) | Moderate | None | **USEFUL** (Phase 4) |
| **RP-07** | Information Diffusion & Gossip Network Topology | Smallville | Low | High | Low | High | Low | Graph Diffusion Metrics | High | RP-01, RP-03 | **DEFER** (Phase 8) |
| **RP-08** | Legacy Lockstep File-Polling IPC Substrate | Smallville (`storage/`) | Disqualified | Defect Confirmed | Fatal | N/A | N/A | N/A | Zero | N/A | **REJECT** |

---

## 3. Substantive Rationale for Top-Tier Candidates

### RP-01: Smallville Memory Recency / Retrieval (`CRITICAL_TO_RESOLVE`)
- **Rationale**: Gate R1 confirmed an explicit paper-to-code inversion in `retrieve.py:145-146`, where older memories receive higher normalized recency scores, coupled with hidden hardcoded weights ($\alpha=0.5, \beta=3.0, \gamma=2.0$) diverging from published equal weights ($\alpha=\beta=\gamma=1.0$). Memory retrieval is the core cognitive substrate of persistent agents. Adopting an inverted or uncalibrated recency mechanism would silently corrupt agent behavior over long horizons. Testing this requires only an isolated retrieval harness on a static dataset with explicit timescale definitions in hours ($\Delta t_{hours} = \Delta t_{ticks} / 360$, half-life $138.28$ hours), making it minimal cost and maximum isolation feasibility.

### RP-02: Compute-Matched Single vs Multi-Agent Debate (`CRITICAL_TO_RESOLVE`)
- **Rationale**: The central architectural justification for multi-agent systems is that multiple communicating agents produce emergent reasoning superior to a single model. Gate R1 established that on closed-domain benchmarks, multi-agent debate fails to beat single-agent Self-Consistency when compute and token budgets are held equal. Due to multi-round context accumulation ($+50\%$ token inflation), call parity and token parity cannot be satisfied simultaneously. SimLab deploys a Dual-Control Protocol ($B_{1-SC-calls}$ at $K=7$ and $B_{1-SC-tokens}$ at $K=10$), deterministic tie-breaking, an expanded $N=500$ GSM8K sample size for $>80\%$ TOST power, and a Binomial GLMM to establish the definitive task boundary where multi-agent debate is scientifically justified.

### RP-03: Structured Phase Boundaries / ChatDev (`CRITICAL_TO_RESOLVE`)
- **Rationale**: Literature claims multi-agent assembly-line SOPs prevent conversational drift and hallucination cascades. However, Gate R1 identified a 4x–220x token coordination tax. Designing an isolated experiment comparing single agent vs. unrestricted multi-agent conversation vs. phase-bounded SOPs across $N=150$ tasks (including SWE-bench Lite mini multi-file tasks for genuine 4-role construct validity) directly answers whether formal phase boundaries justify their coordination overhead, evaluated via paired Wilcoxon and McNemar's tests ($>80\%$ power).

### RP-04: Dynamic Orchestration / ChatDev:puppeteer (`CRITICAL_TO_RESOLVE`)
- **Rationale**: Gate R1 traced Evolving Orchestration to `OpenBMB/ChatDev:puppeteer`. Dynamic routing is claimed to reduce unnecessary activations, but adds meta-agent routing latency and failure modes. Testing progressive escalation against both static full topology (`B3`) and compute-matched single-agent control (`B1-SC`) across $N=300$ tasks with a strict 70/30 train/test split and Cochran's Q test determines whether SimLab requires an adaptive orchestrator or should standardize on static, predictable pipelines.
