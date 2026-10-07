"""demand_table.py — Supplement section on hyperaemic-demand sensitivity (k x 0.7 / 1.0 / 1.3) from three analysis
folders. usage: demand_table.py <out tex>"""
import sys
from pathlib import Path
import pandas as pd
R = Path(__file__).parent.parent / "results"
D = {"0.7": R / "analysis-ablation-demand0.7-2026-10-07", "1.0": R / "analysis-ablation-2026-10-07",
     "1.3": R / "analysis-ablation-demand1.3-2026-10-07"}
def pc(x):  # "45/137 (32.8%, 25.5-41.1)" -> "33 (26--41)"
    v, ci = x.split("(")[1].rstrip(")").split(",")
    lo, hi = ci.strip().split("-")
    return f"{float(v.rstrip('%')):.0f} ({float(lo):.0f}--{float(hi):.0f})"
lines = []
for bed in ("discrete", "leaky"):
    for s, d in D.items():
        h = pd.read_csv(d / "H1_topo_vs_calibre.csv").set_index(["bed", "protocol"])
        p = pd.read_csv(d / "P2_absorption.csv")
        p = p[(p.threshold == 0.10) & (p.bed == bed) & (p.error_type == "TOPOLOGICAL")].set_index("protocol")
        b = pd.read_csv(d / "H6_branch_loss.csv").set_index("bed").loc[bed]
        c = p.loc["C_flowmatched"]
        lines.append(f"{bed.capitalize() if s == '0.7' else ''} & {s} & {pc(h.loc[(bed,'A_fixed')].topo)} & "
                     f"{pc(h.loc[(bed,'A_fixed')].calibre)} & {pc(h.loc[(bed,'B_rederived')].topo)} & "
                     f"{pc(h.loc[(bed,'C_flowmatched')].topo)} & {c.pct:.0f} ({c.lo:.0f}--{c.hi:.0f}) & "
                     f"{b.A_median_dFFR:.3f} / {b.C_median_dFFR:.3f} \\\\")
tex = r"""The demand constant $k$ was scaled by 0.7 and 1.3 and the full ablation was repeated with the same frozen cohort
(Table~\ref{tab:demand}). The ordering of topological against caliber errors under fixed boundary conditions, and of
Protocols B and C against Protocol A for the topological errors, was unchanged at both levels in both beds. The taper,
which flipped fewer decisions under Protocol C than under Protocol A at the primary demand, flipped one and two more
at 1.3 times the demand (7 against 6 of 97; 11 against 9 of 150). The magnitudes changed with demand, which moves the
clean FFR of every instance (leaky-bed median 0.869, 0.801 and 0.741 at 0.7, 1.0 and 1.3 times the demand) and
therefore the number of instances near the threshold, as well as the pressure loss across the lesion. The proportion
of tuned topological-error models that pass the perfusion check while materially wrong fell to 3\% in the leaky bed
at 0.7 times the demand, comparable with the simulated floor for correct anatomy (3.9\% at the primary demand); in
the discrete bed it remained between 12\% and 25\%.
\begin{table}[!h]
\caption{Sensitivity to Hyperemic Demand}\label{tab:demand}
\centering\small
\begin{tabular}{@{}llcccccc@{}}
\toprule
Bed & Demand scale & \multicolumn{2}{c}{Flip, \% (Protocol A)} & \multicolumn{2}{c}{Topological flip, \%} &
Passes and wrong, \% & Missed-branch $\Delta$FFR\\
\cmidrule(lr){3-4}\cmidrule(lr){5-6}
 & & Topological & Caliber & B & C & (C, topological) & median, A / C\\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}
\\[3pt]
\parbox{0.9\textwidth}{\footnotesize Demand scale 1.0 is the primary analysis ($k = 562$~s$^{-1}$). Percentages with Wilson 95\%
intervals in parentheses. Missed-branch $\Delta$FFR is over the instances in which Protocol C was defined.}
\end{table}
"""
Path(sys.argv[1]).write_text(tex); print("\n".join(lines))
