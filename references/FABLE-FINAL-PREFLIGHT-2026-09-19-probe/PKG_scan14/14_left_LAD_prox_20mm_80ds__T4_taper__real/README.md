# 14_left_LAD_prox_20mm_80ds__T4_taper__real

**Frame:** mm, LPS. The ImageCAS-X NIfTI affine is RAS: negate x and y before applying inv(affine) to reach voxel indices. Verified — with the flip 42/42 deletion points land inside the lumen, without it 0/42.

**Tier:** real · **Error type:** T4_taper

Files: `centreline.vtp` (with `radial_scale`, `r_target_mm`), `outlets.csv`, `bc_A.csv`, `bc_B.csv`, `bc_C_flows.csv`, `territories.csv`, `probes.csv`, `inlet.json`, `mask_edit.json`, `meta.json`.

## Build
1. Apply `mask_edit.json.truncation_rule`.
2. Apply `mask_edit.json.mask_edit.rule` if present (a reference implementation ships with it).
3. Marching cubes.
4. **Subdivide the surface inside the lesion window (centre +/- L/2) to edge length <= r_throat/8 BEFORE
   deforming.** At 80 %DS on this cohort r_throat is ~0.23 mm, so the target edge is ~0.03 mm against a
   voxel of ~0.32 mm: roughly 13x refinement. Marching-cubes resolution alone cannot represent the throat
   and the deformation will simply not produce the intended stenosis.
5. Apply `surface_rule` using `radial_scale`, then **check the as-built throat radius against
   `r_target_mm` and reject the case if it differs by more than 1 %** (CFD-ARM-SPEC §6.1a).
6. Flow extensions, mesh, solve per CFD-ARM-SPEC §6.2.

## Solver settings that are NOT free choices
- **Resistance-outlet under-relaxation is a stability bound, not a preference:**
  `alpha < 2 / (1 + R_outlet/R_epicardial)`. On these lumens that bound is ~0.10, and the MILDEST cases
  fail first (a mild case has the largest R_outlet/R_epi). **Start at alpha = 0.05.** The 0.2 in the
  `bc/resistanceOutlet.md` template diverges on the Stage A `sten00` case.
- **Reynolds number:** record it for every solve. Many baselines in this cohort sit above Re 300 and some
  above 400; steady laminar may not converge. Do NOT silently switch turbulence model — use the agreed
  pimpleFoam time-average fallback and report those cases separately.

## Return
as-meshed radius along the centreline; area-averaged pressure AND through-plane flow integral at every probe; per-outlet flow and pressure; throat Re; `checkMesh` status; wall-clock.

`bc_A.csv` / `bc_C_flows.csv` `mode` column: `resistance` imposes R; `closed` means a WALL (zero conductance — the 0D model's own treatment of an outlet with no clean counterpart); `prescribed` imposes the flow for the first Protocol C solve.
