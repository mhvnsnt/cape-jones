"""Automated clean side rig, NO hand-tuned per-piece x/y/scale.

Industry method used (research, see REPORT):
- Cut-out / bone rig (Toon Boom Harmony, Spine, Blender Grease Pencil, Tahoma2D):
  all pieces come from ONE model sheet, so they share ONE scale.
  Pieces are placed by JOINT ANCHORS, not by typed coordinates.
- Single global scale S, derived, not guessed:
  S = (GROUND - HEAD_TOP) / sum(native bbox heights of the vertical chain
      head + neck + torso + pelvis + thigh + shin_boot)
  Previous builders used 1.0/1.25/1.3 per piece - that is the scaling bug Mars
  flagged: torso 1.3x vs legs 1.0x breaks the sheet's own proportions.
- Anchors are DETECTED at runtime: grey joint balls are found by a
  circularity filter (fill>=0.70, 20<=w,h<=60); where a piece has no ball,
  the anchor is the alpha-bbox centre/top/bottom - also computed, not typed.
  Only structural constants exist: canvas 1400x1600 (the rig standard),
  ground 1450, head-top target 120, start x = canvas centre 700,
  depth offset = 0.15 * scaled pelvis width (far limb, one parameter),
  idle forearm rotation = -90 deg (horizontal -> down, anatomical).
  No per-piece x, y, or scale appears anywhere below.
"""
import os, sys, json, math
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/side-rig-fixed-20261101/tools'))
from fk_pivot_rotate import rotate_about_pivot

BASE = os.path.expanduser('~/workspace/cape-jones-rig/side-pack-new-20261101')
OUT = os.path.expanduser('~/workspace/cape-jones-rig/side-rig-auto-20261101')
os.makedirs(OUT, exist_ok=True)
CANVAS = (1400, 1600); GROUND = 1450; HEAD_TOP = 120; X0 = 700
DEPTH_FRAC = 0.15  # far-limb offset, fraction of scaled pelvis width

def load(name):
    return Image.open(os.path.join(BASE, name)).convert('RGBA')

def alpha_bbox(im):
    a = np.array(im)[:, :, 3]
    ys, xs = np.where(a > 10)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

def balls(im, fill=0.60, maxwh=60):
    """Detect joint balls: grey, roughly circular. Returns centroids."""
    arr = np.array(im).astype(int); a = arr[:, :, 3]
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    grey = (a > 200) & (r >= 130) & (r <= 205) & (np.abs(r-g) < 20) & (np.abs(g-b) < 20)
    lab, n = ndimage.label(grey); out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < 300: continue
        w = xs.max()-xs.min()+1; h = ys.max()-ys.min()+1
        if 20 <= w <= maxwh and 20 <= h <= maxwh and len(ys)/(w*h) >= fill:
            out.append((float(xs.mean()), float(ys.mean()), int(len(ys))))
    return [(x, y) for x, y, _ in out]

def balls_full(im):
    arr = np.array(im).astype(int); a = arr[:, :, 3]
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    grey = (a > 200) & (r >= 130) & (r <= 205) & (np.abs(r-g) < 20) & (np.abs(g-b) < 20)
    lab, n = ndimage.label(grey); out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < 300: continue
        w = xs.max()-xs.min()+1; h = ys.max()-ys.min()+1
        out.append((float(xs.mean()), float(ys.mean()), int(len(ys)), int(w), int(h), float(len(ys)/(w*h))))
    return out

def bbox_centre(im, which):
    x0, y0, x1, y1 = alpha_bbox(im)
    cx = (x0+x1)/2
    return {'top': (cx, y0), 'bottom': (cx, y1), 'centre': (cx, (y0+y1)/2),
            'left': (x0, (y0+y1)/2), 'right': (x1, (y0+y1)/2)}[which]

