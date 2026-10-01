#!/bin/bash
# B2 host-level CPU calibration (fix 27, Fable attempt 1; audit SOL_FIX27_R3 finding 2): measures the host-level non-owned CPU (host busy - owned ledger, host_cpu_samples.csv) of the SAME sampler
# (b2_isolation.py) under the SAME 16-rank pinned launch path (b2_run.sh -> setsid b2_jobs.sh -> mpirun -np 16 --bind-to none b2_rank.sh simpleFoam -parallel) on a COPY of the prepared L16 case
# with a short endTime, so that the host-level thresholds HOST_* of b2_isolation.py can be set by the rule stated in b2_design.md ('Host-level calibration'). NOT a measurement: the copy's
# endTime is the calibration budget and the runner is told so (B2_CALIB_ENDTIME, accepted only under /b2_calib/); the original b2/L16/case is only read.
# usage: B2_EXCLUSIVE_OK=1 B2_ALLOW_STOPPED_FOREIGN=1 b2_calibrate.sh [iterations, default 150]
#   env: B2_CALIB_DIR (default /home/azan/paper6_t6_work/b2_calib), B2_SRC (the B2 directory with L16/case, b2_jobs.sh and b2_rank.sh; default the parent of this directory),
#   pass-through to b2_run.sh: B2_EXCLUSIVE_OK, B2_ALLOW_STOPPED_FOREIGN, B2_ALLOW_WINDOWS_LOAD, B2_ALLOW_NO_WINDOWS_CHECK, B2_MAX_RUNTIME_S (default 3600 here), B2_NOPROGRESS_S, B2_SAMPLE_S, B2_WIN_EVERY_S.
# Output: <B2_CALIB_DIR>/<stamp>/ with bin/ (copies of b2_run.sh + b2_isolation.py from this directory and b2_jobs.sh + b2_rank.sh from B2_SRC: the deployed set), L16/case (plain copy, endTime = budget),
#   results_L16/ (everything the runner writes: host_before.txt, isolation_samples.csv, host_cpu_samples.csv, isolation_evidence.json, stopped_foreign_*.txt, run_status.json, ...),
#   run.out / run.err (the runner's output) and calibration.json / calibration.txt (host busy minus owned per sample: mean, p95, max over all samples and over the loaded samples; the threshold rule).
HERE=$(cd "$(dirname "$0")" && pwd); SRC=${B2_SRC:-$(cd "$HERE/.." && pwd)}; CD=${B2_CALIB_DIR:-/home/azan/paper6_t6_work/b2_calib}; N=${1:-150}
die() { echo "FAIL: $*" >&2; exit 2; }
[[ "$N" =~ ^[0-9]+$ ]] && [ "$N" -ge 10 ] && [ "$N" -le 400 ] || die "iterations must be 10..400 (got $N)"
[[ "$CD" == */b2_calib* ]] || die "B2_CALIB_DIR must contain 'b2_calib' ($CD): the runner accepts B2_CALIB_ENDTIME only there"
[ -d "$SRC/L16/case" ] || die "$SRC/L16/case missing"; [ "$(ls -d "$SRC"/L16/case/processor* 2>/dev/null | wc -l)" -eq 16 ] || die "$SRC/L16/case: not 16 processor directories"
grep -q "^endTime *1600;" "$SRC/L16/case/system/controlDict" || die "$SRC/L16/case: endTime is not 1600 (not the prepared case)"
for f in "$HERE/b2_run.sh" "$HERE/b2_isolation.py" "$SRC/b2_jobs.sh" "$SRC/b2_rank.sh"; do [ -e "$f" ] || die "$f missing"; done
[ "${B2_EXCLUSIVE_OK:-0}" = 1 ] || die "set B2_EXCLUSIVE_OK=1 (the calibration is a 16-rank solver run of several minutes; the host must be reserved like for a measurement)"
need=$(( $(du -sm "$SRC/L16/case" | cut -f1) / 1024 + 11 )); [ "$(df --output=avail -B1G "$(dirname "$CD")" | tail -1 | tr -dc 0-9)" -ge "$need" ] || die "less than $need GB free for the case copy + the runner's 10 GB guard"
STAMP=$(date +%Y%m%d_%H%M%S); ROOT=$CD/$STAMP; [ ! -e "$ROOT" ] || die "$ROOT exists"
mkdir -p "$ROOT/bin" "$ROOT/L16" || die "cannot create $ROOT"
echo "$(date +%T) copying $SRC/L16/case -> $ROOT/L16/case (plain copy; the original is not modified)"
cp -a "$SRC/L16/case" "$ROOT/L16/case" || die "copy failed"
rm -rf "$ROOT/L16/case/postProcessing" "$ROOT/L16/case/log.simpleFoam" "$ROOT/L16/case/mpirun_bindings.txt"
sed -i "s/^endTime .*/endTime         $N;/" "$ROOT/L16/case/system/controlDict" && grep -q "^endTime *$N;" "$ROOT/L16/case/system/controlDict" || die "endTime edit failed"
cp -p "$HERE/b2_run.sh" "$HERE/b2_isolation.py" "$SRC/b2_jobs.sh" "$SRC/b2_rank.sh" "$ROOT/bin/" || die "bin copy failed"
{ echo "calibration $STAMP: source case $SRC/L16/case (endTime 1600) copied to $ROOT/L16/case with endTime $N; scripts: b2_run.sh b2_isolation.py from $HERE, b2_jobs.sh b2_rank.sh from $SRC"
  for f in "$HERE/b2_run.sh" "$HERE/b2_isolation.py" "$SRC/b2_jobs.sh" "$SRC/b2_rank.sh"; do sha256sum "$f"; done; grep -E "^(endTime|writeInterval)" "$ROOT/L16/case/system/controlDict"; } > "$ROOT/calibration_setup.txt"
