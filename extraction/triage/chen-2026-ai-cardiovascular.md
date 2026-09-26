---
source_pdf_path: Resources/fcvm-13-1838415.pdf
slug: chen-2026-ai-cardiovascular
ledger_status: TRIAGED
---

# chen-2026-ai-cardiovascular

## Bibliographic
- Title: From assistance to autonomy: AI agent systems in cardiovascular medicine—a review of paradigms, architectures, and clinical translation
- First author / authors (first 3 + et al.): Chen Y, Qin X, Chen S
- Year: 2026
- Venue: Frontiers in Cardiovascular Medicine 13:1838415
- DOI: 10.3389/fcvm.2026.1838415

## One-line claim
Cardiovascular AI is transitioning from isolated predictive models toward autonomous multi-agent systems capable of structured, verifiable reasoning for clinical decision-making and digital twin integration.

## T6 targeted questions
- **Q-A geometry perturbation**: Not reported.
- **Q-B decision flip**: Mentions "reclassification" in general AI contexts but does not report specific FFR 0.80 threshold flip rates.
- **Q-C BC tuning**: Not directly addressed. Paper discusses digital twin integration but does not detail boundary condition tuning or whether tuning re-occurs after geometry changes.
- **Q-D fidelity / quantity**: 3D CFD not emphasized; focus is on AI architectures for decision support rather than reduced-order or CFD-specific modeling. WSS/OSI not mentioned.
- **Q-E data**: No specific cohort reported. Review cites MIMIC dataset for HeartAgent evaluation (Diagnosis accuracy improvements 36% over traditional methods).
- **Q-F meshing**: Not reported.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Establishes multi-agent reasoning architecture and uncertainty quantification standards for autonomous cardiac systems, relevant to T6's validation and clinical decision framework.
- verdict: LIGHT
- revisit-if: Details on FFR decision-flip rates or specific digital twin validation protocols in coronary applications emerge.
