# CFD work order — 2026-10-03. SUPERSEDED as the entry point by WORK-ORDER-2026-10-10.md (still binding where 10-10 does not change it).


**For:** the CFD machine (the one that returned `returns/2026-09-26/` and `STAGE-A-VALIDATION.pdf` built 2026-10-03).
**Paper:** T6 (Paper 6). **Supersedes** `WORK-ORDER-2026-09-26.md` as the entry point. Everything in 09-26 and 09-24
that this file does not change is still binding: the standing rules, the resource rules, "What NOT to do" and the E0
guard.

**Standing rules (unchanged):** meshes, fields and STL files never go into Google Drive, only kilobyte files do.
Report failures and your own mistakes as results. Decide with the rules below. Do not come back for instructions
mid-task.

---

## 0. What the analysis side took from the 2026-09-26 return

Task 0, Task A and Tasks B1–B3 are all in Drive, with the numbers and the code. The analysis side checked them:

- `code_from_cfd/MANIFEST.sha256`: all 212 entries match once CRLF line endings are normalised to LF. **Write the
  manifest over LF-normalised content from now on, or state in its header that it is, so `shasum -c` passes as is.**
- D6 (a) and (b) are met: clean prescribed-flow round trip 0.0013 % max error; `as_meshed_radius_<case>.csv` returned
  for all three cases (coverage 97.7 / 98.3 / 97.7 %). The blank-radius treatment at bifurcation nodes is accepted
  as returned; no `section_valid` column is needed.
- The as-meshed radii were ingested analysis-side. That comparison stays analysis-side, because scan 14 is a cohort
  scan (no 0D predictions for cohort scans, 09-24 §7).
- The B3 two-state finding is a good catch and is accepted as a result.

---

## 1. Analysis-side decisions (binding from now on)

**D7: M1 and the 2 mm rule. Baseline and T1 fail D3/D4 as measured. M1 becomes a PASS only through a declared
deviation backed by a sensitivity test (Task A below). It does not pass by relaxing the rule.**
Reasons: the flagged entities are low-quality face-tet decompositions, the clean mesh carries the same count
(1025 vs 1058 / 977), standard `checkMesh` is clean on all three, and baseline and T1 share one lesion build. That
makes this a property of the mesher, not of the mask. But the rule was set before the result, so a change to it
must rest on evidence, not on the explanation. The deviation is written in the paper.
Acceptance: the measurement-probe FFR of the re-meshed baseline differs from the returned value by
**less than U₃D (0.00055)**, and no flagged entity lies within 2 mm of the throat or the measurement probe on the
re-meshed case. If the re-mesh still has flags within 2 mm, but the FFR difference is below U₃D, report it, and
M1 is PASS WITH DEVIATIONS D2/D3/D4 + D7. If the FFR difference is ≥ U₃D, M1 fails for the lesion cases and the
§9 fallback discussion opens. Do not repair the surface in either case.

**D8: B1 proxy is NOT authorised as a stopping rule.** The production template gets a measurement-probe
function object (area-averaged p on the measurement section, written every iteration) and a throat one. The
SETTLED rule is applied to that series as specified in 09-26 §5 B1. Until a production case has a measurement-probe
history, every solve runs to the full budget. For prescribed-flow solves the outlet-pressure band replaces the
outlet-flow band (accepted, because flows are imposed). The BC-error criterion is not applicable for those solves.

**D9: U₃D stays provisional until Task B.** Report it as 0.00055 (provisional) everywhere it appears.

**D10: no CFD-side change to the lumen-radius definition.** The as-meshed lumen is wider than the package radius
(median +0.14 mm along the tree, throat area-equivalent 0.2756 vs 0.2306 mm). The analysis side compares 3D against
twins rebuilt on the as-meshed radius, as D2 already provides. Keep returning both the area-equivalent and the
inscribed radius files for every case.

---

## 2. TASK A (required, first): the D7 sensitivity test

