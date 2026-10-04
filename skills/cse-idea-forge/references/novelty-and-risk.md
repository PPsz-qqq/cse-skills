# Novelty and risk scoring

Two independent axes, scored separately, with the movement of every score justified by a pointer. A
single blended score hides exactly the trade-off that decides whether an idea should be piloted.

## Novelty, scored 1 to 5 against the ledger

Novelty is not how new the idea feels. It is how far the nearest competitor is, measured by the
ledger from `cse-lit-radar`.

| Score | Condition | Evidence required |
|---|---|---|
| 5 | no directly overlapping work retrieved within the recorded scope, which covers recent venue cycles plus the foundational line of work with near misses listed, and the mechanism itself is unclaimed | the recorded search with its windows, sources and coverage limits, plus a ledger whose top row is `low` overlap severity |
| 4 | no overlapping work on the mechanism; overlapping work exists on the task or the setting | ledger with the differing axis named for each row |
| 3 | one work overlaps on the mechanism but differs on a checkable axis such as the regime, the sensor or the assumption set | that work opened and read, with the location of the difference |
| 2 | the mechanism is published; the novelty is in the combination, the scale, or the application | a statement of what the combination adds beyond the sum |
| 1 | a known method applied to a known setting | none; this score means reconsider the idea |

Novelty score 5 is not available without a recorded search. This is the novelty promotion condition
in [../../cse-shared/core/verdicts-and-loops.md](../../cse-shared/core/verdicts-and-loops.md), and
it is the reason a "first to" sentence cannot be written from memory. Even a score of 5 licenses only
the bounded statement "no directly overlapping work retrieved within <scope>", never an unbounded
historical priority claim.

## Risk, scored 1 to 5

Risk is the probability that the plan cannot produce a publishable result within the resources. Score
the highest-risk component, not the average.

| Score | Condition |
|---|---|
| 5 | a required resource does not exist or is unconfirmed: the dataset is withdrawn or gated, the platform is not available, the baseline cannot be reproduced, or the theorem's key assumption is untested |
| 4 | a required resource exists but with a schedule or access risk: a benchmark whose evaluation server is offline, a hardware campaign with one window, an institutional-access dependency |
| 3 | the main hypothesis is plausible but the expected effect size is near the noise floor, or the pilot has not been run |
| 2 | the effect size is supported by a pilot, and the resources are in hand |
| 1 | the result is already effectively known, which usually means the novelty score is also low |

Score the components and report the maximum. Name which component sets the score.

```markdown
| Risk component | Assessment | Score |
|---|---|---|
| Data access | <will the exact split be obtainable, and by when> | |
| Baseline reproducibility | <can the baselines be re-implemented under our protocol> | |
| Compute | <is the budget from pilot-budget.md sufficient> | |
| Hardware or platform | <is the platform available in the window> | |
| Implementation | <is the hardest piece already prototyped> | |
| Theoretical assumptions | <does the target scenario satisfy them> | |
| Venue timing | <does the decision land before the milestone> | |
| Overall risk (maximum component) | <name the component> | |
```

## The two-axis grid

| | Risk 1-2 | Risk 3 | Risk 4-5 |
|---|---|---|---|
| **Novelty 5** | proceed; the rare case | proceed with a pilot first | do not proceed without changing one of the two axes; look for the reduced-scope version that keeps the mechanism but drops the risky resource |
| **Novelty 4** | proceed | proceed if a fallback contribution exists | reduce scope or change the setting to a resource you control |
| **Novelty 3** | proceed; strong candidate for a solid paper | marginal; strengthen the mechanism claim so novelty rises, or accept an empirical-delta framing | reconsider |
| **Novelty 2** | acceptable only with a scale or application story that reviewers will find consequential | weak | drop |
| **Novelty 1** | drop | drop | drop |

Two combinations deserve a note.

- **Novelty 5, risk 5.** This is the classic over-reach: a genuinely new mechanism that needs a
  resource that does not exist. The right output is a reduced-scope version that preserves the
  mechanism and replaces the resource, plus a record of what was given up.
- **Novelty 3, risk 2.** This is the modal honest project, and it publishes. Do not inflate its
  novelty to make it sound better. Strengthen it by making the mechanism claim testable, which raises
  the novelty score legitimately.

## Fallback contribution

Every idea at risk 3 or above declares, before results exist, the weaker true claim that survives a
refuted hypothesis. Write it as a claim, not as an intention.

| Main hypothesis refuted by | Fallback claim |
|---|---|
| a matched-protocol comparison showing no delta | "under protocol P, the proposed component does not improve the primary metric, while it does improve the secondary regime R; the mechanism responsible is C" |
| an ablation showing the component is inert | "the gain attributed in the literature to component A is reproduced by component B alone; A is not necessary" |
| a proof that needs an assumption the scenario violates | "the bound holds under A1 to A3; on the target scenario A2 is violated with the following measured consequence" |
| a hardware campaign that cannot be run | downgrade the type to empirical delta on simulation, and state the simulation-to-field gap as the limitation |

A fallback is not a consolation prize. Several of the strongest papers in this field are controlled
negative results framed as mechanism findings, and they are cited precisely because they forbid a
popular belief.

## Anti-inflation rules

- Score novelty from the ledger, in writing, with the top ledger row named in the justification.
- Score risk from the component table, and name the component that sets the maximum.
- Start every dimension at 3 and justify movement in either direction with a pointer. This is the
  calibration rule in
  [../../cse-shared/core/verdicts-and-loops.md](../../cse-shared/core/verdicts-and-loops.md).
- Re-score only when an artifact changed. A score that moved because the user pushed back is a
  calibration error.
- Do not accept a self-reported novelty score from the idea's author without the ledger behind it.
- Do not accept an untested but well-argued mechanism as low-novelty merely because it is untested.
  A solid mechanism argument with a named validation experiment can legitimately score 4.
- Re-run the ledger when the venue cycle changes, because a concurrent submission can occupy the
  space between cycles and is visible as a preprint first.

## Reporting format

```text
Novelty  <n>/5, nearest ledger row <work, identifier>, differing axis <axis>, search window
  <dates>, recorded at <path>.
Risk     <n>/5, set by <component>, reason <one line>.
Grid position: novelty <n>, risk <n> -> <proceed | proceed with pilot | reduce scope | drop>
Fallback contribution: <the weaker true claim, or "none - reconsider the idea">
```
