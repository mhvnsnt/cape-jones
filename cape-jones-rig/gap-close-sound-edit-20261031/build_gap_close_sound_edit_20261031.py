#!/usr/bin/env python3
"""Gap closure chunk D — SOUND / CAMERA / EDITING / BACKGROUNDS / EFFECTS WIRING.
Original Cape Jones only. Labels on sheets only, never baked into clean pieces.
New dated files only, in gap-close-sound-edit-20261031/."""
import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont

R = "/home/hatch/workspace/cape-jones-rig"
O = os.path.join(R, "gap-close-sound-edit-20261031")
os.makedirs(O, exist_ok=True)
os.makedirs(os.path.join(O, "_frames_punch"), exist_ok=True)
os.makedirs(os.path.join(O, "_frames_dance"), exist_ok=True)

def font(sz, bold=True):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def wrap(d, txt, xy, fnt, fill=(0,0,0), w=88):
    x, y = xy
    for ln in textwrap.wrap(txt, width=w):
        d.text((x, y), ln, fill=fill, font=fnt); y += 26
    return y

def silhouette(path, size=(300, 410)):
    """Clean apose silhouette/plate for diagrams only — no character art copied into sheets as art."""
    import numpy as np
    im = Image.open(path).convert("RGBA")
    if im.mode == "RGBA" and "transparent" in path:
        mask = im.split()[3]
    else:
        a = np.array(im.convert("RGB")).astype(int)
        diff = np.abs(a - np.array([128, 128, 128])).sum(axis=2)
        mask = Image.fromarray((diff > 60).astype("uint8") * 255)
    bbox = mask.getbbox()
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    if bbox:
        crop, mk = im.crop(bbox), mask.crop(bbox)
        crop.thumbnail(size, Image.LANCZOS)
        mk2 = mk.resize(crop.size, Image.LANCZOS)
        out.paste(Image.new("RGBA", crop.size, (22, 22, 34, 255)), (0, 0), mk2)
    return out

def sheet_base(title, subtitle, W=1500, H=1100):
    img = Image.new("RGB", (W, H), (240, 240, 235))
    d = ImageDraw.Draw(img)
    d.text((30, 18), title, fill=(0, 0, 0), font=font(32))
    y = 60
    for ln in textwrap.wrap(subtitle, width=100):
        d.text((30, y), ln, fill=(60, 60, 60), font=font(19, False)); y += 25
    return img, d, y + 10

APOSE = os.path.join(R, "rig-apose-v7c-clean-transparent.png")
FIGHT = os.path.join(R, "reposes-v7c-clean/fighting-pose-forward-bicep-curl-v7c-clean.png")
JOINT_PUNCH = os.path.join(R, "reposes-v7c-clean/joint-punch-v7c-clean.png")
IMPACT = os.path.join(R, "clips-v7c-clean-20261031/punch/punch-09-impact-hold-v7c-clean.png")

# ---------- 1. SOUND DESIGN LAYER STACK ----------
layers = [
    ("1  DIALOGUE", "Spoken lines (CJ-26, CJ-27 dialogue shots). No recorded dialogue exists yet — this layer is EMPTY in the demo mix by design.", "CJ-A26, CJ-A27 (owed)", "Lead, -14 LUFS mix target", (200, 60, 60)),
    ("2  SFX", "Punch impact, snap, whoosh, walk steps, jump rise — the 5 demo cues below, synthesized tones/noise only.", "CJ-A01..CJ-A05 demo cues", "Effects, -14 LUFS mix target", (30, 110, 180)),
    ("3  MUSIC", "Dance beat bed under CJ-09..CJ-11. Demo uses low thump tones on the beat, not a composed track.", "CJ-A09..CJ-A11 (demo thumps)", "Bed, -14 LUFS mix target", (120, 60, 160)),
    ("4  AMBIENCE", "Room tone / street bed under everything, low and continuous. Demo uses a low brown-noise bed.", "All shots (bed)", "Bed, -14 LUFS mix target", (40, 130, 90)),
    ("5  DEVICE BEEP METRONOME", "The device beep from the dance beat sheet, used as the metronome: short 880 Hz ticks on beat starts.", "CJ-09..CJ-11 dance beats", "Ticks, -14 LUFS mix target", (200, 130, 0)),
]
cues = [
    ("Punch impact", "0.00-0.60s", "120 Hz thump + noise burst", "-6 dB peak"),
    ("Fighting stance whoosh", "1.08-1.58s", "Filtered noise swell", "-12 dB peak"),
    ("Walk steps x2", "2.08-2.75s", "2 short noise taps", "-18 dB peak"),
    ("Jump rise", "3.29-3.88s", "Stepped 300/600 Hz rise", "-12 dB peak"),
    ("Dance beat x4", "4.38-5.98s", "110 Hz thumps + 880 Hz beep ticks", "-10 dB peak"),
]
img, d, y0 = sheet_base("SOUND DESIGN LAYER STACK — CAPE JONES (SYNTHESIZED DEMO)",
    "5 layers mapped to the 5 demo cues from showcase/audio/audio-cue-sheet-v2. MIX integrated target -14 LUFS for every layer stem (measured on the mix, not per-layer loudness stacked). "
    "RECORDED FINAL AUDIO IS 0% — this demo + layer stack is the working replacement, NOT recorded audio. Labels on this sheet only.", H=1180)
