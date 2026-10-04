# Dataset and benchmark atlas

For each benchmark: what it actually measures, its known protocol trap, and what it cannot
establish. This file is written under one rule. A row states a number only where that number was read
at a primary source, and everything else carries an explicit `[UNVERIFIED]` marker naming what is
missing. Counts drift between dataset versions, so confirm the count for the exact version you use
even where a value is given here, and cite the dataset's own paper or page, never this file.

Verification pass: 2026-10-03 (Asia/Hong_Kong). Sources read in that pass: the VOC2007 challenge
page (robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2007/), the COCO paper abstract (arXiv:1405.0312)
and the official evaluation code (cocoapi `pycocotools/cocoeval.py`), the Objects365 ICCV 2019 paper
page (CVF open access), the DOTA papers (arXiv:1711.10398, arXiv:2102.12219) and dataset page
(captain-whu.github.io/DOTA), the VisDrone README (github.com/VisDrone/VisDrone-Dataset), the UAVDT
paper (arXiv:1804.00518), the archived MOT17 and MOT20 pages and the motchallenge.net status page,
the DanceTrack project page and paper (arXiv:2111.14690), the KITTI tracking page (cvlibs.net), the
Market-1501 ICCV 2015 paper page, the MSMT17 paper (arXiv:1711.08565v2), the DukeMTMC paper
(arXiv:1609.01775), the VeRi page (vehiclereid.github.io/VeRi), the PKU VehicleID page (pkuml.org),
the re-ranking paper (arXiv:1701.08398), the UTIAS MR.CLAM page (asrl.utias.utoronto.ca), and the S3E
paper (arXiv:2210.13723v8) and project page. Pages that could not be fetched are named in the rows.

The qualitative columns, meaning what a benchmark measures, its traps, and its limits, are analytical
guidance and depend on the reader confirming the specifics at the source.

## `det` detection benchmarks

| Benchmark | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| PASCAL VOC (2007, 2012) | 20-class detection on natural images. The VOC2007 page lists the 20 classes, 9,963 images with 24,640 annotated objects, split about 50 percent train/val and 50 percent test, and the annotated test set was released after the challenge (November 2007) | the VOC2012 test annotations are commonly described as withheld behind an evaluation server `[UNVERIFIED: VOC2012 page not read in this pass]`, so VOC2007-test and VOC2012-test numbers are produced differently. The AP averaging convention changed between devkit versions `[UNVERIFIED: confirm the devkit used]`; name the devkit and the interpolation rule | small-object performance, dense-scene performance, and anything about modern architectures, since the dataset is small and easy by current standards |
| MS COCO | The dataset paper (arXiv:1405.0312) states 91 object types and 2.5 million labeled instances in 328k images for the original collection. The official evaluator (`cocoeval.py`) averages AP over ten IoU thresholds from 0.50 to 0.95 in steps of 0.05 with 101 recall points, reports AP at 0.50 and 0.75, uses maximum detections 1, 10 and 100, and defines small, medium and large objects by area below 32^2, between 32^2 and 96^2, and above 96^2 pixels | the 2017 detection annotations use a subset of the paper's 91 category ids `[UNVERIFIED: commonly 80; count the categories field of the annotation file you use]`, and the split sizes should be read from the annotation files. `test-dev` labels are commonly described as withheld behind an evaluation server `[UNVERIFIED: cocodataset.org rendered navigation only in this pass]`, so a server number and a locally computed `val2017` number are different measurements | performance on aerial or oriented objects, since the boxes are axis-aligned; cross-dataset generalization; anything about runtime |
| Objects365 | The ICCV 2019 paper states 365 categories, more than 600K training images and more than 10 million boxes for the release it describes. Later releases are larger and are often quoted at about 2 million images and 30 million boxes `[UNVERIFIED: objects365.org could not be reached in this pass]` | pin the version, because the paper's counts and later headline counts differ; using it as extra pretraining data breaks comparability with arms that did not, which is the `det` calibration threshold in [../../cse-shared/core/evidence-integrity.md](../../cse-shared/core/evidence-integrity.md) | state-of-the-art detection quality on its own, because it is usually a pretraining corpus rather than the evaluation target |
| DOTA v1.0, v1.5, v2.0 | Large-scale aerial detection with oriented boxes. v1.0: 2,806 images, 188,282 instances, 15 categories (arXiv:1711.10398). v2.0: 11,268 images, 1,793,658 instances, 18 categories, adding container crane, airport and helipad (arXiv:2102.12219). v1.5 has 16 categories, adding container crane and very small instances `[UNVERIFIED: v1.5 instance count]`. The dataset page lists images from Google Earth, the GF-2 and JL-1 satellites via the China Centre for Resources Satellite Data and Application, and CycloMedia aerial imagery | the official page states that the v1.0 images were re-annotated for v2.0 and that v2.0 is distributed as the v1.0 images plus extra images, so evaluating v2.0 with v1.0 annotations is wrong; the page restricts use to academic purposes and prohibits commercial use; images are large, so tiling creates a leakage risk when tiles of one scene fall on both sides of a split; the `difficult` flag changes reported numbers | performance on non-aerial imagery; anything about real-time operation, since the images are large and processed offline |
| VisDrone (DET and MOT subsets) | Drone imagery from the AISKYEYE team, Tianjin University. The README describes VisDrone2019: 288 video clips with 261,908 frames plus 10,209 static images, more than 2.6 million boxes, captured by various drone platforms across 14 cities in urban and rural settings at sparse and crowded densities; the challenge has five tasks (image detection, video detection, single-object tracking, multi-object tracking, crowd counting) | the README states that test-dev annotations are available for publication use while testset-challenge annotations are not, so name the split exactly; the counts are for the 2019 release, so name the release; the data come from several drone models, so a claim about one platform does not follow | performance on satellite or high-altitude imagery, which has a different scale distribution; anything about a fixed camera |
| UAVDT | A UAV benchmark for detection, single-object tracking and multi-object tracking. The paper (arXiv:1804.00518) states that about 80,000 representative frames were selected from 10 hours of raw video and annotated with boxes and up to 14 kinds of attributes (weather condition, flying altitude, camera view, vehicle category, occlusion and others) | attribute annotations make subset evaluation easy and subset cherry-picking equally easy, so declare the subset rule in advance; the frame count is approximate in the paper, so do not present it as exact | pedestrian performance, since it targets vehicles; performance outside the recorded weather and altitude envelope |

