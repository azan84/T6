"""Task B1 of work order 2026-09-26 (no compute): the settle iteration of every real-lumen steady solve, from the retained monitors and logs only. Reads nothing but postProcessing/*/*/surfaceFieldValue*.dat, log.simpleFoam,
zerod_reference.json (constants and R_i only: for scan-14 cases a constants stub, NO 0D code is imported) and build_info.json. Writes settle_iterations.csv.
CRITERION at iteration n (n >= 500), all must hold:
  (a) SETTLED (design v2.4 of the U3D study): |mean(2nd 250 of the last 500 values of the FFR proxy) - mean(1st 250)| <= 2e-4 and the last-100 band (max-min) <= 1e-4, on the proxy p_LADoutlet/P_aorta;
  (b) every outlet flow's last-100 band (max-min)/|mean| < 0.1 %  (prescribed-flow mode: the flows are imposed, so their bands are ~0 by construction; the same 0.1 % is then applied to every outlet PRESSURE band instead);
  (c) every outlet's BC error < 0.1 %: |p_i - (P_v + R_i Q_i)| / (P_v + R_i Q_i) with the values at iteration n (as analyze_solve.py); resistance mode only (in prescribed mode flows are imposed and this number is a result).
PROXY_NOT_B1 (audit 0926, GPT-5.6 Sol): the table is NOT the B1 criterion as specified; it is B1 on the substitutes below and must not be used as a production stopping rule without the analysis side's authorisation.
FFR PROXY: no solve monitored the measurement-probe pressure per iteration (scan-14 cases monitor the outlets and the throat plane, the scan-837 cases the outlets only); the proxy is the area-averaged static pressure of the outlet on the LAD path
(scan 837: outlet_LAD; scan 14: the outlet at the LAD end, out_600 / out_558 in T1) divided by the aortic pressure. For scan 14 the same criterion (a) applied to the throat-plane pressure monitor (throatP) is reported as an extra column.
'iteration first settled' = the first n at which (a),(b),(c) hold; 'permanently settled' = the first n from which they hold at every later iteration up to the end of the run. FFR (proxy) at n is the last-100 mean at n.
Wall clock to iteration n = ClockTime printed by the log after the step 'Time = n' (last occurrence in the log). The wall clocks of some solves are contended (see contended column from the timing files).
usage: b1_settle.py <out.csv>   (reads item3_837_timing.csv and M1_results.csv from env B1_RETURNS or the newest dated returns folder holding both)"""
import os, sys, re, glob, json, csv
import numpy as np
P = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{P}/pf")
import pf_common as C
K = C.zerod_stub(); RHO, P_VEN, P_AORTA = K.RHO, K.P_VEN, K.P_AORTA
DRIFT, BAND = 2e-4, 1e-4
CASES = []      # (label, scan, dir, LAD outlet patch, mode, note)
for k in ("baseline", "T1_missed_branch", "clean_nolesion"):
    lad = "out_558" if k == "T1_missed_branch" else "out_600"
    for mode in ("resistance", "prescribed", "roundtrip"):
        CASES.append((f"{k}_{mode}", "14", f"{P}/m1/cases/{k}_{mode}", lad, "resistance" if mode in ("resistance", "roundtrip") else "prescribed", "PILOT (T1 targets provisional)" if k == "T1_missed_branch" else ""))
for k in ("solve_baseline", "solve_missedbranch", "solve_lesion80", "solve_baseline_ref", "solve_baseline_extcomp", "solve_lesion80_T25a", "solve_lesion80_T25b", "solve_lesion80_W100",
          "solve_baseline_ref_hyp", "solve_lesion80_hyp", "solve_baseline_ref_E60", "solve_lesion80_E60", "solve_baseline_ref_hyp_E60", "solve_lesion80_hyp_E60"):
    CASES.append((k, "837", f"{P}/{k}", "outlet_LAD", "resistance", "PILOT_OUT_OF_COHORT"))

def load(case, name):
    fs = sorted(glob.glob(f"{case}/postProcessing/{name}/*/surfaceFieldValue*.dat"), key=lambda f: (float(re.search(r"/(\d+(?:\.\d+)?)/", f).group(1)), f))
    t, v = [], []
    for f in fs:
        d = np.loadtxt(f, comments="#", ndmin=2); t += list(d[:, 0]); v += list(d[:, 1])
    t = np.array(t); v = np.array(v)
    if not len(t): return None
    _, idx = np.unique(t[::-1], return_index=True); keep = np.sort(len(t) - 1 - idx)      # a later restart overrides an earlier value of the same iteration
    return t[keep], v[keep]

