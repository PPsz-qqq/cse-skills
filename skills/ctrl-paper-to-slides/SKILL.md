---
name: ctrl-paper-to-slides
description: >-
  Convert an accepted or submitted control-science-and-engineering paper into a conference, oral,
  or defense deck across object detection (目标检测), tracking (目标跟踪), re-identification
  (重识别), cooperative navigation (协同导航), and filtering or state estimation (滤波). Builds a
  Markdown outline as the source of truth, chooses and regenerates figures, enforces a per-minute
  timing budget, traces every number on a slide to a G2-passed ledger row, and prepares the
  anticipated-question bank with backup slides. Use it when the user asks for 论文做PPT, 学术汇报,
  组会汇报, 答辩PPT, 会议报告, 幻灯片, paper to slides, conference talk, oral presentation deck,
  defense slides, or a poster teaser for CVPR, ICCV, ECCV, TAC, T-RO, ICRA, TGRS, 自动化学报, or a
  comparable venue.
---

# CTRL paper to slides

Turn a paper into a talk whose every spoken number can be traced to an artifact, and whose slides
are legible from the back of the room.

## Start here

Read [execution-contract.md](../ctrl-shared/core/execution-contract.md) first. Select the smallest
useful mode, confirm the inputs and available tools, and load only the references needed by the
current step. Use only the output sections relevant to this request; a diagnostic or draft is not
a gate-passed final artifact.

For a literature or lab talk without this pack's ledger, build a scoped source ledger from the
paper and label external numbers `reported`; do not invent G2/G3 history. An outline or qualitative
method deck can proceed without result verification. Final quantitative slides need checked rows.

## Default stance

The outline is the source of truth. The deck is a rendering of the outline, regenerable from it.

- Build the outline first, in Markdown, at `slides/<venue>-<year>-<slug>-outline.md`. Never build
  slides by hand and reverse-engineer the outline afterwards.
- Every number on every slide traces to a row in `ctrl-claims.md` whose gate is G2 pass. A number
  that is not in the ledger does not go on a slide, in the body or in the backup section.
- The paper's own figures are reused by default. Regenerate only for a stated legibility, palette,
  panel-selection, or aspect-ratio reason, and keep the generating script beside the figure.
- Reuse figures and numbers. Never regenerate data for a talk. A slide figure that shows a different
  value from the manuscript is a reconciliation failure, not a design choice.
- The deck inherits the manuscript's validity boundary. If the paper has simulation only, the
  results slide says so on the slide, not only in the notes.
- The default effort tier is `standard` for a lab talk, `thorough` for a venue oral or a defense.

## Workflow

1. **Fix the slot and the gate state.** Record the venue, the talk length, the question time, the
   audience, the language, and whether the paper's G2 and G3 have passed. If G3 has not passed, the
   deck may still be built, but every results slide carries a `preliminary` marker and the outline
   records the gate state.

2. **Build the timing budget before the slides.** Use the slot table in
   [references/deck-outline-template.md](references/deck-outline-template.md). Fix the slide count
   from the available speaking time, excluding questions and backups. Plan at most 90 percent of
   that time and report the exact sum/reserve; template times are examples, not a promised fit.

3. **Draft the outline sequence.** Use the standard architecture: title, problem, motivation, gap,
   contributions, method overview with the one key figure, method detail, experiment setup, main
   results, ablations, failure cases, limitations, conclusion, thank you, then the backup slides.
   Write one line per slide stating that slide's single message. A slide whose message needs the
   word "and" is two slides.

4. **Select the figures.** Work the inventory in
   [references/axis-figure-inventory.md](references/axis-figure-inventory.md) for the paper's axes.
   For each visual, record `reuse` or `regenerate` with the reason, the source file, and the
   generating script when regenerating. Check every reused figure's rendered label height against
   the legibility minimum at the size it will occupy on the slide.

5. **Regenerate the figures that fail.** A publication figure scaled to 60 percent renders its
   12 pt labels at 7 pt. Write a plotting script beside the figure, named after it, so the deck can
   be rebuilt. The regenerated figure shows the same data as the paper's figure, verified against
   the ledger row, not against a recollection.

6. **Annotate every number with its ledger row.** Each results or ablation slide records the claim
   IDs it presents. Verify each row's gate is G2 pass and that no value differs from the manuscript
   at the same precision. State absolute or relative for every percentage, on the slide itself.

