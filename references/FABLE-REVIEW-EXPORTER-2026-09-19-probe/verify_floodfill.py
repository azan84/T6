"""verify_floodfill.py — MUST 3 / MUST 5 verification. EXECUTE the reference implementation shipped inside
mask_edit.json (verbatim, via exec) against the real scan-14 mask, then apply the same rule to the truncation step
(sub_cut_points_mm) and to the composed T1 build (truncation, then branch deletion).

usage: verify_floodfill.py <data_root> <m1_package_dir>
"""
import sys, json, os
from pathlib import Path
import numpy as np, nibabel as nib
from scipy.ndimage import label as cc_label

root, M1 = Path(sys.argv[1]).expanduser(), Path(sys.argv[2])
if not (root / "centerlines").is_dir(): root = next(c for c in root.iterdir() if (c / "centerlines").is_dir())
mask_nii = root / "segmentations" / "14.coronary.nii.gz"
img = nib.load(str(mask_nii)); mask0 = np.asarray(img.dataobj) > 0
sp = np.array(img.header.get_zooms()[:3])
print(f"mask {mask0.shape} spacing {sp} voxels {mask0.sum()} components {cc_label(mask0)[1]}")

def comps(m):
    lab, n = cc_label(m); sizes = np.sort(np.bincount(lab.ravel())[1:])[::-1]
    return n, sizes[:6].tolist()

pk = {p.name.split("__")[1]: p for p in M1.iterdir() if p.is_dir()}
t1 = pk["T1_missed_branch"]
edit = json.loads((t1 / "mask_edit.json").read_text())
me = edit["mask_edit"]
print(f"T1 package: {len(me['deleted_points_mm'])} deleted points, {len(me['retained_points_mm'])} retained points, "
      f"{len(edit['sub_cut_points_mm'])} sub-cut points")

# ---- 1. run the shipped reference implementation VERBATIM (it reads mask_edit.json from cwd and MASK_NII)
os.chdir(t1)
code = me["reference_implementation"]
ns = {"MASK_NII": str(mask_nii)}
exec(code, ns)
out = np.asarray(nib.load("mask_edited.nii.gz").dataobj) > 0
removed = mask0 & ~out
n_after, sizes = comps(out)
print(f"\n[MUST 3] shipped reference implementation, executed verbatim on T1 package:")
print(f"  voxels removed = {removed.sum()}   components after = {n_after} (before {cc_label(mask0)[1]})   sizes {sizes}")
print(f"  added voxels (should be 0) = {(out & ~mask0).sum()}")
# which deleted points were in the protected zone (carina) — reported by the exporter's rule as expected
to_ijk = ns["to_ijk"]; lab = ns["lab"]
ijk = np.round(to_ijk([[p["x"], p["y"], p["z"]] for p in me["deleted_points_mm"]])).astype(int)
in_lumen = mask0[ijk[:, 0], ijk[:, 1], ijk[:, 2]]
print(f"  deleted points inside the ORIGINAL lumen (frame check, MUST 2): {in_lumen.sum()}/{len(ijk)}")
print(f"  deleted points in the protected zone (label 0, restored at carina): {(lab[ijk[:,0],ijk[:,1],ijk[:,2]]==0).sum()}/{len(ijk)}")
print(f"  seeded components: {sorted(ns['kill'])}")
# does anything removed lie close to a RETAINED point (i.e. shell erosion of a kept vessel)?
R = np.array([[p["x"], p["y"], p["z"], p["r_mm"]] for p in me["retained_points_mm"]])
rv = np.argwhere(removed); rv_mm = (img.affine @ np.c_[rv, np.ones(len(rv))].T)[:3].T * np.array([-1, -1, 1])   # RAS->LPS
def min_rel_dist(pts_mm, cl):
    best = np.full(len(pts_mm), np.inf)
    for k in range(0, len(cl), 128):
        d = np.linalg.norm(pts_mm[:, None, :] - cl[None, k:k+128, :3], axis=2) / cl[None, k:k+128, 3]
        best = np.minimum(best, d.min(1))
    return best
