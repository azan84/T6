"""Convergence, mass balance, BC accuracy and 0D flow comparison for a finished simpleFoam case.
usage: analyze_solve.py <case_dir> [--json out.json] [--strict]
--strict (opt-in; default off = the audited behaviour) adds to the verdict: all monitor time columns identical, inlet-flux band(200) < 0.1 %,
no fatal/FPE/non-finite residual in the log, all last residuals finite; and writes last-500 min/max of every outlet Q and P and of the inlet Q and P.
res['strict']['log_finished'] (an 'End' line and 'Finalising parallel run' in the last 2000 characters) is reported only, NOT a check: a live case can still be CONVERGED.
Uses postProcessing/*/0/surfaceFieldValue.dat (per-iteration outlet flux and area-averaged static p) and zerod_reference.json."""
import sys, os, json, re
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code")
import numpy as np
from zerod_ffr import RHO, P_VEN, P_AORTA

def series(case, name):
    f = f"{case}/postProcessing/{name}/0/surfaceFieldValue.dat"
    d = np.loadtxt(f, comments="#")
    return d[:, 0], d[:, 1]

def log_residuals(case):
    """Last initial residuals of p and Ux/Uy/Uz and the last iteration number from log.simpleFoam."""
    txt = open(f"{case}/log.simpleFoam").read()
    last = {}
    for fld in ("p", "Ux", "Uy", "Uz"):
        m = re.findall(rf"Solving for {fld}, Initial residual = ([0-9.eE+-]+)", txt)
        last[fld] = float(m[-1]) if m else float("nan")
    it = re.findall(r"^Time = (\d+)", txt, re.M)
    return last, int(it[-1]) if it else None

TRAPFPE_NOTICE = "trapFpe: Floating point exception trapping enabled (FOAM_SIGFPE)."   # the exact startup notice of every log.simpleFoam (the only exempt line)
NONFINITE = re.compile(r"(?i)(?<![a-z])[-+]?(nan|inf|infinity)(?![a-z])")

def raw_residuals(txt):
    """Strict-mode parser: the LAST 'Initial residual' token of each field whatever it is (nan/inf/garbage -> nan), unlike log_residuals which skips 'nan' and fails on '-nan'."""
    raw = {}
    for fld in ("p", "Ux", "Uy", "Uz"):
        mm = re.findall(rf"Solving for {fld}, Initial residual = ([^,\s]+)", txt)
        try: raw[fld] = float(mm[-1]) if mm else float("nan")
        except ValueError: raw[fld] = float("nan")
    return raw