Related options worth naming when the claim needs them: `xView` and `DIOR` for satellite detection,
`COCO-C` / `Pascal-C` style corruption benchmarks for robustness claims, and `Cityscapes` for
driving scenes `[UNVERIFIED: none of these was read in this pass]`. Any corruption benchmark measures
sensitivity to the chosen corruption set and severity levels, not robustness in general.

## `track` tracking benchmarks

| Benchmark | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| MOT17 | Multi-object pedestrian tracking. The archived MOT17 page lists 7 training and 7 test sequences, each provided with three public detection sets (DPM, Faster R-CNN, SDP), which is why its tables show 21 training and 21 test entries. The MOT16 paper (arXiv:1603.00831), on whose sequences MOT17 builds, documents the annotation protocol: pedestrians are the evaluated targets, "distractors" such as sitting people, reflections and people behind glass are neither penalised nor rewarded, vehicles and occluders are annotated for training and occlusion level, and per-object visibility is provided | the **public versus private detection protocol** is the whole comparability question: in the public protocol the tracker consumes the supplied detections, in the private protocol it runs its own detector, and mixing the two is the most common unfair comparison on this axis. Count sequences consistently (7 unique, or 21 detector variants) and name the detector set. The MOT16 paper also notes that the IoU matching threshold used by papers varied, which changes the numbers; name the evaluator and its version | anything about appearance-free tracking, because the sequences favour discriminative appearance, which is the bias DanceTrack was built to expose |
| MOT20 | Very crowded pedestrian scenes (arXiv:2003.09003). The archived page lists 8 sequences, 4 training and 4 test: training has 8,931 frames and 1,336,920 boxes at a mean of 149.7 people per frame, test has 4,479 frames and 765,465 boxes at 170.9 | density changes the occlusion statistics, so a method tuned on MOT17 does not transfer without stating the difference; detector provenance and online or offline must be declared as for MOT17 | sparse-scene performance, and any claim that generalizes across density regimes without a per-benchmark result |
| DanceTrack | Multi-human tracking where appearance is deliberately not discriminative (arXiv:2111.14690): people with similar appearance, diverse motion and extreme articulation, mostly from group-dance videos. The project page lists 100 videos split 40 train, 25 validation and 35 test; the paper's Table 1 gives 105,855 frames; test annotations are private and evaluated through a CodaLab competition linked from the project page | an appearance-dependent method will look weak here, and that is the intended signal, so report it rather than switching benchmark; numbers are not comparable to MOT17 numbers because the sequence statistics differ; check the competition server's current status before planning a test submission | pedestrian tracking in surveillance conditions, and identity preservation under appearance ambiguity outside dance footage |
| KITTI tracking | 2D box tracking in driving scenes. The benchmark page states 21 training and 29 test sequences, 8 labelled classes of which Car and Pedestrian are evaluated, stereo colour and grayscale images, Velodyne point clouds, GPS/IMU and calibration, with reference detections supplied | HOTA became the main metric in the 25 February 2021 update, with CLEAR MOT and MT/PT/ML also reported, so older MOTA-ranked numbers are not comparable with later rankings; only objects taller than 25 pixels are evaluated; Vans are not counted as false positives for Car and sitting persons not for Pedestrian; the test split requires registration, and the page restricts submissions to work leading to a peer-reviewed paper | pedestrian-dense tracking; anything about non-driving scenes; end-to-end speed, because the reported runtime excludes detection time |
| VisDrone MOT | see the `det` table; the same platform and split caveats apply, plus detector provenance | test-dev annotations are available while testset-challenge annotations are not; detector provenance is unstated in many papers | driving-scene tracking |

