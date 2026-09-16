import re

filepath = r"E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Let's check occurrences of explicit missing tokens
missing_tokens = ["UNKNOWN", "NOT_REPORTED", "NOT_MEASURED", "NOT_APPLICABLE", "UNRESOLVED"]
for token in missing_tokens:
    matches = re.findall(rf"\b{token}\b", text)
    print(f"Token {token}: {len(matches)} occurrences")

# Let's check how many fields use these tokens
import verify_dr05

prims = verify_dr05.primitives
print(f"\nChecking fields across {len(prims)} primitives:")
fields_with_missing = {}
for pid, pdata in sorted(prims.items()):
    for fname, finfo in pdata["fields"].items():
        val = finfo["value"]
        for token in missing_tokens:
            if token in val:
                fields_with_missing[fname] = fields_with_missing.get(fname, 0) + 1
                break

for fname, cnt in sorted(fields_with_missing.items(), key=lambda x: -x[1]):
    print(f"  Field '{fname}' contains explicit missing token in {cnt} primitives")
