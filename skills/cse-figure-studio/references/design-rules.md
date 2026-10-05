# Design rules

What makes a figure in this pack look finished, and what makes it trustworthy. The two overlap: most
figures that look amateur do so because they hide the comparison, not because of a colour choice.
The engines already apply these rules by default; this file says why, gives the numbers, and ends
with the check to run on the rendered figure.

## The look in one paragraph

White ground, near-black ink (`#23272E`), muted grey for everything secondary, one saturated blue
(`#0077BB`) for the proposed method and nothing else, type at the size it prints, thin axes without a
box, a light grid on the value axis only, direct labels instead of legends when there is room, and
generous but even spacing. A reader should find "ours" in under a second and the comparison it wins
or loses in under five.

## Typography

| Element | default | ieee | elsevier | springer | aas |
|---|---|---|---|---|---|
| axis label | 8 | 9.5 | 7.5 | 8.5 | 8 |
| tick label, in-plot annotation | 7 | 9 | 7 | 8 | 8 |
| legend | 7 | 9 | 7 | 8 | 8 |
| panel title | 8 bold | 9.5 bold | 7.5 bold | 8.5 bold | 8 bold |
| smallest allowed text object | 6 | 8 | 6 | 8 | 8 |

- Use `pp.size('annot')`, `pp.size('legend')` and the other keys instead of numbers, so a figure
  stays legal when the venue changes. The lint reports anything smaller than the theme minimum.
- One family per figure: Arial (Helvetica) for the sans themes, Times New Roman with 宋体 for `aas`.
  Bold only for the proposed method, panel labels and diagram titles.
- Variables italic, operators and units upright, a true minus sign: write `$\hat{x}_{k|k-1}$`,
  `$\mathrm{softmax}$`, `RMSE (m)`. Keep symbols identical to the manuscript, per
  [terminology-and-notation.md](../../cse-shared/core/terminology-and-notation.md).
- Axis labels carry quantity and unit, `Position RMSE (m)`; follow the venue if it prescribes
  `时间 / s` instead. State log scales in the label when the reader could miss them.
- Sentence case for labels, no full stops, no title above a plot: the caption is the title.

## Colour

| Role | Colours | Where defined |
|---|---|---|
| proposed method | `OURS` `#0077BB` | pubplot, and figkit tone `blue` |
| baselines | `BASELINES`: grey `#7F8790`, rose, sand, teal, wine, olive | pubplot |
| categories with no emphasis | `CYCLE`: Okabe-Ito blue, orange, green, vermilion, purple, sky | pubplot |
| identities (tracks, agents) | `IDS`: Okabe-Ito without yellow and black | pubplot |
| correct / wrong | `GOOD` `#009E73` / `BAD` `#D55E00`, always with a glyph | pubplot |
| sequential maps | `pp.blues()`, `pp.iridescent()`, viridis | pubplot |
| diverging maps (meaningful midpoint only) | `pp.sunset()` | pubplot |
| diagram tones | blue (new), teal (cues, data), gray (standard), sand (decisions), orange (alternatives) | figkit `TONES` |

- One accent, and only for "ours". Graded neutral greys order the other variants (11).
- The same object keeps the same colour in every figure, every slide and every panel.
- Never rainbow or jet. Never red against green as the only cue. Pair colour with a marker, a dash
  pattern or a glyph; `pp.series_style(i, gray=True)` gives series that survive greyscale print.
- Text on a coloured fill must reach a 4.5:1 contrast ratio: `pp.text_color_for` picks black or
  white for heatmap cells and `pp.label_fill` darkens tab fills until white text passes.
- Check the rendered PNG with `render.py fig.png --preview`, which shows greyscale, deuteranopia and
  protanopia side by side.

## Lines, markers and fills

| Element | Weight |
|---|---|
| data line | 1.1 to 1.2 pt; the proposed method 1.6 pt and drawn last |
| axes, ticks | 0.6 pt, ticks outward, 3 pt long |
| grid | 0.5 pt, `#E6E8EB`, value axis only |
| error bar | 0.7 pt with 2 pt caps |
| reference line (bound, threshold) | 0.7 to 0.9 pt, dashed or dotted, grey |
| marker | 4 pt; hollow for start or capture, filled for end or arrival |
| band | the line colour at 18 % opacity, or `band(..., solid=True)` for EPS |

Nothing thinner than 0.3 pt (the lint flags it); Springer asks for at least 0.1 mm.

## Layout and space

