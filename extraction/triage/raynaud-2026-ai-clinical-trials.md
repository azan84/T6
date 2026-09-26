---
source_pdf_path: Resources/s44222-026-00487-7.pdf
slug: raynaud-2026-ai-clinical-trials
ledger_status: TRIAGED
---

# raynaud-2026-ai-clinical-trials

## Bibliographic
- Title: AI-enabled clinical trials
- First author / authors (first 3 + et al.): Marc Raynaud, Natalia Trayanova, Roslyn B. Mannon, et al.
- Year: 2026
- Venue: Nature Reviews Bioengineering
- DOI: 10.1038/s44222-026-00487-7

## One-line claim
Proposes an AI-enabled clinical trial engineering framework applicable across medical specialties, integrating data harmonization, tool validation, AI-supported trial conduct (patient-to-trial matching, surrogate endpoints, digital twins), and evidence-based go/no-go decisions, with case studies including cardiac digital twins.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Framework discusses surrogate endpoints and digital twins generically; no coronary segmentation or geometric error studies.
- **Q-B decision flip**: NOT REPORTED. Mentions "externally matched comparator arms" but no specific threshold-based diagnostic reclassification in coronary context.
- **Q-C BC tuning**: NOT REPORTED. Heart digital twins mentioned only for ventricular tachycardia (VT), not coronary hemodynamics or FFR modeling.
- **Q-D fidelity / quantity**: PARTIAL. Notes the iBox surrogate in transplantation and "heart digital twins for ventricular tachycardia" but does not detail spatial CFD, WSS, or CFR/FFR modeling.
- **Q-E data**: NOT REPORTED. Generic framework; no specific coronary dataset, N, or FFR ground truth mentioned.
- **Q-F meshing**: NOT REPORTED. No discussion of segmentation robustness or geometric validation.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Provides broad clinical trial design and digital-twin validation framework; mentions cardiac digital twins but only for VT, not coronary FFR applications.
- verdict: LIGHT
- revisit-if: If paper details the cardiac digital twin methodology for VT and discusses cross-validation or model mismatch issues that generalize to FFR systems.
