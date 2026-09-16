# Phase 2 Adversarial Challenge Report: RP-01 & RP-02 Experimental Designs

**Agent Identity**: Phase 2 Challenger 1 (`teamwork_preview_challenger`)  
**Archetype**: EMPIRICAL CHALLENGER (critic, specialist)  
**Working Directory**: `E:\projects\simlab\.agents\phase2_challenger_1`  
**Evaluation Target**: Experimental Designs for RP-01 (Smallville Memory Recency) and RP-02 (Debate vs B1-SC) in:
- `E:\projects\simlab\reproduction_design\RD-05_rp01_experiment_design.md`
- `E:\projects\simlab\reproduction_design\RD-06_rp02_experiment_design.md`
- `E:\projects\simlab\reproduction_design\RD-03_experimental_hypothesis_register.md`
- `E:\projects\simlab\reproduction_design\RD-04_baseline_compute_matching.md`

**Formal Gate Verdict**: **`REQUEST_CHANGES`**

---

## Challenge Summary

**Overall Risk Assessment**: **CRITICAL**

The experimental designs for RP-01 and RP-02 exhibit critical mathematical impossibilities, statistical under-powering, and internal contradictions that will produce false conclusions or invalid benchmarks if executed as written:
1. **RP-02 Token Parity Mathematical Impossibility (CRITICAL)**: Constraining both inference calls ($K=6$) and tokens ($\pm 10\%$) between single-agent B1-SC and 3-agent 2-round debate is mathematically impossible under realistic generation lengths. Debate carries an accumulator history that inflates tokens by $+56.25\%$ ($7,500$ vs $4,800$ tokens). Fixing $K=6$ starves B1-SC of $36\%$ of its compute budget, giving debate an unfair advantage. A true token-matched control requires $K \approx 9\text{--}10$.
2. **RP-02 TOST Equivalence Power Collapse (CRITICAL)**: Demonstrating that B1-SC matches debate on GSM8K within a $\pm 3\%$ margin ($\delta = 0.03$) using $N = 100$ problems has **$0.00\%$ empirical statistical power** ($90\%$ CI half-width is $\pm 5.2\%$ to $\pm 7.4\%$). Proving equivalence within $\pm 0.03$ requires $N \ge 450\text{--}600$ problems.
3. **RP-02 Even $K=6$ Majority Voting Tie Defect (HIGH)**: $K=6$ produces exact 3-3 ties in up to $31.25\%$ of task instances with zero tie-breaking protocol specified.
4. **RP-01 Timescale & Normalization Sensitivity (HIGH)**: Decay parameter $\lambda = 0.995$ has a half-life of 138 hours (~5.76 days) if measured in hours, but only 23 minutes if measured in Smallville's native 10-second ticks (as proposed in `DR-15:305`). Min-max normalization magnifies micro-noise when candidate memory ages are clustered within narrow time windows.
5. **RP-01 Weighting Collapse on Non-Temporal Queries (HIGH)**: Under proposed equal weights ($\alpha=\beta=\gamma=1.0$), recency scoring severely degrades relevance-dominant queries (MRR drops from $0.4423$ to $0.0992$, a $77.6\%$ collapse). Overall MRR under equal weighting ($0.2436$) is significantly *worse* than no-recency retrieval ($0.4010$, $p < 0.001$).
6. **Pre-Registered Failure Threshold Dead Zones (MEDIUM)**: Both RP-01 and RP-02 possess large ambiguous zones between success and failure thresholds where inconclusive results slip through with no pre-registered decision rule.

---

## 1. Observation

Direct inspection of reproduction design documents and authoritative code revealed the following:

### Observation 1.1: RP-02 Token Parity & Inference Call Contradiction
In `RD-04_baseline_compute_matching.md` (lines 32-33):
```markdown
Tokens(B1-SC) ~= Tokens(T_MA) +/- 10%
Inference Calls(B1-SC) ~= Inference Calls(T_MA) +/- 10%
```
And in `RD-06_rp02_experiment_design.md` (lines 52-53):
```markdown
- Total inference calls normalized: B1-SC (K=6 calls) vs T-Debate (3 agents * 2 rounds = 6 calls).
- Total token expenditure window constrained to +/- 10%.
```
In `RD-06_rp02_experiment_design.md` (line 64):
```markdown
Debate rounds append previous agent critiques to conversation history. B1-SC instances run in isolated parallel contexts with zero cross-talk.
```

