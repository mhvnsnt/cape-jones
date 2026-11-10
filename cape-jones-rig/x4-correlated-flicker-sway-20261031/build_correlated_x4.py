#!/usr/bin/env python3
"""X4 correlated flicker-sway, 2026-10-31.
DEFECT (Mars, 23:48 CDT, correct): old X4 moved ONLY the ground cast
(offsets -6/0/+6 on light_dx in ground_layers), while character layers
(I4 form, I3 AO) were built ONCE and pasted unchanged into every frame.
So the ground shadow swayed and the figure's shadow did not.

FIX — one light parameter drives EVERYTHING, per frame:
  light_dx(frame) = 30 + off, off in [-6, 0, +6] (3f) or [-8,-4,0,+4,+8] (5f)
  * ground cast: squashed figure alpha, sheared by light_dx (same code as
    shadows-wire100, so ground motion is unchanged in kind)
  * form terminator: term_x = figure_centre_x + 2.0*off  (C2/X-C1)
    dark alpha = clip((term_x - x)/fw * 0.56 + 0.14, 0, 0.28) inside figure
    -> at x == term_x the dark alpha is exactly half-max (0.14), so the
    terminator is MEASURABLE per frame, and it moves +12/0/-12 px.
  * self-cast: upper side-caster shifted by (20 + 2*off) px, intersected
    with torso/legs only, darkened 0.35 (C3)
  * rim: dilate(figure,6)-figure, masked to the LIT side
    (x > term_x, light is to the right when dx>0), rim (255,180,80) (C4)
  * AO: static <12px band at 25%, plus a small away-side modulation
    (X-C2): AO alpha on the away side scales 1.0 + 0.02*off magnitude
    direction — AO is contact darkening, it does NOT translate, and
    that is stated, not hidden. The moving character shadows are
    form + self-cast + rim; AO only breathes slightly.
  * ground+character share the same dx, same frame, same sign (C1, C5).
    Cast length/shear grows with light_dx, form terminator moves
    the same direction as the cast shear shift.

Character darkening is applied to a COPY of the figure RGBA, then its
alpha channel is reset EXACTLY to the original figure alpha, so the
figure alpha is unchanged by construction. Ground layers sit BEHIND
the figure. Base art is never recoloured in place.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/cape-jones-rig/x4-correlated-flicker-sway-20261031")
ROOM = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/shafts-fix-100-20261031/shafts-eevee-v4-fullres-20261031.png")).convert("RGB")
FIG0 = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png")).convert("RGBA")
RIM = (255, 180, 80)
TINT = tuple(int(round(0.18 * c)) for c in RIM)  # (46,32,14), never pure black
GY, CENTRE_X, BASE_DX = 1400, 550, 30
W, H = ROOM.size

def paste_fig(fig, feet_y=GY, centre_x=CENTRE_X):
    a = np.array(fig.split()[-1]); ys, xs = np.where(a > 10)
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    px = centre_x - (bbox[0] + bbox[2]) // 2; py = feet_y - bbox[3]
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0)); canvas.paste(fig, (px, py))
    return canvas, (bbox[0]+px, bbox[1]+py, bbox[2]+px, bbox[3]+py)

CANVAS, BBOX = paste_fig(FIG0)
ALPHA = np.array(CANVAS.split()[-1]).astype(np.float32) / 255.0
MASK = ALPHA > 0.04
FX0, FY0, FX1, FY1 = BBOX; FCX = (FX0 + FX1) // 2; FW = FX1 - FX0
print("canvas bbox", BBOX, "fcx", FCX, "fw", FW, "alpha>10", int((np.array(CANVAS.split()[-1]) > 10).sum()))

def ground_soft(light_dx):
    """I5 soft ground shadow: contact ellipse + squashed/sheared cast, blurred."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([FCX - FW*0.58, GY-6, FCX + FW*0.58, GY+42], fill=TINT + (200,))
    contact = im.filter(ImageFilter.GaussianBlur(10))
    squashed = CANVAS.resize((W, max(1, int(H*0.28))), Image.LANCZOS)
    placed = Image.new("RGBA", (W, H), (0, 0, 0, 0)); placed.paste(squashed, (0, GY-20))
    arr = np.array(placed); out = np.zeros_like(arr)
    for y in range(H):
        shift = int(light_dx * max(0, (y - GY)) / 120.0)
        if shift > 0: out[y, shift:, :] = arr[y, :W-shift, :]
        elif shift < 0: out[y, :W+shift, :] = arr[y, -shift:, :]
        else: out[y] = arr[y]
    ca = np.array(Image.fromarray(out).split()[-1]).astype(np.float32) / 255.0
    col = np.zeros((H, W, 4), dtype=np.uint8); col[..., 0], col[..., 1], col[..., 2] = TINT
    col[..., 3] = (ca * 190).astype(np.uint8)
    cast = Image.fromarray(col).filter(ImageFilter.GaussianBlur(12))
    u = Image.new("RGBA", (W, H), (0, 0, 0, 0)); u.alpha_composite(contact); u.alpha_composite(cast)
    return u.filter(ImageFilter.GaussianBlur(12)), cast

