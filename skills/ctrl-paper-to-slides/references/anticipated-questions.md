# Anticipated questions

The questions each axis's audience actually asks, with the answer strategy and the backup slide that
carries the evidence. Ten per axis, then the cross-axis set.

Answer strategy is not a script. Each entry states what the answer must contain, and what a wrong
answer sounds like.

## det, object detection

| # | Question | Answer strategy | Backup |
|---|---|---|---|
| 1 | What are the input resolution and augmentation for each arm? | State both, from the protocol block. If they differ, say by how much and why, before anyone asks whether it is fair | B6 |
| 2 | Was the baseline re-trained or copied? | State reported versus re-implemented per arm. Never say "we used the published numbers" without adding the protocol differences | B6 |
| 3 | Is the gain within seed noise? | Give the run count and the dispersion. If the run count is one, say so and say what it means for the claim | B3 |
| 4 | How does it perform on small objects? | Give `AP_S`, or say the breakdown is not available and what it would require | B2 |
| 5 | What is the inference cost? | Latency on the named device at the stated batch size, plus parameter count and FLOPs at the stated resolution | B4 |
| 6 | Why does the component help? | Give the ablation and the mechanism. If the mechanism is not established, say it is an empirical finding | B1 |
| 7 | How sensitive is this to the added hyperparameter? | Give the sweep if it exists. If it does not, say the sensitivity was not characterized and name it as a limitation | B5 |
| 8 | Does this generalize to another dataset or sensor? | Give the second dataset if it exists. If not, state the boundary in the paper's own terms and do not improvise a claim | B2 |
| 9 | How is this different from the most similar recent method? | Name the mechanism difference, not the accuracy difference. Point to the near-miss list | B8 |
| 10 | Is the code available? | Give the repository, or state the release plan and the date | - |

The wrong answer to question 3 is the most common. Never answer a noise question with a confidence
tone. Answer it with the run count.

## track, object tracking

| # | Question | Answer strategy | Backup |
|---|---|---|---|
| 1 | Public or private detections? | State it immediately, for every number on the slide. Ambiguity here invalidates the comparison | B6 |
| 2 | Which detector, and which checkpoint? | Name the detector, its training set, and the confidence threshold | B6 |
| 3 | Online or offline? | State it per arm. If one arm uses future frames, say so before the follow-up | B6 |
| 4 | What is the FPS, and on what hardware? | Give the device, batch size, and whether detection time is included | B4 |
| 5 | Where does the gain come from, detection or association? | Give `HOTA` split into `DetA` and `AssA`. This is the question that decides whether the association contribution stands | B1 |
| 6 | Was the detector held fixed in the ablation? | If yes, say so and show it. If no, state the limitation, because the attribution does not hold otherwise | B1 |
| 7 | How does it behave under long occlusion? | Give the occlusion-subset result if it exists, or state that the subset was not evaluated | B2 |
| 8 | Was anything tuned per sequence? | Answer directly. Per-sequence tuning presented as a general method is a comparison failure, and hiding it is worse | B6 |
| 9 | Why not compare with the tracker that reports a higher `MOTA`? | Give the protocol difference, or the detection provenance difference, and offer the control run | B1 |
| 10 | What happens when the detector degrades? | Give the robustness experiment, or state that it was not run | B2 |

## reid, re-identification

| # | Question | Answer strategy | Backup |
|---|---|---|---|
| 1 | Is re-ranking applied? | Answer for every row on the slide. "Yes for ours, no for baselines" is the answer that ends the talk badly, so if that is the case, present it as a declared difference | B6 |
| 2 | Single-query or multi-query? | State it. Mixing them across arms makes the comparison meaningless | B6 |
| 3 | What test resolution and crop policy? | Give both, for all arms | B6 |
| 4 | Is external data used? | Name every additional dataset, per arm. Silent use of extra data is a comparison failure | B6 |
| 5 | How were query and gallery constructed? | Give the split, the identity count, and the camera-exclusion rule | B8 |
| 6 | Is the gain within seed noise? | Give runs and dispersion | B3 |
| 7 | Does this transfer to another dataset? | Give the cross-dataset result, or state the boundary | B2 |
| 8 | How does it handle clothing change or occlusion? | Give the protocol result if it exists. If not, do not claim robustness | B2 |
| 9 | What is the backbone and its parameter count, against the baselines? | Give both. A larger backbone with a modest gain is the question behind the question | B1 |
| 10 | Are the images used with the dataset's permission? | State the dataset licence and the venue's policy check | - |

Question 1 and the `mAP` slide are the pair that most often damages a reid talk. Put the
re-ranking and resolution status into the results slide header so the question is pre-answered.

## cnav, cooperative navigation

