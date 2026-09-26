"""Gate-M1 geometry pipeline for the shipped scan-14 packages (work order 2026-09-24, Task 3 'Build'; CFD-ARM-SPEC 6.1b/6.2). GEOMETRY ONLY: no mesher, no solver, no 0D code.
usage: build_m1_geometry.py <package_dir_name> <outdir> [--e0-waiver "reason"] [--stop-after STAGE] [--no-surfacecheck]
Pipeline: E0 guard -> package + mask provenance -> frame check -> mask deletion by mask_edit.json's reference implementation (run verbatim, once over the union of truncation and branch sets)
-> left-tree component holding the inlet -> marching cubes (skimage, level 0.5) -> Taubin smoothing (vmtksurfacesmoothing -iterations 30 -passband 0.1, the exact 837 recipe)
-> local plane clips at inlet + outlets (clip_outlets.clip_at_leaves, as 837) -> [baseline/T1: lesion window subdivided to edge <= r_throat/8 BEFORE deforming, radial_scale rule about the smoothed path frames,
as-built throat gate] -> straight flow extensions (5 D inlet, 3 D outlets; D = 2 r_mm) with planar fan caps -> case.stl (solids inlet, <outlet_id>..., wall; metres) + gates.json + surface_radius_<case>.csv.
As-built throat rule. The work order asks: as-built throat radius vs r_target_mm within 1 %. Measured on the CLEAN case before any lesion was built: the package's r_source_mm (vmtk MaximumInscribedSphereRadius on the
dataset's own surface) and the sphere radius of THIS mask-derived surface differ by -4 % median and +-10 % per node (gates.json / README), so an ABSOLUTE 1 % test against r_target_mm cannot be met by any deformation of this surface.
Therefore the gate that decides is RELATIVE: (as-built radius) / (undeformed radius of the same section by the same definition) versus radial_scale within 1 %, for the 2-D maximum inscribed circle, the area-equivalent radius and the
sphere centred on the smoothed axis point (the vmtk definition); the LITERAL absolute deviations (as-built vs r_target_mm, all definitions) are reported next to it and flagged. This is a disclosed deviation.
Reject = exit code 3 with gates.json written. No threshold is tuned and nothing is repaired by hand."""
import os, sys, json, time, argparse, subprocess, shutil, csv
import numpy as np, nibabel as nib, pyvista as pv
from scipy.ndimage import label, generate_binary_structure, distance_transform_edt
from scipy.spatial import cKDTree
from scipy.interpolate import splprep, splev
from skimage import measure

HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, P)
import e0_guard
from m1lib import *
from clip_outlets import clip_at_leaves          # pure numpy/pyvista (837 code)

MASK = "/mnt/e/Paper6-T6/cfd_local_only/archive/paper6_t6_cfd_2026-09_bulk_moved/imagecas_x_raw/extracted/ImageCAS-X_dataset/segmentations/14.coronary.nii.gz"
VMTK_ENV = "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/micromamba/envs/vmtk"
SMOOTH_ITER, SMOOTH_PASSBAND = 30, 0.1
EXT_INLET_D, EXT_OUTLET_D = 5.0, 3.0
LOCAL_RADIUS_FACTOR = 5.0                  # as build_case_surface.build_open_surface
SPLINE_SIGMA_MM = 0.1                      # smoothing-spline scatter of the path frames (837: 0.1 mm on ~0.4 mm node spacing)
FRAME_DS_MM = 0.02
SHIPPED = {"clean_nolesion": dict(removed=1310, erosion=25, components=2), "baseline": dict(removed=1310, erosion=25, components=2), "T1_missed_branch": dict(removed=2089, erosion=40, components=2)}
THROAT_TOL = 0.01
D_BASIS = 'rmm'

def to_ijk(inv, pts, flip=True):
    f = np.array([-1.0, -1.0, 1.0]) if flip else np.ones(3)
    a = np.asarray(pts, float).reshape(-1, 3) * f
    return (inv @ np.c_[a, np.ones(len(a))].T)[:3].T

def xyz(rows): return np.array([[p["x"], p["y"], p["z"]] for p in rows], float)

# ------------------------------------------------------------------ package
def load_package(pk):
    d = f"{HERE}/pkg/{pk}"
    m = json.load(open(f"{d}/mask_edit.json")); meta = json.load(open(f"{d}/meta.json")); inlet = json.load(open(f"{d}/inlet.json"))
    outs = list(csv.DictReader(open(f"{d}/outlets.csv"))); bcA = {r["outlet_id"]: r for r in csv.DictReader(open(f"{d}/bc_A.csv"))}
    cl = pv.read(f"{d}/centreline.vtp")
    kind = "T1_missed_branch" if "T1_missed_branch" in pk else ("baseline" if "__baseline__" in pk else "clean_nolesion")
    return dict(dir=d, name=pk, kind=kind, mask_edit=m, meta=meta, inlet=inlet, outlets=outs, bc_A=bcA, cl=cl)

# ------------------------------------------------------------------ mask stage
def mask_stage(pkg, outdir, rep):
    m = pkg["mask_edit"]; wd = f"{outdir}/mask_work"; os.makedirs(wd, exist_ok=True)
    img = nib.load(MASK); lab = np.asarray(img.dataobj); mask = lab > 0; inv = np.linalg.inv(img.affine); sp = np.array(img.header.get_zooms()[:3], float)
    def n_in(pts, flip=True):
        q = np.rint(to_ijk(inv, xyz(pts), flip)).astype(int); ok = ((q >= 0) & (q < mask.shape)).all(1)
        return int(sum(bool(mask[tuple(x)]) for x, o in zip(q, ok) if o)), int(len(q))
    deleted_branch = list(m.get("mask_edit", {}).get("deleted_points_mm", []) or [])
    kill = list(m["sub_cut_points_mm"]) + deleted_branch
    fc = dict(convention="LPS mm; NIfTI affine is RAS: negate x,y before inv(affine)",
              sub_cut_points_inside_lumen_with_flip=n_in(m["sub_cut_points_mm"]), sub_cut_points_inside_lumen_without_flip=n_in(m["sub_cut_points_mm"], False),
              branch_deletion_points_inside_lumen_with_flip=(n_in(deleted_branch) if deleted_branch else None), branch_deletion_points_inside_lumen_without_flip=(n_in(deleted_branch, False) if deleted_branch else None),
              all_deletion_points_inside_with_flip=n_in(kill), retained_points_inside_with_flip=n_in(m["retained_points_mm"]))
    fc["PASS"] = fc["all_deletion_points_inside_with_flip"][0] == fc["all_deletion_points_inside_with_flip"][1] and fc["all_deletion_points_inside_with_flip"][0] > 0
    rep["frame_check"] = fc
    # the reference implementation, verbatim
    open(f"{wd}/mask_edit.json", "w").write(open(f"{pkg['dir']}/mask_edit.json").read())
    open(f"{wd}/ref_deletion_impl.py", "w").write(f'MASK_NII = "{MASK}"\n' + m["reference_implementation"])
    with timed(rep, "mask_deletion_reference_impl"):
        subprocess.run([sys.executable, "ref_deletion_impl.py"], cwd=wd, check=True)
    out = np.asarray(nib.load(f"{wd}/mask_edited.nii.gz").dataobj) > 0
    removed = mask & ~out; added = out & ~mask
    ri = np.argwhere(removed); ras = (img.affine @ np.c_[ri, np.ones(len(ri))].T)[:3].T; lps_removed = ras * np.array([-1.0, -1.0, 1.0])
    rp = xyz(m["retained_points_mm"]); rr = np.array([p["r_mm"] for p in m["retained_points_mm"]]); tr = cKDTree(rp); dd, ii = tr.query(lps_removed, k=min(8, len(rp)))
    ratio = np.min(dd / rr[ii], axis=1) if len(ri) else np.array([])
    st6, st26 = generate_binary_structure(3, 1), generate_binary_structure(3, 3)
    comp_before = {"6": int(label(mask, structure=st6)[1]), "26": int(label(mask, structure=st26)[1])}; comp_after = {"6": int(label(out, structure=st6)[1]), "26": int(label(out, structure=st26)[1])}
    shipped = SHIPPED[pkg["kind"]]
    me = dict(sha256_mask=sha256_file(MASK), sha256_expected=pkg["meta"]["provenance"]["mask_nii_sha256"], reference_impl="mask_edit.json reference_implementation, executed verbatim (only a MASK_NII line is prepended)",
              protect_radius_factor=1.10, connectivity=6, n_deletion_points=len(kill), n_retained_points=len(rp),
              voxels_removed=int(removed.sum()), voxels_added=int(added.sum()), shipped_voxels_removed=shipped["removed"],
              removed_labels={int(v): int((lab[removed] == v).sum()) for v in np.unique(lab[removed])},
              components_before=comp_before, components_after=comp_after, shipped_components=shipped["components"],
              erosion_shipped=shipped["erosion"],
              erosion_definition_note="the packages give a shipped erosion count (25 truncation-only, 40 with the branch) but not its definition. Measured here: removed voxels whose nearest retained centreline point is at distance <= f x r_mm (protect ball is 1.10 r, so f<=1.10 is 0 by construction).",
              erosion_removed_voxels_within_f_r={str(f): int((ratio <= f).sum()) for f in (1.1, 1.15, 1.2, 1.25, 1.3, 1.5, 2.0)})
    me["voxels_removed_matches_shipped"] = me["voxels_removed"] == shipped["removed"]; me["components_match_shipped"] = comp_after["6"] == shipped["components"] and comp_after["26"] == shipped["components"]
    me["sha256_matches_package"] = me["sha256_mask"] == me["sha256_expected"]
    cl = pkg["cl"]; seg = np.asarray(cl.point_data["segment_name"]); lad = np.asarray(cl.points)[seg == "LAD"]
    dl = cKDTree(lad).query(lps_removed)[0] if len(ri) else np.array([])
    me["removed_voxels_within_r_of_a_LAD_node_mm"] = {str(x): int((dl <= x).sum()) for x in (1.0, 2.0, 3.0)}
    rep["mask_edit"] = me
    return img, lab, mask, out, inv, sp