### Observation 1.2: RP-02 Sample Size and Equivalence Margin on GSM8K
In `RD-06_rp02_experiment_design.md` (lines 20-21):
```markdown
Conversely, on closed-domain symbolic reasoning (GSM8K/MATH), compute-matched B1-SC will equal or exceed multi-agent debate accuracy within a +/- 3% margin.
```
In `RD-06_rp02_experiment_design.md` (lines 70-71):
```markdown
100 balanced problem instances across 4 task suites (400 total task problems):
- 100 problems from GSM8K (Closed Symbolic Reasoning).
```
And in `RD-06_rp02_experiment_design.md` (line 86):
```markdown
Confirmation of hypothesis that T-Debate provides <= 2% advantage on GSM8K under matched compute.
```
Contradicted by `RD-03_experimental_hypothesis_register.md` (line 26):
```markdown
achieves no statistically significant improvement (Delta < 3%, p >= 0.05) on closed-domain symbolic reasoning benchmarks (GSM8K/MATH).
```

### Observation 1.3: RP-02 B1-SC Even-K Voting
In `RD-06_rp02_experiment_design.md` (line 33):
```markdown
Single-agent Self-Consistency with K independent reasoning samples (T=0.7) where K exactly matches the total inference calls of the multi-agent debate treatment, aggregated via majority voting.
```
With $K = 3 \times 2 = 6$ (even number). No tie-breaking protocol is specified anywhere in `RD-06` or `RD-04`.

### Observation 1.4: RP-01 Decay Formula Timescale Divergence
In `RD-05_rp01_experiment_design.md` (lines 20, 36):
```markdown
Corrected exponential temporal recency decay (s_{rec} = 0.995^{\Delta t_{hours}})
where \Delta t = t_{current} - t_{created} in elapsed simulation hours, evaluated as s_{rec} = \gamma^{\Delta t} (with \gamma = 0.995)
```
In `deliverables\DR-15_lessons_learned_forward_constraints.md` (lines 305-308):
```python
def compute_recency(created_tick: int, current_tick: int, decay_factor: float = 0.995) -> float:
    delta_ticks = current_tick - created_tick
    assert delta_ticks >= 0, "Memory creation tick cannot be in the future"
    return float(decay_factor ** delta_ticks)
```
In Smallville's engine, 1 game tick $= 10$ seconds (360 ticks per hour).

### Observation 1.5: RP-01 Published Equal Weighting vs Code Weighting
In `RD-05_rp01_experiment_design.md` (line 36):
```markdown
combined with cosine relevance and pre-computed importance using published equal weighting (\alpha=\beta=\gamma=1.0).
```
In Smallville's repository (`retrieve.py:244-250`):
```python
gw = [0.5, 3, 2] # recency = 0.5, relevance = 3.0, importance = 2.0
```

### Observation 1.6: RP-01 Statistical Method Contradiction
In `RD-05_rp01_experiment_design.md` (line 20):
```markdown
compared to the historical inverted implementation and no-recency baseline (p < 0.01, Mann-Whitney U test)
```
In `RD-05_rp01_experiment_design.md` (line 76):
```markdown
Paired Wilcoxon signed-rank test comparing MRR and NDCG@5 between T-Corrected and B0-Historical.
```

### Observation 1.7: Unhandled Ambiguous Threshold Zones
In `RD-05_rp01_experiment_design.md`:
- Success Threshold (line 81): $\Delta \text{MRR} \ge +0.15, p < 0.0025$.
- Failure Threshold (line 86): $\Delta \text{MRR} < +0.05, p \ge 0.05$.
- The interval $[+0.05, +0.15)$ is completely unspecified.

