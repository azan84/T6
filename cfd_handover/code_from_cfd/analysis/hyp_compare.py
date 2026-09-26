"""Post-run comparison for the hyperaemic pair (written BEFORE the runs; read-only on outputs). Pre-registered readings: hyperaemia_design.md section 5.
usage: hyp_compare.py <solve_lesion80_hyp> <solve_baseline_ref_hyp> <out.json> [tube_end_mm (default 36.0 = M50 meshes; 58.0 for the E60 meshes, whose last 50 um cylinder ends at arc 58.0)]
Needs in each case dir: analysis.json, log.simpleFoam, system/controlDict, postProcessing monitors, sections_<mode>.csv/.json, wss_<mode>.csv/.json (mode lesion80 / baseline_ref),
zerod_reference.json, and for design 5c(e) sections_<mode>_tprev.csv + sections_<mode>_tprev.json ({"time": <previous write time>}).
converged_pair (design 5c) = case_validity() of both cases: strict verdict (analyze_solve.main(case, strict=True), read-only) and stored verdict CONVERGED; log FINISHED;
freshness tied to the final solver iteration F (last 'Time =' of log.simpleFoam): analysis.json last_iteration/log_last_iteration, sections/wss json 'time' and the largest
numeric time directory all == F, and every monitor file has the same rows/time columns ending at F; plane stability: p/P_ao at 18.5/23.5/29.5/40.0 mm < 0.1 % between F and
THE previous write time the rule selects (earliest retained write >= 100 iterations before F, else >= 20; retained writes from controlDict writeInterval/purgeWrite; else NOT ASSESSED).
Otherwise every single-valued result goes under 'values_UNCONVERGED_do_not_quote' (never printed), only the last-500 bands (min-max, outlets and inlet) are quotable, compare_lesion's
printout is suppressed and its outputs are named <out>_compare_UNCONVERGED_do_not_quote.json/.pdf. Old outputs of the prefix are deleted first. compare_lesion writes under
<out>_compare_TMP.*, renamed at once to <out>_compare_UNFINISHED.*; the result json is staged as <out>_UNFINISHED; only at the end all are renamed to the final names (an exception leaves *_UNFINISHED); the companion json carries
'hyp_compare_status' (pair status, 5b label, tube end).
HYP4 finding 2 (attempt Fable-1): spatial coverage counts FINITE samples only (finite_extent): the analysed window end is the last finite (ok) station, an extent is said to END
inside its window only when no station between the last reversed station and the window end is missing (else NOT ASSESSABLE, flag recirculation_extent_not_assessable, and the
label 'mesh-supported' cannot be produced), and reattachment_wss's own missing_stations_in_window / 'no resolved separation' claims are propagated (wss_outcome_assessment).
HYP4 finding 3: the validity, 5b and not-assessable statements are computed BEFORE compare_lesion.main runs (they come from the csv/json inputs, not from its output) and are drawn
in red on the companion pdf (banner) and stored in the companion json; no file exists under an ordinary name until every wrapper computation has succeeded."""
import sys, os, json, re, io, contextlib
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from zerod_ffr import P_AORTA, MMHG
import compare_lesion as CL
import analyze_solve as AS

BASE = os.path.dirname(os.path.abspath(__file__))
REST = dict(les=f"{BASE}/solve_lesion80", ref=f"{BASE}/solve_baseline_ref", res=f"{BASE}/lesion80_results.json")

from lesion_profile import PR as _PR
STATIONS = (_PR["S_UP"], _PR["S_C"], _PR["S_DOWN"], round(_PR["S_C"] + 16.5, 2))   # design 5a / 5c(e); default profile lesion80 = (18.5, 23.5, 29.5, 40.0), unchanged
S_THROAT = STATIONS[1]   # profile throat S_C (23.5 under lesion80): start of the coverage requirement for 'no reversed station' claims (finding 2 (iii))
NUMERIC = re.compile(r"^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$")

def is_true(v):
    """ok column value -> True only for a real boolean True (bool / numpy bool / the string 'True'); NaN, blanks and 'False' are not ok."""
    return (isinstance(v, (bool, np.bool_)) and bool(v)) or (isinstance(v, str) and v.strip() == "True")

def station_value(df, col, s):
    """(value, None) for exactly one row at s with ok True (if an 'ok' column exists) and a finite value; else (None, reason). Never substitutes a neighbour."""
    if col not in df.columns: return None, f"no column {col}"
    d = df[(df.s_mm - s).abs() < 1e-6]
    if len(d) != 1: return None, f"{len(d)} rows at s={s} mm for {col}"
    row = d.iloc[0]
    if "ok" in df.columns and not is_true(row["ok"]): return None, f"section at s={s} mm has ok={row['ok']} for {col}"
    try: v = float(row[col])
    except (TypeError, ValueError): v = float("nan")
    if not np.isfinite(v): return None, f"non-finite {col}={row[col]} at s={s} mm"
    return v, None

def at(df, col, s):
    v, why = station_value(df, col, s)
    if why: raise SystemExit(f"no valid section at s={s} mm for {col} ({why}): refusing to substitute a neighbouring station")
    return v

