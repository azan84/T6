"""Analytic check of flow_state_profile.py on synthetic straight tubes (no solver): a structured hexahedral tube of radius R with the axial velocity u = U0 (1 + a (g . r_perp) / R), g a unit vector normal to the axis.
For a disc section the flux-weighted centroid of u sits at (a R / 4) g from the area centroid, so offset/r_eq = a/4 along g (r_eq = R); in the profile's (N, B) frame o = (a/4) (g.N, g.B).
Cases: (1) tube along x through the straight-x interface (sten70 path), a = 0.4, g at 30 deg in the y-z plane; (2) the same tube rotated to an oblique axis, through the polyline (package-style) interface;
(3) a = 0 (axisymmetric: offset 0); then COMPARE: identical profiles AGREE, a = 0.4 vs a = 0 DIFFER (0.1 > 0.03), a = 0.4 vs a = 0.32 AGREE (0.02 <= 0.03), and the FFR criterion;
(4) attempt 3 (audit round 2, Sol finding 2): the statistic is the max over the FULL profile: one invalid station (either side), a missing (deleted) station, or an extra unmatched station makes the comparison
STATES INDETERMINATE (also with --ffr, also when the subset max is above the tolerance), never AGREE on a subset; the subset max is reported as information only.
usage: python3 test_flow_state_profile.py"""
import os, sys, tempfile, shutil, json
HERE = os.path.dirname(os.path.abspath(__file__)); TC = os.path.dirname(HERE)
sys.path[:0] = [f"{TC}/pf", TC]
import numpy as np, pyvista as pv
import flow_state_profile as F

R_MM, L_MM, A_GRAD = 1.0, 12.0, 0.4

def tube(direction, a, phi_deg, n_r=40, n_t=96, n_z=121):
    d = np.asarray(direction, float); d /= np.linalg.norm(d)
    g0 = F.least_aligned_axis(d); g1 = np.cross(d, g0); ph = np.radians(phi_deg); g = np.cos(ph) * g0 + np.sin(ph) * g1
    radii = np.linspace(0.0, R_MM * 1e-3, n_r)       # from the axis: the innermost ring is degenerate hexahedra (wedges); a hole on the axis would fail the one-boundary-loop rule
    sg = pv.CylinderStructured(radius=radii, height=L_MM * 1e-3, center=d * L_MM * 1e-3 / 2, direction=d, theta_resolution=n_t, z_resolution=n_z)
    m = sg.cast_to_unstructured_grid(); c = np.asarray(m.cell_centers().points)
    rp = c - np.outer(c @ d, d); u = 0.5 * (1 + a * (rp @ g) / (R_MM * 1e-3))
    m.cell_data["U"] = np.outer(u, d); m.cell_data["p"] = np.zeros(m.n_cells)
    return m, d, g

def run(direction, a, phi, straight):
    m, d, g = tube(direction, a, phi)
    if straight: X, arc, rr, s_t, s_m, _ = F.straight_path(2.0, 10.0, 0.0, 0.0, r_ref=R_MM)
    else:
        X = np.outer(np.linspace(0, L_MM, 121), d); arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]; rr = np.full(len(X), R_MM); s_t, s_m = 2.0, 10.0
    rows = F.profile_mesh(m, X, arc, rr, s_t, s_m, label=f"a{a}")
    return rows, g

def check(rows, g, a, tol_rel=0.015, tol_abs=2e-3):
    assert len(rows) == 7 and [round(r["s_from_throat_mm"], 6) for r in rows] == [2, 3, 4, 5, 6, 7, 8], [r["s_from_throat_mm"] for r in rows]
    for r in rows:
        assert r["section_ok"] == 1, r
        N = np.array([r["N_x"], r["N_y"], r["N_z"]]); T = np.array([r["t_x"], r["t_y"], r["t_z"]]); B = np.cross(T, N)
        exp = (a / 4) * np.array([g @ N, g @ B]); got = np.array([r["oN"], r["oB"]])
        assert np.linalg.norm(got - exp) <= max(tol_rel * a / 4, tol_abs), (r["station"], got, exp)
        assert abs(r["r_eq_mm"] - R_MM) < 0.005, r["r_eq_mm"]
    return max(np.hypot(r["oN"], r["oB"]) for r in rows)

