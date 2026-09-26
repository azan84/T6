# Citation search: `VALIDATED_RESIDUAL = 0.10` (ablation.py L54–63; STATISTICS-PLAN §P2)

Date: 2026-09-19. Searcher: literature agent. Status of this document: **evidence gathered and verified**;
it proposes a decision, it does not enact one.

## TL;DR

**Verdict (a): keep `VALIDATED_RESIDUAL = 0.10`. Rewrite the justification. Add a threshold sweep.**

- The literature reports **two** statistics roughly **2.8× apart**, and the code comment does not say which it means.
  As a **within-subject CoV**, "10–15%" is right. As an **agreement bound** — which is how `ablation.py` phrases it
  ("agrees with the measured value to within 10%") — it is **wrong**; the published repeatability coefficient is
  **23% per territory and 27% per segment** for hyperaemic MBF.
- **Yes, per-territory is materially worse than global**, by about 1.5×: the one study measuring all three levels
  on the same subjects gives RC **15% → 23% → 27%** (whole → regional → segmental) and wCV **5.5% → 8.3% → 9.8%**.
  Corroborated in CMR (global 29% → regional 30–37%) and in swine CT (regional RMSE ~4× global).
- **But 0.10 should not move to 0.23.** Our residual compares one *deterministic* model output to one noisy
  measurement — one noise draw, not two — so the RC is √2 too large for our use. The statistically correct 95%
  bound for our comparison is **~0.13–0.16**. 0.10 sits just below it: strict, but not unreasonable.
- **0.10 is the conservative direction for H2** (the headline proportion is monotone non-decreasing in the
  threshold), which is a stronger defence than any citation. Say so, and report 0.05 / 0.10 / 0.15 / 0.23.
- Three fixes to the prose: drop "agrees to within 10%"; drop "CT perfusion" (essentially no human evidence);
  drop "per-territory" wherever the 10–15% figure is cited to a consensus source (that source is unqualified and
  rests on a global study).

## 0. What the constant actually is, in code

`code/ablation.py:282`

```python
resid = float(np.sqrt(np.mean(((pred - q_target) / q_target) ** 2)))
```

The residual is the **root-mean-square RELATIVE deviation across the 2–3 clean-tree territories** between the
tuned model's territory perfusion and the target territory perfusion. It is *not* a max-norm and *not* an
absolute flow difference. **This matters for which literature statistic is the right comparator** (§4).

The justification comment currently reads: *"Test-retest repeatability of quantitative per-territory myocardial
blood flow (CT perfusion / PET MBF) is of order 10-15 %."* That sentence is, as written, **ambiguous between two
different statistics that differ by a factor of ~2.8**, and under one of the two readings it is **wrong**.

---

## 1. Primary sources found and verified

All PubMed metadata below was retrieved through the NCBI E-utilities API (`efetch`, `rettype=abstract`), which
returns the publisher-deposited record; all DOIs were independently confirmed against the Crossref REST API.
Where only an abstract was read, this is stated.

### 1.1 The single most directly on-point source — per-territory AND per-segment, hyperaemic

> Lubberink M, Nordström J, Sigfridsson J, Svanström P, Eggers KM, Sörensen J, Kero T.
> **"Routine clinical reproducibility of hyperemic myocardial blood flow measurements with 15O-water-PET."**
> *European Heart Journal – Cardiovascular Imaging* 2024;25(Supplement_1):jeae142.093.
> DOI: `10.1093/ehjci/jeae142.093` — **verified via Crossref** (title, all 7 authors, container, volume, date
> 2024-06-27 all match).
> **Source read: publisher abstract page (full text; this item IS only an abstract — see the caveat below).**

- Modality/tracer: **15O-water PET**, digital PET-CT, 4-min dynamic rest and stress scans, 400 MBq controlled bolus.
- n = **10 patients**, **same-day test–retest** (repeat ~1 h apart).
- What was repeated: **repeat scans** (true test–retest), hyperaemic MBF.

**Exact reported statistic, verbatim:**

> "RC was 15% (0.43 mL/g/min), 23% (0.67) and 27% (0.80) at whole myocardium, regional and segmental levels,
> respectively. Mean test-retest difference was 7%, 10% and 11%, and wCV was 5.5%, 8.3% and 9.8%, respectively."

Internal consistency check performed by me: 15/5.5 = 2.73, 23/8.3 = 2.77, 27/9.8 = 2.76. So this paper's
**RC = 2.77 × wCV** — the standard Bland–Altman repeatability coefficient. Good; the two statistics are
explicitly and consistently separated in the same sentence.

**Caveats, stated plainly.**
1. This is a **conference abstract in an EHJ-CI supplement, not a full peer-reviewed paper.** I searched PubMed
   for a full-paper version under all three of Lubberink, Kero and Nordström as author, combined with
   repeatability/reproducibility terms, and **found none.** It is citable, but it must be cited as an abstract.
2. n = 10 is small.
3. **The abstract does not define "regional" and "segmental".** The Uppsala group's standard convention (used in
   their other 15O-water papers) is whole LV / **3 coronary artery territories** / **17 AHA segments**, which
   would make "regional" exactly our per-territory case. I could **not** verify that this abstract uses that
   convention — **not verified**, treat as a strong inference only.
4. Rest MBF repeatability is **not reported** in the abstract.

### 1.2 Global hyperaemic, large n, same-day, the clearest CoV-vs-RC contrast in one sentence

> Bober RM, Milani RV, Abelhad NI, Velasco-Gonzalez C, Stewart MH, Morin DP.
> **"Fast vs slow rubidium-82 infusion profiles and test-retest precision of myocardial perfusion using
> contemporary 3D cardiac analog positron emission tomography-computed tomography imaging."**
> *J Nucl Cardiol* 2024;41:102059. DOI `10.1016/j.nuclcard.2024.102059` (Crossref-verified). PMID 39426501.
> **Source read: PubMed abstract only** (paywalled full text).

- Rb-82, modern analog 3D PET-CT, **n = 98** (healthy, clinical, and prior-MI groups), HeartSee software.
- 3 consecutive rest scans and **2 consecutive stress scans, minutes apart** — true same-day test–retest.

**Verbatim:**

> "Fast and slow profiles were associated with similar same-day test-retest precision (COV 11.5% vs 11.3%
> (P = .77); RC 21.5% vs 22.6%, for F-F vs S-S)."

