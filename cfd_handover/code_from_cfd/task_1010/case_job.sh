#!/bin/bash
# Generic solve job for pool jobs outside the audited run_set_generic.sh (that launcher holds one global flock, so two launcher invocations cannot overlap; this script is for the second job lane).
# WO1010 copy of lane2/case_job.sh with ONE change, PRESCRIBED-FLOW MODE: when <case>/build_info.json has mode or stage "prescribed" (both must then say so), the coded-BC requirement ('name res<stem>;' in 0/p)
#   and the smoke's libres*.so / dynamicCode count checks are replaced by prescribed_check: every live outlet of build_info 'outlets' is in 0/U exactly once as flowRateOutletVelocity with a constant
#   volumetricFlowRate equal to its Q_target_m3s (relative 1e-9), no other flowRateOutletVelocity entry, each such outlet in 0/p exactly once as zeroGradient, and no coded entry in any 0/ file; the 2-iteration
#   serial smoke still runs and must End at Time = 2; dynamicCode must be absent after it (nothing coded to compile). Any other build_info (no file, resistance) runs the unchanged resistance path.
# usage: case_job.sh <case_dir> [ranks]  |  case_job.sh --self-test (self-test of the completion test on synthetic logs; touches no case)
#        Steps: flock -n <case>/.case_job.lock (held for the whole run; a second invocation on the same case is refused, exit 3) -> disk gate (free disk on the case filesystem >= DISK_NEED_GB (default 6) + 8 GB
#        reserve, else refused, exit 5) -> strict stale-item refusal (READ-ONLY, all items listed)
#        -> assert production controlDict (startFrom startTime, startTime 0, stopAt endTime, endTime 3000 or CASE_END, no writeNow) -> serial 2-iteration compile smoke (exact End, last Time = 2, one libres<stem>_*.so per
#        'name res<stem>;' of 0/p and names+1 dynamicCode entries; smoke output removed, log kept as log.smoke.keep) -> production controlDict restored and verified -> decomposePar (ranks from decomposeParDict, must equal
#        <ranks>; exactly <ranks> processor dirs) -> mpirun -np <ranks> --bind-to none simpleFoam -parallel (full budget, fields kept) -> success only if
#        rc 0 AND the last run of the log is complete (solve_complete: a line exactly 'End' after the last 'Time = ' line, no Time/header/FOAM FATAL line after it) AND that last 'Time = ' == endTime
#        -> reconstructPar -latestTime verified (exact End in log.reconstructPar; latest reconstructed time == processor0 latest == log's last Time == endTime; U, p, phi non-empty and newer than the solve start)
#        -> optional post hook: if POST_CMD is set, `bash -c "$POST_CMD"` runs in the case dir (env CASE_DIR, CASE_END, CASE_NP; output in log.post); rc != 0 fails the job (processor dirs kept)
#        -> disk staging: the case's processor[0-9]* dirs (decomposed duplicates of the verified reconstructed fields) are purged and the released disk is printed ("PURGED: ..."); KEEP_PROCESSORS=1 keeps them.
#        The reconstructed time dir, 0/, constant/, system/, postProcessing (monitors) and log.* stay. No failure path (refusal, failed check, failed hook, signal before the purge) ever purges.
# controlDict safety: from the moment system/controlDict.production is written, an EXIT trap (also reached from INT/TERM, which first stop the running child) copies it back over system/controlDict, checks the copy
# byte-for-byte (cmp) and re-asserts the production controls on EVERY exit path; a failed restoration is reported as FATAL with exit 4. controlDict.production is kept (it marks the case as used: a rerun is refused
# by the stale check until the case is cleaned). Only SIGKILL bypasses the trap; the kept controlDict.production then holds the production controls.
# Exit codes: 0 success, 1 failure/refusal (incl. POST_CMD failure), 2 usage/no case dir/bad env value, 3 case locked by another invocation, 4 controlDict restoration failed, 5 not enough free disk,
#             130/143 INT/TERM.
# Test hooks (taskJ/tests): CASE_JOB_SKIP_FOAM_ENV=1 skips sourcing the OpenFOAM bashrc (the stub commands come from PATH; the five tools and WM_PROJECT_VERSION v2406 are still required);
#   CASE_JOB_FOAM_BASHRC overrides the bashrc path; CASE_JOB_DRYRUN_STOP (non-empty) stops with rc 0 after the read-only gates, before the smoke (no write but the lock file, no solver).
solve_complete() {   # $1 rc, $2 log, $3 endTime -> prints the reason and returns 1 unless: rc 0, the last run of the log (from its last header line Build:/Exec:/'Starting time loop') has a 'Time = ' line,
                     # the last 'Time = ' is followed by a line exactly 'End', no header/Time/FOAM FATAL line comes after that End, and the last Time == endTime (as taskC/pf/post_helpers.py run_completion)
  [ "$1" = 0 ] || { echo "mpirun exit code $1 (see $2)"; return 1; }
  [ -f "$2" ] || { echo "no log $2"; return 1; }
  awk -v E="$3" -v F="$2" '
    function hdr(l) { return l ~ /^(Exec[ \t]*:|Build[ \t]*:|Starting time loop)/ }
    { sub(/\r$/, ""); L[NR] = $0 }
    hdr($0) { h = NR }
    /^Time = [^ \t]+$/ { t = NR; T = substr($0, 8) }
    $0 == "End" { e = NR }
    END {
      if (!t || t < h) { print "the last run of " F " has no '\''Time = '\'' line"; exit 1 }
      if (!e) { print "no exact '\''End'\'' line in " F; exit 1 }
      if (e < t) { print "the last '\''End'\'' (line " e ") of " F " precedes the last '\''Time = '\'' line (" t ")"; exit 1 }
      if (e < h) { print "the last '\''End'\'' (line " e ") of " F " precedes the last run header (line " h ")"; exit 1 }
      for (i = e + 1; i <= NR; i++) if (hdr(L[i]) || L[i] ~ /^Time = / || index(L[i], "FOAM FATAL")) { print "line " i " after the last End of " F ": " substr(L[i], 1, 60); exit 1 }
      if (T != E && !(T ~ /^[-+.0-9eE]+$/ && T + 0 == E + 0)) { print "last '\''Time = '\'' in " F " is '\''" T "'\'', expected " E; exit 1 }
    }' "$2"
}
case_mode() {   # $1 case dir -> prints 'prescribed' if build_info.json mode AND stage are "prescribed", 'conflict ...' if only one is, else 'resistance' (no/unreadable build_info: the unchanged path)
  python3 - "$1/build_info.json" <<'EOF' 2> /dev/null || echo resistance
import json, sys
try: b = json.load(open(sys.argv[1]))
except Exception: print("resistance"); sys.exit(0)
m, s = b.get("mode"), b.get("stage")
print("prescribed" if m == s == "prescribed" else (f"conflict: build_info mode {m!r}, stage {s!r}" if "prescribed" in (m, s) else "resistance"))
EOF
}
prescribed_check() {   # $1 case dir -> prints the first violation and returns 1, else a one-line summary (prescribed-flow mode, see the header)
  python3 - "$1" <<'EOF'
import json, math, os, re, sys
C = sys.argv[1]
def bf(f):   # top-level entries of boundaryField: {patch: [body, ...]} (bodies of duplicates kept to detect them)
    t = re.sub(r"//[^\n]*", "", re.sub(r"/\*.*?\*/", "", open(f).read(), flags=re.S)); i = t.find("boundaryField")
    if i < 0: raise SystemExit(f"{f}: no boundaryField")
    i = t.index("{", i) + 1; out = {}
    while True:
        m = re.compile(r"\s*([^\s{}]+)\s*\{|\s*\}").match(t, i)
        if not m: raise SystemExit(f"{f}: cannot parse boundaryField at offset {i}")
        if m.group(1) is None: return out
        d, j = 1, m.end()
        while d:
            if j >= len(t): raise SystemExit(f"{f}: unbalanced braces in entry {m.group(1)}")
            d += {"{": 1, "}": -1}.get(t[j], 0); j += 1
        out.setdefault(m.group(1), []).append(t[m.end():j - 1]); i = j
try:
    b = json.load(open(f"{C}/build_info.json")); outs = b["outlets"]
    if not outs: raise SystemExit("build_info.json 'outlets' is empty")
    for f in sorted(os.listdir(f"{C}/0")):
        if os.path.isfile(f"{C}/0/{f}") and re.search(r"coded|#\{|\bname\s+res", open(f"{C}/0/{f}").read()): raise SystemExit(f"coded entry in 0/{f} (prescribed mode has none)")
    U, p = bf(f"{C}/0/U"), bf(f"{C}/0/p"); worst = 0.0
    for o in outs:
        n, q = o["patch"], float(o["Q_target_m3s"])
        if not (math.isfinite(q) and q > 0): raise SystemExit(f"{n}: build_info Q_target_m3s {q} is not a positive number")
        if len(U.get(n, [])) != 1 or len(p.get(n, [])) != 1: raise SystemExit(f"{n}: {len(U.get(n, []))} entries in 0/U and {len(p.get(n, []))} in 0/p, expected 1 each")
        u = " ".join(U[n][0].split())
        if not re.search(r"(^|;) ?type flowRateOutletVelocity;", u): raise SystemExit(f"0/U {n} is not flowRateOutletVelocity: {u[:80]}")
        m = re.search(r"(^|;) ?volumetricFlowRate (?:constant )?([-+.0-9eE]+);", u)
        if not m: raise SystemExit(f"0/U {n}: no constant volumetricFlowRate (a ramp table is not allowed here): {u[:80]}")
        r = abs(float(m.group(2)) - q) / q; worst = max(worst, r)
        if r > 1e-9: raise SystemExit(f"0/U {n}: volumetricFlowRate {m.group(2)} != build_info Q_target_m3s {q!r} (rel {r:.2e} > 1e-9)")
        if " ".join(p[n][0].split()) != "type zeroGradient;": raise SystemExit(f"0/p {n} is not zeroGradient: {' '.join(p[n][0].split())[:80]}")
    extra = sorted(k for k, v in U.items() if k not in {o["patch"] for o in outs} and any("flowRateOutletVelocity" in x for x in v))
    if extra: raise SystemExit(f"flowRateOutletVelocity on patch(es) not in build_info 'outlets' (closed/lost outlets carry no flow): {extra}")
except SystemExit: raise
except Exception as e: raise SystemExit(f"cannot check the prescribed BCs: {type(e).__name__}: {e}")
print(f"{len(outs)} live outlets flowRateOutletVelocity == build_info Q_target_m3s (max rel diff {worst:.1e}), p zeroGradient, no coded entries")
EOF
}
if [ "$1" = --self-test ]; then   # synthetic logs, one per line: name|rc|expected (0 complete, 1 not complete)|log text (printf format)
  D=$(mktemp -d) || exit 1; n=0; bad=0
  while IFS='|' read -r name rc want body; do
    printf "$body" > "$D/log"; why=$(solve_complete "$rc" "$D/log" 3000); got=$?; n=$((n + 1))
    if [ "$got" = "$want" ]; then printf 'self-test PASS  %-22s %s\n' "$name" "${why:-complete}"; else bad=$((bad + 1)); printf 'self-test FAIL  %-22s expected %s, got %s (%s)\n' "$name" "$want" "$got" "$why"; fi
  done <<'E'
