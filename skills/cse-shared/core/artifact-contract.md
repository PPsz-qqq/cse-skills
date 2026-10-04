# Artifact contract

Use these stable names under the user's chosen project directory unless they ask otherwise.
Short conversational work may remain inline; never create research outputs inside an installed
skill bundle. Ask once for an output directory when needed, then retain that choice.

## Workspace layout

```text
<project>/
  cse-artifacts.md                # index of current artifact revisions
  cse-scope.md                    # G0 scope block and axis selection
  cse-plan.md                     # first G1 confirmatory plan
  cse-pilots.md                   # exploratory pilot questions, budgets and outcomes
  cse-claims.md                   # claim-to-evidence ledger
  cse-protocol.md                 # protocol blocks, one per comparison
  cse-gates.md                    # gate history, append-only
  cse-venues.md                   # venue fit and dated guideline checks
  cse-review-<round>-packet.md     # immutable packet, no concerns or conclusions
  cse-review-<round>-brief-R<k>.md # frozen lens, one per reviewer
  cse-review-<round>-R<k>.md       # frozen report, one per reviewer
  cse-review-<round>-synthesis.md  # post-freeze author-side synthesis
  cse-revision-<round>-ledger.md   # comment/promise/result tracking, author-side
  cse-revision-<round>-plan.md     # work packages, owners, costs and dependencies
  cse-response-<round>-R<k>.md     # reviewer-facing replies
  cse-response-<round>-internal.md # author-side cross-reviewer notes
  cse-response-<round>-cover.md    # editor-facing cover letter, when required
  lit/query-plan.md                # queries, windows, filters and expansion budget
  lit/source-ledger.md             # identifiers, versions, read depth and claim support
  lit/competitors.md               # closest works and checkable differences
  lit/synthesis.md                 # findings, gaps, coverage and stop reason
  exp/                            # configs, logs, raw metrics and derived tables
  fig/                            # source figures, scripts and exports
  ms/                             # manuscript sources and frozen snapshots
  slides/                         # outlines, generators and decks
  repro/                          # reproducibility inventory
```

## Revision resolution

Stable names identify logical artifacts, not permission to overwrite a freeze. Keep the first
frozen version; subsequent freezes use a revision suffix, for example `cse-plan-r2.md` or
`cse-claims-r3.md`. Append-only logs may receive dated entries without rewriting old entries.
Working manuscript files may be edited until frozen; preserve each assessed/submitted snapshot.

When a revision changes the current path, update `cse-artifacts.md`:

```markdown
| Artifact | Current path | Revision/hash | State | Updated |
|---|---|---|---|---|
| scope | cse-scope.md | <sha256> | frozen | <timestamp with zone> |
| plan | cse-plan-r2.md | <sha256> | frozen | <timestamp with zone> |
| claims | cse-claims-r3.md | <sha256> | frozen | <timestamp with zone> |
| manuscript | ms/main-r2.tex | <sha256> | frozen | <timestamp with zone> |
```

Downstream skills read this index first when it exists, then read the exact current files and
verify their revisions. Without an index, use the stable names; if multiple plausible revisions
exist, ask rather than silently selecting one. Old claims/concerns retain stable IDs across
revisions. New IDs are never recycled. Gate entries record exact artifact revisions and scope.

Before 2026-10-04 these artifacts were named with a `ctrl-` prefix (`ctrl-artifacts.md`,
`ctrl-claims.md`, and so on). In a project that already has them, read `ctrl-<name>` as the same
logical artifact as `cse-<name>`, prefer whichever the index lists, and never rename a frozen file
to change its prefix. New files use `cse-`; record the mapping in the index when both exist.

## Claim ledger

Each distinct claim has one stable row; repeated occurrences refer to that ID. Both scientific
results and declared assumptions are tracked. Placeholders below are templates, not measurements
or verified bibliographic facts.

