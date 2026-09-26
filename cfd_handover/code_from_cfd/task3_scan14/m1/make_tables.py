"""LaTeX tables of the scan-14 M1 results from m1/out_returns (M1_results.csv, M1_outlets_<case>_<mode>.csv, m1/cases/<case>_roundtrip/roundtrip_result.csv). Writes m1/tables_m1.tex (three tables: solves, resistance-mode outlet flows vs bc_C, round trips). Missing cases are skipped."""
import csv, os, sys
P = os.path.dirname(os.path.abspath(__file__)); O = f"{P}/out_returns"
def ex(s): return s.replace("_", "\\_")
res = {(r["case"], r["bc_mode"]): r for r in csv.DictReader(open(f"{O}/M1_results.csv"))}
labels = {"clean_nolesion": "clean", "baseline": "baseline (80\\%DS)", "T1_missed_branch": "T1 (lesion; branch deleted)"}
out = []
out.append("\\begin{table}[H]\n\\centering\n\\caption{Scan-14 Gate-M1 solves (16 ranks each, one at a time, fixed budget 3000 iterations, strict verdict as stated; the throat Reynolds number is the section flux at the throat probe, at the would-be throat station for the clean tree).}\n\\label{tab:m1-solves}\n\\small\n\\resizebox{\\textwidth}{!}{\\begin{tabular}{llrrrrrrr}\n\\toprule\ncase & BC mode & cells & verdict & inflow (mL/s) & throat $Re$ & wall (h) & RAM (GB) & round trip max error (\\%) \\\\\n\\midrule")
for c in ("clean_nolesion", "baseline", "T1_missed_branch"):
    for (cc, m), r in res.items():
        if cc != c: continue
        rt = r.get("roundtrip_max_err_pct", "")
        out.append(f"{labels[c]} & {m.replace('prescribed-flow','prescribed')} & {int(float(r['n_cells'])):,}".replace(",", "{,}") + f" & {r['converged'].lower()} & {float(r['Q_inlet_mls']):.4f} & {float(r['Re_throat']):.0f} & {float(r['wallclock_min'])/60:.2f} & {float(r['peak_ram_gb']):.1f} & {('%.4f' % float(rt)) if rt else '--'} \\\\")
out.append("\\bottomrule\n\\end{tabular}}\n\\end{table}\n")
out.append("\\begin{table}[H]\n\\centering\n\\caption{Resistance mode with the package resistances (\\texttt{bc\\_A}): 3D outlet flow against the package target flow (\\texttt{bc\\_C}); a positive deviation means that the 3D tree delivers more than the target.}\n\\label{tab:m1-flows}\n\\small\n\\begin{tabular}{llrrr}\n\\toprule\ncase & outlet & $Q_\\text{target}$ (mL/s) & $Q_\\text{3D}$ (mL/s) & deviation (\\%) \\\\\n\\midrule")
for c in ("clean_nolesion", "baseline", "T1_missed_branch"):
    f = f"{O}/M1_outlets_{c}_resistance.csv"
    if not os.path.exists(f): continue
    for r in sorted(csv.DictReader(open(f)), key=lambda r: int(r["outlet_id"].split("_")[1])):
        out.append(f"{labels[c].split(' (')[0]} & {ex(r['outlet_id'])} & {float(r['Q_target_bcC_mls']):.4f} & {float(r['Q_mls']):.4f} & {float(r['Q_over_target_minus_1_pct']):+.1f} \\\\")
out.append("\\bottomrule\n\\end{tabular}\n\\end{table}\n")
rows = []
for c in ("baseline", "T1_missed_branch", "clean_nolesion"):
    f = f"{P}/cases/{c}_roundtrip/roundtrip_result.csv"
    if os.path.exists(f):
        for r in csv.DictReader(open(f)): rows.append((c, r))
if rows:
    out.append("\\begin{table}[H]\n\\centering\n\\caption{Prescribed-flow round trip on scan 14: every outlet flow prescribed at once (\\texttt{bc\\_C}), $R_i=(\\bar p_i-P_v)/Q_i$ derived, re-imposed in resistance mode; error of the re-solved flow against the prescribed one (criterion 0.5\\%), and derived resistance against the package resistance (\\texttt{bc\\_A}).}\n\\label{tab:m1-roundtrip}\n\\small\n\\begin{tabular}{llrrr}\n\\toprule\ncase & outlet & $Q$ (mL/s) & round-trip error (\\%) & $R_\\text{derived}/R_\\text{bc\\_A}-1$ (\\%) \\\\\n\\midrule")
    for c, r in rows:
        out.append(f"{labels[c].split(' (')[0]} & {ex(r['outlet'])} & {float(r['Q_target_mls']):.4f} & {float(r['err_pct']):+.4f} & {float(r['R_derived_over_reference_pct']):+.1f} \\\\")
    out.append("\\bottomrule\n\\end{tabular}\n\\end{table}\n")
open(f"{P}/tables_m1.tex", "w").write("\n".join(out)); print("wrote tables_m1.tex", len(out), "blocks")
