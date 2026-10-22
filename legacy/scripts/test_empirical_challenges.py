import numpy as np
import scipy.stats as stats
from scipy.stats import binom, betabinom

print("=" * 80)
print("TEST 1: SMALLVILLE RETRIEVAL DECAY INVERSION & WEIGHT SENSITIVITY")
print("=" * 80)

def normalize_dict_floats(d, target_min=0.0, target_max=1.0):
    min_val = min(d.values())
    max_val = max(d.values())
    if max_val == min_val:
        return {k: target_max for k in d}
    return {k: (v - min_val) / (max_val - min_val) * (target_max - target_min) + target_min for k, v in d.items()}

def extract_recency(nodes, recency_decay=0.99):
    # Smallville retrieve.py:145-146
    recency_vals = [recency_decay ** i for i in range(1, len(nodes) + 1)]
    return {n['node_id']: val for n, val in zip(nodes, recency_vals)}

print("Checking mathematical decay inversion across different N:")
for N in [2, 5, 10, 50, 100, 500, 1000]:
    nodes = [{'node_id': f'node_{i}', 'last_accessed': i} for i in range(1, N + 1)]
    nodes_sorted = sorted(nodes, key=lambda x: x['last_accessed'])
    raw_rec = extract_recency(nodes_sorted, recency_decay=0.99)
    norm_rec = normalize_dict_floats(raw_rec)
    oldest_id = nodes_sorted[0]['node_id']
    newest_id = nodes_sorted[-1]['node_id']
    print(f"N={N:4d} | Oldest ({oldest_id}, t=1): raw={raw_rec[oldest_id]:.6f}, norm={norm_rec[oldest_id]:.6f} | "
          f"Newest ({newest_id}, t={N}): raw={raw_rec[newest_id]:.6e}, norm={norm_rec[newest_id]:.6f}")

# Sensitivity and Component Correlation Analysis
np.random.seed(42)
N_mem = 100
nodes_full = []
for i in range(1, N_mem + 1):
    nodes_full.append({
        'node_id': f'node_{i}',
        'last_accessed': i, # t=1 is oldest, t=100 is newest
        'importance': np.random.randint(1, 11), # 1 to 10
        'relevance': np.random.beta(2, 5) # beta distribution [0, 1]
    })

nodes_sorted = sorted(nodes_full, key=lambda x: x['last_accessed'])
rec_dict = normalize_dict_floats(extract_recency(nodes_sorted, 0.99))
imp_dict = normalize_dict_floats({n['node_id']: n['importance'] for n in nodes_sorted})
rel_dict = normalize_dict_floats({n['node_id']: n['relevance'] for n in nodes_sorted})

# Scenario A: Smallville Code weights gw = [0.5, 3, 2] (Inverted Recency)
score_code = {n['node_id']: 0.5 * rec_dict[n['node_id']] + 3.0 * rel_dict[n['node_id']] + 2.0 * imp_dict[n['node_id']] for n in nodes_sorted}
# Scenario B: Claimed Paper weights gw = [1, 1, 1] (Inverted Recency)
score_paper = {n['node_id']: 1.0 * rec_dict[n['node_id']] + 1.0 * rel_dict[n['node_id']] + 1.0 * imp_dict[n['node_id']] for n in nodes_sorted}
# Scenario C: Corrected Recency (Newest=1, Oldest=0) with Paper weights gw = [1, 1, 1]
rec_dict_corrected = {n['node_id']: 1.0 - rec_dict[n['node_id']] for n in nodes_sorted}
score_corrected = {n['node_id']: 1.0 * rec_dict_corrected[n['node_id']] + 1.0 * rel_dict[n['node_id']] + 1.0 * imp_dict[n['node_id']] for n in nodes_sorted}

true_recency = [n['last_accessed'] for n in nodes_sorted]
rel_vals = [n['relevance'] for n in nodes_sorted]
imp_vals = [n['importance'] for n in nodes_sorted]

