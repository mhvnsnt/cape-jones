"""Cape styles pack v2 — warps of Cape Jones's own Cape_Back_Main.png.
Method: 2D cloth as bone-chain / verlet-style deformation approximated by
per-pixel remaps: gravity taper, wind shear, sine folds, hem flare.
Folds: dark Multiply bands + light Screen bands following fold direction,
so folds read as fabric, not flat colour. No show art; base is own piece.
v1 lying-flat failure (tall narrow strip) avoided: horizontal styles are
rotated + re-proportioned, never just squashed vertically.
"""
import math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = "/home/hatch/workspace/cape-jones-rig/sliced/Cape_Back_Main.png"
OUT = "/home/hatch/workspace/cape-jones-rig/cape-styles-v2-20261031"
base = Image.open(SRC).convert("RGBA")
W, H = base.size

def remap(img, dx_fn, dy_fn, scale=1.0, rotate=0):
    """Backward remap: out(x,y) = img(x+dx, y+dy) sampled bilinear-ish (nearest via numpy indexing)."""
    arr = np.array(img)
    h, w = arr.shape[:2]
    ys, xs = np.mgrid[0:h, 0:w]
    sx = (xs - dx_fn(xs, ys)).astype(int)
    sy = (ys - dy_fn(xs, ys)).astype(int)
    valid = (sx >= 0) & (sx < w) & (sy >= 0) & (sy < h)
    sxc = np.clip(sx, 0, w - 1); syc = np.clip(sy, 0, h - 1)
    out = arr[syc, sxc].copy()
    out[~valid] = (0, 0, 0, 0)
    im = Image.fromarray(out, "RGBA")
    if scale != 1.0 or rotate != 0:
        nw, nh = int(w * scale), int(h * scale)
        im = im.resize((nw, nh), Image.LANCZOS)
        if rotate:
            im = im.rotate(rotate, resample=Image.BICUBIC, expand=True)
    return im