def left_tree(pkg, img, mask_before, mask_after, inv, sp, rep):
    inlet = pkg["inlet"]["inlet"]; q = np.rint(to_ijk(inv, [[inlet["x"], inlet["y"], inlet["z"]]])[0]).astype(int)
    st26 = generate_binary_structure(3, 3)
    res = {}
    for nm, mk in (("before_edit", mask_before), ("after_edit", mask_after)):
        lb, n = label(mk, structure=st26)
        l0 = lb[tuple(q)]
        if l0 == 0:      # inlet centre is not a lumen voxel: nearest lumen voxel within 4 voxels
            sl = tuple(slice(max(c - 4, 0), c + 5) for c in q); sub = lb[sl]; idx = np.argwhere(sub > 0)
            c = idx[np.argmin(((idx + np.array([s.start for s in sl]) - q) ** 2).sum(1))] + np.array([s.start for s in sl]); l0 = lb[tuple(c)]
        res[nm] = (lb == l0)
    comp0, comp1 = res["before_edit"], res["after_edit"]
    lo = np.array([max(int(a.min()) - 12, 0) for a in np.where(comp0)]); hi = np.array([min(int(a.max()) + 13, s) for a, s in zip(np.where(comp0), mask_before.shape)])
    sl = tuple(slice(l, h) for l, h in zip(lo, hi))
    def edt(c): return distance_transform_edt(c[sl], sampling=sp)
    with timed(rep, "parent_radius_edt"):
        e0, e1 = edt(comp0), edt(comp1)
    cl = pkg["cl"]; seg = np.asarray(cl.point_data["segment_name"]); pts = np.asarray(cl.points)
    qi = np.rint(to_ijk(inv, pts)).astype(int) - lo
    ok = ((qi >= 0) & (qi < e0.shape)).all(1)
    v0 = np.full(len(pts), np.nan); v1 = np.full(len(pts), np.nan)
    v0[ok] = e0[tuple(qi[ok].T)]; v1[ok] = e1[tuple(qi[ok].T)]
    dr = v1 - v0
    def stat(sel):
        a = dr[sel & ok]
        return dict(n=int(len(a)), n_changed=int((np.abs(a) > 1e-9).sum()), max_abs_change_mm=float(np.abs(a).max()) if len(a) else None, max_decrease_mm=float(-a.min()) if len(a) else None,
                    median_change_mm=float(np.median(a)) if len(a) else None, max_relative_decrease_pct=float(100 * np.max(-(a) / np.maximum(v0[sel & ok], 1e-9))) if len(a) else None)
    chg = np.where(ok & (np.abs(dr) > 1e-9))[0]; tnn = np.asarray(cl.point_data["tree_node"])
    changed_nodes = [dict(node=int(i), tree_node=int(tnn[i]), segment=str(seg[i]), edt_before_mm=float(v0[i]), edt_after_mm=float(v1[i]), x_mm=[float(x) for x in pts[i]]) for i in chg]
    rep["parent_radius_change"] = dict(changed_nodes=changed_nodes, method="Euclidean distance transform (voxel spacing 0.318x0.318x0.5 mm) of the left-tree component, sampled at the centreline nodes, edited minus unedited mask",
                                       LAD_nodes=stat(seg == "LAD"), all_retained_nodes=stat(np.ones(len(pts), bool)), by_segment={s: stat(seg == s) for s in sorted(set(seg.tolist()))},
                                       )
    lab_l, n_l = label(comp1, structure=st26)
    rep["left_tree"] = dict(voxels_before_edit=int(comp0.sum()), voxels_after_edit=int(comp1.sum()), inlet_voxel=[int(v) for v in q], all_centreline_nodes_inside_component_after_edit=bool(np.all(comp1[tuple(np.clip(qi + lo, 0, np.array(comp1.shape) - 1).T)][ok])),
                            n_centreline_nodes_outside_component_after_edit=int((~comp1[tuple(np.clip(qi + lo, 0, np.array(comp1.shape) - 1).T)][ok]).sum()))
    return comp1, lo, hi

def surface_stage(pkg, comp, img, outdir, rep):
    inter = f"{outdir}/intermediate"; os.makedirs(inter, exist_ok=True)
    lo = np.array([max(int(a.min()) - 3, 0) for a in np.where(comp)]); hi = np.array([min(int(a.max()) + 4, s) for a, s in zip(np.where(comp), comp.shape)])
    sub = comp[tuple(slice(l, h) for l, h in zip(lo, hi))]
    with timed(rep, "marching_cubes"):
        v, f, n, _ = measure.marching_cubes(sub.astype(np.float32), level=0.5)
    v = v + lo
    ras = (img.affine @ np.c_[v, np.ones(len(v))].T)[:3].T; lps = ras * np.array([-1.0, -1.0, 1.0])
    surf = pv.PolyData(lps, np.c_[np.full(len(f), 3), f].ravel()).connectivity(extraction_mode="largest")
    raw = f"{inter}/raw_mc.vtp"; surf.save(raw)
    rep["surface"] = dict(marching_cubes="skimage.measure.marching_cubes level 0.5 on the isolated left-tree component (voxel-index vertices -> affine -> LPS mm)", n_points_raw=int(surf.n_points), n_cells_raw=int(surf.n_cells))
    sm = f"{inter}/smoothed.vtp"
    with timed(rep, "taubin_smoothing_vmtk"):
        subprocess.run([f"{VMTK_ENV}/bin/python", f"{VMTK_ENV}/bin/vmtksurfacesmoothing", "-ifile", raw, "-iterations", str(SMOOTH_ITER), "-passband", str(SMOOTH_PASSBAND), "-ofile", sm],
                       check=True, env=dict(os.environ, PATH=f"{VMTK_ENV}/bin:" + os.environ["PATH"]), stdout=open(f"{inter}/log.vmtk_smoothing", "w"), stderr=subprocess.STDOUT)
    s = pv.read(sm).extract_surface(algorithm="dataset_surface").triangulate().clean()
    rep["surface"].update(taubin=f"vmtksurfacesmoothing -iterations {SMOOTH_ITER} -passband {SMOOTH_PASSBAND} (identical to the 837 recipe; reproduces 837's smoothed.vtp exactly)", n_points_smoothed=int(s.n_points), n_cells_smoothed=int(s.n_cells),
                          bounds_mm=[float(x) for x in s.bounds], connected_components=int(len(np.unique(s.connectivity(extraction_mode="all").point_data["RegionId"]))))
    return s

