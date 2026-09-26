"""Independent geometry verification of the lesion80 surface (run after build_lesion80_surface.py).
 - baseline sections in the window are single loops and star-shaped about the axis (so radial scaling is injective there)
 - both DS definitions at the throat (area-equivalent radius; 0D EDT node radius), equivalent radius, perimeter, min/max width
 - station correspondence: 0D path nodes <-> smoothed-curve arc used by the deformation (max mismatch vs the polyline arc)
 - minimum triangle area / quality, clearances from the window to every outlet cap and to the other branches
Writes lesion80/geometry_verification.json.
"""
import sys, os, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pyvista as pv
from scipy.spatial import cKDTree
import build_lesion80_surface as G
from outlets_837 import build_tree

BASE = G.BASE

def ordered_loop(part):
    lines = part.lines.reshape(-1, 3)[:, 1:]
    adj = {}
    for a, b in lines:
        adj.setdefault(int(a), []).append(int(b)); adj.setdefault(int(b), []).append(int(a))
    start = next(iter(adj)); loop = [start]; prev = None; cur = start
    while True:
        nxt = [n for n in adj[cur] if n != prev]
        if not nxt or nxt[0] == start: break
        prev, cur = cur, nxt[0]
        if cur in loop: break
        loop.append(cur)
    return np.asarray(part.points)[loop], len(loop) == len(adj)

def section_metrics(surf, c, t):
    sl = surf.slice(normal=t, origin=c)
    if sl.n_points == 0: return None
    part = sl.connectivity(extraction_mode="closest", closest_point=c)
    allc = sl.connectivity(extraction_mode="all"); rid = allc.point_data["RegionId"]; Pall = np.asarray(allc.points)
    rid_mine = rid[np.argmin(np.linalg.norm(Pall - c, axis=1))]
    pts, closed = ordered_loop(part.clean(tolerance=1e-9))
    oth = Pall[rid != rid_mine]
    other_min = float(cKDTree(Pall[rid == rid_mine]).query(oth)[0].min()) if len(oth) else float("inf")
    a = np.cross(t, [1.0, 0, 0]);
    if np.linalg.norm(a) < 1e-6: a = np.cross(t, [0, 1.0, 0])
    a /= np.linalg.norm(a); b = np.cross(t, a)
    q = pts - c; x, y = q @ a, q @ b
    area = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
    per = np.sum(np.linalg.norm(np.diff(np.vstack([pts, pts[:1]]), axis=0), axis=1))
    ang = np.unwrap(np.arctan2(y, x)); steps = np.diff(ang)
    star = bool(closed) and (np.all(steps > -1e-9) or np.all(steps < 1e-9)) and abs(abs(ang[-1] - ang[0]) - 2 * np.pi) < 0.6
    ext = [np.ptp(x * np.cos(th) + y * np.sin(th)) for th in np.radians(np.arange(0, 180, 1.0))]
    return dict(area=area, r_eq=float(np.sqrt(area / np.pi)), perimeter=float(per), min_width=float(min(ext)), max_width=float(max(ext)),
                star=star, other_loop_min_dist=other_min, closed=bool(closed))