7. **Assemble the backup section.** Reach every anticipated question from a slide within one
   keystroke. Use [references/anticipated-questions.md](references/anticipated-questions.md) for the
   per-axis bank, and build one backup slide per question the audience for this venue actually asks.
   The protocol block and the ledger summary are always backup slides.

8. **Apply the design rules.** One message per slide, 18 pt body minimum, 4.5 to 1 contrast,
   semantic colour used consistently, no decorative 3D, no chartjunk, and no distinction conveyed by
   colour alone. The full rule set is in
   [references/slide-design-rules.md](references/slide-design-rules.md).

9. **Write the speaker notes.** Three notes per result slide: the protocol qualifier to say out
   loud, the one sentence the audience must remember, and the backup slide to go to if a specific
   question arrives. Notes are not a script of the paper.

10. **Export.** See the export section below. Write the deck with a script so it can be regenerated
    after the paper changes, and keep the script beside the outline. Never overwrite a deck that was
    already presented. A revision creates a new file.

11. **Run the rendered check on the exported artifact.** Every slide legible at 50 percent zoom, no
    overlap, no stretched figure, no missing font or glyph, the timing budget recomputed from the
    actual slides, and every number traceable. The checklist is at the end of
    [references/slide-design-rules.md](references/slide-design-rules.md).

12. **Rehearse against the clock once and report the result.** A deck that has never been timed is
    an untested artifact. If the rehearsal overruns, cut slides rather than speeding up. Record the
    question log after the talk, since a question asked twice is a finding about the paper.

## Output format

Outline, at `slides/<venue>-<year>-<slug>-outline.md`. Full template in
[references/deck-outline-template.md](references/deck-outline-template.md).

```text
# <paper title>
- Venue and slot: <venue> <year>, <oral | spotlight | defense>, <n> min plus <n> min questions
- Paper revision presented: <path> hash <sha256 prefix>
- Gate status at build time: G2 <pass | fail>, G3 <pass | fail | waived>
- Ledger rows presented: <C1, C3, C7>

## S1. Title
- One line: <the title exactly as submitted>
- Visual: <none | source>
- Timing: 15 s
- Ledger rows: <none | IDs>

## S9. Main results
- One line: <the headline comparison with its protocol qualifier>
- Visual: <file>, action <reuse | regenerate>
- Timing: 90 s
- Ledger rows: C1, C2

### Notes S9
- Say the protocol qualifier out loud: <qualifier>
- The one sentence to remember: <sentence>

## B1. Full results table
- Reachable by: <the question>
```

Figure inventory, inside the outline.

```text
| Slide | Source | Action | File | Script | Ledger rows |
| S9 | paper Table 2 | regenerate | fig/slide9-main-results.png | fig/slide9-main-results.py | C1, C2 |
```

Build report, delivered to the user with the deck.

```text
Deck build report
- Outline: slides/<venue>-<year>-<slug>-outline.md, hash <sha256 prefix>
- Deck: slides/<venue>-<year>-<slug>.pptx, <n> slides, <n> backup slides
- Timing budget: <n> s planned against <n> s available, <pass | overrun by n s>
- Numbers presented: <n> claims, all G2 pass | <n> rows not at G2 pass, listed
- Figures: <n> reused, <n> regenerated, scripts present for all regenerated
- Export: <format produced, tool and version used, date checked>
- Rendered check: <pass | the specific defect found>
- Not done: <rehearsal not timed, PDF not produced, fonts not embedded, or none>
```

## Export

The deliverable is the `.pptx`. Produce a PDF only after confirming, in the environment you are
running in right now, that a converter is present. Never infer availability from what was
installed somewhere else, and never refuse a format the current environment supports.

Run the check before promising a format.

```text
[ ] python-pptx imports and writes a file   -> .pptx is the deliverable
[ ] soffice --version answers, or PowerPoint is present   -> PDF export is available
[ ] pdflatex or xelatex answers, and the deck is Beamer   -> PDF export is available
```

