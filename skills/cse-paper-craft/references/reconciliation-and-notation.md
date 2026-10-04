# Number reconciliation and notation consistency

Two passes that run after the content is settled and before anything is frozen. Both are mechanical
and both must be complete before a freeze. Under
[evidence-integrity.md](../../cse-shared/core/evidence-integrity.md) Rule 4, a value that differs
between surfaces beyond rounding, or a superlative contradicted by the paper's own table, is an
integrity failure rather than a copy-editing issue. The same value printed at two precisions or in
two units is a consistency defect: fix it before the freeze, and rate it `Minor` unless the rounding
changes a comparison, a ranking or a claimed threshold.

## Pass 1, number reconciliation

Run this on the frozen draft. Every line is a check with a verdict, not a reading task.

### 1.1 Build the number inventory

For a full freeze, inventory every scientific quantity in the manuscript, not section numbers,
reference indices or page labels. For a scoped edit, inventory the changed passage and dependencies
and report that limit. A sampled diagnostic is honest only when size/rule are stated; no evaluator
false-positive rate can be estimated without adjudicated ground truth, per
[verdicts-and-loops.md](../../cse-shared/core/verdicts-and-loops.md).

```text
| Number ID | Value | Units | Where it appears | Precision | Ledger row | Protocol ID | Source artifact |
|---|---|---|---|---|---|---|---|
| N1 | 78.4 | mAP | abstract, Table 2, Sec. 4.3, conclusion | 1 decimal | C1 | P-reid-1 | exp/reid-1/metrics.json |
```

Every row resolves to a ledger row in `cse-claims.md`. A number with no ledger row is unsourced,
and `G2` fails on it.

### 1.2 Check the four surfaces

The abstract, the tables, the figure captions, and the conclusion must agree on every shared
number, at the same precision, in the same units.

```text
[ ] Every abstract number appears in the body with the identical value and precision
[ ] Every number in a figure caption appears in the body text or the table it describes
[ ] Every number in the conclusion appears identically in the abstract or the tables
[ ] No quantity appears at two precisions, such as 78.4 in the abstract and 78.42 in a table
[ ] No quantity appears in two units, such as seconds in the text and milliseconds in a table
[ ] Each surface's claims are no stronger than the table's matched-protocol result
```

### 1.3 Check aggregates

```text
[ ] Every average reproduces from the per-item values shown, or the aggregation rule is stated
[ ] Every mean states its run count and its dispersion statistic
[ ] Percentages state absolute or relative, next to the value
[ ] Every delta is computed against the row it claims as its baseline, not against a neighboring row
[ ] Every bolded value is the best under a matched protocol, checked cell by cell
[ ] Any total that sums per-class, per-sequence, or per-node values was summed from those values
```

### 1.4 Check claim strength

```text
[ ] Every `outperforms` has a protocol-matched comparison for that specific baseline
[ ] Every `significantly` has a test, named, with its result
[ ] Novelty is bounded by recorded recent/foundational search, near misses and coverage limits; no two-cycle first proof
[ ] Every field or hardware claim traces to field or hardware data
[ ] Every mechanism sentence traces to a singleton ablation arm
[ ] No claim in the abstract is missing from the ledger, and no ledger row is `STALE`
```

### 1.5 Check protocol adjacency

The axis protocol labels travel with the number, in the tables, not only in the protocol section.
`det` numbers carry resolution and TTA where rows differ; `track` numbers carry online or offline and
public or private in the table; `reid` numbers carry single or multi query and re-ranking on or off;
`cnav` numbers carry the architecture label and the message budget; `filt` numbers carry the Monte
Carlo count and the covariance policy; and every `not comparable` value is marked where it appears,
including in a caption.

### 1.6 Reconciliation outcomes

| Outcome | Action |
|---|---|
| the number has a ledger row, matches everywhere, and its protocol is matched | `pass`, no action |
| the number has no ledger row | `FAIL`: obtain the evidence or remove the number from the manuscript |
| the value differs between surfaces beyond rounding | `FAIL`, integrity: reconcile every surface against the ledger row and report the corrected value |
| the same value appears at two precisions or in two units | `WARN`, consistency defect: propagate the ledger's precision and unit before the freeze; `FAIL` if the rounding changes a comparison, a ranking or a threshold |
| the number is copied under a different protocol | mark it `not comparable` and keep it out of the headline delta |
| the ledger row changed after the number was written | the verdict is `STALE`, recompute it and re-propagate |
| a superlative is contradicted by the table | `FAIL`: delete the superlative or report the contradicting case |

Report the reconciliation as a table of outcomes with counts, so that a partially checked
manuscript cannot be described as fully reconciled.

## Pass 2, notation consistency

Uses `../../cse-shared/core/terminology-and-notation.md` as the reference. Where the user's draft
already uses a consistent symbol set, keep the user's set and record the deviation rather than
rewriting notation mid-manuscript.

### 2.1 Symbol pass

Every symbol is defined at first use in the text rather than only in a figure or a table, has exactly
one meaning across the manuscript, and no two symbols denote the same object in text, figures, or
algorithms. Symbols follow the pack convention or the draft's own consistent set with the deviation
noted, subscripts and superscripts are consistent including markup in text versus equations, vector
and matrix conventions are stated once and held including transpose and norm notation, estimated and
true quantities are distinguished, time and agent and sensor indices use the same letters throughout,
and notation in the appendix matches the main text.

