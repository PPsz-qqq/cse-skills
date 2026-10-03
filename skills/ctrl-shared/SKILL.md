---
name: ctrl-shared
description: >-
  Internal shared reference contract for the ctrl-* control-science-and-engineering skill pack,
  covering object detection (目标检测), tracking (目标跟踪), re-identification (重识别),
  cooperative navigation (协同导航), and filtering / state estimation (滤波). Do not invoke it as a
  standalone user workflow. Another ctrl skill loads only the exact file it names, such as the venue
  and review-criteria matrix, the research-integrity and gate contract, the evidence and verification
  rules, the terminology and notation conventions, or the artifact contract. Load directly only when
  the user explicitly asks for this pack's shared contract itself.
---

# CTRL shared contract

Shared reference package for the `ctrl-*` skill family. It serves research in
控制科学与工程 (Control Science and Engineering) across five application domains:

| Axis | Chinese | Typical subcommunity |
|---|---|---|
| `det` | 目标检测 | computer vision, pattern recognition |
| `track` | 目标跟踪 | computer vision, multi-object tracking |
| `reid` | 重识别 | person / vehicle re-identification, retrieval |
| `cnav` | 协同导航 | multi-robot, UAV swarm, cooperative localization |
| `filt` | 滤波 | estimation, sensor fusion, guidance and control |

A single paper may cross axes. Record every axis that applies and run every gate for the
primary axis plus the evidence rules of each secondary axis.

## Stance

- Ground every statement in an artifact that exists: the user's own draft, code, logs, figures,
  or a verified published source. Never in what a paper "probably" reported.
- Separate three epistemic tiers and label them explicitly wherever they appear: `measured`
  (produced by a run the user can point at), `reported` (stated by a citable source),
  `assumed` (a working hypothesis). Tier mixing is the single most common failure in this
  literature, in both directions: simulated results presented as field results, and single-seed
  numbers presented as stable performance.
- Prefer a smaller, verifiable claim over a larger, unfalsifiable one. A paper that claims
  "improves mAP by 1.2 on MSMT17 with matched protocol" is stronger than one that claims
  "achieves state-of-the-art performance".
- Quantitative comparison is a measurement claim and inherits every obligation of a physical
  measurement: define the instrument, the protocol, the number of trials, and the uncertainty.
- Never invent a citation, a number, a figure, a baseline, a dataset split, a hardware
  specification, or an experiment that was not run. If a requested element does not exist,
  mark the location `[MISSING]` and state what would be required to fill it.
- Report negative and null results. A failed ablation is a finding, and suppressing it is
  misconduct rather than style.

## Invariants

These five hold across every skill in the pack. A violation is blocking regardless of which
skill is active.

1. **No fabricated evidence.** Every number in every artifact traces to a run, a log, a table,
   or a cited source. See `core/evidence-integrity.md`.
2. **No unfair comparison.** A performance comparison is valid only under a matched protocol.
   Declare the protocol before reporting the delta. See `core/evidence-integrity.md`.
3. **No gate skipped.** A gate is passed by an artifact, not by an assertion. See
   `core/gate-contract.md`.
4. **No unreported boundary.** Every claim carries its validity boundary: dataset, split,
   scenario, hardware, seed count, and assumption set.
5. **No silent language switch.** Terminology and notation follow
   `core/terminology-and-notation.md`, so the same object has one symbol and one name
   throughout a manuscript, a slide deck, and a response letter.

## File map

Load only what the current step needs. Read the file with the file-read tool; each path is
relative to this skill's base directory, which the `skill` tool reported.

| File | Open when |
|---|---|
| [core/gate-contract.md](core/gate-contract.md) | You need the gate definitions, pass criteria, artifacts, or blocking semantics |
| [core/evidence-integrity.md](core/evidence-integrity.md) | You are auditing numbers, comparisons, ablations, seeds, or provenance |
| [core/venue-matrix.md](core/venue-matrix.md) | You are choosing or justifying a target venue, or need its review criteria |
| [core/review-rubrics.md](core/review-rubrics.md) | You are scoring a manuscript, calibrating severity, or writing a review |
| [core/verdicts-and-loops.md](core/verdicts-and-loops.md) | You need the verdict enum, staleness rule, loop budgets, effort tiers, calibration rule, or claim-promotion conditions |
| [core/terminology-and-notation.md](core/terminology-and-notation.md) | You need metric definitions, symbol conventions, or bilingual term choices |
| [core/artifact-contract.md](core/artifact-contract.md) | You are creating or naming deliverable files, or running the final checklist |

## Scope boundary

This pack covers the research and publication workflow. It does not run experiments, train
models, or execute simulation campaigns on the user's behalf unless a separate tool exists for
it. It does not replace venue-specific author guidelines, which always win over this pack when
they conflict; when they conflict, follow the venue and record the override.
