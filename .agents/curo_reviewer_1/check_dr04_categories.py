import re

filepath = r"E:\projects\simlab\deliverables\DR-04_paper_code_mapping.md"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

categories = [
    "DOCUMENTED_AND_IMPLEMENTED",
    "DOCUMENTED_PARTIALLY_IMPLEMENTED",
    "IMPLEMENTED_DIFFERENTLY",
    "DOCUMENTED_NOT_FOUND",
    "CODE_ONLY",
    "VERSION_DEPENDENT",
    "UNRESOLVED"
]

for cat in categories:
    count = len(re.findall(rf"\b{cat}\b", text))
    print(f"{cat}: {count} occurrences")
