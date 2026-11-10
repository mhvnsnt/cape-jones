"""Charlie v3.1 nudge — Mars 2026-11-01 20:25 CST, reacting to v3 video.
Screen moves as Mars sees them (1920x1080 video):
  front arm (right side) LEFT 20 px, head RIGHT 40 px, back arm (left side) RIGHT 10 px.
Builder scales 984-wide assembly layers by CH_SCALE=640/1221 (~0.5242), so assembly
shifts are round(req/CH_SCALE): front -38, head +76, back +19 assembly px
=> screen 19.92 / 39.84 / 9.96 px. Whole-layer moves only, no cut/redraw/recolor.
Rotation pivots shifted by the same screen amounts so nod/wave rotate about the
new shoulder/neck points. Thingies stay omitted. All other layers unchanged.
Base: charlie-piece-placement-fix-20261101 (v3), read only, untouched.
"""
import os, math, shutil, json
from PIL import Image, ImageDraw
BASE = os.path.expanduser('~/workspace/cape-jones-rig')
V3 = os.path.join(BASE, 'charlie-piece-placement-fix-20261101')
OUT = '/var/tmp/charlie-v31-20261101'
os.makedirs(OUT, exist_ok=True)
FR = os.path.join(OUT, 'frames'); os.makedirs(FR, exist_ok=True)
LDIR = os.path.join(OUT, 'layers_v3_1'); os.makedirs(LDIR, exist_ok=True)
SHIFTS = {'back_arm': 19, 'legs': 0, 'body_back': 0, 'head': 76, 'body': 0, 'front_arm': -38}
order = ['back_arm', 'legs', 'body_back', 'head', 'body', 'front_arm']
v3_asm = json.load(open(os.path.join(V3, 'assembly_v3.json')))
new_layers, new_offsets = {}, {}
for fn in order:
    im = Image.open(os.path.join(V3, 'layers_v3', fn + '.png')).convert('RGBA')
    dx = SHIFTS[fn]
    canvas = Image.new('RGBA', im.size, (0, 0, 0, 0))
    canvas.paste(im, (dx, 0), im)
    canvas.save(os.path.join(LDIR, fn + '.png'))
    bb = canvas.getbbox()
    new_layers[fn] = {'bbox': list(bb)}
    old = v3_asm['offsets'][fn]
    new_offsets[fn] = [old[0] + dx, old[1]]
    print(fn, 'shift', dx, 'old bbox', v3_asm['layers'][fn]['bbox'], 'new bbox', list(bb), flush=True)
xs = [v['bbox'][0] for v in new_layers.values()]; ys = [v['bbox'][1] for v in new_layers.values()]
xe = [v['bbox'][2] for v in new_layers.values()]; ye = [v['bbox'][3] for v in new_layers.values()]
assembled = [min(xs), min(ys), max(xe), max(ye)]
print('assembled old', v3_asm['assembled_bbox'], 'new', assembled, flush=True)
json.dump({'offsets': new_offsets, 'order': order, 'layers': new_layers,
           'assembled_bbox': assembled,
           'screen_moves': {'front_arm': -20, 'head': 40, 'back_arm': 10},
           'assembly_shifts': SHIFTS,
           'thingies': v3_asm['thingies']},
          open(os.path.join(OUT, 'assembly_v3_1.json'), 'w'), indent=2)
W, H = 1920, 1080; GROUND = 950; N = 96
layers = {}
for fn in order:
    layers[fn] = Image.open(os.path.join(LDIR, fn + '.png')).convert('RGBA')
CH_SCALE = 640 / 1221
def scale_layer(im):
    return im.resize((int(im.width * CH_SCALE), int(im.height * CH_SCALE)), Image.LANCZOS)
