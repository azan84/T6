"""Smoke-test verdict: reads the monitors, log.simpleFoam, the retained mesh files of the smoke case and <workdir>/smoke_checks.json (written by run_smoke_test.sh) and compares with reference_result.json.
usage: compare_smoke.py <workdir> <reference_result.json> [--wall SECONDS] [--write-reference OUT.json [--replace-branch deflected|symmetric]]
TWO BRANCHES (fix26, B3 diagnosis 2026-10-01, audits SOL/AGY): the steady laminar sten70 A5-coarse problem has two stable steady solutions of the discrete equations on the same mesh recipe and cell count:
  a wall-deflected (Coanda-type) jet, Q_out 1.17392231e-06 m3/s, FFR_x56p5 0.78396 (= the returned A5 coarse value, run 2026-09-18) and an axisymmetric jet, Q_out 1.17825059e-06, FFR_x56p5 0.78248
  (reference-machine smoke run 2026-10-01). A fresh run lands on either, decided by tiny cfMesh/decomposition perturbations (cfMesh is not bitwise reproducible). The branches are 0.369 % apart in Q,
  so the 0.1 % windows of the CONSTANTS cannot overlap (the windows of reference entries, each allowed 0.1 % from its constant, can: identification therefore uses Q AND FFR). The branch constants live in BRANCHES below (not only in the reference file: a missing/partial/edited reference file cannot redefine them silently;
  every reference branch entry must itself lie in the window of its constant).
COMPLETE RUN (both modes; audit 0926 finding 1, delta finding 1): an exact line 'End' in log.simpleFoam; the log's 'Time = N' lines are exactly 1, 2, ..., N_ITER = 3000 (each once, in order);
  the monitors outletFlux, measurementP, outletPatchP have first column exactly 1..3000 (ascending, no duplicates/gaps, identical in the three), all values finite; endTime of the retained system/controlDict == 3000.
  (fix25: 3000, not the 2000 of the original A5 run: a fresh 8-way v2406 run is +0.189 % at 2000 (last-100 mean +0.225 %), +0.002 % at 2500, stable to 5 digits from 2750.)
SAME MESH RECIPE AND CELL COUNT (not mesh identity: cfMesh is not bitwise reproducible; both modes; audit 0926 finding 2, delta finding 2): from smoke_checks.json: STL sha256 == 47178798...ef8ef2,
  checkMesh_ok true, inlet_rewrites == 1 AND outlet_rewrites == 1 (wall -> patch), cells an int; RE-VERIFIED from the retained work directory (the sidecar is not trusted alone): sha256 of
  constant/triSurface/sten70.stl, constant/polyMesh/boundary (inlet and outlet type patch, wall type wall), log.checkMesh ('Mesh OK' present, no 'Failed', cell count); every re-verified value must agree
  with the sidecar. compare: cells == the reference's cells EXACTLY (no tolerance); --write-reference: cells == 198252 (the cell count of the returned A5 coarse mesh).
PASS iff (fix26) complete run AND mesh checks AND exactly one branch b with BOTH |Q_out/Q_b - 1| <= 0.1 % AND |FFR_x56p5 - FFR_b| <= 0.0005 (Q_b, FFR_b from reference_result.json 'branches';
  fix26 attempt 2, audit SOL 1: the combined predicate identifies the branch, as in --write-reference; two branches with both in window -> FAIL, ambiguous) AND a stable final window: over the last 200 iterations the Q band (max - min) <= 0.01 % of its mean and the FFR band <= 1e-5 (protects against a run crossing a window
  during a slow transition; the real runs have Q bands ~1e-5 %). The verdict line names the branch; only the deflected branch reproduces the returned value.
  Q in a window but FFR outside, or an unstable final window -> FAIL with the reason; no branch matched -> FAIL with the distance to each branch.
--write-reference OUT.json (fix26): only if the run is complete, the mesh checks hold, the final window is stable and the run falls on one branch (nearest branch CONSTANT within 0.1 % Q and 0.0005 FFR);
  the existing reference (the positional argument, if it exists; schema 2 required) is the base: the other branch is always kept; an existing entry of the run's branch is replaced only with
  --replace-branch <that branch>. Records provenance incl. the sha256 of the retained constant/polyMesh/points and the processor-face count parsed from log.decomposePar.
reference_result.json schema 2 (fix26): {"schema": 2, "branches": {"deflected": {...}, "symmetric": {...}}, common: cells, stl_sha256, n_iter, tolerances, returned_value_stageA_A5_ladders_Q_out_m3s}.
  load_reference (fix26 attempt 2, audit SOL 3 / AGY 4) requires cells == CELLS_A5, stl_sha256 == STL_SHA256, n_iter == N_ITER, returned value == RETURNED_Q and every branch entry within the window of its constant.
  A schema-1 file (one flat run, pre-fix26) is refused with a clear message (exit 2): it cannot say which branch it holds.
exit codes: 0 PASS / reference written; 1 FAIL (flow/branch criterion, or --write-reference: run on no branch / unstable); 2 reference file unusable (missing, schema 1, common field or branch inconsistent with the constants) or
  --write-reference refused (branch entry exists without --replace-branch); 3 NON-COMPARABLE (run incomplete, or different/unverified mesh: the reasons are printed; never PASS, no reference written)."""
