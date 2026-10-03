# Contribution framing and venue mapping

The claim type decides the framing, the evidence requirement, and the venue. Getting this wrong is
the most expensive early mistake, because it is discovered after the experiments are run.

Claim promotion conditions come from `../../ctrl-shared/core/verdicts-and-loops.md`. A statement may
be written no more strongly than its tier permits. When the condition is unmet, write the weaker
true statement and delete the stronger wording rather than hedging it.

## The five claim types

| Claim type | The paper says | Required evidence | Venue classes |
|---|---|---|---|
| Empirical delta | our method reaches `<value>` on `<benchmark>` under `<protocol>` | a matched-protocol comparison, at least 3 runs, dispersion, an ablation chain | A, C, D, and B for `filt` and `cnav` benchmarks |
| Mechanism | the gain comes from `<component>`, because `<reason>` | an ablation isolating that component under one protocol, plus a measurement of the mechanism itself | A, B, and D when the mechanism is the innovation |
| Theory | under `<assumptions>`, `<property>` holds | a complete proof, assumptions that can fail, and an illustration that is not the evidence | B, and A for the learning-theoretic end |
| System | the system runs on `<platform>` and achieves `<value>` in `<conditions>` | an integration that runs, hardware validation, calibration, runtime, failure cases | B robotics, C for sensing, D |
| Survey | the literature supports `<structured finding>` | a documented search protocol, coverage evidence, and a taxonomy that explains something | A journals, D, and dedicated survey venues |

Rules that hold across all five.

- One paper has one primary claim type. Secondary claims inherit the primary type's evidence bar.
- A delta may not be framed as a mechanism. `Our module improves mAP by 1.2` is a delta.
  `The gain comes from better scale handling` is a mechanism and needs its own measurement.
- A simulation may not be framed as a field result. The promotion condition for `in the field` is
  field data with the platform and conditions stated.
- A theory paper's simulation is an illustration. Presenting it as the evidence inverts the paper.
- A system paper's block diagram is not the contribution. The contribution is that it runs.

## Framing a delta honestly

The template below produces a claim that cannot be over-read. Fill every slot or the claim is not
ready.

```text
On <dataset, split>, under <protocol id>, our method reaches <value> <units>
(mean over <N> runs, <dispersion statistic> <dispersion value>),
compared with <baseline> at <value> under the same protocol,
a difference of <delta> <units> (<absolute | relative>),
with a <level> <interval method> interval of <low, high>.
<The interval excludes zero | The interval contains zero, so the difference is not established>.
```

Write the last line whichever way it comes out. `The interval contains zero` belongs in the paper.

Escalation ladder for an empirical claim. Move up only when the condition is met.

| Rung | Wording permitted | Condition |
|---|---|---|
| 1 | `in our experiments, <value>` | one recorded run exists |
| 2 | `our method reaches <value> +- <dispersion>` | at least 3 runs, seeds listed, dispersion reported |
| 3 | `our method outperforms <baseline>` | the baseline comparison is protocol-matched |
| 4 | `evaluated on <named datasets>` | both protocols complete; a generalization claim additionally needs a defined transfer/domain-shift test |
| 5 | `no directly overlapping work retrieved within <search scope>` | recorded recent and foundational search, near misses and coverage limits; not an unbounded first claim |

Never skip a rung. `Outperforms` at rung 3 with a single seed is a rung-1 result with rung-3
wording, and it is the defect that turns a minor revision into a rejection.

## Framing a mechanism

A mechanism claim consists of three parts, and all three must be present.

1. **Attribution.** The component causes the gain. Evidence: a singleton ablation arm under the
   same protocol as the full method.
2. **Interaction.** The component's contribution survives the presence of the others, or the
   interaction is stated. Evidence: the interaction arm.
3. **Mechanism measurement.** The proposed reason is itself measured, not inferred. If the claim
   is that the module improves scale invariance, the paper reports a scale-stratified result. If
   the claim is that the estimator handles non-Gaussian noise, the paper reports the noise regime
   where it holds and where it stops.

Missing part 3 is the common case. Without it, the honest sentence is `the component improves
<metric> under this protocol and we did not isolate why`, which is an empirical finding. Write
that, and put the mechanism hypothesis in the discussion as a hypothesis with the experiment that
would test it.

## Framing theory

- State every assumption, and state which of them can fail in practice.
- The proof must close. An appendix that says `the proof follows similarly` for the hard case does
  not close it.
- Simulations illustrate the theorem's regime. They do not substitute for the proof, and a
  simulation outside the theorem's assumptions must be labeled as such and explained.
