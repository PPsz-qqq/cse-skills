# Figure Template Catalog

Complete reference of available templates with data structure specifications, typical use cases, and output examples.

## Overview

| # | Template name | Type | Typical use | Data complexity | Demo available |
|---|---------------|------|-------------|-----------------|----------------|
| 01 | `bars.py` | Quantitative | Single or grouped bar chart | Low | ✓ |
| 02 | `bars_grouped.py` | Quantitative | Multi-method comparison | Medium | ✓ |
| 03 | `boxplot.py` | Quantitative | Distribution comparison | Medium | ✓ |
| 04 | `curves.py` | Quantitative | Time series or parametric curves | Medium | ✓ |
| 05 | `curves_bands.py` | Quantitative | Curves with uncertainty bands | Medium | ✓ |
| 06 | `heatmap.py` | Quantitative | 2D scalar field | Medium | ✓ |
| 07 | `scatter.py` | Quantitative | Bivariate relationship | Low | ✓ |
| 08 | `scatter_error.py` | Quantitative | Bivariate with uncertainty | Medium | ✓ |
| 09 | `lines_multi.py` | Quantitative | Multi-series comparison | Medium | ✓ |
| 10 | `histogram.py` | Quantitative | Distribution or frequency | Low | ✓ |
| 11 | `histogram_overlay.py` | Quantitative | Multi-distribution comparison | Medium | ✓ |
| 12 | `confusion_matrix.py` | Quantitative | Classification performance | Low | ✓ |
| 13 | `roc_curve.py` | Quantitative | Binary classifier threshold sweep | Medium | ✓ |
| 14 | `trajectory_2d.py` | Quantitative | Spatial path | Medium | ✓ |
| 15 | `trajectory_crlb.py` | Quantitative | Estimation error vs bound | High | ✓ |
| 16 | `trajectory_cov.py` | Quantitative | Trajectory with covariance ellipses | High | ✓ |
| 17 | `precision_recall.py` | Quantitative | Detection/retrieval performance | Medium | ✓ |
| 18 | `detection_boxes.py` | Qualitative | Detection visualization | Medium | ✓ |
| 19 | `reid_retrieval.py` | Qualitative | Re-identification results | Medium | ✓ |

---

## Quantitative Templates

### 01: Simple Bar Chart (`bars.py`)

**Use**: Single-metric comparison across conditions, methods, or datasets.

**Data structure**:
```python
data = {
    'labels': ['Method A', 'Method B', 'Method C'],
    'values': [0.85, 0.92, 0.88],
    'errors': [0.03, 0.02, 0.04]  # Optional: std, sem, or CI
}
```

**Typical scenarios**:
- Accuracy comparison across N methods
- Processing time per method
- Detection rate per condition

**Caption template**: "Comparison of [metric] across [entity]. Error bars show ±1 [SEM/SD/95% CI] over [n] runs."

---

### 02: Grouped Bar Chart (`bars_grouped.py`)

**Use**: Multi-metric comparison across methods (e.g., speed vs accuracy; precision vs recall).

**Data structure**:
```python
data = {
    'methods': ['Ours', 'Baseline A', 'Baseline B'],
    'metrics': ['Accuracy (%)', 'Speed (ms)'],
    'values': [
        [92.3, 15.2],  # Ours
        [88.1, 22.7],  # Baseline A
        [90.5, 18.9]   # Baseline B
    ],
    'errors': [
        [1.2, 0.8],
        [1.5, 1.1],
        [1.3, 0.9]
    ]  # Optional
}
```

**Typical scenarios**:
- Speed-accuracy tradeoff
- Precision-recall across methods
- Multi-objective comparison

**Caption template**: "Comparison of [metric1] and [metric2] on [dataset]. Error bars show ±1 SEM over [n] runs. Our method achieves [X]% [metric1] at [Y] [units] [metric2]."

---

### 03: Box Plot (`boxplot.py`)

**Use**: Show distribution, median, quartiles, and outliers for multiple groups.

**Data structure**:
```python
data = {
    'labels': ['Condition A', 'Condition B', 'Condition C'],
    'distributions': [
        [0.82, 0.85, 0.87, 0.89, 0.91, 0.88, 0.86],  # Condition A samples
        [0.79, 0.83, 0.85, 0.88, 0.90, 0.84, 0.81],  # Condition B samples
        [0.76, 0.80, 0.82, 0.85, 0.87, 0.83, 0.79]   # Condition C samples
    ]
}
```

