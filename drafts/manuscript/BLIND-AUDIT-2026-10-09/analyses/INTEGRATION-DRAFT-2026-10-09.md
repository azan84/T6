# Integration draft: A5, A6, A7, T5 and T5L2 into main.tex and supplement.tex (Fable, 2026-10-09)

Built on PLAN-v2-INTEGRATION.md §3–§4 with decisions D1–D5, and on every correction in FABLE-VERIFY-2026-10-09.md. Every OLD block is copied verbatim from the current `drafts/manuscript/main.tex` (line breaks included) so that it can be applied by exact string replacement; NEW is its replacement. Numbers are listed with their source in §8. Two new bib entries are in §9. Nothing in this file has been applied.

Conventions in the new text: ½ voxel is the primary throat magnitude and the only one in Table I; ±10 points of DS appears once in II-C and otherwise in the supplement; "caliber errors away from the throat" means T3 and T4; no count of bound fits uses the number 97.

---

## 1. Title

```latex
\title{Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study}
```

OLD (main.tex lines 14–15):
```old
\title{Topological Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In
Silico Study}
```
NEW:
```new
\title{Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study}
```

Also the running head (line 30) is unchanged ("Segmentation Error and BC Tuning in Coronary FFR"). The supplement title line (supplement.tex line 20) drops "Topological" in the same way.

## 2. Abstract (248 words)

OLD:
```old
Fractional flow reserve (FFR), which guides coronary revascularization, can be computed from computed tomography
angiography. The computation depends on the segmented artery and on outlet boundary conditions derived from it,
often tuned to measured perfusion, as in a digital twin. We tested in silico whether a perfusion-matched model can be
misclassified at 0.80. We inserted 150 stenoses into 108 coronary trees, applied four segmentation errors (missed
side branch, vessel break, longer lesion, narrowed taper), and recomputed FFR with a reduced-order model under fixed,
re-derived and tuned boundary conditions, with one global or per-territory parameter fitted to clean-model flows of
two or three main-branch territories, in discrete and leaky (distributed-outflow) microvascular beds. In this
threshold-stratified cohort, with fixed boundary conditions, branching (topological) errors changed the decision in
32--33\% of models, against 6--10\% for vessel-size (caliber) errors of inter-observer magnitude, for the error
magnitudes studied. Re-derived or tuned boundary conditions reduced these to 5--19\%. Tuned models passed a
perfusion check stricter than measurement repeatability while wrong by more than 0.05: 19--20\% (discrete bed) and
5--8\% (leaky bed) of topological-error models and 4--18\% of caliber-error models, mostly taper, against 3--4\% for
correct anatomy. Per-territory tuning corrected the typical missed branch; in one three-dimensional case it reduced a
shift of 0.074 to 0.022. Flip-rate directions held at doubled and, in the leaky bed, tripled demand, but the tuned
excess over re-derivation was significant only at baseline demand in the discrete bed. A perfusion match after
tuning did not certify the segmented branching or caliber.
```
NEW:
```new
Fractional flow reserve (FFR), which guides coronary revascularization, can be computed from computed tomography
angiography. The computation depends on the segmented artery and on outlet boundary conditions derived from it,
often tuned to measured perfusion, as in a digital twin. We tested in silico whether a perfusion-matched model can be
misclassified at 0.80. We inserted 150 stenoses into 108 coronary trees, applied five segmentation errors (missed
side branch, vessel break, longer lesion, narrowed taper, half-voxel throat diameter), and recomputed FFR with a
reduced-order model under fixed, re-derived and tuned boundary conditions, with one global or per-territory
parameter fitted to clean-model flows of main-branch territories, in discrete and leaky (distributed-outflow)
microvascular beds. In this threshold-stratified cohort, with fixed boundary conditions,
branching (topological) errors changed the decision in 32--33\% of models and the half-voxel throat error in
30--36\%, against 6--10\% for vessel-size (caliber) errors of inter-observer magnitude away from the throat.
Re-derived or tuned boundary conditions reduced topological flips to 5--19\% but not throat flips. Tuned
models passed a perfusion check stricter than measurement repeatability while wrong by more than 0.05: 19--20\%
(discrete bed) and 5--8\% (leaky bed) of topological-error models, 4--18\% of other caliber-error models and
57--81\% of throat-error models, against 3--4\% for correct anatomy; with finer territories, topological
concealment fell to 2--7\% and throat concealment did not. A missed branch and a taper had the same DSC (0.97).
Per-territory tuning corrected the typical missed branch. A perfusion match after tuning did not certify the
segmented branching or caliber.
```

Word count: 248, counted as whitespace tokens on the LaTeX source, the same basis on which the current abstract counts 250. The demand sentence and the 3D numbers leave the abstract; both results stand in III-D, III-E and the supplement. Each OLD block in this file is to be matched without its final line break (the fenced block adds one).

## 3. Main-text changes

### 3.1 Introduction: sensitivity sentence (+1 line)

OLD:
```old
Sensitivity analyses perturb the radius at fixed bifurcations and report a continuous change in the computed pressure index \cite{sankaran2015tmi,sankaran2015cmame,fernandez2024,dalmaso2025}.
```
NEW:
```new
Sensitivity analyses perturb the radius at fixed bifurcations and report a continuous change in the computed pressure index \cite{sankaran2015tmi,sankaran2015cmame,fernandez2024,dalmaso2025}; the sensitivity peaks at the minimal lumen, rises with stenosis severity \cite{fernandez2024} and depends on the downstream boundary conditions \cite{sankaran2015tmi}.
```

### 3.2 Introduction: contribution paragraph (+2 lines)

OLD:
```old
We propose a controlled test, an ablation that introduces one segmentation error at a time into an otherwise correct
model, whose FFR is the reference. It judges each error by the decision at 0.80 against the variability of repeat
invasive FFR; solves the same corrupted anatomy under fixed, re-derived and tuned boundary conditions in two
microvascular bed structures; and counts how often a model passes a perfusion check while its FFR is materially wrong,
with a 3D computational fluid dynamics (CFD) case as a check.
```
NEW:
```new
We propose a controlled test, an ablation that introduces one segmentation error at a time into an otherwise correct
model, whose FFR is the reference. It judges each error, in the branching, in the caliber away from the lesion and
at the stenosis throat, by the decision at 0.80 against the variability of repeat invasive FFR; solves the same
corrupted anatomy under fixed, re-derived and tuned boundary conditions in two microvascular bed structures; counts
how often a model passes a perfusion check, at two territory resolutions, while its FFR is materially wrong; and
measures what overlap scores and the pre-tuning mismatch show of these errors, with a 3D computational fluid
dynamics (CFD) case as a check.
```

### 3.3 Fig. 1 caption (0 lines)

OLD:
```old
\caption{The four segmentation error types on one cohort tree (left coronary tree of scan 14, front view, line width
proportional to radius).
```
NEW:
```new
\caption{Four of the five segmentation error types on one cohort tree (left coronary tree of scan 14, front view, line width
proportional to radius); the fifth (T5) changes only the throat radius of the lesion in (a).
```

### 3.4 II-C: T5 definition (+5 lines)

OLD:
```old
Four error types were applied to each instance with its lesion in place (Fig.~\ref{fig:design}). Two are
topological errors, which change which vessels exist. Two are caliber errors, which change the lumen size or lesion
extent while the branching is unchanged.
```
NEW:
```new
Five error types were applied to each instance with its lesion in place (Fig.~\ref{fig:design}). Two are
topological errors, which change which vessels exist. Three are caliber errors, which change the lumen size or lesion
extent while the branching is unchanged.
```

OLD:
```old
edge of the lesion onwards and in every descendant vessel. For T3 and T4 the set of modeled nodes is fixed to that
of the clean tree, so a narrowed radius does not remove an outlet.
```
NEW:
```new
edge of the lesion onwards and in every descendant vessel. The throat error (T5) re-inserts the same lesion with its
throat diameter narrowed or widened by half the in-plane voxel size of the scan (median 0.35~mm), each sign a
separate model; a secondary magnitude of $\pm 10$ points of DS, within the disagreement between CT and invasive
angiography on diameter stenosis (standard deviation 12--15 points) \cite{boogers2010,gouya2009}, is reported in the
Supplementary Material. For T3, T4 and T5 the set of modeled nodes is fixed to that
of the clean tree, so a narrowed radius does not remove an outlet.
```

OLD:
```old
The caliber magnitudes are the inter-observer statistics of the test split, so each caliber error is as large as
the disagreement between two annotators. HD95 (2.46~mm), used as a proxy for the disagreement in lesion extent, sets T3. The DSC of 92.8\% sets T4 as the radius
ratio $\lambda$ of two coaxial cylinders, $2\lambda^2/(\lambda^2+1) = 0.928$. Because both annotators edited the same automatically
generated centerlines, the dataset authors describe the inter-observer DSC as an upper bound on agreement \cite{bransby2026}. T1 and T2 have
no measured magnitude and are design choices, so the topological results are conditional on them. Nodes of the corrupted tree were matched to the clean tree by
coordinate, and FFR was read at the same point.
```
NEW:
```new
The T3 and T4 magnitudes are the inter-observer statistics of the test split, so each is as large as
the disagreement between two annotators. HD95 (2.46~mm), used as a proxy for the disagreement in lesion extent, sets T3. The DSC of 92.8\% sets T4 as the radius
ratio $\lambda$ of two coaxial cylinders, $2\lambda^2/(\lambda^2+1) = 0.928$. Because both annotators edited the same automatically
generated centerlines, the dataset authors describe the inter-observer DSC as an upper bound on agreement \cite{bransby2026}. The half-voxel
throat error, below the resolution of the mask, changed the throat radius by a median of 0.088~mm and DS by 7.3 points (4.5--9.8). T1 and T2 have
no measured magnitude and are design choices, so the topological results are conditional on them. Nodes of the corrupted tree were matched to the clean tree by
coordinate, and FFR was read at the same point.
```

