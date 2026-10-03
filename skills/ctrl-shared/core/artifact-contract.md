# Artifact contract

Deliverables from every `ctrl-*` skill use these names and locations unless the user asks for
something else. Stable names let later skills find earlier artifacts without re-reading the
whole conversation, and let a reviewer check one claim against its source.

## Workspace layout

Create this tree under the user's chosen project directory. Do not invent a location the user
did not choose; ask once, then keep it.

```text
<project>/
  ctrl-scope.md                 # G0 scope block and axis selection
  ctrl-plan.md                  # G1 frozen plan: hypothesis, protocol, baselines, ablations
  ctrl-claims.md                # G2 claim-to-evidence ledger
  ctrl-protocol.md              # axis comparison-protocol blocks, one section per axis
  ctrl-gates.md                 # gate status history, append-only
  ctrl-venues.md                # venue fit statements
  ctrl-review-<round>-packet.md     # immutable review packet, no concerns or conclusions
  ctrl-review-<round>-brief-R<k>.md # frozen emphasis brief, one per reviewer
  ctrl-review-<round>-R<k>.md       # one frozen reviewer report per reviewer, never merged
  ctrl-review-<round>-synthesis.md  # post-freeze synthesis, never shown to reviewers
  ctrl-response-<round>-R<k>.md     # one reviewer-facing reply per reviewer, kept separate
  ctrl-response-<round>-internal.md # author-side synthesis, never reviewer-facing
  lit/                          # literature artifacts
  exp/                          # experiment configs, logs, and result tables
  fig/                          # figure scripts, sources, and exports
  ms/                           # manuscript sources
  slides/                       # generated decks
  repro/                        # reproducibility package inventory
```

## Ledger format

`ctrl-claims.md` is the spine of the pack. Every quantitative claim in the manuscript must have
exactly one row, and every row must resolve.

```markdown
| ID | Tier | Claim (as it will appear) | Value | Units | Boundary | Source artifact | Protocol ID | Gate |
|----|------|---------------------------|-------|-------|----------|-----------------|-------------|------|
| C1 | measured | our method reaches 78.4 mAP on MSMT17 | 78.4 | mAP | single query, no re-ranking, 3 seeds | exp/msmt17_main/results.json | P-reid-1 | G2 pass |
| C2 | reported | BoT reports 76.4 under the same protocol | 76.4 | mAP | copied from Table 3, read in full | refs/bot2022.pdf | P-reid-1 | G2 pass |
| C3 | assumed | 5 percent ranging outliers | 5 | percent | stress case, sensitivity in Fig. 4 | ctrl-plan.md | P-cnav-2 | G2 pass |
```

Column rules: `Tier` is `measured` / `reported` / `assumed`; `Value` carries no units and no
percent sign, since `Units` holds them; `Boundary` states the validity limit in one clause;
`Source artifact` is a resolvable relative path or a full citation; `Protocol ID` links to the
relevant block in `ctrl-protocol.md`; `Gate` is the gate status of that row.

A row whose `Source artifact` cannot be resolved is a G2 failure. Do not delete the row to make
the gate pass; obtain the evidence or remove the claim from the manuscript and mark the row
`withdrawn` with the reason.

## Protocol block format

`ctrl-protocol.md` holds one block per comparison. `ctrl-shared` `core/gate-contract.md` lists
the fields each axis requires. A comparison may not be reported as a delta unless its block is
complete.

```markdown
## P-reid-1: main comparison on MSMT17
- Axis: reid
- Dataset and split: MSMT17, official train/test split, 4,101 identities (1,041 train, 3,060 test)
- Backbone and pretraining: ResNet-50-IBN, ImageNet, identical for all arms
- Input: 384x128, random erase 0.5, no re-ranking on any arm
- Query/gallery: official single-query protocol
- Seeds: 3 runs, mean reported, standard deviation in Table 2
- Arms: ours, BoT (re-implemented), TransReID (reported; protocol differences: ViT-B/16 backbone and 256x128 input)
- Comparability verdict: ours vs BoT comparable; ours vs TransReID not comparable, reported separately
```

## Gate log format

`ctrl-gates.md` is append-only. Never edit a past entry; append a new one.

```markdown
## 2026-10-03 G2 evidence freeze
- Status: FAIL
- Checked: ledger resolvability, protocol matching, number reconciliation, axis addenda
- Artifact: ctrl-claims.md
- Failing criterion: C7 cites a tracking MOTA with no detector provenance
- Smallest clearing change: add the detector checkpoint and public/private label to C7
- Waiver: none
```

## Manuscript and slide naming

- Manuscript sources: `ms/main.tex` or `ms/main.md`, with sections named after the section, not
  after a version.
- Figures: `fig/fig<number>-<short-slug>.<ext>`, for example `fig/fig3-cnav-topology.pdf`.
  Every figure has its generating script beside it as `fig/fig3-cnav-topology.py`.
- Slides: `slides/<venue>-<year>-<slug>.pptx`, with the outline kept as
  `slides/<venue>-<year>-<slug>-outline.md` so the deck can be regenerated.
- Response letters: per-reviewer files `ctrl-response-<round>-R<k>.md`, plus an author-side
  `ctrl-response-<round>-internal.md` for any cross-reviewer synthesis, which is never
  reviewer-facing.

## Non-negotiables

- Never overwrite a frozen artifact. A revision creates a new file or appends a dated entry.
- Never place a synthesis in a reviewer-facing file, and never place one reviewer's report
  where another reviewer's context can read it.
- Every generated file that carries a claim must appear in the ledger's `Source artifact`
  column, or the claim it carries is unsourced.
- Keep the raw artifact (log, JSON, CSV) beside any derived table. A table without its source
  data cannot be audited and fails G2.

## Final checklist

Run before declaring any deliverable complete.

```text
[ ] Every gate the workflow requires has a status entry in ctrl-gates.md
[ ] Every quantitative claim has a ledger row with a resolvable source
[ ] Every comparison has a complete protocol block for its axis
[ ] No artifact was overwritten; revisions are new files or dated entries
[ ] Reviewer-facing and synthesis artifacts are separate
[ ] Every figure has its generating script
[ ] Every headline number reproduces from the recorded provenance
[ ] The final message states what was verified and what remains unverified
```
