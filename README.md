# ctrl-skills

English | [中文](README.zh.md)

An agent-skill pack for research and publication in 控制科学与工程 (Control Science and
Engineering), covering five application axes.

| Axis | Chinese | Scope |
|---|---|---|
| `det` | 目标检测 | object detection, including aerial and remote-sensing settings |
| `track` | 目标跟踪 | single and multi-object tracking |
| `reid` | 重识别 | person and vehicle re-identification, retrieval |
| `cnav` | 协同导航 | cooperative navigation, cooperative localization, multi-robot and UAV swarms |
| `filt` | 滤波 | state estimation, sensor fusion, guidance and control |

Target venues span four classes: top-tier vision and machine learning (CVPR, ICCV, ECCV,
NeurIPS, ICML, ICLR, T-PAMI), control, robotics, and navigation (IEEE TAC, Automatica, T-RO,
RA-L, ICRA, IROS, TAES, CDC, ACC), remote sensing (TGRS, JSTARS, ISPRS), and Chinese-language
journals (自动化学报, 控制理论与应用, 控制与决策, 航空学报, 中国惯性技术学报).

## What this pack is for

Most academic skill packs are written for the natural sciences: biology, medicine, chemistry,
materials. Their review criteria, figure conventions, and evidence norms do not transfer to
engineering venues where the contribution is a mechanism, an estimator, or a system, and where
the decisive question is whether a comparison was protocol-matched.

This pack is built around that question. Its organizing idea is that a quantitative comparison
is a measurement, and it inherits every obligation of a measurement: a defined instrument, a
declared protocol, a stated number of trials, and honest uncertainty. Nearly every rule in the
shared contract follows from that one commitment.

## The skills

Eight bundles, in `skills/`. `ctrl-shared` is the contract the other seven obey; the rest form
a pipeline.

| Skill | Use it for | Trigger examples |
|---|---|---|
| [ctrl-shared](skills/ctrl-shared/SKILL.md) | the shared contract: gates, evidence rules, venue matrix, review rubrics, verdicts, terminology, artifact formats. Other skills load it; it is also a usable standalone entry point | "what does this pack require", gate and ledger definitions |
| [ctrl-lit-radar](skills/ctrl-lit-radar/SKILL.md) | literature search, venue-cycle tracking, benchmark atlas, nearest-competitor ledger | 文献综述, 相关工作, 找论文, literature review, 文献调研 |
| [ctrl-idea-forge](skills/ctrl-idea-forge/SKILL.md) | turn a gap into a falsifiable, budgeted research idea; G0 scope and G1 frozen plan | 选题, 开题, 创新点, research idea, hypothesis |
| [ctrl-experiment-suite](skills/ctrl-experiment-suite/SKILL.md) | design, audit, and report experiments; per-axis protocol blocks, statistics, ablations, reproducibility | 实验设计, 消融实验, 结果分析, ablation, protocol |
| [ctrl-paper-craft](skills/ctrl-paper-craft/SKILL.md) | write and revise the manuscript section by section | 写论文, 投稿, 论文写作, manuscript, abstract |
| [ctrl-pre-submission-review](skills/ctrl-pre-submission-review/SKILL.md) | referee-side pre-submission review with mutually blind reviewers | 审稿, 模拟审稿, 预审, mock review, 帮我审一下论文 |
| [ctrl-response-craft](skills/ctrl-response-craft/SKILL.md) | response letters, rebuttals, revision plans | 回复审稿意见, rebuttal, response letter |
| [ctrl-paper-to-slides](skills/ctrl-paper-to-slides/SKILL.md) | conference, oral, and defense decks from a paper | 论文做PPT, 学术汇报, conference talk, slides |

## The pipeline

