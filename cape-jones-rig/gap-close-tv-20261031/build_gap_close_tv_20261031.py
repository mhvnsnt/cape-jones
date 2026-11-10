#!/usr/bin/env python3
"""Gap Closure chunk B — TV Production Stack. Builds all deliverables in this folder.
Sources are READ ONLY; nothing outside this folder is written. No show art copied:
only original Cape Jones clean poses + method notes. Labels live on sheets only."""
import json, csv, os, re, textwrap, math, colorsys
from PIL import Image, ImageDraw, ImageFont
import numpy as np

RIG = os.path.expanduser("~/workspace/cape-jones-rig/")
OUT = os.path.join(RIG, "gap-close-tv-20261031")
os.makedirs(OUT, exist_ok=True)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(sz, bold=True): return ImageFont.truetype(FB if bold else FR, sz)
def rel(p): return os.path.join(RIG, p)

specs = json.load(open(rel("clean-100-20261031/shots/shot-specs-30-20261031.json")))["shots"]
by_id = {s["shot_id"]: s for s in specs}

# ---------------- thumbnail source map: real clean pose file, or None = POSE PENDING ----
THUMB = {
 "CJ-01": None, "CJ-02": None,
 "CJ-03": "clean-100-20261031/exposure-clips/clips/punch/punch-impact-locked-v7c-clean100-20261031.png",
 "CJ-04": None,
 "CJ-05": "clean-100-20261031/exposure-clips/clips/punch-arm2-variants/punch-impact-a2l-minus70-across-down-v7c-clean100-20261031.png",
 "CJ-06": "clips-v7c-clean-20261031/walk/walk-01-contact-v7c-clean.png",
 "CJ-07": "clips-v7c-clean-20261031/walk/walk-13-passing-v7c-clean.png",
 "CJ-08": "clips-v7c-clean-20261031/walk/walk-01-contact-v7c-clean.png",  # pose reused; alley bg owed
 "CJ-09": "clips-v7c-clean-20261031/dance/dance-01-a-v7c-clean.png",
 "CJ-10": "clips-v7c-clean-20261031/dance/dance-13-b-v7c-clean.png",
 "CJ-11": None,
 "CJ-12": "clips-v7c-clean-20261031/flying/flying-01-hover-v7c-clean.png",
 "CJ-13": "clips-v7c-clean-20261031/flying/flying-13-soar-v7c-clean.png",
 "CJ-14": "clips-v7c-clean-20261031/flying/flying-25-dive-v7c-clean.png",
 "CJ-15": None,
 "CJ-16": "reposes-v7c-clean/flex-anticipation-before-tighten-v7c-clean.png",
 "CJ-17": None, "CJ-18": None,  # CJ-18 failed file deliberately NOT used
 "CJ-19": "reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png",
 "CJ-20": None,
 "CJ-21": "clips-v7c-clean-20261031/jump/jump-01-crouch-v7c-clean.png",
 "CJ-22": "clips-v7c-clean-20261031/jump/jump-13-tuck-v7c-clean.png",
 "CJ-23": "reposes-v7c-clean/joint-seated-v7c-clean.png",
 "CJ-24": "reposes-v7c-clean/joint-seated-v7c-clean.png",  # pose; desk bg owed
 "CJ-25": "rig-apose-v7c-clean-transparent.png",          # standing pose; device prop is reference only
 "CJ-26": "DIALOGUE",  # built below, before the index is drawn
 "CJ-27": None,
 "CJ-28": "rig-apose-v7c-clean-transparent.png",          # pose; rooftop bg owed
 "CJ-29": "rig-apose-v7c-clean-transparent.png",
 "CJ-30": "rig-apose-v7c-clean-transparent.png",          # pose; alley bg owed
}
ONE_LINE = {
 "CJ-01":"Punch windup, held — anticipation before the snap.",
 "CJ-02":"Punch extends in a fast snap toward camera.",
 "CJ-03":"Punch impact, LOCKED frame — fist at upper chest.",
 "CJ-04":"Punch recover — tension/power beats close, base returns.",
 "CJ-05":"Arm2 across-down placement — NOT the impact frame.",
 "CJ-06":"Walk contact, street — first leg of the cycle.",
 "CJ-07":"Walk passing, town — second leg of the cycle.",
 "CJ-08":"Walk cycle on alley background (final alley owed).",
 "CJ-09":"Dance A — first dance phrase.",
 "CJ-10":"Dance B — second dance phrase.",
 "CJ-11":"Dance combined finale on twos (combined clip owed).",
 "CJ-12":"Flying hover, skyline.",
 "CJ-13":"Flying soar, arms out, sky.",
 "CJ-14":"Flying dive, arms up, sky.",
 "CJ-15":"Forward flight, fists to camera (foreshortened piece owed).",
 "CJ-16":"Flex anticipation — before the tighten.",
 "CJ-17":"Arms-up reference pose — NOT a flex.",
 "CJ-18":"True flex double-bicep (seam-fix rebuild owed; failed file unused).",
 "CJ-19":"Fighting pose, gauntlets OUT, dual-light.",
 "CJ-20":"Fighting stance, arms up really high.",
 "CJ-21":"Jump crouch + takeoff, rooftop.",
 "CJ-22":"Jump tuck + landing, cape wind.",
 "CJ-23":"Seated lounge pose in room, 2.3x seated scale.",
 "CJ-24":"Seated at desk (final desk background owed).",
 "CJ-25":"Standing in room with handheld device gag.",
 "CJ-26":"Dialogue, neutral / unsure beat — viseme mid-shape.",
 "CJ-27":"Dialogue, shout / angry beat (dialogue shot owed).",
 "CJ-28":"Rooftop at sunset (final rooftop background owed).",
 "CJ-29":"Rooftop at night city (final background owed).",
 "CJ-30":"Alley neon dual-light (final alley background owed).",
}
for sid, src in THUMB.items():
    if src and src != "DIALOGUE":
        assert os.path.exists(rel(src)), f"missing thumb source {sid} {src}"

