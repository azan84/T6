"""
error_types.py — the four segmentation error types, as operations on a tree's segment list.

Each returns a NEW segment list (the clean one is never mutated). Node indices change when topology changes, so
callers map nodes between clean and corrupted trees by coordinate (`Tree.xyz`), never by index.

MAGNITUDES — read this before citing them. The header previously read "derived from ImageCAS-X's own measured
inter-observer disagreement ... not chosen". That is true of T3 and T4 and FALSE of T1 and T2. Corrected 2026-09-19.

  T3, T4  derived from measured statistics (HD95 2.46 mm; lumen DSC 92.8 %). The dataset's lead author states those
          statistics are an UPPER BOUND ON AGREEMENT, because both annotators edited the same automatically generated
          centrelines and initialised from the same 3D U-Net. So as statistics they understate disagreement. Whether
          that makes each derived magnitude conservative is argued per magnitude, not assumed: T4's DSC->radius step
          attributes the whole overlap deficit to coaxial calibre, which biases the other way.
  T1, T2  NO MEASURED MAGNITUDE. Both are design choices, declared as such:
            T1 deletes the LARGEST eligible downstream branch in every instance - a 100 % event rate, not a rate from
               data. ImageCAS-X's Betti error (beta0+beta1) cannot supply one: deleting a side branch changes neither
               the component count nor the loop count. The dataset's DSC-vs-diameter rho = +0.89 suggests real
               disagreement concentrates in the SMALLEST branches, so this choice is not conservative by default.
            T2 truncates at a fixed 25 mm (= RUNOFF + 5 mm; decision B2 raised it from 15 mm, which was SHORTER
               than RUNOFF and so deleted the measurement node). Betti error DOES bear on breaks (they raise beta0),
               but the 25 mm distance itself is a design choice, not a measured magnitude.
  NOT quality-matched. No magnitude is conditioned on image quality, diameter, attenuation or disease status; those
  enter the ANALYSIS as covariates and strata (STATISTICS-PLAN SS5), never the injection.

They are constants here so that a magnitude can never be tuned after seeing a result. Editing this file changes a
hashed artefact: re-issue the manifest (PREREGISTRATION-CHECKLIST SS1).

  T1 missed side branch   delete a branch subtree and its outlets            (topological)
  T2 vessel break         terminate a vessel early, losing the distal subtree (topological)
  T3 stenosis length      mis-measure the lesion's axial extent               (calibre/extent)
  T4 taper / undersizing  scale radius along the vessel and distal tree       (calibre)
"""
from __future__ import annotations
import numpy as np
from zerod_ffr import Segment

# --- magnitudes, from measured disagreement (ImageCAS-X paper, test-set re-annotation) --------------------------
# T4: lumen DSC 92.8 % between annotators. For two co-axial cylinders of radii r and k*r, DSC = 2k^2/(k^2+1);
#     solving 2k^2/(k^2+1) = 0.928 gives k = 0.930, i.e. a ~7 % radius under-read. Under-sizing is the clinically
#     relevant direction (it inflates stenosis severity), so k = 0.93 is the registered magnitude.
T4_RADIUS_SCALE = 0.930
# T3: HD95 = 2.46 mm between annotators — the 95th-percentile surface distance, which is what an axial extent error
#     looks like at a lesion shoulder. Registered as a +2.46 mm over-estimate of lesion length.
T3_LENGTH_DELTA = 2.46e-3
# T2: vessel breaks are reported present in all predictions; distal DSC declines (rho = -0.36 with distance).
#     Truncation of the host vessel this far distal to the lesion's distal edge — the measurement node survives and
#     the run-off beyond it is lost.
#
#     DECISION B2, settled 2026-09-19. This was 15e-3, which is LESS than RUNOFF (20 mm, severity_sweep), so the
#     truncation deleted the very measurement node the docstring below says it "deliberately" preserves. Measured:
#     the node survived in 0 of 30 frozen 3D instances and `meas_same_point` was False in 36/36 T2 smoke rows. The
#     endpoint then fell on the stump -- an OUTLET, whose pressure is imposed by the boundary condition rather than
#     computed, and in 3D literally a patch value. Every T2 number under Protocol A was measuring a wall.
#
#     Set to RUNOFF + 5 mm so the measurement node is interior with a margin, which is the stated design intent:
#     T2 is loss of run-off, not loss of the measurement site. The two constants live in different modules and
#     nothing connected them, so `ablation.py` now asserts T2_KEEP_BEYOND > RUNOFF at import.
T2_KEEP_BEYOND = 25e-3

# The guard lives HERE, beside the constant it protects, and is a raise rather than an assert: `python -O` strips
# asserts, and a guard that vanishes under an optimisation flag is not a guard. It also used to sit in ablation.py,
# so any script that did not import ablation was unprotected.
from severity_sweep import RUNOFF as _RUNOFF          # severity_sweep does not import this module: no cycle
if not T2_KEEP_BEYOND > _RUNOFF:
    raise ValueError(
        f"T2_KEEP_BEYOND ({T2_KEEP_BEYOND*1e3:.1f} mm) must EXCEED RUNOFF ({_RUNOFF*1e3:.1f} mm), or T2's truncation "
        f"deletes the measurement node it is defined to preserve, and the FFR endpoint is read at a boundary "
        f"condition instead of a computed interior pressure (decision B2, 2026-09-19).")

