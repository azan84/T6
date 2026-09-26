#!/bin/bash
# Queue 4 (after queue3 finished): post-process T1/clean resistance solves (probes, results rows; processors purged), then the scan-14 PRESCRIBED-flow solves (all outlets simultaneously) and their ROUND TRIPS,
# baseline first, then T1_missed_branch (PILOT), then clean_nolesion; one solve at a time at 16 ranks. Stops on: <12 GB disk, launcher failure, missing End line, failed analysis. Never kills anything. Log u3d/queue4.log
P=/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot; cd $P
log() { echo "$(date '+%F %T') $*" >> u3d/queue4.log; }
idle() { while pgrep -f "run_set_generic.sh|simpleFoam" > /dev/null; do sleep 30; done; }
diskok() { [ "$(df --output=avail -B1G / | tail -1 | tr -dc 0-9)" -ge 12 ]; }
log "queue4 started"
until grep -q "queue3 finished" u3d/queue3.log 2>/dev/null; do grep -q "STOP" u3d/queue3.log && { log "queue3 stopped: queue4 does not run"; exit 1; }; sleep 60; done
idle; log "host idle"
for L in T1_missed_branch clean_nolesion; do
  m1/post_case.sh $L resistance >> u3d/queue4.log 2>&1 || { log "post $L resistance failed: STOP"; exit 1; }
  rm -rf m1/cases/${L}_resistance/processor*; log "post $L resistance done, processors purged"
done
for L in baseline T1_missed_branch clean_nolesion; do
  PKG=14_left_LAD_prox_20mm_80ds__${L}__real; PC=m1/cases/${L}_prescribed; RC=m1/cases/${L}_roundtrip
  idle; diskok || { log "disk < 12 GB before $L prescribed: STOP"; exit 1; }
  log "launching $PC"
  RUN_SET_ALLOW_NO_CODED=1 ./run_set_generic.sh $PC > $PC.run_set.log 2>&1; rc=$?; log "$L prescribed launcher rc=$rc"
  [ $rc -eq 0 ] && grep -q "^End" $PC/log.simpleFoam || { log "$L prescribed did not finish cleanly: STOP"; exit 1; }
  python3 pf/analyze_case.py $PC --json $PC/analysis_pf.json >> u3d/queue4.log 2>&1 || { log "analysis $L prescribed failed: STOP"; exit 1; }
  python3 pf/build_m1_case.py $PKG $PC roundtrip 16 >> u3d/queue4.log 2>&1 || { log "roundtrip build $L failed: STOP"; exit 1; }
  idle; diskok || { log "disk < 12 GB before $L roundtrip: STOP"; exit 1; }
  log "launching $RC"
  ./run_set_generic.sh $RC > $RC.run_set.log 2>&1; rc=$?; log "$L roundtrip launcher rc=$rc"
  [ $rc -eq 0 ] && grep -q "^End" $RC/log.simpleFoam || { log "$L roundtrip did not finish cleanly: STOP"; exit 1; }
  python3 pf/analyze_case.py $RC --json $RC/analysis_pf.json >> u3d/queue4.log 2>&1 || { log "analysis $L roundtrip failed: STOP"; exit 1; }
  python3 pf/pf_roundtrip_analyse.py $PC $RC >> u3d/queue4.log 2>&1 || { log "roundtrip analyse $L failed: STOP"; exit 1; }
  m1/post_case.sh $L prescribed >> u3d/queue4.log 2>&1 || { log "post $L prescribed failed: STOP"; exit 1; }
  rm -rf $PC/processor* $RC/processor*; log "$L prescribed + roundtrip done, processors purged"
done
log "queue4 finished"
