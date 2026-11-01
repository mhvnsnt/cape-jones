#!/usr/bin/env python3
"""Part 2: ACES sheet, L3 PIL composites, painted-bg shifts, bg colour scripts,
plus prep files for the Blender Cycles room proof. All PIL outputs are labelled
PIL composite / PIL proof — never presented as Blender renders."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.expanduser("~/workspace/cape-jones-rig/gap-close-color-20261031")
RIG = os.path.expanduser("~/workspace/cape-jones-rig")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)

def char_alpha(pose_path):
    """Grey-128 key -> RGBA, 1px feather. Returns (rgba_image, mask_L_image)."""
    im = Image.open(pose_path).convert("RGB")
    a = np.array(im).astype(int)
    dist = np.abs(a - 128).max(axis=2)
    mask = (dist > 20).astype(np.uint8) * 255
    m = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(1))
    rgba = im.convert("RGBA")
    rgba.putalpha(m)
    return rgba, m

def dilate(mask, px):
    return mask.filter(ImageFilter.MaxFilter(2 * px + 1))

def erode(mask, px):
    return mask.filter(ImageFilter.MinFilter(2 * px + 1))

def rim_layer(mask, px, color):
    d = dilate(mask, px)
    rim = Image.new("L", mask.size, 0)
    import numpy as _np
    rim = Image.fromarray((_np.array(d) - _np.array(mask)).clip(0, 255).astype("uint8"))
    solid = Image.new("RGBA", mask.size, color + (255,))
    out = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    out.paste(solid, (0, 0), rim)
    return out

def band_layer(mask, inner_px, outer_px, color, opacity):
    d_o = dilate(mask, outer_px)
    d_i = dilate(mask, inner_px)
    import numpy as _np
    band = Image.fromarray((_np.array(d_o) - _np.array(d_i)).clip(0, 255).astype("uint8"))
    solid = Image.new("RGBA", mask.size, color + (255,))
    out = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    out.paste(solid, (0, 0), band)
    # apply opacity via alpha scale
    arr = _np.array(out).astype(float)
    arr[:, :, 3] *= opacity
    return Image.fromarray(arr.astype("uint8"))

def inner_band(mask, px, color, opacity):
    e = erode(mask, px)
    import numpy as _np
    band = Image.fromarray((_np.array(mask) - _np.array(e)).clip(0, 255).astype("uint8"))
    solid = Image.new("RGBA", mask.size, color + (255,))
    out = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    out.paste(solid, (0, 0), band)
    arr = _np.array(out).astype(float)
    arr[:, :, 3] *= opacity
    return Image.fromarray(arr.astype("uint8"))

def shadow_layers(mask, char_bbox):
    """Ground ellipse + cast shadow (offset silhouette, blurred, 0.45)."""
    x0, y0, x1, y1 = char_bbox
    W, H = mask.size
    ground = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(ground)
    gd.ellipse([x0 - 40, y1 - 30, x1 + 40, y1 + 55], fill=(40, 40, 90, 255))
    ground = ground.filter(ImageFilter.GaussianBlur(18))
    arr = np.array(ground).astype(float); arr[:, :, 3] *= 0.45
    ground = Image.fromarray(arr.astype("uint8"))
    cast = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sil = Image.new("RGBA", (W, H), (30, 30, 70, 255))
    cast.paste(sil, (60, 45), mask)
    cast = cast.filter(ImageFilter.GaussianBlur(10))
    arr = np.array(cast).astype(float); arr[:, :, 3] *= 0.45
    cast = Image.fromarray(arr.astype("uint8"))
    return ground, cast

def shafts(W, H, specs):
    """specs: list of (x_top, width_top, x_bottom, width_bottom, color, opacity)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for xt, wt, xb, wb, col, op in specs:
        d.polygon([(xt - wt, 0), (xt + wt, 0), (xb + wb, H), (xb - wb, H)],
                  fill=col + (int(255 * op),))
    return layer.filter(ImageFilter.GaussianBlur(24))

def screen_paste(base, layer):
    """Screen-blend layer over base (both RGBA)."""
    import numpy as _np
    b = _np.array(base.convert("RGB")).astype(float) / 255
    l = _np.array(layer.convert("RGB")).astype(float) / 255
    la = _np.array(layer)[:, :, 3:4].astype(float) / 255
    scr = 1 - (1 - b) * (1 - l)
    out = b * (1 - la) + scr * la
    res = Image.fromarray((out * 255).astype("uint8")).convert("RGBA")
    res.putalpha(base.split()[3] if base.mode == "RGBA" else 255)
    return res

