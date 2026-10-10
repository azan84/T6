"""Package-driven case builder for Gate-M1-format packages: the scan-14 M1 packages (work order 2026-09-24 Task 3) and the P5 pilot packages (work order 2026-10-03 Task P5, baseline, resistance mode). Package files ONLY; no 0D twin, no zerod_ffr/Tree/outlets_837 import (blinding).
usage: build_m1_case.py <package_dir_name> <mesh_dir> <resistance|prescribed> <outdir> [nproc=16] [--pkg-root R] [--extensions-json F] [--e0-waiver TEXT] [--ramp N] [--csv-subset F] [--no-mesh-check] [--r-scale K]
       build_m1_case.py <package_dir_name> <prescribed_case_dir> roundtrip [nproc]            (stage 2: R_i derived from the finished prescribed solve; delegates to pf_roundtrip_build.py)
<mesh_dir>: a cfMesh case/mesh directory holding constant/polyMesh with patches EXACTLY inlet, wall and out_<tree_node> for every non-closed outlet of outlets.csv (a closed outlet, bc_A mode 'closed', may be present as a patch: it is
made a WALL (U noSlip, p zeroGradient) or be absent, i.e. merged into wall). The polyMesh is hard-linked (same filesystem) else copied; never modified.
resistance: bc_A.csv R_SI per outlet with the audited coded BC (unique names res<tree_node>, relax = min(0.5, 1/(1+G)), G = R/R_own; R_own from the package centreline: m1_package.terminal_R_own), initial outlet p = min((Pv + R*Q_bcC)/rho, 0.98 p0) (for T1 the uncapped value at out_558 would exceed the inlet total pressure).
prescribed: ALL non-closed outlets simultaneously flowRateOutletVelocity with the bc_C_flows.csv flows (m3/s, positive out), p zeroGradient; the run is labelled PILOT for T1_missed_branch (its Protocol-C targets are provisional).
Both modes: inlet totalPressure P_aorta_kinematic (inlet.json) + pressureInletOutletVelocity, walls noSlip, laminar, nu from the template, fixed budget endTime 3000, monitors per outlet (flux + area-average p), inlet, and a throat plane
(the probes.csv 'throat' probe: point + normal) and (D8, work order 2026-10-03) a measurement plane (the probes.csv 'measurement' probe, = meta.json measurement.tree_node): throatFlux/throatP and measurementFlux/measurementP, area-averaged,
written EVERY iteration with the sampled area. Both planes are BOUNDED (sampledPlane `bounds`, probe_sections.py): box sized from r_ref_mm and the centreline, then CHECKED on the actual polyMesh with pyvista (one connected section, not clipped,
no other vessel in the box, area within [0.4, 2.5] pi r^2) and, for the measurement probe, the STRICT single-lumen rule (normal within 20 deg of the tangent, no bifurcation within 1.5 r_ref, one component,
area within a factor 1.6 of pi r_ref^2; probe_sections.py): a package probe failing it is recorded FAILED_SECTION_RULE and relocated deterministically (<= 3 mm along the same vessel path; measurementP = relocated plane,
measurementOrigP = the package plane if its bounded section is valid; build_info measurement_probe_relocated / measurement_probe_used); the builder REFUSES the case if a check fails without a valid relocation; build_info.json 'probe_section_check' records it. --no-mesh-check (stub polyMesh tests only) writes NOT_FOR_PRODUCTION; ranks <= 16. Extension lengths for R_own: --extensions-json (geometry stage: {id: mm} or gates.json with 'extension_lengths_mm'), else the spec default 3 D (flagged).
An outlet patch with ZERO faces in the mesh (P5 272 out_396) is LOST IN MESH: no monitor (fatal in v2406), BC entries kept (inert), build_info outlets_lost_in_mesh (with the mesh stage's reason from <mesh_dir>/mesh_gates.json
when present) and bc_bookkeeping (its territory is closed); see pf_common.write_case. Any package of the format works (outlet patches = the package outlet_ids, closed outlets of bc_A become walls); E0 guard: e0_check.check(scan, side) (from meta.json instance) must pass or carry an explicit --e0-waiver. build_info.json records package hashes, R_own details, the E0 result and all provenance."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pf_common as C
import m1_package as M
import e0_check
import probe_sections as S

TEMPLATE = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/stageA/caseTemplate_real_lumen_steady"

def lost_outlet_reasons(mesh_dir, patches):
    """{patch: reason} for the outlet patches with 0 faces, from the mesh stage's <mesh_dir>/mesh_gates.json (patches_missing_or_empty, mesh volume, cartesianMesh 'unconnected regions' warning) when present"""
    try: bnd = C.read_boundary(C.poly_dir(mesh_dir))
    except SystemExit: return {}
    out = {}
    for p in patches:
        if p not in bnd or bnd[p]["nFaces"] != 0: continue
        r = C.LOST_REASON_DEFAULT; mg = os.path.join(mesh_dir, "mesh_gates.json"); lg = os.path.join(mesh_dir, "log.cartesianMesh")
        if os.path.exists(mg):
            m = json.load(open(mg)); r += f"; mesh stage {os.path.basename(mg)}: patches_missing_or_empty={m.get('patches_missing_or_empty')}, GATES_PASS={m.get('GATES_PASS')}"
        if os.path.exists(lg):
            w = [ln.strip() for ln in open(lg, errors="replace") if "unconnected regions" in ln]
            if w: r += f"; log.cartesianMesh: '{w[0]}'"
        out[p] = r
    return out

