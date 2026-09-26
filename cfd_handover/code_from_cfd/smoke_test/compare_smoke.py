"""Smoke-test verdict: reads the monitors of the smoke case and <workdir>/smoke_checks.json (written by run_smoke_test.sh) and compares with reference_result.json.
usage: compare_smoke.py <workdir> <reference_result.json> [--wall SECONDS] [--write-reference OUT.json]
COMPLETE RUN (both modes, audit 0926 finding 1): log.simpleFoam finished (End), last iteration == 2000, the monitors outletFlux, measurementP, outletPatchP have exactly 2000 rows, all values finite.
SAME MESH (both modes, audit 0926 finding 2, from smoke_checks.json): STL sha256 == 47178798...ef8ef2, checkMesh exit code 0 and 'Mesh OK', exactly 2 'wall -> patch' rewrites (inlet, outlet);
  compare: cells == the reference's cells EXACTLY (no tolerance); --write-reference: cells == 198252 (the returned A5 coarse mesh).
PASS iff complete run, same mesh and |Q_out / Q_ref - 1| <= 0.1 % (outlet flow, the work order's criterion) against reference_result.json and against the returned value 1.17392231e-06;
also reported: FFR at x = 56.5 mm and outlet patch pressure (informational).
--write-reference OUT.json: writes this run's measurement to OUT.json only if the run is complete and the mesh checks hold (the reference argument is not read, it may be missing).
exit codes: 0 PASS / reference written; 1 FAIL (flow criterion); 3 NON-COMPARABLE (run incomplete, or different/unverified mesh: the reasons are printed; never PASS, no reference written)."""
import sys, os, json, re
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
    for n in MONITORS:
        try: d[n] = load(case, n)
        except Exception as e: why.append(f"monitor {n} unreadable ({e})"); continue
        if d[n].shape[0] != N_ITER: why.append(f"monitor {n} has {d[n].shape[0]} rows, expected {N_ITER}")
        if d[n].size == 0 or not np.all(np.isfinite(d[n])): why.append(f"monitor {n} has non-finite values")
    log = open(f"{case}/log.simpleFoam").read() if os.path.exists(f"{case}/log.simpleFoam") else ""
    its = re.findall(r"^Time = (\d+)\s*$", log, flags=re.M); ex = re.findall(r"ExecutionTime = ([\d.]+) s\s+ClockTime = (\d+) s", log)
    m = dict(iterations=int(its[-1]) if its else None, finished=("\nEnd" in log[-400:]), solver_clock_s=int(ex[-1][1]) if ex else None)
    if not m["finished"]: why.append("solver log not finished (no End in log.simpleFoam)")
    if m["iterations"] != N_ITER: why.append(f"iterations {m['iterations']}, expected {N_ITER}")
    if not why:
        dq, pm, po = d["outletFlux"], float(d["measurementP"][-1, 1]), float(d["outletPatchP"][-1, 1])
        m.update(Q_out_m3s=float(dq[-1, 1]), p_measurement_kinematic=pm, FFR_x56p5=pm * RHO / P_AORTA, p_outlet_patch_kinematic=po,
                 Q_band_last200_pct=float((dq[-200:, 1].max() - dq[-200:, 1].min()) / abs(dq[-200:, 1].mean()) * 100))
    return m, why
def mesh_checks(case):
    """(smoke_checks dict, list of failed checks) from <workdir>/smoke_checks.json"""
    try: c = json.load(open(f"{case}/smoke_checks.json"))
    except Exception as e: return {}, [f"smoke_checks.json missing or unreadable ({e})"]
    why = []
    if c.get("stl_sha256") != STL_SHA256: why.append(f"STL sha256 {c.get('stl_sha256')} != {STL_SHA256}")
    if c.get("checkMesh_ok") is not True: why.append("checkMesh failed (exit code != 0 or no 'Mesh OK')")
    if c.get("patch_rewrites") != 2: why.append(f"patch_rewrites {c.get('patch_rewrites')}, expected 2 (inlet, outlet)")
    if not isinstance(c.get("cells"), int): why.append("cell count not parsed")
    return c, why
def non_comparable(m, why):
    print(json.dumps(m, indent=1)); print("NON-COMPARABLE: " + "; ".join(why)); print("SMOKE TEST NON-COMPARABLE (no PASS, no reference written)"); sys.exit(3)
if __name__ == "__main__":
    case, ref = sys.argv[1], sys.argv[2]; wall = int(sys.argv[sys.argv.index("--wall") + 1]) if "--wall" in sys.argv else None
    m, why = measure(case); c, cwhy = mesh_checks(case); why += cwhy
    m.update(cells=c.get("cells"), stl_sha256=c.get("stl_sha256"), checkMesh_ok=c.get("checkMesh_ok"), patch_rewrites=c.get("patch_rewrites"), omp_num_threads=c.get("omp_num_threads"))
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