def spill_on_char(char_rgba, mask, color, opacity, side="left"):
    import numpy as _np
    W, H = mask.size
    grad = _np.tile(_np.linspace(1, 0, W) if side == "left" else _np.linspace(0, 1, W), (H, 1))
    solid = Image.new("RGBA", (W, H), color + (255,))
    arr = _np.array(solid).astype(float)
    ma = _np.array(mask).astype(float) / 255
    arr[:, :, 3] = ma * grad * 255 * opacity
    return Image.fromarray(arr.astype("uint8"))

def dust(layer, shafts_x, W, H, n=40, seed=7):
    import random
    rnd = random.Random(seed)
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        x = rnd.choice(shafts_x) + rnd.randint(-60, 60)
        y = rnd.randint(60, H - 100)
        r = rnd.randint(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 220, 180))
    return layer

def build_l3(pose_path, bg, shaft_specs, rim_col, bleed_col, bleed_op,
             inner_rim_col, spill_col, spill_side, out_name, grade=None):
    W, H = 1100, 1500
    canvas = bg.resize((W, H)).convert("RGBA")
    char_rgba, mask = char_alpha(pose_path)
    if grade:
        arr = np.array(char_rgba).astype(float)
        arr[:, :, 0] *= grade[0]; arr[:, :, 1] *= grade[1]; arr[:, :, 2] *= grade[2]
        char_rgba = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
    ma = np.array(mask)
    ys, xs = np.where(ma > 10)
    bbox = (xs.min(), ys.min(), xs.max(), ys.max())
    ground, cast = shadow_layers(mask, bbox)
    canvas = Image.alpha_composite(canvas, ground)
    canvas = Image.alpha_composite(canvas, cast)
    sh = shafts(W, H, shaft_specs)
    canvas = screen_paste(canvas, sh)
    canvas = Image.alpha_composite(canvas, rim_layer(mask, 3, rim_col))
    if inner_rim_col:
        canvas = Image.alpha_composite(canvas, inner_band(mask, 2, inner_rim_col, 0.9))
    canvas = Image.alpha_composite(canvas, band_layer(mask, 3, 8, bleed_col, bleed_op))
    canvas = Image.alpha_composite(canvas, char_rgba)
    canvas = Image.alpha_composite(canvas, spill_on_char(char_rgba, mask, spill_col, 0.18, spill_side))
    dust_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dust(dust_layer, [s[0] for s in shaft_specs], W, H)
    canvas = Image.alpha_composite(canvas, dust_layer)
    # haze
    haze = Image.new("RGBA", (W, H), (200, 200, 220, 18))
    canvas = Image.alpha_composite(canvas, haze)
    out = os.path.join(OUT, out_name)
    canvas.convert("RGB").save(out)
    print("L3", out, canvas.size)
    return out

