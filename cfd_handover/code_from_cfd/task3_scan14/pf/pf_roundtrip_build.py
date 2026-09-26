"""Stage 2 of the prescribed-flow round trip (Item 1 pf_* and scan-14 M1 cases alike): from a FINISHED, CONVERGED prescribed-flow case derive R_i = (pbar_i*rho - Pv)/Q_i per outlet
(pbar_i = last-100 mean of the outlet-patch area-average p monitor, Q_i = last-100 mean of the outlet flux monitor, Pv = 666.61 Pa) and build the resistance-mode case that uses exactly those R_i.
usage: pf_roundtrip_build.py <prescribed_case_dir> [nproc] [--force]   (default: the prescribed case's own rank count; --force: regenerate analysis_pf.json even if its provenance matches)  -> sibling dir <prescribed name with 'prescribed' -> 'roundtrip'>
Refuses unless <case>/analysis_pf.json exists (written by analyze_case.py --json) with the adjusted verdict CONVERGED and a finished log; the json is used only if its provenance (size + sha256 of log.simpleFoam and the monitor .dat files) matches the files on disk, else it is
regenerated first (analyze_case.load_or_run). relax_i = min(0.5, 1/(1+R_i/R_own,i)) with R_own,i from the prescribed case's build_info (the
same numbers that gave the audited relax of the resistance solves). Mesh hard-linked from the prescribed case (same filesystem), fvSchemes/fvSolution copied from it. Initial outlet p = the prescribed solve's pbar_i.
Also writes roundtrip_plan.json: derived vs reference R_i (Item 1: the resistance solve the targets came from; M1: bc_A), pbar, bands. No 0D code is imported."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pf_common as C
import analyze_case as AC

def main(pcase, nproc=None, force=False):
    pcase = os.path.abspath(pcase); info = json.load(open(f"{pcase}/build_info.json"))
    if info["mode"] != "prescribed": raise SystemExit(f"{pcase} is not a prescribed-flow case")
    aj = f"{pcase}/analysis_pf.json"
    if not os.path.exists(aj): raise SystemExit(f"{aj} missing: run analyze_case.py {pcase} --json {aj} first")
    a = AC.load_or_run(pcase, aj, force=force)
    if a.get("verdict") != "CONVERGED" or not a["strict"]["log_finished"]: raise SystemExit(f"prescribed solve not converged/finished (verdict {a.get('verdict')}, log_finished {a['strict']['log_finished']}): the round trip is NOT ASSESSABLE")
    if a["last_iteration"] != a["log_last_iteration"]: raise SystemExit("analysis is stale (last_iteration != log iteration): re-run analyze_case.py")
    patches = [o["patch"] for o in info["outlets"]]; d = C.derive_R(pcase, patches, 100)
    outlets = []; plan = {}
    for o in info["outlets"]:
        p = o["patch"]; R = d[p]["R_derived"]; Rown = o["R_own"]
        if Rown is None: raise SystemExit(f"{p}: no R_own in build_info")
        G, relax = C.relax_from_G(R, Rown)
        outlets.append(dict(patch=p, code_name=o["code_name"], R=R, R_ref=o["R_ref"], R_own=Rown, G=G, relax=relax, Q_target_m3s=o["Q_target_m3s"], p_init_kin=d[p]["p_bar_kin"]))
        plan[p] = dict(R_derived=R, R_reference=o["R_ref"], R_derived_over_reference_minus_1_pct=(100 * (R / o["R_ref"] - 1)) if o["R_ref"] else None, p_bar_Pa=d[p]["p_bar_Pa"], p_band_pct=d[p]["p_band_pct"],
                       Q_m3s=d[p]["Q_m3s"], Q_band_pct=d[p]["Q_band_pct"], Q_target_m3s=o["Q_target_m3s"], relax=relax, G=G, last_iteration=d[p]["last_iteration"])
    name = os.path.basename(pcase); assert "prescribed" in name
    case = os.path.join(os.path.dirname(pcase), name.replace("prescribed", "roundtrip"))
    extra = {k: info[k] for k in ("family", "label", "ds", "package", "pilot_label", "extension_lengths_mm", "extension_source", "e0_guard", "R_own_definition") if k in info}
    extra.update(stage="roundtrip", derived_from=pcase, R_source="derived from the prescribed solve (last-100 means)")
    b = C.write_case(case, "resistance", C.poly_dir(pcase), f"{pcase}/system", f"{pcase}/constant", outlets, info["p0_kin"], nproc or info["nproc"], closed_patches=info.get("closed_patches", []),
                     throat_plane=None if info.get("throat_plane") is None else (info["throat_plane"]["point_m"], info["throat_plane"]["normal"]), info=extra)
    json.dump(plan, open(f"{case}/roundtrip_plan.json", "w"), indent=1)
    print(f"built {case}: " + ", ".join(f"{p} R {v['R_derived']:.6e} ({v['R_derived_over_reference_minus_1_pct']:+.3f} % vs reference) relax {v['relax']:.5f}" for p, v in plan.items()))

if __name__ == "__main__":
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    pos = [a for a in sys.argv[1:] if a != "--force"]
    main(pos[0], int(pos[1]) if len(pos) > 1 else None, force="--force" in sys.argv)
