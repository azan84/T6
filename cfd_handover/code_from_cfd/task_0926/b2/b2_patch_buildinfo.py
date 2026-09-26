"""Task B2 (audit 0926-SETUPS finding 5): patches <case_dir>/build_info.json of a prepared B2 case to the prepared run: nproc = <nproc> (subdomains), endTime 1600, writeInterval 100000, and a b2_note field.
All other keys are kept (order too). Idempotent (a second call leaves the file byte-identical). Refuses (exit 2, file untouched) if the file is missing/unreadable or lacks one of nproc, endTime, writeInterval,
or if <nproc> is not a positive integer or differs from the processor* directories present in <case_dir> (if any).
usage: b2_patch_buildinfo.py <case_dir> <nproc>"""
import sys, os, json, glob
END_TIME, WRITE_INTERVAL = 1600, 100000
def note(n): return (f"B2 copy of m1/cases/baseline_resistance: nproc {n} (decomposePar scotch), endTime {END_TIME} (B1 settle 1229 + 30 %), writeInterval {WRITE_INTERVAL} (no field writes); "
                     "the other keys are those of the source case (build of the 16-rank, 3000-iteration original)")
def main(case, n):
    f = os.path.join(case, "build_info.json")
    if not (n.isdigit() and int(n) > 0): return f"nproc '{n}' is not a positive integer"
    n = int(n); procs = len(glob.glob(os.path.join(case, "processor*")))
    if procs and procs != n: return f"{case} has {procs} processor directories, not {n}"
    try: d = json.load(open(f))
    except Exception as e: return f"cannot read {f}: {e}"
    miss = [k for k in ("nproc", "endTime", "writeInterval") if k not in d]
    if miss: return f"{f} lacks the key(s) {miss}: not a build_info.json of the source case, refused"
    new = dict(d, nproc=n, endTime=END_TIME, writeInterval=WRITE_INTERVAL, b2_note=note(n)); txt = json.dumps(new, indent=1) + "\n"
    if open(f).read() == txt: print(f"{f}: already patched (nproc {n}, endTime {END_TIME}, writeInterval {WRITE_INTERVAL})"); return None
    tmp = f + ".tmp"; open(tmp, "w").write(txt); os.replace(tmp, f)
    print(f"{f}: nproc {d['nproc']} -> {n}, endTime {d['endTime']} -> {END_TIME}, writeInterval {d['writeInterval']} -> {WRITE_INTERVAL}, b2_note set")
if __name__ == "__main__":
    if len(sys.argv) != 3: print(__doc__); sys.exit(2)
    err = main(sys.argv[1], sys.argv[2])
    if err: print("REFUSED:", err); sys.exit(2)
