import numpy as np
import scipy.stats as stats
import math

print("=" * 80)
print("EMPIRICAL ADVERSARIAL VERIFICATION HARNESS: RP-01 & RP-02")
print("=" * 80)

# ----------------------------------------------------------------------
# 1. RP-01: TIMESCALE SENSITIVITY OF EXPONENTIAL DECAY (lambda = 0.995)
# ----------------------------------------------------------------------
print("\n--- 1.1 TIMESCALE SENSITIVITY OF LAMBDA = 0.995 ---")

decay_rate = 0.995
half_life_units = math.log(0.5) / math.log(decay_rate)
print(f"Base decay rate: {decay_rate}")
print(f"Theoretical Half-life in raw units: {half_life_units:.2f} units")

timescales = {
    "Hours (Paper description)": 1.0, # 1 hour = 1 unit
    "10-second ticks (Smallville engine)": 360.0, # 1 hour = 360 ticks
    "Minutes": 60.0, # 1 hour = 60 units
    "Days": 1.0 / 24.0, # 1 hour = 1/24 units
}

print(f"{'Timescale Unit':<35} | {'Half-life (hours)':<18} | {'Decay @ 1h':<12} | {'Decay @ 24h':<12} | {'Decay @ 72h':<12}")
print("-" * 95)

for name, units_per_hour in timescales.items():
    t_half_hours = half_life_units / units_per_hour
    d_1h = decay_rate ** (1.0 * units_per_hour)
    d_24h = decay_rate ** (24.0 * units_per_hour)
    d_72h = decay_rate ** (72.0 * units_per_hour) if (72.0 * units_per_hour) < 1000 else 0.0
    print(f"{name:<35} | {t_half_hours:<18.2f} | {d_1h:<12.4e} | {d_24h:<12.4e} | {d_72h:<12.4e}")

# Min-max normalization under narrow vs wide candidate age spread
print("\nMin-Max Normalization Behavior across Candidate Sets:")
def min_max_norm(vals):
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return [1.0] * len(vals) # Or 0.0 / NaN
    return [(v - mn) / (mx - mn) for v in vals]

# Scenario A: Wide spread (memories from 0h to 72h ago)
ages_wide = np.array([0.0, 1.0, 12.0, 24.0, 48.0, 72.0])
raw_wide = decay_rate ** ages_wide
norm_wide = min_max_norm(raw_wide)

# Scenario B: Narrow spread (all candidates clustered between 20h and 22h ago)
ages_narrow = np.array([20.0, 20.2, 20.5, 21.0, 21.5, 22.0])
raw_narrow = decay_rate ** ages_narrow
norm_narrow = min_max_norm(raw_narrow)

print("Wide Age Spread (0h to 72h):")
for a, r, n in zip(ages_wide, raw_wide, norm_wide):
    print(f"  Age: {a:4.1f}h -> Raw: {r:.4f} -> Norm: {n:.4f}")

print("Narrow Age Spread (20h to 22h, difference = 2h):")
for a, r, n in zip(ages_narrow, raw_narrow, norm_narrow):
    print(f"  Age: {a:4.1f}h -> Raw: {r:.4f} -> Norm: {n:.4f}")

print(f"Observation: In narrow spread, raw difference of only {raw_narrow[0]-raw_narrow[-1]:.4f} is magnified to full [0.0, 1.0] range!")


# ----------------------------------------------------------------------
# 2. RP-01: SIMULATION OF MEMORY RETRIEVAL & QUERY SELECTION BIAS
# ----------------------------------------------------------------------
print("\n--- 1.2 QUERY SELECTION BIAS & EMBEDDING VARIANCE SIMULATION ---")

np.random.seed(42)
N_MEMORIES = 500
TIMELINE_HOURS = 72.0

# Generate 500 synthetic memory records
memories = []
for i in range(N_MEMORIES):
    t_created = np.random.uniform(0, TIMELINE_HOURS)
    importance = np.random.randint(1, 11) # 1 to 10
    # Embedding vector in d=64
    emb = np.random.randn(64)
    emb /= np.linalg.norm(emb)
    memories.append({
        'id': i,
        'created_at': t_created, # hours ago from current time
        'importance': importance,
        'embedding': emb
    })

