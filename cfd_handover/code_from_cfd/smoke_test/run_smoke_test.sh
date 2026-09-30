#!/bin/bash
# Smoke test (Task B3, work order 2026-09-26; fix26 2026-10-01: branch-aware): a second machine proves that its install reaches one of the two validated steady states of one returned case in well under 30 minutes.
# Case: Stage A sten70 (70 % diameter stenosis, straight tapered vessel), A5 coarse mesh (198,252 cells), steady laminar simpleFoam, coded resistance outlet (R = 6.974826e9 Pa s/m3, fixed relax 0.2), 3000 iterations
#   (fix25: 2000, the iteration count of the original A5 run, is NOT converged in a fresh 8-way run on OpenFOAM v2406: outlet flow +0.189 % at 2000, +0.029 % at 2250, +0.002 % at 2500, stable to 5 digits from 2750;
#   the count is N_ITER in compare_smoke.py and must equal endTime of case_files/system/controlDict, checked in the preflight).
# Two branches (fix26, B3 diagnosis 2026-10-01): the case has two stable steady solutions on the same mesh recipe and cell count (not mesh identity: cfMesh is not bitwise reproducible), a fresh run lands on either,
#   decided by tiny cfMesh/decomposition perturbations: DEFLECTED jet, outlet flow 1.17392231e-06 m3/s, FFR_x56p5 0.78396 (= the returned value, stageA_A5_ladders.csv, A5 sten70 coarse) and SYMMETRIC jet,
#   1.17825059e-06 m3/s, FFR_x56p5 0.78248 (reference-machine smoke run 2026-10-01). Both are in reference_result.json (schema 2, 'branches'); only the deflected branch reproduces the returned value.
# usage: ./run_smoke_test.sh [NPROC=8] [WORKDIR=${TMPDIR:-/tmp}/paper6_t6_smoke_work]      needs: OpenFOAM ESI v2406 (source $FOAM_BASHRC, default /usr/lib/openfoam/openfoam2406/etc/bashrc; cartesianMesh = cfMesh is part of it; wmake + g++ for the coded BC), OpenMPI, python3 + numpy.
# PASS = complete run (exact 'End' line, log 'Time =' 1..3000 each once in order, monitors with iterations exactly 1..3000 and finite values), same mesh recipe and cell count (STL sha256, checkMesh OK, exactly 1 inlet + 1 outlet
#   wall->patch rewrite, cells EQUAL to the reference; compare_smoke.py re-verifies STL hash, boundary types and checkMesh log from the retained work directory) and the run on exactly one branch: outlet flow within 0.1 %
#   and FFR_x56p5 within 0.0005 of that branch, with a stable final window (last 200 iterations: Q band <= 0.01 %, FFR band <= 1e-5); the verdict line names the branch, see compare_smoke.py.
# Timing claim: about 5-6 minutes on 8 PHYSICAL cores of a workstation (reference run: 318 s wall, see reference_result.json); the 30-minute claim needs 8 physical cores (NPROC > physical cores is refused unless SMOKE_ALLOW_FEWER_CORES=1).
# env: WRITE_REFERENCE=1 = reference run: step 6 adds this run to $HERE/reference_result.json as the branch it lands on (no comparison; only if the run is complete, the mesh checks hold, the final window is stable
#      and it lies within 0.1 % Q / 0.0005 FFR of one branch constant; the other branch is kept) and exits 0. fix26: an EXISTING entry of that branch is NOT replaced (step 6 exits 2) unless
#      SMOKE_REPLACE_BRANCH=deflected|symmetric names it (forwarded as --replace-branch; a run landing on the other branch is refused, exit 2, the file is unchanged). fix26 attempt 2 (audit AGY 2, SOL 4):
#      PREFLIGHT (before any expensive step) exits 2 if the reference file is unusable, or already holds both branches and SMOKE_REPLACE_BRANCH is unset, or SMOKE_REPLACE_BRANCH is not deflected|symmetric,
#      or SMOKE_REPLACE_BRANCH is set without WRITE_REFERENCE=1. Without WRITE_REFERENCE, reference_result.json must exist and be usable (checked before any expensive step).
#      GEN = path of make_stageA_geometry.py (default $HERE/../stageA/make_stageA_geometry.py); OMP_NUM_THREADS (default 8) for cartesianMesh (cfMesh cell count depends on the thread count).
#      SMOKE_ALLOW_FEWER_CORES=1: allow NPROC > physical cores (a warning; the timing claim does not hold).
#      SMOKE_PHYS_CORES=<n>: physical core count when lscpu cannot establish it (nproc counts logical CPUs and is never used as the physical count); without it (or SMOKE_ALLOW_FEWER_CORES=1) exit 2.
# WORKDIR (delta-2 audit finding 2): default ${TMPDIR:-/tmp}/paper6_t6_smoke_work, a native Linux scratch directory OUTSIDE this (possibly cloud-synced) folder; it must not exist yet (exit 2).
#      A WORKDIR inside this smoke_test folder is refused (exit 2) unless SMOKE_ALLOW_WORKDIR_IN_TREE=1; a WORKDIR under /mnt/ (WSL DrvFs, slow) gives a warning.
# writes <WORKDIR>/smoke_checks.json: stl_sha256, checkMesh_ok, cells, inlet_rewrites, outlet_rewrites, omp_num_threads (read by compare_smoke.py).
# exit codes: 0 PASS (or reference written); 1 FAIL (branch criterion: no branch matched, FFR inconsistent with the matched branch, or unstable final window); 2 setup error (also: reference_result.json unusable, e.g. schema 1, or lacking a branch entry in compare mode (preflight, fix26 attempt 3), or WRITE_REFERENCE refused to replace a branch entry, in the preflight or at step 6) (preflight: python3/numpy, OpenFOAM v2406 (WM_PROJECT_VERSION), OpenFOAM commands, wmake/g++, NPROC, physical cores; workdir, reference file, geometry generator missing);
#             3 NON-COMPARABLE: geometry/mesh step failed, STL hash differs, checkMesh failed, patch rewrites not exactly inlet 1 + outlet 1, different cell count, or run incomplete (never PASS); 4 simpleFoam failed.
set -u
HERE=$(cd "$(dirname "$0")" && pwd); NP=${1:-8}; W=${2:-${TMPDIR:-/tmp}/paper6_t6_smoke_work}
FOAM_BASHRC=${FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}; GEN=${GEN:-$HERE/../stageA/make_stageA_geometry.py}; REF="$HERE/reference_result.json"
STL_SHA256=47178798e1052ddb7d23d8b318a934baaf42d93d5555b9568eddcabdf9ef8ef2
if [ "${WRITE_REFERENCE:-0}" != 1 ]; then
    [ -z "${SMOKE_REPLACE_BRANCH:-}" ] || { echo "preflight: SMOKE_REPLACE_BRANCH is only valid with WRITE_REFERENCE=1"; exit 2; }
    [ -f "$REF" ] || { echo "no reference: $REF missing. Copy the shipped schema-2 reference_result.json here (it holds both branches); WRITE_REFERENCE=1 only adds or replaces one branch (reference machine)"; exit 2; }
