---
name: ctrl-idea-forge
description: >-
  Turn an axis and a pain point into a falsifiable, fundable research idea for control science and
  engineering, covering object detection (目标检测), tracking (目标跟踪), re-identification (重识别),
  cooperative navigation (协同导航) and filtering or state estimation (滤波). Use it for topic
  selection and proposal writing (选题, 开题), innovation-point formulation (创新点), literature-gap
  analysis, hypothesis building, feasibility and pilot scoping, novelty-versus-risk scoring, killer
  objections, and the pre-commitment contract that fixes the refutation rule before any result
  exists. It emits ctrl-scope.md for G0 and ctrl-plan.md for G1, enforces a hard pilot budget, and
  refuses to draft a proposal whose claim type exceeds the evidence that can be obtained.
---

# CTRL idea forge

Convert a pain point into a claim that can fail, and fix in writing what failure will look like.

## Start here

Read [execution-contract.md](../ctrl-shared/core/execution-contract.md) first. Select the smallest
useful mode, confirm the inputs and available tools, and load only the references needed by the
current step. Use only the output sections relevant to this request; a diagnostic or draft is not
a gate-passed final artifact.

## Default stance

- An idea is not a contribution until it is stated as a hypothesis with a refutation rule. Anything
  that cannot fail is not a hypothesis, it is a description of work.
- The refutation rule is written before the results exist, and it is written in the same document as
  the hypothesis. A rule added afterwards is a rationalisation. See
  [../ctrl-shared/core/gate-contract.md](../ctrl-shared/core/gate-contract.md), G1.
- Claim type sets the evidence bar. An empirical delta needs a matched comparison; a mechanism claim
  needs an ablation chain; a theory claim needs a proof; a system claim needs an integration that
  runs. Never let the ambition of the claim outrun the evidence class. See
  [references/contribution-typing.md](references/contribution-typing.md).
- Pilot work uses a recorded budget. The standard limits are 2 estimated wall-clock hours per
  idea, a 3-hour enforced ceiling, at most 3 ideas and 8 total GPU-hours. Read the chosen tier,
  reservation and executor rules in [references/pilot-budget.md](references/pilot-budget.md).
  A higher effort tier alone never authorizes more compute or guarantees timeout enforcement.
- Novelty is bounded by the recorded search, never asserted. The nearest-competitor ledger from
  `ctrl-lit-radar` is the input, and the novelty promotion condition in
  [../ctrl-shared/core/verdicts-and-loops.md](../ctrl-shared/core/verdicts-and-loops.md) is the gate.
- Generate the strongest objection first, not the balanced discussion. An idea that has never met its
  best objection is not ready to be planned.
- The most useful output is often a downgrade. Reporting "this is an empirical delta, not a
  mechanism" early is worth more than a polished proposal that fails G0.

## Workflow

1. **Anchor the problem.** Take the axis (`det` / `track` / `reid` / `cnav` / `filt`), the user's pain
   point in the user's own words, the deployment or evaluation setting, and the resources actually
   available (compute, data, hardware, people, weeks). An idea that needs a UAV fleet when the user
   has a workstation is a bad idea, however good it is.

2. **Run the gap analysis.** Ask `ctrl-lit-radar` for the nearest-competitor ledger and the gap
   statements. Reject any gap supported by fewer than three works, and label it a hunch. See
   [references/gap-to-hypothesis.md](references/gap-to-hypothesis.md).

3. **State the hypothesis in falsifiable form.** Use the four-part form in
   [references/gap-to-hypothesis.md](references/gap-to-hypothesis.md). The four parts are the
   intervention, the mechanism, the measurable signature, and the refutation rule. Rewrite until the
   refutation rule can fail. If it cannot fail, the hypothesis is a description and must be replaced.

4. **Type the contribution.** Choose empirical delta, mechanism, theory, system, or survey, and name
   the evidence that type requires. If the required evidence is unobtainable within the resources
   from step 1, downgrade the type now and record the downgrade. See
   [references/contribution-typing.md](references/contribution-typing.md).

5. **Generate three to five candidate ideas, not one.** For each, write one sentence of mechanism and
   one sentence of the cheapest test that would kill it. Rank them, then keep at most three for
   pilots.

6. **Score novelty against risk.** Use the two-axis scoring in
   [references/novelty-and-risk.md](references/novelty-and-risk.md). A high-novelty, high-risk idea
   needs a fallback contribution declared in advance, namely the weaker true claim that survives if
   the main hypothesis is refuted.

7. **Plan an exploratory pilot under the chosen budget.** Record its question, wall-clock cap,
   GPU reservation and enforceable cancellation mechanism before any launch. Execute only with an
   authorized tool and user-approved resources; otherwise deliver the plan as `not run`. Retain
   outcomes and influenced choices, never promote the pilot into confirmatory evidence. See
   [references/pilot-budget.md](references/pilot-budget.md).

8. **Produce the killer objection.** Write the strongest 200-word rejection memo a hostile area chair
   would write, then have it adjudicated by an independent pass that is not a defender. Classify each
   point as answered by the current plan, partially answered, or still_unresolved, with a pointer. This
   mechanism is ported from the adversarial attack-and-adjudication pair described in
   [references/killer-objection.md](references/killer-objection.md).

9. **Write the pre-commitment contract.** Freeze the hypothesis, the independent and dependent
   variables, the datasets and splits with the exact protocol, the named baselines with the reason
   each is included, the ablation list, the metrics with definitions, the compute budget, and the
   decision rule. Sign and date it. See [references/precommitment.md](references/precommitment.md).

