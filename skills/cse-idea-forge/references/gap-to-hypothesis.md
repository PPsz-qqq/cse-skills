# From gap to hypothesis

A gap statement becomes an idea only when it is rewritten as a hypothesis that can fail. This file
gives the conversion procedure and the four-part form.

## What makes a gap usable

A gap is an observation across the corpus, not the absence of a retrieval. Before converting one,
check it against these conditions.

| Condition | Check |
|---|---|
| Supported | at least three works show the pattern, with identifiers |
| Specific | it names the setting, the task and the failure mode, not just a missing combination |
| Consequential | someone outside the paper would care that it is closed |
| Reachable | the resources from the anchoring step can actually test it |
| Not a non-problem | closing it would not change what anyone does or believes |

A gap that fails the "consequential" or "not a non-problem" check produces an idea that reviewers
call incremental, and no amount of experiment quality repairs that.

The classic false gaps in this field, and why they are false.

- "The same method has not been tried on the other benchmark." This is a transfer, and a transfer
  with no mechanism explanation is an empirical delta at best, and a weak one.
- "Nobody has combined A and B." Combination is a contribution only if the combination is
  non-obvious and the interaction is analysed. Otherwise it is engineering.
- "Prior work assumes X and X is not always true." This is a real gap only if the consequences of X
  being false are both measurable and non-trivial.
- "Existing methods are slow." Speed is a real contribution, but it needs a stated operational
  consequence and a fair runtime protocol, including the hardware.
- "Results are not comparable across papers." This produces a benchmark or a survey contribution,
  not a method contribution, and the contribution type must say so.

## The four-part hypothesis form

Write all four parts. A missing part is a placeholder and fails G1.

```text
H<n>
1. Intervention: <the single change we make, expressed as something we control>
2. Mechanism: <the causal story for why the change should produce the effect>
3. Measurable signature: <metric, benchmark, split, protocol, expected direction, rough magnitude>
4. Refutation rule: <the observation that makes H<n> false, with an explicit threshold and a
   pre-declared comparison>
```

Rules for each part.

**Intervention.** One change. A hypothesis with two simultaneous changes cannot be attributed, and
the ablation will not save it. If two changes are genuinely necessary, write two hypotheses and plan
the interaction term.

**Mechanism.** The mechanism must predict something beyond "it will be better". A usable mechanism
predicts where the gain appears and where it does not. "The motion prior should help most in the
low-appearance-discriminability regime, and should not help on scenes with distinctive appearance"
is a mechanism, because it forbids a result. "The attention module improves feature
discrimination" is not, because no result contradicts it.

**Measurable signature.** Name the metric with its convention, the benchmark and split, the
evaluation protocol, the expected direction, and a rough expected magnitude. The magnitude is
`assumed` and must be labelled so, with a note on what happens if it is wrong by a factor.

**Refutation rule.** This is the load-bearing part. It must be possible for it to fail, and it must
be checkable by someone else from the artifacts. Weak and strong forms:

| Weak, fails G1 | Strong, passes G1 |
|---|---|
| "if results are promising" | "if the matched-protocol delta on the primary metric is below X after 3 seeds" |
| "if the method does not work" | "if the component's ablation shows no improvement beyond the seed-to-seed spread on any of the three benchmarks" |
| "if reviewers do not like it" | "if the assumption the theorem needs is violated on the target scenario set, so the bound does not apply" |
| "if it is not better" | "if the baseline re-implemented under our protocol matches or exceeds our method on the primary metric" |

Every refutation rule needs three things, which are the metric, the threshold, and the comparison that
produces them.

## Threshold selection

Set the threshold from the smallest difference that would matter, not from the largest difference you
hope for.

1. Choose a practical margin from the task's decision cost or an external requirement, and record
   its rationale before confirmatory outcomes. A provisional margin means G1 cannot yet freeze.
2. Estimate variance from verified literature or a labelled exploratory pilot for power/sample-size
   planning. Do not require the practical margin to exceed an individual arm's standard deviation;
   uncertainty belongs in the interval/test on the difference. If a pilot informs the margin, retain
   that influence and validate on independent confirmatory data under a fresh freeze.
3. State the support, refutation and inconclusive regions and their statistical treatment. Do not
   set the margin after the first confirmatory three-seed run or repeatedly add seeds until it passes.

For `filt`, the threshold should be stated for both accuracy and consistency. An RMSE threshold plus
an ANEES-within-bounds condition, because a filter that is accurate and inconsistent is broken.

## Worked conversion

```text
Gap G1: the three works in the corpus all evaluate tracking on sequences selected for
discriminative appearance, and DanceTrack was built precisely because that selection hides the
appearance-free failure mode, yet none of the three reports a DanceTrack result.

H1
1. Intervention: replace the appearance-similarity term in the association cost with a motion
   consistency term that is re-estimated online from the observed association history.
2. Mechanism: if appearance carries no identity information, the appearance term contributes noise
   to the cost matrix; removing it should raise association accuracy most in the high-crossing,
   high-articulation regimes and should not change results where appearance is discriminative.
3. Measurable signature: HOTA on DanceTrack test, plus the AssA component reported separately,
   compared against ByteTrack and OC-SORT under identical detections; expected AssA gain in the low
   single digits, `assumed`.
4. Refutation rule: H1 is false if, on DanceTrack with identical detector outputs, the AssA of our
   method does not exceed the best of the two baselines by at least the pre-declared margin after
   3 seeds, or if the MOT17 result degrades by more than the pre-declared margin, since the mechanism
   predicts no MOT17 gain but forbids a large loss.
   Fallback contribution if refuted: a controlled negative result showing which association terms
   carry identity information under uniform appearance, which is a mechanism contribution of the
   "what does not work and why" form.
```

Note the two-sided structure in the refutation rule. A mechanism that predicts where a gain appears
usually also predicts where it must not appear, and the second half is often the more discriminating
test.

## Common failure modes

- **The unfalsifiable mechanism.** Any result is consistent with the story, so no result is evidence.
- **The moving threshold.** The threshold is chosen after seeing the numbers, which converts the
  refutation rule into a description of what happened.
- **The orphaned ablation.** The hypothesis names a mechanism, but the plan has no ablation that
  isolates it. The claim type is then an empirical delta, whatever the introduction says.
- **The two-change hypothesis.** Two interventions, one hypothesis, and an unattributable result.
- **The benchmark substitution.** The pre-declared benchmark turns out to be inconvenient and is
  replaced. Report both results, per
  [../../cse-shared/core/evidence-integrity.md](../../cse-shared/core/evidence-integrity.md) rule 9.
- **The missing fallback.** The hypothesis is refuted and there is no declared weaker claim, so the
  work is reported as a failure rather than as a finding.
