"""Wall-shear-stress based separation/reattachment metrics along the LAD (Item 3 lesion80 / baseline_ref).
usage: reattachment_wss.py <case_dir> <lesion80|baseline_ref> [time]
Needs the wallShearStress field on patch 'wall' at the read time (function object, or `simpleFoam -postProcess -func "wallShearStress(patches=(wall))" -latestTime`).
OpenFOAM's field is KINEMATIC and equals (-Sf/|Sf|) & Reff, i.e. NEGATIVE for forward flow; forward-positive axial WSS is tau = -rho * (wss . t).
The sign is CALIBRATED on the undisturbed proximal LM wall (>=90 % of faces must come out forward-positive or the script aborts).
Wall faces are assigned to the LAD PATH (all segments on the root->LAD path, nearest-segment map as in the geometry build, and within 3 mm of the smoothed axis), stations are <=0.25 mm slabs (+-0.125 mm), everything area-weighted.
Per station: circumferential mean tau, minimum tau, 5th percentile, reversed-wall-area fraction f_rev, number of faces. A circumferential mean alone can hide a
recirculation zone in a curved vessel, so reattachment is defined on f_rev (sustained f_rev<1 % over >=1 mm) and the mean-tau sign change is reported as a second, weaker estimate.
Stations beyond the D1 ostium proximal edge (s>=30.0 mm) are junction-influenced: the onset search and the WHOLE sustained-recovery window (>=1 mm between first and last station centre, no missing stations) must lie below it; otherwise the outcome is CENSORED, not a measurement."""
import sys, os, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, pyvista as pv
from zerod_ffr import RHO
from outlets_837 import build_tree
import build_lesion80_surface as G

MODES = ("lesion80", "baseline_ref")
S_JUNCTION = G.PR["JUNCTION"]   # lesion80: D1 ostium at arc 32.0, proximal edge ~30-30.5 (profile value)
SLAB = 0.125               # half-width (mm)
DS = 0.25                  # station spacing (mm)
FREV_TOL, SUSTAIN = 0.01, 1.0

def load_wall(case, time):
    open(f"{case}/case.foam", "w").close()
    rd = pv.OpenFOAMReader(f"{case}/case.foam")
    rd.set_active_time_value(float(time) if time else rd.time_values[-1])
    names = list(rd.patch_array_names)
    wall = [n for n in names if n.endswith("/wall") or n == "wall"]
    assert wall, names
    rd.disable_all_patch_arrays(); rd.enable_patch_array(wall[0])
    mb = rd.read()
    poly = None
    def find(b):
        nonlocal poly
        for i in range(b.n_blocks):
            x = b[i]
            if isinstance(x, pv.MultiBlock): find(x)
            elif x is not None and x.n_cells > 0 and "wallShearStress" in x.cell_data: poly = x if poly is None else poly.merge(x)
    find(mb)
    assert poly is not None, "no wallShearStress on the wall patch (run the function object / postProcess first)"
    poly = poly.extract_surface().compute_cell_sizes(length=False, area=True, volume=False)
    return poly, rd.active_time_value

