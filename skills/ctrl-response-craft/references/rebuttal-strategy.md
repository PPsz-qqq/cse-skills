# Rebuttal strategy

What actually moves a score, and what wastes the one chance to answer. The venue class decides
which of these applies, so fix the class first from
[venue-matrix.md](../../ctrl-shared/core/venue-matrix.md).

## The two review cultures

| Dimension | CVPR-class vision conference | Control, robotics, and estimation journals |
|---|---|---|
| Time for the response | one short rebuttal window, often 1 to 2 pages, sometimes a single text box | a revision round measured in weeks or months |
| What the venue wants | a decision, now, with the smallest convincing evidence | a revised manuscript that a reviewer can re-check |
| What wins | a decisive new number, a factual correction of a misreading, a clear scope statement | a new experiment, a corrected proof, an added comparison, a rewritten section |
| What loses | restating the contribution, promising future work, arguing about novelty in the abstract | arguing with the reviewer, cosmetic edits presented as revisions, a response letter longer than the paper |
| New experiments | often impossible in the window, so a partial run with a stated protocol is worth more than nothing | expected, and their absence is read as evasion |
| Rebuttal length | hard-limited, so every sentence must carry a number or a correction | long is acceptable but a long letter that avoids the point is worse than a short one that answers it |
| The fatal move | claiming to fix something the reviewer will check | claiming a change in the letter that is not in the revised manuscript |

One rule holds in both cultures. The response is read against the manuscript. Any claim in the
letter that the manuscript does not support converts a survivable concern into an integrity
concern, and integrity concerns are the ones that end submissions.

## Concern triage

Classify every comment before writing a word of response. The class determines the evidence
obligation.

| Class | When it applies | Evidence the author must supply | Typical letter length |
|---|---|---|---|
| Accept | the reviewer identified a real defect and the fix is possible | the fix itself, with the location | two sentences plus the change |
| Partially accept | the defect is real but the proposed fix is wrong, or the fix is right but the framing is off | the part accepted, the part declined, and the reason for the split | one paragraph |
| Rebut with evidence | the reviewer misread, or the criticism rests on a factual error, or the requested comparison is not comparable | the misread location, or the protocol difference, or the new measurement that answers the concern's resolution test | one paragraph plus a pointer |
| Defer to limitations | the request is legitimate and cannot be met within this revision | the limitation entry, the reason, and the protocol a future study would use | one paragraph |
| Escalate to the editor | the reviewer is factually wrong on a point the manuscript already answers, or the request violates the venue's scope or ethics policy | the manuscript location that answers it, and the policy statement | a short note in the cover letter, never in the per-reviewer letter |

Track the four counts in the cover letter. A letter that accepts everything signals that the
authors did not evaluate the comments. A letter that rebuts everything signals the same.

## What convinces

- **A number the reviewer did not have.** A new run, a new ablation, a corrected comparison,
  reported with the protocol, the seed count, and the dispersion. This is the strongest move
  available in any culture.
- **A pointer to the existing text.** A misreading is answered by quoting the sentence the reviewer
  missed, with its location, and then asking whether it should be made more prominent. Quote it
  exactly.
- **A declared protocol difference.** When a requested comparison is not comparable, state the three
  differences explicitly and offer the control run. This is the honest form of "we cannot compare".
- **A concession made early.** When the reviewer is right, say so in the first sentence and describe
  the fix. Reviewers reward authors who take a hit well, and they re-read the rest of the letter
  more charitably.
- **A scope statement.** When the criticism is that the paper did not do something it never claimed
  to do, restate the claim in the paper's own words and offer to make the boundary explicit in the
  abstract and the limitations.
- **A revised sentence quoted verbatim.** For a clarity or framing concern, paste the new sentence
  into the letter. It costs three lines and removes the doubt.

## What antagonizes

