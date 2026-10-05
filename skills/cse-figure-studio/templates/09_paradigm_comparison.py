"""09 Paradigm comparison (teaser / Fig. 1): the conventional pipeline above, the proposed one below.

Pattern: two rows with identical geometry so the eye sees only the difference; shared parts in
grey, the changed part in the accent colour, one feedback arc that carries the idea, and short
row titles instead of a legend.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, TONES, template_args  # noqa: E402

args = template_args(__doc__)
fig = Figure('ieee-single', 160, theme=args.theme or 'default')
T = fig.t
ACC = TONES['blue']


def row(y0, title, assoc_title, assoc_sub, ours):
    fig.text(8, y0, title, T.small, 'bold', 'start', ACC['ink'] if ours else T.text)
    cy = y0 + 32
    fig.image_icon(8, cy - 11, 28, 22, tone='gray' if not ours else 'blue', stack=2, offset=3)
    det = fig.box(50, cy - 15, 54, 30, 'Detector', tone='gray')
    asc = fig.box(120, cy - 15, 70, 30, assoc_title, assoc_sub, tone='blue' if ours else 'gray', emphasis=ours,
                  title_size=T.title, sub_size=T.small)
    out = fig.pill(204, cy - 9, 42, 18, 'Tracks', tone='gray')
    fig.arrow((41, cy), det.left)
    fig.arrow(det.right, asc.left)
    fig.arrow(asc.right, out.left)
    return det, asc


row(10, '(a) Two-stage pipeline', 'Association', 'fixed noise $R$', False)
fig.line((8, 72), (fig.W - 8, 72), color='#D6DAE0', width=0.7, dashed=True, dash='3 2.5')
det, asc = row(84, '(b) Ours: uncertainty feedback', 'Association', 'adaptive $R_t$', True)

# The idea in one arc: association uncertainty returns to the detector, drawn below the row.
fig.curve((asc.cx, asc.y + asc.h + 1), (det.cx, det.y + det.h + 1), bend=-0.32, color=ACC['line'], width=1.0)
fig.text((asc.cx + det.cx) / 2, asc.y + asc.h + 19, 'uncertainty $\\Sigma_t$ fed back', T.small,
         color=ACC['ink'], halo=True)

fig.export(args.out, '09_paradigm_comparison', args.formats, args.dpi)
