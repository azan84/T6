#!/usr/bin/env python3
"""Job pool for the 2026-10-03 work order (Tasks A, B, P5): starts jobs from jobs/*.json when (a) the audit marker jobs/<name>.audited exists (both auditors have cleared the setup),
(b) all jobs named in `after` finished OK (status 'done'), (c) free ranks (sum of ranks of running jobs + this job <= RANKS, default 16 = physical cores),
RAM (declared ram_gb of the running jobs + this job <= MemTotal*0.85 - RESERVE_GB, and MemAvailable >= 0.6*ram_gb + 2) and disk (free space of the jobs dir's filesystem >= disk_gb + 10) allow it.
Highest priority (lowest number) first; a job that does not fit never blocks a lower-priority job that does. Job file: {"name","ranks","ram_gb","disk_gb","priority","cmd","after":[...]};
a job file missing name/ranks/ram_gb/cmd, with wrong types, an `after` element that is not a job-name string, or whose name is not the file name (so names are unique) is rejected (logged once per file version).
Admission (in this order, each file written atomically): (1) jobs/<name>.admit = {"ranks","ram_gb","cmd","token","admitted","boot_id"}: the IMMUTABLE record of the admitted resources
(recovery uses only these, never the possibly edited manifest); (2) status 'starting'; (3) spawn of the wrapper (`pool.py --wrap`) in its own session (setsid) with env POOL_JOB_TOKEN=<token>.
The wrapper writes jobs/<name>.pid = {"pid","sid","start","boot_id","token"} ITSELF before it runs `bash -c cmd`, then jobs/<name>.rc (exit code) when the command ends. The pool sets 'running'
once the .pid exists. Status: jobs/<name>.status = starting|running|done|failed rc=N|failed rc=lost|failed rc=spawn; jobs/<name>.log. No job is ever killed by the pool.
Liveness of a job whose wrapper is not the pool's own child (after a pool restart): same boot AND (the .pid process exists with the recorded start time and is its own session leader, OR
(leader gone) a process of that session still exists (Linux does not reuse a pid while its session has members), OR any process carries POOL_JOB_TOKEN=<token> in its environment).
Restart after a pool crash / reboot, for each status 'starting' or 'running': (1) finished from its .rc file if that exists; (2) re-adopted with the ranks/RAM of its .admit if alive;
(3) 'starting' without a .pid and admitted < START_GRACE s ago (default 120) in this boot: kept as alive/unknown (resources stay committed) until the .pid appears or the grace expires;
(4) otherwise 'failed rc=lost'. A 'starting'/'running' status WITHOUT an .admit record (a job of the old pool.py) makes the pool refuse to start (replace the old pool only when no pool job runs).
Only one pool runs per jobs dir (flock on jobs/.pool.lock).
usage: pool.py [--ranks 16] [--reserve-gb 3] [--jobs-dir DIR] [--poll 30] [--start-grace 120]   (runs until jobs/STOP exists)
Tests only: env POOL_MEMINFO = alternative meminfo file; POOL_TEST_CRASH=before_spawn|after_spawn = os._exit(9) of the pool right before / after the spawn of the first admitted job."""
import json, os, subprocess, sys, time, glob, re, fcntl, uuid
D = os.path.dirname(os.path.abspath(__file__)); J = D + "/jobs"; RANKS = 16; RESERVE = 3.0; POLL = 30.0; START_GRACE = 120.0
NAME = re.compile(r"[A-Za-z0-9_.-]+")
for i, a in enumerate(sys.argv):
    if a == "--ranks": RANKS = int(sys.argv[i + 1])
    if a == "--reserve-gb": RESERVE = float(sys.argv[i + 1])
    if a == "--jobs-dir": J = os.path.abspath(sys.argv[i + 1])
    if a == "--poll": POLL = float(sys.argv[i + 1])
    if a == "--start-grace": START_GRACE = float(sys.argv[i + 1])
LOG = J + "/pool.log" if J != D + "/jobs" else D + "/pool.log"
MEMINFO = os.environ.get("POOL_MEMINFO", "/proc/meminfo")
def meminfo(k): return int(re.search(rf"{k}:\s+(\d+)", open(MEMINFO).read()).group(1)) / 2 ** 20
def memavail_gb(): return meminfo("MemAvailable")
def disk_free_gb(): s = os.statvfs(J); return s.f_bavail * s.f_frsize / 2 ** 30
def log(m):
    with open(LOG, "a") as fh: fh.write(time.strftime("%F %T ") + m + "\n")
def wr(path, txt):
    tmp = f"{path}.tmp{os.getpid()}"
    with open(tmp, "w") as fh: fh.write(txt); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)
def status(n):
    try: return open(f"{J}/{n}.status").read().strip()
    except OSError: return None
def read_json(path):
    try: return json.load(open(path))
    except (OSError, ValueError): return None
def boot_id():
    try: return open("/proc/sys/kernel/random/boot_id").read().strip()
    except OSError: return "?"
