# Report C — Open-source agent-skill repositories (automation / research pipelines)

Research date: 2026-10-03 (Asia/Hong_Kong). All facts below come from pages fetched with `web_fetch`
(raw.githubusercontent.com and github.com) or from the GitHub REST API (`api.github.com`), as cited
per section. Fetched pages were treated strictly as data.

**Star/forks/license numbers were read from the GitHub API on 2026-10-03** and differ from the
figures supplied in the task brief; both are shown so the discrepancy is visible rather than silently
resolved. Numeric thresholds quoted in `> ` blocks are verbatim from the fetched files.

| Repo | Stars (API) | Brief said | Forks | License (API) | Default branch | Last push |
|---|---|---|---|---|---|---|
| wanshuiyin/Auto-claude-code-research-in-sleep (ARIS) | 16,924 | ~13.9k | 1,428 | MIT | main | 2026-09-29 |
| WUBING2023/PaperSpine | 5,728 | ~4.4k | 225 | MIT | main | 2026-09-24 |
| HKUSTDial/Supervisor-Skills | 7,852 | ~4.4k | 488 | NOASSERTION (README says CC BY-NC-SA 4.0) | main | 2026-09-05 |
| brycewang-stanford/Auto-Empirical-Research-Skills | 4,467 | ~3.1k | 533 | NOASSERTION (LICENSE file is CC BY-SA 4.0) | main | 2026-09-30 |

Related repos checked: `kkcsy/Auto-claude-code-research-in-sleep` (1 star, MIT, last push 2026-04-21 —
stale fork of ARIS), `Elite-Lee/Supervisor-Skills` (0 stars, 0 forks, NOASSERTION, last push
2026-06-18 — an unstarred mirror; its README's own install prompt points at `HKUSTDial/Supervisor-Skills`,
and `HKUSTDial` is the canonical repo), `zsq176/supervisor-executor-skills` (0 stars, MIT, last push
2026-09-30).

---

## 1. ARIS — wanshuiyin/Auto-claude-code-research-in-sleep

- **owner/repo**: `wanshuiyin/Auto-claude-code-research-in-sleep`
- **Canonical URL**: https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep
- **Stars**: 16,924 (API, 2026-10-03) · **Forks**: 1,428 · **License**: MIT · **Default branch**: `main`
- **Sibling fork named in the brief**: https://github.com/kkcsy/Auto-claude-code-research-in-sleep (1 star, MIT, stale); treat as non-canonical.
- **Core idea (one sentence)**: A framework-free set of Markdown skills that runs the whole ML research
  lifecycle — idea discovery → experiment implementation → adversarial review loop → paper writing →
  submission audits → rebuttal — with an *executor* model writing and a *different model family* acting
  as the independent reviewer.

Sources fetched: repo `README.md`, `AGENT_GUIDE.md`, `docs/SKILLS_CATALOG.md`,
`skills/shared-references/effort-contract.md`, `skills/shared-references/assurance-contract.md`,
`skills/auto-review-loop/SKILL.md`, `skills/idea-discovery/SKILL.md`.

### 1.1 v0.4.x capabilities as requested

| Requested capability | Evidence found | Status |
|---|---|---|
| Plan mode | README changelog line for **v0.4.1 (2026-04-15)**, verbatim: `> **v0.4.1** (2026-04-15) — **Plan mode** (`/plan`) | Cooperative Ctrl+C interrupt | Auto-retry (429/5xx/network) | **Research Wiki** 📚 (persistent knowledge base) | **Self-Evolution** 🧬 (`/meta-optimize`) | Local models (LM Studio/Ollama) | 62 skills synced`. This is the ARIS-**Code CLI** release line, not a skill named `/plan` in the skill catalog. | Plan mode confirmed in the changelog; **UNVERIFIED**: the full behaviour/spec of `/plan` (no SKILL.md or reference for it was located). |
| Autonomous ML research | README tagline: "Let Claude Code do research while you sleep." `/research-pipeline` = W1 → W1.5 → W2 → W3 with no human in the loop by default (`AUTO_PROCEED: true` default). | Confirmed |
| Cross-model review loops | `/auto-review-loop` (W2) review → fix → re-review; executor and reviewer must be different model families; 5-layer audit chain; reviewer routing (`codex` / `oracle-pro` / `agy` / `manual` / Copilot-native `rubber-duck`). | Confirmed |
| Idea discovery | `/idea-discovery` (W1) chains `research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline`, plus `/idea-discovery-robot` for robotics. | Confirmed |
| Experiment automation | `/experiment-bridge` (W1.5), `/run-experiment`, `/monitor-experiment`, `/analyze-results`, `/experiment-queue` (SSH queue with OOM retry, stale-screen cleanup, wave gating), `/training-check`, `/vast-gpu`, `/serverless-modal`, `/qzcli`. | Confirmed |

Note on version numbering: the README's "v0.4.28 (2026-09)" releases describe the **ARIS-Code standalone
CLI**, while the skill catalog is pinned separately ("Bundle 81→83", "83 skills"). Do not conflate the two
version axes when citing "v0.4.x" in the new pack.

### 1.2 Exact skill names and one-line purposes (all 83, from `docs/SKILLS_CATALOG.md`)

Invocation syntax is uniform: `/skill-name "arguments" — key: value, key2: value2`.
Every skill also ships a Codex CLI mirror under `skills/skills-codex/<name>/SKILL.md` (and
`skills-codex-claude-review/`, `skills-codex-gemini-review/` overlays).

**Workflow orchestrators**

| Skill | Purpose |
|---|---|
| `/research-pipeline` | Full chain W1 → W1.5 → W2 → W3, research direction to submission-ready paper |
| `/idea-discovery` | W1 — research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline |
| `/idea-discovery-robot` | W1 adapter for robotics / embodied AI — robotics-aware survey + benchmark-anchored ideation |
| `/experiment-bridge` | W1.5 — read experiment plan → implement code → sanity check → deploy to GPU → collect initial results |
| `/auto-review-loop` | W2 — autonomous review → fix → re-review until positive or max rounds (Codex MCP reviewer) |
| `/auto-review-loop-llm` | W2 variant using any OpenAI-compatible LLM via `llm-chat` MCP |
| `/auto-review-loop-minimax` | W2 variant pinned to the MiniMax API |
| `/paper-writing` | W3 — paper-plan → paper-figure → illustration → paper-write → paper-compile → improvement loop |
| `/rebuttal` | W4 — parse reviews → atomize → strategy → draft → safety check → stress test → 2-version output → follow-ups |
| `/resubmit-pipeline` | W5 — text-only port across venues (no new experiments, no bib edits) |
| `/paper-talk` | W6 — paper → slide outline → Beamer + PPTX → per-page polish → assurance audits → final report |
| `/research-refine-pipeline` | Sub-pipeline: refine method + plan experiments in one chain |
| `/patent-pipeline` | Full patent drafting: invention → claims → spec → jurisdiction format (CN/US/EP) |
| `/dse-loop` | Autonomous design-space exploration loop for computer architecture / EDA |
| `/meta-optimize` | W-M — analyse usage logs, propose SKILL.md / prompt / default-parameter improvements |
| `/meta-apply` | Privileged landing gate — only skill allowed to mutate the skill corpus, after a cross-model jury PASS |

**Literature & search**: `/research-lit` (multi-source search + cross-source dedup), `/arxiv`,
`/semantic-scholar`, `/deepxiv` (progressive reading), `/exa-search`, `/web-debug-search`,
`/openalex`, `/gemini-search`, `/alphaxiv`, `/comm-lit-review`, `/novelty-check` (multi-source +
cross-model verification + closest-prior-work table).