sc_code_vals = [score_code[n['node_id']] for n in nodes_sorted]
sc_paper_vals = [score_paper[n['node_id']] for n in nodes_sorted]
sc_corr_vals = [score_corrected[n['node_id']] for n in nodes_sorted]

print("\nSpearman Correlation with Components (N=100 nodes):")
for name, vals in [('True Recency (t)', true_recency), ('Relevance', rel_vals), ('Importance', imp_vals)]:
    rho_code, _ = stats.spearmanr(sc_code_vals, vals)
    rho_paper, _ = stats.spearmanr(sc_paper_vals, vals)
    rho_corr, _ = stats.spearmanr(sc_corr_vals, vals)
    print(f"{name:16s} | Code gw=[0.5,3,2]: rho={rho_code:7.4f} | Paper gw=[1,1,1]: rho={rho_paper:7.4f} | Corrected: rho={rho_corr:7.4f}")

top5_code = sorted(score_code.keys(), key=lambda k: score_code[k], reverse=True)[:5]
top5_paper = sorted(score_paper.keys(), key=lambda k: score_paper[k], reverse=True)[:5]
top5_corr = sorted(score_corrected.keys(), key=lambda k: score_corrected[k], reverse=True)[:5]
print(f"\nTop-5 Mean Age (last_accessed, higher=newer):")
print(f"Code weights [0.5, 3, 2] (Inverted Recency): {np.mean([int(k.split('_')[1]) for k in top5_code]):.1f} / 100")
print(f"Paper weights [1, 1, 1] (Inverted Recency): {np.mean([int(k.split('_')[1]) for k in top5_paper]):.1f} / 100")
print(f"Corrected Recency [1, 1, 1]:                {np.mean([int(k.split('_')[1]) for k in top5_corr]):.1f} / 100")


print("\n" + "=" * 80)
print("TEST 2: TOKEN-NORMALIZED MULTI-AGENT DEBATE VS B1-SC")
print("=" * 80)

C_0, L = 500, 300
print(f"Assumptions: Prompt Context C_0 = {C_0} tokens, Output Response L = {L} tokens")
for N, R in [(3, 2), (3, 3), (4, 2), (5, 3)]:
    r_tokens = [N * (C_0 + (r - 1) * N * L + L) for r in range(1, R + 1)]
    tot_mad = sum(r_tokens)
    exec_tokens = N * R * L
    tax = (1.0 - exec_tokens / tot_mad) * 100
    k_equiv = tot_mad / (C_0 + L)
    print(f"MAD (N={N}, R={R}): Total Tokens = {tot_mad:6d} | Execution Tokens = {exec_tokens:5d} | "
          f"Coordination Tax = {tax:5.1f}% | B1-SC Equivalent Samples K = {k_equiv:4.1f}")

