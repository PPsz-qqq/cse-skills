# Abstract template with a worked structure

The abstract is written last and checked first. It is the only part that most readers will read, so
every number in it must be the most defensible number in the paper.

## The six slots

A working abstract for this field has six slots. A slot may share a sentence with a neighbour, but
no slot may be missing.

| Slot | Job | Length |
|---|---|---|
| P problem | the task, in the axis community's terms | 1 sentence |
| G gap | the specific thing current methods do not do or do not report | 1 to 2 sentences |
| I idea | the mechanism, in one sentence a reader could repeat | 1 sentence |
| M method | what was actually built, concretely | 1 to 2 sentences |
| E evidence | the numbers with their protocol and run count | 1 to 2 sentences |
| B boundary | the condition under which the claim holds | 1 sentence |

The order is P, G, I, M, E, B. Putting E before I produces a leaderboard abstract that reviewers
in class A discount.

## Skeleton

```text
<P> <Task> is <what it is used for>, and <the operational consequence that makes it hard>.

<G> Recent <line of work> improves <what it improves>, but <the specific limitation>, and
<the measurement that is never reported>.

<I> We observe that <the insight>, which suggests <the mechanism>.

<M> Building on this, we present <method name, expanded at first use>, which <the mechanism in
concrete terms>, and <a second sentence naming the components the ablations test>.

<E> On <dataset and split>, under <the axis-critical protocol labels>, <method> reaches
<value> <units> (mean over <N> runs, <dispersion statistic> <value>), against <baseline> at
<value> under the same protocol, and <the second dataset or setting with its own numbers>.
<Where a mechanism is claimed, one sentence naming the ablation result that supports it.>

<B> The improvement holds for <the boundary conditions>; <the case where the method does not
hold, stated plainly>.
```

## Worked structure, `det`

Filled with placeholders, since no measured value exists in this template. Every `<...>` must be
replaced from a ledger row or the sentence removed.

```text
<P> Small-object detection in aerial imagery is limited by the scale range within a single scene,
and by the spatial correlation between neighbouring tiles that makes a random split optimistic.

<G> Recent multi-scale fusion methods improve average precision on natural-image benchmarks, but
their gains are reported on splits built without a spatial separation rule, and the per-size-bucket
behaviour that the mechanism is supposed to fix is rarely reported.

<I> We observe that <the specific observation>, which suggests <the mechanism>.

<M> We present <method>, which <mechanism>, and we report its behaviour per object-size bucket.

<E> On <dataset, version, split id> with <spatial separation rule>, at <resolution> input, under
<protocol id>, <method> reaches <AP> <units> (mean over <N> seeds, <dispersion statistic>), against
<baseline> at <AP> under the same protocol, an absolute difference of <delta>; the ablation with
<component> removed reaches <AP>, isolating <the component's contribution>.

<B> The result holds for <sensor and region>; on <the failing condition> the method loses to
<baseline> by <delta>.
```

## Worked structure, `filt`

```text
<P> <Estimator class> provides <the guarantee> only when <the assumption>, and in <the operational
setting> that assumption is <how it fails>.

<G> Existing <line> reports accuracy by RMSE without a consistency check, so a filter whose
covariance is wrong can appear superior, and the bound that would reveal it is not reported.

<I> We observe that <the observation>, which suggests <the mechanism>.

<M> We present <estimator>, which <mechanism>, and we evaluate it for both accuracy and consistency.

<E> Over <N = ...> Monte Carlo runs on <the trajectory protocol>, <estimator> reaches
<RMSE> <units> with <ANEES> against chi-square bounds taken at <N * T * n_x> degrees of freedom and
divided by <N * T>, while <baseline> reaches <RMSE> with <ANEES>, which <is inside | exceeds> those
bounds; <the ablation with the component removed> reaches <RMSE> and <ANEES>. State `n_x`, the
confidence level, and the degrees of freedom used, per
[terminology-and-notation.md](../../ctrl-shared/core/terminology-and-notation.md).

<B> Consistency holds for <the noise regime and linearization region>; outside <the condition> the
estimator <the observed behaviour>.
```

## Worked structure, `cnav`

```text
<P> Cooperative navigation in <GNSS-denied setting> requires <what it requires>, and the
communication that makes it work is <the constrained resource>.

<G> Distributed estimators are often evaluated with an ideal channel, and the messages they
exchange are not priced, so a method that improves accuracy by moving more data is reported as an
algorithmic gain.

<I> We observe that <the observation>, which suggests <the mechanism>.

<M> We present <method>, a <distributed | hybrid> estimator in which each agent <what it computes
and what it exchanges>, with <bytes per agent per step>.

<E> Over <N = ...> scenario runs with <which parameters varied>, under <delay and loss model>,
<method> reaches <RMSE in 2D, frame stated> at the worst node with <bytes per agent per step>,
against <baseline> at <RMSE> with <bytes>; the centralized reference reaches <RMSE> and is reported
as a bound, not as a distributed competitor.

<B> The result holds for <N range, topology class, and noise regime>; beyond <the boundary> the
benefit <disappears or reverses>.
```

`reid` and `track` follow the same six slots, with their protocol labels in E: for `reid` the
resolution and crop policy, the re-ranking status, and the query mode; for `track` the detector
provenance, public or private detection, and online or offline.

## Number discipline in the abstract

```text
[ ] Every number has a ledger row whose comparability verdict is comparable
[ ] Every number states its units and its dataset
[ ] Every delta states absolute or relative
[ ] Every stochastic number states its run count and dispersion, or is labeled single seed
[ ] The precision matches the tables exactly
[ ] No number appears that the body does not contain
[ ] No number is rounded differently from the body
[ ] The strongest claim uses the weakest wording the evidence permits
```

A number that cannot satisfy all eight lines is removed from the abstract, even when it is the
best-looking one in the paper. The abstract drives the `G3` check that every claim in it is
supported by a `G2`-passed ledger row.

## Wording that must not appear

| Forbidden | Why | Replacement |
|---|---|---|
| `state-of-the-art` | unsupported without a matched comparison, and dated on arrival | the value with its protocol, and the named baseline |
| `significantly better` | `significantly` is a statistical term | `higher by <delta>, <interval> excluding zero` or the null statement |
| `the first to` | requires a two-cycle search record | the narrow scoped claim, or the measurement gap |
| `novel framework` | `novel` is a reviewer's verdict, not the authors' | name what is new, mechanically |
| `extensive experiments` | a claim about effort, not evidence | name the datasets and the run count |
| `effectively handles` | unfalsifiable | the measured behaviour and the condition |
| `real-world` | a field claim needs field data | `in simulation` or the platform, site, and conditions |
| `robust` | needs a perturbation class | `under <named corruption or outlier rate>` |
| `achieves comparable performance` | usually means it lost | the value, the interval, and `no measurable difference` |
| `to the best of our knowledge` | launders an unrun search | run the search, or state the gap in reported evidence |

## Self-check before the abstract is frozen

```text
[ ] All six slots present, in order P, G, I, M, E, B
[ ] The idea sentence is repeatable by a reader who skipped the method section
[ ] Every number satisfies the eight number-discipline lines
[ ] Every mechanism sentence has an ablation behind it
[ ] The boundary sentence names the condition and the losing case
[ ] No forbidden wording from the table above
[ ] The abstract was written after the experiments were frozen, not before
[ ] The abstract was re-checked after the last edit to any table
```