**Ideation & method design**: `/idea-creator` (brainstorm 8-12 ideas, filter, pilot on GPU, rank by
signal), `/research-refine` (problem anchor → up to 5 review rounds → score ≥ 9), `/experiment-plan`
(claim-driven roadmap with ablations, budgets, run order), `/ablation-planner` (ablations from a
reviewer's perspective), `/formula-derivation`.

**Proof engineering**: `/proof-orchestrator` (stateful proof-run orchestration, run directories,
manual GPT Pro handoff packages).

**Experiments & infrastructure**: `/research-implement-feature`, `/run-experiment`,
`/monitor-experiment`, `/analyze-results`, `/experiment-queue`, `/vast-gpu`, `/serverless-modal`,
`/qzcli`, `/training-check`, `/system-profile`.

**Review, audit & assurance**: `/research-review`, `/experiment-audit`, `/result-to-claim`,
`/paper-claim-audit`, `/citation-audit`, `/proof-checker` (20-category issue taxonomy, two-axis
severity, counterexample red team, proof-obligation ledger), `/kill-argument`, `/integrity-forensics`
(46 patterns, typed BLOCK/WARN gate).

**Paper writing & figures**: `/paper-plan`, `/paper-write`, `/paper-figure`, `/figure-spec`,
`/paper-illustration`, `/paper-illustration-image2`, `/mermaid-diagram`, `/pixel-art`,
`/paper-compile`, `/auto-paper-improvement-loop` (2-round review, "typical 4/10 → 8.5/10 score lift"),
`/proof-writer`, `/writing-systems-papers` (page allocation + paragraph templates for OSDI/SOSP/
ASPLOS/NSDI/EuroSys), `/grant-proposal` (KAKENHI/NSF/NSFC incl. 面上/青年/优青/杰青/海优/重点/ERC/DFG).

**Talks, posters, resubmission**: `/paper-slides`, `/slides-polish`, `/paper-poster-html` (default
poster pipeline, measurement-driven hard gates, print-ready PDF via headless Chromium), `/paper-poster`
(deprecated redirect stub).

**Patents**: `/invention-structuring`, `/claims-drafting`, `/embodiment-description`,
`/specification-writing`, `/figure-description`, `/prior-art-search`, `/patent-novelty-check`,
`/patent-review`, `/jurisdiction-format`.

**Meta & utilities**: `/research-wiki`, `/wiki-enrich`, `/render-html`, `/overleaf-sync`,
`/feishu-notify`, `/interview-cheatsheet`.

### 1.3 Notable mechanisms worth reusing

1. **Two orthogonal control axes.** `effort` (depth/cost) and `assurance` (audit strictness) are
   independent; this was introduced precisely because they used to be conflated (a user reported
   `effort: beast` producing "draft-quality" output with all three submission gates skipped).
2. **Cross-model invariant with fail-closed routing.** "executor and reviewer **must** be different
   model families. Same-family review is a non-feature." Reviewer prompts receive **file paths only**,
   never summaries or interpretations. Audit-class skills open a **fresh** thread per round
   ("narrative accumulation inflates scores"); `/auto-review-loop` is the documented exception
   (one thread + `codex-reply` for round-to-round reviewer memory).
3. **5-layer audit chain, each layer a different skill**: `/experiment-audit` ("Is the eval code
   honest? no fake GT, no self-normalized scores, no phantom results") → `/result-to-claim` (does the
   claim follow from the result) → `/paper-claim-audit` (zero-context numeric verification) →
   `/citation-audit` (existence + metadata + context appropriateness) → `/kill-argument` (adversarial
   Attack-Adjudication: Thread 1 writes the strongest 200-word rejection memo a senior area chair
   would produce; Thread 2 is an independent adjudicator, not a defender, classifying each point
   `answered_by_current_text` / `partially_answered` / `still_unresolved` with file:line evidence).
4. **Machine-readable verdict + hash-freshness gate.** Every mandatory audit writes a JSON artifact
   with `verdict`, `reason_code`, `audited_input_hashes` (SHA256 per consumed file), `trace_path`,
   `thread_id`, `reviewer_model`, `reviewer_family`, `review_independence`, `acceptance_status`.
   `verify_paper_audits.sh` re-hashes current files and emits `STALE` if anything changed after the
   audit ran; at `assurance: submission` a non-zero exit blocks the Final Report.
5. **Honest-skip distinction (`NOT_APPLICABLE` ≠ `SKIP`).** A silent skip leaves no record; the
   contract forces an artifact documenting "we checked, there's nothing to verify".
6. **Result-to-claim verification and ablation planning** as first-class skills (`/result-to-claim`
   writes claim status `supported` / `invalidated` / `pending` into the Research Wiki;
   `/ablation-planner` runs only after main results pass `/result-to-claim`).
7. **Evidence precheck and integrity tooling**: `tools/verify_papers.py` (3-layer fallback:
   arXiv batch API → CrossRef DOI → Semantic Scholar fuzzy title match) with 4 per-paper states
   `verified` / `unverified` / `verify_pending` / `error`, transient failures tagged `verify_pending`
   and **excluded from the hallucination rate**, unverified papers retained tagged `[UNVERIFIED]`
   (retention-over-silent-removal).
8. **Reproducibility / resumability**: `REVIEW_STATE.json` survives context auto-compaction;
   `.aris/runs/<run_id>.json` run state + deterministic evidence gates; `.aris/traces/<skill>/<date>_run<NN>/`
   forensic reviewer traces; `tools/watchdog.py` (alerts when an unattended loop stops updating its
   state file, never restarts a verdict-bearing run) and `tools/iteration_log.py` (stall detection).
9. **Output hygiene**: one canonical deliverable per pipeline via the `— composed: <path>` directive,
   so sub-skills fold findings in instead of scattering overlapping `.md` files.
10. **Gate/mechanism vocabulary to port**: `acceptance-gate.md` — "a loop can DRIVE, it cannot ACQUIT"
    (a loop may self-judge execution completeness, never quality/correctness);
    `external-cadence.md` — `/loop`, `/schedule`, `CronCreate` are "fire-control, never a jury";
    `review-scope-limits.md` — a block every reviewer prompt carries that bounds what a reviewer may
    *propose* (no hashes/digest schemes, no speculative machinery, no corner-case obsession), never
    what it looks for.
11. **Self-evolution with a privilege split**: `/meta-optimize` (read-only producer of patches) vs
    `/meta-apply` (the only skill allowed to mutate the corpus, after a fresh cross-model jury PASS on
    the staged diff).

### 1.4 Numeric thresholds, gates and rubrics (verbatim)

**Effort levels and hard invariants** (`skills/shared-references/effort-contract.md`):

> `lite` (~0.4x tokens) … **Implies `assurance: draft`**.
> `balanced` (1x tokens) — DEFAULT … **Implies `assurance: draft`**.
> `max` (~2.5x tokens) … **Implies `assurance: submission`**.
> `beast` (~5-8x tokens) … **Implies `assurance: submission`**

> | Codex reasoning_effort | **≥ xhigh** (deep-audit skills run `ultra` …) | Reviewer quality is non-negotiable. … and ARIS `— effort: max` is NOT Codex `model_reasoning_effort: max` |
> | DBLP/CrossRef citations | **on** | Citation integrity is non-negotiable |
> | Reviewer independence | **on** | Cross-model protocol is non-negotiable |
> | Experiment integrity | **on** | Fraud prevention is non-negotiable |
> | Sanity check | **on** | Safety is non-negotiable |

Per-skill numeric profiles (lite / balanced / max / beast), verbatim rows:

> research-lit — papers found: 6-8 / 10-15 / 18-25 / 40-50
> research-lit — query variants: 2 / 5 / 8 / 15+
> research-lit — deep reads: 3 / 5-8 / 8 / 15+
> idea-creator — ideas generated: 4-6 / 8-12 / 12-16 / 20-30
> idea-creator — pilots: 1-2 / 2-3 / 3-4 / 5-6
> novelty-check — closest works: top-3 / top-5 / top-8 / top-10+
> research-refine — max rounds: 3 / 5 / 7 / 10+
> experiment-plan — core experiments: 3 / 5 / 7 / 10+
> experiment-plan — seeds: 1 / 3 / 5 / 5
> experiment-plan — baseline families: 2 / 3 / 4 / 5+
> ablation-planner — ablations: 2-3 / 4-5 / 6-8 / 10+
> auto-review-loop — max rounds: 2 / 3-4 / 6 / 8+ (until converged)
> research-review — passes: 1 / 1 + follow-up / 1 + 2 follow-ups / 2 independent + cross-compare
> experiment-audit — depth: skip / basic 4 checks / full 6 checks / line-by-line + reproduce
> auto-paper-improvement — rounds: 1 / 2 / 3 / 5
> paper-illustration — render iterations: 2 / 3 / 5 / 7
> rebuttal — draft rounds: 1 / 2 / 3 / 5
> rebuttal — stress tests: 0-1 / 1 / 2 / 3

Token-cost table, verbatim: `lite | ~0.4x | ~0.5x`; `balanced | 1x | 1x`; `max | ~2.5x | ~2x`;
`beast | ~5-8x | ~3-4x`.

Precedence, verbatim:

> explicit concrete knob (e.g., review_rounds: 2) > explicit dimension override > overall effort level > skill default (balanced)

Transparency line every skill should print, verbatim template:
`⚡ [effort: max] papers=25, ideas=16, rounds=6 | Codex: tier per reviewer-routing.md (floor xhigh)`

**Assurance verdict state machine** (`skills/shared-references/assurance-contract.md`) — six states,
"Draft: Audits run only if their content detector matches. Silent skip allowed." vs
"`submission`: All mandatory audits **must** emit a verdict … Silent skip is **forbidden**."

> `PASS` … Submission-blocking? No
> `WARN` … No
> `FAIL` … **Yes**
> `NOT_APPLICABLE` … Audit phase ran, child audit invocation may have been skipped … No
> `BLOCKED` … Could not complete … **Yes**
> `ERROR` … Attempted but errored … **Yes** at submission

Verifier contract (7 numbered duties, verbatim highlights): the verifier must
"Recompute SHA256 of every file in `audited_input_hashes`; flag `STALE` if any mismatches",
"Verify `trace_path` exists and is non-empty", and
"Output a structured JSON report and exit 0 (all green) or 1 (any FAIL / BLOCKED / ERROR / STALE /
missing artifact)". `overall_assurance` is `blocked` / `provisional` / `accepted`, where
"Provisional remains exit 0 but must never be presented as submission-ready yes."
Also: "the audit aggregator REJECTS a deterministic label on the four semantic paper audits
(proof / claims / citations / attack), which only a cross-family model review can accept."

