"""U3D per-level report and GCI (u3d_design.md sections 5-6). Read-only on the case dirs.
usage: u3d_analyse.py <out.json> <level>... (3D levels S50 S25A S12A [S25B S12B] -> u3d/case_<level>; wedge levels W0..W4 -> u3d/wedge_<level>)   Reads <case>/{analysis.json (analyze_solve.py --strict), postProcessing/*, build_info.json (mesh gates)}; wedge fluxes are multiplied by build_info wedge_scale (360/theta).
Per level: cells, cells across the throat (median/min), p95 cell size, BL stack, iterations, FFR = p_mean(x=56.5 mm)/P_aorta (last-100 mean and band = max-min over the last 100 iterations), outlet Q (last-100 mean), throat flux and Re
(Re = 4 rho Q / (pi mu D), D = 0.891 mm), verdict. Then successive differences and the Celik et al. (2008) GCI for the zone-A family (h = 50, 25, 12.5 um, r = 2):
e21 = f(S25A) - f(S12A), e32 = f(S50) - f(S25A); p = |ln|e32/e21||/ln 2 (constant r); monotone convergence requires e32/e21 > 0 and |e32/e21| > 1; GCI21 = 1.25 |e21 / f(S12A)| / (2^p - 1). Non-monotone -> GCI not applicable (reported as such)."""
import sys, os, re, json
import numpy as np
U = os.path.dirname(os.path.abspath(__file__))
P_AORTA_KIN, RHO, MU, D_T = 11.3198, 1060.0, 0.004, 0.891e-3
SETTLE_DRIFT, SETTLE_BAND = 2e-4, 1e-4      # design v2.4: |mean(2nd 250 of final 500) - mean(1st 250)| <= 2e-4 and last-100 band <= 1e-4
def need(path, what):
    if not os.path.isfile(path): raise SystemExit(f"u3d_analyse: level {what}: missing input file {path}")
    return path
def mon(case, name): return f"{case}/postProcessing/{name}/0/surfaceFieldValue.dat"
def series(case, name, l="?"):
    d = np.loadtxt(need(mon(case, name), l), comments="#", ndmin=2); return d[:, 0], d[:, 1:]
