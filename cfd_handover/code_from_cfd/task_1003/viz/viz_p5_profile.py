"""P5 result graph: section-mean p/P_aorta along the lesion vessel at the package probes (one case) with the throat and measurement probe marked.
usage: viz_p5_profile.py <out.png> <title> <M1_probes.csv>"""
import sys, csv, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, title, f = sys.argv[1:4]; R = [r for r in csv.DictReader(open(f)) if r["p_over_Paorta"] not in ("", "nan") and r["s_from_lesion_mm"] not in ("", "nan")]
s = np.array([float(r["s_from_lesion_mm"]) for r in R]); p = np.array([float(r["p_over_Paorta"]) for r in R]); o = np.argsort(s)
fig, ax = plt.subplots(figsize=(8.5, 4.2), constrained_layout=True); ax.plot(s[o], p[o], "ko-", ms=4, lw=1.2)
for r in R:
    if r["kind"] in ("throat", "measurement"): ax.plot(float(r["s_from_lesion_mm"]), float(r["p_over_Paorta"]), "o", ms=9, mfc="none", mec="r" if r["kind"] == "throat" else "c", mew=1.8); ax.annotate(r["kind"] + " " + r["probe_id"], (float(r["s_from_lesion_mm"]), float(r["p_over_Paorta"])), textcoords="offset points", xytext=(6, 6), fontsize=8)
ax.set_xlabel("arc from the lesion centre (mm)"); ax.set_ylabel("section-mean p / P_aorta"); ax.grid(alpha=0.3); ax.set_title(title, fontsize=9, loc="left")
fig.savefig(out, dpi=170); print("wrote", out)
