# Pre-commitment contract

The pre-commitment fixes, before any result exists, what result would refute the hypothesis. It is the
artifact that makes G1 pass, and it is the mechanism that prevents the plan from being adjusted to fit
whatever the runs produce.

The reason it must be written first is that the asymmetry is severe. After seeing results, every
threshold looks adjustable and every dataset looks replaceable, and the adjustment is always
describable in a way that sounds reasonable. Written first, the same threshold is a test.

## When to freeze

Freeze before the first **confirmatory** run or inspection of confirmatory outcomes. Exploratory
pilots may precede it and inform hypotheses, practical margins and sample-size estimates; retain
the pilot ledger and state every influenced choice. Pilot data must not be relabelled confirmatory
or reused as independent confirmation of choices selected from those data. If confirmatory outcomes
already exist, report the analysis as exploratory and freeze a new plan for independent validation;
a later timestamp cannot make the original study pre-registered.

Freeze happens once per plan revision. If the plan changes materially, re-freeze with a new date and
keep the previous frozen version. The artifact contract requires that a frozen artifact is never
overwritten; a revision is a new file or a dated entry.

## Contract contents

Every element is named. A category instead of a name fails G1.

```markdown
# Pre-commitment contract
- Project: <short name>
- Frozen on: <date, time zone>
- Frozen by: <who>
- Primary axis: <det | track | reid | cnav | filt>   Secondary axes: <list or none>
- Contribution type: <empirical delta | mechanism | theory | system | survey>
- Effort tier: <sketch | standard | thorough | submission>

## Hypotheses
H1: <intervention / mechanism / measurable signature / refutation rule, as in gap-to-hypothesis.md>
H2: ...
- Primary hypothesis: <H number>

## Variables
- Independent variable(s): <the single thing we change>
- Dependent variable(s): <the metric, with its convention>
- Controlled: <what is held identical across arms>
- Not controlled, and why: <list, or "none">

## Data
- Dataset(s): <exact name and version>
- Split(s): <exact split identifier>
- Split construction rule: <for spatial or scene-level data, the separation rule>
- Access: <how, and any license constraint>

## Protocol
- Protocol block ID(s): <P-det-1, P-track-1, ...> written in ctrl-protocol.md per axis
- Arms: <each arm named>
- Seeds: <count>   Dispersion: <statistic>
- Monte Carlo runs, where applicable: <count>
- Hardware: <exact model and configuration, for any timing claim>

## Baselines
| Baseline | Reason it is included | Reported or re-implemented | Protocol difference, if any |
|----------|-----------------------|----------------------------|------------------------------|

## Ablations
| Ablation | Component isolated | Budget | Prediction if the component is inert |
|----------|--------------------|--------|--------------------------------------|

## Metrics
| Metric | Definition and convention | Why this metric | Threshold that matters |
|--------|---------------------------|-----------------|------------------------|

## Budget
- Wall clock: <weeks>
- Compute: <GPU-hours, and the GPU model>
- Pilot budget consumed so far: <GPU-hours of MAX_TOTAL_GPU_HOURS>

## Decision rule
- If <result pattern A>, then <action A>
- If <result pattern B>, then <action B>
- If <result pattern C>, then <action C>

## Refutation
- H1 is refuted if: <the exact observation, with threshold and comparison>
- Fallback contribution if refuted: <the weaker true claim>

## Deviations log
| Date | Deviation | Reason | Approved by | Effect on the claim |
|------|-----------|--------|-------------|---------------------|
```

## The decision rule

The decision rule is where most plans are weakest. It must be possible for it to fail, and it must be
specific enough that two people reading the results would make the same decision.

Three branches are the minimum.

- **Confirm branch.** The result pattern that supports the hypothesis, with the threshold.
- **Refute branch.** The result pattern that falsifies it, with the threshold, and the fallback
  contribution that replaces it.