complete|0|0|Build  : v2406\nStarting time loop\n\nTime = 2999\n\nTime = 3000\n\nExecutionTime = 1 s\n\nEnd\n\n
complete_crlf|0|0|Starting time loop\r\nTime = 3000\r\nEnd\r\n
complete_two_runs|0|0|Starting time loop\nTime = 10\nEnd\nBuild  : v2406\nStarting time loop\nTime = 3000\nEnd\n
rc_nonzero_with_end|1|1|Starting time loop\nTime = 3000\nEnd\n
rc_signal_with_end|143|1|Starting time loop\nTime = 3000\nEnd\n
end_trailing_space|0|1|Starting time loop\nTime = 3000\nEnd \n
end_prefixed|0|1|Starting time loop\nTime = 3000\nEnding\n
end_indented|0|1|Starting time loop\nTime = 3000\n  End\n
no_end|0|1|Starting time loop\nTime = 3000\n
early_stop|0|1|Starting time loop\nTime = 2999\nEnd\n
residual_stop|0|1|Starting time loop\nTime = 1500\nSIMPLE solution converged in 1500 iterations\nEnd\n
past_end|0|1|Starting time loop\nTime = 3001\nEnd\n
end_before_last_time|0|1|Starting time loop\nTime = 2999\nEnd\nTime = 3000\n
appended_run|0|1|Starting time loop\nTime = 3000\nEnd\nBuild  : v2406\nStarting time loop\nTime = 1\n
appended_header_only|0|1|Starting time loop\nTime = 3000\nEnd\nExec   : simpleFoam -parallel\n
fatal_after_end|0|1|Starting time loop\nTime = 3000\nEnd\n--> FOAM FATAL ERROR: (stub)\n
no_time|0|1|Starting time loop\nEnd\n
empty_log|0|1|
E
  echo "self-test: $((n - bad))/$n passed"
  # prescribed-mode checks on a synthetic case: name|expected (0 ok, 1 refused)|mode (expected case_mode output)|sed edit of 0/U|sed edit of 0/p|build_info Q of out_2
  m=0; pbad=0; mkdir -p "$D/pc/0"
  while IFS='|' read -r name want mode eu ep q2; do
    printf '{"mode": "%s", "stage": "prescribed", "outlets": [{"patch": "out_1", "Q_target_m3s": 9.526337218187127e-08}, {"patch": "out_2", "Q_target_m3s": %s}]}\n' "${mode%%:*}" "$q2" > "$D/pc/build_info.json"
    printf 'FoamFile { version 2.0; format ascii; class volVectorField; object U; }\nboundaryField\n{\n    inlet   { type pressureInletOutletVelocity; value uniform (0 0 0); }\n    wall    { type noSlip; }\n    out_1   { type flowRateOutletVelocity; volumetricFlowRate 9.5263372182e-08; value uniform (0 0 0); }\n    out_2   { type flowRateOutletVelocity; volumetricFlowRate 1.0437238952e-07; value uniform (0 0 0); }\n    out_3   { type noSlip; }\n}\n' | sed -E "$eu" > "$D/pc/0/U"
    printf 'FoamFile { version 2.0; format ascii; class volScalarField; object p; }\nboundaryField\n{\n    inlet   { type totalPressure; p0 uniform 11.3; value uniform 11.3; }\n    wall    { type zeroGradient; }\n    out_1   { type zeroGradient; }\n    out_2   { type zeroGradient; }\n    out_3   { type zeroGradient; }\n}\n' | sed -E "$ep" > "$D/pc/0/p"
    cm=$(case_mode "$D/pc"); why=$(prescribed_check "$D/pc" 2>&1); got=$?; m=$((m + 1))
    if [ "$got" = "$want" ] && [ "${cm%%:*}" = "${mode##*:}" ]; then printf 'self-test PASS  %-22s %s: %s\n' "$name" "$cm" "$why"; else pbad=$((pbad + 1)); printf 'self-test FAIL  %-22s expected %s/%s, got %s/%s (%s)\n' "$name" "$want" "${mode##*:}" "$got" "$cm" "$why"; fi
  done <<'E'
