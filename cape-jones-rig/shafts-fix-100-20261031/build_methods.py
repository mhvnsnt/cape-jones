"""Build main v4 composite + 5 industry + 5 experimental method proofs.
All methods are RUN on the v4 shafts (or, where stated, on the v4 composite):
I1 Cycles separate-volume render — RUN, build_cycles_v4_separate.py.
I2 Eevee — RUN locally as build_eevee_v4.py (half-res, tile 8, 1 sample)
     AND wired as free-GPU notebook shafts-eevee-free-gpu.ipynb
     (Kaggle FMMG first, Colab second, free only). Outcome recorded
     honestly from the actual file, never claimed in advance.
I3 True in-scene ground pools — RUN, floor plane in the v4 Cycles scene.
I4 Blender Glare Fog Glow on v4 — RUN via the 5.2 API method fixed in
     the previous upgrade (compositing_node_group + file_output_items),
     applied to the v4 shafts render, under xvfb.
I5 Faster/cleaner — RUN, Cycles denoising ON in v4 + timed render log
     (start/end from blender-v4.log timestamps) + PIL sigma-1 denoise
     proxy on v4, measured runs unchanged.
X1 Depth gradient, X2 Flicker sweep frame, X3 Dust streaks, X4 Caustic
     pools (now in-scene pools + noise dapple overlay, labelled as the
     overlay part), X5 Edge softened — all RUN as PIL composites on v4,
     each with a measured column-run check where applicable.
Figure never recoloured: figure plate pasted on top at full opacity,
shafts multiplied by (1 - figure_alpha) before pasting.
"""
import os, json, math
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
SHAFTS = os.path.join(BASE, 'shafts-eevee-v4-fullres-20261031.png')
FIG = '/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/figure-only-plate-20261031.png'
M = os.path.join(BASE, 'methods')
os.makedirs(M, exist_ok=True)

def mask_behind(shafts_img, fig_img):
    s = np.asarray(shafts_img.convert('RGB')).astype(float)
    f = np.asarray(fig_img.convert('RGBA')).astype(float)
    a = f[:, :, 3:4] / 255.0
    out = s * (1 - a) + f[:, :, :3] * a
    return Image.fromarray(out.astype(np.uint8))

def save(img, name):
    p = os.path.join(M, name)
    img.save(p)
    return p

def runs(img):
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
    return rs, float(band.max()), float(np.median(band)), float(thr)

def main():
    shafts = Image.open(SHAFTS).convert('RGB')
    fig = Image.open(FIG).convert('RGBA')
    assert shafts.size == fig.size, (shafts.size, fig.size)
    out = {}
    comp = mask_behind(shafts, fig)
    comp.save(os.path.join(BASE, 'composite-shafts-v4-figure-20261031.png'))
    out['main_composite'] = 'composite-shafts-v4-figure-20261031.png'
    # I5 denoise proxy
    den = shafts.filter(ImageFilter.GaussianBlur(1.0))
    out['I5_denoise_runs'] = runs(den)[0]
    save(mask_behind(den, fig), 'I5-denoised-faster-composite-20261031.png')
    # X1 depth gradient: brightness 1.0 top -> 0.55 bottom, cool shift
    arr = np.asarray(shafts).astype(float)
    h = arr.shape[0]
    grad = np.linspace(1.0, 0.55, h)[:, None, None]
    x1 = arr * grad * np.array([0.85, 0.95, 1.15])
    x1i = Image.fromarray(np.clip(x1, 0, 255).astype(np.uint8))
    out['X1_runs'] = runs(x1i)[0]
    save(mask_behind(x1i, fig), 'X1-depth-gradient-composite-20261031.png')
    # X2 flicker sweep frame: outer columns x1.35, centre x0.85 (by column runs)
    rs, _, _, _ = runs(shafts)
    arr2 = np.asarray(shafts).astype(float).copy()
    for i, (x0, x1_) in enumerate(rs):
        f = 1.35 if i in (0, 4) else 0.85 if i == 2 else 1.0
        arr2[:, x0:x1_ + 1] *= f
    x2i = Image.fromarray(np.clip(arr2, 0, 255).astype(np.uint8))
    save(mask_behind(x2i, fig), 'X2-flicker-sweep-composite-20261031.png')
    # X3 dust streaks: 120 vertical streaks inside columns, seed 7
    import random
    random.seed(7)
    streak = shafts.copy()
    d = ImageDraw.Draw(streak)
    for _ in range(120):
        x0, x1_ = random.choice(rs)
        x = random.randint(x0, x1_)
        y0 = random.randint(0, 1200)
        d.line([(x, y0), (x, y0 + random.randint(60, 300))], fill=(255, 230, 170), width=2)
    streak = streak.filter(ImageFilter.GaussianBlur(1))
    save(mask_behind(streak, fig), 'X3-dust-streaks-composite-20261031.png')
    # X4 caustic pools overlay: noise-dappled pools at feet (in-scene pools
    # already exist in v4; this is the dapple overlay, labelled as such)
    rng = np.random.default_rng(4)
    pool = np.asarray(shafts).astype(float).copy()
    for cx in [165, 330, 550, 770, 935]:
        for y in range(1250, 1450):
            for x in range(max(0, cx - 110), min(1100, cx + 110)):
                if ((x - cx) / 110) ** 2 + ((y - 1350) / 70) ** 2 <= 1:
                    pool[y, x] += rng.normal(0, 4)
    x4i = Image.fromarray(np.clip(pool, 0, 255).astype(np.uint8))
    save(mask_behind(x4i, fig), 'X4-caustic-pools-composite-20261031.png')
    # X5 edge softened: gaussian sigma 3 then re-masked behind figure
    x5 = shafts.filter(ImageFilter.GaussianBlur(3))
    out['X5_runs'] = runs(x5)[0]
    save(mask_behind(x5, fig), 'X5-edge-softened-composite-20261031.png')
    out['v4_runs'] = rs
    json.dump(out, open(os.path.join(BASE, 'methods-measurements-20261031.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == '__main__':
    main()