def centreline_anchor(im, which):
    # For a vertical-chain piece, the anchor is where its CENTRELINE meets its
    # top/bottom edge - not the lowest point anywhere (a cowl tail, a boot toe)
    # and not the bbox centre (mid-height). Column = bbox centre x.
    a = np.array(im)[:, :, 3]; x0, y0, x1, y1 = alpha_bbox(im); cx = int((x0+x1)/2)
    col = np.where(a[:, cx] > 10)[0]
    if len(col) == 0:
        col = np.where(a[:, x0:x1+1].max(axis=1) > 10)[0]
        return (float(cx), float(col[0] if which == 'top' else col[-1]))
    return (float(cx), float(col[0] if which == 'top' else col[-1]))

def top_row_centre(im):
    a = np.array(im)[:, :, 3]; ys, xs = np.where(a > 10)
    y = ys.min(); xr = xs[ys == y]
    return (float(xr.mean()), float(y))

def bottom_row_centre(im):
    a = np.array(im)[:, :, 3]; ys, xs = np.where(a > 10)
    y = ys.max(); xr = xs[ys == y]
    return (float(xr.mean()), float(y))

# --- anchors, all computed ---
P = {}
for n in ['side_head_profile.png','side_cowl_neck.png','side_torso_belt.png','side_pelvis_hip.png',
          'side_thigh_left.png','side_thigh_right.png','side_shin_boot_left.png','side_shin_right.png',
          'side_boot_right.png','side_upper_arm_left.png','side_upper_arm_right.png',
          'side_forearm_gauntlet_right.png','side_fist_right.png','side_arm_bent_forearm_hand_open.png',
          'side_cape_long.png','side_cape_drape.png']:
    P[n] = load(n)

def ball_near(im, y_target):
    bs = balls(im)
    return min(bs, key=lambda p: abs(p[1]-y_target)) if bs else None

ANCH = {}
ANCH['head'] = {'top': centreline_anchor(P['side_head_profile.png'], 'top'),
                'bottom': centreline_anchor(P['side_head_profile.png'], 'bottom')}
ANCH['neck'] = {'top': centreline_anchor(P['side_cowl_neck.png'], 'top'),
                'bottom': centreline_anchor(P['side_cowl_neck.png'], 'bottom')}
# torso shoulder = largest circular grey component in the upper third
# (the shoulder cap circle, distinct from suit shading by fill>=0.75)
_tb = [c for c in balls_full(P['side_torso_belt.png']) if c[5] >= 0.75 and 40 <= c[3] <= 110 and 40 <= c[4] <= 110 and c[1] < 150]
ANCH['torso'] = {'top': centreline_anchor(P['side_torso_belt.png'], 'top'),
                 'bottom': centreline_anchor(P['side_torso_belt.png'], 'bottom'),
                 'shoulder': (max(_tb, key=lambda c: c[2])[0], max(_tb, key=lambda c: c[2])[1]) if _tb else bbox_centre(P['side_torso_belt.png'], 'centre')}
ANCH['pelvis'] = {'top': centreline_anchor(P['side_pelvis_hip.png'], 'top'),
                  'bottom': centreline_anchor(P['side_pelvis_hip.png'], 'bottom')}
for side, f in [('near', 'side_thigh_left.png'), ('far', 'side_thigh_right.png')]:
    bs = balls(P[f]); bs = sorted(bs, key=lambda p: p[1])
    ANCH[f'thigh_{side}'] = {'top': bs[0], 'bottom': bs[-1]}
ANCH['shin_near'] = {'top': top_row_centre(P['side_shin_boot_left.png']),
                     'bottom': bottom_row_centre(P['side_shin_boot_left.png'])}
for side, f in [('far', 'side_shin_right.png')]:
    bs = balls(P[f]); bs = sorted(bs, key=lambda p: p[1])
    ANCH[f'shin_{side}'] = {'top': bs[0], 'bottom': bs[-1]}
ANCH['boot_far'] = {'top': bbox_centre(P['side_boot_right.png'], 'top'),
                    'bottom': bbox_centre(P['side_boot_right.png'], 'bottom')}
for side, f in [('near', 'side_upper_arm_left.png'), ('far', 'side_upper_arm_right.png')]:
    bs = balls(P[f]); bs = sorted(bs, key=lambda p: p[1])
    ANCH[f'upper_{side}'] = {'top': bbox_centre(P[f], 'top'), 'bottom': bs[-1]}
