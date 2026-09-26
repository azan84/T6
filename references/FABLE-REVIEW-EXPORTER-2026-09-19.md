# Independent adversarial review — `code/export_cfd_case.py` (CFD case packages, Gate M1)

**Date:** 2026-09-19 · **Reviewer:** Fable (independent) · **Target:** `code/export_cfd_case.py` as of today, never run for real.
**Checked against:** CFD-ARM-SPEC v0.2 §2.2–2.5, §6.1b, §7, §11–§13; SEVERITY-SWEEP-SPEC §4; DETECTOR-SPEC §7.2/§8
(provisional, under separate review); `zerod_ffr.py`, `ablation.py`, `severity_sweep.py`, `error_types.py`;
`cfd_handover/START-HERE.md`.
**Probe:** `FABLE-REVIEW-EXPORTER-2026-09-19-probe/probe_exporter.py` (output `probe_output.txt`) and
`probe_t1_rule.py` (output `probe_t1_rule_output.txt`). Packages were written to the session scratch directory only.
Nothing written to `results/`, `protocol/` or `cfd_handover/`; no existing file modified; the ablation was not run.

---

## Verdict: **GO-WITH-CHANGES** — do not export or send any package until MUST 1–8 are done

The core of the exporter is right: the boundary-condition arithmetic inverts the solver exactly, the units and the
kinematic conversion match Stage A, Protocols A and B reproduce `ablation.py`, the geometry files are well formed, and
the whole thing runs in 3 s per package. But the three M1 packages as currently produced would (a) unblind the CFD
operator through `MANIFEST.json`, (b) give the operator deletion coordinates in an unstated frame that, applied
naively to the NIfTI, land **0 of 42** points in the lumen, and (c) ship a missed-branch mask rule that, executed
exactly as written on the real mask, removes only **512 of the branch's 855 voxels and leaves 67 disconnected voxel
islands** — Gate M1 would then fail its "no manual repair" criterion because of the rule, not because of real lumens,
and the 5-day kill would fire on a false signal. Those are one-line to one-function fixes. The study batch has two
further defects (T2 and T4 packages) that M1 does not exercise but that would force a re-export of 300 packages.

---

## 1. Boundary-condition arithmetic — CORRECT

`zerod_ffr._solve` line 217: `g_bed = self.w[el] / C`, with `w = r_ref^2.66` in metres (discrete bed, line 144), so
`C` carries units Pa·s·m⁻³·m^2.66 and `R_i = C / w_i` is in Pa·s/m³. Probe: `max |R_A − C/w| / R = 1.6e-16`.
Hand check on the first M1 outlet: `287.074 / (0.6469e-3)^2.66 = 8.7321e10`, file `8.7321e10`.

Kinematic conversion: the OpenFOAM relation is `p/ρ = P_v/ρ + (R/ρ)·Q` with the same volumetric `Q`, so
`R_kinematic = R_SI/ρ` (units m⁻¹s⁻¹) is right and is the convention Stage A already uses
(`expected_0D.csv`: 6.9776e9 / 1060 = 6.5826e6, as tabulated). `inlet.json`: 11998.98 Pa → 11.31979 m²/s²,
666.61 → 0.62888, ν = 3.7736e-6 — all match START-HERE step 3.

Order of magnitude against Stage A: Stage A has one outlet at 1.5 mL/s with R = 6.975e9. M1 has six outlets at
0.078–0.135 mL/s (sum 0.649 mL/s = the tree's Murray inflow at r_in 1.08 mm) with R = 7.9e10–1.06e11.
`R_M1/R_stageA = 13.4×` against `Q_stageA/Q_M1 = 13.9×`; `R·Q` = 8.3–11.1 kPa in both. Consistent.

`node_map` in `bc_A`: correct for M1. The map is by rounded coordinate (`ablation.node_map`), T1 does not move
nodes, and all five surviving T1 outlets have clean counterparts. **But NaN does reach a BC file silently in the
batch** — see MUST 6.

## 2. Protocol fidelity and the Protocol C adjudication

**A and B are faithful.** `bc_A` = `C_clean / t.w[m]` on surviving leaves is `ablation.py:148–150` restricted to
`t2.leaves` (equivalent, because the exporter iterates leaves only). `bc_B` re-clears `_C` and recalibrates the
corrupted tree to its own Murray demand, `ablation.py:154`. For baseline/clean `R_A ≡ R_B` (same tree, same C);
for T1 `C_B/C_clean = 0.818`, every surviving R falls 18 % — the deployment case, as intended.

**Protocol C — adjudication: a real but second-order threat to the ladder, first-order to the *residual* panel;
cheap to neutralise; the package should carry per-outlet targets plus an explicit statement of the variant, and the
0D twin must run the identical variant.**

Facts established by the probe (scan 14, T1, discrete bed, 0D):

| variant | FFR_meas | ΔFFR vs clean 0.7612 | territory residual | inflow (mL/s) |
|---|---|---|---|---|
| B re-derived | 0.8642 | +0.103 | — | — |
| C, one global scalar on territory totals (`ablation.py`, STATISTICS-PLAN P2) | 0.8991 | +0.138 | 0.087 (**passes** the < 0.10 check) | 0.517 |
| C, per-outlet exactly determined (what §2.2 has 3D do) | 0.9079 | +0.147 | 0 by construction | 0.554 |

- In the **discrete** bed the two target sets are the same numbers: the "territory total over surviving nodes' clean
  counterparts" that `ablation.py:132–135` builds *is* the sum of the surviving outlets' clean flows (0.0782 mL/s for
  the LAD territory in both). The only difference is the fit: one scalar against N ≥ 2 targets (over-determined,
  residual 0.087) versus N resistances against N targets (exact). So the package's per-outlet `Q_target` is the right
  thing to ship; nothing is lost.
