# AS-04: Memory Stress Plan
**Experiment ID**: `EXP-ST-01-SCALE`  
**Target Primitive**: `PR-COG-01`  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Primary Research Question
At what memory store scale ($M$), temporal horizon ($T$), and noise ratio ($\eta$) does tri-factor memory retrieval collapse, and what is the computational and accuracy cost of memory growth?

---

## 2. Progressive Stress Dimensions

```
Stress Level Progression:
BASELINE (M=100, Clean) -> MILD (M=500, 10% Noise) -> MODERATE (M=1,000, 30% Noise) -> SEVERE (M=5,000, 50% Noise) -> EXTREME (M=10,000+, Conflicting Noise)
```

### Stress Factors:
1. **Memory Volume Scale ($M$)**:
   - $M \in \{100, 500, 1,000, 5,000, 10,000\}$ discrete memory nodes.
2. **Temporal Horizon ($T$)**:
   - Short Horizon: $\Delta t \in [1, 50]$ ticks.
   - Medium Horizon: $\Delta t \in [51, 500]$ ticks.
   - Long Horizon: $\Delta t \in [501, 5,000]$ ticks.
3. **Injected Noise Types**:
   - **Irrelevant Distractors**: Synthetically generated memories with high lexical overlap but zero factual relevance.
   - **Duplicate Memories**: Identical episodic events recorded across multiple ticks.
   - **Contradictory / Superseded Memories**: Old facts explicitly invalidated by recent events (tests temporal override).
   - **Misleading High-Importance Lures**: Irrelevant memories assigned maximum importance ($s_{imp} = 1.0$).
4. **Distribution Shift**:
   - Topic drift where agent goals transition from social interaction to specialized technical tasks over time.

---

## 3. Dependent Variables & Failure Thresholds
- **Retrieval Accuracy & MRR**: Track degradation curve across $M$.
- **False Retrieval Rate**: Proportion of top-5 retrieved memories that are noise or superseded facts.
- **Latency & Computation Scaling**: Search latency (ms) and RAM usage (MB) as $M$ scales from 100 to 10,000.
- **Pre-Registered Failure Boundary**: An architecture failure cliff is reached if:
  1. MRR drops below $0.10$ ($p < 0.01$).
  2. False retrieval rate exceeds $40.0\%$.
  3. Single-query retrieval latency exceeds $50$ms on standard CPU.
