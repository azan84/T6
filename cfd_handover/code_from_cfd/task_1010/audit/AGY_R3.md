# Pre-Run Audit Round 3: WO1010 Automation & Job Execution Pipeline

**Auditor:** Gemini 3.7 Flash  
**Scope:** WO1010 automation codebase, Round 3A/3B changes by Opus 5.5, pool jobs in `/home/azan/paper6_t6_work/wo1010_pool/jobs/`, and mesh outputs.  
**Mode:** AUDIT ONLY (Read-only inspection, syntax checks, AST verification, `--plan-only` test; no solver runs, no MPI, no production cases modified).

---

## 1. Acceptance of Coordinator Decision

**Verdict on Coordinator Decision:** **ACCEPTED.**

> **Rationale:**  
> Fallback jobs are pre-declared to never be generated or launched automatically. An unsteady or unsettled steady solve (`NOT_SETTLED` under B1/D8) halts execution fail-closed at the corresponding task gate (`gate_TaskT`, `gate_TaskG`, etc.) with non-zero exit (`rc=1`), which permanently blocks all downstream pool jobs via dependency chaining (`after`).  
>
> Given the projected computational cost of full transient fallbacks at 16 ranks (P5 139: 2.5–5 days; scan 14 T5 narrow: 7–15 days, up to 31 days at the $2\times$ cap), requiring an explicit coordinator decision, cost assessment with the study lead, and an independent pre-run audit before any fallback `.audited` marker is generated is both sound and operationally necessary. The steady solve execution path does not depend on fallback execution.

---

## 2. Review of Sol-R2 Findings (1–12)

