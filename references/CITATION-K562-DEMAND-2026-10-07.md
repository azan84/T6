# Provenance and justification of the hyperaemic-demand constant k = 562 s⁻¹ (Q = k r_in³)

Date: 2026-10-07. Scope: `code/zerod_ffr.py` `K_MURRAY = 562.0`; manuscript Methods B (`drafts/manuscript/main.tex`
line 171). Nothing in the project was edited; this file is the only output. Every DOI below was resolved through the
Crossref REST API on 2026-10-07; abstracts and open-access full texts were read through Europe PMC; the Fournier 2021
PDF was read with `pdftotext`. Items that could not be verified are marked **UNVERIFIED**.

---

## 1. Provenance inside the project

| Where | Date (file mtime / stated) | What it says | Source given |
|---|---|---|---|
| `code/zerod_ffr.py` line 59 | 2026-09-19 23:24 (current); header says "v3 (2026-09-18)" | `K_MURRAY = 562.0  # s^-1 : hyperaemic Q = k r^3 (r = 2.0 mm -> 4.5 mL/s)` | none |
| `Paper6-T6.zip` → `code/zerod_ffr.py` (earliest surviving copy) | 2026-09-18 17:20 | identical line and comment; file already labelled v3 | none |
| `code/run_prevalence.py` (Gate E0 driver) | 2026-09-18 15:22 | calls `tree.ffr(mode="murray")`; defines the alternative `TOTAL_HYP_FLOW = 6.5e-6  # m^3/s, whole heart at maximal vasodilation` | none |
| `protocol/archive/CFD-ARM-SPEC-v0.1-superseded-2026-09-18.md` §2.2 | 2026-09-18 16:20 | "Murray demand Q = k r_inlet³ — the same demand as the leaky model" | none |
| `protocol/SEVERITY-SWEEP-SPEC.md` line 47 | draft 2026-09-18, mtime 09-19 | "Murray demand Q = k r_inlet³ (k = 562 s⁻¹)" | none |
| `results/E0-PREVALENCE-NOTE.md` | 2026-09-18 | demand model chosen "on principle (Murray self-scales and is consistent with the leakage model) and report sensitivity"; fixed-territory 6.5 mL/s used as the check | none |
| `drafts/stageA_validation/STAGE-A-VALIDATION.tex` line 1427 | Stage A report (CFD side) | "The study's 0D demand is Q = k r_in³ with k = 562 s⁻¹ (the 0D code labels this demand 'hyperaemic') ... the size of the ratio carries no physiological claim" | none |
| `drafts/manuscript/ars_intro_methods.tex` line 110 | V2 draft | cites `\cite{murray1926}` for k = 562 | murray1926 (wrong: Murray gives the cube law, not a coefficient) |
| `drafts/manuscript/MERGE-NOTES-2026-10-07.md` | 2026-10-07 | murray1926 dropped as the citation for k ("Murray supports the cube law only"); "k = 562 and K_t = 1.52 left uncited as before" | — |
| `drafts/manuscript/main.tex` line 171 | current | "k = 562 s⁻¹ ...; this model setting gives an inlet of 2.0 mm radius a hyperaemic flow of 4.5 mL/s" | none |

Findings.
1. The constant entered the project with the first 0D solver on 2026-09-18, before 15:22 (the E0 driver of that time
   already uses the Murray demand). The v1/v2 solver files are not preserved; the earliest surviving copy (zip,
   17:20) already carries the identical constant and comment. No earlier draft, note, review (the 2026-09-17 FABLE
   review predates the code and does not mention a demand constant), plan, protocol or extraction note records where
   562 or 4.5 mL/s came from. The inline comment is the only recorded reasoning: the coefficient was fixed so that a
   4.0 mm-diameter vessel receives 4.5 mL/s (270 mL/min).
2. The 6.5 mL/s whole-heart figure of the fixed-territory check is equally uncited and is low against measured
   values (see §2.1: 582–668 mL/min = 9.7–11.1 mL/s).
3. The wider folder (Paper1-P16, Paper2–Paper7, Proposal/ideation_run, research-pipeline, PreviousStudy) contains no
   earlier version of this solver and no occurrence of K_MURRAY, 562 s⁻¹ or 4.5 mL/s in this sense.
