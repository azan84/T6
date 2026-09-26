"""Discrete-bed status of the 150 selected instances (as selected under the leaky bed, 15:55):
healthy gate, outlet count, measurement node active, discrete baseline FFR_meas, band under discrete."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "code"))
from zerod_ffr import Tree
import severity_sweep as ss
root = Path.home() / "Datasets/imagecas-x/ImageCAS-X_dataset"
sel = pd.read_csv(ROOT / "results" / "sweep_test_selected.csv")
rows = []; cache = {}
for _, r in sel.iterrows():
    key = (int(r.scan), r.side)
    if key not in cache:
        rec = {}
        for bed in ("leaky", "discrete"):
            try:
                t = ss.load(root, r.scan, r.side, bed); o = t.ffr("murray", 1.0); base = t.last["ffr"].copy()
                rec[bed] = dict(t=t, C=o["C"], base=base, err="", hmain=t.healthy_main_ffr(), nout=len(t.leaves))
            except Exception as e:
                rec[bed] = dict(t=None, err=f"{e.__class__.__name__}: {e}")
        cache[key] = rec
    rec = cache[key]; labels = ss.HOSTS[r.side][r.vessel]
    out = dict(scan=r.scan, side=r.side, vessel=r.vessel, loc=r.loc, L_mm=r.L_mm, ds_pct=r.ds_pct, band_leaky=r.band, ffr_meas_leaky_file=r.ffr_meas)
    for bed in ("leaky", "discrete"):
        b = rec[bed]
        if b["t"] is None:
            out[f"{bed}_err"] = b["err"]; continue
        t = b["t"]; p, n_same = t.vessel_path(labels)
        if p is None: out[f"{bed}_err"] = "vessel absent"; continue
        s = t.arc[p] - t.arc[p[0]]; c = r.c_mm * 1e-3; L = r.L_mm * 1e-3
        s_meas = c + L / 2 + ss.RUNOFF
        if s_meas > s[-1]: out[f"{bed}_err"] = f"run-off lost (path ends {s[-1]*1e3:.1f} mm < {s_meas*1e3:.1f})"; continue
        mi = int(np.searchsorted(s, s_meas)); ci = int(np.argmin(np.abs(s - c)))
        rr, nodes = ss.insert(t, p, s, c, L, r.ds_pct / 100)
        ffr, Q, info, sten, K = t.evaluate(b["C"], rr)
        out.update({f"{bed}_ffr_meas": float(ffr[p[mi]]), f"{bed}_base": float(b["base"][p[mi]]), f"{bed}_hmain": b["hmain"], f"{bed}_nout": b["nout"],
                    f"{bed}_resolved_meas": bool(t.resolved[p[mi]]), f"{bed}_conv": info["converged"], f"{bed}_c_snap_mm": float(s[ci] * 1e3),
                    f"{bed}_path_len_mm": float(s[-1] * 1e3)})
        # downstream branch >= cut available? (missed-branch error type needs one distal to the lesion, on the path or off it)
        dn = [v for k, v in enumerate(p) if s[k] >= c + L / 2 and len(t.children[v]) >= 2]
        out[f"{bed}_n_dn_bif"] = len(dn)
        up = [v for k, v in enumerate(p) if s[k] <= c - L / 2 and len(t.children[v]) >= 2]
        out[f"{bed}_n_up_bif"] = len(up)
    rows.append(out)
df = pd.DataFrame(rows); df.to_csv(Path(__file__).with_name("selected150_discrete.csv"), index=False)
edges = np.arange(0.65, 0.9501, 0.05)
ok = df.discrete_ffr_meas.notna()
print("selected 150 under discrete bed (0.60 mm, leaf r^2.66):")
print("  load/solve errors:", df.discrete_err.notna().sum() if "discrete_err" in df else 0)
if "discrete_err" in df: print(df.loc[df.discrete_err.notna(), ["scan","side","vessel","discrete_err"]].drop_duplicates().to_string())
print("  leaky recompute vs file: max |d| =", float((df.leaky_ffr_meas - df.ffr_meas_leaky_file).abs().max()), "(expected ~<0.01: lesion-cap fix)")
print("  trees failing healthy gate (hmain<0.90):", int((df.drop_duplicates(['scan','side']).discrete_hmain < 0.90).sum()), "of", df.drop_duplicates(['scan','side']).shape[0])
print("  instances on gate-failing trees:", int((df.discrete_hmain < 0.90).sum()))
print("  instances single-outlet:", int((df.discrete_nout == 1).sum()), "; zero downstream bifurcation on path (discrete):", int((df.discrete_n_dn_bif == 0).sum()), "; leaky:", int((df.leaky_n_dn_bif == 0).sum()))
print("  measurement node unresolved under discrete:", int((~df.discrete_resolved_meas.fillna(True).astype(bool)).sum()))
elig = ok & (df.discrete_hmain >= 0.90) & (df.discrete_nout >= 2)
print("  eligible (solves, hmain>=0.90, >=2 outlets):", int(elig.sum()), "; +downstream bifurcation:", int((elig & (df.discrete_n_dn_bif > 0)).sum()))
d = df.discrete_ffr_meas - df.leaky_ffr_meas
print(f"  discrete - leaky FFR_meas: mean {d.mean():+.4f} SD {d.std():.4f} min {d.min():+.4f} max {d.max():+.4f}")
print("  decision (<=0.80) disagreement leaky vs discrete:", int(((df.leaky_ffr_meas <= 0.80) != (df.discrete_ffr_meas <= 0.80)).sum()), "of", int(ok.sum()))
df["band_discrete"] = pd.cut(df.discrete_ffr_meas, edges, right=False).astype(str)
print("  band under discrete (rows = leaky band as selected):\n", pd.crosstab(df.band_leaky, df.band_discrete).to_string())
print("  instances with discrete baseline (pre-insertion) FFR at meas node < 0.90:", int((df.discrete_base < 0.90).sum()))
print("  both-structure 0.70-0.90 window (CFD §3 rule) count:", int(((df.leaky_ffr_meas>=0.70)&(df.leaky_ffr_meas<0.90)&(df.discrete_ffr_meas>=0.70)&(df.discrete_ffr_meas<0.90)).sum()),
      "; of which eligible+downstream bif:", int((elig & (df.discrete_n_dn_bif>0) & (df.leaky_ffr_meas>=0.70)&(df.leaky_ffr_meas<0.90)&(df.discrete_ffr_meas>=0.70)&(df.discrete_ffr_meas<0.90)).sum()))
print("  per vessel:", df[elig & (df.discrete_n_dn_bif>0) & (df.leaky_ffr_meas>=0.70)&(df.leaky_ffr_meas<0.90)&(df.discrete_ffr_meas>=0.70)&(df.discrete_ffr_meas<0.90)].vessel.value_counts().to_dict())
