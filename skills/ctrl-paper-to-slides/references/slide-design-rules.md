# Slide design rules

What makes a slide readable from the back of a lecture hall, and what makes a deck look generated.
These rules are checkable against a rendered slide, which is the only place they matter.

## The one rule above the others

One message per slide. A slide that makes two points makes none, because the audience reads the
denser point and stops listening. If a slide needs the word "and" in its title, it is two slides.

## Layout

- Title in the top band, one line, at most 12 words. A two-line title pushes the content down and
  the second line is never read.
- Body content in the middle band, occupying at most two thirds of the slide height. The bottom
  third is where the audience's view of the projector is worst and where the presenter stands.
- One visual per slide, sized to be legible at 4 metres. Two figures side by side is acceptable
  only when the slide's single message is the comparison between them, and then the two panels are
  labelled `before` and `after` or `ours` and `baseline` in the figure itself.
- No slide number, logo, and footer competing with the content. One identifier in one corner.
- Margins of at least 5 percent of the slide width on every side. Content touching the edge looks
  cropped even when it is not.

## Legibility

The concrete thresholds below assume a 16:9 slide projected at 1920 by 1080, which is the common
case. A 4:3 or a lower-resolution projector raises every minimum.

| Element | Minimum | Comfortable |
|---|---|---|
| Body text | 18 pt | 22 to 24 pt |
| Slide title | 28 pt | 32 to 36 pt |
| Table text | 16 pt | 18 to 20 pt |
| Axis labels on a chart | 14 pt | 16 to 18 pt |
| Figure annotation | 12 pt | 14 pt |
| Line thickness on a plot | 2 pt | 2.5 to 3 pt |

A font size is measured after any scaling. A 12 pt label in a figure that is then scaled down to 60
percent on the slide renders at 7 pt and is unreadable. The check is the rendered size, not the
source size. This is the most common defect in decks built from publication figures.

Typeface discipline.

- One sans-serif family for the deck, one for the figures if the plotting style requires it. Never
  more than two families across the whole talk.
- Do not use a serif face for slide body text. Serifs survive print and die on a projector.
- No text in all capitals beyond an acronym. Capitalized words are read letter by letter.
- No italics for emphasis. Use weight, colour, or position.

## Contrast

- Dark text on a light background, or light text on a dark background. Never mid-tone on mid-tone.
- A contrast ratio of at least 4.5 to 1 for body text, and at least 3 to 1 for text above 24 pt.
  Word processing tools and image editors report this directly, and a screenshot check is enough.
- Never convey a distinction by colour alone. A red and green pair is invisible to roughly one in
  twelve men in the audience. Pair the colour with a marker shape, a line style, or a label.
- Semantic colour, used consistently. One colour for the proposed method across every figure and
  slide, one for the strongest baseline, and no others unless the figure genuinely needs them.
- A coloured background over more than one slide must not clash with the figure colours. Publication
  figures are usually drawn for a white page, and a dark template makes them unreadable.

## Charts

- Start the value axis at zero for a bar chart. A truncated axis on a bar chart is a
  misrepresentation, not a style choice. For a line chart where the range is narrow, a truncated
  axis is acceptable if the axis is labelled clearly and the truncation is stated.
- State the uncertainty. Error bars, a shaded band, or a stated dispersion, with the run count in
  the caption.
- Label the axes with the quantity and the unit. `RMSE (m)`, not `RMSE`, not `error`.
- State the metric convention in the axis label where it matters. `mAP` alone is an ambiguity, and
  the same applies on a slide as in the manuscript.
- Legend inside the plot area when there is room, in a corner the data does not occupy. A legend
  outside the plot shrinks the plot to make room for text the audience reads once.
- No chartjunk. No gradient fills, no drop shadows, no 3D bars, no bevels, no background gridlines
  heavier than the data.

## Tables on slides

- Reduce to the rows and columns the slide's message needs. A table reproduced in full from the
  paper is a backup slide, not a main-body slide.
