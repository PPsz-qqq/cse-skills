"""07 Timing / sequence diagram: multi-rate asynchronous sensor fusion with a delayed measurement.

Pattern: one lane per sensor on a shared time axis, lane labels right-aligned on the left, capture
time (hollow) and arrival time (filled) joined by a latency bar, filter events on their own lane,
and a single annotated arc for the out-of-sequence correction.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, TONES, template_args  # noqa: E402

args = template_args(__doc__)
fig = Figure('ieee-double', 178, theme=args.theme or 'default')
T = fig.t
X0, X1, T_END = 92, 500, 0.5            # axis span in pt and seconds


def tx(t):
    return X0 + (X1 - X0) * t / T_END


LANES = {'IMU  200 Hz': 30, 'Camera  20 Hz': 58, 'GNSS  5 Hz': 86, 'Filter': 114}
TONE = {'IMU  200 Hz': 'gray', 'Camera  20 Hz': 'blue', 'GNSS  5 Hz': 'orange', 'Filter': 'teal'}
for name, y in LANES.items():
    fig.line((X0 - 4, y), (X1 + 4, y), color='#E1E4E8', width=0.7)
    fig.text(X0 - 10, y, name, T.small, 'bold', 'end', TONES[TONE[name]]['ink'])

# IMU ticks and filter predictions at the IMU rate.
imu = [k * 0.005 for k in range(int(T_END / 0.005) + 1)]
for t in imu:
    fig.line((tx(t), LANES['IMU  200 Hz'] - 3.5), (tx(t), LANES['IMU  200 Hz'] + 3.5), color='#8A9099', width=0.55)
    if round(t / 0.005) % 2 == 0:
        fig.raw(f'<circle cx="{tx(t):.2f}" cy="{LANES["Filter"]}" r="0.9" fill="#8A9099"/>')


def measurement(lane, t_cap, latency, tone):
    y, c = LANES[lane], TONES[tone]['line']
    xa, xb = tx(t_cap), tx(t_cap + latency)
    fig.raw(f'<rect x="{xa:.2f}" y="{y - 1.6}" width="{xb - xa:.2f}" height="3.2" rx="1.6" fill="{TONES[tone]["soft"]}"/>')
    fig.raw(f'<circle cx="{xa:.2f}" cy="{y}" r="2.6" fill="#FFFFFF" stroke="{c}" stroke-width="0.9"/>')
    fig.raw(f'<circle cx="{xb:.2f}" cy="{y}" r="2.6" fill="{c}"/>')
    yf = LANES['Filter']
    fig.line((xb, y + 3.5), (xb, yf - 4.5), color=TONES[tone]['mid'], width=0.6, dashed=True, dash='1.6 1.6')
    fig.raw(f'<path d="M{xb:.2f},{yf - 3.6} l3.6,3.6 -3.6,3.6 -3.6,-3.6 Z" fill="{TONES["teal"]["soft"]}" '
            f'stroke="{TONES["teal"]["line"]}" stroke-width="0.8"/>')
    return xa, xb


for k in range(10):
    measurement('Camera  20 Hz', 0.025 + k * 0.05, 0.018, 'blue')
cap, arr = measurement('GNSS  5 Hz', 0.15, 0.11, 'orange')
measurement('GNSS  5 Hz', 0.35, 0.03, 'orange')

# Out-of-sequence correction for the late GNSS fix.
yf = LANES['Filter']
fig.curve((arr - 2, yf + 7), (cap + 1, yf + 7), bend=-0.18, color=TONES['orange']['line'], width=0.8)
fig.text((cap + arr) / 2, yf + 24, 'retrodict to capture time, then re-propagate', T.small,
         color=TONES['orange']['ink'], halo=True)
fig.text((cap + arr) / 2, LANES['GNSS  5 Hz'] - 9, 'latency 110 ms', T.small, color=T.muted, halo=True)

# Time axis, titled in the lane-label column.
AY = 158
fig.line((X0, AY), (X1, AY), color='#4A515B', width=0.7)
for k in range(6):
    t = k * 0.1
    fig.line((tx(t), AY), (tx(t), AY + 3), color='#4A515B', width=0.7)
    fig.text(tx(t), AY + 9, f'{t:.1f}', T.small, color=T.muted)
fig.text(X0 - 10, AY, 'Time (s)', T.small, 'bold', 'end', T.muted)

fig.legend(fig.W / 2 + 40, 9, [('ring', 'Capture', 'blue'), ('dot', 'Arrival', 'blue'), ('bar', 'Latency', 'blue'),
                               ('diamond', 'Filter update', 'teal'), ('dot', 'Prediction', '#8A9099')],
           gap=10, align='center')

fig.export(args.out, '07_timing', args.formats, args.dpi)
