import re
from pathlib import Path

BASE_DIR = Path("E:/projects/simlab")
RD_DIR = BASE_DIR / "reproduction_design"
MASTER_PKG = BASE_DIR / "curo_reproduction_design_package.md"

def test_master_congruence():
    print("=== TESTING MASTER PACKAGE CONGRUENCE ===")
    master_txt = MASTER_PKG.read_text(encoding="utf-8", errors="replace")
    
    for i in range(1, 17):
        pattern = f"RD-{i:02d}_*.md"
        matches = list(RD_DIR.glob(pattern))
        if not matches:
            print(f"[FAIL] Missing RD-{i:02d}")
            continue
        rd_file = matches[0]
        rd_txt = rd_file.read_text(encoding="utf-8", errors="replace")
        
        # Check if the filename or title appears in master
        file_tag = rd_file.name
        if file_tag not in master_txt:
            print(f"[WARN] Filename {file_tag} not directly found in master package header.")
            
        # Sample lines from the deliverable to verify inclusion
        lines = [line.strip() for line in rd_txt.splitlines() if len(line.strip()) > 30 and not line.strip().startswith("<!--")]
        # Sample 5 distinct lines
        sample_step = max(1, len(lines) // 5)
        samples = [lines[j] for j in range(0, len(lines), sample_step)][:5]
        
        matched_samples = 0
        for s in samples:
            if s in master_txt:
                matched_samples += 1
            else:
                # print sample mismatch
                print(f"  Sample from {file_tag} not found in master:\n    '{s[:80]}...'")
                
        print(f"RD-{i:02d} ({file_tag}): {matched_samples}/{len(samples)} sample sections verified in master package.")

if __name__ == "__main__":
    test_master_congruence()
