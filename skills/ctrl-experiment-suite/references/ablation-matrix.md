# Ablation matrix design

An ablation is the only evidence that a claimed component causes the observed gain. A paper that
claims a mechanism without an ablation chain has a mechanism claim it cannot support, and `G0`
requires the downgrade to empirical delta. This file specifies how to design the matrix so that
each claimed component is isolated, how to price it, and how to report components that fail.

## The chain, not the table

Every claimed component needs a three-rung chain, all under one protocol.

| Rung | Arm | Purpose |
|---|---|---|
| 0 | baseline | the strongest thing the component could be replacing, not the weakest |
| 1 | baseline plus this component only | isolates the component's own contribution |
| 2 | full method | shows the component in its claimed context |

The delta that belongs to a component is `rung 1 minus rung 0`. The delta from `rung 2 minus
rung 1` belongs to the remaining components together, not to this one. Presenting `rung 2 minus
rung 0` as a component's contribution is the single most common ablation defect. For a two-component
paper that means arms `{00, 10, 01, 11}` where `1` means present, and the two single-component arms
are the point of the design. Without them no component is isolated and the interaction is
unmeasured.

## One protocol rule

Every ablation arm runs under the identical protocol block from `references/protocol-blocks.md`.
The following are not ablations and must be presented as separate experiments.

- an arm trained for fewer epochs, or at a smaller resolution, because it was cheaper;
- an arm evaluated on a validation split while the full method used the test split;
- an arm with a different backbone capacity, unless the component is a capacity change;
- an arm with a different detector, tracker, dataset version, or seed list;
- an arm where the component was replaced by a stronger third-party method and the difference is
  attributed to the component.

An ablation run at a different budget from the main result is a second experiment
(`ctrl-shared` `core/evidence-integrity.md` Rule 6). If compute forces a reduced budget, state the
reduction for every arm including the baseline, label the whole table `reduced budget`, and do not
mix its numbers into the main comparison.

## Matrix construction

Use one row per arm and one column per metric, with the component configuration encoded in the
first columns. This shape makes missing arms visible.

```text
| Arm | Component A | Component B | Component C | <primary metric> | <secondary metric> | <cost metric> |
|-----|-------------|-------------|-------------|------------------|--------------------|---------------|
| B0  | -           | -           | -           |                  |                    |               |
| B0A | on          | -           | -           |                  |                    |               |
| B0B | -           | on          | -           |                  |                    |               |
| B0C | -           | -           | on          |                  |                    |               |
| B0AB| on          | on          | -           |                  |                    |               |
| FULL| on          | on          | on          |                  |                    |               |
```


1. **Include every single-component arm.** The singleton arms are what make the claim an ablation
   rather than a leaderboard entry.
2. **Include the interaction arm for every pair claimed complementary.** If the paper says A and B
   are complementary, `B0AB` against `B0A` and `B0B` is the evidence.
3. **Price every arm.** A cost column measured the same way for all arms prevents the `better but
   five times slower` rebuttal. Choose per axis: parameters, GFLOPs, latency on a stated device,
   messages per step, or bytes per step.
4. **Keep the arms on one seed list.** Where compute forbids it, run every arm on the same reduced
   list and state the reduction, rather than running the proposed arm on more seeds.
5. **Pre-declare the decision rule for each component.** Before running, write what result would
   count as the component working and what would count as it failing. In `filt` and `cnav`, write
   whether the criterion is on the error metric, the consistency metric, or the communication cost.
6. **Cap the matrix before running it.** Declare the maximum arm count in `ctrl-plan.md`. A matrix
   that grows after results are seen is a search, and its best cell is a selected maximum.

For an `n`-component paper with all interactions the arm count is `2^n`. Beyond 4 components, use
the singleton arms plus the full method plus the pairs you actually claim, and say in the text that
higher-order interactions were not measured.

## Interaction effects

An interaction exists when the gain from A depends on whether B is present. Report it explicitly.

```text
delta(A | B off) = B0A - B0
delta(A | B on)  = B0AB - B0B
interaction      = delta(A | B on) - delta(A | B off)
```

Write the interaction with its dispersion, and state whether the interval contains zero. Three
outcomes are reportable and all three are useful. An interaction interval containing zero is
**inconclusive**, not proof of additivity or independence; additivity needs a pre-declared margin
and a sufficiently narrow equivalence interval. No synergy is established by a null test. A
**super-additive** interaction is positive with an interval excluding zero, and it is the only
evidence that supports a complementarity claim. A **sub-additive or antagonistic** interaction
means one component's gain shrinks or reverses when the other is present; report it, because it is
often the most informative cell in the table and it usually means the two components do the same
job. A complementarity claim with no interaction measurement is not a claim, it is a hope expressed
in the discussion.

