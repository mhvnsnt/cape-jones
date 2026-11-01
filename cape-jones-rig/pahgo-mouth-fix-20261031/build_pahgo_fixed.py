"""Wired pulled-mouth lip-sync builder, front-only, tight mouth-only cut.
Mars orders, 2026-10-31 20:30 + 20:32 CDT:
- Whose mouth? Robin, Teen Titans. Batman 0, Superman 0 in complete-v1.
- Placement: LEFT, DOWN, scale 0.75x vs the old fitted placement.
- Tight cut: mouth alone (lips / teeth / tongue / opening). No Robin cheek,
  chin, nose, jaw outline, costume, or crease pattern carried over, unless a
  corner wrinkle is labelled NECESSARY for talking. In this set: 0 corner
  wrinkles kept -- Cape's own cheek lines are already in the clean head base,
  and every dropped fragment was a jaw/cheek outline, not a talking wrinkle.
- Angle: front-facing only for the front Cape head. 3/4 mouths are rejected
  for this set, not silently shipped. See ANGLE-AUDIT in the report.

Industry-standard placement methods, run vs mapping:
  RUN (in this file): (1) Harmony-style mouth-chart drawing substitution --
  one mouth layer swapped per frame, head underneath carries no mouth that
  can show through; (2) facial-landmark anchor -- a SINGLE target point for
  every viseme, so the mouth does not jump frame to frame (old set jumped
  17.5px in x between MBP 250.6 and GK 268.1); (3) alpha-bbox centre anchor
  -- the visible mouth's bbox centre lands on the target, NOT the transparent
  patch image centre (old method centred the patch box, which is why the
  thin MBP line sat ~15px high and GK sat right); (4) head-width proportional
  scale -- new scale = old fitted scale x 0.75, same factor every viseme.
  MAPPING (not run, no model on this VM): MediaPipe Face Mesh mouth ROI
  (landmarks 0-17 / 61-68 lip contour) -- the tight crop below is the
  manual equivalent of that ROI: lip contour bbox, nothing outside it.
  Rhubarb Lip Sync phoneme-to-viseme timing -- PAH GO timing here is a
  fixed 6 frames per viseme at 24fps, not audio-driven; audio-driven timing
  is still owed (recorded audio 0%).

Placement numbers (476x688 clean head, old zone [111,409,392,560]):
  OLD zone centre (251.5, 484.5). Mars shift: LEFT -20px, DOWN +20px.
  The -20/+20 is MY interpretation of Mars's "a little more" -- Mars gave
  direction + 0.75x scale, not pixel offsets, and that is stated plainly.
  NEW target alpha-bbox centre, every viseme: (231.5, 504.5).
  Scale: new = old fitted scale x 0.75.
  Old per-viseme alpha centres (measured, patch-box method):
    01 AH 3/4 (252.3, 483.6) size 279.0x133.9 -- REJECTED, angle
    02 MBP 3/4 (250.6, 469.3) size 281.0x20.5 -- REJECTED, angle
    05 GK front (268.1, 484.2) size 247.0x42.8 -- KEPT, re-cut tight
  New per-viseme alpha centres (all): (231.5, 504.5), sizes in JSON.
"""
from PIL import Image
import numpy as np, os, json
from scipy import ndimage

RIG = '/home/hatch/workspace/cape-jones-rig'
OUT = f'{RIG}/pahgo-mouth-fix-20261031'
OLD = f'{RIG}/superhero-mouths-20261031'
BASE = Image.open(f'{RIG}/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')

TARGET = (231.5, 504.5)   # zone centre (251.5,484.5) + (-20,+20)
SCALE_FACTOR = 0.75

def alpha_bbox(im):
    a = np.array(im.convert('RGBA'))
    ys, xs = np.where(a[:, :, 3] > 0)
    if len(xs) == 0:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(len(xs)))

def save_patch(im, name):
    p = f'{OUT}/mouths-tight/{name}'
    im.save(p)
    return p, alpha_bbox(im)

def tight_03():
    """AH-front: old 03 open-smile patch, tight cut.
    Drop top 8 rows (thin cheek/jaw line above the mouth) and x>270
    (thin vertical jaw-outline fragments at the right edge). Keep black
    mouth cavity + brown tongue, which ARE the mouth opening."""
    p = Image.open(f'{OLD}/mouths/03_open-smile-eh_patch.png').convert('RGBA')
    a = np.array(p)
    keep = np.zeros(a.shape[:2], bool)
    keep[8:, :271] = a[8:, :271, 3] > 0
    out = np.zeros_like(a); out[keep] = a[keep]
    return Image.fromarray(out), 0.949  # old fitted scale for 03

def tight_05():
    """GK-front: old 05 grit patch, tight cut.
    Drop rows y>=69 (thin chin/jaw curve below the teeth band; teeth
    white rows end ~65, chin curve is 70-80, 342 alpha px dropped).
    Keep white teeth band + black lip outline, which ARE the mouth."""
    p = Image.open(f'{OLD}/mouths/05_grit-teeth_patch.png').convert('RGBA')
    a = np.array(p)
    keep = np.zeros(a.shape[:2], bool)
    keep[:69, :] = a[:69, :, 3] > 0
    out = np.zeros_like(a); out[keep] = a[keep]
    return Image.fromarray(out), 0.529  # old fitted scale for 05

