#!/bin/bash
# B2 run 4 (2026-10-06): valid-attempt, both orders. Waits (<= 14 h) until NO Claude session is alive (they caused the earlier INVALID verdicts) and load < 0.5, then pair A = L8x2 then L16, then pair B = L16 then L8x2
# (cases re-prepared between the pairs). NO Windows-load override: a refused Windows pre-check stops the driver (logged). rc captured right after each command.
cd "$(dirname "$0")" || exit 2
export B2_EXCLUSIVE_OK=1
LOG=driver4.log
waitquiet() { local w=0; until ! pgrep -x claude >/dev/null && awk '{exit !($1 < 0.5)}' /proc/loadavg; do [ $w -ge 50400 ] && return 1; sleep 20; w=$((w+20)); done; echo "$(date '+%F %T') quiet after ${w}s (claude sessions: $(pgrep -xc claude), load $(cut -d' ' -f1 /proc/loadavg))" >> $LOG; return 0; }
runpair() { local tag=$1; shift
  for L in "$@"; do
    waitquiet || { echo "$(date '+%F %T') STOP: host never quiet before $L" >> $LOG; return 1; }
    echo "$(date '+%F %T') [$tag] start $L" >> $LOG
    bash ./b2_run.sh $L > run_${L}_$tag.log 2>&1; rc=$?; echo "$(date '+%F %T') [$tag] $L rc=$rc" >> $LOG
    [ $rc -eq 0 ] || return $rc
  done
  python3 ./b2_analyse.py B2_throughput.csv > analyse_$tag.log 2>&1; echo "$(date '+%F %T') [$tag] analyse rc=$?" >> $LOG; }
runpair A L8x2 L16 || { echo "$(date '+%F %T') pair A did not complete; pair B not started" >> $LOG; echo DONE4_PARTIAL >> $LOG; exit 3; }
mkdir -p pairA; mv L16 L8 results_L16 results_L8x2 B2_throughput.csv pairA/ 
bash ./b2_prepare.sh > prepare_B.log 2>&1 || { echo "$(date '+%F %T') re-prepare failed" >> $LOG; exit 5; }
runpair B L16 L8x2
echo DONE4 >> $LOG