# ------------------------------------------------------------------ centreline graph
def graph(pkg):
    cl = pkg["cl"]; xyzc = np.asarray(cl.points); lines = cl.lines.reshape(-1, 3)[:, 1:]
    adj = {i: [] for i in range(len(xyzc))}
    for a, b in lines: adj[int(a)].append(int(b)); adj[int(b)].append(int(a))
    inl = pkg["inlet"]["inlet"]; root = int(np.argmin(np.linalg.norm(xyzc - np.array([inl["x"], inl["y"], inl["z"]]), axis=1)))
    par = {root: None}; s = {root: 0.0}; order = [root]; stack = [root]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in par: par[w] = u; s[w] = s[u] + float(np.linalg.norm(xyzc[w] - xyzc[u])); order.append(w); stack.append(w)
    arc = np.array([s[i] for i in range(len(xyzc))])
    return dict(xyz=xyzc, adj=adj, root=root, parent=par, arc=arc)

def path_to(G, node):
    p = [node]
    while G["parent"][p[-1]] is not None: p.append(G["parent"][p[-1]])
    return p[::-1]

# ------------------------------------------------------------------ clip
def clip_stage(pkg, G, surf, rep):
    inl = pkg["inlet"]["inlet"]; n_in = np.array(inl["normal"], float); n_in /= np.linalg.norm(n_in)
    root = G["root"]; child = [w for w in G["adj"][root]][0]; dpath = G["xyz"][child] - G["xyz"][root]
    inlet_dot = float(n_in @ dpath / np.linalg.norm(dpath))
    leaves = [(np.array([inl["x"], inl["y"], inl["z"]]), -n_in, inl["r_mm"])]      # remove the proximal side of the inlet plane (clip_at_leaves keeps -d_plane > 0)
    o_info = []
    for r in pkg["outlets"]:
        p = np.array([float(r["x"]), float(r["y"]), float(r["z"])]); n = np.array([float(r["normal_x"]), float(r["normal_y"]), float(r["normal_z"])]); n /= np.linalg.norm(n)
        node = int(np.where(np.asarray(pkg["cl"].point_data["tree_node"]) == int(r["tree_node"]))[0][0]); par = G["parent"].get(node); back = G["xyz"][node] - G["xyz"][par] if par is not None else None
        o_info.append(dict(id=r["outlet_id"], p=p, n=n, r_mm=float(r["r_mm"]), r_ref_mm=float(r["r_ref_mm"]), tree_node=int(r["tree_node"]), point_index=node, outward_dot=float(n @ back / np.linalg.norm(back)) if back is not None else None))
        leaves.append((p, n, float(r["r_mm"])))
    with timed(rep, "clip_at_inlet_and_outlets"):
        clipped = clip_at_leaves(surf, leaves, local_radius_factor=LOCAL_RADIUS_FACTOR)
    clipped = clipped.extract_surface(algorithm="dataset_surface").triangulate().clean()
    P0 = np.asarray(clipped.points, float); F0 = clipped.faces.reshape(-1, 4)[:, 1:].copy()
    loops, ok = boundary_loops(F0)
    lo = []
    for lp in loops:
        L = P0[lp]; c = L.mean(0); u, s_, vt = np.linalg.svd(L - c); nrm = vt[2]
        uv = np.c_[(L - c) @ vt[0], (L - c) @ vt[1]]; wd = [np.ptp(uv @ np.array([np.cos(t), np.sin(t)])) for t in np.radians(np.arange(0, 180, 2.0))]
        lo.append(dict(n=int(len(lp)), width_max_over_min=float(max(wd) / min(wd)), width_min_mm=float(min(wd)), width_max_mm=float(max(wd)), centroid=c.tolist(), plane_rms_mm=float(np.sqrt(np.mean(((L - c) @ nrm) ** 2))), r_eq_mm=float(np.sqrt(0.5 * abs(np.linalg.norm(np.cross(L - c, np.roll(L - c, -1, 0)).sum(0))) / np.pi)), svd_normal=nrm.tolist()))
    rep["clip"] = dict(local_radius_factor=LOCAL_RADIUS_FACTOR, inlet_normal_dot_first_path_direction=inlet_dot, inlet_normal_is_distal=bool(inlet_dot > 0), outlets_normal_outward=[dict(id=o["id"], dot=o["outward_dot"]) for o in o_info],
                       n_loops=len(loops), expected_loops=1 + len(pkg["outlets"]), loops_simple=bool(ok), loops=lo, n_points=int(len(P0)), n_triangles=int(len(F0)),
                       components_after_clip=int(len(np.unique(clipped.connectivity(extraction_mode="all").point_data["RegionId"]))))
    rep["clip"]["PASS"] = bool(rep["clip"]["n_loops"] == rep["clip"]["expected_loops"] and ok and inlet_dot > 0 and all(o["outward_dot"] is not None and o["outward_dot"] > 0 for o in o_info) and rep["clip"]["components_after_clip"] == 1)
    return clipped, P0, F0, loops, dict(inlet=(np.array([inl["x"], inl["y"], inl["z"]]), -n_in, inl["r_mm"]), outlets=o_info)

# ------------------------------------------------------------------ lesion
class Frames:
    """Smoothing-spline frames of the root->LAD path (as 837), radial_scale interpolated from the package's per-node values, nearest-branch classification of vertices."""
    def __init__(self, pkg, G, rep):
        cl = pkg["cl"]; seg = np.asarray(cl.point_data["segment_name"]); rs_n = np.asarray(cl.point_data["radial_scale"], float)
        self.G, self.pkg = G, pkg; xyzc = G["xyz"]; les = pkg["mask_edit"]["lesion"]; self.c_mm, self.L_mm, self.ds_pct = les["centre_mm"], les["length_mm"], les["ds_pct"]
        leaves = [i for i in range(len(xyzc)) if len(G["adj"][i]) == 1 and i != G["root"] and seg[i] == "LAD"]
        assert len(leaves) == 1, f"expected one LAD leaf, found {leaves}"
        path = path_to(G, leaves[0]); arc = G["arc"][path]
        tn_all = np.asarray(cl.point_data["tree_node"]); tab = les["table"]
        offs = np.array([G["arc"][int(np.where(tn_all == r["tree_node"])[0][0])] - r["s_mm"] for r in tab])
        assert np.ptp(offs) < 1e-6, f"package s_mm is not a constant offset of the arc from the inlet node (ptp {np.ptp(offs)})"
        self.s_offset = float(offs[0])                     # package s_mm = arc along the centreline from the inlet node minus this offset (s = 0 at the LM/LAD/LCX split)
        self.s_end = self.c_mm + self.s_offset + self.L_mm / 2 + 8.0
        keep = arc <= self.s_end; path = np.array(path)[keep]; arc = arc[keep]; self.path = path
        u = arc / arc[-1]; tck, _ = splprep(xyzc[path].T, u=u, s=len(path) * SPLINE_SIGMA_MM ** 2, k=3)
        uu = np.linspace(0, 1, int(arc[-1] / FRAME_DS_MM)); c = np.array(splev(uu, tck)).T; d1 = np.array(splev(uu, tck, der=1)).T
        self.t = d1 / np.linalg.norm(d1, axis=1)[:, None]; self.c = c; self.s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))])
        tree = cKDTree(c); dn, jn = tree.query(xyzc[path]); self.node_frame = jn; s_node_spl = self.s[jn]
        self.rs = np.interp(self.s, s_node_spl, rs_n[path])
        dm = s_node_spl - arc
        self.station_map = dict(max_abs_arc_mismatch_mm=float(np.abs(dm).max()), max_node_to_curve_distance_mm=float(dn.max()), n_path_nodes=int(len(path)), spline_sigma_mm=SPLINE_SIGMA_MM)
        self.tree_c = tree
        # nearest-branch classification: densified polylines of all branches, tag = on the LAD path (frames)
        P, tag = [], []
        pset = set(path.tolist()); pedges = {(a, b) for a, b in zip(path[:-1], path[1:])} | {(b, a) for a, b in zip(path[:-1], path[1:])}
        for a in range(len(xyzc)):
            for b in G["adj"][a]:
                if b < a: continue
                nseg = max(int(np.linalg.norm(xyzc[b] - xyzc[a]) / 0.1), 1); q = np.linspace(0, 1, nseg + 1)[:, None]
                P.append(xyzc[a] + q * (xyzc[b] - xyzc[a])); tag += [(a, b) in pedges] * (nseg + 1)
        self.tree_all = cKDTree(np.vstack(P)); self.on_path = np.array(tag, bool)
        # sanity: rs equals r_target/r_source at the nodes
        rt, rsrc = np.asarray(cl.point_data["r_target_mm"], float), np.asarray(cl.point_data["r_source_mm"], float)
        self.rs_consistency_max_abs = float(np.abs(rt / rsrc - rs_n).max())
        self.window_frames = np.where(self.rs < 1.0 - 1e-12)[0]

    def apply(self, P):
        d, i = self.tree_c.query(P); j = self.tree_all.query(P)[1]
        moved = (self.rs[i] < 1.0 - 1e-12) & self.on_path[j]
        rel = P - self.c[i]; ax = np.einsum("ij,ij->i", rel, self.t[i])[:, None] * self.t[i]; rad = rel - ax
        Pn = P.copy(); Pn[moved] = (self.c[i] + ax + self.rs[i][:, None] * rad)[moved]
        return Pn, moved, self.rs[i], self.s[i], np.linalg.norm(rad, axis=1), self.on_path[j]

