# AS-14: Failure & Abort Register
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Pre-Registered Failure Modes & Abort Conditions

| Failure Code | Failure Description | Trigger Condition | Automated Action |
|:---|:---|:---|:---|
| **AF-01** | Budget Overrun Threat | Cumulative spend exceeds $50.00 USD | HALT execution immediately; require human review. |
| **AF-02** | Model Fingerprint Drift | Provider returns altered `system_fingerprint` | Invalidate current batch; freeze runs until pinned. |
| **AF-03** | SOP Deadlock Epidemic | Reviewer/Coder review loop exceeds 16 turns in $>15\%$ tasks | Terminate condition; record failure boundary. |
| **AF-04** | Sycophancy / Consensus Cascade | False consensus rate in debate exceeds $25\%$ | Flag condition as failed; abort population expansion. |
| **AF-05** | Memory Retrieval Overflow | Retrieval latency exceeds $100$ms or RAM $> 1$ GB | Abort memory scale expansion; document scale cliff. |
| **AF-06** | Severe Routing Collapse | Heuristic router under-activation exceeds $20\%$ | Trigger Escalation Rule review for LLM router. |
| **AF-07** | Non-Deterministic Replay | Re-running identical seed produces different results | Invalidate harness; fix PRNG seeding. |
