"""as_meshed_radius_<case>.csv (work order Task 3 return): for EVERY node of the package centreline.vtp (same node ids = the tree_node array), the section of the MESHED lumen (internalMesh cells of the volume mesh, not the surface)
perpendicular to the local centreline tangent: 3D area-equivalent radius r_eq = sqrt(A/pi), MAX-INSCRIBED (EDT-equivalent) radius of the same section, section area. Send it even if the solve fails: needs only the mesh.
usage: as_meshed_radius.py <mesh_or_case_dir> <package_dir_name> <case_label> <out.csv> [--pkg-root R] [--contract PREFIX]      (mesh-only dirs need constant/polyMesh; case.foam is created if missing)
--contract PREFIX: also the two M1 contract files of the 09-26 return (make_returns_0926.py; read by code/ingest_cfd_radius.py: tree_node and r_asmeshed_mm, blank = uncovered): PREFIX.csv (r_asmeshed_mm = area-equivalent
radius) and PREFIX_inscribed.csv (r_asmeshed_mm = maximum-inscribed radius), columns tree_node, s_mm, r_asmeshed_mm, r_area_equiv_mm, r_max_inscribed_mm, section_area_mm2, covered (covered = section_ok; radii blank
when not covered, no interpolation); <out.csv> is then the detail table (returned as *_detail.csv).
Columns: case, node (tree_node id), point_index, segment_name, branch_id, arc_s_mm (path length from the root along the centreline), x_mm, y_mm, z_mm, section_ok, section_area_mm2, r_eq3D_mm, r_maxinscribed_mm,
centroid_offset_over_req, r_centreline_MIS_mm / r_target_mm / r_ref_mm (the package's own radii, for comparison). Tangent: from the parent to the next point of the same branch (else the last edge); at a bifurcation node the
section may catch two vessels and then fails section_ok (centroid > 0.5 r_eq from the point), exactly as in pullback_radii. Max-inscribed radius: rasterised EDT of the planar section, accuracy about 2 % (sections.py). Frame mm/LPS = the mesh frame (metres x 1e3)."""
import sys, os, csv, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import m1_package as M
import sections as S

def main(mesh_dir, name, label, out, pkg_root=None, contract=None):
    pkg = M.load_package(name, pkg_root); cl = pkg["centreline"]; par, ch = M.graph(cl); xyz = np.asarray(cl.points)
    pd_ = {k: np.asarray(cl.point_data[k]) for k in ("tree_node", "branch_id", "segment_name", "MaximumInscribedSphereRadius", "r_target_mm", "r_ref_mm", "r_source_mm")}
    arc = np.zeros(cl.n_points)
    for i in range(1, cl.n_points): arc[i] = arc[par[i]] + np.linalg.norm(xyz[i] - xyz[par[i]])      # parents have lower index
    mesh, t = S.load_internal_mesh(mesh_dir, fields=False); sec = S.Sectioner(mesh); print(f"{label}: mesh {mesh.n_cells} cells, {cl.n_points} centreline nodes")
    rows = []; t0 = time.time()
    for i in range(cl.n_points):
        same = [c for c in ch.get(i, []) if pd_["branch_id"][c] == pd_["branch_id"][i]] or ch.get(i, [])
        a, b = (par.get(i, i), same[0] if same else i)
        if a == b: a = par[i]
        tvec = xyz[b] - xyz[a]; tvec = tvec / np.linalg.norm(tvec)
        rh = max(pd_["r_ref_mm"][i], pd_["MaximumInscribedSphereRadius"][i], pd_["r_source_mm"][i]) * 1e-3
        s = sec.section(xyz[i] * 1e-3, tvec, rh, need_fields=False)
        row = dict(case=label, node=int(pd_["tree_node"][i]), point_index=i, segment_name=str(pd_["segment_name"][i]), branch_id=int(pd_["branch_id"][i]), arc_s_mm=float(arc[i]), x_mm=float(xyz[i][0]), y_mm=float(xyz[i][1]), z_mm=float(xyz[i][2]),
                   r_centreline_MIS_mm=float(pd_["MaximumInscribedSphereRadius"][i]), r_target_mm=float(pd_["r_target_mm"][i]), r_ref_mm=float(pd_["r_ref_mm"][i]), section_ok=0)
        if s is not None:
            ri, h = S.max_inscribed_radius(s["surface"], s["normal"])
            row.update(section_ok=int(s["section_ok"]), section_area_mm2=s["area"] * 1e6, r_eq3D_mm=s["r_eq"] * 1e3, r_maxinscribed_mm=ri * 1e3, centroid_offset_over_req=s["centroid_offset_over_req"])
        rows.append(row)
        if i % 100 == 0: print(f"  {i}/{cl.n_points} ({time.time() - t0:.0f} s)", flush=True)
    cols = ["case", "node", "point_index", "segment_name", "branch_id", "arc_s_mm", "x_mm", "y_mm", "z_mm", "section_ok", "section_area_mm2", "r_eq3D_mm", "r_maxinscribed_mm", "centroid_offset_over_req", "r_centreline_MIS_mm", "r_target_mm", "r_ref_mm"]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    print(f"wrote {out}: {len(rows)} nodes, {sum(r['section_ok'] for r in rows)} valid sections")
    if contract: write_contract(rows, contract)

CONTRACT_COLS = ["tree_node", "s_mm", "r_asmeshed_mm", "r_area_equiv_mm", "r_max_inscribed_mm", "section_area_mm2", "covered"]

def write_contract(rows, prefix):
    """PREFIX.csv (area-equivalent) and PREFIX_inscribed.csv: the contract format of returns/2026-09-26/as_meshed_radius_<case>{,_inscribed}.csv, same rule as make_returns_0926.py"""
    ok = lambda r, k: r["section_ok"] == 1 and k in r and r[k] == r[k] and r["r_eq3D_mm"] == r["r_eq3D_mm"]       # x == x: not NaN
    for suffix, key in (("", "r_eq3D_mm"), ("_inscribed", "r_maxinscribed_mm")):
        out = []
        for r in rows:
            c = ok(r, key) and ok(r, "r_eq3D_mm")
            out.append(dict(tree_node=r["node"], s_mm=r["arc_s_mm"], r_asmeshed_mm=r[key] if c else "", r_area_equiv_mm=r["r_eq3D_mm"] if c else "", r_max_inscribed_mm=r.get("r_maxinscribed_mm", "") if c else "",
                            section_area_mm2=r["section_area_mm2"] if c else "", covered=1 if c else 0))
        with open(f"{prefix}{suffix}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=CONTRACT_COLS); w.writeheader(); w.writerows(out)
        print(f"wrote {prefix}{suffix}.csv: {sum(o['covered'] for o in out)}/{len(out)} covered")

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 4: raise SystemExit(__doc__)
    main(a[0], a[1], a[2], a[3], a[a.index("--pkg-root") + 1] if "--pkg-root" in a else None, a[a.index("--contract") + 1] if "--contract" in a else None)
