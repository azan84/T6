# Citation search: the physiological-noise SDs (`negatives.py` L52–61; STATISTICS-PLAN §6)

Date: 2026-09-19. Searcher: literature agent. Status of this document: **evidence gathered and verified**;
it proposes decisions, it does not enact them.

Constants under review:

```python
SD_CO   = 0.20          # cardiac output, relative.            PROVISIONAL.
SD_MAP_MMHG = 10.0      # mean arterial pressure, abs. mmHg.   PROVISIONAL.
SD_MU   = 0.15          # viscosity (haematocrit), relative.   PROVISIONAL.
```

---

## TL;DR

1. **The Tanade paper is identified with certainty** (the 50 %/25 % sentence is in it verbatim):
   Tanade C, Chen SJ, Leopold JA, Randles A. *Analysis identifying minimal governing parameters for clinically
   accurate in silico fractional flow reserve.* Front Med Technol. 2022;4:1034801.
   doi:[10.3389/fmedt.2022.1034801](https://doi.org/10.3389/fmedt.2022.1034801). PMID 36561284; PMC9764219.
   Open access; **full text read** (PDF, all sections, tables and reference list).

2. **It publishes SDs for two of our four inputs, and none for the other two.** Table 1 gives a distribution for
   cardiac output and for mean arterial pressure. **There is no SD for heart rate and no SD for haematocrit or
   viscosity anywhere in the paper** — both were deliberately *patient-generalised* (fixed to a cohort constant)
   precisely because the Sobol analysis found they did not matter. §6's phrase "over cardiac output, mean arterial
   pressure, heart rate and haematocrit at Tanade 2022's published standard deviations" **cannot be executed as
   written**: two of the four SDs do not exist.

3. **The "50 % RCA / 25 % LCA at 1 SD of physiological input alone" attribution is WRONG and must be corrected.**
   The figure is real and correctly quoted, but it comes from re-sampling **cardiac output *and stenosis degree***
   simultaneously — stenosis degree at SD = 16.9 percentage points, parameterised from **blinded inter-observer
   disagreement**. Mean arterial pressure was held *fixed* in that analysis. Stenosis degree is an *anatomical
   / observer* error, i.e. exactly the class of error this study injects and asks its detector to catch. Worse:
   Tanade states explicitly that the RCA excess is driven by the **stenosis-degree** term, not the cardiac-output
   term. So the 50 % RCA figure is, if anything, *anti*-correlated with the quantity §6 wants to floor.
   **Using it as a physiological-noise floor is a category error and would set the floor several times too high.**

4. **Tanade does not originate its SDs either** — they are "literature-derived", cited to two references. One of
   them (Dubin 1990) is a **method-comparison** study of Doppler echo vs thermodilution. Its reported ±0.69 L/min
   divided by Tanade's cohort mean cardiac output of 4.5 L/min reproduces Tanade's CoV of 0.153 **exactly**. So
   `SD_CO = 0.153` is, at root, the SD of the *disagreement between two measuring instruments in 18 hospitalised
   patients in 1990* — not physiological variability of any kind.

5. **Recommendations in one line each** (full reasoning in §6):
   - `SD_CO` → **0.05** for the code as currently written (where measurement error is carried separately by
     `WSCV_TARGET`), from a direct biological-variation study in patients (CV_I 5.44 %) corroborated by the only
     hyperaemic CO test–retest dataset (wsSD ≈ 5.0 % rest, 3.1 % adenosine). **0.10** if you intend `SD_CO` to
     absorb measurement error too. Either way **0.20 is unsupported and 0.153 double-counts measurement**; the
     *population* CV of ~0.31 would be wrong by ~6×. Report a sensitivity band.
   - `SD_MAP_MMHG` → **restate as relative and use Tanade's 0.056 (≈ 5.0 mmHg at our P_AORTA = 90 mmHg)**, with a
     sensitivity band up to ~9 mmHg. The current 10.0 mmHg is close to a *population* SD and is roughly double
     what any within-subject source supports.
   - `SD_MU` → **≈ 0.02, not 0.15.** This is the largest single error in the block: about **7–8× too big**.
     It is derivable from a verified primary source (haematocrit CV_I = 2.82 %) through the same viscosity–
     haematocrit law Tanade uses. See §6.3 for the derivation and the sensitivity coefficient.
   - **Heart rate**: leave unrepresented, as `negatives.py` already correctly states. §6 of STATISTICS-PLAN
     should drop it from the list rather than imply it is simulated.

6. **A better floor exists than the one §6 is reaching for.** Two studies measure, empirically, how much FFR moves
   when the *same lesion in the same patient* is re-measured minutes apart under real haemodynamic variation:
   repeat-FFR SD of the difference = **0.018** (Johnson 2015, n = 190 pairs), and band-conditional reclassification
   probability rising to **50 % only at FFR ≈ 0.80 exactly**, and **< 5 % outside [0.75, 0.85]** (Petraco 2013,
   DEFER repeat measurements 10 min apart). That second result is *already expressed on the study's own
   P(flip | band) axes*. **Recommend §6 cite these as the empirical floor and demote the Monte Carlo to a
   mechanistic cross-check.**

---

## 1. Identification of the Tanade paper

**Full citation.**

> Tanade C, Chen SJ, Leopold JA, Randles A. Analysis identifying minimal governing parameters for clinically
> accurate *in silico* fractional flow reserve. *Frontiers in Medical Technology*. 2022;4:1034801.
> doi:10.3389/fmedt.2022.1034801

- PMID **36561284**; PMC **PMC9764219**; published 2022-12-06; open access (CC BY).
- Full text retrieved as PDF and read in full (`https://www.frontiersin.org/journals/medical-technology/articles/10.3389/fmedt.2022.1034801/pdf`).
- Cohort: 50 patients with invasive FFR; 1D–0D reduced-order coronary model; global Sobol uncertainty
  quantification; > 1 million simulations.
- Identification is **certain**, not probabilistic: the exact sentence containing "50 %" and "25 %" is present
  (§3.3, quoted verbatim in §3 below).

Confidence: **high**. This is the right paper.

---

## 2. What Tanade actually publishes, parameter by parameter

The uncertainty distributions are in **Table 1**, captioned *"Input parameter bounds to study the impact of
patient-specificity on FFR."* The table's own footnote fixes the notation:

> "Normal distributions denoted as N(m, s)."

so the second argument **is a standard deviation**, not a variance. Transcribed verbatim:

| Clinical input | Type | Distribution |
|---|---|---|
| Distal location (mm) | Value | N(30.0, 3.5) |
| Cardiac output (%) | Factor | N(1, 0.153) |
| Stenosis degree (%) | Addition | N(0, 16.9) |
| Mean arterial pressure (%) | Factor | N(1, 0.056) |

**Heart rate and haematocrit do not appear in Table 1 at all.**

### 2.1 Cardiac output — SD exists: relative 0.153

- Statistic type: **relative SD (a multiplicative scaling factor)**, dimensionless. Tanade's own words:

  > "Patient-specific cardiac output and mean arterial pressure were varied by multiplying with scaling factors,
  > modeled as normal distributions with means of unity and standard deviations from literature-derived
  > coefficients of variations (27, 54)."

- So: **not** Tanade's own measurement. **Literature-derived**, attributed to refs 27 and 54 (traced in §4).
- Population vs within-subject: **neither, strictly.** See §4 — it traces to an *inter-method measurement
  disagreement*. This is the single most important provenance finding in this document.
- Against our constant: Tanade 0.153 vs our placeholder 0.20. Our placeholder is ~30 % larger.

### 2.2 Mean arterial pressure — SD exists, but it is RELATIVE, not mmHg

- Statistic type: **relative SD = 0.056** (a multiplicative factor), dimensionless. Same sentence, same
  attribution (refs 27, 54).
- Tanade's patient-generalised MAP is **87.3 mmHg** (Table 4), so 0.056 × 87.3 = **4.89 mmHg**.
- **Our code has a units mismatch of intent:** `SD_MAP_MMHG = 10.0` is absolute mmHg; Tanade's figure is a
  *fraction of the patient's own MAP*. At our `P_AORTA = 90 mmHg`, Tanade's equivalent is **≈ 5.0 mmHg** —
  **half** the current placeholder.
- Population vs within-subject: **not stated by Tanade.** Untraced; see §4 and §7.

### 2.3 Heart rate — NO SD IS PUBLISHED

- Heart rate appears in exactly two places, and neither is an uncertainty distribution:
  - **Table 2 (cohort characteristics)**: "Heart rate* (bpm) 70.8 ± 13.7", footnoted *"Values are mean ± SD"*.
    **This is a BETWEEN-PATIENT (population) SD across the 50-patient cohort.** It is emphatically *not*
    within-subject and must not be used as one. **This is the trap flagged in the brief, and it is live in this
    very paper.**
  - **Table 4 (patient-generalised inputs)**: "Heart rate (bpm) 70.8" — a single fixed constant, no dispersion.
- Tanade never propagates heart-rate uncertainty. Heart rate was *removed* from the patient-tuned set.
- Our model is steady anyway, and `negatives.py` already says so explicitly and correctly.

### 2.4 Haematocrit / viscosity — NO SD IS PUBLISHED

- Haematocrit appears only as a fixed patient-generalised constant, **Table 4: "Hematocrit (%) 39.2"**. No SD,
  no CoV, no range, no IQR.
- Viscosity is computed from it, not sampled. Verbatim:

  > "Dynamic viscosity was computed per-patient using an empirical relationship between viscosity and hematocrit
  > from (34): μ = μ₀ / (1 − φ) … where μ is the dynamic viscosity of blood, μ₀ is the dynamic viscosity of
  > plasma, and φ is hematocrit. We assumed a constant plasma hematocrit of 1.2 cP (4, 5, 34)."

  (The phrase "constant plasma hematocrit of 1.2 cP" is a typo in the published paper for *plasma viscosity*.)
  Ref 34 is **Pirofsky B. The determination of blood viscosity in man by a method based on Poiseuille's law.
  J Clin Invest. 1953;32:292–8. doi:10.1172/JCI102738.**
- Resulting mean: *"With an average hematocrit of 39.2 %, the average dynamic viscosity was 1.97 cP."*
  (Note for our own solver: `zerod_ffr.MU = 0.004 Pa·s = 4.0 cP`, roughly **2× Tanade's value**, because Tanade
  uses the low Pirofsky relation. Not an error in our code, but the two are not interchangeable.)
- Tanade's reason for not varying it is stated in the Discussion:

  > "mean arterial pressure, heart rate, and hematocrit did not tangibly influence FFR."

**Answer to question 2 of the brief, stated plainly: Tanade publishes per-parameter SDs for only two of the four
inputs §6 names. For heart rate and haematocrit there is nothing to cite, because Tanade concluded they were not
worth varying.**

### 2.5 The population-SD trap, concretely, in this paper

Tanade's Table 2 offers ready-made *population* SDs that look superficially usable and are **not**:

| Table 2 (population, n = 50) | Table 1 (uncertainty propagated) |
|---|---|
| Cardiac output 4.5 ± 1.5 L/min → CoV **33 %** | CoV **15.3 %** |
| Systolic BP 125.8 ± 25.8 mmHg; diastolic 67.1 ± 12.7 mmHg (MAP SD ≈ 15 mmHg) | 0.056 × 87.3 = **4.9 mmHg** |
| Heart rate 70.8 ± 13.7 bpm | *not propagated at all* |

The population SDs are **2–3× the propagated ones**. Our current `SD_CO = 0.20` and `SD_MAP_MMHG = 10.0` both sit
*between* these two columns — which is what one would expect of placeholders chosen by order of magnitude, and is
exactly the drift the brief was written to catch.

---

## 3. The "50 % RCA / 25 % LCA" claim — VERIFIED AS A QUOTE, REFUTED AS AN ATTRIBUTION

### 3.1 The number is real and correctly transcribed

From §3.3 of the Results, verbatim:

> "Both FFR range and RP curves plateaued after one standard deviation. At one standard deviation, 50 % of cases
> were reclassified in the RCA and 25 % of cases were reclassified in the LCA (Figure 7C)."

So the figures themselves are not in dispute.

### 3.2 But it is NOT "physiological input alone"

The sentence that sets up that analysis, verbatim, immediately preceding it:

> "To test if the impact of patient-specificity in cardiac output and stenosis degree could change treatment
> strategy, we re-sampled the normal distributions of cardiac output and stenosis degree simultaneously while
> restricting distal location and mean arterial pressure to their patient-specific baselines."

And the Figure 7 caption, verbatim:

> "(B) Re-sampling the global parameter space to estimate FFR range and reclassification proportion (RP) when
> **only varying cardiac output and stenosis degree**. Normal distributions of uncertainty were re-sampled at
> increasing levels of standard deviation (SD). (C) Dumbbell plot showing the range of FFR values when re-sampling
> to include 1 standard deviation of the variability in cardiac output and stenosis degree."

(Emphasis added.) Three independent statements in the paper agree. This is not ambiguous.

Therefore, at 1 SD, the perturbation that produced 50 %/25 % was:

| Varied | Held fixed |
|---|---|
| Cardiac output, relative SD 0.153 | Mean arterial pressure (at patient-specific baseline) |
| **Stenosis degree, SD 16.9 percentage points** | Distal location (at patient-specific baseline) |
| | Heart rate, haematocrit (never varied anywhere) |

### 3.3 Why the stenosis-degree term makes this unusable as OUR floor

Tanade's stenosis-degree SD is not physiology. Verbatim:

> "The error bound in stenosis degree was modeled to reflect the worst-case inter-observer variability. The
> difference in stenosis degrees measured by an interventional cardiologist and a researcher, with measurements
> blinded to each other, was used to parameterize a normal distribution of uncertainty. The mean was fixed to zero
> to reflect the case when both observers agreed perfectly."

That is a **geometry / observer** error — the same family as this study's injected anatomical errors. Folding it
into a "physiological-noise floor" would mean floor-ing the detector against a sample of the very signal it is
being asked to detect. The floor would be inflated, and the inflation would be in the direction that makes any
injected-error effect look *indistinguishable from noise* when it is not.

For scale: SD 16.9 percentage points of stenosis degree, against a cohort mean stenosis degree of 55.6 % (Table 2),
is an enormous geometric perturbation — larger than most of the severity bands in our own sweep.

### 3.4 And the RCA/LCA split points the opposite way from §6's use of it

Verbatim, Discussion:

> "…we performed post hoc analyses and discovered that uncertainty in cardiac output had a larger effect on the
> **LCA** than RCA and uncertainty in stenosis degree had a larger effect on the **RCA** than LCA."

So the 50 % RCA figure — the larger, more alarming half of the claim §6 quotes — is the half driven by the
**stenosis-degree (anatomical)** term. The *physiological* term (cardiac output) is the one that acts more on the
**LCA**. §6 currently cites the RCA number as though it were the stronger evidence of a physiological floor; it is
the weakest.

### 3.5 Verdict on question 3

**The claim as written in STATISTICS-PLAN §6 is refuted.** The quotation is accurate; the attribution
("of physiological input alone") is not. §6 must be corrected before registration, and the correction should be
logged as a pre-registration amendment, not a silent edit.

Suggested replacement wording for §6 is in §6.5 below.

---

## 4. Tracing the real source of Tanade's two SDs

Tanade attributes both CoVs to "(27, 54)". From the reference list, transcribed verbatim:

> **27.** Fossan FE, Sturdy J, Müller LO, Strand A, Bråten AT, Jørgensen A, et al. Uncertainty quantification and
> sensitivity analysis for computational FFR estimation in stable coronary artery disease. Cardiovasc Eng Technol.
> (2018) 9:597–622. doi: 10.1007/s13239-018-00388-w

> **54.** Dubin J, Wallerson DC, Cody RJ, Devereux RB. Comparative accuracy of Doppler echocardiographic methods
> for clinical stroke volume determination. Am Heart J. (1990) 120:116–23. doi: 10.1016/0002-8703(90)90168-w

Tanade does not say which CoV came from which reference.

### 4.1 Dubin 1990 — and the exact reconstruction of CoV = 0.153

Dubin 1990 (PMID **2360495**) — **abstract read in full; full text not retrieved** (1990, paywalled). From the
abstract, verbatim:

> "…we compared Doppler with thermodilution stroke volume measurement in 18 hospitalized patients, 16 with an
> acute manifestation of coronary artery disease and two with chronic cardiomyopathies. … It also resulted in the
> most accurate measurement of cardiac output (r = 0.88, p less than 0.0003; **mean difference from thermodilution
> = 0.11 L/min +/- 0.69 L/min**, p = NS)."

Now:

```
0.69 L/min  /  4.5 L/min  =  0.1533…
```

where 4.5 L/min is Tanade's own cohort mean cardiac output (Table 2 / Table 4). This reproduces Tanade's
**0.153 to three significant figures.**

**Confidence: high but INFERRED.** Tanade does not state this arithmetic anywhere. The match is exact and the
reference is cited in the right place, so I am confident, but it should be described as a reconstruction, not as
something Tanade asserts.

**What this means, and it is the crux of this whole document:**

`SD_CO = 0.153` is the **standard deviation of the disagreement between two different measuring instruments**
(Doppler echocardiography vs thermodilution), in **18 hospitalised cardiac patients**, in **1990**. It is:

- **not** a within-subject biological variability (no patient was measured twice by the same method);
- **not** a population SD (the population SD of cardiac output in Tanade's own cohort is 33 %, double this);
- an **inter-method agreement SD**, which is a *third* thing again — and because it is the SD of a *difference*
  between two noisy methods, it is inflated relative to either method alone by up to √2 if the two error sources
  were comparable (0.69/√2 = 0.49 L/min, i.e. CoV ≈ 10.8 %).

It is closer in spirit to what our Monte Carlo needs than a population SD would be — a negative draw *is* the same
patient's target measured imperfectly — but it conflates instrument disagreement with the patient's own variation,
and it is 36 years old.

### 4.2 Fossan 2018 — could not be reached

**NOT VERIFIED.** Fossan et al. 2018 (PMID 30382522, doi:10.1007/s13239-018-00388-w) is paywalled at Springer.
Attempted and failed: Springer (303 to an IdP login), the NTNU Open green-OA copy (the `hdl.handle.net/11250/2622598`
handle now redirects into the NVA/Sikt platform, whose file endpoint returned `Forbidden` / `Missing Authentication
Token`), Europe PMC (`isOpenAccess: N`, no PMCID), and Semantic Scholar (open-access PDF link resolves back to the
same dead NTNU handle). **Only the abstract and indexing metadata were reached.**

Consequence: **I could not determine whether the MAP CoV of 0.056 comes from Fossan, nor what Fossan describes it
as.** This is an open item; see §7.

### 4.3 A comparator that shows the field does not agree on one value

Dalmaso et al. 2025, *Uncertainty Quantification and Sensitivity Analysis for Non-invasive Model-Based
Instantaneous Wave-Free Ratio Prediction*, Int J Numer Method Biomed Eng, doi:10.1002/cnm.3898 (PMC11706247) —
a direct descendant of the Fossan line of work. **Full text read** via PMC. Its Table 3 assumptions:

- Mean aortic pressure multiplier: **N(0.99, 0.09)** → relative SD **9 %**, derived from invasively measured aortic
  pressure waveforms in 63 patients.
- Baseline coronary flow multiplier: **N(0.99, 0.30)** → relative SD **30 %**, derived from comparing four
  different flow-estimation methods across 18 coronary branches.

So across three papers in the same modelling tradition, the assumed flow/cardiac-output relative SD is
**15.3 % (Tanade) vs 30 % (Dalmaso)**, and the pressure relative SD is **5.6 % vs 9 %**. There is a factor of two
in each. **No single literature value is authoritative**, which is itself a finding and should be reported as a
declared sensitivity rather than concealed behind one number.

Note carefully: Dalmaso's 30 % flow figure is *methodological* spread (different estimators disagreeing), not
within-subject physiology either. The same conflation runs through this whole literature.

---
## 5. What the Monte Carlo ACTUALLY needs: short-term within-subject variability

This is the independent half of the brief, and it is the half that governs the answer. A negative draw in
`negatives.py` is **the same patient, measured on a different occasion**. The correct dispersion is therefore the
**within-subject (intra-individual) SD**, and a between-subject/population SD is wrong by roughly a factor of two
for every quantity below.

**Three statistics are routinely confused in this literature, and all three appear in the sources we cite:**

| Statistic | What it is | Relation |
|---|---|---|
| Within-subject SD (wsSD, CV_I) | one patient, repeated occasions | **this is what we want** |
| SD of differences (SDD) | the spread of (visit 2 − visit 1) | SDD = **√2 × wsSD** |
| Between-subject SD (CV_G) | different patients | typically **≈ 2 × wsSD**; never substitute |
| Analytical CV (CV_A) | instrument only | a fourth thing again; small here |

A fifth variant, peculiar to the modelling papers in §4, is the **inter-method agreement SD** (two different
instruments on the same patient) — Dubin 1990 and Dalmaso 2025 are both of this type. It is not any of the above.

### 5.1 Cardiac output — good evidence exists, and it is FAR smaller than any figure currently in play

Two questions have to be separated, because the literature answers them with numbers ~3× apart:

- **(i) How much does the patient's actual cardiac output differ between occasions?** (biological, CV_I)
- **(ii) How much does a *measurement* of it differ between occasions?** (biological + measurement)

**(i) Biological within-subject variation — ≈ 5 %**

- **Täger T, Fröhlich H, Franke J, Slottje K, Horsch A, Zdunek D, Hess G, Dösch A, Katus HA, Wians FH,
  Frankenstein L.** Biological variation of the cardiac index in patients with stable chronic heart failure: inert
  gas rebreathing compared with impedance cardiography. *ESC Heart Fail.* 2015;2(3):112–120.
  doi:10.1002/ehf2.12040. PMID 27708853; PMC5032993. **Full text read.**
  **This is the single most on-point source found**: an explicit *biological variation* study, in *patients*,
  with *repeated measurement of the same subject at weekly intervals* — precisely our negative-draw design.
  n = 50 CHF patients meeting rigid stability criteria; cardiac index by inert gas rebreathing (IGR) and impedance
  cardiography (ICG), weekly over 3 weeks, at rest and at 10 W.
  CV_I is computed by the authors as CV_I = (CV_t² − CV_A²)^½ with CV_A = 2 % taken from the device manuals —
  i.e. **it is a genuine biological within-subject CV with analytical variation removed**:

  | Modality | CV_I, V1 vs V2 | CV_I, V1 vs V3 |
  |---|---|---|
  | **IGR at rest** | **5.44 %** (2.82–9.78) | **5.53 %** (2.32–9.89) |
  | ICG at rest | 1.12 % (0.65–4.26) | 2.99 % (1.70–4.87) |
  | IGR at 10 W | 3.80 % (0.86–8.48) | 4.63 % (3.02–9.38) |
  | ICG at 10 W | 3.34 % (1.76–6.56) | 3.71 % (2.58–6.96) |

  **The population-SD trap, quantified inside this one paper.** Its Table 2 gives IGR-rest cardiac index as
  **2.30 ± 0.71 L/min/m²** — a *between-patient* SD, i.e. a population CV of **30.9 %**. The *within-subject* CV
  in the same patients is **5.44 %**. **The population figure is 5.7× the within-subject figure.** (And 30.9 %
  is almost exactly the 33 % population CV computable from Tanade's own Table 2.) Substituting one for the other
  would inflate the noise floor by nearly a factor of six.

- **Lassen ML, Byrne C, Hartmann JP, et al.** Pulmonary blood volume assessment from a standard cardiac
  rubidium-82 imaging protocol: impact of adenosine-induced hyperemia. *J Nucl Cardiol.* 2023;30(6):2504–2513.
  doi:10.1007/s12350-023-03308-1. PMID 37349559; PMC10682170. **Full text / tables read.**
  **The only hyperaemic cardiac-output test–retest dataset located** — and our model is hyperaemic, so this is
  the directly applicable one. n = 25 healthy volunteers with **repeat rest/adenosine-stress ⁸²Rb sessions,
  median 14 days apart [IQR 6–35]**. Within-subject **repeatability coefficient for cardiac output: 13.8 % at
  rest, 8.5 % under adenosine stress** (stroke volume 8.9 % and 5.6 %).
  **Our conversion, flagged as ours** (RC = 2.77 × wsSD): resting CO wsSD ≈ **5.0 %**; **adenosine-stress CO
  wsSD ≈ 3.1 %**.
  Two things follow. First, it independently reproduces Täger's ≈ 5 % at rest by a completely different modality
  and population. Second, **hyperaemia makes cardiac output *more* reproducible, not less** — maximal vasodilation
  standardises the state. A hyperaemic model is therefore entitled to the *smaller* figure.

**(ii) Measurement-inclusive day-to-day variation — ≈ 9–14 %**

- **Coats AJ.** Doppler ultrasonic measurement of cardiac output: reproducibility and validation. *Eur Heart J.*
  1990;11(Suppl I):49–61. doi:10.1093/eurheartj/11.suppl_i.49. PMID 2092990. **Abstract only.** Review of
  published reproducibility studies; verbatim: *"Short-term variability varies from 4 to 10%, and that over days
  to weeks from 9 to 14%. Thus a single measurement may vary up to +/− 28% over time with no true change in
  cardiac output."* This is the most quotable short-term/long-term split found.
- **McCarthy D, Romano G, Thiessen J, Matharu T, Burr J, Millar P.** Measurement error of cardiac output
  determined by nitrous oxide rebreathing and impedance cardiography in healthy adults. *Appl Physiol Nutr Metab.*
  2025;50:1–10. doi:10.1139/apnm-2025-0234. PMID 41172356. **Abstract only** (publisher 403). n = 60 adults;
  at rest, IGR **CV 11.6 ± 8.5 %** (ICC 0.75), ICG **CV 7.5 ± 8.4 %** (ICC 0.87). ⚠️ The abstract does not state
  whether duplicates were same-visit or separate-visit — **interval unverified.**
- **Sundberg S, Akkila J.** Assessment of cardiac performance: short- and medium-term variability of impedance
  cardiography at rest and during dynamic exercise. *Int J Clin Pharmacol Ther.* 1996;34:93–95. PMID 8705093.
  **Abstract only.** n = 12 healthy men; same-session resting CO/SV **CV 4–6 %**; **between-day resting CV ≈ 12 %**
  (two days 14 days apart).
- **Giraud R, Siegenthaler N, Merlani P, Bendjelid K.** Reproducibility of transpulmonary thermodilution cardiac
  output measurements in clinical practice: a systematic review. *J Clin Monit Comput.* 2017;31:43–51.
  doi:10.1007/s10877-016-9823-y. PMID 26753534. **Abstract only.** 14 adult studies, 3,432 averaged CO values;
  TPTD reproducibility **6.1 ± 2.0 %** — but this is *within-sequence* (bolus-to-bolus), not between occasions.
- **Critchley LA, Critchley JA.** A meta-analysis of studies using bias and precision statistics to compare
  cardiac output measurement techniques. *J Clin Monit Comput.* 1999;15:85–91. doi:10.1023/A:1009982611386.
  **Not read directly**; its content was confirmed from a reachable secondary source, which states the ±30 %
  acceptance threshold "was based on combining notional errors of 20% from each method". ⚠️ **The ±20 % is an
  assumption in that paper, not a measurement** — the secondary source says so explicitly. A "percentage error"
  of 20 % is a 2-SD quantity, so it corresponds to a relative SD of ≈ 10 %. Use it only as an order-of-magnitude
  sanity check, never as a primary citation.

**Convergence.** Biological ≈ **5 %** (two independent modalities, two populations, one of them hyperaemic);
biological + measurement, between occasions ≈ **9–14 %**. Our current `SD_CO = 0.20` exceeds even the upper end of
the measurement-inclusive range, and is **4× the biological figure**.

### 5.2 Mean arterial pressure — no published resting-MAP within-subject SD exists; ≈ 5 mmHg is well supported indirectly

**No source was found that publishes a within-subject SD for resting MAP directly.** This was searched for
specifically and the negative result is reported rather than papered over. What exists is SBP and DBP.

**Primary sources reached:**

- **Muntner P, Shimbo D, Tonelli M, Reynolds K, Arnett DK, Oparil S.** The relationship between visit-to-visit
  variability in systolic blood pressure and all-cause mortality in the general population: findings from NHANES
  III, 1988 to 1994. *Hypertension.* 2011;57(2):160–6. doi:10.1161/HYPERTENSIONAHA.110.162255. PMID 21200000.
  **Abstract only** (AHA full text returned HTTP 403).
  n = 956 US adults ≥ 20 y, **three separate study visits**. Verbatim: *"The mean of the standard deviation for
  systolic blood pressure across visits was 7.7 mm Hg."* This **is** a mean within-person visit-to-visit SD — not
  an SDD, not a population SD. No DBP figure in the abstract.

- **Stergiou GS, Baibas NM, Gantzarou AP, et al.** Reproducibility of home, ambulatory, and clinic blood pressure:
  implications for the design of trials for the assessment of antihypertensive drug efficacy. *Am J Hypertens.*
  2002;15(2 Pt 1):101–4. doi:10.1016/S0895-7061(01)02324-X. PMID 11863243. **Abstract only** (paywalled).
  n = 133 untreated subjects, clinic BP over 5 visits within 3 months; home BP 6 workdays within 2 weeks; ABPM
  twice 2 weeks apart. **Reports SD of DIFFERENCES (SDD), not wsSD** — flagged, because taking these at face value
  would inflate the noise by √2:
  | Modality | SDD systolic / diastolic (mmHg) | **wsSD = SDD/√2** (derived here, not published) |
  |---|---|---|
  | Home BP | 6.9 / 4.7 | 4.9 / 3.3 |
  | 24-h ABPM | 8.3 / 5.6 | 5.9 / 4.0 |
  | Clinic BP | 11.0 / 6.6 | 7.8 / 4.7 |

- **Warren RE, Marshall T, Padfield PL, Chrubasik S.** Variability of office, 24-hour ambulatory, and
  self-monitored blood pressure measurements. *Br J Gen Pract.* 2010;60(578):675–80. doi:10.3399/bjgp10X515403.
  PMID 20849695; PMC2930221. **Full text read.**
  n = 163 recruited (141 office / 107 ABPM / 109 self-monitoring analysable), mean age 46.9 ± 11.7 y, 6-week
  interval. **Within-individual CVs** (their Table 2): office SBP **8.6 %** (7.6–9.6), office DBP **8.6 %**;
  daytime ambulatory SBP **5.5 %** (4.8–6.3), DBP **4.9 %** (4.3–5.6); self-monitored SBP **4.2 %**, DBP **3.9 %**.
  Note these are **combined biological + measurement** variability; no BP source separates the two.

**Deriving a MAP within-subject SD — labelled as our arithmetic, not a published figure.**
Using MAP ≈ (SBP + 2·DBP)/3 with Stergiou's clinic wsSDs (7.8 / 4.7 mmHg), and sweeping the within-subject
SBP–DBP correlation ρ (which **no source reports**, hence the sweep rather than a point value):

| ρ | 0.0 | 0.3 | 0.5 | 0.7 | 1.0 |
|---|---|---|---|---|---|
| MAP wsSD (mmHg) | 4.07 | 4.63 | 4.97 | 5.29 | 5.73 |

**The whole range is 4.1–5.7 mmHg**, and it is insensitive to the unknown ρ. Independently, Tanade's relative SD
of 0.056 applied at our `P_AORTA = 90 mmHg` gives **5.04 mmHg**. Two unrelated routes land in the same place.

**The current `SD_MAP_MMHG = 10.0` is roughly double every within-subject estimate** and is instead close to the
*population* SD of MAP in Tanade's own cohort (≈ 15 mmHg from SBP 125.8 ± 25.8 / DBP 67.1 ± 12.7) and to Warren's
office SBP figure. **This is the population-for-within-subject substitution the brief asked to be flagged, and it
is present in our code today.**

### 5.3 Haematocrit — a clean, high-quality, directly usable within-subject figure exists

This is the best-evidenced of the four constants, and the one currently furthest wrong.

- **Coşkun A, Carobene A, Kilercik M, et al.** (European Biological Variation Study, EFLM WG-BV). Within-subject
  and between-subject biological variation estimates of 21 hematological parameters in 30 healthy subjects.
  *Clin Chem Lab Med.* 2018;56(8). doi:10.1515/cclm-2017-1155. PMID 29605821.
  **Full text read** (PDF from eflm.eu; Table 1 transcribed directly).
  Design: **n = 30 healthy adults** (17 F, 13 M), **blood drawn once weekly for 10 weeks**, duplicate
  measurement, Sysmex XN-3000 — i.e. exactly the short-term, same-subject, repeated-occasion design we need.

  Haematocrit (Htc, %), verbatim from Table 1:
  | | value (95 % CI) |
  |---|---|
  | Mean | 40.2 % (F), 48.1 % (M) |
  | **CV_A (analytical)** | **0.63 %** (0.59–0.69) |
  | **CV_I (WITHIN-subject)** | **2.82 %** (2.59–3.09) — common to both sexes |
  | **CV_G (BETWEEN-subject)** | 5.51 % (4.03–8.41) F; 5.46 % (3.87–9.07) M |
  | Online 2014 BV database (Ricos) comparator | CV_I 2.7 %, CV_G 6.41 % |

- **Corroboration, independent meta-analysis:** Coskun A, Braga F, Carobene A, et al. Systematic review and
  meta-analysis of within-subject and between-subject biological variation estimates of 20 haematological
  parameters. *Clin Chem Lab Med.* 2019;58(1). doi:10.1515/cclm-2019-0658. Haematocrit **CV_I 2.71 %
  (2.24–3.40)**, CV_G 5.45 %, pooled over 6 papers / 13 subgroups.
- **Corroboration, live database:** the EFLM Biological Variation Database (biologicalvariation.eu) currently
  serves haematocrit **CV_I 2.81 %** (95 % CI 2.20–3.12) and CV_G 5.52 %.

**Three independent routes agree on CV_I ≈ 2.7–2.8 %.** Note CV_G is almost exactly **2× CV_I** — the population
substitution would double the error here, and our placeholder does far worse than that.

Caveat to state in the paper: these are **healthy adults sampled weekly**. Our cohort is a CAD population, where
within-subject haematocrit variation may be larger (haemodilution, renal disease, bleeding, transfusion). The
figure should be described as a lower bound for a patient cohort.

---

## 6. RECOMMENDATIONS

### 6.0 First, what these three constants actually control — because it is not the residual

Before choosing values it is worth being precise about what they move, because the brief's concern ("a fabricated
SD here would silently set the detector's false-positive rate") is only **partly** right, and the part that is
wrong matters for how much effort each constant deserves.

Reading `perturbed_targets()` and `fit_global_scaling()` together: all three of `SD_CO`, `SD_MAP_MMHG` and `SD_MU`
enter as **globally acting** perturbations — they scale demand, driving pressure and bed resistance respectively,
and they act on *every* territory at once. Protocol C then fits **one global bed scaling** against the territory
targets. A perturbation that is uniform across territories is very largely **absorbed by that single fitted
parameter**, which is precisely what the module docstring already says of cardiac output ("absorbed by a global
scaling — on its own it is degenerate").

What actually survives into `resid` is the pair of terms the docstring identifies as non-absorbable:
`SD_TERRITORY_SHARE` (0.10, still flagged PROVISIONAL) and `WSCV_TARGET` (0.083, sourced). **So the residual-based
FPR is governed mainly by those two, not by the three physiological SDs.**

The three physiological SDs instead govern the **FFR displacement** of each draw — they move the fitted `C2`, and
because the stenosis pressure drop is nonlinear in flow (a viscous term plus a Bernoulli term), the absorption is
not exact and the FFR shifts. That is what feeds the **P(flip | band) noise floor** of §6, which is the number the
plan actually wants.

**Two consequences:**

1. `SD_TERRITORY_SHARE = 0.10` is, on this reading, a **more** load-bearing unsourced constant than any of the
   three under review here, and it is still marked PROVISIONAL. **It should be the subject of the next citation
   search.** Flagging it here because the present brief did not cover it.
2. None of the reasoning above should be taken on trust. **Measure it**: re-run `negatives.py` at the current and
   recommended constants and report the change in both AUC and the P(flip) floor. If the change is small, say so
   in the paper — "the floor is insensitive to the physiological SDs over the range the literature supports" is a
   much stronger claim than any single citation, and it is cheap to obtain.

**Direction of error, for honesty in the deviation log:** an SD that is too *large* inflates negative-class
dispersion, which *raises* the apparent FPR at a fixed threshold and *lowers* AUC. So the current placeholders are
conservative with respect to the detector's claimed performance — they make it look worse, not better. That is the
safe direction, but it is still wrong, and it distorts the calibrated operating point.

### 6.1 `SD_CO` — **(a) change to 0.05, with a declared sensitivity band** — and first settle a double-counting question

**Recommendation: `SD_CO = 0.05`**, citing **Täger 2015** (doi:10.1002/ehf2.12040, CV_I 5.44 % for cardiac index,
weekly, in patients) as primary and **Lassen 2023** (doi:10.1007/s12350-023-03308-1, hyperaemic CO wsSD ≈ 5.0 %
at rest / 3.1 % under adenosine) as hyperaemia-specific corroboration. Report a declared sensitivity band of
**0.03 / 0.05 / 0.10 / 0.153**.

**But this recommendation depends on a design question that only you can settle, and it is worth stating
explicitly because it moves the answer by a factor of two or three.**

Read literally, `perturbed_targets()` applies `SD_CO` to `t.demand("murray", co)` — the **true patient state** —
and *then* applies `SD_TERRITORY_SHARE` and `WSCV_TARGET` to represent the imperfect **measurement** of that
state. The docstring says exactly this: *"Step 1 perturbs the patient and re-solves, so the true territory flows
move together and physiologically. Steps 2–3 then break the Murray proportions and measure the result
imperfectly."*

If that is the intended semantics — and it is what the code does — then:

- `SD_CO` must carry the **biological** within-subject variation only: **≈ 0.05**.
- Using a measurement-inclusive figure (0.10–0.14) or, worse, an inter-method disagreement figure (Tanade's
  0.153) would **double-count measurement error**, which `WSCV_TARGET = 0.083` already carries.
- Using the *population* CV (0.31–0.33) would be wrong by roughly **6×** — see the Täger arithmetic in §5.1.

So the honest ordering of candidates, worst to best, for the code as written:

| Candidate | Value | What it actually is | Verdict |
|---|---|---|---|
| Population CV (Tanade Table 2; Täger Table 2) | 0.31–0.33 | between-patient | **wrong by ~6×** |
| Current placeholder | 0.20 | nothing — order-of-magnitude guess | unsupported |
| Tanade Table 1 | 0.153 | inter-method measurement disagreement, 1990, n = 18 | double-counts measurement |
| Day-to-day, measurement-inclusive | 0.09–0.14 | biological + measurement | double-counts, but defensibly |
| **Biological within-subject** | **0.05** | the patient's own state between occasions | **matches the code's semantics** |
| Hyperaemic biological | 0.031 | as above, under adenosine | arguably the most exact |

**If instead you intend `SD_CO` to absorb the whole "same patient, different occasion, as observed" budget** —
i.e. you do not regard `WSCV_TARGET` as covering the global component — then **0.10** is the right value
(Coats 9–14 %, Sundberg ≈ 12 %, McCarthy 11.6 %), and the documentation should say so.

**Either way, do not keep 0.20, and do not adopt 0.153 on Tanade's authority**, because §4 shows what that number
really is. Whichever is chosen, record the choice and its reasoning in the code comment, and report the sensitivity
band in the paper rather than a bare constant.

**A note in our favour:** because the model is **hyperaemic**, and Lassen 2023 shows cardiac output is *more*
reproducible under adenosine than at rest (RC 8.5 % vs 13.8 %), every figure above is conservative for our setting.

### 6.2 `SD_MAP_MMHG` — **(a) change to a relative SD of 0.056, i.e. ≈ 5.0 mmHg at P_AORTA = 90**

**Recommendation: replace `SD_MAP_MMHG = 10.0` with a relative SD of 0.056**, applied multiplicatively to the
patient's own MAP, matching Tanade's parameterisation. At our `P_AORTA = 90 mmHg` this is **5.04 mmHg**.

Cite, in this order:
- **Tanade 2022 Table 1**, for the 0.056 itself (declaring it as literature-derived and not independently traced —
  see §7);
- **Stergiou 2002** (PMID 11863243) and **Muntner 2011** (PMID 21200000) as the within-subject anchors, with the
  SDD → wsSD conversion stated explicitly;
- and state that the propagation from SBP/DBP to MAP is **our arithmetic under an unknown within-subject
  SBP–DBP correlation**, with the 4.1–5.7 mmHg range quoted rather than a point value.

Why not keep 10.0: it is roughly double every within-subject estimate and close to the *population* SD. Keeping it
would be exactly the population-for-within-subject error the brief set out to avoid.

**Also fix the parameterisation, not just the number.** The current code draws
`rng.normal(P_AORTA/133.322, SD_MAP_MMHG)` — an absolute mmHg spread around a fixed 90 mmHg. A relative draw is
both closer to the source and better behaved if `P_AORTA` is ever made patient-specific.

Declared sensitivity band to report alongside: **0.056 (Tanade) / 0.09 (Dalmaso 2025) / 0.11 (≈10 mmHg, the
current placeholder)**.

### 6.3 `SD_MU` — **(a) change to ≈ 0.02. The current 0.15 is ~7–8× too large.**

This is the clearest and largest correction in the block, and unlike the others it rests on a **verified primary
source measured in exactly the right design**.

**Derivation, stated in full so it can be checked:**

Haematocrit within-subject CV_I = **2.82 %** (Coşkun 2018, EuBIVAS, n = 30, weekly × 10 weeks; corroborated at
2.71 % and 2.81 % by two independent routes — §5.3). At φ ≈ 0.392 (Tanade's cohort mean) this is an absolute
within-subject SD of **Δφ = 0.0282 × 0.392 = 0.0111** (1.1 haematocrit percentage points).

Propagating through the viscosity–haematocrit law Tanade uses (Pirofsky 1953), μ = μ₀/(1 − φ):

```
d(ln μ)/dφ = 1/(1 − φ)             →  Δμ/μ = 0.0111 / 0.608 = 0.0182
```

So **SD_MU ≈ 0.018** under Tanade's own viscosity law.

Steeper empirical laws (whole-blood viscosity is more strongly nonlinear in haematocrit than Pirofsky's form at
physiological levels; an exponential form μ ∝ exp(kφ) with k ≈ 2.5–3.5 is a common approximation) give
**Δμ/μ = 0.028 to 0.039**.

**Recommend `SD_MU = 0.02`**, with a declared sensitivity band of **0.02–0.04** covering the choice of viscosity
law. Cite Coşkun 2018 (doi:10.1515/cclm-2017-1155) for the haematocrit CV_I and Pirofsky 1953
(doi:10.1172/JCI102738) for the propagation, and **state the sensitivity coefficient explicitly** in the code
comment so the assumption is visible:

> haematocrit within-subject CV_I = 2.82 % (Coşkun 2018, EuBIVAS) propagated through μ = μ₀/(1−φ) at φ = 0.4
> gives a relative viscosity SD of ≈ 0.018; steeper viscosity–haematocrit laws give up to ≈ 0.04. Value chosen:
> 0.02. Sensitivity 0.02–0.04 reported.

**Do not simply carry 0.15 forward.** There is no source for it, and the true figure is not close.

Two honest caveats to record with it:
- the CV_I is from **healthy adults**; a CAD cohort will vary more, so 0.02 is a lower bound for our population;
- our solver uses `MU = 0.004 Pa·s (4 cP)` whereas Tanade's law yields ~1.97 cP. The *relative* SD transfers
  between them; the absolute viscosity does not, and the two papers' viscosities should never be compared directly.

### 6.4 Heart rate — **(b) the literature does not support a value, and none is needed**

Tanade publishes no heart-rate SD (§2.3), and the only heart-rate dispersion in the paper is a **population** SD
(70.8 ± 13.7 bpm) that must not be repurposed. Our model is steady, so heart rate has no port of entry.

**Recommendation: change STATISTICS-PLAN §6, not the code.** `negatives.py` already handles this correctly and
transparently ("NOT REPRESENTED: this is a steady model. Stated, not silently omitted."). §6 currently claims to
vary heart rate; it does not and cannot. Drop it from §6's list and keep the code's explicit statement.

### 6.5 STATISTICS-PLAN §6 — suggested replacement text

The present wording cannot survive review as written. A replacement that is defensible:

> **§6. The physiological-noise floor (pre-specified control).** A no-injection Monte Carlo over cardiac output,
> mean arterial pressure and haematocrit-driven viscosity, at short-term **within-subject** dispersions
> (`SD_CO`, `SD_MAP`, `SD_MU`; sources and sensitivity bands in
> `references/CITATION-PHYSIOLOGICAL-SDS-2026-09-19.md`), 1,000 draws per instance, plotted on the same
> P(flip | band) axes as every result. Heart rate is not represented: the model is steady. **No injected-error
> flip rate is reported without this floor.** The floor is additionally anchored to measured repeat-FFR
> variability in patients — SD of paired repeat FFR = 0.018 (Johnson 2015, n = 190 pairs), and a
> band-conditional probability of changing the revascularisation decision that exceeds 20 % only within
> FFR 0.77–0.83 and reaches 50 % at FFR ≈ 0.80 (Petraco 2013, DEFER repeat measurements 10 min apart). An
> injected-error effect that does not exceed this floor is reported as **not distinguishable from physiological
> noise**, in those words.

and delete the Tanade 50 %/25 % sentence entirely, replacing it in the deviation log with the correction in §3.

### 6.6 The empirical floor — strongly recommended as the primary anchor

Two sources measure the thing §6 wants, directly, in patients, without a simulation in between. **They are better
evidence than any Monte Carlo we can run**, and one of them is already on our own outcome axes.

- **Johnson NP, Johnson DT, Kirkeeide RL, Berry C, De Bruyne B, Fearon WF, Oldroyd KG, Pijls NHJ, Gould KL.**
  Repeatability of Fractional Flow Reserve Despite Variations in Systemic and Coronary Hemodynamics.
  *JACC Cardiovasc Interv.* 2015;8(8):1018–27. doi:10.1016/j.jcin.2015.01.039. PMID 26205441.
  **Abstract read in full**; full text not retrieved.
  Re-analysis of the VERIFY study; **190 complete pairs from 206 patients**, FFR measured **twice** under IV
  adenosine 140 µg/kg/min. Verbatim: *"Despite variability of Pd/Pa during the hyperemic period, the 'smart
  minimum' FFR demonstrated excellent repeatability (bias −0.001, SD 0.018, paired p = 0.93, r² = 98.2 %,
  coefficient of variation = 2.5 %)."*
  ⚠️ **Our reading, flagged as an interpretation:** the bias-and-SD pairing is a Bland–Altman statistic, so
  0.018 is most likely the **SD of the difference** between the two repeats, implying a single-measurement
  wsSD ≈ 0.018/√2 = **0.013**. The abstract does not state which, and the full text was not reached. **Do not
  quote 0.018 as a single-measurement SD without checking the full text.**
  Why it matters here: this is the *whole* physiological noise budget — the paper explicitly notes "associated
  variability in aortic and coronary pressure and heart rate during the hyperemic period" — collapsed into one
  measured number on the FFR scale. It bounds everything our Monte Carlo is trying to reconstruct from parts.

- **Petraco R, Sen S, Nijjer S, Echavarria-Pinto M, Escaned J, Francis DP, Davies JE.** Fractional flow
  reserve-guided revascularization: practical implications of a diagnostic gray zone and measurement variability
  on clinical decisions. *JACC Cardiovasc Interv.* 2013;6(3):222–5. doi:10.1016/j.jcin.2012.10.014. PMID 23517831.
  **Abstract read in full**; full text not retrieved (ScienceDirect and onlinejacc both returned HTTP 403).
  Method: repeat FFR in the **same lesion 10 min apart** from the DEFER trial; the SD of the difference was
  computed and converted to a *measurement certainty* across the FFR range. Verbatim:
  *"Outside the [0.75 to 0.85] FFR range, measurement certainty of a single FFR result is >95%. However, closer to
  its cut-off, certainty falls to less than 80% within 0.77 to 0.83, reaching a nadir of 50% around 0.8."*
  **This is a band-conditional reclassification probability — the same object as our P(flip | band).** It is the
  single most directly comparable published quantity to our primary outcome that this search found.

**Note the contrast with Tanade's 50 %/25 %.** Petraco's reclassification probability reaches 50 % only for
lesions sitting *exactly on* the 0.80 cut-off, and is **below 5 % outside 0.75–0.85**. Tanade's 50 % is a
*cohort-wide* proportion driven substantially by a ±16.9-point stenosis-degree perturbation. Quoting the latter as
a physiological floor would overstate the floor by a large and unquantified factor. **This is the practical harm
the erroneous §6 attribution would have caused**, and it is the reason the correction is worth making before
registration rather than after.

⚠️ **Not verified:** a secondary search result stated Petraco's DEFER-derived SDD as 0.032. **We could not reach
the full text to confirm this and it should not be quoted.** Only the certainty percentages above, which come from
the abstract, are safe to cite.

---

## 7. What I could not establish

Listed plainly, because each is a place where a number could be invented and should not be.

1. **Fossan et al. 2018 full text was never reached.** Paywalled at Springer; the NTNU Open green-OA copy is
   stranded behind a platform migration (`hdl.handle.net/11250/2622598` → NVA/Sikt, whose file endpoint returns
   `Forbidden` / `Missing Authentication Token`); Europe PMC has no PMCID; Semantic Scholar's open-access link
   resolves back to the same dead handle. **Consequence: I cannot say whether Tanade's MAP CoV of 0.056 comes
   from Fossan, nor what Fossan calls it** (measurement uncertainty? population? within-subject?). This is the
   single biggest gap in the provenance chain. **Institutional access would close it in minutes** and is worth
   the five minutes before registration.

2. **Dubin 1990 full text was never reached** (1990, paywalled). The ±0.69 L/min figure is from the abstract,
   which is unambiguous, but I could not confirm Dubin's own cohort mean cardiac output — so the reconstruction
   `0.69 / 4.5 = 0.153` uses **Tanade's** cohort mean, not Dubin's. The match is exact to three significant
   figures and the reference is cited in the right sentence, so confidence is high, **but Tanade never states
   this arithmetic and it must be reported as a reconstruction, not as Tanade's claim.**

3. **No published within-subject SD for resting MAP exists that I could find.** SBP and DBP are well covered;
   MAP is not. Our 4.1–5.7 mmHg range is **our own propagation** from Stergiou's clinic wsSDs under an assumed
   SBP–DBP within-subject correlation that **no source reports**. It should be presented as such.

4. **Petraco 2013's SD of differences was not verified.** A secondary search result gave it as 0.032; both the
   ScienceDirect and onlinejacc full texts returned HTTP 403. **Do not quote 0.032.** Only the measurement-certainty
   percentages, which are in the abstract, are safe.

5. **Johnson 2015's "SD 0.018" — which statistic it is was not verified.** Bias-plus-SD reads as Bland–Altman,
   implying the SD of the *difference* and a single-measurement wsSD of ≈ 0.013, but the abstract does not say and
   the full text was not reached. **Check before quoting it as a single-measurement SD.**

6. **No EFLM Biological Variation Database entry for cardiac output or stroke volume was found.** The database is
   organised by laboratory measurand, and every entry surfaced was a lab analyte. The site is a JavaScript app
   whose search pages returned only headers to our fetcher, so **we could not enumerate the measurand list to
   prove a negative.** Report as "no entry found; scope appears to be laboratory measurands" — not as
   "confirmed absent". (The haematocrit entry *was* retrieved, via the database's own JSON API, and agrees with
   the published meta-analysis.)

7. **No conventional breath-hold cine-CMR scan–rescan study reporting a cardiac-output CoV in healthy adults was
   located.** Grothues 2002 (the standard interstudy-reproducibility reference) reports EDV/ESV/EF/mass but
   **not** stroke volume or cardiac output. Treat as a genuine gap; do not interpolate one from the volume CoVs.

8. **The two cardiac-output literatures were never reconciled by any source.** No paper found states both the
   biological CV_I and the measurement-inclusive day-to-day CV for cardiac output in the same subjects, which is
   why §6.1 has to present the double-counting question as a decision rather than resolve it by citation.

9. **Whether `SD_CO`/`SD_MAP`/`SD_MU` materially move the detector's operating point was NOT measured** — §6.0
   argues from reading the code that they are largely absorbed by Protocol C's single global scaling and that
   `SD_TERRITORY_SHARE` and `WSCV_TARGET` dominate the residual. **That is an inference from code, not a result.**
   Run it.

10. **`SD_TERRITORY_SHARE = 0.10` remains uncited** and, if §6.0 is right, is more load-bearing for the detector's
    false-positive rate than any of the three constants this brief covered. **It should be the next citation
    search.** Nothing in this document supports or refutes it.

11. **Cohort transfer is unquantified for every figure here.** Täger's patients were rigidly stable CHF; Coşkun's
    subjects were young and healthy; Lassen's were healthy volunteers aged ~23. Our cohort is CAD patients
    undergoing invasive FFR. Within-subject variation is plausibly *larger* in our population for all three
    quantities, and **no source was found that measures any of them in a stable-CAD cohort**. Every recommended
    value should be described as a **lower bound** for our population.

---

## 8. Sources, with what was actually read

| Source | Reached | Used for |
|---|---|---|
| Tanade 2022, Front Med Technol, doi:10.3389/fmedt.2022.1034801 | **full text (PDF)** | §1–§3; Tables 1, 2, 4; refs 27/34/54 |
| Dubin 1990, Am Heart J 120:116–23, PMID 2360495 | abstract | §4.1, CoV 0.153 reconstruction |
| Fossan 2018, Cardiovasc Eng Technol 9:597–622, doi:10.1007/s13239-018-00388-w | **metadata only** | §4.2 — unresolved |
| Pirofsky 1953, J Clin Invest 32:292–8, doi:10.1172/JCI102738 | cited via Tanade | §6.3 viscosity law |
| Dalmaso 2025, doi:10.1002/cnm.3898, PMC11706247 | **full text** | §4.3 comparator |
| Täger 2015, ESC Heart Fail 2:112–20, doi:10.1002/ehf2.12040, PMC5032993 | **full text** | §5.1 CO biological CV_I |
| Lassen 2023, J Nucl Cardiol 30:2504–13, doi:10.1007/s12350-023-03308-1, PMC10682170 | **full text/tables** | §5.1 hyperaemic CO |
| Coats 1990, Eur Heart J 11(Suppl I):49–61, PMID 2092990 | abstract | §5.1 day-to-day CO |
| McCarthy 2025, doi:10.1139/apnm-2025-0234, PMID 41172356 | abstract | §5.1 |
| Sundberg 1996, PMID 8705093 | abstract | §5.1 |
| Giraud 2017, doi:10.1007/s10877-016-9823-y, PMID 26753534 | abstract | §5.1 |
| Critchley & Critchley 1999, doi:10.1023/A:1009982611386 | **secondary only** | §5.1 sanity check |
| Muntner 2011, doi:10.1161/HYPERTENSIONAHA.110.162255, PMID 21200000 | abstract | §5.2 SBP wsSD |
| Stergiou 2002, doi:10.1016/S0895-7061(01)02324-X, PMID 11863243 | abstract | §5.2 SDD → wsSD |
| Warren 2010, doi:10.3399/bjgp10X515403, PMC2930221 | **full text** | §5.2 BP within-individual CV |
| Coşkun 2018, Clin Chem Lab Med 56(8), doi:10.1515/cclm-2017-1155, PMID 29605821 | **full text (PDF, Table 1)** | §5.3, §6.3 haematocrit CV_I |
| Coskun 2019, doi:10.1515/cclm-2019-0658 | **full text (Table 2)** | §5.3 corroboration |
| EFLM Biological Variation Database (biologicalvariation.eu) | **JSON API** | §5.3 corroboration |
| Johnson 2015, JACC Cardiovasc Interv 8:1018–27, doi:10.1016/j.jcin.2015.01.039, PMID 26205441 | abstract | §6.6 empirical FFR floor |
| Petraco 2013, JACC Cardiovasc Interv 6:222–5, doi:10.1016/j.jcin.2012.10.014, PMID 23517831 | abstract | §6.6 band-conditional floor |

**Nothing in this document is cited that was not retrieved.** Where only an abstract was reached it is said so;
where a number is our arithmetic rather than a published figure it is labelled; where a claim could not be checked
it is in §7 rather than in the recommendations.
