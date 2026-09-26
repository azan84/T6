"""Build the lesion80 OPEN surface (mm) from the pre-remesh baseline surface: 80 %DS raised-cosine lesion in the proximal LAD.
See lesion80_design.md. No remeshing tool: tangent-frame radial scaling + conforming local edge-split refinement.

usage: build_lesion80_surface.py [out.vtp]
"""
import sys, os, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pyvista as pv
from scipy.spatial import cKDTree
from scipy.interpolate import splprep, splev
from outlets_837 import build_tree
from pullback_compare import node_xyz, path_to

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = f"{BASE}/baseline/clipped_final.vtp"
from lesion_profile import PR
S_C, LEN, DS_FRAC = PR["S_C"], PR["LEN"], PR["DS"]   # window centre (mm arc from ostium), length, diameter stenosis (profile; default = audited lesion80)
MAX_EDGE = 0.15                                # mm, post-deformation target edge inside the window
LAD_SID = PR["SID"]                            # 0D segment holding the window (lesion80: seg2 = proximal LAD, arc 15.0-32.0; lesion_mid: seg3, arc 32.9-70.7)

def f_of_s(s):
    x = (s - S_C) / (LEN / 2)
    w = np.where(np.abs(x) < 1, 0.5 * (1 + np.cos(np.pi * np.clip(x, -1, 1))), 0.0)
    return 1 - DS_FRAC * w, w

def build_frames(T):
    leaf = [v for v in T.leaves if T.label[v] == "LAD"][0]
    nodes = path_to(T, int(leaf))
    xyz = np.array([node_xyz(T, n) for n in nodes])
    arc_poly = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(xyz, axis=0), axis=1))])
    keep = arc_poly < PR["KEEP"]                # only the part up to the profile's KEEP arc is needed
    xyz, arc_poly, nodes = xyz[keep], arc_poly[keep], np.array(nodes)[keep]
    # smoothing spline for tangents (sigma ~0.1 mm on ~0.4 mm node spacing)
    u = arc_poly / arc_poly[-1]
    tck, _ = splprep(xyz.T, u=u, s=len(xyz) * 0.1 ** 2, k=3)
    uu = np.linspace(0, 1, int(arc_poly[-1] / 0.02))
    c = np.array(splev(uu, tck)).T
    d1 = np.array(splev(uu, tck, der=1)).T
    t = d1 / np.linalg.norm(d1, axis=1)[:, None]
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))])
    return dict(c=c, t=t, s=s, nodes=nodes, xyz=xyz, arc_poly=arc_poly)

def build_branch_tree(T):
    P, lab = [], []
    for sg in T.segments:
        pts = sg.pts * 1e3
        seg_len = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        arc = np.concatenate([[0], np.cumsum(seg_len)])
        n = max(int(arc[-1] / 0.1), 2)
        q = np.linspace(0, arc[-1], n)
        P.append(np.stack([np.interp(q, arc, pts[:, k]) for k in range(3)], 1)); lab += [sg.sid] * n
    P = np.vstack(P)
    return cKDTree(P), np.array(lab)

class Deformer:
    def __init__(self, T):
        self.fr = build_frames(T)
        self.tree_lad = cKDTree(self.fr["c"])
        self.tree_all, self.lab_all = build_branch_tree(T)

    def project(self, P):
        d, i = self.tree_lad.query(P)
        d_all, j = self.tree_all.query(P)
        sid = self.lab_all[j]
        return d, i, sid

    def apply(self, P):
        d, i, sid = self.project(P)
        s = self.fr["s"][i]
        f, w = f_of_s(s)
        moved = (sid == LAD_SID) & (w > 0)
        c, t = self.fr["c"][i], self.fr["t"][i]
        rel = P - c
        ax = np.einsum("ij,ij->i", rel, t)[:, None] * t
        rad = rel - ax
        Pn = P.copy()
        Pn[moved] = (c + ax + f[:, None] * rad)[moved]
        return Pn, moved, w, s, d, sid

