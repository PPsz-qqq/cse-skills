# Axis concern taxonomies

What actually gets a paper rejected on each of the five axes. Use this as a coverage checklist
while reviewing, never as a quota. A checklist that must be filled produces invented concerns, and
invented concerns destroy the review's value.

Each entry states the concern, the pointer a reviewer must be able to produce, and the severity it
usually carries. Severity is set by impact on the manuscript's case, so an entry can move down if
the manuscript has already handled it and up if the defect damages the central claim.

Read the entries for the primary axis in full, plus the entries for each secondary axis.

## det, object detection

| # | Concern | Pointer required | Usual severity |
|---|---|---|---|
| det-1 | Comparison arm differs in input resolution, pretraining data, augmentation, or test-time augmentation | the protocol block for both arms, in the manuscript or the config files | Blocking when it carries the headline delta, Major when it is a secondary row |
| det-2 | COCO `val` for one arm against `test-dev` for another, or a local split compared with a public leaderboard entry | the evaluation split named for each arm | Blocking |
| det-3 | Backbone or pretraining data undisclosed, so the gain cannot be separated from a stronger backbone | backbone name, pretraining corpus, and parameter count | Major |
| det-4 | Pretraining on data that overlaps the evaluation set, including a detector pretrained on COCO when COCO is the benchmark | pretraining corpus and its relation to the test set | Blocking, and it is an integrity issue rather than a rigor issue |
| det-5 | Single seed presented as a stable accuracy claim | number of runs and dispersion | Major, Blocking if the claimed margin is inside the observed spread |
| det-6 | NMS policy, score threshold, or maximum-detections setting differs between arms or is unstated | inference config | Major |
| det-7 | Small-object or scale claim with no `AP_S` / `AP_M` / `AP_L` breakdown and no resolution ablation | the per-scale table | Major |
| det-8 | Efficiency claim with no parameter count, FLOPs on a stated input size, and latency on a named device with a stated batch size | the efficiency table | Major |
| det-9 | "State of the art" asserted while the comparison omits a strong same-protocol baseline | the baseline list and the omission | Major |
| det-10 | Remote-sensing split with geographic leakage, tiles from one scene in both train and test | the split construction and the spatial separation rule | Blocking |
| det-11 | Novelty claim without a documented search of recent venue cycles and the foundational line of work | the search terms, window and the near-miss list | Major, and it is a `Question` when the search itself is missing but plausible |
| det-12 | Failure cases absent, so the reader cannot see where the detector loses | a qualitative failure figure or an error analysis | Minor if the paper is otherwise strong, Major when generalization is claimed |

## track, object tracking

| # | Concern | Pointer required | Usual severity |
|---|---|---|---|
| track-1 | Public versus private detection protocol unnamed next to every tracking number | the protocol statement and the results table headers | Blocking |
| track-2 | Detector checkpoint or provenance missing in a tracking-by-detection method, so the number cannot be reproduced or compared | detector identity, training set, and confidence threshold | Blocking |
| track-3 | Online method compared with an offline method, or offline post-processing on one arm only | the setting statement for each arm | Blocking |
| track-4 | FPS reported with no GPU model, batch size, or whether detection time is included | the runtime table | Major |
| track-5 | `MOTA` reported alone for a modern tracker, where `HOTA` with `DetA` and `AssA` separates detection from association gains | the metric table | Major |
| track-6 | Association improvement claimed while the detector is also changed, so the gain is not attributable | the ablation that holds the detector fixed | Blocking when association is the contribution |
| track-7 | Identity switches reported without the matching threshold or the evaluation script identity | the metric definition and script | Major |
| track-8 | Single sequence or single dataset result generalized to the task | the dataset list | Major |
| track-9 | Long-occlusion or crowded-scene claim with no such subset evaluation | the subset definition and its results | Major |
| track-10 | Data association parameters tuned per sequence and reported as a general method | the tuning protocol | Blocking, because it is a comparison-integrity failure |
| track-11 | 3D or multi-camera tracking claim whose calibration and coordinate frame are unstated | the calibration procedure and frame definitions | Major |
| track-12 | Evaluation on a benchmark whose ground truth is the authors' own annotation, with no protocol description | the annotation protocol and the inter-annotator agreement | Blocking when the annotation is the only evidence |

