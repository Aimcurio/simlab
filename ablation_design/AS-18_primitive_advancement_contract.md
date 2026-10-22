# AS-18: Primitive Advancement Contract
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: PHASE_4_DESIGN  
**Design Gate**: PHASE_4_DESIGN_GATE (Alias: GATE_R4D)  
**Adjudication Gate Status**: GATE_R4 strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: UNFROZEN  
**Final SimLab Implementation Authority**: NOT_GRANTED  
**Phase 4 Execution Authority**: NOT_GRANTED  

---

## 1. Purpose & Pre-Execution Binding Rule

To maintain absolute epistemic discipline and prevent post-hoc outcome rationalization, this contract defines the **minimum evidentiary threshold** required for any multi-agent primitive to advance to Primitive Adjudication (GATE_R4).

**Core Governance Rule**:
All advancement rules must be codified **PRIOR** to Phase 4 execution. Evaluators are strictly forbidden from inventing, relaxing, or altering advancement criteria after experimental results are observed (NC-49, NC-66).

---

## 2. Seven Mandatory Primitive Advancement Criteria (A through G)

A cognitive or organizational primitive may advance to Primitive Adjudication **ONLY IF ALL SEVEN** of the following criteria are verified:

### Criterion A: Reproduction Evidence & Lineage Continuity
- **Requirement**: Reproduction evidence must be satisfied by either:
  - **A1 (Direct Phase 3 Qualification)**: A qualifying Phase 3 empirical status of `SUPPORTED` or `SUPPORTED_WITH_CONSTRAINTS`; **OR**
  - **A2 (Phase 4 Preregistered Confirmatory Replication)**: For primitives whose Phase 3 status was `PROMISING_BUT_NOT_SIGNIFICANT` (specifically `PR-ORG-01` / RP-02 private-information coordination), a preregistered `CONFIRMATORY_REPLICATION` (`EXP-AB-02-REP`) that successfully achieves its approved primary statistical threshold ($\alpha = 0.01$, two-sided) and minimum effect-size threshold ($\Delta \ge +10.0\%$).
- **Evidence-Status Transition Rule**:
  - If A2 succeeds, the governance harness explicitly records an immutable status transition from `PROMISING_BUT_NOT_SIGNIFICANT` to `CONFIRMED_BY_PHASE4_REPLICATION`:
    $$\text{PROMISING\_BUT\_NOT\_SIGNIFICANT} \longrightarrow \text{CONFIRMED\_BY\_PHASE4\_REPLICATION}$$
  - The historical Phase 3 finding is **NEVER** retroactively altered, rewritten, or erased. Historical evidence lineage is strictly preserved across all audit layers.
- **Falsification Standard**: Primitives whose Phase 3 findings resulted in `REJECT` or unmitigated `EQUIVALENCE_NOT_ESTABLISHED` (e.g. homogeneous GSM8K debate without tools), or whose Phase 4 confirmatory replication fails to meet the pre-registered $\alpha = 0.01$ and $\Delta \ge +10.0\%$ thresholds (`NOT_CONFIRMED`), are disqualified from advancement.


### Criterion B: Ablation Evidence
- **Requirement**: The component claimed to matter must demonstrate a statistically significant, measurable contribution relative to a valid, compute-matched control ($\Delta > 0, p < lpha$).
- **Falsification Standard**: If ablating the component produces negligible difference ($\Delta \le 	ext{margin}$) or if performance is driven entirely by a confounding factor (e.g. role prompts having zero effect when context boundary is ablated in SOPs), the primitive's standalone causal claim is falsified.

### Criterion C: Stress Evidence
- **Requirement**: The primitive must survive at least one pre-defined non-trivial stress regime (e.g. MODERATE stress under partial observation, memory noise, or distribution shift) without catastrophic accuracy collapse.
- **Falsification Standard**: If the primitive collapses immediately upon transitioning from clean BASELINE to MILD/MODERATE stress, it cannot advance as an architectural building block.

### Criterion D: Failure Boundary Documentation
- **Requirement**: The specific operating limits, degradation points, and failure cliff conditions under which the primitive breaks down must be empirically mapped and documented in the failure register.
- **Falsification Standard**: Unbounded claims of universal functionality or absence of a demonstrated failure boundary disqualify the primitive from advancement.

### Criterion E: Cost / Complexity Justification
- **Requirement**: The net performance benefit must remain positive and meaningful after accounting for token consumption, API latency, operational complexity, and implementation maintenance burden (NC-37).
- **Falsification Standard**: If a primitive delivers $+2\%$ accuracy but incurs 	imes$ token overhead or introduces severe synchronization bottlenecks, the Complexity Burden Rule blocks advancement.

### Criterion F: Confound Status
- **Requirement**: Zero unresolved critical confounds or benchmark artifacts (e.g. token mismatches, data leakage, prompt cues, unpinned models) may invalidate the interpretation of the results.
- **Falsification Standard**: Any experiment exhibiting model fingerprint drift (AF-02) or un-normalized compute (NC-10) is invalidated.

### Criterion G: External Validity Delimitation
- **Requirement**: The supported operating domain and unsupported domain must be explicitly delineated with negative boundaries (NC-46, NC-55).
- **Falsification Standard**: Primitives lacking explicit negative boundary statements are disqualified.

---

## 3. Non-Advancement Classifications

If a primitive fails any of the seven mandatory criteria, it **MUST NOT** advance to Primitive Adjudication. It must be classified strictly as one of the following five pre-registered outcomes:

| Classification | Definition & Evidentiary Trigger | Lifecycle Action |
|:---|:---|:---|
| **SUPPORTED_WITH_CONSTRAINTS** | The primitive survives Criteria A, B, C, D, and F, but has restricted operational boundaries (Criterion G) or tight cost constraints (Criterion E). | Advanced conditionally; final SimLab design must enforce strict runtime guardrails. |
| **CONTEXT_DEPENDENT** | The primitive demonstrates clear benefit under specific conditions (e.g. partitioned private knowledge) but shows zero benefit or negative utility elsewhere (e.g. homogeneous closed tasks). | Advanced for specialized workflows only; prohibited from global default deployment. |
| **DEFER** | The primitive requires higher-scale or cross-phase testing (e.g. 50+ agent populations deferred to Phase 8) or depends on unresolved upstream primitives. | Held in freeze; zero SimLab implementation code authorized until dependencies clear. |
| **REJECT** | The primitive fails Criterion B (ablation shows no causal contribution) or Criterion C (immediate collapse under stress), or was empirically falsified in Phase 3. | Discarded permanently from SimLab architecture. |
| **INSUFFICIENT_EVIDENCE** | Experimental runs were compromised by confounds, under-powering ( > lpha$ on non-replicated effects), or failure triggers (-01$ to -07$). | Requires protocol redesign or amendment under EXPERIMENT_AMENDMENT_REQUIRED. |

---

## 4. Final Curo Invariant

> **Reproduction establishes that an effect may exist.**  
> **Ablation identifies which component contributes to it.**  
> **Stress testing establishes its operating envelope.**  
> **Primitive Adjudication may advance only evidence that survives all three under preregistered criteria.**
