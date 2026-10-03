# Response letter template

The letter is the artifact the editor reads first. It must let a reviewer confirm, in one pass, that
every point was addressed, and it must never leak information across reviewers.

Produce one file per reviewer for mutually blind venues, named `ctrl-response-<round>-R<k>.md`,
plus `ctrl-response-<round>-cover.md` for the editor. Combine into a single
`ctrl-response-<round>.md` only when the venue is single-blind, the reviews are non-anonymous, and
the venue's own guidance permits one combined letter.

## Cover letter to the editor

Short. The editor has read four of these before lunch.

```markdown
Dear Editor,

We thank you and the reviewers for the assessment of <manuscript ID / title>. We have revised the
manuscript and respond to each point below.

Summary of changes
1. <change, one line, with the section or table where it appears>
2. <change>
3. <change>

Points accepted in full: <n>. Points partially accepted: <n>. Points rebutted with new evidence:
<n>. Points deferred to the limitations section: <n>.

The revised manuscript is <n> pages. A marked-up version with changes highlighted accompanies this
letter, along with a revision-tracking table at <path>.

Sincerely,
<author list>
```

Numerical correspondence claims come from the tracking table, never from memory. If the counts do
not match the table, the table is right and the summary is wrong.

## Per-reviewer point-by-point letter

```markdown
# Response to Reviewer <k>, round <n>
Manuscript: <title>   Revision: <path> hash <sha256 prefix>

We thank Reviewer <k> for the detailed reading. Below, each comment is reproduced in full, in the
reviewer's own order and numbering, followed by our response and the resulting change.

---

## Comment <RN>.<i>
> <the reviewer's comment, reproduced verbatim and complete>

**Response.** <what we did, what we found, what we maintain>

**Evidence.** <artifact path, new table or figure number, measurement, with units and the protocol
ID from ctrl-protocol.md>

**Change.** <section, page, table, or figure where the revision appears; or "no manuscript change,
see response">

---

## Comment <RN>.<i+1>
...

---

## Summary of changes for Reviewer <k>
| Comment | Status | Where the change appears |
|---|---|---|
| <RN>.<i> | accepted | Section 4.2, Table 3 |
| <RN>.<i+1> | rebutted with evidence | no change, response above |

## Where the manuscript did not change
<one paragraph stating plainly which concerns were not acted on and why, so the reviewer does not
have to hunt for the omission>
```

## Comment numbering and isolation

Reproduce each reviewer's own numbering exactly. Do not renumber, merge, reorder, or summarize a
comment into a shorter form. A reviewer who numbered their comments `1, 2, 3a, 3b` receives a reply
numbered `1, 2, 3a, 3b`.

The isolation rule, which is the one that most often breaks:

- A reviewer-facing response never mentions another reviewer, another reviewer's numbering, another
  reviewer's recommendation, or the authors' response to another reviewer.
- Never write "as also noted by Reviewer 2", "Reviewer 3 raised the same concern", "one reviewer
  suggested", or "in contrast to the other reviews".
- Never write "we agree with all reviewers that", even when everyone raised the same defect. Every
  letter is written as if it were the only review.
- Never place a shared, cross-reviewer table in a per-reviewer file. If the venue permits a single
  combined letter, the combination itself is the disclosure and must be stated in the cover letter
  as following the venue's guidance.
- Never reveal a recommendation, a score, a confidence rating, or a meta-review sentence, even when
  the venue shows them to the authors. The editor's meta-review is not yours to quote.
- When two reviewers raised the same defect and the fix is identical, write the response twice, once
  per letter, in each reviewer's own framing. Duplicated prose costs nothing and leaking costs the
  submission.

Check before sending. Search every per-reviewer file for the other reviewers' designators, for the
word `reviewer` followed by a numeral other than the addressee, and for `all reviewers`,
`another reviewer`, `the other reviewer`, `meta-review`, and `recommendation`. A hit is a leak until
proven otherwise.

## Response paragraph, the four-part shape

