#!/usr/bin/env python3
"""Item 4 end-to-end runner: built meshes -> 0D twin boundary conditions -> OpenFOAM pair -> solve -> post-processing -> comparison -> cleanup, one command, no interactive step.
usage: run_handoff.py <spec.json> [--stages=build,launch,watch,post,compare,cleanup] [--dry-run]
Spec (json; validated before anything is executed, keys starting with '_' are documentation):
  name, lesion_case, ref_case   [A-Za-z0-9_.-]+ (no '/'): case dir names under the root; profile: a key of lesion_profile.PROFILES
  build    list of shell commands (or one string) that build both cases from their meshes and the 0D twin      } TRUSTED shell input: executed verbatim by bash,
  compare  shell command with {lesion} {ref} {out} placeholders (substituted shell-quoted)                     } the spec author is responsible for them
  out      comparison output prefix (plain file prefix under the root, no path separator, no '..'); result_json: the comparison's result file (default '<out>.json', same rules)
  valid_key  boolean key of result_json that states the pair is VALID (mid_compare: valid_pair, e60_compare: comparison_done, hyp_compare: converged_pair); missing/unreadable = not valid
  watch_timeout_h, optional launch_timeout_min.
Locking: EVERY invocation (dry runs included) takes the exclusive non-blocking lock <root>/.handoff_<name>.lock before it reads the state file and holds it until it exits;
  a second invocation for the same spec name is refused (nothing written). Launched children do not inherit the lock (close_fds), so a later invocation can watch them.
Stages (each timed; logs under handoff_logs/<name>/<invocation timestamp>/; the first failure stops the run with a non-zero exit code, nothing is retried or repaired):
  build    [no process may reference the cases] the cases must not hold output of an earlier run; the build commands; both cases must be FRESH afterwards and hold a zerod_reference.json
  launch   [no process may reference the cases before the launch] ./run_set.sh (audited launcher) then watch_converge.py --strict, both detached; pids, /proc start times and command lines are persisted in handoff_state_<name>.json
  watch    wait until both logs end with 'End' + 'Finalising parallel run' and the tracked launcher/watcher have exited (exit codes recorded when they are children of this invocation;
           a restarted invocation identifies them by pid + start time + command line, zombies count as dead). The solves are NEVER killed by this script; timeout = failure.
  post     [no process may reference the cases] per case: writeControl timeStep, final iteration F and the previous write time of hyperaemia_design 5c(e); reconstructPar -time only
           for a time without a completed reconstruction (reuse is logged); lesion_sections (previous, then final), reattachment_wss, analyze_solve --strict --json; verify the output
           times and analysis last_iteration == log_last_iteration == F. An UNCONVERGED verdict is recorded (the comparison tool decides validity), it is never reported as a success.
  compare  the compare command; result_json must have been written by it (its mtime_ns must not be earlier than that of a marker file written just before the command:
           same filesystem clock, strict nanosecond comparison, no tolerance); recorded in the state file: result path, sha256, mtime_ns, the value of result_json[valid_key],
           the post invocation it compared and the sha256 of every input artifact (analysis.json, sections_*.csv/json, wss_*.csv/json of both cases; unchanged during the command)
  (build, launch and post clear the state flag compare_evidence_valid before they change anything: a cleanup never acts on superseded compare evidence)
  cleanup  [no process may reference the cases] only if the recorded compare exited 0 with result_json[valid_key] recorded True, compare_evidence_valid is set, the recorded
           compare belongs to the recorded post, the CURRENT result_json has the recorded sha256 (and valid_key True) and every input artifact the recorded sha256,
           and the reconstructed times and post outputs verify: deletes exactly the directories processor<digits> when their count equals numberOfSubdomains (or the rest of a set
           whose deletion this runner recorded as started); anything else is refused.
The manifest handoff_manifest_<name>_<timestamp>.json (newest name in handoff_manifest_<name>.latest) records every command, exit code, log, timing, the solves' wall time, md5 of the spec,
of the built case files and of the mesh files. interactive_steps: none (the runner never prompts); human preparation (meshes, specs, review of audits) happens before the runner.
Environment: every PAIR_* variable (run_set.sh test hooks) is removed and NPROC=16 is set for every command.
TEST-ONLY hooks (never set in production): HANDOFF_ROOT (directory holding the cases and the tools, default: this file's directory), HANDOFF_FOAM_BASHRC (OpenFOAM environment file),
HANDOFF_POLL_S (polling period of launch/watch)."""
import sys, os, json, time, subprocess, hashlib, re, shutil, shlex, fcntl, ast
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.environ.get("HANDOFF_ROOT") or HERE)                                          # TEST-ONLY override
FOAM_BASHRC = os.environ.get("HANDOFF_FOAM_BASHRC") or "/usr/lib/openfoam/openfoam2406/etc/bashrc"       # TEST-ONLY override
POLL_S = float(os.environ.get("HANDOFF_POLL_S") or 0)                                                    # TEST-ONLY override (0 = production periods 10 s / 60 s)
ALL = ["build", "launch", "watch", "post", "compare", "cleanup"]
MODES = {"lesion": "lesion80", "ref": "baseline_ref"}        # mode names of the post-processing scripts (file naming), independent of the profile
SAFE = re.compile(r"^[A-Za-z0-9_.-]+$")
NUMERIC = re.compile(r"^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$")
PROCDIR = re.compile(r"^processor(0|[1-9]\d*)$")
KEEP_LOGS = ("log.cartesianMesh", "log.checkMesh")
Q = shlex.quote
LOCK = {}                                                    # spec name -> open, flock'ed file of this invocation (kept until the process exits)

