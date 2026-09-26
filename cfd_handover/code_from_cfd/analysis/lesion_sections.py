"""Lesion-aware section analysis along the LAD path (Item 3 lesion80 / baseline_ref), replaces the old pullback for these cases.
usage: lesion_sections.py <case_dir> <lesion80|baseline_ref> [time]
Per station (0.25 mm within +-6 mm of the throat incl. the exact throat, 1.5 mm elsewhere, up to arc 50 mm): section area (validated against the
expected 3D area from the baseline sections x f^2), centroid offset, section flux Q, area-averaged static p, mass-flux-weighted total p,
reversed-axial-velocity area fraction, Umax, and the 0D twin's pressure interpolated in arc (design and area-matched variants). Every
number is normalised by P_aorta where a pressure. Raises on an unknown mode."""
import sys, os, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, pyvista as pv
from zerod_ffr import RHO, MU, P_AORTA
from outlets_837 import build_tree
import build_lesion80_case as L
from build_lesion80_surface import build_frames, f_of_s, S_C, LEN, LAD_SID, PR

BASE = L.BASE
MODES = ("lesion80", "baseline_ref")

def zero_d(T, C, mode):
    fr = build_frames(T)
    s_node, _ = L.node_stations(fr)
    out = {}
    variants = {"healthy": None} if mode == "baseline_ref" else {"edt": "edt", "area": "area"}
    for name, var in variants.items():
        if var is None:
            ffr, Qn, info, sten, K = T.evaluate(C)
        else:
            r_ov, idx = L.lesion_r_override(T, var)
            ffr, Qn, info, sten, K = T.evaluate(C, r_override=r_ov)
        node_ids = fr["nodes"]
        o = np.argsort(s_node)
        out[name] = (s_node[o], np.asarray(ffr)[node_ids][o], float(Qn[[v for v in T.leaves if T.label[v] == "LAD"][0]]))
    return fr, out

def stations():
    a = np.arange(PR["SEC_START"], S_C - 6.0 - 1e-9, 1.5)
    b = np.arange(S_C - 6.0, S_C + 6.0 + 1e-9, 0.25)
    c = np.arange(S_C + 6.0 + 1.5, PR["SEC_END"], 1.5)
    return np.unique(np.round(np.concatenate([a, b, c, [S_C]]), 4))

def section(mesh, c_m, t):
    sl = mesh.slice(normal=t, origin=c_m)
    if sl.n_cells == 0:
        return None
    sl = sl.extract_geometry().triangulate().clean()            # robust connectivity: a plain slice can yield mismatched-length arrays that make 'closest' return nothing
    part = sl.connectivity(extraction_mode="closest", closest_point=c_m).compute_cell_sizes(length=False, area=True, volume=False)
    if part.n_cells == 0:
        return None
    A = part.cell_data["Area"]; p = part.cell_data["p"]; U = part.cell_data["U"]
    ut = U @ t; A_tot = A.sum(); Q = float((ut * A).sum())
    ctr = part.cell_centers().points
    cen = (ctr * A[:, None]).sum(0) / A_tot
    pt = p + 0.5 * (U ** 2).sum(1)
    return dict(area=A_tot, Q=Q, p=float((p * A).sum() / A_tot), pt_mw=float((pt * ut * A).sum() / Q) if abs(Q) > 0 else np.nan,
                frac_rev=float(A[ut < 0].sum() / A_tot), umax=float(np.abs(ut).max()), cen=cen, n_cells=int(part.n_cells))

