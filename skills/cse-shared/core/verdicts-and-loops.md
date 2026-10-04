# Verdicts, loops, and effort control

Shared machinery that every `cse-*` skill uses when it must judge a state, iterate on a
defect, or decide how much work a request deserves. It exists so that two skills never disagree
about what "pass" means or when to stop.

## Verdict enum

Use exactly these six states. Never invent a seventh, and never soften `FAIL` into `WARN`
because progress is wanted.

| Verdict | Meaning | Effect on the workflow |
|---|---|---|
| `PASS` | the criterion is met and the artifact proves it | continue |
| `WARN` | met, but with a defect that will cost something later | continue, and record the defect in the open-items list |
| `FAIL` | not met | stop the dependent step; produce the smallest clearing change |
| `BLOCKED` | cannot be evaluated because a required input is missing | stop; name the missing input and how to obtain it |
| `ERROR` | the evaluation itself could not run | stop; report the tool or artifact failure, do not guess a verdict |
| `NOT_APPLICABLE` | the criterion does not apply to this artifact type | continue; record why it does not apply |

`BLOCKED` and `ERROR` are not failures of the work and not passes. `ERROR` must never be
reported as `PASS` to keep a pipeline moving.

## Audited input and staleness

When validating an artifact, record its content hash and modification time, or an immutable
source version where hashing is unavailable. Do not invent a hash. Record a missing hash/check
as unverified and use a bounded diagnostic rather than claiming a fully frozen audit.

Freshness (`current` / `STALE`) is a separate field, not a seventh verdict. If an input changes,
retain the historical verdict but mark all dependent evaluations `STALE` and recompute them
before use. Compare content/version, not modification time alone. A stale PASS is unusable;
its pending re-evaluation is `BLOCKED`, not an automatic scientific `FAIL`. Gates, reports and
ledgers all follow this rule. A new revision resolves through the artifact index.

## Iteration loops and stop rules

Every iterative skill declares its loop budget and its stop rule in advance, and reports which
one ended the loop.

| Loop | Default budget | Stop rule |
|---|---|---|
| Review and revise | 4 rounds maximum | stop when the readiness score is at least 6 of 10 and the recommendation is `Accept` or `Minor revision`; stop earlier only on `PASS` with no `Blocking` concern |
| Targeted repair of one defect | 2 attempts per defect | after 2 failed attempts on the same defect, change tactic or escalate to the user; do not attempt the same fix a third time |
| Literature saturation | 3 search expansions | stop when a new expansion adds no new distinct relevant item, or when the marginal yield falls below the declared threshold |
| Experiment tuning | declared before running | stop at the pre-declared budget in `cse-plan.md`; exceeding it requires reopening G1, not a silent extension |
| Figure iteration | 3 rounds | stop when the figure passes its contract checks or when the user accepts the current version |

Report the loop outcome explicitly: `converged`, `budget exhausted with residual defects`, or
`stopped by user`. "Iterated a few times" is not a report.

## Effort tiers

Match effort to the stakes of the request, and state the tier you chose. Escalate only on the
user's instruction or when a gate fails.

| Tier | Multiplier on the default pass | When appropriate |
|---|---|---|
| `sketch` | about 0.4 | a quick internal check, a sanity read, a single-section fix |
| `standard` | 1.0 | the default: a section, a figure, one review round, an ablation plan |
| `thorough` | about 2.5 | a full manuscript pass, a rebuttal package, a multi-reviewer round |
| `submission` | 5 to 8 | a venue-bound submission package, a final integrity freeze |

Derive the tier, do not accept it blindly: a request to "check my abstract" is `sketch`, but the
same request on a manuscript that is one day from its deadline is at least `thorough`, because
the cost of a missed defect is now a rejected submission.

## Calibration: start at the midpoint and justify movement

When scoring any dimension, start at the midpoint and justify every point of movement in either
direction with a pointer. This prevents both inflation and reflexive harshness.

Two scales are used in this pack. They measure different things and must not be conflated.

| Scale | What it scores | Range | Midpoint start |
|---|---|---|---|
| Dimension score | each of the eight review dimensions, from [review-rubrics.md](review-rubrics.md) | 1 to 5 | 3 |
| Readiness score | one overall readiness number for the whole artifact, used to drive the review loop | 1 to 10 | 5 |

