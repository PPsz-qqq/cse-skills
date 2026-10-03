# Related-work writing

The related work is where a reviewer decides whether the authors know the field they are
publishing in. A paragraph that only summarizes signals that the contribution has not been
positioned, and `D6` in `../../ctrl-shared/core/review-rubrics.md` scores it at 2 or below.

The target is not coverage. The target is that a reviewer who wrote one of the cited papers cannot
object to the sentence about it.

## The positioning unit

One nearest competitor gets one block of three to five sentences, in this order.

```text
Nearest competitor: <Author et al., venue year>
What it does: <its contribution in one sentence, in its own terms, not as a foil>
What it shares with ours: <the mechanism, setting, or evaluation it has in common>
Where it differs: <the precise difference, stated so that a reader can check it against both papers>
Why the difference matters for our claim: <the consequence, one sentence>
Protocol note, if a number is quoted: <the difference that makes the quoted value not comparable>
```

The `Where it differs` line is the load-bearing one. It must name a mechanism, a setting, or an
assumption, not a quality. `They use a heavier backbone` is a difference. `They are less
effective` is not.

## Grouping rule

Organize by the distinction the paper turns on, not by year and not by a method list. For each
axis, the natural organizing distinction differs.

| Axis | Organizing distinctions that produce a real gap statement |
|---|---|
| `det` | dense versus sparse assignment; anchor-based versus anchor-free; end-to-end versus NMS-based; single-scale versus multi-scale fusion; closed-set versus open-vocabulary |
| `track` | tracking-by-detection versus joint detection and tracking; motion-only versus appearance-based association; online versus offline; public versus private detection protocols |
| `reid` | global versus part- or attention-based features; metric-learning versus classification losses; supervised versus unsupervised or domain-adaptive; single- versus cross-modality |
| `cnav` | centralized versus distributed estimation; range-only versus bearing or range-bearing; communication-aware versus communication-ideal; static versus time-varying topology; simulation versus field |
| `filt` | linear versus nonlinear Gaussian versus non-Gaussian; model-based versus learning-based; fixed versus adaptive covariance; consistency-focused versus accuracy-focused |

Use two or three of these as subsection headings in the related work. A subsection that cannot
produce a gap statement is not needed in this paper's related work and should be cut or reduced to
a sentence.

## The gap statement

Close the related work with the gap, derived from the differences above it, not asserted.

```text
Taken together, <line> addresses <A> but assumes <X>; <line> removes <X> but evaluates only under
<Y>. Neither reports <the specific missing measurement>. This paper measures <it> under <protocol>.
```

The gap must be a gap in evidence, not a gap in enthusiasm. `No prior work has explored this
promising direction` is not a gap. `No prior work reports a consistency check for the adaptive
variant, which is the setting where the covariance mismatch matters` is a gap.

## Quoting a number from another paper

A copied number stays `reported` and carries its protocol differences. This is the rule that is
most often broken in a related-work paragraph, where a competitor's headline value is quoted
without its setting and then compared with the authors' number in the introduction.

```text
[Author et al.] report <value> <units> on <dataset> under <their protocol labels>, which differs
from ours in <the specific fields>. The value is therefore reported for reference and is not
included in our comparison.
```

Rules.

- Never quote a number read only from an abstract. Read the table
  (`../../ctrl-shared/core/evidence-integrity.md` Rule 10).
- Never quote a number whose protocol labels you cannot state.
- Never place a `reported` value in a comparison table without marking it and naming the difference.
- Where the difference is one of the comparability breaks for the axis, the value is `not
  comparable` and stays out of the delta.

## Straw-man avoidance

Check each characterization against the cited paper's own text before keeping the sentence.

```text
[ ] The cited method is described using its own mechanism terms, not a simplified caricature
[ ] No cited method is described as ignoring something it explicitly handles
[ ] No cited method is credited with less capability than its own results show
[ ] No comparison is made against a version of a method that nobody published
[ ] Contemporaneous work is described without a superiority claim, since reviewers may be its authors
[ ] A limitation attributed to a cited method is one the cited paper itself acknowledges or that is visible in its protocol
[ ] Where the cited paper's setting differs, the difference is stated rather than treated as an omission
```

The characteristic failure in `track` is describing an appearance-based tracker as `relying only
on motion`, and in `filt` it is describing a baseline as `assuming Gaussian noise` when the cited
paper explicitly tests a heavy-tailed case. Both are checkable in one reading and both cost the
paper its credibility with the reviewer who wrote it.

## Novelty claims

A novelty claim needs a documented scope, queries, recent cycles **and foundational prior work**,
with near misses and coverage limits. A recent two-cycle window cannot establish historical priority.
Prefer the bounded claim in [verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md).

```text
Novelty claim: <the exact sentence, scoped as narrowly as it can honestly be>
Search record: <venues and cycles searched, queries used, date of the search>
Near misses: <the closest work found, and the precise difference for each>
Scope limit: <the wording that keeps the claim true, for example "for range-only cooperative
localization under time-varying topology">
Verdict: <supported | narrowed to <scope> | withdrawn>
```

Narrow to what the search actually established: `No directly overlapping work was retrieved under
<recorded queries, sources and window>`. Even a narrowly worded `first` is not proved by retrieval
absence alone. If search cannot run, mark the novelty assertion `[UNVERIFIED: search unavailable]`
and omit it from final prose; describe the planned contribution without asserting an absence of
prior work. `To our knowledge` is not a substitute for a search.

## Common related-work failures

| Failure | Symptom | Repair |
|---|---|---|
| List of summaries | every paragraph ends without a difference statement | rewrite each as a positioning unit |
| Positioned against the wrong work | the nearest competitor is absent while a distant one gets a paragraph | find the nearest work in the last two cycles and position against it |
| Unfair characterization | a cited method's own handling contradicts the description | correct it, and state the real difference |
| Decoration citation | a citation attached to a sentence it does not support | remove it or move it to the sentence it supports |
| Undated currency | the related work ends two cycles before the submission | add the recent line and position against it |
| Borrowed numbers | a competitor's value quoted without protocol labels | add the labels and the comparability verdict |
| Novelty by omission | `the first` because the search was never done | run the search or narrow the claim to a measurement gap |
| Axis conflation | `tracking` used for prediction, `localization` for detection | use the terms per `ctrl-shared` `core/terminology-and-notation.md` |
| Self-citation padding | a block of the authors' own prior work with no differentiating statement | keep only what positions this paper, and state the difference from each |

## Related-work self-check

```text
[ ] Organized by the distinction the paper turns on, not chronologically
[ ] Every nearest competitor has a positioning unit with a precise difference
[ ] The gap statement is derived from the differences above it
[ ] Every quoted number carries its protocol labels and a comparability verdict
[ ] No cited method is mischaracterized, checked against its own text
[ ] Every novelty claim has a search record, or is narrowed and marked
[ ] The section is current through the last two venue cycles
[ ] Every citation supports the sentence it sits in
[ ] Read-in-full versus abstract-only status is recorded where the support is load-bearing
[ ] The section ends with what this paper measures, not with a summary
```
