#!/usr/bin/env python3
"""Angle Sheets 2-4 + Sheet-1 Z pieces, derived ONLY from existing slices.
No new character art is drawn. Transforms: uniform scale, anisotropic
squash/stretch, row-wise trapezoid warp, rotation, compositing of
existing slices. Every output records its source + transform in the index.
Sources: ~/workspace/cape-jones-rig/production-extensions-20261101/slices/
Uploads untouched (read-only)."""
import os, json, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.expanduser("~/workspace/cape-jones-rig/production-extensions-20261101/slices")
OUT = "/tmp/angle-sheets-234"
PIECES = os.path.join(OUT, "pieces")
ASM = os.path.join(OUT, "assemblies")

def load(name):
    p = os.path.join(SRC, name)
    im = Image.open(p).convert("RGBA")
    return im

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def save(im, name):
    p = os.path.join(PIECES, name)
    im.save(p)
    return p

def scale(im, sx, sy=None):
    sy = sx if sy is None else sy
    return im.resize((max(1, round(im.width * sx)), max(1, round(im.height * sy))),
                     Image.LANCZOS)

def trapezoid(im, top_f, bot_f, yscale=1.0):
    """Row-wise horizontal scale lerping top_f -> bot_f (foreshortening
    warp, no new pixels drawn: rows are resampled from the source only)."""
    w, h = im.size
    nh = max(1, round(h * yscale))
    out = Image.new("RGBA", (max(1, round(w * max(top_f, bot_f))) + 4, nh), (0, 0, 0, 0))
    for y in range(h):
        oy = round(y * yscale)
        if oy >= nh:
            break
        f = top_f + (bot_f - top_f) * (y / max(1, h - 1))
        row = im.crop((0, y, w, y + 1))
        nw = max(1, round(w * f))
        row = row.resize((nw, 1), Image.LANCZOS)
        out.alpha_composite(row, ((out.width - nw) // 2, oy))
    # trim transparent borders
    bb = out.getchannel("A").getbbox()
    return out.crop(bb) if bb else out

def paste(base, im, cx, cy):
    """Paste im centred at (cx, cy) on base."""
    base.alpha_composite(im, (round(cx - im.width / 2), round(cy - im.height / 2)))

def shadow(base, cx, cy, rx, ry):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, 70))
    base.alpha_composite(layer)

index = []
def rec(item, sheet, status, source, transform, outname, note):
    p = os.path.join(PIECES, outname) if outname else None
    if p and os.path.exists(p):
        im = Image.open(p); size = list(im.size); s = sha(p)
    else:
        size, s = None, None
    index.append({"item": item, "sheet": sheet, "status": status,
                  "source_piece": source, "transform": transform,
                  "output": ("pieces/" + outname) if outname else None,
                  "output_size_px": size, "sha256": s, "note": note})

# ---------- Sheet-1 Z pieces: GENERATED-DERIVED ----------
fist = load("Hand_Fist.png"); palm = load("Hand_OpenPalm.png")
save(scale(fist, 1.5), "Hand_Fist_Z_Close.png")
rec("Hand_Fist_Z_Close", "Sheet-1 Z", "GENERATED-DERIVED-SCALE", "Hand_Fist.png",
    "Uniform scale 1.5x (LANCZOS), no redraw", "Hand_Fist_Z_Close.png",
    "1.5x foreground swap per spec. Same drawing, larger; not a newly drawn close fist.")
save(scale(palm, 1.5), "Hand_Palm_Z_Close.png")
rec("Hand_Palm_Z_Close", "Sheet-1 Z", "GENERATED-DERIVED-SCALE", "Hand_OpenPalm.png",
    "Uniform scale 1.5x (LANCZOS), no redraw", "Hand_Palm_Z_Close.png",
    "1.5x foreground swap per spec. Same drawing, larger; not a newly drawn close palm.")

ua = load("UpperArm_L.png")
save(scale(ua, 1.30, 0.55), "UpperArm_Z_Short.png")
rec("UpperArm_Z_Short", "Sheet-1 Z", "GENERATED-DERIVED-WARP", "UpperArm_L.png",
    "Anisotropic scale x1.30 / y0.55", "UpperArm_Z_Short.png",
    "Compressed spherical deltoid/bicep by squash only. No new muscle drawing; label as warp, not native Z art.")