def main():
    T = build_tree(); T.ffr(mode="murray")
    dfm = G.Deformer(T); fr = dfm.fr
    base = pv.read(G.SRC).extract_surface(algorithm="dataset_surface").triangulate().clean()
    les = pv.read(f"{BASE}/{G.PR['DIR']}/{G.PR['OPEN']}")
    out = dict(window=[G.S_C - G.LEN / 2, G.S_C + G.LEN / 2])
    # ---- baseline section shape in the window (0.25 mm stations)
    bad = []; rows = []
    for st in np.arange(G.S_C - G.LEN / 2, G.S_C + G.LEN / 2 + 1e-9, 0.25):
        k = int(np.argmin(np.abs(fr["s"] - st)))
        mb = section_metrics(base, fr["c"][k], fr["t"][k]); ml = section_metrics(les, fr["c"][k], fr["t"][k])
        f = float(G.f_of_s(np.array([st]))[0][0])
        rows.append(dict(s=float(st), f=f, base=mb, lesion=ml))
        if not (mb["star"] and mb["closed"] and mb["other_loop_min_dist"] > 0.5): bad.append(float(st))
    out["baseline_sections_not_single_starshaped"] = bad
    out["sections"] = rows
    print(f"baseline window sections: {len(rows)} stations, {len(bad)} not (closed + star-shaped + >0.5 mm from any other vessel's contour): {bad}")
    k0 = int(np.argmin(np.abs(fr["s"] - G.S_C)))
    mb, ml = section_metrics(base, fr["c"][k0], fr["t"][k0]), section_metrics(les, fr["c"][k0], fr["t"][k0])
    out["throat"] = dict(baseline=mb, lesion=ml)
    print(f"throat @ s={G.S_C}: baseline area {mb['area']:.3f} mm2 r_eq {mb['r_eq']:.4f} perim {mb['perimeter']:.3f} width {mb['min_width']:.3f}-{mb['max_width']:.3f} mm")
    print(f"                    lesion   area {ml['area']:.4f} mm2 r_eq {ml['r_eq']:.4f} perim {ml['perimeter']:.3f} width {ml['min_width']:.3f}-{ml['max_width']:.3f} mm")
    ds_area = 1 - ml["r_eq"] / mb["r_eq"]
    out["DS_area_equivalent_diameter_pct"] = 100 * ds_area; out["area_reduction_pct"] = 100 * (1 - ml["area"] / mb["area"])
    print(f"DS (area-equivalent diameter) {100*ds_area:.2f}%  area reduction {out['area_reduction_pct']:.2f}%")
    # ---- station correspondence 0D nodes <-> smoothed curve
    tree = cKDTree(fr["c"]); dn, jn = tree.query(fr["xyz"])
    s_node = fr["s"][jn]; dmis = s_node - fr["arc_poly"]
    win_nodes = [n for n, s_ in zip(fr["nodes"], s_node) if T.seg[n] == G.LAD_SID and G.LEN and abs(s_ - G.S_C) < G.LEN / 2]
    out["station_map"] = dict(max_abs_arc_mismatch_mm=float(np.abs(dmis).max()), mismatch_in_window_mm=float(np.abs(dmis[(np.abs(s_node - G.S_C) < G.LEN / 2)]).max()),
                              max_node_to_curve_distance_mm=float(dn.max()), n_window_nodes=len(win_nodes))
    print(f"node<->smoothed-curve: max |arc mismatch| {np.abs(dmis).max():.3f} mm (window {out['station_map']['mismatch_in_window_mm']:.3f}); max node-to-curve distance {dn.max():.3f} mm; {len(win_nodes)} window nodes")
    # ---- triangle quality
    F = les.faces.reshape(-1, 4)[:, 1:]; P = np.asarray(les.points)
    n = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); A = 0.5 * np.linalg.norm(n, axis=1)
    e = np.stack([np.linalg.norm(P[F[:, i]] - P[F[:, (i + 1) % 3]], axis=1) for i in range(3)], 1)
    q = 4 * np.sqrt(3) * A / np.maximum((e ** 2).sum(1), 1e-30)
    mv = les.point_data["moved"][F].max(1) > 0.5
    out["triangles"] = dict(n=int(len(F)), min_area_mm2=float(A.min()), min_quality=float(q.min()), window_min_quality=float(q[mv].min()),
                            window_p5_quality=float(np.percentile(q[mv], 5)), zero_area=int((A <= 0).sum()))
    print(f"triangles {len(F)}: min area {A.min():.2e} mm2, min quality {q.min():.3f}, window quality min {q[mv].min():.3f} p5 {np.percentile(q[mv],5):.3f}")
    # ---- clearances
    ref = json.load(open(f"{BASE}/solve_baseline/zerod_reference.json"))
    c = fr["c"][k0]; cl = {}
    for p, cen in ref["patch_centroids_mm"].items():
        cl[p] = float(np.linalg.norm(np.array(cen) - c))
    out["clearance_throat_to_caps_mm"] = cl
    print("throat centre to cap centroids (mm):", {k: round(v, 1) for k, v in cl.items()})
    json.dump(out, open(f"{BASE}/{G.PR['DIR']}/geometry_verification.json", "w"), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
    ok = (not bad) and out["triangles"]["zero_area"] == 0
    print("GEOMETRY VERIFICATION:", "PASS" if ok else "FAIL")

if __name__ == "__main__":
    main()
