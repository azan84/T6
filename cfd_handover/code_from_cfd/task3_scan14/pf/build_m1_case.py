"""Package-driven case builder for the scan-14 Gate-M1 packages (work order 2026-09-24 Task 3). Package files ONLY; no 0D twin, no zerod_ffr/Tree/outlets_837 import (blinding).
usage: build_m1_case.py <package_dir_name> <mesh_dir> <resistance|prescribed> <outdir> [nproc=16] [--pkg-root R] [--extensions-json F] [--e0-waiver TEXT] [--ramp N] [--csv-subset F]
       build_m1_case.py <package_dir_name> <prescribed_case_dir> roundtrip [nproc]            (stage 2: R_i derived from the finished prescribed solve; delegates to pf_roundtrip_build.py)
<mesh_dir>: a cfMesh case/mesh directory holding constant/polyMesh with patches EXACTLY inlet, wall and out_<tree_node> for every non-closed outlet of outlets.csv (a closed outlet, bc_A mode 'closed', may be present as a patch: it is
made a WALL (U noSlip, p zeroGradient) or be absent, i.e. merged into wall). The polyMesh is hard-linked (same filesystem) else copied; never modified.
resistance: bc_A.csv R_SI per outlet with the audited coded BC (unique names res<tree_node>, relax = min(0.5, 1/(1+G)), G = R/R_own; R_own from the package centreline: m1_package.terminal_R_own), initial outlet p = min((Pv + R*Q_bcC)/rho, 0.98 p0) (for T1 the uncapped value at out_558 would exceed the inlet total pressure).
prescribed: ALL non-closed outlets simultaneously flowRateOutletVelocity with the bc_C_flows.csv flows (m3/s, positive out), p zeroGradient; the run is labelled PILOT for T1_missed_branch (its Protocol-C targets are provisional).
Both modes: inlet totalPressure P_aorta_kinematic (inlet.json) + pressureInletOutletVelocity, walls noSlip, laminar, nu from the template, fixed budget endTime 3000, monitors per outlet (flux + area-average p), inlet, and a throat plane
(the probes.csv 'throat' probe: point + normal) for Re_throat; ranks <= 16. Extension lengths for R_own: --extensions-json (geometry stage: {id: mm} or gates.json with 'extension_lengths_mm'), else the spec default 3 D (flagged).
E0 guard: e0_check.check(14, 'left') (from meta.json instance_key) must pass or carry an explicit --e0-waiver. build_info.json records package hashes, R_own details, the E0 result and all provenance."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pf_common as C
import m1_package as M
import e0_check

TEMPLATE = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/stageA/caseTemplate_real_lumen_steady"

def build(name, mesh_dir, mode, outdir, nproc=16, pkg_root=None, ext_json=None, waiver=None, ramp=0, subset_csv=e0_check.DEFAULT):
    if mode not in ("resistance", "prescribed"): raise SystemExit("mode must be resistance or prescribed (or 'roundtrip' via pf_roundtrip_build)")
    pkg = M.load_package(name, pkg_root); a, c = M.check_consistency(pkg)
    ik = pkg["meta"]["instance"]; e0 = e0_check.check(ik["scan"], ik["side"], subset_csv, waiver)
    cl = pkg["centreline"]; par, _ = M.graph(cl); ext, ext_src = M.extension_lengths(pkg, ext_json)
    rho, mu = float(pkg["inlet"]["rho"]), float(pkg["inlet"]["mu"]); assert (rho, mu) == (C.RHO, C.MU), (rho, mu)
    pv_pkg = float(pkg["inlet"]["P_venous_Pa"]); assert abs(pv_pkg - C.PV) < 1e-6
    p0 = float(pkg["inlet"]["P_aorta_kinematic"]); assert abs(p0 * C.RHO - float(pkg["inlet"]["P_aorta_Pa"])) < 1e-3
    outlets, closed, rown_info = [], [], {}
    for o in pkg["outlets"]:
        oid = o["outlet_id"]; ma = a[oid]["mode"]
        if ma == "closed": closed.append(oid); continue
        leaf = M.point_of_tree_node(cl, o["tree_node"]); Rown, det = M.terminal_R_own(cl, par, leaf, ext[oid], "r_ref_mm"); _, det_mis = M.terminal_R_own(cl, par, leaf, ext[oid], "MaximumInscribedSphereRadius")
        R = float(a[oid]["R_SI"])
        assert abs(R / C.RHO - float(a[oid]["R_kinematic"])) < 1e-6 * R / C.RHO, (oid, R, a[oid]["R_kinematic"])
        Q = float(c[oid]["Q_target_m3s"]); assert abs(Q * 1e6 - float(c[oid]["Q_target_mls"])) < 1e-9
        G, relax = C.relax_from_G(R, Rown)
        outlets.append(dict(patch=oid, code_name="res" + o["tree_node"], R=R, R_ref=R, R_own=Rown, G=G, relax=relax, Q_target_m3s=Q, p_init_kin=min((C.PV + R * Q) / C.RHO, 0.98 * p0), p_init_capped=bool((C.PV + R * Q) / C.RHO > 0.98 * p0), tree_node=int(o["tree_node"]), territory_id=o["territory_id"]))
        rown_info[oid] = dict(R_own_r_ref=Rown, R_own_MIS_variant=det_mis["R_segment"] + det_mis["R_extension"], **det)
    if not outlets: raise SystemExit("no non-closed outlet")
    pt, nrm, tp = M.throat_plane(pkg)
    label = "PILOT" if ("T1_missed_branch" in name and mode == "prescribed") else None
    info = dict(family="m1", package=name, instance=ik, error_type=pkg["meta"]["error_type"], stage=mode, label=label, pilot_label=label, e0_guard=e0, package_hashes=pkg["hashes"], closed_outlets=closed,
                extension_lengths_mm=ext, extension_source=ext_src, R_own_definition="terminal segment of the package centreline (r_ref_mm radii) + extension at the leaf radius, Poiseuille 8 mu L/(pi r^4); used only for relax", R_own_details=rown_info,
                throat_probe=tp["probe_id"], blinding="no 0D twin / zerod_ffr / Tree / outlets_837 import in this code path; analyze_case.py registers a constants-only zerod_ffr stand-in",
                p_bcA_x_bcC_Pa={o["patch"]: C.PV + o["R"] * o["Q_target_m3s"] for o in outlets}, p_init_capped={o["patch"]: o["p_init_capped"] for o in outlets}, n_bl_layers_recorded_by_mesh_stage=None,
                note_bcA_bcC="Pv + R(bc_A) Q(bc_C) equals the CLEAN outlet pressures for clean_nolesion and baseline; for T1_missed_branch bc_C holds the FULL territory flows (decision B1), so it is only a reference and exceeds P_aorta at the outlet that inherits the deleted branch (19.1 kPa for out_558 vs 12.0 kPa); the prescribed-mode bc_err of analyze_case compares the CFD patch p with it and is reported, not judged; initial outlet p is capped at 0.98 p0")
    mesh_dir = os.path.abspath(mesh_dir)
    return C.write_case(os.path.abspath(outdir), mode, C.poly_dir(mesh_dir), f"{TEMPLATE}/system", f"{TEMPLATE}/constant", outlets, p0, nproc, closed_patches=closed, throat_plane=(pt, nrm), ramp_iters=ramp, info=info)

def main(argv):
    if len(argv) < 3: raise SystemExit(__doc__)
    def opt(flag, default=None):
        return argv[argv.index(flag) + 1] if flag in argv else default
    flags = {"--pkg-root", "--extensions-json", "--e0-waiver", "--ramp", "--csv-subset"}
    pos = [x for i, x in enumerate(argv) if x not in flags and (i == 0 or argv[i - 1] not in flags)]
    if pos[2] == "roundtrip":
        import pf_roundtrip_build
        return pf_roundtrip_build.main(pos[1], int(pos[3]) if len(pos) > 3 else None)
    if len(pos) < 4: raise SystemExit(__doc__)
    b = build(pos[0], pos[1], pos[2], pos[3], int(pos[4]) if len(pos) > 4 else 16, opt("--pkg-root"), opt("--extensions-json"), opt("--e0-waiver"), int(opt("--ramp", 0)), opt("--csv-subset", e0_check.DEFAULT))
    print(f"built {pos[3]} ({b['mode']}): outlets {[o['patch'] for o in b['outlets']]}, closed {b['closed_patches']}, ranks {b['nproc']}, mesh {b['mesh_link']}, E0 {b['e0_guard']['status']}, extensions: {b['extension_source']}")

if __name__ == "__main__":
    main(sys.argv[1:])
