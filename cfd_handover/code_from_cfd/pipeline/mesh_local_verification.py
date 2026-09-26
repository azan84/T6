"""Local mesh verification along the lesion window (Astra round-2 request): (1) mesh section area vs STL section area at every 0.25 mm station from s=17.5 to 32 mm (contraction + expansion + jet zone);
(2) boundary-layer structure measured by wall-normal rays at 8 azimuths x 8 axial stations: run-lengths of consecutive cells along the inward STL normal, first-cell height, 3-layer stack thickness,
growth ratios, coverage. usage: mesh_local_verification.py <mesh_case_dir> <stl (m)> <tag> """
import sys, os, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pyvista as pv
import build_lesion80_surface as G
from outlets_837 import build_tree

def load_mesh(case):
    open(f"{case}/case.foam", "w").close()
    rd = pv.OpenFOAMReader(f"{case}/case.foam"); rd.disable_all_cell_arrays(); rd.disable_all_point_arrays()
    rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh")
    mb = rd.read(); m = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
    return m

def loop_area(slice_poly, c):
    part = slice_poly.connectivity(extraction_mode="closest", closest_point=c)
    return part

def main(case, stl, tag):
    T = build_tree(); T.ffr(mode="murray"); fr = G.Deformer(T).fr
    mesh = load_mesh(case)
    mesh_mm = mesh.copy(); mesh_mm.points = np.asarray(mesh.points) * 1e3
    surf = pv.read(stl).extract_surface(algorithm="dataset_surface").triangulate(); surf.points = np.asarray(surf.points) * 1e3
    surf = surf.compute_normals(cell_normals=True, point_normals=False, auto_orient_normals=True)
    out = dict(tag=tag, section_area=[], boundary_layer=[])
    # ---- (1) section areas: mesh vs STL. STL area from the closed contour via polygon (shoelace) in the plane
    worst = (0, None); rows = []
    for s in np.arange(G.PR["LOCAL_LO"], G.PR["LOCAL_HI"] + 1e-9, 0.25):
        k = int(np.argmin(np.abs(fr["s"] - s))); c = fr["c"][k]; t = fr["t"][k]
        sm = mesh_mm.slice(normal=t, origin=c).extract_geometry().triangulate().clean()
        pm = sm.connectivity(extraction_mode="closest", closest_point=c).compute_cell_sizes(length=False, area=True, volume=False)
        a_mesh = float(pm.cell_data["Area"].sum())
        ss = surf.slice(normal=t, origin=c).connectivity(extraction_mode="closest", closest_point=c).clean(tolerance=1e-9)
        # order the loop
        from verify_lesion80_geometry import ordered_loop
        pts, closed = ordered_loop(ss)
        a = np.cross(t, [1.0, 0, 0]); a /= np.linalg.norm(a); b = np.cross(t, a)
        x, y = (pts - c) @ a, (pts - c) @ b
        a_stl = 0.5 * abs(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))
        err = 100 * (a_mesh / a_stl - 1)
        rows.append(dict(s=float(s), area_mesh_mm2=a_mesh, area_stl_mm2=float(a_stl), err_pct=float(err), closed=bool(closed)))
        if abs(err) > abs(worst[0]): worst = (err, float(s))
    out["section_area"] = rows
    errs = np.array([r["err_pct"] for r in rows])
    out["section_area_summary"] = dict(n=len(rows), max_abs_err_pct=float(np.abs(errs).max()), s_of_max=worst[1], mean_err_pct=float(errs.mean()),
                                       throat_err_pct=float(min(rows, key=lambda r: abs(r["s"] - G.S_C))["err_pct"]),
                                       n_over_2pct=int((np.abs(errs) > 2).sum()), n_over_5pct=int((np.abs(errs) > 5).sum()))
    print(tag, "section-area mesh vs STL:", json.dumps(out["section_area_summary"]))
    # ---- (2) boundary layers by rays
    import vtk
    loc = vtk.vtkStaticCellLocator(); loc.SetDataSet(mesh_mm); loc.BuildLocator()
    depths = np.arange(0.5, 150.0 + 1e-9, 0.5) * 1e-3          # mm
    for s in [G.S_C if x == "S_C" else x for x in G.PR["BL_STATIONS"]]:
        k = int(np.argmin(np.abs(fr["s"] - s))); c = fr["c"][k]; t = fr["t"][k]
        ss = surf.slice(normal=t, origin=c).connectivity(extraction_mode="closest", closest_point=c).clean(tolerance=1e-9)
        pts = np.asarray(ss.points)
        a = np.cross(t, [1.0, 0, 0]); a /= np.linalg.norm(a); b = np.cross(t, a)
        ang = np.arctan2((pts - c) @ b, (pts - c) @ a)
        for kk in range(8):
            target = -np.pi + (kk + 0.5) * 2 * np.pi / 8
            j = int(np.argmin(np.abs(np.angle(np.exp(1j * (ang - target))))))
            p = pts[j]
            cid = surf.find_closest_cell(p); n = np.asarray(surf.cell_data["Normals"][cid])
            if n @ (c - p) < 0: n = -n
            samp = p[None, :] + depths[:, None] * n[None, :]
            ids = np.array([loc.FindCell([float(x) for x in q]) for q in samp])
            inside = ids >= 0
            if not inside.any():
                out["boundary_layer"].append(dict(s=float(s), az=kk, ok=False)); continue
            first = int(np.argmax(inside)); ids = ids[first:]
            runs = []; cur = ids[0]; n0 = 0
            for v in ids:
                if v == cur: n0 += 1
                else: runs.append((cur, n0 * 0.5)); cur = v; n0 = 1
            runs.append((cur, n0 * 0.5))
            th = [r[1] for r in runs if r[0] >= 0][:6]
            out["boundary_layer"].append(dict(s=float(s), az=kk, ok=True, wall_offset_um=float(depths[first] * 1e3), runs_um=th))
    bl = [r for r in out["boundary_layer"] if r["ok"]]
    def lay(r):
        th = r["runs_um"]
        return len(th) >= 4 and th[0] < 12 and th[0] < th[1] < th[2] and th[3] > th[2]
    cov = np.mean([lay(r) for r in bl])
    out["bl_summary"] = dict(n_rays=len(out["boundary_layer"]), n_ok=len(bl), coverage_3layer_increasing=float(cov),
                              first_cell_um_median=float(np.median([r["runs_um"][0] for r in bl])), first_cell_um_max=float(np.max([r["runs_um"][0] for r in bl])),
                              stack3_um_median=float(np.median([sum(r["runs_um"][:3]) for r in bl])),
                              stack3_um_min=float(np.min([sum(r["runs_um"][:3]) for r in bl])), stack3_um_max=float(np.max([sum(r["runs_um"][:3]) for r in bl])))
    print(tag, "boundary layers:", json.dumps(out["bl_summary"]))
    json.dump(out, open(f"{case}/local_verification_{tag}.json", "w"), indent=1)
    by_s = {}
    for r in bl: by_s.setdefault(r["s"], []).append(r["runs_um"])
    for s, v in by_s.items():
        m0 = np.median([x[0] for x in v]); m3 = np.median([sum(x[:3]) for x in v]); nn = np.mean([len(x) >= 4 and x[0] < x[1] < x[2] for x in v])
        print(f"  s={s:5.2f}: first cell {m0:5.1f} um, 3-layer stack {m3:5.1f} um, monotone-3-layer fraction {nn:.2f}")

if __name__ == "__main__":
    main(*sys.argv[1:4])
