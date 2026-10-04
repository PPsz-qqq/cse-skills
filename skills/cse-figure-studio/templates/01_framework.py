"""01 Framework (method overview) figure: staged pipeline with a highlighted proposed stage.

Pattern: stage containers left to right, standard components in grey, proposed modules in blue,
data cues in teal, recurrent state as a dashed loop, legend at the bottom. Replace the labels with
your own modules; keep one accent colour for what is new.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from figkit import Figure, TONES, template_args  # noqa: E402

args = template_args(__doc__)
fig = Figure('ieee-double', 180, theme=args.theme or 'default')
T = fig.t

GY, GH = 32, 118            # stage containers
ROW1, ROW2 = 66, 118        # centre lines of the two rows

# Stage containers first so they sit behind their contents.
fig.group(62, GY, 104, GH, 'Stage 1 · Detection')
fig.group(186, GY, 188, GH, 'Stage 2 · Association (ours)', tone='blue')
fig.group(386, GY, 84, GH, 'Stage 3 · Tracks')

# Input frames.
fig.image_icon(6, ROW1 - 15, 34, 30, tone='blue', stack=3, offset=4)
fig.text(23, ROW1 + 25, 'Frames $I_t$', T.small, color=T.muted)

# Stage 1.
backbone = fig.box(71, ROW1 - 17, 86, 34, 'Backbone', 'multi-scale features', tone='gray')
head = fig.box(71, ROW2 - 17, 86, 34, 'Detection head', 'boxes + scores', tone='gray')
fig.arrow((50, ROW1), backbone.left)
fig.arrow(backbone.bottom, head.top)

# Stage 2: two cues feed the proposed matching module.
motion = fig.box(196, ROW1 - 17, 76, 34, 'Motion', 'Kalman prediction', tone='teal')
appear = fig.box(196, ROW2 - 17, 76, 34, 'Appearance', 're-ID embedding', tone='teal')
MY, MH = 49, 86
match = fig.box(290, MY, 74, MH, 'Matching', 'uncertainty-aware cost', tone='blue', emphasis=True, label_dy=-14)
cost = [[0.95, 0.15, 0.30, 0.10], [0.20, 0.85, 0.10, 0.35], [0.10, 0.25, 0.90, 0.15], [0.30, 0.10, 0.20, 0.55]]
fig.matrix(match.cx - 13.5, MY + MH - 36, cost, cell=6, gap=1, tone='blue')
fig.arrow(head.right, appear.left, label='$\\mathcal{D}_t$')
fig.arrow(motion.right, match.port('left', (ROW1 - MY) / MH))
fig.arrow(appear.right, match.port('left', (ROW2 - MY) / MH))

# Stage 3.
update = fig.box(392, ROW1 - 17, 72, 34, 'Track update', 'Kalman correction', tone='gray')
life = fig.box(392, ROW2 - 17, 72, 34, 'Birth / death', 'lifecycle rules', tone='gray')
fig.arrow(match.port('right', (ROW1 - MY) / MH), update.left)
fig.arrow(update.bottom, life.top)

# Recurrent state: tracks of frame t-1 return to the motion cue, routed above the stage labels.
fig.arrow(update.right, motion.left, route=[(479, ROW1), (479, 13), (178, 13), (178, ROW1)], dashed=True,
          label='tracks $\\mathcal{T}_{t-1}$ from the previous frame')

# Output: trajectories.
ox, oy, ow, oh = 488, ROW2 - 12, 26, 24
fig.raw(f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="1.5" fill="#FFFFFF" '
        f'stroke="{TONES["gray"]["line"]}" stroke-width="0.7"/>')
for pts, tone in ((((2, 18), (8, 13), (14, 12), (22, 6)), 'blue'),
                  (((3, 6), (9, 9), (16, 15), (23, 18)), 'orange'),
                  (((4, 21), (11, 19), (18, 20), (23, 13)), 'teal')):
    path = ' '.join(f'{ox + x},{oy + y}' for x, y in pts)
    fig.raw(f'<polyline points="{path}" fill="none" stroke="{TONES[tone]["line"]}" stroke-width="1.1" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')
    ex, ey = pts[-1]
    fig.raw(f'<circle cx="{ox + ex}" cy="{oy + ey}" r="1.5" fill="{TONES[tone]["line"]}"/>')
fig.arrow(life.right, (ox - 1, ROW2))
fig.text(ox + ow / 2, ROW2 + 25, 'Tracks\n$\\mathcal{T}_t$', T.small, color=T.muted)

# Legend, centred under the figure.
fig.legend(fig.W / 2, 168, [('emph', 'Proposed module', 'blue'), ('box', 'Cue / representation', 'teal'),
                            ('box', 'Standard component', 'gray'), ('arrow', 'Data flow'),
                            ('dashed', 'Recurrent state')], align='center')

fig.export(args.out, '01_framework', args.formats, args.dpi)
