# Per-axis writing guides

What reviewers in each axis expect, the figures and tables they look for, the page budget that
usually fits, and the phrasing that gets a paper rejected in that community. Venue classes and the
review-criteria weightings refer to
[venue-matrix.md](../../ctrl-shared/core/venue-matrix.md) and
[review-rubrics.md](../../ctrl-shared/core/review-rubrics.md).

Common to all five. State the protocol next to the number. Label simulation and field evidence.
Give dispersions. Keep the notation set of
[terminology-and-notation.md](../../ctrl-shared/core/terminology-and-notation.md). A reviewer who
cannot find the protocol assumes it is unfavorable.

## `det` object detection

**Reviewers.** Vision and pattern-recognition reviewers, plus remote-sensing reviewers when the
imagery is aerial or satellite. Class A rejects on perceived novelty first, then on an unfair or
thin comparison, then on a missing ablation.

**What they expect.** A mechanism described precisely enough to re-implement, with the assignment
rule, the loss, and the head structure named rather than gestured at. A comparison table where the
resolution, the TTA, and the backbone capacity class are visible per row, because those are the
levers that move AP most. Ablations for every claimed component under one protocol, including the
pairs claimed complementary. Per-class and per-size-bucket results where the claim touches a class
or a scale. A failure case, and for remote sensing the spatial separation rule between splits.

**Standard figures and tables.**

| Item | Content |
|---|---|
| Figs. 1 to 3 | mechanism diagram showing what is different, qualitative detections with a labeled failure panel, and the key ablation as a plot |
| Tables 1 to 4 | main comparison with protocol columns, ablation with singleton arms, per-class or per-size-bucket breakdown, and cost with the device named |

**Page budget.** Class A conference papers typically hold six to eight body pages plus references,
with the method at about a third, the experiments at about a third, and the introduction, related
work, and conclusion sharing the rest. Remote-sensing journal papers run longer with a larger
dataset-description and split-construction section.

**Phrasing that gets rejected.**
- `mAP 45.2` with no dataset, no averaging convention, and no IoU range.
- A resolution or TTA advantage presented as a method advantage.
- `Our module captures richer features` with no measurement of the feature property claimed.
- An ablation where the baseline is weaker than any published version of it, or a remote-sensing
  result with no statement of how tiles were separated between splits.

## `track` multi-object tracking

**Reviewers.** Vision and robotics reviewers. They check the detector first, because most of the
metric variance in tracking-by-detection comes from detections rather than association.

**What they expect.** Detector provenance with a checkpoint identity and an explicit public or
private detection protocol. An explicit online or offline setting, with every use of future frames
disclosed. `HOTA` with `DetA` and `AssA` separated, so a detection gain is not reported as an
association gain. Throughput with the exact GPU, the batch size, the timed region, and the repeat
count. A per-sequence breakdown, including the sequences where the method loses.

**Standard figures and tables.**

| Item | Content |
|---|---|
| Figs. 1 to 3 | pipeline with the association step highlighted, two sequence excerpts one with an identity switch marked, and `AssA` against `DetA` |
| Tables 1 to 4 | main comparison with detector and setting columns, association and motion ablation reporting `AssA` and `IDSW`, per-sequence metrics, and throughput with the GPU and timed region |

**Page budget.** Conference papers typically six to eight body pages. Reserve two pages for the
main comparison and the per-sequence table, and keep the tracker description under one and a half
pages unless the association mechanism is the contribution.

**Phrasing that gets rejected.**
- A `MOTA` with no detector, no public or private label, and no online or offline label.
- `real-time` with no GPU, no batch size, and no statement of whether detection is included.
- An association claim supported by a `MOTA` gain where `AssA` is flat, detections regenerated per
  arm so a tracker difference is really a detector difference, or an offline method described as
  `practical for online deployment`.

## `reid` re-identification

**Reviewers.** Vision and retrieval reviewers. They look for protocol discipline before they look
at numbers, because re-ranking, resolution, and query construction move the metrics more than most
method changes.

**What they expect.** The evaluation protocol block in the table itself, covering backbone and
pretraining, resolution and crop policy, re-ranking status, query and gallery construction, and
single or multi query. `mAP` and `Rank-1` together with the query count. `CMC` curves where the
ranking depth matters, and `mINP` if used, with its definition. Retrieval examples with the
true-match rank shown, including failures. The test-time path described separately from the
training path.

**Standard figures and tables.**

| Item | Content |
|---|---|
| Figs. 1 to 3 | feature-extraction and training scheme with the sampled batch composition, `CMC` curves with the ranking depth visible, and top-5 retrieval examples with the true-match rank annotated |
| Tables 1 to 4 | main comparison with re-ranking, query mode, and test resolution columns, ablation of sampling and losses, cross-dataset evaluation with the domain gap, and cost |

**Page budget.** Conference papers typically six to eight body pages. Allocate a full column to the
protocol table, because reviewers check it and a compressed version loses the fields they need.

