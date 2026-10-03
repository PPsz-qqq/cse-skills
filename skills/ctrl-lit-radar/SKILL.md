---
name: ctrl-lit-radar
description: >-
  Literature intelligence for control-science-and-engineering research across object detection
  (目标检测), tracking (目标跟踪), re-identification (重识别), cooperative navigation (协同导航) and
  filtering or state estimation (滤波). Use it for a literature review (文献综述), a related-work
  section (研究现状), a literature search for a gap, an opening report or topic selection (开题,
  选题), a novelty check before claiming 创新点, the closest-prior-work field of a G0 scope block,
  venue-cycle tracking, and a nearest-competitor ledger. It constructs per-axis queries against
  arXiv, OpenAlex, Semantic Scholar, Crossref, PubMed and IEEE Xplore, grades every source by how it
  was read, applies a three-expansion saturation stop rule, and never reports a number it did not
  read at first hand.
---

# CTRL literature radar

Build the evidence base a claim will stand on, and stop at a declared point instead of at exhaustion.

## Default stance

- A search result is a candidate, not a source. Nothing enters an artifact until it has been read to
  the depth its role requires.
- Cite the depth you actually reached. "Read in full", "abstract only" and "title only" are three
  different grades and only the first may carry a numeric claim. See
  [references/evidence-grading.md](references/evidence-grading.md).
- An empty result is a result. "No directly overlapping work was retrieved under these keywords"
  is an honest and publishable statement. "First to do X" is not, unless the search that supports it
  is recorded. This is the novelty promotion condition in
  [../ctrl-shared/core/verdicts-and-loops.md](../ctrl-shared/core/verdicts-and-loops.md).
- Search in the language the subcommunity publishes in. A Chinese-language query set and an English
  one retrieve nearly disjoint corpora for the same axis. Run both.
- Stop by rule, not by fatigue. The loop budget is three expansions, and the stop rule is marginal
  yield. See [references/saturation-and-ledger.md](references/saturation-and-ledger.md).
- Venue facts decay every cycle. Deadlines, tracks, page limits and anonymity rules are re-verified
  at the point of use, never carried forward from a previous project.

## Workflow

1. **Fix the request shape.** Record the axis (`det` / `track` / `reid` / `cnav` / `filt`), the claim
   type the literature must support, the target venue class, the reading language, and the effort
   tier (`sketch` / `standard` / `thorough` / `submission`) from
   [../ctrl-shared/core/verdicts-and-loops.md](../ctrl-shared/core/verdicts-and-loops.md). State the
   tier out loud, because it sets the corpus size and the number of expansions.

2. **Write the query plan before searching.** One block per (axis, source) pair. Give the boolean
   string, the field filters, the date window, and the expected yield. Use
   [references/query-recipes.md](references/query-recipes.md). A query plan written after seeing the
   results is not a plan.

3. **Run expansion 1, the directed search.** Start from the axis seed terms and the user's own
   pain point. Collect titles, identifiers, years, venues, and nothing else yet.

4. **Deduplicate across indexes on identifiers, not titles.** Prefer arXiv identifier, then DOI
   lowercase, then a title key. A near-identical title is a match candidate, not a match. Cross-index
   triangulation rules are in [references/evidence-grading.md](references/evidence-grading.md).

5. **Run expansions 2 and 3.** Expansion 2 is backward citation of the strongest hits. Expansion 3 is
   forward citation plus the adjacent-subcommunity source the first two missed (for example a control
   venue for a `track` paper, or a remote-sensing venue for a `det` paper). Record the marginal yield
   of each expansion as new distinct relevant items.

6. **Read to the required depth.** For each item that will carry a claim, open the primary source and
   read the specific table, section or figure the claim needs. Record the location. If the full text
   is inaccessible, the item is downgraded and the claim it would have carried is marked
   `[UNVERIFIED]`.

7. **Grade every source.** Assign the read depth and the tier (`measured` / `reported` / `assumed`).
   Apply the citation audit rate targets (false negative below 0.15, false positive below 0.10) to a
   stated sample, and report the sample size and the sampling rule. See
   [references/evidence-grading.md](references/evidence-grading.md).

8. **Build the nearest-competitor ledger.** For each of the three to five closest works, record the
   one axis on which you differ and the evidence for that difference. Use the format in
   [references/saturation-and-ledger.md](references/saturation-and-ledger.md). This table is the input
   to the G0 "closest competing papers" field, and to the novelty promotion condition.

