"""Re-issue returns/2026-10-03/P5/<scan>/settle_<scan>_resistance.csv as settle_<scan>_resistance_2026-10-06.csv with the empty 'contended' column filled
(post-hoc audit GPT-5.6 Sol, P5 finding 2: the P5 solves ran with up to 32 concurrent MPI ranks on 16 physical cores). Originals are kept unchanged."""
import csv, sys
R = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5"
V = "yes: up to 32 concurrent MPI ranks on the 16 physical cores (study lead's order 2026-10-03; 16-rank cap of WO 2026-09-24 not kept); wall clock is not a cost figure"
for s in ("138", "69", "473", "272", "139"):
    src = f"{R}/{s}/settle_{s}_resistance.csv"; rows = list(csv.DictReader(open(src))); keys = list(rows[0].keys())
    assert "contended" in keys
    for r in rows:
        assert r["contended"] in ("", None), (s, r["contended"]); r["contended"] = V
    with open(f"{R}/{s}/settle_{s}_resistance_2026-10-06.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, lineterminator="\n"); w.writeheader(); w.writerows(rows)
    print(s, len(rows), "rows")
