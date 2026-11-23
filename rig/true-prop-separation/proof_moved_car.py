#!/usr/bin/env python3
"""Moved-car proof for true prop separation (plate).

Composite the background-complete + all props, with the blue car moved
FAR from its original spot (its bbox 437-667, 542-617 -> centred on the
open sunlit asphalt at ~(1415, 887)), plus a soft contact shadow ellipse
under it (ADDED for the proof — the extracted shadow stays at the old
spot, which is the honest behaviour: a moved prop carries no shadow
until one is painted). If the separation were a box crop, the moved car
would carry a visible rectangle of the old background; a true silhouette
carries only the car.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
TS = f"{WD}/true-sep"
W, H = 2048, 1152

bg = Image.open(f"{TS}/plate/background-complete.png").convert("RGBA")


def paste(base, path, dx=0, dy=0):
    img = Image.open(path).convert("RGBA")
    if dx or dy:
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.paste(img, (dx, dy))
        img = canvas
    base.alpha_composite(img)
    return base


comp = bg.copy()
for name in ["cars_left_row", "cars_right_row", "stop_sign",
             "street_lamp_right", "street_lamp_far"]:
    paste(comp, f"{TS}/plate/layers/{name}.png")

# blue car: original bbox x437-667, y542-617 (centre 552, 580).
# Move it to centre (1415, 887) on the open sunlit asphalt, scaled 1.5x
# (it is closer to camera there, so it reads larger).
car = Image.open(f"{TS}/plate/layers/blue_car_mid.png").convert("RGBA")
car = car.crop((437, 542, 667, 617)).resize((345, 113), Image.LANCZOS)
cx, cy = 1415, 887
car_xy = (cx - 345 // 2, cy - 113 // 2)
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
canvas.paste(car, car_xy)
comp.alpha_composite(canvas)

# soft contact shadow under the moved car (added for the proof)
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(sh)
d.ellipse([cx - 195, cy + 27, cx + 195, cy + 72], fill=(0, 0, 0, 110))
sh = sh.filter(ImageFilter.GaussianBlur(12))
# shadow goes UNDER the car: rebuild with shadow first, car on top
comp2 = bg.copy()
for name in ["cars_left_row", "cars_right_row", "stop_sign",
             "street_lamp_right", "street_lamp_far"]:
    paste(comp2, f"{TS}/plate/layers/{name}.png")
comp2.alpha_composite(sh)
comp2.alpha_composite(canvas)

comp2.convert("RGB").save(f"{TS}/plate/proof-moved-car.png")
print("saved proof-moved-car.png, blue car moved to centre (1415, 887), 1.5x")
print("vacated spot: x437-667, y542-617 (now clean asphalt)")
