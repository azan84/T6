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

HOLE_AREA_FRACTION = 0.005      # robust mode: a section whose enclosed holes cover >= 0.5 % of its filled area is not a valid lumen section (sten70 S50 x = 52 mm: about 9 %)

def hole_fraction(surface, normal, n_across=96):
    """area fraction of the holes of a planar triangulated section: rasterise the triangles (rasterise(), pixel r_eq/n_across), fill the enclosed holes (binary_fill_holes): (filled - inside) / filled.
    Inner boundary loops without area (cracks where the polygons of cells with split faces meet at T-junctions, numerical slivers) do not count: their pixels are inside."""
    from scipy.ndimage import binary_fill_holes
    n = np.asarray(normal, float); n = n / np.linalg.norm(n)
    e1 = np.cross(n, [1.0, 0.0, 0.0])
    if np.linalg.norm(e1) < 0.1: e1 = np.cross(n, [0.0, 1.0, 0.0])
    e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
    pts = np.asarray(surface.points); tri = np.asarray(surface.faces).reshape(-1, 4)[:, 1:]; u, v = pts @ e1, pts @ e2
    A = float(surface.compute_cell_sizes(length=False, area=True, volume=False).cell_data["Area"].sum()); h = float(np.sqrt(A / np.pi) / n_across)
    gu = np.arange(u.min() - 2 * h, u.max() + 2 * h, h); gv = np.arange(v.min() - 2 * h, v.max() + 2 * h, h)
    m = rasterise(u, v, tri, gu, gv, eps=1e-6); f = binary_fill_holes(m)
    return float((f.sum() - m.sum()) / max(f.sum(), 1))

class Sectioner:
    def __init__(self, mesh, robust=False):
        """robust=False (default; the method of the returned 09-26 M1 probes, kept for comparability): cut the cells around the point, then keep the slice component (shared slice points) nearest the point.
        robust=True (flow_state_profile.py): keep the 3D-connected component (shared cell points) of the cells that straddle the plane, nearest the point, then cut it (slice polygons of cells with split faces,
        cfMesh refinement-transition polyhedra, can meet at T-junctions without shared points), and count the boundary loops of the section; when there is more than one, the HOLE AREA is measured by
        rasterising the section and filling its enclosed holes (hole_fraction): holes covering >= 0.5 % of the filled area (HOLE_AREA_FRACTION) make section_ok = False (a lumen section has no holes; zero-area
        inner loops, i.e. T-junction cracks or slivers, do not count). A plane through mesh points is moved 0.1 um along its normal. Seen on the sten70 S50 mesh at x = 51.99-52.1 mm: the VTK cut through a band of transition polyhedra leaves 5 holes (area 4.68 vs about 5.1 mm2,
        through-flux +1.8 %) with either method; the cells' own cuts are complete, the holes are a VTK representation/cut defect of those polyhedra."""
        self.mesh = mesh; self.centres = np.asarray(mesh.cell_centers().points); self.tree = cKDTree(self.centres); self.robust = robust

    def section(self, point_m, normal, r_hint_m, need_fields=True, margin_m=1.5e-3):
        pt = np.asarray(point_m, float); n = np.asarray(normal, float); n = n / np.linalg.norm(n)
        ids = self.tree.query_ball_point(pt, 3.0 * r_hint_m + margin_m)
        if len(ids) == 0: return None
        sub = self.mesh.extract_cells(np.asarray(ids, dtype=np.int64)); n_poly = None; nudged = False
        if self.robust:          # lumen = the 3D-connected set of cells straddling the plane (shared corner points), then cut: no slice-level connectivity (see the class docstring)
            d = (np.asarray(sub.points) - pt) @ n
            if np.min(np.abs(d)) < 1e-10:            # the plane passes through mesh points (a layer of faces): move it 0.1 um along n, far below any cell size, so that every cut cell straddles it
                pt = pt + 1e-7 * n; d = d - 1e-7; nudged = True
            conn = np.asarray(sub.cell_connectivity); off = np.asarray(sub.offset)
            dmin = np.minimum.reduceat(d[conn], off[:-1]); dmax = np.maximum.reduceat(d[conn], off[:-1]); st = np.where((dmin < 0) & (dmax > 0))[0]
            if len(st) == 0: return None
            comp = sub.extract_cells(st).connectivity(extraction_mode="closest", closest_point=pt); n_poly = int((np.asarray(comp.celltypes) == 42).sum())
            sl = comp.slice(normal=n, origin=pt)
        else: sl = sub.slice(normal=n, origin=pt)
        if sl.n_cells == 0: return None
        sl = sl.extract_surface(algorithm=None).triangulate().clean()
        part = sl.connectivity(extraction_mode="closest", closest_point=pt).compute_cell_sizes(length=False, area=True, volume=False)
        if part.n_cells == 0: return None
        A = np.asarray(part.cell_data["Area"]); Atot = float(A.sum()); ctr = np.asarray(part.cell_centers().points); cen = (ctr * A[:, None]).sum(0) / Atot
        req = float(np.sqrt(Atot / np.pi)); off = float(np.linalg.norm(cen - pt)) / req
        out = dict(area=Atot, r_eq=req, centroid=cen, centroid_offset_over_req=off, section_ok=bool(off < 0.5), surface=part, normal=n, n_polyhedra_in_section=n_poly)
        if self.robust:
            fe = part.extract_feature_edges(boundary_edges=True, feature_edges=False, manifold_edges=False, non_manifold_edges=False)
            nl = int(np.asarray(fe.connectivity().cell_data["RegionId"]).max() + 1) if fe.n_cells else 0
            hf = hole_fraction(part, n) if nl > 1 else 0.0
            out.update(n_boundary_loops=nl, hole_area_fraction=hf, section_ok=bool(off < 0.5 and hf < HOLE_AREA_FRACTION), plane_nudged_0p1um=nudged)
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