def main():
    tmp = tempfile.mkdtemp(prefix="fsp_test_"); out = {}
    try:
        r1, g1 = run((1, 0, 0), A_GRAD, 30, True); out["x_tube_a0.4_phi30"] = check(r1, g1, A_GRAD)
        assert abs(r1[0]["N_y"] - 1) < 1e-12 and abs(np.degrees(np.arctan2(r1[0]["oB"], r1[0]["oN"])) - 30) < 1.0       # straight x tube: N = y, B = z; imposed direction 30 deg
        r2, g2 = run((1, 2, 0.5), A_GRAD, 75, False); out["oblique_tube_a0.4_phi75"] = check(r2, g2, A_GRAD)
        r3, g3 = run((1, 0, 0), 0.0, 0, True); out["x_tube_a0"] = check(r3, g3, 0.0)
        r4, _ = run((1, 0, 0), 0.32, 30, True)
        for k, rows in (("a04", r1), ("a0", r3), ("a032", r4)): F.write_rows(rows, f"{tmp}/{k}.csv")
        c_same = F.compare(f"{tmp}/a04.csv", f"{tmp}/a04.csv"); c_diff = F.compare(f"{tmp}/a04.csv", f"{tmp}/a0.csv"); c_near = F.compare(f"{tmp}/a04.csv", f"{tmp}/a032.csv")
        c_ffr = F.compare(f"{tmp}/a04.csv", f"{tmp}/a032.csv", (0.8700, 0.8710))
        assert c_same["verdict"].startswith("STATES AGREE") and c_same["max_vector_diff_offset_over_req"] < 1e-12
        assert c_diff["verdict"].startswith("STATES DIFFER") and abs(c_diff["max_vector_diff_offset_over_req"] - 0.1) < 0.002, c_diff["max_vector_diff_offset_over_req"]
        assert c_near["verdict"].startswith("STATES AGREE") and abs(c_near["max_vector_diff_offset_over_req"] - 0.02) < 0.001, c_near["max_vector_diff_offset_over_req"]
        assert c_ffr["verdict"] == "STATES DIFFER" and c_ffr["profile_criterion"] == "AGREE" and c_ffr["ffr_criterion"] == "DIFFER"
        import csv as _csv
        def edit(src, dst, fn):
            rows = list(_csv.DictReader(open(src))); rows = fn(rows)
            with open(dst, "w", newline="") as fh: w = _csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
        def invalid(i):
            def f(rows): rows[i]["section_ok"] = "0"; return rows
            return f
        edit(f"{tmp}/a04.csv", f"{tmp}/a04_inv3.csv", invalid(3)); edit(f"{tmp}/a0.csv", f"{tmp}/a0_inv0.csv", invalid(0))
        edit(f"{tmp}/a04.csv", f"{tmp}/a04_drop.csv", lambda rows: rows[:2] + rows[3:])
        edit(f"{tmp}/a04.csv", f"{tmp}/a04_extra.csv", lambda rows: rows + [dict(rows[-1], s_from_throat_mm="8.5", s_to_measurement_mm="-0.5")])
        c_inv = F.compare(f"{tmp}/a04.csv", f"{tmp}/a04_inv3.csv"); c_inv_ffr = F.compare(f"{tmp}/a04_inv3.csv", f"{tmp}/a04.csv", (0.8700, 0.8701))
        c_inv_diff = F.compare(f"{tmp}/a04.csv", f"{tmp}/a0_inv0.csv"); c_drop = F.compare(f"{tmp}/a04_drop.csv", f"{tmp}/a04.csv"); c_extra = F.compare(f"{tmp}/a04.csv", f"{tmp}/a04_extra.csv")
        for c in (c_inv, c_inv_ffr, c_inv_diff, c_drop, c_extra):
            assert c["verdict"].startswith("STATES INDETERMINATE") and c["profile_criterion"] == "INDETERMINATE" and not c["complete_profile"] and c["max_vector_diff_offset_over_req"] is None, c["verdict"]
        assert [e["s_from_throat_mm"] for e in c_inv["stations_excluded_invalid"]] == [5.0] and c_inv["stations_excluded_invalid"][0]["invalid_in"] == ["B"] and c_inv["subset_max_vector_diff_INFORMATION_ONLY"] < 1e-12
        assert c_inv_ffr["ffr_criterion"] == "AGREE" and c_inv_ffr["verdict"] == "STATES INDETERMINATE"
        assert c_inv_diff["subset_max_exceeds_tol"] and abs(c_inv_diff["subset_max_vector_diff_INFORMATION_ONLY"] - 0.1) < 0.002     # subset above tol: still INDETERMINATE (no replacement rule)
        assert c_drop["stations_missing"] == {"A": [4.0]} and c_drop["stations_unmatched"] == [4.0], (c_drop["stations_missing"], c_drop["stations_unmatched"])
        assert c_extra["stations_unmatched"] == [8.5] and c_extra["stations_not_specified"] == {"B": [8.5]}, c_extra["stations_not_specified"]
        out.update(compare_same=c_same["max_vector_diff_offset_over_req"], compare_a04_vs_a0=c_diff["max_vector_diff_offset_over_req"], compare_a04_vs_a032=c_near["max_vector_diff_offset_over_req"])
        print(json.dumps({k: round(v, 5) for k, v in out.items()}))
        print(f"PASS: analytic offset/r_eq = a/4 = {A_GRAD / 4} reproduced (x tube and oblique tube, frame-independent), axisymmetric 0, compare AGREE/DIFFER as designed; invalid/missing/unmatched stations -> STATES INDETERMINATE (never AGREE on a subset)")
    finally: shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