# ---------------- helpers ----------------
def fit(img, w, h, bg=(232, 230, 225, 255)):
    """Fit img inside w x h on a flat bg, centred, aspect preserved."""
    im = img.convert("RGBA")
    im.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), bg)
    canvas.alpha_composite(im, ((w - im.width)//2, (h - im.height)//2))
    return canvas

def caption_block(d, x, y, w, lines, sizes=(26, 22, 20), colors=((20,20,20),(60,60,60),(150,30,30))):
    yy = y
    for i, ln in enumerate(lines):
        if not ln: continue
        d.text((x+10, yy), ln, font=font(sizes[min(i, len(sizes)-1)], bold=(i == 0)), fill=colors[min(i, len(colors)-1)])
        yy += sizes[min(i, len(sizes)-1)] + 4
    return yy

def strong_red_count(path):
    im = np.array(Image.open(path).convert("RGBA")).astype(int)
    if im.shape[2] < 4: return 0
    r, g, b, a = im[:,:,0], im[:,:,1], im[:,:,2], im[:,:,3]
    return int(((a > 10) & (r >= 200) & (g <= 80) & (b <= 80)).sum())

# ================= 7. DIALOGUE SHOT (built first, so CJ-26 thumbnail can use it) =========
# Room plate: on-background-room.jpg has a labelled character; device-in-final-shot-room
# has a clean centre. Splice the clean centre band from the device render over the old
# character band, then let the new 950px-tall body occlude the centre. Verified below
# by strong-red count + visual viewing; any remnant is patched, never labelled.
room_a = Image.open(rel("showcase/on-background-room.jpg")).convert("RGB")      # 1168x784, labelled char centre
room_b = Image.open(rel("mochiichao-combine-build-20261031/device-in-final-shot-room-20261031.png")).convert("RGB")
W, H = 1168, 1050
plate = Image.new("RGB", (W, H), (122, 74, 52))          # floor-brown extension below the room image
plate.paste(room_a, (0, 0))
# splice clean centre band from room_b (its centre is clean room; its char sits bottom-right)
band = room_b.crop((430, 150, 690, 784))
plate.paste(band, (430, 150))
# floor extension: flat floor colour only (the stretched-bottom-row version left vertical
# rug/floor stripes below the rug line — fixed after viewing). No detail invented.
# (plate base colour (122,74,52) already fills y784..H; nothing pasted here.)

body = Image.open(rel("rig-apose-v7c-clean-transparent.png")).convert("RGBA")   # 1100x1500, bbox y253-1294
SCALE = 950 / 1042.0   # locked room scale: rig 950px tall (2.5x), feet on floor
bw, bh = int(body.width * SCALE), int(body.height * SCALE)
body_s = body.resize((bw, bh), Image.LANCZOS)
# erase the body's own head (old mouth) so the viseme head is a clean swap, not a paste-over
bd = ImageDraw.Draw(body_s)
hc_x = int((82 + 0) )  # placeholder, recomputed after placement below
# place body: bbox bottom (1294*SCALE) lands at y=1000 (feet on floor, full body in taller frame)
bx = (W - bw)//2
by = 1000 - int(1294 * SCALE)
# head centre in scaled body coords: orig centre (549, ~324) -> scaled
head_cx = int(549 * SCALE); head_top = int(253 * SCALE); head_bot = int(395 * SCALE)
head_cy = (head_top + head_bot)//2
# erase old head with an ellipse slightly larger than the head box
bd.ellipse([head_cx - 62, head_top - 6, head_cx + 62, head_bot + 8], fill=(0, 0, 0, 0))
comp = plate.convert("RGBA")
comp.alpha_composite(body_s, (bx, by))
# viseme head: AH (04) = open mid-shape; crop to its alpha bbox, keep true aspect
vis = Image.open(rel("visemes-v2-20261031/head-v2-04-ah-20261031.png")).convert("RGBA")
va = np.array(vis)[:,:,3] > 10
ys, xs = np.where(va); vis_c = vis.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))
vh_h = int((head_bot - head_top + 14) * 1.0); vh_w = int(vh_h * vis_c.width / vis_c.height)
vis_s = vis_c.resize((vh_w, vh_h), Image.LANCZOS)
vx = bx + head_cx - vh_w//2; vy = by + head_top - 6
comp.alpha_composite(vis_s, (vx, vy))
# thin floor shadow ellipse under feet (plate element, not a label)
sd = ImageDraw.Draw(comp)
sd.ellipse([bx + int(360*SCALE), 1000 - 4, bx + int(740*SCALE), 1000 + 10], fill=(0, 0, 0, 40))
comp.convert("RGB").save(os.path.join(OUT, "dialogue-shot-cj26-neutral-ah-20261031.png"))
DIALOGUE = os.path.join(OUT, "dialogue-shot-cj26-neutral-ah-20261031.png")
print("dialogue composite:", comp.size, "body 950 tall, feet y=1000, viseme AH head at", vx, vy, vis_s.size)
print("dialogue strong-red:", strong_red_count(DIALOGUE))