- The FFR consequence of the fit difference is **0.009** here — under the 0.05 "material" threshold but ~2× the V8
  noise floor, and a pure protocol-definition bias that would appear in the 0D-vs-3D Bland–Altman for C and could
  flip κ for any instance within ~0.01 of 0.80. It is not benign for H4 if left unmatched; it is negligible once the
  0D twin runs the same per-outlet procedure (37 iterations of the existing linear solve; the probe does it in 20
  lines).
- The **residual** quantity differs qualitatively: 0.087 (0D one-scalar) versus exactly 0 (3D per-outlet). The §14
  thesis panel ("C drives the flow residual to ~0 while the FFR error persists") is therefore *stronger* at 3D than at
  0D, which reads as a fidelity effect unless the reader is told it is a fit-degrees-of-freedom effect. Also relevant
  to the detector: S3 (residual concentration across territories) is identically zero under 3D-C, and S2's "tuned
  parameter" becomes a vector of per-outlet `R_i/R_A` (probe: `[1, 1.212, 1, 1, 1]` — only the outlet that lost its
  sibling moves). Flag to the DETECTOR-SPEC reviewer.
- The code comment's claim that "the territory-matched variant can be run from the same package" is **false for
  T1/T2**: the deleted outlet's clean flow (0.0953 mL/s) is not in the T1 package, so the clean territory total
  (0.1735) cannot be reconstructed from it. Either carry it or drop the claim (MUST 7).

**What the package should carry:** `bc_C_flows.csv` as now (per-outlet clean flows, territory_id), plus a
`protocol_C` block in `meta.json` stating: targets are the clean model's per-outlet bed flows on surviving outlets;
the 3D procedure is prescribe-flows → read `p_i` → `R_i = (p_i − P_v)/Q_i` → resistance solve (§2.2); the 0D
comparator for P4 is the identical per-outlet procedure (to be added to the discrete 0D twin and pre-registered);
the one-scalar territory fit remains the 0D-primary P2 protocol and is reported alongside. Add
`Q_clean_territory_total_mls` per territory so both variants are runnable from one package.

## 3. Does it run; is the output sane

Ran `--m1 --with-expected` into scratch: 3 packages, 9 files each, 3 s total. (Note: the invocation in the task,
`~/Datasets/imagecas-x`, fails — the data root is `~/Datasets/imagecas-x/ImageCAS-X_dataset`; the exporter does not
descend. CONSIDER 3.)

