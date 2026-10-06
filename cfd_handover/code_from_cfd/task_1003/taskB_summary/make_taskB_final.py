"""Task B (WO 2026-10-03 section 3) summary of the jet-state re-runs of all five U3D levels -> U3D_jet_state_check_2026-10-06.csv.
S25B/S12A/S12B from u3d_check/result_<L>.json; S50/S25A (checked 2026-10-02 before result_*.json existed) from jet_offset_<L>.txt and the
FFR values reported in the report (U3D (v) update) - marked in the 'source' column. GCI21 recomputed from the ORIGINAL level values."""
import json, re, csv, sys
U = "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check"
out = sys.argv[1]
orig = dict(S50=0.793362, S25A=0.791103, S12A=0.790308, S25B=0.791197, S12B=0.790418)
rows = []
for L, ffr, cells, it in (("S50", 0.793363, 2687640, 3000), ("S25A", 0.791103, 3194196, 4000)):
    t = open(f"{U}/jet_offset_{L}.txt").read()
    o50 = float(re.search(r"x=50\.0: ([\d.]+) um", t).group(1)); o56 = float(re.search(r"x=56\.5: ([\d.]+) um", t).group(1))
    rows.append(dict(level=L, cells=cells, iterations=it, mpi_ranks=8, FFR_original=orig[L], FFR_rerun=ffr, dFFR=round(ffr - orig[L], 9), FFR_last100_band="",
                     offset_x50_um=o50, offset_x56p5_um=o56, verdict="axisymmetric", source=f"jet_offset_{L}.txt + FFR as reported (report U3D (v) update, 2026-10-02); 6-digit FFR"))
for L in ("S25B", "S12A", "S12B"):
    r = json.load(open(f"{U}/result_{L}.json"))
    rows.append(dict(level=L, cells=r["cells"], iterations=r["iterations"], mpi_ranks=r["mpi_ranks"], FFR_original=r["FFR_original"], FFR_rerun=round(r["FFR_last100_mean"], 9),
                     dFFR=round(r["dFFR"], 10), FFR_last100_band=f'{r["FFR_last100_band"]:.2e}', offset_x50_um=r["jet_offset_x50_um"], offset_x56p5_um=r["jet_offset_x56p5_um"],
                     verdict=r["verdict"], source=f"result_{L}.json ({r['written']})"))
def gci(f3, f2, f1):
    import math
    e32, e21 = f3 - f2, f2 - f1; p = math.log(e32 / e21) / math.log(2); return p, 1.25 * abs(e21) / (2 ** p - 1)
pA, gA = gci(orig["S50"], orig["S25A"], orig["S12A"]); pB, gB = gci(orig["S50"], orig["S25B"], orig["S12B"])
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    f.write(f"# GCI21 (absolute, from the original values): zone A p={pA:.3f} GCI={gA:.6f}; zone B p={pB:.3f} GCI={gB:.6f}; U3D = max = {max(gA, gB):.5f}\n")
    f.write("# all five levels axisymmetric (rule (a) of u3d_check/U3D_CHECK_DESIGN.md): U3D final under D9\n")
print(open(out).read())
