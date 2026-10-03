#!/bin/bash
# Runs every test of both lineages (taskC/tests + taskP5/tests = taskFinal/tests) against taskFinal, niced, <= 2 threads, foreground.
# usage: bash tests/run_all_consolidation40.sh <run_label> [test ...]   (default: all; run in slices to keep each foreground call short) -> test_output/consolidation40/<run_label>/<test>.txt + summary.txt
TC=$(dirname "$(dirname "$(readlink -f "$0")")"); R=$TC/test_output/consolidation40/${1:?run label}; mkdir -p "$R"; shift; ALL="test_b1_settle.py test_flow_state_profile.py test_post_guards.py test_section_rule.py test_p5_stub.py test_flags_p5.py test_empty_patch_coded_bc.py test_manifest.sh test_flow_state_sten70.sh test_post_case_generic.sh"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1
cd "$TC"
for t in ${@:-$ALL}; do
  case "$t" in *.py) cmd="nice -n 10 python3 -B tests/$t";; *.sh) cmd="nice -n 10 bash tests/$t";; esac
  s=$(date +%s); $cmd > "$R/${t%.*}.txt" 2>&1; rc=$?; e=$(( $(date +%s) - s ))
  last=$(grep -E 'PASS|FAIL|STATES|Error|error' "$R/${t%.*}.txt" | tail -1 | cut -c1-200)
  printf '%-32s rc=%d %4ds  %s\n' "$t" $rc $e "$last" | tee -a "$R/summary.txt"
done
find "$TC" -name __pycache__ -prune -exec rm -rf {} +; rm -rf "$TC/.post_test_tmp"
