# JBHI benchmark and 8-page plan — Paper 6 (2026-10-03)

## 1. Benchmark set

JBHI publishes almost no CFD or FFR papers. The set below is the closest open-access JBHI work: imaging combined
with a physical or simulation model, with validation against a reference. Full texts were read from PMC or the
accepted arXiv version (extracted texts kept in the session scratchpad `bench/`).

| Paper | Topic | Pages (published) | Figs / tables / refs | Source read |
|---|---|---|---|---|
| Ericsson et al. 2024, 28(12):7239–7250 | super-resolution 4D-flow MRI, in-silico training, in-vivo check | 12 | 6 / 5 / 40 | PMC11735690 |
| Fu et al. 2021, 25(8):3061–3072 | iPhantom: patient-specific computational phantoms for CT dosimetry | 12 | 9 / 1 / 36 | PMC8502243 |
| Shenoy et al. 2025, 3502–3515 | 3D-camera ECG imaging, heart–torso registration | 14 | 16 / 3 / 33 | PMC12272559 |
| Inverse ECG with Gaussian impulse data models (accepted JBHI) | physics-model-based inverse problem | 9 (preprint) | – / 2 / 38 | arXiv 2102.00570 |
| autoStrain, segmental strain in TEE (JBHI 2025) | simulation-trained motion estimation, clinical validation | 13 (preprint) | 6 / 6 / 36 | arXiv 2511.02210 |

**Length across the journal (Crossref, all 2025 JBHI articles, n = 940):** median 12 pages (IQR 11–13). Only 10 %
are ≤ 8 pages. An 8-page paper is short for this journal, so every section must carry a result or a necessary
definition.

## 2. What the benchmark shows

