"""cfMesh a level of the U3D sten70 family (u3d_design.md section 3) and gate the MEASURED mesh.
usage: make_sten70_mesh.py <level S50|S25A|S12A|S25B|S12B> <outdir>      (outdir under P/u3d/, must not exist)
Straight axis along x (metres). Lesion zone x in [11.5, 51.5] mm at 50 um for every level; throat zone A [29, 34] mm or B [30, 35] mm at 25 um (S25*) or 12.5 um (S12*).
cfMesh cell-size requests (metres, 5 decimals): <=70 um realises 50 um, <=40 um realises 25 um, <=20 um realises 12.5 um (lesion80 findings); maxCellSize 0.0002; 4 boundary layers ratio 1.2.
Gates: cartesianMesh finished; standard checkMesh OK; strict checkMesh failed-set count recorded and the flagged sets localised against the throat zone; cells across the throat DIAMETER measured
along 8 azimuthal lines at x = 31.5 mm (median/min; required >= 12); p95 cell size in |x-31.5| < 2 mm; throat-plane mesh area vs the STL polygon area (< 1 %); boundary-layer stack (first 4 cells from the wall) at the throat."""
import sys, os, re, shutil, subprocess, json
import numpy as np, pyvista as pv
U = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(U)
STL = f"{U}/sten70_fine.stl"; TEMPLATE = f"{P}/../A5_sten70_fine"
X_T = 31.5e-3 + 3e-6; R_T = 0.4455e-3      # throat plane sampled 3 um downstream of the throat centre: 31.5 mm is a cell-face plane of every level (multiple of 12.5 um), which would make FindCell/slices ambiguous
ZONES = {"A": (29.0e-3, 34.0e-3), "B": (30.0e-3, 35.0e-3)}
REQ = {50: 0.00007, 25: 0.00004, 12: 0.00002}                   # metres, see docstring

def level_spec(level):
    m = re.fullmatch(r"S(50|25|12)([AB]?)", level)
    if not m: raise SystemExit(f"unknown level {level!r}")
    size, z = int(m.group(1)), m.group(2)
    if size != 50 and not z: raise SystemExit("S25/S12 need a zone letter A or B")
    if size == 50 and z: raise SystemExit("S50 has no throat zone")
    return size, z

def meshdict(level):
    size, z = level_spec(level)
    objs = [f"    lesionZone {{ type cone; cellSize {REQ[50]:.5f}; p0 (0.0115 0 0); radius0 0.003; p1 (0.0515 0 0); radius1 0.003; }}\n"]
    if size != 50:
        a, b = ZONES[z]; objs.append(f"    throatZone  {{ type cone; cellSize {REQ[size]:.5f}; p0 ({a:.4f} 0 0); radius0 0.003; p1 ({b:.4f} 0 0); radius1 0.003; }}\n")
    return ("FoamFile { version 2.0; format ascii; class dictionary; object meshDict; }\nsurfaceFile \"constant/triSurface/case.stl\";\nmaxCellSize 0.00020;\n"
            "boundaryLayers { nLayers 4; thicknessRatio 1.2; }\nobjectRefinements\n{\n" + "".join(objs) + "}\n")

def measure(outdir):
    open(f"{outdir}/case.foam", "w").close()
    rd = pv.OpenFOAMReader(f"{outdir}/case.foam"); rd.disable_all_cell_arrays(); rd.disable_all_point_arrays(); rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh")
    mb = rd.read(); m = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
    m = m.compute_cell_sizes(length=False, area=False, volume=True); vol = m.cell_data["Volume"]; h = np.cbrt(vol); cc = np.asarray(m.cell_centers().points)
    import vtk
    loc = vtk.vtkStaticCellLocator(); loc.SetDataSet(m); loc.BuildLocator()
    res = {}
    # cells across the throat diameter along 8 azimuths: a fine sampling of the diameter, counting runs of consecutive equal cell ids (each run = one cell crossed)
    counts = []
    for k in range(8):
        th = np.pi * k / 8; d = np.array([0.0, np.cos(th), np.sin(th)]); last = None; n = 0
        for t in np.arange(-R_T + 0.5e-6, R_T - 0.5e-6, 0.5e-6):
            cid = loc.FindCell((np.array([X_T, 0, 0]) + t * d).tolist())
            if cid >= 0 and cid != last: n += 1
            last = cid
        counts.append(n)
    res["cells_across_throat_diameter"] = dict(per_azimuth=counts, median=float(np.median(counts)), min=int(min(counts)), method="runs of equal cell ids along 8 diameters at x = 31.5 mm, 0.5 um sampling")
    sel = (np.abs(cc[:, 0] - X_T) < 2e-3)
    res["cell_size_um_x31.5_pm2mm"] = dict(n=int(sel.sum()), median=float(np.median(h[sel]) * 1e6), p95=float(np.percentile(h[sel], 95) * 1e6), min=float(h[sel].min() * 1e6))
    sl = m.slice(normal=(1, 0, 0), origin=(X_T, 0, 0)).compute_cell_sizes(length=False, area=True, volume=False)
    a_mesh = float(sl.cell_data["Area"].sum()); a_stl = 0.5 * 192 * R_T ** 2 * np.sin(2 * np.pi / 192)
    res["throat_area"] = dict(mesh_mm2=a_mesh * 1e6, stl_polygon_mm2=a_stl * 1e6, err_pct=100 * (a_mesh / a_stl - 1))
    # boundary-layer stack: 8 radial lines from the wall inward, runs of equal cell ids
    stacks = []
    for k in range(8):
        th = 2 * np.pi * k / 8; d = np.array([0.0, np.cos(th), np.sin(th)]); runs = []; last = None; cur = 0.0
        for depth in np.arange(0.25e-6, 150e-6, 0.25e-6):
            pnt = np.array([X_T, 0, 0]) + (R_T - depth) * d; cid = loc.FindCell(pnt.tolist())
            if cid == last: cur += 0.25e-6
            else:
                if last is not None: runs.append(cur)
                last, cur = cid, 0.25e-6
        runs.append(cur); stacks.append(runs[:4])
    st = np.array([s + [np.nan] * (4 - len(s)) for s in stacks]) * 1e6
    res["boundary_layer_um"] = dict(first_cell_median=float(np.nanmedian(st[:, 0])), first4_stack_median=float(np.nanmedian(np.nansum(st, 1))), per_layer_median=[float(np.nanmedian(st[:, j])) for j in range(4)])
    res["cells_total_check"] = int(m.n_cells); res["mesh_volume_mm3"] = float(vol.sum() * 1e9)
    return res

