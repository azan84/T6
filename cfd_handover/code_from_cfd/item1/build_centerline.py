"""Build the centerline VTP (points + MaximumInscribedSphereRadius + polyline cells per branch,
overlapping root-to-tip paths as vmtkcenterlinemodeller expects) for the item-1 branched tree.

Uses the SAME geometry.py as build_0d.py (panel fix, 2026-09-19 - see geometry.py's module docstring
for why: the previous version duplicated coordinates in both files independently and put branch B on
branch A's own axis, confirmed as a fused-lumen bug by all three reviewers slicing the generated
surface)."""
import sys
from pathlib import Path
import numpy as np
import pyvista as pv

sys.path.insert(0, str(Path(__file__).parent))
from geometry import build_paths, verify_clearances

# VMTK's -bounds argument rejects negative values (a real CLI quirk, not a design choice) - shift the
# whole geometry into positive y/z. B/B1/B2 now reach y=-30mm (see geometry.py), so the shift must
# cover that, not just the old -8mm.
Y_SHIFT, Z_SHIFT = 42.0, 6.0   # B2 reaches y=-33.47mm (steeper B/B1/B2 angles after the geometry fix);
                                # 42mm leaves >=6mm clearance to y=0 for the flow-extension/buffer margin
                                # added when computing the VMTK tube-image bounds.

def build(ds_pct, path):
    verify_clearances(ds_pct)  # re-assert at generation time, not just when geometry.py runs standalone
    paths = build_paths(ds_pct, n_trunk=61, n_a=161, n_b=31, n_b1=61, n_b2=61)
    x_t, y_t, z_t, r_t = paths["trunk"]
    x_a, y_a, z_a, r_a = paths["A"]
    x_b, y_b, z_b, r_b = paths["B"]
    x_b1, y_b1, z_b1, r_b1 = paths["B1"]
    x_b2, y_b2, z_b2, r_b2 = paths["B2"]

    def shifted(x, y, z):
        return np.stack([x, y + Y_SHIFT, z + Z_SHIFT], 1)

    pts_trunk = shifted(x_t, y_t, z_t)
    pts_a = shifted(x_a, y_a, z_a)
    pts_b = shifted(x_b, y_b, z_b)
    pts_b1 = shifted(x_b1, y_b1, z_b1)
    pts_b2 = shifted(x_b2, y_b2, z_b2)

    # Overlapping root-to-tip paths (each path restarts from x=0), which is what
    # vmtkcenterlinemodeller expects for its Voronoi-diagram-based implicit reconstruction.
    path_A = np.vstack([pts_trunk, pts_a[1:]])
    r_path_A = np.concatenate([r_t, r_a[1:]])
    path_B1 = np.vstack([pts_trunk, pts_b, pts_b1[1:]])
    r_path_B1 = np.concatenate([r_t, r_b, r_b1[1:]])
    path_B2 = np.vstack([pts_trunk, pts_b, pts_b2[1:]])
    r_path_B2 = np.concatenate([r_t, r_b, r_b2[1:]])

    all_pts = np.vstack([path_A, path_B1, path_B2]) * 1e-3   # mm -> m (OpenFOAM/project convention)
    all_r = np.concatenate([r_path_A, r_path_B1, r_path_B2]) * 1e-3
    lines = []
    offset = 0
    for p in (path_A, path_B1, path_B2):
        n = len(p)
        lines.append(np.concatenate([[n], np.arange(offset, offset + n)]))
        offset += n
    poly = pv.PolyData(all_pts, lines=np.concatenate(lines))
    poly.point_data["MaximumInscribedSphereRadius"] = all_r
    poly.save(path)
    bounds = poly.bounds
    print(f"wrote {path}: {poly.n_points} points, throat(min r on A)={r_a.min()*1e-3:.6f} m, "
          f"bounds={bounds}")

if __name__ == "__main__":
    import sys
    build(int(sys.argv[1]), sys.argv[2])
