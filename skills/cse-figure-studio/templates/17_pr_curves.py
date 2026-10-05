"""17 Precision-recall curves with iso-F1 contours.

Pattern: square axes from 0 to 1, faint iso-F1 curves labelled at their ends, baselines in muted
colours, "ours" accented and drawn last, the summary metric (AP) inside the legend labels, no
markers on dense curves. Use a detection/tracking evaluator object to compute AP from actual
predictions and ground truth; if you must interpolate, use 101-point or all-point, never 11-point.
DEMO DATA: the curves below are synthetic and the output is stamped; replace with evaluator output
(pycocotools, motmetrics, or a protocol-declared equivalent), and state the evaluator name, IoU
threshold, and any post-processing (NMS settings, score thresholds) in the caption.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

pp.mark_demo('synthetic P-R curves')
r = np.linspace(0, 1, 400)


def curve(a, b, floor, r_max):
    rr = r * r_max
    p = floor + (1 - floor) * np.clip(1 - rr ** a, 0, 1) ** (1 / b)
    return rr, np.minimum.accumulate(p)


specs = [('Method A', 2.2, 1.6, 0.30, 0.90, pp.BASELINES[0]), ('Method B', 2.8, 1.8, 0.32, 0.93, pp.BASELINES[2]),
         ('Method C', 3.4, 2.1, 0.34, 0.94, pp.BASELINES[3]), ('Ours', 4.4, 2.6, 0.38, 0.96, pp.OURS)]

fig, ax = pp.figure('ieee-single', aspect=0.88)
for f in (0.2, 0.4, 0.6, 0.8):
    rr = np.linspace(f / 2 + 1e-3, 1, 200)
    pr = f * rr / (2 * rr - f)
    keep = pr <= 1.0
    ax.plot(rr[keep], pr[keep], color='#C9CED4', lw=0.6, zorder=1)
    ax.text(1.01, pr[keep][-1], f'F1={f:.1f}', fontsize=pp.size('annot'), color='#8A9099', va='center', ha='left')

ours_label = None
for name, a, b, floor, r_max, color in specs:
    rr, p = curve(a, b, floor, r_max)
    ap = np.trapezoid(p, rr) if hasattr(np, 'trapezoid') else np.trapz(p, rr)
    ours = name == 'Ours'
    label = f'{pp.tr(name, "本文") if ours else name} (AP {ap:.2f})'
    ours_label = label if ours else ours_label
    ax.plot(rr, p, color=color, lw=1.6 if ours else 1.1, zorder=3 if ours else 2, label=label)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.set_aspect('equal')
ax.set_xlabel(pp.tr('Recall', '召回率'))
ax.set_ylabel(pp.tr('Precision', '精确率'))
ax.legend(loc='lower left', handlelength=1.4, frameon=True, facecolor='white', edgecolor='none', framealpha=1)
for lbl in ax.get_legend().get_texts():
    if lbl.get_text() == ours_label:
        lbl.set_fontweight('bold')
        lbl.set_color(pp.OURS)

pp.save(fig, args.out, '17_pr_curves', args.formats, args.dpi)
