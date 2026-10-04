#!/usr/bin/env python3
"""pubplot: matplotlib defaults and helpers for publication data figures (companion to figkit).

    import pubplot as pp
    pp.use('ieee')                                   # fonts, sizes, line weights, colours
    fig, ax = pp.figure('ieee-single', aspect=0.62)  # exact column width, constrained layout
    ax.plot(x, y, color=pp.OURS, label='Ours')
    pp.save(fig, 'fig', 'fig3-rmse')                 # PDF (fonts embedded), SVG, PNG + lint report

Figures are created at their final printed width, so the font sizes set here are the sizes that
print. save() lints the drawn figure (text collisions, clipped text, text below the theme minimum,
hairlines) and stamps every figure DEMO DATA while any placeholder data is registered with
mark_demo() or demo_rng(). Requires matplotlib and numpy; scipy is optional (exact chi-square bounds).
"""
from __future__ import annotations

import math
import os
import re
import sys

sys.dont_write_bytecode = True

import matplotlib as mpl  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, to_rgb  # noqa: E402
from matplotlib import font_manager  # noqa: E402

WIDTHS_IN = {
    'ieee-single': 3.5, 'ieee-double': 7.16,
    'elsevier-single': 90 / 25.4, 'elsevier-1.5': 140 / 25.4, 'elsevier-double': 190 / 25.4,
    'springer-single': 84 / 25.4, 'springer-double': 174 / 25.4,
    'aas-single': 80 / 25.4, 'aas-double': 160 / 25.4,
}
# TeX points (what \the\columnwidth prints) are 1/72.27 in; PostScript/DTP points ('bp') are 1/72 in.
_UNITS_IN = {'in': 1.0, 'pt': 1 / 72.27, 'bp': 1 / 72, 'mm': 1 / 25.4, 'cm': 1 / 2.54, 'pc': 12 / 72.27}

# Okabe & Ito, Color Universal Design (jfly.uni-koeln.de/color/).
OKABE_ITO = {'blue': '#0072B2', 'orange': '#E69F00', 'green': '#009E73', 'vermilion': '#D55E00',
             'purple': '#CC79A7', 'sky': '#56B4E9', 'yellow': '#F0E442', 'black': '#000000'}
# Paul Tol, Colour schemes (sronpersonalpages.nl/~pault/), qualitative schemes in default order.
TOL_BRIGHT = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']
TOL_HIGH_CONTRAST = ['#004488', '#DDAA33', '#BB5566']
TOL_VIBRANT = ['#EE7733', '#0077BB', '#33BBEE', '#EE3377', '#CC3311', '#009988', '#BBBBBB']
TOL_MUTED = ['#CC6677', '#332288', '#DDCC77', '#117733', '#88CCEE', '#882255', '#44AA99', '#999933', '#AA4499']
TOL_IRIDESCENT = ['#FEFBE9', '#FCF7D5', '#F5F3C1', '#EAF0B5', '#DDECBF', '#D0E7CA', '#C2E3D2', '#B5DDD8',
                  '#A8D8DC', '#9BD2E1', '#8DCBE4', '#81C4E7', '#7BBCE7', '#7EB2E4', '#88A5DD', '#9398D2',
                  '#9B8AC4', '#9D7DB2', '#9A709E', '#906388', '#805770', '#684957', '#46353A']
TOL_YLORBR = ['#FFFFE5', '#FFF7BC', '#FEE391', '#FEC44F', '#FB9A29', '#EC7014', '#CC4C02', '#993404', '#662506']
TOL_SUNSET = ['#364B9A', '#4A7BB7', '#6EA6CD', '#98CAE1', '#C2E4EF', '#EAECCC', '#FEDA8B', '#FDB366', '#F67E4B',
              '#DD3D2D', '#A50026']

# Pack defaults: "ours" uses the same blue as figkit's proposed modules; baselines are muted and
# distinct; CYCLE is for categories with no emphasis (Okabe-Ito order without yellow).
OURS = '#0077BB'
BASELINES = ['#7F8790', '#CC6677', '#DDAA33', '#44AA99', '#882255', '#999933']
CYCLE = [OKABE_ITO[k] for k in ('blue', 'orange', 'green', 'vermilion', 'purple', 'sky', 'black')]
INK, MUTED, GRID = '#23272E', '#5F6670', '#E6E8EB'

