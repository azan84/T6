"""Bounded probe planes for the D8 monitors (work order 2026-10-03 D8, Task C). No 0D code.
Why: a pointAndNormal sampledPlane WITHOUT limits cuts every vessel of the tree that crosses the infinite plane (the infinite-plane throatP/throatFlux/Re_throat defect of the 09-26 return).
Fix: OpenFOAM ESI v2406 sampledPlane has the optional keyword `bounds` (src/sampling/sampledSurface/sampledPlane/sampledPlane.{H,C}: bounds_(dict.getOrDefault("bounds", boundBox::null()));
src/sampling/surface/cutting/cuttingSurfaceBaseSelection.C: only cells whose CELL CENTRE lies inside the axis-aligned box are cut). The monitors therefore cut only the cells with centres in a box around the probe.
Box (axis-aligned cube, half-width h, centred on the probe point), sized from the package (probes.csv r_ref_mm, centreline.vtp radii and the tree):
  r_own = lumen radius of the centreline at the probe's tree_node (r_target_mm: the lesioned lumen at a throat; = r_ref_mm elsewhere), a_own = r_own/|cos| (|cos| = |n . tangent| of the centreline at the probe),
  h_min = 1.3 a_own + 0.3 mm (the as-meshed lumen is wider than the package radius, D10; one cell of margin), h_pref = max(2 r_ref, h_min),
  every OTHER crossing of the infinite plane by the centreline (edges that cross it, or pass within their radius of it), with the section semi-axis a = min(r/|cos|, 5 r), must stay outside the box:
  h_clear = min over them of (L_inf distance probe -> crossing - a) - 0.2 mm;  h = min(h_pref, h_clear); refuse if h < h_min.
Mesh CHECK (authoritative, pyvista on the actual polyMesh; the builder refuses the case if it fails): the plane is cut through the cells around the probe; on the resulting section
  (1) the cut cells whose centres are in the box form exactly ONE connected component, the one nearest the probe (no other vessel inside the box);
  (2) that component lies wholly inside the box (the box does not clip the lumen section), with a margin of >= 0.5 local cell sizes for the centres (pyvista centre = point mean, OpenFOAM centre = centroid);
  (3) every cut cell of any other component has its centre outside the box by >= 0.5 local cell sizes;
  (4) area of the bounded section within [0.4, 2.5] x pi r_own^2 and its centroid within 0.5 r_eq of the probe.
If the first box fails (1)/(3), h is reduced (x 0.85) down to h_min; if it fails (2), h is increased (x 1.15) up to h_clear; every attempt is recorded.
STRICT MEASUREMENT-SECTION RULE (audit 2026-10-03 Sol finding 2; applied to the measurement probe, recorded but not enforced for the throat probe): the section must be a SINGLE-LUMEN section:
  (S1) the plane normal is within MAX_ANGLE_DEG = 20 deg of the local centreline tangent (tangent = chord of the lesion-vessel path over +-0.5 mm of arc around the probe; the path is root -> probe node, continued distally
       along the child of the same branch_id);
  (S2) no bifurcation within BIF_CLEAR_FACTOR * r_ref = 1.5 r_ref of the probe along that path: every centreline node within that arc distance (and the probe node) has tree degree 2;
  (S3) the mesh check above passes (exactly one connected component in the box, not clipped, no other vessel in the box);
  (S4) the bounded section area is within a factor AREA_FACTOR_STRICT = 1.6 of pi r_ref^2 on both sides (r_ref = probes.csv r_ref_mm): 1/1.6 <= A/(pi r_ref^2) <= 1.6.
  Thresholds (from the scan-14 values): the measurement section of scan 14 is 1.25 x pi r_own^2 (r_own = r_ref there), the as-meshed lumen is about 20 % wider than the package radius (D10, area factor 1.44; the
  throat section, 1.43 x pi r_target^2, is the extreme case): 1.6 leaves 11 % on the area above 1.44 and rejects a cut through two vessels (>= about 2x) and a 45-deg oblique cut of a 20 %-wide lumen
  (1.44/cos 45 = 2.0); 1/1.6 = 0.625 rejects a clipped or partial section (the as-meshed lumen is not narrower than the package). 20 deg keeps the oblique-cut area excess below 1/cos 20 - 1 = 6.4 %; scan 14 and four
  P5 packages have 2.6-10.2 deg. 1.5 r_ref keeps the section's own disc (radius r_ref/cos) away from the bifurcation's flow divider.
  If the package probe fails (S1)-(S4) the builder records FAILED_SECTION_RULE (never silently accepted) and RELOCATES the measurement section deterministically: candidates are the centreline nodes of the same path
  (proximal ancestors and the distal same-branch continuation) within RELOC_MAX_MM = 3 mm of arc, ordered by |arc distance| (ties: distal first); the plane of a candidate is centred on the node with the local path
  tangent as normal and r_ref = the centreline r_ref_mm at that node; the first candidate passing (S1)-(S4) (S3/S4 only when a mesh is given) is used for measurementFlux/measurementP. The package probe plane is kept as
  measurementOrigFlux/measurementOrigP when its bounded section passes the mesh check (S3; else no original monitor). No valid candidate within 3 mm: the builder refuses."""