## Reporting a component that does not help

The null ablation is a result, not a failure of the work.

1. Keep the row. Do not delete it and do not move it to an appendix to reduce its visibility.
2. Report the delta with its interval, and state that the interval contains zero under this
   protocol at this run count.
3. State what the component was supposed to do and what the evidence shows it does not do.
4. Keep it in the method section as a component, or remove it from the method and describe it as an
   investigated variant. Do not keep it in the method while the ablation shows it is inert.
5. If the component was the headline, reframe the contribution before drafting continues. Reopen
   `G1`; do not write the abstract around the null.

A reported null ablation costs one paragraph. A hidden one costs the paper when a reviewer
reproduces it.

## What the ablation does not establish

Write this paragraph, or its equivalent, in the experiments section. It is required by
`ctrl-shared` `core/evidence-integrity.md` Rule 6.

- The ablation shows that the component is necessary for the measured gain under this protocol.
- It does not show why, unless a separate measurement isolates the mechanism.
- It does not establish that the component is necessary in general, only on this data, at this
  resolution, with this backbone, at this run count.
- It does not rule out that a simpler substitute achieves the same gain. Naming the substitute
  that was not tried is itself useful content.

The distinction that must be preserved: a component that improves the metric and whose mechanism
is unexplained is an empirical finding. Writing it as a validated mechanism is the claim
promotion that `ctrl-shared` `core/verdicts-and-loops.md` forbids.

## Per-axis ablation notes

### `det`

- The standard components are a neck, a head, an assignment rule, a loss term, and a data
  augmentation. Assignment and loss changes usually interact strongly, so the pairwise arm is not
  optional.
- Report whether an ablated variant changes inference-time cost or only training-time cost, because
  a training-only component with a gain has a different claim than one that raises latency.
- Never ablate by changing the input resolution, because resolution is a protocol field. A
  resolution sweep is a separate experiment under its own protocol blocks.

### `track`

- Ablate association, motion model, and any learned appearance term separately, and report `AssA`
  and `IDSW` as the primary evidence, not `MOTA`, because detection quality dominates `MOTA`.
- The detector is not an ablation component. Changing the detector changes the protocol. If the
  detector is the contribution, state it as a `det` result with a `det` protocol block.
- Include the "detections only, no tracker" arm where the metric permits. It bounds how much of
  the result is detection.

### `reid`

- Ablate the sampling strategy, the loss terms, the attention or part module, and any re-ranking.
  Re-ranking is not a component of the trained model and must be reported as an evaluation setting
  applied to all arms or to none.
- Report both `mAP` and `Rank-1` for every arm, because components that help retrieval depth and
  components that help top-1 accuracy are different components.
- State whether the ablation arms were trained with the identical sampler and batch composition. A
  changed batch composition is a changed protocol.

### `cnav`

- Ablate the estimator, the message content, the update schedule, and the consistency or outlier
  handling, and price each arm in bytes per agent per step. An arm that improves accuracy by
  exchanging more data is a trade, not a win.
- Include the centralized reference as a bound on what the information could achieve. Label it
  `centralized upper bound` and never enter it as a distributed arm.
- Include the dead-reckoning arm, which defines the value of cooperation at all.
- Report the scaling arm over `N`. A method that helps at `N = 4` and stops helping at `N = 20` has
  a stated boundary, and reviewers in this field ask for it.

### `filt`

- Ablate the estimator structure, the noise adaptation, the outlier rejection, and the
  initialization, reporting both RMSE and the consistency metric for every arm. A structural change
  that improves RMSE while breaking `ANEES` bounds is not a better filter.
- Never retune per-arm covariances inside an ablation comparison. If adaptation is the component,
  the adaptive arm tunes online and the baseline keeps fixed covariances, and that difference is
  the point.
- Include a single-trajectory illustration only as a qualitative companion. It is not an ablation
  arm and carries no statistical weight.
- Where a bound exists, plot it on the same axes as the arms, because reporting RMSE against the
  `CRLB` and against baselines in separate figures hides whether the proposed estimator is near the
  bound or merely near its baseline.

## Ablation pre-flight checklist

```text
[ ] Every claimed component has a singleton arm
[ ] Every pair claimed complementary has an interaction arm
[ ] Every arm runs under one identical protocol block, or the deviation is declared per arm
[ ] Seed list is identical across arms, and printed
[ ] Decision rule per component was written before the runs
[ ] Arm count is inside the budget declared in ctrl-plan.md
[ ] A cost metric is measured for every arm on the same device
[ ] Null and negative components are present, reported, and discussed
[ ] The "what this does not establish" paragraph is drafted
[ ] Interaction effects are computed with intervals, not asserted from the table
[ ] Ablations are not mixed with protocol changes such as resolution or backbone
```
