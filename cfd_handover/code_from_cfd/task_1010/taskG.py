#!/usr/bin/env python3
"""WO 2026-10-10 Task G: one global outlet scaling k in 3D, scan 14 T1_missed_branch, resistance mode, every bc_A R multiplied by k.
Targets T_j: CLEAN full territory flows (territories.csv Q_clean_full_territory_mls, Decision B1). J(k) = sum_j (Q_j(k)/T_j - 1)^2. Q_j = sum of the outlet flows of territory j (outlets.csv territory_id).
k1 = 1: the RETURNED 2026-09-26 solve (returns/2026-09-26/M1_outlets_T1_missed_branch_resistance.csv), not re-solved.
k2 = sum_j Q_j(k1) / sum_j T_j.  k_{n+1} = argmin J under the per-territory fit log Q_j = a_j + b_j log k through the LAST TWO solves (k_{n-1}, k_n).
Stop after solving k_n (n >= 3) when |log k_n - log k_(n-1)| < 0.01 (k_(n-1) = the previous SOLVED k), or after at most two further solves beyond k3 (k4, k5): at most 4 new solves (k2..k5).
Each solve = build (pf/build_m1_case.py --r-scale k) + provenance.py write (solve-time provenance, case + return dir) + wo1010/case_job.sh 16 ranks + post_case_generic.sh, run by THIS driver one after
another (one pool job, after gate_TaskT: Task T complete under D15).
ACCEPTANCE of a solve G<n> (also of one found on restart): the steady return is complete and consistent (wo_common.steady_accept: post_summary run_completion ok, run_completion json ok, no
missing_outputs, M1_outlets AND M1_probes csv = the files whose sha256 the summary records), the case's build_info r_scale_k == the requested k (else stop exit 1, nothing moved), and the B1/D8 settle
decision (pimple_fallback.py check, the D15 trigger) is
  SETTLED and the verdict CONVERGED -> the steady solve is used (source column: the return dir);
  SETTLED but the verdict not CONVERGED -> stop exit 3 (D15 does not apply to a settled solve; operator decision; not moved, not re-solved);
  NOT_SETTLED -> if exactly one usable COMPLETE D15 fallback result exists (wo_common.fallback_for: <RET>/*/pimple_result_*.json with steady_case = this case, settle_decision NOT_SETTLED, FFR at every
     probe) Qterr is taken from its time-averaged outlet flows and FFR at all probes from its time-averaged FFR (source column 'D15 pimple fallback <file>'), and the fit continues;
     otherwise stop EXIT 4 "D15 fallback required for G<n>": the operator creates the fallback job (pimple_fallback.py make-job <case> TaskG <name>_pimple) after its audit, then restarts the driver
     (remove jobs/taskG_14_T1regen.status), which then consumes the fallback;
  NO_DECISION -> stop exit 1.
ATTEMPT ACCOUNTING (durable, outside the return tree): state/taskG_ledger.json (atomic writes). Every attempt is recorded BEFORE it starts (result 'started') and updated with its outcome:
  build_failed / provenance_failed / case_job_failed / post_check_failed: COUNTED (also a build failure that leaves no artefact); an attempt still 'started' when a driver starts (driver killed): 'interrupted',
  COUNTED; case_job rc 3 (case locked) / rc 5 (not enough disk): refused_locked / refused_disk, NOT counted, the driver stops (exit 1) and on restart the built case of a refused attempt is REUSED (not
  rebuilt, not moved, not counted) when its build_info r_scale_k == k and the return dir holds nothing but provenance*.json. Artefacts of a failed attempt (case dir, return dir) are moved to
  cases/_failed/<name>_<ts> and <RET>/_failed/<name>_<ts> (never deleted); artefacts no ledger attempt accounts for are counted once ('leftover_unrecorded'). A second COUNTED failure of the same n
  stops the driver (exit 1). A case dir locked by a running case_job.sh stops the driver (exit 1), nothing moved. A second driver instance is refused (flock state/taskG.lock, exit 1).
Numerical stops (exit 1, reported): a territory flow <= 0 (no log), |log k_n - log k_(n-1)| <= 1e-9 before a fit, argmin of the fit on the edge of the [0.05, 20] bracket.
FFR at all probes per row: FFR_<probe_id> = p_over_Paorta of the probes csv (pf/m1_probes.py; blank when the section is not valid), k1 from returns/2026-09-26/M1_probes_T1_missed_branch_resistance.csv,
k_n from <out>/M1_probes_<LABEL>_G<n>_resistance.csv (or the fallback's FFR dict); the probe set must equal the k1 set (stop exit 1 otherwise), except a 'measurement_relocated' row ('<id>_reloc'),
which gets its own column.
OUTPUTS: working checkpoints state/taskG_checkpoint.json + state/taskG_iterations_working.csv after every solve and at every stop (atomic). The RETURN files <RET>/taskG_iterations.csv/.json are
published only when the driver ends with exit 0, atomically, never overwriting a differing file (dated re-issue _<date>[_rN]). Ledger 'final' = {exit, message, solved_n, published files}: finalise_task.py
and task_gate.py TaskG require final.exit == 0.
usage: taskG.py [--plan-only]"""
import csv, json, math, os, subprocess, sys, shlex, time, fcntl, socket, datetime
# ---- PATHS (the test harness replaces this block in a copy; nothing else differs)
P = "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot"; H = f"{P}/wo1010"; CODE = H
PK = f"{P}/m1/pkg/14_left_LAD_prox_20mm_80ds__T1_missed_branch__real"; LABEL = "14_T1regen"
RET = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-10/TaskG"; K1CSV = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_outlets_T1_missed_branch_resistance.csv"
K1PROBES = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_probes_T1_missed_branch_resistance.csv"
STATE = f"{H}/state"; CASES = f"{H}/cases"; PROV = f"python3 {CODE}/provenance.py"
# ---- end PATHS
sys.path.insert(0, CODE)
import wo_common as W
FC, FR = f"{CASES}/_failed", f"{RET}/_failed"; KLO, KHI = 0.05, 20.0
LEDGER, CKJ, CKC = f"{STATE}/taskG_ledger.json", f"{STATE}/taskG_checkpoint.json", f"{STATE}/taskG_iterations_working.csv"
terr = {r["territory_id"]: float(r["Q_clean_full_territory_mls"]) for r in csv.DictReader(open(f"{PK}/territories.csv"))}
o2t = {r["outlet_id"]: r["territory_id"] for r in csv.DictReader(open(f"{PK}/outlets.csv"))}
rows, probes = [], []       # probes: the k1 probe ids (file order), the FFR columns of every row
PLAN = "--plan-only" in sys.argv
now = lambda: time.strftime("%F %T")
ledger, run = None, None

