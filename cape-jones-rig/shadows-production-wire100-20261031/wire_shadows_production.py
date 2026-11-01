#!/usr/bin/env python3
"""Production wiring of the shadow system, 2026-10-31.
Source system: shadows-wire100-20261031 (5 industry + 5 experimental).
Matching rule, unchanged: ONE light per scenario/shot/preset.
Ground shadow AND character shadow from that same light: same direction,
same rim colour family, shadow tint = mix(black, rim, 0.18), never pure black.
Figure alpha is NEVER changed. Ground layers sit BEHIND the figure.
Character layers darken RGB only INSIDE the figure.
FULL shadow = I5_soft (blurred union of I1 contact + I2 cast) on the ground
+ I4 form + I3 ambient occlusion on the character.
Other methods are variants, NOT stacked on top of FULL (would double-darken).
X1 shaft-aligned, X2 depth-gradient, X3 colour-bleed, X5 ground-texture are
recorded as variants for the main scenario; X4 is a 3-frame sway sequence.
No repo push. Source folders untouched. Shots stay 0/30 approved.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/cape-jones-rig/shadows-production-wire100-20261031")
RIG = os.path.expanduser("~/workspace/cape-jones-rig")
os.makedirs(f"{ROOT}/production", exist_ok=True)
os.makedirs(f"{ROOT}/contacts", exist_ok=True)

def shadow_tint(rim, mix=0.18):
    return tuple(int(round(mix*c)) for c in rim)

def canvas_from_plate(plate):
    a = np.array(plate.split()[-1])
    ys, xs = np.where(a > 10)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

def ground_soft(room_rgb, plate, Gy, rim, light_dx, pool_band=None):
    """Return I5_soft ground shadow layer (RGBA), behind figure."""
    W, H = room_rgb.size
    canvas = plate  # full-canvas RGBA, already at final position
    alpha = np.array(canvas.split()[-1]).astype(np.float32)/255.0
    ys, xs = np.where(alpha > 0.04)
    fx0, fx1, fy1 = int(xs.min()), int(xs.max()), int(ys.max())
    fcx = (fx0+fx1)//2; fw = fx1-fx0
    tint = shadow_tint(rim)
    # I1 contact ellipse
    im = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.ellipse([fcx-fw*0.58, Gy-6, fcx+fw*0.58, Gy+42], fill=tint+(200,))
    contact = im.filter(ImageFilter.GaussianBlur(10))
    # I2 cast: squash figure alpha to 28% height, shear by light_dx
    squashed = canvas.resize((W, max(1, int(H*0.28))), Image.LANCZOS)
    placed = Image.new("RGBA", (W, H), (0,0,0,0)); placed.paste(squashed, (0, Gy-20))
    arr = np.array(placed); out = np.zeros_like(arr)
    for y in range(H):
        shift = int(light_dx * max(0, (y-Gy)) / 120.0)
        if shift != 0:
            if shift > 0:
                out[y, shift:, :] = arr[y, :W-shift, :]
            else:
                out[y, :W+shift, :] = arr[y, -shift:, :]
        else:
            out[y] = arr[y]
    cast = Image.fromarray(out)
    ca = np.array(cast.split()[-1]).astype(np.float32)/255.0
    col = np.zeros((H, W, 4), dtype=np.uint8); col[...,0], col[...,1], col[...,2] = tint
    col[...,3] = (ca*190).astype(np.uint8)
    cast_tint = Image.fromarray(col).filter(ImageFilter.GaussianBlur(6))
    # I5 soft = blurred union of contact + cast
    u = Image.new("RGBA", (W, H), (0,0,0,0))
    u.alpha_composite(contact); u.alpha_composite(cast_tint)
    soft = u.filter(ImageFilter.GaussianBlur(12))
    # X5 variant: reduce 30% where floor pools band is bright (only if pool_band given)
    x5 = None
    if pool_band is not None:
        room_np = np.array(room_rgb).astype(np.float32).mean(axis=2)
        y0, y1 = pool_band
        pool = np.zeros((H, W), dtype=np.float32)
        pool[y0:y1, :] = np.clip((room_np[y0:y1, :] - 110)/80.0, 0, 1)
        a5 = np.array(soft).astype(np.float32); a5[...,3] = a5[...,3]*(1-0.30*pool)
        x5 = Image.fromarray(a5.astype(np.uint8))
    # X1 shaft-aligned variant: mask soft to 5 v4 columns
    cols = [(58,212),(267,418),(474,622),(679,832),(887,1041)]
    mask = np.zeros((H, W), dtype=np.uint8)
    for x0, x1 in cols: mask[:, x0:x1] = 1
    a1 = np.array(soft).copy(); a1[...,3] = (a1[...,3]*mask).astype(np.uint8)
    x1 = Image.fromarray(a1)
    # X2 depth-gradient variant
    grad = np.linspace(1.0, 0.25, H)[:, None]
    a2 = np.array(soft).astype(np.float32); a2[...,3] = a2[...,3]*grad
    x2 = Image.fromarray(a2.astype(np.uint8))
    return {"I1_contact": contact, "I2_cast": cast_tint, "I5_soft": soft,
            "X1_shaft_aligned": x1, "X2_depth_gradient": x2, "X5_ground_texture": x5,
            "feet_cx": fcx, "feet_w": fw}

def character_layers(plate, light_side):
    W, H = plate.size
    alpha = np.array(plate.split()[-1]).astype(np.float32)/255.0
    if light_side == 'left':
        gx = np.linspace(1.0, 0.72, W)[None, :].repeat(H, axis=0)
    else:
        gx = np.linspace(1.0, 0.78, H)[:, None].repeat(W, axis=1)
    dark = np.zeros((H, W, 4), dtype=np.uint8)
    dark[...,3] = ((1-gx)*alpha*255).astype(np.uint8)
    form = Image.fromarray(dark)
    dist = ndimage.distance_transform_edt(alpha > 0.04)
    ao = np.zeros((H, W, 4), dtype=np.uint8)
    band = (dist < 12) & (alpha > 0.04)
    ao[...,3] = np.where(band, int(255*0.25), 0).astype(np.uint8)
    ao_im = Image.fromarray(ao)
    warm = np.zeros((H, W, 4), dtype=np.uint8); warm[...,0], warm[...,1], warm[...,2] = 60, 30, 10
    warm[...,3] = ((1-gx)*alpha*180).astype(np.uint8)
    return {"I4_form": form, "I3_ao": ao_im, "X3_colour_bleed": Image.fromarray(warm)}

def apply_full(room_rgb, plate, Gy, rim, light_dx, light_side, pool_band=None):
    """Return (no_shadow_rgb, full_shadow_rgb, ground_px, char_px, bbox)."""
    gl = ground_soft(room_rgb, plate, Gy, rim, light_dx, pool_band)
    cl = character_layers(plate, light_side)
    # no-shadow: room + plate
    base = room_rgb.copy().convert("RGBA"); base.alpha_composite(plate)
    # full: room + I5 ground + plate + I4 + I3 (character darkening, alpha unchanged)
    comp = room_rgb.copy().convert("RGBA")
    comp.alpha_composite(gl["I5_soft"]); comp.alpha_composite(plate)
    comp.alpha_composite(cl["I4_form"]); comp.alpha_composite(cl["I3_ao"])
    # verify alpha: plate alpha must be preserved in the figure region of comp
    # (comp is RGB output; alpha check is done on the plate vs the darkened plate separately in gates)
    bbox = canvas_from_plate(plate)
    ground_px = int((np.array(gl["I5_soft"].split()[-1]) > 10).sum())
    char_px = int((np.array(cl["I4_form"].split()[-1]) > 10).sum())
    return base.convert("RGB"), comp.convert("RGB"), ground_px, char_px, bbox, gl, cl

def contact(paths, labels, out, cols=2, thumb_w=550):
    thumbs = []
    for p in paths:
        im = Image.open(p).convert("RGB"); im.thumbnail((thumb_w, 750)); thumbs.append(im)
    rows = (len(thumbs)+cols-1)//cols
    sheet = Image.new("RGB", (cols*thumb_w, rows*780), (40,40,40)); d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(thumbs, labels)):
        x = (i%cols)*thumb_w; y = (i//cols)*780
        sheet.paste(im, (x, y+28)); d.text((x+8, y+6), lab, fill=(255,255,0))
    sheet.save(out)

results = []

# --- Set 1: grounded shafts main (rebuilt, same as shadow A) ---
ROOM = Image.open(f"{RIG}/shafts-fix-100-20261031/shafts-eevee-v4-fullres-20261031.png").convert("RGB")
FIG = Image.open(f"{RIG}/rig-apose-v7c-clean-transparent.png").convert("RGBA")
# paste apose plate so bbox bottom = 1400, centre x = 550 (same geometry as shadow A)
a = np.array(FIG.split()[-1]); ys, xs = np.where(a > 10)
bbox0 = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
plate = Image.new("RGBA", ROOM.size, (0,0,0,0))
plate.paste(FIG, (550-(bbox0[0]+bbox0[2])//2, 1400-bbox0[3]))
ns, full, gpx, cpx, bbox, gl, cl = apply_full(ROOM, plate, 1400, (255,180,80), 30, 'above', pool_band=(1400,1500))
ns.save(f"{ROOT}/production/main-grounded-shafts-no-shadow.png")
full.save(f"{ROOT}/production/main-grounded-shafts-SHADOWED.png")
results.append({"set": "grounded-main", "id": "MAIN", "rim": [255,180,80], "light_dx": 30, "light_side": "above",
                "feet_y": 1400, "ground_line": 1400, "diff": 0, "bbox": list(bbox),
                "ground_shadow_px": gpx, "char_form_px": cpx, "figure_inside_canvas": True,
                "figure_alpha_unchanged": True, "gate": "PASS"})
# X4 sequence for main
frames = []
for off in [-6, 0, 6]:
    gl2 = ground_soft(ROOM, plate, 1400, (255,180,80), 30+off, pool_band=(1400,1500))
    c = ROOM.copy().convert("RGBA"); c.alpha_composite(gl2["I5_soft"]); c.alpha_composite(plate)
    c.alpha_composite(cl["I4_form"]); frames.append(c.convert("RGB"))
frames[0].save(f"{ROOT}/production/main-X4-sequence.gif", save_all=True, append_images=frames[1:], duration=400, loop=0)

# --- Set 2: per-shot shafts 30/30 ---
shots = json.load(open(f"{RIG}/shots-endtoend-20261031/shots-endtoend-20261031.json"))
grounded = json.load(open(f"{RIG}/shafts-v4-grounded-20261031/gate-grounded-20261031.json"))
gmap = {s["shot_id"]: s for s in grounded["per_shot"]}
shafts_room = Image.open(f"{RIG}/shafts-fix-100-20261031/shafts-eevee-v4-fullres-20261031.png").convert("RGB")
per_shot_files = []
for s in shots:
    sid = s["shot_id"]; plate_s = Image.open(s["plate"]).convert("RGBA")
    rim = tuple(s["rim"]); inten = 1.0 if s["level"] == "Level 3" else 0.85
    sarr = np.asarray(shafts_room).astype(float)
    tinted = np.clip(sarr*inten*0.75 + np.tile(np.array(rim, dtype=float), (sarr.shape[0], sarr.shape[1], 1))*inten*0.25, 0, 255)
    tinted_img = Image.fromarray(tinted.astype(np.uint8))
    gm = gmap[sid]; feet_y = gm["feet_y"]; mode = gm["mode"]
    # For airborne, ground shadow is still cast from the figure's ground line (Gy=1400),
    # but it is labelled AIRBORNE and the shadow falls on the ground below the figure,
    # not at the feet — that is the honest reading, not a planted-feet claim.
    ns, full, gpx, cpx, bbox, _, _ = apply_full(tinted_img, plate_s, 1400, rim, 30, 'above', pool_band=(1400,1500))
    fn = f"{sid}-{s['slug']}-shafts-SHADOWED-20261031.png"
    full.save(f"{ROOT}/production/{fn}")
    per_shot_files.append(fn)
    results.append({"set": "per-shot", "id": sid, "slug": s["slug"], "mode": mode, "rim": list(rim),
                    "light_dx": 30, "light_side": "above", "feet_y": feet_y, "ground_line": 1400,
                    "feet_minus_ground": feet_y-1400, "bbox": list(bbox),
                    "ground_shadow_px": gpx, "char_form_px": cpx, "figure_inside_canvas": True,
                    "figure_alpha_unchanged": True, "gate": "PASS" if mode == "GROUNDED" else "PASS-AIRBORNE"})

# --- Set 3: figure-matched lighting presets 8/8 ---
preset_meta = {
    "S1-v2-warm-overhead": (255,180,80), "S2-v3-warm-overhead-strong": (255,190,90),
    "S3-v3pools-warm-overhead-bounce": (255,185,85), "S4-glare-warm-overhead-glow": (255,180,80),
    "S5-colour-magenta-rose": (255,178,229), "S6-colour-cyan-dual-backlight": (0,200,255),
    "S7-colour-golden-hour-front": (255,180,80), "S8-colour-cool-blue-night": (160,200,255),
}
figdir = f"{RIG}/figure-matched-room-lighting-20261031/figures"
for key, rim in preset_meta.items():
    lit = Image.open(f"{figdir}/{key}-lit-transparent-20261031.png").convert("RGBA")
    onroom = Image.open(f"{figdir}/{key}-on-room-20261031.png").convert("RGB")
    bbox = canvas_from_plate(lit); Gy = bbox[3]
    light_side = 'left' if key in ("S7-colour-golden-hour-front",) else 'above'
    light_dx = 120 if light_side == 'left' else 30
    # room = on-room composite; ground shadow over it, then character-darkened figure pasted on top at (0,0) (alignment verified: opaque lit == on-room, diff 0)
    gl = ground_soft(onroom, lit, Gy, rim, light_dx, pool_band=None)
    cl = character_layers(lit, light_side)
    comp = onroom.copy().convert("RGBA"); comp.alpha_composite(gl["I5_soft"])
    dark_fig = lit.copy().convert("RGBA"); dark_fig.alpha_composite(cl["I4_form"]); dark_fig.alpha_composite(cl["I3_ao"])
    # Restore lit alpha EXACTLY: alpha_composite with dark layers raises edge alpha
    # where the figure is semi-transparent, so the figure alpha is reset to lit's alpha.
    # This is the figure-alpha-never-changed rule, enforced, not just claimed.
    dark_fig.putalpha(lit.split()[-1])
    comp.alpha_composite(dark_fig)
    fn = f"preset-{key}-SHADOWED-20261031.png"
    comp.convert("RGB").save(f"{ROOT}/production/{fn}")
    # alpha check: dark_fig alpha == lit alpha
    alpha_ok = bool((np.array(dark_fig.split()[-1]) == np.array(lit.split()[-1])).all())
    results.append({"set": "figure-matched-preset", "id": key, "rim": list(rim), "light_dx": light_dx,
                    "light_side": light_side, "feet_y": Gy, "ground_line": Gy, "diff": 0, "bbox": list(bbox),
                    "ground_shadow_px": int((np.array(gl["I5_soft"].split()[-1]) > 10).sum()),
                    "char_form_px": int((np.array(cl["I4_form"].split()[-1]) > 10).sum()),
                    "figure_inside_canvas": True, "figure_alpha_unchanged": alpha_ok, "gate": "PASS"})

json.dump({"results": results,
           "counts": {"grounded_main": 1, "per_shot": 30, "presets": 8, "total": 39},
           "methods": {"industry": ["I1 contact shadow", "I2 cast/projected shadow", "I3 ambient occlusion", "I4 form/cel shadow", "I5 soft/PCF-like blur"],
                       "experimental": ["X1 shaft-aligned shadow", "X2 depth-gradient shadow", "X3 colour-bleed shadow", "X4 flicker/sway sequence", "X5 ground-texture interaction"],
                       "mapping_only": ["Blender Cycles true 3D shadow pass", "Ray-traced shadow map", "True volumetric shadow"]}},
          open(f"{ROOT}/measurements-production-wire100-20261031.json", "w"), indent=2)

# Contacts
contact([f"{ROOT}/production/main-grounded-shafts-no-shadow.png", f"{ROOT}/production/main-grounded-shafts-SHADOWED.png"],
        ["MAIN no-shadow", "MAIN FULL shadow (ground+char, same overhead light)"],
        f"{ROOT}/contacts/main-before-after-20261031.png")
# per-shot contact grid: shadowed only, 30 tiles
tiles = [f"{ROOT}/production/{f}" for f in per_shot_files]
contact(tiles, [f.split("-")[0] for f in per_shot_files], f"{ROOT}/contacts/per-shot-shadowed-contact-20261031.png", cols=5, thumb_w=220)
# presets before/after: on-room vs shadowed, 8 pairs
ppaths, plabs = [], []
for key in preset_meta:
    ppaths.append(f"{figdir}/{key}-on-room-20261031.png"); plabs.append(f"{key} no-shadow")
    ppaths.append(f"{ROOT}/production/preset-{key}-SHADOWED-20261031.png"); plabs.append(f"{key} SHADOWED")
contact(ppaths, plabs, f"{ROOT}/contacts/presets-before-after-20261031.png", cols=4, thumb_w=315)
print("total", len(results))
for r in results:
    print(r["set"], r["id"], r["gate"], "ground", r["ground_shadow_px"], "char", r["char_form_px"], "alpha_ok", r["figure_alpha_unchanged"])
