"""cfMesh + measured gates for a scan-14 Gate-M1 surface (work order 2026-09-24 Task 3). Blinding: package files + the geometry stage's STL only; no 0D code.
usage: build_m1_mesh.py <clean_nolesion|baseline|T1_missed_branch> [--variant=N] [--tag=name]      output P/m1/mesh/<case>[_<tag>]/ (must not exist)
Recipe (from the 837 make_lesion_mesh.py and the U3D make_sten70_mesh.py): maxCellSize 2e-4; 4 boundary layers ratio 1.2 (spec 6.2); sphere refinements (r 4 mm, request 6e-5 -> 50 um) at the inlet and every outlet cap (the 837 patch-loss history);
chained cones (r 3 mm, step 1.5 mm) along the LAD main path root -> out_600: 50 um (request 7e-5) for path arc [s_t-12, s_t+22] mm around the throat (s_t = arc of the probes.csv throat point), 25 um (request 4e-5) for [s_t-4, s_t+4] (lesion cases only:
>= 12 cells across a 0.46 mm throat needs <= 38 um), 100 um (request 1.4e-4: a request of exactly 1e-4 rounds DOWN to the 50 um level, found in variant 1) on the rest of the path, and a 100 um chain on the first 12 mm of D1 (jet junction, as in 837). Every process is run under nice -n 19, OMP_NUM_THREADS=4 and ulimit -v 9 GB.
Gates MEASURED on the mesh: cartesianMesh finished, checkMesh standard OK, strict checkMesh failed-check count and flagged sets LOCALISED (per tree segment, near the whisker sites nodes 285/133, in/near the throat zones and interfaces, near the caps),
patch faces > 0 for inlet + every out_<id>, cells, cells across the throat (8 in-plane diameters through the section centroid, 0.5 um sampling, runs of equal cell ids; min/median), p95 cell size in the throat zone (+-2 mm arc), the 4-layer stack at the throat
(radial rays inward from the wall), throat-plane mesh area vs the surface section area of the STL, peak RAM (/usr/bin/time) and wall-clock."""
import sys, os, re, json, time, shutil, subprocess, collections, csv, glob
import numpy as np, pyvista as pv
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
PKG = {"clean_nolesion": "14_left_LAD_prox_20mm_80ds__clean_nolesion__real", "baseline": "14_left_LAD_prox_20mm_80ds__baseline__real", "T1_missed_branch": "14_left_LAD_prox_20mm_80ds__T1_missed_branch__real"}
FOAM = "source /usr/lib/openfoam/openfoam2406/etc/bashrc"
TEMPLATE = f"{P}/lesion80/mesh_case2"                       # 837 system/ (fvSchemes, fvSolution, controlDict) + constant/ transport properties come from the audited lesion80 mesh dir
REQ = {"throat25": float(os.environ.get("M1_THROAT_REQ", "0.00004")), "tube50": 0.00007, "coarse100": 0.00014, "sphere": 0.00006}
T_LO, T_HI = float(os.environ.get("M1_THROAT_LO_MM", "-4.0")), float(os.environ.get("M1_THROAT_HI_MM", "4.0"))    # throat refinement zone along the LAD arc relative to the throat (Task A D7 variants; defaults = the returned recipe)
ULIMIT_KB = int(os.environ.get("M1_ULIMIT_KB", "9000000"))
R_CYL, R_SPH, SEG_M, MAXCELL = 0.0030, 0.0040, 0.0015, 0.00020
WHISKER_NODES = (285, 133)

def load_centreline(pk):
    m = pv.read(f"{pk}/centreline.vtp"); P_ = np.asarray(m.points); adj = collections.defaultdict(list); ln = m.lines; i = 0
    while i < len(ln): n = ln[i]; a, b = ln[i + 1:i + 3]; adj[int(a)].append(int(b)); adj[int(b)].append(int(a)); i += n + 1
    prev = {0: None}; q = [0]
    for u in q:
        for v in adj[u]:
            if v not in prev: prev[v] = u; q.append(v)
    return m, P_, prev

def path_to(prev, leaf):
    p = []; u = leaf
    while u is not None: p.append(u); u = prev[u]
    return p[::-1]

def arcs(P_, idx): return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P_[idx], axis=0), axis=1))])