y = y0
for name, desc, mapping, lvl, col in layers:
    d.rectangle([30, y, 1470, y + 118], fill=(255, 255, 255), outline=col, width=4)
    d.rectangle([30, y, 46, y + 118], fill=col)
    d.text((60, y + 8), name, fill=(0, 0, 0), font=font(22))
    d.text((60, y + 38), desc, fill=(40, 40, 40), font=font(17, False))
    d.text((60, y + 66), f"Maps to: {mapping}", fill=(40, 40, 40), font=font(17, False))
    d.text((60, y + 92), lvl, fill=col, font=font(17))
    y += 130
d.text((30, y + 4), "DEMO CUES (cue sheet v2 timings, tones only — SYNTHESIZED DEMO, NOT recorded audio):", fill=(0, 0, 0), font=font(20))
y += 34
for c, t, how, pk in cues:
    d.text((60, y), f"• {c}  |  {t}  |  {how}  |  {pk}", fill=(0, 0, 0), font=font(18, False)); y += 28
img.save(os.path.join(O, "sound-layer-stack-20261031.png")); print("sound sheet", img.size)

sound_json = {
    "version": "sound-layer-stack-20261031", "date": "2026-10-31",
    "recorded_final_audio_pct": 0,
    "disclaimer": "SYNTHESIZED DEMO ONLY — tones/noise built with ffmpeg. Not recorded audio. The demo + this layer stack is the working replacement, not a claim of recorded audio.",
    "mix_integrated_target_lufs": -14, "mix_true_peak_ceiling_db": -1.5,
    "method_note": "Each layer stem is authored against the same -14 LUFS mix target; the MIX (not the arithmetic sum of stems) is measured with ffmpeg loudnorm, following the wired-100-20261031 loudnorm method.",
    "layers": [
        {"layer": "dialogue", "role": "Spoken lines", "demo_cues": ["CJ-A26", "CJ-A27"], "demo_content": "EMPTY in demo mix — no recorded dialogue exists yet", "lufs_target": -14},
        {"layer": "sfx", "role": "Impact, snap, whoosh, steps, jump", "demo_cues": ["CJ-A01", "CJ-A02", "CJ-A03", "CJ-A04", "CJ-A05"], "demo_content": "synthesized tones/noise per cue sheet v2", "lufs_target": -14},
        {"layer": "music", "role": "Dance beat bed", "demo_cues": ["CJ-A09", "CJ-A10", "CJ-A11"], "demo_content": "110 Hz thump tones on beat starts (not a composed track)", "lufs_target": -14},
        {"layer": "ambience", "role": "Room/street bed", "demo_cues": ["all shots (bed)"], "demo_content": "low brown-noise bed, whole mix", "lufs_target": -14},
        {"layer": "device_beep_metronome", "role": "Device beep as metronome (dance beat sheet)", "demo_cues": ["CJ-09", "CJ-10", "CJ-11 dance beats"], "demo_content": "880 Hz ticks on beat starts in dance section", "lufs_target": -14},
    ],
    "demo_cues_v2": [{"cue": c, "time": t, "method": h, "peak_db": p} for c, t, h, p in cues],
    "demo_audio_file": "sound-demo-mix-minus14lufs-20261031.wav",
    "source_cue_sheet": "showcase/audio/audio-cue-sheet-v2.csv (5 demo cues)",
    "mars_approval": 0, "still_owed": ["recorded dialogue", "recorded SFX", "composed music track", "dialogue shot audio sync to a real recording"],
}
json.dump(sound_json, open(os.path.join(O, "sound-layer-stack-20261031.json"), "w"), indent=1)

