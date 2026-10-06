"""Robust local check of the surfaceCheck self-intersection point of P5 scan 272 (read-only): for every pair of triangles of the final STL that
lie within R mm of the point (selected by ANY vertex within R, not by centroid) and do not share a vertex, the exact minimum distance between the
two triangles (0 if they intersect or touch, incl. coplanar overlap) = min over the 6 vertex-triangle and 9 edge-edge distances, with an explicit
edge-triangle crossing test; for edge-adjacent pairs the fold angle (normals nearly opposite = fold-over); for vertex-adjacent pairs the
opposite-edge-triangle crossing test. Also the triangle quality statistics of the neighbourhood.
usage: tritri272.py R_mm out.json"""
import sys, json, numpy as np, vtk
from collections import defaultdict
STL = "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/out/272/case.stl"
import os
P = np.array([float(x) for x in os.environ.get("POINT_M", "0.00358718 -0.195366 0.233808").split()]); R = float(sys.argv[1]) * 1e-3
r = vtk.vtkSTLReader(); r.SetFileName(STL); r.MergingOn(); r.Update(); pd = r.GetOutput()
pts = np.array([pd.GetPoint(i) for i in range(pd.GetNumberOfPoints())]); tris = np.array([[pd.GetCell(i).GetPointId(j) for j in range(3)] for i in range(pd.GetNumberOfCells())])
sel = np.where((np.linalg.norm(pts[tris] - P, axis=2) < R).any(1))[0]
T = pts[tris[sel]]; lo, hi = T.min(1), T.max(1); MARGIN = 50e-6

def pt_tri(p, a, b, c):  # closest distance point-triangle (Ericson, Real-Time Collision Detection 5.1.5)
    ab, ac, ap = b - a, c - a, p - a; d1, d2 = ab @ ap, ac @ ap
    if d1 <= 0 and d2 <= 0: return np.linalg.norm(p - a)
    bp = p - b; d3, d4 = ab @ bp, ac @ bp
    if d3 >= 0 and d4 <= d3: return np.linalg.norm(p - b)
    vc = d1 * d4 - d3 * d2
    if vc <= 0 and d1 >= 0 and d3 <= 0: return np.linalg.norm(p - (a + d1 / (d1 - d3) * ab))
    cp = p - c; d5, d6 = ab @ cp, ac @ cp
    if d6 >= 0 and d5 <= d6: return np.linalg.norm(p - c)
    vb = d5 * d2 - d1 * d6
    if vb <= 0 and d2 >= 0 and d6 <= 0: return np.linalg.norm(p - (a + d2 / (d2 - d6) * ac))
    va = d3 * d6 - d5 * d4
    if va <= 0 and (d4 - d3) >= 0 and (d5 - d6) >= 0: return np.linalg.norm(p - (b + (d4 - d3) / ((d4 - d3) + (d5 - d6)) * (c - b)))
    den = 1 / (va + vb + vc); return np.linalg.norm(p - (a + ab * vb * den + ac * vc * den))
def seg_seg(p1, q1, p2, q2):  # Ericson 5.1.9
    d1, d2, r_ = q1 - p1, q2 - p2, p1 - p2; a, e, f = d1 @ d1, d2 @ d2, d2 @ r_
    c = d1 @ r_; b = d1 @ d2; den = a * e - b * b
    s = np.clip((b * f - c * e) / den, 0, 1) if den > 1e-30 else 0.0
    t = (b * s + f) / e
    if t < 0: t, s = 0.0, np.clip(-c / a, 0, 1)
    elif t > 1: t, s = 1.0, np.clip((b - c) / a, 0, 1)
    return np.linalg.norm(p1 + d1 * s - (p2 + d2 * t))
def seg_cross(p0, p1, a, b, c):
    e1, e2 = b - a, c - a; d = p1 - p0; h = np.cross(d, e2); det = e1 @ h
    if abs(det) < 1e-30: return False
    f = 1 / det; s = p0 - a; u = f * (s @ h)
    if u < 0 or u > 1: return False
    q = np.cross(s, e1); v = f * (d @ q)
    if v < 0 or u + v > 1: return False
    t = f * (e2 @ q); return 0 <= t <= 1
def tri_dist(A, B):
    if any(seg_cross(A[k], A[(k + 1) % 3], *B) for k in range(3)) or any(seg_cross(B[k], B[(k + 1) % 3], *A) for k in range(3)): return 0.0
    d = min(min(pt_tri(A[k], *B) for k in range(3)), min(pt_tri(B[k], *A) for k in range(3)))
    return min(d, min(seg_seg(A[i], A[(i + 1) % 3], B[j], B[(j + 1) % 3]) for i in range(3) for j in range(3)))
nrm = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); area2 = np.linalg.norm(nrm, axis=1); nrm = nrm / area2[:, None]
edge_len = np.stack([np.linalg.norm(T[:, (k + 1) % 3] - T[:, k], axis=1) for k in range(3)], 1)
quality = 2 * np.sqrt(3) * area2 / (edge_len ** 2).sum(1)
vt = defaultdict(set)
for li, ti in enumerate(sel):
    for v in tris[ti]: vt[v].add(li)
npairs = 0; dmin = (np.inf, None); folds = []; vadj_cross = []
for i in range(len(sel)):
    cand = np.where(np.all((lo <= hi[i] + MARGIN) & (hi >= lo[i] - MARGIN), axis=1))[0]
    for j in cand[cand > i]:
        shared = set(tris[sel[i]]) & set(tris[sel[j]])
        if len(shared) == 2:
            dot = float(nrm[i] @ nrm[j]);
            if dot < -0.5: folds.append((int(sel[i]), int(sel[j]), dot))
            continue
        if len(shared) == 1:
            A, B = T[i], T[j]; v = list(shared)[0]
            oa = [A[k] for k in range(3) if tris[sel[i]][k] != v]; ob = [B[k] for k in range(3) if tris[sel[j]][k] != v]
            if seg_cross(oa[0], oa[1], *B) or seg_cross(ob[0], ob[1], *A): vadj_cross.append((int(sel[i]), int(sel[j])))
            continue
        npairs += 1; d = tri_dist(T[i], T[j])
        if d < dmin[0]: dmin = (d, (int(sel[i]), int(sel[j])))
res = dict(point_m=P.tolist(), R_mm=R * 1e3, selection="triangles with ANY vertex within R", n_triangles=int(len(sel)), bbox_margin_um=MARGIN * 1e6,
           n_nonadjacent_pairs_tested=npairs, min_nonadjacent_triangle_distance_um=(None if dmin[1] is None else round(dmin[0] * 1e6, 3)), closest_pair=dmin[1],
           pairs_beyond_margin_not_tested="non-adjacent pairs whose bounding boxes are > 50 um apart (their distance is > 50 um)",
           edge_adjacent_folds_dot_lt_minus0p5=folds, vertex_adjacent_opposite_edge_crossings=vadj_cross,
           quality_min=round(float(quality.min()), 4), quality_p1=round(float(np.percentile(quality, 1)), 4), edge_um_min=round(float(edge_len.min() * 1e6), 2), edge_um_max=round(float(edge_len.max() * 1e6), 2))
json.dump(res, open(sys.argv[2], "w"), indent=1); print(json.dumps(res, indent=1))
