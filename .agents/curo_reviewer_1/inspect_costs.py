import verify_dr05

prims = verify_dr05.primitives

for pid, pdata in sorted(prims.items()):
    f = pdata["fields"]
    print(f"=== {pid} ({f['primitive_name']['value']}) ===")
    print(f"  measured_benefit: {f['measured_benefit']['value'][:100]}...")
    print(f"  token_cost: {f['token_cost']['value'][:100]}...")
    print(f"  runtime_cost: {f['runtime_cost']['value'][:100]}...")
    print(f"  latency_effect: {f['latency_effect']['value'][:100]}...")
    print(f"  scaling_effect: {f['scaling_effect']['value'][:100]}...")