# ---------- 2. LIP-SYNC AUDIO TIMELINE ----------
phrase = [
    # (frame_start, frame_end, phoneme, viseme_id, viseme_key, viseme_label)
    (1, 2, "— (silence)", "01", "rest", "rest / Neutral"),
    (3, 5, "P", "07", "mbp", "M/B/P"),
    (6, 11, "AH", "04", "ah", "AH"),
    (12, 13, "— (gap)", "01", "rest", "rest / Neutral"),
    (14, 16, "G", "14", "gk", "G/K"),
    (17, 22, "OH", "05", "oh", "OH"),
    (23, 24, "— (rest)", "01", "rest", "rest / Neutral"),
]
vis_heads = {"01": "head-v2-01-rest-20261031.png", "04": "head-v2-04-ah-20261031.png",
             "05": "head-v2-05-oh-20261031.png", "07": "head-v2-07-mbp-20261031.png", "14": "head-v2-14-gk-20261031.png"}
frames = []
for s, e, ph, vid, key, lab in phrase:
    for f in range(s, e + 1):
        frames.append({"frame": f, "time_sec": round((f - 1) / 24, 4), "phoneme": ph, "viseme_id": vid, "viseme_key": key, "viseme_label": lab})
lipsync = {"version": "lipsync-timeline-20261031", "date": "2026-10-31", "fps": 24,
    "test_phrase": "PAH GO (test phrase only — not show dialogue)",
    "viseme_source": "visemes-v2-20261031 (14 shapes, mask-first swap library)",
    "note": "Frame-by-frame at 24 fps. Real dialogue timing comes from recorded audio when it exists; this strip is a timing test, not a dialogue performance.",
    "segments": [{"frames": f"{s}-{e}", "phoneme": ph, "viseme_id": vid, "viseme_key": key} for s, e, ph, vid, key, lab in phrase],
    "frames": frames, "mars_approval": 0}
json.dump(lipsync, open(os.path.join(O, "lipsync-timeline-20261031.json"), "w"), indent=1)
# strip image: fresh build, gap-audit strip method (head panels in order), not a copy of its file
img, d, y0 = sheet_base("LIP-SYNC AUDIO TIMELINE — TEST PHRASE 'PAH GO' @24fps",
    "Visemes v2 (14 shapes). One head panel per segment, frame ranges on the sheet only. Real dialogue timing comes from recorded audio when it exists.", H=760)
x = 30
for s, e, ph, vid, key, lab in phrase:
    p = os.path.join(R, "visemes-v2-20261031", vis_heads[vid])
    h = Image.open(p).convert("RGBA"); h.thumbnail((210, 300), Image.LANCZOS)
    canvas = Image.new("RGBA", (230, 420), (255, 255, 255, 255)); canvas.paste(h, (10, 10), h)
    img.paste(canvas, (x, y0), canvas)
    d.text((x, y0 + 320), f"F{s}-{e}  {ph}", fill=(0, 0, 0), font=font(19))
    d.text((x, y0 + 348), f"viseme {vid} {key}", fill=(0, 0, 0), font=font(17, False))
    d.text((x, y0 + 372), lab, fill=(60, 60, 60), font=font(16, False))
    x += 240
    if x > 1300: break
# timeline bar
by = y0 + 430
d.rectangle([30, by, 1470, by + 40], outline=(0, 0, 0), width=2)
cx = 30
for s, e, ph, vid, key, lab in phrase:
    w = (e - s + 1) / 24 * 1440
    d.rectangle([cx, by, cx + w, by + 40], fill=(30, 110, 180), outline=(255, 255, 255), width=2)
    d.text((cx + 6, by + 8), ph, fill=(255, 255, 255), font=font(16)); cx += w
d.text((30, by + 52), "24 frames = 1.00 s.  •  P = lips closed (mbp)  •  AH = open (ah)  •  G = back (gk)  •  OH = rounded (oh).", fill=(0, 0, 0), font=font(18, False))
img.save(os.path.join(O, "lipsync-strip-20261031.png")); print("lipsync strip", img.size)