4. The pre-registration documents state the value without a source, so the manuscript cannot attribute it to the
   registration either. It must be declared as a model setting and anchored to measured flow.

## 2. Literature

### 2.1 Measured absolute hyperaemic coronary flow in humans

| Source (DOI verified) | Method / condition | Values |
|---|---|---|
| Fournier et al. 2021, EuroIntervention 17(4):e309–e316, 10.4244/EIJ-D-20-00684 (abstract + full PDF read) | Continuous thermodilution (RayFlow, saline 20 mL/min, which itself induces hyperaemia equivalent to adenosine); 177 arteries, 69 patients; 25 angiographically normal controls, 44 mild non-obstructive atherosclerosis | Hyperaemic Q, mL/min, mean ± SD (Supplementary Table 2): LAD 293 ± 102 (controls) / 228 ± 71 (patients); LCX 204 ± 104 / 160 ± 64; RCA 197 ± 63 / 189 ± 65; whole heart 668 ± 185 / 582 ± 138. Normalised to CT territory mass: 5.9 ± 1.9, 4.9 ± 1.7, 5.3 ± 2.1 mL/min/g (LAD, LCX, RCA; controls); territory masses 50 ± 13, 36 ± 16, 49 ± 16 g. 5–95 % range of LAD Q in controls 149–528 mL/min. |
| Taylor DJ et al. 2022, Front Physiol 13:871912, 10.3389/fphys.2022.871912 (full text read) | Continuous-infusion thermodilution, 27 branched arteries (18 LAD, 7 LCX, 2 RCA) in 20 patients | Mean inlet Q 219 ± 61 mL/min (3.65 mL/s) |
| Gallinoro et al. 2021, EuroIntervention, 10.4244/EIJ-D-20-01092 (abstract) | Thermodilution at 10 vs 20 mL/min saline | 20 mL/min infusion induces hyperaemia (Pd/Pa falls, APV rises); CFR_thermo 2.78 ± 0.91 |
| Wilson et al. 1990, Circulation 82(5):1595–1606, 10.1161/01.CIR.82.5.1595 (abstract) | Doppler catheter, adenosine vs papaverine | Maximal hyperaemia = 4.4–4.6 × resting velocity (i.c. bolus left 4.6 ± 0.7, right 4.4 ± 1.0; i.v. 140 µg/kg/min 4.4 ± 0.9) |
| Sakamoto et al. 2013, Am J Cardiol 111(10):1420–1424, 10.1016/j.amjcard.2013.01.290 (abstract) | Angiography + IVUS segment volume / contrast transit time; **resting**; 1,322 vessels, 496 patients | LCX 72 ± 37 (right-dominant) vs 113 ± 43 mL/min (left/balanced); RCA 113 ± 49 vs 56 ± 40 mL/min; LAD not different by dominance (value not in abstract) |
| Aarnoudse et al. 2007, JACC 50(24):2294–2304, 10.1016/j.jacc.2007.08.047 (abstract) | Validation of the thermodilution method (dogs, 35 patients) | Method paper; no normal values |
| Xaplanteris et al. 2018, Circ Cardiovasc Interv 11:e006194, 10.1161/CIRCINTERVENTIONS.117.006194 (abstract) | Feasibility/safety/reproducibility, 135 patients | ICC 0.89 for repeat flow; no per-vessel normal values in abstract |
| Dodge et al. 1992, Circulation 86(1):232–246, 10.1161/01.CIR.86.1.232 (abstract) | Normal lumen diameters, 83 arteriograms | LM 4.5 ± 0.5 mm, proximal LAD 3.7 ± 0.4 mm, distal LAD 1.9 ± 0.4 mm, proximal RCA 3.9 ± 0.6 mm (right-dominant) / 2.8 ± 0.5 mm, proximal LCX 3.4 ± 0.5 / 4.2 ± 0.6 mm; women −9 % |

Not pursued: PET MBF × mass (Fournier's per-gram thermodilution values already give the territory-based number
needed; thermodilution per-gram values are higher than PET MBF, which the manuscript need not discuss).

### 2.2 Flow–diameter laws used for coronary boundary conditions

