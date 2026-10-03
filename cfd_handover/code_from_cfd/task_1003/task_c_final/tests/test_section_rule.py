"""Strict measurement-section rule (probe_sections.py S1-S4 + relocation; audit 2026-10-03 Sol finding 2). No solver.
A. Centreline only (all five P5 packages + scan-14 baseline): the package measurement probe passes S1/S2 except P5 473 (p011: normal 36.6 deg from the tangent, bifurcation node 424 at -0.84 mm < 1.5 r_ref = 1.30 mm),
   which must be FAILED_SECTION_RULE and relocated deterministically to the nearest node of the same path that passes (the rejected candidates are listed); no original monitor without a mesh.
B. On the real scan-14 baseline mesh (m1/mesh/baseline_v2, 3.66 M cells, read only): (1) the package probe p011 passes S1-S4 on the mesh (area / pi r_ref^2 inside [0.625, 1.6]); (2) a COPY of the package
   (temp dir; the package files are not modified) whose measurement probe is moved to the first node distal of the LAD bifurcation node 116 with the normal tilted 25 deg must fail (S1 and S2), keep the original
   bounded plane only if it passes the mesh check, and be relocated to a mesh-checked node <= 3 mm away; the relocated section passes S4. usage: python3 test_section_rule.py [--no-mesh]"""
import os, sys, json, shutil, tempfile, csv
HERE = os.path.dirname(os.path.abspath(__file__)); TC = os.path.dirname(HERE); PILOT = os.path.dirname(TC)
sys.path[:0] = [f"{TC}/pf"]
import numpy as np
import m1_package as M
import probe_sections as S
P5 = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/P5"; S14 = "14_left_LAD_prox_20mm_80ds__baseline__real"

def part_a():
    out = {}
    for name in sorted(os.listdir(P5)) + [S14]:
        pkg = M.load_package(name, P5 if not name.startswith("14_") else None)
        e = S.probe_planes(pkg, None)["measurement"]; sr = e["section_rule"]; sc = sr["S1_S2_centreline"]
        out[name[:3].rstrip("_")] = dict(probe=sr["probe_id"], status=sr["status"], angle_deg=round(sc["angle_deg"], 1), nearest_non_degree2=sc["nearest_non_degree2_node"], used=e["probe_id"],
                                         relocated=(None if "relocation" not in e else dict(tree_node=e["relocation"]["relocated"]["tree_node"], arc_mm=round(e["relocation"]["relocated"]["arc_from_original_mm"], 3),
                                                                                         rejected=[(c["tree_node"], round(c["arc_from_probe_mm"], 2), c["fails"][:60]) for c in e["relocation"]["candidates_rejected_before"]])))
    for k, v in out.items():
        if k == "473":
            assert v["status"] == "FAILED_SECTION_RULE" and v["used"] == "p011_reloc" and v["relocated"]["tree_node"] == 646 and abs(v["relocated"]["arc_mm"] - 2.853) < 1e-3, v
        else: assert v["status"] == "PASS" and v["used"] == v["probe"], (k, v)
        print(k, json.dumps(v, default=str))
    print("A PASS: S1/S2 pass for 138, 139, 272, 69 and scan 14; 473 FAILED_SECTION_RULE -> relocated to tree_node 646 (+2.853 mm), deterministic")

def moved_package(tmp):
    """copy of the scan-14 package with the measurement probe moved to the first node distal of bifurcation node 116 on the LAD path, normal tilted 25 deg"""
    pkg = M.load_package(S14); d = f"{tmp}/{S14}"; shutil.copytree(pkg["dir"], d)
    cl = pkg["centreline"]; tn = np.asarray(cl.point_data["tree_node"]); path, arc, _ = S.vessel_path(cl, M.point_of_tree_node(cl, 175))
    m = [j for j, p in enumerate(path) if tn[p] == 116][0] + 1; node = int(tn[path[m]]); X = np.asarray(cl.points)[path]
    t = S.path_tangent(X, arc, arc[m]); a = np.cross(t, [0, 0, 1.0]); a /= np.linalg.norm(a); ang = np.radians(25); nrm = np.cos(ang) * t + np.sin(ang) * a
    rows = list(csv.DictReader(open(f"{d}/probes.csv"))); cols = list(rows[0])
    for r in rows:
        if r["kind"] == "measurement": r.update(tree_node=str(node), x=repr(float(X[m][0])), y=repr(float(X[m][1])), z=repr(float(X[m][2])), normal_x=repr(float(nrm[0])), normal_y=repr(float(nrm[1])), normal_z=repr(float(nrm[2])),
                                                r_ref_mm=repr(float(np.asarray(cl.point_data["r_ref_mm"])[path[m]])))
    os.chmod(d, 0o755); [os.chmod(os.path.join(d, f), 0o644) for f in os.listdir(d)]
    with open(f"{d}/probes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    meta = json.load(open(f"{d}/meta.json")); meta["measurement"]["tree_node"] = node; json.dump(meta, open(f"{d}/meta.json", "w"), indent=1)
    return d, node

def part_b():
    poly = f"{PILOT}/m1/mesh/baseline_v2/constant/polyMesh"; checker = S.MeshChecker(S.load_mesh(poly)); print(f"mesh {poly}: {checker.mesh.n_cells} cells")
    e = S.probe_planes(M.load_package(S14), None, kinds=("measurement",), checker=checker)["measurement"]; sr = e["section_rule"]
    assert sr["status"] == "PASS" and sr["S4_area"]["ok"] and sr["S3_mesh_check_ok"], sr
    print(f"B1 PASS: scan-14 p011 on the mesh: angle {sr['S1_S2_centreline']['angle_deg']:.1f} deg, area {e['mesh_check']['bounded_section_area_mm2']:.5f} mm2 = {sr['S4_area']['area_over_pi_r_ref2']:.3f} x pi r_ref^2, one component")
    tmp = tempfile.mkdtemp(prefix="secrule_")
    try:
        d, node = moved_package(tmp); pkg = M.load_package(d)
        o = S.probe_planes(pkg, None, kinds=("measurement",), checker=checker); e = o["measurement"]; rel = e["relocation"]; sr = e["section_rule"]
        assert sr["status"] == "FAILED_SECTION_RULE" and not sr["S1_S2_centreline"]["ok_angle"] and not sr["S1_S2_centreline"]["ok_bifurcation"], sr["why_not_ok"]
        r = rel["relocated"]; assert abs(r["arc_from_original_mm"]) <= 3.0 and r["S4_area"]["ok"] and r["mesh_checked"] and e["status"].startswith("RELOCATED") and e["mesh_check"]["ok"]
        orig = "measurement_orig" in o
        assert (rel["original"]["original_monitor"] is not None) == orig
        print(f"B2 PASS: moved probe (tree_node {node}, 25 deg tilt) FAILED_SECTION_RULE {sr['why_not_ok']}; relocated to tree_node {r['tree_node']} ({r['arc_from_original_mm']:+.3f} mm), "
              f"area {e['mesh_check']['bounded_section_area_mm2']:.5f} mm2 = {r['S4_area']['area_over_pi_r_ref2']:.3f} x pi r_ref^2; candidates rejected before: {[(c['tree_node'], round(c['arc_from_probe_mm'], 2), c['fails'][:50]) for c in rel['candidates_rejected_before']]}; "
              f"original bounded plane {'kept as measurementOrigP' if orig else 'not valid on the mesh: no original monitor (' + str(rel['original']['original_monitor_note']) + ')'}")
    finally: shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    part_a()
    if "--no-mesh" not in sys.argv: part_b()
    print("PASS")