def last_log_time(case):
    it = re.findall(r"^Time = (\d+)", open(f"{case}/log.simpleFoam").read(), re.M)
    return int(it[-1]) if it else None

def latest_time_dir(case):
    t = [float(n) for n in os.listdir(case) if NUMERIC.match(n) and os.path.isdir(f"{case}/{n}")]
    return max(t) if t else None

def monitor_equality(case, final_it):
    """Final-report check for a FINISHED log (read directly; analyze_solve's strict mode tolerates a one-row spread for live cases): every monitor file
    (inletFlux, inletPressure, <patch>Flux, <patch>Pressure) has the same number of rows and identical time columns, and its last time is the final iteration."""
    try: outlets = json.load(open(f"{case}/zerod_reference.json"))["outlets"]
    except (OSError, ValueError, KeyError) as e: return [f"zerod_reference.json unreadable ({type(e).__name__}): monitor list unknown"]
    names = (["inletFlux"] if os.path.exists(f"{case}/postProcessing/inletFlux") else []) + ["inletPressure"] + [f"{p}{k}" for p in outlets for k in ("Flux", "Pressure")]
    T, bad = {}, []
    for nm in names:
        try: T[nm] = np.atleast_2d(np.loadtxt(f"{case}/postProcessing/{nm}/0/surfaceFieldValue.dat", comments="#"))[:, 0]
        except (OSError, ValueError, IndexError) as e: bad.append(f"monitor {nm} unreadable ({type(e).__name__})")
    if bad or not T: return bad or ["no monitor files"]
    rows = {nm: len(t) for nm, t in T.items()}
    if len(set(rows.values())) != 1: bad.append(f"monitor row counts differ {rows}")
    ref_nm = "inletPressure" if "inletPressure" in T else next(iter(T))
    diff = [nm for nm, t in T.items() if len(t) != len(T[ref_nm]) or not np.array_equal(t, T[ref_nm])]
    if diff: bad.append(f"monitor time columns differ from {ref_nm}: {diff}")
    last = {nm: float(t[-1]) for nm, t in T.items() if len(t)}
    wrong = {nm: v for nm, v in last.items() if final_it is None or v != final_it}
    if wrong: bad.append(f"last monitor time != final iteration {final_it}: {wrong}")
    return bad

def freshness(tag, case, mode, A, S_A):
    """Design 5c(b)-(d), tied to the FINAL SOLVER ITERATION F = last 'Time =' of log.simpleFoam: analysis.json last_iteration and log_last_iteration,
    sections/wss json 'time' and the largest numeric time directory must all equal F; the log must be finished; and (finished log) every monitor file has
    identical rows/time columns ending at F. Returns (reason strings (empty = fresh), F)."""
    bad = []
    try: lt = last_log_time(case)
    except OSError as e: lt = None; bad.append(f"{tag}: log.simpleFoam unreadable ({e})")
    if lt is None and not bad: bad.append(f"{tag}: no 'Time =' line in log.simpleFoam: final iteration unknown")
    for k in ("last_iteration", "log_last_iteration"):
        if lt is None or A.get(k) != lt: bad.append(f"{tag}: analysis.json {k}={A.get(k)} != final iteration (last log 'Time =') {lt}")
    td = latest_time_dir(case)
    if lt is None or td is None or td != lt: bad.append(f"{tag}: largest numeric time directory {td} != final iteration {lt} (reconstructed fields are not the final ones)")
    for nm in (f"sections_{mode}.json", f"wss_{mode}.json"):
        try: t = json.load(open(f"{case}/{nm}")).get("time")
        except (OSError, ValueError, AttributeError) as e: bad.append(f"{tag}: {nm} unreadable ({type(e).__name__})"); continue
        try: t = float(t)
        except (TypeError, ValueError): pass
        if lt is None or t != lt: bad.append(f"{tag}: {nm} time={t} != final iteration {lt}" + (f" (latest time directory {td})" if td is not None else ""))
    if S_A is None: bad.append(f"{tag}: strict analysis not evaluated, log completion unknown")
    elif not S_A["strict"].get("log_finished"): bad.append(f"{tag}: log.simpleFoam not finished (no 'End' + 'Finalising parallel run'): a live case is not a final result")
    else: bad += [f"{tag}: {m}" for m in monitor_equality(case, lt)]
    return bad, lt

def top_level_entry(txt, key):
    """Unindented '<key> <value>;' of an OpenFOAM dictionary (function-object sub-dictionaries are indented and have their own writeInterval)."""
    m = re.findall(rf"^{key}\s+([^;\s]+)\s*;", txt, re.M)
    return m[-1] if m else None

def retained_write_times(F, write_interval, purge_write):
    """Write times kept on disk at final iteration F (writeControl timeStep): the multiples of writeInterval up to F plus F itself (the stop writes F),
    the last purgeWrite of them (purgeWrite 0 keeps all)."""
    w = sorted(set(list(range(write_interval, F + 1, write_interval)) + [F]))
    return w[-purge_write:] if purge_write > 0 else w

