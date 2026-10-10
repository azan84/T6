import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

sys.path.insert(0, str(Path(__file__).parent))
from zerod_ffr import Tree
from severity_sweep import load, plan, insert
from error_types import t1_missed_branch, t2_truncation, t4_taper, T3_LENGTH_DELTA

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
P6 = Path(__file__).parent.parent
row = pd.read_csv(P6 / "protocol/COHORT-FROZEN-2026-09-18.csv").query("scan == 14 and side == 'left' and vessel == 'LAD'").iloc[0]
t = load(ROOT, 14, "left", "leaky"); t.ffr("murray", 1.0)
slots, _ = plan(t, "left", t.last["ffr"].copy())
sl = next(s for s in slots if s["vessel"] == "LAD" and s["loc"] == row["loc"] and abs(s["L"] * 1e3 - row.L_mm) < 1e-6)
path, s_arc, c, L = sl["path"], sl["s"], sl["c"], sl["L"]; ds = row.ds_pct / 100
r_les, _ = insert(t, path, s_arc, c, L, ds)

X = t.xyz * 1e3; mu = X.mean(0); V = np.array([[1.0, 0, 0], [0, 0, 1.0], [0, 1.0, 0]])
proj = lambda P: (np.asarray(P) * 1e3 - mu) @ V[:2].T if np.asarray(P).max() < 1 else (np.asarray(P) - mu) @ V[:2].T

def seg_lines(segs, rscale=1.0):
    lines, widths = [], []
    for s in segs:
        p = (s.pts * 1e3 - mu) @ V[:2].T
        for i in range(len(p) - 1):
            lines.append(p[i:i + 2]); widths.append(rscale * 1e3 * 0.5 * (s.r[i] + s.r[i + 1]))
    return lines, np.array(widths)

def draw(ax, segs, color, lw_k=2.6, alpha=1.0, z=1, ls="solid"):
    lines, w = seg_lines(segs)
    ax.add_collection(LineCollection(lines, linewidths=w * lw_k, colors=color, alpha=alpha, zorder=z,
                                     linestyles=ls, capstyle="round"))

GREY, HOST, ERR, INK = "#b9b9b4", "#2a78d6", "#d0412a", "#2b2b2b"
plt.rcParams.update({"font.family": "serif", "font.size": 7, "pdf.fonttype": 42})
fig = plt.figure(figsize=(7.16, 1.8))
gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.35], wspace=0.08, left=0.005, right=0.99, top=0.87, bottom=0.21)
segs = list(t.segments)
host_sids = set(int(t.seg[v]) for v in path)
lesion_xy = proj(t.xyz[path[np.argmin(np.abs(s_arc - c))]])
meas_xy = proj(t.xyz[path[min(int(np.searchsorted(s_arc, c + L / 2 + 20e-3)), len(path) - 1)]])

def base(ax, title):
    ax.set_title(title, fontsize=7); ax.set_aspect("equal"); ax.axis("off")

ax = fig.add_subplot(gs[0]); base(ax, "(a) Tree with inserted lesion")
draw(ax, [s for s in segs if s.sid not in host_sids], GREY)
draw(ax, [s for s in segs if s.sid in host_sids], HOST, z=2)
ax.scatter(*lesion_xy, s=60, facecolor="none", edgecolor=ERR, linewidth=1.0, zorder=4)
ax.annotate("lesion", lesion_xy, xytext=(10, 6), textcoords="offset points", fontsize=6.5, color=ERR)
ax.scatter(*meas_xy, s=14, marker="x", color=INK, zorder=5, linewidth=0.8)
ax.annotate("measurement", meas_xy, xytext=(6, -10), textcoords="offset points", fontsize=6.5, color=INK)
ax.autoscale()

segs1, info1 = t1_missed_branch(segs, t, path, s_arc, c, L)
kept1 = set(s.sid for s in segs1)
ax = fig.add_subplot(gs[1]); base(ax, "(b) T1 missed branch")
draw(ax, segs1, GREY)
draw(ax, [s for s in segs if s.sid not in kept1], ERR, z=3)
ax.autoscale()

segs2, info2 = t2_truncation(segs, t, path, s_arc, c, L)
ax = fig.add_subplot(gs[2]); base(ax, "(c) T2 vessel break")
draw(ax, segs, ERR, z=1)
draw(ax, segs2, GREY, z=2)
ax.autoscale()

ax = fig.add_subplot(gs[3])
r3, _ = insert(t, path, s_arc, c, L + T3_LENGTH_DELTA, ds)
segs4, _ = t4_taper(segs, t, path, s_arc, c, L)
t4 = Tree(segs4, "t4", bed="leaky", trunc_ref=t)
r4, _ = insert(t4, path, s_arc, c, L, ds)
x = (s_arc - c) * 1e3; win = (x > -25) & (x < 45)
ax.plot(x[win], t.r[path][win] * 1e3, color=GREY, lw=1.0, label="Segmented (no lesion)")
ax.plot(x[win], r_les[path][win] * 1e3, color=HOST, lw=1.4, label="With lesion")
ax.plot(x[win], r3[path][win] * 1e3, color=ERR, lw=1.0, ls="--", label="T3 lesion +2.46 mm")
ax.plot(x[win], r4[path][win] * 1e3, color="#1baf7a", lw=1.0, ls=":", label="T4 taper $\\times$0.93")
ax.set_xlabel("Distance from lesion center (mm)"); ax.set_ylabel("Radius (mm)", labelpad=1)
ax.set_title("(d) T3 lesion length and T4 taper", fontsize=7)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.legend(loc="upper right", fontsize=5.8, frameon=False, handlelength=2.2)
fig.savefig(OUT); print("wrote", OUT, info1, info2)
