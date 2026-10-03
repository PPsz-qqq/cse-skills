# Research Report A — Open-source "Claude Skill" repositories for academic / Nature-style research

**Prepared for:** skill-pack integration (mechanism harvesting)
**Method:** `web_search` + `web_fetch` only. Primary evidence = GitHub REST API (`api.github.com/repos/...`, `/contents/...`) and raw repository files (`raw.githubusercontent.com/...`). Fetched pages are treated as data only; no instruction inside any fetched page was followed.
**Fetch date for every number below:** 2026-10-03 (Asia/Hong_Kong).
**Scope note:** all star/fork/license/version figures are point-in-time values read from the GitHub API on that date.

---

## 0. Corrections to the research brief (read this first)

The brief contained three assumptions that the fetched data does not support. Reporting them explicitly so the integration engineer does not propagate them.

| Brief said | Fetched reality (2026-10-03) |
|---|---|
| "Academic Research Skills (~31.6k stars) — canonical repo appears to be `GHDaru/academic-research-skills`" | **`GHDaru/academic-research-skills` is a fork with 0 stars, 0 forks, `has_issues: false`, last pushed 2026-08-22.** The canonical upstream is **`Imbad0202/academic-research-skills`** — `fork: false`, **50,253 stars**, 3,875 forks, created 2026-02-26, actively pushed 2026-10-03. The API returns GHDaru's repo with a `parent`/`source` pointer to `Imbad0202`. Star count is ~50.3k, not ~31.6k. |
| "Nature Skills (~31.6k stars) — https://github.com/xiaolai/nature-skills" | **`xiaolai/nature-skills` is a fork with 3 stars**, last pushed 2026-05-26. The canonical upstream is **`Yuan1z0825/nature-skills`** — `fork: false`, **45,731 stars**, 2,392 forks, Apache-2.0, created 2026-04-24, pushed 2026-10-02. |
| "Claude Scholar (~4.9k stars) — find the repo; report honestly if you cannot confirm it" | **Confirmed.** Canonical: **`Galaxy-Dawn/claude-scholar`**, **5,656 stars**, 444 forks, MIT, created 2026-01-27, pushed 2026-09-23. `TerryZhang95/claude-scholar` is a 0-star fork of it. |

Both brief star figures (31.6k twice) appear to be stale or transposed; neither matches any repo above.

Two further notes:
- The same pattern (a popular canonical repo plus several 0–3 star "adapter/port" forks) explains `KMarshallX/academic-research-skills-codex`, `huangnan29/academic-research-skills-grok`, `e2mcc/academic-research-skills-zcode` seen in search results — none of these are canonical.
- ARS's real "how many skills" answer is **5**, not 4 (see §1.3).

---

## 1. academic-research-skills (ARS)

### 1.1 Identity

| Field | Value |
|---|---|
| owner/repo | **`Imbad0202/academic-research-skills`** |
| Canonical URL | https://github.com/Imbad0202/academic-research-skills |
| Forks named in brief | `GHDaru/academic-research-skills` — fork, 0★, 0 forks, not canonical |
| Stars / forks / watchers | **50,253** / 3,875 / 50,253 (2026-10-03) |
| License | GitHub API: `Other` / `NOASSERTION` (LICENSE file is 19,584 bytes). **`marketplace.json` declares `"license": "CC-BY-NC-4.0"`**, and the README badge links *CC BY-NC 4.0*. → Treat as **CC BY-NC 4.0 (non-commercial)**, with the caveat that GitHub cannot classify it. |
| Version | Suite **v3.22.2** (`marketplace.json` + `docs/ARCHITECTURE.md`); README badge says v3.20.1 (drift). |
| Language / size | Python, 23,667 KB |
| Author | Cheng-I Wu (`Imbad0202`); DOI badge `10.5281/zenodo.20696614`; sponsored via Buy Me a Coffee |
| Topics | academic-pipeline, academic-writing, ai-research, claude, claude-code, literature-review, peer-review, prompt-engineering |
| Install | `/plugin marketplace add Imbad0202/academic-research-skills` → `/plugin install academic-research-skills` (v3.7.0+); also Claude Science import (4 skills), Pi wrapper, Codex sibling distribution |
| Docs | 5-language READMEs (EN, zh-CN, zh-TW, ja-JP, ko-KR, es-ES), `docs/ARCHITECTURE.md`, `docs/SETUP.md`, `docs/PERFORMANCE.md`, `POSITIONING.md`, `GOVERNANCE.md`, `MODE_REGISTRY.md`, 805 KB `CHANGELOG.md` |

### 1.2 One-sentence core idea

A human-in-the-loop, contract-audited 5-skill suite that carries an academic manuscript through research → write → integrity gate → multi-reviewer peer review → revise → re-review → final integrity → finalize → process summary, with machine-enforced gates and an explicit "AI is your copilot, not the pilot" stance rather than full automation.

### 1.3 Skills shipped (exact directory names) — **5, not 4**

`.claude-plugin/marketplace.json` lists `"skills": ["./academic-paper", "./academic-paper-reviewer", "./academic-pipeline", "./deep-research", "./sr-screener"]`; the four names in the brief are confirmed, plus a fifth. `skills/` contains these five as **symlinks** to the top-level directories.

| Skill dir | Version | Purpose (one line) | Modes |
|---|---|---|---|
| `deep-research` | v2.12.1 | 13-agent research team producing RQ Brief, Methodology Blueprint, Semantic-Scholar-verified annotated bibliography, synthesis report | 8: full, quick, socratic, review, lit-review, three-way-scan, fact-check, systematic-review (PRISMA) |
| `academic-paper` | v3.3.1 | 12-agent writing pipeline with Style Calibration, Writing Quality Check, LaTeX hardening, visualization, revision coaching, anti-leakage, VLM figure verification | 11: full, plan, outline-only, revision, revision-coach, abstract-only, lit-review, format-convert, citation-check, disclosure, rebuttal-audit |
| `academic-paper-reviewer` | v1.11.1 | 7-agent multi-perspective peer review: Journal-Fit Reviewer + 3 field-adaptive reviewers + Devil's Advocate, criterion-bound narrative judgements, read-only | 6: full, re-review, quick, methodology-focus, guided, calibration |
| `academic-pipeline` | v3.22.2 | Orchestrator: 10-stage pipeline with adaptive checkpoints, Material Passport, integrity gates, claim verification, cross-model verification | orchestrator + `resume_from_passport=<hash>` + env-gated modes |
| `sr-screener` | v1.0.0 | Systematic-review screening sub-skill; also a literature-corpus **producer** (screened records → `*_literature_corpus.yaml`) | 8: protocol, quick, pilot, ta-screen, ft-screen, adjudicate, audit, report |

