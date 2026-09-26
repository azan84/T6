"""Fine sten70 STL for the U3D study (u3d_design.md section 2): the analytic radius law of make_stageA_geometry.py (imported, not copied), the generator's own write_stl (outward normals, solids wall/inlet/outlet),
192 circumferential segments, axial ring spacing 0.02 mm for x in [20, 43] mm and 0.2 mm elsewhere. Writes u3d/sten70_fine.stl (metres). Gates: analytic vs STL throat area, ring count."""
import sys, os, importlib.util
import numpy as np
G = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/stageA/make_stageA_geometry.py"
spec = importlib.util.spec_from_file_location("stageA_geo", G); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
NCIRC = 192
def grid():
    a = np.linspace(g.X_IN, 20.0, int(round((20.0 - g.X_IN) / 0.2)) + 1)
    b = np.linspace(20.0, 43.0, int(round((43.0 - 20.0) / 0.02)) + 1)
    c = np.linspace(43.0, g.X_OUT, int(round((g.X_OUT - 43.0) / 0.2)) + 1)
    return np.concatenate([a[:-1], b[:-1], c])
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "sten70_fine.stl")
    x = grid(); r = g.radius_sten(x, 70)
    assert abs(x[0] - g.X_IN) < 1e-9 and abs(x[-1] - g.X_OUT) < 1e-9 and (np.diff(x) > 0).all()
    g.write_stl(out, x, r, NCIRC)
    k = int(np.argmin(np.abs(x - g.LESION_C)))
    a_poly = 0.5 * NCIRC * r[k] ** 2 * np.sin(2 * np.pi / NCIRC); a_ana = np.pi * (float(g.radius_sten(g.LESION_C, 70))) ** 2
    print(f"rings {len(x)}, throat ring at x={x[k]:.4f} mm, r={r[k]:.5f} mm; polygon area {a_poly:.6f} vs analytic {a_ana:.6f} mm2 ({100*(a_poly/a_ana-1):+.4f} %); wrote {out} ({os.path.getsize(out)/1e6:.0f} MB)")
    assert abs(a_poly / a_ana - 1) < 5e-4