def build(name, mesh_dir, mode, outdir, nproc=16, pkg_root=None, ext_json=None, waiver=None, ramp=0, subset_csv=e0_check.DEFAULT, mesh_check=True, r_scale=1.0):
    if mode not in ("resistance", "prescribed"): raise SystemExit("mode must be resistance or prescribed (or 'roundtrip' via pf_roundtrip_build)")
    if r_scale != 1.0 and mode != "resistance": raise SystemExit("--r-scale applies to resistance mode only (work order 2026-10-10 Task G)")
    if not (r_scale > 0 and np.isfinite(r_scale)): raise SystemExit(f"bad --r-scale {r_scale}")
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
        R = R * r_scale     # Task G (WO 2026-10-10): every bc_A resistance multiplied by ONE factor k (k = 1: unchanged)
        Q = float(c[oid]["Q_target_m3s"]); assert abs(Q * 1e6 - float(c[oid]["Q_target_mls"])) < 1e-9
        G, relax = C.relax_from_G(R, Rown)
        outlets.append(dict(patch=oid, code_name="res" + o["tree_node"], R=R, R_ref=R, R_own=Rown, G=G, relax=relax, Q_target_m3s=Q, p_init_kin=min((C.PV + R * Q) / C.RHO, 0.98 * p0), p_init_capped=bool((C.PV + R * Q) / C.RHO > 0.98 * p0), tree_node=int(o["tree_node"]), territory_id=o["territory_id"]))
        rown_info[oid] = dict(R_own_r_ref=Rown, R_own_MIS_variant=det_mis["R_segment"] + det_mis["R_extension"], **det)
    if not outlets: raise SystemExit("no non-closed outlet")
    if os.path.exists(os.path.abspath(outdir)): raise SystemExit(f"{outdir} exists")
    pt, nrm, tp = M.throat_plane(pkg); mpt, mnrm, mp = M.measurement_plane(pkg)
    planes = S.probe_planes(pkg, C.poly_dir(os.path.abspath(mesh_dir)) if mesh_check else None, diagnose_infinite=mesh_check)     # refuses (SystemExit) if a bounded section fails the mesh check
    reloc = planes["measurement"].get("relocation")
    for k, (q, nn) in (("throat", (pt, nrm)), ("measurement", (mpt, mnrm))):
        if k == "measurement" and reloc: k = "measurement_orig"
        if k in planes: assert np.allclose(planes[k]["point_m"], q) and np.allclose(planes[k]["normal"], nn)
    psc = {k: dict(probe_id=e["probe_id"], status=e["status"], h_final_mm=e["h_final_mm"], bounds_m=e["bounds_m"], sizing=e["sizing"], mesh_check=e.get("mesh_check"),
                   attempts=[dict(h_mm=a["h_mm"], fails=a["fails"]) for a in e.get("mesh_check_attempts", [])], infinite_plane_unbounded=e.get("infinite_plane"),
                   **{x: e[x] for x in ("section_rule", "relocation", "section_rule_record_only") if x in e}) for k, e in planes.items()}
    psc["rule"] = S.__doc__.split("Mesh CHECK")[1].split("If the first box")[0].strip()
    psc["strict_measurement_rule"] = "STRICT MEASUREMENT-SECTION RULE" + S.__doc__.split("STRICT MEASUREMENT-SECTION RULE")[1].strip()
    srule = planes["measurement"]["section_rule"]; used = planes["measurement"]["probe_id"]
    if reloc: print(f"{name}: measurement probe {mp['probe_id']} FAILED_SECTION_RULE ({srule['why_not_ok']}); RELOCATED to tree_node {reloc['relocated']['tree_node']} ({reloc['relocated']['arc_from_original_mm']:+.3f} mm of arc); original monitor: {reloc['original']['original_monitor']}")
    label = "PILOT" if ("T1_missed_branch" in name and mode == "prescribed") else None
    info = dict(r_scale_k=r_scale, r_scale_note=("every bc_A R_SI multiplied by k (work order 2026-10-10 Task G, one global outlet scaling); R_used = k * bc_A" if r_scale != 1.0 else "k = 1 (bc_A unchanged)"), family="m1", package=name, instance=ik, error_type=pkg["meta"]["error_type"], stage=mode, label=label, pilot_label=label, e0_guard=e0, package_hashes=pkg["hashes"], closed_outlets=closed,
                extension_lengths_mm=ext, extension_source=ext_src, R_own_definition="terminal segment of the package centreline (r_ref_mm radii) + extension at the leaf radius, Poiseuille 8 mu L/(pi r^4); used only for relax", R_own_details=rown_info,
                throat_probe=tp["probe_id"], measurement_probe=mp["probe_id"], measurement_probe_used=used, measurement_section_rule=dict(status=srule["status"], why_not_ok=srule["why_not_ok"], mesh_checked=srule["mesh_checked"]),
                measurement_probe_relocated=reloc, mesh_source_dir=os.path.abspath(mesh_dir), probe_section_check=psc, production_ready=bool(mesh_check), blinding="no 0D twin / zerod_ffr / Tree / outlets_837 import in this code path; analyze_case.py registers a constants-only zerod_ffr stand-in",
                p_bcA_x_bcC_Pa={o["patch"]: C.PV + o["R"] * o["Q_target_m3s"] for o in outlets}, p_init_capped={o["patch"]: o["p_init_capped"] for o in outlets}, n_bl_layers_recorded_by_mesh_stage=None,
                note_bcA_bcC="Pv + R(bc_A) Q(bc_C) equals the CLEAN outlet pressures for clean_nolesion and baseline; for T1_missed_branch bc_C holds the FULL territory flows (decision B1), so it is only a reference and exceeds P_aorta at the outlet that inherits the deleted branch (19.1 kPa for out_558 vs 12.0 kPa); the prescribed-mode bc_err of analyze_case compares the CFD patch p with it and is reported, not judged; initial outlet p is capped at 0.98 p0")
    mesh_dir = os.path.abspath(mesh_dir); lost_reasons = lost_outlet_reasons(mesh_dir, [o["patch"] for o in outlets])
    pl = lambda k: dict(point_m=planes[k]["point_m"], normal=planes[k]["normal"], bounds_m=planes[k]["bounds_m"])
    b = C.write_case(os.path.abspath(outdir), mode, C.poly_dir(mesh_dir), f"{TEMPLATE}/system", f"{TEMPLATE}/constant", outlets, p0, nproc, closed_patches=closed, throat_plane=pl("throat"), ramp_iters=ramp, info=info,
                     measurement_plane=pl("measurement"), extra_planes=({"measurementOrig": pl("measurement_orig")} if "measurement_orig" in planes else None), lost_reasons=lost_reasons)
    for o in b["outlets_lost_in_mesh"]: print(f"{name}: OUTLET_LOST_IN_MESH {o['patch']} (0 faces): no monitors written, BC entries kept (inert); territory closed (bc_C {o['Q_target_m3s'] * 1e6:.5f} mL/s not delivered). Reason: {o['reason']}")
    if not mesh_check: open(f"{os.path.abspath(outdir)}/NOT_FOR_PRODUCTION", "w").write("built with --no-mesh-check: the bounded probe planes were sized from the centreline only and NOT checked on a mesh\n")
    return b