# Forearm aiming at lens: gauntlet shortened along its length + 1.3x fist on top (foreground)
g = load("Gauntlet_L.png")
g_short = scale(g, 0.62, 1.25)          # short along length, wide cuff
fist13 = scale(fist, 1.30)
cw = g_short.width + fist13.width // 2
ch = max(g_short.height, fist13.height) + 20
comp = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
comp.alpha_composite(g_short, (0, (ch - g_short.height) // 2))
comp.alpha_composite(fist13, (g_short.width - fist13.width // 2, (ch - fist13.height) // 2))
bb = comp.getchannel("A").getbbox(); comp = comp.crop(bb)
save(comp, "Forearm_Gauntlet_AimingAtLens.png")
rec("Forearm_Gauntlet_AimingAtLens", "Sheet-1 Z", "GENERATED-DERIVED-COMPOSITE", "Gauntlet_L.png + Hand_Fist.png",
    "Gauntlet x0.62/y1.25 + Hand_Fist 1.30x composited on top (foreground), elbow end behind",
    "Forearm_Gauntlet_AimingAtLens.png",
    "Composite only. Layer rule per spec: reaching toward camera = Hand top, gauntlet under it. NOT a native aiming-at-lens drawing (no new cuff ring / foreshortened pad drawn).")

th = load("Thigh_L.png")
save(trapezoid(th, 0.78, 1.38, 0.88), "Thigh_KneeForward_Z.png")
rec("Thigh_KneeForward_Z", "Sheet-1 Z", "GENERATED-DERIVED-WARP", "Thigh_L.png",
    "Row-wise trapezoid warp: hip width 0.78x -> knee width 1.38x, height 0.88x",
    "Thigh_KneeForward_Z.png",
    "Knee-forward foreshortening by warp only. No new knee-cap drawing; the knee ball is the source art's, widened by the warp.")

sb = load("Shin_Boot_Cut_S1.png")
save(scale(sb, 1.12, 0.62), "Shin_Boot_Z_Compressed.png")
rec("Shin_Boot_Z_Compressed", "Sheet-1 Z", "GENERATED-DERIVED-WARP", "Shin_Boot_Cut_S1.png",
    "Anisotropic scale x1.12 / y0.62", "Shin_Boot_Z_Compressed.png",
    "Compressed shin+boot by squash only. The V-trim is the source art's; no new deep-U trim drawn.")

sole = load("Boot_Angled_Sole_L.png")
save(scale(sole, 1.5), "Foot_Kick_Z.png")
rec("Foot_Kick_Z", "Sheet-1 Z", "GENERATED-DERIVED-SCALE", "Boot_Angled_Sole_L.png",
    "Uniform scale 1.5x (LANCZOS), no redraw", "Foot_Kick_Z.png",
    "Sole-to-camera kick swap at 1.5x. Same sole drawing used for the 20261101 kick at 1.2x; NOT a native toe-first Kick_Z drawing (no toe-first art exists in the sheets).")

# ---------- Sheet-1 Z pieces: REISSUE / EXISTS-PRIOR (copies, pixels identical) ----------
for srcname, outname, item, status, note in [
    ("Pelvis_UnderView.png", "Pelvis_Whole_TiltBack.png", "Pelvis_Whole_TiltBack",
     "REISSUE-EXISTING", "Source is the existing underside pelvis (dome + two leg sockets). Reissued under the spec's TiltBack name; NOT newly drawn. Alias: Pelvis_Top_Dome (parallel spec) = same drawing."),
    ("Torso_LeanBack.png", "Torso_LeanBack.png", "Torso_LeanBack",
     "EXISTS-PRIOR", "Distinct side-leaning torso slice, verified visually 20261101 (abs + side lean, 325x328). The Sheet-1 spec's 'owed' label for this item is superseded: the second slicing pass already sliced it. Parallel spec called the same bbox Torso_Front; that name is a duplicate of Torso_LeanForward, not this drawing."),
]:
    shutil.copyfile(os.path.join(SRC, srcname), os.path.join(PIECES, outname))
    rec(item, "Sheet-1 Z", status, srcname, "Byte-identical copy of existing slice, renamed/reissued only",
        outname, note)

# ---------- Sheet-1 Z pieces: SPEC-ONLY (no PNG; a squash would fake anatomy) ----------
rec("Head_TiltDown_Z", "Sheet-1 Z", "SPEC-ONLY", "Head_Front.png (donor, NOT used)",
    "None - no transform applied", None,
    "OWED. Needs new art: cowl dominating from above, jaw tucked, forward-charging glare. Squashing Head_Front would not create a cowl top or tucked jaw; it would mislabel a distortion as a new view. Head_ThreeQuarter is chin-raised, not tilt-down.")
rec("Head_TiltUp_Z", "Sheet-1 Z", "SPEC-ONLY", "Head_Front.png (donor, NOT used)",
    "None - no transform applied", None,
    "OWED. Needs new art: underside of jaw, cowl compressed from below. Head_ThreeQuarter (chin raised, face still frontal) is NOT an underside view and must not be relabelled as TiltUp_Z.")

# ---------- Derived assemblies (pose mockups from existing slices, NOT native sheets) ----------
GREY = (128, 128, 128, 255)

def assembly_sheet2():
    W, H = 1200, 1500
    base = Image.new("RGBA", (W, H), GREY)
    shadow(base, 600, 1380, 300, 32)
    head = scale(load("Head_Front.png"), 0.85)
    torso = scale(load("Torso_LeanForward.png"), 1.05)  # neck-disc top view suits top-down torso
    pelvis = scale(load("Pelvis_Whole.png"), 0.95)
    ua_z = load(os.path.join(PIECES, "UpperArm_Z_Short.png"))
    hand_s = scale(load("Hand_Fist.png"), 0.70)
    thigh_c = scale(trapezoid(load("Thigh_L.png"), 1.0, 0.85, 0.70), 0.9)
    shin_c = scale(load("Shin_Boot_Cut_S1.png"), 0.80, 0.55)
    sole_s = scale(load("Sole_Boot_Flat_L.png"), 0.70)
    paste(base, torso, 600, 480); paste(base, head, 600, 240)
    paste(base, pelvis, 600, 760)
    paste(base, ua_z, 300, 470); paste(base, ua_z.transpose(Image.FLIP_LEFT_RIGHT), 900, 470)
    paste(base, hand_s, 210, 560); paste(base, hand_s, 990, 560)
    paste(base, thigh_c, 490, 980); paste(base, thigh_c, 710, 980)
    paste(base, shin_c, 490, 1180); paste(base, shin_c, 710, 1180)
    paste(base, sole_s, 490, 1330); paste(base, sole_s, 710, 1330)
    p = os.path.join(ASM, "Angle_Sheet_2_BirdsEye_DERIVED_ASSEMBLY.png"); base.save(p); return p

def assembly_sheet3():
    W, H = 1200, 1600
    base = Image.new("RGBA", (W, H), GREY)
    shadow(base, 600, 1500, 380, 36)
    boot_big = scale(load("Boot.png"), 1.40); boot_big2 = boot_big.transpose(Image.FLIP_LEFT_RIGHT)
    thigh_t = scale(load("Thigh_L.png"), 1.05, 1.20)
    pelvis = scale(load("Pelvis_Whole.png"), 1.05)
    torso = scale(load("Torso_LeanBack.png"), 1.0, 1.25)
    head = scale(load("Head_Front.png"), 0.80)
    aim = load(os.path.join(PIECES, "Forearm_Gauntlet_AimingAtLens.png"))
    aim = scale(aim, 1.10)
    paste(base, boot_big, 420, 1280); paste(base, boot_big2, 780, 1280)
    paste(base, thigh_t, 470, 950); paste(base, thigh_t, 730, 950)
    paste(base, pelvis, 600, 720); paste(base, torso, 600, 450)
    paste(base, head, 600, 170)
    paste(base, aim, 240, 620); paste(base, scale(load("Hand_Fist.png"), 0.70), 980, 560)
    p = os.path.join(ASM, "Angle_Sheet_3_WormsEye_DERIVED_ASSEMBLY.png"); base.save(p); return p

def assembly_sheet4():
    W, H = 1400, 1200
    base = Image.new("RGBA", (W, H), GREY)
    shadow(base, 700, 1080, 420, 32)
    torso = load("Torso_LeanForward.png").rotate(-14, resample=Image.BICUBIC, expand=True)
    torso = scale(torso, 1.05)
    head = load("Head_Front.png").rotate(-10, resample=Image.BICUBIC, expand=True)
    head = scale(head, 0.95)
    # far leg (small, back-left) then near leg (large, foreground-right)
    paste(base, scale(load("Thigh_L.png"), 0.70), 420, 700)
    paste(base, scale(load("Boot.png"), 0.70), 380, 940)
    paste(base, torso, 700, 420); paste(base, head, 760, 170)
    paste(base, scale(load("Hand_Fist.png"), 0.70), 380, 420)  # far hand
    near_thigh = scale(load(os.path.join(PIECES, "Thigh_KneeForward_Z.png")), 1.30)
    near_shin = scale(load(os.path.join(PIECES, "Shin_Boot_Z_Compressed.png")), 1.20)
    kick = load(os.path.join(PIECES, "Foot_Kick_Z.png"))
    paste(base, near_thigh, 980, 720); paste(base, near_shin, 1040, 920)
    paste(base, kick, 1080, 1010)  # foreground, in front of torso plane
    aim = scale(load(os.path.join(PIECES, "Forearm_Gauntlet_AimingAtLens.png")), 1.20)
    paste(base, aim, 420, 620)  # near arm reaching toward lens, foreground-left
    p = os.path.join(ASM, "Angle_Sheet_4_DiagonalLunge_DERIVED_ASSEMBLY.png"); base.save(p); return p

a2, a3, a4 = assembly_sheet2(), assembly_sheet3(), assembly_sheet4()
for item, p, note in [
    ("Angle_Sheet_2_BirdsEye", a2, "DERIVED-ASSEMBLY ONLY: 2D pose mockup composited from existing slices (scales/overlaps listed in the Sheet-2 spec). NOT a native +45deg bird's-eye drawing: no true top-of-head, top-of-shoulders or top-of-cape art exists in the sheets."),
    ("Angle_Sheet_3_WormsEye", a3, "DERIVED-ASSEMBLY ONLY: 2D pose mockup composited from existing slices. NOT a native -45deg worm's-eye drawing: no true jaw-underside, boot-sole-from-below hero art beyond the sole swaps exists."),
    ("Angle_Sheet_4_DiagonalLunge", a4, "DERIVED-ASSEMBLY ONLY: 2D pose mockup composited from existing slices with depth scaling (near 1.2-1.3x, far 0.7x). NOT a native deep-perspective lunge drawing: no diagonal foreshortened torso/cape art exists."),
]:
    im = Image.open(p)
    index.append({"item": item, "sheet": "Angle sheet (derived assembly)", "status": "GENERATED-DERIVED-ASSEMBLY",
                  "source_piece": "Multiple existing slices (see spec)", "transform": "Scale / squash / rotation / compositing only",
                  "output": "assemblies/" + os.path.basename(p), "output_size_px": list(im.size),
                  "sha256": sha(p), "note": note})

with open(os.path.join(OUT, "piece-index-20261101.json"), "w") as f:
    json.dump(index, f, indent=1)
import csv
with open(os.path.join(OUT, "piece-index-20261101.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["item", "sheet", "status", "source_piece", "transform", "output", "output_size_px", "note"])
    w.writeheader()
    for r in index:
        r2 = dict(r); r2.pop("sha256"); r2["output_size_px"] = "x".join(map(str, r["output_size_px"])) if r["output_size_px"] else ""
        w.writerow(r2)
print("pieces+assemblies done:", len(index))
for r in index:
    print(r["item"], r["status"], r["output"], r["output_size_px"])
