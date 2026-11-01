#!/usr/bin/env python3
"""Cape Jones 2D dance v2 - puppet from the DRAWN art (owner correction #5).

Character source: characters/sheets/04-action-flight-vfx-reference.jpg,
the 'HOVERING' full-body figure - drawn 2D art, viewed and confirmed.
The 01 T-pose turnaround (the 3D rig's sheet, source of v1's split cape)
is BANNED as an animation/likeness source and is not used anywhere here.
Same joint engineering as before (socket discs, rounded roots, per-pose
silhouette hole-fill so the cape is one solid piece), new geometry for
this figure: arms hang at the sides, cape wraps both legs.
Dance keys/sampler imported from build_dance_v2 (owner correction #4).
"""
import cv2, numpy as np
from PIL import Image, ImageDraw
import os, json, importlib.util

spec = importlib.util.spec_from_file_location('bd2', os.path.join(os.path.dirname(__file__), 'build_dance_v2.py'))
bd2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd2)
sample_spec, LOOP = bd2.sample_spec, bd2.LOOP
poly_mask, disc_mask, cut, rot_about = bd2.poly_mask, bd2.disc_mask, bd2.cut, bd2.rot_about

ROOT = bd2.ROOT
PARTS2 = f'{ROOT}/parts2'

def segment(fig):
    w, h = fig.size
    def P(fx, fy): return (fx * w, fy * h)
    arr = np.array(fig)
    bright = arr[:, :, :3].max(axis=2)
    R, G, Bc = arr[:, :, 0].astype(int), arr[:, :, 1].astype(int), arr[:, :, 2].astype(int)
    silh = arr[:, :, 3] > 0
    piv = {'head': P(0.42, 0.19), 'torso': P(0.43, 0.365),
           'arm_l': P(0.28, 0.205), 'arm_r': P(0.575, 0.205),
           'leg_l': P(0.345, 0.395), 'leg_r': P(0.505, 0.395), 'cape': P(0.45, 0.18)}

    m_head = poly_mask(fig.size, [P(0.295, 0.0), P(0.545, 0.0), P(0.565, 0.215), P(0.275, 0.215)])
    m_torso = poly_mask(fig.size, [P(0.235, 0.15), P(0.63, 0.15), P(0.63, 0.38), P(0.235, 0.38)])
    m_arm_l = np.maximum(np.array(poly_mask(fig.size, [P(0.06, 0.15), P(0.315, 0.15), P(0.315, 0.51), P(0.06, 0.51)])),
                         np.array(disc_mask(fig.size, *piv['arm_l'], 0.115 * w)))
    m_arm_r = np.maximum(np.array(poly_mask(fig.size, [P(0.535, 0.15), P(0.75, 0.15), P(0.75, 0.51), P(0.535, 0.51)])),
                         np.array(disc_mask(fig.size, *piv['arm_r'], 0.115 * w)))
    m_arm_l = Image.fromarray(m_arm_l); m_arm_r = Image.fromarray(m_arm_r)
    m_leg_l = poly_mask(fig.size, [P(0.225, 0.335), P(0.44, 0.335), P(0.44, 1.0), P(0.225, 1.0)])
    m_leg_r = poly_mask(fig.size, [P(0.415, 0.335), P(0.615, 0.335), P(0.615, 1.0), P(0.415, 1.0)])

    # ---- layer ownership: every pixel belongs to exactly ONE moving part.
    # Priority: head > torso > CAPE (by colour) > arms > legs. The cape must
    # outrank the arm/leg RECTANGLES: a rectangle that owns the cape art
    # behind a limb drags a black slab with straight edges when the limb
    # swings (seen in the first parts2 pass). Sheet-background-coloured
    # pixels enclosed in the silhouette (the see-through gap between the
    # legs) belong to NO part - they stay transparent and the hole-fill
    # bridges them only when the legs are together, as a solid cape should.
    def A(m): return np.array(m)
    rects = {'head': A(m_head), 'torso': A(m_torso), 'arm_l': A(m_arm_l), 'arm_r': A(m_arm_r),
             'leg_l': A(m_leg_l), 'leg_r': A(m_leg_r)}
    # sheet-background colour measured from the extraction's own transparent
    # pixels; silhouette pixels within a tight tolerance of it are the
    # see-through gaps (a loose HSV test eats the blue-tinted suit whites -
    # learned on the first parts2 pass, which shredded the suit)
    bgpx = arr[arr[:, :, 3] == 0][:, :3]
    bgcol = np.median(bgpx, axis=0)
    dist = np.abs(arr[:, :, :3].astype(int) - bgcol.astype(int)).max(axis=2)
    bg_gap = silh & (dist < 20)
    # FINAL ownership: geometric part masks win first (head > torso > arms >
    # legs) so every part keeps its own outline; the cape takes the dark/
    # purple pixels no part claimed; inside an arm/leg mask only components
    # touching the joint core belong to the limb - a cape slab caught in the
    # rectangle is separate and falls back to the cape pool. (Two earlier
    # orders failed on camera: parts-first dragged cape slabs; cape-first
    # handed the cape every part's outline network, which then ghosted.)
    cape_col = silh & ((bright < 120) | ((Bc > R) & (Bc >= G) & (bright < 205))) & ~bg_gap
    owned = {}
    taken = bg_gap.copy()
    for name in ('head', 'torso', 'arm_l', 'arm_r', 'leg_l', 'leg_r'):
        owned[name] = (rects[name] > 0) & silh & ~taken
        taken |= owned[name]
    def keep_core(mask_bool, pivot, r_frac=0.055):
        n, lab = cv2.connectedComponents(mask_bool.astype(np.uint8), 8)
        if n <= 2:
            return mask_bool
        yy, xx = np.mgrid[0:h, 0:w]
        core = (xx - pivot[0]) ** 2 + (yy - pivot[1]) ** 2 <= (r_frac * w) ** 2
        keep_ids = [i for i in range(1, n) if (lab[core] == i).any()]
        return np.isin(lab, keep_ids)
    for name, pv, rf in (('arm_l', piv['arm_l'], 0.11), ('arm_r', piv['arm_r'], 0.11),
                         ('leg_l', piv['leg_l'], 0.08), ('leg_r', piv['leg_r'], 0.08)):
        kept = keep_core(owned[name], pv, rf)
        taken = taken & ~(owned[name] & ~kept)
        owned[name] = kept
    cape_own = cape_col & ~taken
    cape_np = (cape_own * 255).astype(np.uint8)
    cape_np = cv2.morphologyEx(cape_np, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cape_np = np.where(taken & ~cape_own, 0, cape_np).astype(np.uint8)
    cape_mask = Image.fromarray(cape_np)

    def owned_cut(name):
        m = Image.fromarray((owned[name] * 255).astype(np.uint8))
        return clean(cut(fig, m))
    def clean(layer, min_frac=0.02):
        """Drop detached fragments: a part layer keeps only its substantial
        connected pieces. Rectangles catch foreign outline strokes (cape
        fold lines inside a leg rect, torso edges inside an arm rect) that
        otherwise rotate rigidly with the part and land as floating
        scribbles - the shard class the owner named."""
        a = np.array(layer.getchannel('A'))
        n, lab, stats, _ = cv2.connectedComponentsWithStats((a > 0).astype(np.uint8), 8)
        if n <= 2:
            return layer
        total = stats[1:, cv2.CC_STAT_AREA].sum()
        keep_ids = [i + 1 for i, ar in enumerate(stats[1:, cv2.CC_STAT_AREA]) if ar >= min_frac * total]
        keep = np.isin(lab, keep_ids)
        out = layer.copy()
        out.putalpha(Image.fromarray(np.where(keep, a, 0).astype(np.uint8)))
        return out

    # underlay texture (cape-dark gradient + fold bands), rgb only
    grad = np.linspace(0, 1, h)[:, None]
    base = (np.array([36, 26, 52]) * (1 - grad) + np.array([16, 12, 28]) * grad).astype(np.uint8)
    under = np.repeat(base[:, None, :], w, axis=1)
    folds = np.zeros((h, w), np.float32)
    for fx, fw_, depth in [(0.16, 40, 9), (0.45, 30, 6), (0.72, 38, 9), (0.90, 30, 7)]:
        xs = np.arange(w)[None, :]
        folds += depth * np.exp(-((xs - fx * w) ** 2) / (2 * (fw_ / 2) ** 2))
    under = np.clip(under.astype(np.float32) - folds[:, :, None], 0, 255).astype(np.uint8)
    underlay_tex = Image.fromarray(under, 'RGB')

    empty = Image.new('RGBA', fig.size, (0, 0, 0, 0))
    layers = {'underlay_tex': underlay_tex, 'cape': clean(cut(fig, cape_mask)),
              'leg_r': owned_cut('leg_r'), 'leg_l': owned_cut('leg_l'),
              'torso': owned_cut('torso'),
              'sock_l': empty, 'sock_r': empty,
              'arm_l': owned_cut('arm_l'), 'arm_r': owned_cut('arm_r'),
              'head': owned_cut('head')}
    for k, v in layers.items():
        v.save(f'{PARTS2}/layer_{k}.png')
    json.dump({'size': [w, h], 'pivots': {k: list(v) for k, v in piv.items()}},
              open(f'{PARTS2}/pivots.json', 'w'))
    return layers, piv

STATIC = {'sock_l', 'sock_r'}
ORDER = ['cape', 'leg_r', 'leg_l', 'torso', 'sock_l', 'sock_r', 'arm_l', 'arm_r', 'head']

def sample(f):
    """bd2's sampler, with rotation signs corrected for THIS figure: its
    arms hang down (the donor keys were written for a T-pose), and PIL
    rotates counter-clockwise as displayed, so arm/head/torso angles flip.
    Legs and cape were already correct and are untouched."""
    s = dict(sample_spec(f))
    for k in ('arm_l', 'arm_r', 'head', 'torso'):
        r, dx, dy = s[k]
        s[k] = (-r, dx, dy)
    return s

def build_drawing(layers, piv, spec_d):
    canvas = Image.new('RGBA', layers['cape'].size, (0, 0, 0, 0))
    for name in ORDER:
        if name in STATIC:
            canvas.alpha_composite(layers[name], (0, 0))
        else:
            rot, dx, dy = spec_d[name]
            canvas.alpha_composite(rot_about(layers[name], rot, piv[name], dx, dy), (0, 0))
    # HOLE FILL: this drawing's own silhouette, dilated, filled cape-dark,
    # behind the pieces - the cape reads as one solid piece in every pose.
    a = np.array(canvas.getchannel('A'))
    sil = cv2.dilate((a > 0).astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
    under = layers['underlay_tex'].copy()
    under.putalpha(Image.fromarray(sil))
    base = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    base.alpha_composite(under, (0, 0)); base.alpha_composite(canvas, (0, 0))
    canvas = base
    rdx, rdy = spec_d.get('root_dx', 0), spec_d.get('root_dy', 0)
    if rdx or rdy:
        shifted = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        shifted.alpha_composite(canvas, (int(rdx), int(rdy)))
        canvas = shifted
    return canvas

if __name__ == '__main__':
    fig = Image.open(f'{PARTS2}/figure2_rgba.png')
    print('figure2 loaded', fig.size)
    layers, piv = segment(fig)
    sheet_frames = [0, 5, 10, 15, 20, 26, 32, 36, 41, 45]
    sheet = Image.new('RGB', (fig.size[0] * 5 // 2, fig.size[1]), (120, 130, 140))
    draws = {}
    for i, f in enumerate(sheet_frames):
        d = build_drawing(layers, piv, sample(f))
        draws[f] = d
        bg = Image.new('RGBA', fig.size, (120, 130, 140, 255)); bg.alpha_composite(d)
        small = bg.convert('RGB').resize((fig.size[0] // 2, fig.size[1] // 2), Image.LANCZOS)
        sheet.paste(small, ((i % 5) * fig.size[0] // 2, (i // 5) * fig.size[1] // 2))
    sheet.save(f'{PARTS2}/dance_test_sheet.png')
    def zoom(f, box, out, size=(880, 880)):
        d = draws.get(f) or build_drawing(layers, piv, sample(f))
        bg = Image.new('RGBA', fig.size, (110, 190, 245, 255)); bg.alpha_composite(d)
        bg.convert('RGB').crop(box).resize(size).save(f'{PARTS2}/{out}')
    zoom(5, (60, 60, 300, 300), 'zoom_step_r.png')
    zoom(26, (190, 60, 430, 300), 'zoom_twist_l.png')
    zoom(5, (90, 200, 340, 430), 'zoom_cape_legs.png', (810, 745))
    zoom(5, (90, 380, 340, 622), 'zoom_feet_step.png', (880, 850))
    zoom(32, (90, 380, 340, 622), 'zoom_feet_hop.png', (880, 850))
    zoom(36, (90, 380, 340, 622), 'zoom_feet_land.png', (880, 850))
    print('test sheet + acceptance zooms saved (parts2)')
