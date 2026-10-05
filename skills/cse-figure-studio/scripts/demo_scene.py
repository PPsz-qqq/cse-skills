#!/usr/bin/env python3
"""demo_scene: drawn stand-in imagery for the qualitative templates (18, 19).

The qualitative templates need images to place boxes and rankings on. Random noise looks like a
broken figure, and a real photograph would imply a real result, so the templates draw simple flat
illustrations instead: a street with people and a car, or a person crop in front of a camera
backdrop. Everything draws on axes in logical pixel coordinates with the origin at the top-left (use
pubplot.render_array). These pictures are placeholders. Replace them with your own frames or crops.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle, Wedge  # noqa: E402

SHOES = '#26282C'


def _shade(color, t):
    r, g, b = to_rgb(color)
    return (r * (1 - t), g * (1 - t), b * (1 - t))


def _gradient(ax, x0, y0, x1, y1, top, bottom, n=64):
    """Vertical gradient rectangle from colour top to colour bottom."""
    import numpy as np
    a, b = np.array(to_rgb(top)), np.array(to_rgb(bottom))
    ramp = np.linspace(0, 1, n)[:, None, None]
    ax.imshow(a + (b - a) * ramp, extent=(x0, x1, y1, y0), aspect='auto', interpolation='bilinear', zorder=0)


def _rounded(ax, x0, y0, x1, y1, r, color, z):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle=f'round,pad=0,rounding_size={r}',
                                facecolor=color, edgecolor='none', zorder=z))


def person(ax, x, feet, h, top, legs, hair='#2B2522', skin='#E3B590', bag=None, stride=0.0, flip=False, z=3):
    """Standing or walking person of height h whose feet are at (x, feet). stride in [0, 1]."""
    s = -1 if flip else 1
    ax.add_patch(Ellipse((x, feet + 0.01 * h), 0.46 * h, 0.07 * h, facecolor='#000000', alpha=0.16,
                         edgecolor='none', zorder=z))
    spread = 0.06 * h * stride
    for side in (-1, 1):                                   # legs and shoes
        cx = x + side * (0.06 * h + spread)
        _rounded(ax, cx - 0.045 * h, feet - 0.48 * h, cx + 0.045 * h, feet - 0.03 * h, 0.02 * h, legs, z + 0.1)
        ax.add_patch(Ellipse((cx + s * 0.02 * h, feet - 0.025 * h), 0.12 * h, 0.05 * h, facecolor=SHOES,
                             edgecolor='none', zorder=z + 0.2))
    for side in (-1, 1):                                   # arms behind the torso
        cx = x + side * 0.165 * h
        _rounded(ax, cx - 0.032 * h, feet - 0.80 * h, cx + 0.032 * h, feet - 0.47 * h, 0.03 * h,
                 _shade(top, 0.14), z + 0.25)
        ax.add_patch(Circle((cx, feet - 0.465 * h), 0.03 * h, facecolor=skin, edgecolor='none', zorder=z + 0.26))
    if bag:                                                # backpack strap and pack on one side
        _rounded(ax, x - s * 0.21 * h - 0.06 * h, feet - 0.76 * h, x - s * 0.21 * h + 0.06 * h, feet - 0.52 * h,
                 0.025 * h, bag, z + 0.27)
    _rounded(ax, x - 0.14 * h, feet - 0.83 * h, x + 0.14 * h, feet - 0.44 * h, 0.06 * h, top, z + 0.3)
    if bag:
        ax.add_patch(Polygon([(x - s * 0.10 * h, feet - 0.83 * h), (x - s * 0.06 * h, feet - 0.83 * h),
                              (x + s * 0.10 * h, feet - 0.56 * h), (x + s * 0.06 * h, feet - 0.56 * h)],
                             closed=True, facecolor=_shade(bag, 0.2), edgecolor='none', zorder=z + 0.35))
    ax.add_patch(Rectangle((x - 0.03 * h, feet - 0.87 * h), 0.06 * h, 0.05 * h, facecolor=_shade(skin, 0.08),
                           edgecolor='none', zorder=z + 0.28))
    ax.add_patch(Circle((x, feet - 0.92 * h), 0.075 * h, facecolor=skin, edgecolor='none', zorder=z + 0.4))
    ax.add_patch(Wedge((x, feet - 0.925 * h), 0.08 * h, 180, 360, facecolor=hair, edgecolor='none', zorder=z + 0.5))


def car(ax, x0, bottom, w, h, body='#2F7E86', z=3):
    """Side view of a car occupying x0..x0+w, with its wheels resting on y = bottom."""
    ax.add_patch(Ellipse((x0 + w / 2, bottom + 0.02 * h), 1.04 * w, 0.18 * h, facecolor='#000000', alpha=0.18,
                         edgecolor='none', zorder=z))
    ax.add_patch(Polygon([(x0 + 0.20 * w, bottom - 0.60 * h), (x0 + 0.33 * w, bottom - h),
                          (x0 + 0.70 * w, bottom - h), (x0 + 0.85 * w, bottom - 0.60 * h)],
                         closed=True, facecolor=_shade(body, 0.12), edgecolor='none', zorder=z + 0.1))
    for a, b in ((0.25, 0.49), (0.52, 0.77)):              # side windows
        ax.add_patch(Polygon([(x0 + a * w, bottom - 0.62 * h), (x0 + max(a, 0.35) * w, bottom - 0.93 * h),
                              (x0 + min(b, 0.68) * w, bottom - 0.93 * h), (x0 + b * w, bottom - 0.62 * h)],
                             closed=True, facecolor='#D5E1EA', edgecolor='none', zorder=z + 0.2))
    _rounded(ax, x0, bottom - 0.64 * h, x0 + w, bottom - 0.16 * h, 0.12 * h, body, z + 0.3)
    ax.add_patch(Rectangle((x0 + w - 0.05 * w, bottom - 0.52 * h), 0.04 * w, 0.10 * h, facecolor='#F2E3B3',
                           edgecolor='none', zorder=z + 0.4))
    ax.add_patch(Rectangle((x0 + 0.01 * w, bottom - 0.52 * h), 0.035 * w, 0.10 * h, facecolor='#C8574A',
                           edgecolor='none', zorder=z + 0.4))
    for fx in (0.24, 0.76):
        ax.add_patch(Circle((x0 + fx * w, bottom - 0.17 * h), 0.17 * h, facecolor=SHOES, edgecolor='none', zorder=z + 0.5))
        ax.add_patch(Circle((x0 + fx * w, bottom - 0.17 * h), 0.075 * h, facecolor='#9AA1A8', edgecolor='none',
                            zorder=z + 0.6))


def street(ax, w, h, horizon=0.47, curb=0.6):
    """Flat street backdrop: sky, a row of buildings, pavement, curb and a two-lane road."""
    yh, yc = horizon * h, curb * h
    _gradient(ax, 0, 0, w, yh, '#D6E1EB', '#EEF2F5')
    blocks = [(0.00, 0.15, 0.21, '#C5CED8'), (0.15, 0.29, 0.29, '#B6C1CD'), (0.29, 0.40, 0.18, '#CCD3DB'),
              (0.40, 0.58, 0.33, '#B1BDCA'), (0.58, 0.69, 0.23, '#C8D0D8'), (0.69, 0.87, 0.27, '#BAC4CF'),
              (0.87, 1.00, 0.20, '#C3CCD5')]
    for a, b, tall, color in blocks:
        x0, x1, top = a * w, b * w, yh - tall * h
        ax.add_patch(Rectangle((x0, top), x1 - x0, yh - top, facecolor=color, edgecolor='none', zorder=1))
        win = _shade(color, 0.12)
        for wy in range(int(top + 0.035 * h), int(yh - 0.05 * h), max(4, int(0.055 * h))):
            for wx in range(int(x0 + 0.02 * w), int(x1 - 0.025 * w), max(4, int(0.035 * w))):
                ax.add_patch(Rectangle((wx, wy), 0.016 * w, 0.028 * h, facecolor=win, edgecolor='none', zorder=1.1))
    ax.add_patch(Rectangle((0, yh), w, yc - yh, facecolor='#D7D2C8', edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((0, yh), w, 0.006 * h, facecolor='#C4BEB2', edgecolor='none', zorder=1.1))
    ax.add_patch(Rectangle((0, yc), w, 0.018 * h, facecolor='#A8A49C', edgecolor='none', zorder=1.1))
    _gradient(ax, 0, yc + 0.018 * h, w, h, '#A2A8AE', '#8E949B')
    lane = yc + 0.018 * h + 0.25 * (h - yc)
    for x in range(-10, int(w), int(0.13 * w)):
        ax.add_patch(Rectangle((x, lane), 0.075 * w, 0.012 * h, facecolor='#E6E8EA', edgecolor='none', zorder=1.2))


def backdrop(ax, w, h, wall, floor, split=0.64):
    """Plain camera backdrop for a person crop: wall with a soft gradient, then floor."""
    _gradient(ax, 0, 0, w, split * h, wall, _shade(wall, 0.05))
    ax.add_patch(Rectangle((0, split * h), w, (1 - split) * h, facecolor=floor, edgecolor='none', zorder=0.5))
    ax.add_patch(Rectangle((0, split * h), w, 0.012 * h, facecolor=_shade(floor, 0.12), edgecolor='none', zorder=0.6))


__all__ = ['person', 'car', 'street', 'backdrop']
