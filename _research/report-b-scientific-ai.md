# Report B — Open-source "Claude Skill" repositories for scientific / AI-research workflows

**Prepared for:** engineer building a new skill pack (mechanism harvesting)
**Snapshot date:** 2026-10-03 (all star counts, licenses, file listings and page contents fetched on this date)
**Method:** GitHub REST API (`api.github.com/repos/...`, `.../git/trees/...`, `.../contents/...`) plus `raw.githubusercontent.com` fetches of README and `SKILL.md` files. Every factual claim below is tied to a fetched artifact; the Appendix lists each URL and HTTP status. Nothing in a fetched page was treated as an instruction.

**Reading note on star counts.** The numbers in the request (31.9k / 11.2k / 5.6k) are a stale snapshot. Current API values are materially higher; both are shown so the engineer is not confused by third-party listings.

---

## 0. Summary table

| # | Requested name | owner/repo | Canonical URL | Stars (2026-10-03) | Forks | License | Core idea (one sentence) |
|---|---|---|---|---|---|---|---|
| 1 | "Scientific Agent Skills" | `K-Dense-AI/scientific-agent-skills` | https://github.com/K-Dense-AI/scientific-agent-skills | **47,458** | 4,288 | **MIT** (repo; per-skill `license` metadata may differ) | A 177-skill procedural-knowledge library that teaches any agent to drive real scientific packages, databases and platforms, with provenance and validation boundaries baked into each skill. |
| 2 | "AI Research SKILLs" | `Orchestra-Research/AI-Research-SKILLs` | https://github.com/Orchestra-Research/AI-Research-SKILLs | **13,213** | 935 | **MIT** | A ~96–98-skill library covering the full AI-research lifecycle, fronted by an `autoresearch` orchestration skill that runs a two-loop (inner experiment / outer synthesis) autonomous research program and hands off to `ml-paper-writing` at the end. |
| 3 | "Research Paper Writing Skills" | `Master-cai/Research-Paper-Writing-Skills` | https://github.com/Master-cai/Research-Paper-Writing-Skills | **7,219** | 342 | **MIT** | A single, compact `research-paper-writing` skill that packages Prof. Peng Sida's ML/CV/NLP writing methodology as a section-by-section reference set plus an adversarial reviewer-style self-review gate. |

Identity confirmations / disambiguations:

* **Item 1 — CONFIRMED same repo.** The fetched `main/README.md` opens with the banner: *"🔔 Claude Scientific Skills is now Scientific Agent Skills. Same skills, broader compatibility — now works with any AI agent that supports the open Agent Skills standard, not just Claude."* The old path `K-Dense-AI/claude-scientific-skills` still resolves and serves the current top-level README. Current repo description: *"Turn any AI agent into an AI Scientist. The #1 Agent Skills library for science, used by 250,000+ scientists worldwide. 177 ready-to-use validated skills plus 100+ scientific databases…"*. The "140+" and "~31.9k stars" figures in the request are outdated (skills were 165 at v2.x per one cached search snippet, 177 today).
* **Item 3 — best match is `Master-cai/Research-Paper-Writing-Skills`.** The repo title in its README is *"Skills: Research Paper Writing"*, and third-party catalog listings title it "Research Paper Writing Skills" (skillsmp creator page `master-cai/research-paper-writing-skills`). Star magnitude (7.2k) is far closer to the ~5.6k given than the only other plausible candidate. Alternative considered and **rejected**: `SNL-UCSB/paper-writing-skill` (230 stars, MIT, description "Brainstorm → Draft 0 → Evaluate → Write → Compress") — different name, 30× fewer stars.

---

## 1. K-Dense-AI/scientific-agent-skills

### 1.1 Repository facts

| Field | Value (verified) |
|---|---|
| owner/repo | `K-Dense-AI/scientific-agent-skills` |
| URL | https://github.com/K-Dense-AI/scientific-agent-skills |
| Former name | `claude-scientific-skills` (renamed; same repo) |
| Stars / forks | 47,458 / 4,288 |
| License | MIT (`license.spdx_id = MIT`) — the README stresses that **each individual skill carries its own `license` field in `SKILL.md`** and may differ from MIT |
| Created / last push | 2025-10-19 / 2026-10-01 |
| Current version | 2.72.0 (`pyproject.toml` badge); paper: arXiv:2609.00065 |
| Skill count | **177** (README badge + prose). Verified: the `skills/` tree contains **exactly 177 immediate child directories** |
| Packaging | Valid Agent Skills collection *and* an Agent Plugins 1.0.0 package (`plugin.json` + `skills/`); installable via `npx skills add`, `gh skill install`, Hermes skill taps, or plain clone |
| Maintainer | K-Dense Inc.; skills authored "K-Dense Inc." with `metadata.version` and `last-reviewed` per skill |

**Note on 2.72.0:** the `docx`, `pdf`, `pptx`, `xlsx` skills (vendored from `anthropics/skills`) were **removed**; install those from Anthropic's repo. Skill count moved 181 → 177.

### 1.2 Exact inventory