import os, tempfile, shutil
import numpy as np

AREA_FACTOR = (0.4, 2.5)
MAX_ANGLE_DEG, BIF_CLEAR_FACTOR, AREA_FACTOR_STRICT, RELOC_MAX_MM, TANGENT_HALF_MM = 20.0, 1.5, 1.6, 3.0, 0.5
H_MIN_FACTOR, H_MIN_ADD_MM, H_PREF_FACTOR, CLEAR_MARGIN_MM = 1.3, 0.3, 2.0, 0.2

def _radius_field(cl):
    return "r_target_mm" if "r_target_mm" in cl.point_data.keys() else "r_ref_mm"

def plane_crossings(cl, p_mm, n):
    """all places where the centreline meets the infinite plane (point p_mm, unit normal n): list of dict(x_mm, r_mm, cos, a_mm, edge, branch_id, segment)"""
    X = np.asarray(cl.points, float); r = np.asarray(cl.point_data[_radius_field(cl)], float)
    br = np.asarray(cl.point_data["branch_id"]) if "branch_id" in cl.point_data.keys() else np.zeros(len(X), int)
    seg = np.asarray(cl.point_data["segment_name"]) if "segment_name" in cl.point_data.keys() else np.array([""] * len(X))
    L = np.asarray(cl.lines).reshape(-1, 3)[:, 1:]; d = (X - p_mm) @ n; out = []
    for a, b in L:
        t_ = X[b] - X[a]; ln = np.linalg.norm(t_)
        if ln == 0: continue
        c = abs(float(t_ @ n) / ln); re = max(r[a], r[b])
        if d[a] * d[b] <= 0 and d[a] != d[b]:
            s = d[a] / (d[a] - d[b]); x = X[a] + s * t_; rr = r[a] + s * (r[b] - r[a])
        elif min(abs(d[a]), abs(d[b])) < re:              # runs close to the plane without crossing it
            k = a if abs(d[a]) < abs(d[b]) else b; x = X[k] - d[k] * n; rr = r[k]
        else: continue
        out.append(dict(x_mm=x, r_mm=float(rr), cos=c, a_mm=float(min(rr / max(c, 1e-6), 5 * rr)), edge=(int(a), int(b)), branch_id=int(br[a]), segment=str(seg[a])))
    return out

