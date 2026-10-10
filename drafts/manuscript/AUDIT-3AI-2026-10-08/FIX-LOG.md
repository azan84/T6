# Fix log: three-AI audit (Agy, Codex, Claude), 2026-10-08

Simulated audit: findings were fixed or declined here, not in a response letter.

Workflow:
- Opus planned the fixes (`FIX-PLAN.md`).
- A JBHI benchmark of 12 papers decided the contested items (`JBHI-BENCHMARK-AUDIT.md`).
- Fable audited the fixes (`FABLE-FIX-AUDIT.md`).
- Backups: `*-backup-2026-10-08-pre-3ai-audit.*` (main, supplement, refs, cover letter). The previous upload set and portal abstract are in `submission-JBHI/checks/2026-10-08-pre-3ai-upload/`.

## Outcome
- 119 findings. Fable re-checked the text: 83 resolved, 14 partial, 22 declined with justification, 0 not addressed.
- Fable's verdict was READY WITH MINOR FIXES. All five must-fix items and both optional items were applied:
  - comma splice in Limitations;
  - abstract changed to "reduced topological changes";
  - abstract changed to "recomputed fractional flow reserve" (no abbreviation in the abstract);
  - III-A sentence on the 22% / 89% pass rates reworded;
  - noise floor restated as "normal about the clean value";
  - S6 now uses the test–retest wording;
  - forward pointer removed from II-B.
- Operator decisions:
  - Follow JBHI practice: no hash, no pre-registered plan, no post hoc or exploratory labels. These were removed from the main text, the supplement and Fig. S1.
  - Fig. S1 shows the process only, without script or module names.
  - Code stays available on request.
- One number corrected: demand is now 2.28 mL/s (137 mL/min), the median over the 150 instances. Every other number was verified against the results files.
- Length:
  - Main text: 8 pp. Page 8 right column ends at 695 pt, against 731 pt before the fixes.
  - Supplement: 6 pp.
  - Abstract: 249 words.
  - Cover letter: 1 p.
  - Overfull warnings: 9, the same as before (from the template).
- Cover letter (PDF and both portal copies): the "passes … whether or not" claim was replaced. Rates are now given per bed, and the 3D case is described as a single case.
- Upload set rebuilt from `upload_manifest.txt`. The zip builds to 8 + 6 pp with text identical to the working build. The portal abstract was regenerated.

## Acknowledgment and clarity round (2026-10-08, late)
Backup: `main-backup-2026-10-08-pre-clarity.tex`.

### Acknowledgment (`JBHI-ACK-NORMS.md`, 25 JBHI papers)
| Item | JBHI practice found | Action |
|---|---|---|
| Conflict of interest | Stated in the text in 1 of 25 papers | Removed from the paper; declared in the portal and cover letter |
| No-funding statement | No paper has one | Removed |
| Ethics statement for public data | None in public-data papers | Replaced by "public, anonymized ImageCAS dataset" in II-A |
| AI use | IEEE policy places it in the Acknowledgment | Grammarly line kept |
| Thanks to data creators | 3 of 25 papers | Added: "The authors thank the creators of ImageCAS and ImageCAS-X for making their data publicly available." |

### Clarity
- Two independent reviews: `OPUS-CLARITY-REVIEW.md` (10 items) and `FABLE-CLARITY-REVIEW.md` (25 items plus minor ones).
- Applied all 25 Fable items, its minor items, and Opus O7, O9 and O10. O2–O6 overlapped with Fable 3, 5, 22, 23 and 24.
- Opus O1 (a Methods overview) was replaced by Fable 8, which names the bed structures in Intro ¶5.
- Opus O8 was not applied.
- Fable's seam item 2 was also applied in Supplement S7: "lesion-free" in place of "clean".
- Main fixes:
  - "clean model" and "baseline (clean-model) FFR" are defined.
  - "Passes-and-wrong" is defined in II-F.
  - "Clean" (lesion-free) no longer clashes with "clean model" in the 3D section.
  - The IV-A ordinals now have a lead-in.
  - Intro ¶2 pronouns are fixed.
  - Long sentences are split.
  - The threshold is called "stricter than measurement repeatability", as in the abstract.
- Checks:
  - No number changed. The removed citations are still cited elsewhere.
  - Main 8 pp (page 8 right column ends at 660 pt), supplement 6 pp, abstract 249 words, no undefined references, overfull count 9 (unchanged).
  - Upload set rebuilt; the zip build's text is identical to the working build. Portal abstract regenerated.
