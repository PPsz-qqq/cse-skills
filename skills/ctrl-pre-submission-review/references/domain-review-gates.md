# Domain review gates

The axis-specific evidence addenda a reviewer applies on top of the shared G2 criteria, plus the
comparison-protocol fields a review must be able to reconstruct. The normative statements live in
[gate-contract.md](../../ctrl-shared/core/gate-contract.md) and
[evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md). This file is the reviewer's
working form of them.

A gate is passed by an artifact, not by an assertion. When a gate cannot be evaluated because an
input is missing, the verdict is `BLOCKED`, not `FAIL`, and the review names the missing input and
how to obtain it.

## How to run the gate check inside a review

1. Identify the active axes. Run the addendum block for the primary axis and for every secondary
   axis whose evidence the paper uses.
2. For each field, mark `present`, `absent`, or `not applicable`, and record where in the
   manuscript or in the artifacts the field was found.
3. An `absent` field that carries a reported delta becomes a concern with an evidence pointer to
   the missing field's expected location. Do not invent the value.
4. Report the gate status with the standard block and exactly the six verdicts from
   [verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md). `PASS` needs every
   applicable required field present and checked. `WARN` is a met criterion with a non-blocking
   defect, never an integrity failure. `FAIL` needs a specific evaluated unmet criterion. `BLOCKED`
   needs a named missing input or artifact. `ERROR` means the check itself could not run.
   `NOT_APPLICABLE` needs the reason the criterion does not apply to this claim type.
5. A failed G2 is blocking and has no waiver path. The remedy is to remove the claim or produce the
   evidence, so the review's resolution test names which of the two is expected.

## Protocol field names

The field names in the addenda below are the normative registry names from
[protocol-blocks.md](../../ctrl-experiment-suite/references/protocol-blocks.md), which states that
they must not be renamed because a renamed field cannot be reconciled later. A protocol block in
the manuscript that carries a different name for one of these fields is a reconciliation defect in
the manuscript, not a second vocabulary. Each addendum lists the registry fields for its axis, then
the reviewer-side checks that the registry does not define.

## det addendum

| Field | What the reviewer must be able to find | If absent |
|---|---|---|
| `Backbone` | architecture, capacity class, and parameter count, per arm | a delta over a stronger backbone is uninterpretable, Major or Blocking |
| `Pretraining` | corpus, size, and whether it overlaps the evaluation set | overlap with the test distribution is an integrity concern, Blocking |
| `Input resolution` | train and test resolution and the resize policy, per arm | a gap above 1.3x breaks comparability, Blocking when it carries the delta |
| `Augmentation` | the full recipe, and whether it is identical across arms | one arm with extra augmentation is a training-recipe delta, Major |
| `Training schedule` | epochs, batch size, optimizer, and learning rate policy, per arm | a gap beyond 1.5x requires justification, Major |
| `Test-time augmentation` | the transforms applied at inference, or `none`, per arm | on one arm only is an unfair comparison, Blocking when it carries the delta |
| `Multi-scale inference` | single-scale, or the explicit scale list and fusion rule | silent multi-scale on the proposed arm inflates AP, Major |
| `NMS policy` | greedy, soft, or learned, with the IoU and score thresholds and the max detections | a differing policy changes AP with no method difference, Major |
| `Evaluation split` | local split id, or the evaluation server, per arm | `val` for one arm and `test-dev` for another is not comparable, Blocking |

Reviewer-side checks beyond the registry. The metric averaging convention, since `AP` alone is
ambiguous. The `AP_S` / `AP_M` / `AP_L` breakdown when a scale claim is made. The `FPPI` convention
and the evaluation subset for a pedestrian detection result.

## track addendum

| Field | What the reviewer must be able to find | If absent |
|---|---|---|
| `Detector provenance` | detector name, checkpoint identity, training set, and confidence threshold | the number is not reproducible, Blocking |
| `Detection protocol` | `public` or `private`, named per arm | Blocking, and it must travel with every tracking number |
| `Setting` | `online` or `offline`, and every step that uses future frames, per arm | offline post-processing on one arm invalidates the delta, Blocking |
| `FPS` | what the number includes, whether detection time is included, batch size, and the sequence | a throughput number without its scope is not a measurement, Major |
| `FPS GPU` | exact part, memory, power mode, and driver | FPS across different GPUs is a comparability break, Major |
| `Association and motion model` | the association cost, the motion model, and any learned component | a tracker swap presented as a module delta, Blocking when association is the contribution |
| `Tracking metrics` | `HOTA` with `DetA` and `AssA` separated, or `MOTA` with `IDF1`, `IDSW`, `Frag`, `MT`, `ML` | a single `MOTA` hides a detection gain as an association gain, Major |

