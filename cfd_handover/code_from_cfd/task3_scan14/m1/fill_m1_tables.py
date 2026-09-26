"""Regenerates m1/tables_m1.tex (make_tables.py) and inserts it between %%M1_TABLES_BEGIN / %%M1_TABLES_END in the manuscript."""
import subprocess, re
P = "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot/m1"; TEX = "/mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex"
subprocess.run(["python3", f"{P}/make_tables.py"], check=True, stdout=subprocess.DEVNULL); tab = open(f"{P}/tables_m1.tex").read()
s = open(TEX).read(); a = s.index("%%M1_TABLES_BEGIN") + len("%%M1_TABLES_BEGIN"); b = s.index("%%M1_TABLES_END")
open(TEX, "w").write(s[:a] + "\n" + tab + "\n" + s[b:]); print("tables inserted:", tab.count("\\begin{table}"))
