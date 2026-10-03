# Review rubrics and severity calibration

Use this file when scoring a manuscript, calibrating how severe a concern is, writing a review,
or defending a contribution. It governs `ctrl-pre-submission-review` and the scoring steps of
the other skills.

## Two rules that come before any score

1. **No concern quota.** If no grounded concern exists at a level, say so. Inventing a concern
   to look balanced is a failure, and so is omitting a real one to be agreeable.
2. **Evidence pointer or it is not a concern.** Every concern carries a claim pointer and an
   evidence pointer naming the location in the manuscript or the artifact. A concern without a
   pointer is a personal preference and must be dropped or reframed as a question.

## The eight scoring dimensions

Score each dimension 1 to 5. Use the anchors literally; do not interpolate a score you cannot
justify with a pointer.

| # | Dimension | What a 1 looks like | What a 3 looks like | What a 5 looks like |
|---|---|---|---|---|
| D1 | Problem significance | a solved or inconsequential problem | a real problem with a plausible but unproven impact | a problem the field recognizes, with a stated consequence of solving it |
| D2 | Novelty of the contribution | a known method applied to a known dataset | a genuine combination or a meaningful extension | a new formulation, mechanism, or decisive counter-intuitive result |
| D3 | Technical soundness | method underspecified or self-inconsistent | method clear and correct in the main path | method fully specified, correctness argued, edge cases handled |
| D4 | Experimental rigor | unmatched comparisons, single seed, no ablation | matched protocol, seeds stated, ablation present | multi-dataset, multi-seed, statistical treatment, honest failure analysis |
| D5 | Reproducibility | no code, no configs, unclear data | configs or code partially available | code, configs, seeds, and data instructions reproduce a headline number |
| D6 | Positioning in the literature | missing or inaccurate related work | adequate coverage of the main lines | complete, current, and each distinction is precise |
| D7 | Clarity and presentation | unreadable structure, undefined symbols | readable with local defects | figures carry the argument, notation is consistent, derivations verifiable |
| D8 | Validity boundary honesty | simulation presented as real-world; limits unstated | limits stated but incomplete | every claim carries dataset, scenario, hardware, and assumption boundaries |

Weighting is venue-class dependent. Use these defaults unless the venue states otherwise.

| Venue class | Heaviest dimensions |
|---|---|
| A: CVPR-class vision and ML | D2, D4, D3 |
| B: control, robotics, navigation | D3, D4, D1 |
| C: remote sensing | D3, D4, D8 |
| D: Chinese-language journals | D1, D2 (创新点), D4 |
| E: preprint | no gate; use the rubric diagnostically only |

## Recommendation mapping

Derive the recommendation from the scores; do not choose it first and back-fill.

| Condition | Recommendation |
|---|---|
| Any of D1, D3, D4 at 1, or any blocking integrity failure | Reject |
| D2 at 1 or 2 with D4 at 1 or 2 | Reject as incremental and under-evidenced |
| One dimension at 2 with the rest at 3 or above, no blocking concern | Major revision |
| No dimension below 3, at least one at 4 or above, no blocking concern | Minor revision |
| No dimension below 4, at least two at 5, no blocking concern | Accept |

The table is exhaustive over its own conditions, and a score vector can fall between rows. Apply
this tie-break in order, and state which row or tie-break you used:

1. If any Reject row applies, the recommendation is Reject.
2. Otherwise, the lowest-scoring dimension sets the ceiling. A vector with no dimension below 3
   but none reaching 4 is `Major revision`, since the work is sound in outline but has no
   established strength to recommend.
3. A vector where the lowest dimension is 3 and at least one other reaches 4 is
   `Minor revision`, not `Major revision`, because the concern is local rather than structural.
4. If the Accept row applies, use `Accept`; it is the more specific case of the overlapping
   Minor-revision row. Otherwise any unresolved Blocking concern or dimension below 3 is at
   least `Major revision` unless a Reject rule applies. Thus vectors with several dimensions
   at 2 or D5 at 1 are not unmapped. State the rule and grounded concerns that determine it.

A midpoint draft scoring 3 on every dimension is therefore `Major revision`, which is the
expected starting point before any artifact has been strengthened.

Any integrity failure under `ctrl-shared` `core/evidence-integrity.md` rules 1, 2, 4, or 10
forces Reject regardless of scores.

## Severity tiers

| Tier | Definition | Must be fixed |
|---|---|---|
| `Blocking` | the manuscript cannot establish its central case until this is resolved | before any acceptance |
| `Major` | the claim survives only with a caveat, or an essential comparison is missing | before acceptance |
| `Minor` | a local defect in presentation, notation, or reference completeness | before camera-ready |
| `Question` | the reviewer cannot assess without information the authors possess | before the next review round |

A core evidence, validity, ethics, or integrity problem is never `Minor` merely because it is
easy to describe. A local typographic issue is never `Major` merely to sound severe.

## Concern record format

```text
Concern ID: <axis>-C<n>, for example det-C3
Severity: Blocking | Major | Minor | Question
Dimension: D1..D8
Blocking: Yes | No
Claim pointer: <the exact claim, with its location>
Evidence pointer: <the artifact or manuscript location>
Concern: <one paragraph, no rhetorical escalation>
Why it matters: <the consequence for the manuscript's case>
Resolution test: <the observable condition that would close this concern>
```

## Reviewer independence

When producing more than one review, follow the mechanism below, which is the pack's standard
because it is what makes multi-reviewer review informative rather than ornamental.

1. Build one immutable review packet: the manuscript or artifacts, the verified source anchors,
   the assessment boundary, and the common criteria. It contains no concerns, no hypotheses,
   and no conclusions.
2. Define emphasis briefs before any review exists. A brief is a lens, not a persona: no
   invented names, institutions, or biographies.
3. Run each reviewer in a genuinely separate context. Pass only the packet, that reviewer's
   brief, the report skeleton, and these rules.
4. Freeze each report before any comparison. Do not edit a report afterwards to reduce overlap
   or to manufacture disagreement.
5. Compare only after all reports are frozen. Label a point `consensus` only when at least two
   reports independently raised the same underlying concern.
6. If contexts cannot be isolated, generate one report per fresh invocation or declare non-blindness.
   Isolated contexts reduce leaks, not model correlation: label the output simulated reviews and
   never infer real-peer agreement or acceptance probabilities from report overlap.

## Anti-sycophancy calibration

Applies when you are reviewing, revising, or responding, and when a user pushes back on a
finding.

- Score counter-arguments by directness and sufficiency, not by whether their evidence is new.
  A bare assertion is 1; relevant but incomplete evidence is 3; evidence directly closing the
  resolution test is 4 or 5, including existing material the reviewer originally missed.
- Concede a concern only when the counter-argument scores 4 or above. Otherwise maintain the
  concern and restate the resolution test.
- Never lower a severity tier because the user is displeased, because the deadline is near, or
  because the finding is inconvenient.
- State disagreements with the user plainly and once, with the evidence, then continue with the
  work under the user's decision, recording the residual risk.

## Self-audit obligation

A review or assessment is itself a claim. Before delivering one, check: every concern has a
pointer; no severity was inflated or deflated to reach a target recommendation; no invented
fact appears; each resolution test is observable; and the recommendation follows from the
scores by the mapping above. Report your own error rate honestly when you correct a prior
assessment rather than silently revising it.