| Source | Formula / exponent | Coefficient | Condition | Verification |
|---|---|---|---|---|
| Murray 1926, PNAS 12(3):207–214, 10.1073/pnas.12.3.207 (in refs.bib) | Q ∝ D³ | none for coronaries | theory | DOI verified |
| Taylor DJ et al. 2024, Am J Physiol Heart Circ Physiol 327(1):H182–H190, 10.1152/ajpheart.00142.2024 (full text read) | Pooled flow–diameter exponent 2.39 (95 % CI 2.24–2.54), 18 studies, 1,070 trees; humans 2.42 (2.17–2.67); epicardial 2.43 | none (exponents only) | mixed | verified |
| van der Giessen et al. 2011, J Biomech 44(6):1089–1095, 10.1016/j.jbiomech.2011.01.036 (abstract; tabulated in Taylor 2024) | Side-branch flow-ratio exponent 2.27 (abstract); flow–diameter fit 2.55 (2.27–2.83) (Taylor 2024 Table 2); based on Doriot et al. 2000 Doppler data, resting, 6 trees | **The coefficient "1.43" in Q = 1.43 d^2.55 could not be found in any accessible text — UNVERIFIED; do not cite a coefficient from this paper** | resting | DOI verified; exponent verified; coefficient unverified |
| Doriot et al. 2000, Coron Artery Dis 11(6):495–502, 10.1097/00019501-200009000-00008 (abstract) | Resting Doppler flows in 36 normal bifurcations; mean WSS 0.68 Pa | — | resting | DOI verified |
| Taylor DJ et al. 2022 (above) | Optimal exponent 2.15 for flow, 2.38 for microvascular resistance | none | hyperaemic (thermodilution) | verified |
| Choi et al. 2020, Physiol Rep 8(14):e14514, 10.14814/phy2.14514 (full text read) | Q–D exponent 2.27 ± 0.24 (QFR-derived flow, 106 arteries); Q–M 0.50; D–M 0.22 | Y₀ tabulated but units not stated — unusable | near-resting (nitroglycerin, contrast) | verified exponent |
| Choy & Kassab 2008, J Appl Physiol 104(5):1281–1286, 10.1152/japplphysiol.01261.2007 (abstract; in refs.bib) | Q ∝ M^{3/4}, D ∝ M^{3/8}, L ∝ M^{3/4}; pig, perfusion at 100 mmHg | none | ex vivo | verified |
| Zhou, Kassab, Molloi 1999, Phys Med Biol 44(12):2929–2945, 10.1088/0031-9155/44/12/306 (abstract) | Generalised Murray law; the 7/3 exponent is attributed to Kassab's group by Taylor 2024 | none in abstract | morphometric | DOI verified; **coefficient UNVERIFIED** |
| Huo & Kassab 2012, J R Soc Interface 9(66):190–200, 10.1098/rsif.2011.0270 (abstract) | Intraspecific scaling: V ∝ D³ validated; flow–diameter law derived | none in abstract | theory | DOI verified; coefficient unverified |
| Wilson 1990 (above) | hyperaemia = 4.4–4.6 × rest | — | — | verified |
| Taylor CA, Fonte, Min 2013, JACC 61(22):2233–2241, 10.1016/j.jacc.2012.11.083 (in refs.bib; full text blocked) | HeartFlow: rest flow from myocardial mass, outlets by form–function (Murray-type) rule, hyperaemia by microvascular resistance reduction | the specific numbers (mass exponent 0.75; resistance factor 0.24) **UNVERIFIED from the text**; a secondary source (Frontiers Bioeng 2023, 10.3389/fbioe.2023.1207300) gives "0.23 times the resting state" citing Wilson 1990 | rest → hyperaemia | DOI verified |
| Kim et al. 2010, Ann Biomed Eng 38(10):3195–3209, 10.1007/s10439-010-0083-6 (in refs.bib; abstract only) | lumped coronary bed per outlet | flow fraction and hyperaemia factor **UNVERIFIED** | — | DOI verified |
| Sharma et al. 2012, EMBC, 10.1109/EMBC.2012.6347523 (abstract) | rest BCs from non-invasive data; hyperaemia by a transfer function | numbers **UNVERIFIED** | — | DOI verified |
| Itu et al. 2016, J Appl Physiol 121(1):42–52, 10.1152/japplphysiol.00752.2015 (abstract) | ML surrogate of a physics model | BC numbers **UNVERIFIED** | — | DOI verified |
| Fossan et al. 2018, Cardiovasc Eng Technol 9(4):597–622, 10.1007/s13239-018-00388-w (abstract) | "the uncertainty related to the factor by which peripheral resistance is reduced from baseline to hyperemic conditions proved to be the most influential parameter for FFR predictions"; "Improved measurement of coronary blood flow has the potential to reduce uncertainty in computational FFR predictions significantly" | flow-setting numbers not in abstract | — | DOI verified |
| Müller et al. 2021, Int J Numer Meth Biomed Eng 37(11):e3246, 10.1002/cnm.3246 (abstract) | Baseline-flow estimation/distribution methods "proved to have a significant impact on diagnostic performance" of reduced-order FFR | — | — | DOI verified |
| Fossan et al. 2025 (project note `extraction/full/fossan-2025-autoregulation-diagnosis.md`; `fossan2026` in refs.bib) | Resting Q_cor = 0.8 mL/min/g × TMM, TMM = 2.4 × LV mass; hyperaemia by a population "fourfold reduction in resistance (refs 10, 15–18)", Wilson 1990 as the underlying study | territory law: ≈ 3.2 mL/min/g at hyperaemia | rest → hyperaemia | from project extraction note |
| Tu et al. 2016, JACC Cardiovasc Interv 9(19):2024–2035, 10.1016/j.jcin.2016.07.013 (abstract) | fQFR uses a "fixed empiric hyperemic flow velocity" | the value 0.35 m/s is widely quoted but **not in the abstract — UNVERIFIED** | hyperaemic | DOI verified |
| Gosling et al. 2020, J Biomech 103:109698 (in refs.bib; project extraction note) | 1D model with Murray-law distributed leakage, 146 arteries, pressure-wire boundary data | Mean inlet hyperaemic flow 2.52 mL/s (leaky) vs 1.53 mL/s (no leakage) | hyperaemic | from project note |

