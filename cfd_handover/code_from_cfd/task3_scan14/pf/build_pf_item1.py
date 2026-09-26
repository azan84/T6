"""Item 1 branched tree: PRESCRIBED-FLOW (all outlets simultaneously) case builder, stage 1 of the round trip (work order 2026-09-24 Task 3 item 2).
usage: build_pf_item1.py <ds60|ds00> [nproc=8] [--ramp N]      -> P/pf_item1/pf_<ds>_prescribed   (refuses to overwrite)
Mesh: the 370k-cell mesh of the audited Item 1 resistance case case_<ds>_auto (P/../item1_branched_tree, on /mnt/e, so COPIED not hard-linked, ~65 MB). Numerics, transport and turbulence files: copied from that same case.
Targets: the per-outlet flows of the converged Item 1 resistance solve of the SAME tree (returns/2026-09-24/item1_tree.csv, the 'auto' rows, Q3D_m3s), i.e. the prescribed flows are the resistance solution's own flows
(label ITEM1_PILOT: a synthetic tree, its 'targets' are our own solution, not a cohort quantity). Inlet: totalPressure p0 = 11.319792 m2/s2 (90 mmHg) + pressureInletOutletVelocity as in every Task-3 case.
Outlets: flowRateOutletVelocity volumetricFlowRate = Q_i (positive out), p zeroGradient. --ramp N ramps every flow linearly over the first N iterations (default 0 = constant from iteration 0; the ramp is a fallback if the
constant start is unstable). Rank plan: 8 ranks per case, so ds60 + ds00 run concurrently at 16 ranks (work order: total <= 16). No 0D code is imported."""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pf_common as C

SRC_ROOT = os.path.join(os.path.dirname(C.P), "item1_branched_tree")
CSV = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24/item1_tree.csv"
OUT_ROOT = os.path.join(C.P, "pf_item1")
P0_KIN = 11.319792        # as the audited Item 1 cases (P_aorta / rho, unrounded 11.319792452830189)

def item1_rows(ds):
    rows = [r for r in csv.DictReader(open(CSV)) if r["case_dir"] == f"case_{ds}_auto"]
    if {r["outlet"] for r in rows} != {"A", "B1", "B2"}: raise SystemExit(f"item1_tree.csv: rows of case_{ds}_auto are {[r['outlet'] for r in rows]}")
    return {r["outlet"]: r for r in rows}

def main(ds, nproc=8, ramp=0):
    if ds not in ("ds60", "ds00"): raise SystemExit("ds must be ds60 or ds00")
    src = os.path.join(SRC_ROOT, f"case_{ds}_auto"); rows = item1_rows(ds)
    outlets = []
    for k in ("A", "B1", "B2"):
        r = rows[k]; R = float(r["R_out_SI"]); Rown = float(r["R_own_SI"]); Q = float(r["Q3D_m3s"]); G, relax = C.relax_from_G(R, Rown)
        assert abs(G - float(r["G_R_over_Rown"])) < 1e-3 * G, (k, G, r["G_R_over_Rown"])
        outlets.append(dict(patch=f"outlet{k}", code_name=f"res{k}", R_ref=R, R_own=Rown, G=G, relax=relax, Q_target_m3s=Q, p_init_kin=(C.PV + R * Q) / C.RHO))
    case = os.path.join(OUT_ROOT, f"pf_{ds}_prescribed")
    os.makedirs(OUT_ROOT, exist_ok=True)
    info = dict(family="item1", label="ITEM1_PILOT", stage="prescribed", ds=ds, source_case=src, targets_source=f"{CSV} rows case_dir == case_{ds}_auto (Q3D_m3s)", note="synthetic branched tree; not a cohort case; targets = flows of the converged resistance solve")
    b = C.write_case(case, "prescribed", C.poly_dir(src), f"{src}/system", f"{src}/constant", outlets, P0_KIN, nproc, ramp_iters=ramp, info=info)
    print(f"built {case}: {b['mesh_link']} mesh, targets (mL/s) " + ", ".join(f"{o['patch']} {o['Q_target_m3s']*1e6:.6f}" for o in outlets) + f", ranks {nproc}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: raise SystemExit(__doc__)
    ramp = int(a[a.index("--ramp") + 1]) if "--ramp" in a else 0
    pos = [x for i, x in enumerate(a) if x != "--ramp" and (i == 0 or a[i - 1] != "--ramp")]
    main(pos[0], int(pos[1]) if len(pos) > 1 else 8, ramp)
