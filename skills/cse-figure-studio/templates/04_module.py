"""04 Module detail: a cross-attention fusion block drawn bottom to top, transformer style.

Pattern: inputs at the bottom, operator nodes (matrix product, residual sum) as small circles,
residual paths routed along the outside and labelled directly, the repeated block enclosed in a
container whose chip states the repetition. One column wide.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, template_args  # noqa: E402

args = template_args(__doc__)
fig = Figure('ieee-single', 290, theme=args.theme or 'default')
T = fig.t
RES = '#7C838D'                   # residual paths
CX = 94                           # main column

grp = fig.group(10, 30, 222, 222, 'Fusion block  × $N$', tone='blue', chip_at='right')

# Inputs and projections.
fv = fig.pill(30, 266, 60, 16, 'Visual $F_v$', tone='gray')
fm = fig.pill(150, 266, 64, 16, 'Motion $F_m$', tone='gray')
wq = fig.box(38, 222, 44, 20, '$W_Q$', tone='gray')
wk = fig.box(106, 222, 44, 20, '$W_K$', tone='gray')
wv = fig.box(160, 222, 44, 20, '$W_V$', tone='gray')
fig.arrow(fv.top, wq.bottom)
fig.arrow(fm.top, wk.bottom, route='vhv', mid=259)
fig.arrow(fm.top, wv.bottom)
fig.dot(fm.cx, 259)

# Attention weights (the proposed part here) and the weighted sum with V.
att = fig.box(38, 182, 112, 26, 'Attention weights', '$\\mathrm{softmax}(QK^{\\top}/\\sqrt{d})$', tone='blue',
              emphasis=True, title_size=T.body, sub_size=T.small)
fig.arrow(wq.top, att.port('bottom', (wq.cx - att.x) / att.w), label='$Q$', label_side='left', label_size=T.small)
fig.arrow(wk.top, att.port('bottom', (wk.cx - att.x) / att.w), label='$K$', label_side='left', label_size=T.small)
mul = fig.op(CX, 160, 'x')
fig.arrow(att.top, mul.bottom)
fig.arrow(wv.top, mul.right, route='vh', label='$V$', label_side='right', label_size=T.small, label_at=0)

# Residual, norm, feed-forward, residual.
add1 = fig.op(CX, 132, '+')
fig.arrow(mul.top, add1.bottom)
fig.arrow(fv.left, add1.left, route=[(20, fv.cy), (20, add1.cy)], color=RES, dashed=True)
fig.text(20, 206, 'residual', T.small, color=RES, halo=grp.fill, rotate=-90)
ln = fig.box(CX - 40, 98, 80, 18, 'LayerNorm', tone='gray', title_size=T.body)
fig.arrow(add1.top, ln.bottom)
ffn = fig.box(CX - 40, 60, 80, 26, 'FFN', '2-layer MLP', tone='teal', title_size=T.body, sub_size=T.small)
fig.arrow(ln.top, ffn.bottom)
add2 = fig.op(CX, 42, '+')
fig.arrow(ffn.top, add2.bottom)
fig.dot(CX, 92, color=RES)
fig.arrow((CX, 92), add2.right, route=[(150, 92), (150, add2.cy)], color=RES, dashed=True)

out = fig.pill(CX - 36, 6, 72, 16, 'Fused $F_{\\mathrm{fuse}}$', tone='blue')
fig.arrow(add2.top, out.bottom)

fig.export(args.out, '04_module', args.formats, args.dpi)