**`/auto-review-loop` constants** (`skills/auto-review-loop/SKILL.md`), verbatim:

> - MAX_ROUNDS = 4
> - POSITIVE_THRESHOLD: score >= 6/10 **AND** verdict ∈ {"ready", "almost"} — **both** must hold. … the verdict vocabulary is {"ready", "almost", "not ready"} (a high score with a "not ready" verdict does NOT stop the loop).
> - HUMAN_CHECKPOINT = false
> - REVIEWER_DIFFICULTY = medium — `hard`: adds **Reviewer Memory** … + **Debate Protocol** … `nightmare`: Everything in `hard` + **Codex exec reviewer reads the repo directly** … + **Adversarial Verification**
> - MAX_ROUNDS … resume rule: state file older than 24 hours → fresh start.

Debate rulings vocabulary, verbatim: `SUSTAINED` / `OVERRULED` / `PARTIALLY SUSTAINED`;
"Maximum 3 rebuttals per round". Exhaustion rule, verbatim: "try at least 2 different solution
paths … only then concede narrowly and bound the damage. Never give up on the first attempt."
`ACQUITTAL_LOG.jsonl` rules: "Append-only | Never delete, never truncate, never overwrite lines. Only `>>`."
Stop-gate state-transition test list: 9 numbered cases.

**`/idea-discovery` constants** (verbatim) — the most directly portable budget gates:

> - **PILOT_MAX_HOURS = 2** — Skip any pilot experiment estimated to take > 2 hours per GPU. Flag as "needs manual pilot" in the report.
> - **PILOT_TIMEOUT_HOURS = 3** — Hard timeout: kill any running pilot that exceeds 3 hours.
> - **MAX_PILOT_IDEAS = 3** — Run pilots for at most 3 top ideas in parallel.
> - **MAX_TOTAL_GPU_HOURS = 8** — Total GPU budget across all pilots. If exceeded, skip remaining pilots and note in report.
> - **AUTO_PROCEED = true** — When `true`, checkpoints are informational … Set to `false` to ask for explicit user confirmation and end the turn at each selection checkpoint.
> - **RESUMABLE = true** — Record stage evidence under `.aris/runs/<run_id>.json` and require a deterministic evidence gate before declaring the final report complete.

Reviewer-bearing-phase receipt rule, verbatim: "For `novelty-check`, **both PROCEED and PROCEED WITH
CAUTION are positive verdicts** … only ABANDON is negative." And: "A negative verdict does not grant a
review receipt." Gate failure text: `BLOCKED: <stage> evidence missing`. The run-state gate helper
writes to `gates.idea-discovery-evidence`.

**Other quantified rules found in fetched catalogs/changelogs**

- `/research-refine`: "Iterative method refinement — problem anchor → up to 5 review rounds → score ≥ 9".
- `/idea-creator`: "Brainstorm 8-12 ideas, filter by feasibility, pilot on GPU, rank by signal".
- `/auto-paper-improvement-loop`: "2-round content review + format check — typical 4 / 10 → 8.5 / 10 score lift".
- `/research-review` reviewer default: "gpt-6-astra with two-tier reasoning (deep-audit `ultra` / regular `xhigh` …)".
- `tools/verify_papers.py`: "arXiv batch API up to 40 IDs/request → CrossRef DOI lookup → Semantic
  Scholar fuzzy title match, **default 0.6 word-overlap**"; "cache … with **30-day TTL**";
  "canonical key priority `arxiv:{id_without_version}` → `doi:{lowercase}` → `title:{sha1[:16]}`".
- Output manifest: maintain `MANIFEST.md` "only above the **15-artifact threshold**".
- `/integrity-forensics`: "46 patterns"; `/paper-poster-html` gate machinery adapted from `posterly` (MIT).
- Stall detection: "two empty rounds force a change of direction, **four** call in a human".
- `/slides-polish`: "PPTX font scaling **1.5-1.8×** for projector-readable size".
- Helper resolution chain (writing new skills), verbatim:
  `Layer 0: ${CLAUDE_SKILL_DIR}/scripts/<helper>` → `Layer 1: .aris/tools/<helper>` →
  `Layer 2: tools/<helper>` → `Layer 3: $ARIS_REPO/tools/<helper>`, with failure policies A (gate) /
  B (side-effect) / C (forensic) / D1 (cascade) / D2 (multi-source aggregate) / E (diagnostic).

**Not-covered / UNVERIFIED in ARIS**: the individual SKILL.md bodies for most of the 83 skills were not
fetched, so phase-by-phase internal gates beyond `/auto-review-loop` and `/idea-discovery` are not
quoted here. The exact contents of `/plan` are UNVERIFIED. Star history beyond the API snapshot is not
checked.

---

## 2. PaperSpine — WUBING2023/PaperSpine

- **owner/repo**: `WUBING2023/PaperSpine` (product name "PaperSpine5")
- **Canonical URL**: https://github.com/WUBING2023/PaperSpine · Product page: https://wubing2023.github.io/PaperSpine/v5/
- **Stars**: 5,728 (API, 2026-10-03) · **Forks**: 225 · **License**: MIT (README: "MIT License.") · **Default branch**: `main`
- **Current release**: `v0.4.0-alpha.3` (pre-release); Windows x64 ≈ 26.5 MB, Linux glibc x86_64 ≈ 56.2 MB,
  macOS arm64 ≈ 40.6 MB, macOS x86_64 ≈ 40.5 MB, all SHA-256 verified.
- **Core idea (one sentence)**: One host skill that carries a paper from local materials to an
  evidence-bound manuscript — research, citation verification, figures, Word/LaTeX/PDF delivery and
  same-task revision — with a Web UI only for configuration, user choices, preview and download.

Sources fetched: `README.md`, `dist/claude/skills/paper-spine/SKILL.md`,
`dist/claude/commands/paperspine.md`, `dist/claude/skills/paper-spine/references/paper-spine-production-protocol.md`,
`.../references/review-policy.md`, `.../references/visual-readiness-gate.md`, plus the repo git tree.

### 2.1 Exact skill / command / agent names