def level(l):
    wedge = l.startswith("W")
    c = f"{U}/{'wedge_' if wedge else 'case_'}{l}"; bi = json.load(open(need(f"{c}/build_info.json", l))); g = bi["mesh_gates"]; A = json.load(open(need(f"{c}/analysis.json", l)))
    scale = float(bi["wedge_scale"]) if wedge else 1.0          # wedge monitors hold theta/360 of the full flux
    t, pm = series(c, "measurementP", l); ffr = pm[:, 0] / P_AORTA_KIN; last = ffr[-100:]
    to, qo = series(c, "outletFlux", l); tt, qt = series(c, "throatFlux", l)
    files = ", ".join(mon(c, n) for n in ("measurementP", "outletFlux", "throatFlux"))
    if not (np.array_equal(t, to) and np.array_equal(t, tt)): raise SystemExit(f"u3d_analyse: level {l}: the iteration columns of the three monitors differ: {files}")
    if not (len(t) and np.all(np.isfinite(t)) and np.all(np.diff(t) > 0)): raise SystemExit(f"u3d_analyse: level {l}: iteration column not finite and strictly increasing: {files}")
    if not (np.all(np.isfinite(ffr[-500:])) and np.all(np.isfinite(qo[-100:, 0])) and np.all(np.isfinite(qt[-100:, 0]))): raise SystemExit(f"u3d_analyse: level {l}: non-finite monitor value in the last 500 FFR / last 100 fluxes: {files}")
    if "endTime" not in bi: raise SystemExit(f"u3d_analyse: level {l}: no endTime (configured iteration budget) in {c}/build_info.json")
    budget, last_it = int(bi["endTime"]), int(t[-1])      # configured budget vs last OBSERVED iteration
    # outlet patch sum(phi) > 0 for outflow (outward patch normal; cf. analyze_solve.py); throat plane normal +x, areaNormalIntegrate(U) > 0 for forward flow. Both kept signed: a negative value flags reversal/orientation
    qo_m = float(qo[-100:, 0].mean() * 1e6 * scale); qt_m = float(qt[-100:, 0].mean() * 1e6 * scale)
    fin = ffr[-500:]; drift500 = float(abs(fin[250:].mean() - fin[:250].mean())) if len(fin) >= 500 else float("nan"); band100 = float(last.max() - last.min())
    settled = bool(len(fin) >= 500 and drift500 <= SETTLE_DRIFT and band100 <= SETTLE_BAND)      # design v2.4: SETTLED criterion
    d = dict(level=l, family="wedge" if wedge else "3D", cells=g["cells"], strict_failed_checks=g["strict_failed_checks"], max_nonortho=g.get("max_nonortho"), max_skew=g.get("max_skew"),
             iterations=int(t[-1]), FFR_last100_mean=float(last.mean()), FFR_last100_band=float(last.max() - last.min()), outlet_Q_mls=qo_m, throat_Q_mls=qt_m,
             Re_throat=float(4 * RHO * qt_m * 1e-6 / (np.pi * MU * D_T)), verdict=A["verdict"], settled=settled, drift_last500=drift500, budget_iterations=budget, last_iteration=last_it, budget_reached=bool(last_it == budget), failed_checks=[k for k, v in A["checks"].items() if not v], mass_imbalance_pct=A["mass_imbalance_pct"], bc_err_pct=A["outlets"]["outlet"]["bc_err_pct"])
    if wedge:
        rl = A["residuals_last"]; xy_ok = bool(max(rl["Ux"], rl["Uy"]) < 1e-5); failed = d["failed_checks"]
        # the azimuthal component Uz of a one-cell 2-degree wedge is identically ~0, its normalised initial residual stays O(1e-2) whatever the convergence (observed at W0: p 1e-8, Ux 2e-8, Uy 3e-7, Uz 1.6e-2, FFR band 3e-8): reported, and a second verdict without it is given; the decision rules do not use the verdict
        wo = [k for k in failed if k != "U_residual_lt_1e_5"] if xy_ok else failed
        d.update(radial_cells=g["radial_cells"], axial_cell_um_at_throat=g["axial_cell_um_at_throat"], Uz_residual_last=rl["Uz"], verdict_excluding_Uz="CONVERGED" if not wo else "UNCONVERGED", failed_checks_excluding_Uz=wo)
    else: d.update(cells_across_throat_median=g["cells_across_throat_diameter"]["median"], cells_across_throat_min=g["cells_across_throat_diameter"]["min"], cell_size_p95_um=g["cell_size_um_x31.5_pm2mm"]["p95"],
                   bl_first_cell_um=g["boundary_layer_um"]["first_cell_median"], bl_stack4_um=g["boundary_layer_um"]["first4_stack_median"])
    return d
def gci(f_fine, f_mid, f_coarse):
    e21, e32 = f_mid - f_fine, f_coarse - f_mid
    if e21 == 0 or e32 == 0: return dict(applicable=False, reason="a zero difference")
    ratio = e32 / e21
    if not (ratio > 1): return dict(applicable=False, reason=f"not monotone-converging (e32/e21 = {ratio:.3f}; requires > 1)", e21=e21, e32=e32)
    p = abs(np.log(abs(ratio))) / np.log(2); return dict(applicable=True, e21=e21, e32=e32, observed_order=float(p), GCI21=float(1.25 * abs(e21 / f_fine) / (2 ** p - 1)), GCI21_absolute=float(1.25 * abs(e21) / (2 ** p - 1)))
TOL_PASS = 0.005
def family(f, band, z):
    lv = {"50": "S50", "25": f"S25{z}", "12": f"S12{z}"}
    if not all(v in f for v in lv.values()): return None
    e21, e32 = f[lv["25"]] - f[lv["12"]], f[lv["50"]] - f[lv["25"]]      # Celik (2008) signs, as in gci(): e21 = f_mid - f_fine, e32 = f_coarse - f_mid
    finest, coarse = abs(e21), abs(e32); nb = max(band[lv["12"]], band[lv["25"]])
    return dict(zone=z, levels=[lv["50"], lv["25"], lv["12"]], e21=e21, e32=e32, finest_pair_abs=finest, coarse_pair_abs=coarse, shrinks=bool(finest < coarse), clearly_smaller=bool(finest < 0.5 * coarse),
                max_band_finest_two=nb, noise_limited=bool(nb > 0.25 * finest), flat=bool(not (finest < coarse) or nb > 0.25 * finest), celik=gci(f[lv["12"]], f[lv["25"]], f[lv["50"]]))
