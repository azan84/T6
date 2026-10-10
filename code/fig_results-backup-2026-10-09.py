"""fig_results.py — Figs. 2-4 of the JBHI manuscript from one ablation run and its analysis folder.

usage: fig_results.py <ablation.csv> <analysis_dir> <out_dir>
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, an, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 7, "axes.linewidth": 0.5, "xtick.major.width": 0.5,
                     "ytick.major.width": 0.5, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "pdf.fonttype": 42})
COL = {"A_fixed": "#2a78d6", "B_rederived": "#eb6834", "C_flowmatched": "#1baf7a"}
MRK = {"A_fixed": "o", "B_rederived": "s", "C_flowmatched": "^"}
LS = {"A_fixed": "-", "B_rederived": "--", "C_flowmatched": ":"}
LAB = {"A_fixed": "A fixed", "B_rederived": "B re-derived", "C_flowmatched": "C tuned"}
ET = {"T1_missed_branch": "T1 missed branch", "T2_truncation": "T2 vessel break",
      "T3_stenosis_length": "T3 lesion length", "T4_taper": "T4 taper"}
BED = {"discrete": "Discrete bed", "leaky": "Leaky bed"}
GREY, INK = "#8a8a85", "#2b2b2b"

# Discrete arm = healthy-network-eligible instances (same filter as analyse_ablation.py)
df = pd.read_csv(src)
el = pd.read_csv(src.parent / "discrete_arm_eligibility.csv")
key = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]
el = el[el.eligible.astype(bool)][key].assign(_e=True)
df = df.merge(el, on=key, how="left"); df = df[(df.bed != "discrete") | df._e.fillna(False).astype(bool)]
ok = df[(df.status == "ok") & (df.error_type != "clean")].copy()
ok["flip"] = ok.flip.astype(bool)

# ---------------- Fig. 2: P(flip | baseline band), 2 beds x 4 error types, floor 6a as grey band
pb = pd.read_csv(an / "P1_flip_by_band.csv")
fig, axs = plt.subplots(2, 4, figsize=(7.16, 2.55), sharex=True, sharey=True)
for i, bed in enumerate(["discrete", "leaky"]):
    for j, et in enumerate(ET):
        ax = axs[i, j]; g = pb[(pb.bed == bed) & (pb.error_type == et)]
        fl = g.groupby("band_bed").floor6a_pct.mean()
        ax.fill_between(fl.index + 0.025, 0, fl.values, color=GREY, alpha=0.25, lw=0, step=None)
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

# ---------------- Fig. 3: absorption plane, topological errors, per bed
fig, axs = plt.subplots(1, 2, figsize=(3.5, 1.75), sharey=True)
topo = ok[ok.error_type.isin(["T1_missed_branch", "T2_truncation"])].dropna(subset=["outlet_flow_residual"])
for ax, bed in zip(axs, ["discrete", "leaky"]):
    for y0, y1 in ((0.05, 0.45), (-0.45, -0.05)):
        ax.fill_between([0, 0.10], y0, y1, color=GREY, alpha=0.22, lw=0)
    for p in COL:
        h = topo[(topo.bed == bed) & (topo.protocol == p)]
        ax.scatter(h.outlet_flow_residual, h.dFFR, s=6, marker=MRK[p], facecolor=COL[p], edgecolor="white",
                   linewidth=0.3, alpha=0.85, label=LAB[p])
    ax.axhline(0, color=GREY, lw=0.4); ax.set_xscale("symlog", linthresh=0.01)
    ax.set_xlim(0, 1.0); ax.set_ylim(-0.25, 0.45); ax.set_title(BED[bed], fontsize=7)
    ax.set_xticks([0, 0.01, 0.1, 1]); ax.set_xticklabels(["0", "0.01", "0.1", "1"])
    ax.set_xlabel("Perfusion residual")
axs[0].set_ylabel(r"$\Delta$FFR")
axs[0].legend(loc="upper left", fontsize=6, handletextpad=0.2, borderaxespad=0.1, markerscale=1.5)
fig.tight_layout(); fig.savefig(out / "fig3_absorption.pdf"); plt.close(fig)

# ---------------- Fig. 4: T1, paired A vs C
fig, ax = plt.subplots(figsize=(3.5, 1.7))
t1 = ok[ok.error_type == "T1_missed_branch"]
for bed, m, c in (("discrete", "o", "#2a78d6"), ("leaky", "^", "#eb6834")):
    w = t1[t1.bed == bed].pivot_table(index=["scan", "side", "vessel", "loc", "L_mm", "ds_pct"],
                                       columns="protocol", values="dFFR")[["A_fixed", "C_flowmatched"]].dropna()
    ax.scatter(w.A_fixed, w.C_flowmatched, s=8, marker=m, facecolor=c, edgecolor="white", linewidth=0.3,
               label=f"{BED[bed]} (n = {len(w)})")
lim = (-0.01, 0.21)
ax.plot(lim, lim, color=GREY, lw=0.6); ax.axhline(0.05, color=GREY, lw=0.4, ls="--")
ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel(r"$\Delta$FFR, protocol A"); ax.set_ylabel(r"$\Delta$FFR, protocol C")
ax.legend(loc="upper left", fontsize=6); ax.grid(color="#e6e6e3", lw=0.4)
fig.tight_layout(); fig.savefig(out / "fig4_branch_loss.pdf"); plt.close(fig)
print("wrote", out)
