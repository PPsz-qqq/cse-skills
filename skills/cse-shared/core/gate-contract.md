# Gate contract

A gate is passed by a checked artifact, never by assertion. Report an unmet criterion and the
smallest clearing change. Deadline pressure cannot change an evidence requirement.

Gate IDs are stable: `G0` scope, `G1` proposal freeze, `G2` evidence freeze, `G3` submission
readiness. Apply them to dependent actions, not to every conversation. See
[execution-contract.md](execution-contract.md) for task modes and capability limits.

## Applicability and precedence

- Literature discovery, draft planning, local editing and diagnostic review may proceed without
  passed gates. They must not promote unverified results, call a draft frozen, or declare readiness.
  In particular, diagnostic review does not require G2 PASS: missing evidence is a review finding.
- Check only criteria applicable to the claim type and active axes. For theory, inspect assumptions,
  proof and counterexamples; for systems, integration evidence; for surveys, search and synthesis.
  Record inapplicable experimental fields as `NOT_APPLICABLE` with a reason, not invented runs.
- Missing required inputs are `BLOCKED`, evaluated unmet criteria are `FAIL`, and a failed
  evaluation tool is `ERROR`. These are not interchangeable and none is a pass.
- G1 applies prospectively to confirmatory experiments. Existing unregistered work can be audited
  and reported as exploratory; never invent a past freeze date.
- A gate verdict is valid only for its recorded scope and input revisions. A scoped G2 PASS for C1
  does not clear C2 or grant whole-manuscript G2 PASS. Downstream work uses only checked claims.
- Explicit user waivers are allowed only for G0 and G3. Log the action, scope and residual risk,
  but keep the original verdict; `waived` is not a seventh verdict or fabricated PASS. A G3 waiver
  cannot make a failed G2 claim final. G1 and G2 have no waiver path.

## G0 Scope gate

**Question.** What is claimed, against what, and for whom?

**Required artifact.** A scope block of at most 12 lines: research question, primary and
secondary axes (`det` / `track` / `reid` / `cnav` / `filt`), claim type (empirical delta, mechanism,
theory, system or survey), target venue/class, nearest competitors when relevant, available and
obtainable evidence, and validity boundary.

**Passes when.** The claim type matches the evidence available or realistically obtainable.
A mechanism needs an isolating ablation chain, a theory result a proof, and a system demonstration
an integration that runs rather than just a diagram.

**Fails when.** The claim exceeds its obtainable evidence class. State the specific downgrade,
for example mechanism to empirical delta, or the evidence that would clear the mismatch.

**Blocks.** Promotion of that claim into downstream scientific conclusions. It does not block
work to define the scope, find evidence, diagnose the mismatch or edit unchanged prose.

## G1 Proposal freeze gate

**Question.** Is the confirmatory plan specific enough to fail?

**Required artifact.** A dated frozen plan: falsifiable hypothesis, variables, named datasets
and splits, complete protocol blocks, baselines and inclusion reasons, applicable ablations,
metric definitions, seed/sample policy, statistical treatment, compute budget and decision rule.

**Passes when.** Every applicable element is specific and the decision rule was fixed before
confirmatory results were inspected. Named trackers under identical detections can satisfy the
baseline criterion; this alone is not a pass for the whole plan.

**Fails when.** A required element is a placeholder or category, the rule cannot fail, or it was
adjusted using confirmatory outcomes and still described as pre-declared.

**Blocks.** Confirmatory execution under that plan and claims of pre-registration. Exploratory
pilots are permitted before G1 only with a recorded question, budget and stop mechanism; retain
their influence on the final plan. They cannot be relabelled confirmatory after inspection.

## G2 Evidence freeze gate

**Question.** Does each in-scope claim have evidence, and does each comparison hold?

**Required artifact.** Claim-to-evidence ledger with exact source revisions and applicable
protocol blocks/comparison tables, following [artifact-contract.md](artifact-contract.md).

**Passes when.** All applicable checks hold:

- Every in-scope quantitative or substantive scientific claim resolves to checked evidence.
  Assumptions are documented as assumptions, not promoted into demonstrated outcomes.
- Every claimed performance delta uses a matched protocol. Unmatched rows may be reported
  separately with their values and differences, but not as an improvement or delta claim.
- Headline values agree with raw artifacts or primary sources; aggregates reproduce under the
  declared aggregation rule. User-supplied values alone are not independently verified artifacts.
- Stochastic results state run count, dispersion, seed/sample policy and selection rule.
- Active-axis evidence obligations are satisfied where applicable to the claims.

**Fails when.** A checked source contradicts a claim, an unmatched comparison is presented as a
win, reconciliation fails, or an applicable evidence requirement is unmet. If the necessary source
is unavailable, record `BLOCKED` instead of inventing its contents. No waiver is possible: obtain
evidence or withdraw/narrow the claim, retaining the historical ledger row and reason.

**Blocks.** Promotion of unverified claims as established results in manuscripts, final letters
or quantitative slides. Does not block a diagnostic review, provisional response, outline or
clearly marked draft with missing evidence exposed.

## G3 Submission readiness gate

**Question.** Is the exact submission package ready under the venue's current requirements?

**Required artifact.** Readiness record: verified venue fit/guidelines, anonymization/formatting,
applicable reproducibility inventory, limitations, ethics/dual-use where relevant, and resolution
records for blocking concerns. A full-paper decision requires full-paper assessment.

**Passes when.** No unresolved blocking concern remains, venue criteria are met, and every
abstract/final-result claim is supported by current G2-checked evidence for that claim.

**Fails when.** Blocking concerns remain, abstract claims lack evidence, formatting/anonymity
requirements are unmet, or an applicable headline result cannot be reproduced from the inventory.

**Blocks.** Declaring the package ready for submission. A slide deck may be built before G3 but
cannot present the package as ready; preliminary results are explicitly labelled. Submission or
external sending always needs the user's authorization; a skill gate is not permission to send.

## Gate reporting format

Use the six verdicts from [verdicts-and-loops.md](verdicts-and-loops.md). `WARN` means a met
criterion with a non-blocking defect; it cannot replace an integrity failure.

```text
Gate <ID> <name>: PASS | WARN | FAIL | BLOCKED | ERROR | NOT_APPLICABLE
- Scope: <claims, comparisons or package evaluated>
- Checked: <criteria actually evaluated>
- Artifact: <path or inline block, exact revision/hash>
- Freshness: current | STALE
- Failing criterion or missing input: <when not PASS, or reason for NOT_APPLICABLE>
- Smallest clearing change: <action, when needed>
- Waiver: none | <explicit user decision, scope and residual risk; verdict unchanged>
```

Append historical entries; do not rewrite a past verdict after the source changes.

## Axis-specific G2 addenda

Apply these to relevant empirical claims, not mechanically to a proof-only or survey claim.

| Axis | Additional evidence requirement |
|---|---|
| `det` | Backbone, pretraining, resolution, augmentation, training schedule, TTA, inference scales, NMS/NMS-free and evaluation split; isolate the claimed intervention |
| `track` | Detector provenance for tracking-by-detection, public/private and online/offline setting; throughput scope and exact hardware for FPS claims |
| `reid` | Backbone/pretraining, resolution/crop, re-ranking, query/gallery construction and query mode |
| `cnav` | Which nodes compute/exchange what, any central/global state, communication delay/loss and simulation/field setting |
| `filt` | Monte Carlo count and applicable covariance consistency evidence; NEES/ANEES with distribution/independence assumptions, confidence level and correctly scaled bounds |
