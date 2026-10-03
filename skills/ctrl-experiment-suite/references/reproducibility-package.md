# Reproducibility package inventory

`G3` fails when the reproducibility package cannot reproduce a headline number on the authors' own
hardware from the recorded material. This file defines what the package contains, how to name it,
and how to check it before submission. It is the operational form of
`ctrl-shared` `core/evidence-integrity.md` Rule 7.

The package has two audiences. The immediate one is the authors, who must be able to regenerate
every table after the submission deadline. The later one is a reader or a reviewer, who must be
able to reach the same number from the released material. Both need the same six items.

## The six mandatory items

| Item | What to record | Where it lives | Why it fails G3 when missing |
|---|---|---|---|
| Code commit | repository URL plus the full commit hash, and whether the tree was dirty | `repro/code.md` | a branch name is not a version; the branch moves |
| Config | the exact configuration file, not the command-line flags typed at the time | `exp/<run-id>/config.yaml` | reconstructing flags from shell history is not reproducible |
| Dataset version and split id | dataset name, release or version, checksum, split id, and how the split was constructed | `repro/data.md` | a split rebuilt later can differ and the number becomes unattributable |
| Seeds | the exact list or derivation rule, per arm | in the config, and in the protocol block | a single-seed result cannot be reproduced to a distribution |
| Hardware | device model, memory, count, driver, framework and library versions, and power mode where timing is reported | `repro/env.md` | throughput and some numeric results depend on it |
| Exact command | the full invocation that produced the artifact, recorded from the run, not retyped | `exp/<run-id>/cmd.txt` | the difference between two similar invocations is usually the bug |

Record a seventh item for anything that shapes the result and is not in the six. Examples: the
evaluation-script version, the container image digest, the CUDA and cuDNN versions, the
deterministic-algorithm settings, the reduction or threading settings, or the random seed of the
framework's own global generator.

## Naming and layout

Extend the workspace layout in `ctrl-shared` `core/artifact-contract.md`. Never overwrite a run
directory; a rerun creates a new run id and a new directory.

```text
exp/<axis>-<slug>-<run-id>/
  config.yaml         # the resolved config, with defaults applied
  cmd.txt             # the exact command
  env.txt             # device, driver, framework, library versions
  seed.txt            # the seed list or master seed and derivation rule
  stdout.log          # full log, unmuted
  metrics.json        # raw per-unit or per-seed metrics
  table.md            # the derived table that appears in the manuscript
repro/
  code.md             # repository, commit hashes, dirty-tree status, entry points
  data.md             # dataset versions, checksums, split ids, download instructions
  env.md              # hardware and software inventory per reported number
  README.md           # how to reproduce each headline number, in order
  limitations.md      # what cannot be reproduced, and why
```

Run ids follow `<axis>-<slug>-<run-id>`, for example `det-yoloassoc-r07`. The slug names the
experiment, not the attempt. The run id increments and is never reused.

## The reproduce-a-headline-number test

Before submission, run this test on at least one headline number per axis, on the authors' own
hardware, from the recorded material only.

1. Start from a clean checkout of the recorded commit.
2. Restore the recorded environment, or verify that the recorded environment matches the current
   one well enough, and state any difference.
3. Place the dataset at the recorded version and verify the checksum and the split id.
4. Run the recorded command, unmodified.
5. Compare against the recorded metrics at the precision reported in the manuscript.
6. Record the outcome in `ctrl-gates.md`: reproduced exactly, reproduced within dispersion, or not
   reproduced.

The test needs an authorized executor, the recorded hardware class and the data. When any of them
is unavailable to you, record the test as `not performed` (or `BLOCKED` with the missing
dependency named), hand the user the exact steps above, and never report a reproduction that did
not run.

A number that reproduces within its own seed dispersion passes. An exact match is expected when
the recorded seed and a deterministic pipeline are replayed; it is not evidence of a defect. Check
separately that the declared seed variation actually occurred across the runs that make up the
dispersion, because identical values across supposedly different seeds do indicate frozen
randomness.

A number that does not reproduce is a finding to report, not a defect to hide. State what
differs, in what direction, and whether the manuscript's claim survives the difference.

## Binding a claim to the text it verifies

Re-verification is required whenever the wording of a verified claim changes, and the trigger is
otherwise easy to miss because a reworded sentence looks settled. Record the claim source, not only
its result.

1. Store a hash of the normalized claim line rather than the claim text itself, taken after removing
   the ledger markers and collapsing whitespace, and keyed to the whole physical line.
2. Keep one claim per physical line, so that a hash identifies exactly one claim.
3. On any edit, recompute the hash. A changed hash means the ledger row and the protocol block are
   `STALE` for that line and must be re-verified before the number may appear again
   (`../../ctrl-shared/core/verdicts-and-loops.md`).

