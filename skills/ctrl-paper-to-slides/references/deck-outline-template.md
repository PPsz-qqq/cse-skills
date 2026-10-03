# Deck outline template

One Markdown file per deck, kept beside the exported artifact so the deck can be regenerated. The
outline is the source of truth. The PPTX is a rendering of it.

Name the outline `slides/<venue>-<year>-<slug>-outline.md` and the deck
`slides/<venue>-<year>-<slug>.pptx`, per
[artifact-contract.md](../../ctrl-shared/core/artifact-contract.md).

## Front matter

```markdown
# <paper title>
- Venue and slot: <venue> <year>, <oral | spotlight | poster teaser | defense | group meeting>
- Talk length: <n> minutes plus <n> minutes of questions
- Presenter: <name>
- Paper revision presented: <path> hash <sha256 prefix>
- Ledger: ctrl-claims.md, rows presented: <C1, C3, C7, ...>
- Gate status at build time: G2 <pass | fail>, G3 <pass | fail | waived>
- Build date: <date>
```

`Paper revision presented` matters. A deck built from a preprint and presented after a revision is
a mismatch, and the hash is what makes it visible. If G3 has not passed, the deck may still be
built, but the outline records the gate state and the results slides carry the `preliminary` marker.

## Slide list

Each entry is a slide. Keep the sequence and delete the ones that do not apply.

```markdown
## S1. Title
- One line: the paper title, exactly as submitted
- One line: authors and affiliations
- One line: venue, track, and date
- Visual: none, or the venue template
- Timing: 15 s
- Ledger rows: none

## S2. The problem in one picture
- One line: what the task is in the field's terms
- Visual: the task-definition figure, regenerated if the paper's version is unreadable at distance
- Timing: 45 s
- Ledger rows: none

## S3. Why it matters
- One line: the consequence of solving it, stated with a number where one exists
- Visual: one image from the application domain, sourced and credited
- Timing: 30 s
- Ledger rows: <row IDs if a number appears, otherwise none>

## S4. What is missing today (the gap)
- One line: the specific limitation of prior work, stated as a mechanism, not as "performance is
  not good enough"
- Visual: none, or a two-panel contrast
- Timing: 45 s
- Ledger rows: none

## S5. Contributions
- Three to four bullets, each a claim the paper establishes
- Each bullet carries its ledger row ID in the notes, not on the slide
- Visual: none
- Timing: 60 s
- Ledger rows: C1, C4, C9

## S6. Method overview, the ONE key figure
- One line: the mechanism in a single sentence
- Visual: Fig. 2 of the paper, the overview figure, reused if legible at distance
- Timing: 90 s
- Ledger rows: none

## S7. Method detail, the component that is new
- One line: what is new, and what it replaces
- Visual: the component diagram with the equations, three lines maximum on the slide
- Timing: 90 s
- Ledger rows: none

## S8. Experiment setup
- One line per item: datasets, splits, baselines, metrics, hardware
- Visual: a compact setup table
- Timing: 45 s
- Ledger rows: none

## S9. Main results
- One line: the headline comparison, with the protocol qualifier
- Visual: the main results table, reduced to the rows a listener can read
- Timing: 90 s
- Ledger rows: C1, C2

## S10. Ablation
- One line: which component contributes what
- Visual: the ablation table or the component-wise bar chart
- Timing: 60 s
- Ledger rows: <row IDs>

## S11. Failure cases
- One line: where the method loses, and why
- Visual: two to four qualitative failures with the failure mode labelled
- Timing: 45 s
- Ledger rows: none

## S12. Limitations
- Two to three bullets, each a real boundary from the paper's limitations section
- Timing: 30 s
- Ledger rows: none

## S13. Conclusion
- One line: what the field now knows that it did not before
- Timing: 20 s

## S14. Thank you and questions
- Contact, code repository, and the paper reference
- Timing: 5 s
```

## Backup slides

Backup slides are not in the timing budget. They sit after the thank-you slide and are reached only
by answering a question, so the presenter must be able to navigate to one without a search.

```markdown
## B1. Full results table, all baselines        <- "what about <baseline>?"   rows C1 to C8
## B2. Per-dataset breakdown                     <- "does this hold on <other dataset>?"
## B3. Seed dispersion and significance          <- "is this within noise?"
## B4. Runtime and memory                        <- "what is the inference cost?"
## B5. Hyperparameter sensitivity                <- "how sensitive is this to <parameter>?"
## B6. Protocol details                          <- "were the baselines trained under one protocol?"
## B7. Additional qualitative results            <- "can you show more examples?"
## B8. The protocol block and the ledger         <- a methodological challenge needing exact config
```

B8 is allowed to be dense. It exists to settle a dispute, not to be read from the back of the room.

## Timing budget

The talk length sets the slide count and the seconds per slide. Build the budget before building
the slides, and check it after.

| Slot | Slides | Main-body seconds | Notes |
|---|---|---|---|
| 5-minute lightning | 6 to 8 | about 40 s per slide | two results slides maximum, no ablation slide |
| 10-minute spotlight | 10 to 12 | about 45 s per slide | one ablation slide |
| 15-minute oral | 14 to 16 | about 50 s per slide | the sequence above fits with room for one extra results slide |
| 20-minute oral | 18 to 22 | about 55 s per slide | add a related-work slide and a second ablation slide |
| 45-minute defense | 35 to 45 | about 60 s per slide | add the full related-work and methodology walkthrough |
| 3-minute poster teaser | 4 to 5 | about 35 s per slide | problem, gap, contribution, one result, contact |

Rules that keep the budget honest.

- The per-slide numbers in the outline must sum to the talk length minus 10 percent. The remainder
  is the overrun every talk experiences.
- A slide at 90 seconds is a slide the presenter talks over. Reduce its content or split it.
- Never plan to speak at the slide count the venue's template implies. Venue templates run long.
- If the sum exceeds the slot, cut a slide rather than speeding up. Speaking faster is how a
  method slide becomes incomprehensible.

## Number traceability

Every number that appears on a slide or in the speaker notes carries its ledger row ID in the
outline. Before the deck is used, check the annotation.

```text
[ ] Every number on a slide appears in a ledger row with Gate = G2 pass
[ ] No number on a slide differs from the manuscript at the same precision
[ ] Every percentage states absolute or relative, on the slide itself
[ ] Every comparison on a slide names the protocol qualifier, at least in the notes
[ ] No number was recomputed for the slide
[ ] No number appears on a slide that is absent from the manuscript
[ ] Each result slide records the revision hash it was built from
```

If a number the audience will ask about is not in the ledger, the slide does not show it. The
backup slides are where the detail lives, and they follow the same rule.

## Regenerating the deck

The outline is structured enough to rebuild the deck from.

1. Parse the `## S<n>. <title>` headings for slide order and titles.
2. Parse the `- One line:` entries as each slide's title line and first bullet.
3. Parse the `- Visual:` entries as figure references, resolved through the figure inventory in
   [axis-figure-inventory.md](axis-figure-inventory.md).
4. Parse the `- Timing:` entries to recompute the budget, and fail the build if the sum exceeds the
   slot.
5. Parse the `- Ledger rows:` entries and verify each row's gate status before writing the deck.
6. Write the deck with a script, and place the script beside the outline so the deck can be rebuilt
   after the paper changes. A deck without its generator is a dead artifact.

## Presenter notes

Three notes per result slide, no more.

```markdown
### Notes S9
- Say the protocol qualifier out loud before the number: <the qualifier>
- The one sentence the audience must remember: <sentence>
- If asked about <baseline>, go to B1
```

A notes field that transcribes the paper is a sign the presenter has not prepared the talk.
