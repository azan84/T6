"""E0 guard (work order 2026-09-24 section 7): a cohort case may only be built if (scan, side) is in protocol/CFD-SUBSET-FROZEN-2026-09-18.csv.
check(scan, side, csv_path=DEFAULT, waiver=None) -> dict recorded in build_info.json. The frozen csv is NOT on the CFD machine (searched 2026-09-24): without the file the guard FAILS LOUDLY unless an explicit,
logged waiver string is passed (--e0-waiver); the waiver text is stored with the case. Independent of the geometry stage's own copy of the guard (same semantics)."""
import csv, os, sys
DEFAULT = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/CFD-SUBSET-FROZEN-2026-09-18.csv"      # shipped with cfd_handover-2026-09-26.zip

def check(scan, side, csv_path=DEFAULT, waiver=None):
    if os.path.exists(csv_path):
        sub = {(r["scan"], r["side"]) for r in csv.DictReader(open(csv_path))}
        assert (str(scan), side) in sub, f"{scan}-{side} is not in the frozen CFD subset - do not run it as a cohort case"
        return dict(status="MEMBER", csv=csv_path, scan=str(scan), side=side)
    if waiver: return dict(status="WAIVED (frozen subset csv not available on this machine)", csv=csv_path, scan=str(scan), side=side, waiver=waiver)
    raise SystemExit(f"E0 guard: {csv_path} not found. The assertion cannot be executed; pass --e0-waiver '<reason>' to record an explicit waiver (evidence: package README/MANIFEST instance_key, work order text).")
