"""replication_table.py — Supplementary table for the demand replication (code/demand_replication.py) beside the
primary run: per bed and demand scale, class-level flip and passes-and-wrong rates under Protocols A-D.
usage: replication_table.py <out.tex>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from summarise_revision import load, ci, KEY
P6 = Path(__file__).parent.parent; R = P6 / "results"
RUNS = {1: (R / "ablation-2026-10-07.csv", R / "ablation-perterritory-2026-10-08.csv", R / "discrete_arm_eligibility.csv")}
for s in (2, 3):
    d = R / f"demand-replication-x{s}-2026-10-08"
    RUNS[s] = (d / "ablation.csv", d / "ablation-perterritory.csv", d / "discrete_arm_eligibility.csv")
lines = []
for bed in ("discrete", "leaky"):
    for s, paths in RUNS.items():
        x = load(*paths); x = x[x.bed == bed]
        if bed == "discrete" and s == 3: continue
        n = x[KEY].drop_duplicates().shape[0]
        def r(cls, proto, col):
            g = x[(x.cls == cls) & (x.protocol == proto)]
            if col == "pw": g = g.dropna(subset=["outlet_flow_residual"])
            return ci(int(g[col].sum()), len(g))
        lines.append(f"{bed.capitalize() if s == 1 else ''} & {s} & {n} & {r('topo','A_fixed','flip')} & {r('cal','A_fixed','flip')} & "
                     f"{r('topo','C_flowmatched','flip')} & {r('topo','D_perterritory','flip')} & "
                     f"{r('topo','B_rederived','pw')} & {r('topo','C_flowmatched','pw')} & {r('topo','D_perterritory','pw')} & "
                     f"{r('cal','B_rederived','pw')} & {r('cal','C_flowmatched','pw')} & {r('cal','D_perterritory','pw')} \\\\")
Path(sys.argv[1]).write_text("\n".join(lines) + "\n")
print("\n".join(lines))
