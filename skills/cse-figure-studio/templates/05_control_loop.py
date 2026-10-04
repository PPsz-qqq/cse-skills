"""05 Control block diagram: observer-based state feedback with a Kalman filter.

Conventions: signals flow left to right on the forward path and right to left on the feedback
path below it; summing junctions are circles with the sign written beside each input; take-off
points are filled dots; every signal carries an italic symbol. Width is Elsevier 1.5 column.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, template_args  # noqa: E402

args = template_args(__doc__)
fig = Figure('elsevier-1.5', 150, theme=args.theme or 'default')
T = fig.t
TOP, BOT = 52, 118                  # forward and feedback rows
S = T.small                         # sign size


def sign(x, y, s):
    fig.text(x, y, s, S + 0.5, 'bold', color=T.text)


# Forward path: r -> sum -> u -> sum (disturbance) -> plant -> y.
fig.text(10, TOP, '$r$', T.body)
s1 = fig.op(52, TOP, '+', r=5.5)
fig.arrow((16, TOP), s1.left)
sign(43, TOP - 7, '+')

s2 = fig.op(150, TOP, '+', r=5.5)
fig.arrow(s1.right, s2.left, label='$u$')
sign(141, TOP - 7, '+')
fig.text(150, 12, '$d$', T.body)
fig.arrow((150, 18), s2.top)
sign(157, TOP - 12, '+')

plant = fig.box(176, TOP - 20, 96, 40, 'Plant', '$\\dot{x}=Ax+Bu+w$', tone='gray')
fig.arrow(s2.right, plant.left)
fig.dot(306, TOP)
fig.arrow(plant.right, (fig.W - 10, TOP), label='$y$', label_at=0)

# Measurement noise and feedback through the estimator.
s3 = fig.op(306, BOT, '+', r=5.5)
fig.arrow((306, TOP), s3.top)
sign(s3.cx - 8.5, s3.cy - 9.5, '+')
fig.text(fig.W - 12, BOT, '$n$', T.body)
fig.arrow((fig.W - 18, BOT), s3.right)
sign(s3.cx + 9.5, s3.cy + 9, '+')

kf = fig.box(176, BOT - 22, 96, 44, 'Kalman filter', 'state estimator', tone='blue', emphasis=True)
fig.arrow(s3.left, kf.right, label='$z$')

# The control input also drives the estimator's prediction.
fig.dot(104, TOP)
fig.arrow((104, TOP), kf.port('left', 0.27), route='vh')

gain = fig.box(30, kf.y + kf.h * 0.73 - 13, 44, 26, '$-K$', tone='gray', title_size=9)
fig.arrow(kf.port('left', 0.73), gain.right, route='straight', label='$\\hat{x}$')
fig.arrow(gain.top, s1.bottom)
sign(s1.cx + 9, s1.cy + 9.5, '+')

fig.export(args.out, '05_control_loop', args.formats, args.dpi)
