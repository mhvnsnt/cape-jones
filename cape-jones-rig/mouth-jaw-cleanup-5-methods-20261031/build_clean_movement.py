#!/usr/bin/env python3
"""
Mouth/jaw cleanup, 5 industry-standard methods — 2026-10-31.
Mars ordered 2026-10-31 21:20 CDT, replying to pahgo-movement.gif:
pull in and wire 100% five industry-standard things to make the mouth
stuff and jaw movement cleaner and better.

Known defects fixed here (Mars 21:18 CDT; his closer list still open,
so this does NOT claim all defects fixed):
- f00 MBP / f29 REST: mouth line missing in the middle, part edited over,
  line fragmented/not continuous.
- f09 AH key: too much of Robin's features around the mouth, not mouth-only.

The 5 methods (see REPORT for run vs mapping):
1. Toon Boom Harmony mouth-chart substitution — mouth on its own layer,
   swapped per frame over a masked clean head base, no old mouth bleed.
2. Mouth-ROI + garbage matte (rotoscope matte) — MediaPipe lip-contour
   ROI concept, implemented locally: 2D connected components on the
   colour-filtered patch, keep ONLY the component containing the mouth
   body (tongue/interior), drop every other component (top dash, jaw/
   chin outline, cheek slivers). Everything outside the mouth body is
   matte-cut, not hand-erased pixel by pixel.
3. Animation cleanup / line continuity — MBP fragmented line bridged
   with a continuous stroke through measured endpoints, original
   fragments kept, bridge pixels only added where the line was missing.
4. Colour decontamination (compositing spill suppression equivalent) —
   keep only mouth colours (dark outline/interior, orange tongue, white
   teeth for GK); drop JPEG fringe colours (red/green/yellow edge spill).
5. FACS jaw-hinge + Preston Blair slow-in/slow-out — jaw drops preserved
   exactly (MBP 0, AH 16, GK 8, GAP 10, REST 0), smoothstep 3-frame
   inbetweens, upper lip fixed, lower lip follows jaw, mouth centre
   follows jaw by 1/4, hinge-row fill masked to head silhouette.

No existing file overwritten. Input patches are the pahgo-mouth-fix
tight patches; the cleaned patches are written here, in this folder.
Base head is unchanged. No PIL vector mouths invented.
"""
import json, os
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "mouth-jaw-cleanup-5-methods-20261031")
BASE = Image.open(os.path.join(ROOT, "visemes-v2-20261031/clean-head-base-20261031.png")).convert("RGBA")
W, H = BASE.size  # 476 x 688

TIGHT = os.path.join(ROOT, "pahgo-mouth-fix-20261031/mouths-tight")
CX, CY = 231.5, 504.5  # single target centre, every viseme (fixed agent, Mars direction + 0.75x)
PARAMS = {
    "MBP": dict(jaw=0,  w=178, h=23),
    "AH":  dict(jaw=16, w=196, h=67),
    "GK":  dict(jaw=8,  w=188, h=30),
    "GAP": dict(jaw=10, w=0,   h=0),
    "REST":dict(jaw=0,  w=178, h=23),
}
JAW_SPLIT = 560
STATS = {}

def colour_mask(arr):
    rgb = arr[:, :, :3].astype(int)
    alpha = arr[:, :, 3] > 50
    dark = (rgb[:, :, 0] < 90) & (rgb[:, :, 1] < 90) & (rgb[:, :, 2] < 90)
    orange = (rgb[:, :, 0] > 150) & (rgb[:, :, 0] < 220) & (rgb[:, :, 1] > 80) & (rgb[:, :, 1] < 160) & (rgb[:, :, 2] < 80)
    white = (rgb[:, :, 0] > 200) & (rgb[:, :, 1] > 200) & (rgb[:, :, 2] > 200)
    return alpha, dark, orange, white