def main(case, mode, time=None):
    if mode not in MODES:
        raise SystemExit(f"unknown mode {mode!r}; expected one of {MODES}")
    T = build_tree(); Qd = T.demand("murray")
    Qd_case = json.load(open(f"{case}/zerod_reference.json"))["Q_demand_mls"] * 1e-6
    if os.path.basename(os.path.normpath(case)).endswith("_hyp"):
        Qd = Qd_case                                           # hyperaemic pair: demand recorded by build_hyp_cases.py
    else:
        assert abs(Qd_case / Qd - 1) < 1e-9, f"{case}: recorded demand {Qd_case} differs from the resting Murray demand {Qd}"
    C = T.calibrate(Qd)
    fr, z = zero_d(T, C, mode)
    ver = json.load(open(f"{BASE}/{PR['DIR']}/geometry_verification.json"))
    st_b = np.array([r["s"] for r in ver["sections"]]); a_b = np.array([r["base"]["area"] for r in ver["sections"]]) * 1e-6
    open(f"{case}/case.foam", "w").close()
    rd = pv.OpenFOAMReader(f"{case}/case.foam")
    rd.set_active_time_value(float(time) if time else rd.time_values[-1])
    rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh")
    mb = rd.read(); mesh = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
    assert float(rd.active_time_value) > 0, f"read time {rd.active_time_value}: solved fields not reconstructed (run reconstructPar -latestTime)"
    print(f"{mode}: 3D time {rd.active_time_value}, cells {mesh.n_cells}")
    rows = []; prev_area = None
    for s in stations():
        k = int(np.argmin(np.abs(fr["s"] - s))); c = fr["c"][k]; t = fr["t"][k]
        r = section(mesh, c * 1e-3, t)
        if r is None:
            rows.append(dict(s_mm=s, ok=False)); continue
        in_win = abs(s - S_C) <= LEN / 2
        f = float(f_of_s(np.array([s]))[0][0]) if mode == "lesion80" else 1.0
        a_exp = float(np.interp(s, st_b, a_b)) * f * f if in_win else np.nan
        off = float(np.linalg.norm(r["cen"] - c * 1e-3))
        req = np.sqrt(r["area"] / np.pi)
        ok = (off < 0.5 * req) and (np.isnan(a_exp) or abs(r["area"] / a_exp - 1) < 0.25)
        if not in_win and prev_area is not None and not (0.6 < r["area"] / prev_area < 1.6):
            ok = False                                              # outside the window: continuity check against the previous valid station (bifurcation sections fail it)
        if ok: prev_area = r["area"]
        row = dict(s_mm=s, ok=bool(ok), area_mm2=r["area"] * 1e6, area_expected_mm2=a_exp * 1e6, r_eq_mm=req * 1e3, centroid_off_over_req=off / req,
                   Q_mls=r["Q"] * 1e6, p_over_Pao=r["p"] * RHO / P_AORTA, ptot_mw_over_Pao=r["pt_mw"] * RHO / P_AORTA,
                   frac_reversed_area=r["frac_rev"], umax_ms=r["umax"], Re_area_eq=2 * RHO * r["Q"] / (np.pi * MU * req) if r["Q"] > 0 else np.nan,
                   n_cells=r["n_cells"])
        for name, (sn, pn, q) in z.items():
            row[f"p0D_{name}_over_Pao"] = float(np.interp(s, sn, pn))
        rows.append(row)
    df = pd.DataFrame(rows)
    num = [c for c in df.columns if c not in ("s_mm", "ok", "area_mm2", "area_expected_mm2", "r_eq_mm", "centroid_off_over_req", "n_cells")]
    df.loc[~df.ok.astype(bool), num] = np.nan               # invalid stations carry NO pressure/flux numbers
    out = f"{case}/sections_{mode}.csv"; df.to_csv(out, index=False)
    json.dump(dict(mode=mode, time=float(rd.active_time_value), cells=int(mesh.n_cells)), open(f"{case}/sections_{mode}.json", "w"))
    bad = df[~df.ok.astype(bool)]
    print(f"stations {len(df)}, failed validation {len(bad)}: {bad.s_mm.tolist()[:20]}")
    thr = df.iloc[(df.s_mm - S_C).abs().argmin()]
    print(f"throat station s={thr.s_mm}: area {thr.area_mm2:.4f} mm2 (expected {thr.area_expected_mm2:.4f}), Q {thr.Q_mls:.5f} mL/s, Re(area-eq) {thr.Re_area_eq:.1f}, "
          f"reversed-area fraction {thr.frac_reversed_area:.3f}, Umax {thr.umax_ms:.2f} m/s")
    print("wrote", out)
    return df

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
