"""Task 4 isolation evidence (stdlib only; called by task4_run.sh, design task4_design.md v1.3).
  winprecheck <out.json> <seconds>          Windows per-process CPU over <seconds> (two Get-Process snapshots inside ONE powershell.exe call); exit 0 pass, 3 load, 4 unavailable.
  sample <mpirun_pid> <runner_pid> <case_dir> <interval_s> <win_every_s>
                                            in-run sampler: isolation_samples.csv (+ windows_snapshots.log, rank_affinity.txt); exits by itself when mpirun (or the runner) is gone.
  evidence <case_dir>                       post-run isolation_evidence.json with the summary `contended` (no / yes / unknown).
Windows side: powershell.exe (env TASK4_POWERSHELL overrides the path; test hook). Excluded from the Windows load: vmmemWSL, vmmem, System, Idle and the querying powershell process itself.
Get-Process returns no CPU for processes the (non-admin) user cannot open; they are counted (null_cpu_processes) but their load is invisible: stated in the evidence."""
import sys, os, json, time, subprocess, re, glob

PS = os.environ.get("TASK4_POWERSHELL", "powershell.exe")
WIN_EXCLUDE = {"vmmemwsl", "vmmem", "system", "idle"}
WIN_PROC_MAX, WIN_SUM_MAX = 0.25, 0.5          # cores: one Windows process / sum of all non-excluded ones
LIN_MEAN_MAX, LIN_MAX_MAX = 0.25, 1.0          # cores: non-owned Linux CPU busy over the run, mean / max of the 5-s samples
SIB_MEAN_MAX, SIB_MAX_MAX = 0.10, 0.5          # cores: non-owned work on the bound cores' logical CPUs (incl. SMT siblings), attributed by each process's last CPU
# /proc/stat is only a cross-check: this WSL2 kernel uses tick-sampled CPU accounting (CONFIG_TICK_CPU_ACCOUNTING) and in tests its busy total disagreed with the
# per-process (sum_exec_runtime based) accounting in both directions (0.26 vs 1.0 core, 0.85 vs 0.06 core over 3-4 s); the criterion uses per-process deltas.
TCK = os.sysconf("SC_CLK_TCK")

PS_DELTA = r"""#T4MODE=delta
$ErrorActionPreference='SilentlyContinue'; $N=__N__
$a=@{}; foreach($p in Get-Process){ $a[$p.Id]=@($p.Name,$p.CPU) }
$sw=[Diagnostics.Stopwatch]::StartNew(); $tot=$null
try { $tot=(Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples $N -ErrorAction Stop).CounterSamples.CookedValue } catch { }
$rest=$N-$sw.Elapsed.TotalSeconds; if ($rest -gt 0) { Start-Sleep -Milliseconds ([int]($rest*1000)) }
$b=Get-Process; $el=$sw.Elapsed.TotalSeconds
"ELAPSED`t$el"; "SELF`t$PID"; if ($tot) { "TOTALPCT`t" + (($tot | Measure-Object -Average).Average) }
$nul=0
foreach($p in $b){ if ($p.CPU -eq $null) { $nul++; continue }; $o=$a[$p.Id]; if ($o -ne $null -and $o[0] -eq $p.Name -and $o[1] -ne $null) { $d=$p.CPU-$o[1]; $n=0 } else { $d=$p.CPU; $n=1 }; "D`t$($p.Name)`t$($p.Id)`t$d`t$n" }
"NULLCPU`t$nul"
"""
PS_SNAP = r"""#T4MODE=snap
$ErrorActionPreference='SilentlyContinue'; "SELF`t$PID"; $nul=0
foreach($p in Get-Process){ if ($p.CPU -eq $null) { $nul++; continue }; "S`t$($p.Name)`t$($p.Id)`t$($p.CPU)" }
"NULLCPU`t$nul"
"""

