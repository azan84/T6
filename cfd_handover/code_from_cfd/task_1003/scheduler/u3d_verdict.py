#!/usr/bin/env python3
"""Task B jet-state verdict (WORK-ORDER-2026-10-03 sec. 3): applies the rule of u3d_check/U3D_CHECK_DESIGN.md (rule of 2026-10-01 extended 2026-10-03) to the jet_offset.py output and the FFR of one re-run level,
and writes u3d_check/result_<L>.json (atomic: tmp + rename). Exit 0 only if every input parsed and passed its checks; any failure -> message on stderr, exit 1, no result file written.
usage: u3d_verdict.py result --level L --case DIR --jet FILE --ranks N --out FILE.json
       u3d_verdict.py set-status FILE.json DONE|FAILED [reason]        (the job's final status, written into the result file)
Rule (u3d_check/U3D_CHECK_DESIGN.md: rule of 2026-10-01 extended 2026-10-03; per level, the original FFR from returns/2026-09-26/U3D_sten70.csv):
 axisymmetric               SETTLED AND jet offset <= 10 um at x = 50 AND 56.5 mm AND |FFR_rerun - FFR_original| <= 1e-4  -> rule (a): the ORIGINAL level is verified on the same (axisymmetric) state
 deflected                  SETTLED AND jet offset >= 30 um at x = 50 or 56.5 mm -> rule (b); if |FFR_rerun - FFR_original| > 5e-4 the original was on the OTHER (axisymmetric) state; otherwise no inference (decision for the study lead)
 symmetric_but_FFR_differs  SETTLED AND offset <= 10 um at both stations but |dFFR| > 1e-4 -> rule (c): mesh-realisation effect, no conclusion on the original state
 inconclusive               anything else -> rule (d): UNSETTLED (always, whatever the offsets), or 10-30 um at either station
SETTLED (design v2.4, the criterion of u3d/u3d_analyse.py, constants SETTLE_DRIFT = 2e-4, SETTLE_BAND = 1e-4): >= 500 FFR rows, |mean(second 250 of the final 500) - mean(first 250)| <= 2e-4
and last-100 band (max - min) <= 1e-4.
FFR = areaAverage(p) at x = 56.5 mm / 11.3198 (kinematic inlet total pressure 11998.988 Pa / 1060 kg/m3; the constant P_AORTA_KIN of u3d/u3d_analyse.py, which produced the original values),
last-100-iteration mean and band (max - min). Checks: >= 100 rows, all finite, iterations strictly increasing, final iteration == endTime of system/controlDict == build_info.json endTime."""
import sys, os, re, json, math, time
import numpy as np
P_AORTA_KIN = 11.3198
FFR_ORIGINAL = {"S50": 0.793362, "S25A": 0.791103, "S25B": 0.791197, "S12A": 0.790308, "S12B": 0.790418}      # returns/2026-09-26/U3D_sten70.csv (16 ranks)
ORIGINAL_RANKS = 16
TOL_SAME, TOL_OTHER, SYM_UM, DEFL_UM = 1e-4, 5e-4, 10.0, 30.0
STATIONS = ("50.0", "56.5")
SETTLE_DRIFT, SETTLE_BAND = 2e-4, 1e-4      # copied from u3d/u3d_analyse.py (design v2.4); tests/test_verdict.py asserts equality of the constants and of settled() with u3d_analyse.level()
RULE_REF = "u3d_check/U3D_CHECK_DESIGN.md, rule of 2026-10-01 extended 2026-10-03"
EQUIVALENCE = ("The re-run uses {ranks} MPI ranks (scotch) and a re-generated mesh (same tooling and cell count, not bitwise identical); the original run used 16 ranks on the original mesh. "
               "Decomposition identity is NOT claimed. The evidence about the ORIGINAL run's state is the FFR reproduction within 1e-4 of the original value together with the jet state of the re-run.")

class Bad(Exception): pass

def end_time(case):
    m = re.findall(r"^\s*endTime\s+(\d+)\s*;", open(os.path.join(case, "system/controlDict")).read(), re.M)
    if len(m) != 1: raise Bad(f"controlDict: expected one integer endTime, found {m}")
    bi = json.load(open(os.path.join(case, "build_info.json")))
    if int(bi.get("endTime", -1)) != int(m[0]): raise Bad(f"endTime of controlDict ({m[0]}) != build_info.json ({bi.get('endTime')})")
    return int(m[0])

