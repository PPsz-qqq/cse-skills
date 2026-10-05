"""18 Qualitative tracking strip: three frames, boxes coloured by identity, track history, one failure.

Pattern: frames at identical size and crop with a frame chip in the corner, boxes coloured by track
identity (the same colour for the same ID in every frame), label tabs "ID k · score" whose fill keeps
the text readable, the recent trajectory of each track as fading dots, the failure case shown rather
than hidden (an unmatched ground-truth box, dashed), and one legend row. To compare methods, give
each method its own row on the same frames; never a different frame per column. For detection only,
colour by class and drop the history.
DEMO DATA: the frames are drawn illustrations and the boxes are placeholders; the output is stamped.
Replace frame_image() with your images and TRACKS / MISSED with your tracker output for the same
frame indices; state sequence, frame indices, detector, public or private detection and the score
threshold in the caption.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
import demo_scene as ds  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)
pp.mark_demo('illustrated frames and placeholder tracks')    # delete with frame_image() and the tables

W, H = 480, 320                    # frame size in pixels
FRAMES = (120, 135, 150)           # frame indices shown
HISTORY = 15                       # frames of track history drawn behind each box

# ---------------------------------------------------------------- DEMO scene and tracker output
PEOPLE = {   # id: clothing, feet line, height and x position in each shown frame (None: not visible)
    1: dict(top='#3A6EA5', legs='#2E3136', hair='#2B2522', skin='#E3B590', feet=186, h=82, xs=(70, 124, 178)),
    2: dict(top='#B4493B', legs='#4B505A', hair='#5A3B2A', skin='#F1CBA8', feet=189, h=86, xs=(421, 375, 328),
            bag='#6B4E3A'),
    4: dict(top='#D49A3A', legs='#3C4350', hair='#1F1C1A', skin='#C98E67', feet=309, h=122, xs=(None, 452, 440)),
}
CAR = dict(id=3, body='#2F7E86', bottom=300, w=124, h=52, xs=(14, 146, 278))


def x_at(xs, f):
    """Position at frame f, linear between shown frames and extrapolated before the first one."""
    pts = [(fr, x) for fr, x in zip(FRAMES, xs) if x is not None]
    if len(pts) == 1:
        return pts[0][1]
    seg = pts[:2] if f <= pts[1][0] else pts[1:3] if len(pts) > 2 else pts[:2]
    (f0, x0), (f1, x1) = seg
    return x0 + (x1 - x0) * (f - f0) / (f1 - f0)


def frame_image(i):
    """DEMO: an illustrated frame. Replace with e.g. imageio.v3.imread(f'seq/img1/{FRAMES[i]:06d}.jpg')."""
    def draw(ax):
        ds.street(ax, W, H)
        ds.car(ax, CAR['xs'][i], CAR['bottom'], CAR['w'], CAR['h'], CAR['body'], z=3)
        for pid, p in PEOPLE.items():
            if p['xs'][i] is not None:
                ds.person(ax, p['xs'][i], p['feet'], p['h'], p['top'], p['legs'], p['hair'], p['skin'],
                          p.get('bag'), stride=(i + pid) % 2, flip=pid == 2, z=5 if pid == 4 else 3)
    return pp.render_array(draw, W, H, scale=2)


def person_box(p, x, d):
    return (x - 0.21 * p['h'] + d[0], p['feet'] - 1.0 * p['h'] + d[1], x + 0.21 * p['h'] + d[2], p['feet'] + 4 + d[3])


JIT = [(-2, 1, 1, 0), (1, -1, -2, 1), (0, 2, 2, -1)]       # small placeholder localisation errors
TRACKS = {i: [] for i in range(3)}                         # frame -> [(track id, box, score)]
MISSED = {i: [] for i in range(3)}                         # frame -> [ground-truth box without a match]
SCORES = {1: (0.94, 0.93, 0.95), 2: (0.91, 0.88, 0.90), 3: (0.97, 0.96, 0.97), 4: (None, None, 0.81)}
for i in range(3):
    c = CAR['xs'][i]
    TRACKS[i].append((3, (c - 3, CAR['bottom'] - CAR['h'] - 5, c + CAR['w'] + 3, CAR['bottom'] + 4), SCORES[3][i]))
    for pid, p in PEOPLE.items():
        x = p['xs'][i]
        if x is None:
            continue
        if SCORES[pid][i] is None:
            MISSED[i].append(person_box(p, x, (0, 0, 0, 0)))
        else:
            TRACKS[i].append((pid, person_box(p, x, JIT[(i + pid) % 3]), SCORES[pid][i]))


def foot(pid, f):
    if pid == CAR['id']:
        return x_at(CAR['xs'], f) + CAR['w'] / 2, CAR['bottom'] + 2
    return x_at(PEOPLE[pid]['xs'], f), PEOPLE[pid]['feet'] + 2


# ---------------------------------------------------------------- layout (inches) and drawing
FW = pp.width_in('ieee-double')
MARGIN, GAP, TOP, LEGEND = 0.02, 0.07, 0.02, 0.27
PW = (FW - 2 * MARGIN - 2 * GAP) / 3
PH = PW * H / W
fig = pp.canvas(FW, TOP + PH + LEGEND)
color = {k: pp.IDS[n] for n, k in enumerate((1, 2, 3, 4))}
first_seen = {pid: min(i for i in range(3) if any(t[0] == pid for t in TRACKS[i])) for pid in color}

for i, frame in enumerate(FRAMES):
    ax = pp.place(fig, MARGIN + i * (PW + GAP), TOP, PW, PH)
    pp.image_panel(ax, frame_image(i), size=(W, H))
    for pid, _box, _s in TRACKS[i]:                        # history first, so boxes sit on top
        start = frame - HISTORY if first_seen[pid] == 0 else max(frame - HISTORY, FRAMES[first_seen[pid]])
        if start >= frame:
            continue
        fs = np.arange(start, frame + 1, 3)
        pts = np.array([foot(pid, f) for f in fs])
        ax.plot(pts[:, 0], pts[:, 1], color=color[pid], lw=1.1, alpha=0.7, zorder=3, solid_capstyle='round')
        ax.scatter(pts[:-1, 0], pts[:-1, 1], s=11, color=color[pid], alpha=np.linspace(0.35, 0.95, len(pts) - 1),
                   edgecolors='#FFFFFF', linewidths=0.4, zorder=3)
    for gt in MISSED[i]:
        pp.box(ax, gt, '#4A515B', pp.tr('missed', '漏检'), dashed=True, lw=1.1)
    for pid, b, score in TRACKS[i]:
        pp.box(ax, b, color[pid], f'ID {pid} · {score:.2f}')
    pp.chip(ax, pp.tr(f'Frame {frame}', f'第 {frame} 帧'))

handles = [Line2D([], [], color='#3C4148', lw=1.3),
           Line2D([], [], color='#4A515B', lw=1.1, ls=(0, (3, 2))),
           Line2D([], [], color='#3C4148', lw=0.9, marker='o', ms=2.6, mew=0)]
labels = [pp.tr('Tracked box, colour = identity', '跟踪框（颜色区分身份）'),
          pp.tr('Unmatched ground truth', '未匹配的真值框'),
          pp.tr(f'Track history ({HISTORY} frames)', f'轨迹历史（{HISTORY} 帧）')]
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.0), ncols=3, frameon=False,
           handlelength=2.2, columnspacing=1.8, borderaxespad=0.15)

pp.save(fig, args.out, '18_detection_boxes', args.formats, args.dpi)
