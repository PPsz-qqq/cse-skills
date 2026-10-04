#!/usr/bin/env python3
"""figkit: a dependency-free SVG builder for publication diagrams.

Framework, network, flowchart, control-loop, module, topology, timeline and taxonomy figures.
All coordinates are points at final print size (72 pt = 1 inch): font size 8 prints at 8 pt and a
0.8 stroke prints at 0.8 pt, so legibility can be judged from the numbers. Build a Figure, call
save(), then render PNG/PDF previews with render.py and inspect them.

Labels accept a small math markup: $x_{k|k-1}$, $\\hat{x}$, $\\alpha$, $\\oplus$, $\\mathrm{FC}$.
Standard library only.
"""
from __future__ import annotations

import math
import re
import sys
from dataclasses import dataclass, replace
from xml.sax.saxutils import escape

sys.dont_write_bytecode = True      # never leave __pycache__ inside an installed skill bundle

PT_PER_MM = 72 / 25.4

# Final widths in points (1/72 in). Sources and check dates: references/print-and-venue-specs.md.
# Conference templates: measure \columnwidth and \textwidth in the kit and pass e.g. '241.14pt'.
WIDTHS = {
    'ieee-single': 3.5 * 72, 'ieee-double': 7.16 * 72,
    'elsevier-single': 90 * PT_PER_MM, 'elsevier-1.5': 140 * PT_PER_MM, 'elsevier-double': 190 * PT_PER_MM,
    'springer-single': 84 * PT_PER_MM, 'springer-double': 174 * PT_PER_MM,
    'aas-single': 80 * PT_PER_MM, 'aas-double': 160 * PT_PER_MM,
}
# TeX points (what \the\columnwidth prints) are 1/72.27 in; 'bp' are PostScript points (1/72 in).
_UNITS_PT = {'bp': 1.0, 'pt': 72 / 72.27, 'in': 72.0, 'mm': PT_PER_MM, 'cm': 10 * PT_PER_MM, 'pc': 12 * 72 / 72.27}


def width_pt(width):
    """Width in points (1/72 in) from a WIDTHS key, a number of points, or a string with a unit:
    '3.25in', '88mm', '8cm', '21pc', '252bp', or '241.14pt' (TeX points)."""
    if isinstance(width, (int, float)):
        return float(width)
    if width in WIDTHS:
        return WIDTHS[width]
    m = re.fullmatch(r'\s*([\d.]+)\s*(in|pt|bp|mm|cm|pc)\s*', str(width))
    if not m:
        raise ValueError(f'unknown width {width!r}: use a key of WIDTHS, points, or a value with in/pt/bp/mm/cm/pc')
    return float(m.group(1)) * _UNITS_PT[m.group(2)]

SANS = "Arial, Helvetica, 'Liberation Sans', 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', sans-serif"
SERIF = "'Times New Roman', Times, 'Liberation Serif', SimSun, 'Songti SC', serif"

# Line colours from Paul Tol's colour-blind-safe schemes (vibrant, bright, muted, high-contrast).
BASE = {
    'blue': '#0077BB', 'teal': '#009988', 'orange': '#EE7733', 'cyan': '#33BBEE',
    'magenta': '#EE3377', 'red': '#CC3311', 'green': '#228833', 'purple': '#AA3377',
    'indigo': '#332288', 'sand': '#DDAA33', 'gray': '#7C838D',
}