def size_box(cl, probe):
    """probe: a probes.csv row (dict). Returns dict(point_mm, normal, h_mm, h_min_mm, h_pref_mm, h_clear_mm, r_own_mm, r_ref_mm, n_other_crossings, nearest_other, ok, reason)"""
    p = np.array([float(probe["x"]), float(probe["y"]), float(probe["z"])]); n = np.array([float(probe[k]) for k in ("normal_x", "normal_y", "normal_z")]); n /= np.linalg.norm(n)
    r_ref = float(probe["r_ref_mm"]); tn = np.asarray(cl.point_data["tree_node"]); idx = np.where(tn == int(probe["tree_node"]))[0]
    if len(idx) != 1: raise SystemExit(f"probe {probe['probe_id']}: tree_node {probe['tree_node']} matches {len(idx)} centreline points")
    i = int(idx[0]); r_own = float(np.asarray(cl.point_data[_radius_field(cl)])[i])
    cr = plane_crossings(cl, p, n)
    if not cr: raise SystemExit(f"probe {probe['probe_id']}: the centreline does not meet its own plane")
    dist = [np.linalg.norm(c["x_mm"] - p) for c in cr]; own = int(np.argmin(dist))
    if dist[own] > max(r_own, 0.25): raise SystemExit(f"probe {probe['probe_id']}: nearest centreline crossing {dist[own]:.3f} mm from the probe point")
    cos_own = cr[own]["cos"]; a_own = r_own / max(cos_own, 0.2)
    others = [c for k, c in enumerate(cr) if k != own and np.linalg.norm(c["x_mm"] - p) > a_own + cr[own]["r_mm"]]     # crossings within the own section are the edges at the probe node
    h_min = H_MIN_FACTOR * a_own + H_MIN_ADD_MM; h_pref = max(H_PREF_FACTOR * r_ref, h_min)
    clear = [(float(np.max(np.abs(c["x_mm"] - p)) - c["a_mm"] - CLEAR_MARGIN_MM), c) for c in others]
    h_clear = min([v for v, _ in clear], default=np.inf); h = min(h_pref, h_clear)
    near = min(clear, key=lambda v: v[0])[1] if clear else None
    ok = bool(h >= h_min)
    return dict(probe_id=probe["probe_id"], kind=probe["kind"], tree_node=int(probe["tree_node"]), point_mm=p.tolist(), normal=n.tolist(), r_ref_mm=r_ref, r_own_mm=r_own, r_own_field=_radius_field(cl), cos_own=float(cos_own),
                h_mm=float(h), h_min_mm=float(h_min), h_pref_mm=float(h_pref), h_clear_mm=(None if not np.isfinite(h_clear) else float(h_clear)), n_other_crossings_infinite_plane=len(others),
                nearest_other=None if near is None else dict(x_mm=[float(v) for v in near["x_mm"]], r_mm=near["r_mm"], segment=near["segment"], branch_id=near["branch_id"], Linf_dist_mm=float(np.max(np.abs(near["x_mm"] - p)))),
                ok=ok, reason=None if ok else f"centreline clearance {h_clear:.3f} mm < h_min {h_min:.3f} mm: another vessel is too close to the probe section for an axis-aligned box")

def box_m(point_mm, h_mm):
    p = np.asarray(point_mm, float); return ((p - h_mm) * 1e-3).tolist(), ((p + h_mm) * 1e-3).tolist()

# ---------------- mesh check
def load_mesh(poly):
    """internalMesh (no fields, polyhedra NOT decomposed) of a polyMesh dir, read through a temporary case dir (nothing is written next to the mesh)"""
    import pyvista as pv
    tmp = tempfile.mkdtemp(prefix="probe_sections_")
    try:
        os.makedirs(f"{tmp}/constant"); os.symlink(os.path.abspath(poly), f"{tmp}/constant/polyMesh"); open(f"{tmp}/case.foam", "w").close()
        rd = pv.OpenFOAMReader(f"{tmp}/case.foam"); rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh"); rd.disable_all_cell_arrays(); rd.disable_all_point_arrays()
        if hasattr(rd, "decompose_polyhedra"): rd.decompose_polyhedra = False
        mb = rd.read(); m = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
        return m.copy()
    finally: shutil.rmtree(tmp, ignore_errors=True)

