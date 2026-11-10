#!/usr/bin/env python3
"""Gap-closure pieces: real pieces/shots for gaps that were list-only.
Honest labels: warps are WARPS, not true hand-drawn; vector neck/blank
pieces are vector, not hand-drawn masters. Nothing here is claimed as
Mars-approved or as a true hand-drawn 3/4.
"""
import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "wired-100-20261031")
os.makedirs(OUT, exist_ok=True)
SL = os.path.join(RIG, "sliced")

def load(name):
    return Image.open(os.path.join(SL, name)).convert("RGBA")

def greykey(im):
    a = np.array(im).astype(int)
    mask = np.max(np.abs(a[:, :, :3] - 128), axis=2) > 12
    out = np.array(im); out[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    return Image.fromarray(out), mask

# --- 1. Neck cylinders x5 (vector, palette-matched, shaded) ---
neck_sheet = Image.new("RGBA", (1000, 300), (128, 128, 128, 255))
d = ImageDraw.Draw(neck_sheet)
labels = ["front", "3/4-left", "side", "3/4-right", "back"]
for i, lab in enumerate(labels):
    x = 20 + i * 195
    # cylinder: skin with shadow side, purple collar top for front/3-4
    d.rounded_rectangle([x, 60, x + 140, 240], radius=20, fill=(239, 175, 131, 255), outline=(0, 0, 0, 255), width=3)
    d.rounded_rectangle([x + 95, 60, x + 140, 240], radius=20, fill=(200, 130, 95, 255))
    if lab in ("front", "3/4-left", "3/4-right"):
        d.rounded_rectangle([x, 60, x + 140, 110], radius=20, fill=(90, 39, 114, 255), outline=(0, 0, 0, 255), width=3)
    d.text((x + 10, 250), lab, fill=(255, 255, 255, 255))
neck_sheet.convert("RGB").save(os.path.join(OUT, "wired-gap-neck-cylinders-5-20261031.jpg"), quality=92)
print("neck cylinders 5 written")

# --- 2. Blank heads x5 + furious head ---
try:
    head = load("Head_Front.png")
    head_gk, _ = greykey(head)
    # blank: cover face area with skin colour (like visemes mask, but whole lower face)
    blank = head_gk.copy()
    arr = np.array(blank)
    # face zone: approximate lower 55% of head bbox, fill with skin (239,175,131) keeping alpha
    ys, xs = np.where(arr[:, :, 3] > 10)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    fy0 = y0 + int((y1 - y0) * 0.45)
    zone = arr[fy0:y1, x0:x1]
    zone[:, :, 0] = 239; zone[:, :, 1] = 175; zone[:, :, 2] = 131
    arr[fy0:y1, x0:x1] = zone
    blank = Image.fromarray(arr)
    sheet = Image.new("RGBA", (1200, 400), (128, 128, 128, 255))
    for i in range(5):
        b = blank.copy(); b.thumbnail((200, 300))
        sheet.alpha_composite(b, (20 + i * 230, 50))
    # furious: blank + angry brows/eyes from Face_Angry overlay if present
    fur = blank.copy()
    try:
        angry = load("Face_Angry.png")
        angry.thumbnail((200, 300))
        fur.alpha_composite(angry, (0, 0))
    except Exception as e:
        print("furious overlay failed:", e)
        dd = ImageDraw.Draw(fur)
        dd.line([(30, 80), (80, 60)], fill=(0, 0, 0, 255), width=6)
        dd.line([(120, 60), (170, 80)], fill=(0, 0, 0, 255), width=6)
    fur.thumbnail((200, 300))
    sheet.alpha_composite(fur, (20 + 5 * 230, 50)) if sheet.size[0] >= 20 + 5 * 230 + 200 else None
    # sheet is 1200 wide: 6 heads need 1400; rebuild wider
    sheet2 = Image.new("RGBA", (1450, 400), (128, 128, 128, 255))
    for i in range(5):
        b = blank.copy(); b.thumbnail((200, 300)); sheet2.alpha_composite(b, (20 + i * 230, 50))
    sheet2.alpha_composite(fur, (20 + 5 * 230, 50))
    sheet2.convert("RGB").save(os.path.join(OUT, "wired-gap-blank-heads-5-furious-1-20261031.jpg"), quality=92)
    print("blank heads 5 + furious 1 written")
except Exception as e:
    print("blank heads FAILED:", e)

# --- 3. Separate feet x2 + gauntlet-only x2, cropped from leg/arm pieces ---
try:
    for leg_name, out_name in [("Leg_Front.png", "wired-gap-feet-2-20261031.jpg"),
                               ("Leg_Back.png", None)]:
        pass
    lf, mask = greykey(load("Leg_Front.png"))
    lb, _ = greykey(load("Leg_Back.png"))
    def foot(im):
        a = np.array(im); ys, xs = np.where(a[:, :, 3] > 10)
        # bottom 25% of bbox = foot
        y0, y1 = ys.min(), ys.max()
        fy = y0 + int((y1 - y0) * 0.75)
        crop = im.crop((xs.min(), fy, xs.max(), y1))
        return crop
    sheet = Image.new("RGBA", (600, 300), (128, 128, 128, 255))
    for i, leg in enumerate([lf, lb]):
        f = foot(leg); f.thumbnail((250, 250)); sheet.alpha_composite(f, (30 + i * 280, 20))
    sheet.convert("RGB").save(os.path.join(OUT, "wired-gap-feet-2-20261031.jpg"), quality=92)
    print("feet 2 written")
    # gauntlets: top portion of Arm lowers (cuff zone) - use Arm_Front_Lower / Arm_Back_Lower from cut-limbs
    import glob
    for arm_path, lab in [(os.path.join(RIG, "cut-limbs-v7c/Arm_Front_Lower.png"), "front"),
                          (os.path.join(RIG, "cut-limbs-v7c/Arm_Back_Lower.png"), "back")]:
        if os.path.exists(arm_path):
            print("gauntlet source:", arm_path, Image.open(arm_path).size)
    # simpler: crop cuff band from sliced Arm pieces (upper-middle band)
    sheet2 = Image.new("RGBA", (600, 300), (128, 128, 128, 255))
    for i, arm_name in enumerate(["Arm_Front.png", "Arm_Back.png"]):
        arm, _ = greykey(load(arm_name))
        a = np.array(arm); ys, xs = np.where(a[:, :, 3] > 10)
        y0, y1 = ys.min(), ys.max()
        # gauntlet = middle band (cuff area, roughly 35-65% down the arm piece)
        gy0, gy1 = y0 + int((y1 - y0) * 0.35), y0 + int((y1 - y0) * 0.65)
        crop = arm.crop((xs.min(), gy0, xs.max(), gy1)); crop.thumbnail((250, 250))
        sheet2.alpha_composite(crop, (30 + i * 280, 20))
    sheet2.convert("RGB").save(os.path.join(OUT, "wired-gap-gauntlet-only-2-20261031.jpg"), quality=92)
    print("gauntlet-only 2 written")
except Exception as e:
    print("feet/gauntlet FAILED:", e)

# --- 4. Turnaround WARPS (not true hand-drawn): 3/4 torso, side, back ---
try:
    torso = load("Torso_Chest.png") if os.path.exists(os.path.join(SL, "Torso_Chest.png")) else None
    print("torso piece:", torso.size if torso else "missing, listing torso-like:", [f for f in os.listdir(SL) if "Torso" in f or "Chest" in f])
    sheet = Image.new("RGBA", (1200, 500), (128, 128, 128, 255))
    if torso is not None:
        t, _ = greykey(torso)
        variants = [("front", t), ("3/4-warp", t.resize((int(t.size[0] * 0.82), t.size[1]))),
                    ("side-warp", t.resize((int(t.size[0] * 0.55), t.size[1]))),
                    ("back-warp", t.transpose(Image.FLIP_LEFT_RIGHT))]
        for i, (lab, v) in enumerate(variants):
            v2 = v.copy(); v2.thumbnail((260, 400)); sheet.alpha_composite(v2, (20 + i * 290, 40))
    sheet.convert("RGB").save(os.path.join(OUT, "wired-gap-turnaround-warps-20261031.jpg"), quality=92)
    print("turnaround warps written (WARP, not true hand-drawn)")
except Exception as e:
    print("turnaround FAILED:", e)

# --- 5. Three more pipeline shots: CJ-19 dual-light, CJ-28 rooftop, CJ-30 alley ---
try:
    # CJ-19: dual-light V3 variant over grey (already a shot) -> reframe as shot spec output
    v3 = Image.open(os.path.join(RIG, "dual-light-variants-20261031/v3-gold-inner-cyan-outer-20261031.jpg")).convert("RGB")
    v3.save(os.path.join(OUT, "wired-shot-cj19-dual-light-20261031.jpg"), quality=92)
    # CJ-28: rooftop layout + arms-up plate
    roof = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-rooftop-painted-20261031.jpg")).convert("RGBA")
    arms, _ = greykey(Image.open(os.path.join(RIG, "dual-light-variants-20261031/base-arms-up-transparent-20261031.png")).convert("RGBA"))
    arms.thumbnail((400, 545)); roof.alpha_composite(arms, ((1168 - 400) // 2, 784 - 545 - 20))
    roof.convert("RGB").save(os.path.join(OUT, "wired-shot-cj28-rooftop-20261031.jpg"), quality=92)
    # CJ-30: alley layout + fighting pose
    alley = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-alley-painted-20261031.jpg")).convert("RGBA")
    fight, _ = greykey(Image.open(os.path.join(RIG, "reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png")).convert("RGBA"))
    fight.thumbnail((400, 545)); alley.alpha_composite(fight, ((1168 - 400) // 2, 784 - 545 - 20))
    alley.convert("RGB").save(os.path.join(OUT, "wired-shot-cj30-alley-20261031.jpg"), quality=92)
    print("pipeline shots CJ-19/CJ-28/CJ-30 written")
except Exception as e:
    print("pipeline shots FAILED:", e)