def _descendants(segs, sid):
    dead = {sid}; grew = True
    while grew:
        grew = False
        for s in segs:
            if s.parent in dead and s.sid not in dead: dead.add(s.sid); grew = True
    return dead

def t1_missed_branch(segs, tree, path, s_arc, c, L, min_r=None):
    """Delete the largest side branch leaving the host path DISTAL to the lesion (Gamage's downstream case, where the
    effect is large: he reports 13-15 % FFR change downstream vs ~2 % upstream). Returns (segs, info) or (None, why)."""
    pset = set(int(v) for v in path)
    cand = [(tree.r_ref[c_], int(c_), float(s_arc[k])) for k, v in enumerate(path) for c_ in tree.children[v]
            if int(c_) not in pset and s_arc[k] >= c + L / 2 and (min_r is None or tree.r_ref[c_] >= min_r)]
    if not cand: return None, "no deletable downstream branch"
    r_br, node, s_br = max(cand)
    dead = _descendants(segs, int(tree.seg[node]))
    out = [s for s in segs if s.sid not in dead]
    if not out: return None, "deletion would empty the tree"
    return out, dict(branch_r_mm=r_br * 1e3, branch_arc_mm=s_br * 1e3, segments_deleted=len(dead),
                     branch_to_host_ratio=float(r_br / tree.r_fit[path[int(np.argmin(np.abs(s_arc - c)))]]))

def t2_truncation(segs, tree, path, s_arc, c, L):
    """Terminate the host vessel T2_KEEP_BEYOND (25 mm) past the lesion's distal edge; everything beyond is lost,
    including any branch arising there. The measurement node (20 mm distal) is NOT removed — the error is loss of
    run-off, not loss of the measurement site.

    That last sentence was false until 2026-09-19: T2_KEEP_BEYOND was 15 mm, i.e. SHORTER than the 20 mm run-off, so
    the truncation removed the measurement node in every case (0 of 30 frozen 3D instances kept it). Decision B2 set
    the constant to RUNOFF + 5 mm; `ablation.py` now asserts the relationship at import so it cannot regress."""
    s_cut = c + L / 2 + T2_KEEP_BEYOND
    if s_cut >= s_arc[-1]: return None, "vessel already ends before the truncation point"
    k_cut = int(np.searchsorted(s_arc, s_cut))
    node = int(path[k_cut]); sid = int(tree.seg[node])
    host = next(s for s in segs if s.sid == sid)
    keep_pts = [i for i in range(len(host.pts)) if np.linalg.norm(host.pts[i] - tree.xyz[node]) > 1e-12]
    # keep the part of the host segment up to and including the cut node
    d = np.linalg.norm(host.pts - tree.xyz[node], axis=1); i_cut = int(np.argmin(d))
    if i_cut < 2: return None, "truncation point falls at the start of its segment"
    dead = set()
    for s in segs:
        if s.parent == sid: dead |= _descendants(segs, s.sid)
    out = []
    for s in segs:
        if s.sid in dead: continue
        out.append(Segment(s.sid, s.parent, s.pts[:i_cut + 1].copy(), s.r[:i_cut + 1].copy(), s.label)
                   if s.sid == sid else s)
    return out, dict(cut_arc_mm=float(s_arc[k_cut] * 1e3), length_lost_mm=float((s_arc[-1] - s_arc[k_cut]) * 1e3),
                     segments_deleted=len(dead))

def t3_stenosis_length(segs, tree, path, s_arc, c, L):
    """No anatomical change: the lesion's axial EXTENT is mis-measured. Handled by the caller, which re-inserts the
    same %DS over L + T3_LENGTH_DELTA. Returned unchanged so the caller's interface is uniform."""
    return list(segs), dict(length_delta_mm=T3_LENGTH_DELTA * 1e3)

def t4_taper(segs, tree, path, s_arc, c, L, scale=T4_RADIUS_SCALE):
    """Under-size the lumen from the lesion's proximal shoulder distally: radius x scale on the host segment from
    that point and on every descendant segment. Both r and (recomputed) r_fit shrink, so %DS is unchanged and the
    effect is purely the ~1/scale^4 rise in viscous resistance — an under-read lumen, not a fabricated stenosis."""
    s0 = c - L / 2
    k0 = int(np.searchsorted(s_arc, s0)); node = int(path[max(k0, 0)]); sid = int(tree.seg[node])
    fam = _descendants(segs, sid)
    out = []
    for s in segs:
        if s.sid not in fam: out.append(s); continue
        r = s.r.copy()
        if s.sid == sid:
            d = np.linalg.norm(s.pts - tree.xyz[node], axis=1); i0 = int(np.argmin(d))
            r[i0:] *= scale
        else:
            r *= scale
        out.append(Segment(s.sid, s.parent, s.pts, r, s.label))
    return out, dict(radius_scale=scale, segments_scaled=len(fam), from_arc_mm=float(s_arc[max(k0, 0)] * 1e3))

ERROR_TYPES = {"T1_missed_branch": t1_missed_branch, "T2_truncation": t2_truncation,
               "T3_stenosis_length": t3_stenosis_length, "T4_taper": t4_taper}
TOPOLOGICAL = ("T1_missed_branch", "T2_truncation")
