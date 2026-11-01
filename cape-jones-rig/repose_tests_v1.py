"""Repose tests v1 from locked v8 pieces, 2026-10-31.
Not final animation. Each pose reuses v8 pieces, rotated/moved only.
Canvas 1100x1500, grey 128, scale 0.95 (neck 1.05).
PIL rotate(angle) is counter-clockwise in image space as displayed.
"""
from PIL import Image
import os
BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
OUT = "/home/hatch/workspace/cape-jones-rig/reposes"
os.makedirs(OUT, exist_ok=True)

def load(n, scale=0.95):
    im = Image.open(os.path.join(BASE, n)).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)

def arm_left(extra=0):
    # v8 left arm: flip, rot+90, flip -> horizontal, pads top, pointing left
    a = load("Arm_Front.png")
    a = a.transpose(Image.FLIP_TOP_BOTTOM).rotate(90, expand=True)
    a = a.transpose(Image.FLIP_TOP_BOTTOM)
    return a.rotate(extra, expand=True) if extra else a

def arm_right(extra=0):
    a = load("Arm_Front.png")
    a = a.rotate(90, expand=True)
    a = a.transpose(Image.FLIP_TOP_BOTTOM)
    return a.rotate(extra, expand=True) if extra else a

def compose(name, cfg):
    canvas = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
    def paste(im, cx, top):
        canvas.paste(im, (int(cx-im.size[0]/2), int(top)), im)
    paste(load("Cape_Back_Main.png"), 550, cfg.get("cape_top", 410))
    paste(load("Leg_Front.png"), cfg.get("legL_cx", 460), cfg.get("leg_top", 705))
    paste(load("Leg_Back_GRAFTED.png"), cfg.get("legR_cx", 640), cfg.get("leg_top", 705))
    paste(arm_left(cfg.get("armL_rot", 0)), cfg.get("armL_cx", 300), cfg.get("arm_top", 380))
    paste(arm_right(cfg.get("armR_rot", 0)), cfg.get("armR_cx", 800), cfg.get("arm_top", 380))
    paste(load("Pelvis.png"), 550, cfg.get("pelvis_top", 680))
    paste(load("Cape_Collar.png"), 550, cfg.get("collar_top", 370))
    paste(load("Torso_Chest.png"), 550, cfg.get("torso_top", 400))
    paste(load("Belt_Overlay.png"), 550, cfg.get("belt_top", 670))
    paste(load("Neck.png", scale=1.05), 550, cfg.get("neck_top", 360))
    paste(load("Head_Front.png"), 550, cfg.get("head_top", 250))
    canvas.convert("RGB").save(os.path.join(OUT, name))
    print(name, "saved")

# A-pose: arms down-out. From horizontal, rotate left arm -55 (down-left)
# and right arm +55 (down-right) in PIL terms; check visually after.
compose("repose-apose-v1-20261031.png",
        {"armL_rot": 55, "armR_rot": -55, "armL_cx": 360, "armR_cx": 740,
         "legL_cx": 500, "legR_cx": 600})
# Arms-up (was mislabelled as A-pose in first run): fists up-out
compose("repose-armsup-v1-20261031.png",
        {"armL_rot": -55, "armR_rot": 55, "armL_cx": 340, "armR_cx": 760,
         "legL_cx": 500, "legR_cx": 600})
# Flex: arms bent up toward chest. Rotate horizontal arms toward up:
# left arm +55 (up-left), right arm -55 (up-right), fists near chest.
compose("repose-flex-v1-20261031.png",
        {"armL_rot": -55, "armR_rot": 55, "armL_cx": 340, "armR_cx": 760,
         "legL_cx": 480, "legR_cx": 620})
# Dance groove: legs stepped out, arms swinging opposite, torso up 10.
compose("repose-dance-v1-20261031.png",
        {"armL_rot": 30, "armR_rot": -30, "armL_cx": 320, "armR_cx": 780,
         "legL_cx": 420, "legR_cx": 680, "torso_top": 390, "head_top": 240})
# Lounge test (approximate, reclined torso not yet made): legs apart,
# arms relaxed down-out, torso/head slightly lower.
compose("repose-lounge-v1-20261031.png",
        {"armL_rot": -40, "armR_rot": 40, "armL_cx": 340, "armR_cx": 760,
         "legL_cx": 440, "legR_cx": 660, "torso_top": 410, "head_top": 260})
# Punch: right arm straight forward (horizontal, as v8), left arm back,
# legs stepping.
compose("repose-punch-v1-20261031.png",
        {"armL_rot": 20, "armR_rot": 0, "armL_cx": 320, "armR_cx": 800,
         "legL_cx": 420, "legR_cx": 680})
# Jump: arms up, legs tucked (closer together, higher top), torso up.
compose("repose-jump-v1-20261031.png",
        {"armL_rot": 55, "armR_rot": -55, "armL_cx": 360, "armR_cx": 740,
         "legL_cx": 500, "legR_cx": 600, "leg_top": 680,
         "torso_top": 360, "head_top": 210, "neck_top": 320, "pelvis_top": 640, "belt_top": 630})