rel = min_rel_dist(rv_mm, R)
print(f"  removed voxels vs nearest RETAINED point, in units of that point's r: min {rel.min():.2f}, "
      f"5th pct {np.percentile(rel,5):.2f}, median {np.median(rel):.2f}; within 1.3 r of a retained point: {(rel<1.3).sum()}")
os.remove("mask_edited.nii.gz")

# ---- 2. the truncation step (MUST 5): same rule, retained = active centreline (vtp points), deleted = sub_cut_points
import pyvista as pv
def run_rule(mask, retained, deleted, factor=1.00):
    ball, label = ns["ball"], cc_label
    protect = np.zeros_like(mask)
    ns["mask"] = mask
    for p in retained:
        sl, b = ball(to_ijk([[p[0], p[1], p[2]]])[0], factor * p[3]); protect[sl] |= b
    cand = mask & ~protect
    lab, n = label(cand, structure=np.ones((3, 3, 3)))
    q = np.round(to_ijk([[p[0], p[1], p[2]] for p in deleted])).astype(int)
    seeds = lab[q[:, 0], q[:, 1], q[:, 2]]
    kill = set(seeds.tolist()) - {0}
    out = mask & ~np.isin(lab, list(kill))
    return out, kill, (seeds == 0).sum(), (~mask[q[:, 0], q[:, 1], q[:, 2]]).sum()

for name in ("clean_nolesion", "T1_missed_branch"):
    d = pk[name]; ed = json.loads((d / "mask_edit.json").read_text())
    vtp = pv.read(str(d / "centreline.vtp"))
    retained = np.c_[vtp.points, vtp.point_data["r_source_mm"]]
    subcut = np.array([[p["x"], p["y"], p["z"], p["r_mm"]] for p in ed["sub_cut_points_mm"]])
    out1, kill, n_prot, n_outside = run_rule(mask0, retained, subcut)
    n1, s1 = comps(out1)
    rem1 = mask0 & ~out1
    print(f"\n[MUST 5] truncation flood-fill on {name}: {len(subcut)} sub-cut seeds -> {len(kill)} components killed, "
          f"removed {rem1.sum()} voxels; components after {n1} sizes {s1}; seeds in protected zone {n_prot}; "
          f"seeds outside lumen {n_outside}")
    rv = np.argwhere(rem1); rv_mm = (img.affine @ np.c_[rv, np.ones(len(rv))].T)[:3].T * np.array([-1, -1, 1])
    rel = min_rel_dist(rv_mm, retained); rel_s = min_rel_dist(rv_mm, subcut)
    print(f"  removed voxels: nearest retained point rel-dist min {rel.min():.2f} median {np.median(rel):.2f}; "
          f"nearest sub-cut point rel-dist median {np.median(rel_s):.2f}; "
          f"voxels closer (relative) to a retained than to a sub-cut point: {(rel < rel_s).sum()}")
    # what of the retained tree lies OUTSIDE 1.0 r of the centreline in the original mask? (this is the shell that a
    # flood fill could eat if it were connected to a seed)
    if name == "T1_missed_branch":
        # composed build: truncation first, then the branch deletion on the truncated mask
        deleted = np.array([[p["x"], p["y"], p["z"], p["r_mm"]] for p in me["deleted_points_mm"]])
        ret2 = np.array([[p["x"], p["y"], p["z"], p["r_mm"]] for p in me["retained_points_mm"]])
        out2, kill2, n_prot2, _ = run_rule(out1, ret2, deleted)
        n2, s2 = comps(out2)
        print(f"  composed (truncate, then delete branch): removed {(out1 & ~out2).sum()} more voxels -> total "
              f"{(mask0 & ~out2).sum()}; components after {n2} sizes {s2}; deleted seeds in protected zone {n_prot2}")
        # the branch's sub-cut tail: is it gone after the composed build?
        out3, kill3, _, _ = run_rule(mask0, ret2, deleted)
        print(f"  branch deletion alone on the untruncated mask removed {(mask0 & ~out3).sum()} voxels "
              f"(reference value 855)")
