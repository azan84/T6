"""E60 (extended 50 um tube) versus M50 (audited tube to arc 36 mm) at resting flow: the ten registered quantities of the frozen mesh_sensitivity.py, each pair with its OWN reference.
Read-only on the case outputs; writes only the output json. Written before the E60 runs (extended_tube_design.md section 4).
usage: e60_compare.py <out.json> [tube_end_mm=58.0]
Validity (same conditions as hyp_compare, via hyp_compare.case_validity): for all four cases strict verdict (analyze_solve --strict) and stored verdict CONVERGED, log finished,
freshness tied to the final iteration (analysis.json, sections/wss json time, largest time directory, all monitors equal and ending at it); measurement-plane stability (design 5c(e))
REQUIRED for the two E60 cases and NOT required for the two M50 cases (solve_lesion80, solve_baseline_ref: analysed long before 5c(e), no previous-write sections exist).
The frozen loader (mesh_sensitivity.load_safe) must also give 'ok' and time-consistent. Otherwise exit 1, no comparison, and the reasons are listed.
Coverage: the frozen quantities use the sections csv (ends at 49 mm) and the WSS csv (ends at 45 mm); the analysed window ends are read from the csvs and reported. If the last reversed
station reaches within 2 mm of its window end, the reversed extent beyond the window is NOT ASSESSABLE (flag reversed_flow_reaches_analysis_window).
HYP4 finding 2 (attempt Fable-1): coverage counts FINITE samples only (hyp_compare.finite_extent): the window ends are the last finite (ok) stations; an extent 'ends inside'
its window only when no station between its last reversed station and the window end is missing, otherwise NOT ASSESSABLE (flag reversed_extent_not_assessable); a
'no reversed station' claim needs finite coverage from the search start (sections s > 30, wall s > S_C) to the window end; reattachment_wss's own missing_stations_in_window
and outcomes are propagated with their coverage (wss_outcome_assessment)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import mesh_sensitivity as MS
import hyp_compare as H

M50 = ("solve_lesion80", "solve_baseline_ref"); E60 = ("solve_lesion80_E60", "solve_baseline_ref_E60")
TUBE_END_E60 = 58.0   # arc of the end of the last 50 um cylinder of the E60 meshes (make_lesion_mesh.py --tube-end=60: frames end at 58.83 mm, last cylinder at 58.0 mm), not 60
PLANE_NOTE = ("measurement-plane stability (design 5c(e)) is REQUIRED for the E60 cases and NOT required for the M50 cases solve_lesion80/solve_baseline_ref, "
              "which were analysed long before 5c(e) was registered (no previous-write sections exist); for them: strict verdict + finished log + freshness only")

def validity(c, mode, need_plane):
    v = H.case_validity(os.path.join(MS.BASE, c), mode, need_plane, tag=c)
    return dict(valid=v["valid"], reasons=v["reasons"], strict_verdict=v["strict_verdict"], stored_verdict=v["stored_verdict"], log_finished=v["log_finished"],
                final_iteration=v["final_iteration"], plane_stability_required=v["plane_stability_required"],
                plane=None if v["plane"] is None else {k: v["plane"][k] for k in ("status", "reason", "expected_time_prev", "rule", "time_prev", "gap_iterations", "rel_change")})

def load(c, mode):
    try: return MS.load_safe(c, mode)
    except SystemExit as e: return dict(kind="missing", A=dict(verdict="MISSING"), name=c, time_consistent=False, load_error=str(e))

def pair(les, ref):
    c, r = load(les, "lesion80"), load(ref, "baseline_ref")
    ok = c["kind"] == "ok" and r["kind"] == "ok" and c["time_consistent"] and r["time_consistent"]
    return c, r, ok, (MS.quantities(c, r) if ok else None)

def extent_details(c):
    """Finite-coverage extents (hyp_compare.finite_extent) of the frozen descriptive quantities: sections s > 30 mm with ok=True and frac_reversed_area >= 0.01,
    wall stations s > S_C with f_rev >= 0.05 (thresholds unchanged, extended_tube_design.md section 4)."""
    S, W = c["S"], c["W"]
    Ss = S[S["s_mm"] > 30.0]; v = np.where(np.asarray(Ss["ok"]).astype(bool), np.asarray(Ss["frac_reversed_area"], float), np.nan)
    Ws = W[W["s_mm"] > S_C]
    return dict(section=H.finite_extent(np.asarray(Ss["s_mm"], float), v, 0.01, 30.0), wall=H.finite_extent(np.asarray(Ws["s_mm"], float), np.asarray(Ws["f_rev"], float), 0.05, S_C))

def last_reversed(c):
    d = extent_details(c)
    return dict(last_section_reversed_area_ge_1pct_s_gt_30=d["section"]["last_reversed_mm"], last_wall_station_f_rev_ge_5pct=d["wall"]["last_reversed_mm"])

def window_ends(c):
    """Analysed window ends from the actual csvs: last FINITE ok section, last FINITE WSS station (a NaN row is not coverage)."""
    S, W = c["S"], c["W"]
    okS = S[np.asarray(S["ok"]).astype(bool) & np.isfinite(np.asarray(S["frac_reversed_area"], float))]; fW = W[np.isfinite(np.asarray(W["f_rev"], float))]
    return dict(section_window_end_mm=float(okS["s_mm"].max()) if len(okS) else None, wss_window_end_mm=float(fW["s_mm"].max()) if len(fW) else None)

def reach(d):
    """From extent_details: (reaches-window flags, statement per metric, not-assessable flags). 'ends inside' is stated only when no station is missing after the
    last reversed station; a last reversed station >= window end - 2 mm reaches the window (extent beyond it NOT ASSESSABLE); a gap makes the extent NOT ASSESSABLE."""
    r = {k: bool(d[k]["reaches_window_end"]) for k in ("section", "wall")}
    na = {k: bool(not d[k]["end_established"]) for k in ("section", "wall")}
    return r, {k: d[k]["status"] for k in ("section", "wall")}, na

def wss_outcomes(pair_names):
    out = {}
    for tag, c, mode in zip(("lesion", "reference"), pair_names, ("lesion80", "baseline_ref")):
        d = os.path.join(MS.BASE, c)
        try: Wj = json.load(open(f"{d}/wss_{mode}.json")); W = MS.load_safe(c, mode)["W"]
        except Exception as e: out[tag] = dict(outcome_assessed=f"NOT ASSESSABLE (wss_{mode}.json/csv unreadable: {type(e).__name__}: {e})", not_assessable=True); continue
        out[tag] = H.wss_outcome_assessment(W, Wj, S_C)
    return out

S_C = 23.5

def main(out, tube_end=TUBE_END_E60):
    try: outf = open(out, "w")
    except OSError as e: raise SystemExit(f"cannot write {out!r}: {e}")
    val = {c: validity(c, m, need) for c, m, need in ((M50[0], "lesion80", False), (M50[1], "baseline_ref", False), (E60[0], "lesion80", True), (E60[1], "baseline_ref", True))}
    all_valid = all(v["valid"] for v in val.values())
    cm, rm, okm, qm = pair(*M50); ce, re_, oke, qe = pair(*E60)
    done = bool(all_valid and okm and oke)
    res = dict(M50=dict(zip(("lesion", "reference"), M50)), E60=dict(zip(("lesion", "reference"), E60)),
               loaded=dict(M50=[cm["kind"], rm["kind"]], E60=[ce["kind"], re_["kind"]]), validity=val, plane_stability_note=PLANE_NOTE, comparison_done=done)
    if not done:
        reasons = [r for v in val.values() for r in v["reasons"]] + [f"{d['name']}: frozen loader kind={d['kind']} time_consistent={d['time_consistent']}" + (f" ({d['load_error']})" if d.get("load_error") else "")
                                                                   for d in (cm, rm, ce, re_) if not (d["kind"] == "ok" and d["time_consistent"])]
        res["reason"] = "not all four cases are valid (CONVERGED strict+stored, finished, fresh at the final iteration, E60 planes stable) and loadable: no comparison (only last-500 bands of unconverged cases may be quoted)"
        res["reasons"] = reasons
        json.dump(res, outf, indent=1, default=float); outf.close(); print(res["reason"]); print(PLANE_NOTE); [print("  -", r) for r in reasons]; raise SystemExit(1)
    rows = {}
    for name, (kind, tol) in MS.TOL.items():
        a, b = qm[name], qe[name]; t = tol * (abs(a) if kind == "rel" and np.isfinite(a) else 1.0)
        finite = bool(np.isfinite(a) and np.isfinite(b))
        rows[name] = dict(M50=a, E60=b, difference=(b - a) if finite else None, tolerance=t, kind=kind,
                          moved_by_extension=(bool(MS.exceeds(b - a, t)) if finite else None), assessable=finite)
    res["quantities"] = rows
    res["outcome_categories"] = dict(M50=qm["outcome_category"], E60=qe["outcome_category"]); res["physical_outcome_notes"] = dict(M50=qm["physical_outcome_notes"], E60=qe["physical_outcome_notes"])
    res["reversed_extent"] = dict(M50=last_reversed(cm), E60=last_reversed(ce))
    res["analysis_window_ends"] = dict(M50=window_ends(cm), E60=window_ends(ce))
    det = dict(M50=extent_details(cm), E60=extent_details(ce)); rch = {k: reach(det[k]) for k in ("M50", "E60")}
    res["reversed_extent_assessment"] = {k: v[1] for k, v in rch.items()}
    res["reversed_extent_coverage"] = {k: {m: {kk: det[k][m][kk] for kk in ("window_end_mm", "n_finite", "n_missing", "missing_stations", "missing_stations_in_window", "missing_stations_after_last_reversed", "end_established")}
                                           for m in ("section", "wall")} for k in ("M50", "E60")}
    res["wss_outcome_assessment"] = dict(M50=wss_outcomes(M50), E60=wss_outcomes(E60))   # finding 2 (iii)
    res["flags"] = dict(reversed_flow_reaches_analysis_window=rch["E60"][0], reversed_flow_reaches_analysis_window_M50=rch["M50"][0],
                        reversed_extent_not_assessable=rch["E60"][2], reversed_extent_not_assessable_M50=rch["M50"][2],
                        wss_outcome_not_assessable={k: {t_: a["not_assessable"] for t_, a in v.items()} for k, v in res["wss_outcome_assessment"].items()}, tube_end_mm=tube_end,
                        tube_end_note=f"E60 fine tube ends at arc {tube_end:g} mm; the design's interface flag (last reversed arc > tube end - 4 mm) is NOT ASSESSABLE because the analysed windows end at "
                                      f"{res['analysis_window_ends']['E60']['section_window_end_mm']} mm (sections) / {res['analysis_window_ends']['E60']['wss_window_end_mm']} mm (WSS)")
    Sm, Se = cm["S"], ce["S"]
    def p40(S): r = S[(S.s_mm - 40.0).abs() < 1e-6]; return float(r.iloc[0].p_over_Pao) if len(r) == 1 and bool(r.iloc[0].ok) else None
    res["p_over_Pao_at_40mm"] = dict(M50_lesion=p40(Sm), E60_lesion=p40(Se), M50_ref=p40(rm["S"]), E60_ref=p40(re_["S"]))
    Wm, We = cm["W"], ce["W"]
    res["f_rev_profile_30_45"] = dict(s_mm=[float(x) for x in Wm.s_mm[(Wm.s_mm >= 30) & (Wm.s_mm <= 45)]],
                                      M50=[float(x) for x in Wm.f_rev[(Wm.s_mm >= 30) & (Wm.s_mm <= 45)]], E60=[float(x) for x in We.f_rev[(We.s_mm >= 30) & (We.s_mm <= 45)]])
    json.dump(res, outf, indent=1, default=float); outf.close()
    print(PLANE_NOTE)
    print("E60 vs M50 (ten registered quantities; tolerance from the frozen script):")
    for k, r in rows.items():
        print(f"  {k:28s} M50 {r['M50']:11.5f}  E60 {r['E60']:11.5f}  diff {'None' if r['difference'] is None else format(r['difference'], '+.5f'):>10}  tol {r['tolerance']:.4f}  moved={r['moved_by_extension']}")   # Fable-1: None (non-finite quantity) crashed the format
    print("analysed window ends:", res["analysis_window_ends"])
    print("reversed extent:", res["reversed_extent"], "|", res["reversed_extent_assessment"], "| flags:", res["flags"])
    print("WSS outcomes (with coverage):", {k: {t_: a["outcome_assessed"] for t_, a in v.items()} for k, v in res["wss_outcome_assessment"].items()})

if __name__ == "__main__":
    if len(sys.argv) < 2: raise SystemExit("usage: e60_compare.py <out.json> [tube_end_mm (default 58.0: the E60 meshes' last 50 um cylinder ends at arc 58.0 mm, frames at 58.83 mm)]")
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else TUBE_END_E60)
