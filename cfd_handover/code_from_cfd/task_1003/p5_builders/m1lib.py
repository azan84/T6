"""Shared geometry helpers for the scan-14 Gate-M1 pipeline (no 0D code, no zerod_ffr: work-order blinding)."""
import os, sys, time, json, hashlib, contextlib, subprocess, re
import numpy as np
import pyvista as pv
from scipy.spatial import cKDTree
from matplotlib.path import Path as MPath

HERE = os.path.dirname(os.path.abspath(__file__))
FOAM_ENV = "source /usr/lib/openfoam/openfoam2406/etc/bashrc"

def sha256_file(fn, chunk=1 << 22):
    h = hashlib.sha256()
    with open(fn, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def sha256_dir(d):
    h = hashlib.sha256()
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if os.path.isfile(p): h.update(fn.encode()); h.update(sha256_file(p).encode())
    return h.hexdigest()

@contextlib.contextmanager
def timed(rep, name):
    t = time.time(); print(f"[{time.strftime('%H:%M:%S')}] {name} ...", flush=True)
    try: yield
    finally:
        rep.setdefault("wall_clock_s", {})[name] = round(time.time() - t, 2); print(f"[{time.strftime('%H:%M:%S')}] {name} done in {rep['wall_clock_s'][name]} s", flush=True)

# ------------------------------------------------------------------ planar sections
def plane_basis(t):
    t = np.asarray(t, float) / np.linalg.norm(t)
    a = np.cross(t, [1.0, 0, 0])
    if np.linalg.norm(a) < 1e-6: a = np.cross(t, [0, 1.0, 0])
    a /= np.linalg.norm(a); b = np.cross(t, a)
    return a, b

def ordered_loop(part):
    """Ordered point loop of a slice piece (copied from verify_lesion80_geometry.ordered_loop); returns (points, is_single_closed_loop)."""
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

def max_inscribed_radius(xy):
    """Radius of the largest circle inside the closed polygon xy (n,2): coarse grid then local refinement (exact distance to the polygon edges)."""
    from scipy.optimize import minimize
    p = np.vstack([xy, xy[:1]]); a, b = p[:-1], p[1:]; ab = b - a; L2 = np.maximum((ab ** 2).sum(1), 1e-30)
    def dist(q):   # q (m,2) -> distance to polygon boundary
        d = q[:, None, :] - a[None]; tt = np.clip((d * ab[None]).sum(2) / L2[None], 0, 1)
        return np.linalg.norm(d - tt[..., None] * ab[None], axis=2).min(1)
    path = MPath(xy); lo, hi = xy.min(0), xy.max(0)
    gx, gy = np.meshgrid(np.linspace(lo[0], hi[0], 41), np.linspace(lo[1], hi[1], 41)); g = np.c_[gx.ravel(), gy.ravel()]
    g = g[path.contains_points(g)]
    if len(g) == 0: g = xy.mean(0)[None]
    dg = dist(g); best = g[np.argsort(-dg)[:3]]; r = -1.0
    for s in best:
        res = minimize(lambda q: -dist(q[None])[0] if path.contains_point(q) else 0.0, s, method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-9, maxiter=400))
        r = max(r, -res.fun, float(dist(s[None])[0]))
    return float(r)

def section_metrics(surf, origin, normal, want_inscribed=True):
    """Metrics of the connected cross-section of `surf` (a PolyData, mm) nearest `origin` on the plane through `origin` with `normal`.
    Returns None if the plane misses; else dict(area, r_eq, r_insc, cen_off_over_req, closed, n_loops, star, perimeter)."""
    sl = surf.slice(normal=normal, origin=origin)
    if sl.n_points == 0: return None
    allc = sl.connectivity(extraction_mode="all"); rid = allc.point_data["RegionId"]; Pall = np.asarray(allc.points)
    rid_mine = rid[np.argmin(np.linalg.norm(Pall - origin, axis=1))]
    part = sl.connectivity(extraction_mode="closest", closest_point=origin).clean(tolerance=1e-9)
    pts, closed = ordered_loop(part)
    a, b = plane_basis(normal); q = pts - origin; x, y = q @ a, q @ b
    x2, y2 = np.roll(x, -1), np.roll(y, -1); cr = x * y2 - x2 * y; A = 0.5 * cr.sum()
    area = abs(A)
    if area < 1e-12: return None
    cx = ((x + x2) * cr).sum() / (6 * A); cy = ((y + y2) * cr).sum() / (6 * A)
    req = float(np.sqrt(area / np.pi))
    per = float(np.sum(np.linalg.norm(np.diff(np.vstack([pts, pts[:1]]), axis=0), axis=1)))
    ang = np.unwrap(np.arctan2(y, x)); steps = np.diff(ang)
    star = bool(closed) and (np.all(steps > -1e-9) or np.all(steps < 1e-9)) and abs(abs(ang[-1] - ang[0]) - 2 * np.pi) < 0.6
    out = dict(area=float(area), r_eq=req, cen_off_over_req=float(np.hypot(cx, cy) / req), closed=bool(closed), n_loops=int(len(np.unique(rid))), star=star, perimeter=per,
               axis_inside=bool(MPath(np.c_[x, y]).contains_point((0.0, 0.0))), other_loop_min_dist=(float(cKDTree(Pall[rid == rid_mine]).query(Pall[rid != rid_mine])[0].min()) if (rid != rid_mine).any() else float("inf")))
    out["r_insc"] = max_inscribed_radius(np.c_[x, y]) if want_inscribed else None
    return out

