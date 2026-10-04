#!/usr/bin/env python3
"""Render SVG figures to PDF and PNG with a headless Chromium browser (Chrome, Edge or Chromium),
make grayscale and colour-vision-deficiency previews, and check exported PDFs.

  python render.py --doctor                     # what this machine can build, export and preview
  python render.py fig.svg                      # fig.pdf + fig.png (300 dpi) beside the SVG
  python render.py fig.svg --formats png --dpi 600
  python render.py fig.png --preview            # fig.preview.png: original | grey | deutan | protan
  python render.py fig.pdf                      # page size, page count, embedded fonts

PDF text stays vector with embedded font subsets. --preview needs Pillow and numpy; the PDF check
needs nothing. Set CSE_FIGURE_BROWSER to a browser executable if none is found automatically.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

_CANDIDATES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
]


def find_browser():
    env = os.environ.get('CSE_FIGURE_BROWSER')
    if env and Path(env).exists():
        return env
    for name in ('chrome', 'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'msedge',
                 'microsoft-edge'):
        found = shutil.which(name)
        if found:
            return found
    for cand in _CANDIDATES:
        if Path(cand).exists():
            return cand
    return None


def svg_size_pt(svg_text):
    """Return (width, height) in points from the root <svg> element."""
    root = re.search(r'<svg\b[^>]*>', svg_text, re.S)
    if not root:
        raise ValueError('no <svg> element found')
    tag = root.group(0)
    factor = {'pt': 1.0, 'px': 0.75, '': 0.75, 'in': 72.0, 'mm': 72 / 25.4, 'cm': 72 / 2.54}

    def dim(name):
        m = re.search(rf'\b{name}="([\d.]+)\s*(pt|px|in|mm|cm)?"', tag)
        return float(m.group(1)) * factor[m.group(2) or ''] if m else None

    w, h = dim('width'), dim('height')
    if w is None or h is None:
        vb = re.search(r'viewBox="[\d.\-]+[ ,]+[\d.\-]+[ ,]+([\d.]+)[ ,]+([\d.]+)"', tag)
        if not vb:
            raise ValueError('SVG has neither width/height nor viewBox')
        w, h = float(vb.group(1)) * 0.75, float(vb.group(2)) * 0.75
    return w, h


def _html(svg_text, w, h, transparent=False):
    # The absolutely positioned SVG inside a fixed-size, clipped page avoids a blank second PDF page.
    svg_text = re.sub(r'<\?xml[^>]*\?>', '', svg_text).strip()
    bg = 'transparent' if transparent else '#FFFFFF'
    return ('<!doctype html><html><head><meta charset="utf-8"><style>'
            f'@page{{size:{w:.3f}pt {h:.3f}pt;margin:0}}'
            f'html,body{{margin:0;padding:0;width:{w:.3f}pt;height:{h:.3f}pt;overflow:hidden;background:{bg}}}'
            'svg{position:absolute;left:0;top:0;display:block}'
            f'</style></head><body>{svg_text}</body></html>')


def _run(browser, args, timeout):
    with tempfile.TemporaryDirectory(prefix='cse-fig-', ignore_cleanup_errors=True) as profile:
        cmd = [browser, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
               '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--disable-background-networking',
               f'--user-data-dir={profile}', *args]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout, check=False)


FORMATS = ('pdf', 'png', 'eps', 'eps-gray')


def render_svg(svg_path, formats=('pdf', 'png'), dpi=300, out_dir=None, transparent=False, browser=None,
               timeout=120):
    """Render one SVG file; returns the list of written paths.

    pdf and png come from the browser. eps is vector EPS converted from the PDF by Ghostscript,
    pdftops or Inkscape. eps-gray is <name>-gray.eps, an 8-bit greyscale raster EPS at dpi built
    from the PNG (ASCII, no preview), the mode the 自动化学报 template describes."""
    formats = tuple(formats)
    unknown = [f for f in formats if f not in FORMATS]
    if unknown:
        raise ValueError(f'unknown format(s) {unknown}; choose from {FORMATS}')
    svg_path = Path(svg_path).resolve()
    out_dir = Path(out_dir).resolve() if out_dir else svg_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    browser = browser or find_browser()
    if not browser:
        raise RuntimeError('No Chrome/Edge/Chromium found. Install one or set CSE_FIGURE_BROWSER; the SVG is '
                           'still usable and can be converted with Inkscape or rsvg-convert.')
    text = svg_path.read_text(encoding='utf-8')
    w, h = svg_size_pt(text)
    written = []
    pdf_out, png_out = out_dir / (svg_path.stem + '.pdf'), out_dir / (svg_path.stem + '.png')
    with tempfile.TemporaryDirectory(prefix='cse-fig-html-', ignore_cleanup_errors=True) as tmp:
        page = Path(tmp) / 'figure.html'
        page.write_text(_html(text, w, h, transparent), encoding='utf-8')
        url = page.as_uri()
        if 'pdf' in formats or 'eps' in formats:
            if pdf_out.exists():
                pdf_out.unlink()
            _run(browser, [f'--print-to-pdf={pdf_out}', '--no-pdf-header-footer', '--print-to-pdf-no-header',
                           '--run-all-compositor-stages-before-draw', url], timeout)
            if not pdf_out.exists() or pdf_out.stat().st_size == 0:
                raise RuntimeError(f'PDF export failed for {svg_path}')
        if 'png' in formats or 'eps-gray' in formats:
            if png_out.exists():
                png_out.unlink()
            scale = dpi / 96.0
            _run(browser, [f'--force-device-scale-factor={scale:.4f}',
                           f'--window-size={math.ceil(w * 4 / 3)},{math.ceil(h * 4 / 3)}',
                           f'--default-background-color={"00000000" if transparent else "FFFFFFFF"}',
                           f'--screenshot={png_out}', url], timeout)
            if not png_out.exists() or png_out.stat().st_size == 0:
                raise RuntimeError(f'PNG export failed for {svg_path}')
            _optimize_png(png_out, dpi)
    if 'pdf' in formats:
        written.append(pdf_out)
    if 'png' in formats:
        written.append(png_out)
    if 'eps' in formats:
        written.append(pdf_to_eps(pdf_out, out_dir / (svg_path.stem + '.eps'), timeout))
    if 'eps-gray' in formats:
        written.append(write_gray_eps(png_out, out_dir / (svg_path.stem + '-gray.eps'), dpi))
    for intermediate, fmt in ((pdf_out, 'pdf'), (png_out, 'png')):
        if fmt not in formats and intermediate.exists():
            intermediate.unlink()
    return written


def pdf_to_eps(pdf_path, eps_path=None, timeout=120):
    """Vector EPS from a one-page PDF with Ghostscript, pdftops or Inkscape (first one found)."""
    pdf_path = Path(pdf_path)
    eps_path = Path(eps_path) if eps_path else pdf_path.with_suffix('.eps')
    if eps_path.exists():
        eps_path.unlink()
    for name in _EPS_TOOLS:
        exe = shutil.which(name)
        if not exe:
            continue
        if name.startswith('gs'):
            cmd = [exe, '-q', '-dNOPAUSE', '-dBATCH', '-dSAFER', '-sDEVICE=eps2write', '-dEPSCrop',
                   f'-sOutputFile={eps_path}', str(pdf_path)]
        elif name == 'pdftops':
            cmd = [exe, '-eps', str(pdf_path), str(eps_path)]
        else:
            cmd = [exe, str(pdf_path), '--export-type=eps', f'--export-filename={eps_path}']
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout, check=False)
        if eps_path.exists() and eps_path.stat().st_size > 0:
            return eps_path
    raise RuntimeError('Vector EPS needs Ghostscript, pdftops (poppler) or Inkscape, and none produced a file. '
                       'Use eps-gray for a 600 dpi greyscale raster EPS, or ask the journal whether PDF is accepted.')


def write_gray_eps(png_path, eps_path=None, dpi=None):
    """8-bit DeviceGray raster EPS, ASCII hex data, no preview, physical size = pixels / dpi.
    Transparent pixels are composited onto white. Needs Pillow."""
    from PIL import Image
    png_path = Path(png_path)
    eps_path = Path(eps_path) if eps_path else png_path.with_name(png_path.stem + '-gray.eps')
    with Image.open(png_path) as im:
        im.load()
        if dpi is None:
            dpi = float((im.info.get('dpi') or (300, 300))[0])
        rgba = im.convert('RGBA')
    flat = Image.new('RGBA', rgba.size, (255, 255, 255, 255))
    flat.alpha_composite(rgba)
    gray = flat.convert('L')
    wpx, hpx = gray.size
    wpt, hpt = wpx * 72.0 / dpi, hpx * 72.0 / dpi
    data = gray.tobytes().hex().upper()
    lines = '\n'.join(data[i:i + 76] for i in range(0, len(data), 76))
    eps = (f'%!PS-Adobe-3.0 EPSF-3.0\n%%BoundingBox: 0 0 {math.ceil(wpt)} {math.ceil(hpt)}\n'
           f'%%HiResBoundingBox: 0 0 {wpt:.4f} {hpt:.4f}\n%%Creator: cse-figure-studio render.py\n'
           f'%%Title: {png_path.stem} ({wpx}x{hpx} px, {dpi:g} dpi, DeviceGray)\n%%LanguageLevel: 1\n'
           '%%DocumentData: Clean7Bit\n%%Pages: 1\n%%EndComments\n%%Page: 1 1\ngsave\n'
           f'{wpt:.4f} {hpt:.4f} scale\n/cseline {wpx} string def\n'
           f'{wpx} {hpx} 8 [{wpx} 0 0 -{hpx} 0 {hpx}]\n{{currentfile cseline readhexstring pop}} image\n'
           f'{lines}\ngrestore\nshowpage\n%%Trailer\n%%EOF\n')
    eps_path.write_text(eps, encoding='ascii', newline='\n')
    return eps_path


def read_gray_eps(eps_path):
    """Decode an EPS written by write_gray_eps back to (width, height, bytes), for self-checks."""
    text = Path(eps_path).read_text(encoding='ascii')
    m = re.search(r'^(\d+) (\d+) 8 \[', text, re.M)
    body = text.split('readhexstring pop} image\n', 1)[1].split('\ngrestore', 1)[0]
    return int(m.group(1)), int(m.group(2)), bytes.fromhex(body.replace('\n', ''))


def _optimize_png(path, dpi=None):
    """Recompress the PNG and record its resolution, so the printed size survives a re-import."""
    try:
        from PIL import Image
    except ImportError:
        return
    with Image.open(path) as im:
        im.load()
        im.save(path, optimize=True, **({'dpi': (dpi, dpi)} if dpi else {}))


def check_pdf(path):
    """Report MediaBox, page count and font embedding of a PDF written by a browser or matplotlib."""
    data = Path(path).read_bytes()
    boxes = re.findall(rb'/MediaBox\s*\[\s*([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s*\]', data)
    pages = len(re.findall(rb'/Type\s*/Page(?![a-z])', data))
    fonts = sorted({m.decode('latin-1') for m in re.findall(rb'/BaseFont\s*/([^\s/\[\]<>]+)', data)})
    embedded = len(re.findall(rb'/FontFile[23]?\b', data))
    type3 = len(re.findall(rb'/Subtype\s*/Type3', data))
    report = {'pages': pages, 'fonts': fonts, 'embedded_font_files': embedded, 'type3_fonts': type3}
    if boxes:
        x0, y0, x1, y1 = map(float, boxes[0])
        report['size_pt'] = (round(x1 - x0, 2), round(y1 - y0, 2))
        report['size_mm'] = (round((x1 - x0) * 25.4 / 72, 1), round((y1 - y0) * 25.4 / 72, 1))
    report['fonts_ok'] = bool(fonts) and embedded + type3 >= 1 and not type3
    if not fonts:
        report['fonts_ok'] = True        # no text at all
    return report


# Machado, Oliveira & Fernandes (2009), IEEE TVCG 15(6): severity-1.0 matrices in linear RGB.
_CVD = {
    'deutan': ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    'protan': ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    'tritan': ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def preview(png_path, out=None, kinds=('grey', 'deutan', 'protan')):
    """Write a side-by-side sheet: original, greyscale and simulated colour-vision deficiencies."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    src = Image.open(png_path).convert('RGB')
    arr = np.asarray(src).astype(np.float64) / 255.0
    lin = np.where(arr <= 0.04045, arr / 12.92, ((arr + 0.055) / 1.055) ** 2.4)
    tiles = [('original', src)]
    for kind in kinds:
        if kind == 'grey':
            y = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
            rgb = np.repeat(y[..., None], 3, axis=2)
        else:
            m = np.array(_CVD[kind])
            rgb = np.clip(lin @ m.T, 0, 1)
        enc = np.where(rgb <= 0.0031308, rgb * 12.92, 1.055 * np.power(rgb, 1 / 2.4) - 0.055)
        tiles.append((kind, Image.fromarray((np.clip(enc, 0, 1) * 255 + 0.5).astype('uint8'))))
    w, h = src.size
    label_h = max(18, h // 22)
    sheet = Image.new('RGB', (w * len(tiles) + 12 * (len(tiles) - 1), h + label_h), 'white')
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('arial.ttf', int(label_h * 0.7))
    except OSError:
        font = ImageFont.load_default()
    for i, (name, im) in enumerate(tiles):
        x = i * (w + 12)
        sheet.paste(im, (x, label_h))
        draw.text((x + 4, 2), name, fill=(60, 60, 60), font=font)
    out = Path(out) if out else Path(png_path).with_suffix('.preview.png')
    sheet.save(out, optimize=True)
    return out


_FONTS = {'Latin sans': ['Arial', 'Helvetica', 'Liberation Sans'],
          'Latin serif': ['Times New Roman', 'Times', 'Liberation Serif'],
          'Chinese serif (Song)': ['SimSun', 'Songti SC', 'Noto Serif CJK SC', 'Noto Serif SC'],
          'Chinese sans (Hei)': ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'Noto Sans SC', 'PingFang SC']}