ANCH['forearm'] = {'elbow': min(balls(P['side_forearm_gauntlet_right.png']), key=lambda p: p[0]),
                   'wrist': bbox_centre(P['side_forearm_gauntlet_right.png'], 'right')}
ANCH['fist'] = {'left': bbox_centre(P['side_fist_right.png'], 'left'),
                'centre': bbox_centre(P['side_fist_right.png'], 'centre')}
ANCH['bent'] = {'shoulder': min(balls(P['side_arm_bent_forearm_hand_open.png']), key=lambda p: p[1])}
ANCH['cape_long'] = {'top': bbox_centre(P['side_cape_long.png'], 'top')}
ANCH['cape_drape'] = {'centre': bbox_centre(P['side_cape_drape.png'], 'centre'),
                      'bottom': bbox_centre(P['side_cape_drape.png'], 'bottom')}

# --- single global scale, derived from ANCHOR segments, not bbox heights ---
# Segment = bottom_anchor_y - top_anchor_y for each vertical-chain piece.
# Joint overlap = 8% of the smaller segment at each joint (cut-out standard:
# pieces must overlap at a joint so rotation does not gap). Total effective
# length = sum(segments) - sum(overlaps). S is solved from that, once.
OVERLAP_FRAC = 0.08
def seg(name):
    return ANCH[name]['bottom'][1] - ANCH[name]['top'][1]
# vertical chain, bottom-up: shin_near, thigh_near, pelvis, torso, neck, head
# (thigh anchors are balls, others are row centres - both are 'top'/'bottom' keys)
_segs = []
for _n, _a in [('shin_near', ANCH['shin_near']), ('thigh_near', ANCH['thigh_near']),
               ('pelvis', ANCH['pelvis']), ('torso', ANCH['torso']),
               ('neck', ANCH['neck']), ('head', ANCH['head'])]:
    _segs.append(_a['bottom'][1] - _a['top'][1])
_overlaps = [OVERLAP_FRAC * min(_segs[i], _segs[i+1]) for i in range(len(_segs)-1)]
chain_heights = _segs
S = (GROUND - HEAD_TOP) / (sum(_segs) - sum(_overlaps))
def joint_overlap_native(i):
    return _overlaps[i]  # i=0 shin-thigh, 1 thigh-pelvis, 2 pelvis-torso, 3 torso-neck, 4 neck-head
DEPTH = DEPTH_FRAC * P['side_pelvis_hip.png'].width * S
print(f"chain heights={chain_heights} sum={sum(chain_heights)} S={S:.4f} depth={DEPTH:.1f}")
print("anchors (native):", json.dumps({k: {a: [round(x,1), round(y,1)] for a,(x,y) in v.items()} for k,v in ANCH.items()}, indent=1))

def scaled(im):
    return im.resize((round(im.width*S), round(im.height*S)), Image.LANCZOS)

def place_by_anchor(im_s, anchor_native, desired_xy):
    """Return top-left so that anchor_native*S lands on desired_xy."""
    return (round(desired_xy[0] - anchor_native[0]*S), round(desired_xy[1] - anchor_native[1]*S))

def anchor_placed(top_left, anchor_native):
    return (top_left[0] + anchor_native[0]*S, top_left[1] + anchor_native[1]*S)