### 3.5 II-D: bound-fit sentences and the finer partition (+3 lines)

OLD:
```old
of $C_\mathrm{b}$, then refined it; a fit at the edge of the range was a failure (none occurred).
```
NEW:
```new
of $C_\mathrm{b}$, then refined it; a fit at the edge of the range was a failure and was excluded (two half-voxel throat-error models, one per bed).
```

OLD:
```old
own factor, fitted (within $10^{\pm 3}$) so that every territory flow equals its clean target. With one parameter per target the fit is
exactly determined, the most flexible tuning to territory flows.
```
NEW:
```new
own factor, fitted (within $10^{\pm 3}$) so that every territory flow equals its clean target; a fit at this bound keeps a defined residual and is retained. With one parameter per target the fit is
exactly determined, the most flexible tuning to territory flows.
```

OLD:
```old
For every protocol we computed the perfusion residual, the root mean square of the relative differences between the
model's territory flows and the clean targets. It is the mismatch that a perfusion check reports.
```
NEW:
```new
For every protocol we computed the perfusion residual, the root mean square of the relative differences between the
model's territory flows and the clean targets. It is the mismatch that a perfusion check reports. Protocols C and D
were also repeated with each main-branch territory divided again at its own first bifurcation (a median of four
territories in the discrete bed and five in the leaky bed), with a territory left without a vessel counted as a
100\% mismatch.
```

Note: II-C's sentence "Because the topology and reference radii are unchanged, Protocol B equals Protocol A for T5" is carried by the III-A text ("by construction"); no II-D sentence is needed.

### 3.6 II-F: overlap and detector outcomes (+3 lines)

OLD:
```old
\cite{petraco2013}.

Proportions are reported with Wilson 95\% confidence intervals (CIs).
```
NEW:
```new
\cite{petraco2013}. Each corrupted tree was also scored against its clean tree by the DSC and clDice \cite{shit2021} of a
tube model of cylinders, and the perfusion residual before tuning (Protocol B) was evaluated as a detector of
topological error against correct anatomy with noisy targets, by the area under the receiver operating
characteristic curve (AUC) and the false-alarm rate at the 10\% check.

Proportions are reported with Wilson 95\% confidence intervals (CIs).
```

### 3.7 III-A: Table I rows and note (+4 table rows, about +8 column lines; note +1)

OLD:
```old
 & D & 97 & 14 (9--23) & 36 (27--46) & 150 & 5 (2--9) & 8 (5--13) \\
\bottomrule
```
NEW:
```new
 & D & 97 & 14 (9--23) & 36 (27--46) & 150 & 5 (2--9) & 8 (5--13) \\
\addlinespace[2pt]
T5 & A & 194 & 30 (24--37) & 29 (23--36) & 300 & 36 (31--42) & 42 (37--48) \\
 & B & 194 & 30 (24--37) & 29 (23--36) & 300 & 36 (31--42) & 42 (37--48) \\
 & C & 193 & 38 (31--45) & 57 (50--64) & 299 & 37 (32--43) & 69 (63--74) \\
 & D & 194 & 40 (33--47) & 80 (74--85) & 300 & 38 (33--44) & 81 (76--85) \\
\bottomrule
```

OLD:
```old
bed and to 100 under A and B in the leaky bed. T2 was not applicable to one instance per bed; under A it removed every bed node in 36 discrete and 2 leaky instances, whereas under B the new vessel end carries outflow. Wilson 95\% intervals in parentheses. The expected flip
rate from repeat invasive measurement is 5.0--6.5\% across cells.}
```
NEW:
```new
bed and to 100 under A and B in the leaky bed. T2 was not applicable to one instance per bed; under A it removed every bed node in 36 discrete and 2 leaky instances, whereas under B the new vessel end carries outflow. T5 pools the narrower and the wider half-voxel throat error (two models per instance); Protocols A and B coincide for T5 by construction, and one Protocol C fit per bed ended at its search bound and is excluded. Wilson 95\% intervals in parentheses. The expected flip
rate from repeat invasive measurement is 5.0--6.5\% across cells.}
```

### 3.8 III-A text (+5 lines)

OLD:
```old
Topological errors changed the decision more often than caliber errors under Protocols A--C in both beds
(Table~\ref{tab:results}). With fixed boundary conditions in the discrete bed, 45 of 137 topological-error models
(33\%, 95\% CI 26--41\%) crossed 0.80, against 20 of 194 caliber-error models (10\%, 7--15\%). In the leaky bed the
proportions were 32\% (26--38\%) and 6\% (4--9\%) (paired sign test, $p \leq 0.002$ in both beds). Under
Protocols B and C the difference kept its direction. It was significant in the discrete bed
($p = 0.013$ and 0.002) but not in the leaky bed ($p = 0.18$ and 0.057). Under Protocol D the two classes
flipped at similar rates (8\% and 11\% discrete, 6\% and 4\% leaky). Flips were concentrated in the bands adjacent to 0.80 (Fig.~\ref{fig:band}). All 2\,599 corrupted-model solves under Protocols A--C and 769 under Protocol D converged (maximum mass-conservation error $9\times10^{-9}$).

The caliber errors rarely changed the decision. At the magnitude of inter-observer disagreement they changed FFR by
```
NEW:
```new
Topological errors changed the decision more often than caliber errors away from the throat under Protocols A--C in both beds
(Table~\ref{tab:results}). With fixed boundary conditions in the discrete bed, 45 of 137 topological-error models
(33\%, 95\% CI 26--41\%) crossed 0.80, against 20 of 194 lesion-length and taper models (10\%, 7--15\%). In the leaky bed the
proportions were 32\% (26--38\%) and 6\% (4--9\%) (paired sign test, $p \leq 0.002$ in both beds). Under
Protocols B and C the difference kept its direction. It was significant in the discrete bed
($p = 0.013$ and 0.002) but not in the leaky bed ($p = 0.18$ and 0.057). Under Protocol D the two classes
flipped at similar rates (8\% and 11\% discrete, 6\% and 4\% leaky). The half-voxel throat error crossed 0.80 in
30\% (24--37\%) and 36\% (31--42\%) of models with fixed boundary conditions, as often as the topological errors on
the same instances (paired sign test, $p = 1.0$ and 0.46) and more often than the other caliber errors ($p < 0.01$
for each sign and bed); every flip followed the sign of the error, and about half ended beyond the 0.75--0.85 grey
zone. Re-derived boundary conditions coincide with fixed ones for this error by construction, and tuning left its
flip rate at 37--40\%. Flips were concentrated in the bands adjacent to 0.80 (Fig.~\ref{fig:band}). All corrupted-model solves converged (maximum mass-conservation error $9\times10^{-9}$).

The caliber errors away from the throat rarely changed the decision. At the magnitude of inter-observer disagreement they changed FFR by
```

Note: the solve counts (2 599 and 769) are dropped from the sentence because they no longer cover T5; the supplement exclusions section carries the counts (§5.5).

### 3.9 III-B: throat and granularity passes-and-wrong; merge of III-C (+6 lines in III-B, −8 for III-C)

OLD:
```old
the median $|\Delta\mathrm{FFR}|$ of topological-error models fell to 0.005 in both beds, and their flip rate to 8\%
(discrete) and 6\% (leaky).
```
NEW:
```new
the median $|\Delta\mathrm{FFR}|$ of topological-error models fell to 0.005 in both beds, and their flip rate to 8\%
(discrete) and 6\% (leaky). For the missed branch, which raised FFR by a median of 0.095 (discrete) and 0.047
(leaky) with fixed boundary conditions, Protocol C reduced the shift to 0.077 and 0.015 (Wilcoxon signed-rank,
$p < 0.001$ in both beds) and Protocol D to 0.000 and 0.004, with 10 of 44 and 3 of 71 instances still above 0.05.
```

