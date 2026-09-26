"""probe_t1_rule.py — the shipped T1 mask rule (delete within 1.10 r, restore within 1.00 r) vs a flood-fill rule, on scan 14."""
import sys, json
from pathlib import Path
import numpy as np, nibabel as nib
from scipy.ndimage import label as cc_label
HERE = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(HERE / "code"))
from severity_sweep import load
root, M1 = Path(sys.argv[1]), Path(sys.argv[2])
t = load(root, 14, "left", "discrete")
me = json.loads((next(M1.glob("*__T1_missed_branch__real")) / "mask_edit.json").read_text())["mask_edit"]
P = np.array([[q["x"], q["y"], q["z"]] for q in me["points_mm"]]); rdel = np.array([q["r_mm"] for q in me["points_mm"]])
img = nib.load(str(root / "segmentations" / "14.coronary.nii.gz")); lab = np.asarray(img.dataobj) > 0; inv = np.linalg.inv(img.affine)
flip = np.array([-1., -1., 1.])
act = np.where(t.active)[0]; xyz = t.xyz * 1e3
keep = np.array([i for i in act if not np.any(np.all(np.isclose(xyz[i], P), axis=1))])
vox = np.argwhere(lab); vox_mm = (img.affine @ np.c_[vox, np.ones(len(vox))].T)[:3].T
def near(pts_lps, radii, factor):
    out = np.zeros(len(vox), bool); q = pts_lps * flip
    for k in range(0, len(q), 64):
        d = np.linalg.norm(vox_mm[:, None, :] - q[None, k:k+64], axis=2); out |= (d <= factor * radii[None, k:k+64]).any(1)
    return out
protect = near(xyz[keep], t.r[keep] * 1e3, 1.00)
for f in (1.10, 1.30, 1.50):
    dele = near(P, rdel, f) & ~protect
    after = lab.copy(); after[vox[dele, 0], vox[dele, 1], vox[dele, 2]] = False
    _, n = cc_label(after); sizes = np.sort(np.bincount(cc_label(after)[0].ravel())[1:])[::-1]
    print(f"shipped rule, factor {f:.2f}: removed {dele.sum()} voxels; whole-mask components after = {n} (before {cc_label(lab)[1]}); island sizes {sizes[1:9].tolist()}")
# flood-fill alternative: delete the connected component(s) of (mask & ~protect) that contain a deleted centreline point
cand = lab.copy(); cand[vox[protect, 0], vox[protect, 1], vox[protect, 2]] = False
lbl, n = cc_label(cand)
ijk = np.round((inv @ np.c_[P * flip, np.ones(len(P))].T)[:3]).astype(int).T
ids = set(lbl[ijk[:, 0], ijk[:, 1], ijk[:, 2]].tolist()) - {0}
kill = np.isin(lbl, list(ids)); after = lab & ~kill
_, n2 = cc_label(after); sizes = np.sort(np.bincount(cc_label(after)[0].ravel())[1:])[::-1]
print(f"flood-fill rule: components seeded {sorted(ids)}; removed {kill.sum()} voxels; whole-mask components after = {n2}; sizes {sizes[:4].tolist()}")
print(f"deleted points that fell in the PROTECTED zone (carina, restored): {(lbl[ijk[:,0],ijk[:,1],ijk[:,2]]==0).sum()}/{len(P)}")
