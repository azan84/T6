#!/bin/bash
# t6slice.sh <pdf-path> [mode]
# Cheap text slices for T6 triage. Never renders pages as images.
#   mode = triage (default): front matter (pages 1-4) + tail of body before references
#   mode = full            : whole document text
#   mode = grep            : T6 keyword hits with surrounding context, whole document
set -u
f="$1"; mode="${2:-triage}"
[ -f "$f" ] || { echo "MISSING FILE: $f"; exit 1; }

case "$mode" in
  full)
    pdftotext -q "$f" - 2>/dev/null
    ;;
  grep)
    pdftotext -q "$f" - 2>/dev/null | grep -n -i -E \
      'boundary condition|windkessel|resistance|calibrat|tun(e|ed|ing)|inter.?observer|inter.?reader|inter.?segmenter|variabilit|uncertain|perturb|segmentation error|topolog|side.?branch|reclassif|flip|0\.8|threshold|WSS|wall shear|OSI|oscillatory|mesh|snappyHex|svZeroD|zero.?dimensional|reduced.?order|OpenFOAM|SimVascular' \
      -A2 -B2
    ;;
  *)
    echo "===== FRONT (pages 1-4) ====="
    pdftotext -q -f 1 -l 4 "$f" - 2>/dev/null | head -c 18000
    echo
    echo "===== TAIL (end of body, references trimmed) ====="
    pdftotext -q "$f" - 2>/dev/null \
      | awk 'BEGIN{IGNORECASE=1} /^[[:space:]]*(References|REFERENCES|Bibliography)[[:space:]]*$/{exit} {print}' \
      | tail -c 12000
    ;;
esac