Service status. On 2026-10-03, motchallenge.net returned HTTP 410 with a notice that the service is
offline: the website, evaluation server, submissions and accounts are not operating, the dataset
archives remain available, and the leaderboards are preserved as a static snapshot (state of
16 April 2026). A plan that needs a new MOTChallenge test-set evaluation needs another route, and a
claim about "the MOTChallenge leaderboard" needs the snapshot date. Re-check the status at the moment
of use.

## `reid` re-identification benchmarks

| Benchmark | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| Market-1501 | Person re-identification across cameras with DPM-detected boxes. The ICCV 2015 paper page states more than 32,000 annotated boxes plus a distractor set of more than 500,000 images; the MSMT17 paper's comparison table lists 1,501 identities, 32,668 boxes and 6 cameras. The standard split is usually quoted as 751 training and 750 test identities with 3,368 queries `[UNVERIFIED: read the split table in the paper]` | re-ranking on or off changes the numbers substantially and is the classic one-arm-only unfairness; single-query and multi-query are different protocols; the distractor set must be treated identically across arms | cross-domain generalization, since it is usually the training source; vehicle re-identification |
| MSMT17 | Large-scale person re-identification. The paper (arXiv:1711.08565v2) states 4,101 identities and 126,441 boxes from 15 cameras (12 outdoor, 3 indoor) over a long period with complex lighting; training uses 1,041 identities with 32,621 boxes and test 3,060 identities with 93,820 boxes, split into 11,659 queries and 82,161 gallery images | the paper's own baselines are entangled with its GAN-based transfer method, since it reports the domain-gap drop that method addresses; resolution and crop policy differ from Market-1501, so cross-dataset comparisons need per-dataset protocols | performance on a small camera network, and deployment conditions beyond the recorded cameras |
| DukeMTMC-reID | Person re-identification derived from the DukeMTMC multi-camera dataset, whose paper (arXiv:1609.01775) describes 8 synchronized 1080p cameras at 60 fps, more than 2 million frames and more than 2,700 identities over 85 minutes | **the source dataset was withdrawn by Duke in 2019 and is no longer distributed** `[UNVERIFIED: the exposing.ai analysis cited in earlier versions returned HTTP 404 on 2026-10-03; cite a current source for the withdrawal]`. The re-ID derivative uses a subset of the identities, so do not quote the source paper's identity count for it. Do not build a new result on it, do not present it as available, and state the withdrawal when a baseline number is quoted | anything going forward, because it cannot be ethically or practically re-obtained |
| VeRi-776 | Vehicle re-identification in urban surveillance. The VeRi page states over 50,000 images of 776 vehicles from 20 cameras covering about 1.0 km^2 over 24 hours, with each vehicle seen by 2 to 18 cameras and labels for boxes, type, colour and brand; licence plates are no longer distributed for privacy reasons, and access is by request for non-commercial use. The common split is usually quoted as 576 training and 200 test vehicles with 1,678 queries `[UNVERIFIED: read the split in the ECCV 2016 paper]` | viewpoint variation dominates vehicle appearance, so results do not transfer from person re-identification; image counts differ slightly between papers, so cite the version used | person re-identification, and large-scale vehicle retrieval |
| VehicleID | Vehicle re-identification at larger identity scale. The PKU page states 26,267 vehicles in 221,763 images captured in daytime by surveillance cameras in a small city in China, with model labels for 10,319 vehicles (90,196 images); academic use only, under a signed agreement. Test subsets are usually quoted as small, medium and large with 800, 1,600 and 2,400 identities `[UNVERIFIED: read the subset table in the CVPR 2016 paper]` | reporting the best of several test subsets without naming it is a selection effect; the subsets are not interchangeable | cross-camera protocol behaviour equivalent to Market-1501, and anything about non-vehicle objects |
| CUHK03 | Person re-identification with hand-drawn `labeled` boxes and automatically `detected` boxes for 1,467 identities, each seen in two disjoint camera views, as listed in the MSMT17 and re-ranking papers (the original 2014 paper is not read here). The re-ranking paper (arXiv:1701.08398) introduced the widely used protocol with 767 training and 700 test identities; the original protocol used repeated random splits with 100 test identities | comparing a `labeled` result against a `detected` result is the crop-policy unfairness in the `reid` calibration row; name the protocol (original or 767/700) and the box type for every number, since image counts also differ between releases | deployment performance under real detector noise unless the `detected` setting is used |

