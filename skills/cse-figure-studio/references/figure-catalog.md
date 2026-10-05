# Figure catalog

The 19 templates: what each one shows, where it fits on the five axes, what to replace, and what its
caption must state. Every template is a runnable script with the same options.

```text
python templates/<file>.py --out <dir> [--formats svg,pdf,png] [--dpi 600] [--theme ieee] [--lang zh]
```

`--lang` exists on the data templates (10 to 19). Copy a template into the project as
`fig/fig<n>-<slug>.py` before editing it, and keep the copy beside its output. The rendered set is in
the repository at `docs/assets/figure-studio/` (`gallery-diagrams.png`, `gallery-plots.png`,
`gallery-qualitative.png`).

## Diagrams: 01 to 09

Built with [figkit.py](../scripts/figkit.py) in points at final size, saved as SVG and rendered to PDF
and PNG by a headless Chrome or Edge. Diagrams hold no measured values, but they must depict the
method that was actually run: no component that does not exist, no arrow that asserts an effect the
evidence does not show.

| No. | File | Default width | Shows | Fits |
|---|---|---|---|---|
| 01 | `01_framework.py` | IEEE double | input frames, three stage containers, cue modules, the proposed module accented with a cost-matrix glyph, recurrent state as a dashed loop, legend row | method overview on any axis |
| 02 | `02_flowchart.py` | IEEE single | terminators, I/O parallelograms, processes, decision diamonds with labelled exits, a proposed side branch, a loop-back edge labelled along the edge | filter and estimator procedures, tracking logic |
| 03 | `03_network.py` | IEEE double | feature cuboids whose height follows resolution, encoder and decoder hues, a proposed bottleneck, nested skip arcs, one aligned row of shape labels | det, reid and track backbones |
| 04 | `04_module.py` | IEEE single | one block drawn bottom to top: projections, product and sum operators, residual paths routed outside and labelled, a repetition chip | the single component the paper adds |
| 05 | `05_control_loop.py` | Elsevier 1.5 column | forward path left to right, feedback below, summing junctions with signs, take-off dots, disturbance and noise inputs, the estimator accented | filt, guidance and control |
| 06 | `06_cooperative_system.py` | IEEE double | (a) agents, anchors, GNSS-denied hatch, communication and ranging links; (b) one agent's chain with neighbour messages in and out | cnav, any communication graph |
| 07 | `07_timing.py` | IEEE double | one lane per sensor at its rate, capture and arrival joined by a latency bar, filter events, an out-of-sequence correction | multi-rate fusion, delayed measurements |
| 08 | `08_taxonomy.py` | IEEE double | root, one hue per family, leaf cards with name, detail and a citation slot | related work, surveys |
| 09 | `09_paradigm_comparison.py` | IEEE single | conventional pipeline above, the proposed one below in identical geometry, one feedback arc that carries the idea | Fig. 1 teaser |

Replace labels, keep the structure that makes the figure read: one accent for what is new, grey
for standard parts, aligned rows and columns, orthogonal arrows, legend or row titles instead of
colour-only meaning. Labels accept math markup such as `$\hat{x}_{k|k-1}$`. In the taxonomy, the
`[refs]` slot takes real citation numbers; never leave invented references in a figure.

Caption obligations: what is new and what is standard, the data that flows between blocks, and for
06 which agent computes what and which quantities are exchanged.

## Data plots: 10 to 17

Built with [pubplot.py](../scripts/pubplot.py) on matplotlib at final width. Each template keeps its
placeholder data in one marked block (`load_runs()`, an array, or a small simulation) registered with
`pp.mark_demo()` or `pp.demo_rng()`; replace the block with loading code and delete the registration
with it.

