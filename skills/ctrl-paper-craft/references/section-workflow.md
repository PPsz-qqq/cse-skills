# Section-by-section workflow

Write a manuscript section by section, with an acceptance test per section and an explicit list of
what must not appear. A section is done when a reader can state its claim without reading the
next one, and when every sentence in it is supported by an artifact or a citation.

Draft order differs from reading order. Write the method first, then the experiments, then the
related work, then the introduction, then the abstract, then the title. The abstract is written
last because it summarizes claims that must already exist.

## Title

**Job.** Name the contribution precisely enough that the right reader recognizes it and the wrong
reader skips it.

**Acceptance criteria.**
- The axis is recognizable from the title, either by the task name or the mechanism name.
- Neither a bare task name nor a bare mechanism name alone. A title needs a claim-bearing element.
- No unexpanded acronym other than terms the axis community reads as words.
- Under about 15 words for vision venues, under about 20 for control venues, and short enough to
  survive an index entry.

**What must not appear.** `A Novel`, `An Effective`, `Towards`, `Rethinking` unless the paper
actually rethinks something specific, a method named after an acronym invented for the paper, a
question mark, and any superlative.

## Abstract

**Job.** State the problem, the gap, the contribution, the evidence, and the boundary in a
self-contained block that a reader can act on without the paper.

**Acceptance criteria.**
- Every number in the abstract appears identically in the body, at the same precision
  ([reconciliation-and-notation.md](reconciliation-and-notation.md)).
- Every abstract result number has a checked G2 ledger row; comparative claims are `comparable`,
  and absolute non-comparative values use `NOT_APPLICABLE` with a reason.
- The contribution is stated as what was done, not as what was avoided.
- The boundary is present: dataset, scenario, or run count sufficient to prevent over-reading.
- One claim per sentence. The last sentence states the consequence or the boundary, not a
  promise.

**What must not appear.** A number with no protocol, `state-of-the-art` without a matched
comparison, an unbounded `first to` (only a bounded search finding is allowed, per
[verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md)),
`significantly` without a test, a field claim supported by simulation, a citation, and any
sentence that is only true if the reader skips the experiments section.

See [abstract-template.md](abstract-template.md) for the worked structure.

## Introduction

**Job.** Earn the reader's next ten minutes. Establish the problem, show why the obvious approach
is insufficient, state the contribution, and give the evidence summary.

**Acceptance criteria.**
- Paragraph 1 states the task and why it matters in the axis community's terms, with citations.
- Paragraph 2 states the specific limitation of the current best approaches, with the nearest
  competitor named.
- Paragraph 3 states the idea in one sentence a reader could repeat.
- A contribution list of three to four items, each with the artifact that supports it, each
  naming an experiment or a table.
- A figure that shows the mechanism, not the pipeline of standard components.
- The `创新点` for a Chinese-language venue is stated as an explicit numbered list, not buried in
  prose (`../../ctrl-shared/core/venue-matrix.md`).

**What must not appear.** A contribution list item with no corresponding experiment; a claim of
novelty without a documented search; a promise about future work; a review of the whole field,
which belongs in the related work; a comparison to a baseline that the experiments never run;
`to the best of our knowledge` used to launder an unverified novelty claim.

## Related work

**Job.** Position the contribution against the nearest work so precisely that a reviewer who knows
those papers cannot object to the characterization.

**Acceptance criteria.**
- Organized by the distinction that matters to this paper, not by chronology and not by a list of
  methods.
- Every nearest competitor is named and its precise difference from this work is stated in one
  sentence.
- Copied numbers carry their protocol differences ([related-work.md](related-work.md)).
- The gap the paper fills is stated last, and it follows from the specific differences above it.

**What must not appear.** A paragraph that only summarizes; a mischaracterization of a cited
method, including a straw-man version of it; `similar to` with no stated difference; a citation
known only by title used to support a specific claim (`ctrl-shared` `core/evidence-integrity.md`
Rule 10); a claim that a contemporaneous work is inferior.

## Method

**Job.** Let a competent reader re-implement the method, and let them see why each design choice
follows from the problem.

**Acceptance criteria.**
- Notation defined at first use and consistent with `../../ctrl-shared/core/terminology-and-notation.md`
  or with the user's existing consistent set.
- Every symbol in every equation appears in the text, and every symbol in the text appears in an
  equation or a table.