import sys, os, json, re, hashlib, datetime
import numpy as np
RHO, P_AORTA = 1060.0, 11998.98
N_ITER, CELLS_A5 = 3000, 198252     # N_ITER must equal endTime in case_files/system/controlDict (run_smoke_test.sh preflight; retained controlDict re-checked in measure)
STL_SHA256 = "47178798e1052ddb7d23d8b318a934baaf42d93d5555b9568eddcabdf9ef8ef2"
MONITORS = ("outletFlux", "measurementP", "outletPatchP")
RETURNED_Q = 1.17392231e-06         # stageA_A5_ladders.csv, A5 sten70 coarse (the returned value)
# fix26: branch constants (identification and consistency of the reference file); deflected = the returned run (p_meas 8.87426046 -> FFR 0.78395964), symmetric = smoke_ref 2026-10-01
BRANCHES = {"deflected": dict(Q_out_m3s=RETURNED_Q, FFR_x56p5=0.78395964), "symmetric": dict(Q_out_m3s=1.17825059e-06, FFR_x56p5=0.78248298)}
VERDICT = {"deflected": "deflected-jet branch = the returned A5 coarse value", "symmetric": "symmetric-jet branch; not the returned value, see SETUP.md section 4"}
TOL_Q_PCT, TOL_FFR = 0.1, 0.0005    # branch window
WIN, TOL_QBAND_PCT, TOL_FFRBAND = 200, 0.01, 1e-5   # final-window stability (audit SOL 8)
def load(case, name):
    return np.loadtxt(f"{case}/postProcessing/{name}/0/surfaceFieldValue.dat", comments="#", ndmin=2)
