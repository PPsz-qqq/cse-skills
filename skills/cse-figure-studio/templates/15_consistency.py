"""15 Filter consistency: per-time-step ANEES with chi-square bounds, and position RMSE.

Pattern: ANEES at each step over N independent Monte Carlo runs, compared with the two-sided 95%
interval chi2(N*n_x)/N (not pooled over time), the expected value n_x as a dotted reference, a
log scale so over- and under-confident filters stay readable, and RMSE in a second panel that
shares the time axis. For a matched linear Gaussian filter, the posterior covariance equals the
Cramér-Rao lower bound, so panel (b) includes that bound as a dashed reference line.
DEMO DATA: this is a complete simulated scenario and the output is stamped; replace with your own
Monte Carlo filter runs (protocol block, ledger entry, declared N and seeds).
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.ticker import FixedLocator, NullLocator  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

pp.mark_demo('simulated consistency scenario')
rng = np.random.default_rng(42)

N, K, dt, q, r = 100, 120, 1.0, 0.02, 4.0
F = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]], float)
Qc = np.array([[dt ** 3 / 3, 0, dt ** 2 / 2, 0], [0, dt ** 3 / 3, 0, dt ** 2 / 2],
               [dt ** 2 / 2, 0, dt, 0], [0, dt ** 2 / 2, 0, dt]])
H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], float)
R = r * np.eye(2)
P0 = np.diag([10.0, 10.0, 1.0, 1.0])
nx = 4

# Truth and measurements for N runs.
x = np.zeros((K, N, nx))
x[0] = np.array([0, 0, 1, 0.5]) + rng.multivariate_normal(np.zeros(nx), P0, N)
L = np.linalg.cholesky(q * Qc)
for k in range(1, K):
    x[k] = x[k - 1] @ F.T + rng.standard_normal((N, nx)) @ L.T
z = x[:, :, :2] + rng.standard_normal((K, N, 2)) * np.sqrt(r)


def run(scale):
    Q = q * scale * Qc
    xh = np.array([0, 0, 1, 0.5]) + np.zeros((N, nx))
    P = P0.copy()
    nees, rmse, crlb = np.zeros(K), np.zeros(K), np.zeros(K)
    for k in range(K):
        if k:
            xh, P = xh @ F.T, F @ P @ F.T + Q
        S = H @ P @ H.T + R
        Kg = P @ H.T @ np.linalg.inv(S)
        xh = xh + (z[k] - xh @ H.T) @ Kg.T
        P = (np.eye(nx) - Kg @ H) @ P
        e = x[k] - xh
        nees[k] = np.einsum('ni,ij,nj->n', e, np.linalg.inv(P), e).mean()
        rmse[k] = np.sqrt((e[:, :2] ** 2).sum(1).mean())
        crlb[k] = np.sqrt(np.trace(P[:2, :2]))  # matched filter covariance = posterior CRLB
    return nees, rmse, crlb


cases = [(pp.tr('Matched $Q$', '匹配 $Q$'), 1.0, pp.CYCLE[0]),
         (pp.tr('$Q$ too small (×0.05)', '$Q$ 偏小 (×0.05)'), 0.05, pp.CYCLE[3]),
         (pp.tr('$Q$ too large (×20)', '$Q$ 偏大 (×20)'), 20.0, pp.CYCLE[2])]
lo, hi = pp.anees_bounds(N, nx)
steps = np.arange(K)

fig, (ax1, ax2) = pp.figure('ieee-single', aspect=1.08, nrows=2, sharex=True)
ax1.set_yscale('log')
ax1.axhspan(lo, hi, color='#E3E6EA', zorder=0, lw=0)
ax1.axhline(nx, color='#6B727C', lw=0.7, ls=(0, (1, 1.6)), zorder=1)
handles = []
for name, scale, color in cases:
    nees, rmse, crlb = run(scale)
    handles.append(ax1.plot(steps, nees, color=color, lw=1.0, label=name)[0])
    ax2.plot(steps, rmse, color=color, lw=1.0)
    if scale == 1.0:  # matched linear-Gaussian filter: its covariance is the posterior CRLB
        crlb_line = ax2.plot(steps, crlb, color='#3C4148', lw=0.9, ls=(0, (3, 1.5)), zorder=1,
                             label=pp.tr('CRLB (matched model)', 'CRLB（匹配模型）'))[0]
handles += [Patch(facecolor='#E3E6EA', label=pp.tr(f'95% interval ($N={N}$)', f'95% 区间 ($N={N}$)')),
            Line2D([], [], color='#6B727C', lw=0.7, ls=(0, (1, 1.6)), label=pp.tr('expected $n_x$', '期望值 $n_x$')),
            crlb_line]
ax1.set_ylabel('ANEES')
ax1.yaxis.set_major_locator(FixedLocator([0.5, 1, 2, 4, 10, 20, 40]))
ax1.yaxis.set_major_formatter(lambda v, _: f'{v:g}')
ax1.yaxis.set_minor_locator(NullLocator())
ax1.set_ylim(0.4, 60)
pp.panel_label(ax1, '(a)', x=-0.16)

pp.light_grid(ax2)
ax2.set_ylabel(pp.tr('Position RMSE (m)', '位置 RMSE (m)'))
ax2.set_xlabel(pp.tr('Time step $k$', '时间步 $k$'))
ax2.set_xlim(0, K - 1)
ax2.set_ylim(0, None)
pp.panel_label(ax2, '(b)', x=-0.16)
fig.legend(handles=handles, loc='outside upper center', ncols=2, handlelength=1.6, columnspacing=1.2)

pp.save(fig, args.out, '15_consistency', args.formats, args.dpi)
