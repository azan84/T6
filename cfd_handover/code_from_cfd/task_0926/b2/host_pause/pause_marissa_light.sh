#!/bin/bash
# Light pause watcher (2026-10-01, replaces the full-/proc scan loop of pause_marissa.sh --watch during B2): every 30 s, SIGSTOP any NEW running process of the
# OpenFOAM_Marissa project among (a) solver/mesher/MPI executables and (b) processes whose command line names the project or its queue/case/generator scripts;
# the project's interactive claude CLI, MCP helpers and login shell are never touched. Appends to paused.pids like pause_marissa.sh (resume_marissa.sh resumes all).
# usage: pause_marissa_light.sh SECONDS
D=$(dirname "$0"); end=$(( $(date +%s) + ${1:-36000} )); KEEP_RE='(^| )claude( |$)|mcp|server-pdf|npm exec|^-bash'
while [ $(date +%s) -lt $end ]; do
  for p in $( { pgrep -x 'simpleFoam|pimpleFoam|mpirun|orted|blockMesh|snappyHexMesh|cartesianMesh|decomposePar|reconstructPar|checkMesh|potentialFoam'; pgrep -f 'OpenFOAM_Marissa|OpenFOAM-Marissa|run_queue|run_case|gen_case'; } | sort -un); do
    [ "$p" = "$$" ] && continue; st=$(ps -o stat= -p $p 2>/dev/null) || continue; [[ "$st" == T* ]] && continue
    c=$(readlink /proc/$p/cwd 2>/dev/null); a=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
    case "$c $a" in *OpenFOAM_Marissa*|*OpenFOAM-Marissa*) ;; *) continue;; esac
    [[ "$a" =~ $KEEP_RE ]] && continue
    kill -STOP $p 2>/dev/null && echo "$p $(date +%T) ${a:0:160}" >> "$D/paused.pids"
  done
  sleep 30
done