**Typical scenarios**:
- Robustness comparison across noise levels
- Performance distribution over random seeds
- Cross-dataset generalization

**Caption template**: "Distribution of [metric] across [conditions]. Box shows median and interquartile range (IQR); whiskers extend to 1.5×IQR; outliers shown as dots. [n] runs per condition."

---

### 04: Curves (`curves.py`)

**Use**: Single or multiple curves (time series, parametric sweeps, learning curves).

**Data structure**:
```python
data = {
    'x': [0, 1, 2, 3, 4, 5],
    'y_series': {
        'Ours': [0.5, 0.65, 0.78, 0.85, 0.88, 0.90],
        'Baseline': [0.5, 0.60, 0.70, 0.76, 0.79, 0.81]
    },
    'x_label': 'Epoch',
    'y_label': 'Validation Accuracy'
}
```

**Typical scenarios**:
- Training curves
- Parameter sweep (accuracy vs threshold, range vs angle)
- Tracking error over time

**Caption template**: "[Y-axis metric] vs [x-axis parameter] on [dataset]. [Description of curves and comparison]."

---

### 05: Curves with Uncertainty Bands (`curves_bands.py`)

**Use**: Curves with shaded standard error or confidence interval bands.

**Data structure**:
```python
data = {
    'x': [0, 10, 20, 30, 40, 50],
    'curves': {
        'Ours': {
            'mean': [0.5, 0.68, 0.82, 0.88, 0.91, 0.92],
            'std': [0.03, 0.04, 0.03, 0.02, 0.02, 0.02]
        },
        'Baseline': {
            'mean': [0.5, 0.63, 0.75, 0.80, 0.83, 0.85],
            'std': [0.04, 0.05, 0.04, 0.03, 0.03, 0.03]
        }
    },
    'x_label': 'Training steps (×1000)',
    'y_label': 'Test mAP'
}
```

**Typical scenarios**:
- Multi-seed learning curves
- Tracking accuracy with temporal variance
- Robustness evaluation over noise sweeps

**Caption template**: "[Y-axis] vs [x-axis] on [dataset]. Lines show mean; shaded regions show ±1 [SEM/SD] over [n] runs."

---

### 06: Heatmap (`heatmap.py`)

**Use**: 2D scalar field (confusion matrix values, spatial heat, parameter grid search).

**Data structure**:
```python
data = {
    'values': [
        [0.9, 0.05, 0.05],
        [0.1, 0.85, 0.05],
        [0.0, 0.1, 0.9]
    ],  # 2D array
    'x_labels': ['Class A', 'Class B', 'Class C'],
    'y_labels': ['Pred A', 'Pred B', 'Pred C'],
    'colorbar_label': 'Proportion'
}
```

**Typical scenarios**:
- Confusion matrix proportions (see template 12 for integer counts)
- Spatial occupancy grid
- Hyperparameter sweep results

**Caption template**: "[Description of 2D variable]. Rows: [meaning]; columns: [meaning]. Colorbar units: [units]."

---

### 07: Scatter Plot (`scatter.py`)

**Use**: Bivariate relationship (correlation, clustering, outlier detection).

**Data structure**:
```python
data = {
    'x': [10, 15, 20, 25, 30],
    'y': [0.82, 0.85, 0.88, 0.90, 0.92],
    'x_label': 'Model size (MB)',
    'y_label': 'Accuracy (%)',
    'groups': ['Ours', 'Baseline A', 'Ours', 'Baseline B', 'Ours']  # Optional
}
```

**Typical scenarios**:
- Speed-accuracy Pareto frontier
- Model size vs performance
- Feature importance

**Caption template**: "[Y-axis] vs [x-axis] on [dataset]. Each point represents [one method/run/condition]. [Optional: our method marked in bold/accent color]."

---

### 08: Scatter with Error Bars (`scatter_error.py`)

**Use**: Bivariate relationship with uncertainty in both dimensions.

**Data structure**:
```python
data = {
    'x': [10, 15, 20],
    'y': [0.85, 0.88, 0.90],
    'x_err': [0.5, 0.6, 0.7],
    'y_err': [0.02, 0.015, 0.01],
    'labels': ['Method A', 'Method B', 'Method C']
}
```

**Typical scenarios**:
- Trade-off with measurement uncertainty
- Robustness envelope

**Caption template**: "[Y-axis] vs [x-axis]. Error bars show ±1 [SEM/SD] in both dimensions over [n] runs."

---