def lock(name):
    """Exclusive non-blocking runner lock for the whole life of this invocation; refused if another invocation holds it."""
    path = f"{ROOT}/.handoff_{name}.lock"; fd = open(path, "a")
    try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError: fd.close(); raise SystemExit(f"{path} is held by another runner: refused (nothing executed)")
    LOCK[name] = fd

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def read(path):
    with open(path, errors="replace") as f: return f.read()

def last_iteration(case):
    it = re.findall(r"^Time = (\d+)\s*$", read(f"{case}/log.simpleFoam"), re.M)
    if not it: raise RuntimeError(f"{case}: no 'Time =' line in log.simpleFoam")
    return int(it[-1])

def finished(case):
    """The log's final block: an 'End' line followed by 'Finalising parallel run' (blank lines aside) at the very end."""
    try: lines = [l.strip() for l in read(f"{case}/log.simpleFoam")[-5000:].splitlines() if l.strip()]
    except OSError: return False
    return len(lines) >= 2 and lines[-2] == "End" and lines[-1].startswith("Finalising parallel run")

def solve_minutes(case, launch_time):
    """Wall time of a solve: the last 'ClockTime = N s' of its log, and launch -> last log write."""
    lf = f"{case}/log.simpleFoam"
    try: ct = re.findall(r"ClockTime = ([0-9.eE+-]+) s", read(lf)); mt = os.path.getmtime(lf)
    except OSError: return None
    return dict(clocktime_minutes=round(float(ct[-1]) / 60, 2) if ct else None,
                launch_to_last_log_write_minutes=round((mt - launch_time) / 60, 2) if launch_time else None)

def fresh_problems(case):
    """Items that only a run (or its post-processing) leaves in a case: a built case holds none of them."""
    bad = []
    for s in sorted(os.listdir(case)):
        if s in ("log.simpleFoam", "log.smoke", "analysis.json", "postProcessing", "dynamicCode") or s.startswith(("processor", "sections_", "wss_")): bad.append(s)
        elif s.startswith("log.") and s not in KEEP_LOGS: bad.append(s)
        elif s.endswith(".foam") and s != "case.foam": bad.append(s)
        elif NUMERIC.match(s) and s != "0": bad.append(s)                  # '0.0', '00', '-0', any other time
    if os.path.lexists(f"{case}/system/controlDict.production"): bad.append("system/controlDict.production")
    return bad

def subdomains(case):
    n = re.findall(r"^\s*numberOfSubdomains\s+(\d+)\s*;", read(f"{case}/system/decomposeParDict"), re.M)
    if len(n) != 1 or int(n[0]) < 1: raise RuntimeError(f"{case}: numberOfSubdomains not readable from decomposeParDict")
    return int(n[0])

# ---------------------------------------------------------------- processes (/proc)
def proc_stat(pid):
    """(state, start time in clock ticks = field 22) of /proc/<pid>/stat."""
    s = read(f"/proc/{pid}/stat"); r = s.rsplit(")", 1)[1].split()
    return r[0], r[19], int(r[1])

def proc_cmdline(pid):
    with open(f"/proc/{pid}/cmdline", "rb") as f: return [a.decode(errors="replace") for a in f.read().split(b"\0")[:-1]]

def proc_ident(pid):
    try: st, start, _ = proc_stat(pid); return dict(pid=pid, start=start, cmdline=proc_cmdline(pid))
    except OSError: return dict(pid=pid, start=None, cmdline=None)       # already gone: only the Popen handle knows it

def proc_alive(rec):
    """A recorded process is alive only if its pid exists, is not a zombie/dead and has the same start time and command line (a recycled pid does not count)."""
    if not rec or not rec.get("start"): return False
    try: st, start, _ = proc_stat(rec["pid"]); cmd = proc_cmdline(rec["pid"])
    except (OSError, IndexError): return False
    return st not in ("Z", "X") and start == rec["start"] and cmd == rec["cmdline"]

def case_users(cases):
    """Live processes (other than this runner and its ancestors) whose command line names a case (absolute path, or an argument that is the case name / ends in /<case>) or whose cwd is inside it."""
    mine, pid = set(), os.getpid()
    while pid > 1 and pid not in mine:
        mine.add(pid)
        try: pid = proc_stat(pid)[2]
        except (OSError, IndexError): break
    pats = [(c, re.compile(re.escape(c) + r"(?![\w.-])"), re.compile(r"(^|/)" + re.escape(os.path.basename(c)) + r"/?$")) for c in cases]
    hits = []
    for d in os.listdir("/proc"):
        if not d.isdigit() or int(d) in mine: continue
        try:
            if proc_stat(d)[0] in ("Z", "X"): continue
            cmd = proc_cmdline(d)
        except (OSError, IndexError): continue
        try: cwd = os.readlink(f"/proc/{d}/cwd")
        except OSError: cwd = ""
        joined = " ".join(cmd)
        for c, pabs, pbase in pats:
            if pabs.search(joined) or any(pbase.search(a) for a in cmd) or cwd == c or cwd.startswith(c + "/"):
                hits.append(f"pid {d}: {joined[:160]!r} (cwd {cwd})"); break
    return hits

