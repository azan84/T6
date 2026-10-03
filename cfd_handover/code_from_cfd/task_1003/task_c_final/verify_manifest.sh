#!/usr/bin/env bash
# usage: verify_manifest.sh [DIR]   (default: the current directory; reads DIR/MANIFEST.sha256)
# Checks every entry with the hash rule of make_manifest.sh: text files (no NUL byte) hashed with every CR byte removed (LF-normalised),
# binary files hashed raw. Passes on any line-ending convention of the copy. Lines of MANIFEST.sha256 starting with '#' and blank lines
# are skipped, CR bytes in MANIFEST.sha256 itself are ignored. Prints "<path>: OK|FAILED|MISSING" per entry and lists files present
# under DIR but absent from the manifest (reported, not failed). Exit status 0 only if every entry is OK.
set -uo pipefail
export LC_ALL=C
DIR="${1:-.}"
cd "$DIR" || exit 2
[ -f MANIFEST.sha256 ] || { echo "no MANIFEST.sha256 in $(pwd)" >&2; exit 2; }
if command -v sha256sum >/dev/null 2>&1; then H() { sha256sum | cut -d' ' -f1; }; else H() { shasum -a 256 | cut -d' ' -f1; }; fi
is_text() { tr -d '\000' < "$1" | cmp -s - "$1"; }
ok=0; bad=0; LISTED="$(mktemp)"; trap 'rm -f "$LISTED"' EXIT
while IFS= read -r line; do
  line="${line%$'\r'}"
  case "$line" in ''|'#'*) continue;; esac
  want="${line%%  *}"; f="${line#*  }"; f="${f#\*}"          # "<hash>  <path>" (a binary-mode '*' marker is tolerated)
  echo "$f" >> "$LISTED"
  if [ ! -f "$f" ]; then echo "$f: MISSING"; bad=$((bad + 1)); continue; fi
  if is_text "$f"; then got="$(tr -d '\r' < "$f" | H)"; else got="$(H < "$f")"; fi
  if [ "$got" = "$want" ]; then echo "$f: OK"; ok=$((ok + 1)); else echo "$f: FAILED"; bad=$((bad + 1)); fi
done < <(tr -d '\r' < MANIFEST.sha256)
extra="$(find . \( -name __pycache__ -o -name .git \) -prune -o -type f ! -name MANIFEST.sha256 ! -name MANIFEST.README ! -name '*.pyc' -print | sed 's|^\./||' | sort | comm -23 - <(sort "$LISTED"))"
[ -n "$extra" ] && { echo "not in the manifest (not checked):"; echo "$extra" | sed 's/^/  /'; }
echo "verify_manifest: $ok OK, $bad FAILED/MISSING (LF-normalised text, raw binary)"
[ "$bad" -eq 0 ]