def measure(case):
    """(measurement dict, list of reasons why the run is incomplete)"""
    why, d = [], {}
    want = np.arange(1, N_ITER + 1, dtype=float)
    for n in MONITORS:
        try: d[n] = load(case, n)
        except Exception as e: why.append(f"monitor {n} unreadable ({e})"); continue
        if d[n].shape[0] != N_ITER: why.append(f"monitor {n} has {d[n].shape[0]} rows, expected {N_ITER}")
        if d[n].size == 0 or not np.all(np.isfinite(d[n])): why.append(f"monitor {n} has non-finite values")
        elif d[n].shape[1] < 2: why.append(f"monitor {n} has no value column")
        elif d[n].shape[0] != N_ITER or not np.array_equal(d[n][:, 0], want): why.append(f"monitor {n}: first column is not exactly 1..{N_ITER} (ascending, no duplicates or gaps)")
    if len(d) == len(MONITORS) and len({d[n].shape[0] for n in MONITORS}) == 1 and not all(np.array_equal(d[MONITORS[0]][:, 0], d[n][:, 0]) for n in MONITORS):
        why.append("the three monitors do not have identical iteration columns")
    log = open(f"{case}/log.simpleFoam").read() if os.path.exists(f"{case}/log.simpleFoam") else ""
    its = [int(x) for x in re.findall(r"^Time = (\d+)\s*$", log, flags=re.M)]; ex = re.findall(r"ExecutionTime = ([\d.]+) s\s+ClockTime = (\d+) s", log)
    m = dict(iterations=its[-1] if its else None, finished=bool(re.search(r"^End\s*$", log, flags=re.M)), solver_clock_s=int(ex[-1][1]) if ex else None)
    if not m["finished"]: why.append("solver log not finished (no exact line 'End' in log.simpleFoam)")
    if m["iterations"] != N_ITER: why.append(f"iterations {m['iterations']}, expected {N_ITER}")
    if its != list(range(1, N_ITER + 1)): why.append(f"log 'Time =' sequence is not exactly 1..{N_ITER} once each in order ({len(its)} lines)")
    cd = open(f"{case}/system/controlDict").read() if os.path.exists(f"{case}/system/controlDict") else ""; et = re.findall(r"^\s*endTime\s+(\d+)\s*;", cd, flags=re.M)
    if et != [str(N_ITER)]: why.append(f"retained system/controlDict endTime {et or 'missing'}, expected exactly {N_ITER}")
    if not why:
        dq, pm, po = d["outletFlux"], float(d["measurementP"][-1, 1]), float(d["outletPatchP"][-1, 1])
        qw, fw = dq[-WIN:, 1], d["measurementP"][-WIN:, 1] * RHO / P_AORTA
        m.update(Q_out_m3s=float(dq[-1, 1]), p_measurement_kinematic=pm, FFR_x56p5=pm * RHO / P_AORTA, p_outlet_patch_kinematic=po,
                 Q_band_last200_pct=float((qw.max() - qw.min()) / abs(qw.mean()) * 100), FFR_band_last200=float(fw.max() - fw.min()))
    return m, why
def reverify(case):
    """values re-derived from the retained work directory files: (dict, reasons)"""
    r, why = {}, []
    try: r["stl_sha256"] = hashlib.sha256(open(f"{case}/constant/triSurface/sten70.stl", "rb").read()).hexdigest()
    except OSError as e: r["stl_sha256"] = None; why.append(f"retained STL unreadable ({e})")
    try:
        b = open(f"{case}/constant/polyMesh/boundary").read(); t = {}
        for p in ("inlet", "outlet", "wall"):
            x = re.findall(r"(?:^|\s)%s\s*\{[^}]*?\btype\s+(\w+)\s*;" % p, b, flags=re.S); t[p] = x[0] if len(x) == 1 else (x or None)
        r["boundary_types"] = t
        if t != dict(inlet="patch", outlet="patch", wall="wall"): why.append(f"retained constant/polyMesh/boundary types {t}, expected inlet patch, outlet patch, wall wall")
    except OSError as e: why.append(f"retained boundary unreadable ({e})")
    try:
        lg = open(f"{case}/log.checkMesh").read(); c = re.findall(r"^\s*cells:\s+(\d+)\s*$", lg, flags=re.M)
        r["checkMesh_ok"] = bool(re.search(r"^\s*Mesh OK\.?\s*$", lg, flags=re.M)) and not re.search(r"Failed \d+ mesh checks", lg)
        r["cells"] = int(c[0]) if c else None
        if not r["checkMesh_ok"]: why.append("retained log.checkMesh: no 'Mesh OK' (or 'Failed')")
        if r["cells"] is None: why.append("retained log.checkMesh: cell count not parsed")
    except OSError as e: why.append(f"retained log.checkMesh unreadable ({e})")
    return r, why
