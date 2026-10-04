"""10 Curves with uncertainty bands: validation metric versus epoch, mean and range over seeds.

Pattern: direct labels at the line ends instead of a legend, "ours" in the accent colour drawn
last and slightly thicker, bands that state what they are (here min-max over 3 seeds), a light
y-grid only. Also fits error against time per agent (add the operational limit with axhline) and
scaling against agent count (shade the valid range with axvspan).
DEMO DATA: load_runs() is synthetic and the output is stamped; replace it with your logged metrics
(one array of shape runs x epochs per method, read from the files the claim ledger points to).
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

epochs = np.arange(1, 61)
methods = [('Baseline A', pp.BASELINES[0], 58.0, 13.0), ('Baseline B', pp.BASELINES[1], 60.5, 11.0),
           ('Ours', pp.OURS, 63.4, 9.0)]
rng = pp.demo_rng(7, 'synthetic learning curves')


def load_runs(name, plateau, tau):
    """DEMO: replace with e.g. np.stack([np.loadtxt(f'exp/{name}/seed{s}/val_hota.csv') for s in SEEDS])."""
    return np.stack([plateau + rng.normal(0, 0.25) - 22 * np.exp(-epochs / tau) + rng.normal(0, 0.22, epochs.size)
                     for _ in range(3)])


fig, ax = pp.figure('ieee-single', aspect=0.64)
pp.light_grid(ax)
for name, color, plateau, tau in methods:
    runs = load_runs(name, plateau, tau)
    mean = runs.mean(0)
    ours = name == 'Ours'
    pp.band(ax, epochs, mean, runs.min(0), runs.max(0), color, lw=1.6 if ours else 1.1, zorder=3 if ours else 2)
    pp.end_label(ax, epochs[-1], mean[-1], name, color, fontweight='bold' if ours else None)

ax.set_xlim(0, 60)
ax.set_ylim(36, 66)
ax.set_xlabel('Epoch')
ax.set_ylabel('Validation HOTA (%)')
ax.spines['right'].set_visible(False)
fig.get_layout_engine().set(w_pad=0.02, h_pad=0.02, rect=(0, 0, 0.86, 1))

pp.save(fig, args.out, '10_curves_band', args.formats, args.dpi)