# ================= 1a. 6-PANEL PUNCH STORYBOARD =================
APOSE = rel("rig-apose-v7c-clean-transparent.png")
IMPACT = rel("clips-v7c-clean-20261031/punch/punch-09-impact-hold-v7c-clean.png")
LOCKED = rel("clean-100-20261031/exposure-clips/clips/punch/punch-impact-locked-v7c-clean100-20261031.png")
panels = [
 ("TITLE", "CAPE JONES — punch sequence", "Title panel (not a shot). Original text only.", APOSE, False),
 ("1 · WINDUP — 6f", "CJ-01 · punch windup", "Anticipation. Arm draws back before the snap.", APOSE, True),
 ("2 · SNAP — 2f", "CJ-02 · punch extend-snap", "Fast extension. 2-frame snap — no in-between invented.", APOSE, True),
 ("3 · IMPACT", "CJ-03 · punch impact, LOCKED", "Locked impact frame. Arm2 diagonal UP, fist at upper chest.", LOCKED, False),
 ("4 · IMPACT HOLD — 12f", "CJ-03 (hold) · same locked frame, held", "Hold 12f on the locked frame. Energy + gauntlet glow are FX passes, not god rays.", LOCKED, False),
 ("5 · RECOVER — 6f", "CJ-04 · punch recover", "Recover 6f. Base golden-hour restored here.", APOSE, True),
]
PW, PH, CAP = 780, 500, 150
sheet = Image.new("RGB", (3*PW + 40, 130 + 2*(PH + CAP) + 20), (245, 243, 238))
d = ImageDraw.Draw(sheet)
d.text((20, 18), "STORYBOARD — CAPE JONES PUNCH SEQUENCE  ·  6 panels  ·  24 fps  ·  captions/timing on sheet only", font=font(30), fill=(20,20,20))
d.text((20, 60), "Panels marked POSE PENDING use the clean apose plate only — distinct windup / snap / recover clean frames are owed. No pose invented.", font=font(22, bold=False), fill=(150,30,30))
d.text((20, 92), "Timing: windup 6f · snap 2f · impact hold 12f · recover 6f  (= 26f per pass; animatic loops twice = 52f).", font=font(22, bold=False), fill=(60,60,60))
for i, (t, sub, note, src, pending) in enumerate(panels):
    cx, cy = 20 + (i % 3)*PW, 130 + (i//3)*(PH + CAP)
    sheet.paste(fit(Image.open(src), PW-20, PH-10), (cx+10, cy+5))
    d.rectangle([cx, cy+PH, cx+PW-10, cy+PH+CAP], outline=(180,180,180))
    lines = [t, sub, note] + (["POSE PENDING — apose plate only"] if pending else [])
    caption_block(d, cx, cy+PH+6, PW-20, lines, sizes=(24, 20, 18))
sheet.save(os.path.join(OUT, "storyboard-punch-6panel-20261031.png"))
print("storyboard 6-panel:", sheet.size)

# ================= 1b. 30-PANEL THUMBNAIL INDEX =================
# Caption lines are WRAPPED to the cell width (the first build let long slugs /
# one-liners run into the neighbouring cell — fixed after viewing).
def wrapped(text, width):
    return textwrap.wrap(text, width=width) or [""]
CW, CH, CCAP = 480, 280, 150
idx = Image.new("RGB", (5*CW + 60, 120 + 6*(CH + CCAP) + 20), (245, 243, 238))
d = ImageDraw.Draw(idx)
d.text((20, 18), "THUMBNAIL STORYBOARD INDEX — CJ-01 .. CJ-30  ·  one thumbnail per shot  ·  captions on sheet only", font=font(30), fill=(20,20,20))
d.text((20, 58), "POSE PENDING = no distinct clean pose exists for that shot; apose plate shown, pose NOT invented. Backgrounds are stand-ins per shot spec unless noted.", font=font(21, bold=False), fill=(150,30,30))
d.text((20, 88), "Clean pose thumbnails are unlabelled clean pieces. CJ-26 thumbnail is the new dialogue composite built in this folder.", font=font(21, bold=False), fill=(60,60,60))
for i, s in enumerate(specs):
    sid = s["shot_id"]; src = THUMB[sid]
    cx, cy = 20 + (i % 5)*CW, 120 + (i//5)*(CH + CCAP)
    if src is None:
        thumb = fit(Image.open(APOSE), CW-20, CH-10)
        status = "POSE PENDING"
    elif src == "DIALOGUE":
        thumb = fit(Image.open(DIALOGUE), CW-20, CH-10)
        status = "NEW DIALOGUE COMPOSITE"
    else:
        thumb = fit(Image.open(rel(src)), CW-20, CH-10)
        status = "CLEAN POSE"
    idx.paste(thumb, (cx+10, cy+5))
    d.rectangle([cx, cy+CH, cx+CW-10, cy+CH+CCAP], outline=(180,180,180))
    cap_lines = ([(ln, 21, (20,20,20)) for ln in wrapped(f"{sid} · {s['slug']}", 38)]
                 + [(ln, 18, (60,60,60)) for ln in wrapped(ONE_LINE[sid], 44)]
                 + [(status, 18, (150,30,30) if "PENDING" in status else (30,110,40))])
    yy = cy+CH+4
    for ln, sz, col in cap_lines:
        d.text((cx+10, yy), ln, font=font(sz, bold=(sz == 21)), fill=col); yy += sz + 3
idx.save(os.path.join(OUT, "storyboard-index-30panel-20261031.png"))
n_pending = sum(1 for v in THUMB.values() if v is None)
print("index 30-panel:", idx.size, "pending:", n_pending, "clean/new:", 30 - n_pending)

# ================= 2. ANIMATIC (windup 6 / snap 2 / impact hold 12 / recover 6, x2 loops) =====
import subprocess, shutil
frames_dir = os.path.join(OUT, "animatic-frames-20261031"); os.makedirs(frames_dir, exist_ok=True)
anim_panels = [
    ("WINDUP — 6f", "CJ-01 · punch windup", "POSE PENDING — apose plate only", APOSE, 6),
    ("SNAP — 2f", "CJ-02 · punch extend-snap", "POSE PENDING — apose plate only", APOSE, 2),
    ("IMPACT HOLD — 12f", "CJ-03 · punch impact, LOCKED", "Locked impact frame. Hold 12f.", LOCKED, 12),
    ("RECOVER — 6f", "CJ-04 · punch recover", "POSE PENDING — apose plate only", APOSE, 6),
]
AW, AH = 960, 720
fnum = 0; frame_files = []
for loop in range(2):
    for (t, sub, note, src, hold) in anim_panels:
        fr = Image.new("RGB", (AW, AH), (245, 243, 238))
        fr.paste(fit(Image.open(src), AW-40, AH-180), (20, 10))
        dd = ImageDraw.Draw(fr)
        dd.text((20, AH-150), t, font=font(36), fill=(20,20,20))
        dd.text((20, AH-100), sub, font=font(26, bold=False), fill=(60,60,60))
        dd.text((20, AH-60), f"{note}  ·  loop {loop+1}/2  ·  24 fps", font=font(22, bold=False), fill=(150,30,30) if "PENDING" in note else (60,60,60))
        for _ in range(hold):
            fnum += 1
            fp = os.path.join(frames_dir, f"anim-f{fnum:03d}.png"); fr.save(fp); frame_files.append(fp)
print("animatic frames:", fnum, "(expect 52 = 26 x 2 loops)")
mp4 = os.path.join(OUT, "animatic-punch-20261031.mp4")
subprocess.run(["ffmpeg","-y","-framerate","24","-i", os.path.join(frames_dir,"anim-f%03d.png"),
                "-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart", mp4],
               check=True, capture_output=True, text=True)
probe = json.loads(subprocess.run(["ffprobe","-v","quiet","-print_format","json","-show_format","-show_streams", mp4],
               check=True, capture_output=True, text=True).stdout)
st = probe["streams"][0]
print("ffprobe:", st["codec_name"], st["width"], "x", st["height"], st["avg_frame_rate"], "pix_fmt", st["pix_fmt"], "duration", probe["format"]["duration"])
# contact sheet of animatic frames: first frame of each panel per loop (8 frames)
contact = Image.new("RGB", (4*480 + 50, 2*360 + 60), (245, 243, 238))
d = ImageDraw.Draw(contact)
d.text((20, 14), "ANIMATIC CONTACT SHEET — punch sequence, 24 fps, looped twice (52 frames) · first frame of each hold, per loop", font=font(24), fill=(20,20,20))
picks = [1, 7, 9, 21, 27, 33, 35, 47]  # 1-based starts of each hold across 2 loops
for i, p in enumerate(picks):
    im = Image.open(frame_files[p-1]); im.thumbnail((470, 330), Image.LANCZOS)
    contact.paste(im, (20 + (i % 4)*480, 50 + (i//4)*360))
contact.save(os.path.join(OUT, "animatic-punch-contact-20261031.png"))
print("animatic contact:", contact.size)

# ================= 3. EDL =================
def holds(text):
    return [int(x) for x in re.findall(r"hold (\d+)f", text or "")]
edl = []; t = 0
for s in specs:
    hs = holds(s["pose_clip"])
    if hs:
        dur, basis = sum(hs), f"spec hold(s) {hs} summed"
    else:
        dur, basis = 12, "ASSUMED 12f loop — no hold stated in spec (flagged, not a spec claim)"
    edl.append({"shot": s["shot_id"], "slug": s["slug"], "source_pose_clip": s["pose_ref"],
                "source_spec_pose_clip": s["pose_clip"], "in_frame": t, "out_frame": t + dur - 1,
                "duration_frames": dur, "duration_basis": basis, "transition": "cut",
                "background": s["background"], "audio_cue_id": s["audio_cue_id"],
                "thumbnail_status": "POSE PENDING" if THUMB[s["shot_id"]] is None else ("NEW DIALOGUE COMPOSITE" if THUMB[s["shot_id"]] == "DIALOGUE" else "CLEAN POSE")})
    t += dur
edl_doc = {"version": "edl-cj01-cj30-20261031", "fps": 24, "total_frames": t,
           "total_seconds_at_24fps": round(t/24, 3),
           "transition_rule": "Cuts only — no dissolve/fade/wipe appears in shot-specs-30-20261031.json, and no shot spec states otherwise.",
           "note": "In/out frames are cumulative EDL frames at 24fps, not timecode from a picture lock. Assumed durations are flagged per shot.",
           "entries": edl}
json.dump(edl_doc, open(os.path.join(OUT, "edl-cj01-cj30-20261031.json"), "w"), indent=1)
with open(os.path.join(OUT, "edl-cj01-cj30-20261031.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(edl[0].keys())); w.writeheader(); w.writerows(edl)
print("EDL entries:", len(edl), "total frames:", t)
assert len(edl) == 30 and json.load(open(os.path.join(OUT, "edl-cj01-cj30-20261031.json")))["entries"][29]["shot"] == "CJ-30"

# ================= 4. QC =================
def hue(rgb):
    if rgb is None: return None
    r, g, b = [c/255 for c in rgb]
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)
    return round(h*360)
def angdiff(a, b):
    d = abs(a - b) % 360; return min(d, 360 - d)
approved = set()
for f, key in [("showcase/lut-approval-checklist.json", "tint_key"), ("showcase/lut-spectrum-checklist.json", "name"), ("showcase/lut-spectrum-v2-checklist.json", "name")]:
    d = json.load(open(rel(f))); items = d.values() if isinstance(d, dict) else d
    for v in items: approved.add(str(v.get(key, "")).lower())
import glob as _g
for pat in ["showcase/luts-33-upgraded/*.cube", "showcase/luts-spectrum-v2/*.cube"]:
    for p in _g.glob(rel(pat)):
        n = os.path.basename(p).replace("lut-33-", "").replace(".cube", "").lower(); approved.add(n)
approved.discard("")
REQUIRED = ["shot_id","slug","pose_clip","pose_ref","background","scale","lighting_level","lut","lut_file","key_color","rim_color","god_ray_decision","audio_cue_id","audio_note","gate_checklist"]
qc_rows = []
for s in specs:
    sid = s["shot_id"]; checks = {}
    miss = [k for k in REQUIRED if s.get(k) in (None, "")]
    checks["fields_present"] = {"pass": not miss, "detail": "all 15 required fields present" if not miss else f"missing: {miss}"}
    lutn = str(s.get("lut", "")).lower()
    checks["lut_in_approved_70_set"] = {"pass": lutn in approved, "detail": f"lut '{s.get('lut')}' in approved set ({len(approved)} names incl. cube files)" if lutn in approved else f"lut '{s.get('lut')}' NOT in approved set"}
    if s.get("dual_light"):
        dl = s["dual_light"]
        ok = bool(dl.get("front_key") and dl.get("back_source") and dl.get("rim_front") and dl.get("rim_back"))
        fr_h, bk_h = hue(dl["rim_front"]), hue(dl["back_source"]["color"]) if isinstance(dl.get("back_source"), dict) else None
        checks["rim_within_20_of_shifted_key"] = {"pass": ok, "detail": f"DUAL-LIGHT EXCEPTION (allowed: Level 3 dual-light, both sources named + rim ownership stated). Front rim hue {hue(dl['rim_front'])} vs front key hue {hue(dl['front_key']['color'])}; back rim hue {hue(dl['rim_back'])} vs back source hue {bk_h}."}
        checks["dual_light_exception_only_where_allowed"] = {"pass": ok and "dual" in str(s.get("lighting_level", "")).lower(), "detail": "dual_light present and lighting_level is dual-light; both sources named."}
    else:
        checks["dual_light_exception_only_where_allowed"] = {"pass": True, "detail": "no dual_light claimed."}
        base = s.get("shifted_key_hue_deg") if s.get("shifted_key_hue_deg") is not None else s.get("key_hue_deg")
        rim = s.get("rim_hue_deg")
        if base is None or rim is None:
            checks["rim_within_20_of_shifted_key"] = {"pass": False, "detail": f"UNVERIFIABLE — key hue {base}, rim hue {rim}; cannot confirm within +/-20 deg. Spec records: '{s.get('rim_rule_basis')}'. This is NOT the dual-light exception and needs a ruling; counted as FAIL here."}
        else:
            df = angdiff(base, rim)
            checks["rim_within_20_of_shifted_key"] = {"pass": df <= 20, "detail": f"{'shifted' if s.get('shifted_key_hue_deg') is not None else 'base'} key {base} deg vs rim {rim} deg = diff {df} deg (<=20)."}
    god = str(s.get("god_ray_decision", ""))
    lvl = str(s.get("lighting_level", ""))
    god_ok = bool(god) and (("none" in god.lower()) if lvl.startswith("Level 2") else ("god ray" in god.lower()))
    checks["god_ray_decision_present"] = {"pass": god_ok, "detail": f"decision present: '{god}' (level: {lvl})."}
    checks["audio_cue_present"] = {"pass": bool(s.get("audio_cue_id")) and bool(s.get("audio_note")), "detail": f"{s.get('audio_cue_id')} — {s.get('audio_note')}"}
    src = THUMB[sid]
    if src is None:
        checks["label_gate_0_red_pixels"] = {"pass": True, "detail": "n/a — no clean pose referenced (POSE PENDING); no piece to gate. Not counted as a label pass on a piece."}
    else:
        pth = DIALOGUE if src == "DIALOGUE" else rel(src)
        rc = strong_red_count(pth)
        checks["label_gate_0_red_pixels"] = {"pass": rc == 0, "detail": f"strong-red pixels (R>=200,G<=80,B<=80) = {rc} on {os.path.basename(pth)}."}
    overall = all(c["pass"] for c in checks.values())
    qc_rows.append({"shot_id": sid, "slug": s["slug"], "overall": "PASS" if overall else "FAIL", "checks": checks})
npass = sum(1 for r in qc_rows if r["overall"] == "PASS")
qc_doc = {"version": "qc-cj01-cj30-20261031", "source_specs": "clean-100-20261031/shots/shot-specs-30-20261031.json",
          "checks_applied": ["fields_present (15 fields)", "lut_in_approved_70_set", "rim_within_20_of_shifted_key", "dual_light_exception_only_where_allowed", "god_ray_decision_present (+ Level 2 none / Level 3 god-rays cross-check)", "audio_cue_present", "label_gate_0_red_pixels (strong-red proxy on referenced clean poses)"],
          "counts": {"pass": npass, "fail": 30 - npass, "total": 30},
          "failures_plain": [{"shot_id": r["shot_id"], "failed_checks": [k for k, v in r["checks"].items() if not v["pass"]], "detail": [v["detail"] for v in r["checks"].values() if not v["pass"]]} for r in qc_rows if r["overall"] == "FAIL"],
          "notes": ["CJ-09/CJ-10/CJ-16/CJ-17/CJ-21 lut_file is a directory path ('showcase/lut-spectrum/ ...') not a specific .cube file — LUT NAME still in the approved set, so not failed here, but the file path should be made specific before final delivery.",
                    "POSE PENDING shots (9) are not QC-failed for having no pose; their missing poses are tracked in the storyboard index and EDL thumbnail_status.",
                    "Label gate uses a strong-red pixel proxy (R>=200,G<=80,B<=80). It is a label-remnant screen, not a full label audit; all checked clean pieces returned 0."],
          "results": qc_rows}
json.dump(qc_doc, open(os.path.join(OUT, "qc-cj01-cj30-20261031.json"), "w"), indent=1)
lines = ["# QC Report — CJ-01..CJ-30 (gap-close-tv-20261031)", "",
         f"**Result: {npass}/30 PASS, {30-npass}/30 FAIL — NOT 30/30.** Failures are listed plainly below; nothing is rounded up.",
         "", "Source: `clean-100-20261031/shots/shot-specs-30-20261031.json`. Checks: 15 required fields; LUT in the approved 70/70 set (base 30 + spectrum 24 + spectrum-v2 16, incl. .cube filenames); rim within ±20° of the (shifted) key; dual-light exception only where allowed; god-ray decision present (Level 2 = none, Level 3 = god rays); audio cue present; label gate = 0 strong-red pixels on each referenced clean pose.",
         "", "## Failures"]
for f in qc_doc["failures_plain"]:
    lines.append(f"- **{f['shot_id']}** — failed: {', '.join(f['failed_checks'])}. " + " ".join(f["detail"]))
lines += ["", "## Per-shot results"]
for r in qc_rows:
    bad = [k for k, v in r["checks"].items() if not v["pass"]]
    lines.append(f"- {r['shot_id']} ({r['slug']}): **{r['overall']}**" + (f" — failed: {', '.join(bad)}" if bad else ""))
lines += ["", "## Notes"] + [f"- {n}" for n in qc_doc["notes"]]
open(os.path.join(OUT, "qc-cj01-cj30-20261031.md"), "w").write("\n".join(lines) + "\n")
print("QC:", npass, "pass /", 30 - npass, "fail")

# ================= 5. 12-PRINCIPLES MATRIX =================
PRIN = {
 "CJ-01": (["Anticipation","Timing","Staging"], "Silhouette readability (gap-audit sheet, reused)"),
 "CJ-02": (["Timing","Exaggeration","Arcs"], "Punch exposure / smear frame (gap-audit sheet, reused)"),
 "CJ-03": (["Exaggeration","Staging","Timing"], "Impact lock: Arm2 diagonal UP, fist at upper chest"),
 "CJ-04": (["Follow Through and Overlapping Action","Slow In and Slow Out","Timing"], "Cape follow-through (gap-audit sheet, reused)"),
 "CJ-05": (["Staging","Solid Drawing","Appeal"], "Arm2 across-DOWN placement — must not be mistaken for impact"),
 "CJ-06": (["Arcs","Timing","Pose to Pose"], "Knee-feet rule: knee direction = foot direction"),
 "CJ-07": (["Arcs","Timing","Follow Through and Overlapping Action"], "Knee-feet rule"),
 "CJ-08": (["Staging","Timing","Secondary Action"], "Knee-feet rule"),
 "CJ-09": (["Timing","Exaggeration","Appeal"], "Knee-feet rule (dance fix)"),
 "CJ-10": (["Timing","Secondary Action","Appeal"], "Knee-feet rule"),
 "CJ-11": (["Timing","Secondary Action","Exaggeration"], "Beat grid on twos"),
 "CJ-12": (["Slow In and Slow Out","Staging","Appeal"], "Silhouette readability"),
 "CJ-13": (["Arcs","Exaggeration","Staging"], "Silhouette readability"),
 "CJ-14": (["Arcs","Timing","Exaggeration"], "Cape follow-through"),
 "CJ-15": (["Solid Drawing","Staging","Exaggeration"], "BLOCKED: foreshortened forearm piece owed — gate cannot pass yet"),
 "CJ-16": (["Anticipation","Slow In and Slow Out","Squash and Stretch"], "Flex anticipation frame"),
 "CJ-17": (["Staging","Solid Drawing","Appeal"], "Arms-up pose is NOT a flex — do not label it one"),
 "CJ-18": (["Squash and Stretch","Exaggeration","Appeal"], "BLOCKED: seam-fix rebuild owed; failed file must not be used"),
 "CJ-19": (["Staging","Exaggeration","Solid Drawing"], "Gauntlet-out-fixed + dual-light rim ownership"),
 "CJ-20": (["Staging","Exaggeration","Appeal"], "Arms-up reference pose family"),
 "CJ-21": (["Anticipation","Squash and Stretch","Timing"], "Squash-and-stretch jump (wired sheet, reused)"),
 "CJ-22": (["Follow Through and Overlapping Action","Timing","Arcs"], "Cape wind + landing"),
 "CJ-23": (["Staging","Secondary Action","Appeal"], "Room scale 2.3x seated, room-only"),
 "CJ-24": (["Staging","Secondary Action","Appeal"], "Room scale 2.3x seated; desk background owed"),
 "CJ-25": (["Secondary Action","Staging","Appeal"], "Room scale 2.5x standing + prop scale"),
 "CJ-26": (["Timing","Staging","Appeal"], "Lipsync strip: viseme mid-shape (visual only — no recorded audio)"),
 "CJ-27": (["Exaggeration","Timing","Staging"], "Expression swap / lipsync — dialogue shot owed"),
 "CJ-28": (["Staging","Slow In and Slow Out","Appeal"], "God-ray placement (Level 3)"),
 "CJ-29": (["Staging","Secondary Action","Appeal"], "God-ray placement (Level 3)"),
 "CJ-30": (["Staging","Exaggeration","Appeal"], "Dual-light rim ownership (pink front / cyan back)"),
}
mat = {"version": "principles-matrix-cj01-cj30-20261031",
       "statement": "Per-shot principles checks move from 0/30 to 30/30 AS A MATRIX. Visual proof exists for CJ-01 only (its exposure sheet in gap-audit-critique-log-20261031, reused here, not rebuilt). For CJ-02..CJ-30 this file is a matrix assignment + gate, not visual proof — say so plainly. CJ-01 itself is not rebuilt.",
       "cj01_visual_proof_reused": "gap-audit-critique-log-20261031/punch-cj01-exposure-smear-20261031.png + silhouette-readability-20261031.png",
       "entries": [{"shot_id": sid, "slug": by_id[sid]["slug"], "primary_principles": p, "gate": g, "evidence": "visual proof (reused)" if sid == "CJ-01" else "matrix assignment only — visual proof owed"} for sid, (p, g) in PRIN.items()]}
json.dump(mat, open(os.path.join(OUT, "principles-matrix-cj01-cj30-20261031.json"), "w"), indent=1)
# sheet image for the matrix
MS = Image.new("RGB", (1800, 60 + 31*52), (245, 243, 238)); d = ImageDraw.Draw(MS)
d.text((20, 14), "12-PRINCIPLES MATRIX — CJ-01 .. CJ-30  ·  2–3 primary principles + gate per shot  ·  CJ-01 visual proof only; rest = matrix", font=font(26), fill=(20,20,20))
for i, sid in enumerate([f"CJ-{n:02d}" for n in range(1, 31)]):
    y = 60 + i*52
    p, g = PRIN[sid]
    d.text((20, y), sid, font=font(22), fill=(20,20,20))
    d.text((130, y), ", ".join(p), font=font(22, bold=False), fill=(40,40,40))
    d.text((950, y), "GATE: " + g, font=font(20, bold=False), fill=(120,30,30) if "BLOCKED" in g else (60,60,60))
MS.save(os.path.join(OUT, "principles-matrix-cj01-cj30-20261031.png"))
print("principles matrix: 30/30 entries")

# ================= 6. TITLE CARD + CREDITS =================
TW, TH = 1600, 900
grad = Image.new("RGB", (TW, TH))
for y in range(TH):
    t = y / TH; c = (int(30 + 40*t), int(20 + 30*t), int(60 + 40*t))
    ImageDraw.Draw(grad).line([(0, y), (TW, y)], fill=c)
title = grad.convert("RGBA")
# silhouette from apose alpha, in near-black purple, centred, ~640 tall
sil = Image.open(APOSE).convert("RGBA")
sa = np.array(sil); mask = sa[:,:,3] > 10
sil_img = Image.new("RGBA", sil.size, (0, 0, 0, 0)); sarr = np.array(sil_img)
sarr[mask] = (12, 8, 28, 255)
sil_img = Image.fromarray(sarr); sil_img.thumbnail((520, 700), Image.LANCZOS)
title.alpha_composite(sil_img, ((TW - sil_img.width)//2, 90))
d = ImageDraw.Draw(title)
def centre(y, txt, fnt, fill):
    bb = d.textbbox((0, 0), txt, font=fnt); d.text(((TW - (bb[2]-bb[0]))//2, y), txt, font=fnt, fill=fill)
centre(20, "CAPE JONES", font(110), (255, 235, 170))
d.line([(300, 790), (1300, 790)], fill=(255, 235, 170), width=4)
centre(810, "ORIGINAL TITLE CARD", font(28, bold=False), (220, 220, 220))
title.convert("RGB").save(os.path.join(OUT, "title-card-cape-jones-20261031.png"))
print("title card:", title.size)
ROLES = ["Creator","Director","Animation","Character Design","Background Painting","Compositing & Lighting","Sound Design","Music","Editing","Production Management"]
CR = Image.new("RGB", (1400, 1100), (245, 243, 238)); d = ImageDraw.Draw(CR)
d.text((60, 40), "CAPE JONES — CREDITS TEMPLATE", font=font(44), fill=(20,20,20))
d.text((60, 110), "No names are filled in. Every credit below is TBD until a real person is assigned — no names invented.", font=font(24, bold=False), fill=(150,30,30))
y = 190
for r in ROLES:
    d.text((60, y), r, font=font(32), fill=(20,20,20)); d.text((700, y), "TBD", font=font(32, bold=False), fill=(60,60,60)); y += 72
d.text((60, y+20), "Template only — not a finished credit roll. Episode / date / delivery details TBD.", font=font(22, bold=False), fill=(60,60,60))
CR.save(os.path.join(OUT, "credits-template-20261031.png"))
open(os.path.join(OUT, "credits-template-20261031.md"), "w").write(
 "# CAPE JONES — Credits Template\n\nNo names are filled in. Every role is TBD until a real person is assigned — no names invented.\n\n" + "".join(f"- **{r}:** TBD\n" for r in ROLES) + "\nTemplate only — not a finished credit roll.\n")
print("credits: roles", len(ROLES), "all TBD")
print("DONE-BUILD (manifest next, after viewing)")