THEMES = {
    #           base  label  tick  legend  title  min
    'default': (7.5, 8.0, 7.0, 7.0, 8.0, 6.0),
    'ieee': (9.5, 9.5, 9.0, 9.0, 10.0, 9.0),     # IEEE Author Center: approximately 9-10 pt at final size
    'elsevier': (7.0, 7.5, 7.0, 7.0, 7.5, 6.0),  # Elsevier: about 7 pt lettering, scripts >= 6 pt
    'springer': (8.0, 8.5, 8.0, 8.0, 8.5, 6.0),  # Springer: 8-12 pt (2-3 mm) lettering
    'aas': (8.0, 8.0, 8.0, 8.0, 8.0, 8.0),       # 自动化学报 template: 8 pt, Times New Roman / 宋体
}

_STATE = {'theme': 'default', 'min_size': THEMES['default'][5]}
_DEMO = []          # reasons registered by mark_demo(); non-empty means every save() is stamped


def _have(name):
    try:
        font_manager.findfont(font_manager.FontProperties(family=name), fallback_to_default=False)
        return True
    except ValueError:
        return False


def use(theme='default', lang='en'):
    """Apply the pack's matplotlib style. lang='zh' adds CJK fallback fonts for Chinese labels."""
    base, label, tick, legend, title, min_size = THEMES[theme]
    serif = theme == 'aas'
    latin = [f for f in (['Times New Roman', 'Times', 'Liberation Serif'] if serif else
                         ['Arial', 'Helvetica', 'Liberation Sans']) if _have(f)]
    cjk = [f for f in (['SimSun', 'Songti SC', 'Noto Serif CJK SC', 'Noto Serif SC'] if serif else
                       ['Microsoft YaHei', 'Noto Sans CJK SC', 'Noto Sans SC', 'PingFang SC', 'SimHei'])
           if _have(f)] if lang == 'zh' else []
    if lang == 'zh' and not cjk:
        print('[pubplot] no CJK font found: Chinese labels would render as boxes; install SimSun, '
              'Microsoft YaHei or Noto Sans/Serif SC', file=sys.stderr)
    family = latin + cjk + ['DejaVu Serif' if serif else 'DejaVu Sans']
    rc = {
        'font.family': family, 'font.size': base,
        'axes.labelsize': label, 'axes.titlesize': title, 'axes.titleweight': 'bold',
        'xtick.labelsize': tick, 'ytick.labelsize': tick, 'legend.fontsize': legend,
        'axes.linewidth': 0.6, 'axes.edgecolor': '#3C4148', 'axes.labelcolor': INK, 'text.color': INK,
        'axes.spines.top': False, 'axes.spines.right': False, 'axes.axisbelow': True,
        'axes.labelpad': 3.0, 'axes.titlepad': 4.0, 'axes.prop_cycle': mpl.cycler(color=CYCLE),
        'axes.grid': False, 'grid.color': GRID, 'grid.linewidth': 0.5,
        'xtick.color': '#3C4148', 'ytick.color': '#3C4148', 'xtick.direction': 'out', 'ytick.direction': 'out',
        'xtick.major.size': 3.0, 'ytick.major.size': 3.0, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
        'xtick.minor.size': 1.8, 'ytick.minor.size': 1.8, 'xtick.minor.width': 0.5, 'ytick.minor.width': 0.5,
        'xtick.major.pad': 2.5, 'ytick.major.pad': 2.5,
        'lines.linewidth': 1.2, 'lines.markersize': 4.0, 'lines.markeredgewidth': 0.6,
        'patch.linewidth': 0.6, 'hatch.linewidth': 0.5, 'errorbar.capsize': 2.0,
        'legend.frameon': False, 'legend.handlelength': 1.6, 'legend.handletextpad': 0.5,
        'legend.borderaxespad': 0.3, 'legend.columnspacing': 1.1, 'legend.labelspacing': 0.35,
        'image.cmap': 'viridis', 'figure.dpi': 150, 'savefig.dpi': 600, 'savefig.pad_inches': 0.02,
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
        'figure.constrained_layout.h_pad': 0.02, 'figure.constrained_layout.w_pad': 0.02,
        'axes.unicode_minus': True,
    }
    if latin:
        rc.update({'mathtext.fontset': 'custom', 'mathtext.rm': latin[0], 'mathtext.it': f'{latin[0]}:italic',
                   'mathtext.bf': f'{latin[0]}:bold', 'mathtext.sf': latin[0]})
    else:
        rc['mathtext.fontset'] = 'dejavuserif' if serif else 'dejavusans'
    mpl.rcParams.update(rc)
    _STATE.update(theme=theme, min_size=min_size)
    return rc


