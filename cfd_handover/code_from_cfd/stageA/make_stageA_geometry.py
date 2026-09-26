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
Probe planes (x, mm): stenosis cases  inlet -10 | proximal 20 | throat 31.5 | MEASUREMENT 56.5 | x95 95
                      (x95 is an internal probe, NOT the outlet BC patch, which is 5 mm further
                      downstream at X_OUT = 100 - see the note by PROBES_STEN below)
                      pipe            60 and 90 (fully developed; entrance length ~ 30 mm at Re ~ 170)
"""
import sys, argparse
import numpy as np

LESION_C, LESION_L = 31.5, 10.0          # mm
X_IN, X_OUT = -15.0, 100.0               # mm, including straight extensions
# NOTE (2026-09-18 audit): "x95" is an internal sampling PROBE, five mm upstream of the outlet BC
# PATCH at X_OUT = 100 mm. The two are not the same pressure: there is a real ~1% Poiseuille drop
# across that last 5 mm of r=0.9 mm tube. Do not compare A3/A4 (which are defined on the patch)
# against p_x95_Pa - use the separate p_outletPatch_Pa column added in stageA_benchmark_0d.py.
PROBES_STEN = dict(inlet=-10.0, proximal=20.0, throat=31.5, measurement=56.5, x95=95.0)
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
                # Fixed 2026-09-18 audit (Fable/Codex/Gemini all confirmed the prior winding gave
                # inward-pointing wall normals while the caps were correctly outward - surfaceCheck
                # reported 3 orientation zones). This ordering gives outward normals throughout.
                _tri(f, A[k], B[k2], B[k]); _tri(f, A[k], A[k2], B[k2])       # outward normals
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
    ap.add_argument("--ds", type=int, nargs="+", default=[0, 50, 70, 80],
                     help="stenosis %%DS values to generate (default: the original Stage A set, "
                          "0 50 70 80 - pass explicit values, e.g. --ds 60 65, to generate only those)")
    a = ap.parse_args()
    for ds in a.ds:
        if not (0 <= ds < 100):
            raise SystemExit(f"--ds values must be in [0,100), got {ds}")
    import os; os.makedirs(a.outdir, exist_ok=True)
    if not (np.isfinite(a.dx) and a.dx > 0):
        raise SystemExit(f"--dx must be finite and positive, got {a.dx}")
    if a.ncirc < 3:
        raise SystemExit(f"--ncirc must be >= 3, got {a.ncirc}")

    def axial_grid(a0, b0, dx):
        # Fixed 2026-09-18 audit: np.arange(a0, b0+eps, dx) truncates before b0 whenever
        # (b0-a0)/dx is not an integer (e.g. --dx 0.3 stopped at 99.9 mm, not 100 mm), silently
        # shortening the domain and de-syncing the mesh from the probe-plane landmarks. linspace
        # with a rounded point count always includes both endpoints exactly.
        n = max(2, int(round((b0 - a0) / dx)) + 1)
        return np.linspace(a0, b0, n)

    xp = axial_grid(0.0, 100.0, a.dx)
    write_stl(os.path.join(a.outdir, "pipe.stl"), xp, radius_pipe(xp), a.ncirc)
    xs = axial_grid(X_IN, X_OUT, a.dx)
    for ds in a.ds:
        write_stl(os.path.join(a.outdir, f"sten{ds:02d}.stl"), xs, radius_sten(xs, ds), a.ncirc)
        print(f"sten{ds:02d}.stl  throat radius {radius_sten(LESION_C, ds):.4f} mm")
    print(f"wrote pipe.stl + {len(a.ds)} stenosis STL(s) (metres) to", os.path.abspath(a.outdir))