def save(): W.atomic_json(LEDGER, ledger)

def columns():
    cols = ["n", "k", "source", "settle", "J", "max_abs_Q_over_T_minus_1"] + [f"Q_terr{t}_mls" for t in terr] + [f"T_terr{t}_mls" for t in terr] + [f"FFR_{p}" for p in probes]
    return cols + sorted({c for r in rows for c in r if c.startswith("FFR_") and c not in cols}) + ["k_next", "dlogk", "stop"]      # + measurement_relocated column(s)

def csv_text():
    import io
    s = io.StringIO(); w = csv.DictWriter(s, columns(), extrasaction="ignore", lineterminator="\n"); w.writeheader(); [w.writerow(r) for r in rows]; return s.getvalue()

def record(stop=None):      # working checkpoint (state/, atomic)
    if PLAN: return
    W.atomic_json(CKJ, dict(rows=rows, stop=stop, run=run, time=now())); W.atomic_write(CKC, csv_text())

def publish(stop):          # return files: only at exit 0, atomic, dated re-issue when the content differs
    js = json.dumps(dict(rows=rows, stop=stop, attempts=ledger["attempts"], runs=ledger["runs"]), indent=1, default=str) + "\n"
    return dict(csv=W.issue_atomic(f"{RET}/taskG_iterations.csv", csv_text()), json=W.issue_atomic(f"{RET}/taskG_iterations.json", js))

