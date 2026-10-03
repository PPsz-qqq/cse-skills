---
name: ctrl-response-craft
description: >-
  Use when answering peer review for a paper on detection, tracking, re-ID, cooperative navigation
  or filtering (目标检测, 跟踪, 重识别, 协同导航, 滤波): 回复审稿意见, 逐条回复, 修改说明, 返修,
  rebuttal, response letter, revision plan, cover letter to the editor. Triages each comment,
  decides run-versus-decline for requested experiments, tracks promises in a revision ledger,
  follows the venue's response format, and never claims a change the manuscript does not contain.
---

# CTRL response craft

Answer reviewer comments with evidence, in the reviewer's own order, without ever leaking one
review into another.

## Start here

Read [execution-contract.md](../ctrl-shared/core/execution-contract.md) first. Select the smallest
useful mode, confirm the inputs and available tools, and load only the references needed by the
current step. Use only the output sections relevant to this request; a diagnostic or draft is not
a gate-passed final artifact.

Triage and provisional replies are allowed before new experiments finish. Label those replies
`draft: pending evidence`; final letters cannot report unfinished runs as completed changes.

## Default stance

The letter is a claim about the manuscript. If the manuscript does not contain the change, the
letter does not report it.

- Read [verdicts-and-loops.md](../ctrl-shared/core/verdicts-and-loops.md) and the venue's own
  reviewer-response guidance first. The venue's guidance wins over anything here.
- Fix the response format first: `shared-rebuttal` (CVPR, ICCV, ECCV one-page PDF),
  `per-thread` (OpenReview), `combined-letter` (most journals) or `isolated`, per
  [references/red-lines.md](references/red-lines.md). Draft `isolated` until the format is known.
  Only the `isolated` format forbids naming another reviewer; no format ever quotes another
  reviewer's score, recommendation or confidential comment.
- Classify every comment before writing any response. The class determines the evidence obligation,
  and an unclassified comment gets answered from instinct, which is where most rebuttals fail.
- Every promised experiment is a ledger row with an owner before the letter is drafted. The letter
  reports a result only after the row is closed with an artifact.
- Score the authors' own counter-argument 1 to 5 on evidence quality. Rebut at 4 or above, concede
  at 4 or above when the evidence favors the reviewer, and defer below 4 on both sides.
- The default effort tier is `thorough`, rising to `submission` when the round decides acceptance.

## Workflow

1. **Inventory the reviews and fix the round.** Record the venue, the review round, the deadline,
   and the exact venue guidance consulted with its date. Parse every comment into the ledger at
   `ctrl-revision-<round>-ledger.md` using the schema in
   [references/revision-tracking.md](references/revision-tracking.md). Reproduce the reviewer's own
   numbering. A comment that cannot be parsed into a row is a comment that will be missed.

2. **Classify each comment.** Assign exactly one class: accept, partially accept, rebut with
   evidence, defer to limitations, or escalate to the editor in the cover letter only. Record the
   class in the ledger. Decide the class from the comment's mechanism, not its tone, using the
   comment-shape table in [references/rebuttal-strategy.md](references/rebuttal-strategy.md).

3. **Fix the response culture and format.** Determine whether this is a conference rebuttal with a
   short hard limit or a journal revision with a long window, and choose the winning moves
   accordingly. Record the response format (`shared-rebuttal`, `per-thread`, `combined-letter` or
   `isolated`) and the venue rules that come with it, such as a one-page limit, no external links,
   or no unrequested new results in a CVPR-class rebuttal. A journal-style letter in a rebuttal
   window is not read.

4. **Decide run versus argue versus decline for every new-experiment request.** Work the decision
   table in [references/revision-tracking.md](references/revision-tracking.md) row by row and record
   which question decided it. State the cost in comparable units for any declined request. Never
   decide to run because the reviewer asked, and never decline because it is inconvenient.

5. **Create the ledger rows for every promise before drafting.** Each row carries an owner, the
   named evidence artifact, an experiment status, and the claim rows it will update in
   `ctrl-claims.md`. An unowned promise is not made.