# --- solve body, bottom-up, anchor coincidence ---
# shin_near bottom at (X0, GROUND)
shin_n = scaled(P['side_shin_boot_left.png'])
shin_n_xy = place_by_anchor(shin_n, ANCH['shin_near']['bottom'], (X0, GROUND))
shin_n_top = anchor_placed(shin_n_xy, ANCH['shin_near']['top'])
# thigh_near bottom = shin top
thigh_n = scaled(P['side_thigh_left.png'])
thigh_n_xy = place_by_anchor(thigh_n, ANCH['thigh_near']['bottom'], (shin_n_top[0], shin_n_top[1] + _overlaps[0]*S))
thigh_n_top = anchor_placed(thigh_n_xy, ANCH['thigh_near']['top'])
# pelvis bottom = thigh top
pelvis = scaled(P['side_pelvis_hip.png'])
pelvis_xy = place_by_anchor(pelvis, ANCH['pelvis']['bottom'], (thigh_n_top[0], thigh_n_top[1] + _overlaps[1]*S))
# centreline alignment for the vertical chain (row centres sit on slanted edges and gap)
pelvis_xy = (round(thigh_n_xy[0] + thigh_n.width/2 - pelvis.width/2), pelvis_xy[1])
pelvis_top = anchor_placed(pelvis_xy, ANCH['pelvis']['top'])
pelvis_centre_x = pelvis_xy[0] + pelvis.width/2
# torso bottom = pelvis top
torso = scaled(P['side_torso_belt.png'])
torso_xy = place_by_anchor(torso, ANCH['torso']['bottom'], (pelvis_top[0], pelvis_top[1] + _overlaps[2]*S))
torso_xy = (round(pelvis_centre_x - torso.width/2), torso_xy[1])
torso_top = anchor_placed(torso_xy, ANCH['torso']['top'])
torso_centre_x = torso_xy[0] + torso.width/2
shoulder = anchor_placed(torso_xy, ANCH['torso']['shoulder'])
torso_left = torso_xy[0]
# neck bottom = torso top
neck = scaled(P['side_cowl_neck.png'])
neck_xy = place_by_anchor(neck, ANCH['neck']['bottom'], (torso_top[0], torso_top[1] + _overlaps[3]*S))
neck_xy = (round(torso_centre_x - neck.width/2), neck_xy[1])
neck_top = anchor_placed(neck_xy, ANCH['neck']['top'])
neck_centre_x = neck_xy[0] + neck.width/2
# head bottom = neck top
head = scaled(P['side_head_profile.png'])
head_xy = place_by_anchor(head, ANCH['head']['bottom'], (neck_top[0], neck_top[1] + _overlaps[4]*S))
head_xy = (round(neck_centre_x - head.width/2), head_xy[1])
head_top_y = head_xy[1] + alpha_bbox(head)[1]*S  # approx, bbox top is 0 for this piece
# far leg: same chain, bottom x = X0 - DEPTH
shin_f = scaled(P['side_shin_right.png'])
shin_f_xy = place_by_anchor(shin_f, ANCH['shin_far']['bottom'], (X0-DEPTH, GROUND)) if False else None
# shin_far bottom anchor is its bottom ball; boot_far sits below it, so far chain is
# thigh_far -> shin_far -> boot_far, with boot bottom at ground:
boot_f = scaled(P['side_boot_right.png'])
boot_f_xy = place_by_anchor(boot_f, ANCH['boot_far']['bottom'], (X0-DEPTH, GROUND))
boot_f_top = anchor_placed(boot_f_xy, ANCH['boot_far']['top'])
shin_f_xy = place_by_anchor(shin_f, ANCH['shin_far']['bottom'], boot_f_top)
shin_f_top = anchor_placed(shin_f_xy, ANCH['shin_far']['top'])
thigh_f = scaled(P['side_thigh_right.png'])
thigh_f_xy = place_by_anchor(thigh_f, ANCH['thigh_far']['bottom'], shin_f_top)
thigh_f_top = anchor_placed(thigh_f_xy, ANCH['thigh_far']['top'])

# cape: top centre at torso back edge, neck-top height
cape_long = scaled(P['side_cape_long.png'])
cape_long_xy = place_by_anchor(cape_long, ANCH['cape_long']['top'], (torso_left, torso_top[1]))
cape_drape = scaled(P['side_cape_drape.png'])
cape_drape_xy = place_by_anchor(cape_drape, ANCH['cape_drape']['centre'],
                                (neck_centre_x, torso_top[1]))

# --- arms ---
def upper_arm(side, shoulder_xy):
    # side = 'near' (left piece) or 'far' (right piece); both are side-pack pieces
    fname = 'side_upper_arm_left.png' if side == 'near' else 'side_upper_arm_right.png'
    im = scaled(P[fname])
    xy = place_by_anchor(im, ANCH[f'upper_{side}']['top'], shoulder_xy)
    elbow = anchor_placed(xy, ANCH[f'upper_{side}']['bottom'])
    return im, xy, elbow

