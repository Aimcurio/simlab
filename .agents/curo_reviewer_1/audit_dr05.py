import re
import sys

filepath = r"E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

required_fields = [
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
    "status",
]

# Let's see how primitives are formatted in DR-05
sections = re.split(r"\n##\s+(?:3\.\d+\s+)?(?:Primitive\s+)?(PRIM-[A-Z]+-\d+)", text)
print(f"Total splits: {len(sections)}")

# Let's inspect sections
if len(sections) <= 1:
    # Maybe split by ### or something else
    sections_alt = re.findall(r"(PRIM-[A-Z]+-\d+)", text)
    print(f"Total regex findall PRIM-*: {len(set(sections_alt))}")
    print(f"Primitive IDs found: {sorted(list(set(sections_alt)))}")
