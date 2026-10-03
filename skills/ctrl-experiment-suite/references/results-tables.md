# Results-table templates

Table shapes that survive review in this field. Each template lists the columns, the caption
obligations, and the defects that make it fail `G2`. Copy the shape, fill from the run artifacts,
and generate the caption from the protocol block rather than writing it from memory.

## Universal caption obligations

Every results table caption states, at minimum: the dataset and split, the metric conventions, the
run count and seed policy, the dispersion statistic, the axis-critical protocol labels, and the
tier status of every non-measured row. If a caption line cannot be filled, the table is not ready.

Do not put a number in a caption that does not appear in the table, and do not state a superlative
in a caption that the table does not support under a matched protocol.

## Table 1 shape, main comparison

One row per arm, one column per metric, protocol labels in dedicated columns so they cannot be
forgotten.

```text
| Method | Tier | Protocol labels | Metric A | Metric B | Cost | Notes |
|--------|------|-----------------|----------|----------|------|-------|
| Baseline X (reported) | reported | <its own protocol> | <value> | <value> | <value> | not comparable, <difference> |
| Baseline Y (re-implemented) | measured | <our protocol> | <mean> +- <sd> | <mean> +- <sd> | <value> | 3 seeds |
| Ours (component off) | measured | <our protocol> | <mean> +- <sd> | <mean> +- <sd> | <value> | 3 seeds |
| Ours | measured | <our protocol> | <mean> +- <sd> | <mean> +- <sd> | <value> | 3 seeds |
```

Rules.

- The `Protocol labels` column carries the labels that travel with the number for the axis.
  `det` uses resolution and TTA, `track` uses online or offline and public or private, `reid` uses
  single-query or multi-query and re-ranking on or off, `cnav` uses distributed or centralized and
  the message budget, `filt` uses`N` and the covariance policy.
- Bold a value only when it is the best under a matched protocol. If the best-looking number is
  `not comparable`, it stays unbolded and the reason is in `Notes`.
- Every `+-` value names its statistic and run count in the caption.
- The cost column is measured on one device for every row, or it is marked `reported, other
  hardware` and excluded from the efficiency argument.

Caption skeleton.

```text
Table <n>. <what is compared> on <dataset, split>.
<Metric A> is <convention>. <Metric B> is <convention>.
Values are <mean over N seeds, seeds listed in the protocol block> and <+- is the sample standard
deviation>. Rows marked <not comparable> use <the difference>; see protocol <P-axis-n>.
Our arms share one protocol: <the three or four axis-critical labels>.
```

## Table 2 shape, per-axis specialization

### `det`

```text
| Method | Backbone | Resolution | TTA | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | Params | GFLOPs | FPS |
```

Caption must state the AP convention and IoU range, the resolution for every row, the TTA applied,
and the device for FPS. A resolution or TTA difference between rows is a `Notes` entry and a
mis-comparability warning.

### `track`

```text
| Tracker | Detector | Det. protocol | Setting | HOTA | DetA | AssA | MOTA | IDF1 | IDSW | Frag | FPS | GPU |
```

Caption must state the detector checkpoint, public or private, online or offline, the evaluation
tool, and the GPU with batch size and timed region for FPS.

### `reid`

```text
| Method | Backbone | Test size | Re-ranking | Query mode | mAP | Rank-1 | Rank-5 | mINP |
```

Caption must state the query and gallery construction, the query count, whether re-ranking is on,
and the evaluation script version. Re-ranking status is never left to the text.

### `cnav`

```text
| Method | Architecture | Exchange | Bytes/node/step | Topology | Delay | Loss | N | RMSE (m) | Worst-node RMSE | 95th pct | Bound exceedance |
```

Caption must state the frame and dimension of the error, the number of scenario runs, which
parameters varied, and whether the result is simulation or field.

### `filt`

```text
| Estimator | Q, R policy | Init. error | N | RMSE (pos) | RMSE (att) | ANEES | chi2 lower | chi2 upper | Verdict |
```

Caption states `n_x`, confidence level, aggregation, distribution/independence assumptions and
numeric bounds. Default: ANEES at each k over N independent runs, df `N*n_x`, quantiles divided by N.
A time-averaged scalar needs justified temporal independence or correlation-aware calibration, not
unconditional df `N*T*n_x`. Distinguish pointwise from simultaneous bounds and state pre-declaration.

## Table 3 shape, ablation

```text
| Arm | Component A | Component B | Component C | Primary metric | Cost | Delta vs baseline | Interval |
```

Rules.

- One singleton arm per claimed component. See `references/ablation-matrix.md`.
- The `Delta vs baseline` column is relative to the baseline row, not to the previous row.
- The `Interval` column carries the interval on the delta. `not computed` is a visible gap, not a
  blank.
- Null components stay in the table with their interval containing zero.
- State in the caption that every arm ran under one protocol block, and name it.

## Table 4 shape, interaction

```text
| Configuration | A | B | Metric | Delta from A-off | Delta from B-off | Interaction | Interval |
```

State the interaction definition, `delta(A | B on) minus delta(A | B off)`, in the caption. Three
rows are the minimum: `A only`, `B only`, `A and B`.

## Table 5 shape, scaling and robustness

Use for `N` scaling in `cnav`, resolution or corruption sweeps in `det`, and noise
mis-specification in `filt`.

```text
| Setting | Ours | Baseline Y | Delta | Interval | Note |
```

Rules.

- One row per setting value, in increasing order, with the setting value in the first column.
- State which parameters were held fixed while the setting varied.
- Where a sweep was run for one arm and not the other, the table is a single-arm study. Label it
  and do not compute a delta column.
- For a robustness sweep, name the perturbation class, since `robust` without one is a marketing
  word (`ctrl-shared` `core/terminology-and-notation.md`).

## Formatting and precision rules

- One precision per quantity type across all tables. Report a metric at the precision the
  benchmark resolves, and keep extra digits only where the uncertainty justifies them.
- Units in the header or in the caption, not repeated in every cell.
- Values carry no unit and no percent sign inside the cell, so that a table can be parsed.
- Every improvement expressed as a percentage states absolute or relative, in the caption.
- A plus-minus value uses one symbol throughout the manuscript, and it is defined once.
- Significance marks, if used at all, are defined in the caption with the test and the correction
  family. A mark with no test is decoration.
- Bold, italics, and color each mean one thing and only one thing across the whole manuscript.
  Define the convention in the first table caption and keep it.

## Self-check before a table is frozen

```text
[ ] Every value in the table resolves to a run directory under exp/
[ ] The caption carries the protocol labels the axis requires
[ ] The run count, seed policy, and dispersion statistic are in the caption
[ ] Every non-measured row states reported or re-implemented, with the published value shown
[ ] Every not-comparable row is marked, and the difference is named
[ ] Bold marks only a matched-protocol best
[ ] Precision matches the other tables and the abstract
[ ] Units and conventions are unambiguous in the header or the caption
[ ] The table has been regenerated from the raw artifacts after the last code change
[ ] No cell was filled by estimation, interpolation, or memory
```