class MeshChecker:
    def __init__(self, mesh):
        from scipy.spatial import cKDTree
        self.mesh = mesh; self.cc = np.asarray(mesh.cell_centers().points); self.tree = cKDTree(self.cc)

    def check(self, point_mm, normal, h_mm, r_own_mm):
        p = np.asarray(point_mm, float) * 1e-3; n = np.asarray(normal, float); n /= np.linalg.norm(n); h = h_mm * 1e-3; lo, hi = p - h, p + h
        R = np.sqrt(3) * h + max(3e-3, 6 * r_own_mm * 1e-3)
        ids = np.sort(np.asarray(self.tree.query_ball_point(p, R), dtype=np.int64))      # vtkExtractCells keeps the ascending id order
        sub = self.mesh.extract_cells(ids)
        if "vtkOriginalCellIds" in sub.cell_data.keys(): assert np.array_equal(np.asarray(sub.cell_data["vtkOriginalCellIds"]), ids)
        cc = self.cc[ids]; marg = np.min(np.minimum(cc - lo, hi - cc), axis=1)                     # > 0: centre inside the box, value = L_inf distance to the box faces
        hc = np.cbrt(np.abs(np.asarray(sub.compute_cell_sizes(length=False, area=False, volume=True).cell_data["Volume"])))
        sub.cell_data["marg"] = marg; sub.cell_data["hcell"] = hc; sub.cell_data["dcen"] = np.linalg.norm(cc - p, axis=1)
        sl = sub.slice(normal=n, origin=p)
        if sl.n_cells == 0: return dict(ok=False, reason="plane does not cut the mesh near the probe")
        cn = sl.connectivity(extraction_mode="all"); rid = np.array(cn.cell_data["RegionId"], dtype=np.int64, copy=True)    # copy while the connectivity output is alive (pyvista 0.47 relabels RegionId from a numpy buffer)
        con = cn.compute_cell_sizes(length=False, area=True, volume=False); con.cell_data["RegionId"] = rid
        A = np.asarray(con.cell_data["Area"]); mg = np.asarray(con.cell_data["marg"]); hcs = np.asarray(con.cell_data["hcell"])
        own = int(rid[con.find_closest_cell(p)]); inb = mg > 0; ctr = np.asarray(con.cell_centers().points)
        regions_in_box = sorted(set(rid[inb].tolist())); own_c = rid == own; oth = ~own_c
        own_far = float(np.max(np.linalg.norm(ctr[own_c] - p, axis=1)))
        r = dict(h_mm=h_mm, box_lo_m=lo.tolist(), box_hi_m=hi.tolist(), crop_radius_mm=R * 1e3, n_regions_local_unbounded=int(rid.max() + 1), own_region=own, regions_with_centres_in_box=regions_in_box,
                 own_min_margin_over_cell=float(np.min(mg[own_c] / hcs[own_c])), others_max_margin_over_cell=(float(np.max(mg[oth] / hcs[oth])) if oth.any() else None),
                 own_section_area_mm2=float(A[own_c].sum() * 1e6), bounded_section_area_mm2=float(A[inb].sum() * 1e6), area_ref_mm2=float(np.pi * r_own_mm ** 2), own_max_dist_mm=own_far * 1e3)
        Ab = A[inb].sum(); cen = (ctr[inb] * A[inb, None]).sum(0) / Ab if Ab > 0 else p; req = np.sqrt(Ab / np.pi) if Ab > 0 else np.nan
        r.update(bounded_area_over_pi_r_own2=float(Ab / (np.pi * (r_own_mm * 1e-3) ** 2)), bounded_r_eq_mm=float(req * 1e3), centroid_offset_over_req=float(np.linalg.norm(cen - p) / req) if Ab > 0 else None)
        fails = []
        if regions_in_box != [own]: fails.append("other")            # (1)
        if r["own_min_margin_over_cell"] < 0.5 or own_far > R - 2 * float(hcs.max()): fails.append("clip")   # (2)
        if r["others_max_margin_over_cell"] is not None and r["others_max_margin_over_cell"] > -0.5: fails.append("other")   # (3)
        if not (AREA_FACTOR[0] <= r["bounded_area_over_pi_r_own2"] <= AREA_FACTOR[1]): fails.append("area")    # (4)
        if r["centroid_offset_over_req"] is None or r["centroid_offset_over_req"] >= 0.5: fails.append("centroid")
        r["fails"] = sorted(set(fails)); r["ok"] = not fails
        return r

    def infinite_plane(self, point_mm, normal):
        """diagnostic: the UNBOUNDED plane through the whole mesh (what the 09-26 monitors sampled): number of connected components and total vs probe-component area"""
        p = np.asarray(point_mm, float) * 1e-3; n = np.asarray(normal, float); n /= np.linalg.norm(n)
        cn = self.mesh.slice(normal=n, origin=p).connectivity(extraction_mode="all"); rid = np.array(cn.cell_data["RegionId"], dtype=np.int64, copy=True)
        con = cn.compute_cell_sizes(length=False, area=True, volume=False); A = np.asarray(con.cell_data["Area"]); own = int(rid[con.find_closest_cell(p)])
        return dict(n_components=int(rid.max() + 1), total_area_mm2=float(A.sum() * 1e6), probe_component_area_mm2=float(A[rid == own].sum() * 1e6))