def clock_table(case):
    txt = open(f"{case}/log.simpleFoam").read(); tab = {}; cur = None
    for ln in txt.splitlines():
        m = re.match(r"^Time = (\d+)$", ln)
        if m: cur = int(m.group(1)); continue
        m = re.match(r"^ExecutionTime = [\d.]+ s\s+ClockTime = (\d+) s", ln)
        if m and cur is not None: tab[cur] = int(m.group(1))
    return tab

def rolling_ok(x, n, i):     # x: array, index i = position of iteration n (0-based); SETTLED of design v2.4 ending at i
    if i < 499: return False
    w = x[i - 499:i + 1]; return bool(abs(w[250:].mean() - w[:250].mean()) <= DRIFT and (w[-100:].max() - w[-100:].min()) <= BAND)

def band_pct(x, i): w = x[i - 99:i + 1]; return float((w.max() - w.min()) / abs(w.mean()) * 100)

def analyse(label, scan, case, lad, mode, note):
    r = dict(case=label, scan=scan, label=note or ("frozen cohort (E0 assertion passed)" if scan == "14" else ""), mode=("prescribed-flow" if mode == "prescribed" else "resistance"))
    r["b1_variant"] = "PROXY_NOT_B1: LAD-outlet pressure / P_aorta replaces the measurement-probe pressure (no solve monitored it); " + ("outlet-PRESSURE bands < 0.1 % replace the outlet-flow bands and the BC-error criterion is not applicable (flows are imposed): not authorised by B1" if mode == "prescribed" else "outlet-flow bands and BC errors as specified")
    r["bc_error_criterion"] = "N/A (flows imposed)" if mode == "prescribed" else "applied (< 0.1 %)"
    if not os.path.exists(f"{case}/log.simpleFoam"): return dict(r, status="no log.simpleFoam retained")
    ref = json.load(open(f"{case}/zerod_reference.json"))["outlets"]; info = json.load(open(f"{case}/build_info.json")) if os.path.exists(f"{case}/build_info.json") else {}
    pin = load(case, f"{lad}Pressure")
    if pin is None: return dict(r, status=f"no monitor {lad}Pressure")
    t, p = pin; ffr = p * RHO / P_AORTA; n = len(t)
    Q, PP = {}, {}
    for o, d in ref.items():
        q = load(case, f"{o}Flux"); pp = load(case, f"{o}Pressure")
        if q is None or pp is None: return dict(r, status=f"monitor of outlet {o} missing")
        Q[o] = q[1][:n]; PP[o] = pp[1][:n] * RHO
    n = min([n] + [len(v) for v in Q.values()] + [len(v) for v in PP.values()]); t = t[:n]; ffr = ffr[:n]
    ok = np.zeros(n, bool); a_ok = np.zeros(n, bool); b_ok = np.zeros(n, bool); c_ok = np.zeros(n, bool)
    for i in range(499, n):
        a = rolling_ok(ffr, t[i], i)
        if mode == "prescribed": b = all(band_pct(PP[o], i) < 0.1 for o in ref); c = True
        else:
            b = all(band_pct(Q[o], i) < 0.1 for o in ref)
            c = all(abs(PP[o][i] - (P_VEN + d["R_out"] * Q[o][i])) / (P_VEN + d["R_out"] * Q[o][i]) * 100 < 0.1 for o, d in ref.items())
        a_ok[i], b_ok[i], c_ok[i] = a, b, c; ok[i] = a and b and c
    tp = load(case, "throatP") if scan == "14" else None
    thr_first = None
    if tp is not None:
        ft = tp[1][:n] * RHO / P_AORTA
        for i in range(499, len(ft)):
            if rolling_ok(ft, tp[0][i], i): thr_first = int(tp[0][i]); break
    clk = clock_table(case); end_it = int(t[-1]); last100 = lambda i: float(ffr[max(0, i - 99):i + 1].mean())
    ffr_end = last100(n - 1); r.update(iterations_run=end_it, budget_endTime=info.get("endTime"), cells=info.get("cells") or (info.get("mesh_gates") or {}).get("cells"), ranks=info.get("nproc"),
                                       FFR_proxy_last100_at_end=ffr_end, wall_clock_total_s=clk.get(end_it), status="ok",
                                       iter_settled_criterion_a_only_first=(int(t[np.argmax(a_ok)]) if a_ok.any() else None), criterion_b_holds_at_end=bool(b_ok[-1]), criterion_c_holds_at_end=bool(c_ok[-1]),
                                       extra_throat_plane_first_settled_iteration=thr_first)
    if ok.any():
        i1 = int(np.argmax(ok)); perm = None
        bad = np.where(~ok[499:])[0]
        if not len(bad) or bad.max() + 499 < n - 1: perm = 499 if not len(bad) else int(bad.max()) + 499 + 1
        r.update(iter_first_settled=int(t[i1]), wall_clock_to_first_settled_s=clk.get(int(t[i1])), FFR_proxy_at_first_settled=last100(i1), FFR_proxy_end_minus_at_first_settled=ffr_end - last100(i1),
                 iter_permanently_settled=(int(t[perm]) if perm is not None else None), fraction_of_budget_at_first_settled=float(t[i1] / end_it))
        if perm is not None: r.update(wall_clock_to_permanently_settled_s=clk.get(int(t[perm])), FFR_proxy_at_permanently_settled=last100(perm), FFR_proxy_end_minus_at_permanently_settled=ffr_end - last100(perm))
    else: r.update(iter_first_settled=None, note_not_settled="criterion (a)+(b)+(c) never held within the run")
    return r

