1. **MINOR — N1 remains timing-dependent at elapsed zero.** `fix28/test_fix27.sh:383-384`  
   The idle-run output reports `running 0 s, about 100000 s left`, while N1 requires the remaining value to start with `9`. The runner behaved correctly; the assertion caused the failure. This is unrelated to `paused.pids`.

2. **MINOR — N5 is coupled to a specific live-host watcher invocation.** `fix28/test_fix27.sh:399-403`  
   N5 hard-codes `pause_marissa_light2.sh 43200`, but the recorded watcher used `50000`, so recognition succeeded while the assertion failed. The missing `paused.pids` was correctly reported as “not readable” and is not part of N5’s failing condition. This is a harness/environment defect, not a production-code defect.

3. **MINOR — The required fix report is absent.** `OPUS_BRIEF_28.md:5`  
   `fix28/FIX28_REPORT.md` was required but does not exist. The supplied run logs partly provide the evidence, but the requested deliverable remains incomplete.

The driver fix is correct: exit codes are captured immediately after each command in `fix28/b2_driver.sh:7,12-13` and `fix28/b2_driver2.sh:11-12`. Both load waits are bounded at 1,800 seconds and stop before launching further work on timeout (`b2_driver.sh:8-10`; `b2_driver2.sh:6-8`). Syntax checks pass.

The requested test changes do not weaken coverage. N7 now isolates the 1.62-core maximum boundary using 100 controlled samples and explicitly verifies count, mean, and both maxima (`test_fix27.sh:418-432`). N3 merely adds the valid elapsed-zero value while retaining the prior 35900–35999 range (`test_fix27.sh:393`). The deployed scripts tested are byte-identical to their `fix27` counterparts.

VERDICT: READY WITH CONDITIONS
