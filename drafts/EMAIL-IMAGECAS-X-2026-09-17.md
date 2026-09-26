# Email — request for ImageCAS-X paired re-annotations

**Status:** **SENT 2026-09-18** to kimbr@dtu.dk (CC rapa@dtu.dk). Awaiting reply. Created 2026-09-17; revised
2026-09-18 (deadline pressure removed; tiered ask replaced by a single polite request).
**Follow-up:** if no reply after ~3 weeks, one short courteous nudge; do not chase further. Fallbacks below remain
live regardless.
**Why this matters:** Gate D1b in `STUDY-PLAN-v2.md`. If the paired masks arrive, the paper's strongest arm — running
both annotators' *actual* segmentations, nothing injected — becomes possible. Fallbacks exist but are weaker.

## Before sending — fill these in

- [x] **Recipient address — resolved 2026-09-18 from the paper's own corresponding-author line.**
      **To:** Kit M. Bransby, DTU Compute, Technical University of Denmark — `kimbr@dtu.dk`
      **CC:** Rasmus R. Paulsen — `rapa@dtu.dk` (listed as co-corresponding; DTU group lead).
      Klaus F. Kofoed is the clinical senior author (Copenhagen); CC only if the reply suggests the data decision
      sits with the clinical side. Funding: Novo Nordisk A/S — no bearing on the request.
- [x] **IVUS connection — verified 2026-09-18, same person.** The POLYCORE IVUS paper (Comput Biol Med 2024,
      first author Kit Mills Bransby, Queen Mary University of London, co-authors Zhang / Slabaugh / Bourantas) and
      ImageCAS-X (2026, DTU Compute) share the author. Bransby's own site: PhD at Queen Mary supervised by Zhang,
      Slabaugh and Bourantas; thesis *"Bridging Graph and Dense Representations for Coronary Vessel Segmentation and
      Registration"*; now postdoc at DTU Visual Computing and the CARROT/ARTICHOKE cardiovascular group at
      Rigshospitalet Copenhagen. The opening sentence below now references the graph/topology thesis work rather
      than IVUS generically — it is the more relevant hook, and it is true.
- [ ] **Confirm the acknowledgement / co-authorship offer** with your co-authors before sending.
- [ ] Fill in your title, department and email in the signature.

---

**Subject:** ImageCAS-X — request for the 160 paired re-annotations (inter-observer subset)

Dear Dr Bransby,

I read ImageCAS-X with great interest. The decision to re-annotate the 160 test scans blind, by a second analyst
and without lead-analyst review, is unusually rigorous, and reporting topology explicitly — Betti number error
alongside DSC and clDice — is exactly what the vascular segmentation literature has been missing. It is also very
much in the spirit of your earlier work bridging graph and dense representations for coronary vessels, where
anatomical plausibility rather than pixel overlap was the point.

I am preparing a study on how coronary lumen segmentation error propagates to the binary FFR ≤ 0.80
revascularisation decision in reduced-order and 3D haemodynamic models. The existing FFR-CT sensitivity literature
perturbs lumen geometry by researcher-chosen amounts, typically importing variability magnitudes from unrelated
cohorts, and treats segmentation error as a single scalar. I want to do two things differently: drive the
perturbations from *measured* inter-observer disagreement, and distinguish between error *types* — missed side
branches and other topological errors, stenosis-length error, taper and undersizing — because a reduced-order
model responds to them very differently.

Your inter-observer subset is the best-suited data I have found for this. The published aggregate statistics are
already more defensible than anything else available, but to characterise error *types* I would need the paired
segmentations themselves rather than the summary metrics. Ideally I would build models from *both* analysts'
segmentations of the same scan and compare them directly, so that nothing is synthetically injected at all.

I would therefore like to ask whether you would be willing to share the 160 paired re-annotations — both
analysts' masks for the same scans — alongside the released consensus labels. I fully understand if this is not
possible.

On terms: I would of course cite ImageCAS-X and the ImageCAS source dataset and comply with CC BY 4.0. I would
acknowledge the contribution explicitly, share the resulting error-type characterisation with you before
submission, and would welcome a conversation about co-authorship if you feel the contribution warrants it. I am
equally happy to sign a data-use agreement or work under whatever conditions you prefer. The study will be
pre-registered, and the code and every derived geometry will be released.

There is no hard deadline on my side — I would rather do this properly with your data than quickly without it — so
whatever timeline suits you is fine.

Thank you for assembling and releasing the dataset. The stratified reporting by vessel diameter, lumen attenuation
and coronary segment has already shaped how this study is designed.

With best wishes,

[Name]
[Title], [Department]
Monash University
[email]

---

## If they decline or do not reply

Two fallbacks, in order (STUDY-PLAN-v2 §6, Gate D1b):
1. **Commission a second blinded annotation on ~30 ImageCAS-X cases in-house.** Affordable now that there is no
   deadline, and it yields inter-observer data you own and can release.
2. Calibrate injection magnitudes from the published tables — per-segment DSC (70.9% L-PLA → 95.3% RCA; side
   branches 70.9–83.6%), HD95 2.46 ± 3.62 mm, Betti number error 0.2 ± 0.4, and the stratifiers (DSC vs diameter
   ρ = +0.89, vs attenuation ρ = +0.90, distal decline ρ = −0.36). State plainly that magnitudes are measured but
   error-type apportionment is assumed. Still stronger than 10.1002/cnm.3822, which imported its 6%/15% from
   Schepis 2010 and Leber 2006.