OLD:
```old
Looser thresholds of 13\% and 16\% raised the proportions (Supplementary Material).

Tuning also turned caliber errors into passes-and-wrong. With re-derived boundary conditions no caliber-error model
passed while materially wrong in either bed. After tuning, 5\% (C) and 18\% (D) did so in the discrete bed and 12\%
and 4\% in the leaky bed (McNemar against B, $p \leq 0.004$ in all four comparisons). Almost all were taper models
in which tuning lowered FFR: forcing the clean flow through a uniformly narrowed lumen raises its pressure drop
(Table~\ref{tab:results}).
```
NEW:
```new
Looser thresholds of 13\% and 16\% raised the proportions (Supplementary Material).

Tuning also turned caliber errors into passes-and-wrong. With re-derived boundary conditions no lesion-length or taper model
passed while materially wrong in either bed. After tuning, 5\% (C) and 18\% (D) did so in the discrete bed and 12\%
and 4\% in the leaky bed (McNemar against B, $p \leq 0.004$ in all four comparisons). Almost all were taper models
in which tuning lowered FFR: forcing the clean flow through a uniformly narrowed lumen raises its pressure drop
(Table~\ref{tab:results}). The throat error was the least visible to the check. With fixed or re-derived boundary
conditions 29\% (discrete) and 42\% (leaky) of half-voxel throat-error models passed while materially wrong, after
Protocol C 57\% and 69\%, and after Protocol D 80\% and 81\%, with a median $|\Delta\mathrm{FFR}|$ of 0.11--0.16;
tuning moved FFR further from the clean value because the clean territory flow was forced through a wrong throat.
With each main-branch territory divided again at its first bifurcation, topological passes-and-wrong fell to 7\%
(C) and 3\% (D) in the discrete bed and to 5\% and 2\% in the leaky bed, near the 3--4\% of correct anatomy at
main-branch level, whereas taper passes-and-wrong rose under Protocol D to 23\% and 9\% and throat passes-and-wrong
fell by at most 9 points, to 51--60\% (C) and 78--81\% (D), with flip rates unchanged (Supplementary Material).
```

OLD (whole of III-C, removed):
```old
\subsection{Side-Branch Loss Under Fixed and Tuned Resistance}
A missed side branch raised the computed FFR. In the 44 (discrete) and 71 (leaky) instances in which tuning was
defined, it raised FFR by a median of 0.095 and 0.047 with fixed boundary conditions. Protocol C reduced the shift to
0.077 and 0.015 (Wilcoxon signed-rank, $p < 0.001$ in both beds; Fig.~S3 in the Supplementary Material), and Protocol
D to 0.000 and 0.004, but 10 of 44 and 3 of 71 instances remained above 0.05 after Protocol D.

\subsection{Three-Dimensional Case Study}
```
NEW:
```new
\subsection{Overlap Scores and the Pre-Tuning Mismatch}
In a tube model of each tree, the missed branch and the taper had the same median DSC (0.97), although the missed
branch changed the decision about twice as often (27\% against 13\% discrete, 18\% against 9\% leaky); a vessel
break lowered the DSC to 0.89, and to 0.62 in the right coronary artery, and clDice fell only for topological
errors. Of the decision-changing topological errors, 91\% (discrete) and 62\% (leaky) kept a whole-scan DSC at or
above the inter-observer 0.928; within topological errors the AUC of the DSC for a decision change was 0.54 and
0.70. The perfusion residual before tuning separated topological errors from correct anatomy with noisy targets in
the discrete bed only (AUC 0.77 against 0.22), flagging 83\% of them and 48\% of correct models at the 10\% check.

\subsection{Three-Dimensional Case Study}
```

### 3.10 IV-A (+4 lines)

OLD:
```old
With fixed boundary conditions, the decision risk of segmentation lay mainly in the branching
structure of the lumen: a topological error changed the decision at 0.80 three to six times as often as a caliber
error of inter-observer magnitude, whose flip rates were of the order of repeat invasive measurement. This ranking
holds for the magnitudes studied; no error type perturbed the stenosis throat alone.

Re-deriving or tuning the bed reduced topological flips from 18--43\% to 2--20\% per error type. Per-territory
tuning restored the flow that the missing branch had carried through the stenosis, in the cohort and in the 3D case, by construction of its targets.
```
NEW:
```new
With fixed boundary conditions, the decision risk of segmentation lay in the branching and at the stenosis throat:
a missed branch, a vessel break or a half-voxel error in throat diameter each changed about a third of decisions in
this threshold-stratified cohort, whereas caliber errors of inter-observer magnitude away from the throat changed
decisions at rates of the order of repeat invasive measurement. The throat result agrees with sensitivity analyses
in which the computed pressure index responds most to the minimal lumen, increasingly so with stenosis severity
\cite{sankaran2015tmi,fernandez2024}; the present test adds the effect on the decision and the interaction with
tuning. These rates hold for the magnitudes studied.

Re-deriving or tuning the bed reduced topological flips from 18--43\% to 2--20\% per error type and left throat
flips unchanged. Per-territory
tuning restored the flow that the missing branch had carried through the stenosis, in the cohort and in the 3D case, by construction of its targets.
```

OLD:
```old
caliber errors into passing models with a wrong FFR, which re-derivation did not, because restoring the clean flow through a narrowed lumen enlarges
its pressure drop. The check measured agreement with the fitted targets, not the correctness of the model. The leaky
bed damped topological errors, and their excess of passes-and-wrong over re-derived boundary conditions held only in
the discrete bed.
```
NEW:
```new
caliber errors into passing models with a wrong FFR, because restoring the clean flow through a narrowed lumen enlarges
its pressure drop; for the throat error, which the check did not see even before tuning, it did so in 57--81\% of models. The check measured agreement with the fitted targets, not the correctness of the model. A check one
branching level finer removed most topological passes-and-wrong but few throat or taper ones. The leaky
bed damped topological errors, and their excess of passes-and-wrong over re-derived boundary conditions held only in
the discrete bed.
```

### 3.11 IV-B: overlap sentence (0 lines)

OLD:
```old
Vessel breaks occur in the output of current segmentation methods despite high overlap scores \cite{bransby2026},
and a missing side branch removes few voxels, so the error types that carried the decision risk here are the ones that the usual overlap metrics do not measure, although topology-aware measures such as clDice
exist \cite{shit2021}.
```
NEW:
```new
Vessel breaks occur in the output of current segmentation methods despite high overlap scores \cite{bransby2026}.
In our tube model a missed branch left the DSC as high as a taper did while changing the decision twice as often,
and a vessel break lowered the whole-scan DSC below the inter-observer value only in the right coronary artery, so
overlap scores, including the topology-aware clDice \cite{shit2021}, did not rank these errors by decision risk.
```

### 3.12 IV-C: practical considerations (+1 line)

OLD:
```old
For a user who computes FFR from an image, the results suggest four considerations. First, especially with fixed boundary conditions, check that the side branches
beyond the lesion are present and that no vessel ends early, because overlap scores do not reveal these errors.
Second, if the boundary conditions are tuned to perfusion, check the lumen caliber as well: diameter errors of
inter-observer size flipped decisions at rates near repeat invasive measurement (the taper up to 14\%), but after
tuning they produced passing models with a wrong FFR. Third, record the perfusion mismatch before tuning, which erases it: in the discrete bed
only 22\% of re-derived topological-error models passed, although in the leaky bed most did. Fourth, take most care near 0.80. These considerations are not validated decision rules.
```
NEW:
```new
For a user who computes FFR from an image, the results suggest four considerations. First, check that the side branches
beyond the lesion are present and that no vessel ends early, because a missed branch leaves the overlap score as high as a taper does.
Second, check the lumen caliber, above all the throat diameter: caliber errors of
inter-observer size away from the throat flipped decisions at rates near repeat invasive measurement (the taper up to 14\%), a half-voxel throat error flipped 30--36\%, and after
tuning both produced passing models with a wrong FFR. Third, record the perfusion mismatch before tuning: it marked topological errors only in the discrete bed (AUC 0.77), and half of the correct models with noisy targets exceeded 10\%. Fourth, take most care near 0.80. These considerations are not validated decision rules.
```

### 3.13 IV-D: Limitations (+2 lines)

OLD:
```old
effects. The missed-branch and vessel-break magnitudes are design choices, and the caliber magnitudes come from
inter-observer statistics that likely overstate agreement.
```
NEW:
```new
effects. The missed-branch and vessel-break magnitudes are design choices, and the lesion-length and taper magnitudes come from
inter-observer statistics that likely overstate agreement. The throat magnitudes are half a voxel and $\pm 10$
points of DS; validated clinical computation of FFR from CT includes an expert review of the lumen before
simulation \cite{norgaard2014}, so the throat rates describe an error that reaches the model unreviewed.
```

OLD:
```old
direction or its reduction by prescribed flows. A caliber error of this size at the throat may therefore matter as much as a topological one. No invasive FFR was available, so the noise floor was modeled from published repeat
measurements. Errors were applied one at a time in one dataset; caliber errors only narrowed or lengthened the lumen; microvascular
dysfunction, collaterals and links between error and lesion morphology were not modeled. A segment-level perfusion
check could detect errors within a main-branch territory that this one cannot. Tuning targets were error-free clean-model flows
(noise entered only the simulated floor).
```
NEW:
```new
direction or its reduction by prescribed flows. No invasive FFR was available, so the noise floor was modeled from published repeat
measurements. Errors were applied one at a time in one dataset; caliber errors away from the throat only narrowed or lengthened the lumen; microvascular
dysfunction, collaterals and links between error and lesion morphology were not modeled. A perfusion check one
branching level finer detected most topological errors that passed at main-branch level, but not throat or taper
errors; the noise floor was computed at main-branch level only. Tuning targets were error-free clean-model flows
(noise entered only the simulated floor).
```

The clause on expert review cites norgaard2014; the operator should confirm against the NXT methods (FFR computed centrally by trained analysts) before applying.

### 3.14 Conclusion (+2 lines)

