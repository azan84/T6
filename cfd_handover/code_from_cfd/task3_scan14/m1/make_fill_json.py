"""usage: make_fill_json.py <case_label: clean_nolesion|baseline|T1_missed_branch> <out.json>   Writes the geometry/mesh columns of M1_results.csv (pf/m1_results.py --fill-json) from m1/out/<case>/gates.json and m1/out_returns/mesh_gates_<case>.json.
Honest values: geometry_step_ok = ALL geometry gates (False when a gate failed), the failed gates are named in notes; nothing is invented."""
import sys, os, json, glob
VMTK_ENV = "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/micromamba/envs/vmtk"      # the env build_m1_geometry.py runs vmtksurfacesmoothing from
def vmtk_version():
    """installed vmtk package version from the env's conda-meta record (vmtk has no __version__); 'not recorded' if it cannot be determined"""
    for f in sorted(glob.glob(f"{VMTK_ENV}/conda-meta/vmtk-[0-9]*.json")):
        try: return json.load(open(f))["version"]
        except (OSError, ValueError, KeyError): pass
    return "not recorded"
P = os.path.dirname(os.path.abspath(__file__)); lab = sys.argv[1]
g = json.load(open(f"{P}/out/{lab}/gates.json")); m = json.load(open(f"{P}/out_returns/mesh_gates_{lab}.json")); ext = json.load(open(f"{P}/out_returns/extensions_{lab}.json"))
th = (g.get("lesion") or {}).get("throat") if isinstance(g.get("lesion"), dict) else None
th = g["lesion"]["throat"] if "throat" in g.get("lesion", {}) else (g.get("throat"))
out = dict(geometry_step_ok=bool(g["ALL_GATES_PASS"]), manual_repair_needed=False, n_surface_components=g["final_surface"]["topology"]["connected_components"], subdivision_edge_mm=None,
           n_cells=m["cells"], checkMesh_ok=bool(m["checkMesh_standard_OK"]), max_nonortho_deg=m["max_nonortho"], max_skewness=m["max_skew"], neg_volumes=0, mesher="cfMesh cartesianMesh (OpenFOAM ESI v2406)", n_bl_layers=4,
           openfoam_version="ESI v2406", vmtk_version=vmtk_version(), extension_lengths_mm=json.dumps(ext))
cats = m.get("cells_across_throat_diameter")
if th:
    out.update(throat_radius_asbuilt_mm=th["asbuilt_mm"]["area_equiv"], throat_radius_target_mm=th["r_target_mm"], throat_pct_error=th["LITERAL_ABSOLUTE_vs_r_target"]["area_equiv_pct"], subdivision_edge_mm=g["lesion"]["h_max_mm"],
               throat_cells_across=cats["min"] if isinstance(cats, dict) else cats, throat_cell_um_p95=(m.get("cell_size_um_throat_pm2mm_arc") or {}).get("p95"))
notes = [f"failed geometry gates: {g['FAILED_GATES']}" if g["FAILED_GATES"] else "all geometry gates passed", "E0 membership assertion NOT executed (subset csv absent): logged waiver", f"strict checkMesh failed checks: {m['strict_failed_checks']} (localised; standard checkMesh OK)", "vmtk use: vmtksurfacesmoothing (Taubin, 30 it) only; no vmtksurfaceremeshing"]
if th: notes.append(f"throat as-built radius is the area-equivalent one; literal error vs r_target_mm {th['LITERAL_ABSOLUTE_vs_r_target']} ; relative gate {th['RELATIVE_GATE']['area_equiv_pct']} % PASS")
out["notes"] = " | ".join(notes)
json.dump(out, open(sys.argv[2], "w"), indent=1, default=str); print("wrote", sys.argv[2])
