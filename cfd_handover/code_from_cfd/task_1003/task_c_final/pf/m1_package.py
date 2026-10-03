"""Reading a Gate-M1-format package (packages/M1/<name>/ for scan 14, packages/P5/<name>/ for the P5 pilot: same format) and the quantities the case builder needs from it. Package files ONLY: no 0D twin, no zerod_ffr / Tree / outlets_837 import (work-order blinding).
Frame: mm, LPS (centreline.vtp, outlets.csv, probes.csv, inlet.json); the solver works in metres (x 1e-3).
R_own,i (used ONLY for the relaxation factor relax_i = min(0.5, 1/(1+R_i/R_own,i)); the fixed point of the BC does not depend on it): Poiseuille resistance 8 mu L/(pi r^4) of the outlet's own TERMINAL SEGMENT of the package
centreline (points that carry the leaf's branch_id, from the segment start (child of the last bifurcation) to the leaf, edge by edge with the mean of the two end radii) PLUS the resistance of the flow extension at the leaf radius
(the audited definition of build_solve_cases.terminal_R_own, radii = the package's r_ref_mm by default; the MaximumInscribedSphereRadius variant is also returned for the record)."""
import os, csv, json, hashlib
import numpy as np

MU = 0.004
DRIVE_PKG_ROOTS = ("/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/M1", "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/P5")     # authoritative, read-only use (kilobyte package files)
PERSISTENT_PKG_ROOTS = ("/home/azan/paper6_t6_work/scratchpad/zipcheck/cfd_handover/packages/M1",)                                      # the persistent copy of the 09-26 handover zip (scan 14 M1 packages)
HASHED_FILES = ("outlets.csv", "bc_A.csv", "bc_C_flows.csv", "probes.csv", "inlet.json", "centreline.vtp", "meta.json", "mask_edit.json")

def resolve_pkg_root(arg=None, name=None):
    """resolution order (audit round 2, Sol finding 1): the explicit path argument (--pkg-root / $PKG_ROOT of the runner) ONLY, if given; else the first of the Drive roots packages/M1, packages/P5, then the
    persistent zipcheck copy packages/M1. With a name: the first such root that holds that package. No temporary (/tmp) roots, no environment fallbacks."""
    if arg:
        if not os.path.isdir(arg): raise SystemExit(f"--pkg-root {arg} is not a directory")
        cands = [arg]
    else: cands = [c for c in DRIVE_PKG_ROOTS + PERSISTENT_PKG_ROOTS if os.path.isdir(c)]
    if name is not None: cands = [c for c in cands if os.path.isdir(os.path.join(c, name))]
    if cands: return cands[0]
    raise SystemExit(f"no package root found{' holding ' + name if name else ''} (searched {[arg] if arg else list(DRIVE_PKG_ROOTS + PERSISTENT_PKG_ROOTS)}; give the package directory or --pkg-root)")

def resolve_pkg_dir(name, root=None):
    """absolute package directory: name may be a package directory itself (holding meta.json) or a package folder name resolved by resolve_pkg_root"""
    if os.path.isdir(name) and os.path.exists(os.path.join(name, "meta.json")): return os.path.abspath(name)
    d = os.path.join(resolve_pkg_root(root, name), name)
    if not os.path.isdir(d): raise SystemExit(f"package {name} not found under {root}")
    return os.path.abspath(d)

def package_hashes(d):
    return {f: sha256(f"{d}/{f}") for f in HASHED_FILES if os.path.exists(f"{d}/{f}")}

def verify_against_build(d, info):
    """compare the package files of directory d with the package_hashes the case was built with (build_info.json): returns a list of mismatch strings (empty = verified); a missing record is a mismatch"""
    rec = info.get("package_hashes")
    if not rec: return ["build_info.json has no package_hashes: the package cannot be verified"]
    now = package_hashes(d); why = []
    if info.get("package") and os.path.basename(d.rstrip("/")) != os.path.basename(str(info["package"]).rstrip("/")):      # build_info records the builder's argument: a name or a path
        why.append(f"package name {os.path.basename(d.rstrip('/'))} != build_info package {info['package']}")
    for f in sorted(set(rec) | set(now)):
        if f not in now: why.append(f"{f}: recorded in build_info but missing in {d}")
        elif f not in rec: why.append(f"{f}: present in {d} but not recorded in build_info")
        elif now[f] != rec[f]: why.append(f"{f}: sha256 {now[f][:12]} != recorded {rec[f][:12]}")
    return why

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def load_package(name, root=None):
    """name: the package folder name under the root, or a path to the package folder itself"""
    import pyvista as pv
    d = resolve_pkg_dir(name, root); name = os.path.basename(d.rstrip("/"))
    rd = lambda f: list(csv.DictReader(open(os.path.join(d, f))))
    pkg = dict(name=name, dir=d, meta=json.load(open(f"{d}/meta.json")), inlet=json.load(open(f"{d}/inlet.json")), outlets=rd("outlets.csv"), bcA=rd("bc_A.csv"), bcC=rd("bc_C_flows.csv"), probes=rd("probes.csv"),
               territories=rd("territories.csv"), centreline=pv.read(f"{d}/centreline.vtp"))
    pkg["hashes"] = package_hashes(d)
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
        if n not in par: continue                   # the root (a single-vessel tree whose terminal segment reaches the root: no edge above it)
        p = par[n]; ds = float(np.linalg.norm(xyz[n] - xyz[p])); rm = 0.5 * (r[n] + r[p]); R += 8 * mu * ds / (np.pi * rm ** 4); L += ds
    R_ext = 8 * mu * (ext_mm * 1e-3) / (np.pi * r[leaf_point] ** 4)
    return R + R_ext, dict(segment_length_mm=L * 1e3, n_edges=len(seg), R_segment=R, R_extension=R_ext, r_leaf_mm=float(r[leaf_point] * 1e3), ext_mm=float(ext_mm), field=field)

def throat_plane(pkg):
    """the probes.csv 'throat' probe (also present in clean_nolesion, where it marks the would-be throat station): (point_m, normal)"""
    t = [p for p in pkg["probes"] if p["kind"] == "throat"]
    if len(t) != 1: raise SystemExit(f"{len(t)} throat probes in {pkg['name']}")
    p = t[0]; n = np.array([float(p["normal_x"]), float(p["normal_y"]), float(p["normal_z"])]); n /= np.linalg.norm(n)
    return np.array([float(p["x"]), float(p["y"]), float(p["z"])]) * 1e-3, n, p

def probe_row(pkg, kind):
    """the single probes.csv row of a kind ('throat', 'measurement'); the measurement row must sit on meta.json's measurement tree_node"""
    t = [p for p in pkg["probes"] if p["kind"] == kind]
    if len(t) != 1: raise SystemExit(f"{len(t)} '{kind}' probes in {pkg['name']}")
    if kind == "measurement":
        mt = (pkg["meta"].get("measurement") or {}).get("tree_node")
        if mt is not None and int(mt) != int(t[0]["tree_node"]): raise SystemExit(f"{pkg['name']}: measurement probe tree_node {t[0]['tree_node']} != meta.json measurement.tree_node {mt}")
    return t[0]

def measurement_plane(pkg):
    """the probes.csv 'measurement' probe (the node the analysis side reports FFR at): (point_m, normal, row)"""
    p = probe_row(pkg, "measurement"); n = np.array([float(p["normal_x"]), float(p["normal_y"]), float(p["normal_z"])]); n /= np.linalg.norm(n)
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