def width_in(width):
    """Printed width in inches from a WIDTHS_IN key, a number of inches, or a string with a unit:
    '3.25in', '88mm', '8cm', '21pc', '252bp', or '241.14pt' (TeX points, as \\the\\columnwidth prints)."""
    if isinstance(width, (int, float)):
        return float(width)
    if width in WIDTHS_IN:
        return WIDTHS_IN[width]
    m = re.fullmatch(r'\s*([\d.]+)\s*(in|pt|bp|mm|cm|pc)\s*', str(width))
    if not m:
        raise ValueError(f'unknown width {width!r}: use a key of WIDTHS_IN, inches, or a value with in/pt/bp/mm/cm/pc')
    return float(m.group(1)) * _UNITS_IN[m.group(2)]


def figure(width='ieee-single', height=None, aspect=0.62, nrows=1, ncols=1, **kw):
    """Figure at the exact printed width with constrained layout. height is in inches or a unit
    string; by default height = width * aspect."""
    w = width_in(width)
    h = width_in(height) if height is not None else w * aspect
    fig, axes = plt.subplots(nrows, ncols, figsize=(w, h), layout='constrained', **kw)
    return fig, axes


def light_grid(ax, axis='y'):
    ax.grid(True, axis=axis, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)


def panel_label(ax, label, x=-0.02, y=1.02, size=None):
    """Bold panel label such as '(a)' at the top-left corner, outside the plotting area."""
    ax.text(x, y, label, transform=ax.transAxes, ha='right', va='bottom', fontweight='bold',
            fontsize=size or mpl.rcParams['axes.titlesize'])


def tint(color, t):
    """Blend a colour toward white by fraction t: an opaque stand-in for transparency (EPS, print)."""
    r, g, b = to_rgb(color)
    return (r + (1 - r) * t, g + (1 - g) * t, b + (1 - b) * t)


def band(ax, x, y, lo, hi, color, label=None, lw=1.2, alpha=0.18, zorder=2, solid=False, **kw):
    """Line with a shaded interval (state what the interval is in the caption). solid=True fills
    with an opaque tint instead of transparency, for EPS output or greyscale print."""
    fill = {'color': tint(color, 1 - alpha)} if solid else {'color': color, 'alpha': alpha}
    ax.fill_between(x, lo, hi, linewidth=0, zorder=zorder - 0.5, **fill)
    return ax.plot(x, y, color=color, lw=lw, label=label, zorder=zorder, **kw)[0]


GRAY_STYLES = [  # greyscale-safe series: tone, dash pattern and marker all differ
    {'color': '#000000', 'linestyle': '-', 'marker': 'o'},
    {'color': '#4D4D4D', 'linestyle': (0, (4.0, 1.6)), 'marker': 's'},
    {'color': '#7A7A7A', 'linestyle': (0, (1.0, 1.4)), 'marker': '^'},
    {'color': '#4D4D4D', 'linestyle': (0, (5.0, 1.4, 1.0, 1.4)), 'marker': 'D'},
    {'color': '#9A9A9A', 'linestyle': '-', 'marker': 'v'},
    {'color': '#000000', 'linestyle': (0, (2.4, 1.2)), 'marker': 'x'},
]


def series_style(i, gray=False, ours=False):
    """Style dict for series i. gray=True gives tone + dash + marker so no series depends on colour
    (greyscale journals such as 自动化学报 print; colour-vision deficiency). ours=True: accent / black."""
    if gray:
        s = dict(GRAY_STYLES[i % len(GRAY_STYLES)])
        if ours:
            s.update(color='#000000', linestyle='-')
        return s
    return {'color': OURS if ours else BASELINES[i % len(BASELINES)]}


