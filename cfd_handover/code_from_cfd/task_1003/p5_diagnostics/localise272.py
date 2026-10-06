"""Localise the region cfMesh deleted in P5 scan 272 (read-only): STL vertices of the final surface that are far (> 0.3 mm) from the meshed wall
(wall patch extracted by surfaceMeshExtract into a VTK file), grouped by the nearest tree node / segment of the package-derived centreline sampling
(surface_radius_272_baseline.csv). usage: localise272.py <mesh_wall.vtk|.vtp|.obj> <out.json>"""
import sys, json, csv, numpy as np, vtk
from scipy.spatial import cKDTree
P5 = "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5"
def read(path):
    r = vtk.vtkXMLPolyDataReader() if path.endswith(".vtp") else (vtk.vtkOBJReader() if path.endswith(".obj") else vtk.vtkPolyDataReader())
    r.SetFileName(path); r.Update(); o = r.GetOutput(); return np.array([o.GetPoint(i) for i in range(o.GetNumberOfPoints())])
r = vtk.vtkSTLReader(); r.SetFileName(f"{P5}/out/272/case.stl"); r.MergingOn(); r.Update(); s = r.GetOutput()
stl = np.array([s.GetPoint(i) for i in range(s.GetNumberOfPoints())]) * 1e3                 # m -> mm
wall = read(sys.argv[1]); wall = wall * (1e3 if np.abs(wall).max() < 1.0 else 1.0)
d, _ = cKDTree(wall).query(stl)
far = stl[d > 0.3]
rows = list(csv.DictReader(open(f"{P5}/out/272/surface_radius_272_baseline.csv")))
X = np.array([[float(x[k]) for k in ("x_mm", "y_mm", "z_mm")] for x in rows]); _, ni = cKDTree(X).query(far) if len(far) else (None, [])
by = {}
for i in ni: key = (rows[i]["segment"], int(rows[i]["tree_node"])); by[key] = by.get(key, 0) + 1
nodes = sorted(by); segs = sorted(set(k[0] for k in nodes))
res = dict(n_stl_vertices=len(stl), n_wall_points=len(wall), threshold_mm=0.3, n_far=int(len(far)), far_segments=segs,
           far_tree_node_range={sg: [min(k[1] for k in nodes if k[0] == sg), max(k[1] for k in nodes if k[0] == sg)] for sg in segs},
           far_count_by_node={f"{a}:{b}": c for (a, b), c in sorted(by.items())},
           max_distance_mm=round(float(d.max()), 3))
json.dump(res, open(sys.argv[2], "w"), indent=1); print(json.dumps({k: v for k, v in res.items() if k != "far_count_by_node"}, indent=1))
