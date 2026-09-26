"""One returns row per finished U3D level (3D or wedge): merges u3d_analyse.level() with timing/RAM/ranks, then writes/appends the CSV.
usage: u3d_make_csv.py <out.csv> <contended: yes|no|unknown> <level>...       (levels S50 S25A S12A S25B S12B W0..W4)
Timing from log.simpleFoam (last ExecutionTime/ClockTime, iteration count), ranks from decomposeParDict, physical cores 16 (host), peak RAM = max of memlog.txt 'simpleFoam_RSS_MB' between the log's start datetime (header Date/Time) and its last write (mtime); the memlog dating relies on preserved mtimes (see peak_ram_gb, column peak_ram_dating_note)
(memlog lines carry HH:MM:SS only: dates are assigned walking back from the memlog's mtime and stepping back one day at every midnight wrap, so runs crossing midnight are handled; the value is the SUM over all simpleFoam processes on the host, so it includes any concurrent case: stated in the column name).
Never deletes anything. Existing rows of the same level in the CSV are replaced (the file is rewritten)."""
import sys, os, re, csv, json, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u3d_analyse as A
U = A.U; MEMLOG = os.path.dirname(U) + "/memlog.txt"

def timing(case):
    txt = open(f"{case}/log.simpleFoam").read()
    ex = re.findall(r"ExecutionTime = ([\d.]+) s\s+ClockTime = (\d+) s", txt)
    if not ex: raise SystemExit(f"{case}: no ExecutionTime line in log.simpleFoam")
    m = re.search(r"^Date\s*:\s*(\w+ \d+ \d+)\s*\nTime\s*:\s*(\d+:\d+:\d+)", txt, re.M)
    start = dt.datetime.strptime(f"{m.group(1)} {m.group(2)}", "%b %d %Y %H:%M:%S") if m else None      # full datetimes (local time), so a solve crossing midnight is bracketed correctly
    return dict(execution_time_s=float(ex[-1][0]), clock_time_s=int(ex[-1][1]), start_clock=start, end_clock=dt.datetime.fromtimestamp(os.path.getmtime(f"{case}/log.simpleFoam")).replace(microsecond=0),
                finished=("Finalising parallel run" in txt[-3000:] or "\nEnd" in txt[-500:]))

def memlog_samples(path=None):
    """[(datetime, simpleFoam_RSS_MB)] of memlog.txt (chronological, HH:MM:SS only). The last line is dated by the file's mtime; walking backwards, a clock time LATER than the
    following line's is a midnight wrap, so the date steps back one day (assumes no logging gap > 24 h)."""
    path = path or MEMLOG
    rows = [(m.group(1), int(m.group(2))) for m in (re.match(r"(\d\d:\d\d:\d\d) .*simpleFoam_RSS_MB=(\d+)", ln) for ln in open(path).read().splitlines()) if m]
    if not rows: return []
    day = dt.datetime.fromtimestamp(os.path.getmtime(path)).date(); out = []; nxt = None
    for hms, mb in reversed(rows):
        if nxt is not None and hms > nxt: day -= dt.timedelta(days=1)
        nxt = hms; out.append((dt.datetime.combine(day, dt.time.fromisoformat(hms)), mb))
    return out[::-1]

RAM_DATING_NOTE = "memlog mtime is not the last write; RAM window may be misdated"
ram_dating_warning = ""      # set by peak_ram_gb(): "" when fine, else RAM_DATING_NOTE

def peak_ram_gb(start, end, path=None, now=None):
    """max simpleFoam_RSS_MB (GB) of memlog samples inside [start, end] (datetimes from timing()); None if no sample / no memlog.
    RAM dating relies on a preserved memlog mtime (the logger's last write): if the newest sample, dated from the mtime, is more than 1 h away from now (the file was
    touched/copied later, or the logger stopped), the value is still returned but the module attribute ram_dating_warning is set to RAM_DATING_NOTE ("" when fine)."""
    global ram_dating_warning
    ram_dating_warning = ""; path = path or MEMLOG
    if not (start and end and os.path.exists(path)): return None
    if isinstance(start, str) or isinstance(end, str): raise TypeError("peak_ram_gb needs datetimes (timing() start_clock/end_clock), not HH:MM:SS strings")
    s = memlog_samples(path)
    if s and abs(((now or dt.datetime.now()) - s[-1][0]).total_seconds()) > 3600: ram_dating_warning = RAM_DATING_NOTE
    v = [mb for t, mb in s if start <= t <= end]
    return round(max(v) / 1024.0, 2) if v else None

def row(l, contended):
    case = f"{U}/{'wedge_' if l.startswith('W') else 'case_'}{l}"; d = A.level(l); t = timing(case)
    bi = json.load(open(f"{case}/build_info.json")); g = bi["mesh_gates"]
    nproc = int(re.search(r"numberOfSubdomains\s+(\d+)", open(f"{case}/system/decomposeParDict").read()).group(1))
    d.update(family=("wedge" if l.startswith("W") else "3D"), mpi_ranks=nproc, physical_cores_of_host=16, wall_clock_s=t["clock_time_s"], execution_time_s=t["execution_time_s"], log_finished=t["finished"],
             peak_ram_gb_sum_all_simpleFoam_on_host=peak_ram_gb(t["start_clock"], t["end_clock"]), peak_ram_dating_note=ram_dating_warning, contended=contended,
             checkMesh_standard_OK=g.get("checkMesh_standard_OK"), max_nonortho_deg=g.get("max_nonortho"), max_skew=g.get("max_skew"), checkMesh_strict_failed_checks=g.get("strict_failed_checks"), GATES_PASS=g.get("GATES_PASS"),
             throat_area_err_pct=(g.get("throat_area") or {}).get("err_pct"), flagged_sets=json.dumps({k: dict(n=v["n_points"], x_min_mm=round(v["x_min_mm"], 2), x_max_mm=round(v["x_max_mm"], 2)) for k, v in (g.get("flagged_sets") or {}).items()}),
             refinement_zone=("uniform wedge family" if l.startswith("W") else {"S50": "lesion zone 11.5-51.5 mm at 50 um", "A": "throat zone A 29-34 mm", "B": "throat zone B 30-35 mm (shifted)"}["S50" if l == "S50" else l[-1]]))
    return d

if __name__ == "__main__":
    if len(sys.argv) < 4: raise SystemExit(__doc__)
    out, contended, levels = sys.argv[1], sys.argv[2], sys.argv[3:]
    old = {r["level"]: r for r in csv.DictReader(open(out))} if os.path.exists(out) else {}
    new = {l: row(l, contended) for l in levels}
    rows = list(old.values()) if not new else [r for k, r in old.items() if k not in new]
    cols = []
    for r in list(rows) + list(new.values()):
        for k in r:
            if k not in cols: cols.append(k)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for r in rows + list(new.values()): w.writerow({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in r.items()})
    print("wrote", out, len(rows) + len(new), "rows")
