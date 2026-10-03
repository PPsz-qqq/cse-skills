# Contribution typing

The contribution type determines the evidence bar, the venue class, and the sentence that may appear
in the abstract. Choosing it late, or choosing it to sound impressive, is the most expensive mistake
in this pack because it fails G0 and invalidates everything downstream.

## The five types

| Type | The claim is | Required evidence | Typical venue class |
|---|---|---|---|
| Empirical delta | a named method reaches a higher value than named alternatives under a matched protocol | a protocol-matched comparison against named baselines, seeds and dispersion, and a statement of what the delta does not generalize to | A, B, C |
| Mechanism | the gain comes from a specific component, and we can say why | an ablation chain isolating that component under one protocol, plus a prediction about where the effect should and should not appear, tested | A, B |
| Theory | a proved property of a formulation: stability, convergence, an optimality condition, a bound | a complete proof, assumptions stated as assumptions, and a demonstration that the assumptions hold or are violated in the intended setting | B |
| System | an integrated system that works on hardware, under stated conditions | a running integration, hardware and calibration detail, timing on the named platform, and failure cases | B, C |
| Survey | a characterization of the field that others can act on | a documented, reproducible search, a MECE taxonomy, and a synthesis that is a judgement rather than a listing | A, C, D |

A paper may have a primary type and a secondary one. When it does, the primary type sets the bar and
the secondary type is supported additionally. Do not average the two bars.

## Type-specific evidence requirements in this pack

### Empirical delta

- The comparison protocol block for the active axis, from
  [../../ctrl-shared/core/gate-contract.md](../../ctrl-shared/core/gate-contract.md), completed for
  every arm.
- Seeds and dispersion per
  [../../ctrl-shared/core/evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md) rule 5.
- A statement of the absolute-or-relative form of every percentage.
- The claim in the abstract must be the weaker true statement if the protocol could not be matched on
  any arm.

The bar is a matched comparison. If the only available baseline numbers are copied from papers with
different resolutions, different pretraining data or a different detection source, the honest output
is a table of `not comparable` rows, and the delta claim is not available. This is common in `det`,
`track` and `reid`, and it is why the axis calibration table exists.

### Mechanism

- An ablation chain with baseline, baseline plus one component, and the full method, all at the same
  budget. An ablation run at a different budget is a second experiment, not an ablation.
- A predicted interaction, tested. If components are claimed to be complementary, the interaction
  must be shown, not asserted.
- A statement of what the ablation does not establish. A component that improves the metric with an
  unexplained mechanism is an empirical finding.

### Theory

- Assumptions stated as numbered assumptions with their role in the proof, and a statement of which
  of them is most likely to be violated in practice.
- The main result proved, with the proof either closing in the paper or in a supplement that closes.
- A bound or a limit compared against, where one exists. For `filt`, consistency is the operational
  test, namely NEES or ANEES against its chi-square bounds with the Monte Carlo count stated.
- A demonstration that does not overclaim. For control venues, simulations illustrate the theory;
  they do not establish it.

### System

- An integration that runs, not a block diagram. The evidence is a logged run, with the platform,
  the sensor configuration, and the timing.
- Hardware named exactly: the model, the memory, and the power mode. Throughput without the part
  number is not a measurement.
- Failure cases, with the conditions that produced them.
- A stated gap between the field or hardware setting and any simulation. A system claim built on
  simulation is a simulation claim, and the wording must say so.

### Survey

- A reproducible search: sources, queries, date windows, screening criteria, and the number of items
  at each stage.
- A taxonomy that is MECE with respect to the stated axes, with the placement rule stated so a reader
  can place a new paper.
- A synthesis that takes positions: which approaches work in which regimes, and what the evidence
  does not support. A listing organized by year is not a survey.

## The downgrade rule

When the required evidence for the chosen type cannot be obtained within the resources, downgrade the
type and record the downgrade explicitly. Never keep the type and soften the wording.

```text
Downgrade record
- From: <type>   To: <type>
- Reason: <the specific missing evidence and why it cannot be obtained in the available resources>
- Consequence for the abstract: <the sentence that must change>
- Consequence for the venue: <whether the venue class changes>
- Recorded on: <date>
```

Common downgrades in this pack, with the reason they are usually correct.

| Apparent type | Usually actually | Trigger |
|---|---|---|
| mechanism | empirical delta | no ablation isolating the component |
| theory | empirical delta | the proof depends on an assumption that the target scenario violates, and the paper does not test that |
| system | empirical delta with a system section | the integration is simulated, or the hardware detail is insufficient to reproduce the timing |
| survey | annotated bibliography | the output is organized but takes no positions |
| empirical delta | a negative or null result | the matched comparison does not favour the method; this is still publishable, and the framing must change to the mechanism of the failure |

The last row is the one most often mishandled. A refuted hypothesis with a clean, well-controlled
comparison is a finding. Reporting it as a finding in the limitations section, while the abstract
claims a delta, is the integrity failure that reviewers catch.

## Mapping type to venue and to framing

| Type | Framing that works | Framing that fails |
|---|---|---|
| Empirical delta | "under protocol P, method M reaches X against baselines A and B; the delta holds on datasets D1 and D2" | "a novel framework that achieves state-of-the-art performance" |
| Mechanism | "the gain comes from component C; removing C removes the gain, and the prediction for regime R holds" | "an effective module that can be plugged into any detector" |
| Theory | "under assumptions A1 to A3, the estimator is consistent, and the assumption most at risk is A2" | "a theoretically grounded approach" |
| System | "the system runs at N hertz on platform P with sensor set S, and degrades in the following conditions" | "a complete solution for autonomous navigation" |
| Survey | "we characterise the field along three axes; the placement rule is R; the evidence does not support claims C1 and C2" | "a comprehensive review of recent advances" |

## Diagnostic questions

Ask these before freezing G0.

1. What is the one sentence a reviewer will repeat when describing this paper to a colleague? If it
   is a topic rather than a result, the type is wrong.
2. Which evidence, if removed, makes the paper unpublishable? That is the evidence the type requires,
   and it must be in the plan by name.
3. If the main hypothesis is refuted, what is left? If the answer is nothing, add a fallback
   contribution now, per [novelty-and-risk.md](novelty-and-risk.md).
4. Could a competitor produce the same claim with less work? If yes, the idea is not yet a
   contribution.
5. Does the claim type match the venue class the work will be sent to? A theory claim sent to a
   vision venue, or an empirical delta sent to TAC, is a scope error, not a quality problem.
