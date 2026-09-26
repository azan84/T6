"""Task 0b pullback with BOTH radii (work order 2026-09-24): per centreline station of every root->outlet path of scan 837 (PILOT_OUT_OF_COHORT), the 3D section quantities of the solved case and the 0D twin's node data.
Columns: case, path (label), path_leaf_node, station, arc_s_mm, x/y/z_mm (station point), section_ok, section_area_mm2, r_eq3D_mm (area-equivalent radius of the 3D section), r0D_edt_mm (0D node radius = mask max-inscribed/EDT radius,
linearly interpolated along the path arc), r0D_fit_mm (robust-taper healthy fit r_fit), r0D_ref_mm (r_ref used by the bed), centroid_offset_over_req (section validity), Q_section_mls (through-plane flux along the path tangent, forward positive),
p3D_over_Pa (area-averaged static pressure of the section / P_aorta), p0D_over_Pa (0D twin pressure at the nearest node), r0D_edt_lesion_mm (lesion80 only: the radius the 0D lesion variant used).
Stations every 1.5 mm from the path start plus the outlet end; the connected section nearest the centreline point only (as pullback_compare.py); a section is ok if its area-weighted centroid lies within 0.5 r_eq of the point and the area is within a factor 0.6..1.6 of the previous ok station of the path (bifurcation sections that catch two vessels fail this).
usage: pullback_radii.py <case_dir_name> <baseline|missedbranch|extcomp|lesion80|baseline_ref> <out.csv> [time]     (default LESION_PROFILE=lesion80)"""
import sys, os, json, csv
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pyvista as pv
from zerod_ffr import RHO, P_AORTA
from outlets_837 import build_tree
from build_solve_cases import drop_branch
import build_lesion80_case as L
from pullback_compare import node_xyz, path_to

BASE = os.path.dirname(os.path.abspath(__file__)); STEP_MM = 1.5

def section(mesh, origin_m, t):
    sl = mesh.slice(normal=t, origin=origin_m)
    if sl.n_cells == 0: return None
    sl = sl.extract_geometry().triangulate().clean()
    part = sl.connectivity(extraction_mode="closest", closest_point=origin_m).compute_cell_sizes(length=False, area=True, volume=False)
    if part.n_cells == 0: return None
    A = part.cell_data["Area"]; p = part.cell_data["p"]; U = part.cell_data["U"]; Atot = float(A.sum())
    ctr = part.cell_centers().points; cen = (ctr * A[:, None]).sum(0) / Atot
    return dict(area=Atot, p=float((p * A).sum() / Atot), Q=float(((U @ t) * A).sum()), cen=cen)

def main(case, mode, out, time=None):
    if mode not in ("baseline", "missedbranch", "extcomp", "lesion80", "baseline_ref"): raise SystemExit(f"unknown mode {mode!r}")
    T = build_tree(); Qd = T.demand("murray")
    if mode == "missedbranch": T, _ = drop_branch(T, "D2")
    C = T.calibrate(Qd)
    r_ov = None
    if mode == "lesion80":
        r_ov, _ = L.lesion_r_override(T); ffr0, _, _, _, _ = T.evaluate(C, r_override=r_ov)
    else:
        ffr0, _, _, _, _ = T.evaluate(C)
    cdir = f"{BASE}/{case}"; open(f"{cdir}/case.foam", "a").close()
    rd = pv.OpenFOAMReader(f"{cdir}/case.foam"); rd.set_active_time_value(float(time) if time else rd.time_values[-1])
    rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh"); mb = rd.read()
    mesh = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
    assert float(rd.active_time_value) > 0, "solved fields not reconstructed"
    print(f"{case}: time {rd.active_time_value}, cells {mesh.n_cells}")
    rows = []
    for leaf in T.leaves:
        lab = str(T.label[leaf]); nodes = path_to(T, int(leaf))
        xyz = np.array([node_xyz(T, n) for n in nodes]); arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(xyz, axis=0), axis=1))])
        st = np.append(np.arange(0, arc[-1], STEP_MM), arc[-1])
        r_edt = np.interp(st, arc, T.r[nodes] * 1e3); r_fit = np.interp(st, arc, T.r_fit[nodes] * 1e3); r_ref = np.interp(st, arc, T.r_ref[nodes] * 1e3)
        r_les = np.interp(st, arc, r_ov[nodes] * 1e3) if r_ov is not None else None
        prev = None
        for k, s in enumerate(st):
            i = min(int(np.searchsorted(arc, s)), len(arc) - 1); j = max(i - 1, 0)
            f = 0 if arc[i] == arc[j] else (s - arc[j]) / (arc[i] - arc[j]); pt = xyz[j] + f * (xyz[i] - xyz[j])
            lo, hi = max(0, i - 3), min(len(xyz) - 1, i + 3); tan = xyz[hi] - xyz[lo]; tan = tan / np.linalg.norm(tan)
            sec = section(mesh, pt * 1e-3, tan)
            row = dict(case=case, path=lab, path_leaf_node=int(leaf), station=k, arc_s_mm=float(s), x_mm=float(pt[0]), y_mm=float(pt[1]), z_mm=float(pt[2]),
                       r0D_edt_mm=float(r_edt[k]), r0D_fit_mm=float(r_fit[k]), r0D_ref_mm=float(r_ref[k]), p0D_over_Pa=float(ffr0[nodes[i]]))
            if r_les is not None: row["r0D_edt_lesion_mm"] = float(r_les[k])
            ok = False
            if sec is not None:
                req = np.sqrt(sec["area"] / np.pi); off = float(np.linalg.norm(sec["cen"] - pt * 1e-3)) / req
                ok = bool(off < 0.5 and (prev is None or 0.6 < sec["area"] / prev < 1.6))
                if ok: prev = sec["area"]
                row.update(section_area_mm2=sec["area"] * 1e6, r_eq3D_mm=req * 1e3, centroid_offset_over_req=off,
                           Q_section_mls=(sec["Q"] * 1e6) if ok else None, p3D_over_Pa=(sec["p"] * RHO / P_AORTA) if ok else None)
            row["section_ok"] = int(ok); rows.append(row)
        print(f"  {lab:4s} leaf {leaf}: {len(st)} stations")
    cols = ["case", "path", "path_leaf_node", "station", "arc_s_mm", "x_mm", "y_mm", "z_mm", "section_ok", "section_area_mm2", "r_eq3D_mm", "r0D_edt_mm", "r0D_fit_mm", "r0D_ref_mm"] + (["r0D_edt_lesion_mm"] if r_ov is not None else []) + \
           ["centroid_offset_over_req", "Q_section_mls", "p3D_over_Pa", "p0D_over_Pa"]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    print("wrote", out, len(rows), "rows")

if __name__ == "__main__":
    if len(sys.argv) < 4: raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
