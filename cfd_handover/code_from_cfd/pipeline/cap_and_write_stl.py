"""Cap each open boundary loop of a flow-extended surface (cfMesh needs a watertight STL; the caps are
still flow boundaries, just labelled as distinct 'solid' patches, matching this project's Stage A STL
convention in make_stageA_geometry.py) and write a multi-solid STL: wall + inlet + one outlet per label.
"""
import numpy as np
import pyvista as pv


def cap_and_label(surf: pv.PolyData, outlet_labels: dict) -> pv.PolyData:
    """outlet_labels: {name: (x,y,z) approx centroid in mm} - e.g. {'inlet': ..., 'outlet_LAD': ...}.
    Returns a PolyData with a 'patch' cell array (strings encoded as ints via a side table)."""
    n_before = surf.n_cells
    filled = surf.fill_holes(hole_size=1e6)   # generous hole_size: our holes are all we want capped
    n_after = filled.n_cells
    assert n_after > n_before, "fill_holes added no faces - are the boundary loops actually open?"
    # classify: original faces -> 'wall'; new faces -> nearest label by cell-centroid distance
    patch = np.array(["wall"] * n_after, dtype=object)
    centers = filled.cell_centers().points
    names = list(outlet_labels.keys())
    label_xyz = np.array([outlet_labels[k] for k in names])
    new_cell_ids = np.arange(n_before, n_after)   # fill_holes appends new cells after the originals
    d = np.linalg.norm(centers[new_cell_ids][:, None, :] - label_xyz[None, :, :], axis=2)
    nearest = d.argmin(axis=1)
    for i, cid in enumerate(new_cell_ids):
        patch[cid] = names[nearest[i]]
    filled.cell_data["patch"] = patch
    counts = {n: int((patch == n).sum()) for n in ["wall"] + names}
    print("cap face counts:", counts)
    return filled


def write_multisolid_stl(mesh: pv.PolyData, out_path: str, scale: float = 1e-3):
    """scale: applied to point coordinates before writing - default 1e-3 converts this project's mm
    (LPS, ImageCAS-X convention) to metres (OpenFOAM/cfMesh convention, matching make_stageA_geometry.py's
    own `pts_mm * 1e-3` pattern)."""
    patch = mesh.cell_data["patch"]
    pts = mesh.points * scale
    faces = mesh.faces.reshape(-1, 4)[:, 1:]
    with open(out_path, "w") as f:
        for name in sorted(set(patch)):
            f.write(f"solid {name}\n")
            idx = np.where(patch == name)[0]
            for ci in idx:
                a, b, c = pts[faces[ci]]
                n = np.cross(b - a, c - a)
                norm = np.linalg.norm(n)
                n = n / norm if norm > 0 else np.array([0.0, 0.0, 1.0])
                f.write(f"facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n outer loop\n")
                for v in (a, b, c):
                    f.write(f"  vertex {v[0]:.6e} {v[1]:.6e} {v[2]:.6e}\n")
                f.write(" endloop\nendfacet\n")
            f.write(f"endsolid {name}\n")
    print("wrote", out_path)
