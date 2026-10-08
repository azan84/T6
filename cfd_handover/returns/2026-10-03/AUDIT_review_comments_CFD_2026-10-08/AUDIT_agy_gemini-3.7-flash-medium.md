### Model Identity
**Model:** Gemini 3.7 Flash

---

### Audit Verdicts per Question

#### Question 1: Volumetric Flow & Boundary Conditions
**Verdict:** **CONFIRMED**
* **Evidence:**
  * [`M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_results.csv#L1-L7), [`M1_outlets_*.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_outlets_baseline_resistance.csv), [`M1_roundtrip_*.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_roundtrip_baseline.csv).
  * **Inlet flows ($Q_\text{inlet}$):**
    * `clean_nolesion`: Resistance $0.711856\text{ mL/s}$ ($42.71\text{ mL/min}$); Prescribed $0.648971\text{ mL/s}$ ($38.94\text{ mL/min}$).
    * `baseline`: Resistance $0.681732\text{ mL/s}$ ($40.90\text{ mL/min}$); Prescribed $0.648971\text{ mL/s}$ ($38.94\text{ mL/min}$).
    * `T1_missed_branch`: Resistance $0.579621\text{ mL/s}$ ($34.78\text{ mL/min}$); Prescribed $0.648971\text{ mL/s}$ ($38.94\text{ mL/min}$).
  * **Design Demand:** Total prescribed target flow is $0.648971\text{ mL/s}$ across all 3 prescribed cases. This corresponds to Murray demand $k \cdot r_\text{in}^3$ ($k=562\text{ s}^{-1}$) with an effective $r_\text{in} = 1.04913\text{ mm}$ ($r_\text{ref}=1.082\text{ mm}$, $r_\text{MIS}=1.301\text{ mm}$, $r_\text{eq3D}=1.710\text{ mm}$).
  * **Mass Imbalance & Roundtrip:** Mass imbalance is $< 10^{-5}\%$ for all solves. Prescribed-flow round-trip errors are $< 0.0013\%$ (`baseline`, `clean`) and $0.0051\%$ (`T1`), far beating the $0.5\%$ gate.
  * **Flow Deviations (> 1%):** Under Protocol A (fixed clean resistances), flow naturally deviates: in `baseline`, `out_160` (+16.03%), `out_600` (+15.42%), `out_742` (+1.96%), `out_868` (+1.73%); in `T1`, `out_558` (-43.25%) due to the missing child branch resistance. Under Protocol D, all outlet deviations are $< 0.0001\%$. The prescribed flows preserve territory totals identically between baseline and T1 ($0.173478\text{ mL/s}$ to the bifurcated/merged territory).

---

#### Question 2: Flow Regime
**Verdict:** **CONFIRMED**
* **Evidence:**
  * [`M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_results.csv#L1-L7), [`lesion80_hyperaemic.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/lesion80_hyperaemic.csv#L1-L7), [`main.tex#L164`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L164).
  * **Flow Rates:** 3D inlet flow for Scan 14 is $34.8\text{--}42.7\text{ mL/min}$ ($0.58\text{--}0.71\text{ mL/s}$), which is $\sim 2.5\times$ below cohort median demand ($1.5\text{ mL/s} = 90\text{ mL/min}$) and $\sim 5.5\times$ below the physiological anchor ($214\text{ mL/min}$ for a $3.7\text{ mm}$ LAD).
  * **Reynolds Number & FFR:** $\text{Re}_\text{throat} = 106.4$ (prescribed) and $123.1$ (resistance baseline). At such low flow (trans-stenotic flow $\approx 0.17\text{--}0.20\text{ mL/s}$), inertial/quadratic expansion losses ($\propto Q^2$) are minor, yielding an unphysiologically high FFR of $0.870$ for a severe $80\%\text{ DS}$, $20\text{ mm}$ stenosis.
  * **Scan 837 Hyperaemic Pair:** Elevating flow $\sim 3.1\times$ ($0.66\rightarrow 2.02\text{ mL/s}$) increased trans-stenotic pressure drop by $3.37\times$ (FFR dropped from $0.883$ to $0.605$). This confirms severe nonlinear sensitivity to flow, though quantitative values from Scan 837 do not directly transfer to Scan 14 due to geometric differences.

---

#### Question 3: Radius Bias
**Verdict:** **PARTLY SUPPORTED**
* **Evidence:**
  * [`as_meshed_radius_baseline_detail.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/as_meshed_radius_baseline_detail.csv#L1-L750), [`main.tex#L414-L418`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L414-L418).
  * **Radius Discrepancy:** The meshed 3D area-equivalent radius $r_\text{eq3D}$ exceeds the 0D centerline radius $r_\text{MIS}$ by a median difference of $0.1384\text{ mm}$ (manuscript reports $0.14\text{ mm}$) and median ratio of $1.182$ (+18.2%). At the stenosis throat (node 73), $r_\text{eq3D} = 0.2756\text{ mm}$ vs target $0.2306\text{ mm}$ (manuscript reports $0.276$ vs $0.231\text{ mm}$).
  * **Paired Deltas:** The manuscript claim that this offset "shifts absolute FFR but not the paired differences" holds *qualitatively* (positive $\Delta\text{FFR}$ under Protocol A, near-zero under Protocol D), but *not quantitatively*: $\Delta\text{FFR}$ drops from $+0.127$ on the requested 0D radius to $+0.081$ on the 0D as-meshed radius and $+0.074$ in 3D CFD (a $\sim 42\%$ reduction in effect size).

---

#### Question 4: 3D "Concealment" Claim
**Verdict:** **CONFIRMED** (Reviewer critique is fully supported by data)
* **Evidence:**
  * [`M1_probes_baseline_prescribed.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_probes_baseline_prescribed.csv#L13), [`M1_probes_T1_missed_branch_prescribed.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_probes_T1_missed_branch_prescribed.csv#L12).
  * **Numerical Verification:** Under Protocol A, baseline FFR $= 0.8698$, T1 $= 0.9436$, $\Delta\text{FFR} = +0.0738 \approx +0.074$. Under Protocol D, baseline $= 0.8923$, T1 $= 0.8916$, $\Delta\text{FFR} = -0.00069 \approx -0.0007$.
  * **Probe Indexing Reconciliation:** In baseline, the measurement probe at arc $s = 49.89\text{ mm}$ is indexed as `p011` ($0.892295$). In T1 (missing two bifurcation probes), the probe at $s = 49.89\text{ mm}$ is indexed as `p010` ($0.891606$). The manuscript's $-0.0007$ correctly compares the same anatomical location ($0.891606 - 0.892295 = -0.000689$).
  * **Mechanism Refutation:** Prescribing per-outlet flows (Protocol D) fixes trans-stenotic flow, completely eliminating the FFR error ($|\Delta\text{FFR}| < 0.001 \ll 0.05$). This is **error removal / correction**, not concealment. Protocol C (single global resistance scaling) was never run in 3D.

---

#### Question 5: Other CFD Contradictions & Reviewer Accuracy
**Verdict:** **CONFIRMED**
* **Evidence:**
  * [`STAGE-A-VALIDATION.tex#L200721-L203000`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L200721), [`NOTE.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/NOTE.md).
  * **Task A Sensitivity & Gate Failures:** Halving throat cells to $12.5\,\mu\text{m}$ shifted FFR by $+0.00189$ (A1) and $+0.00207$ (A2). The manuscript quotes $0.0019$ and $0.0021$ but conceals that Task A **failed** its pre-registered threshold ($|\Delta| < U_\text{3D} = 0.00055$, failing by $3.8\times$).
  * **Geometry Gates & Strict Mesh Checks:** Baseline and T1 failed strict checkMesh (1058/977 low-quality face tets within $1.43\text{ mm}$ of throat, failing D3/D4 2 mm exclusion rule) and failed `surfaceCheck_not_self_intersecting`.
  * **Reviewer Accuracy:** Domain W1 (low flow regime) and Methodology W1 / Domain W2 (3D shows correction, not concealment) are accurate. Domain W13 is **overstated/inaccurate** in its mechanistic premise: prescribed baseline FFR was higher ($0.892$) than resistance baseline ($0.870$) because total prescribed flow ($0.649\text{ mL/s}$) was lower than resistance solve flow ($0.682\text{ mL/s}$).

---

### Ranked List of Manuscript Defects & Risks

1. **Fatal Framing Contradiction on 3D "Concealment" (High Severity):**
   * *Location:* [`main.tex#L401-L406`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L401-L406), [`main.tex#L489-L493`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L489-L493).
   * *Defect:* Claiming 3D "reproduced this concealment" when Protocol D eliminated the FFR error ($\Delta\text{FFR} = -0.0007$).
2. **Unphysiological Flow Regime & FFR Discordance (High Severity):**
   * *Location:* [`main.tex#L160-L165`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L160-L165), [`main.tex#L223-L230`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L223-L230).
   * *Defect:* Scan 14 inlet flow ($39\text{--}41\text{ mL/min}$) is $\sim 5\times$ below physiological LAD hyperemia ($214\text{ mL/min}$), masking quadratic stenosis loss and producing FFR 0.870 on an 80% DS lesion.
3. **Selective Reporting of 3D Verification Gates (Medium Severity):**
   * *Location:* [`main.tex#L240-L244`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L240-L244), [`main.tex#L416-L418`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L416-L418).
   * *Defect:* Cites $U_\text{3D} = 5.5\times 10^{-4}$ (from straight-tube sten70) and Task A shifts without disclosing that Task A and mesh proximity gates D3/D4 failed pre-registered criteria.
4. **Overstatement of Paired Invariance to Radius Bias (Low/Medium Severity):**
   * *Location:* [`main.tex#L481-L483`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex#L481-L483).
   * *Defect:* Stating radius offset "shifts absolute FFR but not paired differences" ignores that $\Delta\text{FFR}$ reduced by $42\%$ ($0.127 \rightarrow 0.074$).

---

### Recommended Actionable Fixes

1. **Reframe 3D Arm:** Explicitly contrast Protocol A (+0.074 shift) with Protocol D (-0.0007 correction). State that per-outlet/territory flow matching *restores* true FFR for distal branch loss, whereas under-parameterized 1-scalar scaling (Protocol C) conceals error.
2. **Acknowledge Flow Regime & Radius Bias:** Report Scan 14 Reynolds numbers ($\sim 106\text{--}123$) and baseline flows ($39\text{--}43\text{ mL/min}$) in Discussion/Limitations, noting that higher hyperemic flows amplify both baseline stenosis drops and topological error shifts.
3. **Transparent Mesh Uncertainty Reporting:** Clarify that $U_\text{3D}=0.00055$ applies to idealized sten70, while patient-specific throat refinement (Task A) introduced a $0.0019\text{--}0.0021$ delta (still small relative to the $0.074$ error effect).
