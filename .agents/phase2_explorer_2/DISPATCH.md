# DISPATCH: Phase 2 Explorer 2

- **Role**: Read-only Exploration Agent (`teamwork_preview_explorer`)
- **Working Directory**: `E:\projects\simlab\.agents\phase2_explorer_2`
- **Assigned Scope**: Deep audit of the 4 Experiment Specification Records:
  - `E:\projects\simlab\reproduction_design\RD-05_rp01_experiment_design.md` (RP-01: Smallville Memory Inversion)
  - `E:\projects\simlab\reproduction_design\RD-06_rp02_experiment_design.md` (RP-02: Multi-Agent Debate vs B1-SC)
  - `E:\projects\simlab\reproduction_design\RD-07_rp03_experiment_design.md` (RP-03: ChatDev Phase Sandboxing)
  - `E:\projects\simlab\reproduction_design\RD-08_rp04_experiment_design.md` (RP-04: Evolving Orchestration RL Policy)
- **Context Files**:
  - `E:\projects\simlab\ORIGINAL_REQUEST.md` (MUST read before starting)
  - `E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md`
  - `E:\projects\simlab\deliverables\DR-12_proposed_experiment_matrix.md`

## Objectives:
1. Conduct an exhaustive schema audit against all 35 required Experiment Specification Record fields:
   1. experiment_id, 2. reproduction_candidate, 3. research_question, 4. falsifiable_hypothesis, 5. null_hypothesis, 6. primitive_under_test, 7. reference_mechanism, 8. baseline, 9. treatment, 10. independent_variables, 11. dependent_variables, 12. controlled_variables, 13. model_configuration, 14. prompt_configuration, 15. context_configuration, 16. randomness_configuration, 17. dataset_or_environment, 18. minimum_run_count, 19. statistical_method, 20. success_threshold, 21. failure_threshold, 22. termination_condition, 23. token_budget, 24. latency_budget, 25. compute_budget, 26. logging_requirements, 27. provenance_requirements, 28. known_confounds, 29. expected_failure_modes, 30. what_result_supports, 31. what_result_does_not_support, 32. external_validity_limits, 33. architecture_implication_if_positive, 34. architecture_implication_if_negative, 35. execution_authority.
2. Verify that NO field is missing, placeholder, or ambiguous across all 4 files.
3. Verify deterministic-first measurement, statistical test rigor (power calculations, test selection, non-parametric where needed), pre-registered failure thresholds.
4. Verify execution authority is explicitly set to `NOT_GRANTED` in all 4 records.

Produce a comprehensive handoff report at `E:\projects\simlab\.agents\phase2_explorer_2\handoff.md` with an explicit 35-field compliance table for each candidate.

## 2026-09-16T09:34:20Z

User Request:
You are Phase 2 Explorer 2 for Curo SimLab.
Working directory: E:\projects\simlab\.agents\phase2_explorer_2
Authoritative Request: E:\projects\simlab\ORIGINAL_REQUEST.md (MANDATORY: read this file first before starting work).
Dispatch Instructions: E:\projects\simlab\.agents\phase2_explorer_2\DISPATCH.md

Your task is to conduct an exhaustive audit of the 4 Experiment Specification Records:
- E:\projects\simlab\reproduction_design\RD-05_rp01_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-06_rp02_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-07_rp03_experiment_design.md
- E:\projects\simlab\reproduction_design\RD-08_rp04_experiment_design.md

Verify:
1. Exhaustive presence and quality of all 35 required schema fields in EVERY record:
   1. experiment_id, 2. reproduction_candidate, 3. research_question, 4. falsifiable_hypothesis, 5. null_hypothesis, 6. primitive_under_test, 7. reference_mechanism, 8. baseline, 9. treatment, 10. independent_variables, 11. dependent_variables, 12. controlled_variables, 13. model_configuration, 14. prompt_configuration, 15. context_configuration, 16. randomness_configuration, 17. dataset_or_environment, 18. minimum_run_count, 19. statistical_method, 20. success_threshold, 21. failure_threshold, 22. termination_condition, 23. token_budget, 24. latency_budget, 25. compute_budget, 26. logging_requirements, 27. provenance_requirements, 28. known_confounds, 29. expected_failure_modes, 30. what_result_supports, 31. what_result_does_not_support, 32. external_validity_limits, 33. architecture_implication_if_positive, 34. architecture_implication_if_negative, 35. execution_authority.
2. Confirm that NO field is omitted, placeholder, or ambiguous.
3. Check deterministic-first measurement, statistical test rigor, power/sample sizes, pre-registered failure thresholds.
4. Confirm execution_authority = NOT_GRANTED in all 4 records.

Produce your structured handoff report with a 35-field compliance matrix at:
E:\projects\simlab\.agents\phase2_explorer_2\handoff.md
Update progress.md regularly. When complete, send a message to parent with your summary.