def stl_patch_centres(stl, names):
    """Vertex mean of the small patch solids (inlet, out_*): a cap is planar, so the vertex mean lies on it."""
    acc = {}; cur = None
    with open(stl) as f:
        for ln in f:
            if ln.startswith("solid "):
                nm = ln.split()[1]; cur = nm if nm in names else None
                if cur: acc[cur] = []
            elif cur and "vertex" in ln:
                acc[cur].append([float(x) for x in ln.split()[1:4]])
            elif ln.startswith("endsolid"): cur = None
    return {k: np.mean(np.array(v), axis=0) for k, v in acc.items()}

def meshdict(case, pk, with_throat):
    m, P_, prev = load_centreline(pk); sn = np.asarray(m["segment_name"]); tn = np.asarray(m["tree_node"])
    outl = list(csv.DictReader(open(f"{pk}/outlets.csv"))); ids = [r["outlet_id"] for r in outl]
    # tree_node == point index only for the first nodes: map the tree_node values of outlets.csv to point indices
    pidx = {int(t): i for i, t in enumerate(tn)}
    paths = {r["outlet_id"]: path_to(prev, pidx[int(r["tree_node"])]) for r in outl}
    lad_id = max(paths, key=lambda k: sum(1 for i in paths[k] if str(sn[i]) == "LAD")); lad_path = paths[lad_id]     # the outlet whose root path holds the most LAD points = the LAD main path (out_600 in clean/baseline)
    d1_ids = [k for k in paths if any(str(sn[i]) == "D1" for i in paths[k])]; d1_path = paths[d1_ids[0]] if d1_ids else []                       # none in T1 (D1 deleted)
    thr = [r for r in csv.DictReader(open(f"{pk}/probes.csv")) if r["kind"] == "throat"][0]; thr_xyz = np.array([float(thr[k]) for k in ("x", "y", "z")]); thr_n = np.array([float(thr[k]) for k in ("normal_x", "normal_y", "normal_z")])
    a = arcs(P_, lad_path); j = int(np.argmin(np.linalg.norm(P_[lad_path] - thr_xyz, axis=1))); s_t = float(a[j])
    # resample the LAD path every SEG and build the chained cones with the size of the arc at the cone start
    def chain(idx, name, size_fn):
        aa = arcs(P_, idx); q = np.arange(0, aa[-1], SEG_M * 1e3); Q = np.stack([np.interp(q, aa, P_[idx][:, k]) for k in range(3)], 1) * 1e-3; out = []
        for i in range(len(Q) - 1): out.append((f"{name}_{i}", Q[i], Q[i + 1], size_fn(q[i])))
        return out
    def lad_size(arc):
        if with_throat and T_LO <= arc - s_t <= T_HI: return REQ["throat25"]
        if s_t - 12.0 <= arc <= s_t + 22.0: return REQ["tube50"]
        return REQ["coarse100"]
    cones = chain(lad_path, "lad", lad_size)
    d1_seg = [i for i in d1_path if str(sn[i]) == "D1"]
    if d1_seg: cones += chain(d1_seg[:np.searchsorted(arcs(P_, d1_seg), 12.0) + 1], "d1", lambda a_: REQ["coarse100"])
    return dict(cones=cones, s_t=s_t, thr_xyz=thr_xyz, thr_n=thr_n, lad_path=lad_path, ids=ids, P=P_, tn=tn, sn=sn, m=m, lad_arcs=a, thr_pt_index=lad_path[j], lad_outlet=lad_id, d1_outlet=(d1_ids[0] if d1_ids else None))