def main(level, outdir):
    if os.path.exists(outdir): raise SystemExit(f"{outdir} exists")
    os.makedirs(f"{outdir}/constant/triSurface"); os.symlink(STL, f"{outdir}/constant/triSurface/case.stl")     # symlink: 163 MB STL is shared by all levels
    shutil.copytree(f"{TEMPLATE}/system", f"{outdir}/system");
    for f in ("transportProperties", "turbulenceProperties"): shutil.copy(f"{TEMPLATE}/constant/{f}", f"{outdir}/constant/{f}")
    open(f"{outdir}/system/meshDict", "w").write(meshdict(level))
    env = "source /usr/lib/openfoam/openfoam2406/etc/bashrc; cd " + outdir + "; "
    subprocess.run(["bash", "-c", env + "cartesianMesh > log.cartesianMesh 2>&1; checkMesh > log.checkMesh.standard 2>&1; checkMesh -allGeometry -allTopology -writeSets vtk > log.checkMesh.strict 2>&1"], check=True)
    lc = open(f"{outdir}/log.cartesianMesh").read(); std = open(f"{outdir}/log.checkMesh.standard").read(); strict = open(f"{outdir}/log.checkMesh.strict").read()
    g = dict(level=level, zone=level_spec(level)[1] or None, cartesianMesh_finished=("End" in lc), checkMesh_standard_OK=("Mesh OK" in std))
    m = re.search(r"cells:\s+(\d+)", strict); g["cells"] = int(m.group(1)) if m else None
    g["strict_failed_checks"] = int(re.search(r"Failed (\d+) mesh checks", strict).group(1)) if "Failed" in strict else 0
    for k, pat in (("max_nonortho", r"Mesh non-orthogonality Max: ([\d.]+)"), ("max_skew", r"Max skewness = ([\d.]+)")):
        mm = re.search(pat, strict); g[k] = float(mm.group(1)) if mm else None
    bt = open(f"{outdir}/constant/polyMesh/boundary").read(); g["patch_faces"] = {n: int(f) for n, f in re.findall(r"(\w+)\s*\{[^}]*?nFaces\s+(\d+);", bt)}
    g.update(measure(outdir))
    import glob
    fl = {}
    for f in sorted(glob.glob(f"{outdir}/postProcessing/constant/*/*.vtp")):
        pts = np.asarray(pv.read(f).points) * 1e3; x = pts[:, 0]; z = g["zone"]
        za = ZONES[z] if z else (31.5e-3 - 2.5e-3, 31.5e-3 + 2.5e-3)
        fl[os.path.basename(f)[:-4]] = dict(n_points=int(len(x)), x_min_mm=float(x.min()), x_max_mm=float(x.max()),
                                            n_in_throat_zone_pm2mm=int(((x >= za[0] * 1e3 - 2) & (x <= za[1] * 1e3 + 2)).sum()), n_in_lesion_zone=int(((x >= 11.5) & (x <= 51.5)).sum()))
    g["flagged_sets"] = fl
    if g["strict_failed_checks"] > 0 and not fl: raise SystemExit("strict checkMesh failed but no failed-set VTK found: an empty search is not a pass")
    ok = g["cartesianMesh_finished"] and g["checkMesh_standard_OK"] and all(v > 0 for v in g["patch_faces"].values()) and g["cells_across_throat_diameter"]["min"] >= 12 and abs(g["throat_area"]["err_pct"]) < 1.0
    g["GATES_PASS"] = bool(ok); json.dump(g, open(f"{outdir}/mesh_gates.json", "w"), indent=1); print(json.dumps(g, indent=1))
    if not ok: raise SystemExit("mesh gates failed: see mesh_gates.json (the mesh is NOT to be used)")

if __name__ == "__main__":
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