and, from its own Background, the figure our code's comment is probably echoing:

> "On legacy 2D positron emission tomography (PET) systems utilizing a 50 mL/min Rb-82 profile, test-retest
> precision of quantitative perfusion is ∼10%."

This paper is the cleanest demonstration that **"precision ~10%" and "agreement bound ~22%" are the same data
described by two different statistics.** These are **global** numbers.

### 1.3 The source of the "~10%" figure — global, Rb-82, very large scan count

> Kitkungvan D, Johnson NP, Roby AE, Patel MB, Kirkeeide R, Gould KL.
> **"Routine Clinical Quantitative Rest Stress Myocardial Perfusion for Managing Coronary Artery Disease:
> Clinical Relevance of Test-Retest Variability."**
> *JACC Cardiovasc Imaging* 2017;10(5):565–577. DOI `10.1016/j.jcmg.2016.09.019` (Crossref-verified). PMID 28017383.
> **Source read: PubMed abstract only.**

- Rb-82, dipyridamole, **120 volunteers, 708 serial quantitative PET perfusion scans.**

**Verbatim:**

> "Test-retest methodological precision (coefficient of variance) for serial quantitative **global** myocardial
> perfusion minutes apart is ±10% (mean ΔSD at rest ±0.09, at stress ±0.23 cc/min/g) and for days apart is ±21%
> (mean ΔSD at rest ±0.2, at stress ±0.46 cc/min/g) reflecting added biological variability."

Note three things: the statistic is a **coefficient of variance**, the level is explicitly **global**, and the
**same study's day-apart figure is ±21%**, i.e. *biological* variability roughly doubles it even at the global level.

### 1.4 Per-territory (ischaemic vs remote), repeatability coefficient, human, CAD patients

> Jagathesan R, Kaufmann PA, Rosen SD, Rimoldi OE, Turkeimer F, Foale R, Camici PG.
> **"Assessment of the long-term reproducibility of baseline and dobutamine-induced myocardial blood flow in
> patients with stable coronary artery disease."** *J Nucl Med* 2005;46(2):212–219. PMID 15695778.
> (No DOI in the PubMed record — JNM of this vintage; **not verified** that a DOI exists.)
> **Source read: PubMed abstract only.**

- 15O-water PET, **n = 15** CAD patients (>70% stenosis), repeat at **24 weeks** (long-term, not same-day),
  **dobutamine** stress (not adenosine/dipyridamole).
- Territories: whole LV, **Isc** (region subtended by the most severe stenosis) and **Rem** (remote myocardium) —
  i.e. an explicitly **per-territory** analysis of the same kind we use.

**Verbatim:**

> "The BA repeatability coefficients (and %BA) for MBF in ischemic and remote territories were 0.3 (28%) and
> 0.26 (24%) at rest and 0.49 (27%) and 0.58 (26%) during Dob stress."

So **per-territory RC during stress = 26–27%**, converging with Lubberink's 23% regional / 27% segmental despite
a different tracer protocol and a 24-week rather than same-hour interval.

### 1.5 Global hyperaemic RC, the classic same-session study

> Kaufmann PA, Gnecchi-Ruscone T, Yap JT, Rimoldi O, Camici PG.
> **"Assessment of the reproducibility of baseline and hyperemic myocardial blood flow measurements with
> 15O-labeled water and PET."** *J Nucl Med* 1999;40(11):1848–1856. PMID 10565780.
> **Source read: PubMed abstract only.**

- 15O-water, **n = 21 healthy men**, two baseline+adenosine measurements **within 1 h**.

**Verbatim:**

> "There was no significant difference between the two baselines (0.89 +/- 0.14 versus 0.99 +/- 0.15 mL/min/g,
> mean difference 13% +/- 11%) or between the two hyperemic MBFs (3.51 +/- 0.45 versus 3.83 +/- 0.49 mL/min/g,
> mean difference 10% +/- 14%) ... The repeatability coefficient for MBF was 0.17 mL/min/g at baseline and
> 0.94 mL/min/g during hyperemia."

