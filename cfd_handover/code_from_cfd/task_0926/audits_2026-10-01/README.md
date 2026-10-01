# Audit and bug-protocol records, 2026-10-01
- `b3/`: smoke-test non-reproduction (two steady states of the sten70 case): diagnosis (`B3_DIAGNOSIS.md`), diagnosis audits (GPT-5.6 Sol `SOL_B3_DIAG.md`, Gemini 3.8 Flash `AGY_B3_DIAG.md`), fix 26 briefs (Opus 5.5 attempts 1-3), post-fix audits rounds 1-3 (`*_FIX26*.md`), fixer report `FIX26_REPORT.md`.
- `b2/`: B2 runner change for paused foreign jobs (fix 27): briefs (Opus 5.5 attempts 1-3, Fable 5.1 attempts 1-2), audit prompts and audits rounds 1-4 (`SOL_FIX27*.md`, `AGY_FIX27*.md`); fixer report in `../b2/FIX27_REPORT.md`.
Roles: auditors are read-only; fixes come from Opus 5.5 then Fable 5.1 (bug protocol); the coordinator verifies.
