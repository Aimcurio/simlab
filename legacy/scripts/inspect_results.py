import json

with open(r"E:\projects\simlab\phase4_execution\telemetry\exp_ab_01_comp\exp_ab_01_comp_results.json", "r", encoding="utf-8") as f:
    res = json.load(f)

print("Telemetry:")
print(json.dumps(res["telemetry"], indent=2))

print("\nHypothesis Testing:")
print(json.dumps(res["hypothesis_testing"], indent=2))

print("\nA8 Reflection Metrics:")
print(json.dumps(res["condition_summaries"]["A8"].get("reflection_metrics"), indent=2))

print("\nCondition Summaries:")
for code, s in res["condition_summaries"].items():
    print(f"{code} ({s['condition_name']}): MRR={s['mrr_mean']:.4f} +/- {s['mrr_std']:.4f}, NDCG@5={s['ndcg5_mean']:.4f}, Inversion={s['temporal_inversion_rate_mean']*100:.1f}%, FalseRet={s['false_retrieval_rate']*100:.1f}%, Latency={s['latency_ms_mean']:.3f}ms")
    for qt, qts in s["stratified"].items():
        print(f"    {qt}: MRR={qts['mrr_mean']:.4f}, NDCG@5={qts['ndcg5_mean']:.4f}")

print("\nComparisons vs A7:")
for code, comp in res["comparisons_vs_a7"].items():
    print(f"{code} vs A7: Delta={comp['delta_mrr']:+.4f}, W={comp['wilcoxon_w']}, p={comp['p_value']:.4e}, d={comp['cohens_d']:+.4f}, Sig={comp['statistically_significant']}")

print("\nSimplex Best & Worst:")
print("Best:", res["simplex_sweep"]["best_point"])
print("Worst:", res["simplex_sweep"]["worst_point"])

print("\nBeta Gradient:")
for b, bg in sorted(res["simplex_sweep"]["beta_gradient"].items(), key=lambda x: float(x[0])):
    print(f"beta={float(b):.1f}: mean_mrr={bg['mean_mrr']:.4f}, max_mrr={bg['max_mrr']:.4f}, min_mrr={bg['min_mrr']:.4f}")
