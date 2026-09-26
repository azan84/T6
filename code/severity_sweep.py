"""
severity_sweep.py — controlled-stenosis cohort on real ImageCAS-X trees. Implements protocol/SEVERITY-SWEEP-SPEC.md.

  --verify <root> [scan ...]   run checks V1-V10 on a few trees; NOTHING is written. Must pass before --run.
  --run    <root> [--split test]   full factorial on every eligible host -> results/sweep_<split>.csv
  --select <csv>               stratified selection into the Phase 2 cohort -> results/sweep_<split>_selected.csv

Physiology (r_fit, r_ref, bed weights, C) is computed from the ORIGINAL tree and frozen; a lesion changes only the
epicardial radius (Tree.evaluate with r_override).
"""
from __future__ import annotations
import sys, time, argparse
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from zerod_ffr import Tree, Segment, DS_LESION
from imagecasx_loader import load_tree

HOSTS = {"left": {"LAD": ("LAD",), "LCX": ("LCX", "LCx")}, "right": {"RCA": ("RCA",)}}
LOCS = {"prox": 20e-3, "mid": 45e-3}            # lesion centre from vessel origin (m), snapped to nearest node
LENGTHS = (10e-3, 20e-3)
SEVERITIES = (40, 50, 55, 60, 65, 70, 75, 80)   # %DS relative to healthy reference
MIN_HOST_RFIT, RUNOFF, NATIVE_MAX, BASE_MIN, QUALITY_MIN = 1.0e-3, 20e-3, 0.40, 0.90, 2
SEED = 20260918

def insert(tree: Tree, path, s, c, L, ds_frac):
    inw = np.abs(s - c) < L / 2
    w = 0.5 * (1 + np.cos(np.pi * (s[inw] - c) / (L / 2)))
    nodes = path[inw]; r_new = tree.r.copy()
    r_new[nodes] = np.minimum(tree.r[nodes], (1 - w) * tree.r[nodes] + w * tree.r_fit[nodes] * (1 - ds_frac))
    return r_new, nodes

def plan(tree: Tree, side: str, base_ffr):
    """Eligible (vessel, location, length) slots for one tree, with the reason for every rejection."""
    slots, rejects = [], []
    for vessel, labels in HOSTS[side].items():
        path, n_same = tree.vessel_path(labels)
        if path is None: rejects.append((vessel, "-", "-", "vessel absent")); continue
        s = tree.arc[path] - tree.arc[path[0]]; s_same = s[n_same - 1]
        bif = np.array([s[k] for k, v in enumerate(path) if len(tree.children[v]) >= 2])
        for loc, c0 in LOCS.items():
            for L in LENGTHS:
                ci = int(np.argmin(np.abs(s - c0))); c = s[ci]; why = None
                if c - L / 2 < 0 or c + L / 2 > s_same: why = "window outside same-label vessel"
                elif tree.r_fit[path[ci]] < MIN_HOST_RFIT: why = f"host r_fit {tree.r_fit[path[ci]]*1e3:.2f} mm < 1.0"
                else:
                    s_meas = c + L / 2 + RUNOFF
                    if s_meas > s[-1]: why = "run-off < 20 mm"
                    else:
                        mi = int(np.searchsorted(s, s_meas))
                        span = (s >= c - L / 2 - 5e-3) & (s <= s[mi])
                        if not tree.resolved[path[mi]]: why = "measurement node unresolved"
                        elif tree.stenosis[path[span]].max() >= NATIVE_MAX: why = f"native {100*tree.stenosis[path[span]].max():.0f}%DS >= 40"
                        elif base_ffr[path[mi]] < BASE_MIN: why = f"baseline FFR {base_ffr[path[mi]]:.3f} < 0.90"
                if why: rejects.append((vessel, loc, int(L * 1e3), why)); continue
                up = bif[bif <= c - L / 2]; dn = bif[bif >= c + L / 2]
                slots.append(dict(vessel=vessel, loc=loc, L=L, c=c, ci=ci, mi=mi, path=path, s=s,
                                  r_fit_c_mm=tree.r_fit[path[ci]] * 1e3,
                                  d_up_bif_mm=float((c - L / 2 - up.max()) * 1e3) if len(up) else np.nan,
                                  d_dn_bif_mm=float((dn.min() - c - L / 2) * 1e3) if len(dn) else np.nan,
                                  bif_in_window=bool(((bif > c - L / 2) & (bif < c + L / 2)).any()),
                                  base_ffr_meas=float(base_ffr[path[mi]])))
    return slots, rejects

