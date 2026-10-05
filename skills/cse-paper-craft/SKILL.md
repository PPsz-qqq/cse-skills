---
name: cse-paper-craft
description: >-
  Use when writing, revising or polishing a manuscript on detection, tracking, re-ID, cooperative
  navigation or filtering (目标检测, 跟踪, 重识别, 协同导航, 滤波): 写论文, 论文修改, 润色, 摘要,
  引言, 相关工作, 创新点表述, 中英文摘要, LaTeX, manuscript, abstract, contribution framing,
  self-edit before submission. Frames each claim at the strength its evidence supports, positions
  against named competitors, reconciles numbers across abstract, tables and captions, and checks
  notation.
---

# CSE paper craft

Write and revise the manuscript for the five `cse-*` axes so that every claim is framed at the
strength its evidence supports, and every number survives a reconciliation pass.

## Start here

Read [execution-contract.md](../cse-shared/core/execution-contract.md) first. Select the smallest
useful mode, confirm the inputs and available tools, and load only the references needed by the
current step. Use only the output sections relevant to this request; a diagnostic or draft is not
a gate-passed final artifact.

For a `local-edit`, preserve the supplied claims, citations and numbers; check the changed passage
and report that no full-paper audit was performed. Start the full workflow below only when its
scope is requested. New or strengthened result claims require the applicable evidence checks.

## Default stance

- The claim type decides the framing. An empirical delta, a mechanism, a theory result, a system
  demonstration, and a survey need different evidence and different venues. Never present a delta as
  a mechanism, and never present a simulation as a field result.
- Write at the strength the promotion conditions in `../cse-shared/core/verdicts-and-loops.md`
  permit. When the condition is unmet, write the weaker true statement and delete the stronger
  wording instead of appending a hedge.
- One number, one precision, one unit, on every surface. A value that conflicts between surfaces
  beyond rounding is an integrity failure; the same value at two precisions is a consistency defect
  to fix before any freeze.
- The protocol travels with the number. A `track` number without online or offline and public or
  private labels beside it is not comparable to anything, and a `reid` number without its
  re-ranking status is ambiguous on its face.
- Name the nearest competitor and state the precise difference. A related-work paragraph that only
  summarizes fails to position the paper.
- Write in the register of the target venue and the pack. No marketing adjectives, no emoji, and no
  em dash, en dash, or colon used as a habitual sentence connector.
- Simulation and field evidence are labeled wherever a result appears, including captions and the
  abstract.
- Every claim that cannot be supported is withdrawn or restated. A `[MISSING]` slot is a correct
  output and a confidently written unsupported sentence is not.

## Workflow

1. **Fix the claim type and the venue class.** Read `cse-scope.md` and the `G0` block in
   `../cse-shared/core/gate-contract.md`. Determine whether this is an empirical delta, a
   mechanism, a theory, a system, or a survey, and map it to a venue class with
   `../cse-shared/core/venue-matrix.md`. Write the fit statement. If the claim type exceeds the
   evidence, emit the downgrade before writing anything.

2. **Read the frozen evidence, not the memory of it.** Pull the claim rows from `cse-claims.md`,
   the protocol blocks from `cse-protocol.md`, and the tables from `exp/`. A manuscript written
   from recalled numbers is the most common source of a reconciliation failure at submission time.

3. **Draft in reading-order-independent sequence.** Method first, then experiments, then related
   work, then introduction, then abstract, then title. Each section has acceptance criteria and a
   "must not appear" list in `references/section-workflow.md`. A section is done when its claim is
   clear without the next section, and every sentence traces to an artifact or a citation.

4. **Frame each contribution at its permitted strength.** Use the escalation ladder and the framing
   templates in `references/contribution-framing.md`. A `outperforms` needs a protocol-matched
   comparison; a `the gain comes from` needs a singleton ablation arm under one protocol; a
   novelty needs a documented scoped search including recent and foundational work; a two-cycle
   window alone never proves historical priority.

5. **Position against the nearest competitors.** Write one positioning unit per nearest competitor
   from `references/related-work.md`, with the precise difference stated so a reader can check it
   against both papers. Organize by the distinction the paper turns on, close with the gap derived
   from those differences, and mark any quoted number with its protocol differences.

6. **Write the experiments section around the protocols.** Every comparison carries or references a
   protocol block, every headline number carries a dispersion or an explicit `single seed` label,
   and the failure analysis is present. Results tables come from
   [results-tables.md](../cse-experiment-suite/references/results-tables.md), filled from the
   raw artifacts.

7. **Write the abstract last, against the six slots.** Problem, gap, idea, method, evidence,
   boundary, in that order, using `references/abstract-template.md`. Every abstract number must have
   a checked ledger row at the tables' precision. Comparative numbers need `comparable`; an
   absolute, non-comparative value uses `NOT_APPLICABLE` with a reason, not a fabricated baseline.

8. **Run the number-reconciliation pass.** Build the complete number inventory and check the
   abstract, tables, captions, and conclusion against it, then check aggregates, claim strength, and
   protocol adjacency. See `references/reconciliation-and-notation.md`, pass 1.

9. **Run the notation-consistency pass.** Symbols, acronyms, bilingual terminology, references,
   figures and tables, and style, against
   `../cse-shared/core/terminology-and-notation.md`. See `references/reconciliation-and-notation.md`,
   pass 2.

10. **Self-edit against the checklist and report.** Walk `references/self-edit-checklist.md` top to
    bottom, classify each finding by severity, and report the counts with the recommendation derived
    from the integrity rules. Record any verdict that a later revision invalidated as `STALE`.

