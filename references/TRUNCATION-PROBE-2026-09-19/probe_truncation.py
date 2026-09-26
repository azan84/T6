"""CFD-ARM-SPEC §10 item 1, protocol-grade: the truncation-radius survival counts.

The spec chose 0.60 mm over 0.75 mm on a reviewer's probe over 140 trees, claiming that at 0.75 mm only 54 % of
lesion slots keep a deletable downstream branch and 43/140 trees collapse to a single outlet, against 77 % and
18/140 at 0.60 mm. That choice is pre-registered; the numbers behind it were never reproduced with the protocol
solver. This reproduces them on the FROZEN cohort's trees.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, "code")
from zerod_ffr import Tree
from severity_sweep import load, plan, HOSTS
from imagecasx_loader import load_tree
ROOT = Path("/Users/mzpi/Datasets/imagecas-x/ImageCAS-X_dataset")
coh = pd.read_csv("protocol/COHORT-FROZEN-2026-09-18.csv")
trees = coh[["scan", "side"]].drop_duplicates().sort_values(["scan", "side"])
rows = []
for cut in (0.60e-3, 0.75e-3, 1.00e-3):
    for _, tr in trees.iterrows():
        try:
            t = load_tree(str(ROOT / "centerlines" / f"{int(tr.scan)}.coronary_{tr.side}_centerline.vtk"),
                          str(ROOT / "segmentations" / f"{int(tr.scan)}.coronary.nii.gz"),
                          name=f"{tr.scan}_{tr.side}", bed="discrete")
            t2 = Tree(t.segments, t.name, bed="discrete", r_trunc=cut)
            o = t2.ffr("murray", 1.0)
            slots, _ = plan(t2, tr.side, t2.last["ffr"].copy())
            n_slots = len(slots); n_deletable = 0
            for sl in slots:
                path, s_arc, c, L = sl["path"], sl["s"], sl["c"], sl["L"]
                pset = set(int(v) for v in path)
                cand = [c_ for k, v in enumerate(path) for c_ in t2.children[v]
                        if int(c_) not in pset and s_arc[k] >= c + L / 2]
                n_deletable += bool(cand)
            rows.append(dict(cut_mm=cut * 1e3, scan=int(tr.scan), side=tr.side, ok=True,
                             n_outlets=len(t2.leaves), single_outlet=len(t2.leaves) <= 1,
                             n_slots=n_slots, n_slots_with_deletable=n_deletable))
        except Exception as e:
            rows.append(dict(cut_mm=cut * 1e3, scan=int(tr.scan), side=tr.side, ok=False, err=str(e)[:60]))
d = pd.DataFrame(rows); d.to_csv(sys.argv[1], index=False)
print(f"trees attempted per cut: {len(trees)}\n")
print(f"{'cut mm':>7} {'built':>6} {'single-outlet':>14} {'slots':>7} {'with deletable branch':>22}")
for cut, g in d.groupby("cut_mm"):
    b = g[g.ok == True]
    pct = 100 * b.n_slots_with_deletable.sum() / max(b.n_slots.sum(), 1)
    print(f"{cut:>7.2f} {len(b):>6} {int(b.single_outlet.sum()):>8}/{len(b):<5} "
          f"{int(b.n_slots.sum()):>7} {int(b.n_slots_with_deletable.sum()):>10} ({pct:.0f}%)")
    if len(g) - len(b): print(f"        {len(g)-len(b)} trees failed to build at this cut")
