#!/bin/bash
# queue_checked.sh = queue4.sh with the post-hoc audit fixes, for FUTURE queues (queue4.sh itself is unchanged): post-process T1/clean resistance solves (probes, results rows; processors purged), then the scan-14
# PRESCRIBED-flow solves (all outlets simultaneously) and their ROUND TRIPS, baseline first, then T1_missed_branch (PILOT), then clean_nolesion; one solve at a time at 16 ranks. Never kills anything.
# Stops on: < 12 GiB free disk, launcher failure, missing End line, any non-zero exit of an analysis/build/post step. The analyses run with --strict-exit (exit 3 = case not CONVERGED/finished, or round trip
# not PASS), so an UNCONVERGED / FAIL / NOT ASSESSABLE result stops the queue BEFORE post-processing and BEFORE any purge: on every STOP the processor directories are kept and the reason is logged.
# Log: u3d/<script name>.log (queue_checked.log for this file).
# Test hooks: QUEUE_ROOT (default P), QUEUE_DRY_RUN=1 (solver launches, case builds, post_case.sh, purges and the idle wait are PRINTED, not run; the read-only analyses and every check still run).
P=${QUEUE_ROOT:-/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot}; cd $P || exit 1
NAME=$(basename "$0" .sh); LOG=u3d/$NAME.log
FLOOR_BYTES=$((12 * 1024 * 1024 * 1024))
log() { echo "$(date '+%F %T') $*" >> $LOG; }
dry() { [ "${QUEUE_DRY_RUN:-}" = 1 ]; }
exec 3>&1                                                                          # the queue's own stdout (step output goes to the log)
act() { if dry; then echo "DRY-RUN: $*" >&3; echo "DRY-RUN: $*" >> $LOG; else "$@"; fi; }          # solver/mesher/builder/purge steps
stop() { log "$*: STOP (processor directories kept)"; exit 1; }
idle() { if dry; then echo "DRY-RUN: idle wait skipped" >&3; log "DRY-RUN: idle wait skipped"; return; fi; while pgrep -f "run_set_generic.sh|simpleFoam" > /dev/null; do sleep 30; done; }
# exact floor in bytes (-B1G rounds up: 11.2 GiB would read as 12). PRE-LAUNCH check only: nothing monitors the disk while a solve runs.
diskok() { local a; a=$(df --output=avail -B1 / | tail -1 | tr -dc 0-9); [ -n "$a" ] && [ "$a" -ge $FLOOR_BYTES ]; }
[ "${QUEUE_SOURCE_ONLY:-}" = 1 ] && { return 0 2>/dev/null || exit 0; }        # tests: define the functions only
log "$NAME started${QUEUE_DRY_RUN:+ (DRY RUN)}"
until grep -q "queue3 finished" u3d/queue3.log 2>/dev/null; do grep -q "STOP" u3d/queue3.log && { log "queue3 stopped: $NAME does not run"; exit 1; }; sleep 60; done
idle; log "host idle"
for L in T1_missed_branch clean_nolesion; do
  act m1/post_case.sh $L resistance >> $LOG 2>&1 || stop "post $L resistance failed (rc=$?)"
  act rm -rf m1/cases/${L}_resistance/processor*; log "post $L resistance done, processors purged"
done
for L in baseline T1_missed_branch clean_nolesion; do
  PKG=14_left_LAD_prox_20mm_80ds__${L}__real; PC=m1/cases/${L}_prescribed; RC=m1/cases/${L}_roundtrip
  idle; diskok || stop "disk < 12 GiB ($(df --output=avail -B1 / | tail -1 | tr -dc 0-9) bytes free) before $L prescribed"
  log "launching $PC"
  RUN_SET_ALLOW_NO_CODED=1 act ./run_set_generic.sh $PC > $PC.run_set.log 2>&1; rc=$?; log "$L prescribed launcher rc=$rc"
  [ $rc -eq 0 ] && grep -q "^End" $PC/log.simpleFoam || stop "$L prescribed did not finish cleanly"
  python3 pf/analyze_case.py $PC --json $PC/analysis_pf.json --strict-exit >> $LOG 2>&1; rc=$?; [ $rc -eq 0 ] || stop "analysis $L prescribed rc=$rc (3 = not CONVERGED/finished)"
  act python3 pf/build_m1_case.py $PKG $PC roundtrip 16 >> $LOG 2>&1 || stop "roundtrip build $L failed (rc=$?)"
  idle; diskok || stop "disk < 12 GiB ($(df --output=avail -B1 / | tail -1 | tr -dc 0-9) bytes free) before $L roundtrip"
  log "launching $RC"
  act ./run_set_generic.sh $RC > $RC.run_set.log 2>&1; rc=$?; log "$L roundtrip launcher rc=$rc"
  [ $rc -eq 0 ] && grep -q "^End" $RC/log.simpleFoam || stop "$L roundtrip did not finish cleanly"
  python3 pf/analyze_case.py $RC --json $RC/analysis_pf.json --strict-exit >> $LOG 2>&1; rc=$?; [ $rc -eq 0 ] || stop "analysis $L roundtrip rc=$rc (3 = not CONVERGED/finished)"
  python3 pf/pf_roundtrip_analyse.py $PC $RC --strict-exit >> $LOG 2>&1; rc=$?; [ $rc -eq 0 ] || stop "roundtrip analyse $L rc=$rc (3 = status not PASS)"
  act m1/post_case.sh $L prescribed >> $LOG 2>&1 || stop "post $L prescribed failed (rc=$?)"
  act rm -rf $PC/processor* $RC/processor*; log "$L prescribed + roundtrip done, processors purged"
done
log "$NAME finished"