11. **Hand the frozen manuscript to review.** The review, the response letter, and the slide deck
    belong to cse-pre-submission-review, cse-response-craft, and cse-paper-to-slides. Do not
    present a draft as ready while a blocking finding is open.

## Output format

```text
## Manuscript pass: <axis> <section or full draft>

### Claim and framing
Primary axis: <det | track | reid | cnav | filt>
Claim type: <empirical delta | mechanism | theory | system | survey>
Target venue and class: <exact venue> / <A | B | C | D | E>
Contribution framed as: <the sentence the venue's criteria reward>
Promotion condition met: <the condition, and the artifact that satisfies it>

### Section drafts
#### <Section name>
<draft text>
Acceptance criteria check: <criterion -> pass | fail, one line each>
Must-not-appear check: <none found | the offending sentence, quoted, with its repair>

### Contribution list, one line each
C1 <claim, with the experiment or table that supports it, and its protocol id>
C2 <...>

### Related work positioning
| Competitor | Shares | Precise difference | Quoted number and its protocol labels |
|---|---|---|---|

### Number reconciliation
| Number ID | Value | Units | Where it appears | Precision | Ledger row | Protocol ID | Source artifact |
|---|---|---|---|---|---|---|---|
Outcome counts: <pass>, <fail>, <not comparable marked>, <stale>
Failing numbers and their clearing change: <list, or none>

### Notation and consistency
Symbols: <pass | fail, with the defect>
Acronyms: <pass | fail> | Bilingual: <pass | fail | not applicable>
References: <pass | fail> | Figures and tables: <pass | fail> | Style: <pass | fail>

### Self-edit findings
| ID | Pass | Severity | Claim pointer | Evidence pointer | Finding | Smallest clearing change |
|---|---|---|---|---|---|---|
Counts: <blocking>, <major>, <minor>, <question>. Recommendation: <derived, not chosen>

### Gaps
[MISSING: <what is needed and how to obtain it>]
[UNVERIFIED: <the item and why it was not verified>]
```

## Red lines

- Never write `outperforms` without a protocol-matched comparison against that specific baseline,
  and never carry a `not comparable` value into an abstract or a conclusion.
- Never treat a recent two-cycle search as proof of `first to`. Prefer a bounded search finding
  with sources, window, foundational prior work, near misses and coverage limits.
- Never present a simulation result as a field result, and never write a field or hardware claim
  without field or hardware data.
- Never present a delta as a mechanism. A mechanism sentence requires an ablation that isolates the
  component under one protocol.
- Never report a single-seed number as a stable result, and never state a mean without its
  dispersion or an explicit `single seed` label.
- Never tune on the reported split and describe it as held out.
- Never invent a citation, a number, a figure, a baseline, a hardware fact, or an experiment. Write
  `[MISSING: <need>]` instead.
- Never generate a bibliography entry from memory. Fetch it from a source of record and confirm the
  cited claim is in the paper, or leave a visible placeholder and notify the author.
- Never leave a quoted competitor number without its protocol differences and a comparability
  verdict.
- Never strengthen a claim between rounds without new evidence, and never lower a severity tier
  because the deadline is near.
- Never mark a reconciliation `PASS` on a revision that changed after the pass ran. A reworded claim
  is a changed claim, and its verification is `STALE`.

## Related files

| File | Open when |
|---|---|
| [references/section-workflow.md](references/section-workflow.md) | You are drafting or revising a specific section and need its acceptance criteria and must-not-appear list |
| [references/contribution-framing.md](references/contribution-framing.md) | You are deciding the claim type, framing a contribution, or mapping the work to a venue class |
| [references/reconciliation-and-notation.md](references/reconciliation-and-notation.md) | You are running the number inventory, the notation pass, the bilingual pass, or the reference pass |
| [references/related-work.md](references/related-work.md) | You are positioning the work against named competitors or writing a novelty claim |
| [references/axis-writing-guides.md](references/axis-writing-guides.md) | You need what reviewers in a specific axis expect, the standard figures and tables, or the rejection phrasing to avoid |
| [references/latex-skeleton.md](references/latex-skeleton.md) | You are setting up the manuscript source, a table, a figure, an algorithm, or a bilingual abstract |
| [references/abstract-template.md](references/abstract-template.md) | You are writing or revising the abstract, or a number in it failed reconciliation |
| [references/self-edit-checklist.md](references/self-edit-checklist.md) | You are doing a pre-submission self-edit pass and need the pass order and the report format |

Cross-skill. Read [verdicts-and-loops.md](../cse-shared/core/verdicts-and-loops.md) for the
promotion conditions, the stale-verdict rule, and the loop budgets,
[evidence-integrity.md](../cse-shared/core/evidence-integrity.md) for the integrity rules and the
comparability break table, [gate-contract.md](../cse-shared/core/gate-contract.md) for the `G0` to
`G3` gates, [terminology-and-notation.md](../cse-shared/core/terminology-and-notation.md) for
terminology, symbols, and the consistency sweep,
[artifact-contract.md](../cse-shared/core/artifact-contract.md) for artifact and figure naming,
[venue-matrix.md](../cse-shared/core/venue-matrix.md) for the venue classes and the fit statement,
and [review-rubrics.md](../cse-shared/core/review-rubrics.md) for the scoring dimensions and
severity tiers. Literature searching and novelty verification belong to cse-lit-radar, experiment
design and protocol blocks belong to cse-experiment-suite, drawing and restyling the figures
belongs to cse-figure-studio, the pre-submission review belongs to
cse-pre-submission-review, the response letter belongs to cse-response-craft, and the deck belongs
to cse-paper-to-slides.
