#!/bin/bash
# run_set_generic.sh = run_set.sh with the coded resistance-BC set derived per case from 0/p and a fixed rank cap (usage: run_set_generic.sh <case_dir_name> ...): serial 2-iteration compile smoke (per case) -> restore + assert production controls -> decomposePar -> all solves concurrently.
# Rank counts are read from each decomposeParDict; their SUM must not exceed RUN_SET_MAX_RANKS (default 16 = physical cores; work-order rule: total ranks over all concurrent jobs <= 16).
# The expected libres<stem>_*.so set is derived READ-ONLY in 0a from the 'name res<stem>;' entries of each case's 0/p (missing 0/p, no names [unless RUN_SET_ALLOW_NO_CODED=1, below] or a duplicate name = refusal); dynamicCode must hold (names + 1) entries. Every background step is waited for individually; any failure aborts before the
# next phase and restores the production controlDict. Start with:  setsid nohup ./run_set.sh <cases...> > run_set.log 2>&1 &
# A refusal is mutation-free: every case is validated READ-ONLY first (disk, ranks, stale items, the controlDict that WOULD be used); only then are controlDicts written, and an abort
# restores only the cases this invocation has itself begun to mutate (MUTATED). A non-blocking flock on $P/.run_set.lock excludes concurrent invocations.
# Opt-in for coded-free (prescribed-flow) cases: with RUN_SET_ALLOW_NO_CODED=1 (only the value 1), a case whose 0/p holds zero 'name res<...>;' entries is accepted iff no file under its 0/ contains
# 'codedFixedValue', 'codedMixed' or '#{' (else the refusal stands); its name list is empty and its smoke must leave NO dynamicCode directory. Coded and coded-free cases may be mixed in one call.
# Per-case production endTime: assert_controls requires 'endTime <E>;' where E = 3000 unless RUN_SET_END_MAP (optional, comma-separated case=endTime pairs, case exactly as given on the command line, e.g.
# 'u3d/wedge_W3=9000,pf_item1/pf_ds60_prescribed=3000'; endTime = 1-6 digits without a leading zero) sets it. Unset/empty = 3000 for every case. The map is validated READ-ONLY at the start of 0a
# (malformed entry, duplicate key, key that is not a case argument or a bad value = mutation-free refusal); the smoke still runs with endTime 2 and then restores and re-asserts the case's own E.
# Test hooks (used only by the failure-injection tests): PAIR_ROOT, PAIR_SKIP_FOAM_ENV=1, PAIR_MIN_GB, PAIR_SETTLE_S, PAIR_NPROC (overrides RUN_SET_MAX_RANKS when set).
# Shares $P/.run_set.lock with run_set.sh on purpose: the two launchers can never run at once (their rank caps are per invocation, and both write the same cases' controls).
P=${PAIR_ROOT:-/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot}
CASES="$*"
[ -n "$CASES" ] || { echo "usage: run_set.sh <case_dir_name> ..." >&2; exit 2; }
if [ -n "${PAIR_NPROC:-}" ]; then NCPU=$PAIR_NPROC; NCPU_SRC="PAIR_NPROC override"
elif [ -n "${RUN_SET_MAX_RANKS:-}" ]; then NCPU=$RUN_SET_MAX_RANKS; NCPU_SRC="RUN_SET_MAX_RANKS"
else NCPU=16; NCPU_SRC="default rank cap (16 physical cores)"; fi
MIN_BYTES=$(( ${PAIR_MIN_GB:-10} * 1024 * 1024 * 1024 ))
if [ -z "${PAIR_SKIP_FOAM_ENV:-}" ]; then source /usr/lib/openfoam/openfoam2406/etc/bashrc; fi   # before any strict shell options (its bashrc uses unset variables)
set -eo pipefail

fail() { echo "FAIL: $*" >&2; exit 1; }
SEEN=" "; for c in $CASES; do case "$SEEN" in *" $c "*) fail "duplicate case argument '$c'";; esac; SEEN="$SEEN$c "; done
exec 9> "$P/.run_set.lock" || fail "cannot open lock file $P/.run_set.lock"
flock -n 9 || fail "another run_set.sh holds $P/.run_set.lock: concurrent invocations are refused"   # held (fd 9) for the whole life of this script; external commands get 9>&-

