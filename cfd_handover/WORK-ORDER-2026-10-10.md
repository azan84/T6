# CFD work order — 2026-10-10. Read this before anything else in this folder.

**For:** the CFD machine(s). A second machine may take tasks in parallel; see the split in §6.
**Paper:** T6 (Paper 6). **Supersedes** `WORK-ORDER-2026-10-03.md` as the entry point. Everything in 10-03, 09-26
and 09-24 that this file does not change is still binding: the standing rules, the resource rules, "What NOT to do",
the E0 guard, D1–D10, the Task C template and probe function objects.

**Standing rules (unchanged):** meshes, fields and STL files never go into Google Drive, only kilobyte files do.
Report failures and your own mistakes as results. Decide with the rules below. Do not come back for instructions
mid-task.

---

## 0. Why these runs

The paper is being submitted with the reduced-order (0D) results and one 3D case (scan 14, missed branch, resistance
and prescribed-flow outlets). Since 10-03 the paper has gained a fifth error type, **T5: the stenosis throat diameter
read half a voxel too narrow or too wide**, which changes the decision about as often as the topological errors. It
has no 3D evidence yet. The paper's central claim (a model tuned to perfusion can pass the check while its FFR is
wrong) is also shown only in 0D, and the 3D comparison covers one instance. These tasks address all three.

## 1. Analysis-side decisions (binding from now on)

**D11: M1 for the lesion cases is accepted WITH DEVIATIONS D2/D3/D4 + D7.** The 12.5 µm throat-zone sensitivity of
0.0019–0.0021 (Task A of 10-03; control A0 = 0) is reported in the paper as the 3D resolution uncertainty for lesion
cases. The production recipe (D1, 25 µm throat zone) stays the recipe. Do not repair surfaces.

**D12: the 10-03 hold on new 3D cases is lifted for the packages listed in §2 only.** Stage B/C/D batches stay on hold.

**D13: T5 packages are built exactly like the others.** The only difference from the baseline package of the same
instance is `r_target_mm` / `radial_scale` at the 34–44 centreline points inside the lesion window: the throat radius
is changed by a quarter of the scan's in-plane voxel spacing (half a voxel in diameter). Topology, outlets, `bc_A`,
`bc_C_flows`, territories and probes are identical to the baseline package. The §6.1a 1 % throat check applies to
the new `r_target_mm`.

**D14: thin throats.** The narrow T5 variant of scan 14 has a target throat radius of 0.151 mm. Build it with the
production recipe like every other case, and in addition run the one extra solve listed in Task T (step 4) at the 12.5 µm
throat zone, paired with the 10-03 A1 baseline (also 12.5 µm). The narrow variants of scans 138, 306 and 473
(0.18–0.51 mm) use the production recipe only.

**D15: Reynolds number.** Narrow throats raise the throat Reynolds number. Record it for every solve. If steady
simpleFoam does not settle within the budget, use the agreed pimpleFoam time-average fallback and flag the row. Do
not change the turbulence model.

---

## 2. Packages: `packages/WO1010/` (14 folders, same format as M1 and P5, no predictions inside)

| package | needed by |
|---|---|
| `14_left_LAD_prox_20mm_80ds__T5_vox_narrow__real` | Task T |
| `14_left_LAD_prox_20mm_80ds__T5_vox_wide__real` | Task T |
| `138_left_LAD_prox_20mm_70ds__T5_vox_narrow__real` | Task T2 |
| `138_left_LAD_prox_20mm_70ds__T5_vox_wide__real` | Task T2 |
| `473_left_LCX_prox_20mm_60ds__T5_vox_narrow__real` | Task T2 |
| `473_left_LCX_prox_20mm_60ds__T5_vox_wide__real` | Task T2 |
| `138_left_LAD_prox_20mm_70ds__T1_missed_branch__real` | Task M |
| `69_left_LCX_prox_20mm_65ds__T1_missed_branch__real` | Task M |
| `473_left_LCX_prox_20mm_60ds__T1_missed_branch__real` | Task M |
| `139_right_RCA_prox_10mm_70ds__T1_missed_branch__real` | Task M |
| `306_left_LAD_prox_20mm_80ds__baseline__real` | Task N |
| `306_left_LAD_prox_20mm_80ds__T1_missed_branch__real` | Task N |
| `306_left_LAD_prox_20mm_80ds__T5_vox_narrow__real` | Task N |
| `306_left_LAD_prox_20mm_80ds__T5_vox_wide__real` | Task N |

Baselines for scans 14, 138, 69, 473 and 139 are the solves you already returned (M1 and P5): reuse them, and do not
re-solve them. Scan 272 is not used (outlet lost in meshing).

Every package was written by `code/export_cfd_case.py` (T5 through the wrapper `code/export_cfd_case_t5.py`, which
patches the insertion in memory only). The exporter's blinding check passed on the folder. Re-exporting the shipped
M1 and P5 packages from the same code gives byte-identical files.