# Define 3 query types (100 total queries: 40 recency, 40 relevance, 20 conflict)
# For each query, define target memory and evaluate MRR and NDCG@5 under:
# Condition 1: Historical Inverted (Smallville code)
# Condition 2: No Recency (Relevance + Importance only)
# Condition 3: Equal Weights Corrected (alpha=1, beta=1, gamma=1)
# Condition 4: Smallville Code Weights Corrected (alpha=0.5, beta=3.0, gamma=2.0)

def evaluate_retrieval(query_type, target_idx, q_emb, t_current=72.0):
    # Candidate pool: say top 30 by cosine similarity or random 30
    # Compute components for all candidates
    cand_indices = list(range(len(memories)))
    
    # 1. Cosine similarity
    rel_scores = {}
    for idx in cand_indices:
        cos_sim = np.dot(memories[idx]['embedding'], q_emb)
        rel_scores[idx] = float(cos_sim)
    
    # 2. Importance
    imp_scores = {idx: memories[idx]['importance'] for idx in cand_indices}
    
    # 3. Recency:
    # A. Historical Inverted: sorted by creation time oldest first
    sorted_by_time = sorted(cand_indices, key=lambda idx: memories[idx]['created_at'], reverse=True) # oldest first
    hist_rec = {idx: 0.99 ** (rank + 1) for rank, idx in enumerate(sorted_by_time)}
    
    # B. Corrected Exponential Decay (hours)
    corr_rec = {idx: 0.995 ** (t_current - memories[idx]['created_at']) for idx in cand_indices}
    
    # Normalize components across candidates
    norm_rel = min_max_norm(list(rel_scores.values()))
    norm_rel = dict(zip(rel_scores.keys(), norm_rel))
    
    norm_imp = min_max_norm(list(imp_scores.values()))
    norm_imp = dict(zip(imp_scores.keys(), norm_imp))
    
    norm_hist_rec = min_max_norm(list(hist_rec.values()))
    norm_hist_rec = dict(zip(hist_rec.keys(), norm_hist_rec))
    
    norm_corr_rec = min_max_norm(list(corr_rec.values()))
    norm_corr_rec = dict(zip(corr_rec.keys(), norm_corr_rec))
    
    # Scoring configurations:
    scores = {
        'Historical': {idx: norm_hist_rec[idx] + norm_rel[idx] + norm_imp[idx] for idx in cand_indices},
        'NoRecency': {idx: 0.0 * norm_corr_rec[idx] + 1.0 * norm_rel[idx] + 1.0 * norm_imp[idx] for idx in cand_indices},
        'EqualWeights': {idx: 1.0 * norm_corr_rec[idx] + 1.0 * norm_rel[idx] + 1.0 * norm_imp[idx] for idx in cand_indices},
        'CodeWeights': {idx: 0.5 * norm_corr_rec[idx] + 3.0 * norm_rel[idx] + 2.0 * norm_imp[idx] for idx in cand_indices},
    }
    
    # Compute rank of target_idx for each condition
    ranks = {}
    for cond, sc in scores.items():
        sorted_cands = sorted(sc.keys(), key=lambda k: sc[k], reverse=True)
        rank = sorted_cands.index(target_idx) + 1
        ranks[cond] = rank
    return ranks

# Run 100 queries
results = {'recency': [], 'relevance': [], 'conflict': []}

# 40 Recency-sensitive: target is newest memory among top relevance
for q in range(40):
    # Pick a memory created recently (< 12 hours ago)
    recent_mems = [i for i, m in enumerate(memories) if (72.0 - m['created_at']) < 12.0]
    target = np.random.choice(recent_mems)
    # Query embedding is close to target
    q_emb = memories[target]['embedding'] + 0.3 * np.random.randn(64)
    q_emb /= np.linalg.norm(q_emb)
    ranks = evaluate_retrieval('recency', target, q_emb)
    results['recency'].append(ranks)