scaled = {k: scale_layer(v) for k, v in layers.items()}
CW = int(984 * CH_SCALE); CH = int(1735 * CH_SCALE)
HEAD_PIV = (int(506 * CH_SCALE) + 40, int(1011 * CH_SCALE))
ARM_PIV = (int(860 * CH_SCALE) - 20, int(887 * CH_SCALE))
print('CW/CH', CW, CH, 'HEAD_PIV', HEAD_PIV, 'ARM_PIV', ARM_PIV, flush=True)
cj = Image.open(os.path.join(BASE, 'rig-apose-v7c-clean-transparent.png')).convert('RGBA')
cj_bb = cj.getbbox(); cj_h = cj_bb[3] - cj_bb[1]; CJ_SCALE = 720 / cj_h
cj_s = cj.resize((int(cj.width * CJ_SCALE), int(cj.height * CJ_SCALE)), Image.LANCZOS); cj_bb2 = cj_s.getbbox()
def lerp(a, b, t): return a + (b - a) * t
def ease(t): return t * t * (3 - 2 * t)
def frame_params(f):
    if f < 24:
        t = ease(f / 23); return lerp(-400, 430, t), abs(math.sin(f * 0.9)) * 6, 0, 0, 0, abs(math.sin(f * 0.5)) * 3
    if f < 48:
        t = (f - 24) / 23; return 430, math.sin(t * math.pi) * 4, math.sin(t * math.pi) * 2, -6 * ease(t), -35 * ease(t), 3
    if f < 72:
        t = (f - 48) / 23; wave = math.sin(t * math.pi * 2) * 20
        return 430, 3 + math.sin(t * math.pi * 2) * 3, 2 * math.sin(t * math.pi * 2), -6 + 5 * math.sin(t * math.pi * 2), -25 + wave, 4 + abs(math.sin(t * math.pi * 2)) * 5
    t = (f - 72) / 23; return 430, 2 * (1 - t), 0, -6 * (1 - t), -25 * (1 - t), 3 * (1 - t)
BG = Image.new('RGB', (W, H), (216, 216, 210)); _dr = ImageDraw.Draw(BG)
for _y in range(H):
    _g = int(216 - (_y / H) * 18); _dr.line([(0, _y), (W, _y)], fill=(_g, _g, _g - 6))
_dr.rectangle([0, GROUND, W, H], fill=(150, 140, 125)); _dr.line([(0, GROUND), (W, GROUND)], fill=(60, 50, 40), width=3)
def compose(f):
    cj_x, cj_bob, cj_rot, ch_head, ch_arm, ch_bob = frame_params(f)
    img = BG.copy()
    ch_left = 1380 - CW // 2; ch_top = int(GROUND - int(1696 * CH_SCALE) + ch_bob)
    for fn in order:
        lay = scaled[fn]
        if fn == 'head' and ch_head != 0: lay = lay.rotate(-ch_head, resample=Image.BICUBIC, center=HEAD_PIV)
        if fn == 'front_arm' and ch_arm != 0: lay = lay.rotate(-ch_arm, resample=Image.BICUBIC, center=ARM_PIV)
        img.paste(lay, (ch_left, ch_top), lay)
    cj_img = cj_s
    if cj_rot != 0: cj_img = cj_s.rotate(-cj_rot, resample=Image.BICUBIC, center=(cj_s.width // 2, int(cj_bb2[3])))
    img.paste(cj_img, (int(cj_x), int(GROUND - cj_bb2[3] + cj_bob)), cj_img)
    dr = ImageDraw.Draw(img); dr.rectangle([0, 0, W, 36], fill=(0, 0, 0))
    dr.text((12, 8), 'TEST ONLY - CHARLIE = ACTUAL DONOR CHARACTER PLACEHOLDER - DO NOT SHIP AS-IS - RESKIN PENDING - PIECE PLACEMENT FIX v3.1', fill=(255, 220, 80))
    dr.text((12, H - 30), 'Cape Jones (own rig, left) + Charlie (own separate XFL layer rig, v3.1 nudge, right) - no dialogue, no donor audio, thingies masked out', fill=(40, 40, 40))
    return img
for f in range(N):
    compose(f).save(os.path.join(FR, f'frame_{f+1:03d}.png'))
print('frames done', N, flush=True)
sel = [1, 24, 36, 60, 72, 96]
sheet = Image.new('RGB', (1920, 1080), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
for i, fn in enumerate(sel):
    im = Image.open(os.path.join(FR, f'frame_{fn:03d}.png')).resize((640, 360)); x = (i % 3) * 640; y = (i // 3) * 540
    sheet.paste(im, (x, y)); dr.text((x + 10, y + 10), f'frame {fn}', fill=(255, 255, 0))
sheet.save(os.path.join(OUT, 'contact-sheet-charlie-interaction-v3-1-20261101.png'))
shutil.copy(os.path.join(FR, 'frame_060.png'), os.path.join(OUT, 'frame60-v3-1-20261101.png'))
shutil.copy(os.path.join(V3, 'interaction-sfx-v3-20261101.wav'), os.path.join(OUT, 'interaction-sfx-v3-1-20261101.wav'))
print('contact + frame60 + sfx done', flush=True)
