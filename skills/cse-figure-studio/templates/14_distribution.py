"""14 Distribution comparison ("raincloud"): half violin, box and the raw points for each method.

Pattern: show every per-sequence or per-run value, not just a mean bar; a density shape for the
form, a slim box for median and quartiles, jittered points underneath; methods on the y axis so
names stay horizontal; "ours" accented, baselines grey. The KDE is reflected at zero for strictly
non-negative data (errors, latencies).
DEMO DATA: the samples below are synthetic and the output is stamped; replace with your per-unit
measurements (per-sequence errors, per-run times), and state the unit in the caption.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

methods = ['EKF', 'UKF', 'Factor graph', 'Ours']
rng = pp.demo_rng(3, 'synthetic per-sequence errors')
data = [rng.lognormal(np.log(m), s, 28) for m, s in ((1.45, 0.38), (1.22, 0.34), (0.98, 0.33), (0.71, 0.27))]
jitter_rng = pp.demo_rng(17, 'cosmetic jitter')
colors = ['#8C939D', '#8C939D', '#8C939D', pp.OURS]


def kde(x, grid, bw, support_min=None):
    """Gaussian KDE with optional reflection at support_min for non-negative data."""
    dens = np.exp(-0.5 * ((grid[:, None] - x[None, :]) / bw) ** 2).sum(1)
    if support_min is not None:
        reflected = 2 * support_min - x
        dens += np.exp(-0.5 * ((grid[:, None] - reflected[None, :]) / bw) ** 2).sum(1)
    return dens / (x.size * bw * np.sqrt(2 * np.pi))


fig, ax = pp.figure('ieee-single', aspect=0.70)
pp.light_grid(ax, 'x')
for i, (vals, color) in enumerate(zip(data, colors)):
    y0 = i
    # Silverman bandwidth; KDE is reflected at zero since errors are non-negative.
    bw = 1.06 * vals.std(ddof=1) * vals.size ** (-1 / 5)
    grid = np.linspace(0.0, vals.max() + 2.5 * bw, 300)
    dens = kde(vals, grid, bw, support_min=0.0)
    dens = dens / dens.max() * 0.36
    ax.fill_between(grid, y0 + 0.06, y0 + 0.06 + dens, color=color, alpha=0.28, linewidth=0)
    ax.plot(grid, y0 + 0.06 + dens, color=color, lw=0.8)
    q1, med, q3 = np.percentile(vals, [25, 50, 75])
    lo, hi = vals[vals >= q1 - 1.5 * (q3 - q1)].min(), vals[vals <= q3 + 1.5 * (q3 - q1)].max()
    ax.plot([lo, hi], [y0, y0], color=color, lw=0.8, solid_capstyle='butt')
    ax.add_patch(FancyBboxPatch((q1, y0 - 0.045), q3 - q1, 0.09, boxstyle='round,pad=0,rounding_size=0.02',
                                facecolor='white', edgecolor=color, linewidth=0.9, zorder=3))
    ax.plot([med, med], [y0 - 0.045, y0 + 0.045], color=color, lw=1.4, zorder=4, solid_capstyle='butt')
    jitter = jitter_rng.uniform(-0.09, 0.09, vals.size)
    ax.scatter(vals, y0 - 0.2 + jitter, s=5, color=color, alpha=0.8, linewidth=0, zorder=2)

ax.set_yticks(range(len(methods)), methods)
for lbl, color in zip(ax.get_yticklabels(), colors):
    lbl.set_color(pp.OURS if color == pp.OURS else pp.INK)
    lbl.set_fontweight('bold' if color == pp.OURS else 'normal')
ax.tick_params(axis='y', length=0)
ax.spines['left'].set_visible(False)
ax.set_ylim(-0.45, len(methods) - 0.45)
ax.set_xlim(0, 3.4)
ax.set_xlabel('Position error per sequence (m)')

pp.save(fig, args.out, '14_distribution', args.formats, args.dpi)
