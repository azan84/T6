> **⚠ SUPERSEDED as the entry point on 2026-09-26: read `WORK-ORDER-2026-09-26.md` first.** This file stays binding
> wherever 09-26 does not change it: its standing rules, §6 resource rules, §7 "What NOT to do" and the E0 guard.

# CFD work order — 2026-09-24.

**For:** the CFD machine (the one that produced `STAGE-A-VALIDATION (2).pdf`, 41 pp., built 2026-09-24).
**Paper:** T6 (Paper 6). **Supersedes** `WORK-ORDER-2026-09-19.md` as the entry point. That file is kept for its
physics constants, per-case relax table and background, which remain correct.
Full specification: `../protocol/CFD-ARM-SPEC.md` (§6.2 production meshing, §7 Gate M1, §12 returns, §13 blinding).

**Standing rules (unchanged):** meshes, fields and STL files never go into Google Drive, only kilobyte files do.
Report failures and your own mistakes as results, as the last report did. Decide with the rules below; do not come
back for instructions mid-task.

---

## 0. What the analysis side took from the 2026-09-24 report

Very good work: the M1 root cause (the `vmtksurfaceremeshing` coarsening pinch), resistance BCs on a real 5-outlet tree
to machine precision, Item 5 RCR PASS, and lesion80 with an audited launch. Thank you. Four things are still missing,
and they are why this work order exists:

1. **Nothing has come back to Drive.** `returns/` still holds only the two templates. `bc/resistanceOutlet.md` in Drive
   is still the pre-fix version and `stageA/caseTemplate/` does not exist in Drive. Every number in the report exists
   only as PDF text and on your disk. **This is Task 0 and it comes first.**
