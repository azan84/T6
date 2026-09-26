"""Smoke-test verdict: reads the monitors, log.simpleFoam, the retained mesh files of the smoke case and <workdir>/smoke_checks.json (written by run_smoke_test.sh) and compares with reference_result.json.
usage: compare_smoke.py <workdir> <reference_result.json> [--wall SECONDS] [--write-reference OUT.json]
COMPLETE RUN (both modes; audit 0926 finding 1, delta finding 1): an exact line 'End' in log.simpleFoam; the log's 'Time = N' lines are exactly 1, 2, ..., 2000 (each once, in order);
  the monitors outletFlux, measurementP, outletPatchP have first column exactly 1..2000 (ascending, no duplicates/gaps, identical in the three), all values finite.
SAME MESH (both modes; audit 0926 finding 2, delta finding 2): from smoke_checks.json: STL sha256 == 47178798...ef8ef2, checkMesh_ok true, inlet_rewrites == 1 AND outlet_rewrites == 1 (wall -> patch),
  cells an int; RE-VERIFIED from the retained work directory (the sidecar is not trusted alone): sha256 of constant/triSurface/sten70.stl, constant/polyMesh/boundary (inlet and outlet type patch,
  wall type wall), log.checkMesh ('Mesh OK' present, no 'Failed', cell count); every re-verified value must agree with the sidecar.
  compare: cells == the reference's cells EXACTLY (no tolerance); --write-reference: cells == 198252 (the returned A5 coarse mesh).
PASS iff complete run, same mesh and |Q_out / Q_ref - 1| <= 0.1 % (outlet flow, the work order's criterion) against reference_result.json and against the returned value 1.17392231e-06;
also reported: FFR at x = 56.5 mm and outlet patch pressure (informational).
--write-reference OUT.json: writes this run's measurement to OUT.json only if the run is complete and the mesh checks hold (the reference argument is not read, it may be missing).
exit codes: 0 PASS / reference written; 1 FAIL (flow criterion); 3 NON-COMPARABLE (run incomplete, or different/unverified mesh: the reasons are printed; never PASS, no reference written)."""
import sys, os, json, re, hashlib
import numpy as np
RHO, P_AORTA = 1060.0, 11998.98
N_ITER, CELLS_A5 = 2000, 198252
STL_SHA256 = "47178798e1052ddb7d23d8b318a934baaf42d93d5555b9568eddcabdf9ef8ef2"
MONITORS = ("outletFlux", "measurementP", "outletPatchP")
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
    if not why:
        dq, pm, po = d["outletFlux"], float(d["measurementP"][-1, 1]), float(d["outletPatchP"][-1, 1])
        m.update(Q_out_m3s=float(dq[-1, 1]), p_measurement_kinematic=pm, FFR_x56p5=pm * RHO / P_AORTA, p_outlet_patch_kinematic=po,
                 Q_band_last200_pct=float((dq[-200:, 1].max() - dq[-200:, 1].min()) / abs(dq[-200:, 1].mean()) * 100))
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
def non_comparable(m, why):
    print(json.dumps(m, indent=1)); print("NON-COMPARABLE: " + "; ".join(why)); print("SMOKE TEST NON-COMPARABLE (no PASS, no reference written)"); sys.exit(3)
if __name__ == "__main__":
    case, ref = sys.argv[1], sys.argv[2]; wall = int(sys.argv[sys.argv.index("--wall") + 1]) if "--wall" in sys.argv else None
    m, why = measure(case); c, cwhy = mesh_checks(case); why += cwhy
    m.update(cells=c.get("cells"), stl_sha256=c.get("stl_sha256"), checkMesh_ok=c.get("checkMesh_ok"), inlet_rewrites=c.get("inlet_rewrites"), outlet_rewrites=c.get("outlet_rewrites"), omp_num_threads=c.get("omp_num_threads"))
    if "--write-reference" in sys.argv:
        if isinstance(m["cells"], int) and m["cells"] != CELLS_A5: why.append(f"different mesh (cells {m['cells']} vs {CELLS_A5} of the returned A5 coarse mesh)")
        if why: non_comparable(m, why)
        out = sys.argv[sys.argv.index("--write-reference") + 1]; m["wall_clock_total_s"] = wall; m["returned_value_stageA_A5_ladders_Q_out_m3s"] = 1.17392231e-06
        json.dump(m, open(out, "w"), indent=1); print("wrote", out); sys.exit(0)
    r = json.load(open(ref))
    if isinstance(m["cells"], int) and m["cells"] != r.get("cells"): why.append(f"different mesh (cells {m['cells']} vs {r.get('cells')})")
    if why: non_comparable(m, why)
    dq = 100 * (m["Q_out_m3s"] / r["Q_out_m3s"] - 1); dq_ret = 100 * (m["Q_out_m3s"] / r["returned_value_stageA_A5_ladders_Q_out_m3s"] - 1)
    ok = bool(abs(dq) <= 0.1 and abs(dq_ret) <= 0.1)
    print(json.dumps(m, indent=1)); print(f"outlet flow vs reference_result.json: {dq:+.5f} %   vs the returned Stage A A5 coarse value 1.17392231e-06: {dq_ret:+.5f} %   cells {m['cells']} (reference {r['cells']})   wall {wall} s (reference {r.get('wall_clock_total_s')} s)")
    print("SMOKE TEST", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
