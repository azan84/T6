"""CFD-ARM-SPEC §10, protocol-grade: truncation-radius survival counts.
Tree OUTER, cut INNER — the EDT load dominates, so loading once and rebuilding at three cuts is ~3x cheaper.
Writes incrementally so a kill leaves partial results rather than nothing."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, "code")
from zerod_ffr import Tree
from severity_sweep import plan
from imagecasx_loader import load_tree
ROOT = Path("/Users/mzpi/Datasets/imagecas-x/ImageCAS-X_dataset")
out = Path(sys.argv[1])
coh = pd.read_csv("protocol/COHORT-FROZEN-2026-09-18.csv")
trees = coh[["scan", "side"]].drop_duplicates().sort_values(["scan", "side"])
rows = []
for i, (_, tr) in enumerate(trees.iterrows(), 1):
    try:
        t = load_tree(str(ROOT / "centerlines" / f"{int(tr.scan)}.coronary_{tr.side}_centerline.vtk"),
                      str(ROOT / "segmentations" / f"{int(tr.scan)}.coronary.nii.gz"),
                      name=f"{tr.scan}_{tr.side}", bed="discrete")
        segs = t.segments
    except Exception as e:
        rows.append(dict(scan=int(tr.scan), side=tr.side, cut_mm=np.nan, ok=False, err=f"load: {e}"[:70])); continue
    for cut in (0.60e-3, 0.75e-3, 1.00e-3):
        try:
            t2 = Tree(segs, t.name, bed="discrete", r_trunc=cut)
            t2.ffr("murray", 1.0)
            slots, _ = plan(t2, tr.side, t2.last["ffr"].copy())
            n_del = 0
            for sl in slots:
                path, s_arc, c, L = sl["path"], sl["s"], sl["c"], sl["L"]
                pset = set(int(v) for v in path)
                n_del += bool([c_ for k, v in enumerate(path) for c_ in t2.children[v]
                               if int(c_) not in pset and s_arc[k] >= c + L / 2])
            rows.append(dict(scan=int(tr.scan), side=tr.side, cut_mm=cut * 1e3, ok=True,
                             n_outlets=len(t2.leaves), single_outlet=len(t2.leaves) <= 1,
                             n_slots=len(slots), n_slots_with_deletable=n_del))
        except Exception as e:
            rows.append(dict(scan=int(tr.scan), side=tr.side, cut_mm=cut * 1e3, ok=False, err=str(e)[:70]))
    if i % 10 == 0:
        pd.DataFrame(rows).to_csv(out, index=False)
        print(f"  {i}/{len(trees)} trees", flush=True)
d = pd.DataFrame(rows); d.to_csv(out, index=False)
print(f"\n{'cut mm':>7} {'built':>6} {'single-outlet':>16} {'slots':>7} {'with deletable':>18}")
for cut, g in d[d.ok == True].groupby("cut_mm"):
    pct = 100 * g.n_slots_with_deletable.sum() / max(g.n_slots.sum(), 1)
    print(f"{cut:>7.2f} {len(g):>6} {int(g.single_outlet.sum()):>9}/{len(g):<6} "
          f"{int(g.n_slots.sum()):>7} {int(g.n_slots_with_deletable.sum()):>8} ({pct:.0f}%)")
fails = d[d.ok != True]
if len(fails): print(f"\n{len(fails)} tree-cut combinations failed to build (expected at the larger cuts):")
for cut, g in fails.groupby("cut_mm", dropna=False): print(f"   cut {cut}: {len(g)}")
