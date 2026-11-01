#!/usr/bin/env python3
"""10-flex figure-extraction analysis — read-only on the original.
Methods (all slice_clean-style, no hand rectangles, no recolour):
 A alpha>10 connected components (8-conn) over the whole sheet
 B figure-column (x 300..860) alpha components
 C bright-core components (opaque & RGB-sum>400) in figure column
 D near-black components (opaque & RGB-sum<150) in figure column
 E purple-cowl components (head seeds) in figure column
Outputs: ANALYSIS.json + proof contact PNGs (mask visualisations only).
"""
import json, os
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

SRC = '/home/hatch/workspace/cape-jones-rig/transparent-plates-grok-full-sweep-20261031/plates/exposure-sheets/exposure-sheet-10-flex.png'
OUT = os.path.dirname(os.path.abspath(__file__))
a = np.array(Image.open(SRC).convert('RGBA')).astype(int)
H, W = a.shape[:2]
alpha, s = a[:,:,3], a[:,:,0]+a[:,:,1]+a[:,:,2]
opaque = alpha > 10
TICKS = [190,344,497,650,800,954,1108,1262,1425,1571]
ACTIONS = ['START FLEX','BICEP PEAK','BICEP PEAK','CHEST EXPAND','HOLD POSE','HNNNG!','HOLD POSE','(frame 8)','RELAX ARMS','(frame 10)']

def comps(mask, min_area=200):
    lab, n = ndimage.label(mask, structure=np.ones((3,3)))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None: continue
        ysl, xsl = sl; area = int((lab[sl]==i).sum())
        if area >= min_area:
            out.append({'area': area, 'x0': int(xsl.start), 'y0': int(ysl.start),
                        'x1': int(xsl.stop), 'y1': int(ysl.stop)})
    out.sort(key=lambda c: -c['area'])
    return out, lab

col = np.zeros((H, W), bool); col[:, 300:860] = True
fig_mask = opaque & col
res = {'source': SRC, 'size': [W, H], 'ticks': TICKS,
       'alpha_opaque_px': int(opaque.sum()),
       'alpha_components': comps(opaque, 800)[0][:20],
       'figure_column': {'x': [300, 860], 'opaque_px': int(fig_mask.sum()),
                         'components': comps(fig_mask, 800)[0][:20]},
       'bright_components': comps(fig_mask & (s > 400), 500)[0][:20],
       'black_components': comps(fig_mask & (s < 150), 200)[0][:20]}
# purple head seeds: R 50..150, G<110, B 70..190, R<B, opaque, in column
purp = opaque & col & (a[:,:,0]>=40)&(a[:,:,0]<=160)&(a[:,:,1]<=110)&(a[:,:,2]>=60)&(a[:,:,2]<=200)&(a[:,:,2]>a[:,:,0])
pc, _ = comps(purp, 300)
res['purple_components_ge300'] = pc[:30]
res['purple_head_candidates_ge1500'] = [c for c in pc if c['area'] >= 1500]
# per-frame: figure-column opaque px in tick-centred 155px bands (ANALYSIS ONLY, not cuts)
mids = [(TICKS[i]+TICKS[i+1])//2 for i in range(9)]
bands = [(0, mids[0])] + [(mids[i], mids[i+1]) for i in range(8)] + [(mids[-1], H)]
res['analysis_bands_midpoints'] = mids
res['per_frame_band_opaque_px'] = [int(fig_mask[y0:y1].sum()) for y0, y1 in bands]
json.dump(res, open(os.path.join(OUT, 'ANALYSIS.json'), 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('alpha_opaque_px',)}, indent=1))
print('figure-column opaque', res['figure_column']['opaque_px'])
print('figure-column alpha comps>=800:', len(res['figure_column']['components']))
for c in res['figure_column']['components'][:6]: print('  figcol', c)
print('bright comps>=500:', len(res['bright_components']))
for c in res['bright_components'][:8]: print('  bright', c)
print('black comps>=200:', len(res['black_components']))
for c in res['black_components'][:8]: print('  black', c)
print('purple comps>=300:', len(pc))
for c in res['purple_head_candidates_ge1500']: print('  head?', c)
print('band opaque px:', res['per_frame_band_opaque_px'])

# ---- proof contacts (visualisations of masks, not new art) ----
# Contact 1: alpha mask + tick lines + head-candidate boxes
vis = Image.new('RGB', (W, H), (40, 40, 40))
arr = np.array(vis); arr[opaque] = (255, 255, 255)
vis = Image.fromarray(arr); d = ImageDraw.Draw(vis)
for t in TICKS: d.line([(0, t), (W, t)], fill=(255, 0, 0), width=2)
for c in res['purple_head_candidates_ge1500']:
    d.rectangle([c['x0'], c['y0'], c['x1'], c['y1']], outline=(0, 255, 0), width=3)
vis.save(os.path.join(OUT, 'flex-contact-alpha-mask-ticks-heads.png'))
# Contact 2: component maps (alpha comps coloured) for figure column, cropped to column
def cmap(mask, path):
    lab, n = ndimage.label(mask, structure=np.ones((3,3)))
    rng = np.random.default_rng(7)
    cols = rng.integers(40, 255, size=(n+1, 3)); cols[0] = (30, 30, 30)
    img = Image.fromarray(cols[lab].astype(np.uint8))
    img.save(path)
cmap(fig_mask, os.path.join(OUT, 'flex-contact-figcol-alpha-components.png'))
cmap(fig_mask & (s > 400), os.path.join(OUT, 'flex-contact-figcol-bright-components.png'))
cmap(fig_mask & (s < 150), os.path.join(OUT, 'flex-contact-figcol-black-components.png'))
print('contacts written')
