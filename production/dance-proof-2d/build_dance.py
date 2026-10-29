#!/usr/bin/env python3
"""Cape Jones 2D dance montage - proof of the production model (PR #265).
Cutout puppet built ONLY from the show's own model-sheet stock
(characters/sheets/01-tpose-turnaround.jpg). One 4-drawing dance loop,
flipped for the other direction. Lighting + environment carry the montage.
24fps timeline, drawings on threes (each drawing held 3 frames).
"""
import cv2, numpy as np
from PIL import Image, ImageDraw
import os, json, math

ROOT = os.path.expanduser('~/workspace/_cj-dance-2d/build')
SRC  = os.path.expanduser('~/workspace/cape-jones/characters/sheets/01-tpose-turnaround.jpg')
W, H = 1920, 1080
FPS = 24

# ---------- STAGE 1: extraction (flood-fill roto from the white sheet bg) ----------
def extract_figure():
    img = cv2.imread(SRC)                       # BGR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # candidate background: bright + unsaturated. The white suit is also a
    # candidate, but its black outlines wall it off from the border flood.
    cand = ((hsv[:, :, 2] > 192) & (hsv[:, :, 1] < 42)).astype(np.uint8)
    n, lab = cv2.connectedComponents(cand, 4)
    border_labels = set(np.unique(np.concatenate(
        [lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border_labels))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    # tidy: kill specks, fill pinholes
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 0).astype(np.uint8), 8)
    keep = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
    alpha = np.where(lab == keep, 255, 0).astype(np.uint8)
    rgba = np.dstack([img, alpha])
    ys, xs = np.where(alpha > 0)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    fig = Image.fromarray(rgba).crop(box)
    fig.save(f'{ROOT}/parts/figure_rgba.png')
    print('figure crop', fig.size, 'from box', box)
    return fig

# ---------- STAGE 2: segmentation into puppet layers ----------
def poly_mask(size, pts):
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    d.polygon(pts, fill=255)
    return m

def cut(fig, mask_img):
    out = fig.copy()
    out.putalpha(Image.composite(fig.getchannel('A'), Image.new('L', fig.size, 0), mask_img))
    return out

def segment(fig):
    w, h = fig.size
    def P(fx, fy): return (fx * w, fy * h)
    arr = np.array(fig)
    bright = arr[:, :, :3].max(axis=2)
    silh = arr[:, :, 3] > 0
    # CAPE: dark pixels inside the silhouette (cape + outline), used as back layer.
    # Subtract the other parts' areas so their black outlines don't stay behind
    # as ghost shells when the parts rotate away.
    m_head  = poly_mask(fig.size, [P(0.385, 0.0), P(0.615, 0.0), P(0.625, 0.215), P(0.375, 0.215)])
    m_torso = poly_mask(fig.size, [P(0.355, 0.185), P(0.645, 0.185), P(0.645, 0.52), P(0.355, 0.52)])
    m_arm_l = poly_mask(fig.size, [P(0.0, 0.14), P(0.352, 0.14), P(0.352, 0.335), P(0.0, 0.335)])
    m_arm_r = poly_mask(fig.size, [P(0.648, 0.14), P(1.0, 0.14), P(1.0, 0.335), P(0.648, 0.335)])
    m_leg_l = poly_mask(fig.size, [P(0.345, 0.495), P(0.502, 0.495), P(0.502, 1.0), P(0.345, 1.0)])
    m_leg_r = poly_mask(fig.size, [P(0.498, 0.495), P(0.655, 0.495), P(0.655, 1.0), P(0.498, 1.0)])
    others = np.maximum.reduce([np.array(m) for m in (m_head, m_torso, m_arm_l, m_arm_r)])
    feet_band = np.zeros((h, w), np.uint8); feet_band[int(0.90 * h):, :] = 255
    others = np.maximum(others, np.minimum(np.maximum(np.array(m_leg_l), np.array(m_leg_r)), feet_band))
    cape_np = np.where(silh & (bright < 78) & (others == 0), 255, 0).astype(np.uint8)
    cape_mask = Image.fromarray(cape_np)
    head  = cut(fig, m_head)
    torso = cut(fig, m_torso)
    arm_l = cut(fig, m_arm_l)
    arm_r = cut(fig, m_arm_r)
    leg_l = cut(fig, m_leg_l)
    leg_r = cut(fig, m_leg_r)
    layers = {'cape': cape_mask and cut(fig, cape_mask), 'leg_r': leg_r, 'leg_l': leg_l,
              'torso': torso, 'arm_l': arm_l, 'arm_r': arm_r, 'head': head}
    # pivots in figure coords
    piv = {'head': P(0.5, 0.20), 'torso': P(0.5, 0.50),
           'arm_l': P(0.335, 0.235), 'arm_r': P(0.665, 0.235),
           'leg_l': P(0.435, 0.515), 'leg_r': P(0.565, 0.515), 'cape': P(0.5, 0.2)}
    for k, v in layers.items():
        v.save(f'{ROOT}/parts/layer_{k}.png')
    json.dump({'size': [w, h], 'pivots': {k: list(v) for k, v in piv.items()}},
              open(f'{ROOT}/parts/pivots.json', 'w'))
    return layers, piv

