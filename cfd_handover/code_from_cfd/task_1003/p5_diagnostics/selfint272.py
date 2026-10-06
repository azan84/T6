"""Inspect the single self-intersection point of P5 scan 272 final STL (read-only). Lists the triangles within R of the
point, tests every non-adjacent triangle pair there for an edge-triangle crossing, and reports the ring/loop indices of
the inlet extension the crossing triangles belong to (geometry only).  usage: python3 selfint272.py <out_dir>"""
import sys, os, json, numpy as np, vtk
STL = "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/out/272/case.stl"
P = np.array([0.00358718, -0.195366, 0.233808]); R = float(os.environ.get('R_MM', '0.6')) * 1e-3
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
r = vtk.vtkSTLReader(); r.SetFileName(STL); r.MergingOn(); r.Update(); pd = r.GetOutput()
pts = np.array([pd.GetPoint(i) for i in range(pd.GetNumberOfPoints())])
tris = np.array([[pd.GetCell(i).GetPointId(j) for j in range(3)] for i in range(pd.GetNumberOfCells())])
cen = pts[tris].mean(1); near = np.where(np.linalg.norm(cen - P, axis=1) < R)[0]

def seg_tri(p0, p1, a, b, c, eps=1e-15):
    e1, e2 = b - a, c - a; d = p1 - p0; h = np.cross(d, e2); det = np.dot(e1, h)
    if abs(det) < eps: return False
    f = 1 / det; s = p0 - a; u = f * np.dot(s, h)
    if u < 0 or u > 1: return False
    q = np.cross(s, e1); v = f * np.dot(d, q)
    if v < 0 or u + v > 1: return False
    t = f * np.dot(e2, q); return 0 < t < 1
hits = []
lo = pts[tris[near]].min(1); hi = pts[tris[near]].max(1)
for a_, i in enumerate(near):
    cand = near[a_ + 1:][np.all((lo[a_ + 1:] <= hi[a_] + 1e-9) & (hi[a_ + 1:] >= lo[a_] - 1e-9), axis=1)]
    for j in cand:
        if set(tris[i]) & set(tris[j]): continue
        A, B = pts[tris[i]], pts[tris[j]]
        if any(seg_tri(A[k], A[(k + 1) % 3], *B) for k in range(3)) or any(seg_tri(B[k], B[(k + 1) % 3], *A) for k in range(3)):
            hits.append((int(i), int(j)))
def tri_info(i):
    v = pts[tris[i]]; e = [np.linalg.norm(v[k] - v[(k + 1) % 3]) for k in range(3)]
    area = 0.5 * np.linalg.norm(np.cross(v[1] - v[0], v[2] - v[0]))
    return dict(tri=int(i), verts=[int(x) for x in tris[i]], edges_um=[round(x * 1e6, 2) for x in e], area_um2=round(area * 1e12, 3),
                min_angle_deg=round(float(min(np.degrees(np.arccos(np.clip(np.dot(v[(k+1)%3]-v[k], v[(k+2)%3]-v[k]) /
                     (np.linalg.norm(v[(k+1)%3]-v[k]) * np.linalg.norm(v[(k+2)%3]-v[k])), -1, 1))) for k in range(3))), 3),
                normal=(np.cross(v[1] - v[0], v[2] - v[0]) / (2 * area)).round(4).tolist())
res = dict(point_m=P.tolist(), n_triangles_within_R=int(len(near)), R_mm=R * 1e3, crossing_pairs=[[tri_info(i), tri_info(j)] for i, j in hits])
# duplicate / near-duplicate vertex check in the neighbourhood
nv = np.unique(tris[near])[:3000]; d = np.linalg.norm(pts[nv][:, None] - pts[nv][None], axis=2) + np.eye(len(nv))
res["min_vertex_spacing_um"] = round(float(d.min() * 1e6), 3)
json.dump(res, open(f"{OUT}/selfint272_R{R*1e3:g}mm.json", "w"), indent=1)
print(json.dumps(res, indent=1)[:4000])
