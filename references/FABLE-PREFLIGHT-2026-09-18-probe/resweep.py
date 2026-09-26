"""Re-run the severity sweep with the CURRENT code into the probe dir (never into results/).
usage: resweep.py <data_root> <out_csv> [--cap3]
--cap3 restores the old 'at most 3 lesion terms per segment' rule so that the loader edit (16:51) can be separated
from the lesion-cap removal (17:20) when comparing against results/sweep_test.csv (15:55)."""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
import zerod_ffr
from zerod_ffr import Tree, RHO, KT, DS_LESION
import severity_sweep as ss

root, out = Path(sys.argv[1]), Path(sys.argv[2])
if "--treerule" in sys.argv:
    sys.path.insert(0, str(Path(__file__).resolve().parent)); import runrule2; runrule2.activate(); print("tree-wide run rule active")
if "--cap3" in sys.argv:
    def _set_radius_cap3(self, r):
        self.r = r
        self.stenosis = np.clip(1.0 - self.r / np.maximum(self.r_fit, 1e-9), 0.0, 0.99)
        K = np.zeros(len(r))
        for sid in np.unique(self.seg):
            cand = np.where((self.seg == sid) & self.resolved & (self.stenosis >= DS_LESION))[0]
            n_les = 0
            while len(cand) and n_les < 3:
                v = cand[np.argmax(self.stenosis[cand])]
                A0 = np.pi * self.r_fit[v] ** 2; As = np.pi * self.r[v] ** 2
                K[v] = RHO * KT / (2 * A0 ** 2) * (A0 / As - 1.0) ** 2
                cand = cand[np.abs(self.arc[cand] - self.arc[v]) > 5e-3]; n_les += 1
        self.K = K
    Tree._set_radius = _set_radius_cap3
    print("cap3 monkeypatch active")

meta = ss.scans_of(root, "test"); rows, rej, t0, fails = [], [], time.time(), 0
for n, (sid, m) in enumerate(meta.iterrows(), 1):
    for side in ("left", "right"):
        try:
            t = ss.load(root, sid, side); o = t.ffr("murray", 1.0); base = t.last["ffr"].copy()
            slots, rj = ss.plan(t, side, base); rej += [(sid, side) + r for r in rj]
            for sl in slots:
                for ds in ss.SEVERITIES:
                    r_new, _ = ss.insert(t, sl["path"], sl["s"], sl["c"], sl["L"], ds / 100)
                    ffr, Q, info, _, K = t.evaluate(o["C"], r_new)
                    main = t.resolved & np.isin(t.label, ss.HOSTS[side][sl["vessel"]])
                    rows.append(dict(scan=sid, side=side, quality=int(m["Image Quality"]), dominance=m["Dominance"],
                                     disease=m["Disease"], vessel=sl["vessel"], loc=sl["loc"], c_mm=sl["c"] * 1e3,
                                     L_mm=sl["L"] * 1e3, ds_pct=ds, r_fit_c_mm=sl["r_fit_c_mm"],
                                     d_up_bif_mm=sl["d_up_bif_mm"], d_dn_bif_mm=sl["d_dn_bif_mm"],
                                     bif_in_window=sl["bif_in_window"], r_in_mm=o["r_in_mm"],
                                     base_ffr_meas=sl["base_ffr_meas"], ffr_meas=float(ffr[sl["path"][sl["mi"]]]),
                                     ffr_min_vessel=float(np.nanmin(ffr[main])), Q_in_pre=o["Q_in_mls"],
                                     Q_in_post=info["inflow"] * 1e6, iters=info["iters"], converged=info["converged"],
                                     mass_err=info["mass_err"], n_K=int((K > 0).sum()), n_K_base=int((t.K > 0).sum())))
        except Exception as e:
            fails += 1; print(f"  FAIL {sid} {side}: {e.__class__.__name__}: {e}", file=sys.stderr)
    if n % 20 == 0: print(f"  {n}/{len(meta)} {len(rows)} inst {fails} fails {time.time()-t0:.0f}s", flush=True)
df = pd.DataFrame(rows); df.to_csv(out, index=False)
pd.DataFrame(rej, columns=["scan", "side", "vessel", "loc", "L_mm", "why"]).to_csv(out.with_name(out.stem + "_rejections.csv"), index=False)
print(f"wrote {out}: {len(df)} instances, {fails} failures, {time.time()-t0:.0f}s")