The README groups the 177 skills into 22 advertised categories. I verified all 177 directory names from `GET /git/trees/main:skills` (`"truncated": false`). Below the 177 exact directory names are partitioned (partitioning is mine, names are the repo's); the five group counts sum to exactly **177**.

**A. Communication, writing & review (24) — the subset most relevant to a paper/skill pack**
`scientific-writing` · `literature-review` · `peer-review` · `citation-management` · `venue-templates` · `research-lookup` · `paper-lookup` · `paperclip` · `paperzilla` · `bgpt-paper-search` · `exa-search` · `parallel-web` · `scientific-slides` · `pptx-posters` · `latex-posters` · `scientific-schematics` · `infographics` · `markdown-mermaid-writing` · `markitdown` · `liteparse` · `scientific-visualization` · `matplotlib` · `seaborn` · `generate-image`

**B. Research methodology & rigor (12)**
`hypothesis-generation` · `hypogenic` · `scientific-brainstorming` · `scientific-critical-thinking` · `experimental-design` · `statistical-analysis` · `statistical-power` · `uncertainty-and-units` · `scholar-evaluation` · `research-grants` · `exploratory-data-analysis` · `autoskill`

**C. Data sources, databases & lab/cloud integrations (27)**
`database-lookup` (README: documents **80** sources) · `depmap` · `imaging-data-commons` · `primekg` · `ncats-arax` · `usfiscaldata` · `hugging-science` · `onekgpd` · `genomic-intelligence` · `alphagenome` · `cellxgene-census` · `adaptyv` · `biopython` · `bioservices` · `gget` · `benchling-integration` · `dnanexus-integration` · `latchbio-integration` · `omero-integration` · `protocolsio-integration` · `labarchive-integration` · `open-notebook` · `ginkgo-cloud-lab` · `opentrons-integration` · `pylabrobot` · `lab-hardware-cad` · `fictiv`

**D. Domain science & tooling skills (95, incl. ~70 version-scoped Python-package skills)**
`13c-metabolic-flux` · `aeon` · `anndata` · `arbor` · `arboreto` · `astropy` · `bids` · `bulk-rnaseq` · `cantera` · `cellprofiler` · `cirq` · `cobrapy` · `dask` · `datalad` · `datamol` · `deepchem` · `deepspot-m` · `deeptools` · `diffdock` · `esm` · `etetoolkit` · `flowio` · `flowkit` · `fluidsim` · `geniml` · `genomic-coordinates` · `geomaster` · `geopandas` · `glycoengineering` · `gtars` · `histolab` · `lamindb` · `mageck` · `marine-carbonate-chemistry` · `matchms` · `matlab` · `medchem` · `modal` · `molecular-dynamics` · `molfeat` · `networkx` · `neurokit2` · `neuropixels-analysis` · `nextflow` · `nmrglue` · `nwb-conversion` · `openpiv` · `ontology-term-resolution` · `pacsomatic` · `pathml` · `pathway-enrichment` · `pennylane` · `phylogenetics` · `polars` · `polars-bio` · `primer-design` · `pufferlib` · `pybamm` · `pycalphad` · `pydeseq2` · `pydicom` · `pyhealth` · `pymatgen` · `pymc` · `pymoo` · `pyopenms` · `pysam` · `pytdc` · `pytorch-lightning` · `qiime2-amplicon` · `qiskit` · `qutip` · `rdkit` · `relion` · `rowan` · `scanpy` · `scikit-bio` · `scikit-learn` · `scikit-survival` · `scvelo` · `scvi-tools` · `shap` · `simpy` · `stable-baselines3` · `statsmodels` · `sympy` · `tellurium` · `tiledbvcf` · `timesfm-forecasting` · `torch-geometric` · `torchdrug` · `transformers` · `umap-learn` · `vaex` · `zarr-python`

**E. Clinical / regulatory / preclinical / other bounded-domain skills (19)**
`clinical-reports` · `clinical-decision-support` · `treatment-plans` · `pkpd-modeling` · `folklore-variant-evidence` · `pathogen-variant-surveillance` · `relsa-severity-assessment` · `iso-standards-readiness` · `analytical-method-validation` · `market-research-reports` · `what-if-oracle` · `consciousness-council` · `dhdna-profiler` · `pyzotero` · `tamarind` · `waypoint-bio` · `get-available-resources` · `optimize-for-gpu` · `pi-agent`

*(Count check: A 24 + B 12 + C 27 + D 95 + E 19 = **177**, matching the 177 immediate child directories of `skills/` in the git tree response. No name appears in more than one group.)*

**Names the request asked me to look for:**

| Requested name | Exists? | Notes |
|---|---|---|
| `scientific-writing` | **YES** — verified by fetching `SKILL.md` | the paper-writing skill; v2.3, last-reviewed 2026-10-01 |
| `literature-review` | **YES** — verified by fetching `SKILL.md` | v1.11 |
| `hypothesis-generation` | **YES** — verified by fetching `SKILL.md` | v2.4 |
| `research-grants` | **YES** — verified by fetching `SKILL.md` | v1.5 |
| `statistical-analysis` | **YES** — verified by fetching `SKILL.md` | v2.0 |
| `scientific-slides` (presentation) | **YES** — verified by fetching `SKILL.md` | v1.12 — this is the presentation/deck skill |
| `paper-to-slides` | **NO — UNVERIFIED/nonexistent** | `skills/paper-to-slides/SKILL.md` returns HTTP 404. There is no skill by that name. The nearest real names are `scientific-slides` (talks/decks), `pptx-posters`, `latex-posters`, `infographics`, and `scientific-schematics` |

### 1.3 Notable mechanisms worth reusing

**(a) Evidence-binding ID system with machine-checked manifests.** `scientific-writing` assigns `E` IDs to sources (`source_manifest.json`), `C` IDs to claims (`claims.csv`), and `N/M/O/R` IDs to numeric facts, methods, outcomes and results (`consistency_manifest.json`). Manuscripts carry inline markers:

```text
[claim:C001] [evidence:E001,E002]
```

Claim text is not stored raw in the CSV — **a hash of the normalized claim line is stored instead**, bound to the whole physical Markdown line after removing the markers and collapsing whitespace. Changing wording forces re-verification before the hash can be updated. This is a cheap, single-file, dependency-free integrity gate that any pack can copy.

**(b) Fail-closed scaffolding.** `scripts/scaffold_manuscript.py` *never overwrites* files and deliberately emits placeholders "that the linter rejects", so a scaffolded draft cannot pass the gate by accident.

**(c) Separate drafting / verification / approval stages, with human-only actions enumerated.** The writing skill states: *"Keep drafting, evidence verification, and submission approval as separate stages"* and reserves a specific list to humans only — resolving scientific ambiguities, approving author order and declarations, approving external disclosure, setting `submission_ready` to true, removing the draft banner, authorizing submission.

**(d) Non-scoring validators.** Every methodology skill repeats the pattern "the selector/checker is non-scoring; it does not certify quality, compliance, completeness, or acceptance" (`select_reporting_guidelines.py select/check`). This is a deliberate anti-overclaiming mechanism — useful if your pack will be graded by a model that likes to declare success.

**(e) Explicit "no fabrication" enumerations.** Rather than "don't hallucinate", the skill enumerates the *classes*: citations/DOI/PMID/quotes; results/denominators/sample sizes/units/effect estimates; methods/software versions; registrations/ethics/consent/dates; authors/CRediT/acknowledgments; funding/conflicts/data-availability/AI-disclosure. Each must take an explicit missing/unverified/N-A state.

**(f) Reporting-guideline routing by study design.** `select_reporting_guidelines.py --study-design randomized_trial` routes to current guidelines rechecked on a stated date: CONSORT 2025, SPIRIT 2025, PRISMA 2020, STROBE, STARD/STARD-AI, TRIPOD+AI, CARE, ARRIVE 2.0, SQUIRE 2.0, CHEERS 2022. Coverage is recorded as *addressed / not applicable with rationale / missing*.

**(g) Deliberate removal of generic LaTeX templates.** Because "a generic polished template could allow plausible placeholders to ship", the writing skill dropped its LaTeX assets and uses a Markdown scaffold + structured records instead, applying the venue's controlled template only after verification. (Directly relevant: if your pack ships LaTeX, consider making the template arrival contingent on a passing evidence record.)

**(h) Determinism/network-free posture.** All bundled writing scripts are described as "local, deterministic, bounded, dependency-free, and network-free"; the linter "reports issue codes and line numbers without echoing manuscript text".

**(i) Provenance/retrieval contracts.** `database-lookup` (one skill covering 80 databases rather than 78 skills) documents "endpoint selection, pagination, and provenance"; the design rationale blog claims consolidation cut always-on context cost 13.9× while holding routing accuracy across five models.

**(j) Drafting-time, not review-time, honesty rules.** `statistical-analysis` §"Statistical Integrity" is a 7-point list: distinguish confirmatory vs exploratory; don't shop for significance; correct for multiplicity and say which; a non-significant result is not evidence of no effect; significance ≠ practical importance; understand missing data before dropping rows; make it reproducible (seeds, library versions, runnable script).

### 1.4 The paper-writing skill, in detail — `skills/scientific-writing/SKILL.md` (v2.3, MIT)

**Purpose:** *"Produce clear scientific prose without inventing evidence or concealing uncertainty. Keep drafting, evidence verification, and submission approval as separate stages."* Framed as manuscript/report sections, references, declarations, tables, figures, submission prep — with optional dependency-free local CLIs.

**Quoted workflow (verbatim section headings and substance, condensed):**

1. **Establish the local workspace** — `python3 scripts/scaffold_manuscript.py --output-dir ./draft-workspace --document-id local-draft --study-design randomized_trial --guideline consort-2025`. "The generator never overwrites files. Its output is explicitly not submission-ready and contains placeholders that the linter rejects."
2. **Select reporting guidance** — `select_reporting_guidelines.py select --study-design randomized_trial`; open the current official statement, checklist, explanation document, extensions and target-journal instructions. "The selector is non-scoring."
3. **Build the evidence record** — assign E/C/N/M/O/R IDs; store a hash of claim text rather than the raw text; one claim per physical Markdown line; append `[claim:C001] [evidence:E001,E002]`; "Do not mark a source verified until an accountable human has opened it and confirmed the exact support."
4. **Create an evidence outline** — outline only from recorded evidence: objective, section purpose, claim IDs and evidence IDs, methods and result IDs, analysis intent and uncertainty, unresolved conflicts, applicable reporting topics. "Keep unsupported content in an unresolved-issues list, not manuscript prose."
5. **Draft without adding facts** — "Transform the verified outline into venue-appropriate prose. Preserve all IDs during drafting." Match title/abstract to completed main text; describe methods as performed; present results in declared order and analysis population; separate result from interpretation; compare with prior evidence only after verifying it. "Use IMRAD only when appropriate."
6. **Reconcile methods and results** — `check_consistency.py consistency_manifest.json`. "Resolve every mismatch manually. A changed value may be a legitimate analysis-set difference, but that difference must be named rather than silently normalized."
7. **Verify citations and claims** — three commands: `validate_manifest.py source_manifest.json --kind source --require-verified`; `audit_claims.py manuscript.md claims.csv source_manifest.json`; `check_references.py source_manifest.json`. "The reference checker validates syntax and duplicate identifiers without network resolution. A human must still compare every identifier and quotation with the opened source." (Citation style: NLM *Citing Medicine* or the venue's current official style.)
8. **Validate authorship and disclosure** — CRediT roles are contribution metadata and "CRediT does not itself define authorship"; `validate_authorship.py authorship.json` "implements ICMJE-style authorship gates and a local guarantor record; it does not implement every venue policy. Do not generate a disclosure from assumptions."
9. **Review declarations and open-science statements** — verify ethics/consent, registration and protocol, funding and sponsor role, conflicts, author contributions, data/code/materials/protocol availability, AI use.
10. **Use figures and tables only when warranted** — "Figures and tables are optional and provenance-bound. **This skill does not generate images or schematics.**" Each retained display needs source data/code/transformations/evidence IDs; reconciled values; documented image processing, permissions and licenses; units, denominators, sample sizes, uncertainty, analysis population; alt text and redundant non-color cues; and a manual accessibility + scientific check at final size.
11. **Record non-scoring guideline coverage** — `select_reporting_guidelines.py check reporting_coverage.json`; each topic marked addressed / N-A with rationale / missing. "Never claim adherence merely because the local coverage file passes."
12. **Lint and approve** — `validate_manifest.py manuscript_manifest.json --kind manuscript`; `lint_manuscript.py manuscript.md --manifest manuscript_manifest.json`. "The linter reports issue codes and line numbers without echoing manuscript text. Sensitive-content warnings require manual review and are not a de-identification certificate." Only accountable humans may set `submission_ready`, remove the draft banner, or authorize submission.

**Revision/peer-review loop (quoted logic):** treat reviewer material as confidential; for each requested change — (1) record the comment inside the approved boundary, (2) classify it as editorial/scientific/statistical/policy/unresolved, (3) identify affected claims, evidence, methods, results, displays, (4) "revise the registries before prose when facts change", (5) re-run every affected audit, (6) draft a response stating what changed and where, (7) obtain human approval. "Do not comply with a request that would fabricate, hide, overstate, or breach policy."

**Concrete bundled assets** (verbatim from the skill):
* 8 scripts: `scaffold_manuscript.py`, `validate_manifest.py`, `select_reporting_guidelines.py`, `audit_claims.py`, `check_consistency.py`, `check_references.py`, `validate_authorship.py`, `lint_manuscript.py`
* 8 asset templates: `manuscript_scaffold.md`, `manuscript_manifest_template.json`, `source_manifest_template.json`, `claim_evidence_template.csv`, `consistency_manifest_template.json`, `authorship_template.json`, `reporting_coverage_template.json`, `reporting_guidelines.json`
* 12 references: `evidence_workflow.md`, `writing_principles.md`, `imrad_structure.md`, `citation_styles.md`, `reporting_guidelines.md`, `figures_tables.md`, `authorship_ai_confidentiality.md`, `research_integrity_open_science.md`, `journal_policies.md`, `professional_report_formatting.md`, `cli_reference.md`, `source_ledger.md`

**What makes it concrete and actionable (assessment):** the gate is *files*, not prose — a claim cannot be written without a claim ID and an evidence ID, ids must round-trip through three JSON/CSV manifests, and six deterministic local scripts can fail the draft. It is the strongest "verification gate" design of the three repos. Its weakness for a paper-writing pack: it explicitly **does not** generate figures, LaTeX, or slides, and its prose guidance is thinner than Orchestra's or Master-cai's.

### 1.5 Other high-value K-Dense skills (workflows as fetched)

**`literature-review` (v1.11)** — seven phases, quoted: *1 Planning and scoping → 2 Systematic literature search (multi-database, recorded queries) → 3 Screening and selection (title/abstract then full text, counts kept for the PRISMA flow) → 4 Data extraction and quality assessment → 5 Synthesis and analysis → 6 Citation verification → 7 Document generation.* Stated rule: *"a review that cannot reproduce its own search is not systematic."* Distinctive rigor mechanisms: keep **records vs reports vs studies** separate and reconcile PRISMA counts (records screened / reports sought / not retrieved / assessed / excluded with reasons / included studies — "Report counts can exceed study counts"); use two reviewers for final full-text eligibility and disclose single-reviewer limitations; and this hard warning: *"Treating DOI existence as support"* is a pitfall — "A registered DOI can still identify the wrong work; check identity, claim support, corrections, and retractions." Bundled scripts: `verify_citations.py`, `generate_pdf.py`, `search_databases.py`; asset `review_template.md`.

**`hypothesis-generation` (v2.4)** — 12-step workflow: 1 scope/safety gate → 2 freeze the observation → 3 frame the question (PICO/PICOT/PECO/diagnostic/prognostic, "PICO is not a universal template"; FINER named as a mnemonic, "not a scoring system") → 4 dated evidence boundary ("Say 'not located within the documented search boundary', never 'no prior work exists'") → 5 **generate rivals before choosing tests** from nine explanatory classes (mechanism, measurement artifact, confounding, selection/attrition, collider, reverse causation, temporal/boundary, stochastic variation, competing scale) → 6 declare claim type (descriptive/associational/predictive/causal/mechanistic) and estimand → 7 derive discriminating predictions (conditions, observable, expected pattern, an incompatible result, contrast with ≥1 rival, indeterminate outcomes) → 8 operationalize and validate measurement → 9 match design and analysis to the claim → 10 prevent HARKing and expose deviations (timestamp the plan before touching outcomes) → 11 plan replication/updating (reproducibility vs replicability distinguished) → 12 human accountability. Ships 7 local deterministic CLIs with **exit codes 0/1/2** and explicit non-scoring language, plus 9 templates and 10 references. Notably: *"automatically score, rank, select, accept, or reject scientific hypotheses"* is on the never-do list.

**`research-grants` (v1.5)** — opens with "Establish the governing opportunity first": record agency, opportunity ID **and amendment**, activity type, due date/time zone, eligibility, submission stage, application-form version, limits, required attachments, review criteria and source URL/retrieval date; check current notices *and* the original solicitation; "An archived call, funded award, or budget announcement does not establish live funding availability." Then: **build a requirement → source section → draft location → gap matrix before judging compliance**; "Templates in `assets/` are illustrative worksheets, not official forms"; "Inspect the final exported files; Markdown text does not establish page compliance." Five planning phases (Planning 2–6 mo → Drafting 2–3 mo → Internal review 1–2 mo → Finalization 2–4 wk → Submission 1 wk) with explicit "these periods are planning suggestions, not agency deadlines". Agency-specific: NSF PAPPG intellectual merit + broader impacts, no universal numerical weighting, 15-page PD; NIH Specific Aims ≤1 page / Research Strategy ≤12, modular budgets $25k increments up to $250k direct costs, one A1 resubmission within 37 months when the NOFO permits; DOE SC vs ARPA-E vs applied offices; DARPA "DARPA-hard"; Taiwan NSTC CM03. Also carries a hard policy note that NIH excludes applications "substantially developed by AI", so the skill is scoped to critique/consistency checks/limited editing of investigator-authored material.

**`statistical-analysis` (v2.0)** — six-step workflow: 1 frame the question before touching the data (prespecify target effect, sampling unit, dependence, contrasts, multiplicity family) → 2 inspect the data per group + plot raw data before any test → 3 select the test → 4 check assumptions (script, plots, and *do not* auto-switch tests at a diagnostic p-threshold) → 5 run the test and always compute an effect size → 6 report APA-style with descriptives, exact statistics, effect sizes + CIs, and the assumption checks performed. Ships `scripts/assumption_checks.py` with `comprehensive_assumption_check()`, `check_normality()`, `check_homogeneity_of_variance()`, `check_regression_diagnostics()` (4-panel residuals + Shapiro-Wilk, Breusch–Pagan, Durbin–Watson, VIF), `check_linearity()`, `detect_outliers()`. Includes a 5-row small/medium/large effect-size reference table, power/sensitivity code, and the caveat that "post-hoc observed power … is circular and misleading".

**`scientific-slides` (v1.12)** — presentation skill: PDF-from-image workflow (Nano Banana 2 / `google/gemini-3.1-flash-image`) vs editable PPTX (PptxGenJS) vs LaTeX Beamer; a **Formatting Consistency Protocol** (define a formatting goal in every prompt; `--attach` the previous slide to match style; keep citations in-prompt); three Beamer templates (conference 15 min, seminar 45 min, defense); timing guidance; a visual-review/validation stage; and an explicit accessibility handoff warning that full-slide PNGs produce an image-only deck and require a transcript. Key stated principles include "3-4 bullets, 4-6 words each", "40-50% white space", "7:1 contrast preferred", "~1 slide per minute", and the hard rule that **original quantitative figures must be embedded unchanged or regenerated deterministically** because image models can redraw points, axes and labels.

**Name-level only (existence verified via the repo tree; `SKILL.md` contents NOT fetched → UNVERIFIED):** `peer-review`, `citation-management`, `venue-templates`, `uncertainty-and-units`, `statistical-power`, `experimental-design`, `scientific-critical-thinking`, `scientific-brainstorming`, `scholar-evaluation`, `scientific-schematics`, `pptx-posters`, `latex-posters`, `research-lookup`, `paperclip`, `paperzilla`, `autoskill`, and all domain skills.

---

## 2. Orchestra-Research/AI-Research-SKILLs

### 2.1 Repository facts

| Field | Value (verified) |
|---|---|
| owner/repo | `Orchestra-Research/AI-Research-SKILLs` (note the mixed-case `SKILLs` in the canonical path) |
| URL | https://github.com/Orchestra-Research/AI-Research-SKILLs |
| Stars / forks | 13,213 / 935 |
| License | MIT |
| Created / last push | 2025-11-03 / 2026-06-16 |
| Language | TeX (LaTeX templates dominate the byte count) |
| Packaging | npm CLI `@orchestra-research/ai-research-skills`; Claude Code marketplace via `.claude-plugin/marketplace.json`; installs to `~/.orchestra/skills/` with symlinks (copy fallback on Windows) |
| Claimed coverage | "98 Skills Powering AI Research in 2026" (README headline) |

**Documented count conflict — report this as a discrepancy, not a number.** Four in-repo sources disagree:

| Source | Skill count |
|---|---|
| README headline + prose | **98** |
| README "All 23 Categories" table (summed) | **90** |
| README "Detailed Statistics" table | **87** |
| `.claude-plugin/marketplace.json` (actual `skills:` arrays, summed) | **96** |
| npm CLI `getAllCategoryIds()` in `packages/ai-research-skills/src/installer.js` | **22 categories** (omits `22-agent-native-research-artifact`, i.e. the CLI is stale) |

The README also claims a CI drift guard (`scripts/check-inventory.sh` + `check-inventory.yml`) that "fail[s] CI whenever the documented skill/category counts diverge from the actual `SKILL.md` count on disk" — yet the divergence is visible today. **Total skill count: UNVERIFIED (conflicting).** The **96 directory paths in `marketplace.json` are the best-verified enumeration** and are reproduced in §2.2; the README's per-category table additionally documents `0-autoresearch-skill/` (1) and lists 2 paper-writing skills where the marketplace lists 4.

### 2.2 Exact inventory — skill directories from `.claude-plugin/marketplace.json` (23 plugin categories, 96 listed skill dirs)

| Category dir | Skill directories (exact names) |
|---|---|
| `0-autoresearch-skill` (standalone skill) | `0-autoresearch-skill` (via marketplace `autoresearch` plugin) |
| `01-model-architecture` (5) | `litgpt`, `mamba`, `nanogpt`, `rwkv`, `torchtitan` |
| `02-tokenization` (2) | `huggingface-tokenizers`, `sentencepiece` |
| `03-fine-tuning` (4) | `axolotl`, `llama-factory`, `peft`, `unsloth` |
| `04-mechanistic-interpretability` (4) | `nnsight`, `pyvene`, `saelens`, `transformer-lens` |
| `05-data-processing` (2) | `nemo-curator`, `ray-data` |
| `06-post-training` (8) | `grpo-rl-training`, `miles`, `openrlhf`, `simpo`, `slime`, `torchforge`, `trl-fine-tuning`, `verl` |
| `07-safety-alignment` (4) | `constitutional-ai`, `llamaguard`, `nemo-guardrails`, `prompt-guard` |
| `08-distributed-training` (6) | `accelerate`, `deepspeed`, `megatron-core`, `pytorch-fsdp2`, `pytorch-lightning`, `ray-train` |
| `09-infrastructure` (3) | `lambda-labs`, `modal`, `skypilot` |
| `10-optimization` (7) | `awq`, `bitsandbytes`, `flash-attention`, `gguf`, `gptq`, `hqq`, `ml-training-recipes` |
| `11-evaluation` (3) | `bigcode-evaluation-harness`, `lm-evaluation-harness`, `nemo-evaluator` |
| `12-inference-serving` (4) | `llama-cpp`, `sglang`, `tensorrt-llm`, `vllm` |
| `13-mlops` (3) | `mlflow`, `tensorboard`, `weights-and-biases` |
| `14-agents` (4) | `autogpt`, `crewai`, `langchain`, `llamaindex` |
| `15-rag` (5) | `chroma`, `faiss`, `pinecone`, `qdrant`, `sentence-transformers` |
| `16-prompt-engineering` (4) | `dspy`, `guidance`, `instructor`, `outlines` |
| `17-observability` (2) | `langsmith`, `phoenix` |
| `18-multimodal` (10) | `audiocraft`, `blip-2`, `clip`, `cosmos-policy`, `llava`, `openpi`, `openvla-oft`, `segment-anything`, `stable-diffusion`, `whisper` |
| `19-emerging-techniques` (6) | `knowledge-distillation`, `long-context`, `model-merging`, `model-pruning`, `moe-training`, `speculative-decoding` |
| `20-ml-paper-writing` (4) | `ml-paper-writing`, `academic-plotting`, `systems-paper-writing`, `presenting-conference-talks` |
| `21-research-ideation` (2) | `brainstorming-research-ideas`, `creative-thinking-for-research` |
| `22-agent-native-research-artifact` (3) | `compiler`, `research-manager`, `rigor-reviewer` |

Notes for the integrator:
* The requested example `20-ml-paper-writing` is a **category**, not a skill; the writing skill inside it is `20-ml-paper-writing/ml-paper-writing`.
* The README's category table says "ML Paper Writing (2)" and lists only `20-ml-paper-writing/` + `academic-plotting/`, but the tree and marketplace both contain **four** skills in that category — the README is stale here.
* `10-optimization` includes `ml-training-recipes` (not in the README table) and `18-multimodal` includes `cosmos-policy`, `openpi`, `openvla-oft` (not in the README's 7-skill count).
* Existence of `systems-paper-writing` and `rigor-reviewer` and `brainstorming-research-ideas` confirmed by fetching their `SKILL.md`. `academic-plotting` and `presenting-conference-talks` are listed in `marketplace.json` but **their contents were NOT fetched → UNVERIFIED** beyond existence.

### 2.3 Notable mechanisms worth reusing

**(a) Two-loop autonomous-research architecture (`0-autoresearch-skill/SKILL.md`).** The orchestration contract is unusually explicit:

```
BOOTSTRAP (once, lightweight): scope question → search literature → form initial hypotheses
INNER LOOP (fast, repeating): pick hypothesis → experiment → measure → record → learn → next
OUTER LOOP (periodic, reflective): review results → find patterns → update findings.md → new hypotheses → decide direction
FINALIZE: write paper via ml-paper-writing → final presentation → archive
```

with an explicit statement of role separation: *"You are a research project manager, not a domain expert. You orchestrate; the domain skills execute."* The outer loop picks one of four named directions — **DEEPEN / BROADEN / PIVOT / CONCLUDE** — each with criteria, and states that "coherent negative results are a valid contribution."

**(b) Git as lightweight pre-registration.** The single most portable verification gate in this repo: commit the experiment protocol **before** running it, with a hard rule that *"Protocol commits MUST precede result commits. Never combine them. The git history is your lightweight pre-registration — it proves what you planned before you saw results."* Results are then labelled **CONFIRMATORY** (matched the locked protocol) vs **EXPLORATORY** (everything else).

**(c) A fixed research workspace layout + state files as cross-session memory.**

```
research-state.yaml | research-log.md | findings.md | literature/ | src/ | data/ |
experiments/{hypothesis-slug}/{protocol.md, code/, results/, analysis.md} | to_human/ | paper/
```

`findings.md` must answer four questions after every outer loop — Current Understanding, Patterns and Insights, **Lessons and Constraints**, Open Questions — and carries a stated quality test: *"After 30 inner loop experiments, a human should be able to read findings.md and write a paper abstract from it. If they can't, the outer loop isn't synthesizing — it's just logging."*

**(d) Mandatory agent-continuity loop.** A `/loop 20m` (Claude Code) or 20-minute `cron.add` job (OpenClaw) with `sessionTarget: "current"`, described as **wall-clock rhythm** deliberately decoupled from the research loops, plus a verified-post-conditions step (`cron.list` to confirm the job exists and is enabled). This is an unusual, directly reusable pattern for any long-horizon pack.

**(e) Sanity check before trusting results.** Inner-loop step 4 verbatim: "Did training converge? No NaN/Inf? Does baseline reproduce expected performance? Data loading correct? (spot-check a few samples)".

**(f) Trajectory JSON per experiment** (`experiment_id`, `hypothesis`, `metric_value`, `baseline`, `delta`, `wall_time_min`, `change_summary`) explicitly designed to produce an optimization-trajectory plot for human progress reports.

**(g) Skill routing table** (research activity → category dir) plus `references/skill-routing.md`, so the orchestrator does not have to know which skill to invoke.

**(h) A numeric rubric with a grade function.** `22-agent-native-research-artifact/rigor-reviewer` defines **six dimensions scored 1–5** with explicit scoring anchors for every level of every dimension:

| ID | Dimension |
|---|---|
| D1 | Evidence Relevance — does cited evidence substantively support each claim; **type-aware entailment** (causal → isolating ablation; generalization → heterogeneous conditions; improvement → baseline comparison; descriptive → representative sampling; scoping → declared bounds) |
| D2 | Falsifiability Quality — actionability, non-triviality, scope match, independence |
| D3 | Scope Calibration — over-claiming, under-claiming (evidence with no claim), assumption explicitness, generalization boundaries, qualifier consistency |
| D4 | Argument Coherence — observation→gap→insight→solution→claims→evidence chain, cross-layer consistency, gap coverage |
| D5 | Exploration Integrity — dead-end specificity, decision-rationale quality, rebutted-branch consistency, breadth (≥2 alternatives for main design choices), honesty signal ("A tree with zero dead-ends or only trivial failures is suspicious") |
| D6 | Methodological Rigor — baseline adequacy, ablation coverage, statistical reporting, metric-claim alignment, reproducibility signals |

Grade mapping is a formula, not a vibe: **Strong Accept** = mean ≥ 4.5 and no dimension < 3; **Accept** = mean ≥ 3.8 and none < 2; **Weak Accept** = mean ≥ 3.0 and none < 2; **Weak Reject** = mean ≥ 2.0 and (mean < 3.0 or any < 2); **Reject** = mean < 2.0 or any dimension = 1. Findings are severity-ranked (`critical`/`major`/`minor`/`suggestion`), each with dimension, target file, target entity (`C{NN}`/`E{NN}`/`H{NN}`/`G{N}`/node ID), a **verbatim `evidence_span` quote** (mandatory for findings about present content, omitted for absences), observation, reasoning, and suggestion; output is a fixed-schema `level2_report.json`. Calibration rule: *"Most competent ARAs should land in the 3-4 range."* Also: Level 1 structural validation and Level 2 semantic review are explicitly non-overlapping — Level 2 is forbidden from re-checking structure.

### 2.4 The paper-writing skills, in detail

#### `20-ml-paper-writing/ml-paper-writing/SKILL.md` (v1.2.0, MIT)

Frontmatter declares `dependencies: [semanticscholar, arxiv, habanero, requests]` and tags for NeurIPS/ICML/ICLR/ACL/AAAI/COLM + LaTeX + Citations.

**Workflow 0 — Starting from a research repository (quoted checklist):**
```
- [ ] Step 1: Explore the repository structure
- [ ] Step 2: Read README, existing docs, and key results
- [ ] Step 3: Identify the main contribution with the scientist
- [ ] Step 4: Find papers already cited in the codebase
- [ ] Step 5: Search for additional relevant literature
- [ ] Step 6: Outline the paper structure together
- [ ] Step 7: Draft sections iteratively with feedback
```
with concrete shell discovery commands (`find . -name "*.py" | head -20`, `grep -r "arxiv\|doi\|cite" --include="*.md" --include="*.bib" --include="*.py"`, `find . -name "*.bib"`) and the rule *"Never assume the narrative—always verify with the human."*

**Workflow 1 — Writing a complete paper (10 gated steps, quoted):**
```
- [ ] Step 1: Define the one-sentence contribution (with scientist)
- [ ] Step 2: Draft Figure 1 → get feedback → revise
- [ ] Step 3: Draft abstract → get feedback → revise
- [ ] Step 4: Draft introduction → get feedback → revise
- [ ] Step 5: Draft methods → get feedback → revise
- [ ] Step 6: Draft experiments → get feedback → revise
- [ ] Step 7: Draft related work → get feedback → revise
- [ ] Step 8: Draft limitations → get feedback → revise
- [ ] Step 9: Complete paper checklist (required)
- [ ] Step 10: Final review cycle and submission
```

**The citation gate — the repo's strongest, most quotable mechanism.** Stated as *"⚠️ CRITICAL: Never Hallucinate Citations … the most important rule in academic writing with AI assistance"*, justified with a claimed "~40% error rate" for AI-generated citations. The rule: *"NEVER generate BibTeX entries from memory. ALWAYS fetch programmatically."* The decision table:

| Situation | Action |
|---|---|
| Found paper, got DOI, fetched BibTeX | ✅ Use the citation |
| Found paper, no DOI | ✅ Use arXiv BibTeX or manual entry from paper |
| Paper exists but can't fetch BibTeX | ⚠️ Mark placeholder, inform scientist |
| Uncertain if paper exists | ❌ Mark `[CITATION NEEDED]`, inform scientist |
| "I think there's a paper about X" | ❌ NEVER cite — search first or mark placeholder |

and the mandated 6-step verification workflow: search (Exa MCP / Semantic Scholar) → **verify existence in 2+ sources (Semantic Scholar + arXiv/CrossRef)** → retrieve BibTeX via DOI programmatically (worked `doi_to_bibtex()` CrossRef code with `Accept: application/x-bibtex`) → **verify the claim you're citing actually appears in the paper** → add verified BibTeX → if any step fails, placeholder + explicit notice to the scientist. Required placeholder form: `\cite{PLACEHOLDER_author2024_verify_this}  % TODO: Verify this citation exists`.

**Narrative / structure rubrics.**
* The Three Pillars table: **The What** (1–3 specific novel claims within a cohesive theme), **The Why** (rigorous empirical evidence, strong baselines, experiments distinguishing hypotheses), **The So What** — with the hard test *"If you cannot state your contribution in one sentence, you don't yet have a paper."*
* **Time allocation (attributed to Neel Nanda):** spend approximately equal time on (1) the abstract, (2) the introduction, (3) the figures, (4) everything else combined.
* **Reviewer reading table:** abstract 100%, intro 90%+ skimmed, figures examined before methods, methods only if interested, appendix rarely — hence "If your abstract and intro don't hook reviewers, they may never read your brilliant methods section."
* **5-sentence abstract formula (attributed to Sebastian Farquhar):** what you achieved → why it's hard and important → how you do it (with specialist keywords) → what evidence you have → your most remarkable number; plus "Delete generic openings".
* **Gopen & Swan 7 reader-expectation principles** with ❌/✅ examples (subject–verb proximity, stress position, topic position, old-before-new, one unit one function, action in verb, context before new).
* **Word-choice rules (Lipton / Steinhardt / Perez):** be specific, eliminate hedging, avoid incremental vocabulary ("combine/modify/expand" → "develop/propose/introduce"), delete intensifiers, minimize pronouns, unfold apostrophes, delete filler words, keep terminology consistent.
* **Experiments section requirements:** for each experiment state what claim it supports, how it connects to the contribution, the setting, and what to observe; plus error bars with methodology, hyperparameter search ranges, compute infrastructure, seed-setting.
* **Related work:** organize methodologically, not paper-by-paper (with a good/bad example pair); "Cite generously—reviewers likely authored relevant papers."
* **Limitations section marked REQUIRED**, framed as pre-empting criticism rather than inviting it; NeurIPS/ICML/ICLR paper checklists flagged as mandatory, with `references/checklists.md`.
* A **reviewer criteria + NeurIPS 6-point scale** table (6 Strong Accept … 1 Strong Reject) and pointer to `references/reviewer-guidelines.md`.

**LaTeX/BibTeX handling.** Workflow 4 (template setup, 6 checked steps) plus Workflow 3 (format conversion, 6 checked steps). Hard rules: **copy the ENTIRE template directory, never just `main.tex`**; **compile the unmodified template before making any change** (`latexmk -pdf main.tex`, or `pdflatex → bibtex → pdflatex ×2`); keep template example content commented as a formatting reference until the end; **never edit `.sty` files**; **never copy LaTeX preambles between templates** (copy only content sections, figures, tables, and bibliography entries); a 5-row "template pitfalls" table; a per-conference template file table (`neurips2025`→`neurips.sty`; `icml2026`→`example_paper.tex` + `icml2026.sty`; `iclr2026`→`iclr2026_conference.tex`; `acl_latex.tex`; `aaai2026-unified-template.tex`; `colm2025_conference.tex`); a conference page-limit/requirement table (NeurIPS 2025 9pp + checklist; ICML 2026 8pp +1 broader impact; ICLR 2026 9pp +1 + LLM disclosure; ACL 8pp + mandatory limitations; AAAI 7pp +1; COLM 9pp +1); and convention tables for `\method`/`\eg`/`\ie`/`\etal` macros and `booktabs` table style (bold best value, ↑/↓ direction symbols, right-aligned numerics, consistent precision).

**Figures:** vector PDF/EPS for plots, PNG 600 DPI only for photographs, colorblind-safe palettes (Okabe-Ito or Paul Tol), verify grayscale readability (8% of men have CVD), no title inside the figure, self-contained captions.

#### `20-ml-paper-writing/systems-paper-writing/SKILL.md` (v1.1.0, MIT)

The most *structurally prescriptive* writing artifact across all three repos — a page-budget and paragraph-level blueprint for 10–12-page systems papers (OSDI, SOSP, ASPLOS, NSDI, EuroSys).

**Page allocation table:** Abstract ~0.25 · S1 Introduction 1.5–2 · S2 Background & Motivation 1–1.5 · S3 Design 3–4 · S4 Implementation 0.5–1 · S5 Evaluation 3–4 · S6 Related Work 1 · S7 Conclusion 0.5 ≈ 12 pages (USENIX 12 submission / 14 camera-ready; ACM ASPLOS 11 / 13).

**Per-section paragraph blueprints**, each with an authoritative-source attribution (Levin & Redell SOSP'83; Irene Zhang; Gernot Heiser; Timothy Roscoe; Mike Dahlin; Yi Ding; hzwer & DingXiaoH). Highlights:
* Abstract: a literal **5-sentence template** (problem context → gap → key insight → approach+results → impact).
* Introduction: 4-paragraph structure — problem statement ~0.5p, **gap analysis enumerating G1–Gn**, key insight as the **"X is better for applications Y running in environment Z"** formula, numbered contributions 3–5 each mapping to a section.
* Design: architecture diagram *first* ("draw a picture first"), module-by-module with alternatives considered, then an explicit **design alternatives and trade-offs** subsection.
* Evaluation: setup / end-to-end / microbenchmarks+ablation / scalability, plus the standout rule — **state every experimental conclusion three times**: as a hypothesis in the section opening ("We expect X to outperform Y because…"), as the result in the section closing ("Results show X outperforms Y by Z%"), and as evidence in the figure caption ("Figure N shows X achieves Z% better throughput than Y").

**Four reusable writing patterns** with worked paper examples: Gap Analysis (Lucid, ASPLOS'23: G1–Gn → A1–An), Observation-Driven (GFS: O1–O3 → design insights), Contribution List (Blox EuroSys'24; Sia SOSP'23), Thesis Formula (Irene Zhang).

**Quality self-check adapted from Levin & Redell — six dimensions:** Original Ideas, Reality (is it built?), Lessons (what did you learn?), Choices (alternatives discussed?), Context (related work fair?), Presentation.

**Venue table** (format, submission limit, camera-ready, references) for OSDI/NSDI/SOSP/ASPLOS/EuroSys, with a repeated **temporal-validity warning**: "Venue rules change yearly. Always verify against the current year's CFP."

**Academic-integrity section** restates the no-fabrication rules (no fabricated production observations/traces/deployment experiences/results, no fake venue rules or best-paper claims, no paragraph-level copying from reference papers) and defers citation verification to `ml-paper-writing`. Ships `references/section-blueprints.md`, `references/writing-patterns.md`, `references/checklist.md` (a **7-stage pre-submission checklist**), `references/systems-conferences.md`, `references/reviewer-guidelines.md`, and four venue LaTeX templates (`osdi2026`, `nsdi2027`, `asplos2027`, `sosp2026`) — all listed in the marketplace but **template contents not fetched → UNVERIFIED**.

#### `21-research-ideation/brainstorming-research-ideas/SKILL.md` (v1.0.0, MIT)

Ten named ideation lenses, each with a workflow and self-check: (1) Problem-First vs Solution-First, (2) the Abstraction Ladder (up/down/sideways), (3) Tension & Contradiction Hunting with a 6-row tension table, (4) Cross-Pollination/Analogy Transfer (with a source-field→concept table and the requirement of structural fidelity + non-obviousness + testable predictions), (5) the "What Changed?" principle (compute/scale/regulation/tooling/failure/cultural), (6) Failure Analysis & Boundary Probing (distributional/scale/adversarial/compositional/temporal), (7) the Simplicity Test, (8) Stakeholder Rotation (end user/developer/theorist/adversary/ethicist/regulator/operator), (9) Composition & Decomposition, (10) the "Explain It to Someone" two-sentence template. These compose into a three-phase end-to-end workflow — **Phase 1 Diverge (10–20 candidates) → Phase 2 Converge (5 named filters with explicit "kill criteria") → Phase 3 Refine (six concrete steps + completion checklist)** — plus a "framework selection guide" that maps a user's situation to a starting lens, and a pitfalls table. Also ships an explicit non-use rule (do not use for experimental design — use domain skills).

---

## 3. Master-cai/Research-Paper-Writing-Skills

### 3.1 Repository facts

| Field | Value (verified) |
|---|---|
| owner/repo | `Master-cai/Research-Paper-Writing-Skills` |
| URL | https://github.com/Master-cai/Research-Paper-Writing-Skills |
| Stars / forks | 7,219 / 342 |
| License | MIT |
| Created / last push | 2026-03-05 / 2026-06-23 |
| Repo description | "Skill package for ML/CV/NLP paper writing, curated and adapted from Prof. Peng Sida's open notes for Codex, Claude Code, and Gemini." |
| Attribution | README states most writing knowledge comes from Prof. Peng Sida's open notes (`https://pengsida.notion.site/...`) and `github.com/pengsida/learning_research`; the author's contribution is "organization, structured adaptation, and packaging as reusable Skills" |
| Hosts supported | Codex (`$CODEX_HOME/skills/`), Claude Code (`~/.claude/skills/` or `.claude/skills/`), Gemini (`~/.gemini/skills/`) |

**Exact inventory — ONE skill package:** `research-paper-writing/`. Full verified file tree (from `git/trees/main?recursive=1`, `"truncated": false`):

```
research-paper-writing/SKILL.md                       (4,834 B)
research-paper-writing/agents/openai.yaml             (243 B)
research-paper-writing/references/abstract.md         (3,628 B)
research-paper-writing/references/conclusion.md       (1,244 B)
research-paper-writing/references/does-my-writing-flow-source.md (4,990 B)
research-paper-writing/references/experiments.md      (4,476 B)
research-paper-writing/references/introduction.md     (15,015 B)
research-paper-writing/references/method.md           (6,256 B)
research-paper-writing/references/paper-review.md     (5,442 B)
research-paper-writing/references/related-work.md     (1,283 B)
research-paper-writing/references/examples/index.md   (2,402 B)
research-paper-writing/references/examples/abstract-examples.md
research-paper-writing/references/examples/abstract/template-a.md, template-b.md, template-c.md
research-paper-writing/references/examples/introduction-examples.md
research-paper-writing/references/examples/introduction/
    novel-task-challenge-decomposition.md
    pipeline-not-recommended-abstract-only.md
    pipeline-version-1-one-contribution-multi-advantages.md
    pipeline-version-2-two-contributions.md
    pipeline-version-3-new-module-on-existing-pipeline.md
    pipeline-version-4-observation-driven.md
    technical-challenge-version-1-existing-task.md
    technical-challenge-version-2-existing-task-insight-backed-by-traditional.md
    technical-challenge-version-3-novel-task.md
    version-1-task-then-application.md
    version-2-application-first.md
    version-3-general-to-specific-setting.md
    version-4-open-with-challenge.md
research-paper-writing/references/examples/method-examples.md
research-paper-writing/references/examples/method/
    example-of-the-three-elements.md
    method-writing-common-issues-note.md
    module-design-instant-ngp.md
    module-motivation-patterns.md
    module-triad-neural-body.md
    neural-body-annotated-figure-text.md
    overview-template.md
    pre-writing-questions.md
    section-skeleton.md
```

No scripts, no LaTeX templates, no assets — it is pure prose guidance plus an example bank. That is its distinguishing trait: **the smallest and cheapest to port, and the most "writerly" of the three.**

### 3.2 What makes its paper-writing skill concrete and actionable

**`SKILL.md` — Core Workflow (quoted verbatim):**
```
1. Clarify the paper story before sentence-level edits.
2. Use section-specific guidance in `references/`.
3. Rewrite paragraph-by-paragraph with one message per paragraph.
4. Run reverse outlining after writing each section.
5. Check every major claim in Abstract/Introduction against experimental evidence.
6. Run final-paper adversarial review with `references/paper-review.md`.
```

**Global Principles (quoted):** one paragraph per message; state the paragraph message in the first sentence; make nouns self-contained and define terms before reuse; maintain sentence-to-sentence flow (cause, contrast, consequence, or refinement); iterate with adversarial self-review; "Treat visual quality as core content, not decoration"; clean teaser and pipeline figure; readable minimal-ink tables; consistent formatting.

**Paragraph Clarity Check (quoted structure):** (1) read as an external reader — does the paragraph have one explicit message, does the first sentence state what it will do, are key nouns readable without hidden context, does each sentence connect with a clear relation; (2) run **reverse outlining** — write the thesis/main claim, each paragraph's topic sentence, and the evidence under each paragraph, then check topic-sentence→thesis and evidence→topic-sentence mapping, and "Revise or remove any paragraph that cannot be mapped cleanly"; (3) if flow is still weak, add temporary section headers and explicit transition phrases, then remove unnecessary headers before finalizing.

**Execution Rules (quoted):** build a mini-outline before drafting prose; each subsection explicitly includes motivation, design and technical advantage where applicable; **avoid writing that looks like incremental patching of a naive baseline**; keep terminology stable across the paper; **"If a claim cannot be supported by results, weaken or remove the claim"**; append and answer a five-dimension self-review question list before finalizing; and a context-budget rule — **"Do not load all section references at once; load only the specific section guide needed for the current edit target."**

**Output Contract (quoted) — the mechanism I would port first.** Every rewrite request must return:
```
1. A compact section outline (3-7 bullets).
2. Revised paragraphs with explicit paragraph roles
   (opening/challenge/method/advantage/evidence/limitation).
3. A short self-review checklist covering clarity, flow, terminology consistency,
   unsupported claims, and missing evidence.
4. A claim-evidence map for each major claim in the revised text using
   Claim: ... | Evidence: ... | Status: supported/needs evidence.
```
This is a tiny, portable, machine-checkable output schema imposing a claim↔evidence map on every writing turn — the same idea as K-Dense's claim registry, but with zero infrastructure.

**`references/paper-review.md` — the adversarial review gate (quoted):**
* Goal: "Use an adversarial, reviewer-style checklist to detect reject risks early and revise the paper before submission." Core principle: "assume reviewers will probe every weak point and proactively fix them."
* **Critical Rule (Do Not Violate):** every major claim, especially in Abstract and Introduction, must be (1) technically correct and (2) explicitly supported by experimental evidence — "If a claim is not supported, either add evidence or weaken/remove the claim."
* **What usually gets a paper accepted:** sufficient contribution (novel task / pipeline / module / design choices / experimental findings / insight); better empirical performance under fair comparisons; sufficient comparison experiments and ablations.
* **Common Rejection Dimensions table** — 5 dimensions each with numbered failure signals: 1 Insufficient contribution (targeted failure cases too common; technique already well explored / predictable gains); 2 Unclear writing (missing details, not reproducible; a module lacks clear motivation); 3 Weak empirical effect (only marginal improvement; absolute performance not strong enough); 4 Incomplete evaluation (missing ablations; missing important baselines or metrics; datasets too simple); 5 Problematic method design (unrealistic setting; technical flaws; not robust / needs per-scenario hyperparameter tuning; new design introduces stronger limitations than benefits → negative net value).
* **End-of-Paper Self-Review Question List** — exactly 5 dimensions × 4–5 questions, appended near the end of the draft: **Contribution** ("What new knowledge does this paper give to readers?"; "Is our gain surprising or insightful rather than a predictable improvement?"), **Writing Clarity** (reproducible method; enough detail per module; explicit motivation per module; notation consistency; one message per paragraph), **Experimental Strength** (meaningful vs statistically tiny improvement; absolute performance competitive; gains consistent across datasets/settings/metrics; report both strengths and failure cases honestly), **Evaluation Completeness** (ablations for all key design choices; all strong/recent baselines under fair settings; standard sufficient metrics; challenging datasets; documented protocols), **Method Design Soundness** (realistic setting; hidden defects/unreasonable assumptions; robustness without per-case retuning; benefits outweigh added complexity; could reviewers argue net benefit is negative).
* **Adversarial Writing Workflow (quoted):** "1. Read the paper as a skeptical reviewer. 2. Answer every question above with explicit evidence from the paper. 3. Mark each item as `pass`, `needs revision`, or `needs new experiment`. 4. Revise claims, writing, experiments, or method scope accordingly. 5. Repeat until no major rejection risk remains."

That three-state marking (`pass` / `needs revision` / `needs new experiment`) is the crispest triage vocabulary of the three repos and maps directly onto a fix-type decision.

**Section-specific references** (contents not fetched → coverage UNVERIFIED beyond the SKILL.md's own description): `introduction.md`, `abstract.md`, `related-work.md`, `method.md`, `experiments.md`, `conclusion.md`, plus a **concrete example bank** organized by paper archetype — an abstract template set (a/b/c) and 14 introduction patterns named by strategy (`pipeline-version-1-one-contribution-multi-advantages`, `technical-challenge-version-3-novel-task`, `version-4-open-with-challenge`, and an explicitly negative example `pipeline-not-recommended-abstract-only`), plus method-writing assets (`overview-template.md`, `module-triad-neural-body.md`, `neural-body-annotated-figure-text.md`, `pre-writing-questions.md`, `section-skeleton.md`, a real `module-design-instant-ngp.md` case study, and `method-writing-common-issues-note.md`).

---

## 4. Cross-repo synthesis — what to port into a new skill pack

Ranked by value per unit of integration effort.

**Tier 1 — verification gates (all three repos agree these matter; K-Dense and Orchestra have working designs):**
1. **Claim↔evidence registry with IDs and a hash of claim text** (K-Dense `scientific-writing`): cheap, single-file, deterministic, and it makes "unsupported claim" a mechanical failure rather than a judgement call. Port the `E`/`C`/`N`/`M`/`O`/`R` ID scheme and the `[claim:C001] [evidence:E001,E002]` inline marker.
2. **Never-generate-BibTeX-from-memory gate with a 2-source existence check + claim-level verification + mandatory `[CITATION NEEDED]` placeholder + explicit user notice** (Orchestra `ml-paper-writing`). Highest signal-to-effort ratio in the whole survey.
3. **Git-protocol-before-results as lightweight pre-registration**, plus CONFIRMATORY vs EXPLORATORY labelling (Orchestra `autoresearch`).
4. **Non-scoring validators** — state, in the skill itself, that the checker does not certify quality/compliance/acceptance, and that a human must open every source (K-Dense, applied consistently across skills).
5. **Fail-closed scaffolding** that never overwrites and emits placeholders the linter rejects (K-Dense).

**Tier 2 — output contracts and rubrics:**
6. **A mandatory structured output contract** — outline + role-tagged paragraphs + self-review checklist + `Claim | Evidence | Status` map (Master-cai). Nearly free to adopt, immediately visible to users.
7. **A 5-dimension adversarial self-review question list appended to the draft**, with three-state marking `pass / needs revision / needs new experiment` (Master-cai), and a rejection-dimension table so the model can *name* the risk class.
8. **A 6-dimension 1–5 numeric rubric with per-level scoring anchors, a mean-plus-floor grade function, severity-ranked findings each carrying a verbatim evidence span, and a fixed JSON schema** (Orchestra `rigor-reviewer`). The strongest reusable rubric design; note the "no false grounding" rule (agreement in prose never substitutes for experimental evidence) and the "most competent artifacts land 3–4" calibration.
9. **Type-aware entailment** for evidence sufficiency (causal claim → needs an isolating ablation; generalization claim → needs heterogeneous conditions; etc.). Portable as a small table and it catches the most common AI over-claim.

**Tier 3 — process/architecture:**
10. **Two-loop orchestration with a role statement** ("you orchestrate; domain skills execute"), a routing table, and four named outer-loop directions (DEEPEN/BROADEN/PIVOT/CONCLUDE) with criteria (Orchestra `autoresearch`).
11. **Persistent state files as cross-session memory** (`research-state.yaml`, `research-log.md`, `findings.md` with a **Lessons and Constraints** section) plus the stated quality test that findings.md must be sufficient to write the abstract from after N experiments.
12. **Skills load one reference at a time** ("Do not load all section references at once") — a context-budget rule, not just a style rule (Master-cai; K-Dense uses the same consolidation logic in `database-lookup`).
13. **Wall-clock continuity loop** (`/loop` or a 20-minute cron bound to the session) with a verify-it-exists step, explicitly decoupled from research phases (Orchestra `autoresearch`).
14. **Prescriptive structural blueprints with page budgets and paragraph counts per section, plus the "state each eval conclusion three times (hypothesis / result / caption)" rule** (Orchestra `systems-paper-writing`) — and its counterweight, the repeated temporal-validity warning to re-verify venue rules against the current CFP.
15. **LaTeX/BibTeX hygiene rules** if the pack ships templates: copy the whole template dir, compile unmodified first, never edit `.sty`, never copy preambles between templates, keep example content commented until the end (Orchestra `ml-paper-writing`).

**Anti-patterns to avoid (documented, not invented):**
* Shipping a generic polished template that lets plausible placeholders ship (K-Dense removed its LaTeX assets for exactly this reason).
* Letting a generic image model redraw data figures (K-Dense `scientific-slides`: attachments "can redraw points, axes, labels, and logos" — embed originals or regenerate deterministically).
* Treating DOI existence as claim support (K-Dense `literature-review`).
* Treating "no prior work found" as novelty (K-Dense `hypothesis-generation`: say "not located within the documented search boundary").
* Documented inventory drift (Orchestra) — if your pack advertises a skill count, add a CI check that counts `SKILL.md` files, and keep the marketplace/CLI/README in one source of truth.

---

## Appendix — verification log

Fetched 2026-10-03 (all HTTP 200 unless noted). Untrusted page content was used as data only.

**K-Dense-AI/scientific-agent-skills**
* `api.github.com/repos/K-Dense-AI/scientific-agent-skills` — stars 47,458; forks 4,288; license MIT; created 2025-10-19; pushed 2026-10-01
* `raw.githubusercontent.com/K-Dense-AI/claude-scientific-skills/main/README.md` — served the Scientific Agent Skills README (rename confirmation)
* `raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/README.md` — 177 skills, version 2.72.0, categories, testing/security process, citation
* `api.github.com/repos/K-Dense-AI/scientific-agent-skills/git/trees/main:skills` — **177 immediate child directories, `"truncated": false`**
* `.../main/skills/scientific-writing/SKILL.md` — v2.3, 12-step workflow, scripts/assets/references lists
* `.../main/skills/literature-review/SKILL.md` — v1.11, 7 phases
* `.../main/skills/hypothesis-generation/SKILL.md` — v2.4, 12 steps, CLI exit codes
* `.../main/skills/research-grants/SKILL.md` — v1.5, 5 phases, agency rules
* `.../main/skills/statistical-analysis/SKILL.md` — v2.0, 6 steps, integrity list
* `.../main/skills/scientific-slides/SKILL.md` — v1.12
* `.../main/skills/paper-to-slides/SKILL.md` — **HTTP 404 (skill does not exist)**

**Orchestra-Research/AI-Research-SKILLs**
* `api.github.com/repos/Orchestra-Research/AI-Research-SKILLs` — stars 13,213; forks 935; license MIT; created 2025-11-03; pushed 2026-06-16; language TeX
* `raw.githubusercontent.com/Orchestra-Research/AI-Research-SKILLs/main/README.md` — claimed 98/90/87 counts, category table, changelog
* `.../main/.claude-plugin/marketplace.json` — 23 plugin categories, 96 listed skill directories (primary inventory source)
* `.../main/0-autoresearch-skill/SKILL.md` — two-loop architecture, git protocol, continuity loop, routing
* `.../main/20-ml-paper-writing/SKILL.md` — HTTP 404 (category dir, not a skill)
* `.../main/20-ml-paper-writing/ml-paper-writing/SKILL.md` — v1.2.0, workflows 0–4, citation gate
* `.../main/20-ml-paper-writing/systems-paper-writing/SKILL.md` — v1.1.0, page blueprint, patterns
* `.../main/21-research-ideation/brainstorming-research-ideas/SKILL.md` — v1.0.0, 10 lenses
* `.../main/22-agent-native-research-artifact/rigor-reviewer/SKILL.md` — v3.0.0, D1–D6 rubric, grade formula
* `api.github.com/repos/.../contents/20-ml-paper-writing` — confirms 4 subdirectories
* `api.github.com/repos/.../git/trees/main:packages/ai-research-skills` and `.../src` — file listing only
* `.../main/packages/ai-research-skills/src/installer.js` — `getAllCategoryIds()` returns 22 categories (omits `22-agent-native-research-artifact`)

**Master-cai/Research-Paper-Writing-Skills**
* `api.github.com/repos/Master-cai/Research-Paper-Writing-Skills` — stars 7,219; forks 342; license MIT; created 2026-03-05; pushed 2026-06-23
* `raw.githubusercontent.com/Master-cai/Research-Paper-Writing-Skills/main/README.md` — single skill package, attribution to Prof. Peng Sida, install paths
* `.../main/research-paper-writing/SKILL.md` — workflow, global principles, output contract
* `.../main/research-paper-writing/references/paper-review.md` — rejection dimensions, self-review question list, adversarial workflow
* `api.github.com/repos/Master-cai/Research-Paper-Writing-Skills/git/trees/main?recursive=1` — full file tree, `"truncated": false`

**Disambiguation check**
* `api.github.com/repos/SNL-UCSB/paper-writing-skill` — 230 stars, MIT, created 2026-03-25 (considered and rejected as the item-3 match)

### Explicitly UNVERIFIED items
* Orchestra total skill count — four in-repo sources disagree (98 / 90 / 87 / 96). Not settled.
* Contents of Orchestra skills `academic-plotting`, `presenting-conference-talks`, `compiler`, `research-manager`, `creative-thinking-for-research`, and every domain skill listed in §2.2 — only existence/path verified.
* Contents of K-Dense skills listed by name but not fetched (`peer-review`, `citation-management`, `venue-templates`, `research-lookup`, `scientific-schematics`, `pptx-posters`, `latex-posters`, `statistical-power`, `experimental-design`, `scientific-critical-thinking`, `scientific-brainstorming`, `scholar-evaluation`, all domain skills) — names verified from the git tree; descriptions are the README's, not the skills' own text.
* Contents of Master-cai's seven section reference files and the example bank — only paths, byte sizes and the SKILL.md's own summary descriptions verified.
* Orchestra's LaTeX template directories (`osdi2026`, `nsdi2027`, `asplos2027`, `sosp2026`, and the six ML/AI conference templates) — listed in the skills' own text; files not fetched.
* Per-skill sub-licenses in the K-Dense repo — the README warns they may differ from MIT; only `scientific-writing`, `literature-review`, `hypothesis-generation` (MIT) and `statistical-analysis`, `research-grants`, `scientific-slides` (MIT) were individually read.
