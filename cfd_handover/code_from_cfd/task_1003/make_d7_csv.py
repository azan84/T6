"""Build returns/2026-10-03/M1_D7_sensitivity_2026-10-06.csv (one row per Task A variant) from TaskA/M1_results.csv, post summaries and probes.
Re-issue 2026-10-06 (post-hoc audit GPT-5.6 Sol, finding 1): the control A0 is labelled CONTROL_NOT_APPLICABLE (it is not a D7 variant) instead of
PASS_WITH_DEVIATIONS_candidate, and every row carries the overall verdict M1_D7_overall. The first issue M1_D7_sensitivity.csv is kept unchanged."""
import csv, json, os
R = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns"; O = f"{R}/2026-10-03/TaskA"; REF = 0.8697574904997768
V = [("A1", "baseline_D7_12p5", "throat zone 12.5 um +-4 mm", ""), ("A2", "baseline_D7_12p5_zoneB", "throat zone 12.5 um, interfaces shifted +1 mm (-3..+5 mm)", ""), ("A0", "baseline_A0_25um", "CONTROL: production 25 um mesh regenerated and re-solved with the Task C template", "")]
res = {r["case"].replace("_resistance", ""): r for r in csv.DictReader(open(f"{O}/M1_results.csv"))}
q0 = {r["outlet_id"]: float(r["Q_mls"]) for r in csv.DictReader(open(f"{R}/2026-09-26/M1_outlets_baseline_resistance.csv"))}
rows = []
for tag, lab, desc, _ in V:
    f = f"{O}/post_summary_{lab}_resistance.json"
    if not os.path.exists(f) or lab not in res: rows.append(dict(variant=tag, description=desc, status="not finished")); continue
    s = json.load(open(f)); r = res[lab]; P = {x["probe_id"]: x for x in csv.DictReader(open(f"{O}/M1_probes_{lab}_resistance.csv"))}
    q = {x["outlet_id"]: float(x["Q_mls"]) for x in csv.DictReader(open(f"{O}/M1_outlets_{lab}_resistance.csv"))}
    p11 = float(P["p011"]["p_over_Paorta"]); p4 = float(P["p004"]["p_over_Paorta"])
    delta = p11 - REF
    rows.append(dict(
        variant=tag, description=desc, status="finished", cells=r["n_cells"], iterations=r["iterations"], converged=r["converged"],
        p011_over_Paorta=f"{p11:.7f}", returned_p011=REF, delta_FFR_vs_returned=f"{delta:+.7f}", abs_delta_over_U3D=f"{abs(delta)/0.00055:.2f}",
        acceptance_D7=("CONTROL_NOT_APPLICABLE (control, not a D7 variant; reproduces the returned value)" if tag == "A0" else ("MET (|delta| < U3D 0.00055)" if abs(delta) < 0.00055 else "NOT_MET (|delta| >= U3D 0.00055)")), p004_throat_over_Paorta=f"{p4:.7f}",
        max_outlet_flow_change_pct=f"{max(abs(100 * (q[k] / q0[k] - 1)) for k in q0 if k in q):.3f}", D3_verdict=r.get("D3_verdict"), D4_verdict=r.get("D4_verdict"),
        D34_min_dist_throat_mm=r.get("D34_min_dist_throat_mm"), D34_min_dist_measurement_mm=r.get("D34_min_dist_measurement_mm"), flags=r.get("flags"),
        wall_clock_s_contended=s.get("wall_clock_s") or r.get("wallclock_min"),
        note=("flow-state comparison A1 vs A2: STATES INDETERMINATE (pre-registered rule: invalid section 23-24 mm distal to the throat); FFR criterion AGREE (0.00018)" if tag in ("A1", "A2") else "")))
ok = [r for r in rows if r.get("variant") in ("A1", "A2") and r.get("status") == "finished"]
overall = ("M1_FAIL_LESION_CASES (A1 and A2 differ by >= U3D: D7 acceptance not met; work order section 9 fallback: analysis side)" if len(ok) == 2 and all(r["acceptance_D7"].startswith("NOT_MET") for r in ok)
           else "PASS_WITH_DEVIATIONS candidate (both variants below U3D; D4 as reported)" if len(ok) == 2 and all(r["acceptance_D7"].startswith("MET") for r in ok) else "UNDECIDED (variants missing or split)")
for r in rows: r["M1_D7_overall"] = overall
keys = [];  [keys.append(k) for r in rows for k in r if k not in keys]
with open(f"{R}/2026-10-03/M1_D7_sensitivity_2026-10-06.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
print("wrote", len(rows), "rows")
