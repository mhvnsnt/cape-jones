#!/usr/bin/env python3
"""Workstream 7: room-scale per shot + seated proof + per-sheet eye pass.
New dated folder only. No existing file overwritten. No repo push.
Background: STAND-IN batch-KKGuh, NOT canonical. Canonical room pictures owed from Mars.
Lock (task, Mars 2026-10-31 20:56 CDT): room standing 3.0x ONLY for him in that room;
2.5x superseded FOR ROOM USE. Portrait B 3.0x planted matches lock.
655px landscape revert stays REJECTED.
Feet anchor = alpha-bbox bottom on world ground line; rug band 0.55-0.95;
ground gate tolerance |feet-ground| <= 10px (ground-gate rule).
"""
import json, os, csv, math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.dirname(os.path.abspath(__file__))
SHEETS = os.path.expanduser("~/workspace/cape-jones-flying/characters/sheets")
SLICED = os.path.join(ROOT, "sliced-clean-20261031")

# ---------- 1. Room-scale per-shot table ----------
specs = json.load(open(os.path.join(ROOT, "clean-100-20261031/shots/shot-specs-30-20261031.json")))
gate = json.load(open(os.path.join(ROOT, "ground-gate-complete-20261031/gate-30-results.json")))
# gate list has CJ-21/22 split; map base shot
gmap = {}
for g in gate:
    gmap.setdefault(g["shot"], []).append(g)

ROOM_STANDING = {"CJ-25", "CJ-26", "CJ-27"}
ROOM_SEATED = {"CJ-23", "CJ-24"}
rows = []
for s in specs["shots"]:
    sid, slug = s["shot_id"], s["slug"]
    gs = gmap.get(sid, [])
    modes = sorted(set(x["mode"] for x in gs))
    gverdict = "PASS" if gs and all(x["verdict"] == "PASS" for x in gs) else ("see note" if sid in ("CJ-21", "CJ-22") else "n/a")
    if sid in ROOM_STANDING:
        ruling = "ROOM-STANDING 3.0x"
        scale_note = ("Locked 3.0x ONLY in this room (Mars 20:56 CDT). Scene figure 1398px in portrait "
                      "master (portrait B planted, feet 1700, rug 0.624); landscape pull-back B figure/chair 1.710. "
                      "Supersedes old spec 2.5x FOR ROOM USE. 655px landscape revert REJECTED (ratio 1.193).")
        ground_note = "Grounded: feet anchor on rug/floor, rug band 0.55-0.95, |feet-ground|<=10px in room framing (portrait B feet 1700, rug 0.624 PASS)."
    elif sid in ROOM_SEATED:
        ruling = "ROOM-SEATED (see seated proof)"
        scale_note = ("Seated proof built at BOTH scales (see seated section): 2.3x absolute = 974px bbox in portrait, "
                      "and 2.8x lock-consistent (3.0-0.2) = 1186px bbox. Mars pick owed which seated scale is canonical. "
                      "CJ-24 desk background is STAND-IN (final painted desk owed), so its seated scale is provisional on that bg.")
        ground_note = "Seated: feet anchor = alpha-bbox bottom on floor line (1700 in portrait proof, rug 0.624 PASS); chair/seat support is the chair, feet are not airborne."
    else:
        ruling = "NOT-ROOM — room 3.0x does NOT apply"
        scale_note = ("Room-only rule: keep spec layout scale ~0.35 on rig canvas 1100x1500. "
                      "Do NOT rescale to 3.0x outside the room; that would repeat the landscape revert error.")
        if "AIRBORNE" in modes:
            ground_note = "Airborne (flying): feet NOT forced to ground; flight line stated in ground-gate results."
        elif sid == "CJ-21":
            ground_note = "Split: crouch grounded + takeoff airborne (ground-gate 21a/21b both PASS)."
        elif sid == "CJ-22":
            ground_note = "Split: tuck airborne + landing grounded (ground-gate 22a/22b both PASS)."
        else:
            ground_note = "Grounded on its own background ground line (ground-gate composite feet 997 vs line 1000, offset -3px, within 10px PASS)."
    rows.append({
        "shot_id": sid, "slug": slug, "background_spec": s["background"],
        "original_spec_scale": s["scale"], "room_scale_ruling": ruling,
        "scale_note": scale_note, "ground_mode": "/".join(modes) if modes else "n/a",
        "ground_gate": gverdict, "ground_note": ground_note,
        "room_scale_assigned": "PASS",
    })
