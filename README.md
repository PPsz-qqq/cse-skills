# cse-skills

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

## Scoped use

See [中文快速使用](docs/QUICKSTART.zh-CN.md). Local edits, diagnostic review and draft planning
can run independently without rebuilding the entire research pipeline. Final scientific claims
require the applicable evidence gates. All entries use the
[execution contract](skills/cse-shared/core/execution-contract.md) for capability limits and handoff.

## The skills

Nine bundles, in `skills/`. `cse-shared` is the contract the other eight obey; the rest form
a pipeline. The `cse-` prefix stands for Control Science and Engineering. Until 2026-10-04 the
skills were named `ctrl-*`; the repository keeps the name ctrl-skills, the installer removes links
left under the old names, and projects with old `ctrl-*` artifact files keep working (see
[artifact-contract.md](skills/cse-shared/core/artifact-contract.md)).

| Skill | Use it for | Trigger examples |
|---|---|---|
| [cse-shared](skills/cse-shared/SKILL.md) | the shared contract: gates, evidence rules, venue matrix, review rubrics, verdicts, terminology, artifact formats. Other skills load it; explicit questions about the contract can load it directly | "what does this pack require", gate and ledger definitions |
| [cse-lit-radar](skills/cse-lit-radar/SKILL.md) | literature search, venue-cycle tracking, benchmark atlas, nearest-competitor ledger | 文献综述, 相关工作, 找论文, literature review, 文献调研 |
| [cse-idea-forge](skills/cse-idea-forge/SKILL.md) | turn a gap into a falsifiable, budgeted research idea; G0 scope and G1 frozen plan | 选题, 开题, 创新点, research idea, hypothesis |
| [cse-experiment-suite](skills/cse-experiment-suite/SKILL.md) | design, audit, and report experiments; per-axis protocol blocks, statistics, ablations, reproducibility | 实验设计, 消融实验, 结果分析, ablation, protocol |
| [cse-figure-studio](skills/cse-figure-studio/SKILL.md) | publication-grade data visualization with venue-compliant themes and demo-data tracking | 画图, 作图, 论文图表, 科研绘图, figure, plot, visualization |
| [cse-paper-craft](skills/cse-paper-craft/SKILL.md) | write and revise the manuscript section by section | 写论文, 投稿, 论文写作, manuscript, abstract |
| [cse-pre-submission-review](skills/cse-pre-submission-review/SKILL.md) | referee-side pre-submission review with mutually blind reviewers | 审稿, 模拟审稿, 预审, mock review, 帮我审一下论文 |
| [cse-response-craft](skills/cse-response-craft/SKILL.md) | response letters, rebuttals, revision plans | 回复审稿意见, rebuttal, response letter |
| [cse-paper-to-slides](skills/cse-paper-to-slides/SKILL.md) | conference, oral, and defense decks from a paper | 论文做PPT, 学术汇报, conference talk, slides |

## The pipeline

```text
cse-lit-radar      find the gap and the nearest competitors
       |
cse-idea-forge     G0 scope -> G1 frozen plan (falsifiable, budgeted)
       |
cse-experiment-suite   run and audit; G2 evidence freeze (claim ledger)
       |
       +------------+
       |            |
cse-figure-studio   cse-paper-craft    visualize results    write manuscript
       |            |                   (venue-compliant)   (against ledger)
       +------------+
       |
cse-pre-submission-review  3 blind reviewers -> G3 readiness
       |
cse-response-craft     revision round and point-by-point response
       |
cse-paper-to-slides    audience-facing deck
```

Each stage reads the previous stage's artifacts by file, not by conversation memory. The
artifact names are fixed by [cse-shared/core/artifact-contract.md](skills/cse-shared/core/artifact-contract.md).

## The four gates

Everything else in the pack serves these. A gate is passed by an artifact, never by an
assertion.

| Gate | Question | Blocks |
|---|---|---|
| `G0` scope | Is the claim type matched to obtainable evidence? | promotion of that scientific claim |
| `G1` proposal freeze | Is the confirmatory plan specific and pre-declared? | confirmatory execution, not exploratory planning |
| `G2` evidence freeze | Does each in-scope claim resolve and each comparison hold? | unverified final claims, not diagnostic review or local editing |
| `G3` submission readiness | Would this survive its own reviewer? | submission |

`G1` and `G2` have no waiver path. `G0` and `G3` may be waived only on explicit user instruction,
with the residual risk recorded; the waiver is logged beside the unchanged verdict and is never a
pass. Definitions and pass criteria are in
[cse-shared/core/gate-contract.md](skills/cse-shared/core/gate-contract.md).

## What makes it domain-specific

General academic-writing advice does not cover the things that actually decide these papers.

- **Protocol-matched comparison.** Input resolution, test-time augmentation, pretraining data,
  detector provenance, re-ranking, query construction, and hand-tuning symmetry. Each axis has a
  list of differences that invalidate a delta, in
  [cse-shared/core/evidence-integrity.md](skills/cse-shared/core/evidence-integrity.md).
- **Axis-specific evidence obligations.** Tracking numbers require detector provenance and the
  public-versus-private detection label. Cooperative navigation requires a distribution proof
  and a communication model with delay and loss. Filtering requires Monte Carlo consistency
  evidence, NEES or ANEES against chi-square bounds. The default is a per-time-step evaluation
  with `N * n_x` degrees of freedom; pooling over `N * T * n_x` is permitted only when
  independence holds or the correlation has been handled by a calibrated method.