My arithmetic (not the paper's): 0.94 / 3.67 (mean of the two group means) = **25.6% relative RC** at hyperaemia,
against a "mean difference" of 10% ± 14%. Again the same factor-of-~2.5 gap between the two statistics, **in a
paper that reports both**. This is very likely one of the papers behind the loose "10–15%" folklore.

### 1.6 Global hyperaemic, Rb-82, same-day

> Manabe O, Yoshinaga K, Katoh C, Naya M, deKemp RA, Tamaki N.
> **"Repeatability of Rest and Hyperemic Myocardial Blood Flow Measurements with 82Rb Dynamic PET."**
> *J Nucl Med* 2009;50(1):68–71. DOI `10.2967/jnumed.108.055673` (Crossref-verified). PMID 19091892.
> **Source read: publisher abstract page + PubMed record.**

- n = 15 healthy volunteers, repeat at 60 min.
- Rest MBF mean difference 6.18% ± 12.22%; **hyperaemic MBF mean difference 1.17% ± 13.64%**;
  **repeatability coefficients 0.19 mL/min/g (rest) and 0.92 mL/min/g (hyperaemia)**.
- 0.92 / 3.37 = **27% relative RC** at hyperaemia (my arithmetic). The abstract reports whole-myocardium values
  only and gives no regional breakdown; whether the full text contains one is **not verified**.

### 1.7 Recent, patient population, ~3-week interval, reports CV *and* RC *and* ICC

> Seidelin L, Prescott E, Fischer M, Haahr R, Hovind P, Rauf M, Krakauer M.
> **"Intra-Individual Variability of Myocardial Blood Flow and Flow Reserve Assessed by [15O]H2O-PET in Patients
> with Angina and No Obstructive Coronary Disease."** *Diagnostics (Basel)* 2026;16(13):1975.
> DOI `10.3390/diagnostics16131975` (Crossref-verified). PMID 42449757. PMCID PMC13360267.
> **Source read: PubMed abstract only** (open access full text exists and was not read).

**Verbatim:**

> "Hyperaemic MBF averaged 3.06 ± 0.9 vs. 2.97 ± 0.78 mL/min/g (r = 0.83; RC 0.98 mL/min/g; CV 11.6%; ICC 0.81).
> MFR showed only moderate reproducibility (3.47 ± 1.23 vs. 3.23 ± 0.92; RC 1.90; CV 21%; ICC 0.60)."

n = 21, median interval 21 days. 0.98 / 3.015 = **32.5% relative RC**; 2.77 × 11.6% = 32.1% — confirming
RC = 2.77 × CV here too. **A CV of 11.6% and an agreement bound of 32% are the same finding.**

### 1.8 Regional variability is worse — the oldest explicit statement

> Sawada S, Muzik O, Beanlands RS, Wolfe E, Hutchins GD, Schwaiger M.
> **"Interobserver and interstudy variability of myocardial blood flow and flow-reserve measurements with
> nitrogen 13 ammonia-labeled positron emission tomography."** *J Nucl Cardiol* 1995;2(5):413–422.
> DOI `10.1016/s1071-3581(05)80029-7` (Crossref-verified). PMID 9420821.
> **Source read: PubMed abstract only.**

- 13N-ammonia, rest + adenosine, **6 normals + 6 stable CAD**, MBF in **5 myocardial regions**.

**Verbatim:**

> "For individual myocardial regions, there was considerable interstudy variability of stress MBF and CFR, with a
> mean percent difference for CFR of 19% +/- 19% in normal volunteers and 38% +/- 16% in patients with coronary
> disease."
> "The temporal reproducibility of MBF and CFR was fair, with individual regions demonstrating substantial
> interstudy variability."

n is tiny and the CFR figure is not MBF, but the **direction** is unambiguous and is the earliest clear statement
of it.

### 1.9 Also checked, and deliberately NOT used

| Source | Why not used |
|---|---|
| Nagamachi S, Czernin J, Kim AS, Sun KT, Böttcher M, Phelps ME, Schelbert HR. *J Nucl Med* 1996;37(10):1626–31. PMID 8862296. "Reproducibility of measurements of regional resting and hyperemic myocardial blood flow assessed with PET." | Real test–retest (13N-ammonia; n=21 rest, 15 adenosine, 7 dipyridamole). Reports **"Baseline and follow-up hyperemic myocardial blood flow did not differ (11.8% +/- 9.4%)"** — but that is a **mean absolute percent difference**, not a CoV and not an RC, and the abstract does not report the level (global vs regional) for that figure despite "regional" in the title. Usable as supporting, **not** as the anchor. |
| Knešaurek K, Machac J, Zhang Z. *BMC Med Phys* 2009;9:2. PMID 19178700. "Repeatability of regional myocardial blood flow calculation in 82Rb PET imaging." Reports per-sector RC "0.056 (8.5%)" rest and "0.089 (6.3%)" stress. | **TRAP. This is not test–retest.** Verbatim from the paper: *"The same set of images was analyzed twice in order to investigate repeatability of the analysis."* It is **re-processing repeatability of a single scan**. Citing its 6.3% stress figure to justify a 10% threshold would be a serious error — it excludes every source of variance our residual has to tolerate. |
| Chareonthaitawee P et al. *J Nucl Med* 2006;47(7):1193–1201. PMID 16818955. | **Swine**, and **resting MBF only**. Regional RC 0.09–0.43 (H215O) and 0.09–0.18 (13NH3) mL/min/g. Not human, not hyperaemic. |
| Efseaff M, Klein R, Ziadi MC, Beanlands RS, deKemp RA. *J Nucl Cardiol* 2012;19(5):997–1006. DOI `10.1007/s12350-012-9600-3`. PMID 22826134. | Genuine same-day test–retest (n=27 CAD + 9 healthy) but **resting, whole-LV only**: "The best repeatability coefficient for same-day MBF was 0.20 mL/minute/g". ~20% relative at rest. Supporting only. |
| Ocneanu AF, deKemp RA, Renaud JM et al. *Comput Math Methods Med* 2017;2017:6810626. PMCID PMC5331165. | Same-day Rb-82 test–retest (n=12) but reports a **non-standard nonparametric RC** — verbatim, *"RPCnp = 1.45 × interquartile range"* — over **pooled rest and stress**: "RPCnp = 0.21 mL/min/g (15.8%)". Different statistic, pooled state; not comparable. Useful only as a warning that "RC" is not defined identically across this literature. |
| Sunderland JJ et al.; Dunet V et al.; deKemp RA et al. (multisoftware); Monroy-Gonzalez AG et al. | **Software/inter-package reproducibility**, not test–retest. Same trap as Knešaurek. |

---

## 2. Consensus, guideline and review statements

### 2.1 ASNC / SNMMI information statement — explicit on the global-vs-regional point

> Bateman TM, Heller GV, Beanlands R, Calnon DA, Case J, deKemp R, DePuey EG, Di Carli M, Guler EC, Murthy VL,
> Rosenblatt J, Sher R, Slomka P, Ruddy TD.
> **"Practical Guide for Interpreting and Reporting Cardiac PET Measurements of Myocardial Blood Flow: An
> Information Statement from the American Society of Nuclear Cardiology, and the Society of Nuclear Medicine and
> Molecular Imaging."** *J Nucl Med* 2021;62(11):1599–1615. DOI `10.2967/jnumed.121.261989`. PMID 33789935.
> PMCID **PMC8612323**. (Dual-published: *J Nucl Cardiol* 2021;28(2):768–787, DOI `10.1007/s12350-021-02552-7`,
> PMID 33786730.)
> **Source read: PMC full text (open access), retrieved and searched directly.**

**Verbatim:**

> "Interrogation of the individual segments in the vascular distribution will provide more specific information
> about vessel branches (Figure 5). **However, precision of MBF measurement decreases with smaller segments due
> to more statistical noise. Care must be taken to avoid over-interpretation of small reductions in MBF in small
> regions.**"

This is the consensus-level statement that **regional/segmental precision is worse than global** — qualitative,
but from the field's own joint information statement, and exactly the direction the numbers in §1 show.

### 2.2 EANM procedural guidelines — a useful NEGATIVE finding

> Sciagrà R, Lubberink M, Hyafil F, Saraste A, Slart RHJA, Agostini D, Nappi C, Georgoulias P, Bucerius J,
> Rischpler C, Verberne HJ; Cardiovascular Committee of the EANM.
> **"EANM procedural guidelines for PET/CT quantitative myocardial perfusion imaging."**
> *Eur J Nucl Med Mol Imaging* 2021;48(4):1040–1069. DOI `10.1007/s00259-020-05046-9` (Crossref-verified).
> PMID 33135093. PMCID PMC7603916.
> **Source read: PMC full text, retrieved and searched directly for every instance of
> repeat*/reproducib*/test-retest/variabilit*.**

**Finding: the EANM guideline does not state a numeric test–retest repeatability figure for MBF.** Every
"reproducibility" passage in it concerns **model and software reproducibility** (e.g. the Lortie one-tissue
compartment model across software platforms), not repeat-scan repeatability. Do not cite it for a number.

---

## 2A. CT myocardial perfusion — the half of the code comment that has almost no evidence behind it

The comment in `ablation.py` says "(CT perfusion / PET MBF)". **The CT half of that parenthesis is not supported
by a comparable body of evidence and should be dropped or heavily qualified.**

### 2A.1 The only human test–retest repeat-scan study of quantitative dynamic CTP MBF

> Hasegawa D, Nakamura S, Takafuji M, Sakuma H, Kitagawa K.
> **"Test-retest reproducibility of absolute myocardial blood flow obtained using stress dynamic CT myocardial
> perfusion imaging."** *Int J Cardiol Heart Vasc* 2024;55:101510.
> DOI `10.1016/j.ijcha.2024.101510` (Crossref-verified). PMID 39324034. PMCID **PMC11421242**.
> **Source read: PMC full text, retrieved and searched directly by me.**

- **n = 30**, retrospective, suspected/known CAD, Siemens syngo VPCT Body, 16 AHA segments, units mL/100 mL/min.
- **Stress only** (ATP 200 µg/kg/min); two separate dynamic CTMPI acquisitions.
- The paper's own claim: *"To the best of our knowledge, this is the first study to examine the reproducibility
  of MBF values quantified with dynamic CTMPI."*

**The disqualifying caveat, verified by me in the PMC full text, verbatim:**

> "The median interval between the two tests was 795 days (interquartile range, 543 to 1068 days)."

That is **not** test–retest precision in any sense useful to us. It is two years of biology, therapy and scanner
drift bundled together. The authors say so themselves in their limitations.

**Exact statistics, verbatim from the full text:**

> "ICC was 0.94 (95 % CI: 0.87–0.97), 0.93 (95 % CI: 0.86–0.97), and 0.90 (95 % CI: 0.89–0.91) between global
> 1st and 2nd global MBFs, between 1st and 2nd remote MBFs, and between 1st and 2nd MBFs in all segments.
> Bland-Altman plots showed a mean difference of –0.7 mL/100 mL/min (95 % limits of agreement [LoA], –35.3 to
> 36.7 mL/100 mL/min) between 1st and 2nd global MBFs, of –1.3 mL/100 mL/min (95 % LoA, –42.4 to 45.0
> mL/100 mL/min) between 1st and 2nd remote MBFs and of 0.7 mL/100 mL/min (95 % LoA, –48.6 to 50.0
> mL/100 mL/min) between 1st and 2nd MBFs in all segments."

Note: "global" here is the **mean** of all segments and "remote" the **maximum** of all segments — not an
anatomical territory. **The paper reports no CV% and no repeatability coefficient.** A 95% LoA half-width *is*
numerically the repeatability coefficient, so (my arithmetic, not theirs, on a global mean of ~139
mL/100 mL/min): **global ≈ ±26%, segment level ≈ ±35%.** Same ordering as PET, slightly worse, hugely confounded.

### 2A.2 The only short-interval repeat-scan CT data are porcine

> Hadjiabdolhamid N, Zhao Y, Hubbard L, Molloi S.
> **"Reproducibility of a single-volume dynamic CT myocardial blood flow measurement technique: validation in a
> swine model."** *Eur Radiol Exp* 2024;8(1):91. DOI `10.1186/s41747-024-00498-2` (Crossref-verified). PMID 39143412.
> **Source read: PMC full text (PMC11324639) by the assisting agent; PubMed record verified by me.**

- **Swine (n = 13), not human.** 34 paired measurements, **10-minute delay between pairs**, rest and adenosine.
- Also a **single-volume** technique, not conventional multi-phase dynamic CTP.
- Global: `RMSE = 0.08 mL/min/g`. **All vessel-specific territories:** *"linearly related by
  PReg2 = 0.86PReg1 + 0.13 with a Spearman correlation (ρ) of 0.87, a RMSE of 0.31 mL/min/g and a RMSD of
  0.29 mL/min/g"*. Per-territory RMSE is **~4× the global RMSE** — the same global→regional penalty again.
- Authors' own limitation: *"our study used healthy swine subjects"* and *"several of the animals did not achieve
  an adequate response to adenosine"* — so the "stress" arm is only partly hyperaemic.

### 2A.3 What everything else cited as "CT MBF is reproducible" actually is

The assisting agent read in full **Nieman & Balla 2020** (*J Cardiovasc Comput Tomogr* 14(4):303–306, DOI
`10.1016/j.jcct.2019.09.003`, PMID 31540820), **Sliwicka et al. 2023** (*Eur Radiol*, DOI
`10.1007/s00330-023-09550-y`, PMID 36997751), **Kato et al. 2026** (*Front Radiol*, DOI
`10.3389/fradi.2026.1760241`), and **Nous et al. 2022 SPECIFIC** (*JACC Cardiovasc Imaging* 15(1):75–87, DOI
`10.1016/j.jcmg.2021.07.021`, PMID 34538630) — **none contains a CT MBF test–retest repeatability statistic.**
The commonly repeated "ICC > 0.9" traces to **Pan et al., *Korean J Radiol* 2019;20(5):709–718**
(DOI `10.3348/kjr.2018.0729`, PMID 30993922), which is **same-scan inter-observer reanalysis at rest**, reported
only as the inequality *"ICC > 0.9 for all parameters"* with no per-parameter values and no CIs.

**The reason for the gap is structural and worth stating in the paper:** dynamic CTP costs roughly 5–13 mSv plus
a contrast bolus per acquisition (Sliwicka 2023, verbatim: *"a mean effective dose of 9.2 mSv (range of
4.6–12.8 mSv)"*), so a deliberate same-day repeat in humans is hard to justify to an ethics committee.

### 2A.4 A useful bracketing comparator from CMR (clearly labelled: not CT, not PET)

> Brown LAE et al. **"Fully automated, inline quantification of myocardial blood flow with cardiovascular magnetic
> resonance: repeatability of measurements in healthy subjects."** *J Cardiovasc Magn Reson* 2018;20:48.
> DOI `10.1186/s12968-018-0462-y` (Crossref-verified). PMID 29983119. PMCID PMC6036695.
> **Source read: PMC full text, retrieved and searched directly by me.**

n = 42 healthy; **15-min intrastudy repeat** and ≥7-day interstudy repeat; global and **regional (coronary
territories and slices)**. Verbatim:

> "There was no significant difference in intrastudy repeated global rest MBF (0.65 ± 0.13 ml/g/min vs
> 0.62 ± 0.12 ml/g/min, p = 0.24, repeatability coefficient (RC) = 24%) or stress (2.89 ± 0.56 ml/g/min vs
> 2.83 ± 0.64 ml/g/min, p = 0.41, **RC = 29%**) MBF."
> "**Regional repeatability was good for stress (RC = 30–37%)** and rest MBF (RC = 32–36%) but poorer for MPR
> (RC = 35–43%). **Within subject coefficient of variation was 8% for rest and 11% for stress within the same
> study**, and 11% for rest and 12% for stress between studies."
> "Fully automated, inline, myocardial perfusion mapping by CMR shows good repeatability **that is similar to the
> published PET literature**."

