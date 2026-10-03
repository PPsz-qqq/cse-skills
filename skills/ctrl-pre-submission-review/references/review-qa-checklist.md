# Review QA checklist

Run this before delivering any review. A review is itself a claim, and an ungrounded review costs
the authors work on defects that do not exist while hiding the ones that do.

Answer each item `pass`, `fail`, or `not applicable`, and record the pointer that supports the
answer. A `fail` is repaired before delivery, not noted in a footnote.

## 1. Groundedness

```text
[ ] Every concern has a claim pointer that resolves to a real location in the manuscript
[ ] Every concern has an evidence pointer that resolves to an artifact or a manuscript location
[ ] Every quotation matches the manuscript text exactly
[ ] Every number cited in a concern appears in the manuscript as written, at the same precision
[ ] No concern depends on a location or artifact that was not actually read
[ ] A location not found is marked [NOT FOUND: <what you searched>], never approximated
[ ] Anything that could not be verified is marked [UNVERIFIED: <what is missing>]
[ ] No statement about the field, a venue, or a baseline rests on model memory alone
```

The last item is the one that fails most often. A claim such as "the field has moved to NMS-free
detectors, so this contribution is outdated" is a literature claim and needs a citation or a
documented search. Without either, reframe it as a `Question`.

## 2. Non-invention

```text
[ ] No invented citation, dataset statistic, baseline number, hardware fact, or experiment
[ ] No invented reviewer name, institution, expertise, or biography
[ ] No invented venue rule, page limit, or review policy
[ ] No invented location in the manuscript, such as a table row or page number
[ ] No described figure or table that does not exist in the reviewed revision
[ ] No concern about a file that was never opened
[ ] No attributed intent, such as "the authors deliberately chose an unmatched baseline"
[ ] No claim about what the real venue's reviewers would decide
[ ] Every rule stated as a venue requirement is either quoted from the current guidelines or
    marked [UNVERIFIED: guidelines not checked]
```

A missing element is written as a gap with a stated remedy. "The detector checkpoint is not stated
anywhere in the paper or the released config, and the number cannot be reproduced without it" is
correct. "The authors probably used the standard checkpoint" is fabrication with a hedge.

## 3. Severity calibration

```text
[ ] Every Blocking concern states why the central case cannot be established without it
[ ] No Minor concern is marked Blocking
[ ] No evidence, validity, ethics, or integrity problem is marked Minor
[ ] No presentation issue is marked Major merely to sound severe
[ ] Severity follows impact on the manuscript's case, not the tone of the writing
[ ] The recommendation follows from the dimension profile by the stated mapping rule
[ ] No score of 9 or 10 with a Blocking concern open
[ ] No score of 9 or 10 with three or more Major concerns
[ ] Every dimension scored 4 or 5 names the artifact that earns it
[ ] Every dimension scored 1 or 2 names the defect that costs it
[ ] Every consensus severity is the maximum assigned, not an average
[ ] No severity changed without a change in the artifact or in the evidence
```

The calibration test for the whole review. If the Dimension profile would map to a different
recommendation than the one written, the review is internally inconsistent and must be corrected
before delivery.

## 4. Independence integrity

```text
[ ] The isolation path is stated in the report header and in the synthesis
[ ] The packet contains no concerns, hypotheses, or conclusions
[ ] The packet contains no prior-round report, author response, or risk assessment
[ ] Each reviewer received only the packet, its own brief, the skeleton, and the rules
[ ] No reviewer saw another reviewer's report, brief, or the synthesis
[ ] Every emphasis brief was written before the first report existed
[ ] No brief names an identity, institution, or personality
[ ] Every report was frozen before any comparison, with a recorded hash, or with `hash not computed` and an immutable file version when no hashing tool exists
[ ] No frozen report was edited; corrections are appended and dated
[ ] Consensus is labelled only where at least two reports raised the same underlying mechanism
[ ] Every consensus row states the shared mechanism, not just similar wording
[ ] Where isolation failed, the deliverable carries the correct non-blindness label
[ ] The word consensus does not appear in a declared non-blind deliverable
[ ] The synthesis is in its own file and appears in no reviewer-facing file
```

## 5. Coverage without quota

```text
[ ] All eight dimensions were scored, not only the emphasized ones
[ ] The per-axis taxonomy for each active axis was walked
[ ] A severity level with no grounded concern is stated as empty rather than padded
[ ] No concern was added to reach an expected count
[ ] No grounded concern was dropped to make the review more agreeable
[ ] Concerns the manuscript already handles are acknowledged, not re-raised
[ ] At least one sentence per report records what the manuscript does well, if anything
[ ] Every secondary axis with a claim was assessed under its own evidence rules
```

The balance test. A report that finds only defects reads as hostile and is discounted by the
authors. A report that finds only praise reads as useless and is discounted by the editor. Neither
should be manufactured. The correct output is whatever the artifact supports.

## 6. Staleness and provenance

```text
[ ] Every reviewed file has a recorded content hash and modification time
[ ] The manuscript did not change after any report was frozen
[ ] Any artifact that changed after a verdict invalidated that verdict
[ ] The round is marked STALE rather than patched if the revision moved
[ ] The gate verdict names the revision it was computed from
```

## 7. Consistency between reports

```text
[ ] A concern raised in an earlier round and repaired is marked closed with its evidence
[ ] A concern raised in an earlier round and not repaired is carried forward with its original ID
[ ] A score that moved between rounds has a stated reason tied to an artifact change
[ ] No concern silently disappeared between rounds
[ ] The synthesis accounts for every concern ID present in any frozen report
```

## 8. Deliverable completeness

```text
[ ] One frozen report file per reviewer, each hashed
[ ] One synthesis file, separate from every reviewer file
[ ] A blocking-flags roll-up with a resolution test per flag
[ ] Every concern ID follows the axis-prefixed form
[ ] A gate report using the standard block, with the failing criterion and the smallest fix
[ ] The loop outcome stated as converged, budget exhausted, or stopped by user
[ ] The effort tier stated
[ ] The final message separates what was verified from what remains unverified
```

## Self-audit statement

Close every delivered review with these five lines, filled in.

```text
Self-audit
- Concerns delivered: <n>, of which Blocking <n>, Major <n>, Minor <n>, Question <n>
- Concerns dropped for lack of a pointer: <n>, with the reason for each
- Items marked [UNVERIFIED]: <n>, listed
- Items marked [NOT FOUND]: <n>, with the search performed
- Isolation path: <path>, so the independence claim in this review means <what it means>
```

## Anti-patterns to check for last

| Anti-pattern | Recognition signal | Correction |
|---|---|---|
| Padding | the report has exactly the same concern count as the previous round | report the actual count and state which levels are empty |
| Harshness theatre | severity words appear without a corresponding pointer | delete the escalation, keep the finding |
| Agreeableness | a defect visible in the table is absent from the report | add it with its pointer |
| Retrofit scoring | the recommendation is stated first and the profile supports something else | recompute the profile, then re-derive the recommendation |
| Vigilante forensics | a numerical anomaly is called a confirmed error with no arithmetic proof | reclassify as ambiguity or input needed |
| Category error | a `det` paper judged by control-theory criteria, or the reverse | fix the venue class and re-run the affected dimensions |
| Synthesis creep | consensus language appearing in a reviewer file | move it to the synthesis file |
| Silent non-blindness | three similar reports with no isolation label | add the label, or re-run on a blinded path |
