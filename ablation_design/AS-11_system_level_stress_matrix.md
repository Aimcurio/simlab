# AS-11: System-Level Stress Matrix
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Cross-Primitive Interaction Stress Dimensions

To prevent combinatorial explosion while testing real-world multi-agent failure modes, Phase 4 defines a bounded cross-primitive stress matrix targeting high-risk interactions:

```
+----------------------------------------------------------------------------------------------------+
|                                    SYSTEM-LEVEL STRESS MATRIX                                      |
+----------------------------------------------------------------------------------------------------+
| Stress Vector             | Interacting Primitives | Target Failure Mode (RD-11) | Test Level      |
+----------------------------------------------------------------------------------------------------+
| 1. Population Growth      | Memory + Routing + SOP | FM-04 / FM-11 (Token/IPC    | N = 1, 5, 10, 25|
|    (1 to 25 Agents)       |                        | Congestion Blowout)         |                 |
| 2. Long-Horizon Drift     | Memory (PR-COG-01) +   | FM-02 / Context Stale Drift | T = 100 to      |
|    (Continuous Ticks)     | Social Dialogue        |                             | 5,000 ticks     |
| 3. Partial Communication  | Debate (PR-ORG-01) +   | FM-06 (Consensus Collapse   | Packet Loss:    |
|    Failure (Dropouts)     | Distributed State      | under Partition)            | 0%, 10%, 25%    |
| 4. Injected Misinformation| Memory + Debate        | False Belief Epidemic       | 1 to 5 Corrupt  |
|    (Adversarial Agents)   |                        | (Information Cascade)       | Seed Facts      |
| 5. Context Saturation     | SOP (PR-ORG-02) +      | FM-01 (Context Window       | Context Load:   |
|    (Tool Artifact Flood)  | Tool Execution         | Truncation & Memory Purge)  | 50%, 80%, 100%  |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Operational Invariants During System Stress
- Populations above 25 agents are strictly deferred to Phase 8.
- Host system resources remain bounded by `bubblewrap` cgroups (60s timeout, 512MB RAM, `--network none`).
- All stress runs remain subject to the pre-call financial projection constraint (`NC-38`).