def stop(msg, code=1):
    print(f"TASK G STOPPED (exit {code}): {msg}", flush=True)
    if not PLAN:
        st = dict(exit=code, message=msg, time=now()); record(st)
        run.update(end=now(), exit=code, message=msg)
        ledger["final"] = dict(st, solved_n=[r["n"] for r in rows if r["n"] >= 2]); save()
    sys.exit(code)

def Qterr(flows, src):      # flows: {outlet_id: Q_mls} of the live outlets
    q = {t: 0.0 for t in terr}
    for o, v in flows.items():
        if o not in o2t: stop(f"{src}: outlet {o} not in the package outlets.csv")
        q[o2t[o]] += float(v)
    bad = {t: v for t, v in q.items() if not (math.isfinite(v) and v > 0)}
    if bad: stop(f"territory flow(s) not > 0 in {src}: {bad} (log Q undefined; no fit)")
    return q

def outlets_csv(path): return {r["outlet_id"]: float(r["Q_mls"]) for r in csv.DictReader(open(path)) if r.get("closed") != "1"}

def check_probe_set(ids, src):
    if not probes: probes.extend(ids)
    elif ids != probes: stop(f"probe set of {src} differs from the k1 set: missing {[p for p in probes if p not in ids]}, extra {[p for p in ids if p not in probes]}" + ("" if set(ids) != set(probes) else " (order differs)"))

def FFR(probes_csv):     # -> {FFR_<probe_id>: p_over_Paorta ("" when the section is not valid)}; the non-relocated probe set must equal the k1 set
    if not os.path.isfile(probes_csv): stop(f"{probes_csv} missing (FFR at all probes)")
    rs = list(csv.DictReader(open(probes_csv)))
    if len(set(r["probe_id"] for r in rs)) != len(rs): stop(f"duplicate probe_id in {probes_csv}")
    check_probe_set([r["probe_id"] for r in rs if r["kind"] != "measurement_relocated"], probes_csv)
    return {f"FFR_{r['probe_id']}": (float(r["p_over_Paorta"]) if r.get("p_over_Paorta", "") != "" else "") for r in rs}

def FFR_fallback(d, src):     # the fallback's {probe_id: time-averaged FFR} (every k1 probe required); '<id>_reloc' = the relocated measurement plane, own column
    f = d.get("FFR") or {}; ids = {p for p in f if not p.endswith("_reloc")}
    if ids != set(probes): stop(f"FFR probe set of {src} differs from the k1 set: missing {[p for p in probes if p not in ids]}, extra {sorted(ids - set(probes))}")
    return {**{f"FFR_{p}": float(f[p]) for p in probes}, **{f"FFR_{p}": float(v) for p, v in f.items() if p.endswith("_reloc")}}

def J(q): return sum((q[t] / terr[t] - 1) ** 2 for t in terr)
def kmin(p1, p2):
    (k1, q1), (k2, q2) = p1, p2; L1, L2 = math.log(k1), math.log(k2)
    if not abs(L2 - L1) > 1e-9: stop(f"|log k {k2!r} - log k {k1!r}| = {abs(L2 - L1):.3e} <= 1e-9: the two points coincide, no fit")
    b = {t: (math.log(q2[t]) - math.log(q1[t])) / (L2 - L1) for t in terr}; a = {t: math.log(q1[t]) - b[t] * L1 for t in terr}
    f = lambda L: sum((math.exp(a[t] + b[t] * L) / terr[t] - 1) ** 2 for t in terr)
    lo, hi = math.log(KLO), math.log(KHI)
    for _ in range(200):       # golden section on log k (J under the fit is smooth; bracket 0.05..20)
        m1, m2 = lo + 0.382 * (hi - lo), lo + 0.618 * (hi - lo)
        if f(m1) < f(m2): hi = m2
        else: lo = m1
    Lm = 0.5 * (lo + hi); grid = min((f(math.log(0.05) + i * (math.log(400) / 4000)), math.log(0.05) + i * (math.log(400) / 4000)) for i in range(4001))
    if grid[0] < f(Lm) - 1e-12: Lm = grid[1]      # global check on a dense grid (two territories: J may have one minimum per sign region)
    fit = dict(a=a, b=b, J_fit=f(Lm), k_argmin=math.exp(Lm))
    if min(abs(Lm - math.log(KLO)), abs(Lm - math.log(KHI))) < 1e-6:
        rows[-1].update(fit=fit); stop(f"argmin of J under the fit through k = {k1!r}, {k2!r} is k = {math.exp(Lm):.6g}, on the edge of the bracket [{KLO}, {KHI}] (fit {fit}): no interior minimum, not solved")
    return math.exp(Lm), fit

