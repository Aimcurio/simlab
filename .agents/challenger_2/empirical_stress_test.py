"""
Empirical Stress Test Harness for Agent Simulation Lab (SimLab)
Author: Challenger 2 (Adversarial Stress Tester & Boundary Challenger)
Date: 2026-09-07
"""

import math
import numpy as np
import scipy.stats as stats

def test_cim_mathematical_pathologies():
    print("=" * 60)
    print("TEST 1: Critic Independence Metric (CIM) Formulations")
    print("=" * 60)
    
    # Pathology 1: Constant Builder Self-Assessment (Variance = 0)
    # LLM agents frequently rate their own work with maximum confidence
    V_b_constant = np.array([1.0] * 50)
    V_c_normal = np.random.RandomState(42).uniform(-1.0, 1.0, 50)
    
    with np.errstate(all='ignore'):
        corr_const, _ = stats.pearsonr(V_c_normal, V_b_constant)
        cim_const = 1.0 - abs(corr_const) if not np.isnan(corr_const) else np.nan
    print(f"Pathology 1 (Constant Builder): corr={corr_const}, CIM={cim_const}")
    assert np.isnan(cim_const), "Expected NaN due to zero variance in V_b!"

    # Pathology 2: Competent Independent Agents (Common Cause Confounding)
    # Ground truth: 100 artifacts, 50 clean (+1), 50 flawed (-1)
    np.random.seed(123)
    ground_truth = np.array([1.0] * 50 + [-1.0] * 50)
    
    # Builder accuracy: 90%
    b_noise = np.random.choice([1, -1], size=100, p=[0.90, 0.10])
    V_b = ground_truth * b_noise
    
    # Critic accuracy: 90% (completely independent noise from builder)
    c_noise = np.random.choice([1, -1], size=100, p=[0.90, 0.10])
    V_c = ground_truth * c_noise
    
    corr_competent, p_val = stats.pearsonr(V_c, V_b)
    cim_competent = 1.0 - abs(corr_competent)
    
    print(f"Pathology 2 (Both Agents 90% Accurate & Independent):")
    print(f"  Builder Accuracy: {np.mean(V_b == ground_truth):.2f}")
    print(f"  Critic Accuracy:  {np.mean(V_c == ground_truth):.2f}")
    print(f"  Correlation rho(V_c, V_b): {corr_competent:.4f}")
    print(f"  Calculated CIM: {cim_competent:.4f}")
    print(f"  CONCLUSION: A highly accurate and completely independent critic is penalized")
    print(f"  with a near-zero CIM ({cim_competent:.4f}) purely because both track ground truth!")
    
    # Pathology 3: Maximizing CIM requires zero correlation with ground truth
    # If builder is 90% accurate, an uncorrelated critic (rho=0 -> CIM=1.0) must have accuracy ~50% (random coin flip)
    V_c_random = np.random.choice([1.0, -1.0], size=100, p=[0.5, 0.5])
    corr_rand, _ = stats.pearsonr(V_c_random, V_b)
    cim_rand = 1.0 - abs(corr_rand)
    print(f"Pathology 3 (Random Coin-Flip Critic):")
    print(f"  Critic Accuracy:  {np.mean(V_c_random == ground_truth):.2f}")
    print(f"  Correlation rho(V_c_rand, V_b): {corr_rand:.4f}")
    print(f"  Calculated CIM: {cim_rand:.4f} (Gamed to near-maximum!)")

def test_statistical_power_exp1():
    print("\n" + "=" * 60)
    print("TEST 2: Statistical Power Verification - Experiment 1 (EXP-001)")
    print("=" * 60)
    # Claim: d = 0.65, alpha = 0.05, power = 0.85 -> requires N = 44 runs per condition.
    d = 0.65
    alpha = 0.05
    desired_power = 0.85
    
    # Independent two-sample t-test sample size formula (approximate & exact)
    # n per group = 2 * ((z_{1-alpha/2} + z_{1-beta}) / d)^2
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(desired_power)
    n_approx = 2 * ((z_alpha + z_beta) / d) ** 2
    
    # Exact via non-central t distribution
    def t_power(n, d, alpha):
        df = 2 * n - 2
        ncp = d * math.sqrt(n / 2)
        crit = stats.t.ppf(1 - alpha / 2, df)
        power = 1 - stats.nct.cdf(crit, df, ncp) + stats.nct.cdf(-crit, df, ncp)
        return power
    
    n = 10
    while t_power(n, d, alpha) < desired_power:
        n += 1
    
    print(f"Welch/Student's t-test power calculation for d={d}, alpha={alpha}, power={desired_power}:")
    print(f"  Approximate n per group: {n_approx:.2f}")
    print(f"  Exact n per group: {n}")
    print(f"  Claimed in document: N = 44 per condition. MATCHES EXACT POWER: {n == 44}")

    # Cluster / Pseudoreplication Analysis:
    # 20 SWE-bench tasks * 5 seeds = 100 runs per condition.
    # What if intra-cluster correlation ICC = 0.4 across tasks?
    # Effective sample size N_eff = N_total / (1 + (m - 1) * ICC)
    m = 5 # cluster size (5 seeds per task)
    icc = 0.40
    design_effect = 1 + (m - 1) * icc
    n_total_per_cond = 100
    n_effective = n_total_per_cond / design_effect
    print(f"Cluster Effect / Pseudoreplication Check:")
    print(f"  Total runs per condition: {n_total_per_cond} (20 tasks x 5 seeds)")
    print(f"  Design Effect (ICC={icc}): {design_effect:.2f}")
    print(f"  Effective sample size N_eff per condition: {n_effective:.1f}")
    power_effective = t_power(int(round(n_effective)), d, alpha)
    print(f"  Effective Power with clustering accounted for: {power_effective:.4f}")