This is the single cleanest corroboration of the whole argument, in an open-access full text I read myself:
**the same study, same data, reports wsCV = 11% for stress and RC = 29% global / 30–37% regional.** Both the
factor-of-~2.8 gap and the global→regional penalty, in one paper, with the authors themselves noting the
agreement with PET. This is what a properly designed short-interval *regional* repeatability study looks like,
and the CT equivalent does not exist.

**Action for the code comment: drop "CT perfusion" from the justification, or keep it only as
"(and, with far weaker evidence, CT perfusion)".**


---

## 2B. The likely actual source of the "10–15%" in our code comment — and it is a CoV

### 2B.1 JACC: Cardiovascular Imaging Expert Panel Statement

> Schindler TH, Fearon WF, Pelletier-Galarneau M, Ambrosio G, Sechtem U, Ruddy TD, Patel KK, Bhatt DL,
> Bateman TM, Gewirtz H, Shirani J, Knuuti J, Gropler RJ, Chareonthaitawee P, Slart RHJA, Windecker S,
> Kaufmann PA, Abraham MR, Taqueti VR, Ford TJ, Camici PG, Schelbert HR, Dilsizian V.
> **"Myocardial Perfusion PET for the Detection and Reporting of Coronary Microvascular Dysfunction:
> A JACC: Cardiovascular Imaging Expert Panel Statement."** *JACC Cardiovasc Imaging* 2023;16(4):536–548.
> DOI `10.1016/j.jcmg.2022.12.015` (Crossref-verified). PMID 36881418 (E-utilities-verified: authors, journal,
> volume, pages, date all match).
> **Source: section "PET MBF and MFR: Validation, Reproducibility, and Thresholds".** jacc.org and ScienceDirect
> both return **HTTP 403** to direct fetching — I confirmed this myself. The body text was obtained by the
> assisting agent through a text-extraction proxy of the publisher HTML, and the substance of the key sentence
> was **independently corroborated** by a search-engine index snippet I retrieved separately.
> **Re-check against the published PDF before quoting it in the manuscript.**

