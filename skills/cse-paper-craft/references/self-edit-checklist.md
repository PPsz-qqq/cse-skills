# Self-edit checklist

A structured pass over a draft before it goes to review. Work top to bottom, record a verdict per
block, and do not skip a block because the draft looks clean. The sections that catch the most
rejections are the claim-strength block and the protocol block.

Use the effort tiers from `../../cse-shared/core/verdicts-and-loops.md`. A single-section request is
`sketch`; a full manuscript pass before a deadline is at least `thorough`.

## Pass 0, scope and claim type

```text
[ ] The research question is one sentence and falsifiable
[ ] The primary axis is stated, and secondary axes are listed
[ ] The claim type is one of: empirical delta, mechanism, theory, system, survey
[ ] The claim type matches the evidence that exists
[ ] The target venue class is fixed and the fit statement is written
[ ] The validity boundary is stated somewhere in the paper, not only in the limitations
[ ] The contribution list and the experiments are one-to-one
```

If the claim type exceeds the evidence, stop here and emit the downgrade. Continuing to draft on a
claim the evidence cannot support wastes every later pass.

## Pass 1, claim strength

```text
[ ] Every `outperforms` has a protocol-matched comparison against that specific baseline
[ ] Every `significantly` has a named test and its result
[ ] Novelty uses a bounded search finding, with recent/foundational work and near misses; two cycles do not prove first
[ ] Every `in the field` or hardware claim traces to field or hardware data
[ ] Every `the gain comes from` traces to a singleton ablation arm
[ ] Every `robust` names the perturbation class
[ ] Every `generalizes` has a defined transfer/domain-shift test and no target-test leakage, not just two trained datasets
[ ] No claim was strengthened between rounds without new evidence
[ ] No hedge was added to keep a stronger wording alive
```

## Pass 2, protocol adjacency

```text
[ ] Every comparison has a complete protocol block for its axis
[ ] Every table caption carries the axis-critical labels
[ ] Every `not comparable` value is marked where it appears
[ ] Every copied baseline value shows the published value beside the re-implemented one
[ ] No bolded value is `not comparable` or non-best under a matched protocol
[ ] Every claim's protocol id resolves to a block that exists
```

## Pass 3, numbers

```text
[ ] The number inventory is complete, not sampled
[ ] Abstract, tables, captions, and conclusion agree at one precision and one unit
[ ] Every average reproduces from the per-item values, or the aggregation rule is stated
[ ] Every percentage states absolute or relative
[ ] Every stochastic number states its run count, seed policy, and dispersion
[ ] No single-seed number is presented as stable
[ ] No cell was filled by estimation, interpolation, or memory
```

Run the full procedure in [reconciliation-and-notation.md](reconciliation-and-notation.md) for a
submission-tier pass.

## Pass 4, structure and argument

```text
[ ] The title states the contribution without a marketing adjective
[ ] The abstract has all six slots, in order, and its numbers pass Pass 3
[ ] The introduction reaches the contribution list within the first two pages
[ ] Each contribution item names its experiment or table
[ ] The related work is organized by the distinction the paper turns on
[ ] Every nearest competitor has a precise difference stated
[ ] The gap statement follows from the differences above it
[ ] The method justifies each choice as derived or measured, not by intuition
[ ] The experiments section leads with the protocol, then the numbers
[ ] The discussion separates mechanism claims from empirical findings
[ ] The conclusion introduces nothing new
```

## Pass 5, method completeness

```text
[ ] Every symbol is defined at first use and used identically
[ ] Every equation's variables appear in the text
[ ] Every hyperparameter states how it was selected
[ ] Every component claimed as a contribution has its ablation arm
[ ] Implementation detail is sufficient to re-implement, or points to released code
[ ] Cost is reported where the claim involves cost
[ ] Assumptions are stated explicitly and each can fail
```

## Pass 6, evidence integrity

```text
[ ] Every quantitative claim has a ledger row with a resolvable source
[ ] No invented citation, number, figure, hardware fact, or experiment
[ ] Every tier label is correct: measured, reported, or assumed
[ ] Negative and null results are present in the ablation and in the limitations
[ ] No losing case was removed from the evaluation set after seeing the result
[ ] No metric was redefined after seeing that the original did not favor the method
[ ] Every unverified item is visibly marked [UNVERIFIED]
[ ] Every missing item is visibly marked [MISSING: what is needed]
[ ] Read-in-full versus abstract-only citation status is recorded where the support matters
```

## Pass 7, presentation

```text
[ ] Every figure and table is cited in the text, in numerical order
[ ] Generated figures have generators/data; reused figures have source/version/credit; schematics have editable sources
[ ] Captions are self-contained and state the protocol
[ ] Axis labels carry units and the frame where one applies
[ ] Figures survive greyscale and common color-vision deficiency
[ ] Font sizes match the body after scaling
[ ] Notation is consistent across text, figures, tables, and algorithms
[ ] No em dash, en dash, or colon used as a habitual sentence connector
[ ] No emoji, no marketing adjective without an artifact behind it
```

## Pass 8, venue compliance

```text
[ ] Class and style files are the current official ones, with the version recorded
[ ] Page limit and reference treatment match the current call
[ ] Anonymity rules satisfied, including repository links and acknowledgments
[ ] Supplementary-material policy followed
[ ] Ethics and dual-use statement present where the venue requires it
[ ] Data and code availability statement present where the venue requires it
[ ] Chinese-venue requirements met: 创新点 list, both abstracts, 中图分类号, 基金项目, and references in the GB/T 7714 edition the journal names (GB/T 7714-2025 replaced the 2015 edition on 2026-07-01)
[ ] Preprint policy checked before posting
```

## Pass 9, response readiness

```text
[ ] The limitations section states what the paper does not establish
[ ] Every claim a reviewer could contest has a pointer to its artifact
[ ] The failure analysis is present and specific
[ ] The closest competing work is one the reviewer will know, and the difference is precise
[ ] The reproducibility package inventory is complete
```

## Severity and stopping

Classify every finding from the passes above as `Blocking`, `Major`, `Minor`, or `Question`, using
the definitions in `../../cse-shared/core/review-rubrics.md`. A core evidence, validity, or integrity
problem is never `Minor`.

Stop conditions, from `../../cse-shared/core/verdicts-and-loops.md`.

- The repair loop for one defect gets two attempts. After two failures, change tactic or escalate.
- The review-and-revise loop gets four rounds. Report non-convergence rather than starting a fifth.
- A defect that survives two rounds unchanged is reported with its unresolved state, not
  re-described as resolved.

## Report format

```text
Self-edit: <manuscript file and revision>
Effort tier: <sketch | standard | thorough | submission>
Passes run: <0 through 9, with any pass not applicable named and why>

Findings
| ID | Pass | Severity | Claim pointer | Evidence pointer | Finding | Smallest clearing change |
|----|------|----------|---------------|------------------|---------|--------------------------|

Counts: <blocking>, <major>, <minor>, <question>
Recommendation: <derived from the counts and the integrity rules, not chosen first>
Residual defects: <the findings that remain open, with their reasons>
Stale verdicts: <any verdict computed on an earlier revision, and what invalidated it>
```

A self-edit that reports zero findings on a first draft is almost always a self-edit that was not
run. If nothing is wrong, say which artifact you checked for each pass, so the report is auditable.