- Fix the width first, then the aspect: about 0.62 to 0.75 of the width for a single-column plot.
  Never resize a finished figure in LaTeX; regenerate it at the right width.
- Constrained layout aligns axes; image grids are placed by hand in inches (`pp.canvas`,
  `pp.place`) so every image has the same size and the gaps are equal.
- Legends go above the axes in one or two rows, or inside an empty corner, never over data. Prefer
  direct labels: `pp.end_label` for curves, `pp.label_points` for scatter points (it moves each
  label to a free position around its marker).
- Panel labels `(a)`, `(b)` in bold at the top-left, outside the plotting area; panels that share an
  axis share its range and its ticks.
- In diagrams: everything on the 0.75 pt grid, equal box heights within a row, orthogonal arrows
  with rounded corners, containers drawn first and behind, one accent box, labels that fit their box
  (the figkit lint reports overflow and overlaps).

## Rules per figure type

| Type | Rules |
|---|---|
| framework, module, network | left to right or bottom to top, never both; one accent; tensor shapes on one aligned row; no decorative 3D beyond feature cuboids |
| flowchart | standard symbols; decisions label every exit; loops return on the left; one column |
| control block diagram | forward path on top, feedback below; signs at every summing junction; italic signal symbols on every edge |
| curves | direct labels; band or error statistic named in the plot or caption; x axis starts where data starts |
| bars | start at zero; neighbouring variants separated by thin white edges; value labels only where they carry the message (the gain) |
| scatter | marker area, not radius, encodes size; the Pareto front or threshold line in grey; ours with a halo |
| heatmap | square-ish cells with white gaps; sequential map unless a true midpoint exists; the selected cell outlined in a contrasting colour and its value bold |
| distribution | show every unit as a point; density reflected at a hard bound such as zero; methods on the y axis so names stay horizontal |
| consistency | log scale for ANEES; the bound band and the expected value drawn; bounds per time step, not pooled |
| trajectory | equal axis scaling; ground truth thin dark dashed; ellipses with a stated probability (`cov_ellipse(prob=0.95)`; a "2 sigma" ellipse holds 86 %, not 95 %) |
| precision-recall | square axes from 0 to 1; iso-F1 contours faint; AP in the legend |
| image strips | identical size and crop per column; boxes 1.3 pt; label tabs with readable contrast; a small chip for frame or camera; the failure case shown |
| retrieval | query first behind a separator; correct and wrong by colour plus glyph; similarity under every crop; the same gallery in every row |

## Integrity rules that are also design rules

- A bar that does not start at zero misstates its ratio. Zoom with points and intervals instead.
- Every band and error bar names its statistic and run count, in the plot or the caption.
- Arms in one panel share protocol, hardware and detector, or the difference is labelled on the
  figure. Speed comparisons are timed on one machine.
- The highlighted setting in a sensitivity plot was selected on validation data.
- Placeholder data stays stamped DEMO DATA. The stamp leaves with the placeholder, never alone.
- A figure regenerated for slides shows the same data as the paper figure.
- No 3D bars, shadows, gradients behind data, or clip art. A drawn icon is acceptable in a diagram
  when it identifies a platform (UAV, ground robot, anchor), not as decoration.

## Chinese figures

- Run data templates with `--lang zh`; labels written as `pp.tr('Time step $k$', '时间步 $k$')`
  switch with it. `pp.tr` also wraps Chinese next to math so that it renders: matplotlib draws every
  character of a label containing `$...$` with the math fonts, which have no CJK glyphs.
- `aas` uses Times New Roman with 宋体 at 8 pt. For other Chinese journals use the venue's stated
  face; without one, a sans theme falls back to Microsoft YaHei or Noto Sans SC.
- Do not mix languages inside one figure. Bilingual figure captions, where a journal requires them,
  belong in the manuscript, not in the figure.

## Final check on the rendered figure

Run it on the exported file. Without a renderer, report `visual check: not performed` and list the
items left open.

```text
[ ] The lint printed no warning (size, overlap, clipping, hairline) and no DEMO notice for a result
[ ] At 100 % zoom on the PNG, every label reads at its printed size and nothing touches anything
[ ] "Ours" is the only accent and is found first; colours mean the same thing as in other figures
[ ] Greyscale and colour-vision previews still separate every series
[ ] Every plotted value traces to a file; the caption states statistic, run count and protocol
[ ] Bars start at zero; log scales are labelled; the highlighted setting came from validation
[ ] The PDF has the venue's page size, one page, all fonts embedded and no Type 3 font
[ ] Script, data and figure sit together under fig/, and the build report is written
```