def stat_fields(pid):
    """fields 3.. of /proc/<pid>/stat (index 0 = state, 3 = session id, 19 = start time in jiffies), or None if the process does not exist."""
    try: return open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()
    except (OSError, IndexError): return None
def proc_start(pid):
    f = stat_fields(pid)
    return int(f[19]) if f else None
def pids(): return [int(p) for p in os.listdir("/proc") if p.isdigit()]
def token_alive(token):
    key = f"POOL_JOB_TOKEN={token}".encode() + b"\0"
    for p in pids():
        try:
            if key in open(f"/proc/{p}/environ", "rb").read(): return True
        except OSError: pass
    return False
def job_alive(adm, rec):
    """True if a process of the job may exist (see the module doc). adm: .admit record (required); rec: .pid record or None."""
    if adm.get("boot_id") != boot_id(): return False
    if rec and rec.get("boot_id") == adm["boot_id"] and rec.get("token") == adm["token"]:
        pid = int(rec["pid"]); f = stat_fields(pid)
        if f is not None:
            if int(f[19]) == rec["start"] and int(f[3]) == pid: return True      # the leader itself: same pid, same start time, session leader
        else:
            for p in pids():      # leader gone: members of its session (the pid is not reused while they exist)
                g = stat_fields(p)
                if g is not None and int(g[3]) == pid: return True
    return token_alive(adm["token"])
def rc_file(n):
    try: return int(open(f"{J}/{n}.rc").read().strip())
    except (OSError, ValueError): return None
def finish(n, rc):
    wr(f"{J}/{n}.status", "done" if rc == 0 else f"failed rc={rc}"); log(f"{n} finished rc={rc}")

def valid(j, f):
    ok = (isinstance(j, dict) and isinstance(j.get("name"), str) and NAME.fullmatch(j["name"]) and os.path.basename(f) == j["name"] + ".json"
          and isinstance(j.get("ranks"), int) and not isinstance(j["ranks"], bool) and j["ranks"] >= 1 and isinstance(j.get("ram_gb"), (int, float)) and not isinstance(j["ram_gb"], bool) and j["ram_gb"] >= 0
          and isinstance(j.get("cmd"), str) and isinstance(j.get("disk_gb", 5), (int, float)) and isinstance(j.get("priority", 5), (int, float))
          and isinstance(j.get("after", []), list) and all(isinstance(a, str) and NAME.fullmatch(a) and a != j["name"] for a in j.get("after", [])))
    return bool(ok)

warned = set()
def warn_once(key, m):
    if key not in warned: warned.add(key); log(m)
def load_jobs():
    jobs = {}
    for f in sorted(glob.glob(J + "/*.json")):
        try: mt = os.path.getmtime(f); j = json.load(open(f))
        except Exception as e: warn_once(("bad", f), f"bad job file {f}: {e}"); continue
        if not valid(j, f): warn_once(("invalid", f, mt), f"invalid job file {f} (needs name == file name, int ranks >= 1, ram_gb >= 0, cmd str; optional disk_gb, priority, after = list of job-name strings): rejected"); continue
        jobs[j["name"]] = j
    return jobs

def wrap(jdir, n):
    """the job's wrapper (session leader): writes <n>.pid itself, runs the command, writes <n>.rc."""
    adm = json.load(open(f"{jdir}/{n}.admit")); pid = os.getpid()
    rec = dict(pid=pid, sid=os.getsid(0), start=proc_start(pid), boot_id=boot_id(), token=adm["token"])
    if rec["sid"] != pid: sys.exit(f"pool wrapper {n}: not a session leader")
    wr(f"{jdir}/{n}.pid", json.dumps(rec))
    rc = subprocess.call(["bash", "-c", adm["cmd"]], stdin=subprocess.DEVNULL)
    rc = 128 - rc if rc < 0 else rc      # killed by a signal -> 128 + signal, as bash
    wr(f"{jdir}/{n}.rc", f"{rc}\n"); sys.exit(rc)

