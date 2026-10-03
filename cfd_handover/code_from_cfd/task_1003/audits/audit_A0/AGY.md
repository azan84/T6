### Pre-Run Audit Report: Task A0 Control & Second Scheduler Lane (`pool2`)

---

### 1. Case Comparison: [`baseline_A0_25um_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance) vs Returned [`baseline_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_resistance)

* **Mesh & PolyMesh**: Both cases are hard-linked to the rebuilt production 25&nbsp;µm scan-14 baseline mesh [`m1/mesh/baseline_v2`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/mesh/baseline_v2) (`3,657,147` cells, 8 patches: `inlet`, `wall`, and 6 outlets `out_160`, `out_425`, `out_600`, `out_639`, `out_742`, `out_868`).
* **Boundary Conditions & Fields**:
  * [`0/p`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance/0/p): Byte-for-byte identical. Total pressure inlet ($p_0 = 11.31979245\text{ m}^2/\text{s}^2$, $P_\text{aorta} = 11998.98\text{ Pa}$), zero-gradient wall, identical `codedFixedValue` resistance models for all 6 outlets ($P_v = 666.61\text{ Pa}$, $\rho = 1060\text{ kg/m}^3$, identical $R$ and relaxation parameters).
  * [`0/U`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance/0/U): Byte-for-byte identical (`pressureInletOutletVelocity` on inlet/outlets, `noSlip` on wall).
* **Physical Properties & Discretization**:
  * [`constant/transportProperties`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance/constant/transportProperties) and [`constant/turbulenceProperties`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance/constant/turbulenceProperties): Identical ($\nu = 3.7735849\times 10^{-6}\text{ m}^2/\text{s}$, laminar).
  * [`system/fvSchemes`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance/system/fvSchemes): Identical steady-state, linearUpwind, limited Laplacian and snGrad schemes.
  * [`system/fvSolution`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance/system/fvSolution): Identical linear solver settings (GAMG for $p$, smoothSolver for $U$, relaxation 0.3/0.7, no `residualControl` per spec).
  * [`system/decomposeParDict`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance/system/decomposeParDict): Identical (`16` subdomains, `scotch`).
