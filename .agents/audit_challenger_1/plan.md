# Plan: Audit Challenger 1 (Statistical & Sub-Population Stress Testing)

Working Directory: `E:\projects\simlab\.agents\audit_challenger_1\`
Deliverable Under Review: `E:\projects\simlab\audits\EXP-AB-01-COMP\AUDIT_EXP_AB_01_COMP.md`
Mission:
Adversarially challenge statistical adjudication:
- Test query sub-populations (40 recency-sensitive, 40 relevance-dominant, 20 temporal-conflict queries). Does A4 outperform A7 in all 3 sub-cohorts?
- Run permutation and bootstrap tests on non-inferiority margin delta=0.02 and delta=0.05.
- Verify whether outlier queries could skew Cohen's d or LCB.
Deliver Verdict: APPROVE or REQUEST_CHANGES in `handoff.md`.
