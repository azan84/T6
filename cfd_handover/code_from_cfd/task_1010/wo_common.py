#!/usr/bin/env python3
"""WO 2026-10-10: shared definitions of the wo1010 drivers (single source of truth for task_gate.py, finalise_task.py, taskG.py, make_job.py, provenance.py).
  EXPECTED      the expected solves (return sub-folder names) of every task; Task G's list is read from the Task G ledger (state/taskG_ledger.json), see expected().
  steady_accept the acceptance of a returned steady solve: post_summary verdict CONVERGED, run_completion ok (summary AND run_completion json), no missing_outputs, M1_outlets and M1_probes csv equal to
                the files whose sha256 the summary records.
  settle        the B1/D8 settle decision: `pimple_fallback.py check <settle.csv> <steady_case>` (the ONE implementation of the rule; exit 0 NOT_SETTLED, 3 SETTLED, 2 NO_DECISION).
  fallback_for  the D15 fallback result of a steady solve: <task_dir>/*/pimple_result_*.json with basename(steady_case) == the solve name (interface agreed with part B, 2026-10-10:
                keys status COMPLETE|INCOMPLETE, steady_case, settle_decision, outlets {id: Q_mls}, FFR {probe_id: mean}, FFR_probes_missing, production_ready, forced_untriggered).
                Usable only when status COMPLETE, settle_decision NOT_SETTLED, not forced, FFR_probes_missing empty, production_ready not False, and exactly one such result exists.
  solve_state   one expected solve: ok = (steady accepted AND settle SETTLED) OR (steady case NOT_SETTLED AND a usable COMPLETE fallback); provenance.json must exist in the return dir.
  atomic_write / issue_atomic   write-to-temp + os.replace; issue_atomic never overwrites a differing file (dated suffix _<date>, then _<date>_rN; work order section 5)."""
import os, re, csv, json, glob, hashlib, subprocess, datetime, tempfile

HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
JOBS = "/home/azan/paper6_t6_work/wo1010_pool/jobs"
DRIVE_RETURNS = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns"
WO = "2026-10-10"
CASES = f"{HERE}/cases"; STATE = f"{HERE}/state"
TASKS = ("TaskT", "TaskG", "TaskM", "TaskT2", "TaskN")
G_LABEL = "14_T1regen"
EXPECTED = dict(TaskT=["14_T5n_resistance", "14_T5n_prescribed", "14_T5w_resistance", "14_T5w_prescribed", "14_T5n_12p5_resistance"],
                TaskM=[f"{s}_T1_{m}" for s in (138, 69, 473, 139) for m in ("resistance", "prescribed")],
                TaskT2=[f"{s}_{v}_{m}" for s in (138, 473) for v in ("T5n", "T5w") for m in ("resistance", "prescribed")],
                TaskN=["306_base_resistance"] + [f"306_{v}_{m}" for v in ("T1", "T5n", "T5w") for m in ("resistance", "prescribed")])
# the pool job that produces each expected solve (Task G: the driver job)
JOB_OF = {s: s for t in ("TaskT", "TaskM", "TaskT2", "TaskN") for s in EXPECTED[t]}

def g_solve(n): return f"{G_LABEL}_resistance_G{n}"
def ledger_path(state=None): return f"{state or STATE}/taskG_ledger.json"

def expected(task, state=None):
    """-> list of expected solve names; Task G: G2..Gn of a driver that ENDED WITH EXIT 0 (ledger 'final'); raises ValueError (with the reason) otherwise"""
    if task not in TASKS: raise ValueError(f"task must be one of {TASKS}")
    if task != "TaskG": return list(EXPECTED[task])
    lp = ledger_path(state)
    try: L = json.load(open(lp))
    except (OSError, ValueError) as e: raise ValueError(f"Task G ledger {lp} unreadable ({type(e).__name__}: {e}): the driver has not run/finished")
    fin = L.get("final") or {}
    if fin.get("exit") != 0: raise ValueError(f"Task G driver has not finished with exit 0 (ledger final = {fin or 'none'}; last run {(L.get('runs') or [{}])[-1]})")
    ns = fin.get("solved_n") or []
    if not ns or sorted(ns) != list(range(2, max(ns) + 1)): raise ValueError(f"Task G ledger final.solved_n = {ns}: not a contiguous G2..Gn list")
    return [g_solve(n) for n in ns]

def tag_of(solve):
    """return-dir name -> file tag: <label>_<mode> stays; <label>_resistance_G<n> -> <label>_G<n>_resistance (post_case_generic.sh label of the Task G solves)"""
    m = re.fullmatch(r"(.+)_(resistance|prescribed)_G(\d+)", solve)
    return f"{m.group(1)}_G{m.group(3)}_{m.group(2)}" if m else solve

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""): h.update(blk)
    return h.hexdigest()