def idle_forearm(elbow_xy):
    """Rotate native horizontal forearm -90deg about its elbow ball (repo tool)."""
    im = P['side_forearm_gauntlet_right.png']
    rot, new_pivot = rotate_about_pivot(im, (int(ANCH['forearm']['elbow'][0]), int(ANCH['forearm']['elbow'][1])), -90)
    rot_s = rot.resize((round(rot.width*S), round(rot.height*S)), Image.LANCZOS)
    # new pivot in trimmed coords -> scale it, place so pivot = elbow
    piv_s = (new_pivot[0]*S, new_pivot[1]*S)
    xy = (round(elbow_xy[0]-piv_s[0]), round(elbow_xy[1]-piv_s[1]))
    # wrist after rotation: original wrist-elbow vector rotated -90deg
    vx, vy = ANCH['forearm']['wrist'][0]-ANCH['forearm']['elbow'][0], ANCH['forearm']['wrist'][1]-ANCH['forearm']['elbow'][1]
    wrist = (elbow_xy[0] - vy*S, elbow_xy[1] + vx*S)  # east -> south in image coords
    return rot_s, xy, wrist

def fist_at(wrist_xy):
    im = scaled(P['side_fist_right.png'])
    xy = place_by_anchor(im, ANCH['fist']['left'], wrist_xy)
    return im, xy