**Phrasing that gets rejected.**
- `mAP` without saying whether re-ranking was applied.
- An arm with re-ranking compared against an arm without it.
- Multi-query results compared against single-query results from another paper.
- A Rank-1 gain on a small query set with no query count shown, or a self-built split that overlaps
  the training identities described as the official protocol.

## `cnav` cooperative navigation

**Reviewers.** Robotics, control, and navigation reviewers. Class B rejects on unstated
assumptions, a straw-man baseline, and simulation-only results dressed as system claims.

**What they expect.** A node distribution proof showing which agent computes what, what each message
carries, and whether any node holds global state, since reviewers look for the hidden central step. A
communication model with delay and loss applied to every arm, plus the message budget in bytes per
agent per step counted identically across arms. Per-node results with the worst node visible, because
a formation fails at its worst node. The scaling behaviour over `N` and the `N` range over which the
benefit holds. The dead-reckoning arm and the centralized bound, labeled as a bound. Simulation and
field results labeled separately, with the platform, sensors, and site for field results.

**Standard figures and tables.**

| Item | Content |
|---|---|
| Figs. 1 to 4 | scenario and communication topology with lambda_2 and the update schedule, per-node position error against time with the operational limit drawn, error against communication cost, and scaling over `N` with the valid range marked |
| Tables 1 to 4 | main comparison with architecture, exchange, delay, loss, and node-count columns, per-node RMSE with the worst node visible, ablation with the message budget priced per arm, and field results with platform and conditions |

**Page budget.** Robotics conference papers typically six to eight pages with a hardware section;
journal papers run longer. Control-venue theory papers invert the emphasis, with the analysis
dominant and the simulation illustrative at about a quarter of the length.

**Phrasing that gets rejected.**
- `distributed` for a method whose update needs a global quantity computed somewhere.
- `robust to communication constraints` with no delay or loss model and no message count.
- A fleet-mean RMSE with no per-node breakdown, or a field claim supported only by simulation.
- `the proposed method converges` with one trajectory shown and no distribution over runs, or a
  centralized reference entered as a distributed competitor in the main table.

## `filt` filtering and state estimation

**Reviewers.** Estimation, signal-processing, and control reviewers. In this class, consistency and
bound checks are first-class evidence, not supplementary material.

**What they expect.** The process and measurement models as implemented, with the nonlinearity
identified and the linearization region stated. `Q_k` and `R_k` per arm, with how they were obtained
and no per-arm hand tuning that favors the proposed estimator. The Monte Carlo count, identical
across arms, and the trajectory protocol. `NEES` or `ANEES` against explicit chi-square bounds, with
`n_x`, the confidence level, whether the test is one-sided or two-sided, the number of samples
averaged, and the degrees of freedom the bounds were taken at, which is `N * T * n_x` for an average
over `N` runs and `T` time steps, per
[terminology-and-notation.md](../../ctrl-shared/core/terminology-and-notation.md). `RMSE` and
consistency reported together, since a filter can be accurate and inconsistent. A `CRLB` or posterior
`CRLB` plotted as a bound and never entered as a baseline. Sensitivity to covariance
mis-specification where robustness is claimed, with the mis-specification class named.

**Standard figures and tables.**

| Item | Content |
|---|---|
| Figs. 1 to 4 | estimation architecture with update ordering, one illustrative trajectory with its covariance envelope labeled illustrative, `ANEES` against time with the chi-square bounds drawn, and `RMSE` per component against the `CRLB` on the arms' axes |
| Tables 1 to 4 | main comparison with `N`, the covariance policy, and the initialization error, accuracy and consistency together with bounds and verdict, ablation reporting both `RMSE` and consistency, and the mis-specification sweep |

**Page budget.** Control-theory journal papers run long, with assumptions and proofs occupying
several pages and simulations about a quarter. Letters and conference papers compress the
illustrations but must keep the consistency table, because it is the evidence for the central
claim in this class.

**Phrasing that gets rejected.**
- An `ANEES` value with no bounds, no `n_x`, and no sample count, or a consistency claim from one
  trajectory.
- True `Q_k` and `R_k` given to the proposed filter while the baseline keeps mis-specified values,
  presented as an accuracy advantage.
- A covariance retuned after seeing the consistency result with the sequence undisclosed, a `CRLB`
  entered as a baseline, `the filter is robust` with no perturbation class, or a proof of the main
  property deferred to an appendix that does not close the hard case.

## Cross-axis checks before submitting

```text
[ ] The axis-critical protocol labels travel with the numbers, in the tables
[ ] The nearest competitor for this axis is named and precisely differentiated
[ ] The figures and tables a reviewer in this axis expects are present
[ ] The page budget matches the venue's limit, verified against the current call
[ ] The failure case exists and is discussed
[ ] The evidence class of every result is labeled, simulation or field
[ ] The terminology matches ctrl-shared terminology-and-notation, in both languages
[ ] No phrasing from the rejection lists above appears anywhere in the manuscript
```
