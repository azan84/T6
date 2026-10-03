#!/usr/bin/env bash
# Test of make_manifest.sh / verify_manifest.sh: __pycache__/, *.pyc and .git/ neither listed nor reported as extra; LF copy (plain sha256sum -c and verify pass), CRLF copy incl. the manifest itself (verify passes), tampered file (verify fails).
set -u; H="$(cd "$(dirname "$0")/.." && pwd)"; T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT; fail=0
mkdir -p "$T/d/sub dir"; printf 'a\nb\n' > "$T/d/x.py"; printf 'line one\nline two\n' > "$T/d/sub dir/my file.md"; printf '\x00\x01\r\n\x02' > "$T/d/bin.dat"
mkdir -p "$T/d/__pycache__" "$T/d/.git"; printf 'x' > "$T/d/__pycache__/x.cpython-310.pyc"; printf 'y' > "$T/d/stray.pyc"; printf 'z' > "$T/d/.git/HEAD"
"$H/make_manifest.sh" "$T/d" >/dev/null
grep -qE '__pycache__|\.pyc$|\.git/' "$T/d/MANIFEST.sha256" && { echo "FAIL: generated/VCS files listed"; fail=1; }
"$H/verify_manifest.sh" "$T/d" | grep -qE '__pycache__|stray.pyc|\.git/' && { echo "FAIL: generated/VCS files reported as extra"; fail=1; }
grep -q '^#' "$T/d/MANIFEST.sha256" && { echo "FAIL: comment line in MANIFEST.sha256"; fail=1; }
(cd "$T/d" && sha256sum -c --quiet MANIFEST.sha256) || { echo "FAIL: plain sha256sum -c on the LF copy"; fail=1; }
"$H/verify_manifest.sh" "$T/d" >/dev/null || { echo "FAIL: verify on the LF copy"; fail=1; }
for f in "$T/d/x.py" "$T/d/sub dir/my file.md" "$T/d/MANIFEST.sha256"; do sed -i 's/$/\r/' "$f"; done
"$H/verify_manifest.sh" "$T/d" >/dev/null || { echo "FAIL: verify on the CRLF copy"; fail=1; }
echo x >> "$T/d/x.py"; "$H/verify_manifest.sh" "$T/d" >/dev/null && { echo "FAIL: tampered file passed"; fail=1; }
[ $fail -eq 0 ] && echo "PASS test_manifest" ; exit $fail
