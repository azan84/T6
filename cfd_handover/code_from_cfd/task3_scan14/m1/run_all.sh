#!/bin/bash
cd "$(dirname "$0")"
W="$(cat e0_waiver.txt)"
for c in clean_nolesion T1_missed_branch baseline; do
  pk=$(ls pkg | grep "__${c}__real")
  d=out/${c}; t0=$(date +%s)
  nice -n 10 /usr/bin/python3 build_m1_geometry.py "$pk" "$d" --e0-waiver "$W" > out/${c}.log 2>&1
  echo "$c rc=$? $(( $(date +%s) - t0 )) s" >> out/run_all.log
done
echo ALLDONE >> out/run_all.log