### 2.3 What each law gives, and the comparison with Q = 562 r³

Project law: Q = 562 r³ (r in m, Q in m³/s). r = 2.0 mm → 4.50 mL/s (270 mL/min); r = 1.39 mm (cohort median) →
1.51 mL/s (91 mL/min). Cohort (E0 test split, 320 trees, `results/E0_prevalence_test.csv`, mode murray, scale 1):
r_in median 1.39 mm (IQR 1.16–1.64, range 0.81–2.43); Q_demand median 1.52 mL/s (IQR 0.88–2.50, max 8.0); left
trees median 1.77 mL/s, right 1.35 mL/s.

| Law | r = 2.0 mm (d = 4.0 mm) | r = 1.39 mm (d = 2.78 mm) | Rest→hyperaemia multiplier used |
|---|---|---|---|
| Q = 562 r³ (project) | 4.50 mL/s (270 mL/min) | 1.51 mL/s (91 mL/min) | none (declared hyperaemic) |
| Measured hyperaemic flow anchored on normal calibre (Fournier 2021 × Dodge 1992): LAD 3.7 mm ↔ 228–293 mL/min; LM 4.5 mm ↔ LAD+LCX 388–497 mL/min; RCA 3.9 mm ↔ 189–197 mL/min | implied k: LAD 600–771 s⁻¹; LM 568–727 s⁻¹; RCA 425–443 s⁻¹ (k = Q / r³) | — | none (measured hyperaemia) |
| 562 r³ evaluated at the normal calibres | LAD (r 1.85 mm): 3.56 mL/s = 213 mL/min vs 228–293 (−7 % to −27 %); LM (r 2.25): 6.40 mL/s = 384 mL/min vs 388–497 (−1 % to −23 %); RCA (r 1.95): 4.17 mL/s = 250 mL/min vs 189–197 (+27 % to +32 %) | — | — |
| Fixed hyperaemic velocity 0.35 m/s (fQFR convention; value unverified) × π r² | 4.40 mL/s | 2.12 mL/s | none |
| Taylor 2024 pooled exponent 2.39, anchored to 4.50 mL/s at r = 2.0 mm | 4.50 mL/s | 1.88 mL/s (cube law gives 1.51: 20 % lower) | — |
| Territory law (Fossan 2025 resting 0.8 mL/min/g × 4; Fournier hyperaemic 4.9–5.9 mL/min/g) | LAD territory 50 g → 160–295 mL/min = 2.7–4.9 mL/s | not diameter-based | ×4 (Wilson 1990: 4.4–4.6) |
| van der Giessen "Q = 1.43 d^2.55" (coefficient unverified; if Q in mL/min, d in mm) | 49 mL/min rest → ×4.4 = 3.6 mL/s | 19 mL/min rest → 1.4 mL/s | ×4.4 (Wilson 1990) |
| Project fixed-territory check, 6.5 mL/s whole heart | LCA 0.70–0.82 × 6.5 = 4.6–5.3 mL/s regardless of calibre | same | none; 6.5 mL/s is 35–40 % below Fournier's 9.7–11.1 mL/s |