def mesh_checks(case):
    """(smoke_checks dict, list of failed checks): <workdir>/smoke_checks.json, each value re-verified from the retained work directory (reverify)"""
    try: c = json.load(open(f"{case}/smoke_checks.json"))
    except Exception as e: return {}, [f"smoke_checks.json missing or unreadable ({e})"]
    if not isinstance(c, dict): return {}, ["smoke_checks.json is not an object"]
    why = []
    if c.get("stl_sha256") != STL_SHA256: why.append(f"STL sha256 {c.get('stl_sha256')} != {STL_SHA256}")
    if c.get("checkMesh_ok") is not True: why.append("checkMesh failed (exit code != 0 or no 'Mesh OK')")
    for k in ("inlet_rewrites", "outlet_rewrites"):
        if type(c.get(k)) is not int or c.get(k) != 1: why.append(f"{k} {c.get(k)}, expected exactly 1")
    if type(c.get("cells")) is not int: why.append("cell count not parsed")
    r, rwhy = reverify(case); why += rwhy
    for k in ("stl_sha256", "checkMesh_ok", "cells"):
        if k in r and r[k] != c.get(k): why.append(f"smoke_checks.json {k}={c.get(k)} disagrees with the retained work directory ({r[k]})")
    return c, why
def distance(m, b):
    """(dQ %, dFFR) of measurement m to branch values b"""
    return 100 * (m["Q_out_m3s"] / b["Q_out_m3s"] - 1), m["FFR_x56p5"] - b["FFR_x56p5"]
def in_window(m, b):
    dq, df = distance(m, b); return abs(dq) <= TOL_Q_PCT, abs(df) <= TOL_FFR
def stability(m):
    """reasons why the final window is not stable (empty list = stable)"""
    why = []
    if not m["Q_band_last200_pct"] <= TOL_QBAND_PCT: why.append(f"unstable final window: Q band over the last {WIN} iterations {m['Q_band_last200_pct']:.3g} % > {TOL_QBAND_PCT} % of its mean")
    if not m["FFR_band_last200"] <= TOL_FFRBAND: why.append(f"unstable final window: FFR band over the last {WIN} iterations {m['FFR_band_last200']:.3g} > {TOL_FFRBAND}")
    return why
def load_reference(path):
    """(schema-2 reference dict, None) or (None, reason); every branch entry must lie in the window of its BRANCHES constant (a reference file cannot redefine a branch)"""
    try: r = json.load(open(path))
    except Exception as e: return None, f"reference {path} missing or unreadable ({e})"
    if not isinstance(r, dict): return None, f"reference {path} is not a JSON object"
    if r.get("schema") != 2 or not isinstance(r.get("branches"), dict):
        return None, (f"reference {path} is not schema 2 (no 'schema': 2 / 'branches'): a schema-1 (pre-fix26, single-run) file cannot say which jet branch it holds; use the schema-2 "
                      f"reference_result.json shipped with this folder (branches deflected + symmetric), then add a run with --write-reference")
    for k, want in (("cells", CELLS_A5), ("stl_sha256", STL_SHA256), ("n_iter", N_ITER), ("returned_value_stageA_A5_ladders_Q_out_m3s", RETURNED_Q)):   # fix26 attempt 2 (SOL 3 / AGY 4)
        if k not in r: return None, f"reference {path}: common field '{k}' missing (expected {want})"
        if r[k] != want or type(r[k]) is bool: return None, f"reference {path}: common field '{k}' = {r[k]!r}, expected {want!r} (the constant in compare_smoke.py)"
    for k, b in r["branches"].items():
        if k not in BRANCHES: return None, f"reference {path}: unknown branch '{k}' (known: {', '.join(BRANCHES)})"
        try: q, f = in_window(b, BRANCHES[k])
        except Exception as e: return None, f"reference {path}: branch '{k}' lacks Q_out_m3s / FFR_x56p5 ({e})"
        if not (q and f): return None, f"reference {path}: branch '{k}' (Q {b['Q_out_m3s']}, FFR {b['FFR_x56p5']}) is outside the window of its constant {BRANCHES[k]}"
    return r, None
