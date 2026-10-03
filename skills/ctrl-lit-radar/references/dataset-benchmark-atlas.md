# Dataset and benchmark atlas

For each benchmark: what it actually measures, its known protocol trap, and what it cannot
establish. This file is written under one rule. A row states a number only where that number was read
at a primary source during the compilation of this file, and everything else carries an explicit
`[UNVERIFIED]` marker naming what is missing. Counts drift between dataset versions, so confirm the
count for the exact version you use even where a value is given here.

Primary sources consulted: the COCO dataset site (cocodataset.org) and the COCO paper (arXiv:1405.0312),
the DOTA dataset page (captain-whu.github.io/DOTA), objects365.org, the MOT16 benchmark paper
(arXiv:1603.00831), the DanceTrack paper (arXiv:2111.14690), the UAVDT benchmark paper
(arXiv:1804.00518), the VisDrone dataset README (github.com/VisDrone/VisDrone-Dataset), the MSMT17
paper (arXiv:1711.08565), the KITTI tracking benchmark page (cvlibs.net), and the reporting on the Duke
MTMC withdrawal (exposing.ai) plus the MOTChallenge service notice (motchallenge.net).

Numbers in this file carry one of three statuses. A value read at the primary source during
compilation is stated plainly with the source named in the row. A value that could not be confirmed is
either omitted or enclosed in an explicit `[UNVERIFIED]` marker naming what is missing. The
qualitative columns, meaning what a benchmark measures, its traps, and its limits, are analytical
guidance throughout and depend on the reader confirming the specifics at the source.

## `det` detection benchmarks

