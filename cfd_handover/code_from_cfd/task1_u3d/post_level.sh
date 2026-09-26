#!/bin/bash
# usage: post_level.sh <level> <contended yes|no|unknown> [purge]   analyse one FINISHED level: strict analysis json, CSV row, optional deletion of the processor* directories (fields are not needed: every reported quantity is a monitor series)
cd "$(dirname "$0")" || exit 1; L=$1; C=$2
case $L in W*) D=wedge_$L;; *) D=case_$L;; esac
[ -d "$D" ] || { echo "no case dir $D"; exit 1; }
grep -q "^End" "$D/log.simpleFoam" || { echo "$D: log.simpleFoam has no End line: run not finished"; exit 1; }
python3 ../analyze_solve.py "$D" --strict --json "$D/analysis.json" > "$D/log.analyze" 2>&1 || { echo "analyze_solve failed: see $D/log.analyze"; exit 1; }
tail -6 "$D/log.analyze" | cut -c1-200
python3 u3d_make_csv.py U3D_sten70_work.csv "$C" "$L" || exit 1
if [ "${3:-}" = "purge" ]; then rm -rf "$D"/processor* && echo "$D: processor directories removed"; fi
