import json
import numpy as np

with open(r"E:\projects\simlab\.agents\audit_explorer_2\condition_distributions.json", "r") as f:
    cd = json.load(f)

print("Condition Quantiles Table (All Scores across 100 queries x pool size):")
print(f"{'Condition':<6} | {'Min':<8} | {'Q25':<8} | {'Q50':<8} | {'Mean':<8} | {'Q75':<8} | {'Q95':<8} | {'Max':<8} | {'Var':<8} | {'Std':<8}")
print("-" * 90)
for code, s in cd.items():
    st = s["all_score_stats"]
    print(f"{code:<6} | {st['min']:<8.4f} | {st['q25']:<8.4f} | {st['q50']:<8.4f} | {st['mean']:<8.4f} | {st['q75']:<8.4f} | {st['q95']:<8.4f} | {st['max']:<8.4f} | {st['var']:<8.4f} | {st['std']:<8.4f}")

print("\nTarget Score Quantiles Table:")
print(f"{'Condition':<6} | {'Min':<8} | {'Q25':<8} | {'Q50':<8} | {'Mean':<8} | {'Q75':<8} | {'Q95':<8} | {'Max':<8} | {'Var':<8} | {'Std':<8}")
print("-" * 90)
for code, s in cd.items():
    st = s["target_score_stats"]
    print(f"{code:<6} | {st['min']:<8.4f} | {st['q25']:<8.4f} | {st['q50']:<8.4f} | {st['mean']:<8.4f} | {st['q75']:<8.4f} | {st['q95']:<8.4f} | {st['max']:<8.4f} | {st['var']:<8.4f} | {st['std']:<8.4f}")

print("\nDistractor Score Quantiles Table:")
print(f"{'Condition':<6} | {'Min':<8} | {'Q25':<8} | {'Q50':<8} | {'Mean':<8} | {'Q75':<8} | {'Q95':<8} | {'Max':<8} | {'Var':<8} | {'Std':<8}")
print("-" * 90)
for code, s in cd.items():
    st = s["distractor_score_stats"]
    print(f"{code:<6} | {st['min']:<8.4f} | {st['q25']:<8.4f} | {st['q50']:<8.4f} | {st['mean']:<8.4f} | {st['q75']:<8.4f} | {st['q95']:<8.4f} | {st['max']:<8.4f} | {st['var']:<8.4f} | {st['std']:<8.4f}")

print("\nTarget Ranks Quantiles Table:")
print(f"{'Condition':<6} | {'Min':<6} | {'Q25':<6} | {'Median':<6} | {'Mean':<6} | {'Q75':<6} | {'Q95':<6} | {'Max':<6} | {'MRR':<6}")
print("-" * 75)
for code, s in cd.items():
    st = s["target_rank_stats"]
    print(f"{code:<6} | {st['min']:<6.1f} | {st['q25']:<6.1f} | {st['q50']:<6.1f} | {st['mean']:<6.1f} | {st['q75']:<6.1f} | {st['q95']:<6.1f} | {st['max']:<6.1f} | {s['mean_mrr']:<6.4f}")

print("\nScore Margins (Target - Top Distractor):")
print(f"{'Condition':<6} | {'Min':<8} | {'Q25':<8} | {'Median':<8} | {'Mean':<8} | {'Q75':<8} | {'Max':<8} | {'Std':<8}")
print("-" * 75)
for code, s in cd.items():
    st = s["score_margin_stats"]
    print(f"{code:<6} | {st['min']:<8.4f} | {st['q25']:<8.4f} | {st['q50']:<8.4f} | {st['mean']:<8.4f} | {st['q75']:<8.4f} | {st['max']:<8.4f} | {st['std']:<8.4f}")