In `RD-06_rp02_experiment_design.md`:
- Success Threshold (lines 85-86): `T-Debate` exceeds `B1-SC` by $\ge +10\%$ on Private Info & Tools ($p < 0.01$) AND `T-Debate` provides $\le 2\%$ advantage on GSM8K.
- Failure Threshold (line 89): `B1-SC` achieves equal or higher accuracy than `T-Debate` across all 4 task categories ($p \ge 0.05$).
- If `T-Debate` achieves $+6\%$ advantage on Private Info, neither condition triggers.

---

## 2. Logic Chain

### Logic Chain 2.1: Mathematical Impossibility of $\pm 10\%$ Token Parity under $K=6$ (RP-02)
1. **Input Context & Accumulation**: In B1-SC, each of the $K$ inference calls receives prompt $C_0$ and emits output $L$, consuming total tokens $T_{\text{B1-SC}} = K(C_0 + L)$. For $K=6$, $T_{\text{B1-SC}} = 6 C_0 + 6 L$.
2. **Debate History Expansion**: In a 3-agent, 2-round debate, Round 1 consumes $3(C_0 + L)$. In Round 2, each agent receives the problem prompt $C_0$ plus all 3 Round 1 agent outputs ($3L$). Thus, Round 2 input tokens per agent are $C_0 + 3L$, and total Round 2 tokens are $3(C_0 + 3L + L) = 3 C_0 + 12 L$.
3. **Total Debate Tokens**: $T_{\text{Debate}} = 3(C_0 + L) + 3(C_0 + 4L) = 6 C_0 + 15 L$.
4. **Token Ratio**: The ratio of Debate tokens to B1-SC ($K=6$) tokens is:
   $$\frac{T_{\text{Debate}}}{T_{\text{B1-SC}}} = \frac{6 C_0 + 15 L}{6 C_0 + 6 L} = 1 + \frac{9 L}{6 (C_0 + L)} = 1 + 1.5 \left(\frac{L}{C_0 + L}\right)$$
5. **Empirical Evaluation**: For typical prompt length $C_0 = 500$ tokens and reasoning response $L = 300$ tokens:
   - $T_{\text{B1-SC}} = 6 \times 800 = 4,800$ tokens.
   - $T_{\text{Debate}} = 6(500) + 15(300) = 3,000 + 4,500 = 7,500$ tokens.
   - Excess tokens: $+56.25\%$.
6. **Boundary Condition**: For Debate to remain within $+10\%$ of B1-SC ($K=6$):
   $$6 C_0 + 15 L \le 1.10 (6 C_0 + 6 L) \implies 8.4 L \le 0.6 C_0 \implies L \le \frac{C_0}{14} \approx 0.0714 C_0$$
   For $C_0 = 500$, $L$ would have to be $\le 35.7$ tokens, which is impossible for multi-turn CoT or debate reasoning.
7. **Compute Equivalence Violation**: B1-SC with $K=6$ is starved of $36\%$ of the tokens consumed by Debate. To achieve token equivalence with $7,500$ tokens, B1-SC requires $K = 7,500 / 800 = 9.38 \approx 9\text{--}10$ samples. Therefore, matching calls at $K=6$ directly violates the token parity mandate of `RD-04`.

### Logic Chain 2.2: TOST Equivalence Margin Collapse on GSM8K (RP-02)
1. **Hypothesis**: The design claims compute-matched B1-SC will equal multi-agent debate within $\pm 3\%$ margin ($\delta = 0.03$) on GSM8K.
2. **Sample Allocation**: Only $N = 100$ problems are allocated for GSM8K in `RD-06:71`.
3. **Paired Difference Variance**: Let discordance rate between conditions be $p_{\text{disc}} = P(Y_{\text{Debate}} \ne Y_{\text{B1-SC}})$. The standard error of the difference is $\text{SE} = \sqrt{p_{\text{disc}} / N}$.
4. **Confidence Interval Width**: In TOST, non-inferiority/equivalence requires the two-sided $90\%$ confidence interval ($z_{0.95} = 1.6449$) to lie entirely within $[-\delta, +\delta] = [-0.03, +0.03]$. The half-width is $\text{HW} = 1.6449 \sqrt{p_{\text{disc}} / N}$.
5. **Sample Size Impossibility**: For $\text{HW} < 0.03$:
   $$N > \left(\frac{1.6449}{0.03}\right)^2 p_{\text{disc}} \approx 3,006.5 \cdot p_{\text{disc}}$$
   - At $p_{\text{disc}} = 0.10$, $N \ge 301$ (HW with $N=100$ is $\pm 5.20\%$).
   - At $p_{\text{disc}} = 0.15$, $N \ge 451$ (HW with $N=100$ is $\pm 6.37\%$).
   - At $p_{\text{disc}} = 0.20$, $N \ge 602$ (HW with $N=100$ is $\pm 7.36\%$).
