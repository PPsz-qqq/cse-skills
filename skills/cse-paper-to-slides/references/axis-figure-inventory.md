# Axis figure inventory

The figures and demos that carry a talk on each axis, which of the paper's figures to reuse, and
what to regenerate. Open this when building the `Method` and `Results` slides, whose visuals decide
whether the audience follows the argument.

Each entry names the figure, what it must show, and the presentation-specific requirement that
differs from the paper.

## det, object detection

| Slide role | Figure | What it must show | Presentation requirement |
|---|---|---|---|
| Task | detection examples with boxes | the objects, the box convention, the image scale | four examples at most, each large enough that a box is visible at 4 metres |
| Gap | failure of the prior method | the specific failure mode, annotated | one panel, with the failure circled. A two-panel figure without annotation is not a gap figure |
| Method | architecture overview | input, backbone, the new component, the prediction heads | readable left to right, with the new component visually dominant. Regenerate if the paper's version buries it |
| Method detail | the new component | the mechanism and its tensor shapes | three equations maximum on the slide. Move the rest to backup |
| Results | main comparison table | the metric, the protocol, the comparison arms | reduce to 5 to 7 rows. Every arm carries its resolution and backbone in a header note |
| Results | qualitative comparison | ours against the strongest baseline on the same images | identical crops, identical zoom, side by side. Never a different test image per column |
| Scale behaviour | `AP_S` / `AP_M` / `AP_L` | where the gain comes from | a grouped bar chart reads better than the paper's table |
| Failure | missed and false detections | small objects, occlusion, unusual aspect ratio | label the failure mode on each panel |
| Backup | PR curve or per-class AP | the distribution behind the mean | only if the audience for this venue asks per-class questions |
| Backup | throughput and memory | latency on the named device at the stated batch size | state the device and the batch size on the slide |

Demo, when the venue allows it. A live detector on a video clip is the strongest single minute
available on this axis, and the risk is that it fails. Pre-record it. A recorded clip that plays
reliably beats a live demo that stutters, and if the live demo is kept, have the recording one
keystroke away.

## track, object tracking

| Slide role | Figure | What it must show | Presentation requirement |
|---|---|---|---|
| Task | a sequence with identity-coloured trajectories | who is who over time, and the trajectories | use a short clip rather than a still. Identity colour must be consistent across frames |
| Gap | identity switches in the prior method | the switch, annotated with the frame number | one clip or three stills with the switch framed. An unannotated trajectory plot does not show a switch |
| Method | the pipeline, detector to association to output | the detector is external or joint, and the association step | state public or private detection on the pipeline figure itself, since the audience will ask |
| Method detail | the association mechanism | the cost, the assignment, and the new term | one equation for the assignment objective, then a diagram of the term |
| Results | `HOTA` with `DetA` and `AssA` | whether the gain is detection or association | show `HOTA` split. A `MOTA`-only slide invites the wrong question and cannot answer it |
| Results | the error breakdown | identity switches, fragmentations, false positives | a stacked bar per method |
| Qualitative | the sequence the baseline loses on | the specific moment of divergence | clip, with both methods playing side by side if the venue's tooling allows |
| Failure | where the tracker loses identity | crowd, long occlusion, similar appearance | label the cause on each example |
| Backup | per-sequence results | the variance across sequences | needed whenever the dataset has heterogeneous sequences |
| Backup | FPS with the device and batch size | whether it is real time | state the device, the batch size, and whether detection time is included |

## reid, re-identification

| Slide role | Figure | What it must show | Presentation requirement |
|---|---|---|---|
| Task | a query and the ranked gallery | the retrieval setting, and what a correct match means | a query image plus the top 5 ranked results, with correct matches marked |
| Gap | the failure case of the prior method | a hard positive the baseline misses, such as the same person in different clothing | annotate why it is hard. The audience must see the difficulty without being told |
| Method | the feature-learning architecture | the backbone, the embedding, the new loss or module | state the input resolution on the figure, since it is a protocol field the audience checks |
| Method detail | the new loss or attention mechanism | the mechanism, not the formula alone | show the effect on a t-SNE plot or a similarity matrix beside the formula |
| Results | `mAP` and `Rank-1` table | both metrics, with the protocol | state re-ranking on or off in the header. A re-ranked row beside a non-re-ranked row is the question that sinks a talk |
| Results | the retrieval ranking, ours against the baseline | the visible difference in ranking quality | identical gallery, identical query, side by side, with the rank position labelled |
| Embedding structure | t-SNE or UMAP of the embedding | cluster separation before and after | label the identities in the legend. An unlabelled t-SNE is decorative |
| Failure | the queries the method still fails | similar appearance, low resolution, occlusion | label the difficulty class |
| Backup | cross-dataset transfer | whether the method generalizes | needed whenever the talk claims generalization |
| Backup | the evaluation protocol block | query and gallery construction, camera exclusion | dense by design. This slide settles disputes |