2. **The 3D FFR discretisation uncertainty U₃D still does not exist.** Task 1 of 09-19 (sten70 at *production*
   resolution) was not run. The 4-level sten70 result in §11.3 is the one 09-19 already cited. The statistics plan has a
   pre-registered rule that waits on this number (`protocol/STATISTICS-PLAN.md`, "PRE-REGISTERED CONTINGENCY on the 3D
   discretisation floor"). It is still the single most valuable number you can return.
3. **Gate M1 has not been run on the study's own packages.** All real-lumen work used **scan 837, which is not in the
   frozen cohort** (`protocol/COHORT-FROZEN-2026-09-18.csv`). The shipped packages (`packages/M1/`, **scan 14**, which
   is in both the cohort and the CFD subset) are still unattempted. The 837 work is a valid *pipeline* pilot. It does
   not pass M1.
4. **Prescribed-flow outlet mode has never been run on a multi-outlet tree.** Item 1 and Item 3 ran both relax code
   paths, but both are *resistance* mode. Protocol C in 3D prescribes every outlet's flow at once. If that is unstable,
   the replication arm changes shape. It is part of the M1 pass criterion, not an extra.

---

## 1. TASK 0 (required, first, minutes): return the code and the numbers you already have

No new compute. Create `returns/2026-09-24/` and `code_from_cfd/`, then copy these into Drive.

### 0a. Code into `cfd_handover/code_from_cfd/` (kilobytes; the paper's code deposit needs them)
- `bc/resistanceOutlet_steady.md`: the `simpleFoam` version with `p.prevIter()` relaxation, **plus** the note that
  `p` must be listed under `relaxationFactors` or `prevIter()` FatalErrors.
- `bc/resistanceOutlet_transient.md`: the `pimpleFoam` direct-impose version (`operator==(pTarget)`).
- `bc/rcrOutlet.md`: the Crank–Nicolson RCR BC from Item 5.
- `stageA/make_stageA_geometry.py` (wall normals fixed) and `stageA/caseTemplate/` (the full skeleton, including the
  `div((nuEff*dev2(T(grad(U)))))` entry and the `(U|UFinal)` solver entry).
- The Item 1 branched-tree generator and its clearance check.
- The **real-lumen pipeline** as it now works: mask isolation, marching cubes, Taubin smoothing, outlet clip, planar
  extrusion and capping (the rebuilt path that **skips** `vmtksurfaceremeshing`), and the lesion deformation (edge-split,
  raised-cosine, with its geometry gates). Also: the auto-relax generator (Gᵢ = Rᵢ/R_own,i from the 0D tree), the 0D
  leaf-to-patch matcher with its 3 mm assertion, the pullback and section-averaging script, the WSS/recirculation
  script, the audited launch script and the (fixed) convergence watcher, and the mesh-sensitivity analysis script
  (frozen version).
- A `code_from_cfd/README.md` of about 20 lines: what each file is, which OpenFOAM version (ESI v2406), and which report
  section it produced.

Do **not** overwrite the old Drive copies. Put the new files beside them under `code_from_cfd/`. The analysis side
will reconcile.

### 0b. Numbers into `cfd_handover/returns/2026-09-24/`, one CSV per table, with a header row and SI or stated units
| File | Content (report section) |
|---|---|
| `stageA_summary.csv` | A1–A5 all cases: cells, checkMesh stats, iterations, Q, p_outlet, FFR at x = 56.5 mm, residuals, throat Re, wall-clock, cores (§2–§9) |
| `stageA_A2_sweep.csv` | six severities 0/50/60/65/70/80: 3D Q, 0D Q, gap, 3D FFR, 0D FFR, cells (Table 5) |
| `stageA_A5_ladders.csv` | sten70 four levels + sten80 three levels: cells, **cells across throat (measured)**, BL settings, FFR mean and band (Tables 3, 6) |
| `item1_tree.csv` | per outlet, both severities: R, relax, 3D Q, 0D Q, BC error (Table 4) |
| `item3_837_outlets.csv` | baseline, missed-branch, extcomp, lesion80, reference: per-outlet R, relax, Q, p/P_aorta, BC error, 0D Q (Tables 7, 9) |
| `item3_837_pullback_<case>.csv` | per centreline station: path id, arc s, 3D section area, **3D area-equivalent radius**, **0D node (EDT) radius**, 3D section-mean p/P_aorta, 3D section flux, 0D p/P_aorta |
| `item3_837_lesion80_wss.csv` | Table 11 at every 0.25 mm slab (not only the selected stations) |
| `item3_837_timing.csv` | per solve: cells, ranks, physical cores, peak RAM, iterations, wall-clock, whether the machine was contended |
| `item5_rcr.csv` | cycle-2 max and mean error, samples, backflow samples |
| `item6_cost.csv` | the isolated pre-contention timing: cells, cores, Δt, wall-s per step, Courant, projected hours |
| `failures.csv` | every mesh or solve failure so far: case, stage, symptom, what was ruled out, final cause (spec §12 treats this as a finding) |
| `NOTE.md` | one page: anything in the CSVs that needs a caveat |

**The two radius columns in `item3_837_pullback_*.csv` are the most important thing in 0b.** The report's finding
that the 3D area-equivalent radius exceeds the 0D EDT radius by 23–44% changes how the analysis side builds every 0D
twin. The analysis side needs the raw per-station numbers, not the path means.

---

## 2. TASK 1 (required): U₃D, the 3D FFR discretisation uncertainty

### What changed since 09-19
Your own §11.3 names the likely reason sten70 did not converge: **the boundary-layer stack was held constant across
levels**, so the ladder was not a single-parameter refinement family. Your lesion80 sensitivity design already fixes
that (cfMesh 2× quantised sizes, BL stack scaling with cell size, measured cell sizes). Apply the same method to sten70.

### Run
1. **sten70, 3D, three levels, refinement ratio exactly 2** in the lesion zone (cfMesh quantises to 0.2 mm/2ⁿ). Use
   throat-zone cell sizes of **50 / 25 / 12.5 µm**. 50 µm is the production base: sten70's throat is 0.891 mm, so
   50 µm gives about 18 cells across, and ≥ 12 is required. Scale the BL stack with the cell size (same number of
   layers, same ratio, first-layer thickness proportional to cell size). Keep the zone extents identical across levels.
   If 12.5 µm over the whole lesion ±2 lengths exceeds RAM, refine a throat zone only, as T25a/T25b did, **and** run a
   second throat zone with shifted interfaces so interface contamination can be tested. Measure and report the
   achieved cells across the throat and the p95 cell size. Do not assume either.
2. **sten70, 2D axisymmetric wedge, four or more levels, ratio 2** (Fable's ~37k-cell suggestion). This is cheap. It
   answers the physics-versus-discretisation question for the same geometry with a clean systematic family and a
   proper Celik GCI. It is the cross-check, not the primary number.
3. Same BCs as before: coded resistance R = 6.974826 × 10⁹, relax 0.20, initial 8.0694, inlet `totalPressure` 11.3198.
   Use a fixed iteration budget, not `residualControl`. Report the last-100 mean FFR at x = 56.5 mm and its band,
   outlet Q, throat Re, cells, cells across throat, checkMesh summary, wall-clock, cores and RAM.
4. If budget remains, run **sten80** on the same 3D recipe. Its A5 "pass" was at about 6 cells across, half the
   required resolution.

### Decide without coming back
- **3D successive differences shrink, and the finest pair is < 0.005** → PASS. Report U₃D from Celik GCI on the three
  3D levels. Those production settings become the study recipe.
- **3D differences still flat, but the wedge converges cleanly** → the 3D drift is a meshing artefact (interfaces,
  cfMesh transition cells). Report both. Report U₃D as the 3D finest-pair difference, not the wedge GCI, and describe
  what you think causes it.
- **Both flat** → run time-accurate `pimpleFoam` on the finest 3D mesh (use the transient BC). Time-average FFR over the
  last stable window and report the mean and band. Stop there.
- **In every case, return one number, U₃D, with the sentence that defines it.** If U₃D ≥ 0.005, say so plainly. The
  analysis side has a pre-registered rule for that case, so a large number is not a failure to hide.

Return: `returns/2026-09-24/U3D_sten70.csv` (+ `U3D_sten80.csv` if run), with a verdict line at the top of `NOTE.md`.

---

## 3. TASK 2 (required): finish the lesion80 mesh-sensitivity study on scan 837

The W100 / T25a / T25b meshes are built and audited and the rules are pre-registered. When the runs finish, apply
the frozen analysis script unchanged and return `returns/2026-09-24/lesion80_sensitivity.csv`: the ten quantities ×
four levels, and the label for each (INSENSITIVE / NON-MONOTONE / INTERFACE-CONTAMINATED / SENSITIVE / UNASSESSABLE).
Do not change the rules or the tolerances after seeing the numbers. If a solve is unconverged, it is UNASSESSABLE.
Report it as such.

This is the first real-lumen resolution evidence. After this, **stop new work on scan 837**. It is outside the cohort.

---

## 4. TASK 3 (required): Gate M1 on the shipped scan-14 packages

`packages/M1/` has three cases on scan 14 (clean_nolesion · baseline = 80 %DS lesion · T1_missed_branch = lesion **and**
a deleted side branch). Scan 14's cohort FFR is 0.799, on the decision threshold. That is deliberate: the missed-branch
case is the paper's decision-flip test in miniature.

### Build: use the working 837 pipeline, with the package's own rules
- Run the **E0 guard** membership assertion (§7) first. Scan 14 left passes it.
- Read `packages/M1/README.txt`, then each package's `README.md`.
- **Frame:** mm, LPS. The NIfTI affine is RAS, so negate x and y before `inv(affine)`. The check is 42/42 deletion
  points inside the lumen.
- **Mask deletion: 6-connected, protect radius 1.10 r, run once over the union of truncation and branch sets.** Use
  the reference implementation in `mask_edit.json`. On 837 your own deletion eroded the parent LAD by up to 0.24 mm
  over 35 mm. The shipped rule measures about 40 voxels of erosion on scan 14. Report the erosion you get: voxels
  removed, and the parent radius change along the LAD from the pullback.
- **No `vmtksurfaceremeshing`** unless its target edge is ≤ r_min/3 **and** a pre/post cross-section deviation gate
  passes (your own §11.5 lesson). Default: skip it, as the rebuilt 837 path does.
- **Lesion:** subdivide the lesion window to edge ≤ r_throat/8 **before** deforming. Scan 14's `r_target_mm` minimum is
  **0.2306 mm** (throat diameter 0.46 mm, much tighter than 837's 0.75 mm). Check the as-built throat against
  `r_target_mm`: **reject if > 1 %**. Run your 837 geometry gates (ownership, fold-over, self-intersection with the
  positive control).
- **Throat resolution:** ≥ 12 cells across a 0.46 mm throat needs ≤ 38 µm, which is the **25 µm** cfMesh level. Use a
  throat zone as in T25a/T25b if the full window will not fit in RAM. Measure cells across.
- **Flow extensions:** spec §6.2 says 5 D at the inlet and 3 D at each outlet. The 837 pilot used 20 mm, and your
  extcomp diagnostic showed the extension resistance is not negligible. **Use the spec lengths.** Record the actual
  length per outlet in the return. If you have a reason to keep 20 mm, keep it, record it, and say why in `NOTE.md`.
- **Boundary layers:** spec says 4 layers, ratio 1.2 (lesion80 used 3). Use 4, or state why not.

### Solve: both BC modes
1. **Resistance mode** using `bc_A.csv`. Take relax from the Gᵢ = Rᵢ/R_own,i rule. `bc_A.csv` `mode = closed` means
   the outlet is a **wall**, not an outlet.
2. **Prescribed-flow mode, ALL outlets prescribed simultaneously**, with a `totalPressure` inlet and flows from
   `bc_C_flows.csv`. Derive R_i = (p̄_i − P_v)/Q_i per outlet, then re-solve in resistance mode with those R_i.
   **Pass: every outlet's flow reproduced within 0.5 %.** This is Protocol C's mechanism on a multi-outlet tree and has
   never been run. **Run it first on the Item 1 branched tree** (370k cells, known good) before scan 14, so a failure
   there is cheap and diagnosable. Label the T1 prescribed-flow run PILOT (its targets are provisional).
3. Record throat Re for every solve. If steady laminar will not converge, use the `pimpleFoam` time-average fallback
   and report the case separately. **Never switch to a turbulence model.**

### Blinding (spec §13), applies from now on
The scan-14 packages deliberately contain **no 0D prediction**. **Do not run `zerod_ffr.py` or any 0D twin on scan 14**
and do not put 0D predictions for it in the report. The analysis side computes them after your CSV arrives. On 837
you built your own 0D twin, which was fine for a pipeline pilot but is not allowed for cohort cases.

### Pass / kill (unchanged)
- **Pass:** all three cases give a checkMesh-clean mesh and a converged solve, with **no manual geometry repair**. Both
  BC modes are stable, the round trip is within 0.5 %, and as-meshed radius is returned.
- **Kill:** 5 working days without a scriptable path → spec §9 fallback. **Report days consumed so far** (837 work
  counts toward it; state your own accounting).

### Return
- `returns/2026-09-24/M1_results.csv` from `M1_results_TEMPLATE.csv` (one row per case × BC mode). Add columns
  `extension_lengths_mm`, `n_bl_layers`, `throat_cell_um_p95`, `peak_ram_gb`, `physical_cores`, `roundtrip_max_err_pct`.
- `returns/2026-09-24/as_meshed_radius_<case>.csv`: per centreline node of `centreline.vtp` (same node ids): arc s,
  **3D area-equivalent radius**, **max-inscribed (EDT-equivalent) radius** of the same meshed section, section area.
  Send it even if the solve fails.
- `returns/2026-09-24/M1_probes_<case>_<mode>.csv`: area-averaged p **and** through-plane flux at every probe in
  `probes.csv`.
- `returns/2026-09-24/M1_outlets_<case>_<mode>.csv`: per outlet R used or derived, Q, p̄.

---

## 5. TASK 4 (optional, only if Tasks 0–3 are done): pulsatile cost

Stage D stays on hold, so do **not** run the 30–40 h campaign. Take one clean, **uncontended** timing on sten60: at
least 200 timesteps at Co 3–5, 8 physical cores. Report wall-s per step and projected hours per cycle. That replaces
the pre-contention estimate.

---

## 6. Resource rules (from your own §11.7 incident)

- The host has **16 physical cores**. Plan against 16, not the 32 that `nproc` reports.
- **Total solver ranks across all concurrent jobs ≤ 16.** Launch jobs sequentially unless the sum of ranks fits.
  Consider `--bind-to core` and yielding-when-idle MPI settings.
- One coordinator owns the core budget. Sub-agents or forks must not launch solves without checking the live load
  first.
- Mark any timing taken under contention as contended in `*_timing.csv`.

---

## 7. What NOT to do

- Do not start the study batch (Stages B, C, D). It is still on hold for the analysis-side re-cut.
- Do not run the sten80 `pimpleFoam` stall diagnostic. It is closed by decision (report §8).
- Do not do new work on scan 837 beyond Task 2.
- Do not compute 0D predictions for any cohort scan (§4, blinding).
- Do not put meshes, fields or STL files into Drive.
- **Do not select or gate any case from `results/E0_prevalence_test.csv`.** See the E0 guard below.

### E0 guard (added 2026-09-24, after an independent audit)
`E0_prevalence_test.csv` is a **leaky-bed prevalence screen**. Its `min_ffr_main` is FFR on the tree **as segmented**
(native lesions included) under `bed="leaky"`. It is **not** the discrete healthy-network gate (`healthy_main_ffr`
under `bed="discrete"`). The two disagree often: **34 of 108 cohort trees pass ≥ 0.90 on E0 but fail the discrete
gate.** Rules:

1. **The only source of cohort cases is `protocol/CFD-SUBSET-FROZEN-2026-09-18.csv`**, or a package already built
   from it (`packages/`). Its `healthy_main`, `base_discrete` and `ffr_discrete` are the discrete-bed gate values.
   Do not recompute them and do not substitute other values.
2. **Before building any case, assert membership.** Stop if the assertion fails:
   ```python
   import csv
   sub = {(r["scan"], r["side"]) for r in csv.DictReader(open("protocol/CFD-SUBSET-FROZEN-2026-09-18.csv"))}
   assert (str(scan), side) in sub, f"{scan}-{side} is not in the frozen CFD subset — do not run it as a cohort case"
   ```
3. **Pipeline or debug cases outside the subset** (scan 837, for example) may be used only as pilots. Label them
   `PILOT_OUT_OF_COHORT` in every return file and every report table. Never mix them into cohort results.
4. If you need a discrete gate value for a scan outside the subset, compute it with
   `Tree(..., bed="discrete").healthy_main_ffr()` (murray, scale 1.0), and label it by that exact name. Never label
   `min_ffr_main` as a healthy-network value.

---

## 8. Corrections for the next version of the report

These are documentation issues. None changes a number. Fix them when the report is next rebuilt.

1. **The report now contradicts itself on sten70 A5.** The abstract ("8 of 8 pass/fail checks pass"; "A5 passes for
   both sten70 … and sten80"), §2's running summary and §12 all still read A5-sten70 as PASS. §12 also says whether
   sten70 "would survive a fourth, finer mesh level" is open, but §11.3 answered it: GCI not trustworthy. State
   A5-sten70 as **NOT ESTABLISHED** everywhere, and change "8 of 8" to "7 of 8, one not established".
2. The abstract says the resistance BC has confirmations "across five distinct cases", while §12 says "four". Items 1
   and 3 add a 3-outlet and a 5-outlet tree. Recount and state it once.
3. §11.4 says the Item 6 runs "are running". §11.7 says they were stopped. State that they were stopped.
4. The lesion80 text says **"resting (not hyperaemic) flow"**. The study's Murray demand is hyperaemic by definition
   (`code/zerod_ffr.py:59`, `K_MURRAY = 562 s⁻¹`, "hyperaemic Q = k r³"). If Q_demand = 0.6636 mL/s came from that
   constant, the flow is hyperaemic by the study's convention. Relabel it, and state the inlet radius used. If a
   different k was used, state which one.
5. Say explicitly that **scan 837 is outside the frozen cohort**: it is a pipeline pilot, not a Gate M1 result.
6. The title block still reads "2026-09-18 to 2026-09-19" and the running header is truncated ("in progre"). The
   document covers work to 2026-09-24.
7. Consider splitting the report: a closed Stage A report (§1–§10), and a separate, dated pilot report (§11). The
   combined "Final Report" title no longer fits a document that is 60 % in-progress pilot work.
8. **§11.5, the scan 828/837 selection: the gate is misnamed.** An independent recompute (2026-09-24) reproduced
   0.845 (828) and 0.9813 (837) exactly. Both are the **discrete-bed min-FFR on the network as segmented**
   (`min_ffr_main`), not the healthy-network gate (`healthy_main_ffr`). Under the actual gate, 828-left scores
   **0.9127, which passes**. 828 was still a poor clean-baseline pilot: it has 5 native lesions (max 44.6 %DS). Reword
   it that way. `E0_prevalence_test.csv` is a leaky-bed prevalence screen, not a selection file. Cohort cases come
   only from `protocol/CFD-SUBSET-FROZEN-2026-09-18.csv`, which is correctly gated under the discrete bed.
9. Record the deviations from spec §6.2 wherever they apply: 3 boundary layers instead of 4, 20 mm extensions instead
   of 3 D, and the validation-pass meshes below the ≥ 12 cells-across rule.

---

## 9. Priority if time runs short

Task 0 → Task 1 (U₃D) → Task 3 prescribed-flow round trip on the Item 1 tree → Task 3 scan-14 resistance mode →
Task 2 → Task 3 scan-14 prescribed-flow → Task 4. Work down this list, not across it.