- **Metric precision.** `mAP` is meaningless without its averaging convention; `MOTA` without the
  detection protocol is not comparable to anything; `FPPI` is an operating rate while `LAMR` is
  the summary metric. Conventions are pinned in
  [cse-shared/core/terminology-and-notation.md](skills/cse-shared/core/terminology-and-notation.md).
- **Venue-class reviewer behaviour.** What a CVPR-class reviewer rejects on differs from what a
  TAC reviewer rejects on. See
  [cse-shared/core/venue-matrix.md](skills/cse-shared/core/venue-matrix.md).
- **Chinese-language venue requirements.** 创新点 stated as explicit points, a real Chinese
  abstract rather than a translation, 基金项目 and 中图分类号 fields, references in the GB/T 7714
  edition the journal names (GB/T 7714-2025 replaced the 2015 edition on 2026-07-01).

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
level of a scanned root when the filesystem provider is enabled. Healthy enabled watchers pick
up file changes without a restart; inactive or misconfigured providers do not.

The eight bundles live in the `skills/` directory of this repository, which contains nothing but
skills, so it can be handed to DSH directly or copied elsewhere as-is.

```powershell
powershell -File tools/install.ps1 -WhatIf   # preview the plan, change nothing
powershell -File tools/install.ps1           # junction into ~/.dsh/skills
powershell -File tools/install.ps1 -Remove   # remove only what this installer owns
```

The installer finds `skills/` automatically and falls back to the repository root if the bundles
are stored inline. It never deletes data it does not own: links are removed without touching their
targets, copies carry an ownership record, and `-Force` moves unowned directories to a backup folder
instead of deleting them. Full options, root priority, verification steps, and a manual fallback are
in [INSTALL.md](INSTALL.md).

## Validate

```powershell
node tools/validate-skills.cjs              # defaults to skills/
node tools/validate-skills.cjs --fix-bom    # also repair a UTF-8 BOM in place
node tools/check-dsh-discovery.cjs skills   # offline compatibility, not live activation
node --test tools/skill-tools.test.cjs      # structural/discovery regression fixtures
node --test tools/install.test.cjs          # installer ownership rules, Windows, temp dirs only
```

The validator checks frontmatter presence and keys, kebab-case `name` matching the directory
name, boolean spelling of invocation keys, frontmatter closure, a UTF-8 BOM, unresolved
`TODO`/`TBD` markers, every relative markdown link, and every inline-code path such as
[gate-contract.md](skills/cse-shared/core/gate-contract.md). Inline paths are checked in both
directions: a `../` path that is right in `SKILL.md` resolves one level too high inside
`references/`, and a bundle-root path such as `references/x.md` resolves one level too deep there.
It also fails any description longer than 500 characters, because DSH's skill catalog cuts
descriptions at that default length and the trigger phrases at the end would never reach the model.
If it finds no bundles at all it exits non-zero rather than reporting a clean pack, so a mistyped
root cannot look like success.

`check-dsh-discovery.cjs` uses real YAML parsing and the inspected invocation contract, checking
all eight distinct expected names rather than just a count. This is an offline compatibility
check, not live provider activation or session visibility. Run it after frontmatter/layout changes. See [tools/README.md](tools/README.md) for the failure modes both tools exist to catch.

## Evaluate

[evals/evals.json](evals/evals.json) holds 33 behavioural cases, one or more per skill. Each case
targets a contract rule and asserts on behaviour rather than wording, for example refusing an
unmatched comparison, refusing a single-seed state-of-the-art claim, refusing to alter a number
for a slide, and refusing to report a gate as passed without its artifact.

## Provenance

The pack was built by inventorying existing academic skill collections, extracting their
transferable mechanisms, and rewriting them for these five axes. The mapping from source project
to landed mechanism is in [docs/INTEGRATION.md](docs/INTEGRATION.md), including verified
repository identities, licences, star counts, and the fork traps to avoid.

Upstream collections cover the natural sciences, so their domain content was dropped and only
their workflow machinery was reused. Thresholds are pack defaults, not externally validated laws.
Later maintenance corrected statistical assumptions, scoped gates and budget semantics, fitted the
descriptions to the DSH catalog limit, verified benchmark and venue facts against primary sources,
and made the installer non-destructive. See [improvement notes](docs/IMPROVEMENTS.zh-CN.md).

## Layout

```text
ctrl-skills/                 the repository root
  README.md             this file
  README.zh.md          中文说明
  INSTALL.md            install, verification, and uninstall
  skills/               the skill root: exactly the nine bundles, nothing else
    cse-shared/          the shared contract
    cse-lit-radar/       literature intelligence
    cse-idea-forge/      scoping and planning
    cse-experiment-suite/  experiments and statistics
    cse-figure-studio/   publication-grade data visualization
    cse-paper-craft/     manuscript writing
    cse-pre-submission-review/  referee-side review
    cse-response-craft/  revision correspondence
    cse-paper-to-slides/ decks
  tools/                validator, DSH discovery check, installer and their tests
  evals/                behavioural eval cases
  docs/                 source-to-mechanism mapping, Chinese quick start, improvement notes
  _research/            the research reports the pack was built from
```

`skills/` is the directory to point DSH at, or to copy to another machine. The rest of the
repository holds everything that supports the pack but is not itself a skill.

## License

No license is granted by default. The pack implements mechanisms observed in upstream projects
under differing licenses (MIT, Apache-2.0, CC BY-NC 4.0, CC BY-SA 4.0) and copies no upstream
file, but if you intend to redistribute or reuse this commercially, review
[docs/INTEGRATION.md](docs/INTEGRATION.md) and the upstream licenses yourself.