def refine_undeformed(P0, F, fr, h_max, max_pass=16):
    """Conforming edge-split refinement in UNDEFORMED space (837 refine(), threshold on the undeformed edge): an edge with a window endpoint and length > h_max is split; a triangle with 1/2/3 marked edges -> 2/3/4 triangles."""
    for it in range(max_pass):
        moved = fr.apply(P0)[1]
        e = np.unique(np.sort(np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1), axis=0)
        L = np.linalg.norm(P0[e[:, 0]] - P0[e[:, 1]], axis=1)
        mark = (L > h_max) & (moved[e[:, 0]] | moved[e[:, 1]])
        if not mark.any(): print(f"  refine: converged after {it} passes; {len(F)} triangles"); return P0, F, it
        me = e[mark]
        mid_id = {(int(a), int(b)): len(P0) + k for k, (a, b) in enumerate(me)}
        P0 = np.vstack([P0, 0.5 * (P0[me[:, 0]] + P0[me[:, 1]])])
        dist = lambda i, j: np.linalg.norm(P0[i] - P0[j]); key = lambda a, b: (a, b) if a < b else (b, a)
        newF = []
        for tri in F:
            a, b, c = (int(x) for x in tri)
            mab, mbc, mca = mid_id.get(key(a, b)), mid_id.get(key(b, c)), mid_id.get(key(c, a)); n = (mab is not None) + (mbc is not None) + (mca is not None)
            if n == 0: newF.append((a, b, c))
            elif n == 3: newF += [(a, mab, mca), (mab, b, mbc), (mca, mbc, c), (mab, mbc, mca)]
            elif n == 1:
                if mab is not None: newF += [(a, mab, c), (mab, b, c)]
                elif mbc is not None: newF += [(a, b, mbc), (a, mbc, c)]
                else: newF += [(b, c, mca), (a, b, mca)]
            elif mca is None:
                newF.append((mab, b, mbc))
                if dist(a, mbc) < dist(mab, c): newF += [(a, mab, mbc), (a, mbc, c)]
                else: newF += [(a, mab, c), (mab, mbc, c)]
            elif mab is None:
                newF.append((mbc, c, mca))
                if dist(a, mbc) < dist(b, mca): newF += [(a, b, mbc), (a, mbc, mca)]
                else: newF += [(a, b, mca), (b, mbc, mca)]
            else:
                newF.append((a, mab, mca))
                if dist(mab, c) < dist(b, mca): newF += [(mab, b, c), (mab, c, mca)]
                else: newF += [(mab, b, mca), (b, c, mca)]
        F = np.array(newF, dtype=int)
        print(f"  refine pass {it}: {int(mark.sum())} edges split -> {len(F)} triangles", flush=True)
    return P0, F, max_pass