Ethics note. Person re-identification decks use imagery of identifiable people. Check the venue's
policy and the dataset licence before showing faces, and prefer the dataset's own published examples
where the policy is unclear.

## cnav, cooperative navigation

| Slide role | Figure | What it must show | Presentation requirement |
|---|---|---|---|
| Task | the multi-agent scenario | the agents, the environment, GNSS availability | show the topology and the communication links on the same figure, since both are protocol fields |
| Gap | what a centralized or perfect-communication solution requires | the central node, or the bandwidth | this figure is the argument for the paper. Make it explicit |
| Method | the distributed algorithm | which node computes what, and what is exchanged | draw the computation location on the figure. The audience will ask whether it is truly distributed |
| Method detail | the estimator or the consistency mechanism | the update, and where information crosses agents | one equation for the update, then a diagram of the exchange |
| Results | position error over time, or RMSE per agent | the accuracy against the baselines | state the run count and show the dispersion band. A single trajectory is not a result |
| Results | communication cost | bytes or messages per step, against the baselines | a grouped bar chart. This is the axis where the efficiency claim lives |
| Results | topology sensitivity | performance against agent count or connectivity | a line chart with the algebraic connectivity on the secondary axis if it varies |
| Failure | where the method degrades | agent dropout, communication loss, poor initialization | a scenario table beats a single anecdote |
| Backup | the simulation-to-field gap statement | what was simulated and what was measured | mandatory when any hardware is involved |
| Backup | the Monte Carlo setup | run count, seed policy, scenario generator | needed whenever the audience asks about significance |

Demo video. A multi-robot or swarm video is the most persuasive artifact on this axis and the most
expensive to produce. If the paper has field data, use the field footage and state the platform. If
it has simulation only, present the simulation as a simulation, clearly, on the slide itself.

## filt, filtering and state estimation

| Slide role | Figure | What it must show | Presentation requirement |
|---|---|---|---|
| Task | the estimation problem | the state, the measurements, the noise sources | a block diagram with the symbols from the paper, not new ones |
| Gap | the failure of the standard filter | divergence, bias, or inconsistency | show the error curve diverging, not a table. The visual is the argument |
| Method | the estimator structure | the prediction and update, and the new element | keep the symbol set identical to the manuscript. Notation drift between slide and paper is the common defect here |
| Method detail | the new mechanism | the derivation's key step, not the full derivation | one equation with the step's intuition beside it |
| Consistency | `NEES` or `ANEES` against its bounds | the statistic, the chi-square bounds, and the run count | shade the bounds on the plot. An `ANEES` number without the bounds is not evidence |
| Results | error curves against the baselines | accuracy over time or over an error range | shaded dispersion bands, and the run count in the caption |
| Results | `RMSE` table with units and frame | the comparison under one protocol | state the initialization and the covariance assumption in the header |
| Bound comparison | error against the Cramer-Rao or covariance bound | how close the estimator runs to its bound | a log-scale plot if the range is wide |
| Failure | where the filter degrades | non-Gaussianity, outliers, model mismatch | label the violated assumption on each panel |
| Backup | the assumption list and where each is used | whether the proof's hypotheses hold in the experiment | dense by design |
| Backup | runtime per step | whether it is deployable in real time | state the processor and the step size |

## Cross-axis figures

| Slide role | Figure | Notes |
|---|---|---|
| Contribution map | a one-slide diagram linking each contribution to the experiment that establishes it | useful at a defense, and useful at a venue where the audience is broad |
| Ledger summary | the claim-to-evidence table, reduced | a backup slide that settles protocol challenges |
| Related-work timeline | the near-miss list from the novelty search | only for a defense or a venue that asks about novelty directly |
| Reproducibility | code, configs, seeds, dataset instructions | a text slide with the repository link, shown at the end of a defense |
| Compute disclosure | hardware, run count, total GPU-hours | increasingly expected, and always safer to show than to be asked for |

## Figure inventory discipline

Record the inventory for the deck in the outline, one line per visual.

```markdown
| Slide | Source | Action | File | Script | Ledger rows |
|---|---|---|---|---|---|
| S6 | paper Fig. 2 | reuse | fig/fig2-cnav-topology.pdf | - | - |
| S9 | paper Table 2 | regenerate | fig/slide9-main-results.png | fig/slide9-main-results.py | C1, C2 |
| S10 | paper Fig. 4(a) | regenerate, one panel only | fig/slide10-ablation.png | fig/slide10-ablation.py | C5 to C8 |
```

Columns: `Action` is `reuse` or `regenerate` or `reuse with the stated modification`. Every
regenerated figure has its script beside it. Every visual in the deck appears in this table, so a
reviewer of the talk can find the source of any picture on any slide.

When a figure must be regenerated and the plotting script does not exist, that is a finding to
report rather than a problem to work around. The paper's figure contract requires a generating
script, so a missing script is a reproducibility gap that belongs in the ledger, and the slide can
still be built with the paper's figure scaled to fit.
