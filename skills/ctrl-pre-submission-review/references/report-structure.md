# Report structure

How to write the reviewer report, the concern record, the synthesis, and the forensic consistency
pass. The concern record field list is normative in
[review-rubrics.md](../../ctrl-shared/core/review-rubrics.md). This file says what to put in each
field and what to leave out.

## Voice

Write the way a competent, busy referee writes. Specific, signed by no one, and free of theatre.

- State the defect, the pointer, and the consequence. Stop there.
- No rhetorical escalation. "The comparison is unmatched" is a finding. "This is a serious
  methodological failure that undermines the paper's credibility" is performance.
- No praise padding. A sentence of genuine positive assessment per report is useful to the authors
  and to the editor. Three paragraphs of it is noise.
- No questions in place of findings. If you know the defect, state it. Reserve `Question` severity
  for the case where the manuscript genuinely does not let you decide.
- Attribute uncertainty to yourself, not to the paper. "I could not determine from the text
  whether the baseline was re-trained" is honest. "The authors fail to document the baseline" makes
  a claim about a file you may not have seen.
- No em dash, en dash, or colon as a habitual sentence connector. Use a full stop, a comma, a
  semicolon, parentheses, or a short heading. Keep ordinary hyphens in compounds and in
  identifiers such as `det-C1`.

## Reviewer report, field by field

```text
# Reviewer R<k> report, round <n>
- Manuscript revision: ms/main.tex, hash <sha256 prefix>, mtime <iso8601>
- Primary axis: det   Secondary axes: filt
- Target venue and class: CVPR, class A
- Emphasis brief: comparison fairness and reproducibility
- Isolation: separate context
- Sources read in full: ms/main.tex, exp/det_main/config.yaml, exp/det_main/results.json
- Read in part: the supplement, sections 3 and 4
- Unavailable: the released code repository, which returns 404 on the stated URL
```

The header exists so a later reader can tell exactly what was reviewed. Fill every line. When a
line is unknown, write `[UNVERIFIED: <what is missing>]` rather than leaving it blank.

Dimension scores. One row per dimension, with the artifact or defect that moves the score off the
midpoint. A 3 needs no justification, because 3 is the starting point. A 4 or 5 needs a named
artifact. A 1 or 2 needs a named defect. A row reading `4` with no text is a calibration error.

Concerns. Use the record format exactly, including the IDs.

```text
### det-C3
Severity: Major
Dimension: D4
Blocking: No
Claim pointer: "our detector improves small-object AP by 2.1 over the baseline" (abstract, line 6;
  Table 2 row 3)
Evidence pointer: exp/det_main/results.json reports a single run at seed 0, and the ablation in
  Table 4 uses 24 epochs while the main result uses 36
Concern: The 2.1 point small-object gain is reported from one training run, and the ablation that
  is offered as the explanation runs a different schedule from the main result.
Why it matters: The abstract presents a mechanism, but the evidence is a single observation and
  the supporting ablation does not share the main result's protocol, so neither the magnitude nor
  the attribution is established.
Resolution test: report at least three seeds with dispersion for both arms, and re-run the ablation
  at the main-result schedule; the concern closes when the small-object delta exceeds the observed
  seed spread under the matched schedule.
```

Concern ID rules. The prefix is the axis, in the form `det-C1`, `track-C2`, `reid-C3`, `cnav-C4`,
`filt-C5`. Number sequentially within a report, starting at `C1` for the first concern raised, and
never renumber after freezing. A concern that survives into the next round keeps its ID and gains a
round suffix if the report format requires one. A concern that is closed gets a closure note in the
synthesis rather than deletion, so the history stays auditable.

`Blocking: Yes` is reserved for the case where the manuscript cannot establish its central case
until the concern is resolved. A missing citation is never blocking. A `Minor` concern is never
blocking. If a report contains a blocking concern, the recommendation cannot be `Accept` or
`Minor revision`.

The no-concern statement. Close the concerns section with one line per severity level that has no
grounded concern, or a single line stating that a level is empty.

```text
## Dimensions with no grounded concern
D6 Positioning: the related work covers the four nearest lines of work and each distinction is
  accurate against the cited papers.
No Blocking concern was found.
```

Recommendation block. The eight-dimension profile in order, the overall readiness score, the
pointers that moved it from 5, and the mapping rule that produced the recommendation.

```text
## Recommendation
Eight-dimension profile: D1 4, D2 4, D3 3, D4 2, D5 3, D6 4, D7 4, D8 3
Overall readiness 1-10: 5
Movement justified by: 4 for D2 because the reformulation of the association cost is not present in
  the cited trackers and is derived rather than assembled; 2 for D4 because the main comparison has
  one arm under the private detection protocol while the other uses public detections.
Recommendation: Major revision
Reason: "One dimension at 2 with the rest at 3 or above, no blocking concern" maps to Major revision.
```

