1. **MAJOR — Staged tooling is ready, but production deployment is not.** The live `/home/azan/paper6_t6_work/pool/` copies of `pool.py`, `u3d_job.sh`, and `u3d_verdict.py` are not byte-identical to the audited attempt-2 versions. The live jobs directory also retains legacy `A1_D7_12p5.status = running` without `.admit`, `.pid`, or `.rc`, although no associated pool, MPI, or solver process is visible. The new scheduler will correctly refuse this unverifiable legacy state. Before Task B, the coordinator must resolve/archive that stale Task-A record, confirm no old pool job exists, install all three audited files together, install the manifests, and only then create audit markers.

2. **MINOR — `U3D_RETURNS_DIR` remains a mandatory publication condition.** Task B itself does not call `u3d_returns.py`, but final publication must explicitly set:
   ```bash
   export U3D_RETURNS_DIR=/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03
   ```
   Otherwise the downstream tool still defaults to the frozen 2026-09-24 directory.

3. **MINOR — Disk headroom is currently narrow.** Free space is 16.50 GiB. The S12B manifest requires at least 16 GiB free (`disk_gb=6` plus the scheduler’s 10-GiB reserve). Retained reconstructed fields from S25B and S12A may reduce that margin. Recheck/free space before launch and between levels; the scheduler will safely wait if the threshold is not met.

All substantive audit findings are resolved:

- Round-1 Sol 1–7: fail-fast execution, verified reconstruction before purge, per-level results, `flock`, exact FFR denominator and validation, verdict recording, and the 8-rank/regenerated-mesh qualification are implemented.
- Gemini conditions: manifests strictly enforce S25B → S12A → S12B; reconstructed `U`, `p`, and `phi` at the verified final time exist before purge; `U3D_RETURNS_DIR` is documented as an operational requirement.
- Round-2 majors: SETTLED now gates every verdict; the dated 2026-10-03 extension is present and correctly implemented; recovery uses immutable admitted ranks/RAM; and the spawn/recovery race is closed with `starting`, wrapper-written PID identity, token/session verification, and a grace interval.
- Rank and RAM admission are safe, malformed dependencies are rejected, and the single-pool `flock` works.
- The dated extension is scientifically consistent with the original rule and was recorded before Task B runs.
- The three cases remain fresh and unchanged since Round 1. Their newest files predate the Round-1 audits; budgets remain 4000/6000/3000, cell counts remain 3,299,948/6,739,168/7,649,800, decomposition remains 8-rank Scotch, and mesh hard links remain intact.
- Independent solver-free rerun: verdict tests `57/57`, job tests `21/21`, pool tests `26/26`, all passing. Outputs are in [audit_tmp](/home/azan/paper6_t6_work/audit_tmp).

VERDICT: READY WITH CONDITIONS