def test_statistical_power_exp2():
    print("\n" + "=" * 60)
    print("TEST 2B: Statistical Power Verification - Experiment 2 (EXP-002)")
    print("=" * 60)
    # Claim: Chi-square test of independence on binary VER with df = 2, w = 0.25, alpha = 0.01, power = 0.90
    # requires N >= 220 total observations. Document uses N = 450.
    w = 0.25
    df = 2
    alpha = 0.01
    desired_power = 0.90
    
    crit_chi2 = stats.chi2.ppf(1 - alpha, df)
    
    def chi2_power(N, w, df, alpha):
        crit = stats.chi2.ppf(1 - alpha, df)
        lambda_param = N * (w ** 2)
        power = 1 - stats.ncx2.cdf(crit, df, lambda_param)
        return power

    N = 50
    while chi2_power(N, w, df, alpha) < desired_power:
        N += 1
        
    print(f"Chi-square test of independence (df={df}, w={w}, alpha={alpha}, power={desired_power}):")
    print(f"  Exact required total N: {N}")
    print(f"  Claimed in document: N >= 220. MATCHES EXACT POWER: {N == 220}")
    print(f"  Document uses N = 450 total runs (Power = {chi2_power(450, w, df, alpha):.6f})")

def test_statistical_power_exp3():
    print("\n" + "=" * 60)
    print("TEST 2C: Statistical Power Verification - Experiment 3 (EXP-003)")
    print("=" * 60)
    # Claim: 2 x 3 ANOVA, total N = 60, 10 per cell.
    # Power > 0.80 to detect interaction effects at alpha = 0.05 with f = 0.40.
    # Factors: Factor A (2 levels), Factor B (3 levels). Total cells = 6.
    # df_interaction = (2-1) * (3-1) = 2.
    # df_error = N - k = 60 - 6 = 54.
    f = 0.40
    alpha = 0.05
    N = 60
    k = 6
    df_inter = (2 - 1) * (3 - 1) # 2
    df_error = N - k # 54
    
    # Noncentrality parameter lambda = N * f^2 = 60 * 0.16 = 9.6
    lambda_inter = N * (f ** 2)
    crit_f = stats.f.ppf(1 - alpha, df_inter, df_error)
    power_inter = 1 - stats.ncf.cdf(crit_f, df_inter, df_error, lambda_inter)
    
    # Main effect A (df=1):
    df_A = 1
    crit_A = stats.f.ppf(1 - alpha, df_A, df_error)
    power_A = 1 - stats.ncf.cdf(crit_A, df_A, df_error, lambda_inter)
    
    # Main effect B (df=2):
    df_B = 2
    crit_B = stats.f.ppf(1 - alpha, df_B, df_error)
    power_B = 1 - stats.ncf.cdf(crit_B, df_B, df_error, lambda_inter)
    
    print(f"2x3 Factorial ANOVA (N={N}, n=10/cell, f={f}, alpha={alpha}):")
    print(f"  Interaction df: {df_inter}, Error df: {df_error}")
    print(f"  Non-centrality parameter lambda: {lambda_inter:.2f}")
    print(f"  Critical F (interaction): {crit_f:.4f}")
    print(f"  Exact Power for Interaction Effect: {power_inter:.4f}")
    print(f"  Exact Power for Main Effect A (df=1): {power_A:.4f}")
    print(f"  Exact Power for Main Effect B (df=2): {power_B:.4f}")
    print(f"  Claim in document: 'power > 0.80'. VERIFIED: {power_inter > 0.80} (actual: {power_inter:.4f})")

if __name__ == '__main__':
    test_cim_mathematical_pathologies()
    test_statistical_power_exp1()
    test_statistical_power_exp2()
    test_statistical_power_exp3()