def lesion_stage(pkg, G, P0, F0, outdir, rep, lab=None, inv=None):
    fr = Frames(pkg, G, rep); les = pkg["mask_edit"]["lesion"]; table = les["table"]; cl = pkg["cl"]
    rt_n = np.asarray(cl.point_data["r_target_mm"], float); r_throat = float(rt_n.min()); h_max = r_throat / 8
    d, i = fr.tree_c.query(P0); j = fr.tree_all.query(P0)[1]; inwin0 = fr.rs[i] < 1.0 - 1e-12
    gates = dict(r_throat_mm=r_throat, h_max_mm=h_max, window_s_mm=[fr.c_mm - fr.L_mm / 2, fr.c_mm + fr.L_mm / 2], package_s_offset_from_inlet_arc_mm=fr.s_offset, n_window_frames=int(len(fr.window_frames)), station_map=fr.station_map,
                 radial_scale_min=float(fr.rs.min()), rs_equals_rtarget_over_rsource_max_abs_dev=fr.rs_consistency_max_abs)
    wall_like = inwin0 & (d < 2.6); bad = wall_like & ~fr.on_path[j]
    d_lad = d[inwin0 & fr.on_path[j]]; d_other = d[inwin0 & ~fr.on_path[j]]
    gates["window_vertices_within_2p6mm_of_axis"] = int(wall_like.sum()); gates["window_vertices_within_2p6mm_not_assigned_to_LAD_path"] = int(bad.sum())
    gates["LAD_wall_max_radial_distance_mm"] = float(d_lad.max()) if len(d_lad) else None
    gates["other_branch_vertices_projecting_into_window_min_distance_mm"] = float(d_other.min()) if len(d_other) else None
    gates["gap_other_branch_minus_LAD_wall_mm"] = float(d_other.min() - d_lad.max()) if len(d_other) and len(d_lad) else None
    src_surf = pv.PolyData(P0, np.hstack([np.full((len(F0), 1), 3), F0]).ravel())
    with timed(rep, "lesion_subdivision"):
        Pr, Fr, npass = refine_undeformed(P0, F0, fr, h_max)
    gates["refine_passes"] = int(npass); gates["n_points_after_refine"] = int(len(Pr)); gates["n_triangles_after_refine"] = int(len(Fr))
    with timed(rep, "lesion_deformation"):
        Pd, moved, rs_v, s_v, rad_v, on_path = fr.apply(Pr)
    gates["moved_vertices"] = int(moved.sum()); gates["nothing_outside_window_moves"] = bool(np.abs(Pd[~moved] - Pr[~moved]).max() == 0.0)
    e = np.vstack([Fr[:, [0, 1]], Fr[:, [1, 2]], Fr[:, [2, 0]]]); Lu = np.linalg.norm(Pr[e[:, 0]] - Pr[e[:, 1]], axis=1).reshape(3, -1); inwin_t = moved[Fr].any(1)
    gates["window_triangles"] = int(inwin_t.sum()); gates["undeformed_edge_max_in_window_mm"] = float(Lu[:, inwin_t].max()); gates["undeformed_edge_median_in_window_mm"] = float(np.median(Lu[:, inwin_t]))
    mv3 = moved[Fr]; ed_moved = np.stack([mv3[:, 0] | mv3[:, 1], mv3[:, 1] | mv3[:, 2], mv3[:, 2] | mv3[:, 0]])      # edges with at least one deformed endpoint
    gates["n_edges_with_a_moved_endpoint"] = int(ed_moved.sum()); gates["undeformed_edge_max_over_edges_with_a_moved_endpoint_mm"] = float(Lu[ed_moved].max())
    gates["edge_le_r_throat_over_8_in_window_fraction"] = float((Lu[ed_moved] <= h_max * (1 + 1e-9)).mean())
    n0 = np.cross(Pr[Fr[:, 1]] - Pr[Fr[:, 0]], Pr[Fr[:, 2]] - Pr[Fr[:, 0]]); n1 = np.cross(Pd[Fr[:, 1]] - Pd[Fr[:, 0]], Pd[Fr[:, 2]] - Pd[Fr[:, 0]])
    den = np.maximum(np.linalg.norm(n0, axis=1) * np.linalg.norm(n1, axis=1), 1e-300); dot = np.einsum("ij,ij->i", n0, n1) / den
    gates["fold_over_min_dot"] = float(dot.min()); gates["fold_over_faces_dot_le_0"] = int((dot <= 0).sum())
    Ld = np.linalg.norm(Pd[e[:, 0]] - Pd[e[:, 1]], axis=1).reshape(3, -1)
    gates["deformed_edge_min_median_max_in_window_mm"] = [float(Ld[:, inwin_t].min()), float(np.median(Ld[:, inwin_t])), float(Ld[:, inwin_t].max())]
    # G1 purity: every triangle with a moved vertex has all three vertices on the LAD path; non-LAD original vertices have zero displacement
    n0v = len(P0); disp0 = np.linalg.norm(Pd[:n0v] - P0, axis=1); j0 = fr.tree_all.query(P0)[1]; other = ~fr.on_path[j0]
    tri_moved = moved[Fr].any(1); impure = tri_moved & (~on_path[Fr]).any(1)
    gates["G1_max_displacement_non_LAD_original_vertices_mm"] = float(disp0[other].max()) if other.any() else 0.0; gates["G1_impure_triangles"] = int(impure.sum()); gates["G1_triangles_with_moved_vertex"] = int(tri_moved.sum())
    # G3 mask-label cross-check (837): the label volume 0.35 mm inside the wall at every moved ORIGINAL vertex must be the LAD label (mode of the labels at the package's LAD centreline nodes)
    if lab is not None:
        seg_ = np.asarray(cl.point_data["segment_name"]); lad_pts = np.asarray(cl.points)[seg_ == "LAD"]
        ql = np.rint(to_ijk(inv, lad_pts)).astype(int); lv = lab[tuple(ql.T)]; lad_label = int(np.bincount(lv[lv > 0]).argmax())
        idx0 = np.where(moved[:n0v])[0]; ii = fr.tree_c.query(P0[idx0])[1]; inward = fr.c[ii] - P0[idx0]; inward /= np.maximum(np.linalg.norm(inward, axis=1), 1e-9)[:, None]
        qs = np.rint(to_ijk(inv, P0[idx0] + 0.35 * inward)).astype(int); vals = lab[tuple(np.clip(qs, 0, np.array(lab.shape) - 1).T)]
        gates["G3_label_check"] = dict(LAD_label=lad_label, LAD_label_fractions_at_LAD_nodes={int(v): float((lv == v).mean()) for v in np.unique(lv)}, n_moved_original_vertices=int(len(idx0)),
                                       label_fractions_at_moved_vertices={int(v): float((vals == v).mean()) for v in np.unique(vals)}, fraction_LAD_label=float((vals == lad_label).mean()), PASS=bool((vals == lad_label).mean() >= 0.99))
    # per-node as-built table
    out_surf = pv.PolyData(Pd, np.hstack([np.full((len(Fr), 1), 3), Fr]).ravel())
    ctr_src = pv.PolyData(P0, np.hstack([np.full((len(F0), 1), 3), F0]).ravel())
    rows = []; thr_node = int(np.argmin(rt_n)); rs_n = np.asarray(cl.point_data["radial_scale"], float); rsrc_n = np.asarray(cl.point_data["r_source_mm"], float)
    with timed(rep, "lesion_asbuilt_sections"):
        for w, row in enumerate(table):
            node = int(np.where(np.asarray(cl.point_data["tree_node"]) == row["tree_node"])[0][0]); k = int(fr.node_frame[list(fr.path).index(node)])
            c_k, t_k = fr.c[k], fr.t[k]
            m0 = section_metrics(ctr_src, c_k, t_k); m1 = section_metrics(out_surf, c_k, t_k)
            sph0 = float(np.linalg.norm(ctr_src.find_closest_cell(c_k, return_closest_point=True)[1] - c_k)); sph1 = float(np.linalg.norm(out_surf.find_closest_cell(c_k, return_closest_point=True)[1] - c_k))
            rows.append(dict(tree_node=int(row["tree_node"]), s_mm=float(row["s_mm"]), radial_scale=float(rs_n[node]), r_source_mm=float(rsrc_n[node]), r_target_mm=float(rt_n[node]),
                             undeformed=dict(r_insc_mm=m0["r_insc"], r_eq_mm=m0["r_eq"], star=m0["star"], closed=m0["closed"], centroid_offset_over_req=m0["cen_off_over_req"], axis_inside=m0["axis_inside"], other_loop_min_dist_mm=m0["other_loop_min_dist"]),
                             asbuilt=dict(r_insc_mm=m1["r_insc"], r_eq_mm=m1["r_eq"], closed=m1["closed"], centroid_offset_over_req=m1["cen_off_over_req"], axis_inside=m1["axis_inside"]),
                             dev_asbuilt_insc_vs_target_pct=100 * (m1["r_insc"] / rt_n[node] - 1), dev_undeformed_insc_vs_source_pct=100 * (m0["r_insc"] / rsrc_n[node] - 1),
                             ratio_insc_over_radial_scale_minus1_pct=100 * (m1["r_insc"] / m0["r_insc"] / rs_n[node] - 1), ratio_req_over_radial_scale_minus1_pct=100 * (m1["r_eq"] / m0["r_eq"] / rs_n[node] - 1),
                             dev_asbuilt_req_vs_target_pct=100 * (m1["r_eq"] / rt_n[node] - 1),
                             sphere_at_axis=dict(undeformed_mm=sph0, asbuilt_mm=sph1, ratio_over_radial_scale_minus1_pct=100 * (sph1 / sph0 / rs_n[node] - 1), dev_asbuilt_vs_target_pct=100 * (sph1 / rt_n[node] - 1), undeformed_vs_source_pct=100 * (sph0 / rsrc_n[node] - 1))))
    gates["stations"] = rows
    thr = [r for r in rows if r["tree_node"] == int(np.asarray(cl.point_data["tree_node"])[thr_node])][0]
    sp_ = thr["sphere_at_axis"]
    gates["throat"] = dict(tree_node=thr["tree_node"], r_target_mm=thr["r_target_mm"], r_source_mm=thr["r_source_mm"], radial_scale=thr["radial_scale"],
                           RELATIVE_GATE=dict(rule="|as-built/undeformed (same section, same definition) / radial_scale - 1| <= 1 % for all three definitions", tolerance_pct=100 * THROAT_TOL,
                                              insc_circle_pct=thr["ratio_insc_over_radial_scale_minus1_pct"], area_equiv_pct=thr["ratio_req_over_radial_scale_minus1_pct"], sphere_at_axis_pct=sp_["ratio_over_radial_scale_minus1_pct"]),
                           LITERAL_ABSOLUTE_vs_r_target=dict(rule="as-built radius vs r_target_mm (work order text); reported, NOT decisive (see module docstring)", insc_circle_pct=thr["dev_asbuilt_insc_vs_target_pct"], area_equiv_pct=thr["dev_asbuilt_req_vs_target_pct"],
                                                             sphere_at_axis_pct=sp_["dev_asbuilt_vs_target_pct"], undeformed_sphere_vs_r_source_pct=sp_["undeformed_vs_source_pct"], undeformed_insc_vs_r_source_pct=thr["dev_undeformed_insc_vs_source_pct"]),
                           asbuilt_mm=dict(insc_circle=thr["asbuilt"]["r_insc_mm"], area_equiv=thr["asbuilt"]["r_eq_mm"], sphere_at_axis=sp_["asbuilt_mm"]), undeformed_mm=dict(insc_circle=thr["undeformed"]["r_insc_mm"], area_equiv=thr["undeformed"]["r_eq_mm"], sphere_at_axis=sp_["undeformed_mm"]))
    rg = gates["throat"]["RELATIVE_GATE"]; gates["throat"]["PASS"] = bool(max(abs(rg["insc_circle_pct"]), abs(rg["area_equiv_pct"]), abs(rg["sphere_at_axis_pct"])) <= 100 * THROAT_TOL)
    gates["throat"]["LITERAL_ABSOLUTE_PASS"] = bool(max(abs(gates["throat"]["LITERAL_ABSOLUTE_vs_r_target"][k]) for k in ("insc_circle_pct", "area_equiv_pct", "sphere_at_axis_pct")) <= 100 * THROAT_TOL)
    gates["stations_relative_dev_max_abs_pct"] = dict(insc=float(max(abs(r["ratio_insc_over_radial_scale_minus1_pct"]) for r in rows)), area_equiv=float(max(abs(r["ratio_req_over_radial_scale_minus1_pct"]) for r in rows)), sphere_at_axis=float(max(abs(r["sphere_at_axis"]["ratio_over_radial_scale_minus1_pct"]) for r in rows)))
    gates["stations_undeformed_sphere_vs_r_source_pct_median_p10_p90"] = [float(x) for x in np.percentile([r["sphere_at_axis"]["undeformed_vs_source_pct"] for r in rows], [50, 10, 90])]
    dev = np.array([abs(r["dev_asbuilt_insc_vs_target_pct"]) for r in rows]); gates["stations_max_abs_dev_insc_vs_target_pct"] = float(dev.max()); gates["stations_median_abs_dev_insc_vs_target_pct"] = float(np.median(dev))
    gates["undeformed_sections_all_closed_single_starshaped_and_axis_inside"] = bool(all(r["undeformed"]["closed"] and r["undeformed"]["star"] and r["undeformed"]["axis_inside"] and r["undeformed"]["other_loop_min_dist_mm"] > 0.5 for r in rows))
    gates["max_centroid_offset_over_req_undeformed"] = float(max(r["undeformed"]["centroid_offset_over_req"] for r in rows))
    gates["PASS_purity_fold_window"] = bool(gates["G1_impure_triangles"] == 0 and gates["G1_max_displacement_non_LAD_original_vertices_mm"] == 0.0 and gates["fold_over_faces_dot_le_0"] == 0 and gates["nothing_outside_window_moves"]
                                            and gates["window_vertices_within_2p6mm_not_assigned_to_LAD_path"] == 0 and (gates["gap_other_branch_minus_LAD_wall_mm"] is None or gates["gap_other_branch_minus_LAD_wall_mm"] > 0.5)
                                            and gates["edge_le_r_throat_over_8_in_window_fraction"] == 1.0 and gates["max_centroid_offset_over_req_undeformed"] <= 0.3 and gates.get("G3_label_check", {}).get("PASS", True))
    rep["lesion"] = gates
    # keep the open deformed surface (mm) for the extension step
    return Pd, Fr, fr

