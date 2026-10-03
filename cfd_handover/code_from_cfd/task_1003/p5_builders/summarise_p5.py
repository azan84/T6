"""Collects p5/out/<scan>/gates.json, p5/mesh/<scan>/{mesh_gates.json,d34.json} and runs.log into p5/P5_summary.json (+ markdown tables printed for P5_BUILD_REPORT.md). Read-only.
D10 (audit P5 Sol finding 2): all_gates_pass_decisive (= ALL_GATES_PASS of the fixed builder; the literal absolute r_target check excluded) and all_gates_pass_including_reported are both reported; an older gates.json
(no GATES_DECISIVE) is split here the same way. Staging copy (taskP5/p5/): reads the pilot's p5/out, p5/mesh and runs.log, writes P5_summary.json next to this script."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = HERE
if not os.path.isdir(f"{HERE}/out"): HERE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "p5")      # staging copy: inputs from the pilot's p5/
REPORTED_NON_DECISIVE_GATES = ("lesion_literal_absolute_r_target_check",)
CASES = sys.argv[1:] or ["14_regression", "138", "69", "473", "272", "139"]
runs = open(f"{HERE}/runs.log").read() if os.path.exists(f"{HERE}/runs.log") else ""
def j(p):
    try: return json.load(open(p))
    except Exception: return None
S = {}
for c in CASES:
    g = j(f"{HERE}/out/{c}/gates.json"); m = j(f"{HERE}/mesh/{c}/mesh_gates.json"); d = j(f"{HERE}/mesh/{c}/d34.json"); d = d[list(d)[0]] if d else None
    if g is None: S[c] = dict(missing=True); continue
    L = g.get("lesion", {}); th = L.get("throat", {}); fs = g["final_surface"]; rg = th.get("RELATIVE_GATE", {}); ab = th.get("LITERAL_ABSOLUTE_vs_r_target", {})
    gs = g.get("GATES") or {}; dec = g.get("GATES_DECISIVE") or {k: v for k, v in gs.items() if k not in REPORTED_NON_DECISIVE_GATES}
    r = dict(case=g["case"], scan=g["scan"], side=g["side"], vessel=g["vessel"], L_mm=L.get("lesion_length_mm"), ds_pct=L.get("ds_pct"), status=g["status"], failed_gates=[k for k, v in dec.items() if not v],
             failed_gates_including_reported=[k for k, v in gs.items() if not v], all_gates_pass_decisive=bool(dec) and all(dec.values()), all_gates_pass_including_reported=bool(gs) and all(gs.values()),
             throat_node=th.get("tree_node"), r_target_mm=th.get("r_target_mm"), radial_scale=th.get("radial_scale"), h_max_mm=L.get("h_max_mm"), lesion_outlet=L.get("throat_selection", {}).get("lesion_outlet"),
             throat_selection=L.get("throat_selection"),
             rel_gate_pct=[rg.get("insc_circle_pct"), rg.get("area_equiv_pct"), rg.get("sphere_at_axis_pct")], rel_PASS=th.get("PASS"),
             abs_pct=[ab.get("insc_circle_pct"), ab.get("area_equiv_pct"), ab.get("sphere_at_axis_pct")], abs_PASS=th.get("LITERAL_ABSOLUTE_PASS"),
             asbuilt_mm=th.get("asbuilt_mm"), purity_fold_window_PASS=L.get("PASS_purity_fold_window"), fold_min_dot=L.get("fold_over_min_dot"), G3=L.get("G3_label_check", {}).get("fraction_vessel_label"),
             frame=[g["frame_check"]["all_deletion_points_inside_with_flip"], g["frame_check"]["sub_cut_points_inside_lumen_without_flip"]], frame_stated=g["frame_check"].get("package_stated"),
             voxels_removed=g["mask_edit"]["voxels_removed"], components_before_after=[g["mask_edit"]["components_before"]["6"], g["mask_edit"]["components_after"]["6"]], erosion_f=g["mask_edit"]["erosion_removed_voxels_within_f_r"],
             clip_loops=[g["clip"]["n_loops"], g["clip"]["expected_loops"]], tri=fs["topology"]["n_triangles"], vol_mm3=fs["topology"]["volume_mm3"],
             final_self_intersecting=fs.get("surfaceCheck", {}).get("self_intersecting"), si_clusters=fs.get("self_intersection_clusters"), raw_mc_self_intersecting=fs.get("surfaceCheck_raw_mc_left_tree_surface", {}).get("self_intersecting"),
             smoothed_self_intersecting=fs.get("surfaceCheck_smoothed_left_tree_surface", {}).get("self_intersecting"), poscontrol=fs.get("positive_control_surfaceCheck", {}).get("self_intersecting"),
             extensions={e["patch"]: dict(L_mm=round(e["extension_length_mm"], 3), D_mm=round(e["D_used_mm"], 3), mult=e["D_multiple"], loop_Deq_mm=round(e["loop_area_equivalent_diameter_mm"], 3)) for e in g["extensions"]["per_patch"]},
             geometry_wall_s=g["wall_clock_total_s"])
    mm = re.findall(rf"(\S+) {re.escape(c)} (\w+) rc=(\d+) (?:total )?(\d+) s", runs); r["runs_log"] = mm
    if m:
        r.update(cells=m.get("cells"), strict_failed=m.get("strict_failed_checks"), strict_lines=m.get("strict_failure_lines"), std_OK=m.get("checkMesh_standard_OK"), patches=m.get("patch_faces"), patches_ok=m.get("patches_expected_present_nonzero"),
                 cells_across=(m.get("cells_across_throat_diameter") or {}), throat_area_err_pct=m.get("throat_plane_area_err_pct"), p95_throat_um=(m.get("cell_size_um_throat_pm2mm_arc") or {}).get("p95"), BL=m.get("boundary_layer_um"),
                 mesh_GATES_PASS=m.get("GATES_PASS"), rss_gb=m.get("cartesianMesh_peak_rss_gb"), cartesian_elapsed=m.get("cartesianMesh_elapsed"), mesh_wall_s=m.get("wall_clock_mesh_s"), mesh_total_s=m.get("total_wall_incl_gates_s"),
                 max_nonortho=m.get("max_nonortho"), max_skew=m.get("max_skew"), max_aspect=m.get("max_aspect"), lesion_outlet_mesh=m.get("lesion_outlet"), d1_chain=m.get("d1_chain_outlet"), measure_error=m.get("measure_error"),
                 flagged=m.get("flagged_sets_localised"))
    if d: r.update(D4=d["D4_verdict"], D3=d["D3_verdict"], d34_min_throat_mm=d["min_over_checks_throat_centre_mm"], d34_min_meas_mm=d["min_over_checks_measurement_centre_mm"], d34_checks={k: dict(n=v["n_entities_in_log"], thr=v["min_dist_to_throat_centre_mm"], meas=v["min_dist_to_measurement_centre_mm"], thr_disc=v["min_dist_to_throat_disc_mm"], meas_disc=v["min_dist_to_measurement_disc_mm"]) for k, v in d["checks"].items()}, d34_within_2mm=d["checks_within_2mm"])
    S[c] = r
json.dump(S, open(f"{OUT}/P5_summary.json", "w"), indent=1, default=str)
f = lambda x, n=2: "n/a" if x is None else (f"{x:+.{n}f}" if isinstance(x, float) else str(x))
for c, r in S.items():
    if r.get("missing"): print(c, "MISSING"); continue
    print(f"| {c} | {r['vessel']} {r['L_mm']:.0f} mm {r['ds_pct']:.0f}% | node {r['throat_node']}, r_t {r['r_target_mm']:.4f} | rel {', '.join(f(x, 3) for x in r['rel_gate_pct'])} {'PASS' if r['rel_PASS'] else 'FAIL'} | abs {', '.join(f(x, 1) for x in r['abs_pct'])} {'PASS' if r['abs_PASS'] else 'FAIL'} | final SI {r['final_self_intersecting']} ({len(r['si_clusters'] or [])} cl), raw {r['raw_mc_self_intersecting']} | cells {r.get('cells')} | across {r.get('cells_across', {}).get('min')}/{r.get('cells_across', {}).get('median')} | strict {r.get('strict_failed')} | decisive gates {'PASS' if r['all_gates_pass_decisive'] else 'FAIL ' + ','.join(r['failed_gates'])} (incl. reported {'PASS' if r['all_gates_pass_including_reported'] else 'FAIL'}) | D3 {r.get('D3')} D4 {r.get('D4')} thr {f(r.get('d34_min_throat_mm'))} meas {f(r.get('d34_min_meas_mm'))} |")
