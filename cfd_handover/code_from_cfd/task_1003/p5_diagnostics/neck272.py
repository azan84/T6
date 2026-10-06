"""Root cause of the lost outlet out_396 in P5 scan 272 (read-only; writes only to the output dir given).
Measures along R-PDA tree nodes 370-392: mask EDT radius (edited mask), lumen voxel count in the section plane,
section area / r_eq of the raw marching-cubes, smoothed and final surfaces, and the cfMesh background cell size there.
usage: python3 neck272.py <out_dir>"""
import csv, json, sys, os
import numpy as np, nibabel as nib, vtk
from scipy import ndimage

P5 = "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5"
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
rows = [r for r in csv.DictReader(open(f"{P5}/out/272/surface_radius_272_baseline.csv")) if r["segment"] == "R-PDA"]
rows = [r for r in rows if 370 <= int(r["tree_node"]) <= 392]
X = np.array([[float(r[k]) for k in ("x_mm", "y_mm", "z_mm")] for r in rows])          # LPS mm

img = nib.load(f"{P5}/out/272/mask_work/mask_edited.nii.gz"); m = np.asarray(img.dataobj) > 0
A = img.affine; sp = np.sqrt((A[:3, :3] ** 2).sum(0))
edt = ndimage.distance_transform_edt(m, sampling=sp)
Ainv = np.linalg.inv(A)
def vox(p_lps):  # frame_check of gates.json: LPS mm, affine RAS -> negate x,y
    ras = np.array([-p_lps[0], -p_lps[1], p_lps[2], 1.0]); return (Ainv @ ras)[:3]

def reader(path):
    r = vtk.vtkSTLReader() if path.endswith(".stl") else vtk.vtkXMLPolyDataReader(); r.SetFileName(path); r.Update(); return r.GetOutput()
surfs = {k: reader(f"{P5}/out/272/{p}") for k, p in (("raw_mc", "intermediate/raw_mc.vtp"), ("smoothed", "intermediate/smoothed.vtp"), ("final", "case.stl"))}
def section(poly, o, n, scale):
    pl = vtk.vtkPlane(); pl.SetOrigin(*(o * scale)); pl.SetNormal(*n)
    c = vtk.vtkCutter(); c.SetCutFunction(pl); c.SetInputData(poly); c.Update()
    s = vtk.vtkStripper(); s.SetInputConnection(c.GetOutputPort()); s.Update(); pd = s.GetOutput()
    best = None
    for i in range(pd.GetNumberOfCells()):
        ids = pd.GetCell(i).GetPointIds(); pts = np.array([pd.GetPoint(ids.GetId(j)) for j in range(ids.GetNumberOfIds())]) / scale
        if len(pts) < 3: continue
        d = np.linalg.norm(pts - o, axis=1).min()
        if d > 1.5: continue
        u = np.cross(n, [1, 0, 0]); u = u / np.linalg.norm(u) if np.linalg.norm(u) > 1e-6 else np.cross(n, [0, 1, 0]) / np.linalg.norm(np.cross(n, [0, 1, 0])); v = np.cross(n, u)
        q = np.c_[(pts - o) @ u, (pts - o) @ v]; area = 0.5 * abs(np.dot(q[:-1, 0], q[1:, 1]) - np.dot(q[1:, 0], q[:-1, 1]) + q[-1, 0] * q[0, 1] - q[0, 0] * q[-1, 1])
        if best is None or d < best[1]: best = (area, d)
    return best[0] if best else float("nan")

# unit check of the surface coordinates (STL in metres or mm)
scales = {k: (1e-3 if abs(np.array(p.GetBounds())).max() < 1.0 else 1.0) for k, p in surfs.items()}
res = []
for i, r in enumerate(rows):
    a, b = X[max(i - 1, 0)], X[min(i + 1, len(X) - 1)]; n = (b - a) / np.linalg.norm(b - a)
    iv = np.round(vox(X[i])).astype(int)
    rec = dict(tree_node=int(r["tree_node"]), s_mm=round(float(r["s_mm"]), 2), pkg_r_target_mm=float(r["pkg_r_target_mm"]),
               csv_r_eq_final=float(r["r_eq3D_mm"]), csv_r_inscribed_final=float(r["r_max_inscribed_mm"]),
               edt_at_node_mm=float(edt[tuple(iv)]) if m[tuple(iv)] else 0.0,
               edt_max_within_1mm=float(edt[tuple(slice(max(c - 3, 0), c + 4) for c in iv)].max()))
    for k, p in surfs.items():
        ar = section(p, X[i], n, scales[k])
        rec[f"r_eq_{k}_mm"] = float(np.sqrt(ar / np.pi)) if ar == ar else None
    res.append(rec)
# cfMesh sizing at the neck, parsed from the meshDict and the mesher log (not assumed): maxCellSize, root level, and membership of every neck
# node in every objectRefinement (sphere: distance to the centre <= radius; cone: projection inside the axis segment and distance <= radius0 = radius1)
import re
MD = open(f"{P5}/mesh/272/system/meshDict").read(); LOG = open(f"{P5}/mesh/272/log.cartesianMesh").read()
maxcell = float(re.search(r"maxCellSize\s+([\d.eE+-]+);", MD).group(1)); lvl = int(re.search(r"corresponds to octree level (\d+)", LOG).group(1))
objs = []
for m_ in re.finditer(r"(\w+)\s*\{\s*type (\w+);\s*cellSize ([\d.eE+-]+);([^}]*)\}", MD):
    n_, t_, cs_, body = m_.groups()
    vec = lambda k: np.array([float(a) for a in re.search(k + r"\s*\(([^)]*)\)", body).group(1).split()]) * 1e3
    sca = lambda k: float(re.search(k + r"\s+([\d.eE+-]+);", body).group(1)) * 1e3
    objs.append((n_, t_, float(cs_) * 1e3, (vec("centre"), sca("radius")) if t_ == "sphere" else (vec("p0"), vec("p1"), sca("radius0"))))
def covering(x):
    out = []
    for n_, t_, cs_, g in objs:
        if t_ == "sphere": inside = np.linalg.norm(x - g[0]) <= g[1]
        else:
            a_ = g[1] - g[0]; L_ = np.linalg.norm(a_); u_ = a_ / L_; t = (x - g[0]) @ u_; inside = 0 <= t <= L_ and np.linalg.norm(x - g[0] - t * u_) <= g[2]
        if inside: out.append(f"{n_} ({cs_:.3f} mm)")
    return out
for rec, x in zip(res, X): rec["xyz_mm"] = x.round(3).tolist(); rec["refinement_objects_covering"] = covering(x * 1.0)
sph = {n_: g for n_, t_, cs_, g in objs if t_ == "sphere"}
neck = X[[i for i, r in enumerate(rows) if int(r["tree_node"]) == 381][0]]
info = dict(voxel_spacing_mm=sp.tolist(), surface_units={k: ("m" if s == 1e-3 else "mm") for k, s in scales.items()},
            cfmesh_maxCellSize_mm=maxcell * 1e3, cfmesh_root_level=lvl, n_refinement_objects=len(objs),
            neck_node381_to_out_396_sphere_centre_mm=round(float(np.linalg.norm(neck - sph["out_396_ref"][0])), 3), out_396_sphere_radius_mm=sph["out_396_ref"][1],
            mesher_log_unconnected=bool(re.search(r"Mesh has 2 unconnected regions", LOG)), rows=res)
json.dump(info, open(f"{OUT}/neck272.json", "w"), indent=1)
print("spacing", sp, info["surface_units"])
for x in res: print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in x.items()})
