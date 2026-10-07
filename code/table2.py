"""table2.py — Table II (flips and absorption, both beds) as LaTeX rows from the analysis folder."""
import sys
from pathlib import Path
import pandas as pd
an = Path(sys.argv[1])
t = pd.read_csv(an / "P1_flips.csv"); p = pd.read_csv(an / "P2_absorption.csv"); p = p[p.threshold == 0.10]
ET = {"T1_missed_branch": "T1", "T2_truncation": "T2", "T3_stenosis_length": "T3", "T4_taper": "T4"}
PR = {"A_fixed": "A", "B_rederived": "B", "C_flowmatched": "C"}
f = lambda v, lo, hi: f"{v:.0f} ({lo:.0f}--{hi:.0f})"
for e, es in ET.items():
    for k, (pr, ps) in enumerate(PR.items()):
        cells = []
        for bed in ("discrete", "leaky"):
            a = t[(t.bed == bed) & (t.error_type == e) & (t.protocol == pr)].iloc[0]
            b = p[(p.bed == bed) & (p.error_type == e) & (p.protocol == pr)].iloc[0]
            cells += [f"{int(a.n)}", f(a.flip_pct, a.lo, a.hi), f(b.pct, b.lo, b.hi)]
        print(f"{es if k == 0 else ''} & {ps} & " + " & ".join(cells) + r" \\")
    if e != "T4_taper": print(r"\addlinespace[2pt]")