## reid, re-identification

| # | Concern | Pointer required | Usual severity |
|---|---|---|---|
| reid-1 | Re-ranking applied to one arm only, or applied at all without being stated in the table | the protocol line for each arm | Blocking, since re-ranking alone can dominate the reported gain |
| reid-2 | Test resolution or crop policy differing between arms | the input block | Blocking when it carries the delta |
| reid-3 | Multi-query result compared with a single-query baseline | the query construction | Blocking |
| reid-4 | External unlabeled or weakly labeled data used for one arm only | the training-data inventory per arm | Blocking |
| reid-5 | Backbone capacity class differing between the proposed method and the baselines | parameter counts for each arm | Major |
| reid-6 | Query and gallery construction undocumented, including whether the same camera is excluded | the evaluation protocol block | Major |
| reid-7 | `mAP` and `Rank-1` reported without the number of identities or the split | the dataset description | Major |
| reid-8 | Cross-dataset or domain-generalization claim from a single target dataset | the target dataset list | Major |
| reid-9 | Occlusion, cloth-change, or vehicle-orientation robustness claimed with no such protocol | the robustness experiment | Major |
| reid-10 | Retrieval experiment presented as re-identification, with no query-gallery separation | the task definition | Major |
| reid-11 | Single-seed training result on a stochastic metric with a sub-1-point margin | runs and dispersion | Major |
| reid-12 | Privacy or ethics dimension unaddressed when the data are personal imagery | a data-handling and ethics statement | Major at a venue that requires it, otherwise Minor |

## cnav, cooperative navigation

| # | Concern | Pointer required | Usual severity |
|---|---|---|---|
| cnav-1 | A centralized solution presented as distributed, or a central node silently present | the algorithm description and the computation distribution statement | Blocking |
| cnav-2 | Perfect communication assumed for the proposed method while a baseline is evaluated under a lossy model | the communication model for each arm | Blocking |
| cnav-3 | Communication model with no delay, loss, bandwidth, or rate assumption stated | the model definition and its parameters | Major, Blocking when the contribution is communication-efficient |
| cnav-4 | Ranging or bearing noise model differing between arms, or unstated | the measurement model | Blocking when it carries the delta |
| cnav-5 | Simulation results presented as system or field results | the platform statement and the data source | Blocking, and it is an integrity issue |
| cnav-6 | Observability or convergence claim asserted without the condition that guarantees it, such as connectivity or excitation | the theorem, its assumptions, and where they are checked | Blocking for a theory claim |
| cnav-7 | Number of Monte Carlo runs below the field minimum, or no run count at all | the run count and dispersion | Major, Blocking for a consistency claim |
| cnav-8 | Agent count, topology, and graph connectivity unstated or varying only in a favorable range | the scenario table with the algebraic connectivity | Major |
| cnav-9 | Initialization error or clock synchronization assumption given only to the proposed method | the initialization block per arm | Major |
| cnav-10 | GNSS-denied claim with a short outage only, or with intermittent GNSS the method actually uses | the outage profile | Major |
| cnav-11 | Hardware claim with no platform specification, sensor calibration, or runtime on the onboard computer | the platform section | Major |
| cnav-12 | Comparison against a straw-man baseline, such as a dead-reckoning integrator presented as the state of the art | the baseline justification | Major |
| cnav-13 | Scalability claimed from three agents, or complexity stated without the exchange count per step | the scaling experiment and the per-step message count | Major |

## filt, filtering and state estimation