# ------------------------------------------------------------------ closed-surface bookkeeping
def boundary_loops(F):
    """Directed boundary loops of a triangle set F (n,3): returns (loops list of vertex-id arrays, ok) where ok = every boundary vertex has exactly one outgoing boundary edge."""
    directed = {}
    for f in F:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])): directed[(a, b)] = directed.get((a, b), 0) + 1
    bnd = [(a, b) for (a, b) in directed if (b, a) not in directed]
    nxt = {}; ok = True
    for a, b in bnd:
        if a in nxt: ok = False
        nxt[a] = b
    loops = []; seen = set()
    for s in nxt:
        if s in seen: continue
        loop = [s]; seen.add(s); v = nxt[s]
        while v != s:
            if v in seen or v not in nxt: ok = False; break
            loop.append(v); seen.add(v); v = nxt[v]
        loops.append(np.array(loop))
    return loops, ok and all(c == 1 for c in directed.values())

def surface_topology(P, F):
    """Closed-surface checks on the final triangle soup (P (n,3), F (m,3))."""
    directed = {}
    for f in F:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])): directed[(a, b)] = directed.get((a, b), 0) + 1
    multi = sum(1 for c in directed.values() if c > 1)
    open_edges = sum(1 for (a, b) in directed if (b, a) not in directed)
    n = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); A = 0.5 * np.linalg.norm(n, axis=1)
    e = np.stack([np.linalg.norm(P[F[:, i]] - P[F[:, (i + 1) % 3]], axis=1) for i in range(3)], 1)
    q = 4 * np.sqrt(3) * A / np.maximum((e ** 2).sum(1), 1e-30)
    vol = float(np.einsum("ij,ij->i", P[F[:, 0]], np.cross(P[F[:, 1]], P[F[:, 2]])).sum() / 6)
    # connected components by union-find on shared vertices
    par = np.arange(len(P))
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b, c in F:
        ra, rb, rc = find(a), find(b), find(c); par[rb] = ra; par[find(c)] = ra
    comps = len({find(v) for v in np.unique(F)})
    return dict(n_vertices=int(len(np.unique(F))), n_triangles=int(len(F)), open_edges=int(open_edges), non_manifold_or_duplicate_directed_edges=int(multi), volume_mm3=vol,
                connected_components=int(comps), min_area_mm2=float(A.min()), zero_area_triangles=int((A <= 1e-14).sum()), min_quality=float(q.min()), p1_quality=float(np.percentile(q, 1)),
                min_edge_mm=float(e.min()), max_edge_mm=float(e.max()))

def write_multisolid_stl(fn, P_mm, F, lab, scale=1e-3):
    P = P_mm * scale
    with open(fn, "w") as f:
        for name in sorted(set(lab)):
            f.write(f"solid {name}\n")
            for tri in F[lab == name]:
                a, b, c = P[tri]; nn = np.cross(b - a, c - a); nn = nn / (np.linalg.norm(nn) or 1)
                f.write(f"facet normal {nn[0]:.6e} {nn[1]:.6e} {nn[2]:.6e}\n outer loop\n")
                for v in (a, b, c): f.write(f"  vertex {v[0]:.9e} {v[1]:.9e} {v[2]:.9e}\n")
                f.write(" endloop\nendfacet\n")
            f.write(f"endsolid {name}\n")

def surface_check(stl, workdir, self_intersection=True, tag="check"):
    """OpenFOAM surfaceCheck on `stl` inside a scratch case dir (geometry tool, no mesh, no solver). Returns dict(parsed summary, log path)."""
    workdir = os.path.abspath(workdir); os.makedirs(f"{workdir}/constant/triSurface", exist_ok=True); os.makedirs(f"{workdir}/system", exist_ok=True)
    open(f"{workdir}/system/controlDict", "w").write("FoamFile { version 2.0; format ascii; class dictionary; object controlDict; }\napplication surfaceCheck;\nstartFrom startTime;\nstartTime 0;\nstopAt endTime;\nendTime 1;\ndeltaT 1;\n")
    link = f"{workdir}/constant/triSurface/{tag}.stl"
    if os.path.lexists(link): os.remove(link)
    os.symlink(os.path.abspath(stl), link)
    log = f"{workdir}/log.surfaceCheck.{tag}"
    cmd = f"{FOAM_ENV}; cd {workdir}; nice -n 10 surfaceCheck {'-checkSelfIntersection ' if self_intersection else ''}constant/triSurface/{tag}.stl > {log} 2>&1"
    subprocess.run(["bash", "-c", cmd], check=False)
    txt = open(log).read()
    return dict(log=log, closed=("Surface is closed" in txt), n_parts=(int(re.search(r"Number of unconnected parts : (\d+)", txt).group(1)) if re.search(r"Number of unconnected parts : (\d+)", txt) else None),
                n_zones=(int(re.search(r"Number of zones \(connected area with consistent normal\) : (\d+)", txt).group(1)) if re.search(r"Number of zones \(connected area with consistent normal\) : (\d+)", txt) else None),
                illegal_triangles=("Surface has no illegal triangles" in txt or "no illegal triangles" in txt.lower()),
                self_intersecting=(("is self-intersecting" in txt) if "Checking self-intersection" in txt else None),
                not_self_intersecting=("Surface is not self-intersecting" in txt), ended=("\nEnd" in txt))