### 09: Multi-Line Plot (`lines_multi.py`)

**Use**: Multiple time series or parametric curves on same axes.

**Data structure**:
```python
data = {
    'x': [0, 1, 2, 3, 4, 5],
    'series': {
        'Ours': [0.5, 0.7, 0.85, 0.90, 0.92, 0.93],
        'Baseline A': [0.5, 0.65, 0.78, 0.82, 0.84, 0.85],
        'Baseline B': [0.5, 0.68, 0.80, 0.85, 0.87, 0.88]
    },
    'x_label': 'Epoch',
    'y_label': 'mAP (%)'
}
```

**Typical scenarios**:
- Convergence comparison
- Multi-condition tracking performance

**Caption template**: "[Y-axis] over [x-axis] for [methods] on [dataset]. [Optional: our method converges to X after Y epochs]."

---

### 10: Histogram (`histogram.py`)

**Use**: Single distribution or frequency count.

**Data structure**:
```python
data = {
    'values': [0.8, 0.82, 0.85, 0.87, 0.88, 0.90, 0.85, 0.83],  # Raw samples
    'bins': 15,  # Or explicit bin edges
    'x_label': 'Accuracy',
    'y_label': 'Frequency'
}
```

**Typical scenarios**:
- Performance distribution over runs
- Residual error histogram

**Caption template**: "Distribution of [metric] over [n] [runs/samples/images]. [Optional: mean ± std reported]."

---

### 11: Overlaid Histograms (`histogram_overlay.py`)

**Use**: Compare multiple distributions.

**Data structure**:
```python
data = {
    'distributions': {
        'Ours': [0.85, 0.87, 0.88, 0.90, 0.89, 0.91],
        'Baseline': [0.78, 0.80, 0.82, 0.81, 0.83, 0.79]
    },
    'bins': 10,
    'x_label': 'Detection confidence',
    'y_label': 'Count'
}
```

**Typical scenarios**:
- Confidence score distributions (true vs false positives)
- Cross-method robustness

**Caption template**: "Distribution of [metric] for [methods]. [Optional: our method's distribution is shifted toward higher values]."

---

### 12: Confusion Matrix (`confusion_matrix.py`)

**Use**: Classification accuracy breakdown with integer counts or proportions.

**Data structure**:
```python
data = {
    'matrix': [
        [450, 25, 5],
        [30, 420, 10],
        [10, 15, 435]
    ],  # Rows: true class; columns: predicted class
    'labels': ['Class A', 'Class B', 'Class C']
}
```

**Typical scenarios**:
- Multi-class classification performance
- Tracking identity confusion

**Caption template**: "Confusion matrix on [dataset]. Rows: ground truth; columns: predictions. Diagonal entries are correct classifications. Overall accuracy: [X]%."

---

### 13: ROC Curve (`roc_curve.py`)

**Use**: Binary classifier threshold sweep (TPR vs FPR).

**Data structure**:
```python
data = {
    'curves': {
        'Ours': {
            'fpr': [0.0, 0.05, 0.1, 0.2, 1.0],
            'tpr': [0.0, 0.8, 0.9, 0.95, 1.0],
            'auc': 0.95
        },
        'Baseline': {
            'fpr': [0.0, 0.1, 0.2, 0.3, 1.0],
            'tpr': [0.0, 0.7, 0.8, 0.85, 1.0],
            'auc': 0.88
        }
    }
}
```

**Typical scenarios**:
- Detection threshold analysis
- Validation-only curve (do not select threshold on test set)

**Caption template**: "ROC curves on [validation/test] set. AUC: Ours [X.XX], Baseline [Y.YY]. [Important: state which set; if test set, confirm threshold was chosen on validation]."

---

### 14: 2D Trajectory (`trajectory_2d.py`)

**Use**: Spatial path (ground truth vs estimate, multiple agents).

**Data structure**:
```python
data = {
    'trajectories': {
        'Ground truth': {
            'x': [0, 1, 2, 3, 4],
            'y': [0, 0.5, 1.2, 2.1, 3.0]
        },
        'Estimate': {
            'x': [0, 1.05, 2.1, 3.0, 4.1],
            'y': [0, 0.48, 1.18, 2.05, 2.95]
        }
    },
    'x_label': 'x (m)',
    'y_label': 'y (m)'
}
```

**Typical scenarios**:
- Tracking or navigation path
- SLAM trajectory

**Caption template**: "Trajectories on [dataset/scenario]. Ground truth shown as [style]; estimate shown as [style]. RMSE: [X.XX] m."