def fit_and_check(checker, sb, max_steps=8):
    """mesh check of a sized box with the shrink/grow rule; returns (h_final_mm or None, attempts)"""
    h = sb["h_mm"]; att = []; hmax = sb["h_clear_mm"] if sb["h_clear_mm"] is not None else 3 * sb["h_pref_mm"]
    for _ in range(max_steps):
        r = checker.check(sb["point_mm"], sb["normal"], h, sb["r_own_mm"]); att.append(r)
        if r["ok"]: return h, att
        if "other" in r["fails"] and "clip" not in r["fails"] and h * 0.85 >= sb["h_min_mm"]: h *= 0.85
        elif "clip" in r["fails"] and "other" not in r["fails"] and h * 1.15 <= hmax: h *= 1.15
        else: break
    return None, att

def probe_planes_lenient(pkg, poly=None, kinds=("throat", "measurement"), checker=None, diagnose_infinite=False):
    """for each probe kind: the sized box and (if a polyMesh is given) the mesh check. Returns {kind: dict(point_m, normal, bounds_m=(lo, hi) or None, sizing, mesh_check, status)}"""
    cl = pkg["centreline"]; out = {}
    if poly is not None and checker is None: checker = MeshChecker(load_mesh(poly))
    for k in kinds:
        rows = [p for p in pkg["probes"] if p["kind"] == k]
        if len(rows) != 1: raise SystemExit(f"{len(rows)} '{k}' probes in {pkg['name']}")
        sb = size_box(cl, rows[0]); e = dict(probe_id=rows[0]["probe_id"], point_m=(np.asarray(sb["point_mm"]) * 1e-3).tolist(), normal=sb["normal"], sizing=sb)
        if not sb["ok"]: raise SystemExit(f"{pkg['name']} {k} probe: {sb['reason']}")
        if checker is None:
            e.update(bounds_m=box_m(sb["point_mm"], sb["h_mm"]), h_final_mm=sb["h_mm"], mesh_check=None, status="SIZED_FROM_CENTRELINE_ONLY (no mesh: NOT CHECKED, not for production)")
        else:
            h, att = fit_and_check(checker, sb)
            e.update(mesh_check_attempts=att)
            if diagnose_infinite: e["infinite_plane"] = checker.infinite_plane(sb["point_mm"], sb["normal"])
            if h is None: raise SystemExit(f"{pkg['name']} {k} probe {rows[0]['probe_id']}: bounded-plane mesh check FAILED for every box tried: {[(round(a['h_mm'], 3), a['fails']) for a in att]} - refusing to build")
            e.update(bounds_m=box_m(sb["point_mm"], h), h_final_mm=h, mesh_check=att[-1], status="CHECKED_ON_MESH")
        out[k] = e
    return out


# ---------------- strict single-lumen rule for the measurement section (S1-S4 in the module docstring)
def _graph(cl):
    L = np.asarray(cl.lines).reshape(-1, 3)[:, 1:]; par = {}
    for a, b in L: par[int(max(a, b))] = int(min(a, b))
    ch = {}
    for k, v in par.items(): ch.setdefault(v, []).append(k)
    return par, ch

def degree(par, ch, i): return (1 if i in par else 0) + len(ch.get(i, []))

def vessel_path(cl, i):
    """point indices of the lesion-vessel path through point i: root -> i, continued distally from i along the child of the same branch_id (else the lowest-index child) to a leaf; returns (path, arc_mm, k = index of i)"""
    par, ch = _graph(cl); br = np.asarray(cl.point_data["branch_id"]) if "branch_id" in cl.point_data.keys() else np.zeros(cl.n_points, int)
    path = [i]
    while path[-1] in par: path.append(par[path[-1]])
    path = path[::-1]; k = len(path) - 1; j = i
    while ch.get(j):
        same = sorted(c for c in ch[j] if br[c] == br[j]) or sorted(ch[j]); j = same[0]; path.append(j)
    X = np.asarray(cl.points, float)[path]; arc = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]
    return path, arc, k

