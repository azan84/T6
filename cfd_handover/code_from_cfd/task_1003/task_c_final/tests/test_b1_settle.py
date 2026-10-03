"""Synthetic test of taskC/b1_settle.py (D8 update): three fake cases in a temp dir, run through the --case CLI.
  A resistance, measurementP present (written with writeArea: Area column first), settles near iteration 600  -> B1, first settled ~600, floor none
  B prescribed, measurementP present, settles near 500                                                          -> B1 (D8 prescribed-flow variant), floored to 800
  C prescribed, NO measurementP, proxy outlet out_1                                                             -> PROXY_NOT_B1
Every row must recommend the full budget. usage: python3 test_b1_settle.py"""
import os, sys, json, csv, subprocess, tempfile, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); B1 = os.path.join(os.path.dirname(HERE), "b1_settle.py")
RHO, PV, PA = 1060.0, 666.61, 11998.98
N = 1200

def dat(path, t, v, area=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("# Region type : sampledSurface\n# Time          \t" + ("Area\t" if area is not None else "") + "areaAverage(p)\n")
        for a, b in zip(t, v): f.write(f"{int(a)}\t" + (f"{area:.8e}\t" if area is not None else "") + f"{b:.10e}\n")

def settle_curve(t, t0, final, amp):
    return final + amp * np.exp(-(t / t0) ** 2 * 12) * np.cos(t / 15.0)

def make(root, name, mode, settle_at, with_mp):
    c = os.path.join(root, name); t = np.arange(1, N + 1, dtype=float)
    R = 1e11; Q = 1e-7; pout = (PV + R * Q) / RHO
    flux = Q * (1 + 0.2 * np.exp(-(t / settle_at) ** 2 * 12)); pq = (PV + R * flux) / RHO                                  # BC exactly satisfied at every iteration
    if mode == "prescribed": flux = np.full(N, Q); pq = pout * (1 + 0.2 * np.exp(-(t / settle_at) ** 2 * 12))
    dat(f"{c}/postProcessing/out_1Flux/0/surfaceFieldValue.dat", t, flux); dat(f"{c}/postProcessing/out_1Pressure/0/surfaceFieldValue.dat", t, pq)
    if with_mp: dat(f"{c}/postProcessing/measurementP/0/surfaceFieldValue.dat", t, settle_curve(t, settle_at, 0.85 * PA / RHO, 0.5), area=3.37e-6)
    json.dump(dict(outlets={"out_1": dict(R_out=R, Q0_mls=0.1)}), open(f"{c}/zerod_reference.json", "w"))
    json.dump(dict(mode=mode, endTime=N, nproc=4, throat_plane=None), open(f"{c}/build_info.json", "w"))
    with open(f"{c}/log.simpleFoam", "w") as f:
        for i in range(1, N + 1): f.write(f"Time = {i}\n\nExecutionTime = {i * 0.5:.2f} s  ClockTime = {i} s\n\n")
    return c

def main():
    root = tempfile.mkdtemp(prefix="b1test_")
    try:
        a = make(root, "A_res_mp", "resistance", 600, True); b = make(root, "B_pre_mp", "prescribed", 450, True); c = make(root, "C_pre_proxy", "prescribed", 550, False)
        out = f"{root}/s.csv"
        r = subprocess.run([sys.executable, B1, out, "--case", a, "--case", b, "--case", f"{c}:out_1"], capture_output=True, text=True)
        print(r.stdout); print(r.stderr[-2000:]); assert r.returncode == 0
        rows = {x["case"]: x for x in csv.DictReader(open(out))}
        A, Bb, Cc = rows["A_res_mp"], rows["B_pre_mp"], rows["C_pre_proxy"]
        assert A["b1_label"] == "B1" and A["ffr_series"].startswith("measurementP"), A
        assert Bb["b1_label"] == "B1 (D8 prescribed-flow variant)" and Bb["min_iterations_floor"] == "800"
        assert Cc["b1_label"] == "PROXY_NOT_B1" and Cc["ffr_series"] == "proxy out_1Pressure"
        fa, fb = int(A["iter_first_settled"]), int(Bb["iter_first_settled"])
        assert 500 <= fa < 1000 and int(A["iter_first_settled_floored"]) == fa, A
        assert fb < 800 and int(Bb["iter_first_settled_floored"]) == 800, Bb
        assert abs(float(A["FFR_mon_last100_at_end"]) - 0.85) < 1e-6, A["FFR_mon_last100_at_end"]                    # the Area column was NOT read as the value
        for x in rows.values(): assert x["stop_recommendation"].startswith("RUN THE FULL BUDGET"), x["stop_recommendation"]
        assert "WOULD stop at iteration 800" in Bb["stop_recommendation"] and "not applied" in Bb["stop_recommendation"]
        print("PASS", {k: (v["b1_label"], v["iter_first_settled"], v["iter_first_settled_floored"], v["stop_recommendation"]) for k, v in rows.items()})
    finally: shutil.rmtree(root, ignore_errors=True)

if __name__ == "__main__":
    main()
