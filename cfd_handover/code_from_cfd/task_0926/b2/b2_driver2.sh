#!/bin/bash
# B2 driver part 2 (2026-10-01): L8x2 was refused at 09:44 by the runner's load guard (1-min load 1.75 >= 1.5, two minutes after L16 ended); wait until the 1-min load is < 0.5 (at most 30 min), then L8x2, then the analysis.
# fix 28: rc is captured right after each command (before, rc=$? inside the echo recorded the status of the $(date) substitution, always 0); the load wait is bounded.
cd "$(dirname "$0")" || exit 2
export B2_EXCLUSIVE_OK=1 B2_ALLOW_STOPPED_FOREIGN=1 B2_ALLOW_WINDOWS_LOAD=1
w=0; until awk '{exit !($1 < 0.5)}' /proc/loadavg; do
  if [ $w -ge 1800 ]; then echo "$(date '+%F %T') STOP: 1-min load $(cut -d' ' -f1 /proc/loadavg) still >= 0.5 after 1800 s; L8x2 retry and the analysis not started" >> driver.log; exit 4; fi
  sleep 15; w=$((w+15)); done
echo "$(date '+%F %T') start L8x2 (retry; load $(cut -d' ' -f1 /proc/loadavg), waited $w s)" >> driver.log
mv run_L8x2.log run_L8x2_refused_0944.log 2>/dev/null
bash ./b2_run.sh L8x2 > run_L8x2.log 2>&1; rc=$?; echo "$(date '+%F %T') L8x2 rc=$rc" >> driver.log
python3 ./b2_analyse.py B2_throughput.csv > analyse.log 2>&1; rc=$?; echo "$(date '+%F %T') analyse rc=$rc" >> driver.log
echo DONE2 >> driver.log
