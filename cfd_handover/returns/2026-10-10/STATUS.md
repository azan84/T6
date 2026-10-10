# WO 2026-10-10 — CFD-side status (live; per-task NOTE.md/INDEX.csv/MANIFEST.sha256 are written by finalise_task.py when each task finishes)

**2026-10-10 20:55 (Malaysia time).** All 14 packages plus 2 extra meshes are built: scan-14 T1 regenerated for Task G, and the D14 12.5 µm narrow-throat mesh. Solves have started.
- **Pre-run audit gate.** Three rounds of auditing by codex GPT-5.6 Sol (`gpt-5.6-sol`) and agy Gemini (`gemini-3.7-flash-medium`). The fixes were written by Opus 5.5 and the reports are in `code_from_cfd/task_1010/audit/` and `opus/`.
  - Round 3 verdicts: Sol rated Task T READY and Tasks G, M, T2 and N READY WITH CONDITIONS (the conditions apply only to a future D15 fallback); Gemini rated every set READY.
- **Order is enforced by fail-closed gate jobs:** T → gate_TaskT → G → gate_TaskG → M → gate_TaskM → T2 → gate_TaskT2 → 306 baseline → rest of N. There is one machine, so the §6 two-machine split is not used.
- **Machine use.** Each solve runs on 16 ranks, two at a time, on 32 logical CPUs.
- **k1 reuse for Task G.** The regenerated scan-14 T1 geometry is byte-identical to the 2026-09-26 build: STL sha256 5f61dffb… and 3,485,528 cells. So k1 = 1 is the returned solve. From it, k2 = ΣQ/ΣT = 0.893139.
- **D15.** A steady solve that does not settle under the B1 rule stops its task at the gate. No pimpleFoam fallback starts automatically: the projected cost per fallback at 16 ranks is about 2.5–5 days for scan 139 and 7–15 days for the scan-14 narrow throat. Any such case is reported to the analysis side first.
- **Gate deviations, solved and returned flagged without repair (D11 / standing rules):**
  - Every mesh except 69 has D3/D4 FAIL.
  - The 138 meshes fail standard checkMesh, as P5 138 did.
  - 139_T1, 306 and 473 fail the relative-throat gate.
  - The surfaceCheck self-intersection gate fails on scan 14, 139 and 306 (whisker sites, plus 1–2-point sites in the narrow-throat window).
  - 306 and 69 fail lesion purity.
- **Code changes:** `--r-scale k` in `build_m1_case.py` (default 1 leaves the output unchanged), a prescribed-flow mode in the job wrapper, and solve-time provenance in every case and return directory.
