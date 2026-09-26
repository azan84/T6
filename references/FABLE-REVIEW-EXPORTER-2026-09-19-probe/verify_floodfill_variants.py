"""verify_floodfill_variants.py — why the shipped rule removes 2061 voxels where the review's probe removed 855.
Ground truth for 'the branch': every mask voxel whose nearest centreline point (distance / r of that point) is a
DELETED point. Score each rule variant by false positives (voxels of retained vessel removed = erosion) and false
negatives (branch voxels left = remnant).

usage: verify_floodfill_variants.py <data_root> <m1_package_dir>
"""
import sys, json
from pathlib import Path
import numpy as np, nibabel as nib
from scipy.ndimage import label as cc_label

root, M1 = Path(sys.argv[1]).expanduser(), Path(sys.argv[2])
if not (root / "centerlines").is_dir(): root = next(c for c in root.iterdir() if (c / "centerlines").is_dir())
img = nib.load(str(root / "segmentations" / "14.coronary.nii.gz")); mask0 = np.asarray(img.dataobj) > 0
sp = np.array(img.header.get_zooms()[:3]); inv = np.linalg.inv(img.affine); FLIP = np.array([-1.0, -1.0, 1.0])
t1 = next(p for p in M1.iterdir() if "T1_missed_branch" in p.name)
edit = json.loads((t1 / "mask_edit.json").read_text()); me = edit["mask_edit"]
D = np.array([[p["x"], p["y"], p["z"], p["r_mm"]] for p in me["deleted_points_mm"]])
R = np.array([[p["x"], p["y"], p["z"], p["r_mm"]] for p in me["retained_points_mm"]])
SC = np.array([[p["x"], p["y"], p["z"], p["r_mm"]] for p in edit["sub_cut_points_mm"]])

def to_ijk(pts):
    ras = np.asarray(pts)[:, :3] * FLIP
    return (inv @ np.c_[ras, np.ones(len(ras))].T)[:3].T
vox = np.argwhere(mask0); vox_mm = (img.affine @ np.c_[vox, np.ones(len(vox))].T)[:3].T * FLIP    # LPS mm
def rel_dist(cl):
    best = np.full(len(vox), np.inf)
    for k in range(0, len(cl), 128):
        d = np.linalg.norm(vox_mm[:, None, :] - cl[None, k:k+128, :3], axis=2) / cl[None, k:k+128, 3]
        best = np.minimum(best, d.min(1))
    return best
rel_D, rel_R, rel_SC = rel_dist(D), rel_dist(R), rel_dist(SC)
truth_branch = rel_D < rel_R                                    # nearest (relative) centreline point is a deleted one
truth_branch_strict = truth_branch & (rel_D < 2.0)              # and actually near the branch
print(f"ground truth: {truth_branch.sum()} voxels belong to the deleted branch (nearest-relative-centreline); "
      f"{truth_branch_strict.sum()} within 2 r of it")
print(f"retained-vessel voxels farther than 1.0 r from every retained point (the unprotected shell): "
      f"{((~truth_branch) & (rel_R > 1.0)).sum()}  (> 1.15 r: {((~truth_branch) & (rel_R > 1.15)).sum()}, "
      f"> 1.3 r: {((~truth_branch) & (rel_R > 1.3)).sum()})")

def ball_mask(cl, factor):
    protect = np.zeros_like(mask0)
    ijk = to_ijk(cl)
    for c_ijk, p in zip(ijk, cl):
        r = factor * p[3]; rad = np.ceil(r / sp).astype(int); c = np.round(c_ijk).astype(int)
        sl = tuple(slice(max(c[d]-rad[d], 0), min(c[d]+rad[d]+1, mask0.shape[d])) for d in range(3))
        g = np.mgrid[sl]; d2 = sum(((g[d]-c_ijk[d])*sp[d])**2 for d in range(3))
        protect[sl] |= d2 <= r**2
    return protect

def rule(retained, deleted, factor, conn, corridor=None):
    protect = ball_mask(retained, factor)
    cand = mask0 & ~protect
    lab, n = cc_label(cand, structure=np.ones((3, 3, 3)) if conn == 26 else None)
    q = np.round(to_ijk(deleted)).astype(int)
    kill = set(lab[q[:, 0], q[:, 1], q[:, 2]].tolist()) - {0}
    rm = np.isin(lab, list(kill))
    if corridor is not None:
        rm &= ball_mask(deleted, corridor)
    return rm

def score(name, rm):
    rmv = rm[vox[:, 0], vox[:, 1], vox[:, 2]]
    fp = (rmv & ~truth_branch).sum(); fn = (~rmv & truth_branch_strict).sum()
    after = mask0 & ~rm; n_after = cc_label(after)[1]
    print(f"{name:<58} removed {rmv.sum():5d}  erosion(FP) {fp:5d}  remnant(FN) {fn:4d}  components after {n_after}")

print("\n--- T1 branch deletion variants (deleted = 42 branch points, retained = 706) ---")
score("SHIPPED: protect 1.00 r, 26-conn", rule(R, D, 1.00, 26))
score("protect 1.00 r, 6-conn (review probe's connectivity)", rule(R, D, 1.00, 6))
score("protect 1.15 r, 26-conn", rule(R, D, 1.15, 26))
score("protect 1.30 r, 26-conn", rule(R, D, 1.30, 26))
score("protect 1.00 r, 26-conn, corridor 1.5 r of deleted pts", rule(R, D, 1.00, 26, corridor=1.5))
score("protect 1.00 r, 26-conn, corridor 2.0 r of deleted pts", rule(R, D, 1.00, 26, corridor=2.0))
score("protect 1.15 r, 26-conn, corridor 2.0 r of deleted pts", rule(R, D, 1.15, 26, corridor=2.0))
truth_rm = np.zeros_like(mask0); truth_rm[vox[truth_branch_strict, 0], vox[truth_branch_strict, 1], vox[truth_branch_strict, 2]] = True
score("nearest-centreline assignment (ground truth itself)", truth_rm)

# ---- truncation step (MUST 5): deleted = sub-cut points, retained = active points (retained + branch for the clean case)
print("\n--- truncation step variants (deleted = 121 sub-cut points, retained = 748 active points) ---")
ACT = np.vstack([R, D])
truth_sc = (rel_SC < np.minimum(rel_R, rel_D)) & (rel_SC < 2.0)
truth_keep_shell = (~truth_sc) & (np.minimum(rel_R, rel_D) > 1.0)
print(f"ground truth sub-cut vessel voxels: {truth_sc.sum()}; retained-tree shell beyond 1.0 r: {truth_keep_shell.sum()}")
def score_sc(name, rm):
    rmv = rm[vox[:, 0], vox[:, 1], vox[:, 2]]
    fp = (rmv & ~truth_sc).sum(); fn = (~rmv & truth_sc).sum()
    print(f"{name:<58} removed {rmv.sum():5d}  erosion(FP) {fp:5d}  remnant(FN) {fn:4d}  components after {cc_label(mask0 & ~rm)[1]}")
score_sc("SHIPPED rule: protect 1.00 r, 26-conn", rule(ACT, SC, 1.00, 26))
score_sc("protect 1.00 r, 6-conn", rule(ACT, SC, 1.00, 6))
score_sc("protect 1.15 r, 26-conn", rule(ACT, SC, 1.15, 26))
score_sc("protect 1.00 r, 26-conn, corridor 2.0 r of sub-cut pts", rule(ACT, SC, 1.00, 26, corridor=2.0))
score_sc("protect 1.15 r, 26-conn, corridor 2.0 r of sub-cut pts", rule(ACT, SC, 1.15, 26, corridor=2.0))
