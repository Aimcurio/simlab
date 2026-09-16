import sys
import re

print("Auditing Code Citations & Repository Commits...")

# 1. Check System 5 (Puppeteer / Evolving Orchestration)
with open(r"E:\projects\simlab\deliverables\DR-02_source_authority_map.md", encoding="utf-8") as f:
    dr02 = f.read()

with open(r"E:\projects\simlab\deliverables\DR-04_paper_code_mapping.md", encoding="utf-8") as f:
    dr04 = f.read()

with open(r"E:\projects\simlab\deliverables\DR-05_primitive_evidence_matrix.md", encoding="utf-8") as f:
    dr05 = f.read()

# Verify commit hash of Puppeteer
puppeteer_commit = "b24e6e6bd00bb04d317e0447cb7acb1e4973c83a"
assert puppeteer_commit in dr02, "Puppeteer commit missing in DR-02"
assert "OpenBMB/ChatDev" in dr02, "ChatDev repo missing in DR-02"
assert "puppeteer" in dr02, "puppeteer branch missing in DR-02"
assert "puppeteer" in dr04, "puppeteer branch missing in DR-04"
assert "puppeteer" in dr05, "puppeteer branch missing in DR-05"

# 2. Check Smallville commit
smallville_commit = "fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4"
assert smallville_commit in dr02, "Smallville commit missing in DR-02"
assert "joonspk-research/generative_agents" in dr02, "Smallville repo missing in DR-02"
assert "fe05a71" in dr05, "Smallville commit missing in DR-05"

# 3. Check AI Hospital commit and disambiguation
ai_hospital_commit = "870fc38c1daffa549c20332d273a8ad71b9d9fe1"
assert ai_hospital_commit in dr02, "AI Hospital commit missing in DR-02"
assert "LibertFan/AI_Hospital" in dr02, "LibertFan repo missing in DR-02"
assert "LibertFan" in dr04, "LibertFan missing in DR-04"
assert "LibertFan" in dr05, "LibertFan missing in DR-05"
assert "Agent Hospital" in dr02, "Agent Hospital disambiguation missing in DR-02"
assert "Zhang et al." in dr02, "Zhang et al. disambiguation missing in DR-02"
assert "Fan et al." in dr02, "Fan et al. disambiguation missing in DR-02"

# 4. Check ChatDev commit / release
assert "OpenBMB/ChatDev" in dr02, "ChatDev repo missing in DR-02"
assert "5defde31" in dr02, "ChatDev historical release missing in DR-02"

# 5. Check AgentVerse commit / release
assert "OpenBMB/AgentVerse" in dr02, "AgentVerse repo missing in DR-02"
assert "6d42bb6e" in dr02, "AgentVerse release missing in DR-02"

print("All repository identities, branches, commits, and disambiguations verified!")
