# cse-figure-studio | 科研绘图工作室

[English](#english) | [中文](#中文)

---

## English

Publication-grade data visualization for detection, tracking, re-identification, navigation, and filtering research.

### What it does

Generates submission-ready scientific figures that match venue specifications (IEEE, Elsevier, Springer, Nature, CVPR, NeurIPS, 自动化学报, 控制理论与应用) with built-in quality checks:

- **Demo stamps** when using placeholder data
- **Text collision detection** to prevent overlapping labels
- **Size lint** for font sizes (7–12 pt ranges based on venue)
- **WCAG color contrast** checks for accessibility
- **Unit validation** for dimensions

### Templates

**Conceptual** (1–9):
- Framework diagrams, flowcharts, network architectures
- Module breakdowns, control loops, cooperative systems
- Timing diagrams, taxonomies, paradigm comparisons

**Quantitative** (10–17):
- Learning curves with confidence bands
- Ablation study bars, parameter tradeoff scatter plots
- Confusion matrices, boundary distributions
- CRLF bounds, covariance ellipses
- Precision-recall curves, mAP comparisons

**Qualitative** (18–19):
- Detection/tracking bounding box grids
- Re-ID retrieval ranking galleries

### Themes

`ieee`, `elsevier`, `springer`, `nature`, `cvpr`, `neurips`, `aas` (自动化学报), `cta` (控制理论与应用)

### Usage

Load the skill when you need to:
- Create paper figures (论文配图)
- Visualize research data (科研绘图)
- Generate publication plots (可视化)

The skill will:
1. Understand your data and conclusion
2. Select appropriate template
3. Generate figure with venue-specific formatting
4. Apply quality checks and warn about issues
5. Export as SVG/PDF/PNG

### Documentation

- `references/figure_catalog.md` — Complete template gallery
- `references/print_venues.md` — Primary-source verified venue specifications (accessed 2026-10-04)
- `references/data_integrity.md` — Data-figure matching and caption writing
- `references/render_qa.md` — QA workflow
- `references/api.md` — API reference for scripts

### Scripts

- `scripts/pubplot.py` — Core plotting engine
- `scripts/figkit.py` — Figure utilities
- `scripts/render.py` — CLI renderer with `--doctor` mode

---

## 中文

面向目标检测、跟踪、重识别、导航和滤波研究的出版级数据可视化。

### 功能

生成符合投稿期刊/会议规范（IEEE、Elsevier、Springer、Nature、CVPR、NeurIPS、自动化学报、控制理论与应用）的科研图表，内置质量检查：

- **演示数据标记** 使用占位数据时自动添加水印
- **文本碰撞检测** 防止标签重叠
- **字号检查** 根据期刊要求验证字体大小（7–12 pt）
- **WCAG 色彩对比度** 检查可访问性
- **单位验证** 检查尺寸单位

### 模板

**概念图** (1–9)：
- 框架图、流程图、网络架构
- 模块分解、控制回路、协同系统
- 时序图、分类树、范式对比

**定量图** (10–17)：
- 学习曲线（含置信带）
- 消融实验柱状图、参数权衡散点图
- 混淆矩阵、边界分布
- CRLB 界、协方差椭圆
- PR 曲线、mAP 对比

**定性图** (18–19)：
- 检测/跟踪框网格展示
- 重识别检索排序画廊

### 主题

`ieee`、`elsevier`、`springer`、`nature`、`cvpr`、`neurips`、`aas`（自动化学报）、`cta`（控制理论与应用）

### 使用方法

在以下场景加载技能：
- 论文配图
- 科研绘图
- 数据可视化

技能将：
1. 理解你的数据和结论
2. 选择合适的模板
3. 生成符合期刊格式的图表
4. 执行质量检查并警告问题
5. 导出为 SVG/PDF/PNG

### 文档

- `references/figure_catalog.md` — 完整模板画廊
- `references/print_venues.md` — 一手来源验证的期刊规范（2026-10-04 访问）
- `references/data_integrity.md` — 数据-图表匹配与题注撰写
- `references/render_qa.md` — 质量保证流程
- `references/api.md` — 脚本 API 参考

### 脚本

- `scripts/pubplot.py` — 核心绘图引擎
- `scripts/figkit.py` — 图表工具
- `scripts/render.py` — 命令行渲染器（含 `--doctor` 诊断模式）

---

## Installation | 安装

The skill is part of the **cse-skills** pack. Install via DSH:

本技能是 **cse-skills** 包的一部分。通过 DSH 安装：

```powershell
# From the cse-skills repository root
# 在 cse-skills 仓库根目录
.\tools\install.ps1
```

This creates a junction at `~/.dsh/skills/cse-figure-studio`.

这会在 `~/.dsh/skills/cse-figure-studio` 创建一个连接点。

## License | 许可证

MIT License - See repository root for details.

MIT 许可证 - 详见仓库根目录。