**Verbatim (provenance as caveated above):**

> "Repeatability coefficient of resting MBF is approximately 0.20 mL/min/g for both 82Rb and 13N-NH3. Reported
> repeatability of hyperemic MBF measurements is similar for the common pharmacologic stress agents—adenosine,
> dipyridamole, and dobutamine—with improved repeatability when applying correction for hyperemic rate-pressure
> product. **Repeatability studies of hyperemic MBF with dipyridamole reported coefficients of variation (CoV) of
> ∼10% for same day measurements and CoV of 15% to 20% for different day measurements.**"

**This is almost certainly where our "of order 10-15 %" comes from, whether directly or at second hand.** Note
exactly what it says and does not say:

- The ~10% and 15–20% figures are **coefficients of variation**, named as such, *not* agreement bounds.
- The 10% is **same-day**; the 15–20% is **different-day** — so "10–15%" is a conflation of two different
  quantities (methodological precision vs methodological + biological variability). It is not a range for one thing.
- **Global vs regional is not stated.** The wording is unqualified. **Do not assert it is global** — but its cited
  support is Kitkungvan 2017 (§1.3), which *is* explicitly global, so a per-territory reading is unsupported.
- The RC sentence (0.20 mL/min/g) is **rest**, not hyperaemic. Quoting "RC ≈ 0.20" alongside a hyperaemic
  application would be a second error.

**Documented citation discrepancy, found by the assisting agent and worth knowing:** this passage cites the
Murthy 2018 position paper (ref 29) as support, and the Murthy 2018 paper **does not contain these numbers**
(§2B.2). So the chain of provenance for "10–15%" is weaker than it looks. One more reason not to rest the
constant on it.

### 2B.2 SNMMI/ASNC Joint Position Paper — a second important NEGATIVE finding

> Murthy VL, Bateman TM, Beanlands RS, et al.
> **"Clinical Quantification of Myocardial Blood Flow Using PET: Joint Position Paper of the SNMMI
> Cardiovascular Council and the ASNC."** *J Nucl Med* 2018;59(2):273–293. DOI `10.2967/jnumed.117.201368`
> (Crossref-verified). PMID 29242396. Co-published *J Nucl Cardiol* 2018;25(1):269–297,
> DOI `10.1007/s12350-017-1110-x`.
> **Source read: full text PDF (`jnm.snmjournals.org/content/jnumed/59/2/273.full.pdf`), downloaded and grepped
> exhaustively by the assisting agent.**

**Finding: no numeric test–retest repeatability figure, and no threshold for a meaningful change in MBF,
anywhere in the document.** Its Tables 3 and 4 are **normal reference ranges (mean ± SD), not repeatability** —
a table it would be very easy to misread as repeatability. Its only repeatability content is qualitative, e.g.:

> "The shape of the blood input function should also be standardized as much as possible (e.g., 30-s square
> wave), as variations in tracer injection profile have been shown to adversely affect MBF accuracy and
> test–retest repeatability, in particular when using the simplified retention model."

**Do not cite the position paper for a number. It has none.**

### 2B.3 Moody et al. 2015 — could not be reached

> Moody JB, Lee BC, Corbett JR, Ficaro EP, Murthy VL. **"Precision and accuracy of clinical quantification of
> myocardial blood flow by dynamic PET: A technical perspective."** *J Nucl Cardiol* 2015;22(5):935–951.
> DOI `10.1007/s12350-015-0100-0` (Crossref-verified). PMID 25868451.

