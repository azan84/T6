import sys, numpy as np, pandas as pd
from pathlib import Path
CODE = Path("/Users/mzpi/Library/CloudStorage/GoogleDrive-Mohd.Zulhilmi@monash.edu/My Drive/Research/01 CollabProject-MonashIIUM/Imaging-Medical/Paper6-T6/code")
sys.path.insert(0, str(CODE))
import zerod_ffr as Z
from zerod_ffr import Tree
import severity_sweep as SS
_orig = Tree.__init__
def _init(self, segments, name=""):
    self._segs = segments; _orig(self, segments, name)
Tree.__init__ = _init
root = Path.home() / "Datasets/imagecas-x/ImageCAS-X_dataset"
if not (root / "centerlines").exists():
    root = next(p.parent for p in (Path.home() / "Datasets/imagecas-x").rglob("centerlines"))
sel = pd.read_csv(CODE.parent / "results/sweep_test_selected.csv")
rows = []
for (sid, side), g in sel.groupby(["scan", "side"]):
    Z.R_TRUNC = 0.5e-3
    t = SS.load(root, int(sid), side); o = t.ffr("murray", 1.0); base = t.last["ffr"].copy()
    slots, _ = SS.plan(t, side, base)
    leaf = t.active & np.array([len(c) == 0 for c in t.children])
    leaf_frac = t.w[leaf].sum() / t.w.sum()
    disc = {}
    for T in (1.0e-3, 0.75e-3, 0.5e-3):
        Z.R_TRUNC = T; d = Tree(t._segs, t.name)
        lf = d.active & np.array([len(c) == 0 for c in d.children])
        d.w = np.where(lf, d.r_ref ** 3, 0.0); d._C = {}
        Cd = d.calibrate(d.demand("murray", 1.0)); fb, *_ = d.evaluate(Cd, None)
        disc[T] = (d, Cd, fb, int(lf.sum()))
    Z.R_TRUNC = 0.5e-3
    for _, r in g.iterrows():
        sl = [s for s in slots if s["vessel"] == r.vessel and s["loc"] == r["loc"] and abs(s["L"] * 1e3 - r.L_mm) < 1e-6]
        if not sl: continue
        sl = sl[0]; path, s, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]
        r_new, _ = SS.insert(t, path, s, c, L, r.ds_pct / 100)
        f, *_ = t.evaluate(o["C"], r_new); meas = path[mi]
        pset = set(path.tolist()); br = []
        for k, v in enumerate(path):
            for ch in t.children[v]:
                if ch not in pset:
                    pos = "up" if s[k] <= c - L / 2 else ("win" if s[k] < c + L / 2 else ("mid" if s[k] <= s[mi] else "dist"))
                    br.append((pos, t.r_ref[ch] * 1e3))
        row = dict(scan=sid, side=side, vessel=r.vessel, ds=r.ds_pct, ffr_leaky=f[meas], ffr_csv=r.ffr_meas,
                   rref_meas=t.r_ref[meas] * 1e3, rfit_meas=t.r_fit[meas] * 1e3, leaf_frac=leaf_frac, n_br=len(br),
                   n_br_ge1=sum(b[1] >= 1.0 for b in br), n_br_075_1=sum(0.75 <= b[1] < 1.0 for b in br),
                   n_br_lt075=sum(b[1] < 0.75 for b in br),
                   n_dn_ge1=sum(b[1] >= 1.0 and b[0] in ("mid", "dist", "win") for b in br),
                   n_dn_all=sum(b[0] in ("mid", "dist", "win") for b in br),
                   n_mid_ge1=sum(b[1] >= 1.0 and b[0] == "mid" for b in br), n_mid_all=sum(b[0] == "mid" for b in br))
        for T, (d, Cd, fb, nl) in disc.items():
            k = f"{T*1e3:.2f}"; row[f"act_meas_{k}"] = bool(d.active[meas]); row[f"nout_{k}"] = nl
            if d.active[meas]:
                fd, *_ = d.evaluate(Cd, r_new); row[f"base_{k}"] = fb[meas]; row[f"ffr_{k}"] = fd[meas]
            # retained length of host path distal to lesion
            act = d.active[path]; row[f"runoff_{k}"] = (s[act].max() - (c + L / 2)) * 1e3 if act.any() else np.nan
        rows.append(row)
df = pd.DataFrame(rows); df.to_csv(Path(__file__).parent / "trunc_check.csv", index=False)
pd.set_option("display.width", 200)
print("n", len(df), " max|leaky-csv|", (df.ffr_leaky - df.ffr_csv).abs().max())
print("r_ref at meas node mm:", df.rref_meas.describe()[["min", "25%", "50%", "75%", "max"]].round(3).to_dict())
print("leaf weight fraction (leaky model; rest is distributed leak):", df.leaf_frac.describe()[["min", "25%", "50%", "75%", "max"]].round(3).to_dict())
for k in ("1.00", "0.75", "0.50"):
    a = df[f"act_meas_{k}"]; sub = df[a]
    print(f"\n== discrete, trunc {k} mm: meas node retained {a.sum()}/{len(df)}; outlets median {df[f'nout_{k}'].median()} (min {df[f'nout_{k}'].min()}); runoff distal to lesion median {df[f'runoff_{k}'].median():.1f} mm, <20mm in {(df[f'runoff_{k}']<20).sum()}")
    if len(sub):
        dlt = sub[f"ffr_{k}"] - sub.ffr_leaky
        print(f"   baseline(no lesion) FFR at meas: median {sub[f'base_{k}'].median():.3f}, min {sub[f'base_{k}'].min():.3f}, <0.90 in {(sub[f'base_{k}']<0.90).sum()}")
        print(f"   FFR discrete-leaky: mean {dlt.mean():+.3f} sd {dlt.std():.3f} min {dlt.min():+.3f} max {dlt.max():+.3f}; decision disagreement {((sub[f'ffr_{k}']<=0.8)!=(sub.ffr_leaky<=0.8)).sum()}/{len(sub)}")
print("\nside branches off host path per instance: total median", df.n_br.median(), "| >=1.0mm median", df.n_br_ge1.median(), "| sum >=1.0:", df.n_br_ge1.sum(), " 0.75-1.0:", df.n_br_075_1.sum(), " <0.75:", df.n_br_lt075.sum())
print("instances with NO side branch >=1.0 mm on host path:", (df.n_br_ge1 == 0).sum(), "/", len(df))
print("instances with NO downstream(of lesion prox edge) branch >=1.0mm:", (df.n_dn_ge1 == 0).sum(), " (any size: ", (df.n_dn_all == 0).sum(), ")")
print("instances with a branch between lesion and meas node: >=1.0mm", (df.n_mid_ge1 > 0).sum(), " any size", (df.n_mid_all > 0).sum())
