"""Decisions D3/D4 of work order 2026-09-26: for every case, the counts per strict-checkMesh check (from log.checkMesh.strict) and the distance from the nearest flagged entity to the throat probe and to the
measurement probe, from the sets written by `checkMesh -allGeometry -allTopology -writeSets vtk` (postProcessing/constant/<set>/<set>.vtp; the vtp holds the VERTICES of the flagged faces/cells, in metres).
Two distances per probe, both reported: to the probe's centreline point ("centre") and to the probe's cross-section disc (centre, normal, as-meshed area-equivalent radius; a point inside the disc's cylinder-of-influence counts |axial|).
Verdict rule (D3/D4): a case FAILS if any flagged entity lies < 2 mm (centre distance, the literal reading) from the throat probe or the measurement probe; the disc distance is reported beside it.
The self-intersection clusters of the raw marching-cubes surface (gates.json) are localised the same way (D3 first condition: the intersection is present in the RAW marching-cubes surface).
usage: d34_distances.py [out.json]   (reads P/m1/mesh/<case>_v2, P/m1/out/<case>/gates.json, the packages under P/m1/pkg, returns as_meshed_radius files; no solver, read-only)"""
import os, sys, re, json, csv
import numpy as np, pyvista as pv
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = {"baseline": "14_left_LAD_prox_20mm_80ds__baseline__real", "T1_missed_branch": "14_left_LAD_prox_20mm_80ds__T1_missed_branch__real", "clean_nolesion": "14_left_LAD_prox_20mm_80ds__clean_nolesion__real"}
SETS = ["concaveCells", "concaveFaces", "lowQualityTetFaces", "lowVolRatioFaces"]
LOGLINE = {"lowQualityTetFaces": r"Error in face tets: (\d+) faces", "concaveCells": r"Concave cells \(using face planes\) found, number of cells: (\d+)", "lowVolRatioFaces": r"small volume ratio \(< 0\.01\) found, number of faces: (\d+)"}
LIMIT_MM = 2.0

def probe(pk, kind):
    r = [r for r in csv.DictReader(open(f"{pk}/probes.csv")) if r["kind"] == kind][0]
    return dict(id=r["probe_id"], node=int(r["tree_node"]), c=np.array([float(r[k]) for k in ("x", "y", "z")]), n=np.array([float(r[k]) for k in ("normal_x", "normal_y", "normal_z")]), s_mm=float(r["s_mm"]))

def as_meshed_r(case, node):
    f = f"/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24/as_meshed_radius_{case}.csv"      # section radius at the node (area-equivalent); the node's section is valid or not (section_ok)
    for r in csv.DictReader(open(f)):
        if int(r["node"]) == node: return float(r["r_eq3D_mm"]) if r["r_eq3D_mm"] not in ("", "nan") else None, r["section_ok"] == "1"
    return None, False

def dist_disc(pts, pr, r):
    n = pr["n"] / np.linalg.norm(pr["n"]); d = pts - pr["c"]; ax = d @ n; rad = np.linalg.norm(d - np.outer(ax, n), axis=1)
    return np.where(rad <= r, np.abs(ax), np.sqrt(ax ** 2 + (rad - r) ** 2))

