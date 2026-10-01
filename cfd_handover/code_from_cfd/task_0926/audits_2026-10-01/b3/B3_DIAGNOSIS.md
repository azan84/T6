# B3 smoke test: diagnosis of the non-reproduction (2026-10-01) and proposed change

## Observation
`code_from_cfd/smoke_test/run_smoke_test.sh` (fix25: 3000 iterations, Stage A sten70, A5 coarse recipe, 198,252 cells, 8 ranks, OpenFOAM v2406) was run as the reference run (`WRITE_REFERENCE=1`).
Result: outlet flow 1.17825059e-06 m3/s, flat to 5 digits from iteration 1000 to 12000 (continued run). Returned value (stageA_A5_ladders.csv, A5 sten70 coarse): 1.17392231e-06. Difference +0.369 %; the test criterion is 0.1 %.

## Evidence (all runs: same dictionaries, same 0/ files, 8 ranks scotch, same build `_1653fa08-20260127`; work dirs under /home/azan/paper6_t6_work)
| run | mesh | inlet/outlet polyPatch type | initial state | Q_out (m3/s) | p_meas kin. (x=56.5 mm) | FFR_x56.5 | jet centroid offset at x=50 / 56.5 mm |
|---|---|---|---|---|---|---|---|
| original 2026-09-18 (archive A5_sten70_coarse) | archived | wall | default | 1.17392231e-06 | 8.87426 | 0.78396 | 85.0 / 82.8 um |
| a5_arch8 (today) | archived | wall | default | 1.17390297e-06 (2000 it) | 8.87434 | 0.78397 | 85.1 um at x=50 |
| t2_archmesh_patch | archived | patch | default | 1.17390294e-06 (3000 it) | 8.87434 | | (same trajectory as a5_arch8 to all printed digits) |
| smoke_ref / smoke_cont | new (today's cartesianMesh) | patch | default | 1.17825059e-06 (3000), 1.17825058e-06 (12000) | 8.85754 | 0.78248 | 0.9 um at x=50 |
| t1_newmesh_wall | new | wall | default | 1.17825059e-06 | 8.85754 | | (same trajectory as smoke_ref) |
| bi_new_from_asym | new | patch | mapFields from t2_archmesh_patch (deflected) | 1.17390288e-06 (4000 it, flat from 1000) | 8.87434 | 0.78397 | 85.1 / 82.7 um |
| bi_arch_from_sym | archived | patch | mapFields from smoke_cont (symmetric) | 1.17825071e-06 (4000 it, flat from 200) | 8.85754 | 0.78248 | 0.9 / 1.5 um |
Mesh comparison archived vs new: both 198,252 cells, 214,037 points, identical bounding box; 96 % of points coincide, 4 % differ by > 0.1 um, max 2.1 um, all near the wall (r 1.66-1.80 mm), x in [-0.1, 3.7] mm (inlet region). STL sha256 identical. cfMesh (OMP_NUM_THREADS=8) is therefore not bitwise reproducible from run to run.
Jet diagnostic (`jet_offset.py`): |U_x|-weighted centroid of 0.8 mm slabs; the throat is at x = 30 mm; the measurement station x = 56.5 mm lies inside the recirculation region of both states.
Archived A5 ladder solutions: coarse 85 um (deflected), medium (379,468 cells) 2.1 / 3.5 um (symmetric), fine (760,480 cells) 7.2 / 12.0 um (weakly off-axis).
The run on 2026-09-27 (fresh mesh, lost with the scratch directory) was reported as +0.189 % at 2000, +0.002 % at 2500 it relative to the returned value, i.e. it ended on the deflected branch after a slow transition.
One unexplained event: an identical repeat of a5_arch8 stopped at iteration 1301 with SIGFPE in one rank (WSL crash capture, no OpenFOAM trace); the same set-up then ran 3000 iterations (t2_archmesh_patch) without error. Not reproduced.

## Diagnosis
The steady laminar sten70 problem at this resolution (Re_throat about 450) has TWO stable steady solutions of the discrete equations on the same mesh: an axisymmetric jet (Q 1.178251e-06, FFR_x56.5 0.78248) and a wall-deflected (Coanda-type) jet (Q 1.173903e-06, FFR 0.78397). Each is stable for >= 4000 iterations on either mesh; which one a run from the default initial field reaches is decided by micrometre-level differences of the cfMesh output. Branch values are mesh-realisation independent to 5 digits. The polyPatch type (wall vs patch) has no effect. The environment (OpenFOAM build, host) reproduces the returned value to 0.0016 % on the archived mesh. Hence the smoke test as written passes or fails by chance of the mesh realisation; it is not a code defect of the solver set-up.

## Proposed change of the smoke test (to be implemented by the fixer, then verified by two real runs)
1. `compare_smoke.py`: two admissible reference states. PASS iff complete run AND same-mesh checks (unchanged) AND |Q/Q_b - 1| <= 0.1 % for exactly one branch b in {deflected: 1.17392231e-06 (the returned value), symmetric: 1.17825059e-06 (reference machine 2026-10-01)}; the verdict line names the branch ("SMOKE TEST PASS (deflected-jet branch = the returned A5 value)" / "(symmetric-jet branch)"). The branches are 0.369 % apart, so the 0.1 % windows cannot overlap. FFR_x56.5 of the matched branch (0.78397 / 0.78248) is printed as information and must agree within 0.0005 (consistency check of the branch identification; FAIL otherwise).
2. `reference_result.json`: schema with `branches: {deflected: {...}, symmetric: {...}}` each holding Q_out, FFR_x56p5, p values, cells, provenance (which run, date, mesh, iterations); `--write-reference` adds/updates the branch the run falls on (identified by nearest of the two constants above within 0.1 %; refuses otherwise) and keeps the other. The deflected entry is seeded from a reference-machine run of the smoke case itself if one lands there; until then it carries the returned value with provenance 'returned A5 run 2026-09-18 (archive), re-run 2026-10-01 on the archived mesh: 1.17390297e-06'.
3. `run_smoke_test.sh`, `SETUP.md` section 4 (still says 2000 iterations and ./smoke_work): text updated; no change of numerics, mesh recipe, iteration count (3000) or exit codes.
4. Report/NOTE: a short subsection stating the two-state finding, its effect on the A5 ladder (coarse level on the other branch than medium/fine: the non-monotonic ladder), and the caveat for U3D (fields of the U3D levels were purged; indirect evidence only: two independent zone families agree within 1e-4 at each level and the finest 3D level agrees with the axisymmetric wedge within 1e-4, consistent with the symmetric branch; a direct check needs a re-run with fields kept).

## Questions for the auditors
(a) Is the diagnosis supported by the evidence, or is an alternative explanation (incomplete convergence, BC relaxation artefact, decomposition effect) not excluded? (b) Is accept-either-branch a sound smoke-test criterion for "a second machine reproduces one returned result", or should the case be replaced/forced to one branch (how, without shipping fields)? (c) Is the U3D caveat worded correctly, and is further evidence required before the U3D value 0.00055 stands? (d) Anything else missing.
