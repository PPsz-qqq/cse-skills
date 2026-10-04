# Integration map

Which upstream project each part of this pack came from, what was taken, and what was left
behind. This file exists so that a future maintainer can tell an inherited decision from an
invented one, and so that upstream changes can be re-evaluated deliberately.

## Method

Three research passes inventoried the source repositories by fetching their README files, skill
directories, and in several cases the skill bodies themselves, then verified identity, star
count, and license through the GitHub API on 2026-10-03. Full research notes are in
`_research/report-a-academic-nature.md`, `_research/report-b-scientific-ai.md`, and
`_research/report-c-automation.md`.

What was ported is **mechanism, not text**: workflow structure, gate definitions, thresholds,
scoring rules, and failure taxonomy, rewritten in this pack's own prose and adapted to the five
control axes. No file in this pack is a copy of an upstream file.

## Source status

Star counts and identities below are as verified on 2026-10-03. Several differ from the numbers
circulating in summary posts, so the verified value is given with the commonly quoted one.

| Source | Verified identity | Stars | License | Status here |
|---|---|---|---|---|
| Academic Research Skills | `Imbad0202/academic-research-skills` | 50,253 | CC BY-NC 4.0 | mechanism source |
| Nature Skills | `Yuan1z0825/nature-skills` | 45,731 | Apache-2.0 | mechanism source |
| Scientific Agent Skills | `K-Dense-AI/scientific-agent-skills`, renamed from `claude-scientific-skills` | 47,458 | MIT | mechanism source |
| AI Research SKILLs | `Orchestra-Research/AI-Research-SKILLs` | 13,213 | MIT | mechanism source |
| ARIS | `wanshuiyin/Auto-claude-code-research-in-sleep` | 16,924 | MIT | mechanism source |
| PaperSpine | `WUBING2023/PaperSpine` | 5,728 | MIT | mechanism source |
| Supervisor Skills | `HKUSTDial/Supervisor-Skills` | 7,852 | mixed per file | mechanism source |
| Research Paper Writing Skills | `Master-cai/Research-Paper-Writing-Skills` | 7,219 | MIT | mechanism source |
| Claude Scholar | `Galaxy-Dawn/claude-scholar` | 5,656 | MIT | mechanism source |
| Auto Empirical Research Skills | `brycewang-stanford/Auto-Empirical-Research-Skills` | 4,467 | CC BY-SA 4.0 | mechanism source |
| `lishix520/academic-paper-skills` | not independently verified | n/a | unknown | not used |
| `luwill/research-skills` | not independently verified | n/a | unknown | not used |
| `kthorn/research-superpower` | not independently verified | n/a | unknown | not used |
| `fuhaoda/stats-paper-writing-agent-skills` | not independently verified | n/a | unknown | not used |

Fork warning recorded during research: `xiaolai/nature-skills` (3 stars), `GHDaru/academic-research-skills`
(0 stars), `Elite-Lee/Supervisor-Skills` (0 stars), `kkcsy/Auto-claude-code-research-in-sleep`
(1 star, stale), and `TerryZhang95/claude-scholar` (0 stars) are forks, not the projects the
widely shared lists refer to. Install from the verified column.

## What was ported, and where it landed

### From Academic Research Skills

| Mechanism | Landed in |
|---|---|
| Multi-stage pipeline with mandatory, coverage-bounded integrity checks between stages | `cse-shared` G0 to G3, `cse-paper-craft` |
| Two-stage peer review with a revision round between them | `cse-pre-submission-review`, `cse-response-craft` |
| Claim-pointer and evidence-pointer discipline on every concern | `cse-shared` `core/review-rubrics.md` |
| Failure-mode classification used as a pre-submission gate | `cse-shared` `core/gate-contract.md` |
| Schema-style pre-commitment: fix the decision rule before executing | `cse-idea-forge` pre-commitment contract |

### From Nature Skills

| Mechanism | Landed in |
|---|---|
| Mutually blind multi-reviewer review: one immutable packet, emphasis briefs defined first, each reviewer isolated, reports frozen before comparison | `cse-pre-submission-review`, and the same rule stated as a red line in `cse-shared` `core/review-rubrics.md` |
| Consensus labeled only when two reviews independently raise the same concern | `cse-pre-submission-review` synthesis step |
| Separation of the reviewer package from any synthesis, with the synthesis never shown to reviewers | `cse-pre-submission-review`, `cse-response-craft` |
| Reviewer-facing isolation, so no reviewer sees another's comments or numbering | `cse-response-craft` |
| Consistency sweep: a manuscript checked against itself for numbers and superlatives | `cse-shared` `core/terminology-and-notation.md`, and the G2 reconciliation rule |
| Journal-fragment and paper-type routing | `cse-shared` `core/venue-matrix.md` classification by claim type |

### From Scientific Agent Skills (K-Dense)

| Mechanism | Landed in |
|---|---|
| Claim and evidence registries with stable IDs | `cse-shared` `core/artifact-contract.md` ledger, IDs `C1`, `C2`, ... |
| Human-only approval gates on irreversible steps | gate reporting format and the waiver rule in `cse-shared` |
| Deterministic, no-network verification scripts as the checker rather than model judgment | `tools/validate-skills.cjs` in this repository |
| Evidence-before-prose ordering | `cse-paper-craft` workflow order |