The same discipline gives a mechanical answer to "is this audit still current" for the whole
package. Record the hash of every artifact an audit consumed, and have the check recompute those
hashes and report `STALE` if any differ. An audit that cannot name the revision it ran against is a
verdict about an artifact that no longer exists.

## What a checklist cannot certify

State the limit of every mechanical check in the artifact that carries its output, because a
passing check is routinely read as a quality verdict.

- A script certifies that a field is present, a path resolves, a hash matches, or a value
  reconciles. It does not certify that a comparison is fair, that a claim is true, or that the paper
  is ready.
- A checker must never score, rank, or declare acceptance. Any output that reads as a quality grade
  is an overclaim by the tool.
- Keep checks deterministic, local, and offline. A check that reaches the network is not
  reproducible and cannot be part of the freeze.
- Where a check reports a problem, report the issue code and its location rather than echoing the
  manuscript text, so the check can run on unpublished material without leaking it.
- The remaining human obligations are exactly those a script cannot perform: opening the source and
  confirming the support, resolving a scientific ambiguity, and approving the submission.

## Checklist

```text
[ ] Every table in the manuscript resolves to a run directory under exp/
[ ] Every run directory has config, cmd, env, seed, log, and raw metrics
[ ] Every headline number has a commit hash and a dirty-tree status
[ ] Dataset versions are pinned, and split construction is described well enough to rebuild
[ ] Seeds are listed, not described, and are identical across compared arms
[ ] Hardware statements name the exact device, including for every timing number
[ ] The reproduce-a-headline-number test has been run and its outcome recorded
[ ] Nothing needed for reproduction exists only in a private notebook or a chat message
[ ] Released material has a license compatible with the data and the venue rules
[ ] Third-party code and checkpoints are credited with their licenses
[ ] What cannot be released is named, with the reason and the closest available substitute
[ ] The anonymized artifact, if the venue requires one, contains no identifying paths or author names
```

## Axis-specific packaging notes

### `det`

- Pin the evaluation code and its version. COCO-style AP implementations differ in the maximum
  detection count, the area-range handling, and the interpolation, and the differences are worth
  several tenths of a point.
- Record the class ordering, the label mapping, and whether evaluation ran on an official server
  or locally. Server evaluation is not offline-reproducible, so record the submission id.
- Ship the exact inference script used for the reported numbers, including TTA and NMS settings.
  A `detect.py` with defaults is not the recorded command.

### `track`

- Ship or reference the exact detection files used for every arm, with their checksums. A tracker
  result whose detections are regenerated is not the same result.
- Record the sequence list and the evaluation tool version. TrackEval conventions, threshold
  settings, and the `MT`/`ML` percentage thresholds change the numbers.
- Record the timing protocol: warm-up handling, repeat count, batch size, whether detection is
  included, and the power mode. Two runs of the same tracker on the same GPU differ otherwise.

### `reid`

- Record the exact query and gallery files, the identity and camera lists, and the evaluation
  script version. A rebuilt split that is nearly the same produces nearly the same number and is
  still not a reproduction.
- State whether re-ranking was applied at evaluation time and with which parameters, since a
  rerun with defaults silently changes the number.
- Record the test-time crop and resize code path, because the train path and the test path are
  often different functions and only one of them is covered by the training config.

### `cnav`

- Ship the scenario generator, not the generated scenarios only. The generator defines the
  distribution the result claims to hold over, and reviewers in this field ask for it.
- Record the topology list or the topology sampling rule, the timing of topology changes, the
  delay and loss draw streams, and their seeding, separately from the estimator's seeding.
- Record the message size accounting rule, including headers and any serialization overhead, so
  the reported communication cost is auditable.

### `filt`

- Ship the trajectory generator and the noise generator with their seeds, and state the process
  and measurement models in the form actually used, not in idealized notation.
- Record all filter parameters per arm, including gating thresholds, sigma-point scaling,
  particle counts, and resampling schemes. These are the parameters reviewers ask for first.
- Record the consistency computation itself: degrees of freedom, the `P_k` used, whether the
  covariance was symmetrized or regularized, and the handling of singular `P_k`.

## Common failures

- A commit hash recorded on the day of submission, after the repository moved. Record it at run
  time, in the run directory.
- A configuration in the paper's appendix that differs from the one that produced the number.
  Generate the appendix table from the config, not by hand.
- Hardware recorded as a category rather than a part, which makes every timing number
  unreproducible.
- Seeds recorded for training but not for the evaluation-time sampling, the augmentation, or the
  scenario generator.
- A split described in prose, such as "we randomly split 80/20", with no id and no rule. State the
  rule and the seed of the split itself.
