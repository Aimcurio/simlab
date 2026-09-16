# AS-06: Distributed-State Stress Plan
**Experiment ID**: `EXP-ST-02-STATE`  
**Target Primitive**: `PR-ORG-01`  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Primary Research Question
How does multi-agent state tracking perform as agent population scales from 1 to 25 agents, and under what levels of communication delay, agent dropout, and observation error does distributed coordination break down?

---

## 2. Progressive Stress Scaling Dimensions

### A. Population Scale Grid:
- $N_{\text{agents}} \in \{1, 3, 5, 10, 25\}$. (Populations of $50+$ are strictly deferred per `NC-57` until 25-agent stability is proven).

### B. State Complexity & Observation Noise:
1. **World State Dimensionality**:
   - Small: 5 locations, 10 dynamic entities.
   - Moderate: 15 locations, 50 entities.
   - Complex: 25 locations, 100 entities.
2. **Partial Observation Bandwidth**:
   - Each agent observes only a local field of view ($\le 20\%$ of world state).
3. **Observation Corruption / Noise ($\epsilon_{\text{obs}}$)**:
   - $0\%$ error (clean observations).
   - $10\%$ false-entity observation noise.
   - $25\%$ conflicting observation reports between agents in adjacent locations.
4. **Agent Dropout & Communication Delay**:
   - Dropout: $0\%$, $10\%$, or $20\%$ of agents fail to transmit state updates on any given tick.
   - Delay: State messages arrive with a 1-tick or 2-tick latency.

---

## 3. Metrics & Failure Boundaries
- **State Tracking Accuracy**: Proportion of world state entity locations correctly identified across discrete ticks.
- **Consensus Latency**: Number of message rounds required for the agent group to resolve state conflicts.
- **Token Scaling Curve**: Token growth as a function of population ($N$) and entity count ($E$).
- **Pre-Registered Failure Cliff**: Architecture failure is declared if communication overhead scales worse than $\mathcal{O}(N^2)$ or tracking accuracy falls below single-agent baseline.