### From AI Research SKILLs (Orchestra Research)

| Mechanism | Landed in |
|---|---|
| Never generate a bibliography entry from memory; verify against two independent sources; emit a placeholder instead | `cse-lit-radar` citation discipline, `cse-shared` rule 1 and rule 10 |
| Pre-registration of the protocol before results exist | `cse-idea-forge` pre-commitment, `cse-experiment-suite` protocol blocks |
| A multi-dimension rigor rubric with an explicit grade formula | `cse-shared` `core/review-rubrics.md` eight dimensions and the recommendation mapping |

### From ARIS

| Mechanism | Landed in |
|---|---|
| Effort tiers that scale the work to the stakes | `cse-shared` `core/verdicts-and-loops.md` effort tiers |
| Six-state verdict enum with staleness invalidation on the audited input | `cse-shared` `core/verdicts-and-loops.md` |
| Review loop round cap and an explicit numeric stop rule | review and revise loop in the same file |
| Pilot budget caps in hours and GPU-hours, with a hard stop | `cse-idea-forge` pilot budget |
| Strongest-rejection-memo plus an independent adjudicator | `cse-idea-forge` killer-objection step |

### From PaperSpine

| Mechanism | Landed in |
|---|---|
| A long explicit step protocol rather than an open-ended instruction | the numbered workflow in every `cse-*` skill |
| Two attempts on a defect, then change tactic | `cse-shared` `core/verdicts-and-loops.md` repair loop |
| Review policy tiers from balanced to strict | effort tiers combined with the review loop |

Not ported from PaperSpine, and recorded here so the omission is deliberate rather than an
oversight: its exemplar-driven learning (read a fixed number of strong papers in the target
venue, then match their structure and ambition level quantitatively). `cse-paper-craft` instead
derives structure from the venue-class expectations in `cse-shared` `core/venue-matrix.md`. If
you want exemplar calibration later, the natural home is a step in `cse-paper-craft` that reads
3 to 6 accepted papers from the target venue and records their section word budgets and figure
counts as a target range, with the venue and the sampled papers named so the target is auditable.

### From Supervisor Skills (HKUSTDial)

| Mechanism | Landed in |
|---|---|
| Calibration rule: start every dimension at the midpoint and justify movement | `cse-shared` `core/verdicts-and-loops.md` |
| Top scores require zero Blocking findings and at most two Major findings | the same file, applied in `cse-pre-submission-review` |
| Multi-dimension idea evaluation with a strong-accept condition | `cse-idea-forge` scoring |
| Banned-style checks promoted to findings rather than nitpicks | `cse-shared` punctuation rule and the `cse-paper-craft` self-edit checklist |

### From Research Paper Writing Skills and Claude Scholar

| Mechanism | Landed in |
|---|---|
| Output contract: outline, role-tagged paragraphs, and a claim-evidence-status map | `cse-paper-craft` output format and the ledger |
| Adversarial self-review triaged into pass / needs revision / needs experiment | `cse-paper-craft` self-edit pass |
| Evidence records and claim promotion gates | `cse-shared` `core/verdicts-and-loops.md` promotion table |
| Blocker-first behaviour: refuse to produce output when the evidence is insufficient, and name the one unblocking item | the same file |

### From Auto Empirical Research Skills

| Mechanism | Landed in |
|---|---|
| Hard gates at fixed pipeline positions rather than advisory checks | G0 to G3 |
| Warning against flat installation of very large skill sets | the install-time separation of `cse-shared`, which other skills load surgically |

## What was deliberately left behind

- **Domain content.** Upstream skills carry biology, medicine, chemistry, and materials content
  and their dataset and assay vocabularies. None of it is relevant to these five axes and all of
  it was dropped.
- **Journal-specific style rules.** Nature-family and CNS style fragments were replaced by the
  venue-class matrix for vision, control, robotics, remote-sensing, and Chinese-language venues.
- **Persona-based reviewers.** Invented reviewer identities, specialties, and biographies were
  replaced by emphasis briefs, which is both more honest and more useful.
- **Tool-specific commands.** Upstream slash commands, CLI invocations, and MCP tool names were
  replaced by instructions that work with whatever tools the running agent has.
- **Bulk skill counts.** Packs advertising hundreds or thousands of skills were treated as
  catalogues to mine, not as content to mirror. Seven coherent bundles beat several hundred
  shallow ones, and a flat install of a large catalogue measurably degrades selection.
- **Unverified numbers.** Anything a report could not confirm is marked `[UNVERIFIED]` in the
  research files and is not stated as fact in this pack.

## Licensing note

Upstream licenses differ, and two of the mechanism sources are non-commercial or share-alike.
This pack implements ideas and restates mechanisms in original prose, and it copies no upstream
file, so it is not a derivative work of their text. If you intend to redistribute this pack
commercially, review the upstream licenses yourself rather than relying on this note: porting
ideas is generally unencumbered, but copying any upstream file, example, or figure is not, and
the share-alike and non-commercial terms would then apply.
