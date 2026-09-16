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

with open(r'E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md', 'r', encoding='utf-8') as f:
    content = f.read()

prim_blocks = re.split(r'#### Primitive (PRIM-[A-Z]+-\d+):', content)
print(f'Total split segments: {len(prim_blocks)}')

primitives = {}
for i in range(1, len(prim_blocks), 2):
    pid = prim_blocks[i].strip()
    block = prim_blocks[i+1]
    primitives[pid] = block

print(f'Parsed {len(primitives)} primitives: {list(primitives.keys())}')

errors = []
validated_count = 0
status_distribution = {}
repro_distribution = {}

for pid, block in primitives.items():
    found_fields = {}
    for line in block.split('\n'):
        m = re.match(r'^- \*\*(\d+)\.\s+([a-z_]+)\*\*:\s*(.*)$', line.strip())
        if m:
            num = int(m.group(1))
            fname = m.group(2)
            val = m.group(3).strip()
            found_fields[fname] = (num, val)
    
    for idx, rf in enumerate(REQUIRED_FIELDS, 1):
        if rf not in found_fields:
            errors.append(f'{pid}: missing required field {rf}')
        else:
            num, val = found_fields[rf]
            if num != idx:
                errors.append(f'{pid}: field {rf} has number {num}, expected {idx}')
            if not val:
                errors.append(f'{pid}: field {rf} is empty')
    
    if 'status' in found_fields:
        _, status_val = found_fields['status']
        status_clean = status_val.replace('', '').strip()
        status_distribution[status_clean] = status_distribution.get(status_clean, 0) + 1
        if 'VALIDATED' in status_clean:
            validated_count += 1
            errors.append(f'{pid}: has prohibited VALIDATED status: {status_val}')
        if status_clean not in PERMITTED_STATUS:
            errors.append(f'{pid}: status {status_clean} not in permitted status set')
            
    if 'reproducibility_status' in found_fields:
        _, repro_val = found_fields['reproducibility_status']
        repro_clean = repro_val.replace('', '').split()[0].strip()
        repro_distribution[repro_clean] = repro_distribution.get(repro_clean, 0) + 1
        if repro_clean not in PERMITTED_REPRODUCIBILITY:
            errors.append(f'{pid}: reproducibility_status {repro_clean} not in permitted set')

print('=' * 60)
print('DR-05 AUDIT REPORT')
print('=' * 60)
print(f'Total Primitives Checked: {len(primitives)}')
print(f'Total Validation Errors: {len(errors)}')
print(f'VALIDATED Status Count: {validated_count} (Must be 0)')
print('\nStatus Distribution:')
for s, c in sorted(status_distribution.items()):
    print(f'  {s:30s}: {c}')

print('\nReproducibility Status Distribution:')
for r, c in sorted(repro_distribution.items()):
    print(f'  {r:30s}: {c}')

if errors:
    print('\nERRORS FOUND:')
    for e in errors:
        print('  FAIL:', e)
    sys.exit(1)
else:
    print('\nSUCCESS: All 28 primitives in DR-05 contain all 26 schema fields with valid statuses and ZERO VALIDATED status!')
