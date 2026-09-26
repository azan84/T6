"""returns/2026-09-26/M1_geometry_gates.csv (report Table 17 + decisions D2/D3/D4 of work order 2026-09-26): one row per case, from m1/out/<case>/gates.json, m1/mesh/<case>_v2/mesh_gates.json and
m1/out_returns/d34_distances.json (d34_distances.py). Read-only. usage: make_geometry_gates_csv.py <out.csv>"""
import os, sys, json, csv
HERE = os.path.dirname(os.path.abspath(__file__))
CASES = [("clean_nolesion", "clean"), ("baseline", "baseline (80 %DS)"), ("T1_missed_branch", "T1 (missed branch, pilot)")]
def build():
    d34 = json.load(open(f"{HERE}/out_returns/d34_distances.json")); rows = []
    for case, label in CASES:
        g = json.load(open(f"{HERE}/out/{case}/gates.json")); mg = json.load(open(f"{HERE}/mesh/{case}_v2/mesh_gates.json")); d = d34[case]; G = g["GATES"]; les = g.get("lesion") or {}; thr = les.get("throat") or {}
        rel, lit = thr.get("RELATIVE_GATE") or {}, thr.get("LITERAL_ABSOLUTE_vs_r_target") or {}; asb = thr.get("asbuilt_mm") or {}; fs = g["final_surface"]; c = d["checks"]
        worst = min(((k, e) for k, e in c.items() if e["min_dist_to_throat_centre_mm"] is not None), key=lambda t: t[1]["min_dist_to_throat_centre_mm"])
        r = dict(case=case, label=label, package=g["case"], scan=g["scan"], side=g["side"], cohort_status="frozen cohort, in CFD subset (E0 assertion PASSED against CFD-SUBSET-FROZEN-2026-09-18.csv sha256 8e0079a0...)",
                 manual_repair=False, pipeline_gates_frame_check=G["frame_check"], pipeline_gate_mask_edit_matches_shipped=G["mask_edit_matches_shipped_voxels_and_components"], pipeline_gate_clip_loops_outward=G["clip_loops_and_outward_normals"],
                 pipeline_gate_extensions_outward=G["extensions_outward"], pipeline_gate_surface_closed_one_part_positive_volume=G["final_surface_closed_one_part_positive_volume"],
                 D2_relative_throat_gate_pass=G.get("lesion_relative_throat_gate"), relative_dev_insc_pct=rel.get("insc_circle_pct"), relative_dev_area_equiv_pct=rel.get("area_equiv_pct"), relative_dev_axis_sphere_pct=rel.get("sphere_at_axis_pct"), relative_tolerance_pct=rel.get("tolerance_pct"),
                 radial_scale_package=thr.get("radial_scale"), r_target_mm=thr.get("r_target_mm"), r_source_mm=thr.get("r_source_mm"),
                 absolute_check_reported_not_decisive_pass=(G.get("lesion_literal_absolute_r_target_check") if les else None), absolute_dev_insc_pct=lit.get("insc_circle_pct"), absolute_dev_area_equiv_pct=lit.get("area_equiv_pct"), absolute_dev_axis_sphere_pct=lit.get("sphere_at_axis_pct"),
                 asbuilt_r_insc_mm=asb.get("insc_circle"), asbuilt_r_area_equiv_mm=asb.get("area_equiv"), asbuilt_r_axis_sphere_mm=asb.get("sphere_at_axis"),
                 self_intersecting_raw_marching_cubes=d["raw_mc_surface_self_intersecting"], self_intersecting_smoothed=(fs.get("surfaceCheck_smoothed_left_tree_surface") or {}).get("self_intersecting"), self_intersecting_final_surface=(fs.get("surfaceCheck") or {}).get("self_intersecting"),
                 self_intersection_clusters=len(d["self_intersection_clusters"]), self_intersection_clusters_min_dist_to_throat_mm=(min(x["d_throat_mm"] for x in d["self_intersection_clusters"]) if d["self_intersection_clusters"] else None),
                 self_intersection_clusters_min_dist_to_measurement_mm=(min(x["d_measurement_mm"] for x in d["self_intersection_clusters"]) if d["self_intersection_clusters"] else None),
                 cells=mg["cells"], checkMesh_standard_OK=mg["checkMesh_standard_OK"], checkMesh_strict_failed_checks=mg["strict_failed_checks"], strict_failure_lines=" | ".join(mg["strict_failure_lines"]),
                 n_faces_low_quality_face_tets=c["lowQualityTetFaces"]["n_entities_in_log"], n_concave_cells=c["concaveCells"]["n_entities_in_log"], n_faces_small_volume_ratio=c["lowVolRatioFaces"]["n_entities_in_log"],
                 throat_probe=d["throat_probe"], throat_probe_kind_note=("would-be throat station (no lesion in this case)" if case == "clean_nolesion" else "lesion throat"), measurement_probe=d["measurement_probe"],
                 min_dist_flagged_to_throat_centre_mm=d["min_over_checks_throat_centre_mm"], check_of_min_dist_to_throat=worst[0], min_dist_flagged_to_measurement_centre_mm=d["min_over_checks_measurement_centre_mm"])
        for s, short in (("lowQualityTetFaces", "face_tets"), ("concaveCells", "concave_cells"), ("concaveFaces", "concave_faces"), ("lowVolRatioFaces", "small_vol_ratio")):
            r[f"{short}_min_dist_throat_centre_mm"] = c[s]["min_dist_to_throat_centre_mm"]; r[f"{short}_min_dist_throat_disc_mm"] = c[s]["min_dist_to_throat_disc_mm"]
            r[f"{short}_min_dist_measurement_centre_mm"] = c[s]["min_dist_to_measurement_centre_mm"]; r[f"{short}_min_dist_measurement_disc_mm"] = c[s]["min_dist_to_measurement_disc_mm"]
        r.update(checks_within_2mm=" ".join(d["checks_within_2mm"]) or "none", n_face_tet_vertex_points_within_2mm_of_throat=c["lowQualityTetFaces"]["n_points_within_2mm_of_throat"], D3_self_intersection_verdict=d["D3_verdict"], D4_strict_checkMesh_verdict=d["D4_verdict"],
                 distance_basis="vertices of the flagged faces/cells written by checkMesh -writeSets vtk, in mm, package frame; centre = to the probe's centreline point, disc = to the probe's cross-section disc (as-meshed area-equivalent radius)",
                 M1_status_D6=("PASS WITH DEVIATIONS (D2 relative gate decisive; absolute check and D3/D4 conditions as reported)" if (d["D3_verdict"] in ("PASS",) or d["D3_verdict"].startswith("NOT")) and d["D4_verdict"] == "PASS" else "FAILS M1 under D3/D4 (a flagged entity lies within 2 mm of the throat or measurement probe); reported, not repaired"))
        rows.append(r)
    return rows
if __name__ == "__main__":
    rows = build(); out = sys.argv[1]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("wrote", out, len(rows), "rows,", len(rows[0]), "columns")
    for r in rows: print(r["case"], "| D2 relative", r["D2_relative_throat_gate_pass"], "| abs", r["absolute_check_reported_not_decisive_pass"], "| D3", r["D3_self_intersection_verdict"], "| D4", r["D4_strict_checkMesh_verdict"], "| within 2 mm:", r["checks_within_2mm"])