def locked(case):
    try: fd = os.open(f"{case}/.case_job.lock", os.O_RDONLY)
    except FileNotFoundError: return False
    try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB); return False
    except BlockingIOError: return True
    finally: os.close(fd)

def case_k(case):
    try: return float(json.load(open(f"{case}/build_info.json"))["r_scale_k"])
    except (OSError, ValueError, KeyError, TypeError): return None

def only_provenance(out): return os.path.isdir(out) and all(f.startswith("provenance") and f.endswith(".json") for f in os.listdir(out))

def attempt(n, k, name, **kw):
    at = dict(dict(n=n, k=k, name=name, run=len(ledger["runs"]), time=now(), counted=False), **kw); ledger["attempts"].append(at); save(); return at

def counted(name): return sum(1 for a in ledger["attempts"] if a["name"] == name and a.get("counted"))

def solve(k, n):     # -> (source text, settle text, Q by territory, FFR columns)
    name = W.g_solve(n); case = f"{CASES}/{name}"; out = f"{RET}/{name}"; tag = W.tag_of(name)
    ext = f"{H}/out/{LABEL}_extensions.json"
    for f in (ext, f"{H}/mesh/{LABEL}/d34.json", f"{H}/mesh/{LABEL}/mesh_gates.json"):
        if not os.path.isfile(f): stop(f"{f} missing")
    while True:
        st, why = W.steady_accept(out, tag)
        if st != "failed":
            ck = case_k(case)
            if ck is None or abs(ck - k) > 1e-12 * k: stop(f"{name}: complete return but the case build_info r_scale_k = {ck!r} != requested k = {k!r} (or the case dir is gone): nothing moved")
            dec, det = W.settle(W.latest(out, f"settle_{tag}*.csv"), case)
            if dec == "NOT_SETTLED":
                f, d = W.fallback_for(RET, name)
                if f:
                    attempt(n, k, name, result="accepted_fallback", detail=f); src = f"D15 pimple fallback {f} (time averages; steady {out} NOT_SETTLED)"
                    return src, "NOT_SETTLED -> D15 COMPLETE", Qterr({o: float(v) for o, v in d["outlets"].items() if v is not None}, f), FFR_fallback(d, f)
                attempt(n, k, name, result="not_settled", detail=f"{det} | fallback: {d}")
                stop(f"D15 fallback required for G{n}: {name} (k = {k!r}) is complete but B1 did NOT settle ({det}); no usable COMPLETE fallback result ({d}). Create the fallback job "
                     f"(pimple_fallback.py make-job {case} TaskG {name}_pimple) after its audit, then restart this driver: it continues from the fallback time averages", 4)
            if dec != "SETTLED": stop(f"{name}: no B1 settle decision ({det}): nothing moved")
            if st == "unconverged":
                attempt(n, k, name, result="unconverged", detail=why)
                stop(f"{name} (k = {k!r}) completed, B1 SETTLED, but the verdict is NOT CONVERGED: {why}. Not moved, not re-solved (deterministic); D15 does not apply to a settled solve: operator decision", 3)
            attempt(n, k, name, result="accepted", detail=why)
            return out, "SETTLED", Qterr(outlets_csv(f"{out}/M1_outlets_{tag}.csv"), out), FFR(f"{out}/M1_probes_{tag}.csv")
        if os.path.isdir(case) and locked(case): stop(f"{case} is locked by a running case_job.sh (.case_job.lock): nothing moved")
        mine = [a for a in ledger["attempts"] if a["name"] == name]
        last = mine[-1] if mine else None
        reuse = (last is not None and last["result"] in ("refused_disk", "refused_locked") and not last.get("moved") and case_k(case) is not None and abs(case_k(case) - k) <= 1e-12 * k
                 and (not os.path.exists(out) or only_provenance(out)))
        if not reuse and (os.path.exists(case) or os.path.exists(out)):      # artefacts of a failed/interrupted/refused attempt: keep them under _failed, never delete
            un = [a for a in mine if not a.get("moved") and a["result"] not in ("accepted", "accepted_fallback")]
            if not any(a.get("counted") or a["result"].startswith("refused") for a in un):
                un.append(attempt(n, k, name, result="leftover_unrecorded", counted=True, detail=f"artefacts no ledger attempt accounts for ({why})"))
            ts0 = ts = time.strftime("%Y%m%d_%H%M%S"); mv = {}; i = 1
            while os.path.exists(f"{FC}/{name}_{ts}") or os.path.exists(f"{FR}/{name}_{ts}"): ts = f"{ts0}_{i}"; i += 1      # two moves within one second
            for src, dst in ((case, f"{FC}/{name}_{ts}"), (out, f"{FR}/{name}_{ts}")):
                if os.path.exists(src): os.makedirs(os.path.dirname(dst), exist_ok=True); os.rename(src, dst); mv[src] = dst
            for a in un: a["moved"] = mv
            save(); print(f"{name}: artefacts of the earlier attempt moved: {mv} ({why})", flush=True)
        nf = counted(name)
        if nf >= 2: stop(f"{name} (k = {k!r}) failed {nf} counted times (ledger {LEDGER}; artefacts {FC}/{name}_* and {FR}/{name}_*; last: {why}): stopping, not retried again")
        at = attempt(n, k, name, result="started", reused_case=reuse)
        print(f"{name}: attempt {nf + 1} (k = {k!r}){' reusing the case built before a refused run' if reuse else ''}", flush=True)
        if reuse: rb = 0
        else:
            rb = subprocess.run(f"OMP_NUM_THREADS=4 nice -n 5 python3 {P}/pf/build_m1_case.py {PK} {H}/mesh/{LABEL} resistance {case} 16 --extensions-json {ext} --r-scale {k!r} > {H}/logs/build_{name}.log 2>&1", shell=True).returncode
            if rb == 0 and case_k(case) != k: rb = 99      # the builder must record the requested k
        if rb != 0: at.update(result="build_failed", counted=True, build_rc=rb, time_end=now()); save(); continue
        rp = subprocess.run(f"{PROV} write {case} --out {out} --job taskG_14_T1regen:{name} --built-in-job {0 if reuse else 1} >> {H}/logs/taskG_{name}.log 2>&1", shell=True).returncode
        if rp != 0: at.update(result="provenance_failed", counted=True, provenance_rc=rp, time_end=now()); save(); continue
        post = (f"cd {P} && mkdir -p {out} && P={P} GATES_JSON={H}/out/{LABEL}/gates.json MESH_GATES_JSON={H}/mesh/{LABEL}/mesh_gates.json D34_JSON={H}/mesh/{LABEL}/d34.json "
                f"OMP_NUM_THREADS=4 bash {P}/post_case_generic.sh {case} {PK} {LABEL}_G{n} resistance {out}")
        rs = subprocess.run(f"POST_CMD={shlex.quote(post)} DISK_NEED_GB=6 bash {H}/case_job.sh {case} 16 >> {H}/logs/taskG_{name}.log 2>&1", shell=True).returncode
        if rs in (3, 5):
            at.update(result="refused_locked" if rs == 3 else "refused_disk", counted=False, case_job_rc=rs, time_end=now()); save()
            stop(f"{name}: case_job.sh refused (rc {rs}: {'case locked' if rs == 3 else 'not enough free disk'}); not counted as a failed attempt; the built case is reused on restart")
        if rs != 0: at.update(result="case_job_failed", counted=True, case_job_rc=rs, time_end=now()); save(); continue
        st2, why2 = W.steady_accept(out, tag)
        at.update(result=("ran" if st2 != "failed" else "post_check_failed"), counted=(st2 == "failed"), case_job_rc=0, detail=why2, time_end=now()); save()

