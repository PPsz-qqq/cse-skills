"""13 Annotated heatmap: hyperparameter sensitivity on a perceptually ordered colour scale.

Pattern: square cells, a sequential scale with monotonic lightness (Tol iridescent here, viridis
also fine; never jet or rainbow), values printed in each cell with text colour chosen by WCAG
contrast, the selected setting outlined, a thin colour bar with units. Use a diverging scale
only when a meaningful midpoint exists. The selection must come from validation, not test argmax.
DEMO DATA: the grid below is synthetic and the output is stamped; replace with your validation
scores from the tuning ledger, and set SELECTED from the declared hyperparameter protocol.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

lam = [0.1, 0.2, 0.5, 1.0, 2.0]
tau = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
L, Tg = np.meshgrid(np.log10(lam), tau, indexing='ij')
pp.mark_demo('synthetic validation grid')
score = 62.6 - 9.0 * (L + 0.30) ** 2 - 22.0 * (Tg - 0.58) ** 2 - 1.2 * (L + 0.3) * (Tg - 0.58) * 10
SELECTED = (2, 3)  # from validation protocol, not argmax of displayed metric

fig, ax = pp.figure('ieee-single', aspect=0.74)
cm = pp.blues()                               # single hue, monotonic lightness; pp.iridescent() also works
im = ax.imshow(score, cmap=cm, vmin=score.min() - 1.0, vmax=score.max(), aspect='auto', origin='upper')
for i in range(len(lam) - 1):                 # white gaps between cells read cleaner than gridlines
    ax.axhline(i + 0.5, color='#FFFFFF', lw=1.2)
for j in range(len(tau) - 1):
    ax.axvline(j + 0.5, color='#FFFFFF', lw=1.2)
for i in range(len(lam)):
    for j in range(len(tau)):
        sel = (i, j) == SELECTED
        ax.text(j, i, f'{score[i, j]:.1f}', ha='center', va='center', fontsize=pp.size('annot'),
                fontweight='bold' if sel else 'normal', color=pp.text_color_for(cm(im.norm(score[i, j]))))
bi, bj = SELECTED
ax.add_patch(Rectangle((bj - 0.46, bi - 0.46), 0.92, 0.92, fill=False, edgecolor='#E69F00', linewidth=1.6, zorder=3))

ax.set_xticks(range(len(tau)), [f'{t:.1f}' for t in tau])
ax.set_yticks(range(len(lam)), [f'{v:g}' for v in lam])
ax.set_xlabel(pp.tr('Gating threshold $\\tau$', '门限 $\\tau$'))
ax.set_ylabel(pp.tr('Weight $\\lambda$', '权重 $\\lambda$'))
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(length=0)
cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03, aspect=22)
cb.set_label(pp.tr('Validation HOTA (%)', '验证集 HOTA (%)'))
cb.outline.set_visible(False)
cb.ax.tick_params(width=0.5, length=2.5)

pp.save(fig, args.out, '13_heatmap', args.formats, args.dpi)