def rot_about(layer, angle, pivot, dx=0, dy=0):
    if angle == 0 and dx == 0 and dy == 0:
        return layer
    out = layer.rotate(angle, resample=Image.BICUBIC, center=pivot)
    if dx or dy:
        canvas = Image.new('RGBA', layer.size, (0, 0, 0, 0))
        canvas.alpha_composite(out, (int(dx), int(dy)))
        out = canvas
    return out

# ---------- STAGE 3: the dance. ONE loop of 4 drawings. ----------
# transforms per layer: (rot_deg, dx, dy) in figure pixels (fig ~1200x1100)
DANCE = [
    # D1 lean left, arms in opposition, legs split, weight shifted left
    {'root_dx': -10,
     'head': (-5, -4, 3), 'torso': (-3, -3, 0), 'cape': (-1, 0, 0),
     'arm_l': (28, 0, 0), 'arm_r': (38, 0, 0), 'leg_l': (-9, 0, 0), 'leg_r': (8, 0, 0)},
    # D2 crouch centre, arms low
    {'root_dx': 0,
     'head': (0, 0, 9), 'torso': (0, 0, 7), 'cape': (0, 0, 0),
     'arm_l': (-8, 0, 0), 'arm_r': (8, 0, 0), 'leg_l': (3, 0, 0), 'leg_r': (-3, 0, 0)},
    # D3 lean right (mirror energy of D1)
    {'root_dx': 10,
     'head': (5, 4, 3), 'torso': (3, 3, 0), 'cape': (1, 0, 0),
     'arm_l': (-38, 0, 0), 'arm_r': (-28, 0, 0), 'leg_l': (-8, 0, 0), 'leg_r': (9, 0, 0)},
    # D4 crouch centre B, arms a touch higher (the bounce)
    {'root_dx': 0,
     'head': (-3, 0, 8), 'torso': (0, 0, 6), 'cape': (0, 0, 0),
     'arm_l': (12, 0, 0), 'arm_r': (-12, 0, 0), 'leg_l': (-3, 0, 0), 'leg_r': (3, 0, 0)},
]
ORDER = ['cape', 'leg_r', 'leg_l', 'torso', 'arm_l', 'arm_r', 'head']

def build_drawing(layers, piv, spec):
    canvas = Image.new('RGBA', layers['cape'].size, (0, 0, 0, 0))
    for name in ORDER:
        rot, dx, dy = spec[name]
        canvas.alpha_composite(rot_about(layers[name], rot, piv[name], dx, dy), (0, 0))
    rdx = spec.get('root_dx', 0)
    if rdx:
        shifted = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        shifted.alpha_composite(canvas, (int(rdx), 0))
        canvas = shifted
    return canvas

if __name__ == '__main__':
    os.makedirs(f'{ROOT}/parts', exist_ok=True)
    if os.path.exists(f'{ROOT}/parts/figure_rgba.png'):
        fig = Image.open(f'{ROOT}/parts/figure_rgba.png')
        print('figure loaded', fig.size)
    else:
        fig = extract_figure()
    layers, piv = segment(fig)
    # test sheet: the 4 drawings on a checkerboard so the owner can judge the loop
    sheet = Image.new('RGB', (fig.size[0] * 2, fig.size[1] * 2), (70, 70, 70))
    for i, spec in enumerate(DANCE):
        d = build_drawing(layers, piv, spec)
        bg = Image.new('RGBA', fig.size, (255, 255, 255, 255))
        bg.alpha_composite(d)
        sheet.paste(bg.convert('RGB'), ((i % 2) * fig.size[0], (i // 2) * fig.size[1]))
    sheet.save(f'{ROOT}/parts/dance_test_sheet.png')
    print('test sheet saved', sheet.size)
