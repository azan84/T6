1. **MAJOR — “Exactly one branch” is evaluated using Q alone, not the required combined Q-and-FFR predicate.**  
   [compare_smoke.py](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py:180) builds `hit` from only the Q component of `in_window()`. Lines 183–185 reject whenever two Q windows match, even if FFR uniquely identifies one branch. This can occur after legitimate `--replace-branch` updates because [load_reference()](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py:121) permits each reference Q to move 0.1% from its constant. An in-memory probe produced overlapping Q windows where the candidate matched `(Q=True, FFR=True)` for deflected and `(Q=True, FFR=False)` for symmetric; the specification therefore requires PASS, but the implementation reports two Q hits and FAIL. Branch matching must be based on `all(in_window(...))`, as the write path correctly does at line 150.

2. **MINOR — The symmetric PASS points to a README that does not document the two-branch result.**  
   [compare_smoke.py](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py:35) emits “see README”. There is no README in `fix26/`; the deployment parent does contain `README.md`, but its smoke-test description still says the test reproduces the single returned value at [README.md](/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md:22). The accurate explanation is actually in [SETUP.md](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md:31). The verdict should refer to `SETUP.md section 4`, or README must be updated.

3. **MINOR — Schema-2 validation is incomplete and can assign the wrong exit code to an unusable reference.**  
   [load_reference()](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py:113) validates the schema marker and branch measurements, but not required common fields such as `cells`, `stl_sha256`, `n_iter`, or the returned value. For example, a schema-2 reference missing `cells` passes loading, then [line 175](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py:175) classifies it as run/mesh non-comparability and exits 3, rather than reference-unusable exit 2. This is fail-safe but inconsistent with the documented schema and exit semantics.

4. **MINOR — `WRITE_REFERENCE=1` refusal is acceptable and mostly documented, but its startup message remains misleading.**  
   Refusing replacement without `--replace-branch` is explicitly required and correct. Since both shipped branch entries exist, the shell path at [run_smoke_test.sh:95](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh:95) will always propagate exit 2 after a complete run. Lines 14–16 and 23 document this and give the manual replacement command, so the behavior is acceptable. However, [line 29](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh:29) still announces that step 6 “writes” the reference, and [SETUP.md section 4](/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md:24) does not explain the always-refused environment-variable path.

Checks completed:

- The permitted real comparison exited 0 and correctly passed the symmetric branch; FFR was `8.85754493 × 1060 / 11998.98 = 0.78248297987`, and the last-200 bands were within tolerance.
- `bash -n` passed. Normal comparison and `WRITE_REFERENCE` paths propagate the Python exit code correctly.
- Reference hashes and processor-face provenance for `smoke_ref` were verified.
- Diff inspection found no solver numerics, mesh recipe, iteration-count, or OpenFOAM execution changes; executable shell changes are limited to the final explanatory message and preserved exit code.
- The permitted unit-test command ran zero tests because the enforced read-only environment provided no writable temporary directory. The real comparison and read-only/in-memory probes were still completed.

VERDICT: NOT READY
