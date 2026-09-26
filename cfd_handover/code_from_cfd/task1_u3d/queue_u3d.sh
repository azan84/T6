#!/bin/bash
# Sequential U3D queue (design v2.5): waits for the running launcher/solvers to end, post-processes S25A, then S12A (6000), S25B (4000), S12B (6000), each one at 16 ranks via run_set_generic.sh and post_level.sh (purge).
# Stops (does not continue) on: <12 GB free disk, a launcher failure, a missing End line. Log: u3d/queue_u3d.log. Never kills anything.
P=/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot; cd $P
log() { echo "$(date '+%F %T') $*" >> u3d/queue_u3d.log; }
idle() { while pgrep -f "run_set_generic.sh|simpleFoam" > /dev/null; do sleep 30; done; }
diskok() { [ "$(df --output=avail -B1G / | tail -1 | tr -dc 0-9)" -ge 12 ]; }
log "queue started"
idle; log "host idle: post-processing S25A"
u3d/post_level.sh S25A no purge >> u3d/queue_u3d.log 2>&1 || { log "post S25A failed: STOP"; exit 1; }
for job in "S12A 6000" "S25B 4000" "S12B 6000"; do
  set -- $job; L=$1; E=$2
  idle; diskok || { log "disk < 12 GB before $L: STOP"; exit 1; }
  log "launching $L (endTime $E)"
  RUN_SET_END_MAP="u3d/case_$L=$E" ./run_set_generic.sh u3d/case_$L > u3d/run_set_$L.log 2>&1; rc=$?
  log "$L launcher rc=$rc"
  [ $rc -eq 0 ] && grep -q "^End" u3d/case_$L/log.simpleFoam || { log "$L did not finish cleanly: STOP"; exit 1; }
  u3d/post_level.sh $L no purge >> u3d/queue_u3d.log 2>&1 || { log "post $L failed: STOP"; exit 1; }
done
log "queue finished"
