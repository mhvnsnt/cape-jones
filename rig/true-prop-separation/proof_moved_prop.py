#!/usr/bin/env python3
"""Moved-prop proof for true prop separation (boards 02-07).

Composite background-complete + all props, with JONES moved FAR from
his original spot (scaled for depth), plus a soft contact shadow
ellipse under him (ADDED for the proof — the extracted shadow stays at
the old spot, which is the honest behaviour: a moved prop carries no
shadow until one is painted). Board 07 ALSO moves the dumpsters /
barriers group (the board's special risk) to the open left foreground.
If the separation were a box crop, the moved figure would carry a
visible rectangle of the old background; a true silhouette carries
only the figure, and the vacated spot reads as clean background.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
TS = f"{WD}/true-sep"
W, H = 2048, 1152

# board: (props kept in place, in order; jones destination (cx, cy, scale);
#         extra group move (layer names, cx, cy, scale) or None)
BOARDS = {
    # Jones 0.5x centred (450,950): open bottom-left asphalt.
    "cj-pl-02": (["cars_left_row", "cars_right_row", "street_lamp_right"],
                 (450, 950, 0.5), None),
    # Jones 0.5x centred (1650,900): open right foreground.
    "cj-pl-03": (["cars_left_row", "cars_right_row",
                  "street_lamp_far", "street_lamp_right"],
                 (1650, 900, 0.5), None),
    # Jones 0.45x centred (1600,850): open right foreground.
    "cj-pl-04": (["cars_right_row", "street_lamp_far"],
                 (1600, 850, 0.45), None),
    # Jones 0.8x centred (350,850): open left lot.
    "cj-pl-05": (["street_lamp_broken"],
                 (350, 850, 0.8), None),
    # Jones 0.5x centred (600,900): open centre-left asphalt.
    "cj-pl-06": (["cars_left_row", "cars_right_row", "street_lamp_broken"],
                 (600, 900, 0.5), None),
    # Jones 0.5x centred (1550,880): open centre-right.
    # Dumpsters group 1.2x centred (400,950): open left foreground.
    "cj-pl-07": (["cars_left_row", "cars_centre", "cars_right_row",
                  "street_lamp_broken"],
                 (1550, 880, 0.5),
                 (["dumpsters", "dumpster_small",
                   "barriers_left", "barriers_centre"], 400, 950, 1.2)),
}


def alpha_bbox(img):
    a = np.asarray(img)[..., 3]
    ys, xs = np.where(a > 10)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def positioned(layer_img, cx, cy, scale, name):
    """Return (canvas, shadow-ellipse box) for layer_img scaled by
    `scale` and centred on (cx, cy). The shadow box sits under the
    moved prop's feet."""
    x0, y0, x1, y1 = alpha_bbox(layer_img)
    crop = layer_img.crop((x0, y0, x1, y1))
    nw, nh = max(1, round((x1 - x0) * scale)), max(1, round((y1 - y0) * scale))
    crop = crop.resize((nw, nh), Image.LANCZOS)
    px, py = cx - nw // 2, cy - nh // 2
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.paste(crop, (px, py))
    sw, sh_h = int(nw * 0.9), max(8, int(nw * 0.10))
    box = [cx - sw // 2, py + nh - 4, cx + sw // 2, py + nh - 4 + sh_h]
    print(f"  moved {name}: bbox {x0},{y0}-{x1},{y1} -> {nw}x{nh} centred ({cx},{cy})")
    return canvas, box


def proof(board):
    props, (jx, jy, js), group = BOARDS[board]
    bdir = f"{TS}/boards/{board}"
    bg = Image.open(f"{bdir}/background-complete.png").convert("RGBA")
    jones = Image.open(f"{bdir}/layers/jones.png").convert("RGBA")
    jcanvas, jbox = positioned(jones, jx, jy, js, "jones")
    gcanvas = gbox = None
    if group:
        names, gx, gy, gs = group
        combo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for name in names:
            combo.alpha_composite(
                Image.open(f"{bdir}/layers/{name}.png").convert("RGBA"))
        gcanvas, gbox = positioned(combo, gx, gy, gs, "+".join(names))
    # Stack: bg + in-place props + soft shadow (ADDED) + moved props.
    comp = bg.copy()
    for name in props:
        comp.alpha_composite(
            Image.open(f"{bdir}/layers/{name}.png").convert("RGBA"))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    d.ellipse(jbox, fill=(0, 0, 0, 110))
    if gbox:
        d.ellipse(gbox, fill=(0, 0, 0, 110))
    comp.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(12)))
    comp.alpha_composite(jcanvas)
    if gcanvas:
        comp.alpha_composite(gcanvas)
    out = f"{bdir}/proof-moved-jones.png"
    comp.convert("RGB").save(out)
    print(f"saved {out} (soft contact shadow ADDED under the moved prop)")


if __name__ == "__main__":
    import sys
    for b in sys.argv[1:] or list(BOARDS):
        print("=====", b)
        proof(b)
