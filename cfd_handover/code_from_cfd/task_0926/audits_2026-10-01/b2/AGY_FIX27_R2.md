# Pre-Run Audit Round 2: Fix 27 Attempt 2

**Target under review**: [`fix27/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/) ([`b2_run.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh), [`b2_isolation.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py), [`b2_analyse.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py), [`b2_design.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_design.md), [`test_fix27.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/test_fix27.sh), [`FIX27_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/FIX27_REPORT.md)) versus Attempt 1 ([`fix27_a1_snapshot/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27_a1_snapshot/)) and audited originals in [`b2/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/).  
**Briefs**: [`OPUS_BRIEF_27.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/OPUS_BRIEF_27.md), [`OPUS_BRIEF_27b.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/OPUS_BRIEF_27b.md); Round 1 audit [`SOL_FIX27.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/SOL_FIX27.md).  
**Rules followed**: Audit-only; no files modified; `b2_run.sh` not executed against real cases; no solvers or mpirun started; no signals sent; `test_fix27.sh` not executed.

---

### 1. Resolution of Round-1 Audit Findings

1. **Round-1 Finding 1 (MAJOR — Reused PID hiding new running offender): RESOLVED**
   - In [`fix27/b2_run.sh:36`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L36), `prek` accumulates composite tokens `"$pid:$s0 "` using PID and start time `${sf#start=}`.
   - In [`fix27/b2_run.sh:44-45`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L44-L45), the post-run offender scan only skips a process if `[[ "$prek" == *" $pid:${s#start=} "* ]]`. A process reusing a pre-run PID with a new start time is not skipped; it is classified as `new_running` (or `new_stopped`). The pre-run process whose PID was reused is classified as `vanished` at line 38 (`"$s" != "$s0"`).
   - In [`fix27/b2_isolation.py:321`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L321), any `new_running > 0` triggers `contended=yes` ("foreign stopped job resumed during the run").

2. **Round-1 Finding 2 (MINOR — Vanished / new-stopped conservative evidence disposition): RESOLVED**
   - In [`fix27/b2_isolation.py:324-327`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L324-L327), the conservative rule is implemented:
     `if post.get("vanished", 0) + post.get("new_stopped", 0) > 0: unk.append(...)` sets `contended=unknown` unless already `yes`.
   - In [`fix27/b2_run.sh:55`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L55), a matching warning is emitted to stderr.
   - In [`fix27/b2_analyse.py:50-58`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L50-L58), this reason is treated as a non-Windows reason, setting `layout_status = INVALID` and `ratio_status = NOT CLAIMED`.

