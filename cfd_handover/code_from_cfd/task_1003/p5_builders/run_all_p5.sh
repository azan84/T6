#!/bin/bash
# the five P5 packages, one at a time, in the work-order order
cd "$(dirname "$0")"
for pk in 138_left_LAD_prox_20mm_70ds__baseline__real 69_left_LCX_prox_20mm_65ds__baseline__real 473_left_LCX_prox_20mm_60ds__baseline__real 272_right_RCA_prox_10mm_65ds__baseline__real 139_right_RCA_prox_10mm_70ds__baseline__real; do
  ./run_case.sh "$pk"
done
echo "$(date +%F_%T) ALLDONE" >> runs.log
