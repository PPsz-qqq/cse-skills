# Response red lines

Hard rules for any author-side correspondence with a reviewer or an editor. These are not style
preferences. Each one maps to a failure that has cost a submission, and each is checkable against an
artifact before the letter is sent.

Read this file in full before drafting any response, and again before sending it.

## 1. Follow the venue's response format, and never leak what it keeps private

Fix the response format from the current venue guidance or the decision letter before drafting,
and record the document consulted with its date. Four formats occur in this field.

| Format | Typical venues (verify every cycle) | Referring to another reviewer |
|---|---|---|
| `shared-rebuttal` | CVPR, ICCV, ECCV: one anonymous one-page PDF that answers all reviews, read by the assigned reviewers and area chairs, with no external links | allowed by the reviewer IDs the venue assigned, for navigation |
| `per-thread` | OpenReview venues such as ICLR and NeurIPS: replies posted under each review, visible according to the venue's reader settings | allowed only when that reply's readers include the reviewer referred to |
| `combined-letter` | most journal revisions, for example IEEE Transactions and Automatica: one response document with a section per reviewer plus a cover letter; common practice, not a universal rule | allowed by reviewer and comment number, such as "see Response 2.3" |
| `isolated` | the venue or editor asks for separate responses that the other reviewers will not see, or the format is still unknown | forbidden, in any wording |

When the format is unknown, draft in the `isolated` format. Isolated sections can always be
assembled into a combined document later, but a combined draft cannot be safely split.

In the `isolated` format, forbidden in any reviewer-facing file:

- naming or numbering another reviewer, in any wording. Not `Reviewer 2`, not `R2`, not `the second
  reviewer`, not `one of the reviewers`, not `another referee`;
- reporting what the authors told another reviewer;
- copying a shared response table into a per-reviewer letter;
- referring to reviews in the plural from inside a letter addressed to one reviewer.

In every format, forbidden:

- reporting another reviewer's score, confidence rating, recommendation, or ranking;
- quoting a confidential comment to the area chair or editor, or a meta-review sentence the venue
  did not show to the reviewers;
- arguing by headcount: another reviewer's agreement is not evidence for the point in dispute;
- revealing author identity in a double-blind format, including through links or acknowledgments.

Correct practice when two reviewers raised the same defect. In the `isolated` format, write the
response twice, once in each reviewer's own framing, with the same evidence in both. In the shared
formats, answer once in full and point the second reviewer to it by the venue's identifier.

## 2. Never claim a change that is not in the manuscript

The reviewer will open the revised file and look. A letter that reports a change the manuscript does
not contain converts a technical concern into an honesty concern, and honesty concerns are not
recoverable in the next round.

Check every `Change` line against the revised file at the cited location before sending. If the edit
is planned but not yet made, the letter is not ready.

## 3. Never promise an experiment that is not tracked

Every promise creates a ledger row with an owner and a status, before the letter is drafted. A run
that fails is reported as a failure, with the reason, in the letter. It never becomes silence and it
never becomes a deferral without a stated reason.

The specific forbidden pattern. Promising an experiment in round one, failing to run it, and
reporting a different experiment in round two as if it were the requested one. Reviewers detect this,
and it reads as evasion regardless of the actual cause.

## 4. Never invent evidence

Every number, artifact path, dataset statistic, and citation in a letter must resolve. The rules in
[evidence-integrity.md](../../cse-shared/core/evidence-integrity.md) rule 1 apply to correspondence
exactly as they apply to the manuscript.

Forbidden without exception.

- inventing a result for a run that was not performed;
- reporting a number from memory instead of from the result file;
- describing an artifact path that does not exist at the time of sending;
- citing a paper without reading at least its abstract first hand, or citing one known only by title;
- restating a baseline's published number from memory rather than from the paper or the ledger;
- describing a figure that has not been generated.

When an element is unavailable, write `[MISSING: <what is needed and how to obtain it>]` in the
internal ledger and either obtain it or remove the claim from the letter. A gap in the internal
ledger is a normal working state. A gap in the sent letter is a defect.

## 5. Never let the letter and the manuscript disagree

