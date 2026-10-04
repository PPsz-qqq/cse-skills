"""06 System / topology figure: (a) a cooperative-navigation scene, (b) the per-agent pipeline.

Pattern: a light scene panel with a hatched GNSS-denied region, agent icons, anchors and two
link styles explained in a legend; a second panel with the processing chain of one agent, the
proposed fusion step emphasised, neighbour messages entering from below.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, TONES, template_args  # noqa: E402

args = template_args(__doc__)
fig = Figure('ieee-double', 196, theme=args.theme or 'default')
T = fig.t
COMM, RANGE = '#8A9099', TONES['teal']['line']

# ---------------------------------------------------------------- (a) scene
fig.panel(6, 4, '(a)')
PX, PY, PW, PH = 10, 20, 236, 150
fig.raw('<defs><pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="5" stroke="#D6DAE0" stroke-width="1.4"/>'
        '</pattern></defs>')
fig.raw(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="6" fill="#FAFBFC" stroke="#D3D7DD" '
        f'stroke-width="0.7"/>')
fig.raw(f'<path d="M{PX + 120},{PY} H{PX + PW - 6} a6,6 0 0 1 6,6 V{PY + PH - 6} a6,6 0 0 1 -6,6 H{PX + 150} '
        f'C{PX + 128},{PY + 110} {PX + 104},{PY + 60} {PX + 120},{PY} Z" fill="url(#hatch)" stroke="none"/>')
fig.text(PX + PW - 8, PY + 10, 'GNSS-denied area', T.small, 'bold', 'end', T.muted, halo=True)

uavs = {1: (52, 58), 2: (110, 46), 3: (176, 66), 4: (206, 118)}
robots = {5: (72, 134), 6: (150, 142)}
anchors = [(28, 34), (28, 158)]
comm = [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 4), (2, 6)]
ranging = [(1, 2), (3, 4), (6, 4), (5, 6)]
pos = {**uavs, **robots}
for a, b in comm:
    fig.line(pos[a], pos[b], color=COMM, width=0.75)
for a, b in ranging:
    (x0, y0), (x1, y1) = pos[a], pos[b]
    dx, dy = x1 - x0, y1 - y0
    n = (dx * dx + dy * dy) ** 0.5
    ox, oy = -dy / n * 3.2, dx / n * 3.2
    fig.line((x0 + ox, y0 + oy), (x1 + ox, y1 + oy), color=RANGE, width=0.9, dashed=True, dash='2.4 1.8')
for ax, ay in anchors:
    fig.line((ax, ay), pos[1] if ay < 100 else pos[5], color='#C2A04A', width=0.75, dashed=True, dash='1.2 1.8')
for k, (x, y) in uavs.items():
    fig.uav(x, y, 8, tone='blue', ring='blue' if k == 3 else None)
    fig.text(x + 12, y - 9, str(k), T.small, 'bold', 'start', TONES['blue']['ink'])
for k, (x, y) in robots.items():
    fig.robot(x, y, 8, tone='teal')
    fig.text(x + 11, y - 9, str(k), T.small, 'bold', 'start', TONES['teal']['ink'])
for ax, ay in anchors:
    fig.beacon(ax, ay, 6.5, tone='sand')
fig.text(176, 66 + 21, 'agent $i$', T.small, color=TONES['blue']['ink'], halo=True)

fig.legend(PX + 2, PY + PH + 14, [('line', 'Communication', COMM), ('dline', 'Ranging', RANGE),
                                  ('tri', 'Anchor', 'sand')], gap=10)

# ---------------------------------------------------------------- (b) agent pipeline
fig.panel(262, 4, '(b)')
fig.group(266, 26, 226, 106, 'Agent $i$', tone='blue')
R1, R2 = 62, 108
imu = fig.io(274, R1 - 15, 60, 30, 'IMU', 'odometry', tone='teal')
local = fig.box(344, R1 - 16, 56, 32, 'Local EKF', 'propagation', tone='gray')
fuse = fig.box(412, 44, 70, 80, 'CI fusion', 'covariance intersection', tone='blue', emphasis=True)
rng = fig.io(274, R2 - 15, 60, 30, 'UWB', 'range $r_{ij}$', tone='teal')
fig.arrow(imu.right, local.left)
fig.arrow(local.right, fuse.port('left', (R1 - fuse.y) / fuse.h))
fig.arrow(rng.right, fuse.port('left', (R2 - fuse.y) / fuse.h))

# Neighbour messages in (solid), own estimate broadcast out (dashed), labelled on the outer sides.
nb = fig.box(412, 160, 70, 28, 'Neighbours', '$j\\in\\mathcal{N}_i$', tone='gray', dashed=True, title_size=8,
             sub_size=7)
xin, xout = fuse.x + 18, fuse.x + fuse.w - 18
ymid = (nb.y + fuse.y + fuse.h) / 2
fig.arrow((xin, nb.y), (xin, fuse.y + fuse.h))
fig.arrow((xout, fuse.y + fuse.h), (xout, nb.y), dashed=True, color=COMM)
fig.text(xin - 4, ymid, 'receive\n$\\hat{x}_j,\\,P_j$', T.small, anchor='end', color=T.muted)
fig.text(xout + 4, ymid, 'broadcast\n$\\hat{x}_i,\\,P_i$', T.small, anchor='start', color=T.muted)
fig.export(args.out, '06_cooperative_system', args.formats, args.dpi)