```markdown
| ID | Tier | Provenance | Setting | Claim | Value | Units | Boundary | Source artifact | Source revision/location | Verification | Protocol ID | Comparability | Gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | measured | original | benchmark | <our result> | <value> | <unit> | <split, runs> | <raw artifact> | <hash, key> | verified | P-reid-1 | <pair verdict or NOT_APPLICABLE> | <G2 verdict> |
| C2 | reported | copied | benchmark | <source reports a result> | <value> | <unit> | <source's protocol> | <primary source path/URL> | <DOI/version, table/row> | <verified or UNVERIFIED> | P-reid-1 | <pair verdict> | <G2 verdict> |
| C3 | assumed | design | simulation | <stress-test assumption> | <parameter> | <unit> | <scenario and sensitivity> | <plan/config> | <hash, section> | <documented assumption> | P-cnav-1 | NOT_APPLICABLE | <G2 verdict for assumption only> |
```

Column rules:

- `Tier` is `measured` / `reported` / `assumed`. `re-implemented` is provenance, not a tier.
  Setting is separate; a measured simulation remains simulation evidence.
- `Value` holds no unit or percent sign; `Units` defines scale/convention. Non-numeric proof or
  synthesis claims may use `NOT_APPLICABLE` in Value/Units with their evidence pointer retained.
- `Boundary` includes the applicable dataset/split, setting, runs, hardware and assumptions.
- `Source artifact` points upstream to the raw log, config, proof or primary published source,
  not back to the manuscript/slide that repeats the claim. Location and revision make it auditable.
- `Verification` distinguishes checked artifacts from user-supplied assertions or inaccessible
  sources. Supplied numbers may be retained as supplied without fabricating a verified G2 PASS.
- `Protocol ID` resolves to the current indexed protocol file. Use `NOT_APPLICABLE` with a reason
  for non-comparative claims. `Comparability` is per arm pair, not an unconditional table verdict.
- `Gate` records the scoped verdict. Documented assumptions can pass only as assumptions. This
  never promotes them to measured outcomes. Freshness is tracked with the audited revision.

If a source is missing, obtain it or withdraw/narrow the dependent claim. Keep the historical row
marked `withdrawn` with a reason; do not delete losing evidence to make a gate pass.

## Protocol blocks

Use [protocol-blocks.md](../../cse-experiment-suite/references/protocol-blocks.md) for exact fields.
One block per comparison, stable IDs such as `P-reid-1`, per-arm deviations and per-pair verdicts.
Only matched comparisons support delta claims; reported external rows keep their own protocol.

## Gate history

Append a dated entry using [gate-contract.md](gate-contract.md): verdict, scope, checked criteria,
artifact paths/revisions, freshness, missing/failing criterion, clearing change and any permitted
waiver. A revision invalidates dependent evaluations; append a re-evaluation, not a rewritten past.

## Manuscript, figure and slide naming

- Working manuscript: `ms/main.tex` or `ms/main.md`; frozen snapshots use revision suffixes.
- Figures: `fig/fig<number>-<slug>.<ext>`. Generated figures keep their generator and input data.
  Reused external figures keep their source/version and permission/credit; no fictional generator
  is required for a supplied figure. A newly drawn schematic keeps an editable source.
- Slides: `slides/<venue>-<year>-<slug>.pptx`, with its outline and build script beside it.
  Presented or submitted decks are frozen; create a new revision rather than overwriting them.
- Reviewer-facing files stay separate from author-side ledgers and synthesis. Venue-required
  combined uploads may assemble labelled reviewer sections without leaking restricted comments.

## Final checklist

```text
[ ] Every applicable gate has a scoped verdict with exact revisions; no unrun PASS
[ ] Every substantive claim resolves upstream, without a circular provenance chain
[ ] Every comparison has the applicable complete protocol and a per-pair verdict
[ ] Current revisions are unambiguous and frozen artifacts were not overwritten
[ ] Reviewer-facing and restricted author-side material remain separated
[ ] Generated figures have generators; reused figures have sources and credit
[ ] Headline values reconcile with recorded provenance
[ ] Verification limits, unchecked render/rehearsal steps and the next dependency are stated
```
