# AS-14: Failure & Abort Register & Stress Termination Contract
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  
**Design Gate**: `PHASE_4_DESIGN_GATE` (Alias: `GATE_R4D`)  
**Adjudication Gate Status**: `GATE_R4` strictly reserved for post-ablation/stress execution adjudication  
**Architecture Status**: `UNFROZEN`  
**Final SimLab Implementation Authority**: `NOT_GRANTED`  
**Phase 4 Execution Authority**: `NOT_GRANTED`  

---

## 1. Pre-Registered Failure Modes & Abort Conditions

| Failure Code | Failure Description | Threshold Category | Trigger Condition | Automated Action |
|:---|:---|:---|:---|:---|
| **AF-01** | Hard Budget Overrun Threat | `abort_threshold` | Cumulative API spend exceeds **$50.00 USD** | HALT execution immediately; trigger emergency review. |
| **AF-02** | Model Fingerprint Drift | `abort_threshold` | Provider returns altered `system_fingerprint` | Invalidate current batch; freeze runs until pinned. |
| **AF-03** | SOP Deadlock Epidemic | `failure_threshold` | Reviewer/Coder review loop exceeds 16 turns in $>15\%$ tasks | Terminate condition; record failure boundary. |
| **AF-04** | Sycophancy / Consensus Cascade| `failure_threshold` | False consensus rate in debate exceeds **$25.0\%$** | Flag condition as failed; abort population expansion. |
| **AF-05** | Memory Retrieval Overflow | `abort_threshold` | Retrieval latency $> 100$ms or RSS RAM $> 1.0$ GB | Abort memory scale expansion; document scale cliff. |
| **AF-06** | Severe Routing Collapse | `failure_threshold` | Heuristic under-activation exceeds **$20.0\%$** | Trip Complexity Escalation Rule for router review. |
| **AF-07** | Non-Deterministic Replay | `abort_threshold` | Re-running identical PRNG seed produces divergent output | Invalidate run harness; fix RNG seeding sequence. |
| **AF-08** | Task Degradation Floor | `degradation_threshold`| Primary accuracy metric drops $> 10.0\%$ below control | Log degradation warning; evaluate recovery threshold. |
| **AF-09** | Consensus Recovery Failure | `recovery_threshold` | Re-introducing full state fails to restore consensus $>90\%$ | Declare unrecoverable distributed state breakdown. |

---

## 2. Universal Stress Experiment Termination Contract

For every stress experiment across memory, multi-agent debate, SOP pipelines, and routing, the execution harness must strictly adhere to the following termination contract:

### 2.1 Four Operational Tiers:
- **`BASELINE`**: Nominal load; validates baseline operation.
- **`MILD`**: Low-level stress; checks for unexpected sensitivity.
- **`MODERATE`**: Realistic stress; identifies performance degradation.
- **`SEVERE`**: Near-cliff stress; locates the definitive failure boundary.

### 2.2 Binding Stop Rules & Multi-Trigger Escalation Protocol:
The execution harness **MUST TERMINATE** testing immediately upon encountering any of the following three conditions:
1. **Failure Boundary Established**: When the experimental metric crosses the pre-registered `failure_threshold` and establishes the operational envelope of the primitive.
2. **Safety or Budget Ceiling Reached**: When `abort_threshold` triggers ($AF-01$ budget, $AF-02$ drift, $AF-05$ memory/latency).
3. **Epistemic Invariance**: When further stress execution cannot alter the architectural conclusion (e.g. if a primitive fails at `MODERATE`, testing `SEVERE` is prohibited).

### 2.3 Multi-Trigger Escalation & Practical-Significance Discipline
Escalation across tiers (`SCREEN` $\to$ `ESCALATE` $\to$ `INTERACTION_TEST`) is authorized when **ANY ONE** of the three preregistered triggers is satisfied:
1. **Practical Degradation Trigger**: `practical_degradation_threshold` or `failure_threshold` is crossed.
2. **Statistical Trigger**: `statistical_threshold` demonstrates a material effect under the preregistered test ($p < \alpha$ with meaningful effect size).
3. **Mechanistic Failure Trigger**: A scientifically important failure mode appears that requires bounded follow-up even when sample size is insufficient for formal significance.

