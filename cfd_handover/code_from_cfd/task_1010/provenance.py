#!/usr/bin/env python3
"""WO 2026-10-10 section 6 (Sol R2 finding 5): solve-time provenance of one case, written by the pool job (make_job.py) and the Task G driver right BEFORE case_job.sh starts the solve.
usage: provenance.py write <case> [--out <return_dir>] [--job NAME] [--built-in-job 0|1]
Writes <case>/provenance.json (atomic) and, with --out, a copy into the return dir (<out>/provenance.json; a differing earlier copy is never overwritten: provenance_<date>[_rN].json, the newest is used).
An earlier, differing <case>/provenance.json (an earlier attempt on the same case) is kept as <case>/provenance_superseded_<UTC timestamp>.json (not a stale item for case_job.sh).
Content:
  host (socket.gethostname()), date (local ISO), user, job, built_in_job (1 = the case was built by this same job seconds before, so the code hashes below are the code that built it;
  0 = an existing case was reused: the code hashes are those at solve start, the build time is case_built_at, the build log hash is recorded);
  openfoam: WM_PROJECT_VERSION, WM_PROJECT_DIR, `simpleFoam -help` 'Using:' and 'Build:' lines (from the v2406 bashrc, as case_job.sh sources it);
  code: sha256 of pf/build_m1_case.py, pf/pf_common.py, wo1010/case_job.sh, post_case_generic.sh, wo1010/make_job.py, wo1010/taskG.py, wo1010/provenance.py, wo1010/wo_common.py;
  template: TEMPLATE path read from pf/build_m1_case.py, template_sha256 = sha256 over the sorted '<sha256>  <relpath>' lines of ALL its files (recursive), n files;
  case as built: sha256 of build_info.json, case_system_sha256 / case_0_sha256 (same tree rule over system/ and 0/), r_scale_k, mode, package, mesh_source_dir, case_built_at (build_info mtime),
  build log sha256 (wo1010/logs/build_<case name>.log when present).
No git repository holds the template: template_commit says so unless $TEMPLATE_COMMIT is set."""
import os, sys, re, json, socket, subprocess, datetime, getpass
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from wo_common import P, sha256, tree_sha256, atomic_json, issue_atomic

FOAM_ENV = "/usr/lib/openfoam/openfoam2406/etc/bashrc"
CODE = [f"{P}/pf/build_m1_case.py", f"{P}/pf/pf_common.py", f"{HERE}/case_job.sh", f"{P}/post_case_generic.sh", f"{HERE}/make_job.py", f"{HERE}/taskG.py",
        f"{HERE}/provenance.py", f"{HERE}/wo_common.py"]

def template_path():
    m = re.search(r'^TEMPLATE\s*=\s*"([^"]+)"', open(f"{P}/pf/build_m1_case.py").read(), re.M)
    if not m: raise SystemExit("REFUSED: no TEMPLATE = \"...\" line in pf/build_m1_case.py")
    return m.group(1)

def openfoam():
    r = subprocess.run(["bash", "-c", f"source {FOAM_ENV} >/dev/null 2>&1; echo \"V=$WM_PROJECT_VERSION\"; echo \"D=$WM_PROJECT_DIR\"; simpleFoam -help 2>&1 | grep -E '^(Using|Build)' | head -2"],
                       capture_output=True, text=True, timeout=120)
    d = dict(re.findall(r"^(V|D)=(.*)$", r.stdout, re.M))
    using = re.search(r"^Using:\s*(.*)$", r.stdout, re.M); build = re.search(r"^Build:\s*(.*)$", r.stdout, re.M)
    o = dict(WM_PROJECT_VERSION=d.get("V", ""), WM_PROJECT_DIR=d.get("D", ""), using=using.group(1).strip() if using else "", build=build.group(1).strip() if build else "")
    if not o["WM_PROJECT_VERSION"] or not o["build"]: raise SystemExit(f"REFUSED: OpenFOAM version/build not determined from {FOAM_ENV} ({r.stdout!r} {r.stderr[-300:]!r})")
    return o

def collect(case, job=None, built=None):
    case = os.path.abspath(case); bi = f"{case}/build_info.json"
    if not os.path.isfile(bi): raise SystemExit(f"REFUSED: {bi} missing (provenance is written for a BUILT case only)")
    info = json.load(open(bi)); tp = template_path()
    if not os.path.isdir(tp): raise SystemExit(f"REFUSED: template {tp} not found")
    missing = [f for f in CODE if not os.path.isfile(f)]
    if missing: raise SystemExit(f"REFUSED: code files missing: {missing}")
    for d in ("system", "0"):
        if not os.path.isdir(f"{case}/{d}"): raise SystemExit(f"REFUSED: {case}/{d} missing")
    th, tn = tree_sha256(tp); sh, sn = tree_sha256(f"{case}/system"); zh, zn = tree_sha256(f"{case}/0")
    blog = f"{HERE}/logs/build_{os.path.basename(case)}.log"
    return dict(provenance_version=1, case=case, case_name=os.path.basename(case), job=job, host=socket.gethostname(), user=getpass.getuser(),
                date=datetime.datetime.now().astimezone().isoformat(timespec="seconds"), built_in_job=built,
                openfoam=openfoam(), code={f: sha256(f) for f in CODE}, template=tp, template_sha256=th, template_files=tn,
                template_commit=os.environ.get("TEMPLATE_COMMIT") or "none: no git repository holds the production template (content hash template_sha256 instead)",
                build_info_sha256=sha256(bi), case_system_sha256=sh, case_system_files=sn, case_0_sha256=zh, case_0_files=zn,
                case_built_at=datetime.datetime.fromtimestamp(os.path.getmtime(bi)).astimezone().isoformat(timespec="seconds"),
                build_log=blog if os.path.isfile(blog) else None, build_log_sha256=sha256(blog) if os.path.isfile(blog) else None,
                r_scale_k=info.get("r_scale_k"), mode=info.get("mode"), stage=info.get("stage"), package=info.get("package"), mesh_source_dir=info.get("mesh_source_dir"))

def write(case, out=None, job=None, built=None):
    d = collect(case, job, built); p = f"{os.path.abspath(case)}/provenance.json"
    if os.path.exists(p):
        old = open(p).read(); new = json.dumps(d, indent=1, default=str) + "\n"
        if old != new: os.replace(p, f"{os.path.abspath(case)}/provenance_superseded_{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')}.json")
    atomic_json(p, d)
    q = issue_atomic(f"{out}/provenance.json", open(p).read()) if out else None
    print(f"provenance: {p}" + (f" -> {q}" if q else "") + f" (host {d['host']}, OpenFOAM {d['openfoam']['WM_PROJECT_VERSION']} {d['openfoam']['build']}, template {d['template_sha256'][:12]}, built_in_job {built})")
    return d

def main(a):
    if not a or a[0] != "write" or len(a) < 2: raise SystemExit(__doc__)
    def opt(f, dflt=None):
        if f in a: i = a.index(f); v = a[i + 1]; del a[i:i + 2]; return v
        return dflt
    out, job, built = opt("--out"), opt("--job"), opt("--built-in-job")
    if built not in (None, "0", "1"): raise SystemExit("--built-in-job 0|1")
    if out: os.makedirs(out, exist_ok=True)
    write(a[1], out, job, None if built is None else built == "1")

if __name__ == "__main__":
    main(sys.argv[1:])