# 40 Relevance-dominant: target is an older memory (> 36 hours ago) with highest semantic match
for q in range(40):
    older_mems = [i for i, m in enumerate(memories) if (72.0 - m['created_at']) > 36.0]
    target = np.random.choice(older_mems)
    q_emb = memories[target]['embedding'] + 0.1 * np.random.randn(64) # very high relevance
    q_emb /= np.linalg.norm(q_emb)
    ranks = evaluate_retrieval('relevance', target, q_emb)
    results['relevance'].append(ranks)

# 20 Conflict: target is an older memory, but there are newer superficially similar memories
for q in range(20):
    older_mems = [i for i, m in enumerate(memories) if (72.0 - m['created_at']) > 48.0]
    target = np.random.choice(older_mems)
    q_emb = memories[target]['embedding'] + 0.2 * np.random.randn(64)
    q_emb /= np.linalg.norm(q_emb)
    ranks = evaluate_retrieval('conflict', target, q_emb)
    results['conflict'].append(ranks)

print("\nMean Reciprocal Rank (MRR) by Query Category:")
print(f"{'Category':<20} | {'Historical':<12} | {'NoRecency':<12} | {'EqualWeights':<12} | {'CodeWeights':<12}")
print("-" * 75)

for cat in ['recency', 'relevance', 'conflict']:
    mrr_hist = np.mean([1.0 / r['Historical'] for r in results[cat]])
    mrr_norec = np.mean([1.0 / r['NoRecency'] for r in results[cat]])
    mrr_eq = np.mean([1.0 / r['EqualWeights'] for r in results[cat]])
    mrr_cw = np.mean([1.0 / r['CodeWeights'] for r in results[cat]])
    print(f"{cat:<20} | {mrr_hist:<12.4f} | {mrr_norec:<12.4f} | {mrr_eq:<12.4f} | {mrr_cw:<12.4f}")

all_queries = results['recency'] + results['relevance'] + results['conflict']
mrr_all_hist = np.mean([1.0 / r['Historical'] for r in all_queries])
mrr_all_norec = np.mean([1.0 / r['NoRecency'] for r in all_queries])
mrr_all_eq = np.mean([1.0 / r['EqualWeights'] for r in all_queries])
mrr_all_cw = np.mean([1.0 / r['CodeWeights'] for r in all_queries])
print("-" * 75)
print(f"{'OVERALL (100 Qs)':<20} | {mrr_all_hist:<12.4f} | {mrr_all_norec:<12.4f} | {mrr_all_eq:<12.4f} | {mrr_all_cw:<12.4f}")

# Paired test vs Independent test power
print("\nPaired vs Unpaired Test on Overall MRR (EqualWeights vs NoRecency):")
mrr_pairs_eq = [1.0 / r['EqualWeights'] for r in all_queries]
mrr_pairs_norec = [1.0 / r['NoRecency'] for r in all_queries]
wilc = stats.wilcoxon(mrr_pairs_eq, mrr_pairs_norec)
mwu = stats.mannwhitneyu(mrr_pairs_eq, mrr_pairs_norec)
print(f"Paired Wilcoxon signed-rank p-value: {wilc.pvalue:.6e}")
print(f"Mann-Whitney U (unpaired) p-value:   {mwu.pvalue:.6e}")


# ----------------------------------------------------------------------
# 3. RP-02: TOKEN PARITY & EXPANSION RATIO MATHEMATICS
# ----------------------------------------------------------------------
print("\n" + "=" * 80)
print("TEST 2: RP-02 TOKEN PARITY & COMPUTE EQUIVALENCE STRESS-TEST")
print("=" * 80)

# 3 agents, 2 rounds:
# Round 1: 3 * (C0 + L)
# Round 2: 3 * (C0 + 3L + L) = 3 * (C0 + 4L) = 3 C0 + 12 L
# Total Debate Tokens = 6 C0 + 15 L
# B1-SC with K=6:
# Total B1-SC Tokens = 6 * (C0 + L) = 6 C0 + 6 L