def refine(segments):
    out = []
    for sg in segments:
        n = len(sg.r); p = np.empty((2 * n - 1, 3)); r = np.empty(2 * n - 1)
        p[0::2] = sg.pts; r[0::2] = sg.r; p[1::2] = 0.5 * (sg.pts[1:] + sg.pts[:-1]); r[1::2] = 0.5 * (sg.r[1:] + sg.r[:-1])
        out.append(Segment(sg.sid, sg.parent, p, r, sg.label))
    return out

def scans_of(root: Path, split: str):
    d = pd.read_excel(root / "Descriptors.xlsx"); d.columns = [c.strip() for c in d.columns]
    d["Scan ID"] = d["Scan ID"].astype(int); d = d[d["Image Quality"] >= QUALITY_MIN]
    keep = {int(l) for l in (root / "filelist" / f"{split}.txt").read_text().split()}
    return d[d["Scan ID"].isin(keep)].set_index("Scan ID")

def load(root, sid, side, bed="leaky"):
    return load_tree(str(root / "centerlines" / f"{sid}.coronary_{side}_centerline.vtk"),
                     str(root / "segmentations" / f"{sid}.coronary.nii.gz"), name=f"{sid}_{side}", bed=bed)

# ----------------------------------------------------------------------------------------------- verify
def verify(root: Path, scan_ids, bed="leaky"):
    print(f"bed structure: {bed}")
    meta = scans_of(root, "test")
    ids = [int(x) for x in scan_ids] or list(meta.index[:6])
    e0 = pd.read_csv(Path(__file__).parent.parent / "results" / "E0_prevalence_test.csv")
    e0 = e0[(e0["mode"] == "murray") & (e0.scale == 1.0)].set_index(["scan", "side"]).min_ffr_main
    W = dict(v1=0.0, v1_out=0.0, widen=0, v2=True, v3=0.0, v3K=True, v4=0, v4n=0, v5=0, v5n=0, v6=0.0, v7=True,
             itmax=0, v8=0.0, v8b=0.0, v8b_out=0, v8n=0, v9=0, v10=0.0, vnan=0, v3n=0, v3nn=0, v3native=0, n_inst=0, n_slots=0)
    rej_all = []
    for sid in ids:
        for side in ("left", "right"):
            t = load(root, sid, side, bed); o = t.ffr("murray", 1.0); C = o["C"]; base = t.last["ffr"].copy()
            if bed == "leaky" and (sid, side) in e0.index: W["v10"] = max(W["v10"], abs(o["min_ffr_main"] - e0[(sid, side)]))
            frozen = (t.r_ref.copy(), t.r_fit.copy(), t.w.copy(), t.r.copy())
            slots, rej = plan(t, side, base); rej_all += [(sid, side) + r for r in rej]; W["n_slots"] += len(slots)
            t2 = None
            for sl in slots:
                prev = None
                for ds in SEVERITIES:
                    r_new, nodes = insert(t, sl["path"], sl["s"], sl["c"], sl["L"], ds / 100)
                    ffr, Q, info, sten, K = t.evaluate(C, r_new); W["n_inst"] += 1
                    cnode = sl["path"][sl["ci"]]
                    W["v1"] = max(W["v1"], abs(r_new[cnode] / t.r_fit[cnode] - (1 - ds / 100)))
                    out = np.setdiff1d(np.arange(len(t.r)), nodes)
                    W["v1_out"] = max(W["v1_out"], float(np.abs(r_new[out] - frozen[3][out]).max()))
                    W["widen"] += int((r_new > frozen[3] + 1e-15).sum())
                    W["v2"] &= (np.array_equal(t.r_ref, frozen[0]) and np.array_equal(t.r_fit, frozen[1])
                                and np.array_equal(t.w, frozen[2]) and np.array_equal(t.r, frozen[3]) and t.calibrate(t.demand()) == C)
                    W["v3"] = max(W["v3"], abs(sten[cnode] - ds / 100)); W["v3K"] &= bool(K[cnode] > 0)
                    # V3b: the inserted lesion must produce exactly ONE expansion-loss term. A second term inside the
                    # window is a defect (shoulder term, or a bifurcation double-count — the 2026-09-18 pre-flight
                    # finding) UNLESS it is a genuine native narrowing, i.e. already >= DS_LESION before insertion.
                    kn = nodes[K[nodes] > 0]
                    if len(kn):
                        thr = kn[np.argmax(sten[kn])]
                        spurious = [v for v in kn if v != thr and t.stenosis[v] < DS_LESION - 1e-9]
                        W["v3n"] = max(W["v3n"], 1 + len(spurious)); W["v3nn"] += 1
                        W["v3native"] += int(len(kn) - 1 - len(spurious))
                    f = float(ffr[sl["path"][sl["mi"]]])
                    if prev is not None:
                        W["v4n"] += 1; W["v4"] += int(not f < prev)
                    prev = f; sl.setdefault("f", {})[ds] = f
                    # NaN-safe: max(0.0, nan) is 0.0, so a NaN solve used to pass V6 silently (review §5.2).
                    W["v6"] = np.nanmax([W["v6"], info["mass_err"]]) if np.isfinite(info["mass_err"]) else np.inf
                    W["vnan"] += int(not (np.isfinite(info["mass_err"]) and np.isfinite(info["inflow"]) and np.isfinite(f)))
                    W["v7"] &= info["converged"]; W["itmax"] = max(W["itmax"], info["iters"])
                    W["v9"] += int(info["inflow"] > o["Q_in_mls"] * 1e-6 * (1 + 1e-9))
                # V8 on the 60 % instance of each slot: halve the centreline spacing, redo the same insertion by arc
                if t2 is None:
                    # V8a: SOLVER discretisation only — the healthy reference and hence the bed/outlet set are
                    # inherited from the coarse tree. Re-fitting the reference on the refined centreline is a separate
                    # (larger) sensitivity, measured as V8b below.
                    t2 = Tree(refine(t.segments), t.name + "_fine", bed=t.bed, reference=t)
                    C2 = t2.ffr("murray", 1.0)["C"]
                    t3 = Tree(refine(t.segments), t.name + "_refit", bed=t.bed); C3 = t3.ffr("murray", 1.0)["C"]
                    W["v8b_out"] = max(W["v8b_out"], abs(len(t3.leaves) - len(t.leaves)))
                vessel_labels = HOSTS[side][sl["vessel"]]; p2, _ = t2.vessel_path(vessel_labels); s2 = t2.arc[p2] - t2.arc[p2[0]]
                r2, _ = insert(t2, p2, s2, sl["c"], sl["L"], 0.60)
                f2 = t2.evaluate(C2, r2)[0][p2[int(np.searchsorted(s2, sl["c"] + sl["L"] / 2 + RUNOFF))]]
                W["v8"] = max(W["v8"], abs(float(f2) - sl["f"][60])); W["v8n"] += 1
                p3, _ = t3.vessel_path(vessel_labels); s3 = t3.arc[p3] - t3.arc[p3[0]]
                r3, _ = insert(t3, p3, s3, sl["c"], sl["L"], 0.60)
                f3 = t3.evaluate(C3, r3)[0][p3[int(np.searchsorted(s3, sl["c"] + sl["L"] / 2 + RUNOFF))]]
                W["v8b"] = max(W["v8b"], abs(float(f3) - sl["f"][60]))
            # V5: 20 mm vs 10 mm at same vessel/location/severity
            by = {(sl["vessel"], sl["loc"], sl["L"]): sl for sl in slots}
            for (v, l, L), sl in by.items():
                if L == LENGTHS[0] and (v, l, LENGTHS[1]) in by:
                    for ds in SEVERITIES:
                        W["v5n"] += 1; W["v5"] += int(by[(v, l, LENGTHS[1])]["f"][ds] > sl["f"][ds] + 1e-9)
    ok = lambda c: "PASS" if c else "FAIL"
    print(f"\nverified on scans {ids}: {W['n_slots']} eligible slots, {W['n_inst']} instances\n")
    rows = [("V1  insertion exact at throat", W["v1"] < 1e-9, f"max |r/r_fit-(1-DS)| = {W['v1']:.1e}"),
            ("V1b untouched outside window", W["v1_out"] == 0.0 and W["widen"] == 0, f"max change {W['v1_out']:.1e}; widened nodes {W['widen']}"),
            ("V2  physiology frozen (r_ref, r_fit, bed, C)", W["v2"], "bit-identical" if W["v2"] else "CHANGED"),
            ("V3  detected %DS = inserted; K>0 at throat", W["v3"] < 1e-9 and W["v3K"], f"max |DS err| = {W['v3']:.1e}"),
            ("V3b no spurious K term from the insertion", W["v3n"] == 1,
             f"max non-native K terms in window = {W['v3n']} over {W['v3nn']} instances ({W['v3native']} genuine native lesions coexisted)"),
            ("V4  FFR strictly decreasing in %DS", W["v4"] == 0, f"{W['v4']} violations / {W['v4n']} steps"),
            ("V5  longer lesion never raises FFR", W["v5"] == 0, f"{W['v5']} violations / {W['v5n']} pairs"),
            ("V6  mass balance", W["v6"] < 1e-6, f"max rel. error {W['v6']:.1e}"),
            ("V6b no NaN in any solve (mass err / inflow / FFR)", W["vnan"] == 0, f"{W['vnan']} NaN results"),
            ("V7  all solves converged", W["v7"], f"max iterations {W['itmax']}"),
            ("V8a solver discretisation (reference inherited)", W["v8"] < 0.005, f"max |dFFR| = {W['v8']:.4f} over {W['v8n']} slots"),
            ("V8b + healthy reference re-fitted (reported, not a gate)", True,
             f"max |dFFR| = {W['v8b']:.4f}; outlet-count change up to {W['v8b_out']}"),
            ("V9  inflow never rises after insertion", W["v9"] == 0, f"{W['v9']} violations"),
            ("V10 regression vs E0 natural cohort", W["v10"] < 0.005,
             f"max |d min-FFR| = {W['v10']:.4f}" if bed == "leaky" else "n/a — no discrete-bed E0 reference exists")]
    for name, c, note in rows: print(f"  {ok(c):4}  {name:<48} {note}")
    rj = pd.DataFrame(rej_all, columns=["scan", "side", "vessel", "loc", "L_mm", "why"])
    rj["why"] = rj.why.str.replace(r"[\d.]+", "#", regex=True)
    print("\nrejection reasons in these trees:"); print(rj.why.value_counts().to_string())
    allok = all(c for _, c, _ in rows); print("\nOVERALL:", "ALL CHECKS PASS — safe to --run" if allok else "DO NOT RUN — fix failures first")
    return allok