| check | result |
|---|---|
| `centreline.vtp` opens in pyvista | yes; 748 points / 747 lines (baseline), 706/705 (T1); arrays `MaximumInscribedSphereRadius, r_ref_mm, r_fit_mm, segment_name, branch_id, resolved` — §11's three plus extras |
| `outlets.csv` normals | unit to 1e-16; outward (cos with the 3-edge tangent 0.88–0.998) |
| outlet radii | r_ref 0.601–0.673 mm — every outlet sits at the 0.60 mm cut, i.e. the 1.2 mm-diameter outlets §2.4 warned about; actual EDT radius 0.55–0.79 mm |
| `probes.csv` | 24/24/23 stations, `s_mm` strictly monotone, every station on a centreline point (2.8e-14 mm) and inside the lumen mask (24/24); cap of 40 not reached |
| `bc_C_flows.csv` | all positive, sum 0.649 mL/s = Murray inflow for r_in = 1.08 mm (small but the model's own demand; Stage A used 1.5 mL/s for a 1.5 mm pipe) |
| NaN | none in the three M1 packages; **present in every T2 and T4 package of the 3D subset** (MUST 6) |
| `mask_edit.json` T1 | 42 points, radii 0.50–0.77 mm (3–5 voxels across at 0.318 × 0.318 × 0.5 mm); executable only with an unstated LPS→RAS flip (MUST 2); leaves islands (MUST 3) |
| `--with-expected` | writes `<out>/../withheld/<pkg>/expected_0D.json` — with the default `--out` that is **`cfd_handover/packages/withheld/`**, inside the folder START-HERE calls "the only thing the CFD machine needs from Google Drive" (MUST 4) |

Two things about the probes that are not defects but should be known: grid stations are snapped to the nearest
node while `s_mm` records the grid value, so `s_mm` and `(x,y,z)` disagree by up to 0.24 mm; and there are no
`inlet` or `outlet` rows although §11 lists both and DETECTOR §7.2 lists `outlet` as a kind (SHOULD 3).

## 4. Blinding (§13)

Three findings, in decreasing severity.

1. **`MANIFEST.json` inside `packages/M1/` carries `ffr_discrete = 0.7612` and `base_discrete = 0.9901`** — the 0D
   prediction at the measurement node for the M1 instance and its baseline — because `main()` dumps the whole
   CFD-SUBSET row. Direct violation. MUST 1.
2. **`bc_A.csv × bc_C_flows.csv` reconstructs the clean 0D outlet FFR exactly.** `p_i = P_v + R_i·Q_i` is the outlet
   BC relation itself; with the clean flows as targets it returns the clean lesioned solve's pressure at every outlet:
   0.7488 and 0.7490 at the two LAD outlets against 0.7612 at the measurement node. This is structural — any package
   that ships both A resistances and C flow targets for the same outlets leaks the clean prediction to ~0.01. It cannot
   be removed without splitting the batch; it should be *declared*: §13 blinds the operator to the corrupted-geometry
   predictions and to ΔFFR, not to the clean baseline. SHOULD 1.
3. `r_ref_mm` / `r_fit_mm` in the vtp and probes do not by themselves reveal FFR; together with `R_i`, `P` and the
   radii the operator has the complete 0D input set and could rerun the model — inherent to handing over a 0D-derived
   BC set and acceptable. `--with-expected` does write outside the package folder, but not outside the handover tree
   (MUST 4). The withheld file also records only Protocol B; A and both C variants should be there too (SHOULD 2).

## 5. The M1 instance (scan 14, left LAD prox, 20 mm, 80 %DS)

`m1_instance()` selects `ds_pct == max ∧ n_branch_ge_cut ≥ 1`, then sorts by `n_outlets` desc, `scan` asc. Two
candidates tie (scans 306 and 14, both 6 outlets, 1 branch); 14 wins on scan number, not on difficulty. Comparison:

| | scan 14 | scan 306 |
|---|---|---|
| host r_fit at centre → throat radius | 1.153 → **0.231 mm** (**1.4 voxels across** at 0.318 mm) | 1.348 → 0.270 mm (1.5 voxels at 0.357 mm) |
| bifurcation in lesion window | no (nearest downstream 13.3 mm) | **yes**, 1.3 mm from the distal shoulder |
| deletable branch | r 0.647 mm, 0.56 of host | r 1.065 mm, 0.79 of host (a large diagonal — the harder carina scar) |
| truncated centreline | 121/869 nodes, 47 of 410 mm | 84/891 |

Scan 14 is the harder *mesh* (tighter throat, more sub-cut vessel in the mask); 306 is the harder *edit* (branch
deletion at a big carina, vertex deformation across a bifurcation). The docstring's "most outlets" is not what
decided it (the subset maximum is 8 outlets, scan 43 LCX at 65 %DS). Scan 14 is a defensible pilot; the claim in the
docstring should say what actually chose it (SHOULD 6). The number to carry into the M1 protocol: the 80 %DS throat
is **0.46 mm in diameter on a 0.318 mm grid** — a marching-cubes surface has one vertex per voxel edge, so the throat
polygon will have ~4–5 vertices around its circumference unless the surface is subdivided in the window before
deformation. §6.1a's "spacing ≤ r_throat/8" rule for polyball has no real-tier counterpart yet (SHOULD 7).

## 6. What would waste CFD time or force a re-export

- **T2 and T4 packages all carry a NaN resistance** (60/120 subset packages), written as `out_163,,`.
- **T4 packages carry no taper instruction at all**: `mask_edit.json` has only the lesion table; the 0.93 radius
  scale from the proximal shoulder through every descendant (`error_types.t4_taper`) exists only implicitly in the
  vtp's `MaximumInscribedSphereRadius`. A real-tier T4 built from this package is the baseline.
- **T2 deletes the measurement node**: `T2_KEEP_BEYOND = 15 mm < RUNOFF = 20 mm`, so the cut at 44.72 mm removes
  the 49.71 mm measurement node despite the docstring "deliberately NOT removed". The exporter then puts the
  `measurement` station at the stump (44.72), writes `measurement_s_mm = 49.71` in `meta.json`, and under Protocol A
  that stump is the NaN outlet (zero conductance in 0D = a wall). This is an `error_types.py`/ablation-level
  contradiction the exporter inherits — it must be settled before pre-registration, not patched here.
- **No truncation rule for the real tier.** The mask contains 47 mm of sub-cut vessel on scan 14 (3 outlet
  continuations, 1 sub-cut side branch); the package says where the outlets are but not "clip at these planes and
  remove/close everything the active centreline does not cover". Polyball has no such vessel; real lumen does. Left
  unstated it is a construction difference inside the `|polyball − real|` "geometric-reduction gap".
- **`node` columns are not vtp point ids** (`outlets.csv` node 868 in a 748-point file). Coordinates are the identity;
  say so or add a `node` array to the vtp.
- **`MaximumInscribedSphereRadius` is the pre-lesion radius** (1.108 mm at the throat where the 0D solved 0.231 mm).
  A polyball built with `vmtkcenterlinemodeller` straight from the package is the *unlesioned* tube.
- **No provenance hashes**: `meta.json` records no checksum of the source vtk/nii.gz, the frozen subset file or the
  exporter; `source.cohort` names COHORT-FROZEN for an M1 instance drawn from CFD-SUBSET. When DETECTOR §7.2 changes
  (it is provisional), nothing marks which probes.csv version a package carries.
- **No batch mode**: `--instance` indexes COHORT-FROZEN (150 rows), not the 30-row 3D subset; a wrong index exports a
  non-subset instance silently. The 300-package batch needs a `--subset` iterator keyed on (scan, side, vessel, loc,
  L, ds).

---

## Required changes

### MUST (before any package is exported to `cfd_handover/`)

1. **Strip 0D predictions from `MANIFEST.json`.** Write only the instance key (scan, side, vessel, loc, L_mm,
   ds_pct, c_mm, n_outlets, n_branch_ge_cut); never the CFD-SUBSET row wholesale. Add a unit test that greps every
   file in a package for `ffr`, `FFR` and `base_` and fails on a hit.
2. **State the coordinate frame** in `meta.json`, `mask_edit.json` and `outlets.csv`/`probes.csv` headers ("mm, LPS;
   the ImageCAS-X NIfTI affine is RAS: negate x and y before `inv(affine)`"), and put the same recipe in a package
   README. Probe: with the flip 42/42 deletion points are in the lumen; without it 0/42.
3. **Replace the T1/T2 voxel rule with a flood-fill rule.** Shipped rule on scan 14: 512 voxels removed, 67 islands
   (21 islands even at 1.5 r). Flood-fill from the same inputs — protect voxels within 1.0 r of a retained
   centreline point, then delete the connected component(s) of (mask ∧ ¬protect) containing any deleted centreline
   point — removes 855 voxels and leaves the mask as its original two components. Ship that rule text and, ideally, a
   10-line reference implementation in the package so "executable by someone with only the mask and this file" is
   literally true.
4. **Move `withheld/` out of the handover tree.** Default it to `results/cfd_withheld/<pkg>/` (or `--withheld-dir`
   required when `--with-expected` is given) and refuse to write it under `cfd_handover/`.
5. **Ship the truncation rule for the real tier** in every package: clip at each outlet plane (`outlets.csv`
   position + normal) and discard the distal component; delete or close sub-cut branches by the MUST 3 rule using
   the inactive centreline points (the exporter knows them — `~t.active`); and state that the polyball tier has
   none of this vessel by construction. The `clean_nolesion` M1 case is the right place to test the clip.
6. **No NaN in a BC file.** For an outlet with no clean counterpart (T2 stump, T4 new leaves), write the explicit
   Protocol-A rule — `closed` (wall, Q = 0), which is what `ablation.py:148` does with `w = 0` — as a `mode` column
   (`resistance` / `closed`), and assert `isfinite` on every numeric BC column before writing.
7. **Make `mask_edit.json` sufficient for T4 and unambiguous for vertex deformation.** Add a per-point
   `radial_scale = r_target / r` array to `centreline.vtp` (1 outside edits; the cosine law inside the window; 0.93 ×
   that from the taper start distally, on every descendant) and define the surface operation as "scale each surface
   vertex's distance to its nearest centreline point by that point's `radial_scale`". This single rule covers
   baseline, T3 and T4 on both tiers, makes the polyball build direct (also add `r_target_mm` = the 0D-solved
   radius), and removes the "min(r, …) applied to which r?" ambiguity in the current law string. Keep the table.
8. **Carry the Protocol C statement** (§2 above): variant, procedure, the 0D comparator, and
   `Q_clean_territory_total_mls` per territory including deleted outlets' shares; delete or correct the comment
   claiming the territory variant is runnable from the corrupted package.

### SHOULD

1. Amend CFD-ARM-SPEC §13 to say precisely what is blind: the operator can derive the clean 0D outlet pressures
   from `bc_A × bc_C_flows` (probe: exact to 4 decimals); blinding covers the corrupted-geometry predictions and ΔFFR.
2. `expected_0D.json` (withheld): record A, B, C one-scalar and C per-outlet, with the measurement node id and
   `s_mm`, so the return can be compared without re-solving.
3. `probes.csv`: add `inlet` (tree root: point 0 of the vtp, LM ostium at (20.61, −141.01, 134.45), r 1.30 mm) and
   one `outlet` row per outlet, per §11 and DETECTOR §7.2; add `s_node_mm` next to the grid `s_mm`; write the inlet
   position/normal/radius into `inlet.json`.
4. Add a `node` point array to the vtp (or rename the CSV column `tree_node` and document that it is not a vtp id).
5. Stamp provenance in `meta.json`: sha256 of the centreline vtk, the mask, the subset CSV, and the exporter file;
   DETECTOR-SPEC version for the station rule; make `source.cohort` name the file the instance actually came from.
   Make `probes.csv` regenerable alone (`--probes-only`) so a §7.2 change does not re-export geometry.
6. `m1_instance()`: say what chose the instance (80 %DS ∧ deletable branch, tie on outlets, lowest scan id) and
   consider running scan 306 as the fourth M1 case — it is the harder *edit* (bifurcation inside the window, 1.07 mm
   branch at the carina) and M1 exists to test the edit step.
7. Real-tier lesion window: instruct subdivision/remeshing of the surface inside ±L/2 to edge length ≤ r_throat/8
   (≈ 0.03 mm here) before deformation, and require the as-built throat radius check (§6.1a) on the real tier too.
8. Settle `T2_KEEP_BEYOND (15 mm) < RUNOFF (20 mm)` in `error_types.py` before pre-registration: either the
   measurement node survives (KEEP_BEYOND ≥ 20 mm, docstring true) or the measurement moves to the stump (then
   `meta.measurement_s_mm` must report the stump and Protocol A's closed stump must be declared). The exporter must
   follow, not decide.

### CONSIDER

1. A `--subset` batch mode over CFD-SUBSET keyed on (scan, side, vessel, loc, L, ds), writing one MANIFEST per stage
   with per-package hashes; `--instance` by row index is a foot-gun.
2. Average the last three edges for outlet/probe normals (one outlet has cos 0.876 with its 3-edge tangent on a
   0.43 mm last edge); harmless now, but flow-extension direction on a jittery 0.4 mm edge is avoidable noise.
3. Accept both `~/Datasets/imagecas-x` and `…/ImageCAS-X_dataset` as the data root (descend if `centerlines/` is
   absent) — the documented invocation currently fails.
4. Package-level `README.md` generated by the exporter listing files, frames, units, the truncation/edit rules and
   the acceptance checks the CFD side must return (as-meshed radius, throat radius, checkMesh), so the operator never
   has to open CFD-ARM-SPEC to run a case.

---

## Numbers that surprised me

- The 80 %DS throat on the M1 host is **0.46 mm in diameter — 1.4 voxels** on a 0.318 mm grid.
- The shipped missed-branch rule reaches **60 %** of the branch's voxels (512/855) and leaves **67 islands**.
- Deleting one 0.65 mm side branch (13 mm distal to the lesion) moves the 0D FFR at the measurement node from 0.761
  to **0.864 under B, 0.899 under C** — and C *passes* the 10 % validation check (residual 0.087) while doing it. The
  thesis, in one instance.
- T2 removes the measurement node it says it keeps (15 mm cut, 20 mm run-off).
- All six M1 outlets sit within 0.07 mm of the 0.60 mm truncation radius: the whole outlet set is at the meshing
  limit §2.4 pre-registered a fallback for.
