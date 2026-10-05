"""19 Re-identification ranking: one query, the top-10 gallery of a baseline and of ours.

Pattern: the query at the left of each row behind a dashed separator, ranks 1-10 at identical size,
correct identity marked by a green frame plus a check and a wrong identity by a vermilion frame plus
a cross (never colour alone), the similarity under every thumbnail, the method name as a row label
with ours last and accented. Same query, same gallery and same crops in both rows; true matches from
the query's own camera are excluded, as in the Market-1501 protocol.
DEMO DATA: the people are drawn illustrations and the rankings are placeholders; the output is
stamped. Replace thumbnail() with your crops (dataset licence and face policy permitting) and RANKS
with the ranked gallery your evaluator produced; state dataset, query ID, single or multi query and
whether re-ranking is applied in the caption.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402
import demo_scene as ds  # noqa: E402
import pubplot as pp  # noqa: E402

args = pp.template_args(__doc__)
pp.use(args.theme, args.lang)
pp.mark_demo('illustrated crops and placeholder rankings')   # delete with thumbnail() and RANKS

TW, TH = 64, 128                   # crop size in pixels (width x height), as in Market-1501

# ---------------------------------------------------------------- DEMO identities and rankings
OUTFITS = {   # q is the query identity; the others are hard negatives that share some clothing
    'q': dict(top='#2F5D8C', legs='#2A2C31', hair='#2B2522', skin='#E3B590', bag='#C9822B'),
    'n1': dict(top='#2F5D8C', legs='#C9B48C', hair='#3A2A22', skin='#C98E67', bag=None),
    'n2': dict(top='#3B4A68', legs='#2A2C31', hair='#2B2522', skin='#F1CBA8', bag='#6B4E3A'),
    'n3': dict(top='#6E8240', legs='#2A2C31', hair='#1F1C1A', skin='#E3B590', bag=None),
    'n4': dict(top='#2F5D8C', legs='#2A2C31', hair='#B08A5A', skin='#F1CBA8', bag=None),
    'n5': dict(top='#A9473B', legs='#3B4049', hair='#2B2522', skin='#C98E67', bag=None),
    'n6': dict(top='#58708F', legs='#5A5F66', hair='#2B2522', skin='#E3B590', bag='#2A2C31'),
}
CAMS = {1: ('#E7E2D8', '#CEC7BA'), 2: ('#DDE3E9', '#C2CAD2'), 3: ('#E3E6DC', '#C8CCBE'), 4: ('#EAE4E6', '#D1CACE')}
QUERY = ('q', 1, 0)                # (identity, camera, pose)
RANKS = {   # method -> ranked gallery [(identity, camera, pose), ...] and similarity scores
    'Baseline': ([('n4', 2, 1), ('q', 3, 0), ('n1', 1, 2), ('n2', 4, 1), ('q', 2, 2), ('n6', 3, 0), ('n1', 3, 1),
                  ('n3', 2, 0), ('q', 4, 1), ('n5', 1, 2)],
                 [0.91, 0.89, 0.86, 0.84, 0.82, 0.79, 0.77, 0.74, 0.72, 0.70]),
    'Ours': ([('q', 3, 0), ('q', 2, 2), ('n4', 2, 1), ('q', 4, 1), ('n1', 1, 2), ('n2', 4, 1), ('q', 2, 0),
              ('n6', 3, 0), ('n3', 2, 0), ('n5', 1, 2)],
             [0.95, 0.93, 0.88, 0.86, 0.80, 0.77, 0.75, 0.71, 0.69, 0.66]),
}


def thumbnail(item):
    """DEMO: a drawn crop. Replace with your image, e.g. imageio.v3.imread(path) resized to TW x TH."""
    ident, cam, pose = item
    o = OUTFITS[ident]
    h, feet = (100, 120) if pose != 2 else (88, 116)
    x = TW / 2 + (-3, 2, 4)[pose]

    def draw(ax):
        ds.backdrop(ax, TW, TH, *CAMS[cam])
        ds.person(ax, x, feet, h, o['top'], o['legs'], o['hair'], o['skin'], o['bag'], stride=pose % 2,
                  flip=(cam + pose) % 2 == 1)
    return pp.render_array(draw, TW, TH, scale=4)


def mark(ax, ok):
    """Check or cross badge in the lower-right corner, drawn as strokes (no font glyph needed)."""
    cx, cy, r = TW - 11, TH - 11, 8
    ax.add_patch(Circle((cx, cy), r, facecolor=pp.GOOD if ok else pp.BAD, edgecolor='#FFFFFF', linewidth=0.8,
                        zorder=6))
    pts = [(-4, 0.5), (-1.2, 3.4), (4.2, -3.2)] if ok else None
    kw = dict(color='#FFFFFF', lw=1.4, solid_capstyle='round', solid_joinstyle='round', zorder=7)
    if ok:
        ax.add_line(Line2D([cx + p[0] for p in pts], [cy + p[1] for p in pts], **kw))
    else:
        for sx in (-1, 1):
            ax.add_line(Line2D([cx - 3.3 * sx, cx + 3.3 * sx], [cy - 3.3, cy + 3.3], **kw))


# ---------------------------------------------------------------- layout (inches) and drawing
FW = pp.width_in('ieee-double')
MARGIN, LABEL, SEP, GAP = 0.02, 0.22, 0.16, 0.035
HEAD, SCORE, ROWGAP = 0.21, 0.19, 0.05
TWI = (FW - 2 * MARGIN - LABEL - SEP - 9 * GAP) / 11
THI = TWI * TH / TW
fig = pp.canvas(FW, HEAD + 2 * (THI + SCORE) + ROWGAP)
fs = pp.size('annot')
cache = {}

for row, (method, (ranked, scores)) in enumerate(RANKS.items()):
    top = HEAD + row * (THI + SCORE + ROWGAP)
    ours = method == 'Ours'
    fig.text((MARGIN + LABEL / 2) / FW, 1 - (top + THI / 2) / fig.get_size_inches()[1], pp.tr(method, '本文方法' if ours
             else '基线方法'), rotation=90, ha='center', va='center', fontsize=pp.size('label'),
             fontweight='bold' if ours else 'normal', color=pp.OURS if ours else pp.MUTED)
    x = MARGIN + LABEL
    for k, item in enumerate([QUERY] + ranked):
        ax = pp.place(fig, x, top, TWI, THI)
        if item not in cache:
            cache[item] = thumbnail(item)
        is_query = k == 0
        ok = item[0] == QUERY[0]
        pp.image_panel(ax, cache[item], size=(TW, TH), frame=pp.INK if is_query else (pp.GOOD if ok else pp.BAD),
                       lw=1.2 if is_query else 1.5)
        if not is_query:
            mark(ax, ok)
            ax.text(0.5, -0.035, f'{scores[k - 1]:.2f}', transform=ax.transAxes, ha='center', va='top', fontsize=fs,
                    color=pp.INK if ok else pp.MUTED, fontweight='bold' if ok else 'normal')
        if row == 0:
            ax.text(0.5, 1.03, pp.tr('Query', '查询') if is_query else str(k), transform=ax.transAxes, ha='center',
                    va='bottom', fontsize=fs, color=pp.INK if is_query else pp.MUTED,
                    fontweight='bold' if is_query else 'normal')
        x += TWI + (SEP if is_query else GAP)

H_in = fig.get_size_inches()[1]
sx = (MARGIN + LABEL + TWI + SEP / 2) / FW
fig.add_artist(Line2D([sx, sx], [1 - (HEAD - 0.02) / H_in, 0.02 / H_in], transform=fig.transFigure, color='#AEB4BC',
                      lw=0.8, ls=(0, (3, 2.5))))

pp.save(fig, args.out, '19_reid_retrieval', args.formats, args.dpi)