| Target | Tool | Availability rule |
|---|---|---|
| `.pptx` | `python-pptx` | Run the import check. Where it succeeds, write the deck and deliver it |
| `.pdf` from a deck | LibreOffice `soffice --headless --convert-to pdf`, or PowerPoint's own export | Run the check first. Where neither is present, deliver the `.pptx` and say in one line that no PDF was produced, without claiming one |
| `.pdf` from Beamer | a LaTeX toolchain | Only if the deck is authored in LaTeX. Check for `pdflatex` or `xelatex` first |
| `.key`, `.odp` | the corresponding application | Check for the application. Where it is absent, do not claim the format was produced |

Rules for the export step.

- State which check you ran, its result, and the tool version, in the build report.
- Where a converter is absent, say so in one line and deliver the `.pptx`, which is a complete
  deliverable on its own. Never claim a file that does not exist on disk.
- A `.pptx` written by `python-pptx` is a real `.pptx`, not a placeholder, and it opens in
  PowerPoint and LibreOffice Impress. Do not describe it as a Markdown export.
- `python-pptx` does not embed fonts. A deck that uses a non-standard face renders in a substitute
  face on the presenting machine. Use a face present on the venue's machines, or produce a PDF in an
  environment that has the font.
- Video and animation do not survive a PDF conversion. If the deck carries a demo clip, deliver the
  `.pptx` with the media embedded and check it on the presenting machine.
- Never overwrite a deck that was presented or submitted. A revised deck is a new file.

## Red lines

- Never put a number on a slide that has no G2-passed ledger row, in the body or in the backup.
- Never regenerate a value for a talk. Re-run an experiment only if the paper itself is being
  revised, and then the ledger and the manuscript change together.
- Never present simulation as field data, in the body or in the notes. State it on the slide.
- Never claim an exported file that does not exist, and never describe a Markdown outline as a deck.
- Never present results as final when G3 has not passed. Mark them `preliminary` on the slide.
- Never carry a validity boundary in the notes alone when the results slide could mislead without
  it. The boundary that matters goes on the slide.
- Never invent a number in the speaker notes, and never round a remembered value into one.
- Never overwrite a previously presented deck.

## Related files

| File | Open when |
|---|---|
| [references/deck-outline-template.md](references/deck-outline-template.md) | You are drafting the outline, setting the timing budget, laying out the backup section, or writing speaker notes |
| [references/slide-design-rules.md](references/slide-design-rules.md) | You are checking legibility, contrast, charts, tables, figure reuse, or running the rendered-deck check |
| [references/axis-figure-inventory.md](references/axis-figure-inventory.md) | You are choosing figures for det, track, reid, cnav, or filt slides, or deciding reuse versus regenerate |
| [references/anticipated-questions.md](references/anticipated-questions.md) | You are building the backup section, or preparing answers for the questions this axis's audience asks |
| [../ctrl-shared/core/artifact-contract.md](../ctrl-shared/core/artifact-contract.md) | You are naming the outline and deck files, or checking the figure and script naming scheme |
| [../ctrl-shared/core/gate-contract.md](../ctrl-shared/core/gate-contract.md) | You are checking whether G2 or G3 permits the results to be presented as final |
| [../ctrl-shared/core/evidence-integrity.md](../ctrl-shared/core/evidence-integrity.md) | You are tracing a slide number to its source, or checking a comparison for a protocol qualifier |
| [../ctrl-shared/core/terminology-and-notation.md](../ctrl-shared/core/terminology-and-notation.md) | You need symbol, metric, or bilingual term conventions so the deck matches the manuscript |
| [../ctrl-shared/core/venue-matrix.md](../ctrl-shared/core/venue-matrix.md) | You are judging what this venue's audience will ask, or what its slot and format expect |
| [../ctrl-shared/core/verdicts-and-loops.md](../ctrl-shared/core/verdicts-and-loops.md) | You need the verdict enum, the effort tiers, the figure-iteration budget, or the promotion conditions for a spoken claim |
| [../ctrl-shared/core/review-rubrics.md](../ctrl-shared/core/review-rubrics.md) | You are judging whether a slide's claim exceeds the evidence behind it |

Forward references, owned by other skills. Use `ctrl-paper-craft` when the exposition itself needs
rewriting rather than condensing, `ctrl-experiment-suite` when a question exposes a missing
experiment, `ctrl-lit-radar` when a novelty question needs a documented search, and
`ctrl-pre-submission-review` when a talk exposes a concern that belongs in a review round.
