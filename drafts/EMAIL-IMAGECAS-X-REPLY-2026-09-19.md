# Email — reply to Bransby (accept the model-prediction offer)

**Status: SENT 2026-09-19.** Awaiting reply. Opens Gate **D1c** (algorithmic prediction variability).
Nudge once after ~3 weeks if silent, then let it go — the arm is off the critical path and the registration does not
wait on it. A `.docx` of the letter as sent is alongside this file.
Created 2026-09-19 in reply to his 2026-09-18 20:36 message
(`Monash University Mail - ImageCAS-X — request for the 160 paired re-annotations (inter-observer subset).pdf`).
**To:** Kit M. Bransby `kimbr@dtu.dk` · **CC:** Rasmus R. Paulsen `rapa@dtu.dk` (as before).

**v2 (after independent audit, `references/FABLE-AUDIT-RESULTS-PLAN-2026-09-19.md` §B2–B3) —
three substantive corrections to v1:**
1. **The reason for withdrawing our topological claim was wrong in v1.** v1 said topology is inherited from the shared
   centreline. The real reason is sharper and checkable: ImageCAS-X reports **Betti error = β₀ + β₁** — components and
   loops. **A missed side branch changes neither** (the tree stays one component with no cycle). So 0.2 ± 0.4 never
   measured the error type our study turns on. It *does* bear on vessel breaks (T2), which raise β₀.
2. **v1 asked him to confirm the caveat extends to the topological statistics.** Dropped — his confirmation could not
   repair a statistic that does not measure the event.
3. **v1's post-processing question named LCC filtering.** The paper's benchmark used a **< 100-voxel component
   filter**, so "did you apply LCC?" gets "no" and misses the real issue. Reworded, and a question added about which
   weights.

## Before sending — operator decisions

- [ ] **Attribution.** The draft asks what he would like, including co-authorship, rather than offering it outright.
      Settle with the existing four authors first (`STUDY-PLAN-v2` §7b is unresolved on byline and corresponding).
- [ ] **Do not promise a timeline.** This is off the critical path.
- [ ] Fill in title/department/email in the signature.

## What this email deliberately does NOT do

- It does not re-ask for the paired masks.
- It does not describe his predictions as inter-observer variability, or imply we will use them as one. They are a
  **model-error** regime — β-err 1.9 (CAS-Net) and 5.6 (nnU-Net) against 0.2 inter-observer, i.e. ten to forty times
  more topologically wrong. Different estimand, and the paper must never blur the two.

---

**Subject:** Re: ImageCAS-X — request for the 160 paired re-annotations (inter-observer subset)

Dear Dr Bransby,

Thank you for the quick and unusually informative reply — and for explaining the reasoning rather than simply
declining. Keeping the unchecked second set out of circulation so that nobody mistakes it for a second ground truth
is the right call, and we will not ask again.

Your point about the shared initialisation is the more valuable half of your email, and it has already changed what
we are doing. Since both annotators edited the same automatically generated centrelines and started from the same
3D U-Net boundaries, the published agreement is an upper bound — so where we derive a disagreement magnitude from
those statistics, we now treat it as a floor rather than an estimate, and say so.

It also made us re-examine a claim of our own, and withdraw it. We had intended to cite your Betti-number error as a
measured *topological* disagreement rate, and to lean on it for the error type our study is most sensitive to: a
missed side branch. On checking, that will not do — Betti error is β₀ + β₁, and a missing side branch leaves a tree
with the same number of components and no new loops, so it moves neither. Your statistic is a real measurement of a
real thing — vessel breaks, which do raise β₀ — but it is not a measurement of the event we care most about. We would
rather withdraw the claim than stretch your number to cover it.

Which is what makes your suggestion genuinely useful to us, and for a more specific reason than I would have given
yesterday. What our error model currently lacks is not a single magnitude — it is **apportionment**: of the errors a
real segmentor makes, what fraction are missed branches rather than breaks, which branches go missing and at what
calibre, and how radius bias varies with vessel diameter. We assume that apportionment at present, and say so in our
protocol as a declared weakness. A set of model predictions against your reference labels would let us measure it
across many scans and several models, and calibrate the injection design to it. That is a direct strengthening of
the part of our study that is weakest, and it is worth more to us than the paired masks would have been.

We would be glad to take you up on it. Four questions, so that we ask once rather than twice:

1. **How many scans, and which models?** Your message mentioned a distribution of predictions, and I want to be sure
   I read the scope right — is that predictions on a single scan, or across the test set? For measuring apportionment
   the more scans the better; even a few dozen would be genuinely useful.

2. **Raw or post-processed output — and could we have both?** This is the one that matters most to us. I understand
   the benchmark removed connected components below about 100 voxels. That is entirely sensible for reporting
   segmentation quality, but small fragments and breaks are exactly the topological events we are trying to count, so
   the filter removes our signal. Raw binarised output (or probability maps, if that is easier) **alongside** the
   post-processed version would let us report both and show what the filtering changes.

3. **Which training run or weights?** We want to be certain the predictions come from models that did not train on
   the scans they are predicting. If these are the benchmark runs trained on the 560 training scans with the 160 held
   out, that settles it — but I gather at least one public CAS-Net checkpoint used a different split, so I would
   rather ask than assume.

4. **On what terms?** Licence, how you would like it cited, and whether we may redeposit derived results (our
   measurements, not your predictions) as Source Data alongside the paper. Please also say what form of attribution
   you would prefer — including co-authorship if you would rather be involved that way, which we would welcome.

And one optional extra, only if it is easy to hand over: the **automatically generated centrelines as they were
before the annotators edited them**. The difference between those and the final edited centrelines is a measured
topological correction rate, which as far as we can find is not published anywhere, and it would let us separate
centreline error from lumen error — currently the weakest joint in our error model.

None of this is on our critical path, so there is no hurry at your end. We are grateful for the steer either way; the
caveat alone has improved the study, and the Betti point saved us from a claim we should not have made.

With thanks and best wishes,

[name]
[title, department]
[email]