Reconcile in both directions before sending.

- Forward. Every change reported in a letter appears in the revised manuscript at the cited
  location.
- Backward. Every change made to the manuscript in response to a review appears in the
  corresponding letter, or is listed in the cover letter's summary of changes.
- Numbers. Every value in a letter matches the manuscript at the same precision and in the same
  units.

A change made silently is as damaging as a change claimed but not made. The second reviewer round
compares the two files, and an unlisted change reads as an attempt to slip something past.

## 6. Never escalate a scientific disagreement to the editor

Reserve the editor for a factual error the manuscript already settles, a violation of the venue's
stated policy, or a conflict of interest. Never for a disagreement about novelty, significance,
expected effect size, or whether a comparison is worth running. The editor adjudicates process, not
science, and an unnecessary escalation is remembered.

When escalation is warranted, put it in the cover letter, in two sentences, with the manuscript
location that settles the point. Keep the per-reviewer letter ordinary.

## 7. Never trade a concession for a score

Do not accept a concern because the reviewer was emphatic, do not accept it because the deadline is
near, and do not accept it to make the next round easier. A concession the data contradict is a
factual error the next reviewer will find, and it is a permanent record of the authors agreeing to
something untrue.

Score the authors' own counter-argument 1 to 5 on evidence quality before sending. Concede only at 4
or above when the evidence is on the reviewer's side, and rebut only at 4 or above when it is on
yours. Below 4 on both sides, the honest class is defer to limitations.

## 8. Never antagonize

Every sentence in a letter is written as if it will be read aloud at a program committee meeting,
because it may be. Forbidden: sarcasm, exclamation, capitalized emphasis, rhetorical questions,
phrases implying the reviewer was careless, phrases implying the reviewer did not read, and any
statement about the reviewer's competence.

Replacements for the common failures.

| Instead of | Write |
|---|---|
| "The reviewer is mistaken." | "Section 4.2 states <quote>. We have moved this statement to the abstract so it is not missed." |
| "This is out of scope." | "The paper claims <claim>, which does not extend to <requested setting>. We have made that boundary explicit in Section 7." |
| "We already did this." | "Table 3 contains this comparison. We have added a pointer to it from Section 5.2 and clarified the caption." |
| "Due to the page limit we cannot add this." | "We have deferred this to the limitations section and describe the protocol a future study would follow." |

## 9. Never let the letter invent a new claim

A response answers a concern. It does not introduce a contribution, a result, or a comparison that
the manuscript does not contain. When a good answer would require a new claim, either run the
experiment and add the claim to the manuscript, or answer within the existing claim.

## 10. Never send with an unresolved blocking item

Run the consistency check in [revision-tracking.md](revision-tracking.md) before sending. The letter
is not sent while any of the following is true.

```text
[ ] A ledger row for an accepted comment has no manuscript location
[ ] A letter reports a result whose ledger row is not closed
[ ] A change is claimed but not present in the revised file
[ ] A change is present but not reported in any letter or in the cover summary
[ ] A number in a letter disagrees with the manuscript
[ ] An isolated-format letter names another reviewer, or any letter quotes another reviewer's score, recommendation or confidential comment
[ ] A deferral has no corresponding limitation entry
[ ] An evidence pointer does not resolve
[ ] The manuscript revision hash in the ledger does not match the file being sent
```

## Reporting to the user

When a request cannot be answered honestly, say so before drafting rather than after. Use the shape
from [verdicts-and-loops.md](../../cse-shared/core/verdicts-and-loops.md) under
`Blocker-first behaviour`, naming the single missing item that unblocks the work.

Two situations that reach this point.

- The reviewer's requested experiment cannot run and the paper's claim depends on it. The honest
  output is a limitation entry plus a scope statement, and the user should be told that the concern
  will likely stay open.
- Two reviewers' requested fixes are mutually incompatible, for instance one asks for a broader
  claim and the other for a narrower one. The correct action is to state the conflict to the user,
  choose the claim the evidence supports, and record the residual risk. It is not to satisfy both by
  hedging, because a hedged claim satisfies neither reviewer and weakens the manuscript.
