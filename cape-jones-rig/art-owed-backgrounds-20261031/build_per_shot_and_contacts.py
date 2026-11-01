#!/usr/bin/env python3
"""Per-shot canvas-sized BG files + before/after contact sheets.

Masters (1920x1280 media-generated, 1920x1080 / 1920x1280 code-painted) are
centre-cropped to each shot's canvas from shots-endtoend-20261031.json
(1920x1080, room shots 1920x1280). No LUT/rim/effect is baked into a BG file:
shot grading stays with the end-to-end composite lane, exactly as the prior
painted BGs were used (base painting, grade at composite time).
Before thumbnails are the storyboard panels (flat charcoal stand-ins, or for
CJ-29 the rooftop-painted panel used as its night-city stand-in). Labels
appear ONLY on the contact sheets, never inside a BG file.
"""
import json, glob, os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/home/hatch/workspace/cape-jones-rig"
OUT = f"{ROOT}/art-owed-backgrounds-20261031"
MASTERS = {
    "street": glob.glob(f"{OUT}/masters/*bg-street-golden-hour-painted-0-*.png")[0],
    "town": glob.glob(f"{OUT}/masters/*bg-town-golden-hour-painted-ne-0-*.png")[0],
    "stage": glob.glob(f"{OUT}/masters/*bg-stage-magenta-painted-new-2-0-*.png")[0],
    "night-city": glob.glob(f"{OUT}/masters/*bg-night-city-cj29-painted-new-0-*.png")[0],
    "plaza": f"{OUT}/masters/bg-plaza-neutral-painted-code-20261031.png",
    "room": f"{OUT}/masters/bg-room-lounge-painted-code-20261031.png",
}
# shot -> (location, spec family from shots-endtoend JSON)
SHOT_LOC = {
    "CJ-01": "street", "CJ-02": "street", "CJ-03": "street", "CJ-04": "street",
    "CJ-05": "town", "CJ-06": "street", "CJ-07": "town",
    "CJ-09": "stage", "CJ-10": "stage", "CJ-11": "stage",
    "CJ-16": "plaza", "CJ-17": "plaza", "CJ-18": "plaza", "CJ-19": "plaza", "CJ-20": "plaza",
    "CJ-23": "room", "CJ-25": "room", "CJ-27": "room",
    "CJ-29": "night-city",
}
METHOD = {"street": "media-generated", "town": "media-generated", "stage": "media-generated",
          "night-city": "media-generated", "plaza": "code-painted (PIL)",
          "room": "code-painted (PIL)"}

specs = {s["shot_id"]: s for s in json.load(
    open(f"{ROOT}/shots-endtoend-20261031/shots-endtoend-20261031.json"))}
panels = {s["shot"]: s["panel"] for s in json.load(
    open(f"{ROOT}/storyboards-animatic-20261031/panels-manifest-20261031.json"))}


