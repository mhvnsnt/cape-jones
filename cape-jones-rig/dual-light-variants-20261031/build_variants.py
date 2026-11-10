#!/usr/bin/env python3
"""5 dual-light rim-mix variants on the arms-up transparent base.
PIL rim technique (dilated-alpha rings, directional fade, bleed, shadow).
God rays here are PIL DRAFT (fan wedges, blurred) — a Blender volumetric
background is attempted separately; if it succeeds, V2/V5 get Blender-bg
re-issues and this file's rays are superseded, not hidden.
Colours: gold rim (255,180,80), gold bleed (255,120,0), cyan rim (0,200,255),
cyan bleed (0,120,255), gold gain (1.10,0.95,0.70)."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np, os
R = "/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031"
BASE = Image.open(os.path.join(R, "base-arms-up-transparent-20261031.png")).convert("RGBA")
W, H = BASE.size
alpha = BASE.split()[3]
arr = np.array(alpha)
ys, xs = np.where(arr > 10)
xmin, xmax, ymin, ymax = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
GOLD = (255, 180, 80); GOLD_BLEED = (255, 120, 0)
CYAN = (0, 200, 255); CYAN_BLEED = (0, 120, 255)
GOLD_GAIN = np.array([1.10, 0.95, 0.70])

def graded(gain):
    rgb = np.array(BASE.convert("RGB")).astype(float) * gain
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    out.putalpha(alpha); return out

def ring(inner_px, outer_px):
    """Alpha mask for a ring band: dilate outer minus dilate inner."""
    d_out = alpha.filter(ImageFilter.MaxFilter(outer_px * 2 + 1))
    d_in = alpha.filter(ImageFilter.MaxFilter(inner_px * 2 + 1)) if inner_px > 0 else Image.new("L", (W, H), 0)
    return Image.fromarray(np.clip(np.array(d_out).astype(int) - np.array(d_in).astype(int), 0, 255).astype(np.uint8))

def solid(mask, color, opacity=1.0):
    layer = Image.new("RGBA", (W, H), color + (0,))
    m = mask.point(lambda v: int(v * opacity)) if opacity < 1.0 else mask
    layer.putalpha(m); return layer

def bleed_layer(color, opacity=0.20):
    band = ring(0, 5).filter(ImageFilter.GaussianBlur(4))
    return solid(band, color, opacity)

def shadow_layer():
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    cx = (xmin + xmax) // 2
    d.ellipse([cx - (xmax - xmin) // 3, ymax - 10, cx + (xmax - xmin) // 3, ymax + 50], fill=(40, 40, 90, 110))
    return s.filter(ImageFilter.GaussianBlur(6))

def bg_with_glow(glow_color=None, glow_alpha=0):
    bg = Image.new("RGBA", (W, H), (5, 8, 16, 255))
    if glow_color and glow_alpha:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(glow)
        cx, cy = (xmin + xmax) // 2, (ymin + ymax) // 2
        d.ellipse([cx - 450, cy - 550, cx + 450, cy + 550], fill=glow_color + (glow_alpha,))
        bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))
    return bg

def godrays_draft(color=(0, 200, 255), strength=90):
    """Fan wedges from a source above/behind, blurred, background only."""
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(rays)
    sx, sy = (xmin + xmax) // 2, ymin - 260
    for i, dx in enumerate(range(-500, 501, 100)):
        d.polygon([(sx, sy), (sx + dx - 55, H), (sx + dx + 55, H)], fill=color + (strength,))
    rays = rays.filter(ImageFilter.GaussianBlur(10))
    # keep rays off the character silhouette (dilated 8px)
    block = alpha.filter(ImageFilter.MaxFilter(17))
    rarr = np.array(rays); barr = np.array(block)
    rarr[barr > 10, 3] = 0
    return Image.fromarray(rarr)

def save(name, img):
    p = os.path.join(R, name); img.convert("RGB").save(p); print("saved", p)

def compose(body, layers):
    bg = layers.pop(0)
    for lyr in layers: bg.alpha_composite(lyr)
    bg.alpha_composite(body)
    return bg

inner, outer = ring(0, 2), ring(2, 5)
# left->right gradient across silhouette for V5 (gold front-left, cyan back-right)
gx = np.zeros((H, W), dtype=float)
gx[:, xmin:xmax + 1] = np.linspace(0, 1, xmax - xmin + 1)[None, :]
def mixed_rim(inner_mask, outer_mask):
    """Inner+outer rim with per-pixel gold/cyan mix by x-gradient."""
    for mask, strength in ((inner_mask, 1.0), (outer_mask, 0.85)):
        m = np.array(mask).astype(float) / 255.0 * strength
        r = GOLD[0] * (1 - gx) + CYAN[0] * gx
        g = GOLD[1] * (1 - gx) + CYAN[1] * gx
        b = GOLD[2] * (1 - gx) + CYAN[2] * gx
        a = (m * 255).astype(np.uint8)
        yield Image.fromarray(np.stack([r.astype(np.uint8), g.astype(np.uint8),
                                        b.astype(np.uint8), a], axis=-1), "RGBA")

# V1: gold rim only, no cyan backlight
body = graded(GOLD_GAIN)
save("v1-gold-rim-only-20261031.jpg", compose(body, [
    bg_with_glow(), shadow_layer(), bleed_layer(GOLD_BLEED), solid(inner, GOLD), solid(outer, GOLD, 0.7)]))
# V2: cyan rim + gold LUT + cyan back god rays (PIL DRAFT rays)
body = graded(GOLD_GAIN)
save("v2-cyan-rim-gold-lut-cyan-godrays-draft-20261031.jpg", compose(body, [
    bg_with_glow(CYAN, 70), godrays_draft(), shadow_layer(), bleed_layer(CYAN_BLEED),
    solid(inner, CYAN), solid(outer, CYAN, 0.7)]))
# V3: gold inner, cyan outer around it
body = graded(GOLD_GAIN)
save("v3-gold-inner-cyan-outer-20261031.jpg", compose(body, [
    bg_with_glow(CYAN, 45), shadow_layer(), bleed_layer(GOLD_BLEED),
    solid(inner, GOLD), solid(outer, CYAN, 0.85)]))
# V4: reverse — cyan inner, gold outer (comparison)
body = graded(GOLD_GAIN)
save("v4-cyan-inner-gold-outer-20261031.jpg", compose(body, [
    bg_with_glow(GOLD, 45), shadow_layer(), bleed_layer(CYAN_BLEED),
    solid(inner, CYAN), solid(outer, GOLD, 0.85)]))
# V5: mixed silhouette — gold front-facing (left) edges, cyan back-facing (right) edges + cyan god rays (DRAFT)
body = graded(GOLD_GAIN)
layers = [bg_with_glow(CYAN, 60), godrays_draft(strength=70), shadow_layer()]
layers.extend(mixed_rim(inner, outer))
save("v5-mixed-silhouette-gold-front-cyan-back-draft-20261031.jpg", compose(body, layers))
print("all 5 variants built")