3. **Round-1 Finding 3 (MINOR — Memory evidence, pressure tracking, and disclosure): RESOLVED**
   - **Disclosure**: [`fix27/b2_design.md:18`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_design.md#L18) explicitly specifies that the measurement is a throughput comparison on a host with ~5.5 GB reserved by paused foreign jobs (not an empty-host result), detailing the ~5.5 GB nominal headroom with 27 GB RAM against the 16 GB L8x2 requirement.
   - **Snapshots**: [`fix27/b2_run.sh:57-67`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L57-L67) implements `mem_snapshot` (`MemTotal`, `MemAvailable`, `SwapTotal`, `SwapFree`, `pswpin`, `pswpout`, `pgmajfault`, `uptime_s`, `epoch`) before launch (line 141) and at completion (line 170), written unconditionally with or without override.
   - **OOM Tracking**: `dmesg_oom` filters kernel OOM lines bounded strictly within the run's uptime window into `dmesg_oom.txt`.
   - **Fault Tracking**: [`fix27/b2_isolation.py:165-167`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L165-L167) samples `majflt` for owned session processes into `owned_majflt.txt`.
   - **Cross-Layout Population & Swap Checks**: [`fix27/b2_analyse.py:113-125`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L113-L125) compares pre-run `pid:start` sets (`stopped_foreign_population`) between L16 and L8x2, recording a ratio note if populations differ, and flags swap growth (`swap_grew_layouts`).

---

### 2. Foreign Job Isolation & Guard Verification

- **Pre-run Admission**: With `B2_ALLOW_STOPPED_FOREIGN=1`, [`fix27/b2_run.sh:111-116`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L111-L116) requires `is_stopped "$pid"` to hold for each process. `proc_states` checks `/proc/<pid>/task/*/stat` and returns non-zero unless every readable thread is `T` or `t`. Any running thread, multi-threaded process with mixed state (e.g. `tS`), unreadable thread stat, or vanished task forces the PID to remain in `OFF1`/`OFF2`, immediately triggering `fail "host busy..."` at line 119.
- **Post-run Classification**:
  - `resumed`: Any pre-run process that increased CPU ticks or whose threads are no longer all `T/t`.
  - `new_running`: Any process matching `PAT1`/`PAT2` not matching a pre-run `pid:start` and not stopped.
  - Both directly set `contended=yes` and invalidate the layout.
- **In-run CPU Capture**: The existing non-owned CPU sampler (`LIN_MEAN_MAX = 0.05`, `LIN_MAX_MAX = 0.20`, `SIB_MEAN_MAX = 0.02`, `SIB_MAX_MAX = 0.10`) remains unchanged.
- **Non-Regression**:
  - Exclusivity guard (`B2_EXCLUSIVE_OK=1`), load average guard (`< 1.5`), disk guard (`>= 10 GB`), Windows pre-run checks (`powershell.exe`), case structure checks (`endTime 1600`), mpirun wrapper binding checks (`b2_rank.sh`), and B1 settle calculation logic are identical to the audited originals.
- **Syntax and Compilation**:
  - `bash -n`: Passed on [`fix27/b2_run.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh), [`fix27/test_fix27.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/test_fix27.sh), [`b2_jobs.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_jobs.sh), [`b2_rank.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_rank.sh).
  - `python3 -m py_compile`: Passed on [`fix27/b2_isolation.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py) and [`fix27/b2_analyse.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py) without touching repository files.

---

### 3. Numbered Findings

1. **MINOR (Operational Condition) — Script deployment location for execution.**  
   [`fix27/b2_run.sh:15,143`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L15,L143)  
   `b2_run.sh` sets `HERE=$(cd "$(dirname "$0")" && pwd)` and executes `setsid "$HERE/b2_jobs.sh"`. The helper scripts [`b2_jobs.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_jobs.sh) and [`b2_rank.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_rank.sh) reside in `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/`, not inside the review subfolder `fix27/`. Furthermore, [`b2_analyse.py:18`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L18) computes its path to `b1_settle.py` as two levels up from `__file__`.  
   *Condition*: The audited files in `fix27/` must be deployed (copied) into `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/` before the real runs are launched.

2. **MINOR (Operational Condition) — Quiescence of foreign queue launchers and watchers.**  
   [`fix27/b2_isolation.py:324`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L324), [`fix27/b2_run.sh:55`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L55)  
   Under the conservative rule, any newly appeared process caught by the watcher during the run becomes `new_stopped`, which marks the layout `contended=unknown` and `INVALID`.  
   *Condition*: Prior to launch, the operator must verify that all foreign launchers, queue loops, and cron-like jobs (such as those in `OpenFOAM_Marissa`) are fully paused and cannot spawn new processes, and that `pause_marissa.sh --watch` does not encounter new processes.

3. **MINOR (Operational Condition) — Constant foreign stopped population across both layout runs.**  
   [`fix27/b2_analyse.py:114-118`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L114-L118)  
   `b2_analyse.py` checks that the `pid:start` set of stopped processes is identical between L16 and L8x2. If any foreign process exits or starts between the two layout executions, the ratio row will flag `stopped foreign population differs between layouts`.  
   *Condition*: The host's stopped process population must remain undisturbed for the entire duration of both runs until analysis is complete.

---

VERDICT: READY WITH CONDITIONS
