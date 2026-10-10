# JBHI practice benchmark: code/data availability and reporting (2024-2026)

Date: 2026-10-09. Journal: IEEE J Biomed Health Inform (ISSN 2168-2194). Method: 20 papers whose full text was read via PMC author manuscripts (7), IEEE Xplore open-access PDFs (7), arXiv accepted/preprint versions (5), plus one NIH-PMC page set; repositories named in papers were opened (GitHub API/README/file tree, Hugging Face, OpenI, project page).

## Limits (read first)

- Full-text access is the constraint: the sample is the JBHI 2024-2026 papers that are open access (IEEE gold/hybrid), NIH-funded (PMC), or on arXiv. Closed-access JBHI papers were not readable. NIH-funded and arXiv-posting authors are probably more open than the journal average, so repository rates here are likely biased upward.
- The truly mechanistic in-silico subgroup (cardiac EP model, FSI valve model, ECG-imaging forward/inverse model) is small (n=3) and JBHI digital-twin special-issue papers were not found in a readable form. The modelling subgroup (n=6) adds two simulation-trained surrogate/ML papers and one simulation-dataset paper.
- Two arXiv items are not the final version: Taskén (v1, Nov 2025) and Ericsson's repo statement was read in the PMC author manuscript (final). MCSeg is arXiv v2 (Sep 2026). Statements added at proof stage could be missing for Taskén.
- "None found" in column E means no CI/test/correction in the passages located by keyword search plus the results sections I opened; it is not a line-by-line audit of all 20 papers. Counts for E and F are therefore lower bounds. Columns A-D and H are firmer (statements and repositories were read directly).
- Excluded as non-comparable: two position papers (Viceconti et al., 10.1109/JBHI.2023.3323688; Extending Credibility Assessment of In Silico Medicine Predictors, 10.1109/JBHI.2025.3552320: no data or code by design); Beetz et al. 10.1109/JBHI.2024.3389871 (only arXiv v1, July 2023, read; no code/data statement in v1, final unknown); a non-cardiovascular paper (Predicting Effort to Mend Auto-Segmentations, 10.1109/JBHI.2025.3623042) which states "The datasets and codes from this research are available from the authors upon request for research purposes." (the only "on request" statement met in any paper read). Not counted in the tables.

## 1. Table (20 papers)

Groups: M = modelling/in silico/simulation (1-6); S = segmentation/imaging with quantitative use (8-13); O = other cardiovascular (7, 14-20).
A code, B data, C simulation case files / figure sources / raw outputs deposited, D location of statement, E statistics, F supplementary, G pages (published page range, or accepted-manuscript count for early access).