def strict_extras(case, ref, res):
    """Opt-in (strict=True) checks and last-500 bands; returns the added checks. Nothing here runs in the default mode."""
    names = (["inletFlux"] if os.path.exists(f"{case}/postProcessing/inletFlux") else []) + ["inletPressure"] + [f"{p}{k}" for p in ref["outlets"] for k in ("Flux", "Pressure")]
    times = {nm: series(case, nm)[0] for nm in names}
    m = min(len(t) for t in times.values()); spread = max(len(t) for t in times.values()) - m
    mism = [nm for nm, t in times.items() if not np.array_equal(t[:m], times["inletPressure"][:m])]
    full = open(f"{case}/log.simpleFoam").read(); txt = full.splitlines()
    fatal = [ln.strip() for ln in txt if ("FOAM FATAL" in ln or "sigFpe" in ln or "Floating point exception" in ln) and ln.strip() != TRAPFPE_NOTICE]
    finished = any(ln.startswith("End") for ln in txt) and "Finalising parallel run" in full[-2000:]
    nonfin = [ln.strip() for ln in txt if "Solving for" in ln and NONFINITE.search(ln)]
    raw = raw_residuals("\n".join(txt))
    qi = series(case, "inletFlux")[1][-201:] if "inletFlux" in times else None
    inlet_band = float((qi.max() - qi.min()) / abs(qi.mean()) * 100) if qi is not None and len(qi) and qi.mean() != 0 else None
    for patch in ref["outlets"]:
        q = series(case, f"{patch}Flux")[1][-501:]; p = series(case, f"{patch}Pressure")[1][-501:]   # same window as band500_pct
        res["outlets"][patch].update(Q_min_last500_mls=float(q.min() * 1e6), Q_max_last500_mls=float(q.max() * 1e6),
                                     P_min_last500_Pa=float(p.min() * RHO), P_max_last500_Pa=float(p.max() * RHO))
    pi = series(case, "inletPressure")[1][-501:]; qi5 = -series(case, "inletFlux")[1][-501:] * 1e6 if "inletFlux" in times else None   # inflow positive, as inlet_flux_mls
    res["strict"] = dict(monitor_names=names, monitor_length_spread=int(spread), monitors_time_mismatch=mism, inlet_flux_band200_pct=inlet_band,
                         log_fatal_lines=fatal[:5], log_nonfinite_residual_lines=nonfin[:5], residuals_last_raw=raw,
                         last500_window_samples=int(min(501, m)), log_finished=bool(finished),
                         inlet_P_min_last500_Pa=float(pi.min() * RHO), inlet_P_max_last500_Pa=float(pi.max() * RHO),
                         inlet_Q_min_last500_mls=float(qi5.min()) if qi5 is not None and len(qi5) else None,
                         inlet_Q_max_last500_mls=float(qi5.max()) if qi5 is not None and len(qi5) else None)
    return dict(monitors_time_aligned=bool(spread <= 1 and not mism),
                inlet_flux_band200_lt_0_1pct=bool(inlet_band is not None and inlet_band < 0.1),
                log_no_fatal_or_nonfinite=bool(not fatal and not nonfin),
                residuals_all_finite=bool(all(np.isfinite(v) for v in raw.values())))

