"""Jet symmetry diagnostic for the Stage A sten70 cases: flux-weighted centroid offset of the axial velocity from the vessel axis in slabs downstream of the throat (x_throat = 30 mm).
usage: jet_offset.py <case_dir> [...]   (needs the reconstructed latest time; pyvista)"""
import sys, os, numpy as np, pyvista as pv
for c in sys.argv[1:]:
    f = os.path.join(c, "case.foam"); open(f, "a").close()
    r = pv.OpenFOAMReader(f); r.set_active_time_value(r.time_values[-1]); m = r.read()["internalMesh"]
    cc = m.cell_centers().points; U = m.cell_data["U"]; V = m.compute_cell_sizes().cell_data["Volume"]
    out = []
    for x0 in (0.030, 0.035, 0.040, 0.045, 0.050, 0.0565, 0.065, 0.080):
        s = np.abs(cc[:, 0] - x0) < 0.0004; w = V[s] * np.abs(U[s, 0])
        cy = (w * cc[s, 1]).sum() / w.sum(); cz = (w * cc[s, 2]).sum() / w.sum()
        out.append("x=%.1f: %.1f um (umin %.3f)" % (x0 * 1e3, 1e6 * np.hypot(cy, cz), U[s, 0].min()))
    print(os.path.basename(os.path.abspath(c)), "t=%g cells=%d |" % (r.time_values[-1], m.n_cells), "; ".join(out))