| Benchmark | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| PASCAL VOC (2007, 2012) | 20-class detection on natural images; the classic AP with a fixed IoU threshold `[UNVERIFIED: class count and image counts not read at a primary source in this pass]` | `[UNVERIFIED]` the 2007 test annotations are commonly described as public and the 2012 ones as withheld, which would make 2012 numbers evaluation-server numbers and not locally reproducible, but this was not confirmed at the official VOC site in this pass; confirm before relying on it. VOC-style AP averaging differs from COCO-style | small-object performance, dense-scene performance, and anything about modern architectures, since the dataset is small and easy by current standards |
| MS COCO (2017) | `[UNVERIFIED]` the standard AP summary is commonly described as an average over ten IoU thresholds from 0.50 to 0.95 in steps of 0.05, plus AP at 0.50 and 0.75 and a split by object size, but the cocodataset.org page fetched in this pass returned navigation only, so the metric list and the category and image counts were not read at a primary source. The dataset paper (arXiv:1405.0312) states 91 object types and 2.5 million labeled instances in 328k images for the original release, which is not the same as the 2017 detection release | `[UNVERIFIED]` the usual claim is that `test-dev` and `test-challenge` labels are withheld and results go through an evaluation server, so a leaderboard number would not be comparable to a locally computed `val2017` number; confirm at the official evaluation page. Also confirm whether the category index has 91 entries with 80 used, since category-count claims depend on it | performance on aerial or oriented objects, since the boxes are axis-aligned; cross-dataset generalization; anything about runtime |
| Objects365 | 365 categories, 2 million images, 30 million bounding boxes, read directly from the official site (objects365.org) | the published counts are a headline figure whose version (v1 versus v2) must be pinned, because the two differ and the site's figure does not name a version; using it as extra pretraining data breaks comparability with arms that did not, which is exactly the `det` calibration threshold in [../../ctrl-shared/core/evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md) | state-of-the-art detection quality on its own, because it is usually a pretraining corpus rather than the evaluation target |
| DOTA v1.0 and v2.0 | large-scale aerial detection with oriented bounding boxes. Read from the official dataset page: v1.0 has 15 categories, v2.0 has 18, adding container crane, airport and helipad. Images come from Google Earth, GF-2 and JL-1 satellite imagery via the China Centre for Resources Satellite Data and Application, plus aerial imagery from CycloMedia B.V.; RGB images come from Google Earth and CycloMedia while grayscale images come from the GF-2 and JL-1 panchromatic bands. DOTA-v2.0 is downloaded as the v1.0 images plus extra images. `[UNVERIFIED: image and instance counts were not read at the primary source in this pass]` | **DOTA-v2.0 relabelled the DOTA-v1.0 images**, stated explicitly on the official page, so evaluating v2.0 with v1.0 annotations is wrong; the official page also states that the images and annotations may be used for academic purposes only and that any commercial use is prohibited, which matters for a release; images are enormous, so tiling introduces a train/test leakage risk if tiles from one scene are split across sets; annotations carry a `difficult` flag whose handling changes reported numbers | performance on non-aerial imagery; anything about real-time operation, since the images are large and offline |
| VisDrone (DET and MOT subsets) | drone-captured detection and tracking, collected by the AISKYEYE team at the Lab of Machine Learning and Data Mining, Tianjin University. The official README states the benchmark consists of 288 video clips formed by 261,908 frames plus 10,209 static images, with more than 2.6 million bounding boxes, captured by various drone-mounted cameras across details including 14 cities, urban and country environments, and sparse and crowded densities. The challenge defines five tasks: image detection, video detection, single-object tracking, multi-object tracking, and crowd counting | the split naming is the trap, and it is commonly mis-stated. The official README states that **test-dev annotations are available** and that researchers can use test-dev to publish, while **testset-challenge annotations are unavailable**; a paper that treats the whole test set as withheld or as available is wrong either way, and the split must be named exactly. The data was collected on **various drone models**, so a claim about one specific platform does not follow, and the scale distribution is still platform-dependent | performance on satellite or high-altitude imagery, which has a different scale distribution; anything about a fixed camera; and the counts differ between the VisDrone2018 and VisDrone2019 releases, so the release must be named |
| UAVDT | a UAV benchmark for detection, single-object tracking and multi-object tracking. The paper (arXiv:1804.00518) states that about 80,000 representative frames were selected from 10 hours of raw video and fully annotated with bounding boxes plus up to 14 kinds of attributes (weather condition, flying altitude, camera view, vehicle category, occlusion, and others) for three tasks | the attribute annotations make subset evaluation easy and subset cherry-picking equally easy, so the evaluation subset rule must be declared in advance; the frame count is stated as approximate in the paper, so do not present it as an exact count | pedestrian performance, since it targets vehicles; performance outside the recorded weather and altitude envelope |

Related options worth naming when the claim needs them: `xView` and `DIOR` for satellite detection,
`COCO-C` / `Pascal-C` style corruption benchmarks derived from COCO and PASCAL for robustness claims,
and `Cityscapes` for driving-scene detection. Any corruption benchmark measures sensitivity to the
chosen corruption set and severity levels, not robustness in general.

## `track` tracking benchmarks

