# JBHI Acknowledgment / related-statement norms (checked 2026-10-08)

## Method and caveats
- Europe PMC / NCBI efetch JATS full text (PMC author manuscripts, NIH-funded, so biased to funded work) and arXiv accepted/preprint PDFs (pdftotext). N = 25 papers (2024-2026): 11 PMC + 14 arXiv. Scratch: scratchpad/ack/.
- The JBHI typeset version was not seen. PMC manuscripts put funding in an "Acknowledgment" section or funding-group (IEEE places it in an unnumbered first-page footnote); arXiv versions show the first-page footnote text but sometimes drop the Acknowledgment. Where the location is uncertain, it is flagged.
- Few JBHI papers in the corpus use ImageCAS/ASOCA. Public-data papers sampled: ADNI, TCGA, IXI/OASIS, PBC/ALL-IDB, Sleep-EDF (PhysioNet), CBIS-DDSM/EMBED, STARE, MIMIC-type EHR.

## Per-paper (A=Acknowledgment, F=first-page footnote)
| Paper | Ack? | Funding location | COI | AI/language | Ethics for data | Dataset thanks |
|---|---|---|---|---|---|---|
| PMC12145120 Frozen VLMs (mammo, public CBIS-DDSM/EMBED) 2025 | Yes, funding only | A: "supported in part by National Institute of Health under Grant R01CA251710" | none | none | none | none |
| PMC11863751 CASiiMIL (3 public WSI sets) 2024 | Yes | A: grants + "solely the responsibility of the authors" disclaimer | none | none | none seen | none |
| PMC11971012 OUD PU learning (claims) 2025 | Yes | A: NIH grants + "views ... those of the authors" | none | none | none | none |
| PMC11875883 AD progression (ADNI) 2025 | Yes, ADNI boilerplate | A: ADNI data-use text (ADNI investigators "did not participate in analysis or writing") | none | none | none | Yes, ADNI mandatory acknowledgment in A + footnote |
| PMC11100861 CiGNN cuffless BP 2024 | none located in JATS | "Funding Statement" (footnote) | none | none | Methods: "approved by relevant Institutional Ethics Committee" | n/a |
| PMC11735690 Super-res 4D Flow (synthetic CFD) 2024 | Yes | A: computing resource ("Berzelius") + ERC/NIH | none | none | Methods: IRB approval for in vivo data | A: "We also thank Ning Jin, PhD, at Siemens ... for providing" sequences |
| PMC11590181 LoMAE 2024 | no section; footnote | F: "supported in part by NIH/NIBIB under grants..." | none | none (ChatGPT only as context) | none | none |
| PMC11422060 DeScoD-ECG 2024 | Yes | A: grants + "views of the sponsors" disclaimer | none | none | none | none |
| PMC11574742 mpMRI series 2024 | Yes | A: "Intramural Research Program of the NIH" | none | none | Methods: IRB, consent waived | none |
| PMC11969577 dBP-Net 2025 | Yes | A: grants | none | none | none | none |
| PMC11970992 CT-HMFM mHealth 2025 | Yes | A: grants | none | none | none | none |
| PMC12229045 GAN inversion colonoscopy 2025 | Yes | A: NIH + Olympus ("funding but not sponsoring") | In A: "All other authors have no conflict of interest to declare" | none | Methods: IRB number | none |
| PMC12313345 Fully hyperbolic NNs 2025 | Yes | A: grants "(to DP)" | none | none | none | none |
| PMC12885328 Myocardial seg. 2026 | Yes | A: Phantomics + NIH | none | none | Methods: IRB protocol number | none |
| PMC13030920 Benchmark, public EHR 2025 | Yes | A: "Duke-NUS Signature Research Programme funded by the Ministry of Health, Singapore" | none | none | none | none |
| PMC13096767 Mend effort 2026 | Yes | A: "funded by a grant from the National Institutes of Health R01CA255748" | none | none | Methods: IRB | none |
| PMC11262011 Eye-tracking review 2024 | Yes | A: Novo Nordisk + NIH | none | none | n/a | none |
| PMC11700499 MEG hyperbolic 2024 | Yes | none stated (no funding) | none | none | Methods: ethics committee + consent | A: "wish to thank Hugo Ramirez for his valuable comments" (person, not dataset) |
| arXiv 2401.05376 eating speed 2024 | Yes | none found | none | none | Methods: KU Leuven IRB | A: "thank the participants" |
| arXiv 2401.10966 HOPE (ADNI/NACC) 2024 | none | none found (preprint) | none | none | Methods: "reviewed by each subject's local review committee" | none |
| arXiv 2404.06421 survival PNN 2024 | none | F: "supported by the PRECISE project ... Grant Agreement No." | none | none | none | none |
| arXiv 2406.09931 SCKansformer (private + public PBC/ALL-IDB) 2024 | none | F: "supported by National Key Research and Development Program" | none | none | Methods: Helsinki, consent waiver, ethics no. (private data only) | none for PBC/ALL-IDB (cited only) |
| arXiv 2411.09874 EEG report 2024 | Yes | none found | none | none | Methods: IRB No., consent waived | A: thanks Prof. Picone "for providing the TUAB" dataset (plus clinician thanks) |
| arXiv 2503.05990 / 2503.06114 / 2504.13754 / 2510.06113 / 2606.30183 (CN groups; TCGA, IXI, OASIS in last two) 2025-26 | none | F: "This work was supported by..." | none | none | Methods (private data only); public TCGA/IXI/OASIS: none | none |
| arXiv 2509.10082 FetalSleepNet (Sleep-EDF from PhysioNet) 2025 | none | F: NIH/Google.org/NHMRC | none | none | Methods: animal ethics + ARRIVE; PhysioNet: cited only | none |
| arXiv 2505.02779 keypoints 2025 | Yes | A + F: grants, "Funding for open access charge" | none | none | none | none |
| arXiv 2605.20458 retinal vessels (STARE etc.) 2026 | none | template placeholder front matter | none | none | none | none |

