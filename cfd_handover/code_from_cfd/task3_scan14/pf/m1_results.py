"""M1 return files from a finished case: M1_outlets_<case>_<mode>.csv and a row of M1_results.csv (the shipped M1_results_TEMPLATE.csv columns + extension_lengths_mm, n_bl_layers, throat_cell_um_p95, peak_ram_gb,
physical_cores, roundtrip_max_err_pct). Reads only the case's monitors/logs/build_info and small json/csv files: no fields, no 0D code.
usage: m1_results.py <case_dir> <case_label> <mode: resistance|prescribed> [--analysis analysis_pf.json] [--roundtrip roundtrip_result.json] [--probes M1_probes_...csv]
                     [--fill-json file.json ...] [--set key=value ...] [--peak-ram-gb X] [--outdir dir] [--force]
Solver columns come from analysis_pf.json (analyze_case.py; created if missing, regenerated if its provenance - size + sha256 of log.simpleFoam and the monitor .dat files - does not match the files on disk
or with --force): converged (adjusted verdict), iterations, final_residual_p/U, mass_imbalance_pct, Q_inlet_mls, wallclock_min and cores from log.simpleFoam
(ExecutionTime/ClockTime) and decomposeParDict, Re_throat = 4 rho |Q| / (pi mu D) with Q = Q_through_mls and D = 2 r_eq_mm of the SAME throat-section row of the probes csv (--probes, kind 'throat'; cross-checked against its
Re_section column). Never from the throatFlux/throatP monitors: they sample an INFINITE plane that also cuts other branches of the tree. Without --probes (or without a valid throat row) Re_throat stays EMPTY and notes say why. Geometry / mesh columns (geometry_step_ok, manual_repair_needed, n_surface_components, throat_radius_asbuilt_mm, throat_pct_error, subdivision_edge_mm, n_cells,
throat_cells_across, checkMesh_ok, max_nonortho_deg, max_skewness, neg_volumes, vmtk_version, mesher, n_bl_layers, throat_cell_um_p95, openfoam_version) are taken from the geometry/mesh stages' gate files through --fill-json (any json whose
keys are column names; later files override earlier ones) or --set. Unknown columns stay empty (never invented). The row is written/replaced by (case, bc_mode) in <outdir>/M1_results.csv."""
import sys, os, re, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pf_common as C

COLS = ["case", "geometry_step_ok", "manual_repair_needed", "n_surface_components", "throat_radius_asbuilt_mm", "throat_radius_target_mm", "throat_pct_error", "subdivision_edge_mm", "n_cells", "throat_cells_across", "checkMesh_ok",
        "max_nonortho_deg", "max_skewness", "neg_volumes", "bc_mode", "relax_used", "converged", "iterations", "final_residual_p", "final_residual_U", "mass_imbalance_pct", "Q_inlet_mls", "Re_throat", "wallclock_min", "cores",
        "openfoam_version", "vmtk_version", "mesher", "notes", "extension_lengths_mm", "n_bl_layers", "throat_cell_um_p95", "peak_ram_gb", "physical_cores", "roundtrip_max_err_pct"]

def log_times(case):
    txt = open(f"{case}/log.simpleFoam").read(); m = re.findall(r"ExecutionTime = ([0-9.]+) s\s+ClockTime = (\d+) s", txt)
    return (float(m[-1][0]), int(m[-1][1])) if m else (None, None)

def outlets_csv(case, label, mode, out, analysis):
    info = json.load(open(f"{case}/build_info.json")); rows = []
    plan = json.load(open(f"{case}/roundtrip_plan.json")) if os.path.exists(f"{case}/roundtrip_plan.json") else None
    for o in info["outlets"]:
        p = o["patch"]; L = analysis["last100"][p]
        if info["mode"] == "resistance": R, Rsrc = o["R_used"], ("derived from the prescribed solve (last-100 means)" if plan else "bc_A.csv")
        else: R, Rsrc = (L["p_last100_Pa"] - C.PV) / L["Q_last100_m3s"], "derived here from THIS prescribed solve: (p_bar - Pv)/Q, last-100 means"
        rows.append(dict(case=label, mode=mode, outlet_id=p, tree_node=o.get("code_name", "")[3:] or "", R_SI=R, R_source=Rsrc, relax=o.get("relax"), Q_mls=L["Q_last100_m3s"] * 1e6, Q_target_bcC_mls=o["Q_target_m3s"] * 1e6,
                         Q_over_target_minus_1_pct=L["Q_over_target_minus_1_pct"], Q_band_last100_pct=L["Q_last100_band_pct"], p_bar_Pa=L["p_last100_Pa"], p_bar_over_Paorta=L["p_last100_Pa"] / C.P_AORTA_PA,
                         p_bar_band_last100_pct=L["p_last100_band_pct"], p_bcA_x_bcC_Pa=(info.get("p_bcA_x_bcC_Pa") or {}).get(p), closed=0))
    for c in info.get("closed_patches", []) + [x for x in info.get("closed_outlets", []) if x not in info.get("closed_patches", [])]:
        rows.append(dict(case=label, mode=mode, outlet_id=c, Q_mls=0.0, closed=1, R_source="closed outlet = wall (bc_A/bc_C mode closed)"))
    cols = ["case", "mode", "outlet_id", "tree_node", "R_SI", "R_source", "relax", "Q_mls", "Q_target_bcC_mls", "Q_over_target_minus_1_pct", "Q_band_last100_pct", "p_bar_Pa", "p_bar_over_Paorta", "p_bar_band_last100_pct", "p_bcA_x_bcC_Pa", "closed"]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    return rows

