# Revision tracking

The ledger that makes the response letter checkable. Every comment gets a row before any response
is drafted, and every row is resolved before the letter is sent.

Keep the full ledger at `cse-revision-<round>-ledger.md`. Keep the per-reviewer summary block in
each reviewer's letter. The full ledger is author-side: never put it into a reviewer-facing file,
and in the `isolated` response format of [red-lines.md](red-lines.md) never let one reviewer's rows
reach another reviewer's letter.

## Ledger schema

```markdown
| ID | Reviewer | Comment (short) | Class | Owner | Evidence needed | Experiment status | Manuscript location | Claim rows | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1.3 | R1 | compare with <method> at matched resolution | partially accept | A2 | control run at 512x512, 3 seeds | exp/det_ctrl_r512, done | Table 3, Sec 5.2 | C11, C12 | closed |
| 2.1 | R2 | add <dataset> evaluation | defer | A1 | dataset availability statement | not run, unavailable | Sec 7 lim. 2 | - | closed |
| 3.4 | R3 | p-value on the 0.4 delta | accept | A3 | 5 paired seeds, t interval on the difference (a signed-rank test cannot reach 0.05 with 3 pairs) | exp/det_seeds, running | Table 4 | C14 | open |
```

Column rules.

| Column | Content |
|---|---|
| `ID` | the reviewer's own comment number, verbatim, as `<reviewer-number>.<comment>` |
| `Reviewer` | the reviewer designator used internally; it appears in another reviewer's letter only in a shared response format |
| `Class` | accept, partially accept, rebut with evidence, defer to limitations, escalate |
| `Owner` | one named author. An unowned row is an unfinished row |
| `Evidence needed` | the artifact that would close the comment, named specifically |
| `Experiment status` | not needed, planned, running, done, failed, abandoned. Never blank |
| `Manuscript location` | section, table, or figure, or `none` with the reason |
| `Claim rows` | the claim IDs in `cse-claims.md` that the new evidence creates or updates |
| `Status` | open, blocked, closed. A letter may not claim a closed row that is still open |

## The promise-to-result rule

The letter is a claim about the manuscript, so every promised experiment is a claim awaiting
evidence. Apply this rule without exception.

1. When the response promises a run, create the ledger row with `Experiment status: planned` and a
   named owner before the letter is drafted.
2. When the run finishes, record the result artifact path, update `Claim rows` in `cse-claims.md`,
   and only then write the result into the letter.
3. When the run fails or cannot be completed, the letter states the failure and the reason, and the
   row moves to `abandoned` with the reason. It never silently becomes a deferral.
4. A letter that claims a result for a row whose status is not `closed` is not sent.
5. Before sending, reconcile: every sentence in the letter that reports a result must correspond to
   a closed ledger row, and every closed ledger row that reports a result must appear in the letter
   or in the manuscript.

The deadline does not change this. A missing experiment written as a limitation is a survivable
paper. A promised experiment written as a result is a fabrication.

## The revision plan

Produce the plan before editing the manuscript. It is the artifact that keeps a long revision from
drifting.

```markdown
# Revision plan, round <n>
- Manuscript revision: <path> hash <sha256>
- Reviews received: <n>, on <date>
- Deadline: <date>  Days available: <n>
- Effort tier: <standard | thorough | submission>

## Work packages
| WP | Covers comment IDs | Work | Owner | Estimated cost | Dependency | Status |
|---|---|---|---|---|---|---|
| WP1 | 1.3, 2.2 | control run at matched resolution | A2 | 12 GPU-hours | none | running |
| WP2 | 2.1 | dataset availability investigation | A1 | 2 hours | none | done |
| WP3 | 3.4 | seed sweep and significance test | A3 | 6 GPU-hours | WP1 hardware | planned |
| WP4 | all | manuscript edits and number reconciliation | A1 | 1 day | WP1, WP3 | blocked |

## Decisions taken
| Decision | Reason | Residual risk |
|---|---|---|
| decline the dual-camera experiment | no second camera in the revision window | reviewer may hold the concern open |

## Cut list
<what is being removed from the manuscript to make room for the additions, and who owns the cut>
```

Work packages are the unit of scheduling, not comments. Three comments that all need the same
control run are one work package. A work package with no owner or no cost estimate is a wish.

## New-experiment requests, run versus argue versus decline

Run the decision as a table, one row per request, and put it in the revision plan.

| Question | If yes | If no |
|---|---|---|
| Is the requested comparison actually comparable under our protocol? | continue to the remaining checks, not an automatic run decision | explain the mismatch and assess a matched control instead |
| Is the missing artifact already obtainable from runs we have? | produce it from existing logs, no new compute | estimate the new compute cost |
| Does the cost fit inside the remaining days at the stated budget? | run it | decline or defer, and say so plainly |
| Have we committed to retaining both positive and negative outcomes? | record that reporting commitment; other checks decide whether to run | resolve the reporting commitment before any run; never select whether to report after seeing results |
| Would the result change a reader's decision? | run it | decline, and say the request would not change the conclusion |
| Is the request within the paper's stated scope? | run it | restate the scope, and offer a limitation entry instead |

Cost must be stated in the letter for any declined request, in comparable units. "Roughly 40
GPU-hours on an A100 plus two weeks of annotation" is a cost. "Infeasible" is not.

Never decide to run an experiment because the reviewer asked, and never decide to decline because it
is inconvenient. The decision rule above is the decision. Record which row decided it.

## Revision-package consistency check

Run before sending. Each item is a check against an artifact, not a recollection.

```text
[ ] Every comment ID in every review appears in the ledger
[ ] Every ledger row has a class, an owner, and a status
[ ] Every ledger row with Class = accept or partially accept names a manuscript location
[ ] Every manuscript location named in the ledger actually contains the change
[ ] Every experiment reported in a letter has Experiment status = done and a result artifact path
[ ] Every result reported in a letter has a claim row, and that row passes G2
[ ] Every number in a letter matches the manuscript at the same precision
[ ] Every figure or table cited in a letter exists in the revised manuscript with that number
[ ] Every deferral names the limitation entry that now carries it
[ ] No letter introduces a claim absent from the manuscript
[ ] The response format is recorded; isolated letters never mention another reviewer, and no letter quotes a score or recommendation
[ ] The cover letter's counts match the ledger
[ ] The marked-up manuscript's highlights match the change list
[ ] The response files and the manuscript revision carry the same hash recorded in the ledger
```

## Round history

Append one block per round. Never edit a past block.

```markdown
## Round 2, <date>
- Reviews: 3  Comments: 24
- Closed in this round: 19  Carried forward: 3  Newly created by this round's text: 2
- Concerns accepted in round 1 and left unfixed: 0
- Experiment promises made in round 1 and delivered: 4 of 4
- Result: minor revision
```

The two numbers worth watching are the carried-forward count and the unfixed-accepted count. A
rising carried-forward count means the revision is not converging, and the correct response is to
report non-convergence to the user rather than to run another round.

## Multi-round stop rule

Use the shared stop rule in
[verdicts-and-loops.md](../../cse-shared/core/verdicts-and-loops.md): at most four rounds, readiness
at least 6/10 and recommendation `Accept` or `Minor revision`, with no unresolved Blocking concern;
stop earlier on an applicable `PASS` with none open. Missing inputs remain `BLOCKED`, evaluated
unmet criteria `FAIL`. At the cap report `budget exhausted with residual defects` and name them;
never introduce `ready`/`almost` verdicts or run a fifth round silently.