Scan 14 baseline only, resistance mode, production recipe (D1), **with fields kept**.
1. Re-mesh with the throat zone at 12.5 µm (±4 mm) instead of 25 µm. Keep everything else in the recipe.
   If the flagged face-tets still lie within 2 mm of the throat, also try the zone-B interface shift you used in
   the U₃D ladder. Report both, and do not search beyond these two variants.
2. Run `checkMesh -allGeometry -allTopology -writeSets vtk`, and report the counts and distances in the
   `M1_geometry_gates.csv` format (new dated file).
3. Solve with the D8 probe function objects. Report FFR at the measurement and throat probes, outlet flows, the
   flow state (axisymmetric or deflected jet, as in B3), and the difference from the returned baseline.
4. Return `M1_D7_sensitivity.csv` plus one paragraph in `NOTE.md`.

## 3. TASK B (required): make U₃D final

Re-run the S12A, S12B and S25B levels of the sten70 ladder with fields kept, and record the jet state of each.
Recompute GCI₂₁ for both families. If all five levels are on the axisymmetric state, U₃D becomes final. If any level
is on the deflected state, report the ladder per state, and do not mix them.

## 4. TASK C (required): production template

Add the D8 function objects to the production case template and the end-to-end runner. Prescribed-flow runs keep a
minimum of 800 iterations (your B1 observation). Push the template and runner changes to `code_from_cfd/` with the
manifest regenerated.

## 5. TASK P5 (required, after Task C): five-case baseline pilot

Five new cohort cases, **baseline geometry only, one resistance-mode solve each** (bc_A). Packages are in
`packages/P5/` (five folders, same format as M1, no predictions inside):

| package | vessel | lesion |
|---|---|---|
| `138_left_LAD_prox_20mm_70ds__baseline__real` | LAD | 20 mm, 70 %DS |
| `69_left_LCX_prox_20mm_65ds__baseline__real` | LCx | 20 mm, 65 %DS |
| `473_left_LCX_prox_20mm_60ds__baseline__real` | LCx | 20 mm, 60 %DS |
| `272_right_RCA_prox_10mm_65ds__baseline__real` | RCA | 10 mm, 65 %DS |
| `139_right_RCA_prox_10mm_70ds__baseline__real` | RCA | 10 mm, 70 %DS |

The analysis side chose these by a fixed rule written down before any solve. Run them in the order listed.
1. Build, mesh and solve with the production recipe (D1) and the Task C template (probe function objects on).
   Apply the D2 relative throat gate, and report the D3/D4 distances. **Do not repair.** A case that fails a gate is
   still solved and returned, flagged.
2. Return, per case: `as_meshed_radius_<case>.csv` **and** `_inscribed.csv`, `M1_probes`-format and
   `M1_outlets`-format CSVs, a `M1_results`-format row, the measurement-probe history (for B1), wall-clock and
   cells. Name the folder `returns/2026-10-03/P5/`.
3. These solves are production baselines. They will be reused in the batch, so keep the case directories (not in
   Drive) until the batch list arrives.

Budget: about 2.5 h per case on 16 ranks, about 12 h in total. If a case has not settled by the 3000-iteration
budget, return it as unsettled and move on.

## 6. TASK D (when the host can be made quiet): B2 replicate

Repeat B2 under the strict isolation rule: auto-updates and unattended-upgrades off, no interactive session on the
host, the other project paused, both run orders (L16 first, then L8×2 first). Stop at the D8 rule if Task C is done,
otherwise at the fixed iteration used in B2. The ratio is claimed only if all four runs are VALID.

---

## 7. Still on hold, and what not to do

- Stage B, C and D batches stay on hold until M1 is settled (Task A), U₃D is final (Task B) and the analysis side has read the P5 pilot.
- Everything in 09-24 §7 and 09-26 §6 still applies: no new work on scan 837, no 0D predictions for cohort scans, no
  case selected from `E0_prevalence_test.csv`, no meshes, fields or STL files in Drive.
- Re-issued CSVs get a dated suffix. Do not overwrite.

**Order:** Task A → Task C → Task P5 → Task B → Task D (P5 needs the Task C template; B is not needed before the pilot). Return into `returns/2026-10-03/`.
