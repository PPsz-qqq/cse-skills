---
name: cse-figure-studio
description: Publication-grade data visualization for detection, tracking, re-ID, navigation, and filtering research
whenToUse: Use when creating, auditing, or revising manuscript figures for CSE papers (目标检测/跟踪/重识别/协同导航/滤波论文配图). Triggers include 画图/作图/论文图表/科研绘图/figure generation/plot/visualization
---

# CSE Figure Studio

Publication-grade data visualization engine for control science and engineering research: detection, tracking, re-identification, cooperative navigation, and filtering. Produces IEEE/Elsevier/Springer/中文期刊-compliant figures with automatic demo-data tracking, text-collision detection, WCAG-compliant colors, and venue-specific typographic themes.

## Execution contract

### Start

1. **Clarify intent**: figure type (quantitative data plot vs qualitative detection/tracking visualization), target venue (IEEE conference/journal, Elsevier, Springer, 自动化学报, 控制理论与应用, 控制与决策), language (English/Chinese labels), and whether this is initial drafting or camera-ready revision.

2. **Check data provenance**: 
   - Real experimental results with stated protocol, dataset, and statistical treatment → proceed with production figure
   - Placeholder/synthetic/demo data → mark with `pp.mark_demo()`, apply demo stamp, warn that figure is not a manuscript-ready result

3. **Select or customize template**: 
   - Match figure type to template catalog (curves with bands, bar charts, scatter plots, confusion matrices, trajectories with covariance ellipses, PR curves, detection boxes, re-ID retrieval)
   - Customize data, labels, colors, and layout
   - Never violate venue constraints (widths, font sizes, resolution, file format)

### Workflow

1. **Template discovery**: show user the template catalog if they request "show me examples" or "what figures can you make"
2. **Data integration**: 
   - Replace demo data with user's actual results
   - Verify units, axis labels, and caption-figure alignment
   - Check that every plotted number has a source (experiment log, evaluation script output, statistical test)
3. **Venue compliance**: 
   - Apply theme: `--theme ieee` (default 9-10pt), `--theme elsevier` (7pt), `--theme springer` (8-12pt), `--theme zh` (中文标注), `--theme aas` (自动化学报 8pt)
   - Set width: `ieee-single` (88.9mm), `ieee-double` (182mm), `elsevier-single` (90mm), `elsevier-double` (190mm), `springer-small` (119mm), `springer-large` (174mm), `aas-single` (8cm), `aas-double` (16cm)
   - Export formats: `--formats eps pdf svg png` with `--dpi 600` (line art) or `--dpi 300` (photos/halftones)
4. **Rendering and QA**:
   - Run `python <template>.py --out <dir> --formats <fmt> --dpi <dpi> --theme <theme> --lang <en|zh>`
   - Inspect warnings: text overlaps, clipped labels, WCAG color contrast failures, demo data stamps
   - Run `python render.py --doctor <output.svg>` for additional PDF/EPS checks (fonts, clipping, transparency)
5. **Caption drafting**: state dataset, protocol, statistical test, sample size, error bar meaning (SEM/SD/CI), and any post-processing

### Output

- **Figure files**: EPS (vector, IEEE/Springer preferred), PDF (vector, universal), SVG (inspection), PNG/TIFF (raster fallback, at specified DPI)
- **Demo stamp**: "DEMO DATA" watermark in bottom-right when `pp.mark_demo()` was called
- **Warnings log**: text overlaps, clipped elements, WCAG contrast issues, font embedding problems
- **Template source**: user receives the exact `.py` file used, enabling reproducibility and fine-tuning

### Red lines

- **No fabricated data**: if user has no real results, produce a demo figure with visible stamp and explicit "this is placeholder" warning. Never present demo data as real results.
- **No venue rule violations**: do not exceed max figure dimensions, drop below minimum font sizes, or use prohibited formats (JPEG for line art, Type 3 fonts for IEEE venues that ban them, RGB when CMYK is required)
- **No unlabeled axes**: every axis must have quantity, unit, and scale (linear/log) clearly stated
- **No unattributed claims in captions**: every performance number, dataset name, and comparison must trace to a stated source (our experiment, cited paper, public benchmark)
- **Caption-figure consistency**: numbers in caption must match figure data exactly; axis labels in caption must match axis labels in figure; figure title/number in caption must match presented figure

## When to delegate

- **Statistical analysis beyond plotting**: use `cse-experiment-suite` for ANOVA, t-tests, consistency checks (NEES/ANEES), or multi-seed aggregation
- **Baseline/competitor literature search**: use `cse-lit-radar` to find comparison methods and their reported numbers
- **Caption writing and claim framing**: use `cse-paper-craft` for Results section prose and evidence-calibrated claim strength
- **Pre-submission figure audit**: use `cse-pre-submission-review` for referee-perspective critique of figure clarity, caption completeness, and data integrity

## Integration with pack

Part of the `ctrl-skills` CSE research pack:
- `cse-idea-forge` → research question
- `cse-lit-radar` → related work and baselines  
- `cse-experiment-suite` → protocol and statistical design
- **`cse-figure-studio`** → data visualization (this skill)
- `cse-paper-craft` → manuscript writing
- `cse-pre-submission-review` → mock peer review
- `cse-response-craft` → reviewer response

