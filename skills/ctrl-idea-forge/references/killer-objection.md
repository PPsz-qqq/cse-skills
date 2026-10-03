# Killer objection and independent adjudication

The purpose of this step is to find the objection that ends the paper, while it is still cheap to
answer. It is a two-part mechanism. One pass writes the strongest rejection memo an experienced area
chair would produce. A separate pass adjudicates, and it is not a defender.

The mechanism is ported from the adversarial attack-and-adjudication pair described in the pack's
automation research notes, which pairs an attack thread that writes the strongest short rejection memo
with an independent adjudication thread that classifies each point against the current text with
file-and-line evidence rather than arguing back.

## Separation rule

The two roles must not be the same pass, and they must not share a context that contains the plan's
justifications.

| Role | Sees | Does not see |
|---|---|---|
| Attacker | the frozen plan, the hypothesis, the protocol blocks, the artifacts | the authors' rationale, the rebuttal, any prior adjudication |
| Adjudicator | the plan, the objection memo, the artifacts | the attacker's reasoning about severity, any defence |

If genuine context separation is unavailable, run the two roles as two separate invocations and state
explicitly that mutual blindness was not guaranteed. Never present a single-pass critique as an
independent adjudication. This mirrors the reviewer-independence rule in
[../../ctrl-shared/core/review-rubrics.md](../../ctrl-shared/core/review-rubrics.md).

## Part one: the rejection memo

Write at most 200 words. It is a memo, not a review. It must read as a decision, not as a list of
worries, and it must name the reason for rejection.

Constraints that make it useful.

- Assume the reviewers are competent and hostile. No straw men.
- Attack the central case, not the presentation.
- Exactly one primary reason for rejection, with at most two supporting points.
- Every point carries a pointer to the plan or an artifact. A point without a pointer is a preference
  and is dropped.
- No severity inflation. A typographic point is not a rejection reason.
- Written before the plan is defended. Once a defence exists, the memo is contaminated.

Template.

```text
Rejection memo
- Recommendation: reject
- Primary reason: <one sentence>
- Supporting point 1: <pointer to the plan or artifact>
- Supporting point 2: <pointer to the plan or artifact>
- What would have changed this: <one sentence, stated as obtainable evidence>
```

### Prompts that produce useful memos

Ask these in order and keep the strongest answer for each.

1. What is the single claim the paper needs the reader to accept, and what is the weakest link in the
   chain that supports it?
2. If the main result is real, what is the cheapest alternative explanation, and does the plan rule
   it out?
3. Which named baseline is most likely to match the method under the declared protocol, and what
   happens to the paper then?
4. Where does the claim outrun the protocol? Name the row in the comparison table where the arms
   differ.
5. Which of the five axes' calibration rows in
   [../../ctrl-shared/core/evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md)
   applies to this comparison, and is it addressed?
6. What does the plan assume about the deployment or evaluation setting that the venue's reviewers
   will not grant?
7. What is the honest answer to "why should I believe the number"?

## Part two: adjudication

The adjudicator classifies each point. It does not argue, does not defend, and does not soften.

| Verdict | Meaning | Requirement |
|---|---|---|
| `answered_by_current_plan` | the plan or an existing artifact already addresses the point | cite the location, with file and line where the artifact is machine-readable |
| `partially_answered` | something addresses it, but incompletely | cite the location and state precisely what is missing |
| `still_unresolved` | nothing addresses it | state the smallest change that would move it to `partially_answered` |

Output format.

```markdown
| Point | Memo reference | Verdict | Evidence pointer | Smallest change to resolve |
|-------|----------------|---------|------------------|----------------------------|
| 1 | primary reason | still_unresolved | ctrl-plan.md has no matched-protocol row for baseline B | add baseline B under the declared protocol, or drop the comparison |
```

Adjudication rules.

- A point moves to `answered_by_current_plan` only with a pointer. An assertion that the plan handles
  it is `still_unresolved`.
- The adjudicator does not invent new objections. Its job is classification, and adding objections
  silently changes the memo after the fact.
- If the adjudicator cannot assess a point because information is missing, the verdict is
  `still_unresolved` with the missing item named. There is no fourth verdict.
- Any `still_unresolved` point on the primary reason blocks G1. This is the same blocking semantics as
  a `Blocking` concern in
  [../../ctrl-shared/core/review-rubrics.md](../../ctrl-shared/core/review-rubrics.md).

## Responding to the objection

The response is a plan change, not a paragraph. For each still_unresolved point, exactly one of three
actions, recorded in `ctrl-plan.md`:

1. **Close it with evidence.** Add the named experiment, baseline, or analysis to the plan, with its
   budget. This is the preferred action when the point touches the primary reason.
2. **Close it with scope.** Narrow the claim so the objection no longer applies, and record the
   narrowing. For example, drop a generalization claim and state the claim for the tested regime
   only.
3. **Accept it and disclose it.** Keep the claim, and put the objection in the limitations section as
   a stated limitation. This is legitimate only for points that do not challenge the central case.

Scoring a rebuttal uses the anti-sycophancy mechanism from
[../../ctrl-shared/core/review-rubrics.md](../../ctrl-shared/core/review-rubrics.md). Score the
response 1 to 5 on evidence quality, where 1 is an assertion, 3 is a pointer to existing material, and
5 is new evidence that directly tests the point's resolution test. Concede only at 4 or above.
Otherwise the point stays still_unresolved and the resolution test is restated.

## Loop budget

Two rounds. The first round finds the objections, and the second confirms whether the plan changes
closed them. If the second round leaves a still_unresolved primary reason, do not run a third round.
Report non-convergence and name the unrepaired point. This follows the loop stop rules in
[../../ctrl-shared/core/verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md).

```text
Killer objection loop: converged | budget exhausted with residual defects | stopped by user
- Round 1: <n> points, <n> unresolved
- Round 2: <n> points, <n> unresolved
- Unrepaired primary reason: <one line, or "none">
```

## Anti-patterns

- **The soft memo.** A memo that reads like a review with suggestions is not an attack and finds
  nothing. It must name a rejection reason.
- **The defender adjudicator.** An adjudicator that declares every point handled without evidence
  is acting as a defender. Check the pointers, not a quota: all points may genuinely be answered.
  Zero `still_unresolved` findings is not proof of contamination and never licenses inventing one.
- **The severity downgrade.** A point that challenges the central case is never `Minor`, however
  easy it is to describe. See the severity tiers in
  [../../ctrl-shared/core/review-rubrics.md](../../ctrl-shared/core/review-rubrics.md).
- **The memo written after the defence.** Once a rebuttal exists, the memo is contaminated and its
  value is gone.
- **The unbounded objection list.** Twenty points is a review, not a memo. The strongest one plus two
  supporting points is the format because it forces a decision about what matters.
- **The rhetorical escalation.** A memo that is hostile in tone rather than precise in pointer is
  useless and will be dismissed.
