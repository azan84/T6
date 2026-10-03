#!/bin/bash
# B2 driver (2026-10-01): L16 then L8x2 with the audited runner (fix 27), then the analysis. Detached; one layout at a time; between layouts wait until the 1-min load is < 0.5 (at most 30 min).
# fix 28: rc is captured right after each command (before, rc=$? inside the echo recorded the status of the $(date) substitution, always 0).
cd "$(dirname "$0")" || exit 2
export B2_EXCLUSIVE_OK=1 B2_ALLOW_STOPPED_FOREIGN=1 B2_ALLOW_WINDOWS_LOAD=1
echo "$(date '+%F %T') start L16" >> driver.log
bash ./b2_run.sh L16 > run_L16.log 2>&1; rc=$?; echo "$(date '+%F %T') L16 rc=$rc" >> driver.log
w=0; until awk '{exit !($1 < 0.5)}' /proc/loadavg; do
  if [ $w -ge 1800 ]; then echo "$(date '+%F %T') STOP: 1-min load $(cut -d' ' -f1 /proc/loadavg) still >= 0.5 after 1800 s; L8x2 and the analysis not started" >> driver.log; exit 4; fi
  sleep 15; w=$((w+15)); done
echo "$(date '+%F %T') start L8x2 (load $(cut -d' ' -f1 /proc/loadavg), waited $w s)" >> driver.log
bash ./b2_run.sh L8x2 > run_L8x2.log 2>&1; rc=$?; echo "$(date '+%F %T') L8x2 rc=$rc" >> driver.log
python3 ./b2_analyse.py B2_throughput.csv > analyse.log 2>&1; rc=$?; echo "$(date '+%F %T') analyse rc=$rc" >> driver.log
echo DONE >> driver.log