RETURNS_ROOT = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns"
def returns_dir():
    """env B1_RETURNS, else the newest dated folder RETURNS_ROOT/YYYY-MM-DD holding item3_837_timing.csv and M1_results.csv."""
    need = ("item3_837_timing.csv", "M1_results.csv")
    if os.environ.get("B1_RETURNS"):
        d = os.path.abspath(os.environ["B1_RETURNS"])
        if not all(os.path.isfile(f"{d}/{n}") for n in need): sys.exit(f"B1_RETURNS={d}: {' and '.join(need)} required")
        return d
    ds = sorted(d for d in glob.glob(f"{RETURNS_ROOT}/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]") if all(os.path.isfile(f"{d}/{n}") for n in need))
    if not ds: sys.exit(f"no dated returns folder under {RETURNS_ROOT} with {' and '.join(need)} (set B1_RETURNS)")
    return ds[-1]

if __name__ == "__main__":
    rows = [analyse(*c) for c in CASES]
    RET = returns_dir()
    print("returns folder:", RET, file=sys.stderr)
    tim = {x["case"]: x for x in csv.DictReader(open(f"{RET}/item3_837_timing.csv"))}
    m1 = {(x["case"], x["bc_mode"]): x for x in csv.DictReader(open(f"{RET}/M1_results.csv"))}
    for r in rows:
        if r["scan"] == "837" and r["case"] in tim:
            t_ = tim[r["case"]]; r.update(cells=int(t_["cells"]), ranks=int(t_["mpi_ranks"]), contended=t_["contended"], wall_clock_note=t_["timing_note"])
        elif r["scan"] == "14":
            k, mode = r["case"].rsplit("_", 1); x = m1.get((k, {"resistance": "resistance", "prescribed": "prescribed-flow"}.get(mode, "prescribed-flow")))
            if x: r.update(cells=int(x["n_cells"]), ranks=int(x["cores"]), contended="no (one solve at a time, 16 ranks)" if mode != "roundtrip" else "no (one solve at a time, 16 ranks)")
        r.setdefault("contended", "")
        r.pop("budget_endTime", None)
    first = ["case", "scan", "label", "mode", "cells", "ranks", "contended"]
    rows = [dict({k: r.get(k) for k in first}, **{k: v for k, v in r.items() if k not in first}) for r in rows]
    cols = []
    for r in rows:
        for k in r:
            if k not in cols: cols.append(k)
    with open(sys.argv[1], "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    for r in rows: print(r["case"], r.get("status"), "first", r.get("iter_first_settled"), "perm", r.get("iter_permanently_settled"), "end", r.get("iterations_run"), "dFFR(first)", r.get("FFR_proxy_end_minus_at_first_settled"), "clk", r.get("wall_clock_to_first_settled_s"), "/", r.get("wall_clock_total_s"))
