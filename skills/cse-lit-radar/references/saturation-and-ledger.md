# Saturation, stop rules, and the nearest-competitor ledger

The loop budget is finite and declared in advance. The loop ends by rule, and the rule that ended it
is reported. The ledger produced at the end of the loop is what feeds the G0 "closest competing
papers" field.

## The saturation rule

Budget is three expansions. Expansion 1 is the directed search; expansion 2 is backward citation;
expansion 3 is forward citation plus the adjacent-subcommunity sweep.

The stop rule is marginal yield. Stop when an expansion adds no new distinct relevant item, or when
the marginal yield falls below the declared threshold for that effort tier. Declare the threshold
before running the expansion, not after counting.

| Effort tier | Corpus target | Expansions | Marginal-yield threshold to continue | Deep reads required |
|---|---|---|---|---|
| `sketch` | 6 to 8 works | 1 | not applicable, single pass | 2 |
| `standard` | 10 to 15 works | up to 2 | at least 3 new distinct relevant items | 5 |
| `thorough` | 18 to 25 works | up to 3 | at least 3 new distinct relevant items | 8 |
| `submission` | 30 or more works | up to 3 | at least 5 new distinct relevant items | 12 |

Count "new distinct relevant" strictly. A second copy of a work already in the ledger is not new. A
work that is topically adjacent but establishes nothing the claim needs is not relevant. A work you
have not opened is not counted as relevant, only as retrieved.

Report the loop outcome in exactly one of these forms.

```text
Loop outcome: converged - expansion <n> added <k> new distinct relevant items, below the declared
threshold of <t>, so the loop stopped by rule after <n> expansion(s).

Loop outcome: budget exhausted with residual defects - <n> of <declared tier budget> expansions
run; saturation was not demonstrated, with these residual coverage gaps: <list>. A one-pass sketch
is budget-limited, not proof of saturation. Corpus/deep-read targets are planning guides, never quotas.

Loop outcome: stopped by user - the user ended the search at expansion <n>, with these residual
coverage gaps: <list>.
```

"Examined the literature thoroughly" and "iterated a few times" are not reports.

## What a saturation claim does and does not mean

Saturation is a statement about your search, not about the field. The honest form is "the recorded
queries returned no new distinct relevant items at expansion three". It does not mean no such work
exists, and it does not license "the first to".

The novelty promotion condition in
[../../cse-shared/core/verdicts-and-loops.md](../../cse-shared/core/verdicts-and-loops.md) requires a
documented search of recent venue cycles plus the foundational line of work, with the near misses
listed. The permitted statement is bounded by the recorded sources, windows and queries, which is
why it is achievable and why an unbounded "first to" claim is not. A two-cycle window alone never
proves historical priority.

## Nearest-competitor ledger

Three to five rows. Fewer is acceptable only when the search genuinely returned fewer; say so.

```markdown
| Rank | Work | Axis overlap | The one axis on which we differ | Evidence for the difference | Overlap severity |
|------|------|--------------|--------------------------------|-----------------------------|------------------|
| 1 | <author year, venue> <identifier> | det, small-object | we predict dense clusters; they predict per-object heatmaps | their Sec. 3.2 and Eq. (4), read in full | high |
| 2 | | | | | medium |
| 3 | | | | | low |
```

Column rules.

- `Rank` is by threat to the novelty claim, not by citation count or recency. The most threatening
  work is the one closest to your mechanism, even if it is older or less cited.
- `Axis overlap` lists the axes from the five-axis set that the work also addresses. A work that
  overlaps on two axes is more threatening than one that overlaps on one.
- `The one axis on which we differ` must be a single axis and must be checkable. "Better
  performance" is not an axis. "Handles the crossing case by a learned motion prior rather than an
  appearance model" is.
- `Evidence for the difference` is a location in the primary source, with the read depth. A
  difference asserted from the abstract is a hypothesis, not a difference.
- `Overlap severity` is `high` when a reviewer would likely call the work a concurrent version of
  yours, `medium` when the setting differs but the mechanism is close, `low` when only the task
  overlaps.

## Gap statement format

A gap is an observation across the corpus, not the absence of a retrieval. Write it with its support.

```markdown
Gap G<n>: <one sentence>
- Observed across: <at least three works, with identifiers>
- The pattern: <what all of them do, or all of them omit>
- Why it matters: <the consequence for the task, not for your paper>
- What would close it: <the experiment or analysis that would, stated as a result>
- Nearest work that could close it first: <work, and why it does not>
```

A gap supported by fewer than three works is a hunch. Label it as a hunch and put it in the
unresolved list rather than in the related-work narrative.

## Handoff to the scope block

The ledger supplies the G0 fields, and nothing else may be substituted for it.

```text
Closest competing papers: <rank 1 to 3 from the ledger, each with the differing axis in one clause>
Novelty statement permitted by this search: <"no directly overlapping work retrieved under the
  recorded queries dated <window>" or the weaker true form>
Search record: <path to the ledger and the query plan>
```

If the ledger's top row is a `high` overlap severity on your primary mechanism, the novelty claim is
not available and the G0 claim type must change, usually from a novelty-framed contribution to an
empirical-delta or mechanism contribution. Report that downgrade rather than dressing it up.

## Anti-patterns

- Declaring saturation after one expansion because the results looked familiar.
- Counting retrieved items as relevant items.
- Listing competitors that do not actually compete, to make the novelty claim easier.
- Omitting a competitor that a reviewer is certain to know.
- Running expansion 2 and 3 with the same query and the same index, which reproduces the same set and
  manufactures convergence.
- Writing the threshold after counting the yield, which converts a rule into a rationalisation.