| Name | Type | One-line purpose |
|---|---|---|
| `paper-spine` | Skill (`dist/claude/skills/paper-spine/SKILL.md`) | The orchestrator: research, write, review and deliver an evidence-bound paper in one task, with user choices, real files, editable outputs and same-task revision |
| `/paperspine` | Claude command (`dist/claude/commands/paperspine.md`) | Open or resume the current PaperSpine workflow, or handle an explicit update request |
| `paperspine.md` | Codex prompt (`dist/codex/prompts/paperspine.md`) | Codex-host projection of the same entry point |
| host projections | `dist/codex/skills/paper-spine`, `dist/claude/skills/paper-spine`, `dist/openclaw/skills/paper-spine` | Per-host copies of the same skill |

Sub-agents (from the repo tree, `agents/`):
`research-exemplar`, `research-scene`, `research-sota` (research side) and
`reviewer-evidence`, `reviewer-method`, `reviewer-writing` (independent review side).
*Note*: only the three `reviewer-*` names are visible as agent filenames; their full prompts were not
fetched, so their internal rubrics are UNVERIFIED.

References: **81 playbooks** under `dist/claude/skills/paper-spine/references/` (counted from the git
tree), including `paper-spine-production-protocol.md`, `review-policy.md`, `results-validation.md`,
`scientific-evidence-ledger.md`, `writing-rationale-matrix.md`, `citation-support-bank.md`,
`figure-story.md`, `figure-reference-mapping.md`, `scientific-figure-workflow.md`,
`visual-readiness-gate.md`, `publication-surface.md`, `submission-metadata.md`, `submission.md`,
`reviewer-audit.md`, `evidence-grounded-review.md`, `round1-literature-revision.md` …
`round4-template-integration.md`, `scenario-journal.md` / `scenario-conference.md` /
`scenario-competition.md` / `scenario-report-review.md`, `platform-cnki.md` / `platform-weipu.md` /
`platform-general.md`, `journal-transfer.md`, `logic-transfer-audit.md`, `translate.md`,
`translation-package.md`, `humanize.md` / `humanize-calibration.md`, `adaptive-shadow.md`,
`deep-imitation-protocol.md`.

Scripts/tools named in README and playbooks (verbatim names): `writing_rationale_matrix`,
`citation_support_bank`, `translation_package`, `artifact_check.py`, `reference_inventory.py`,
`citation_bank_check.py`, `latex_guard.py`, `word_guard.py`; plus, from fetched playbooks,
`scripts/paperspine_update.py --preflight --yes`, `scripts/paperspine5_web.py launch`,
`scripts/visual_readiness_check.py [--prepare|--write]`, `author_voice_check.py`, `humanize_check.py`.
*UNVERIFIED*: the complete script inventory (the repo tree was not enumerated exhaustively for `scripts/`).

### 2.2 Notable mechanisms worth reusing

1. **17-step production protocol** (`paper-spine-production-protocol.md`) that is explicitly *not* a
   checklist: "Apply only the steps needed for the saved workflow… These are host work instructions,
   not new backend states or per-step gates." Each step has a **"Check and use:"** clause that states
   what must be *observed*, not merely produced — e.g. "A listed filename or successful registration
   does not prove reading", "A prefill is not a save", "A route name, method list or summary does not
   prove application", "Hashes/mtimes identify files but cannot establish semantic parity."
2. **Defect-based repair loop with a buck-stops rule**: "When a defect is found, make the **next action
   a concrete source repair**, not 'continue step N'"; "If two targeted attempts leave the same defect
   unchanged, stop that tactic"; "A new hash alone does not reset this rule."
3. **Research-mode contract separate from depth**: `required` / `agent_decide` / `materials_only`
   where `materials_only` still allows literature reading, faithful extraction, plotting supplied
   results and consistency checks but forbids new EDA/tests/modelling/reruns — an unusually precise
   way to stop an agent from silently re-analysing user data.
4. **Evidence contract + object-reference discipline**: every claim has source/result support and a
   bounded uncertainty; steps 14–15 require native citation/cross-reference fields so links survive
   reordering, and require submission and reading surfaces to share one semantic source.
5. **Figure planning as job assignment, not a quota**: "map the full result inventory to the paper's
   questions. Decide the jobs of the main figures, mechanism/conceptual figure, tables and supplement…
   There is no arbitrary panel quota."
6. **Two-tier independent review policy** (`balanced` default / `strict`), with an explicit
   anti-bureaucracy stance: "Strict mode still must not reward bureaucracy. An artifact passes because
   it captures a useful decision or verifiable fact, not because it is long."
7. **Honest-readiness vocabulary**: tool success, hashes and task status do not establish scientific,
   editorial, visual or submission readiness; final status must separately state scientific quality,
   editorial/visual quality, technical portability, local delivery and submission readiness.
8. **Visual gate with explicit re-render invalidation**: "Any changed PDF/TeX/figure hash invalidates
   the receipt and requires render + inspection again. An unavailable renderer, missing page,
   unrendered SVG, unresolved conflict, or pending check keeps `visual_ready=false`."

### 2.3 Numeric thresholds, gates and rubrics (verbatim)

From the 17-step protocol:

> Default learning is 3 same-direction plus 3 target-venue papers; a deeper request uses 6+6; an explicit count wins.

> The bibliography count must satisfy the user's configured count and, by default, be **above the observed mean of the target exemplars** unless the user specifies otherwise.

> If two targeted attempts leave the same defect unchanged, stop that tactic

> After the first complete draft, reserve work for **at least one evidence/argument pass, one
> figure/layout pass and one independent review/repair pass** whenever the inputs support them.

> do not stop because a first PDF compiled or because a nominal round count was reached.

From `review-policy.md` (severity gating):

> CRITICAL scientific defects block. MAJOR findings block only when they affect a primary claim, figure/text identity, citation truth, or deliverable usability. MINOR/style findings are advisory.

> A gate may report `PASS_WITH_ADVISORIES`; this does not mean the advice must be converted into more forms before writing can continue.

> Judge manuscript completeness through **one free-form editor synthesis, not a fixed scorecard**.

> Use `review_policy` from the current saved configuration; … Missing/unknown values resolve to `balanced`.

Also, the SKILL.md's own config contract: guided work continues only when "Configuration needs
`source=web_user`, `user_confirmed=true`, `readiness.ready=true`".

From `visual-readiness-gate.md` (failure definition — portable verbatim):

> A blank or nearly blank page, an avoidable page with only a small remnant of text, or a large unexplained void in the middle of a manuscript is a visual failure. Do not solve it by shrinking all text: first repair float placement, figure/table size, paragraph breaks, section order or the correct venue surface.

> Check the smallest labels at physical output size independently in PDF and Word; **DPI is not a label-size measurement**.

> A visible conflict such as a different method name inside the figure is a submission blocker even when the filename and caption look correct.

> A resulting-field set: `story_claim_alignment`, `panel_role_alignment`, `claim_boundary_respected` plus panel-level receipts.

**UNVERIFIED in PaperSpine**: the internal reviewer rubric (the `reviewer-*` agent prompts), any
numeric rubric inside `reviewer-audit.md` / `evidence-grounded-review.md`, and the exact CLI surface of
the 3 named scripts beyond the invocations quoted above. The README's claim that `-CleanLegacy`
"先只读预览" (read-only preview first) and the SHA-256 self-checks on first start are from the README
only; not independently verified.

---

## 3. Supervisor Skills — HKUSTDial/Supervisor-Skills (and zsq176/supervisor-executor-skills)

- **owner/repo (canonical)**: `HKUSTDial/Supervisor-Skills` — https://github.com/HKUSTDial/Supervisor-Skills
- **Stars**: 7,852 (API, 2026-10-03) · **Forks**: 488 · **Default branch**: `main`
- **License**: README states `[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)`;
  the GitHub API reports `NOASSERTION`; **per-skill front matter is mixed** — `idea-evaluator` and
  `pre-submission-reviewer` declare `license: CC-BY-4.0`, while `paper-writer`, `deep-research` and
  `paper-polish` declare `license: CC-BY-NC-SA-4.0`. *Porting note: confirm per-file licence before reuse.*
- **Brief's URL** `Elite-Lee/Supervisor-Skills` exists but has **0 stars / 0 forks** and last pushed
  2026-06-18 — an unstarred mirror. Its README's install prompt itself points at
  `https://github.com/HKUSTDial/Supervisor-Skills`, and the "Star History" widget in the same README
  charts `HKUSTDial/Supervisor-Skills`. Treat HKUSTDial as canonical (author: Yuyu Luo, HKUST-GZ).