def expected_prev_time(F, write_interval, purge_write):
    """Design 5c(e): the earliest retained write time >= 100 iterations before F, else the earliest >= 20 before F; (time, rule) or (None, reason)."""
    earlier = [t for t in retained_write_times(F, write_interval, purge_write) if t < F]
    for gap in (100, 20):
        c = [t for t in earlier if F - t >= gap]
        if c: return min(c), f">={gap}"
    return None, f"no retained write time >= 20 iterations before {F} (retained earlier: {earlier})"

def plane_stability(case, mode, final_it=None):
    """Design 5c(e): p/P_ao at the four stations from sections_<mode>.csv (latest write) vs sections_<mode>_tprev.csv, whose time (sections_<mode>_tprev.json)
    must be THE previous write time the rule selects from system/controlDict (writeInterval, purgeWrite) and the final iteration."""
    r = dict(status="NOT ASSESSED", reason=None, time_new=None, time_prev=None, gap_iterations=None, rel_change={}, expected_time_prev=None, rule=None, final_iteration=final_it)
    try:
        if final_it is None: final_it = r["final_iteration"] = last_log_time(case)
        cd = open(f"{case}/system/controlDict").read()
        wc, wi, pw = top_level_entry(cd, "writeControl"), top_level_entry(cd, "writeInterval"), top_level_entry(cd, "purgeWrite")
        if wc != "timeStep": raise ValueError(f"writeControl {wc!r} is not timeStep: write times cannot be derived")
        wi, pw = int(wi), int(pw if pw is not None else 0)
        if final_it is None or wi <= 0: raise ValueError(f"final iteration {final_it} / writeInterval {wi} unusable")
    except (OSError, ValueError, TypeError) as e:
        r["reason"] = f"previous write time cannot be derived ({type(e).__name__}: {e})"; return r
    exp, rule = expected_prev_time(final_it, wi, pw)
    r.update(expected_time_prev=exp, write_interval=wi, purge_write=pw, retained_write_times=retained_write_times(final_it, wi, pw))
    if exp is None: r["reason"] = rule; return r
    r["rule"] = rule
    try:
        t_new = float(json.load(open(f"{case}/sections_{mode}.json"))["time"]); t_prev = float(json.load(open(f"{case}/sections_{mode}_tprev.json"))["time"])
        S_new = pd.read_csv(f"{case}/sections_{mode}.csv"); S_prev = pd.read_csv(f"{case}/sections_{mode}_tprev.csv")
    except (OSError, ValueError, KeyError, TypeError) as e:
        r["reason"] = f"previous-write section files missing/unreadable ({type(e).__name__}: {e}); expected previous write time {exp} (rule {rule})"; return r
    r.update(time_new=t_new, time_prev=t_prev, gap_iterations=t_new - t_prev)   # write-time directory names are iteration numbers
    if t_new != final_it: r["reason"] = f"latest sections time {t_new:g} != final iteration {final_it}"; return r
    if t_prev != exp: r["reason"] = f"previous-write sections time {t_prev:g} != expected {exp} (rule {rule}; retained {r['retained_write_times']})"; return r
    if not any(NUMERIC.match(n) and os.path.isdir(f"{case}/{n}") and float(n) == exp for n in os.listdir(case)):   # HYP4 finding 1: retention is inferred, the write must exist
        r["reason"] = (f"previous write time {exp:g} (rule {rule}) is not reconstructed on disk: no time directory {case}/{exp:g} (numeric directories: "
                       f"{sorted(float(n) for n in os.listdir(case) if NUMERIC.match(n) and os.path.isdir(f'{case}/{n}'))}); the previous-write sections cannot be verified"); return r
    for s in STATIONS:
        (a, wa), (b, wb) = station_value(S_new, "p_over_Pao", s), station_value(S_prev, "p_over_Pao", s)
        if wa or wb: r["reason"] = f"invalid station: {'latest: ' + wa if wa else ''}{' ' if wa and wb else ''}{'previous: ' + wb if wb else ''}"; return r
        r["rel_change"][s] = abs(a / b - 1)
    r["gap_ge_100"] = bool(t_new - t_prev >= 100)
    r["status"] = "STABLE" if all(v < 1e-3 for v in r["rel_change"].values()) else "NOT STABLE"
    if r["status"] != "STABLE": r["reason"] = "|p_new/p_prev - 1| >= 1e-3 at " + str([s for s, v in r["rel_change"].items() if v >= 1e-3])
    return r