**Mechanistic Failure Trigger Governance Rules**:
- Must be explicitly logged with timestamp, run ID, and environmental parameters.
- Must identify the observed causal failure mechanism (e.g. agent dropout state divergence, deterministic stale retrieval, cyclic SOP deadlock, specialist starvation).
- Must justify the bounded follow-up experiment.
- Strictly does not permit unrestricted exploratory expansion or arbitrary compute burning.

**Practical-Significance Discipline**:
Escalating solely because $p < \alpha$ when the observed effect is operationally trivial is strictly prohibited. Statistical and practical evidence serve as complementary signals, not a mandatory AND pair.

**Anti-Waste Invariant**: Never execute tests up to maximum stress merely because the tier exists in the matrix (`NC-54`). Compute must be conserved for discriminative evaluations.

---

## 3. Secure Execution Architecture & Network Isolation Model

To reconcile the requirement for `--network none` container isolation (`NC-16`) with live provider API evaluation (`NC-39`), the execution runtime enforces a two-tier brokered architecture:

```
+-----------------------------------------------------------------------------------------------+
|                                ISOLATED EXPERIMENT CONTAINER                                  |
|  - Network Namespace: --network none (Zero Direct Internet Access)                             |
|  - Host Isolation: No provider credentials, no environment secrets, ephemeral tmpfs mounts   |
|  - Capabilities: Reads immutable inputs; writes only approved telemetry & result paths       |
+-----------------------------------------------------------------------------------------------+
                                               |
                                               | Structured Local Request (Unix Domain Socket / Local IPC)
                                               v
+-----------------------------------------------------------------------------------------------+
|                                 CONTROLLED INFERENCE BROKER                                   |
|  - Location: Separate trusted host process / gateway daemon                                   |
|  - Security: Holds provider API credentials; enforces strict credential boundary              |
|  - Pre-Call Checks: Enforces per-experiment budget and Phase 4 $50.00 abort ceiling (AF-01)   |
|  - Validation: Pinned model snapshot check; logs provider system_fingerprint (AF-02)          |
|  - Rate & Token Limits: Enforces max token caps and concurrency governors                     |
+-----------------------------------------------------------------------------------------------+
                                               |
                                               | Outbound Egress: HTTPS (Port 443) Only
                                               v
+-----------------------------------------------------------------------------------------------+
|                                  ALLOWLISTED MODEL API                                        |
|  - Authorized Providers: Provider-pinned endpoints only                                       |
|  - Egress Audit Log: Every request/response hash, token count, and latency logged             |
+-----------------------------------------------------------------------------------------------+
```

### 3.1 Egress Policy Specification
- `allowed_provider_domains`: Explicit allowlist (e.g. `generativelanguage.googleapis.com`, `api.openai.com`, or configured local mock endpoint).
- `allowed_ports`: 443 (HTTPS) only from Inference Broker.
- `credential_owner`: Controlled Inference Broker exclusively. Worker containers possess zero credentials.
- `request_broker`: Local IPC / authenticated Unix domain socket crossing the isolation boundary.
- `network_namespace`: Experiment workers run with `--network none`. Direct egress from workers is blocked at kernel level.
- `firewall_policy`: Strict deny-all for worker namespace; outbound allowlist strictly restricted to provider endpoints for Inference Broker.
- `egress_audit_log`: Append-only cryptographic ledger recording timestamp, `run_id`, `request_hash`, `prompt_hash`, `system_fingerprint`, and token usage.

### 3.2 Model Drift Circuit Breaker Protocol (`AF-02`)
For every paid or live inference call, the broker captures:
`provider`, `model_id`, `model_version/snapshot`, `system_fingerprint`, `request_hash`, `prompt_hash`, `run_id`, `response_id`, `token_usage`.
If the provider returns an altered `system_fingerprint` during a controlled experiment, the broker raises `STOP_VERSION_DRIFT`, halts run dispatch, and invalidates the batch.

### 3.3 Pre-Call Budget Projection Protocol (`AF-01`)
Before dispatching any outbound model call:
1. Compute projected token spend: $\text{Cost}_{\text{proj}} = \text{Current}_{\text{spend}} + \text{EstCall}_{\text{cost}}$.
2. Check against `EXP_BUDGET_LIMIT` (Level 2) and `PHASE4_BUDGET_ABORT_THRESHOLD` ($50.00 USD, Level 3).
3. If projected spend exceeds either threshold, the call is blocked immediately without dispatch.


