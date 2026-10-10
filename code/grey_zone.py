"""grey_zone.py — decision changes against the FFR grey zone 0.75-0.85 (Petraco et al. 2013), Protocols A-D, primary
run. A flip is 'beyond the grey zone' when the corrupted FFR lies outside 0.75-0.85 on the other side of 0.80 from the
clean FFR; a flip with both values inside 0.75-0.85 is 'within the grey zone'.
usage: grey_zone.py <out_dir>"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import binomtest
sys.path.insert(0, str(Path(__file__).parent))
from summarise_revision import load, ci, KEY
R = Path(__file__).parent.parent / "results"
x = load(R / "ablation-2026-10-07.csv", R / "ablation-perterritory-2026-10-08.csv", R / "discrete_arm_eligibility.csv")
LO, HI = 0.75, 0.85
f0, f1 = x.ffr_clean, x.ffr
x["within"] = (x.flip == 1) & f0.between(LO, HI) & f1.between(LO, HI)
x["beyond"] = (x.flip == 1) & (((f0 > 0.80) & (f1 < LO)) | ((f0 <= 0.80) & (f1 > HI)))
x["clean_in_gz"] = f0.between(LO, HI)
rows = []
for (bed, cls, p), g in x.groupby(["bed", "cls", "protocol"]):
    n, fl, w, b = len(g), int(g.flip.sum()), int(g.within.sum()), int(g.beyond.sum())
    rows.append(dict(bed=bed, cls=cls, protocol=p, n=n, flips=fl, within=w, beyond=b,
                     flip_ci=ci(fl, n), beyond_ci=ci(b, n), within_share=(100 * w / fl if fl else np.nan)))
t = pd.DataFrame(rows); out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
t.to_csv(out / "grey_zone.csv", index=False); print(t.to_string(index=False))
print("\nclean FFR inside grey zone:", x.drop_duplicates(KEY + ["bed"]).groupby("bed").clean_in_gz.mean().round(3).to_dict())
for bed in ("discrete", "leaky"):
    for p in ("A_fixed", "B_rederived", "C_flowmatched", "D_perterritory"):
        g = x[(x.bed == bed) & (x.protocol == p)].groupby(KEY + ["cls"]).beyond.mean().unstack().dropna()
        d = g.topo - g.cal; k, m = int((d > 0).sum()), int((d != 0).sum())
        print(f"{bed:9}{p:16} beyond-grey-zone topo>cal in {k}/{m}, sign test p={binomtest(k, m).pvalue if m else 1:.3g}")
P = {"A_fixed": "A", "B_rederived": "B", "C_flowmatched": "C", "D_perterritory": "D"}
lines = []
for bed in ("discrete", "leaky"):
    for i, (p, pl) in enumerate(P.items()):
        r = {c: t[(t.bed == bed) & (t.cls == c) & (t.protocol == p)].iloc[0] for c in ("topo", "cal")}
        lines.append(f"{bed.capitalize() if i == 0 else ''} & {pl} & {r['topo'].n} & {r['topo'].flip_ci} & {r['topo'].beyond_ci} & "
                     f"{r['cal'].n} & {r['cal'].flip_ci} & {r['cal'].beyond_ci} \\\\")
(Path(__file__).parent.parent / "drafts/manuscript/supplement_tables/tab_greyzone.tex").write_text("\n".join(lines) + "\n")