Reading of the table. With the hyperaemic flows measured by continuous thermodilution (Fournier 2021) and the normal
calibres of Dodge 1992, the coefficient implied by the data lies between about 430 and 770 s⁻¹ depending on the
vessel and population; k = 562 s⁻¹ sits inside that range, close to the values for patients with mild
atherosclerosis and for the left main. The scatter of the measurements (SD 30–50 % of the mean; 5–95 % range of LAD
flow 149–528 mL/min in normals) is far wider than the distance between 562 and any single anchor. The constant is
therefore defensible as a model setting matched to measured hyperaemic flow, but it cannot be attributed to a
publication: no paper states k = 562 s⁻¹ or 4.5 mL/s at 2.0 mm, and the "Q = 1.43 d^2.55" coefficient attributed to
van der Giessen 2011 could not be verified anywhere.

The cube exponent is a modelling choice consistent with the bed (leak conductance ∝ r_ref³). Human data pool to
2.39 (Taylor 2024) and 2.15–2.27 in single studies (Taylor 2022, van der Giessen 2011, Choi 2020). Over the cohort's
inlet range (0.8–2.4 mm) the choice of exponent changes the relative demand of small versus large trees by up to
about 25 % at the median radius (anchored at 2.0 mm), which is of the same order as the k uncertainty itself; it is
a limitation to state, not a reason to change the model now.

## 3. Sensitivity of FFR to k (existing evidence)

Pre-registered: `protocol/STATISTICS-PLAN.md` §10 "Demand-model sensitivity: flow scaled ×0.7 / ×1.0 / ×1.3 on the
selected instances; reported alongside." `STUDY-PLAN-v2.md` E0 row: "the count is highly sensitive to the
flow-demand model — fixed territory flow puts 140 trees in 0.70–0.90 vs Murray's 20 ... The demand model must be
chosen on principle and its sensitivity reported."

What exists. The ×0.7/×1.3 scaling was run only at Gate E0 (natural cohort, baseline FFR, 320 trees), not on the
150 selected ablation instances: `results/ablation-2026-10-07.csv` has no scale column and `code/ablation.py` calls
`demand("murray", 1.0)` only. Computed today from `results/E0_prevalence_test.csv` (mode murray; 318 trees with all
three scales; 175 lesions with `lesion_ffr20`):

| Scaling of k | Main-vessel min-FFR change, median (IQR; p90; max) | Flips at 0.80 | Trees with FFR 0.70–0.90 | Lesion FFR (20 mm) change, median (p90) |
|---|---|---|---|---|
| ×0.7 | +0.016 (0.011–0.021; 0.028; 0.080) | 2 / 318 | 4 (vs 20 at ×1.0) | +0.013 (0.030) |
| ×1.3 | −0.016 (−0.022 to −0.011; 0.028; 0.073) | 2 / 318 | 52 (vs 20 at ×1.0) | −0.014 (0.030) |

The response is close to linear in k: for trees with baseline FFR < 0.95 the median ratio ΔFFR / (1 − FFR) is −0.29
for a +30 % demand, i.e. the pressure loss scales almost proportionally with flow (Poiseuille-dominated, with a mild
super-linear contribution from the expansion loss). Consequences for the paper's outcomes:

- Baseline FFR: a 30 % error in k shifts FFR by about 0.3 × (1 − FFR), a median 0.016 in this cohort, below the
  0.05 material threshold and of the order of the 0.01 noise floor. Near-threshold counts in the natural cohort are
  sensitive (4 / 20 / 52), which is exactly why the severity sweep exists: the sweep populates the 0.65–0.95 band by
  construction at k = 562, so a different k would call for a different sweep selection, not for a different design.
- Paired outcome ΔFFR (corrupted minus clean, same k, same C): both members scale together, so ΔFFR scales roughly
  in proportion to k; a ±30 % error in k moves the 0.05 threshold to an effective 0.038–0.065 and leaves the ranking
  of error types and protocols unchanged. This is a first-order argument, not a measured one; the measured check on
  the selected instances is the pre-registered ×0.7/×1.3 run, which has not been done at the ablation stage.
- Protocol C: by construction (`code/negatives.py` header: "cardiac output ... absorbed by a global scaling"), the
  tuned protocol refits the bed scaling to territory flows, so the tuned results do not depend on k at all; only
  Protocols A and B carry k through the calibrated C.
- Radius bias: the cohort's EDT radii read 23–44 % below the 3D area-equivalent radius (STUDY-PLAN-v2 2026-10-03
  note). Under Q = k r_in³ the demand falls with the under-read radius (r³) while resistance rises (r⁻⁴), so the net
  pressure loss scales as r⁻¹; under a fixed-flow (territory) model the loss would scale as r⁻⁴. The self-scaling
  demand is therefore the less radius-sensitive choice for this cohort, which is the principled reason recorded in
  the E0 note.

Recommendation on the gap: if the ablation run is cheap enough before 2026-10-14 (the negatives run of 5,860 rows
took 44 min; the ablation driver already accepts `Tree.demand(scale=)`), run Protocols A and B at ×0.7 and ×1.3 on
the 150 instances and report the flip counts beside the main table, which closes the pre-registered item. If not
feasible, state the E0 figures above and the gap plainly in Limitations.

## 4. Recommendation

Verdict. k = 562 s⁻¹ is defensible as a declared model setting: it reproduces, for vessels of normal proximal
calibre, hyperaemic flows inside the range measured by continuous thermodilution in humans (within −27 % to +32 % of
the vessel means, against a measurement SD of 30–50 %). It is not traceable to any publication, and the manuscript
must not imply that it is. The best supporting citations are Fournier 2021 (measured hyperaemic flow per artery and
per gram; DOI verified, full text read) and Dodge 1992 (normal calibre; DOI verified), with Murray 1926 kept for the
cube law only. No change of value is recommended before submission: a literature-anchored value would be anywhere in
430–770 s⁻¹, 562 is inside that range, and re-running the cohort, the sweep selection and the 3D packages is not
feasible before 2026-10-14. Changing k to, say, 700 s⁻¹ (LAD-controls anchor) would lower baseline FFR by about
0.25 × (1 − FFR) (median ≈ 0.013), raise near-threshold counts in the natural cohort, re-select the sweep cohort,
and scale ΔFFR by roughly the same factor; it would not change which error types or protocols flip decisions.

### 4.1 Replacement text for Methods B (`main.tex` lines 169–172)

Replace

> In both structures $C$ was calibrated on the healthy-equivalent network, the tree with its reference radius and no
> lesion, so that inflow equals the hyperaemic demand $Q = k\,r_\mathrm{in}^3$ with $k = 562$~s$^{-1}$ and
> $r_\mathrm{in}$ the inlet radius; this model setting gives an inlet of 2.0~mm radius a hyperaemic flow of 4.5~mL/s.

with