- On the 1 to 5 dimension scale, start at 3. To score 4 or 5, name the specific artifact that
  earns it. To score 1 or 2, name the specific defect that costs it.
- On the 1 to 10 readiness scale, start at 5 and apply the same rule. A readiness score of 9 or
  10 requires zero `Blocking` findings and at most two `Major` findings, and the readiness score
  must be consistent with the dimension scores rather than contradicting them.
- A dimension score is never a readiness score. Do not report a dimension out of 5 as though it
  were the readiness number, and do not derive the recommendation from the readiness score; the
  recommendation comes from the dimension scores by the mapping in [review-rubrics.md](review-rubrics.md).
- Severity vocabulary is fixed by [review-rubrics.md](review-rubrics.md): `Blocking`, `Major`,
  `Minor`, and `Question`. Do not import another severity vocabulary such as `CRITICAL`, and do
  not invent a recommendation tier such as `Strong Accept`. The four tiers are `Reject`,
  `Major revision`, `Minor revision`, and `Accept`.
- Every score change between rounds needs a stated reason. A score that moved without the
  artifact changing is a calibration error, not an improvement.

## Claim promotion

A statement may only be promoted into the manuscript, the abstract, or a slide when it meets the
promotion condition for its tier. This is the mechanism that keeps drafts honest.

| Statement | May be written as | Promotion condition |
|---|---|---|
| an observation from one run | "in our experiments" / "we observed" | the run exists and is recorded |
| a claim across runs | "our method achieves X" | justified sample size (at least the axis default unless a recorded rationale overrides it), dispersion and complete protocol; 3 runs alone never prove stability |
| a claim across datasets | "evaluated on A and B" | at least 2 named datasets with complete protocols; "generalizes" additionally requires a defined transfer/domain-shift test and no target-test leakage |
| a mechanism claim | "the gain comes from" | an ablation isolating that component under one protocol |
| a superiority claim | "outperforms" | a protocol-matched comparison against that specific baseline |
| a novelty claim | "no directly overlapping work retrieved within <scope>" | documented recent cycles plus foundational prior work and near misses; never treat a two-cycle window as proof of an unbounded "first to" |
| a field-deployment claim | "in the field" | field data, not simulation, with the platform and conditions stated |

If the promotion condition is unmet, write the weaker true statement. Never keep the stronger
wording and append a hedge.

## Blocker-first behaviour

When a request cannot be completed honestly with the available evidence, say so before doing any
of the requested work, and name the single missing item that unblocks it. Producing a confident
artifact from insufficient evidence, then noting the gap in a footnote, is the failure mode this
rule exists to prevent.

The correct output in that situation is:

```text
Cannot complete <request> as specified.
- Blocking gap: <the one missing input, artifact, or decision>
- Why it blocks: <which claim or gate depends on it>
- Fastest unblock: <the concrete action, and roughly what it costs>
- What I can do meanwhile: <the reduced-scope work that is honest without it>
```

## Citation audit thresholds

A citation audit directly reports support classifications and coverage, not its own accuracy.
State the population, sample size/rule, locations read, inaccessible items and counts of
`supported`, `overstated`, `unsupported`, `misattributed`, and `inaccessible`. Exclude inaccessible
items from adjudicated denominators and expose their count; never silently count them as supported.

False-negative and false-positive rates require **independent adjudicated ground truth**. Only
then compute FNR = FN/(TP+FN) and FPR = FP/(TN+FP), with supported as the positive class. Keep the
pack's heuristic targets below 0.15 and 0.10 respectively as calibration goals, not guarantees.
Report counts and uncertainty; a zero denominator means `not estimable`. Without ground truth,
write `FNR/FPR not estimable` rather than inventing rates or treating unsupported fraction as FPR.
A sampled audit is never a full audit.

## Anti-patterns

- Reporting `PASS` for a check that was never run.
- Reporting `WARN` for an integrity failure to avoid stopping the workflow.
- Raising a score because the user pushed back rather than because the artifact changed.
- Treating a `STALE` verdict as still valid.
- Running a fifth review round because the fourth did not converge; the correct action is to
  report non-convergence and name the unrepaired defect.
- Meeting a numeric gate by narrowing the evaluation set, changing the metric, or dropping a
  losing baseline.
