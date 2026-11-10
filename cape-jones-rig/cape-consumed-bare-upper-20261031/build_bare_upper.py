"""Cape Consumed: BARE vs UPPER-ONLY versions. Mars 2026-10-31 21:39 CDT.
FUTURE ONLY, NOT V2, NOT canon. No repo push. No existing file overwritten.
Upper cape part = COLLAR piece Cape_Collar.png (360x185 original).
Lower cape part = BACK piece Cape_Back_Main.png (490x833 original).
BARE: both pieces omitted. UPPER-ONLY: collar only, back still omitted.
Reuses the v7c stack builder from the capeless build (build_base.py),
patched only to take cape_mode instead of a cape boolean.
"""
import os, json, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_base import build, blacken, apply_symbol, bbox, APOSE

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "cape-consumed-bare-upper-20261031")
os.makedirs(OUT, exist_ok=True)

def grey(im, path):
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(path)

def alpha(im):
    return int((np.asarray(im)[..., 3] > 10).sum())

results = {}
renders = {}
for mode, label in (("none", "bare"), ("collar", "upper_only")):
    raw, _, _ = build(APOSE, cape_mode=mode)
    black, mask = blacken(raw)
    final, sym = apply_symbol(black, mask)
    renders[label] = final
    results[label] = {
        "cape_mode": mode,
        "cape_back_main_present": False,
        "cape_collar_present": mode == "collar",
        "alpha_px": alpha(final),
        "bbox": bbox(final),
        "symbol_white_px": sym,
        "body_colour": (18, 18, 22),
        "symbol_colour": (255, 255, 255),
    }
    final.save(os.path.join(OUT, f"cape-consumed-{label}-20261031.png"))
    grey(final, os.path.join(OUT, f"cape-consumed-{label}-20261031-on-grey.png"))
    print(label, results[label])

# Reference: rebuilt with-cape stack from the earlier capeless build
results["reference_rebuilt_with_cape"] = {
    "cape_back_main_present": True, "cape_collar_present": True,
    "alpha_px": 374816, "bbox": [248, 254, 876, 1295],
    "symbol_white_px": 1524, "source": "future-symbiote-capeless-white-outline-20261031 measurements",
}
bare = np.asarray(renders["bare"])[..., 3] > 10
upper = np.asarray(renders["upper_only"])[..., 3] > 10
results["upper_only_vs_bare"] = {
    "visible_collar_px_added": int((upper & ~bare).sum()),
    "pixels_removed_vs_bare": int((bare & ~upper).sum()),
    "note": "Visible collar pixels = alpha present in upper-only but not in bare. "
            "The collar sits behind torso/neck, so only its visible fringe counts here; "
            "the full collar piece is 360x185 original (342x176 at 0.95 build scale).",
}
# Piece original sizes, measured from sliced/
from PIL import Image as _I
for piece in ("Cape_Collar.png", "Cape_Back_Main.png"):
    im = _I.open(os.path.join(ROOT, "sliced", piece))
    results.setdefault("piece_original_sizes", {})[piece] = list(im.size)
print(json.dumps(results, indent=2))

# Contact: bare left, upper-only right, with labels
def tile(im, tw=400):
    bg = Image.new("RGBA", (tw, int(tw * 1500 / 1100)), (128, 128, 128, 255))
    bg.alpha_composite(im.resize((tw, int(tw * 1500 / 1100))))
    return bg

tw = 400
th = int(tw * 1500 / 1100)
sheet = Image.new("RGBA", (tw * 2, th + 60), (0, 0, 0, 255))
d = ImageDraw.Draw(sheet)
for i, (label, key) in enumerate((("1 BARE — no cape at all", "bare"),
                                  ("2 UPPER-ONLY — collar only, no back", "upper_only"))):
    sheet.alpha_composite(tile(renders[key], tw), (i * tw, 0))
    d.text((i * tw + 4, th + 4), label, fill=(255, 255, 0))
sheet.convert("RGB").save(os.path.join(OUT, "cape-consumed-bare-upper-contact-20261031.png"))

with open(os.path.join(OUT, "measurements-20261031.json"), "w") as f:
    json.dump(results, f, indent=2)
print("done")
