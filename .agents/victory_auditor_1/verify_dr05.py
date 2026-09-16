import re
import sys

REQUIRED_FIELDS = [
    'primitive_id', 'primitive_name', 'source_system', 'source_version', 'category',
    'mechanism_description', 'claimed_purpose', 'claimed_benefit', 'measured_benefit',
    'evidence_type', 'evidence_strength', 'dependencies', 'runtime_cost', 'token_cost',
    'latency_effect', 'scaling_effect', 'known_failure_modes', 'known_limitations',
    'negative_evidence', 'transferability_hypothesis', 'reproduction_required',
    'proposed_control', 'proposed_metric', 'reproducibility_status', 'confidence', 'status'
]

PERMITTED_STATUS = {
    'PROPOSED', 'REPRODUCTION_CANDIDATE', 'PROMISING_BUT_UNVERIFIED',
    'CONTEXT_DEPENDENT', 'INSUFFICIENT_EVIDENCE', 'REJECTED'
}

PERMITTED_REPRODUCIBILITY = {
    'NOT_ASSESSED', 'AUTHOR_REPORTED', 'CODE_AVAILABLE',
    'PARTIALLY_REPRODUCED', 'INDEPENDENTLY_REPRODUCED',
    'FAILED_REPRODUCTION', 'UNRESOLVED'
}

EXPLICIT_STATES = {'NOT_REPORTED', 'NOT_MEASURED', 'UNKNOWN', 'NOT_APPLICABLE', 'UNRESOLVED'}

with open(r'E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md', 'r', encoding='utf-8') as f:
    content = f.read()

prim_blocks = re.split(r'#### Primitive (PRIM-[A-Z]+-\d+):', content)

primitives = {}
for i in range(1, len(prim_blocks), 2):
    pid = prim_blocks[i].strip()
    block = prim_blocks[i+1]
    primitives[pid] = block

errors = []
validated_count = 0
status_dist = {}
repro_dist = {}
explicit_state_count = 0

for pid, block in primitives.items():
    found_fields = {}
    for line in block.split('\n'):
        m = re.match(r'^- \*\*(\d+)\.\s+([a-z_]+)\*\*:\s*(.*)$', line.strip())
        if m:
            num = int(m.group(1))
            fname = m.group(2)
            val = m.group(3).strip()
            found_fields[fname] = (num, val)
    
    # Check 26 fields
    for idx, rf in enumerate(REQUIRED_FIELDS, 1):
        if rf not in found_fields:
            errors.append(f'{pid}: missing required field {rf}')
        else:
            num, val = found_fields[rf]
            if num != idx:
                errors.append(f'{pid}: field {rf} has number {num}, expected {idx}')
            if not val:
                errors.append(f'{pid}: field {rf} is empty')
                
            # Check explicit states usage in metrics/costs
            for es in EXPLICIT_STATES:
                if es in val:
                    explicit_state_count += 1
                    break
    
    # Status check
    if 'status' in found_fields:
        _, sval = found_fields['status']
        sclean = re.sub(r'[`*]', '', sval).strip()
        status_dist[sclean] = status_dist.get(sclean, 0) + 1
        if 'VALIDATED' in sclean:
            validated_count += 1
            errors.append(f'{pid}: PROHIBITED VALIDATED status found!')
        if sclean not in PERMITTED_STATUS:
            errors.append(f'{pid}: status {sclean} not in permitted set')
            
    # Reproducibility status check
    if 'reproducibility_status' in found_fields:
        _, rval = found_fields['reproducibility_status']
        rclean = re.sub(r'[`*]', '', rval).split()[0].strip()
        repro_dist[rclean] = repro_dist.get(rclean, 0) + 1
        if rclean not in PERMITTED_REPRODUCIBILITY:
            errors.append(f'{pid}: repro status {rclean} not in permitted set')

print('=' * 70)
print('INDEPENDENT DR-05 VERIFICATION')
print('=' * 70)
print(f'Total Primitives Analyzed: {len(primitives)}')
print(f'Total Errors / Violations: {len(errors)}')
print(f'VALIDATED Status Count:    {validated_count} (Must be 0)')
print(f'Explicit Placeholders:     {explicit_state_count} occurrences detected')
print('\nStatus Breakdown:')
for s, c in sorted(status_dist.items()):
    print(f'  {s:30s}: {c:2d}')
print('\nReproducibility Status Breakdown:')
for r, c in sorted(repro_dist.items()):
    print(f'  {r:30s}: {c:2d}')

if errors:
    print('\nVIOLATIONS FOUND:')
    for e in errors:
        print(' ', e)
    sys.exit(1)
else:
    print('\nVERDICT: DR-05 FULLY PASSES ALL SCHEMA & ANTI-FABRICATION CHECKS!')
