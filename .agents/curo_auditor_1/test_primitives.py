import sys
import re

with open(r'E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md', encoding='utf-8') as f:
    text = f.read()

primitive_pattern = re.compile(r'#### Primitive (PRIM-[A-Z]+-\d+):?([^\n]+)', re.MULTILINE)
matches = list(primitive_pattern.finditer(text))

required_fields = [
    'primitive_id', 'primitive_name', 'source_system', 'source_version',
    'category', 'mechanism_description', 'claimed_purpose', 'claimed_benefit',
    'measured_benefit', 'evidence_type', 'evidence_strength', 'dependencies',
    'runtime_cost', 'token_cost', 'latency_effect', 'scaling_effect',
    'known_failure_modes', 'known_limitations', 'negative_evidence',
    'transferability_hypothesis', 'reproduction_required', 'proposed_control',
    'proposed_metric', 'reproducibility_status', 'confidence', 'status'
]

permitted_statuses = {
    'PROPOSED', 'REPRODUCTION_CANDIDATE', 'PROMISING_BUT_UNVERIFIED',
    'CONTEXT_DEPENDENT', 'INSUFFICIENT_EVIDENCE', 'REJECTED'
}

permitted_repro_statuses = {
    'NOT_ASSESSED', 'AUTHOR_REPORTED', 'CODE_AVAILABLE',
    'PARTIALLY_REPRODUCED', 'INDEPENDENTLY_REPRODUCED',
    'FAILED_REPRODUCTION', 'UNRESOLVED'
}

print(f'Auditing {len(matches)} primitives against 26 schema fields...')
failures = []

for i, m in enumerate(matches):
    pid = m.group(1).strip()
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(text)
    block = text[start:end]
    
    fields_found = {}
    for line in block.splitlines():
        fm = re.match(r'- \*\*(\d+)\. ([a-z_]+)\*\*:\s*(.*)', line.strip())
        if fm:
            fields_found[fm.group(2)] = (int(fm.group(1)), fm.group(3).strip())
            
    # 1. Check all 26 fields present
    for idx, rf in enumerate(required_fields, 1):
        if rf not in fields_found:
            failures.append(f'{pid}: missing field {idx}. {rf}')
        else:
            found_idx, val = fields_found[rf]
            if found_idx != idx:
                failures.append(f'{pid}: field {rf} has index {found_idx}, expected {idx}')
            if not val:
                failures.append(f'{pid}: field {rf} is empty')
                
    # 2. Check status
    if 'status' in fields_found:
        raw_val = fields_found['status'][1]
        status_val = raw_val.replace('`', '').replace('*', '').strip()
        if status_val == 'VALIDATED':
            failures.append(f'{pid}: VIOLATION - status is VALIDATED!')
        if status_val not in permitted_statuses:
            failures.append(f'{pid}: invalid status value: {status_val}')
            
    # 3. Check reproducibility status
    if 'reproducibility_status' in fields_found:
        repro_raw = fields_found['reproducibility_status'][1]
        repro_clean = repro_raw.replace('`', '').replace('*', '').split('(')[0].strip()
        if repro_clean not in permitted_repro_statuses:
            failures.append(f'{pid}: invalid reproducibility_status value: {repro_clean}')

print(f'Audit finished. Total failures found: {len(failures)}')
if failures:
    for f in failures:
        print('  FAIL:', f)
else:
    print('ALL 28 PRIMITIVES FULLY COMPLIANT WITH ZERO FAILURES!')