def _rgb(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return '#' + ''.join(f'{max(0, min(255, round(v))):02X}' for v in rgb)


def mix(a, b, t):
    """Blend colour a toward b by fraction t."""
    ra, rb = _rgb(a), _rgb(b)
    return _hex(tuple(x + (y - x) * t for x, y in zip(ra, rb)))


def tint(c, t):
    return mix(c, '#FFFFFF', t)


def shade(c, t):
    return mix(c, '#000000', t)


def make_tone(line):
    return {'line': line, 'fill': tint(line, 0.93), 'soft': tint(line, 0.82), 'mid': tint(line, 0.55),
            'ink': shade(line, 0.48)}


TONES = {k: make_tone(v) for k, v in BASE.items()}
TONES['gray'].update(fill='#F5F6F8', soft='#E4E7EB', ink='#2F343B')
TONES['white'] = {'line': '#7C838D', 'fill': '#FFFFFF', 'soft': '#F5F6F8', 'mid': '#C9CED4', 'ink': '#23272E'}


@dataclass
class Theme:
    font: str = SANS
    title: float = 8.5       # module titles
    body: float = 7.5        # subtitles, arrow labels
    small: float = 7.0       # legends, notes
    min_size: float = 6.0    # nothing may print smaller, sub/superscripts included
    sub_scale: float = 0.8
    stroke: float = 0.75
    arrow: float = 0.85
    radius: float = 3.5
    text: str = '#23272E'
    muted: str = '#5F6670'
    line: str = '#4A515B'


THEMES = {
    'default': Theme(),
    # IEEE Author Center: about 9-10 pt type at final size; scripts may shrink to 0.8 of 9 pt.
    'ieee': Theme(title=9.5, body=9.0, small=8.5, min_size=7.2),
    # Elsevier: about 7 pt lettering, sub/superscripts at least 6 pt.
    'elsevier': Theme(title=8.0, body=7.0, small=7.0, min_size=6.0),
    # Springer: 8-12 pt (2-3 mm) lettering.
    'springer': Theme(title=9.0, body=8.0, small=8.0, min_size=6.0),
    # 自动化学报 template: 8 pt, Times New Roman for Latin and 宋体 for Chinese.
    'aas': Theme(font=SERIF, title=8.0, body=8.0, small=8.0, min_size=6.4),
}

# Helvetica/Arial advance widths (1/1000 em) for ASCII 32..126; Arial is metric-compatible.
_W = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
     [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
      722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556,
      556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556,
      500, 722, 500, 500, 500, 334, 260, 334, 584]


def char_width(ch, size, bold=False):
    o = ord(ch)
    if 32 <= o <= 126:
        w = _W[o - 32] / 1000
    elif 0x2E80 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFFEF or 0x3000 <= o <= 0x303F:
        w = 1.0
    elif 0x0300 <= o <= 0x036F or 0x20D0 <= o <= 0x20FF:
        w = 0.0                      # combining accents
    else:
        w = 0.6
    return w * size * (1.07 if bold else 1.0)


GREEK = {n: c for n, c in zip(
    'alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi pi rho '
    'sigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Phi Psi Omega'.split(),
    'αβγδϵεζηθϑικλμνξπρστυϕφχψωΓΔΘΛΞΠΣΦΨΩ')}
SYMBOLS = {'times': '×', 'cdot': '·', 'oplus': '⊕', 'otimes': '⊗', 'odot': '⊙', 'in': '∈', 'to': '→',
           'rightarrow': '→', 'leftarrow': '←', 'leq': '≤', 'geq': '≥', 'neq': '≠', 'approx': '≈', 'sim': '∼',
           'pm': '±', 'infty': '∞', 'partial': '∂', 'nabla': '∇', 'sum': '∑', 'prod': '∏', 'int': '∫',
           'cdots': '⋯', 'ldots': '…', 'mid': '|', 'top': '⊤', 'ell': 'ℓ', 'circ': '∘', 'star': '⋆',
           'langle': '⟨', 'rangle': '⟩', ',': ' ', ';': ' ', 'quad': '  '}
ACCENTS = {'hat': '\u0302', 'bar': '\u0304', 'tilde': '\u0303', 'dot': '\u0307', 'ddot': '\u0308',
           'vec': '\u20D7'}


def _brace(s, i):
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return j
    return len(s) - 1


RELATIONS = set('=<>≤≥≠≈∼≡∈→←')
BINARY = set('+−×·±⊕⊗⊙∘')


def _spaced(sym, level, prev):
    """TeX-like spacing at the base level: relations always, binary operators unless unary."""
    if level != 0:
        return sym
    if sym in RELATIONS:
        return f' {sym} '
    if sym in BINARY and prev and prev not in '([{,' and prev not in RELATIONS and prev not in BINARY:
        return f' {sym} '
    return sym


def _math_runs(s, level=0):
    out, i = [], 0

    def prev():
        for t, _it, lv in reversed(out):
            if lv == level and t.strip():
                return t.strip()[-1]
        return ''

    while i < len(s):
        c = s[i]
        if c == ' ':                     # spaces are ignored in math mode, as in TeX
            i += 1
            continue
        if c in '_^':
            lvl = level + (-1 if c == '_' else 1)
            i += 1
            if i < len(s) and s[i] == '{':
                j = _brace(s, i)
                inner, i = s[i + 1:j], j + 1
            elif i < len(s) and s[i] == '\\':
                m = re.match(r'\\[A-Za-z]+', s[i:])
                inner = m.group(0) if m else s[i]
                i += len(inner)
            else:
                inner, i = s[i:i + 1], i + 1
            out += _math_runs(inner, lvl)
        elif c == '\\':
            m = re.match(r'\\([A-Za-z]+|.)', s[i:])
            name = m.group(1) if m else ''
            i += len(name) + 1
            arg = None
            if i < len(s) and s[i] == '{' and (name in ACCENTS or name in ('mathrm', 'text', 'mathcal', 'mathbf',
                                                                           'boldsymbol', 'operatorname', 'sqrt')):
                j = _brace(s, i)
                arg, i = s[i + 1:j], j + 1
            if name == 'sqrt' and arg is not None:
                out.append(('\u221A', False, level))
                out += _math_runs(arg, level)
            elif name in ACCENTS and arg is not None:
                runs = _math_runs(arg, level)
                if runs:
                    t, it, lv = runs[-1]
                    runs[-1] = (t + ACCENTS[name], it, lv)
                out += runs
            elif name in ('mathrm', 'text', 'operatorname', 'mathbf', 'boldsymbol') and arg is not None:
                out.append((arg, False, level))
            elif name == 'mathcal' and arg is not None:
                out.append((arg, True, level))
            elif name in GREEK:
                out.append((GREEK[name], name[0].islower(), level))
            elif name in SYMBOLS:
                sym = SYMBOLS[name]
                out.append((_spaced(sym, level, prev()) if len(sym) == 1 else sym, False, level))
            else:
                out.append((name, False, level))
        elif c == '{':
            j = _brace(s, i)
            out += _math_runs(s[i + 1:j], level)
            i = j + 1
        else:
            # Math mode uses a true minus sign, not the hyphen, and spaces relations and operators.
            ch = '\u2212' if c == '-' else c
            out.append((_spaced(ch, level, prev()), c.isascii() and c.isalpha(), level))
            i += 1
    return out


def parse(text):
    """Split a label into (text, italic, level) runs; level -1 is subscript and +1 superscript."""
    runs = []
    for part in re.split(r'(\$[^$]*\$)', text):
        if len(part) >= 2 and part[0] == '$' and part[-1] == '$':
            runs += _math_runs(part[1:-1])
        elif part:
            runs.append((part, False, 0))
    merged = []
    for t, it, lv in runs:
        if merged and merged[-1][1] == it and merged[-1][2] == lv:
            merged[-1] = (merged[-1][0] + t, it, lv)
        else:
            merged.append((t, it, lv))
    return merged


def _layout_runs(runs, size, bold, sub_scale, min_size):
    """Yield (text, italic, level, font_size, width, dx) with opposite scripts stacked (x_k^2)."""
    prev_script, pending, last_level = None, 0.0, 0
    for t, it, lv in runs:
        fs = max(size * (sub_scale ** abs(lv)), min_size) if lv else size
        w = sum(char_width(ch, fs, bold) for ch in t)
        dx, pending = pending, 0.0
        stacked = bool(lv and prev_script and prev_script[1] * lv < 0)
        if stacked:
            dx -= prev_script[0]
            pending = max(0.0, prev_script[0] - w)
        yield t, it, lv, fs, w, dx
        prev_script = (w, lv) if (lv and not stacked and last_level == 0) else None
        last_level = lv


def measure(text, size, bold=False, sub_scale=0.8, min_size=0.0):
    """Estimated width (pt) of the widest line of a label."""
    best = 0.0
    for line in str(text).split('\n'):
        best = max(best, sum(w + dx for _t, _i, _l, _f, w, dx in
                             _layout_runs(parse(line), size, bold, sub_scale, min_size)))
    return best


def wrap(text, max_width, size, bold=False):
    """Greedy word wrap that never breaks inside $...$."""
    out = []
    for para in str(text).split('\n'):
        tokens = re.findall(r'\$[^$]*\$\S*|\S+', para)
        line = ''
        for tok in tokens:
            cand = f'{line} {tok}'.strip()
            if line and measure(cand, size, bold) > max_width:
                out.append(line)
                line = tok
            else:
                line = cand
        out.append(line)
    return '\n'.join(out)


@dataclass
class Node:
    x: float
    y: float
    w: float
    h: float
    kind: str = 'box'
    name: str = ''
    fill: str = ''              # background colour, set for groups (useful as a label halo)

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    @property
    def center(self):
        return (self.cx, self.cy)

    def port(self, side, t=0.5, gap=0.0):
        if self.kind == 'circle':
            r = self.w / 2 + gap
            ang = {'right': 0, 'bottom': 90, 'left': 180, 'top': 270}[side] if isinstance(side, str) else side
            return (self.cx + r * math.cos(math.radians(ang)), self.cy + r * math.sin(math.radians(ang)))
        if self.kind == 'diamond' and t == 0.5:
            return {'left': (self.x - gap, self.cy), 'right': (self.x + self.w + gap, self.cy),
                    'top': (self.cx, self.y - gap), 'bottom': (self.cx, self.y + self.h + gap)}[side]
        return {'left': (self.x - gap, self.y + self.h * t), 'right': (self.x + self.w + gap, self.y + self.h * t),
                'top': (self.x + self.w * t, self.y - gap), 'bottom': (self.x + self.w * t, self.y + self.h + gap)}[side]

    @property
    def left(self):
        return self.port('left')

    @property
    def right(self):
        return self.port('right')

    @property
    def top(self):
        return self.port('top')

    @property
    def bottom(self):
        return self.port('bottom')


def _f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v)


