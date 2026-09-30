"""Figure: the two steady states of the Stage A sten70 case on the same (smoke-test) mesh. Axial velocity on the y=0 and z=0 mid-planes, x = 20..80 mm.
usage: fig_two_states.py <out.png>   (reads /home/azan/paper6_t6_work/{smoke_cont (axisymmetric), bi_new_from_asym (deflected)}; both on the mesh of smoke_ref)"""
import sys, numpy as np, pyvista as pv, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
cases = [("smoke_cont", "axisymmetric jet: Q = 1.17825e-6 m$^3$/s, FFR$_{56.5}$ = 0.78248"), ("bi_new_from_asym", "wall-deflected jet: Q = 1.17390e-6 m$^3$/s, FFR$_{56.5}$ = 0.78397 (returned A5 value)")]
fig, ax = plt.subplots(4, 1, figsize=(10, 5.4), constrained_layout=True)
k = 0
for c, title in cases:
    r = pv.OpenFOAMReader(f"/home/azan/paper6_t6_work/{c}/case.foam"); r.set_active_time_value(r.time_values[-1]); m = r.read()["internalMesh"].cell_data_to_point_data()
    for normal, lab, j in (("z", "z = 0 plane (x-y)", 1), ("y", "y = 0 plane (x-z)", 2)):
        sl = m.slice(normal=normal, origin=(0, 0, 0)).triangulate(); p = sl.points; tri = sl.faces.reshape(-1, 4)[:, 1:]
        xs, ys = p[:, 0] * 1e3, p[:, j] * 1e3; keep = (xs > 20) & (xs < 80)
        T = Triangulation(xs, ys, tri); T.set_mask(~keep[tri].all(1))
        cs = ax[k].tricontourf(T, sl.point_data["U"][:, 0], levels=np.linspace(-0.4, 1.5, 39), cmap="RdBu_r", extend="both")
        ax[k].tricontour(T, sl.point_data["U"][:, 0], levels=[0.0], colors="k", linewidths=0.6)
        ax[k].axvline(56.5, color="0.2", ls="--", lw=0.8); ax[k].set_xlim(20, 80); ax[k].set_aspect("equal"); ax[k].set_ylabel(("y" if j == 1 else "z") + " (mm)")
        ax[k].set_title(f"({'abcd'[k]}) {title}; {lab}", fontsize=9, loc="left"); k += 1
ax[-1].set_xlabel("x (mm)  (throat at 30 mm; dashed: measurement station 56.5 mm; black line: $U_x$ = 0)")
fig.colorbar(cs, ax=ax, shrink=0.8, label="$U_x$ (m/s)")
fig.savefig(sys.argv[1], dpi=200); print("wrote", sys.argv[1])