General rule for this axis. A re-identification number is a tuple, not a scalar: backbone and
pretraining, input resolution and crop policy, re-ranking status, query mode, and the dataset split
and protocol version. A comparison table that omits one of those columns is not a comparison.

## `cnav` cooperative-navigation datasets

This axis has no single dominant public benchmark, and that is itself the finding. Claims here are
usually supported by a custom simulation plus, where the venue demands it, a hardware demonstration.
Only the first three rows were read at a primary source in the verification pass.

| Resource | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| UTIAS MR.CLAM (multi-robot cooperative localization and mapping) | The dataset page describes five iRobot Create ground robots in an indoor 15 m by 8 m area, each with a monocular camera giving range and bearing to barcode-labelled landmarks and to the other robots, plus odometry, with ground truth for robots and landmarks from a 10-camera Vicon system; cite Leung et al., IJRR 2011 | the official dataset page lists 9 datasets while the lab's dataset index says 8, so name the files used; motion-capture ground truth means an indoor, controlled setting; the team size and arena are fixed | outdoor or GNSS-denied operation, large teams, aerial platforms |
| S3E | A collaborative SLAM and localization dataset from **three unmanned ground vehicles**, not UAVs. Version 8 of the paper (arXiv:2210.13723v8, 2024) and the project page describe 18 sequences (13 outdoor, 5 indoor) with 16-beam 3D LiDAR, stereo cameras, a 9-axis IMU, UWB inter-robot ranges and RTK GNSS; version 1 (2022) described 12 sequences without UWB | ground truth is RTK and GNSS/INS post-processing outdoors, while indoors motion capture covers only the start and end of trajectories in the laboratory, so indoor accuracy claims must say which segments have ground truth; cite the version used | aerial cooperation, and continuous indoor ground truth |
| EuRoC MAV | Visual-inertial estimation on one micro aerial vehicle, with ground truth from a Vicon system in one environment and a laser tracker in another `[UNVERIFIED: sequence count and ground-truth details; the paper and dataset page were not reachable in this pass]` | widely used for `filt` and single-agent estimation, so it is mis-cited as a cooperative benchmark | multi-agent cooperation, inter-agent ranging, communication effects |
| GrAco and Kimera-Multi data | GrAco pairs one ground vehicle and one UAV outdoors; the Kimera-Multi data come from a team of ground robots. Both are listed in the S3E paper's comparison table as having no UWB inter-agent ranging `[UNVERIFIED: secondary description only; read each dataset's own paper]` | without inter-agent ranging, they support collaborative mapping or relative pose from vision and LiDAR, not range-based cooperative localization | range-only cooperative localization |
| Custom simulation | whatever the author defines | the dominant trap of the axis: a simulation whose noise model, communication delay, packet loss, ranging outlier model and topology were chosen by the author, compared against a baseline given a different model. This is the `cnav` calibration row in [../../cse-shared/core/evidence-integrity.md](../../cse-shared/core/evidence-integrity.md) | field validity. A simulation result is a `simulation` result |

The "GRASP multiple micro-UAV" work is a testbed paper (Michael, Fink and Kumar, IEEE Robotics and
Automation Magazine, 2010), not a released benchmark dataset; do not cite it as one.

For any `cnav` result, the protocol block in
[protocol-blocks.md](../../cse-experiment-suite/references/protocol-blocks.md) applies, together with
the `cnav` addendum in [gate-contract.md](../../cse-shared/core/gate-contract.md). It must state which
nodes compute, what is exchanged, whether any central node or global state exists, and the
communication model with delay and loss. Without that block the number is not interpretable.

## `filt` filtering and estimation scenarios

These are classic scenarios rather than datasets. The references named below are the commonly cited
sources; their exact equations, parameters and section locators were not read in the verification
pass `[UNVERIFIED]`, so transcribe the scenario from the paper you cite and state every parameter.

| Scenario | What it measures | Protocol trap | Cannot establish |
|---|---|---|---|
| Bearings-only tracking | a nonlinear problem where one sensor measures only bearing, so observability depends on the own-ship manoeuvre; classic references include Nardone and Aidala (1981) and Aidala and Hammel (IEEE TAC, 1983), and Ristic, Arulampalam and Gordon (2004) for particle-filter treatments | the manoeuvre profile is part of the problem definition, and a filter tuned per scenario is not a filter; the initialization error dominates the early RMSE, so the initialization must match across arms | performance under a different sensor suite, and anything about the estimate while the geometry is unobservable |
| Reentry-vehicle tracking | a highly nonlinear tracking problem with a very informative measurement late in the trajectory, going back to Athans, Wishner and Bertolini (IEEE TAC, 1968) and used by Julier and Uhlmann (Proc. IEEE, 2004) | the near-singular geometry makes results sensitive to numerical implementation and to sigma-point or particle settings, so a small implementation difference can dominate the comparison | general filtering quality, because it is an extreme case; steady-state behaviour |
| Univariate nonstationary growth model | a scalar benchmark with a multimodal posterior, commonly attributed to Kitagawa (1987) and popularized for particle filters by Gordon, Salmond and Smith (IEE Proc. F, 1993) | variants differ in noise variances and in the time index of the cosine term, so print the exact equations; because it is cheap, it is often run with too few Monte Carlo runs to resolve the tails it is chosen for | multi-dimensional behaviour, and a Gaussian NEES consistency check, because the non-Gaussian posterior is what invalidates that check |
| Author-supplied target-tracking scenarios | whatever the paper needs | the `filt` calibration row: per-filter hand tuning for the proposed method only, different Monte Carlo counts, different initialization error, and noise covariance mismatch applied to the baseline only | anything beyond the scenario envelope |

Required evidence for this axis is set by the `filt` fields of
[protocol-blocks.md](../../cse-experiment-suite/references/protocol-blocks.md) and the `filt`
addendum in [gate-contract.md](../../cse-shared/core/gate-contract.md): the Monte Carlo count, NEES or
ANEES against chi-square bounds computed as in
[terminology-and-notation.md](../../cse-shared/core/terminology-and-notation.md), and the numeric
bounds used. Bar-Shalom, Li and Kirubarajan (2001) is the standard textbook treatment of these
consistency tests `[UNVERIFIED: section locator]`. The pack minimum is 100 Monte Carlo runs for
accuracy and consistency claims. A single trajectory is not a statistical result.

## How to read this atlas

1. Pick the benchmark whose failure mode matches the claim's failure mode, not the most popular one.
2. Write the protocol block for the axis before running anything, using
   [protocol-blocks.md](../../cse-experiment-suite/references/protocol-blocks.md).
3. Write the "cannot establish" column into the limitations section in advance. It is the cheapest
   and most credible honesty in the paper.
4. Confirm every count, split, version, licence and service status at the primary source before it
   appears in a manuscript. Even a value stated here was read at one version on one date.
