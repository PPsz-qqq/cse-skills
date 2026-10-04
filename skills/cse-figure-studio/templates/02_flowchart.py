"""02 Algorithm flowchart: standard symbols, one main column, a side branch and a loop-back edge.

Symbols follow the usual flowchart conventions: rounded terminators, rectangles for processes,
parallelograms for input/output, diamonds for decisions with labelled exits. Flow runs top to
bottom; the loop returns on the left and the side branch rejoins from the right.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, template_args  # noqa: E402

args = template_args(__doc__)
fig = Figure('ieee-single', 346, theme=args.theme or 'default')
T = fig.t
DARK = {'line': '#3D434B', 'fill': '#3D434B', 'soft': '#3D434B', 'mid': '#3D434B', 'ink': '#FFFFFF'}

CX, BW = 108, 136                     # main column centre and box width
X0 = CX - BW / 2

start = fig.pill(CX - 30, 6, 60, 16, 'Start', tone=DARK)
init = fig.io(X0 + 8, 34, BW - 16, 24, 'Initialize', '$\\hat{x}_0$, $P_0$, $Q$, $R$', tone='teal')
pred = fig.box(X0, 70, BW, 28, 'Predict', '$\\hat{x}_{k|k-1}$,  $P_{k|k-1}$', tone='gray')
meas = fig.io(X0 + 8, 110, BW - 16, 22, 'Read measurement $z_k$', tone='teal')
innov = fig.box(X0, 144, BW, 28, 'Innovation test', '$\\epsilon_k=\\nu_k^{\\top}S_k^{-1}\\nu_k$', tone='gray')
gate = fig.diamond(CX, 200, 116, 40, '$\\epsilon_k\\leq\\chi^2_{m}(0.95)$?', tone='sand')
upd = fig.box(X0, 234, BW, 28, 'Update', '$K_k$,  $\\hat{x}_{k|k}$,  $P_{k|k}$', tone='gray')
more = fig.diamond(CX, 292, 92, 34, '$k<K$?', tone='sand')
end = fig.pill(CX - 30, 323, 60, 16, 'End', tone=DARK)
infl = fig.box(190, 183, 56, 34, 'Inflate $R_k$', 'robust gain', tone='blue', emphasis=True)

for a, b in ((start, init), (init, pred), (pred, meas), (meas, innov), (innov, gate), (upd, more), (more, end)):
    fig.arrow(a.bottom, b.top)
fig.arrow(gate.bottom, upd.top, label='Yes', label_side='right', label_size=T.small)
fig.arrow(gate.right, infl.left, label='No', label_size=T.small)
fig.arrow(infl.bottom, upd.right, route='vh')
fig.arrow(more.bottom, end.top, label='No', label_side='right', label_size=T.small)

# Loop back on the left, label written along the edge.
fig.arrow(more.left, pred.left, route=[(18, more.cy), (18, pred.cy)])
fig.text(18, (more.cy + pred.cy) / 2, 'Yes:  $k\\leftarrow k+1$', T.small, halo=True, rotate=-90)

fig.export(args.out, '02_flowchart', args.formats, args.dpi)
