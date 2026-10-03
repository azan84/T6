"""Scan-14 regression: every numerical / boolean leaf of the reference m1/out/baseline/gates.json vs the generalised builder's p5/out/14_regression/gates.json (keys renamed LAD -> lesion_path mapped back).
Wall-clock, paths, hashes of scripts and timestamps are excluded (they differ by construction). usage: compare_regression.py REF NEW OUT.json"""
import json, sys, math
REN = {"window_vertices_within_2p6mm_not_assigned_to_lesion_path": "window_vertices_within_2p6mm_not_assigned_to_LAD_path", "lesion_path_wall_max_radial_distance_mm": "LAD_wall_max_radial_distance_mm",
       "gap_other_branch_minus_lesion_path_wall_mm": "gap_other_branch_minus_LAD_wall_mm", "G1_max_displacement_non_lesion_path_original_vertices_mm": "G1_max_displacement_non_LAD_original_vertices_mm",
       "vessel_label": "LAD_label", "vessel_label_fractions_at_vessel_nodes": "LAD_label_fractions_at_LAD_nodes", "fraction_vessel_label": "fraction_LAD_label", "lesion_vessel_nodes": "LAD_nodes",
       "removed_voxels_within_r_of_a_lesion_vessel_node_mm": "removed_voxels_within_r_of_a_LAD_node_mm"}
SKIP = ("wall_clock", "script", "lib_sha256", "started", "log", "path", "package_sha256", "sha256", "status", "deviations", "e0", "stl", "mask_sha256_check", "method", "note", "rule", "case", "blinding")
def flat(d, p=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            k2 = REN.get(k, k)
            out.update(flat(v, f"{p}/{k2}"))
    elif isinstance(d, list):
        for i, v in enumerate(d): out.update(flat(v, f"{p}[{i}]"))
    elif isinstance(d, (int, float, bool)) or d is None: out[p] = d
    return out
ref, new = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
fr, fn = flat(ref), flat(new)
skip = lambda k: any(s in k.lower() for s in SKIP)
common = [k for k in fr if k in fn and not skip(k)]
diff = [dict(key=k, ref=fr[k], new=fn[k]) for k in common if not (fr[k] == fn[k] or (isinstance(fr[k], float) and isinstance(fn[k], float) and math.isclose(fr[k], fn[k], rel_tol=0, abs_tol=0)))]
only_ref = [k for k in fr if k not in fn and not skip(k)]; only_new = [k for k in fn if k not in fr and not skip(k)]
rep = dict(n_compared=len(common), n_different=len(diff), differences=diff, only_in_reference=only_ref, only_in_new=only_new[:200], n_only_in_new=len(only_new), GATES_ref=ref.get("GATES"), GATES_new=new.get("GATES"))
json.dump(rep, open(sys.argv[3], "w"), indent=1); print(json.dumps({k: rep[k] for k in ("n_compared", "n_different", "only_in_reference", "n_only_in_new")}, indent=1)); print("first differences:", diff[:15])
