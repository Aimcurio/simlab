# Plan: Remedy Worker 1

Working Directory: `E:\projects\simlab\.agents\remedy_worker_1\`
Target Deliverable: `E:\projects\simlab\audits\EXP-AB-01-COMP\AUDIT_EXP_AB_01_COMP.md`

Remediation Tasks:
1. Incorporate audit_challenger_1 findings:
   - Disclose RELEVANCE_DOMINANT sub-cohort in Section C.3 (A4 MRR 0.0277 vs A7 MRR 0.0675, Delta -0.0398, p=2.78e-10, A7 wins 32/40).
   - Qualify superiority in Executive Summary and Section B.5.
   - Update NC-74 and MI-01 with query-intent gating.
2. Incorporate audit_challenger_2 findings:
   - High-res 5151-point simplex sweep in Section C.4 and D.4: global optimum (0.06, 0.94, 0.00) MRR 0.7535, 390 interior points beating baseline A4.
   - Normalization stress tests: Softmax rescues A7 to 0.6705, but A4 to 0.9650.
   - 80-seed step-function phase transition at reflection importance >= 6.0 in Section E.3.
3. Incorporate audit_forensic_auditor clerical fix:
   - Update exp_ab_01_comp_results.json hash to 70eb26a84f348463217d14689310d3ca22d29948be4209fe2855fcdc58e6cc56 in line 51.
4. Run all test suites: verify_audit.py, test_audit_verification.py, test_challenger_empirical.py.
