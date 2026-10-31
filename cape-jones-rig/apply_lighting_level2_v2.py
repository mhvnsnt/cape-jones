#!/usr/bin/env python3
"""Level 2 v2 — upgraded, clean, no stubs. Free PIL stack.
Upgrades over v1 (which had a squashed-silhouette blob shadow, a flat
8px bleed ring, and no internal line light and no LUT grade):
1. LUT grade FIRST (approved golden-hour gain for colored, neutral for
   non-colored) — grade is a layer, not an afterthought.
2. Directional rim: outer-only 3px, dilated alpha minus original, 0.8px
   feather, strength fades lit-side (left) 1.0 -> opposite side 0.3.
   No rim around any debug label — plates with red labels are refused.
3. Bleed with falloff: 5px band, 4px blur, opacity 0.20 (tightened from 8px/0.25 after viewing v2 — halo was too wide), same lit-side
   fade, edge-band only, never whole-suit tint.
4. Clean shadow: NO squashed silhouette blob. One soft ground ellipse
   (cool blue-violet, blurred) + two blurred contact foot pads at the
   actual foot positions (bottom-most alpha in each half).
5. Internal line light: dark line pixels inside a 12px inner edge band,
   lit side only, blended 50% toward the rim colour, fading inward.
   Base art is copied untouched; every light is a separate layer on top.
6. Feathered silhouette edge (1px) so the rim does not look jagged.
Usage: python3 apply_lighting_level2_v2.py PLATE.PNG OUTDIR
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageChops

def main():
    plate_path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    plate = Image.open(plate_path).convert("RGBA")
    a = np.array(plate)
    red = int(((a[:, :, 0] > 200) & (a[:, :, 1] < 80) & (a[:, :, 2] < 80) & (a[:, :, 3] > 100)).sum())
    if red > 100:
        raise SystemExit(f"REFUSED: plate carries {red} red debug-label pixels. Use a clean plate.")
    alpha = plate.split()[3]
    # feather edge 1px
    alpha_f = alpha.filter(ImageFilter.GaussianBlur(1))
    plate_f = plate.copy(); plate_f.putalpha(alpha_f)
    W, H = plate.size
    # silhouette bbox
    ys, xs = np.where(np.array(alpha_f) > 10)
    xmin, xmax, ymin, ymax = xs.min(), xs.max(), ys.min(), ys.max()
    # lit-side gradient: 1.0 at left edge -> 0.3 at right edge
    gx = np.linspace(1.0, 0.3, W)[None, :].repeat(H, axis=0)
    for colored in (True, False):
        tag = "colored" if colored else "noncolored"
        rim_col = np.array([0, 200, 255], dtype=float) if colored else np.array([255, 255, 255], dtype=float)
        bleed_col = np.array([255, 120, 0], dtype=float) if colored else np.array([255, 255, 255], dtype=float)
        gain = np.array([1.10, 0.95, 0.70]) if colored else np.array([1.0, 1.0, 1.0])
        # 1. graded base
        rgb = np.array(plate_f.convert("RGB")).astype(float) * gain
        base = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
        base.putalpha(alpha_f)
        # 2. shadow: soft ellipse + foot pads
        shadow = Image.new("RGBA", plate.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(shadow)
        cx = (xmin + xmax) // 2
        d.ellipse([cx - (xmax - xmin) // 3, ymax - 10, cx + (xmax - xmin) // 3, ymax + 50], fill=(40, 40, 90, 110))
        # foot pads: bottom-most alpha in left/right halves
        for half in (0, 1):
            x0 = xmin if half == 0 else cx; x1 = cx if half == 0 else xmax
            sub = np.array(alpha_f)[ymin:ymax+1, x0:x1+1] > 10
            if sub.any():
                rows = np.where(sub.any(axis=1))[0]
                foot_y = ymin + rows.max()
                cols = np.where(sub[rows.max()])[0]
                foot_x = x0 + int(cols.mean())
                d.ellipse([foot_x - 55, foot_y - 8, foot_x + 55, foot_y + 22], fill=(20, 20, 50, 140))
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        # 3. rim directional
        dil3 = alpha_f.filter(ImageFilter.MaxFilter(7))
        rim_a = np.array(ImageChops.subtract(dil3, alpha_f)).astype(float) / 255.0
        rim_a = rim_a * gx
        rim_a = np.array(Image.fromarray((np.clip(rim_a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(float) / 255.0
        rim = np.zeros((H, W, 4), dtype=np.uint8)
        rim[:, :, 0:3] = rim_col.astype(np.uint8); rim[:, :, 3] = (rim_a * 255).astype(np.uint8)
        rim_img = Image.fromarray(rim, "RGBA")
        # 4. bleed falloff
        dil8 = alpha_f.filter(ImageFilter.MaxFilter(11))
        bleed_a = np.array(ImageChops.subtract(dil8, alpha_f)).astype(float) / 255.0
        bleed_a = bleed_a * gx * 0.20
        bleed_a = np.array(Image.fromarray((np.clip(bleed_a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(float) / 255.0
        bleed = np.zeros((H, W, 4), dtype=np.uint8)
        bleed[:, :, 0:3] = bleed_col.astype(np.uint8); bleed[:, :, 3] = (bleed_a * 255).astype(np.uint8)
        bleed_img = Image.fromarray(bleed, "RGBA")
        # 5. internal line light: dark pixels in 12px inner band, lit side
        ero = alpha_f.filter(ImageFilter.MinFilter(25))
        inner_band = np.array(ImageChops.subtract(alpha_f, ero)).astype(float) / 255.0
        rgb_arr = np.array(base.convert("RGB")).astype(float)
        dark = (rgb_arr.sum(axis=2) < 180) & (np.array(alpha_f) > 100)
        w = inner_band * gx * 0.5
        lit = rgb_arr.copy()
        for c in range(3):
            lit[:, :, c] = rgb_arr[:, :, c] * (1 - w * dark) + rim_col[c] * (w * dark)
        internal = Image.fromarray(np.clip(lit, 0, 255).astype(np.uint8)).convert("RGBA")
        internal.putalpha(alpha_f)
        # composite in order: graded base -> shadow (under) -> rim -> bleed -> internal (on top of base only, so composite internal over graded, then add rim/bleed/shadow)
        # shadow goes UNDER the character: start with shadow, then base, then internal tint is already in a full image — blend internal only where dark+band, else base:
        comp = Image.new("RGBA", plate.size, (0, 0, 0, 0))
        comp = Image.alpha_composite(comp, shadow)
        # internal image = base with tinted dark lines; use it as the character layer
        comp = Image.alpha_composite(comp, internal)
        comp = Image.alpha_composite(comp, bleed_img)
        comp = Image.alpha_composite(comp, rim_img)
        comp.save(os.path.join(outdir, f"level-2-v2-{tag}.png"))
        for nm, img in [("shadow", shadow), ("rim", rim_img), ("bleed", bleed_img), ("internal", internal)]:
            img.save(os.path.join(outdir, f"pass-{nm}-{tag}.png"))
        print(f"level-2-v2-{tag} done, rim max {rim_a.max():.2f}, bleed max {bleed_a.max():.2f}")

if __name__ == "__main__":
    main()
