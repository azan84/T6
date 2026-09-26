"""B2 attrition: with T2_KEEP_BEYOND = 25 mm, does T2 still have vessel left to delete?
Geometry only — no solve, no FFR. Sorted by scan so imagecasx_loader's EDT cache is hit once per mask."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, "code")
from severity_sweep import load, plan, HOSTS, RUNOFF
from error_types import T2_KEEP_BEYOND
ROOT = Path("/Users/mzpi/Datasets/imagecas-x/ImageCAS-X_dataset")
coh = pd.read_csv("protocol/COHORT-FROZEN-2026-09-18.csv").sort_values(["scan", "side"])
rows = []
for bed in ("leaky", "discrete"):
    for _, r in coh.iterrows():
        try:
            t = load(ROOT, int(r.scan), r.side, bed)
            t.ffr("murray", 1.0)
            sl = next((s for s in plan(t, r.side, t.last["ffr"].copy())[0]
                       if s["vessel"] == r.vessel and s["loc"] == r["loc"] and abs(s["L"]*1e3 - r.L_mm) < 1e-6), None)
            if sl is None:
                rows.append(dict(bed=bed, scan=int(r.scan), applicable=None, why="slot not eligible")); continue
            s_arc, c, L = sl["s"], sl["c"], sl["L"]
            end = float(s_arc[-1]); cut = c + L/2 + T2_KEEP_BEYOND
            rows.append(dict(bed=bed, scan=int(r.scan), vessel=r.vessel,
                             applicable=bool(cut < end), lost_mm=(end - cut)*1e3,
                             margin_meas_mm=(T2_KEEP_BEYOND - RUNOFF)*1e3))
        except Exception as e:
            rows.append(dict(bed=bed, scan=int(r.scan), applicable=None, why=str(e)[:50]))
d = pd.DataFrame(rows); d.to_csv(sys.argv[1], index=False)
print(f"T2 applicability at KEEP = {T2_KEEP_BEYOND*1e3:.0f} mm (was 15 mm), frozen cohort\n")
for bed in ("leaky", "discrete"):
    s = d[d.bed == bed]; ap = s[s.applicable.notna()]
    yes = ap[ap.applicable == True]
    print(f"  {bed:9s}: {len(ap)} instances  |  T2 applicable {len(yes)} ({100*len(yes)/max(len(ap),1):.0f} %)  "
          f"|  run-off deleted: median {yes.lost_mm.median():.1f} mm, p10 {yes.lost_mm.quantile(0.1):.1f}, max {yes.lost_mm.max():.1f}")
    if len(s[s.applicable.isna()]): print(f"             errors/ineligible: {len(s[s.applicable.isna()])}")