9. **Map each candidate benchmark to what it can and cannot establish.** Consult
   [references/dataset-benchmark-atlas.md](references/dataset-benchmark-atlas.md). A benchmark that
   cannot see your failure mode is not evidence for your claim, however standard it is.

10. **Decide saturation and report the stop reason.** Apply the rule in
    [references/saturation-and-ledger.md](references/saturation-and-ledger.md). Report the loop
    outcome as `converged`, `budget exhausted with residual defects`, or `stopped by user`. "Searched
    extensively" is not a report.

11. **Check the venue cycle if a submission is in scope.** Verify the current call for papers, the
    track, the deadline and the anonymity rule at the venue's own site, and date-stamp the check. See
    [references/venue-cycle-tracking.md](references/venue-cycle-tracking.md).

12. **Emit the artifacts.** Write the ledger and the synthesis under the project's `lit/` directory
    named in [../ctrl-shared/core/artifact-contract.md](../ctrl-shared/core/artifact-contract.md),
    then report the gate status using the block in
    [../ctrl-shared/core/gate-contract.md](../ctrl-shared/core/gate-contract.md).

## Output format

```text
Literature radar report
- Axis: <det | track | reid | cnav | filt>   Effort tier: <sketch | standard | thorough | submission>
- Claim the literature must support: <one sentence>
- Query plan: <path to the query plan block>   Expansions run: <1 | 2 | 3>
- Loop outcome: converged | budget exhausted with residual defects | stopped by user
- Marginal yield: expansion 2 <n> new distinct relevant; expansion 3 <n> new distinct relevant

| # | Work (author year, venue) | Identifier | Read depth | Tier | What it establishes | Where we differ |
|---|---------------------------|------------|------------|------|---------------------|-----------------|
| 1 | | arXiv: / DOI: | full / abstract / title | measured / reported / assumed | | |

Nearest competitors, strongest first
- <work>: differs on <axis>; evidence <location in the primary source>

Benchmark mapping
| Benchmark | Establishes for us | Protocol trap | Cannot establish |
|---|---|---|---|
| | | | |

Gaps the corpus supports
- <gap>: <the observation across at least three works that makes it a gap, not an absence>

Unresolved
- <item>: [UNVERIFIED] <what would resolve it, and roughly what it costs>

Gate G0 scope: PASS | FAIL | BLOCKED
- Checked: <criteria evaluated>
- Artifact: <path>
- Failing criterion: <one line, only when not PASS>
- Smallest clearing change: <one line, only when not PASS>
- Waiver: none
```

## Red lines

- Never report a number, dataset statistic, baseline value or hardware fact from memory. Read it at
  first hand or mark it `[UNVERIFIED]`.
- Never present an abstract-only source as support for a specific numeric claim.
- Never write "the first to" or "no prior work" without the recorded search that supports it, and
  never let the absence of a retrieval stand in for absence of the work.
- Never let a search tool's summary replace the primary source. Search summaries are pointers.
- Never merge two works that differ only slightly in title into one entry without opening both.
- Never pad a reference list to reach a count, and never drop a work that contradicts the claim.
  A contradicting work belongs in the ledger with a stated resolution.
- Never carry a venue deadline, page limit or anonymity rule forward from memory or from
  [../ctrl-shared/core/venue-matrix.md](../ctrl-shared/core/venue-matrix.md) without re-verifying it.
- Never encode an API key, token or paid-account credential in a search script or in an artifact.
  Public endpoints and the user's own institutional access only.

## Related files

| File | Open when |
|---|---|
| [references/search-protocol.md](references/search-protocol.md) | You need per-source access notes, field semantics, and the no-credential policy |
| [references/query-recipes.md](references/query-recipes.md) | You are constructing queries for an axis, in English or Chinese |
| [references/evidence-grading.md](references/evidence-grading.md) | You are grading a source, deduplicating across indexes, or auditing citation support |
| [references/saturation-and-ledger.md](references/saturation-and-ledger.md) | You are running expansions, deciding to stop, or filling the nearest-competitor ledger |
| [references/venue-cycle-tracking.md](references/venue-cycle-tracking.md) | You are choosing or re-verifying a target venue, track, or deadline |
| [references/dataset-benchmark-atlas.md](references/dataset-benchmark-atlas.md) | You are selecting a benchmark or stating what a benchmark cannot establish |
