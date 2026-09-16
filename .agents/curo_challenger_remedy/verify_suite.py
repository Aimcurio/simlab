import os
import re
import numpy as np
from scipy import stats

def test_token_formula():
    print('=== TEST 1: Token Formula Derivation & Values ===')
    def closed_form(N, R, C0=500, L=300):
        return N * R * (C0 + L) + (N**2 * L * R * (R - 1)) // 2
    
    def legacy_form(N, R, L=300):
        return sum(N * r * L for r in range(1, R + 1))
    
    test_cases = [
        (3, 2, 500, 300, 7500, 2700, 2.78),
        (3, 3, 500, 300, 15300, 5400, 2.83),
        (5, 3, 500, 300, 34500, 9000, 3.83),
        (8, 4, 500, 300, 140800, 24000, 5.87)
    ]
    
    for N, R, C0, L, expected_true, expected_legacy, expected_factor in test_cases:
        true_val = closed_form(N, R, C0, L)
        legacy_val = legacy_form(N, R, L)
        factor = true_val / legacy_val
        print(f'N={N}, R={R}: True={true_val} (exp {expected_true}), Legacy={legacy_val} (exp {expected_legacy}), Factor={factor:.2f}x (exp {expected_factor:.2f}x)')
        assert true_val == expected_true, f'Mismatch in true value for N={N}, R={R}'
        assert legacy_val == expected_legacy, f'Mismatch in legacy value for N={N}, R={R}'
        assert abs(factor - expected_factor) < 0.015, f'Mismatch in factor for N={N}, R={R}'
    print('PASS: Token formula exact values and discrepancy factors confirmed!\n')

def test_statistical_power():
    print('=== TEST 2: Statistical Power Re-computation ===')
    
    # EXP-001
    p1 = 0.15
    p2 = 0.30
    delta = 0.15
    
    def prop_power(n_eff, p1, p2, alpha=0.05):
        p_bar = (p1 + p2) / 2
        se_null = np.sqrt(2 * p_bar * (1 - p_bar) / n_eff)
        se_alt = np.sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / n_eff)
        z_crit = stats.norm.ppf(1 - alpha/2)
        z_power = (delta - z_crit * se_null) / se_alt
        return stats.norm.cdf(z_power)
    
    power_legacy_57 = prop_power(57.69, p1, p2)
    print(f'EXP-001 legacy power (n_eff=57.69): {power_legacy_57:.4f} (expected ~0.4875 / 48.8%)')
    assert abs(power_legacy_57 - 0.4875) < 0.01
    
    power_rem_138 = prop_power(138.46, p1, p2)
    print(f'EXP-001 remediated power (rho=0.40, n_eff=138.46): {power_rem_138:.4f} (expected >= 0.85)')
    assert power_rem_138 >= 0.85, 'EXP-001 power below 0.85 under DE=2.6'
    
    power_rem_225 = prop_power(225.0, p1, p2)
    print(f'EXP-001 remediated power (rho=0.15, n_eff=225.0): {power_rem_225:.4f} (expected > 0.95)')
    assert power_rem_225 > 0.95, 'EXP-001 power below 0.95 under DE=1.6'
    
    # EXP-002 Cochran's Q
    alpha_01 = 0.01
    df_q = 2
    chi2_crit = stats.chi2.ppf(1 - alpha_01, df=df_q)
    w = 0.25
    
    # legacy blocks = 150
    lam_150 = 150 * (w**2)
    power_q_150 = 1 - stats.ncx2.cdf(chi2_crit, df=df_q, nc=lam_150)
    print(f'EXP-002 legacy power (N_blocks=150): {power_q_150:.4f} (expected ~0.5770 / 57.7%)')
    assert abs(power_q_150 - 0.5770) < 0.01
    
    # if total cells = 450
    lam_450 = 450 * (w**2)
    power_q_450 = 1 - stats.ncx2.cdf(chi2_crit, df=df_q, nc=lam_450)
    print(f'EXP-002 false power if cell count used (N=450): {power_q_450:.4f} (expected ~0.9916)')
    assert abs(power_q_450 - 0.9916) < 0.01
    
    # remediated blocks = 280
    lam_280 = 280 * (w**2)
    power_q_280 = 1 - stats.ncx2.cdf(chi2_crit, df=df_q, nc=lam_280)
    print(f'EXP-002 remediated power (N_blocks=280): {power_q_280:.4f} (expected >= 0.90 / ~0.903)')
    assert power_q_280 >= 0.90, 'EXP-002 power below 0.90 under 280 matched blocks'
    
    # EXP-003 ANOVA interaction
    df1 = 2
    df2 = 66
    f_crit = stats.f.ppf(0.95, df1, df2)
    lam_f = 72 * (0.40**2)  # 11.52
    power_f = 1 - stats.ncf.cdf(f_crit, df1, df2, lam_f)
    print(f'EXP-003 ANOVA interaction power (N=72, f=0.40): {power_f:.4f} (expected ~0.8527 > 0.80)')
    assert power_f > 0.85, 'EXP-003 power below 0.85'
    print('PASS: Statistical power calculations confirmed!\n')

if __name__ == '__main__':
    test_token_formula()
    test_statistical_power()
