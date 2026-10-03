"""E0 guard (work order 2026-09-24, section 7, rules 1-2): cohort cases may only come from protocol/CFD-SUBSET-FROZEN-2026-09-18.csv.
The assertion is the work order's own; if the csv is absent it FAILS LOUDLY unless an explicit, logged waiver text is passed.
usage: e0_guard.py <scan> <side> [--subset-csv PATH] [--e0-waiver "reason"]      returns 0 (member or waived), 2 (not a member / csv absent without waiver)."""
import csv, os, sys, argparse

DEFAULT_CSV = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/CFD-SUBSET-FROZEN-2026-09-18.csv"      # shipped with cfd_handover-2026-09-26.zip, sha256 8e0079a0...

def check(scan, side, subset_csv=DEFAULT_CSV, waiver=None):
    """Returns a dict for the gate report. Raises SystemExit (loud) on a failure that is not waived."""
    rep = dict(guard="E0 membership (work order 2026-09-24 section 7)", scan=str(scan), side=side, subset_csv=subset_csv, csv_present=os.path.exists(subset_csv))
    if rep["csv_present"]:
        sub = {(r["scan"], r["side"]) for r in csv.DictReader(open(subset_csv))}
        member = (str(scan), side) in sub
        rep.update(status="MEMBER" if member else "NOT_A_MEMBER", n_rows=len(sub))
        assert member, f"{scan}-{side} is not in the frozen CFD subset - do not run it as a cohort case"
        return rep
    if waiver:
        rep.update(status="WAIVED_CSV_ABSENT", waiver=waiver)
        print(f"E0 GUARD WAIVED: {subset_csv} is not on this machine. Waiver text: {waiver}", file=sys.stderr)
        return rep
    raise SystemExit(f"E0 GUARD FAILED: {subset_csv} is not on this machine and no --e0-waiver was given. The membership of scan {scan} ({side}) in the frozen CFD subset cannot be asserted; refusing to build.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("scan"); ap.add_argument("side"); ap.add_argument("--subset-csv", default=DEFAULT_CSV); ap.add_argument("--e0-waiver", default=None)
    a = ap.parse_args()
    try:
        print(check(a.scan, a.side, a.subset_csv, a.e0_waiver))
    except (AssertionError, SystemExit) as e:
        print(e, file=sys.stderr); sys.exit(2)