def end_label(ax, x, y, text, color, dx=4, dy=0, **kw):
    """Direct label at the end of a line, which reads faster than a legend."""
    return ax.annotate(text, (x, y), xytext=(dx, dy), textcoords='offset points', color=color,
                       va='center', ha='left', fontsize=mpl.rcParams['legend.fontsize'], **kw)


def chi2_interval(df, alpha=0.05):
    """Two-sided chi-square quantiles; exact with scipy, Wilson-Hilferty approximation otherwise."""
    try:
        from scipy.stats import chi2
        return chi2.ppf(alpha / 2, df), chi2.ppf(1 - alpha / 2, df)
    except ImportError:
        z = 1.959963984540054 if abs(alpha - 0.05) < 1e-12 else _norm_ppf(1 - alpha / 2)
        f = lambda s: df * (1 - 2 / (9 * df) + s * z * math.sqrt(2 / (9 * df))) ** 3  # noqa: E731
        return f(-1), f(1)


def _norm_ppf(p):
    lo, hi = -10.0, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def anees_bounds(n_runs, n_x, alpha=0.05):
    """Per-time-step ANEES acceptance interval: chi-square with N*n_x dof, divided by N."""
    lo, hi = chi2_interval(n_runs * n_x, alpha)
    return lo / n_runs, hi / n_runs


def cov_ellipse(ax, mean, cov, prob=None, nsig=None, **kw):
    """Draw the region (x - m)^T C^-1 (x - m) <= r^2 of a 2-D covariance and return (patch, p).

    Give prob, for example 0.95 (r^2 = -2 ln(1 - prob), exact for a 2-D Gaussian), or nsig, which
    encloses p = 1 - exp(-nsig^2 / 2): 39 % for 1, 86 % for 2, 99 % for 3. A '2 sigma' ellipse is
    therefore an 86 % region, not 95 %; label the ellipse with p. Use equal axis scaling."""
    import numpy as np
    from matplotlib.patches import Ellipse
    if (prob is None) == (nsig is None):
        raise ValueError('give exactly one of prob or nsig')
    if prob is not None and not 0 < prob < 1:
        raise ValueError('prob must lie in (0, 1)')
    r2 = -2 * math.log(1 - prob) if prob is not None else float(nsig) ** 2
    p = prob if prob is not None else 1 - math.exp(-r2 / 2)
    c = np.asarray(cov, float)[:2, :2]
    if not np.allclose(c, c.T, atol=1e-12 * max(1.0, abs(c).max())):
        raise ValueError('covariance is not symmetric')
    vals, vecs = np.linalg.eigh(c)
    if vals.min() < -1e-12 * max(1.0, vals.max()):
        raise ValueError('covariance is not positive semidefinite')
    vals = np.clip(vals, 0, None)
    big = int(np.argmax(vals))
    angle = math.degrees(math.atan2(vecs[1, big], vecs[0, big]))
    patch = Ellipse(tuple(mean[:2]), 2 * math.sqrt(r2 * vals[big]), 2 * math.sqrt(r2 * vals[1 - big]),
                    angle=angle, **kw)
    ax.add_patch(patch)
    return patch, p


def cmap(colors, name='custom', n=256):
    return LinearSegmentedColormap.from_list(name, colors, N=n)


def iridescent():
    return cmap(TOL_IRIDESCENT, 'tol_iridescent')


def sunset():
    return cmap(TOL_SUNSET, 'tol_sunset')


def ylorbr():
    return cmap(TOL_YLORBR, 'tol_ylorbr')


def _luminance(color):
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in to_rgb(color)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast_ratio(a, b):
    """WCAG 2 contrast ratio between two colours, from 1 to 21."""
    la, lb = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def text_color_for(background, dark=INK, light='#FFFFFF'):
    """Dark or light annotation text for a cell colour, whichever has the higher contrast ratio."""
    return dark if contrast_ratio(background, dark) >= contrast_ratio(background, light) else light


