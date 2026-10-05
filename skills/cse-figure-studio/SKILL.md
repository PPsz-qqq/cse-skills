---
name: cse-figure-studio
description: >-
  Use when drawing, restyling or auditing figures for a paper on detection, tracking, re-ID,
  cooperative navigation or filtering (目标检测, 跟踪, 重识别, 协同导航, 滤波): 画图, 作图, 论文配图,
  科研绘图, 框架图, 流程图, 网络结构图, 控制框图, 结果曲线, 消融柱状图, figure, plot. Builds diagrams
  and data plots at final column width with IEEE, Elsevier, Springer or 自动化学报 themes, lints text
  size and collisions, stamps placeholder data DEMO, exports PDF/SVG/PNG/EPS, never plots invented
  numbers.
---

# CSE figure studio

Draw the figures of a detection, tracking, re-ID, cooperative-navigation or filtering paper at their
printed size, so that what the reviewer sees is exactly what was checked: legible type, one accent
for the proposed method, honest uncertainty, and a number on every mark that traces to a result file.

## Start here

Read [execution-contract.md](../cse-shared/core/execution-contract.md) first. Select the smallest
useful mode: restyling one supplied figure is `local-edit`, auditing a draft's figures is
`diagnostic`, planning a paper's figure set is `design`, and producing figures that carry final
results is `finalize`. Then check the machine:

```text
python scripts/render.py --doctor
```

It reports whether matplotlib, a headless Chrome or Edge (SVG to PDF/PNG), Pillow (previews), an EPS
converter and the Latin and Chinese fonts are present. Promise only the formats it confirms.

## Default stance

- A figure is a display of measurements. Every plotted value comes from a file the claim ledger or
  the user points to. A value that does not exist is `[MISSING: ...]` in the plan, never a plausible
  curve.
- Templates ship with placeholder data registered through `pp.mark_demo()` or `pp.demo_rng()`.
  While it is registered, every export is stamped DEMO DATA. Remove the registration only together
  with the placeholder data, never to clean up a picture.
- Draw at the final width. Pick the width key or the measured `\columnwidth` first; font sizes are
  then the sizes that print, and the lint can judge them.
- One message per figure, one accent colour for "ours", muted greys for baselines, and the same
  colour for the same object in every figure of the paper.
- Regenerate data figures deterministically from data with a script kept beside the figure. Never
  let an image model redraw a plot, and never edit a value inside a drawing program.
- The default effort tier is `standard` for one figure and `thorough` for a full figure set.

## Workflow

1. **Fix the figure's job.** Write one sentence the figure must make obvious, the claim rows it
   displays (`C3`, `C5`), the panels, and the figure type. Choose the nearest template from the
   table below or from [references/figure-catalog.md](references/figure-catalog.md).

2. **Check the evidence behind every mark.** For each series record the source file, the tier
   (`measured`, `reported`, `assumed`), the run count and the dispersion statistic. Comparisons in
   one panel must share a protocol, timings must share hardware, and a highlighted best setting must
   come from validation data. If a source is missing, stop and name it; offer the template with its
   DEMO stamp as a layout preview only.

3. **Fix venue, width and language.** Theme `default`, `ieee`, `elsevier`, `springer` or `aas`; width
   key or measured width; `--lang zh` for Chinese labels. Facts and their sources are in
   [references/print-and-venue-specs.md](references/print-and-venue-specs.md); re-check the venue's
   current guidelines before a submission.

4. **Copy the template into the project.** Put the script at `fig/fig<n>-<slug>.py` in the user's
   project, never inside this skill. Replace the demo block with loading code, delete the
   `mark_demo` call with it, and keep labels in the paper's notation. Use `pp.tr(en, zh)` for any
   label that must exist in both languages.

5. **Render and lint.** Run the script. Fix every lint warning: text below the theme minimum,
   overlapping or clipped text, hairlines. `python scripts/gallery.py` runs the whole template set
   the same way and fails on any warning.

6. **Look at the result.** Inspect the PNG at print size, then
   `python scripts/render.py fig.png --preview` for the greyscale and colour-vision-deficiency
   sheet, and `python scripts/render.py fig.pdf` for page size and embedded fonts. Judge it against
   [references/design-rules.md](references/design-rules.md). Without a renderer, report
   `visual check: not performed`.

7. **Write the caption from the protocol.** State what is plotted, the dataset and split, the run
   count and what bars or bands show, protocol labels the axis needs, and simulation or field. Use
   the caption obligations in
   [results-tables.md](../cse-experiment-suite/references/results-tables.md).

8. **Export and record.** Write `fig/fig<n>-<slug>.pdf` (plus `svg`, `png`, `eps` as the venue
   needs) beside its script and data, per
   [artifact-contract.md](../cse-shared/core/artifact-contract.md). Stop after 3 iteration rounds
   (the figure-iteration budget in [verdicts-and-loops.md](../cse-shared/core/verdicts-and-loops.md))
   and report the outcome.

## Templates

