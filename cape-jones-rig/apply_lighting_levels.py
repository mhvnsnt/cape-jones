#!/usr/bin/env python3
"""Pass-based lighting levels 0-5, free stack (PIL only).
Input: a transparent PNG character plate (alpha = silhouette).
Output: <outdir>/level-<n>-<colored|noncolored>.png plus separate pass PNGs
(shadow, rim, bleed, volume, emission, finishing) so each pass can be tuned
without re-rendering — the AOV idea, rebuilt free, no proprietary code.
Rules: base art is never recoloured; rim outer-only 2-4px; bleed edge-band only;
god rays only at Level 3+. Usage: python3 apply_lighting_levels.py PLATE.PNG OUTDIR
"""
import sys, os
from PIL import Image, ImageFilter, ImageDraw, ImageChops

def rim_pass(alpha, px, colour):
    dil = alpha.filter(ImageFilter.MaxFilter(px*2+1))
    rim = ImageChops.subtract(dil, alpha)
    out = Image.new("RGBA", alpha.size, colour+(0,))
    out.putalpha(rim)
    return out

def main():
    plate_path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    plate = Image.open(plate_path).convert("RGBA")
    alpha = plate.split()[3]
    W, H = plate.size
    for colored in (True, False):
        tag = "colored" if colored else "noncolored"
        rim_col = (0, 200, 255) if colored else (255, 255, 255)
        bleed_col = (255, 120, 0) if colored else (255, 255, 255)
        # passes
        shadow = plate.copy()
        # ground-flattened shadow: squash silhouette to 25% height, lay at feet
        sil = Image.new("RGBA", plate.size, (20, 20, 60, 110))
        sil.putalpha(alpha)
        squashed = sil.resize((W, max(1, H//4)))
        shadow_img = Image.new("RGBA", plate.size, (0, 0, 0, 0))
        shadow_img.paste(squashed, (0, H - H//4))
        rim = rim_pass(alpha, 3, rim_col)
        bleed = rim_pass(alpha, 8, bleed_col)
        bleed = Image.blend(Image.new("RGBA", plate.size, (0, 0, 0, 0)), bleed, 0.35)
        vol = Image.new("RGBA", plate.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(vol)
        for x in range(0, W, 120):
            col = (255, 200, 120, 45) if colored else (255, 255, 255, 45)
            d.polygon([(x, 0), (x+40, 0), (x+90, H), (x+30, H)], fill=col)
        emis = plate.filter(ImageFilter.GaussianBlur(6))
        fin = Image.new("RGBA", plate.size, (0, 0, 0, 0))
        passes = {"shadow": shadow_img, "rim": rim, "bleed": bleed, "volume": vol, "emission": emis}
        for name, img in passes.items():
            img.save(os.path.join(outdir, f"pass-{name}-{tag}.png"))
        for level in range(6):
            comp = plate.copy()
            if level >= 2:
                comp = Image.alpha_composite(comp, shadow_img)
                comp = Image.alpha_composite(comp, rim)
                comp = Image.alpha_composite(comp, bleed)
            if level >= 3:
                comp = Image.alpha_composite(comp, vol)
            if level >= 4:
                comp = Image.alpha_composite(comp, emis)
            if level >= 5:
                # finishing: vignette only (grain omitted on transparent plate)
                vig = Image.new("L", plate.size, 0)
                dv = ImageDraw.Draw(vig)
                dv.ellipse([-W//4, -H//4, W+W//4, H+H//4], fill=255)
                vig = vig.filter(ImageFilter.GaussianBlur(80))
                dark = Image.new("RGBA", plate.size, (0, 0, 0, 60))
                dark.putalpha(ImageChops.invert(vig))
                comp = Image.alpha_composite(comp, dark)
            comp.save(os.path.join(outdir, f"level-{level}-{tag}.png"))
    print(f"levels 0-5 x colored/noncolored written to {outdir}")

if __name__ == "__main__":
    main()