OLD:
```old
perfusion is not necessarily a correct one. With fixed boundary conditions, missed branches and vessel breaks changed the decision three to six times
as often as caliber errors of inter-observer size, for the magnitudes studied; re-derived from the segmented tree, as in automated pipelines, the boundary conditions lowered topological decision changes to 5--18\% per error type. Tuning the boundary conditions to perfusion reduced these
changes without making the models correct: in the discrete bed, up to one in five tuned topological-error models (5--8\% in the leaky bed) passed a main-branch perfusion check stricter than
measurement repeatability while their FFR was materially wrong, against 3--4\% for correct anatomy. The results
point to where safeguards are likely to matter most: a check of the branching near the lesion, which overlap scores miss, and
a record of the perfusion mismatch before tuning, which tuning erases. The same test can be adapted to other
pipelines, including coronary digital twins calibrated to perfusion.
```
NEW:
```new
perfusion is not necessarily a correct one. With fixed boundary conditions, a missed branch, a vessel break or a
half-voxel error in throat diameter each changed about a third of decisions in this threshold-stratified cohort, whereas caliber errors of inter-observer size away from the throat
changed decisions at rates near repeat invasive measurement; re-derived from the segmented tree, as in automated pipelines, the boundary conditions lowered topological decision changes to 5--18\% per error type and throat decision changes not at all. Tuning the boundary conditions to perfusion reduced topological
changes without making the models correct: in the discrete bed, up to one in five tuned topological-error models (5--8\% in the leaky bed) and 57--81\% of throat-error models in both beds passed a main-branch perfusion check stricter than
measurement repeatability while their FFR was materially wrong, against 3--4\% for correct anatomy. The results
point to where safeguards are likely to matter most: a check of the branching near the lesion and of the throat diameter, which overlap scores do not rank by decision risk, and,
for discrete beds, a record of the perfusion mismatch before tuning. The same test can be adapted to other
pipelines, including coronary digital twins calibrated to perfusion.
```

### 3.15 Methods cuts (−10 lines)

**Eligibility (II-A), −3 lines.** Moved to supplement S1 (§4).

OLD:
```old
otherwise unchanged tree. An instance is one lesion in one tree. Its clean model is the lesioned tree with no segmentation error. A host vessel (left anterior descending, LAD; left circumflex, LCx; or right coronary artery, RCA) was eligible
when image quality was at least adequate (2 on a 0--4 scale), the taper-fit radius $r_\mathrm{fit}$ (a linear fit of radius along the vessel) at the
lesion center was at least 1.0~mm, native narrowing relative to $r_\mathrm{fit}$ was below 40\% diameter stenosis (DS),
the measurement point 20~mm beyond the lesion lay on a vessel of radius at least 0.75~mm, and the FFR before
insertion was at least 0.90. The lesion is an axisymmetric cosine narrowing (Supplementary Material),
```
NEW:
```new
otherwise unchanged tree. An instance is one lesion in one tree. Its clean model is the lesioned tree with no segmentation error. A host vessel (left anterior descending, LAD; left circumflex, LCx; or right coronary artery, RCA) was eligible
when image quality was at least adequate, the taper-fit radius $r_\mathrm{fit}$ (a linear fit of radius along the vessel) at the
lesion center was at least 1.0~mm, native narrowing was below 40\% diameter stenosis (DS) and the FFR before
insertion was at least 0.90 (full criteria in the Supplementary Material). The lesion is an axisymmetric cosine narrowing,
```

**Demand calibration (II-B), −3 lines.** Moved to supplement S4.2.

OLD:
```old
the inlet radius. With the model setting $k = 562$~s$^{-1}$, a
vessel with the normal proximal LAD diameter of 3.7~mm \cite{dodge1992} carries 214~mL/min,
within one standard deviation of the hyperemic flow measured in that artery by continuous thermodilution
($228 \pm 71$ to $293 \pm 102$~mL/min) \cite{fournier2021}. The segmented arteries were narrower than these
normal values (median inlet radius 1.60~mm), so the cohort's median demand was 2.28~mL/s (137~mL/min) per tree, and
the full pipeline was repeated with $k$ doubled and tripled; FFR was also recomputed on the same cohort with $k$ scaled by 0.7 and 1.3. Reference radii and $C_\mathrm{b}$ are computed from the original tree, so an inserted lesion changes
```
NEW:
```new
the inlet radius. With $k = 562$~s$^{-1}$, a normal proximal LAD (diameter 3.7~mm \cite{dodge1992}) carries
214~mL/min, within one standard deviation of thermodilution measurements \cite{fournier2021}; because the segmented
arteries were narrower (median inlet radius 1.60~mm), the cohort's median demand was 137~mL/min per tree, and the
pipeline was repeated with $k$ doubled and tripled and with $k$ scaled by 0.7 and 1.3 (Supplementary Material). Reference radii and $C_\mathrm{b}$ are computed from the original tree, so an inserted lesion changes
```

**3D mesh and solver (II-E), −4 lines.** Moved to supplement S7.

OLD:
```old
lesion and the missed branch (T1). Surfaces were extracted from the mask by marching cubes and Taubin smoothing; the
lesion was applied by moving surface vertices radially with (1), and the branch was removed by deleting its voxels.
Meshes of 3.5--3.9 million cells (cfMesh) had 25~\textmu m cells within $\pm 4$~mm of the throat and four boundary
layers.

Steady laminar Newtonian flow, with the viscosity and density of the reduced-order model, was solved with OpenFOAM
(simpleFoam, ESI v2406; SIMPLE coupling; bounded second-order upwind convection). Each solve ran
3\,000 iterations; convergence required scaled residuals below $10^{-5}$ and a steady pressure at the measurement
point. The walls were rigid with no slip, and the inlet carried aortic pressure. Each outlet either set its pressure
```
NEW:
```new
lesion and the missed branch (T1). Surfaces were extracted from the mask, the
lesion was applied by moving surface vertices radially with (1), and the branch was removed by deleting its voxels.
Meshes of 3.5--3.9 million cells had 25~\textmu m cells within $\pm 4$~mm of the throat (mesh and solver settings in the Supplementary Material).
Steady laminar Newtonian flow, with the viscosity and density of the reduced-order model, was solved with OpenFOAM
(simpleFoam) to scaled residuals below $10^{-5}$ and a steady pressure at the measurement
point. The walls were rigid with no slip, and the inlet carried aortic pressure. Each outlet either set its pressure
```

## 4. Where the moved Methods passages go in supplement.tex

| Passage | Destination | Text to add |
|---|---|---|
| Eligibility details | S1 Analysis Pipeline, after the paragraph beginning "Cohort selection (step 3) shuffles" (before `\begin{figure}[!h]`) | "Host-vessel eligibility (step 2) required an image quality of at least 2 on the 0--4 scale of the dataset, a taper-fit radius $r_\mathrm{fit}$ of at least 1.0~mm at the lesion center, native narrowing relative to $r_\mathrm{fit}$ below 40\% DS over the lesion window and run-off, a measurement point 20~mm beyond the lesion on a resolved vessel of radius at least 0.75~mm, and an FFR before insertion of at least 0.90 at that point." |
| Demand calibration | S4.2 Hyperemic Demand, as a sentence before `\input{supplement_tables/tab_demand.tex}` | "With $k = 562$~s$^{-1}$, a vessel with the normal proximal LAD diameter of 3.7~mm carries 214~mL/min, within one standard deviation of the hyperemic flow measured in that artery by continuous thermodilution ($228 \pm 71$ to $293 \pm 102$~mL/min); the cohort's median demand was 2.28~mL/s (137~mL/min) per tree." (Citations dodge1992 and fournier2021 are in the main text; the supplement carries no bibliography, so the values are stated without keys, as elsewhere in the supplement.) |
| 3D mesh and solver | S7 Three-Dimensional Case Study: Mesh Checks, as the first sentences of the section | "Surfaces were extracted from the mask by marching cubes and Taubin smoothing. Meshes of 3.5--3.9 million cells (cfMesh) had 25~\textmu m cells within $\pm 4$~mm of the throat and four boundary layers. Steady laminar flow was solved with OpenFOAM simpleFoam (ESI v2406; SIMPLE coupling; bounded second-order upwind convection) for 3\,000 iterations per solve, with convergence defined as scaled residuals below $10^{-5}$ and a steady pressure at the measurement point." |

Also in supplement.tex: the title line (line 20) drops "Topological"; pipeline figure box 5 (line 56–57) becomes "T1 missed branch, T2 vessel break, T3 lesion $+2.46$~mm, T4 taper $\times 0.930$, T5 throat $\pm\tfrac12$ voxel; nodes matched by coordinate."; and S2 is corrected as in §5.5.

## 5. New supplement sections

Insert after S5 (Sensitivity Analyses, which ends with the Grey Zone subsection) and before S6 Noise Floors, so that the throat and granularity sections follow the grey-zone table they extend; the overlap and detector sections follow. Each table is written in the style of `supplement_tables/*.tex`; the bodies may be moved to `supplement_tables/tab_throat.tex`, `tab_gran.tex`, `tab_overlap.tex` and `tab_detector.tex` and pulled in with `\inputtab`, as the existing tables are.

### 5.1 S-throat

