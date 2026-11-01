"""Clean-plate plate-swap re-render CJ-01..CJ-05 — Cape Jones, 2026-10-31.
Adapted from shots-endtoend-20261031/build_shots.py, plate-swap ONLY:
 same specs (LUT/char gain/rim/bleed/effect/BG/canvas/ground), same builder
 functions, only the 5 character plates swapped to the new clean plates
 (art-owed-punch-plates-20261031/plates-clean/, v7c labels=False, 0 red).
 The old red->white debug conversion is replaced by a 0-red assert.
 No endtoend file is overwritten; outputs land in rerenders/ here.
Original header follows:
Shots end-to-end 30/30 — Cape Jones, 2026-10-31.
Layers per shot (separate, base art never recoloured on disk):
 far plane / mid plane / character (LUT gain, char only) / rim (outer 4px) /
 bleed (inner 6px band) / shadow / shafts (L3 only, L2 verified 0) /
 effects (named per shot) / foreground strip.
Canvas: 1920x1080, auto-expanded for room shots (char 1140px tall at 3.0x
 room scale cannot fit 1080 with ground line + headroom, so room finals
 are 1920x1280, ground_y=1180). No clip: every final is checked so the
 full char+glow bbox sits inside the canvas.
Sources: transparent plates (transparent-plates-sweep-20261031) — NOT the
 baked showcase/layout images, which contain the character + red debug
 dots and would double-print him. Painted BGs only where a clean painting
 exists; otherwise a colour-script multiplane (gradient + silhouette),
 labelled as such — final painted BG still owed for those shots.
"""
import json, math, os, random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

R = '/home/hatch/workspace/cape-jones-rig'
OUT = os.path.join(R, 'art-owed-punch-plates-20261031')
# plate-swap only: FIN/PRF redirected below, after the original FIN/PRF lines
FIN = os.path.join(OUT, 'rerenders/finals'); PRF = os.path.join(OUT, 'rerenders/proofs')
import pathlib; pathlib.Path(FIN).mkdir(parents=True, exist_ok=True); pathlib.Path(PRF).mkdir(parents=True, exist_ok=True)
PL = os.path.join(R, 'transparent-plates-sweep-20261031/plates')

def T(p): return os.path.join(PL, p)

SHOTS = [
 # id, slug, plate, bg_kind, bg_src, level, lut, char_gain, rim, bleed, mode, height, effect, effect_kind, note
 ('CJ-01','punch-windup', os.path.join(R, 'art-owed-punch-plates-20261031/plates-clean/CJ-01-punch-windup-clean-plate-20261031.png'), 'script','street', 'Level 2', [1.1,0.95,0.7], [1.2,0.7,1.3], (255,178,229), (230,80,170), 'GROUNDED', 0, 'wind-streaks','wind', 'JOJO-TENSION demo-only; char gain = tension gain, BG = base golden-hour | CLEAN-PLATE RERENDER: v7c labels=False plate, 0 red px, plate swap only'),
 ('CJ-02','punch-extend-snap', os.path.join(R, 'art-owed-punch-plates-20261031/plates-clean/CJ-02-punch-extend-snap-clean-plate-20261031.png'), 'script','street', 'Level 2', [1.1,0.95,0.7], [1.2,0.7,1.3], (255,178,229), (230,80,170), 'GROUNDED', 0, 'snap-lines','snap', 'JOJO-TENSION continued demo-only | CLEAN-PLATE RERENDER: v7c labels=False plate, 0 red px, plate swap only'),
 ('CJ-03','punch-impact-locked', os.path.join(R, 'art-owed-punch-plates-20261031/plates-clean/CJ-03-punch-impact-locked-clean-plate-20261031.png'), 'script','street', 'Level 2', [1.1,0.95,0.7], [1.1,0.95,0.7], (255,120,115), (220,60,50), 'GROUNDED', 0, 'impact-burst + gauntlet-glow','impact', 'JOJO-POWER demo-only; locked impact plate; FX passes, not god rays | CLEAN-PLATE RERENDER: v7c labels=False plate, 0 red px, plate swap only'),
 ('CJ-04','punch-recover', os.path.join(R, 'art-owed-punch-plates-20261031/plates-clean/CJ-04-punch-recover-clean-plate-20261031.png'), 'script','street', 'Level 2', [1.1,0.95,0.7], [1.1,0.95,0.7], (255,180,80), (255,120,0), 'GROUNDED', 0, 'afterglow-faint','afterglow', 'Return-to-base: tension/power beats closed here | CLEAN-PLATE RERENDER: v7c labels=False plate, 0 red px, plate swap only'),
 ('CJ-05','punch-across-down-placement', os.path.join(R, 'art-owed-punch-plates-20261031/plates-clean/CJ-05-punch-across-down-placement-clean-plate-20261031.png'), 'script','town', 'Level 2', [1,1,1], [1,1,1], (255,255,255), (255,255,255), 'GROUNDED', 0, 'placement-glow','glow', 'Across-down placement frame, NOT the impact frame. QC CJ-05 is post-episode per Space Ghost workflow, not a hold. | CLEAN-PLATE RERENDER: v7c labels=False plate, 0 red px, plate swap only'),
]

