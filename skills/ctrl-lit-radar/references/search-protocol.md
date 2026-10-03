# Search protocol and source access

How to reach each index, what its fields mean, and where each source is weaker than it looks. This
file contains no credentials and assumes none. Anything requiring a paid seat is described as such
and is used through the user's own institutional session, never through a key written into a file.

## Source map

| Source | Coverage strength | Weakness to compensate for | Access |
|---|---|---|---|
| arXiv API | fast preprint coverage in cs.CV, cs.RO, eess.SY, eess.SP, math.OC | not peer reviewed; versions drift; withdrawn papers linger; an identifier without a version is ambiguous | public, no key |
| OpenAlex | broad metadata, citation graph, institution and funder links | metadata-level only; author disambiguation errors; abstract text sometimes truncated | public, polite pool with a contact mailto |
| Semantic Scholar Graph API | good CS coverage, citation context | rate limited without a key; occasional duplicate records; abstracts may be missing | public tier is rate limited |
| Crossref | authoritative DOI, volume, pages, journal record | no abstracts for many records; published record lags the preprint by months | public, no key |
| PubMed | biomedical and some sensing or imaging work | near-empty for control, robotics and vision venues | public, no key |
| IEEE Xplore | the venue of record for TAC, T-RO, RA-L, TGRS and most of class B and C | the search surface is the weakest link for bulk work; metadata only without a subscription | user's institutional session |
| DBLP | clean venue and author records for CS | bibliographic only, no abstracts | public, no key |
| CNKI, 万方, 维普 | 自动化学报, 控制理论与应用 and other Chinese venues | metadata and abstracts are often gated; 创新点 statements live in the Chinese abstract | user's institutional session |
| Publisher sites | the version of record, the exact table, the supplement | paywalls; final numbers may differ from the arXiv version | user's institutional session |

## The intended combination

No single index is sufficient, and the failure mode is asymmetric. arXiv misses work published
directly in journals by control and remote-sensing groups. Crossref and DBLP find the record but
carry no abstract. OpenAlex and Semantic Scholar connect the citation graph but misattribute authors.
IEEE Xplore holds the version of record but is awkward for bulk queries.

Recommended division of labour.

1. **Discovery.** arXiv plus OpenAlex plus Semantic Scholar. Recall matters more than precision here.
2. **Record resolution.** Crossref or DBLP to fix the DOI, venue, volume and pages of anything that
   survives.
3. **Version of record.** IEEE Xplore, publisher site, or the user's library session, to read the
   table a number will come from.
4. **Chinese-language sweep.** CNKI or 万方 for the class D venues, using the Chinese query set in
   [query-recipes.md](query-recipes.md), because the English indexes index these venues poorly.

## Protocol notes per source

### arXiv

- Prefer the versioned identifier in the ledger (`arXiv:2111.14690v3`) and record the version you
  read. A later version can change a number that a claim depends on.
- Use the abstract page to confirm the title, authors, and version history, and to detect a
  withdrawal notice. Do not treat the absence of a withdrawal notice as proof the paper is current.
- Category choice is a filter with a cost. `cs.CV` will not surface an `eess.SP` filtering paper
  that is directly relevant to `filt`.
- A preprint is `reported` evidence at best, and its venue status must be stated. Never cite a
  preprint as if it were the peer-reviewed record when both exist.

### OpenAlex

- Use a contact address in the query so the request enters the polite pool. This is a courtesy, not
  a key, and it is fine to write into a script.
- `is_retracted` and the retraction fields are worth checking on anything central to the claim.
- Author identity clusters are unreliable. Confirm the author list against the publisher record
  before attributing a result to a group.

### Semantic Scholar

- The public tier is rate limited. Space the requests and cache responses locally under `lit/`.
- `citationContext` is useful for finding what a citing paper says about a method, but that sentence
  is a secondary source. Any number quoted from it is `reported` and must name the citing paper.
- Do not use the "influential citation" flag as a quality signal. It measures graph structure, not
  correctness.

### Crossref

- The typed metadata is the most trustworthy part. Use it to settle a disputed year, page range or
  venue name.
- Abstract coverage is uneven, and a missing abstract means nothing about the paper's content.

### IEEE Xplore

- Treat the HTML page as the authority for the version of record when a preprint also exists.
- Confirm the venue string exactly, including the track or special-issue name, before writing a
  venue fit statement.
- The user's session, not an API key, is the expected access path.

### Chinese-language sources

- Search the Chinese term set, not a translation of the English one. 协同导航 and cooperative
  navigation retrieve different corpora.
- Record 中图分类号 when it is available. It is a reliable axis hint for a domestic venue paper.
- For a domestic venue, the 创新点 list in the Chinese abstract is often the paper's own claim
  inventory and is the fastest way to see whether the work overlaps.

## Credential and access policy

- No API key, token, cookie or password is written into a skill file, a search script, or an
  artifact. If a source needs one, the user supplies the session.
- If an endpoint requires a key that the user has not provided, mark the source `[UNVERIFIED]` for
  that expansion and record which source was unavailable. Do not silently drop it.
- Respect rate limits and terms of service. A bulk harvest that violates the terms of service puts
  the resulting paper at risk and is not a shortcut worth taking.
- Never scrape a gated full text. If a paper is paywalled and the user has no access, grade it
  `abstract only` and let the claim that needed it be downgraded.

## Failure handling

| Symptom | Meaning | Action |
|---|---|---|
| endpoint returns nothing for a query that should match | query or field filter is wrong, or the coverage gap is real | re-run once with a broader field filter, then record a coverage gap |
| the same work under two identifiers | preprint and record pair, or a duplicate record | merge into one ledger row with both identifiers, keep the version of record as the citable one |
| abstract present, full text inaccessible | depth limit | grade `abstract only`, mark dependent claims `[UNVERIFIED]` |
| a claim's cited source cannot be retrieved at all | the claim is unsourced | remove the claim or replace the source; do not keep it with a soft hedge |
| a value differs between preprint and record | version drift | cite the version of record and report the drift if the number is central |