- A bound, such as a `CRLB` or a posterior `CRLB`, is a reference line, not a competitor. Plotting
  it as a baseline in a comparison table is a category error.
- Consistency results, such as `NEES` against its chi-square bounds, are evidence for `filt`. Treat
  them as first-class results and give them a table, not a sentence.

## Framing a system

- The contribution is the integration, so the paper must show the integration running on the named
  platform, with the sensors, the onboard computer, and the runtime.
- Calibration and synchronization detail is part of the contribution in this class. Reviewers in
  robotics reject on missing calibration before they reject on accuracy.
- Failure cases are mandatory. A system section with no failure analysis reads as a demo.
- Field conditions are named: site, weather, lighting, traffic, GNSS availability, and the range of
  each. `Real-world experiments` is not a condition description.
- Cost is reported on the deployed platform, not on a workstation.

## Venue-class mapping

Use the class table in `../../ctrl-shared/core/venue-matrix.md` for the details, the evidence bar, and
the reviewer behaviour. The mapping from contribution to class, in the order to apply it.

1. Fix the claim type from the `G0` scope gate. A theory result, an empirical delta, a system
   demonstration, and a survey have nearly disjoint venue sets.
2. Map the claim to the venue's own stated contribution criteria, in the venue's words, and write
   the fit statement using the template in the venue matrix.
3. Check the evidence bar. If the venue requires field validation and only simulation exists,
   change venue or add the validation. Do not blur the gap.
4. Check the cycle cost against the deadline.
5. Prefer the venue whose program committee already believes the premise.

Summarized mapping, with the weightings from `../../ctrl-shared/core/review-rubrics.md`.

| Axis and claim | First-choice class | Heaviest rubric dimensions |
|---|---|---|
| `det`, `track`, `reid` with a mechanism | A, CVPR-class | D2 novelty, D4 rigor, D3 soundness |
| `det`, `track`, `reid` with a delta only | A second tier, or A with a complete multi-dataset story | D4 rigor, D3 soundness |
| `det` on remote-sensing imagery | C | D3 soundness, D4 rigor, D8 boundary honesty |
| `filt` with theory | B, TAC, Automatica | D3 soundness, D4 rigor, D1 significance |
| `filt` with an estimator and bounds | B, TSP, Signal Processing | D3 soundness, D4 rigor |
| `cnav` on hardware | B robotics, T-RO, RA-L, ICRA | D3, D4, D1 |
| `cnav` with theory | B, TAC, Automatica, CDC, ACC | D3, D4, D1 |
| any axis in a Chinese-language venue | D | D1, D2 创新点, D4 |

## Framing failures and their repairs

| Failure | Symptom in the draft | Repair |
|---|---|---|
| Delta dressed as mechanism | the introduction says `the gain comes from` and the ablation has only `full` and `baseline` | add the singleton arm or downgrade the sentence |
| Mechanism with no measurement | the paper explains a gain by a property it never measures | state the finding and move the explanation to a hypothesis |
| Simulation dressed as field | `achieves 0.3 m positioning accuracy` with no platform | add the simulation label and the gap statement, or change venue |
| System claim without integration | a block diagram and per-module evaluations | add the integrated run, or reframe as a method paper |
| Theory claim without a closing proof | assumptions in words, the hard case deferred | close the proof or state the result as the case that is proved |
| Novelty claim without a search | `the first framework to` with no near misses | document the two-cycle search or delete the claim |
| Post-hoc metric substitution | a metric introduced in the experiments section with no justification | report both metrics and state why the second was added |
| Borrowed baseline number | a competitor's published value inside the main table | mark it `reported`, show the protocol difference, and keep it out of the headline delta |

## Fit statement

Produce this before writing, and reuse it in the cover letter. It is the same block as the venue
matrix's template, filled for this paper.

```text
Target venue: <exact name, track, and year>
Venue class: <A | B | C | D | E>
Official guidelines consulted: <URL or document version, and the date checked>
Primary axis: <det | track | reid | cnav | filt>
Claim type: <empirical delta | mechanism | theory | system | survey>
Contribution framed as: <the one sentence that the venue's criteria reward>
Why this venue's reviewers will care: <two sentences in the venue's own criteria terms>
Contribution mapped to criteria: <criterion -> our contribution, one line each>
Evidence we have: <list, with tier labels>
Evidence this venue expects that we lack: <list, or none>
Closest competing papers at this venue: <citations, with how we differ>
Risk of desk rejection: <the single most likely reason, and our mitigation>
```
