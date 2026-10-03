# Mutual-blindness protocol

The full procedure for producing N independent reviewer reports over one manuscript plus one
post-freeze synthesis. This file is normative for `ctrl-pre-submission-review`. The summary lives
in [review-rubrics.md](../../ctrl-shared/core/review-rubrics.md) under `Reviewer independence`, and
the procedure below is the operational expansion.

The premise is simple. Three opinions produced in one context are one opinion with three
signatures. Isolation is the only thing that makes agreement informative, so the protocol spends
its effort on keeping contexts apart and on never repairing that separation after the fact.

## Artifact inventory

| Artifact | Produced when | Visible to reviewers | Visible to the user |
|---|---|---|---|
| `ctrl-review-<n>-packet.md` | step 3, before any report | yes, and only this | yes |
| `ctrl-review-<n>-brief-R<k>.md` | step 4, before any report | only its own reviewer | yes |
| `ctrl-review-<n>-R<k>.md` | step 5, one per reviewer | never | yes, frozen |
| `ctrl-review-<n>-synthesis.md` | step 7, after all reports frozen | never | yes |

Write the round as a literal token, for example `ctrl-review-1-packet.md`, matching the naming in
[artifact-contract.md](../../ctrl-shared/core/artifact-contract.md).

## Step 1, the immutable review packet

The packet is the only manuscript-derived material a reviewer sees. Build it once and hash it.

```text
# Review packet, round <n>
## Artifacts under review
- <path>  hash <sha256>  mtime <iso8601>  <what it is>
## Assessment boundary
- Read in full: <sources>
- Read in part, with what part: <sources>
- Not available to this review: <sources, and what would be required>
## Verified source anchors
- <dataset statistic, baseline number, or release artifact, each with how it was verified>
## Common criteria
- Rubric: ctrl-shared core/review-rubrics.md, eight dimensions, 1 to 5
- Severity tiers: Blocking, Major, Minor, Question
- Active axes: <primary and secondary>
- Rules: evidence pointer or drop, no concern quota, no invented locations
## Reviewer briefs
- R1 <path>  R2 <path>  R3 <path>
```

Forbidden packet contents, without exception:

- any concern, hypothesis, suspicion, or preliminary conclusion, including one phrased as a
  question to the reviewer;
- any prior-round review, any author response, any rebuttal, any editorial email;
- the authors' own risk assessment, a "known weaknesses" list, or a supervisor's note;
- another reviewer's brief, the synthesis from a prior round, or the consensus list;
- the user's preferred outcome, deadline pressure, or a target recommendation.

A packet that leaks any of these converts the round into a single review and the synthesis into
theatre. If the user supplies such material, keep it out of the packet and say which items were
excluded and why.

## Step 2, emphasis briefs

Write every brief before the first report exists. A brief allocates depth, never the rubric.

```text
# Emphasis brief R<k>, round <n>
- Lens: <one line naming the emphasis>
- Allocated depth: <the dimensions, artifacts, or evidence classes this reviewer examines hardest>
- Explicitly unchanged: all eight dimensions are scored on the full 1 to 5 scale
- Required reading order: packet, then the per-axis taxonomy for <axes>, then the manuscript
- Required output: the standard report skeleton, every grounded concern retained
- Independence statement: you have not seen and will not seek another reviewer's report
```

Three default lenses for this pack:

| Lens | Concentrates on | Typical high-yield findings |
|---|---|---|
| Method and evidence chain | whether the claim stated in the abstract is established by the experiments as specified | an unsupported mechanism claim, an ablation that does not isolate the component, a result table that does not test the stated hypothesis |
| Comparison fairness and reproducibility | protocol matching, baseline reported-versus-re-implemented status, seeds, configs, code and data instructions | an unmatched protocol presented as a delta, a baseline tuned only for the competing arm, a headline number with no provenance |
| Validity boundary and failure modes | dataset, scenario, hardware and assumption limits, negative results, generalization claims | simulation presented as field results, one environment generalized to all, losing cases removed, limits stated only in words |

A brief is not a persona. Do not write a name, an affiliation, a career stage, a publication
record, or a personality. Do not write "this reviewer is a known skeptic of attention modules".
Inventing an identity adds no information and creates a fabricated fact the user may repeat.

Custom briefs are allowed when the manuscript has a specific exposure, for example a legal, ethics,
dual-use, or hardware-safety dimension. Write the custom brief before the report and freeze it.

## Step 3, isolation paths

Choose exactly one path per round and print the choice in every report and in the synthesis.

| Path | Condition | What you produce | Required label |
|---|---|---|---|
| Isolated | the environment starts a separate context, subagent, or process per reviewer, each receiving only packet plus its own brief | three reports plus synthesis | `separate contexts` |
| One report per invocation | one context only, but the user can start fresh invocations | one report here, and instructions for the remaining invocations | `one report per invocation` |
| Single reviewer | one context only, and the user wants one round now | exactly one report, no consensus step | `single reviewer, multi-reviewer isolation unavailable` |
| Declared non-blind | the user insists on three reports in this context | three reports, with overlap reported as drafting overlap | `NON-BLIND shared context, reports are not independent` |

Rules that hold on every path:

- The one-report-per-invocation path is the default fallback. It costs the user three invocations
  and buys genuine blindness, which is the entire value of the mechanism.
- On the single-reviewer path, the deliverable is a strong single review. It is not a panel, and
  a consensus section would be fabricated.
- On the declared non-blind path, the word consensus is unavailable. Describe overlap as what it
  is, one drafter producing similar findings twice, and state plainly that the reports cannot be
  used to estimate how many real reviewers would raise a given concern.
- Context compaction does not restore isolation. If a reviewer's context later receives another
  report, the round is `NON-BLIND` from that point.
- Cross-model dispatch is a bonus when available, never a substitute for context separation. The
  same model in two isolated contexts is a valid panel. Two models in one context are not.

## Step 4, the reviewer instruction block

Give each reviewer this block verbatim, with the paths substituted. It is short on purpose, since
the rubric is already a separate file.

```text
You are reviewer <Rk> for round <n>. Your emphasis brief is <brief path>.
Read, in order: <packet path>, then the taxonomy for the active axes, then the artifacts listed
in the packet.

Rules.
1. Score all eight dimensions 1 to 5, starting at 3 and justifying every point of movement with a
   pointer.
2. Every concern carries a claim pointer and an evidence pointer. A concern you cannot point at is
   dropped or reframed as a Question.
3. No quota. If a severity level has no grounded concern, write that sentence explicitly.
4. Severity follows impact on the manuscript's case, never the tone of the writing.
5. Mark a location you cannot find as [NOT FOUND: <what you searched>]. Never approximate one.
6. Mark anything you could not verify as [UNVERIFIED: <what is missing>]. Invent nothing.
7. You have not seen and will not seek any other reviewer's report, brief, ledger, or synthesis.
8. Output the standard report skeleton, then stop.
```

## Step 5, freezing

Freeze at the moment the report is written. Record the hash in the synthesis.

- Write each report once, to its own file.
- Record `<path>, sha256 <prefix>, mtime <iso8601>`.
- A frozen report is never edited. Corrections become an appended, dated `Correction` section that
  states the original text, the corrected text, and the reason. Never silently revise.
- If the manuscript changes, the entire round becomes `STALE`. Do not patch one report. Re-run the
  round against the new hash, because a review that mixes two revisions is not attributable to
  either.

## Step 6, the comparison

Compare only after every report is frozen. Compare mechanisms, not sentences.

Two concerns are the same underlying concern when they name the same defect of the same object
with the same consequence, even when the wording, the dimension, or the severity differ. Example.
R1 writes "the ablation in Table 4 changes the training budget, so the gain is not attributable to
the proposed module" and R2 writes "Table 4 compares against a baseline trained for fewer epochs,
so the delta is unmatched". That is one underlying concern under D4, raised independently twice,
and it is `consensus`.

Not the same concern, despite similar wording. R1 objects to an unspecified loss weight and R2
objects to an unspecified optimizer schedule. Both are underspecification, but they are two
defects with two different resolution tests.

Label decisions:

| Situation | Label | Synthesis treatment |
|---|---|---|
| 2 or 3 reports raise the same underlying concern | `consensus` | list the report concern IDs, state the shared mechanism, set severity to the highest assigned |
| 1 report raises it | `single` | retain it, name the report, note that the panel is one voice here |
| all reports raise it | `consensus, unanimous` | retain, and note that uniform agreement often signals an obvious defect the authors can see too |
| reports conflict on whether the defect exists | `disputed` | report the conflict, name the artifact that would settle it, do not average the positions |
| reports differ only in severity | `consensus` | report both severities and the highest |

Severity for a consensus concern is the maximum any reporting reviewer assigned, and the synthesis
states which reviewer assigned it. Averaging severities is prohibited, because severity is a claim
about what blocks publication, not a preference to be averaged.

## Step 7, the separate forensic pass

After freezing, optionally run the artifact-side consistency checks in
[report-structure.md](report-structure.md) as their own editorial pass over the manuscript against
itself, not over the reviewers' opinions. Keep it out of reviewer contexts. Its findings enter the
synthesis under their own heading, labelled `post-freeze editorial finding`, and are never
attributed to a reviewer, because attributing a post-freeze finding to a frozen report rewrites
that report.

## Common failure modes

| Failure | What it looks like | Correct handling |
|---|---|---|
| Shared-context drafting | three reports with the same three findings, the same order, and the same phrasings | mark `NON-BLIND` and say the reports are not independent evidence |
| Packet leak | a reviewer report that answers a question only the authors asked | rebuild the packet, re-run the round, record why |
| Retroactive smoothing | overlap reduced by editing after comparison | never edit; report the overlap |
| Manufactured disagreement | one reviewer briefed to disagree | briefs allocate depth, not positions |
| Consensus by wording | two reports both say "unclear" about different objects | compare mechanisms and objects, not vocabulary |
| Severity averaging | "the panel considers this Major-to-Minor" | state the maximum and who assigned it |
| Synthesis in a reviewer file | the consensus list appearing inside `ctrl-review-<n>-R1.md` | the synthesis lives in its own file, always |
| Stale round | reports frozen, manuscript then revised | recompute the round; do not reissue the verdict |
