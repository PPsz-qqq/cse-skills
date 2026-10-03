# Evidence and integrity rules

The rules below are the pack's answer to the failure modes that actually occur in detection,
tracking, re-identification, cooperative navigation, and filtering papers. They are ordered by
how often they cause a rejection or a post-publication correction.

## Rule 1. No fabricated evidence

Every number, figure, table cell, citation, dataset statistic, hardware specification, and
baseline result must trace to something that exists. Permitted sources: a file the user
produced, a log or console output the user can point at, a released result table from a cited
source read at first hand, or a value the user explicitly supplies.

Forbidden without exception: inventing a citation; inventing a baseline number "from the
literature"; rounding a placeholder into a plausible value; describing a figure that was never
generated; stating a hardware configuration that was not used; asserting that an experiment
"showed" something that was never run; completing a table by interpolation and presenting it
as measured.

When an element is unavailable, write `[MISSING: <what is needed and how to obtain it>]`.
A visible gap is a correct output. A plausible fiction is not.

## Rule 2. Tier labeling

Label every quantitative statement with its tier.

| Tier | Meaning | Citation obligation |
|---|---|---|
| `measured` | produced by a run the user performed | state the artifact path, seed count, and hardware |
| `reported` | stated by a citable source | cite it and state whether you read the primary source |
| `assumed` | a working assumption or a design target | state the assumption and its sensitivity |

A value copied from another paper into a comparison table stays `reported` and carries protocol
differences and a per-pair comparability verdict. A re-implemented baseline is `measured` with
`Provenance: re-implemented`, not a fourth tier. Record setting (`benchmark` / `simulation` /
`field`) and verification status separately. A measured simulation is not field evidence.
A user-supplied value can be quoted as supplied; without checking the underlying artifact, mark
its verification `UNVERIFIED` and do not grant an independently verified G2 PASS.

## Rule 3. Protocol-matched comparison

A performance delta is a measurement claim. Before reporting any delta, fill the comparison
protocol block for the active axis from `core/gate-contract.md` and confirm the arms match.

Unmatched arms must be presented in one of three honest ways: as a separate row with the
difference declared; with the difference corrected by a control run you performed (for example
re-training the baseline under your protocol); or omitted.

Match controlled conditions, not the intervention being tested. An architecture, covariance
estimator or NMS change may be the declared treatment; record it and choose the relevant equal-
data, compute or deployment-cost estimand. It is not automatically a nuisance confound. For a
component-attribution claim isolate that treatment; for a whole-system benchmark disclose resource
trade-offs. The numeric thresholds below are heuristic red flags, not safe harbours below them:
any unaccounted protocol difference may confound a claimed gain.

### Calibration thresholds for common unfair comparisons

These are the differences that most often invalidate a delta in practice. Treat any of them as
requiring an explicit justification or a control run.

| Axis | Difference that breaks comparability |
|---|---|
| `det` | input resolution above 1.3x; extra pretraining data; test-time augmentation on one arm only; different epoch budget beyond 1.5x; COCO `val` for one arm against `test-dev` for another; different NMS policy |
| `track` | private detections for one arm against public detections for another; different detector checkpoint; offline post-processing on one arm; FPS measured on different GPUs or with different batch sizes |
| `reid` | re-ranking on for one arm only; different test resolution or crop policy; multi-query against single-query; external unlabeled data for one arm; different backbone capacity class |
| `cnav` | centralized solution presented as distributed; perfect communication for one arm; different ranging noise model; simulation against field data without a declared gap |
| `filt` | per-filter hand tuning for the proposed method only; different Monte Carlo counts; different initialization error; noise covariance mismatch applied to the baseline only |

## Rule 4. Number reconciliation

Before freezing results, reconcile:

- the abstract, the results tables, the figure captions, and the conclusion must agree on every
  shared number, at the same precision and with the same units;
- any average must be reproducible from the per-item values shown, or the aggregation rule must
  be stated;
- any best-in-table value must be bolded only if it is actually the best under a matched
  protocol;
- any improvement expressed in percent must state whether it is absolute or relative.

A number that appears at two precisions, or a superlative contradicted by the paper's own
table, is a blocking integrity failure, not a copy-editing issue.

## Rule 5. Stochastic results

For any result with a random component (initialization, data order, sampling, seed, Monte Carlo
draw), state: the number of runs, the seed policy (fixed list, range, or single seed), and the
dispersion (standard deviation, confidence interval, or min-max). Report single-seed results as
single-seed results. In filtering, a single trajectory is not a statistical result; in
detection and tracking, a single training run is not a stable accuracy claim.

Recommended minimums unless the venue or the user's field convention sets another: 3 seeds for
detection and re-identification training runs, 3 to 5 for tracking, at least 100 Monte Carlo
runs for filtering accuracy and consistency claims, and at least 30 runs for stochastic
cooperative-navigation scenarios.

## Rule 6. Ablation sufficiency

A contribution claim requires an ablation that isolates it. The ablation chain must show: the
baseline, the baseline plus the single component, and the full method, all under one protocol.
Report the delta per component and the interaction where components are claimed to be
complementary. An ablation run at a different budget from the main result is not an ablation,
it is a second experiment.

State what the ablation does *not* establish. A component that improves the metric but whose
mechanism remains unexplained must be reported as an empirical finding, not as a validated
mechanism.

## Rule 7. Provenance and reproducibility

Record, for each result: code version or commit, configuration file, dataset version and split
identifier, random seeds, hardware and driver or library versions where the number depends on
them, and the command that produced the artifact. A headline number must be reproducible by the
authors on their own hardware from the recorded material. If it is not reproducible, say so and
report it as a single observation.

## Rule 8. Reported versus re-implemented baselines

State for every baseline whether the number is `reported` (copied) or `re-implemented`
(reproduced by the authors). Re-implemented baselines that underperform their published value
must be reported with both numbers and the gap. Publishing a lowered baseline number without
noting the published value is a comparison-integrity failure.

## Rule 9. Negative and null results

Keep them. A component that does not help, a scenario where the method loses, and a hypothesis
that the data refutes are all publishable content and all mandatory content in the limitations
section. Do not remove a losing case from the evaluation set after seeing the result. Do not
redefine a metric after seeing that the original metric did not favor the method; if a metric
is changed, report both.

## Rule 10. Source honesty

When citing, distinguish: read in full, read in abstract only, or known only by title. Never
attribute a specific numeric result to a source you have not read at first hand; cite the
secondary source or mark it `[UNVERIFIED]`. For venue requirements and author guidelines, the
official call for papers wins over any summary, including this pack's own
`core/venue-matrix.md`.

## Quick integrity audit

Run this before any freeze. Answer each item `pass`, `fail`, or `not applicable` with the
evidence path.

```text
[ ] Every quantitative claim has a ledger row with a resolvable source
[ ] No invented citation, number, figure, hardware fact, or experiment
[ ] Every tier label is correct and every reported delta is protocol-matched
[ ] Abstract, tables, captions, and conclusion reconcile
[ ] Stochastic results state runs, seed policy, and dispersion
[ ] Ablation chain isolates each claimed component under one protocol
[ ] Provenance recorded for every headline number
[ ] Baseline reported-versus-re-implemented status is stated
[ ] Negative results retained and limitations written
[ ] Percentages state absolute or relative
[ ] No metric redefinition after seeing results
[ ] Every unverified item is visibly marked
```
