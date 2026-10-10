#!/usr/bin/env python3
"""WO 2026-10-10: write one pool job (wo1010_pool/jobs/<name>.json, atomic) per (label, mode) solve, per task gate, or the Task G driver. No .audited marker is ever written here: the pool starts a job
only after the pre-run audit (codex gpt-5.6-sol + agy gemini-3.7-flash-medium) has cleared it and the marker is created by hand.
usage: make_job.py <package_path> <label> <resistance|prescribed> <task> <priority> [--r-scale K] [--tag T] [--after a,b,...]     solve job <label>_<mode><tag>
       make_job.py gate <Task> <priority> --after a,b,...                                                                      gate job gate_<Task> (task_gate.py; ranks 1, ram 0.5 GB)
       make_job.py taskG <priority> --after a,b,...                                                                            Task G driver job taskG_14_T1regen (taskG.py)
SOLVE job: builds the case with pf/build_m1_case.py if it does not exist (package path, mesh wo1010/mesh/<label>, as-built extensions from the geometry stage), then writes the solve-time provenance
(provenance.py write <case> --out <return dir>: host, OpenFOAM build, code + template hashes, as-built case hashes, built_in_job 1 when this job built the case), then wo1010/case_job.sh <case> 16 with
POST_CMD = post_case_generic.sh into the Drive return folder returns/2026-10-10/<task>/<label>_<mode>/ (kilobyte CSV/JSON only).
Refuses (exit 1) when out/<label>_extensions.json, mesh/<label>/d34.json, mesh/<label>/mesh_gates.json or the mesh cell count is missing. The job's build step refuses an existing case dir without
build_info.json (half-built).
--after: names of jobs that must have finished OK first (pool `after`; comma-separated).
Idempotent: an identical existing job file is left untouched ('unchanged'); a DIFFERENT existing job file is replaced only if it has neither a .audited marker nor a .status file (an audited or started job
is never rewritten: exit 1)."""
import json, os, sys, shlex
P = "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot"; H = f"{P}/wo1010"; J = os.environ.get("WO1010_JOBS_DIR", "/home/azan/paper6_t6_work/wo1010_pool/jobs")
RET = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-10"
a = [x for x in sys.argv[1:]]
def opt(f, d=None):
    if f in a: i = a.index(f); v = a[i + 1]; del a[i:i + 2]; return v
    return d
after = [x for x in (opt("--after", "") or "").split(",") if x]

def write_job(job):
    n = job["name"]; f = f"{J}/{n}.json"; txt = json.dumps(job, indent=1)
    if os.path.exists(f):
        if open(f).read() == txt: print(f"{n}: unchanged"); return
        held = [x for x in (f"{J}/{n}.audited", f"{J}/{n}.status") if os.path.exists(x)]
        if held: sys.exit(f"REFUSED: {f} differs from the new job but {held} exist(s): an audited/started job is never rewritten")
    tmp = f"{J}/.{n}.json.tmp"; open(tmp, "w").write(txt); os.replace(tmp, f)      # atomic: the running pool never reads a partial file
    print(f"{n}: written, after {job['after']}")

if a and a[0] == "gate":
    task, prio = a[1], int(a[2])
    assert task in ("TaskT", "TaskG", "TaskM", "TaskT2", "TaskN") and after, "gate <Task> <priority> --after a,b,..."
    write_job(dict(name=f"gate_{task}", ranks=1, ram_gb=0.5, disk_gb=0, priority=prio, cmd=f"cd {H} && python3 -u task_gate.py {task} >> logs/gate_{task}.log 2>&1", after=after))
    sys.exit(0)
if a and a[0] == "taskG":
    prio = int(a[1]); assert after, "taskG <priority> --after a,b,..."
    write_job(dict(name="taskG_14_T1regen", ranks=16, ram_gb=6.4, disk_gb=6, priority=prio, cmd=f"cd {H} && mkdir -p cases logs state && python3 -u taskG.py >> logs/taskG_driver.log 2>&1", after=after))
    sys.exit(0)

k = float(opt("--r-scale", 1.0)); tag = opt("--tag", "")
pk, label, mode, task, prio = a[0], a[1], a[2], a[3], int(a[4])
assert mode in ("resistance", "prescribed") and os.path.isdir(pk), (pk, label)
for f in (f"{H}/mesh/{label}/constant/polyMesh/boundary", f"{H}/out/{label}_extensions.json", f"{H}/mesh/{label}/d34.json", f"{H}/mesh/{label}/mesh_gates.json"):
    if not os.path.isfile(f): sys.exit(f"REFUSED: {f} missing (run_geom_mesh.sh has not finished {label})")
name = f"{label}_{mode}{tag}"; case = f"{H}/cases/{name}"; out = f"{RET}/{task}/{name}"
ext = f"{H}/out/{label}_extensions.json"
cells = json.load(open(f"{H}/mesh/{label}/mesh_gates.json")).get("cells")
if not isinstance(cells, int) or cells <= 0: sys.exit(f"REFUSED: {H}/mesh/{label}/mesh_gates.json has no cell count (cells = {cells!r})")
ram = round(1.4 * cells / 1e6 + 1.5, 1)
build = (f"[ -f {case}/build_info.json ] || {{ [ -e {case} ] && {{ echo 'REFUSED: {case} exists without build_info.json (half-built): move it away first'; exit 1; }}; OMP_NUM_THREADS=4 nice -n 5 python3 {P}/pf/build_m1_case.py {pk} {H}/mesh/{label} {mode} {case} 16 --extensions-json {ext}"
         + (f" --r-scale {k!r}" if k != 1.0 else "") + f" > {H}/logs/build_{name}.log 2>&1 && B=1; }}")
prov = f"python3 {H}/provenance.py write {case} --out {out} --job {name} --built-in-job $B"
post = (f"cd {P} && mkdir -p {out} && P={P} GATES_JSON={H}/out/{label}/gates.json MESH_GATES_JSON={H}/mesh/{label}/mesh_gates.json D34_JSON={H}/mesh/{label}/d34.json "
        f"OMP_NUM_THREADS=4 bash {P}/post_case_generic.sh {case} {pk} {label}{tag} {mode} {out}")
cmd = f"B=0; mkdir -p {H}/cases {H}/logs && {{ {build}; }} && {prov} && POST_CMD={shlex.quote(post)} DISK_NEED_GB=6 bash {H}/case_job.sh {case} 16"
write_job(dict(name=name, ranks=16, ram_gb=ram, disk_gb=6, priority=prio, cmd=cmd, after=after))
print(f"{name}: cells {cells}, ram {ram} GB, prio {prio}, task {task}, k {k}")
