"""Repose v2: cut-limb pivots, not whole-arm rotation.
Layer rotate around a joint point (PIL rotate center=).
Upper arm: vertical piece, top=shoulder, bottom=elbow (~290px unscaled).
Lower arm: vertical piece, top=elbow, bottom=wrist.
Angles: PIL rotate is counter-clockwise as displayed.
For a screen-right arm, upper pointing down-out = rotate -30 (clockwise).
Flex: forearm bent up toward chest = rotate lower +110 from upper direction.
"""
from PIL import Image
import os, math
BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs"
OUT = "/home/hatch/workspace/cape-jones-rig/reposes"
SCALE = 0.95

def load(path, scale=SCALE):
    im = Image.open(path).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)

def paste_at(canvas, im, cx, top):
    canvas.paste(im, (int(cx-im.size[0]/2), int(top)), im)

def limb_layer(im, pivot, angle, paste_cx, paste_top):
    """Return a full-canvas layer with im pasted, rotated around pivot."""
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(paste_cx-im.size[0]/2), int(paste_top)), im)
    return layer.rotate(angle, center=pivot, expand=False)

def rotate_vec(dx, dy, angle_deg):
    """Rotate a vector by PIL angle (counter-clockwise on screen)."""
    a = math.radians(angle_deg)
    # PIL rotate CCW on screen: screen y down, so math sign flips for y
    # Use screen coordinates: x' = x cos - y sin, y' = x sin + y cos with y down = CCW visually? 
    # We will verify visually and flip if needed.
    return (dx*math.cos(a) - dy*math.sin(a), dx*math.sin(a) + dy*math.cos(a))

def build_flex():
    canvas = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
    paste_at(canvas, load(os.path.join(BASE, "Leg_Front.png")), 460, 705)
    paste_at(canvas, load(os.path.join(BASE, "Leg_Back_GRAFTED.png")), 640, 705)
    # Arms via cut limbs, both sides, flex: upper down-out, lower bent up
    for side, shoulder, upper_angle in [("R", (680, 430), -30), ("L", (420, 430), 30)]:
        upper = load(os.path.join(CUT, "Arm_Front_Upper.png"))
        # paste upper with top at shoulder
        layer = limb_layer(upper, shoulder, upper_angle, shoulder[0], shoulder[1])
        canvas.alpha_composite(layer)
        # elbow = shoulder + rotated (0, upper_len) ; upper_len ~ 275 scaled (290*0.95, joint near bottom)
        ex, ey = rotate_vec(0, 275, upper_angle)
        elbow = (shoulder[0]+ex, shoulder[1]+ey)
        lower = load(os.path.join(CUT, "Arm_Front_Lower.png"))
        # lower bend: total angle = upper_angle + bend (bend toward chest = inward)
        bend = -110 if side == "R" else 110
        total = upper_angle + bend
        layer2 = limb_layer(lower, elbow, total, elbow[0], elbow[1])
        canvas.alpha_composite(layer2)
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    canvas.convert("RGB").save(os.path.join(OUT, "repose-flex-v2-20261031.png"))
    print("flex v2 saved")

build_flex()
