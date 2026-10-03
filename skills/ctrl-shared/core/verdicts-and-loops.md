# Verdicts, loops, and effort control

Shared machinery that every `ctrl-*` skill uses when it must judge a state, iterate on a
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

When a step validates an artifact, record the artifact's content hash and modification time
alongside the verdict. If the artifact changes afterwards, every verdict derived from it becomes
`STALE` and must be recomputed. A verdict is only valid for the exact revision it was computed
from.

Apply this rule without exception to gate verdicts, review reports, and claim ledgers. A
revision after a pass invalidates the pass; a claim in the abstract whose ledger row is `STALE`
is unsourced, so G2 reverts to `FAIL`.

## Iteration loops and stop rules

Every iterative skill declares its loop budget and its stop rule in advance, and reports which
one ended the loop.

| Loop | Default budget | Stop rule |
|---|---|---|
| Review and revise | 4 rounds maximum | stop when the readiness score is at least 6 of 10 and the recommendation is `Accept` or `Minor revision`; stop earlier only on `PASS` with no `Blocking` concern |
| Targeted repair of one defect | 2 attempts per defect | after 2 failed attempts on the same defect, change tactic or escalate to the user; do not attempt the same fix a third time |
| Literature saturation | 3 search expansions | stop when a new expansion adds no new distinct relevant item, or when the marginal yield falls below the declared threshold |
| Experiment tuning | declared before running | stop at the pre-declared budget in `ctrl-plan.md`; exceeding it requires reopening G1, not a silent extension |
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
| a claim across runs | "our method achieves X" | at least 3 runs, dispersion reported, protocol block complete |
| a claim across datasets | "generalizes to" | at least 2 datasets, both protocol blocks complete |
| a mechanism claim | "the gain comes from" | an ablation isolating that component under one protocol |
| a superiority claim | "outperforms" | a protocol-matched comparison against that specific baseline |
| a novelty claim | "the first to" | a documented search of the last two venue cycles, with the near misses listed |
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

When auditing whether cited claims are supported by their sources, track two rates and report
them with the audit:

- false negative rate, a supported claim wrongly flagged, target below 0.15;
- false positive rate, an unsupported claim wrongly passed, target below 0.10.

Sampling a subset and reporting the rate is honest. Claiming a full audit when a sample was
checked is not. State the sample size and the sampling rule.

## Anti-patterns

- Reporting `PASS` for a check that was never run.
- Reporting `WARN` for an integrity failure to avoid stopping the workflow.
- Raising a score because the user pushed back rather than because the artifact changed.
- Treating a `STALE` verdict as still valid.
- Running a fifth review round because the fourth did not converge; the correct action is to
  report non-convergence and name the unrepaired defect.
- Meeting a numeric gate by narrowing the evaluation set, changing the metric, or dropping a
  losing baseline.