echo "$(date +%T) launching the runner on the copy: B2_ROOT=$ROOT B2_CALIB_ENDTIME=$N B2_MAX_RUNTIME_S=${B2_MAX_RUNTIME_S:-3600} bash $ROOT/bin/b2_run.sh L16"
B2_ROOT="$ROOT" B2_CALIB_ENDTIME="$N" B2_MAX_RUNTIME_S="${B2_MAX_RUNTIME_S:-3600}" bash "$ROOT/bin/b2_run.sh" L16 > "$ROOT/run.out" 2> "$ROOT/run.err"; RC=$?
echo "$(date +%T) runner rc $RC (run.out / run.err in $ROOT)"; tail -3 "$ROOT/run.err" | cut -c1-200
R=$ROOT/results_L16
[ -s "$R/host_cpu_samples.csv" ] || die "no host_cpu_samples.csv in $R (runner rc $RC; see $ROOT/run.err)"
python3 - "$ROOT" "$N" "$RC" <<'PY' | tee "$ROOT/calibration.txt"
import csv, json, os, re, sys
root, n_it, rc = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); r = f"{root}/results_L16"
h = list(csv.DictReader(open(f"{r}/host_cpu_samples.csv"))); s = list(csv.DictReader(open(f"{r}/isolation_samples.csv")))
col = lambda rows, k: [float(x[k]) for x in rows if x.get(k, "") != ""]
def st(v):
    if not v: return dict(n=0, mean=None, p95=None, max=None, min=None)
    v = sorted(v); return dict(n=len(v), mean=round(sum(v) / len(v), 4), p95=round(v[max(0, -(-95 * len(v) // 100) - 1)], 4), max=round(v[-1], 4), min=round(v[0], 4))
hn, raw, hb, ho = col(h, "host_nonowned_cores"), col(h, "host_minus_owned_raw_cores"), col(h, "host_busy_cores"), col(h, "owned_ledger_cores")
loaded = [x for x in h if x.get("owned_ledger_cores", "") != "" and float(x["owned_ledger_cores"]) >= 12.0]      # samples with the 16 ranks running (start-up / shutdown excluded)
pp = col(s, "nonowned_linux_cores"); ppo = col(s, "owned_cores")
diff = [float(a["host_nonowned_cores"]) - float(b["nonowned_linux_cores"]) for a, b in zip(h, s) if a.get("host_nonowned_cores", "") != "" and b.get("nonowned_linux_cores", "") != ""]
ev = json.load(open(f"{r}/isolation_evidence.json")) if os.path.exists(f"{r}/isolation_evidence.json") else {}
rs = json.load(open(f"{r}/run_status.json")) if os.path.exists(f"{r}/run_status.json") else {}
log = open(f"{root}/L16/case/log.simpleFoam").read() if os.path.exists(f"{root}/L16/case/log.simpleFoam") else ""
steps = len(re.findall(r"^Time = ", log, re.M)); et = re.findall(r"ExecutionTime = ([0-9.]+) s  ClockTime = ([0-9.]+) s", log)
out = dict(calibration_run=os.path.basename(root), iterations_budget=n_it, iterations_run=steps, runner_rc=rc, end_reason=rs.get("end_reason"), controlled_end=rs.get("controlled_end"),
           clock_s_last=float(et[-1][1]) if et else None, samples=len(h), sample_interval_s=(float(h[-1]["elapsed_s"]) - float(h[0]["elapsed_s"])) / max(len(h) - 1, 1) if len(h) > 1 else None,
           host_nonowned_cores_all=st(hn), host_minus_owned_raw_cores_all=st(raw), host_busy_cores_all=st(hb), owned_ledger_cores_all=st(ho),
           host_nonowned_cores_loaded=st(col(loaded, "host_nonowned_cores")), host_minus_owned_raw_cores_loaded=st(col(loaded, "host_minus_owned_raw_cores")), loaded_samples=len(loaded),
           perpid_nonowned_cores_all=st(pp), perpid_owned_cores_all=st(ppo), host_minus_perpid_nonowned_cores_all=st(diff),
           evidence_contended=ev.get("contended"), evidence_reasons=ev.get("contended_reasons"), bindings_verified=ev.get("bindings_verified"), host_level_mode_used=ev.get("host_level_mode"),
           run_host_nonowned_cores_evidence=ev.get("run_host_nonowned_cores"), run_linux_nonowned_cores_evidence=ev.get("run_linux_nonowned_cores"), host_forks=ev.get("host_forks"),
           stopped_foreign_postrun=ev.get("stopped_foreign_postrun"), top_nonowned=ev.get("run_linux_nonowned_top_processes_max_cores"))
m, p95, mx = out["host_nonowned_cores_all"]["mean"], out["host_nonowned_cores_all"]["p95"], out["host_nonowned_cores_all"]["max"]
sys.path.insert(0, f"{root}/bin"); import b2_isolation as I          # the deployed sampler module: calib_rule is THE pre-stated rule (b2_design.md); the thresholds it currently uses are recorded too
rule = I.calib_rule(m, p95, mx); out["threshold_rule"] = rule
out["deployed_thresholds"] = dict(calibration_run=I.CALIB_RUN, HOST_MODE=I.HOST_MODE, HOST_MEAN_MAX=I.HOST_MEAN_MAX, HOST_MAX_MAX=I.HOST_MAX_MAX,
                                  same_as_this_rule=(rule.get("HOST_MODE"), rule.get("HOST_MEAN_MAX", I.HOST_MEAN_MAX), rule.get("HOST_MAX_MAX", I.HOST_MAX_MAX)) == (I.HOST_MODE, I.HOST_MEAN_MAX, I.HOST_MAX_MAX))
json.dump(out, open(f"{root}/calibration.json", "w"), indent=1)
print(f"calibration {out['calibration_run']}: {steps}/{n_it} iterations, runner rc {rc}, end {rs.get('end_reason')}, controlled_end {rs.get('controlled_end')}, clock {out['clock_s_last']} s, {len(h)} host samples ({out['sample_interval_s'] and round(out['sample_interval_s'], 2)} s)")
for k in ("host_nonowned_cores_all", "host_minus_owned_raw_cores_all", "host_busy_cores_all", "owned_ledger_cores_all", "host_nonowned_cores_loaded", "host_minus_owned_raw_cores_loaded", "perpid_nonowned_cores_all", "perpid_owned_cores_all", "host_minus_perpid_nonowned_cores_all"): print(f"  {k:40s} {out[k]}")
print(f"  loaded samples (owned >= 12 cores): {len(loaded)}; evidence contended={ev.get('contended')} {ev.get('contended_reasons')}; bindings_verified={ev.get('bindings_verified')}; mode used {ev.get('host_level_mode')}")
print(f"  host_forks {ev.get('host_forks')}\n  stopped_foreign_postrun {ev.get('stopped_foreign_postrun')}\n  top non-owned (per-PID, max core) {ev.get('run_linux_nonowned_top_processes_max_cores')}")
print(f"  threshold rule -> {rule}\n  deployed thresholds (bin/b2_isolation.py) -> {out['deployed_thresholds']}")
PY
echo "calibration written: $ROOT/calibration.json, $ROOT/calibration.txt"