| Benchmark | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| MOT17 | multi-object pedestrian tracking. The MOT16 paper (arXiv:1603.00831), which the benchmark line builds on, documents 14 sequences split into 7 training and 7 testing, a strict annotation protocol, and crucially three annotated object classes: pedestrians as the evaluated targets, "distractors" such as sitting people, reflections, mannequins and people behind glass that are neither penalised nor rewarded, and vehicles or occluders annotated only for training and for computing occlusion level. It also states that visibility level is provided per object and that a minimum pixel height gates which pedestrians the evaluation counts. `[UNVERIFIED]` MOT17 is commonly described as associating each sequence with DPM, Faster R-CNN (FRCNN) and SDP detection sets; the FRCNN variant was confirmed in a public copy of the dataset, but the full triple and the exact split counts were not read at the official source in this pass | the **public versus private detection protocol** distinction is the whole comparability question. In the public protocol the tracker consumes the supplied detections, and in the private protocol it runs its own detector, so the two numbers are not comparable and mixing them is the most common unfair comparison in this axis. The MOT16 paper also documents two further traps: the IoU matching threshold varies between papers from about 25 to 50 percent and changes the numbers, and the distractors class means a tracker that follows a sitting person is not penalised | anything about appearance-free tracking, because the sequences were selected partly because appearance is discriminative, which is precisely the bias DanceTrack was built to expose |
| MOT20 | `[UNVERIFIED]` a MOTChallenge release commonly described as denser pedestrian scenes than MOT17; the sequence and identity counts were not read at a primary source in this pass | `[UNVERIFIED]` the density is commonly said to change the occlusion statistics so a method tuned on MOT17 does not transfer without stating the difference; detector provenance and online versus offline must be declared as for MOT17. Confirm both at the official source | sparse-scene performance, and any claim that generalizes across density regimes without a per-benchmark result |
| DanceTrack | multi-human tracking where appearance is deliberately not discriminative. Read from the paper (arXiv:2111.14690): a large-scale dataset for multi-human tracking where humans have similar appearance, diverse motion and extreme articulation, collected mostly from group-dancing videos. The paper states the motivation explicitly, which is that existing tracking datasets are biased because most objects have distinguishing appearance so re-identification models suffice for association | a method that relies on an appearance model will look weak here and that is the intended signal, so report it rather than switching benchmark; the paper reports a significant performance drop for benchmarked state-of-the-art trackers when compared against existing benchmarks, so numbers are not comparable to MOT17 numbers because the sequence statistics differ | pedestrian tracking in surveillance conditions, and identity-preserving re-identification under appearance ambiguity outside dance footage |
| KITTI tracking | 2D bounding-box tracking in driving scenes; the benchmark page states 21 training and 29 test sequences, with 8 labelled classes of which only Car and Pedestrian are evaluated; the sensor suite provides colour and grayscale stereo images, Velodyne point clouds, GPS/IMU, and calibration, with L-SVM and Regionlets reference detections supplied | since February 2021 the evaluation uses HOTA as the primary metric with CLEAR MOT and MT/PT/ML also reported, and older MOTA-style numbers are not comparable with post-2021 numbers; the test split requires registration and a submission, and the benchmark states a policy restricting submissions to work leading to a peer-reviewed paper; detections smaller than 25 pixels in height are excluded from evaluation, and Vans are not counted as false positives for Cars | pedestrian-dense tracking; anything about non-driving scenes; and the benchmark explicitly does not include detection time in the reported runtime, so its speed numbers are not end-to-end |
| VisDrone MOT | see the `det` table; the same platform and split caveats apply, and the tracking numbers carry the additional detector-provenance question | test-dev annotations are available while testset-challenge annotations are not; detector provenance unstated in many papers | driving-scene tracking |

Service availability warning. The MOTChallenge site (motchallenge.net) served an HTTP 410 notice at
the time of writing, stating that the benchmark service is offline, the evaluation server and
submissions are not operating, and that the dataset archives remain available while the leaderboards
were preserved as a static archive. A plan that depends on a new MOTChallenge submission needs a
different route, and a claim about "the current MOTChallenge leaderboard" needs the archive date. Treat
the live status as `[UNVERIFIED]` at the moment of use and check it.

## `reid` re-identification benchmarks

