# Opus fix 28, attempt 2: post-fix audit findings (../SOL_FIX28.md, ../AGY_FIX28.md: both READY WITH CONDITIONS)
Work only in b2/fix28/ (snapshot fix28_a1_snapshot/: do not edit). No real runs, no solvers; foreground tests only; leave no processes. Another project's solver jobs are running on the host (busy): the runner-path tests will refuse with 'host busy' there, that is expected; do not try to work around the guard.
1. N1: accept the elapsed-zero case (remaining == the full duration) as well as the 'starts with 9' case, without weakening the check otherwise.
2. N5: do not hard-code the live watcher's argument (43200); read it from the live watcher process (or skip N5 with an explicit SKIP line when no live watcher exists) and assert recognition + remaining coverage consistent with that argument.
3. Write fix28/FIX28_REPORT.md (attempt 1 and 2 changes, the audits' verdicts, test outputs; note that the runner-path tests need an idle host and are run by the coordinator in the exclusive window).
bash -n; run the suite once (expect host-busy refusals for the runner-path cases; report the counts honestly). Exit when done.
