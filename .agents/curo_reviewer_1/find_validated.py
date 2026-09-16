filepath = r"E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if "VALIDATED" in line:
        print(f"Line {i}: {line.strip()}")