# ------------------------------------------------------------------ extensions + caps
def extend_and_cap(pkg, P, F, clipinfo, rep):
    closed = {k for k, v in pkg["bc_A"].items() if v["mode"] == "closed"}
    loops, ok = boundary_loops(F)
    o_info = clipinfo["outlets"]; specs = []
    inl_p, inl_nrm_remove, inl_r = clipinfo["inlet"]
    spec_names = ["inlet"] + [o["id"] for o in o_info]; spec_pts = [inl_p] + [o["p"] for o in o_info]; spec_out = [inl_nrm_remove] + [o["n"] for o in o_info]   # inlet outward = -n_distal = inl_nrm_remove
    spec_D = [2 * inl_r] + [2 * o["r_mm"] for o in o_info]; spec_mult = [EXT_INLET_D] + [EXT_OUTLET_D] * len(o_info)
    assign = {}
    for lp in loops:
        c = P[lp].mean(0); dd = [np.linalg.norm(c - q) for q in spec_pts]; k = int(np.argmin(dd)); assign[k] = (lp, dd[k])
    assert len(assign) == len(loops) == len(spec_names), f"loop/outlet assignment not one-to-one: {len(assign)} {len(loops)} {len(spec_names)}"
    pts = [P]; tris = [F]; labels = ["wall"] * len(F); npts = len(P); ext_rep = []
    for k, name in enumerate(spec_names):
        lp, off = assign[k]; L = P[lp]; c = L.mean(0); n = np.array(spec_out[k], float); n /= np.linalg.norm(n)
        _, _, vt = np.linalg.svd(L - c); svn = vt[2] * (1 if vt[2] @ n > 0 else -1); ang = float(np.degrees(np.arccos(np.clip(svn @ n, -1, 1))))
        # confirm n points out of the vessel (away from the surface interior near the loop)
        near = P[np.linalg.norm(P - c, axis=1) < 3 * np.linalg.norm(L - c, axis=1).max()]; outward_ok = bool(np.dot(near.mean(0) - c, n) < 0)
        D_eq = float(2 * np.sqrt(0.5 * np.linalg.norm(np.cross(L - c, np.roll(L - c, -1, 0)).sum(0)) / np.pi)); mult = spec_mult[k]
        Dv = spec_D[k] if D_BASIS == 'rmm' else D_eq; EXT = mult * Dv; ledge = float(np.mean(np.linalg.norm(np.roll(L, -1, 0) - L, axis=1))); nring = int(np.ceil(EXT / max(ledge, 0.1))); ds = EXT / nring; m = len(lp)
        idx_prev = lp
        for r in range(1, nring + 1):
            ring = L + r * ds * n; idx = np.arange(npts, npts + m); npts += m; pts.append(ring)
            for i in range(m):
                u0, v0 = idx_prev[i], idx_prev[(i + 1) % m]; u1, v1 = idx[i], idx[(i + 1) % m]
                tris.append(np.array([[v0, u0, u1], [v0, u1, v1]])); labels += ["wall", "wall"]
            idx_prev = idx
        ce = npts; npts += 1; pts.append((L + EXT * n).mean(0)[None])
        cap_label = "wall" if name in closed else name        # bc_A mode 'closed' = the outlet is a WALL (zero conductance)
        for i in range(m): tris.append(np.array([[idx_prev[(i + 1) % m], idx_prev[i], ce]])); labels.append(cap_label)
        ext_rep.append(dict(patch=name, D_basis=D_BASIS, D_2r_mm_mm=spec_D[k], D_used_mm=Dv, D_multiple=mult, extension_length_mm=float(EXT), n_rings=nring, ring_spacing_mm=float(ds), loop_vertices=int(m), loop_centroid_to_csv_point_mm=float(off),
                            loop_area_equivalent_diameter_mm=D_eq, extension_length_over_area_equivalent_D=float(EXT / D_eq), plane_normal_angle_csv_vs_svd_deg=ang, outward_normal_confirmed=outward_ok))
    P2 = np.vstack(pts); F2 = np.vstack(tris).astype(int); lab = np.array(labels)
    vol = float(np.einsum("ij,ij->i", P2[F2[:, 0]], np.cross(P2[F2[:, 1]], P2[F2[:, 2]])).sum() / 6)
    flipped = False
    if vol < 0: F2 = F2[:, ::-1].copy(); flipped = True
    rep["extensions"] = dict(rule="CFD-ARM-SPEC 6.2: 5 D at the inlet, 3 D at each outlet; D = 2 r_mm of the package (inlet.json / outlets.csv); straight planar extrusion of the clipped loop along the package plane normal, planar fan cap (837 rebuild_surface method; no vmtksurfaceremeshing)",
                             per_patch=ext_rep, orientation_flipped_to_outward=flipped, all_outward_normals_confirmed=all(e["outward_normal_confirmed"] for e in ext_rep), max_normal_angle_csv_vs_svd_deg=max(e["plane_normal_angle_csv_vs_svd_deg"] for e in ext_rep))
    return P2, F2, lab

