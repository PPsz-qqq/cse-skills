"""08 Taxonomy tree for a related-work or survey section.

Pattern: root on the left, one hue per first-level family, leaves as light cards with a coloured
accent bar, a bold name and a muted detail on one line, plain elbow connectors without arrow
heads. Replace "[refs]" with real citations; never leave invented references in a figure.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, TONES, measure, template_args  # noqa: E402

args = template_args(__doc__)
EDGE = '#9AA1AA'

tree = [   # keep details short: a leaf holds name, detail and citations on one line at every theme
    ('Tracking-by-detection', 'detector + association', 'blue', [
        ('Motion-based', 'IoU and Kalman gating'),
        ('Appearance-based', 're-ID embeddings'),
        ('Learned association', 'graph or transformer')]),
    ('Joint detection and tracking', 'one shared network', 'teal', [
        ('Embedding heads', 'joint detection + re-ID'),
        ('Motion heads', 'displacement regression')]),
    ('Query-based tracking', 'end-to-end queries', 'orange', [
        ('Track queries', 'set prediction over frames'),
        ('Temporal memory', 'attention to past frames')]),
]

LEAF_H, LEAF_GAP, FAMILY_GAP = 18, 5, 14
LX = 256
LW = 515 - LX - 8                 # ieee-double canvas width minus a right margin
leaves_y, y = [], 8
for _, _, _, leaves in tree:
    ys = []
    for _ in leaves:
        ys.append(y)
        y += LEAF_H + LEAF_GAP
    leaves_y.append(ys)
    y += FAMILY_GAP - LEAF_GAP
bottom = leaves_y[-1][-1] + LEAF_H

# The canvas height follows the content; the root sits at the vertical centre of the leaves.
fig = Figure('ieee-double', bottom + 8, theme=args.theme or 'default')
T = fig.t
mid = (leaves_y[0][0] + bottom) / 2
root = fig.box(8, mid - 24, 92, 48, 'Multi-object tracking', 'paradigms', tone='gray', emphasis=True)
for (name, detail, tone, leaves), ys in zip(tree, leaves_y):
    cy = (ys[0] + ys[-1] + LEAF_H) / 2
    fam = fig.box(126, cy - 19, 112, 38, name, detail, tone=tone, title_size=T.body, sub_size=T.small)
    fig.line(root.right, fam.left, color=EDGE, width=0.8, route='hvh', mid=114)
    for (leaf, info), ly in zip(leaves, ys):
        tn = TONES[tone]
        fig.raw(f'<rect x="{LX}" y="{ly}" width="{LW}" height="{LEAF_H}" rx="3" fill="#FFFFFF" stroke="#D6DAE0" '
                f'stroke-width="0.7"/>')
        fig.raw(f'<rect x="{LX}" y="{ly}" width="3.2" height="{LEAF_H}" rx="1.4" fill="{tn["line"]}"/>')
        fig.text(LX + 9, ly + LEAF_H / 2, leaf, T.body, 'bold', 'start', tn['ink'])
        w = measure(leaf, T.body, True)
        fig.text(LX + 9 + w + 7, ly + LEAF_H / 2, info, T.small, None, 'start', T.muted)
        fig.text(LX + LW - 7, ly + LEAF_H / 2, '[refs]', T.small, None, 'end', '#9AA1AA')
        fig.line(fam.right, (LX, ly + LEAF_H / 2), color=EDGE, width=0.8, route='hvh', mid=(fam.x + fam.w + LX) / 2)

fig.export(args.out, '08_taxonomy', args.formats, args.dpi)