| Move | Why it costs | Replacement |
|---|---|---|
| "We respectfully disagree" with no evidence | reads as a refusal | state the evidence first, then the position |
| "This is beyond the scope of the paper" without restating the claim | reads as an excuse | restate the claim and the boundary it implies |
| "The reviewer may have missed that..." | condescending, and it is usually wrong | "We see that Section 4.2 states this only in passing. We have moved it into the abstract." |
| Restating the contribution instead of answering | the reviewer asked a question, not for the abstract again | answer the question in the first sentence |
| Blaming the page limit | the venue set the limit | cut something else, or defer explicitly |
| Promising an experiment without tracking it | a promise that fails is worse than a deferral | decide run or defer, and record the decision |
| Arguing about novelty in the abstract | novelty is established by the related-work section and the search record | point to the near-miss list and the concrete difference |
| A long letter that answers two of ten points | the unanswered points are the ones that decide the score | answer all ten, in order |
| Escalating to the editor over a scientific disagreement | the editor sides with the reviewer | escalate only on a factual error the manuscript already settles, and only in the cover letter |
| Adding a new claim to answer a concern | the new claim has no evidence behind it | answer within the existing claim, or run the experiment |
| Copying the same paragraph into every reviewer letter | it is correct practice, but only when phrased for each reviewer's own comment | phrase each response against that reviewer's wording |
| Mentioning another reviewer to show consensus | it breaks blindness and can void the review | never, in any venue, in any wording |

## Using the review's own structure

A review that classifies each comment helps. When the review does not, infer the class from the
comment's shape, which is a reliable signal of what the reviewer wants.

| Comment shape | What the reviewer wants | Best response class |
|---|---|---|
| "The authors should compare with X" | a comparison, or a justification for its absence | accept if comparable, rebut with the protocol difference if not |
| "Unclear how Y is computed" | a specification, not a new experiment | accept, and quote the new equation or configuration |
| "Why is Z better than the baseline?" | a mechanism, which requires an ablation | accept and run the ablation, or downgrade the claim |
| "The paper does not discuss W" | a related-work addition | accept, add it, and state the concrete difference |
| "Results on only one dataset" | a second dataset | accept and run it, or defer with the limitation and the reason |
| "The improvement is marginal" | the uncertainty | accept, and add the seed dispersion |
| "This is incremental" | a novelty argument against the nearest prior work, not a broader claim | rebut with the near-miss list and one concrete mechanism difference |
| "The writing needs polishing" | nothing, in a rebuttal. In a journal revision it is a real item | journal: accept and do a full pass. Conference: one line, no argument |

## Response order and length

- Answer in the reviewer's order. Reviewers check off as they read, and a reordered letter forces
  them to search.
- Put the strongest responses first among the comments of equal severity, not first overall. A
  letter that opens with a minor accept and buries the decisive experiment reads badly.
- Keep each response under roughly 150 words unless a new experiment is being reported. Anything
  longer is read as defensive.
- Use a heading per comment. Reviewers copy headings back into their re-review.
- State the position in the first two sentences of the response. Do not make the reviewer wait
  four sentences for whether the concern was accepted.

## Anti-sycophancy in the author role

The mirror of the reviewer's calibration rule applies to the author's own side. When the authors are
tempted to concede to end the argument, or to press a rebuttal because the deadline is near, apply
the evidence score.

- Score counter-arguments 1 to 5 by directness and sufficiency: 1 is an assertion, 3 is incomplete
  support, 4 or 5 directly closes the resolution test. Existing evidence overlooked by the reviewer
  can score 4 or 5; newness alone is not evidence quality.
- Send a rebuttal only at 4 or above. Below 4, the honest options are accept, partial accept, or
  defer. A weak rebuttal spends credibility that a later strong response needs.
- Never concede a concern that the evidence supports simply because the reviewer was emphatic.
  A concession that the data contradict is a factual error the next reviewer will find.
- Never accept a concern in the letter and leave the manuscript unchanged. The letter and the
  manuscript must agree, always, in both directions.
- When the authors and the responding author disagree about a classification, the evidence decides,
  not seniority. Record the residual risk if the decision goes against the evidence.

## Repeated rounds

At the second round, the rules change in one way. Only the concerns still open matter, and every one
of them needs either a new artifact or an explicit statement that the position is unchanged with
the reason. Do not re-argue a closed concern, and do not re-run an experiment the reviewer already
accepted.

Track the round history in the revision ledger. A concern that was accepted in round one and not
fixed in round two is the single most common cause of a late rejection, because it converts an
author from someone with a defect into someone who does not respond to reviews.