```text
ctrl-lit-radar      find the gap and the nearest competitors
       |
ctrl-idea-forge     G0 scope -> G1 frozen plan (falsifiable, budgeted)
       |
ctrl-experiment-suite   run and audit; G2 evidence freeze (claim ledger)
       |
ctrl-paper-craft    write the manuscript against the ledger
       |
ctrl-pre-submission-review  3 blind reviewers -> G3 readiness
       |
ctrl-response-craft     revision round and point-by-point response
       |
ctrl-paper-to-slides    audience-facing deck
```

Each stage reads the previous stage's artifacts by file, not by conversation memory. The
artifact names are fixed by [ctrl-shared/core/artifact-contract.md](skills/ctrl-shared/core/artifact-contract.md).

## The four gates

Everything else in the pack serves these. A gate is passed by an artifact, never by an
assertion.

| Gate | Question | Blocks |
|---|---|---|
| `G0` scope | What is claimed, against what, for whom? Is the claim type matched to the evidence class? | all downstream work |
| `G1` proposal freeze | Is the plan specific enough to fail? Is the refutation rule pre-declared? | experiments and drafting |
| `G2` evidence freeze | Does every number exist, and does every comparison hold? | drafting, review, rebuttal, slides |
| `G3` submission readiness | Would this survive its own reviewer? | submission |

`G2` has no waiver path. `G0` and `G3` may be waived only on explicit user instruction, with the
residual risk recorded. Definitions and pass criteria are in
[ctrl-shared/core/gate-contract.md](skills/ctrl-shared/core/gate-contract.md).

## What makes it domain-specific

General academic-writing advice does not cover the things that actually decide these papers.

- **Protocol-matched comparison.** Input resolution, test-time augmentation, pretraining data,
  detector provenance, re-ranking, query construction, and hand-tuning symmetry. Each axis has a
  list of differences that invalidate a delta, in
  [ctrl-shared/core/evidence-integrity.md](skills/ctrl-shared/core/evidence-integrity.md).
- **Axis-specific evidence obligations.** Tracking numbers require detector provenance and the
  public-versus-private detection label. Cooperative navigation requires a distribution proof
  and a communication model with delay and loss. Filtering requires Monte Carlo consistency
  evidence, NEES or ANEES against chi-square bounds. The default is a per-time-step evaluation
  with `N * n_x` degrees of freedom; pooling over `N * T * n_x` is permitted only when
  independence holds or the correlation has been handled by a calibrated method.
- **Metric precision.** `mAP` is meaningless without its averaging convention; `MOTA` without the
  detection protocol is not comparable to anything; `FPPI` is an operating rate while `LAMR` is
  the summary metric. Conventions are pinned in
  [ctrl-shared/core/terminology-and-notation.md](skills/ctrl-shared/core/terminology-and-notation.md).
- **Venue-class reviewer behaviour.** What a CVPR-class reviewer rejects on differs from what a
  TAC reviewer rejects on. See
  [ctrl-shared/core/venue-matrix.md](skills/ctrl-shared/core/venue-matrix.md).
- **Chinese-language venue requirements.** 创新点 stated as explicit points, a real Chinese
  abstract rather than a translation, 基金项目 and 中图分类号 fields, GB/T 7714 references.

## Design rules the pack enforces on itself

- **No fabricated evidence.** A missing value is written `[MISSING: ...]`, never filled with a
  plausible number. A bibliography entry is never generated from memory.
- **Tier discipline.** Every quantity is labelled `measured`, `reported`, or `assumed`.
- **Blocker first.** When the evidence cannot support the request, say so before doing the work
  and name the one item that unblocks it.
- **No concern quota.** A review reports the concerns that exist, not the number requested.
- **Calibration with a midpoint start.** Scores begin at the midpoint and every point of movement
  needs a pointer. Top scores require zero `Blocking` findings.
- **Reviewer blindness is real or declared.** Multi-reviewer output is isolated, frozen, and only
  then compared; if contexts cannot be isolated, the limitation is stated instead of the claim.
- **Gates are not negotiable under deadline pressure.** Severity is not lowered because a user is
  displeased.

## Install

Skills are plain `SKILL.md` bundles. DSH discovers them from `<root>/<name>/SKILL.md` at the top
level of a scanned root, watches the roots, and needs no restart.

