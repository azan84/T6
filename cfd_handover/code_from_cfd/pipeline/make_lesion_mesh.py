"""cfMesh a case with lesion-region refinement that FOLLOWS the smoothed LAD centreline (chained short cylinders) and the
proximal D1 (jet-impingement junction), identical for the lesion80 surface and for the baseline surface (so the lesion effect
is not confounded by mesh differences). Gates on the MEASURED mesh, not the dictionary.

usage: make_lesion_mesh.py <stl (m)> <outdir> [--lesion]     (--lesion enables the throat-area-vs-STL gate)
"""
import sys, os, re, shutil, subprocess, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pyvista as pv
from scipy.spatial import cKDTree
import build_lesion80_surface as G
from outlets_837 import build_tree
from lesion_profile import PR

BASE = G.BASE
FINE, COARSE = 0.00007, 0.00010            # metres (cfMesh quantises to powers of two of maxCellSize: 0.07 -> ~0.05, 0.10 -> 0.10)
ZONE_LO, ZONE_HI, ZONE_REQ, ALL_REQ = None, None, None, None   # sensitivity variants: cell-size request (m) for the LAD cylinders whose MID-arc lies in [ZONE_LO, ZONE_HI] (mm); ALL_REQ overrides every cylinder. Defaults = the audited lesion80 mesh.
TUBE_START = None                          # --tube-start=<arc mm>: start of the LAD refinement chain (default: the profile's TUBE_START)
TUBE_END = None                            # --tube-end=<arc mm>: end of the LAD refinement chain (default 36.0 = the audited M50 mesh)
R_CYL = 0.0030                             # cylinder radius (m): covers the lumen (max wall distance 2.33 mm) plus margin
SEG = 0.0015                               # chain step (m)

def cones():
    T = build_tree(); T.ffr(mode="murray"); dfm = G.Deformer(T); fr = dfm.fr
    out = []
    def chain(P, name, size_fn):
        # resample polyline P (mm) every SEG
        d = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
        q = np.arange(0, d[-1], SEG * 1e3)
        Q = np.stack([np.interp(q, d, P[:, k]) for k in range(3)], 1) * 1e-3
        for i in range(len(Q) - 1):
            out.append((f"{name}_{i}", Q[i], Q[i + 1], size_fn(q[i])))
    s0, s1 = (PR["TUBE_START"] if TUBE_START is None else TUBE_START), (PR["TUBE_END"] if TUBE_END is None else TUBE_END)
    k = (fr["s"] >= s0) & (fr["s"] <= s1)
    Pl = fr["c"][k]; sl = fr["s"][k]
    def lad_size(a):
        if ALL_REQ is not None: return ALL_REQ
        if ZONE_LO is not None and ZONE_LO <= sl[0] + a + 0.5 * SEG * 1e3 <= ZONE_HI: return ZONE_REQ     # a = cylinder START arc; mid-arc = start + half a segment
        return FINE if abs(sl[0] + a - G.S_C) < 6.5 else COARSE
    chain(Pl, "lad", lad_size)
    if PR["D1_CHAIN"]:      # the proximal-LAD lesion's jet impinges on the D1 ostium; the isolated lesion has no such junction
        d1 = [sg for sg in T.segments if sg.label == "D1"][0]
        Pd = d1.pts * 1e3
        dd = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Pd, axis=0), axis=1))])
        chain(Pd[dd <= 12.0], "d1", lambda a: ALL_REQ if ALL_REQ is not None else COARSE)
    return out, fr

