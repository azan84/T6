Audit completed read-only. Syntax/compile checks and all three permitted Task C tests passed.

## Findings — (C) Task C

1. **BLOCKER — The required end-to-end runner was not delivered.** The report explicitly says the runner was not changed and that the existing post-processing script is scan-14-specific, contains a dead hard-coded `/tmp/...` root, and cannot drive P5 with its package root and as-built extension data: [FIX30_REPORT.md:115](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/FIX30_REPORT.md:115), [post_case.sh:4](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/post_case.sh:4). Task C requires both the production template and end-to-end runner. This blocks installation as a complete Task C deliverable.

2. **MAJOR — P5 package 473 does not yet have a trustworthy measurement section.** Its measurement probe is at a bifurcation, its normal is 45° from the centreline tangent, and the report concedes it is not a clean single-vessel section: [FIX30_REPORT.md:113](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/FIX30_REPORT.md:113). The current check accepts one connected component and a broad area range, but a connected bifurcation cut could satisfy those tests: [probe_sections.py:10](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/probe_sections.py:10), [probe_sections.py:53](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/probe_sections.py:53). Resolve or replace that package probe before P5 case 473; do not merely accept it because the eventual mesh check happens to pass.

3. **MINOR — The demonstration manifest is not complete.** Verification reports three unlisted `pf/__pycache__/*.pyc` files, but extras are informational and do not make verification fail: [verify_manifest.sh:24](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/verify_manifest.sh:24). Remove generated caches from the deliverable or regenerate after final staging. The LF-normalized hashing itself passed LF, CRLF, and tamper tests.

Confirmed correct:

- Both old 09-26 planes were genuinely defective: throat cut 4 components and measurement cut 2. The bounded monitors passed the real five-iteration test and their `Area` columns agreed with the mesh sections.
- `measurementP`, `measurementFlux`, `throatP`, and `throatFlux` use `writeInterval 1`, `writeArea true`, and bounds: [pf_common.py:69](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/pf_common.py:69).
- Area-aware column parsing is correct: [pf_common.py:143](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/pf_common.py:143).
- The B1 tests correctly distinguish real measurement B1 from `PROXY_NOT_B1`, apply the prescribed-flow 800-iteration floor, and retain the full-budget recommendation.
- All five P5 packages passed the case-file/stub-patch test, but this was deliberately not an actual mesh-section test: [test_p5_stub.py:19](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_p5_stub.py:19).
- No unrelated numerical-template changes were found: `0/U`, `0/p`, `fvSchemes`, `fvSolution`, and transport/turbulence files are byte-identical to `baseline_resistance`.

## Findings — (A) Task A

4. **MAJOR — The experiment changes MPI decomposition as well as mesh resolution.** The returned/baseline case uses 16 ranks; both D7 cases specify 8 ranks: [baseline_D7 build_info.json:4](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance/build_info.json:4). Therefore the assertion “equal except mesh and new monitors” is not true. Because decomposition/round-off can select a steady branch, especially in a comparison with a 0.00055 threshold, either run at the returned 16 ranks or explicitly preregister 8 ranks as an additional deviation and require matching flow-state evidence.

5. **BLOCKER — There is no usable Task A solve/post-process workflow that guarantees retained fields and records flow state.** The only post script has the invalid hard-coded root and only recognizes the old `baseline` label: [post_case.sh:2](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/post_case.sh:2), [post_case.sh:4](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/post_case.sh:4). No D7 launcher or real-lumen jet-state diagnostic exists. Before running, provide a checked sequence that solves one variant at a time, reconstructs the final fields, verifies reconstruction before any processor-directory cleanup, generates the required probe/outlet/results files, and computes the state diagnostic.

6. **MAJOR — Current resource headroom is insufficient for an unguarded run plan.** At 2.2 GB per million cells, the 6.241 M and 8.309 M cases require approximately 13.7 and 18.3 GB respectively. Current `MemAvailable` is about 24 GiB, so they fit only sequentially; concurrent execution does not. Free disk is about 26 GB, which is below the 18.3 GB largest-case estimate plus a 10 GB safety margin, before retaining the first case’s reconstructed fields. Free disk or define a measured reconstruct-and-purge policy before launch. The relevant cell counts are recorded at [baseline_D7 mesh_gates.json:10](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/mesh/baseline_D7_12p5/mesh_gates.json:10) and [zoneB mesh_gates.json:10](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/mesh/baseline_D7_12p5_zoneB/mesh_gates.json:10).

7. **MAJOR — The acceptance reference is misidentified and the comparison statistic is not operationally specified.** `M1_results.csv` contains no measurement-probe FFR column. The actual returned reference is `p_over_Paorta = 0.8697574904997768` in [M1_probes_baseline_resistance.csv:14](/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_probes_baseline_resistance.csv:14). Compare like with like: the new reconstructed iteration-3000 measurement section against that returned iteration-3000 probe value. Report the `measurementP` last-100 mean separately for B1. Apply `abs(FFR_D7 − 0.8697574904997768) < 0.00055` separately to both variants.

8. **MAJOR — Flow-state classification must be preregistered before looking at the final fields.** A sten70 Cartesian-axis script is not transferable to this curved real lumen. For each D7 result, use bounded connected LAD sections from immediately downstream of the throat through measurement p011, oriented by the local centreline tangent. Record the flux-weighted velocity-centroid offset normalized by section radius and its persistent lateral direction along the vessel. Classify axisymmetric versus deflected using a fixed threshold established before examining results, and compare the two D7 signatures. If their states differ—or if the 8-rank state cannot be related to the returned 16-rank state—the FFR difference is confounded and must not be presented as mesh sensitivity alone.

Confirmed correct:

- The meshing-code diff is confined to configurable throat request, throat-zone endpoints, their provenance metadata, and the virtual-memory limit: [build_m1_mesh.py:16](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/build_m1_mesh.py:16), [build_m1_mesh.py:67](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/build_m1_mesh.py:67).
- Realized throat resolution is about 12.5 µm, with 66 minimum cells across the throat; both standard checks pass.
- Both variants retain strict D3/D4 failure from low-quality face-tets 0.698 mm from the throat, as expected: [d34_D7_12p5.json:41](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/out_returns/d34_D7_12p5.json:41), [d34_D7_12p5_zoneB.json:41](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/out_returns/d34_D7_12p5_zoneB.json:41). Both therefore must be solved.
- Resistance values, `G`, relaxation factors, initial fields, schemes, solver settings, fluid properties, and as-built extension inputs match the audited baseline.
- The D8 bounded monitors and their mesh checks are present in both D7 cases.

VERDICT (C): NOT READY  
VERDICT (A): NOT READY