**Headings.** IEEE Roman numerals in capitals, then lettered subsections, then `1)` sub-subsections:
`I. INTRODUCTION` · `II. METHODS` (or `MATERIALS AND METHODS`) · `III. RESULTS` · `IV. DISCUSSION` ·
`V. CONCLUSION`. Headings are short and descriptive (2–6 words). **Results subsections mirror the evaluation
subsections of Methods one to one** (Ericsson: Methods C.1–C.3 ↔ Results A–C; Fu: Validation A–C ↔ Results A–C).
Discussion is split into thematic subsections, one of which is **Limitations** (Ericsson "E. Limitations and future
work"; autoStrain "D. Limitations and Future Work").

**Abstract.** 215–276 words (the JBHI limit is 250). It is either one paragraph or labelled
Objective/Methods/Results/Conclusion/Significance (Fu, inverse ECG). Sequence: clinical context (1 sentence) → gap
(1) → aim (1) → methods (2–3) → results with numbers (2–4) → conclusion and significance (1–2).

**Introduction.** 740–1,210 words. It opens with a broad clinical statement ("HEMODYNAMIC quantification is a
central feature of contemporary cardiovascular medicine…"). It ends with the aim and an explicit contribution list,
either inline "(1) … (2) … (3)" (Ericsson) or bulleted (autoStrain).

**Language.** "We" with active voice is the norm (Fu 69, Shenoy 64, autoStrain 45 occurrences). Mean sentence length
in Results is 18–26 words. Results paragraphs state the number and its comparison directly, then point to the figure
or table. The weaker papers use promotional phrasing ("paving the way", "a significant step forward", "crucial role").
**Paper 6 avoids it**: no evaluative adjectives without a number, no forward-looking claims beyond the evidence.

**Depth and rigour.** The analysis is organised around 2–4 evaluation questions, each with its own Results subsection
and Discussion paragraph. Statistical reporting is moderate:
- uncertainty is reported as mean ± SD (inverse ECG, autoStrain) or as error ranges (Fu, Shenoy);
- Bland–Altman bias and 95 % limits of agreement in the clinical validation (autoStrain);
- formal tests are rare (Ericsson: Kolmogorov–Smirnov p-values, moved to the supplement);
- none reports a pre-registration, a multiplicity correction or a noise floor.

**Implication.** Paper 6's pre-registered design (patient-level mixed models, Wilson intervals, paired McNemar
contrasts, Holm correction, physiological-noise floor, two bed structures) exceeds the benchmark's rigour. It has to
be presented compactly: the design in one Methods subsection, the full statistical detail in the supplement, and the
main text reporting the estimates with intervals.

**Limitations and conclusion.** Limitations take 150–530 words. The conclusion takes 80–155 words and restates the
findings without new claims.

## 3. Page budget (8 pages, IEEE double column)

One full text page holds about 1,000–1,100 words. Five figures and two tables take about 2.3 pages, and about 35
references take about 0.8 page. That leaves **about 5,000 words** for the abstract through the conclusion.

| Section | Words | Content (only what carries a result or a necessary definition) |
|---|---|---|
| Abstract | ≤ 250 | single paragraph; ends with one significance sentence (JBHI requirement) |
| I. Introduction | 650 | clinical context → BC tuning in FFR-CT → the untested question (decision at 0.80 under tuning) → aim → three inline contributions |
| II. Methods | 1,700 | A. Data and cohort · B. Reduced-order FFR model · C. Segmentation error types · D. Boundary-condition protocols · E. Three-dimensional case study · F. Outcomes and statistical analysis (pre-registration, noise floor, deviations) |
| III. Results | 1,300 | A. Decision changes by error type and protocol (H1, H3) · B. Absorption under tuned boundary conditions (H2) · C. Branch loss under fixed and tuned resistance (H6) · D. Three-dimensional case study |
| IV. Discussion | 900 | A. Concealment at calibration · B. Relation to published studies (generic wording, no criticism) · C. Implications for model validation · D. Limitations (~200 words) |
| V. Conclusion | 100 | findings only |
| Back matter | – | pre-registration and code DOIs, data source, acknowledgment |

**Figures (5):**
1. Study design: pipeline from ImageCAS-X tree → lesion insertion → error types → protocols A/B/C → outcomes.
2. P(flip | baseline-FFR band) by error type × protocol, with the noise floor on the same axes (H1, H3).
3. Absorption plane: territory-perfusion residual against ΔFFR, per protocol; the "passes and materially wrong"
   region shaded (H2, the thesis figure).
4. Branch-loss effect under Protocol A against Protocol C (H6).
5. Scan 14 in 3D: pressure along the LAD for baseline and the missed branch under fixed resistances and under
   prescribed flows, with the 0D twin overlaid.

**Tables (2):**
1. Error types and protocols: definition, magnitude, source of the magnitude (measured or declared).
2. Headline estimates: proportion passing validation and materially wrong, and P(flip), per protocol × error type,
   both beds, with Wilson 95 % intervals and the noise floor.

**Supplement** (counts toward the 14-page journal limit; check whether it counts toward the over-length charge):
full mixed-model output, bed-structure results, sensitivity analyses (validation threshold 13/16 %, demand ×0.7/1.3,
the eight pre-exposed instances excluded), verification suite, the scan-14 mesh and M1 deviations, and the full
deviations list.

## 4. What is left out of the 8 pages

- H4 and H5: one sentence in Methods F stating that they are registered and that their results are not part of this
  report (no promise of a follow-up).
- The development history (nine defects) goes to the supplement, with a one-sentence pointer.
- The radius-definition gap: one sentence in the case study, with a limitation entry.
- Literature on segmentation methods, ImageCAS-X benchmarks and CFD meshing: cited, not described.

## 5. Style rules for the draft

- Formal sentences, 18–25 words on average. One idea per sentence. No sentence that carries neither a fact, a
  definition nor a necessary link.
- "We" with active voice in Methods and Results, matching the journal.
- Every claim of size carries its number and interval. No "significant" without a test.
- No promotional or forward-looking language. The Conclusion restates findings.
- Facts, not instructions, in Methods and Results (no "should").
- Prior work described in generic, neutral terms ("published studies report …").
