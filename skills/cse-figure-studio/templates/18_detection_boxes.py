"""18 Detection or tracking bounding boxes on image sequences.

Pattern: a row or grid of frames from a video or image sequence, each showing ground-truth and
predicted bounding boxes with distinct line styles and colours, class labels and confidence scores
positioned consistently (top-left inside the box when possible, above when occluded), a compact
legend distinguishing GT from predictions, and no overlapping text. Use distinct hues for different
object classes and reserve OURS colour for your method when comparing multiple detectors.
DEMO DATA: synthetic boxes on placeholder images; replace with actual frames and detections, and
state the dataset, sequence name, frame numbers, detector configuration, and IoU/confidence
threshold in the caption. Include a scale bar or state the image resolution.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

pp.mark_demo('synthetic boxes on placeholder images')
rng = pp.demo_rng()
from matplotlib.patches import Rectangle

# Create a placeholder image grid (3 frames)
fig, axes = pp.figure('ieee-double', aspect=0.3, nrows=1, ncols=3, squeeze=False)
axes = axes.flatten()

frame_data = [
    # Frame 1: single object
    {'gt': [(30, 40, 90, 120, 'person')], 'pred': [(32, 38, 88, 118, 'person', 0.95)]},
    # Frame 2: multiple objects
    {'gt': [(20, 30, 70, 110, 'person'), (120, 50, 160, 100, 'car')],
     'pred': [(22, 28, 68, 108, 'person', 0.92), (118, 48, 158, 98, 'car', 0.88)]},
    # Frame 3: missed detection
    {'gt': [(40, 60, 100, 140, 'person'), (140, 70, 190, 130, 'bicycle')],
     'pred': [(42, 58, 98, 138, 'person', 0.79)]}
]

class_colors = {'person': pp.OURS, 'car': pp.BASELINES[0], 'bicycle': pp.BASELINES[2]}

for idx, (ax, data) in enumerate(zip(axes, frame_data)):
    # Create synthetic image
    img = rng.integers(180, 220, (200, 240, 3), dtype=np.uint8)
    ax.imshow(img, aspect='equal')
    
    # Draw ground truth boxes (dashed)
    for x1, y1, x2, y2, cls in data['gt']:
        color = class_colors.get(cls, pp.INK)
        rect = Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1.1, edgecolor=color, 
                           facecolor='none', linestyle=(0, (4, 3)), zorder=3)
        ax.add_patch(rect)
        ax.text(x1 + 2, y1 + 9, cls, fontsize=7, color=color, weight='normal',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8))
    
    # Draw predictions (solid)
    for x1, y1, x2, y2, cls, conf in data['pred']:
        color = class_colors.get(cls, pp.INK)
        rect = Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1.4, edgecolor=color,
                           facecolor='none', linestyle='-', zorder=4)
        ax.add_patch(rect)
        label = f'{cls} {conf:.2f}'
        ax.text(x1 + 2, y2 - 4, label, fontsize=7, color=color, weight='bold',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.9))
    
    ax.set_xlim(0, 240)
    ax.set_ylim(200, 0)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Frame {idx * 15 + 1:03d}', fontsize=8, pad=3)

# Add legend to the figure
from matplotlib.lines import Line2D
handles = [Line2D([0], [0], color=pp.INK, lw=1.1, ls=(0, (4, 3)), label='Ground truth'),
           Line2D([0], [0], color=pp.INK, lw=1.4, ls='-', label='Detection')]
fig.legend(handles=handles, loc='lower center', ncol=2, frameon=False, 
          bbox_to_anchor=(0.5, -0.02), columnspacing=1.5, handlelength=2.0)

pp.save(fig, args.out, '18_detection_boxes', args.formats, args.dpi)
