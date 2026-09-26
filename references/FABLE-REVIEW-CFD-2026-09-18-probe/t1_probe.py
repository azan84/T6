# Reviewer's probe (NOT protocol-grade): missed downstream side branch under leaky vs discrete BC structure, protocols A/B/C.
import sys, numpy as np, pandas as pd
from pathlib import Path
from scipy.optimize import minimize_scalar
CODE = Path("/Users/mzpi/Library/CloudStorage/GoogleDrive-Mohd.Zulhilmi@monash.edu/My Drive/Research/01 CollabProject-MonashIIUM/Imaging-Medical/Paper6-T6/code")
sys.path.insert(0, str(CODE))
import zerod_ffr as Z
from zerod_ffr import Tree
import severity_sweep as SS
_orig = Tree.__init__
def _init(self, segments, name=""):
    self._segs = segments; _orig(self, segments, name)
    segs = {s.sid: s for s in segments}; kids = {k: [] for k in segs}; root = None
    for s in segments:
        if s.parent is None: root = s.sid
        else: kids[s.parent].append(s.sid)
    order, q = [], [root]
    while q: u = q.pop(0); order.append(u); q += kids[u]
    X = [segs[root].pts[0]]
    for sid in order: X += list(segs[sid].pts[1:])
    self.xyz = np.array(X)
Tree.__init__ = _init
def build(segs, name, trunc, discrete):
    Z.R_TRUNC = trunc; d = Tree(segs, name); Z.R_TRUNC = 0.5e-3
    if discrete:
        lf = d.active & np.array([len(c) == 0 for c in d.children]); d.w = np.where(lf, d.r_ref ** 3, 0.0); d._C = {}
    return d
def leaves(d): return np.where(d.active & np.array([len(c) == 0 for c in d.children]))[0]
def bedflow(d, C, f): return d.w / C * (f * Z.P_AORTA - Z.P_VEN)
root = next(p.parent for p in (Path.home() / "Datasets/imagecas-x").rglob("centerlines"))
sel = pd.read_csv(CODE.parent / "results/sweep_test_selected.csv"); rows = []
for (sid, side), g in sel.groupby(["scan", "side"]):
    t0 = SS.load(root, int(sid), side); o = t0.ffr("murray", 1.0); slots, _ = SS.plan(t0, side, t0.last["ffr"].copy())
    for _, r in g.iterrows():
        sl = [s for s in slots if s["vessel"] == r.vessel and s["loc"] == r["loc"] and abs(s["L"] * 1e3 - r.L_mm) < 1e-6]
        if not sl: continue
        sl = sl[0]; path, s, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]; pset = set(path.tolist())
        cand = [(t0.r_ref[ch], ch, s[k]) for k, v in enumerate(path) for ch in t0.children[v]
                if ch not in pset and s[k] >= c + L / 2 and t0.r_ref[ch] >= 0.75e-3]
        if not cand: continue
        rb, ch, sb = max(cand); r_new0, _ = SS.insert(t0, path, s, c, L, r.ds_pct / 100)
        dead = {int(t0.seg[ch])}; grew = True
        while grew:
            grew = False
            for sg in t0._segs:
                if sg.parent in dead and sg.sid not in dead: dead.add(sg.sid); grew = True
        segs_bad = [sg for sg in t0._segs if sg.sid not in dead]
        row = dict(scan=sid, side=side, vessel=r.vessel, ds=r.ds_pct, r_branch=rb * 1e3, r_host=sl["r_fit_c_mm"],
                   branch_before_meas=bool(sb <= s[mi]))
        for tag, trunc, disc in (("leaky", 0.5e-3, False), ("disc", 0.75e-3, True)):
            cl = build(t0._segs, "c", trunc, disc); bad = build(segs_bad, "b", trunc, disc)
            key = {tuple(np.round(x, 9)): i for i, x in enumerate(cl.xyz)}
            m = np.array([key[tuple(np.round(x, 9))] for x in bad.xyz])          # bad node -> clean node
            meas_b = int(np.where(m == path[mi])[0][0])
            Cc = cl.calibrate(cl.demand()); fc, Qc, ic, *_ = cl.evaluate(Cc, r_new0)
            rb_new = r_new0[m]
            # A: beds frozen from clean (weights of surviving nodes and C unchanged)
            wB = bad.w.copy(); bad.w = np.where(bad.active, cl.w[m], 0.0); fA, *_ = bad.evaluate(Cc, rb_new); bad.w = wB
            # B: re-derived from corrupted geometry, recalibrated to the demand
            bad._C = {}; Cb = bad.calibrate(bad.demand()); fB, *_ = bad.evaluate(Cb, rb_new)
            # C: one global scale tuned so surviving outlets reproduce the clean outlets' flows and pressures
            lv = leaves(bad); lv = lv[cl.active[m[lv]]]; q0 = bedflow(cl, Cc, fc)[m[lv]]; p0 = fc[m[lv]]
            ok = q0 > 0
            def loss(lc):
                f, *_ = bad.evaluate(10 ** lc, rb_new); q = bedflow(bad, 10 ** lc, f)[lv]
                return np.mean(((q[ok] - q0[ok]) / q0[ok]) ** 2) + np.mean(((f[lv] - p0) / p0) ** 2)
            res = minimize_scalar(loss, bounds=(np.log10(Cb) - 1, np.log10(Cb) + 1), method="bounded", options=dict(xatol=1e-6))
            fC, *_ = bad.evaluate(10 ** res.x, rb_new); qC = bedflow(bad, 10 ** res.x, fC)[lv]
            qB = bedflow(bad, Cb, fB)[lv]
            row.update({f"{tag}_clean": fc[path[mi]], f"{tag}_A": fA[meas_b], f"{tag}_B": fB[meas_b], f"{tag}_C": fC[meas_b],
                        f"{tag}_nout": len(lv), f"{tag}_resB": np.sqrt(np.mean(((qB[ok] - q0[ok]) / q0[ok]) ** 2)),
                        f"{tag}_resC": np.sqrt(np.mean(((qC[ok] - q0[ok]) / q0[ok]) ** 2)),
                        f"{tag}_presC": np.max(np.abs(fC[lv] - p0))})
        rows.append(row)