```latex
In both structures $C$ was calibrated on the healthy-equivalent network, the tree with its reference radius and no
lesion, so that inflow equals a hyperaemic demand $Q = k\,r_\mathrm{in}^3$, where $r_\mathrm{in}$ is the inlet
radius. The cube law is Murray's \cite{murray1926}; the constant $k = 562$~s$^{-1}$ is a model setting chosen so
that a vessel of normal proximal left anterior descending calibre, 3.7~mm in diameter \cite{dodge1992}, carries
3.6~mL/s (213~mL/min), within the hyperaemic flow measured in that artery by continuous thermodilution,
$228 \pm 71$ to $293 \pm 102$~mL/min \cite{fournier2021}. For this cohort, with a median inlet radius of 1.39~mm,
the median demand was 1.5~mL/s.
```

Shorter variant if space is tight:

```latex
... so that inflow equals a hyperaemic demand $Q = k\,r_\mathrm{in}^3$ \cite{murray1926}, where $r_\mathrm{in}$ is
the inlet radius and $k = 562$~s$^{-1}$ is a model setting that gives a 3.7~mm vessel, the normal proximal left
anterior descending calibre \cite{dodge1992}, 213~mL/min, within the hyperaemic flow measured in that artery by
thermodilution ($228 \pm 71$ to $293 \pm 102$~mL/min) \cite{fournier2021}.
```

### 4.2 Sensitivity sentence (Results A, after the centreline-spacing check, or Limitations)

```latex
Scaling $k$ by 0.7 and 1.3 moved the baseline main-vessel FFR of the 320 unmodified test-split trees by a median of
$\pm 0.016$ (90th percentile 0.028) and changed the classification at 0.80 in two trees in each direction; the
change is close to $0.3\,(1-\mathrm{FFR})$ per 30\% change in demand, and the paired differences between corrupted
and clean models scale in proportion.
```

The last clause is a first-order statement; if the ×0.7/×1.3 ablation run is completed, replace it with the measured
flip counts. If it is not completed, add to Limitations:

```latex
The demand constant is a model setting matched to measured hyperaemic flow rather than a measured quantity, and the
cube exponent is above the pooled human flow--diameter exponent of 2.39 \cite{taylor2024murray}; the pre-registered
demand-scaling sensitivity was evaluated on baseline FFR only.
```

### 4.3 BibTeX (all DOIs resolved through Crossref on 2026-10-07; `murray1926` already in refs.bib)

```bibtex
@article{fournier2021,
  title   = {Normal values of thermodilution-derived absolute coronary blood flow and microvascular resistance in humans},
  author  = {Fournier, Stephane and Keulards, Dani{\"e}lle C. J. and van 't Veer, Marcel and Colaiori, Iginio and Di Gioia, Giuseppe and Zimmermann, Frederik M. and Mizukami, Takuya and Nagumo, Sakura and Kodeboina, Monika and El Farissi, Mohamed and Zelis, Jo M. and Sonck, Jeroen and Collet, Carlos and Pijls, Nico H. J. and De Bruyne, Bernard},
  journal = {EuroIntervention},
  volume  = {17},
  number  = {4},
  pages   = {e309--e316},
  year    = {2021},
  doi     = {10.4244/EIJ-D-20-00684}
}

@article{dodge1992,
  title   = {Lumen diameter of normal human coronary arteries. {Influence} of age, sex, anatomic variation, and left ventricular hypertrophy or dilation},
  author  = {Dodge, J. Theodore and Brown, B. Greg and Bolson, Edward L. and Dodge, Harold T.},
  journal = {Circulation},
  volume  = {86},
  number  = {1},
  pages   = {232--246},
  year    = {1992},
  doi     = {10.1161/01.CIR.86.1.232}
}

@article{taylor2024murray,
  title   = {Systematic review and meta-analysis of {Murray}'s law in the coronary arterial circulation},
  author  = {Taylor, Daniel J. and Saxton, Harry and Halliday, Ian and Newman, Tom and Hose, D. Rodney and Kassab, Ghassan S. and Gunn, Julian P. and Morris, Paul D.},
  journal = {American Journal of Physiology-Heart and Circulatory Physiology},
  volume  = {327},
  number  = {1},
  pages   = {H182--H190},
  year    = {2024},
  doi     = {10.1152/ajpheart.00142.2024}
}
```

Optional (only if the Discussion wants the hyperaemia multiplier or the measured-exponent studies):