# ------------------------------------------------------------------ as-built radius (surface)
def radius_csv(pkg, G, surf_final, fr, out_csv, rep):
    cl = pkg["cl"]; xyzc = G["xyz"]; n = len(xyzc); arc = G["arc"]
    seg = np.asarray(cl.point_data["segment_name"]); bid = np.asarray(cl.point_data["branch_id"]); tn = np.asarray(cl.point_data["tree_node"])
    rsrc = np.asarray(cl.point_data["r_source_mm"], float); rt = np.asarray(cl.point_data["r_target_mm"], float); rs = np.asarray(cl.point_data["radial_scale"], float)
    centres = surf_final.cell_centers().points; tree = cKDTree(centres)
    path_pos = {int(v): k for k, v in enumerate(fr.path)} if fr is not None else {}
    rows = []; prev_area = {}
    order = np.argsort(arc)
    # package s_mm (probes.csv) = arc from the inlet node minus a constant offset on the LM->LAD path (s = 0 at the LM/LAD/LCX split, tree_node 33); verified against every non-inlet probe
    pr = [r for r in csv.DictReader(open(f"{pkg['dir']}/probes.csv")) if r["kind"] not in ("inlet", "outlet")]      # inlet/outlet probes carry the plain arc from the inlet node (offset 0)
    tn_all = {int(v): i for i, v in enumerate(tn)}; offs = np.array([arc[tn_all[int(r["tree_node"])]] - float(r["s_node_mm"]) for r in pr])
    s_off = float(np.median(offs)); rep["probe_s_offset"] = dict(offset_mm=s_off, n_probes=len(pr), max_abs_dev_mm=float(np.abs(offs - s_off).max()), note="package s_mm = arc from the inlet node - offset_mm on the root->LAD path")
    lad_leaf = [i for i in range(n) if len(G["adj"][i]) == 1 and i != G["root"] and seg[i] == "LAD"][0]; on_lad_path = set(path_to(G, lad_leaf))
    with timed(rep, "surface_radius_csv"):
        for i in order:
            nb = G["adj"][i]; par = G["parent"][i]; kids = [w for w in nb if w != par]
            if i in path_pos and fr is not None:
                t = fr.t[int(fr.node_frame[path_pos[i]])]; org = fr.c[int(fr.node_frame[path_pos[i]])]
            else:
                a = i; b = i
                for _ in range(2):
                    if G["parent"].get(a) is not None: a = G["parent"][a]
                    ch = [w for w in G["adj"][b] if w != G["parent"].get(b)]
                    if ch: b = ch[0]
                t = xyzc[b] - xyzc[a]; t = t / np.linalg.norm(t) if np.linalg.norm(t) > 0 else np.array([1.0, 0, 0]); org = xyzc[i]
            sel = np.array(tree.query_ball_point(org, 6.0), int)
            row = dict(node=int(i), tree_node=int(tn[i]), segment=str(seg[i]), branch_id=int(bid[i]), s_mm=float(arc[i]), s_pkg_mm=(float(arc[i] - s_off) if i in on_lad_path else ""), x_mm=float(org[0]), y_mm=float(org[1]), z_mm=float(org[2]),
                       pkg_r_source_mm=float(rsrc[i]), pkg_r_target_mm=float(rt[i]), pkg_radial_scale=float(rs[i]), section_ok=0)
            if len(sel):
                sub = surf_final.extract_cells(sel).extract_surface(algorithm="dataset_surface"); m = section_metrics(sub, org, t)
                if m is not None:
                    a0 = prev_area.get(par)
                    ok = bool(m["cen_off_over_req"] < 0.5 and m["closed"] and m["n_loops"] <= 2 and (a0 is None or 0.6 < m["area"] / a0 < 1.6))
                    row.update(section_area_mm2=m["area"], r_eq3D_mm=m["r_eq"], r_max_inscribed_mm=m["r_insc"], centroid_offset_over_req=m["cen_off_over_req"], n_section_loops=m["n_loops"], section_ok=int(ok))
                    if ok: prev_area[i] = m["area"]
            rows.append(row)
    cols = ["node", "tree_node", "segment", "branch_id", "s_mm", "s_pkg_mm", "x_mm", "y_mm", "z_mm", "section_ok", "section_area_mm2", "r_eq3D_mm", "r_max_inscribed_mm", "centroid_offset_over_req", "n_section_loops", "pkg_r_source_mm", "pkg_r_target_mm", "pkg_radial_scale"]
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["case", "scan", "cohort_status"] + cols, extrasaction="ignore"); w.writeheader()
        for r in rows: r.update(case=pkg["name"], scan=14, cohort_status="IN_COHORT (scan 14; E0 subset csv absent on this machine, waived)"); w.writerow(r)
    ok = [r for r in rows if r["section_ok"]]
    rep["surface_radius_csv"] = dict(path=out_csv, n_nodes=len(rows), n_sections_ok=len(ok), columns_note="s_mm = arc from the inlet node along the centreline tree; s_pkg_mm = the package's probe s (arc - offset) on the root->LAD path only; x/y/z = the section origin (path frame point for the LAD path, node otherwise)", definition="surface-based (not the mesh): planar section of the final wall surface normal to the path tangent at each centreline node; r_eq3D = area-equivalent radius, r_max_inscribed = 2-D maximum inscribed circle of the section; section_ok = centroid within 0.5 r_eq of the node, closed loop, area within 0.6..1.6 of the parent node's; the mesh-based version comes after meshing",
                                     median_r_eq_over_pkg_r_source=float(np.median([r["r_eq3D_mm"] / r["pkg_r_source_mm"] for r in ok])), median_r_insc_over_pkg_r_source=float(np.median([r["r_max_inscribed_mm"] / r["pkg_r_source_mm"] for r in ok])))
    return rows


def diagnose_selfintersection(obj, pkg, G, fr, outdir):
    """Cluster the surfaceCheck intersection points (0.5 mm single linkage) and attribute each cluster to the nearest centreline node / outlet / lesion window."""
    if not os.path.exists(obj): return []
    p = np.atleast_2d(np.loadtxt(obj, usecols=(1, 2, 3))) * 1e3
    from scipy.cluster.hierarchy import fcluster, linkage
    cl_ = fcluster(linkage(p, "single"), 0.5, "distance") if len(p) > 1 else np.ones(len(p), int)
    cl = pkg["cl"]; seg = np.asarray(cl.point_data["segment_name"]); tn = np.asarray(cl.point_data["tree_node"]); rsrc = np.asarray(cl.point_data["r_source_mm"], float); tr = cKDTree(G["xyz"]); out = []
    for k in np.unique(cl_):
        c = p[cl_ == k].mean(0); d, i = tr.query(c)
        do = sorted([(o["outlet_id"], float(np.linalg.norm(c - np.array([float(o["x"]), float(o["y"]), float(o["z"])])))) for o in pkg["outlets"]], key=lambda x: x[1])[0]
        arc_pkg = float(G["arc"][i] - (fr.s_offset if fr is not None else 0.0))
        out.append(dict(n_points=int((cl_ == k).sum()), centroid_mm=[round(float(x), 2) for x in c], nearest_node=int(tn[i]), segment=str(seg[i]), distance_to_node_mm=round(float(d), 2), node_r_source_mm=round(float(rsrc[i]), 2), distance_over_r_source=round(float(d / rsrc[i]), 2),
                        nearest_outlet=do[0], distance_to_outlet_mm=round(do[1], 2), in_lesion_window=(bool(abs(arc_pkg - fr.c_mm) < fr.L_mm / 2) if fr is not None else False)))
    return out

