"""Task 4 analysis of the isolated timing run (design task4_design.md v1.3): python3 task4_analyse.py <case_dir> <out.csv> [--skip 20] [--waveform <case>/constant/waveform.table]
Inputs: log.pimpleFoam (per step: Courant Number max, deltaT, 'Time = t', ExecutionTime/ClockTime), decompose.log (cells), run_status.json (runner: how the run ended),
isolation_evidence.json (runner: bindings, `contended`), mem.log (5-s summed pimpleFoam RSS), host_before/after.txt.
OpenFOAM v2406 prints ExecutionTime = CPU time (user+system) of the master process and ClockTime = elapsed wall time (integer s). Hence:
 - WALL s/step = (ClockTime[b] - ClockTime[a-1]) / (b-a+1) over the retained contiguous window of steps a..b (1-based); the integer-second endpoints give a resolution of
   1/(b-a+1) s/step (wall_quantisation_s_per_step). No wall median/p90 exists (per-step ClockTime differences are 0/1/2 s).
 - CPU s/step = differences of consecutive ExecutionTime values (step i: ex[i]-ex[i-1]), reported as cpu_s_per_step_* (never as wall).
Window: candidate steps skip+1 .. n-1, i.e. exactly the first `skip` steps (dt ramp, coded-BC startup) and the final (stop) step are excluded; in 0-based arrays the per-step CPU is
np.diff(ex)[skip-1:-1] and the wall endpoints are clock[skip-1] .. clock[-2]. Retained = the longest contiguous run of candidate steps whose printed max Co lies in [3.0, CO_HI]
(normally the whole candidate window); dt, Co, CPU and wall all come from these same steps. Fewer than MIN_STEPS retained steps -> INVALID (no fallback); fewer than half of the
retained steps in the strict window [3.0, 5.0] -> INVALID (co_mostly_above_5: the work order asks for Co 3-5, CO_HI only absorbs the printed-Co overshoot).
run_status.json / isolation_evidence.json are type-checked: contended must be the string "no"/"yes"/"unknown", bindings_verified and controlled_end the JSON boolean true, mpirun_rc
an integer; anything else -> INVALID (evidence_malformed / run_status_malformed).
Projections (from the WALL figure; written ONLY for status VALID): flat = 0.8 s / mean dt of the retained steps; flow-weighted = integral_0^0.8 Q(t)/Q_win dt / mean dt (Q_win = mean
inlet flow over the retained steps; assumes dt ~ 1/Q at fixed Co: an ESTIMATE). A CPU-based projection is given only as the extra column cpu_projected_hours_per_cycle_CPU."""
import sys, re, csv, os, json
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")    # one BLAS thread: the numpy import alone otherwise spins up 32 threads on this host
import numpy as np
case = sys.argv[1]; out = sys.argv[2]; skip = int(sys.argv[sys.argv.index("--skip") + 1]) if "--skip" in sys.argv else 20
wf_path = sys.argv[sys.argv.index("--waveform") + 1] if "--waveform" in sys.argv else f"{case}/constant/waveform.table"
assert skip >= 1, "--skip must be >= 1 (step 1's ExecutionTime includes start-up)"
PERIOD, CELLS, MIN_STEPS, CO_LO, CO_HI, CO_STRICT = 0.8, 381356, 200, 3.0, 5.05, 5.0
CO_WINDOW = (f"printed max Co in [{CO_LO}, {CO_HI}]: the printed Co is computed from the previous step's flux with the previous deltaT, before setDeltaT adjusts dt to maxCo 5, "
             "so a Co-limited run prints values scattered around 5 (existing run_co5.log, controlled steps 12-50: 4.924-5.011, 6/39 above 5.0); 5.05 = 1% above maxCo, about 4x the "
             "largest observed overshoot (0.0115); a printed Co above 5.05 means the flux changed by >1% within one step, i.e. not the steady Co-limited regime")

def _load(name):
    try: return json.load(open(os.path.join(case, name)))
    except (OSError, ValueError): return None

txt = open(f"{case}/log.pimpleFoam").read() if os.path.exists(f"{case}/log.pimpleFoam") else ""
steps = []; cur = None; pco = pdt = None      # log order per step: Courant Number line, deltaT, "Time = t", solver output, ExecutionTime line
for ln in txt.splitlines():
    m = re.match(r"Courant Number mean: ([0-9.e+-]+) max: ([0-9.e+-]+)", ln)
    if m: pco = float(m.group(2)); continue
    m = re.match(r"deltaT = ([0-9.e+-]+)", ln)
    if m: pdt = float(m.group(1)); continue
    m = re.match(r"Time = ([0-9.e+-]+)$", ln)
    if m: cur = dict(t=float(m.group(1)), dt=pdt, co=pco); continue
    m = re.match(r"ExecutionTime = ([0-9.e+-]+) s\s+ClockTime = (\d+) s", ln)
    if m and cur is not None and cur["dt"] is not None and cur["co"] is not None: cur["ex"] = float(m.group(1)); cur["clock"] = float(m.group(2)); steps.append(cur); cur = None
