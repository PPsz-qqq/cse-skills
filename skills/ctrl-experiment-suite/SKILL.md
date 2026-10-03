---
name: ctrl-experiment-suite
description: >-
  Design, audit, and report experiments for 控制科学与工程 research across object detection
  (目标检测), multi-object tracking (目标跟踪), re-identification (重识别), cooperative navigation
  (协同导航), and filtering / state estimation (滤波). Use it to build the per-axis comparison
  protocol block that a delta requires, to fix a seed policy and a significance test, to design an
  ablation matrix that isolates each claimed component, to assemble a reproducibility package, and
  to fill results-table templates that survive review. Triggers include 实验设计, 消融实验,
  结果分析, 对比实验, 重复性实验, 误差棒, experiment design, ablation study, protocol matching,
  significance testing, error bars, reproducibility checklist, and results table formatting.
---

# CTRL experiment suite

Design, audit, and report experiments for the five `ctrl-*` axes so that every reported number is a
measurement with a named instrument and a stated uncertainty.

## Start here

Read [execution-contract.md](../ctrl-shared/core/execution-contract.md) first. Select the smallest
useful mode, confirm the inputs and available tools, and load only the references needed by the
current step. Use only the output sections relevant to this request; a diagnostic or draft is not
a gate-passed final artifact.

## Default stance

- A delta is a measurement claim. It needs a protocol block, a run count, and a dispersion before
  it can be written as an improvement. See `references/protocol-blocks.md`.
- Declare the protocol before running, not after. A protocol block written after the results
  exists is a description of what happened, and it cannot catch a comparison that was never fair.
- Prefer the smallest honest claim. `+1.2 mAP over 3 seeds, matched protocol` beats `achieves
  state-of-the-art` every time a reviewer recomputes it.
- Dispersion is part of the result, not an appendix. A mean without a spread is an incomplete
  measurement, and a best-of-`n` is not a mean.
- A null ablation is a result. Keep it in the table and discuss it; `ctrl-shared`
  `core/evidence-integrity.md` Rule 9 makes removing it a misconduct issue rather than a style
  choice.
- Simulation and field evidence are different tiers. Label them wherever the number appears,
  including table captions and the abstract.
- Every number traces to a run directory. If it does not, the value is `[MISSING: <need>]` and the
  claim is withdrawn from the manuscript.

## Workflow

1. **Identify the axes and claim type.** Read `ctrl-scope.md` if it exists. Record the primary axis
   and every secondary axis, and the claim type from the `G0` scope gate in
   `../ctrl-shared/core/gate-contract.md`. A mechanism claim needs an ablation chain; an empirical
   delta claim needs a matched protocol and a run count. If the claim type exceeds the evidence,
   emit the downgrade now rather than after the experiments are run.

2. **Emit one comparison protocol block per planned comparison.** Use the field registry in
   `references/protocol-blocks.md`, with the exact field names for the axis. In `det`, that means
   backbone, pretraining, input resolution, augmentation, training schedule, test-time
   augmentation, multi-scale inference, NMS policy, and evaluation split. In `track`, detector
   provenance, public or private detection, online or offline, and FPS with the exact GPU. In
   `reid`, backbone and pretraining, resolution and crop policy, re-ranking on or off,
   query/gallery construction, and single or multi query. In `cnav`, the node distribution proof,
   the communication model with delay and loss, and the centralized or distributed label. In
   `filt`, the Monte Carlo count and NEES or ANEES against its chi-square bounds. Write the blocks
   into `ctrl-protocol.md` and give each an id such as `P-det-1`.

3. **Fix the seed policy and the statistical treatment before the first run.** Choose
   `fixed-list`, `fixed-range`, or `derived`, apply the same list to every arm, and record the
   recommended minimum run count per axis. Write the dispersion statistic, the interval method,
   and the significance test into `ctrl-plan.md`. See `references/statistics-and-seeds.md`.

4. **Size the ablation matrix and pre-declare its decision rules.** Every claimed component gets a
   singleton arm under one protocol, every pair claimed complementary gets an interaction arm, and
   every arm carries a cost metric. Cap the arm count in `ctrl-plan.md`. See
   `references/ablation-matrix.md`.

5. **Run the per-axis checklist.** Walk the axis list in `references/axis-checklists.md` before,
   during, and after running. Anything that cannot be checked becomes a visible `[MISSING: ...]` in
   `ctrl-plan.md` rather than an implicit assumption.

6. **Capture the reproducibility package incrementally.** Each run directory gets its resolved
   config, exact command, environment record, seed record, full log, and raw metrics at the moment
   it runs. Reconstructing them afterwards is the failure mode that costs a headline number. See
   `references/reproducibility-package.md`.

7. **Reconcile the numbers against the artifacts.** Regenerate every table from the raw artifacts,
   check that aggregates reproduce from the per-item values, and check that the same quantity has
   one precision everywhere. Fill the results tables from `references/results-tables.md` and
   generate captions from the protocol blocks.

8. **Sweep the statistical traps.** Apply `references/statistical-traps.md` item by item. For any
   delta whose interval contains zero, apply the ladder in `references/statistics-and-seeds.md` and
   write the weaker true statement.

9. **Report gate status.** Emit the `G2` evidence-freeze block in the format from
   `../ctrl-shared/core/gate-contract.md`, listing the criteria checked, the artifact, the failing
   criterion, and the smallest clearing change. A failed `G2` has no waiver path.