- **Core idea (one sentence)**: Distil a supervisor's decade of top-venue reviewing/publishing
  judgement into small, immediately-copyable AI skills (plus a handbook) that evaluate an idea, plan
  the paper's logic, draft prose, design figures, and audit a draft before submission.

Sources fetched: `README.md`, and `skills/*/SKILL.md` for
`idea-evaluator`, `pre-submission-reviewer`, `paper-writer`, `paper-polish`, `deep-research`,
`rebuttal-guidance`, `drawio-reconstruction` (7 of 12), plus the repo git tree.

### 3.1 Exact skill names and one-line purposes

The README documents **7** skills under the path `plugins/phd-research/skills/<name>/SKILL.md`; the
actual repo tree (**236 entries**) places **12** skills at `skills/<name>/SKILL.md`. The README's tree
diagram and docs are therefore out of date relative to the tree — use `skills/<name>/`.

| Skill (confirmed path `skills/<name>/SKILL.md`) | One-line purpose |
|---|---|
| `idea-evaluator` | Score a draft idea on the five dimensions (Higher/Faster/Stronger/Cheaper/Broader) + lifecycle-capability match + paradigm-shift probe + fatal-flaws audit, and return a reviewer-style verdict |
| `vibe-research-workflow` | AI-assisted research workflow guidance: Vibe Coding / Vibe Figure / Vibe Writing |
| `intro-drafter` | Generate a high-quality Introduction outline from the motivation, using the Introduction flowchart thinking model |
| `tech-paper-template` | Walk the author step by step through the full logic chain using the technical full-paper template |
| `benchmark-paper-template` | Plan benchmark/evaluation papers: evaluation logic and experiment design |
| `pre-submission-reviewer` | Top-venue-reviewer-style audit of a draft across five dimensions with CRITICAL/MAJOR/MINOR severity tags |
| `figure-designer` | Professional figure advice per the motivated-example / solution-overview / experimental-results design paradigms |
| `deep-research` | Survey-grade literature investigation: freeze RQs, search from adversarial perspectives, verify every citation, synthesize a MECE taxonomy |
| `paper-writer` | Draft publishable prose (paragraph to full manuscript) where every factual claim traces to user input, verified retrieval or field common knowledge |
| `paper-polish` | Polish existing prose (grammar/flow/AI-tone/Chinese→English) while never silently changing scientific meaning |
| `rebuttal-guidance` | Per-concern rebuttal **guidance** (not prose) using conditional persuasion P(Z\|X,Y) |
| `drawio-reconstruction` | Reconstruct reference images into high-fidelity editable `.drawio` files with rendered previews |