Existence and metadata verified. **Full text NOT reached** — Unpaywall `is_oa: false`, no PMC copy, Springer and
ScienceDirect serve abstract only / 403. Whether it tabulates test–retest repeatability figures is
**not verified**, and nothing is attributed to it here. If the operator has institutional access, this is the one
source most likely to contain a ready-made table of the primary figures, and is worth 10 minutes of a library login.

### 2B.4 No systematic review exists

Structured PubMed searches with `systematic review[pt]` / `meta-analysis[pt]` filters over
`(myocardial blood flow OR myocardial flow reserve) AND (repeatability OR test-retest) AND PET` return
**zero records**, run independently by me and by the assisting agent. The nearest thing is a **narrative** review:
Gould KL et al., *Curr Cardiol Rep* 2021;23:12, DOI `10.1007/s11886-021-01449-8`, PMID 33483794 — abstract only
read, and the abstract carries no repeatability number.

**So: there is no systematic review to cite. The answer to brief item 2 is that the best available
summary-level sources are §2.1 (ASNC/SNMMI, qualitative on the regional point) and §2B.1 (JACC panel, numeric but
a CoV, rest-vs-stress mixed, and citing a paper that does not contain its numbers).**


---

## 3. Does the literature support ~10–15% for per-territory hyperaemic MBF?

**Partly, and only under one reading. The honest answer is that the field reports two numbers, ~2.8× apart,
and the code's comment does not say which one it means.**

Per-territory / per-segment **hyperaemic** MBF, test–retest:

| statistic | value (per-territory / segmental) | value (global) | sources |
|---|---|---|---|
| within-subject CoV (wCV) | **8.3% regional, 9.8% segmental** | 5.5% (same study); ~10–11.6% elsewhere | §1.1; §1.2, §1.3, §1.7 |
| mean test–retest difference | **10% regional, 11% segmental** | 7% (same study); 10±14%; 1.2±13.6% | §1.1, §1.5, §1.6 |
| **repeatability coefficient (RC)** | **23% regional, 27% segmental; 26–27% per-territory at stress** | 15%; 21.5–22.6%; 25.6%; 27%; 32.5% | §1.1, §1.4; §1.2, §1.5, §1.6, §1.7 |
| *(CMR comparator, same pattern)* | *RC 30–37% regional stress; wsCV 11%* | *RC 29% global stress* | *§2A.4* |
| *(CT comparator — weak)* | *~±35% segment-level LoA, 795-day interval* | *~±26%* | *§2A.1* |

**Conclusions:**

0. **We have probably located the exact source of the code comment, and it says something narrower than we wrote.**
   The JACC Expert Panel statement (§2B.1) says: *"Repeatability studies of hyperemic MBF with dipyridamole
   reported coefficients of variation (CoV) of ∼10% for same day measurements and CoV of 15% to 20% for different
   day measurements."* So "10–15%" is (i) a **CoV**, (ii) a splice of a **same-day** number and a **different-day**
   number rather than a range for one quantity, and (iii) **not qualified as per-territory** — its cited support is
   an explicitly global study. Our comment says "per-territory"; the source does not.
1. **"10–15%" is defensible as a within-subject CoV / mean test–retest difference for per-territory hyperaemic
   MBF.** The best per-territory numbers are wCV 8.3% and mean difference 10% (§1.1), with global same-day CoVs of
   ~10–11.5% (§1.2, §1.3). So the *magnitude* in the code comment is in the right place — but only for that statistic.
2. **"10–15%" is NOT defensible as an agreement bound.** The 95% repeatability coefficient for per-territory
   hyperaemic MBF is **~23–27%**, consistently, across four independent groups, two tracers and intervals from
   one hour to 24 weeks (§1.1, §1.4, §1.5, §1.6, §1.7). *"Agrees with the measured value to within 10%"* — the
   phrasing currently in `ablation.py` — is therefore **not** what this literature says.
   (But see §4: the RC is the bound between *two* noisy measurements, and our model output is not noisy, so the
   RC is √2 too large for our specific comparison. The right upper bound for us is ~0.13–0.16, not 0.23.)
3. **Per-territory repeatability IS materially worse than global, and by a known amount.** The one study that
   measures all three levels on the same subjects gives RC **15% → 23% → 27%** and wCV **5.5% → 8.3% → 9.8%**
   going whole-myocardium → regional → segmental (§1.1). Jagathesan's per-territory stress RC of 26–27% (§1.4) sits
   exactly where that predicts. The ASNC/SNMMI information statement says the same thing in words (§2.1).
   **So yes — the plausible worry in the brief is correct, and it is roughly a 1.5× penalty from global to
   per-territory.** Anyone who quotes Kitkungvan's ±10% for a per-territory application is quoting a global number.
4. **Biological variability roughly doubles the methodological figure.** Kitkungvan: ±10% minutes apart, **±21%**
   days apart (§1.3). Our targets are notionally a single measurement, so the same-session figure is the right one
   — but this bounds how much a "validated" model could ever be expected to track a patient.
5. **The pattern is modality-independent.** CMR gives wsCV 11% stress / RC 29% global / RC 30–37% regional
   (§2A.4), and its authors say this is "similar to the published PET literature". CT is consistent in ordering
   but the only human data has a 795-day inter-scan interval (§2A.1). So the conclusion is not an artefact of one
   tracer, one group or one statistic package.
6. **"CT perfusion" does not belong in the justification as an equal partner to PET.** There is essentially one
   human test–retest CTP MBF paper, it is not short-interval, and it reports no CV and no RC (§2A).

---

## 4. The distinction we are eliding, stated precisely

`VALIDATED_RESIDUAL` is compared against an **RMS relative deviation over 2–3 territories** (§0), computed
between **one** model prediction and **one** target value.

- A **within-subject coefficient of variation** is the relative SD of a *single* measurement about the subject's
  true value. An RMS-over-territories relative deviation is the direct analogue of this. **This is the right
  comparator for our residual.**
- A **repeatability coefficient** is `2.77 × within-subject SD` (equivalently `1.96 × SD of paired differences`)
  and is the **95% bound on the difference between two independent measurements**. It is larger than the wCV by
  2.77×, and larger than the *single*-measurement 95% bound by √2. This is the right statistic for *"would a
  clinician call this change real?"* — it is **not** the right statistic for *"how far off is one prediction,
  typically?"*.