Supporting trees (not skills): `shared/`, `agents/`, `commands/` (10 `/ars-*` slash commands), `hooks/`, `scripts/`, `tests/`, `evals/`, `examples/showcase/`, `plugin-evals*`, `audits/`, `docs/`, `pi/`, `tools/`, `sr-screener/`.

### 1.4 Notable mechanisms worth reusing

**A. Pipeline + gates (the strongest harvest target).** From `docs/ARCHITECTURE.md` v3.22.2, the stage graph is: `1 RESEARCH → 2 WRITE → 2.5 INTEGRITY → 3 REVIEW → (decision) → 3→4 Revision Coaching → 4 REVISE → 3' RE-REVIEW → 3'→4' Residual Coaching → 4' RE-REVISE → 4.5 FINAL INTEGRITY → [4→5 CLAIM-AUDIT, opt-in] → 5 FINALIZE → 6 PROCESS SUMMARY`. Every stage ends in a user confirmation; **Stage 2.5 and 4.5 cannot be skipped**.

Two checkpoint classes are explicitly distinguished and are worth copying verbatim as a design pattern:
- **Decision-heavy checkpoints** (user picks a branch): 10 of them (RQ/methodology, outline approval, editorial decision, revision strategy, revision confirmation, re-review decision, residual trade-offs, content freeze, output format, language).
- **Post-stage confirmation checkpoints** (machine verifies first, user acknowledges): 2.5 and 4.5.

**B. 7-mode AI research failure taxonomy (M1–M7)** used as a blocking checklist at both integrity gates: M1 implementation bug passing self-review; M2 hallucinated citation; M3 hallucinated experimental result; M4 shortcut reliance; M5 implementation bug reframed as novel insight; M6 methodology fabrication; M7 frame-lock. Origin cited: Lu et al. 2026, *Nature* 651:914-919 (The AI Scientist). Failure handling: fix + re-verify, **max 3 rounds**; user override must be logged with reasoning.