For `filt`, the symbol set (`x_k`, `z_k`, `u_k`, `F_k`, `H_k`, `Q_k`, `R_k`, `P_k`, `K_k`,
`epsilon_k`, `N`) carries correctness risk, not only readability. A `P_k` used for two different
covariances in one derivation is a defect a reviewer will find.

### 2.2 Acronym pass

Every acronym is expanded at first use and used consistently in the short form after, no acronym is
expanded twice in the same section, none appears in the title or the abstract without expansion,
acronyms in figures and captions match the text usage, and abbreviations in tables are explained in
the caption rather than in the text three pages away.

### 2.3 Bilingual pass

The Chinese and English abstracts must describe the same claims with the same numbers and the same
units, symbols, and equation numbering. The Chinese abstract is a real summary rather than a
sentence-by-sentence translation of the English one. Terminology follows the mapping in
`../../cse-shared/core/terminology-and-notation.md` or the venue's own usage, 创新点 is stated as an
explicit list where the venue expects it, no figure carries Chinese labels in an English submission
or the reverse, and 中图分类号, 文献标识码, and 基金项目 fields are present where the venue requires
them.

### 2.4 Reference pass

Never generate a bibliography entry from memory. A fabricated or mismatched citation costs the most
credibility per unit of effort, it is invisible in a compiled PDF, and it is the one defect a reader
can check in seconds. Fetch every entry from a source of record and verify it, or leave a visible
placeholder. Every citation in the text appears in the reference list and the reverse, numbering is
sequential in first-appearance order where the venue requires it, formatting follows the venue or,
for Chinese venues, the GB/T 7714 edition the journal names (GB/T 7714-2025 replaced the 2015
edition on 2026-07-01), every DOI, venue, year, and page range was checked against the
source rather than from memory, no citation was added as decoration, read-in-full and abstract-only
and title-only sources are distinguished where the support matters, and no invented citation or
invented result is attributed to a real paper.

The gate, applied per entry.

| Situation | Action |
|---|---|
| entry fetched from a source of record, and the cited claim confirmed in the paper | use it |
| the paper exists but the entry cannot be fetched | insert a placeholder and notify the author |
| the paper's identity is uncertain | insert a placeholder and notify the author |
| the claim is recalled but the source is not located | search first; never cite from recall |

Two rules make the gate real. Confirm the paper exists in at least two independent sources before
citing it, because a DOI can resolve to the wrong work and existence is not claim support
(`../../cse-shared/core/evidence-integrity.md` Rule 10). Then read the cited paper and confirm the
specific claim appears in it, since a real reference attached to a claim it does not make is
indistinguishable from a fabrication to the reader who checks. Placeholders are visible and
greppable so that none can ship, using one fixed high-signal token that a final pass searches for,
with every unresolved placeholder listed for the author rather than resolved from memory, as in
`\cite{PLACEHOLDER_author2026_verify}` followed by a `CITATION-PLACEHOLDER` comment on that line.
A placeholder is a correct output. A confident entry generated from memory is not, and a
bibliography assembled from recall fails `G2` on the same footing as an invented number.

### 2.5 Figure and table pass

```text
[ ] Every figure and table is cited in the text, in numerical order
[ ] Generated figures keep generators/data; reused figures keep source/version and credit; schematics keep editable source
[ ] Axis labels carry units, and the frame is stated where a frame applies
[ ] Color choices survive greyscale printing and the common forms of color-vision deficiency
[ ] Font sizes in figures match the body text after scaling to the column width
[ ] Captions are self-contained, stating what is plotted and under which protocol
[ ] No figure asserts a claim, through an arrow or an annotation, that the text does not support
```

### 2.6 Style pass

The house rule from `../../cse-shared/core/terminology-and-notation.md` applies. No em dash, en dash,
or colon used as a habitual sentence connector, and ordinary hyphens stay in compounds and in
identifiers such as `det-C1` and `G2`.

```text
[ ] No em dash or en dash as a sentence connector
[ ] No colon used as a habitual connector outside lists, definitions, and block intros
[ ] One term per object across the manuscript and any companion deck or response letter
[ ] `robust` never appears without the perturbation class it is robust to
[ ] `detection` and `localization` are not used interchangeably
[ ] `tracking` and `trajectory prediction` are not used interchangeably
[ ] `cooperative` is not used to imply a distributed implementation
[ ] `fusion` names its type: measurement, state, track-to-track, or covariance intersection
[ ] `state-of-the-art` appears only with the matched comparison that supports it
[ ] `novel`, `effective`, and `efficient` each have an artifact behind them or are deleted
```

## Freeze protocol

```text
[ ] Number inventory complete, no sampling
[ ] Every inventory row resolves to a ledger row that is not STALE
[ ] Four-surface agreement checked; aggregate reproduction checked
[ ] Claim strength checked against the promotion conditions
[ ] Protocol labels present next to the numbers that need them
[ ] Symbol, acronym, bilingual, reference, figure, and style passes run
[ ] The reconciliation outcome table is recorded, with counts
[ ] Any RED line failure removed the claim or produced the evidence, not a hedge
```

Never mark a reconciliation `PASS` on a revision that changed after the pass. The verdict is valid
only for the exact revision it was computed from (`../../cse-shared/core/verdicts-and-loops.md`).