```bibtex
@article{wilson1990,
  title   = {Effects of adenosine on human coronary arterial circulation},
  author  = {Wilson, Robert F. and Wyche, Kathleen and Christensen, Betsy V. and Zimmer, Scott and Laxson, David D.},
  journal = {Circulation},
  volume  = {82},
  number  = {5},
  pages   = {1595--1606},
  year    = {1990},
  doi     = {10.1161/01.CIR.82.5.1595}
}

@article{taylor2022murray,
  title   = {Refining our understanding of the flow through coronary artery branches; revisiting {Murray}'s law in human epicardial coronary arteries},
  author  = {Taylor, Daniel J. and Feher, Jeroen and Halliday, Ian and Hose, D. Rodney and Gosling, Rebecca and Aubiniere-Robb, Louise and van 't Veer, Marcel and Keulards, Danielle and Tonino, Pim A. L. and Rochette, Michel and Gunn, Julian and Morris, Paul D.},
  journal = {Frontiers in Physiology},
  volume  = {13},
  pages   = {871912},
  year    = {2022},
  doi     = {10.3389/fphys.2022.871912}
}

@article{vandergiessen2011,
  title   = {The influence of boundary conditions on wall shear stress distribution in patients specific coronary trees},
  author  = {van der Giessen, Alina G. and Groen, Harald C. and Doriot, Pierre-Andr{\'e} and de Feyter, Pim J. and van der Steen, Antonius F. W. and van de Vosse, Frans N. and Wentzel, Jolanda J. and Gijsen, Frank J. H.},
  journal = {Journal of Biomechanics},
  volume  = {44},
  number  = {6},
  pages   = {1089--1095},
  year    = {2011},
  doi     = {10.1016/j.jbiomech.2011.01.036}
}
```

Given names for Dodge 1992 and Wilson 1990 are expanded from Crossref initials and the journal record; initials are
what Crossref returns (J T Dodge; R F Wilson). Use initials if the journal's style requires exact Crossref form.

### 4.4 Do not cite

- `murray1926` for the value of k (it supports the cube law only; the merge notes already removed it).
- van der Giessen 2011 for a coefficient (none verified).
- Taylor 2013 / Kim 2010 / Itu 2016 / Sharma 2012 for specific numbers (0.75 mass exponent, 0.24 or 0.23 resistance
  factor, 4 % of cardiac output): plausible and widely repeated, but not verified from the texts in this check.
- Tu 2016 for 0.35 m/s (not in the abstract; the full text was not accessible).

---

## Summary

k = 562 s⁻¹ entered the project on 2026-09-18 as an inline code constant with the comment "r = 2.0 mm → 4.5 mL/s" and
no source; no earlier version, note or review records its origin. No publication states this coefficient. It is
nevertheless defensible: with the normal calibres of Dodge 1992 and the hyperaemic flows measured by continuous
thermodilution in Fournier 2021 the implied coefficient is 430–770 s⁻¹, and 562 lies inside that range (a 3.7 mm LAD
carries 213 mL/min under the model against 228–293 mL/min measured). Keep the value, declare it as a model setting
matched to measured hyperaemic flow, cite Fournier 2021 and Dodge 1992 for the anchor and Murray 1926 for the cube
law only, and report the demand-scaling sensitivity (median ±0.016 FFR, 2/318 flips per direction for ±30 % in k,
from the E0 run). The pre-registered ×0.7/×1.3 run on the 150 selected instances has not been done; run it if
feasible before 2026-10-14, otherwise state the gap in Limitations.

Recommended Methods sentence: "In both structures $C$ was calibrated on the healthy-equivalent network ... so that
inflow equals a hyperaemic demand $Q = k\,r_\mathrm{in}^3$, where $r_\mathrm{in}$ is the inlet radius. The cube law
is Murray's \cite{murray1926}; the constant $k = 562$~s$^{-1}$ is a model setting chosen so that a vessel of normal
proximal left anterior descending calibre, 3.7~mm in diameter \cite{dodge1992}, carries 3.6~mL/s (213~mL/min),
within the hyperaemic flow measured in that artery by continuous thermodilution, $228 \pm 71$ to
$293 \pm 102$~mL/min \cite{fournier2021}. For this cohort, with a median inlet radius of 1.39~mm, the median demand
was 1.5~mL/s."
