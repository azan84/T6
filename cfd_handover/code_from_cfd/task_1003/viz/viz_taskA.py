"""Task A (D7 sensitivity) result graph: section-averaged pressure along the lesion vessel for each variant against the returned baseline, with the difference panel.
usage: viz_taskA.py <out.png> <returned_probes.csv> <label>=<probes.csv> [...]"""
import sys, csv, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, ret = sys.argv[1], sys.argv[2]; var = [a.split("=", 1) for a in sys.argv[3:]]
def load(f):
    rows = [r for r in csv.DictReader(open(f)) if r["kind"] != "inlet" or True]
    return {r["probe_id"]: r for r in rows}
R = load(ret); ids = [k for k in R if k != "inlet" and R[k]["s_from_lesion_mm"] not in ("", "nan") and R[k]["p_over_Paorta"] not in ("", "nan")]; s = np.array([float(R[k]["s_from_lesion_mm"]) for k in ids]); pr = np.array([float(R[k]["p_over_Paorta"]) for k in ids])
fig, ax = plt.subplots(2, 1, figsize=(9.5, 6.2), sharex=True, gridspec_kw=dict(height_ratios=[2.2, 1]), constrained_layout=True)
ax[0].plot(s, pr, "ko-", ms=4, lw=1.2, label="returned baseline (25 um throat zone, 2026-09-26)")
cols = ["tab:red", "tab:blue", "tab:green", "tab:orange"]
for (lab, f), c in zip(var, cols):
    V = load(f); ids2 = [k for k in ids if k in V and V[k]["p_over_Paorta"] not in ("", "nan")]; pv_ = np.array([float(V[k]["p_over_Paorta"]) for k in ids2]); s2 = np.array([float(R[k]["s_from_lesion_mm"]) for k in ids2]); pr2 = np.array([float(R[k]["p_over_Paorta"]) for k in ids2]); ax[0].plot(s2, pv_, "s-", color=c, ms=3.5, lw=1, label=lab); ax[1].plot(s2, pv_ - pr2, "s-", color=c, ms=3.5, lw=1, label=lab)
ax[1].axhline(0.00055, color="0.4", ls="--", lw=0.9); ax[1].axhline(-0.00055, color="0.4", ls="--", lw=0.9); ax[1].axhline(0, color="k", lw=0.5)
for a in ax: a.axvline(0, color="r", ls=":", lw=1); a.axvline(30.18, color="c", ls="--", lw=1)
ax[0].set_ylabel("section-mean p / P_aorta"); ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3); ax[0].set_title("Scan 14 baseline (80 % DS LAD lesion), resistance mode: pressure along the LAD at the package probes", fontsize=10, loc="left")
ax[1].set_ylabel("difference to returned"); ax[1].set_xlabel("arc from the lesion centre (mm)\nred dotted: throat; cyan dashed: measurement probe p011; grey dashed: +-0.00055 (U3D)"); ax[1].grid(alpha=0.3); ax[1].legend(fontsize=8)
fig.savefig(out, dpi=170); print("wrote", out)
