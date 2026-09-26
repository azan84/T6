"""Cap the 4 open flow-extension boundaries of the extended branched-tree surface with flat fan-
triangulated disks, each its own named STL 'solid' block (cfMesh's convention for boundary patches,
matching this project's existing make_stageA_geometry.py style: named solids -> named patches).
The tube's lateral surface (already triangulated, no cap) becomes 'solid wall'."""
import sys
import numpy as np
import pyvista as pv

def write_solid(f, name, A, B, C):
    """Vectorised normal computation (the original per-triangle np.cross/np.linalg.norm loop was the
    actual bottleneck - numpy's per-call overhead dominates at ~500k+ triangles; batching it into a
    handful of array ops instead of ~500k tiny ones is the fix, not more patience)."""
    N = np.cross(B - A, C - A)
    norm = np.linalg.norm(N, axis=1, keepdims=True)
    norm[norm < 1e-15] = 1.0
    N = N / norm
    f.write(f"solid {name}\n")
    lines = [
        f"facet normal {N[i,0]:.6e} {N[i,1]:.6e} {N[i,2]:.6e}\n outer loop\n"
        f"  vertex {A[i,0]:.8e} {A[i,1]:.8e} {A[i,2]:.8e}\n"
        f"  vertex {B[i,0]:.8e} {B[i,1]:.8e} {B[i,2]:.8e}\n"
        f"  vertex {C[i,0]:.8e} {C[i,1]:.8e} {C[i,2]:.8e}\n"
        " endloop\nendfacet\n"
        for i in range(len(A))
    ]
    f.write("".join(lines))
    f.write(f"endsolid {name}\n")

def cap_loop(pts, outward_normal):
    """Fan-triangulate a closed boundary loop (pts already ordered around the ring) from its centroid,
    oriented so the cap's normal points OUTWARD (away from the fluid domain, i.e. along outward_normal),
    matching the tube wall's own outward-normal convention. Returns (A,B,C) vertex arrays."""
    c = pts.mean(axis=0)
    n_pts = len(pts)
    A = np.tile(c, (n_pts, 1))
    B = pts
    C = np.roll(pts, -1, axis=0)
    n = np.cross(B - A, C - A)
    flip = (n @ outward_normal) < 0
    B2, C2 = B.copy(), C.copy()
    B2[flip], C2[flip] = C[flip], B[flip]
    return A, B2, C2

def order_loop(pts):
    """Order an unordered set of boundary-loop points into a ring by nearest-neighbour walk (the
    loops here are simple, near-circular, non-self-intersecting - a greedy walk is sufficient)."""
    remaining = list(range(len(pts)))
    order = [remaining.pop(0)]
    while remaining:
        last = pts[order[-1]]
        d = [np.linalg.norm(pts[i] - last) for i in remaining]
        j = int(np.argmin(d))
        order.append(remaining.pop(j))
    return pts[order]

def main(ds):
    surf = pv.read(f"extended_ds{ds}.vtp")
    edges = surf.extract_feature_edges(boundary_edges=True, feature_edges=False,
                                        manifold_edges=False, non_manifold_edges=False)
    conn = edges.connectivity(extraction_mode="all")
    rid = conn.point_data["RegionId"]

    # identify which loop is which by centroid position (established from the flow-extension check)
    def classify(centroid_mm):
        x, y, z = centroid_mm
        if x < 0: return "inlet"
        if abs(y - 42.03) < 2 and x > 80: return "outletA"
        if abs(y - 17.03) < 2: return "outletB1"
        if abs(y + 2.04) < 2: return "outletB2"
        raise ValueError(f"unclassified boundary loop centroid {centroid_mm}")

    faces = surf.faces.reshape(-1, 4)[:, 1:4]   # vectorised - the per-cell Python loop was the bottleneck
    V = surf.points
    Aw, Bw, Cw = V[faces[:, 0]], V[faces[:, 1]], V[faces[:, 2]]

    out_path = f"branched_ds{ds}.stl"
    with open(out_path, "w") as f:
        write_solid(f, "wall", Aw, Bw, Cw)
        for r in np.unique(rid):
            pts = conn.points[rid == r]
            centroid_mm = pts.mean(axis=0) * 1e3
            name = classify(centroid_mm)
            ordered = order_loop(pts)
            # outward normal: along the local tube axis, pointing OUT of the domain (away from the
            # bulk of the surface) - approximate via centroid-to-loop-centroid direction from the
            # overall surface centroid, which is correct for a simple tree with no U-turns.
            overall_c = surf.points.mean(axis=0)
            outward = ordered.mean(axis=0) - overall_c
            outward /= np.linalg.norm(outward)
            Ac, Bc, Cc = cap_loop(ordered, outward)
            write_solid(f, name, Ac, Bc, Cc)
            print(f"  ds={ds}: capped {name} with {len(Ac)} triangles, centroid(mm)={centroid_mm}")
    print(f"wrote {out_path}")

if __name__ == "__main__":
    for ds in ("00", "60"):
        main(ds)