def refine(P0, F, dfm, max_edge, max_pass=8):
    """Conforming edge-split refinement. Marks edges whose DEFORMED length exceeds max_edge and that have a moved
    endpoint; a triangle with 1/2/3 marked edges is split into 2/3/4 triangles sharing edge midpoints, so the mesh stays
    watertight (no T-junctions). Midpoints are placed at the UNDEFORMED linear midpoint and deformed afterwards."""
    for it in range(max_pass):
        Pd, moved, *_ = dfm.apply(P0)
        e = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
        e = np.sort(e, axis=1)
        e = np.unique(e, axis=0)
        L = np.linalg.norm(Pd[e[:, 0]] - Pd[e[:, 1]], axis=1)
        mark = (L > max_edge) & (moved[e[:, 0]] | moved[e[:, 1]])
        if not mark.any():
            print(f"  refine: converged after {it} passes; {len(F)} triangles"); break
        me = e[mark]
        mid_id = {(a, b): len(P0) + k for k, (a, b) in enumerate(me)}
        P0 = np.vstack([P0, 0.5 * (P0[me[:, 0]] + P0[me[:, 1]])])
        Pn = dfm.apply(P0)[0]                       # deformed positions incl. the new midpoints (diagonal choice)
        dist = lambda i, j: np.linalg.norm(Pn[i] - Pn[j])
        newF = []
        key = lambda a, b: (a, b) if a < b else (b, a)
        for tri in F:
            a, b, c = (int(x) for x in tri)
            mab, mbc, mca = mid_id.get(key(a, b)), mid_id.get(key(b, c)), mid_id.get(key(c, a))
            n = (mab is not None) + (mbc is not None) + (mca is not None)
            if n == 0:
                newF.append((a, b, c))
            elif n == 3:
                newF += [(a, mab, mca), (mab, b, mbc), (mca, mbc, c), (mab, mbc, mca)]
            elif n == 1:
                if mab is not None: newF += [(a, mab, c), (mab, b, c)]
                elif mbc is not None: newF += [(a, b, mbc), (a, mbc, c)]
                else: newF += [(b, c, mca), (a, b, mca)]
            elif mca is None:        # ab, bc marked: corner triangle at b, quad a-mab-mbc-c
                newF.append((mab, b, mbc))
                if dist(a, mbc) < dist(mab, c): newF += [(a, mab, mbc), (a, mbc, c)]
                else: newF += [(a, mab, c), (mab, mbc, c)]
            elif mab is None:        # bc, ca marked: corner triangle at c, quad a-b-mbc-mca
                newF.append((mbc, c, mca))
                if dist(a, mbc) < dist(b, mca): newF += [(a, b, mbc), (a, mbc, mca)]
                else: newF += [(a, b, mca), (b, mbc, mca)]
            else:                    # ca, ab marked: corner triangle at a, quad mab-b-c-mca
                newF.append((a, mab, mca))
                if dist(mab, c) < dist(b, mca): newF += [(mab, b, c), (mab, c, mca)]
                else: newF += [(mab, b, mca), (b, c, mca)]
        F = np.array(newF, dtype=int)
    return P0, F

def section_area(surf, origin, normal, r_hint=3.0):
    sl = surf.slice(normal=normal, origin=origin)
    if sl.n_points == 0:
        return np.nan
    part = sl.connectivity(extraction_mode="closest", closest_point=origin)
    pts = np.asarray(part.points)
    n = normal / np.linalg.norm(normal)
    a = np.cross(n, [1.0, 0, 0]);
    if np.linalg.norm(a) < 1e-6: a = np.cross(n, [0, 1.0, 0])
    a /= np.linalg.norm(a); b = np.cross(n, a)
    ctr = pts.mean(0); q = pts - ctr
    x, y = q @ a, q @ b
    o = np.argsort(np.arctan2(y, x)); x, y = x[o], y[o]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