n = len(steps)
ex = np.array([s["ex"] for s in steps]); clock = np.array([s["clock"] for s in steps]); dt_all = np.array([s["dt"] for s in steps]); co_all = np.array([s["co"] for s in steps])
t_all = np.array([s["t"] for s in steps])
# candidate steps skip+1 .. n-1 (1-based) = 0-based indices skip .. n-2
cand = np.arange(skip, n - 1) if n - 1 > skip else np.arange(0)
ok = (co_all[cand] >= CO_LO) & (co_all[cand] <= CO_HI) if len(cand) else np.zeros(0, bool)
best = (0, 0); i = 0                              # longest contiguous run of ok (earliest on ties), as [start, stop) into cand
while i < len(ok):
    if ok[i]:
        j = i
        while j < len(ok) and ok[j]: j += 1
        if j - i > best[1] - best[0]: best = (i, j)
        i = j
    else: i += 1
ret = cand[best[0]:best[1]]; n_ret = len(ret)          # 0-based step indices; step k's CPU = ex[k]-ex[k-1] (k >= 1 since skip >= 1)
n_ret_strict = int((co_all[ret] <= CO_STRICT).sum()) if n_ret else 0      # retained steps also in the strict window [3.0, 5.0] (retained Co >= CO_LO already)
if n_ret:
    a, b = ret[0], ret[-1]
    cpu = ex[a:b + 1] - ex[a - 1:b]                     # == np.diff(ex)[a-1:b]; for the full candidate window np.diff(ex)[skip-1:-1]
    wall = float((clock[b] - clock[a - 1]) / n_ret)     # full candidate window: (clock[-2] - clock[skip-1]) / (n-1-skip)
    d = dt_all[ret]; c = co_all[ret]; t_ret = t_all[ret]; mdt = float(d.mean())
    cpu_wall_ratio = float((ex[b] - ex[a - 1]) / (clock[b] - clock[a - 1])) if clock[b] > clock[a - 1] else None
else:
    cpu = np.zeros(0); wall = None; d = c = t_ret = np.zeros(0); mdt = None; cpu_wall_ratio = None
strict = cand[(co_all[cand] >= CO_LO) & (co_all[cand] <= CO_STRICT)] if len(cand) else cand

def _cells():
    f = f"{case}/decompose.log"      # decomposePar prints 'Number of cells = N' once per processor
    if os.path.exists(f):
        v = [int(x) for x in re.findall(r"Number of cells = (\d+)", open(f).read())]
        if v: return sum(v)
    return None
cells = _cells()
def _peak_ram():
    f = f"{case}/mem.log"
    if not os.path.exists(f): return "", "mem.log absent: peak RAM not measured"
    v = [float(p[1]) for p in (l.split() for l in open(f)) if len(p) >= 2]
    return (round(max(v) / 1024, 3), f"max over {len(v)} 5-s samples of summed pimpleFoam RSS (mem.log)") if v else ("", "mem.log empty")
peak_ram_gb, ram_note = _peak_ram()
def _waveform(f):
    """(t Q) pairs of an OpenFOAM table file, e.g. '    (0.000000 1.357500e-06)'."""
    num = r"[-+]?[0-9.]+(?:[eE][-+]?\d+)?"
    a_ = np.array([(float(x), float(y)) for x, y in re.findall(rf"^\s*\(\s*({num})\s+({num})\s*\)\s*$", open(f).read(), re.M)])
    assert len(a_) >= 2 and np.all(np.diff(a_[:, 0]) > 0), f"bad waveform table {f}"
    return a_[:, 0], a_[:, 1]

# ---- status ----
rs = _load("run_status.json"); ev = _load("isolation_evidence.json")
reasons = []; why = []
CONTENDED = ("no", "yes", "unknown")
def _malformed(d, checks):
    """Fields of a JSON object whose value has the wrong type/value ('<missing>' if absent); a non-object is malformed as a whole."""
    if not isinstance(d, dict): return ["not a JSON object"]
    return [f"{k}={d.get(k, '<missing>')!r}" for k, good in checks.items() if not (k in d and good(d[k]))]