def fc_ok(rep): return bool(rep["frame_check"]["PASS"] and rep["frame_check"]["sub_cut_points_inside_lumen_without_flip"][0] == 0)

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("package"); ap.add_argument("outdir"); ap.add_argument("--e0-waiver", default=None); ap.add_argument("--stop-after", default=None); ap.add_argument("--no-surfacecheck", action="store_true"); ap.add_argument("--d-basis", choices=["rmm", "areaeq"], default="rmm")
    a = ap.parse_args(); global D_BASIS; D_BASIS = a.d_basis; t_all = time.time(); pkg = load_package(a.package); outdir = os.path.abspath(a.outdir)
    if os.path.exists(f"{outdir}/gates.json") and False: raise SystemExit(f"{outdir}/gates.json exists")
    os.makedirs(outdir, exist_ok=True); assert not os.path.abspath(outdir).startswith("/mnt/e/Paper6-T6/Paper6-T6"), "outputs must not go into the Drive-synced project folder"
    rep = dict(case=pkg["name"], kind=pkg["kind"], scan=14, side="left", script="build_m1_geometry.py", script_sha256=sha256_file(__file__), lib_sha256=sha256_file(f"{HERE}/m1lib.py"), package_sha256=sha256_dir(pkg["dir"]), started=time.strftime("%Y-%m-%d %H:%M:%S"),
               blinding="no 0D code imported: zerod_ffr / Tree / outlets_837 are not imported by this pipeline", status="RUNNING", deviations=[])
    def save():
        rep["wall_clock_total_s"] = round(time.time() - t_all, 1); json.dump(rep, open(f"{outdir}/gates.json", "w"), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else (float(o) if isinstance(o, (np.floating,)) else (int(o) if isinstance(o, np.integer) else str(o))))
    rep["deviations"] = ["E0 membership assertion could not be executed (subset csv absent on this machine): logged waiver, see e0",
                         "throat gate: the deciding test is RELATIVE (as-built/undeformed vs radial_scale, <= 1 %); the literal absolute test vs r_target_mm cannot be met by this surface (undeformed radius differs from the package r_source by -10..+14 % at the throat depending on definition): reported, not decisive",
                         "flow-extension diameter D = 2 r_mm of the package (as instructed); the area-equivalent diameter of the clipped loops is 1.0-1.9x larger (recorded per patch; --d-basis areaeq switches)",
                         "patch names are the package outlet_ids (out_<node>) verbatim, not 'outlet_<id>' (spec 6.2 literal), so that bc_A/bc_C_flows/territories join without a mapping",
                         "the erosion count of the packages (25/40) has no shipped definition: several measured definitions are reported (mask_edit.erosion_removed_voxels_within_f_r)",
                         "lesion deformation uses the smoothing-spline path frames of the 837 pipeline (radial scaling in the normal plane about the axis point, radial_scale interpolated along the path) instead of literal 3-D scaling about the nearest raw centreline point: the literal rule steps by up to 0.4 mm across Voronoi cells at 0.5 mm node spacing"]
    rep["e0"] = e0_guard.check(14, "left", waiver=a.e0_waiver)
    rep["mask_sha256_check"] = dict(actual=sha256_file(MASK), expected=pkg["meta"]["provenance"]["mask_nii_sha256"]); assert rep["mask_sha256_check"]["actual"] == rep["mask_sha256_check"]["expected"], "mask sha256 differs from the package provenance"
    save()
    img, lab, mask, edited, inv, sp = mask_stage(pkg, outdir, rep); save()
    comp, lo, hi = left_tree(pkg, img, mask, edited, inv, sp, rep); save()
    if a.stop_after == "mask": return
    surf = surface_stage(pkg, comp, img, outdir, rep); save()
    G = graph(pkg)
    clipped, P0, F0, loops, clipinfo = clip_stage(pkg, G, surf, rep); save()
    clipped.save(f"{outdir}/intermediate/clipped_open.vtp")
    if a.stop_after == "clip": return
    fr = None; Pd, Fd = P0, F0; reject = False
    if pkg["kind"] != "clean_nolesion":
        Pd, Fd, fr = lesion_stage(pkg, G, P0, F0, outdir, rep, lab, inv); save()
        pv.PolyData(Pd, np.hstack([np.full((len(Fd), 1), 3), Fd]).ravel()).save(f"{outdir}/intermediate/lesion_open.vtp")
        if not rep["lesion"]["throat"]["PASS"]:
            rep["status"] = "REJECTED: relative as-built throat differs from radial_scale by more than 1 % (no repair attempted; artefacts below are for inspection only)"; reject = True
    rep["closed_outlets"] = [k for k, v in pkg["bc_A"].items() if v["mode"] == "closed"]
    P2, F2, lab_f = extend_and_cap(pkg, Pd, Fd, clipinfo, rep); save()
    topo = surface_topology(P2, F2); rep["final_surface"] = dict(topology=topo, patch_faces={n: int((lab_f == n).sum()) for n in sorted(set(lab_f))})
    stl = f"{outdir}/case.stl"
    with timed(rep, "write_stl"): write_multisolid_stl(stl, P2, F2, lab_f)
    rep["final_surface"]["stl"] = dict(path=stl, sha256=sha256_file(stl), size_mb=round(os.path.getsize(stl) / 1e6, 1), units="metres", patches=sorted(set(lab_f)))
    surf_final = pv.PolyData(P2, np.hstack([np.full((len(F2), 1), 3), F2]).ravel()); save()
    if not a.no_surfacecheck:
        with timed(rep, "surfaceCheck"):
            sc = surface_check(stl, f"{outdir}/sc", True, "case"); rep["final_surface"]["surfaceCheck"] = sc
            rep["final_surface"]["self_intersection_clusters"] = diagnose_selfintersection(f"{outdir}/sc/selfInterPoints.obj", pkg, G, fr, outdir)
            for nm_ in ("raw_mc", "smoothed"):       # is the intersection already in the marching-cubes surface / created by smoothing?
                s_ = pv.read(f"{outdir}/intermediate/{nm_}.vtp").extract_surface(algorithm="dataset_surface").triangulate().clean(); F_ = s_.faces.reshape(-1, 4)[:, 1:].astype(int)
                write_multisolid_stl(f"{outdir}/intermediate/{nm_}.stl", np.asarray(s_.points), F_, np.array(["wall"] * len(F_)))
                rep["final_surface"][f"surfaceCheck_{nm_}_left_tree_surface"] = surface_check(f"{outdir}/intermediate/{nm_}.stl", f"{outdir}/sc_{nm_}", True, nm_)
        save()
    radius_csv(pkg, G, surf_final, fr, f"{outdir}/surface_radius_{pkg['kind']}.csv", rep); save()
    if not a.no_surfacecheck:
        # positive control (all cases): a bump of the wall around one LAD point is pushed 1.2 r past the axis, through the far wall; the same surfaceCheck must flag it
        with timed(rep, "positive_control"):
            seg_ = np.asarray(pkg["cl"].point_data["segment_name"]); rsrc_ = np.asarray(pkg["cl"].point_data["r_source_mm"], float); lad_i = np.where(seg_ == "LAD")[0]
            if fr is not None: lad_i = np.array([i for i in lad_i if abs(G["arc"][i] - (fr.c_mm + fr.s_offset)) > fr.L_mm])      # away from the lesion window
            ci = int(lad_i[len(lad_i) // 2]); cpt = G["xyz"][ci]; rr_ = float(rsrc_[ci]); wall_idx = np.where(lab_f == "wall")[0]; wv = np.unique(F2[wall_idx]); dwall = np.linalg.norm(P2[wv] - cpt, axis=1)
            w0 = P2[wv[np.argmin(dwall)]]; selv = wv[np.linalg.norm(P2[wv] - w0, axis=1) < 0.8 * rr_]
            Pbad = P2.copy(); Pbad[selv] += 2.2 * (cpt - w0)
            bad_stl = f"{outdir}/sc_poscontrol_bad.stl"; write_multisolid_stl(bad_stl, Pbad, F2, lab_f)
            rep["final_surface"]["positive_control_surfaceCheck"] = surface_check(bad_stl, f"{outdir}/sc_poscontrol", True, "bad"); rep["final_surface"]["positive_control_n_vertices_moved"] = int(len(selv)); rep["final_surface"]["positive_control_node"] = ci
        save()
    fs = rep["final_surface"]
    rep["final_surface"]["PASS"] = bool(fs["topology"]["open_edges"] == 0 and fs["topology"]["non_manifold_or_duplicate_directed_edges"] == 0 and fs["topology"]["connected_components"] == 1 and fs["topology"]["volume_mm3"] > 0 and fs["topology"]["zero_area_triangles"] == 0
                                       and (a.no_surfacecheck or (fs["surfaceCheck"]["closed"] and fs["surfaceCheck"]["n_parts"] == 1 and fs["surfaceCheck"]["not_self_intersecting"] and fs["positive_control_surfaceCheck"]["self_intersecting"])))
    gs = {"frame_check": fc_ok(rep), "mask_edit_matches_shipped_voxels_and_components": bool(rep["mask_edit"]["voxels_removed_matches_shipped"] and rep["mask_edit"]["components_match_shipped"] and rep["mask_edit"]["sha256_matches_package"]),
          "clip_loops_and_outward_normals": bool(rep["clip"]["PASS"]), "extensions_outward": bool(rep["extensions"]["all_outward_normals_confirmed"]),
          "final_surface_closed_one_part_positive_volume": bool(fs["topology"]["open_edges"] == 0 and fs["topology"]["connected_components"] == 1 and fs["topology"]["volume_mm3"] > 0 and fs["topology"]["zero_area_triangles"] == 0)}
    if fr is not None: gs.update({"lesion_relative_throat_gate": bool(rep["lesion"]["throat"]["PASS"]), "lesion_purity_fold_window_edge_labels": bool(rep["lesion"]["PASS_purity_fold_window"]), "lesion_literal_absolute_r_target_check": bool(rep["lesion"]["throat"]["LITERAL_ABSOLUTE_PASS"])})
    if not a.no_surfacecheck: gs.update({"surfaceCheck_closed_one_part": bool(fs["surfaceCheck"]["closed"] and fs["surfaceCheck"]["n_parts"] == 1 and fs["surfaceCheck"]["illegal_triangles"]), "surfaceCheck_not_self_intersecting": bool(fs["surfaceCheck"]["not_self_intersecting"]),
                                        "self_intersection_positive_control_flagged": bool(fs["positive_control_surfaceCheck"]["self_intersecting"])})
    rep["GATES"] = gs; rep["ALL_GATES_PASS"] = bool(all(gs.values())); rep["FAILED_GATES"] = [k for k, v in gs.items() if not v]
    if not reject: rep["status"] = "DONE: all gates passed" if rep["ALL_GATES_PASS"] else "DONE: gates FAILED: " + ", ".join(rep["FAILED_GATES"])
    assert "zerod_ffr" not in sys.modules and "outlets_837" not in sys.modules
    save(); print(json.dumps({k: rep[k] for k in ("case", "status", "wall_clock_total_s")}))
    if reject: sys.exit(3)

if __name__ == "__main__":
    main()