---

## 3. Tasks

All solves use the production recipe (D1), the Task C template with the D8 probe function objects, 16 ranks per
solve on a quiet lane where possible, the 3000-iteration budget and the B1 settle rule. Return for every solve: a
`M1_results`-format row, `M1_probes`- and `M1_outlets`-format CSVs, the measurement-probe history, the throat
Reynolds number, cells, and the D2–D4 gate distances. Return for every new geometry: `as_meshed_radius_<case>.csv`
and `_inscribed.csv`. "Resistance mode" = `bc_A`; "prescribed-flow mode" = per-outlet flows from `bc_C_flows`
(the clean flows), as in M1.

### TASK T (first; required): throat error in 3D, scan 14
1. `14_..._T5_vox_narrow`: build, mesh, solve in resistance mode and in prescribed-flow mode (2 solves).
2. `14_..._T5_vox_wide`: the same (2 solves).
3. Report FFR at the measurement probe (p011) and the throat probe against the returned scan-14 baseline, for both
   modes.
4. D14 extra: `14_..._T5_vox_narrow` in resistance mode with the 12.5 µm throat zone (1 solve). Compare it with A1.

Budget about 15 h. This is the task the paper needs most.

### TASK G (second; required): one global outlet scaling in 3D, scan 14 missed branch
The 0D Protocol C scales every outlet resistance by **one** factor k, fitted to the territory flows. The 3D arm has
so far run only fixed resistances (k = 1) and per-outlet prescribed flows. Run the one-parameter fit on the shipped
M1 package `14_left_LAD_prox_20mm_80ds__T1_missed_branch__real`, in resistance mode with every `bc_A` resistance
multiplied by k.
- **Targets:** the CLEAN territory totals in that package's `territories.csv`, as Decision B1 defines them. These are
  the full clean outflow, including the deleted branch's share.
- **Objective:** J(k) = Σ_j (Q_j(k)/T_j − 1)².
- **Procedure:**
  1. k₁ = 1 is the T1 resistance-mode solve you already returned. Do not re-solve it.
  2. Set k₂ = (Σ_j Q_j(k₁)) / (Σ_j T_j) and solve.
  3. Fit log Q_j against log k through the two points for each territory, take k₃ as the minimiser of J under that
     fit, and solve.
  4. Stop when |log k₃ − log k₂| < 0.01, or after at most two further solves.
- **Report per solve:** k, every territory flow, J, the largest |Q_j/T_j − 1|, and FFR at all probes.

Budget about 9 h (2–4 solves).

### TASK M (third): missed branch on four more instances
For each of the four T1 packages, run resistance mode and prescribed-flow mode (8 solves). Compare against the
returned P5 baseline of the same instance. If a T1 build fails a gate, flag it, solve it and return it. Do not repair
it. If the RCA case (139) has too few territories for a defined residual, still return the solves.

Budget about 24 h.

### TASK T2 (fourth): throat error on two more instances
As Task T steps 1–3, for scans 138 and 473 (8 solves). No 12.5 µm extra.

Budget about 24 h.

### TASK N (fifth; optional if time allows): one more instance, all three geometries
Scan 306, LAD, 20 mm, 80 %DS. Run the baseline in resistance mode (1 solve, whose case is kept for reuse), then T1,
T5 narrow and T5 wide in both modes (6 solves). The analysis side chose this instance by a fixed rule before any
solve.

Budget about 21 h.

---

## 4. Order and deadline

**Order:** T → G → M → T2 → N.

The analysis side would like Task T and Task G returned by **2026-10-13 18:00 (Malaysia time)**. Return each task
when it finishes, without waiting for the rest. Task M, T2 and N feed the revision and have no deadline.

## 5. Return

Return into `returns/2026-10-10/<task>/`, with a dated `NOTE.md` paragraph per task, an `INDEX.csv` and
`MANIFEST.sha256` over LF-normalised content. Re-issued CSVs get a dated suffix; never overwrite. Keep the case
directories (not in Drive) until the analysis side has read the return.

## 6. Two machines

If a second machine is available, give it Task M then Task T2 while the first runs T → G → N. Record the host in
every result row. Both machines must use the same OpenFOAM build and template commit (record the commit hash).

## 7. Still on hold, and what not to do

- Everything in 10-03 §7, 09-26 §6 and 09-24 §7 still applies:
  - no new work on scan 837;
  - no 0D predictions for cohort scans on the CFD side;
  - no case selected from `E0_prevalence_test.csv`;
  - no meshes, fields or STL files in Drive.
- Keep analysis-only files out of the shared repository; this is the 10-03 blinding incident.
- Do not tune or adjust anything to make a 3D result agree with any expectation. A 3D result that disagrees is a
  result.
