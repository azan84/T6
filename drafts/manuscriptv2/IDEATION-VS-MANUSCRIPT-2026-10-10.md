# Paper 6: ideation score (2026-09-13) vs current manuscript (v2, 2026-10-10)

Rubric: research-ideation `scoring-rubric.md`, default weights (novelty 25, gap 15, impact 15, feasibility 20, journal fit 15, defensibility 10). Weighted = sum(w x s)/100 x 2.
Initial: `Proposal/ideation_run/2026-09-13/candidates.json` (T6). Current: re-scored by Claude on the same anchors against drafts/manuscriptv2 (not a blind score).

| Criterion (weight) | Ideation 09-13 | Manuscript v2 | Change | Basis |
|---|---|---|---|---|
| Novelty (25) | 3 (INCREMENTAL cap) | 3 strict / 4 uncapped | 0 / +1 | Planned novelty (empirical segmenter-disagreement error sizes at matched clDice) not delivered: paired masks declined, so sizes come from the literature (DSC 0.928). New novelty delivered instead: passes-and-wrong under perfusion tuning, noise-matched floor, four BC protocols, throat error. The cap stays until the prior-art check is re-run. |
| Gap evidence (15) | 5 | 5 | 0 | Same corpus gap (P258, P263, P474; n = 1–60); still open. |
| Impact (15) | 4 | 4 | 0 | Two audiences (CT-FFR/digital-twin credibility, segmentation metrics), but in silico only and "not validated decision rules", so 5 is not reached. |
| Feasibility (20) | 3 (WITH-CHANGE) | 4 | +1 | Delivered on CPU with open data within the window. 3D arm reduced to one case (M1 failed for lesions), coronary arm only, synthetic stenoses. |
| Journal fit (15) | 4 | 5 | +1 | CFP aims quote maps directly; tier confirmed top 10%; cites 3 recent JBHI papers; 20-paper JBHI practice benchmark. |
| Defensibility (10) | 2 (H1 unresolved) | 4 | +2 | H1 resolved: the message is no longer radius scaling; mechanism stated (tuning forces clean flow through a wrong lumen); single message; noise-matched floor, demand x2/x3, finer territories, DSC measured. Remaining trigger: in silico only, error frequency not measured. |
| **Weighted /10** | **7.00** | **8.10 strict / 8.60 uncapped** | **+1.10 / +1.60** | |

External check: blind 5-seat audit 10-09 = 6.4 (all major); re-score 10-09 pm = 6.5. Of its 7 convergent weaknesses, #2 (unequal floor) is closed in v2; #1, #4, #6, #7 were addressed 10-09; #3 (discrete-only excess) and #5 (low demand) stay as stated limitations.