- Every design choice is either derived from the problem or measured in the ablation, and the text
  says which.
- Complexity or cost analysis where the claim involves cost: parameters, FLOPs, messages per step,
  or per-update arithmetic.
- Implementation details sufficient for re-implementation, with the details that change results
  stated rather than left to released code.

**What must not appear.** Motivation by assertion, such as `intuitively, this module captures
richer features`; a component whose only justification is that it improved the metric, presented
as a mechanism; an equation whose variables are never defined; a hyperparameter value with no
statement of how it was selected; a claimed theoretical property without a proof or a citation to
one.

## Experiments

**Job.** Present the evidence that the claims hold and the conditions under which they do not.

**Acceptance criteria.**
- Every comparison carries its protocol block from
  [protocol-blocks.md](../../ctrl-experiment-suite/references/protocol-blocks.md), in the text or
  in an appendix referenced from the table.
- Every headline number has a dispersion or an explicit `single seed` label.
- Ablations isolate each claimed component, and null results are present and discussed.
- The failure analysis is present: a scene, class, or condition where the method loses.
- Limitations stated as findings, with the boundary the reader should apply.
- Reproducibility details present or pointed to: commit, config, split id, seeds, hardware,
  command.

**What must not appear.** A delta where the protocol differs; a bolded best value that is not the
best under a matched protocol; `we outperform` against a number that was copied under another
protocol; a table without its source data; a result whose run count is unstated; a hyperparameter
selected on the reported split; a metric changed after seeing it did not favor the method.

## Discussion

**Job.** State what the results mean, where they stop meaning anything, and what would falsify
them. Distinct from the conclusion, which restates the contribution.

**Acceptance criteria.**
- Each interpretation is tied to a specific measured result, not to the method's design intent.
- The mechanism claim is separated from the empirical finding, and its evidence class is stated.
- Generalization limits named: dataset, sensor, geography, node count, noise regime, hardware.
- Threats to validity, including any selection or tuning that could inflate a number.
- Negative and null results discussed here and in the ablation table, not only in a footnote.
- Honest comparison of cost against the baseline, including where the method is worse.

**What must not appear.** Speculation presented as a finding; a claim about a scenario that was
never run; `this suggests that our method generalizes`; an explanation invented for a gain that
the ablation did not isolate; a limitations paragraph that only lists future work.

## Conclusion

**Job.** Restate the contribution and the evidence in one short block, and name the next honest
step.

**Acceptance criteria.**
- Numbers in the conclusion match the abstract and the tables exactly.
- One or two sentences on impact, bounded by the validity limits already stated.
- Future work that follows from an identified boundary, not a wish list.

**What must not appear.** A new claim, a new number, a new citation, an expanded superlative, or a
restatement of the abstract in different words with a stronger adjective.

## Section order and length control

Adjust to the venue's structure and page budget ([axis-writing-guides.md](axis-writing-guides.md)).

| Section | Share of the body | Fails when |
|---|---|---|
| Introduction | 10 to 15 percent | the contribution list appears after page 2 |
| Related work | 10 to 15 percent | it reads as a list of summaries |
| Method | 25 to 35 percent | the mechanism figure is missing, or the section is a component catalogue |
| Experiments | 30 to 40 percent | protocols are in the text but not next to the numbers |
| Discussion | 5 to 10 percent | limits are stated but not tied to results |
| Conclusion | under 5 percent | it contains a new claim |

A `filt` or `cnav` theory paper inverts the method and experiments shares, with proof detail in
the method or an appendix and simulation as illustration. A system paper in the robotics class
moves budget into a hardware section and a failure analysis.

## Per-section self-check

```text
[ ] Title states the contribution, with no marketing adjective
[ ] Abstract numbers match the body exactly, and every one has a comparable ledger row
[ ] Introduction contribution list items each name their experiment
[ ] Related work names the nearest competitors and states a precise difference for each
[ ] Method defines every symbol and justifies every choice as derived or measured
[ ] Experiments carry a protocol block per comparison and a dispersion per headline number
[ ] Discussion ties every interpretation to a measured result and states the limits
[ ] Conclusion introduces nothing new
[ ] Every claim's strength matches its promotion condition in ctrl-shared verdicts-and-loops
[ ] Simulation and field results are labeled in prose and in captions
```
