#!/usr/bin/env python3
"""Build the TRUE-prop-separation layered PSDs (v2) for PURPLE LOT.

Replaces the v1 box-cut PSD (torbox-pulls/free-proof/purple-lot-layered.psd,
PR #443) with layers cut along the art's own edges:
  background  background-complete.png (props removed, holes rebuilt)
  props       silhouette RGBA layers (grabCut / traced, alpha = the art's
              own edge, never a box)
  character   jones (board 01 only)
  shadows     car_shadows.png (extracted MULTIPLY, not the v1 soft ellipse)
  light/grade REUSED from v1 (synthetic radials / solids / noise — full
              frame, no box cuts): sodium visible, purple hidden (toggle)

Rest match (light/grade OFF): bg+props+shadows vs original = 0.49 (plate),
0.16 (board 01). The full PSD sodium composite adds the v1 light/grade
layers on top of the baked plate, exactly as v1 did (v1 diff 8.26) — the
light layers are the sodium->purple toggle, not a redraw.
"""
import os
import shutil
import numpy as np
from PIL import Image
from psd_tools import PSDImage
from psd_tools.constants import BlendMode

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
TS = os.path.join(WD, "true-sep")
V1L = os.path.join(TS, "light")  # shared light/grade layers (v1 synthetics)
W, H = 2048, 1152

LIGHT_GRADE = [
    # (filename, layer name, group, blend, opacity, visible)
    ("lamp_glow_sodium.png", "lamp glow sodium", "light", BlendMode.SCREEN, 255, True),
    ("lamp_glow_purple.png", "lamp glow purple", "light", BlendMode.SCREEN, 255, False),
    ("light_pool_sodium.png", "light pool sodium", "light", BlendMode.SCREEN, 255, True),
    ("light_pool_purple.png", "light pool purple", "light", BlendMode.SCREEN, 255, False),
    ("light_sodium.png", "light sodium", "grade", BlendMode.COLOR, 255, True),
    ("light_purple.png", "light purple", "grade", BlendMode.COLOR, 255, False),
    ("dusty_air.png", "dusty air", "grade", BlendMode.SCREEN, 255, True),
    ("vignette.png", "vignette", "grade", BlendMode.OVERLAY, 50, True),
    ("grain.png", "grain", "grade", BlendMode.OVERLAY, 255, True),
]


def build(board_dir, psd_path, orig_path, prop_names, char_name=None):
    layers = []
    bg = Image.open(os.path.join(board_dir, "background-complete.png")).convert("RGBA")
    layers.append(("background", "background complete", bg, BlendMode.NORMAL, 255, True))
    for name in prop_names:
        img = Image.open(os.path.join(board_dir, "layers", name + ".png")).convert("RGBA")
        layers.append(("props", name.replace("_", " "), img, BlendMode.NORMAL, 255, True))
    if char_name:
        img = Image.open(os.path.join(board_dir, "layers", char_name + ".png")).convert("RGBA")
        layers.append(("character", char_name, img, BlendMode.NORMAL, 255, True))
    sh = Image.open(os.path.join(board_dir, "layers", "car_shadows.png")).convert("RGBA")
    layers.append(("shadows", "car shadows", sh, BlendMode.MULTIPLY, 255, True))
    for fname, name, group, blend, op, vis in LIGHT_GRADE:
        img = Image.open(os.path.join(V1L, fname)).convert("RGBA")
        layers.append((group, name, img, blend, op, vis))

    psd = PSDImage.new("RGB", (W, H), depth=8)
    groups = {}
    for gname, name, img, blend, op, vis in layers:
        g = groups.get(gname)
        if g is None:
            g = psd.create_group(name=gname)
            groups[gname] = g
        layer = g.create_pixel_layer(img, name=name, opacity=op, blend_mode=blend)
        layer.visible = vis
    psd.save(psd_path)
    print(f"saved {psd_path} bytes={os.path.getsize(psd_path)}")

    psd2 = PSDImage.open(psd_path)
    def walk(l, d=0):
        print("  " * d + f"{'GROUP' if l.is_group() else 'LAYER'} {l.name!r} blend={l.blend_mode} op={l.opacity} vis={l.visible}")
        if l.is_group():
            for c in l:
                walk(c, d + 1)
    for l in psd2:
        walk(l)
    orig = np.asarray(Image.open(orig_path).convert("RGB")).astype(np.float32)
    comp = np.asarray(psd2.composite().convert("RGB")).astype(np.float32)
    print("  sodium composite vs original: mean abs diff",
          float(np.abs(comp - orig).mean()))
    Image.fromarray(comp.astype(np.uint8)).save(
        os.path.join(board_dir, "composite-sodium.png"))
    for l in psd2.descendants():
        if l.name in ("light sodium", "lamp glow sodium", "light pool sodium"):
            l.visible = False
        if l.name in ("light purple", "lamp glow purple", "light pool purple"):
            l.visible = True
    comp2 = np.asarray(psd2.composite().convert("RGB")).astype(np.float32)
    Image.fromarray(comp2.astype(np.uint8)).save(
        os.path.join(board_dir, "composite-purple.png"))
    print("  purple composite saved (toggle check)")


if __name__ == "__main__":
    build(os.path.join(TS, "plate"),
          os.path.join(TS, "plate", "purple-lot-layered-v2.psd"),
          f"{WD}/rig/plate-sodium.png",
          ["cars_left_row", "blue_car_mid", "cars_right_row",
           "stop_sign", "street_lamp_right", "street_lamp_far"])
    build(os.path.join(TS, "boards", "cj-pl-01"),
          os.path.join(TS, "boards", "cj-pl-01", "cj-pl-01-layered-v2.psd"),
          f"{WD}/repo/production/2d-parking-lot/boards/cj-pl-01.png",
          ["cars_left_row", "blue_car_mid", "cars_right_row",
           "stop_sign", "street_lamp_right", "street_lamp_far"],
          char_name="jones")
