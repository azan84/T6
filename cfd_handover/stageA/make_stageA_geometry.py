#!/usr/bin/env python3
"""
make_stageA_geometry.py — analytic test geometries for Stage A of the CFD arm (CFD-ARM-SPEC v0.2 §8).
Needs only numpy. Run ON THE CFD MACHINE; nothing large is stored in Google Drive.

    python3 make_stageA_geometry.py [outdir] [--ncirc 64] [--dx 0.10]

Writes, in METRES, multi-solid ASCII STL (solids: inlet, outlet, wall — cfMesh and snappyHexMesh both read the solid
names as patches):
    pipe.stl                 straight pipe, r = 1.5 mm, x = 0 .. 100 mm
    sten00.stl .. sten80.stl tapering vessel 1.8 -> 0.9 mm over x = 0 .. 90 mm, straight extensions
                             x = -15 .. 0 (r = 1.8) and x = 90 .. 100 (r = 0.9); cosine lesion, 10 mm long,
                             centred at x = 31.5 mm, 0 / 50 / 70 / 80 % diameter stenosis
The radius law below is THE definition shared with the 0D benchmark (code/stageA_benchmark_0d.py imports it).
Probe planes (x, mm): stenosis cases  inlet -10 | proximal 20 | throat 31.5 | MEASUREMENT 56.5 | outlet 95
                      pipe            60 and 90 (fully developed; entrance length ~ 30 mm at Re ~ 170)
"""
import sys, argparse
import numpy as np

LESION_C, LESION_L = 31.5, 10.0          # mm
X_IN, X_OUT = -15.0, 100.0               # mm, including straight extensions
PROBES_STEN = dict(inlet=-10.0, proximal=20.0, throat=31.5, measurement=56.5, outlet=95.0)
PROBES_PIPE = dict(p60=60.0, p90=90.0)

def radius_sten(x_mm, ds_pct):
    """Radius (mm) of the tapering test vessel with a cosine lesion of ds_pct % diameter stenosis."""
    x = np.asarray(x_mm, float)
    r = np.where(x <= 0, 1.8, np.where(x >= 90, 0.9, 1.8 + (0.9 - 1.8) * x / 90.0))
    inl = np.abs(x - LESION_C) < LESION_L / 2
    w = np.where(inl, 0.5 * (1 + np.cos(np.pi * (x - LESION_C) / (LESION_L / 2))), 0.0)
    return r * (1 - ds_pct / 100.0 * w)

def radius_pipe(x_mm):
    return np.full_like(np.asarray(x_mm, float), 1.5)

def _tri(f, a, b, c):
    n = np.cross(b - a, c - a); n = n / (np.linalg.norm(n) + 1e-30)
    f.write(f" facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n  outer loop\n")
    for p in (a, b, c): f.write(f"   vertex {p[0]:.9e} {p[1]:.9e} {p[2]:.9e}\n")
    f.write("  endloop\n endfacet\n")

def write_stl(path, x_mm, r_mm, ncirc):
    th = np.linspace(0, 2 * np.pi, ncirc, endpoint=False)
    ring = lambda x, r: np.stack([np.full(ncirc, x), r * np.cos(th), r * np.sin(th)], 1) * 1e-3     # metres
    rings = [ring(x, r) for x, r in zip(x_mm, r_mm)]
    with open(path, "w") as f:
        f.write("solid wall\n")
        for A, B in zip(rings[:-1], rings[1:]):
            for k in range(ncirc):
                k2 = (k + 1) % ncirc
                _tri(f, A[k], B[k], B[k2]); _tri(f, A[k], B[k2], A[k2])       # outward normals
        f.write("endsolid wall\nsolid inlet\n")
        c = np.array([x_mm[0], 0, 0]) * 1e-3
        for k in range(ncirc): _tri(f, c, rings[0][(k + 1) % ncirc], rings[0][k])          # normal -x
        f.write("endsolid inlet\nsolid outlet\n")
        c = np.array([x_mm[-1], 0, 0]) * 1e-3
        for k in range(ncirc): _tri(f, c, rings[-1][k], rings[-1][(k + 1) % ncirc])        # normal +x
        f.write("endsolid outlet\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("outdir", nargs="?", default=".")
    ap.add_argument("--ncirc", type=int, default=64); ap.add_argument("--dx", type=float, default=0.10)
    a = ap.parse_args()
    import os; os.makedirs(a.outdir, exist_ok=True)
    xp = np.arange(0.0, 100.0 + 1e-9, a.dx)
    write_stl(os.path.join(a.outdir, "pipe.stl"), xp, radius_pipe(xp), a.ncirc)
    xs = np.arange(X_IN, X_OUT + 1e-9, a.dx)
    for ds in (0, 50, 70, 80):
        write_stl(os.path.join(a.outdir, f"sten{ds:02d}.stl"), xs, radius_sten(xs, ds), a.ncirc)
        print(f"sten{ds:02d}.stl  throat radius {radius_sten(LESION_C, ds):.4f} mm")
    print("wrote pipe.stl + 4 stenosis STLs (metres) to", os.path.abspath(a.outdir))