def case_validity(case_dir, mode, need_plane_stability, tag=None):
    """Shared validity gate (hyp_compare and e60_compare): strict verdict (analyze_solve.main(case, strict=True), read-only) CONVERGED, stored analysis.json
    verdict CONVERGED, log finished, freshness tied to the final iteration + monitor equality (freshness()), and, if need_plane_stability, design 5c(e)."""
    tag = tag or os.path.basename(os.path.normpath(case_dir))
    v = dict(case=case_dir, tag=tag, mode=mode, reasons=[], A=None, strict=None)
    try: v["A"] = A = json.load(open(f"{case_dir}/analysis.json"))
    except (OSError, ValueError) as e: A = None; v["reasons"].append(f"{tag}: analysis.json unreadable ({type(e).__name__}: {e})")
    v["stored_verdict"] = A.get("verdict") if isinstance(A, dict) else None
    if v["stored_verdict"] != "CONVERGED": v["reasons"].append(f"{tag}: stored analysis.json verdict {v['stored_verdict']} (must be CONVERGED)")
    with contextlib.redirect_stdout(io.StringIO()): v["strict"], v["strict_verdict"], v["strict_failed_checks"] = strict_verdict(case_dir)
    if v["strict_verdict"] != "CONVERGED": v["reasons"].append(f"{tag}: strict verdict {v['strict_verdict']} (failed: {v['strict_failed_checks']})")
    v["log_finished"] = bool(v["strict"] and v["strict"]["strict"].get("log_finished"))
    v["freshness_failures"], v["final_iteration"] = freshness(tag, case_dir, mode, A if isinstance(A, dict) else {}, v["strict"])
    v["reasons"] += v["freshness_failures"]
    v["plane_stability_required"] = bool(need_plane_stability)
    v["plane"] = plane_stability(case_dir, mode, v["final_iteration"]) if need_plane_stability else None
    if need_plane_stability and v["plane"]["status"] != "STABLE": v["reasons"].append(f"{tag}: measurement-plane stability {v['plane']['status']} ({v['plane']['reason']})")
    v["valid"] = not v["reasons"]
    return v

def finite_extent(s, v, thr, s_lo, gap_mm=2.0):
    """HYP4 finding 2: coverage = FINITE samples only. s/v: coordinates and values of EVERY row of a csv (a missing sample is NaN: reattachment_wss writes a NaN row for a
    station with < 10 faces, an ok=False section counts as missing); thr: the frozen reversed threshold (sections 0.01, wall 0.05; design 5b/5c, unchanged).
    window_end_mm = last FINITE station; last_reversed_mm = last finite station with v >= thr. The extent is claimed to END inside the window ('ends inside',
    end_established) only if every station in (last_reversed, window_end] is finite; a last reversed station within gap_mm of the window end 'reaches' it (extent
    beyond it NOT ASSESSABLE); a missing station after the last reversed one - or, with no reversed station at all, between s_lo and the window end - makes the
    extent NOT ASSESSABLE (gap_free False). Only end_established allows a mesh-support claim about the tail."""
    s = np.asarray(s, float); v = np.asarray(v, float); fin = np.isfinite(v)
    r = dict(last_reversed_mm=None, window_end_mm=None, threshold=thr, s_lo_mm=s_lo, n_finite=int(fin.sum()), n_missing=int((~fin).sum()), missing_stations=sorted(float(x) for x in s[~fin]),
             missing_stations_in_window=[], missing_stations_after_last_reversed=[], reaches_window_end=False, gap_free=False, end_established=False, status="NOT ASSESSABLE (no finite station)")
    if not fin.any(): return r
    win = float(s[fin].max()); r["window_end_mm"] = win
    r["missing_stations_in_window"] = sorted(float(x) for x in s[~fin & (s >= s_lo) & (s <= win)])
    rev = fin & (v >= thr)
    if not rev.any():
        if r["missing_stations_in_window"]: r["status"] = f"NOT ASSESSABLE (missing stations between {s_lo:g} mm and the window end {win:g} mm: {r['missing_stations_in_window']})"
        else: r.update(gap_free=True, end_established=True, status=f"no reversed station (finite coverage from {s_lo:g} mm to the window end {win:g} mm)")
        return r
    last = float(s[rev].max()); r["last_reversed_mm"] = last
    r["missing_stations_after_last_reversed"] = sorted(float(x) for x in s[~fin & (s > last) & (s <= win)])
    r["missing_stations_beyond_window"] = sorted(float(x) for x in s[~fin & (s > win)])   # csv stations past the last finite one (they truncate the window)
    r["reaches_window_end"] = bool(last >= win - gap_mm)
    trunc = f"; missing stations beyond it: {r['missing_stations_beyond_window']}" if r["missing_stations_beyond_window"] else ""
    if r["missing_stations_after_last_reversed"]: r["status"] = f"NOT ASSESSABLE (missing stations after the last reversed station: {r['missing_stations_after_last_reversed']})"
    elif r["reaches_window_end"]: r.update(gap_free=True, status=f"reaches the analysed window end ({win:g} mm{trunc}): extent beyond {win:g} mm NOT ASSESSABLE")
    else: r.update(gap_free=True, end_established=True, status=f"ends inside the analysed window (to {win:g} mm)")
    return r