def build_l3_all():
    stage = Image.new("RGB", (1100, 1500), (40, 20, 70))
    d = ImageDraw.Draw(stage)
    d.rectangle([0, 1150, 1100, 1500], fill=(25, 12, 45))
    dark = Image.new("RGB", (1100, 1500), (18, 18, 30))
    d = ImageDraw.Draw(dark)
    d.rectangle([0, 1250, 1100, 1500], fill=(12, 12, 22))
    roof = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-rooftop-painted-20261031.jpg")).convert("RGB")
    dance = os.path.join(RIG, "reposes-v7c-clean/joint-dance-v7c-clean.png")
    fight = os.path.join(RIG, "reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png")
    apose = os.path.join(RIG, "reposes-v7c-clean/joint-apose-v7c-clean.png")
    cj11 = build_l3(dance, stage,
        [(450, 90, 380, 200, (220, 150, 255), 0.55), (750, 70, 820, 160, (220, 150, 255), 0.45)],
        (220, 150, 255), (170, 80, 235), 0.35, None, (220, 150, 255), "left",
        "level3-CJ11-spotlight-finale-PIL-20261031.png")
    cj19 = build_l3(fight, dark,
        [(550, 80, 480, 190, (0, 200, 255), 0.55), (300, 50, 240, 130, (0, 200, 255), 0.35)],
        (0, 200, 255), (255, 120, 0), 0.20, (255, 180, 80), (0, 200, 255), "left",
        "level3-CJ19-dual-light-PIL-20261031.png", grade=(1.10, 0.95, 0.70))
    cj28 = build_l3(apose, roof,
        [(400, 100, 300, 220, (255, 155, 75), 0.50)],
        (255, 155, 75), (255, 100, 20), 0.25, None, (255, 155, 75), "left",
        "level3-CJ28-rooftop-sunset-PIL-20261031.png")
    # combined sheet
    pw, ph = 520, 709
    sheet = Image.new("RGB", (16 * 2 + 3 * pw + 2 * 12, 78 + 16 + ph + 40 + 150), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    dr.rectangle([0, 0, sheet.size[0], 78], fill=(20, 20, 20))
    dr.text((16, 8), "LEVEL-3 PROOF COMPOSITES — CJ-11 / CJ-19 / CJ-28 (all PIL composite, NOT Blender renders)",
             font=font(22, True), fill=(255, 255, 255))
    dr.text((16, 44), "Each: character + god-ray shafts + bleed + ground shadow + cast shadow + spill on character + haze + dust.",
             font=font(15), fill=(220, 220, 220))
    x = 16
    caps = [("CJ-11 spotlight finale (Level 3, violet-magenta stage key)",
             "Rim (220,150,255) under stage key; bleed (170,80,235); shafts from above."),
            ("CJ-19 dual-light (Level 3, gold front + cyan back)",
             "BACK rim cyan (0,200,255) + FRONT inner rim amber (255,180,80); bleeds orange + cyan-dark."),
            ("CJ-28 rooftop sunset (Level 3, sun low behind)",
             "Rim (255,155,75) under sunset key; bleed (255,100,20); character stays BASE (ATMOSPHERE is env-only).")]
    for f, (t1, t2) in zip([cj11, cj19, cj28], caps):
        im = Image.open(f).resize((pw, ph), Image.LANCZOS)
        sheet.paste(im, (x, 78 + 16))
        dr.rectangle([x, 78 + 16, x + pw - 1, 78 + 16 + ph - 1], outline=(0, 0, 0), width=2)
        dr.text((x + 4, 78 + 16 + ph + 6), t1, font=font(14, True), fill=(0, 0, 0))
        dr.text((x + 4, 78 + 16 + ph + 28), t2, font=font(13), fill=(0, 0, 0))
        x += pw + 12
    y = 78 + 16 + ph + 62
    dr.text((16, y), "HONESTY: PIL stack (masks regenerated per pose — godray-level3 layers are not pose-aligned for dance/fighting).",
             font=font(14), fill=(0, 0, 0))
    y += 24
    dr.text((16, y), "L3 test applied: bright shafts + layered rim + bleed + shadow interaction (ground + cast + spill) + bloom-adjacent haze/dust.",
             font=font(14), fill=(0, 0, 0))
    y += 24
    dr.text((16, y), "NOT Mars-approved as L3 (Mars decides). Background paintings unchanged (rooftop painting reused as-is for CJ-28).",
             font=font(14), fill=(0, 0, 0))
    out = os.path.join(OUT, "level3-proof-composites-sheet-20261031.png")
    sheet.save(out)
    print("L3 sheet", out, sheet.size)
    return [cj11, cj19, cj28, out]

def build_aces_sheet():
    std = np.array(Image.open(os.path.join(OUT, "aces13-standard-20261031.png")).convert("RGB")).astype(int)
    ace = np.array(Image.open(os.path.join(OUT, "aces13-aces13-20261031.png")).convert("RGB")).astype(int)
    d = np.abs(std - ace)
    mean, mx = round(float(d.mean()), 2), int(d.max())
    per = [round(float(d[:, :, c].mean()), 2) for c in range(3)]
    samples = {}
    for name, (x, y) in [("bg corner", (10, 10)), ("suit torso", (330, 450)),
                          ("cowl", (330, 180)), ("shadow zone", (330, 750))]:
        samples[name] = (tuple(std[y, x]), tuple(ace[y, x]))
    print("ACES mean", mean, "max", mx, "per-channel", per, samples)
    pw, ph = 440, 600
    sheet = Image.new("RGB", (16 * 2 + 2 * pw + 12, 78 + 16 + ph + 40 + 260), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    dr.rectangle([0, 0, sheet.size[0], 78], fill=(20, 20, 20))
    dr.text((16, 8), "ACES 1.3 COMPARISON — same Blender plate, same node tree, only the view transform changed",
             font=font(21, True), fill=(255, 255, 255))
    dr.text((16, 44), "Blender 5.2.3 LTS, Cycles CPU, 16 samples, 660x900, display device sRGB both, exposure 0 / gamma 1. 34 nodes / 43 links.",
             font=font(15), fill=(220, 220, 220))
    x = 16
    for f, lab in [("aces13-standard-20261031.png", "STANDARD view transform"),
                   ("aces13-aces13-20261031.png", "ACES 1.3 view transform")]:
        im = Image.open(os.path.join(OUT, f)).resize((pw, ph), Image.LANCZOS)
        sheet.paste(im, (x, 78 + 16))
        dr.rectangle([x, 78 + 16, x + pw - 1, 78 + 16 + ph - 1], outline=(0, 0, 0), width=2)
        dr.text((x + 6, 78 + 16 + ph + 8), lab, font=font(16, True), fill=(0, 0, 0))
        x += pw + 12
    y = 78 + 16 + ph + 44
    lines = [
        f"MEASURED PIXEL DELTAS (Standard -> ACES 1.3, full 660x900 frame): mean absolute = {mean}  |  max = {mx}  |  per-channel mean R {per[0]} / G {per[1]} / B {per[2]}.",
    ]
    for name, (s, a_) in samples.items():
        lines.append(f"Sample {name}: Standard {s} -> ACES 1.3 {a_}.")
    lines += [
        "Read: ACES 1.3 is darker and greyer than Standard — grey 129 -> 104, warm cream suit -> grey-beige, rim warmth muted, cowl stays purple.",
        "OCIO NOTE: Blender 5.2.3 built-in OCIO config; view transform is the ONLY change (same .blend node tree, same plate, same display).",
        "Prior ACES 2.0 result (clean-100, EEVEE, Rec.1886 display): grey 129 -> 107, mean 24.0, max 73 — NOT like-for-like with this run",
        "(different engine + display device), so no 1.3-vs-2.0 ranking is claimed here. For a strict Rec.709 gamma 2.4 finish, Standard remains",
        "the finishing view; ACES 1.3 is a creative look, same verdict as ACES 2.0 in the clean-100 report.",
        "EGL warnings on the console are harmless noise on this VM (renders saved, verified on disk). NOT Mars-approved.",
    ]
    for ln in lines:
        dr.text((16, y), ln, font=font(14), fill=(0, 0, 0))
        y += 24
    out = os.path.join(OUT, "aces13-comparison-20261031.png")
    sheet.save(out)
    print("ACES sheet", out, sheet.size)
    return out, mean, mx, per, samples

def build_painted_bg():
    desk = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-desk-painted-20261031.jpg")).convert("RGB")
    def shift(im, gains, tint, op):
        arr = np.array(im).astype(float)
        arr[:, :, 0] *= gains[0]; arr[:, :, 1] *= gains[1]; arr[:, :, 2] *= gains[2]
        arr = arr * (1 - op) + np.array(tint) * op
        return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
    ten = shift(desk, (1.15, 0.75, 1.20), (255, 110, 180), 0.12)
    pow_ = shift(desk, (1.20, 0.80, 0.65), (255, 90, 40), 0.12)
    ten.save(os.path.join(OUT, "painted-bg-room-TENSION-shifted-20261031.png"))
    pow_.save(os.path.join(OUT, "painted-bg-room-POWER-shifted-20261031.png"))
    apose = os.path.join(RIG, "reposes-v7c-clean/joint-apose-v7c-clean.png")
    char_rgba, _ = char_alpha(apose)
    def panel(bg, pw=560):
        bg_r = bg.resize((pw, int(pw * bg.size[1] / bg.size[0])), Image.LANCZOS)
        ph = bg_r.size[1]
        canvas = bg_r.convert("RGBA")
        ch_h = 300
        scale = ch_h / 1041
        ch = char_rgba.resize((int(1100 * scale), int(1500 * scale)), Image.LANCZOS)
        canvas.alpha_composite(ch, (int((pw - ch.size[0]) / 2), 376 - ch.size[1] + 30))
        return canvas.convert("RGB")
    panels = [("BASE background + BASE character (control)", panel(desk)),
              ("TENSION-shifted background + BASE character (environment-only)", panel(ten)),
              ("POWER-shifted background + BASE character (environment-only)", panel(pow_))]
    pw = panels[0][1].size[0]; ph = panels[0][1].size[1]
    sheet = Image.new("RGB", (16 * 2 + 3 * pw + 2 * 12, 78 + 16 + ph + 40 + 130), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    dr.rectangle([0, 0, sheet.size[0], 78], fill=(20, 20, 20))
    dr.text((16, 8), "PAINTED-BACKGROUND VERSIONS (partial close) — environment shift, character held at BASE",
             font=font(21, True), fill=(255, 255, 255))
    dr.text((16, 44), "Painted room = clean-100 desk painting (batch-KKGuh file was not found on disk — substitute stated, never claimed as KKGuh).",
             font=font(15), fill=(220, 220, 220))
    x = 16
    for t, im in panels:
        sheet.paste(im, (x, 78 + 16))
        dr.rectangle([x, 78 + 16, x + pw - 1, 78 + 16 + ph - 1], outline=(0, 0, 0), width=2)
        dr.text((x + 4, 78 + 16 + ph + 8), t, font=font(13, True), fill=(0, 0, 0))
        x += pw + 12
    y = 78 + 16 + ph + 44
    for ln in ["DISTINCTION: here ONLY the background shifts (character stays canon base). In a FULL JoJo shift (task-3 sheet) the",
               "character is ALSO repainted (TENSION rose suit + full magenta cape; POWER red-orange suit + scarlet cape).",
               "Method on painted art: palette-family grade + palette tint overlay (a painted bg has no flat parts to reassign — this is",
               "a grade, labelled as such, NOT the v3 flat replacement). TENSION grade (1.15,0.75,1.20) + rose tint 0.12;",
               "POWER grade (1.20,0.80,0.65) + scarlet tint 0.12. Other palettes' painted versions: still owed. NOT Mars-approved."]:
        dr.text((16, y), ln, font=font(14), fill=(0, 0, 0)); y += 24
    out = os.path.join(OUT, "painted-bg-environment-shift-sheet-20261031.png")
    sheet.save(out)
    print("painted sheet", out, sheet.size)

def build_bg_scripts():
    desk = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-desk-painted-20261031.jpg")).convert("RGB")
    roof = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-rooftop-painted-20261031.jpg")).convert("RGB")
    alley = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-alley-painted-20261031.jpg")).convert("RGB")
    scenes = [
        {"scene": "room", "bg": desk, "bg_note": "desk painting (clean-100; KKGuh substitute, stated)",
         "base_palette": "canon base", "lut": "warm-interior", "lut_gain": [1.10, 0.95, 0.70],
         "key": "warm lamp, front-left", "rim": "warm amber (255,180,80)", "bleed": "orange (255,120,0) 0.20",
         "jojo_shift": "none", "light_direction": "front-left, lamp height",
         "horizon_scale": "ROOM-ONLY 2.5x rule: rig 950px tall, feet on floor, chair back at waist (locked sheet)"},
        {"scene": "street", "bg": None, "bg_note": "NO clean painted street art on disk — swatch panel only; layout-pass-street.jpg is labelled, NOT embedded",
         "base_palette": "canon base", "lut": "golden-hour", "lut_gain": [1.10, 0.95, 0.70],
         "key": "warm gold sun, front-right low", "rim": "magenta-rose (255,178,229) ONLY under TENSION shift",
         "bleed": "pink-dark (230,80,170)", "jojo_shift": "JOJO-TENSION (CJ-01 family; demo-only, not canon until Mars approves)",
         "light_direction": "front-right, low sun",
         "horizon_scale": "layout scale ~0.35 of rig canvas (room 2.5x rule does NOT apply — room-only)"},
        {"scene": "rooftop", "bg": roof, "bg_note": "rooftop painting (clean-100)",
         "base_palette": "canon base (character)", "lut": "sunset-rooftop", "lut_gain": [1.15, 0.80, 0.70],
         "key": "sun low behind (primary source)", "rim": "warm sunset (255,155,75) — follows sunset LUT, NOT the atmosphere shift",
         "bleed": "orange (255,100,20)", "jojo_shift": "JOJO-ATMOSPHERE, environment-only (approved 15:36 as world shift; character never leaves base)",
         "light_direction": "behind, low",
         "horizon_scale": "layout scale ~0.35 of rig canvas; horizon at rooftop parapet line"},
        {"scene": "alley", "bg": alley, "bg_note": "alley painting (clean-100)",
         "base_palette": "canon base", "lut": "neon-alley-pink-cyan", "lut_gain": [0.95, 0.85, 1.05],
         "key": "pink/magenta neon front + cyan neon back (dual)", "rim": "FRONT magenta-rose (255,178,229) + BACK cyan (0,200,255) — each rim named to its source",
         "bleed": "front pink-dark (230,80,170); back cyan-dark (0,140,200)",
         "jojo_shift": "none (dual-light exception, not a JoJo shift)", "light_direction": "front neon + behind cyan",
         "horizon_scale": "layout scale ~0.35 of rig canvas; alley walls converge to centre horizon"},
    ]
    pw, ph = 520, 350
    sheet = Image.new("RGB", (16 * 2 + 4 * pw + 3 * 12, 78 + 16 + ph + 40 + 8 * 30 + 60), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    dr.rectangle([0, 0, sheet.size[0], 78], fill=(20, 20, 20))
    dr.text((16, 8), "BACKGROUND COLOUR SCRIPTS — room / street / rooftop / alley",
             font=font(22, True), fill=(255, 255, 255))
    dr.text((16, 44), "Per scene: base palette, LUT, key / rim / bleed, JoJo shift if any, light direction, horizon / scale note. NOT Mars-approved.",
             font=font(15), fill=(220, 220, 220))
    x = 16
    for s in scenes:
        if s["bg"] is not None:
            im = s["bg"].resize((pw, ph), Image.LANCZOS)
        else:
            im = Image.new("RGB", (pw, ph), (200, 170, 190))
            dd = ImageDraw.Draw(im)
            dd.text((20, 150), "STREET PAINTED BG OWED", font=font(20, True), fill=(40, 40, 40))
            dd.text((20, 185), "swatch only — no labelled art embedded", font=font(15), fill=(40, 40, 40))
        sheet.paste(im, (x, 78 + 16))
        dr.rectangle([x, 78 + 16, x + pw - 1, 78 + 16 + ph - 1], outline=(0, 0, 0), width=2)
        dr.text((x + 6, 78 + 16 + ph + 8), s["scene"].upper(), font=font(16, True), fill=(0, 0, 0))
        x += pw + 12
    y = 78 + 16 + ph + 44
    for s in scenes:
        dr.text((16, y), f'{s["scene"].upper()}: base {s["base_palette"]} | LUT {s["lut"]} gain {s["lut_gain"]} | key: {s["key"]}',
                font=font(13), fill=(0, 0, 0)); y += 22
        dr.text((16, y), f'    rim: {s["rim"]} | bleed: {s["bleed"]} | shift: {s["jojo_shift"]}',
                font=font(13), fill=(0, 0, 0)); y += 22
        dr.text((16, y), f'    light: {s["light_direction"]} | horizon/scale: {s["horizon_scale"]} | bg: {s["bg_note"]}',
                font=font(13), fill=(0, 0, 0)); y += 26
    out = os.path.join(OUT, "background-colour-scripts-20261031.png")
    sheet.save(out)
    jout = os.path.join(OUT, "background-colour-scripts-20261031.json")
    data = {"mars_approved": False, "scenes": [{k: v for k, v in s.items() if k != "bg"} for s in scenes]}
    json.dump(data, open(jout, "w"), indent=2)
    print("bg scripts", out, sheet.size, jout)

def build_room_prep():
    desk = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-desk-painted-20261031.jpg")).convert("RGB")
    W, H = 1168, 1060
    canvas = Image.new("RGB", (W, H))
    canvas.paste(desk, (0, 0))
    bot = np.array(desk)[-1, :, :].mean(axis=0).astype(int)
    print("floor extension colour (avg bottom row):", tuple(bot))
    import numpy as _np
    arr = _np.array(canvas)
    arr[784:, :] = bot
    Image.fromarray(arr).save(os.path.join(OUT, "room-proof-bg-canvas-20261031.png"))
    char_rgba, _ = char_alpha(os.path.join(RIG, "reposes-v7c-clean/joint-apose-v7c-clean.png"))
    char_rgba.save(os.path.join(OUT, "room-proof-char-alpha-20261031.png"))
    print("room prep done")

if __name__ == "__main__":
    build_aces_sheet()
    build_l3_all()
    build_painted_bg()
    build_bg_scripts()
    build_room_prep()
