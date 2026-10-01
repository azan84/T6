#!/bin/bash
# Pause (SIGSTOP) every process of the OpenFOAM_Marissa project EXCEPT its interactive claude CLI, its MCP helpers and its login shell,
# so the host is idle for the Paper6-T6 B2 throughput measurement (user request 2026-10-01). PIDs are appended to paused.pids; resume with resume_marissa.sh.
# usage: pause_marissa.sh [--watch SECONDS]   (--watch: repeat every 10 s for SECONDS, to catch jobs started later)
D=$(dirname "$0"); KEEP_RE='(^| )claude( |$)|mcp|server-pdf|npm exec|^-bash'
once() {
  for p in $(ps -eo pid=); do
    [ "$p" = "$$" ] && continue
    c=$(readlink /proc/$p/cwd 2>/dev/null) || continue; a=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
    case "$c $a" in *OpenFOAM_Marissa*|*OpenFOAM-Marissa*) ;; *) continue;; esac
    [[ "$a" =~ $KEEP_RE ]] && continue
    st=$(ps -o stat= -p $p 2>/dev/null); [[ "$st" == T* ]] && continue
    kill -STOP $p 2>/dev/null && echo "$p $(date +%T) ${a:0:160}" >> "$D/paused.pids"
  done
}
once; if [ "${1:-}" = --watch ]; then end=$(( $(date +%s) + ${2:-3600} )); while [ $(date +%s) -lt $end ]; do sleep 10; once; done; fi