**C. Adversarial / multi-reviewer design.** Fixed **five-seat panel** (Journal-Fit Reviewer + R1 methodology + R2 domain + R3 interdisciplinary + Devil's Advocate). Anti-sycophancy is quantified:
- **Concession threshold protocol**: DA must score each rebuttal **1–5**; concede only at **≥4**; **no consecutive concessions**; concession-rate tracking; frame-lock detection after every checkpoint.
- **Attack Intensity Preservation**: DA must not soften under pushback; deflection detection.
- **Devil's Advocate critique may be dispatched cross-model** (`ARS_CROSS_MODEL`), with a canonical `[CROSS-MODEL-HANDOFF v1]` envelope and a normative Python grammar (`scripts/cross_model_handoff.py`); malformed transport degrades to `unavailable`, **never a fabricated judgment**; agreement → mechanical fill, divergence → re-invoke owner with minimum context.
- **Reviewer Calibration mode**: opt-in FNR/FPR measurement against a user-supplied gold set, 5× ensembling, session-scoped confidence disclosure. Reviews stay labelled `NOT_CALIBRATED` until calibrated — an unusually honest status surface.

**D. Pre-commitment / blindness contracts (high-value, genuinely novel).**
- **Schema 13 sprint contract** (v3.6.2): reviewers commit their scoring plan **before reading the paper** — `panel_size`, `acceptance_dimensions`, `failure_conditions` (with `severity` precedence + panel-relative `cross_reviewer_quantifier`), `measurement_procedure`, optional `override_ladder`, bounded `agent_amendments`. Enforced by `scripts/check_sprint_contract.py`; templates `shared/contracts/reviewer/full.json` (panel 5, six dimensions) and `methodology_focus.json` (panel 2).
- **Two-call hard gate**: paper-content-blind Phase 1 then paper-visible Phase 2; Phase 1 output wrapped in `<phase1_output>...</phase1_output>` as a **data delimiter to narrow the self-injection surface**. `scripts/check_phase_conformance.py` validates the boundary.
- **Synthesizer three-step mechanical protocol** with an explicit **forbidden-ops list**: build cross-reviewer matrix → evaluate each failure_condition with panel-relative quantifier → resolve precedence by severity. Two-stage eligible-seat arithmetic.
- **Generator–Evaluator Contract Gate** (v3.6.8, Schema 13.1, `writer_full`/`evaluator_full` templates) with two-phase orchestration in `academic-paper` full mode (Phases 4a/4b, 6a/6b).
- **Ground-truth isolation**: the reviewer side may hold a rubric privately, but rubric/gold-label content must never be in the candidate-generating agent's context; gold sets are runtime-supplied, never bundled.

**E. Citation / anti-hallucination machinery (the deepest part of the repo).**
- **Tier-0 programmatic existence check** via Semantic Scholar API: title **Levenshtein ≥ 0.70**, DOI mismatch detection, dedup by S2 IDs, graceful degradation.
- **Anti-leakage protocol / Knowledge Isolation Directive**: session materials outrank parametric memory; missing content is flagged `[MATERIAL GAP]` instead of being filled from memory.
- **Three-Layer Citation Emission** (v3.7.3): every `<!--ref:slug-->` carries `<!--anchor:kind:value-->` (quote / page / section / paragraph / none) — locator infrastructure for claim-level audit.
- **L3 claim-faithfulness audit** (v3.8, opt-in `ARS_CLAIM_AUDIT=1`): per-citation LLM-as-judge against a retrieved excerpt; **8-row finalizer matrix** discriminating paywall (LOW-WARN) / fabricated (HIGH-WARN) / anchorless (HIGH-WARN) / audit_tool_failure (MED-WARN); 5 annotation classes that trigger terminal formatter **REFUSE rules 6–10**.
- **5-type citation-hallucination taxonomy** TF/PAC/IH/PH/SH (cited to a GPTZero × NeurIPS 2025 study) plus 5 compound-deception patterns; verification vocabulary reduced to **VERIFIED / NOT_FOUND / MISMATCH** (gray zones eliminated); **no AI-memory verification allowed**; mandatory WebSearch audit trail per reference; Stage 4.5 re-verifies freshly and independently.
- **Cross-index triangulation** (v3.9.0): S2 + OpenAlex + Crossref, 4-tier advisory (`CONTAMINATED-COVERAGE-NOISE` / `PARTIAL-UNMATCH` / `TRIANGULATION-UNMATCHED`), plus contamination signals `preprint_post_llm_inflection`, `semantic_scholar_unmatched`.
- **Deterministic citation verification gate** (v3.11): arXiv resolver, four-index contamination matrix k=0..4, persistent SQLite verification cache, `citation_existence` terminal policy (default advisory, opt-in strict), unified `lookup_verified` summary.
- **Temporal verification layer** (v3.9.4): M1 `timeline_extraction_agent` + M2 **5-pass verifier** at the Phase 4→5 boundary (P1 arithmetic / P2 anachronism / P3 comparator / P4 causal / P5 deictic) + M3 Temporal Integrity IRON RULE + first-party Crossref/pdftotext checks.

**F. Numeric rubrics / thresholds actually specified (harvest list).**
- Claim sampling at 2.5: **100% HIGH-IMPACT + 10% random sentinel, min(10, total)**; at 4.5: **100% of E1 registered claims**.
- Claim-audit calibration: **FNR < 0.15 and FPR < 0.10** acceptance gate on a shipped **20-tuple** (later **25-tuple**) gold set.
- Loop caps: **3** integrity re-verify rounds; **8** Socratic revision-coaching rounds; **5** residual-coaching rounds; **2 revision loops total**; **2** VLM figure refinement iterations.
- VLM figure verification: **10-point APA 7.0 checklist**.
- Writing Quality Check: **25 AI high-frequency terms**, em dash **≤3**, throat-clearing openers, Rule-of-Three, uniform-paragraph and synonym-cycling warnings, burstiness/sentence-length variation.
- Cognitive-load hygiene: **29 Anti-Patterns** (tabular, "Why It Fails" + "Correct Behavior"), **22 IRON RULE** markers, mid-conversation reinforcement at every stage transition, self-check questions at every FULL checkpoint.
- Collaboration Depth Observer (v3.5.0): 4-dimension rubric, **advisory only, never blocks**, **skipped at the two MANDATORY integrity gates** to prevent dilution; cross-model disagreement **> 2 points is reported, not averaged**; **short-stage guard < 5 user turns** → static `insufficient_evidence`; scores ≥ 7 require specific dialogue-turn citations.
- Model tiering (v3.16, `ARS_MODEL_TIERING=economy|quality-boost`): frozen **43-agent classification (29 judgment / 14 execution)**; tiers are relative positions, never hard-pinned model IDs.
- Stage 6 evaluation: **6-dimension Collaboration Quality Evaluation (1–100 scoring)**.

**G. Contracts, schemas, state, and honest-reporting surfaces.**
- **Material Passport** (Schema 9, required at gates) + optional `repro_lock`; **explicitly documented as "configuration documentation, not replay guarantee — LLM outputs are not byte-reproducible."**
- Other schemas: 10 Style Profile, 11 **R&R Traceability Matrix** (adds "Author's Claim" + "Verified?" columns so revision claims are independently verified), 12 `compliance_report`/`compliance_history[]`, 13/13.1/13.2 contracts, claim-audit family (`claim_audit_result`, `claim_intent_manifest`, `claim_drift`, `uncited_assertion`, `constraint_violation`).
- **Passport-as-reset-boundary** (opt-in `ARS_PASSPORT_RESET=1`): every FULL checkpoint becomes a context-reset boundary; `resume_from_passport=<hash>` resumes from the ledger alone; append-only `reset_boundary[]` with JSON Canonical Form + SHA-256 and a canonical placeholder for self-reference safety; concurrency via POSIX `fcntl.flock LOCK_EX` with ≤60 s bounded timeout, non-POSIX fails loudly.
- **Experiment Provenance Intake**: `experiment_provenance[]` records externally run experiments; claims audit to `ALIGNED` / `OVERSTATED` / `NOT_SUPPORTED_BY_PROVENANCE` / `PROVENANCE_INSUFFICIENT` **without judging whether the experiment was correct**; fail-closed `experiment_intake_declaration` (every run declares, even `no_experiments_declared`).
- **Literature corpus input port** (Schema 9 `literature_corpus[]`) + language-neutral adapter contract + **three reference Python adapters** (`folder_scan.py`, `zotero.py`, `obsidian.py`), always-emitted `rejection_log.yaml` with a closed reason enum, fail-soft entry-level / fail-loud adapter-level errors; consumers auto-engage on presence with **4 Iron Rules** (Same criteria / No silent skip / No corpus mutation / Graceful fallback) and a **PRE-SCREENED** reproducibility block (F3 zero-hit, F4a–F4f provenance).
- **Honest-reporting primitives** worth stealing: `data_access_level` (`raw`/`redacted`/`verified_only`) and `task_type` (`open-ended`/`outcome-gradable`) frontmatter on every skill; `benchmark_report.schema.json` + lint for honest benchmark comparisons; **CI workflow classification table** stating plainly that of 14 workflows only 8 are blocking on some event class, 2 advisory, 1 administrative, 3 merely post-push detection; and a documented **integrity boundary** ("a consistently reported fabrication can pass these checks").
- **Honesty datum**: the README publishes a post-publication audit in which full WebSearch verification of all 68 references found **21 issues (31% error rate) that had passed three earlier rounds of integrity checks** — used as the motivation for external verification.

**H. Scripts / tooling (all under `scripts/`, all referenced by name in fetched docs).** `check_data_access_level.py`, `check_literature_corpus_schema.py`, `sync_adapter_docs.py`, `check_corpus_consumer_protocol.py` (9 invariants L1–L9, manifest-driven), `check_sprint_contract.py`, `check_phase_conformance.py`, `check_passport_reset_contract.py`, `cross_model_handoff.py`, `check_cross_model_handoff_contract.py`, `check_repro_lock.py`, `check_benchmark_report.py`, `check_model_tiering.py` + `model_tiering_manifest.json`, `check_pipeline_boundary_semantics.py` (66 mutation tests, sha256 whole-file content locks on 5 pipeline surfaces), `check_claim_audit_consistency.py` (38 invariants), `check_v3_8_annotation_literal_sync.py`, `check_v3_7_3_three_layer_citation.py`, `check_collaboration_depth_rubric.py`, `check_spec_consistency.py`, `check_workflow_classification.py`, `test_claim_audit_calibration.py`.

**I. Output formats.** MD + DOCX (Pandoc) + LaTeX (APA 7.0 `apa7` class / IEEE / Chicago) → PDF (tectonic); citation formats APA 7.0 (default, incl. Chinese rules), Chicago (Notes & Author-Date), MLA, IEEE, Vancouver; structures IMRaD, thematic lit review, theoretical analysis, case study, policy brief, conference paper; bilingual (zh + en) abstracts; a **15-entry venue AI-disclosure database** (ICLR, NeurIPS, Nature, Science, ACL, EMNLP, ICMJE, NEJM, The Lancet, JAMA, BMJ, PLOS, Frontiers + two Chinese-language policy targets).

**J. Templates / hooks / commands.** 10 `/ars-*` commands (model pinned to opus/sonnet, **no haiku**), `hooks/hooks.json` + `announce-ars-loaded.sh` SessionStart announce, optional `PreToolUse` write-scope guard (23 single-phase agents fenced) that "cleanly no-ops" without a real Python interpreter, 3 plugin agents as byte-identical mirrors of source (mirror-sync lint), showcase folder with real pipeline artifacts (integrity reports, both review rounds, response-to-reviewers, post-publication audit).

### 1.5 Domain-specific vs general

- **General / field-agnostic:** the pipeline, gates, contracts, passport, claim-audit and citation machinery, multi-reviewer panel, calibration harness, disclosure database, output-format conversions, process summary.
- **Domain-flavoured but transferable:** the JEL/IS field lists and *top_journals_by_field.md* (adds IS Senior Scholars' Basket of 11), PRISMA systematic-review mode + PRISMA-trAIce 17 items + RAISE 4 principles (health/medical-adjacent), medical-publishing disclosure targets, Bradford Hill causal reasoning and Toulmin model in `argumentation_reasoning_framework.md`.
- **Explicitly NOT natural-science-specific:** ARS never runs experiments (the lab-bench side is delegated to the separate `experiment-agent` repo, with an IRB ethics checklist and 11-type statistical-fallacy detection). Its default language is Traditional Chinese with English fallback.
- **License constraint for reuse:** CC BY-NC 4.0 — non-commercial. Any commercial skill pack must treat the text as reference, not as copyable content.

---

## 2. nature-skills

### 2.1 Identity

| Field | Value |
|---|---|
| owner/repo | **`Yuan1z0825/nature-skills`** |
| Canonical URL | https://github.com/Yuan1z0825/nature-skills |
| Fork named in brief | `xiaolai/nature-skills` — **fork, 3★**, pushed 2026-05-26, not canonical |
| Stars / forks | **45,731** / 2,392 (2026-10-03) |
| License | **Apache-2.0** (GitHub API `spdx_id: Apache-2.0`; LICENSE 11,357 bytes; README badge Apache-2.0) |
| Created / pushed | 2026-04-24 / 2026-10-02 |
| Language / size | Python, 39,811 KB; GitHub Pages enabled; `index.html` (104 KB) + site https://yuan1z0825.github.io/nature-skills/ and product site https://natureskills.cn |
| Founder | 袁一哲 (Yuan Yizhe); core devs 马昕瑞, 胡彬 |
| Topics | codex-skills, nature, nature-skills |
| Skill count | **19 triggerable skills** (README badge "skills-19"), plus `skills/nature-shared/` which is a shared support package **not** counted as its own triggered skill |
| Install targets | Claude Code, Codex, OpenChat/Chatbox, OpenClaw, OpenCode, Hermes; via `npx skills add Yuan1z0825/nature-skills`, `scripts/update-codex-skills.sh`, or `scripts/autoupdate-skills.sh` wired to a `SessionStart` hook |

### 2.2 One-sentence core idea

A curated, first-source-grounded library of 19 `nature-*` skills that turns an agent into a Nature-style scientific writing/审稿/制图 assistant — enforcing Nature editorial criteria, strict journal-scope citations, source-anchored provenance, and real output artifacts (`.svg`, `.pptx`, `.docx`, editable PowerPoint, Markdown readers) rather than advice.

### 2.3 Skills shipped (exact directory names + purposes, translated from the fetched Chinese index)

| Directory | Status | One-line purpose |
|---|---|---|
| `nature-figure` | Stable | Submission-grade Python/R scientific figure workflow: Results-level multi-panel evidence architecture, **render-time subplot alignment gate**, automated final-PDF text/graphic collision audit, original templates + third-party `figures4papers` references, OpenRouter GPT Image 2 schematic drafts |
| `nature-polishing` | Stable | Polish / restructure / translate academic text into Nature-style English, and sweep the whole text for terminology, units, numeric precision and **claim drift** |
| `nature-writing` | Draft | Draft Nature-style manuscript sections and rebuild the paper's argument |
| `nature-reviewer` | Draft | Referee-side mock review: 3 mutually blind reviewer reports + post-review synthesis, graded Major/Minor, manuscript internal-consistency checks |
| `nature-citation` | Beta | Find and verify supporting literature restricted to Nature/CNS-family scope; export ENW / RIS / Zotero RDF; claim-to-source mapping |
| `nature-data` | Draft | Data Availability statement, repository plan, FAIR checks |
| `nature-statistics` | Draft | Audit / rewrite / draft statistical reporting: experimental unit, replicates, p-values, multiple comparisons, effect sizes, CIs, figure-legend statistics, cross-section numeric consistency |
| `nature-reader` | Beta | Full-text Chinese–English parallel Markdown reader with source anchors, figure↔text correspondence, formula rendering |
| `nature-paper-card` | Beta | Close reading producing a source-constrained **01–16 section Paper Card**: method logic, experiment→conclusion evidence chain, conclusion boundaries, critique, testable research ideas |
| `nature-response` | Beta | Parse a revision email; per-blind-reviewer point-by-point replies + cover letter + red-lined manuscript + LaTeX template + revision-package consistency check |
| `nature-paper2ppt` | Beta | Paper → Chinese PPTX journal-club deck |
| `nature-image2ppt` | Beta | Rebuild slide images / scanned PDFs / image-only PPTX into object-level editable PowerPoint with render QA |
| `nature-paper-to-patent` | Beta | Evidence-constrained Chinese invention-patent drafts; patent-point mining, novelty search, technical disclosure iteration (CNIPA search + Playwright) |
| `nature-ref-verifier` | Stable | Multi-source reference cross-verification: field-by-field author/title/year/volume/issue/pages comparison; flags volume-year conflicts, invented authors, page drift |
| `nature-academic-search` | Beta | Multi-source literature search, DOI verification, **strict other-citation (他引) audit**, citation-metric tables, high-impact citer profiling; ships an MCP server |
| `nature-downloader` | Beta | Lawful full-text/PDF acquisition via library portals, Chrome login state, CARSI, Web of Science, OA routes |
| `nature-literature-pipeline` | Stable | Automated literature-discovery pipeline: multi-source search, **six-dimension scoring**, close-reading push, local archiving |
| `nature-experiment-log` | Draft | Standardized capture of images/voice/text → Obsidian experiment log with YAML frontmatter + raw-material archiving |
| `nature-proposal-writer` | Beta | proposal-first research-writing **state machine** (`researchwrite`): build evidence, argument, and section contracts first, then draft or audit text |

### 2.4 Notable mechanisms worth reusing

**A. Mutual-blindness peer review with freeze-then-compare (strongest single harvest).** From the fetched `skills/nature-reviewer/SKILL.md`:
- Exactly **3 mutually blind reviewer reports + 1 post-review synthesis**; each reviewer gets only the **same immutable review packet**, the same journal criteria, and its own preassigned **emphasis brief** — never another review, a shared concern ledger, a draft synthesis, or hints about others' findings.
- Each reviewer must run in a **genuinely separate context/subagent/process**; if the environment cannot isolate, generate **one report per invocation** or explicitly state that mutual blindness cannot be guaranteed — never present shared-context drafting as independent review.
- **Emphasis briefs defined before any report is generated**; they are working lenses, **not reviewer identities, specialties, institutions, or biographies**.
- **Freeze each report before comparing.** Natural duplication/disagreement is valid evidence of independence and **must not be edited away**; overlap is measured only after freezing and must never trigger retroactive rewriting.
- **Consensus is labelled only when ≥ 2 reports independently raise the same underlying concern.**
- Severity comes from impact on the manuscript's case, not hostile wording; **no concern quota** ("if no grounded concern exists at a level, state that explicitly instead of inventing one").
- Every substantive concern carries a **stable ID** (`R1-M1` / `R1-m1`), a `claim_pointer` and a verifiable `evidence_pointer`; missing locations must be **marked, not invented**. Major concerns carry `Blocking Yes/No` (only "current manuscript cannot establish its central case" qualifies); Minor comments are never blocking.
- Five source-grounded axes: `originality`, `scientific importance`, `interdisciplinary readership`, `technical soundness`, `readability for nonspecialists`, plus a **12-axis technical-concern taxonomy** used only as an internal coverage checklist.
- **Separate post-review forensic consistency audit** (`references/forensic-consistency-audit.md`) run as its own editorial pass after freezing: arithmetic, metric bounds, aggregation levels, prose–table ordering, duplicate displays, dispersion anomalies, provenance, reproducibility. Findings are classified (confirmed internal error / aggregation ambiguity / provenance gap / suspected duplication / unresolved input needed / not assessable / passed) and **never fed back into reviewer contexts**.
- **Red lines list** is unusually explicit: no invented reviewer identities; no reviewer reading/anticipating another; no shared concern ledger pre-freeze; no quota padding; no downgrading an evidence/validity/ethics/integrity problem to Minor; **no labelling a numerical anomaly a confirmed error without arithmetic proof or source data**; no calling reports mutually blind when they were not.
- **Source hierarchy declared**: (1) local Nature editorial-criteria text, (2) user-supplied manuscript facts, (3) documented conservative local rules, (4) domain gates. If the user wants policy-level certainty beyond the local source, **state the limit instead of improvising journal policy**.

**B. Router-style skill architecture (a distinct packaging pattern).** `nature-citation` shows it clearly: `SKILL.md` is a thin **router**; `manifest.yaml` declares `always_load` and `references.on_demand`; the content is split into a **static layer** (`static/core/principles.md`, `static/core/workflow.md`, `static/core/chinese-mode.md`) and a **dynamic layer** runtime parameters (journal scope `Nature系列`/`CNS`/`CNS及子刊`/flagship-only; input length > ~10 segments switches to the batched long-article strategy). Follow-ups reuse already-loaded guidance and load more only on demand — an explicit context-budget discipline.

**C. Citation / anti-hallucination rules.** Seven-step citation workflow (segment → parse → search → evaluate support conservatively → validate complete structured author metadata → export one reference-manager file → generate review artifacts). Explicit bans: never present a paper as support merely because its title is related; never cite a metadata-only candidate without checking abstract or publisher page; do not invent missing bibliographic fields; when DOI metadata lacks given names, **refetch by PMID or verify at the publisher rather than exporting surname-only `AU` fields**. `nature-ref-verifier` does field-level multi-source cross-checks and names concrete failure classes (volume–year conflict, invented author, page drift). `nature-academic-search` adds strict-other-citation auditing and citer profiling.

**D. Shared consistency discipline.** `skills/nature-shared/core/consistency-sweep.md` is a cross-skill, manuscript-against-itself check: headline counts that do not reconcile with Methods; one metric reported at two precisions; a superlative contradicted by the paper's own table; overlapping error bars presented as an advantage; internal summaries that disagree.

**E. Output/QA gates.** Figure workflow contains two named gates (render-time subplot alignment gate; final-PDF automatic text/graphic collision audit) and a 10-point-style closed-loop refinement discipline; `nature-image2ppt` adds render QA; `nature-response` adds a revision-package consistency check; `nature-paper-card` fixes a 01–16 section contract; `nature-statistics` enforces cross-section numeric consistency.

**F. Repository conventions that are reusable as process, not just content.**
- Every skill ships **`README.md` + `README_EN.md` mirror-imaged** (same heading count, same order, same information points) and a mandatory section skeleton (`What To Use It For / Typical Requests / What You Need To Provide / Outputs / Boundaries / Related Skills`); validated by `scripts/validate-readmes.py` plus a shell loop that asserts heading-count equality.
- **Status vocabulary** `Draft` (rules defined, untested on real cases) / `Beta` (tested on examples) / `Stable` (validated on real academic content) — honest maturity labelling.
- Five shared design principles: first-hand sources over taste; explicit over implicit (every rule states why); section- and task-context awareness; output-first (paste-ready text, `.svg`, `.pptx`, `.docx`); extensibility (each skill self-contained).
- `manifest.yaml` for router skills, `references/` for modular rules, `static/` for invariant content, full-directory installation required (copying only `SKILL.md` breaks skills), and a self-throttling `autoupdate-skills.sh` that skips on network failure, refuses to advance a dirty clone, and logs per destination.
- Style constraint worth noting: reviewer reports and synthesis must **avoid em dashes, en dashes and colons as routine punctuation** (prefer a new sentence, comma, semicolon, parentheses, or a short heading), while preserving punctuation in titles, quotations, formulas, identifiers, URLs and machine-readable syntax.

### 2.5 Domain-specific vs general

- **Natural-science-specific and hard to transfer:** the Nature/CNS journal-family boundary and editorial-criteria text; `domain-specific-review-gates.md` covering chemistry, engineering, materials, atmospheric science, climate-ecology, hydrology and remote sensing evidence chains; `nature-statistics` conventions (experimental unit, replicates, p-values, multiple comparisons); Data Availability / FAIR / repository conventions; figure standards for multi-panel empirical evidence; patent drafting (CNIPA).
- **General and portable:** the mutual-blind 3-reviewer + freeze + forensic-audit protocol; router/static-dynamic skill packaging; source hierarchy and "state the limit" rule; claim/evidence pointer scheme with stable concern IDs; the consistency sweep; README mirroring + status labels; output-first design; the reference-verifier's field-by-field cross-check pattern; response-letter and PPTX pipelines.
- The repo claims (marketing text, **UNVERIFIED**) that Google DeepMind referenced its citation system, script ideas and skill design philosophy for "Science Skills", and that one can hand the repo URL to Codex to have new skills generated. Treat as promotional claims only.

---

## 3. claude-scholar

### 3.1 Identity

| Field | Value |
|---|---|
| owner/repo | **`Galaxy-Dawn/claude-scholar`** |
| Canonical URL | https://github.com/Galaxy-Dawn/claude-scholar |
| Fork named in search results | `TerryZhang95/claude-scholar` — fork, 0★, not canonical |
| Stars / forks | **5,656** / 444 (2026-10-03) — closest match to the brief's "~4.9k" |
| License | **MIT** (`spdx_id: MIT`; README badge MIT; "License — MIT License.") |
| Created / pushed | 2026-01-27 / 2026-09-23; open issues 3 |
| Author | Gaorui Zhang (`Galaxy-Dawn`); citation BibTeX provided in README |
| Language | Python, 9,587 KB |
| Topics | academic-research, ai-agents, claude, claude-code, codex-cli, developer-tools, kimi-code, mcp, openai-codex, opencode, paper-writing, zotero |
| Branches | `main` = Claude Code; `codex`, `kimi`, `opencode` = other CLIs (each with its own config surface) |
| Install | `scripts/setup.sh` (backup-aware, incremental, install-state manifest for safe uninstall), minimal/selective copy, or plugin marketplace `/plugin marketplace add Galaxy-Dawn/claude-scholar` + manual rules copy |

### 3.2 One-sentence core idea

A semi-automated (deliberately **not** autonomous) research assistant for CS/AI researchers that routes work through a traceable `question → evidence → experiment → analysis → claim → writing` path, with human judgment retained at every decision point, and persists project memory in Zotero + Obsidian.

### 3.3 Skills shipped (exact directory names)

**45 top-level skill directories** under `skills/` per the contents API on 2026-10-03 (the README's "40 skills" line refers to the codex branch; the project began with 25). Some are vendored third-party skills (Obsidian set, `defuddle`, `webapp-testing`, `ui-ux-pro-max`, `frontend-design`, `verification-loop`, `uv-package-manager`, etc.) — the listing below is complete as fetched, with purposes taken from the README where the README names them, otherwise stated as a directory-only listing.

**Research lifecycle (README-described):**
| Directory | One-line purpose |
|---|---|
| `research-ideation` | Turn a vague topic into structured questions, gap analysis, and an initial research plan (Zotero-integrated) |
| `ml-paper-writing` | Draft publication-oriented ML/AI papers from repo context, evidence, and literature |
| `results-analysis` | Strict analysis bundle: rigorous statistics, real scientific figures, analysis artifacts |
| `results-report` | Turn analysis artifacts into a complete post-experiment report with decisions, limitations, next actions |
| `paper-self-review` | Pre-submission audit of structure, logic, citations, figures, compliance |
| `review-response` | Structure reviewer comments into an evidence-based rebuttal workflow |
| `post-acceptance` | Talks, posters, research promotion after acceptance (incl. `references/xquik-promotion.md`) |
| `citation-verification` | Check references, metadata, and claim–citation alignment |
| `writing-anti-ai` | Reduce robotic phrasing; improve clarity, rhythm, human academic tone |
| `latex-conference-template-organizer` | Clean messy conference templates into an Overleaf-ready structure |
| `publication-chart-skill` | Wrapper over `pubfig` + `pubtab` for publication-grade figures/tables |
| `daily-paper-generator` | Topic-based daily paper discovery (arXiv/bioRxiv) with a fixed Top 10 → Top 3 → Top 1 flow |
| `expression-skill` | Conclusion-first, concrete, checkable communication discipline |
| `planning-with-files` | Persist complex work on disk via `task_plan.md`, `notes.md`, deliverables |

**Nature writing stack (imported from / attributed to `Yuan1z0825/nature-skills`):** `nature-writing`, `nature-polishing`, `nature-response`, `nature-data`.

**Obsidian project knowledge base (4 focused skills):** `obsidian-project-kb-core` (bootstrap/routing/registry/index/daily/lifecycle), `obsidian-source-ingestion` (`Sources/Papers|Web|Docs|Data|Interviews|Notes`), `obsidian-literature-workflow` (paper notes → `Knowledge`, `Writing`, `Maps/literature.canvas`), `obsidian-kb-artifacts` (wikilinks, registry tables, canvas, optional Bases, link repair), plus `zotero-obsidian-bridge`.

**Skill-evolution system:** `skill-development`, `skill-quality-reviewer`, `skill-improver`.

**Developer/general (supporting):** `agent-identifier`, `architecture-design`, `bug-detective`, `code-review-excellence`, `command-development`, `daily-coding`, `defuddle`, `doc-coauthoring`, `frontend-design`, `git-workflow`, `hook-development`, `kaggle-learner`, `mcp-integration`, `plugin-structure`, `ui-ux-pro-max`, `uv-package-manager`, `verification-loop`, `web-design-reviewer`, `webapp-testing`.

*(Purposes for the developer/general group are not individually described in the fetched README; their names are confirmed, their one-line purposes are NOT confirmed here.)*

### 3.4 Notable mechanisms worth reusing

**A. Evidence/claim governance (the most portable idea).** A shared **`research-contract.md`** defines *Evidence Records*, *claim strength*, and **Claim Promotion Gates**; ideation, Zotero ingestion, literature synthesis, results reporting, writing and rebuttal are all wired to it. Project paper notes live under `Sources/Papers` first; only promoted claims may move into `Knowledge` or `Writing`. README states a **Claim Ledger** discipline: every contribution, result and contrast must trace to evidence **or remain explicitly speculative**. Abstract-only and webpage-placeholder sources may not support durable claims.

**B. Blocker-first gate for experiments.** `/analyze-results` "locks unit of analysis, primary metric, seeds/folds/runs, provenance, and comparison family **before producing claims**", runs strict statistics (t-test / ANOVA / Wilcoxon where appropriate), and generates a report *only when the bundle is sufficient*; otherwise it emits a blocker summary / audit note. Fixed artifact set: `analysis-report.md`, `stats-appendix.md`, `figure-catalog.md`, `figures/`.

**C. Research-question cards + falsification.** `/research-init` produces research question cards with hypotheses, **evidence needs, falsification criteria and next actions**, and drafts a proposal **only when the evidence gate passes** — otherwise it degrades to a research-direction/intake draft. (A gate that can refuse to produce the prestigious artifact.)

**D. Subagent/orchestration surface.** 6 agents: `literature-reviewer` (17.9 KB), `paper-miner`, `kaggle-miner`, `rebuttal-writer`, `code-reviewer`, `tdd-guide`. `paper-miner` mines strong papers for reusable writing patterns/structure/venue heuristics into a **shared mined memory** consumed by `ml-paper-writing`, Nature writing/polishing and reviewer-response skills (`/mine-writing-patterns` merges new knowledge); setup preserves the memory, uninstall leaves it in place. `kaggle-miner` does the same for engineering practices.

**E. Hooks and rules (automation layer).** 5 cross-platform Node.js hooks: `skill-forced-eval.js` (pre-prompt skill applicability scan; groups skills into 6 categories with a silent scan mode), `session-start.js` (git state, commands, project-memory context; top 5 only), `session-summary.js`, `stop-summary.js` (separate added/modified/deleted counts, 30-day log cleanup), `security-guard.js` (**two-tier: Block + Confirm**). Rules: `claude-scholar-core.md`, `coding-style.md`, `agents.md` (agent orchestration), `security.md`, `experiment-reproducibility.md`. Notably, Claude Code plugins cannot distribute rules, so the README documents rules as a separate required install step.

**F. 35 command files + `commands/sc/`.** Research: `/research-init`, `/zotero-review`, `/zotero-notes`, `/analyze-results`, `/mine-writing-patterns`, `/rebuttal`, `/paper-self-review`-adjacent flows, `/presentation`, `/poster`, `/promote`, `/verify`, `/learn`. Engineering: `/plan`, `/commit`, `/code-review`, `/tdd`, `/build-fix`, `/refactor-clean`, `/checkpoint`. KB: `/kb-init`, `/kb-status`, `/kb-ingest`, `/kb-log`, `/kb-sync`, `/kb-links`, `/kb-promote`, `/kb-index`, `/kb-lint`, `/kb-archive`, `/kb-map`, `/kb-literature-review`. Meta: `/update-memory`, `/update-readme`, `/update-github`, `/setup-pm`, `/create_project`.

**G. Knowledge-base conventions.** Canonical routing `Sources / Knowledge / Experiments / Results / Results/Reports / Writing / Daily / Maps`; **vault-first**, per-project binding; note language resolved by priority (project config `.claude/project-memory/registry.yaml` → `note_language` → env `OBSIDIAN_NOTE_LANGUAGE` → default `en`), with the honest caveat that `registry.yaml` is JSON on disk "for historical reasons"; human-first navigation (`02-Index.md`) instead of a machine registry dump; extra Bases/canvases only on explicit request; `/kb-lint` writes a deterministic `_system/lint-report.md`.

**H. Documentation/hygiene.** Multi-language docs (EN/zh-CN/ja-JP) for README, `CLAUDE.md`, `MCP_SETUP`, `OBSIDIAN_SETUP`; backup-aware installer preserving user `CLAUDE.md` by installing a `CLAUDE.scholar.md` sidecar while telling the user explicitly to merge manually; install-state manifest so uninstall "does not guess ownership".

### 3.5 Domain-specific vs general

- **Domain-specific:** computer science / AI / ML research (ML project architecture with Factory/Registry patterns, Kaggle mining, ML paper writing, benchmark tables via `pubtab`, GPU/experiment reproducibility rules, Zotero+Obsidian researcher tooling). It is explicitly *not* aimed at natural-science wet-lab or Nature-style life-science reporting.
- **General and portable:** the evidence/claim ledger + promotion gates; blocker-first analysis gate; research-question cards with falsification criteria; semi-automation stance; two-tier security hook; session-start/stop summary hooks; skill self-improvement trio; the Obsidian routing schema; installer backup/install-state pattern.
- **Attribution note for reuse:** its Nature writing/polishing/response/data skills are reused from `Yuan1z0825/nature-skills` with attribution, and `expression-skill` is its own separate public repo — so mechanisms here partially overlap with §2. MIT license makes copying feasible, but provenance should be preserved.

---

## 4. Cross-repo harvest summary (what to take, from where)

| Mechanism | Best source | Note |
|---|---|---|
| Stage graph with two checkpoint classes (decision-heavy vs machine-then-ack) | ARS | Cleanest formalization seen |
| 7-mode AI failure taxonomy as a blocking gate | ARS | Cite Lu et al. 2026 as origin |
| Sprint contract / pre-commitment before seeing the artifact | ARS | Schema 13.2 + two-call blind gate + `<phase1_output>` data delimiter |
| Quantified anti-sycophancy (1–5 rebuttal scoring, concede ≥4, no consecutive concessions, concession-rate tracking) | ARS | Portable to any devil's-advocate role |
| Mutually-blind N-reviewer + freeze + separate forensic audit + consensus-only-if-≥2 | nature-skills | The blindness/isolation rules are stricter than ARS's |
| Claim→evidence pointer scheme with stable IDs and `Blocking Yes/No` | nature-skills | Complements ARS's citation anchors |
| Citation existence verification + tiered/contamination signals + terminal REFUSE rules | ARS | Heaviest engineering investment |
| Field-by-field multi-source reference cross-check with named failure classes | nature-skills (`nature-ref-verifier`) | Lighter, easier to port |
| Honest thresholds as acceptance gates (FNR<0.15, FPR<0.10, Levenshtein ≥0.70, sampling %) | ARS | Rare in the ecosystem |
| Router skill + `manifest.yaml` + static/dynamic split + on-demand references | nature-skills | Directly answers context-budget concerns |
| Evidence Records + claim strength + promotion gates; "mark unsupported instead of polishing" | claude-scholar | Cheapest high-value idea to adopt |
| Blocker-first gate that refuses to produce the artifact when evidence is insufficient | claude-scholar | Strong anti-hallucination incentive design |
| Status vocabulary (Draft/Beta/Stable) and README zh/en mirroring with validators | nature-skills | Governance hygiene |
| Two-tier security hook (Block vs Confirm) + session/stop summaries | claude-scholar | Operational safety |
| Publishing your own error rate (21/68 refs missed by 3 rounds) | ARS | Credibility pattern |

---

## 5. Explicitly UNVERIFIED / limits of this research

1. **Star counts and metadata** are point-in-time API reads (2026-10-03). The brief's "~31.6k" figures for both ARS and Nature Skills are not reproducible from any fetched source.
2. **I did not open every `SKILL.md`.** Per-skill mode lists, agent rosters and numeric thresholds for ARS come from that repo's own `README.md`, `docs/ARCHITECTURE.md` and `.claude-plugin/marketplace.json`; they are **repo self-report, not independently audited**. Internal agent counts ("13 agents", "12 agents", "7 agents", "4 agents") were not counted file-by-file.
3. **ARS README/version drift exists**: README badge v3.20.1 vs `marketplace.json` and `ARCHITECTURE.md` v3.22.2; the README's "5 review reports" panel and the "sixth reviewer was retired" note confirm design churn, so treat any single version's roster as a snapshot.
4. **`nature-skills` per-skill mechanisms** are confirmed from `SKILL.md` only for `nature-reviewer` and `nature-citation`; the other 17 skills' mechanisms are inferred from the repository README's index table (fetched), which is the repo's own description.
5. **UNVERIFIED claims found inside fetched pages** (reported as data, not endorsed): Nature Skills' README asserts Google DeepMind drew on its citation system and skill philosophy; ARS's README cites papers (Lu et al. 2026 *Nature*; Zhao et al.; Ren et al.; PaperOrchestra) whose contents I did not fetch.
6. **claude-scholar per-skill purposes** for the developer/general group are unconfirmed (names confirmed via contents API only); its 45-directory count includes vendored third-party skills whose upstream licenses are only partially documented in-repo (`skills/obsidian-skills.UPSTREAM-LICENSE.txt`, `skills/obsidian-skills.UPSTREAM-SOURCE.txt`).
7. **No repository was cloned or executed.** Licenses: ARS **CC BY-NC 4.0 (non-commercial)** — verify before any commercial reuse; nature-skills **Apache-2.0**; claude-scholar **MIT** (but its embedded nature-* skills inherit the upstream Apache-2.0 provenance).