| No. | File | Shows | Replace with | Caption must state |
|---|---|---|---|---|
| 10 | `10_curves_band.py` | mean curve and min-max band over runs per method, direct labels at the line ends, ours drawn last and thicker | runs x steps array per method from the logged metrics | the band statistic, run count, split |
| 11 | `11_ablation_bars.py` | variants as bars per metric from zero, error bars, the absolute gain over the baseline above the full model, legend above | the ablation table's mean and std at the same precision | protocol block, statistic, run count, that gains are absolute points |
| 12 | `12_tradeoff_scatter.py` | log speed axis, marker area by parameter count, baseline Pareto front, real-time line, ours with a halo, labels placed without collisions | FPS, accuracy and size measured on one machine | device, batch size, precision, timed region |
| 13 | `13_heatmap.py` | two hyperparameters on a single-hue blue scale, white cell gaps, values in cells with readable text, the selected setting outlined | the validation grid and the setting the tuning protocol selected | validation split, metric, how the setting was selected |
| 14 | `14_distribution.py` | raincloud: density reflected at zero, slim box, every per-unit value as a point | per-sequence or per-run values | the unit (sequence, run, scene) and the count |
| 15 | `15_consistency.py` | (a) ANEES per time step on a log axis with the 95 % interval and the expected value; (b) RMSE with the CRLB of the matched model; legend above | NEES and RMSE of your Monte Carlo runs | `N`, `n_x`, confidence, per-step aggregation, assumptions |
| 16 | `16_trajectories.py` | equal axes, ground truth dashed, estimates with start and end marks, 95 % covariance ellipses, anchors, the denied region named in place | estimates and 2x2 position covariances | that the run is illustrative, the ellipse probability |
| 17 | `17_pr_curves.py` | square axes, iso-F1 contours, AP inside the legend, ours accented | precision-recall points exported by the evaluator | evaluator, IoU threshold, interpolation, split |

## Qualitative figures: 18 and 19

Also pubplot. They place axes by hand in inches (`pp.canvas`, `pp.place`) so that every image has
the same size. Their stand-in images are drawn illustrations from
[demo_scene.py](../scripts/demo_scene.py): obviously not data, and stamped.

| No. | File | Shows | Replace with | Caption must state |
|---|---|---|---|---|
| 18 | `18_detection_boxes.py` | three frames with frame chips, boxes coloured by track identity with label tabs, fading track history, an unmatched ground-truth box | your frames and your tracker output for the same frame indices | sequence, frame indices, detector, public or private detection, score threshold |
| 19 | `19_reid_retrieval.py` | the query and the top-10 gallery for baseline and ours; correct and wrong marked by colour plus a check or cross; similarity under each crop | your crops and the ranked gallery from the evaluator | dataset, query ID, single or multi query, re-ranking, same-camera exclusion |

For detection only, colour 18's boxes by class and drop the history. For people, check the dataset
licence and the venue's policy on faces before showing real crops.

## Which template for which figure

The standard figures of each axis, from
[axis-writing-guides.md](../../cse-paper-craft/references/axis-writing-guides.md), map to templates
as follows.

| Axis | Figure a reviewer expects | Template |
|---|---|---|
| `det` | mechanism diagram | 01, 03 or 04 |
| `det` | qualitative detections with a failure panel | 18, coloured by class, no history |
| `det` | key ablation; `AP_S` / `AP_M` / `AP_L` breakdown | 11 |
| `det` | precision-recall; speed against accuracy | 17; 12 |
| `track` | pipeline with the association step accented | 01 or 09 |
| `track` | sequence excerpt with an identity switch marked | 18 |
| `track` | `AssA` against `DetA`; throughput | 12 with the axes changed; 12 |
| `reid` | feature and training scheme | 01 or 04 |
| `reid` | `CMC` curve | 10 with rank on the x axis |
| `reid` | top-k retrieval with the true match marked | 19 |
| `cnav` | scenario and communication topology | 06 |
| `cnav` | per-node error against time with the operational limit | 10 plus a horizontal limit line |
| `cnav` | error against communication cost; scaling over `N` | 12 with the axes changed; 10 with the valid range shaded |
| `cnav` | trajectories with covariance | 16 |
| `filt` | estimation architecture and update order | 02, 05 or 07 |
| `filt` | `ANEES` with chi-square bounds; `RMSE` against the `CRLB` | 15 |
| `filt` | illustrative trajectory with covariance envelope | 16 |
| `filt` | error distributions over Monte Carlo runs | 14 |

When no template fits, build the figure with the same engine and the rules in
[design-rules.md](design-rules.md); the API is in [api.md](api.md).