## Synthesis, section by section

The synthesis is a separate file, never merged into a reviewer report, and never shown to a
reviewer context.

Cross-report matrix. One row per underlying concern, one column per reviewer, cells holding the
concern ID in that report or a dash. Add the status label and the highest severity assigned.

```text
| Underlying concern | R1 | R2 | R3 | Status | Highest severity |
|---|---|---|---|---|---|
| Unmatched detector protocol on the main comparison | det-C2 | track-C1 | - | consensus | Blocking |
| Seed count unstated for the training result | det-C5 | - | - | single | Major |
| Loss weight undocumented | det-C7 | reid-C4 | - | consensus | Major |
| Small-object gain attributed without a matched ablation | det-C3 | - | det-C2 | consensus | Major |
```

Note the last two rows. `consensus` requires two reports raising the same underlying concern, and
the highest severity among them is reported, not an average.

The shared-mechanism justification. For every consensus row, state in one sentence why the two
concerns are the same mechanism rather than the same wording. Without that sentence, the consensus
label is unearned.

The disputed section. Record conflicts rather than resolving them by preference.

```text
## Unresolved disagreement between reviewers
R2 reads the 0.4 point IDF1 gain as within noise and calls D4 a 2. R3 reads the same table as
evidence of a real association improvement under the private protocol and calls D4 a 4. The
artifact that would settle this is the per-sequence result file with a seed sweep, which is not
in the reviewed revision.
```

The blocking-flags roll-up. One row per blocking concern, with the reports that raised it, the
dimension it damages, the resolution test, and whether the repair is an experiment, a rewording, or
a removal.

```text
| Flag | Reports | Dimension | Resolution test | Repair class |
|---|---|---|---|---|
| det-C2 / track-C1 | R1, R2 | D4 | both arms under one detection protocol, or the delta withdrawn | experiment or rewording |
```

The gate block. Use the standard format from
[gate-contract.md](../../ctrl-shared/core/gate-contract.md). State the failing criterion as one line
and the smallest clearing change as one line. If the review cannot evaluate G3 because an artifact
is missing, report `BLOCKED` and name the artifact.

## Forensic consistency pass

An optional, separate editorial pass over the manuscript against itself. Run it after freezing, in
its own context, and never feed its findings back into a reviewer context.

Checks, in the order that finds the most defects:

| Check | What it looks for |
|---|---|
| Arithmetic | a total that does not equal the sum of its parts; an average that does not reproduce from the per-item values; a percentage that does not match the stated base |
| Metric bounds | a value outside its range, such as an `mAP` above 100, a negative identity-switch count, or a probability above 1 |
| Aggregation level | a per-sequence value presented beside a per-dataset value without a label |
| Prose and table agreement | a sentence claiming a gain that the table shows as a loss, or a different precision for the same number |
| Duplicate displays | the same result appearing in two tables with different values, or a training set used as a test set |
| Dispersion anomalies | a standard deviation larger than the mean's plausible range, error bars whose statistic (SD, SE, CI) is undefined, or a claimed significance with no test; overlap or separation of plotted bars is not itself a significance test |
| Provenance | a headline number with no artifact path, no seed, and no config |
| Reproducibility | a stated command, checkpoint, or dataset version that does not resolve |
| Figure and text correspondence | a caption describing a panel that shows something else, a figure referenced in the wrong order |
| Unit and frame consistency | the same quantity in two units, or a frame stated in one section and contradicted in another |

Classify each finding into exactly one class, and report the class rather than an accusation.

| Class | Meaning |
|---|---|
| confirmed internal error | arithmetic proof or the source data establishes the discrepancy |
| aggregation ambiguity | the numbers are consistent once the aggregation is known, but the text does not say so |
| provenance gap | the number exists but its source artifact is not resolvable from the manuscript |
| suspected duplication | the same underlying result appears twice, and the text does not acknowledge it |
| unresolved, input needed | the check cannot run without an artifact the reviewers do not have |
| not assessable | the check does not apply to this manuscript |
| passed | the check ran and found nothing |

A numerical anomaly is never reported as a confirmed error without arithmetic proof or the source
data. Report it as `aggregation ambiguity` or `unresolved, input needed` and say which artifact
would settle it. This is the single most common way a forensic pass damages its own credibility.

## Length and signal

A review's value is in the pointers, not the word count. A report with four well-pointered concerns
outperforms one with twenty impressions. Suggested scale for a full manuscript at the `thorough`
tier: 8 to 20 concerns per reviewer, of which the blocking ones are few. If a report has thirty
concerns, most of them are probably `Minor` presentation notes that belong in one grouped item. If
a report has two, check whether the reviewer stopped reading, since real manuscripts are rarely
that clean.