def main(case, mode, time=None):
    if mode not in MODES:
        raise SystemExit(f"unknown mode {mode!r}")
    T = build_tree(); T.ffr(mode="murray"); dfm = G.Deformer(T); fr = dfm.fr
    poly, tval = load_wall(case, time)
    assert float(tval) > 0, f"read time {tval}: the solved fields were not reconstructed (use reconstructPar -latestTime first)"
    ctr = np.asarray(poly.cell_centers().points) * 1e3            # mm
    A = poly.cell_data["Area"]; W = np.asarray(poly.cell_data["wallShearStress"])
    d, i, sid = dfm.project(ctr)
    path_sids = set(int(x) for x in T.seg[fr["nodes"]])
    lad = np.isin(sid, list(path_sids)) & (d < 3.0)
    s = fr["s"][i]; tt = fr["t"][i]
    tau_raw = -RHO * np.einsum("ij,ij->i", W, tt)                  # forward-positive IF the OpenFOAM sign convention holds
    cal = lad & (s > 2.0) & (s < 12.0)
    frac_fwd = float((tau_raw[cal] > 0).mean()); med = float(np.median(tau_raw[cal]))
    print(f"{mode}: read t={tval}, {poly.n_cells} wall faces, {lad.sum()} LAD-assigned; sign calibration on proximal LM (s 2-12 mm, {cal.sum()} faces): "
          f"{100*frac_fwd:.1f} % forward-positive, median tau {med:.3f} Pa")
    assert frac_fwd > 0.90 and med > 0, "sign calibration failed: forward-positive axial WSS is not the majority on the undisturbed wall"
    rows = []
    for st in np.arange(G.PR["WSS_START"], G.PR["WSS_END"] + 1e-9, DS):
        m = lad & (np.abs(s - st) <= SLAB)
        if m.sum() < 10:
            rows.append(dict(s_mm=st, n=int(m.sum()))); continue
        a = A[m]; tv = tau_raw[m]; ww = a / a.sum()
        rows.append(dict(s_mm=st, n=int(m.sum()), tau_mean_Pa=float((tv * ww).sum()), tau_min_Pa=float(tv.min()),
                         tau_p5_Pa=float(np.percentile(tv, 5)), f_rev=float(a[tv < 0].sum() / a.sum()),
                         tau_absmean_Pa=float((np.abs(tv) * ww).sum())))
    df = pd.DataFrame(rows); df.to_csv(f"{case}/wss_{mode}.csv", index=False)
    ok = df.dropna(subset=["f_rev"])
    # analysis window: throat to the junction edge only; missing stations stay as NaN rows so a recovery test can never bridge a gap;
    # the whole sustain window must lie in the uncensored region (all stations < S_JUNCTION)
    win = df[(df.s_mm >= G.S_C) & (df.s_mm < S_JUNCTION)].reset_index(drop=True)
    post = win.dropna(subset=["f_rev"])
    n_need = int(round(SUSTAIN / DS)) + 1                          # stations >= SUSTAIN apart between first and last centre (each slab is 2*SLAB = DS wide)
    fv = win.f_rev.values; sv = win.s_mm.values
    rev = np.where(np.isnan(fv), False, fv >= FREV_TOL)
    have = ~np.isnan(fv)
    onset = float(sv[rev.argmax()]) if rev.any() else None
    reatt = None
    if onset is not None:
        for k in np.where(sv > onset)[0]:
            w = slice(k, k + n_need)
            if len(fv[w]) == n_need and have[w].all() and (fv[w] < FREV_TOL).all():
                reatt = float(sv[k]); break
    n_missing = int((~have).sum())
    rev_any = post[post.f_rev >= FREV_TOL]
    mean_sign = post[post.tau_mean_Pa < 0]
    post_all = ok[ok.s_mm >= G.S_C]                                 # includes the junction-influenced part, reported separately, never used for the reattachment call
    res = dict(mode=mode, time=float(tval), peak_f_rev_before_junction=float(post.f_rev.max()), s_of_peak_f_rev=float(post.s_mm.values[post.f_rev.values.argmax()]), peak_f_rev_junction_influenced=float(post_all[post_all.s_mm >= S_JUNCTION].f_rev.max()) if (post_all.s_mm >= S_JUNCTION).any() else None, missing_stations_in_window=n_missing,
               last_station_f_rev_ge_1pct_before_junction=float(rev_any.s_mm.max()) if len(rev_any) else None,
               separation_onset_s_mm=onset, reattachment_s_mm_f_rev_rule=reatt, distance_from_throat_mm=(reatt - G.S_C) if reatt is not None else None,
               reattached_before_junction=bool(reatt is not None and reatt < S_JUNCTION),
               min_tau_mean_after_throat_Pa=float(post.tau_mean_Pa.min()), stations_with_negative_mean_tau=mean_sign.s_mm.tolist()[:40],
               tau_mean_at_throat_Pa=float(ok.iloc[(ok.s_mm - G.S_C).abs().argmin()].tau_mean_Pa), calibration=dict(frac_forward=frac_fwd, median_Pa=med))
    res["outcome"] = ("no resolved separation (f_rev < 1 % everywhere after the throat)" if onset is None else
                      (f"separation from s={onset:.2f}, reattached at s={reatt:.2f} ({reatt-G.S_C:.2f} mm past the throat)" if (reatt is not None and reatt < S_JUNCTION)
                       else f"separation from s={onset:.2f}, NOT reattached before the {G.PR['JUNCTION_NAME']} ostium influence (s>={S_JUNCTION}): censored"))
    json.dump(res, open(f"{case}/wss_{mode}.json", "w"), indent=1)
    print(json.dumps(res, indent=1))
    return df, res

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