```latex
\FloatBarrier
\section{Caliber Error at the Stenosis Throat}\label{sec:throat}
The throat error (T5) re-inserts each lesion at the same center, length and node set with a changed severity: the
throat radius is changed by a quarter of the in-plane voxel size of the scan (a throat diameter error of half a voxel),
or the diameter stenosis is raised or lowered by 10 percentage points. In-plane spacing had a median of 0.352~mm
(0.295--0.449~mm), so the half-voxel error changed the throat radius by a median of 0.088~mm and the diameter stenosis
by a median of 7.3 points (4.5--9.8). The $\pm 10$-point magnitude lies within the published disagreement between CT
and invasive angiography on diameter stenosis (standard deviation of the difference 12.3--12.4 points per vessel and
patient; 95\% limits of agreement $-27.3$ to $+29.9$ points for intermediate stenoses). No severity required clipping
to 5--95\%. An increased stenosis lowers FFR and a reduced stenosis raises it, so each sign is reported separately and
pooled (Table~\ref{tab:throat}). Because the topology and the reference radii are unchanged, Protocol B re-derives
the clean bed and gives the same result as Protocol A. With fixed boundary conditions the pooled half-voxel error
changed the decision in 30\% (discrete) and 36\% (leaky) of models and the pooled $\pm 10$-point error in 40\% and
42\%, against 33\% and 32\% for topological errors on the same instances (paired sign test on per-instance
proportions, $p = 1.0$ and 0.46 at half a voxel, $p = 0.21$ and 0.012 at $\pm 10$ points). Every flip followed the
sign of the error. Tuning moved FFR further from the clean value, because the clean territory flow was forced through
a wrong throat. Protocol C fits reached the search bound in two half-voxel and eight $\pm 10$-point models with an
increased stenosis and were excluded. Protocol D fits reached the parameter bound in 54 discrete-bed and 10
leaky-bed models with an increased stenosis (23 at half a voxel), all but two with a clean FFR at or below 0.80;
43 failed the check and the 21 that passed were materially wrong. They were retained as in Table~I; excluding them
would raise the Protocol D passes-and-wrong rates by up to 13 points.
\begin{table}[!ht]
\caption{Throat Caliber Error: Flips, Passes-and-Wrong and Flips Beyond the Grey Zone, \% of Models (Wilson 95\% Interval)}\label{tab:throat}
\centering\footnotesize\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}llrccc rccc@{}}
\toprule
 & & \multicolumn{4}{c}{Discrete bed (97 instances)} & \multicolumn{4}{c}{Leaky bed (150 instances)}\\
\cmidrule(lr){3-6}\cmidrule(l){7-10}
Error & Protocol & $n$ & Flip & Passes and wrong & Beyond zone & $n$ & Flip & Passes and wrong & Beyond zone\\
\midrule
Throat $-\tfrac12$ voxel & A, B & 97 & 28 (20--37) & 26 (18--35) & 16 (10--25) & 150 & 25 (19--33) & 43 (36--51) & 15 (10--22) \\
 & C & 96 & 30 (22--40) & 49 (39--59) & 23 (16--32) & 149 & 26 (19--33) & 68 (61--75) & 21 (15--28) \\
 & D & 97 & 30 (22--40) & 84 (75--90) & 25 (17--34) & 150 & 27 (21--35) & 91 (85--94) & 19 (14--26) \\
\addlinespace[2pt]
Throat $+\tfrac12$ voxel & A, B & 97 & 32 (24--42) & 32 (24--42) & 12 (7--20) & 150 & 47 (39--55) & 41 (34--49) & 26 (20--34) \\
 & C & 97 & 45 (36--55) & 65 (55--74) & 21 (14--30) & 150 & 49 (41--57) & 69 (61--76) & 38 (31--46) \\
 & D & 97 & 49 (40--59) & 77 (68--85) & 28 (20--37) & 150 & 49 (41--57) & 71 (64--78) & 39 (31--47) \\
\addlinespace[2pt]
$\pm\tfrac12$ voxel pooled & A, B & 194 & 30 (24--37) & 29 (23--36) & 14 (10--20) & 300 & 36 (31--42) & 42 (37--48) & 21 (16--26) \\
 & C & 193 & 38 (31--45) & 57 (50--64) & 22 (17--28) & 299 & 37 (32--43) & 69 (63--74) & 29 (25--35) \\
 & D & 194 & 40 (33--47) & 80 (74--85) & 26 (21--33) & 300 & 38 (33--44) & 81 (76--85) & 29 (24--34) \\
\addlinespace[2pt]
DS $+10$ & A, B & 97 & 34 (25--44) & 11 (6--19) & 30 (22--40) & 150 & 34 (27--42) & 31 (24--38) & 26 (20--34) \\
 & C & 90 & 39 (29--49) & 34 (25--45) & 34 (25--45) & 149 & 36 (29--44) & 49 (41--57) & 32 (25--39) \\
 & D & 97 & 38 (29--48) & 65 (55--74) & 33 (24--43) & 150 & 37 (30--45) & 91 (86--95) & 31 (24--38) \\
\addlinespace[2pt]
DS $-10$ & A, B & 97 & 45 (36--55) & 29 (21--39) & 25 (17--34) & 150 & 50 (42--58) & 49 (41--57) & 43 (36--51) \\
 & C & 97 & 49 (40--59) & 66 (56--75) & 39 (30--49) & 150 & 50 (42--58) & 74 (66--80) & 50 (42--58) \\
 & D & 97 & 52 (42--61) & 85 (76--90) & 47 (38--57) & 150 & 50 (42--58) & 80 (73--86) & 50 (42--58) \\
\addlinespace[2pt]
DS $\pm10$ pooled & A, B & 194 & 40 (33--47) & 20 (15--26) & 27 (22--34) & 300 & 42 (37--48) & 40 (34--45) & 35 (30--40) \\
 & C & 187 & 44 (37--52) & 51 (44--58) & 37 (30--44) & 299 & 43 (38--49) & 62 (56--67) & 41 (35--46) \\
 & D & 194 & 45 (38--52) & 75 (68--80) & 40 (34--47) & 300 & 44 (38--49) & 86 (81--89) & 40 (35--46) \\
\bottomrule
\end{tabular}
\\[3pt]
\parbox{0.95\textwidth}{\footnotesize Throat $\mp\tfrac12$ voxel: throat diameter narrowed or widened by half the in-plane voxel size. DS $\pm10$: diameter stenosis raised or lowered by 10 percentage points. Passes and wrong: perfusion residual below 10\% and $|\Delta\mathrm{FFR}| > 0.05$. Beyond zone: flips whose corrupted FFR lies outside 0.75--0.85. Protocols A and B coincide for throat errors. Protocol C fits on the search bound are excluded, which reduces $n$. For comparison, topological errors under Protocol A flipped 33\% (26--41\%) and 32\% (26--38\%) of models and caliber errors away from the throat 10\% (7--15\%) and 6\% (4--9\%).}
\end{table}
```

### 5.2 S-granularity

```latex
\FloatBarrier
\section{Territory Granularity}\label{sec:granularity}
Protocols C and D were repeated with a finer partition. Each main-branch territory was divided again at its own first
bifurcation; the vessel between the two bifurcations formed a territory of its own, and an unbranched main-branch
territory was kept whole. A territory with a positive clean target and no surviving vessel entered the residual with a
relative error of $-1$; under Protocol D it carried no parameter. Trunk territories had no bed outflow in the discrete
bed and were omitted, as is the root trunk. The same models were solved at both levels, so all comparisons are paired,
and with the main-branch partition the procedure reproduced the original results exactly. Trees had a median of four
(range 2--5) territories in the discrete bed and five (2--7) in the leaky bed, against two or three. Topological
passes-and-wrong fell in the discrete bed under both protocols and rose in neither bed (Table~\ref{tab:gran}). A
territory left without a vessel failed the check (residual $\geq 0.38$) in 30 of 104 discrete and 45 of 171 leaky
topological-error models, most of which already failed or were correct at main-branch level; most of the fall came
from models with every territory perfused, in which the single scaling no longer matched the finer targets (C) or the
additional parameters restored the FFR (D). Taper passes-and-wrong did not fall: under Protocol D it rose from 36\% to
45\% (discrete) and from 8\% to 19\% (leaky). Throat errors, which leave every territory perfused, lost at most 9
points; every model removed from the count failed the finer check, none had its FFR corrected, and of the throat-error
models that passed after tuning 76--88\% remained materially wrong, against 3--29\% of topological-error models.
Flip rates under C and D changed by at most five models per cell (McNemar $p \geq 0.13$; at most two for throat
errors). Protocol D fits on the parameter bound rose to 77 discrete-bed and 30 leaky-bed throat-error models with an
increased stenosis; excluding them would raise the finer-level Protocol D rates to 81--86\%. The simulated noise floor
was computed at main-branch level only. Had a territory without a vessel been omitted from the residual, topological
passes-and-wrong would have risen to 26\% in the discrete bed.
\begin{table}[!ht]
\caption{Passes and Wrong, \% (Wilson 95\% Interval), at Main-Branch and Finer Territory Level}\label{tab:gran}
\centering\small
\begin{tabular}{@{}lllrccc@{}}
\toprule
Bed & Errors & Protocol & $n$ & Main branch & Finer & $p$\\
\midrule
Discrete & T1+T2 & C & 104 & 19 (13--28) & 7 (3--13) & $<0.001$ \\
 & & D & 104 & 20 (14--29) & 3 (1--8) & $<0.001$ \\
 & T3+T4 & C & 194 & 5 (2--9) & 5 (3--9) & 1.0 \\
 & & D & 194 & 18 (13--24) & 23 (18--30) & 0.002 \\
 & T5, $\pm\tfrac12$ voxel & A, B & 194 & 29 (23--36) & 25 (20--32) & 0.016 \\
 & & C & 193 & 57 (50--64) & 51 (44--58) & 0.003 \\
 & & D & 194 & 80 (74--85) & 78 (71--83) & 0.12 \\
 & T5, DS $\pm10$ & A, B & 194 & 20 (15--26) & 16 (12--22) & 0.016 \\
 & & C & 186 & 51 (44--58) & 45 (38--52) & $<0.001$ \\
 & & D & 194 & 75 (68--80) & 69 (62--75) & 0.002 \\
\addlinespace[2pt]
Leaky & T1+T2 & C & 171 & 8 (5--13) & 5 (2--9) & 0.07 \\
 & & D & 171 & 5 (3--10) & 2 (1--6) & 0.18 \\
 & T3+T4 & C & 300 & 12 (9--17) & 12 (9--17) & 1.0 \\
 & & D & 300 & 4 (2--7) & 9 (7--13) & $<0.001$ \\
 & T5, $\pm\tfrac12$ voxel & A, B & 300 & 42 (37--48) & 35 (30--41) & $<0.001$ \\
 & & C & 299 & 69 (63--74) & 60 (55--66) & $<0.001$ \\
 & & D & 300 & 81 (76--85) & 81 (76--85) & 1.0 \\
 & T5, DS $\pm10$ & A, B & 300 & 40 (34--45) & 33 (28--39) & $<0.001$ \\
 & & C & 299 & 62 (56--67) & 55 (50--61) & $<0.001$ \\
 & & D & 300 & 86 (81--89) & 83 (78--87) & 0.008 \\
\bottomrule
\end{tabular}
\\[3pt]
\parbox{0.85\textwidth}{\footnotesize Passes and wrong: perfusion residual below 10\% and $|\Delta\mathrm{FFR}| > 0.05$. Main branch: subtrees below each child of the first bifurcation (two or three per tree). Finer: each divided again at its own first bifurcation (median four, discrete; five, leaky). $n$ counts models with a defined residual at both levels; Protocol C fits on the search bound at either level are excluded. For throat errors the FFR of Protocols A and B is the same at both levels and only the residual changes. $p$: exact McNemar test, paired by model.}
\end{table}
```

