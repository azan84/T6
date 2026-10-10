#!/usr/bin/env python3
"""WO 2026-10-10 (Sol R2 findings 1, 2, 12): fail-closed completion gate of one task, run as the pool job gate_<Task> (ranks 1, ram 0.5 GB) after the task's solve jobs.
usage: task_gate.py <TaskT|TaskG|TaskM|TaskT2|TaskN> [--returns-root R] [--cases-dir C] [--state-dir S]
Expected solves: wo_common.EXPECTED (the list finalise_task.py uses; Task G: G2..Gn of the ledger state/taskG_ledger.json, which must record a driver that ended with exit 0).
PASS (exit 0) only if EVERY expected solve <returns>/2026-10-10/<Task>/<solve>/ has
  (a) an accepted steady return (post_summary verdict CONVERGED, run_completion ok in the summary and in run_completion_*.json, no missing_outputs, M1_outlets/M1_probes sha256 = the summary's record)
      AND the B1/D8 settle decision SETTLED (`pimple_fallback.py check <settle csv> <wo1010/cases/<solve>>`, the same rule as the fallback trigger), OR
  (b) a complete steady run that is NOT_SETTLED AND exactly one usable COMPLETE D15 fallback result (pimple_result_*.json with steady_case = that case, settle_decision NOT_SETTLED, not forced,
      FFR at every probe present);
  and (c) provenance.json in the return dir (provenance.py, written at job start) with host and template_sha256.
Task G additionally: the published taskG_iterations csv exists in the TaskG folder and its rows n >= 2 are exactly the ledger's solved iterations.
Otherwise exit 1 and list, per solve, what is missing (the fallback job for an unsettled solve is created by the operator after its own audit:
  `pimple_fallback.py make-job <steady_case> <Task> <solve>_pimple`). Exit 2: usage / no expected list (e.g. the Task G driver has not finished with exit 0).
Every run writes state/gate_<Task>.json (atomic): time, verdict, per-solve state; finalise_task.py re-runs the same check itself.
RE-RUN AFTER A FAILURE: the pool never restarts a job that has a status file; once the missing items exist, the operator removes jobs/gate_<Task>.status (and .rc/.admit/.pid/.log of it)
so that the pool runs the gate again (its dependants wait meanwhile: a failed dependency blocks them, it never releases them)."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import wo_common as W

def gate(task, returns_root=W.DRIVE_RETURNS, cases=W.CASES, state=W.STATE):
    """-> (ok, report dict)"""
    td = f"{returns_root}/{W.WO}/{task}"
    try: exp = W.expected(task, state)
    except ValueError as e: return None, dict(task=task, task_dir=td, verdict="NO_EXPECTED_LIST", reason=str(e), solves=[])
    sts = [W.solve_state(td, s, cases) for s in exp]; extra = []
    if task == "TaskG":
        it = W.latest(td, "taskG_iterations*.csv")
        if not it: extra.append(f"published taskG_iterations csv missing in {td}")
        else:
            import csv
            ns = sorted(int(r["n"]) for r in csv.DictReader(open(it)) if r.get("n") and int(r["n"]) >= 2)
            want = sorted(int(s.rsplit("G", 1)[1]) for s in exp)
            if ns != want: extra.append(f"{os.path.basename(it)} rows n>=2 {ns} != ledger solved iterations {want}")
    ok = all(s["ok"] for s in sts) and not extra
    return ok, dict(task=task, task_dir=td, verdict="PASS" if ok else "FAIL", time=time.strftime("%F %T"), expected=exp, problems=extra,
                    solves=[{k: v for k, v in s.items()} for s in sts])

def main(a):
    if not a or a[0] in ("-h", "--help"): print(__doc__); sys.exit(2)
    def opt(f, d=None):
        if f in a: i = a.index(f); v = a[i + 1]; del a[i:i + 2]; return v
        return d
    rr, cs, sd = opt("--returns-root", W.DRIVE_RETURNS), opt("--cases-dir", W.CASES), opt("--state-dir", W.STATE)
    task = a[0]
    if task not in W.TASKS: print(f"task must be one of {W.TASKS}"); sys.exit(2)
    ok, rep = gate(task, rr, cs, sd)
    W.atomic_json(f"{sd}/gate_{task}.json", rep)
    if ok is None: print(f"GATE {task}: NO EXPECTED LIST: {rep['reason']}"); sys.exit(2)
    for s in rep["solves"]:
        print(f"  {s['solve']}: " + (f"OK ({s['source']}{': ' + s['fallback'] if s['fallback'] else ''})" if s["ok"] else "MISSING: " + " | ".join(s["reasons"])))
    for p in rep["problems"]: print(f"  {task}: {p}")
    print(f"GATE {task}: {rep['verdict']} ({sum(s['ok'] for s in rep['solves'])}/{len(rep['solves'])} solves complete)")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main(sys.argv[1:])