# ---------------------------------------------------------------- demo data guard
def mark_demo(reason='synthetic demo data'):
    """Declare that the figure being built uses placeholder data. While any reason is registered,
    save() stamps every exported figure 'DEMO DATA' and warns, so a template preview cannot pass
    for a result. Delete the call together with the placeholder data it labels."""
    _DEMO.append(reason)


def demo_rng(seed=0, reason='synthetic demo data'):
    """numpy Generator for placeholder data; registers mark_demo(reason)."""
    import numpy as np
    mark_demo(reason)
    return np.random.default_rng(seed)


def is_demo():
    return bool(_DEMO)


def _stamp(fig):
    if any(t.get_gid() == 'pubplot-demo' for t in fig.texts):
        return
    w, h = fig.get_size_inches()
    size = max(14.0, min(w, h) * 72 * 0.13)
    fig.text(0.5, 0.5, 'DEMO DATA', gid='pubplot-demo', rotation=math.degrees(math.atan2(h, w)) * 0.8,
             ha='center', va='center', fontsize=size, fontweight='bold', color='#CC3311', alpha=0.16,
             zorder=1000)


# ---------------------------------------------------------------- lint
def _drawn_texts(fig):
    """Text artists that are actually drawn: ticks inside the view interval, labels, titles,
    annotations, legend entries and figure-level text."""
    found = []

    def add(kind, t):
        if t is not None and t.get_visible() and t.get_text().strip() and t.get_gid() != 'pubplot-demo' \
                and (t.get_alpha() is None or t.get_alpha() > 0):
            found.append((kind, t))

    for ax in fig.axes:
        if not ax.get_visible():
            continue
        for axis in (ax.xaxis, ax.yaxis):
            if not axis.get_visible():
                continue
            lo, hi = sorted(axis.get_view_interval())
            tol = 1e-9 * max(1.0, abs(lo), abs(hi))
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                loc = tick.get_loc()
                if loc is not None and lo - tol <= loc <= hi + tol:
                    add('tick label', tick.label1)
                    add('tick label', tick.label2)
            add('axis label', axis.label)
            add('offset text', axis.get_offset_text())
        for t in (ax.title, getattr(ax, '_left_title', None), getattr(ax, '_right_title', None)):
            add('title', t)
        for t in ax.texts:
            add('text', t)
        legend = ax.get_legend()
        if legend is not None and legend.get_visible():
            for t in legend.get_texts():
                add('legend', t)
            add('legend title', legend.get_title())
    for legend in fig.legends:
        for t in legend.get_texts():
            add('legend', t)
    for t in fig.texts:
        add('figure text', t)
    return found


def lint(fig, min_size=None, overlap_tol=0.8):
    """Check the drawn figure: text below the theme minimum, text clipped by the figure edge,
    overlapping text, hairlines thinner than 0.3 pt. Returns a list of warning strings."""
    min_size = _STATE['min_size'] if min_size is None else min_size
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    k = 72.0 / fig.dpi
    W, H = fig.bbox.width * k, fig.bbox.height * k
    warns, boxes = [], []
    for kind, t in _drawn_texts(fig):
        label = t.get_text().replace('\n', ' ')
        if t.get_fontsize() < min_size - 1e-6:
            warns.append(f'{kind} "{label}" is {t.get_fontsize():.1f} pt, below the {min_size} pt minimum')
        bb = t.get_window_extent(renderer)
        x0, y0, x1, y1 = bb.x0 * k, bb.y0 * k, bb.x1 * k, bb.y1 * k
        if x1 - x0 <= 0 or y1 - y0 <= 0:
            continue
        if x0 < -0.5 or y0 < -0.5 or x1 > W + 0.5 or y1 > H + 0.5:
            warns.append(f'{kind} "{label}" is clipped by the figure edge')
        boxes.append((kind, label, x0, y0, x1, y1))
    for i, (ka, la, ax0, ay0, ax1, ay1) in enumerate(boxes):
        for kb, lb, bx0, by0, bx1, by1 in boxes[i + 1:]:
            ox, oy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
            if ox > overlap_tol and oy > overlap_tol:
                warns.append(f'{ka} "{la}" overlaps {kb} "{lb}" by {ox:.1f} x {oy:.1f} pt')
    for ax in fig.axes:
        for line in ax.get_lines():
            if line.get_visible() and line.get_linestyle() not in ('None', '', ' ') and 0 < line.get_linewidth() < 0.3:
                warns.append(f'line "{line.get_label()}" is {line.get_linewidth():.2f} pt wide and may vanish in print')
    return list(dict.fromkeys(warns))


