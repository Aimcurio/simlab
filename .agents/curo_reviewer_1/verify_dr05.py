import re
import sys

filepath = r"E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

expected_fields = [
    "primitive_id",
    "primitive_name",
    "source_system",
    "source_version",
    "category",
    "mechanism_description",
    "claimed_purpose",
    "claimed_benefit",
    "measured_benefit",
    "evidence_type",
    "evidence_strength",
    "dependencies",
    "runtime_cost",
    "token_cost",
    "latency_effect",
    "scaling_effect",
    "known_failure_modes",
    "known_limitations",
    "negative_evidence",
    "transferability_hypothesis",
    "reproduction_required",
    "proposed_control",
    "proposed_metric",
    "reproducibility_status",
    "confidence",
    "status"
]

permitted_status = {
    "PROPOSED",
    "REPRODUCTION_CANDIDATE",
    "PROMISING_BUT_UNVERIFIED",
    "CONTEXT_DEPENDENT",
    "INSUFFICIENT_EVIDENCE",
    "REJECTED"
}

permitted_reproducibility = {
    "NOT_ASSESSED",
    "AUTHOR_REPORTED",
    "CODE_AVAILABLE",
    "PARTIALLY_REPRODUCED",
    "INDEPENDENTLY_REPRODUCED",
    "FAILED_REPRODUCTION",
    "UNRESOLVED"
}

permitted_missing_tokens = {
    "UNKNOWN",
    "NOT_REPORTED",
    "NOT_MEASURED",
    "NOT_APPLICABLE",
    "UNRESOLVED"
}

# Parse primitives
primitives = {}
current_prim = None

field_pattern = re.compile(r"^-\s+\*\*(\d+)\.\s+([a-z_]+)\*\*:\s*(.*)$")
header_pattern = re.compile(r"^####\s+Primitive\s+(PRIM-[A-Z]+-\d+):\s*(.*)$")

for line_num, line in enumerate(lines, 1):
    hm = header_pattern.match(line.strip())
    if hm:
        pid = hm.group(1)
        current_prim = pid
        primitives[pid] = {
            "header_name": hm.group(2),
            "line": line_num,
            "fields": {}
        }
        continue
    
    fm = field_pattern.match(line.strip())
    if fm and current_prim:
        fidx = int(fm.group(1))
        fname = fm.group(2)
        fval = fm.group(3).strip()
        primitives[current_prim]["fields"][fname] = {
            "index": fidx,
            "value": fval,
            "line": line_num
        }

print(f"Total parsed primitives: {len(primitives)}")

errors = []
validated_count = 0

for pid, pdata in sorted(primitives.items()):
    pfields = pdata["fields"]
    
    # Check all 26 fields exist
    for idx, ef in enumerate(expected_fields, 1):
        if ef not in pfields:
            errors.append(f"Primitive {pid} missing field #{idx}: {ef}")
        else:
            actual_idx = pfields[ef]["index"]
            if actual_idx != idx:
                errors.append(f"Primitive {pid} field {ef} has index {actual_idx}, expected {idx}")
    
    # Check status
    if "status" in pfields:
        raw_status = pfields["status"]["value"].replace("`", "").strip()
        if "VALIDATED" in raw_status:
            validated_count += 1
            errors.append(f"INTEGRITY VIOLATION: Primitive {pid} has VALIDATED status: {raw_status}")
        if raw_status not in permitted_status:
            errors.append(f"Primitive {pid} has invalid status: '{raw_status}' (permitted: {permitted_status})")
            
    # Check reproducibility_status
    if "reproducibility_status" in pfields:
        raw_repro = pfields["reproducibility_status"]["value"].replace("`", "").strip()
        if raw_repro not in permitted_reproducibility:
            errors.append(f"Primitive {pid} has invalid reproducibility_status: '{raw_repro}' (permitted: {permitted_reproducibility})")

print(f"Validation errors count: {len(errors)}")
for err in errors[:20]:
    print("  ERROR:", err)

print(f"Total VALIDATED status detected: {validated_count}")

# Check summary of statuses
status_dist = {}
repro_dist = {}
for pid, pdata in primitives.items():
    st = pdata["fields"].get("status", {}).get("value", "").replace("`", "").strip()
    status_dist[st] = status_dist.get(st, 0) + 1
    rp = pdata["fields"].get("reproducibility_status", {}).get("value", "").replace("`", "").strip()
    repro_dist[rp] = repro_dist.get(rp, 0) + 1

print("\nStatus distribution:")
for st, cnt in sorted(status_dist.items()):
    print(f"  {st}: {cnt}")

print("\nReproducibility distribution:")
for rp, cnt in sorted(repro_dist.items()):
    print(f"  {rp}: {cnt}")