def throat_re(probes, nolesion=False):
    """(Re_throat, note) from the kind == 'throat' row of the probes csv: Re = 4 rho |Q_through| / (pi mu 2 r_eq), same row, cross-checked against its Re_section. (None, reason) when it cannot be computed."""
    if not probes: return None, "Re_throat not computed: no --probes file given (the throatFlux/throatP plane monitors are NOT used: infinite plane, cuts other branches)"
    if not os.path.exists(probes): return None, f"Re_throat not computed: probes file {probes} missing (plane monitors NOT used)"
    t = [r for r in csv.DictReader(open(probes)) if r.get("kind") == "throat"]
    if len(t) != 1: return None, f"Re_throat not computed: {len(t)} 'throat' rows in {os.path.basename(probes)} (need exactly 1; plane monitors NOT used)"
    r = t[0]
    if str(r.get("section_ok", "1")) not in ("1", "True", "true") or not r.get("Q_through_mls") or not r.get("r_eq_mm"):
        return None, f"Re_throat not computed: throat probe {r.get('probe_id')} section invalid or empty in {os.path.basename(probes)} (plane monitors NOT used)"
    Q, D = abs(float(r["Q_through_mls"])) * 1e-6, 2 * float(r["r_eq_mm"]) * 1e-3
    Re = 4 * C.RHO * Q / (np.pi * C.MU * D)
    note = f"Re_source: probes row {r.get('probe_id')} (kind throat, s_mm={r.get('s_mm')}) of {os.path.basename(probes)}: |Q_through|={Q * 1e6:.6g} mL/s, D=2 r_eq={D * 1e3:.6g} mm"
    if r.get("Re_section"):
        rs = float(r["Re_section"]); note += f", Re={Re:.4g} (Re_section column {rs:.4g}" + (", agrees)" if abs(Re - rs) <= 1e-3 * max(abs(rs), 1e-12) else ", DISAGREES: value computed here is reported)")
    if nolesion: note += "; case without a lesion: row taken at the would-be throat station (not a stenosis throat)"
    return Re, note

def main(argv):
    if len(argv) < 3: raise SystemExit(__doc__)
    case, label, mode = os.path.abspath(argv[0]), argv[1], argv[2]; g = lambda f, d=None: argv[argv.index(f) + 1] if f in argv else d
    outdir = g("--outdir", os.getcwd()); info = json.load(open(f"{case}/build_info.json")); assert info["mode"] == mode, (info["mode"], mode)
    aj = g("--analysis", f"{case}/analysis_pf.json")
    import analyze_case; an = analyze_case.load_or_run(case, aj, force="--force" in argv)
    fill = {}
    i = 0
    while i < len(argv):
        if argv[i] == "--fill-json": fill.update({k: v for k, v in json.load(open(argv[i + 1])).items()}); i += 2
        elif argv[i] == "--set": k, v = argv[i + 1].split("=", 1); fill[k] = v; i += 2
        else: i += 1
    exec_s, clock_s = log_times(case); rp = an["residuals_last"]
    row = {c: "" for c in COLS}
    row.update({k: v for k, v in fill.items() if k in COLS})
    row.update(case=label, bc_mode="prescribed-flow" if mode == "prescribed" else "resistance", converged=an["verdict"], iterations=an["last_iteration"], final_residual_p=rp["p"], final_residual_U=max(rp["Ux"], rp["Uy"], rp["Uz"]),
               mass_imbalance_pct=an["mass_imbalance_pct"], Q_inlet_mls=an["inlet_flux_mls"], wallclock_min=(clock_s / 60 if clock_s is not None else ""), cores=info["nproc"], physical_cores=16,
               relax_used=("n/a (flows prescribed)" if mode == "prescribed" else "; ".join(f"{o['patch']}={o['relax']:.5f}" for o in info["outlets"])), extension_lengths_mm=json.dumps(info.get("extension_lengths_mm", {})),
               peak_ram_gb=g("--peak-ram-gb", row.get("peak_ram_gb", "")))
    if mode == "prescribed" and an.get("dropped_checks"): row["notes"] = f"prescribed-flow verdict adjusted (dropped check(s): {list(an['dropped_checks'])}, see analysis_pf.json); " + str(row.get("notes", ""))
    if info.get("pilot_label") or info.get("label"): row["notes"] = f"{info.get('pilot_label') or info.get('label')}; " + str(row.get("notes", ""))
    # throat Re from the throat SECTION of the probes csv (never from the infinite-plane monitors throatFlux/throatP)
    re_val, re_note = throat_re(g("--probes"), info.get("error_type") == "clean_nolesion" or "nolesion" in label)
    row["Re_throat"] = "" if re_val is None else re_val
    row["notes"] = (str(row.get("notes", "")).rstrip() + " | " if str(row.get("notes", "")).strip() else "") + re_note
    print(re_note)
    rt = g("--roundtrip")
    if rt: row["roundtrip_max_err_pct"] = json.load(open(rt))["roundtrip_max_err_pct"]
    os.makedirs(outdir, exist_ok=True)
    outlets_csv(case, label, mode, f"{outdir}/M1_outlets_{label}_{mode}.csv", an)
    f = f"{outdir}/M1_results.csv"; rows = list(csv.DictReader(open(f))) if os.path.exists(f) else []
    rows = [r for r in rows if not (r["case"] == label and r["bc_mode"] == row["bc_mode"])] + [row]
    with open(f, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    print(f"wrote {outdir}/M1_outlets_{label}_{mode}.csv and the ({label}, {row['bc_mode']}) row of {f}")

if __name__ == "__main__":
    main(sys.argv[1:])
