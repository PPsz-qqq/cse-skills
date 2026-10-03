# Venue matrix for control science and engineering

Use this file to choose, justify, and write toward a target venue. It records the venue *class*,
what its reviewers actually weight, and the evidence each class expects.

**Currency warning.** Venue names, tracks, page limits, deadlines, anonymity rules, and
supplementary-material policies change every cycle. This file is a planning aid, not an
authority. Always verify against the current official call for papers or author guidelines
before formatting a submission, and record the version of the guidelines you used. Where this
file conflicts with the official call, the official call wins.

Verification status: venue names and publishers in the tables were checked against official
publisher, society or IEEE Xplore pages on 2026-10-03. The "weight" and "evidence bar" columns are
this pack's planning guidance, not statements of any venue's policy.

## How to choose, in order

1. Fix the claim type from `ctrl-shared` G0. A theory result, an empirical delta, a system
   demonstration, and a survey have almost disjoint venue sets.
2. Match the claim to the venue's stated contribution criteria, in the venue's own words.
3. Check the evidence bar you must clear. If the venue requires real-world validation and you
   have simulation only, either change venue or add the validation; do not blur the gap.
4. Check the review-cycle cost against the deadline. A venue whose next deadline is after your
   funding or graduation milestone is not a plan.
5. Prefer the venue where a reviewer drawn from its own program committee would already believe
   the premise. Explaining a premise costs pages you do not have.

## Class A: top-tier computer vision and machine learning

Applies to `det`, `track`, `reid`, and the learning-heavy end of `cnav` and `filt`.

| Venue class | Axis fit | Contribution the reviewers weight | Evidence bar |
|---|---|---|---|
| CVPR, ICCV, ECCV | the three vision axes (`det`, `track`, `reid`) | new problem, new mechanism, or a decisive empirical result; strong visual results | multi-dataset or multi-benchmark; ablations; leaderboard-grade numbers; code expected |
| NeurIPS, ICML, ICLR | `filt`, `cnav` theory and learning; `det`/`track` if method-driven | novelty of the formulation or the learning principle; theory or strong generality | rigorous baselines, seeds, compute disclosure; theory needs proof |
| AAAI, IJCAI | all axes | solid contribution with clear framing | broad but slightly lower empirical bar than CVPR-class |
| WACV, BMVC, ACCV | the three vision axes (`det`, `track`, `reid`) | complete, honest, well-evaluated work | one strong benchmark plus ablations is often enough |
| T-PAMI, IJCV | the three vision axes (`det`, `track`, `reid`) | journal-depth: extended analysis, broader validation | substantial extension beyond any conference version is mandatory |
| IEEE TIP, IEEE TCSVT, Pattern Recognition, IEEE TMM, IEEE TIFS | `det`, `track`, `reid` (TIFS often for person re-identification and surveillance) | sound method with thorough evaluation; journal-length analysis | multi-dataset evaluation, ablations, fair baselines; check each journal's conference-extension policy |

Reviewer behaviour to plan for: this class rejects on perceived novelty first, then on
unfair or thin comparison, then on missing ablations. A negative attitude toward "yet another
module" is common, so the G0 mechanism-versus-delta distinction decides the framing.

## Class B: control, estimation, robotics, and navigation

Applies primarily to `cnav` and `filt`.

| Venue class | Axis fit | Contribution the reviewers weight | Evidence bar |
|---|---|---|---|
| IEEE TAC, Automatica | `filt` theory, `cnav` theory | stability, convergence, optimality, or a new estimation-theoretic result | proofs, assumptions stated, simulations as illustration only |
| IEEE TSP, Signal Processing | `filt` | estimator design, bounds, performance analysis | CRLB or covariance analysis, Monte Carlo consistency |
| IEEE T-RO, RA-L, ICRA, IROS | `cnav`, `filt` on real platforms | system that works on hardware; real-robot validation | field or hardware experiments, sensor calibration, failure cases |
| IEEE TAES, Aerospace | `cnav`, `filt` in aerospace settings | navigation, guidance, integrity, fault detection | realistic scenarios, GNSS-denied or degraded conditions |
| IFAC World Congress, IFAC journals, CDC, ACC | `filt`, `cnav` | methodological control contribution | theory plus simulation, hardware optional |
| IEEE T-ITS, ITSC, IV | `det`, `track`, `reid` in traffic; `cnav` for vehicles | transportation-specific impact and datasets | dataset realism, vehicle-platform validation |
| IEEE Sensors Journal, Measurement | `filt`, `cnav` sensing | sensor system, calibration, fusion architecture | bench validation, error characterization, repeatability |
| NAVIGATION (Journal of the Institute of Navigation, ION), GPS Solutions, ION GNSS+, IEEE/ION PLANS, IET Radar, Sonar & Navigation | `cnav`, `filt` for positioning, navigation and timing | GNSS, inertial and multisensor PNT, integrity, cooperative positioning | real or recorded sensor data, error budgets, comparison with established PNT baselines |
| Information Fusion (Elsevier), International Conference on Information Fusion (FUSION, ISIF) | `filt`, `track`, `cnav` fusion | fusion architectures, multi-target tracking, distributed estimation | consistency evidence, Monte Carlo design, fusion-rule correctness (for example cross-covariance handling) |
| IEEE TNNLS, IEEE Transactions on Cybernetics, IEEE TII, IEEE TIE, IEEE TASE, IEEE/CAA Journal of Automatica Sinica | all axes when framed as learning, control or industrial systems | method plus control, learning or industrial relevance | stability or convergence arguments where claimed, application validation |
| Chinese Journal of Aeronautics, Science China Information Sciences | `cnav`, `filt`, aerospace `det` and `track` | English-language aerospace or information-science contributions, published in China | as for the matching class B or A venue |
| IEEE T-IV, IEEE TVT, IEEE Internet of Things Journal | `cnav` and `det`/`track` on vehicles, V2X and networked agents | vehicular or networked-system relevance | platform or network realism, communication assumptions stated |