def tree_sha256(root, rel_to=None):
    """sha256 over the sorted lines '<sha256>  <relative path>' of every regular file under root (recursive; symlinks followed for files) -> (hash, n_files)"""
    fs = []
    for d, ds, ff in os.walk(root):
        ds.sort()
        for f in sorted(ff):
            p = os.path.join(d, f)
            if os.path.isfile(p): fs.append((os.path.relpath(p, rel_to or root), sha256(p)))
    fs.sort()
    return hashlib.sha256("".join(f"{h}  {r}\n" for r, h in fs).encode()).hexdigest(), len(fs)

def atomic_write(path, data):
    """write text/bytes to path through a temp file in the same directory + fsync + os.replace (a reader never sees a partial file)"""
    d = os.path.dirname(os.path.abspath(path)); os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{os.path.basename(path)}.", suffix=".tmp", dir=d)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data.encode() if isinstance(data, str) else data); fh.flush(); os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp): os.unlink(tmp)
        raise
    return path

def atomic_json(path, obj): return atomic_write(path, json.dumps(obj, indent=1, default=str) + "\n")

def issue_atomic(path, text, date=None):
    """like pimple_fallback.issue (identical file: kept; differing file: never overwritten, <stem>_<date><ext>, then _<date>_r2 ...) but each new file is written atomically. -> the path holding text"""
    date = date or datetime.date.today().isoformat(); stem, ext = os.path.splitext(path)
    for cand in [path, f"{stem}_{date}{ext}"] + [f"{stem}_{date}_r{i}{ext}" for i in range(2, 100)]:
        if os.path.exists(cand):
            if open(cand, newline="").read() == text: return cand
            continue
        return atomic_write(cand, text)
    raise SystemExit(f"too many re-issues of {path}")

def latest(d, name):
    """the newest issue of <d>/<name> (name may contain '*' only right before the extension, e.g. settle_<tag>*.csv): the plain file or its dated re-issues <stem>_YYYY-MM-DD[_rN]<ext>"""
    stem, ext = os.path.splitext(name.replace("*", "")); rx = re.compile(re.escape(stem) + r"(?:_(\d{4}-\d\d-\d\d)(?:_r(\d+))?)?" + re.escape(ext) + "$")
    c = []
    for f in os.listdir(d) if os.path.isdir(d) else []:
        m = rx.fullmatch(f)
        if m: c.append(((m.group(1) or "", int(m.group(2) or (1 if m.group(1) else 0))), os.path.join(d, f)))
    return max(c)[1] if c else None

# ---------------------------------------------------------------- acceptance of a returned steady solve
def steady_accept(out, tag):
    """-> ("accepted" | "unconverged" | "failed", reason). 'unconverged' = a complete, consistent return whose analyze verdict is not CONVERGED."""
    sp, rp = f"{out}/post_summary_{tag}.json", f"{out}/run_completion_{tag}.json"
    if not os.path.exists(sp): return "failed", f"no {sp}"
    try: s = json.load(open(sp)); rc = json.load(open(rp))
    except Exception as e: return "failed", f"unreadable summary/run_completion: {type(e).__name__}: {e}"
    if not (s.get("run_completion") or {}).get("ok") or not rc.get("ok"): return "failed", f"run_completion not ok: {(s.get('run_completion') or {}).get('fails')} / {rc.get('fails')}"
    if s.get("missing_outputs"): return "failed", f"post_summary missing_outputs {s['missing_outputs']}"
    for f in (f"{out}/M1_outlets_{tag}.csv", f"{out}/M1_probes_{tag}.csv"):
        rec = (s.get("outputs") or {}).get(os.path.basename(f)) or {}
        if not os.path.exists(f) or not rec.get("sha256") or rec.get("sha256") != sha256(f): return "failed", f"{f} missing or not the file recorded in {sp} (sha256)"
    if s.get("verdict") != "CONVERGED": return "unconverged", f"verdict {s.get('verdict')!r}, failed checks {s.get('failed_checks')} ({sp})"
    return "accepted", sp

# ---------------------------------------------------------------- settle decision (B1/D8), the rule of pimple_fallback.py check
def settle(settle_csv, case):
    """-> (decision SETTLED | NOT_SETTLED | NO_DECISION, detail text)"""
    if not settle_csv or not os.path.isfile(settle_csv): return "NO_DECISION", f"settle csv missing ({settle_csv})"
    if not os.path.isfile(f"{case}/build_info.json"): return "NO_DECISION", f"steady case {case} (build_info.json) missing: cannot apply the settle rule (keep the case dirs, work order section 5)"
    r = subprocess.run(["python3", f"{HERE}/pimple_fallback.py", "check", settle_csv, case], capture_output=True, text=True)
    dec = {0: "NOT_SETTLED", 3: "SETTLED"}.get(r.returncode, "NO_DECISION")
    return dec, (r.stdout.strip() or r.stderr.strip()[-400:])