_EPS_TOOLS = ('gswin64c', 'gswin32c', 'gs', 'pdftops', 'inkscape')


def doctor():
    """Report the capabilities this machine actually has; returns a dict of booleans."""
    import importlib
    import platform
    caps = {}
    print(f'python        {platform.python_version()}  ({sys.executable})')
    versions = {}
    for mod, role in (('matplotlib', 'data figures (pubplot templates)'), ('numpy', 'data figures, previews'),
                      ('scipy', 'optional: exact chi-square bounds'), ('PIL', 'optional: PNG optimisation, --preview')):
        try:
            versions[mod] = getattr(importlib.import_module(mod), '__version__', 'present')
        except Exception:  # noqa: BLE001 - any import failure means the capability is absent
            versions[mod] = None
        print(f'{"Pillow" if mod == "PIL" else mod:<13} {versions[mod] or "MISSING":<10} {role}')
    browser = find_browser()
    print(f'browser       {browser or "MISSING"}  (SVG to PDF/PNG)')
    others = {name: shutil.which(name) for name in ('inkscape', 'rsvg-convert', 'gswin64c', 'gs', 'pdftops')}
    for name, path in others.items():
        print(f'{name:<13} {path or "not found"}  (alternative converter; vector EPS from SVG/PDF)')
    caps['eps_vector_from_svg'] = any(shutil.which(n) for n in _EPS_TOOLS)
    if versions['matplotlib']:
        from matplotlib import font_manager
        names = {f.name for f in font_manager.fontManager.ttflist}
        for group, fams in _FONTS.items():
            have = [f for f in fams if f in names]
            print(f'fonts         {group:<20} {", ".join(have) if have else "NONE (fallback face will be used)"}')
            caps[f'font:{group}'] = bool(have)
    else:
        print('fonts         not checked (matplotlib missing)')
    caps.update(svg=True, pdf_png=bool(browser), plots=bool(versions['matplotlib'] and versions['numpy']),
                preview=bool(versions['PIL'] and versions['numpy']))
    print('capabilities  diagrams to SVG: yes | SVG to PDF/PNG: {} | data plots: {} | grey/CVD preview: {}'.format(
        *('yes' if caps[k] else 'NO' for k in ('pdf_png', 'plots', 'preview'))))
    print('              vector EPS: plots {} (matplotlib), diagrams {} | raster grey EPS (eps-gray): {}'.format(
        'yes' if caps['plots'] else 'NO', 'yes' if caps['eps_vector_from_svg'] else 'NO (needs Ghostscript, '
        'pdftops or Inkscape)', 'yes' if versions['PIL'] and caps['pdf_png'] else 'NO'))
    if not browser:
        print('              without a browser, deliver the SVG and state "PDF/PNG export: not performed"')
    return caps


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputs', nargs='*', help='SVG to render, PNG to preview, or PDF to check')
    ap.add_argument('--doctor', action='store_true', help='report available libraries, browser and fonts')
    ap.add_argument('--formats', default='pdf,png', help='comma list for SVG input: pdf,png')
    ap.add_argument('--dpi', type=int, default=300)
    ap.add_argument('--out-dir', default=None)
    ap.add_argument('--transparent', action='store_true')
    ap.add_argument('--preview', action='store_true', help='write a grey/CVD preview sheet for PNG inputs')
    ap.add_argument('--check', action='store_true', help='also check the PDF written from an SVG input')
    a = ap.parse_args(argv)
    if a.doctor:
        doctor()
        if not a.inputs:
            return 0
    if not a.inputs:
        ap.error('give at least one SVG, PNG or PDF, or use --doctor')
    status = 0
    for item in a.inputs:
        p = Path(item)
        if p.suffix.lower() == '.svg':
            for out in render_svg(p, tuple(a.formats.split(',')), a.dpi, a.out_dir, a.transparent):
                print(f'wrote {out}')
                if a.check and out.suffix == '.pdf':
                    print(f'  {check_pdf(out)}')
                if a.preview and out.suffix == '.png':
                    print(f'  preview {preview(out)}')
        elif p.suffix.lower() == '.png' and a.preview:
            print(f'preview {preview(p)}')
        elif p.suffix.lower() == '.pdf':
            rep = check_pdf(p)
            print(f'{p}: {rep}')
            if not rep['fonts_ok']:
                status = 1
        else:
            print(f'skip {p}: nothing to do (use --preview for PNG)', file=sys.stderr)
    return status


if __name__ == '__main__':
    sys.exit(main())