Reviewer-side checks beyond the registry. The IoU matching threshold used for identity assignment.
The evaluation tooling version, since implementations differ. The definition of any difficult
subset, such as occlusion or crowded scenes, where a subset claim is made. Whether the experiment
holding the detector constant exists, since without it the association contribution is unattributed
and Blocking. Whether parameters were tuned per sequence or globally, since per-sequence tuning
reported as a general method is a comparison-integrity failure.

## reid addendum

| Field | What the reviewer must be able to find | If absent |
|---|---|---|
| `Backbone and pretraining` | architecture, capacity class, pretraining dataset, and whether extra data was used, per arm | external data on one arm only is a comparison-integrity failure, Blocking |
| `Input resolution and crop policy` | height, width, ratio convention, and the crop or padding rule, per arm | Blocking when it carries the delta |
| `Re-ranking` | `on` or `off`, per arm, stated in the table itself | Blocking, because re-ranking alone can dominate the reported gain |
| `Query/gallery construction` | the official split, or the explicit rule used, including camera overlap and identity disjointness | a self-built split that leaks training identities inflates both metrics, Major |
| `Query mode` | `single-query` or `multi-query`, consistently across arms | Blocking |
| `Evaluation data` | the official test split, or a validation split carved from train | tuning on test and reporting test is test-set tuning, Blocking |
| `Reid metrics` | `mAP`, `Rank-1`, `Rank-5`, and whether the official evaluation code version was used | a hand-rolled `mAP` is not comparable to a published one, Major |

Reviewer-side checks beyond the registry. Whether `mINP` is reported, and with which convention.
Whether any target-domain images were used for adaptation, and if so on which arms.

## cnav addendum

| Field | What the reviewer must be able to find | If absent |
|---|---|---|
| `Node distribution proof` | which node computes what, listed per node, and the artifact that shows it | a centralized solution described as distributed is Blocking |
| `Exchange` | the quantity each message carries, its size, and the message rate | an unstated exchange lets a central-equivalent method look distributed, Major, Blocking when communication efficiency is the contribution |
| `Central node or global state` | `none`, or the named node and the state it holds | a hidden global state invalidates the distribution claim, Blocking |
| `Communication model` | channel type, topology and whether it is time-varying, and the update schedule | Major, Blocking when a baseline is evaluated under a harsher model |
| `Delay` | the delay model, its parameters, and whether it applies to every arm | zero delay on the proposed arm only is a comparability break, Major |
| `Loss` | the packet loss or dropout model, its parameter, and the timeout policy | an ideal channel for one arm is a comparability break, Major |
| `Computation architecture` | `centralized`, `distributed`, or `hybrid`, and the convergence rounds per step | the label must match `Node distribution proof`, not the paper's aspiration, Blocking |
| `Scenario generation` | node count `N`, deployment region, initial error distribution, and the number of runs | fewer than 30 runs cannot support a stochastic scenario claim, Major |
| `Position metrics` | `RMSE` or `CEP`, 2D or 3D, per node and fleet-aggregate, with the frame | an unspecified frame or dimension makes the error value meaningless, Major |
| `Ranging model` | line-of-sight or non-line-of-sight, noise distribution, outlier rate, and whether all arms share it | a different ranging model per arm is a comparability break, Blocking when it carries the delta |

Reviewer-side checks beyond the registry. The observability or connectivity condition the result
requires, which is Blocking for a convergence or observability claim. What was simulated against
what was measured, where presenting simulation as field data is an integrity failure. The platform,
sensors, calibration procedure, and onboard runtime where a hardware claim is made.

## filt addendum