def main(argv):
    if len(argv) < 3: raise SystemExit(__doc__)
    def opt(flag, default=None):
        return argv[argv.index(flag) + 1] if flag in argv else default
    flags = {"--pkg-root", "--extensions-json", "--e0-waiver", "--ramp", "--csv-subset", "--r-scale"}
    pos = [x for i, x in enumerate(argv) if x not in flags and x != "--no-mesh-check" and (i == 0 or argv[i - 1] not in flags)]
    if pos[2] == "roundtrip":
        import pf_roundtrip_build
        return pf_roundtrip_build.main(pos[1], int(pos[3]) if len(pos) > 3 else None)
    if len(pos) < 4: raise SystemExit(__doc__)
    b = build(pos[0], pos[1], pos[2], pos[3], int(pos[4]) if len(pos) > 4 else 16, opt("--pkg-root"), opt("--extensions-json"), opt("--e0-waiver"), int(opt("--ramp", 0)), opt("--csv-subset", e0_check.DEFAULT), mesh_check="--no-mesh-check" not in argv, r_scale=float(opt("--r-scale", 1.0)))
    print(f"built {pos[3]} ({b['mode']}): outlets {[o['patch'] for o in b['outlets']]}, closed {b['closed_patches']}, ranks {b['nproc']}, mesh {b['mesh_link']}, E0 {b['e0_guard']['status']}, extensions: {b['extension_source']}, probe planes: " + ", ".join(f"{k} {v['status']} h={v['h_final_mm']:.3f} mm" for k, v in b['probe_section_check'].items() if isinstance(v, dict)) + f"; measurement probe used {b['measurement_probe_used']} (section rule {b['measurement_section_rule']['status']})")

if __name__ == "__main__":
    main(sys.argv[1:])
