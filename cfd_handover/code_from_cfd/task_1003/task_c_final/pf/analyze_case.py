"""Strict analysis of a Task-3 case (Item 1 pf_* or scan-14 M1) WITHOUT importing the 0D twin: a constants-only stand-in for zerod_ffr is registered before analyze_solve.py is imported.
usage: analyze_case.py <case_dir> [--json out.json] [--strict-exit] [--require-finished] [--cached [--force]]
resistance mode: analyze_solve.py --strict verbatim (all checks count).
prescribed mode: analyze_solve's own 'all_bc_err_lt_0_1pct' compares the outlet-patch p with Pv + R_ref*Q for the REFERENCE resistance law (Item 1: the resistance solve the targets came from; M1: bc_A). With flows imposed
that number is a RESULT (how far the CFD pressure sits from the reference law), not a convergence criterion; it is therefore removed from the verdict EXPLICITLY (listed under dropped_checks with its per-outlet values,
never silently) and replaced by 'prescribed_flows_delivered' (last-100 mean of every outlet flux within 1e-6 relative of its target; the BC fixes the patch flux, so this is a BC/monitor sanity check).
Every other strict check (residuals < 1e-5, mass imbalance < 0.1 %, flux and pressure bands < 0.1 % over 200 iterations, monitors aligned, no fatal lines, finished log, ...) stays and decides the adjusted verdict.
Output json: the analyze_solve result plus  mode, verdict_analyze_solve, verdict (adjusted for prescribed mode), dropped_checks, prescribed_Q_check, p_bar_vs_reference_law_pct (prescribed), last-100 means/bands of every
outlet flux and p, and provenance (relative path, size_bytes, sha256 of log.simpleFoam and of every surfaceFieldValue.dat read here).
Per outlet, analyze_solve's keys Q0D_mls / Q0D_healthy_mls / Q_vs_0D_pct are written as Q_target_bcC_mls (zerod_reference stub 'Q0_mls' = the case's target flow: M1 bc_C; Item 1 the flow of the resistance solve the
targets came from; NOT a 0D prediction), Q_healthy_reference_mls (stub 'Q0_healthy_mls': never set by pf_common.write_case, hence null) and Q_vs_target_pct. Readers use outlet_value() (old keys accepted as fallback).
--strict-exit (opt-in): exit code 3 if the adjusted verdict is not CONVERGED or the log is not finished (default: exit 0, everything reported).
--require-finished: exit code 4 if the analysis completion flag strict.log_finished is false, whatever the verdict (post_case_generic.sh always passes it: the completion flag is enforced, convergence only reported).
Outlets LOST IN MESH (0-face patch, build_info outlets_lost_in_mesh; P5 272 out_396): not monitored and not in zerod_reference, so every check (BC error, flux/pressure bands, mass balance) runs over the outlets
that exist in the mesh only; the json lists them under outlets_lost_in_mesh (Q = 0, p N/A, flag OUTLET_LOST_IN_MESH) with the case's bc_bookkeeping (lost territory closed). A case built BEFORE this handling with a lost
outlet in zerod_reference is refused (rebuild it).
--cached: reuse <case>/analysis_pf.json (or --json) only if its provenance matches the files now on disk (load_or_run); --force: always regenerate."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pf_common as C
sys.modules["zerod_ffr"] = C.zerod_stub()        # BLINDING: never import the 0D twin in the scan-14 code path
PILOT_DEFAULT = "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot"
for _d in [d for d in (os.environ.get("P"), C.P, os.path.dirname(C.P), PILOT_DEFAULT) if d][::-1]:      # analyze_solve.py lives in the pilot root ($P; the installed pf/ parent; the taskC/ staging copy's parent)
    if os.path.exists(os.path.join(_d, "analyze_solve.py")): sys.path.insert(0, _d)
import analyze_solve as AS
assert getattr(sys.modules["zerod_ffr"], "IS_CONSTANTS_STUB", False) and not hasattr(sys.modules["zerod_ffr"], "Tree")

RENAMED = {"Q0D_mls": "Q_target_bcC_mls", "Q0D_healthy_mls": "Q_healthy_reference_mls", "Q_vs_0D_pct": "Q_vs_target_pct"}   # old analyze_solve key -> analysis_pf.json key
EXIT_NOT_CONVERGED = 3
EXIT_NOT_FINISHED = 4

def outlet_value(d, key):
    """per-outlet value by its NEW key, falling back to the old analyze_solve key (cached analysis_pf.json written before the rename)"""
    if key in d: return d[key]
    old = {v: k for k, v in RENAMED.items()}.get(key)
    return d[old] if old in d else d[key]

def provenance_files(case):
    """relative paths of every input file analyse() reads: log.simpleFoam + the surfaceFieldValue.dat of inletFlux (if present), inletPressure and each outlet Flux/Pressure (zerod_reference and build_info outlets)"""
    ref = json.load(open(f"{case}/zerod_reference.json")); info = json.load(open(f"{case}/build_info.json"))
    names = (["inletFlux"] if os.path.exists(f"{case}/postProcessing/inletFlux") else []) + ["inletPressure"]
    for p in list(ref["outlets"]) + [o["patch"] for o in C.live_outlets(info)]:
        for k in ("Flux", "Pressure"):
            if f"{p}{k}" not in names: names.append(f"{p}{k}")
    return ["log.simpleFoam"] + [f"postProcessing/{n}/0/surfaceFieldValue.dat" for n in names]

def file_stamp(case, rel):
    h = hashlib.sha256(); f = os.path.join(case, rel)
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return dict(path=rel, size_bytes=os.path.getsize(f), sha256=h.hexdigest())

def provenance(case):
    return dict(algorithm="sha256", files=[file_stamp(case, r) for r in provenance_files(case)])

def stale_reasons(case, a):
    """[] if the cached analysis a was written from exactly the files now on disk, else the reasons (which file changed); a json without provenance is stale"""
    pv = a.get("provenance")
    if not pv or not pv.get("files"): return ["no provenance in the cached analysis (written by an older analyze_case.py)"]
    old = {f["path"]: f for f in pv["files"]}; why = []
    for rel in provenance_files(case):
        if rel not in old: why.append(f"{rel}: not in the cached provenance"); continue
        if not os.path.exists(os.path.join(case, rel)): why.append(f"{rel}: missing now"); continue
        now = file_stamp(case, rel)
        if now["size_bytes"] != old[rel]["size_bytes"] or now["sha256"] != old[rel]["sha256"]:
            why.append(f"{rel}: changed (size {old[rel]['size_bytes']} -> {now['size_bytes']}, sha256 {old[rel]['sha256'][:12]} -> {now['sha256'][:12]})")
    why += [f"{rel}: in the cached provenance but no longer read" for rel in old if rel not in provenance_files(case)]
    return why

def load_or_run(case, f=None, force=False):
    """the cached analysis json f (default <case>/analysis_pf.json) if its provenance matches the files on disk, else (or with force) a fresh analyse(case, f)"""
    f = f or f"{case}/analysis_pf.json"
    if os.path.exists(f) and not force:
        a = json.load(open(f)); why = stale_reasons(case, a)
        if not why: print(f"{f}: cached analysis reused (provenance matches)"); return a
        print(f"{f}: cached analysis STALE, regenerating: " + "; ".join(why))
    elif force and os.path.exists(f): print(f"{f}: --force, regenerating")
    return analyse(case, f)

def not_converged(res):
    return res.get("verdict") != "CONVERGED" or not res.get("strict", {}).get("log_finished")

def analyse(case, out=None):
    info = json.load(open(f"{case}/build_info.json")); mode = info["mode"]
    lost = C.lost_outlets(info); stale_lost = [o["patch"] for o in lost if o["patch"] in json.load(open(f"{case}/zerod_reference.json"))["outlets"]]
    if stale_lost: raise SystemExit(f"{case}: outlet(s) {stale_lost} have 0 faces in the mesh but are in zerod_reference.json (case built before the lost-outlet handling, its 0-face monitors are fatal in v2406): rebuild the case")
    prov = provenance(case)                          # hashed BEFORE the read, so a file changing during the analysis makes the json stale, never falsely fresh
    res = AS.main(case, None, strict=True)
    for p, d in res["outlets"].items(): res["outlets"][p] = {RENAMED.get(k, k): v for k, v in d.items()}
    res["mode"] = mode; res["verdict_analyze_solve"] = res["verdict"]; live = C.live_outlets(info); patches = [o["patch"] for o in live]
    means = {}
    for o in live:
        p = o["patch"]; Q, qb, it = C.last_mean(case, f"{p}Flux", 100); pb, pbb, _ = C.last_mean(case, f"{p}Pressure", 100)
        means[p] = dict(Q_last100_m3s=Q, Q_last100_band_pct=qb, p_last100_kin=pb, p_last100_Pa=pb * C.RHO, p_last100_band_pct=pbb, Q_target_m3s=o["Q_target_m3s"], last_iteration=it,
                        Q_over_target_minus_1_pct=100 * (Q / o["Q_target_m3s"] - 1) if o["Q_target_m3s"] else None)
    res["last100"] = means
    res["outlets_lost_in_mesh"] = {o["patch"]: dict(Q_mls=0.0, p_Pa="N/A", flag="OUTLET_LOST_IN_MESH", Q_target_bcC_mls=o["Q_target_m3s"] * 1e6, R_bcA=o.get("R_used"), reason=o.get("reason")) for o in lost}
    res["bc_error_criteria_over_outlets"] = patches
    if lost: res["bc_bookkeeping"] = info.get("bc_bookkeeping") or C.bc_bookkeeping([dict(o) for o in live], [dict(o) for o in lost], mode)
    if mode == "prescribed":
        checks = dict(res["checks"]); dropped = {}
        if "all_bc_err_lt_0_1pct" in checks:
            dropped["all_bc_err_lt_0_1pct"] = dict(original_value=bool(checks.pop("all_bc_err_lt_0_1pct")), reason="flows are imposed; patch p vs the reference resistance law is a result, reported below, not a convergence criterion",
                                                  per_outlet_bc_err_pct={p: res["outlets"][p]["bc_err_pct"] for p in patches})
        worst = max(abs(m["Q_last100_m3s"] / m["Q_target_m3s"] - 1) for m in means.values())
        checks["prescribed_flows_delivered_1e_6"] = bool(worst < 1e-6)
        res["prescribed_Q_check"] = dict(worst_relative_deviation=worst)
        res["checks"] = checks; res["dropped_checks"] = dropped
        res["p_bar_vs_reference_law_pct"] = {p: res["outlets"][p]["bc_err_pct"] for p in patches}
        res["verdict"] = "CONVERGED" if all(checks.values()) else "UNCONVERGED"
        print(f"{res['case']}: PRESCRIBED-MODE verdict {res['verdict']} (analyze_solve verdict {res['verdict_analyze_solve']}; dropped checks {list(dropped)}; failed {[k for k, v in checks.items() if not v]})")
    else:
        res["dropped_checks"] = {}
    res["provenance"] = prov
    if out: json.dump(res, open(out, "w"), indent=1)
    return res

if __name__ == "__main__":
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    case = sys.argv[1]; out = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    if "--cached" in sys.argv: res = load_or_run(case, out, force="--force" in sys.argv)
    else: res = analyse(case, out)
    if "--require-finished" in sys.argv and not res.get("strict", {}).get("log_finished"):
        print(f"{res['case']}: --require-finished: analysis completion flag strict.log_finished is false -> exit {EXIT_NOT_FINISHED}")
        sys.exit(EXIT_NOT_FINISHED)
    if "--strict-exit" in sys.argv and not_converged(res):
        print(f"{res['case']}: --strict-exit: verdict {res.get('verdict')}, log finished {res.get('strict', {}).get('log_finished')} -> exit {EXIT_NOT_CONVERGED}")
        sys.exit(EXIT_NOT_CONVERGED)
