#!/bin/bash
# B2 third measurement (2026-10-06, quiet host, original order L16 then L8x2); rc captured right after each command; bounded load waits.
cd "$(dirname "$0")" || exit 2
export B2_EXCLUSIVE_OK=1 B2_ALLOW_WINDOWS_LOAD=1
waitload() { local w=0; until awk '{exit !($1 < 0.5)}' /proc/loadavg; do [ $w -ge 1800 ] && return 1; sleep 15; w=$((w+15)); done; return 0; }
for L in L16 L8x2; do
  waitload || { echo "$(date '+%F %T') STOP: load stays >= 0.5 before $L" >> driver3.log; exit 4; }
  echo "$(date '+%F %T') start $L (load $(cut -d' ' -f1 /proc/loadavg))" >> driver3.log
  bash ./b2_run.sh $L > run_$L.log 2>&1; rc=$?; echo "$(date '+%F %T') $L rc=$rc" >> driver3.log
  [ $rc -eq 0 ] || break
done
python3 ./b2_analyse.py B2_throughput.csv > analyse.log 2>&1; rc=$?; echo "$(date '+%F %T') analyse rc=$rc" >> driver3.log; echo DONE3 >> driver3.log
