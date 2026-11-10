#!/usr/bin/env python3
"""Cape Jones 2D dance proof v2 - puppet rebuild (fixes v1's gaps/seams).

Same source stock, same 4-drawing loop, same transforms as v1. What changed
is the puppet engineering, per the owner's verdict on v1 (draft: cutout
pieces, seams and gaps - the shoulder notch):

- SHOULDER SOCKET DISCS: a disc of the sheet's own art, centred exactly on
  each shoulder pivot, sits between torso and arm. It never rotates, so the
  joint is always covered by suit art; the arm rotates over it.
- ROUNDED ARM ROOTS: each arm mask is extended inward and unioned with a
  disc around its pivot, so the arm's root edge is a circle centred on the
  pivot - rotation cannot sweep a corner open (v1's rectangles did).
- HEAD/COWL EXTENDED: the head mask runs further down the cowl flare so the
  cowl overlaps the chest with real art at every tilt in the loop.
- LEGS EXTENDED UP under the torso (hidden overlap at the hips).
- CAPE UNDERLAY: the full silhouette, dilated, filled with a dark cape
  gradient with painted fold shading, behind everything. Any residual
  sliver between pieces reads as cape shadow, never as background.
- Cape mask gets a morphological close + the new parts subtracted, so no
  pinhole cracks or ghost shells survive.
"""
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os, json

ROOT = os.path.expanduser('~/workspace/_cj-dance-v2/build')
V1PARTS = os.path.expanduser('~/workspace/_cj-dance-2d/build/parts')
os.makedirs(f'{ROOT}/parts', exist_ok=True)

def poly_mask(size, pts):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m

