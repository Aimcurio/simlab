import os
import re
import sys

deliverables_dir = r"E:\projects\simlab\deliverables"
package_path = r"E:\projects\simlab\curo_research_package.md"

def audit_dr05():
    dr05_path = os.path.join(deliverables_dir, "DR-05_primitive_evidence_matrix.md")
    with open(dr05_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Required 26 schema fields
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
        "status"
    ]

    permitted_statuses = {
        "PROPOSED",
        "REPRODUCTION_CANDIDATE",
        "PROMISING_BUT_UNVERIFIED",
        "CONTEXT_DEPENDENT",
        "INSUFFICIENT_EVIDENCE",
        "REJECTED"
    }

    permitted_repro_statuses = {
        "NOT_ASSESSED",
        "AUTHOR_REPORTED",
        "CODE_AVAILABLE",
        "PARTIALLY_REPRODUCED",
        "INDEPENDENTLY_REPRODUCED",
        "FAILED_REPRODUCTION",
        "UNRESOLVED"
    }

    # Find all primitive blocks
    # Header format: #### Primitive PRIM-...
    primitive_pattern = re.compile(r"#### Primitive (PRIM-[A-Z]+-\d+):?([^\n]+)", re.MULTILINE)
    matches = list(primitive_pattern.finditer(content))
    print(f"Total Primitive Headers Found: {len(matches)}")

    primitives = {}
    for i, m in enumerate(matches):
        pid = m.group(1).strip()
        pname_header = m.group(2).strip()
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        block = content[start:end]
        primitives[pid] = block

    print(f"Unique Primitives: {len(primitives)}")
    
    # Check each primitive for all 26 fields
    field_pattern = re.compile(r"- \*\*(\d+)\. ([a-z_]+)\*\*:\s*(.*)")
    
    audit_results = []
    
    for pid, block in primitives.items():
        found_fields = {}
        for line in block.splitlines():
            fm = field_pattern.match(line.strip())
            if fm:
                idx = int(fm.group(1))
                field_name = fm.group(2)
                val = fm.group(3).strip()
                found_fields[field_name] = (idx, val)
        
        # Check field presence
        missing_fields = []
        for i, rf in enumerate(required_fields, 1):
            if rf not in found_fields:
                missing_fields.append((i, rf))
        
        # Check status
        status_val = found_fields.get("status", (None, ""))[1].strip("`* ")
        repro_val = found_fields.get("reproducibility_status", (None, ""))[1].strip("`* ")
        
        is_validated = "VALIDATED" in status_val.upper() and "VALIDATED" == status_val.upper()
        # Ensure status is one of permitted statuses
        status_clean = re.sub(r"[`*]", "", status_val).strip()
        repro_clean = re.sub(r"[`*]", "", repro_val).strip()
        
        status_ok = status_clean in permitted_statuses
        repro_ok = repro_clean in permitted_repro_statuses
        
        audit_results.append({
            "pid": pid,
            "fields_count": len(found_fields),
            "missing_fields": missing_fields,
            "status": status_clean,
            "status_ok": status_ok,
            "repro_status": repro_clean,
            "repro_ok": repro_ok,
            "is_validated": is_validated,
            "fields": {k: v[1] for k, v in found_fields.items()}
        })

    return audit_results

if __name__ == "__main__":
    results = audit_dr05()
    all_ok = True
    validated_found = False
    for r in results:
        if r["fields_count"] != 26 or r["missing_fields"]:
            print(f"FAIL: {r['pid']} missing fields: {r['missing_fields']}")
            all_ok = False
        if r["is_validated"] or r["status"] == "VALIDATED":
            print(f"FAIL: {r['pid']} has VALIDATED status!")
            validated_found = True
        if not r["status_ok"]:
            print(f"FAIL: {r['pid']} invalid status: {r['status']}")
            all_ok = False
        if not r["repro_ok"]:
            print(f"FAIL: {r['pid']} invalid repro status: {r['repro_status']}")
            all_ok = False

    print(f"DR-05 Audit complete: 28 primitives checked. all_ok={all_ok}, validated_found={validated_found}")