## Examples

**Request**: "Plot ROC curves for my three detectors on COCO validation set"
**Response**: 
1. Clarify: do you have the actual per-image predictions, or should I show you the template with demo data first?
2. If demo: present template 17 (PR curves), show code, explain how to replace synthetic curves with real evaluator output (pycocotools AP)
3. If real data: request predictions file, run evaluation, plot actual curves, omit demo stamp

**Request**: "Make an IEEE two-column bar chart comparing our method's speed and accuracy against three baselines"
**Response**:
1. Confirm venue: IEEE conference or journal? (determines font size 9-10pt)
2. Request data: mean ± std for speed (ms) and accuracy (%) for all four methods
3. Template 02 (grouped bars), width `ieee-double`, theme `ieee`, export EPS at 600 dpi
4. Draft caption: "Comparison of inference speed and accuracy on [dataset]. Error bars show ±1 SEM over [n] runs. Our method achieves [X]% accuracy at [Y] ms per frame."

**Request**: "画一个中文的自动化学报单栏轨迹图，要有协方差椭圆"
**Response**:
1. Venue: 自动化学报 (single column 8cm, 中文标注, Times New Roman + 宋体, 8 pt labels, 600 ppi grayscale EPS)
2. Template 16 (trajectories with covariance ellipses), width `aas-single`, theme `aas`, lang `zh`
3. Check: do you have real trajectory estimates with covariance matrices, or demo first?
4. Export: `--formats eps --dpi 600`, verify grayscale mode, check 8pt labels are readable

## Technical reference

- **Engine**: `scripts/pubplot.py` (core plotting), `scripts/figkit.py` (utilities), `scripts/render.py` (doctor/validator)
- **Templates**: 19 templates in `templates/` directory covering quantitative data plots and qualitative visualizations (see [figure_catalog.md](references/figure_catalog.md))
- **Themes**: `ieee` (9-10pt, Helvetica/Arial/TNR), `elsevier` (7pt, Arial/Helvetica/TNR), `springer` (8-12pt, Helvetica/Arial), `zh` (中文, SimSun/SimHei), `aas` (自动化学报, 8pt, TNR+宋体)
- **Venue specs**: see [print_venues.md](references/print_venues.md) for IEEE/Elsevier/Springer/CVPR/NeurIPS/ICML/自动化学报/控制理论与应用 widths, fonts, DPI, and format requirements (verified 2026-10-04)

## Quality checklist

Before presenting a figure as manuscript-ready:
- [ ] Real data with stated source (not demo/placeholder)
- [ ] Venue-compliant width, font size, resolution, format
- [ ] No text overlaps, clipped labels, or WCAG contrast failures (check stderr warnings)
- [ ] Axes labeled with quantity, unit, parentheses/slashes per venue style
- [ ] Legend distinguishes all plotted elements; "Ours" in bold/accent color when comparing methods
- [ ] Caption states dataset, protocol, sample size, error bar type, statistical test if claims are made
- [ ] Numbers in caption match figure data exactly
- [ ] Exported files tested: EPS opens in Illustrator/Inkscape, PDF renders correctly, fonts embedded

## Frequently asked questions

**Q: My figure has a "DEMO DATA" stamp. How do I remove it?**  
A: Replace the synthetic/placeholder data in the template with your actual experimental results, then remove or comment out the `pp.mark_demo()` call. The stamp only appears when demo data is explicitly registered.

**Q: Can I use JPEG for my plots?**  
A: No. JPEG is lossy and creates compression artifacts in line art and text. IEEE explicitly permits JPEG only for author photographs. Use EPS, PDF, or high-DPI PNG for plots.

**Q: The template uses 9pt labels but my journal requires 7pt. How do I change it?**  
A: Use `--theme elsevier` (7pt default) or manually edit the template's `pp.use()` call to load a custom theme. Check `scripts/pubplot.py` for theme definitions.

**Q: I have Chinese labels but the font renders as boxes.**  
A: Use `--theme zh` or `--theme aas`, which load SimSun (宋体) and SimHei (黑体). Verify these fonts are installed on your system. Export to EPS or PDF with embedded fonts.

**Q: How do I add error bars?**  
A: Use `ax.errorbar(x, y, yerr=std, ...)` for standard deviation, or `yerr=sem` for standard error of the mean. State which one in the caption. See templates 01, 02, 08 for examples.

**Q: My covariance ellipse doesn't match the trajectory spread.**  
A: Use `pp.cov_ellipse(ax, mean, cov, prob=0.95)` for a 95% probability region. This is exact for 2-D Gaussians. If your estimator produces 3×3 or larger covariances, slice the x-y submatrix. State the probability level in the caption.

**Q: Can I use this for non-CSE domains (robotics, computer vision, machine learning)?**  
A: Yes. The templates and engine are general-purpose. The CSE pack integration (experiment protocols, claim strength, baseline search) is domain-specific, but the plotting itself works for any quantitative or qualitative data.