def path_point(X, arc, s):
    return np.array([np.interp(s, arc, X[:, d]) for d in range(3)])

def path_tangent(X, arc, s, half=TANGENT_HALF_MM):
    a, b = max(s - half, arc[0]), min(s + half, arc[-1]); t = path_point(X, arc, b) - path_point(X, arc, a)
    return t / np.linalg.norm(t)

def strict_centreline(cl, point_index, normal, r_ref_mm):
    """(S1) + (S2) at a centreline point: dict(angle_deg, tangent, bifurcations_within, ok_angle, ok_bifurcation, ok)"""
    par, ch = _graph(cl); path, arc, k = vessel_path(cl, point_index); X = np.asarray(cl.points, float)[path]
    t = path_tangent(X, arc, arc[k]); n = np.asarray(normal, float); n = n / np.linalg.norm(n)
    ang = float(np.degrees(np.arccos(min(1.0, abs(float(n @ t))))))
    lim = BIF_CLEAR_FACTOR * r_ref_mm
    bad = [dict(tree_node=int(np.asarray(cl.point_data["tree_node"])[path[m]]), point_index=int(path[m]), arc_from_probe_mm=float(arc[m] - arc[k]), degree=degree(par, ch, path[m]))
           for m in range(len(path)) if abs(arc[m] - arc[k]) <= lim and degree(par, ch, path[m]) != 2]
    near = [dict(arc_from_probe_mm=float(arc[m] - arc[k]), degree=degree(par, ch, path[m]), tree_node=int(np.asarray(cl.point_data["tree_node"])[path[m]]))
            for m in range(len(path)) if degree(par, ch, path[m]) != 2]
    nearest = min(near, key=lambda d: abs(d["arc_from_probe_mm"])) if near else None
    return dict(angle_deg=ang, max_angle_deg=MAX_ANGLE_DEG, tangent=t.tolist(), bifurcation_clearance_required_mm=lim, non_degree2_nodes_within=bad, nearest_non_degree2_node=nearest,
                ok_angle=bool(ang <= MAX_ANGLE_DEG), ok_bifurcation=not bad, ok=bool(ang <= MAX_ANGLE_DEG and not bad))

def strict_area(mesh_check, r_ref_mm):
    """(S4) on a mesh-check result: bounded area / (pi r_ref^2) within [1/1.6, 1.6]"""
    f = mesh_check["bounded_section_area_mm2"] / (np.pi * r_ref_mm ** 2)
    return dict(area_over_pi_r_ref2=float(f), limits=[1 / AREA_FACTOR_STRICT, AREA_FACTOR_STRICT], ok=bool(1 / AREA_FACTOR_STRICT <= f <= AREA_FACTOR_STRICT))

def relocation_candidates(cl, point_index):
    """nodes of the same vessel path within RELOC_MAX_MM of arc, ordered by |arc distance| (ties: distal first), the probe node itself excluded"""
    path, arc, k = vessel_path(cl, point_index)
    c = [(abs(arc[m] - arc[k]), 0 if arc[m] > arc[k] else 1, m) for m in range(len(path)) if m != k and abs(arc[m] - arc[k]) <= RELOC_MAX_MM]
    X = np.asarray(cl.points, float)[path]; out = []
    for d, _, m in sorted(c):
        out.append(dict(point_index=int(path[m]), arc_from_probe_mm=float(arc[m] - arc[k]), point_mm=X[m].tolist(), tangent=path_tangent(X, arc, arc[m]).tolist()))
    return out

