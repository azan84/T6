"""Build a truncation-matched, open-ended surface for one M1 case (baseline / missed-branch), given a
Tree already built (bed='discrete') and a smoothed, mask-derived surface. Reusable for both cases since
the clipping logic only depends on the tree's own leaves + root."""
import sys
sys.path.insert(0, "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot")
import numpy as np
import pyvista as pv
from outlets_837 import node_xyz_and_tangent
from clip_outlets import clip_at_leaves

def inlet_clip_spec(T):
    root_seg = [s for s in T.segments if s.sid == 0][0]
    pts_mm = root_seg.pts * 1e3
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts_mm, axis=0), axis=1))])
    j = int(np.searchsorted(arc, 4.0))  # skip the ~4mm ostial end-cap artefact region (loader's own convention)
    p = pts_mm[j]
    tan = pts_mm[j + 2] - pts_mm[max(0, j - 2)]; tan /= np.linalg.norm(tan)
    r = root_seg.r[j] * 1e3
    return p, -tan, r   # negate: remove the PROXIMAL cap (behind this point), keep the distal tree

def build_open_surface(T, surf: pv.PolyData, local_radius_factor: float = 5.0) -> pv.PolyData:
    leaves_info = [inlet_clip_spec(T)]
    for v in T.leaves:
        p, tan = node_xyz_and_tangent(T, v)
        leaves_info.append((p, tan, T.r_ref[v] * 1e3))
    clipped = clip_at_leaves(surf, leaves_info, local_radius_factor=local_radius_factor)
    return clipped, leaves_info

if __name__ == "__main__":
    from outlets_837 import build_tree
    T = build_tree()
    surf = pv.read(f"{sys.argv[1]}/smoothed.vtp") if len(sys.argv) > 1 else pv.read("baseline/smoothed.vtp")
    clipped, leaves_info = build_open_surface(T, surf)
    edges = clipped.extract_feature_edges(boundary_edges=True, feature_edges=False, manifold_edges=False, non_manifold_edges=False)
    conn = edges.connectivity(extraction_mode="all")
    n_loops = len(np.unique(conn.point_data["RegionId"])) if edges.n_points else 0
    print(f"{clipped.n_points} points, {n_loops} boundary loops (want {1+len(T.leaves)})")
    out = sys.argv[2] if len(sys.argv) > 2 else "baseline/clipped_final.vtp"
    clipped.save(out)
    print("wrote", out)
