# Statistical treatment, seeds, and dispersion

Detection, tracking, re-identification, cooperative navigation, and filtering all produce numbers
with a random component, from initialization, data order, sampling, Monte Carlo draws, scenario
generation, or the environment. This file states how to size the experiment, how to report it, and
what to do when an effect is uncertain. Judge the interval/test on the **difference**, not the
ratio of the mean difference to either arm's standard deviation. A small paired effect can be
precisely estimated; a large noisy effect can remain unresolved. Statistical uncertainty and
practical importance are separate questions.

## Seed policy

Fix the seed policy before the first run and record it in `ctrl-plan.md`. Three policies are
acceptable and one is not.

| Policy | Definition | When acceptable | Reporting obligation |
|---|---|---|---|
| `fixed-list` | an explicit list of seeds, for example `0,1,2`, applied to every arm | default for all comparisons | print the list, and per-seed values in the results table |
| `fixed-range` | a contiguous range, for example `0..4`, applied to every arm | when the list is long and the run is cheap | print the range and the count |
| `derived` | seeds generated from one master seed by a recorded rule | when the campaign is scripted | print the master seed and the derivation rule |
| `single-seed` | one run | only for a pilot, a smoke test, or a figure | write `single seed` next to every number it produces |

Two rules hold under all policies. Every arm uses the same seed list, because a different seed list
per arm turns a method comparison into a seed comparison. The seed is applied at every stochastic
site the framework exposes, including data loader worker seeding, the augmentation pipeline,
dropout, and any scenario or Monte Carlo generator, because a fixed top-level seed with unseeded
workers is not a fixed seed. Recommended minimum runs per axis, from `ctrl-shared`
`core/evidence-integrity.md` Rule 5 and to be raised when a venue or the field convention requires
it, are 3 training seeds for `det` and `reid`, 3 to 5 runs for `track`, 30 scenario runs for `cnav`,
and 100 Monte Carlo runs for `filt` accuracy and consistency claims.

Reporting a single-seed result as if it were typical is the failure the policy exists to prevent. If
only one run exists, write the number, label it `single seed`, and state that no dispersion is
available. Do not estimate a standard deviation from one run and do not borrow a dispersion figure
from another experiment.
## Dispersion

Report a mean with a dispersion for every aggregate. Choose one statistic per quantity type and keep
it across the manuscript.

| Statistic | Use when | Note |
|---|---|---|
| standard deviation over runs | the quantity is roughly symmetric and the run count is at least 3 | state whether it is the sample or population form; the difference matters at 3 runs |
| standard error of the mean | the claim is about the mean itself | do not present it where a reader will read it as spread over runs |
| min and max | the run count is very small | honest and unambiguous at 2 runs |
| confidence interval | the venue expects an interval, or the comparison is marginal | state the level and the method |
| median and interquartile range | the metric is heavy tailed, for example a loss rate or a failure count | preferred for outlier-dominated quantities |

Write the dispersion next to the mean in the results table, not only in the text. `78.4 mAP` is
incomplete; `78.4 +- 0.6 mAP over 3 seeds, seeds 0,1,2` is a measurement. Never report a best-of-run
number as the method's performance, because best-of-`n` rises with `n` and is not comparable between
arms with different run counts. If a best number must appear, label it `best of <n> runs` and keep
the mean beside it.

## Significance testing

A significance test answers one question. Given the observed spread, how often would a difference at
least this large appear if the two arms were the same? Report the test, its assumptions, and the
effect size together, never the p-value alone. Prefer a paired comparison over the seed list plus a
bootstrap over evaluation units, and state both. Report the effect size in the metric's own units,
for example `+1.2 mAP`, beside any p-value, because a tiny p-value on a 0.05 mAP difference is a
statement about sample size rather than usefulness. Correct for multiple comparisons when testing
many arms or ablations at once, and state whether the reported interval is per-comparison or
family-wise. Do not test after selecting the best of many configurations and report the test as if
the configuration had been pre-declared, because selection invalidates the nominal level.

