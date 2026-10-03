> ## ⚠ SUPERSEDED as the entry point — read `WORK-ORDER-2026-10-03.md` first (then `WORK-ORDER-2026-09-26.md` and `WORK-ORDER-2026-09-24.md`, which it extends, and `WORK-ORDER-2026-09-19.md` for background).
> Stage A **has been run** (2026-09-18/19, OpenFOAM ESI v2406): 8 of 8 pass/fail checks pass and the coded
> resistance-outlet BC is confirmed on real hardware. This file still describes Stage A as if it were unrun, and its
> `relax` guidance has been superseded by a measured per-case table. It is kept for the geometry, probe positions,
> expected 0D values and BC background, which remain correct.

# CFD machine — start here

**For:** the 16-core CFD PC. **Paper:** T6 (Paper 6). **Full specification:** `../protocol/CFD-ARM-SPEC.md` (v0.2).
**This folder is the only thing the CFD machine needs from Google Drive.** Everything in it is kilobytes.
**Rule:** meshes, fields and STL files stay on the CFD machine's local disk. **Never write them into Google Drive.**
Only small CSVs come back (into `returns/`).

## What this arm is for, in one line
Show that the paper's effect — boundary conditions tuned to match their flow targets while the FFR ≤ 0.80 decision still
moves — exists at 3D fidelity on real lumens, not only in the 0D model.

## What you can do today, without waiting for anything
### Step 1 — install
OpenFOAM (record exact version and whether it is the .com/ESI or .org/Foundation line — the coded-BC API differs),
cfMesh (`cartesianMesh`) or snappyHexMesh, VMTK (conda: `conda install -c vmtk vmtk`), ParaView, Python 3 + numpy.
Check RAM: plan ≥ 2 GB per million cells per job; two 8-core jobs run side by side.

### Step 2 — generate the Stage A test geometry (local disk, NOT Drive)
```
python3 stageA/make_stageA_geometry.py ~/cfd_t6/stageA
```
Writes `pipe.stl`, `sten00.stl`, `sten50.stl`, `sten70.stl`, `sten80.stl` — metres, multi-solid ASCII STL with solids
`inlet`, `outlet`, `wall`. Validated 2026-09-18: all five watertight and manifold; throat radii 1.4850 / 0.7425 / 0.4455
/ 0.2970 mm. Files are 34–39 MB each (≈ 190 MB total), which is why only the generator is in Drive.

### Step 3 — run the four Stage A checks (spec §8)
Fluid: laminar, Newtonian, ρ = 1060 kg m⁻³, μ = 0.004 Pa s → **ν = 3.774e-6 m² s⁻¹**. Rigid no-slip wall. `simpleFoam`.
OpenFOAM pressure is kinematic: divide Pa by ρ. P_aorta = 11 998.98 Pa → **11.3198 m² s⁻²**; P_venous = 666.61 Pa → 0.62888.

| # | Case | Boundary conditions | Compare with (`stageA/expected_0D.csv`) | Pass |
|---|---|---|---|---|
| A1 | `pipe` | inlet: parabolic or uniform velocity for Q = 1.5 mL/s (1.5e-6 m³ s⁻¹); outlet: fixed pressure | ΔP between x = 60 and 90 mm = **90.54 Pa** (Poiseuille) | within 1 % |
| A2 | `sten00/50/70/80` | inlet `totalPressure` = 11.3198; outlet **resistance BC** with that case's `R_out_SI` (≈ 6.975e9 Pa s m⁻³) | 0D-discrete FFR at x = 56.5 mm: **0.983 / 0.946 / 0.754 / 0.485**; flows 1.50 / 1.44 / 1.13 / 0.69 mL/s | **no pass/fail** — tabulate the gap; it is a result about the 0D lumped stenosis model |
| A3 | resistance BC (on A2) | — | at convergence p_outlet = P_v + R·Q | within 0.1 % |
| A4 | round trip (on `sten70`) | solve with **prescribed outlet flow** = the A2 converged flow; read p_outlet; derive R = (p − P_v)/Q; re-solve with that R | second solve reproduces the prescribed flow | within 0.5 % |
| A5 | mesh independence (`sten70`, `sten80`) | three refinement levels | FFR at x = 56.5 mm | < 0.005 between the two finest |

