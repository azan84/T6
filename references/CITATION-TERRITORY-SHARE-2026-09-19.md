> ## ⚠ OUTCOME NOTE added 2026-09-19 by the operator side — read before acting on §8.
>
> **The main finding of this document stands** and has been applied: `SD_TERRITORY_SHARE` has no supportable single
> value, 0.10 is retained as a declared choice, and specificity is reported across a 0.05/0.10/0.15/0.20 band.
> The `WSCV_TARGET` spillover (§8) also stands — Kaufmann 1999's regional figure is roughly double ours, and both
> noise terms are now declared to err toward an easy negative class.
>
> **The `MURRAY_EXP = 2.66` spillover finding is WITHDRAWN.** It is not uncited and it is not outside an empirical
> CI, because the comparison is category-mismatched:
> - **2.66 = 8/3 is a MASS–diameter exponent** — Choy & Kassab 2008, M ∝ A^(4/3) and A ∝ D², giving M ∝ D^(8/3).
>   In this model it allocates *myocardial bed* to a truncated outlet.
> - **Taylor 2024's 2.39 pools the FLOW–diameter exponent** (Q ∝ D^n, near Kassab's theoretical 7/3), which predicts
>   flow *through* a vessel. A pooled estimate of a different exponent is not evidence against this one.
>
> Measured on the 30 frozen 3D-subset trees: substituting 2.39 moves any outlet's share of its tree's flow by a
> median **0.33 pp** (p90 0.94, max 1.95) against a validation check that passes at 10 pp — because truncation
> leaves every outlet within ~0.06 mm of the cut. Retained as a sensitivity (allocate the bed by mass or by flow),
> not as a correction. *(Choy & Kassab still to be verified against the paper before the manuscript quotes it.)*
>
> This note is appended rather than edited into the text: the review is a record of what was found at the time, and
> it found a real thing worth checking.

# Citation search: `SD_TERRITORY_SHARE` — the scatter of territory perfusion about an anatomical calibre rule

Date: 2026-09-19. Searcher: literature agent. Status of this document: **evidence gathered and verified**;
it proposes a decision, it does not enact one. Nothing in `code/`, `protocol/` or `results/` was modified.
The only files written are this document and the probe in
`references/CITATION-TERRITORY-SHARE-2026-09-19-probe/`.

Constant under review (`code/negatives.py` L76):

```python
SD_TERRITORY_SHARE = 0.10   # per-territory departure from the Murray demand split. STILL PROVISIONAL, AND NOW
                            # THE MOST LOAD-BEARING CONSTANT HERE.
```

Flagged as the next citation search by `CITATION-PHYSIOLOGICAL-SDS-2026-09-19.md` §6.0 and §7 item 10.

---

## TL;DR

1. **The literature does not support a single value.** Recommendation is **(b)**: keep `0.10` as the
   **pre-registered primary**, declare it as a *chosen* value rather than a cited one, and report the
   detector's specificity across a **pre-specified sensitivity band of 0.05 / 0.10 / 0.15 / 0.20**.
   The band is measured, not asserted — §7 gives the numbers from a probe run on 50 cohort instances.

2. **There is one nearly ideal primary source, and it was found.**
   **Keulards DCJ, Fournier S, van 't Veer M, Colaiori I, Zelis JM, El Farissi M, Zimmermann FM, Collet C,
   De Bruyne B, Pijls NHJ. Computed tomographic myocardial mass compared with invasive myocardial perfusion
   measurement. *Heart.* 2020;106(19):1489–1494. doi:[10.1136/heartjnl-2020-316689](https://doi.org/10.1136/heartjnl-2020-316689).
   PMID 32471907; PMC7509389. Open access; full text read.**
   It compares, per territory and as a **percentage of the total**, an **anatomical calibre-based prediction of
   flow share** against **invasively measured hyperaemic flow share**, in 35 patients with normal or near-normal
   coronaries, in all three major arteries. That is `SD_TERRITORY_SHARE` measured in humans, almost exactly as
   the model defines it. The paper is not framed that way — it is framed as a validation of CT myocardial mass —
   which is presumably why it has not surfaced before.

3. **The headline numbers.** Verbatim (Results): *"The mean difference was 5.3%±6.2% for the LAD territory,
   −2.0±7.4% for the LCX territory and −3.1±3.4% for the RCA territory."* (The Abstract gives −3.2±3.4 for the
   RCA; the paper is internally inconsistent by 0.1 pp. Both are quoted below where used.) These are
   **percentage points of total heart flow**, and both a **bias** (the means) and a **scatter** (the SDs).

4. **On the code's scale, the observed relative scatter is 0.147 / 0.273 / 0.111 for LAD / LCx / RCA — larger
   than 0.10** — but it is a measurement-inclusive **upper bound**. After removing the invasive flow
   measurement's own repeatability and undoing the model's renormalisation, the implied
   `SD_TERRITORY_SHARE` is **0.170 / 0.281 / 0.051**, RMS **0.192** (from 0.226 before the subtraction).
   Full arithmetic, labelled as ours, in §3.3. **Every step of that reduction is a reconstruction, not a
   published figure**, and the vessel-to-vessel spread (a factor of 5.5) is larger than any precision one could
   claim for a single recommended value — which is the core reason the answer is a band.

5. **Answer to the double-counting question (brief item 3): YES, every published figure here contains
   measurement error, and it must be removed.** The invasive flow in Keulards is continuous thermodilution.
   Its same-sitting duplicate **Bland-Altman SD of differences is 35.48 mL/min on a mean of 211 mL/min = 16.8 %**,
   giving a one-measurement **within-subject CV of 16.8/√2 = 11.9 %** (Gallinoro 2023, n = 102 — §4).
   ⚠️ **That paper's own "Variability (%) 11.89" column is a *difference* statistic, not a CV** — taking it at
   face value would repeat the RC-vs-wsSD error DETECTOR-SPEC §5 warns about. The two routes happen to agree;
   §4 uses the Bland-Altman one because it is unambiguous. The correction is of the same order as the whole
   signal, so it is not a refinement — it is the dominant step. `WSCV_TARGET = 0.083` already carries
   per-territory measurement noise, so keeping Keulards' raw 6.2/7.4/3.4 pp would double-count.