The eight bundles live in the `skills/` directory of this repository, which contains nothing but
skills, so it can be handed to DSH directly or copied elsewhere as-is.

```powershell
powershell -File tools/install.ps1           # junction into ~/.dsh/skills
powershell -File tools/install.ps1 -Remove   # remove only what was installed
```

The installer finds `skills/` automatically and falls back to the repository root if the bundles
are stored inline. Full options, root priority, verification steps, and a manual fallback are in
[INSTALL.md](INSTALL.md).

## Validate

```powershell
node tools/validate-skills.cjs              # defaults to skills/
node tools/validate-skills.cjs --fix-bom    # also repair a UTF-8 BOM in place
node tools/check-dsh-discovery.cjs          # run DSH's own parser over the installed root
```

The validator checks frontmatter presence and keys, kebab-case `name` matching the directory
name, boolean spelling of invocation keys, description length, frontmatter closure, a UTF-8 BOM,
unresolved `TODO`/`TBD` markers, every relative markdown link, and every inline-code path such as
[gate-contract.md](skills/ctrl-shared/core/gate-contract.md). That last check matters because an
inline path that is correct in `SKILL.md` resolves one level too high inside `references/`, and
nothing else reports it. If it finds no bundles at all it exits non-zero rather than reporting a
clean pack, so a mistyped root cannot look like success.

`check-dsh-discovery.cjs` is the acceptance test that matters: it replicates the provider's own
parse path with the same `yaml` version DSH depends on, so it reports what the Harness will
actually see rather than what this repository believes. Run it after any frontmatter or layout
change. See [tools/README.md](tools/README.md) for the failure modes both tools exist to catch.

## Evaluate

[evals/evals.json](evals/evals.json) holds 14 behavioural cases, one or more per skill. Each case
targets a contract rule and asserts on behaviour rather than wording, for example refusing an
unmatched comparison, refusing a single-seed state-of-the-art claim, refusing to alter a number
for a slide, and refusing to report a gate as passed without its artifact.

## Provenance

The pack was built by inventorying existing academic skill collections, extracting their
transferable mechanisms, and rewriting them for these five axes. The mapping from source project
to landed mechanism is in [docs/INTEGRATION.md](docs/INTEGRATION.md), including verified
repository identities, licences, star counts, and the fork traps to avoid.

Upstream collections cover the natural sciences, so their domain content was dropped and only
their workflow machinery was reused. Where a mechanism was ported, its threshold was kept
exactly, for example the midpoint-start calibration rule, the loop round cap, the pilot budget
caps, and the top-score condition.

## Layout

```text
ctrl-skills/                 the repository root
  README.md             this file
  README.zh.md          中文说明
  INSTALL.md            install, verification, and uninstall
  skills/               the skill root: exactly the eight bundles, nothing else
    ctrl-shared/          the shared contract
    ctrl-lit-radar/       literature intelligence
    ctrl-idea-forge/      scoping and planning
    ctrl-experiment-suite/  experiments and statistics
    ctrl-paper-craft/     manuscript writing
    ctrl-pre-submission-review/  referee-side review
    ctrl-response-craft/  revision correspondence
    ctrl-paper-to-slides/ decks
  tools/                validator, DSH discovery check, installer
  evals/                behavioural eval cases
  docs/                 INTEGRATION.md, the source-to-mechanism mapping
  _research/            the research reports the pack was built from
```

`skills/` is the directory to point DSH at, or to copy to another machine. The rest of the
repository holds everything that supports the pack but is not itself a skill.

## License

No license is granted by default. The pack implements mechanisms observed in upstream projects
under differing licenses (MIT, Apache-2.0, CC BY-NC 4.0, CC BY-SA 4.0) and copies no upstream
file, but if you intend to redistribute or reuse this commercially, review
[docs/INTEGRATION.md](docs/INTEGRATION.md) and the upstream licenses yourself.
