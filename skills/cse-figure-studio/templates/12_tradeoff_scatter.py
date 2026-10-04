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

# name, FPS, accuracy, parameters (M), label offset in points, horizontal and vertical alignment
pts = [('Method A', 8.5, 63.9, 92, (0, 11), 'center', 'bottom'), ('Method B', 14, 62.2, 61, (-35, 0), 'right', 'center'),
       ('Method C', 26, 60.4, 38, (-35, 0), 'right', 'center'), ('Method D', 45, 57.8, 25, (0, -8), 'center', 'top'),
       ('Method E', 85, 53.9, 12, (-6, 0), 'right', 'center'), ('Method F', 19, 58.6, 70, (0, -11), 'center', 'top')]
ours = ('Ours', 38, 63.2, 31)
pp.mark_demo('placeholder speed and accuracy values')

fig, ax = pp.figure('ieee-single', aspect=0.70)
ax.set_xscale('log')
pp.light_grid(ax, 'both')
ax.axvline(30, color='#9AA1AA', lw=0.7, ls=(0, (3, 2)), zorder=1)
ax.text(31.5, 50.6, 'real time (30 FPS)', color=pp.MUTED, fontsize=6.8, va='bottom', ha='left')

fps = np.array([p[1] for p in pts])
acc = np.array([p[2] for p in pts])
order = np.argsort(-fps)
front, best = [], -np.inf
for i in order:
    if acc[i] > best:
        front.append(i)
        best = acc[i]
front = sorted(front, key=lambda i: fps[i])
ax.step(fps[front], acc[front], where='post', color='#9AA1AA', lw=0.8, ls=(0, (2.5, 2)), zorder=1)

for name, f, a, params, off, ha, va in pts:
    ax.scatter(f, a, s=params * 1.4, color='#B4BAC2', edgecolor='#6B727C', linewidth=0.6, zorder=3)
    ax.annotate(name, (f, a), xytext=off, textcoords='offset points', fontsize=7, color=pp.MUTED, ha=ha, va=va)
name, f, a, params = ours
ax.scatter(f, a, s=params * 1.4, color=pp.OURS, edgecolor='white', linewidth=0.8, zorder=4)
ax.annotate('Ours', (f, a), xytext=(8, 6), textcoords='offset points', fontsize=7.5, fontweight='bold',
            color=pp.OURS, va='center')

ax.xaxis.set_major_locator(FixedLocator([5, 10, 20, 50, 100]))
ax.xaxis.set_major_formatter(lambda v, _: f'{v:g}')
ax.xaxis.set_minor_locator(NullLocator())
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_xlim(5, 140)
ax.set_ylim(50, 66)
ax.set_xlabel('Speed (FPS, same GPU, log scale)')
ax.set_ylabel('HOTA (%)')
for s, label in ((20, '20M'), (60, '60M')):
    ax.scatter([], [], s=s * 1.4, color='#B4BAC2', edgecolor='#6B727C', linewidth=0.6, label=label)
ax.legend(title='Parameters', loc='upper right', title_fontsize=7, labelspacing=0.9, borderpad=0.4,
          handletextpad=0.8)

pp.save(fig, args.out, '12_tradeoff_scatter', args.formats, args.dpi)