# ---------- 3. CAMERA-MOVE SHEET ----------
sil = silhouette(APOSE)
img, d, y0 = sheet_base("CAMERA-MOVE SHEET — CAPE JONES PUNCH / WALK SHOT",
    "Clean apose silhouettes/plates only — no character art copied. Diagrams + one-line when-to-use notes on the sheet only. 180-degree rule sheet already exists (gap-audit camera-180-rule-20261031.png) and is NOT rebuilt here.", H=1500)
panels = [
    ("PAN — camera turns left/right, stays put", "When to use: follow the punch/walk across the frame without moving the camera.", "pan"),
    ("TILT — camera turns up/down, stays put", "When to use: reveal height — low crouch up to the raised fist, or drop to the feet.", "tilt"),
    ("DOLLY — camera moves IN/OUT on the action", "When to use: push in on the impact hold; pull back on the recover.", "dolly"),
    ("TRUCK — camera moves sideways with the action", "When to use: track the walk/punch travel so the figure stays framed.", "truck"),
    ("WIDE — whole figure + ground + room", "When to use: establish the punch/walk geography and the ground plane.", "wide"),
    ("MEDIUM — waist-up, action reads", "When to use: the punch itself — arm, torso and fist all in frame.", "medium"),
    ("CLOSE-UP — head/shoulders or fist", "When to use: the impact beat only — 2-3 frames, then cut back out.", "closeup"),
]
cw, ch = 490, 430
for i, (title, note, kind) in enumerate(panels):
    x = 20 + (i % 3) * cw; y = y0 + (i // 3) * ch
    d.rectangle([x, y, x + cw - 20, y + ch - 20], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    d.text((x + 14, y + 10), title, fill=(0, 0, 0), font=font(18))
    ny = wrap(d, note, (x + 14, y + ch - 96), font(16, False), w=42)
    # diagram area
    if kind == "pan":
        for px, a in [(x + 40, 255), (x + 190, 200), (x + 340, 255)]:
            s = sil.copy(); s.thumbnail((110, 150), Image.LANCZOS); img.paste(s, (px, y + 120), s)
        d.line([(x + 60, y + 300), (x + 410, y + 300)], fill=(200, 0, 0), width=4)
        d.polygon([(x + 410, y + 288), (x + 410, y + 312), (x + 440, y + 300)], fill=(200, 0, 0))
        d.text((x + 150, y + 310), "PAN →", fill=(200, 0, 0), font=font(18))
    elif kind == "tilt":
        s = sil.copy(); s.thumbnail((110, 150), Image.LANCZOS); img.paste(s, (x + 180, y + 120), s)
        d.line([(x + 400, y + 110), (x + 400, y + 300)], fill=(200, 0, 0), width=4)
        d.polygon([(x + 388, y + 110), (x + 412, y + 110), (x + 400, y + 80)], fill=(200, 0, 0))
        d.polygon([(x + 388, y + 300), (x + 412, y + 300), (x + 400, y + 330)], fill=(200, 0, 0))
        d.text((x + 330, y + 200), "TILT ↕", fill=(200, 0, 0), font=font(18))
    elif kind == "dolly":
        for px, sz in [(x + 50, 90), (x + 170, 140), (x + 300, 190)]:
            s = sil.copy(); s.thumbnail((sz, int(sz * 1.37)), Image.LANCZOS); img.paste(s, (px, y + 280 - int(sz * 1.37)), s)
        d.text((x + 150, y + 300), "DOLLY IN → larger", fill=(200, 0, 0), font=font(18))
    elif kind == "truck":
        for px in [x + 60, x + 200, x + 320]:
            s = sil.copy(); s.thumbnail((110, 150), Image.LANCZOS); img.paste(s, (px, y + 120), s)
        d.line([(x + 60, y + 300), (x + 410, y + 300)], fill=(0, 120, 0), width=4)
        d.text((x + 130, y + 310), "CAMERA TRUCKS → with figure", fill=(0, 120, 0), font=font(18))
    elif kind == "wide":
        s = sil.copy(); s.thumbnail((130, 178), Image.LANCZOS); img.paste(s, (x + 170, y + 90), s)
        d.line([(x + 30, y + 270), (x + 440, y + 270)], fill=(0, 0, 0), width=3); d.text((x + 30, y + 278), "GROUND", fill=(0, 0, 0), font=font(16))
    elif kind == "medium":
        s = sil.copy(); crop = s.crop((0, 0, s.size[0], int(s.size[1] * 0.62))); crop = crop.resize((220, int(220 * crop.size[1] / crop.size[0])), Image.LANCZOS)
        img.paste(crop, (x + 125, y + 60), crop)
        d.line([(x + 30, y + 270), (x + 440, y + 270)], fill=(0, 0, 0), width=3); d.text((x + 30, y + 278), "WAIST LINE", fill=(0, 0, 0), font=font(16))
    else:
        s = sil.copy(); crop = s.crop((0, 0, s.size[0], int(s.size[1] * 0.30))); crop = crop.resize((300, int(300 * crop.size[1] / crop.size[0])), Image.LANCZOS)
        img.paste(crop, (x + 85, y + 60), crop)
        d.text((x + 150, y + 300), "HEAD / FIST ONLY", fill=(200, 0, 0), font=font(18))
img.save(os.path.join(O, "camera-move-sheet-20261031.png")); print("camera sheet", img.size)

# ---------- 4. EDITED SEQUENCES: frame sequences + contact sheets ----------
def prep_frame(path, size=(550, 750), bg=(128, 128, 128)):
    im = Image.open(path).convert("RGBA")
    canvas = Image.new("RGBA", im.size, bg + (255,))
    canvas.paste(im, (0, 0), im)
    return canvas.convert("RGB").resize(size, Image.LANCZOS)

punch_plan = [("windup", FIGHT, 6), ("snap", JOINT_PUNCH, 2), ("impact hold", IMPACT, 12), ("recover", APOSE, 6)]
n = 0; punch_frames_meta = []
for name, path, hold in punch_plan:
    fr = prep_frame(path)
    for k in range(hold):
        n += 1; fr.save(os.path.join(O, "_frames_punch", f"p{n:03d}.png"))
        punch_frames_meta.append({"edit_frame": n, "beat": name, "source": os.path.basename(path), "hold_frames": hold})
print("punch edit frames", n)
# dance beat-held
beat_starts = [1, 15, 28, 42, 56, 69, 83, 97, 110]
beat_files = ["dance-improved-f001.png", "dance-improved-f015.png", "dance-improved-f028.png", "dance-improved-f042.png",
              "dance-improved-f056.png", "dance-improved-f069.png", "dance-improved-f083.png", "dance-improved-f097.png"]
n = 0; dance_meta = []
for bi, (bs, fn) in enumerate(zip(beat_starts[:-1], beat_files)):
    hold = beat_starts[bi + 1] - bs
    fr = prep_frame(os.path.join(R, "dance-improved-20261031/frames", fn), bg=(30, 30, 50))
    for k in range(hold):
        n += 1; fr.save(os.path.join(O, "_frames_dance", f"d{n:03d}.png"))
    dance_meta.append({"beat": bi + 1, "beat_start_frame": bs, "hold_frames": hold, "source": fn})
print("dance edit frames", n)
edit_json = {"version": "edited-sequences-20261031", "date": "2026-10-31", "fps": 24, "codec": "libx264, yuv420p",
    "punch_sequence": {"source_order": "Stream H edit order: windup 6f / snap 2f / impact hold 12f / recover 6f = 26 frames (1.08 s)",
        "beats": [{"beat": nm, "source": os.path.basename(p), "hold_frames": h} for nm, p, h in punch_plan],
        "total_frames": 26, "file": "punch-sequence-edited-20261031.mp4",
        "note": "Only one clean punch frame exists (impact hold); windup uses the clean fighting-pose plate, snap the clean joint-punch plate, recover the clean apose plate. Holds, not new poses — a re-posed windup/snap/recover pass is still owed."},
    "dance_sequence": {"source": "dance-improved-20261031/frames (beat-held: each beat-start frame held to the next beat)",
        "beats": dance_meta, "total_frames": n, "file": "dance-sequence-edited-20261031.mp4",
        "note": "Beat starts from dance-improved BEAT-SHEET.md (107 BPM grid, beats 1,15,28,42,56,69,83,97). Known defects carry over: weak kick frame, twist is an arms/legs stand-in — see beat sheet."},
    "mars_approval": 0}
json.dump(edit_json, open(os.path.join(O, "edited-sequences-20261031.json"), "w"), indent=1)

def contact(frames, titles, path, title, subtitle, cols=4):
    W = 1500; tw = W // cols; th = 470
    rows = (len(frames) + cols - 1) // cols
    img = Image.new("RGB", (W, 150 + rows * th), (240, 240, 235)); d = ImageDraw.Draw(img)
    d.text((30, 18), title, fill=(0, 0, 0), font=font(30))
    y = 60
    for ln in textwrap.wrap(subtitle, width=100):
        d.text((30, y), ln, fill=(60, 60, 60), font=font(19, False)); y += 25
    for i, (fr, cap) in enumerate(zip(frames, titles)):
        x = (i % cols) * tw + 20; yy = 140 + (i // cols) * th
        t = fr.copy(); t.thumbnail((tw - 40, 400), Image.LANCZOS)
        img.paste(t, (x, yy), t if t.mode == "RGBA" else None)
        for j, ln in enumerate(textwrap.wrap(cap, width=32)):
            d.text((x, yy + 410 + j * 22), ln, fill=(0, 0, 0), font=font(17))
    img.save(path); print("contact", path, img.size)

contact([prep_frame(p) for _, p, _ in punch_plan],
        ["WINDUP 6f — fighting-pose plate", "SNAP 2f — joint-punch plate", "IMPACT HOLD 12f — punch-09-impact-hold clean", "RECOVER 6f — apose plate"],
        os.path.join(O, "punch-sequence-contact-20261031.png"),
        "PUNCH SEQUENCE — CONTACT SHEET (edited, 26f @24fps)",
        "Stream H edit order: windup 6 / snap 2 / impact hold 12 / recover 6. Labels on this sheet only; clean plates unchanged.")
contact([prep_frame(os.path.join(R, "dance-improved-20261031/frames", f), bg=(30, 30, 50)) for f in beat_files],
        [f"BEAT {i+1} start F{bs} hold {beat_starts[i+1]-bs}f — {fn}" for i, (bs, fn) in enumerate(zip(beat_starts[:-1], beat_files))],
        os.path.join(O, "dance-sequence-contact-20261031.png"),
        "DANCE SEQUENCE — CONTACT SHEET (beat-held, 109f @24fps)",
        "Beat-held from dance-improved frames. Labels on this sheet only; dance defects (weak kick, twist stand-in) carry over.")

# ---------- 6. SAFE-AREA OVERLAY ----------
room = Image.open(os.path.join(R, "showcase/layout-pass-room-scaled-25x-20261031.jpg")).convert("RGB")
# sheet: room layout scaled to fit, percentages drawn over it
W, H = 1500, 1500
img = Image.new("RGB", (W, H), (240, 240, 235)); d = ImageDraw.Draw(img)
d.text((30, 18), "SAFE-AREA OVERLAY — PERCENTAGE-BASED (NO FRAME SIZE SET HERE)", fill=(0, 0, 0), font=font(30))
y = 60
for ln in textwrap.wrap("Action-safe 90% and title-safe 80% as percentages of whatever the delivery frame is. The delivery frame size itself is Mars-only and is NOT set here — no pixel frame size is claimed. Overlay drawn on a copy for this sheet only; the clean room layout is unchanged.", width=100):
    d.text((30, y), ln, fill=(60, 60, 60), font=font(19, False)); y += 25
ox, oy, ow, oh = 60, y + 10, 1380, 1180
base = room.copy(); base.thumbnail((ow, oh), Image.LANCZOS)
img.paste(base, (ox, oy))
bw, bh = base.size
# action-safe 90%: 5% inset; title-safe 80%: 10% inset — percentages of the placed image
d.rectangle([ox + bw * 0.05, oy + bh * 0.05, ox + bw * 0.95, oy + bh * 0.95], outline=(0, 180, 0), width=5)
d.text((ox + bw * 0.05 + 8, oy + bh * 0.05 + 8), "ACTION-SAFE 90%", fill=(0, 150, 0), font=font(22))
d.rectangle([ox + bw * 0.10, oy + bh * 0.10, ox + bw * 0.90, oy + bh * 0.90], outline=(220, 0, 0), width=5)
d.text((ox + bw * 0.10 + 8, oy + bh * 0.10 + 8), "TITLE-SAFE 80%", fill=(200, 0, 0), font=font(22))
d.text((ox, oy + bh + 12), "Full placed image = 100% frame (reference only, NOT a delivery size). Keep action inside green, titles inside red.", fill=(0, 0, 0), font=font(18, False))
img.save(os.path.join(O, "safe-area-overlay-20261031.png")); print("safe area", img.size, "room base", room.size)
print("DONE")
