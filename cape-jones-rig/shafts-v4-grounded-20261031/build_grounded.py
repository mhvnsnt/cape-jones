"""Shafts v4 grounded rebuild.
Ground rule: GROUNDED unless shot spec says AIRBORNE.
Ground line Gy=1400 on 1100x1500 shafts canvas = top of the in-scene
floor/pools band y1400-1500 in the v4 Eevee master. Feet anchor =
alpha-bbox bottom. Grounded plates are shifted vertically ONLY (no
scale, no recolour, no horizontal move) so alpha bottom = 1400 exactly.
Airborne plates are NOT shifted (CJ-12,13,14,15,21); their height above
Gy is recorded, not planted. Shafts are masked by (1-plate_alpha) so
they stay behind the figure; figure pixels at alpha==255 are unchanged.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
V4 = '/home/hatch/workspace/cape-jones-rig/shafts-fix-100-20261031'
SHAFTS = os.path.join(V4, 'shafts-eevee-v4-fullres-20261031.png')
SHOTS = '/home/hatch/workspace/cape-jones-rig/shots-endtoend-20261031/shots-endtoend-20261031.json'
FIG = '/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/figure-only-plate-20261031.png'
OUT = os.path.join(BASE, 'per-shot-grounded')
GY = 1400
W, H = 1100, 1500

def bbox_of(plate):
    a = np.asarray(plate)[:,:,3]
    ys, xs = np.where(a > 10)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None

def shift_plate(plate, dy):
    arr = np.asarray(plate)
    out = np.zeros_like(arr)
    if dy >= 0:
        out[dy:,:] = arr[:H-dy,:]
    else:
        out[:H+dy,:] = arr[-dy:,:]
    return Image.fromarray(out)

def composite(shafts_rgb, plate, tint=None, inten=1.0):
    s = np.asarray(shafts_rgb).astype(float)
    if tint is not None:
        rim = np.array(tint, dtype=float)
        s = s * inten * 0.75 + np.tile(rim, (s.shape[0], s.shape[1], 1)) * inten * 0.25
        s = np.clip(s, 0, 255)
    p = np.asarray(plate).astype(float)
    a = p[:,:,3:4]/255.0
    return Image.fromarray((s*(1-a) + p[:,:,:3]*a).astype(np.uint8)), p

def runs(img):
    a = np.asarray(img.convert('RGB')).astype(float)
    band = a[500:700].mean(axis=0).mean(axis=1)
    thr = (float(np.percentile(band,90)) + float(np.percentile(band,10)))/2
    above = band > thr
    rs, x = [], 0
    while x < len(band):
        if above[x]:
            x0 = x
            while x < len(band) and above[x]: x += 1
            rs.append([int(x0), int(x-1)])
        else: x += 1
    return rs

def main():
    shafts = Image.open(SHAFTS).convert('RGB')
    shots = json.load(open(SHOTS))
    rows = []
    # main composite, untinted shafts, figure plate shifted to Gy
    fig = Image.open(FIG).convert('RGBA')
    fb = bbox_of(fig); fdy = GY - fb[3]
    fig_g = shift_plate(fig, fdy)
    comp, p = composite(shafts, fig_g)
    comp.save(os.path.join(BASE, 'composite-shafts-v4-GROUNDED-20261031.png'))
    main_row = {"id":"MAIN","mode":"GROUNDED","orig_bbox":fb,"shift_dy":fdy,
                "grounded_bbox":bbox_of(fig_g),"feet_y":bbox_of(fig_g)[3],
                "feet_minus_Gy":bbox_of(fig_g)[3]-GY,
                "shaft_runs":runs(shafts)}
    # per-shot
    for s in shots:
        plate = Image.open(s['plate']).convert('RGBA')
        ob = bbox_of(plate)
        if s['mode'] == 'GROUNDED':
            dy = GY - ob[3]; pg = shift_plate(plate, dy)
        else:
            dy = 0; pg = plate
        inten = 1.0 if s['level'] == 'Level 3' else 0.85
        c, p = composite(shafts, pg, tint=s['rim'], inten=inten)
        fn = f"{s['shot_id']}-{s['slug']}-shafts-GROUNDED-20261031.png"
        c.save(os.path.join(OUT, fn))
        gb = bbox_of(pg)
        opaque = np.asarray(pg)[:,:,3] == 255
        occl = float(np.abs(np.asarray(c).astype(float)[:,:, :3][opaque] - p[:,:,:3][opaque]).max()) if opaque.any() else -1
        if s['mode'] == 'GROUNDED':
            verdict = 'PASS' if abs(gb[3]-GY) <= 10 else 'FAIL'
        else:
            verdict = 'PASS-AIRBORNE'
        rows.append({"shot_id":s['shot_id'],"slug":s['slug'],"level":s['level'],"mode":s['mode'],
                     "orig_bbox":ob,"shift_dy":dy,"grounded_bbox":gb,"feet_y":gb[3],
                     "feet_minus_Gy":gb[3]-GY,"height_above_Gy":GY-gb[3] if s['mode']!='GROUNDED' else 0,
                     "file":fn,"occlusion_max_diff":occl,"pass_occlusion":bool(occl==0),
                     "figure_inside_canvas":bool(gb[0]>=0 and gb[1]>=0 and gb[2]<W and gb[3]<H),
                     "verdict":verdict})
        print(s['shot_id'], s['mode'], 'dy', dy, 'feet', gb[3], verdict, 'occl', occl)
    json.dump({"ground_line_Gy":GY,"canvas":[W,H],"main":main_row,"per_shot":rows},
              open(os.path.join(BASE,'gate-grounded-20261031.json'),'w'), indent=1)
    print('main', main_row)
    print(f"grounded {sum(1 for r in rows if r['mode']=='GROUNDED')}/25 PASS, airborne {sum(1 for r in rows if r['mode']!='GROUNDED')}/5 kept airborne, occlusion PASS {sum(1 for r in rows if r['pass_occlusion'])}/30")

if __name__ == '__main__':
    main()
