# CFD Verification & Validation Audit Report

**Target Document:** [`STAGE-A-VALIDATION.tex`](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex)  
**Reference Data:** [`cfd_handover/returns/2026-10-03/`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/) (`TaskA/`, `TaskB/`, `TaskD_B2/` incl. `run4_2026-10-07/`, `P5/`, `NOTE.md`, `M1_D7_sensitivity_2026-10-06.csv`)  
**Auditor Role:** Independent, Strict, Read-Only Auditor

---

### **VERDICT: SOUND WITH CAVEATS**
The numeric results, gate flags, convergence statuses, and physical/numerical diagnostics in the audited sections of `STAGE-A-VALIDATION.tex` match the deposited return files and execution logs with high fidelity. No data fabrication, numeric discrepancies, or unjustified overclaims were found. The only caveats relate to minor text-level drafting synchronization between early subsections and the latest completed re-run records for Task B.

---

### **Findings and Evidence**

#### 1. Task B2 & Replicate 4
* **Soundness:** **PASS (Strict compliance with isolation rules)**
* **Evidence & Data Check:**
  1. **Run 4A (order L8x2 then L16):** Report lines [1701](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1701) & [2003](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L2003) claim L8x2 settled in 8937 s & 8989 s (0.803 solves/h), L16 in 4009 s (0.898 solves/h), with a throughput ratio of $0.895$ (paired: $0.892$). Both layouts meet the strict isolation criteria (`contended: "no"`, Linux non-owned CPU mean 0.0033 core, host non-owned max 0.2259 core). This matches [`pairA_L8x2_then_L16/B2_throughput.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskD_B2/run4_2026-10-07/pairA_L8x2_then_L16/B2_throughput.csv#L2-L7) and [`analyse_A.log`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskD_B2/run4_2026-10-07/pairA_L8x2_then_L16/analyse_A.log#L1-L3) exactly.
  2. **Run 4B (order L16 then L8x2):** Report lines [1701](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1701) & [2003](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L2003) record L16 as VALID (4020 s, 0.896 solves/h) and L8x2 as **INVALID** (8781 s & 8871 s, 0.816 solves/h; ratio 0.911 **NOT CLAIMED**). This matches [`pairB_L16_then_L8x2/B2_throughput.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskD_B2/run4_2026-10-07/pairB_L16_then_L8x2/B2_throughput.csv#L2-L7) and [`isolation_evidence.json`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskD_B2/run4_2026-10-07/pairB_L16_then_L8x2/results_L8x2/isolation_evidence.json#L213-L275), where a background OS update burst (`systemd` at 3.361 cores, `unattended-upgrades` at 1.086 cores) triggered `contended: "yes"`.
  3. **Claim Scope:** The text properly restricts the throughput advantage claim ($\sim 12\%$ more solves/h for L16) to order L8x2$\to$L16 only, explicitly disclosing that the bidirectional criterion was not established.

#### 2. Task P5 (Five-Case Baseline Pilot)
* **Soundness:** **PASS (All table entries and narrative statements match returned data)**
* **Evidence & Data Check:**
  1. **Table 6 (`\label{tab:p5}`, lines [1828-1838](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1828-L1838)):
     * **Scan 138:** 4,941,176 cells; $\text{Re}_\text{throat} = 264$; $p/P_\text{aorta} = 0.87816$ at p010; flags `D3_FAIL, D4_FAIL, CHECKMESH_STANDARD_FAIL`. Matches [`P5/138/M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/138/M1_results.csv) and [`P5/138/M1_probes_138_resistance.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/138/M1_probes_138_resistance.csv).
     * **Scan 69:** 4,218,023 cells; $\text{Re}_\text{throat} = 366$; $p/P_\text{aorta} = 0.86960$ at p012; flags `LESION_PURITY_GATE_FAIL, POSITIVE_CONTROL_UNDETECTED`. Matches [`P5/69/M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/69/M1_results.csv) and [`P5/69/M1_probes_69_resistance.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/69/M1_probes_69_resistance.csv).
     * **Scan 473:** 5,487,673 cells; $\text{Re}_\text{throat} = 400$; $p/P_\text{aorta} = 0.88333$ (`p011_reloc`, tree node 646) vs $0.88685$ (rejected package probe `p011`); flags `D2_RELATIVE_THROAT_GATE_FAIL, D3_FAIL, D4_FAIL, MEASUREMENT_PROBE_RELOCATED`. Matches [`P5/473/M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/473/M1_results.csv) and [`P5/473/M1_probes_473_resistance.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/473/M1_probes_473_resistance.csv).
     * **Scan 272:** 7,639,018 cells; $\text{Re}_\text{throat} = 320$; $p/P_\text{aorta} = 0.93861$ at p009; flags `SELF_INTERSECTION, D3_FAIL, D4_FAIL, OUTLET_LOST_IN_MESH (out_396)`. Matches [`P5/272/M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/272/M1_results.csv) and [`P5/272/M1_probes_272_resistance.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/272/M1_probes_272_resistance.csv).
     * **Scan 139:** 4,138,185 cells; $\text{Re}_\text{throat} = 236$; $p/P_\text{aorta} = 0.85674$ at p009; flags `D2_RELATIVE_THROAT_GATE_FAIL, D3_FAIL, D4_FAIL`. Matches [`P5/139/M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/139/M1_results.csv) and [`P5/139/M1_probes_139_resistance.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/139/M1_probes_139_resistance.csv).
  2. **Scan 473 Probe Relocation (line [1937](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1937)):** Accurately details the failure of package probe p011 under the section rule ($36.6^\circ > 20^\circ$ tangent angle) and deterministic relocation to `p011_reloc` (+2.85 mm distal), with the returned pressure of $0.88333$.
  3. **Scan 272 Truncated Domain (lines [1939-1940](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1939-L1940)):** Accurately describes that outlet `out_396` (31.5% target flow, 0.507 mL/s) was lost due to an under-resolved 1-voxel neck meshed at $200\,\mu\text{m}$ root cells resulting in 32,527 cells disconnected/deleted; 751 of 754 far surface vertices belong to R-PDA nodes 381–396. Triangle-triangle intersection checks (2,930 triangles within 3 mm, min distance $4.85\,\mu\text{m}$) confirm the `surfaceCheck` flag was a tool tolerance artifact. Explicitly states that the truncated solve is not a valid production baseline. Matches [`P5/272/ROOT_CAUSE_272_2026-10-06.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/P5/272/ROOT_CAUSE_272_2026-10-06.md) completely.

#### 3. Task B (Jet-State Verification & $U_{3D}=0.00055$ Final Claim)
* **Soundness:** **PASS WITH MINOR CAVEATS (Numeric data verified; drafting sync caveat in earlier text)**
* **Evidence & Data Check:**
  1. **Table 5 (`\label{tab:taskB}`, lines [1788-1803](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1788-L1803)) & Narrative ([1805](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1805)):
     * **S50:** 2,687,640 cells; FFR 0.793363 (re-run) vs 0.793362 (orig); offsets 0.0 / $0.4\,\mu\text{m}$; axisymmetric.
     * **S25A:** 3,194,196 cells; FFR 0.791103 (re-run) vs 0.791103 (orig); offsets 0.0 / $0.1\,\mu\text{m}$; axisymmetric.
     * **S25B:** 3,299,948 cells; FFR 0.791197 (re-run) vs 0.791197 (orig); offsets 0.0 / $0.1\,\mu\text{m}$; axisymmetric.
     * **S12A:** 6,739,168 cells; FFR 0.790308 (re-run) vs 0.790308 (orig); offsets 0.0 / $0.0\,\mu\text{m}$; axisymmetric.
     * **S12B:** 7,649,800 cells; FFR 0.790418 (re-run) vs 0.790418 (orig); offsets 1.2 / $2.3\,\mu\text{m}$; axisymmetric.
     * Matches [`TaskB/U3D_jet_state_check_2026-10-06.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskB/U3D_jet_state_check_2026-10-06.csv#L1-L6) and [`TaskB/result_S12A.json`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskB/result_S12A.json), [`TaskB/result_S12B.json`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskB/result_S12B.json), [`TaskB/result_S25B.json`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskB/result_S25B.json) bit-for-bit.
  2. **Finality Claim:** Section \S\ref{sec:taskB} (line [1805](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1805)) and Open Item (i) (line [2003](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L2003)) correctly declare that all five levels are verified on the axisymmetric state and $U_{3D}=0.00055$ is **final under Decision D9**.
  3. **[CAVEAT - Textual Desynchronization]:** In \S\ref{sec:u3d} (line [1531](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1531), item v) and \S\ref{sec:workorder} (line [2001](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L2001)), stale drafting notes dated 2026-10-01/02 remain in place claiming that $U_{3D}=0.00055$ is still "provisional" and that S12A, S12B, and S25B are "checked only indirectly." While \S\ref{sec:taskB} (lines 1784–1805) and line 2003 provide the updated final status, lines 1531 and 2001 represent un-synchronized draft text.

#### 4. Task A (D7 Sensitivity Test)
* **Soundness:** **PASS (Fully consistent with returned files and pre-registered protocol)**
* **Evidence & Data Check:**
  1. **Table 4 (`\label{tab:taskA}`, lines [1723-1741](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1723-L1741)):
     * Cell counts: Baseline/A0 = 3,657,147; A1 = 6,241,438; A2 = 8,308,794. Matches [`TaskA/M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskA/M1_results.csv).
     * $\Delta$ at measurement probe p011: $\text{A0} = +0.0000000$; $\text{A1} = +0.00189$; $\text{A2} = +0.00207$. Matches [`M1_D7_sensitivity_2026-10-06.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/M1_D7_sensitivity_2026-10-06.csv#L1-L4).
     * Probe profiles: Upstream p003 ($-0.00001$), throat p004 ($+0.00099$ / $+0.00097$), 5 mm distal p005 ($+0.00195$ / $+0.00200$), and 90 mm distal p023 ($+0.00188$ / $+0.00206$) match [`TaskA/M1_probes_*.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskA/M1_probes_baseline_D7_12p5_resistance.csv) to displayed precision.
     * Outlet flows: $+0.24\%$ (A1) and $+0.25\%$ (A2) on `out_160`/`out_600`; $<0.003\%$ on remaining 4 outlets. Matches [`TaskA/M1_outlets_*.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskA/M1_outlets_baseline_D7_12p5_resistance.csv).
     * Settle iterations: A0 = 1421, A1 = 2193, A2 = 2614. Matches [`TaskA/settle_*.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskA/settle_baseline_A0_25um_resistance.csv).
  2. **Honesty of Claim / Protocol Compliance (lines [1744-1746](file:///mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1744-L1746)):**
     * Correctly concludes that because $|\Delta| > U_{3D}$ ($3.4\times$ and $3.8\times$), **neither A1 nor A2 passes the D7 acceptance gate**, and Gate M1 fails for the lesion cases.
     * Correctly reports that the curved-lumen jet-centroid profile diagnostic is strictly **INDETERMINATE** by pre-registered rule due to an invalid section at 23–24 mm distal to the throat.
     * Correctly characterizes the shift as a $25\,\mu\text{m}\to 12.5\,\mu\text{m}$ resolution sensitivity without overclaiming asymptotic discretisation error bounds.

---
### **Audit Summary**
The technical substance across all four subsections is solid and faithful to the raw computation records. Updating the historical drafting text in lines 1531 and 2001 to align with the completed Task B re-runs in \S\ref{sec:taskB} will bring internal document consistency to 100%.
