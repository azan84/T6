#!/bin/bash
# Generalisation of the audited run_pair.sh to any set of cases (usage: run_set.sh <case_dir_name> ...): serial 2-iteration compile smoke (per case) -> restore + assert production controls -> decomposePar -> all solves concurrently.
# Rank counts are read from each decomposeParDict; their SUM must not exceed the logical CPU count (nproc), so no oversubscription. Every background step is waited for individually; any failure aborts before the
# next phase and restores the production controlDict. Start with:  setsid nohup ./run_set.sh <cases...> > run_set.log 2>&1 &
# A refusal is mutation-free: every case is validated READ-ONLY first (disk, ranks, stale items, the controlDict that WOULD be used); only then are controlDicts written, and an abort
# restores only the cases this invocation has itself begun to mutate (MUTATED). A non-blocking flock on $P/.run_set.lock excludes concurrent invocations.
# Test hooks (used only by the failure-injection tests): PAIR_ROOT, PAIR_SKIP_FOAM_ENV=1, PAIR_MIN_GB, PAIR_SETTLE_S, PAIR_NPROC.
P=${PAIR_ROOT:-/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot}
CASES="$*"
[ -n "$CASES" ] || { echo "usage: run_set.sh <case_dir_name> ..." >&2; exit 2; }
NCPU=${PAIR_NPROC:-$(nproc)}
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
assert_controls() {   # $1 = label, $2 = controlDict file (default $1/system/controlDict)
  local f="${2:-$1/system/controlDict}"
  [ -f "$f" ] || fail "$1: $f missing"
  grep -qE "^startFrom +startTime;" "$f" || fail "$1: startFrom is not startTime in $f"
  grep -qE "^startTime +0;"        "$f" || fail "$1: startTime is not 0 in $f"
  grep -qE "^stopAt +endTime;"     "$f" || fail "$1: stopAt is not endTime in $f"
  grep -qE "^endTime +3000;"       "$f" || fail "$1: endTime is not 3000 in $f"
  ! grep -q "writeNow" "$f"        || fail "$1: $f contains 'writeNow'"
}

# ---- 0a. READ-ONLY validation of ALL cases (nothing is written before every case has passed)
AVAIL=$(df --output=avail -B1 / | tail -1 | tr -dc 0-9)
[ "$AVAIL" -ge "$MIN_BYTES" ] || fail "only $AVAIL bytes free on / (< $MIN_BYTES)"

TOTAL_RANKS=0
for c in $CASES; do
  [ -f "$P/$c/system/decomposeParDict" ] || fail "$c: $P/$c/system/decomposeParDict missing"
  NPc=$(grep numberOfSubdomains "$P/$c/system/decomposeParDict" | tr -dc 0-9 || true); [ -n "$NPc" ] && [ "$NPc" -ge 1 ] || fail "$c: bad numberOfSubdomains"
  TOTAL_RANKS=$((TOTAL_RANKS + NPc))
done
[ "$TOTAL_RANKS" -le "$NCPU" ] || fail "total ranks $TOTAL_RANKS exceed logical CPUs $NCPU (oversubscription forbidden)"

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
done

# ---- 0b. mutation pass: production controlDict in place (restored copy or fresh snapshot)
for c in $CASES; do
  d="$P/$c"
  MUTATED="$MUTATED $c"   # set before the first write to this case
  if [ -f "$d/system/controlDict.production" ]; then cp "$d/system/controlDict.production" "$d/system/controlDict"
  else cp "$d/system/controlDict" "$d/system/controlDict.production"; fi
  assert_controls "$d"
done

# ---- 1. serial smoke (compiles the 5 coded BCs; no MPI ranks race for the dynamicCode build)
smoke() {
  local d="$P/$1"; cd "$d"
  sed -i 's/^endTime .*/endTime         2;/' system/controlDict
  simpleFoam > log.smoke 2>&1 9>&-
  grep -q "^End" log.smoke || fail "$1: smoke run did not reach End"
  for n in LCX IM D1 D2 LAD; do ls dynamicCode/platforms/*/lib/libres${n}_*.so > /dev/null 2>&1 || fail "$1: library for res$n not built"; done
  [ "$(ls dynamicCode | wc -l)" -eq 6 ] || fail "$1: dynamicCode has $(ls dynamicCode | wc -l) entries, expected 6 (5 sources + platforms)"
  rm -rf 2 1 postProcessing                                # smoke output must not shadow the production run's monitors
  cp system/controlDict.production system/controlDict
  assert_controls "$d"
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
for c in $CASES; do assert_controls "$P/$c"; done           # final gate before any production launch
LAUNCHED=1; trap - INT TERM                                  # production solves are independent of this shell from here on

# ---- 3. concurrent production solves (rank counts from each decomposeParDict; their sum <= nproc)
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
