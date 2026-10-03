# Protocol blocks and the per-axis field registry

A protocol block is the instrument definition for a comparison. Without it a delta is not a
measurement, and `ctrl-shared` `core/gate-contract.md` G2 fails the comparison by default. This file
defines the exact field names to emit, so that `ctrl-protocol.md`, `ctrl-claims.md`, the manuscript
tables, and any later response letter use one vocabulary. Copy the block below into
`ctrl-protocol.md`, one block per comparison, then fill the per-axis fields for the active axis. Do
not rename fields, because a renamed field cannot be reconciled later.

## Block skeleton

```text
## P-<axis>-<n>: <one line naming what is compared and where>
- Axis: det | track | reid | cnav | filt
- Dataset and split: <dataset, version, split id, and how the split was built>
- Task and metric definitions: <metric names with their exact convention>
- Arms: <arm name; tier measured/reported/assumed; provenance original/re-implemented/copied; setting; per-arm deviations>
- Seeds and runs: <count, exact seed list or policy, dispersion reported where>
- Hardware and environment: <device, count, framework and version, determinism flags>
- <per-axis fields, in the order given for the active axis>
- Comparability verdict: <comparable | partially comparable | not comparable, per arm pair>
```

`Arms` is a list, not a category. "ours versus several state-of-the-art methods" fails G1. Write
`ours, ByteTrack (re-implemented), OC-SORT (reported, protocol difference: 256x128 input)`.

## Per-axis required fields

The field names below are normative. Every comparison on that axis emits every field, including
those whose value is `identical for all arms`, `none`, or `[MISSING: <what is needed>]`.

### `det` object detection

| Field | What must be written | Failure mode when omitted |
|---|---|---|
| `Backbone` | architecture, capacity class, and parameter count | a delta between a ResNet-50 arm and a Swin-L arm is a capacity delta |
| `Pretraining` | dataset, supervision type, and whether extra data beyond the baseline's was used | extra pretraining data is a comparability break at any size |
| `Input resolution` | train and test resolution in pixels, and the resize policy | any ratio above 1.3x between arms is a comparability break |
| `Augmentation` | the full recipe, including random scale range, flip, mosaic or mixup policy, and copy-paste | one arm with extra augmentation is a training-recipe delta |
| `Training schedule` | epochs or iterations, batch size, optimizer, learning rate schedule, warmup | an epoch budget beyond 1.5x of another arm is a comparability break |
| `Test-time augmentation` | every TTA transform applied at inference, or `none` | TTA on one arm only is a comparability break |
| `Multi-scale inference` | single-scale or the explicit scale list, and the fusion rule | silent multi-scale on the proposed arm inflates AP |
| `NMS policy` | greedy, soft, or learned; IoU threshold; score threshold; max detections per image; whether class-wise | a differing NMS policy changes AP without any method difference |
| `Evaluation split` | evaluation server versus local split, and the split hash or id | COCO `val` for one arm against `test-dev` for another is a comparability break |

Metric definitions for `det` state the averaging convention explicitly, such as COCO-style
101-point interpolated AP averaged over IoU 0.50 to 0.95 in steps of 0.05, with `AP_50`, `AP_75`,
and `AP_S` / `AP_M` / `AP_L` reported separately, or VOC-style all-point AP with the stated IoU
threshold. For pedestrian detection state the FPPI convention and the log-average miss rate
evaluation subset, because the numbers move with the subset.

### `track` multi-object tracking

| Field | What must be written | Failure mode when omitted |
|---|---|---|
| `Detector provenance` | detector name, checkpoint identity or hash, training set, and confidence threshold | a MOTA without provenance is comparable to nothing |
| `Detection protocol` | `public` or `private`, and the exact public detection set used when public | private for one arm against public for another is a comparability break |
| `Setting` | `online` or `offline`, and every post-processing step that uses future frames | offline post-processing on one arm only is a comparability break |
| `FPS` | what the number includes, detection or not, preprocessing or not, batch size, and the sequence | a throughput number without its scope is not a measurement |
| `FPS GPU` | exact part, memory, power mode, and driver | FPS across different GPUs is a comparability break |
| `Association and motion model` | the association cost, the motion model, and any learned component | a tracker swap is presented as a module delta |
| `Tracking metrics` | `HOTA` with `DetA` and `AssA` separated, or `MOTA` with `IDF1`, `IDSW`, `Frag`, `MT`, `ML` and their percentage thresholds | a single MOTA hides a detection gain as an association gain |

State `online` or `offline` and `public` or `private` adjacent to every tracking number in every
table, not once in the protocol section. The two labels travel with the number.

### `reid` re-identification