**There is a second, subtler factor of √2 that cuts the other way, and we should not get it wrong either.**
An RC is the 95% bound on the difference between **two noisy measurements**, so it carries `√2` for the two
noise draws. Our comparison is between **one deterministic model output** and **one noisy measurement** — only
one noise draw. So the correct 95% single-territory bound is `1.96 × wsSD`, **not** `2.77 × wsSD`. Taking the
literature RC at face value therefore *overstates* the tolerance our residual needs by √2.

Putting both corrections together (my arithmetic, per-territory σ = 8.3% from §1.1, and the residual being an RMS
over k territories which further shrinks the tail):

| interpretation | per-territory σ = 8.3% | σ = 9.8% (segmental) |
|---|---|---|
| typical deviation (1 wsSD) | 8.3% | 9.8% |
| **95th percentile of the RMS residual of a perfectly correct model, k = 3** | **13.4%** | 15.8% |
| same, k = 2 | 14.4% | 17.0% |
| same, k = 1 (= 1.96 σ) | 16.3% | 19.2% |
| literature repeatability coefficient (2.77 σ) — the number a reviewer will quote | 23% | 27% |

So the *statistically correct* upper bound for our use is around **0.13–0.16**, not 0.23 and not 0.10. `0.10` sits
just below it and is therefore **strict but not unreasonably so**; `0.23` is genuinely too loose for our
comparison because it double-counts measurement noise.

Three further consequences we must not get wrong:

- **A 10% CoV is not a 10% agreement bound.** Under a wCV of 8.3% per territory, ~32% of single territories will
  deviate by more than 8.3%, and the 95% single-measurement interval is ±16%. The code comment's phrase
  "agrees with the measured value to within 10%" is a 95%-agreement claim being supported by a 1-SD statistic.
- **"RC" is not defined identically across this literature.** Bateman/Kaufmann/Lubberink/Seidelin use Bland–Altman
  `2.77 × wsSD`; Bober's RC ≈ `1.96 × SD(differences)`; Ocneanu uses `1.45 × IQR`. Quote the definition with the
  number, always.
- **Directionality of the detector's noise injection.** `DETECTOR-SPEC` §5 requires injecting "target measurement
  noise at the test–retest SD" into the negative class. That must be the **within-subject SD (~8–10% per
  territory)**, *not* the RC (~23%). If we inject 23% noise we make the negatives absurdly easy and the AUC is
  meaningless; if we inject the RC into the noise model *and* keep a 10% threshold we make the positives
  unreachable. **Threshold and injected noise must be derived from the same statistic.**

---

## 5. RECOMMENDATION

**Verdict: (a) with a mandatory rewrite of the justification — the VALUE 0.10 stands, the STATED REASON does not.**

In one sentence: *the literature supports ~8–12% as a within-subject coefficient of variation for per-territory
hyperaemic MBF, which is what our RMS relative residual should be compared against, but it supports ~23–27% as
the repeatability coefficient, and the code's phrase "agrees to within 10%" is the second claim resting on the
first statistic.* Keep 0.10; stop calling it an agreement bound; add a threshold sweep. Specifically:

### 5.1 Keep `VALIDATED_RESIDUAL = 0.10`, but change *why*

Keep the value. Replace the justification. The defensible statement is:

> The residual is an RMS relative deviation across territories, so its natural comparator is the **within-subject
> coefficient of variation** of repeat per-territory hyperaemic MBF measurement, which is **8.3% at the
> vascular-territory level and 9.8% at the segment level** for same-day 15O-water PET test–retest
> (Lubberink et al., EHJ-CI 2024;25(Suppl 1):jeae142.093, doi:10.1093/ehjci/jeae142.093 — conference abstract),
> and ~10–11.5% globally for same-day Rb-82 (Kitkungvan et al., JACC Cardiovasc Imaging 2017;10:565–77,
> doi:10.1016/j.jcmg.2016.09.019; Bober et al., J Nucl Cardiol 2024;41:102059, doi:10.1016/j.nuclcard.2024.102059).
> The same pattern holds in CMR, where one study reports a within-subject CV of 11% for stress MBF alongside
> a regional repeatability coefficient of 30–37% (Brown et al., J Cardiovasc Magn Reson 2018;20:48,
> doi:10.1186/s12968-018-0462-y). `VALIDATED_RESIDUAL = 0.10` is therefore approximately **one within-subject SD**
> of the measurement the model is being validated against.

Also **remove "CT perfusion" from the parenthesis** (§2A): the human CT evidence is a single n=30 study with a
median 795-day inter-scan interval and no CV or RC reported. Say "PET MBF" and, if CT must be mentioned, say so
as an explicit gap.

And **remove the word "per-territory" from any sentence that cites the 10–15% figure to a consensus source**:
the consensus sentence that carries that number (§2B.1) is unqualified and rests on a global study. Per-territory
numbers must be cited to §1.1 or §1.4, not to the panel statement.

**Delete the phrase "agrees with the measured value to within 10%"** wherever it appears
(`ablation.py` L55–57, `STATISTICS-PLAN` §P2, `DETECTOR-SPEC` §5), because the 95% agreement bound is ~23%, not 10%.
Replace with "agrees to within about one within-subject SD of the measurement".

### 5.2 Say out loud that 0.10 is the CONSERVATIVE choice, and prove it

The headline is *P(passes check AND materially wrong)*. As the threshold rises the passing set grows
monotonically, so that proportion is **monotone non-decreasing in `VALIDATED_RESIDUAL`.** A threshold of 0.10 is
therefore **strictly conservative for H2**: any absorption demonstrated at 0.10 is a *lower bound* on the
absorption that would be demonstrated at the literature's agreement bound. That is a much stronger position to
defend at review than "0.10 is the repeatability figure", and it survives a reviewer who disagrees with the
number. **Say it in the paper.**

### 5.3 Add a pre-specified sensitivity sweep over the threshold — four values, not one

Re-run the P2 headline at, and report all of:

| value | what it is | role |
|---|---|---|
| **0.05** | ~0.6 × per-territory wsSD | strict end; shows the trend is monotone, not an artefact |
| **0.10** | ≈1.2 × per-territory wsSD; 77% pass rate for a correct-but-noisy model | **primary, pre-registered** |
| **0.15** | ≈ the 95th percentile of a perfectly correct model's residual (§4) | the statistically correct upper bound for *our* comparison |
| **0.23** | the published per-territory hyperaemic **repeatability coefficient** (§1.1, corroborated at 26–27% by §1.4) | the number a reviewer will quote at us; the permissive bracket |