DUAL = {'CJ-19': ((255,180,80),(0,200,255),(255,120,0),(0,140,200)),
        'CJ-30': ((255,178,229),(0,200,255),(230,80,170),(0,140,200))}

def gain_img(rgb, gain):
    a = np.array(rgb).astype(np.float32)
    a = a * np.array(gain, dtype=np.float32)
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))

def resize_rgba(im, h):
    w0,h0 = im.size; w = int(round(w0*h/h0))
    return im.resize((w,h), Image.LANCZOS)

def script_bg(env, W, H, lut, ground_y, seed):
    rnd = random.Random(seed)
    top = tuple(int(min(255, c*1.15)) for c in (90,110,150))
    if env in ('street','town'):
        top, bot = (70,80,110), (150,130,110)
    elif env == 'stage':
        top, bot = (40,30,60), (90,70,80)
    elif env == 'any':
        top, bot = (80,85,100), (140,135,120)
    else:
        top, bot = (90,110,150), (160,150,130)
    arr = np.zeros((H,W,3), dtype=np.uint8)
    for y in range(H):
        t = y/max(1,H-1); arr[y,:,:] = [int(top[i]+(bot[i]-top[i])*t) for i in range(3)]
    img = Image.fromarray(arr); d = ImageDraw.Draw(img)
    # mid-plane silhouettes, horizon at ground_y
    if env == 'stage':
        d.rectangle([0,0,180,H], fill=(30,20,40)); d.rectangle([W-180,0,W,H], fill=(30,20,40))
        d.rectangle([0,ground_y,W,H], fill=(70,55,60))
    elif env == 'any':
        d.rectangle([0,ground_y,W,H], fill=(110,100,90))
    else:
        x = -40
        while x < W:
            bw = rnd.randint(90,220); bh = rnd.randint(180,420)
            d.rectangle([x, ground_y-bh, x+bw, ground_y], fill=(45,50,70))
            for wy in range(ground_y-bh+20, ground_y-20, 45):
                for wx in range(x+15, x+bw-15, 35):
                    if rnd.random() < 0.5: d.rectangle([wx,wy,wx+14,wy+18], fill=(200,180,120))
            x += bw + rnd.randint(10,60)
        d.rectangle([0,ground_y,W,H], fill=(100,95,85))
    img = gain_img(img, lut)
    return img

def painted_bg(src, W, H, lut, ground_y):
    im = Image.open(os.path.join(R, src)).convert('RGB')
    # room-proof canvas has a brown strip at bottom; crop to painting part
    if 'room-proof-bg-canvas' in src:
        im = im.crop((0,0,im.size[0], int(im.size[1]*0.83)))
    # cover-crop to canvas
    sw, sh = im.size; sc = max(W/sw, H/sh)
    im = im.resize((int(sw*sc)+1, int(sh*sc)+1), Image.LANCZOS)
    x = (im.size[0]-W)//2; y = (im.size[1]-H)//2
    im = im.crop((x,y,x+W,y+H))
    return gain_img(im, lut)