MUTATED=""   # cases whose controlDict(.production) this invocation has begun to write: the only ones an abort may restore
restore_all() { for c in $MUTATED; do [ -f "$P/$c/system/controlDict.production" ] && cp "$P/$c/system/controlDict.production" "$P/$c/system/controlDict"; done; return 0; }
LAUNCHED=""
pids=()
wait_all() { local f=0 p; for p in "$@"; do wait "$p" || f=1; done; return $f; }   # wait for EVERY job: an abort must never restore controls under a still-running serial smoke
kill_children() { local p; for p in "${pids[@]}"; do pkill -TERM -P "$p" 2>/dev/null || true; kill "$p" 2>/dev/null || true; done; }
trap 'echo "signal received: stopping background jobs"; kill_children; sleep 1; exit 143' INT TERM
trap 'rc=$?; if [ "$rc" -ne 0 ] && [ -z "$LAUNCHED" ]; then echo "ABORT (rc=$rc): restoring production controlDicts of the cases this run modified: [${MUTATED# }]"; restore_all; fi' EXIT
assert_controls() {   # $1 = case (as given on the command line), $2 = controlDict file (default $P/$1/system/controlDict); expected endTime = ${ENDTIME[$1]}
  local f="${2:-$P/$1/system/controlDict}" e="${ENDTIME[$1]:-}"
  [ -n "$e" ] || fail "$1: no expected endTime (internal error)"
  [ -f "$f" ] || fail "$1: $f missing"
  grep -qE "^startFrom +startTime;" "$f" || fail "$1: startFrom is not startTime in $f"
  grep -qE "^startTime +0;"        "$f" || fail "$1: startTime is not 0 in $f"
  grep -qE "^stopAt +endTime;"     "$f" || fail "$1: stopAt is not endTime in $f"
  grep -qE "^endTime +$e;"         "$f" || fail "$1: endTime is not $e in $f"
  ! grep -q "writeNow" "$f"        || fail "$1: $f contains 'writeNow'"
}

# ---- 0a. READ-ONLY validation of ALL cases (nothing is written before every case has passed)
declare -A ENDTIME   # case -> expected production endTime (RUN_SET_END_MAP entry, else 3000)
for c in $CASES; do ENDTIME[$c]=3000; done
MAP="${RUN_SET_END_MAP:-}"
if [ -n "$MAP" ]; then
  case "$MAP" in *[[:space:]]*|,*|*,|*,,*) fail "RUN_SET_END_MAP '$MAP' is malformed (whitespace or empty entry; expected case=endTime[,case=endTime...])";; esac
  MAPKEYS=" "; IFS=, read -ra ENTRIES <<< "$MAP"
  for en in "${ENTRIES[@]}"; do
    [[ "$en" =~ ^([^=]+)=([^=]*)$ ]] || fail "RUN_SET_END_MAP entry '$en' is malformed (expected case=endTime)"
    k=${BASH_REMATCH[1]}; v=${BASH_REMATCH[2]}
    [[ "$v" =~ ^[1-9][0-9]{0,5}$ ]] || fail "RUN_SET_END_MAP entry '$en': endTime '$v' is not a positive integer (digits only, no leading zero, at most 6 digits)"
    case "$MAPKEYS" in *" $k "*) fail "RUN_SET_END_MAP: duplicate key '$k'";; esac; MAPKEYS="$MAPKEYS$k "
    case "$SEEN" in *" $k "*) ;; *) fail "RUN_SET_END_MAP: key '$k' is not one of the case arguments [$CASES]";; esac
    ENDTIME[$k]=$v
  done
fi
for c in $CASES; do echo "$c: expected production endTime ${ENDTIME[$c]}"; done
AVAIL=$(df --output=avail -B1 / | tail -1 | tr -dc 0-9)
[ "$AVAIL" -ge "$MIN_BYTES" ] || fail "only $AVAIL bytes free on / (< $MIN_BYTES)"

TOTAL_RANKS=0
declare -A RESNAMES   # case -> library stems derived from its 0/p (reused by the smoke phase)
for c in $CASES; do
  [ -f "$P/$c/system/decomposeParDict" ] || fail "$c: $P/$c/system/decomposeParDict missing"
  NPc=$(grep numberOfSubdomains "$P/$c/system/decomposeParDict" | tr -dc 0-9 || true); [ -n "$NPc" ] && [ "$NPc" -ge 1 ] || fail "$c: bad numberOfSubdomains"
  TOTAL_RANKS=$((TOTAL_RANKS + NPc))
done
[ "$TOTAL_RANKS" -le "$NCPU" ] || fail "total ranks $TOTAL_RANKS exceed the rank limit $NCPU set by $NCPU_SRC (oversubscription forbidden)"