def provenance(case, m, wall):
    """provenance of this run for --write-reference: points sha256 of the retained mesh, processor faces and ranks from log.decomposePar, decomposition method"""
    p = dict(run=os.path.abspath(case), date=datetime.date.today().isoformat(), mesh_origin="fresh cartesianMesh of run_smoke_test.sh (same recipe and cell count; not mesh identity)",
             iterations=m["iterations"], solver_clock_s=m["solver_clock_s"], wall_clock_total_s=wall, omp_num_threads=m.get("omp_num_threads"),
             Q_band_last200_pct=m["Q_band_last200_pct"], FFR_band_last200=m["FFR_band_last200"])
    try:
        h = hashlib.sha256()
        with open(f"{case}/constant/polyMesh/points", "rb") as f:
            for blk in iter(lambda: f.read(1 << 20), b""): h.update(blk)
        p["mesh_points_sha256"] = h.hexdigest()
    except OSError: p["mesh_points_sha256"] = None
    lg = open(f"{case}/log.decomposePar").read() if os.path.exists(f"{case}/log.decomposePar") else ""
    pf = re.findall(r"^Number of processor faces = (\d+)", lg, flags=re.M); p["processor_faces"] = int(pf[-1]) if pf else None
    p["nprocs"] = len(set(re.findall(r"^Processor (\d+)\s*$", lg, flags=re.M))) or None
    dd = open(f"{case}/system/decomposeParDict").read() if os.path.exists(f"{case}/system/decomposeParDict") else ""
    mt = re.findall(r"^\s*method\s+(\w+)\s*;", dd, flags=re.M); p["decomposition_method"] = mt[0] if mt else None
    return p
def non_comparable(m, why):
    print(json.dumps(m, indent=1)); print("NON-COMPARABLE: " + "; ".join(why)); print("SMOKE TEST NON-COMPARABLE (no PASS, no reference written)"); return 3
def write_reference(case, ref, out, m, why, wall, replace):
    if isinstance(m["cells"], int) and m["cells"] != CELLS_A5: why.append(f"different cell count ({m['cells']} vs {CELLS_A5} of the returned A5 coarse mesh)")
    if why: return non_comparable(m, why)
    print(json.dumps(m, indent=1))
    hit = [k for k, b in BRANCHES.items() if all(in_window(m, b))]; unstable = stability(m)
    if len(hit) != 1 or unstable:
        for k, b in BRANCHES.items(): dq, df = distance(m, b); print(f"  distance to the {k} branch constant: Q {dq:+.5f} %, FFR {df:+.6f}")
        print("REFERENCE NOT WRITTEN: " + "; ".join(unstable + ([] if len(hit) == 1 else [f"the run lies in {len(hit)} branch windows (need exactly one; +-{TOL_Q_PCT} % Q and +-{TOL_FFR} FFR)"]))); return 1
    b = hit[0]
    if os.path.exists(ref):
        base, err = load_reference(ref)
        if err: print("REFERENCE NOT WRITTEN: " + err); return 2
    else:
        base = None; print(f"note: {ref} does not exist: a new reference with only the {b} branch is written; compare needs both branches (copy the shipped reference_result.json)")
    if base is None: base = dict(schema=2, branches={}, cells=CELLS_A5, stl_sha256=STL_SHA256, n_iter=N_ITER, returned_value_stageA_A5_ladders_Q_out_m3s=RETURNED_Q)
    if replace is not None and replace != b: print(f"REFERENCE NOT WRITTEN: --replace-branch {replace}, but this run is on the {b} branch"); return 2
    if b in base["branches"] and replace != b: print(f"REFERENCE NOT WRITTEN: {ref} already holds a {b} entry; pass --replace-branch {b} to replace it (the other branch is always kept)"); return 2
    base["branches"][b] = dict({k: m[k] for k in ("Q_out_m3s", "FFR_x56p5", "p_measurement_kinematic", "p_outlet_patch_kinematic")}, provenance=provenance(case, m, wall))
    with open(out, "w") as f: json.dump(base, f, indent=1)
    print(f"wrote {out}: branch {b} ({VERDICT[b]}), kept: {', '.join(k for k in base['branches'] if k != b) or 'none'}"); return 0