def draw_effect(kind, rim, bleed, box, W, H):
    """box = (x0,y0,x1,y1) char bbox in final canvas. Returns RGBA layer."""
    lay = Image.new('RGBA', (W,H), (0,0,0,0)); d = ImageDraw.Draw(lay)
    x0,y0,x1,y1 = box; cx = (x0+x1)//2; cy = (y0+y1)//2; w = x1-x0; h = y1-y0
    def ell(cx_,cy_,rx,ry,col,a,wd=3):
        d.ellipse([cx_-rx,cy_-ry,cx_+rx,cy_+ry], outline=col+(a,), width=wd)
    if kind == 'impact':
        for r,a in [(30,220),(55,160),(85,110)]:
            ell(cx, int(y0+h*0.35), r, r, (255,220,120), a, 5)
        for ang in range(0,360,30):
            a_ = math.radians(ang); d.line([cx, int(y0+h*0.35), cx+int(110*math.cos(a_)), int(y0+h*0.35)+int(110*math.sin(a_))], fill=(255,230,150,200), width=4)
        ell(cx, int(y0+h*0.35), 22, 22, rim, 230, 4)
    elif kind == 'snap':
        for i in range(7):
            yy = int(y0+h*0.25)+i*14; d.line([x1-10, yy, x1+90-i*8, yy-18], fill=rim+(190,), width=4)
    elif kind == 'wind':
        for i in range(6):
            yy = int(y0+h*0.3)+i*22; d.arc([x0-110, yy-30, x0+40, yy+30], 300, 60, fill=rim+(170,), width=4)
    elif kind == 'afterglow':
        ell(cx, cy, int(w*0.55), int(h*0.55), rim, 70, 10)
    elif kind == 'glow':
        ell(cx, int(y0+h*0.4), int(w*0.4), int(h*0.3), rim, 120, 8)
    elif kind == 'dust':
        for i,dx in enumerate([-70,-30,20,60]):
            d.ellipse([x0+w//2+dx-22, y1-18, x0+w//2+dx+22, y1+18], fill=(200,190,170,110))
    elif kind == 'sparkles':
        rnd = random.Random(7)
        for _ in range(26):
            sx = rnd.randint(max(0,x0-60), min(W-1,x1+60)); sy = rnd.randint(max(0,y0-40), min(H-1,y1))
            d.line([sx-9,sy,sx+9,sy], fill=rim+(200,), width=2); d.line([sx,sy-9,sx,sy+9], fill=rim+(200,), width=2)
    elif kind == 'rings':
        for r,a in [(int(w*0.5),150),(int(w*0.62),100),(int(w*0.74),60)]:
            ell(cx, y1+10, r, int(r*0.22), rim, a, 5)
    elif kind == 'speed':
        for i in range(8):
            yy = int(y0+h*0.2)+i*int(h*0.09); d.line([x0-130, yy, x0-15, yy], fill=rim+(180,), width=5)
    elif kind == 'aura':
        ell(cx, cy, int(w*0.58), int(h*0.54), rim, 130, 12)
    elif kind == 'gauntlet':
        ell(int(x0+w*0.32), int(y0+h*0.28), 34, 34, rim, 230, 6)
        ell(int(x0+w*0.68), int(y0+h*0.28), 34, 34, rim, 230, 6)
    elif kind == 'halo':
        ell(cx, int(y0+h*0.18), 90, 90, rim, 90, 8)
    elif kind == 'burst':
        for ang in range(0,360,24):
            a_ = math.radians(ang); d.line([cx, int(y0+h*0.15), cx+int(120*math.cos(a_)), int(y0+h*0.15)+int(120*math.sin(a_))], fill=rim+(200,), width=4)
    elif kind == 'flare':
        ell(int(x0+w*0.8), int(y0+30), 70, 70, rim, 160, 6); ell(int(x0+w*0.8), int(y0+30), 110, 110, rim, 70, 4)
    elif kind == 'bokeh':
        rnd = random.Random(11)
        for _ in range(22):
            sx = rnd.randint(0,W-1); sy = rnd.randint(0,ground_y if 'ground_y' in dir() else H-1)
            r = rnd.randint(6,20); d.ellipse([sx-r,sy-r,sx+r,sy+r], outline=rim+(120,), width=3)
    return lay.filter(ImageFilter.GaussianBlur(1.2))

results = []
for (sid, slug, plate, bg_kind, bg_src, level, lut, c_gain, rim, bleed, mode, height, effect, ekind, note) in SHOTS:
    is_room = sid in ('CJ-23','CJ-24','CJ-25','CJ-26','CJ-27')
    W, H = (1920,1280) if is_room else (1920,1080)
    ground_y = 1180 if is_room else 950
    # --- character plate, true alpha ---
    src = Image.open(plate).convert('RGBA')
    # DEBUG-CLEAN: punch plates carry baked red joint dots (debug markers).
    # Clean standard = white joint balls that stay. Convert red-debug pixels
    # to white, same geometry, same balls — this removes labels, it does not
    # recolour character art. Other plates have 0 such pixels (no-op).
    _arr = np.array(src)
    _red = (_arr[:,:,0]>200)&(_arr[:,:,1]<90)&(_arr[:,:,2]<90)&(_arr[:,:,3]>10)
    _red_px = int(_red.sum())
    assert _red_px == 0, f"CLEAN-PLATE RERENDER REFUSED: {sid} plate carries {_red_px} red debug px; clean plates must be 0 red"
    # No red->white conversion: clean plates carry no debug labels to convert.
    # White elbow/knee joint balls in the plate are character joints and stay.
    a = np.array(src)[:,:,3]; ys,xs = np.where(a>10)
    crop = src.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))
    if is_room:
        target_h = 1140 if sid != 'CJ-23' and sid != 'CJ-24' else 1034
        # seated: 1034 = 1140 * seated/standing bbox ratio (945/1042)
    else:
        target_h = 880
    char = resize_rgba(crop, target_h)
    cw, ch = char.size
    cx0 = (W-cw)//2
    feet_y = ground_y - height
    cy0 = feet_y - ch
    # NO-CROP: if the raised (airborne) figure would poke above the canvas,
    # expand the canvas upward and shift the ground line down by the same pad.
    if cy0 < 40:
        pad = 40 - cy0
        H += pad; ground_y += pad; feet_y += pad; cy0 += pad
    # --- background multiplane ---
    if bg_kind == 'painted':
        far = painted_bg(bg_src, W, H, lut, ground_y).filter(ImageFilter.GaussianBlur(4))
        mid_full = painted_bg(bg_src, W, H, lut, ground_y)
        mid_full = mid_full.resize((int(W*1.07), int(H*1.07)), Image.LANCZOS)
        mid_full = mid_full.crop((24, int(H*0.07)//2, 24+W, int(H*0.07)//2+H))
        # mid plane visible in ground band only (feathered top edge)
        band = Image.new('L', (W,H), 0); bd = ImageDraw.Draw(band)
        for y in range(ground_y-260, H):
            t = min(255, max(0, (y-(ground_y-260))*4)); bd.line([(0,y),(W,y)], fill=t)
        bg = Image.composite(mid_full, far, band)
        bg_kind_label = f'painted: {bg_src}'
    else:
        far = script_bg(bg_src, W, H, lut, ground_y, seed=int(sid[3:])).filter(ImageFilter.GaussianBlur(3))
        bg = far; bg_kind_label = f'colour-script multiplane ({bg_src} family; final painted BG owed)'
    canvas = bg.convert('RGBA')
    # --- shafts (L3 only) ---
    shaft_count = 0; shaft_colours = []
    if level.startswith('Level 3'):
        sh = Image.new('RGBA', (W,H), (0,0,0,0)); sd = ImageDraw.Draw(sh)
        cols = [DUAL[sid][0], DUAL[sid][1]] if sid in DUAL else [rim]
        shaft_colours = cols
        sx_top = W//2 + 260
        for i in range(6):
            x_top = sx_top - 300 + i*110; x_bot = x_top - 180
            sd.polygon([(x_top,0),(x_top+55,0),(x_bot+220,H),(x_bot+120,H)], fill=cols[i%len(cols)]+(30,))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        canvas.alpha_composite(sh); shaft_count = 6
    # --- shadow on ground line ---
    shl = Image.new('RGBA', (W,H), (0,0,0,0)); sd = ImageDraw.Draw(shl)
    sw_ = int(cw*(0.75 if mode=='GROUNDED' else 0.45)); sa = 95 if mode=='GROUNDED' else 45
    sd.ellipse([W//2-sw_//2, ground_y-8, W//2+sw_//2, ground_y+26], fill=(0,0,0,sa))
    canvas.alpha_composite(shl.filter(ImageFilter.GaussianBlur(6)))
    # --- character with LUT gain (char only) + uncertainty desat ---
    carr = np.array(char).astype(np.float32)
    rgb = carr[:,:,:3]
    if sid == 'CJ-26':
        lum = (0.299*rgb[:,:,0]+0.587*rgb[:,:,1]+0.114*rgb[:,:,2])
        lum = np.clip((lum-128)*1.2+128, 0, 255)
        rgb = np.stack([lum,lum,lum], axis=2)
    else:
        rgb = rgb * np.array(c_gain, dtype=np.float32)
    carr[:,:,:3] = np.clip(rgb,0,255)
    char_g = Image.fromarray(carr.astype(np.uint8))
    # --- rim (outer 4px) + bleed (inner 6px band) as separate layers ---
    mask = char_g.split()[3]
    dil = mask.filter(ImageFilter.MaxFilter(9))
    rim_layer = Image.new('RGBA', char.size, (0,0,0,0))
    dil_np = np.array(dil); m_np = np.array(mask)
    band_np = (dil_np>10) & (m_np<=10)
    rim_px = int(band_np.sum())
    if sid in DUAL:
        fr, bk, _, _ = DUAL[sid]
        w_ = char.size[0]
        xs_grid = np.tile(np.arange(w_), (char.size[1],1))
        rcol = np.zeros((*band_np.shape,4), dtype=np.uint8)
        left = band_np & (xs_grid < w_//2); right = band_np & (xs_grid >= w_//2)
        rcol[left] = (*fr, 230); rcol[right] = (*bk, 230)
        rim_layer = Image.fromarray(rcol)
    else:
        rcol = np.zeros((*band_np.shape,4), dtype=np.uint8); rcol[band_np] = (*rim, 230)
        rim_layer = Image.fromarray(rcol)
    ero = mask.filter(ImageFilter.MinFilter(13))
    ero_np = np.array(ero); bleed_band = (m_np>10) & (ero_np<=10)
    bleed_px = int(bleed_band.sum())
    bl = np.array(char_g).astype(np.float32)
    if sid in DUAL:
        _, _, fb, bb = DUAL[sid]
        w_ = char.size[0]; xs_grid = np.tile(np.arange(w_), (char.size[1],1))
        for col, sel in [(fb, xs_grid<w_//2),(bb, xs_grid>=w_//2)]:
            s = bleed_band & sel
            bl[s][:,:3] = bl[s][:,:3]*0.65 + np.array(col)*0.35
    else:
        bl[bleed_band][:,:3] = bl[bleed_band][:,:3]*0.65 + np.array(bleed)*0.35
    char_g = Image.fromarray(np.clip(bl,0,255).astype(np.uint8))
    # --- composite char + rim, then effects, then foreground strip ---
    canvas.alpha_composite(rim_layer, (cx0-0, cy0))  # rim layer is char-sized; paste at char origin
    # NOTE: rim_layer was built at char size; alpha_composite with dest works (same size layer, offset)
    canvas.alpha_composite(char_g, (cx0, cy0))
    box = (cx0, cy0, cx0+cw, cy0+ch)
    eff = draw_effect(ekind, rim, bleed, box, W, H)
    eff_np = np.array(eff)[:,:,3]; eff_px = int((eff_np>10).sum())
    canvas.alpha_composite(eff)
    # foreground strip (painted: blurred BG strip; script: dark floor strip), in front of feet, low alpha
    if bg_kind == 'painted':
        fg_src = painted_bg(bg_src, W, H, lut, ground_y).filter(ImageFilter.GaussianBlur(8))
    else:
        fg_src = script_bg(bg_src, W, H, lut, ground_y, seed=int(sid[3:])+99)
    fg = fg_src.crop((0, H-130, W, H)).convert('RGBA')
    fga = Image.new('RGBA', (W,130), (0,0,0,0)); fga.paste(fg, (0,0))
    fa = np.array(fga); fa[:,:,3] = (fa[:,:,3]*0.30).astype(np.uint8)
    canvas.alpha_composite(Image.fromarray(fa), (0, H-130))
    # --- no-crop verification: full char+glow bbox inside canvas ---
    final_rgb = canvas.convert('RGB')
    # glow bbox: rim+effect extents approximated by char box expanded 130px (effects reach) — verify by alpha of (rim+char+eff) region vs canvas edges
    margin_l = box[0]; margin_r = W-box[2]; margin_t = box[1]; margin_b = H-box[3]
    clipped = (box[0]<0 or box[1]<0 or box[2]>W or box[3]>H)
    outname = f'{sid}-{slug}-clean-plate-rerender-20261031.png'
    final_rgb.save(os.path.join(FIN, outname))
    # proof version: ground/flight line + feet marker (DEBUG ONLY, not the final)
    pr = final_rgb.copy(); pd = ImageDraw.Draw(pr)
    pd.line([(0,ground_y),(W,ground_y)], fill=(255,255,0), width=3)
    if mode == 'AIRBORNE':
        pd.line([(0,feet_y),(W,feet_y)], fill=(0,255,255), width=3)
        pd.ellipse([W//2-8, feet_y-8, W//2+8, feet_y+8], outline=(0,255,255), width=3)
    else:
        pd.ellipse([W//2-8, feet_y-8, W//2+8, feet_y+8], outline=(255,255,0), width=3)
    pr.save(os.path.join(PRF, f'{sid}-{slug}-clean-plate-rerender-proof-20261031.png'))
    results.append(dict(shot_id=sid, slug=slug, file=outname, proof=f'{sid}-{slug}-clean-plate-rerender-proof-20261031.png',
        plate=plate, bg_kind=bg_kind, bg_source=bg_src if bg_kind=='painted' else bg_kind_label,
        level=level, lut=lut, lut_gain=lut, char_gain=c_gain, rim=rim, bleed=bleed,
        dual_light=DUAL.get(sid), mode=mode, height_px=height, ground_y=ground_y, feet_y=feet_y,
        flight_line_y=(feet_y if mode=='AIRBORNE' else None),
        char_bbox=[int(box[0]),int(box[1]),int(box[2]),int(box[3])], char_size=[cw,ch],
        canvas=[W,H], clipped=clipped, margins=dict(left=int(margin_l), right=int(margin_r), top=int(margin_t), bottom=int(margin_b)),
        rim_px=rim_px, bleed_px=bleed_px, shaft_count=shaft_count, shaft_colours=[list(c) for c in shaft_colours],
        effect=effect, effect_px=eff_px, note=note, approval='0/1 PENDING Mars look',
        audio_cue=f'CJ-A{int(sid[3:]):02d} (cue ID only; no audio claimed)',
        red_debug_px_cleaned=_red_px))
    print(sid, 'canvas', W, H, 'char', cw, ch, 'feet', feet_y, 'ground', ground_y, 'rim', rim_px, 'bleed', bleed_px, 'shafts', shaft_count, 'eff', eff_px, 'clipped', clipped)

json.dump(results, open(os.path.join(OUT,'rerenders-manifest-20261031.json'),'w'), indent=1)
print('DONE', len(results))