def fit(im, w, h):
    """Centre-crop to aspect, then resize — no stretching, no letterbox."""
    sw, sh = im.size
    ta = w / h
    sa = sw / sh
    if sa > ta:  # too wide: crop sides
        nw = int(sh * ta)
        im = im.crop(((sw - nw) // 2, 0, (sw + nw) // 2, sh))
    else:
        nh = int(sw / ta)
        im = im.crop((0, (sh - nh) // 2, sw, (sh + nh) // 2))
    return im.resize((w, h), Image.LANCZOS)


def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


manifest = []
for shot, loc in SHOT_LOC.items():
    s = specs[shot]
    w, h = s["canvas"]
    master = Image.open(MASTERS[loc]).convert("RGB")
    out = fit(master, w, h)
    name = f"{shot}-bg-{loc}-painted-new-20261031.png"
    out.save(f"{OUT}/per-shot/{name}")
    manifest.append({"shot": shot, "slug": s["slug"], "location": loc, "method": METHOD[loc],
                     "spec_bg_source_before": s["bg_source"], "spec_bg_kind_before": s["bg_kind"],
                     "canvas": [w, h], "file": f"per-shot/{name}",
                     "master": os.path.basename(MASTERS[loc]),
                     "level": s["level"], "rim": s["rim"], "bleed": s["bleed"],
                     "approval": "0/1 PENDING Mars look"})
    print(shot, loc, (w, h), name)

# ---- before/after contact: one row per shot, before panel | after BG ----
TW = 620  # thumb width
rows = []
for shot, loc in SHOT_LOC.items():
    panel = Image.open(f"{ROOT}/storyboards-animatic-20261031/panels/{panels[shot]}").convert("RGB")
    # picture area is the top 1920x1200 of the 1920x1440 panel
    panel = panel.crop((0, 0, 1920, 1200))
    after = Image.open(f"{OUT}/per-shot/{shot}-bg-{loc}-painted-new-20261031.png").convert("RGB")
    rows.append((shot, loc, panel, after))
row_h = 360
sheet = Image.new("RGB", (TW * 2 + 30, 90 + row_h * len(rows)), (24, 22, 28))
d = ImageDraw.Draw(sheet)
d.text((15, 15), "BEFORE (stand-in)  vs  AFTER (new painted BG) — art-owed-backgrounds-20261031",
       fill=(255, 220, 80), font=font(26))
d.text((15, 52), "Before = storyboard panel picture area (flat charcoal stand-in; CJ-29: rooftop painting as night-city stand-in). "
                  "After = new painted BG file, no character, no labels baked in. Approval 0/1.",
       fill=(220, 220, 220), font=font(18))
for i, (shot, loc, panel, after) in enumerate(rows):
    y = 90 + i * row_h
    for x, im, tag in [(0, panel, "BEFORE"), (TW + 30, after, "AFTER")]:
        th = fit(im, TW, row_h - 40)
        sheet.paste(th, (x + 15 if x == 0 else x, y + 34))
    d.text((15, y + 4), f"{shot} — {loc}  |  BEFORE (left)  /  AFTER (right)",
           fill=(255, 255, 255), font=font(20))
sheet.save(f"{OUT}/before-after-contact-20261031.png")
print("contact", sheet.size)

# ---- location masters contact ----
masters = [("street", MASTERS["street"]), ("town", MASTERS["town"]), ("stage", MASTERS["stage"]),
           ("plaza", MASTERS["plaza"]), ("room", MASTERS["room"]), ("night-city", MASTERS["night-city"])]
cell_w, cell_h = 940, 560
ms = Image.new("RGB", (cell_w * 2 + 30, 70 + cell_h * 3), (24, 22, 28))
d = ImageDraw.Draw(ms)
d.text((15, 15), "NEW LOCATION MASTERS — 6/6 (4 media-generated + 2 code-painted, all NEW, none a prior render)",
       fill=(255, 220, 80), font=font(24))
for i, (loc, path) in enumerate(masters):
    x = 15 + (i % 2) * cell_w
    y = 70 + (i // 2) * cell_h
    th = fit(Image.open(path).convert("RGB"), cell_w - 30, cell_h - 40)
    ms.paste(th, (x, y + 34))
    d.text((x, y + 4), f"{loc} — {METHOD[loc]} — {os.path.basename(path)}",
           fill=(255, 255, 255), font=font(19))
ms.save(f"{OUT}/location-masters-contact-20261031.png")
print("masters contact", ms.size)

json.dump({"locations": {k: {"master": os.path.basename(v), "method": METHOD[k],
                            "shots": sorted(s for s, l in SHOT_LOC.items() if l == k)}
                          for k, v in MASTERS.items()},
           "per_shot": manifest,
           "counts": {"new_painted_shots": len(manifest),
                      "painted_before": "15/30 shots (shots-endtoend count; CJ-29 counted there on graded rooftop)",
                      "painted_after": "30/30 = 100% (14 prior distinct + CJ-26 existing composite + 19 new, "
                                       "with CJ-29's graded-rooftop stand-in replaced by its own night-city painting; "
                                       "CJ-23/25/27 room-proof canvas replaced by the new lounge-room painting)",
                      "approval": "0/1 for the painted background set"}},
          open(f"{OUT}/manifest-20261031.json", "w"), indent=1)
print("manifest written")