| # | Question | Answer strategy | Backup |
|---|---|---|---|
| 1 | Is this actually distributed? | Name which node computes what, per step. If any node holds global state, say so and stop claiming full distribution | B8 |
| 2 | What is exchanged, and at what rate? | Give the quantities and the per-step message count, and compare it against the baselines | B1 |
| 3 | What is the communication model? | Give delay, loss, and bandwidth assumptions, for every arm. Silence here reads as ideal channels | B6 |
| 4 | How many Monte Carlo runs? | Give the count and the dispersion. Below the field minimum, say so and qualify the claim | B3 |
| 5 | How does it scale with agent count? | Give the scaling experiment. Three agents is not a scalability result | B2 |
| 6 | What conditions does convergence require? | State the connectivity or excitation condition and where the experiment satisfies it | B8 |
| 7 | Is this simulation or field data? | Answer directly and state the gap explicitly. The fastest way to lose an audience on this axis is to let simulation sound like a deployment | B8 |
| 8 | How is the initial error set? | Give it per arm. Different initialization between arms usually decides a nonlinear comparison | B6 |
| 9 | What happens when an agent drops out? | Give the dropout scenario, or state it as untested | B2 |
| 10 | What is the onboard runtime? | Give the platform and the per-step time on the onboard computer | B4 |

Question 7 is the integrity question on this axis. Answer it before it is asked, on the results
slide, by labelling simulated results as simulated.

## filt, filtering and state estimation

| # | Question | Answer strategy | Backup |
|---|---|---|---|
| 1 | Is the filter consistent? | Give `NEES` or `ANEES` against the chi-square bounds, with the run count and the degrees of freedom. A consistency claim without both is not evidence | B1 |
| 2 | How many Monte Carlo runs? | Give the count. For accuracy and consistency claims, the field minimum is high, and a small count must be stated as a limitation | B3 |
| 3 | Was the baseline tuned as carefully as yours? | Answer directly. Asymmetric tuning is the most common defect on this axis, and an evasive answer is worse than an admission | B6 |
| 4 | How is the initial error set, per arm? | Give the mean and covariance per arm | B6 |
| 5 | Do the noise covariances match the simulated ones? | Give the assumed and actual covariance per arm. A mismatch for one arm only is a comparison failure | B6 |
| 6 | Which bound are you comparing against? | Name it exactly, and state the conditions under which it applies | B1 |
| 7 | Which assumptions does the proof use, and do they hold here? | Walk the list and name where each is checked. Assumptions stated only in words are the standard rejection reason on this axis | B8 |
| 8 | What is the per-step cost? | Give the complexity and the measured runtime on the named processor | B4 |
| 9 | Does this hold under non-Gaussian noise or outliers? | Give the stress experiment, or state the boundary | B2 |
| 10 | Is there real-data validation? | Give it if it exists. If the venue expects hardware evidence and the paper has simulation, say so plainly | B8 |

## Cross-axis questions

| # | Question | Answer strategy |
|---|---|---|
| 1 | What is genuinely new here? | Name the mechanism and the nearest prior work, and give the one concrete difference. Do not restate the abstract |
| 2 | Why is that better than the obvious alternative? | Compare against the alternative on the same protocol, from the ablation. If the alternative was not tried, say so |
| 3 | Is the improvement practically significant? | Convert the metric delta into a downstream consequence, or state that the practical effect is unknown |
| 4 | What are the failure modes? | Name two, concretely. An answer of "none that we found" is not credible and the audience knows it |
| 5 | Can I reproduce this? | Give the repository, the configs, the seeds, and the dataset instructions. If any is missing, name what is missing |
| 6 | How much compute did this take? | Give the hardware and the total GPU-hours. Being asked this and not knowing it damages credibility more than a large number would |
| 7 | What would you do with more time? | Name the single most valuable missing experiment and why it matters. This question tests whether the authors understand their own paper's weakest point |
| 8 | Does this hold under a different protocol? | Give the protocol difference and what it would change, or state that it was not tested |
| 9 | Is this a fair comparison? | Go to the backup slide that reproduces the checked protocol block and walk the matched fields; if a field is not on the slide, say it is not available rather than reconstructing it from memory. This is the question the talk exists to pre-empt |
| 10 | What is the significance test? | Give the test, the seed count, and the result, or state that no test was run and why |

## Answer discipline

- Answer the question that was asked. Restating the contribution is the most common way to lose
  an audience's confidence, because it signals that the answer does not exist.
- Say "we did not test that" when it is true. It costs one question. Improvising a number costs the
  talk and possibly the paper.
- Never invent a number under pressure, and never round a remembered value into a spoken one. If the
  value is on a backup slide, go to the slide. If it is not, say the number is not available.
- When a question contains a mistaken premise, correct the premise first, then answer. Correct it
  once, neutrally, with the slide that settles it.
- When a questioner is hostile, answer the technical content and ignore the tone. Never match the
  tone. The audience is judging both of you.
- Defer the questions that need more than 30 seconds. "That needs a figure, let us take it after the
  session" is a complete answer.
- Keep a question log in the outline after the talk. Recurring questions across two talks are
  findings about the paper's clarity, and they belong in the next revision.
