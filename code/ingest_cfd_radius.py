"""
ingest_cfd_radius.py — rebuild the 0D twin from the geometry that was ACTUALLY MESHED (CFD-ARM-SPEC §6.1b, §10).

WHY THIS EXISTS. The CFD side is asked to return the as-meshed radius along the centreline because what it meshed is
not exactly what the package requested: marching cubes, Taubin smoothing, the flow extensions and the mesher's own
resolution all move the lumen a little. Comparing a 0D model built from the REQUESTED radius against a 3D solve of
the ACHIEVED one would charge that difference to "fidelity", which is precisely the quantity the ladder
decomposition is trying to measure. So the twin is rebuilt from the achieved radius and the comparison is
like with like.

THE ONE DESIGN DECISION, AND IT IS NOT OBVIOUS. Only `r` comes from the mesh. The healthy reference (`r_fit`,
`r_ref`), and therefore the bed weights, the truncation and the calibration constant C, are INHERITED from the
package's own tree via `Tree(..., reference=...)`. Two reasons:

  1. The 3D case was given its boundary conditions from the package's tree. If the twin re-derived its own bed from
     the as-meshed radii it would carry a DIFFERENT bed from the 3D case it is being compared against, and the
     comparison would no longer isolate geometry.
  2. `r_ref` is a robust taper fit. Re-fitting it to a surface that has been smoothed and remeshed would fold the
     mesher's smoothing into the healthy reference, which is a modelling artefact, not anatomy.

So: same bed, same BCs, same modelled node set — only the epicardial radius differs. That is the comparison
CFD-ARM-SPEC §14's ladder decomposition needs.

EXPECTED INPUT (the contract with the CFD side; `cfd_handover/WORK-ORDER-2026-09-19.md` §6 item 3):
    as_meshed_radius_<case>.csv   columns: tree_node, s_mm, r_asmeshed_mm
`tree_node` is the point array of the same name shipped in the package's `centreline.vtp`, so the join is exact and
does not depend on floating-point coordinate matching. Rows may be missing (the mesher may not have covered every
node) — coverage is reported, never silently interpolated over.

usage: ingest_cfd_radius.py <data_root> --package <dir> --radii <csv> [--out <csv>]
"""
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
    """Return (twin, original, diagnostics). The twin differs from the original ONLY in its epicardial radius."""
    meta = json.loads((pkg / "meta.json").read_text())
    inst, etype, bed = meta["instance"], meta["error_type"], meta["bed"]

    t = load(root, int(inst["scan"]), inst["side"], bed)
    t.ffr("murray", 1.0)
    sl = next((s for s in plan(t, inst["side"], t.last["ffr"].copy())[0]
               if s["vessel"] == inst["vessel"] and s["loc"] == inst["loc"]
               and abs(s["L"] * 1e3 - inst["L_mm"]) < 1e-6), None)
    if sl is None: raise SystemExit(f"slot not eligible under the {bed} bed — package and cohort disagree")
    path, s_arc, c, L = sl["path"], sl["s"], sl["c"], sl["L"]

    # the tree the package actually described (baseline or a corrupted variant)
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

    # THE FALLBACK FOR AN UNCOVERED NODE IS THE REQUESTED RADIUS, NOT THE UNLESIONED ONE. `segs` carries the tree's
    # ORIGINAL radii — for a baseline package that is the vessel WITHOUT its lesion, because the lesion is applied
    # by insert() and shipped as the vtp's `r_target_mm`. Falling back to `sg.r` would therefore silently DELETE the
    # stenosis at every node the mesher did not return, i.e. exactly the nodes least likely to be well resolved.
    # Requested radius comes from the package itself, which is also what "as-meshed vs requested" must mean.
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
                r[j] = max(r_req, R_FLOOR); n_fallback += 1      # requested, NOT unlesioned
        new_segs.append(type(sg)(sg.sid, sg.parent, sg.pts, r, sg.label))
    diag.update(n_radii_substituted=n_sub, n_fallback_to_requested=n_fallback)

    # reference=base_tree: inherit r_fit / r_ref, hence the bed, the truncation and C. See the module docstring.
    twin = Tree(new_segs, f"{base_tree.name}_asmeshed", bed=bed, r_trunc=base_tree.r_trunc, reference=base_tree)
    # AS-MESHED vs REQUESTED, on the nodes the mesher actually returned. Comparing the twin against base_tree.r
    # instead would measure the LESION (base_tree is unlesioned for a baseline package) and report it as mesh error.
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
    print("\nNOTE: this rebuilds the twin and reports how far the mesh moved the lumen. Solving it under A/B/C and\n"
          "comparing against the returned 3D FFR is the next step and belongs with the 3D results, not here —\n"
          "CFD-ARM-SPEC §13 withholds the 0D predictions until the CFD side has returned its numbers.")

if __name__ == "__main__":
    main()
