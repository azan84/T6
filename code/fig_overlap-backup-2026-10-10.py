"""fig_overlap.py — tube-model Dice score of each corrupted tree against the change in FFR under fixed boundary
conditions (Protocol A), by error type and bed.
usage: fig_overlap.py <overlap_joined.csv> <out_dir>"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 7, "axes.linewidth": 0.5, "xtick.major.width": 0.5,
                     "ytick.major.width": 0.5, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "pdf.fonttype": 42})
ET = {"T1_missed_branch": ("T1 missed branch", "#d0473b", "o"), "T2_truncation": ("T2 vessel break", "#7a3fb0", "D"),
      "T3_stenosis_length": ("T3 lesion length", "#8a8a85", "s"), "T4_taper": ("T4 taper", "#2a78d6", "^")}
BED = {"discrete": "Discrete bed", "leaky": "Leaky bed"}
d = pd.read_csv(src)
d = d[d.error_type.isin(ET)].dropna(subset=["net_dsc_scan", "dFFR_A"]).rename(columns={"dFFR_A": "dFFR"})
fig, axs = plt.subplots(1, 2, figsize=(3.5, 1.9), sharey=True)
for ax, bed in zip(axs, ["discrete", "leaky"]):
    ax.axhspan(-0.05, 0.05, color="#e9e9e6", lw=0)
    ax.axvline(0.928, color="#8a8a85", lw=0.6, ls="--")
    for et, (lab, c, m) in ET.items():
        h = d[(d.bed == bed) & (d.error_type == et)]
        ax.scatter(h.net_dsc_scan, h.dFFR, s=6, marker=m, facecolor=c, edgecolor="white", linewidth=0.3,
                   alpha=0.85, label=lab)
    ax.set_xlim(0.75, 1.0); ax.set_ylim(-0.1, 0.56); ax.set_xticks([0.8, 0.9, 1.0]); ax.set_title(BED[bed], fontsize=7)
    ax.set_xlabel("Dice score, whole scan")
axs[0].set_ylabel(r"$\Delta$FFR, Protocol A")
axs[0].legend(loc="upper left", fontsize=5.5, handletextpad=0.2, borderaxespad=0.1, markerscale=1.4)
fig.tight_layout(); fig.savefig(out / "fig_overlap.pdf"); plt.close(fig)
print("wrote", out / "fig_overlap.pdf")