df = pd.DataFrame(rows); df.to_csv(Path(__file__).parent / "t1_probe.csv", index=False)
print("instances with a downstream side branch >=0.75 mm:", len(df), "| branch/host radius ratio median", (df.r_branch / df.r_host).median().round(2),
      "| branch proximal to meas node:", int(df.branch_before_meas.sum()))
for tag in ("leaky", "disc"):
    print(f"\n== {tag}: clean FFR median {df[f'{tag}_clean'].median():.3f}; surviving outlets median {df[f'{tag}_nout'].median():.0f}")
    for p in "ABC":
        d = df[f"{tag}_{p}"] - df[f"{tag}_clean"]; fl = ((df[f"{tag}_{p}"] <= .8) != (df[f"{tag}_clean"] <= .8))
        print(f"   {p}: dFFR mean {d.mean():+.4f}  mean|d| {d.abs().mean():.4f}  max|d| {d.abs().max():.4f}  flips {fl.sum()}/{len(df)}")
    print(f"   outlet-flow RMS residual vs clean: B {df[f'{tag}_resB'].median():.3f} (median)  C {df[f'{tag}_resC'].median():.3f}; max outlet pressure error under C (FFR units) median {df[f'{tag}_presC'].median():.4f}")
near = df[(df.disc_clean.between(.7, .9))]
print("\nnear-threshold under discrete (0.70-0.90):", len(near), " flips A/B/C:", [int(((near[f'disc_{p}'] <= .8) != (near.disc_clean <= .8)).sum()) for p in "ABC"])
near = df[(df.leaky_clean.between(.7, .9))]
print("near-threshold under leaky (0.70-0.90):", len(near), " flips A/B/C:", [int(((near[f'leaky_{p}'] <= .8) != (near.leaky_clean <= .8)).sum()) for p in "ABC"])
