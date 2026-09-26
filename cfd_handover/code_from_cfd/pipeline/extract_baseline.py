"""Extract the LEFT-tree baseline surface for scan 837 from the ImageCAS-X mask (spec Sec.6.1b: from
the mask, not the shipped .vtk surface), via marching cubes at voxel-index resolution then an affine
transform to LPS mm (matching the centerline's coordinate convention: NIfTI affine is RAS, negate x,y).
"""
import sys
import numpy as np
import nibabel as nib
from skimage import measure
import pyvista as pv

ROOT = "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/imagecas_x_raw/extracted/ImageCAS-X_dataset"
SCAN = 837
LEFT_LABELS = [1, 2, 3, 4, 5, 8]   # LM, LAD, LCX, D1, D2, IM (verified against this scan's centreline)
OUT = "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot"

def mask_to_lps_surface(mask_bool: np.ndarray, affine: np.ndarray) -> pv.PolyData:
    verts_ijk, faces, normals, _ = measure.marching_cubes(mask_bool.astype(np.float32), level=0.5)
    ijk1 = np.c_[verts_ijk, np.ones(len(verts_ijk))]
    ras = (affine @ ijk1.T).T[:, :3]
    lps = ras * np.array([-1.0, -1.0, 1.0])   # RAS -> LPS, matches centreline convention
    n = len(faces)
    vtk_faces = np.c_[np.full(n, 3), faces].ravel()
    return pv.PolyData(lps, vtk_faces)

def extract(labels, out_path, edit_fn=None):
    img = nib.load(f"{ROOT}/segmentations/{SCAN}.coronary.nii.gz")
    data = np.asarray(img.dataobj)
    if edit_fn is not None:
        data = edit_fn(data.copy())
    mask = np.isin(data, labels)
    surf = mask_to_lps_surface(mask, img.affine)
    surf = surf.connectivity(extraction_mode="largest")
    surf.save(out_path)
    print(f"wrote {out_path}: {surf.n_points} points, {surf.n_cells} cells, "
          f"bounds={np.round(surf.bounds, 1)}")
    return surf

if __name__ == "__main__":
    extract(LEFT_LABELS, f"{OUT}/baseline/raw_mc.vtp")
