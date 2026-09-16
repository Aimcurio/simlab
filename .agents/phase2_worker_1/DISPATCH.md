# DISPATCH: Phase 2 Remediation Worker 1

- **Role**: Versatile Worker (`teamwork_preview_worker`)
- **Working Directory**: `E:\projects\simlab\.agents\phase2_worker_1`
- **Assigned Deliverables**:
  - `E:\projects\simlab\reproduction_design\RD-01_reproduction_priority_matrix.md`
  - `E:\projects\simlab\reproduction_design\RD-03_experimental_hypothesis_register.md`
  - `E:\projects\simlab\reproduction_design\RD-04_baseline_compute_matching.md`
  - `E:\projects\simlab\reproduction_design\RD-05_rp01_experiment_design.md`
  - `E:\projects\simlab\reproduction_design\RD-06_rp02_experiment_design.md`
  - `E:\projects\simlab\reproduction_design\RD-07_rp03_experiment_design.md`
  - `E:\projects\simlab\reproduction_design\RD-08_rp04_experiment_design.md`
  - `E:\projects\simlab\reproduction_design\RD-09_metrics_evaluation_contract.md`
  - `E:\projects\simlab\reproduction_design\RD-10_reproducibility_telemetry_contract.md`
  - `E:\projects\simlab\reproduction_design\RD-12_cost_token_latency_budget.md`

## Context & Input Reports:
- `E:\projects\simlab\ORIGINAL_REQUEST.md` (MANDATORY: read first)
- Reviewer 1 Handoff: `E:\projects\simlab\.agents\phase2_reviewer_1\handoff.md`
- Challenger 1 Handoff: `E:\projects\simlab\.agents\phase2_challenger_1\handoff.md`
- Challenger 2 Handoff: `E:\projects\simlab\.agents\phase2_challenger_2\handoff.md`

## Mandatory Warning:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Remediation Tasks:
1. **RP-02 Compute-Matching & Token Parity (RD-04 & RD-06)**:
   - Implement Dual-Control Protocol: (a) $B_{1-SC-calls}$ ($K=7$, odd to eliminate majority ties) and (b) $B_{1-SC-tokens}$ ($K=10$, strictly matching the $+50\%$ multi-turn debate token overhead).
   - Add deterministic tie-breaking rules (highest mean logprob or lowest index).
   - Expand GSM8K sample size to $N=500$ problems to ensure $>80\%$ power under TOST with margin $\delta = 0.03$.
   - Replace Two-Way ANOVA with Binomial Generalized Linear Mixed Model (GLMM with logit link) for binary accuracy outcomes.
2. **RP-01 Timescale & Weight Sensitivity (RD-05)**:
   - Explicitly define $\Delta t$ in hours ($s_{rec} = 0.995^{\Delta t_{hours}}$, half-life $138$ hours) and explicitly document translation to 10-second simulation ticks to avoid half-life distortion.
   - In conditions, evaluate both published equal weights ($\alpha=\beta=\gamma=1.0$) and calibrated code weights ($\alpha=0.5, \beta=3.0, \gamma=2.0$).
3. **RP-03 Sample Size & Construct Validity (RD-07)**:
   - Expand sample size from $N=50$ to $N=150$ tasks for $>80\%$ power under McNemar's test ($\alpha=0.01$).
   - Supplement single-function tasks with multi-file tasks (SWE-bench Lite mini / complex modular tasks) so that a 4-role hierarchy is construct-valid.
4. **RP-04 Sample Size, Baselines & Test Selection (RD-08)**:
   - Expand sample size from $N=100$ to $N=300$ tasks for $>80\%$ power.
   - Include compute-matched single-agent control (`B1-SC`) alongside fixed waterfall $B_3$ per RD-04 and NC-05.
   - Add strict 70/30 train/test split.
   - Replace Pearson Chi-square with Cochran's Q test for matched binary blocks.
5. **Inconclusive Outcomes (RD-03 & RD-05–RD-08)**:
   - Explicitly define `INCONCLUSIVE_SUB_THRESHOLD` outcome states across all experiments, specifying default architecture recommendations (defaulting to simpler baseline).
6. **Budget Correction (RD-12)**:
   - Update API token expenditures and costs to reflect the expanded sample sizes and true multi-turn context ($63.50 USD).

Maintain all 35 schema fields in RD-05 through RD-08. When finished, produce a detailed handoff report at:
`E:\projects\simlab\.agents\phase2_worker_1\handoff.md`

## 2026-09-16T09:47:00Z
<USER_REQUEST>
You are Phase 2 Remediation Worker 1 for Curo SimLab.
Working directory: E:\projects\simlab\.agents\phase2_worker_1
Authoritative Request: E:\projects\simlab\ORIGINAL_REQUEST.md (MANDATORY: read first).
Dispatch Instructions: E:\projects\simlab\.agents\phase2_worker_1\DISPATCH.md

Your task is to remediate the methodological, baseline, sample size, and statistical issues identified by Reviewer 1, Challenger 1, and Challenger 2 across:
- E:\projects\simlab\reproduction_design\RD-01_reproduction_priority_matrix.md
- E:\projects\simlab\reproduction_design\RD-03_experimental_hypothesis_register.md
- E:\projects\simlab\reproduction_design\RD-04_baseline_compute_matching.md
- E:\projects\simlab\reproduction_design\RD-05_rp01_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-06_rp02_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-07_rp03_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-08_rp04_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-09_metrics_evaluation_contract.md
- E:\projects\simlab\reproduction_design\RD-10_reproducibility_telemetry_contract.md
- E:\projects\simlab\reproduction_design\RD-12_cost_token_latency_budget.md

Mandatory Warning: DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work.

Execute all remediation tasks in DISPATCH.md:
1. RP-02: Dual-Control Protocol (B1-SC-calls at K=7, B1-SC-tokens at K=10), tie-breaker rules, N=500 sample size, Binomial GLMM.
2. RP-01: Timescale unit clarification (hours vs ticks), equal vs calibrated weights.
3. RP-03: Sample size expansion (N=150), multi-file SWE-bench Lite mini tasks.
4. RP-04: Sample size expansion (N=300), B1-SC compute-matched control, 70/30 train/test split, Cochran's Q test.
5. Inconclusive outcome states (INCONCLUSIVE_SUB_THRESHOLD) defaulting to simpler baselines.
6. Correct API token expenditures and costs in RD-12 ($63.50).

Maintain all 35 schema fields in RD-05 to RD-08.
Produce your handoff report at:
E:\projects\simlab\.agents\phase2_worker_1\handoff.md
When complete, send a message to parent with your summary.
</USER_REQUEST>