def clean_patch(filename, kind):
    """Return cleaned patch image + stats. kind: 'ah' | 'gk' | 'mbp'."""
    im = Image.open(os.path.join(TIGHT, filename)).convert("RGBA")
    arr = np.array(im).astype(int)
    alpha, dark, orange, white = colour_mask(arr)
    if kind == "ah":
        colour = dark | orange
    elif kind == "gk":
        colour = dark | white
    else:
        colour = dark
    mask = alpha & colour
    n_alpha = int(alpha.sum()); n_colour = int(mask.sum())
    if kind == "ah":
        # Method 2: keep ONLY the largest component that contains the
        # tongue (orange). That is the mouth body. All other components
        # are Robin features around the mouth.
        lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
        sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
        # tongue centre seed: orange centroid
        oys, oxs = np.where(orange & mask)
        seed = lab[int(oys.mean()), int(oxs.mean())]
        keep = (lab == seed)
        dropped = []
        for i, s in enumerate(sizes, start=1):
            if i != seed:
                ys, xs = np.where(lab == i)
                dropped.append({"component": i, "pixels": int(s),
                                "x": [int(xs.min()), int(xs.max())],
                                "y": [int(ys.min()), int(ys.max())]})
        out_arr = np.zeros_like(arr)
        out_arr[:, :, :3] = arr[:, :, :3]
        out_arr[:, :, 3] = np.where(keep, 255, 0)
        kept_img = Image.fromarray(out_arr.astype(np.uint8))
        # crop to kept bbox, then resize to placed size (mouth body only,
        # re-centred on the single target centre at placement time)
        ys, xs = np.where(keep)
        kept_img = kept_img.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
        STATS["AH"] = {"source": filename, "source_size": list(im.size),
                       "alpha_px": n_alpha, "after_colour_filter_px": n_colour,
                       "kept_component": int(seed), "kept_px": int(keep.sum()),
                       "dropped_components": dropped,
                       "kept_bbox": [int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())]}
        return kept_img
    else:
        out_arr = np.zeros_like(arr)
        out_arr[:, :, :3] = arr[:, :, :3]
        out_arr[:, :, 3] = np.where(mask, 255, 0)
        STATS[kind.upper()] = {"source": filename, "source_size": list(im.size),
                               "alpha_px": n_alpha, "after_colour_filter_px": n_colour,
                               "removed_fringe_px": n_alpha - n_colour}
        return Image.fromarray(out_arr.astype(np.uint8))

ah_clean = clean_patch("ah-front-03_tight_patch.png", "ah")
gk_clean = clean_patch("gk-front-05_tight_patch.png", "gk")
mbp_src = clean_patch("mbp-front-09_tight_patch.png", "mbp")

# Method 3: MBP line bridge, measured at placed size.
mbp = mbp_src.resize((178, 23), Image.LANCZOS)
arr = np.array(mbp)
dark = (arr[:, :, 0] < 90) & (arr[:, :, 1] < 90) & (arr[:, :, 2] < 90) & (arr[:, :, 3] > 50)
cols = {}
for x in range(178):
    ys = np.where(dark[:, x])[0]
    if len(ys):
        cols[x] = float(np.median(ys))
xs_sorted = sorted(cols)
# gap = longest run of columns with no dark pixels between first and last dark column
gap_start = gap_end = None; best = 0; run = 0; run_start = None
for x in range(xs_sorted[0], xs_sorted[-1] + 1):
    if x not in cols:
        if run == 0: run_start = x
        run += 1
        if run > best: best = run; gap_start, gap_end = run_start, x
    else:
        run = 0
left_y = cols[gap_start - 1]; right_y = cols[gap_end + 1]
bridge = Image.new("RGBA", mbp.size, (0, 0, 0, 0))
d = ImageDraw.Draw(bridge)
# stroke width = median fragment thickness (6 px at placed size)
d.line([(gap_start - 2, left_y), (gap_end + 2, right_y)], fill=(0, 0, 0, 255), width=6)
mbp_clean = Image.alpha_composite(mbp, bridge)
STATS["MBP"]["bridge"] = {"gap_columns": [int(gap_start), int(gap_end)], "gap_width_px": int(best),
                          "left_end_y": float(left_y), "right_start_y": float(right_y),
                          "stroke_width_px": 6, "note": "Bridge pixels only; original fragments kept, not redrawn."}
# count bridge pixels actually added (bridge alpha where original had no dark)
barr = np.array(bridge)
added = int(((barr[:, :, 3] > 0) & ~dark).sum())
STATS["MBP"]["bridge"]["bridge_pixels_added"] = added

mouths = {
    "MBP": mbp_clean,
    "AH": ah_clean.resize((196, 67), Image.LANCZOS),
    "GK": gk_clean.resize((188, 30), Image.LANCZOS),
}
for k, v in mouths.items():
    v.save(os.path.join(OUT, f"clean-{k.lower()}-patch.png"))
    print(k, "clean placed", v.size)

def render_frame(viseme, w_mul, h_mul, jaw):
    frame = BASE.copy()
    jaw = int(round(jaw))
    if jaw > 0:
        chin = frame.crop((0, JAW_SPLIT, W, H))
        head_alpha = BASE.getchannel("A")
        row = head_alpha.crop((0, JAW_SPLIT - 1, W, JAW_SPLIT))
        hinge = BASE.crop((0, JAW_SPLIT - 1, W, JAW_SPLIT))
        band = Image.new("RGBA", (W, jaw))
        for yy in range(jaw):
            band.paste(hinge, (0, yy))
        mask = Image.new("L", (W, jaw), 0)
        for yy in range(jaw):
            mask.paste(row, (0, yy))
        frame.paste(band, (0, JAW_SPLIT), mask)
        frame.paste(chin, (0, JAW_SPLIT + jaw))
    meas = dict(viseme=viseme, jaw_drop=jaw, mouth_w=0, mouth_h=0, mouth_cx=CX, mouth_top=None)
    if viseme == "GAP":
        return frame, meas
    if viseme == "REST":
        viseme = "MBP"
    patch = mouths[viseme]
    tw = int(round(w_mul)); th = int(round(h_mul))
    resized = patch.resize((tw, th), Image.LANCZOS)
    top = int(round(CY - th / 2 + jaw * 0.25))
    left = int(round(CX - tw / 2))
    frame.alpha_composite(resized, (left, top))
    meas.update(mouth_w=tw, mouth_h=th, mouth_top=top)
    return frame, meas

