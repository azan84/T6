# Fix 28 report (attempts 1 and 2)

Work dir: `b2/fix28/` (copies). Attempt-1 state preserved read-only in `b2/fix28_a1_snapshot/` (not edited).
Nothing deployed to `b2/`. No real runs, no solvers, no mpirun; no processes signalled except the test's own shims; no processes left behind.

## Attempt 1 (OPUS_BRIEF_28.md)

1. **`b2_driver.sh`, `b2_driver2.sh`, rc logging.** `echo "$(date ...) L16 rc=$?"` logged the exit status of the `$(date)` substitution, so it was always 0 (the 09:44 L8x2 refusal was logged as rc=0). Each command is now followed by `rc=$?`, and that `$rc` is what gets logged (L16, L8x2, analyse).
2. **Inter-layout wait.** `b2_driver.sh` used a fixed `sleep 120`, and `b2_driver2.sh` had an unbounded wait. Both now poll every 15 s until the 1-min load is < 0.5, with a 1800 s limit. On timeout they write `STOP: ... not started` to `driver.log` and `exit 4` before launching anything more. The start line logs the load and the time waited. Nothing else changed.
3. **`test_fix27.sh` N7.** N7 now builds its own `host_cpu_samples.csv` instead of mutating I2's live 4-sample CSV: n=100, 99 × 0.05 core plus one sample at 1.61 or 1.62, so the mean is about 0.066, far below 0.48. Only the max boundary (HOST_MAX_MAX 1.62) decides the result. It asserts n, mean < 0.1, both maxima, criterion mode, "1.61 → no host reason" and "1.62 → contended=yes", and that the rule names 0.48 / 1.62 / 20261001_074246.
4. **`test_fix27.sh` N3.** N3 now also accepts `36000 s left`, which is what appears when the watcher is sampled at elapsed 0. The 35900..35999 range is unchanged.
5. **Test target.** The tests run against the deployed scripts in `b2/` (`S=$(cd "$HERE/.." && pwd)`), which are identical to `fix27/`, with `PYTHONDONTWRITEBYTECODE=1`.

Attempt 1 ended without writing this report (audit finding 3).

## Audits of attempt 1

- `../SOL_FIX28.md`: **READY WITH CONDITIONS.**
  1. N1 is timing-dependent at elapsed 0.
  2. N5 hard-codes 43200, but the live watcher runs with 50000.
  3. FIX28_REPORT.md is missing.

  The driver fixes and the N7/N3 changes were judged correct and not weakening.
- `../AGY_FIX28.md`: **READY WITH CONDITIONS**, with the same findings 1–3. It adds finding 4: the drivers must be copied from `fix28/` to `b2/` before use (deployment is the coordinator's job).

  It also judged that neither idle-run failure (`t28_idle.out`: 45 passed, 2 failed, N1 and N5) was a production defect. The missing `paused.pids` was handled correctly ("not readable").

## Attempt 2 (OPUS_BRIEF_28b.md)

1. **N1** (`test_fix27.sh:383-385`). Both assertions (the watcher line and the pre-launch recheck line) now accept `\(9[0-9]*\|100000\)` instead of `9[0-9]*`. The only new case accepted is elapsed 0 (remaining = the full 100000 s). The rest of each pattern is unchanged: form, `for 100000 s`, cmdline, `passed (1 alive, ... >= B2_MAX_RUNTIME_S 14400 s`, rc=3, no WARNING, own light watcher not listed.
2. **N5** (`test_fix27.sh:400-411`). N5 no longer hard-codes 43200:
   - It reads the argument from the live watcher's cmdline (`/proc/<watcher.pid>/cmdline`): the token after `pause_marissa_light2.sh`, or the script's default 36000 if there is none.
   - It asserts the report line for that pid has the light2 form, `for <arg> s`, and the exact cmdline. It also asserts that `running E s` + `about L s left` == `<arg>`, `L <= <arg>`, `L >= 14400`, and that there is no "ends before" WARNING.
   - If there is no light2 watcher at watcher.pid, it prints an explicit `SKIP: N5: ...` line. Before, this line was `N5 skipped: ...`.

## Checks

- `bash -n` passes for `test_fix27.sh`, `b2_driver.sh` and `b2_driver2.sh`.
- **Full suite**, run once in the foreground: `TMPDIR=/home/azan/paper6_t6_work/audit_tmp timeout 590 bash test_fix27.sh`, output in `test_fix28b_run1.out`.
  - Another project's solver jobs were running (load about 22). The runner-path cases were refused with `FAIL: host busy (...)`, as expected (7 such runner refusals).
  - The run **did not finish.** The suite's load waits (up to 300 s each, for example before G2 and N1) ran out on the busy host. The 590 s foreground limit (the tool maximum is 600 s) ended it at the start of section L, so **N1–N7 were not reached in this run.**
  - Results up to section L: **15 PASS, 13 test FAILs.** All 13 failures are runner-path or host-dependent cases:
    - case 1 Windows guard
    - 2 × "pid not listed"
    - entry count
    - postrun classification
    - evidence
    - pid reuse
    - evidence outcomes
    - G2a, G2b, G2c
    - host-level real sampler
    - pause watcher (K)
  - The PASS/FAIL pattern matches attempt 1's busy-host run (`test_fix28_run1.out`, also cut short) for the cases both runs reached.
  - The EXIT cleanup ran: no shims left and the temp dir was removed.
- **N1, targeted check of the new regex.** I took the two patterns exactly from lines 383/384 and tested them against the real elapsed-0 lines 248/249 of `/home/azan/paper6_t6_work/t28_idle.out` ("about 100000 s left", "1 alive, 100000 s left"):
  - Both now **match.** These are the lines that failed in the idle run.
  - These variants still match, as before: 99999, 90000, 9.
  - These variants are still rejected: 100001, 1000000, 89999, 10000, -1.
- **N5, standalone.** I ran the N5 block verbatim, read-only, with the suite's `withhelpers` and the deployed `b2_run.sh`:
  - Result: `PASS: N5 the host's live watcher (pid 2429236: pause_marissa_light2.sh 50000, argument read from its cmdline) ... running 4191 s + 45809 s left = 50000 s, remaining >= 14400 s`.
  - Negative check: forcing the argument to 43200 gives `FAIL: N5`.
  - Negative check: a non-existent watcher.pid gives `SKIP: N5: no live host watcher of the light2 form`.

## Remaining for the coordinator

- The runner-path tests (cases 1–4, A2, E, G2, I2, K, L, N1–N4) need an **idle host**. Run the full `fix28/test_fix27.sh` in the exclusive window, with `TMPDIR=/home/azan/paper6_t6_work/audit_tmp`, preferably twice. That run is the evidence for N1 and N7 through the real runner. The full idle-host result for this attempt is still outstanding.
- Deploy `fix28/b2_driver.sh` and `fix28/b2_driver2.sh` to `b2/` before the next driver use (AGY finding 4).