def _ps(script, timeout):
    try:
        r = subprocess.run([PS, "-NoProfile", "-NonInteractive", "-Command", script], capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"{PS}: {e}"
    if r.returncode != 0: return None, f"{PS} rc {r.returncode}: {r.stderr.strip()[:300]}"
    return r.stdout.replace("\r", ""), ""

def _csvfield(v):
    """One field of isolation_samples.csv: process names may contain commas or newlines (Windows names, Linux comm)."""
    return v.replace(",", ";").replace("\r", " ").replace("\n", " ")

def _excluded(name, pid, selfpid): return name.lower() in WIN_EXCLUDE or pid == selfpid

def win_delta(seconds):
    """One powershell call: CPU seconds per process over `seconds`. Returns dict (status pass/load/unavailable)."""
    out, err = _ps(PS_DELTA.replace("__N__", str(int(seconds))), seconds + 60)
    if out is None: return dict(status="unavailable", error=err)
    kv = {}; procs = []
    for ln in out.splitlines():
        p = ln.split("\t")
        if p[0] == "D" and len(p) == 5:
            try: procs.append(dict(name=p[1], pid=int(p[2]), cpu_s=float(p[3]), new=p[4] == "1"))
            except ValueError: pass
        elif len(p) == 2: kv[p[0]] = p[1]
    try: el = float(kv["ELAPSED"]); selfpid = int(kv["SELF"])
    except (KeyError, ValueError): return dict(status="unavailable", error="unparseable powershell output: " + out[:300])
    others = [dict(q, cores=q["cpu_s"] / el) for q in procs if not _excluded(q["name"], q["pid"], selfpid)]
    excl = {q["name"]: round(q["cpu_s"] / el, 3) for q in procs if _excluded(q["name"], q["pid"], selfpid)}
    others.sort(key=lambda q: -q["cores"]); tot = sum(q["cores"] for q in others)
    off = [q for q in others if q["cores"] > WIN_PROC_MAX]
    status = "load" if off or tot > WIN_SUM_MAX else "pass"
    return dict(status=status, window_s=el, sum_nonexcluded_cores=round(tot, 4), max_process_cores=round(others[0]["cores"], 4) if others else 0.0,
                offenders=[f"{q['name']}({q['pid']}) {q['cores']:.3f} cores" for q in off], top10=[f"{q['name']}({q['pid']}) {q['cores']:.3f}" for q in others[:10]],
                excluded_cores=excl, null_cpu_processes=int(kv.get("NULLCPU", -1)), processor_total_pct_incl_wsl=float(kv["TOTALPCT"]) if "TOTALPCT" in kv else None,
                thresholds=f"refuse if one process > {WIN_PROC_MAX} core or the sum > {WIN_SUM_MAX} core (excluded: vmmemWSL, vmmem, System, Idle, the querying powershell)")

def win_snap():
    out, err = _ps(PS_SNAP, 60)
    if out is None: return None, err
    selfpid = None; d = {}
    for ln in out.splitlines():
        p = ln.split("\t")
        if p[0] == "SELF": selfpid = int(p[1])
        elif p[0] == "S" and len(p) == 4:
            try: d[int(p[2])] = (p[1], float(p[3]))
            except ValueError: pass
    if selfpid is None: return None, "unparseable powershell output"
    return (time.monotonic(), selfpid, d), ""

def snap_delta(a, b):
    """Non-excluded Windows CPU (cores) between two snapshots; processes new in b count with their full CPU."""
    el = b[0] - a[0]; tot = 0.0; top = ("", 0.0)
    for pid, (name, cpu) in b[2].items():
        if _excluded(name, pid, b[1]) or pid == a[1]: continue
        o = a[2].get(pid); d = cpu - o[1] if o and o[0] == name else cpu
        tot += max(d, 0.0)
        if d > top[1]: top = (f"{name}({pid})", d)
    return tot / el, _csvfield(f"{top[0]} {top[1] / el:.3f}")      # written to the CSV column win_top

def _stat(pid):
    try: s = open(f"/proc/{pid}/stat").read()
    except OSError: return None
    r = s[s.rindex(")") + 2:].split()      # fields from 3 (state) on
    return dict(ppid=int(r[1]), sid=int(r[3]), cpu=int(r[11]) + int(r[12]), ccpu=int(r[13]) + int(r[14]), last_cpu=int(r[36]), comm=s[s.index("(") + 1:s.rindex(")")])

def _procs():
    return {int(p): st for p in os.listdir("/proc") if p.isdigit() for st in [_stat(p)] if st}

def _descendants(root, pr):
    kids = {}
    for p, st in pr.items(): kids.setdefault(st["ppid"], []).append(p)
    out, todo = set(), [root]
    while todo:
        p = todo.pop(); out.add(p); todo += kids.get(p, [])
    return out

def _cpustat():
    d = {}
    for ln in open("/proc/stat"):
        if ln.startswith("cpu"):
            f = ln.split(); v = [int(x) for x in f[1:]]
            d[f[0]] = (v[0] + v[1] + v[2] + v[5] + v[6], v[7] if len(v) > 7 else 0)   # busy = user+nice+system+irq+softirq; steal separately
    return d

def _cpulist(s):
    out = set()
    for part in s.strip().split(","):
        if "-" in part: a, b = part.split("-"); out |= set(range(int(a), int(b) + 1))
        elif part: out.add(int(part))
    return out

def _psi():
    try: return int(re.search(r"some .*total=(\d+)", open("/proc/pressure/cpu").read()).group(1))
    except (OSError, AttributeError): return None

def _memavail():
    for ln in open("/proc/meminfo"):
        if ln.startswith("MemAvailable:"): return int(ln.split()[1]) / 1024
    return None

def _mhz():
    return [float(x) for x in re.findall(r"^cpu MHz\s*:\s*([0-9.]+)", open("/proc/cpuinfo").read(), re.M)]

def _alive(pid):
    try: os.kill(pid, 0); return True
    except ProcessLookupError: return False
    except PermissionError: return True

def sample(mp, runner, case, interval, win_every):
    """Every `interval` s one CSV row; every `win_every` s one Windows snapshot (a powershell.exe call, ~1 s and a small CPU cost of its own,
    which is Windows-side and excluded as the querying process; its Linux-side interop process is a child of this sampler, i.e. owned)."""
    me = os.getpid(); f = open(os.path.join(case, "isolation_samples.csv"), "w", buffering=1)
    wlog = open(os.path.join(case, "windows_snapshots.log"), "w", buffering=1); afile = os.path.join(case, "rank_affinity.txt")
    f.write("epoch,elapsed_s,owned_cores,nonowned_linux_cores,nonowned_top,procstat_busy_cores,procstat_minus_perprocess_cores,bound_cpus_nonowned_cores,"
            "bound_cpus_procstat_minus_ranks_cores,steal_cores,psi_cpu_some_total_us,psi_cpu_some_frac,memavailable_mb,bound_cpu_mhz_mean,win_nonwsl_cores,win_top\n")
    t_start = time.monotonic(); ranks = {}; prev = None; wprev = None; wnext = 0.0
    fmt = lambda v, p: "" if v == "" or v is None else f"{v:.{p}f}"
    while True:
        alive = _alive(mp) and _alive(runner)
        now = time.monotonic(); epoch = time.time(); pr = _procs(); cs = _cpustat(); psi = _psi()
        owned = {p for p, st in pr.items() if st["sid"] == mp} | _descendants(runner, pr) | {me}
        for p in owned:                                       # rank affinity: the pimpleFoam processes of mpirun's session
            if p in pr and pr[p]["sid"] == mp and pr[p]["comm"] == "pimpleFoam" and p not in ranks:
                try: ranks[p] = re.search(r"Cpus_allowed_list:\s*(\S+)", open(f"/proc/{p}/status").read()).group(1)
                except (OSError, AttributeError): pass
        if ranks:
            with open(afile, "w") as af: af.writelines(f"{p} pimpleFoam {cl}\n" for p, cl in sorted(ranks.items()))
        sets = {frozenset(_cpulist(cl)) for cl in ranks.values()}
        bcpus = set().union(*sets) if sets and all(len(x) < os.cpu_count() for x in sets) else set()
        sib = set(bcpus)
        for c in bcpus:
            try: sib |= _cpulist(open(f"/sys/devices/system/cpu/cpu{c}/topology/thread_siblings_list").read())
            except OSError: pass
        win = ""; wtop = ""
        if now >= wnext:
            s, err = win_snap(); wnext = now + win_every
            if s is None: wlog.write(f"{time.time():.0f} snapshot failed: {err}\n")
            else:
                if wprev is not None: v, wtop = snap_delta(wprev, s); win = f"{v:.4f}"; wlog.write(f"{time.time():.0f} nonwsl_cores {v:.4f} top {wtop}\n")
                else: wlog.write(f"{time.time():.0f} first snapshot ({len(s[2])} processes)\n")
                wprev = s
        if prev is not None:
            el = now - prev["t"]; pp = prev["pr"]
            both = [p for p in pr if p in pp and pr[p]["comm"] == pp[p]["comm"]]
            d_own = sum(pr[p]["cpu"] - pp[p]["cpu"] for p in both if p in owned) / TCK / el
            d_rank = sum(pr[p]["cpu"] - pp[p]["cpu"] for p in both if p in owned and pr[p]["sid"] == mp and p != mp) / TCK / el
            # non-owned: own CPU + CPU of children reaped in the interval (cutime/cstime), so short-lived jobs are counted too (conservative: may double count)
            dn = {p: max(pr[p]["cpu"] - pp[p]["cpu"], 0) + max(pr[p]["ccpu"] - pp[p]["ccpu"], 0) for p in both if p not in owned and p not in prev["owned"]}
            d_non = sum(dn.values()) / TCK / el; top = max(dn, key=dn.get) if dn else None
            d_sib = sum(max(pr[p]["cpu"] - pp[p]["cpu"], 0) for p in dn if pr[p]["last_cpu"] in sib) / TCK / el if sib else ""
            d_busy = (cs["cpu"][0] - prev["cs"]["cpu"][0]) / TCK / el; d_steal = (cs["cpu"][1] - prev["cs"]["cpu"][1]) / TCK / el
            d_sib_ps = (sum(cs[f"cpu{c}"][0] - prev["cs"][f"cpu{c}"][0] for c in sib if f"cpu{c}" in cs) / TCK / el - d_rank) if sib else ""
            mhz = _mhz(); bm = sum(mhz[c] for c in bcpus if c < len(mhz)) / len(bcpus) if bcpus else ""
            psif = (psi - prev["psi"]) / 1e6 / el if psi is not None and prev["psi"] is not None else ""
            f.write(",".join([f"{epoch:.0f}", f"{now - t_start:.1f}", fmt(d_own, 4), fmt(d_non, 4), _csvfield(f"{pr[top]['comm']}({top}) {dn[top] / TCK / el:.3f}") if top else "",
                              fmt(d_busy, 4), fmt(d_busy - d_own - d_non, 4), fmt(d_sib, 4), fmt(d_sib_ps, 4), fmt(d_steal, 4), "" if psi is None else str(psi), fmt(psif, 4),
                              fmt(_memavail(), 0), fmt(bm, 1), win, wtop]) + "\n")
        prev = dict(t=now, pr=pr, cs=cs, psi=psi, owned=owned)
        if not alive: break
        t_next = now + interval
        while time.monotonic() < t_next:
            time.sleep(min(1.0, max(t_next - time.monotonic(), 0)))
            if not (_alive(mp) and _alive(runner)): break     # liveness tied to mpirun (and the runner): one last row, then exit
    s, err = win_snap()                                       # closing Windows snapshot so that the in-run Windows figure covers the whole run
    if s is not None and wprev is not None:
        v, wtop = snap_delta(wprev, s); wlog.write(f"{time.time():.0f} nonwsl_cores {v:.4f} top {wtop} (closing)\n")
        f.write(f"{time.time():.0f},{time.monotonic() - t_start:.1f}," + "," * 12 + f"{v:.4f},{wtop}\n")
    elif s is None: wlog.write(f"{time.time():.0f} closing snapshot failed: {err}\n")

def _col(rows, k):
    return [float(r[k]) for r in rows if r.get(k, "") != ""]

def parse_bindings(txt):
    """OpenMPI 4.x --report-bindings: '[host:pid] MCW rank 3 bound to socket 0[core 3[hwt 0-1]]: [../../../BB/..]'."""
    lines = [l for l in txt.splitlines() if re.search(r"MCW rank \d+ bound to", l)]
    ranks = {}
    for l in lines:
        m = re.search(r"MCW rank (\d+) bound to (.*?):", l)
        cores = re.findall(r"core (\d+)\[", m.group(2)) if m else []
        if m: ranks[int(m.group(1))] = cores
    ok = len(ranks) == 8 and all(len(c) == 1 for c in ranks.values()) and len({c[0] for c in ranks.values()}) == 8
    return dict(raw_lines=lines, ranks={str(k): v for k, v in sorted(ranks.items())}, n_ranks=len(ranks),
                distinct_cores=sorted({c for v in ranks.values() for c in v}, key=int), verified=ok)

def _read(p, default=""):
    try: return open(p).read()
    except OSError: return default

def evidence(case):
    import csv
    ev = dict(schema="task4 isolation evidence v1.3", written=time.strftime("%F %T"))
    ev["lscpu"] = subprocess.run(["lscpu"], capture_output=True, text=True).stdout
    ev["numa_nodes"] = sorted(os.path.basename(n) for n in glob.glob("/sys/devices/system/node/node[0-9]*"))
    ev["topology_note"] = "guest (WSL2 / Hyper-V) topology: vCPU-to-physical-core placement is decided by the Windows hypervisor and cannot be verified from the guest"
    b = parse_bindings(_read(os.path.join(case, "mpirun_bindings.txt"))); ev["bindings_report"] = b
    aff = [l.split() for l in _read(os.path.join(case, "rank_affinity.txt")).splitlines() if len(l.split()) == 3]
    sets = sorted({frozenset(_cpulist(a[2])) for a in aff}, key=min)     # distinct rank affinity sets (a rank may fork helpers with the same set)
    core_of = {}
    for s in sets:
        for c in s:
            core_of[c] = (_read(f"/sys/devices/system/cpu/cpu{c}/topology/physical_package_id").strip(), _read(f"/sys/devices/system/cpu/cpu{c}/topology/core_id").strip())
    aff_ok = len(sets) == 8 and all(1 <= len(s) <= 2 for s in sets) and sum(len(s) for s in sets) == len(set().union(*sets)) \
        and all(len({core_of[c] for c in s}) == 1 for s in sets) \
        and len({core_of[min(s)] for s in sets}) == 8 and all(k[1] != "" for k in core_of.values())     # 8 DISTINCT physical cores; unreadable core_id -> not verified
    bound = sorted(set().union(*sets)) if sets else []
    ev["rank_affinity_observed"] = dict(lines=[" ".join(a) for a in aff], bound_logical_cpus=bound, verified=aff_ok,
                                        rule="8 rank processes, 8 disjoint Cpus_allowed_list sets, each within one core (SMT siblings), on 8 distinct (package, core_id) physical cores")
    ev["thread_siblings_list"] = {str(c): _read(f"/sys/devices/system/cpu/cpu{c}/topology/thread_siblings_list").strip() for c in bound}
    ev["bindings_verified"] = bool(b["verified"] and aff_ok)
    gov = _read("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor").strip()
    ev["governor"] = gov or "unavailable in this WSL2 guest"
    ev["frequency_note"] = "no cpufreq in the guest; /proc/cpuinfo 'cpu MHz' is sampled (bound_cpu_mhz_mean) but in WSL2 it is normally the constant nominal value, not the actual clock; turbo/power plan are not visible"
    ev["windows_prerun"] = json.loads(_read(os.path.join(case, "windows_prerun.json"), "null"))
    ev["windows_postrun"] = json.loads(_read(os.path.join(case, "windows_postrun.json"), "null"))
    rows = list(csv.DictReader(open(os.path.join(case, "isolation_samples.csv")))) if os.path.exists(os.path.join(case, "isolation_samples.csv")) else []
    lin = _col(rows, "nonowned_linux_cores"); un = _col(rows, "procstat_minus_perprocess_cores"); sib = _col(rows, "bound_cpus_nonowned_cores"); win = _col(rows, "win_nonwsl_cores")
    stat = lambda v: dict(n=len(v), mean=round(sum(v) / len(v), 4), max=round(max(v), 4)) if v else dict(n=0, mean=None, max=None)
    ev["run_linux_nonowned_cores"] = stat(lin); ev["run_procstat_minus_perprocess_cores_crosscheck"] = stat(un); ev["run_bound_cpus_nonowned_cores"] = stat(sib)
    ev["run_bound_cpus_procstat_minus_ranks_cores_crosscheck"] = stat(_col(rows, "bound_cpus_procstat_minus_ranks_cores"))
    ev["procstat_note"] = "cross-check only: tick-sampled /proc/stat in this WSL2 guest disagrees with per-process accounting in both directions; not used for `contended`"
    top = {}
    for r in rows:
        if r.get("nonowned_top"): n_, v_ = r["nonowned_top"].rsplit(" ", 1); top[n_] = max(top.get(n_, 0.0), float(v_))
    ev["run_linux_nonowned_top_processes_max_cores"] = dict(sorted(top.items(), key=lambda kv: -kv[1])[:10])
    ev["run_windows_nonwsl_cores"] = stat(win); ev["run_psi_cpu_some_frac"] = stat(_col(rows, "psi_cpu_some_frac")); ev["run_steal_cores"] = stat(_col(rows, "steal_cores"))
    ev["run_memavailable_mb_min"] = min(_col(rows, "memavailable_mb")) if _col(rows, "memavailable_mb") else None
    ev["run_bound_cpu_mhz"] = stat(_col(rows, "bound_cpu_mhz_mean"))
    sib_busy = None if not sib else (ev["run_bound_cpus_nonowned_cores"]["mean"] > SIB_MEAN_MAX or ev["run_bound_cpus_nonowned_cores"]["max"] > SIB_MAX_MAX)
    ev["sibling_of_bound_cpu_busy_with_nonowned_work"] = sib_busy
    ev["sibling_rule"] = (f"non-owned processes' CPU attributed to their last CPU (/proc/<pid>/stat field 39), summed over the bound CPUs and their SMT siblings; busy if mean > "
                          f"{SIB_MEAN_MAX} or max > {SIB_MAX_MAX} core (approximate: a process may migrate within a 5-s interval)")
    pre = ev["windows_prerun"] or {}
    yes, unk = [], []
    if pre.get("status") == "load": yes.append("windows pre-run load") if not pre.get("override") else unk.append("windows pre-run load overridden (TASK4_ALLOW_WINDOWS_LOAD=1)")
    elif pre.get("status") != "pass": unk.append(f"windows pre-run check {pre.get('status', 'missing')}")
    if not lin: unk.append("no Linux samples")
    elif ev["run_linux_nonowned_cores"]["mean"] >= LIN_MEAN_MAX or ev["run_linux_nonowned_cores"]["max"] >= LIN_MAX_MAX: yes.append("non-owned Linux CPU over threshold")
    if not win: unk.append("no in-run Windows snapshot interval")
    elif ev["run_windows_nonwsl_cores"]["mean"] >= WIN_SUM_MAX: yes.append("Windows non-WSL CPU over the run over threshold")
    if sib_busy: yes.append("non-owned work on the bound CPUs / SMT siblings")
    elif sib_busy is None: unk.append("bound-CPU occupancy not measured")
    if not ev["bindings_verified"]: unk.append("bindings not verified (report and/or observed affinity)")
    ev["contended"] = "yes" if yes else ("unknown" if unk else "no")
    ev["contended_reasons"] = yes + unk
    ev["contended_rule"] = (f"no ONLY if: pre-run Windows check passed; non-owned Linux CPU mean < {LIN_MEAN_MAX} and max < {LIN_MAX_MAX} core; Windows non-WSL CPU over the run < {WIN_SUM_MAX} core; "
                            f"no non-owned work on the bound CPUs; bindings verified. yes if a threshold is exceeded; else unknown")
    json.dump(ev, open(os.path.join(case, "isolation_evidence.json"), "w"), indent=1)
    print(f"isolation_evidence.json: contended={ev['contended']} {ev['contended_reasons']}")

if __name__ == "__main__":
    a = sys.argv
    if a[1] == "winprecheck":
        r = win_delta(float(a[3])); r["override"] = os.environ.get("TASK4_ALLOW_WINDOWS_LOAD", "0") == "1" and r["status"] == "load"
        json.dump(r, open(a[2], "w"), indent=1); print(json.dumps({k: r.get(k) for k in ("status", "sum_nonexcluded_cores", "max_process_cores", "offenders", "error")}))
        sys.exit({"pass": 0, "load": 3}.get(r["status"], 4))
    elif a[1] == "sample": sample(int(a[2]), int(a[3]), a[4], float(a[5]), float(a[6]))
    elif a[1] == "evidence": evidence(a[2])