6. **Draft the responses in the reviewer's own order.** Use the four-part shape: acknowledge what is
   correct, state the position, give the evidence, name the change. State the position within the
   first two sentences. Keep each response under roughly 150 words unless it reports a new
   experiment.

7. **Run the experiments and close the rows, then promote the claim.** A result enters a letter only
   after its ledger row is closed and its claim row passes G2. Before any sentence in a letter is
   strengthened, check the promotion condition for that statement in
   [verdicts-and-loops.md](../ctrl-shared/core/verdicts-and-loops.md). A superiority claim needs a
   protocol-matched comparison against that specific baseline, a mechanism claim needs an ablation
   isolating the component under one protocol, and a claim across runs needs a justified sample
   size under the active axis default plus dispersion. Where the condition is unmet, write the weaker true statement rather than the
   stronger wording plus a hedge. A run that fails is reported as a failure with its reason, never
   as silence and never as a deferral without a reason.

8. **Write the revision plan.** Group the ledger rows into work packages with owners, costs, and
   dependencies, and record the decisions taken with their residual risk. Produce the plan before
   editing the manuscript, so a long revision does not drift.

9. **Draft the per-reviewer sections and the cover letter.** Use
   [references/response-letter-template.md](references/response-letter-template.md), then assemble
   them in the recorded format. In the `isolated` format write each letter as if it were the only
   review, and answer a shared defect twice in each reviewer's own framing with the same evidence.
   In a shared format answer it once and cross-reference it by the venue's identifier.

10. **Reconcile the package in both directions.** Every claimed change is in the revised file at the
    cited location, and every change made is claimed somewhere. Every number in a letter matches the
    manuscript at the same precision. Run the full consistency check before sending.

11. **Run the leak and red-line scan.** In every format, search reviewer-facing files for score,
    recommendation and confidence words, confidential or meta-review language, and identifying
    details or external links where the venue forbids them. In the `isolated` format also search
    for the other reviewers' designators and plural references to reviews. A hit is a leak until
    proven otherwise. Apply [references/red-lines.md](references/red-lines.md) in full.

12. **Report the round outcome.** State the counts by class, the promises delivered versus made, the
    concerns carried forward, and whether the loop converged. Stop at four rounds, and report
    non-convergence with the unrepaired defect named rather than running a fifth.

## Output format

Per-reviewer section, one file per reviewer in the `isolated` format and assembled into the venue's
upload otherwise. Full template in
[references/response-letter-template.md](references/response-letter-template.md).

```text
# Response to Reviewer <k>, round <n>
Manuscript: <title>   Revision: <path> hash <sha256 prefix>

## Comment <k>.<i>
> <the reviewer's comment, reproduced verbatim and complete>

**Response.** <acknowledgement, position, and the substance of the reply>
**Evidence.** <artifact path, table or figure, measurement with units, protocol ID>
**Change.** <section, page, table, or figure; or "no manuscript change, see response">

## Summary of changes for Reviewer <k>
| Comment | Status | Where the change appears |
|---|---|---|

## Where the manuscript did not change
<which concerns were not acted on and why>
```

Cover letter to the editor, `ctrl-response-<round>-cover.md`.

```text
Dear Editor,
We thank you and the reviewers for the assessment of <manuscript ID>.
Summary of changes
1. <change, one line, with its location>
Points accepted <n>. Partially accepted <n>. Rebutted with evidence <n>. Deferred <n>.
The revised manuscript is <n> pages, with a marked-up version and the tracking table at <path>.
```

Revision ledger row, `ctrl-revision-<round>-ledger.md`.

```text
| ID | Reviewer | Comment (short) | Class | Owner | Evidence needed | Experiment status | Manuscript location | Claim rows | Status |
| 1.3 | R1 | compare at matched resolution | partially accept | A2 | control run, 512x512, 3 seeds | done, exp/det_ctrl | Table 3 | C11 | closed |
```

Round report.