# isolation_evidence.json: exact types only (a string 'false', a number, null or a missing key is malformed, never truthy)
ev_bad = [] if ev is None else _malformed(ev, dict(contended=lambda v: isinstance(v, str) and v in CONTENDED, bindings_verified=lambda v: isinstance(v, bool)))
if ev_bad: reasons.append("evidence_malformed"); why.append("isolation_evidence.json malformed: " + ", ".join(ev_bad))
evd = ev if isinstance(ev, dict) else {}
contended = evd["contended"] if isinstance(evd.get("contended"), str) and evd["contended"] in CONTENDED else "unknown"   # never assumed "no": missing/malformed = unknown
bindings_ok = evd.get("bindings_verified") is True
ev_reasons = evd.get("contended_reasons", ["isolation_evidence.json missing"]); ev_reasons = [str(x) for x in ev_reasons] if isinstance(ev_reasons, list) else [str(ev_reasons)]
# run_status.json: controlled_end must be a JSON boolean, mpirun_rc an integer (not a bool/float/string) or null (the runner's "unknown", then not 0 -> termination)
rs_bad = [] if rs is None else _malformed(rs, dict(controlled_end=lambda v: isinstance(v, bool), mpirun_rc=lambda v: v is None or type(v) is int))
rsd = rs if isinstance(rs, dict) else {}
if rs is None: reasons.append("no_run_status"); why.append("run_status.json missing")
elif rs_bad: reasons.append("run_status_malformed"); why.append("run_status.json malformed: " + ", ".join(rs_bad))
if rs is not None and not (rsd.get("controlled_end") is True and rsd.get("end_reason") in ("stop_honoured", "endTime") and rsd.get("bounded_stop") == "none"
                           and type(rsd.get("mpirun_rc")) is int and rsd.get("mpirun_rc") == 0):
    reasons.append("termination"); why.append(f"end {rsd.get('end_reason')!r}, bounded stop {rsd.get('bounded_stop')!r}, mpirun rc {rsd.get('mpirun_rc')!r}")
if not re.search(r"^End\s*$", txt, re.M): reasons.append("no_End_line"); why.append("log.pimpleFoam has no End line")
if cells != CELLS: reasons.append(f"cells_{cells}"); why.append(f"cells {cells} != {CELLS}")
if not bindings_ok: reasons.append("bindings_unverified"); why.append("8 distinct verified core bindings not established (isolation_evidence.json)")
if n_ret < MIN_STEPS: reasons.append(f"retained_{n_ret}_lt_{MIN_STEPS}"); why.append(f"{n_ret} retained steps with Co in [{CO_LO}, {CO_HI}] < {MIN_STEPS}")
if n_ret and 2 * n_ret_strict < n_ret:
    reasons.append("co_mostly_above_5"); why.append(f"only {n_ret_strict} of {n_ret} retained steps have Co in the strict window [{CO_LO}, {CO_STRICT}] (at least half required)")
if contended != "no": reasons.append(f"contended_{contended}"); why.append(f"contended={contended}: {ev_reasons}")
status = "VALID" if not reasons else "INVALID_" + "+".join(reasons)
valid = not reasons

# ---- projections (WALL-based; blank unless VALID) ----
fw = dict(waveform_table="", waveform_Q_start_m3s="", waveform_Q_cycle_mean_m3s="", waveform_Q_mean_over_start="", waveform_Q_retained_over_start="",
          flow_weighted_steps_per_cycle="", flow_weighted_hours_per_cycle="", flow_weighted_hours_two_cycles="")
q_note = ""
if os.path.exists(wf_path):
    wt, wq = _waveform(wf_path); q0 = float(wq[0]); g = np.linspace(0.0, PERIOD, 80001); qg = np.interp(g, wt, wq)
    qmean = float(np.sum(0.5 * (qg[1:] + qg[:-1]) * np.diff(g)) / PERIOD)
    qwin = float(np.mean(np.interp(t_ret, wt, wq))) if n_ret else q0
    fw.update(waveform_table=os.path.abspath(wf_path), waveform_Q_start_m3s=q0, waveform_Q_cycle_mean_m3s=qmean, waveform_Q_mean_over_start=qmean / q0, waveform_Q_retained_over_start=qwin / q0)
    q_note = f"Q_start {q0:.4e} m3/s vs cycle mean {qmean:.4e} m3/s (ratio {qmean / q0:.5f}); "
    if valid:
        spc = PERIOD * qmean / qwin / mdt
        fw.update(flow_weighted_steps_per_cycle=spc, flow_weighted_hours_per_cycle=spc * wall / 3600, flow_weighted_hours_two_cycles=2 * spc * wall / 3600)
else:
    print(f"WARNING: waveform table {wf_path} absent: flow-weighted projection left blank", file=sys.stderr)
