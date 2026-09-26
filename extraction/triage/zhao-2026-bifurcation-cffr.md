---
source_pdf_path: Resources/s10554-026-03807-5.pdf
slug: zhao-2026-bifurcation-cffr
ledger_status: TRIAGED
---

# zhao-2026-bifurcation-cffr

## Bibliographic
- Title: Diagnostic performance of CT-derived fractional flow reserve across coronary lesion morphologies: a prospective multicenter study
- First author / authors: Na Zhao, Yunqiang An, Lei Song et al.
- Year: 2026
- Venue: The International Journal of Cardiovascular Imaging
- DOI: 10.1007/s10554-026-03807-5

## One-line claim
Prospective multicenter study evaluating CT-FFR diagnostic performance across six lesion morphologies (vessel, location, length, bifurcation, calcification, calcium burden) using invasive FFR reference; identifies bifurcation lesions as a potential reliability boundary.

## T6 targeted questions

- **Q-A geometry perturbation**: Addresses geometric complexity but NOT inter-observer disagreement quantification. Study evaluates lesion-specific anatomical features (bifurcation angle, branch size, calcification, lesion location) that affect FFR calculation. Notes: "Lesion-related anatomical features may influence CT-FFR reliability by affecting lumen segmentation, three-dimensional coronary modeling, boundary conditions, and simulated hyperemic flow behavior." Discussion mentions: "the anatomical heterogeneity of bifurcation lesions, including differences in plaque distribution, branch size, and bifurcation configuration, may increase the difficulty of accurate lumen modeling and matched CT-FFR sampling."

- **Q-B decision flip**: YES. Central to study. FFR <0.80 used as threshold for hemodynamically significant stenosis. Overall accuracy 87.2%, sensitivity 87.0%, specificity 87.3%. Median absolute FFR deviation 0.050. Bifurcation lesions had lower NPV (80.4% vs. 92.0% non-bifurcation), suggesting higher false-negative rate.

- **Q-C BC tuning**: NOT DETAILED in scanned text. Study uses "CFD-based CT-FFR software platform" with "centerline definition" and "application of boundary conditions" as standard steps but no explicit discussion of tuning strategy or re-tuning after geometry changes. Blood flow modeled as "Newtonian fluid governed by the incompressible Navier-Stokes equations."

- **Q-D fidelity / quantity**: 3D CFD-based CT-FFR (Navier-Stokes solver). Focus is on FFR diagnostic performance; does not report WSS, OSI, or other spatially-resolved hemodynamic indices.

- **Q-E data**: Large prospective multicenter cohort: 317 patients, 366 target vessels, with paired CCTA and invasive FFR measurements. Multiple institutions (5 centers in China), November 2018–March 2020. Invasive FFR ground truth present.

- **Q-F meshing**: Discusses segmentation-related geometry challenges. States: "Coronary arteries with a diameter of at least 1.5 mm were analyzed." Notes bifurcation definition required: "bifurcation lesions were defined as stenoses with diameter reduction ≥50% located within 5 mm of the carina of a coronary artery bifurcation." Discussion acknowledges: "the anatomical heterogeneity of bifurcation lesions...may increase the difficulty of accurate lumen modeling." Also notes: "Exact side-branch diameters were not prospectively recorded beyond the ≥1.5-mm eligibility threshold."

## Novelty bearing on T6

- **bucket**: SUPPORT
- **one-line reason**: Large-scale validation of CT-FFR across lesion anatomies; identifies bifurcation geometry complexity as a reliability challenge; supports T6's premise that anatomical complexity affects FFR but shows overall robustness.
- **verdict**: LIGHT
- **revisit-if**: Paper quantifies inter-observer segmentation disagreement or compares FFR predictions to actual inter-segmenter variations.