6. **Answer to brief item 4: YES, a systematic component exists, it replicates across modalities, and it is a
   bias rather than an SD.** The LAD territory receives **≈ 5 percentage points more** of total hyperaemic flow
   than the anatomical rule predicts, the LCx **≈ 2 points less** (Keulards, paired, n = 35). Independently:
   minimal microvascular resistance is **significantly lower in the anterior wall** (Fournier 2021, p < 0.05);
   and in two CMR normal cohorts with within-subject tests and no shared method, **stress MBF is highest in the
   LAD and lowest in the RCA** (Brown 2023, n = 150, p < 0.001; Kamani 2025, n = 138). **The model has no term
   for this.**
   ⚠️ **Three things weaken it**, all in §6.2–6.3: (a) at **hyperaemia** — our state — the effect is weaker or
   absent (Brown 2018, n = 42: significant at rest, *"No significant difference … in stress MBF"*;
   Chareonthaitawee's cohort ANOVA at hyperaemia is null; Lyu 2022 CT-MPI, P = 0.399); (b) three different
   modalities each have a **septum-specific artefact** pointing the same way — uncorrected CMR coil shading
   manufactures a **60 % septal-vs-lateral** difference in normals (Miller 2015), and ¹³N-ammonia underestimates
   septal flow by **0–30 %** (Hove 1998); (c) our territories are not vessel-identified, so the bias could not
   be applied even if wanted. **Recommendation: declare it, do not model it.**

7. **A second, independent method family agrees — and it splits the constant into two legs.** The PET/CMR
   perfusion literature measures the **mass→flow leg** (does each gram of a territory get the same flow?) and
   puts it at **≈ 7–15 %**: Chareonthaitawee 2001 (n = 169, ¹⁵O-water) gives a **within-subject,
   between-region CV of 17 ± 10 % at hyperaemia** at quarter-LV scale, of which most is measurement
   (Kaufmann 1999, same lab, regional hyperaemic RC 41–59 %); Bassingthwaighte 1989 — the only paper anywhere
   that subtracts methodological from spatial dispersion — extrapolates to **≈ 6–13 % at territory scale**;
   and Choy & Kassab 2008 measured it directly in eight porcine hearts: *"The mean flow per mass (perfusion)
   for all the territories was 1.05±0.16 ml/min/g"*, a **CV of 15.2 %** with near-zero measurement error.
   **§5.7 puts the two legs together: if the model needed only perfusion-per-gram, 0.10 would be an excellent
   central value. It needs the calibre→mass leg too, so 0.10 sits at the low end.**

8. **⚠️ The most tempting wrong citation in this field, flagged before anyone reaches for it.** The famous
   microsphere heterogeneity figure of **35 %** is measured *"when observations were made by dividing the
   hearts into 100–250 pieces"* — sub-gram samples, two to three orders of magnitude finer than a coronary
   territory. Bassingthwaighte's own scaling law shows dispersion falls as pieces are aggregated. **Quoting
   35 % at territory scale would overstate this constant roughly five-fold**, and Gould says so in print
   (§5.6).

9. **⚠️ A spillover finding for a different constant.** Kaufmann 1999 (full text) gives a regional hyperaemic
   repeatability coefficient of **41–59 %**, i.e. a within-subject CV of **15–21 %** — roughly **double** the
   `WSCV_TARGET = 0.083` taken from Lubberink 2024. Modern PET is better than 1999 PET, so 8.3 % may well
   stand, but the disagreement deserves a sentence in
   `references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md` rather than silence. §5.5.

10. **A separate finding the search turned up that is not about the SD at all, and should be logged:** the code's
   `MURRAY_EXP = 2.66` is uncited and **sits outside the pooled human/animal flow–diameter exponent of 2.39
   (95 % CI 2.24–2.54)** from a 1,070-tree meta-analysis (Taylor 2024, §8). 2.66 is defensible as Kassab's
   *volume*–diameter 8/3 law, but it is not the *flow*–diameter law, and the difference acts as a **systematic
   redistribution between territories of roughly the same size as `SD_TERRITORY_SHARE` itself**. §8.

11. **Direction of error matters here and it is the unsafe one.** A too-*small* `SD_TERRITORY_SHARE` makes the
   negatives tighter, lowers their residuals, and **raises the fraction of correct-but-noisy models that pass
   the 10 % validation check** — i.e. it inflates the specificity that DETECTOR-SPEC §5 reports as "~77 %".
   Unlike the three physiological SDs, where the placeholders erred large and therefore conservatively, an
   under-set share SD flatters the result. **Measured in §7: the pass rate runs 85 % → 43 % across
   0.05 → 0.20, and is 92 % with the share noise switched off entirely.** (§7 deliberately stops short of
   claiming a direction for AUC; that needs the positives, and §7.2 explains why the sign is not obvious.)

12. **The result that limits the damage.** Over that same band the **|dFFR| noise floor barely moves**
    (median 0.0190 → 0.0225, against `MATERIAL_DFFR = 0.05`). So the *physiological* claim the negatives exist
    to support is robust to this constant; only the *validation-gate specificity* is fragile. That distinction
    should be made explicitly in the paper.

---

## 1. What the constant has to be, stated precisely

From `perturbed_targets()`:

```python
share = rng.normal(1.0, SD_TERRITORY_SHARE, size=len(tgt))
tgt_shared = tgt * share
if tgt_shared.sum() > 0:                      # renormalise: REDISTRIBUTES, does not create flow
    tgt_shared *= tgt.sum() / tgt_shared.sum()
```

So `SD_TERRITORY_SHARE` is the relative SD of an **independent multiplier applied to each territory's
model-predicted flow, before renormalisation**. The target quantity in the literature is the relative SD of

&nbsp;&nbsp;&nbsp;&nbsp;(a real patient's territory flow share) ÷ (the share an anatomical calibre rule predicts)

and the two are not the same number, because renormalisation shrinks the injected σ. For territories with
predicted shares *wᵢ*, a first-order expansion gives the **realised** relative share deviation

&nbsp;&nbsp;&nbsp;&nbsp;δᵢ ≈ εᵢ − Σⱼ *wⱼ* εⱼ, &nbsp; SD(δᵢ) = σ · √[(1 − *wᵢ*)² + Σ_{j≠i} *wⱼ*²]

**(our arithmetic, not from any paper).** For two equal territories the factor is **0.707**; for the three-vessel
weights in Keulards it is **0.71 / 0.90 / 0.86**. So a literature figure expressed as share scatter must be
**divided by ≈ 0.7–0.9 before it is set as `SD_TERRITORY_SHARE`**, or the injected noise will be ~20–30 % too
small. This is a real factor and it is currently unaccounted for in the code comment.

**Scale note, and it bounds how far the literature transfers.** `ablation.territories()` defines a territory as
*"the subtrees rooted at each child of the FIRST branching node"* of a **single-side** tree. For a left tree
that is LAD vs LCx — precisely the scale of every source below. For a **right** tree it is two sub-branches of
the RCA, a **finer** spatial scale, over which perfusion heterogeneity is necessarily **larger** (averaging over
less myocardium cancels less). The frozen cohort is 100 left / 50 right. **Every figure in this document is
therefore a lower bound for the right-side third of the cohort**, and that should be stated in the paper rather
than glossed.

---

## 2. Choy & Kassab 2008 — the controlled anchor, and the source of `MURRAY_EXP`

> **Choy JS, Kassab GS.** Scaling of myocardial mass to flow and morphometry of coronary arteries.
> *J Appl Physiol (1985).* 2008;104(5):1281–1286. doi:[10.1152/japplphysiol.01261.2007](https://doi.org/10.1152/japplphysiol.01261.2007).
> PMID 18323461; PMC2629558. **Full text read.**

Design, verbatim from Methods: eight normal Yorkshire swine hearts; *"Two cannulations were made at different
points (proximal and distal) along the main trunk of the LAD, three in the RCA, and two in the LCX artery … The
seven vessel segments were individually perfused at pressure of 100 mmHg with cardioplegic solution and the
corresponding flows measured by a flowmeter (Transonic Systems, Inc.)."* Each region was then **weighed**.

**The number that matters**, verbatim:

> "The mean flow per mass (perfusion) for all the territories was 1.05±0.16 ml/min/g."

**CV = 0.16 / 1.05 = 15.2 %.**

| property | assessment |
|---|---|
| Includes measurement error? | **Yes, but very little.** Transonic flowmeter + direct gravimetric mass. This is the cleanest measurement-error profile of any source here. |
| Between-subject or within-subject? | **Pooled, and this is its main weakness.** The ± spans seven territories across eight hearts; the paper does not decompose. Some of the 15.2 % is heart-to-heart, which our renormalised share model does not need. So **15.2 % is an upper bound on the within-heart between-territory figure.** |
| What leg of the prediction? | **mass → flow only.** It says nothing about how well *calibre* predicts *mass*. Our rule is calibre-based, so the full share scatter is this ⊕ the calibre→mass scatter. |
| Physiological state | **Excised, KCl-arrested, cardioplegia-perfused at 100 mmHg.** This is passive conductance per gram with no metabolic autoregulation. Cuts both ways: it is *not* hyperaemic blood flow in a beating heart, but our 0D model is *also* a passive conductance network at fixed perfusion pressure, so the analogy is closer than it first looks. |

Other figures from the same paper (all n = 8 subtrees, least-squares fit, full extrapolated model):

| relation | exponent ± SD | R² |
|---|---|---|
| V – m | 1.05 ± 0.06 | 0.99 |
| L – m | 0.81 ± 0.12 | 0.93 |
| **D – m** | **0.41 ± 0.05** | **0.87** |
| Q – m | 0.74 ± 0.04 | 0.97 |
| **V – D** | **2.51 ± 0.19** (vs the 8/3 = 2.66 law) | 0.97 |

**This is where `MURRAY_EXP = 2.66` comes from**, whether or not it was taken from here: 8/3 is Kassab's
volume–diameter law, and with V ∝ m¹ it gives m ∝ D^(8/3). The code comment calls it an *"empirical coronary
exponent"* with no citation; **Choy & Kassab 2008 is a defensible citation for it, and it should be added.**
But see §8 — the *flow*–diameter exponent is a different and smaller number.

**What could not be recovered from this paper:** a residual SD about the D–m regression. R² = 0.87 alone cannot
be converted to a residual scatter without the spread of the data, and the paper does not report it. Attempting
to reconstruct one from a guessed mass range would be invention; it is not done here.

---

## 3. Keulards 2020 — the primary human source

### 3.1 Why it is the right paper, which is not obvious from its title

The paper validates HeartFlow's CT myocardial-mass computation against invasive flow. The **method by which
that CT mass is computed** is what makes it the right paper. Verbatim from Methods:

> "Next, total flow to the LCA and RCA was distributed to the individual vessels within these territories
> **based on downstream vascular volume**. Finally, the myocardial mass subtended by each coronary vessel
> territory (left anterior descending (LAD), left circumflex (LCX) and right coronary artery (RCA)) was computed
> by dividing the territory flow … by a constant baseline flow per unit tissue and the fraction of total
> myocardial mass was reported."

So the "CT mass share" **is** an anatomical calibre/volume-based prediction of flow share, rescaled by a
constant. Comparing it against measured flow share is comparing an anatomical rule's prediction against reality
— the same object as `SD_TERRITORY_SHARE`, differing only in which anatomical rule (downstream vascular volume,
rather than our r^2.66 leaf weighting). Both are Murray-family rules; Choy & Kassab's V ∝ m¹ makes them close
relatives.

The paper's own framing states the assumption plainly:

> "Assuming homogeneous myocardial perfusion and assuming a direct relation between blood flow and mass of the
> perfused territory, the relative distributions of both the mass and flow should be equal."

The departure from that equality is exactly our constant.

### 3.2 Design and the numbers as published

- n = 35 patients (33 CT-analysable; 2 excluded for motion artefact); **105 arteries, all three majors in every
  patient**. Angiographically normal or ≤ 30 % in one segment only, FFR > 0.80 in all three, Agatston < 400.
- Invasive flow: continuous intracoronary thermodilution, Rayflow catheter, CoroFlow; **hyperaemic** (total
  hyperaemic flow 738.9 ± 201.9 mL/min). Reported as **Qnorm** — *"the flow in the absence of a stenosis is
  determined by the Coroventis software (Qnorm) by dividing the actually measured flow by FFR."*
- CT and invasive angiography **< 3 months apart**.

Table 2, verbatim (mean ± SD):

| | LAD | LCx | RCA | total |
|---|---|---|---|---|
| Myocardial mass on CCTA (g) | 49.2 ± 12.2 | 39 ± 13.2 | 46.5 ± 15.9 | LV 153.3 ± 33.5 |
| Qnorm (mL/min) | 312.1 ± 108.8 | 200 ± 77.5 | 226.8 ± 79.4 | 738.9 ± 201.9 |
| FFR (adenosine, no Rayflow) | 0.86 ± 0.06 | 0.95 ± 0.03 | 0.94 ± 0.05 | |
| FFR with Rayflow in situ | 0.81 ± 0.06 | 0.92 ± 0.06 | 0.91 ± 0.11 | |

⚠️ **The ± in that table are BETWEEN-PATIENT SDs and must not be used.** CV of LAD flow across patients is
108.8/312.1 = 35 %; that is the population spread of a patient's cardiac output and heart size, which our
renormalised share model removes by construction. **This is the same trap that `SD_MAP_MMHG = 10.0` fell into.**
The usable statistic is the *paired within-patient difference*, which the paper reports separately:

> "The mean difference was 5.3%±6.2% for the LAD territory, −2.0±7.4% for the LCX territory and −3.1±3.4% for
> the RCA territory."

(Abstract: "−3.2±3.4% for the right coronary artery territory". Same SD, 0.1 pp discrepancy in the mean.)

> "The intraclass correlation between mass and flow is 0.90 in these normal or near-normal patients."

**Sign convention — resolved, because it matters for §6 and the paper states it ambiguously.** The Methods say
the difference is *"between relative CTmass per territory and relative flow"*, which reads as mass% − flow%. But
from Table 2, mass shares over the three territories are 36.5 / 29.0 / 34.5 % and flow shares are
42.2 / 27.1 / 30.7 %, giving mass% − flow% = **−5.7 / +1.9 / +3.8** — the *opposite sign* to the reported
+5.3 / −2.0 / −3.1 and the same magnitudes to within 0.7 pp. **The reported quantity is therefore flow% − mass%**,
i.e. **the LAD receives more of the total than the anatomical rule allots it.** This is our inference from the
paper's own table, not a statement the paper makes; it is flagged as such in §9.

### 3.3 Converting to the code's scale — every line of this is our arithmetic

Flow shares from Table 2: *w* = (0.4224, 0.2707, 0.3069) for LAD / LCx / RCA.

**Step 1 — relative SD of the share departure** (SD in pp ÷ mean flow share):

| | LAD | LCx | RCA |
|---|---|---|---|
| SD of difference (pp) | 6.2 | 7.4 | 3.4 |
| ÷ mean flow share | **0.147** | **0.273** | **0.111** |

**Step 2 — remove the flow measurement's repeatability.** §4: continuous-thermodilution Qhyp CoV = 0.1189.
Propagated to a renormalised share with the factor from §1 (0.708 / 0.897 / 0.856) the measurement contribution
to each share is 0.084 / 0.107 / 0.102. Subtracting in quadrature:

| | LAD | LCx | RCA |
|---|---|---|---|
| share scatter net of flow measurement | **0.120** | **0.252** | **0.044** |

**Step 3 — undo the renormalisation** to recover the σ the code should inject:

| | LAD | LCx | RCA | RMS |
|---|---|---|---|---|
| before removing measurement error | 0.207 | 0.305 | 0.130 | 0.226 |
| **implied `SD_TERRITORY_SHARE`** | **0.170** | **0.281** | **0.051** | **0.192** |

**Step 4 — what is still left in it that should not be.** All of the following inflate the figure and none can
be quantified from the published data:

1. **CT geometry and territory-assignment error.** Lumen segmentation, centreline extraction and the
   LV/RV/vessel assignment all carry error, and it lands in this residual. **In our study that class of error is
   the POSITIVE class**: the negatives are built on *correct* anatomy. Including it in `SD_TERRITORY_SHARE`
   would put segmentation error into the negative class — precisely the category error that
   `CITATION-PHYSIOLOGICAL-SDS-2026-09-19.md` §3.3 identified in Tanade's stenosis-degree term.
2. **CT and catheterisation up to three months apart.** Any real change in the patient between them appears here.
3. **The Qnorm = Q / FFR correction.** With LAD FFR-with-Rayflow at 0.81 ± 0.06, the LAD flow is scaled up by
   ~23 % with its own propagated error, and by much less in the LCx (0.92) and RCA (0.91). **This is a
   vessel-asymmetric correction applied to the vessel that shows the anomaly**, and it is a live alternative
   explanation for part of the LAD bias in §6.
4. **n = 35.** The SE of an SD at n = 35 is ≈ SD/√(2(n−1)) ≈ 12 % relative, so 0.170 carries roughly ±0.02 from
   sampling alone — which does *not* explain the LCx/RCA spread (0.281 vs 0.051 is a factor of 5.5).

**Conclusion of this section.** The honest reading is **0.19 is a ceiling and the true biological + rule-misfit
figure is somewhere below it**, with the vessel-to-vessel spread (0.05 to 0.28) larger than any plausible
precision on a single recommended value. **This is why the recommendation is a band and not a number.**

---

## 4. The measurement-error term to subtract — the double-counting answer

> **Gallinoro E, Bertolone DT, Fernandez-Peregrina E, Paolisso P, Bermpeis K, Esposito G, Gomez-Lopez A,
> Candreva A, Mileva N, Belmonte M, Mizukami T, Fournier S, Vanderheyden M, Wyffels E, Bartunek J, Sonck J,
> Barbato E, Collet C, De Bruyne B.** Reproducibility of bolus versus continuous thermodilution for assessment of
> coronary microvascular function in patients with ANOCA. *EuroIntervention.* 2023;19(2):e155–e166.
> doi:[10.4244/EIJ-D-22-00772](https://doi.org/10.4244/EIJ-D-22-00772). PMID 36809253; PMC10242662.
> **Full text reached via PMC (tables read).**

n = 102 patients, LAD, duplicate measurements in the **same sitting with a 2-minute wait**, randomised order.
Table 1, verbatim:

| Qhyp (mL/min) | 1st | 2nd | Average | R (95 % CI) | **Variability (%)** | **Bias (SD)** | ICC (95 % CI) |
|---|---|---|---|---|---|---|---|
| continuous thermodilution | 203 ± 66 | 218 ± 79 | 211 ± 71 | 0.89 (0.85–0.93) | **11.89 ± 11.54** | **−13.92 (35.48)** | 0.87 (0.78–0.91) |

**⚠️ WHICH STATISTIC — and this is the same trap the project has already been bitten by once.** The column is
headed **"Variability (%)", not "coefficient of variation"**, and the Methods define it as a **difference**
statistic, verbatim:

> "Variability between two measurements (named A and B) was assessed as relative difference and expressed as a
> percentage according to the formula:"

(the formula itself is rendered as an image and could not be read as text — see §10). **A relative difference
between two measurements is an SDD-family quantity and carries a √2 for the second measurement.** Taking
11.89 % at face value as a one-measurement CV would be the same class of error as injecting at the RC instead of
the within-subject SD, which `DETECTOR-SPEC` §5 warns costs a factor of 2.8.

**So the figure is derived from the unambiguous Bland-Altman statistic instead, which is in the same table:**

&nbsp;&nbsp;&nbsp;&nbsp;SD of the paired difference = 35.48 mL/min on a mean of 211 mL/min = **16.8 %**
&nbsp;&nbsp;&nbsp;&nbsp;→ within-subject CV = 16.8 / √2 = **11.89 %** &nbsp; *(our arithmetic)*

The two routes land on the same number to four significant figures, which is reassuring but also suggests the
paper's "Variability" column may already be √2-corrected. **Either way 11.89 % is the correct one-measurement
within-subject CV to subtract**, and the derivation above is the reason, not the column heading.

**Statistic type:** same-sitting test–retest, **so almost purely measurement**, with essentially no biological
between-occasion component. That is exactly the term that must come out of Keulards' residual before it can be
handed to `SD_TERRITORY_SHARE`. It is *not* a between-patient SD.

Also relevant, and it favours us: hyperaemic measurements are the more reproducible ones — *"the reproducibility
of the hyperaemic values of Q and Rµ were significantly better than the corresponding resting values"*
(Qrest variability 17.98 ± 13.99 % vs Qhyp 11.89 ± 11.54 %). Keulards' measurements, like our model, are
hyperaemic.

Corroborating, same protocol in a different population:
**Wong CY, Dawson L, Theriault-Lauzier P, et al. Repeatability and correlation of coronary physiology indices
measured with bolus and continuous thermodilution. *Circ Cardiovasc Interv.* 2025;18(4):e014919.
doi:10.1161/CIRCINTERVENTIONS.124.014919. PMID 40233166.** n = 20 cardiac transplant recipients, LAD, repeats
≥ 2 minutes apart. Qhyp 183 ± 71 then 202 ± 93 mL/min, ICC 0.80 (0.57–0.92). **No CoV is published**; ⚠️ a CoV
reconstructed from the ICC would be ours and is not reported here as a source.

**So, stated explicitly for brief item 3:** *every* figure in §2, §3 and §5 of this document **includes**
measurement error. Only §4 isolates it. The one figure with negligible measurement error is Choy & Kassab's
15.2 %, and that one is missing the calibre→mass leg instead.

---

## 5. Fournier 2021 — the systematic component, independently significant

> **Fournier S, Keulards DCJ, van 't Veer M, Colaiori I, Di Gioia G, Zimmermann FM, Mizukami T, Nagumo S,
> Kodeboina M, El Farissi M, Zelis JM, Sonck J, Collet C, Pijls NHJ, De Bruyne B.** Normal values of
> thermodilution-derived absolute coronary blood flow and microvascular resistance in humans.
> *EuroIntervention.* 2021;17(4):e309–e316. doi:[10.4244/EIJ-D-20-00684](https://doi.org/10.4244/EIJ-D-20-00684).
> PMID 33016881; PMC9724861. **Full text read.**

177 arteries in 69 patients; vessel-specific myocardial mass from CCTA by the **same HeartFlow core lab** as
Keulards, in 15 normals (41 vessels) and 25 patients (71 vessels). Verbatim, Results:

> "In normals, after adjustment for the mass, the average values of Q observed in the three different vascular
> territories were similar (5.9±1.9, 4.9±1.7, and 5.3±2.1 mL/min/g, for the LAD, the LCX and the RCA,
> respectively, p=NS). R micro was lower in the anterior wall than in the two other territories (15.5±5.6,
> 20.6±5.1, and 21.7±6.4 mL/min/g, for the LAD, the LCX and the RCA, respectively, p<0.05)."

(The unit "mL/min/g" on the Rmicro figures is an error in the published paper — Rmicro is a resistance.)

**Two things to take from this, and they point in opposite directions.**

⚠️ **First, the trap.** Those ± are **BETWEEN-PATIENT SDs across pooled vessels**: CV = 32 %, 35 %, 40 %. **They
are not the within-subject between-territory scatter and using them would be wrong by roughly a factor of three.**
The paper says so itself in its conclusion: *"the large ranges of observed hyperaemic values of flow and of
microvascular resistance preclude their clinical use for inter-patient comparison."* This is the single most
tempting wrong number found in the whole search, and it is the closest match to what the brief asked for.

**Second, the bias.** The *means* carry the signal that the unpaired p-value cannot detect. Perfusion per gram
relative to the three-territory mean (5.37 mL/min/g): **LAD +10 %, LCx −9 %, RCA −1 %**. And Rmicro is
**significantly** lower in the anterior wall (p < 0.05), which is the same statement with power, because
resistance is measured per vessel and the mass normalisation enters differently. **Direction agrees with
Keulards**: the LAD territory is over-perfused relative to its anatomical allotment.

⚠️ **Independence caveat, and it is serious.** Fournier and Keulards share nine authors, the same two centres,
the same Rayflow/CoroFlow method and the same HeartFlow mass core lab, and the patient sets overlap. **They are
one body of evidence, not two.** If the LAD anomaly is an artefact of how HeartFlow assigns septal myocardium,
both papers would show it identically. No independent replication with a different mass algorithm was found.

### 5.1 ⚠️ A published attack on exactly these per-gram numbers

> **Johnson NP, Gould KL.** Hybrid quantification of absolute perfusion requires accurate measurement of
> myocardial mass. *EuroIntervention.* 2024;20(19):e1196–e1198.
> doi:[10.4244/EIJ-E-24-00051](https://doi.org/10.4244/EIJ-E-24-00051). PMID 39374093; PMC11443250.
> **Editorial, full text read.**

Verbatim:

> "downstream myocardial mass using the Voronoi algorithm has only been compared against relative mass
> (percentage of the left ventricle, not absolute grams of tissue)"

> "Among 15 normal controls and 25 patients with mild atherosclerosis, hyperaemic perfusion reached approximately
> 5 mL/min/g … This rate of perfusion substantially exceeds the average stress value of 3 mL/min/g noted in
> almost 550 normal subjects"

> "Inaccurate measurement of myocardial mass likely explains this disagreement"

"15 normal controls and 25 patients with mild atherosclerosis" **is Fournier 2021's exact CT subgroup**. So
Gould's group holds that the absolute per-gram values in §5 are inflated by ~60 % through mass error.

**How much of §3 does this damage? Less than it first appears, and the reason is worth stating.** Keulards
compares **shares** — percentages of the total — and a *global* scale error in the mass algorithm cancels
exactly in a share. The criticism therefore lands hard on Fournier's 5.9/4.9/5.3 mL/min/g (§5) and only
indirectly on Keulards' 5.3/−2.0/−3.1 pp (§3), through whatever part of the mass error is
**territory-differential** rather than global. **That differential part is unquantified** (§10).

### 5.2 How large is the mass-assignment error itself?

The one paper that measures it against a physical reference:

> **Malkasian S, Hubbard L, Abbona P, Dertli B, Kwon J, Molloi S.** Vessel-specific coronary perfusion
> territories using a CT angiogram with a minimum cost path technique and its direct comparison to the American
> Heart Association 17-segment model. *Eur Radiol.* 2020;30(6):3334–3345.
> doi:[10.1007/s00330-020-06697-w](https://doi.org/10.1007/s00330-020-06697-w). PMID 32072257; PMC7416454.
> **Full text read (by the CT-strand search agent; figures quoted from its report).**

Six swine, 24 territory measurements. Verbatim: *"The overall relative RMSE for the AHA and MCP techniques were
16.24 ± 18.25% and 6.08 ± 6.38%, respectively."* Absolute RMSE 2.38 g (AHA) vs 1.12 g (MCP); Dice 0.82 ± 0.13
vs 0.92 ± 0.06. Inter-observer on the AHA method: *"The mean mass of LCA AHA perfusion territories was 48.22 ±
5.12 g for reader 1 and 54.37 ± 4.53 g for reader 2"* — a 6 g shift on the same hearts.

⚠️ **Do not quote this paper's R² = 1.00.** The agent flagged, correctly, that the data form only two clusters
(LCA ≈ 42 g, RCA ≈ 11 g) in six animals; RMSE is the honest statistic.

**Consequence for §3.3 step 4 item 1:** a *good* territory-assignment algorithm carries ≈ **6 %** relative mass
error, and a segment-model one ≈ **16 %**. If HeartFlow's volume-based assignment sits near the good end, then
roughly 0.06 of the Keulards residual is mass-assignment error, which would take the RMS implied
`SD_TERRITORY_SHARE` from 0.19 down to about **0.18** — a small correction. If it sits near the AHA end, the
correction is much larger. **Which end it sits at is not established** (§10).

### 5.3 The largest systematic effect in this literature is dominance, not vessel identity

> **Stalikas N, Mizukami T, Bouisset F, … Collet C.** Vessel-specific myocardial mass in patients with stable
> coronary artery disease. *J Am Heart Assoc.* 2025;14(22):e039013.
> doi:[10.1161/JAHA.124.039013](https://doi.org/10.1161/JAHA.124.039013). PMID 41195772; PMC12887209.
> **Full text read (by the CT-strand search agent).** 948 patients, 9,228 branches, Voronoi.

Verbatim: *"the LAD subtended 42.5% [37.9–48.1] of the LV mass, and the LCX and RCA subtended 28.8% [21.9–35.7]
and 26.4% [20.9–31.9] of the LV mass, respectively."* ⚠️ **Those IQRs are BETWEEN-PATIENT**, not
between-territory within a patient — do not use them for this constant.

And: *"Patients with a left dominant coronary circulation exhibited a significantly greater mass subtended by
the LCX compared with those with right dominance (47.5% [39.4–52.6] versus 27.7% [21.0–33.7], P<0.001)."*

**Why this is reassuring rather than alarming for our model.** Dominance changes territory share by a factor of
~1.7, far more than any SD discussed here — but our rule reads calibre off the **patient's own segmented tree**,
so a left-dominant patient's large LCx is seen as large. Dominance is largely absorbed by the anatomy, not left
in the residual. (The frozen cohort CSV carries a `dominance` column, so this is checkable rather than assumed.)
It does mean that any literature figure derived from a **population-average** territory assignment carries
dominance variance that ours does not, and is therefore inflated.

### 5.4 The one published per-vessel limits-of-agreement figure

> **Murai T, van de Hoef TP, van den Boogert TPW, Wijntjens GWM, Stegehuis VE, Echavarria-Pinto M, Hoshino M,
> Yonetsu T, Planken RN, Henriques JPS, Escaned J, Kakuta T, Piek JJ.** Quantification of myocardial mass
> subtended by a coronary stenosis using intracoronary physiology. *Circ Cardiovasc Interv.* 2019;12(8):e007322.
> doi:[10.1161/CIRCINTERVENTIONS.118.007322](https://doi.org/10.1161/CIRCINTERVENTIONS.118.007322).
> PMID 31518164. **Abstract only** (publisher returned HTTP 403 to the search agent).

43 vessels in 32 patients. Verbatim: *"Median PMM was 15.8 g (Q1, Q3: 11.7, 28.4 g) for physiology-based PMM,
and 17.0 g (Q1, Q3: 12.5, 25.9 g) for computed tomography-based PMM (P=0.84) … Bland-Altman analysis documented
a mean bias of 0.5 g (limit of agreement: −9.1 to 10.2 g)."*

LoA of about ±10 g on a median of ~16 g is **±60 %**, i.e. an SD of the difference of ≈ 4.9 g ≈ **31 % relative**
(our arithmetic). **But the "physiology-based" predictor is APV × D² — a Doppler velocity times an area**, so
this is flow-vs-mass agreement with Doppler measurement error in it, not calibre-vs-mass. It is quoted as an
**upper bound and a caution**, not as a source for the constant.

### 5.5 The independent modality: PET and CMR give the perfusion-per-gram leg, and it is SMALLER

Everything in §3–§5.4 is one method family (CT anatomy + invasive thermodilution). A parallel search of the
PET/CMR perfusion literature gives a genuinely independent estimate of the **mass→flow leg** — how much
perfusion per gram differs between regions of one heart.

> **Chareonthaitawee P, Kaufmann PA, Rimoldi O, Camici PG.** Heterogeneity of resting and hyperemic myocardial
> blood flow in healthy humans. *Cardiovasc Res.* 2001;50(1):151–161.
> doi:[10.1016/S0008-6363(01)00202-4](https://doi.org/10.1016/S0008-6363(01)00202-4). PMID 11282088.
> **Full text read** (via a Wayback snapshot of a green-OA copy; the publisher PDF is Cloudflare-blocked).

169 healthy volunteers, ¹⁵O-water, adenosine or dipyridamole. Four whole-wall ROIs (septal, anterior, lateral,
inferior) drawn on 12 consecutive planes — roughly a quarter LV each, so **close to our territory scale**.
Verbatim, and note the design is explicitly within-subject:

> "The true variability of baseline MBF was assessed by comparing paired estimates of regional baseline MBF
> **within each individual at a single time point**. … The dispersion among these four regions may be summarized
> by the average coefficient of variation, which was **13±8%** for both uncorrected and corrected estimates of
> baseline flow."

> "The dispersion was slightly greater than for baseline MBF with a coefficient of variation of **17±10%**."
> *(hyperaemia — the relevant state for us)*

**This is the single closest published match to the mass→flow leg of our constant: a within-subject,
between-region CV of 17 % under hyperaemia.** The ±10 is the between-subject SD *of that within-subject CV*
across 169 people, not a population spread — a distinction worth keeping straight.

⚠️ **The between-subject numbers in the same paper, for contrast, and they must not be used:**
global hyperaemic MBF *"3.542±1.010 ml/min/g … coefficient of variation 29%"*; Fig. 4 legend, regional
hyperaemic distribution, *"The coefficient of variation was **34.1%**."* **Twice the within-subject figure.**

**Does 17 % include measurement error? Yes, entirely, and the paper does not separate it.** Worse, the same
lab's reproducibility study suggests the measurement term alone could account for most of it:

> **Kaufmann PA, Gnecchi-Ruscone T, Yap JT, Rimoldi O, Camici PG.** Assessment of the reproducibility of
> baseline and hyperemic myocardial blood flow measurements with ¹⁵O-labeled water and PET. *J Nucl Med.*
> 1999;40(11):1848–1856. PMID 10565780. **Full text read (PDF).** 21 healthy men, same 4-ROI scheme.

> "for all left ventricular segments, regional MBF showed a **higher repeatability coefficient, indicating a
> reduced agreement** compared to the resting global MBF."
> "This measure of repeatability **accounts for both methodological error and any physiological variability**."

Its Table 2 repeatability coefficients under hyperaemia are **global 25 %, regional 41–59 %**
(⚠️ **reconstructed from a column-merged PDF table by the PET-strand search agent and flagged by it as needing
eyes on the printed page — do not cite without checking**). Converting RC → one-measurement wsCV by RC/2.77
gives **global ≈ 9 %, regional ≈ 15–21 %**.

**So the PET route says: observed between-region dispersion 17 %, of which the measurement term is plausibly
15–21 %, leaving a biological term near zero.** That subtraction over-corrects — part of the test–retest
variation is a *global* flow shift shared by all regions, which does not contribute to within-scan
between-region dispersion — but the direction is unambiguous: **most of the 17 % is measurement.**

⚠️ **A spillover finding the project should log separately.** `WSCV_TARGET = 0.083` rests on Lubberink 2024
(regional RC 23 % → wsCV 8.3 %). Kaufmann 1999, full text, same tracer, same 4-region scheme, gives a
**regional hyperaemic RC of 41–59 %, i.e. a wsCV of 15–21 % — roughly double.** Modern PET is better than
1999 PET, so 8.3 % may well be right today; but **an older, full-text-verified source disagrees by 2×, and
that is worth a sentence in `CITATION-VALIDATED-RESIDUAL-2026-09-19.md` rather than silence.**

### 5.6 The only source that separates biological from methodological dispersion — and it settles the scale question

> **Bassingthwaighte JB, King RB, Roger SA.** Fractal nature of regional myocardial blood flow heterogeneity.
> *Circ Res.* 1989;65(3):578–590. doi:[10.1161/01.res.65.3.578](https://doi.org/10.1161/01.res.65.3.578).
> PMID 2766485; PMC3361973. **Full text read.** Baboons, sheep, rabbits; microspheres.

This is the one paper in the entire search that does the decomposition properly. Verbatim:

> "the observed dispersion (RD_obs) is the composite of at least two dispersive processes which we will
> distinguish as spatial dispersion (RD_s) and methodological dispersion (RD_M)." … "RD_S² = RD_obs² − RD_M²"

> "The relative dispersions … were **about 35%** … when observations were made by **dividing the hearts into
> 100–250 pieces**." … "**use of large tissue pieces underestimates the degree of observable heterogeneity**"

> "RD(m) = RD(m_ref)·(m/m_ref)^(1−D)"

Measurement-corrected spatial dispersion at a 1 g reference: **baboons RD_s 11.4–21.8 %** (fractal dimension
D_s 1.14–1.29), sheep 9.3–43.0 %, rabbits 7.0–25.6 %.

**Extrapolating their own law to a quarter-LV region of 30–45 g** (the PET-strand agent's arithmetic, and it
extrapolates well beyond the ≤10 g aggregates they actually tested, in another species):

| RD_s(1 g), D | 30 g | 37 g | 45 g |
|---|---|---|---|
| 15 %, 1.20 (typical baboon) | 7.6 % | 7.3 % | 7.0 % |
| 11.4 %, 1.19 (lowest) | 6.0 % | 5.7 % | 5.5 % |
| 21.8 %, 1.14 (highest) | 13.5 % | 13.1 % | 12.8 % |

**So the expected *purely biological* spatial dispersion at three-territory scale is ≈ 6–13 %, centred near
7 %** — and the residual once that is removed from Chareonthaitawee's 17 % is ≈ 15 %, which matches Kaufmann's
regional measurement estimate almost exactly. Three independent routes close.

**The scale effect is also visible inside single human datasets, which is easier to defend than an
extrapolation.** Brown 2023's own data span **~12 % between territories but ~28 % between AHA segments**
(*"highest in AHA Segment 1 (basal anterior) 2.63 ± 0.73 … and lowest in Segment 15 (apical inferior)
1.90 ± 0.46"*). Lyu 2022 is null between territories (P = 0.399) and significant between 17 segments
(P = 0.006) **in the same scans**. Greve 2014 (*J Cardiovasc Magn Reson* 16(Suppl 1):P21, PMC4044203 — ⚠️ an
SCMR **conference abstract** that was never developed into a full paper, zero Europe PMC citations) states the
scale in grams explicitly: RD **13.0 %** at rest and **15.9 %** at stress *"at the intrinsic image acquisition
resolution (1 voxel = 0.07 g)"*, falling *"in a highly-significant pattern"* as voxels are aggregated to 0.27,
0.61 and 1.1 g — ⚠️ though those three values appear **only in a figure** and could not be read.

**And this kills the most tempting wrong citation in the field.** The famous microsphere figure of **35 %**
heterogeneity is measured on 100–250 pieces, i.e. sub-gram samples. Quoting it at territory scale would
overstate this constant by roughly **five-fold**. Gould makes the same point in print — Johnson NP, Gould KL,
*J Nucl Med* 2005;46(9):1427–37, PMID 16157524, full text read: *"the heterogeneity that we observe by PET
perfusion imaging is **separate and unrelated to the dispersion of perfusion in small 1-mm myocardial samples
for microsphere measurements** of perfusion reported for experimental animals."* And de Jong 1995
(*J Nucl Med* 36:581–5, PMID 7699445, full text read) states the mechanism outright: the relative dispersion
*"has the disadvantage of being influenced by the size of myocardial samples employed to analyze perfusion."*

**The nearest thing to a formal variance decomposition in humans**, and it is not on MBF:

> **Hoshino M, Hoek R, Jukema RA, et al.** Homogeneity of the coronary microcirculation in angina with
> non-obstructive coronary artery disease. *Eur Heart J Cardiovasc Imaging.* 2025;26(7):1120–1127.
> doi:[10.1093/ehjci/jeaf101](https://doi.org/10.1093/ehjci/jeaf101). PMID 40126977; PMC12206580.
> **Full text read.** 155 ANOCA patients, 465 vessels, [¹⁵O]H₂O PET + three-vessel FFR, whole-territory scale
> (*"MBF was defined as the mean MBF of the entire vascular territory"*).

> "There was no significant difference in CFR among the regions … and similarly, there were no significant
> differences in MRR among the three coronary branches (MRR: LAD 4.04 ± 1.21, RCA 3.97 ± 1.29, LCX 3.74 ± 1.11,
> and P = 0.697)." … "**The overall ICC was 0.80 (95% CI: 0.74–0.85) for absolute agreement**" …
> "Mean differences were 2.4% (Lower limit: −38.7 to upper limit: 43.4) for LAD/RCA, 5.1% (−29.2 to 39.4) for
> RCA/LCX, and 7.5% (−23.1 to 38.1) for LAD/LCX"

⚠️ Its *"CV for MRR measurements were 30.0% for LAD, 32.6% for RCA, and 29.5% for LCX"* are **between-subject**
(they are simply SD/mean of the cohort — 1.21/4.04 = 30.0 %, verified). The **within-subject** information is
in the ICC and the limits of agreement: SD of the paired territory difference = 20.9 / 17.5 / 15.6 %, giving a
per-territory within-subject SD of **≈ 11–15 %**, and ICC = 0.80 means **≈ 20 % of total variance is
between-territory-within-subject plus measurement** *(the PET-strand agent's arithmetic, not the authors')*.
It is MRR, not MBF, in patients, not normals — but it lands in the same **11–15 %** window as everything else.

### 5.7 Reconciling the two method families — the decomposition that actually resolves the question

The CT+thermodilution route (§3) and the PET/CMR route (§5.5–5.6) measure **different legs of the same chain**,
and once that is seen they stop disagreeing:

| leg | what it is | best estimate | source |
|---|---|---|---|
| **mass → flow** | does each gram of a territory get the same perfusion? | **≈ 7–15 %** | Bassingthwaighte extrapolation ≈ 7 %; Chareonthaitawee 17 % minus measurement ≈ 8 %; Choy & Kassab 15.2 % |
| **calibre → mass** | does the r^2.66 rule predict the subtended mass? | not cleanly isolated anywhere | — |
| **both, combined** | the quantity the code needs | **≈ 0.19 RMS**, an upper bound | Keulards §3.3 |

Taking the combined figure and the first leg together, the implied calibre→mass leg is
√(0.19² − 0.10²) ≈ **0.16** *(our arithmetic)* — the larger of the two, which is consistent with §8's finding
that the exponent itself is contested and vessel-dependent, and with §10 item 11's failure to reach the Seiler
papers where a published figure for it would most likely live.

**The practical upshot, and it changes the reading of 0.10.** If the model needed only the perfusion-per-gram
leg, **0.10 would be an excellent central value**. It needs both legs, so **0.10 sits at the low end**.
That is a much more precise statement than "0.10 is defensible", and it is the basis of §9.

---

## 6. Is the departure systematic? — brief item 4

**Yes, in part.** Consolidating §3 and §5, the best available estimate of the *mean* departure of measured
hyperaemic flow share from the anatomical prediction is:

| territory | bias (percentage points of total flow) | bias (relative to that territory's share) |
|---|---|---|
| LAD | **+5.3** | ≈ +13 % |
| LCx | **−2.0** | ≈ −7 % |
| RCA | **−3.1** (Abstract: −3.2) | ≈ −10 % |

The three sum to +0.2 pp, consistent with the sum-to-one constraint the model's renormalisation also imposes.

### 6.1 Independent replication in a different modality — this removes the main caveat

§5 warned that Keulards and Fournier are one body of evidence. **Two large CMR normal-value cohorts, with no
HeartFlow involvement, no invasive measurement and a within-subject statistical test, find the same ordering.**

> **Brown LAE, Gulsin GS, Onciul SC, Broadbent DA, … Greenwood JP, Moon JC, Adlam D, McCann GP, Plein S.**
> Sex- and age-specific normal values for automated quantitative pixel-wise myocardial perfusion cardiovascular
> magnetic resonance. *Eur Heart J Cardiovasc Imaging.* 2023;24(4):426–434.
> doi:[10.1093/ehjci/jeac231](https://doi.org/10.1093/ehjci/jeac231). PMID 36458882; PMC10029853.
> **Full text read.** n = 150 healthy, 3 T.

> "When coronary artery territories were compared, both rest and stress flow were **highest in the left anterior
> descending (LAD) artery territory**, with significant differences between the three territories"
> … "Differences between coronary territories were compared using **repeated measures analysis of variance**."

Stress MBF: **LAD 2.36 ± 0.57, Cx 2.25 ± 0.56, RCA 2.10 ± 0.50 mL/g/min, P < 0.001.** ⚠️ **Those ± are
between-subject** (the paper's own CV% column, 23.8–24.9 %, is a population spread) — but **the test is
within-subject**, so the ordering is real. LAD − RCA = 0.26 mL/g/min ≈ **12 % of global** *(our arithmetic)*.

> **Kamani CH, Brown L, Anderton T, … Plein S.** Normal values of high-resolution transmural perfusion
> distribution metrics for automated quantitative pixel-wise myocardial perfusion cardiovascular magnetic
> resonance. *J Cardiovasc Magn Reson.* 2025;27:101927.
> doi:[10.1016/j.jocmr.2025.101927](https://doi.org/10.1016/j.jocmr.2025.101927). PMID 40543719; PMC12445411.
> **Full text read.** n = 138 healthy.

> "**Most ENDO and EPI stress and rest MBF values were higher in the LAD territory and lower in the RCA
> territory.**" (stress LAD 2.34 ± 0.56, LCX 2.23 ± 0.56, RCA 2.09 ± 0.49)

**What replicates, stated precisely: the RCA / inferior territory is consistently the LOWEST. The LAD-vs-LCx
ordering does not replicate.**

| source | modality | n | finding |
|---|---|---|---|
| Keulards 2020 | thermodilution + CT share | 35 | LAD +5.3 pp, LCx −2.0, RCA −3.1 |
| Fournier 2021 | thermodilution + CT mass | 15 normals | Rmicro lowest in anterior wall, **p < 0.05** |
| Brown 2023 | CMR pixel-wise | 150 | LAD > Cx > RCA, **p < 0.001** (repeated-measures ANOVA) |
| Kamani 2025 | CMR pixel-wise | 138 | "higher in the LAD territory and lower in the RCA territory" |
| Chareonthaitawee 2001 | ¹⁵O-water PET | 169 | inferior wall lowest, **p < 0.001** within-subject |
| ⚠️ Piccinelli 2020 | ¹³N-ammonia PET | 16 | **LCX 3.28 > LAD 2.64 > RCA 2.14** — LCx highest, contradicting Brown; **and the authors never test territory vs territory** |

Magnitudes where tested: ~12 % LAD-vs-RCA in CMR, ~15 % anterior-vs-inferior in PET at rest, ~23 % in Keulards.

⚠️ **But the effect is weaker or absent at HYPERAEMIA, which is our state, and two datasets are null.**

- **Brown LAE, Onciul SC, Broadbent DA, et al.** Fully automated, inline quantification of myocardial blood
  flow with CMR: repeatability of measurements in healthy subjects. *J Cardiovasc Magn Reson.* 2018;20(1):48.
  doi:[10.1186/s12968-018-0462-y](https://doi.org/10.1186/s12968-018-0462-y). PMID 29983119; PMC6036695.
  **Full text read.** n = 42. The same group's earlier cohort: *"MBF in the LAD was higher than the Cx
  territory on both visits (mean difference 0.09 ml/g/min, p = 0.01 on the first scan, and 0.08 ml/g/min,
  p = 0.04 on the second)"* — **but "No significant difference was seen between coronary territories in stress
  MBF."** So the LAD excess replicates at rest and does not reach significance at stress in n = 42.
- Chareonthaitawee 2001's **cohort-level** ANOVA at hyperaemia is null: *"there were **no statistically
  significant differences (ANOVA) in hyperemic MBF among the four myocardial regions**"* — while the paired
  within-subject test in the same data is highly significant. **That contrast, inside one paper, is the
  between-vs-within distinction this project keeps running into, and it is worth quoting in the manuscript.**
- **Lyu L, Pan J, et al.** *Front Cardiovasc Med.* 2022;9:817911. PMID 35187130; PMC8850642. **Full text read.**
  Dynamic CT-MPI, 51 healthy: *"Hyperemic MBF values were **homogeneously distributed among myocardial regions
  (all P > 0.05)**, but not among 17 myocardial segments (P = 0.006)"* — LAD 167 ± 24, RCA 164 ± 24,
  LCX 160 ± 25, **P = 0.399**. A clean demonstration of the scale point: **null at territory scale, significant
  at segment scale, in the same data.**

**Net reading: the bias is real at rest, and at hyperaemia it is small, inconsistent, and of the same order as
the measurement noise.** That is a further argument for §6.3's recommendation not to model it.

### 6.2 ⚠️ The artefact case against all of it, which is strong

Before anyone models a +5 pp LAD term, note how easily this literature manufactures exactly that finding:

- **Miller CA, Hsu L-Y, Ta A, Conn H, Winkler S, Arai AE.** Quantitative pixel-wise measurement of myocardial
  blood flow: the impact of surface coil-related field inhomogeneity and a comparison of methods for its
  correction. *J Cardiovasc Magn Reson.* 2015;17(1):11.
  doi:[10.1186/s12968-015-0117-1](https://doi.org/10.1186/s12968-015-0117-1). PMID 25827156; PMC4323126.
  **Full text read.** Verbatim: *"when the analysis was performed without surface coil intensity correction,
  **MBF was calculated to be 60% higher in the septum compared to the lateral wall**"*, and heterogeneity fell
  from *"36.2 ± 6.3%"* uncorrected to *"20.8 ± 3.0%"* corrected — **and the sign of the septal difference
  reverses.** (Brown 2023 does apply proton-density coil correction.)
- **Hove JD, Gambhir SS, Kofoed KF, Kelbaek H, et al.** Dual spillover problem in the myocardial septum with
  nitrogen-13-ammonia flow quantitation. *J Nucl Med.* 1998;39(4):591–598. PMID 9544662. **Full text read.**
  *"the **septal flow may be underestimated by 0%–30%**"* — a tracer-specific bias on the LAD territory.
- **de Jong RM, Blanksma PK, Willemsen ATM, et al.** *J Nucl Med.* 1995;36(4):581–585. PMID 7699445.
  **Full text read.** Apical and inferior regional differences attributed to *"a partial volume effect"* and
  *"spillover from the liver"* respectively.
- Chareonthaitawee's own authors decline to adjudicate: *"it was not within the scope of this study to
  differentiate as to whether the observed reduction in flow to the inferior wall … is a true biological
  phenomenon or a methodological artifact."*

### 6.3 The verdict on the bias

**Whether this should be modelled is a judgement, and the honest answer is "no, but it must be stated".**
Four reasons for caution:

1. **It may be a mass-assignment or imaging artefact, not physiology.** The LAD supplies the interventricular
   septum; how septal mass is allotted between LAD and RCA is an algorithmic choice, and the septum is also
   exactly where both the CMR coil profile (Miller 2015) and ¹³N-ammonia spillover (Hove 1998) do their damage.
   That **three different methods each have a septum-specific failure mode pointing the same way** is a real
   alternative explanation for a consistent LAD finding.
2. **It is vessel-identity-specific, and our model's territories are not vessel-identified.**
   `ablation.territories()` returns *"the subtrees rooted at each child of the first branching node"* — for a
   left tree these are LAD and LCx, but the code never labels them, and for a right tree they are not LAD/LCx/RCA
   at all. Applying a +5.3 pp LAD bias would require a vessel-identification step the pipeline does not have.
3. **The Qnorm = Q/FFR correction is applied most strongly to the LAD** (§3.3 item 3), so part of the bias may be
   methodological.

**Recommended handling:** do **not** add a bias term to `negatives.py`. Instead (a) state in the paper that the
anatomical prediction of territory flow share is known to carry a **systematic LAD excess of ≈ 5 pp of total
flow (≈ 12–23 % relative to the RCA)** in addition to random scatter, citing Keulards and Fournier for the
invasive evidence and **Brown 2023 and Kamani 2025 for independent CMR replication**; (b) state the artefact
counter-case (§6.2) and the two null results (§6.1) in the same breath, because the honest position is that the
effect is reproducible but its cause is unsettled; (c) note that the model represents only the random part, so
the negative class is, in this one respect, **easier than reality** — a limitation in the unsafe direction that
must be declared as such; and (d) offer the sensitivity arm in §7 as the quantitative answer to "how much would
it matter".

---

## 7. What the constant actually does — measured, not argued

`CITATION-PHYSIOLOGICAL-SDS-2026-09-19.md` §7 item 9 recorded that the claim "the share SD dominates the
residual" was *"an inference from code, not a result"* and asked for it to be run. It has now been run.

**Probe** (`references/CITATION-TERRITORY-SHARE-2026-09-19-probe/sweep_share_sd.py`): monkeypatches
`negatives.SD_TERRITORY_SHARE` and re-runs the **same 50 cohort instances, same bed (`leaky`), same seed
(20260919), 2 draws each**, so the only thing that differs between arms is the constant. Nothing in `code/`,
`protocol/` or `results/` is touched. Raw output: `sweep_share_sd.csv` and `sweep_share_sd.log` in the probe
directory.

**Cross-check that the probe is not measuring something else.** The project's own
`results/negatives_smoke-2026-09-19.csv` (36 rows, all `ok`) has median residual **0.0718** and pass rate
**63.9 %** at the shipped constant. The probe's `sd = 0.10` arm gives **0.0705** and **68 %** on a different,
larger instance subset. The probe reproduces the shipped pipeline.

### 7.1 The sweep

| `SD_TERRITORY_SHARE` | n ok | residual median | residual p10–p90 | **passes the 0.10 check** | \|dFFR\| median | \|dFFR\| p90 | flips | C_ratio IQR |
|---|---|---|---|---|---|---|---|---|
| 0.00 (measurement noise only) | 100 | 0.0413 | 0.0099–0.0946 | **92 %** | 0.0194 | 0.0436 | 0 | 0.148 |
| 0.05 | 100 | 0.0479 | 0.0081–0.1037 | **85 %** | 0.0195 | 0.0426 | 0 | 0.149 |
| **0.10 (shipped)** | 100 | **0.0705** | 0.0138–0.1422 | **68 %** | **0.0190** | 0.0438 | 0 | 0.139 |
| 0.15 | 100 | 0.0977 | 0.0190–0.1880 | **53 %** | 0.0206 | 0.0471 | 0 | 0.149 |
| 0.20 | 97 | 0.1208 | 0.0270–0.2472 | **43 %** | 0.0225 | 0.0592 | 2 | 0.165 |
| 0.25 | 97 | 0.1334 | 0.0266–0.3055 | **40 %** | 0.0243 | 0.0758 | 5 | 0.160 |

50 instances × 2 draws, `leaky` bed, seed 20260919, identical across arms.

**Three results, and they do not all point the same way.**

1. **The validation gate's specificity is almost entirely set by this constant.** Across the literature-supported
   band 0.05–0.20 the pass rate runs **85 % → 43 %**, a factor of two. At the shipped 0.10 it is **68 %** on this
   subset (DETECTOR-SPEC §5 predicts ~77 %; the difference is the instance subset and the `leaky`-only bed).
   With `SD_TERRITORY_SHARE = 0`, i.e. measurement noise alone, it is 92 % — so **roughly three-quarters of the
   negatives' failure rate at the 10 % check comes from this one uncited number.** The brief's concern is
   confirmed quantitatively.

2. **But the dFFR noise floor is almost immune to it**, and that is the more important result for the paper.
   The median |dFFR| moves only **0.0190 → 0.0225** over 0.10 → 0.20, and only to 0.0243 at 0.25 — against
   `MATERIAL_DFFR = 0.05`. `negatives.py` calls this *"the single most useful number here"*, and it is stable.
   **So the study's physiological claim — the irreducible FFR error a correctly-segmented model still makes —
   does not depend on the constant under review.** Only the "passes its validation check X % of the time"
   claim does. That is worth saying explicitly in the paper, because it converts a weakness into a bounded one.
   (The p90 is less stable: 0.0436 → 0.0758 over the same range, so the *tail* of the floor is sensitive even
   though the median is not.)

3. **The Gaussian share draw starts to break above 0.20.** At 0.20 and 0.25 three of 100 draws no longer
   return `status == "ok"` (the single global scaling hits the search bound), and the first sign flips appear
   (2 at 0.20, 5 at 0.25). **Do not extend the sensitivity band above 0.20 without changing the draw** — an
   unconstrained `N(1, σ)` multiplier at σ = 0.25 puts appreciable mass near zero and below, which is not a
   physiological perturbation. A log-normal multiplier would be the natural fix if the band ever needs to go
   higher.

### 7.2 A caution about reading "specificity" off this table

The probe measures **the negative class only**. It does not compute AUC, because that needs the positives run
under the same arms, which was outside this brief. Two things should be said before anyone reads a detector
conclusion into the numbers above.

**First, the quantity the table does settle is the one DETECTOR-SPEC §5 quotes.** §5 states that at the
published wsCV *"a threshold of 0.10 passes a correct-but-noisy model about **77 %** of the time"*, and offers
that as the operating characteristic that turns `VALIDATED_RESIDUAL = 0.10` into something other than an
arbitrary constant. That 77 % is a direct function of `SD_TERRITORY_SHARE`, and the table shows how strongly.
**The headline specificity of the validation gate is set by an uncited constant**, which is exactly what the
brief suspected.

**Second, the sign of the effect on AUC is not obvious and should not be guessed.** From the existing
positives run (`results/ablation_smoke_DETECTORCOLS-2026-09-19.csv`, Protocol C, n = 38 rows with
`status == "ok"`), the **positives'** residuals are *median 0.0119, IQR 0.0040–0.0209, and only 5 % exceed
0.10*. At `SD_TERRITORY_SHARE = 0.10` the **negatives'** median residual is 0.0705. **The negatives' residuals
are larger than the positives'** — because the positives are fitted to noiseless targets while the negatives are
fitted to noisy ones. A residual-threshold rule therefore does not separate the classes in the direction
DETECTOR-SPEC §5's "residual > 0.001" sketch assumes, and raising `SD_TERRITORY_SHARE` pushes the two
distributions further apart in the *inverted* direction.

**That is a finding about the detector's design, not about this constant, and it is flagged rather than
resolved here.** It does mean the honest claim is the narrow one: this constant sets **the pass rate of the
10 % validation check on correct models**, monotonically and steeply. Whether it also sets AUC, and in which
direction, needs the positives re-run across the same arms — a one-line extension of the probe script.

---

## 8. A separate uncited constant this search surfaced: `MURRAY_EXP = 2.66`

`zerod_ffr.py` L37: `MURRAY_EXP = 2.66  # leaf outlet weight r_ref^MURRAY_EXP; empirical coronary exponent
(Murray: 3)`. Uncited.

> **Taylor DJ, Saxton H, Halliday I, Newman T, Hose DR, Kassab GS, Gunn JP, Morris PD.** Systematic review and
> meta-analysis of Murray's law in the coronary arterial circulation. *Am J Physiol Heart Circ Physiol.*
> 2024;327(1):H182–H190. doi:[10.1152/ajpheart.00142.2024](https://doi.org/10.1152/ajpheart.00142.2024).
> PMID 38787386; PMC11380967. **Full text reached via PMC.**

1,070 unique coronary trees from 372 humans and 112 animals, 18 studies pooled. Verbatim:

> "The pooled flow diameter exponent across both epicardial and transmural arteries was 2.39 (95% confidence
> interval: 2.24–2.54; I2 = 99%)."

Subgroups: humans 2.42 (2.17–2.67); animals 2.36 (2.17–2.55); epicardial 2.43 (2.25–2.61); transmural 2.21
(1.93–2.49). **I² = 99 %** — the between-study heterogeneity is essentially total, so the CI understates the
real uncertainty.

Corroborating in humans in vivo: **Choi JH, Kim E, Kim HY, Lee SH, Kim SM.** Allometric scaling patterns among
the human coronary artery tree, myocardial mass, and coronary artery flow. *Physiol Rep.* 2020;8(14):e14514.
doi:[10.14814/phy2.14514](https://doi.org/10.14814/phy2.14514). PMID 32725793; PMC7387886. **Full text read.**
638 arteries from 43 patients by CCTA with Voronoi-tessellation segment-specific mass; flow in 106 arteries by
QFR. Table 3, adjusted for individual: **Q–D exponent 2.271 ± 0.235 (r² 0.605)**; D–M 0.224 ± 0.082 (r² 0.665),
i.e. m ∝ D^4.5, which is *not* the 8/3 law. ⚠️ Choi's Q is QFR-derived (frame-count velocity × lumen area), so
Q–D is partly circular — treat the exponent as supportive, not independent.

**Choi's D–M scatter, reconstructed — and why it is NOT usable as the constant.** Choi reports r² = 0.665 for
D–M adjusted for individual (0.541 unadjusted) and, in Table 2, per-vessel myocardial mass 23.0 ± 21.9 cm³
(CV 0.95). Assuming log-normality, SD(log₁₀ M) ≈ 0.35, so the within-patient residual SD of predicted mass is
≈ √(1 − 0.665) × 0.35 ≈ **0.20 log₁₀ units, i.e. ×/÷ 1.6 at one SD** (**reconstruction by the CT-strand search
agent, not a published figure — the paper reports no SEE, residual SD or CV about the regression**).

That is ≈ 50 % relative, far above everything else in this document, and it should **not** be carried into the
constant. Three reasons: (i) the 638 arteries span the whole tree down to small branches, where a small CCTA
diameter error produces a large mass error, whereas our territories are the two subtrees off the first
bifurcation; (ii) the log-normality assumption is ours; (iii) Choi's own Methods caution that OLS *"is based on
the premise of accurate measurement in X-axis values and constant variance in Y-axis values, which may not be
met in real-world dataset."* **It is reported here because it was computed, and because it would have been
tempting to report it as the answer.**

Choi also shows the law is **vessel-dependent**: per-vessel D–M r² = .595 (LAD), .523 (LCx), .429 (RCA), and
verbatim from the Discussion, *"In the comparison among vessels, RCA showed smaller arterial length, arterial
volume, and diameter given the same size of myocardium."* So the RCA is both **biased** (less calibre per gram)
and **noisiest** under a single scaling law. ⚠️ The magnitude of that bias could not be extracted — see §10.

**Why the exponent matters to the constant under review.** Territory share under a leaf rule r^n scales as
(r₁/r₂)^n.
Changing n from 2.66 to 2.39 changes the share *ratio* of two territories whose reference radii differ by 1.5×
by (1.5)^−0.27 ≈ **10 %** (our arithmetic). **That is a systematic redistribution of the same magnitude as
`SD_TERRITORY_SHARE` itself**, and it is currently a silent modelling choice.

**Recommendation for this constant separately:** cite **Choy & Kassab 2008** (V ∝ D^2.51 ± 0.19, compared by the
authors to the 8/3 law) for the 2.66 as used, state that it is a *volume*–diameter law, and add **n = 2.39** to
the sensitivity sweep alongside the share SD. It is a one-line addition to an existing sweep.

---

## 9. RECOMMENDATION

### 9.1 The decision: **(b) — no single value is supportable**

**Do not replace 0.10 with a cited number.** No source publishes the quantity the model needs (within-patient,
between-territory departure of hyperaemic flow share from a calibre rule, with measurement error removed).
Every candidate requires at least one reconstruction step, and the best human source disagrees with itself by a
factor of 5.5 between vessels.

**Instead:**

1. **Keep `SD_TERRITORY_SHARE = 0.10` as the pre-registered primary**, and rewrite the code comment to say what
   it is: a **chosen value inside a literature-supported band of roughly 0.05–0.20**, not a citation.
   0.10 is **defensible but at the low end**, and §5.7 says exactly why:

   | leg of the chain | evidence | figure |
   |---|---|---|
   | mass → flow (perfusion per gram between territories) | Bassingthwaighte extrapolation; Chareonthaitawee minus measurement; Choy & Kassab; Hoshino ICC | **0.07–0.15** |
   | calibre → mass (does r^2.66 predict subtended mass?) | not cleanly isolated anywhere | **unknown** |
   | both — what the code needs | Keulards, measurement-corrected | **≈ 0.19, an upper bound** |

   **If the model needed only the first leg, 0.10 would be an excellent central value. It needs both.**
2. **Report the detector's specificity across a declared sensitivity band of 0.05 / 0.10 / 0.15 / 0.20**, using
   the §7 table (**pass rate 85 % / 68 % / 53 % / 43 %** on the probe subset). Pre-specify the band before
   unblinding; it is already measured, so there is no cost to declaring it. **Do not extend it above 0.20** —
   §7.1 result 3.
   **And report alongside it the result that rescues the paper:** the |dFFR| noise floor moves only
   0.0190 → 0.0225 over that same band, against `MATERIAL_DFFR = 0.05`. The sentence to aim for is *"the
   physiological noise floor on dFFR is insensitive to this assumption over the range the literature supports,
   while the pass rate of the 10 % validation check is not"* — which is a much stronger position than a single
   cited SD would have bought.
3. **State the direction of the residual risk.** 0.10 may be too small, and too small is the direction that
   **flatters** the detector. Say so in those words.
4. **Cite, for the band rather than the value:**
   - Keulards 2020, *Heart*, doi:10.1136/heartjnl-2020-316689 — the human measurement of the whole quantity.
   - Gallinoro 2023, *EuroIntervention*, doi:10.4244/EIJ-D-22-00772 — the measurement-error term removed from it.
   - Chareonthaitawee 2001, *Cardiovasc Res*, doi:10.1016/S0008-6363(01)00202-4 — the independent PET estimate
     of the perfusion-per-gram leg (within-subject between-region CV 17 ± 10 % at hyperaemia).
   - Bassingthwaighte 1989, *Circ Res*, doi:10.1161/01.res.65.3.578 — the scale law, and the one source that
     separates spatial from methodological dispersion. **Cite it for the scale argument, and to pre-empt a
     reviewer quoting the 35 % microsphere figure at you.**
   - Choy & Kassab 2008, *J Appl Physiol*, doi:10.1152/japplphysiol.01261.2007 — the controlled corroboration
     and the source of the 8/3 leaf exponent.
   - Fournier 2021, *EuroIntervention*, doi:10.4244/EIJ-D-20-00684 and Brown 2023, *Eur Heart J Cardiovasc
     Imaging*, doi:10.1093/ehjci/jeac231 — the systematic per-territory component, invasive and CMR.
5. **Fix the renormalisation factor, or at least document it** (§1). The code injects σ and realises ≈ 0.7σ for a
   two-territory tree. If 0.10 is meant as the *realised* share scatter, the injected constant should be ≈ 0.14.
   **This is a semantics decision only the operator can settle**, and it moves the number by 40 % — larger than
   most of the differences argued over above.
6. **Declare the scale limitation** (§1): the literature is at the LAD/LCx/RCA scale, the cohort's 50 right-side
   trees are partitioned finer, and finer partitions are more heterogeneous. Every figure here is a lower bound
   for those.
7. **Do not model the LAD bias** (§6), but declare it.
8. **Separately, cite `MURRAY_EXP = 2.66`** and add 2.39 to the sweep (§8).

### 9.2 Suggested replacement code comment

> ```
> SD_TERRITORY_SHARE = 0.10   # per-territory departure of true perfusion from the anatomical (Murray r^2.66)
>                             # share. NOT A CITED VALUE: no source publishes this quantity with measurement
>                             # error removed. It is the CENTRE of a literature-supported band of 0.05-0.20, and
>                             # the detector's specificity is reported across 0.05/0.10/0.15/0.20
>                             # (references/CITATION-TERRITORY-SHARE-2026-09-19.md).
>                             # Anchors: Keulards 2020 Heart doi 10.1136/heartjnl-2020-316689 measured
>                             # anatomically-predicted vs invasively-measured hyperaemic flow share per territory
>                             # in 35 near-normal patients: SD of the paired difference 6.2/7.4/3.4 percentage
>                             # points for LAD/LCx/RCA, i.e. 0.15/0.27/0.11 relative. That INCLUDES the
>                             # continuous-thermodilution within-subject CV of 11.9 % (Gallinoro 2023 doi
>                             # 10.4244/EIJ-D-22-00772, derived as its Bland-Altman SD of differences 35.48 on a
>                             # mean of 211 mL/min, /sqrt(2) -- NOT its "Variability (%)" column, which is a
>                             # difference statistic); removing it in quadrature leaves ~0.19 RMS, still an
>                             # upper bound because CT geometry error, a <=3-month CT-to-cath interval and the
>                             # Qnorm=Q/FFR correction remain in it. Choy & Kassab 2008 doi
>                             # 10.1152/japplphysiol.01261.2007 give the cleanest low-measurement-error anchor
>                             # for the mass->flow leg alone: perfusion 1.05+/-0.16 mL/min/g across territories,
>                             # CV 15.2 %, in 8 excised porcine hearts. The PET/CMR literature puts that same
>                             # leg at 0.07-0.15 (Chareonthaitawee 2001 doi 10.1016/S0008-6363(01)00202-4:
>                             # within-subject between-region CV 17+/-10 % at hyperaemia, mostly measurement;
>                             # Bassingthwaighte 1989 doi 10.1161/01.res.65.3.578 scale law -> ~7 % at 30-45 g).
>                             # So 0.10 would be right for the perfusion-per-gram leg ALONE; this constant must
>                             # also carry the calibre->mass leg, hence "low end", hence the band.
>                             # DO NOT cite the 35 % microsphere heterogeneity figure: it is measured on
>                             # 100-250 pieces (sub-gram) and overstates territory-scale dispersion ~5x.
>                             # NOTE 1 (renormalisation): the draw is renormalised, so the REALISED relative
>                             # share scatter is ~0.71*SD for a two-territory tree, not SD.
>                             # NOTE 2 (direction): too SMALL flatters the detector. See the sweep.
>                             # NOTE 3 (bias): the departure is partly systematic -- the LAD receives ~5 pp more
>                             # of total flow than the anatomical rule allots (Keulards 2020; Fournier 2021 doi
>                             # 10.4244/EIJ-D-20-00684, Rmicro lower in the anterior wall, p<0.05). Not modelled;
>                             # declared as a limitation, and it makes the negatives easier than reality.
> ```

---

## 10. What I could not establish

Listed plainly, because each is a place where a number could be invented and should not be.

1. **No source publishes the biological-only figure.** Not one paper found measures territory flow share against
   an anatomical prediction *and* removes its own measurement error. Every number in §3 that is net of
   measurement error is **our quadrature subtraction using a repeatability CoV from a different study in a
   different population**. It should be presented as a reconstruction.
2. **The CT-side error in Keulards is unquantified.** Lumen/centreline extraction and territory assignment
   error is inside the 6.2/7.4/3.4 pp and cannot be separated from the published data. Because that error class
   is this study's *positive* class, leaving it in biases `SD_TERRITORY_SHARE` upward by an unknown amount.
3. **Keulards' sign convention was inferred, not stated.** §3.2 resolves it from the paper's own Table 2, and
   the paper's Abstract and Results disagree by 0.1 pp on the RCA mean. If the direction of the LAD bias matters
   to a downstream decision, **check Figure 2's Bland-Altman axis labels in the PDF** — that would settle it in
   one look and was not done here.
4. **Keulards and Fournier are not independent.** Nine shared authors, same centres, same method, same mass core
   lab, overlapping patients. **No replication of the LAD excess with a different mass algorithm was found**, so
   it cannot be distinguished from a HeartFlow septal-assignment artefact.
5. **Choy & Kassab's 15.2 % is not decomposed** into between-heart and between-territory, and the paper gives no
   way to do it. It is an upper bound on the within-heart figure.
6. **No residual SD is recoverable from any of the scaling-law papers.** Choy & Kassab, Choi 2020 and Taylor 2024
   all report exponents, R² and CIs but **none reports a residual SD, SEE, prediction interval or CV about the
   regression**. Reconstructing one needs the spread of the data, which none publishes. This was attempted and
   abandoned rather than guessed.
7. **Choi 2020's per-vessel Tukey differences could not be interpreted.** Table 4 reports significant LAD/LCx/RCA
   differences for L–M, V–M, D–M, V–L and D–L, with a "Tukey's honest significant differences" column giving
   values such as −0.077 (p = .015 for D–M, LAD vs LCx). **The units of that column are not stated** and cannot
   be inferred with confidence, so it is reported here only as "the scaling law is vessel-dependent", with no
   magnitude attached.
8. **No test–retest of a territory flow *share* exists.** That single design would separate the biological from
   the measurement component in one study, and no such study was found in PET, CMR or invasive physiology.
9. **Nothing was found at the right-tree sub-branch scale.** All sources are at the three-major-vessel scale.
   The 50 right-side trees in the frozen cohort are partitioned at a finer scale, and no figure was found for it.
10. **Cohort transfer.** Keulards and Fournier are near-normal coronary patients; Choy & Kassab are healthy
    pigs; our cohort is ImageCAS-X CT anatomy. Whether territory-share scatter is larger in diseased hearts was
    not established by any source.
11. **⚠️ THE BIGGEST REMAINING GAP: the two Seiler papers could not be read.** These are the classic in-vivo
    calibre→bed-size studies and are the most likely place a published SEE exists:
    - **Seiler C, Kirkeeide RL, Gould KL.** Measurement from arteriograms of regional myocardial bed size distal
      to any point in the coronary vascular tree for assessing anatomic area at risk. *J Am Coll Cardiol.*
      1993;21(3):783–797. doi:10.1016/0735-1097(93)90113-F. PMID 8436762.
    - **Seiler C, Kirkeeide RL, Gould KL.** Basic structure-function relations of the epicardial coronary
      vascular tree. Basis of quantitative coronary arteriography for diffuse coronary artery disease.
      *Circulation.* 1992;85(6):1987–2003. doi:10.1161/01.CIR.85.6.1987. PMID 1591819.

    Both are bronze open access (free at the publisher) but ScienceDirect and ahajournals returned HTTP 403 to
    every automated request; neither is in PMC, Europe PMC, the PMC OA subset or the Wayback Machine as full
    text. **Abstracts only were read**, and neither abstract contains an r, R², SEE or scatter statistic. The
    1992 abstract does give the law verbatim — *"a 2/3 power law relating coronary artery lumen area to distal
    summed branch lengths and regional mass"* (12 patients without CAD, 17 with) — which implies m ∝ D³ and is
    a **third** exponent to set beside 2.66 and 2.39.
    **These two PDFs should open in a normal browser in under a minute** at
    `https://www.sciencedirect.com/science/article/pii/073510979390113F` and
    `https://www.ahajournals.org/doi/10.1161/01.CIR.85.6.1987`. **If a published SEE for the calibre→bed-size
    relation exists anywhere, it is most likely in one of those two figures' captions.** Worth the minute
    before registration.
12. **No within-patient between-territory SD of the coronary volume-to-mass ratio (V/M) exists.** Liu 2022
    (*Exp Biol Med* 2022;247(18):1630–8, doi:10.1177/15353702211027119, PMID 34238054, PMC9597209, full text
    read by the CT-strand agent) is the only paper computing V/M **per vessel** as well as per patient — median
    V/M 25.86, median V_R/M_R 16.35 mm³/g — but **publishes no SD or IQR for the per-vessel figure**, only a
    histogram. Taylor 2017 (*J Cardiovasc Comput Tomogr* 11:429–36, doi:10.1016/j.jcct.2017.08.001) states V/M
    is quantified *"on a patient-level"*; Grover 2017 (doi:10.1016/j.jcct.2017.09.015) gives 30.0 ± 6.5 mm³/g in
    controls, ⚠️ **a between-patient SD (CV ≈ 22 %)**. Had a per-vessel V/M dispersion been published it would
    have been the second independent estimate this document lacks.
13. **Gallinoro's "Variability (%)" formula could not be read.** The Methods sentence defining it ends in a
    rendered formula image that the PMC HTML does not carry as text, so **the exact definition of the 11.89 %
    is unverified**. §4 works around it by deriving 11.89 % independently from the published Bland-Altman SD,
    and the two agree to four significant figures — but if that column turns out *not* to be √2-corrected then
    the subtraction in §3.3 step 2 is too small and the implied `SD_TERRITORY_SHARE` in step 3 is too large.
    **One look at the formula image in the PDF settles it**, and it was not done here.
14. **No within-subject, between-territory CV of MBF in mL/min/g for LAD / LCx / RCA exists in normals, in any
    modality.** This was searched for specifically across PET (¹⁵O-water, ¹³N-ammonia, ⁸²Rb) and CMR and the
    negative result is reported rather than papered over. Chareonthaitawee's 17 ± 10 % is at a **four-wall**
    (septal / anterior / lateral / inferior) scale, which is the closest available. Checked and global-only:
    Lassen 2026 (*Eur J Nucl Med Mol Imaging* 53:6075–84, PMID 42249938, PMC13421257, 277 healthy adults —
    full text read, no regional analysis at all); Schindler 2007; Kajander 2010; Danad 2014 (⚠️ a **patient**
    cohort, not a normal database — its 3.26 ± 1.04 mL/min/g pools subject-to-subject and vessel-to-vessel
    variation in one ±).
15. **`Sunderland JJ, Pan XB, Declerck J, Menda Y.` *J Nucl Cardiol* 2015;22(1):72–84,
    doi:10.1007/s12350-014-9920-6, PMID 25294436 — the one title promising ⁸²Rb normals by vascular territory
    in 49 cardiovascular-normal subjects.** Closed access, no OA copy per Unpaywall/OpenAlex; its companion
    editorial (PMID 25342214) was also unreachable. **Second-highest-value item to fetch through Monash**, after
    the two Seiler papers.
16. **Muehling OM et al., *J Cardiovasc Magn Reson* 2004;6(2):499–507, PMID 15137334 — abstract only**
    (paywalled at Taylor & Francis, not in PMC). Its *"Regional variabilities for resting, hyperemic perfusion,
    and perfusion reserve were 22 ± 8%, 21 ± 10%, and 35 ± 18%"* **reads** as a second within-subject
    between-region figure and matches Chareonthaitawee's format exactly — **but the abstract never defines
    "regional variability", so it is not cited as within-subject anywhere in this document.** Its septal finding
    is in any case directly undercut as coil-shading artefact by Miller 2015 (§6.2).
17. **No paper in any modality formally decomposes MBF variance into between-subject + between-region-
    within-subject + measurement.** Bassingthwaighte 1989 does spatial-vs-methodological, in animals, at
    sub-gram scale; Hoshino 2025's ICC = 0.80 is the closest human equivalent and is MRR in ANOCA patients.
18. **Kaufmann 1999's Table 2 was reconstructed from a column-merged PDF**, not read as a clean table. Two
    search agents reconstructed it independently to identical values and four of five stress cells reconcile
    arithmetically against the printed means — **but the regional RC figures of 41–59 % should have eyes on the
    printed page before they are cited.** The paper is also internally inconsistent on the global hyperaemic RC
    (0.94 in the abstract, 0.90 in Results and Table 2, 0.936 in the Fig. 5 legend).

---

## 11. Sources, with what was actually read

| Source | Reached | Used for |
|---|---|---|
| Keulards 2020, *Heart* 106:1489–94, doi:10.1136/heartjnl-2020-316689, PMC7509389 | **full text (PMC)** | §3, §6 — the primary human measurement |
| Gallinoro 2023, *EuroIntervention* 19:e155–66, doi:10.4244/EIJ-D-22-00772, PMC10242662 | **full text (tables)** | §4 — measurement-error term |
| Fournier 2021, *EuroIntervention* 17:e309–16, doi:10.4244/EIJ-D-20-00684, PMC9724861 | **full text** | §5 — systematic component, population-SD trap |
| Choy & Kassab 2008, *J Appl Physiol* 104:1281–6, doi:10.1152/japplphysiol.01261.2007, PMC2629558 | **full text** | §2 — controlled anchor; `MURRAY_EXP` provenance |
| Choi 2020, *Physiol Rep* 8:e14514, doi:10.14814/phy2.14514, PMC7387886 | **full text (Tables 2–4)** | §8 — human Q–D and D–M exponents |
| Taylor 2024, *Am J Physiol Heart Circ Physiol* 327:H182–90, doi:10.1152/ajpheart.00142.2024, PMC11380967 | **full text (PMC)** | §8 — pooled flow–diameter exponent |
| Wong 2025, *Circ Cardiovasc Interv* 18:e014919, doi:10.1161/CIRCINTERVENTIONS.124.014919, PMID 40233166 | **full text (Table 1)** | §4 — corroboration; no CoV published |
| Johnson & Gould 2024, *EuroIntervention* 20:e1196–8, doi:10.4244/EIJ-E-24-00051, PMC11443250 | **full text (editorial)** | §5.1 — attack on the per-gram numbers |
| Malkasian 2020, *Eur Radiol* 30:3334–45, doi:10.1007/s00330-020-06697-w, PMC7416454 | **full text** (via search agent) | §5.2 — mass-assignment error |
| Stalikas 2025, *J Am Heart Assoc* 14:e039013, doi:10.1161/JAHA.124.039013, PMC12887209 | **full text** (via search agent) | §5.3 — dominance; population-spread trap |
| Murai 2019, *Circ Cardiovasc Interv* 12:e007322, doi:10.1161/CIRCINTERVENTIONS.118.007322, PMID 31518164 | abstract only | §5.4 — per-vessel limits of agreement |
| Liu 2022, *Exp Biol Med* 247:1630–8, doi:10.1177/15353702211027119, PMC9597209 | **full text** (via search agent) | §10 item 12 — per-vessel V/M, no dispersion |
| Seiler 1993, *J Am Coll Cardiol* 21:783–97, doi:10.1016/0735-1097(93)90113-F, PMID 8436762 | **abstract only — 403** | §10 item 11 — open gap |
| Seiler 1992, *Circulation* 85:1987–2003, doi:10.1161/01.CIR.85.6.1987, PMID 1591819 | **abstract only — 403** | §10 item 11 — open gap |
| Chareonthaitawee 2001, *Cardiovasc Res* 50:151–61, doi:10.1016/S0008-6363(01)00202-4, PMID 11282088 | **full text** (green-OA PDF via Wayback) | §5.5 — the PET within-subject figure |
| Kaufmann 1999, *J Nucl Med* 40:1848–56, PMID 10565780 | **full text (PDF)**; Table 2 reconstructed | §5.5 — regional PET measurement error |
| Bassingthwaighte 1989, *Circ Res* 65:578–90, doi:10.1161/01.res.65.3.578, PMC3361973 | **full text** | §5.6 — scale law; the only spatial/methodological split |
| Hoshino 2025, *Eur Heart J Cardiovasc Imaging* 26:1120–7, doi:10.1093/ehjci/jeaf101, PMC12206580 | **full text** | §5.6 — ICC variance split |
| Brown 2023, *Eur Heart J Cardiovasc Imaging* 24:426–34, doi:10.1093/ehjci/jeac231, PMC10029853 | **full text** | §6.1 — CMR systematic replication |
| Kamani 2025, *J Cardiovasc Magn Reson* 27:101927, doi:10.1016/j.jocmr.2025.101927, PMC12445411 | **full text** | §6.1 — CMR systematic replication |
| Brown 2018, *J Cardiovasc Magn Reson* 20:48, doi:10.1186/s12968-018-0462-y, PMC6036695 | **full text** | §6.1 — null at stress |
| Piccinelli 2020, *J Nucl Cardiol* 27:1756–69, doi:10.1007/s12350-018-01472-3, PMC6488439 | **full text** | §6.1 — contradicting ordering |
| Lyu 2022, *Front Cardiovasc Med* 9:817911, PMC8850642 | **full text** | §6.1 — null at territory scale |
| Miller 2015, *J Cardiovasc Magn Reson* 17:11, doi:10.1186/s12968-015-0117-1, PMC4323126 | **full text** | §6.2 — coil-shading artefact |
| Hove 1998, *J Nucl Med* 39:591–8, PMID 9544662 | **full text** | §6.2 — septal spillover bias |
| de Jong 1995, *J Nucl Med* 36:581–5, PMID 7699445 | **full text** | §6.2 — PVE/liver spillover; scale caveat |
| Johnson & Gould 2005, *J Nucl Med* 46:1427–37, PMID 16157524 | **full text** | §5.6 — microsphere-scale warning |

**Provenance note on the two search strands.** §5.2–5.4 and §8's Choi reconstruction come from a CT-strand
search agent; §5.5–5.6 and §6.1–6.2 from a PET/CMR-strand agent. Both were instructed to quote verbatim, to
state full-text-vs-abstract, and to label between- vs within-subject. **The PET-strand agent reported that two
automated page summarisations during its search produced fabricated details — one invented a PMID** (16157540
for Johnson & Gould 2005, which is an unrelated paper; the correct PMID is 16157524) **and one paraphrased
table values as if quoted.** It re-verified everything against raw extracted text, and every DOI and PMID in
this document was independently re-checked here against Europe PMC. **The items still carrying reconstruction
risk are named in §10: Kaufmann's Table 2 (item 18), Choi's residual (§8), the Bassingthwaighte extrapolation
(§5.6), the Hoshino Bland-Altman conversion (§5.6), and Gallinoro's variability formula (item 13).**

**Nothing in this document is cited that was not retrieved.** Where a number is our arithmetic rather than a
published figure it is labelled. Where a claim could not be checked it is in §10 rather than in §9.