| Situation | Appropriate test | Assumption to state |
|---|---|---|
| 3 or more paired runs, same seeds, per-run values available | paired test over the seed pairs | the pairing is real, that is both arms saw the same seed and the same data order |
| 3 or more unpaired runs per arm | rank-based test such as Mann-Whitney | observations are independent and the metric distribution is not assumed normal |
| per-image or per-sequence scores available | bootstrap over the evaluation units | the resampling unit is the unit of independence, images or sequences, not detections |
| large per-unit sample, for example per-query reid scores | bootstrap confidence interval on the difference | state the number of resamples and the resampling unit |
| comparison of a curve, for example a CMC or an FPPI curve | bootstrap over the whole curve, or compare at pre-declared operating points | do not compare curves by eye where they separate most |

## Confidence intervals

Prefer an interval to a bare point estimate for any headline number. State the level, the method,
and the sample it was computed from.

| Method | Use when | Requirement |
|---|---|---|
| bootstrap percentile | per-unit scores exist, the metric is not a simple mean | at least 1000 resamples, and the resampling unit stated |
| normal approximation over seeds | at least 5 seeds and an approximately symmetric metric | state the sample standard deviation and whether the t or z factor was used |
| exact or binomial interval | the quantity is a rate, for example identity switch rate or detection rate per frame | state the interval family |
| chi-square interval for ANEES | filtering consistency | see the `filt` section below |

For `cnav` and `filt`, where the quantity is often an error distribution, report the interval of the
error statistic and the empirical error distribution's quantiles rather than only its mean. A method
with the same mean RMSE and a much heavier 95th percentile is a different method for a navigation
system. This is also the most common reporting decision in the five axes and the one most often made
dishonestly, so apply the ladder below in order and stop at the first rung that applies.

1. **Compute the interval on the difference.** If it contains zero, superiority is not established
   at the stated level and sample size. Report the observed delta and interval, and write
   `the comparison is inconclusive at this sample size` rather than claiming a win.
2. **Do not turn a null test into equivalence.** Do not write `equivalent`, `on par` or `no effect`
   merely because zero is inside the interval. Equivalence/non-inferiority requires a pre-declared
   practical margin and an appropriate test/interval. Lower compute cost can be reported if measured,
   but cannot make an unresolved accuracy comparison equivalent.
3. **If the design is underpowered, say so instead of claiming a win.** Report the observed
   difference, the dispersion, and the run count, and state that the experiment cannot separate the
   arms at this run count. That sentence is a result.
4. **If the difference is detectable but practically irrelevant, say both.** A `+0.03 mAP`
   difference with 20 seeds is detectable and meaningless. Report the value and state that it is
   below the precision at which the benchmark discriminates.
5. **Do not repeatedly sample until significance.** Additional runs require a pre-specified
   sequential design with its error control, or a new confirmatory phase with a fresh freeze and
   independent data. Record any post-hoc extension as exploratory, extend arms symmetrically, and
   do not treat declaring an extension after a null result as correcting optional stopping.
6. **Keep the null result in the paper.** `ctrl-shared` `core/evidence-integrity.md` Rule 9 makes
   this mandatory. A component that does not help belongs in the ablation table and in the
   limitations section, with the same status as a component that does.

A tie reported as a tie is a stronger contribution than a tie reported as a win, because a reviewer
who recomputes the second one rejects the paper.

## Axis-specific statistical notes

### `det`

- AP is not an average of independent per-image AP values. Resample independent images/scenes or
  whole sequences with their predictions and ground truth, then recompute the official AP metric.
- mAP averages a fixed benchmark class set. Bootstrap over classes only for a declared population-of-
  classes estimand, not as a substitute for dataset uncertainty on that fixed set. Report training-
  seed uncertainty separately; do not silently change the estimand when estimating an interval.
- Small-object AP has far higher variance than large-object AP, so do not compare `AP_S` across arms
  without dispersion.
- When an evaluation server returns only a scalar, dispersion across seeds is the only available
  spread. State that repetition on the server was not possible.

### `track`

- The bootstrap unit is the sequence and there are typically few sequences, so the interval is
  coarse. Report it as coarse and rely on the seed spread as the second component.
