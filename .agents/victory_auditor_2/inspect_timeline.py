import os
import re
from pathlib import Path

AGENTS_DIR = Path("E:/projects/simlab/.agents")

def inspect_agent_timeline():
    print("=== TIMELINE RECONSTRUCTION ===")
    agents = [
        "orchestrator_3",
        "phase2_explorer_1", "phase2_explorer_2", "phase2_explorer_3",
        "phase2_reviewer_1", "phase2_reviewer_2",
        "phase2_challenger_1", "phase2_challenger_2",
        "phase2_auditor_1",
        "phase2_worker_1", "phase2_worker_2",
        "phase2_remedy_reviewer", "phase2_remedy_auditor"
    ]
    
    for ag in agents:
        ag_dir = AGENTS_DIR / ag
        if not ag_dir.exists():
            print(f"[MISSING AGENT DIR] {ag}")
            continue
        handoff = ag_dir / "handoff.md"
        progress = ag_dir / "progress.md"
        briefing = ag_dir / "BRIEFING.md"
        dispatch = ag_dir / "DISPATCH.md"
        
        info = []
        for f, name in [(dispatch, "dispatch"), (progress, "progress"), (handoff, "handoff")]:
            if f.exists():
                mtime = f.stat().st_mtime
                import datetime
                dt = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                # extract conclusion or status
                txt = f.read_text(encoding="utf-8", errors="replace")
                status = "N/A"
                for line in txt.splitlines():
                    if "conclusion" in line.lower() or "verdict" in line.lower() or "status:" in line.lower() or "gate result:" in line.lower():
                        status = line.strip()
                        break
                info.append(f"{name} ({dt}): {status[:80]}")
            else:
                info.append(f"{name}: missing")
        print(f"Agent {ag:25s} | " + " | ".join(info))

if __name__ == "__main__":
    inspect_agent_timeline()