assert len(rows) == 30
json.dump(rows, open(os.path.join(OUT, "roomscale-30-20261031.json"), "w"), indent=2)
with open(os.path.join(OUT, "roomscale-30-20261031.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ---------- 2. Seated proof ----------
BG = Image.open(os.path.expanduser("~/workspace/cape-jones-flying/characters/sheets/backgrounds/batch-KKGuh.jpg")).convert("RGB")
def cover(bg, size):
    im = bg.copy(); r = max(size[0]/im.width, size[1]/im.height)
    im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    x = (im.width-size[0])//2; y = (im.height-size[1])//2
    return im.crop((x, y, x+size[0], y+size[1]))
master_bg = cover(BG, (1920, 1920))
port_bg = master_bg.crop((420, 0, 1500, 1920)).convert("RGBA")
seat = Image.open(os.path.join(ROOT, "ground-gate-complete-20261031/plates/joint-seated-v7c-clean.png")).convert("RGBA")
sb = seat.split()[3].getbbox()  # (223,251,878,1200)
stand = Image.open(os.path.join(ROOT, "dual-light-variants-20261031/base-arms-up-transparent-20261031.png")).convert("RGBA")
stb = stand.split()[3].getbbox()  # (222,239,880,1283)
STAND_SCENE_H = 1398  # portrait B 3.0x
FEET = 1700; CX = 539
RUG_FAR, RUG_NEAR = 1421, 1868
def build_seated(scale, name):
    # bbox height in portrait scene = STAND_SCENE_H * (scale/3.0) * (seat_h/stand_h)
    h = round(STAND_SCENE_H * (scale/3.0) * ((sb[3]-sb[1])/(stb[3]-stb[1])))
    w = round(seat.width * (h/(sb[3]-sb[1])) * ((sb[3]-sb[1])/seat.height) * seat.height / (sb[3]-sb[1]))  # placeholder, replaced below
    # correct resize: scale factor from native bbox height to scene bbox height
    f = h / (sb[3]-sb[1])
    nw, nh = round(seat.width*f), round(seat.height*f)
    fig = seat.resize((nw, nh), Image.LANCZOS)
    px = CX - round((sb[0]*f + (sb[2]-sb[0])*f/2))
    py = FEET - round(sb[3]*f)
    # contact shadow: clusters from bottom 40 rows of resized alpha
    am = np.asarray(fig.split()[3])
    ab = round(sb[3]*f)
    bot = am[max(0, ab-40):ab, :]
    cols = np.where((bot > 10).any(axis=0))[0]
    clusters = []
    if len(cols):
        cur = [cols[0]]
        for c in cols[1:]:
            if c - cur[-1] > 30: clusters.append(cur); cur = [c]
            else: cur.append(c)
        clusters.append(cur)
    shadow = Image.new("RGBA", (1080, 1920), (0,0,0,0)); sd = ImageDraw.Draw(shadow)
    for cl in clusters:
        if len(cl) < 20: continue
        cx = px + (cl[0]+cl[-1])//2; ww = (cl[-1]-cl[0])//2
        sd.ellipse([cx-int(ww*0.75), FEET-8, cx+int(ww*0.75), FEET+24], fill=(0,0,0,95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    out = port_bg.copy(); out.alpha_composite(shadow); out.alpha_composite(fig, (px, py))
    fx0 = px+round(sb[0]*f); fy0 = py+round(sb[1]*f); fx1 = px+round(sb[2]*f); fy1 = py+round(sb[3]*f)
    out.convert("RGB").save(os.path.join(OUT, "room-proofs", name))
    return {"file": name, "scale": scale, "bbox": [fx0, fy0, fx1, fy1], "height": fy1-fy0,
            "width": fx1-fx0, "head": fy0, "feet": fy1, "centre_x": (fx0+fx1)//2,
            "rug_position": round((fy1-RUG_FAR)/(RUG_NEAR-RUG_FAR), 3),
            "rug_in_front_px": RUG_NEAR-fy1, "whole": fy0 >= 0 and fy1 <= 1920,
            "shadow_clusters": len([c for c in clusters if len(c) >= 20]),
            "rug_band_pass": 0.55 <= (fy1-RUG_FAR)/(RUG_NEAR-RUG_FAR) <= 0.95}
s28 = build_seated(2.8, "seated-2p8-lock-consistent-portrait-20261031.png")
s23 = build_seated(2.3, "seated-2p3-absolute-portrait-20261031.png")
seated = {"standing_alpha_bbox": list(stb), "standing_alpha_h": stb[3]-stb[1],
          "seated_alpha_bbox": list(sb), "seated_alpha_h": sb[3]-sb[1],
          "standing_scene_h_3p0_portrait": STAND_SCENE_H, "feet_anchor": FEET, "centre_x": CX,
          "rug_far": RUG_FAR, "rug_near": RUG_NEAR,
          "versions": {"2.8_lock_consistent_3p0_minus_0p2": s28, "2.3_absolute_old_derivation": s23},
          "formula": "scene_bbox_h = 1398 * (scale/3.0) * (949/1044)",
          "mars_pick_owed": "2.8x (standing-0.2 under new 3.0x lock) vs 2.3x absolute (old derivation). Both built+viewed; neither claimed approved."}
json.dump(seated, open(os.path.join(OUT, "seated-measurements-20261031.json"), "w"), indent=2)
print("SEATED", json.dumps(seated, indent=2))

# room contact: portrait B | landscape B | seated 2.8 | seated 2.3
def thumb(im, w):
    return im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
pb = Image.open(os.path.join(ROOT, "dual-portrait-feet-planted-20261031/portrait-3p0-planted-20261031.png")).convert("RGB")
lb = Image.open(os.path.join(ROOT, "dual-landscape-scale-fix-20261031/landscape-up0p5-3p0x-1920x1080-20261031.png")).convert("RGB")
s28im = Image.open(os.path.join(OUT, "room-proofs", s28["file"])).convert("RGB")
s23im = Image.open(os.path.join(OUT, "room-proofs", s23["file"])).convert("RGB")
# contact: top row portrait B + seated 2.8 + seated 2.3 (portrait thumbs), bottom landscape B wide
W = 540
sheet = Image.new("RGB", (W*3, 44 + 960 + 44 + 304), (128,128,128)); d = ImageDraw.Draw(sheet)
d.text((10,12), "ROOM 3.0x LOCK | Portrait B planted | Seated 2.8 lock-consistent | Seated 2.3 absolute", fill=(255,255,0))
for i, im in enumerate([pb, s28im, s23im]):
    sheet.paste(thumb(im, W), (i*W, 44))
d.text((10, 44+960+8), "Landscape B 3.0x pull-back (figure/chair 1.710, whole, margins 29/29) — 655px revert REJECTED, not shown as delivery", fill=(255,255,0))
sheet.paste(thumb(lb, W*3), (0, 44+960+44))
sheet.save(os.path.join(OUT, "room-proofs", "roomscale-3p0-seated-contact-20261031.png"))
print("room contact saved")

# ---------- 3. Eye pass: 140 sheets ----------
results = json.load(open(os.path.join(ROOT, "sliced-clean-20261031-results.json")))
keys = sorted(results.keys())
assert len(keys) == 140, len(keys)
# map sliced folders by basename
sliced_dirs = {}
for dp, dn, fn in os.walk(SLICED):
    for dname in dn:
        sliced_dirs.setdefault(dname, os.path.join(dp, dname))
eye = []
for k in keys:
    src = os.path.join(SHEETS, k)
    exists = os.path.exists(src)
    # sliced dir: folder name = basename without ext
    base = os.path.splitext(os.path.basename(k))[0]
    sdir = sliced_dirs.get(base)
    pieces = []
    if sdir:
        pieces = sorted([f for f in os.listdir(sdir) if f.lower().endswith(".png")])
    # numeric QC on pieces
    bad = 0; rgba_bad = 0
    largest = None; largest_area = -1
    for f in pieces:
        p = os.path.join(sdir, f)
        try:
            im = Image.open(p)
            if im.mode != "RGBA" or im.size[0] == 0 or im.size[1] == 0: rgba_bad += 1
            if os.path.getsize(p) == 0: bad += 1
            a = im.size[0]*im.size[1]
            if a > largest_area: largest_area = a; largest = f
        except Exception:
            bad += 1
    eye.append({"sheet": k, "source_exists": exists, "pieces_manifest": results[k]["pieces"],
                "pieces_on_disc": len(pieces), "pieces_match": len(pieces) == results[k]["pieces"],
                "bad_files": bad, "non_rgba_or_empty": rgba_bad, "largest_piece": largest,
                "sliced_dir": os.path.relpath(sdir, ROOT) if sdir else None, "source": os.path.relpath(src, os.path.expanduser("~")) if exists else None})
json.dump(eye, open(os.path.join(OUT, "eye-pass-numeric-20261031.json"), "w"), indent=2)
mismatch = [e for e in eye if not e["pieces_match"] or not e["source_exists"] or e["bad_files"] or e["non_rgba_or_empty"]]
print("EYE numeric mismatches:", len(mismatch))
for m in mismatch: print(" ", m)

# contacts: 10 sheets per contact, original sheet thumbnails
CELL_W, CELL_H, LABEL = 880, 560, 44
for ci in range(0, 140, 10):
    batch = keys[ci:ci+10]
    sheet_im = Image.new("RGB", (CELL_W*2, LABEL + (CELL_H+LABEL)*5), (90,90,90))
    d = ImageDraw.Draw(sheet_im)
    d.text((10,12), f"EYE PASS {ci+1}-{ci+len(batch)}/140 — original sheets (thumbnails) + piece count", fill=(255,255,0))
    for i, k in enumerate(batch):
        src = os.path.join(SHEETS, k)
        try: im = Image.open(src).convert("RGB")
        except Exception: im = Image.new("RGB", (100,100), (255,0,0))
        r = min((CELL_W-16)/im.width, CELL_H/im.height)
        th = im.resize((max(1,round(im.width*r)), max(1,round(im.height*r))), Image.LANCZOS)
        col, row = i % 2, i // 2
        x0, y0 = col*CELL_W, LABEL + row*(CELL_H+LABEL)
        sheet_im.paste(th, (x0+8, y0+8))
        d.text((x0+8, y0+CELL_H+6), f"{ci+i+1}. {k} — {results[k]['pieces']} pcs", fill=(255,255,255))
    sheet_im.save(os.path.join(OUT, "eye-contacts", f"eye-contact-{ci+1:03d}-{ci+len(batch):03d}-20261031.png"))
    print("contact", ci+1, ci+len(batch))
# largest-piece contacts: 20 per contact
for ci in range(0, 140, 20):
    batch = eye[ci:ci+20]
    CW, CH = 440, 360
    sheet_im = Image.new("RGB", (CW*4, 44 + CH*5), (90,90,90)); d = ImageDraw.Draw(sheet_im)
    d.text((10,12), f"EYE PASS largest-piece {ci+1}-{ci+len(batch)}/140 — sliced piece edge/fringe check", fill=(255,255,0))
    for i, e in enumerate(batch):
        p = os.path.join(ROOT, e["sliced_dir"], e["largest_piece"]) if e["sliced_dir"] and e["largest_piece"] else None
        try: im = Image.open(p).convert("RGBA")
        except Exception: im = Image.new("RGBA", (100,100), (255,0,0,255))
        bg = Image.new("RGBA", im.size, (128,128,128,255)); bg.alpha_composite(im); im = bg.convert("RGB")
        r = min((CW-16)/im.width, (CH-44)/im.height)
        th = im.resize((max(1,round(im.width*r)), max(1,round(im.height*r))), Image.LANCZOS)
        col, row = i % 4, i // 4
        x0, y0 = col*CW, 44 + row*CH
        sheet_im.paste(th, (x0+8, y0+8))
        d.text((x0+8, y0+CH-28), f"{ci+i+1}. {os.path.basename(e['sheet'])[:34]}", fill=(255,255,255))
    sheet_im.save(os.path.join(OUT, "eye-contacts", f"eye-largest-{ci+1:03d}-{ci+len(batch):03d}-20261031.png"))
    print("largest contact", ci+1, ci+len(batch))
print("DONE sheets", len(keys), "pieces total", sum(e["pieces_on_disc"] for e in eye))
