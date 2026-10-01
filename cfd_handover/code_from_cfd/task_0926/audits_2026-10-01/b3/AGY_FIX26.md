# Strict Read-Only Post-Fix Audit: Task B3 Branch-Aware Smoke Test (`fix26`)

**Audit Target:** Changed files in [`/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/)  
**Baseline / Originals:** [`/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test/`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test/) and [`/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/SETUP.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/SETUP.md)  
**Context Documents:** [`B3_DIAGNOSIS.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md), [`SOL_B3_DIAG.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/SOL_B3_DIAG.md), [`AGY_B3_DIAG.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/AGY_B3_DIAG.md), [`OPUS_BRIEF_26.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/OPUS_BRIEF_26.md), and [`FIX26_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/FIX26_REPORT.md)  
**Verification Mode:** Strict read-only execution; no OpenFOAM/mpirun jobs executed; no files edited.

---

## 1. Audit Execution Results

Both permitted commands were executed in the test environment:

1. **Unit Test Suite (`python3 fix26/smoke_test/test_compare_smoke.py`):**
   ```text
   Ran 14 tests in 0.906s
   OK
   ```
   All 14 tests passed, asserting deflected pass, symmetric pass, between-branches failure, Q-in-window-FFR-out failure, unstable final-window failure, incomplete run (exit 3), cell count mismatch (exit 3), write-reference refusal/replacement governance, schema 1 rejection (exit 2), branch tampering rejection (exit 2), shipped reference consistency, and real `smoke_ref` evaluation.

2. **Real Run Evaluation (`python3 fix26/smoke_test/compare_smoke.py /home/azan/paper6_t6_work/smoke_ref fix26/smoke_test/reference_result.json`):**
   ```text
     vs deflected branch (1.17392231e-06 m3/s, FFR 0.78396): Q +0.36870 %, FFR -0.001477
     vs symmetric branch (1.17825059e-06 m3/s, FFR 0.78248): Q +0.00000 %, FFR +0.000000
   vs the returned Stage A A5 coarse value 1.17392231e-06: +0.36870 %   cells 198252 (reference 198252)   final-window bands: Q 1.19e-05 %, FFR 2.74e-08   wall None s
   SMOKE TEST PASS (symmetric-jet branch; not the returned value, see README)
   ```
   Exit code: `0`. Correctly identified the reference-machine run as the symmetric-jet branch with stationarity verified to $1.19 \times 10^{-5}\%$ in flow and $2.74 \times 10^{-8}$ in FFR.

---

## 2. Audit Conditions Compliance Matrix

| Audit Condition | Source Requirement | Status in `fix26` | Evidence |
| :--- | :--- | :--- | :--- |
| **Eliminate Logical Conjunction Deadlock** | AGY Finding 1 | **MET** | In [`compare_smoke.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L180-L188), the deadlock condition `abs(dq) <= 0.1 and abs(dq_ret) <= 0.1` has been removed. Gating is evaluated against exactly one branch. |
| **Two Admissible Reference States** | B3 Diagnosis §27, OPUS 1 | **MET** | Defined in code constants [`BRANCHES`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L34) and populated in schema-2 [`reference_result.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/reference_result.json#L16-L75). |
| **Dual-Variable Joint Gating ($Q$ and $\text{FFR}$)** | AGY §3(b), OPUS 1 | **MET** | Tolerance is $\pm 0.1\%$ on $Q_{\text{out}}$ and $\pm 0.0005$ on $\text{FFR}_{x56.5}$ ([`compare_smoke.py#L36,L105-L106`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L36)). |
| **Final-Window Stability Gating** | SOL Finding 8, OPUS 1 | **MET** | Evaluated over last 200 iterations: $Q$ band $\le 0.01\%$ of mean, $\text{FFR}$ band $\le 10^{-5}$ ([`compare_smoke.py#L37,L63-L65,L107-L112`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L37)). |
| **Schema 2 & Reference Governance** | OPUS 2, SOL Finding 8 | **MET** | Schema 2 enforced; Schema 1 rejected with exit 2; reference file cannot redefine code constants; `--replace-branch` required for replacements ([`compare_smoke.py#L113-L126,L161-L162`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L113-L126)). |
| **Provenance Metadata Recording** | SOL Finding 8, OPUS 2 | **MET** | Records `mesh_points_sha256`, `processor_faces`, `nprocs`, `decomposition_method`, and window bands in [`provenance()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L127-L143). Verified against raw logs. |
| **Wording: "Same Recipe / Cell Count"** | SOL Finding 8, OPUS 4 | **MET** | Updated throughout [`compare_smoke.py:11`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L11), [`run_smoke_test.sh:6,10,99`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L6), and [`SETUP.md:31-33`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md#L31-L33). |
| **No Numerics or Recipe Alterations** | OPUS 6 | **MET** | All mesh, solver, boundary, and geometry files in [`case_files/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/case_files) are 100% byte-identical to originals. `cartesianMesh` and 3000 iterations preserved. |

---

## 3. Technical Evaluation of Logic & Edge Cases

### A. Exactly-One-Branch & Disjoint Windows
- In [`compare_smoke.py#L180-L188`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L180-L188), candidates are identified by $Q$ matching:
  - If 0 branches match $Q$: appends `"outlet flow in no branch window"`, prints distances to both, returns exit code 1.
  - If $>1$ branches match $Q$: appends `"outlet flow in N branch windows"`, returns exit code 1. (Mathematically impossible under valid reference values: branches differ by $+0.3687\%$, whereas windows span $\pm 0.1\%$, leaving a $+0.168\%$ deadband gap).
  - If exactly 1 branch matches $Q$: checks if that branch's $\text{FFR}$ matches within $\pm 0.0005$. If $\text{FFR}$ fails, it reports the exact delta and returns exit code 1.
  - If both $Q$ and $\text{FFR}$ match, and final window is stable: returns exit code 0.

### B. Window Stability Computation
- Lines 63–65 compute:
  $$\Delta Q_{\text{rel}} = \frac{\max(Q_{2801..3000}) - \min(Q_{2801..3000})}{|\text{mean}(Q_{2801..3000})|} \times 100\%$$
  $$\Delta \text{FFR}_{\text{abs}} = \max(\text{FFR}_{2801..3000}) - \min(\text{FFR}_{2801..3000})$$
- Non-finite values or incomplete series are trapped in [`measure()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L40-L66) before these lines run, preventing division-by-zero or NaN propagation.

### C. FFR Kinematic Pressure Conversion
- Conversion formula: $\text{FFR} = p_{\text{meas}} \times \rho / P_{\text{aorta}}$ with $\rho = 1060.0\,\text{kg/m}^3$ and $P_{\text{aorta}} = 11998.98\,\text{Pa}$.
- Matches the physical definition: for $p_{\text{meas}} = 8.87426046$, $\text{FFR} = 0.78395964$; for $p_{\text{meas}} = 8.85754493$, $\text{FFR} = 0.78248298$. Evaluated and consistent across all files.

### D. Schema 2 and Branch Tampering Protection
- [`load_reference()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L113-L126) rejects Schema 1 files with exit code 2 and a descriptive message pointing to the shipped Schema 2 file.
- It also asserts that any branch in `reference_result.json` lies within $\pm 0.1\%$ $Q$ and $\pm 0.0005$ $\text{FFR}$ of the hardcoded [`BRANCHES`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L34) constants. Thus, a corrupted or malicious reference file cannot silently move the branch targets.

---

## 4. Specific Audit Focus Items

### A. The `WRITE_REFERENCE=1` Path in `run_smoke_test.sh`
The user prompt requested an evaluation of:
> *"...the WRITE_REFERENCE path which now always exits 2 because both branches exist - is that acceptable/documented?"*

1. **Mechanism:**
   In [`run_smoke_test.sh#L95-L97`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L95-L97):
   ```bash
   if [ "${WRITE_REFERENCE:-0}" = 1 ]; then
       step "6/6 write reference"; python3 "$HERE/compare_smoke.py" "$W" "$REF" --wall $(( $(date +%s) - T0 )) --write-reference "$REF"; exit $?
   fi
   ```
   `compare_smoke.py` is invoked with `--write-reference "$REF"`, without `--replace-branch`. In [`compare_smoke.py#L162`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L162):
   ```python
   if b in base["branches"] and replace != b:
       print(f"REFERENCE NOT WRITTEN: {ref} already holds a {b} entry; pass --replace-branch {b} to replace it (the other branch is always kept)"); return 2
   ```
   Because the shipped [`reference_result.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/reference_result.json) already has both `deflected` and `symmetric` entries, any run via `WRITE_REFERENCE=1 ./run_smoke_test.sh` will reach step 6, refuse to write, and exit with code 2.

2. **Is it acceptable?**
   - **No, not in its current automated state.** While the safety refusal in `compare_smoke.py` is sound (preventing silent overwriting), [`run_smoke_test.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh) provides **no passthrough flag or environment variable** (e.g., `SMOKE_REPLACE_BRANCH=...`) to allow `--replace-branch` to be forwarded to `compare_smoke.py`.
   - Even worse: [`run_smoke_test.sh#L29`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L29) prints at the start: `WRITE_REFERENCE=1: reference run, step 6 writes $REF (no comparison)`. It does **not** fail fast in preflight, but instead permits an expensive 5-minute OpenFOAM simulation (3000 iterations across 8 cores) to run to completion, only to abort at step 6.
   - The user is then forced to manually run `python3 compare_smoke.py <W> reference_result.json --write-reference reference_result.json --replace-branch <branch>`. This renders `WRITE_REFERENCE=1` in `run_smoke_test.sh` a dead end when the shipped reference file is present.

3. **Is it documented?**
   - It is documented in the header comments of [`run_smoke_test.sh#L15-L16`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L15-L16) and in [`FIX26_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/FIX26_REPORT.md#L123) (Open Point 2).
   - However, it is **completely omitted** from [`SETUP.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md), and contradicted by [`code_from_cfd/README.md#L22`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md#L22) (which still states that `reference_result.json` is written by running `WRITE_REFERENCE=1`).

### B. The Verdict String & "see README"
The user prompt requested an evaluation of:
> *"...documentation accurate (the verdict string says 'see README' - is there such a README?)."*

1. **Findings on Disk:**
   - In [`compare_smoke.py#L35`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L35):
     ```python
     VERDICT = {"deflected": "deflected-jet branch = the returned A5 coarse value", "symmetric": "symmetric-jet branch; not the returned value, see README"}
     ```
   - When a fresh run lands on the symmetric branch, it outputs:
     `SMOKE TEST PASS (symmetric-jet branch; not the returned value, see README)`
   - **There is no such README.**
     - There is no `README` in `fix26/smoke_test/`.
     - There is no `README` in `fix26/`.
     - The top-level [`code_from_cfd/README.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md) has not been updated and contains no mention of the two branches.
     - The actual explanation of the two branches is located in [`SETUP.md` Section 4](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md#L31-L33).
   - In fact, [`run_smoke_test.sh#L99`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L99) prints `(SETUP.md section 4)`, directly contradicting the string emitted by `compare_smoke.py` immediately above it.
   - While the fixer followed the exact text specified in [`OPUS_BRIEF_26.md#L10`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/OPUS_BRIEF_26.md#L10), the brief contained a dangling reference that creates a confusing user experience.

---

## 5. Numbered Findings

### Finding 1: Dangling Documentation Pointer in PASS Verdict String
- **Severity:** **MAJOR**
- **Evidence:** [`fix26/smoke_test/compare_smoke.py:35`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L35), [`fix26/smoke_test/compare_smoke.py:188`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L188), [`/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md:22`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md#L22)
- **Description:** The verdict string emitted on the symmetric branch instructs the user to `"see README"`. However, no README exists in `smoke_test/`, and the repository's root [`code_from_cfd/README.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md) does not document the two branches (it still describes the obsolete single-value pass criterion). The actual explanation exists in [`SETUP.md` Section 4](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md#L31-L33). The string in `compare_smoke.py` should say `"see SETUP.md section 4"` to match [`run_smoke_test.sh:99`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L99).

### Finding 2: `WRITE_REFERENCE=1` in `run_smoke_test.sh` Inevitably Refuses and Exits 2 After 5 Minutes of Computation
- **Severity:** **MAJOR**
- **Evidence:** [`fix26/smoke_test/run_smoke_test.sh:29,96`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L29), [`fix26/smoke_test/compare_smoke.py:162`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L162)
- **Description:** Because [`reference_result.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/reference_result.json) already ships with both branches populated, invoking `WRITE_REFERENCE=1 ./run_smoke_test.sh` runs the entire 3000-iteration solve and then unconditionally aborts at step 6 with exit code 2. There is no preflight check warning the user before running, nor is there any environment variable (e.g. `SMOKE_REPLACE_BRANCH`) to forward `--replace-branch` to `compare_smoke.py`. Furthermore, line 29 announces `"WRITE_REFERENCE=1: reference run, step 6 writes $REF (no comparison)"`, which is contradicted by step 6's refusal.

### Finding 3: Omission of Reference-Writing and Replacement Instructions in `SETUP.md`
- **Severity:** **MINOR**
- **Evidence:** [`fix26/SETUP.md:24-36`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md#L24-L36)
- **Description:** While [`SETUP.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md) Section 4 has been well updated with the 3000-iteration requirement, the default WORKDIR, the two branches, and the test command, it contains no guidance on `WRITE_REFERENCE=1` or how to update branch entries using `--replace-branch`. An operator on the reference machine seeking to update the reference file has no documentation in `SETUP.md`.

### Finding 4: Incomplete Structural Validation of `cells` in `load_reference()`
- **Severity:** **MINOR**
- **Evidence:** [`fix26/smoke_test/compare_smoke.py:113-126`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L113-L126), line 175
- **Description:** [`load_reference()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L113-L126) validates `schema == 2`, branch presence, and branch Q/FFR boundaries against `BRANCHES` constants, but omits verifying that the top-level `cells` field equals `CELLS_A5` (198,252). While `write_reference()` verifies `m["cells"] == CELLS_A5` (line 147) and `main()` checks `m["cells"] == r.get("cells")` (line 175), a reference file manually altered to `cells: 999` would cause `main()` to demand 999 cells from the simulation rather than rejecting the reference file itself as invalid with exit code 2.

---

## 6. Conditions for Production Readiness

To achieve full production readiness and promote `fix26` into `code_from_cfd/`:
1. **Fix Verdict String / Documentation Pointer:** In [`compare_smoke.py:35`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L35), update the verdict text to reference `SETUP.md section 4` instead of `README`, or provide a `README.md` inside `smoke_test/` that explains the physical Coanda bistability. Update [`code_from_cfd/README.md:22`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md#L22) to remove the obsolete single-branch claim.
2. **Support Reference Replacement in `run_smoke_test.sh`:** Allow an environment variable such as `SMOKE_REPLACE_BRANCH=deflected|symmetric` in [`run_smoke_test.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh) so that `--replace-branch` is forwarded to `compare_smoke.py` at step 6; or if `WRITE_REFERENCE=1` is invoked without replacement against an already complete reference file, fail fast in preflight (exit 2) rather than burning 5 minutes of compute.
3. **Document Reference Governance in `SETUP.md`:** Add a brief note in [`SETUP.md` Section 4](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md#L24-L36) describing how reference files are updated and governance is enforced.

---

VERDICT: READY WITH CONDITIONS