---

### 15: Trajectory with CRLB Bound (`trajectory_crlb.py`)

**Use**: Estimator performance vs Cramér-Rao lower bound.

**Data structure**:
```python
data = {
    'time': [0, 1, 2, 3, 4, 5],
    'rmse_ours': [0.1, 0.15, 0.12, 0.14, 0.13, 0.11],
    'rmse_baseline': [0.2, 0.25, 0.22, 0.24, 0.23, 0.21],
    'crlb': [0.08, 0.09, 0.085, 0.09, 0.088, 0.087],
    'x_label': 'Time (s)',
    'y_label': 'Position RMSE (m)'
}
```

**Typical scenarios**:
- Filtering or tracking performance vs theoretical bound
- Sensor fusion efficiency

**Caption template**: "Position RMSE over time. CRLB computed from [sensor model/Fisher information]. Our method achieves [X]× bound at time [Y]."

---

### 16: Trajectory with Covariance Ellipses (`trajectory_cov.py`)

**Use**: Path with uncertainty ellipses at keypoints.

**Data structure**:
```python
data = {
    'trajectory': {
        'x': [0, 1, 2, 3, 4],
        'y': [0, 0.5, 1.0, 1.5, 2.0]
    },
    'covariances': [
        [[0.01, 0.002], [0.002, 0.01]],  # At (0, 0)
        [[0.02, 0.005], [0.005, 0.02]],  # At (1, 0.5)
        # ... one 2×2 matrix per point
    ],
    'x_label': 'x (m)',
    'y_label': 'y (m)'
}
```

**Typical scenarios**:
- Kalman filter state covariance
- Multi-agent cooperative localization

**Caption template**: "Estimated trajectory with 95% confidence ellipses. Covariances from [estimator name] at [interval]. Dataset: [name]."

---

### 17: Precision-Recall Curve (`precision_recall.py`)

**Use**: Detection or retrieval performance sweep.

**Data structure**:
```python
data = {
    'curves': {
        'Ours': {
            'recall': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            'precision': [1.0, 0.95, 0.92, 0.88, 0.82, 0.75],
            'ap': 0.89
        },
        'Baseline': {
            'recall': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            'precision': [1.0, 0.90, 0.85, 0.78, 0.70, 0.60],
            'ap': 0.81
        }
    }
}
```

**Typical scenarios**:
- Object detection (COCO AP)
- Re-identification retrieval
- Information retrieval

**Caption template**: "Precision-recall curves on [dataset]. AP: Ours [X.XX], Baseline [Y.YY]. Computed using [evaluator, e.g., pycocotools]."

---

## Qualitative Templates

### 18: Detection Boxes (`detection_boxes.py`)

**Use**: Visualize ground truth and predicted bounding boxes on images.

**Data structure**:
```python
data = {
    'image': np.array(...),  # H×W×3 RGB image
    'gt': [
        (x1, y1, x2, y2, 'person'),
        (x1, y1, x2, y2, 'car'),
        # ... ground truth boxes
    ],
    'pred': [
        (x1, y1, x2, y2, 'person', 0.95),  # x1, y1, x2, y2, class, confidence
        (x1, y1, x2, y2, 'car', 0.88),
        # ... predictions
    ]
}
```

**Typical scenarios**:
- Detection qualitative results
- Failure case visualization

**Caption template**: "Detection results on [dataset]. Ground truth: dashed boxes; predictions: solid boxes. [Optional: describe specific successes/failures]."

---

### 19: Re-ID Retrieval (`reid_retrieval.py`)

**Use**: Show query and ranked retrieval results.

**Data structure**:
```python
data = {
    'query': np.array(...),  # H×W×3 query image
    'gallery': [
        (np.array(...), True, 0.95),   # (image, is_correct, similarity)
        (np.array(...), True, 0.92),
        (np.array(...), False, 0.88),
        # ... top-k retrievals
    ]
}
```

**Typical scenarios**:
- Re-identification retrieval visualization
- Image similarity results

**Caption template**: "Re-identification retrieval on [dataset]. Query (left); top-[k] retrievals sorted by similarity. Green border: correct identity; gray border: incorrect."

---

## Demo Data Policy

All templates include `pp.mark_demo()` calls when using synthetic/placeholder data. This:
- Stamps "DEMO DATA" in bottom-right
- Logs warning to stderr
- Prevents accidental use of placeholder figures in manuscripts