6. **Empirical Power**: In a 10,000-iteration Monte Carlo simulation with $N=100$ and true $\Delta = 0.00$, the empirical power to establish equivalence within $[-0.03, +0.03]$ was **$0.09\%$ at $p_{\text{disc}}=0.10$** and **$0.00\%$ at $p_{\text{disc}}=0.15$ and $0.20$**. The test is statistically pre-destined to fail.

### Logic Chain 2.3: Even $K=6$ and Majority Voting Ties (RP-02)
1. **Binomial Tie Probability**: When $K$ is even ($K=6$), an exact 3-3 split occurs with probability $\binom{6}{3} p_0^3 (1-p_0)^3 = 20 p_0^3 (1-p_0)^3$.
2. **Quantification**:
   - At $p_0 = 0.50$, $P(\text{Tie}) = 31.25\%$.
   - At $p_0 = 0.60$, $P(\text{Tie}) = 27.65\%$.
   - At $p_0 = 0.70$, $P(\text{Tie}) = 18.52\%$.
3. **Zero Marginal Value of 6th Call**: If ties are broken by a coin flip, $P(\text{Success} \mid K=6) = P(>3) + 0.5 P(=3) = \sum_{k=4}^6 \binom{6}{k} p_0^k (1-p_0)^{6-k} + 0.5 \binom{6}{3} p_0^3 (1-p_0)^3$, which is algebraically identical to $\sum_{k=3}^5 \binom{5}{k} p_0^k (1-p_0)^{5-k} = P(\text{Success} \mid K=5)$. The 6th inference call adds exactly $0.0\%$ accuracy over $K=5$, while creating unhandled tie states.

### Logic Chain 2.4: Timescale Sensitivity of $\lambda=0.995$ & Normalization Instability (RP-01)
1. **Half-Life Derivation**: The half-life is $t_{1/2} = \ln(0.5) / \ln(0.995) = 138.28$ units.
2. **Timescale Conflict**:
   - If unit is **hours** (`RD-05`): $t_{1/2} \approx 138.3$ hours (5.76 days). In a 72-hour timeline, a memory from 72 hours ago decays only to $0.995^{72} = 0.697$.
   - If unit is **ticks** (`DR-15:305`): 1 tick $= 10$ seconds $= 1/360$ hours. $t_{1/2} = 138.28 \text{ ticks} = 23.0$ minutes. At 1 hour (360 ticks), score decays to $0.1645$. At 24 hours (8,640 ticks), score is $1.55 \times 10^{-19} \approx 0.000$.
3. **Normalization Distortion**: Min-max normalization maps $s_{\max} \to 1.0$ and $s_{\min} \to 0.0$. If candidate memories are clustered between 20h and 22h ago, raw scores are $[0.9046, 0.8956]$ (a spread of $0.0090$). Min-max normalization stretches this $0.0090$ difference across the entire $[0, 1]$ interval, amplifying noise and overpowering relevance. If timestamps are identical, division by zero occurs ($0/0 \to \text{NaN}$).