| Benchmark | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| Market-1501 | `[UNVERIFIED: identity, image, box and camera counts were not read at a primary source in this pass]` person re-identification over multiple cameras, evaluated with mean AP and Rank-1 under a single-query protocol | re-ranking on or off changes the numbers substantially and is the classic one-arm-only unfairness; the standard protocol uses a fixed query/gallery split and a distractor set whose treatment must match across arms | cross-domain generalization, since it is usually the training source; vehicle re-identification |
| MSMT17 | person re-identification with a large identity count. Read from the paper (arXiv:1711.08565): 4,101 identities and 126,441 bounding boxes, from raw video taken by a 15-camera network deployed in both indoor and outdoor scenes, covering a long period with complex lighting variation | the paper states that domain gap between datasets causes severe performance drop when training and testing on different datasets, and it proposes a GAN-based transfer method to narrow it, so the dataset's own baselines are entangled with that method; image resolution and crop policy differ from Market-1501, so a comparison across the two datasets must use per-dataset protocols | performance on a small camera network, and anything about real deployment conditions beyond the recorded 15 cameras |
| DukeMTMC-reID | person re-identification derived from the Duke MTMC surveillance dataset | **the underlying dataset was withdrawn.** The exposing.ai dataset analysis records that Duke MTMC was built from campus surveillance video collected in 2014 from 8 cameras at 1080p and 60 FPS, with over 2 million frames, and that Duke University terminated the dataset in 2019 after that report and a Financial Times investigation. The same source notes the original paper mentions 2,700 identities while the ground-truth file lists annotations for 1,812, which is itself a reminder to confirm identity counts rather than quote a headline. The re-identification extension shares those subjects, so do not build a new result on it, do not present it as available, and if a baseline number is quoted, state that it is withdrawn | anything going forward, because it cannot be ethically or practically re-obtained |
| VeRi-776 | `[UNVERIFIED: identity, image and camera counts were not read at a primary source in this pass]` vehicle re-identification from surveillance cameras with identity and attribute annotations | the vehicle setting has far more appearance variation from viewpoint than person re-identification, so results are not transferable across the two tasks; the standard split is small | person re-identification, and large-scale vehicle retrieval |
| VehicleID | `[UNVERIFIED: identity and image counts were not read at a primary source in this pass]` vehicle re-identification at larger identity scale, with a protocol that historically offered several gallery-size test splits | reporting the best of several test splits without stating which split is a selection effect; the splits are not interchangeable | cross-camera protocol behaviour equivalent to Market-1501, and anything about non-vehicle objects |
| CUHK03 | `[UNVERIFIED: identity count and split convention were not read at a primary source in this pass]` person re-identification with both hand-drawn `labeled` boxes and automatically `detected` boxes, giving two evaluation settings | the classic trap is comparing a `labeled`-box result against a `detected`-box result, which is exactly the crop-policy unfairness in the `reid` calibration row; the identity count and the split convention have changed across versions of the benchmark, so the version must be stated | deployment performance under real detector noise unless the `detected` setting is used |

General rule for this axis. A re-identification number is a tuple, not a scalar. It is composed of the
backbone and pretraining, the input resolution and crop policy, the re-ranking status, the query mode,
and the dataset split. Any comparison table that omits one of those columns is not a comparison.

## `cnav` cooperative-navigation benchmarks

This axis has no single dominant public benchmark, and that is itself the finding. Claims here are
usually supported by a custom simulation plus, where the venue demands it (class B robotics venues),
a hardware demonstration.

Verification status for this section. None of the resources below was opened at a primary source in
this pass, and no counts are stated for them. The rows describe the structural properties and the
traps of each resource type, and are marked `[UNVERIFIED]` as to their specifics. Confirm the
publisher, the contents, the ground-truth method and the license at the dataset's own page before
naming any of them in a plan or a manuscript.

