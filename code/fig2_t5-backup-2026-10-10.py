"""fig2_t5.py — Fig. 2 with the half-voxel throat error (T5, both signs pooled) as a fifth column.
usage: fig2_t5.py <ablation.csv> <analysis_dir> <ablation_t5.csv> <out_dir>"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import norm
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, an, t5src, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
out.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 7, "axes.linewidth": 0.5, "xtick.major.width": 0.5,
                     "ytick.major.width": 0.5, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "pdf.fonttype": 42})
COL = {"A_fixed": "#2a78d6", "B_rederived": "#eb6834", "C_flowmatched": "#1baf7a"}
MRK = {"A_fixed": "o", "B_rederived": "s", "C_flowmatched": "^"}
LS = {"A_fixed": "-", "B_rederived": "--", "C_flowmatched": ":"}
LAB = {"A_fixed": "A fixed", "B_rederived": "B re-derived", "C_flowmatched": "C tuned"}
ET = {"T1_missed_branch": "T1 missed branch", "T2_truncation": "T2 vessel break",
      "T3_stenosis_length": "T3 lesion length", "T4_taper": "T4 taper", "T5": "T5 throat $\\pm\\frac{1}{2}$ voxel"}
BED = {"discrete": "Discrete bed", "leaky": "Leaky bed"}
GREY = "#8a8a85"
KEY = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]

def band_of(f):
    f = np.asarray(f, float); i = np.floor((f - 0.65) / 0.05)
    return np.where((f >= 0.65) & (f < 0.95), 0.65 + 0.05 * i, np.nan).round(2)

pb = pd.read_csv(an / "P1_flip_by_band.csv")
el = pd.read_csv(src.parent / "discrete_arm_eligibility.csv")
el = el[el.eligible.astype(bool)][KEY].assign(_e=True)
t5 = pd.read_csv(t5src)
t5 = t5[t5.error_type.isin(["T5_vox_narrow", "T5_vox_wide"]) & (t5.status == "ok")]
t5 = t5.merge(el, on=KEY, how="left"); t5 = t5[(t5.bed != "discrete") | t5._e.fillna(False).astype(bool)].copy()
t5["band_bed"] = band_of(t5.ffr_clean.values)
t5["flip"] = t5.flip.astype(bool)
t5["floor"] = 100 * norm.cdf(-np.abs(t5.ffr_clean - 0.80) / 0.018)
g5 = t5.groupby(["bed", "protocol", "band_bed"]).agg(n=("flip", "size"), flip_pct=("flip", lambda s: 100 * s.mean()),
                                                      floor=("floor", "mean")).reset_index()

fig, axs = plt.subplots(2, 5, figsize=(7.16, 2.55), sharex=True, sharey=True)
for i, bed in enumerate(["discrete", "leaky"]):
    for j, et in enumerate(ET):
        ax = axs[i, j]
        if et == "T5":
            g = g5[g5.bed == bed]; fl = g.groupby("band_bed")["floor"].mean()
        else:
            g = pb[(pb.bed == bed) & (pb.error_type == et)]; fl = g.groupby("band_bed").floor6a_pct.mean()
        ax.fill_between(fl.index + 0.025, 0, fl.values, color=GREY, alpha=0.25, lw=0)
        for p in COL:
            h = g[(g.protocol == p) & (g.n >= 3)].sort_values("band_bed")
            ax.plot(h.band_bed + 0.025, h.flip_pct, LS[p], color=COL[p], lw=1.2, marker=MRK[p], ms=3.2,
                    mec="white", mew=0.4, label=LAB[p])
        ax.axvline(0.80, color=GREY, lw=0.5, ls="-")
        ax.set_ylim(0, 100); ax.set_xlim(0.65, 0.95); ax.set_xticks([0.70, 0.80, 0.90])
        ax.grid(axis="y", color="#e6e6e3", lw=0.4)
        if i == 0: ax.set_title(ET[et], fontsize=7)
        if j == 0: ax.set_ylabel(f"{BED[bed]}\nflips (%)")
        if i == 1: ax.set_xlabel("Baseline FFR band")
h, l = axs[0, 0].get_legend_handles_labels()
h.append(plt.Rectangle((0, 0), 1, 1, color=GREY, alpha=0.25)); l.append("Repeat-FFR floor")
fig.legend(h, l, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.02))
fig.tight_layout(rect=(0, 0, 1, 0.93)); fig.savefig(out / "fig2_flip_by_band.pdf"); plt.close(fig)
print("wrote", out / "fig2_flip_by_band.pdf")