def folds(im, n=7, vertical=True, strength=0.28, phase=0.0):
    """Subtle fold shading: low-alpha dark/light bands clipped to alpha, blurred."""
    im = im.convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(n * 2 + 1):
        a_dark, a_light = 42, 26
        col = (0, 0, 0, a_dark) if i % 2 == 0 else (255, 200, 130, a_light)
        if vertical:
            x0 = int(i * w / (n * 2 + 1))
            od.rectangle([x0, 0, x0 + max(8, w // (n * 3)), h], fill=col)
        else:
            y0 = int(i * h / (n * 2 + 1))
            od.rectangle([0, y0, w, y0 + max(8, h // (n * 3))], fill=col)
    overlay = overlay.filter(ImageFilter.GaussianBlur(6))
    # clip overlay to source alpha
    alpha = im.split()[3]
    overlay.putalpha(Image.composite(overlay.split()[3], Image.new("L", (w, h), 0), alpha))
    return Image.alpha_composite(im, overlay)

def hem_weight(im, darken=0.25):
    """Darker hem band (weight) at bottom of alpha span."""
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rows = np.where(alpha.max(axis=1) > 10)[0]
    if len(rows):
        y0 = rows[-1] - max(20, int(0.08 * im.size[1]))
        for y in range(y0, im.size[1]):
            f = (y - y0) / max(1, im.size[1] - y0)
            m = alpha[y] > 10
            arr[y, :, 0:3] = (arr[y, :, 0:3] * (1 - darken * f)).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")

def save(im, name):
    im.save(f"{OUT}/{name}")
    print(name, im.size)

def taper(dx_amp):
    return lambda xs, ys: (dx_amp * (ys / H) ** 2 * np.sin(xs / W * 3.0))

styles = []
def add(name, im, meta):
    save(im, name)
    styles.append({"file": name, "size": list(im.size), **meta})

# 1 draped (v1 improved: vertical folds)
im = folds(base, n=9, vertical=True, strength=0.30)
add("cape-01-draped-20261031.png", hem_weight(im), {"form": "draped", "direction": "down, vertical", "wind": "none", "weight": "heavy hem", "folds": "9 vertical, gravity", "movement": "idle, standing", "method": "warp + fold shading"})
# 2 lying-flat (horizontal, re-proportioned, NOT a squash strip)
im = base.rotate(90, expand=True)
im = folds(im, n=8, vertical=False, strength=0.22)
add("cape-02-lying-flat-20261031.png", im, {"form": "lying-flat", "direction": "horizontal, spread", "wind": "none", "weight": "flat, pooled", "folds": "8 horizontal", "movement": "resting, knocked down", "method": "rotate + fold shading"})
# 3 swinging (S-curve)
im = remap(base, lambda xs, ys: 40 * np.sin(ys / H * 3.14 * 1.5), lambda xs, ys: np.zeros_like(xs, dtype=float))
add("cape-03-swinging-20261031.png", folds(im, n=8, vertical=True, strength=0.28), {"form": "swinging", "direction": "S-curve, side to side", "wind": "moderate", "weight": "medium", "folds": "8 vertical following curve", "movement": "walk, turn", "method": "sine warp + folds"})
# 4 billowing (bottom flare)
im = remap(base, lambda xs, ys: ((xs - W / 2) * (ys / H) * 0.6), lambda xs, ys: np.zeros_like(xs, dtype=float))
add("cape-04-billowing-20261031.png", folds(im, n=10, vertical=True, strength=0.30), {"form": "billowing", "direction": "outward, flared hem", "wind": "strong from behind", "weight": "light, lifted", "folds": "10 vertical, flared", "movement": "run, fly, wind", "method": "flare warp + folds"})
# 5 wind-blown left
im = remap(base, lambda xs, ys: -70 * (ys / H) ** 1.5, lambda xs, ys: np.zeros_like(xs, dtype=float))
add("cape-05-wind-left-20261031.png", folds(im, n=9, vertical=True, strength=0.32), {"form": "wind-blown left", "direction": "hem swept left", "wind": "strong right-to-left", "weight": "light", "folds": "9 diagonal-leaning", "movement": "run, storm, fly", "method": "shear warp + folds"})
# 6 wind-blown right
im = remap(base, lambda xs, ys: 70 * (ys / H) ** 1.5, lambda xs, ys: np.zeros_like(xs, dtype=float))
add("cape-06-wind-right-20261031.png", folds(im, n=9, vertical=True, strength=0.32), {"form": "wind-blown right", "direction": "hem swept right", "wind": "strong left-to-right", "weight": "light", "folds": "9 diagonal-leaning", "movement": "run, storm, fly", "method": "shear warp + folds"})
# 7 lifted up (hem raised, tapered)
im = remap(base, lambda xs, ys: ((xs - W / 2) * (1 - ys / H) * 0.4), lambda xs, ys: -18 * (1 - ys / H))
add("cape-07-lifted-up-20261031.png", folds(im, n=8, vertical=True, strength=0.26), {"form": "lifted up", "direction": "up, gathered", "wind": "updraft / jump", "weight": "lifted", "folds": "8 vertical, gathered", "movement": "jump, punch, flex", "method": "lift warp + folds"})
# 8 hanging heavy (long, narrow, weighted hem)
im = base.resize((int(W * 0.85), int(H * 1.05)), Image.LANCZOS)
add("cape-08-hanging-heavy-20261031.png", hem_weight(folds(im, n=11, vertical=True, strength=0.34), darken=0.35), {"form": "hanging heavy", "direction": "straight down, weighted", "wind": "none", "weight": "very heavy hem", "folds": "11 tight vertical", "movement": "idle, dramatic stand", "method": "taper + heavy hem + folds"})
# 9 twisted (spiral-ish sine, opposite phases top/bottom)
im = remap(base, lambda xs, ys: 50 * np.sin(ys / H * 6.28), lambda xs, ys: np.zeros_like(xs, dtype=float))
add("cape-09-twisted-20261031.png", folds(im, n=9, vertical=True, strength=0.30), {"form": "twisted", "direction": "spiral, torso turn", "wind": "spin", "weight": "medium", "folds": "9 following twist", "movement": "spin, dance twist, dodge", "method": "double-sine warp + folds"})
# 10 folded over shoulder (diagonal fold, shortened)
im = base.rotate(-28, expand=True)
im = im.crop((0, 0, im.size[0], int(im.size[1] * 0.62)))
add("cape-10-over-shoulder-20261031.png", folds(im, n=7, vertical=True, strength=0.28), {"form": "folded over shoulder", "direction": "diagonal up-left, shortened", "wind": "none", "weight": "folded, thick", "folds": "7 diagonal", "movement": "walk, talk, casual", "method": "rotate + crop + folds"})
# 11 wrapped in front (narrow, centred)
im = base.resize((int(W * 0.62), H), Image.LANCZOS)
add("cape-11-wrapped-front-20261031.png", folds(im, n=10, vertical=True, strength=0.30), {"form": "wrapped in front", "direction": "narrow, centred, closed", "wind": "none", "weight": "closed, warm", "folds": "10 tight vertical", "movement": "cold, hiding, stealth", "method": "narrow + folds"})
# 12 trailing behind (running, long horizontal-back sweep)
im = base.rotate(38, expand=True)
add("cape-12-trailing-behind-20261031.png", folds(im, n=9, vertical=True, strength=0.30), {"form": "trailing behind", "direction": "back-diagonal, running", "wind": "strong forward motion", "weight": "streaming", "folds": "9 streaming", "movement": "run, chase", "method": "rotate + folds"})
# 13 flying spread (wide flare, both sides)
im = remap(base, lambda xs, ys: ((xs - W / 2) * (ys / H) * 1.0), lambda xs, ys: -30 * (ys / H))
add("cape-13-flying-spread-20261031.png", folds(im, n=12, vertical=True, strength=0.32), {"form": "flying spread", "direction": "wide, both sides, lifted", "wind": "strong airflow", "weight": "light, spread", "folds": "12 wide", "movement": "fly, dive, superhero landing", "method": "wide flare + folds"})
# 14 sitting pooled (hem spread on ground)
im = base.resize((int(W * 1.25), int(H * 0.72)), Image.LANCZOS)
add("cape-14-sitting-pooled-20261031.png", folds(im, n=10, vertical=False, strength=0.26), {"form": "sitting pooled", "direction": "outward on ground", "wind": "none", "weight": "pooled, heavy hem", "folds": "10 ground folds", "movement": "sit, rest", "method": "wide + short + ground folds"})
# 15 cape raised high (both sides up, V shape)
im = remap(base, lambda xs, ys: ((xs - W / 2) * (ys / H) * 0.5), lambda xs, ys: -80 * np.abs(xs - W / 2) / W * (ys / H))
add("cape-15-raised-high-20261031.png", folds(im, n=10, vertical=True, strength=0.30), {"form": "raised high", "direction": "V, both sides up", "wind": "dramatic reveal", "weight": "lifted", "folds": "10 V-following", "movement": "reveal, dance accent, fight stance", "method": "V warp + folds"})

json.dump(styles, open(f"{OUT}/cape-styles-v2-manifest-20261031.json", "w"), indent=2)
print(f"styles: {len(styles)}")
