# P5 build report: geometry + mesh for the five P5 baseline packages (work order 2026-10-03 §5, Opus brief 32), 2026-10-03

Scratch dir `item3_M1_pilot/p5/` only. Nothing written to Drive. No solver, no mpirun, no case directories. No 0D code: `zerod_ffr` and `outlets_837` are not imported, and both builders assert this.
The P5 cases were built one at a time with `nice -n 10`, `OMP_NUM_THREADS=4`. The mesh builder's own nice 19, ulimit and resource guard are unchanged.

## 1. Code (copies of `m1/`, generalised)
`build_m1_geometry.py`, `build_m1_mesh.py`, `m1lib.py` (unchanged), `e0_guard.py` (unchanged), `fix_patch_types.py` (unchanged), `run_mesh_seq.sh`, `d34_generic.py` (copy of `../d34_generic.py`).
New: `run_case.sh` (geometry → mesh → patch types → D3/D4), `run_all_p5.sh`, `compare_regression.py`, `summarise_p5.py` (→ `P5_summary.json`).
`clip_outlets.py` is imported from `../`. The `pf/` and `taskC/pf/` builders were not needed: no case directories were built.

Scan-14 assumptions removed, as listed in the brief:
| assumption | now |
|---|---|
| `MASK` path | `MASK_DIR/<meta.instance.scan>.coronary.nii.gz`; sha256 checked against `meta.json` provenance (all 5 match) |
| `VMTK_ENV` | env var, default `/home/azan/paper6_t6_work/scratchpad/micromamba/envs/vmtk` (reproduces the scan-14 STL byte for byte, §2) |
| `SHIPPED` dict | read from `mask_edit.json` if present. **No package ships these numbers** (scan 14's 1310 / 25 / 2 came from the work order). Observed numbers are reported and nothing is asserted. The gate becomes `mask_sha256_matches_package_(no_shipped_counts)`. |
| kind from the package name | `meta.json` `error_type` |
| mesh `PKG` dict | package resolved by name (`packages/P5/`, then `m1/pkg/`) or by path |
| `WHISKER_NODES` (285, 133) | replaced by the self-intersection clusters the geometry stage localises on the final surface (`gates.json final_surface.self_intersection_clusters`) |
| "LAD main path" (most LAD points / the single LAD leaf) | lesion path = the root → outlet path through the `probes.csv` throat `tree_node` that continues farthest distal. Used for the frames, the purity tagging, `s_pkg`, and the 25/50/100 µm zones. |
| r_throat = min r_target over the tree, throat = argmin | throat = `probes.csv` throat node; r_throat = `r_target_mm` there; h_max = r_throat/8. The old rule would have picked a distal outlet vessel in 473 (out_571, 0.457 mm) and 272 (node 380, 0.420 mm). |
| D1 jet-junction chain | kept only for an LAD lesion whose D1 segment branches off the lesion path: scan 14 (out_160, unchanged) and 138 (out_496). None for 69, 473, 272, 139. |
| G3 label / positive control / removed-voxel proximity on "LAD" | on the lesion vessel's segment (`meta.instance.vessel`: LAD / LCX / RCA) |
| E0 row (14, left) | `(meta.instance.scan, side)`. The frozen subset csv is on this machine now; all 5 are MEMBER. |
| frame-flip counts | measured counts are the gate (all deletion points inside with the flip, none without). The `meta.json` frame sentence ("42/42") is the same template text in every package, scan 14 included. Its counts are parsed and compared (reported only): fractions match in all, counts do not. |
| lesion window L, ds, centre | from `mask_edit.json` `lesion` (20/20/20/10/10 mm) |
Gate keys that were named `LAD` in the scan-14 `gates.json` are named `lesion_path` here; `compare_regression.py` maps them back.
Mesh builder: the `M1_THROAT_REQ`, `M1_THROAT_LO_MM`, `M1_THROAT_HI_MM` and `M1_ULIMIT_KB` options are kept, with defaults equal to the production recipe D1 (25 µm ±4 mm, 50 µm tube [s_t−12, s_t+22] mm and r 4 mm cap spheres, 100 µm elsewhere, 4 BL ratio 1.2). Two additions: `--geom/--out` and `--measure-only` (re-measures the gates on an existing mesh). The gates are now also measured when standard checkMesh fails; scan 14 skipped them in that case.

## 2. Regression on scan 14 (baseline package, m1/pkg)
- **Geometry** (`out/14_regression/`, 406 s): 1381 numeric/boolean gate leaves compared with `../m1/out/baseline/gates.json` (`out/14_regression/regression_vs_m1.json`). **All equal** except the 5 "shipped" fields, which are now `None` by design. The observed values (1310 voxels removed, 2 → 2 components) are unchanged. `case.stl` is **byte-identical** to the reference. The radius csv data are identical; only the `cohort_status` text differs (E0 is now MEMBER, it was waived then).
- **Mesh** with defaults (`mesh/14_regression/`, 221 s): **3,657,147 cells, the same as the reference** (third exact reproduction). Strict checkMesh gives the same 3 failures (face tets 1058, concave cells 52, small volume ratio 30). Patch faces, max non-orth/skew/aspect (55.62 / 1.850 / 10.98), cells across the throat (36/39.5), throat-plane area error (−0.158 %) and the cones of the meshDict (95, identical text) are all identical.
  The only different number: low-quality face-tet points within 2 mm of a self-intersection site are 67 now vs 81 before. The sites are now the measured cluster centroids, no longer the two centreline nodes.
- D3/D4 on the regression mesh: FAIL, face tets 1.43 mm from the throat (as returned before).

## 3. Per-case results (order 138, 69, 473, 272, 139)
Relative throat gate (D2, decisive) = as-built / undeformed / radial_scale − 1, for the inscribed circle, the area-equivalent radius and the sphere at the axis, each within 1 %. The absolute gate (vs `r_target_mm`) is reported only. Self-intersection uses `surfaceCheck -checkSelfIntersection` on the final STL; "raw" is the marching-cubes surface. D3/D4 is the minimum distance from a strict-checkMesh flagged vertex to the throat and the measurement probe centre (disc distance after the slash); FAIL if < 2 mm.

| | 138 LAD 20 mm 70 % | 69 LCX 20 mm 65 % | 473 LCX 20 mm 60 % | 272 RCA 10 mm 65 % | 139 RCA 10 mm 70 % |
|---|---|---|---|---|---|
| throat node / r_target / radial_scale | 62 / 0.4026 / 0.3707 | 76 / 0.5206 / 0.3442 | 81 / 0.6031 / 0.4038 | 55 / 0.5511 / 0.3268 | 44 / 0.3049 / 0.2982 |
| lesion outlet (path) | out_439 (LM, LAD) | out_657 (LM, LCX) | out_836 (LM, LCX) | out_620 (RCA) | out_367 (RCA) |
| **relative gate** insc / area-eq / sphere % | +0.014 / +0.014 / +0.354 **PASS** | +0.012 / +0.030 / +0.015 **PASS** | +0.019 / +0.036 / **+1.780 FAIL** | +0.041 / +0.123 / +0.022 **PASS** | +0.028 / +0.060 / **+3.332 FAIL** |
| absolute vs r_target % (insc / area-eq / sphere) | +4.3 / +15.1 / −4.3 FAIL | +3.2 / +10.2 / −4.9 FAIL | +2.2 / +6.5 / −5.1 FAIL | +9.3 / +17.4 / +5.5 FAIL | +7.6 / +12.0 / −0.4 FAIL |
| as-built throat mm (insc / area-eq / sphere) | 0.420 / 0.464 / 0.385 | 0.538 / 0.573 / 0.495 | 0.616 / 0.643 / 0.573 | 0.602 / 0.647 / 0.581 | 0.328 / 0.341 / 0.304 |
| purity / fold / window-edge gate | PASS (fold min dot 0.92) | **FAIL** (229 impure triangles, see §4) | PASS | PASS | PASS |
| frame check / voxels removed / components | 67/67, 0/67 / 694 / 2→2 | 85/85, 0/85 / 1095 / 2→2 | 126/126, 0/126 / 1224 / 2→2 | 194/194, 0/194 / 1887 / 2→2 | 61/61, 0/61 / 665 / 2→2 |
| final surface self-intersection | no | no | no | **yes, 1 point (inlet extension, §4)** | no |
| raw MC self-intersecting / positive control flagged | yes / yes | yes / **no** (§4) | yes / yes | yes / yes | yes / yes |
| cells | 4,941,176 | 4,218,023 | 5,487,673 | 7,639,018 | 4,138,185 |
| cells across throat min / median (≥ 12) | 50 / 63 PASS | 67 / 76 PASS | 79 / 86 PASS | 68 / 85.5 PASS | 39 / 43.5 PASS |
| p95 cell ±2 mm / BL first cell, 4-stack µm | 25.6 / 4.0, 20.5 | 25.6 / 3.5, 19.3 | 25.6 / 3.0, 17.5 | 25.5 / 3.5, 17.3 | 25.5 / 3.5, 17.3 |
| throat-plane area mesh vs STL | −0.06 % | −0.04 % | −0.04 % | −0.02 % | −0.07 % |
| standard checkMesh | **FAILED 1** (2 highly skew faces, max skew 4.81) | OK | OK | OK | OK |
| strict checkMesh failed checks | 4: skew 2, face tets 834, concave 49, vol ratio 31 | 3: 739, 74, 71 | 3: 1026, 115, 66 | 3: 466, 38, 15 (re-run, §4) | 3: 480, 33, 12 |
| max non-orth / skew / aspect | 52.6 / 4.81 / 12.5 | 58.8 / 1.83 / 11.3 | 58.1 / 1.91 / 13.0 | 55.9 / 2.05 / 12.3 | 55.6 / 1.91 / 11.4 |
| patches > 0 faces | all | all | all | **out_396 = 0 faces (lost, §4)** | all |
| mesh gate (finished, std OK, patches, ≥12 across, area) | **FAIL** (std checkMesh) | PASS | PASS | **FAIL** (out_396) | PASS |
| **D3/D4**: nearest flagged to throat / measurement mm | **FAIL** 0.45/0.05 / 1.02/0.13 (face tets) | **PASS** 2.60/2.42 / 2.04/1.57 | **FAIL** 1.32/1.25 / 1.07/0.38 (all 4 sets < 2 mm) | **FAIL** 0.83/0.60 / 2.01/1.44 (concave, face tets) | **FAIL** 1.55/1.43 / 1.79/1.46 (concave, face tets) |
| extensions mm (5 D inlet, 3 D outlets, D = 2 r_mm) | inlet 15.16; 159 3.23, 439 3.43, 496 3.41, 571 3.98, 712 4.54 | inlet 18.12; 282 4.05, 369 3.52, 486 3.46, 657 3.33 | inlet 19.02; 160 3.76, 372 3.16, 571 2.74, 633 3.42, 691 3.31, 836 3.11 | inlet 16.59; 279 3.37, 396 3.17, 620 3.36 | inlet 10.82; 367 3.35, 550 3.13 |
| wall clock: geometry / mesh incl. checkMesh+gates (cartesianMesh) / total | 347 / 878 (7:16) / 1232 s | 260 / 346 (2:37) / 639 s | 367 / 458 (3:10) / 871 s | 233 / 619 (4:13) / 1013 s + strict re-run 478 s + re-measure | 316 / 310 (2:18) / 657 s |
| cartesianMesh peak RSS | 3.49 GB | 2.86 GB | 3.72 GB | 4.98 GB (strict checkMesh 10.1 GB) | 2.95 GB |

Wall-clock was measured with the host busy: other solvers ran throughout, load 18–26 on 32 threads. 138's cartesianMesh took 7:16 at load ~20. No case had to wait for the memory guard. The clipped-loop area-equivalent diameters are in `gates.json` per patch, ranging 0.60 (473 out_571) to 5.17 mm (473 inlet). With `--d-basis areaeq` the extensions would scale by Deq/2r_mm (0.65–1.6).
Disk: geometry 120–630 MB per case, mesh 0.66–1.4 GB per case. In total, out/ is 1.6 GB and mesh/ is 5.4 GB; 17 GB is still free on /.

## 4. Flags and deviations (none repaired)
1. **473 and 139 fail the D2 relative throat gate, on the sphere-at-axis definition only** (+1.78 %, +3.33 %). The two in-plane definitions are within 0.06 %; scan 14's three were all ≤ 0.03 %.
   Measured cause: on the undeformed surface the nearest wall point to the throat axis point lies 0.26 mm off the throat plane, at a frame with larger radial_scale (139: 0.309 vs 0.298; 473: 0.412 vs 0.404). After deformation the nearest point lies in the plane (offset ≤ 0.02 mm). The sphere ratio therefore compares two different wall points; the deformation itself scales the throat section exactly.
   The rule was not changed. Both geometries exited with code 3 ("REJECTED") and were meshed anyway, flagged, as the work order asks. In 473 the min-radial_scale node (82) is one node distal of the probe throat (81).
2. **D3/D4: four of five cases FAIL** (138, 473, 272, 139); **69 PASSES** narrowly (2.04 mm to the measurement probe). The flagged entities nearest the probes are the same kinds as scan 14 (low-quality face tets, concave cells/faces). They are spread over the whole tree, with some inside the 25 µm zone and at its interfaces (counts per set in `mesh_gates.json flagged_sets_localised`). In 473 the measurement probe sits 1.07 mm from a flagged face (0.11 mm by the disc distance).
   D3 applies because the raw marching-cubes surface self-intersects in every case. In 138, 69, 473 and 139 the self-intersection is gone after vmtk smoothing; 272's is at the inlet extension (item 5).
3. **138: standard checkMesh fails** on 2 highly skew faces (max skewness 4.81). They are in the LCX (6 set points), 44 mm from the throat and 63 mm from the measurement probe. Recorded in `standard_checkMesh_failure_lines`; the mesh gate is FAIL.
   The first run skipped the throat measurements because of this, as the scan-14 code did. I changed the builder to measure whenever the mesh finished, and re-measured 138 with `--measure-only` on the unchanged mesh (`measure_only_rerun` in its `mesh_gates.json`).
4. **272: patch out_396 lost** (0 faces). cartesianMesh reported "Mesh has 2 unconnected regions" and removed 32,527 cells; mesh volume is −0.9 % vs the STL (−0.3 to −0.4 % for the others). The lost part is the distal R-PDA with the out_396 cap: 751 STL vertices more than 0.3 mm from the mesh boundary, all around out_396.
   It lies beyond a narrow neck in the mask lumen 6.1–6.9 mm upstream of the outlet (nodes 380–382: section r_eq 0.28–0.35 mm, inscribed 0.23–0.31 mm, against 100 µm background cells; node 380 is also the tree's minimum r_target). This is a mask feature, not the construction. **272 cannot be solved in resistance mode as meshed**: bc_A has a resistance on out_396. It is returned flagged. Changing the recipe there (e.g. a refinement zone on the R-PDA neck) would be a repair, so it was not done.
   Also for 272: the **strict checkMesh aborted under the 9 GB `ulimit -v`** ("new cannot satisfy memory request"; 7.64 M cells, the same failure mode as the scan-14 v1 mesh). With MemAvailable at 18.3 GB, I re-ran only the strict checkMesh with `ulimit -v 16 GB` (peak RSS 10.1 GB, 478 s): 3 failed checks. The aborted log is kept as `log.checkMesh.strict.aborted_ulimit9GB` and the first `mesh_gates.json` as `mesh_gates.first_run.json`.
   `d34_generic.py` (p5 copy) now returns `NOT_EVALUATED` when the strict log is incomplete. Before the re-run it had reported a false PASS for 272.
5. **272: final surface self-intersects at one point, inside the inlet flow extension** (5.1 mm upstream of the inlet plane, on the extension wall). It is 5.1 mm from any vertex of the pre-extension surface, and the smoothed tree surface is not self-intersecting, so it is an artefact of the straight extrusion of the clipped inlet loop. It is about 25 mm from the throat and was not repaired; cfMesh meshed through it, and standard checkMesh is OK.
6. **69: lesion purity gate FAILS.** The OM1 ostium sits at the distal edge of the window (OM1 branches at s_pkg 30.63; window end 29.97). Its result:
   - 43 OM1 wall vertices in the window tail (radial_scale 0.988–1.0, i.e. ≤ 1.2 % radial change) are not moved, and 229 triangles straddle moved LCX and unmoved OM1 vertices.
   - The gap to the other branch is −0.49 mm, against a required > 0.5 mm.
   - No fold-over (min dot 0.66), no non-path vertex displaced (0.0 mm), G3 label 99.9 %.
   The throat is unaffected (relative gate +0.03 %).
7. **69: the gates.json positive control was not flagged.** The bump at the middle LCX node (542) moved only 7 vertices. A supplementary control with the same rule at two other LCX nodes (511: 14 vertices; 573: 12) **is flagged** (`out/69/poscontrol_supplementary/result.json`; the corrupted STLs were deleted). So the surfaceCheck detector works on this surface, and the original control was too small a bump.
8. Disclosed as in scan 14 (unchanged): patch names are the package outlet_ids; D = 2 r_mm, not the loop diameter; spline path frames; the 837 clip zone factor 5; the absolute throat test is reported only (D2/D10). The D3/D4 disc distances use the geometry-stage surface section radius (`surface_radius_<scan>_baseline.csv`); as-meshed radius files come with the case build. `mesh_gates.json` keeps the name `lad_*` for the lesion path in its internal fields.
9. Blinding note: to check E0 membership I printed the matching rows of `CFD-SUBSET-FROZEN-2026-09-18.csv`, which also carry 0D columns (`ffr_discrete`, `base_discrete`, `healthy_main`). Nothing from those columns was used or stored. `e0_guard.py` reads only scan and side.

## 5. Files per case
`out/<scan>/`: `gates.json`, `case.stl` (metres; solids `inlet`, `out_<node>`, `wall`), `surface_radius_<scan>_baseline.csv`, `intermediate/` (raw/smoothed/clipped/lesion surfaces), `sc*/` (surfaceCheck logs).
`mesh/<scan>/`: `mesh_gates.json`, `recipe.json`, `d34.json`, logs (`log.cartesianMesh`, `log.checkMesh.standard`, `log.checkMesh.strict`, `log.time.*`), the strict sets `postProcessing/constant/<set>/<set>.vtp`, `constant/polyMesh` (inlet and out_* set to type `patch`, `patch_types_fixed.json`).
Run logs: `runs.log`, `logs/`. Summary: `P5_summary.json`, `logs/summary_table.md`. Regression: `out/14_regression/regression_vs_m1.json`, `mesh/14_regression/`.

Not done (outside this brief): case directories, solves, as-meshed radius files and the return CSVs. No background process is left running.
