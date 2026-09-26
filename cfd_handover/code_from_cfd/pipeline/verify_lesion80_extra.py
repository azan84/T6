"""Extra pre-run geometry gates from the three-model audit of lesion80 (Fable/Astra/Gemini):
 G1 triangle purity: every triangle containing a moved vertex has all three vertices assigned to the LAD segment; every original
    vertex assigned to another branch has EXACTLY zero displacement.
 G2 centreline inside every baseline window section, centroid offset <= 0.3 r_eq (homothety about an off-centre point would
    displace the throat by 0.8 x the offset).
 G3 mask-label cross-check: sample the label volume (0.35 mm inside the wall) at every moved vertex; require the LAD label.
"""
import sys, os, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pyvista as pv
from matplotlib.path import Path as MPath
import build_lesion80_surface as G
from verify_lesion80_geometry import ordered_loop
from outlets_837 import build_tree, ROOT

BASE = G.BASE

def main():
    T = build_tree(); T.ffr(mode="murray"); dfm = G.Deformer(T); fr = dfm.fr
    src = pv.read(G.SRC).extract_surface(algorithm="dataset_surface").triangulate().clean()
    P0 = np.asarray(src.points, float); n0 = len(P0)
    les = pv.read(f"{BASE}/{G.PR['DIR']}/{G.PR['OPEN']}")
    Pd = np.asarray(les.points, float); F = les.faces.reshape(-1, 4)[:, 1:]
    moved = les.point_data["moved"] > 0.5
    out = {}
    # ---- G1
    d0, i0, sid0 = dfm.project(P0)
    disp = np.linalg.norm(Pd[:n0] - P0, axis=1)
    other = sid0 != G.LAD_SID
    g1a = float(disp[other].max()) if other.any() else 0.0
    sid_d = dfm.project(Pd)[2]
    tri_has_moved = moved[F].any(axis=1)
    impure = tri_has_moved & (sid_d[F] != G.LAD_SID).any(axis=1)
    out["G1"] = dict(max_displacement_of_non_LAD_original_vertices_mm=g1a, n_non_LAD_original_vertices=int(other.sum()),
                     triangles_with_moved_vertex=int(tri_has_moved.sum()), impure_triangles=int(impure.sum()))
    print(f"G1: max displacement of original vertices assigned to another branch = {g1a:.3e} mm ({other.sum()} vertices); "
          f"triangles with a moved vertex: {tri_has_moved.sum()}, of which not all-LAD: {impure.sum()}")
    # ---- G2
    base = src; rows = []
    worst = 0.0; outside = 0
    for st in np.arange(G.S_C - G.LEN / 2, G.S_C + G.LEN / 2 + 1e-9, 0.25):
        k = int(np.argmin(np.abs(fr["s"] - st))); c, t = fr["c"][k], fr["t"][k]
        sl = base.slice(normal=t, origin=c)
        part = sl.connectivity(extraction_mode="closest", closest_point=c).clean(tolerance=1e-9)
        pts, closed = ordered_loop(part)
        a = np.cross(t, [1.0, 0, 0]); a /= np.linalg.norm(a); b = np.cross(t, a)
        q = pts - c; x, y = q @ a, q @ b
        x2, y2 = np.roll(x, -1), np.roll(y, -1)
        cr = x * y2 - x2 * y; A = 0.5 * cr.sum()
        cx = ((x + x2) * cr).sum() / (6 * A); cy = ((y + y2) * cr).sum() / (6 * A)
        req = np.sqrt(abs(A) / np.pi)
        inside = MPath(np.c_[x, y]).contains_point((0.0, 0.0))
        off = float(np.hypot(cx, cy)) / req
        worst = max(worst, off); outside += (not inside)
        rows.append((float(st), off, bool(inside)))
    out["G2"] = dict(max_centroid_offset_over_req=worst, stations_with_axis_outside_lumen=int(outside), n_stations=len(rows))
    print(f"G2: max centroid offset / r_eq over the window = {worst:.3f} (limit 0.3); stations with the axis outside the lumen: {outside}/{len(rows)}")
    # ---- G3
    import nibabel as nib
    img = nib.load(f"{ROOT}/segmentations/837.coronary.nii.gz"); lab = np.asarray(img.dataobj); inv = np.linalg.inv(img.affine)
    idx = np.where(moved[:n0])[0]
    d, i, sid = dfm.project(P0[idx])
    ax_pt = fr["c"][i]
    inward = ax_pt - P0[idx]; inward /= np.maximum(np.linalg.norm(inward, axis=1), 1e-9)[:, None]
    samp = P0[idx] + 0.35 * inward
    ras = samp * np.array([-1.0, -1.0, 1.0])
    ijk = np.rint((inv @ np.c_[ras, np.ones(len(ras))].T)[:3]).astype(int)
    vals = lab[ijk[0], ijk[1], ijk[2]]
    frac = {int(v): float((vals == v).mean()) for v in np.unique(vals)}
    out["G3"] = dict(n_moved_original_vertices=int(len(idx)), label_fractions=frac)
    print(f"G3: mask labels at {len(idx)} moved original vertices (0.35 mm inside): {frac}  (LAD label = 2)")
    ok = (g1a == 0.0 and impure.sum() == 0 and worst <= 0.3 and outside == 0 and frac.get(2, 0) >= 0.99)
    out["PASS"] = bool(ok)
    json.dump(out, open(f"{BASE}/{G.PR['DIR']}/geometry_verification_extra.json", "w"), indent=1)
    print("EXTRA GATES:", "PASS" if ok else "FAIL")

if __name__ == "__main__":
    main()