def _attrs(**kw):
    return ' '.join(f'{k.rstrip("_").replace("_", "-")}="{_f(v) if isinstance(v, (int, float)) else escape(str(v))}"'
                    for k, v in kw.items() if v is not None)


class Figure:
    """An SVG canvas measured in points at final size."""

    def __init__(self, width, height, theme='default', background='#FFFFFF', **overrides):
        """width: a WIDTHS key, points, or a unit string such as '241.14pt' or '88mm'; height in
        points or a unit string. Overrides patch the theme, e.g. Figure(..., body=8.0)."""
        w = width_pt(width)
        height = width_pt(height)
        # Snap to the 0.75 pt (1 CSS px) grid so browsers print the page at exactly this size.
        self.W = math.floor(w / 0.75 + 1e-6) * 0.75
        self.H = math.ceil(float(height) / 0.75 - 1e-6) * 0.75
        base = THEMES[theme] if isinstance(theme, str) else theme
        self.t = replace(base, **overrides) if overrides else base
        self.background = background
        self.items = []
        self.nodes = []
        self.texts = []
        self.warnings = []

    # ---------------------------------------------------------------- text
    def _text_el(self, x, y, line, size, weight, anchor, color, italic=False, family=None, opacity=None):
        if size < self.t.min_size - 1e-6:
            self.warnings.append(f'text "{line}" at {size:.1f} pt is below the {self.t.min_size} pt minimum')
        runs = parse(line)
        parts, cur = [], 0.0
        # Sub/superscripts shrink by sub_scale but never below the theme minimum; opposite
        # scripts on one base are stacked.
        for t, it, lv, fs, _w, dx in _layout_runs(runs, size, weight == 'bold', self.t.sub_scale, self.t.min_size):
            target = 0.0 if lv == 0 else (0.24 * size * abs(lv) if lv < 0 else -0.36 * size * lv)
            dy, cur = target - cur, target
            a = []
            if abs(dx) > 1e-6:
                a.append(f'dx="{dx:.2f}"')
            if abs(dy) > 1e-6:
                a.append(f'dy="{dy:.2f}"')
            if lv:
                a.append(f'font-size="{fs:.2f}"')
            if it and not italic:
                a.append('font-style="italic"')
            parts.append(f'<tspan {" ".join(a)}>{escape(t)}</tspan>' if a else escape(t))
        return (f'<text xml:space="preserve" {_attrs(x=x, y=y, font_size=size, font_weight=weight, text_anchor=anchor, fill=color, font_style="italic" if italic else None, font_family=family, opacity=opacity)}'
                f'>{"".join(parts)}</text>')

    def text(self, x, y, text, size=None, weight=None, anchor='middle', color=None, italic=False, valign='middle',
             family=None, halo=False, opacity=None, line_height=1.22, rotate=0):
        """Place a (multi-line) label. With valign='middle', y is the visual centre of the block.
        halo=True puts a background-coloured chip behind the label so it can sit on top of lines
        (a chip, not stroked text, because stroked text becomes a Type 3 font in PDF).
        rotate=-90 turns the label about (x, y), for labels along vertical edges."""
        size = size or self.t.body
        lines = str(text).split('\n')
        lh = size * line_height
        if valign == 'middle':
            first = y - (len(lines) - 1) * lh / 2 + 0.35 * size
        elif valign == 'top':
            first = y + 0.72 * size
        else:
            first = y - (len(lines) - 1) * lh
        width = measure(text, size, weight == 'bold', self.t.sub_scale, self.t.min_size)
        x0 = x - width / 2 if anchor == 'middle' else (x - width if anchor == 'end' else x)
        top, height = first - 0.78 * size, (len(lines) - 1) * lh + 1.05 * size
        els = []
        if halo:
            chip = halo if isinstance(halo, str) else (self.background or '#FFFFFF')
            els.append(f'<rect {_attrs(x=x0 - 1.6, y=top - 0.6, width=width + 3.2, height=height + 1.2, rx=1.5, fill=chip)}/>')
        for k, line in enumerate(lines):
            els.append(self._text_el(x, first + k * lh, line, size, weight, anchor, color or self.t.text,
                                     italic, family, opacity))
        if rotate:
            self.items.append(f'<g transform="rotate({_f(float(rotate))} {_f(float(x))} {_f(float(y))})">{"".join(els)}</g>')
            if abs(abs(rotate) - 90) < 1e-6:
                cy = top + height / 2
                x0, top, width, height = x - height / 2 + (cy - y), y - width / 2, height, width
        else:
            self.items += els
        self.texts.append((x0, top, width, height, text))
        return width

    # ---------------------------------------------------------------- shapes
    def _label_block(self, node, title, sub, tone, title_size, sub_size, pad, wrap_text, align='middle'):
        inner = node.w - 2 * pad
        ts, ss = title_size or self.t.title, sub_size or self.t.body
        if wrap_text and title:
            title = wrap(title, inner, ts, True)
        if wrap_text and sub:
            sub = wrap(sub, inner, ss)
        tl = title.split('\n') if title else []
        sl = sub.split('\n') if sub else []
        gap = 1.6 if tl and sl else 0
        total = len(tl) * ts * 1.2 + len(sl) * ss * 1.2 + gap
        top = node.cy - total / 2
        x = node.cx if align == 'middle' else node.x + pad
        anchor = 'middle' if align == 'middle' else 'start'
        if tl:
            self.text(x, top + len(tl) * ts * 1.2 / 2, title, ts, 'bold', anchor, tone['ink'])
        if sl:
            self.text(x, top + len(tl) * ts * 1.2 + gap + len(sl) * ss * 1.2 / 2, sub, ss, None, anchor,
                      self.t.muted)
        for label, size, bold in ((title, ts, True), (sub, ss, False)):
            if label and measure(label, size, bold) > inner + 0.5:
                self.warnings.append(f'"{label}" ({measure(label, size, bold):.0f} pt) overflows a {node.w:.0f} pt wide {node.kind}')
        if total > node.h - 2:
            self.warnings.append(f'labels need {total:.0f} pt but the {node.kind} "{title or sub}" is {node.h:.0f} pt tall')

    def box(self, x, y, w, h, title='', sub='', tone='blue', emphasis=False, dashed=False, fill=None, radius=None,
            title_size=None, sub_size=None, pad=5, wrap_text=True, align='middle', name='', stroke=None, label_dy=0.0):
        """A rounded module card: bold title, optional muted subtitle. label_dy shifts the labels
        (negative = up) to leave room for a glyph inside the card."""
        tn = TONES[tone] if isinstance(tone, str) else tone
        r = self.t.radius if radius is None else radius
        sw = (1.3 if emphasis else self.t.stroke) if stroke is None else stroke
        self.items.append(f'<rect {_attrs(x=x, y=y, width=w, height=h, rx=r, fill=fill or (tn["soft"] if emphasis else tn["fill"]), stroke=tn["line"], stroke_width=sw, stroke_dasharray="3 2" if dashed else None)}/>')
        node = Node(x, y, w, h, 'box', name or title)
        self.nodes.append(node)
        self._label_block(Node(x, y + label_dy, w, h, 'box') if label_dy else node, title, sub, tn, title_size,
                          sub_size, pad, wrap_text, align)
        return node

    def matrix(self, x, y, values, cell=6.0, gap=1.0, tone='blue', stroke=True):
        """Small matrix glyph (cost, attention, adjacency). values: rows of numbers in [0, 1]."""
        tn = TONES[tone]
        for i, row in enumerate(values):
            for j, v in enumerate(row):
                fill = mix(tn['fill'], tn['line'], max(0.0, min(1.0, v)))
                self.items.append(f'<rect {_attrs(x=x + j * (cell + gap), y=y + i * (cell + gap), width=cell, height=cell, rx=0.8, fill=fill, stroke=tn["line"] if stroke else None, stroke_width=0.4 if stroke else None)}/>')
        rows, cols = len(values), len(values[0])
        return Node(x, y, cols * (cell + gap) - gap, rows * (cell + gap) - gap, 'glyph', 'matrix')

    def pill(self, x, y, w, h, title='', sub='', tone='gray', emphasis=False, **kw):
        """Terminator (start/end) or tag."""
        return self.box(x, y, w, h, title, sub, tone, emphasis, radius=h / 2, **kw)

    def diamond(self, cx, cy, w, h, title='', tone='sand', size=None, name=''):
        tn = TONES[tone]
        pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
        self.items.append(f'<polygon points="{" ".join(f"{_f(a)},{_f(b)}" for a, b in pts)}" {_attrs(fill=tn["fill"], stroke=tn["line"], stroke_width=self.t.stroke, stroke_linejoin="round")}/>')
        node = Node(cx - w / 2, cy - h / 2, w, h, 'diamond', name or title)
        self.nodes.append(node)
        size = size or self.t.body
        self.text(cx, cy, title, size, 'bold', 'middle', tn['ink'])
        if measure(title, size, True) > w * 0.62:
            self.warnings.append(f'decision text "{title}" is wide for a {w:.0f} pt diamond; widen it or shorten the text')
        return node

    def io(self, x, y, w, h, title='', sub='', tone='cyan', slant=7, **kw):
        """Input/output parallelogram."""
        tn = TONES[tone]
        pts = [(x + slant, y), (x + w, y), (x + w - slant, y + h), (x, y + h)]
        self.items.append(f'<polygon points="{" ".join(f"{_f(a)},{_f(b)}" for a, b in pts)}" {_attrs(fill=tn["fill"], stroke=tn["line"], stroke_width=self.t.stroke, stroke_linejoin="round")}/>')
        node = Node(x, y, w, h, 'io', title)
        self.nodes.append(node)
        self._label_block(Node(x + slant / 2, y, w - slant, h, 'io'), title, sub, tn, None, None, 4, True)
        return node

    def cylinder(self, x, y, w, h, title='', sub='', tone='gray'):
        """Database / memory bank."""
        tn = TONES[tone]
        ry = min(5.0, h * 0.14)
        self.items.append(
            f'<path d="M{_f(x)},{_f(y + ry)} a{_f(w / 2)},{_f(ry)} 0 0 1 {_f(w)},0 v{_f(h - 2 * ry)} a{_f(w / 2)},{_f(ry)} 0 0 1 {_f(-w)},0 Z" '
            f'{_attrs(fill=tn["fill"], stroke=tn["line"], stroke_width=self.t.stroke)}/>'
            f'<path d="M{_f(x)},{_f(y + ry)} a{_f(w / 2)},{_f(ry)} 0 0 0 {_f(w)},0" fill="none" {_attrs(stroke=tn["line"], stroke_width=self.t.stroke)}/>')
        node = Node(x, y, w, h, 'cylinder', title)
        self.nodes.append(node)
        self._label_block(Node(x, y + ry, w, h - ry, 'cylinder'), title, sub, tn, None, None, 4, True)
        return node

    def group(self, x, y, w, h, label='', tone='gray', dashed=True, fill=None, chip=True, chip_at='left'):
        """A stage/container. Draw groups first so they sit behind their contents.
        chip_at='right' moves the label chip to the top-right corner."""
        tn = TONES[tone]
        fill = fill or tint(tn['fill'], 0.35)
        self.items.append(f'<rect {_attrs(x=x, y=y, width=w, height=h, rx=6, fill=fill, stroke=tn["line"] if tone != "gray" else "#AEB4BC", stroke_width=0.7, stroke_dasharray="3.2 2.2" if dashed else None)}/>')
        if label:
            size = self.t.small
            tw = measure(label, size, True)
            if chip:
                cw, ch = tw + 10, size + 5
                cx0 = x + 8 if chip_at == 'left' else x + w - 8 - cw
                self.items.append(f'<rect {_attrs(x=cx0, y=y - ch / 2, width=cw, height=ch, rx=ch / 2, fill=tn["soft"] if tone != "gray" else "#E4E7EB", stroke="none")}/>')
                self.text(cx0 + cw / 2, y, label, size, 'bold', 'middle', tn['ink'])
            else:
                self.text(x + 7, y + 8, label, size, 'bold', 'start', tn['ink'])
        return Node(x, y, w, h, 'group', label, fill)

    def op(self, cx, cy, kind='+', r=5.5, tone='gray', name=''):
        """Operator node: '+' sum, 'x' product, 'c' concatenation, or any short symbol such as 'σ'."""
        tn = TONES[tone]
        el = [f'<circle {_attrs(cx=cx, cy=cy, r=r, fill="#FFFFFF", stroke=tn["line"] if tone != "gray" else "#4A515B", stroke_width=0.85)}/>']
        k = r * 0.55
        sc = tn['ink'] if tone != 'gray' else '#2F343B'
        if kind == '+':
            el.append(f'<path d="M{_f(cx - k)},{_f(cy)} H{_f(cx + k)} M{_f(cx)},{_f(cy - k)} V{_f(cy + k)}" {_attrs(stroke=sc, stroke_width=0.9, stroke_linecap="round")}/>')
        elif kind == 'x':
            d = k * 0.75
            el.append(f'<path d="M{_f(cx - d)},{_f(cy - d)} L{_f(cx + d)},{_f(cy + d)} M{_f(cx + d)},{_f(cy - d)} L{_f(cx - d)},{_f(cy + d)}" {_attrs(stroke=sc, stroke_width=0.9, stroke_linecap="round")}/>')
        self.items += el
        if kind not in ('+', 'x'):
            self.text(cx, cy, 'C' if kind == 'c' else kind, r * 1.15, 'bold', 'middle', sc)
        node = Node(cx - r, cy - r, 2 * r, 2 * r, 'circle', name or kind)
        self.nodes.append(node)
        return node

    def dot(self, x, y, r=1.6, color=None):
        """Take-off point where one signal splits."""
        self.items.append(f'<circle {_attrs(cx=x, cy=y, r=r, fill=color or self.t.line)}/>')

    def tensor(self, x, y, w, h, depth=7.0, tone='blue', label='', label_size=None, emphasis=False):
        """Feature-map cuboid; (x, y) is the top-left of the front face."""
        tn = TONES[tone]
        dx, dy = depth, -depth * 0.62
        sw = 0.9 if emphasis else 0.6
        front = f'<rect {_attrs(x=x, y=y, width=w, height=h, fill=tn["soft"] if not emphasis else tn["mid"], stroke=tn["line"], stroke_width=sw, stroke_linejoin="round")}/>'
        top = (f'<polygon points="{_f(x)},{_f(y)} {_f(x + dx)},{_f(y + dy)} {_f(x + w + dx)},{_f(y + dy)} {_f(x + w)},{_f(y)}" '
               f'{_attrs(fill=tn["fill"], stroke=tn["line"], stroke_width=sw, stroke_linejoin="round")}/>')
        side = (f'<polygon points="{_f(x + w)},{_f(y)} {_f(x + w + dx)},{_f(y + dy)} {_f(x + w + dx)},{_f(y + h + dy)} {_f(x + w)},{_f(y + h)}" '
                f'{_attrs(fill=tn["mid"] if not emphasis else tn["line"], stroke=tn["line"], stroke_width=sw, stroke_linejoin="round", fill_opacity=0.75)}/>')
        self.items += [top, side, front]
        node = Node(x, y + dy, w + dx, h - dy, 'tensor', label)
        self.nodes.append(node)
        if label:
            self.text(x + (w + dx) / 2, y + h + 3.5, label, label_size or self.t.small, None, 'middle', self.t.muted,
                      valign='top')
        return node

    def image_icon(self, x, y, w, h, tone='blue', stack=3, offset=4.0, name=''):
        """Stack of image frames with a simple scene, for 'input images/video' blocks."""
        tn = TONES[tone]
        for k in range(stack - 1, -1, -1):
            ox, oy = x + k * offset, y - k * offset
            self.items.append(f'<rect {_attrs(x=ox, y=oy, width=w, height=h, rx=1.5, fill="#FFFFFF", stroke=tn["line"], stroke_width=0.7)}/>')
        fx, fy = x, y
        sky = tint(tn['line'], 0.86)
        self.items.append(f'<rect {_attrs(x=fx + 2, y=fy + 2, width=w - 4, height=h - 4, rx=1, fill=sky)}/>')
        gx = fy + h - 2
        self.items.append(f'<polygon points="{_f(fx + 2)},{_f(gx)} {_f(fx + w * 0.38)},{_f(fy + h * 0.42)} {_f(fx + w * 0.58)},{_f(fy + h * 0.66)} {_f(fx + w * 0.72)},{_f(fy + h * 0.52)} {_f(fx + w - 2)},{_f(gx)}" {_attrs(fill=tn["mid"])}/>')
        self.items.append(f'<circle {_attrs(cx=fx + w * 0.76, cy=fy + h * 0.28, r=min(w, h) * 0.09, fill=TONES["sand"]["mid"])}/>')
        node = Node(x, y - (stack - 1) * offset, w + (stack - 1) * offset, h + (stack - 1) * offset, 'icon', name)
        self.nodes.append(node)
        return node

    def uav(self, cx, cy, s=10.0, tone='blue', ring=None):
        """Quadrotor icon of half-size s; ring draws an emphasis circle in that tone."""
        tn = TONES[tone]
        el = []
        if ring:
            el.append(f'<circle {_attrs(cx=cx, cy=cy, r=s * 1.55, fill=TONES[ring]["fill"], stroke=TONES[ring]["line"], stroke_width=0.8)}/>')
        a = s * 0.62
        el.append(f'<path d="M{_f(cx - a)},{_f(cy - a)} L{_f(cx + a)},{_f(cy + a)} M{_f(cx + a)},{_f(cy - a)} L{_f(cx - a)},{_f(cy + a)}" {_attrs(stroke=tn["ink"], stroke_width=1.0, stroke_linecap="round")}/>')
        for sx in (-1, 1):
            for sy in (-1, 1):
                el.append(f'<circle {_attrs(cx=cx + sx * a, cy=cy + sy * a, r=s * 0.36, fill=tn["soft"], stroke=tn["line"], stroke_width=0.7)}/>')
        el.append(f'<rect {_attrs(x=cx - s * 0.3, y=cy - s * 0.3, width=s * 0.6, height=s * 0.6, rx=s * 0.12, fill=tn["line"])}/>')
        self.items += el
        node = Node(cx - s, cy - s, 2 * s, 2 * s, 'circle', 'uav')
        self.nodes.append(node)
        return node

    def robot(self, cx, cy, s=10.0, tone='teal'):
        """Ground-robot icon of half-width s."""
        tn = TONES[tone]
        self.items.append(f'<rect {_attrs(x=cx - s, y=cy - s * 0.55, width=2 * s, height=s * 0.95, rx=s * 0.22, fill=tn["soft"], stroke=tn["line"], stroke_width=0.8)}/>')
        for sx in (-0.55, 0.55):
            self.items.append(f'<circle {_attrs(cx=cx + sx * s, cy=cy + s * 0.48, r=s * 0.28, fill=tn["ink"])}/>')
        self.items.append(f'<rect {_attrs(x=cx - s * 0.35, y=cy - s * 0.95, width=s * 0.7, height=s * 0.38, rx=s * 0.1, fill=tn["line"])}/>')
        node = Node(cx - s, cy - s, 2 * s, 2 * s, 'circle', 'robot')
        self.nodes.append(node)
        return node

    def beacon(self, cx, cy, s=7.0, tone='sand'):
        """Anchor / beacon triangle."""
        tn = TONES[tone]
        self.items.append(f'<polygon points="{_f(cx)},{_f(cy - s)} {_f(cx + s * 0.9)},{_f(cy + s * 0.65)} {_f(cx - s * 0.9)},{_f(cy + s * 0.65)}" {_attrs(fill=tn["soft"], stroke=tn["line"], stroke_width=0.8, stroke_linejoin="round")}/>')
        node = Node(cx - s, cy - s, 2 * s, 2 * s, 'circle', 'beacon')
        self.nodes.append(node)
        return node

    # ---------------------------------------------------------------- connectors
    def _route(self, p0, p1, route, mid):
        (x0, y0), (x1, y1) = p0, p1
        if route == 'auto':
            route = 'straight' if abs(x0 - x1) < 0.5 or abs(y0 - y1) < 0.5 else ('hvh' if abs(x1 - x0) >= abs(y1 - y0) else 'vhv')
        if route == 'straight':
            return [p0, p1]
        if route == 'hv':
            return [p0, (x1, y0), p1]
        if route == 'vh':
            return [p0, (x0, y1), p1]
        if route == 'hvh':
            m = (x0 + x1) / 2 if mid is None else mid
            return [p0, (m, y0), (m, y1), p1]
        if route == 'vhv':
            m = (y0 + y1) / 2 if mid is None else mid
            return [p0, (x0, m), (x1, m), p1]
        if isinstance(route, (list, tuple)):
            return [p0, *route, p1]
        raise ValueError(f'unknown route {route!r}')

    @staticmethod
    def _rounded(pts, r):
        d = [f'M{_f(pts[0][0])},{_f(pts[0][1])}']
        for i in range(1, len(pts) - 1):
            (ax, ay), (bx, by), (cx, cy) = pts[i - 1], pts[i], pts[i + 1]
            l1, l2 = math.hypot(bx - ax, by - ay), math.hypot(cx - bx, cy - by)
            rr = min(r, l1 / 2, l2 / 2)
            if rr < 0.3 or l1 == 0 or l2 == 0:
                d.append(f'L{_f(bx)},{_f(by)}')
                continue
            p = (bx - (bx - ax) / l1 * rr, by - (by - ay) / l1 * rr)
            q = (bx + (cx - bx) / l2 * rr, by + (cy - by) / l2 * rr)
            d.append(f'L{_f(p[0])},{_f(p[1])} Q{_f(bx)},{_f(by)} {_f(q[0])},{_f(q[1])}')
        d.append(f'L{_f(pts[-1][0])},{_f(pts[-1][1])}')
        return ' '.join(d)

    def _head(self, tip, prev, color, width):
        dx, dy = tip[0] - prev[0], tip[1] - prev[1]
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        L = 3.6 + 1.9 * width
        W = L * 0.42
        bx, by = tip[0] - ux * L, tip[1] - uy * L
        nx, ny = -uy, ux
        notch = (tip[0] - ux * L * 0.72, tip[1] - uy * L * 0.72)
        pts = [tip, (bx + nx * W, by + ny * W), notch, (bx - nx * W, by - ny * W)]
        self.items.append(f'<polygon points="{" ".join(f"{_f(a)},{_f(b)}" for a, b in pts)}" fill="{color}" stroke="none"/>')
        return (tip[0] - ux * L * 0.6, tip[1] - uy * L * 0.6)

    def arrow(self, p0, p1, route='auto', label='', label_at=None, label_side=None, dashed=False, color=None,
              width=None, head=True, tail=False, radius=5.0, mid=None, label_size=None, label_color=None,
              dash='3.2 2.4', label_halo=False):
        """Connector from p0 to p1 (points or Node ports). route: 'auto' | 'straight' | 'hv' | 'vh' | 'hvh' |
        'vhv' | list of intermediate points. label_at selects the segment index (default: longest)."""
        if isinstance(p0, Node):
            p0 = p0.right
        if isinstance(p1, Node):
            p1 = p1.left
        color = color or self.t.line
        width = width or self.t.arrow
        pts = [tuple(map(float, p)) for p in self._route(tuple(p0), tuple(p1), route, mid)]
        draw = list(pts)
        if head:
            draw[-1] = self._head(pts[-1], pts[-2], color, width)
        if tail:
            draw[0] = self._head(pts[0], pts[1], color, width)
        self.items.insert(len(self.items) - (1 if head else 0) - (1 if tail else 0),
                          f'<path d="{self._rounded(draw, radius)}" {_attrs(fill="none", stroke=color, stroke_width=width, stroke_dasharray=dash if dashed else None, stroke_linejoin="round", stroke_linecap="round" if not dashed else "butt")}/>')
        if label:
            segs = list(zip(pts[:-1], pts[1:]))
            k = label_at if label_at is not None else max(range(len(segs)), key=lambda i: math.dist(*segs[i]))
            (ax, ay), (bx, by) = segs[k]
            mx, my = (ax + bx) / 2, (ay + by) / 2
            size = label_size or self.t.body
            horizontal = abs(by - ay) < abs(bx - ax)
            side = label_side or ('above' if horizontal else 'right')
            if side == 'above':
                self.text(mx, my - 2.6 - 0.5 * size, label, size, None, 'middle', label_color or self.t.text, halo=label_halo)
            elif side == 'below':
                self.text(mx, my + 2.6 + 0.5 * size, label, size, None, 'middle', label_color or self.t.text, halo=label_halo)
            elif side == 'left':
                self.text(mx - 3.2, my, label, size, None, 'end', label_color or self.t.text, halo=label_halo)
            else:
                self.text(mx + 3.2, my, label, size, None, 'start', label_color or self.t.text, halo=label_halo)
        return pts

    def line(self, p0, p1, color=None, width=0.7, dashed=False, dash='3 2', route='straight', radius=4.0, mid=None,
             opacity=None):
        pts = self._route(tuple(p0), tuple(p1), route, mid)
        self.items.append(f'<path d="{self._rounded(pts, radius)}" {_attrs(fill="none", stroke=color or self.t.line, stroke_width=width, stroke_dasharray=dash if dashed else None, stroke_linecap="round", opacity=opacity)}/>')

    def curve(self, p0, p1, bend=0.25, color=None, width=None, dashed=False, head=True, label='', label_size=None):
        """Quadratic arc for skip connections and links that should not compete with the main flow."""
        color = color or self.t.line
        width = width or self.t.arrow
        (x0, y0), (x1, y1) = p0, p1
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = x1 - x0, y1 - y0
        cx, cy = mx - dy * bend, my + dx * bend
        end = (x1, y1)
        if head:
            end = self._head((x1, y1), (cx, cy), color, width)
        self.items.insert(len(self.items) - (1 if head else 0),
                          f'<path d="M{_f(x0)},{_f(y0)} Q{_f(cx)},{_f(cy)} {_f(end[0])},{_f(end[1])}" {_attrs(fill="none", stroke=color, stroke_width=width, stroke_dasharray="3 2.2" if dashed else None, stroke_linecap="round")}/>')
        if label:
            lx, ly = 0.25 * x0 + 0.5 * cx + 0.25 * x1, 0.25 * y0 + 0.5 * cy + 0.25 * y1
            self.text(lx, ly, label, label_size or self.t.small, None, 'middle', self.t.text, halo=True)

    # ---------------------------------------------------------------- annotation
    def legend(self, x, y, items, size=None, gap=12.0, swatch=11.0, align='left'):
        """Horizontal legend. items: ('arrow'|'dashed'|'line'|'box'|'emph'|'dot', label, tone_or_colour).
        align='center' centres the whole legend on x."""
        size = size or self.t.small
        glyph = {'arrow': 20, 'dashed': 20, 'line': 18, 'dline': 18, 'box': swatch + 4, 'emph': swatch + 4, 'dot': 9,
                 'ring': 9, 'diamond': 11, 'bar': 18, 'tri': 10}
        if align == 'center':
            total = sum(glyph[it[0]] + measure(it[1], size) + gap for it in items) - gap
            x = x - total / 2
        cx = x
        for item in items:
            kind, label = item[0], item[1]
            spec = item[2] if len(item) > 2 else None
            col = TONES[spec]['line'] if spec in TONES else (spec or self.t.line)
            if kind in ('arrow', 'dashed'):
                self.arrow((cx, y), (cx + 16, y), route='straight', dashed=kind == 'dashed', color=col)
                cx += 20
            elif kind in ('line', 'dline'):
                self.line((cx, y), (cx + 14, y), color=col, width=1.0, dashed=kind == 'dline', dash='2.4 1.8')
                cx += 18
            elif kind == 'ring':
                self.items.append(f'<circle {_attrs(cx=cx + 3, cy=y, r=2.6, fill="#FFFFFF", stroke=col, stroke_width=0.9)}/>')
                cx += 9
            elif kind == 'diamond':
                self.items.append(f'<path d="M{_f(cx + 4)},{_f(y - 3.6)} l3.6,3.6 -3.6,3.6 -3.6,-3.6 Z" {_attrs(fill=TONES[spec]["soft"] if spec in TONES else "#FFFFFF", stroke=col, stroke_width=0.8)}/>')
                cx += 11
            elif kind == 'tri':
                tn = TONES[spec] if spec in TONES else TONES['sand']
                self.items.append(f'<polygon points="{_f(cx + 4)},{_f(y - 3.6)} {_f(cx + 7.6)},{_f(y + 2.6)} {_f(cx + 0.4)},{_f(y + 2.6)}" {_attrs(fill=tn["soft"], stroke=tn["line"], stroke_width=0.8, stroke_linejoin="round")}/>')
                cx += 10
            elif kind == 'bar':
                soft = TONES[spec]['soft'] if spec in TONES else col
                self.items.append(f'<rect {_attrs(x=cx, y=y - 1.6, width=14, height=3.2, rx=1.6, fill=soft)}/>')
                cx += 18
            elif kind in ('box', 'emph'):
                tn = TONES[spec or 'blue']
                self.items.append(f'<rect {_attrs(x=cx, y=y - swatch * 0.36, width=swatch, height=swatch * 0.72, rx=1.6, fill=tn["soft"] if kind == "emph" else tn["fill"], stroke=tn["line"], stroke_width=1.2 if kind == "emph" else self.t.stroke)}/>')
                cx += swatch + 4
            elif kind == 'dot':
                self.items.append(f'<circle {_attrs(cx=cx + 3, cy=y, r=2.4, fill=col)}/>')
                cx += 9
            w = self.text(cx, y, label, size, None, 'start', self.t.text)
            cx += w + gap
        return cx

    def panel(self, x, y, label, size=None):
        """Panel label such as '(a)'."""
        return self.text(x, y, label, size or self.t.title, 'bold', 'start', self.t.text, valign='top')

    def brace(self, x0, x1, y, label='', depth=4.0, color=None, size=None, below=True):
        """Horizontal curly-ish bracket with a centred label."""
        color = color or self.t.muted
        s = 1 if below else -1
        m = (x0 + x1) / 2
        d = (f'M{_f(x0)},{_f(y)} q0,{_f(s * depth)} {_f(depth)},{_f(s * depth)} H{_f(m - depth)} '
             f'q{_f(depth)},0 {_f(depth)},{_f(s * depth)} q0,{_f(-s * depth)} {_f(depth)},{_f(-s * depth)} '
             f'H{_f(x1 - depth)} q{_f(depth)},0 {_f(depth)},{_f(-s * depth)}')
        self.items.append(f'<path d="{d}" {_attrs(fill="none", stroke=color, stroke_width=0.7, stroke_linejoin="round")}/>')
        if label:
            self.text(m, y + s * (2 * depth + 0.5 * (size or self.t.small) + 1), label, size or self.t.small, None,
                      'middle', color)

    def raw(self, svg):
        """Insert raw SVG markup (escape hatch)."""
        self.items.append(svg)

    # ---------------------------------------------------------------- output
    def lint(self):
        """Approximate layout checks: overflow, overlaps, out-of-canvas content, tiny text."""
        warns = list(dict.fromkeys(self.warnings))
        solid = [n for n in self.nodes if n.kind not in ('group',)]
        for i, a in enumerate(solid):
            if a.x < -0.5 or a.y < -0.5 or a.x + a.w > self.W + 0.5 or a.y + a.h > self.H + 0.5:
                warns.append(f'{a.kind} "{a.name}" extends beyond the {self.W:.0f}x{self.H:.0f} pt canvas')
            for b in solid[i + 1:]:
                ox = min(a.x + a.w, b.x + b.w) - max(a.x, b.x)
                oy = min(a.y + a.h, b.y + b.h) - max(a.y, b.y)
                if ox > 1.0 and oy > 1.0:
                    warns.append(f'{a.kind} "{a.name}" overlaps {b.kind} "{b.name}" by {ox:.0f}x{oy:.0f} pt')
        for x0, y0, w, h, t in self.texts:
            if x0 < -0.5 or y0 < -0.5 or x0 + w > self.W + 0.5 or y0 + h > self.H + 0.5:
                warns.append(f'text "{t}" extends beyond the canvas')
        # Text boxes are estimates from Arial metrics, so only clear collisions are reported.
        boxes = [b for b in self.texts if str(b[4]).strip()]
        for i, (ax0, ay0, aw, ah, at) in enumerate(boxes):
            for bx0, by0, bw, bh, bt in boxes[i + 1:]:
                ox = min(ax0 + aw, bx0 + bw) - max(ax0, bx0)
                oy = min(ay0 + ah, by0 + bh) - max(ay0, by0)
                if ox > 1.0 and oy > 1.0:
                    warns.append(f'text "{at}" overlaps text "{bt}" by {ox:.0f}x{oy:.0f} pt')
        return list(dict.fromkeys(warns))

    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{_f(self.W)}pt" height="{_f(self.H)}pt" '
                f'viewBox="0 0 {_f(self.W)} {_f(self.H)}" font-family="{escape(self.t.font)}" '
                f'text-rendering="geometricPrecision" shape-rendering="geometricPrecision">')
        bg = f'<rect width="100%" height="100%" fill="{self.background}"/>' if self.background else ''
        return '\n'.join([head, bg, *self.items, '</svg>']) + '\n'

    def save(self, path, quiet=False):
        """Write the SVG and print lint warnings; returns the warning list."""
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(self.svg())
        warns = self.lint()
        if warns and not quiet:
            for w in warns:
                print(f'[figkit] {path}: {w}', file=sys.stderr)
        return warns

    def export(self, out_dir, name, formats=('svg', 'pdf', 'png'), dpi=300):
        """Save <name>.svg in out_dir and render the other formats with render.py: pdf, png,
        eps (vector, needs Ghostscript/pdftops/Inkscape) and eps-gray (<name>-gray.eps, raster)."""
        import os
        unknown = [f for f in formats if f not in ('svg', 'pdf', 'png', 'eps', 'eps-gray')]
        if unknown:
            raise ValueError(f'unknown format(s) {unknown}')
        os.makedirs(out_dir, exist_ok=True)
        svg_path = os.path.join(out_dir, f'{name}.svg')
        warns = self.save(svg_path)
        rest = tuple(f for f in formats if f in ('pdf', 'png', 'eps', 'eps-gray'))
        written = [svg_path]
        if rest:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import render
            written += [str(p) for p in render.render_svg(svg_path, rest, dpi)]
        if 'svg' not in formats:
            os.remove(svg_path)
            written.remove(svg_path)
        for p in written:
            print(f'wrote {p}')
        return warns


def template_args(description=''):
    """Shared command line for the templates: --out, --formats, --dpi, --theme."""
    import argparse
    ap = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='figures', help='output directory (default: ./figures)')
    ap.add_argument('--formats', default='svg,pdf,png', help='comma list of svg,pdf,png')
    ap.add_argument('--dpi', type=int, default=300, help='PNG resolution')
    ap.add_argument('--theme', default=None, help=' | '.join(THEMES))
    args = ap.parse_args()
    args.formats = tuple(f.strip() for f in args.formats.split(',') if f.strip())
    return args


__all__ = ['Figure', 'Node', 'Theme', 'THEMES', 'TONES', 'BASE', 'WIDTHS', 'PT_PER_MM', 'width_pt', 'measure',
           'wrap', 'parse', 'mix', 'tint', 'shade', 'make_tone', 'template_args']