def _try_section(checker, cl, row):
    """mesh check (S3, with the shrink/grow rule) + (S4) of a probe row; returns (ok, h_or_None, sizing, attempts, area_rule, why)"""
    try: sb = size_box(cl, row)
    except SystemExit as e: return False, None, None, [], None, f"box sizing: {e}"
    if not sb["ok"]: return False, None, sb, [], None, sb["reason"]
    if checker is None: return True, sb["h_mm"], sb, [], None, "no mesh: S3/S4 not checked"
    h, att = fit_and_check(checker, sb)
    if h is None: return False, None, sb, att, None, f"mesh check failed for every box: {[(round(a['h_mm'], 3), a['fails']) for a in att]}"
    ar = strict_area(att[-1], float(row["r_ref_mm"]))
    return ar["ok"], h, sb, att, ar, (None if ar["ok"] else f"area {ar['area_over_pi_r_ref2']:.3f} x pi r_ref^2 outside [{1 / AREA_FACTOR_STRICT:.3f}, {AREA_FACTOR_STRICT}]")

def _entry(row, sb, h, att, checker, status):
    e = dict(probe_id=row["probe_id"], point_m=(np.asarray(sb["point_mm"]) * 1e-3).tolist(), normal=sb["normal"], sizing=sb, bounds_m=box_m(sb["point_mm"], h), h_final_mm=h, mesh_check_attempts=att,
             mesh_check=att[-1] if att else None, status=status)
    return e