def write_case(case, tag, outdir, variant):
    pk = f"{HERE}/pkg/{PKG[case]}"; stl = f"{HERE}/out/{case}/case.stl"; with_throat = case != "clean_nolesion"
    D = meshdict(case, pk, with_throat)
    os.makedirs(outdir + "/constant/triSurface"); os.makedirs(outdir + "/system")
    for f in ("controlDict", "fvSchemes", "fvSolution"): shutil.copy(f"{TEMPLATE}/system/{f}", f"{outdir}/system/{f}")
    for f in ("transportProperties", "turbulenceProperties"):
        src = f"{TEMPLATE}/constant/{f}"
        if os.path.exists(src): shutil.copy(src, f"{outdir}/constant/{f}")
    os.symlink(os.path.abspath(stl), f"{outdir}/constant/triSurface/case.stl")
    outl = list(csv.DictReader(open(f"{pk}/outlets.csv"))); inl = json.load(open(f"{pk}/inlet.json"))
    centres = stl_patch_centres(stl, {"inlet"} | {r["outlet_id"] for r in outl}); assert len(centres) == 1 + len(outl), sorted(centres)
    obj = "".join(f"    {n}_ref {{ type sphere; cellSize {REQ['sphere']:.5f}; centre ({c[0]*1e0:.6f} {c[1]:.6f} {c[2]:.6f}); radius {R_SPH}; }}\n" for n, c in centres.items())
    obj += "".join(f"    {n:9s} {{ type cone; cellSize {sz:.5f}; p0 ({p0[0]:.6f} {p0[1]:.6f} {p0[2]:.6f}); radius0 {R_CYL}; p1 ({p1[0]:.6f} {p1[1]:.6f} {p1[2]:.6f}); radius1 {R_CYL}; }}\n" for n, p0, p1, sz in D["cones"])
    md = (f'FoamFile {{ version 2.0; format ascii; class dictionary; object meshDict; }}\nsurfaceFile "constant/triSurface/case.stl";\nmaxCellSize {MAXCELL:.5f};\n'
          f"boundaryLayers {{ nLayers 4; thicknessRatio 1.2; }}\n\nobjectRefinements\n{{\n{obj}}}\n")
    open(outdir + "/system/meshDict", "w").write(md)
    json.dump(dict(case=case, variant=variant, s_throat_arc_mm=D["s_t"], n_cones=len(D["cones"]), cell_requests_m=REQ, zones=dict(throat25_arc_mm=[D["s_t"] + T_LO, D["s_t"] + T_HI] if with_throat else None, throat_request_m=REQ["throat25"], tube50_arc_mm=[D["s_t"] - 12, D["s_t"] + 22]), patch_centres_m={k: v.tolist() for k, v in centres.items()}),
              open(outdir + "/recipe.json", "w"), indent=1)
    return D, pk, stl

def run_mesher(outdir):
    free = int(re.search(r"MemAvailable:\s+(\d+)", open("/proc/meminfo").read()).group(1)) // 1024; du = shutil.disk_usage("/").free // 2 ** 30
    if free < 12000 or du < 12: raise SystemExit(f"resource guard: MemAvailable {free} MB (< 12000) or free disk {du} GB (< 12): not started")
    env = (f"{FOAM}; cd {outdir}; export OMP_NUM_THREADS=4 MALLOC_ARENA_MAX=2; ulimit -v {ULIMIT_KB}; "
           "/usr/bin/time -v -o log.time.cartesianMesh nice -n 19 cartesianMesh > log.cartesianMesh 2>&1; "
           "nice -n 19 checkMesh > log.checkMesh.standard 2>&1; nice -n 19 checkMesh -allGeometry -allTopology -writeSets vtk > log.checkMesh.strict 2>&1")
    t = time.time(); subprocess.run(["bash", "-c", env]); return time.time() - t