### 5.3 S-overlap

```latex
\FloatBarrier
\section{Overlap and Topology of the Corrupted Trees}\label{sec:overlap}
Each network was represented as cylinders of the node radius and element length, and every corrupted tree was
compared with its clean lesioned tree in the same bed (a tube model; a voxel mask would differ at partial-volume
level). Corrupted node sets were contained in the clean ones for all four error types; radii were contained except in
the lesion window of some T2 and T4 trees (at most 0.04~mm), so the intersection was taken as the smaller radius on
matched nodes. No error changed the number of connected components. Table~\ref{tab:overlap} gives the medians. The
missed branch and the taper had the same DSC, although the missed branch changed the decision under Protocol A about
twice as often; a vessel break in the right coronary artery lowered tree DSC to a median of 0.62. Of the topological
errors that changed the decision, 91\% (79--96\%) in the discrete bed and 62\% (51--72\%) in the leaky bed had a
whole-scan DSC at or above the inter-observer value of 0.928. With instance-level bootstrap intervals, the AUC of tree
DSC for a Protocol A decision change was 0.79 (0.74--0.83) leaky and 0.65 (0.57--0.72) discrete across all error
types, and 0.70 (0.65--0.76) and 0.54 (0.44--0.65) within topological errors; clDice and the share of bed flow lost did
not exceed these within topological errors. The applied taper gives a DSC above 0.928 because it narrows only the
tree beyond the lesion's proximal edge (median 40\% of the tree volume).
\begin{table}[!ht]
\caption{Tube-Model Overlap of Corrupted Trees, Median (IQR), and Protocol A Decision Changes}\label{tab:overlap}
\centering\small
\begin{tabular}{@{}llrcccrc@{}}
\toprule
Bed & Error & $n$ & DSC, tree & DSC, scan & clDice & Flow lost, \% & Flip A, \% \\
\midrule
Discrete & T1 & 77 & 0.975 (0.947--0.984) & 0.985 (0.977--0.991) & 0.940 (0.903--0.963) & 27 (14--43) & 27 (19--38) \\
 & T2 & 96 & 0.893 (0.701--0.937) & 0.935 (0.888--0.960) & 0.847 (0.544--0.907) & 30 (15--100) & 40 (29--53)$^a$ \\
 & T3 & 97 & 0.996 (0.995--0.997) & 0.998 (0.998--0.998) & 1.000 & 0 & 7 (4--14) \\
 & T4 & 97 & 0.971 (0.947--0.981) & 0.983 (0.974--0.989) & 1.000 & 0 & 13 (8--22) \\
Leaky & T1 & 118 & 0.969 (0.946--0.980) & 0.983 (0.975--0.990) & 0.930 (0.899--0.957) & 9 (6--17) & 18 (12--26) \\
 & T2 & 149 & 0.895 (0.721--0.936) & 0.934 (0.886--0.962) & 0.855 (0.517--0.899) & 14 (7--56) & 43 (35--51) \\
 & T3 & 150 & 0.997 (0.995--0.998) & 0.998 (0.998--0.999) & 1.000 & 0 & 2 (1--6) \\
 & T4 & 150 & 0.972 (0.951--0.981) & 0.983 (0.976--0.988) & 1.000 & 0 & 9 (6--15) \\
\midrule
\multicolumn{3}{@{}l}{T2, right coronary artery} & 0.62--0.63 & 0.85--0.86 & 0.45--0.49 & & \\
\bottomrule
\end{tabular}
\\[3pt]
\parbox{0.85\textwidth}{\footnotesize Flip A: Wilson 95\% interval. Flow lost: share of the clean model's bed outflow on deleted nodes. $^a$ $n = 60$; right coronary breaks leave no discrete outlet under Protocol A.}
\end{table}
```

### 5.4 S-detector

```latex
\FloatBarrier
\section{Detection Before and During Tuning}\label{sec:detector}
The perfusion residual before tuning (Protocol B) and the fitted Protocol C scaling relative to its start,
$|\ln(C_\mathrm{C}/C_\mathrm{B})|$, were evaluated as detectors. Positives are error models with a defined residual;
negatives are the 20 draws per instance of the simulated floor, evaluated before tuning with the same noise model. The
AUC carries an instance-level bootstrap interval (2000 resamples); sensitivity and false-alarm rate are given at 0.10
and at the value exceeded by 5\% of the negatives (Table~\ref{tab:detector}). Without noise, correct anatomy has a
residual below $10^{-8}$; with physiological noise its median residual before tuning is 0.10, and 48\% (discrete)
and 50\% (leaky) of draws exceed 0.10. In the discrete bed the residual separated topological errors from correct
anatomy (AUC 0.77; 0.82 when the error models' targets carried the same noise); in the leaky bed the residual caused
by a topological error was smaller than that caused by noise (AUC 0.22; 0.56 with noise on both). The fitted scaling
did not separate topological errors from correct anatomy in either bed (AUC 0.47 and 0.12); in the leaky bed it
exceeded the 5\% false-alarm value in 36 of 38 taper models whose decision changed after tuning.
\begin{table}[!ht]
\caption{Detection Before and During Tuning Against Correct Anatomy With Noisy Targets}\label{tab:detector}
\centering\small\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}lllrccccc@{}}
\toprule
Bed & Quantity & Positives & $n$ & AUC & Sens.\ at 0.10, \% & FA at 0.10, \% & 5\% FA value & Sens.\ at 5\% FA, \%\\
\midrule
Discrete & Pre-tuning residual & Topological & 137 & 0.77 (0.71--0.82) & 83 (76--89) & 48 & 0.22 & 47 (39--55) \\
 &  & Flip under B$^a$ & 36 & 0.57 (0.46--0.69) & 69 (53--82) & 48 & 0.22 & 22 (12--38) \\
 & $|\ln C|$ & Topological & 104 & 0.47 (0.40--0.53) & 30 (22--39) & 37 & 0.24 & 9 (5--16) \\
 &  & Flip or P\&W under C$^a$ & 61 & 0.53 (0.44--0.62) & 41 (30--54) & 37 & 0.24 & 15 (8--26) \\
\addlinespace[2pt]
Leaky & Pre-tuning residual & Topological & 218 & 0.22 (0.18--0.27) & 19 (15--25) & 50 & 0.23 & 6 (3--9) \\
 &  & Flip under B$^a$ & 16 & 0.21 (0.08--0.36) & 12 (3--36) & 50 & 0.23 & 6 (1--28) \\
 & $|\ln C|$ & Topological & 171 & 0.12 (0.09--0.15) & 3 (1--7) & 34 & 0.24 & 2 (1--5) \\
 &  & Flip or P\&W under C$^a$ & 66 & 0.66 (0.55--0.77) & 61 (49--71) & 34 & 0.24 & 59 (47--70) \\
\bottomrule
\end{tabular}
\\[3pt]
\parbox{0.9\textwidth}{\footnotesize Negatives: 1\,940 (discrete) and 3\,000 (leaky; 2\,990 for $|\ln C|$) correct-anatomy draws on 97 and 150 instances. FA, false alarm; P\&W, passes and wrong; Sens., sensitivity. $^a$Any error type.}
\end{table}
```

