#!/bin/bash
# Umbrella of ONE B2 run (started by b2_run.sh with setsid, so this process is the session leader and every job process belongs to its session).
# usage: b2_jobs.sh <L16|L8x2> <results_dir>   (env: B2_ROOT, B2_MPIRUN, B2_SKIP_FOAM_ENV; OpenFOAM environment sourced by the caller)
# L16: one job, 16 ranks, cases b2/L16/case, cpus 0-31 (all 16 physical cores).  L8x2: two jobs, 8 ranks each, b2/L8/caseA on cpus 0-15 (cores 0-7) and b2/L8/caseB on cpus 16-31 (cores 8-15).
# Each mpirun: --bind-to none and the per-rank wrapper b2_rank.sh (taskset of rank r to the two logical CPUs of physical core (base/2 + r); OpenMPI ignores a taskset on mpirun and --cpu-set fails silently here). Writes <results_dir>/job_rc.txt ("<case> <rc>" per job).
HERE=$(cd "$(dirname "$0")" && pwd); B=${B2_ROOT:-/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot/b2}; LAYOUT=$1; OUT=$2; MPIRUN=${B2_MPIRUN:-mpirun}
case "$LAYOUT" in L16) CASES=("$B/L16/case"); NPJ=16; BASES=(0);; L8x2) CASES=("$B/L8/caseA" "$B/L8/caseB"); NPJ=8; BASES=(0 16);; *) echo "usage: b2_jobs.sh <L16|L8x2> <results_dir>" >&2; exit 2;; esac
PIDS=(); i=0
for c in "${CASES[@]}"; do
    ( cd "$c" && export B2_CPU_BASE="${BASES[$i]}" && exec $MPIRUN -np "$NPJ" --bind-to none "$HERE/b2_rank.sh" simpleFoam -parallel > log.simpleFoam 2> mpirun_bindings.txt ) &
    PIDS+=($!); i=$((i+1))
done
: > "$OUT/job_rc.txt"
for k in "${!PIDS[@]}"; do wait "${PIDS[$k]}"; echo "${CASES[$k]} $?" >> "$OUT/job_rc.txt"; done
