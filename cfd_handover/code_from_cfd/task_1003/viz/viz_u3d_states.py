"""Task B figure: axial velocity on the two mid-planes (z = 0 and y = 0) of the re-run U3D levels, x = 25..75 mm (throat at 30 mm), with the FFR of the re-run against the original.
usage: viz_u3d_states.py <out.png> <level>=<case_dir>=<FFR_rerun>=<FFR_original> [...]"""
import sys, numpy as np, pyvista as pv, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
out = sys.argv[1]; L = [a.split("=") for a in sys.argv[2:]]
fig, ax = plt.subplots(2 * len(L), 1, figsize=(10, 2.2 * len(L) * 1.25), constrained_layout=True)
k = 0
for lev, case, fr, fo in L:
    open(f"{case}/case.foam", "a").close(); r = pv.OpenFOAMReader(f"{case}/case.foam"); r.set_active_time_value(r.time_values[-1]); m = r.read()["internalMesh"].cell_data_to_point_data()
    for normal, lab, j in (("z", "z = 0 plane", 1), ("y", "y = 0 plane", 2)):
        sl = m.slice(normal=normal, origin=(0, 0, 0)).triangulate(); p = sl.points; tri = sl.faces.reshape(-1, 4)[:, 1:]; xs, ys = p[:, 0] * 1e3, p[:, j] * 1e3
        keep = (xs > 25) & (xs < 75); T = Triangulation(xs, ys, tri); T.set_mask(~keep[tri].all(1))
        cs = ax[k].tricontourf(T, sl.point_data["U"][:, 0], levels=np.linspace(-0.4, 1.5, 39), cmap="RdBu_r", extend="both"); ax[k].tricontour(T, sl.point_data["U"][:, 0], levels=[0.0], colors="k", linewidths=0.5)
        ax[k].set_xlim(25, 75); ax[k].set_aspect("equal"); ax[k].set_ylabel(("y" if j == 1 else "z") + " (mm)", fontsize=8); ax[k].axvline(56.5, color="0.3", ls="--", lw=0.7)
        ax[k].set_title(f"{lev}: re-run FFR {float(fr):.6f} (original {float(fo):.6f}); {lab}", fontsize=8, loc="left"); k += 1
ax[-1].set_xlabel("x (mm); dashed: measurement station 56.5 mm; black: U_x = 0"); fig.colorbar(cs, ax=ax, shrink=0.6, label="U_x (m/s)")
fig.savefig(out, dpi=170); print("wrote", out)
