---
source_pdf_path: Resources/applsci-16-00318-v2.pdf
slug: mikolajewska-2026-cps-healthcare
ledger_status: TRIAGED
---

# mikolajewska-2026-cps-healthcare

## Bibliographic
- Title: Cyber–Physical Systems in Healthcare Based on Medical and Social Research Reflected in AI-Based Digital Twins of Patients
- First author / authors (first 3 + et al.): Emilia Mikołajewska, Urszula Rogalla-Ładniak, Jolanta Masiak, et al.
- Year: 2026
- Venue: Applied Sciences
- DOI: 10.3390/app16010318

## One-line claim
This bibliometric review synthesizes evidence on cyber-physical systems (CPS) with AI-based patient digital twins in healthcare, identifying gaps in clinical validation, sensor interoperability, and ethical frameworks while proposing directions for trustworthy, personalized, and scalable digital twin deployment.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Bibliometric review; addresses general digital twin architectures in healthcare, not vascular geometry or segmentation error quantification.
- **Q-B decision flip**: NOT REPORTED. Review covers various clinical domains (stroke, diabetes, neuromusculoskeletal) but does not focus on FFR or specific diagnostic threshold reclassification rates.
- **Q-C BC tuning**: NOT REPORTED. No discussion of haemodynamic boundary condition tuning or compensation for anatomical error.
- **Q-D fidelity / quantity**: MIXED. Review acknowledges that "existing implementations remain predominantly proof-concept, prioritizing architectural novelty over validation rigor" and notes the need for more accurate physiological models. No specific CFD or WSS/OSI cases reported in the extracted text.
- **Q-E data**: Bibliometric analysis of publications 2016-2025 from WoS, Scopus, PubMed, dblp; identified ~400+ papers but no specific clinical dataset or invasive-FFR ground truth.
- **Q-F meshing**: NOT REPORTED. Addresses high-level CPS architecture and interoperability challenges, not segmentation-to-mesh pipelines.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: This bibliometric review identifies critical gaps in clinical validation of health digital twins, highlighting the critical concern that "existing implementations remain predominantly proof-concept, prioritizing architectural novelty over validation rigor." The paper emphasizes that validation, sensor interoperability, and ethical governance are lacking—directly supporting T6's emphasis on validation methodology and the risk that architectural acceptance may precede rigorous structural validation.
- verdict: FULL
- revisit-if: N/A; this is supportive background for situating T6's validation concerns within broader CPS/digital twin field

## Key T6-bearing findings
The paper explicitly states:
> "However, existing implementations remain predominantly proof-concept, prioritizing architectural novelty over validation rigor. Temporal robustness, behavior under missing modalities, subgroup calibration, and clinical plausibility remain critically underexplored."

And identifies the risk that model re-fitting may mask errors:
> "AI models in DTs often function as 'black boxes', limiting clinical trust and interpretability."

It further emphasizes:
> "Ensuring the security of CPS is challenging because adaptive, learning systems behave unpredictably in new environments."

These findings directly align with T6's concern: a digital twin re-tuned to match outlet pressure/flow on a geometrically incorrect model may appear well-validated architecturally while the underlying anatomy/topology is unvalidated.

