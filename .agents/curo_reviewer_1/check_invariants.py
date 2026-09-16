import os
import re

deliverables_dir = r"E:\projects\simlab\deliverables"
files = [f"DR-0{i}" for i in range(1, 9)]

for fn in sorted(os.listdir(deliverables_dir)):
    if any(fn.startswith(prefix) for prefix in files):
        fpath = os.path.join(deliverables_dir, fn)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check header lifecycle state
        state_match = re.search(r"Lifecycle State.*?Implementation Authority.*", content)
        state_str = state_match.group(0) if state_match else "NO MATCH"
        
        # Check for VALIDATED
        validated_matches = re.findall(r"\bVALIDATED\b", content)
        
        # Check for IMPLEMENTATION_AUTHORITY
        auth_granted = "IMPLEMENTATION_AUTHORITY: GRANTED" in content.upper() or "AUTHORITY: GRANTED" in content.upper()
        
        print(f"=== {fn} ===")
        print(f"  Header State: {state_str}")
        print(f"  VALIDATED matches: {len(validated_matches)}")
        print(f"  Authority Granted detected: {auth_granted}")