def main(argv):
    case, ref = argv[1], argv[2]; wall = int(argv[argv.index("--wall") + 1]) if "--wall" in argv else None
    m, why = measure(case); c, cwhy = mesh_checks(case); why += cwhy
    m.update(cells=c.get("cells"), stl_sha256=c.get("stl_sha256"), checkMesh_ok=c.get("checkMesh_ok"), inlet_rewrites=c.get("inlet_rewrites"), outlet_rewrites=c.get("outlet_rewrites"), omp_num_threads=c.get("omp_num_threads"))
    if "--write-reference" in argv:
        return write_reference(case, ref, argv[argv.index("--write-reference") + 1], m, why, wall, argv[argv.index("--replace-branch") + 1] if "--replace-branch" in argv else None)
    if "--replace-branch" in argv: print("--replace-branch is only valid with --write-reference"); return 2
    r, err = load_reference(ref)
    if err: print(err); return 2
    if isinstance(m["cells"], int) and m["cells"] != r.get("cells"): why.append(f"different cell count ({m['cells']} vs {r.get('cells')})")
    if why: return non_comparable(m, why)
    print(json.dumps(m, indent=1))
    for k in BRANCHES:
        if k not in r["branches"]: print(f"reference {ref} lacks the {k} branch (compare needs both; use the shipped reference_result.json)"); return 2
    # fix26 attempt 2 (audit SOL 1): the branch is identified by the combined predicate (Q AND FFR in window), as in write_reference; Q-only hits only explain a FAIL
    fail, hit, qhit = stability(m), [k for k in BRANCHES if all(in_window(m, r["branches"][k]))], [k for k in BRANCHES if in_window(m, r["branches"][k])[0]]
    for k in BRANCHES:
        dq, df = distance(m, r["branches"][k]); print(f"  vs {k} branch ({r['branches'][k]['Q_out_m3s']:.8e} m3/s, FFR {r['branches'][k]['FFR_x56p5']:.5f}): Q {dq:+.5f} %, FFR {df:+.6f}")
    if len(hit) > 1: fail.append(f"ambiguous: Q and FFR both in the windows of {len(hit)} branches ({', '.join(hit)}): reference branches too close")
    elif not hit and not qhit: fail.append(f"outlet flow in no branch window (+-{TOL_Q_PCT} %): distances above")
    elif not hit:
        for k in qhit: fail.append(f"outlet flow in the {k} window but FFR_x56p5 {m['FFR_x56p5']:.6f} differs from {r['branches'][k]['FFR_x56p5']:.6f} by more than {TOL_FFR}")
    print(f"vs the returned Stage A A5 coarse value {RETURNED_Q}: {100 * (m['Q_out_m3s'] / RETURNED_Q - 1):+.5f} %   cells {m['cells']} (reference {r['cells']})   final-window bands: Q {m['Q_band_last200_pct']:.2e} %, FFR {m['FFR_band_last200']:.2e}   wall {wall} s")
    if fail: print("FAIL: " + "; ".join(fail)); print("SMOKE TEST FAIL"); return 1
    print(f"SMOKE TEST PASS ({VERDICT[hit[0]]})"); return 0
if __name__ == "__main__":
    sys.exit(main(sys.argv))