def classify(f, band, wedge, settled=None):
    """Design v2.1 section 11 (iii)/(iv): RULE 1 / 1b / 2 / 3 and the ONE number U3D with its defining sentence. f, band: level -> last-100 mean FFR / band; wedge: the 'wedge' result dict or None.
    settled: level -> SETTLED (design v2.4); a classified level (zone family or three finest wedge levels) missing from it counts as NOT settled. settled=None (omitted):
    no settled information, the SETTLED criterion is not applied at all."""
    fams = [x for x in (family(f, band, z) for z in "AB") if x]
    out = dict(families={x["zone"]: x for x in fams}, zoneB_required_by_work_order=True, zoneB_complete=bool(any(x["zone"] == "B" for x in fams)))      # throat-zone-only refinement => a second, shifted zone is required for the interface test
    if not fams or fams[0]["zone"] != "A": out.update(rule="INCOMPLETE", U3D=None, sentence="zone family A (S50, S25A, S12A) is not complete: no classification"); return out
    def basis(x): return (x["celik"]["GCI21_absolute"], "Celik GCI21") if x["celik"].get("applicable") else (x["finest_pair_abs"], "finest pair (GCI not applicable: " + x["celik"].get("reason", "?") + ")")
    if settled is not None:
        bad = [l for x in fams for l in x["levels"] if not settled.get(l, False)]
        if bad:
            out.update(rule="UNSETTLED", U3D=None, unsettled_levels=sorted(set(bad)), sentence=f"levels {sorted(set(bad))} are not SETTLED at their budget (design v2.4): re-run with double the budget (max 12000); no classification, no U3D")
            return out
    any_flat = any(x["flat"] for x in fams); wedge_clean = None
    if wedge is not None:
        c = wedge["celik"]; wl = wedge["levels"][-3:]; wsettled = settled is None or all(settled.get(l, False) for l in wl)
        wedge_clean = bool(wedge["differences_shrink"] and c.get("applicable") and wedge["finest_pair_abs"] < TOL_PASS) if wsettled else None      # an unsettled wedge level is a budget problem, not evidence of flatness: undecided
        out["wedge_finest_three_settled"] = wsettled
    out["wedge_clean"] = wedge_clean
    if not any_flat:
        vals = [(basis(x), x["zone"]) for x in fams]; (u, how), z = max(vals, key=lambda t: t[0][0]); allpass = all(x["finest_pair_abs"] < TOL_PASS for x in fams)
        out.update(rule="RULE1" if allpass else "RULE1b", U3D=float(u), U3D_basis=how, U3D_zone=z)
        out["sentence"] = (f"U3D = {u:.5f}: the larger, over the zone families {[x['zone'] for x in fams]}, of the 3D FFR discretisation uncertainty at x = 56.5 mm, taken as the {how} of the throat-zone refinement 50/25/12.5 um (dominant family {z}); "
                           + (("all finest pairs < 0.005: PASS, these settings become the study recipe." if out["zoneB_complete"] else "all finest pairs < 0.005: would be a PASS if the shifted-zone family (S25B, S12B) confirms interface insensitivity;")
                              if allpass else "a finest pair is >= 0.005: NO PASS claim; U3D is reported as is."))
        if u >= TOL_PASS: out["sentence"] += " U3D >= 0.005."
    elif wedge_clean is None: out.update(rule="PENDING_WEDGE", U3D=None, sentence="a 3D family is flat; the wedge family is not complete or its finest levels are not SETTLED (re-run with a larger budget), so rule 2 vs rule 3 is undecided")
    elif wedge_clean:
        u = max(x["finest_pair_abs"] for x in fams); z = max(fams, key=lambda x: x["finest_pair_abs"])["zone"]
        out.update(rule="RULE2", U3D=float(u), U3D_basis="3D finest-pair difference", U3D_zone=z)
        out["sentence"] = f"U3D = {u:.5f}: the largest 3D finest-pair FFR difference at x = 56.5 mm (zone {z}); the 3D differences are flat while the wedge family converges cleanly, so the 3D drift is attributed to meshing (interfaces, cfMesh transition cells, zone-only refinement), not to the physics." + (" U3D >= 0.005." if u >= TOL_PASS else "")
    else: out.update(rule="RULE3", U3D=None, sentence="3D and wedge families are both flat: time-accurate pimpleFoam on the finest 3D mesh with the transient BC, time-averaged FFR over the last stable window (mean and band), then stop")
    if out["rule"] in ("RULE1", "RULE1b", "RULE2") and not out["zoneB_complete"]:      # design section 3: without zone B the interface test is missing -> not a PASS by construction; U3D and its basis unchanged
        out["rule"] += "_PROVISIONAL"; out["sentence"] += " PROVISIONAL: zone B not run, the interface-contamination test is missing."
    return out