# ---------------------------------------------------------------- D15 fallback result
def fallback_results(task_dir, solve):
    """every pimple_result_*.json under <task_dir>/*/ whose steady_case is the case of this solve -> [(path, dict)]"""
    out = []
    for f in sorted(glob.glob(f"{task_dir}/*/pimple_result_*.json")):
        try: d = json.load(open(f))
        except (OSError, ValueError): continue
        if os.path.basename(os.path.normpath(str(d.get("steady_case") or ""))) == solve: out.append((f, d))
    return out

def usable_fallback(d):
    """-> reason it is NOT usable, or '' """
    if d.get("status") != "COMPLETE": return f"status {d.get('status')!r}"
    if d.get("settle_decision") != "NOT_SETTLED": return f"settle_decision {d.get('settle_decision')!r} (a fallback is valid only for a NOT_SETTLED steady solve)"
    if d.get("forced_untriggered"): return "forced_untriggered build (NOT_FOR_PRODUCTION)"
    if d.get("production_ready") is False: return "production_ready false"
    if d.get("FFR_probes_missing"): return f"FFR missing at probes {sorted(d['FFR_probes_missing'])}"
    if not d.get("outlets") or not d.get("FFR"): return "no time-averaged outlets/FFR"
    return ""

def fallback_for(task_dir, solve):
    """-> (path, dict) of THE usable COMPLETE fallback of the solve, or (None, reason)"""
    res = fallback_results(task_dir, solve)
    ok = [(f, d) for f, d in res if not usable_fallback(d)]
    if len(ok) == 1: return ok[0]
    if len(ok) > 1:       # dated re-issues of one result: take the newest 'analysed', but only if they all come from the same fallback case
        if len({os.path.dirname(f) for f, _ in ok}) == 1: return max(ok, key=lambda x: str(x[1].get("analysed") or ""))
        return None, f"{len(ok)} COMPLETE fallback results in different folders: {[f for f, _ in ok]} (ambiguous)"
    return None, ("no fallback result" if not res else "; ".join(f"{os.path.basename(f)}: {usable_fallback(d)}" for f, d in res))

# ---------------------------------------------------------------- one expected solve
def provenance_of(out):
    p = latest(out, "provenance*.json")
    try: return p, (json.load(open(p)) if p else None)
    except (OSError, ValueError): return p, None

def solve_state(task_dir, solve, cases=None):
    """-> dict(solve, ok, source 'steady'|'pimple'|None, steady, settle, settle_detail, fallback, provenance, reasons[])"""
    out, tag = f"{task_dir}/{solve}", tag_of(solve); case = f"{cases or CASES}/{solve}"
    st = dict(solve=solve, out=out, tag=tag, case=case, ok=False, source=None, reasons=[], fallback=None)
    if not os.path.isdir(out): st["reasons"].append(f"return dir {out} missing"); return st
    st["steady"], why = steady_accept(out, tag); st["steady_detail"] = why
    if st["steady"] == "failed": st["reasons"].append(f"steady return not accepted: {why}"); return st
    st["settle"], st["settle_detail"] = settle(latest(out, f"settle_{tag}*.csv"), case)
    if st["settle"] == "SETTLED":
        if st["steady"] == "accepted": st["source"] = "steady"
        else: st["reasons"].append(f"B1 settled but the steady verdict is not CONVERGED ({why}); D15 does not apply to a settled solve: operator decision")
    elif st["settle"] == "NOT_SETTLED":
        f, d = fallback_for(task_dir, solve)
        if f: st["source"], st["fallback"] = "pimple", f
        else: st["reasons"].append(f"B1 NOT settled and no usable COMPLETE D15 fallback ({d}): create the fallback job (pimple_fallback.py make-job {case} {os.path.basename(os.path.normpath(task_dir))} {solve}_pimple) after its audit")
    else: st["reasons"].append(f"no settle decision: {st['settle_detail']}")
    pp, pd = provenance_of(out); st["provenance"] = pp
    if not pd: st["reasons"].append(f"provenance.json missing/unreadable in {out} (provenance.py writes it at job start)")
    elif not pd.get("host") or not pd.get("template_sha256"): st["reasons"].append(f"{pp}: host/template_sha256 empty")
    st["ok"] = st["source"] is not None and not st["reasons"]
    return st
