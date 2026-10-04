"""11 Grouped bars for an ablation: metrics on the x axis, variants as bars, the full model accented.

Pattern: graded neutral greys for the incremental variants and the accent colour for the full
model, error bars that are named in the caption (here std over 3 seeds), the gain over the
baseline written once above the full model in absolute points, the legend above the axes, bars
that start at zero. Every arm must come from one protocol block; a variant run at another budget
is a second experiment, not an ablation row.
DEMO DATA: the numbers below are placeholders and the output is stamped; read mean and std from
your result files (the same values as the ablation table, at the same precision).
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

metrics = ['HOTA', 'IDF1', 'AssA']
variants = ['Baseline', '+ Motion cue', '+ Appearance cue', 'Full (ours)']
pp.mark_demo('placeholder ablation numbers')     # delete together with the two arrays below
mean = np.array([[58.2, 70.1, 55.4], [60.0, 72.4, 58.1], [60.9, 73.5, 59.6], [62.7, 75.8, 62.3]])
std = np.array([[0.4, 0.5, 0.6], [0.3, 0.4, 0.5], [0.4, 0.4, 0.5], [0.3, 0.3, 0.4]])
colors = ['#D9DCE1', '#B4BAC2', '#8C939D', pp.OURS]

fig, ax = pp.figure('ieee-single', aspect=0.66)
pp.light_grid(ax)
n = len(variants)
width = 0.8 / n
x = np.arange(len(metrics))
for i, (name, color) in enumerate(zip(variants, colors)):
    pos = x - 0.4 + width * (i + 0.5)
    ax.bar(pos, mean[i], width * 0.92, yerr=std[i], color=color, label=name, zorder=2,
           error_kw={'elinewidth': 0.7, 'capthick': 0.7, 'ecolor': '#3C4148'})
for j in range(len(metrics)):
    gain = mean[-1, j] - mean[0, j]
    pos = x[j] - 0.4 + width * (n - 0.5)
    ax.annotate(f'+{gain:.1f}', (pos, mean[-1, j] + std[-1, j]), xytext=(0, 2.5), textcoords='offset points',
                ha='center', va='bottom', color=pp.OURS, fontweight='bold', fontsize=7)

ax.set_xticks(x, metrics)
ax.tick_params(axis='x', length=0)
ax.set_ylim(0, 85)
ax.set_ylabel('Score (%)')
ax.legend(ncols=2, loc='lower left', bbox_to_anchor=(0, 1.0), borderaxespad=0.2, handlelength=1.0)

pp.save(fig, args.out, '11_ablation_bars', args.formats, args.dpi)