for c in $CASES; do
  d="$P/$c"
  [ ! -d "$d/processor0" ] || fail "$c already decomposed"
  for s in "$d"/* "$d"/.[!.]*; do   # a fresh case holds none of these: stale output would mix with the new run (or be restored over it)
    b=$(basename "$s"); [ -e "$s" ] || continue
    case "$b" in
      log.simpleFoam|log.smoke|postProcessing|dynamicCode|processor*) fail "$c: stale item '$b' in $d (remove it before a new run)";;
    esac
    if [ -d "$s" ] && [[ "$b" =~ ^[-+]?([0-9]+[.]?[0-9]*|[.][0-9]+)([eE][-+]?[0-9]+)?$ ]] && [ "$b" != 0 ]; then fail "$c: stale time directory '$b' in $d (only 0 is allowed before a new run)"; fi
  done
  if [ -f "$d/system/controlDict.production" ]; then assert_controls "$c" "$d/system/controlDict.production"   # an aborted earlier attempt: its production copy is what would be used
  else assert_controls "$c" "$d/system/controlDict"; fi
  [ -f "$d/0/p" ] || fail "$c: $d/0/p missing (the coded resistance BCs are derived from it)"
  NAMES=$(grep -oE 'name +res[A-Za-z0-9_]+;' "$d/0/p" | sed -E 's/^name +res//; s/;$//' || true)
  if [ -z "$NAMES" ]; then   # coded-free case: accepted only on explicit opt-in and only if 0/ holds no coded BC at all
    if [ "${RUN_SET_ALLOW_NO_CODED:-}" = 1 ] && { grep -rqF -e codedFixedValue -e codedMixed -e '#{' "$d/0"; [ $? -eq 1 ]; }; then RESNAMES[$c]=""; continue; fi   # grep exit 1 = no coded block; a grep error (2) refuses
    fail "$c: no 'name res<...>;' entry in $d/0/p (zero coded resistance BCs)"
  fi
  DUP=$(printf '%s\n' $NAMES | sort | uniq -d | tr '\n' ' ')
  [ -z "$DUP" ] || fail "$c: duplicate coded BC name(s) in $d/0/p: ${DUP% }"
  RESNAMES[$c]=$(echo $NAMES)
done

# ---- 0b. mutation pass: production controlDict in place (restored copy or fresh snapshot)
for c in $CASES; do
  d="$P/$c"
  MUTATED="$MUTATED $c"   # set before the first write to this case
  if [ -f "$d/system/controlDict.production" ]; then cp "$d/system/controlDict.production" "$d/system/controlDict"
  else cp "$d/system/controlDict" "$d/system/controlDict.production"; fi
  assert_controls "$c"
done

# ---- 1. serial smoke (compiles the coded BCs derived from 0/p; no MPI ranks race for the dynamicCode build)
smoke() {
  local d="$P/$1"; cd "$d"
  sed -i 's/^endTime .*/endTime         2;/' system/controlDict
  simpleFoam > log.smoke 2>&1 9>&-
  grep -q "^End" log.smoke || fail "$1: smoke run did not reach End"
  local NN=0 n; for n in ${RESNAMES[$1]}; do NN=$((NN + 1)); done
  if [ "$NN" -eq 0 ]; then [ ! -e dynamicCode ] || fail "$1: dynamicCode exists for a case declared coded-free"   # only reachable via RUN_SET_ALLOW_NO_CODED=1
  else
  for n in ${RESNAMES[$1]}; do ls dynamicCode/platforms/*/lib/libres${n}_*.so > /dev/null 2>&1 || fail "$1: library for res$n not built"; done
  [ "$(ls dynamicCode | wc -l)" -eq $((NN + 1)) ] || fail "$1: dynamicCode has $(ls dynamicCode | wc -l) entries, expected $((NN + 1)) ($NN sources + platforms)"
  fi
  rm -rf 2 1 postProcessing                                # smoke output must not shadow the production run's monitors
  cp system/controlDict.production system/controlDict
  assert_controls "$1"
  echo "$1: smoke OK, production controls restored and asserted"
}
pids=(); for c in $CASES; do smoke "$c" & pids+=($!); done
wait_all "${pids[@]}" || fail "a smoke run failed"

# ---- 2. decompose into the number of domains in the dict
decomp() {
  local d="$P/$1"; cd "$d"
  local NP; NP=$(grep numberOfSubdomains system/decomposeParDict | tr -dc 0-9)
  decomposePar -force > log.decomposePar 2>&1 9>&-
  [ "$(ls -d processor* | wc -l)" -eq "$NP" ] || fail "$1: processor directory count != $NP"
  echo "$1: decomposed into $NP"
}
pids=(); for c in $CASES; do decomp "$c" & pids+=($!); done
wait_all "${pids[@]}" || fail "a decomposition failed"
for c in $CASES; do assert_controls "$c"; done              # final gate before any production launch
LAUNCHED=1; trap - INT TERM                                  # production solves are independent of this shell from here on

# ---- 3. concurrent production solves (rank counts from each decomposeParDict; their sum <= the rank limit)
run() {
  local d="$P/$1"; cd "$d"
  local NP; NP=$(grep numberOfSubdomains system/decomposeParDict | tr -dc 0-9)
  mpirun -np "$NP" --use-hwthread-cpus --bind-to none --mca mpi_yield_when_idle 1 simpleFoam -parallel > log.simpleFoam 2>&1 9>&-
}
pids=(); for c in $CASES; do run "$c" & pids+=($!); done
sleep "${PAIR_SETTLE_S:-60}"
for c in $CASES; do echo "== $c"; tail -3 "$P/$c/log.simpleFoam" | cut -c1-150; done
echo "launched: all solves running"
rc=0; for p in "${pids[@]}"; do wait "$p" || rc=1; done
echo "solves finished (rc=$rc)"; exit $rc
