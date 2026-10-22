# Verify the implementation of run_exp_ab_01_comp.py for any bugs, edge cases, tie breaking, etc.
with open(r"E:\projects\simlab\run_exp_ab_01_comp.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in run_exp_ab_01_comp.py: {len(lines)}")
# Check evaluate_query function
for i, l in enumerate(lines):
    if "def evaluate_query" in l:
        print("".join(lines[i:i+65]))
        break
