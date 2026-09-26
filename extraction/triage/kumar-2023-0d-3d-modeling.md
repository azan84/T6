---
source_pdf_path: Resources/101907_1_5.0169867.pdf
slug: kumar-2023-0d-3d-modeling
ledger_status: TRIAGED
---

# kumar-2023-0d-3d-modeling

## Bibliographic
- Title: An open loop 0D-3D modeling of pulsatile hemodynamics for the diagnosis of a suspected coronary arterial disease with patient data
- First author / authors (first 3 + et al.): Sumit Kumar, B. V. Rathish Kumar, Sanjay Kumar Rai et al.
- Year: 2023
- Venue: Physics of Fluids
- DOI: 10.1063/5.0169867

## One-line claim
Patient-specific 0D-3D coupled CFD analysis using lumped parameter network boundary conditions to predict coronary hemodynamics (WSS, OSI, pressure) for early diagnosis of CAD.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Single patient case study; no systematic perturbation or uncertainty quantification.
- **Q-B decision flip**: NOT REPORTED. Study focuses on hemodynamic parameter estimation, not FFR threshold classification.
- **Q-C BC tuning**: Yes, central to method. "We successfully built and implemented a coronary boundary condition that relates a lumped parameter coronary vascular simulation to each coronary outlet of the three-dimensional finite element model of the aorta and epicardial coronary arteries. When attempting to depict the intramyocardial pressure by considering the interactions between the artery system, we used both a lumped parameter model and an open loop model." States: "This open loop modeling approach with lumped parameter-based physiologically and geometrically realistic outflow pressures will help cardiologists to analyze medically imaged coronary arteries and compute hemodynamic parameters to assess their patients' risk of coronary arterial disease (CAD)." Key insight: "It is challenging to make an accurate diagnosis of a patient and choose an appropriate therapy for them just based on the data that were observed using CCTA." Acknowledges: "previous research demonstrated that the effects of cardiac movement were secondary and did not influence the pressure and flow fields as much as geometry and boundary conditions." No statement on re-tuning after geometry change.
- **Q-D fidelity / quantity**: 0D-3D coupled model. Reports WSS, TAWSS, OSI, RRT distributions. Full 3D CFD in coronary tree coupled to lumped parameter model for systemic circulation.
- **Q-E data**: Private clinical data. Single case study (51-year-old male patient from BHU Hospital). Patient-specific CCTA acquired; no invasive FFR ground truth mentioned.
- **Q-F meshing**: Detailed meshing strategy described: "SimVascular" software used for 3D modeling; discusses path planning, 2D segmentation via level set method, lofting, and 3D volume rendering. Mentions challenges in automated vs. manual segmentation but does not specifically address robustness on topologically incorrect geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates practical 0D-3D coupling with lumped parameter BC for patient-specific coronary analysis; directly relevant to T6's BC tuning investigation but limited by single-case design and lack of geometric perturbation study.
- verdict: FULL
- revisit-if: Multi-patient validation study comparing 0D-3D results against invasive FFR and exploring sensitivity to segmentation error.
