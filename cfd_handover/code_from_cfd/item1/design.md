# Item 1 design: branched idealised tree (Y-bifurcation + 1 side branch, 3 outlets)

## REVISION NOTE (2026-09-19, post-panel)
Fable 5.1, GPT-6-astra and Gemini 3.8 Flash independently audited the first version of this design and
all three found the SAME fatal geometry bug by directly slicing the generated surface: branch B was
placed on branch A's own axis (y=0,z=0) for x=30-45mm, so the two vessels shared a single fused lumen
in 3D while the 0D model treated them as parallel. All three also independently derived that the hand
relax values (0.05/0.2) and the naive automatic relax rule would diverge on this tree
(true stability limit ~0.006-0.02, not 0.05-0.5). This revision fixes both, verified against an
independent numeric check (see below) that matches Fable's own hand-derived numbers to within ~1%.

## Topology (see `geometry.py`, now the SINGLE shared source for both `build_0d.py` and
`build_centerline.py` — the previous version duplicated coordinates in both files independently,
which is how they drifted apart and both encoded the same bug)
trunk (r=1.8mm, x=0-30mm, straight) -> at x=30mm bifurcates into:
  - A (r=1.518mm CONSTANT except a 60%DS cosine lesion at x=45-55mm, x=30-70mm, continues straight
    along the trunk axis) — "main branch". (Previously mis-described as "tapering"; it is constant
    radius outside the lesion window. The lesion is DOWNSTREAM of the A/B split, not upstream as an
    earlier draft said.)
  - B (r=1.326mm, leaves the bifurcation at a genuine 60-degree angle, length 15mm) -> at its tip
    bifurcates into:
    - B1 (r=1.148mm, diverges a further -15 degrees from B's own direction, length 30mm)
    - B2 (r=0.935mm, diverges a further -55 degrees from B's own direction, length 25mm)

**Numeric clearance verification** (`geometry.py::verify_clearances`, run automatically at the top of
both builders, not just documented): every pair of non-sibling/non-parent-child tubes keeps >=0.3mm
surface-to-surface clearance beyond a 5mm carina allowance at any shared bifurcation point (real
vessels of this bore cannot separate instantaneously at the ostium — a real carina occupies a few mm,
consistent with these radii; the check only flags fusion that PERSISTS past that region, which is what
the panel's bug actually was). Both ds=0% and ds=60% pass with comfortable margins
(A-B=2.18mm, A-B1=10.3mm, A-B2=10.5mm, B1-B2=1.34mm clearance beyond the allowance).

**Confirmed against the actual reconstructed surface, not just the analytic check** (2026-09-19,
re-running the SAME slice-count diagnostic the panel used to find the original bug): the corrected
`raw_surface_ds00.vtp`/`raw_surface_ds60.vtp` now show 1 contour at x=20-32mm (trunk, correctly within
the carina region), 2 contours at x=35-38mm (A and B genuinely separated — the original bug showed 1
fused contour here, persisting to x~53mm), 3 contours at x=40-52mm (A/B1/B2 all separate), dropping to 2
past each of B2's (~52mm) then B1's (~66mm) endpoints — exactly the expected topology. As-built throat
radius on branch A (the lesion-bearing, decision-relevant branch) measured 0.6067mm vs target 0.6072mm
(-0.08%) at the ds=60% lesion centre, and 1.5176mm vs 1.518mm (-0.03%) at a healthy A location — both
well under the 1% criterion, on the RAW pre-smoothing surface. (B1/B2's naive x=const-slice apparent
radius reads 1.5-35% high because those branches are steeply angled — an oblique-slice measurement
artifact, not a geometry defect; the pipeline's planned perpendicular-to-axis throat check, still to be
run after Taubin smoothing, will confirm their true radii correctly.)

## 0D reference (`build_0d.py`, rewritten to freeze physiology — panel finding #2)
**Bug fixed:** the previous version built a FRESH `Tree` for the ds=60% case, which let
`robust_taper()` re-fit branch A's now-lesioned radius profile and silently shifted r_ref/r_fit/the
leaf weights w/and the calibration constant C for ALL THREE outlets — B1 and B2 moved ~1.2% even
though the lesion is only in A, contradicting the original design's "(~unchanged)" claim, which had
never actually been checked.
**Fix:** build ONE healthy (ds=0%) `Tree(bed="discrete")`, calibrate C once, then get the diseased case
via `T.evaluate(C, r_override=r_diseased)` — this is exactly the mechanism `zerod_ffr.Tree`'s own
docstring describes it for ("solving with an overridden radius while the physiology... stays frozen").
r_ref, r_fit, the leaf weights w, and C are now IDENTICAL between the two 3D cases by construction, and
both 3D cases use the SAME (ds=0-derived) outlet R values.

Verified output (`python3 build_0d.py`, ds=0% and ds=60%, both from the same healthy tree):
| outlet | R_out (Pa.s/m3, SAME for both ds cases) | R_own (own terminal segment) | G=R_out/R_own | relax=min(0.5,1/(1+G)) |
|---|---|---|---|---|
| A  | 1.308255e10 | 7.6731e7 | 170.5 | 0.0058 |
| B1 | 2.750617e10 | 1.7594e8 | 156.3 | 0.0064 |
| B2 | 4.748064e10 | 3.3319e8 | 142.5 | 0.0070 |

Flow split ds=0%: A=0.8579, B1=0.4067, B2=0.2355 mL/s (sums to Q_demand=1.5 mL/s).
Flow split ds=60% (frozen physiology, only A's epicardial radius changed): A=0.8243 (FFR_A drops to
0.9543), B1=0.4067, B2=0.2355 mL/s (both B1/B2 numerically UNCHANGED to 4 significant figures, unlike
the previous, buggy version) — this cross-checks against Fable's independent hand-derivation
(0.8247/0.4066/0.2354 mL/s, FFR_A=0.9546) to within ~0.05%.

## Geometry pipeline (status: centreline + tube-function images regenerating with the fixed geometry)
1. Centreline (`build_centerline.py`, uses `geometry.py`): three overlapping root-to-tip paths, shifted
   +42mm/+6mm in y/z (VMTK's `-bounds` rejects negative values; the new geometry's wider branch spread,
   down to y=-33.5mm before the shift, needed a bigger shift than the original +12mm).
2. `vmtkcenterlinemodeller`: dimensions recomputed per-axis (not reusing the old grid) at the same
   throat-resolution target (r_throat_min/8 = 7.59e-5 m, r_throat_min=0.6072mm at the ds=60% lesion):
   969 x 534 x 93 (~48.1M voxels), bounds `0.0 0.0735 0.00503 0.0455 0.0025 0.0095`.
3. Remaining, not yet run: `vmtkmarchingcubes` + Taubin smoothing (VMTK's tutorial-standard
   `-iterations 30 -passband 0.1`, NOT VMTK's own defaults — corrected wording per panel finding) with
   an explicit post-smoothing check that the as-built throat radius is still within 1% of target (panel
   finding: this check was missing; smoothing is where the throat radius is actually at risk) ->
   explicit clipping of the 4 open ends (trunk inlet, A/B1/B2 outlets) perpendicular to the local axis
   (panel finding: the previous surfaces had only ONE connected boundary loop at x=0, i.e. the other
   three ends were capped/closed by the implicit reconstruction, not open — clipping must happen before
   `vmtkflowextensions`, which needs genuinely open boundaries to attach to) -> `vmtkflowextensions`
   (length ~8x local diameter, a stated deliberate deviation from the spec's 5D inlet/3D outlet
   convention) -> cfMesh at Stage-A-consistent settings (maxCellSize scaled per-branch from local
   radius; boundaryLayers nLayers=4/thicknessRatio 1.2) -> OpenFOAM case.

## BC test plan
**Pass criterion:** every outlet reaches P = Pv + R*Q within 0.1% AND the 3D flow split matches
svZeroD (the `build_0d.py` split above), for BOTH the 0% and 60%DS cases.

**Two relax strategies, both required to pass independently:**
1. **Hand values**, per-outlet, from the table above (0.0058/0.0064/0.0070) — NOT the original
   0.05/0.2, which all three reviewers independently showed would diverge (true stability limit here is
   ~0.006-0.02 because the epicardial vessels are extremely short/low-resistance relative to the
   distal bed, G~140-170, far more extreme than any single-outlet Stage A case).
2. **A revised automatic relax rule** (panel consensus, replacing the original global-`p0-pBar`
   proposal, which Fable/Gemini/astra all independently showed underestimates each outlet's true
   self-gain on a branched tree, by 1.3-1.7x in this specific case and potentially 10-50x on a real,
   more asymmetric tree — enough to destabilise the "conservative" rule):
   ```cpp
   const scalar G = R / R_own;              // R_own = 8*mu*L/(pi*r^4) of THIS outlet's own terminal
                                              // segment, from the 0D tree (build_0d.py table above) -
                                              // a per-outlet LOCAL quantity, not a shared global drop.
   const scalar relax = min(0.5, 1.0/(1.0 + G));
   ```
   Static per-outlet values (from the table above), not a live in-solver estimate — the panel flagged
   that a live estimate has a start-up hazard (Q~=0 at iteration 0 gives G~=0, relax~=0.5, i.e. exactly
   the unstable value) unless floored at a pre-computed minimum G, which for this tree makes the
   "automatic" and "hand" values identical. This item now tests whether hand-computed-from-R_own values
   (i.e., what a script COULD compute automatically from the 0D tree, without a human picking them) hold
   up on a real multi-outlet case — a de-risked version of "automatic" that avoids the start-up
   instability class of failure the panel identified, per the work order's own "if it's stable here it
   becomes the production rule" framing.
   Initialise each patch at its own 0D-predicted pressure (not P_v/rho), matching Stage A's established
   practice.

Both strategies get the SAME two acceptance checks (BC accuracy to 0.1%, flow-split match to svZeroD).

## Documentation corrections applied
- Lesion is downstream of the A/B split (in A, x=45-55mm), not upstream — text fixed above.
- Branch A is constant radius outside the lesion window, not "tapering" — text fixed above.
- Flow extensions at ~8x local diameter are a stated, deliberate deviation from the spec's 5D/3D
  convention (unchanged from the original design, now explicitly flagged as a deviation rather than
  left silent).