def main(stl, outdir, lesion):
    if os.path.exists(outdir): shutil.rmtree(outdir)
    os.makedirs(outdir + "/constant/triSurface")
    src = f"{BASE}/opus_debug/CF_baseline_fixedsurf"
    shutil.copytree(src + "/system", outdir + "/system")
    for f in ("transportProperties", "turbulenceProperties"): shutil.copy(f"{src}/constant/{f}", outdir + "/constant/")
    shutil.copy(stl, outdir + "/constant/triSurface/case.stl")
    cs, fr = cones()
    md = open(outdir + "/system/meshDict").read()
    body = "".join(f"    {n:10s} {{ type cone; cellSize {sz:.5f}; p0 ({p0[0]:.6f} {p0[1]:.6f} {p0[2]:.6f}); radius0 {R_CYL}; "
                   f"p1 ({p1[0]:.6f} {p1[1]:.6f} {p1[2]:.6f}); radius1 {R_CYL}; }}\n" for n, p0, p1, sz in cs)
    i = md.rindex("}")
    open(outdir + "/system/meshDict", "w").write(md[:i] + body + "}\n")
    print(f"{len(cs)} refinement cylinders")
    env = "source /usr/lib/openfoam/openfoam2406/etc/bashrc; cd " + outdir + "; "
    subprocess.run(["bash", "-c", env + "cartesianMesh > log.cartesianMesh 2>&1; checkMesh > log.checkMesh.standard 2>&1; checkMesh -allGeometry -allTopology -writeSets vtk > log.checkMesh 2>&1; cp log.checkMesh log.checkMesh.strict"], check=True)
    lc = open(outdir + "/log.cartesianMesh").read(); ck = open(outdir + "/log.checkMesh").read()
    gates = {}
    gates["cartesianMesh_finished"] = "End" in lc
    gates["checkMesh_standard_OK"] = "Mesh OK" in open(outdir + "/log.checkMesh.standard").read()
    gates["strict_failed_checks"] = int(re.search(r"Failed (\d+) mesh checks", ck).group(1)) if "Failed" in ck else 0
    assert gates["checkMesh_standard_OK"], "standard checkMesh failed"
    m = re.search(r"cells:\s+(\d+)", ck); gates["cells"] = int(m.group(1))
    m = re.search(r"Mesh non-orthogonality Max: ([\d.]+)", ck); gates["max_nonortho"] = float(m.group(1))
    m = re.search(r"Max skewness = ([\d.]+)", ck); gates["max_skew"] = float(m.group(1))
    bad = re.findall(r"(?i)(number of bad faces is|inverted boundary faces?[^\n]*)", lc)
    gates["mesher_bad_face_lines"] = re.findall(r"[^\n]*(?:bad faces|nverted)[^\n]*", lc)[-3:]
    # patches
    bt = open(outdir + "/constant/polyMesh/boundary").read()
    gates["patch_faces"] = {n: int(f) for n, f in re.findall(r"(\w+)\s*\{[^}]*?nFaces\s+(\d+);", bt)}
    assert all(v > 0 for v in gates["patch_faces"].values()), gates["patch_faces"]
    # measured cell size along the refined path + throat section vs STL
    open(outdir + "/case.foam", "w").close()
    rd = pv.OpenFOAMReader(outdir + "/case.foam"); rd.disable_all_cell_arrays(); rd.disable_all_point_arrays()
    rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh")
    mb = rd.read(); m = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
    m = m.compute_cell_sizes(length=False, area=False, volume=True)
    cc = np.asarray(m.cell_centers().points); vol = m.cell_data["Volume"]; h = np.cbrt(vol)
    c_path = fr["c"] * 1e-3; s = fr["s"]
    tree = cKDTree(c_path); d, j = tree.query(cc)
    sel = d < 1.2e-3
    cell_size = {}
    for lab, lo, hi in (("throat_pm2mm", G.S_C - 2, G.S_C + 2), ("fine_zone", G.S_C - 6, G.S_C + 6), ("jet_zone_to_D1", G.S_C + 6, PR["JET_END"])):
        k = sel & (s[j] >= lo) & (s[j] <= hi)
        cell_size[lab] = dict(n=int(k.sum()), median_um=float(np.median(h[k]) * 1e6), p95_um=float(np.percentile(h[k], 95) * 1e6))
    gates["cell_size_along_axis_um"] = cell_size
    if VARIANT is None:
        assert cell_size["throat_pm2mm"]["p95_um"] < 80 and cell_size["jet_zone_to_D1"]["p95_um"] < 130, cell_size
    if lesion:
        info = json.load(open(f"{BASE}/{PR['DIR']}/" + PR["OPEN"].replace(".vtp", "_info.json")))
        c = np.array(info["throat_xyz_mm"]) * 1e-3; t = np.array(info["throat_axis"])
        sl = m.slice(normal=t, origin=c).connectivity(extraction_mode="closest", closest_point=c).compute_cell_sizes(length=False, area=True, volume=False)
        a_mesh = float(np.sum(sl.cell_data["Area"])) * 1e6
        gates["throat_area_mesh_mm2"] = a_mesh; gates["throat_area_stl_mm2"] = info["r_throat_mm"] ** 2 * np.pi
        gates["throat_area_err_pct"] = 100 * (a_mesh / gates["throat_area_stl_mm2"] - 1)
        if VARIANT is None:
            assert abs(gates["throat_area_err_pct"]) < 2.0, gates      # sensitivity variants RECORD the throat-area error (it is part of the discretisation error being measured)
    gates["mesh_volume_mm3"] = float(vol.sum() * 1e9)
    json.dump(gates, open(outdir + "/mesh_gates.json", "w"), indent=1)
    print(json.dumps(gates, indent=1))

VARIANT = None
if __name__ == "__main__":
    for a in sys.argv[3:]:
        if a.startswith("--zone="):        # --zone=<arc_lo mm>:<arc_hi mm>:<request m>  e.g. --zone=20.5:26.5:0.000035
            lo, hi, r = a[7:].split(":"); ZONE_LO, ZONE_HI, ZONE_REQ, VARIANT = float(lo), float(hi), float(r), a
        if a.startswith("--tube-start="):
            TUBE_START = float(a[len("--tube-start="):])
        if a.startswith("--tube-end="):    # --tube-end=<arc_end mm>  e.g. --tube-end=42 (extends the chained 50 um LAD cylinders; production gates stay active)
            TUBE_END = float(a[len("--tube-end="):])
        if a.startswith("--all="):         # --all=<request m>  e.g. --all=0.14
            ALL_REQ, VARIANT = float(a[6:]), a
    main(sys.argv[1], sys.argv[2], "--lesion" in sys.argv)