# ----------------------------------------------------------------------------------------------- run
def run(root: Path, split: str):
    meta = scans_of(root, split); rows, rej, t0, fails = [], [], time.time(), 0
    for n, (sid, m) in enumerate(meta.iterrows(), 1):
        for side in ("left", "right"):
            try:
                t = load(root, sid, side); o = t.ffr("murray", 1.0); base = t.last["ffr"].copy()
                slots, rj = plan(t, side, base); rej += [(sid, side) + r for r in rj]
                for sl in slots:
                    for ds in SEVERITIES:
                        r_new, _ = insert(t, sl["path"], sl["s"], sl["c"], sl["L"], ds / 100)
                        ffr, Q, info, _, _ = t.evaluate(o["C"], r_new)
                        main = t.resolved & np.isin(t.label, HOSTS[side][sl["vessel"]])
                        rows.append(dict(scan=sid, side=side, quality=int(m["Image Quality"]), dominance=m["Dominance"],
                                         disease=m["Disease"], vessel=sl["vessel"], loc=sl["loc"], c_mm=sl["c"] * 1e3,
                                         L_mm=sl["L"] * 1e3, ds_pct=ds, r_fit_c_mm=sl["r_fit_c_mm"],
                                         d_up_bif_mm=sl["d_up_bif_mm"], d_dn_bif_mm=sl["d_dn_bif_mm"],
                                         bif_in_window=sl["bif_in_window"], r_in_mm=o["r_in_mm"],
                                         base_ffr_meas=sl["base_ffr_meas"], ffr_meas=float(ffr[sl["path"][sl["mi"]]]),
                                         ffr_min_vessel=float(np.nanmin(ffr[main])), Q_in_pre=o["Q_in_mls"],
                                         Q_in_post=info["inflow"] * 1e6, iters=info["iters"], converged=info["converged"],
                                         mass_err=info["mass_err"]))
            except Exception as e:
                fails += 1; print(f"  FAIL {sid} {side}: {e.__class__.__name__}: {e}", file=sys.stderr)
        if n % 20 == 0: print(f"  {n}/{len(meta)} scans  {len(rows)} instances  {fails} failures  {time.time()-t0:.0f}s", flush=True)
    res = Path(__file__).parent.parent / "results"; res.mkdir(exist_ok=True)
    df = pd.DataFrame(rows); df.to_csv(res / f"sweep_{split}.csv", index=False)
    pd.DataFrame(rej, columns=["scan", "side", "vessel", "loc", "L_mm", "why"]).to_csv(res / f"sweep_{split}_rejections.csv", index=False)
    print(f"\nwrote results/sweep_{split}.csv: {len(df)} instances, {df.groupby(['scan','side','vessel']).ngroups} hosts, "
          f"{df.scan.nunique()} scans, {fails} failures, {time.time()-t0:.0f}s")
    summarise(df)

