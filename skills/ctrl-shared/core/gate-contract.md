# Gate contract

A gate is a checkpoint that a workflow cannot pass on assertion alone. Each gate names the
artifact that proves it, the criteria that artifact is checked against, and what happens when
it fails. Report a failed gate with the failing criterion and the smallest change that would
clear it. Never report a gate as passed because the user is in a hurry, and never downgrade a
failed integrity criterion to an advisory note.

Gate IDs are stable across the pack: `G0` scope, `G1` proposal freeze, `G2` evidence freeze,
`G3` submission readiness.

## G0 Scope gate

**Question.** What is being claimed, against what, and for whom?

**Required artifact.** A scope block of at most 12 lines containing: the research question in
one sentence; the primary axis (`det` / `track` / `reid` / `cnav` / `filt`); the claim type
(empirical delta, mechanism explanation, theoretical result, system demonstration, or survey);
the target venue or venue class; and the validity boundary.

**Passes when.** The claim type matches the evidence the user actually has or can obtain. A
"mechanism explanation" claim needs an ablation chain, not just a leaderboard number. A
"theoretical result" claim needs a proof, not a benchmark. A "system demonstration" claim
needs an integration that runs, not a block diagram.

**Fails when.** The stated claim type exceeds the available evidence class. Emit the specific
downgrade: for example, "claim type is mechanism explanation but no ablation exists; either
downgrade to empirical delta or add the ablation in `ctrl-experiment-suite`".

**Blocks.** All downstream work. An unresolved G0 wastes the entire pipeline.

## G1 Proposal freeze gate

**Question.** Is the plan specific enough to fail?

**Required artifact.** A frozen plan containing: the hypothesis in falsifiable form, the
independent and dependent variables, the datasets and splits with the exact evaluation
protocol, the baseline list with the reason each baseline is included, the ablation list, the
metrics with their definitions, the compute budget, and the pre-declared decision rule
(what result would refute the hypothesis).

**Passes when.** Every element is named specifically. "Compare with several state-of-the-art
methods" fails; "compare with ByteTrack, OC-SORT, and BoT-SORT under the private-detection
MOT17 protocol with identical detections" passes. The pre-declared refutation rule must be
written before results are seen, and it must be possible for the rule to fail.

**Fails when.** Any element is a placeholder, a TBD, or a category rather than a name. Also
fails when the decision rule is unfalsifiable, such as "if results are promising".

**Blocks.** Experiment execution and drafting. Freeze the plan in a file so that later
deviations are visible.

## G2 Evidence freeze gate

**Question.** Does every reported number exist, and does every comparison hold?

**Required artifact.** A claim-to-evidence ledger plus a protocol-matched comparison table.
Each row of the ledger carries a claim ID, the tier (`measured` / `reported` / `assumed`), the
source artifact path or citation, the exact value with units, and the validity boundary.

**Passes when.** All of the following hold.

- Every quantitative claim has a ledger row with a resolvable source.
- Every reported delta was produced under a matched protocol. Where the protocol could not be
  matched, the delta is reported as `not comparable` with the reason.
- Every headline number agrees with the artifact it came from, and aggregate numbers
  reconcile with the per-item numbers they summarize.
- Seed count, variance, and selection rule are stated for any stochastic result.
- Each axis-specific evidence rule is satisfied for the active axes.

**Fails when.** Any claim is unsourced, any comparison is protocol-mismatched and still
presented as a delta, any number fails reconciliation, or any axis rule is unmet. A failed G2
is blocking and cannot be waived; the remedy is to remove the claim or produce the evidence.

**Blocks.** Manuscript drafting, review, rebuttal, and slide generation.

## G3 Submission readiness gate

**Question.** Would this survive its own reviewer?

**Required artifact.** A readiness record containing: the venue fit statement mapping the
contribution to that venue's stated criteria; the anonymization and formatting check; the
reproducibility package inventory (code, configs, seeds, dataset instructions, license
compatibility); the limitations section; the ethics and dual-use statement where applicable;
and a resolved list of every blocking concern raised by `ctrl-pre-submission-review`.

**Passes when.** No unresolved blocking concern remains, the contribution maps to the venue's
criteria in the venue's own terms, and every claim in the abstract is supported by a G2-passed
ledger row.

**Fails when.** Any blocking concern is open, the abstract contains a claim absent from the
ledger, or the reproducibility package cannot reproduce a headline number on the authors'
own hardware.

**Blocks.** Submission. Also blocks `ctrl-paper-to-slides` from presenting unready results as
final.

## Gate reporting format

Use this block whenever reporting gate status, in any skill.

```text
Gate <ID> <name>: PASS | FAIL | BLOCKED
- Checked: <criteria evaluated>
- Artifact: <path or inline block>
- Failing criterion: <one line, only when not PASS>
- Smallest clearing change: <one line, only when not PASS>
- Waiver: none | <explicit user decision with scope and residual risk>
```

A waiver is permitted only for G0 and G3, only on explicit user instruction, and must be
recorded with its residual risk. G2 has no waiver path.

## Axis-specific gate addenda

These extend G2. Run the addendum for each active axis.

| Axis | Additional G2 requirement |
|---|---|
| `det` | Comparison protocol block: backbone, pretraining data, input resolution, augmentation, training schedule, test-time augmentation, single or multi-scale inference, NMS or NMS-free, and evaluation server versus local split |
| `track` | Detector provenance for tracking-by-detection, public versus private detection protocol, online versus offline setting, and reported FPS with the exact GPU |
| `reid` | Evaluation protocol block: backbone and pretraining, image resolution and crop policy, re-ranking on or off, query/gallery construction, and single-query versus multi-query |
| `cnav` | Distribution proof: which nodes compute, what is exchanged, and whether any central node or global state exists; plus communication model with delay and loss |
| `filt` | Consistency evidence: Monte Carlo count, NEES or ANEES against its chi-square bounds, and the bound used for comparison |
