"""Cross-sections of an OpenFOAM volume mesh (pyvista): the connected section nearest a point, cut by a plane with a given normal, with area, area-averaged p, through-plane flux and the maximum inscribed radius.
Same idea as P/pullback_radii.section() but made to work on 5-8 M-cell meshes: a KD-tree of cell centres restricts every slice to the cells around the point (no whole-mesh slice per station). No 0D code.
Units: the OpenFOAM mesh is in metres; p is kinematic (m2/s2, multiply by rho for Pa); U in m/s.
Section validity (section_ok): the area-weighted centroid lies within 0.5 r_eq of the station point (a bifurcation section that catches two vessels, or a station outside the lumen, fails this)."""
import os
import numpy as np
import pyvista as pv
from scipy.spatial import cKDTree
from scipy.ndimage import distance_transform_edt

def load_internal_mesh(case_dir, time=None, fields=True):
    """internalMesh of <case_dir>/case.foam at `time` (default: the latest time directory that is not 0, else 0) as an UnstructuredGrid; returns (mesh, time_used)"""
    open(f"{case_dir}/case.foam", "a").close()
    rd = pv.OpenFOAMReader(f"{case_dir}/case.foam"); rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh")
    if not fields: rd.disable_all_cell_arrays(); rd.disable_all_point_arrays()
    else: rd.enable_all_cell_arrays()
    tv = [t for t in rd.time_values]
    if not tv: t = 0.0                                   # a mesh-only directory: no time directories at all
    elif time is None: t = tv[-1]
    else:
        t = float(time)
        if t not in tv: raise SystemExit(f"time {t} not among reconstructed times {tv}")
    if tv: rd.set_active_time_value(t)
    mb = rd.read()
    mesh = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
    if fields and (t == 0 or "p" not in mesh.cell_data): raise SystemExit(f"no solved fields at time {t} (reconstructPar first)")
    return mesh, t

class Sectioner:
    def __init__(self, mesh):
        self.mesh = mesh; self.centres = np.asarray(mesh.cell_centers().points); self.tree = cKDTree(self.centres)

    def section(self, point_m, normal, r_hint_m, need_fields=True, margin_m=1.5e-3):
        pt = np.asarray(point_m, float); n = np.asarray(normal, float); n = n / np.linalg.norm(n)
        ids = self.tree.query_ball_point(pt, 3.0 * r_hint_m + margin_m)
        if len(ids) == 0: return None
        sub = self.mesh.extract_cells(np.asarray(ids, dtype=np.int64))
        sl = sub.slice(normal=n, origin=pt)
        if sl.n_cells == 0: return None
        sl = sl.extract_surface(algorithm=None).triangulate().clean()
        part = sl.connectivity(extraction_mode="closest", closest_point=pt).compute_cell_sizes(length=False, area=True, volume=False)
        if part.n_cells == 0: return None
        A = np.asarray(part.cell_data["Area"]); Atot = float(A.sum()); ctr = np.asarray(part.cell_centers().points); cen = (ctr * A[:, None]).sum(0) / Atot
        req = float(np.sqrt(Atot / np.pi)); off = float(np.linalg.norm(cen - pt)) / req
        out = dict(area=Atot, r_eq=req, centroid=cen, centroid_offset_over_req=off, section_ok=bool(off < 0.5), surface=part, normal=n)
        if need_fields:
            p = np.asarray(part.cell_data["p"]); U = np.asarray(part.cell_data["U"])
            out.update(p_mean=float((p * A).sum() / Atot), Q=float(((U @ n) * A).sum()), Q_abs=float((np.abs(U @ n) * A).sum()))
        return out

def rasterise(u, v, tri, gu, gv, eps=1e-9):
    """boolean mask (len(gv) x len(gu)) of the grid points inside any triangle (barycentric test per triangle over its bounding box; robust to degenerate/duplicate triangles, unlike a trapezoid-map trifinder)"""
    mask = np.zeros((len(gv), len(gu)), bool); h = gu[1] - gu[0]; u0, v0 = gu[0], gv[0]
    for a, b, c in tri:
        x = u[[a, b, c]]; y = v[[a, b, c]]
        i0 = max(int(np.floor((x.min() - u0) / h)), 0); i1 = min(int(np.ceil((x.max() - u0) / h)), len(gu) - 1)
        j0 = max(int(np.floor((y.min() - v0) / h)), 0); j1 = min(int(np.ceil((y.max() - v0) / h)), len(gv) - 1)
        if i1 < i0 or j1 < j0: continue
        d = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(d) < 1e-300: continue
        UX, VY = np.meshgrid(gu[i0:i1 + 1], gv[j0:j1 + 1])
        l1 = ((y[1] - y[2]) * (UX - x[2]) + (x[2] - x[1]) * (VY - y[2])) / d; l2 = ((y[2] - y[0]) * (UX - x[2]) + (x[0] - x[2]) * (VY - y[2])) / d
        mask[j0:j1 + 1, i0:i1 + 1] |= (l1 >= -eps) & (l2 >= -eps) & (1 - l1 - l2 >= -eps)
    return mask

def max_inscribed_radius(surface, normal, n_across=48):
    """max inscribed circle radius of a planar triangulated section: project onto the plane, rasterise the triangles on a square grid (pixel h = r_eq/n_across), Euclidean distance transform of the inside mask,
    r = (max EDT - 0.5) h (a pixel-centre EDT overestimates the continuous distance by about half a pixel). Accuracy about one pixel (about 2 % of the radius at n_across 48). Also returns the pixel size."""
    n = np.asarray(normal, float); n = n / np.linalg.norm(n)
    e1 = np.cross(n, [1.0, 0.0, 0.0])
    if np.linalg.norm(e1) < 0.1: e1 = np.cross(n, [0.0, 1.0, 0.0])
    e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
    pts = np.asarray(surface.points); tri = np.asarray(surface.faces).reshape(-1, 4)[:, 1:]
    u, v = pts @ e1, pts @ e2; A = surface.compute_cell_sizes(length=False, area=True, volume=False).cell_data["Area"].sum()
    h = float(np.sqrt(A / np.pi) / n_across)
    gu = np.arange(u.min() - 2 * h, u.max() + 2 * h, h); gv = np.arange(v.min() - 2 * h, v.max() + 2 * h, h)
    inside = rasterise(u, v, tri, gu, gv)
    edt = distance_transform_edt(inside)
    return float(max(edt.max() - 0.5, 0.0) * h), h