SAVE_FORMATS = ('svg', 'pdf', 'png', 'eps', 'eps-gray')


def save(fig, out_dir, name, formats=('svg', 'pdf', 'png'), dpi=600, check=True):
    """Save at the figure's exact size (no tight bbox, so the column width is preserved). Lints the
    figure first and stamps it DEMO DATA while placeholder data is registered. Returns the warnings.

    eps is vector EPS (Type 42 fonts; PostScript has no transparency, so translucent artists print
    opaque: use solid tints). eps-gray is <name>-gray.eps, an 8-bit greyscale raster EPS at dpi."""
    unknown = [f for f in formats if f not in SAVE_FORMATS]
    if unknown:
        raise ValueError(f'unknown format(s) {unknown}; choose from {SAVE_FORMATS}')
    os.makedirs(out_dir, exist_ok=True)
    warns = []
    if _DEMO:
        _stamp(fig)
        warns.append('DEMO DATA: placeholder data registered (' + '; '.join(dict.fromkeys(_DEMO)) +
                     '); the figure is stamped and is not a result')
    if check:
        warns += lint(fig)
    if 'eps' in formats:
        clear = [a for a in fig.findobj(lambda a: hasattr(a, 'get_alpha'))
                 if a.get_visible() and a.get_alpha() is not None and a.get_alpha() < 1
                 and a.get_gid() != 'pubplot-demo']
        if clear:
            warns.append(f'EPS has no transparency: {len(clear)} translucent artist(s) will print opaque; '
                         'use solid tints such as pp.tint(color, 0.8) or band(..., solid=True)')
    for w in warns:
        print(f'[pubplot] {name}: {w}', file=sys.stderr)
    written = []
    for fmt in formats:
        if fmt == 'eps-gray':
            continue
        path = os.path.join(out_dir, f'{name}.{fmt}')
        meta = {'Creator': None, 'Producer': None, 'CreationDate': None} if fmt == 'pdf' else (
            {'Date': None, 'Creator': None} if fmt == 'svg' else None)
        fig.savefig(path, dpi=dpi if fmt == 'png' else None, metadata=meta)
        written.append(path)
    if 'eps-gray' in formats:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import render
        png = os.path.join(out_dir, f'{name}.png')
        temp = 'png' not in formats
        if temp:
            fig.savefig(png, dpi=dpi)
        written.append(str(render.write_gray_eps(png, os.path.join(out_dir, f'{name}-gray.eps'), dpi)))
        if temp:
            os.remove(png)
    for path in written:
        print(f'wrote {path}')
    return warns


def template_args(description=''):
    import argparse
    ap = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='figures', help='output directory (default: ./figures)')
    ap.add_argument('--formats', default='svg,pdf,png')
    ap.add_argument('--dpi', type=int, default=600)
    ap.add_argument('--theme', default='default', help=' | '.join(THEMES))
    ap.add_argument('--lang', default='en', help='en | zh')
    args = ap.parse_args()
    args.formats = tuple(f.strip() for f in args.formats.split(',') if f.strip())
    return args


__all__ = ['use', 'figure', 'save', 'lint', 'width_in', 'light_grid', 'panel_label', 'tint', 'band', 'end_label',
           'series_style', 'GRAY_STYLES', 'SAVE_FORMATS', 'chi2_interval', 'anees_bounds', 'cov_ellipse', 'cmap',
           'iridescent', 'sunset', 'ylorbr', 'contrast_ratio', 'text_color_for', 'mark_demo', 'demo_rng',
           'is_demo', 'template_args',
           'WIDTHS_IN', 'THEMES', 'OKABE_ITO', 'TOL_BRIGHT', 'TOL_HIGH_CONTRAST', 'TOL_VIBRANT', 'TOL_MUTED',
           'TOL_IRIDESCENT', 'TOL_YLORBR', 'TOL_SUNSET', 'OURS', 'BASELINES', 'CYCLE', 'INK', 'MUTED', 'GRID']
