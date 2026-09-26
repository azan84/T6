"""Compute truncation-matched outlet clip planes for scan 837/left, bed='discrete' (r_ref<0.60mm cut).
Node->3D-coordinate mapping: within a segment, tree node insertion order (skipping the segment's own
first point, shared with its parent's end node) exactly matches the segment's own point order - verified
directly against zerod_ffr.Tree.__init__'s `for j in range(1, len(r))` loop.
"""
import sys
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code")
import numpy as np
from imagecasx_loader import load_tree

ROOT = "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/imagecas_x_raw/extracted/ImageCAS-X_dataset"

def build_tree(mask_edit_fn=None):
    """mask_edit_fn: unused here (mask isolation happens at the surface-extraction stage, not in the
    0D tree, which reads its own radius directly from the ORIGINAL mask via imagecasx_loader's own EDT
    - for the missed-branch case, the 0D tree must be rebuilt with that segment deleted, done separately
    in build_missedbranch_tree() below, not by editing the mask this function reads)."""
    T = load_tree(f"{ROOT}/centerlines/837.coronary_left_centerline.vtk",
                  f"{ROOT}/segmentations/837.coronary.nii.gz", "837_left", bed="discrete")
    return T

def node_xyz_and_tangent(T, v, eps_nodes=3):
    """3D coordinate (mm, LPS) and local unit tangent (pointing distally) at tree node v."""
    sid = T.seg[v]
    seg = [s for s in T.segments if s.sid == sid][0]
    seg_nodes = np.where(T.seg == sid)[0]           # increasing order == seg.pts[1:] order (verified)
    local_idx = int(np.where(seg_nodes == v)[0][0])  # 0-based position among this segment's OWN nodes
    pts_mm = seg.pts * 1e3                            # seg.pts[0] is the shared point with the parent
    p = pts_mm[local_idx + 1]                         # +1: node 0 of the segment's own new points is seg.pts[1]
    lo = max(0, local_idx + 1 - eps_nodes); hi = min(len(pts_mm) - 1, local_idx + 1 + eps_nodes)
    tangent = pts_mm[hi] - pts_mm[lo]
    tangent = tangent / np.linalg.norm(tangent)
    return p, tangent

if __name__ == "__main__":
    T = build_tree()
    o = T.ffr(mode="murray")
    print(f"min_ffr_main_segmented_network={o['min_ffr_main']:.4f}  n_leaves={len(T.leaves)}")
    print(f"healthy_main_ffr={T.healthy_main_ffr(mode='murray'):.4f}  n_leaves={len(T.leaves)}  (gate: >=0.90 and >=2 outlets)")
    for v in T.leaves:
        p, tan = node_xyz_and_tangent(T, v)
        print(f"leaf {v} ({T.label[v]}): r_ref={T.r_ref[v]*1e3:.4f}mm  xyz={np.round(p,2)}  "
              f"tangent={np.round(tan,3)}")