print("\nToken Expansion Analysis for 3-Agent 2-Round Debate vs B1-SC (K=6):")
print(f"{'Prompt C0':<10} | {'Output L':<10} | {'B1-SC (K=6)':<12} | {'Debate Tokens':<14} | {'Token Ratio':<12} | {'Debate Excess %':<16} | {'K equiv for B1-SC':<18}")
print("-" * 105)

test_configs = [
    (200, 150),
    (300, 200),
    (500, 300),
    (1000, 400),
    (1500, 500),
    (2000, 600)
]

for c0, l in test_configs:
    tok_b1sc = 6 * (c0 + l)
    tok_debate = 6 * c0 + 15 * l
    ratio = tok_debate / tok_b1sc
    excess_pct = (ratio - 1.0) * 100
    k_equiv = tok_debate / (c0 + l)
    print(f"{c0:<10} | {l:<10} | {tok_b1sc:<12} | {tok_debate:<14} | {ratio:<12.3f} | +{excess_pct:<15.1f}% | {k_equiv:<18.2f}")

# Can Debate ever be within +/- 10% of B1-SC with K=6?
# 6 C0 + 15 L <= 1.10 * (6 C0 + 6 L) = 6.6 C0 + 6.6 L
# 8.4 L <= 0.6 C0 ==> L <= 0.6 / 8.4 C0 = C0 / 14 = 0.0714 * C0
print("\nConstraint Check: For Debate to be within +10% of B1-SC (K=6):")
print(f"Requires Output Length L <= C0 / 14 = 0.0714 * C0")
print("For C0 = 500, max permitted output L is ONLY 35.7 tokens!")
print("PROVEN: +/- 10% token parity is MATHEMATICALLY IMPOSSIBLE under realistic output lengths for K=6!")


# ----------------------------------------------------------------------
# 4. RP-02: EVEN K=6 TIE PROBABILITY & MAJORITY VOTING BIAS
# ----------------------------------------------------------------------
print("\n--- 2.2 EVEN K=6 TIE PROBABILITY & MAJORITY VOTING ---")

p_vals = [0.50, 0.60, 0.70, 0.80, 0.90]
print(f"{'Base Acc p0':<12} | {'P(Exact 3-3 Tie in K=6)':<25} | {'Odd K=5 Acc':<14} | {'Even K=6 Acc (coin tie)':<24} | {'Odd K=7 Acc':<14}")
print("-" * 95)

for p in p_vals:
    # Exact tie in K=6: binom.pmf(3, 6, p)
    p_tie = stats.binom.pmf(3, 6, p)
    # Odd K=5: sum_{k=3}^5 binom.pmf(k, 5, p)
    acc_k5 = 1.0 - stats.binom.cdf(2, 5, p)
    # Even K=6 with coin flip on tie: P(>3) + 0.5 * P(==3)
    p_strict_win = 1.0 - stats.binom.cdf(3, 6, p)
    acc_k6 = p_strict_win + 0.5 * p_tie
    # Odd K=7: sum_{k=4}^7 binom.pmf(k, 7, p)
    acc_k7 = 1.0 - stats.binom.cdf(3, 7, p)
    print(f"{p:<12.2f} | {p_tie*100:<24.2f}% | {acc_k5*100:<13.2f}% | {acc_k6*100:<23.2f}% | {acc_k7*100:<13.2f}%")


# ----------------------------------------------------------------------
# 5. RP-02: TOST EQUIVALENCE MARGIN ([-0.03, +0.03]) STATISTICAL POWER
# ----------------------------------------------------------------------
print("\n--- 2.3 TOST EQUIVALENCE MARGIN ([-0.03, +0.03]) POWER ON GSM8K (N=100) ---")