| Field | What the reviewer must be able to find | If absent |
|---|---|---|
| `Monte Carlo count` | the number of runs `N`, and whether every arm used the same `N` | a different `N` per arm is a comparability break, Blocking for a consistency claim |
| `Consistency metric` | `NEES` or `ANEES`, the estimator that produced `P_k`, and the degrees of freedom `n_x` | Blocking for a consistency claim |
| `Chi-square bounds` | the quantiles used, the confidence level, and whether the test is one-sided or two-sided | a bound chosen after seeing the result is not a test, Major |
| `Bound used for comparison` | the numeric bounds actually plotted, the run count `N`, the time index or aggregation, and, for any time-averaged statistic, its correlation-aware calibration (degrees of freedom are never inferred from `N*T` alone) | a bare `ANEES` value with no bound is not evidence, Major |
| `Initialization error` | the initial error distribution and whether it is consistent with the initial `P_0` | a different initial error per arm is a comparability break, Blocking when arms differ |
| `Noise covariance policy` | the `Q_k` and `R_k` used per arm, how they were obtained, and whether any arm was hand-tuned | a covariance mismatch applied to the baseline only is a comparison-integrity failure, Blocking |
| `Estimator settings` | sigma points or particles, resampling scheme, and every tunable parameter, per arm | per-filter hand tuning for the proposed method only is a comparability break, Blocking |
| `Trajectory protocol` | trajectory count, duration, timestep, and the ground-truth generator | a single trajectory is not a statistical result, Blocking for an accuracy claim |
| `Linearization regime` | where the model is nonlinear and whether the covariance stays positive definite | a consistency claim in a strongly nonlinear regime without a stated region is not falsifiable, Major |

Reviewer-side checks beyond the registry. Whether the main theorem's proof closes, and whether every
hypothesis it uses is stated where it is used, which is Blocking for a theory claim. Whether the
discretization step and integration scheme match the continuous model used in the analysis. Per-step
complexity and measured runtime on a named processor where a real-time claim is made. Real-data
evidence, the sensor calibration, and the claim level it supports where a deployment claim is made.

## Comparison-protocol reconstruction test

A reviewer can reconstruct the comparison if the manuscript or its artifacts answer every question
below for the axis in question. Run this test before accepting any reported delta.

```text
[ ] Both arms are named specifically, not as a category
[ ] The dataset and split are identical, or the difference is declared
[ ] Every preprocessing and inference setting is identical, or the difference is declared
[ ] Any pretraining or external data is identical, or the difference is declared
[ ] The tuning effort is symmetric, or the asymmetry is stated
[ ] The baseline status is stated as reported or re-implemented
[ ] For a re-implemented baseline below its published value, both numbers appear
[ ] The metric definition and its parameters are identical across arms
[ ] The evaluation tooling is identical across arms
[ ] The seed policy and run count are identical across arms
```

Any unchecked box means the delta is `not comparable` until the box is checked. That is not a
rejection, it is a required wording change, and the review's resolution test should say so.

## Calibration thresholds for the common unfair comparisons

The canonical per-axis list of differences that break comparability lives in
[evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md) under Rule 3, and in
[protocol-blocks.md](../../ctrl-experiment-suite/references/protocol-blocks.md) under the
comparability verdict rules. Apply those lists as written. Do not restate them here, because a
second copy drifts and a reviewer working from a stale copy approves a delta the canonical rule
rejects.

The additions below are the breaks those lists do not name, and they are reviewer-side checks
rather than protocol fields.

| Axis | Additional break to check for |
|---|---|
| `det` | multi-scale inference applied silently on one arm, where the other list names only test-time augmentation as a whole |
| `track` | an association or motion model swapped between arms while the comparison is presented as a module delta, so the gain is attributed to the wrong component |
| `reid` | a self-built query or gallery split that leaks training identities, and tuning on the evaluation split before reporting it |
| `cnav` | a delay or loss model applied to the proposed arm only, where the other list names the ideal-channel case rather than the asymmetry of the model itself |
| `filt` | a chi-square bound selected after the result was seen, which is not a pre-registered test at any `N` |

## Evidence rules that extend beyond the primary axis

When a paper crosses axes, the primary axis gate runs in full and each secondary axis contributes
its evidence rules. The common case is a `det` paper with a `cnav` component, or a `filt` paper
with a `track` evaluation. In that situation:

- run the primary axis addendum in full;
- run the secondary axis addendum for the specific claim the secondary axis carries, not for the
  whole paper;
- apply the secondary axis's calibration thresholds to any delta computed under it;
- state in the synthesis which axis each concern belongs to, so the authors can route the repair.

## What a review must never do with a gate

- Never report a gate as passed because no one looked. `PASS` requires the artifact.
- Never downgrade a failed integrity criterion to an advisory note.
- Never convert `BLOCKED` into `FAIL`. The remedy differs, since `BLOCKED` needs an input rather
  than a change.
- Never accept a gate verdict computed on a different revision of the manuscript. A revision marks
  the earlier verdict `STALE`; its re-evaluation is `BLOCKED` until it is re-run, which is not an
  automatic scientific `FAIL`.