- **Inconclusive branch.** The result pattern that neither confirms nor refutes, together with what
  happens next, such as more seeds, a different benchmark, or a narrowing of the claim. This branch is
  the one most often missing, and an inconclusive branch with no action is a placeholder.

Weak and strong forms.

| Weak, fails G1 | Strong, passes G1 |
|---|---|
| "if the results support the hypothesis, proceed" | "if the mean delta over 3 seeds exceeds X on the primary metric with matched protocol, proceed to the full evaluation; report the per-seed values and dispersion regardless" |
| "if not, reconsider" | "if the pre-declared interval on the difference crosses the practical decision margin, report an inconclusive result; any extension follows the pre-specified sequential design with error control, or uses a new independent confirmatory phase" |
| "if reviewers object, revise" | "if the killer objection's primary reason is still_unresolved at round 2, narrow the claim to the tested regime before drafting" |

## Deviations

A deviation is any change to a frozen element. Deviations are permitted; silent deviations are not.

Record the date, the element changed, the reason, who approved it, and the effect on the claim for
every deviation. A deviation that changes the hypothesis or the refutation rule is not a deviation. It
is a new plan, and it requires a re-freeze with a new date.

The rule from the integrity side is that the deviation must appear in the manuscript's limitations or
methodology, whichever the venue expects. A dataset swap that is not disclosed, and a metric change
after seeing that the original metric did not favour the method, are both integrity failures under
[../../ctrl-shared/core/evidence-integrity.md](../../ctrl-shared/core/evidence-integrity.md) rules 9
and 10.

## Writing ctrl-scope.md for G0

At most 12 lines. This is the whole file, and the limit is the point.

```markdown
# ctrl-scope.md
- Research question: <one sentence>
- Primary axis: <det | track | reid | cnav | filt>   Secondary: <list or none>
- Claim type: <empirical delta | mechanism | theory | system | survey>
- Target venue or class: <exact venue and track, or the class from venue-matrix.md with the reason>
- Closest competing papers: <rank 1 to 3 from the ledger, each with the differing axis>
- Validity boundary: <dataset, split, scenario, hardware, and assumption set limitations>
- Evidence we have: <tiers, with sources>
- Evidence this claim type requires that we lack: <list, or "none">
- Downgrade applied: <none | from X to Y, reason>
- Frozen on: <date>
```

G0 passes when the claim type matches the evidence the user has or can obtain. It fails when the
claim type exceeds the available evidence class, and the required output in that case is the specific
downgrade, per [../../ctrl-shared/core/gate-contract.md](../../ctrl-shared/core/gate-contract.md).

## Writing ctrl-plan.md for G1

The frozen plan. It contains the contract above, plus the protocol blocks for each axis, plus the run
order. The run order matters because it is how the budget is protected. Cheap, high-information runs
come first, so that a plan is abandoned on evidence rather than on time.

```markdown
# ctrl-plan.md
- Frozen on: <date>
- Pre-commitment contract: <inline or path>
- Protocol blocks: <P-det-1, ...> per gate-contract.md
- Run order:
  | Order | Run | Purpose | Estimated GPU-hours | Stop condition |
  |-------|-----|---------|---------------------|----------------|
- Reporting plan: <which table and figure will carry which claim, and the ledger rows they map to>
- Open risks: <from novelty-and-risk.md, with the mitigation each>
```

The G1 test is a single question. Is the plan specific enough to fail? "Compare with several
state-of-the-art methods" fails. "Compare with ByteTrack, OC-SORT and BoT-SORT under the
private-detection protocol with identical detections" passes. Every element must be a name.

## Gate reporting

Append both verdicts to `ctrl-gates.md` in the append-only format from
[../../ctrl-shared/core/artifact-contract.md](../../ctrl-shared/core/artifact-contract.md). A waiver
is permitted only for G0 and G3, only on explicit user instruction, and must record the residual risk.
G2 has no waiver path, and a G1 failure is cleared by naming the placeholders, not by declaring the
plan frozen anyway.