def character_figure(off, fixed=False):
    """Return (figure RGBA with correlated char shadows, diagnostics dict).
    fixed=True reproduces the OLD defect: form terminator/self-cast/rim
    built at off=0 regardless of the frame's off."""
    o = 0.0 if fixed else float(off)
    term_x = FCX + 2.0 * o
    xs = np.arange(W)[None, :].repeat(H, axis=0).astype(np.float32)
    # form: dark 0.28 at far away (left) edge, 0 at lit (right) edge,
    # 0.14 exactly at term_x
    form_a = np.clip((term_x - xs) / FW * 0.56 + 0.14, 0, 0.28)
    form_a = np.where(MASK, form_a, 0)
    # self-cast: upper side-caster, shifted (20 + 2*o) px, intersect torso/legs
    # self-cast: upper side-caster, projected DOWN onto the body by the
    # light (shift_x = 20 + 2*o, shift_y = +40), intersected with the body.
    # The caster and the receiver must overlap in Y — the old version of
    # this code used disjoint Y bands, which gave 0 px and was caught here.
    caster = MASK & (np.arange(H)[:, None].repeat(W, axis=1) < FY0 + 540) & ((xs < FCX - 150) | (xs > FCX + 150))
    shift = int(round(20 + 2 * o))
    caster_s = np.zeros_like(caster)
    caster_s[40:, shift:] = caster[:-40, :-shift] if shift > 0 else caster[:-40, -shift:]
    torso = MASK & (np.arange(H)[:, None].repeat(W, axis=1) > FY0 + 200)
    selfcast = caster_s & torso
    # AO: static band, away-side breathes slightly with |off|
    dist = ndimage.distance_transform_edt(MASK)
    ao = np.where((dist < 12) & MASK, 0.25, 0)
    ao = np.where(xs < term_x, ao * (1.0 + 0.02 * abs(o)), ao)
    # rim: dilate-figure band, lit side only (x > term_x)
    dil = ndimage.binary_dilation(MASK, iterations=6)
    rim_mask = dil & (~MASK) & (xs > term_x)
    fig = np.array(CANVAS).astype(np.float32)
    dark = form_a + np.where(selfcast, 0.35, 0) + ao
    dark = np.clip(dark, 0, 0.75)
    fig[..., 0:3] *= (1 - dark[..., None])
    out = Image.fromarray(fig.astype(np.uint8))
    # rim on top, then restore alpha EXACTLY
    rim_im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ra = np.zeros((H, W, 4), dtype=np.uint8); ra[..., 0], ra[..., 1], ra[..., 2] = RIM
    ra[..., 3] = np.where(rim_mask, 200, 0).astype(np.uint8)
    out.alpha_composite(Image.fromarray(ra))
    arr = np.array(out); arr[..., 3] = np.array(CANVAS.split()[-1])
    out = Image.fromarray(arr)
    # diagnostics
    # terminator: along rows in the torso band, x where form_a crosses 0.14
    terms = []
    for y in range(FY0 + 350, FY0 + 650, 25):
        row = np.where(MASK[y])[0]
        if len(row) < 50: continue
        fa = form_a[y, row]
        idx = np.argmin(np.abs(fa - 0.14))
        terms.append(float(row[idx]))
    diag = {
        "off": off, "term_x_expected": float(term_x),
        "term_x_measured_median": float(np.median(terms)) if terms else None,
        "selfcast_px": int(selfcast.sum()), "rim_px": int(rim_mask.sum()),
        "form_px": int((form_a > 0.01).sum()),
        "alpha_unchanged": bool(np.array_equal(np.array(out.split()[-1]), np.array(CANVAS.split()[-1]))),
    }
    return out, diag

def composite(off, fixed_char=False, ground_off=None):
    go = off if ground_off is None else ground_off
    soft, cast = ground_soft(BASE_DX + go)
    fig, diag = character_figure(off, fixed=fixed_char)
    comp = ROOM.copy().convert("RGBA"); comp.alpha_composite(soft); comp.alpha_composite(fig)
    # ground cast centroid (below feet, alpha>10 in soft layer, y>=GY)
    sa = np.array(soft.split()[-1]); ys, xs = np.where((sa > 10) & (np.arange(H)[:, None] >= GY))
    diag["ground_cast_centroid_x"] = float(xs.mean()) if len(xs) else None
    diag["ground_cast_px"] = int((sa > 10).sum())
    diag["feet_y"] = GY
    return comp.convert("RGB"), diag, soft

