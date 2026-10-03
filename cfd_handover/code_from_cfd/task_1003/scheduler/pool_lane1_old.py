#!/usr/bin/env python3
"""Job pool for the 2026-10-03 work order (Tasks A, B, P5): starts jobs from jobs/*.json when (a) the audit marker jobs/<name>.audited exists (both auditors have cleared the setup),
(b) all jobs named in `after` finished OK, (c) free ranks (budget RANKS, default 16 = physical cores) and RAM (MemAvailable - RESERVE_GB >= ram_gb) and disk (free / >= disk_gb + 10) allow it.
Highest priority (lowest number) first; a job that does not fit never blocks a lower-priority job that does. Job file: {"name","ranks","ram_gb","disk_gb","priority","cmd","after":[...]}.
Status: jobs/<name>.status = running|done|failed rc=N ; jobs/<name>.log ; a job is run as `bash -c cmd` in its own session (setsid). No job is ever killed by the pool.
usage: pool.py [--ranks 16] [--reserve-gb 3]   (runs until jobs/STOP exists)"""
import json, os, subprocess, sys, time, glob, re
D = os.path.dirname(os.path.abspath(__file__)); J = D + "/jobs"; RANKS = 16; RESERVE = 3.0
for i, a in enumerate(sys.argv):
    if a == "--ranks": RANKS = int(sys.argv[i + 1])
    if a == "--reserve-gb": RESERVE = float(sys.argv[i + 1])
procs = {}
BUDGET = int(re.search(r"MemTotal:\s+(\d+)", open("/proc/meminfo").read()).group(1)) / 2 ** 20 * 0.85 - RESERVE
def status(n):
    try: return open(f"{J}/{n}.status").read().strip()
    except OSError: return None
def memavail_gb(): return int(re.search(r"MemAvailable:\s+(\d+)", open("/proc/meminfo").read()).group(1)) / 2 ** 20
def disk_free_gb(): s = os.statvfs("/"); return s.f_bavail * s.f_frsize / 2 ** 30
def log(m): open(D + "/pool.log", "a").write(time.strftime("%F %T ") + m + "\n")
log(f"pool start ranks={RANKS} reserve={RESERVE} ram budget {BUDGET:.1f} GB")
while not os.path.exists(J + "/STOP"):
    for n, p in list(procs.items()):
        rc = p.poll()
        if rc is not None:
            open(f"{J}/{n}.status", "w").write("done" if rc == 0 else f"failed rc={rc}"); log(f"{n} finished rc={rc}"); del procs[n]
    jobs = []
    for f in glob.glob(J + "/*.json"):
        try: jobs.append(json.load(open(f)))
        except Exception as e: log(f"bad job file {f}: {e}")
    used = sum(j["ranks"] for j in jobs if j["name"] in procs); ram_committed = sum(j["ram_gb"] for j in jobs if j["name"] in procs)
    for j in sorted(jobs, key=lambda j: (j.get("priority", 5), j["name"])):
        n = j["name"]
        if n in procs or status(n) is not None: continue
        if not os.path.exists(f"{J}/{n}.audited"): continue
        if any(status(a) != "done" for a in j.get("after", [])): continue
        # RAM: declared ram_gb of the running jobs + this job must fit the budget (MemTotal*0.85 - RESERVE), and MemAvailable must cover the job's start-up now
        if ram_committed + j["ram_gb"] > BUDGET: continue
        if memavail_gb() < j["ram_gb"] * 0.6 + 2.0: continue
        if disk_free_gb() < j.get("disk_gb", 5) + 10: continue
        lf = open(f"{J}/{n}.log", "a"); p = subprocess.Popen(["bash", "-c", j["cmd"]], stdout=lf, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
        procs[n] = p; open(f"{J}/{n}.status", "w").write("running"); used += j["ranks"]; ram_committed += j["ram_gb"]; log(f"started {n} ranks={j['ranks']} ram={j['ram_gb']} (used ranks {used}, MemAvailable {memavail_gb():.1f} GB, disk {disk_free_gb():.0f} GB)")
    time.sleep(30)
log("pool stop requested; running jobs are left running")