def disc_mask(size, cx, cy, r, feather=0):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    if feather:
        m = m.filter(ImageFilter.GaussianBlur(feather))
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
    piv = {'head': P(0.5, 0.20), 'torso': P(0.5, 0.50),
           'arm_l': P(0.335, 0.235), 'arm_r': P(0.665, 0.235),
           'leg_l': P(0.435, 0.515), 'leg_r': P(0.565, 0.515), 'cape': P(0.5, 0.2)}

    # ---- masks, now with deliberate overlaps ----
    # head: runs down the cowl flare (was 0.215, now 0.26, wider at the base)
    m_head = poly_mask(fig.size, [P(0.385, 0.0), P(0.615, 0.0), P(0.635, 0.26), P(0.365, 0.26)])
    m_torso = poly_mask(fig.size, [P(0.355, 0.185), P(0.645, 0.185), P(0.645, 0.52), P(0.355, 0.52)])
    # arms: rectangle extended inward + rounded root disc on the pivot
    m_arm_l = np.maximum(np.array(poly_mask(fig.size, [P(0.0, 0.14), P(0.40, 0.14), P(0.40, 0.335), P(0.0, 0.335)])),
                         np.array(disc_mask(fig.size, *piv['arm_l'], 0.088 * w)))
    m_arm_r = np.maximum(np.array(poly_mask(fig.size, [P(0.60, 0.14), P(1.0, 0.14), P(1.0, 0.335), P(0.60, 0.335)])),
                         np.array(disc_mask(fig.size, *piv['arm_r'], 0.088 * w)))
    m_arm_l = Image.fromarray(m_arm_l); m_arm_r = Image.fromarray(m_arm_r)
    # legs: extended up to 0.44 (hidden under the torso, which draws above)
    m_leg_l = poly_mask(fig.size, [P(0.345, 0.44), P(0.502, 0.44), P(0.502, 1.0), P(0.345, 1.0)])
    m_leg_r = poly_mask(fig.size, [P(0.498, 0.44), P(0.655, 0.44), P(0.655, 1.0), P(0.498, 1.0)])

    # ---- cape: dark art only, other parts subtracted, cracks closed ----
    others = np.maximum.reduce([np.array(m) for m in (m_head, m_torso, m_arm_l, m_arm_r)])
    feet_band = np.zeros((h, w), np.uint8); feet_band[int(0.90 * h):, :] = 255
    others = np.maximum(others, np.minimum(np.maximum(np.array(m_leg_l), np.array(m_leg_r)), feet_band))
    cape_np = np.where(silh & (bright < 78) & (others == 0), 255, 0).astype(np.uint8)
    cape_np = cv2.morphologyEx(cape_np, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cape_mask = Image.fromarray(cape_np)

    # ---- cape underlay TEXTURE (rgb only; alpha comes from each posed
    # drawing's own silhouette in build_drawing - a static T-pose underlay
    # would ghost the T-pose arms behind the posed ones) ----
    grad = np.linspace(0, 1, h)[:, None]
    base = (np.array([34, 34, 44]) * (1 - grad) + np.array([14, 14, 19]) * grad).astype(np.uint8)
    under = np.repeat(base[:, None, :], w, axis=1)
    # soft vertical fold bands
    folds = np.zeros((h, w), np.float32)
    for fx, fw_, depth in [(0.30, 46, 10), (0.44, 30, 7), (0.58, 34, 8), (0.70, 42, 10)]:
        cx = fx * w
        xs = np.arange(w)[None, :]
        band = np.exp(-((xs - cx) ** 2) / (2 * (fw_ / 2) ** 2))
        folds += depth * band
    under = np.clip(under.astype(np.float32) - folds[:, :, None], 0, 255).astype(np.uint8)
    underlay_tex = Image.fromarray(under, 'RGB')

    # ---- shoulder socket discs: the sheet's own art, static, feathered rim ----
    def socket(pivot):
        r = int(0.082 * w)
        m = disc_mask(fig.size, pivot[0], pivot[1], r, feather=3)
        return cut(fig, m)
    sock_l, sock_r = socket(piv['arm_l']), socket(piv['arm_r'])

    layers = {'underlay_tex': underlay_tex, 'cape': cut(fig, cape_mask),
              'leg_r': cut(fig, m_leg_r), 'leg_l': cut(fig, m_leg_l),
              'torso': cut(fig, m_torso),
              'sock_l': sock_l, 'sock_r': sock_r,
              'arm_l': cut(fig, m_arm_l), 'arm_r': cut(fig, m_arm_r),
              'head': cut(fig, m_head)}
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

# The dance - owner correction #4 (2026-10-29), his words: "I asked for
# more motion, more animations and frames, in a simple dance, that's
# repetitive, but actually looks like a animation, even if it's funny or
# comical or not a good dance." Space Ghost / JLU level: legs STEP with
# weight transfer (feet leave and meet the ground), a little hop, a
# shuffle, cape swinging, head acting. One 48-frame (2 s) loop, reused in
# every section: the dance does not change, the world does. Transforms are
# eased through the key poses EVERY frame - 48 real frames of motion, not
# held cels. (This puppet render is the VACE DRIVING performance + the
# labelled fallback; shipped frames are VACE redraws, likeness held.)
def _S(head=(0, 0, 0), torso=(0, 0, 0), cape=(0, 0, 0), arm_l=(0, 0, 0), arm_r=(0, 0, 0),
       leg_l=(0, 0, 0), leg_r=(0, 0, 0), root_dx=0, root_dy=0):
    return {'head': head, 'torso': torso, 'cape': cape, 'arm_l': arm_l, 'arm_r': arm_r,
            'leg_l': leg_l, 'leg_r': leg_r, 'root_dx': root_dx, 'root_dy': root_dy}

KEYS = [
    (0,  _S(arm_l=(10, 0, 0), arm_r=(-10, 0, 0), head=(0, 0, 2), root_dy=2)),
    # STEP LEFT: weight shifts over the left leg, right leg swings out
    (5,  _S(root_dx=-30, root_dy=-2, head=(-8, -4, 2), torso=(-5, -4, 0), cape=(6, 0, 0),
            arm_l=(34, 0, 0), arm_r=(-30, 0, 0), leg_l=(-4, 0, 0), leg_r=(22, 0, 0))),
    # PLANT + DIP: right foot lands wide, body drops, arms sweep low
    (10, _S(root_dx=-34, root_dy=12, head=(0, 0, 10), torso=(0, -2, 8), cape=(2, 0, 3),
            arm_l=(-18, 0, 0), arm_r=(18, 0, 0), leg_l=(-10, 0, 0), leg_r=(8, 0, 0))),
    # STEP RIGHT: mirror
    (15, _S(root_dx=30, root_dy=-2, head=(8, 4, 2), torso=(5, 4, 0), cape=(-6, 0, 0),
            arm_l=(30, 0, 0), arm_r=(-34, 0, 0), leg_l=(-22, 0, 0), leg_r=(4, 0, 0))),
    # PLANT + DIP B
    (20, _S(root_dx=34, root_dy=12, head=(-2, 0, 11), torso=(0, 2, 8), cape=(-2, 0, 3),
            arm_l=(18, 0, 0), arm_r=(-18, 0, 0), leg_l=(-8, 0, 0), leg_r=(10, 0, 0))),
    # TWIST + CAPE SWING: windmill arms, head looking off, cape follows late
    (26, _S(root_dx=-10, root_dy=0, head=(-15, -5, 3), torso=(-9, -3, 0), cape=(11, 0, 0),
            arm_l=(46, 0, 0), arm_r=(-44, 0, 0), leg_l=(-12, 0, 0), leg_r=(8, 0, 0))),
    # TA-DA HOP: both feet leave the ground, arms in a V, chin up
    (32, _S(root_dy=-12, head=(-2, 0, -5), torso=(-2, 0, -4), cape=(-4, 0, -2),
            arm_l=(74, 0, 0), arm_r=(-74, 0, 0), leg_l=(6, 0, 0), leg_r=(-6, 0, 0))),
    # LAND CROUCH: weight lands, knees-out crouch, arms out for balance
    (36, _S(root_dy=16, head=(0, 0, 12), torso=(0, 0, 12), cape=(0, 0, 5),
            arm_l=(26, 0, 0), arm_r=(-26, 0, 0), leg_l=(-13, 0, 0), leg_r=(13, 0, 0))),
    # SHUFFLE L / R: quick alternating steps, arms pumping
    (41, _S(root_dx=-12, root_dy=4, head=(-6, 0, 4), torso=(-4, 0, 2), cape=(4, 0, 0),
            arm_l=(22, 0, 0), arm_r=(-8, 0, 0), leg_l=(-16, 0, 0), leg_r=(2, 0, 0))),
    (45, _S(root_dx=12, root_dy=4, head=(6, 0, 4), torso=(4, 0, 2), cape=(-4, 0, 0),
            arm_l=(8, 0, 0), arm_r=(-22, 0, 0), leg_l=(-2, 0, 0), leg_r=(16, 0, 0))),
]
LOOP = 48

def sample_spec(f):
    """Eased (smoothstep) spec at loop frame f - continuous motion."""
    f = f % LOOP
    ks = KEYS + [(LOOP, KEYS[0][1])]
    for (f0, s0), (f1, s1) in zip(ks, ks[1:]):
        if f0 <= f < f1:
            t = (f - f0) / (f1 - f0)
            t = t * t * (3 - 2 * t)
            out = {}
            for k in s0:
                if isinstance(s0[k], tuple):
                    out[k] = tuple(a + (b - a) * t for a, b in zip(s0[k], s1[k]))
                else:
                    out[k] = s0[k] + (s1[k] - s0[k]) * t
            return out
    return ks[-1][1]
# sockets never take a spec transform (round art centred on the pivot);
# the underlay is derived per-drawing in build_drawing.
STATIC = {'sock_l', 'sock_r'}
ORDER = ['cape', 'leg_r', 'leg_l', 'torso', 'sock_l', 'sock_r', 'arm_l', 'arm_r', 'head']

def build_drawing(layers, piv, spec):
    canvas = Image.new('RGBA', layers['cape'].size, (0, 0, 0, 0))
    for name in ORDER:
        if name in STATIC:
            canvas.alpha_composite(layers[name], (0, 0))
        else:
            rot, dx, dy = spec[name]
            canvas.alpha_composite(rot_about(layers[name], rot, piv[name], dx, dy), (0, 0))
    # HOLE FILL: this drawing's own silhouette, dilated a touch, filled with
    # the cape-dark underlay texture, slipped BEHIND the posed pieces. Any
    # sliver left between pieces shows cape shadow, never background; and
    # because the shape comes from the posed drawing, nothing ghosts.
    a = np.array(canvas.getchannel('A'))
    sil = cv2.dilate((a > 0).astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
    under = layers['underlay_tex'].copy()
    under.putalpha(Image.fromarray(sil))
    base = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    base.alpha_composite(under, (0, 0))
    base.alpha_composite(canvas, (0, 0))
    canvas = base
    rdx = spec.get('root_dx', 0); rdy = spec.get('root_dy', 0)
    if rdx or rdy:
        shifted = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        shifted.alpha_composite(canvas, (int(rdx), int(rdy)))
        canvas = shifted
    return canvas

if __name__ == '__main__':
    fig = Image.open(f'{V1PARTS}/figure_rgba.png')
    print('figure loaded', fig.size)
    layers, piv = segment(fig)
    # test sheet: sampled frames of the loop on mid-grey (5 x 2)
    sheet_frames = [0, 5, 10, 15, 20, 26, 32, 36, 41, 45]
    sheet = Image.new('RGB', (fig.size[0] // 2 * 5, fig.size[1] // 2 * 2), (120, 130, 140))
    draws = {}
    for i, f in enumerate(sheet_frames):
        d = build_drawing(layers, piv, sample_spec(f))
        draws[f] = d
        bg = Image.new('RGBA', fig.size, (120, 130, 140, 255))
        bg.alpha_composite(d)
        small = bg.convert('RGB').resize((fig.size[0] // 2, fig.size[1] // 2), Image.LANCZOS)
        sheet.paste(small, ((i % 5) * fig.size[0] // 2, (i // 5) * fig.size[1] // 2))
    sheet.save(f'{ROOT}/parts/dance_test_sheet.png')
    # ACCEPTANCE ZOOMS (owner defect list): shoulders/cape at the step and
    # twist poses, cape between the legs, legs/feet at step + hop + landing
    def zoom(f, box, out, size=(880, 880)):
        d = draws.get(f) or build_drawing(layers, piv, sample_spec(f))
        bg = Image.new('RGBA', fig.size, (110, 190, 245, 255)); bg.alpha_composite(d)
        bg.convert('RGB').crop(box).resize(size).save(f'{ROOT}/parts/{out}')
    zoom(5, (150, 40, 590, 480), 'zoom_step_r.png')
    zoom(26, (610, 40, 1050, 480), 'zoom_twist_l.png')
    zoom(5, (330, 430, 870, 830), 'zoom_cape_legs.png', (810, 600))
    zoom(5, (330, 700, 870, 1111), 'zoom_feet_step.png', (880, 670))
    zoom(32, (330, 700, 870, 1111), 'zoom_feet_hop.png', (880, 670))
    zoom(36, (330, 700, 870, 1111), 'zoom_feet_land.png', (880, 670))
    print('test sheet + acceptance zooms saved')
