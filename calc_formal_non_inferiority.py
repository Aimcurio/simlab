import json
import math
from pathlib import Path
import numpy as np
import scipy.stats as stats

ROOT = Path(__file__).resolve().parent
with open(ROOT / "phase4_execution" / "telemetry" / "exp_ab_01_comp" / "exp_ab_01_comp_telemetry.jsonl", "r", encoding="utf-8") as f:
    events = [json.loads(line) for line in f]

a4_events = [e for e in events if e['condition_code'] == 'A4']
a7_events = [e for e in events if e['condition_code'] == 'A7']

# ensure ordered by query_id
a4_events.sort(key=lambda x: x['query_id'])
a7_events.sort(key=lambda x: x['query_id'])

a4_mrrs = np.array([e['reciprocal_rank'] for e in a4_events])
a7_mrrs = np.array([e['reciprocal_rank'] for e in a7_events])
diffs = a4_mrrs - a7_mrrs

N = len(diffs)
mean_diff = np.mean(diffs)
std_diff = np.std(diffs, ddof=1)
se_diff = std_diff / math.sqrt(N)

margin = 0.02 # delta <= 0.02
# Test H0: mu_d <= -0.02 vs H1: mu_d > -0.02
t_stat = (mean_diff - (-margin)) / se_diff
p_val_t_onesided = 1.0 - stats.t.cdf(t_stat, df=N-1)

# Lower confidence bounds:
# For alpha = 0.05 (95% one-sided LCB):
t_crit_05 = stats.t.ppf(1 - 0.05, df=N-1)
lcb_95 = mean_diff - t_crit_05 * se_diff

# For alpha = 0.01 (99% one-sided LCB):
t_crit_01 = stats.t.ppf(1 - 0.01, df=N-1)
lcb_99 = mean_diff - t_crit_01 * se_diff

# For Bonferroni alpha = 0.00142857 (99.857% one-sided LCB):
alpha_bonf = 0.01 / 7.0
t_crit_bonf = stats.t.ppf(1 - alpha_bonf, df=N-1)
lcb_bonf = mean_diff - t_crit_bonf * se_diff

# Non-parametric: Wilcoxon signed-rank test against shift -margin
shifted_diffs = diffs - (-margin)
nonzero_shifted = shifted_diffs[shifted_diffs != 0]
w_stat, p_val_w_onesided = stats.wilcoxon(nonzero_shifted, alternative='greater')

print(f"Sample size N = {N}")
print(f"Mean difference (A4 - A7): {mean_diff:.6f}")
print(f"Std dev of difference:     {std_diff:.6f}")
print(f"Std error of difference:   {se_diff:.6f}")
print(f"Non-inferiority margin:    -{margin:.4f}")
print(f"T-statistic (vs -0.02):    {t_stat:.4f} (df={N-1})")
print(f"One-sided p-value (t):     {p_val_t_onesided:.4e}")
print(f"One-sided 95% LCB (a=0.05): {lcb_95:.6f}")
print(f"One-sided 99% LCB (a=0.01): {lcb_99:.6f}")
print(f"One-sided Bonferroni LCB:   {lcb_bonf:.6f}")
print(f"Wilcoxon W (shifted):       {w_stat:.1f}")
print(f"One-sided p-value (W):      {p_val_w_onesided:.4e}")