| No. | Template | Use it for |
|---|---|---|
| 01 | framework overview | method pipeline with the proposed stage accented |
| 02 | algorithm flowchart | filter or algorithm steps, decisions, loops |
| 03 | network architecture | encoder-decoder or backbone with tensor shapes |
| 04 | module detail | one block (attention, fusion) with operators and residuals |
| 05 | control block diagram | feedback loop with summing junctions and an estimator |
| 06 | cooperative system | multi-agent scene and per-agent processing chain |
| 07 | timing diagram | multi-rate sensors, latency, out-of-sequence updates |
| 08 | taxonomy tree | related-work families for a survey or introduction |
| 09 | paradigm comparison | teaser: conventional pipeline against the proposed one |
| 10 | curves with seed bands | metric against epoch or time, mean and range over runs |
| 11 | ablation bars | variants against metrics, error bars, gain over baseline |
| 12 | accuracy-speed trade-off | scatter on a log speed axis with Pareto front |
| 13 | sensitivity heatmap | two hyperparameters, selected setting outlined |
| 14 | raincloud distributions | per-sequence or per-run errors of several methods |
| 15 | filter consistency | ANEES with chi-square bounds, RMSE with CRLB |
| 16 | trajectories with covariance | ground truth, estimates, 95 % ellipses, anchors |
| 17 | precision-recall curves | PR curves with iso-F1 contours and AP in the legend |
| 18 | tracking strip | frames with identity-coloured boxes, history, a failure |
| 19 | re-ID ranking | query against the top-10 gallery of baseline and ours |

Templates 01 to 09 use `scripts/figkit.py` (SVG built in points, rendered by a headless browser);
10 to 19 use `scripts/pubplot.py` (matplotlib). `scripts/demo_scene.py` draws the illustrated stand-in
images of 18 and 19. The API of both engines is in [references/api.md](references/api.md).

## Output format

Report every figure with a build report.

```text
Figure build report
- Figure: fig/fig4-anees.pdf (+ svg, png), generator fig/fig4-anees.py, data exp/mc-200/anees.csv
- Job: <the one sentence>; claim rows: C4, C5
- Venue and size: <IEEE single column, 88.9 mm, theme ieee, lang en>
- Data: <measured, from the files above | supplied, unverified | DEMO, stamped, not a result>
- Lint: <0 warnings | the remaining warnings>
- Visual check: <PNG at print size and grey/CVD preview inspected | not performed: no renderer>
- Fonts: <all embedded, no Type 3 | not checked>
- Iteration: <round n of 3, converged | budget exhausted with residual defects | stopped by user>
- Not done: <EPS (no converter), Chinese version, or none>
```

## Red lines

- Never plot a value without a source, never draw a baseline curve "to look reasonable", and never
  remove the DEMO stamp while placeholder data remains.
- Never start a bar axis above zero. For a zoomed comparison, use points with intervals on a
  labelled range.
- Never show an error bar or band without naming its statistic and run count in the caption.
- Never put arms with different protocols, hardware or detectors in one panel without labelling the
  difference on the figure.
- Never highlight a setting selected on test data, and never redraw a figure to hide a losing case.
- Never use colour alone to separate meanings: pair it with a marker, a line style or a glyph.
  Never use rainbow or jet colour maps.
- Never claim a render, a visual check or an exported format that did not happen.
- Never let an arrow or annotation assert a claim that the text and the evidence do not support.
- Never write figures, scratch output or caches inside the installed skill.

## Related files

| File | Open when |
|---|---|
| [references/figure-catalog.md](references/figure-catalog.md) | You are choosing a template, or need what a template expects and what its caption must state |
| [references/design-rules.md](references/design-rules.md) | You are judging or improving how a figure looks: typography, colour, layout, per-type rules, the final checklist |
| [references/print-and-venue-specs.md](references/print-and-venue-specs.md) | You need widths, type sizes, resolution, formats or font rules of a venue, with sources and check dates |
| [references/api.md](references/api.md) | You are building or modifying a figure with figkit, pubplot, render, gallery or demo_scene |
| [../cse-shared/core/evidence-integrity.md](../cse-shared/core/evidence-integrity.md) | You are checking that plotted values are sourced, tier-labelled and protocol-matched |
| [../cse-shared/core/terminology-and-notation.md](../cse-shared/core/terminology-and-notation.md) | You need metric conventions, symbols or bilingual terms for axis labels and legends |
| [../cse-shared/core/artifact-contract.md](../cse-shared/core/artifact-contract.md) | You are naming figure files or deciding what to keep beside a figure |
| [../cse-shared/core/verdicts-and-loops.md](../cse-shared/core/verdicts-and-loops.md) | You need the figure-iteration budget, effort tiers or verdict words |
| [../cse-experiment-suite/references/results-tables.md](../cse-experiment-suite/references/results-tables.md) | You are writing a caption, which carries the same obligations as a results table |

Forward references, owned by other skills. Use `cse-experiment-suite` when a figure needs a
statistic, a protocol block or more runs; `cse-paper-craft` when captions and the text must be
reconciled; `cse-paper-to-slides` when a figure is resized for a talk; and
`cse-pre-submission-review` for a referee-side figure audit.