def probe_planes(pkg, poly=None, kinds=("throat", "measurement"), checker=None, diagnose_infinite=False):
    """probe_planes_lenient() for the throat; the STRICT rule (S1-S4) with the documented relocation for the measurement probe. Returns {kind: entry}; when the package measurement probe fails the rule,
    out['measurement'] is the RELOCATED plane (status 'RELOCATED ...'), out['measurement_orig'] the package plane when its bounded section passes the mesh check (else absent), and every entry of the measurement
    side carries 'section_rule' (and 'relocation'); a relocation that finds no valid candidate within RELOC_MAX_MM refuses (SystemExit)."""
    cl = pkg["centreline"]
    if poly is not None and checker is None: checker = MeshChecker(load_mesh(poly))
    out = probe_planes_lenient(pkg, None, [k for k in kinds if k != "measurement"], checker, diagnose_infinite) if any(k != "measurement" for k in kinds) else {}
    tn = np.asarray(cl.point_data["tree_node"])
    if "throat" in out:          # recorded, not enforced (the throat section is judged by the lenient rule: r_own = r_target there)
        tr = [p for p in pkg["probes"] if p["kind"] == "throat"][0]; ti = int(np.where(tn == int(tr["tree_node"]))[0][0])
        out["throat"]["section_rule_record_only"] = strict_centreline(cl, ti, out["throat"]["normal"], float(tr["r_ref_mm"]))
    if "measurement" not in kinds: return out
    rows = [p for p in pkg["probes"] if p["kind"] == "measurement"]
    if len(rows) != 1: raise SystemExit(f"{len(rows)} 'measurement' probes in {pkg['name']}")
    row = rows[0]; idx = np.where(tn == int(row["tree_node"]))[0]
    if len(idx) != 1: raise SystemExit(f"measurement probe tree_node {row['tree_node']}: {len(idx)} centreline points")
    i = int(idx[0]); n = np.array([float(row[k]) for k in ("normal_x", "normal_y", "normal_z")])
    sc = strict_centreline(cl, i, n, float(row["r_ref_mm"]))
    ok3, h, sb, att, ar, why = _try_section(checker, cl, row)
    rule = dict(probe_id=row["probe_id"], tree_node=int(row["tree_node"]), S1_S2_centreline=sc, S3_mesh_check_ok=(None if checker is None else bool(h is not None)), S4_area=ar, mesh_checked=checker is not None,
                why_not_ok=[x for x in ([None if sc["ok_angle"] else f"S1: normal {sc['angle_deg']:.1f} deg from the centreline tangent (> {MAX_ANGLE_DEG})",
                                         None if sc["ok_bifurcation"] else f"S2: non-degree-2 node(s) within {sc['bifurcation_clearance_required_mm']:.3f} mm: {[(b['tree_node'], round(b['arc_from_probe_mm'], 3), b['degree']) for b in sc['non_degree2_nodes_within']]}"]
                                         + ([] if ok3 else [f"S3/S4: {why}"])) if x])
    if diagnose_infinite and checker is not None and sb is not None: rule["infinite_plane_unbounded"] = checker.infinite_plane(sb["point_mm"], sb["normal"])
    if sc["ok"] and ok3:
        rule["status"] = "PASS"
        e = _entry(row, sb, h, att, checker, "CHECKED_ON_MESH (strict single-lumen rule PASS)" if checker is not None else "SIZED_FROM_CENTRELINE_ONLY (no mesh: NOT CHECKED, not for production; strict rule S1/S2 PASS)")
        e.update(section_rule=rule, infinite_plane=rule.get("infinite_plane_unbounded")); out["measurement"] = e; return out
    rule["status"] = "FAILED_SECTION_RULE"
    orig_bounded_valid = (h is not None) and checker is not None
    if orig_bounded_valid: out["measurement_orig"] = _entry(row, sb, h, att, checker, "ORIGINAL PACKAGE PROBE: bounded section passes the mesh check (S3) but FAILED_SECTION_RULE; monitor measurementOrigP, NOT the measurement used")
    tried = []
    for c in relocation_candidates(cl, i):
        r_ref_c = float(np.asarray(cl.point_data["r_ref_mm"])[c["point_index"]])
        crow = dict(probe_id=f"{row['probe_id']}_reloc", kind="measurement", tree_node=str(int(tn[c["point_index"]])), x=c["point_mm"][0], y=c["point_mm"][1], z=c["point_mm"][2],
                    normal_x=c["tangent"][0], normal_y=c["tangent"][1], normal_z=c["tangent"][2], r_ref_mm=r_ref_c)
        scc = strict_centreline(cl, c["point_index"], c["tangent"], r_ref_c)
        if not scc["ok"]: tried.append(dict(tree_node=int(tn[c["point_index"]]), arc_from_probe_mm=c["arc_from_probe_mm"], fails="S1/S2", nearest_non_degree2=scc["nearest_non_degree2_node"])); continue
        okc, hc, sbc, attc, arc_, whyc = _try_section(checker, cl, crow)
        if not okc: tried.append(dict(tree_node=int(tn[c["point_index"]]), arc_from_probe_mm=c["arc_from_probe_mm"], fails=f"S3/S4: {whyc}")); continue
        rel = dict(original=dict(probe_id=row["probe_id"], tree_node=int(row["tree_node"]), point_mm=[float(row["x"]), float(row["y"]), float(row["z"])], normal=n.tolist(), r_ref_mm=float(row["r_ref_mm"]),
                                 s_mm=row.get("s_mm"), section_rule=rule, original_monitor=("measurementOrigFlux/measurementOrigP" if orig_bounded_valid else None),
                                 original_monitor_note=(None if orig_bounded_valid else ("no mesh given: original bounded section not checked, no original monitor" if checker is None else f"no original monitor: bounded section not valid ({why})"))),
                   relocated=dict(probe_id=crow["probe_id"], tree_node=int(crow["tree_node"]), point_mm=c["point_mm"], normal=c["tangent"], r_ref_mm=r_ref_c, arc_from_original_mm=c["arc_from_probe_mm"],
                                  S1_S2_centreline=scc, S4_area=arc_, mesh_checked=checker is not None),
                   rule=f"nearest node of the same vessel path within {RELOC_MAX_MM} mm of arc (ties distal) passing S1-S4; normal = local path tangent", candidates_rejected_before=tried,
                   monitors=dict(measurementP=crow["probe_id"], measurementOrigP=(row["probe_id"] if orig_bounded_valid else None)))
        e = _entry(crow, sbc, hc, attc, checker, ("RELOCATED (package probe FAILED_SECTION_RULE): " + ("CHECKED_ON_MESH, strict rule PASS" if checker is not None else "SIZED_FROM_CENTRELINE_ONLY (no mesh: NOT CHECKED, not for production)")))
        e.update(section_rule=rule, relocation=rel); out["measurement"] = e
        return out
    raise SystemExit(f"{pkg['name']} measurement probe {row['probe_id']}: FAILED_SECTION_RULE ({rule['why_not_ok']}) and no valid single-lumen node within {RELOC_MAX_MM} mm of arc on the same path: {tried} - refusing to build")
