import sys, json
from pathlib import Path
import numpy as np, pandas as pd, pyvista as pv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

P6, ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(P6 / "code"))
from ingest_cfd_radius import rebuild
from zerod_ffr import R_FLOOR, P_AORTA, P_VEN

PK = P6 / "cfd_handover/packages/M1"; RET = P6 / "cfd_handover/returns/2026-09-26"

def solve_resistance(tw, R_by):
    w = np.zeros_like(tw.w)
    for v, R in R_by.items(): w[v] = 1.0 / R
    tw.w = w
    P, Q, _ = tw._solve(1.0, P_AORTA, P_VEN, healthy=False); assert tw.info["converged"]
    return P

def solve_prescribed(tw, Q_by):
    n = len(tw.r); Q = np.zeros(n)
    for v, q in Q_by.items(): Q[v] = q
    for v in sorted(np.where(tw.active)[0], key=lambda v: -tw.arc[v]):
        if v != 0 and tw.parent[v] >= 0 and tw.children[v]: Q[v] = sum(Q[c] for c in tw.children[v])
    P = np.full(n, np.nan); P[0] = P_AORTA
    for v in sorted(np.where(tw.active)[0], key=lambda v: tw.arc[v]):
        if v == 0: continue
        p = tw.parent[v]; r_mid = max(0.5 * (tw.r[v] + tw.r[p]), R_FLOOR)
        P[v] = P[p] - Q[v] * (8 * tw.mu * tw.ds[v] / (np.pi * r_mid ** 4) + tw.K[v] * abs(Q[v]))
    return P

data = {}
for case in ("baseline", "T1_missed_branch"):
    pkg = PK / f"14_left_LAD_prox_20mm_80ds__{case}__real"
    ol = pd.read_csv(pkg / "outlets.csv"); node_of = dict(zip(ol.outlet_id, ol.tree_node))
    bcA = pd.read_csv(pkg / "bc_A.csv"); bcC = pd.read_csv(pkg / "bc_C_flows.csv")
    R_by = {int(node_of[o]): R for o, R, m in zip(bcA.outlet_id, bcA.R_SI, bcA["mode"]) if m == "resistance"}
    Q_by = {int(node_of[o]): q for o, q, m in zip(bcC.outlet_id, bcC.Q_target_m3s, bcC["mode"]) if m == "prescribed"}
    tw, *_ = rebuild(ROOT, pkg, RET / f"as_meshed_radius_{case}.csv")
    for mode in ("resistance", "prescribed"):
        pr = pd.read_csv(RET / f"M1_probes_{case}_{mode}.csv")
        pr = pr[pr.kind.isin(["grid", "lesion_prox", "throat", "lesion_dist", "measurement"]) & (pr.section_ok == 1)]
        pr = pr.sort_values("s_from_lesion_mm")
        P = solve_resistance(tw, R_by) if mode == "resistance" else solve_prescribed(tw, Q_by)
        pr = pr.assign(p0d=P[pr.tree_node.astype(int).values] / P_AORTA)
        meas = pr[pr.kind == "measurement"].iloc[0]
        data[(case, mode)] = (pr, meas)

plt.rcParams.update({"font.family": "serif", "font.size": 7, "axes.linewidth": 0.5, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False, "pdf.fonttype": 42})
from PIL import Image

src = Image.open(P6 / "drafts/stageA_validation/figures/img_m1_wall_pressure.png"); k = src.width / 2000
trees = src.crop((0, int(235 * k), int(1340 * k), int(830 * k)))
bar = src.crop((int(585 * k), int(985 * k), int(1420 * k), int(1052 * k)))
img = trees
throat = src.crop((int(1395 * k), int(100 * k), int(1935 * k), int(950 * k)))
COL = {"baseline": "#2a78d6", "T1_missed_branch": "#eb6834"}
LAB = {"baseline": "Lesion", "T1_missed_branch": "Lesion and missed branch"}
fig = plt.figure(figsize=(7.16, 2.75))

ax0 = fig.add_axes((0.0, 0.2, 0.555, 0.72)); ax0.imshow(img); ax0.axis("off")
W, H = trees.width, trees.height
for x, t in ((0.15, "(a) No lesion"), (0.48, "(b) Lesion"), (0.81, "(c) Lesion + missed branch")):
    ax0.text(x * W, -15, t, ha="center", va="bottom", fontsize=7)
axt = fig.add_axes((0.555, 0.24, 0.075, 0.62)); axt.imshow(throat); axt.axis("off")
axt.text(throat.width / 2, -15, "(d) Lesion", ha="center", va="bottom", fontsize=7)
import matplotlib as mpl
cax = fig.add_axes((0.07, 0.12, 0.5, 0.03))
cb = fig.colorbar(mpl.cm.ScalarMappable(mpl.colors.Normalize(0.86, 1.0), "turbo_r"), cax=cax, orientation="horizontal")
cb.set_label("Wall pressure / aortic pressure (fixed outlet resistances)", fontsize=6.5); cb.ax.tick_params(labelsize=6)
cb.outline.set_linewidth(0.4)
axe = fig.add_axes((0.72, 0.57, 0.27, 0.3)); axf = fig.add_axes((0.72, 0.13, 0.27, 0.3), sharex=axe)
for ax, mode, title in zip((axe, axf), ("resistance", "prescribed"), ("(e) Fixed resistances", "(f) Prescribed flows")):
    for case, mk in (("baseline", "o"), ("T1_missed_branch", "^")):
        pr, meas = data[(case, mode)]
        ax.plot(pr.s_from_lesion_mm, pr.p0d, "-", color=COL[case], lw=1.0)
        ax.scatter(pr.s_from_lesion_mm, pr.p_over_Paorta, s=7, marker=mk, facecolor=COL[case], edgecolor="white",
                   linewidth=0.3, zorder=3, label=LAB[case])
    ax.axvspan(-10, 10, color="#8a8a85", alpha=0.12, lw=0)
    ax.axvline(data[("baseline", mode)][1].s_from_lesion_mm, color="#8a8a85", lw=0.5, ls="--")
    ax.set_title(title, fontsize=7, pad=2); ax.set_ylim(0.84, 1.01)
    ax.grid(axis="y", color="#e6e6e3", lw=0.4); ax.set_ylabel("$p/P_\\mathrm{a}$", labelpad=1)
plt.setp(axe.get_xticklabels(), visible=False)
axf.set_xlabel("Distance from lesion (mm)")
h, l = axe.get_legend_handles_labels()
fig.legend(h, l, loc="upper center", ncol=2, bbox_to_anchor=(0.845, 1.0), fontsize=6.3, handletextpad=0.3)
fig.savefig(OUT, dpi=300); print("wrote", OUT)
for k, (pr, meas) in data.items():
    print(k, f"3D {meas.p_over_Paorta:.3f}  0D twin {meas.p0d:.3f}  s={meas.s_from_lesion_mm:.1f} mm  n={len(pr)}")
