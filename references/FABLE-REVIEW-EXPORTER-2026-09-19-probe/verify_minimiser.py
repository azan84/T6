"""verify_minimiser.py — independent check of the ablation.py Protocol C minimiser fix.
1. scan 341 / RCA / leaky / T1: run the fixed run_instance, then brute-force the loss on a dense log-C grid over
   +/- 3 decades and confirm the recorded C_ratio / dFFR are the GLOBAL optimum; confirm fit_n_basins/fit_at_bound.
2. old vs new on the 6-instance smoke set: diff results/ablation_smoke.csv (pre-fix) against the re-run, and
   brute-force every C row that changed to say which side was right.
usage: verify_minimiser.py <data_root> <abl_new6.csv>
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import minimize_scalar
HERE = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(HERE / "code"))
import ablation as A
from zerod_ffr import Tree
from severity_sweep import load, plan, insert, HOSTS, RUNOFF
from error_types import ERROR_TYPES, T3_LENGTH_DELTA

root = Path(sys.argv[1]).expanduser()
if not (root / "centerlines").is_dir(): root = next(c for c in root.iterdir() if (c / "centerlines").is_dir())
coh = pd.read_csv(HERE / "protocol" / "COHORT-FROZEN-2026-09-18.csv")

def setup(row, bed, etype):
    """Replicates ablation.run_instance up to the Protocol C loss (copied, not imported, so it is independent)."""
    t = load(root, int(row.scan), row.side, bed); o = t.ffr("murray", 1.0); C_clean = o["C"]
    slots, _ = plan(t, row.side, t.last["ffr"].copy())
    sl = next(s for s in slots if s["vessel"] == row.vessel and s["loc"] == row["loc"] and abs(s["L"] * 1e3 - row.L_mm) < 1e-6)
    path, s_arc, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]
    meas_clean = int(path[mi]); ds = row.ds_pct / 100
    r_clean, _ = insert(t, path, s_arc, c, L, ds); ffr0, *_ = t.evaluate(C_clean, r_clean); f0 = float(ffr0[meas_clean])
    q0_all = A.bed_flow(t, C_clean, ffr0)
    segs2, info = ERROR_TYPES[etype](list(t.segments), t, path, s_arc, c, L)
    t2 = Tree(segs2, "x", bed=bed); m = A.node_map(t, t2)
    p2, _ = t2.vessel_path(HOSTS[row.side][row.vessel]); s2 = t2.arc[p2] - t2.arc[p2[0]]
    L2 = L + T3_LENGTH_DELTA if etype == "T3_stenosis_length" else L
    r2, _ = insert(t2, p2, s2, c, L2, ds)
    cand = np.where(m == meas_clean)[0]
    meas2 = int(cand[0]) if len(cand) else int(p2[min(int(np.searchsorted(s2, c + L / 2 + RUNOFF)), len(p2) - 1)])
    t_pairs = []
    for sub in A.territories(t2):
        mc = m[sub][m[sub] >= 0]
        if len(mc) == 0: continue
        q = float(q0_all[mc].sum())
        if q > 0: t_pairs.append((sub, q))
    q_target = np.array([q for _, q in t_pairs])
    t2._C.clear(); C_start = t2.calibrate(t2.demand("murray", 1.0))
    def loss(lc):
        f, *_ = t2.evaluate(10 ** lc, r2); q = A.bed_flow(t2, 10 ** lc, f)
        return float(np.mean(((np.array([q[sub].sum() for sub, _ in t_pairs]) - q_target) / q_target) ** 2))
    def ffr_at(lc): return float(t2.evaluate(10 ** lc, r2)[0][meas2])
    return dict(C_clean=C_clean, C_start=C_start, loss=loss, ffr_at=ffr_at, f0=f0, n_terr=len(t_pairs))

def brute(S, half=3.0, n=1201):
    lc0 = np.log10(S["C_start"]); grid = np.linspace(lc0 - half, lc0 + half, n)
    lv = np.array([S["loss"](x) for x in grid]); k = int(np.argmin(lv))
    res = minimize_scalar(S["loss"], bounds=(grid[max(k - 1, 0)], grid[min(k + 1, n - 1)]), method="bounded", options=dict(xatol=1e-10))
    lc = float(res.x) if res.fun <= lv[k] else float(grid[k])
    minima = [i for i in range(1, n - 1) if lv[i] < lv[i - 1] and lv[i] < lv[i + 1]]
    return dict(C_ratio=10 ** lc / S["C_clean"], loss=min(float(res.fun), lv[k]), ffr=S["ffr_at"](lc), dFFR=S["ffr_at"](lc) - S["f0"],
                n_minima=len(minima), minima_C_ratio=[round(10 ** grid[i] / S["C_clean"], 4) for i in minima],
                minima_loss=[round(float(lv[i]), 5) for i in minima], at_edge=k in (0, n - 1))

def old_fit(S):
    """The pre-fix minimiser: one bounded Brent over +/- 1.5 decades."""
    lc0 = np.log10(S["C_start"])
    res = minimize_scalar(S["loss"], bounds=(lc0 - 1.5, lc0 + 1.5), method="bounded", options=dict(xatol=1e-9))
    return dict(C_ratio=10 ** float(res.x) / S["C_clean"], loss=float(res.fun), dFFR=S["ffr_at"](float(res.x)) - S["f0"])

# ---- 1. scan 341
print("=" * 100 + "\n1. scan 341 / right / RCA / prox 10 mm 70 %DS / leaky / T1_missed_branch\n" + "=" * 100)
row = coh[(coh.scan == 341) & (coh.vessel == "RCA")].iloc[0]
rows, why = A.run_instance(root, row, "leaky"); df = pd.DataFrame(rows)
r = df[(df.error_type == "T1_missed_branch") & (df.protocol == "C_flowmatched")].iloc[0]
print("fixed ablation.py row:", {k: r[k] for k in ("status", "C_ratio", "dFFR", "ffr", "outlet_flow_residual", "fit_n_basins", "fit_loss_at_Cstart", "fit_loss", "fit_at_bound", "n_territories")})
S = setup(row, "leaky", "T1_missed_branch")
b = brute(S); o = old_fit(S)
print("brute force (+/-3 decades, 1201 pts):", b)
print("old minimiser (pre-fix):", o)
print(f"fixed == global: C_ratio diff {abs(r.C_ratio - b['C_ratio']):.2e}, dFFR diff {abs(r.dFFR - b['dFFR']):.2e}")
print(f"all 12 rows of the 341 leaky instance have fit_* columns populated for C: "
      f"{df[df.protocol=='C_flowmatched'][['error_type','status','C_ratio','fit_n_basins','fit_at_bound']].to_string()}")

# ---- 2. old vs new on the smoke set
print("\n" + "=" * 100 + "\n2. pre-fix smoke (results/ablation_smoke.csv) vs fixed re-run, Protocol C rows\n" + "=" * 100)
old = pd.read_csv(HERE / "results" / "ablation_smoke.csv"); new = pd.read_csv(sys.argv[2])
key = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct", "bed", "error_type", "protocol"]
mg = old.merge(new, on=key, suffixes=("_old", "_new"))
print(f"rows old {len(old)} new {len(new)} merged {len(mg)}")
ab = mg[mg.protocol != "C_flowmatched"]
print(f"A/B rows: max |dFFR_new - dFFR_old| = {np.nanmax(np.abs(ab.dFFR_new - ab.dFFR_old)):.2e}, "
      f"max |C_ratio diff| = {np.nanmax(np.abs(ab.C_ratio_new - ab.C_ratio_old)):.2e}, status equal: {(ab.status_old == ab.status_new).all()}")
cc = mg[mg.protocol == "C_flowmatched"].copy()
cc["dC"] = (cc.C_ratio_new - cc.C_ratio_old).abs(); cc["ddFFR"] = (cc.dFFR_new - cc.dFFR_old).abs()
cols = ["scan", "bed", "error_type", "status_old", "status_new", "C_ratio_old", "C_ratio_new", "dFFR_old", "dFFR_new",
        "outlet_flow_residual_old", "outlet_flow_residual_new", "fit_n_basins", "fit_at_bound"]
print(cc[cols].round(4).to_string())
changed = cc[(cc.dC > 1e-3) | (cc.ddFFR > 1e-3) | (cc.status_old != cc.status_new)]
print(f"\nC rows changed by more than 1e-3 (or status): {len(changed)} of {len(cc)}; "
      f"unchanged rows max |dC_ratio| = {cc[~cc.index.isin(changed.index)].dC.max():.2e}, max |d dFFR| = {cc[~cc.index.isin(changed.index)].ddFFR.max():.2e}")
for _, z in changed.iterrows():
    rw = coh[(coh.scan == z.scan) & (coh.side == z.side) & (coh.vessel == z.vessel) & (coh["loc"] == z["loc"]) & (coh.L_mm == z.L_mm) & (coh.ds_pct == z.ds_pct)].iloc[0]
    S = setup(rw, z.bed, z.error_type); b = brute(S)
    print(f"  {z.scan} {z.bed} {z.error_type}: old C_ratio {z.C_ratio_old:.4f} (dFFR {z.dFFR_old:+.4f}) | new {z.C_ratio_new:.4f} ({z.dFFR_new:+.4f}) status_new {z.status_new} | "
          f"brute global {b['C_ratio']:.4f} ({b['dFFR']:+.4f}) loss {b['loss']:.2e}, minima at C_ratio {b['minima_C_ratio']} losses {b['minima_loss']}")
# brute-force a handful of UNCHANGED rows too
print("\nbrute-force spot checks on unchanged rows:")
for _, z in cc[~cc.index.isin(changed.index)].sample(min(6, len(cc)), random_state=1).iterrows():
    rw = coh[(coh.scan == z.scan) & (coh.vessel == z.vessel) & (coh["loc"] == z["loc"]) & (coh.L_mm == z.L_mm) & (coh.ds_pct == z.ds_pct)].iloc[0]
    S = setup(rw, z.bed, z.error_type); b = brute(S)
    print(f"  {z.scan} {z.bed} {z.error_type}: new C_ratio {z.C_ratio_new:.4f} vs brute {b['C_ratio']:.4f} (diff {abs(z.C_ratio_new-b['C_ratio']):.1e}); n_minima brute {b['n_minima']} vs fit_n_basins {z.fit_n_basins}")