def row(n, k, q, src, settle, ffr): return dict(n=n, k=k, source=src, settle=settle, J=J(q), max_abs_Q_over_T_minus_1=max(abs(q[t] / terr[t] - 1) for t in terr),
                                                **{f"Q_terr{t}_mls": q[t] for t in terr}, **{f"T_terr{t}_mls": terr[t] for t in terr}, **ffr)

if not PLAN:
    os.makedirs(STATE, exist_ok=True); os.makedirs(f"{H}/logs", exist_ok=True)
    _lk = open(f"{STATE}/taskG.lock", "w")
    try: fcntl.flock(_lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError: print("TASK G REFUSED: another taskG.py holds state/taskG.lock"); sys.exit(1)
    try: ledger = json.load(open(LEDGER))
    except FileNotFoundError: ledger = dict(created=now(), runs=[], attempts=[], final=None)
    for a in ledger["attempts"]:
        if a["result"] == "started": a.update(result="interrupted", counted=True, detail="the driver stopped during this attempt (found 'started' by a later driver run)")
    for r in ledger["runs"]:
        if r.get("exit") is None: r.update(exit="lost", message="no end recorded (driver killed)")
    if ledger.get("final"): ledger.setdefault("finals", []).append(ledger["final"])
    ledger["final"] = None; run = dict(start=now(), pid=os.getpid(), host=socket.gethostname(), exit=None); ledger["runs"].append(run); save()

q1 = Qterr(outlets_csv(K1CSV), K1CSV); pts = [(1.0, q1)]; rows.append(row(1, 1.0, q1, "returned 2026-09-26 solve (k1 = 1, not re-solved)", "returned 2026-09-26", FFR(K1PROBES)))
k2 = sum(q1.values()) / sum(terr.values()); rows[-1]["k_next"] = k2
print(f"k1 = 1: Q = {q1}, T = {terr}, J = {J(q1):.5f}; k2 = {k2:.6f}; FFR {dict((c, v) for c, v in rows[-1].items() if c.startswith('FFR_'))}")
if PLAN: sys.exit(0)
k, n = k2, 2
while True:
    out, settle, q, ffr = solve(k, n); pts.append((k, q)); rows.append(row(n, k, q, out, settle, ffr))
    d = abs(math.log(k) - math.log(pts[-2][0])) if n >= 3 else None     # WO: after solving k_n (n >= 3) stop if |log k_n - log k_(n-1)| < 0.01
    stop_ = (n >= 3 and d < 0.01) or n >= 5; rows[-1].update(dlogk=d, stop=("converged |dlog k| < 0.01" if (n >= 3 and d < 0.01) else ("max solves (k2..k5)" if n >= 5 else "")))
    if stop_ and not abs(math.log(k) - math.log(pts[-2][0])) > 1e-9: rows[-1].update(k_next=None, fit="not fitted: |dlog k| <= 1e-9")      # converged onto the same k: nothing to fit, not an error
    else: kn, fit = kmin(pts[-2], pts[-1]); rows[-1].update(k_next=kn, fit=fit)
    record(); print(rows[-1], flush=True)
    if stop_: break
    k, n = kn, n + 1
fin = dict(exit=0, message=rows[-1]["stop"], time=now()); record(fin)
pub = publish(fin)
run.update(end=now(), exit=0, message=fin["message"])
ledger["final"] = dict(fin, solved_n=[r["n"] for r in rows if r["n"] >= 2], published=pub); save()
print(f"TASK G DONE: {fin['message']}; published {pub}")