def contact_sheet(paths, labels, out, cols=3, thumb_w=366):
    thumbs = []
    for p in paths:
        im = Image.open(p).convert("RGB"); im.thumbnail((thumb_w, 500)); thumbs.append(im)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols*thumb_w, rows*530), (40, 40, 40)); d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(thumbs, labels)):
        x = (i % cols) * thumb_w; y = (i // cols) * 530
        sheet.paste(im, (x, y+28)); d.text((x+8, y+6), lab, fill=(255, 255, 0))
    sheet.save(out)

results = {"base": {"bbox": BBOX, "fcx": FCX, "fw": FW, "gy": GY, "base_dx": BASE_DX},
           "frames_3f": [], "frames_5f": [], "frames_old": []}

# OLD (defect reproduction): ground moves, character fixed at off=0
old_frames = []
for off in [-6, 0, 6]:
    comp, diag, _ = composite(off, fixed_char=True, ground_off=off)
    p = f"{ROOT}/frames_old/old-f{off:+d}.png"; comp.save(p); old_frames.append(comp)
    diag["kind"] = "OLD-defect"; results["frames_old"].append(diag)
Image.open(f"{ROOT}/frames_old/old-f-6.png").save(
    f"{ROOT}/x4-OLD-defect-3f.gif", save_all=True,
    append_images=[Image.open(f"{ROOT}/frames_old/old-f+0.png"), Image.open(f"{ROOT}/frames_old/old-f+6.png")],
    duration=400, loop=0)

# NEW correlated 3f
new_frames = []
for off in [-6, 0, 6]:
    comp, diag, _ = composite(off)
    p = f"{ROOT}/frames/new-f{off:+d}.png"; comp.save(p); new_frames.append(comp)
    diag["kind"] = "NEW-correlated"; results["frames_3f"].append(diag)
new_frames[0].save(f"{ROOT}/x4-CORRELATED-3f.gif", save_all=True, append_images=new_frames[1:], duration=400, loop=0)

# NEW correlated 5f (smoothstep sway, X-C5)
new5 = []
for off in [-8, -4, 0, 4, 8]:
    comp, diag, _ = composite(off)
    p = f"{ROOT}/frames/new5-f{off:+d}.png"; comp.save(p); new5.append(comp)
    diag["kind"] = "NEW-correlated-5f"; results["frames_5f"].append(diag)
new5[0].save(f"{ROOT}/x4-CORRELATED-5f.gif", save_all=True, append_images=new5[1:], duration=300, loop=0)

# Correlation gate: ground centroid AND terminator must move same sign, monotonic with off
def gate(rows):
    offs = [r["off"] for r in rows]; g = [r["ground_cast_centroid_x"] for r in rows]; t = [r["term_x_measured_median"] for r in rows]
    mono_g = all(g[i] < g[i+1] for i in range(len(g)-1)); mono_t = all(t[i] < t[i+1] for i in range(len(t)-1))
    return {"ground_centroids": g, "terminators": t, "ground_monotonic_up": mono_g, "terminator_monotonic_up": mono_t,
            "ground_delta_total": g[-1]-g[0], "terminator_delta_total": t[-1]-t[0], "PASS": bool(mono_g and mono_t)}
results["gate_3f_new"] = gate(results["frames_3f"])
results["gate_3f_old"] = gate(results["frames_old"])
results["gate_5f_new"] = gate(results["frames_5f"])
print(json.dumps(results, indent=2))
with open(f"{ROOT}/measurements-x4-correlated-20261031.json", "w") as f: json.dump(results, f, indent=2)

contact_sheet(
    [f"{ROOT}/frames_old/old-f-6.png", f"{ROOT}/frames_old/old-f+0.png", f"{ROOT}/frames_old/old-f+6.png",
     f"{ROOT}/frames/new-f-6.png", f"{ROOT}/frames/new-f+0.png", f"{ROOT}/frames/new-f+6.png"],
    ["OLD f-6 (ground moves)", "OLD f0", "OLD f+6 (char fixed)", "NEW f-6 (ground+char)", "NEW f0", "NEW f+6 (char moves)"],
    f"{ROOT}/contacts/old-vs-new-contact-20261031.png")
contact_sheet(
    [f"{ROOT}/frames/new5-f-8.png", f"{ROOT}/frames/new5-f-4.png", f"{ROOT}/frames/new5-f+0.png", f"{ROOT}/frames/new5-f+4.png", f"{ROOT}/frames/new5-f+8.png"],
    ["NEW5 f-8", "NEW5 f-4", "NEW5 f0", "NEW5 f+4", "NEW5 f+8"],
    f"{ROOT}/contacts/new5-contact-20261031.png", cols=5, thumb_w=220)
print("GATES:", results["gate_3f_new"], results["gate_3f_old"], results["gate_5f_new"])
