import sys, numpy as np, pandas as pd
sys.path.insert(0, "code")
from zerod_ffr import Tree, R_TRUNC_DISCRETE
from severity_sweep import load, plan, insert, HOSTS, RUNOFF
from error_types import T4_RADIUS_SCALE
from pathlib import Path
ROOT = Path("/Users/mzpi/Datasets/imagecas-x/ImageCAS-X_dataset")
coh = pd.read_csv("protocol/COHORT-FROZEN-2026-09-18.csv")
rows = []
for bed in ("leaky", "discrete"):
    for _, r in coh.iterrows():
        try:
            t = load(ROOT, int(r.scan), r.side, bed)
            o = t.ffr("murray", 1.0)
            sl = next((s for s in plan(t, r.side, t.last["ffr"].copy())[0]
                       if s["vessel"] == r.vessel and s["loc"] == r["loc"] and abs(s["L"]*1e3 - r.L_mm) < 1e-6), None)
            if sl is None: continue
            s_arc, c, L = sl["s"], sl["c"], sl["L"]
            end = float(s_arc[-1])                     # host path length incl. run-off
            runoff_beyond = {k: end - (c + L/2 + k*1e-3) for k in (15, 20, 22, 25, 30)}
            d = dict(bed=bed, scan=int(r.scan), vessel=r.vessel, end_mm=end*1e3,
                     meas_mm=(c + L/2 + RUNOFF)*1e3, **{f"beyond{k}": v*1e3 for k, v in runoff_beyond.items()})
            # B3: how many discrete leaves fall below the cut when radii scale by 0.93
            if bed == "discrete":
                n_below = int(((t.r_ref[t.leaves] * T4_RADIUS_SCALE) < R_TRUNC_DISCRETE).sum())
                d.update(n_leaves=len(t.leaves), n_leaves_lost_T4=n_below)
            rows.append(d)
        except Exception as e:
            rows.append(dict(bed=bed, scan=int(r.scan), err=str(e)[:40]))
df = pd.DataFrame(rows); df.to_csv(sys.argv[1], index=False)
ok = df[df.get("err").isna()] if "err" in df else df
print("=== B2: run-off available beyond the truncation point (mm), frozen cohort ===")
for k in (15, 20, 22, 25, 30):
    v = ok[f"beyond{k}"].dropna()
    print(f"  KEEP={k:2d} mm: median {v.median():6.1f}  >0 in {int((v>0).sum()):3d}/{len(v)}  "
          f">5mm in {int((v>5).sum()):3d}  >10mm in {int((v>10).sum()):3d}")
print("\n=== B3: discrete leaves pushed below the 0.60 mm cut by T4's 0.93 scaling ===")
dd = ok[ok.bed == "discrete"]
print(f"  instances: {len(dd)}   total leaves {int(dd.n_leaves.sum())}   lost under T4 {int(dd.n_leaves_lost_T4.sum())} "
      f"({100*dd.n_leaves_lost_T4.sum()/dd.n_leaves.sum():.0f}%)")
print(f"  instances losing EVERY leaf: {int((dd.n_leaves_lost_T4 >= dd.n_leaves).sum())}")
print(f"  instances losing >=1 leaf  : {int((dd.n_leaves_lost_T4 > 0).sum())}")