# ---------------------------------------------------------------- spec
def profiles():
    tree = ast.parse(read(f"{HERE}/lesion_profile.py"))
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "PROFILES" for t in n.targets): return [k.value for k in n.value.keys]
    raise RuntimeError("lesion_profile.PROFILES not found")

def validate(spec):
    err = []
    known = {"name", "profile", "lesion_case", "ref_case", "build", "compare", "out", "result_json", "valid_key", "watch_timeout_h", "launch_timeout_min"}
    err += [f"unknown key {k!r}" for k in spec if k not in known and not k.startswith("_")]
    err += [f"missing '{k}'" for k in ("name", "profile", "lesion_case", "ref_case", "build", "compare", "out", "valid_key", "watch_timeout_h") if k not in spec]
    if err: return err
    spec.setdefault("result_json", f"{spec['out']}.json")
    for k in ("name", "lesion_case", "ref_case", "out", "result_json"):
        v = spec[k]
        if not isinstance(v, str) or not SAFE.match(v) or ".." in v or v.startswith("."): err.append(f"{k} {v!r} must match [A-Za-z0-9_.-]+ (no '/', no '..', no leading '.')")
    if spec["lesion_case"] == spec["ref_case"]: err.append("lesion_case == ref_case")
    if spec["profile"] not in profiles(): err.append(f"profile {spec['profile']!r} not in lesion_profile.PROFILES {profiles()}")
    if isinstance(spec["build"], str): spec["build"] = [spec["build"]]
    if not isinstance(spec["build"], list) or not spec["build"] or not all(isinstance(c, str) and c.strip() for c in spec["build"]): err.append("build must be a non-empty list of shell commands")
    if not isinstance(spec["compare"], str): err.append("compare must be a string")
    else:
        try: spec["compare"].format(lesion="L", ref="R", out="O")
        except (KeyError, IndexError, ValueError) as e: err.append(f"compare: bad placeholder ({type(e).__name__}: {e})")
    if not isinstance(spec["valid_key"], str) or not spec["valid_key"]: err.append("valid_key must be a non-empty string")
    for k in ("watch_timeout_h", "launch_timeout_min"):
        if k in spec and (isinstance(spec[k], bool) or not isinstance(spec[k], (int, float)) or spec[k] <= 0): err.append(f"{k} must be a positive number")
    return err

