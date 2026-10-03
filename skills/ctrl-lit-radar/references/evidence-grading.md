# Evidence grading and citation audit

How much a source may carry, and how to check that the citation you wrote actually supports the
sentence you wrote. This file is the operational form of
[../../ctrl-shared/core/evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md) for the
literature stage.

## Read depth grades

Assign one grade per source, per use. The same paper can be `full` for one claim and `title` for
another, and the grade attaches to the use.

| Grade | What you did | May carry |
|---|---|---|
| `full` | opened the primary source and read the section, table or figure the claim needs | a specific number with its protocol, a method description, a mechanism claim |
| `methods` | read the method and the result table, not the whole paper | a method description and a table value with its stated protocol |
| `abstract` | read the abstract only | a directional statement, a task framing, a claim about what the paper addresses |
| `title` | saw the title in a list | a mention that the work exists and is related; nothing else |
| `secondary` | read a description inside another paper's related work | attribution of a research direction; never a number |

Rules that follow from the grades.

- A numeric claim requires at least `methods` depth on the source that carries it.
- A protocol-difference claim requires `methods` depth, because the protocol usually lives in the
  implementation-details section, not the abstract.
- A "this is the state of the art" claim requires `methods` depth on the claimed best result and
  knowledge of the benchmark's current leaderboard.
- An `abstract` grade is honest and useful. Presenting an abstract as if it were read in full is not.

## Tier assignment

The tier (`measured` / `reported` / `assumed`) is defined in
[../../ctrl-shared/core/evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md). In the
literature stage, almost everything you collect is `reported`. Two recurring mistakes.

- A number copied from a survey is still `reported`, and the survey is a secondary source. Cite the
  original, or cite the survey and say so.
- A number you recomputed from a published table is still `reported` unless you ran the evaluation.
  State that you recomputed it and from which table.

## Cross-index triangulation

Deduplicate on identifiers, in this order.

1. arXiv identifier without the version suffix.
2. DOI, lowercased.
3. A title key built from the normalised title.

Then classify each merged record.

| Class | Condition | Action |
|---|---|---|
| `confirmed` | resolves in at least two indexes with matching title, authors and year | merge and use the version of record |
| `partial-match` | resolves in one index only, or metadata fields disagree | keep both identifiers in one row, flag the disagreement, resolve by hand before citing |
| `contaminated` | preprint and record differ in a reported number, or the record has a retraction notice | cite the version of record, report the difference if the number is central |
| `unmatched` | DOI in the citation does not resolve to the title it is attached to | treat the citation as suspect; do not propagate it |

The `unmatched` class is the important one. A DOI that resolves to a different title is the
signature of an invented or garbled reference, and it propagates through co-author chains and
reference lists for years.

## Citation support audit

Audit whether the sentences that cite sources are actually supported by them. This is a different
check from reference existence.

Procedure.

1. Build the audit set: every sentence in the draft that carries a citation and a specific claim.
2. Sample when the set is large, and state the sample size and the sampling rule. A random sample
   plus every citation that carries a headline number is a defensible rule.
3. For each item, retrieve the cited location and answer one question. Does the source state this, in
   this strength, under this protocol?
4. Classify: `supported`, `overstated` (true but weaker in the source), `unsupported` (not in the
   source), `misattributed` (in another source), `inaccessible` (could not retrieve).

Report both rates against the targets in
[../../ctrl-shared/core/verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md). The false
negative rate, meaning a supported claim wrongly flagged, has a target below 0.15. The false positive
rate, meaning an unsupported claim wrongly passed, has a target below 0.10. State the sample size.
Claiming a full audit after checking a sample is itself a false claim.

## Claim strength calibration ladder

Match the verb to the evidence. This ladder is the literature-stage companion to the promotion table
in [../../ctrl-shared/core/verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md).

| Evidence available | Write | Do not write |
|---|---|---|
| one paper reports a value | "X reports Y under protocol Z" | "Y is the state of the art" |
| several papers, matched protocols | "reported values on this benchmark range from A to B" | "the method achieves B" |
| several papers, unmatched protocols | "reported values range from A to B; protocols differ in resolution and augmentation, so the spread is not a ranking" | "outperforms" |
| a shared benchmark with a public leaderboard | "the best reported value on the leaderboard as of <date> is B" | "is the state of the art" without the date |
| no overlapping work found | "no directly overlapping work was retrieved under the recorded queries" | "the first to" |

## Anti-patterns

- **The survey shortcut.** Citing a survey for a number that is stated more precisely in the
  original. Read the original.
- **The abstract promotion.** Promoting an abstract-only source into a comparison table.
- **The title match.** Treating a near-identical title as proof of duplication, or a different title
  as proof of novelty. Duplication requires failing to find even one differing axis, and novelty
  requires a documented search.
- **The citation chain.** Citing a source because another paper cites it, without retrieving it.
  This is how an invented reference spreads.
- **The one-index confirmation.** Concluding that a work does not exist because one index returned
  nothing. Coverage differs sharply by venue class and by language.
- **The language gap.** Running only English queries on a Chinese venue target, which silently omits
  the domestic literature that a class D reviewer will expect to see cited.
