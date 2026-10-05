#!/usr/bin/env python3
"""gallery: run every template, report lint, and optionally compose contact sheets.

  python gallery.py --out _gallery                          # render all templates as PNG, report
  python gallery.py --out _gallery --theme ieee              # under a venue theme
  python gallery.py --out _gallery --theme aas --lang zh     # Chinese labels, 自动化学报 fonts
  python gallery.py --out _gallery --only 10,11,18           # a subset
  python gallery.py --out _gallery --sheet gallery           # also gallery-{diagrams,plots,qualitative}.png

This is the regression test of the template set: run it after editing figkit.py, pubplot.py,
demo_scene.py or a template. Exit status is 1 when a template fails or prints a lint warning; the
DEMO DATA notice of a template that still holds placeholder data is reported but is not a failure.
Write outputs to a scratch or project directory, never inside the installed skill.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / 'templates'
TITLES = {1: 'Framework overview', 2: 'Algorithm flowchart', 3: 'Network architecture', 4: 'Module detail',
          5: 'Control block diagram', 6: 'Cooperative system', 7: 'Timing diagram', 8: 'Taxonomy tree',
          9: 'Paradigm comparison', 10: 'Curves with seed bands', 11: 'Ablation bars', 12: 'Accuracy-speed trade-off',
          13: 'Sensitivity heatmap', 14: 'Raincloud distributions', 15: 'Filter consistency (ANEES)',
          16: 'Trajectories with covariance', 17: 'Precision-recall curves', 18: 'Tracking strip',
          19: 'Re-ID ranking'}
# group name, template numbers, target row height in pixels (None: one figure per full-width row)
GROUPS = [('diagrams', range(1, 10), 470), ('plots', range(10, 18), 360), ('qualitative', range(18, 20), None)]
ACCENT, INK, MUTED, LINE, PAPER = (0, 119, 187), (35, 39, 46), (95, 102, 112), (222, 226, 231), (246, 247, 249)


def templates(only=None):
    found = []
    for path in sorted(TEMPLATES.glob('[0-9][0-9]_*.py')):
        n = int(path.name[:2])
        if only is None or n in only:
            found.append((n, path))
    return found


def run_one(n, path, out, theme, lang, dpi, formats):
    text = path.read_text(encoding='utf-8')
    plots = 'import pubplot' in text
    cmd = [sys.executable, str(path), '--out', str(out), '--formats', formats, '--dpi', str(dpi)]
    if theme:
        cmd += ['--theme', theme]
    if lang and plots:
        cmd += ['--lang', lang]
    t0 = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    lines = [s for s in proc.stderr.splitlines() if s.strip()]
    demo = [s for s in lines if 'DEMO DATA' in s]
    lint = [s for s in lines if re.match(r'\[(figkit|pubplot)\]', s) and 'DEMO DATA' not in s]
    other = [s for s in lines if s not in demo and s not in lint]
    return {'n': n, 'name': path.stem, 'ok': proc.returncode == 0 and not other, 'code': proc.returncode,
            'demo': bool(demo), 'lint': lint, 'errors': other, 'seconds': time.perf_counter() - t0,
            'png': out / f'{path.stem}.png'}


def _font(bold, size):
    from PIL import ImageFont
    try:
        from matplotlib import font_manager
        family = font_manager.FontProperties(family=['Arial', 'Helvetica', 'DejaVu Sans'],
                                             weight='bold' if bold else 'normal')
        return ImageFont.truetype(font_manager.findfont(family), size)
    except Exception:  # noqa: BLE001 - any font failure falls back to the bitmap default
        return ImageFont.load_default()


def _rows(aspects, width, target, gap, pad):
    """Justified rows in the given order: each row's figures share one height chosen so the row fills
    the width exactly, and a row closes when adding the next figure moves that height further from
    the target. Returns [(indices, figure height)]."""
    def height(idx):
        return (width - (len(idx) + 1) * gap - 2 * pad * len(idx)) / sum(aspects[i] for i in idx)
    if target is None:                                          # one figure per full-width row
        return [([i], height([i])) for i in range(len(aspects))]
    rows, cur = [], []
    for i in range(len(aspects)):
        if cur and abs(height(cur + [i]) - target) > abs(height(cur) - target):
            rows.append((cur, height(cur)))
            cur = []
        cur.append(i)
    cap = 1.25 * max(h for _idx, h in rows) if rows else 1.8 * target
    rows.append((cur, min(height(cur), cap)))                   # a short last row is not blown up
    return rows


def contact_sheet(items, target, path, width=1800):
    """White cards on a light paper background in justified rows; number and title under each figure.
    1800 px is twice the width a README shows, so the sheet stays sharp on high-density screens."""
    from PIL import Image, ImageDraw
    k = width / 2280                                            # geometry was designed at 2280 px
    gap, pad, label_h, fs0 = round(30 * k), round(24 * k), round(62 * k), round(30 * k)
    target = None if target is None else target * k
    images = [(n, title, Image.open(png).convert('RGB')) for n, title, png in items]
    rows = _rows([im.width / im.height for _n, _t, im in images], width, target, gap, pad)
    total_h = sum(h + 2 * pad + label_h for _idx, h in rows) + (len(rows) + 1) * gap
    sheet = Image.new('RGB', (width, round(total_h)), PAPER)
    draw = ImageDraw.Draw(sheet)
    f_num, f_title = _font(True, fs0), _font(False, fs0)
    y = gap
    for idx, h in rows:
        widths = [round(images[i][2].width * h / images[i][2].height) for i in idx]
        row_w = sum(widths) + len(idx) * 2 * pad + (len(idx) - 1) * gap
        x = (width - row_w) // 2
        card_h = round(h) + 2 * pad + label_h
        for i, w in zip(idx, widths):
            n, title, im = images[i]
            draw.rounded_rectangle((x, y, x + w + 2 * pad, y + card_h), radius=round(18 * k), fill=(255, 255, 255),
                                   outline=LINE, width=2)
            sheet.paste(im.resize((w, round(h)), Image.LANCZOS), (x + pad, y + pad))
            ty = y + card_h - label_h + round(8 * k)
            num = f'{n:02d}'
            draw.text((x + pad, ty), num, font=f_num, fill=ACCENT)
            room = w - draw.textlength(num, font=f_num) - round(14 * k)
            font, text = f_title, title
            for fs in (fs0 - 2, fs0 - 4, fs0 - 6, fs0 - 8):      # shrink a long title to its card first
                if draw.textlength(text, font=font) <= room:
                    break
                font = _font(False, fs)
            while draw.textlength(text, font=font) > room and len(text) > 4:
                text = text[:-2].rstrip() + '…'
            draw.text((x + pad + draw.textlength(num, font=f_num) + round(14 * k), ty + (fs0 - font.size) // 2), text,
                      font=font, fill=INK)
            x += w + 2 * pad + gap
        y += card_h + gap
    # Full-colour PNG: a 256-colour palette shifts small accent areas (identity colours) and bands
    # gradients, which a gallery meant to show colour choices cannot afford.
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)
    return path


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):         # a GBK console must not crash on a replacement char
        try:
            stream.reconfigure(errors='replace')
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True, help='scratch directory for the rendered templates')
    ap.add_argument('--theme', default=None, help='default | ieee | elsevier | springer | aas')
    ap.add_argument('--lang', default=None, help='en | zh (data templates only)')
    ap.add_argument('--dpi', type=int, default=300)
    ap.add_argument('--formats', default='png', help='comma list passed to every template (png needed for sheets)')
    ap.add_argument('--only', default=None, help='comma list of template numbers, e.g. 10,11,18')
    ap.add_argument('--sheet', default=None, help='path prefix for contact sheets: <prefix>-<group>.png')
    a = ap.parse_args(argv)
    out = Path(a.out).resolve()
    if TEMPLATES.resolve() in (out, *out.parents) or HERE.parent.resolve() == out:
        ap.error('write outputs outside the skill bundle')
    out.mkdir(parents=True, exist_ok=True)
    only = {int(s) for s in a.only.split(',')} if a.only else None
    results = [run_one(n, p, out, a.theme, a.lang, a.dpi, a.formats) for n, p in templates(only)]
    failed = 0
    for r in results:
        status = 'FAIL' if not r['ok'] else ('WARN' if r['lint'] else 'ok')
        failed += status != 'ok'
        print(f"{status:<4} {r['name']:<28} {r['seconds']:5.1f}s  lint={len(r['lint'])}"
              f"{'  demo-data' if r['demo'] else ''}")
        for line in (r['errors'] + r['lint'])[:6]:
            print(f'       {line}')
    print(f"{len(results)} template(s), {failed} with problems; theme={a.theme or 'default'} lang={a.lang or 'en'}")
    if a.sheet:
        by_n = {r['n']: r for r in results if r['ok'] and r['png'].exists()}
        for group, numbers, target in GROUPS:
            items = [(n, TITLES.get(n, by_n[n]['name']), by_n[n]['png']) for n in numbers if n in by_n]
            if items:
                print(f'wrote {contact_sheet(items, target, Path(f"{a.sheet}-{group}.png"))}')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