Reviewer behaviour to plan for: this class rejects on unstated assumptions, missing proof
details, comparisons to a straw-man baseline, and simulation-only claims dressed as system
claims. Consistency and bound checks are treated as first-class evidence in `filt`.

## Class C: remote sensing and geoscience

Applies to `det` on aerial and satellite imagery, and to `cnav` where positioning is the
contribution.

| Venue class | Axis fit | Contribution the reviewers weight | Evidence bar |
|---|---|---|---|
| IEEE TGRS, JSTARS, GRSL | `det` on remote-sensing imagery | task-specific method plus geospatial validity | geo-aware splits, scale and orientation variation, sensor diversity |
| ISPRS Journal, ISPRS Annals | `det`, change detection | photogrammetric and geospatial rigor | rigorous ground truth and registration quality |
| Remote Sensing (MDPI) | `det`, `cnav` | competent application studies | careful validation; be explicit about geographic generalization limits |

Beware the standard trap: the same scene appearing in both training and test tiles inflates
results. Report the split construction and the spatial separation rule.

## Class D: Chinese-language journals and domestic venues

Applies to all axes when the target is a Chinese venue.

| Venue class | Notes |
|---|---|
| 自动化学报, 控制理论与应用, 控制与决策, 航空学报, 宇航学报, 电子学报, 测绘学报, 中国惯性技术学报 | domestic control, navigation, and estimation venues; explicit 创新点 statement expected; Chinese abstract plus English abstract usual |
| 计算机学报, 软件学报, 自动化学报, 中国图象图形学报, 计算机辅助设计与图形学学报 | domestic vision venues for `det`, `track`, `reid` |
| 中文核心 and EI-indexed journals | faster cycle; check the 影响因子 and the 收录 status claimed by the venue itself |

Requirements that differ from English venues and are commonly missed: an explicit statement of
创新点 (what is new, stated as a list of points), a Chinese abstract that is a real summary
rather than a translation of the English one, 基金项目 funding acknowledgment formatting,
中图分类号 and 文献标识码 fields, and reference formatting per the GB/T 7714 edition the journal
names. GB/T 7714-2025 replaced GB/T 7714-2015 on 2026-07-01 (national standards platform record,
checked 2026-10-03); journals may lag, so follow the 投稿指南 and record the edition used.

## Class E: preprints and archives

| Platform | Use it for | Constraint to state |
|---|---|---|
| arXiv (cs.CV, cs.RO, eess.SY, eess.SP, math.OC) | priority stamping, early feedback, community visibility | not peer reviewed; check the target venue's preprint policy before posting |
| PhilArchive and other humanities archives | not applicable to this pack's axes | — |
| ResearchGate, institutional repositories | dissemination | not citable as peer-reviewed evidence |

Posting policy varies by venue and by publisher. Verify the specific venue's rule before
posting, and never assume that a preprint is permitted.

## Fit statement template

Produce this before writing, and reuse it in the cover letter.

```text
Target venue: <exact name, track, and year>
Venue class: <A | B | C | D | E>
Official guidelines consulted: <URL or document version, and the date checked>
Primary axis: <det | track | reid | cnav | filt>
Claim type: <empirical delta | mechanism | theory | system | survey>
Why this venue's reviewers will care: <two sentences in the venue's own criteria terms>
Contribution mapped to criteria: <criterion -> our contribution, one line each>
Evidence we have: <list, with tier labels>
Evidence this venue expects that we lack: <list, or "none">
Closest competing papers at this venue: <citations, with how we differ>
Risk of desk rejection: <the single most likely reason, and our mitigation>
```

## Venue-specific failure modes worth pre-empting

- **CVPR-class vision.** Ablation missing for the central claim; comparison under unmatched
  protocol; "we are the first" without a documented search of recent cycles and the foundational
  line of work; missing failure cases;
  no compute or training-detail disclosure.
- **Control theory venues.** Assumptions stated only in words; proof of the main theorem left to
  an appendix that does not close; comparisons against a baseline tuned unfairly; simulation
  presented without a consistency or bound check.
- **Robotics venues.** Hardware section without calibration or timing detail; experiments in one
  environment generalized to all environments; no failure-case analysis; no runtime on the
  specified onboard computer.
- **Remote sensing.** Geographic leakage between splits; a single sensor or single region
  presented as general; ground-truth construction undocumented.
- **Domestic journals.** 创新点 buried in the introduction instead of stated as points; English
  abstract that is a machine translation; figures with Chinese labels in an English submission
  or vice versa.
