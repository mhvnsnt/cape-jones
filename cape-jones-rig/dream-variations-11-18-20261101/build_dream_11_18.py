"""Dream 11-18 builder: same method as dream-dual-saved-20261101/build_dream_3_10.py.
Base: rig-apose-v7c-clean-transparent.png, int32 distances, dist>110 untouched,
black outline never reassigned. Difference vs Dream 3-10: rim is its OWN colour
in every variation here, not a copy of the cape colour, so cowl/suit/cape/rim/skin
are each coloured independently. Eye note: the base plate has no separate eye
colour class in this method (white eye pixels sit in the suit-white class), so
eyes follow the suit class; skin is varied independently per variation."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "/home/hatch/workspace/cape-jones-rig/dream-variations-11-18-20261101"
PLATE = "/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png"
BASE = {
    "cowl": (90, 39, 114), "skin": (239, 175, 131), "suit": (255, 255, 255),
    "suit_shadow": (178, 186, 199), "cape": (23, 21, 26), "outline": (0, 0, 0),
}
# Each variation: cowl, suit, cape, rim all different from each other; skin varied too.
DREAMS = {
 11: {"name": "Dream 11 — Lime Helm, Coral Suit, Navy Cape, Gold Rim",
      "cowl": (180, 255, 60), "skin": (255, 220, 200), "suit": (255, 120, 120), "cape": (30, 30, 180), "rim": (255, 215, 0)},
 12: {"name": "Dream 12 — Cyan Helm, Magenta Suit, Forest Cape, Orange Rim",
      "cowl": (0, 220, 220), "skin": (240, 180, 150), "suit": (255, 80, 200), "cape": (20, 140, 60), "rim": (255, 150, 0)},
 13: {"name": "Dream 13 — Red Helm, Teal Suit, Yellow Cape, Purple Rim",
      "cowl": (220, 30, 30), "skin": (255, 200, 180), "suit": (0, 160, 160), "cape": (255, 230, 0), "rim": (150, 0, 255)},
 14: {"name": "Dream 14 — Gold Helm, Navy Suit, Pink Cape, Green Rim",
      "cowl": (255, 200, 0), "skin": (230, 170, 140), "suit": (25, 25, 120), "cape": (255, 100, 180), "rim": (0, 220, 100)},
 15: {"name": "Dream 15 — Violet Helm, Orange Suit, Silver Cape, Cyan Rim",
      "cowl": (130, 0, 220), "skin": (255, 210, 190), "suit": (255, 140, 0), "cape": (200, 205, 215), "rim": (0, 180, 255)},
 16: {"name": "Dream 16 — Deep Blue Helm, Lime Suit, Crimson Cape, White Rim",
      "cowl": (0, 60, 180), "skin": (245, 190, 165), "suit": (170, 255, 80), "cape": (200, 0, 80), "rim": (255, 255, 255)},
 17: {"name": "Dream 17 — Pink Helm, Purple Suit, Teal-Green Cape, Red Rim",
      "cowl": (255, 130, 200), "skin": (255, 225, 205), "suit": (120, 60, 200), "cape": (0, 200, 140), "rim": (255, 40, 40)},
 18: {"name": "Dream 18 — Orange-Red Helm, Sky Suit, Charcoal-Purple Cape, Lime Rim",
      "cowl": (255, 80, 0), "skin": (235, 175, 145), "suit": (120, 200, 255), "cape": (70, 40, 110), "rim": (140, 255, 0)},
}
for spec in DREAMS.values():
    # suit_shadow: darker suit, same hue family, computed not hand-picked
    spec["suit_shadow"] = tuple(int(c * 0.78) for c in spec["suit"])

plate = Image.open(PLATE).convert("RGBA")
arr = np.array(plate).astype(np.int32)
rgb, alpha = arr[:, :, :3], arr[:, :, 3]
base_names = list(BASE.keys())
base_arr = np.array([BASE[n] for n in base_names], dtype=np.int32)
idx = np.zeros(rgb.shape[:2], dtype=np.int8)
mind = np.full(rgb.shape[:2], 1e9)
for i, bc in enumerate(base_arr):
    d = np.sum((rgb - bc) ** 2, axis=2)
    better = d < mind
    mind[better] = d[better]
    idx[better] = i
mind_sqrt = np.sqrt(mind)
base_alpha_count = int((alpha > 0).sum())
results = {}
for n, spec in DREAMS.items():
    mapping = np.array([spec[k] if k in spec else BASE[k] for k in base_names], dtype=np.int32)
    delta = mapping - base_arr
    out_rgb = np.clip(rgb + delta[idx], 0, 255).astype(np.uint8)
    keep = mind_sqrt > 110
    out_rgb[keep] = rgb[keep].astype(np.uint8)
    img = Image.fromarray(np.dstack([out_rgb, alpha.astype(np.uint8)]), "RGBA")
    a = img.split()[3]
    dil = a.filter(ImageFilter.MaxFilter(13))
    rim_np = (np.array(dil) > 0) & (np.array(a) == 0)
    rim_img = Image.new("RGBA", img.size, spec["rim"] + (255,))
    canvas = Image.new("RGBA", img.size, (0, 0, 0, 0))
    canvas.paste(rim_img, (0, 0), Image.fromarray((rim_np * 255).astype(np.uint8)))
    canvas.alpha_composite(img)
    # gates: alpha unchanged by recolour (rim adds only outside figure alpha)
    fig_alpha = int((np.array(canvas.split()[3]) > 0).sum())
    interior = Image.fromarray(np.dstack([out_rgb, alpha.astype(np.uint8)]), "RGBA")
    assert np.array_equal(np.array(interior.split()[3]), alpha), "interior alpha changed"
    d = os.path.join(OUT, "presets", f"dream-{n}")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"dream-{n}-20261101.png")
    canvas.save(p)
    spec_out = {"preset": f"Dream {n}", "name": spec["name"], "status": "PRESET, approval 0/1 separately",
                "cowl_helm": spec["cowl"], "skin": spec["skin"], "suit": spec["suit"],
                "suit_shadow": spec["suit_shadow"], "cape": spec["cape"], "rim_6px": spec["rim"],
                "rim_note": "rim is its OWN colour here, not a copy of the cape colour",
                "eye_note": "no separate eye class in this method; white eye pixels sit in the suit-white class, so eyes follow the suit class",
                "method": "nearest-base-colour recolour, int32, dist>110 untouched, outline never reassigned; rim dilate(6)-alpha, plate after rim, interior preserved 100%",
                "source_base": "rig-apose-v7c-clean-transparent.png", "size": list(canvas.size),
                "base_alpha_px": base_alpha_count, "canvas_alpha_px": fig_alpha}
    json.dump(spec_out, open(os.path.join(d, "PRESET.json"), "w"), indent=2)
    results[n] = {"file": p, "size": list(canvas.size), "spec": spec_out}
    print("saved", n, p, canvas.size, "alpha", fig_alpha)

json.dump(results, open(os.path.join(OUT, "dream-11-18-measurements.json"), "w"), indent=2)
# contact 4x2
try:
    small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except Exception:
    small = ImageFont.load_default()
TW, TH, GAP = 340, 500, 20
sheet = Image.new("RGB", (GAP + 4 * (TW + GAP), GAP + 2 * (TH + 40 + GAP)), (128, 128, 128))
dr = ImageDraw.Draw(sheet)
for i, n in enumerate(range(11, 19)):
    img = Image.open(results[n]["file"])
    thumb = img.copy()
    thumb.thumbnail((TW, TH), Image.LANCZOS)
    x = GAP + (i % 4) * (TW + GAP)
    y = GAP + (i // 4) * (TH + 40 + GAP)
    bg = Image.new("RGBA", (TW, TH), (128, 128, 128, 255))
    bg.alpha_composite(thumb, ((TW - thumb.width) // 2, (TH - thumb.height) // 2))
    sheet.paste(bg.convert("RGB"), (x, y))
    dr.text((x, y + TH + 5), DREAMS[n]["name"], fill=(255, 255, 255), font=small)
sheet.save(os.path.join(OUT, "contacts", "dream-11-to-18-contact-20261101.png"))
print("contact", sheet.size)