Probe planes (x, mm): inlet −10 · proximal 20 · throat 31.5 · **measurement 56.5** · outlet 95. Report the
**area-averaged static pressure on the cross-section**, not a point value. FFR = p̄ / P_aorta.
Mesh guidance: base cell ≈ D/20; refine the lesion ± 20 mm so the throat has **≥ 12 cells across** (the 80 % throat is
0.594 mm in diameter → cells ≤ 0.05 mm there); 4 boundary layers, growth 1.2. Expected throat Reynolds numbers are
170–430, so laminar is appropriate; record Re for every run.
A4 matters most: it is the mechanism by which Protocol C is tuned *inside* the 3D model for one extra solve.

### Step 4 — the resistance outlet
`bc/resistanceOutlet.md` has a `codedFixedValue` template. **It is UNTESTED** — it was written on a machine with no
OpenFOAM. Treat A3 as its acceptance test, and send back whatever you had to change.

**Two corrections were made to that file on 2026-09-19 — use the current version, and note both:**
1. **The under-relaxation is a stability bound, not a preference:** `α < 2/(1 + R_outlet/R_epicardial)`. The original
   template's `0.2` **diverges** on `sten00` (bound 0.134). Default is now **0.05**.
2. **Run A3 on `sten00` FIRST.** Counter-intuitively the *mildest* case is the hardest for this BC — least epicardial
   resistance means the largest R_outlet/R_epi and the tightest stability bound. If `sten00` is stable, the rest are.

Also: the template previously said to prescribe all but one outlet in flow-prescribed mode. **That was wrong** —
with a `totalPressure` inlet, prescribe every outlet. A free outlet would absorb the whole flow discrepancy, which is
the exact effect this study exists to measure.

### Step 5 — send back
Fill `returns/stageA_results_TEMPLATE.csv` (save as `returns/stageA_results.csv`). Also note: OpenFOAM version, cores
used, wall-clock per case, cells per mesh. Those timings replace the estimates in spec §4 and set the study's case count.

## Gate M1 — READY 2026-09-19, in `packages/M1/`
Three real-lumen cases on scan 14 (clean lumen · 80 %DS lesion · missed side branch). M1 tests the one risky step —
turning an edited CT lumen mask into a meshable surface with no manual repair — and has a hard 5-working-day kill
with a pre-agreed fallback (spec §7, §9). **Read `packages/M1/README.txt` first**; each package then has its own
`README.md` with the frame, build order and return set.

Two things in there that will bite if skipped, both measured on that scan: the coordinate frame is **mm, LPS while
the NIfTI affine is RAS** (negate x and y — with the flip 42/42 deletion points land in the lumen, without it 0/42),
and the mask deletion rule is **6-connected with a 1.10 r protect radius** (26-connectivity erodes the retained
vessel by ~1300 voxels instead of ~40).

**M1 can run alongside Stage A — they are independent.** If you have only one pair of cores free, Stage A first:
it proves the solver setup, and the resistance BC is still untested.

- Then the study batches: Stage B polyball tier → Stage C real-lumen tier → Stage D pulsatile figure (spec §5).

## Folder map
```
cfd_handover/
  START-HERE.md                       this file
  stageA/make_stageA_geometry.py      analytic test surfaces (numpy only)
  stageA/expected_0D.csv              BC values to impose + 0D-discrete pressures to compare
  bc/resistanceOutlet.md              coded outlet BC template (UNTESTED)
  returns/stageA_results_TEMPLATE.csv what to send back
  packages/                           case packages will appear here (M1 first)
```