- Highlight the row the audience should read, using bold or a single background tint. Do not bold
  every cell that is numerically largest.
- Keep the numeric precision consistent within a column, and drop digits the comparison does not
  need.
- Signpost the units in the header, not in every cell.
- If the table has more than 6 columns or 8 rows, it belongs in the backup section.

## What not to do

| Anti-pattern | Why it fails |
|---|---|
| Decorative 3D, bevels, drop shadows, perspective charts | The distortion changes the perceived values, and it dates the deck instantly |
| Clip art, stock icons, emoji, animated transitions | Consumes attention that belongs to the method |
| A slide that is a paragraph of prose | The audience reads it instead of listening, and they read it faster than the presenter speaks |
| Full sentences in bullets | A bullet is a claim fragment, not a sentence. If it needs a full stop, it is a script |
| A dark slide template with figures drawn for a white page | The figure becomes unreadable, and the palette clashes |
| A figure lifted from the paper and scaled down | Labels drop below the legibility minimum |
| An equation without a spoken explanation | The audience decodes symbols instead of following the argument |
| An animation that reveals a result already discussed | Breaks the pacing contract with the audience |
| A results slide with no comparison | A single number is not a result, it is a claim |
| The paper's abstract pasted into the conclusion slide | The conclusion is what the field now knows, not what the paper did |

## Reusing the paper's figures

Reuse is the default. The paper's figures have already been reviewed, and redrawing them costs time
that the talk preparation needs.

Reuse without modification when the figure is legible at the final rendered size, its labels are in
the language of the talk, its colour scheme works on the slide background, and it carries the single
message of that slide.

Regenerate with a plotting script when any of the following holds.

- Rendered label height falls below the legibility minimum at the slide's size.
- The palette clashes with the slide background, or relies on red and green alone.
- The figure is a multi-panel figure from the paper and the slide needs one panel.
- The figure contains annotation that the talk does not discuss, or omits annotation the talk needs.
- The figure is raster and will be scaled up beyond roughly 1.5 times its natural size.
- The venue requires different aspect ratios, such as a 4:3 projector or a poster panel.

When regenerating, keep the original as the reference and place the generating script beside the
figure, named after the figure, per
[artifact-contract.md](../../ctrl-shared/core/artifact-contract.md). The regenerated
figure must show the same data as the paper's figure. A slide figure showing a different number
from the manuscript is a reconciliation failure, not a design choice. This is the failure mode that
ends careers rather than talks.

## Language and audience

- English deck for an international venue, Chinese deck for a domestic venue, and never mixed
  within a slide.
- Chinese decks use the standard terms from
  [terminology-and-notation.md](../../ctrl-shared/core/terminology-and-notation.md), and do not
  carry English figure labels unless the figure is reused unchanged from an English paper, in which
  case the difference is stated in the notes.
- Acronyms are expanded at first use on the slide where they appear, not on the slide where the
  term was first needed. The audience joins late and remembers poorly.
- No more than three new terms per slide. Beyond three, the audience stops tracking the argument
  and starts decoding vocabulary.

## Final rendered check

Run this on the exported artifact, not on the Markdown outline. Visual items need a renderer or an
image export that you can actually inspect. Without one, report `rendered check: not performed`,
list the visual items left unchecked, and still run the items that can be verified from files (the
timing sum, ledger traceability, the revision recorded in the outline). Never report a visual PASS
for a deck nobody rendered.

```text
[ ] Every slide read at 50 percent zoom is still legible
[ ] No text overlaps a figure, a table, or another text box
[ ] No figure is cropped or stretched non-uniformly
[ ] Every font renders, with no substitution to a fallback face
[ ] Every equation renders, with no missing glyph or a placeholder box
[ ] Every colour used semantically is consistent across the deck
[ ] Every slide states its own single message in its title
[ ] The timing budget recomputed from the slides fits the slot
[ ] Every number on every slide traces to a G2-passed ledger row, or to the scoped source ledger as `reported`
[ ] The deck was built from the revision recorded in the outline (hash when computable)
```