**To use real data**:
1. Replace demo data structure with actual results
2. Remove or comment out `pp.mark_demo(...)` call
3. Verify no demo stamp appears in output

**Demo data is acceptable for**:
- Template exploration ("show me what this looks like")
- Code integration testing
- Layout prototyping

**Demo data must never be used for**:
- Manuscript submission
- Conference presentations claiming real results
- Any figure labeled as experimental data

---

## Customization Guide

### Changing colors

Edit the palette in template source or theme:
```python
pp.OURS = '#3B6DFF'      # Accent color for "our method"
pp.BASELINE = '#8A9099'  # Neutral gray for baselines
pp.INK = '#0A0D12'       # Main text/line color
```

### Adjusting fonts

Themes define font sizes. For custom sizes:
```python
ax.set_xlabel('Time (s)', fontsize=9)
ax.tick_params(labelsize=8)
```

Check venue minimum sizes in `print_venues.md`.

### Multi-panel figures

Use `fig, axes = pp.subplots(nrows=1, ncols=2, ...)` and address individual axes:
```python
axes[0].plot(x, y1)
axes[1].plot(x, y2)
```

### Axis limits and scales

```python
ax.set_xlim(0, 10)
ax.set_ylim(0, 1)
ax.set_xscale('log')  # For log-scale axes
```

### Grid and spines

```python
ax.grid(True, linewidth=0.3, color='#E5E7EB', zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### Legends

```python
ax.legend(loc='upper left', fontsize=8, frameon=False)
```

For "Ours" in bold:
```python
ax.plot(x, y, label=r'$\mathbf{Ours}$', color=pp.OURS, linewidth=1.5)
```

---

## Caption Checklist

Every figure caption must include:
- [ ] Dataset or scenario name
- [ ] What each visual element represents (line color, marker shape, bar group)
- [ ] Units for all quantities
- [ ] Error bar meaning (SEM, SD, CI) and sample size
- [ ] Statistical test if significance is claimed
- [ ] Source of baseline numbers (our run, cited paper, public leaderboard)
- [ ] Validation vs test set distinction for performance metrics

**Bad caption**: "Accuracy comparison."

**Good caption**: "Comparison of detection accuracy (mAP) on COCO 2017 validation set. Error bars show ±1 SEM over 3 runs with different random seeds. Our method achieves 42.3% mAP, outperforming Faster R-CNN (39.1%, from [cite]) and RetinaNet (40.5%, our reproduction)."

---

## Template Selection Flowchart

```
Is your data quantitative (numbers) or qualitative (images/boxes)?
├─ Quantitative
│  ├─ Single metric across categories? → 01 bars
│  ├─ Multiple metrics per category? → 02 bars_grouped
│  ├─ Show full distribution? → 03 boxplot or 10 histogram
│  ├─ Time series or parametric sweep?
│  │  ├─ Single curve or few curves → 04 curves
│  │  ├─ Multiple curves → 09 lines_multi
│  │  └─ With uncertainty → 05 curves_bands
│  ├─ Bivariate relationship? → 07 scatter (or 08 scatter_error)
│  ├─ 2D field? → 06 heatmap
│  ├─ Classification breakdown? → 12 confusion_matrix
│  ├─ Classifier threshold sweep?
│  │  ├─ Binary (TPR vs FPR) → 13 roc_curve
│  │  └─ Detection/retrieval (precision vs recall) → 17 precision_recall
│  └─ Spatial trajectory?
│     ├─ Simple path → 14 trajectory_2d
│     ├─ vs theoretical bound → 15 trajectory_crlb
│     └─ with covariance → 16 trajectory_cov
└─ Qualitative
   ├─ Detection/tracking visualization → 18 detection_boxes
   └─ Re-ID or retrieval results → 19 reid_retrieval
```

---

## Next Steps

After selecting and customizing a template:
1. **Replace demo data** with your actual results
2. **Run the template** with target venue theme and width
3. **Check warnings** in stderr (text overlaps, clipping, color contrast)
4. **Inspect output** visually (fonts readable, legend clear, colors distinguishable)
5. **Draft caption** following checklist above
6. **Verify numbers** in caption match figure data exactly
7. **Export final formats** (EPS/PDF for print, PNG for preview)
8. **Archive source** (`.py` file and data) for reproducibility

For detailed venue compliance, see `print_venues.md`.  
For data integrity and caption writing, use `cse-paper-craft` skill.  
For pre-submission audit, use `cse-pre-submission-review` skill.
