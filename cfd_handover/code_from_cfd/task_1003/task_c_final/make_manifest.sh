#!/usr/bin/env bash
# usage: make_manifest.sh [DIR]   (default: the current directory)
# Writes DIR/MANIFEST.sha256 and DIR/MANIFEST.README (work order 2026-10-03 section 0).
# MANIFEST.sha256: one "<sha256>  <relative path>" line per file under DIR (sorted, LC_ALL=C; the MANIFEST.* files themselves and generated/VCS files - __pycache__/, *.pyc, .git/ - excluded),
#   NO comment lines, so that plain `sha256sum -c MANIFEST.sha256` / `shasum -a 256 -c MANIFEST.sha256` work on the body as is.
# Hash rule: TEXT files (no NUL byte) are hashed over their LF-normalised content, i.e. with every CR byte removed (tr -d '\r');
#   BINARY files (containing a NUL byte) are hashed raw. verify_manifest.sh applies the identical rule, so it passes whatever
#   line-ending convention the copy has (LF, CRLF after a Drive/Windows round trip, ...).
# Files written on this machine are LF, so the normalised hash equals the raw hash and plain `sha256sum -c` passes too; any text file
#   that does contain CR bytes is listed in MANIFEST.README (plain `sha256sum -c` would report it FAILED; verify_manifest.sh passes it).
set -euo pipefail
export LC_ALL=C
DIR="${1:-.}"
cd "$DIR"
if command -v sha256sum >/dev/null 2>&1; then H() { sha256sum | cut -d' ' -f1; }; else H() { shasum -a 256 | cut -d' ' -f1; }; fi
is_text() { tr -d '\000' < "$1" | cmp -s - "$1"; }        # no NUL byte -> text
TMP="$(mktemp)"; CRL="$(mktemp)"; trap 'rm -f "$TMP" "$CRL"' EXIT
n=0
while IFS= read -r -d '' f; do
  f="${f#./}"
  case "$f" in MANIFEST.sha256|MANIFEST.README) continue;; esac
  case "$f" in *$'\n'*|*$'\r'*) echo "refusing file name with CR/LF: $f" >&2; exit 1;; esac
  if is_text "$f"; then
    h="$(tr -d '\r' < "$f" | H)"
    if ! tr -d '\r' < "$f" | cmp -s - "$f"; then echo "$f" >> "$CRL"; fi
  else
    h="$(H < "$f")"
  fi
  printf '%s  %s\n' "$h" "$f" >> "$TMP"; n=$((n + 1))
done < <(find . \( -name __pycache__ -o -name .git \) -prune -o -type f ! -name '*.pyc' -print0 | sort -z)
mv "$TMP" MANIFEST.sha256; trap 'rm -f "$CRL"' EXIT
{
  echo "MANIFEST.sha256 ($n entries, written $(date -u +%Y-%m-%dT%H:%M:%SZ) by make_manifest.sh)"
  echo "Hashes are SHA-256 over LF-NORMALISED content: for text files (no NUL byte) every CR byte is removed before hashing (tr -d '\\r');"
  echo "binary files (containing a NUL byte) are hashed raw. MANIFEST.sha256 has no comment lines, so plain 'sha256sum -c MANIFEST.sha256'"
  echo "(or 'shasum -a 256 -c MANIFEST.sha256') works on it as is for an LF copy of the files."
  echo "For a copy with any line-ending convention (e.g. CRLF after a Windows/Drive round trip) run: verify_manifest.sh <dir>"
  echo "(same normalisation; it also ignores '#' lines and CR bytes in MANIFEST.sha256 itself)."
  if [ -s "$CRL" ]; then
    echo "Text files that contain CR bytes on the writing machine (plain sha256sum -c reports them FAILED, verify_manifest.sh passes them):"
    sed 's/^/  /' "$CRL"
  else
    echo "No text file contained CR bytes when the manifest was written: normalised hash == raw hash for every entry."
  fi
} > MANIFEST.README
echo "MANIFEST.sha256: $n entries in $(pwd)"
