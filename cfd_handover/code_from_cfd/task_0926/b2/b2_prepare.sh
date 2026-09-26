#!/bin/bash
# Task B2 preparation (no solve): builds the three case directories from the finished scan-14 baseline resistance case (m1/cases/baseline_resistance: mesh, dictionaries, coded BC with its compiled dynamicCode) and decomposes them:
#   b2/L16/case (16 subdomains), b2/L8/caseA and b2/L8/caseB (8 subdomains each). controlDict: endTime 1600, writeInterval 100000 (no field writes: the wall clock measures the iterations), everything else identical.
# 1600 iterations = the B1 first-settled iteration of this case (1229) plus a margin (30 %); b2_analyse.py applies the B1 rule to the monitors and takes the wall clock at the settle iteration.
# build_info.json is copied and then patched to the prepared run by b2_patch_buildinfo.py (nproc = subdomains, endTime 1600, writeInterval 100000, b2_note; other keys kept; audit 0926-SETUPS finding 5).
# usage: b2_prepare.sh        (about 5 GB of disk in total; refuses below 12 GB free; nice -n 10; fails if a target exists)
P=/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot; SRC=$P/m1/cases/baseline_resistance; B=$P/b2
[ "$(df --output=avail -B1G / | tail -1 | tr -dc 0-9)" -ge 12 ] || { echo "less than 12 GB free"; exit 2; }
for f in constant/polyMesh system/controlDict system/fvSchemes system/fvSolution 0/p 0/U dynamicCode zerod_reference.json build_info.json; do [ -e "$SRC/$f" ] || { echo "missing $SRC/$f"; exit 2; }; done
source /usr/lib/openfoam/openfoam2406/etc/bashrc || exit 2
for spec in L16/case:16 L8/caseA:8 L8/caseB:8; do
    d=$B/${spec%%:*}; n=${spec##*:}; [ ! -e "$d" ] || { echo "$d exists"; exit 2; }
    mkdir -p "$d" && cp -a "$SRC/constant" "$SRC/system" "$SRC/0" "$SRC/dynamicCode" "$SRC/zerod_reference.json" "$SRC/build_info.json" "$SRC/case.foam" "$d/" || exit 2
    sed -i -e 's/^endTime .*/endTime         1600;/' -e 's/^writeInterval .*/writeInterval   100000;/' "$d/system/controlDict"
    printf 'FoamFile { version 2.0; format ascii; class dictionary; object decomposeParDict; }\nnumberOfSubdomains %s;\nmethod scotch;\n' "$n" > "$d/system/decomposeParDict"
    grep -E "^(endTime|writeInterval|stopAt)" "$d/system/controlDict" | tr '\n' ' '; echo
    ( cd "$d" && nice -n 10 decomposePar -force > log.decomposePar 2>&1 ) || { echo "decomposePar failed in $d"; exit 3; }
    python3 "$B/b2_patch_buildinfo.py" "$d" "$n" || { echo "build_info.json patch failed in $d"; exit 3; }
    echo "$d: $(ls -d $d/processor* | wc -l) processor dirs, $(du -sh $d | cut -f1)"
done