| # | Concern | Pointer required | Usual severity |
|---|---|---|---|
| filt-1 | Consistency claim without `NEES` or `ANEES` against its chi-square bounds, or without the bound used | the consistency table, the Monte Carlo count, and the degrees of freedom | Blocking for a consistency claim |
| filt-2 | Monte Carlo count far below the field minimum, or a single trajectory presented as a statistical result | the run count | Blocking for an accuracy claim |
| filt-3 | Noise covariance mismatch applied to the baseline only, or per-filter hand tuning of the proposed method alone | the tuning protocol and the covariance used per arm | Blocking, since it is a comparison-integrity failure |
| filt-4 | Different initialization error between arms, which usually decides the outcome in a nonlinear filter comparison | the initialization block | Blocking |
| filt-5 | Assumptions stated informally and not used in the proof, or the main theorem deferred to an appendix that does not close | the theorem, its hypotheses, and the proof chain | Blocking for a theory claim |
| filt-6 | Stability or convergence result proven for a linearized system while the claim is about the nonlinear one | the proof's model and the paper's claim | Blocking |
| filt-7 | Comparative bound claim, such as a tighter covariance bound, without a derivation or an empirical check | the derivation or the numerical comparison | Major |
| filt-8 | Nonlinearity, non-Gaussianity, or outlier handling claimed with no test under that condition | the stress experiment | Major |
| filt-9 | `RMSE` reported without units, frame, run count, or dispersion | the results table | Major |
| filt-10 | Computational cost claim without per-step complexity and measured runtime | the complexity and runtime table | Major |
| filt-11 | Real-data validation absent when the venue expects hardware evidence, with a simulation-only claim framed as deployable | the data source and the claim wording | Major, Blocking when the claim is a deployment claim |
| filt-12 | Observability or detectability discussed only qualitatively where it decides the result | the observability analysis | Major |
| filt-13 | Process and measurement models given in continuous time while the implementation is discrete, with no discretization stated | the model and the implementation step | Major if the step size matters to the result, otherwise Minor |

## Cross-axis concerns, valid on every axis

These apply regardless of axis and are the most frequent cause of a low score.

| Concern | Pointer required | Usual severity |
|---|---|---|
| The abstract claims more than the ledger supports, such as a mechanism explanation backed only by a leaderboard delta | the abstract sentence and the corresponding experiment | Blocking |
| A confirmed integrity failure under [evidence-integrity.md](../../cse-shared/core/evidence-integrity.md) rules 1, 2 or 10 | the claim and the artifact that contradicts it | Blocking, forces Reject |
| A value differs between surfaces beyond rounding, or a superlative is contradicted by the paper's own table (rule 4) | both occurrences and the arithmetic | Blocking; Reject only when it carries the central claim |
| The same value is printed at two precisions or in two units | both occurrences | Minor, Major if the rounding changes a comparison |
| A contribution claimed in the introduction has no section, table, or figure that establishes it | the contribution list and the experiment list | Blocking |
| An ablation run at a different budget from the main result, presented as an ablation | both configurations | Major |
| Limitations section that lists only future work | the section | Major |
| Negative results removed from the evaluation set after the result was seen | the evaluation-set definition and its revision history | Blocking |
| A percentage improvement with no statement of absolute or relative | the sentence | Minor |
| Novelty claimed as "the first" without a documented search | the search | Major |
| Related work that omits the closest competing paper, or describes it inaccurately | the citation and the paper | Major |
| Units, frames, or coordinate conventions missing for a physical quantity | the table or equation | Major when the quantity decides the conclusion, otherwise Minor |

## Using the taxonomies correctly

- Coverage, not quota. Walk the entries, ask whether the manuscript exhibits the defect, and record
  only the ones you can point at.
- The taxonomy does not replace the rubric. A defect that matches no entry is still a concern if it
  has a pointer.
- An entry marked Blocking is Blocking only when it damages the central case. A protocol mismatch in
  a secondary ablation is a Major finding, not a Blocking one.
- If the paper handles an entry explicitly, say so in the report. A reviewer who confirms that a
  common defect is absent is providing information, and it protects the authors against a later
  reviewer who assumes the defect is present.