| # | Grp | Authors, title, year, DOI | A Code | B Data | C Sim/raw/figure files | D Where | E CI / clustering / multiplicity | F Suppl. | G Pp |
|---|---|---|---|---|---|---|---|---|---|
| 1 | M | Gómez M, Carro J, Pueyo E et al. In Silico Modeling and Validation of the Effect of Calcium-Activated Potassium Current on Ventricular Electrophysiology in Heart Failure. 2025. 10.1109/JBHI.2024.3495027 | None stated | None stated (human failing-heart tissue data not shared) | No | n/a | No CI (tolerance intervals in suppl.); n/a (cell/1-D fibre sims); no correction | Yes: sensitivity analyses, tolerance-interval statistics, current traces S9-S24 | 9 |
| 2 | M | Arminio M, Carbonaro D, Gallo D et al. Patient-specific Biomechanical Investigation of Percutaneous Pulmonary Valves: Towards the Integration of ... 2026 (early access). 10.1109/JBHI.2026.3708991 | None stated | None stated (3 patient cases, CT/clinical) | No | n/a | No inferential statistics; case-based | Yes: Supplementary Video | 14 |
| 3 | M | Ericsson L, Hjalmarsson A, Akbar MU et al. Generalized Super-Resolution 4D Flow MRI - Using Ensemble Learning to Extend Across the Cardiovascular System. 2024. 10.1109/JBHI.2024.3429291 | Public GitHub | None stated in paper; README links one example HR CFD file (institutional SharePoint) | Partial: example CFD HDF5 + weights per README; no meshes/case files | End of Methods (implementation paragraph) | No CI; KS tests p<0.05 on 10% sampled voxels; no clustering (n=1 CFD subject/domain); no correction | Yes: Suppl. I (p-values), II (manifold analysis); also in repo | 12 |
| 4 | M | Shin M, Seo M, Yoo S-S, Yoon K. tFUSFormer: Physics-Guided Super-Resolution Transformer for Simulation of Transcranial Focused Ultrasound Propagation in Brain Stimulation. 2024. 10.1109/JBHI.2024.3389708 | Public GitHub | Derived data deposited (Zenodo simulation datasets; CT excluded for privacy) | Yes (repo test_results/*.txt seen); simulation datasets on Zenodo (link in README, not opened); no CT/meshes | Separate section "VII. DATA AVAILABILITY" | No CI (mean +/- SD); one-way ANOVA + Tukey HSD (multiplicity handled); clustering not stated | No | 12 |
| 5 | M | Shenoy N, Toloubidokhti M, Gharbia O et al. A Novel 3D Camera-Based ECG-Imaging System for Electrode Position Discovery and Heart-Torso Registration. 2025. 10.1109/JBHI.2024.3520486 | None stated | None stated (clinical CT/ECG, ethics ref given) | No | n/a | No CI (95th-percentile errors); per-patient averaging; no tests | No | 14 |
| 6 | M | Taskén AA, Judge T, Berg EAR et al. Estimation of Segmental Longitudinal Strain in Transesophageal Echocardiography by Deep Learning. 2026. 10.1109/JBHI.2025.3605793 (arXiv v1) | None stated | Derived/simulated data stated released (synTEE) | Claimed (simulated sequences with ground-truth motion); URL landing page read as placeholder | Methods body + reference [26] with URL | No CI (Bland-Altman 95% limits of agreement); clustering not stated; no correction | Not seen | 12 |
| 7 | O | Skoric J, D'Mello Y, Plant DV. Generative Reconstruction of Multimodal Cardiac Waveforms From a Single Vibrational Cardiography Sensor. 2025. 10.1109/JBHI.2025.3561071 | Public GitHub | Not public (explicit) | No | Separate section "VI. DATA AVAILABILITY" | No CI; leave-one-out CV (grouping not specified); no tests | No | 12 |
| 8 | S | Xing F, Liu X, Aganj I et al. Variance Extrapolated Class-Imbalance-Aware Domain Adaptive Myocardial Segmentation in Multi-Sequence Cardiac MRI. 2026. 10.1109/JBHI.2025.3649765 | None stated | None stated (in-house multi-scanner MRI) | No | n/a | No CI; p<0.01 reported (test not named in text read); no clustering; no correction | Yes: NIHMS supplement PDF (content not read) | 10 |
| 9 | S | Ye Z, Zheng H, Zhang T. MCSeg: Pre-training and Fine-tuning Volumetric Pyramid Transformer for Multi-modal Cardiac Image Segmentation. 2026 (early access). 10.1109/JBHI.2026.3733783 (arXiv v2) | Public repo (OpenI) | Public datasets only (ImageCHD, MM-WHS, HVSMR-2.0, MSD Heart) | No | Abstract + Discussion (no separate section) | No CI; Wilcoxon signed-rank vs MCSeg; correction not stated | Yes: ablations in "supplementary materials" | 9 |
| 10 | S | Ghouse H, Alsharqi M, Nezami F et al. PULSE: A Unified Multi-Task Architecture for Cardiac Segmentation, Diagnosis, and Few-Shot Cross-Modality Clinical Adaptation. 2026 (early access). 10.1109/JBHI.2026.3725919 | None stated | Public datasets only (ACDC, Sunnybrook, M&Ms-2, CAMUS) | No | Separate section "VII. DATA AVAILABILITY" | Bootstrap 95% CI (macro-AUC); Wilcoxon on paired per-patient Dice; correction not stated | No separate file | 14 |
| 11 | S | Fermann BS, Nyberg J, Remme EW et al. Cardiac Valve Event Timing in Echocardiography Using Deep Learning and Triplane Recordings. 2024. 10.1109/JBHI.2024.3373124 | None stated | None stated (states data are not public) | No | n/a | None found | No | 10 |
| 12 | S | Wan J, Li W, Adhinarta JK et al. TriSAM: Tri-Plane SAM for Zero-Shot Cortical Blood Vessel Segmentation in VEM Images. 2025. 10.1109/JBHI.2025.3577625 | Public GitHub + project page | Public volumes + derived annotations deposited (Hugging Face BvEM) | No (annotations, not outputs) | Abstract | None found | No | 10 |
| 13 | S | Jeong H, Jeon J, Yoon YE et al. Multi-Task Deep Learning Framework for Real-Time Quality Assessment and Probe Guidance in Echocardiography. 2026 (early access). 10.1109/JBHI.2026.3717967 | None stated | None stated | No | n/a | None found (5-fold CV) | In-text appendix only | 15 |
| 14 | O | Mendoza A, Tume S, Puri K et al. Clinical Features and Physiological Signals Fusion Network for Mechanical Circulatory Support Need Prediction. 2025. 10.1109/JBHI.2024.3510217 | None stated | None stated (single-centre CICU data) | No | n/a | No CI/tests found; 10x repeated stratified k-fold (patient grouping not stated) | No | 9 |
| 15 | O | Ding C, Guo Z, Rudin C et al. Learning From Alarms: A Robust Learning Approach for Accurate Photoplethysmography-Based Atrial Fibrillation Detection. 2024. 10.1109/JBHI.2024.3360952 | Public GitHub + hosted models (M2D web app) | Public dataset cited (Stanford) + private UCSF/UCLA/Emory data, no statement on the private data | No | Separate "Code Availability" section (end matter) | Bootstrap with one sample per patient per draw (repeated measures handled); Wilcoxon; Bonferroni (0.05 to 0.0033) | No | 12 |
| 16 | O | Li H, Ditzler G, Roveda J, Li A. DeScoD-ECG: Deep Score-Based Diffusion Model for ECG Baseline Wander and Noise Removal. 2024. 10.1109/JBHI.2023.3237712 | Public GitHub | Public datasets only (QT DB, NSTDB) | No | Footnote 1 | None found | No | 11 |
| 17 | O | Alkhodari M, Hadjileontiadis LJ, Khandoker AH. Identification of Congenital Valvular Murmurs in Young Patients Using Deep Learning-Based Attention Transformers and Phonocardiograms. 2024. 10.1109/JBHI.2024.3357506 | Public GitHub (transformer network, MATLAB) + third-party feature code | Public dataset only (PhysioNet/CinC 2022) | No | Separate section "DATA AVAILABILITY" | 95% CI for AUROC/AUPR; t-test/ANOVA for cohort characteristics; no clustering statement; no correction | No | 12 |
| 18 | O | Plaza-Seco C, Baksh M, Barner KE, Blanco-Velasco M. DeepTWA-TM: Deep Learning T-Wave Alternans Detection in Ambulatory ECG via Time Analysis. 2025. 10.1109/JBHI.2025.3553789 | None stated | None stated | No | n/a | No CI; patient-wise permutation folds, text says "cannot be considered as a statistical test" | No | 11 |
| 19 | O | Reznichenko S, Whitaker J, Ni Z et al. AI-Based QRS Onset Detection in the Early Ventricular Activation Site ECGs. 2026. 10.1109/JBHI.2025.3605298 | None stated | Public datasets cited (QTDB, LUDB, PhysioNet) + own pacing dataset cited to earlier paper; availability not stated | No | n/a | None found; patient-level split | No | 14 |
| 20 | O | Liu L, Lu H, Whelan M et al. CiGNN: A Causality-Informed and Graph Neural Network Based Framework for Cuffless Continuous Blood Pressure Estimation. 2024. 10.1109/JBHI.2024.3377128 | None stated | None stated (data "from previous study") | No | n/a | Student's t-test p<0.05; no CI found; no correction | No | 13 |

Verbatim statements (A/B):

1. Ericsson (#3): "Complete setup and trained weights are publicly available at https://github.com/LeonEricsson/Ensemble4DFlowNet ." Repo README: "We provide an example dataset [here]" (SharePoint link).
2. Shin (#4): "The dataset, source code, and description are available at https://github.com/iangilan/tFUSFormer." Repo README: "You can download training, validation, and test datasets from [here](https://zenodo.org/uploads/10791265). Due to privacy concerns, CT images are excluded."
3. Taskén (#6, arXiv v1): "The complete dataset has been released for access by researchers [26]." [26] = https://kiss.folk.ntnu.no/jbhi/ whose page reads "This is a placeholer for the simulated data we created for our JBHI publication."
4. Skoric (#7): "The dataset associated with this study is not publicly available. The code associated with this study is available at: https://github.com/jamesskoric/VCG-Generative-Reconstruction"
5. MCSeg (#9): "Codes and pre-trained ViT-B weights are open-sourced at https://openi.pcl.ac.cn/OpenMedIA/MCSeg." Discussion: "we have open-sourced our pre-trained ViT weights, the fine-tuned downstream model weights, and the complete source code".
6. PULSE (#10): "This study utilizes four publicly accessible cardiac imaging datasets covering MRI and echocardiography modalities. All datasets are released for research use and were obtained under their respective data usage terms." No code statement.
7. Fermann (#11): "future use and validation of this method is difficult without publicly available data sets. Future work using triplane data should strive to create a shareable data set."
8. TriSAM (#12), in abstract: "Our dataset, code, and model are available online at https://jia-wan.github.io/bvem ."
9. AF alarms (#15), "Code Availability": "All code of this work can be accessed at https://github.com/chengding0713/Cluster-membership-consistency . As an alternative to researchers who are just interested in testing models reported in this paper, we hosted all the trained models in this study through a web application ModelMeetsData (M2D)".
10. DeScoD-ECG (#16): body text "the source code will be freely available if this work is accepted" with footnote 1 giving https://github.com/HuayuLiArizona/Score-based-ECG-Denoising.git
11. Murmurs (#17), "DATA AVAILABILITY": "The dataset used in this study was part of the George B. Moody PhysioNet 2022 challenge which is publicly available at: https://moody-challenge.physionet.org/2022/ ... The transformer network was developed in MATLAB for the first time and can be obtained from here: https://github.com/malkhodari/Transformer_MATLAB.git."
12. Fully silent (no statement of any kind found): #1, 2, 5, 8, 13, 14, 18, 19, 20.

## 2. Counts

### A. Code availability

| Category | All (n=20) | Modelling (n=6) | Segmentation/imaging (n=6) | Other CV (n=8) |
|---|---|---|---|---|
| Public repository with link | 8 (40%) | 2 (33%) | 2 (33%) | 4 (50%) |
| "Available on request" | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) |
| None stated | 12 (60%) | 4 (67%) | 4 (67%) | 4 (50%) |

Mechanistic in-silico models only (#1, 2, 5): 0 of 3 give code. Both modelling papers with a repository (#3, 4) are deep-learning surrogates trained on simulation output. No Zenodo/Code Ocean DOI-archived code was found; all 8 are plain GitHub/OpenI links.

### B. Data availability

| Category | All (n=20) | Modelling (n=6) | Seg/imaging (n=6) | Other CV (n=8) |
|---|---|---|---|---|
| Public dataset(s) only, cited | 4 (20%) | 0 | 2 (33%) | 2 (25%) |
| Derived data deposited | 3 (15%) | 2 (33%) | 1 (17%) | 0 |
| On request | 0 | 0 | 0 | 0 |
| Explicitly not public | 1 (5%) | 0 | 0 | 1 (13%) |
| Public cited plus private data, private not addressed | 2 (10%) | 0 | 0 | 2 (25%) |
| None stated | 10 (50%) | 4 (67%) | 3 (50%) | 3 (38%) |

Note #11 (Fermann) is counted in "None stated" although it says no public data exist.

### C. Simulation case files, figure sources or raw outputs deposited

| | All (n=20) | Modelling (n=6) |
|---|---|---|
| Yes, verified | 1 (5%) (#4 test_results; Zenodo simulation sets listed) | 1 (17%) |
| Partial or claimed only | 2 (10%) (#3 one example CFD file; #6 placeholder page) | 2 (33%) |
| No | 17 (85%) | 3 (50%) |

No paper deposited meshes, solver case files (OpenFOAM/Ansys/ k-Wave inputs) or figure source data. Figure-source files: 0 of 20.

### E and F (lower bounds, see Limits)

- CIs reported: 2 (10%) (#10 bootstrap CI, #17 95% CI); Bland-Altman limits of agreement in 1 (#6). Modelling subgroup: 0 of 6.
- Clustering/repeated measures explicitly handled in the analysis: 4 (20%) (#15 one sample per patient per bootstrap draw; #10 per-patient paired test; #18, #19 patient-wise splits). Modelling subgroup: 0 of 6.
- Multiple-comparison control: 2 (10%) (#15 Bonferroni; #4 Tukey HSD). Modelling subgroup: 1 of 6.
- Inferential tests present: 8 (#3, 4, 8, 9, 10, 15, 17, 20).
- Supplementary material: 5 (25%) (#1, 2, 3, 8, 9): extra sensitivity analyses and statistics (#1, #3), a video (#2), ablations (#9), unknown content (#8).

### H. Scope of what was released (the 9 papers that deposit code and/or data: #3, 4, 6, 7, 9, 12, 15, 16, 17)

| Code | Evidence | H1 own method/analysis code | H2 figure/table scripts | H3 raw or derived result files | H4 data extracted/re-processed from other studies | H5 simulation case files / meshes |
|---|---|---|---|---|---|---|
| #3 Ericsson | GitHub tree: src/Network, prepare_data, trainers, predictors, evaluation_playground.ipynb, Supplementary Material.pdf | Yes (model, training, inference, CFD-to-patch preparation) | Partial: README "Everything used for quantitative and qualitative evaluation is present in the jupyter notebook evaluation_playground.ipynb" (a "playground", not a figure pipeline) | Weights per README; no result files seen | Not applicable; one example HR CFD velocity file (own CFD) | No (velocity HDF5 only; no meshes or solver files) |
| #4 Shin | GitHub tree: models, train/test, ANOVA*.py, tFUSFormer_analysis_torch.py, test_results/ | Yes (models, training, evaluation, statistics scripts) | Partial: analysis and ANOVA scripts; no figure script seen | Yes: IoU/distance/inference-time text files per model; pretrained models on Google Drive | No | Partial: simulation datasets on Zenodo (not opened); dataset creator script; CT excluded |
| #6 Taskén | Landing page placeholder | No | Unknown | Unknown | Unknown | Claimed (simulated sequences), not verifiable |
| #7 Skoric | GitHub: one notebook + saved_weights.h5 + LICENSE | Yes (single notebook) | Unknown (notebook not run) | Weights only | No | n/a |
| #9 MCSeg | OpenI repo: pretrain/, finetune/, data/ dirs; README | Yes (pretrain and finetune) | Not seen | Weights per paper | Unknown (data/ dir content not opened) | n/a |
| #12 TriSAM | GitHub: model/ (main, SAM utils, seeds, 3D seg) + tests; HF dataset | Yes (inference pipeline; no training since zero-shot) | No | No | Yes: BvEM annotations re-processed from three public VEM volumes (Hugging Face) | n/a |
| #15 AF alarms | GitHub: train_AE, train_model, cluster_data, README; M2D web app | Yes (loss, autoencoder, training) | No (paper says AUPRC "is reported in" the repo) | Partial (extra metrics in repo per paper; trained models via M2D) | No | n/a |
| #16 DeScoD | GitHub: main_exp, eval_new, metrics, Data_Preparation, check_points, download_data.sh | Yes | No | Yes: trained checkpoints; no result tables | Scripts only: download and preparation of public QT DB/NSTDB, no extracted data | n/a |
| #17 Murmurs | GitHub: 15 MATLAB files (layers, train_transformer_net.m) | Partial: transformer network only; preprocessing and evaluation not included | No | No | No | n/a |

Counts among the 9 depositors: H1 yes 8 (89%; #6 no); H2 yes 0, partial 2 (#3, #4); H3 yes 1 (#4), partial 2 (#15, #16 checkpoints only), weights-only 3 (#3, #7, #9); H4 yes 1 (#12), scripts-only 1 (#16); H5 yes 0, partial or claimed 2 (#4, #6). Over all 20 papers: H1 8 (40%), H2 0 (0%), H3 1 (5%), H4 1 (5%), H5 0 (0%).

## 3. Answer

Within this sample, "code available on request, with only public datasets cited" is within normal JBHI practice, and a public repository is not the norm. Public code links appear in 8 of 20 papers (40%) and in 2 of 6 modelling papers (33%); the commonest behaviour is saying nothing about code or data (12 of 20 for code; 10 of 20 for data), and none of the three mechanistic in-silico papers (cardiac electrophysiology model, pulmonary-valve fluid-structure model, ECG-imaging model) released code, data, meshes or case files. An explicit "on request" statement is rare in what I read (0 of 20; one non-cardiovascular paper outside the sample used it), so such a statement would put the manuscript ahead of the modal paper, not behind it. The repositories that do exist are machine-learning code, typically plain GitHub links with model, training and inference code and weights; none had figure-regeneration scripts, none carried a DOI-archived release, and only 1 of 9 included data re-processed from other studies (TriSAM) and 1 more only preparation scripts (DeScoD-ECG). Releasing only the authors' own analysis code, without figure scripts or extracted third-party data, therefore matches typical JBHI practice (8 of 9 depositors did exactly that; 0 of 9 released figure scripts). Policy text supports this reading: sharing is encouraged, not required. Caveats: the sample favours open-access, NIH-funded and arXiv-posting authors, mechanistic-model n is 3, and the statistics columns are lower bounds.

Policy text found:

- IEEE Author Center, Research Reproducibility, https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/research-reproducibility/ : "All IEEE authors are encouraged to share their data, code, and other research outputs to facilitate verification and reproducibility of experiments and their conclusions." Also: "Improve the discoverability of your data by hosting it in an easily accessible repository such as figshare, Zenodo, or Dryad." and "Help other researchers view and run your code with Code Ocean, a cloud-based computational reproducibility platform that allows code to be stored, shared, and run in the cloud." (Code Ocean is integrated with IEEE Xplore; "Authors who have published with IEEE in the past five years can upload their code to Code Ocean and link it to the article published in IEEE Xplore"; see also https://innovate.ieee.org/ieee-code-ocean/.) No Code Ocean link was found in any of the 20 papers.
- JBHI, Prepare and Submit Your Manuscript, https://embs.org/jbhi/prepare-and-submit-your-manuscript : "If the data are derived from a publicly available database, the original source and reference must be provided."; "When public datasets are utilized appropriate citations (or URLs) should also be provided for them, while in the case of other than public datasets information regarding their ethical approval (e.g. reference number) should be mentioned in the manuscript."; "For studies involving human subjects, relevant institutional review board (IRB) approval must to be obtained and the paper must state explicitly the reference number of the IRB approval for the study." Page limit text: "14 pages for regular papers and 16 pages for review papers including supplementary material." Dataset papers: "IEEE J-BHI accepts a new type of papers, which describe a dataset." (authors must "provide an e-mail address from where other researchers can ask for permission to use the dataset for research purposes").
- JBHI Editorial Policy, https://www.embs.org/jbhi/editorial-policy/ : no text on data, code or reproducibility found. I did not find a mandatory JBHI data-availability or code-availability statement. The JBHI digital-twin special issue call is at https://www.embs.org/jbhi/special-issues/the-role-of-digital-twin-in-healthcare-current-trends-and-challenges/ (call PDF not read).
- Not found in this search: a JBHI-specific reproducibility checklist or badge (unlike IEEE Access, which runs a Reproducibility Initiative: https://ieeeaccess.ieee.org/news/ieee-access-reproducibility-initiative/, not read in detail).

Observed placement: separate data/code-availability sections exist in 5 of 20 papers (#7, #10, #15, #17, #4) and are all 2024-2026; otherwise statements sit in the abstract (#9, #12), end of Methods (#3), a footnote (#16) or the Methods body with a reference (#6).
