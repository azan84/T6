"""M1_probes_<case>_<mode>.csv (work order Task 3 return): area-averaged p AND through-plane flux at EVERY probe of the package's probes.csv, from the reconstructed final fields.
usage: m1_probes.py <case_dir> <package_dir_name> <case_label> <mode> [--time T] [--pkg-root R] [--out file.csv]     (default time = the latest reconstructed time; default out = M1_probes_<case_label>_<mode>.csv in cwd)
Section = the connected section nearest the probe point, cut with the probe's own normal (probes.csv normal_x/y/z; package normals follow the downstream direction, outlets outward), cell-data p (kinematic, x rho -> Pa) and U (p and flux only for a VALID section: centroid within 0.5 r_eq of the probe point; the invalid section's area/r_eq/offset are still given);
Q_through_mls = sum over the section of (U . n) A, SIGNED along the probe normal (mL/s); Q_abs_mls = sum |U . n| A (differs when the section has reversed flow); p_mean_Pa = area-weighted mean static p. Columns also give the
package's probe_id/kind/s/s_from_lesion, section validity (centroid offset over r_eq < 0.5), area, r_eq, section Reynolds number 4 rho |Q|/(pi mu D) with D = 2 r_eq, and the time used. Inlet/outlet probes lie at the
package's inlet/outlet planes (the mesh's inlet/outlet faces are further out by the flow extensions). No 0D quantity is used or written.
When the case's build_info.json records a RELOCATED measurement probe (strict single-lumen section rule, Task C probe_sections.py), one extra row kind 'measurement_relocated' (probe_id <orig>_reloc, s_mm = package s_mm +
the arc shift) is added for the section the measurementP monitor samples; the package's 'measurement' row stays (the returns state which probe was used: M1_results notes)."""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import json
import m1_package as M
import sections as S
RHO, MU, P_AORTA_PA = 1060.0, 0.004, 11998.98

def relocated_rows(case, pkg):
    """the RELOCATED measurement probe of the case (build_info measurement_probe_relocated, written by build_m1_case when the package probe failed the strict single-lumen section rule) as an extra probes row,
    kind 'measurement_relocated' (the section measurementP monitors); [] when the package probe was used. The package's own 'measurement' row is always kept (same method, its section_ok says whether it is valid)."""
    f = os.path.join(case, "build_info.json")
    rel = json.load(open(f)).get("measurement_probe_relocated") if os.path.exists(f) else None
    if not rel: return []
    r, o = rel["relocated"], rel["original"]; orow = [p for p in pkg["probes"] if p["probe_id"] == o["probe_id"]][0]
    ds = float(r["arc_from_original_mm"])
    sf = lambda k: (float(orow[k]) + ds) if orow.get(k) not in (None, "") else ""
    return [dict(probe_id=r["probe_id"], kind="measurement_relocated", tree_node=str(r["tree_node"]), s_mm=sf("s_mm"), s_from_lesion_mm=sf("s_from_lesion_mm"), x=r["point_mm"][0], y=r["point_mm"][1], z=r["point_mm"][2],
                 normal_x=r["normal"][0], normal_y=r["normal"][1], normal_z=r["normal"][2], r_ref_mm=r["r_ref_mm"], resolved=orow.get("resolved", ""))]

def main(case, name, label, mode, time=None, pkg_root=None, out=None):
    pkg = M.load_package(name, pkg_root); mesh, t = S.load_internal_mesh(case, time, fields=True); sec = S.Sectioner(mesh); rows = []
    for pr in list(pkg["probes"]) + relocated_rows(case, pkg):
        pt = np.array([float(pr["x"]), float(pr["y"]), float(pr["z"])]) * 1e-3; n = np.array([float(pr["normal_x"]), float(pr["normal_y"]), float(pr["normal_z"])])
        s = sec.section(pt, n, max(float(pr["r_ref_mm"]), 0.3) * 1e-3)
        row = dict(case=label, mode=mode, probe_id=pr["probe_id"], kind=pr["kind"], tree_node=pr["tree_node"], s_mm=pr["s_mm"], s_from_lesion_mm=pr["s_from_lesion_mm"], x_mm=pr["x"], y_mm=pr["y"], z_mm=pr["z"], resolved=pr["resolved"], time=t, section_ok=0)
        if s is not None:
            D = 2 * s["r_eq"]
            row.update(section_ok=int(s["section_ok"]), section_area_mm2=s["area"] * 1e6, r_eq_mm=s["r_eq"] * 1e3, centroid_offset_over_req=s["centroid_offset_over_req"])
            if s["section_ok"]:      # p and flux are reported only for a valid section (the nearest section of an off-lumen or bifurcation station is not the probe's vessel)
                row.update(p_mean_Pa=s["p_mean"] * RHO, p_over_Paorta=s["p_mean"] * RHO / P_AORTA_PA, Q_through_mls=s["Q"] * 1e6, Q_abs_mls=s["Q_abs"] * 1e6, Re_section=4 * RHO * abs(s["Q"]) / (np.pi * MU * D))
        rows.append(row)
    cols = ["case", "mode", "probe_id", "kind", "tree_node", "s_mm", "s_from_lesion_mm", "x_mm", "y_mm", "z_mm", "resolved", "time", "section_ok", "section_area_mm2", "r_eq_mm", "centroid_offset_over_req", "p_mean_Pa", "p_over_Paorta", "Q_through_mls", "Q_abs_mls", "Re_section"]
    out = out or f"M1_probes_{label}_{mode}.csv"
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    print(f"wrote {out}: {len(rows)} probes, {sum(r['section_ok'] for r in rows)} valid sections, time {t}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 4: raise SystemExit(__doc__)
    g = lambda f: a[a.index(f) + 1] if f in a else None
    main(a[0], a[1], a[2], a[3], g("--time"), g("--pkg-root"), g("--out"))
