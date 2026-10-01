#!/bin/bash
# B2 driver (2026-10-01): L16 then L8x2 with the audited runner (fix 27), then the analysis. Detached; one layout at a time; 120 s settle pause between layouts.
cd "$(dirname "$0")" || exit 2
export B2_EXCLUSIVE_OK=1 B2_ALLOW_STOPPED_FOREIGN=1 B2_ALLOW_WINDOWS_LOAD=1
echo "$(date '+%F %T') start L16" >> driver.log
bash ./b2_run.sh L16 > run_L16.log 2>&1; echo "$(date '+%F %T') L16 rc=$?" >> driver.log
sleep 120
echo "$(date '+%F %T') start L8x2" >> driver.log
bash ./b2_run.sh L8x2 > run_L8x2.log 2>&1; echo "$(date '+%F %T') L8x2 rc=$?" >> driver.log
python3 ./b2_analyse.py B2_throughput.csv > analyse.log 2>&1; echo "$(date '+%F %T') analyse rc=$?" >> driver.log
echo DONE >> driver.log