10. **Hand the frozen numbers to the manuscript.** Every ledger row in `ctrl-claims.md` carries the
    protocol id and the comparability verdict. `ctrl-paper-craft` consumes those rows; it does not
    re-derive them from memory.

## Output format

```text
## Experiment design: <axis> <slug>

### Axis and claim
Primary axis: <det | track | reid | cnav | filt>
Secondary axes: <list, or none>
Claim type: <empirical delta | mechanism | theory | system | survey>
Falsifiable hypothesis: <one sentence>
Pre-declared refutation rule: <the result that would refute it>

### Protocol block
P-<axis>-<n>: <one line naming what is compared and where>
- Axis / dataset and split / metric definitions: <...>
- <normative per-axis fields, in the order given in references/protocol-blocks.md>
- Arms: <arm (tier, status) with per-arm deviations>
- Seeds and runs: <count, exact list, dispersion reported where>
- Hardware and environment: <device, framework, determinism settings>
- Comparability verdict: <comparable | partially comparable | not comparable, per arm pair>

### Runs
| Arm | Runs | Seeds | Primary metric | Dispersion | Interval | Cost metric |
|---|---|---|---|---|---|---|
| <arm> | <N> | <list> | <mean> | <stat> | <level, method> | <value, device> |

### Ablations
| Arm | <components> | Primary metric | Delta vs baseline | Interval | Interaction |
|---|---|---|---|---|---|

### Statistical treatment
Dispersion statistic: <...>
Interval method and level: <...>
Significance test and correction family: <...>
Deltas inside the noise: <value, interval, and the weaker statement used>

### Reproducibility
Run directory: exp/<axis>-<slug>-<run-id>/
Code commit: <hash and dirty status> | Config: <path> | Data: <version, split id, checksum>
Command: <the exact invocation> | Environment: <device, driver, library versions>

### Gate status
Gate G2 evidence freeze: PASS | FAIL | BLOCKED
- Checked: <criteria evaluated>
- Artifact: ctrl-claims.md, ctrl-protocol.md
- Failing criterion: <one line, when not PASS>
- Smallest clearing change: <one line, when not PASS>
- Waiver: none

### Open gaps
[MISSING: <what is needed and how to obtain it>]
[UNVERIFIED: <the item and why it could not be verified>]
```

## Red lines

- Never report a delta without a complete protocol block for its axis, and never report a
  `not comparable` pair as a delta anywhere, including the abstract.
- Never compare arms on different seed lists, different run counts, or different detection files.
- Never present a single-seed result as a stable performance claim. Label it `single seed`.
- Never tune a covariance, a threshold, or a configuration on the test split and then report the
  test split as held out.
- Never time the proposed method and the baseline on different hardware, at different batch sizes,
  or with different timed regions, and never present such a comparison as an efficiency result.
- Never attribute a gain to a component without a singleton arm under one protocol. If the arm is
  missing, downgrade the claim to empirical delta or add the arm.
- Never delete a losing arm, a losing sequence, or a null ablation to make a table read better.
- Never fill a table cell by interpolation, estimation, or memory. A visible `[MISSING]` is a
  correct output.
- Never retune `Q_k` or `R_k` after seeing the consistency result and report the tuned filter's
  consistency as evidence of consistency.
- Never claim distributed operation for a method that requires a central node or global state.

## Related files

| File | Open when |
|---|---|
| [references/protocol-blocks.md](references/protocol-blocks.md) | You are writing a protocol block, need the exact per-axis field names, or must decide a comparability verdict |
| [references/statistics-and-seeds.md](references/statistics-and-seeds.md) | You are fixing a seed policy, choosing a dispersion statistic, running a significance test, or a delta is inside the noise |
| [references/ablation-matrix.md](references/ablation-matrix.md) | You are designing the ablation chain, computing interaction effects, or a component failed to help |
| [references/reproducibility-package.md](references/reproducibility-package.md) | You are assembling the package, naming run directories, or running the reproduce-a-headline-number test |
| [references/axis-checklists.md](references/axis-checklists.md) | You are starting, running, or reporting experiments on a specific axis |
| [references/results-tables.md](references/results-tables.md) | You are filling a results, ablation, interaction, or scaling table, or writing its caption |
| [references/statistical-traps.md](references/statistical-traps.md) | You are about to freeze results, or a reviewer questioned the statistical treatment |

Cross-skill. Read [evidence-integrity.md](../ctrl-shared/core/evidence-integrity.md) for the ten
integrity rules and the comparability break table,
[gate-contract.md](../ctrl-shared/core/gate-contract.md) for the `G0` to `G3` gates and the axis
addenda, [artifact-contract.md](../ctrl-shared/core/artifact-contract.md) for artifact names and
locations, [terminology-and-notation.md](../ctrl-shared/core/terminology-and-notation.md) for metric
conventions and symbol conventions, and
[verdicts-and-loops.md](../ctrl-shared/core/verdicts-and-loops.md) for claim-promotion conditions
and the experiment tuning loop budget. Planning upstream belongs to ctrl-idea-forge, the literature
search behind a novelty claim belongs to ctrl-lit-radar, manuscript writing belongs to
ctrl-paper-craft, and the review of a frozen result belongs to ctrl-pre-submission-review.
