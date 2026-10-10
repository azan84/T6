from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from zerod_ffr import Tree, R_FLOOR
from severity_sweep import load, plan, insert, HOSTS, RUNOFF
from error_types import ERROR_TYPES, T3_LENGTH_DELTA
from ablation import (THRESHOLD, node_map, bed_flow, territories, protocol_c_targets,
                      trunc_for, CALIBRE_ONLY, sc_covariates)

def rebuild(root: Path, pkg: Path, radii_csv: Path):
    meta = json.loads((pkg / "meta.json").read_text())
    inst, etype, bed = meta["instance"], meta["error_type"], meta["bed"]

    t = load(root, int(inst["scan"]), inst["side"], bed)
    t.ffr("murray", 1.0)
    sl = next((s for s in plan(t, inst["side"], t.last["ffr"].copy())[0]
               if s["vessel"] == inst["vessel"] and s["loc"] == inst["loc"]
               and abs(s["L"] * 1e3 - inst["L_mm"]) < 1e-6), None)
    if sl is None: raise SystemExit(f"slot not eligible under the {bed} bed — package and cohort disagree")
    path, s_arc, c, L = sl["path"], sl["s"], sl["c"], sl["L"]

    if etype in ("baseline", "clean_nolesion"):
        base_tree, segs = t, list(t.segments)
    else:
        segs, info = ERROR_TYPES[etype](list(t.segments), t, path, s_arc, c, L)
        if segs is None: raise SystemExit(f"{etype} not applicable: {info}")
        base_tree = Tree(segs, f"{t.name}_{etype}", bed=bed, r_trunc=trunc_for(bed, etype),
                         trunc_ref=t if etype in CALIBRE_ONLY else None)

    df = pd.read_csv(radii_csv)
    need = {"tree_node", "r_asmeshed_mm"}
    if not need <= set(df.columns):
        raise SystemExit(f"{radii_csv.name} must contain {sorted(need)}; found {sorted(df.columns)}")
    got = {int(k): float(v) * 1e-3 for k, v in zip(df.tree_node, df.r_asmeshed_mm) if np.isfinite(v) and v > 0}

    active = np.where(base_tree.active)[0]
    covered = [v for v in active if v in got]
    diag = dict(package=pkg.name, error_type=etype, bed=bed,
                n_active=len(active), n_returned=len(got), n_covered=len(covered),
                coverage=len(covered) / max(len(active), 1))

    import pyvista as pv
    vtp = pv.read(pkg / "centreline.vtp")
    req = {int(n): float(rt) * 1e-3 for n, rt in zip(np.asarray(vtp.point_data["tree_node"]),
                                                     np.asarray(vtp.point_data["r_target_mm"]))}
    xyz_to_node = {tuple(np.round(x, 9)): i for i, x in enumerate(base_tree.xyz)}
    new_segs, n_sub, n_fallback, shifts = [], 0, 0, []
    for sg in segs:
        r = sg.r.copy()
        for j, p in enumerate(sg.pts):
            v = xyz_to_node.get(tuple(np.round(p, 9)))
            if v is None: continue
            r_req = req.get(v)
            if v in got:
                r[j] = max(got[v], R_FLOOR); n_sub += 1
                if r_req is not None: shifts.append(abs(r[j] - r_req) * 1e3)
            elif r_req is not None:
                r[j] = max(r_req, R_FLOOR); n_fallback += 1
        new_segs.append(type(sg)(sg.sid, sg.parent, sg.pts, r, sg.label))
    diag.update(n_radii_substituted=n_sub, n_fallback_to_requested=n_fallback)

    twin = Tree(new_segs, f"{base_tree.name}_asmeshed", bed=bed, r_trunc=base_tree.r_trunc, reference=base_tree)

    d = np.array(shifts) if shifts else np.array([np.nan])
    diag.update(radius_shift_median_mm=float(np.median(d)), radius_shift_p95_mm=float(np.percentile(d, 95)),
                radius_shift_max_mm=float(np.nanmax(d)))
    return twin, base_tree, t, sl, diag

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--package", required=True); ap.add_argument("--radii", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    root, pkg, radii = Path(a.root).expanduser(), Path(a.package), Path(a.radii)
    twin, base_tree, t, sl, diag = rebuild(root, pkg, radii)

    print("AS-MESHED TWIN")
    for k in ("package", "error_type", "bed", "n_active", "n_returned", "n_covered"):
        print(f"  {k:24s} {diag[k]}")
    print(f"  {'coverage':24s} {diag['coverage']:.1%}"
          f"{'   <-- INCOMPLETE: nodes without a returned radius keep the requested value' if diag['coverage'] < 0.999 else ''}")
    print(f"  radius shift vs requested: median {diag['radius_shift_median_mm']:.4f} mm, "
          f"p95 {diag['radius_shift_p95_mm']:.4f}, max {diag['radius_shift_max_mm']:.4f}")
    if diag["coverage"] < 0.90:
        print("  WARNING: coverage below 90 %. The twin is mostly the REQUESTED geometry, so any 0D-vs-3D gap\n"
              "           computed from it is not the geometric-reduction gap it claims to be. Ask for a complete\n"
              "           radius return before using this in the ladder decomposition.")

    if a.out:
        pd.DataFrame([diag]).to_csv(a.out, index=False); print(f"\nwrote {a.out}")

if __name__ == "__main__":
    main()