Present as: *"the proportion that pass and are materially wrong is W%, X%, Y% and Z% at residual thresholds of
0.05, 0.10, 0.15 and 0.23; the primary analysis uses 0.10."* Four numbers, all cited, nothing hidden. This costs
one extra table in the results and removes the entire line of attack — including from the reviewer who thinks
0.10 is too strict *and* the reviewer who thinks 0.23 double-counts measurement noise.

### 5.3a The operating characteristic this gives you — DETECTOR-SPEC §5's "cleanest available answer to B4"

`DETECTOR-SPEC` §5 wants the threshold to be *"an operating characteristic rather than an arbitrary constant"*:
targets noisy at the repeatability the threshold comes from, so a correct model misses them by about that much.
With the residual being an RMS over `k` territories of independent relative target errors of SD `σ`, the residual
is `σ·sqrt(χ²_k/k)`, so a **model that is correct except for target measurement noise** passes with probability
`P(χ²_k < k·(thr/σ)²)`. My arithmetic (χ² CDF, not from any paper):

| per-territory wsCV σ | k | pass rate at 0.05 | **pass rate at 0.10** | pass rate at 0.23 |
|---|---|---|---|---|
| 8.3% (Lubberink regional, §1.1) | 2 | 0.30 | **0.77** | 1.00 |
| 8.3% | 3 | 0.22 | **0.77** | 1.00 |
| 9.8% (Lubberink segmental) | 3 | 0.15 | **0.63** | 1.00 |
| 11.5% (Bober global COV, §1.2) | 3 | 0.10 | **0.48** | 0.99 |

**This is the argument that makes 0.10 principled.** At the literature's per-territory wsCV, a threshold of 0.10
passes a correct-but-noisy model about **three times in four** — neither degenerate-permissive nor unreachable.
The abandoned 1% threshold would have passed it essentially never; the repeatability coefficient (0.23) passes it
essentially always, which is exactly why 0.23 belongs in the *sensitivity* analysis and not as the primary. Put
this table, or a sentence from it, in the paper — it converts `VALIDATED_RESIDUAL` from an assumption into a
derived operating point.

### 5.4 Fix the detector's noise model to match

`DETECTOR-SPEC` §5's "target measurement noise at the test–retest SD" should be **per-territory wsSD = 8.3%**
(citing §1.1), applied independently per territory, **not** the RC. Record the choice and the citation in the spec
so the threshold and the noise model cannot drift apart.

### 5.5 Declare the deviation

Under STATISTICS-PLAN's own rule, the *value* does not change, so this is not a deviation in the constant. But the
**stated justification changes materially** (from "agreement within measurement precision" to "one within-subject
SD, deliberately strict"), and a **new pre-specified sensitivity analysis is added**. Both should be logged in the
pre-registration checklist as amendments dated 2026-09-19, before the confirmatory run.

---

## 6. What I could NOT establish

1. **No full peer-reviewed paper reports per-territory hyperaemic MBF test–retest repeatability.** The best
   source (§1.1) is a **conference abstract with n = 10**. I searched PubMed under Lubberink, Kero and Nordström
   with repeatability/reproducibility terms and found no full-paper version. If a reviewer objects to an abstract
   citation, the fallback is Jagathesan 2005 (§1.4) — a full paper, explicitly per-territory, RC 26–27% at stress —
   but that is dobutamine at 24 weeks, n = 15, which is a different stressor and a different interval.
2. **Whether "regional" in §1.1 means the 3 coronary territories.** The abstract does not say. Inferred from the
   group's convention; **not verified.**
3. **I did not read the full text of §1.2, §1.3, §1.4, §1.5, §1.6, §1.7** — all paywalled or not retrieved.
   Every number quoted from them is from the publisher-deposited abstract, verbatim. §1.1's results sentence came
   from the publisher's abstract page; §2.1 and §2.2 were read in PMC full text.
4. **No repeatability figure stratified by territory size or by which territory (LAD/LCx/RCA).** Smaller
   territories are noisier (§2.1 says so qualitatively) but I found no number for it. Our RCA/LCx territories may
   be worse than our LAD ones; we cannot quantify that.
5. **Nothing found on repeatability of territory perfusion measured as an absolute flow (mL/min) rather than a
   perfusion density (mL/min/g).** Our targets are flows; the literature is all flow-per-gram. The conversion
   involves a myocardial mass estimate, whose own error is not in any of these repeatability figures. This is a
   real, unquantified gap and should appear as a limitation.
6. **Whether any of these cohorts resemble ours.** Most are healthy volunteers or non-obstructive-CAD patients;
   repeatability in the diseased territories we care about may be worse (Sawada's CAD patients: 38 ± 16% regional
   CFR difference vs 19 ± 19% in normals, §1.8).
7. **The short-interval, per-territory, hyperaemic repeatability of CT myocardial perfusion MBF in humans is
   simply unmeasured.** Not "hard to find" — as far as two independent searches can establish, it does not exist
   (§2A). Four full-text reviews contain no such statistic. If the paper needs a CT number, it must either use the
   swine regional RMSE, the CMR regional RC as a bracket, or say the value is unknown.
8. **Moody et al. 2015 full text** (*J Nucl Cardiol* 22(5):935–951, DOI 10.1007/s12350-015-0100-0, PMID 25868451)
   — paywalled, not open access, no PMC copy. It is the most likely place to find a ready-made table of the
   primary repeatability figures. **Nothing in this document is attributed to it.** Worth retrieving via
   institutional access before submission.
9. **The JACC Expert Panel verbatim text came through a proxy**, because jacc.org and ScienceDirect both return
   403 (I verified the 403 myself). The substance was corroborated by an independent search-index snippet, but the
   **exact wording must be re-checked against the published PDF** before it is quoted in the manuscript.
10. **Two CT sources the assisting agent could not open** (Sliwicka et al., *Acta Radiol* 2024, PMID 38630492;
   and *Int J Cardiovasc Imaging* 2025, DOI 10.1007/s10554-025-03361-6) — **not verified**, do not cite. Both
   appear to be reanalysis-of-one-acquisition designs in any case.
