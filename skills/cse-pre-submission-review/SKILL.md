---
name: cse-pre-submission-review
description: >-
  Use when the user wants a referee-style check of a paper on detection, tracking, re-ID,
  cooperative navigation or filtering (目标检测, 跟踪, 重识别, 协同导航, 滤波): 审稿, 模拟审稿, 预审,
  帮我审一下论文, 拒稿风险, mock or peer review, pre-submission check for CVPR, TAC, Automatica,
  T-RO, ICRA, TGRS, 自动化学报 or similar. Gives pointer-backed concerns with severities,
  eight-dimension scores, a derived recommendation and G3 readiness; several reviewers only in
  isolated contexts, otherwise one labelled report.
---

# CSE pre-submission review

Referee-side review of a manuscript before it is submitted, producing frozen reviewer reports and
a separately held synthesis so the authors learn what a real panel would find.

## Start here

Read [execution-contract.md](../cse-shared/core/execution-contract.md) first. Select the smallest
useful mode, confirm the inputs and available tools, and load only the references needed by the
current step. Use only the output sections relevant to this request; a diagnostic or draft is not
a gate-passed final artifact.

Diagnostic review does not require G2 PASS. Missing evidence is something to review, not a reason
to refuse the review. For an excerpt or quick check, produce one bounded report by default; do not
infer whole-paper readiness from an excerpt.

## Default stance

Review the artifact, not the author. Every concern carries a claim pointer and an evidence
pointer, or it is dropped.

- Read [review-rubrics.md](../cse-shared/core/review-rubrics.md) first. It holds the normative
  eight dimensions, severity tiers, concern record format, and the two rules that precede any score.
- A review is itself a claim. Apply the self-audit obligation before delivering it.
- Multiple simulated reports require isolated contexts to avoid leakage. Isolation is not proof
  of cognitive or statistical independence, especially with the same model and prompt. Label the
  reports `context-isolated simulated reviews`; agreement is not an estimate of real reviewers'
  acceptance probability. Shared-context drafts are non-blind, not an independent panel.
- Never invent a concern to look balanced, and never suppress one to be agreeable. If a severity
  level has no grounded concern, write that sentence.
- Assume the user will show the review to a co-author. Write findings that survive being checked
  against the manuscript line by line.
- Default effort tier: `thorough` for one round, `submission` for a camera-ready freeze.

## Workflow

1. **Fix scope and effort tier.** Record the primary axis (`det` / `track` / `reid` / `cnav` /
   `filt`), every secondary axis, the target venue and its class, and the claim type from G0. A
   review of a `det` paper judged by class B control criteria is a category error. State the effort
   tier and the loop budget of four review rounds.

