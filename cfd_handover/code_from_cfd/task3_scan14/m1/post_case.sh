#!/bin/bash
# usage: m1/post_case.sh <label clean_nolesion|baseline|T1_missed_branch> <mode resistance|prescribed>
# After a finished scan-14 solve (m1/cases/<label>_<mode>, analysed by pf/analyze_case.py): reconstructPar -latestTime (nice), M1_probes_<label>_<mode>.csv, M1_outlets_<label>_<mode>.csv + one M1_results.csv row into m1/out_returns/.
P=/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot; cd $P; L=$1; M=$2; C=m1/cases/${L}_${M}; PKG=14_left_LAD_prox_20mm_80ds__${L}__real; O=m1/out_returns
[ -d "$C" ] && grep -q "^End" $C/log.simpleFoam || { echo "$C: not finished"; exit 1; }
# cached analysis reused only if its provenance (size + sha256 of log.simpleFoam and the monitor .dat files) matches the files on disk, else regenerated; POST_FORCE=1 always regenerates
python3 pf/analyze_case.py $C --json $C/analysis_pf.json --cached ${POST_FORCE:+--force} || exit 1
source /usr/lib/openfoam/openfoam2406/etc/bashrc
( cd $C && nice -n 10 reconstructPar -latestTime > log.reconstructPar 2>&1 ) || { echo "reconstructPar failed"; exit 1; }
nice -n 10 python3 pf/m1_probes.py $C $PKG $L $M --out $O/M1_probes_${L}_${M}.csv || exit 1
python3 m1/make_fill_json.py $L $O/fill_${L}.json || exit 1
RAM=$(python3 - <<PY
import sys; sys.path.insert(0, "$P/u3d")
import u3d_make_csv as M
t = M.timing("$P/$C"); print(M.peak_ram_gb(t["start_clock"], t["end_clock"]) or "")
PY
)
RT=""; [ "$M" = prescribed ] && [ -f m1/cases/${L}_roundtrip/roundtrip_result.json ] && RT="--roundtrip m1/cases/${L}_roundtrip/roundtrip_result.json"
python3 pf/m1_results.py $C $L $M --analysis $C/analysis_pf.json --probes $O/M1_probes_${L}_${M}.csv --fill-json $O/fill_${L}.json ${RAM:+--peak-ram-gb $RAM} $RT --outdir $O || exit 1
echo POSTDONE $L $M