presc_ok|0|prescribed:prescribed|||1.0437238952330091e-07
presc_mode_conflict|0|resistance:conflict|||1.0437238952330091e-07
presc_q_mismatch|1|prescribed:prescribed|||1.0437239e-07
presc_q_ramp|1|prescribed:prescribed|s/volumetricFlowRate 1.0437238952e-07/volumetricFlowRate table ((0 0) (100 1.0437238952e-07))/||1.0437238952330091e-07
presc_u_inletoutlet|1|prescribed:prescribed|s/out_2   \{ type flowRateOutletVelocity;/out_2   { type inletOutlet; inletValue uniform (0 0 0);/||1.0437238952330091e-07
presc_u_missing|1|prescribed:prescribed|/out_2/d||1.0437238952330091e-07
presc_u_duplicate|1|prescribed:prescribed|/out_2/p||1.0437238952330091e-07
presc_extra_flow|1|prescribed:prescribed|s/out_3   \{ type noSlip; \}/out_3   { type flowRateOutletVelocity; volumetricFlowRate 1e-08; value uniform (0 0 0); }/||1.0437238952330091e-07
presc_p_fixed|1|prescribed:prescribed||s/out_1   \{ type zeroGradient; \}/out_1   { type fixedValue; value uniform 0; }/|1.0437238952330091e-07
presc_p_coded|1|prescribed:prescribed||s/out_2   \{ type zeroGradient; \}/out_2   { type codedFixedValue; value uniform 0; name res2; code #{ #}; }/|1.0437238952330091e-07
presc_q_nonpositive|1|prescribed:prescribed|s/1.0437238952e-07/0/||0
E
  rm -rf "$D"; echo "self-test (prescribed check): $((m - pbad))/$m passed"; [ $bad = 0 ] && [ $pbad = 0 ]; exit
fi
[ $# -ge 1 ] && [ $# -le 2 ] || { echo "usage: case_job.sh <case_dir> [ranks]  |  case_job.sh --self-test"; exit 2; }
NP=${2:-16}; END=${CASE_END:-3000}
[[ "$NP" =~ ^[1-9][0-9]*$ ]] || { echo "bad ranks '$NP'"; exit 2; }
[[ "$END" =~ ^[1-9][0-9]*$ ]] || { echo "bad CASE_END '$END'"; exit 2; }
NEED=${DISK_NEED_GB:-6}; RESERVE_GB=8; KEEP=${KEEP_PROCESSORS:-0}
[[ "$NEED" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "bad DISK_NEED_GB '$NEED' (GB, a non-negative number)"; exit 2; }
[[ "$KEEP" =~ ^[01]$ ]] || { echo "bad KEEP_PROCESSORS '$KEEP' (0 = purge after the verified reconstruct, 1 = keep)"; exit 2; }
C=$(cd "$1" 2>/dev/null && pwd) || { echo "no case dir $1"; exit 2; }
# OpenFOAM environment (attempt 3). The case dir and ranks are already in C/NP, so `set --` first: a bare source hands the job's "<case_dir> [ranks]" to the bashrc
# (config.sh/setup exports them as FOAM_SETTINGS and tries each as a settings file). The v2406 bashrc reads unset variables (fatal under `set -u`) and has commands returning
# non-zero (fatal under `set -e`), so -e/-u/pipefail are suspended ONLY around the source and restored right after, as in taskB/u3d_job.sh ($- read directly; `|| :` on the
# pipefail snapshot: `shopt -po` returns 1 when pipefail is off, which would kill the shell under `set -e`). Then the rc, the five tools and the version are checked.
if [ -z "${CASE_JOB_SKIP_FOAM_ENV:-}" ]; then
  set -- ; fo=$-; fp=$(shopt -po pipefail || :); set +eu +o pipefail; source "${CASE_JOB_FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}"; rc=$?; eval "$fp"; [[ $fo != *e* ]] || set -e; [[ $fo != *u* ]] || set -u
  [ $rc -eq 0 ] || { echo "FAILED: cannot source the OpenFOAM bashrc (rc $rc)"; exit 1; }
fi
for t in decomposePar simpleFoam reconstructPar mpirun foamDictionary; do command -v $t > /dev/null || { echo "FAILED: $t not on PATH after sourcing the OpenFOAM bashrc"; exit 1; }; done
[ "${WM_PROJECT_VERSION:-}" = v2406 ] || { echo "FAILED: WM_PROJECT_VERSION is '${WM_PROJECT_VERSION:-unset}', expected v2406"; exit 1; }
cd "$C" || { echo "no case dir $C"; exit 2; }

PROD_MADE=0; CHILD=""; CHILD_PG=0
fail() { echo "FAILED: $*"; exit 1; }
check_controls() {   # $1 = controlDict file; prints the first violation and returns 1
  local f=$1
  [ -f "$f" ] || { echo "$f missing"; return 1; }
  grep -qE "^startFrom +startTime;" "$f" || { echo "startFrom is not startTime in $f"; return 1; }
  grep -qE "^startTime +0;"         "$f" || { echo "startTime is not 0 in $f"; return 1; }
  grep -qE "^stopAt +endTime;"      "$f" || { echo "stopAt is not endTime in $f"; return 1; }
  grep -qE "^endTime +$END;"        "$f" || { echo "endTime is not $END in $f"; return 1; }
  ! grep -q "writeNow" "$f"              || { echo "$f contains 'writeNow'"; return 1; }
}
restore_controls() {   # production copy back over controlDict, byte-identical, production controls asserted
  cp system/controlDict.production system/controlDict && cmp -s system/controlDict.production system/controlDict && check_controls system/controlDict > /dev/null
}
kill_child() {   # stop the running external command (mpirun forwards TERM to its ranks; a POST_CMD hook runs in its own process group, which is signalled as a whole); KILL after 60 s
  [ -n "$CHILD" ] && kill -0 "$CHILD" 2> /dev/null || return 0
  local tgt=$CHILD i; [ "$CHILD_PG" = 1 ] && tgt=-$CHILD
  kill -TERM -- "$tgt" 2> /dev/null
  for i in $(seq 600); do kill -0 "$CHILD" 2> /dev/null || break; sleep 0.1; done
  [ "$CHILD_PG" = 1 ] && kill -KILL -- "$tgt" 2> /dev/null
  kill -0 "$CHILD" 2> /dev/null && { pkill -KILL -P "$CHILD" 2> /dev/null; kill -KILL "$CHILD" 2> /dev/null; }
  wait "$CHILD" 2> /dev/null; CHILD=""
}
run_child() {   # external commands run in the background and are waited for, so INT/TERM interrupt the wait at once instead of after the child
  "$@" & CHILD=$!; wait "$CHILD"; local rc=$?; CHILD=""; return $rc
}
run_child_pg() {   # as run_child, in a new process group (setsid execs in the background child, so $! is the group id): arbitrary hook commands are stopped with all their descendants
  CHILD_PG=1; setsid "$@" & CHILD=$!; wait "$CHILD"; local rc=$?; CHILD=""; CHILD_PG=0; return $rc
}
on_signal() { trap '' INT TERM; exec 1>&8 2>&8; echo "FAILED: received SIG$1, stopping the running command"; kill_child; exit "$2"; }
on_exit() {
  local rc=$?; trap - EXIT; trap '' INT TERM; exec 1>&8 2>&8   # a trap can fire inside a redirected command (e.g. > log.smoke): report on the job's own stdout
  kill_child
  if [ "$PROD_MADE" = 1 ]; then
    if restore_controls; then echo "controlDict: production copy restored and verified (cmp, endTime $END)"
    else echo "FATAL: system/controlDict could NOT be restored from system/controlDict.production: $(check_controls system/controlDict) - restore it by hand"; rc=4; fi
  fi
  exit $rc
}
exec 8>&1   # the job's own stdout, for the handlers
trap 'on_signal INT 130' INT; trap 'on_signal TERM 143' TERM; trap on_exit EXIT

# ---- ownership: one invocation per case for the whole run (fd 9 is inherited by the children, so the lock also outlives a killed script while its solver still runs)
exec 9> "$C/.case_job.lock" || fail "cannot open lock file $C/.case_job.lock"
flock -n 9 || { echo "REFUSED: $C is locked by another case_job.sh invocation ($C/.case_job.lock); concurrent runs on one case are not allowed"; exit 3; }

# ---- disk gate (READ-ONLY): the decomposed run plus its reconstruction must fit, with a reserve for the system
free_kb() { df -Pk -- "$C" | awk 'NR == 2 { print $4 }'; }
gb() { awk -v k="$1" 'BEGIN { printf "%.2f", k / 1048576 }'; }   # KiB -> GiB text
mb() { awk -v k="$1" 'BEGIN { printf "%.0f", k / 1024 }'; }
FREE0=$(free_kb); [[ "$FREE0" =~ ^[0-9]+$ ]] || fail "cannot read the free disk of the filesystem of $C (df)"
NEED_KB=$(awk -v n="$NEED" -v r="$RESERVE_GB" 'BEGIN { printf "%d", (n + r) * 1048576 }')
if [ "$FREE0" -lt "$NEED_KB" ]; then
  echo "REFUSED: not enough free disk for $C: $(gb "$FREE0") GB free on its filesystem ($(df -P -- "$C" | awk 'NR == 2 { print $6 }')), need DISK_NEED_GB $NEED + reserve $RESERVE_GB = $(gb "$NEED_KB") GB; free disk (e.g. purge the verified processor dirs of finished cases) first"; exit 5
fi
echo "$(date '+%F %T') disk gate OK: $(gb "$FREE0") GB free >= DISK_NEED_GB $NEED + reserve $RESERVE_GB GB"

# ---- strict stale-item refusal (READ-ONLY): a fresh case holds only 0/, constant/, system/ and inputs
STALE=()
for s in * .[!.]*; do
  [ -e "$s" ] || continue
  case "$s" in
    dynamicCode|postProcessing|processor*|log.*|*.status) STALE+=("$s");;
    *) [ -d "$s" ] && [[ "$s" =~ ^[-+]?([0-9]+[.]?[0-9]*|[.][0-9]+)([eE][-+]?[0-9]+)?$ ]] && [ "$s" != 0 ] && STALE+=("$s");;
  esac
done
[ -e system/controlDict.production ] && STALE+=("system/controlDict.production")
[ ${#STALE[@]} -eq 0 ] || fail "stale items in $C (remove them before a new run; a controlDict.production is the production copy of an earlier attempt): ${STALE[*]}"

MSG=$(check_controls system/controlDict) || fail "production controls: $MSG"
N=$(grep -E "^numberOfSubdomains" system/decomposeParDict | tr -dc 0-9); [ "$N" = "$NP" ] || fail "decomposeParDict has '$N' subdomains, expected $NP"
MODE=$(case_mode "$C"); [ "${MODE%%:*}" != conflict ] || fail "$MODE (prescribed mode needs both)"
if [ "$MODE" = prescribed ]; then   # WO1010 change: prescribed-flow case, no coded BC (see the header)
[ -f 0/p ] && [ -f 0/U ] || fail "0/p or 0/U missing (prescribed mode)"
PMSG=$(prescribed_check "$C" 2>&1) || fail "prescribed-flow BCs: $PMSG"
echo "$(date '+%F %T') prescribed mode (build_info.json): $PMSG"
if [ -n "${CASE_JOB_DRYRUN_STOP:-}" ]; then   # test/pre-flight hook, as below
  echo "$(date '+%F %T') DRY RUN: OpenFOAM $WM_PROJECT_VERSION sourced, tools on PATH, lock, disk gate, stale check, production controls, $NP subdomains and the prescribed-flow BCs OK; stop before the serial smoke and decomposePar"; exit 0
fi
else
[ -f 0/p ] || fail "0/p missing (the coded resistance BCs are derived from it)"
NAMES=$(grep -oE 'name +res[A-Za-z0-9_]+;' 0/p | sed -E 's/^name +res//; s/;$//')
[ -n "$NAMES" ] || fail "no 'name res<...>;' entry in 0/p (zero coded resistance BCs)"
DUP=$(printf '%s\n' $NAMES | sort | uniq -d | tr '\n' ' '); [ -z "$DUP" ] || fail "duplicate coded BC name(s) in 0/p: $DUP"
NN=$(printf '%s\n' $NAMES | wc -l)
if [ -n "${CASE_JOB_DRYRUN_STOP:-}" ]; then   # test/pre-flight hook: every read-only gate passed; stop before the first write and the first solver run (the serial smoke precedes decomposePar)
  echo "$(date '+%F %T') DRY RUN: OpenFOAM $WM_PROJECT_VERSION sourced, tools on PATH, lock, disk gate, stale check, production controls, $NP subdomains and $NN coded BCs OK; stop before the serial compile smoke and decomposePar"; exit 0
fi
fi

# ---- serial compile smoke (endTime 2); from here on the EXIT trap restores the production controlDict
cp system/controlDict system/controlDict.production && cmp -s system/controlDict system/controlDict.production || fail "cannot write system/controlDict.production"
PROD_MADE=1
run_child foamDictionary -entry endTime -set 2 system/controlDict > /dev/null || fail "cannot set smoke endTime"
grep -qE "^endTime +2;" system/controlDict || fail "smoke endTime 2 not set"
echo "$(date '+%F %T') serial compile smoke (2 iterations)"
run_child simpleFoam > log.smoke 2>&1 || fail "smoke run failed (rc $?), see log.smoke"
grep -qx End log.smoke || fail "smoke run has no exact 'End' line, see log.smoke"
[ "$(grep '^Time = ' log.smoke | tail -1 | awk '{print $3}')" = 2 ] || fail "smoke run did not reach Time = 2"
restore_controls || fail "controlDict not restored after the smoke"
if [ "$MODE" = prescribed ]; then
[ ! -e dynamicCode ] || fail "smoke built dynamicCode ($(ls dynamicCode | tr '\n' ' ')) in a prescribed-flow case, which has nothing coded"
else
for n in $NAMES; do ls dynamicCode/platforms/*/lib/libres${n}_*.so > /dev/null 2>&1 || fail "smoke: library for res$n not built"; done
[ "$(ls dynamicCode | wc -l)" -eq $((NN + 1)) ] || fail "dynamicCode has $(ls dynamicCode | wc -l) entries, expected $((NN + 1)) ($NN sources + platforms)"
fi
for s in *; do [ -d "$s" ] && [[ "$s" =~ ^[-+]?([0-9]+[.]?[0-9]*|[.][0-9]+)([eE][-+]?[0-9]+)?$ ]] && [ "$s" != 0 ] && { rm -rf "$s" || fail "cannot remove smoke time $s"; }; done
rm -rf postProcessing || fail "cannot remove smoke postProcessing"; mv log.smoke log.smoke.keep
if [ "$MODE" = prescribed ]; then echo "$(date '+%F %T') smoke OK (prescribed flow: no coded library, no dynamicCode), production controls restored and verified"
else echo "$(date '+%F %T') smoke OK ($NN coded libraries), production controls restored and verified"; fi

# ---- decompose
echo "$(date '+%F %T') decomposePar"
run_child decomposePar -force > log.decomposePar 2>&1 || fail "decomposePar failed, see log.decomposePar"
grep -qx End log.decomposePar || fail "log.decomposePar has no exact 'End' line"
ND=$(ls -d processor[0-9]* 2> /dev/null | wc -l); [ "$ND" -eq "$NP" ] || fail "decomposePar produced $ND processor directories, expected $NP"

# ---- solve
date '+%F %T' > log.solve_start   # reference stamp: the reconstructed fields must be newer than this file
echo "$(date '+%F %T') solve start ($NP ranks)"
run_child mpirun -np "$NP" --bind-to none --mca mpi_yield_when_idle 1 simpleFoam -parallel > log.simpleFoam 2>&1; rc=$?
echo "$(date '+%F %T') solve end rc=$rc"
MSG=$(solve_complete "$rc" log.simpleFoam "$END") || fail "$MSG"
LAST=$(grep "^Time = " log.simpleFoam | tail -1 | awk '{print $3}')

# ---- reconstruct and verify (as taskC/pf/post_helpers.py reconstruct_check)
latest_time() { local d=$1 s; for s in "$d"/*; do s=${s##*/}; [ -d "$d/$s" ] && [[ "$s" =~ ^[-+]?([0-9]+[.]?[0-9]*|[.][0-9]+)([eE][-+]?[0-9]+)?$ ]] && echo "$s"; done | sort -g | tail -1; }
num_eq() { awk -v a="$1" -v b="$2" 'BEGIN { exit !(a != "" && b != "" && a + 0 == b + 0) }'; }
run_child nice -n 10 reconstructPar -latestTime > log.reconstructPar 2>&1 || fail "reconstructPar failed, see log.reconstructPar"
grep -qx End log.reconstructPar || fail "log.reconstructPar has no exact 'End' line"
TP0=$(latest_time processor0); TR=$(latest_time .)
num_eq "$TP0" "$END" || fail "processor0 latest time '$TP0' != endTime $END"
num_eq "$TR" "$TP0" || fail "latest reconstructed time '$TR' != processor0 latest time '$TP0'"
num_eq "$TR" "$LAST" || fail "latest reconstructed time '$TR' != last log Time '$LAST'"
for f in U p phi; do
  [ -s "$TR/$f" ] || fail "reconstructed field $TR/$f missing or empty"
  [ "$TR/$f" -nt log.solve_start ] || fail "reconstructed field $TR/$f is not newer than the solve start (log.solve_start)"
done
restore_controls || fail "production controlDict check failed at the end"
echo "$(date '+%F %T') reconstruct verified (time $TR; U, p, phi non-empty and newer than the solve start)"

# ---- optional post hook: its failure fails the job (the scheduler marks a job done only on rc 0); the processor dirs are still there
if [ -n "${POST_CMD:-}" ]; then
  echo "$(date '+%F %T') POST_CMD: $POST_CMD"
  CASE_DIR=$C CASE_END=$END CASE_NP=$NP run_child_pg bash -c "$POST_CMD" > log.post 2>&1; prc=$?
  [ $prc -eq 0 ] || fail "POST_CMD failed (rc $prc), see log.post; processor dirs kept"
  echo "$(date '+%F %T') POST_CMD OK (rc 0, log.post)"
fi

# ---- disk staging: purge the decomposed duplicates only now, after every check and the hook have passed
if [ "$KEEP" = 1 ]; then
  echo "$(date '+%F %T') OK: solve and reconstruct done (time $TR; U, p, phi verified; processor dirs kept: KEEP_PROCESSORS=1, disk released 0.00 GB)"
  exit 0
fi
PD=(processor[0-9]*); [ "${#PD[@]}" -eq "$NP" ] && [ -d "${PD[0]}" ] || fail "expected $NP processor dirs before the purge, found ${#PD[@]}: nothing purged"
DU=$(du -skc -- "${PD[@]}" | tail -1 | cut -f1); FREE1=$(free_kb)
rm -rf -- "${PD[@]}"; LEFT=$(ls -d processor[0-9]* 2> /dev/null | wc -l)
[ "$LEFT" -eq 0 ] || fail "purge incomplete: $LEFT processor dirs left (the reconstructed time $TR is verified and kept)"
FREE2=$(free_kb)
echo "$(date '+%F %T') PURGED: ${#PD[@]} processor dirs, disk released $(gb "$DU") GB ($(mb "$DU") MB, du; df free $(gb "$FREE1") -> $(gb "$FREE2") GB); kept: $TR/, 0/, constant/, system/, postProcessing, log.*"
echo "$(date '+%F %T') OK: solve and reconstruct done (time $TR; U, p, phi verified; processor dirs purged, disk released $(gb "$DU") GB)"
