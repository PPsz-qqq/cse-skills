"""19 Re-identification retrieval ranks with query and gallery.

Pattern: a query image on the left, followed by ranked gallery results in descending similarity
order, with correct matches highlighted by a border or background, incorrect matches in neutral
styling, rank numbers in consistent positions, and optional similarity scores below each thumbnail.
Lay out as a single row when showing top-K (K <= 10), or as a grid for larger galleries.
DEMO DATA: synthetic placeholder thumbnails with random correct/incorrect patterns; replace with
actual query/gallery images from a re-ID dataset (Market-1501, DukeMTMC, MSMT17, VeRi), state the
dataset name, query ID, gallery size, rank metric (CMC@k, mAP), model name, and any pre/post
processing (cropping, reranking) in the caption.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import numpy as np  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)

pp.mark_demo('synthetic retrieval results with placeholder images')
rng = pp.demo_rng()
from matplotlib.patches import Rectangle

# Create figure: query + 10 gallery results
fig, axes = pp.figure('ieee-double', aspect=0.35, nrows=1, ncols=11, squeeze=False)
axes = axes.flatten()

# Query image (leftmost)
query_img = rng.integers(60, 120, (120, 80, 3), dtype=np.uint8)
# Add a distinctive color tint to query
query_img[:, :, 0] = np.clip(query_img[:, :, 0] + 40, 0, 255)  # red tint

axes[0].imshow(query_img, aspect='auto')
axes[0].set_title('Query', fontsize=8, weight='bold', pad=3)
axes[0].axis('off')
# Query border
rect = Rectangle((0, 0), 79, 119, linewidth=2.5, edgecolor=pp.OURS, 
                   facecolor='none', zorder=10)
axes[0].add_patch(rect)

# Gallery results: ranks 1-10
# Correct matches at ranks 1, 3, 5, 9 (typical sparse retrieval)
correct_ranks = {1, 3, 5, 9}
similarities = [0.94, 0.87, 0.83, 0.79, 0.76, 0.71, 0.68, 0.64, 0.61, 0.58]

for rank in range(1, 11):
    ax = axes[rank]
    is_correct = rank in correct_ranks
    
    # Generate gallery image
    if is_correct:
        # Similar appearance to query (red tint)
        gallery_img = rng.integers(60, 120, (120, 80, 3), dtype=np.uint8)
        gallery_img[:, :, 0] = np.clip(gallery_img[:, :, 0] + 35, 0, 255)
    else:
        # Different appearance (blue/green tint)
        gallery_img = rng.integers(80, 140, (120, 80, 3), dtype=np.uint8)
        gallery_img[:, :, 1] = np.clip(gallery_img[:, :, 1] + 30, 0, 255)
    
    ax.imshow(gallery_img, aspect='auto')
    ax.axis('off')
    
    # Border: green for correct, neutral for incorrect
    border_color = '#2D9F4E' if is_correct else '#8A9099'
    border_width = 2.0 if is_correct else 0.8
    rect = Rectangle((0, 0), 79, 119, linewidth=border_width, edgecolor=border_color,
                       facecolor='none', zorder=10)
    ax.add_patch(rect)
    
    # Rank label (top-left corner)
    ax.text(2, 8, str(rank), fontsize=7.5, color='white', weight='bold',
           bbox=dict(boxstyle='round,pad=0.25', facecolor='#2B3139', edgecolor='none', alpha=0.85),
           zorder=11)
    
    # Similarity score (bottom)
    score_color = '#2D9F4E' if is_correct else pp.INK
    ax.text(40, 127, f'{similarities[rank-1]:.2f}', fontsize=6.5, ha='center', color=score_color,
           weight='bold' if is_correct else 'normal')

# Add legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
handles = [Patch(facecolor='none', edgecolor='#2D9F4E', linewidth=2.0, label='Correct match'),
           Patch(facecolor='none', edgecolor='#8A9099', linewidth=0.8, label='Incorrect')]
fig.legend(handles=handles, loc='lower center', ncol=2, frameon=False,
          bbox_to_anchor=(0.5, -0.02), columnspacing=1.5, handlelength=1.8)

pp.save(fig, args.out, '19_reid_retrieval', args.formats, args.dpi)
