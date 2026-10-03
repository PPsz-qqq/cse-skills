# Pilot budget discipline

Pilots answer exploratory feasibility/signal questions cheaply. Their outcomes may inform a
confirmatory plan, but are never retroactively confirmatory evidence. Read
[precommitment.md](precommitment.md) before promoting any pilot finding.

## Default budget and units

```text
PILOT_MAX_HOURS     = 2   # estimated wall-clock hours per idea, not hours per GPU
PILOT_TIMEOUT_HOURS = 3   # wall-clock ceiling per running pilot, if an executor can enforce it
MAX_PILOT_IDEAS     = 3   # ideas actually attempted; retries still consume time/compute
MAX_TOTAL_GPU_HOURS = 8   # sum over all allocated GPUs and all attempts
```

GPU-hours = sum of allocated GPU count times allocation duration in hours. Two GPUs allocated
for 1.5 hours consume 3 GPU-hours, not 1.5. State device model/count and allocation/start/end
times. CPU-only work still has a wall-clock ceiling and a recorded CPU budget.

Before launching, reserve enough GPU-hours for the run's enforceable worst-case allocation;
do not start concurrent jobs whose combined reservations can exceed the total. At the earliest
wall-clock or total-budget stop, cancel the relevant jobs and confirm termination. An estimate
below the cap permits a run; it is not itself an automatic kill deadline. A running pilot may
exceed its estimate only within the recorded timeout and reserved total budget; report the overrun.

## Effort tiers

The table gives candidate budgets, not automatic authorization to spend more compute.
Use `standard` unless a smaller budget fits or the user explicitly approves a larger budget.
A thorough/submission writing request alone does not authorize larger experiment costs.

| Effort tier | Estimated wall-clock cap per pilot | Enforced timeout | Max ideas | Total GPU-hours |
|---|---|---|---|---|
| `sketch` | 0.5 h | 1 h | 1 | 2 |
| `standard` | 2 h | 3 h | 3 | 8 |
| `thorough` | 3 h | 4 h | 3 | 12 |
| `submission` | 3 h | 5 h | 4 | 16 |

Record the chosen limits before execution. Reductions are allowed; increases require an explicit
user decision and a dated pilot-plan revision. If G1 already exists, reopen/re-freeze it too.
A G1 that does not yet exist cannot be described as "reopened".

## Execution preflight

Confirm an authorized executor, cancellation method and enforceable stop mechanism before
starting. A command-tool timeout may merely move a process to a background job: this is **not**
a hard execution timeout. Inspect the executor's actual semantics; do not assume the harness
kills a process at a configured duration. Record job IDs, termination responsibility and how
GPU use is tracked. Without enforcement, provide a runnable pilot plan for the user and record
`not run: executor/timeout enforcement unavailable`; never claim a killed or completed pilot.

## Pilot shapes and estimation

- **Signal pilot:** smallest useful configuration, usually one seed. Record the observed delta
  as exploratory; one seed cannot estimate run-to-run dispersion or prove superiority.
- **Feasibility pilot:** does data loading, inference/training and evaluation work end to end?
- **Reproduction pilot:** can a baseline run under the intended protocol? Record any published
  versus reproduced difference and its protocol, not a claimed confirmation from one run.

Estimate from a verified comparable timing or a local smoke test; state scaling assumptions,
integration overhead and hardware. If no timing exists, label the estimate `assumed`. Skip a pilot
estimated above the chosen cap or requiring unavailable data/hardware; narrow its question only
through a recorded pre-run revision, never while hiding an overrun. Pilots are not open-ended
tuning, disguised full experiments or a way around a confirmatory freeze.

## Pilot ledger

Keep in `ctrl-pilots.md`; use the current revision from the artifact index.

```markdown
| Idea | Question | Tier/limits | Estimated wall h | GPUs/model | Reserved GPU-h | Actual wall h | Actual GPU-h | Executor/job | Outcome | Stop reason |
|---|---|---|---|---|---|---|---|---|---|---|
| <idea> | signal/feasibility/reproduction | <limits> | <estimate> | <count/model> | <reservation> | <actual or not run> | <actual> | <ID or unavailable> | <outcome> | <reason> |
```

Outcomes: `supported` (exploratory indication, not confirmation), `inconclusive`, `refuted`
(against the pilot's question, not automatic proof of a full hypothesis), `skipped` or `not run`.
Retain negative and infrastructure-failure outcomes. After two failed repair attempts on the same
infrastructure defect, change tactic or escalate, per
[verdicts-and-loops.md](../../ctrl-shared/core/verdicts-and-loops.md).

## Budget report

```text
Pilot phase: complete within budget | budget exhausted | not run
- Chosen limits and user-approved increase: <limits, decision or none>
- Attempts: <n>, skipped/not run: <n with reasons>
- Actual/reserved GPU-hours: <n>/<n>, devices <models/counts>
- Timeout enforcement: <method checked, or unavailable>
- Budget-stopped jobs: <IDs, elapsed use and confirmed termination; or none>
- Influence on confirmatory plan: <choices informed by pilots; independent evaluation planned>
- Consequence for G1: <initial freeze pending | existing plan re-frozen with date | no change>
```

Never silently extend budgets, lose track of a background run, report a reminder as a forced
kill, or promote pilot-selected settings using the same pilot data as independent confirmation.
