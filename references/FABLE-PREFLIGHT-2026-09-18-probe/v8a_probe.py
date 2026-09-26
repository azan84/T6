"""V8a deep dive: 993_left LCX prox L=20mm, discrete bed. Decompose the 0.0054 refinement change and test convergence
order with 2x and 4x refinement (reference inherited from the coarse tree in every case)."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "code"))
from zerod_ffr import Tree, MU, R_FLOOR
import severity_sweep as ss
root = Path.home() / "Datasets/imagecas-x/ImageCAS-X_dataset"

def refine_n(segments, k):
    out = segments
    for _ in range(k): out = ss.refine(out)
    return out

def slot_ffr(t, C, vessel_labels, c, L, ds, s_shift=0.0):
    p, _ = t.vessel_path(vessel_labels); s = t.arc[p] - t.arc[p[0]]
    r, nodes = ss.insert(t, p, s, c, L, ds)
    ffr, Q, info, sten, K = t.evaluate(C, r)
    mi = int(np.searchsorted(s, c + L / 2 + ss.RUNOFF + s_shift))
    return dict(f=float(ffr[p[mi]]), s_meas=float(s[mi] * 1e3), nK=int((K > 0).sum()), nK_path=int((K[p] > 0).sum()),
                K_path_mm=np.round(s[K[p] > 0] * 1e3, 2).tolist(), n_win=int(len(nodes)), C=C, nout=len(t.leaves),
                Qin=info["inflow"] * 1e6, ffr_path=ffr[p], s_path=s, Q_path=Q[p], r_path=r[p], p=p)

for bed in ("discrete", "leaky"):
    t = ss.load(root, 993, "left", bed); o = t.ffr("murray", 1.0); C = o["C"]; base = t.last["ffr"].copy()
    slots, rej = ss.plan(t, "left", base)
    sl = [s for s in slots if s["vessel"] == "LCX" and s["loc"] == "prox" and abs(s["L"] - 20e-3) < 1e-9][0]
    labels = ss.HOSTS["left"]["LCX"]
    ds_native = t.ds[t.active]
    print(f"\n=== bed={bed}: native node spacing on active nodes: median {np.median(ds_native)*1e3:.3f} mm, p90 {np.percentile(ds_native,90)*1e3:.3f}, max {ds_native.max()*1e3:.3f}")
    print(f"slot c={sl['c']*1e3:.2f} mm L=20 r_fit_c={sl['r_fit_c_mm']:.2f} base_ffr_meas={sl['base_ffr_meas']:.4f}")
    res = {}
    for k in (0, 1, 2, 3):
        tk = t if k == 0 else Tree(refine_n(t.segments, k), f"993_left_x{2**k}", bed=bed, reference=t)
        Ck = tk.ffr("murray", 1.0)["C"]
        r = slot_ffr(tk, Ck, labels, sl["c"], sl["L"], 0.60)
        res[k] = r
        # also: same refinement but evaluated with the COARSE C (isolates bed/C change from solver discretisation)
        rC = slot_ffr(tk, C, labels, sl["c"], sl["L"], 0.60)
        # and at the coarse measurement arc exactly (isolate measurement-node snap)
        print(f"  x{2**k:<2} FFR_meas={r['f']:.5f}  (with coarse C: {rC['f']:.5f})  s_meas={r['s_meas']:.2f} mm  nK={r['nK']} nK_on_path={r['nK_path']} at {r['K_path_mm']}  win_nodes={r['n_win']}  C={r['C']:.4f} nout={r['nout']} Qin={r['Qin']:.4f}")
    f = [res[k]["f"] for k in (0, 1, 2, 3)]
    d = [f[i] - f[i + 1] for i in range(3)]
    print(f"  successive differences: {d[0]:+.5f}, {d[1]:+.5f}, {d[2]:+.5f}; ratios {d[0]/d[1] if d[1] else float('nan'):.2f}, {d[1]/d[2] if d[2] else float('nan'):.2f}  (2nd order => 4)")
    if d[1] != 0:
        ext = f[3] + d[2] / 3.0 if d[2] else f[3]
        print(f"  Richardson estimate of converged FFR_meas: {ext:.5f}; coarse error {f[0]-ext:+.5f}; x2 error {f[1]-ext:+.5f}")
    # measurement-node interpolation: coarse FFR interpolated at the FINE s_meas, and gradient
    r0 = res[0]; r1 = res[1]
    g = np.interp(r1["s_meas"] * 1e-3, r0["s_path"], r0["ffr_path"])
    print(f"  coarse FFR linearly interpolated at fine s_meas ({r1['s_meas']:.2f} mm) = {g:.5f} vs coarse at own node {r0['f']:.5f} -> snap contributes {r0['f']-g:+.5f}")
    # where does the extra drop come from? cumulative FFR along path at coarse vs x2 (sampled on coarse arc)
    f1_on0 = np.interp(r0["s_path"], r1["s_path"], r1["ffr_path"])
    dd = r0["ffr_path"] - f1_on0
    win = (r0["s_path"] >= sl["c"] - sl["L"] / 2) & (r0["s_path"] <= sl["c"] + sl["L"] / 2)
    i_up = np.searchsorted(r0["s_path"], sl["c"] - sl["L"] / 2); i_dn = np.searchsorted(r0["s_path"], sl["c"] + sl["L"] / 2); i_m = np.searchsorted(r0["s_path"], r0["s_meas"] * 1e-3)
    print(f"  coarse-minus-fine FFR along path: at window start {dd[i_up]:+.5f}, at window end {dd[min(i_dn,len(dd)-1)]:+.5f}, at meas node {dd[min(i_m,len(dd)-1)]:+.5f}")
    # Jensen check: Poiseuille sum over the window with r_mid averaging, coarse vs fine at the same Q
    for k in (0, 1, 2):
        rk = res[k]; s, rr = rk["s_path"], rk["r_path"]
        w = (s >= sl["c"] - sl["L"] / 2) & (s <= sl["c"] + sl["L"] / 2)
        idx = np.where(w)[0]
        Rw = sum(8 * MU * (s[j] - s[j - 1]) / (np.pi * max(0.5 * (rr[j] + rr[j - 1]), R_FLOOR) ** 4) for j in idx[1:])
        print(f"  x{2**k}: Poiseuille R over window (r_mid averaging) = {Rw:.4e} Pa s/m3; x Q_meas => {Rw*rk['Q_path'][idx[-1]]/133.322:.3f} mmHg")
