---
source_pdf_path: Resources/kd-1-1-6.pdf
slug: seo-2023-kawasaki-disease-cfd
ledger_id: C034
ledger_status: TRIAGED
---

# seo-2023-kawasaki-disease-cfd

## Bibliographic
- Title: Advancing Risk Stratification of Coronary Artery Aneurysms Caused by Kawasaki Disease Using Hemodynamics Analysis and Computational Fluid Dynamics
- First author / authors: Jongmin Seo
- Year: 2023
- Venue: Kawasaki Dis 2023;1(1):e6
- DOI: https://doi.org/10.59492/kd.2023.1.1.e6

## One-line claim
Review of patient-specific CFD studies showing hemodynamic metrics (WSS, particle residence time, FFR) are better predictors of clinical outcomes (thrombosis, myocardial ischemia) than geometric parameters alone in Kawasaki disease coronary aneurysms.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Reviewed studies use patient-specific CT/MRI geometry reconstruction but do not test segmentation uncertainty or geometry perturbation.
- **Q-B decision flip**: YES—MENTIONED. Menon et al. computed FFR with cutoff < 0.80. "The pressure drop induced by the CAA did not lead to FFR values below the cutoff indicating functional significance (< 0.8)." NOT REPORTED: reclassification rates or sensitivity to geometry changes.
- **Q-C BC tuning**: YES—CORE METHODOLOGY. "Rule-based morphometry relationships derived from population studies are used to prescribe the BC at the outlet." "Lumped parameter network (LPN) models consisting of resistances and capacitances are tuned to reproduce the physiologic response." Grande et al. used "closed-loop LPN heart model... fully coupled... LPN values were automatically tuned to match patient-specific clinical data." NOT REPORTED: whether tuning changes with geometry perturbation or compensates for geometric error.
- **Q-D fidelity / quantity**: 3D CFD (Navier-Stokes). Studies compute "velocity, wall shear stress (TAWSS), oscillatory shear index (OSI), and particle residence time (RT)." "WSS and RT were better able to predict the thrombotic risk." NOT EXPLICITLY REPORTED: formal sensitivity analysis of these fields to geometry variation.
- **Q-E data**: Multiple retrospective cohorts. Sengupta et al.: N=1, then N=6 (USA, Russia). Grande et al.: N=10 (Canada, 32 aneurysms). Menon et al.: N=15 KD patients (Japan, USA, 153 coronary arteries). Imaging: CT and MRI. NOT REPORTED: invasive FFR ground truth (Menon et al. notes agreement with catheter measurement).
- **Q-F meshing**: NOT REPORTED. Uses Simvascular; validated against in vitro phantom (PC-MRI with errors 5%-17%) and in vivo data, but no segmentation robustness or topology-handling details.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates CFD-derived hemodynamics (WSS, RT, FFR) as clinically superior metrics versus geometry alone; validates FFR computation with clinical outcomes; describes BC tuning and closed-loop LPN methodology.
- verdict: FULL
- revisit-if: N/A (demonstrates core CFD pipeline, BC methodology, and clinical decision validation relevant to T6).

## Ideation opening (CFD + imaging)
- "Current guideline... heavily relies on the size of the aneurysm" but "patient clinical outcomes were less correlated with the geometric parameters alone," suggesting that imaging-derived geometry alone is insufficient; CFD hemodynamics add predictive power for clinical decision-making in pediatric coronary disease.