def measure(outdir, D, pk, stl, with_throat):
    g = {}
    open(f"{outdir}/case.foam", "w").close()
    rd = pv.OpenFOAMReader(f"{outdir}/case.foam"); rd.disable_all_cell_arrays(); rd.disable_all_point_arrays(); rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh")
    mb = rd.read(); m = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
    m = m.compute_cell_sizes(length=False, area=False, volume=True); vol = m.cell_data["Volume"]; h = np.cbrt(vol); cc = np.asarray(m.cell_centers().points)
    c = D["thr_xyz"] * 1e-3; t = D["thr_n"] / np.linalg.norm(D["thr_n"])
    sl = m.slice(normal=t, origin=c).connectivity(extraction_mode="closest", closest_point=c).compute_cell_sizes(length=False, area=True, volume=False)
    A = sl.cell_data["Area"]; ctr = np.asarray(sl.cell_centers().points); cen = (ctr * A[:, None]).sum(0) / A.sum(); g["throat_plane_mesh_area_mm2"] = float(A.sum() * 1e6)
    g["throat_plane_centroid_offset_from_probe_mm"] = float(np.linalg.norm(cen - c) * 1e3)
    a_ = np.cross(t, [1.0, 0, 0]); a_ = a_ / np.linalg.norm(a_) if np.linalg.norm(a_) > 1e-6 else np.cross(t, [0, 1.0, 0]); b_ = np.cross(t, a_)
    import vtk
    loc = vtk.vtkStaticCellLocator(); loc.SetDataSet(m); loc.BuildLocator()
    def ray(d, step=0.5e-6, maxlen=3e-3):
        """cell-id runs along cen +- s*d until three consecutive misses; returns (n_cells, length_m, list of run lengths from one wall to the other)"""
        pts = []; miss = 0; s = -maxlen
        ids = []; s_list = []
        for s in np.arange(-maxlen, maxlen, step):
            cid = loc.FindCell((cen + s * d).tolist()); ids.append(cid); s_list.append(s)
        ids = np.array(ids); s_arr = np.array(s_list); inside = ids >= 0
        # the connected inside interval that contains s = 0
        k0 = int(np.argmin(np.abs(s_arr)));
        if not inside[k0]: return 0, 0.0, []
        lo = k0
        while lo > 0 and inside[lo - 1]: lo -= 1
        hi = k0
        while hi < len(ids) - 1 and inside[hi + 1]: hi += 1
        seg = ids[lo:hi + 1]; runs = []; cur = 1
        for x, y in zip(seg[:-1], seg[1:]):
            if y == x: cur += 1
            else: runs.append(cur * step); cur = 1
        runs.append(cur * step)
        return len(runs), (hi - lo + 1) * step, runs
    counts, diam, stacks = [], [], []
    for k in range(8):
        th = np.pi * k / 8; d = np.cos(th) * a_ + np.sin(th) * b_; n, L, runs = ray(d); counts.append(n); diam.append(L * 1e3)
        if n >= 8: stacks.append([float(sum(runs[:i])) * 1e6 for i in range(1, 5)])
    g["cells_across_throat_diameter"] = dict(per_diameter=counts, median=float(np.median(counts)), min=int(min(counts)), chord_lengths_mm=[round(x, 4) for x in diam], method="8 in-plane diameters through the section centroid, 0.5 um sampling, runs of equal cell ids inside the lumen")
    g["throat_min_over_max_chord"] = float(min(diam) / max(diam)) if diam and max(diam) > 0 else None
    # 4-layer stack: first 4 run lengths from the wall along the ray, both ends averaged (cumulative thickness of layers 1..4, um)
    st = []
    for k in range(8):
        th = np.pi * k / 8; d = np.cos(th) * a_ + np.sin(th) * b_; n, L, runs = ray(d)
        if n >= 8: st.append([sum(runs[:4]) * 1e6, sum(runs[-4:]) * 1e6, runs[0] * 1e6, runs[-1] * 1e6])
    if st: st = np.array(st); g["boundary_layer_um"] = dict(first4_stack_median=float(np.median(st[:, :2])), first_cell_median=float(np.median(st[:, 2:])), note="run lengths from the wall of the first 4 cells on both ends of 8 diameters")
    # p95 cell size in +-2 mm of the throat along the LAD path
    lad = D["P"][D["lad_path"]] * 1e-3; arc = D["lad_arcs"]; tr = cKDTree(lad); dd, jj = tr.query(cc, distance_upper_bound=1.2e-3)
    sel = (dd < 1.2e-3) & (np.abs(arc[np.minimum(jj, len(arc) - 1)] - D["s_t"]) <= 2.0)
    g["cell_size_um_throat_pm2mm_arc"] = dict(n=int(sel.sum()), median=float(np.median(h[sel]) * 1e6), p95=float(np.percentile(h[sel], 95) * 1e6), min=float(h[sel].min() * 1e6)) if sel.any() else None
    for lab, lo, hi in (("tube50_zone", D["s_t"] - 12, D["s_t"] + 22),):
        s2 = (dd < 1.2e-3) & (arc[np.minimum(jj, len(arc) - 1)] >= lo) & (arc[np.minimum(jj, len(arc) - 1)] <= hi)
        g["cell_size_um_" + lab] = dict(n=int(s2.sum()), median=float(np.median(h[s2]) * 1e6), p95=float(np.percentile(h[s2], 95) * 1e6))
    # throat-plane area of the STL surface
    try:
        surf = pv.read(stl); ss = surf.slice(normal=t, origin=c).connectivity(extraction_mode="closest", closest_point=c)
        pts = np.asarray(ss.points); q = pts - c; x = q @ a_; y = q @ b_
        ln = ss.lines; i = 0; order = []
        segs = []
        while i < len(ln): n = ln[i]; segs.append(ln[i + 1:i + 1 + n]); i += n + 1
        adj = collections.defaultdict(list)
        for s_ in segs:
            for u, v in zip(s_[:-1], s_[1:]): adj[int(u)].append(int(v)); adj[int(v)].append(int(u))
        start = next(iter(adj)); order = [start]; seen = {start}; cur = start
        while True:
            nx = [v for v in adj[cur] if v not in seen]
            if not nx: break
            cur = nx[0]; order.append(cur); seen.add(cur)
        xs, ys = x[order], y[order]; a_stl = 0.5 * abs(np.dot(xs, np.roll(ys, -1)) - np.dot(ys, np.roll(xs, -1)))
        g["throat_plane_stl_area_mm2"] = float(a_stl * 1e6); g["throat_plane_area_err_pct"] = float(100 * (g["throat_plane_mesh_area_mm2"] / (a_stl * 1e6) - 1)); g["stl_loop_points_used"] = len(order)
    except Exception as e:
        g["throat_plane_stl_area_mm2"] = None; g["throat_plane_area_err_pct"] = None; g["stl_area_error"] = f"{type(e).__name__}: {e}"
    g["mesh_volume_mm3"] = float(vol.sum() * 1e9); g["cells_total_check"] = int(m.n_cells)
    # localisation of flagged sets
    allc = D["P"]; tnode = D["tn"]; snm = D["sn"]; kd = cKDTree(allc); lad_t = int(np.argmin(np.linalg.norm(allc - D["thr_xyz"], axis=1)))
    mb0 = pv.read(f"{HERE}/pkg/{PKG['baseline']}/centreline.vtp"); tn0 = np.asarray(mb0["tree_node"]); wh = np.array([np.asarray(mb0.points)[int(np.where(tn0 == w)[0][0])] for w in WHISKER_NODES])   # whisker sites (LAD node 285, D1 node 133) from the baseline package: same anatomy in all three
    cent = json.load(open(f"{outdir}/recipe.json"))["patch_centres_m"]; capc = np.array(list(cent.values())) * 1e3
    fl = {}
    for f in sorted(glob.glob(f"{outdir}/postProcessing/constant/*/*.vtp")) + sorted(glob.glob(f"{outdir}/postProcessing/*/*.vtp")):
        pts = np.asarray(pv.read(f).points) * 1e3
        if not len(pts): continue
        dist, ii = kd.query(pts); seg = collections.Counter(str(snm[i]) for i in ii)
        # arc on the LAD path of the nearest LAD-path point
        lp = D["P"][D["lad_path"]]; d2, j2 = cKDTree(lp).query(pts); on_lad = d2 < 1.5; arc_ = D["lad_arcs"][j2]
        fl[os.path.basename(f)[:-4]] = dict(n_points=int(len(pts)), per_segment=dict(seg), min_dist_to_throat_mm=float(np.min(np.linalg.norm(pts - D["thr_xyz"], axis=1))),
              n_within_2mm_of_whisker_sites=int((np.min(np.linalg.norm(pts[:, None, :] - wh[None], axis=2), axis=1) < 2.0).sum()), n_within_4mm_of_caps=int((np.min(np.linalg.norm(pts[:, None, :] - capc[None], axis=2), axis=1) < 4.0).sum()),
              n_on_lad_path=int(on_lad.sum()), n_in_throat25_zone=int((on_lad & (np.abs(arc_ - D["s_t"]) <= 4.0)).sum()) if with_throat else 0,
              n_at_25um_interfaces_pm1mm=int((on_lad & ((np.abs(arc_ - (D["s_t"] - 4)) < 1.0) | (np.abs(arc_ - (D["s_t"] + 4)) < 1.0))).sum()) if with_throat else 0, n_in_tube50_zone=int((on_lad & (arc_ >= D["s_t"] - 12) & (arc_ <= D["s_t"] + 22)).sum()),
              n_at_50um_interfaces_pm1mm=int((on_lad & ((np.abs(arc_ - (D["s_t"] - 12)) < 1.0) | (np.abs(arc_ - (D["s_t"] + 22)) < 1.0))).sum()))
    g["flagged_sets_localised"] = fl
    return g