def case_report(case):
    md = f"{HERE}/mesh/{case}_v2"; pk = f"{HERE}/pkg/{PKG[case]}"; g = json.load(open(f"{HERE}/out/{case}/gates.json"))
    thr, mea = probe(pk, "throat"), probe(pk, "measurement")
    rt, okt = as_meshed_r(case, thr["node"]); rm, okm = as_meshed_r(case, mea["node"])
    log = open(f"{md}/log.checkMesh.strict").read(); out = dict(case=case, throat_probe=thr["id"], throat_node=thr["node"], throat_xyz_mm=thr["c"].tolist(), measurement_probe=mea["id"], measurement_node=mea["node"], measurement_xyz_mm=mea["c"].tolist(),
                                                              throat_section_radius_mm=rt, measurement_section_radius_mm=rm, checks={})
    for s in SETS:
        f = f"{md}/postProcessing/constant/{s}/{s}.vtp"
        pts = np.asarray(pv.read(f).points) * 1e3 if os.path.exists(f) else np.zeros((0, 3))
        m = re.search(LOGLINE[s], log) if s in LOGLINE else None
        e = dict(n_entities_in_log=int(m.group(1)) if m else None, n_vertex_points=int(len(pts)))
        if len(pts):
            dt_c = np.linalg.norm(pts - thr["c"], axis=1); dm_c = np.linalg.norm(pts - mea["c"], axis=1)
            dt_d = dist_disc(pts, thr, rt if rt else 0.0); dm_d = dist_disc(pts, mea, rm if rm else 0.0)
            e.update(min_dist_to_throat_centre_mm=float(dt_c.min()), min_dist_to_throat_disc_mm=float(dt_d.min()), min_dist_to_measurement_centre_mm=float(dm_c.min()), min_dist_to_measurement_disc_mm=float(dm_d.min()),
                     n_points_within_2mm_of_throat=int((dt_c < LIMIT_MM).sum()), n_points_within_2mm_of_measurement=int((dm_c < LIMIT_MM).sum()))
        else: e.update(min_dist_to_throat_centre_mm=None, min_dist_to_throat_disc_mm=None, min_dist_to_measurement_centre_mm=None, min_dist_to_measurement_disc_mm=None, n_points_within_2mm_of_throat=0, n_points_within_2mm_of_measurement=0)
        out["checks"][s] = e
    fs = [c for c in g["final_surface"].get("self_intersection_clusters", [])]
    cl = []
    for c in fs:
        p = np.array(c["centroid_mm"]); cl.append(dict(n_points=c["n_points"], nearest_node=c.get("nearest_node"), segment=c.get("segment"), d_throat_mm=float(np.linalg.norm(p - thr["c"])), d_measurement_mm=float(np.linalg.norm(p - mea["c"]))))
    out["self_intersection_clusters"] = cl
    out["raw_mc_surface_self_intersecting"] = bool(g["final_surface"].get("surfaceCheck_raw_mc_left_tree_surface", {}).get("self_intersecting"))
    near = {s: e for s, e in out["checks"].items() if (e["min_dist_to_throat_centre_mm"] is not None and e["min_dist_to_throat_centre_mm"] < LIMIT_MM) or (e["min_dist_to_measurement_centre_mm"] is not None and e["min_dist_to_measurement_centre_mm"] < LIMIT_MM)}
    out["checks_within_2mm"] = sorted(near); out["D4_verdict"] = "FAIL" if near else "PASS"
    out["D3_verdict"] = ("FAIL" if near else "PASS") if out["raw_mc_surface_self_intersecting"] else "NOT_APPLICABLE (no self-intersection in the raw surface)"
    out["min_over_checks_throat_centre_mm"] = min((e["min_dist_to_throat_centre_mm"] for e in out["checks"].values() if e["min_dist_to_throat_centre_mm"] is not None), default=None)
    out["min_over_checks_measurement_centre_mm"] = min((e["min_dist_to_measurement_centre_mm"] for e in out["checks"].values() if e["min_dist_to_measurement_centre_mm"] is not None), default=None)
    return out

if __name__ == "__main__":
    res = {c: case_report(c) for c in PKG}
    dst = sys.argv[1] if len(sys.argv) > 1 else f"{HERE}/out_returns/d34_distances.json"
    json.dump(res, open(dst, "w"), indent=1); print("wrote", dst)
    for c, r in res.items():
        print(c, "D4", r["D4_verdict"], "D3", r["D3_verdict"], "| checks < 2 mm:", r["checks_within_2mm"], "| min throat/measurement centre mm:", r["min_over_checks_throat_centre_mm"], r["min_over_checks_measurement_centre_mm"])
        for s, e in r["checks"].items(): print("   ", s, e["n_entities_in_log"], e["n_vertex_points"], "thr", e["min_dist_to_throat_centre_mm"], e["min_dist_to_throat_disc_mm"], "meas", e["min_dist_to_measurement_centre_mm"], e["min_dist_to_measurement_disc_mm"])
