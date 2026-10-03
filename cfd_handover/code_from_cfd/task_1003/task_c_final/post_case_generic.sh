#!/bin/bash
# usage: post_case_generic.sh <case_dir> <package_dir_or_name> <label> <mode resistance|prescribed> <out_dir>
# End-to-end post-solve runner for ANY Gate-M1-format package (scan-14 M1 cases incl. the Task A D7 variants, the P5 cases), Task C (work order 2026-10-03; audit Sol findings 1 and 5). Run it once per FINISHED solve.
# Steps (each logged; the script stops at the first failure with a non-zero exit):
#   0. the solve is finished (post_helpers.py finished, defined on the log tail): the LAST run of log.simpleFoam completed (an exact 'End' line after its last 'Time = <t>' line, no later run header /
#      'Starting time loop' / Time line, i.e. no appended partial run) and <t> == endTime of system/controlDict -> <out_dir>/run_completion_<label>_<mode>.json   (else exit 1, nothing generated)
#   0b. the package is resolved (pf/m1_package.py) and its files are verified against build_info.json package_hashes BEFORE anything is generated -> <out_dir>/package_check_<label>_<mode>.json
#      (any mismatch, missing or extra hashed file, or a missing record: exit 1); every later step gets the verified absolute package directory
#   1. pf/analyze_case.py (strict analyze_solve checks; prescribed mode adjusted, see its docstring) -> <case>/analysis_pf.json (cached only if its provenance hashes match; POST_FORCE=1 regenerates).
#      The analysis completion flag (strict.log_finished) is ENFORCED (--require-finished: exit 4). The convergence verdict is reported, not a stop: an UNCONVERGED solve still gets its return files
#      (M1_results 'converged' says so). POST_REQUIRE_CONVERGED=1 makes it a stop (--strict-exit, exit 3).
#   2. reconstructPar -latestTime (nice) unless the latest time is already reconstructed and verified; then the CHECK (post_helpers.py reconstruct-check): reconstructed latest time == processor0 latest time,
#      U and p present and non-empty, log.reconstructPar ends with End -> <out_dir>/reconstruct_check_<label>_<mode>.json. Fields are KEPT; processor directories are NEVER removed by this script.
#   3. pf/m1_probes.py: M1_probes_<label>_<mode>.csv (every package probe; the relocated measurement probe as an extra row when the builder relocated it)
#   4. pf/as_meshed_radius.py: as_meshed_radius_<label>_detail.csv + contract files as_meshed_radius_<label>.csv (area-equivalent) and _inscribed.csv. Mesh/package-only quantity: existing files are reused ONLY
#      if as_meshed_radius_<label>_provenance.json records the same mesh sha256 (case constant/polyMesh files) and package hashes and the files are unchanged; otherwise regenerated (and the provenance written).
#      POST_FORCE=1 always regenerates; POST_REUSE_UNCHECKED=1 reuses existing files WITHOUT the provenance check (explicit waiver); POST_SKIP_RADIUS=1 skips. The decision is recorded in the summary (radius_outputs).
#   5. pf/post_helpers.py fill: fill_<label>_<mode>.json (geometry/mesh gate columns, D3/D4 columns from d34.json, machine-readable flags; GATES_JSON / MESH_GATES_JSON / D34_JSON override the discovery,
#      see post_helpers.py; geometry_step_ok follows the DECISIVE geometry gates, D10). An outlet lost in the mesh (0 faces) is reported Q = 0, p N/A, flag OUTLET_LOST_IN_MESH (pf_common / analyze_case / m1_results)
#   6. pf/m1_results.py: M1_outlets_<label>_<mode>.csv + the (label, mode) row of <out_dir>/M1_results.csv (peak RAM when available: PEAK_RAM_GB or a MEMLOG sampler file)
#   7. pf/post_helpers.py history: M1_monitor_history_<label>_<mode>.csv (every iteration of measurementP/measurementFlux/throatP/throatFlux[/measurementOrig*]) + its summary json (cross-check vs the probes csv)
#      and b1_settle.py --case: settle_<label>_<mode>.csv (B1 SETTLED rule on measurementP; the production default stays 'run the full budget')
#   8. flow_state_profile.py profile: flow_state_<label>_<mode>.csv (pre-registered Task A diagnostic: centreline-normal connected sections every 1 mm from throat+2 mm to the measurement probe; POST_SKIP_FLOWSTATE=1 skips)
#   9. post_helpers.py summary: post_summary_<label>_<mode>.json (verdict, wall clock, cells, peak RAM, measurement probe used, sha256 of every output); with REF_FFR=<value> [REF_TOL, default 0.00055]
#      also DeltaFFR = p_over_Paorta of the package 'measurement' row of the probes csv (reconstructed final fields) - REF_FFR (Task A: REF_FFR=0.8697574904997768, the returned p011 value; like with like,
#      Sol finding A7); the measurementP last-100 mean is reported next to it for B1, not used
# Paths: P (the pilot root) = $P, else /home/azan/paper6_t6_work/scratchpad/item3_M1_pilot. Python helpers: <this script's dir>/pf if it holds post_helpers.py (taskC staging), else $P/pf.
# Package: a package directory, or a name resolved by pf/m1_package.py: $PKG_ROOT (explicit) only if set, else Drive packages/M1, packages/P5, then the persistent copy scratchpad/zipcheck/cfd_handover/packages/M1 (read-only). Host etiquette: nice -n 10, OMP_NUM_THREADS=2.
set -o pipefail
[ $# -eq 5 ] || { sed -n '2,3p' "$0"; exit 2; }
CASE=$(readlink -f "$1"); PKG=$2; L=$3; M=$4; O=$(readlink -m "$5")
case "$M" in resistance|prescribed) ;; *) echo "mode must be resistance or prescribed"; exit 2;; esac
SD=$(dirname "$(readlink -f "$0")")
P=${P:-/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot}; export P
if [ -f "$SD/pf/post_helpers.py" ]; then PF=$SD/pf; else PF=$P/pf; fi
B1=$SD/b1_settle.py; [ -f "$B1" ] || B1=$P/b1_settle.py
FSP=$SD/flow_state_profile.py; [ -f "$FSP" ] || FSP=$P/flow_state_profile.py
PR=${PKG_ROOT:+--pkg-root $PKG_ROOT}
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-2}
PY="nice -n 10 python3"
mkdir -p "$O" || exit 1
LOG=$O/post_${L}_${M}.log
say() { echo "[post $(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
run() { say "+ $*"; "$@" 2>&1 | tee -a "$LOG"; local rc=${PIPESTATUS[0]}; [ $rc -eq 0 ] || say "step failed (exit $rc): $*"; return $rc; }
say "case $CASE package $PKG label $L mode $M out $O (P=$P, helpers $PF)"
[ -f "$CASE/build_info.json" ] || { say "$CASE: no build_info.json"; exit 1; }
run python3 "$PF/post_helpers.py" finished "$CASE" --json "$O/run_completion_${L}_${M}.json" || { say "$CASE: the last run of log.simpleFoam is not complete (see $O/run_completion_${L}_${M}.json): nothing done"; exit 1; }
# 0b. package verification against build_info.json package_hashes (before anything is generated)
say "+ post_helpers.py package-check $CASE $PKG $PR"
PKGDIR=$(python3 "$PF/post_helpers.py" package-check "$CASE" "$PKG" $PR --json "$O/package_check_${L}_${M}.json" 2> >(tee -a "$LOG" >&2)) || { say "package $PKG NOT verified against $CASE/build_info.json: stopping (see $O/package_check_${L}_${M}.json)"; exit 1; }
say "package verified against build_info package_hashes: $PKGDIR"; PKG=$PKGDIR; PR=""
# 1. strict analysis
run $PY "$PF/analyze_case.py" "$CASE" --json "$CASE/analysis_pf.json" --cached --require-finished ${POST_FORCE:+--force} ${POST_REQUIRE_CONVERGED:+--strict-exit} || exit $?
# 2. reconstruct the latest time (kept) and verify before anything else
RC=$O/reconstruct_check_${L}_${M}.json
if [ -z "$POST_FORCE" ] && python3 "$PF/post_helpers.py" reconstruct-check "$CASE" "$RC" >/dev/null 2>&1; then
  say "latest time already reconstructed and verified: reconstructPar not re-run"
else
  say "+ reconstructPar -latestTime (log: $CASE/log.reconstructPar)"
  ( source /usr/lib/openfoam/openfoam2406/etc/bashrc >/dev/null 2>&1; cd "$CASE" && nice -n 10 reconstructPar -latestTime > log.reconstructPar 2>&1 ) || { say "reconstructPar failed (see $CASE/log.reconstructPar)"; exit 1; }
fi
run python3 "$PF/post_helpers.py" reconstruct-check "$CASE" "$RC" || { say "reconstruction NOT verified: stopping (processor directories untouched)"; exit 1; }
# 3. probes
run $PY "$PF/m1_probes.py" "$CASE" "$PKG" "$L" "$M" --out "$O/M1_probes_${L}_${M}.csv" || exit 1
# 4. as-meshed radius (mesh only)
RAD=$O/as_meshed_radius_${L}
if [ -n "$POST_SKIP_RADIUS" ]; then POST_RADIUS_DECISION="SKIPPED (POST_SKIP_RADIUS=1)"
elif [ -z "$POST_FORCE" ] && [ -n "$POST_REUSE_UNCHECKED" ] && [ -s "${RAD}_detail.csv" ] && [ -s "${RAD}.csv" ] && [ -s "${RAD}_inscribed.csv" ]; then
  POST_RADIUS_DECISION="REUSED UNCHECKED (POST_REUSE_UNCHECKED=1: mesh/package provenance NOT verified)"
elif [ -z "$POST_FORCE" ] && { python3 "$PF/post_helpers.py" radius-check "$CASE" "$PKG" "$RAD" 2>&1 | tee -a "$LOG"; }; then      # pipefail: the status of radius-check
  POST_RADIUS_DECISION="reused (provenance verified: same mesh sha256 and package hashes)"; rm -f "${RAD}_provenance.pending.json"
else
  if [ -n "$POST_FORCE" ]; then python3 "$PF/post_helpers.py" radius-check "$CASE" "$PKG" "$RAD" >/dev/null || true; fi      # (POST_FORCE) writes the pending provenance = current hashes
  run $PY "$PF/as_meshed_radius.py" "$CASE" "$PKG" "$L" "${RAD}_detail.csv" --contract "$RAD" || exit 1
  run python3 "$PF/post_helpers.py" radius-commit "$RAD" || exit 1
  POST_RADIUS_DECISION="regenerated${POST_FORCE:+ (POST_FORCE=1)}; provenance written"
fi
say "as-meshed radius: $POST_RADIUS_DECISION"; export POST_RADIUS_DECISION
# 5. geometry/mesh columns
run python3 "$PF/post_helpers.py" fill "$CASE" "$(basename "$PKG")" "$O/fill_${L}_${M}.json" ${GATES_JSON:+--gates $GATES_JSON} ${MESH_GATES_JSON:+--mesh-gates $MESH_GATES_JSON} ${D34_JSON:+--d34 $D34_JSON} || exit 1
# 6. outlets + results row
RAM=$(python3 "$PF/post_helpers.py" peak-ram "$CASE")
RT=""; [ "$M" = prescribed ] && [ -f "${CASE%_prescribed}_roundtrip/roundtrip_result.json" ] && RT="--roundtrip ${CASE%_prescribed}_roundtrip/roundtrip_result.json"
run $PY "$PF/m1_results.py" "$CASE" "$L" "$M" --analysis "$CASE/analysis_pf.json" --probes "$O/M1_probes_${L}_${M}.csv" --fill-json "$O/fill_${L}_${M}.json" ${RAM:+--peak-ram-gb $RAM} $RT --outdir "$O" || exit 1
# 7. measurement-probe history + B1 settle analysis
run python3 "$PF/post_helpers.py" history "$CASE" "$O/M1_monitor_history_${L}_${M}.csv" --probes "$O/M1_probes_${L}_${M}.csv" --json "$O/M1_monitor_history_${L}_${M}.json" || exit 1
run python3 "$B1" "$O/settle_${L}_${M}.csv" --case "$CASE:" || exit 1
# 8. flow-state diagnostic (pre-registered, TASK_A_DESIGN.md)
FS=$O/flow_state_${L}_${M}.csv
if [ -n "$POST_SKIP_FLOWSTATE" ]; then say "flow-state profile SKIPPED (POST_SKIP_FLOWSTATE)"; FS=""
else run $PY "$FSP" profile "$CASE" --package "$PKG" --label "${L}_${M}" --out "$FS" || exit 1; fi
# 9. summary
OUTS="$O/run_completion_${L}_${M}.json $O/package_check_${L}_${M}.json $O/M1_probes_${L}_${M}.csv $O/M1_outlets_${L}_${M}.csv $O/M1_results.csv $O/fill_${L}_${M}.json $O/M1_monitor_history_${L}_${M}.csv $O/M1_monitor_history_${L}_${M}.json $O/settle_${L}_${M}.csv $RC"
[ -z "$POST_SKIP_RADIUS" ] && OUTS="$OUTS ${RAD}.csv ${RAD}_inscribed.csv ${RAD}_detail.csv"
[ -z "$POST_SKIP_RADIUS" ] && [ -z "$POST_REUSE_UNCHECKED" ] && OUTS="$OUTS ${RAD}_provenance.json"
[ -n "$FS" ] && OUTS="$OUTS $FS"
run python3 "$PF/post_helpers.py" summary "$CASE" "$O" "$L" "$M" "$O/post_summary_${L}_${M}.json" $OUTS || exit 1
say "POSTDONE $L $M (processor directories kept: remove them only after checking $RC and the outputs)"