* **Differences in [`system/controlDict`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance/system/controlDict#L104-L160)**:
  * Solver numerics and execution controls are identical (`endTime 3000;`, `deltaT 1;`, `writeInterval 250;`, `purgeWrite 3;`).
  * Updated to the Task C template:
    1. `throatFlux` / `throatP`: added `writeArea true;` and spatial bounding box `bounds (0.041228 -0.152239 0.120644) (0.045840 -0.147627 0.125256);`.
    2. `measurementFlux` / `measurementP`: newly added Task C / D8 monitors on bounded plane at $p_{011}$ with `writeArea true;` and `bounds (0.052276 -0.170567 0.100589) (0.055995 -0.166849 0.104308);`.
  * These function objects are non-intrusive runtime monitors (they do not alter the governing equations or solution trajectory).

---

### 2. Concurrency, Memory, and Disk Verification

1. **Correctness of Concurrent 16 + 16 Ranks (SMT Oversubscription)**:
   * **Safe for Correctness**: The Linux kernel and Open MPI provide full memory isolation between independent processes. The cases run in separate directories ([`baseline_D7_12p5_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance) vs [`baseline_A0_25um_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_A0_25um_resistance)) with distinct MPI session directories.
   * **Algebraic Independence**: OpenFOAM algebraic solver operations are deterministic floating-point calculations under IEEE-754. Steady-state solution convergence depends on iteration count and linear solver convergence criteria, not wall-clock timing or core scheduling.
   * **SMT Contention**: The 32 ranks across 16 physical cores (32 logical threads) will contend for L1/L2/L3 caches and memory bus bandwidth, increasing solve wall-clock time, but will not corrupt or alter the converged solution. Both jobs use `--bind-to none` and `--mca mpi_yield_when_idle 1`, enabling CPU sharing without thread-locking.
2. **Memory Footprint**:
   * **Available**: Physical RAM is 27&nbsp;GiB (16&nbsp;GiB currently available; 7.1&nbsp;GiB free + 9.4&nbsp;GiB reclaimable buffers/cache) plus 15&nbsp;GiB swap.
   * **Demand**: A1 (6.24&nbsp;M cells) currently draws 8.04&nbsp;GB resident RAM (~515&nbsp;MB/rank). A0 (3.66&nbsp;M cells) is projected to draw ~4.7&nbsp;GB resident RAM (~295&nbsp;MB/rank). Total active resident memory will be ~12.7&nbsp;GB (or ~14.7&nbsp;GB including OS).
   * **Headroom**: >12&nbsp;GB of physical RAM headroom remains. OOM risk is negligible.
3. **Disk Capacity**:
   * **Available**: 18.7&nbsp;GB available on `/dev/sdd` (`/`), currently 94% full.
   * **Demand**: A0 decomposed mesh, 3 written checkpoints (`purgeWrite 3`), logs, and final reconstructed time 3000 require ~3.5&nbsp;GB (under 5&nbsp;GB). A1 has ~1.5&nbsp;GB remaining growth. Total peak consumption ~5.0&nbsp;GB.
   * **Headroom**: ~13.7&nbsp;GB free disk space will remain upon completion.
   * **Scheduler Threshold**: [`pool2/pool.py:39`](file:///home/azan/paper6_t6_work/pool2/pool.py#L39) checks `disk_free_gb() >= disk_gb + 10` ($5 + 10 = 15\text{ GB}$). Current free space of 17.8&nbsp;GiB satisfies this condition.

---

### 3. Numbered Findings

1. **MAJOR — Missing Trap to Restore `controlDict` on Abort or Signal**  
   **File & Line**: [`/home/azan/paper6_t6_work/pool/case_job.sh:11-15`](file:///home/azan/paper6_t6_work/pool/case_job.sh#L11-L15)  
   **Description**: In [`case_job.sh`](file:///home/azan/paper6_t6_work/pool/case_job.sh), `controlDict` is modified via `foamDictionary -entry endTime -set 2`. If `foamDictionary` fails at line 12, `fail` exits without restoring `controlDict`. More critically, there is no signal or `EXIT` trap. If the script is interrupted (e.g. `SIGINT`, `SIGTERM`, runner kill) while the 2-iteration smoke solve runs at line 14, the shell terminates without executing line 15, leaving `system/controlDict` permanently modified at `endTime 2;`.

2. **MAJOR — Incomplete Stale-Item Guard**  
   **File & Line**: [`/home/azan/paper6_t6_work/pool/case_job.sh:8`](file:///home/azan/paper6_t6_work/pool/case_job.sh#L8)  
   **Description**: Line 8 checks only `log.simpleFoam`, `postProcessing`, and `processor*`. It does not detect pre-existing `dynamicCode`, `log.smoke`, `log.smoke.keep`, `log.decomposePar`, `log.reconstructPar`, `system/controlDict.production`, or pre-existing numerical time directories (e.g. `3000`). If a stale `3000/` directory is left from an aborted or previous attempt, line 25 (`[ -d "$LAST" ] && [ -s "$LAST/p" ]`) evaluates to true immediately, masking a failed reconstruction or failed solve.

3. **MAJOR — Solved Time Not Asserted Against Requested `endTime`**  
   **File & Line**: [`/home/azan/paper6_t6_work/pool/case_job.sh:23-25`](file:///home/azan/paper6_t6_work/pool/case_job.sh#L23-L25)  
   **Description**: `LAST=$(grep "^Time = " log.simpleFoam | tail -1 | awk '{print $3}')` parses the final time step. The script never verifies that `"$LAST" = "$END"`. If the solver stopped early (e.g. on `stopAt nextWrite` or abnormal termination that wrote `End`), `reconstructPar -latestTime` reconstructs that premature time and line 25 reports `OK: solve and reconstruct done (time $LAST)` despite violating the mandatory 3000-iteration budget.

4. **MAJOR — Missing Verification of Compiled dynamicCode Libraries**  
   **File & Line**: [`/home/azan/paper6_t6_work/pool/case_job.sh:16`](file:///home/azan/paper6_t6_work/pool/case_job.sh#L16)  
   **Description**: Line 16 only checks `ls dynamicCode > /dev/null 2>&1`. It does not verify that all 6 required outlet shared libraries (`libres160_*.so`, `libres425_*.so`, `libres600_*.so`, `libres639_*.so`, `libres742_*.so`, `libres868_*.so`) were actually compiled during smoke (unlike [`run_set_generic.sh:119-120`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/run_set_generic.sh#L119-L120)). If an outlet library fails to build during smoke, all 16 MPI ranks will attempt on-the-fly compilation concurrently at line 20, causing compiler lock contention and race conditions.

5. **MINOR — Solver Exit Code Ignored When `^End` is Found**  
   **File & Line**: [`/home/azan/paper6_t6_work/pool/case_job.sh:20-21`](file:///home/azan/paper6_t6_work/pool/case_job.sh#L20-L21)  
   **Description**: `rc=$?` is captured from `mpirun`, but line 21 only checks `grep -q "^End" log.simpleFoam`. If `mpirun` or an MPI rank terminates with an error code after outputting `End` (e.g. during final MPI teardown), the non-zero exit code is printed at line 22 but execution proceeds to reconstruct.

6. **MINOR — `reconstructPar` Completion Token (`End`) Not Checked**  
   **File & Line**: [`/home/azan/paper6_t6_work/pool/case_job.sh:24-25`](file:///home/azan/paper6_t6_work/pool/case_job.sh#L24-L25)  
   **Description**: Line 24 executes `nice -n 10 reconstructPar -latestTime > log.reconstructPar 2>&1`. Line 25 checks that `$LAST/p` and `$LAST/U` are non-empty, but unlike [`post_helpers.py:reconstruct_check`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/post_helpers.py), it does not verify that `log.reconstructPar` terminated with `End` or that the reconstructed time matches `processor0`'s latest time.

7. **MINOR — Rank Budget Never Enforced in [`pool2/pool.py`](file:///home/azan/paper6_t6_work/pool2/pool.py)**  
   **File & Line**: [`/home/azan/paper6_t6_work/pool2/pool.py:30-41`](file:///home/azan/paper6_t6_work/pool2/pool.py#L30-L41)  
   **Description**: Line 30 computes `used = sum(...)`, but the loop never tests `if used + j["ranks"] > RANKS: continue`. While `pool2/jobs` currently only contains [`A0_control_25um.json`](file:///home/azan/paper6_t6_work/pool2/jobs/A0_control_25um.json), any additional job queued in `pool2` would be launched concurrently regardless of rank limits as long as RAM and disk pass.

---

VERDICT: READY WITH CONDITIONS