fi
[ -f "$GEN" ] || { echo "geometry generator not found: $GEN (copy the folder stageA/ next to smoke_test/, or set GEN=<path of make_stageA_geometry.py>)"; exit 2; }
# --- preflight (exit 2, nothing expensive has run) ---
[[ "$NP" =~ ^[1-9][0-9]*$ ]] || { echo "preflight: NPROC '$NP' is not a positive integer"; exit 2; }
command -v python3 > /dev/null || { echo "preflight: python3 not found"; exit 2; }
python3 -c "import numpy" 2> /dev/null || { echo "preflight: python3 cannot import numpy (pip install numpy)"; exit 2; }
N_ITER=$(cd "$HERE" && PYTHONDONTWRITEBYTECODE=1 python3 -c "import compare_smoke; print(compare_smoke.N_ITER)" 2> /dev/null)
END_TIME=$(grep -E "^\s*endTime\s+" "$HERE/case_files/system/controlDict" | tr -dc 0-9)
[[ "$N_ITER" =~ ^[1-9][0-9]*$ ]] && [ "$END_TIME" = "$N_ITER" ] || { echo "preflight: endTime '$END_TIME' of case_files/system/controlDict != N_ITER '$N_ITER' of compare_smoke.py (iteration count inconsistent)"; exit 2; }
# reference governance (fix26 attempt 2, audit AGY 2/3, SOL 4): usable reference and, for WRITE_REFERENCE=1, what step 6 will do; decided here, before sourcing OpenFOAM
BR=$(cd "$HERE" && PYTHONDONTWRITEBYTECODE=1 python3 -c 'import sys, os, compare_smoke as c
if not os.path.exists(sys.argv[1]): print("-"); sys.exit(0)
r, e = c.load_reference(sys.argv[1])
if e: print(e); sys.exit(1)
print(" ".join(sorted(r["branches"])) or "-")' "$REF"); BRC=$?
[ $BRC -eq 0 ] || { echo "preflight: $BR"; exit 2; }
# fix26 attempt 3 (audit AGY R2-2): compare mode needs both branch entries; a partial reference fails here, not at step 6 after the solve
if [ "${WRITE_REFERENCE:-0}" != 1 ] && [ "$BR" != "deflected symmetric" ]; then
    echo "preflight: compare mode needs both branch entries (deflected, symmetric) in $REF, but it holds: $BR. Copy the shipped schema-2 reference_result.json here (WRITE_REFERENCE=1 adds or replaces one branch, reference machine only)"; exit 2
fi
if [ "${WRITE_REFERENCE:-0}" = 1 ]; then
    RB=${SMOKE_REPLACE_BRANCH:-}
    [ -z "$RB" ] || [ "$RB" = deflected ] || [ "$RB" = symmetric ] || { echo "preflight: SMOKE_REPLACE_BRANCH '$RB' must be deflected or symmetric"; exit 2; }
    if [ "$BR" = "deflected symmetric" ] && [ -z "$RB" ]; then
        echo "preflight: WRITE_REFERENCE=1 but $REF already holds both branch entries (deflected, symmetric); step 6 would refuse to replace either. To replace one, set SMOKE_REPLACE_BRANCH=deflected or SMOKE_REPLACE_BRANCH=symmetric (the other branch is kept; a run landing on the other branch is refused, exit 2)"; exit 2
    fi
    [ "$BR" = - ] && BR="none (new file)"
    if [ -n "$RB" ]; then echo "WRITE_REFERENCE=1: reference run, no comparison; entries in $REF: $BR. Step 6 replaces the $RB entry IF the run lands on the $RB branch (the other entry is kept); a run on the other branch is refused (exit 2, file unchanged)"
    else echo "WRITE_REFERENCE=1: reference run, no comparison; entries in $REF: $BR. Step 6 adds this run as the branch it lands on if that branch has no entry yet; an existing entry is not replaced (exit 2; set SMOKE_REPLACE_BRANCH)"; fi
fi
[ -f "$FOAM_BASHRC" ] || { echo "OpenFOAM v2406 bashrc not found: $FOAM_BASHRC (set FOAM_BASHRC)"; exit 2; }
# the OpenFOAM v2406 bashrc references unset variables (WM_PROJECT_SITE, ...): set -u is suspended only while it is sourced (under set -u the source aborts the script)
set +u; source "$FOAM_BASHRC" || { echo "preflight: sourcing $FOAM_BASHRC failed"; exit 2; }; set -u
echo "WM_PROJECT_VERSION=${WM_PROJECT_VERSION:-<unset>} (required: v2406, ESI)"
[ "${WM_PROJECT_VERSION:-}" = v2406 ] || { echo "preflight: WM_PROJECT_VERSION '${WM_PROJECT_VERSION:-}' is not v2406 (ESI OpenFOAM v2406 required; set FOAM_BASHRC)"; exit 2; }
for c in cartesianMesh checkMesh decomposePar mpirun simpleFoam; do command -v "$c" > /dev/null || { echo "preflight: $c not found after sourcing $FOAM_BASHRC"; exit 2; }; done
for c in wmake g++; do command -v "$c" > /dev/null || { echo "preflight: $c not found (needed to compile the coded resistance BC)"; exit 2; }; done
PHYS=$(lscpu -p=CORE,SOCKET 2> /dev/null | grep -v '^#' | grep -E '^[0-9]+,[0-9]+$' | sort -u | wc -l)
if ! [ "${PHYS:-0}" -gt 0 ] 2> /dev/null; then
    if [[ "${SMOKE_PHYS_CORES:-}" =~ ^[1-9][0-9]*$ ]]; then PHYS=$SMOKE_PHYS_CORES; echo "physical cores from SMOKE_PHYS_CORES: $PHYS (lscpu could not establish them)"
    elif [ "${SMOKE_ALLOW_FEWER_CORES:-0}" = 1 ]; then PHYS=0; echo "WARNING: lscpu could not establish the physical core count; SMOKE_ALLOW_FEWER_CORES=1: running anyway, the timing claim does not hold"
    else echo "preflight: lscpu cannot establish the physical core count (nproc counts logical CPUs, not used): set SMOKE_PHYS_CORES=<physical cores> or SMOKE_ALLOW_FEWER_CORES=1"; exit 2; fi
fi
if [ "$NP" -gt "$PHYS" ]; then
    [ "${SMOKE_ALLOW_FEWER_CORES:-0}" = 1 ] || { echo "preflight: NPROC $NP > $PHYS physical cores (set SMOKE_ALLOW_FEWER_CORES=1 to run anyway)"; exit 2; }
    echo "WARNING: the 30-minute claim needs 8 physical cores (NPROC $NP, physical cores $PHYS)"
elif [ "$PHYS" -lt 8 ] || [ "$NP" -lt 8 ]; then echo "WARNING: the 30-minute claim needs 8 physical cores (NPROC $NP, physical cores $PHYS)"; fi
[ ! -e "$W" ] || { echo "$W exists: remove it or choose another WORKDIR"; exit 2; }
WA=$(realpath -m -- "$W"); HA=$(realpath -m -- "$HERE")
if [ "$WA" = "$HA" ] || [[ "$WA" == "$HA"/* ]]; then
    [ "${SMOKE_ALLOW_WORKDIR_IN_TREE:-0}" = 1 ] || { echo "WORKDIR $WA is inside the smoke_test folder $HA (synced tree: large, changing mesh files): choose a WORKDIR outside it (default ${TMPDIR:-/tmp}/paper6_t6_smoke_work) or set SMOKE_ALLOW_WORKDIR_IN_TREE=1"; exit 2; }
    echo "WARNING: WORKDIR $WA inside the smoke_test folder (SMOKE_ALLOW_WORKDIR_IN_TREE=1)"
fi
[[ "$WA" == /mnt/* ]] && echo "WARNING: WORKDIR $WA is under /mnt/ (WSL DrvFs: slow I/O, the timing claim may not hold); a native Linux path such as /tmp/... is recommended"
echo "WORKDIR=$WA"
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-8}
T0=$(date +%s); step() { echo "$(date +%T) [+$(( $(date +%s) - T0 )) s] $*"; }
SHA=""; CHK_OK=null; CELLS=null; RW_IN=null; RW_OUT=null
write_checks() { python3 -c 'import json, sys; a = sys.argv[1:]; j = lambda s: json.loads(s)
json.dump(dict(stl_sha256=a[0] or None, stl_sha256_expected=a[1], checkMesh_ok=j(a[2]), cells=j(a[3]), inlet_rewrites=j(a[4]), outlet_rewrites=j(a[5]), omp_num_threads=a[6]), open("smoke_checks.json", "w"), indent=1)' \
    "$SHA" "$STL_SHA256" "$CHK_OK" "$CELLS" "$RW_IN" "$RW_OUT" "$OMP_NUM_THREADS"; }
mkdir -p "$W/constant/triSurface" "$W/geo" && cd "$W" || exit 2
step "1/6 geometry (analytic, numpy only): sten70.stl"
python3 "$GEN" geo --ds 70 > log.geometry 2>&1 || { echo "geometry failed, see $W/log.geometry"; exit 3; }
mv geo/sten70.stl constant/triSurface/sten70.stl; rm -rf geo; sha256sum constant/triSurface/sten70.stl | tee stl.sha256; SHA=$(cut -d' ' -f1 stl.sha256)
[ "$SHA" = "$STL_SHA256" ] || { write_checks; echo "NON-COMPARABLE: STL sha256 $SHA != expected $STL_SHA256"; exit 3; }
cp -r "$HERE/case_files/0" "$HERE/case_files/system" "$HERE/case_files/constant" . 2>/dev/null; mv system/decomposeParDict.template system/decomposeParDict; sed -i "s/@NPROC@/$NP/" system/decomposeParDict
step "2/6 mesh (cfMesh cartesianMesh, 4 boundary layers, OMP_NUM_THREADS=$OMP_NUM_THREADS)"; cartesianMesh > log.cartesianMesh 2>&1 || { write_checks; echo "cartesianMesh failed, see $W/log.cartesianMesh"; exit 3; }
step "3/6 checkMesh"; checkMesh > log.checkMesh 2>&1; CRC=$?; grep -E "cells:|Mesh OK|Failed" log.checkMesh | head -5
CELLS=$(grep -m1 -E "^\s*cells:\s+[0-9]+" log.checkMesh | tr -dc 0-9); CELLS=${CELLS:-null}
if [ $CRC -eq 0 ] && grep -q "Mesh OK" log.checkMesh; then CHK_OK=true; else CHK_OK=false; write_checks; echo "NON-COMPARABLE: checkMesh failed (rc $CRC, 'Mesh OK' $(grep -q 'Mesh OK' log.checkMesh && echo present || echo absent)), see $W/log.checkMesh"; exit 3; fi
# cfMesh writes the inlet and outlet patches as type wall in constant/polyMesh/boundary: patch types must be 'patch' for inlet and outlet (exactly one rewrite each, reported)
RW=$(python3 - <<'PY'
import re
f = "constant/polyMesh/boundary"; s = open(f).read(); n = {}
for p in ("inlet", "outlet"): s, n[p] = re.subn(r"(\b%s\s*\{[^}]*?type\s+)wall(\s*;)" % p, r"\1patch\2", s, flags=re.S)
open(f, "w").write(s); print(n["inlet"], n["outlet"])
PY
); read -r RW_IN RW_OUT <<< "$RW"; echo "wall -> patch rewrites: inlet ${RW_IN:-?}, outlet ${RW_OUT:-?}"
[[ "${RW_IN:-x}" =~ ^[0-9]+$ ]] || RW_IN=null; [[ "${RW_OUT:-x}" =~ ^[0-9]+$ ]] || RW_OUT=null
write_checks
[ "${RW_IN:-}" = 1 ] && [ "${RW_OUT:-}" = 1 ] || { echo "NON-COMPARABLE: wall -> patch rewrites must be exactly inlet 1 and outlet 1: inlet ${RW_IN:-?}, outlet ${RW_OUT:-?}"; exit 3; }
step "4/6 decomposePar ($NP subdomains)"; decomposePar -force > log.decomposePar 2>&1 || { echo "decomposePar failed"; exit 3; }
step "5/6 simpleFoam -parallel ($N_ITER iterations; the coded BC is compiled on first use: about 1-2 minutes)"
mpirun -np "$NP" --bind-to core --map-by core simpleFoam -parallel > log.simpleFoam 2>&1; RC=$?
[ $RC -eq 0 ] || { echo "simpleFoam failed (rc $RC), see $W/log.simpleFoam"; exit 4; }
if [ "${WRITE_REFERENCE:-0}" = 1 ]; then
    step "6/6 write reference"; python3 "$HERE/compare_smoke.py" "$W" "$REF" --wall $(( $(date +%s) - T0 )) --write-reference "$REF" ${SMOKE_REPLACE_BRANCH:+--replace-branch "$SMOKE_REPLACE_BRANCH"}; exit $?
fi
step "6/6 compare"; echo "solver rc=$RC"; python3 "$HERE/compare_smoke.py" "$W" "$REF" --wall $(( $(date +%s) - T0 )); RC=$?
[ $RC -eq 0 ] && echo "PASS means: a correct install reaching one of the two validated steady states of this case (same mesh recipe and cell count, not mesh identity); only the deflected-jet branch reproduces the returned value 1.17392231e-06 m3/s (SETUP.md section 4)"
exit $RC
