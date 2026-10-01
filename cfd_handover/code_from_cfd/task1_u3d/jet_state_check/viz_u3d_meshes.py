"""U3D mesh close-up (rebuilt 2026-10-02; the original viz_u3d_meshes.py was lost with the scratch directory): cell edges of the mid-plane z = 0 around the sten70 throat
(x = 29.2..33.8 mm, y = 0..1.0 mm) for the rebuilt U3D levels given on the command line (polyMesh read with pyvista; meshes rebuilt from the deposited code, same cell counts as the returned levels).
usage: viz_u3d_meshes.py <out.png> <level>=<case_dir> [...]"""
import sys, numpy as np, pyvista as pv, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
out, pairs = sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]]
fig, axs = plt.subplots(len(pairs), 1, figsize=(10, 2.4 * len(pairs)), constrained_layout=True, squeeze=False)
for ax, (lev, case) in zip(axs[:, 0], pairs):
    open(f"{case}/case.foam", "a").close(); r = pv.OpenFOAMReader(f"{case}/case.foam"); r.set_active_time_value(r.time_values[0])
    m = r.read()["internalMesh"]; box = m.clip_box((0.0288, 0.0342, -1e-5, 0.0011, -0.002, 0.002), invert=False)
    sl = box.slice(normal="z", origin=(0, 0, 0)); e = sl.extract_all_edges(); p = e.points * 1e3; ln = e.lines.reshape(-1, 3)[:, 1:]
    segs = p[ln][:, :, :2]; keep = (segs[:, :, 0].min(1) > 29.2) & (segs[:, :, 0].max(1) < 33.8) & (segs[:, :, 1].min(1) >= -1e-6) & (segs[:, :, 1].max(1) < 1.0)
    ax.add_collection(LineCollection(segs[keep], linewidths=0.25, colors="0.15"))
    x = np.linspace(28, 36, 400); ax.set_xlim(29.2, 33.8); ax.set_ylim(0, 1.0); ax.set_aspect("equal")
    ax.set_title(f"{lev}: {m.n_cells:,} cells; mid-plane z = 0, throat at x = 31.5 mm (throat radius 0.4455 mm)", fontsize=9, loc="left"); ax.set_ylabel("y (mm)")
axs[-1, 0].set_xlabel("x (mm)"); fig.savefig(out, dpi=220); print("wrote", out)
