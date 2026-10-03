# Pilot budget discipline

Pilots exist to kill bad ideas cheaply. They are not preliminary experiments for the paper, and they
are not a place to start the real work early. The budget below is hard, and it is ported from the
idea-discovery budget gates described in the pack's automation research notes.

## The constants

```text
PILOT_MAX_HOURS     = 2     # skip any pilot estimated above 2 hours per GPU; flag as needing a manual pilot
PILOT_TIMEOUT_HOURS = 3     # hard kill for any running pilot that exceeds 3 hours
MAX_PILOT_IDEAS     = 3     # at most 3 top ideas piloted, in parallel
MAX_TOTAL_GPU_HOURS = 8     # total GPU budget across all pilots
```

Rules that make the constants binding.

- The estimate is written before the run. A pilot whose estimate exceeds 2 hours is skipped and
  flagged, not attempted with a smaller scope decided mid-run.
- The timeout is enforced by the harness, not by attention. A pilot at 3 hours is killed.
- The idea limit is a ranking decision. If there are five candidates, the two weakest are not piloted,
  and the report says so.
- The total budget is a ceiling on the sum, not a per-pilot cap. Three pilots at 2 hours and 3
  GPU-hours each exceed the total and the third is skipped.
- Exceeding the total requires reopening G1 as a new dated decision, not a silent extension. The
  experiment-tuning stop rule in
  [../../ctrl-shared/core/verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md) says
  the same thing.

## Scaling the budget by effort tier

The constants are the default for a `standard` pass. Scale the wall-clock and total-GPU figures with
the effort tier, and state the scaled values rather than silently using different ones.

| Effort tier | Max hours per pilot | Timeout | Max pilot ideas | Total GPU-hours |
|---|---|---|---|---|
| `sketch` | 0.5 | 1 | 1 | 2 |
| `standard` | 2 | 3 | 3 | 8 |
| `thorough` | 3 | 4 | 3 | 12 |
| `submission` | 3 | 5 | 4 | 16 |

Scaling up is a decision the user makes explicitly. Scaling down is always permitted, and is often
the right call when the pilot question is narrow.

## What a pilot is for

A pilot answers exactly one question, whether the signal is large enough to justify the full
experiment. Three acceptable pilot shapes.

- **Signal pilot.** Train or run the smallest configuration that can show whether the effect exists,
  on a subset, with one seed. The question is whether the delta is above the noise floor.
- **Feasibility pilot.** Does the pipeline run end to end at all, including the data loader, the
  evaluation harness, and the metric computation. The question is whether unknown unknowns remain.
- **Reproduction pilot.** Can the baseline be reproduced at approximately its published value under
  our protocol. The question is whether the comparison is available at all.

A pilot is not for hyperparameter search, not for a first full training run, and not for producing a
figure. If the pilot answer is "it would work with more tuning", the pilot failed to answer its
question and the outcome is `inconclusive`.

## Estimation procedure

Estimate before running, using this order.

1. Find the smallest published configuration that reports the same metric on the same benchmark.
   Scale the reported training time by the ratio of the two configurations, and state the ratio.
2. Multiply by a factor of 1.5 for integration overhead on the first run of a new pipeline, and state
   that the factor is a judgement.
3. Ask whether the estimate exceeds the cap. If it does, stop. Do not look for a way to make it fit
   by changing the question after the estimate.
4. Record the estimate, the basis, and the factor. The estimate is a claim and is graded `assumed`.

## Pilot ledger

```markdown
| Idea | Question the pilot answers | Estimate (h) | Basis for estimate | Actual (h) | GPU-h | Outcome | Budget-stopped |
|------|---------------------------|--------------|--------------------|------------|-------|---------|----------------|
| | signal / feasibility / reproduction | | | | | supported / inconclusive / refuted / skipped | yes / no |
```

Outcome definitions.

- `supported` means the pilot answered its question in favour of the hypothesis, with the number
  recorded. It does not mean the hypothesis is confirmed.
- `inconclusive` means the pilot did not resolve the question, usually because the run was too small,
  the metric was too noisy, or the pipeline failed in a way that hid the signal. An inconclusive
  pilot does not license a larger run; it means the pilot question was badly chosen.
- `refuted` means the pilot answered in the negative. Refuted at pilot stage is a good outcome,
  because it cost two hours instead of two months. Record it in the idea report and do not quietly
  delete the idea from the record.
- `skipped` means the estimate exceeded the cap, or the idea limit or total budget was reached. The
  report must mark it as needing a manual pilot rather than omitting it.

## Reporting the budget outcome

State whether the budget ended the pilot phase, because that is a finding about the plan.

```text
Pilot phase: complete within budget
- Pilots run: <n> of <MAX_PILOT_IDEAS>
- Total GPU-hours: <n> of <MAX_TOTAL_GPU_HOURS>
- Killed by timeout: <n>, listed with the idea and the elapsed time
- Skipped for exceeding the estimate: <n>, listed as needing a manual pilot
- Consequence for G1: <which hypotheses survive into the frozen plan>
```

```text
Pilot phase: budget exhausted
- Pilots run: <n>, total GPU-hours <n> of <MAX_TOTAL_GPU_HOURS>
- Remaining candidates not piloted: <list>
- Consequence for G1: reopened on <date>; the following was decided: <narrower scope | additional
  budget | hypothesis dropped>
```

## Anti-patterns

- **The creeping pilot.** The estimate was 2 hours, the run takes 30. The timeout is what prevents
  this; the estimate is what exposes it.
- **The disguised main experiment.** A pilot that is the full experiment at full scale, described as a
  pilot to avoid the plan freeze. If the result is going into the paper, it belongs in the plan.
- **The pilot as evidence.** A single-seed pilot result may not be promoted to a claim. Per the
  promotion table in
  [../../ctrl-shared/core/verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md), an
  observation from one run may be written as "we observed", and nothing stronger.
- **The unlimited retry.** A pilot that fails for an infrastructure reason is fixed once and re-run;
  after two failed attempts on the same defect, change tactic or escalate. See the targeted-repair
  budget in [../../ctrl-shared/core/verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md).
- **The silent skip.** A skipped pilot leaves a record saying it was skipped and why. A silently
  skipped pilot looks like a piloted idea in the final report, which is a misrepresentation.
- **The hidden hardware.** GPU-hours are meaningless without the part. Record the GPU model, since
  8 hours on one card and 8 hours on another are different budgets.