def recirculation_extent(S_l, W_l, tube_end_mm, s_lo=None):
    """Design 5b/5c (frozen, unchanged): last section with frac_reversed_area >= 0.01 (ok=True only) and last wall station with f_rev >= 0.05 (WSS csv 15-45 mm, no junction
    censoring); flag = either > tube_end - 2 mm -> label NOT MESH-SUPPORTED. HYP4 finding 2: coverage counts FINITE samples only (finite_extent, throat s_lo = S_THROAT):
    the window ends are the last finite (ok) stations; an extent ENDS inside its window only if no station between its last reversed station and the window end is
    missing, else NOT ASSESSABLE (not_assessable[k]); the label 'mesh-supported' is produced only when both extents end inside their windows (extent_end_established)."""
    s_lo = S_THROAT if s_lo is None else s_lo
    okv = S_l.ok.map(is_true).values if "ok" in S_l.columns else np.ones(len(S_l), bool)
    v_sec = np.where(okv, pd.to_numeric(S_l.frac_reversed_area, errors="coerce").astype(float).values, np.nan)
    sec = finite_extent(S_l.s_mm.values, v_sec, 0.01, s_lo)
    wal = finite_extent(W_l.s_mm.values, pd.to_numeric(W_l.f_rev, errors="coerce").astype(float).values, 0.05, s_lo)
    s_sec, s_wal = sec["last_reversed_mm"], wal["last_reversed_mm"]
    lim = tube_end_mm - 2.0; flag = any(v is not None and v > lim for v in (s_sec, s_wal))
    win_sec, win_wal = sec["window_end_mm"], wal["window_end_mm"]
    reach = dict(section=bool(sec["reaches_window_end"]), wall=bool(wal["reaches_window_end"]))
    not_ass = dict(section=bool(not sec["end_established"]), wall=bool(not wal["end_established"]))
    established = bool(sec["end_established"] and wal["end_established"])
    remark = (f"reversed flow ends inside the analysed windows (sections to {win_sec} mm, WSS to {win_wal} mm)" if established
              else "; ".join(f"{k} reversed flow: {d['status']}" for k, d in (("section", sec), ("wall", wal)) if not d["end_established"]))
    label = ("NOT MESH-SUPPORTED (tail in coarse cells)" if flag else "mesh-supported (tail inside the fine tube)" if established
             else f"NOT ASSESSABLE (extent end not established: {remark})")
    wfin = np.isfinite(pd.to_numeric(W_l.f_rev, errors="coerce").astype(float).values)
    return dict(s_last_rev_section_mm=s_sec, s_last_rev_wall_mm=s_wal, tube_end_mm=tube_end_mm, limit_mm=lim, wss_csv_range_mm=[float(W_l.s_mm.min()), float(W_l.s_mm.max())],
                wss_finite_range_mm=[float(W_l.s_mm[wfin].min()), float(W_l.s_mm[wfin].max())] if wfin.any() else None,
                section_window_end_mm=win_sec, wss_window_end_mm=win_wal, reversed_flow_reaches_analysis_window=reach, not_assessable=not_ass, extent_end_established=established,
                coverage=dict(section=sec, wall=wal), window_remark=remark, label=label,
                rules="frozen: sections frac_reversed_area >= 0.01 (ok=True, finite), wall f_rev >= 0.05 (finite); NOT MESH-SUPPORTED if either > tube_end - 2 mm; "
                      "coverage = finite samples; 'ends inside' needs no missing station after the last reversed station (HYP4 finding 2)"), flag

def wss_outcome_assessment(W, Wj, s_lo=None):
    """HYP4 finding 2 (iii): reattachment_wss's outcome (wss_<mode>.json) is repeated only with complete coverage: its own missing_stations_in_window (throat to junction)
    must be 0 and every WSS station of the csv from the throat (s_lo = S_THROAT) to the analysed (finite) window end must be finite. Otherwise a 'no resolved separation'
    claim becomes 'NOT ASSESSABLE (missing stations ...)' (an absent reversal cannot be established with missing samples) and any other outcome keeps its finite
    evidence (onset) but carries the missing-station caveat (not_assessable True: a missing station can hide a sustained recovery)."""
    s_lo = S_THROAT if s_lo is None else s_lo
    s = np.asarray(W.s_mm, float); f = pd.to_numeric(W.f_rev, errors="coerce").astype(float).values; fin = np.isfinite(f)
    win = float(s[fin].max()) if fin.any() else None
    missing = sorted(float(x) for x in (s[~fin & (s >= s_lo) & (s <= win)] if win is not None else s))
    n_own = Wj.get("missing_stations_in_window") if isinstance(Wj, dict) else None; outcome = Wj.get("outcome") if isinstance(Wj, dict) else None
    complete = bool(not missing and n_own == 0)
    why = f"missing stations: WSS csv {missing} between the throat {s_lo:g} mm and the window end {win} mm; reattachment_wss missing_stations_in_window={n_own}"
    if complete: assessed = outcome
    elif isinstance(outcome, str) and outcome.startswith("no resolved separation"): assessed = f"NOT ASSESSABLE ({why}); reattachment_wss said: {outcome}"
    else: assessed = f"{outcome} [NOT FULLY ASSESSABLE: {why}]"
    return dict(outcome_reattachment_wss=outcome, missing_stations_in_window_reattachment_wss=n_own, missing_wss_stations_throat_to_window_end=missing, wss_window_end_mm=win,
                coverage_complete=complete, not_assessable=bool(not complete), outcome_assessed=assessed)