| # | Sol-R2 Finding | Status in Round 3 | Details & Verification |
|---|---|---|---|
| **1** | **BLOCKER**: Task G lacks D15 settle checking; accepts unsettled steady solves. | **RESOLVED** *(with Minor Fallback Interface Disconnect)* | [`taskG.py:151-165`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L151-L165) now calls `wo_common.settle()` on every iteration. Settled unconverged solves stop with exit 3. Unsettled solves stop with exit 4 ("D15 fallback required for G\<n\>"). On restart with a complete fallback, territory flows (`Qterr`) and probe FFRs are consumed from fallback time-averages. *(See Finding 1 below regarding scan-14 fallback probe interface).* |
| **2** | **BLOCKER**: Pool `after` list enforces only steady job exit, not D15 settle completion before Task G. | **RESOLVED** | Fail-closed gate job [`gate_TaskT.json`](file:///home/azan/paper6_t6_work/wo1010_pool/jobs/gate_TaskT.json) runs [`task_gate.py TaskT`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/task_gate.py#L21-L37) after the 5 Task T solves. It verifies steady acceptance + B1 settle (or valid D15 fallback) for all 5 cases. [`taskG_14_T1regen`](file:///home/azan/paper6_t6_work/wo1010_pool/jobs/taskG_14_T1regen.json) lists `after: ["gate_TaskT"]`. If any Task T solve does not settle, `gate_TaskT` exits 1, setting pool status `failed rc=1` and permanently blocking Task G. |
| **3** | **MAJOR**: Fallback averaging window defensibility & stationarity acceptance. | **RESOLVED** | [`pimple_fallback.py:62-78`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/pimple_fallback.py#L62-L78) enforces pre-declared $T_{decl} = \max(6\tau_{jet}, 1.5\tau_{slow})$ with volume-based $\tau_{slow} = V_{post}/Q_{post}$. Time-averaging over $[T_{run}/2, T_{run}]$. Acceptance requires quarter-stationarity: $|\Delta \text{FFR}_{meas}| < U3D = 0.00055$ and outlet flow differences $< 0.5\%$. Failure extends in $+0.25 T_{decl}$ increments up to $2\times T_{decl}$ cap, else marks `INCOMPLETE` (`WINDOW_NOT_STATIONARY`). |
| **4** | **MAJOR**: Fallback execution lacked audited pool wrapper and safety model. | **RESOLVED** | [`fallback_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/fallback_job.sh#L1-L195) provides full `case_job.sh`-equivalent safety: flock on `.<name>.fallback.lock`, disk gate (`DISK_NEED_GB + 8 GB`), stale refusal, trigger check (`build` refuses unless `NOT_SETTLED`), resumable mpirun loop with signal traps, purge only upon `COMPLETE`. `pimple_fallback.py make-job` outputs atomic pool job JSON. Direct manual `run` command was eliminated. |
| **5** | **MAJOR**: Solve-time host and code provenance missing from case & return rows. | **RESOLVED** | [`provenance.py:37-66`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/provenance.py#L37-L66) runs immediately prior to `case_job.sh` in all pool jobs and `taskG.py`. Captures `host`, `date`, OpenFOAM v2406 build line, sha256 of all 8 driver/wrapper scripts, full template directory content tree hash (`template_sha256`), and as-built case hashes (`system/`, `0/`, `build_info.json`). Written to `<case>/provenance.json` and mirrored to return directory. Read by [`finalise_task.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/finalise_task.py#L145-L171). Old 4 Task T cases moved aside to rebuild inside jobs. |
| **6** | **MAJOR**: Finalisation was fail-open and could publish incomplete tasks. | **RESOLVED** | [`finalise_task.py:8-15, 173-181`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/finalise_task.py#L8-L15) now fails closed (`refuse()`, exit 1) unless: `task_gate.gate()` passes; all expected solves exist and are settled/COMPLETE; all solves share one OpenFOAM build and template hash; reference comparisons exist; and `verify_manifest.sh` passes on the folder. |
| **7** | **MAJOR**: Task G retry logic could loop indefinitely on early build failure. | **RESOLVED** | [`taskG.py:19-24, 136-140, 181-190`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L19-L24) implements durable ledger accounting in `state/taskG_ledger.json`. Every attempt is recorded as `started` before execution; build failures without artifacts are counted (`build_failed`). Hard stop after 2 counted failures (`nf >= 2`). Case lock (rc 3) and disk refusal (rc 5) are recorded as uncounted, and built cases survive for reuse on restart. |
| **8** | **MINOR**: Task G checkpoint atomicity and re-issue rules. | **RESOLVED** | Checkpoints written atomically to `state/` (`taskG_checkpoint.json`, `taskG_iterations_working.csv`). Return files (`taskG_iterations.csv/.json`) published only on exit 0 via `W.issue_atomic` (dated re-issue suffix upon content difference). Restart acceptance verifies `M1_probes` and `M1_outlets` sha256 and checks case `r_scale_k == k`. |
| **9** | **MINOR**: Geometry gate failure flags propagate to M1 results. | **RESOLVED** | Confirmed: all 16 meshes completed with `mesh_gates.json`, `d34.json`, and extensions. Rejection flags (`D2_RELATIVE_THROAT_GATE_FAIL`, `SELF_INTERSECTION`, checkMesh standard failures) propagate to M1 results as required. |
| **10** | **MINOR**: Prescribed-flow implementation and resistance solve consistency. | **RESOLVED** | Prescribed BC logic verified; resistance mode execution unchanged. 18/18 solve completion self-tests and 11/11 prescribed BC self-tests pass in `case_job.sh`. |
| **11** | **MINOR**: Resolution, mesh admission serialisation, numerical guards. | **RESOLVED** | Flock-serialised mesh admission verified; bracket guards $[0.05, 20]$ in Task G verified; D14 12.5 $\mu$m mesh meets resolution targets. |
| **12** | **MINOR**: Task dependency ordering across M $\to$ T2 $\to$ N. | **RESOLVED** | [`make_job.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/make_job.py#L1-L61) and [`make_all_jobs.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/make_all_jobs.sh#L1-L49) encode a complete pool dependency DAG: Task T $\to$ `gate_TaskT` $\to$ `taskG_14_T1regen` $\to$ `gate_TaskG` $\to$ Task M $\to$ `gate_TaskM` $\to$ Task T2 $\to$ `gate_TaskT2` $\to$ Task N baseline $\to$ Task N other solves $\to$ `gate_TaskN`. |

---

## 3. Evaluation of the New Codebase

1. **Syntax & AST Verification:**
   - `bash -n` clean across `case_job.sh`, `fallback_job.sh`, `make_all_jobs.sh`, `run_geom_mesh.sh`, `queue.sh`.
   - `py_compile` clean across `wo_common.py`, `provenance.py`, `task_gate.py`, `make_job.py`, `taskG.py`, `finalise_task.py`, `pimple_fallback.py`.
   - `taskG.py --plan-only` executed cleanly: $k_2 = 0.893139$, all 29 baseline probes loaded.
   - `case_job.sh --self-test` executed cleanly: 18/18 completion tests and 11/11 prescribed BC checks passed.

2. **Resistance-Mode Solve Invariance:**
   - `case_job.sh` maintains strict separation between prescribed mode and resistance mode. The coded BC derivation from `0/p`, serial compile smoke (2 iterations), `mpirun` execution, `reconstructPar -latestTime`, post-processing, and processor purge operate identical to Lane 2 production.

3. **Provenance Completeness:**
   - Verified live via `provenance.collect()`: extracts host (`Azan`), OpenFOAM build (`v2406 _1653fa08-20260127`), template content hash (`7052192e6d61...`), and hashes of all 8 core Python and Bash code files.
   - Provenance is collected at solve start, written into `<case>/provenance.json`, copied to the return folder, and verified by `finalise_task.py`.

4. **Fail-Closed Gate & Dependency Chain Logic:**
   - Verified live: running `task_gate.py TaskT` on empty returns yields exit code 1 (`GATE TaskT: FAIL (0/5 solves complete)`).
   - Running `task_gate.py TaskG` yields exit code 2 (`NO EXPECTED LIST: ledger unreadable`).
   - Running `finalise_task.py TaskT` yields exit code 1 (`FINALISE REFUSED`).
   - In `pool.py`, any non-zero exit from a gate marks it `failed rc=1`, which permanently halts all downstream jobs via `bad = [a for a in j.get("after", []) if status(a) not in (None, "starting", "running", "done")]`.

---

## 4. Numbered Findings

### MAJOR FINDINGS

#### 1. Scan-14 Fallback Probe Interface Disconnect on `p000`
- **Location:** [`wo_common.py:140`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/wo_common.py#L140), [`taskG.py:102`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L102), [`pimple_fallback.py:58-60, 771`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/pimple_fallback.py#L58-L60)
- **Description:**  
  In `pimple_fallback.py`, scan-14 geometries cannot represent probe `p000` with a valid single-lumen section (it cuts the merged left-main bifurcation). `pimple_fallback.py` records `p000` in `FFR_probes_missing` and outputs 28 of 29 probes, while marking the transient run `COMPLETE`.  
  However, in `wo_common.py:140`, `usable_fallback()` explicitly rejects any fallback result where `d.get("FFR_probes_missing")` is non-empty (`return f"FFR missing at probes ..."`). Furthermore, `taskG.py:102` enforces `if ids != set(probes): stop(...)`, which requires all 29 probes from the k1 baseline.
- **Impact:**  
  If a scan-14 solve (Task G or Task T) were to fail B1 settle and attempt to consume a fallback, `wo_common.usable_fallback()` would deem the fallback unusable, and `taskG.py` would abort with exit 1.  
- **Operational Status:**  
  Non-blocking for steady production launch because fallbacks are never triggered automatically. If any steady solve fails to settle, the pipeline halts fail-closed at the task gate. This discrepancy must be updated before any scan-14 fallback job is created/audited.

---

### MINOR FINDINGS

#### 2. Gate Re-Run After Failure Requires Operator Status Cleanup
- **Location:** [`task_gate.py:15-16`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/task_gate.py#L15-L16), [`wo1010_pool/pool.py:149`](file:///home/azan/paper6_t6_work/wo1010_pool/pool.py#L149)
- **Description:**  
  When a gate job exits non-zero (e.g. because a solve is not settled), `pool.py` records `.status` as `failed rc=1`. The pool does not re-try jobs with existing status files. Once missing solves or fallbacks are ready, the operator must manually remove `wo1010_pool/jobs/gate_<Task>.status` (along with `.rc`, `.admit`, `.pid`, `.log`) to re-trigger gate execution. This is standard fail-closed pool design, noted for operational awareness.

#### 3. Prohibitive Computational Cost for Scan 14 Narrow Fallback
- **Location:** [`pimple_fallback.py:84-85`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/pimple_fallback.py#L84-L85)
- **Description:**  
  The slow recirculation time $\tau_{slow} = V_{post}/Q_{post}$ scales with $1/A_{throat}$. For scan 14 T5 narrow ($r = 0.151$ mm), the pre-declared window reaches $44\tau_{jet}$ (253k–470k steps), projecting to 7–15 days of wall-clock time at 16 ranks (up to 31 days at the $2\times$ cap).  
  This confirms the validity of the Coordinator Decision to prevent automated fallback execution.

---

## 5. Verdict & Launch Decisions per Task Set

All 34 pool jobs in `/home/azan/paper6_t6_work/wo1010_pool/jobs/` are strictly dependency-chained via pool `after` parameters. Because the pool will not start any job whose dependencies have not completed with status `done`, later sets cannot execute ahead of time.

| Task Set | Included Pool Jobs | Dependency Chain | Verdict | Can `.audited` Marker Be Created Now? |
|---|---|---|---|---|
| **Task T** | `14_T5n_resistance`, `14_T5n_prescribed`, `14_T5w_resistance`, `14_T5w_prescribed`, `14_T5n_12p5_resistance`, `gate_TaskT` | `after: []` for solves; `gate_TaskT` after all 5 solves | **READY** | **YES.** All 5 solve commands build fresh cases, capture solve-time provenance, and run under `case_job.sh`. `gate_TaskT` fails closed if any solve is unsettled. |
| **Task G** | `taskG_14_T1regen`, `gate_TaskG` | `taskG` after `gate_TaskT`; `gate_TaskG` after `taskG` | **READY WITH CONDITIONS** | **YES (with Condition).** Condition: Valid for steady solving. If Task G encounters an unsettled solve, it will stop with exit 4; reconciling `p000` handling in `wo_common.py` is required prior to auditing any scan-14 fallback job. Because it is chained after `gate_TaskT`, it will not launch until Task T passes. |
| **Task M** | 8 solve jobs (`{138, 69, 473, 139}_T1_{res,presc}`), `gate_TaskM` | All 8 solves after `gate_TaskG`; `gate_TaskM` after all 8 | **READY** | **YES.** All meshes ready. Protected by `gate_TaskG`. |
| **Task T2** | 8 solve jobs (`{138, 473}_{T5n, T5w}_{res,presc}`), `gate_TaskT2` | All 8 solves after `gate_TaskM`; `gate_TaskT2` after all 8 | **READY** | **YES.** All meshes ready (138 checkMesh failures disclosed as expected; 473 relative-throat fail flagged). Protected by `gate_TaskM`. |
| **Task N** | `306_base_resistance`, 6 solve jobs (`306_{T1, T5n, T5w}_{res,presc}`), `gate_TaskN` | `306_base` after `gate_TaskT2`; 6 solves after `gate_TaskT2` + `306_base`; `gate_TaskN` after all 7 | **READY** | **YES.** All meshes ready (`306_T5n` meshed and d34 generated). Protected by `gate_TaskT2` and `306_base_resistance`. |

### Concrete Action Summary for Launch:
1. Touch `.audited` markers in `/home/azan/paper6_t6_work/wo1010_pool/jobs/` for Task T:
   - `14_T5n_resistance.audited`
   - `14_T5n_prescribed.audited`
   - `14_T5w_resistance.audited`
   - `14_T5w_prescribed.audited`
   - `14_T5n_12p5_resistance.audited`
   - `gate_TaskT.audited`
2. `.audited` markers for Task G, Task M, Task T2, and Task N may either be placed simultaneously (safe under pool `after` gating) or staged sequentially upon gate completions per operational preference.
