# Venue cycle tracking

A target venue is a moving object. Tracks appear, deadlines move, page limits shrink, anonymity rules
flip, and preprint policies change. This file describes how to track the cycle without carrying stale
facts into a plan.

[../../ctrl-shared/core/venue-matrix.md](../../ctrl-shared/core/venue-matrix.md) holds the venue
classes and what their reviewers weight. That file is a planning aid and it says so. This file is the
procedure for turning it into a date-stamped decision.

## The rule that governs everything here

Any venue fact that will appear in a plan, a cover letter, a formatting decision or a submission
checklist is verified at the venue's own site, at the time of use, and is recorded with the date it
was checked and the exact document or page checked. A venue fact from memory, from a colleague, from
a blog post, or from this pack is `[UNVERIFIED]`.

## What to verify, in order

```markdown
## Venue check: <venue and year>
- Checked on: <date, with time zone>
- Source: <exact URL or document title and version>
- Track: <main conference | journal | special issue | workshop, with the exact track name>
- Primary deadline: <date and time zone, plus the abstract deadline if separate>
- Rebuttal or author-response window: <date range, or "not applicable">
- Notification and camera-ready dates: <dates>
- Page limit: <number, and whether references count>
- Format: <template name and version>
- Anonymity: <double-blind | single-blind | none>, and whether the supplementary or code link must
  be anonymised
- Preprint policy: <permitted | not permitted | unclear>, with the exact clause
- Supplementary and code policy: <required | optional | not accepted>
- AI-use disclosure: <required | not required | prohibited>, with the exact clause
- Open-access or APC obligation: <amount or "none", and who pays>
- Verified by: <who checked>
```

Anything left blank is an open item, not a default. In particular, "page limit: 8 pages, references
not counted" is a claim that must be read off the current author instructions, because that clause
changes between cycles and venues in the same family.

## Cycle tracking across venues

Maintain one row per candidate venue so the cycle can be compared on lead time rather than on
prestige. The plan is only viable if the notification date lands before the funding or graduation
milestone.

```markdown
| Venue | Class | Next deadline | Notification | Camera ready | Lead time from today | Fit verdict |
|---|---|---|---|---|---|---|
| <name year> | A/B/C/D | <date> | <date> | <date> | <weeks> | <strong | weak | reject> |
```

Lead time is the deciding number more often than fit is. A venue whose decision arrives after the
milestone is not a plan regardless of its class. Record the milestone date in the same table so the
comparison is visible.

## Class-specific checks

### Class A, vision and machine learning

- Verify the anonymity rule and the supplementary policy, because vision venues differ on whether a
  code link may be included and whether it must be anonymised.
- Verify the page limit against the number of figures the contribution needs. A paper whose mechanism
  requires four figures is a different length problem than one that needs two.
- Check the rebuttal format. A venue without a rebuttal makes every unresolved concern permanent,
  which changes how much must be pre-empted in the submission itself.
- Check the pre-print policy explicitly. Some venues treat a preprint as prior art and others do not.

### Class B, control, robotics and navigation

- Journals in this class have no deadline, so the binding constraint is the review duration and the
  revision cycle. Record the expected time to first decision if the venue publishes it.
- Verify the length policy carefully. TAC and Automatica style venues have note and paper categories
  with different limits and different expectations of proof detail.
- For robotics venues, verify the hardware-evidence expectation and whether a video is required or
  permitted, because a video submission can change the anonymity situation.
- Check whether the venue expects a comparison against a specific reference implementation.

### Class C, remote sensing

- Verify whether the venue requires a geo-aware split description and whether it has a reproducibility
  or data-availability requirement.
- Check the page limit and the figure budget, because remote-sensing results often need large
  multi-panel figures.
- Verify whether the venue allows an evaluation-server number without local test labels, since some
  do and the resulting claim differs.

### Class D, Chinese-language journals

- Verify the current 投稿指南 for: the 中英文摘要 requirement, the 创新点 statement requirement, the
  基金项目 acknowledgment format, the 中图分类号 and 文献标识码 fields, and the GB/T 7714 reference
  format edition. GB/T 7714-2025 replaced GB/T 7714-2015 on 2026-07-01; a journal may still name the
  older edition during transition, and its own instruction wins.
- Verify the review cycle length. Domestic venues often publish an expected 审稿周期, and it may
  exceed an English venue's full cycle.
- Check whether the venue requires a 保密审查 or a 单位介绍信 for certain topics, which is a real
  schedule risk for navigation and aerospace work.
- Confirm the processing fee position (版面费) and whether it depends on page count or color figures.

## Re-verification triggers

Re-verify a venue fact when any of these occurs, rather than on a fixed schedule.

- A new cycle's call for papers is posted, which is the normal case for conference venues.
- The plan's claim type or axis changes, which can change the venue class.
- The manuscript length changes materially.
- A review round completes and the revision target is reset.
- The user's deadline or funding milestone moves.
- Any fact about the venue is about to be written into a cover letter or a formatting decision.

## Failure handling

| Symptom | Meaning | Action |
|---|---|---|
| the call for papers page is not reachable | the cycle may not be open, or the site moved | check the parent society or publisher page, and mark the venue `[UNVERIFIED]` until confirmed |
| two documents give different page limits | an outdated page is live, or the template and the call disagree | use the most recently dated official document, record both, and ask the venue if the difference is material |
| the deadline time zone is unstated | a real risk of a missed deadline by hours | plan against the earliest plausible instant, such as the venue's local time or UTC rather than Anywhere on Earth (UTC-12), ask the venue, and record the assumption |
| the venue has moved to a new submission system | the account and the previous submission history may not carry over | create the account early, and treat the deadline as earlier than stated |
| the preprint policy is unclear | cannot be resolved by reading | state the limit, do not post, and record the open question |

## Handoff

The verified venue block supplies the G0 target-venue field and the G3 venue-fit statement. Do not
write a venue fit statement from an unverified venue block, and do not let a fit statement borrow
language from a call for papers without quoting it as the venue's own words.