class Run:
    def __init__(self, spec, spec_path, stages, dry):
        self.spec, self.stages, self.dry = spec, stages, dry
        self.name = spec["name"]; self.procs = {}
        removed = sorted(k for k in os.environ if k.startswith("PAIR_"))
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("PAIR_")}
        self.env.update(LESION_PROFILE=spec["profile"], NPROC="16", PYTHONUNBUFFERED="1"); os.environ["LESION_PROFILE"] = spec["profile"]   # also for the in-process hyp_compare import
        self.les, self.ref = f"{ROOT}/{spec['lesion_case']}", f"{ROOT}/{spec['ref_case']}"
        ts0 = ts = time.strftime("%Y%m%d_%H%M%S"); base = f"{ROOT}/handoff_logs/{self.name}"; os.makedirs(base, exist_ok=True); n = 1
        while os.path.exists(f"{base}/{ts}") or os.path.exists(f"{ROOT}/handoff_manifest_{self.name}_{ts}.json"): ts = f"{ts0}_{n}"; n += 1
        self.ts, self.logdir = ts, f"{base}/{ts}"; os.makedirs(self.logdir)
        self.mpath = f"{ROOT}/handoff_manifest_{self.name}_{ts}.json"; self.spath = f"{ROOT}/handoff_state_{self.name}.json"
        self.state = json.load(open(self.spath)) if os.path.exists(self.spath) else dict(name=self.name, stages={})
        self.manifest = dict(name=self.name, invocation=ts, root=ROOT, spec_file=os.path.abspath(spec_path), spec_md5=md5(spec_path), spec=spec,
                             started=time.strftime("%Y-%m-%d %H:%M:%S"), stages_requested=stages, stages=[], dry_run=dry, logdir=self.logdir, state_file=self.spath,
                             environment=dict(NPROC="16", LESION_PROFILE=spec["profile"], removed_PAIR_variables=removed),
                             interactive_steps="none (the runner never prompts)",
                             human_preparation="meshes, specs and the review of audits are prepared by a person; the runner starts from built meshes")

    def save(self):
        self.manifest["total_stage_minutes"] = round(sum(s.get("minutes", 0) for s in self.manifest["stages"]), 2)
        with open(self.mpath, "w") as f: json.dump(self.manifest, f, indent=1, default=str)
        with open(f"{ROOT}/handoff_manifest_{self.name}.latest.tmp", "w") as f: f.write(os.path.basename(self.mpath) + "\n")
        os.replace(f"{ROOT}/handoff_manifest_{self.name}.latest.tmp", f"{ROOT}/handoff_manifest_{self.name}.latest")

    def save_state(self):
        if self.dry: return                                     # a dry run never changes the recorded state
        with open(self.spath + ".tmp", "w") as f: json.dump(self.state, f, indent=1, default=str)
        os.replace(self.spath + ".tmp", self.spath)

    def guard(self):
        """build/launch/post/cleanup: no live process may reference the case directories (the invocation lock is held since main()).
        The launch stage calls it BEFORE starting its children, and later stages of the same invocation only run after the watch stage has seen them exit,
        so the runner's own launched processes never trigger a refusal; an own solve that is still running (e.g. --stages=launch,post) is refused like any other."""
        if LOCK.get(self.name) is None: raise RuntimeError("internal: runner lock not held")
        users = case_users([self.les, self.ref])
        if users: raise RuntimeError(f"refused: live processes reference the case directories: {users[:5]}")

    def sh(self, stage, idx, cmd, cwd=None, foam=True, timeout=None, check=True):
        cwd = cwd or ROOT; log = f"{self.logdir}/{stage}_{idx}.log"; t0 = time.time()
        pre = f"source {Q(FOAM_BASHRC)} || exit 1; [ -n \"$WM_PROJECT_DIR\" ] || {{ echo 'OpenFOAM environment not set' >&2; exit 1; }}; " if foam else ""
        full = pre + f"set -e -o pipefail; cd {Q(cwd)} || exit 1; {cmd}"   # the OpenFOAM bashrc itself fails under set -e: it is sourced first, checked explicitly
        if self.dry: rc = 0; open(log, "w").write("DRY RUN: " + full + "\n")
        else:
            with open(log, "w") as f: rc = subprocess.run(["bash", "-c", full], stdout=f, stderr=subprocess.STDOUT, env=self.env, timeout=timeout, stdin=subprocess.DEVNULL).returncode
        self.cur["commands"].append(dict(cmd=cmd, cwd=cwd, shell=full, rc=rc, seconds=round(time.time() - t0, 1), log=log))
        if check and rc != 0: raise RuntimeError(f"command failed (rc={rc}): {cmd}  (see {log})")
        return rc

    def invalidate(self, why):
        """build/launch/post are about to change what a recorded comparison was based on: its evidence no longer licenses a cleanup."""
        if self.dry: return
        self.state["compare_evidence_valid"] = False
        if self.state.get("compare"): self.state["compare"]["superseded_by"] = why
        self.save_state()

    def note(self, msg):
        self.cur["notes"].append(msg); print(f"  {msg}", flush=True)

    def stage(self, name, fn):
        if name not in self.stages: return
        self.cur = dict(stage=name, commands=[], notes=[], status="RUNNING", started=time.strftime("%H:%M:%S")); t0 = time.time()
        self.manifest["stages"].append(self.cur); print(f"[{time.strftime('%H:%M:%S')}] stage {name} ...", flush=True)
        try: fn(); self.cur["status"] = "OK"
        except BaseException as e:
            self.cur["status"] = "FAILED"; self.cur["error"] = f"{type(e).__name__}: {e}"; self.manifest["outcome"] = f"FAILED at stage {name}: not a result"
            print(f"stage {name} FAILED: {e}", file=sys.stderr)
        finally:
            self.cur["minutes"] = round((time.time() - t0) / 60, 2)
            if not self.dry: self.state.setdefault("stages", {})[name] = dict(status=self.cur["status"], invocation=self.ts, time=time.time()); self.save_state()
            self.save()
        if self.cur["status"] != "OK": raise SystemExit(1)
        print(f"[{time.strftime('%H:%M:%S')}] stage {name} OK ({self.cur['minutes']} min)", flush=True)

    # ---------------------------------------------------------------- stages
    def build(self):
        self.guard()
        for c in (self.les, self.ref):
            if os.path.isdir(c) and fresh_problems(c): raise RuntimeError(f"{c} already holds run output {fresh_problems(c)[:6]}: the build stage never overwrites a run")
        self.invalidate(f"build {self.ts}")
        for i, cmd in enumerate(self.spec["build"]): self.sh("build", i, cmd)
        if self.dry: return
        self.cur["built"] = {}
        for c in (self.les, self.ref):
            bad = fresh_problems(c)
            if bad: raise RuntimeError(f"{c}: not fresh after the build: {bad}")
            for need in ("zerod_reference.json", "0/p", "0/U", "system/controlDict", "system/decomposeParDict"):
                if not os.path.exists(f"{c}/{need}"): raise RuntimeError(f"{c}: {need} missing after the build")
            z = json.load(open(f"{c}/zerod_reference.json")); pm = f"{c}/constant/polyMesh"
            mesh = {n: md5(f"{pm}/{n}") for n in sorted(os.listdir(pm)) if os.path.isfile(f"{pm}/{n}")}
            self.cur["built"][os.path.basename(c)] = dict(files={n: md5(f"{c}/{n}") for n in ("0/p", "0/U", "system/controlDict", "system/decomposeParDict", "zerod_reference.json")},
                                                          Q_demand_mls=z["Q_demand_mls"], C=z.get("C"), n_outlets=len(z["outlets"]), mesh_files_md5=mesh,
                                                          polyMesh_md5=hashlib.md5("".join(md5(f"{pm}/{n}") for n in ("points", "faces", "owner", "neighbour", "boundary")).encode()).hexdigest())
        zl, zr = (json.load(open(f"{c}/zerod_reference.json")) for c in (self.les, self.ref))
        if set(zl["outlets"]) != set(zr["outlets"]): raise RuntimeError(f"outlet sets differ between the pair: {sorted(zl['outlets'])} vs {sorted(zr['outlets'])}")
        for p, d in zr["outlets"].items():
            if abs(zl["outlets"][p]["R_out"] / d["R_out"] - 1) > 1e-9 or abs(zl["outlets"][p]["relax"] / d["relax"] - 1) > 1e-9: raise RuntimeError(f"{p}: R_out/relax differ between the pair")
        self.manifest["previous_state"] = self.state
        self.state = dict(name=self.name, stages={}, compare_evidence_valid=False, build=dict(invocation=self.ts, time=time.time()))      # a new build starts a new run: nothing recorded earlier applies to it

    def launch(self):
        lb, rb = os.path.basename(self.les), os.path.basename(self.ref)
        log, wlog = f"{self.logdir}/run_set.log", f"{self.logdir}/watch.log"
        argv = ["./run_set.sh", lb, rb]; wargv = [sys.executable, f"{ROOT}/watch_converge.py", "--strict", rb, lb]
        self.cur["commands"] += [dict(argv=argv, cwd=ROOT, log=log, detached=True), dict(argv=wargv, cwd=ROOT, log=wlog, detached=True)]
        if self.dry: self.note("dry run: nothing launched"); return
        L0 = self.state.get("launch") or {}
        live = [k for k in ("run_set", "watch") if proc_alive(L0.get(k))]
        if live: raise RuntimeError(f"the {live} process(es) of an earlier launch ({L0.get('invocation')}) are still alive: refused")
        self.guard()                                            # before any child of this invocation exists
        self.invalidate(f"launch {self.ts}")
        p = subprocess.Popen(argv, cwd=ROOT, stdout=open(log, "w"), stderr=subprocess.STDOUT, env=self.env, start_new_session=True, stdin=subprocess.DEVNULL)
        self.procs["run_set"] = p; t0 = time.time()
        L = self.state["launch"] = dict(invocation=self.ts, time=t0, time_str=time.strftime("%Y-%m-%d %H:%M:%S"), run_set=dict(proc_ident(p.pid), log=log, rc=None))
        for k in ("post", "compare", "cleanup"): self.state.pop(k, None)
        self.save_state(); self.manifest["launch"] = L
        tmax = 60 * float(self.spec.get("launch_timeout_min", 30))
        while True:
            time.sleep(POLL_S or 10)
            rc = p.poll()
            if rc is not None: L["run_set"]["rc"] = rc; self.save_state()
            if rc is not None and rc != 0: raise RuntimeError(f"run_set.sh exited with {rc} before the production solves started (see {log})")
            up = [os.path.exists(f"{c}/log.simpleFoam") and re.search(r"^Time = 1\s*$", read(f"{c}/log.simpleFoam"), re.M) for c in (self.les, self.ref)]
            if all(up): break
            if rc is not None: raise RuntimeError(f"run_set.sh exited 0 but the production solves never started (see {log})")
            if time.time() - t0 > tmax: raise RuntimeError(f"production solves did not start within {tmax/60:g} min (see {log}); run_set.sh left running")
        w = subprocess.Popen(wargv, cwd=ROOT, stdout=open(wlog, "w"), stderr=subprocess.STDOUT, env=self.env, start_new_session=True, stdin=subprocess.DEVNULL)
        self.procs["watch"] = w; L["watch"] = dict(proc_ident(w.pid), log=wlog, rc=None); self.save_state()
        self.note(f"solves started after {round((time.time() - t0) / 60, 1)} min; run_set pid {p.pid}, watcher pid {w.pid}")

    def alive(self, key):
        """Child of this invocation: poll() (reaps it, records the exit code). Otherwise the recorded identity (pid + start time + cmdline, not a zombie)."""
        L = self.state.get("launch") or {}; p = self.procs.get(key)
        if p is not None:
            rc = p.poll()
            if rc is not None and L.get(key, {}).get("rc") != rc: L[key]["rc"] = rc; self.save_state()
            return rc is None
        return proc_alive(L.get(key))

    def watch(self):
        tmax = 3600 * float(self.spec.get("watch_timeout_h", 8)); t0 = time.time()
        if self.dry: self.note("dry run"); return
        L = self.state.get("launch")
        if not L: self.note("no launch recorded in the state file: no watcher or launcher to track; waiting for both logs to finish")
        L = L or {}; wlog = (L.get("watch") or {}).get("log"); said = set()
        while True:
            wa, ra = self.alive("watch"), self.alive("run_set")          # sampled BEFORE the logs: a launcher that has exited has already let the logs end
            done = finished(self.les) and finished(self.ref)
            if done and not wa and not ra: break
            if not done:
                rs = L.get("run_set") or {}
                if not ra and ("run_set" in self.procs or rs.get("start")):
                    raise RuntimeError(f"run_set.sh (which waits for both solves) has exited (exit code {rs.get('rc') if rs.get('rc') is not None else 'unknown: not a child of this invocation'}) "
                                       f"and the logs have not finished (see {rs.get('log')})")
                if not wa:
                    if wlog and os.path.exists(wlog) and "STALLED/TERMINATED" in read(wlog): raise RuntimeError(f"the watcher reports a stalled/terminated solve (see {wlog})")
                    wrc = (L.get("watch") or {}).get("rc")
                    msg = ("watcher exited 0 (stop requested): waiting for the solves to finalise" if wrc == 0 else
                           f"watcher not running (exit code {wrc if wrc is not None else 'unknown: lost, not recorded or not a child of this invocation'}) and the solves "
                           f"have not finished: the runner never kills a solve; waiting for their natural completion by polling the logs (timeout {tmax/3600:g} h)")
                    if msg not in said: said.add(msg); self.note(msg)
            if time.time() - t0 > tmax: raise RuntimeError(f"solves not finished after {tmax/3600:g} h (they are left running)")
            time.sleep(POLL_S or 60)
        rc = {k: (L.get(k) or {}).get("rc") for k in ("run_set", "watch")}
        self.cur["exit_codes"] = {k: (v if v is not None else "unknown (not a child of this invocation)") for k, v in rc.items()}
        self.manifest["solves"] = {os.path.basename(c): solve_minutes(c, L.get("time")) for c in (self.les, self.ref)}
        self.note(f"final iterations: les {last_iteration(self.les)}, ref {last_iteration(self.ref)}; exit codes {self.cur['exit_codes']}; solves {self.manifest['solves']}")
        for k, v in rc.items():
            if v not in (None, 0): raise RuntimeError(f"{k} exited with {v} (see {(L.get(k) or {}).get('log')})")

    def times(self, case):
        """(F, t_prev, rule) with writeControl timeStep checked."""
        import hyp_compare as H
        name = os.path.basename(case); cd = read(f"{case}/system/controlDict")
        wc = H.top_level_entry(cd, "writeControl")
        if wc != "timeStep": raise RuntimeError(f"{name}: writeControl {wc!r} is not timeStep: the write times cannot be derived")
        F = last_iteration(case); wi = int(H.top_level_entry(cd, "writeInterval")); pw = int(H.top_level_entry(cd, "purgeWrite") or 0)
        tprev, rule = H.expected_prev_time(F, wi, pw)
        if tprev is None: raise RuntimeError(f"{name}: {rule}")
        return F, tprev, rule

    def verify_outputs(self, key, case, F, tprev):
        name, mode = os.path.basename(case), MODES[key]
        for t in (F, tprev):
            if not os.path.isdir(f"{case}/{t}"): raise RuntimeError(f"{name}: reconstructed time directory {t} missing")
        for f, t in ((f"sections_{mode}.json", F), (f"sections_{mode}_tprev.json", tprev), (f"wss_{mode}.json", F)):
            got = float(json.load(open(f"{case}/{f}"))["time"])
            if got != t: raise RuntimeError(f"{name}: {f} time {got} != expected {t}")
        a = json.load(open(f"{case}/analysis.json"))
        if not (a.get("last_iteration") == F == a.get("log_last_iteration")):
            raise RuntimeError(f"{name}: analysis.json last_iteration {a.get('last_iteration')} / log_last_iteration {a.get('log_last_iteration')} != final iteration {F}")
        return a

    def post(self):
        self.guard()
        if self.dry: self.note("dry run: post-processing not evaluated"); return
        self.invalidate(f"post {self.ts}")
        info = {}
        for key, case in (("lesion", self.les), ("ref", self.ref)):
            mode, name, c = MODES[key], os.path.basename(case), Q(case)
            if not finished(case): raise RuntimeError(f"{name}: solve not finished (no 'End' + 'Finalising parallel run' final block)")
            F, tprev, rule = self.times(case); NP = subdomains(case)
            procs = [s for s in os.listdir(case) if PROCDIR.match(s) and os.path.isdir(f"{case}/{s}")]
            full = sorted(procs) == sorted(f"processor{i}" for i in range(NP))
            info[name] = dict(final_iteration=F, t_prev=tprev, rule=rule, numberOfSubdomains=NP, processor_dirs_present=len(procs), reconstruction={})
            for i, t in enumerate((tprev, F)):
                d, rlog = f"{case}/{t}", f"{case}/log.reconstructPar.{t}"
                if os.path.isdir(d) and os.path.exists(rlog) and re.search(r"^End\s*$", read(rlog), re.M):
                    act = f"time {t}: reconstructed directory present with a completed log.reconstructPar.{t}: reused, not reconstructed again"
                elif full and all(os.path.isdir(f"{case}/processor{j}/{t}") for j in range(NP)):
                    self.sh("post", f"{key}_{i}", f"reconstructPar -time {t} > log.reconstructPar.{t} 2>&1", cwd=case)
                    act = f"time {t}: reconstructed from {NP} processor directories" + (" (an incomplete earlier reconstruction was overwritten)" if os.path.isdir(d) else "")
                else: raise RuntimeError(f"{name}: time {t}: {'directory present but no completed reconstruction log' if os.path.isdir(d) else 'not reconstructed'} "
                                         f"and the processor set is incomplete ({len(procs)}/{NP} with that time): cannot reconstruct")
                info[name]["reconstruction"][str(t)] = act; self.note(f"{name}: {act}")
            self.sh("post", f"{key}_2", f"python3 lesion_sections.py {c} {mode} {tprev} > {Q(f'{case}/log.sections.{tprev}')} 2>&1", foam=False)
            for ext in ("csv", "json"): shutil.copy(f"{case}/sections_{mode}.{ext}", f"{case}/sections_{mode}_tprev.{ext}")
            self.sh("post", f"{key}_3", f"python3 lesion_sections.py {c} {mode} {F} > {Q(f'{case}/log.sections.{F}')} 2>&1", foam=False)
            self.sh("post", f"{key}_4", f"python3 reattachment_wss.py {c} {mode} {F} > {Q(f'{case}/log.wss.{F}')} 2>&1", foam=False)
            self.sh("post", f"{key}_5", f"python3 analyze_solve.py {c} --strict --json {Q(f'{case}/analysis.json')} > {Q(f'{case}/log.analyze')} 2>&1", foam=False)
            a = self.verify_outputs(key, case, F, tprev)
            info[name].update(verdict=a.get("verdict"), strict_log_finished=a.get("strict", {}).get("log_finished"), failed_checks=[k for k, v in a.get("checks", {}).items() if not v])
            if a.get("verdict") != "CONVERGED": self.note(f"{name}: analyze_solve verdict {a.get('verdict')}: recorded, not a runner failure; the comparison tool decides validity - this is NOT a successful result")
        self.cur["cases"] = info; self.state["post"] = dict(invocation=self.ts, time=time.time(), cases=info)

    def result_valid(self, since_ns=None):
        """(valid, value, reason) of result_json[valid_key]; a missing, stale (mtime_ns earlier than 'since_ns', strict, no tolerance), unreadable file or a missing key = not valid."""
        rj, vk = f"{ROOT}/{self.spec['result_json']}", self.spec["valid_key"]
        if not os.path.exists(rj): return False, None, f"{rj} missing"
        if since_ns is not None and os.stat(rj).st_mtime_ns < since_ns: return False, None, f"{rj} not written by this compare (stale: mtime_ns {os.stat(rj).st_mtime_ns} < command start {since_ns})"
        try: j = json.load(open(rj))
        except (OSError, ValueError) as e: return False, None, f"{rj} unreadable ({type(e).__name__})"
        if not isinstance(j, dict) or vk not in j: return False, None, f"key {vk!r} missing in {rj}"
        return j[vk] is True, j[vk], f"{vk} = {j[vk]!r}"

    def inputs(self):
        """sha256 of the post outputs a comparison depends on: analysis.json, sections_*.csv/json, wss_*.csv/json of both cases."""
        h = {}
        for c in (self.les, self.ref):
            if not os.path.isdir(c): continue
            for s in sorted(os.listdir(c)):
                if (s == "analysis.json" or (s.startswith(("sections_", "wss_")) and s.endswith((".csv", ".json")))) and os.path.isfile(f"{c}/{s}"):
                    h[f"{os.path.basename(c)}/{s}"] = sha256(f"{c}/{s}")
        return h

    def compare(self):
        out, rj = f"{ROOT}/{self.spec['out']}", f"{ROOT}/{self.spec['result_json']}"
        cmd = self.spec["compare"].format(lesion=Q(self.les), ref=Q(self.ref), out=Q(out))
        if not self.dry:
            self.state["compare_evidence_valid"] = False; self.state.pop("compare", None); self.save_state()   # the old record is superseded whatever happens now
            h0 = self.inputs(); marker = f"{self.logdir}/compare_0.started"
            open(marker, "w").close(); t0 = os.stat(marker).st_mtime_ns   # command start on the filesystem clock that stamps result_json
        rc = self.sh("compare", 0, cmd, foam=False, check=False)
        if self.dry: self.note("dry run: result not evaluated"); return
        valid, value, why = self.result_valid(since_ns=t0); h1 = self.inputs()
        st = os.stat(rj) if os.path.exists(rj) else None
        rec = self.cur["compare"] = dict(invocation=self.ts, time=time.time(), rc=rc, command_start_mtime_ns=t0, result_json=rj,
                                         result_sha256=sha256(rj) if st else None, result_mtime_ns=st.st_mtime_ns if st else None,
                                         valid_key=self.spec["valid_key"], value=value, valid=valid, reason=why,
                                         post_invocation=(self.state.get("post") or {}).get("invocation"), inputs_sha256=h1)
        if h1 != h0:
            rec.update(valid=False, reason=f"input artifacts changed while the compare command ran: {sorted(k for k in set(h0) | set(h1) if h0.get(k) != h1.get(k))}")
        self.state["compare"] = rec; self.state["compare_evidence_valid"] = rc == 0 and rec["valid"] is True; self.save_state()
        if h1 != h0: raise RuntimeError(rec["reason"])
        if rc != 0: raise RuntimeError(f"compare command exited {rc} ({why}; see {self.cur['commands'][-1]['log']})")
        self.note(f"pair {'VALID' if valid else 'NOT VALID'}: {why}; result sha256 {rec['result_sha256']}")

    def cleanup(self):
        self.guard()
        if self.dry: self.note("dry run: gates not evaluated, nothing deleted"); return
        C, P = self.state.get("compare"), self.state.get("post")
        if not C or C.get("rc") != 0 or C.get("valid") is not True or C.get("value") is not True:
            raise RuntimeError(f"refused: no successful compare with a VALID pair recorded ({C and {k: C.get(k) for k in ('rc', 'valid', 'value', 'reason')}}); processor directories kept")
        if self.state.get("compare_evidence_valid") is not True:
            raise RuntimeError(f"refused: the recorded compare evidence is superseded ({C.get('superseded_by') or 'compare_evidence_valid not set'}); processor directories kept")
        if not P or C["time"] < P["time"] or C.get("post_invocation") != P.get("invocation"):
            raise RuntimeError(f"refused: the recorded compare (of post {C.get('post_invocation')}) does not belong to the recorded post stage ({P and P.get('invocation')})")
        rj = f"{ROOT}/{self.spec['result_json']}"
        if C.get("result_json") != rj: raise RuntimeError(f"refused: recorded result {C.get('result_json')} is not the spec's {rj}")
        cur = sha256(rj) if os.path.isfile(rj) else None
        if not C.get("result_sha256") or cur != C["result_sha256"]:
            raise RuntimeError(f"refused: {rj} sha256 {cur} != recorded {C.get('result_sha256')} (not the compared artifact); processor directories kept")
        valid, _, why = self.result_valid()
        if not valid: raise RuntimeError(f"refused: {why} now; processor directories kept")
        h = self.inputs(); rec = C.get("inputs_sha256") or {}
        diff = sorted(k for k in set(h) | set(rec) if h.get(k) != rec.get(k))
        if not rec or diff: raise RuntimeError(f"refused: input artifacts differ from those compared: {diff or 'none recorded'}; processor directories kept")
        plan = {}
        for key, case in (("lesion", self.les), ("ref", self.ref)):
            name = os.path.basename(case); pc = (P.get("cases") or {}).get(name)
            if not pc: raise RuntimeError(f"refused: {name} not in the recorded post stage")
            F, tprev, _ = self.times(case)
            if (F, tprev) != (pc["final_iteration"], pc["t_prev"]): raise RuntimeError(f"refused: {name} final/previous times {F}/{tprev} differ from the post record")
            self.verify_outputs(key, case, F, tprev)
            NP = subdomains(case); ents = sorted(s for s in os.listdir(case) if s.startswith("processor"))
            odd = [s for s in ents if not PROCDIR.match(s) or os.path.islink(f"{case}/{s}") or not os.path.isdir(f"{case}/{s}")]
            if odd: raise RuntimeError(f"refused: {name}: unexpected processor* entries {odd}")
            idx = sorted(int(s[9:]) for s in ents); started = ((self.state.get("cleanup") or {}).get(name) or {}).get("started")
            if idx and (idx[-1] >= NP or (len(idx) != NP and not started)):
                raise RuntimeError(f"refused: {name}: {len(idx)} processor directories (max index {idx[-1]}) vs numberOfSubdomains {NP} and no interrupted cleanup recorded")
            plan[name] = (case, ents, NP, started)
        for name, (case, ents, NP, started) in plan.items():
            if not ents: self.note(f"{name}: no processor directories left (already cleaned)"); continue
            self.state.setdefault("cleanup", {})[name] = dict(started=True, invocation=self.ts, time=time.time()); self.save_state()
            for s in ents: shutil.rmtree(f"{case}/{s}")
            self.state["cleanup"][name]["done"] = True; self.save_state()
            self.note(f"{name}: deleted {len(ents)} processor directories" + (f" (the rest of a set of {NP} whose deletion was interrupted)" if len(ents) != NP else ""))

