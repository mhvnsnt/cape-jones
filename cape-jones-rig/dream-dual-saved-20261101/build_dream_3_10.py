"""Dream 3-10 builder: same nearest-base-colour method as jojo-shift-variation build_variation.py.
Base plate: rig-apose-v7c-clean-transparent.png. Black outline never reassigned (dist>110 untouched).
Rim: dilate(alpha,6)-alpha, in rim colour, plate pasted AFTER rim, interior preserved 100% (gold-split rim method)."""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "/home/hatch/workspace/cape-jones-rig/dream-dual-saved-20261101"
PLATE = "/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png"
BASE = {
    "cowl": (90, 39, 114), "skin": (239, 175, 131), "suit": (255, 255, 255),
    "suit_shadow": (178, 186, 199), "cape": (23, 21, 26), "outline": (0, 0, 0),
}
DREAMS = {
 3: {"name":"Dream 3 — Cyan Cape", "cowl":(255,60,180), "skin":(255,200,180), "suit":(255,255,255), "suit_shadow":(178,186,199), "cape":(0,200,255), "rim":(0,200,255)},
 4: {"name":"Dream 4 — Red Cape, Violet Helm", "cowl":(140,80,220), "skin":(255,200,180), "suit":(200,210,220), "suit_shadow":(150,160,175), "cape":(255,60,60), "rim":(255,60,60)},
 5: {"name":"Dream 5 — Green Cape, Orange Helm", "cowl":(255,140,40), "skin":(255,200,180), "suit":(255,255,255), "suit_shadow":(178,186,199), "cape":(60,220,120), "rim":(60,220,120)},
 6: {"name":"Dream 6 — Purple Cape, Gold Suit", "cowl":(40,200,210), "skin":(255,200,180), "suit":(255,205,90), "suit_shadow":(200,150,70), "cape":(140,60,255), "rim":(140,60,255)},
 7: {"name":"Dream 7 — White Cape, Black Suit", "cowl":(255,60,180), "skin":(255,200,180), "suit":(20,20,30), "suit_shadow":(60,60,75), "cape":(255,255,255), "rim":(255,255,255)},
 8: {"name":"Dream 8 — Teal Cape, Lavender Suit", "cowl":(255,205,90), "skin":(255,200,180), "suit":(200,180,255), "suit_shadow":(160,140,210), "cape":(0,180,180), "rim":(0,180,180)},
 9: {"name":"Dream 9 — Orange Cape, Blue Helm", "cowl":(40,100,255), "skin":(255,200,180), "suit":(255,255,255), "suit_shadow":(178,186,199), "cape":(255,120,40), "rim":(255,120,40)},
 10: {"name":"Dream 10 — Light Pink Cape, Cyan Suit", "cowl":(60,220,120), "skin":(255,200,180), "suit":(180,240,255), "suit_shadow":(140,190,210), "cape":(255,120,220), "rim":(255,120,220)},
}
plate = Image.open(PLATE).convert("RGBA")
arr = np.array(plate).astype(np.int32)
rgb, alpha = arr[:,:,:3], arr[:,:,3]
base_names = list(BASE.keys())
base_arr = np.array([BASE[n] for n in base_names], dtype=np.int32)
# nearest base per pixel (vectorised, chunked by rows to limit memory)
idx = np.zeros(rgb.shape[:2], dtype=np.int8)
mind = np.full(rgb.shape[:2], 1e9)
for i, bc in enumerate(base_arr):
    d = np.sum((rgb - bc)**2, axis=2)
    better = d < mind
    mind[better] = d[better]; idx[better] = i
mind_sqrt = np.sqrt(mind)
results = {}
for n, spec in DREAMS.items():
    mapping = np.array([spec[k] if k in spec else BASE[k] for k in base_names], dtype=np.int32)
    delta = mapping - base_arr
    out_rgb = np.clip(rgb + delta[idx], 0, 255).astype(np.uint8)
    # outline: dist>110 untouched -> restore original rgb where mind_sqrt>110
    keep = mind_sqrt > 110
    out_rgb[keep] = rgb[keep].astype(np.uint8)
    img = Image.fromarray(np.dstack([out_rgb, alpha.astype(np.uint8)]), "RGBA")
    # thin 6px rim in rim colour, plate after rim
    a = img.split()[3]
    dil = a.filter(ImageFilter.MaxFilter(13))
    rim_mask = Image.new("L", img.size, 0)
    import numpy as _np
    rim_np = (_np.array(dil) > 0) & (_np.array(a) == 0)
    rim_img = Image.new("RGBA", img.size, spec["rim"] + (255,))
    canvas = Image.new("RGBA", img.size, (0,0,0,0))
    canvas.paste(rim_img, (0,0), Image.fromarray((rim_np*255).astype(np.uint8)))
    canvas.alpha_composite(img)
    d = os.path.join(OUT, "presets", f"dream-{n}")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"dream-{n}-20261101.png")
    canvas.save(p)
    spec_out = {"preset": f"Dream {n}", "name": spec["name"], "status": "PRESET, approval 0/1 separately",
                "cape": spec["cape"], "cowl_helm": spec["cowl"], "suit": spec["suit"],
                "suit_shadow": spec["suit_shadow"], "skin": spec["skin"], "rim_6px": spec["rim"],
                "method": "nearest-base-colour recolour, dist>110 untouched, outline never reassigned; rim dilate(6)-alpha, plate after rim",
                "source_base": "rig-apose-v7c-clean-transparent.png", "size": list(canvas.size)}
    json.dump(spec_out, open(os.path.join(d, "PRESET.json"), "w"), indent=2)
    results[n] = {"file": p, "size": list(canvas.size), "spec": spec_out}
    print("saved", n, p, canvas.size)
json.dump(results, open(os.path.join(OUT, "dream-3-10-measurements.json"), "w"), indent=2)
# contact Dream 3-10, 4x2 on grey, labels
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except Exception:
    font = small = ImageFont.load_default()
TW, TH, GAP = 340, 500, 20
sheet = Image.new("RGB", (GAP + 4*(TW+GAP), GAP + 2*(TH+40+GAP)), (128,128,128))
dr = ImageDraw.Draw(sheet)
for i, n in enumerate(range(3, 11)):
    img = Image.open(results[n]["file"])
    thumb = img.copy(); thumb.thumbnail((TW, TH), Image.LANCZOS)
    x = GAP + (i % 4)*(TW+GAP); y = GAP + (i // 4)*(TH+40+GAP)
    bg = Image.new("RGBA", (TW, TH), (128,128,128,255))
    bg.alpha_composite(thumb, ((TW-thumb.width)//2, (TH-thumb.height)//2))
    sheet.paste(bg.convert("RGB"), (x, y))
    dr.text((x, y+TH+5), DREAMS[n]["name"], fill=(255,255,255), font=small)
sheet.save(os.path.join(OUT, "contacts", "dream-3-to-10-contact-20261101.png"))
print("contact", sheet.size)
