## 2026-09-16T21:54:00Z

<USER_REQUEST>
# Teamwork Project Prompt

Perform a bounded scientific audit of CURO SIMLAB EXP-AB-01-COMP before dispatching the next Phase 4 experiment, distinguishing real mechanisms from implementation defects, benchmark artifacts, or measurement errors.

Working directory: `E:\projects\simlab\audits\EXP-AB-01-COMP`
Integrity mode: development

## Requirements

### R1. PRESERVE OBSERVED RESULTS
Treat the existing raw results as immutable evidence. Do not rewrite or suppress the existing MRR scores (A2: 0.5130, A4: 0.5002, A7: 0.0941, A3: 0.0086, A8: 0.0325). Preserve all hashes, telemetry, seeds, and run IDs. Do not rerun the experiment unless the audit identifies a defect requiring a preregistered corrective rerun. Do not advance to another Phase 4 experiment.

### R2. CORRECT NON-INFERIORITY ADJUDICATION
Verify the preregistered non-inferiority procedure for A4 vs A7. Determine if a formal one-sided non-inferiority test or confidence-bound comparison against the preregistered margin was performed. If yes, report the statistic, bound, alpha, and decision. If no, use `NON_INFERIORITY_DIRECTION_SUPPORTED_PENDING_FORMAL_TEST` or similar. Do not infer formal non-inferiority from a two-sided Wilcoxon p-value alone.

### R3. CORRECT IMPORTANCE-NECESSITY INTERPRETATION
Address the contradiction that A4 (recency+relevance) outperformed A7 (full tri-factor) by ~+0.4061 MRR. Explain the result using effect direction, effect magnitude, confidence interval, and statistical test. Do not claim the hypothesis is rejected simply because p is very small; explain the directional failure of the full tri-factor condition.

### R4. MECHANISTIC FAILURE AUDIT
Inspect importance, relevance, and recency score distributions (min, max, mean, variance, quantiles). Verify normalization method, sign/direction semantics, weight application, score combination, tie handling, sorting direction, rank construction, and candidate-set construction. Specifically test for scale dominance, scale inversion, normalization mismatch, weight application error, reflection score dominance, duplicate crowding, label leakage, and benchmark bias. Do not assume; test them.

### R5. REFLECTION FAILURE ANALYSIS
Determine why A8 produced 100% Rank-1 crowding, 100/100 queries affected, and all top-five slots occupied by reflection nodes. Inspect differences in relevance, importance, recency, embedding similarity, metadata, eligibility, and duplication rate between reflection nodes and ordinary nodes. Classify as REAL_PRIMITIVE_FAILURE, IMPLEMENTATION_DEFECT, BENCHMARK_ARTIFACT, SCORING_SCALE_ARTIFACT, or UNRESOLVED_MECHANISM.

### R6. VALIDATE WEIGHT CONFIGURATIONS
Verify that every A1-A8 configuration exactly matches AS-03 preregistration (especially A4 = recency+relevance, A7 = full tri-factor, A8 = A7 + reflection). Record expected_weights, executed_weights, and match?. If any mismatch exists, output `EXPERIMENT_CONFIGURATION_DRIFT` and stop progression.

### R7. CHECK PHASE 3 COMPATIBILITY
Compare this result with Phase 3 RP-01 findings. Determine if the Phase 4 tri-factor collapse is consistent, a different weight regime, a different benchmark regime, a different retrieval implementation, or a true contradiction. Do not silently reconcile. Record `PHASE3_PHASE4_EVIDENCE_CONFLICT` if necessary.

### R8. PRIMITIVE EVIDENCE STATUS
Update only Criterion B (ABLATION_EVIDENCE) for PR-COG-01. Do not adjudicate globally. Do not freeze architecture. Use statuses: SUPPORTED, SUPPORTED_WITH_CONSTRAINTS, COMPONENT_NOT_NECESSARY_UNDER_TESTED_CONDITIONS, MECHANISTIC_FAILURE_UNDER_INVESTIGATION, or EVIDENCE_CONFLICT.

### R9. LESSONS LEARNED
Capture validated lessons as forward constraints (e.g., scale compatibility, reflection admission controls, directional interpretation). Only promote lessons actually supported by the audit.

### R10. GATE TO NEXT EXPERIMENT
Return exactly one of the following statuses. Do not automatically execute the next experiment:
- STAGE_4A_RESULT_VALID_NEXT_EXPERIMENT_ALLOWED
- STAGE_4A_CORRECTIVE_RERUN_REQUIRED
- STAGE_4A_MECHANISTIC_INVESTIGATION_REQUIRED
- STAGE_4A_EVIDENCE_CONFLICT_REQUIRES_REVIEW

## Acceptance Criteria

### Execution Constraints
- [ ] No experiments were rerun unless explicitly triggered by a preregistered corrective rerun finding.
- [ ] No advancement to subsequent Phase 4 experiments occurred.
- [ ] The "CURO INVARIANT" was respected: Extreme effects were treated as evidence to be mechanistically diagnosed, not automatic truth.

### Required Output Sections
- [ ] A. Statistical Adjudication Correction
- [ ] B. Non-Inferiority Verification
- [ ] C. Importance-Necessity Interpretation
- [ ] D. Score-Distribution Audit
- [ ] E. Reflection Mechanism Analysis
- [ ] F. Configuration Integrity Check
- [ ] G. Phase 3 / Phase 4 Compatibility
- [ ] H. PR-COG-01 Evidence Update
- [ ] I. Lessons Learned / Forward Constraints
- [ ] J. Stage 4A Decision
- [ ] K. Next Approved Action
</USER_REQUEST>