def summarise(df):
    bands = np.arange(0.40, 1.0001, 0.05)
    print(f"\nnon-converged: {int((~df.converged).sum())};  max mass error {df.mass_err.max():.1e};  baseline FFR_meas median {df.base_ffr_meas.median():.3f}")
    print("\nFFR_meas by inserted severity (median [p10, p90]):")
    for ds, g in df.groupby("ds_pct"): print(f"   {ds:>3}%DS  {g.ffr_meas.median():.3f}  [{g.ffr_meas.quantile(.1):.3f}, {g.ffr_meas.quantile(.9):.3f}]   <=0.80: {100*(g.ffr_meas<=0.80).mean():5.1f}%")
    print("\ninstances per FFR_meas band (supply for selection):")
    h, _ = np.histogram(df.ffr_meas, bins=bands)
    for lo, c in zip(bands[:-1], h): print(f"   [{lo:.2f},{lo+0.05:.2f})  {c:6d}  {'#' * int(60 * c / max(h.max(), 1))}")
    print("\nhosts by vessel:"); print(df.groupby("vessel").apply(lambda g: g.groupby(["scan", "side"]).ngroups, include_groups=False).to_string())

def select(csv_path, per_band=25, max_per_tree=2):
    df = pd.read_csv(csv_path); df = df[df.converged]; rng = np.random.default_rng(SEED)
    edges = np.arange(0.65, 0.9501, 0.05); df["band"] = pd.cut(df.ffr_meas, edges, right=False)
    df = df.dropna(subset=["band"]).sample(frac=1.0, random_state=SEED)
    per_tree, used_host_band, chosen = {}, set(), []
    for band in sorted(df.band.unique(), key=lambda b: (df.band == b).sum()):          # scarcest band first
        pool = df[df.band == band]; got = 0; vessels = list(rng.permutation(pool.vessel.unique()))
        while got < per_band:
            progressed = False
            for v in vessels:
                for idx, row in pool[pool.vessel == v].iterrows():
                    tree, host = (row.scan, row.side), (row.scan, row.side, row.vessel, str(band))
                    if idx in chosen or per_tree.get(tree, 0) >= max_per_tree or host in used_host_band: continue
                    chosen.append(idx); per_tree[tree] = per_tree.get(tree, 0) + 1; used_host_band.add(host); got += 1; progressed = True; break
                if got >= per_band: break
            if not progressed: break
    sel = df.loc[chosen].sort_values(["band", "vessel", "scan"]); out = Path(csv_path).with_name(Path(csv_path).stem + "_selected.csv")
    sel.to_csv(out, index=False)
    print(f"selected {len(sel)} instances from {sel.groupby(['scan','side']).ngroups} trees (seed {SEED}) -> {out.name}")
    print(pd.crosstab(sel.band, sel.vessel, margins=True).to_string())
    print("\nshortfall vs target of", per_band, "per band:", {str(b): per_band - int(n) for b, n in sel.band.value_counts().items() if n < per_band} or "none")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--verify", nargs="+"); g.add_argument("--run", nargs=1); g.add_argument("--select", nargs=1)
    ap.add_argument("--split", default="test"); ap.add_argument("--bed", default="leaky", choices=("leaky", "discrete"))
    a = ap.parse_args()
    if a.verify: sys.exit(0 if verify(Path(a.verify[0]), a.verify[1:], a.bed) else 1)
    if a.run: run(Path(a.run[0]), a.split)
    if a.select: select(a.select[0])
