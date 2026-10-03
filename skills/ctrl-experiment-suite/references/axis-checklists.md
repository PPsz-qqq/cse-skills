# Per-axis experiment checklists

One checklist per axis. Run the whole list for the primary axis and the axis-specific items for
every secondary axis. Each line is an artifact obligation, not a preference, and a line that cannot
be checked becomes a visible `[MISSING: <what is needed>]` in `ctrl-plan.md` rather than an implicit
assumption.

## `det` object detection

```text
Before running
[ ] Research question in one falsifiable sentence, with the pre-declared refutation rule
[ ] Dataset named with version and split id; the split construction rule recorded
[ ] Evaluation convention chosen and written: COCO-style or VOC-style, IoU range, point count
[ ] Baseline list with the reason for each baseline, and its capacity class
[ ] Backbone and pretraining fixed for every arm that is not a backbone ablation
[ ] Input resolution fixed across arms, or the deviation declared with its ratio
[ ] Augmentation written per arm: scale range, flip, mosaic, mixup, copy-paste
[ ] Schedule written per arm: epochs, batch size, optimizer, learning rate schedule, warmup
[ ] NMS policy written: type, IoU threshold, score threshold, max detections, class-wise or not
[ ] Inference-time settings written: TTA list, multi-scale list, fusion rule, or explicitly none
[ ] Compute budget in GPU-hours per arm, and the arm count inside the declared budget
[ ] Seed list fixed and identical across arms
During running
[ ] Every run writes config, command, environment, seeds, stdout log, and raw per-image output
[ ] Training loss curves retained for every arm, including the arms that lose
[ ] Checkpoints retained for the reported run of every arm
[ ] The evaluation script version is recorded, and one invocation evaluated every arm
[ ] Class-wise AP retained, not only mAP, so per-class regressions are visible
[ ] Object-size buckets retained: AP_S, AP_M, AP_L with the area ranges stated
[ ] Inference timing measured with the timed region, precision, batch size, and device recorded
[ ] Raw parameter and GFLOP counts recorded, measured by one tool for every arm
Before reporting
[ ] Each claimed component has a singleton arm under one protocol (references/ablation-matrix.md)
[ ] mAP reported with its averaging convention and its IoU range
[ ] AP_50, AP_75, and the size buckets reported separately where the claim touches them
[ ] Dispersion across seeds shown, with the seed list printed in the caption or the protocol block
[ ] Every arm's tier is labeled measured, re-implemented, or reported
[ ] Copied baseline numbers carry their protocol differences and a not-comparable verdict
[ ] A failure figure exists: a scene, class, or condition where the method loses
[ ] Remote-sensing submissions state the spatial separation rule between train and test tiles
[ ] Per-class results for the classes the claim depends on, not only the aggregate
```

## `track` multi-object tracking

```text
Before running
[ ] Detector named with its checkpoint identity, training set, and confidence threshold
[ ] Detection protocol fixed as public or private, with the public detection set identified
[ ] Setting fixed as online or offline, and every use of future frames listed
[ ] Metric set chosen: HOTA with DetA and AssA separated, or MOTA with IDF1, IDSW, Frag, MT, ML
[ ] MT and ML percentage thresholds stated
[ ] Evaluation tool and its version recorded, and the same tool used for every arm
[ ] Sequence list fixed, including which sequences are validation and which are reported
[ ] Association cost, motion model, and any learned appearance component named
[ ] Lifespan, birth and death logic, and track initialization rule recorded
[ ] Timing protocol written: timed region, detection included or excluded, batch size, repeats
[ ] Exact GPU named, with memory and power mode
[ ] Seed list fixed, identical across arms; 3 to 5 runs minimum

[ ] Detection files retained per arm with checksums, when public detections are used
[ ] Per-sequence metrics retained, not only the aggregate over sequences
[ ] AssA and DetA retained per sequence so an association claim can be separated from detection
[ ] IDSW and Frag counts retained with their per-sequence breakdown
[ ] Timing repeats recorded, with warm-up handling and the spread across repeats
[ ] Frame-level outputs retained for at least one sequence per arm for qualitative figures

[ ] online or offline and public or private appear next to every tracking number in every table
[ ] HOTA is reported with DetA and AssA, never alone
[ ] The detector is identical for every re-implemented arm, or the change is declared as protocol
[ ] FPS carries the GPU, batch size, timed region, and repeat count
[ ] Bootstrap or rank-based interval computed over the sequence unit, with the coarseness stated
[ ] The detections-only or no-tracker reference is reported where the metric permits it
[ ] Association-only ablations report AssA and IDSW as their evidence, not MOTA
[ ] Losing sequences are kept and discussed, not dropped from the sequence list
```

## `reid` re-identification

```text
Before running
[ ] Dataset named with version, and the identity and camera counts recorded
[ ] Query and gallery construction stated: official split, or the explicit rule with its seed
[ ] Identity disjointness between train and test verified and recorded
[ ] Backbone and pretraining fixed, including capacity class and any external unlabeled data
[ ] Input resolution written as height x width, with the crop and padding policy
[ ] Re-ranking fixed as on or off for every arm, with k-reciprocal parameters when on
[ ] Query mode fixed as single-query or multi-query, with the aggregation rule
[ ] Sampling strategy recorded: identity sampling, batch composition, instances per identity
[ ] Loss terms and their weights recorded per arm
[ ] Test-time protocol recorded separately from training, including flip and multi-crop features
[ ] Evaluation script and its version recorded; mAP convention stated
[ ] Seed list fixed, identical across arms; 3 runs minimum

[ ] Per-query scores retained so a bootstrap interval over queries is possible
[ ] CMC curve retained, not only Rank-1, so the ranking depth is visible
[ ] mINP retained when the paper uses it, with its definition stated
[ ] Distance matrix or feature files retained for at least one arm for the qualitative figure
[ ] Results logged for both mAP and Rank-1 at every evaluation point, not only at the end

[ ] Re-ranking status appears in the table header or the protocol block, identical for every row
[ ] mAP and Rank-1 reported together for every arm
[ ] Single-query or multi-query stated next to the numbers
[ ] Query count stated, so the reader can judge the resolution of a Rank-1 difference
[ ] The interval's resampling unit is the query, and the training-seed spread is reported too
[ ] Retrieval examples show failures as well as successes, with the rank of the true match
[ ] External-data arms are marked not comparable and kept out of the headline delta
[ ] Re-ranking is never presented as a model component in an ablation table
```