Handbook chapters (from README, for context): 01 Preliminary (how to judge a paper's quality),
02 Idea Generation (idea lifecycle, "更高更快更强", disruptive innovation), 03 Paper Writing
(full-process, Introduction model, technical/benchmark templates, writing checklist),
04 Scientific Plotting (motivated example / solution overview / experimental results figures + checklist),
05 Vibe Research, 06 Case Studies (ICML'25 Alpha-SQL, ICLR'25 AFlow, VLDB'26 LEAD).

### 3.2 Contrast: zsq176/supervisor-executor-skills

- https://github.com/zsq176/supervisor-executor-skills · **0 stars, 0 forks, MIT**, last push 2026-09-30.
- Ships exactly **two** skills: `supervisor/SKILL.md` (`/supervisor`) and `executor/SKILL.md`
  (`/executor`), plus `AGENTS-template.md`.
- Core idea: split a two-window AI coding workflow by decision/execution — the scarce high-capability
  model only *thinks*, the abundant model *does*, and they hand off through a project-root `AGENTS.md`.
- The single division-of-labour rule, verbatim Chinese: **"Supervisor 替 Executor 思考，Executor 只负责执行。"**
- Reusable mechanisms (its numbers are small but sharp): **TRIAGE first** (A = hand the chore straight
  down; B = hand down after light judgement; C = only architecture / trade-off / irreversible /
  cross-layer-full work gets deep thinking); **"省额度 = 少参与次数 + 少轮次 + 一次到位"**;
  **"深度 ≠ 长度"** with the plan opening with the 3–5 largest risks then defining only
  taxonomies, criteria and thresholds; the handoff file is a **six-section structure with a hard cap of
  about 100 lines** (`约 100 行硬上限`); verdict vocabulary is exactly
  **`PASS / REWORK / DECISION REQUIRED`**; graded acceptance that is never skipped
  (low risk = evidence only, high risk = deep check against the plan); the Executor must write
  `DECISION REQUIRED` into `AGENTS.md` and pause that part rather than redesign.
- **Contrast in one line**: HKUSTDial is a *knowledge-distillation* pack (12 content skills + handbook,
  non-commercial licence), while zsq176 is a *token-economics controller* (2 role skills + one handoff
  file, MIT) — the two are complementary, and zsq176's TRIAGE/AGENTS.md pattern is the better source
  for cheap multi-model routing, HKUSTDial's for reviewer rubrics.

### 3.3 Rubrics and thresholds worth porting (verbatim)

**`idea-evaluator` — the five-dimension scoring rubric:**

> Score each 1-10 with explicit evidence from the user's stated contribution.

> Scoring discipline: **start every dimension at 5 and justify movement.** Two kinds of grounds move a score up, and both count: measured results the user reported (quote them), or a mechanism argument that holds up (label the score "mechanism-based, not yet confirmed by data"). A solid, untested mechanism **can** reach 8 or 9 with that label plus a named validation experiment; do not systematically cap untested ideas. A dimension with neither data nor mechanism stays at 5 with "no grounds given".

> when an impressive gain plausibly comes from a peripheral factor (routing, post-processing, a stronger base model, favorable samples), cap that dimension until an ablation isolates the core mechanism.

Verdict gate, verbatim:

> - **Strong Accept**: execute now. **Two or more dimensions at 8+, no fatal flaws, capability match green, lifecycle fit.**
> - **Accept with Revisions**: pivot the scope per recommendations before starting. Some dimensions weak, fixable flaws, or lifecycle mismatch that can be shortened.
> - **Reject and Pivot**: do not pursue this version. Dominated by a prior benchmark or method, unfixable capability mismatch, or **more than one fatal flaw**.

Short-circuit + integrity rules, verbatim:

> Run the fatal-flaws audit **before** the scoring steps rather than after them. Identify **at most two** fatal flaws.
> If any fatal flaw is tagged CRITICAL in the severity taxonomy (single-handedly causes rejection, unfixable within the lifecycle), stop here and emit the verdict directly … Do **not** run the five-dimension scoring, paradigm-shift probe, feasibility check, or integrity gate. Those would be decoration on a rejection.
> **A data-refuted core mechanism is an automatic CRITICAL.** … lock the verdict to Reject and Pivot; write no defense and invent no optimistic threshold.
> Two or more yes answers means the idea has disruptive potential. (paradigm-shift probe, 4 questions: First Principles, Elephant in the Room, Technology Cycle, Hamming's Rule)
> **[inspection]** Verdict is consistent with scoring: Strong Accept requires at least two dimensions at 8+ and zero CRITICAL flaws.

Also worth copying: the integrity gate tags each bullet `[inspection]` / `[attestation]` / `[user-attest]`
(a clean way to distinguish what the model can self-verify from what the user must confirm), and its
rule "Run the gate silently. Do not print a per-gate pass or fail report."
Novelty grounding rule, verbatim: "name the three to five closest published works…" and
"'not found' does not prove novelty: report it as 'no directly overlapping work retrieved under these
keywords'"; a near-miss title "alone never establishes duplication; duplication requires failing to
find even one differing axis."

**`pre-submission-reviewer` — five dimensions + severity taxonomy + final score:**

Severity definitions, verbatim:

> - **CRITICAL**: blocks submission. Example: contributions do not map to sections; introduction flowchart broken; no real-world running example; raster figure in final draft; missing key baseline; page-limit violation.
> - **MAJOR**: reviewers will flag in first round. Example: topic-sentence absent from 3+ paragraphs; em-dash in 5+ places; banned AI-tone word in 3+ places; Table 1 comparison missing; chart type mismatched with data.
> - **MINOR**: polish. Example: two long sentences that could be split; default Matplotlib styling; single article error.

> any unresolved CRITICAL forbids "ready to submit", and a **near-ready verdict requires zero CRITICAL and at most two MAJOR**.

> **[inspection]** Final score matches the CRITICAL + MAJOR count; **a score of 9 or 10 requires zero CRITICAL and at most two MAJOR items.**

> Em-dashes are MAJOR by default; banned AI-tone words are MAJOR if they appear **three or more times**.

> Paragraphs are not over **10 lines**; split if so.

Banned AI-tone vocabulary list (verbatim, portable as a lint list): "innovative, pioneering,
revolutionary paradigm, transformative framework, superior, surpass, excel, remarkable, unprecedented,
breakthrough performance, general-purpose, is capable of, notably, yet, yielding, at its essence,
encompass, differentiate, reveal, underscore, pave the way for, highlight the potential of, profound
challenges, stems from, rigid, impede."

Other verbatim rules: "Novelty verification: extract two or three keyword groups … identify the three to
five closest published works"; "Retrieval results support metadata-level judgments only"; attribution
check — "an ablation separates the core mechanism from peripheral factors … No such ablation: flag
'attribution unverified' as MAJOR"; "Claims match their evidence: 'solves' is stronger than most papers
earn (usually 'improves')". Output template ends with a 1–10 **Final score** and a three-value
submission recommendation: `Ready to submit | Needs 1-2 days more work | Needs major revision before submission`.

**`deep-research` — six quality gates with severities:**

> | Angle | a judgment, or just a listing? | CRITICAL | back to Step 0 |
> | Coverage | key works all found? | MAJOR | targeted re-scout |
> | Citation | references real and honestly quoted? | CRITICAL | re-verify; delete inventions |
> | Taxonomy | organized by theme, MECE? | MAJOR | redesign axes |
> | Calibration | claim strength matches evidence? | MAJOR | re-calibrate wording |
> | Weaving | in-sentence comparison present? | MAJOR | rewrite flagged sections |

> The loop this creates is the point: a Coverage or Citation failure sends the work back to scouting for a **targeted** supplement … not a restart. Iterate until every gate is CLEAR … **Depth is driven by the topic's complexity, not by a fixed round count.**

> Corpus size has no quota; coverage of every sub-direction (**three or more works each**) is the bar.

Five search perspectives (mainstream school / critics / adjacent fields / methodology / application-policy),
and the grey-zone rule: "unconfirmable means unused".

**`paper-writer` — evidence levels and citation-verification ladder:**

> Every factual claim has one of three origins: the user's materials, this session's verified retrieval, or field common knowledge that carries no numbers, names, or comparisons. **Model memory is never a source.**
> Delivered prose contains **zero bracketed placeholder tags** of any kind.
> **Evidence level caps claim strength.** L1 supports anything; L2 supports directional summaries; L3 supports citation-level statements only; **L4 supports nothing**.
> **Independent citation verification.** Mandatory for full papers, Final mode, or **three or more citations**.

Reference density (guidance, not quota), verbatim: "a full Introduction typically weaves **15-25**
references; a single gap or background paragraph **3-6**; Related Work **15-30**; Methods **3-8** …
Discussion **5-15**; a full paper on the order of **20-40**." Search effort: "run **three to five**
retrieval rounds under different angles". Evidence-map gate: "a claim with no L0-L3 source is not
written as fact. Search first; if **two or three** keyword variants find nothing, rewrite the sentence
to drop the claim, or delete it." Red-flag table has 13 stop-signals ("I remember this scale has 10
items" → "Stop. Uncertain. Omit the item count"). Also the honest-limits line: "Same-context review
reliably catches mechanical issues… It cannot reliably catch its own semantic fabrication; a model that
invented a scenario will confirm that scenario on re-reading."

**`rebuttal-guidance` — the one genuinely novel review mechanism here:**

> The core model is **conditional persuasion P(Z=1 | X, Y)**: X: reviewer mindset (behavior cluster inferred from review text); Y: rebuttal strategy vector (which tactics to emphasize); Z: success (score increase or paper accepted).

> Score the review on **5–7 behavior signals** (openness, severity, constructiveness, specificity, skepticism, harshness, actionability). Map scores to a cluster in references/mindset-library.md.

> **Cohen's d effects**: highlight dimensions with **d > 0.8** in success group.

Concern taxonomy (verbatim): `misunderstanding | evidence_gap | novelty | baseline_fairness |
scope_claim | writing_clarity | theory | efficiency | other`. Per-concern block requires
"Recommended structure: Acknowledge → Response → Evidence → Revision note", `[TO VERIFY]` marking for
anything unverified, no fabricated numbers, defensive phrases flagged. Reference files:
`concern-classification.md`, `mindset-matching-heuristics.md`, `mindset-library.md`,
`strategy-dimensions.md` (10 dimensions), `response-templates.md` (templates A/B/C), `checklist.md`.
*UNVERIFIED*: the actual statistics inside `mindset-library.md` (up-rate, rule-stat diffs) — the file
was not fetched, so the numbers behind "Cohen's d > 0.8" remain internal.

**`paper-polish`** — the faithfulness rule worth porting verbatim: "**Never silently make an edit that
changes scientific meaning.** … Do not strengthen or weaken the author's conclusion … unless you tell
the author and ask them to confirm." Plus "**prefer the small edit over the big one, and no edit over
the small one**", a verb ladder (strong: show/demonstrate/establish; medium: suggest/indicate/be
consistent with; weak: may reflect/appears to), an overclaiming wordlist ("prove, conclusively,
unprecedented, best, superior, state-of-the-art, groundbreaking, first") — note this overlaps and
extends the banned list in `pre-submission-reviewer`.

**`drawio-reconstruction`** — batch trigger threshold, verbatim: "Treat the request as batch
reconstruction when it names a folder, multiple image files, a glob/pattern, or any target that
resolves to **2 or more image entries**"; bounded worker pool "no larger than the available
concurrency"; helpers `batch_manifest.py`, `batch_verify.py`, `check_drawio.py`, `export_drawio.py`,
`crop_assist.py`; blocking-defect list includes "script-only pass without reference comparison" and
"any inventory item still marked `needs-fix`"; the fidelity contract states
"The primary goal is visual fidelity to the reference image. **Editability is secondary.**"
*UNVERIFIED*: whether the referenced `scripts/` helpers are present in the tree (the tree listing
returned only `SKILL.md` files for this skill; the helper directory was not enumerated).

---

## 4. Auto Empirical Research Skills — brycewang-stanford/Auto-Empirical-Research-Skills

- **owner/repo**: `brycewang-stanford/Auto-Empirical-Research-Skills` (maintained by CoPaper.AI, from Stanford REAP)
- **Canonical URL**: https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills
- **Stars**: 4,467 (API, 2026-10-03) · **Forks**: 533 · **Default branch**: `main`
- **License**: `LICENSE` = **Creative Commons Attribution-ShareAlike 4.0 International, Copyright (c) 2026 CoPaper.AI**
  (root `SKILL.md` front matter also declares `license: CC-BY-SA-4.0`); the GitHub API reports
  `Other / NOASSERTION` because the file is a CC summary rather than an SPDX-recognised text. There is
  **no single repo-wide licence for the contents**: `catalog/skills-enriched.json` carries per-collection
  `license` and `commercial_use` fields. *Porting note: check each vendored collection — several are
  third-party and some are non-commercial.*
- **Repo description vs. catalog size — a real discrepancy**: the GitHub description says
  "A curated collection of **23,000+** agent skills for empirical research across 8 social science
  disciplines", while the root `SKILL.md` states "**1,107 skills across 77 vendored collections**".
  Both are quoted as found; which is current **UNVERIFIED** (the README/catalog were not both fetched
  and reconciled).
- **Core idea (one sentence)**: A single router skill over a very large vendored catalog of
  empirical-research skills that classifies a request by stage/method and loads exactly one child
  `SKILL.md` at a time.

Sources fetched: root `SKILL.md`, `LICENSE`, repo root contents, and the repo git tree (partial listing
covering `skills/00*` through `skills/73-*`, `catalog/`, `docs/`, `scripts/`, `tools/`, `tests/`).

### 4.1 Exact names it ships

**Root skill**: `auto-empirical-research-skills` (installed as one skill folder; acts as router + catalog,
"not as a request to load every vendored `SKILL.md`").

**Flagship / named entry points** (verbatim from `SKILL.md`):

| Name | One-line purpose |
|---|---|
| `/paper-workflow` | Full-pipeline trigger for `skills/69-Paper-WorkFlow/` |
| `skills/69-Paper-WorkFlow/` | Orchestrator: raw data → analysis → writing → assembled `09_submission/main.docx`; a git submodule |
| `skills/00-Full-empirical-analysis-skill_StatsPAI/` | Agent-native causal analysis (one call runs DiD / RD / IV / SCM / DML with automatic robustness gates) |
| `skills/00.1-Full-empirical-analysis-skill_Python/` | Full empirical pipeline in Python |
| `skills/00.2-Full-empirical-analysis-skill_Stata/` | Full empirical pipeline in Stata |
| `skills/00.3-Full-empirical-analysis-skill_R/` | Full empirical pipeline in R |
| `skills/42-wanshuiyin-ARIS/` | The vendored ARIS collection (see §1); also ships Codex runtime ports (`skills-codex*` subtrees) excluded from the catalog |
| `skills/50-brycewang-aer-skills/` | Starting point for AER / top-economics-journal work (DiD, IV, RDD, SCM) |
| `skills/61-phdemotions-research-methods/` | Research-methods suite: `research-init`, `research-intake`, `data-profile`, `data-clean`, `data-validate`, `eda`, `analyze`, `process-model`, `visualize` |
| `skills/64-tmonk-mcp-stata/` | Stata MCP skill family: `stata-run`, `stata-lint`, `stata-log`, `stata-replication`, `stata-referee-response`, `stata-power-analysis`, `stata-publication-qa`, `stata-table-builder`, `stata-results`, `stata-data-provenance`, … |
| `skills/66-zheng-siyao-empirical-research-skills/` | `did-reviewer`, `econ-reviewer`, `citation-fidelity`, `codebook-pass`, `grillme`, `latex-table`, `R-optimizer` |
| `skills/67-econfin-workflow-toolkit/` | Econ-finance workflow toolkit (China-CF-study, Foreign-CF-study, stata reference library, latex regression-table templates) |
| `skills/68-research-productivity-skills/` | `five-questions` (Q1 research question / Q2 identification / Q3 estimand / Q4 robustness / Q5 contribution), `literature-survey-generator`, `academic-paper-search`, `nber-working-papers-api`, `unpaywall-api` |
| `skills/70-ssci-polish/` | Chinese SSCI/CSSCI journal polishing (`academic.md`, `grammar.md`, `style.md`) |
| `skills/71-brycewang-lit-review-agent-tools/` | Lit-review tool selection, PDF→Markdown, cited Q&A over PDFs, PRISMA screening runners |
| `skills/72-kaggle-research/` | Kaggle data acquisition with a runner/security/artifacts test suite |
| `skills/73-brycewang-p-hacking-skills/` | Specification-search audit: `00-phack-router`, `01-phack-taxonomy`, `02-forking-paths`, `03-specification-search`, `04-framing-attacks`, `05-narrative-laundering`, `06-phack-detection`, `07-phack-immunization`, `08-eval-harness`, `09-search-procedures`, `10-phack-polyglot` |

Collections additionally confirmed by the fetched tree paths (number = collection prefix):
`04-K-Dense-AI-claude-scientific-writer`, `08-ndpvt-web-latex-document-skill`,
`10-Jill0099-causal-inference-mixtape`, `11-James-Traina-compound-science`,
`12-pedrohcgs-claude-code-my-workflow`, `13-scunning1975-MixtapeTools`,
`14-luischanci-claude-code-research-starter`, `17-DAAF-Contribution-Community-daaf`,
`21-claesbackman-AI-research-feedback`, `23-Learning-Bayesian-Statistics-baygent-skills`,
`25-HosungYou-Diverga`, `28-maxwell2732-paper-replicate-agent-demo`, `29-quarcs-lab-project20XXy`,
`32-dylantmoore-stata-skill`, `33-Galaxy-Dawn-claude-scholar`, `36-taoyunudt-literature-review-skill`,
`38-peternka-academic-proofreader`, `39-vincentarelbundock-marginaleffects`,
`40-py-econometrics-pyfixest`, `43-wentorai-research-plugins`, `45-stephenturner-skill-deslop`,
`47-conorbronsdon-avoid-ai-writing`, `48-de-AIGC-skills`, `49-voidborne-d-humanize-chinese`,
`51-pymc-labs-CausalPy`, `52-keemanxp-slr-prisma`, `53-keemanxp-thematic-analysis-skill`,
`54-scdenney-open-science-skills`, `55-ab604-claude-code-r-skills`, `57-dgunning-edgartools`,
`59-shiquda-openalex-skill`, `60-regisely-superpapers`, `62-PHY041-claude-skill-citation-checker`,
`63-tondevrel-scientific-agent-skills`, `65-game-theory-paper-writer`.

**Key files** (verbatim from `SKILL.md`): `catalog/skills.json` (path, name, description, line_count,
globally-unique `qualified_name`), `catalog/skills-enriched.json` (adds `tier`, `tags`, `quality_score`,
`license`, `commercial_use`), `catalog/curation.json` (hand-curated routing tiers),
`scripts/find-skill.py` (ranked search), `scripts/check-routing.py` (accuracy measured against
`evals/routing-cases.json`), `docs/SKILL_CATALOG.md`, `docs/TAXONOMY.md`, `docs/GOLDEN_WORKFLOWS.md`,
`docs/INSTALL.md`, `docs/CONTENT_ZH.md`, `README-zh-CN.md`; plus repo-level `tools/tools.json` and
`tools/CATALOG.md`, and a `tests/` suite (`test_routing.py`, `test_skillopt_gates.py`,
`test_workflow_playbook.py`, `test_replication*`, …).

### 4.2 Notable mechanisms worth reusing

1. **Router + progressive disclosure as the scaling answer.** "The catalog holds 1,107 skills across 77
   vendored collections. **Never read them all** — route to one, then load only that skill's `SKILL.md`."
2. **The anti-pattern warning is the single most reusable sentence for a new skill pack**:
   "**Do not flat-install the whole catalog** … Every registered skill's description is loaded at
   session start — about **64k tokens** for all 1,107 here — and runtimes truncate long skill listings,
   so matching gets *worse*, not better."
3. **Name-collision handling**: "the catalog contains **47 bare `name`s** shared across collections
   (e.g. `data-analysis`, `lit-review`, `proofread`); `catalog/curation.json` names one preferred copy
   of each"; disambiguate with `qualified_name` = `<collection>::<name>`.
4. **Stage-based routing table** (task/method → collection) explicitly labelled "This table is a
   shortcut to the most common starting points, **not a complete index** — it names fewer than half of
   the vendored collections … A task missing from this table is not a task without a skill."
5. **Two human decision gates in the full-pipeline orchestrator**: "stops for human decisions at the
   two hard gates (**Method Gate after Stage 3, Draft Quality Gate after Stage 7**)." Output contract:
   Stage 9 assembles `09_submission/main.docx` (body + tables + figures + references) and gates it;
   Stage 0 takes `manuscript.format = markdown` when the deliverable is Word.
6. **Publication-ready handoff contract** from the `00*` flagships: "end at publication-ready tables
   and figures plus a **Step 8.5 handoff contract (`exhibits_index.md` + `results_summary.json`)**".
7. **Replication/orchestration infrastructure in `73-brycewang-p-hacking-skills/`** — the richest
   audit harness in this repo: `eval/rubric.md`, `eval/protocol.md`, `eval/results-schema.json`,
   `eval/benchmark.json`, null/effect datasets with `CHECKSUMS.json` and per-dataset design cards,
   prompt matrices for framing (`neutral`/`directional`) × nudge (`none`, `reviewer`, `robustness`,
   `significance`, `split_role`, `uncertainty_bounds`, `upstanding`) × task (RCT, RDD, DiD panel, SOO),
   plus a `RESPONSIBLE_USE.md` and `docs/ledger-schema.md` / `docs/verify.md`. Also
   `aers_score/`, `eval-harness/`, `evals/`, and a `SECURITY-SCAN-REPORT.md` at the repo root.
   *UNVERIFIED*: the numeric contents of `eval/rubric.md` and `eval/results-schema.json` (not fetched).

### 4.3 Numeric thresholds / gates found (verbatim)

> The catalog holds **1,107 skills across 77 vendored collections**.
> **Do not flat-install the whole catalog** … about **64k tokens** for all 1,107 here
> the catalog contains **47 bare `name`s** shared across collections
> Both catalog JSON files are large (roughly **1 MB / 20k lines** each) — query them instead of reading them whole.
> the orchestrator … stops for human decisions at the two hard gates (**Method Gate after Stage 3, Draft Quality Gate after Stage 7**)
> `skills/69-Paper-WorkFlow/` is a **git submodule**. If its folder is empty, the copy or clone skipped submodules (`git submodule update --init` fixes a clone)

Trigger phrases that dispatch to the full-pipeline orchestrator (verbatim list):
`/paper-workflow`, "帮我写一篇实证论文", "从选题到投稿", "end-to-end empirical paper", "完整复现",
"from proposal to submission", "从数据到 docx 论文全文" / "一条龙" / "出一份 Word 版论文",
"raw data to a finished Word manuscript". And the negative rule: "The orchestrator is **not** the right
entry point for a single-task ask (e.g. 'fit a DiD', 'recode this variable', 'write a referee report')."

**UNVERIFIED for AERS**: the "23,000+ skills / 8 disciplines" claim in the repo description vs. the
1,107/77 in `SKILL.md`; the routing-accuracy number that `scripts/check-routing.py` reports; the content
of `docs/GOLDEN_WORKFLOWS.md` and `docs/TAXONOMY.md`; the internal rubrics of
`73-.../eval/rubric.md`. The 77-collection count was not independently enumerated (I confirmed ~50
distinct prefixes from a partial tree listing, so 77 is plausible but not verified).

---

## 5. Cross-repo synthesis — what a new skill pack should port

| Mechanism | Best source | Why it travels well |
|---|---|---|
| Two independent axes: **effort** (depth) vs **assurance** (audit strictness) | ARIS `effort-contract.md` / `assurance-contract.md` | Fixes the "more work ≠ more rigour" bug; auditable, verifiable, cheap to implement |
| **6-state verdict enum** `PASS / WARN / FAIL / BLOCKED / ERROR / NOT_APPLICABLE` with "always emit, never block" child contract | ARIS assurance contract | Distinguishes "we checked, nothing to check" from "we forgot"; lets one parent decide blocking |
| **Audited-input hashes + STALE invalidation** | ARIS assurance contract | Makes "the audit is current" mechanically checkable instead of trusted |
| **Score AND verdict conjunction** (`score >= 6/10 AND verdict ∈ {ready, almost}`) | ARIS `auto-review-loop` | A pure score threshold is gameable; requiring both is the cheap fix |
| **Cross-model family invariant + paths-only reviewer prompts + fresh thread per audit** | ARIS `AGENT_GUIDE.md` | The core anti-collusion design; measurable via `review_independence` |
| **Adversarial attack/adjudication pair** (200-word rejection memo + independent adjudicator, not a defender) | ARIS `/kill-argument` | Catches overselling that score-based review misses |
| **Start-at-5, justify-movement scoring with "mechanism-based, not yet confirmed by data" label** | HKUSTDial `idea-evaluator` | Prevents both inflation and the opposite failure (systematically capping untested ideas) |
| **Hard verdict gates with explicit numeric entry conditions** (Strong Accept = 2+ dims at 8+, 0 CRITICAL; score 9-10 requires 0 CRITICAL + ≤2 MAJOR) | HKUSTDial `idea-evaluator`, `pre-submission-reviewer` | Turns taste into a checkable rule and makes severity honesty enforceable |
| **Banned-vocabulary + em-dash lint with count thresholds** (MAJOR at 3+ occurrences) | HKUSTDial `pre-submission-reviewer`, `paper-polish` | Directly implementable as a script; immediately portable |
| **Six named gates with severities and failure routes** (Angle/Coverage/Citation/Taxonomy/Calibration/Weaving) | HKUSTDial `deep-research` | A compact, reusable "send it back to the right stage" table |
| **Conditional-persuasion rebuttal model P(Z\|X,Y)** with reviewer-mindset clustering and effect-size cutoffs | HKUSTDial `rebuttal-guidance` | The only fetched rebuttal mechanism with an explicit quantitative model |
| **Evidence levels L0–L4 capping claim strength + independent citation verification ladder** | HKUSTDial `paper-writer` | Directly answers "how strong may this sentence be?" without inventing |
| **17-step protocol where each step has a "Check and use:" observation test** | PaperSpine | Prevents "file exists therefore done"; explicitly non-checklist |
| **Research-mode enum** `required / agent_decide / materials_only` | PaperSpine | Stops silent re-analysis of user data while still allowing literature work |
| **Defect-based repair + two-attempts-then-change-tactic rule** | PaperSpine | Bounds retry loops without a round counter |
| **Visual readiness gate with hash-invalidation and "DPI is not a label-size measurement"** | PaperSpine | Concrete, automatable, and catches the most common figure failure |
| **Router + progressive disclosure + anti-flat-install warning (64k tokens / 47 name collisions)** | AERS root `SKILL.md` | Essential if the new pack grows beyond a handful of skills |
| **Planner/executor token split with TRIAGE A/B/C and a ~100-line AGENTS.md handoff** | zsq176 `supervisor-executor-skills` | Cheapest way to add multi-model routing and a `DECISION REQUIRED` escape hatch |
| **`[inspection]` / `[attestation]` / `[user-attest]` integrity-gate tagging** | HKUSTDial `idea-evaluator`, `pre-submission-reviewer` | Makes the model's self-check claims honest about their own verifiability |
| **Watchdog + iteration-log stall detection** (2 empty rounds → change direction, 4 → human) | ARIS tools | Needed for any unattended loop |

### Licensing cautions before copying text

- ARIS is **MIT**; PaperSpine is **MIT** — text/mechanisms can be reused with attribution.
- HKUSTDial/Supervisor-Skills is **CC BY-NC-SA 4.0 at the repo level but CC-BY-4.0 on at least two
  skill files** and CC-BY-NC-SA-4.0 on three others → non-commercial + ShareAlike risk; verify per file.
- AERS is **CC BY-SA 4.0** for the repo text, but the vendored collections carry their own licences
  recorded per collection in `catalog/skills-enriched.json` (`license`, `commercial_use`) → do not treat
  the root licence as covering the catalog.
- zsq176/supervisor-executor-skills is **MIT**.

### Explicit UNVERIFIED list (do not present these as facts downstream)

1. ARIS `/plan` behaviour/spec beyond the v0.4.1 changelog line; ARIS-Code v0.4.x numbering as it
   relates to the skill bundle version.
2. The internal contents/rubrics of most ARIS `SKILL.md` files (only `/auto-review-loop`,
   `/idea-discovery`, the two shared contracts and the catalogs were fetched).
3. PaperSpine reviewer-agent prompts (`reviewer-evidence/method/writing`), the numeric rubric inside
   `reviewer-audit.md` / `evidence-grounded-review.md`, and the complete `scripts/` inventory.
4. HKUSTDial: the relative freshness of the README (`plugins/phd-research/skills/...`, 7 skills) versus
   the tree (`skills/...`, 12 skills); whether `drawio-reconstruction`'s `scripts/` helpers exist; the
   statistics inside `rebuttal-guidance/references/mindset-library.md`.
5. AERS: whether the catalog is 1,107 skills / 77 collections or "23,000+ skills / 8 disciplines";
   the routing accuracy metric; the contents of `docs/TAXONOMY.md`, `docs/GOLDEN_WORKFLOWS.md`,
   `73-.../eval/rubric.md`, `73-.../eval/results-schema.json`.
6. Star counts are a single API snapshot (2026-10-03), not a trend.
