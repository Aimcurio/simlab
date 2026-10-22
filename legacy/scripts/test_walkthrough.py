# Verify documentation walkthrough exists and can be accessed
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
p = ROOT_DIR / "README.md"
print(f"Documentation walkthrough exists at {p}: {os.path.exists(p)}")
