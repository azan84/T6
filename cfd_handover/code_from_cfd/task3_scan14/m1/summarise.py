import json, sys
for c in ("clean_nolesion","baseline","T1_missed_branch"):
    try: g=json.load(open(f"out/{c}/gates.json"))
    except Exception as e: print(c,"missing",e); continue
    m=g["mask_edit"]; f=g["final_surface"]; t=f["topology"]
    print("=====",c,g["status"], "| total s",g.get("wall_clock_total_s"))
    print(" frame: sub_cut in lumen flip/noflip",g["frame_check"]["sub_cut_points_inside_lumen_with_flip"],g["frame_check"]["sub_cut_points_inside_lumen_without_flip"],"branch",g["frame_check"]["branch_deletion_points_inside_lumen_with_flip"],g["frame_check"]["branch_deletion_points_inside_lumen_without_flip"])
    print(" mask: removed",m["voxels_removed"],"shipped",m["shipped_voxels_removed"],"comps after 6/26",m["components_after"],"erosion(f x r)",m["erosion_removed_voxels_within_f_r"],"shipped erosion",m["erosion_shipped"])
    pr=g["parent_radius_change"]; print(" parent radius (EDT): LAD n_changed",pr["LAD_nodes"]["n_changed"],"max decrease mm",round(pr["LAD_nodes"]["max_decrease_mm"],3),"nodes",[(n["segment"],n["tree_node"],round(n["edt_before_mm"],2),round(n["edt_after_mm"],2)) for n in pr["changed_nodes"]])
    cl=g["clip"]; print(" clip loops",cl["n_loops"],"/",cl["expected_loops"],"PASS",cl["PASS"],"aspects",[round(l["width_max_over_min"],2) for l in cl["loops"]])
    print(" extensions mm",{e["patch"]:round(e["extension_length_mm"],2) for e in g["extensions"]["per_patch"]})
    print(" ext / D_areaeq",{e["patch"]:round(e["extension_length_over_area_equivalent_D"],2) for e in g["extensions"]["per_patch"]})
    if "lesion" in g:
        L=g["lesion"]; T=L["throat"]
        print(" lesion: refine passes",L["refine_passes"],"tri",L["n_triangles_after_refine"],"edge<=h frac",L["edge_le_r_throat_over_8_in_window_fraction"],"max edge",round(L["undeformed_edge_max_over_edges_with_a_moved_endpoint_mm"],4),"h_max",round(L["h_max_mm"],4),"foldover min dot",round(L["fold_over_min_dot"],3),"G1 impure",L["G1_impure_triangles"],"G3",L["G3_label_check"]["fraction_LAD_label"])
        print(" throat node",T["tree_node"],"r_target",round(T["r_target_mm"],4),"asbuilt insc/eq/sphere",{k:round(v,4) for k,v in T["asbuilt_mm"].items()})
        print("   RELATIVE",{k:round(v,3) for k,v in T["RELATIVE_GATE"].items() if k.endswith("pct")},"LITERAL",{k:round(v,2) for k,v in T["LITERAL_ABSOLUTE_vs_r_target"].items() if isinstance(v,float)})
        print("   stations relative max dev",L["stations_relative_dev_max_abs_pct"],"| undeformed sphere vs r_source median/p10/p90",[round(x,1) for x in L["stations_undeformed_sphere_vs_r_source_pct_median_p10_p90"]])
    print(" final: tri",t["n_triangles"],"vol",round(t["volume_mm3"],1),"open",t["open_edges"],"comps",t["connected_components"],"min edge mm",round(t["min_edge_mm"],5),"p1 quality",round(t["p1_quality"],3),"STL MB",f["stl"]["size_mb"])
    print(" surfaceCheck",{k:v for k,v in f.get("surfaceCheck",{}).items() if k!="log"},"poscontrol self-int",f.get("positive_control_surfaceCheck",{}).get("self_intersecting"))
    print(" self-intersection clusters",[(c["segment"],c["nearest_node"],c["n_points"],c["distance_over_r_source"],c["nearest_outlet"],c["distance_to_outlet_mm"]) for c in f.get("self_intersection_clusters",[])], "raw MC self-int",f.get("surfaceCheck_raw_mc_left_tree_surface",{}).get("self_intersecting"))
    print(" GATES failed:",g.get("FAILED_GATES"))
    print(" wall clock s",g["wall_clock_s"])
    print(" radius csv: ok sections",g["surface_radius_csv"]["n_sections_ok"],"/",g["surface_radius_csv"]["n_nodes"],"median r_eq/r_source",round(g["surface_radius_csv"]["median_r_eq_over_pkg_r_source"],3),"median r_insc/r_source",round(g["surface_radius_csv"]["median_r_insc_over_pkg_r_source"],3))
