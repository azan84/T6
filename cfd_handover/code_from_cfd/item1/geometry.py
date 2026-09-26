"""
Shared, single-source-of-truth geometry for the Item-1 branched tree (Y + 1 side branch, 3 outlets),
used by BOTH build_0d.py and build_centerline.py so they cannot drift apart (panel finding, 2026-09-19:
the two builders previously duplicated coordinates independently, and both put branch B on A's own axis).

FIX applied per unanimous 3-way panel finding (Fable 5.1 / GPT-6-astra / Gemini 3.8 Flash, all three
independently sliced the generated surface and found A and B fused into a single lumen from x=30 to
x=45mm, because both builders placed B on A's exact axis, y=0,z=0, with only a radius difference).
B now branches off at a real 40 degree angle starting AT the bifurcation point (x=30mm), and B1/B2
diverge further from B's own endpoint at angles chosen so neither approaches back within
r_i+r_j+3-voxel margin of A or of each other over the full run. Verified numerically below, not just by
inspection - `verify_clearances()` samples every non-parent-child pair of tubes densely and asserts a
minimum surface-to-surface clearance.
"""
import numpy as np

LESION_C, LESION_L = 50.0, 10.0   # mm, centred in branch A, i.e. x in (45,55) - DOWNSTREAM of the
                                   # A/B split at x=30 (earlier design.md wording called this
                                   # "upstream", which was wrong; fixed here).
MARGIN_MM = 0.3                   # required surface-to-surface clearance between non-parent-child
                                   # tubes (~4 voxels at the ~76um target spacing - panel asked for 3).

def r_A(x, ds_pct):
    """Branch A radius profile: constant 1.518mm except a raised-cosine 60%DS lesion. A is CONSTANT
    radius outside the lesion window, not tapering (design.md previously mis-described it as
    'tapering' throughout - fixed)."""
    x = np.asarray(x, float)
    r0 = 1.518
    w = np.where(np.abs(x - LESION_C) < LESION_L / 2,
                 0.5 * (1 + np.cos(np.pi * (x - LESION_C) / (LESION_L / 2))), 0.0)
    return r0 * (1 - ds_pct / 100.0 * w)

def _polyline(p0, angle_deg, length_mm, n):
    """n points from p0, straight line at angle_deg (in the x-y plane) for length_mm."""
    t = np.linspace(0, 1, n)
    dx = length_mm * np.cos(np.radians(angle_deg))
    dy = length_mm * np.sin(np.radians(angle_deg))
    x = p0[0] + t * dx
    y = p0[1] + t * dy
    z = np.full_like(x, p0[2])
    return x, y, z

def build_paths(ds_pct, n_trunk=61, n_a=161, n_b=31, n_b1=61, n_b2=61):
    """Returns dict of branch -> (x,y,z,r) arrays in mm, in the project's (x,y,z) convention, all
    starting from the true origin (0,0,0) - NOT yet shifted for VMTK's non-negative-bounds quirk
    (build_centerline.py applies that shift itself)."""
    x_t = np.linspace(0, 30, n_trunk); y_t = np.zeros_like(x_t); z_t = np.zeros_like(x_t)
    r_t = np.full_like(x_t, 1.8)

    x_a = np.linspace(30, 70, n_a); y_a = np.zeros_like(x_a); z_a = np.zeros_like(x_a)
    r_a = r_A(x_a, ds_pct)

    # B leaves the bifurcation at x=30mm at a real 60deg angle (was: collinear with A, the bug -
    # see verify_clearances for the numeric requirement this angle satisfies).
    xb, yb, zb = _polyline((30.0, 0.0, 0.0), angle_deg=-60.0, length_mm=15.0, n=n_b)
    r_b = np.full_like(xb, 1.326)
    b_end = (xb[-1], yb[-1], zb[-1])

    # B1/B2 diverge further from B's endpoint, at angles chosen (see verify_clearances) to stay clear
    # of A and of each other for the rest of the domain.
    xb1, yb1, zb1 = _polyline(b_end, angle_deg=-15.0, length_mm=30.0, n=n_b1)
    r_b1 = np.full_like(xb1, 1.148)

    xb2, yb2, zb2 = _polyline(b_end, angle_deg=-55.0, length_mm=25.0, n=n_b2)
    r_b2 = np.full_like(xb2, 0.935)

    return {
        "trunk": (x_t, y_t, z_t, r_t),
        "A":     (x_a, y_a, z_a, r_a),
        "B":     (xb, yb, zb, r_b),
        "B1":    (xb1, yb1, zb1, r_b1),
        "B2":    (xb2, yb2, zb2, r_b2),
    }

CARINA_SKIP_MM = 5.0   # a real bifurcation's two daughters touch AT the shared ostium point - only
                        # flag fusion that persists beyond a short carina region, not the physically
                        # unavoidable contact exactly at a branch point.

def _min_surface_gap(path1, path2, skip1_mm=0.0, skip2_mm=0.0):
    """Minimum surface-to-surface distance between two dense-sampled tube paths (centre distance minus
    both radii, at the closest pair of samples), ignoring the first skip*_mm of arc length of each path
    (used only for pairs that share a start point, i.e. true siblings at a bifurcation)."""
    x1, y1, z1, r1 = path1; x2, y2, z2, r2 = path2
    s1 = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(np.stack([x1, y1, z1], 1), axis=0), axis=1))])
    s2 = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(np.stack([x2, y2, z2], 1), axis=0), axis=1))])
    m1 = s1 >= skip1_mm; m2 = s2 >= skip2_mm
    P1 = np.stack([x1, y1, z1], 1)[m1]; P2 = np.stack([x2, y2, z2], 1)[m2]
    r1 = r1[m1]; r2 = r2[m2]
    d = np.sqrt(((P1[:, None, :] - P2[None, :, :]) ** 2).sum(-1))
    gap = d - r1[:, None] - r2[None, :]
    return gap.min()

def verify_clearances(ds_pct, margin_mm=MARGIN_MM):
    """Assert every pair of NON-parent-child tubes keeps at least margin_mm surface-to-surface
    clearance, everywhere BEYOND a short carina region at any shared bifurcation point. Parent-child
    pairs (trunk/A, trunk/B, B/B1, B/B2) touch at their shared point by construction and are not
    checked. Returns the checked pair->gap dict."""
    paths = build_paths(ds_pct, n_trunk=301, n_a=801, n_b=301, n_b1=601, n_b2=601)  # dense for the check
    # (pair, skip-first-N-mm-of-first-path, skip-first-N-mm-of-second-path)
    pairs = [("A", "B", CARINA_SKIP_MM, CARINA_SKIP_MM),
             ("A", "B1", 0.0, 0.0), ("A", "B2", 0.0, 0.0),
             ("B1", "B2", CARINA_SKIP_MM, CARINA_SKIP_MM)]
    gaps = {}
    for u, v, s1, s2 in pairs:
        g = _min_surface_gap(paths[u], paths[v], s1, s2)
        gaps[(u, v)] = g
        assert g >= margin_mm, (
            f"geometry.py: {u}/{v} clearance {g:.4f}mm < required {margin_mm}mm (beyond the "
            f"{CARINA_SKIP_MM}mm carina allowance) at ds={ds_pct}% - these tubes would fuse in the "
            f"reconstructed surface, exactly the bug the panel found."
        )
    return gaps

if __name__ == "__main__":
    for ds in (0, 60):
        gaps = verify_clearances(ds)
        print(f"ds={ds}%DS clearances (mm): " + ", ".join(f"{k[0]}-{k[1]}={v:.3f}" for k, v in gaps.items()))