10. **Emit `ctrl-scope.md` at G0.** At most 12 lines, using the format in
    [../ctrl-shared/core/gate-contract.md](../ctrl-shared/core/gate-contract.md). Run the G0 check
    honestly, including the case where the claim type exceeds the evidence class.

11. **Emit `ctrl-plan.md` at G1.** Use the frozen-plan format in
    [../ctrl-shared/core/artifact-contract.md](../ctrl-shared/core/artifact-contract.md) and the
    protocol-block format for the axis. Every element is a name, not a category. "Compare with
    several state-of-the-art methods" fails; named baselines with a stated reason each pass.

12. **Record the gate status** using the reporting block in
    [../ctrl-shared/core/gate-contract.md](../ctrl-shared/core/gate-contract.md), and append it to
    `ctrl-gates.md`. Report a failed gate with the failing criterion and the smallest clearing
    change, rather than working around it.

## Output format

```text
Idea forge report
- Axis: <det | track | reid | cnav | filt>   Effort tier: <sketch | standard | thorough | submission>
- Pain point (user's words): <quote>
- Resources available: <compute, data, hardware, people, weeks>
- Gap: G<n> supported by <k> works  |  hunch (k < 3, not used as a gap)

Hypothesis H1
- Intervention: <what we change>
- Mechanism: <why it should produce the effect>
- Measurable signature: <metric, benchmark, expected direction and rough size>
- Refutation rule: <the result that makes H1 false, with the threshold>
- Fallback contribution if refuted: <the weaker true claim that survives>

Contribution typing
- Type: <empirical delta | mechanism | theory | system | survey>
- Evidence this type requires: <list>
- Evidence obtainable within resources: <list>
- Downgrade applied: <none | from X to Y, reason>

Candidate ranking
| # | Idea | Mechanism in one sentence | Cheapest killing test | Novelty (1-5) | Risk (1-5) | Pilot run? |
|---|------|---------------------------|-----------------------|---------------|------------|------------|
| 1 | | | | | | yes / no / budget-skipped |

Pilot ledger
| Idea | Estimated hours | Actual hours | GPU-hours | Outcome | Stopped by budget |
|---|---|---|---|---|---|
| | | | | supported / inconclusive / refuted | yes / no |

Killer objection
<the strongest 200-word rejection memo, verbatim>

Adjudication
| Point | Verdict | Evidence pointer |
|-------|---------|------------------|
| | answered_by_current_plan / partially_answered / still_unresolved | |

Pre-commitment
- Frozen on: <date>   Hypotheses: H1..H<n>
- Refutation rule as written above: yes / no  (must be yes before any result is seen)
- Baselines: <named list with the reason each is included>
- Ablations: <named list, each isolating one component>
- Compute budget: <GPU-hours and wall-clock, matching the pilot budget>
- Decision rule: <the exact result pattern that changes the plan>

Gate G0 scope: PASS | FAIL | BLOCKED
- Checked: <criteria evaluated>
- Artifact: ctrl-scope.md
- Failing criterion: <one line, only when not PASS>
- Smallest clearing change: <one line, only when not PASS>
- Waiver: none

Gate G1 proposal freeze: PASS | FAIL | BLOCKED
- Checked: <criteria evaluated>
- Artifact: ctrl-plan.md
- Failing criterion: <one line, only when not PASS>
- Smallest clearing change: <one line, only when not PASS>
- Waiver: none
```

## Red lines

- Never write a refutation rule after seeing a result, and never rewrite one to accommodate a result.
  Reopen the gate instead and record the reason.
- Never state a hypothesis that no experiment could refute. "The method will perform well" is not a
  hypothesis.
- Never exceed the chosen pilot limits or start an unreserved/uncontrolled run. Standard limits
  are 2 estimated wall-clock hours, a 3-hour ceiling, 3 ideas and 8 total GPU-hours; other limits
  require the decisions in the pilot-budget reference.
- Never call a post-hoc rule pre-declared for already inspected outcomes. Keep pilot influence
  visible and freeze before independent confirmatory evaluation.
- Never claim novelty beyond what the recorded search supports, and never treat a near-miss title as
  proof of duplication or a different title as proof of novelty.
- Never invent a baseline, a dataset split, a hardware fact, or a preliminary result. Mark it
  `[MISSING]` with what would produce it.
- Never soften a killer objection because the user is attached to the idea. The adjudicator reports
  `still_unresolved` when the plan does not answer the point.
- Never promote an idea's claim type to make it sound fundable. Fundability follows from the claim
  matching the evidence, not from the wording.
- Never reuse a previous project's frozen plan without re-freezing it against the current resources
  and the current venue cycle.

## Related files

| File | Open when |
|---|---|
| [references/gap-to-hypothesis.md](references/gap-to-hypothesis.md) | You are converting a gap into a hypothesis or writing a refutation rule |
| [references/contribution-typing.md](references/contribution-typing.md) | You are choosing a contribution type or checking whether a claim exceeds its evidence |
| [references/novelty-and-risk.md](references/novelty-and-risk.md) | You are scoring ideas, ranking them, or deciding a fallback contribution |
| [references/pilot-budget.md](references/pilot-budget.md) | You are scoping, estimating, or reporting a pilot experiment |
| [references/killer-objection.md](references/killer-objection.md) | You are generating the strongest objection or running the independent adjudication |
| [references/precommitment.md](references/precommitment.md) | You are freezing the plan or writing the decision rule before results exist |