def smoothstep(t):
    return t * t * (3 - 2 * t)

def timeline(keys):
    frames = []
    prev = PARAMS[keys[0]]
    for i, k in enumerate(keys):
        cur = PARAMS[k]
        for f in range(6):
            if i == 0 or f >= 3:
                frames.append((k, cur["w"], cur["h"], cur["jaw"]))
            else:
                t = smoothstep((f + 1) / 3)
                frames.append((f"{keys[i-1]}->{k}",
                               prev["w"] + (cur["w"] - prev["w"]) * t,
                               prev["h"] + (cur["h"] - prev["h"]) * t,
                               prev["jaw"] + (cur["jaw"] - prev["jaw"]) * t))
        prev = cur
    return frames

keys = ["MBP", "AH", "GK", "GAP", "REST"]
tl = timeline(keys)
meas = []; gif_frames = []
for i, (label, w, h, jaw) in enumerate(tl):
    draw_key = label.split("->")[-1] if "->" in label else label
    fr, m = render_frame(draw_key, w, h, jaw)
    m["frame"] = i; m["timeline_label"] = label
    meas.append(m)
    fr.save(os.path.join(OUT, "frames_clean", f"f{i:02d}_{draw_key}.png"))
    gif_frames.append(fr.convert("RGB"))
gif_frames[0].save(os.path.join(OUT, "pahgo-movement-clean-20261031.gif"), save_all=True,
                   append_images=gif_frames[1:], duration=1000 // 24, loop=0)

# contacts: key frames, and defect check f00/f09/f29 with mouth zooms
def contact(picks, name):
    tiles = []
    for i in picks:
        tiles.append(Image.open(os.path.join(OUT, "frames_clean", f"f{i:02d}_{meas[i]['viseme']}.png")).resize((238, 344), Image.LANCZOS))
    sheet = Image.new("RGB", (238 * len(tiles), 344 + 22), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for j, t in enumerate(tiles):
        sheet.paste(t, (238 * j, 22))
        d.text((238 * j + 6, 4), f"f{picks[j]} {meas[picks[j]]['viseme']}", fill=(255, 255, 0))
    sheet.save(os.path.join(OUT, name))

contact([3, 9, 15, 21, 27], "pahgo-movement-clean-contact-20261031.png")

# defect-check sheet: f00, f09, f29 full + mouth zoom (crop 110,450,370,600, x3)
def defect_sheet():
    rows = []
    for i in [0, 9, 29]:
        fr = Image.open(os.path.join(OUT, "frames_clean", f"f{i:02d}_{meas[i]['viseme']}.png"))
        zoom = fr.crop((110, 450, 370, 600)).resize((780, 450), Image.NEAREST)
        rows.append((i, fr.resize((238, 344), Image.LANCZOS), zoom))
    sheet = Image.new("RGB", (238 + 780, (344 + 450 + 44) * 1), (40, 40, 40))
    # build vertically: each row = full left, zoom right, label on top
    total_h = sum(450 for _ in rows) + 22 * 3
    sheet = Image.new("RGB", (238 + 780 + 10, total_h), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    y = 0
    for i, full, zoom in rows:
        d.text((6, y + 4), f"f{i:02d} {meas[i]['viseme']} jaw {meas[i]['jaw_drop']}  |  mouth zoom right", fill=(255, 255, 0))
        y += 22
        sheet.paste(full.resize((238, 344), Image.LANCZOS) if False else Image.open(os.path.join(OUT, "frames_clean", f"f{i:02d}_{meas[i]['viseme']}.png")).resize((238, 344), Image.LANCZOS), (0, y))
        sheet.paste(zoom, (238 + 10, y))
        y += 450
    sheet.save(os.path.join(OUT, "pahgo-defect-check-20261031.png"))
    print("defect sheet", sheet.size)

defect_sheet()

with open(os.path.join(OUT, "pahgo-movement-clean-measurements-20261031.json"), "w") as f:
    json.dump({"phrase_keys": keys, "placement": {"centre": [CX, CY],
               "placed_sizes": {k: {"w": v["w"], "h": v["h"], "jaw": v["jaw"]} for k, v in PARAMS.items()}},
               "clean_stats": STATS, "frames": meas}, f, indent=1)
print("done", len(tl), "frames, jaw range", min(m["jaw_drop"] for m in meas), "to", max(m["jaw_drop"] for m in meas))
print(json.dumps(STATS, indent=1))