- Report `DetA` and `AssA` dispersion separately. An association claim supported by an `AssA` gain
  inside the noise is not supported.
- `IDSW` and `Frag` are counts and typically overdispersed. Use the median and interquartile range,
  or a bootstrap interval, rather than a normal interval.
- FPS is a timing measurement. Report the repeat count, whether warm-up was discarded, and the
  spread. A single timing is not a throughput result.

### `reid`

- Rank-1 is a rate over queries, so its interval is binomial or a bootstrap over queries. The query
  count is usually large enough that this interval is narrow and misleading, while the dominant
  uncertainty is the training seed. Report both.
- mAP and Rank-1 move together but not proportionally. A gain in mAP without Rank-1 changed the
  ranking inside the top list; state that instead of claiming a general gain.
- Re-ranking changes both metrics substantially and is not a method component. Never compare an arm
  with re-ranking against an arm without it.
- State the query count when reporting a gain on a small dataset, because a Rank-1 difference of one
  point can be a handful of queries.

### `cnav`

- Scenario runs are the sample. Vary the initial error, the topology or its realization, the ranging
  noise realization, and the delay and loss draws, and report which of them varied.
- Report per-node RMSE and the fleet aggregate separately, because a mean over nodes hides one agent
  diverging, which is the failure that matters for a formation or a swarm.
- Report the tail of the error distribution, at minimum the 95th percentile of position error and
  the fraction of runs exceeding the declared operational bound.
- A convergence claim needs a distribution over runs of the convergence time or the consensus
  residual, not one trajectory.
- Communication cost is part of the result. Report bytes per agent per step beside the error, and
  hold it fixed when comparing two methods, or state both axes of the trade.

### `filt`

- A chi-square reference for `NEES` assumes zero-mean Gaussian errors with the recorded covariance;
  name approximations for nonlinear/non-Gaussian estimators and the assessed state dimension.
- Default to `ANEES_k` over `N` independent runs **at one time step**: reference degrees of freedom
  `N*n_x`, chi-square quantiles divided by `N`. Record the numeric bounds and confidence level.
  Consecutive time steps are generally correlated. Use `N*T*n_x` divided by `N*T` only with justified
  independence of all pooled samples; otherwise use correlation-aware calibration or whole-trajectory
  resampling. The normative assumptions and formula are in
  [terminology-and-notation.md](../../ctrl-shared/core/terminology-and-notation.md).
- Above-upper-bound values indicate overconfident covariance, and below-lower-bound values indicate
  conservative covariance under the reference assumptions. Isolated pointwise violations are expected
  at the test's nominal rate; do not pronounce a filter inconsistent from one crossing. Report the
  violation fraction, pattern, uncertainty and any simultaneous-test treatment.
- Never retune `Q_k` or `R_k` after seeing `ANEES` and then report the tuned filter's consistency as
  evidence of consistency. That is fitting the test to the result.
- Report RMSE and consistency together, because a filter can have low RMSE and be inconsistent,
  meaning its uncertainty estimate is wrong even though its point estimate happens to be good.
- For a particle filter, state the particle count, whether it was chosen before or after seeing
  results, and the state dimension, since consistency degrades with dimension. A `CRLB` or posterior
  `CRLB` is a bound, not a baseline, so plot it as a bound and never enter it in a baseline
  comparison table as an arm.

## Reporting template

```text
Quantity: <metric name with its convention>
Value: <mean> +- <dispersion> <units>
Runs: <N>, seed policy <fixed-list | fixed-range | derived | single-seed>, seeds <list or rule>
Dispersion: <statistic used, and whether sample or population>
Interval: <level and method, or "none, N too small">
Comparison: <arm> vs <arm>, difference <value> <units>, interval <low, high>, test <name>
Selection: <how this configuration was chosen, and whether it was pre-declared>
Boundary: <dataset, split, scenario, hardware>
```

If any line cannot be filled, the quantity is not ready to be reported as a result. It may still
appear as a pilot number with an explicit `pilot, single seed` label, and it must record the numbers
themselves rather than a conclusion, so a later reader can recompute the verdict.