CLASSIFIED = re.compile(r"^(S50|S25[AB]|S12[AB]|W\d)$")      # only these names feed the zone/wedge families and the classification; any other level (e.g. an archived W3_3000it) is reported in the levels table only
def wedge_key(s_):
    m = re.match(r"W(\d+)", s_); return (int(m.group(1)) if m else 10 ** 9, s_)
def main(out, levels):
    R = {l: level(l) for l in levels}; res = dict(levels=R); used = [l for l in R if CLASSIFIED.match(l)]
    res["levels_reported_only"] = [l for l in R if l not in used]
    if res["levels_reported_only"]: print("levels reported only, NOT used in any family/classification:", res["levels_reported_only"])
    f = {l: R[l]["FFR_last100_mean"] for l in used}; band = {l: R[l]["FFR_last100_band"] for l in used}
    if all(k in f for k in ("S50", "S25A", "S12A")):
        res["zoneA"] = dict(diff_S25A_minus_S50=f["S25A"] - f["S50"], diff_S12A_minus_S25A=f["S12A"] - f["S25A"], finest_pair_abs=abs(f["S12A"] - f["S25A"]), successive_differences_shrink=bool(abs(f["S12A"] - f["S25A"]) < abs(f["S25A"] - f["S50"])),
                            celik=gci(f["S12A"], f["S25A"], f["S50"]))
    if all(k in f for k in ("S25B", "S12B")):
        res["zoneB"] = dict(finest_pair_abs=abs(f["S12B"] - f["S25B"]), diff_S12A_minus_S12B=(f["S12A"] - f["S12B"]) if "S12A" in f else None, diff_S25A_minus_S25B=(f["S25A"] - f["S25B"]) if "S25A" in f else None)
    w = sorted([l for l in f if re.fullmatch(r"W\d", l)], key=wedge_key)
    if len(w) >= 3:
        f3 = [f[x] for x in w[-3:]]        # three finest wedge levels, coarse -> fine
        # gci() assumes r = 2: the three levels must be consecutive W-indices (each step doubles axial and radial counts -> cells x ~4)
        wi = [wedge_key(x)[0] for x in w[-3:]]; wc = [R[x]["cells"] for x in w[-3:]]; cr = [wc[i + 1] / wc[i] for i in range(2)]
        if wi != list(range(wi[0], wi[0] + 3)): wg = dict(applicable=False, reason=f"finest three wedge levels {w[-3:]} are not consecutive refinement steps")
        elif not all(3.5 <= x <= 4.5 for x in cr): wg = dict(applicable=False, reason=f"wedge cell-count ratios {[round(x, 3) for x in cr]} outside 3.5-4.5 (r = 2 in 2D)")
        else: wg = gci(f3[2], f3[1], f3[0])
        res["wedge"] = dict(levels=w, diffs_successive=[f[w[i + 1]] - f[w[i]] for i in range(len(w) - 1)], finest_pair_abs=abs(f[w[-1]] - f[w[-2]]),
                            differences_shrink=bool(all(abs(f[w[i + 1]] - f[w[i]]) < abs(f[w[i]] - f[w[i - 1]]) for i in range(1, len(w) - 1))), celik=wg)
    res["classification"] = classify(f, band, res.get("wedge"), {l: R[l]["settled"] for l in used})
    res["all_converged"] = all((R[l].get("verdict_excluding_Uz") or R[l]["verdict"]) == "CONVERGED" for l in used)      # over the classified levels only
    json.dump(res, open(out, "w"), indent=1, default=float); c = res["classification"]
    print(json.dumps({l: (R[l]["cells"], R[l]["FFR_last100_mean"], R[l]["FFR_last100_band"], R[l]["verdict"]) for l in R})); print("RULE:", c["rule"], "| U3D:", c.get("U3D"), "|", c["sentence"])
if __name__ == "__main__":
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2:])