```text
Round <n> report
- Reviews <n>, comments <n>.  Closed <n>, carried forward <n>, blocked <n>
- Classes: accept <n>, partially accept <n>, rebut <n>, defer <n>, escalate <n>
- Experiment promises made <n>, delivered <n>
- Concerns accepted in a prior round and still unfixed: <n>
- Response format: <shared-rebuttal | per-thread | combined-letter | isolated>, guidance <document, date>
- Leak scan: <pass | the specific leak found>
- Package reconciliation: <pass | the specific mismatch>
- Loop outcome: converged | budget exhausted with residual defects | stopped by user
- Residual risk: <what stays open, and what it costs>
```

## Red lines

- In the `isolated` format, never mention another reviewer in a reviewer-facing file, in any
  wording, including `Reviewer 2`, `R2`, `another reviewer`, `one of the reviewers`, or a plural
  reference to reviews. Draft in this format until the venue's format is confirmed.
- In every format, never report another reviewer's score, confidence, recommendation, confidential
  comment, or a meta-review sentence the reviewers were not shown, and never argue by headcount.
- Never claim a change the revised manuscript does not contain, and never make a change that no
  letter reports.
- Never promise an experiment that has no ledger row with an owner, and never report a result whose
  ledger row is not closed.
- Never strengthen a claim past its promotion condition, and never keep the stronger wording with a
  hedge appended.
- Never invent a result, an artifact path, a citation, or a number, and never report a value from
  memory instead of from the result file.
- Never escalate a scientific disagreement to the editor, and never trade a concession for a
  favorable reading.
- Never send while the red-line scan in [references/red-lines.md](references/red-lines.md) has an
  open item.

## Related files

| File | Open when |
|---|---|
| [references/response-letter-template.md](references/response-letter-template.md) | You are drafting the cover letter, a per-reviewer letter, or a response paragraph, or checking comment numbering and isolation |
| [references/rebuttal-strategy.md](references/rebuttal-strategy.md) | You are choosing between conference-rebuttal and journal-revision tactics, or classifying a comment by its shape |
| [references/revision-tracking.md](references/revision-tracking.md) | You are building the revision ledger, deciding run versus decline, writing the revision plan, or running the consistency check |
| [references/red-lines.md](references/red-lines.md) | You are about to send anything to a reviewer or an editor, or handling a hostile or mistaken review |
| [../ctrl-shared/core/verdicts-and-loops.md](../ctrl-shared/core/verdicts-and-loops.md) | You need the claim-promotion conditions, the anti-sycophancy calibration, the loop budget, the effort tiers, or the blocker-first output shape |
| [../ctrl-shared/core/evidence-integrity.md](../ctrl-shared/core/evidence-integrity.md) | You are checking a number, a comparison, a citation, or a provenance claim that will appear in a letter |
| [../ctrl-shared/core/gate-contract.md](../ctrl-shared/core/gate-contract.md) | You are checking that a result reported in a letter passes G2, or reporting a gate in the round report |
| [../ctrl-shared/core/artifact-contract.md](../ctrl-shared/core/artifact-contract.md) | You are naming the response files, the ledger, or the per-reviewer split |
| [../ctrl-shared/core/review-rubrics.md](../ctrl-shared/core/review-rubrics.md) | You need the severity tiers or the concern record fields to map a reviewer comment onto your ledger |
| [../ctrl-shared/core/venue-matrix.md](../ctrl-shared/core/venue-matrix.md) | You are judging what this venue's reviewers weight, or checking the venue's own guidance version |
| [../ctrl-shared/core/terminology-and-notation.md](../ctrl-shared/core/terminology-and-notation.md) | You are reusing a symbol, metric name, or bilingual term consistently between the letter and the manuscript |

Forward references, owned by other skills. Use `ctrl-experiment-suite` when a reviewer request
becomes a run that must be planned and executed, `ctrl-pre-submission-review` when a round needs a
fresh referee-side read before resubmission, `ctrl-paper-craft` when a revision requires rewriting
sections rather than patching them, and `ctrl-lit-radar` when a novelty objection needs a documented
search of the recent venue cycles.
