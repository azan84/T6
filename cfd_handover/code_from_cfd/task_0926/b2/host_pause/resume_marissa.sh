#!/bin/bash
# Resume (SIGCONT) every process paused by pause_marissa.sh (paused.pids); stop any running --watch loop first.
D=$(dirname "$0"); for f in "$D"/watcher.pid; do [ -f "$f" ] && kill "$(cat "$f")" 2>/dev/null; done
awk '{print $1}' "$D/paused.pids" | sort -u | while read p; do kill -CONT $p 2>/dev/null && echo "resumed $p"; done; mv "$D/paused.pids" "$D/paused.pids.$(date +%Y%m%d_%H%M%S).done"