blank = lambda v: v if valid else ""
before = open(f"{case}/host_before.txt").read() if os.path.exists(f"{case}/host_before.txt") else ""
after = open(f"{case}/host_after.txt").read() if os.path.exists(f"{case}/host_after.txt") else ""
fnum = lambda f, v: f(v) if len(v) else ""
notes = ("Courant: the printed max Co precedes the time-step adjustment (existing flux with the PREVIOUS deltaT), not the achieved Co of the newly solved step. "
         "Wall = ClockTime (elapsed); cpu_* = ExecutionTime (CPU of the master rank, user+system); cpu/wall near 1 does NOT prove absence of contention (a descheduled "
         "rank stalls the others in MPI waits). projected_* (flat): starting-flow dt held over the cycle. flow_weighted_*: " + q_note +
         "assumes dt ~ 1/Q at fixed Co (same flow pattern scaled, maxDeltaT inactive); an ESTIMATE, not a validated full-cycle prediction (evolving velocity profiles and "
         "pressure iterations change the cost per step). dt and wall cost come from the same retained steps. Timing columns are blank unless status is VALID.")
row = dict(status=status, invalid_reasons="; ".join(why), contended=contended, contended_reasons="; ".join(ev_reasons),
           case="sten60_pulsatile (Item 6 mesh)", solver="pimpleFoam", cells=cells, mpi_ranks=8, cores_used="8 distinct cores (--bind-to core --map-by core), verified: " + str(bindings_ok),
           physical_cores_of_host=16, steps_run=n, first_steps_excluded=skip, last_step_excluded=1, steps_candidate=len(cand), steps_retained=n_ret,
           retained_first_step=int(ret[0]) + 1 if n_ret else "", retained_last_step=int(ret[-1]) + 1 if n_ret else "", steps_candidate_outside_co_window=int((~ok).sum()) if len(ok) else 0,
           co_window=CO_WINDOW, steps_strict_co_3_to_5=len(strict), steps_retained_strict_co_3_to_5=n_ret_strict, maxCo_mean_strict_3_to_5=float(co_all[strict].mean()) if len(strict) else "",
           cpu_s_per_step_mean_strict_3_to_5=blank(float(np.mean(ex[strict] - ex[strict - 1])) if len(strict) else ""),
           wall_s_per_step=blank(wall if wall is not None else ""), wall_quantisation_s_per_step=1.0 / n_ret if n_ret else "",
           cpu_s_per_step_mean=blank(fnum(lambda v: float(v.mean()), cpu)), cpu_s_per_step_median=blank(fnum(lambda v: float(np.median(v)), cpu)),
           cpu_s_per_step_p90=blank(fnum(lambda v: float(np.percentile(v, 90)), cpu)), cpu_s_per_step_min=blank(fnum(lambda v: float(v.min()), cpu)), cpu_s_per_step_max=blank(fnum(lambda v: float(v.max()), cpu)),
           cpu_to_wall_ratio=blank(cpu_wall_ratio if cpu_wall_ratio is not None else ""), peak_ram_gb=peak_ram_gb, peak_ram_note=ram_note,
           deltaT_s_first=float(steps[0]["dt"]) if n else "", deltaT_s_min_retained=fnum(lambda v: float(v.min()), d), deltaT_s_max_retained=fnum(lambda v: float(v.max()), d),
           deltaT_s_mean_retained=mdt if mdt is not None else "", maxCo_range_retained=f"{c.min():.3f}-{c.max():.3f}" if n_ret else "",
           projected_steps_per_cycle_0p8s=blank(PERIOD / mdt if mdt else ""), projected_hours_per_cycle=blank(PERIOD / mdt * wall / 3600 if mdt else ""),
           projected_hours_two_cycles=blank(2 * PERIOD / mdt * wall / 3600 if mdt else ""),
           cpu_projected_hours_per_cycle_CPU=blank(PERIOD / mdt * float(cpu.mean()) / 3600 if mdt else ""),
           **fw,
           end_reason=rsd.get("end_reason", ""), bounded_stop=rsd.get("bounded_stop", ""), mpirun_rc=rsd.get("mpirun_rc", ""),
           load_at_start=re.search(r"load at start ([0-9.]+)", before).group(1) if re.search(r"load at start ([0-9.]+)", before) else "",
           uptime_after=after.splitlines()[1].strip() if len(after.splitlines()) > 1 else "", notes=notes)
with open(out, "w", newline="") as fh: w_ = csv.DictWriter(fh, fieldnames=list(row)); w_.writeheader(); w_.writerow(row)
diag = dict(status=status, steps_retained=n_ret, wall_s_per_step=wall, cpu_s_per_step_mean=float(cpu.mean()) if n_ret else None, deltaT_s_mean_retained=mdt,
            projected_hours_per_cycle_wall=PERIOD / mdt * wall / 3600 if mdt else None, contended=contended, peak_ram_gb=peak_ram_gb)
if not valid:
    bar = "#" * 100
    print(f"{bar}\n# INVALID TIMING RUN: {status}\n# " + "\n# ".join(why) + f"\n# the numbers below are NOT a Task 4 result and are NOT in the CSV\n{bar}", file=sys.stderr)
print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in diag.items()})
sys.exit(0 if valid else 2)