2. **Audit the input, then hash it, and report every verdict in the pack enum.** Record the content
   hash and modification time of every file under review. When the input is pasted text or no
   hashing tool exists, identify the exact input instead (file name, version, date or the pasted
   excerpt's first and last sentence) and write `hash not computed`; never invent one. Every
   finding, over every reviewer and
   every gate, resolves to exactly one of `PASS` / `WARN` / `FAIL` / `BLOCKED` / `ERROR` /
   `NOT_APPLICABLE` from [verdicts-and-loops.md](../cse-shared/core/verdicts-and-loops.md). Never
   invent a seventh state, never soften `FAIL` into `WARN` because progress is wanted, and never
   report `ERROR` as `PASS`. A verdict is valid only for the revision it was computed from, so a
   manuscript change after a report is frozen makes that report and every verdict derived from it
   `STALE`, and the round is re-run rather than patched.

3. **Build the immutable review packet.** One file, `cse-review-<round>-packet.md`, holding the
   artifact paths under review, the verified source anchors, the assessment boundary (read in
   full, read in part, unavailable), the common criteria, and the axis list. It holds no concern,
   no hypothesis, no conclusion, no prior-round report, and no self-assessment by the authors.
   Freeze it before any report exists.

4. **Define the emphasis briefs before any review exists.** One file per reviewer,
   `cse-review-<round>-brief-R<k>.md`. A brief is a lens, not a persona.

   | Reviewer | Emphasis brief | Extra depth allocated to |
   |---|---|---|
   | R1 | method and evidence chain | whether the stated claim is established by the experiments as specified |
   | R2 | comparison fairness and reproducibility | protocol matching, baseline status, seeds, code and config availability |
   | R3 | validity boundary and failure modes | dataset, scenario, hardware and assumption limits, negative results, generalization |

   Every reviewer scores all eight dimensions on the full scale. A brief changes where depth goes,
   never the rubric and never the score range. Freeze the brief set with the packet. Invent no
   reviewer names, institutions, or biographies.

5. **Run each reviewer in a genuinely separate context.** Pass only the packet, that reviewer's
   brief, the report skeleton, and the review rules. Never pass another report, a shared concern
   ledger, a draft synthesis, or a hint about what the others found. Each reviewer walks the
   per-axis taxonomy for the active axes and reports every grounded concern it raises, with no
   quota in either direction. If the environment cannot start separate contexts, take one path,
   label it in the output, and never present shared-context drafting as independent peer review.
   - **Path A, one report per invocation.** Ask the user to start a fresh invocation per reviewer,
     hand it the packet path and one brief path, and keep the produced report out of the next
     invocation. Preferred fallback, and it preserves blindness.
   - **Path B, single reviewer.** Produce exactly one report and label it
     `single reviewer, multi-reviewer isolation unavailable`. Do not claim three reviewers and do
     not run a consensus step.
   - **Path C, declared non-blindness.** Only on user insistence. Stamp every report and the
     synthesis `NON-BLIND: shared context, reports are not independent`, report overlap as draft
     overlap, and never use the word consensus.

6. **Freeze each report before any comparison.** Write each report to its own file and record its
   hash. Do not edit a frozen report afterwards to reduce overlap, to manufacture disagreement, or
   to match a later finding. Natural duplication and natural disagreement are both evidence about
   the manuscript and are left intact.

7. **Compare only after all reports are frozen.** Produce `cse-review-<round>-synthesis.md` as a
   separate file, never inside a reviewer file and never shown to a reviewer context. Label a point
   `consensus` only when at least two reports independently raised the same underlying concern,
   judged by mechanism rather than wording, and `single` when one report raised it. Report the
   overlap honestly, including full convergence, which is itself a finding about obviousness.

8. **Resolve severity, then derive the recommendation.** Take the highest severity any report
   assigned to a shared underlying concern and state which reports supported it. Derive the
   recommendation from the eight dimension scores using the mapping in
   [review-rubrics.md](../cse-shared/core/review-rubrics.md), never choosing a recommendation first
   and back-filling scores into it.

9. **Score overall readiness on 1 to 10 under the calibration rule.** Start at 5 and justify every
   point of movement with a pointer, per
   [verdicts-and-loops.md](../cse-shared/core/verdicts-and-loops.md). A 9 or 10 requires zero
   `Blocking` findings and at most two `Major` findings. A score that moves between rounds without
   the artifact changing is a calibration error, not progress.

10. **Roll up blocking flags.** List every concern with `Blocking: Yes`, the reports that raised
    it, the dimension it damages, and its resolution test. An unresolved blocking concern forces
    `FAIL` at G3 and forbids any statement that the paper is ready to submit. A gate that cannot be
    evaluated because an artifact is missing is `BLOCKED`, and names the missing input.

11. **Apply the anti-sycophancy rule to push-back.** When the authors contest a finding, score
    their counter-argument 1 to 5 by relevance and sufficiency. Concede at 4 or above when evidence
    directly closes the resolution test, including existing material the review missed. A bare
    assertion is 1 and incomplete support is 3. Never move a severity tier because the user is
    displeased or the deadline is near, and never move one to sound rigorous.

12. **Deliver, then report the loop outcome.** State `converged`, `budget exhausted with residual
    defects`, or `stopped by user`, and append the round to `cse-gates.md` with the G3 verdict.

## Output format

Two artifacts. The report skeleton goes to `cse-review-<round>-R<k>.md`, one file per reviewer.
Everything after the separator line goes to `cse-review-<round>-synthesis.md`, never shown to a
reviewer context.

```text
# Reviewer R<k> report, round <n>
- Manuscript revision: <path> hash <sha256 prefix | not computed>, mtime <timestamp | version>
- Axis: <det|track|reid|cnav|filt>, secondary <list or none>   Venue class: <A|B|C|D|E>
- Emphasis brief: <lens name>
- Isolation: separate context | one report per invocation | NON-BLIND shared context
- Sources read in full: <list>   Read in part: <list>   Unavailable: <list>

## Dimension scores
Score all eight 1-5 from a start of 3, one pointer per point of movement.
`D1 <n> <p>  D2 <n> <p>  D3 <n> <p>  D4 <n> <p>  D5 <n> <p>  D6 <n> <p>  D7 <n> <p>  D8 <n> <p>`

## Concerns
### <axis>-C1
Severity: Blocking | Major | Minor | Question   Dimension: D<n>   Blocking: Yes | No
Claim pointer: <exact claim and location>
Evidence pointer: <artifact or manuscript location>
Concern: <one paragraph, no rhetorical escalation>
Why it matters: <consequence for the manuscript's case>
Resolution test: <observable condition that closes this concern>

## Dimensions with no grounded concern
<dimension: one sentence stating that no grounded concern was found>

## Recommendation
Eight-dimension profile: <D1..D8>   Overall readiness 1-10: <n>
Movement justified by: <pointers>
Recommendation: Reject | Major revision | Minor revision | Accept
Reason: <mapping rule applied, quoted>
Verdict: <PASS | WARN | FAIL | BLOCKED | ERROR | NOT_APPLICABLE>
Staleness: valid for revision <sha256 prefix, or the identified version> only; a later change voids this report

# ===== separate file, cse-review-<round>-synthesis.md, never shown to a reviewer =====
# Post-freeze synthesis, round <n>
- Reviewers compared: R1 <hash> R2 <hash> R3 <hash>, all frozen at <timestamp>
- Isolation status: <separate contexts | one report per invocation | NON-BLIND>
- Consensus rule applied: at least two reports raising the same underlying concern

## Cross-report matrix
| Underlying concern | R1 | R2 | R3 | Status | Highest severity |
|---|---|---|---|---|---|
| <concern> | <id> | <id> | - | consensus | Major |

## Consensus concerns
<the shared mechanism, the report IDs that independently raised it, and why they are the same
mechanism rather than the same wording>

## Single-reviewer concerns
<concern, its report ID, and the reason it is retained rather than dropped>

## Blocking flags roll-up
| Flag | Reports | Dimension | Resolution test | Owner action |
|---|---|---|---|---|

## Disagreement, gate report, deliverable
<where two reports reached incompatible readings and what artifact would settle it, then the
standard gate block from core/gate-contract.md for G3, then report and flag counts>
```

## Red lines

- Never label reports mutually blind when they were drafted in one context. Path A, B, and C exist
  so that honesty is always cheaper than the lie.
- Never place a synthesis, a consensus label, or one reviewer's report inside another reviewer's
  context or file, and never edit a frozen report to change its overlap with another report.
- Never invent a reviewer identity or expertise, a location, a quotation, a table cell, or a
  number, and never claim what a real venue's reviewers would decide. A location you cannot find is
  marked `[NOT FOUND: <what you searched>]`, never approximated.
- Never mark a numerical anomaly as a confirmed error without arithmetic proof or the source data,
  never downgrade an evidence, validity, ethics, or integrity problem to `Minor`, and never upgrade
  a typographic issue to `Major` to sound severe.
- Never report a seventh verdict state, never soften `FAIL` into `WARN`, and never treat a verdict
  computed on an earlier revision as still valid.
- Never issue a 9 or 10 with a `Blocking` finding open or with three or more `Major` findings, never
  let the recommendation precede the scores, and never deliver a review that does not identify its
  exact input revision. Record a hash when one can be computed; otherwise state `hash not computed`
  rather than inventing one.

## Related files

| File | Open when |
|---|---|
| [references/mutual-blindness-protocol.md](references/mutual-blindness-protocol.md) | You are building the packet, writing emphasis briefs, choosing an isolation path, or freezing reports |
| [references/axis-concern-taxonomies.md](references/axis-concern-taxonomies.md) | You need the per-axis concerns that actually cause rejection in det, track, reid, cnav, or filt |
| [references/domain-review-gates.md](references/domain-review-gates.md) | You are checking the axis-specific G2 addenda, comparison-protocol fields, or a secondary axis's evidence rules |
| [references/report-structure.md](references/report-structure.md) | You are writing or auditing a reviewer report, the synthesis, the concern fields, or the forensic pass |
| [references/review-qa-checklist.md](references/review-qa-checklist.md) | You are self-auditing a finished review on groundedness, non-invention, or severity calibration |
| [../cse-shared/core/review-rubrics.md](../cse-shared/core/review-rubrics.md) | You need the normative eight dimensions, severity tiers, recommendation mapping, or concern record format |
| [../cse-shared/core/verdicts-and-loops.md](../cse-shared/core/verdicts-and-loops.md) | You need the verdict enum, the staleness rule, the loop budget, the calibration rule, or the effort tiers |
| [../cse-shared/core/gate-contract.md](../cse-shared/core/gate-contract.md) | You need the G0 to G3 definitions, the axis gate addenda, or the gate reporting format |
| [../cse-shared/core/evidence-integrity.md](../cse-shared/core/evidence-integrity.md) | You are auditing numbers, comparisons, ablations, seeds, provenance, or citation honesty |
| [../cse-shared/core/venue-matrix.md](../cse-shared/core/venue-matrix.md) | You are judging venue fit, venue-class weighting, or a venue-specific failure mode |
| [../cse-shared/core/artifact-contract.md](../cse-shared/core/artifact-contract.md) | You are naming review artifacts or checking reviewer-facing versus synthesis separation |
| [../cse-shared/core/terminology-and-notation.md](../cse-shared/core/terminology-and-notation.md) | You need symbol, metric, or bilingual term conventions while writing a concern |

Forward references, owned by other skills. Use `cse-lit-radar` for a documented search of the
recent venue cycles, `cse-idea-forge` when a rejected framing needs a different claim type,
`cse-experiment-suite` when a resolution test is a missing experiment, and `cse-paper-craft` when
the review hands the manuscript back for rewriting.