Every response uses the same shape, in this order. Keep each part to a few sentences.

1. **Acknowledge what is correct in the comment.** State the concern in your own words, accurately,
   even when you disagree with the conclusion. This proves you read it and it prevents a
   straw-man reply.
2. **State the position.** Accepted, partially accepted, rebutted with evidence, or deferred.
3. **Give the evidence.** A pointer to a new experiment, a table, a measurement, or a citation read
   at first hand. Not an adjective, not a restatement of the claim.
4. **Name the change.** Section, page, table, figure, or an explicit statement that nothing changed.

Example of a correct rebuttal, on a request to compare against a method that is not comparable:

```markdown
## Comment R1.3
> The paper should compare against <method> which reports a higher mAP on the same benchmark.

**Response.** We thank the reviewer for pointing us to this work, which we have now read in full
and cited. Our position is a partial accept. The published number was obtained at 640x640 input
resolution with test-time augmentation and additional pretraining data, while our protocol is
fixed at 512x512 with neither. Reporting the two as a matched comparison would overstate our
difference and understate theirs. We have therefore added a declared-difference comparison rather
than a delta, re-trained the baseline under our protocol, and reported both numbers.

**Evidence.** Table 3 now carries two rows for this baseline. The row labelled `re-implemented`
is our retraining at 512x512, three seeds, mean reported with standard deviation. The row labelled
`reported` reproduces the published 45.2 and states the three protocol differences. Protocol block
P-det-2 in the revised manuscript records the comparison.

**Change.** Table 3, Section 5.2 paragraph 2, and the new protocol block in Appendix A.
```

Example of an unacceptable response to the same request:

```markdown
**Response.** We thank the reviewer for this suggestion. We have added the comparison in Table 3,
where our method outperforms <method>. This further demonstrates the superiority of our approach.
```

The second version fails on three counts. It invents a comparison, it does not state that the
protocols differ, and it uses a superiority claim where the promotion condition requires a matched
comparison. It is also the single most common rejection cause at the second round.

## Handling a request for an experiment that cannot be run

State the cost and the decision. Never promise and never silently drop.

```markdown
## Comment R2.5
> The authors should evaluate on <dataset>.

**Response.** We agree this evaluation would strengthen the paper, and we have assessed it honestly.
<Reason it was not run: the dataset is not publicly available as of <date>; or reproducing the
annotation requires approximately <n> GPU-hours plus annotation that is outside this revision's
scope>. Rather than promise an experiment we cannot complete before the deadline, we state this
explicitly as a limitation in Section 7 and describe the evaluation protocol we would use, so that
the reader can judge the gap.

**Evidence.** The dataset's availability status is recorded at <path or URL, with the date checked>.

**Change.** Section 7 limitation 2, which now states the missing evaluation, the reason, and the
protocol a future study would follow.
```

The rule behind this shape. A deferred item is honest, checkable, and reviewable. A promise that is
not delivered by the camera-ready deadline is a broken commitment in the permanent record, and
reviewers remember it.

## Tracking table in the letter

The tracking table is described in [revision-tracking.md](revision-tracking.md). Include the
per-reviewer summary block in each letter and keep the full cross-reviewer table in the internal
ledger, never in a reviewer-facing file for a blind venue.

## Red-line scan before sending

```text
[ ] No mention of any reviewer other than the addressee
[ ] No mention of another reviewer's numbering, score, or recommendation
[ ] No meta-review quotation
[ ] Every reproduced comment is complete and in the reviewer's original order
[ ] Every promised experiment has a result row in the ledger
[ ] Every evidence pointer resolves to an artifact that exists
[ ] Every changed location cited in the letter actually contains the change in the revised file
[ ] Numbers in the letter match the tracking table, which matches the manuscript
[ ] No superiority claim without a matched comparison
[ ] No new claim introduced that is absent from the manuscript
[ ] Percentages state absolute or relative
[ ] Every deferral names the limitation section where it now appears
```