def main():
    os.makedirs(J, exist_ok=True)
    lk = open(J + "/.pool.lock", "w")
    try: fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: sys.exit(f"pool.py: another pool is running on {J}")
    BUDGET = meminfo("MemTotal") * 0.85 - RESERVE
    procs = {}      # name -> dict(p=Popen or None (adopted), adm=.admit record, rec=.pid record or None)
    # restart recovery: refuse legacy records first (nothing is changed then)
    active = sorted(os.path.basename(sf)[:-7] for sf in glob.glob(J + "/*.status") if status(os.path.basename(sf)[:-7]) in ("starting", "running"))
    legacy = [n for n in active if read_json(f"{J}/{n}.admit") is None]
    if legacy:
        log(f"pool refuses to start: jobs {legacy} have status starting/running but no .admit record (old pool.py?); their processes cannot be verified. Replace the old pool only when no pool job runs.")
        sys.exit(f"pool.py: jobs {legacy} have status starting/running without an .admit record; refusing to start")
    log(f"pool start ranks={RANKS} reserve={RESERVE} ram budget {BUDGET:.1f} GB start grace {START_GRACE:g} s jobs {J}")
    for n in active:
        adm = read_json(f"{J}/{n}.admit"); rec = read_json(f"{J}/{n}.pid"); rc = rc_file(n)
        if rc is not None: finish(n, rc); log(f"{n}: recovered from its .rc file after a pool restart"); continue
        young = status(n) == "starting" and rec is None and adm.get("boot_id") == boot_id() and time.time() - adm["admitted"] < START_GRACE
        if job_alive(adm, rec) or young:
            procs[n] = dict(p=None, adm=adm, rec=rec)
            log(f"{n}: {'alive' if rec else 'starting, no .pid yet (alive/unknown)'} after a pool restart: re-adopted, ranks={adm['ranks']} ram={adm['ram_gb']} (from its .admit) committed")
        else: wr(f"{J}/{n}.status", "failed rc=lost"); log(f"{n}: status {status(n)} but no process (pool crash/reboot): marked failed rc=lost")
    crash = os.environ.get("POOL_TEST_CRASH")
    while not os.path.exists(J + "/STOP"):
        for n, r in list(procs.items()):
            if r["rec"] is None:
                r["rec"] = read_json(f"{J}/{n}.pid")
                if r["rec"] is not None and status(n) == "starting": wr(f"{J}/{n}.status", "running"); log(f"{n}: running (pid {r['rec']['pid']})")
            if r["p"] is not None: rc = r["p"].poll()
            else:
                rc = rc_file(n)
                if rc is None and not job_alive(r["adm"], r["rec"]):
                    if r["rec"] is None and r["adm"].get("boot_id") == boot_id() and time.time() - r["adm"]["admitted"] < START_GRACE: continue      # alive/unknown
                    wr(f"{J}/{n}.status", "failed rc=lost"); log(f"{n}: adopted job has no process and no rc file: failed rc=lost"); del procs[n]; continue
            if rc is not None: finish(n, rc); del procs[n]
        jobs = load_jobs()
        used = sum(r["adm"]["ranks"] for r in procs.values()); ram_committed = sum(r["adm"]["ram_gb"] for r in procs.values())
        for j in sorted(jobs.values(), key=lambda j: (j.get("priority", 5), j["name"])):
            n = j["name"]
            if n in procs or status(n) is not None: continue
            if not os.path.exists(f"{J}/{n}.audited"): continue
            bad = [a for a in j.get("after", []) if status(a) not in (None, "starting", "running", "done")]
            if bad: warn_once(("dep", n, tuple(bad)), f"{n}: blocked, dependency failed: {[(a, status(a)) for a in bad]} (the pool will not start it)"); continue
            if any(status(a) != "done" for a in j.get("after", [])): continue
            if used + j["ranks"] > RANKS: continue
            # RAM: declared ram_gb of the running jobs + this job must fit the budget (MemTotal*0.85 - RESERVE), and MemAvailable must cover the job's start-up now
            if ram_committed + j["ram_gb"] > BUDGET: warn_once(("ram", n, ram_committed), f"{n}: waits, committed {ram_committed} + {j['ram_gb']} GB > budget {BUDGET:.1f} GB"); continue
            if memavail_gb() < j["ram_gb"] * 0.6 + 2.0: continue
            if disk_free_gb() < j.get("disk_gb", 5) + 10: continue
            for x in (".rc", ".pid"):
                try: os.remove(f"{J}/{n}{x}")
                except FileNotFoundError: pass
            adm = dict(ranks=j["ranks"], ram_gb=j["ram_gb"], cmd=j["cmd"], token=uuid.uuid4().hex, admitted=time.time(), boot_id=boot_id())
            wr(f"{J}/{n}.admit", json.dumps(adm))      # immutable admission record, BEFORE the status and the spawn
            wr(f"{J}/{n}.status", "starting")
            if crash == "before_spawn": os._exit(9)
            try:
                with open(f"{J}/{n}.log", "a") as lf:
                    p = subprocess.Popen([sys.executable, os.path.abspath(__file__), "--wrap", J, n], stdout=lf, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                         start_new_session=True, env=dict(os.environ, POOL_JOB_TOKEN=adm["token"]))
            except OSError as e:
                wr(f"{J}/{n}.status", "failed rc=spawn"); log(f"{n}: spawn failed: {e}"); continue
            if crash == "after_spawn": os._exit(9)
            procs[n] = dict(p=p, adm=adm, rec=None); used += j["ranks"]; ram_committed += j["ram_gb"]
            log(f"started {n} ranks={j['ranks']} ram={j['ram_gb']} (used ranks {used}/{RANKS}, committed RAM {ram_committed}/{BUDGET:.1f} GB, MemAvailable {memavail_gb():.1f} GB, disk {disk_free_gb():.0f} GB)")
        time.sleep(POLL)
    log(f"pool stop requested; running jobs are left running: {sorted(procs)}")

if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--wrap": wrap(sys.argv[2], sys.argv[3])
    else: main()
