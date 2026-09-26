"""Rebuild an M1 case STL from the PRE-remesh clipped surface (skipping the coarse remesh step that cut
chords across the narrow lumens), with straight 20mm flow extensions and planar fan caps.

usage: rebuild_surface.py <pre_remesh.vtp (mm)> <old_case.stl (m, for cap labels)> <out.stl> [ext_mm] [ds_mm]
"""
import sys
import numpy as np
import pyvista as pv

pre_fn, old_stl, out_fn = sys.argv[1:4]
EXT = float(sys.argv[4]) if len(sys.argv) > 4 else 20.0
DS = float(sys.argv[5]) if len(sys.argv) > 5 else 0.3

surf = pv.read(pre_fn).extract_surface(algorithm="dataset_surface").triangulate().clean()
surf = surf.compute_normals(consistent_normals=True, auto_orient_normals=True, split_vertices=False)
P = np.asarray(surf.points, float)
F = surf.faces.reshape(-1, 4)[:, 1:].copy()

# directed boundary edges: (u,v) as they appear in a face, whose reverse never appears
directed = {}
for f in F:
    for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
        directed[(a, b)] = directed.get((a, b), 0) + 1
bnd = {a: b for (a, b) in directed if (b, a) not in directed}
loops = []
seen = set()
for s in bnd:
    if s in seen:
        continue
    loop = [s]; seen.add(s); v = bnd[s]
    while v != s:
        loop.append(v); seen.add(v); v = bnd[v]
    loops.append(np.array(loop))
print(f"{len(loops)} boundary loops, sizes {[len(l) for l in loops]}")

# old cap centroids (mm) for labelling
caps = {}; cur = None; buf = []
for line in open(old_stl):
    t = line.split()
    if not t:
        continue
    if t[0] == "solid":
        cur = t[1]; caps.setdefault(cur, [])
    elif t[0] == "vertex" and cur != "wall":
        caps[cur].append([float(x) * 1e3 for x in t[1:4]])
caps = {k: np.mean(v, axis=0) for k, v in caps.items() if k != "wall" and v}

pts = [P]; tris = [F]; labels = ["wall"] * len(F); npts = len(P)
for loop in loops:
    L = P[loop]; c = L.mean(0)
    n = np.linalg.svd(L - c)[2][2]
    near = P[np.linalg.norm(P - c, axis=1) < 3 * np.linalg.norm(L - c, axis=1).max()]
    if np.dot(near.mean(0) - c, n) > 0:
        n = -n                                    # n points out of the vessel
    nring = int(np.ceil(EXT / DS)); ds = EXT / nring; m = len(loop)
    idx_prev = loop
    for k in range(1, nring + 1):
        ring = L + k * ds * n
        idx = np.arange(npts, npts + m); npts += m; pts.append(ring)
        # boundary edge (u->v) belongs to an existing face, so the new quad runs v->u on its side
        for i in range(m):
            u0, v0 = idx_prev[i], idx_prev[(i + 1) % m]
            u1, v1 = idx[i], idx[(i + 1) % m]
            tris.append(np.array([[v0, u0, u1], [v0, u1, v1]]))
            labels += ["wall", "wall"]
        idx_prev = idx
    # planar fan cap (orientation continues the boundary direction reversed)
    ce = npts; npts += 1; pts.append((L + EXT * n).mean(0)[None])
    name = min(caps, key=lambda k: np.linalg.norm(caps[k] - (c + EXT * n)))
    for i in range(m):
        tris.append(np.array([[idx_prev[(i + 1) % m], idx_prev[i], ce]]))
        labels.append(name)
    print(f"  loop n={m:3d} -> {name:11s} (cap-centroid mismatch vs old STL "
          f"{np.linalg.norm(caps[name] - (c + EXT * n)):.3f} mm)")

P2 = np.vstack(pts); F2 = np.vstack(tris); lab = np.array(labels)
assert len(set(lab) - {"wall"}) == len(loops), "cap labels not unique"
# orientation: outward (positive signed volume)
vol = np.einsum("ij,ij->i", P2[F2[:, 0]], np.cross(P2[F2[:, 1]], P2[F2[:, 2]])).sum() / 6
if vol < 0:
    F2 = F2[:, ::-1]; vol = -vol
print(f"closed volume {vol:.2f} mm3, {len(F2)} triangles")

with open(out_fn, "w") as f:
    for name in sorted(set(lab)):
        f.write(f"solid {name}\n")
        for tri in F2[lab == name]:
            a, b, c = P2[tri] * 1e-3
            nn = np.cross(b - a, c - a); nn /= (np.linalg.norm(nn) or 1)
            f.write(f"facet normal {nn[0]:.6e} {nn[1]:.6e} {nn[2]:.6e}\n outer loop\n")
            for v in (a, b, c):
                f.write(f"  vertex {v[0]:.9e} {v[1]:.9e} {v[2]:.9e}\n")
            f.write(" endloop\nendfacet\n")
        f.write(f"endsolid {name}\n")
print("wrote", out_fn)