# In TOST with margin delta = 0.03 on paired binary data (N=100)
# Let d_i = y_{1,i} - y_{2,i} in {-1, 0, 1}.
# Discordance rate p_disc = P(y1 != y2).
# Variance of difference = p_disc - (p1 - p2)^2. Under H0 (true delta = 0), Var = p_disc.
# Standard error SE = sqrt(p_disc / N).
# 90% Confidence Interval half-width = z_{0.95} * SE = 1.6449 * sqrt(p_disc / N).
# To reject TOST at alpha=0.05, 90% CI must lie entirely inside [-0.03, +0.03].
# This requires z_{0.95} * sqrt(p_disc / N) < 0.03!

print(f"{'Discordance p_disc':<20} | {'SE (N=100)':<12} | {'90% CI Half-Width (N=100)':<28} | {'Fits in [-0.03, +0.03]?':<24} | {'Min N required':<15}")
print("-" * 105)

for p_disc in [0.05, 0.10, 0.15, 0.20, 0.25]:
    se = math.sqrt(p_disc / 100.0)
    hw = 1.644853 * se
    fits = "YES" if hw < 0.03 else "NO (POWER = 0.0%)"
    # Min N: 1.644853 * sqrt(p_disc / N) < 0.03 ==> N > (1.644853 / 0.03)^2 * p_disc
    min_n = math.ceil(((1.644853 / 0.03) ** 2) * p_disc)
    print(f"{p_disc:<20.2f} | {se:<12.4f} | {hw*100:<27.2f}% | {fits:<24} | {min_n:<15d}")

# Simulate TOST power across 10,000 synthetic experiments with N=100
N_SIMS = 10000
for p_disc in [0.10, 0.15, 0.20]:
    # Simulate paired differences under true delta = 0
    # Outcomes: +1 with p_disc/2, -1 with p_disc/2, 0 with 1 - p_disc
    diffs = np.random.choice([1, -1, 0], size=(N_SIMS, 100), p=[p_disc/2, p_disc/2, 1-p_disc])
    mean_diffs = np.mean(diffs, axis=1)
    se_diffs = np.std(diffs, axis=1, ddof=1) / math.sqrt(100)
    ci_lower = mean_diffs - 1.644853 * se_diffs
    ci_upper = mean_diffs + 1.644853 * se_diffs
    power = np.mean((ci_lower > -0.03) & (ci_upper < 0.03))
    print(f"Empirical TOST Power (N=100, delta=0.03, p_disc={p_disc:.2f}): {power*100:.2f}%")


# ----------------------------------------------------------------------
# 6. OBJECTIVE 3: PRE-REGISTERED THRESHOLD AMBIGUITY AUDIT
# ----------------------------------------------------------------------
print("\n" + "=" * 80)
print("TEST 3: PRE-REGISTERED THRESHOLD AMBIGUITY AUDIT")
print("=" * 80)

print("RP-01 Threshold Analysis:")
print("  Success: Delta MRR >= +0.15 AND p < 0.0025")
print("  Failure: Delta MRR < +0.05 AND p >= 0.05")
print("  Ambiguous Zones:")
print("    Zone 1: +0.05 <= Delta MRR < +0.15 (regardless of p-value)")
print("    Zone 2: Delta MRR >= +0.15 BUT 0.0025 <= p < 0.05")
print("    Zone 3: Delta MRR < +0.05 BUT p < 0.05 (statistically significant small effect)")

print("\nRP-02 Threshold Analysis:")
print("  Success: T-Debate accuracy exceeds B1-SC by >= +10% on Private Info AND Asymmetric Tools (p < 0.01)")
print("           AND T-Debate provides <= 2% advantage on GSM8K")
print("  Failure: B1-SC achieves equal or higher accuracy across ALL 4 task categories (p >= 0.05)")
print("  Ambiguous Zones:")
print("    Zone 1: T-Debate advantage is +5% to +9% on Private Info (sub-threshold positive gain)")
print("    Zone 2: T-Debate wins on 2 categories, B1-SC wins on 2 categories (neither condition met)")
print("    Zone 3: T-Debate advantage on GSM8K is +4% (violates success, but prevents B1-SC failure threshold)")