def ffr(case, endtime):
    d = os.path.join(case, "postProcessing/measurementP/0")
    files = sorted(os.listdir(d)) if os.path.isdir(d) else []
    if files != ["surfaceFieldValue.dat"]: raise Bad(f"{d}: expected exactly surfaceFieldValue.dat, found {files} (a restarted run writes surfaceFieldValue_<t>.dat)")
    rows = []
    for ln in open(os.path.join(d, files[0])):
        if ln.startswith("#") or not ln.strip(): continue
        f = ln.split()
        if len(f) != 2: raise Bad(f"measurementP: malformed row {ln.strip()!r}")
        rows.append((float(f[0]), float(f[1])))
    if len(rows) < 100: raise Bad(f"measurementP: {len(rows)} rows < 100")
    it = [r[0] for r in rows]; v = [r[1] / P_AORTA_KIN for r in rows]
    if not all(math.isfinite(x) for x in it + v): raise Bad("measurementP: non-finite value")
    if any(b <= a for a, b in zip(it, it[1:])): raise Bad("measurementP: iterations not strictly increasing")
    if it[-1] != endtime: raise Bad(f"measurementP: final iteration {it[-1]:g} != endTime {endtime}")
    ok, drift, band = settled(v); last = np.asarray(v, float)[-100:]
    return dict(FFR_last100_mean=float(last.mean()), FFR_last100_band=band, FFR_rows=len(rows), FFR_final_iteration=int(it[-1]), settled=ok, drift_last500=None if math.isnan(drift) else drift)

def settled(ffr):
    """SETTLED of design v2.4, the same expressions as u3d/u3d_analyse.py level(): returns (settled, drift over the final 500 (nan if < 500 rows), last-100 band)."""
    ffr = np.asarray(ffr, float); last = ffr[-100:]
    fin = ffr[-500:]; drift500 = float(abs(fin[250:].mean() - fin[:250].mean())) if len(fin) >= 500 else float("nan"); band100 = float(last.max() - last.min())
    return bool(len(fin) >= 500 and drift500 <= SETTLE_DRIFT and band100 <= SETTLE_BAND), drift500, band100

def jet(path, endtime):
    """jet_offset.py output (one line per case): '<case> t=<T> cells=<N> | x=30.0: 0.0 um (umin 0.009); ...' -> dict."""
    lines = [ln for ln in open(path).read().splitlines() if ln.strip()]
    if len(lines) != 1: raise Bad(f"{path}: expected one output line, found {len(lines)} (error output?)")
    m = re.match(r"^(\S+) t=(\S+) cells=(\d+) \| (.*)$", lines[0])
    if not m: raise Bad(f"{path}: unparseable line {lines[0][:200]!r}")
    if float(m.group(2)) != endtime: raise Bad(f"{path}: fields at t={m.group(2)} != endTime {endtime}")
    off = {}
    for part in m.group(4).split("; "):
        p = re.match(r"^x=(\d+\.\d): (\S+) um \(umin (\S+)\)$", part)
        if not p: raise Bad(f"{path}: unparseable station {part!r}")
        o, u = float(p.group(2)), float(p.group(3))
        if not (math.isfinite(o) and math.isfinite(u)): raise Bad(f"{path}: non-finite value at x={p.group(1)}")
        off[p.group(1)] = o
    for s in STATIONS:
        if s not in off: raise Bad(f"{path}: no station x={s} mm")
    return dict(jet_time=float(m.group(2)), cells=int(m.group(3)), jet_offset_um=off)

