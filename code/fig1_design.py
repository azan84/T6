"""fig1_design.py — Fig. 1: study design as a left-to-right pipeline. usage: fig1_design.py <out pdf>"""
import sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({"font.family": "serif", "font.size": 5.3, "pdf.fonttype": 42})
INK, EDGE, FILL, ACC = "#2b2b2b", "#8a8a85", "#f4f4f1", "#2a78d6"
fig = plt.figure(figsize=(7.16, 1.55)); ax = fig.add_axes((0, 0, 1, 1)); ax.set_xlim(0, 100); ax.set_ylim(0, 22)
ax.axis("off")

stages = [
    ("Data", "ImageCAS-X test split\n160 CT angiography scans\nleft and right trees\ndistance-map radius"),
    ("Lesion insertion", "cosine stenosis, 40–80% DS\nLAD, LCx, RCA; 10/20 mm\n6 944 eligible instances\n150 in six FFR bands"),
    ("Segmentation error", "T1 missed side branch\nT2 vessel break\nT3 lesion +2.46 mm\nT4 taper ×0.930"),
    ("Boundary conditions", "A fixed (clean bed)\nB re-derived on\n   corrupted tree\nC one scaling fitted to\n   clean territory flows"),
    ("Reduced-order FFR", "leaky bed: 150\ndiscrete bed: 97\nsteady hyperaemia\nFFR 20 mm distal"),
    ("Outcomes", "$\\Delta$FFR vs clean model\nflip at FFR 0.80\nresidual < 10% and\n$|\\Delta$FFR$|$ > 0.05"),
]
w, gap, x0, y0, h = 14.6, 2.0, 1.0, 5.2, 13.5
for i, (head, body) in enumerate(stages):
    x = x0 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0,rounding_size=0.8", fc=FILL, ec=EDGE, lw=0.6))
    ax.text(x + w / 2, y0 + h - 1.6, head, ha="center", va="top", fontweight="bold", color=INK)
    ax.text(x + 0.9, y0 + h - 4.4, body, ha="left", va="top", color=INK, linespacing=1.35)
    if i < len(stages) - 1:
        ax.add_patch(FancyArrowPatch((x + w + 0.15, y0 + h / 2), (x + w + gap - 0.15, y0 + h / 2),
                                     arrowstyle="-|>", mutation_scale=7, color=INK, lw=0.7))
# 3D case-study lane under stages 3-6
xs, xe = x0 + 2 * (w + gap), x0 + 6 * (w + gap) - gap
ax.add_patch(FancyBboxPatch((xs, 0.6), xe - xs, 3.4, boxstyle="round,pad=0,rounding_size=0.8", fc="white", ec=ACC, lw=0.7))
ax.text((xs + xe) / 2, 2.3, "3D case study (one LAD lesion, 80% DS): baseline and T1 lumens solved in OpenFOAM under\n"
        "fixed resistances and prescribed territory flows, beside reduced-order twins",
        ha="center", va="center", color=INK, fontsize=5.3)
fig.savefig(sys.argv[1]); print("wrote", sys.argv[1])