## IEEE policy (fetched 2026-10-08, journals.ieeeauthorcenter.ieee.org, Submission and Peer Review Policies; WebFetch summary)
- "The use of content generated by artificial intelligence (AI) in an article (including but not limited to text, figures, images, and code) shall be disclosed in the acknowledgments section" (verbatim per fetch). Disclosure should name the system, the affected sections and how it was used.
- Grammar/editing AI use: page said generally not requiring disclosure but recommended (paraphrased by the fetch tool, wording UNVERIFIED). Conflicts: "Conflicts of interest, whether actual, perceived, or potential, must be avoided" (reviewer/editor context). The page has no funding text. The separate "Guidelines for AI-Generated Text" page was NOT fetched: UNVERIFIED.

## Norms table
| Item | Typical JBHI practice | n/N | Recommendation (public ImageCAS/ImageCAS-X, no funding, no COI, Grammarly) |
|---|---|---|---|
| Acknowledgment section | Present mostly in PMC/NIH papers; many arXiv/Chinese-group papers have none (funding in footnote only) | 16/25 present (11 PMC: 10/11); 13 JBHI-arXiv: 3 | Optional. Include a short one only to carry the Grammarly line and dataset thanks |
| Funding location | First-page footnote or Acknowledgment; both occur (PMC shows Ack) | 24/25 funded; footnote ~9, Ack ~14 (typeset location unverified) | No funding: omit footnote. No "no funding" wording was seen (0/25 had a "received no funding" sentence), so do not add one unless the portal asks |
| COI statement in text | Almost never in body | 1/25 (inside Ack, funder-linked) | Omit; declare in the submission portal |
| AI / language-editing disclosure | Not found | 0/25 | Grammarly is editing; IEEE says AI-generated content is disclosed in Acknowledgments. Add one line in Ack: "Grammarly was used for language editing" (low-cost, compatible with the project rule) |
| Ethics for public data | Rare for public data; Methods IRB sentences only for private data | public-only: 0 of ~8 papers; private: ~9 | One Methods sentence: public, de-identified data, original approvals and consent per ImageCAS; no new approval needed |
| Dataset-creator thanks | Rare; ADNI mandatory text; occasional thanks for data provision | 3/25 (ADNI, TUAB provider, Siemens sequences) | Optional single Ack sentence; cite the dataset paper in Methods (norm) and respect any ImageCAS licence/citation requirement |