| Resource | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| UTIAS multi-robot cooperative localization dataset | a canonical multi-robot dataset for cooperative localization with ground truth from a motion-capture system | motion-capture ground truth means an indoor, controlled environment, so a claim about outdoor or GNSS-denied operation does not follow; the vehicle count and formation are fixed | outdoor operation, GNSS-denied operation, large-scale swarms |
| EuRoC MAV | visual-inertial odometry and state estimation on a micro aerial vehicle, with ground truth from a motion-capture system in one part and from a laser tracker in another | widely used for `filt` and single-agent estimation, so it is often mis-cited as a cooperative benchmark when it involves one vehicle | multi-agent cooperation, inter-agent ranging, and communication effects |
| S3E and similar multi-UAV datasets | multi-UAV flight with cooperative tasks | ground-truth quality and synchronization between agents determine what can be claimed; if ground truth is derived from one agent's GNSS, the results are relative to that agent | absolute accuracy under GNSS denial |
| GRASP multiple micro-UAV dataset | multi-quadrotor flight data for cooperative estimation and control | the platform is small and indoor or short-range | outdoor swarms, long-duration operation, communication loss over distance |
| Custom simulation | whatever the author defines | the dominant trap of the axis: a simulation whose noise model, communication delay, packet loss, ranging outlier model and topology were chosen by the author, compared against a baseline given a different model. This is the `cnav` calibration row in [../../ctrl-shared/core/evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md) | field validity. A simulation result is a `simulation` result |

For any `cnav` result, the required protocol block from
[../../ctrl-shared/core/gate-contract.md](../../ctrl-shared/core/gate-contract.md) applies. It must
state which nodes compute, what is exchanged, whether any central node or global state exists, and the
communication model with delay and loss. Without that block the number is not interpretable.

## `filt` filtering and estimation benchmarks

Verification status for this section. These scenarios are named from general knowledge of the
estimation literature, and none was traced to a defining primary source in this pass, so every row is
`[UNVERIFIED]` as to its attribution. The scenario descriptions and traps below are the operating
guidance; the attribution of who defined each scenario, and whether reference results exist, must be
established by reading the citing literature before any of them is named in a manuscript.

| Benchmark or scenario | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| The bearings-only tracking scenario | a nonlinear estimation problem where a single sensor measures only the bearing to a target, so observability depends on the own-ship manoeuvre; a standard vehicle for comparing nonlinear filters | the manoeuvre profile is part of the problem definition, and a filter tuned per scenario is not a filter; the initialization error dominates the early RMSE, so the initialization must match across arms | performance under a different sensor suite, and anything about the estimate at times when the geometry is unobservable |
| The reentry-vehicle problem | a highly nonlinear, non-Gaussian tracking problem used to discriminate between filters, where the measurement model is very informative near the end of the trajectory | the near-singular measurement geometry makes results extremely sensitive to numerical implementation and to the sigma-point or particle settings, so a small implementation difference can dominate the comparison | general filtering quality, because it is an extreme case; steady-state behaviour |
| The univariate nonstationary growth model | a scalar nonlinear benchmark with a bimodal or heavily skewed posterior, widely used to test particle filters and sigma-point filters | because it is scalar and cheap, it is often run with a small Monte Carlo count, which is not enough to resolve the tails that the benchmark is chosen for | multi-dimensional estimation behaviour, and a Gaussian consistency check in the NEES sense, because the strong non-Gaussianity of the posterior is exactly what invalidates that check |
| Author-supplied target-tracking scenarios | whatever the paper needs | the `filt` calibration row: per-filter hand tuning for the proposed method only, different Monte Carlo counts, different initialization error, and noise covariance mismatch applied to the baseline only | anything beyond the scenario envelope |

Required evidence for this axis, from
[../../ctrl-shared/core/gate-contract.md](../../ctrl-shared/core/gate-contract.md), is the Monte Carlo
count, NEES or ANEES against its chi-square bounds, and the bound used for comparison. The pack
minimum is 100 Monte Carlo runs for accuracy and consistency claims. A single trajectory is not a
statistical result.

## How to read this atlas

1. Pick the benchmark whose failure mode matches the claim's failure mode, not the most popular one.
2. Write the protocol block for the axis before running anything, using
   [../../ctrl-shared/core/gate-contract.md](../../ctrl-shared/core/gate-contract.md).
3. Write the "cannot establish" column into the limitations section in advance. It is the cheapest
   and most credible honesty in the paper.
4. Confirm every count, split and version at the primary source before it appears in a manuscript.
   Even a value stated here was read at one specific version on one specific date, and dataset counts
   drift.
