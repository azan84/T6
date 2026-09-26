# Stage A case skeleton — added 2026-09-18 after the 3-way setup audit

**Update 2026-09-26: no longer untested** — the values of this skeleton were exercised on real OpenFOAM ESI v2406 in every Stage A / Item solve (the runs used files with the same values but different formatting; see `code_from_cfd/README.md`); a complete case as actually run is in `../example_complete_case_sten70_S25A/`. The rest of this text is the original 2026-09-18 note. The coded BC file is now `bc/resistanceOutlet_steady.md` (formerly `resistanceOutlet.md`).

_(original text)_ Still UNTESTED on real OpenFOAM hardware — same caveat as everything else in `cfd_handover/`.
This exists because all three audits (`references/SETUP-AUDIT-SYNTHESIS-2026-09-18.md`) flagged
that no `fvSchemes`/`fvSolution`/`controlDict` were provided anywhere, so an operator improvising
one from a tutorial risks a first-order `div(phi,U) bounded Gauss upwind` default — which would
silently add numerical diffusion to the throat pressure drop, and nothing in Stage A except A5
(mesh independence) would necessarily catch it, since A2 has no pass/fail by design.

## What's here
- `system/fvSchemes` — pins **second-order** convection (`linearUpwind`, not `upwind`).
- `system/fvSolution` — standard SIMPLE relaxation, plus `residualControl` deliberately **off**.
  The spec's convergence criterion is "residuals < 1e-5 **and** flow/pressure monitors stable to
  < 0.1% over 200 iterations" — a compound, monitor-based criterion, not the single-threshold
  auto-stop `residualControl` normally provides. Leaving it on would let the run stop on
  residuals alone before the monitors have actually settled. Run a fixed, generous iteration
  count instead and inspect the monitor history (see below).
- `constant/transportProperties`, `constant/turbulenceProperties` — laminar, ν = 3.773585e-6 m²/s
  (unrounded quotient of μ/ρ = 0.004/1060; the commonly-quoted 3.774e-6 is a +0.011% rounding).
- `system/controlDict` — run control plus two worked `surfaceFieldValue` function objects (inlet
  flux sum, outlet patch pressure average — the latter is exactly `p_outletPatch_Pa`, the quantity
  A3/A4 need). **Copy the pattern to add the other probe planes** (proximal/throat/measurement/x95
  at x = 20/31.5/56.5/95 mm) as `sampledSurface` `plane` regions — not written out here because an
  untested multi-plane function-object dictionary is worse than an honest gap; the one worked
  example (a patch-based `surfaceFieldValue`, the simplest and most standard form) is enough to
  copy from.

## What's NOT here (assemble from elsewhere, per case)
- `0/p`, `0/U` — copy from `bc/resistanceOutlet.md`, substituting that case's `R`, `relax`, and
  initial `value` from the per-case table there. Different per case (sten00/50/70/80/pipe), so not
  duplicated here to avoid two sources of truth drifting apart.
- The mesh itself (`system/cartesianMeshDict` for cfMesh, or `snappyHexMeshDict`) — geometry- and
  mesher-specific, out of scope for this generic skeleton.
- `system/decomposeParDict` — add when you know the core count per job (spec: two 8-core jobs
  side by side).

## Fork-specific risk, flagged by the audits, not resolved here
Foundation 11+ restructured `simpleFoam` into a `foamRun -solver incompressibleFluid` wrapper and
may rename `constant/turbulenceProperties` to `constant/momentumTransport`. This skeleton uses the
ESI/.com and Foundation-through-v10 convention (`constant/turbulenceProperties`,
`application simpleFoam;`). If you're on Foundation 11+, check which convention your installed
release actually expects before running, and report back which one worked, with the exact
OpenFOAM version.
