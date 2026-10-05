# API reference

The five scripts and the calls a figure needs. Signatures are abbreviated to the arguments used in
practice; the docstrings in each file are complete.

## pubplot: data plots on matplotlib

[pubplot.py](../scripts/pubplot.py). Import with `import pubplot as pp` after putting the scripts
directory on `sys.path`, as every template does.

```python
pp.use(theme='default', lang='en')          # theme: default | ieee | elsevier | springer | aas
fig, ax = pp.figure('ieee-single', aspect=0.62, nrows=1, ncols=1, **subplots_kw)
ax.plot(x, y, color=pp.OURS, label=pp.tr('Ours', '本文'))
pp.save(fig, 'fig', 'fig3-rmse', formats=('pdf', 'svg', 'png'), dpi=600)   # lints, stamps DEMO
```

| Call | Does |
|---|---|
| `use(theme, lang)` | rcParams for the theme: fonts (CJK fallback with `lang='zh'`), sizes, weights, colours, embedded TrueType fonts |
| `size(kind)` | the theme's size in pt for `base`, `label`, `tick`, `legend`, `title`, `annot`, `min` |
| `tr(en, zh)` | the label for the active language; Chinese next to `$...$` is made renderable |
| `cjk_math(s)` | that conversion on its own, for labels built without `tr` |
| `figure(width, height=None, aspect=0.62, nrows, ncols)` | figure at the exact printed width with constrained layout |
| `canvas(width, height)`, `place(fig, left, top, w, h)` | a figure without layout engine, and axes placed in inches from the top-left |
| `width_in(width)` | inches from a width key, a number, or `'241.14pt'`, `'88mm'`, `'3.25in'`, `'21pc'`, `'252bp'` |
| `light_grid(ax, axis='y')`, `panel_label(ax, '(a)')` | value-axis grid; bold panel label outside the axes |
| `band(ax, x, y, lo, hi, color, solid=False)` | line with a shaded interval; `solid=True` uses an opaque tint (EPS) |
| `end_label(ax, x, y, text, color)` | direct label at a line end |
| `label_points(ax, x, y, labels, marker_size, colors, weights, order)` | collision-free direct labels for scatter points |
| `series_style(i, gray=False, ours=False)` | colour, or tone plus dash plus marker for greyscale print |
| `cov_ellipse(ax, mean, cov, prob=0.95 \| nsig=2, **patch_kw)` | covariance region with exact 2-D probability; returns `(patch, p)` |
| `anees_bounds(N, n_x, alpha=0.05)`, `chi2_interval(df, alpha)` | per-step ANEES acceptance interval, chi-square quantiles |
| `blues()`, `iridescent()`, `sunset()`, `ylorbr()`, `cmap(colors)` | colour maps |
| `contrast_ratio(a, b)`, `text_color_for(bg)`, `label_fill(color)`, `tint(color, t)` | WCAG contrast helpers and an opaque tint |
| `render_array(draw, w, h, scale)` | rasterise `draw(ax)` (pixel coordinates, origin top-left) into an RGB array |
| `image_panel(ax, img, size=(w, h), frame, lw)` | image in pixel coordinates with a thin frame and no ticks |
| `box(ax, (x0, y0, x1, y1), color, label, dashed)` | bounding box with a readable label tab kept inside the panel |
| `chip(ax, text)` | small dark chip in an image corner (frame index, camera) |
| `mark_demo(reason)`, `demo_rng(seed, reason)`, `is_demo()` | register placeholder data; every save is then stamped DEMO DATA |
| `lint(fig)` | text below the minimum, clipped or overlapping text, hairlines; `save` runs it |
| `save(fig, out_dir, name, formats, dpi)` | `svg`, `pdf`, `png`, `eps` (vector), `eps-gray` (greyscale raster EPS) |

Constants: `OURS`, `BASELINES`, `CYCLE`, `IDS`, `GOOD`, `BAD`, `INK`, `MUTED`, `GRID`, `OKABE_ITO`, the
Tol schemes, `BLUES`, `WIDTHS_IN`, `THEMES`.

## figkit: diagrams as SVG

[figkit.py](../scripts/figkit.py). Coordinates are points at final size, origin top-left.

```python
from figkit import Figure, TONES, template_args
fig = Figure('ieee-double', 180, theme='ieee')          # width key or '241.14pt'; height in pt
a = fig.box(20, 40, 90, 36, 'Backbone', 'multi-scale features', tone='gray')
b = fig.box(140, 40, 90, 36, 'Matching', 'ours', tone='blue', emphasis=True)
fig.arrow(a.right, b.left, label='$\\mathcal{D}_t$')
fig.export('fig', 'fig1-framework', ('svg', 'pdf', 'png'))   # prints lint warnings
```

| Call | Does |
|---|---|
| `box`, `pill`, `io`, `diamond`, `cylinder` | module card, terminator, I/O parallelogram, decision, store; titles wrap to the box |
| `group(x, y, w, h, label, tone)` | stage container with a label chip; draw it first |
| `op(cx, cy, '+' \| 'x' \| 'c' \| symbol)`, `dot(x, y)` | operator node, take-off point |
| `tensor`, `matrix`, `image_icon`, `uav`, `robot`, `beacon` | feature cuboid, matrix glyph, image stack, platform icons |
| `arrow(p0, p1, route, label, dashed)` | orthogonal connector (`'auto'`, `'hv'`, `'vh'`, `'hvh'`, `'vhv'` or waypoints) with optional label |
| `line`, `curve` | plain line; quadratic arc for skips and feedback |
| `text(x, y, s, size, weight, anchor, halo, rotate)` | label with math markup; `halo` puts a chip behind it |
| `legend(x, y, items, align)`, `panel(x, y, '(a)')`, `brace` | legend row, panel label, bracket |
| `Node.left/right/top/bottom`, `port(side, t)` | anchor points for arrows |
| `lint()`, `save(path)`, `export(dir, name, formats, dpi)` | overflow, overlap, out-of-canvas and size checks; SVG; SVG plus pdf, png, eps, eps-gray |

Themes `default`, `ieee`, `elsevier`, `springer`, `aas`; `fig.t.title`, `fig.t.body`, `fig.t.small`
are the sizes to pass as `title_size` and `sub_size`. Tones: blue, teal, orange, cyan, magenta, red,
green, purple, indigo, sand, gray, white.

## render: export, previews, checks

[render.py](../scripts/render.py).

```text
python render.py --doctor                     # libraries, browser, EPS converters, Latin and CJK fonts
python render.py fig.svg --formats pdf,png --dpi 600
python render.py fig.svg --formats eps        # vector EPS: needs Ghostscript, pdftops or Inkscape
python render.py fig.svg --formats eps-gray   # 8-bit greyscale raster EPS, ASCII, no preview
python render.py fig.png --preview            # original | grey | deutan | protan sheet
python render.py fig.pdf                      # page size, pages, fonts, embedded, Type 3
```

Set `CSE_FIGURE_BROWSER` to a Chrome, Edge or Chromium executable if none is found.

## gallery: regression test and contact sheets

[gallery.py](../scripts/gallery.py) runs every template and exits non-zero on an error or a lint
warning. Run it after changing an engine or a template, under the theme and language you use.

```text
python gallery.py --out <scratch> [--theme ieee] [--lang zh] [--only 10,11] [--sheet <prefix>]
```

## demo_scene: stand-in illustrations

[demo_scene.py](../scripts/demo_scene.py): `street`, `person`, `car` and `backdrop` draw the flat
illustrations used by templates 18 and 19 inside `pp.render_array`. They exist so a template can
show layout without implying a result; replace them with real images.
