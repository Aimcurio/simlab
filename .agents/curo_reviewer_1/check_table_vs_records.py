import re

filepath = r"E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Let's extract Section 2 table rows
table_rows = re.findall(r"\|\s*\*\*(PRIM-[A-Z]+-\d+)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|", text)
print(f"Table rows in Section 2: {len(table_rows)}")

table_status = {}
table_repro = {}
for row in table_rows:
    pid = row[0].strip()
    repro = row[6].replace("`", "").strip()
    status = row[7].replace("`", "").strip()
    table_repro[pid] = repro
    table_status[pid] = status

import verify_dr05
prims = verify_dr05.primitives

mismatches = []
for pid, pdata in sorted(prims.items()):
    rec_status = pdata["fields"]["status"]["value"].replace("`", "").strip()
    rec_repro = pdata["fields"]["reproducibility_status"]["value"].replace("`", "").strip()
    
    t_status = table_status.get(pid, "MISSING_IN_TABLE")
    t_repro = table_repro.get(pid, "MISSING_IN_TABLE")
    
    if rec_status != t_status:
        mismatches.append(f"{pid} STATUS mismatch: Section 2 Table='{t_status}' vs Section 3 Record='{rec_status}'")
    if rec_repro != t_repro:
        mismatches.append(f"{pid} REPRO mismatch: Section 2 Table='{t_repro}' vs Section 3 Record='{rec_repro}'")

print(f"\nMismatches between Section 2 Table and Section 3 Records: {len(mismatches)}")
for m in mismatches:
    print("  ", m)
