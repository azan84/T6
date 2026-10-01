#!/bin/bash
# Lighter pause watcher v2 (2026-10-01 07:55; replaces pause_marissa_light.sh, whose per-scan ps/readlink calls on ~50 already-stopped PIDs cost up to 0.31 core in a 5-s sample
# of the B2 calibration): every 30 s two pgrep calls; PIDs already seen stopped are skipped in memory (no ps/readlink); only NEW matching PIDs are inspected and SIGSTOPped if they
# belong to OpenFOAM_Marissa (never its claude CLI, MCP helpers or login shell). Appends to paused.pids (resume_marissa.sh resumes all). usage: pause_marissa_light2.sh SECONDS
D=$(dirname "$0"); end=$(( $(date +%s) + ${1:-36000} )); KEEP_RE='(^| )claude( |$)|mcp|server-pdf|npm exec|^-bash'; declare -A SEEN
while [ $(date +%s) -lt $end ]; do
  for p in $( { pgrep -x 'simpleFoam|pimpleFoam|mpirun|orted|blockMesh|snappyHexMesh|cartesianMesh|decomposePar|reconstructPar|checkMesh|potentialFoam'; pgrep -f 'OpenFOAM_Marissa|OpenFOAM-Marissa|run_queue|run_case|gen_case'; } | sort -un); do
    [ -n "${SEEN[$p]}" ] && continue; [ "$p" = "$$" ] && continue
    read -r st < <(ps -o stat= -p $p 2>/dev/null) || continue
    c=$(readlink /proc/$p/cwd 2>/dev/null); a=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
    case "$c $a" in *OpenFOAM_Marissa*|*OpenFOAM-Marissa*) ;; *) continue;; esac     # foreign to Marissa: not remembered (may be ours; re-inspected next scan only if still matching)
    [[ "$a" =~ $KEEP_RE ]] && { SEEN[$p]=keep; continue; }
    if [[ "$st" != T* ]]; then kill -STOP $p 2>/dev/null && echo "$p $(date +%T) ${a:0:160}" >> "$D/paused.pids"; fi
    SEEN[$p]=stopped
  done
  sleep 30
done
