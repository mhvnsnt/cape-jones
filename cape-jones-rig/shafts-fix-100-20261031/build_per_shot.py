"""Per-shot shafts 30/30.
For each shot in shots-endtoend-20261031.json, build a shafts composite
from that shot's own transparent plate + the v4 shafts master:
- shafts tinted toward the shot's rim colour at 25% mix (shafts only,
  figure NEVER recoloured), intensity L3=1.0, L2=0.85
- shafts masked by (1 - plate_alpha), plate pasted on top at full opacity
- canvas 1100x1500 (plate canvas), figure bbox checked inside canvas
- output per-shot/<SHOT>-shafts-20261031.png + per-shot JSON table with
  column runs (from the shafts layer), shaft px, figure bbox, occlusion
  diff (must be 0 where plate opaque), mode (GROUNDED/AIRBORNE) carried
  from the shot spec.
Honest label: the Blender master is ONE v4 separate-volume render;
per-shot application is a measured composite reuse per shot, not 30
separate Blender volumetric renders. That is stated in the report.
"""
import os, json
import numpy as np
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SHAFTS = os.path.join(BASE, 'shafts-eevee-v4-fullres-20261031.png')
SHOTS = '/home/hatch/workspace/cape-jones-rig/shots-endtoend-20261031/shots-endtoend-20261031.json'
OUT = os.path.join(BASE, 'per-shot')
os.makedirs(OUT, exist_ok=True)

def runs_of(img):
    a = np.asarray(img.convert('RGB')).astype(float)
    band = a[500:700].mean(axis=0).mean(axis=1)
    thr = (float(np.percentile(band, 90)) + float(np.percentile(band, 10))) / 2
    above = band > thr
    rs, x, w = [], 0, len(band)
    while x < w:
        if above[x]:
            x0 = x
            while x < w and above[x]:
                x += 1
            rs.append([int(x0), int(x - 1)])
        else:
            x += 1
    return rs

def main():
    shafts = Image.open(SHAFTS).convert('RGB')
    shots = json.load(open(SHOTS))
    rows = []
    for s in shots:
        plate = Image.open(s['plate']).convert('RGBA')
        assert plate.size == shafts.size, (s['shot_id'], plate.size)
        rim = np.array(s['rim'], dtype=float)
        inten = 1.0 if s['level'] == 'Level 3' else 0.85
        sarr = np.asarray(shafts).astype(float)
        tinted = sarr * inten * 0.75 + np.tile(rim, (sarr.shape[0], sarr.shape[1], 1)) * inten * 0.25
        tinted = np.clip(tinted, 0, 255)
        parr = np.asarray(plate).astype(float)
        a = parr[:, :, 3:4] / 255.0
        comp = tinted * (1 - a) + parr[:, :, :3] * a
        comp_img = Image.fromarray(comp.astype(np.uint8))
        fn = f"{s['shot_id']}-{s['slug']}-shafts-20261031.png"
        comp_img.save(os.path.join(OUT, fn))
        opaque = parr[:, :, 3] == 255
        occl = float(np.abs(comp[:, :, :3][opaque] - parr[:, :, :3][opaque]).max()) if opaque.any() else -1
        bbox = plate.split()[3].getbbox()
        rows.append({
            "shot_id": s['shot_id'], "slug": s['slug'], "level": s['level'],
            "mode": s['mode'], "file": fn, "rim": s['rim'], "intensity": inten,
            "shaft_runs_tinted": runs_of(Image.fromarray(tinted.astype(np.uint8))),
            "figure_bbox": list(bbox) if bbox else None,
            "figure_inside_canvas": bool(bbox and bbox[0] >= 0 and bbox[1] >= 0 and bbox[2] <= 1100 and bbox[3] <= 1500),
            "occlusion_max_diff": occl, "pass_occlusion": bool(occl == 0),
        })
    json.dump(rows, open(os.path.join(BASE, 'per-shot-table-20261031.json'), 'w'), indent=1)
    passed = sum(1 for r in rows if r['pass_occlusion'] and r['figure_inside_canvas'])
    print(f"per-shot built {len(rows)}/30, gate-pass {passed}/30")
    for r in rows:
        print(r['shot_id'], r['file'], 'occl', r['occlusion_max_diff'], 'inside', r['figure_inside_canvas'], 'runs', len(r['shaft_runs_tinted']))

if __name__ == '__main__':
    main()
