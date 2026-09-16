import re

filepath = r"E:\projects\simlab\deliverables\DR-07_failure_register.md"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Find all FM-xx
fm_headers = re.findall(r"####\s+(FM-\d+):\s*(.*)", text)
print(f"Total Failure Modes found: {len(fm_headers)}")
for fmid, title in fm_headers:
    print(f"  {fmid}: {title}")

# Check required fields for each FM
# Description, severity, likelihood, detectability, mitigation, deterministic vs probabilistic
fms = re.split(r"\n####\s+(FM-\d+):\s*", text)
# fms[0] is preface, then alternating fmid, body
fm_dict = {}
for i in range(1, len(fms), 2):
    fmid = fms[i]
    body = fms[i+1]
    fm_dict[fmid] = body

print(f"\nParsed {len(fm_dict)} failure modes.")

deterministic_count = 0
for fmid, body in sorted(fm_dict.items()):
    has_sev = bool(re.search(r"Severity", body, re.IGNORECASE))
    has_lik = bool(re.search(r"Likelihood", body, re.IGNORECASE))
    has_det = bool(re.search(r"Detectability", body, re.IGNORECASE))
    has_mit = bool(re.search(r"Mitigation", body, re.IGNORECASE))
    has_det_prev = bool(re.search(r"Deterministic", body, re.IGNORECASE))
    if has_det_prev:
        deterministic_count += 1
    missing = []
    if not has_sev: missing.append("Severity")
    if not has_lik: missing.append("Likelihood")
    if not has_det: missing.append("Detectability")
    if not has_mit: missing.append("Mitigation")
    if missing:
        print(f"  {fmid} missing: {missing}")

print(f"\nTotal failure modes with deterministic prevention/mitigation elements: {deterministic_count}/15")