def banner_text(converged, ext, wss_ass, width=125):
    """Red suptitle of the companion pdf (HYP4 finding 3): pair validity, the 5b mesh-support label and every not-assessable statement; also stored in hyp_compare_status."""
    import textwrap
    lines = ["VALID PAIR" if converged else "NOT A VALID PAIR: DO NOT QUOTE", f"5b: {ext['label']} (tube end {ext['tube_end_mm']:g} mm)"]
    na = [f"{k} extent: {ext['coverage'][k]['status']}" for k in ("section", "wall") if ext["not_assessable"][k]] + \
         [f"WSS outcome ({k}): {a['outcome_assessed']}" for k, a in wss_ass.items() if a["not_assessable"]]
    if na: lines.append("NOT ASSESSABLE: " + " | ".join(na))
    return "\n".join("\n".join(textwrap.wrap(l, width)) for l in lines)

def category(d3, d_area, d_edt):
    """Frozen rules, hyperaemia_design.md section 5a."""
    if d_area * d_edt < 0: return "not categorised (0D-area and 0D-EDT changes differ in sign)"
    if d3 * d_area < 0: return "(iv) opposite sign"
    a3, aa, ae = abs(d3), abs(d_area), abs(d_edt)
    if aa > ae and ae < a3 < aa: return "not categorised (|d_area| > |d_EDT|: (i) and (iii) overlap)"   # not expected (the area variant is the milder lesion); flagged instead of picking one
    if a3 < aa: return "(i) smaller than 0D-area"
    if a3 <= ae: return "(ii) between 0D-area and 0D-EDT"
    return "(iii) beyond 0D-EDT"

def strict_verdict(case):
    """Strict analysis (read-only). If it cannot be evaluated the case counts as not converged and the reason is reported."""
    try:
        r = AS.main(case, strict=True)
        return r, r["verdict"], [k for k, v in r["checks"].items() if not v]
    except Exception as e:
        return None, f"STRICT_NOT_EVALUATED ({type(e).__name__}: {e})", None

def loss_scaling(dp_mmHg_rest, q_rest_mls, dp_mmHg_hyp, q_hyp_mls):
    """DeltaP = a Q + b Q^2 from two points (SI units); descriptive only."""
    q1, q2 = q_rest_mls * 1e-6, q_hyp_mls * 1e-6; d1, d2 = dp_mmHg_rest * MMHG, dp_mmHg_hyp * MMHG
    A = np.array([[q1, q1 ** 2], [q2, q2 ** 2]]); a, b = np.linalg.solve(A, [d1, d2])
    return dict(a_PaS_per_m3=float(a), b_Pa_s2_per_m6=float(b), dP_over_Q2_rest=float(d1 / q1 ** 2), dP_over_Q2_hyp=float(d2 / q2 ** 2),
                quadratic_share_at_hyp=float(b * q2 ** 2 / d2))

def output_names(out):
    """Every output this prefix can produce (design 5a naming), deleted at the start so that a failed or unconverged rerun never leaves an older ordinary output behind."""
    return [out, out + "_UNFINISHED"] + [f"{out}_compare{x}.{e}" for x in ("", "_UNCONVERGED_do_not_quote", "_TMP", "_UNFINISHED") for e in ("json", "pdf")]

