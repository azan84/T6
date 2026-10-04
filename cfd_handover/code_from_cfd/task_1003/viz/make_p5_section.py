"""Regenerate the P5 subsection of the report (between %%P5_BEGIN and %%P5_END) from returns/2026-10-03/P5/<scan>/M1_results.csv and copy/quantize the figures.
usage: make_p5_section.py   (idempotent; run after every finished P5 case)"""
import csv, os, re, json, shutil
from PIL import Image
D = "/mnt/e/Paper6-T6/Paper6-T6"; T = f"{D}/drafts/stageA_validation/STAGE-A-VALIDATION.tex"; F = f"{D}/drafts/stageA_validation/figures"; R = f"{D}/cfd_handover/returns/2026-10-03/P5"; V = "/home/azan/paper6_t6_work/viz/out"
CASES = [("138", "LAD", "20", "70"), ("69", "LCx", "20", "65"), ("473", "LCx", "20", "60"), ("272", "RCA", "10", "65"), ("139", "RCA", "10", "70")]
def esc(x): return x.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")
rows = []; blocks = []
for s, ves, L, ds in CASES:
    f = f"{R}/{s}/M1_results.csv"
    if not os.path.exists(f): rows.append(f"{s} & {ves} & {L} / {ds} & \\multicolumn{{5}}{{l}}{{queued}} \\\\"); continue
    r = list(csv.DictReader(open(f)))[0]; ps = json.load(open(f"{R}/{s}/post_summary_{s}_resistance.json"))
    pr = {x["probe_id"]: x for x in csv.DictReader(open(f"{R}/{s}/M1_probes_{s}_resistance.csv"))}; mp = ps.get("measurement_probe_used"); pm = pr.get(mp, {}); pv = float(pm.get("p_over_Paorta", "nan")) if pm else float("nan")
    flags = r.get("flags", "").replace(";", ", ")
    rows.append(f"{s} & {ves} & {L} / {ds} & {int(float(r['n_cells'])):,}".replace(",", "{,}") + f" & {r['converged'].lower()} & {float(r['Re_throat']):.0f} & {pv:.5f} ({esc(str(mp))}) & {esc(flags)} \\\\")
    for nm in ("cpr_cfd", "wall"):
        src = f"{V}/{s}_{nm}.png"
        if os.path.exists(src):
            im = Image.open(src).convert("RGB"); im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE).save(f"{F}/cfd_p5_{s}_{nm}.png", optimize=True)
    cap_c = f"P5 scan {s} ({ves}, {L}\\,mm, {ds}\\%DS): curved-planar reformation of the unmodified lumen label (white) in two orthogonal planes with the CFD speed $|U|$ in the CFD domain (the synthetic stenosis exists only in the CFD surface), and $p/P_\\text{{aorta}}$ on the axis (bottom); red dotted: throat, cyan dashed: measurement probe."
    cap_w = f"P5 scan {s}: wall pressure $p/P_\\text{{aorta}}$ of the tree in three views and the 6\\,mm around the throat."
    blocks.append(f"\\begin{{figure}}[H]\n\\centering\n\\includegraphics[width=\\textwidth]{{figures/cfd_p5_{s}_cpr_cfd.png}}\n\\caption[P5 scan {s}: segmentation reformation with the CFD speed]{{{cap_c}}}\n\\end{{figure}}\n\\begin{{figure}}[H]\n\\centering\n\\includegraphics[width=\\textwidth]{{figures/cfd_p5_{s}_wall.png}}\n\\caption[P5 scan {s}: wall pressure]{{{cap_w}}}\n\\end{{figure}}\n")
sec = r"""%%P5_BEGIN
\subsection{Task P5 of the 2026-10-03 work order: five-case baseline pilot (results so far)}
\label{sec:p5}
\textbf{Design.} Five new cohort baselines (scans 138, 69, 473, 272, 139; selected by the analysis side by a fixed rule), baseline geometry only, one resistance-mode solve each with the production recipe (25\,$\mu$m throat zone, 4 boundary layers, bounded probe monitors of Task~C, 3000 iterations, fields kept), built by the generalised pipeline (\texttt{code\_\allowbreak{}from\_\allowbreak{}cfd/\allowbreak{}task\_\allowbreak{}1003/\allowbreak{}p5\_\allowbreak{}builders}; its regression on scan 14 reproduces the STL byte for byte and the mesh cell count). Gates are reported, not repaired: a case that fails a gate is solved and returned flagged. The solves ran concurrently with other jobs (up to 32 MPI ranks on the 16 physical cores, at the study lead's request), so the wall-clock columns of the returns are contended. No 0D prediction is available or used for these cohort scans; the 3D values below are for the analysis side to compare.

\begin{table}[H]
\centering
\caption{\label{tab:p5}P5 cases: lesion vessel, length / diameter stenosis (mm / \%), cells, convergence verdict, throat Reynolds number, $p/P_\text{aorta}$ at the measurement probe used, and the machine-readable gate flags (D2: relative throat gate; D3/D4: strict \texttt{checkMesh} within 2\,mm of the throat or the measurement probe).}
\small
\resizebox{\textwidth}{!}{\begin{tabular}{llrrlrll}
\toprule
scan & vessel & L / DS & cells & verdict & Re$_\text{throat}$ & $p/P_\text{aorta}$ at measurement & flags \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}}
\end{table}

""" + "\n".join(blocks) + "%%P5_END\n"
s = open(T).read()
if "%%P5_BEGIN" in s: a = s.index("%%P5_BEGIN"); b = s.index("%%P5_END") + len("%%P5_END\n"); s = s[:a] + sec + s[b:]
else:
    anchor = "\\subsection{Item 5: RCR outlet BC verification --- \\PASS{}}"; assert s.count(anchor) == 1; s = s.replace(anchor, sec + "\n" + anchor)
open(T, "w").write(s); print("P5 section regenerated:", len(rows), "rows,", len(blocks), "case blocks")
