#!/bin/bash
# Queue 2 (after the running S25B): post S25B; S12B (3000, design v2.6); post S12B; then the three scan-14 RESISTANCE-mode solves (work-order priority 4), one at a time at 16 ranks
# (m1/cases/baseline_resistance, T1_missed_branch_resistance, clean_nolesion_resistance; 3000 iterations; strict analysis via pf/analyze_case.py; no purge: fields are needed for probes).
# Stops (never continues) on: <12 GB free disk, a launcher failure, a missing End line, a failed analysis. Never kills anything. Log: u3d/queue2.log
P=/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot; cd $P
log() { echo "$(date '+%F %T') $*" >> u3d/queue2.log; }
idle() { while pgrep -f "run_set_generic.sh|simpleFoam" > /dev/null; do sleep 30; done; }
diskok() { [ "$(df --output=avail -B1G / | tail -1 | tr -dc 0-9)" -ge 12 ]; }
log "queue2 started"
idle; log "host idle: post-processing S25B"
u3d/post_level.sh S25B no purge >> u3d/queue2.log 2>&1 || { log "post S25B failed: STOP"; exit 1; }
idle; diskok || { log "disk < 12 GB before S12B: STOP"; exit 1; }
log "launching S12B (endTime 3000)"
RUN_SET_END_MAP="u3d/case_S12B=3000" ./run_set_generic.sh u3d/case_S12B > u3d/run_set_S12B.log 2>&1; rc=$?
log "S12B launcher rc=$rc"
[ $rc -eq 0 ] && grep -q "^End" u3d/case_S12B/log.simpleFoam || { log "S12B did not finish cleanly: STOP"; exit 1; }
u3d/post_level.sh S12B no purge >> u3d/queue2.log 2>&1 || { log "post S12B failed: STOP"; exit 1; }
for c in baseline_resistance T1_missed_branch_resistance clean_nolesion_resistance; do
  idle; diskok || { log "disk < 12 GB before $c: STOP"; exit 1; }
  log "launching scan-14 m1/cases/$c"
  ./run_set_generic.sh m1/cases/$c > m1/cases/$c.run_set.log 2>&1; rc=$?
  log "$c launcher rc=$rc"
  [ $rc -eq 0 ] && grep -q "^End" m1/cases/$c/log.simpleFoam || { log "$c did not finish cleanly: STOP"; exit 1; }
  python3 pf/analyze_case.py m1/cases/$c --json m1/cases/$c/analysis_pf.json >> u3d/queue2.log 2>&1 || { log "analysis $c failed: STOP"; exit 1; }
done
log "queue2 finished"