| Field | What must be written | Failure mode when omitted |
|---|---|---|
| `Backbone and pretraining` | architecture, capacity class, pretraining dataset, and whether external unlabeled data was used | external unlabeled data on one arm is a comparability break |
| `Input resolution and crop policy` | height x width, the ratio convention, and the crop or padding rule | a differing test resolution or crop policy is a comparability break |
| `Re-ranking` | `on` or `off` for every arm, plus k-reciprocal parameters when on | re-ranking on one arm only is a comparability break |
| `Query/gallery construction` | the official split, or the explicit rule used to build query and gallery, including camera overlap and identity disjointness | a self-built split that leaks training identities inflates both metrics |
| `Query mode` | `single-query` or `multi-query`, and the aggregation rule when multi-query | multi-query against single-query is a comparability break |
| `Evaluation data` | whether evaluation ran on the official test split or a validation split carved from train | tuning on test and reporting test is test-set tuning |
| `Reid metrics` | `mAP`, `Rank-1`, `Rank-5`, and whether the metric is computed with the official evaluation code version | a hand-rolled mAP is not comparable to a published one |

### `cnav` cooperative navigation

| Field | What must be written | Failure mode when omitted |
|---|---|---|
| `Node distribution proof` | which node computes what, listed per node, and the artifact that shows it | a centralized solution presented as distributed is a comparability break |
| `Exchange` | the exact quantity each message carries, its size in bytes or scalar count, and the message rate | an unstated exchange lets a central-equivalent method look distributed |
| `Central node or global state` | `none` or the named node and the state it holds | a hidden global state invalidates the distribution claim |
| `Communication model` | channel type, topology and whether it is time-varying, update schedule, and whether messages are synchronous | a perfect channel on one arm only is a comparability break |
| `Delay` | delay model, its distribution and parameters, and whether it is applied to all arms | zero delay on the proposed arm only is a comparability break |
| `Loss` | packet loss or dropout model with its parameter, plus reconnection or timeout policy | an ideal channel for one arm is a comparability break |
| `Computation architecture` | `centralized`, `distributed`, or `hybrid`, and the convergence or consensus rounds per step | the label must match `Node distribution proof`, not the paper's aspiration |
| `Scenario generation` | node count `N`, deployment region, initial error distribution, motion profile, and the number of runs | fewer than 30 runs cannot support a stochastic scenario claim |
| `Position metrics` | `RMSE` or `CEP` in 2D or 3D, per-node and fleet-aggregate, with the frame (ENU, NED, or world) | an unspecified frame or dimension makes the error value meaningless |
| `Ranging model` | line-of-sight or non-line-of-sight, noise distribution, outlier rate, and whether the model is shared by all arms | a different ranging noise model per arm is a comparability break |

### `filt` filtering and state estimation

| Field | What must be written | Failure mode when omitted |
|---|---|---|
| `Monte Carlo count` | the number of runs `N`, and whether every arm used the same `N` | a different `N` per arm is a comparability break |
| `Consistency metric` | `NEES` or `ANEES`, the estimator that produced `P_k`, and the degrees of freedom `n_x` | an error plot without a consistency metric cannot support an optimality or consistency claim |
| `Chi-square bounds` | the quantiles used, the confidence level, whether the test is one-sided or two-sided, and the degrees of freedom those quantiles were taken at | a bound chosen after seeing the result is not a test; a bound taken at the wrong degrees of freedom flags a consistent filter as inconsistent |
| `Bound used for comparison` | the numeric lower and upper bound actually plotted, the degrees of freedom used, and over how many runs and time steps it was averaged | a bare ANEES value with no bound is not evidence |
| `Initialization error` | the initial state error distribution and whether it is consistent with the initial `P_0` | a different initial error per arm is a comparability break |
| `Noise covariance policy` | `Q_k` and `R_k` used per arm, how they were obtained, and whether any arm was hand-tuned | covariance mismatch applied to the baseline only is a comparability break |
| `Estimator settings` | sigma points or particles, resampling scheme, and all tunable parameters per arm | per-filter hand tuning for the proposed method only is a comparability break |
| `Trajectory protocol` | trajectory count, duration, timestep, process model, and the ground-truth generator | a single trajectory is not a statistical result |
| `Linearization regime` | where the model is nonlinear, the operating region, and whether the covariance stays positive definite | a consistency claim in a strongly nonlinear regime without a stated region is not falsifiable |

Use the distribution and independence assumptions in
[terminology-and-notation.md](../../ctrl-shared/core/terminology-and-notation.md). Default to ANEES
at each time step across independent runs: `N*n_x` degrees of freedom, chi-square quantiles divided
by `N`, expected value `n_x`. Temporal pooling uses `N*T*n_x` divided by `N*T` only when **all pooled
samples are independent** under the chi-square model; normal filtering trajectories do not guarantee
this. Otherwise specify a correlation-aware calibration. Record aggregation and assumptions in
`Consistency metric` and `Chi-square bounds`, and label pointwise versus simultaneous assessment.

## Comparability verdict rules

Write one verdict per arm pair, not one per table.

| Verdict | Condition | How the number may appear |
|---|---|---|
| `comparable` | every required field matches, or differs only in ways justified by a control run | as a delta in the main table |
| `partially comparable` | one declared difference whose direction of bias is known | in the main table with the difference in a footnote, and in the text as an upper or lower bound on the true delta |
| `not comparable` | any break in `ctrl-shared` `core/evidence-integrity.md` Rule 3 for the axis, or an unknown difference | as a separate row or a separate table, with `not comparable` written next to it |