### Logic Chain 2.5: Equal Weighting Retrieval Collapse on Non-Temporal Queries (RP-01)
1. **Mechanics**: When $\alpha=\beta=\gamma=1.0$, recency accounts for $33.3\%$ of the total score.
2. **Degradation on Relevance Queries**: For queries where the ground truth is an older event (e.g. agent's educational background), any recent irrelevant memory receives normalized recency $1.0$, easily outscoring the older relevant memory ($s_{\text{rec}} = 0.0$).
3. **Empirical Simulation**: On a 500-memory database with 100 queries:
   - Recency queries: MRR increases from $0.3680$ (NoRecency) to $0.5030$ (EqualWeights).
   - Relevance queries: MRR collapses from $0.4423$ (NoRecency) to $0.0992$ (EqualWeights) — a $77.6\%$ degradation!
   - Conflict queries: MRR collapses from $0.3846$ to $0.0137$.
   - **Overall MRR**: Drops from $0.4010$ (NoRecency) to $0.2436$ (EqualWeights), $p < 0.001$.
4. **Code Weighting Superiority**: Smallville code weights ($\alpha=0.5, \beta=3.0, \gamma=2.0$) achieved overall MRR of $0.5147$, proving that recency must be heavily subordinated to relevance. Mandating published equal weights ($\alpha=\beta=\gamma=1.0$) falsifies the retrieval hypothesis in reverse.

---

## 3. Caveats

1. **Deterministic Micro-Harness Scope**: Verification was conducted using statistical, mathematical, and synthetic retrieval simulations. No commercial LLM benchmark API calls were executed, adhering strictly to the governance boundary.
2. **Context Window Lengths**: Token calculations assumed typical prompt length $C_0 \in [300, 1000]$ tokens and output length $L \in [200, 500]$ tokens. If prompts are massive ($C_0 > 10,000$) and outputs are trivial ($L < 20$), the token ratio narrows, but such parameters do not represent reasoning benchmarks like GSM8K.
3. **Tie-Breaking Implementations**: In B1-SC, ties can be broken by selecting the answer with highest average log-probability or first occurrence; however, neither is specified in RD-06.

---

## 4. Challenges

### [Critical] Challenge 1: Token Parity Is Impossible Under $K=6$ (RP-02)
- **Assumption Challenged**: That B1-SC ($K=6$) provides both inference call parity and token budget parity within $\pm 10\%$ against 3-agent 2-round debate.
- **Attack Scenario**: Because debate appends prior turns into context, Round 2 input tokens expand quadratically. Debate consumes $+56.25\%$ more tokens ($7,500$ vs $4,800$ tokens). B1-SC at $K=6$ is starved of $36\%$ compute.
- **Blast Radius**: Rigged benchmark favoring multi-agent debate; invalidates the compute-matching claim of `RD-04` and `RD-06`.
- **Mitigation**: Decouple call parity from token parity. Standardize on **Token-Matched B1-SC** by setting $K = 9$ (or $K = 11$), ensuring total tokens match within $\pm 10\%$.

### [Critical] Challenge 2: TOST Equivalence Margin Has Zero Statistical Power at $N=100$ (RP-02)
- **Assumption Challenged**: That $N = 100$ problems on GSM8K can establish equivalence between B1-SC and Debate within $[-0.03, +0.03]$ at $\alpha = 0.05$.
- **Attack Scenario**: With $N=100$, the standard error of paired proportions is $\ge 3.2\%$, yielding a $90\%$ CI half-width of $\ge \pm 5.2\%$. It is mathematically impossible for the confidence interval to fit within $\pm 3\%$, even if the observed difference is $0.00\%$. Empirical power is $0.00\%$.
- **Blast Radius**: Guaranteed failure to demonstrate equivalence; leads to false rejection of the null hypothesis or ambiguous impasse.
- **Mitigation**: Expand GSM8K sample size to at least $N = 500$ problems, or widen the equivalence margin to $\delta = 0.08$ with formal power justification.

### [High] Challenge 3: B1-SC Even $K=6$ Produces Massive Ties (RP-02)
- **Assumption Challenged**: That majority voting over $K=6$ samples is an effective, standard self-consistency baseline.
- **Attack Scenario**: Exact 3-3 ties occur in $18.5\%$ to $31.3\%$ of problems. The 6th sample provides $0.0\%$ marginal accuracy over $K=5$.
- **Blast Radius**: Uncontrolled random noise in baseline scoring; invalidates exact reproducibility.
- **Mitigation**: Enforce odd sample counts for B1-SC ($K = 7$ for call-matched or $K = 9$ for token-matched), and pre-register a deterministic tie-breaking rule (e.g. cumulative log-probability or lower sample index).

### [High] Challenge 4: Timescale Unit Ambiguity and Normalization Artifacts (RP-01)
- **Assumption Challenged**: That $\lambda = 0.995$ is an invariant decay constant across implementations.
- **Attack Scenario**: If implemented in ticks (`DR-15:305`), half-life is 23 minutes, wiping out memories older than 2 hours. If in hours (`RD-05`), half-life is 138 hours, barely distinguishing memories within 24 hours. Furthermore, min-max normalization magnifies micro-differences into full $[0, 1]$ swings when candidates have narrow age spreads.
- **Blast Radius**: Total invalidation of memory retrieval benchmark; failure of cross-agent reproduction.
- **Mitigation**: Pin the decay formula to continuous simulation seconds with explicit timescale parameterization: $s_{\text{rec}} = \exp(-\Delta t_{\text{sec}} / \tau)$, where $\tau$ is chosen to match the target operational half-life (e.g. $\tau = 48\text{ hours} / \ln 2 \approx 250,000\text{ s}$). Replace min-max normalization with static sigmoid or raw exponential bounds to prevent scale compression.

### [High] Challenge 5: Equal Weights ($\alpha=\beta=\gamma=1.0$) Destroys Retrieval (RP-01)
- **Assumption Challenged**: That testing published equal weighting ($\alpha=\beta=\gamma=1.0$) validates effective retrieval.
- **Attack Scenario**: Equal weighting allows recency to overpower semantic relevance on non-temporal queries, causing a $77.6\%$ MRR collapse on relevance queries and lowering overall MRR below the no-recency baseline.
- **Blast Radius**: Primary hypothesis $H_1$ in RD-05 will be decisively rejected simply due to poor weighting, obscuring whether temporal decay itself works.
- **Mitigation**: Update the primary treatment to use calibrated weights where relevance dominates ($\alpha=0.5, \beta=3.0, \gamma=2.0$), and evaluate equal weighting only as an ablation condition.

### [Medium] Challenge 6: Pre-Registered Threshold Dead Zones (RP-01 & RP-02)
- **Assumption Challenged**: That pre-registered success and failure thresholds partition the outcome space deterministically.
- **Attack Scenario**: Outcomes falling in ambiguous zones (e.g. RP-01 $\Delta \text{MRR} = +0.10$; RP-02 Private Info gain $= +6\%$) trigger neither success nor failure.
- **Blast Radius**: Inconclusive experiment with no pre-registered decision rule, forcing subjective post-hoc adjudication.
- **Mitigation**: Define exhaustive, complementary threshold partitions: Success ($H_1$), Failure ($H_0$), and Inconclusive/Marginal ($H_{\text{marginal}}$) with explicit architectural consequences for each.

---

## 5. Stress Test Results Summary

| Scenario / Test | Expected Behavior | Actual / Simulated Behavior | Status |
|---|---|---|---|
| **RP-02 Token Parity ($K=6$)** | $\text{Tokens}_{\text{Debate}} \approx \text{Tokens}_{\text{B1-SC}} \pm 10\%$ | Debate consumes $+56.25\%$ tokens ($7,500$ vs $4,800$); parity requires $L \le 35$ tokens | **FAIL (CRITICAL)** |
| **RP-02 TOST Power ($N=100, \delta=0.03$)** | Power $\ge 80\%$ to confirm equivalence | True power $= 0.00\%$; 90% CI is $[-7.4\%, +7.4\%]$, failing $[-3\%, +3\%]$ | **FAIL (CRITICAL)** |
| **RP-02 B1-SC Tie Probability ($K=6$)** | Deterministic majority voting | Ties occur in $18.52\%$ of cases at $p=0.70$ and $27.65\%$ at $p=0.60$; 0% gain over $K=5$ | **FAIL (HIGH)** |
| **RP-02 Sycophancy vs Token-Matched B1-SC** | Debate outperforms B1-SC | Token-matched B1-SC ($K=9$) beats Debate by $+7.96\%$ to $+9.20\%$ at $p_0 \in [0.7, 0.8]$ | **CONFIRMED RISK** |
| **RP-01 Timescale Sensitivity ($\lambda=0.995$)** | Robust decay across engine units | Ticks: $t_{1/2}=23$ min ($1.5 \times 10^{-19}$ at 24h); Hours: $t_{1/2}=138$ h ($0.70$ at 72h) | **FAIL (HIGH)** |
| **RP-01 Equal Weights ($\alpha=\beta=\gamma=1.0$)** | Improved retrieval quality | MRR on relevance queries drops by $77.6\%$; overall MRR drops from $0.4010$ to $0.2436$ | **FAIL (HIGH)** |
| **RP-01 Statistical Method Pairing** | Consistent paired methodology | Line 20 specifies Mann-Whitney U (unpaired); line 76 specifies Paired Wilcoxon | **FAIL (MEDIUM)** |

---

## 6. Unchallenged Areas

- **RP-03 (ChatDev SOPs) and RP-04 (Dynamic Orchestration)**: Out of assigned scope for Challenger 1 (assigned to Challenger 2).
- **Physical Wall-Clock Latency on Real Cloud APIs**: Latency values analyzed theoretically based on sequential vs parallel inference structures; live API network jitter was not measured.

---

## 7. Conclusion & Required Changes

### Explicit Verdict: **`REQUEST_CHANGES`**

Before `RP-01` and `RP-02` can be approved for execution in Gate R2, the following mandatory changes must be incorporated into `RD-05`, `RD-06`, `RD-03`, and `RD-04`:

1. **Fix RP-02 Compute Matching (`RD-04` & `RD-06`)**:
   - Replace $K=6$ call matching with **Token-Matched B1-SC** using an odd sample size: $K = 9$ (or $K = 11$), ensuring total token spend matches within $\pm 10\%$.
   - Specify a deterministic tie-breaking protocol for B1-SC majority voting.
2. **Fix RP-02 GSM8K Equivalence Power (`RD-06`)**:
   - Either increase the GSM8K sample size to at least $N = 500$ problem instances, or calibrate the TOST equivalence margin to $\delta = 0.08$ with an explicit power calculation proving $1 - \beta \ge 0.85$.
   - Reconcile the discrepancy between `RD-03:26` ($\Delta < 3\%$) and `RD-06:86` ($\le 2\%$).
3. **Fix RP-01 Timescale & Normalization (`RD-05`)**:
   - Standardize the decay formulation to elapsed simulation seconds: $s_{\text{rec}} = \exp(-\Delta t / \tau)$ with pinned half-life $\tau$ (e.g. 48 hours). Remove ambiguous tick-based formulations and align `DR-15:305` with `RD-05`.
   - Add a epsilon safeguard ($\epsilon = 10^{-6}$) and variance threshold in min-max normalization to prevent division-by-zero and micro-noise amplification.
4. **Fix RP-01 Weighting Specification (`RD-05`)**:
   - Change the primary treatment in `RD-05` to calibrated weights where relevance dominates ($\alpha=0.5, \beta=3.0, \gamma=2.0$), designating equal weighting ($\alpha=\beta=\gamma=1.0$) as an ablation condition.
   - Reconcile the statistical test in `RD-05`: eliminate "Mann-Whitney U" in Section 4 and standardize on Paired Wilcoxon signed-rank test.
5. **Close Threshold Dead Zones (`RD-03`, `RD-05`, `RD-06`)**:
   - Pre-register exhaustive outcome categories for all intervals between success and failure thresholds.

---

## 8. Verification Method

To independently verify all findings and mathematical proofs, execute the self-contained verification scripts in this working directory:

```bash
cd E:\projects\simlab\.agents\phase2_challenger_1
python verify_rp01_rp02_challenges.py
python verify_debate_sycophancy.py
```

### Invalidation Conditions:
This challenge report would be invalidated if:
1. It can be mathematically demonstrated that passing Round 1 debate outputs into Round 2 prompts can be achieved within $\pm 10\%$ tokens of $6(C_0 + L)$ when $L \ge 200$.
2. It can be proven that a paired binary proportion test with $N=100$ achieves $\ge 80\%$ power to confirm equivalence within $[-0.03, +0.03]$ at $\alpha = 0.05$.