def main(case, tag=None, variant=1):
    outdir = f"{HERE}/mesh/{case}" + (f"_{tag}" if tag else "")
    if os.path.exists(outdir): raise SystemExit(f"{outdir} exists")
    t0 = time.time(); D, pk, stl = write_case(case, tag, outdir, variant); with_throat = case != "clean_nolesion"
    wall = run_mesher(outdir)
    lc = open(f"{outdir}/log.cartesianMesh").read() if os.path.exists(f"{outdir}/log.cartesianMesh") else ""; std = open(f"{outdir}/log.checkMesh.standard").read() if os.path.exists(f"{outdir}/log.checkMesh.standard") else ""; strict = open(f"{outdir}/log.checkMesh.strict").read() if os.path.exists(f"{outdir}/log.checkMesh.strict") else ""
    tm = open(f"{outdir}/log.time.cartesianMesh").read() if os.path.exists(f"{outdir}/log.time.cartesianMesh") else ""
    g = dict(case=case, variant=variant, cartesianMesh_finished=("End" in lc), checkMesh_standard_OK=("Mesh OK" in std), wall_clock_mesh_s=round(wall, 1))
    m_ = re.search(r"Maximum resident set size \(kbytes\): (\d+)", tm); g["cartesianMesh_peak_rss_gb"] = round(int(m_.group(1)) / 2 ** 20, 2) if m_ else None
    m_ = re.search(r"Elapsed \(wall clock\) time.*: ([\d:.]+)", tm); g["cartesianMesh_elapsed"] = m_.group(1) if m_ else None
    g["exit_note"] = "bad_alloc / memory cap hit" if re.search(r"bad_alloc|std::bad_alloc|Cannot allocate", lc) else None
    m_ = re.search(r"cells:\s+(\d+)", strict); g["cells"] = int(m_.group(1)) if m_ else None
    g["strict_failed_checks"] = int(re.search(r"Failed (\d+) mesh checks", strict).group(1)) if "Failed" in strict else (0 if strict else None)
    for k, pat in (("max_nonortho", r"Mesh non-orthogonality Max: ([\d.]+)"), ("max_skew", r"Max skewness = ([\d.]+)"), ("max_aspect", r"Max aspect ratio = ([\d.]+)")):
        mm = re.search(pat, strict); g[k] = float(mm.group(1)) if mm else None
    g["strict_failure_lines"] = [ln.strip() for ln in strict.splitlines() if "***" in ln][:12]
    bpath = f"{outdir}/constant/polyMesh/boundary"
    exp = ["inlet", "wall"] + list(D["ids"])
    if os.path.exists(bpath):
        bt = open(bpath).read(); g["patch_faces"] = {n: int(f) for n, f in re.findall(r"(\w+)\s*\{[^}]*?nFaces\s+(\d+);", bt)}
        g["patches_expected_present_nonzero"] = all(g["patch_faces"].get(n, 0) > 0 for n in exp); g["patches_missing_or_empty"] = [n for n in exp if g["patch_faces"].get(n, 0) <= 0]
    else: g["patch_faces"] = {}; g["patches_expected_present_nonzero"] = False; g["patches_missing_or_empty"] = exp
    if g["cartesianMesh_finished"] and g["checkMesh_standard_OK"] and g["cells"]:
        try: g.update(measure(outdir, D, pk, stl, with_throat))
        except Exception as e: g["measure_error"] = f"{type(e).__name__}: {e}"
    ok_cells_across = (g.get("cells_across_throat_diameter") or {}).get("min", 0) >= 12 if with_throat else None
    g["GATES_PASS"] = bool(g["cartesianMesh_finished"] and g["checkMesh_standard_OK"] and g["patches_expected_present_nonzero"] and (ok_cells_across if with_throat else True) and abs(g.get("throat_plane_area_err_pct") or 0) < 2.0)
    g["gate_definition"] = "finished + standard checkMesh OK + inlet and every out_<id> patch > 0 faces + (lesion cases) >= 12 cells across the throat (min over 8 diameters) + |throat plane area error| < 2 % (strict checkMesh failures are localised and disclosed, not a gate, as for the 837 meshes)"
    g["total_wall_incl_gates_s"] = round(time.time() - t0, 1)
    json.dump(g, open(f"{outdir}/mesh_gates.json", "w"), indent=1, default=float); print(json.dumps(g, indent=1, default=float)[:6000])
    return g

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]; kw = dict(x[2:].split("=") for x in sys.argv[1:] if x.startswith("--") and "=" in x)
    if not a: raise SystemExit(__doc__)
    main(a[0], kw.get("tag"), int(kw.get("variant", 1)))