The calibration thresholds that most often flip a verdict are resolution above 1.3x, extra
pretraining data, one-arm TTA, an epoch budget beyond 1.5x, val against test-dev, public against
private detection, a different detector checkpoint, offline post-processing on one arm, re-ranking
on one arm, multi-query against single-query, external unlabeled reid data, a perfect communications
arm, a different ranging noise model, per-arm hand tuning, and a different Monte Carlo count. Each is
listed with its axis in `ctrl-shared` `core/evidence-integrity.md`.

## Worked examples

Two filled blocks, abbreviated to the fields that carry the argument. Real blocks carry every field.

```text
## P-track-1: association comparison on the MOT benchmark, private detection
- Axis: track
- Dataset and split: MOT17 train split, first half for validation, second half for reporting
- Task and metric definitions: HOTA with DetA and AssA separated; MOTA, IDF1, IDSW, Frag; MT at 80 percent and ML at 20 percent
- Arms: ours (measured); ByteTrack (re-implemented, our detector); OC-SORT (reported, protocol difference: their detector)
- Seeds and runs: 3 seeds, seed list 0,1,2, dispersion in Table 3
- Hardware and environment: 1x A100 40GB, PyTorch 2.x, cuDNN deterministic, single sequence stream
- Detector provenance: YOLOX-x checkpoint, COCO-pretrained, confidence 0.1, identical for all re-implemented arms
- Detection protocol: private, identical detection files for every re-implemented arm
- Setting: online, no future frames, no track-level smoothing
- FPS: tracker only, detection excluded, batch size 1, per sequence then averaged
- FPS GPU: A100 40GB, default power mode, driver recorded in exp/track-1/env.txt
- Comparability verdict: ours vs ByteTrack comparable; ours vs OC-SORT not comparable on HOTA
```

```text
## P-filt-1: consistency of the proposed estimator against the baseline
- Axis: filt
- Dataset and split: simulated nonlinear benchmark, 200 independent trajectories
- Task and metric definitions: RMSE per state component; NEES and ANEES on the full state
- Arms: ours (measured); EKF baseline (re-implemented under the same model); UKF (re-implemented)
- Seeds and runs: 200 Monte Carlo runs per arm, identical seed list shared across arms
- Hardware and environment: CPU only, NumPy recorded version, no GPU nondeterminism
- Monte Carlo count: 200 per arm, identical for all arms
- Consistency metric: ANEES_k across 200 independent runs at each k, from each filter's own P_k, n_x = 6; chi-square reference assumes Gaussian errors with the stated covariance
- Chi-square bounds: pointwise two-sided 95 percent, quantiles 0.025 and 0.975, df = N*n_x = 1200
- Bound used for comparison: chi2(0.025,1200)/200 and chi2(0.975,1200)/200; compute numeric bounds with the recorded statistics library before plotting, never use T as extra independent replicates
- Initialization error: consistent with P_0 for every arm, drawn from the same generator
- Noise covariance policy: true Q_k and R_k given to all arms, no per-arm tuning
- Estimator settings: 2n+1 sigma points, systematic resampling at 1000 particles for the particle arm
- Trajectory protocol: 100 steps, dt 0.1 s, same process model for all arms
- Linearization regime: heading error below 30 degrees, P_k positive definite checked each step
- Comparability verdict: comparable across all three arms
```

## Emitting the block, and pre-registration

Read the fields from the run configuration rather than from memory, because a field that is not in
the config file will drift between the run and the manuscript. Record the config path in the block's
`Hardware and environment` line so the block can be regenerated, and append a dated revision rather
than editing a frozen block in place. Commit the block before the first run of the comparison, with
the configuration first and the results in a separate later commit, never combined, so the history
shows what was planned before the numbers were seen.

| Label | Meaning | How it may be written |
|---|---|---|
| `confirmatory` | arm, metric, split, and decision rule all match the frozen block | as the result of the planned experiment |
| `exploratory` | anything chosen or changed after results were seen, including a post-hoc metric, split, or threshold | as an observation, with the deviation named, never as the test of the hypothesis |

A deviation is admissible and concealing it is not. State in the revision which results moved to
`exploratory`. Checklist before use.

```text
[ ] Every normative field for the axis is present, none left blank
[ ] Every arm carries a tier label and a measured/re-implemented/reported status
[ ] Dataset version and split id are recorded, not described
[ ] Metric conventions are stated where the metric name alone is ambiguous
[ ] Seeds are listed, not summarized as "several runs"
[ ] Hardware is exact, including the GPU model for every throughput number
[ ] Comparability verdict is written per arm pair, and the block id appears in every dependent row
[ ] Filt bounds state aggregation/distribution/independence; default is N*n_x divided by N at each k
[ ] Temporal pooling is justified or uses correlation-aware calibration; pointwise violations are not an all-time guarantee
[ ] The block was committed before the numbers were read
[ ] Every result carries a confirmatory or exploratory label, and every post-hoc deviation is dated
```