def front_mbp_09():
    """MBP-front: NEW extraction, model-sheet front 09_RBN01_CAMS_DCTTAS.
    Front: both eyes symmetric, both ears visible, mouth symmetric.
    Tight cut: dark line pixels only, box (205,688,290,697) in the render,
    i.e. the horizontal mouth line itself, no skin, no chin, no jaw outline
    diagonal (that diagonal is y>=697 / x>270 and is excluded)."""
    src = Image.open(f'{RIG}/robin-eyes-100-20261031/render/09_RBN01_CAMS_DCTTAS.png').convert('RGBA')
    box = (205, 688, 290, 697)
    crop = src.crop((box[0], box[1], box[2] + 1, box[3] + 1))
    a = np.array(crop)
    dark = (a[:, :, 3] > 100) & (a[:, :, 0] < 80) & (a[:, :, 1] < 80) & (a[:, :, 2] < 80)
    out = np.zeros_like(a); out[dark] = a[dark]
    # keep only the horizontal line component cluster: rows 688-696 in
    # render coords = rows 0-8 here; the diagonal jaw outline enters at
    # the right edge below row 6, so drop dark pixels with x>60 and y>6
    # (those are jaw outline, not mouth line) -- measured, not guessed.
    out2 = np.zeros_like(out)
    for y in range(out.shape[0]):
        for x in range(out.shape[1]):
            if dark[y, x] and not (x > 60 and y > 6):
                out2[y, x] = out[y, x]
    return Image.fromarray(out2), None  # scale set by target width below

def place_mouth(patch, old_scale):
    """Scale then paste so the VISIBLE (alpha) bbox centre = TARGET.
    Returns (head image, measurements dict)."""
    if old_scale is None:
        # MBP-front: target width = old MBP fitted width 281 x 0.75 = 210.8
        sc = 210.8 / patch.width
    else:
        sc = old_scale * SCALE_FACTOR
    nw = max(1, int(round(patch.width * sc)))
    nh = max(1, int(round(patch.height * sc)))
    resized = patch.resize((nw, nh), Image.LANCZOS)
    bb = alpha_bbox(resized)
    head = BASE.copy()
    if bb:
        cx = (bb[0] + bb[2]) / 2; cy = (bb[1] + bb[3]) / 2
        head.alpha_composite(resized, (int(round(TARGET[0] - cx)), int(round(TARGET[1] - cy))))
    else:
        head.alpha_composite(resized, (0, 0))
    meas = dict(scale=round(sc, 4), resized=[nw, nh],
                alpha_bbox=bb, alpha_px=bb[4] if bb else 0,
                alpha_size=[round(bb[2] - bb[0] + 1, 1), round(bb[3] - bb[1] + 1, 1)] if bb else None,
                target=list(TARGET))
    return head, meas

CHART = [  # PAH GO, front-only, OH = GAP (no front round OH exists)
    ('MBP', 'mbp-front-09', front_mbp_09),
    ('AH', 'ah-front-03', tight_03),
    ('GK', 'gk-front-05', tight_05),
    ('OH', 'gap', None),
]

def main():
    results = []
    frames = []
    for viseme, key, fn in CHART:
        if fn is None:
            head = BASE.copy()
            results.append(dict(viseme=viseme, key=key, source='GAP: clean head, no mouth patch',
                                angle='n/a', note='No front round OH/OO mouth exists in the Robin set; EH (03) was NOT duplicated to paper over it.'))
            frames.append(head)
            continue
        patch, old_scale = fn()
        path, bb_old = save_patch(patch, f'{key}_tight_patch.png')
        head, meas = place_mouth(patch, old_scale)
        head.save(f'{OUT}/fitted-tight/{key}_on_cape_head.png')
        src = {'mbp-front-09': '09_RBN01_CAMS_DCTTAS.png (model sheet, FRONT)',
               'ah-front-03': '53_RBEXPRES03_CA_DCTTAS.png via old 03 patch, re-cut tight (FRONT/near-front)',
               'gk-front-05': '49_RBEXPRES05_CA_DCTTAS.png via old 05 patch, re-cut tight (FRONT)'}[key]
        results.append(dict(viseme=viseme, key=key, source=src, angle='front',
                            tight_patch=path, tight_alpha_bbox=bb_old, **meas))
        frames.append(head)
        print(viseme, key, meas, flush=True)
    # 24 frames @24fps, 6 per viseme, 1.0s -- matches the original report's
    # intended timeline. Note: the old GIF file on disk is actually 4 frames
    # at 250ms, not 24 frames; the fixed GIF uses the intended 24-frame count.
    gif_frames = []
    for f in frames:
        gif_frames.extend([f] * 6)
    gif_frames[0].save(f'{OUT}/pahgo-fixed-20261031.gif', save_all=True,
                       append_images=gif_frames[1:], duration=42, loop=0)
    for i, f in enumerate(gif_frames):
        f.save(f'{OUT}/frames/pahgo-fixed-f{i:02d}-20261031.png')
    json.dump(results, open(f'{OUT}/pahgo-fixed-measurements-20261031.json', 'w'), indent=1)
    print('DONE', len(frames), 'visemes,', len(gif_frames), 'gif frames')

if __name__ == '__main__':
    main()