def main(case, out=None, strict=False):
    ref = json.load(open(f"{case}/zerod_reference.json"))
    res = {"case": os.path.basename(case), "outlets": {}}
    it, qin = series(case, "inletFlux") if os.path.exists(f"{case}/postProcessing/inletFlux") else (None, None)
    _, pin = series(case, "inletPressure")
    n = len(pin); res["last_iteration"] = int(it[-1]) if it is not None else None
    tot = 0.0
    for patch, d in ref["outlets"].items():
        nm = patch
        t, q = series(case, f"{nm}Flux"); _, p = series(case, f"{nm}Pressure")
        Q = q[-1]; P = p[-1] * RHO; R = d["R_out"]
        bc_err = (P - (P_VEN + R * Q)) / (P_VEN + R * Q) * 100
        w200 = q[-201:]; w500 = q[-501:]
        drift200 = (w200.max() - w200.min()) / abs(w200.mean()) * 100
        drift500 = (w500.max() - w500.min()) / abs(w500.mean()) * 100
        q0 = d.get("Q0_mls"); q0h = d.get("Q0_healthy_mls")
        res["outlets"][patch] = dict(Q_mls=Q * 1e6, P_Pa=P, P_over_Paorta=P / P_AORTA, bc_err_pct=bc_err,
                                     band200_pct=drift200, band500_pct=drift500, Q0D_mls=q0, Q0D_healthy_mls=q0h,
                                     Q_vs_0D_pct=(100 * (Q * 1e6 / q0 - 1)) if q0 else None)
        tot += Q
    q_inlet = -tot
    try:
        _, qi = series(case, "inletFlux"); q_inlet = -qi[-1]
    except Exception:
        pass
    res["sum_outlets_mls"] = tot * 1e6
    res["inlet_static_p_Pa"] = float(pin[-1] * RHO); res["inlet_static_p_over_Paorta"] = float(pin[-1] * RHO / P_AORTA)
    res["inlet_flux_mls"] = q_inlet * 1e6 if q_inlet else None
    res["inlet_pressure_band200_pct"] = float((pin[-201:].max() - pin[-201:].min()) / abs(pin[-201:].mean()) * 100)
    res["mass_imbalance_pct"] = float(100 * (tot - q_inlet) / q_inlet) if q_inlet else None
    try:
        resid, log_it = log_residuals(case)
    except ValueError:   # e.g. a '-nan' residual; the default mode keeps the audited behaviour (raise), strict mode records non-finite residuals and fails
        if not strict:
            raise
        txt = open(f"{case}/log.simpleFoam").read(); it_ = re.findall(r"^Time = (\d+)", txt, re.M)
        resid, log_it = raw_residuals(txt), (int(it_[-1]) if it_ else None)
    res["residuals_last"] = resid; res["log_last_iteration"] = log_it
    lens = {len(series(case, f"{p}Flux")[0]) for p in ref["outlets"]} | {len(series(case, f"{p}Pressure")[0]) for p in ref["outlets"]} | {n}
    res["monitor_length_spread"] = max(lens) - min(lens)
    res["monitors_aligned"] = (max(lens) - min(lens) <= 1 and abs(res["last_iteration"] - log_it) <= 1)   # a running solve is up to one iteration ahead in the log (the log prints "Time = N" before the monitors of iteration N are written)
    checks = dict(p_residual_lt_1e_5=bool(resid["p"] < 1e-5), U_residual_lt_1e_5=bool(max(resid["Ux"], resid["Uy"], resid["Uz"]) < 1e-5),
                  at_least_200_iterations=bool(n >= 200), monitors_aligned=bool(res["monitors_aligned"]),
                  mass_imbalance_lt_0_1pct=bool(abs(100 * (tot - q_inlet) / q_inlet) < 0.1) if q_inlet else False,
                  all_bc_err_lt_0_1pct=bool(all(abs(r["bc_err_pct"]) < 0.1 for r in res["outlets"].values())),
                  all_Q_band200_lt_0_1pct=bool(all(r["band200_pct"] < 0.1 for r in res["outlets"].values())),
                  inlet_p_band200_lt_0_1pct=bool(res["inlet_pressure_band200_pct"] < 0.1))
    for patch in ref["outlets"]:
        _, pp = series(case, f"{patch}Pressure"); checks[f"{patch}_P_band200_lt_0_1pct"] = bool((pp[-201:].max() - pp[-201:].min()) / abs(pp[-201:].mean()) * 100 < 0.1)
    if strict:
        checks.update(strict_extras(case, ref, res))
    res["checks"] = checks; res["verdict"] = "CONVERGED" if all(checks.values()) else "UNCONVERGED"
    print(f"{res['case']}: VERDICT {res['verdict']}  residuals p={resid['p']:.2e} U=({resid['Ux']:.1e},{resid['Uy']:.1e},{resid['Uz']:.1e}) log iter {log_it}; failed checks: {[k for k, v in checks.items() if not v]}")
    print(f"{res['case']}: last iter {res['last_iteration']}, sum outlets {tot*1e6:.5f} mL/s, mass imbalance {res['mass_imbalance_pct']} %, "
          f"inlet static p {res['inlet_static_p_Pa']:.2f} Pa ({res['inlet_static_p_over_Paorta']:.5f} Paorta), band(200) {res['inlet_pressure_band200_pct']:.4f} %")
    print(f"{'outlet':11s} {'Q mL/s':>9s} {'0D mL/s':>9s} {'Q/0D-1 %':>9s} {'P/Pao':>8s} {'BCerr %':>9s} {'band200 %':>10s} {'band500 %':>10s}")
    for p, r in res["outlets"].items():
        print(f"{p:11s} {r['Q_mls']:9.5f} {r['Q0D_mls'] or float('nan'):9.5f} {r['Q_vs_0D_pct'] if r['Q_vs_0D_pct'] is not None else float('nan'):+9.2f} "
              f"{r['P_over_Paorta']:8.5f} {r['bc_err_pct']:+9.4f} {r['band200_pct']:10.5f} {r['band500_pct']:10.5f}")
    if strict:
        print(f"{res['case']}: STRICT checks {({k: checks[k] for k in ('monitors_time_aligned', 'inlet_flux_band200_lt_0_1pct', 'log_no_fatal_or_nonfinite', 'residuals_all_finite')})} "
              f"inlet-flux band(200) {res['strict']['inlet_flux_band200_pct']} %, log finished {res['strict']['log_finished']}")
    if out:
        json.dump(res, open(out, "w"), indent=1)
    return res

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None, strict="--strict" in sys.argv)