### 5.5 Corrections to existing supplement text (S2 Exclusions)

OLD (supplement.tex, S2):
```old
Of 6\,944 swept instances, 150 were selected and 97 form the discrete arm; 2\,802 corrupted models were defined
(an applicable error type under each of Protocols A--C) and 2\,599 solved, all of which converged.
```
NEW:
```new
Of 6\,944 swept instances, 150 were selected and 97 form the discrete arm; 2\,802 corrupted models with error types T1--T4 were defined
(an applicable error type under each of Protocols A--C) and 2\,599 solved, all of which converged, and 494 half-voxel throat-error models were solved under each protocol, with the two Protocol C exceptions below.
```

OLD:
```old
is recorded as a failure; none did in the ablation or in the demand runs (Section~\ref{sec:demand}), and 10 of
4\,940 noise-floor draws did (Section~\ref{sec:floor}). Protocol D scales each territory within $10^{\pm 3}$; the
scaling reached $10^3$ in two discrete-bed missed-branch models of one tree, which kept perfusion residuals of 0.08 and
0.11 and $|\Delta\mathrm{FFR}| < 0.05$. They are retained, because their residuals remain defined and are scored against the check, whereas a Protocol C fit at a bound leaves its single parameter unidentified. All 769 Protocol D solves converged.
```
NEW:
```new
is recorded as a failure; none did for T1--T4 in the ablation or in the demand runs (Section~\ref{sec:demand}), two did for the half-voxel throat error (one per bed, both with a narrowed throat; Section~\ref{sec:throat}), and 10 of
4\,940 noise-floor draws did (Section~\ref{sec:floor}). Protocol D scales each territory within $10^{\pm 3}$; the
scaling reached $10^3$ in two discrete-bed missed-branch models of one tree, which kept perfusion residuals of 0.08 and
0.11 and $|\Delta\mathrm{FFR}| < 0.05$, and in 20 discrete-bed and 3 leaky-bed throat-error models with a narrowed throat, most of which failed the check (Section~\ref{sec:throat}). They are retained, because their residuals remain defined and are scored against the check, whereas a Protocol C fit at a bound leaves its single parameter unidentified. All Protocol D solves converged.
```

Note: these counts are for the half-voxel error that Table I carries; the ±10-point counts (8 C excluded, 41 D at the bound) are in S-throat. The exclusions table `tab_exclusions_nz.tex` gains two rows: "Discrete & T5 & C & 193 & Protocol C fit at search bound: 1 \\" and "Leaky & T5 & C & 299 & Protocol C fit at search bound: 1 \\".

## 6. Line budget (main text)

Measured, not estimated: column lines at 55 characters from the character counts of the OLD and NEW blocks above after whitespace normalization (script `/private/tmp/claude-501/fable_verify/budget.py`, which also confirms that all 30 OLD blocks occur exactly once in main.tex or supplement.tex). Table rows are counted as the plan does (a double-column row ≈ 2 column lines). The parenthetical estimates in the §3 headings are the plan's; this table supersedes them.

| Change | OLD chars | NEW chars | Δ column lines |
|---|---|---|---|
| 3.1 Intro sensitivity sentence | 191 | 359 | +3.1 |
| 3.2 Intro contribution paragraph | 520 | 713 | +3.5 |
| 3.3 Fig. 1 caption | 141 | 217 | +1.4 |
| 3.4 II-C (three blocks) | 1 196 | 1 757 | +10.2 |
| 3.5 II-D (three blocks) | 510 | 881 | +6.7 |
| 3.6 II-F outcomes | 89 | 475 | +7.0 |
| 3.7 Table I: 4 rows and note | 419 | 953 | +8 (rows) +2 (note) |
| 3.8 III-A text | 1 041 | 1 567 | +9.6 |
| 3.9 III-B additions, III-C merged, new overlap subsection | 1 260 | 2 801 | +28.0 |
| 3.10 IV-A (two blocks) | 1 067 | 1 608 | +9.8 |
| 3.11 IV-B overlap sentence | 345 | 455 | +2.0 |
| 3.12 IV-C | 824 | 841 | +0.3 |
| 3.13 IV-D (two blocks) | 812 | 1 112 | +5.5 |
| 3.14 Conclusion | 1 043 | 1 312 | +4.9 |
| 3.15 Methods cuts (three blocks) | 2 240 | 1 814 | −7.7 |
| **Net** | | | **about +95 column lines ≈ 0.55 page** |

The net is about 90 lines over the 3 free lines on p. 8. The plan's §3 estimate of +2 assumed insertions of one or two sentences; the content that D1–D5 and the verification flags require (throat definition with its magnitudes, two bound-fit rules, the granularity design, two new outcome measures, four Table I rows, three result sentences, the MLA framing and the norgaard clause) does not fit in that. Cuts that remove no result from the paper, each measured on the current main.tex (characters / 55):

