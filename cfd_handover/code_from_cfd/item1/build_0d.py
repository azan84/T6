"""
build_0d.py - 0D-discrete reference for the Item-1 branched idealised tree (Y + 1 side branch, 3 outlets).

Geometry: see geometry.py (shared with build_centerline.py, so the 0D and 3D models cannot drift
apart - a previous version duplicated coordinates in both files and put branch B on branch A's own
axis; three independent reviewers (Fable 5.1, GPT-6-astra, Gemini 3.8 Flash) caught this on 2026-09-19
by slicing the generated 3D surface. Fixed: shared geometry.py, B now leaves the bifurcation at a real
60deg angle, clearance-verified.

FROZEN PHYSIOLOGY (panel finding, 2026-09-19): the previous version rebuilt a fresh Tree for ds=60%,
which let robust_taper() re-fit A's now-lesioned radius profile and silently shift r_ref/r_fit/w/C for
ALL THREE outlets (B1/B2 moved ~1.2% even though the lesion is only in A) - the design doc's claim that
B1/B2 stay "(~unchanged)" was therefore never actually true. Fixed: build ONE healthy (ds=0) tree,
calibrate C once, then evaluate the diseased case via `T.evaluate(C, r_override=...)`, which changes
ONLY the epicardial radius of the overridden nodes while r_ref, r_fit, the leaf weights w, and C stay
frozen at their healthy values - exactly the mechanism zerod_ffr.Tree.evaluate()'s docstring describes
this API for. Both ds=0% and ds=60% 3D cases must use the SAME (ds=0-derived) R_out values.
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code")
from zerod_ffr import Tree, Segment, MU, RHO, P_AORTA, P_VEN

sys.path.insert(0, str(Path(__file__).parent))
from geometry import build_paths, r_A, verify_clearances, LESION_C, LESION_L

Q_DEMAND = 1.5e-6   # m^3/s

def build_healthy_tree():
    paths = build_paths(ds_pct=0)
    segs = []
    sid_of = {"trunk": 0, "A": 1, "B": 2, "B1": 3, "B2": 4}
    parent_of = {"trunk": None, "A": "trunk", "B": "trunk", "B1": "B", "B2": "B"}
    for name, (x, y, z, r) in paths.items():
        pts_m = np.stack([x, y, z], 1) * 1e-3
        r_m = r * 1e-3
        parent_sid = sid_of[parent_of[name]] if parent_of[name] is not None else None
        segs.append(Segment(sid_of[name], parent_sid, pts_m, r_m, name))
    T = Tree(segs, "branched_ds00", bed="discrete")
    return T, paths

def diseased_r_override(T0, ds_pct):
    """Per-node radius array matching T0's internal node order, identical to T0.r everywhere except
    branch A's nodes, which get the ds_pct-diseased profile at the SAME x-positions (so indices line
    up one-to-one with T0's segment-A node order)."""
    r_override = T0.r.copy()
    mask_A = (T0.label == "A")
    # T0's node order for a non-root segment skips its own first point (shared with the parent's end
    # node) - build_healthy_tree fed x_a = build_paths(0)["A"][0] in increasing order, so the SAME
    # x_a[1:] here reproduces the exact node order/count Tree.__init__ assigned to label=="A".
    x_a_full = build_paths(0)["A"][0]
    r_diseased = r_A(x_a_full[1:], ds_pct) * 1e-3
    assert mask_A.sum() == len(r_diseased), (mask_A.sum(), len(r_diseased))
    r_override[mask_A] = r_diseased
    return r_override

if __name__ == "__main__":
    for ds in (0, 60):
        verify_clearances(ds)  # re-assert at import/run time, not just when geometry.py is invoked directly
    print("geometry clearances OK (see geometry.py for the numeric check)\n")

    T0, paths = build_healthy_tree()
    C = T0.calibrate(Q_DEMAND)

    results = {}
    for ds in (0, 60):
        if ds == 0:
            ffr, Q, info, sten, K = T0.evaluate(C)
        else:
            r_ov = diseased_r_override(T0, ds)
            ffr, Q, info, sten, K = T0.evaluate(C, r_override=r_ov)
        T0.last = dict(ffr=ffr, Q=Q)
        results[ds] = dict(info=info)
        print(f"=== ds={ds}%DS ===  converged={info['converged']}  iters={info['iters']}  "
              f"inflow={info['inflow']*1e6:.4f} mL/s")
        for r in T0.segment_table():
            print(f"    seg{r['seg']:<2} {r['label']:<6} r {r['r_prox']:.3f}->{r['r_dist']:.3f}mm "
                  f"Q {r['Q_prox']:.4f}->{r['Q_dist']:.4f} mL/s  maxDS={r['maxDS_resolved']:.1f}%  "
                  f"FFRdist={r['ffr_dist']:.4f}")
        print("  leaf outlet resistances (R_out = C / w) - SAME for both ds cases by construction:")
        for v in T0.leaves:
            R_out = C / T0.w[v]
            print(f"    node {v} ({T0.label[v]}): r_ref={T0.r_ref[v]*1e3:.4f}mm  R_out_SI={R_out:.6e} "
                  f"Pa.s/m3  R_kinematic={R_out/RHO:.4f}")
        # this project's own "own-vessel resistance" for the panel-mandated relax rule G_i = R_i/R_own,i
        # (see item1/design.md's resolved relax-rule section): Poiseuille resistance of outlet i's own
        # terminal segment, from the SAME healthy tree (frozen, so this is also identical for both ds
        # cases).
    print("\n  R_own (Poiseuille resistance of each outlet's OWN TERMINAL SEGMENT, full length, healthy tree):")
    for v in T0.leaves:
        # sum ds over every node sharing this leaf's segment label (its full terminal-vessel length,
        # not just the last discretisation step) - the physically meaningful "own vessel resistance"
        # the panel's G_i = R_i/R_own,i relax rule calls for.
        seg_mask = (T0.seg == T0.seg[v])
        L = T0.ds[seg_mask].sum(); r = T0.r_ref[v]
        R_own = 8 * MU * L / (np.pi * r ** 4)
        R_out = C / T0.w[v]
        G = R_out / R_own
        relax = min(0.5, 1.0 / (1.0 + G))
        print(f"    node {v} ({T0.label[v]}): L={L*1e3:.2f}mm  R_own={R_own:.4e} Pa.s/m3  "
              f"G=R_out/R_own={G:.2f}  relax=min(0.5,1/(1+G))={relax:.4f}")