def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    spec_path = sys.argv[1]; stages = ALL[:]; dry = False
    for a in sys.argv[2:]:
        if a.startswith("--stages="): stages = a.split("=", 1)[1].split(",")
        elif a == "--dry-run": dry = True
        else: raise SystemExit(f"unknown argument {a!r}")
    unknown = [s for s in stages if s not in ALL]
    if unknown: raise SystemExit(f"unknown stage(s) {unknown}; expected {ALL}")
    spec = json.load(open(spec_path))
    if not isinstance(spec, dict): raise SystemExit("spec must be a json object")
    err = validate(spec)
    if err: raise SystemExit("invalid spec (nothing executed):\n  " + "\n  ".join(err))
    lock(spec["name"])                                         # every invocation, for its whole life, before the state file is read
    R = Run(spec, spec_path, stages, dry)
    for name in ALL: R.stage(name, getattr(R, name))
    post, cmp_ = R.state.get("post") or {}, R.state.get("compare") or {}
    verdicts = {n: c.get("verdict") for n, c in (post.get("cases") or {}).items()}
    ok = not dry and all(v == "CONVERGED" for v in verdicts.values()) and len(verdicts) == 2 and cmp_.get("valid") is True
    R.manifest.update(finished=time.strftime("%Y-%m-%d %H:%M:%S"), verdicts=verdicts, pair_valid=cmp_.get("valid"),
                      outcome="valid converged pair compared" if ok else "requested stages completed; NOT a validated result (dry run, stages missing, UNCONVERGED or pair not valid)")
    R.save()
    print(json.dumps({s["stage"]: (s["status"], s["minutes"]) for s in R.manifest["stages"]}), "| verdicts:", verdicts, "| pair valid:", cmp_.get("valid"), "|", R.manifest["outcome"])
    print("manifest:", R.mpath, "| interactive_steps:", R.manifest["interactive_steps"])

if __name__ == "__main__":
    main()