## `cnav` cooperative navigation

```text
Before running
[ ] Research question names the cooperative mechanism, not only the accuracy target
[ ] Node count N fixed, with the deployment region and the initial error distribution
[ ] Node distribution proof written before running: which node computes what, per node
[ ] Exchange defined: quantity, size in bytes or scalars, rate, and whether it is broadcast
[ ] Central node or global state stated as none or named explicitly
[ ] Communication model written: channel, topology, time-variance, update schedule, synchrony
[ ] Delay model written with its distribution and parameters, applied to every arm
[ ] Loss model written with its parameter, plus reconnection and timeout policy
[ ] Computation architecture labeled centralized, distributed, or hybrid, matching the proof
[ ] Ranging model written: line-of-sight or non-line-of-sight, noise distribution, outlier rate
[ ] Same ranging model for every arm, or the difference declared as a comparability break
[ ] Scenario count at least 30, with the seed list and the varied-parameter list recorded
[ ] Dead-reckoning arm and centralized upper-bound arm included

[ ] Per-node, per-run errors retained for every arm, not only the fleet average
[ ] Convergence time or consensus residual retained per run
[ ] Message counts and bytes per agent per step logged by the same rule for every arm
[ ] Topology realization and its algebraic connectivity lambda_2 recorded per run
[ ] Divergence and failure runs retained and labeled, including any run that violated a bound
[ ] Scaling runs over N recorded with the same scenario generator and the same seed list

[ ] Position metrics state 2D or 3D and the frame, ENU, NED, or world
[ ] Per-node RMSE reported with the worst node visible
[ ] The 95th percentile of position error and the fraction of runs exceeding the operational bound
[ ] Communication cost reported per arm, counted identically, including headers
[ ] Accuracy against cost reported as a frontier when two methods differ in message volume
[ ] Simulation and field results labeled separately in captions and in the text
[ ] A centralized arm is labeled as a bound and never entered as a distributed competitor
[ ] The scaling result states the N range over which the benefit holds, and where it stops
```

## `filt` filtering and state estimation

```text
Before running
[ ] Process and measurement models written as implemented, with the nonlinearity identified
[ ] State dimension n_x recorded, since it sets the NEES degrees of freedom
[ ] Estimator parameters written per arm: sigma points, particles, resampling, gating, scaling
[ ] Noise covariance policy written per arm: how Q_k and R_k were obtained, and by what tuning
[ ] Initialization error distribution written, and checked against P_0
[ ] Trajectory protocol written: count, duration, timestep, motion profile, ground-truth generator
[ ] Monte Carlo count N fixed at 100 or more, identical for every arm
[ ] Seed list identical across arms, with the generator streams separated and recorded
[ ] Chi-square bounds chosen before running: confidence level, quantiles, one-sided or two-sided
[ ] Bound used for comparison computed including the number of samples averaged
[ ] CRLB or posterior CRLB computed where a bound exists, to be plotted as a bound
[ ] Linearization region stated, and positive definiteness of P_k asserted at every step

[ ] Per-run, per-step errors retained so NEES and ANEES can be recomputed
[ ] Full P_k or a sufficient factorization retained per run/step; diagonal-only logs are insufficient for NEES unless P_k is actually diagonal
[ ] ANEES_k computed across independent runs at each time step; any temporal summary records correlation-aware calibration
[ ] RMSE computed per state component and for the full state, with the convention stated
[ ] Outlier and divergence events logged with their run id, not silently dropped
[ ] Parameter sensitivity sweeps run as separate experiments under their own protocol blocks
[ ] Single-trajectory illustrations generated from a recorded run id, labeled illustrative

[ ] Monte Carlo count stated for every arm and identical across arms
[ ] NEES/ANEES states n_x, confidence level, distribution assumptions, aggregation and numeric bounds
[ ] Default pointwise ANEES bounds use N*n_x divided by N; pooling time requires independence or calibrated correlation handling
[ ] The bound actually plotted is given as a number, with the sample count it was averaged over
[ ] RMSE and consistency reported together for every arm
[ ] A filter outside the bounds is reported as inconsistent, with the direction stated
[ ] No covariance was retuned after seeing the consistency result, or the sequence is disclosed
[ ] CRLB appears as a bound on the axes, not as a baseline in the comparison table
[ ] A single trajectory is never presented as a statistical result
[ ] The covariance mis-specification sensitivity analysis is present where robustness is claimed,
    with the mis-specification class named
```

## Closing items for every axis

```text
[ ] The protocol block for this axis is complete (references/protocol-blocks.md)
[ ] The statistical treatment is applied (references/statistics-and-seeds.md)
[ ] The trap audit has been run (references/statistical-traps.md)
[ ] Every table was regenerated from the raw artifacts after the last code change
```
