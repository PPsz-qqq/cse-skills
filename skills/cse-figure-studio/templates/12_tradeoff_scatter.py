"""12 Accuracy-speed trade-off: scatter on a log speed axis with the Pareto front and real-time line.

Pattern: baselines in muted grey, marker area proportional to model size, the Pareto front of the
baselines as a dashed step, a labelled real-time threshold, "ours" as the only coloured mark,
direct point labels instead of a legend. Same hardware for every timing, or the plot is invalid.
DEMO DATA: the speeds and scores below are placeholders and the output is stamped; replace with
your measured values from the same hardware configuration (benchmark table, results ledger).
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
from matplotlib.ticker import FixedLocator, NullFormatter, NullLocator  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

# name, FPS, accuracy (%), parameters (M); labels are placed automatically by pp.label_points
pts = [('Method A', 8.5, 63.9, 92), ('Method B', 14, 62.2, 61), ('Method C', 26, 60.4, 38),
       ('Method D', 45, 57.8, 25), ('Method E', 85, 53.9, 12), ('Method F', 19, 58.6, 70)]
ours = ('Ours', 38, 63.2, 31)
pp.mark_demo('placeholder speed and accuracy values')
AREA = 1.4                                    # marker area (pt^2) per million parameters
BASE_FILL, BASE_EDGE = '#C7CCD3', '#6B727C'

fig, ax = pp.figure('ieee-single', aspect=0.72)
ax.set_xscale('log')
pp.light_grid(ax, 'both')
ax.axvline(30, color='#9AA1AA', lw=0.7, ls=(0, (3, 2)), zorder=1)
ax.text(31.5, 50.5, pp.tr('real time (30 FPS)', '实时 (30 FPS)'), color=pp.MUTED, fontsize=pp.size('annot'),
        va='bottom', ha='left')

fps = np.array([p[1] for p in pts])
acc = np.array([p[2] for p in pts])
front, best = [], -np.inf                     # Pareto front of the baselines, drawn as a step line
for i in np.argsort(-fps):
    if acc[i] > best:
        front.append(i)
        best = acc[i]
front = sorted(front, key=lambda i: fps[i])
ax.step(fps[front], acc[front], where='post', color='#A3AAB3', lw=0.8, ls=(0, (2.5, 2)), zorder=1)

ax.scatter(fps, acc, s=[p[3] * AREA for p in pts], color=BASE_FILL, edgecolor=BASE_EDGE, linewidth=0.6, zorder=3)
name, f, a, params = ours
ax.scatter(f, a, s=params * AREA * 3.2, color='none', edgecolor=pp.OURS, linewidth=0.6, alpha=0.45, zorder=3)
ax.scatter(f, a, s=params * AREA, color=pp.OURS, edgecolor='#FFFFFF', linewidth=0.8, zorder=4)

ax.xaxis.set_major_locator(FixedLocator([5, 10, 20, 50, 100]))
ax.xaxis.set_major_formatter(lambda v, _: f'{v:g}')
ax.xaxis.set_minor_locator(NullLocator())
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_xlim(5, 140)
ax.set_ylim(50, 66)
ax.set_xlabel(pp.tr('Speed (FPS, same GPU, log scale)', '速度 (FPS，同一 GPU，对数坐标)'))
ax.set_ylabel('HOTA (%)')
for s, label in ((20, '20M'), (60, '60M')):
    ax.scatter([], [], s=s * AREA, color=BASE_FILL, edgecolor=BASE_EDGE, linewidth=0.6, label=label)
ax.legend(title=pp.tr('Parameters', '参数量'), loc='upper right', title_fontsize=pp.size('legend'), labelspacing=0.9,
          borderpad=0.4, handletextpad=0.8)

names = [p[0] for p in pts] + [pp.tr('Ours', '本文')]
pp.label_points(ax, list(fps) + [f], list(acc) + [a], names, marker_size=[p[3] * AREA for p in pts] + [params * AREA * 3.2],
                colors=[pp.MUTED] * len(pts) + [pp.OURS], weights=['normal'] * len(pts) + ['bold'],
                order=[len(pts)] + list(range(len(pts))))

pp.save(fig, args.out, '12_tradeoff_scatter', args.formats, args.dpi)
