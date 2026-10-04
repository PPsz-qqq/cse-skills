"""03 Network architecture: encoder-decoder with a transformer bottleneck and skip connections.

Pattern: cuboids whose height follows spatial resolution and whose thickness follows channels,
encoder in blue, decoder in teal, the proposed block emphasised, nested skip arcs above the
main axis, and every tensor annotated with one aligned row of shape labels.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, template_args  # noqa: E402

args = template_args(__doc__)
fig = Figure('ieee-double', 170, theme=args.theme or 'default')
T = fig.t
CY = 84                    # main axis
LABEL_Y = 132              # one baseline for all shape labels


def stage(x, w, h, depth, tone, name, shape):
    node = fig.tensor(x, CY - h / 2, w, h, depth=depth, tone=tone)
    cx = x + (w + depth) / 2
    fig.text(cx, LABEL_Y, name, T.small, 'bold', color=T.text)
    fig.text(cx, LABEL_Y + 9.5, shape, T.small, color=T.muted)
    return node, x + w + depth, x + w / 2 + depth / 2, CY - h / 2 - depth * 0.62


# Input image.
fig.image_icon(8, CY - 20, 40, 40, tone='blue', stack=1)
fig.text(28, LABEL_Y, 'Input', T.small, 'bold')
fig.text(28, LABEL_Y + 9.5, '$3\\times H\\times W$', T.small, color=T.muted)

enc_spec = [(60, 8, 72, 14, 'E1', '$H/4$, 64'), (94, 11, 56, 12, 'E2', '$H/8$, 128'),
            (129, 14, 42, 10, 'E3', '$H/16$, 256'), (165, 18, 30, 8, 'E4', '$H/32$, 512')]
enc = [stage(x, w, h, d, 'blue', n, s) for x, w, h, d, n, s in enc_spec]
fig.arrow((52, CY), (enc[0][0].x - 1, CY))
for (_, right, _, _), (node, _, _, _) in zip(enc, enc[1:]):
    fig.arrow((right + 1.5, CY), (node.x - 1, CY))

# Proposed bottleneck.
tr = fig.box(204, CY - 24, 74, 48, 'Transformer', '6 layers, global context', tone='blue', emphasis=True)
fig.arrow((enc[-1][1] + 1.5, CY), tr.left)
fig.text(tr.cx, LABEL_Y, 'Bottleneck', T.small, 'bold')
fig.text(tr.cx, LABEL_Y + 9.5, '$HW/1024$ tokens', T.small, color=T.muted)

dec_spec = [(292, 14, 42, 10, 'D3', '$H/16$, 256'), (328, 11, 56, 12, 'D2', '$H/8$, 128'),
            (363, 8, 72, 14, 'D1', '$H/4$, 64')]
dec = [stage(x, w, h, d, 'teal', n, s) for x, w, h, d, n, s in dec_spec]
fig.arrow(tr.right, (dec[0][0].x - 1, CY))
for (_, right, _, _), (node, _, _, _) in zip(dec, dec[1:]):
    fig.arrow((right + 1.5, CY), (node.x - 1, CY))

# Nested skip connections, longest outermost.
for (_, _, ex, ey), (_, _, dx, dy) in zip(enc[2::-1], dec):
    fig.curve((ex, ey - 1.5), (dx, dy - 2), bend=-0.17, dashed=True, color='#7C838D', width=0.75)

# Heads and output heatmap.
head = fig.box(399, CY - 21, 54, 42, 'Heads', 'center, size, offset', tone='gray')
fig.arrow((dec[-1][1] + 1.5, CY), head.left)
heat = [[0.05, 0.1, 0.15, 0.1, 0.05, 0.05], [0.1, 0.45, 0.8, 0.4, 0.1, 0.05], [0.1, 0.5, 1.0, 0.5, 0.15, 0.1],
        [0.05, 0.15, 0.35, 0.2, 0.55, 0.3], [0.05, 0.05, 0.1, 0.35, 0.9, 0.4], [0.02, 0.05, 0.05, 0.15, 0.3, 0.15]]
hm = fig.matrix(468, CY - 13.5, heat, cell=3.9, gap=0.8, tone='orange', stroke=False)
fig.arrow(head.right, (hm.x - 1, CY))
fig.text(hm.cx, LABEL_Y, 'Output', T.small, 'bold')
fig.text(hm.cx, LABEL_Y + 9.5, 'heatmap', T.small, color=T.muted)

fig.legend(fig.W / 2, 160, [('box', 'Encoder feature', 'blue'), ('box', 'Decoder feature', 'teal'),
                            ('emph', 'Proposed block', 'blue'), ('dashed', 'Skip connection', '#7C838D')],
           align='center')

fig.export(args.out, '03_network', args.formats, args.dpi)