def main(les, ref, out, tube_end_mm=36.0):
    for f in output_names(out):
        if os.path.lexists(f): os.remove(f)
    cv_l, cv_r = case_validity(les, "lesion80", True, tag="lesion"), case_validity(ref, "baseline_ref", True, tag="reference")
    for cv in (cv_l, cv_r):
        if cv["A"] is None: raise SystemExit(f"{cv['case']}: analysis.json unreadable: no comparison ({cv['reasons']})")
    A_l, A_r, S_A_l, S_A_r = cv_l["A"], cv_r["A"], cv_l["strict"], cv_r["strict"]
    sv_l, sv_r, sf_l, sf_r = cv_l["strict_verdict"], cv_r["strict_verdict"], cv_l["strict_failed_checks"], cv_r["strict_failed_checks"]
    fresh_fail = cv_l["freshness_failures"] + cv_r["freshness_failures"]
    plane = dict(lesion=cv_l["plane"], reference=cv_r["plane"])
    converged = bool(cv_l["valid"] and cv_r["valid"])   # strict + stored verdicts CONVERGED, finished, fresh at the final iteration, monitors equal, planes STABLE
    # HYP4 finding 3(c): the 5b / coverage statements come from the csv/json inputs and are computed BEFORE compare_lesion runs so that its pdf can carry them
    S_l = pd.read_csv(f"{les}/sections_lesion80.csv"); S_r = pd.read_csv(f"{ref}/sections_baseline_ref.csv")
    W_l = pd.read_csv(f"{les}/wss_lesion80.csv"); W_r = pd.read_csv(f"{ref}/wss_baseline_ref.csv")
    Wj_l = json.load(open(f"{les}/wss_lesion80.json")); Wj_r = json.load(open(f"{ref}/wss_baseline_ref.json"))
    ext, not_supported = recirculation_extent(S_l, W_l, tube_end_mm)
    wss_ass = dict(lesion=wss_outcome_assessment(W_l, Wj_l), reference=wss_outcome_assessment(W_r, Wj_r))
    banner = banner_text(converged, ext, wss_ass)
    tmp, unf = out + "_compare_TMP", out + "_compare_UNFINISHED"   # compare_lesion writes single values: never under an ordinary name until the pair verdict is final
    try:
        if converged: CL.main(les, ref, tmp, banner=banner)
        else:   # compare_lesion prints single values: captured, not shown
            with contextlib.redirect_stdout(io.StringIO()): CL.main(les, ref, tmp, banner=banner)
            print("=" * 70 + "\nPAIR NOT CONVERGED: compare_lesion output suppressed (single values are not to be quoted)\n" + "=" * 70)
    finally:
        for e in ("json", "pdf"):
            if os.path.exists(f"{tmp}.{e}"): os.replace(f"{tmp}.{e}", f"{unf}.{e}")
    fin = out + ("_compare" if converged else "_compare_UNCONVERGED_do_not_quote")
    cmp_json, cmp_pdf = fin + ".json", fin + ".pdf"
    C = json.load(open(unf + ".json"))
    Z = json.load(open(f"{les}/zerod_reference.json")); Zr = json.load(open(f"{ref}/zerod_reference.json"))
    V = {}
    # 1 flow categories
    V["flow_categories"] = {p: dict(d3D=d["delta_3D_pct"], d0D_edt=d["delta_0D_edt_pct"], d0D_area=d["delta_0D_area_pct"],
                                    category=category(d["delta_3D_pct"], d["delta_0D_area_pct"], d["delta_0D_edt_pct"])) for p, d in C["flow"].items()}
    # 2 FFR-like ratio at 40.0 mm
    cols = dict(lesion_3D=(S_l, "p_over_Pao"), ref_3D=(S_r, "p_over_Pao"), lesion_0D_edt=(S_l, "p0D_edt_over_Pao"), lesion_0D_area=(S_l, "p0D_area_over_Pao"), healthy_0D=(S_r, "p0D_healthy_over_Pao"))
    V["p_over_Pao_at_40mm"] = {k: at(df, c, 40.0) for k, (df, c) in cols.items()}
    V["p_over_Pao_at_throat_23_5"] = {k: at(df, c, 23.5) for k, (df, c) in cols.items()}
    # 3 loss scaling vs the resting pair
    R = json.load(open(REST["res"]))
    dp_rest = R["pressure"]["prox_to_distal"]["added_by_lesion_3D_mmHg"]; dp_hyp = C["pressure"]["prox_to_distal"]["added_by_lesion_3D_mmHg"]
    q_rest, q_hyp = R["throat"]["Q_mls"], C["throat"]["Q_mls"]
    K_win = [k for n, k in zip(Z["K_nodes"], Z["K_values"]) if n in set(Z["lesion_nodes"])]
    V["loss_scaling_18.5_to_29.5"] = dict(dP_rest_mmHg=dp_rest, Q_throat_rest_mls=q_rest, dP_hyp_mmHg=dp_hyp, Q_throat_hyp_mls=q_hyp, **loss_scaling(dp_rest, q_rest, dp_hyp, q_hyp),
                                          K_0D_nodes=Z["K_nodes"], K_0D_values=Z["K_values"],
                                          K_total_Pa_s2_per_m6=float(sum(Z["K_values"])), K_lesion_window_Pa_s2_per_m6=float(sum(K_win)),
                                          K_units="b and K in Pa s^2/m^6 (DeltaP = K Q^2, Q in m^3/s); side by side, no tolerance",
                                          K_note="K_total sums every K>0 node of the lesion case's 0D tree, including native narrowings outside the lesion window that the healthy tree has too; "
                                                 "K_lesion_window sums only the K_nodes inside lesion_nodes",
                                          note="two points solve a and b exactly: descriptive, not a test of the quadratic form")
    # 4-6 throat, Re, healthy reference flow
    V["throat"] = C["throat"]; V["wss"] = dict(C["wss"]); V["reversed_axial_velocity_sections"] = dict(C["reversed_axial_velocity_sections"])
    V["recirculation_extent_5b"] = ext
    V["wss_outcome_assessment"] = wss_ass   # finding 2 (iii): reattachment_wss's outcomes with their coverage (NOT ASSESSABLE when stations are missing)
    if not_supported:   # design 5b: the recirculation-extent results carry the label
        V["wss"]["label_5b"] = V["reversed_axial_velocity_sections"]["label_5b"] = ext["label"]
    elif not ext["extent_end_established"]:   # finding 2: a not-assessable extent carries its statement too (never the 'mesh-supported' label)
        V["wss"]["assessment_5b"] = V["reversed_axial_velocity_sections"]["assessment_5b"] = ext["label"]
    V["healthy_reference"] = dict(total_3D_mls=A_r["sum_outlets_mls"], Q_demand_mls=Zr["Q_demand_mls"], inflow_0D_mls=Zr["inflow_mls"],
                                  total_3D_vs_0D_pct=100 * (A_r["sum_outlets_mls"] / Zr["inflow_mls"] - 1),
                                  split_vs_0D_pct={p: 100 * (d["Q_mls"] / Zr["outlets"][p]["Q0_mls"] - 1) for p, d in A_r["outlets"].items()})
    V["flags"] = dict(Re_throat_gt_600=bool(C["throat"]["Re_area_eq"] > 600), recirculation_not_mesh_supported=bool(not_supported),
                      recirculation_extent_not_assessable=bool(not ext["extent_end_established"]), extent_not_assessable=ext["not_assessable"],
                      wss_outcome_not_assessable={k: a["not_assessable"] for k, a in wss_ass.items()})
    def bands(Ad, Sd):
        B = {p: dict(band200=d["band200_pct"], band500=d["band500_pct"]) for p, d in Ad["outlets"].items()}
        if Sd is not None:   # last-500 min-max from the strict analysis (the quotable result of an unconverged case), outlets and inlet
            for p, d in Sd["outlets"].items():
                B[p].update({k: d[k] for k in ("Q_min_last500_mls", "Q_max_last500_mls", "P_min_last500_Pa", "P_max_last500_Pa")})
            B["inlet"] = {k: Sd["strict"].get(k) for k in ("inlet_Q_min_last500_mls", "inlet_Q_max_last500_mls", "inlet_P_min_last500_Pa", "inlet_P_max_last500_Pa")}
        return B
    res = dict(converged_pair=converged, verdicts=dict(lesion=A_l["verdict"], reference=A_r["verdict"]),
               verdicts_strict=dict(lesion=sv_l, reference=sv_r), strict_failed_checks=dict(lesion=sf_l, reference=sf_r),
               log_finished=dict(lesion=cv_l["log_finished"], reference=cv_r["log_finished"]), final_iteration=dict(lesion=cv_l["final_iteration"], reference=cv_r["final_iteration"]),
               freshness_failures=fresh_fail, measurement_plane_stability=plane, validity_reasons=cv_l["reasons"] + cv_r["reasons"],
               compare_outputs=dict(json=cmp_json, pdf=cmp_pdf),
               bands=dict(lesion=bands(A_l, S_A_l), reference=bands(A_r, S_A_r)))
    res["values" if converged else "values_UNCONVERGED_do_not_quote"] = V
    status = dict(converged_pair=converged, verdicts_strict=res["verdicts_strict"], freshness_failures=fresh_fail,
                  recirculation_not_mesh_supported=bool(not_supported), recirculation_extent_not_assessable=bool(not ext["extent_end_established"]),
                  tube_end_mm=tube_end_mm, label_5b=ext["label"], window_remark=ext["window_remark"], extent_assessment={k: ext["coverage"][k]["status"] for k in ("section", "wall")},
                  wss_outcome_assessment={k: a["outcome_assessed"] for k, a in wss_ass.items()}, banner=banner,
                  measurement_plane_stability={k: (p["status"], p["reason"]) for k, p in plane.items()}, validity_reasons=res["validity_reasons"])
    C["hyp_compare_status"] = status   # the pair status and the 5b label travel with the companion file
    json.dump(C, open(unf + ".json", "w"), indent=1, default=float)
    json.dump(res, open(out + "_UNFINISHED", "w"), indent=1, default=float)   # HYP4 finding 3(b): every write is complete before any file gets an ordinary name
    os.replace(unf + ".json", cmp_json); os.replace(unf + ".pdf", cmp_pdf); os.replace(out + "_UNFINISHED", out)
    print("=" * 70); print("PAIR", "CONVERGED" if converged else "NOT CONVERGED -> single values are NOT to be quoted; use the bands", "default:", res["verdicts"], "strict:", res["verdicts_strict"],
                           "strict failed:", res["strict_failed_checks"])
    print("validity reasons:", res["validity_reasons"])
    print("measurement-plane stability:", {k: (p["status"], p["reason"], p["expected_time_prev"], p["rule"], p["gap_iterations"]) for k, p in plane.items()})
    print("compare outputs:", cmp_json, cmp_pdf)
    if converged:
        print("measurement-plane relative changes:", {k: p["rel_change"] for k, p in plane.items()})
        print("5b recirculation extent:", {k: v for k, v in V["recirculation_extent_5b"].items() if k != "coverage"}); print("WSS outcome assessment:", {k: a["outcome_assessed"] for k, a in wss_ass.items()})
        print(json.dumps(V["flow_categories"], indent=1)); print("p/Pao at 40 mm:", V["p_over_Pao_at_40mm"]); print("loss scaling:", V["loss_scaling_18.5_to_29.5"]); print("healthy ref:", V["healthy_reference"])
    else:   # no single value of an unconverged pair is printed; they exist only under the *_UNCONVERGED_do_not_quote names
        print("5b:", ext["label"], "|", ext["window_remark"], "| WSS outcomes:", {k: a["outcome_assessed"] for k, a in wss_ass.items()})
        print("quotable last-500 bands (min-max):", json.dumps(res["bands"], default=float))
    return res

if __name__ == "__main__":
    if len(sys.argv) < 4: raise SystemExit(__doc__)
    main(*sys.argv[1:4], tube_end_mm=float(sys.argv[4]) if len(sys.argv) > 4 else 36.0)
