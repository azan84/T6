"""Clip a surface at truncation-matched outlet points, LOCALLY (an infinite plane cut through a tree can
slice through unrelated, spatially-nearby branches elsewhere - confirmed empirically: a plain plane clip
at LCX's leaf removed >half the surface). Restrict each cut to a local neighbourhood of the leaf point."""
import numpy as np
import pyvista as pv

def clip_at_leaves(surf: pv.PolyData, leaves_xyz_tan_r: list, local_radius_factor: float = 8.0) -> pv.PolyData:
    """leaves_xyz_tan_r: list of (xyz_mm, tangent_unit, r_ref_mm). Returns the clipped surface (largest
    connected component kept, so a fully-severed distal cap piece is dropped)."""
    pts = surf.points
    keep_scalar = np.ones(surf.n_points)   # >0 means keep by default (outside every local cut zone)
    for xyz, tan, r_ref in leaves_xyz_tan_r:
        R_local = local_radius_factor * r_ref
        d_plane = (pts - xyz) @ tan                       # >0 = distal side of this leaf's plane
        d_leaf = np.linalg.norm(pts - xyz, axis=1)
        local = d_leaf < R_local
        # within the local zone, override keep_scalar with the plane test (negative = remove);
        # outside it, leave whatever keep_scalar already was (untouched by this leaf's cut)
        keep_scalar = np.where(local, np.minimum(keep_scalar, -d_plane), keep_scalar)
    surf = surf.copy()
    surf.point_data["keep"] = keep_scalar
    clipped = surf.clip_scalar(scalars="keep", value=0.0, invert=False)   # keep where "keep" > 0
    clipped = clipped.connectivity(extraction_mode="largest")
    clipped = clipped.triangulate().clean()
    return clipped