p0 = 0.782
def majority_acc(p, k):
    m = (k // 2) + 1
    return 1.0 - binom.cdf(m - 1, k, p)

def betabinom_acc(p, k, rho):
    if rho == 0: return majority_acc(p, k)
    alpha = p * (1.0 - rho) / rho
    beta = (1.0 - p) * (1.0 - rho) / rho
    m = (k // 2) + 1
    return 1.0 - betabinom.cdf(m - 1, k, alpha, beta)

print(f"\nBaseline Single-Agent Accuracy p0 = {p0*100:.1f}% (GSM8K GPT-3.5-Turbo)")
print("Reported Multi-Agent Debate Accuracy (N=3, R=2): 85.6% (Liang et al., 2023)")
for k in [1, 3, 5, 9, 15, 19]:
    a_ind = majority_acc(p0, k)
    a_c15 = betabinom_acc(p0, k, 0.15)
    a_c30 = betabinom_acc(p0, k, 0.30)
    print(f"K={k:2d} | Indep B1-SC: {a_ind*100:5.2f}% | Correlated (rho=0.15): {a_c15*100:5.2f}% | Correlated (rho=0.30): {a_c30*100:5.2f}%")


print("\n" + "=" * 80)
print("TEST 3: COMPLEXITY DERIVATION DISCREPANCY AUDIT (DR-13)")
print("=" * 80)

print("Auditing DR-13 Section 4.1 line 179:")
print("DR-13 claims: Tokens_debate = sum_{r=1}^R N * (r * L) = O(N * R^2)")
print("Rigorous derivation: Each agent in round r receives prompt C_0 + (r-1)*N*L previous outputs.")
print("Across N agents, input tokens in round r = N * [C_0 + (r-1)*N*L], output = N * L.")
print("Total debate tokens = N*R*(C_0 + L) + N^2 * L * R*(R-1)/2  --> O(N^2 * R^2)")

for N, R in [(3, 2), (3, 3), (5, 3), (8, 4)]:
    dr13_formula = sum([N * (r * L) for r in range(1, R + 1)])
    actual_broadcast = sum([N * (C_0 + (r - 1) * N * L + L) for r in range(1, R + 1)])
    print(f"N={N:2d}, R={R:2d} | DR-13 Formula: {dr13_formula:6d} tokens | Actual Full Broadcast: {actual_broadcast:6d} tokens | Discrepancy Ratio: {actual_broadcast/dr13_formula:.2f}x")


print("\n" + "=" * 80)
print("TEST 4: CONFOUND VARIANCE DECOMPOSITION (MODEL SCALE VS ARCHITECTURE)")
print("=" * 80)

# 2x2 Factorial ANOVA on HumanEval
# Factor A: Foundation Model (GPT-3.5 vs GPT-4)
# Factor B: Architecture (Single Agent vs Multi-Agent)
data_he = np.array([
    [48.1, 67.0], # Single Agent: [GPT-3.5, GPT-4]
    [54.3, 85.9]  # Multi-Agent:  [GPT-3.5, GPT-4]
])
mu = np.mean(data_he)
ss_total = np.sum((data_he - mu)**2)
ss_model = 2 * np.sum((np.mean(data_he, axis=0) - mu)**2)
ss_arch = 2 * np.sum((np.mean(data_he, axis=1) - mu)**2)
ss_inter = ss_total - ss_model - ss_arch

print("HumanEval Benchmark Variance Decomposition (2x2 Factorial Design):")
print(f"Total Sum of Squares: {ss_total:7.2f} (100.0%)")
print(f"  Model Factor (GPT-3.5 -> GPT-4):    {ss_model:7.2f} ({ss_model/ss_total*100:5.1f}%)")
print(f"  Architecture (Single -> MAS):       {ss_arch:7.2f} ({ss_arch/ss_total*100:5.1f}%)")
print(f"  Interaction Effect (Model x Arch):  {ss_inter:7.2f} ({ss_inter/ss_total*100:5.1f}%)")

# 2x2 Factorial ANOVA on GSM8K
data_gsm = np.array([
    [78.2, 92.0], # Single Agent CoT: [GPT-3.5, GPT-4]
    [85.6, 95.0]  # Multi-Agent Debate: [GPT-3.5, GPT-4]
])
mu_g = np.mean(data_gsm)
ss_total_g = np.sum((data_gsm - mu_g)**2)
ss_model_g = 2 * np.sum((np.mean(data_gsm, axis=0) - mu_g)**2)
ss_arch_g = 2 * np.sum((np.mean(data_gsm, axis=1) - mu_g)**2)
ss_inter_g = ss_total_g - ss_model_g - ss_arch_g

print("\nGSM8K Benchmark Variance Decomposition (2x2 Factorial Design):")
print(f"Total Sum of Squares: {ss_total_g:7.2f} (100.0%)")
print(f"  Model Factor (GPT-3.5 -> GPT-4):    {ss_model_g:7.2f} ({ss_model_g/ss_total_g*100:5.1f}%)")
print(f"  Architecture (Single -> MAS):       {ss_arch_g:7.2f} ({ss_arch_g/ss_total_g*100:5.1f}%)")
print(f"  Interaction Effect (Model x Arch):  {ss_inter_g:7.2f} ({ss_inter_g/ss_total_g*100:5.1f}%)")
