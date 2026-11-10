"""L5 helper layers (PIL/numpy only; the shot itself is composited in Blender).
Honest method notes, printed in the report:
- Estimated normals: Sobel gradient of the plate's own luminance (shape-from-
  shading proxy, industry intrinsic-relighting idea). NOT a true 3D rebuild
  normal pass; it IS direction-based (dot(N, light dir) per pixel), which is
  the step beyond L4's flat gradient wash. The L5 spec allows 'normal/depth
  pass or estimated normals'.
- Side weight: wrap/spill alpha multiplied by a left->right weight
  (1.0 backlit left -> 0.35 front right).
- Crisp shafts: hard-edged diagonal bands (2px feather only) over god-ray v2.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage

R = '/home/hatch/workspace/cape-jones-rig'
OUT = R + '/godray-level5-20261031'
L3 = R + '/godray-level3-20261031'
L4 = R + '/godray-level4-20261031'

def load(p):
    return Image.open(p).convert('RGBA')

def save(im, name):
    im.save(f'{OUT}/{name}'); print('saved', name, im.size)

def normal_shading(plate_path, tag):
    """Two clipped light layers: gold from the left, cyan from the right.
    N from Sobel of luminance; shade = 0.5 + 0.5*dot(N_xy, L_xy), scaled."""
    pl = load(plate_path)
    a = np.asarray(pl, dtype=np.float32)[..., 3] / 255.0
    lum = np.asarray(pl.convert('L'), dtype=np.float32) / 255.0
    gy, gx = np.gradient(lum)  # gy: vertical, gx: horizontal
    # normal xy components from shading gradient (shape-from-shading)
    nx, ny = -gx, -gy
    n = np.sqrt(nx**2 + ny**2 + 1.0)
    nx, ny = nx / n, ny / n
    for light, (lx, ly), color, fname in [
        ('gold', (-0.85, -0.35), (255, 180, 80), f'normal-shade-gold-{tag}.png'),
        ('cyan', (0.85, -0.35), (0, 200, 255), f'normal-shade-cyan-{tag}.png'),
    ]:
        dot = nx * lx + ny * ly  # -1..1
        shade = np.clip(0.5 + 0.5 * dot, 0, 1)
        # only the LIT side contributes (dot>0); scale to 0.38 max
        alpha = (np.clip(dot, 0, 1) ** 1.2 * 0.38 * a * 255).astype(np.uint8)
        layer = np.zeros((*a.shape, 4), dtype=np.uint8)
        layer[..., 0], layer[..., 1], layer[..., 2] = color
        layer[..., 3] = alpha
        save(Image.fromarray(layer), fname)
    # also save the normal map itself (visual proof of direction data)
    nmap = np.zeros((*a.shape, 4), dtype=np.uint8)
    nmap[..., 0] = ((nx * 0.5 + 0.5) * 255).astype(np.uint8)
    nmap[..., 1] = ((ny * 0.5 + 0.5) * 255).astype(np.uint8)
    nmap[..., 2] = 128
    nmap[..., 3] = (a * 255).astype(np.uint8)
    save(Image.fromarray(nmap), f'normal-map-{tag}.png')

def side_weighted(src_path, tag):
    """Multiply alpha by left(1.0)->right(0.35) weight."""
    im = load(src_path)
    arr = np.asarray(im, dtype=np.float32)
    W = arr.shape[1]
    w = np.linspace(1.0, 0.35, W, dtype=np.float32)[None, :]
    arr[..., 3] = arr[..., 3] * w
    save(Image.fromarray(arr.astype(np.uint8)), tag)

def rings_from_alpha(plate_path, tag):
    """inner ring 0-2px, outer ring 2-5px, from plate alpha (like L3 masks)."""
    pl = load(plate_path)
    a = np.asarray(pl)[..., 3] > 10
    d2 = ndimage.binary_dilation(a, iterations=2)
    d5 = ndimage.binary_dilation(a, iterations=5)
    inner = (d2 & ~a).astype(np.uint8) * 255
    outer = (d5 & ~d2).astype(np.uint8) * 255
    for arr, name in [(inner, f'mask-inner-{tag}.png'), (outer, f'mask-outer-{tag}.png')]:
        layer = np.zeros((*arr.shape, 4), dtype=np.uint8)
        layer[..., 3] = arr
        save(Image.fromarray(layer), name)

def crisp_shaft_bg():
    bg = load(L3 + '/godray-bg-v2-1100x1500.png').convert('RGB')
    W, H = bg.size
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # shafts from upper-left: perpendicular coordinate, diagonal bands
    s = xx * 0.94 + yy * 0.34
    period, core = 170.0, 62.0
    ph = np.mod(s, period)
    band = (ph < core).astype(np.float32)
    # 2px feather only: blur the band mask slightly
    band_im = Image.fromarray((band * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    band = np.asarray(band_im, dtype=np.float32) / 255.0
    arr = np.asarray(bg, dtype=np.float32)
    core_col = np.array([190, 240, 255], dtype=np.float32)
    arr = arr * (1 - band[..., None] * 0.38) + core_col * (band[..., None] * 0.38)
    save(Image.fromarray(arr.astype(np.uint8)).convert('RGBA'), 'godray-bg-v3-crisp-1100x1500.png')
    # edge sharpness measurement: horizontal profile at y=400 across a band edge
    row = band[400, :]
    # find first rising edge
    idx = np.where((row[:-1] < 0.1) & (row[1:] >= 0.9))[0]
    if len(idx):
        e = idx[0]
        seg = row[max(0, e - 10):e + 10]
        # width from 10% to 90%
        above10 = np.where(seg >= 0.1)[0][0]; above90 = np.where(seg >= 0.9)[0][0]
        print('CRISP EDGE 10-90 width px:', above90 - above10)
    # same measurement on v2 bg luminance profile at y=400 (soft bands reference)
    v2 = np.asarray(load(L3 + '/godray-bg-v2-1100x1500.png').convert('L'), dtype=np.float32) / 255.0
    print('v2 bg row400 min/max:', v2[400].min(), v2[400].max())

def dust():
    import random
    random.seed(5)
    im = Image.new('RGBA', (1100, 1500), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(120):
        x, y = random.randint(0, 1099), random.randint(0, 1499)
        r = random.randint(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, random.randint(60, 160)))
    save(im, 'dust-foreground-l5.png')

def pool():
    im = Image.new('RGBA', (1100, 1500), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([300, 1300, 800, 1440], fill=(255, 180, 80, 70))
    d.ellipse([350, 1320, 750, 1420], fill=(0, 200, 255, 50))
    im = im.filter(ImageFilter.GaussianBlur(25))
    save(im, 'ground-pool-l5.png')

arms = R + '/dual-light-variants-20261031/base-arms-up-transparent-20261031.png'
apose = R + '/rig-apose-v7c-clean-transparent.png'
print('arms size', load(arms).size, 'apose size', load(apose).size)
normal_shading(arms, 'armsup')
normal_shading(apose, 'apose')
rings_from_alpha(apose, 'apose')
# side-weighted rim/spill: reuse L3 solids+masks via rim-layer composition in Blender;
# here we pre-weight the spill layers (already RGBA images)
side_weighted(L3 + '/layer-spill-cyan.png', 'spill-cyan-sideweighted.png')
side_weighted(L3 + '/layer-spill-gold.png', 'spill-gold-sideweighted.png')
crisp_shaft_bg()
dust(); pool()
print('HELPERS DONE')