def classify(off50, off565, dffr, is_settled):
    """rule of 2026-10-01 extended 2026-10-03; returns (verdict, inference about the original run). An unsettled run is always inconclusive (rule (d))."""
    if not is_settled: return "inconclusive", "rule (d): the run is NOT SETTLED (design v2.4: >= 500 rows, final-500 drift <= 2e-4, last-100 band <= 1e-4); no conclusion on the state"
    if off50 <= SYM_UM and off565 <= SYM_UM:
        if abs(dffr) <= TOL_SAME: return "axisymmetric", "rule (a): the ORIGINAL level is verified on the axisymmetric state (same FFR within 1e-4 on the same state)"
        return "symmetric_but_FFR_differs", "rule (c): mesh-realisation effect larger than expected; no conclusion on the state of the original"
    if off50 >= DEFL_UM or off565 >= DEFL_UM:
        if abs(dffr) > TOL_OTHER: return "deflected", "rule (b): |dFFR| > 5e-4: the original was on the OTHER (axisymmetric) state; a symmetric-start re-run is a decision for the study lead"
        return "deflected", "rule (b): |dFFR| <= 5e-4: the rule makes no inference on the original state; decision for the study lead"
    return "inconclusive", "rule (d): offset between 10 and 30 um at a station (not deflected, not symmetric at both); report"

def write_json(path, d):
    tmp = f"{path}.tmp{os.getpid()}"
    with open(tmp, "w") as fh: json.dump(d, fh, indent=1); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)

def result(a):
    if a.level not in FFR_ORIGINAL: raise Bad(f"unknown level {a.level}")
    et = end_time(a.case); f = ffr(a.case, et); j = jet(a.jet, et)
    dffr = f["FFR_last100_mean"] - FFR_ORIGINAL[a.level]
    v, inf = classify(j["jet_offset_um"]["50.0"], j["jet_offset_um"]["56.5"], dffr, f["settled"])
    d = dict(level=a.level, verdict=v, inference=inf, jet_offset_um=j["jet_offset_um"], jet_offset_x50_um=j["jet_offset_um"]["50.0"], jet_offset_x56p5_um=j["jet_offset_um"]["56.5"],
             FFR_last100_mean=f["FFR_last100_mean"], FFR_last100_band=f["FFR_last100_band"], FFR_original=FFR_ORIGINAL[a.level], dFFR=dffr, FFR_rows=f["FFR_rows"], settled=f["settled"], drift_last500=f["drift_last500"], settle_drift_max=SETTLE_DRIFT, settle_band_max=SETTLE_BAND,
             iterations=f["FFR_final_iteration"], endTime=et, jet_fields_time=j["jet_time"], cells=j["cells"], mpi_ranks=a.ranks, original_mpi_ranks=ORIGINAL_RANKS,
             equivalence=EQUIVALENCE.format(ranks=a.ranks), rule=RULE_REF + ": " + __doc__.split("Rule (u3d_check")[1].split("FFR = ")[0].split("\n", 1)[1].strip(), rule_reference=RULE_REF,
             P_AORTA_KIN=P_AORTA_KIN, case=os.path.abspath(a.case), jet_offset_file=os.path.abspath(a.jet), written=time.strftime("%F %T"), job_status="PENDING")
    write_json(a.out, d)
    print(f"{a.level}: verdict {v} | offset x50 {d['jet_offset_x50_um']} um, x56.5 {d['jet_offset_x56p5_um']} um | FFR {d['FFR_last100_mean']:.6f} band {d['FFR_last100_band']:.1e} settled {d['settled']} "
          f"(original {d['FFR_original']}, dFFR {dffr:+.2e}) | it {d['iterations']} | {inf} [{RULE_REF}]\n{d['equivalence']}")

def set_status(path, st, reason):
    d = json.load(open(path)); d["job_status"] = st; d["failure_reason"] = reason if st == "FAILED" else None; d["status_written"] = time.strftime("%F %T"); write_json(path, d)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("result"); r.add_argument("--level", required=True); r.add_argument("--case", required=True); r.add_argument("--jet", required=True); r.add_argument("--ranks", type=int, required=True); r.add_argument("--out", required=True)
    s = sp.add_parser("set-status"); s.add_argument("file"); s.add_argument("status", choices=["DONE", "FAILED"]); s.add_argument("reason", nargs="?", default="")
    a = ap.parse_args()
    try:
        result(a) if a.cmd == "result" else set_status(a.file, a.status, a.reason)
    except (Bad, OSError, ValueError, KeyError) as e:
        sys.exit(f"u3d_verdict: FAILED: {type(e).__name__}: {e}")