| # | Cut | Yield |
|---|---|---|
| 1 | Drop the new III-C subsection (3.9, second block); keep the IV-B sentence (3.11) and the IV-C clause (3.12); the supplement (§5.3, §5.4) carries every number | −16 |
| 2 | Move III-E Hyperemic Demand (873 chars) to the supplement S4.3, leaving one sentence: "With $k$ doubled and tripled, the lesion insertion, cohort selection and all four protocols were repeated; the flip-rate directions held in both beds at twice and in the leaky bed at three times the demand (Supplementary Material)." | −12 |
| 3 | Move the 3D caveat paragraph "Two caveats apply ... (Supplementary Material)." (440 chars) to S7, leaving "The meshed lumen was wider than the reduced-order radius (throat 0.276 against 0.231~mm; Supplementary Material)." | −6 |
| 4 | II-F: move "Published repeatability of hyperemic myocardial blood flow ... analyzed as sensitivities." (469 chars) to S6, leaving "The 10\% threshold is stricter than published measurement repeatability, and 13\% and 16\% were analyzed as sensitivities (Supplementary Material)." | −6 |
| 5 | II-F: move the second-floor description "A second floor was simulated ... as in Protocol C." (303 chars) to S6, leaving "A second floor was simulated on the clean anatomy with physiological noise (Supplementary Material)." | −4 |
| 6 | II-B: move the solver sentences "The nonlinear equations are solved ... recorded for every solve." (241 chars) to S1, which already states them | −4 |
| 7 | II-B: move "The exponent is close to 8/3 ... perfused mass." (197 chars) to S1 | −3.5 |
| 8 | II-D: drop "They were undefined for 33 of 77 ... all but four in the RCA." (Table S1 carries the counts) | −3 |
| 9 | II-D: move "The fit minimized the mean squared relative error ... then refined it;" to S2, keeping the bound-fit clause | −2.5 |
| 10 | II-C: move the T4 derivation "The DSC of 92.8\% sets T4 as the radius ratio ... = 0.928." to S1 | −2 |
| 11 | II-F: shorten the Bayesian sentence to "A Bayesian mixed-effects logistic model agreed with the paired tests (Supplementary Material)." | −1.5 |
| 12 | III-B: drop "relative to A, Protocol C did not change them in the discrete bed ($p = 0.07$) and lowered them in the leaky bed ($p < 0.001$)" | −2.5 |
| 13 | 3.4: shorten the ±10-point clause to "a secondary magnitude of $\pm 10$ points of DS is reported in the Supplementary Material" (the citation then moves to S-throat; the supplement has no bibliography, so cite the two references in IV-D instead) | −3 |
| 14 | 3.6: shorten to "Each corrupted tree was also scored by the tube-model DSC and clDice \cite{shit2021}, and the pre-tuning perfusion residual was evaluated as a detector against correct anatomy with noisy targets (Supplementary Material)." | −3 |
| 15 | Fig. 2 height −10% and Fig. 1 width 0.93 → 0.88 (plan §3) | −5 |
| 16 | 3.13: drop "the noise floor was computed at main-branch level only" from IV-D (kept in III-B's sentence as "at main-branch level") | −1 |
| | **Total** | **about −75** |

With all sixteen cuts the net is about +20 lines, which the free lines and a further 10% reduction of Fig. 2 do not absorb. The remaining choices are: (a) shorten the III-A Protocol B paragraph ("Of Protocols A--C, re-deriving ... passed the perfusion check.", 488 chars) to its first and last sentences (−5) and the III-D 3D paragraph by its reduced-order counterpart sentence (−4); (b) drop the T5 "B" row from Table I, since it equals the A row and the note says so (−2); (c) drop the IV-A sentence that cites sankaran2015tmi and fernandez2024 and keep the citation in the Introduction (3.1) only (−4); (d) accept a 9-page main text at the $250 over-length charge. Cuts 1–16 with (a)–(c) bring the net to about +5, which Fig. 2 at −15% covers. The operator should decide between the full cut set and (d) after the first rebuild, because the measured page break, not this estimate, settles it.

Recommended set for the 10-10 integration: cuts 1–16 and (a)–(b); rebuild; then (c) only if p. 9 is still reached.

## 7. Cover letter: contribution sentences

Title line: replace ``Topological Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study'' with ``Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study''.

Second paragraph, "applied four segmentation error types" → "applied five segmentation error types, in the branching, in the caliber away from the lesion and at the stenosis throat,".

Innovation paragraph, second point: "and it separates topological errors (missing or broken vessels) from caliber errors of measured inter-observer size" → "and it separates topological errors (missing or broken vessels), caliber errors of measured inter-observer size away from the lesion and a half-voxel error at the stenosis throat". Third point, append: "It also measures what the overlap scores used to judge segmentation, and the perfusion mismatch before tuning, show of each error."

Main findings, replace the three bullets:
```latex
\item With fixed boundary conditions, a missed side branch, a vessel break or a half-voxel error in the throat
diameter each changed the treatment decision at 0.80 in about a third of models in this threshold-stratified
cohort (30--36\%), against 6--10\% for caliber errors of inter-observer magnitude away from the throat, which were
close to the variability of repeat invasive measurement.
\item Re-deriving or tuning the boundary conditions reduced topological decision changes to 5--19\% and throat
decision changes not at all. A passing check after tuning did not show that the FFR was correct: 19--20\% (discrete
bed) and 5--8\% (leaky bed) of tuned topological-error models, 4--18\% of tuned caliber-error models and 57--81\% of
tuned throat-error models passed a check stricter than measurement repeatability while their FFR was wrong by more
than 0.05, against 3--4\% for models with correct anatomy. With territories one branching level finer, the
topological figure fell to 2--7\% and the throat figure did not.
\item The overlap score did not rank these errors by decision risk: a missed branch and a taper had the same Dice
coefficient (0.97) although the missed branch changed the decision twice as often, and the perfusion mismatch before
tuning flagged topological errors only in the discrete bed, with a 48\% false-alarm rate under physiological noise.
\end{itemize}
```

Significance paragraph: "and overlap-based segmentation metrics do not capture the error types that carry the decision risk" → "and overlap-based segmentation metrics do not rank the error types by the decision risk they carry".

## 8. Number checklist

Every number in the new text, with its source. CSV paths are under `Paper6-T6/results/`; "recompute" refers to `/private/tmp/claude-501/fable_verify/recompute*.out`, all values cross-checked against the agents' reports.

| Number | Where used | Source |
|---|---|---|
| 30 (24--37), 36 (31--42): ½-voxel pooled flips, A | abstract, III-A, Table I, IV-C, conclusion, letter | `t5_throat-2026-10-09/ablation_t5.csv`, T5_vox_* rows, A_fixed, eligible discrete / leaky; recompute §T5 |
| 29 (23--36), 42 (37--48): ½-voxel pooled P&W, A and B | III-B, Table I | same, residual < 0.10 & \|ΔFFR\| > 0.05 |
| 38 (31--45), 57 (50--64), n 193; 37 (32--43), 69 (63--74), n 299: ½-voxel C | Table I, III-A/B | same, C_flowmatched (one failed fit excluded per bed) |
| 40 (33--47), 80 (74--85); 38 (33--44), 81 (76--85): ½-voxel D | Table I, III-B | `t5_throat-2026-10-09/perterritory_t5.csv` |
| 57--81%: tuned throat P&W (½ voxel, C and D, both beds) | abstract, IV-A, conclusion, letter | the four cells above (57, 69, 80, 81) |
| 37--40%: throat flips under C and D | III-A | 38, 40 (discrete), 37, 38 (leaky) |
| p = 1.0 and 0.46: sign test T1+T2 vs ½ voxel, A | III-A, S-throat | recompute: 34/33 and 40/48 discordant |
| p < 0.01 for each sign and bed vs T3+T4 | III-A | `t5_sign_tests.csv`: 1.9e-6, 0.0096, 5.8e-11, 4.1e-10 |
| about half of flips beyond grey zone | III-A | recompute: 28/58 discrete, 62/108 leaky |
| median \|ΔFFR\| 0.11 (A), 0.11--0.16 (A–D) | III-A, III-B | recompute: 0.112, 0.105; C 0.141, 0.128; D 0.162, 0.122 |
| 0.352 (0.295--0.449) mm; 0.088 mm; 7.3 (4.5--9.8) points; 0.35 mm | II-C, S-throat | `t5_magnitude.txt`; recompute |
| 40, 42%: ±10 pooled flips, A; p = 0.21, 0.012 | S-throat | `ablation_t5.csv` T5_ds_*; recompute |
| 12.3--12.4 points SD; −27.3 to +29.9 LoA; "12--15 points" | II-C, S-throat | Boogers 2010 abstract; Gouya 2009 abstract (FABLE-VERIFY §4) |
| two half-voxel + eight ±10 C failed fits; one per bed | II-D, S-throat, S2, Table I note | recompute, Table I basis: discrete narrow 1, leaky narrow 1; ds_plus10 7 + 1 |
| 54 discrete + 10 leaky D bound fits (23 at ½ voxel: 20 + 3); 43 fail, 21 pass and wrong; all but two clean-positive; +1--13 points | S-throat, S2 | recompute §3 (fab counts; 62/64 clean ≤ 0.80; excl. raises 80→83, 75→88, 81→81, 86→87) |
| 77, 30 D bound fits at Level 2; 81--86% excluding | S-granularity | `t5l2-2026-10-09/perterritory_t5_L2keep.csv`; recompute_t5l2 |
| 7%, 3% (discrete), 5%, 2% (leaky): topological P&W at Level 2 | abstract (2--7%), III-B, S-granularity | `a6_territory-2026-10-09/*_L2keep.csv`; recompute §A6 |
| 23%, 9%: caliber P&W under D at Level 2; taper 36→45, 8→19 | III-B, S-granularity | same; A6 report §3.2 by type |
| 51--60% (C), 78--81% (D): ½-voxel P&W at Level 2; "at most 9 points" | III-B, S-granularity | recompute_t5l2 (51, 60; 78, 81; largest fall 9 = leaky C 69→60) |
| 76--88% and 3--29%: P(wrong \| pass) at Level 2 | S-granularity | recompute_t5l2 (76, 81, 81, 88, 84, 82, 87; A6 29, 4, 8, 3) |
| median 4 (2--5), 5 (2--7) territories | II-D, S-granularity | `territory_counts_L2keep.csv` |
| 30 of 104, 45 of 171; residual ≥ 0.38; 26% under the drop rule | S-granularity | A6 report §3.4 (not recomputed; mechanism counts) |
| 0.97 DSC (T1 and T4); 0.89; 0.62; 27 vs 13, 18 vs 9% | abstract, III-C, IV-B, S-overlap, letter | `a5_overlap-2026-10-09/overlap_metrics.csv`; recompute §A5 |
| 91% (79--96), 62% (51--72); AUC 0.54, 0.70, 0.65, 0.79 | III-C, S-overlap | `overlap_joined.csv`; recompute (bootstrap CIs from `auc.csv`) |
| AUC 0.77 (0.71--0.82), 0.22; 83%; 48%, 50%; 0.22, 0.23; 47% | III-C, IV-C, S-detector, letter | `a7_detector-2026-10-09/negatives_pretune.csv` + frozen B rows; recompute §A7 (CIs from `detector_metrics.csv`) |
| 0.82, 0.56 (noisy targets); 0.47, 0.12; 36 of 38 | S-detector | A7 report (not recomputed) |
| 0.095/0.047, 0.077/0.015, 0.000/0.004, 10 of 44, 3 of 71 | III-B (merged III-C) | unchanged from current main.tex |
| 32--33%, 6--10%, 5--19%, 19--20%, 5--8%, 4--18%, 3--4%, 18--43%, 2--20%, 5--18%, 14%, 22%, 0.045 mm, 0.11 | unchanged | current main.tex |

## 9. New bibliography entries (refs.bib)

```bibtex
@article{boogers2010,
  title={Automated quantification of stenosis severity on 64-slice {CT}: {A} comparison with quantitative coronary angiography},
  volume={3},
  doi={10.1016/j.jcmg.2010.01.010},
  number={7},
  journal={JACC Cardiovasc. Imag.},
  author={Boogers, Mark J. and Schuijf, Joanne D. and Kitslaar, Pieter H. and van Werkhoven, Jacob M. and de Graaf, Fleur R. and Boersma, Eric and van Velzen, Joëlla E. and Dijkstra, Jouke and Adame, Isabel M. and Kroft, Lucia J. and de Roos, Albert and Schreur, Johan H. and Heijenbrok, Mark W. and Jukema, J. Wouter and Reiber, Johan H. C. and Bax, Jeroen J.},
  year={2010},
  pages={699--709}
}

@article{gouya2009,
  title={Coronary artery stenosis in high-risk patients: 64-section {CT} and coronary angiography---{P}rospective study and analysis of discordance},
  volume={252},
  doi={10.1148/radiol.2522081271},
  number={2},
  journal={Radiology},
  author={Gouya, Herv{\'e} and Varenne, Olivier and Trinquart, Ludovic and Touz{\'e}, Emmanuel and Vignaux, Olivier and Spaulding, Christian and Mas, Jean-Louis and Sablayrolles, Jean-Louis},
  year={2009},
  pages={377--385}
}
```

Author first names for boogers2010 beyond the initials in the Europe PMC record should be checked against the journal page before the bib is finalized; the initials, title, volume, pages and DOI are verified.
