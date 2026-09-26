# Gate D2 — ASOCA terms, licence and annotator count. Checked 2026-09-19.

**Verdict: OBTAINABLE, but with one material limitation and one unverified clause. Gate D2 = CONDITIONAL PASS.**

Sources: the ASOCA challenge site and its Data Access page; the UK Data Service ReShare record 855916; the
Scientific Data descriptor (Gharleghi et al. 2023, via PMC). Checked by web, not by obtaining the data.

## 1. What ASOCA is

| | |
|---|---|
| Dataset title | *Computed Tomography Coronary Angiogram Images, Annotations and Associated Data of Normal and Diseased Arteries, 2017–2020* |
| Creators | Gharleghi, Adikari, Ellenberger, Webster, Ellis, Sowmya, Ooi, Beier |
| Contents | anonymised CTCA images, voxel-wise lumen annotations, **centrelines**, calcification scores, **lumen meshes** |
| Size | **40 released** (20 normal / 20 diseased). A further **20 test cases are held back** by the challenge |
| Annotation | *"performed independently by three annotators"*; *"combined using majority voting to generate the final annotations"* |
| Inclusion rule | *"All coronary vessels with a diameter larger 1 mm, representing 1–2 voxels, were included"* |

## 2. The material limitation — read this before planning anything around it

**Only the majority-vote combination is released. The three individual annotators' segmentations are not.**

So ASOCA **cannot** supply inter-observer disagreement, in the same way ImageCAS-X now cannot. Every public coronary
segmentation dataset we have looked at releases a consensus label and keeps the disagreement.

**Consequence for the documents:** `STUDY-PLAN-v2` §E0 describes ASOCA as *"40 CCTA, 20 healthy / 20 diseased,
multi-expert annotation"*. That is literally true and materially misleading — it reads as though per-expert masks are
available. It must be reworded to *"three annotators combined by majority voting; individual masks not released."*

**What ASOCA is still good for, and it is the thing we actually wanted it for:** an **external test set for the
detector** (`DETECTOR-SPEC` v0.2 §6) — a different population, scanner and annotation protocol, with centrelines and
meshes already supplied in the same shape as ImageCAS-X. That use is unaffected.

**But size it honestly.** 40 cases, minus our eligibility filters (healthy-network gate, ≥ 2 outlets, a deletable
branch, baseline in the usable FFR window). On ImageCAS-X those filters kept 97/150 and then 77. A comparable
attrition on 40 leaves roughly **20–25 usable cases** — enough for an external AUC with wide CIs, and it must be
reported as such, not as a second cohort.

## 3. Access and licence

**Access is gated. It is not a download.**

- Hosted at **UK Data Service ReShare, record 855916**.
- ReShare record states, verbatim: *"The Data Collection is available for download to users registered with the UK
  Data Service. All requests are subject to the permission of the data owner or his/her nominee."*
- So: **UKDS registration + data-owner permission.** Lead time unknown — assume weeks, not days, and start early if
  the external test is wanted.
- The challenge's own Data Access page additionally offers a **temporary Microsoft Forms request** *"while we work on
  having a better repository set up"*, which suggests the hosting arrangement is still in flux. Prefer ReShare as the
  citable route; use the form only if ReShare stalls.

**Licence — partly verified, one clause outstanding.**

- Governed by the **UK Data Service End User Licence**, plus owner permission.
- Secondary sources (the publisher's own community post) state that **both commercial and non-commercial use is
  permitted** and that the data may be used for unrestricted research.
- **CAUTION, and the reason this is not a clean pass:** the "CC BY 4.0" that appears on the Scientific Data article
  is the **article's** licence boilerplate — *"This article is licensed under a Creative Commons Attribution 4.0
  International License"* — **not** a statement about the dataset. Conflating the two is an easy and consequential
  mistake. **Do not cite CC BY 4.0 for the ASOCA data.**
- **UNVERIFIED:** whether the EUL permits redistributing **derived** outputs (our corrupted geometries, per-case
  results) as Source Data alongside the paper. `STUDY-PLAN-v2` §8 promises exactly that for every dataset used.
  **This must be confirmed from the EUL text or from the data owner before ASOCA results go into a submission.**

## 4. Actions

- [ ] Register with the UK Data Service and request record 855916; expect an owner-permission step.
- [ ] In the request, ask explicitly whether **derived results** may be redeposited as Source Data (§8's promise).
- [ ] Reword `STUDY-PLAN-v2` §E0's "multi-expert annotation" to say what is actually released.
- [ ] Size the external test at ~20–25 usable cases in `DETECTOR-SPEC` §6, not 40.
- [ ] Do **not** cite CC BY 4.0 for the data.

## 5. Residual risk

If the EUL forbids redeposit of derived outputs, the options are: report ASOCA results without Source Data and say
why; or drop ASOCA and fall back to a held-out ImageCAS-X split — which `DETECTOR-SPEC` §6 already flags is *"a
weaker external claim"*, since a split is not an external dataset and the paper will not call it one.