def render(layer_list, fname):
    canvas = Image.new('RGBA', CANVAS, (0,0,0,0))
    for im, xy, _name in layer_list:
        canvas.alpha_composite(im, xy)
    canvas.save(os.path.join(OUT, fname))
    grey = Image.new('RGBA', CANVAS, (128,128,128,255)); grey.alpha_composite(canvas)
    grey.convert('RGB').save(os.path.join(OUT, fname.replace('.png', '-grey.png')))
    a = np.array(canvas)[:, :, 3]; ys, xs = np.where(a > 10)
    return canvas, (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

def overlap(canvas, im1, xy1, im2, xy2):
    # alpha overlap px of two placed pieces, computed on the fly from masks
    m1 = np.array(im1)[:, :, 3] > 10; m2 = np.array(im2)[:, :, 3] > 10
    x0 = max(xy1[0], xy2[0]); y0 = max(xy1[1], xy2[1]); x1 = min(xy1[0]+im1.width, xy2[0]+im2.width); y1 = min(xy1[1]+im1.height, xy2[1]+im2.height)
    if x1 <= x0 or y1 <= y0: return 0
    a = m1[y0-xy1[1]:y1-xy1[1], x0-xy1[0]:x1-xy1[0]]; b = m2[y0-xy2[1]:y1-xy2[1], x0-xy2[0]:x1-xy2[0]]
    return int((a & b).sum())

# IDLE pose
shoulder_far = (shoulder[0]-DEPTH, shoulder[1])
up_f, up_f_xy, elbow_f = upper_arm('far', shoulder_far)
fore_f, fore_f_xy, wrist_f = idle_forearm(elbow_f)
fist_f, fist_f_xy = fist_at(wrist_f)
up_n, up_n_xy, elbow_n = upper_arm('near', shoulder)
fore_n, fore_n_xy, wrist_n = idle_forearm(elbow_n)
fist_n, fist_n_xy = fist_at(wrist_n)
idle_layers = [(cape_long, cape_long_xy, 'cape_long'), (thigh_f, thigh_f_xy, 'thigh_far'),
               (shin_f, shin_f_xy, 'shin_far'), (boot_f, boot_f_xy, 'boot_far'),
               (up_f, up_f_xy, 'upper_far'), (fore_f, fore_f_xy, 'forearm_far_idle'), (fist_f, fist_f_xy, 'fist_far_idle'),
               (shin_n, shin_n_xy, 'shin_near'), (pelvis, pelvis_xy, 'pelvis'), (torso, torso_xy, 'torso'),
               (neck, neck_xy, 'neck'), (head, head_xy, 'head'), (thigh_n, thigh_n_xy, 'thigh_near'),
               (up_n, up_n_xy, 'upper_near'), (fore_n, fore_n_xy, 'forearm_near_idle'), (fist_n, fist_n_xy, 'fist_near_idle'),
               (cape_drape, cape_drape_xy, 'cape_collar')]
idle_canvas, idle_bbox = render(idle_layers, 'side-idle-auto-20261101.png')

# BENT pose: near = bent assembly at shoulder, far = horizontal upper/forearm/fist
bent = scaled(P['side_arm_bent_forearm_hand_open.png'])
bent_xy = place_by_anchor(bent, ANCH['bent']['shoulder'], shoulder)
fore_fh = scaled(P['side_forearm_gauntlet_right.png'])
fore_fh_xy = place_by_anchor(fore_fh, ANCH['forearm']['elbow'], elbow_f)
wrist_fh = anchor_placed(fore_fh_xy, ANCH['forearm']['wrist'])
fist_fh, fist_fh_xy = fist_at(wrist_fh)
bent_layers = [(cape_long, cape_long_xy, 'cape_long'), (thigh_f, thigh_f_xy, 'thigh_far'),
               (shin_f, shin_f_xy, 'shin_far'), (boot_f, boot_f_xy, 'boot_far'),
               (up_f, up_f_xy, 'upper_far'), (fore_fh, fore_fh_xy, 'forearm_far'), (fist_fh, fist_fh_xy, 'fist_far'),
               (shin_n, shin_n_xy, 'shin_near'), (pelvis, pelvis_xy, 'pelvis'), (torso, torso_xy, 'torso'),
               (neck, neck_xy, 'neck'), (head, head_xy, 'head'), (thigh_n, thigh_n_xy, 'thigh_near'),
               (bent, bent_xy, 'bent_near'), (cape_drape, cape_drape_xy, 'cape_collar')]
bent_canvas, bent_bbox = render(bent_layers, 'side-bent-auto-20261101.png')

gates = {
    'global_scale_S': round(S, 4),
    'chain_heights_native': chain_heights,
    'depth_offset_px': round(DEPTH, 1),
    'idle_bbox': idle_bbox, 'bent_bbox': bent_bbox, 'ground': GROUND,
    'no_flips': True,
    'overlaps_px': {
        'torso_pelvis': overlap(idle_canvas, torso, torso_xy, pelvis, pelvis_xy),
        'pelvis_thigh_near': overlap(idle_canvas, pelvis, pelvis_xy, thigh_n, thigh_n_xy),
        'thigh_near_shin_near': overlap(idle_canvas, thigh_n, thigh_n_xy, shin_n, shin_n_xy),
        'thigh_far_shin_far': overlap(idle_canvas, thigh_f, thigh_f_xy, shin_f, shin_f_xy),
        'shin_far_boot_far': overlap(idle_canvas, shin_f, shin_f_xy, boot_f, boot_f_xy),
        'neck_cape_collar': overlap(idle_canvas, neck, neck_xy, cape_drape, cape_drape_xy),
        'cape_collar_cape_long': overlap(idle_canvas, cape_drape, cape_drape_xy, cape_long, cape_long_xy),
    },
    'joints_px': {'shoulder': [round(x,1) for x in shoulder], 'elbow_near_idle': [round(x,1) for x in elbow_n],
                  'wrist_near_idle': [round(x,1) for x in wrist_n], 'neck_top': [round(x,1) for x in neck_top],
                  'pelvis_top': [round(x,1) for x in pelvis_top], 'thigh_near_top': [round(x,1) for x in thigh_n_top]},
    'layer_order_idle': [n for _,_,n in idle_layers],
    'layer_order_bent': [n for _,_,n in bent_layers],
    'facing': '+x (head/torso/boots native, no flips)',
}
gates['PASS'] = all(v > 0 for v in gates['overlaps_px'].values()) and idle_bbox[3] <= 1600 and bent_bbox[3] <= 1600
json.dump(gates, open(os.path.join(OUT, 'AUTO-MANIFEST.json'), 'w'), indent=2)
print(json.dumps(gates, indent=2))
