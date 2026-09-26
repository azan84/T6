"""Round-trip verdict (Item 1 pf_* and scan-14 M1 alike): the resistance-mode case built by pf_roundtrip_build.py against the flows that the prescribed-flow case imposed.
usage: pf_roundtrip_analyse.py <prescribed_case_dir> <roundtrip_case_dir> [out_stem] [--strict-exit] [--force]      (writes <out_stem>.json and <out_stem>.csv, default <roundtrip_case>/roundtrip_result)
--strict-exit (opt-in): exit code 3 unless status is "PASS" (default: exit 0, everything reported). --force: regenerate both analysis_pf.json even if their provenance matches.
Per outlet: error % = 100 (Q_roundtrip / Q_target - 1) with Q_roundtrip the last-100 mean of the outlet flux monitor; PASS iff every |error| <= 0.5 % (work order Task 3 item 2) AND both solves are valid
(adjusted strict verdict CONVERGED, log finished, analysis not stale: a cached <case>/analysis_pf.json is reused only if its provenance - size and sha256 of log.simpleFoam and of every monitor
.dat it was computed from - matches the files now on disk, else it is regenerated, see analyze_case.load_or_run). If either solve is not valid the status is NOT ASSESSABLE (numbers still reported). Also reported: derived vs reference R_i, the two pbar_i, the
bands, the strict verdicts (prescribed mode: adjusted verdict, dropped checks listed), mass imbalance, roundtrip_max_err_pct (the M1_results column). No 0D code is imported."""
import sys, os, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pf_common as C
import analyze_case as AC

TOL_PCT = 0.5
EXIT_NOT_PASS = 3

def load_or_run(case, force=False):
    return AC.load_or_run(case, f"{case}/analysis_pf.json", force=force)

def main(pcase, rcase, stem=None, force=False):
    pcase, rcase = os.path.abspath(pcase), os.path.abspath(rcase)
    pi, ri = json.load(open(f"{pcase}/build_info.json")), json.load(open(f"{rcase}/build_info.json"))
    if pi["mode"] != "prescribed" or ri["mode"] != "resistance" or ri.get("derived_from") != pcase: raise SystemExit("cases are not a (prescribed, derived resistance) pair")
    pa, ra = load_or_run(pcase, force), load_or_run(rcase, force); plan = json.load(open(f"{rcase}/roundtrip_plan.json"))
    rows, worst = [], 0.0
    for o in ri["outlets"]:
        p = o["patch"]; q = ra["last100"][p]; err = q["Q_over_target_minus_1_pct"]; worst = max(worst, abs(err))
        rows.append(dict(outlet=p, Q_target_mls=o["Q_target_m3s"] * 1e6, Q_roundtrip_mls=q["Q_last100_m3s"] * 1e6, Q_roundtrip_band_pct=q["Q_last100_band_pct"], err_pct=err, pass_0p5=bool(abs(err) <= TOL_PCT),
                         R_derived_SI=plan[p]["R_derived"], R_reference_SI=plan[p]["R_reference"], R_derived_over_reference_pct=plan[p]["R_derived_over_reference_minus_1_pct"], relax=plan[p]["relax"],
                         pbar_prescribed_Pa=pa["last100"][p]["p_last100_Pa"], pbar_roundtrip_Pa=q["p_last100_Pa"], pbar_diff_pct=100 * (q["p_last100_Pa"] / pa["last100"][p]["p_last100_Pa"] - 1)))
    valid = pa.get("verdict") == "CONVERGED" and ra.get("verdict") == "CONVERGED" and pa["strict"]["log_finished"] and ra["strict"]["log_finished"]
    status = ("PASS" if worst <= TOL_PCT else "FAIL") if valid else "NOT ASSESSABLE (a solve is not converged/finished)"
    res = dict(status=status, roundtrip_max_err_pct=worst, tolerance_pct=TOL_PCT, prescribed_case=os.path.basename(pcase), roundtrip_case=os.path.basename(rcase), label=pi.get("label") or pi.get("pilot_label"),
               prescribed_verdict_adjusted=pa.get("verdict"), prescribed_verdict_analyze_solve=pa.get("verdict_analyze_solve"), prescribed_dropped_checks=pa.get("dropped_checks"), roundtrip_verdict=ra.get("verdict"),
               prescribed_mass_imbalance_pct=pa["mass_imbalance_pct"], roundtrip_mass_imbalance_pct=ra["mass_imbalance_pct"], prescribed_iterations=pa["last_iteration"], roundtrip_iterations=ra["last_iteration"],
               prescribed_failed_checks=[k for k, v in pa["checks"].items() if not v], roundtrip_failed_checks=[k for k, v in ra["checks"].items() if not v], outlets=rows)
    stem = stem or f"{rcase}/roundtrip_result"
    json.dump(res, open(stem + ".json", "w"), indent=1)
    with open(stem + ".csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"ROUND TRIP {status}: max |Q error| {worst:.4f} % (tolerance {TOL_PCT} %); " + ", ".join(f"{r['outlet']} {r['err_pct']:+.4f} %" for r in rows))
    return res

if __name__ == "__main__":
    pos = [a for a in sys.argv[1:] if a not in ("--strict-exit", "--force")]
    if len(pos) < 2: raise SystemExit(__doc__)
    res = main(pos[0], pos[1], pos[2] if len(pos) > 2 else None, force="--force" in sys.argv)
    if "--strict-exit" in sys.argv and res["status"] != "PASS":
        print(f"--strict-exit: round-trip status {res['status']} -> exit {EXIT_NOT_PASS}"); sys.exit(EXIT_NOT_PASS)