def main(out):
    T = build_tree(); T.ffr(mode="murray")
    surf = pv.read(SRC).extract_surface(algorithm="dataset_surface").triangulate().clean()
    P0 = np.asarray(surf.points, float); F = surf.faces.reshape(-1, 4)[:, 1:].copy()
    print(f"source: {len(P0)} points, {len(F)} triangles, bounds {np.round(surf.bounds,2)}")
    dfm = Deformer(T)
    # ---- gate: (a) every vertex that projects into the window and lies at LAD-wall distance is assigned to the LAD segment;
    #            (b) vertices of other branches project far enough from the LAD axis to be separate walls.
    d, i, sid = dfm.project(P0)
    s = dfm.fr["s"][i]
    _, w0 = f_of_s(s)
    inwin = w0 > 0
    wall_like = inwin & (d < 2.6)                  # LAD radius here is 1.4-1.8 mm; anything within 2.6 mm of the axis is LAD wall
    bad = wall_like & (sid != LAD_SID)
    print(f"window vertices within 2.6 mm of the LAD axis: {wall_like.sum()}; not assigned to the LAD segment: {bad.sum()}")
    assert bad.sum() == 0, "LAD-wall vertices inside the window were assigned to another branch (would tear)"
    d_lad_wall = d[inwin & (sid == LAD_SID)]
    d_other = d[inwin & (sid != LAD_SID)]
    assert len(d_other) > 0
    print(f"LAD-wall vertices in window: max distance to axis {d_lad_wall.max():.3f} mm; "
          f"other-branch vertices projecting into the window: min distance to the LAD axis {d_other.min():.3f} mm "
          f"(gap {d_other.min() - d_lad_wall.max():.3f} mm)")
    assert d_other.min() > d_lad_wall.max() + 0.5, "another branch's wall is within 0.5 mm of the LAD wall inside the window"
    r_loc = d[(np.abs(s - S_C) < 1.0)]
    print(f"local radius (vertex distance to axis) at the window centre: median {np.median(r_loc):.3f} mm, "
          f"min {r_loc.min():.3f} max {r_loc.max():.3f}")
    # ---- refine (undeformed midpoints), then deform
    Pr, Fr = refine(P0, F, dfm, MAX_EDGE)
    Pd, moved, w, sr, dd, sidr = dfm.apply(Pr)
    print(f"after refinement: {len(Pr)} points, {len(Fr)} triangles; moved vertices {moved.sum()}")
    # ---- gate: nothing outside the window moves
    assert np.abs(Pd[~moved] - Pr[~moved]).max() == 0.0
    # ---- gate: fold-over
    def normals(P, F):
        n = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
        return n / np.maximum(np.linalg.norm(n, axis=1), 1e-30)[:, None], np.linalg.norm(n, axis=1) / 2
    n0, A0 = normals(Pr, Fr); n1, A1 = normals(Pd, Fr)
    dot = np.einsum("ij,ij->i", n0, n1)
    print(f"fold-over check: min dot(normal_before, normal_after) = {dot.min():.3f}; faces with dot<=0: {(dot<=0).sum()}")
    assert (dot > 0).all(), "triangle fold-over"
    # ---- quality
    e = np.vstack([Fr[:, [0, 1]], Fr[:, [1, 2]], Fr[:, [2, 0]]])
    L = np.linalg.norm(Pd[e[:, 0]] - Pd[e[:, 1]], axis=1).reshape(3, -1)
    inwin = moved[Fr].any(axis=1)
    ar = L[:, inwin].max(0) / L[:, inwin].min(0)
    print(f"window triangles {inwin.sum()}: edge length min/median/max = {L[:, inwin].min():.3f}/{np.median(L[:, inwin]):.3f}/{L[:, inwin].max():.3f} mm; "
          f"edge-ratio median/max = {np.median(ar):.2f}/{ar.max():.2f}")
    # ---- gate: cross-section areas vs f(s)^2 on planes normal to the centreline
    out_surf = pv.PolyData(Pd, np.hstack([np.full((len(Fr), 1), 3), Fr]).ravel())
    src_surf = pv.PolyData(P0, np.hstack([np.full((len(F), 1), 3), F]).ravel())
    fr = dfm.fr; rows = []
    print("section check (station s, f(s)^2, area_new/area_old):")
    worst = 0
    for st in np.arange(S_C - LEN / 2 + 0.25, S_C + LEN / 2, 0.5):
        k = int(np.argmin(np.abs(fr["s"] - st)))
        a_new = section_area(out_surf, fr["c"][k], fr["t"][k]); a_old = section_area(src_surf, fr["c"][k], fr["t"][k])
        f = float(f_of_s(np.array([st]))[0][0]); ratio = a_new / a_old
        rows.append((float(st), f * f, float(ratio), float(a_old), float(a_new)))
        worst = max(worst, abs(ratio - f * f) / max(f * f, 1e-6))
        print(f"   s={st:5.2f}  f^2={f*f:.4f}  ratio={ratio:.4f}  (old {a_old:.3f} mm2 -> new {a_new:.3f} mm2)")
    k = int(np.argmin(np.abs(fr["s"] - S_C)))
    a_thr = section_area(out_surf, fr["c"][k], fr["t"][k]); a_ref = section_area(src_surf, fr["c"][k], fr["t"][k])
    r_thr = np.sqrt(a_thr / np.pi); r_ref = np.sqrt(a_ref / np.pi)
    print(f"THROAT (s={S_C}): area {a_thr:.4f} mm2 (equiv. radius {r_thr:.4f} mm) vs baseline {a_ref:.3f} mm2 (r {r_ref:.4f} mm): "
          f"radius ratio {r_thr/r_ref:.4f} (target {1-DS_FRAC:.2f}); worst relative area deviation vs f^2 along the window {100*worst:.2f}%")
    out_surf.point_data["moved"] = moved.astype(float)
    out_surf.save(out)
    json.dump(dict(S_C=S_C, LEN=LEN, DS=DS_FRAC, throat_xyz_mm=fr["c"][k].tolist(), throat_axis=fr["t"][k].tolist(),
                   r_ref_mm=float(r_ref), r_throat_mm=float(r_thr), sections=rows, n_points=int(len(Pr)), n_tri=int(len(Fr))),
              open(out.replace(".vtp", "_info.json"), "w"), indent=1)
    print("wrote", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else f"{BASE}/{PR['DIR']}/{PR['OPEN']}")
