"""Reading a scan-14 Gate-M1 package (packages/M1/<name>/) and the quantities the case builder needs from it. Package files ONLY: no 0D twin, no zerod_ffr / Tree / outlets_837 import (work-order blinding).
Frame: mm, LPS (centreline.vtp, outlets.csv, probes.csv, inlet.json); the solver works in metres (x 1e-3).
R_own,i (used ONLY for the relaxation factor relax_i = min(0.5, 1/(1+R_i/R_own,i)); the fixed point of the BC does not depend on it): Poiseuille resistance 8 mu L/(pi r^4) of the outlet's own TERMINAL SEGMENT of the package
centreline (points that carry the leaf's branch_id, from the segment start (child of the last bifurcation) to the leaf, edge by edge with the mean of the two end radii) PLUS the resistance of the flow extension at the leaf radius
(the audited definition of build_solve_cases.terminal_R_own, radii = the package's r_ref_mm by default; the MaximumInscribedSphereRadius variant is also returned for the record)."""
import os, csv, json, hashlib
import numpy as np

MU = 0.004
ZIP_PKG_ROOT = "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/zipcheck/cfd_handover/packages/M1"

def resolve_pkg_root(arg=None):
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for c in (arg, os.environ.get("M1_PKG_ROOT"), os.path.join(here, "m1", "pkg"), ZIP_PKG_ROOT):
        if c and os.path.isdir(c): return c
    raise SystemExit("no package root found (use --pkg-root or $M1_PKG_ROOT)")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def load_package(name, root=None):
    import pyvista as pv
    root = resolve_pkg_root(root); d = os.path.join(root, name)
    if not os.path.isdir(d): raise SystemExit(f"package {name} not found under {root}")
    rd = lambda f: list(csv.DictReader(open(os.path.join(d, f))))
    pkg = dict(name=name, dir=d, meta=json.load(open(f"{d}/meta.json")), inlet=json.load(open(f"{d}/inlet.json")), outlets=rd("outlets.csv"), bcA=rd("bc_A.csv"), bcC=rd("bc_C_flows.csv"), probes=rd("probes.csv"),
               territories=rd("territories.csv"), centreline=pv.read(f"{d}/centreline.vtp"))
    pkg["hashes"] = {f: sha256(f"{d}/{f}") for f in ("outlets.csv", "bc_A.csv", "bc_C_flows.csv", "probes.csv", "inlet.json", "centreline.vtp", "meta.json", "mask_edit.json") if os.path.exists(f"{d}/{f}")}
    return pkg

def check_consistency(pkg):
    """outlets.csv, bc_A.csv and bc_C_flows.csv describe the same outlets; resistance<->prescribed, closed<->closed"""
    ids = [o["outlet_id"] for o in pkg["outlets"]]; a = {r["outlet_id"]: r for r in pkg["bcA"]}; c = {r["outlet_id"]: r for r in pkg["bcC"]}
    if set(ids) != set(a) or set(ids) != set(c) or len(ids) != len(set(ids)): raise SystemExit(f"outlet id sets differ: outlets {sorted(ids)} bc_A {sorted(a)} bc_C {sorted(c)}")
    for i in ids:
        ma, mc = a[i]["mode"], c[i]["mode"]
        if (ma, mc) not in (("resistance", "prescribed"), ("closed", "closed")): raise SystemExit(f"{i}: bc_A mode {ma!r} / bc_C mode {mc!r} not (resistance,prescribed) or (closed,closed)")
    return a, c

def graph(cl):
    """parent map of the centreline in POINT indices (edges are (lower, higher) point index, single parent, root = point 0: verified for the shipped packages) and children lists"""
    L = np.asarray(cl.lines).reshape(-1, 3)[:, 1:]; par = {}
    for a, b in L:
        hi, lo = int(max(a, b)), int(min(a, b))
        if hi in par and par[hi] != lo: raise SystemExit(f"point {hi} has two parents")
        par[hi] = lo
    roots = [i for i in range(cl.n_points) if i not in par]
    if roots != [0]: raise SystemExit(f"centreline roots {roots} (expected [0])")
    ch = {}
    for k, v in par.items(): ch.setdefault(v, []).append(k)
    return par, ch

def point_of_tree_node(cl, tree_node):
    idx = np.where(np.asarray(cl.point_data["tree_node"]) == int(tree_node))[0]
    if len(idx) != 1: raise SystemExit(f"tree_node {tree_node}: {len(idx)} matching centreline points")
    return int(idx[0])

def terminal_R_own(cl, par, leaf_point, ext_mm, field="r_ref_mm", mu=MU):
    """returns (R_own_SI, dict(segment_length_mm, n_edges, R_segment, R_extension, r_leaf_mm, ext_mm, field))"""
    r = np.asarray(cl.point_data[field]) * 1e-3; br = np.asarray(cl.point_data["branch_id"]); xyz = np.asarray(cl.points) * 1e-3
    seg = []; n = leaf_point
    while br[n] == br[leaf_point]:
        seg.append(n)
        if n not in par: break
        n = par[n]
    R = 0.0; L = 0.0
    for n in seg:                                   # edge (n, parent[n]) for every node of the segment: exactly build_solve_cases.terminal_R_own
        p = par[n]; ds = float(np.linalg.norm(xyz[n] - xyz[p])); rm = 0.5 * (r[n] + r[p]); R += 8 * mu * ds / (np.pi * rm ** 4); L += ds
    R_ext = 8 * mu * (ext_mm * 1e-3) / (np.pi * r[leaf_point] ** 4)
    return R + R_ext, dict(segment_length_mm=L * 1e3, n_edges=len(seg), R_segment=R, R_extension=R_ext, r_leaf_mm=float(r[leaf_point] * 1e3), ext_mm=float(ext_mm), field=field)

def throat_plane(pkg):
    """the probes.csv 'throat' probe (also present in clean_nolesion, where it marks the would-be throat station): (point_m, normal)"""
    t = [p for p in pkg["probes"] if p["kind"] == "throat"]
    if len(t) != 1: raise SystemExit(f"{len(t)} throat probes in {pkg['name']}")
    p = t[0]; n = np.array([float(p["normal_x"]), float(p["normal_y"]), float(p["normal_z"])]); n /= np.linalg.norm(n)
    return np.array([float(p["x"]), float(p["y"]), float(p["z"])]) * 1e-3, n, p

def extension_lengths(pkg, arg_json=None):
    """{outlet_id: extension length in mm}: from a JSON given by the geometry stage ({id: mm} or a gates.json holding 'extension_lengths_mm'), else the spec default 3 D per outlet (D = 2 r_mm of outlets.csv), flagged"""
    if arg_json:
        j = json.load(open(arg_json)); j = j.get("extension_lengths_mm", j)
        ids = [o["outlet_id"] for o in pkg["outlets"]]
        miss = [i for i in ids if i not in j]
        if miss: raise SystemExit(f"extension lengths missing for {miss} in {arg_json}")
        return {i: float(j[i]) for i in ids}, f"as-built, from {arg_json}"
    return {o["outlet_id"]: 3 * 2 * float(o["r_mm"]) for o in pkg["outlets"]}, "SPEC DEFAULT 3 D (D = 2 r_mm of outlets.csv), not the as-built lengths"
