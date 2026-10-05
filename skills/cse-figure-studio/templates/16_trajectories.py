"""16 Trajectory plot: ground truth versus estimates for several agents, with covariance ellipses.

Pattern: equal axis scaling with units, ground truth as a thin dark dashed line, each agent's
estimate in its own colour labelled at the start, 95% covariance ellipses at regular intervals,
start and end markers, anchors as triangles, and the GNSS-denied region shaded and named in place.
The ellipses are drawn with the actual probability-correct scaling from the covariance matrix.
DEMO DATA: the paths and covariances are synthetic and the output is stamped; plot your logged
estimates and covariances (from the filter output or experiment ledger).
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

pp.mark_demo('synthetic trajectories and covariances')
rng = np.random.default_rng(11)

t = np.linspace(0, 1, 160)
paths = [np.c_[8 + 84 * t, 41 + 9 * np.sin(2 * np.pi * t)],
         np.c_[8 + 84 * t, 24 + 6 * np.sin(4 * np.pi * t + 0.6)],
         np.c_[14 + 74 * t, 9 + 3 * np.cos(3 * np.pi * t)]]
colors = [pp.CYCLE[0], pp.CYCLE[1], pp.CYCLE[2]]
DENIED = (42, 70)

fig, ax = pp.figure('ieee-single', aspect=0.70)
ax.add_patch(Rectangle((DENIED[0], -4), DENIED[1] - DENIED[0], 62, facecolor='#F2F3F5', edgecolor='none',
                       hatch='////', zorder=0))
ax.patches[-1].set_edgecolor('#D9DCE1')
ax.patches[-1].set_linewidth(0)
ax.text(np.mean(DENIED), 54.2, pp.tr('GNSS-denied', 'GNSS 拒止区'), ha='center', va='center',
        fontsize=pp.size('annot'), color=pp.MUTED, fontweight='bold',
        bbox={'boxstyle': 'round,pad=0.2', 'fc': 'white', 'ec': 'none'})

for i, (gt, color) in enumerate(zip(paths, colors)):
    inside = (gt[:, 0] > DENIED[0]) & (gt[:, 0] < DENIED[1])
    sigma = 0.5 + 2.2 * np.convolve(inside.astype(float), np.ones(25) / 25, mode='same')
    walk = np.cumsum(rng.normal(0, 1, (len(t) + 40, 2)), axis=0)
    kern = np.exp(-0.5 * (np.arange(-20, 21) / 7.0) ** 2)
    smooth = np.stack([np.convolve(walk[:, d], kern / kern.sum(), mode='valid') for d in (0, 1)], axis=1)[:len(t)]
    smooth -= smooth[0]
    err = smooth / np.abs(smooth).max() * sigma[:, None] * 1.1
    est = gt + err
    ax.plot(gt[:, 0], gt[:, 1], color='#4A515B', lw=0.7, ls=(0, (3, 2)), zorder=2)
    ax.plot(est[:, 0], est[:, 1], color=color, lw=1.2, zorder=3)
    for k in range(10, len(t), 16):
        v = gt[min(k + 1, len(t) - 1)] - gt[k - 1]
        ang = np.degrees(np.arctan2(v[1], v[0]))
        # Build a 2x2 covariance: along-track variance grows with GNSS-denied accumulation.
        s_along = sigma[k] * 1.3
        s_cross = sigma[k] * 0.7
        c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        R = np.array([[c, -s], [s, c]])
        P = R @ np.diag([s_along**2, s_cross**2]) @ R.T
        pp.cov_ellipse(ax, est[k], P, prob=0.95, facecolor=color, alpha=0.13, edgecolor=color,
                       linewidth=0.6, zorder=2.5)
    ax.plot(*est[0], 'o', ms=4, mfc='white', mec=color, mew=1.0, zorder=4)
    ax.plot(*est[-1], 's', ms=3.6, color=color, zorder=4)
    ax.text(est[0, 0] - 2.2, est[0, 1], pp.tr(f'Agent {i + 1}', f'智能体 {i + 1}'), ha='right', va='center',
            fontsize=pp.size('annot'), color=color, fontweight='bold')

anchors = np.array([[2, 54], [98, 54], [98, 0]])
ax.plot(anchors[:, 0], anchors[:, 1], '^', ms=5.5, color='#C2A04A', mec='#8A6E1F', mew=0.6, zorder=4)

ax.set_aspect('equal')
ax.set_xlim(-14, 102)
ax.set_ylim(-4, 58)
ax.set_xlabel(pp.tr('East (m)', '东向 (m)'))
ax.set_ylabel(pp.tr('North (m)', '北向 (m)'))
handles = [Line2D([], [], color='#4A515B', lw=0.7, ls=(0, (3, 2))), Line2D([], [], color=pp.INK, lw=1.2),
           Patch(facecolor='#7F8790', alpha=0.25, edgecolor='#7F8790', linewidth=0.6),
           Line2D([], [], ls='', marker='^', ms=5.5, color='#C2A04A', mec='#8A6E1F')]
labels = [pp.tr('Ground truth', '真值'), pp.tr('Estimate', '估计'), pp.tr('95% ellipse', '95% 置信椭圆'),
          pp.tr('Anchor', '锚点')]
ax.legend(handles, labels, ncols=4 if pp.size('legend') < 8 else 2, loc='lower left', bbox_to_anchor=(0, 1.0),
          borderaxespad=0.2, handlelength=1.5, columnspacing=1.0)

pp.save(fig, args.out, '16_trajectories', args.formats, args.dpi)
