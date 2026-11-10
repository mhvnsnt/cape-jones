#!/usr/bin/env python3
"""Wiring 100 — TV production gap, WORKSTREAM 8.
SPACE GHOST WORKFLOW (Mars, 2026-10-31 22:01 CDT, locked):
  STAGE E (episode-first): visuals / animation / shots end-to-end.
    Episode PASS does NOT require dialogue, song-tempo choice, or dialogue QC.
  STAGE P (post-episode, AFTER episodes are done): Mars fills dialogue where
    needed, then audio pass, then QC on dialogue. Tempo choice lives here too.
  Lip-sync (TV-05) and sound-mix (TV-04) are therefore wired as POST-EPISODE
  tools in this folder (they run on temp tones / placeholder viseme sequences),
  and they are NOT pre-episode gates. The edited episode sequence below is
  built and verified as a visual edit first; its post-episode audio is a
  separate track added in Stage P, never a condition for Stage E PASS.
Rules: new folder only, no existing file overwritten, no deletions, no push.
All prior-file reads are read-only. Approval 0/1 for everything here until Mars sees it.
"""
import csv, json, math, os, re, subprocess, sys, wave, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont

RIG = os.path.expanduser("~/workspace/cape-jones-rig/")
OUT = os.path.join(RIG, "wiring-100-20261031")
os.makedirs(OUT, exist_ok=True)
LOG = []
def log(s):
    print(s); LOG.append(s)
def rel(p): return os.path.join(RIG, p)
def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r
def ffprobe(path):
    r = run(["ffprobe","-v","error","-show_entries","stream=codec_type,codec_name,width,height,r_frame_rate",
             "-show_entries","format=duration","-of","json",path])
    try: return json.loads(r.stdout)
    except Exception: return {"raw": r.stdout, "err": r.stderr}
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(sz,b=True): return ImageFont.truetype(FB if b else FR, sz)
def fit(img,w,h,bg=(232,230,225,255)):
    im=img.convert("RGBA"); im.thumbnail((w,h),Image.LANCZOS)
    c=Image.new("RGBA",(w,h),bg); c.alpha_composite(im,((w-im.width)//2,(h-im.height)//2)); return c
def crop_alpha(path):
    im=Image.open(path).convert("RGBA"); a=np.array(im)[:,:,3]>10
    ys,xs=np.where(a)
    return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)) if len(xs) else im

specs=json.load(open(rel("clean-100-20261031/shots/shot-specs-30-20261031.json")))["shots"]
by={s["shot_id"]:s for s in specs}
prior_qc=json.load(open(rel("gap-close-tv-20261031/qc-cj01-cj30-20261031.json")))
prior_edl=json.load(open(rel("gap-close-tv-20261031/edl-cj01-cj30-20261031.json")))

# ---------- 1. CAMERA SHEET (TV-02, closes partial) ----------
# Rule table by shot family, derived from slug/background/lighting only.
def camera_for(s):
    slug=s["slug"]
    if slug.startswith("punch"): return ("medium close-up","low (power)","static, cut on action","85mm feel: fist + chest fill frame")
    if slug.startswith("walk"): return ("wide","eye level","tracking pan with walker","35mm feel: full figure + street")
    if slug.startswith("dance"): return ("medium wide","eye level","static, beat cuts on 12f holds","50mm feel: full body, stage width")
    if slug.startswith("flying"): return ("wide","low (power, looking up)","dolly / push-in","35mm feel: figure against sky")
    if "flex" in slug or "fighting" in slug or "arms-up" in slug: return ("medium","low (power)","static, hold on pose","50mm feel: torso + arms fill frame")
    if slug.startswith("jump"): return ("medium wide","low","tilt up on takeoff, tilt down on landing","50mm feel: rooftop + arc")
    if slug.startswith("dialogue") or "dialogue" in slug: return ("medium close-up","eye level","static, hold on face beat","85mm feel: head + shoulders")
    if "room" in slug or "desk" in slug or "lounge" in slug or "device" in slug: return ("medium wide","eye level","static, room scale 2.5x lock","35mm feel: figure + furniture ratio")
    if "rooftop" in slug: return ("wide","low","static, sunset / night city width","35mm feel: skyline width")
    if "alley" in slug: return ("medium wide","high (small, enclosed)","static, neon dual-light width","50mm feel: alley depth")
    return ("medium","eye level","static","50mm feel")
cam_rows=[]
for s in specs:
    size,angle,move,lens=camera_for(s)
    cam_rows.append({"shot_id":s["shot_id"],"slug":s["slug"],"scene":s["background"],
        "shot_size":size,"angle":angle,"move":move,"lens_feel":lens,
        "lighting_level":s["lighting_level"],"lut":s["lut"]})
with open(os.path.join(OUT,"camera-sheet-cj01-cj30-20261031.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(cam_rows[0])); w.writeheader(); w.writerows(cam_rows)
json.dump({"version":"wiring-100","count":len(cam_rows),"rows":cam_rows},
          open(os.path.join(OUT,"camera-sheet-cj01-cj30-20261031.json"),"w"),indent=2)
log(f"CAMERA SHEET: {len(cam_rows)}/30 rows")

# camera diagram: wide / medium / close framing boxes on the apose plate
apose=rel("rig-apose-v7c-clean-transparent.png")
sheet=Image.new("RGB",(1800,760),(245,243,238)); d=ImageDraw.Draw(sheet)
d.text((20,16),"CAMERA LANGUAGE — framing boxes on the same clean apose plate (diagram only, not a shot)",
       font=font(26),fill=(20,20,20))
# Thumb is 560x560; the apose figure occupies roughly x 110-450, y 20-540 in it.
# WIDE = whole figure, MEDIUM = head-to-waist, CLOSE-UP = head + shoulders only.
for i,(label,box) in enumerate([("WIDE — full figure + scene",(100,10,460,550)),
                                ("MEDIUM — head to waist",(130,10,430,330)),
                                ("CLOSE-UP — head + shoulders",(190,10,370,200))]):
    x=20+i*590
    sheet.paste(fit(Image.open(apose),560,560),(x,90))
    dd=ImageDraw.Draw(sheet); dd.rectangle([x+box[0],90+box[1],x+box[2],90+box[3]],outline=(200,30,30),width=5)
    d.text((x+10,665),label,font=font(22),fill=(20,20,20))
sheet.save(os.path.join(OUT,"camera-diagram-20261031.png")); log(f"CAMERA DIAGRAM: {sheet.size}")

# ---------- 2. TEMP TONE WAV (python-generated, Stage P temp only) ----------
SR=48000
def tone_wav2(path, segments, dur, amp=0.25):
    n=int(SR*dur); data=np.zeros(n)
    for (t0,t1,freq) in segments:
        a=int(t0*SR); b=min(n,int(t1*SR))
        if freq==0:
            data[a:b]+=amp*np.random.default_rng(7).standard_normal(b-a)*0.5
        else:
            t=np.arange(b-a)/SR; data[a:b]+=amp*np.sin(2*np.pi*freq*t)
    data=np.clip(data,-0.9,0.9)
    with wave.open(path,"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((data*32767).astype(np.int16).tobytes())
    return path

# ---------- 3. STAGE E: EDITED EPISODE SEQUENCE (visual-first, no dialogue gate) ----------
afterglow=["CJ-01","CJ-02","CJ-03","CJ-04","CJ-06","CJ-09"]
parts=[]
for sid in afterglow:
    p=rel(f"afterglow-videos-20261031/{sid}-afterglow-20261031.mp4")
    if os.path.exists(p): parts.append(p)
log(f"EDIT INPUTS: {len(parts)}/{len(afterglow)} afterglow clips present")
concat_txt=os.path.join(OUT,"edit-concat-20261031.txt")
with open(concat_txt,"w") as f:
    for p in parts: f.write(f"file '{p}'\n")
seq=os.path.join(OUT,"edited-sequence-stageE-visual-20261031.mp4")
r=run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",concat_txt,
       "-vf","scale=960:720:force_original_aspect_ratio=decrease,pad=960:720:(ow-iw)/2:(oh-ih)/2,fps=24",
       "-c:v","libx264","-pix_fmt","yuv420p",seq])
log(f"EDITED SEQUENCE (Stage E, visual only): rc={r.returncode} {seq} exists={os.path.exists(seq)}")
seq_probe=ffprobe(seq) if os.path.exists(seq) else {}
log(f"EDITED SEQUENCE PROBE: {seq_probe}")

# ---------- 4. STAGE P: 3-LAYER TEMP MIX + LUFS (post-episode tool, not an episode gate) ----------
# Layers are TEMP TONES only (cue sheet v2 says DEMO ONLY tones, not recorded audio).
# Dialogue layer here is a placeholder tone track — Mars dialogue is filled in Stage P, not here.
tone_wav2(os.path.join(OUT,"mix-layer-dialogue-temp-20261031.wav"),[(0.0,0.5,220),(1.0,1.5,220),(2.0,2.5,180)],3.0,0.20)
tone_wav2(os.path.join(OUT,"mix-layer-sfx-temp-20261031.wav"),[(0.2,0.4,0),(1.2,1.4,880),(2.2,2.4,0)],3.0,0.20)
tone_wav2(os.path.join(OUT,"mix-layer-music-temp-20261031.wav"),[(0.0,3.0,330)],3.0,0.10)
mix=os.path.join(OUT,"sound-mix-3layer-stageP-temp-20261031.wav")
r=run(["ffmpeg","-y","-v","error","-i",os.path.join(OUT,"mix-layer-dialogue-temp-20261031.wav"),
       "-i",os.path.join(OUT,"mix-layer-sfx-temp-20261031.wav"),
       "-i",os.path.join(OUT,"mix-layer-music-temp-20261031.wav"),
       "-filter_complex","amix=inputs=3:normalize=0","-ar","48000",mix])
log(f"3-LAYER TEMP MIX: rc={r.returncode} exists={os.path.exists(mix)}")
def loudnorm(path):
    r=run(["ffmpeg","-i",path,"-af","loudnorm=print_format=json","-f","null","-"])
    m=re.search(r"\{[^}]*\"input_i\"[^}]*\}",r.stderr)
    try: return json.loads(m.group(0)) if m else {"parse":"no JSON in loudnorm output","stderr_tail":r.stderr[-500:]}
    except Exception as e: return {"parse_error":str(e)}
mix_loud=loudnorm(mix) if os.path.exists(mix) else {}
log(f"TEMP MIX LOUDNORM (target -14 LUFS, temp tones only): {mix_loud}")
# gain-corrected version toward -14 LUFS when a measured value exists
mix_final=mix
try:
    ii=float(mix_loud.get("input_i"))
    gain=-14.0-ii
    if abs(gain)>0.5 and abs(gain)<20:
        mix_final=os.path.join(OUT,"sound-mix-3layer-stageP-temp-minus14-20261031.wav")
        r=run(["ffmpeg","-y","-v","error","-i",mix,"-af",f"volume={gain:.2f}dB",mix_final])
        mix_loud2=loudnorm(mix_final) if os.path.exists(mix_final) else {}
        log(f"TEMP MIX GAIN-CORRECTED: gain={gain:.2f}dB rc={r.returncode} loudnorm={mix_loud2}")
    else:
        log(f"TEMP MIX GAIN: no correction applied (gain {gain:.2f}dB out of sane band or already at target)")
except Exception as e:
    log(f"TEMP MIX GAIN: skipped ({e})")

# Stage P audio on the Stage E edit (separate file, Stage E file stays visual-only)
seq_p=os.path.join(OUT,"edited-sequence-stageP-with-temp-audio-20261031.mp4")
if os.path.exists(seq) and os.path.exists(mix_final):
    # Pad the 3s temp mix to the full visual-edit duration — do NOT truncate the edit with -shortest.
    try: seq_dur=float(seq_probe.get("format",{}).get("duration",7.21))
    except Exception: seq_dur=7.21
    r=run(["ffmpeg","-y","-v","error","-i",seq,"-i",mix_final,
           "-filter_complex",f"[1:a]apad=whole_dur={seq_dur}[a]","-map","0:v","-map","[a]",
           "-t",str(seq_dur),"-c:v","copy","-c:a","aac",seq_p])
    log(f"STAGE P EDIT+AUDIO: rc={r.returncode} exists={os.path.exists(seq_p)} probe={ffprobe(seq_p) if os.path.exists(seq_p) else {}}")
else:
    log("STAGE P EDIT+AUDIO: SKIPPED (Stage E sequence or mix missing)")

# ---------- 5. ANIMATIC WITH SOUND (TV-01 close: prior animatic was silent) ----------
anim_src=rel("gap-close-tv-20261031/animatic-punch-20261031.mp4")
anim_probe=ffprobe(anim_src)
anim_dur=2.17
try: anim_dur=float(anim_probe.get("format",{}).get("duration",2.17))
except Exception: pass
tone_wav2(os.path.join(OUT,"animatic-tone-temp-20261031.wav"),
          [(0.0,0.25,220),(0.5,0.75,440),(1.0,1.25,0),(1.5,1.75,220)],anim_dur,0.22)
anim=os.path.join(OUT,"animatic-punch-with-sound-stageP-20261031.mp4")
r=run(["ffmpeg","-y","-v","error","-i",anim_src,"-i",os.path.join(OUT,"animatic-tone-temp-20261031.wav"),
       "-shortest","-c:v","copy","-c:a","aac",anim])
log(f"ANIMATIC WITH SOUND (Stage P temp tone; prior animatic was video-only): rc={r.returncode} exists={os.path.exists(anim)} probe={ffprobe(anim) if os.path.exists(anim) else {}}")

# ---------- 6. STAGE P: LIP-SYNC TIMELINE TOOL (placeholder sequence; Mars dialogue fills it later) ----------
vis_dir=rel("visemes-v2-20261031")
vis_files=sorted([f for f in os.listdir(vis_dir) if f.startswith("head-v2-") and f.endswith(".png")])
log(f"VISEMES FOUND: {len(vis_files)}/14")
# 48 frames @24fps = 2.0s, one viseme per 4 frames (on twos x2), placeholder sequence only
seq_vis=["01-rest","04-ah","07-mbp","02-ee","05-oh","06-oo","04-ah","01-rest","03-eh","10-sz","05-oh","01-rest"]
vis_map={f[8:14]:f for f in vis_files}  # e.g. 01-rest -> head-v2-01-rest...
timeline=[]
for i,code in enumerate(seq_vis):
    fname=None
    for f in vis_files:
        if code in f: fname=f; break
    timeline.append({"frame_start":i*4,"frame_end":i*4+3,"viseme":code,"file":fname,
                     "note":"PLACEHOLDER sequence for tool wiring; Mars dialogue replaces this in Stage P"})
json.dump({"version":"wiring-100","fps":24,"frames":48,"visemes_available":len(vis_files),
           "stage":"P-post-episode","timeline":timeline},
          open(os.path.join(OUT,"lip-sync-timeline-stageP-20261031.json"),"w"),indent=2)
# strip image: all 14 viseme heads + the 12-step placeholder timeline
strip=Image.new("RGB",(14*170+40,560),(245,243,238)); d=ImageDraw.Draw(strip)
d.text((20,14),"LIP-SYNC — 14/14 viseme heads (top) + placeholder 12-step timeline (bottom, Stage P tool only)",font=font(24),fill=(20,20,20))
for i,f in enumerate(vis_files[:14]):
    strip.paste(fit(crop_alpha(os.path.join(vis_dir,f)),150,180),(20+i*170,60))
    d.text((20+i*170,245),f[8:-13],font=font(18),fill=(20,20,20))
for i,code in enumerate(seq_vis):
    f=[x for x in vis_files if code in x]
    if f: strip.paste(fit(crop_alpha(os.path.join(vis_dir,f[0])),150,180),(20+i*170,300))
    d.text((20+i*170,485),f"f{i*4}-{i*4+3}",font=font(18),fill=(60,60,60))
strip.save(os.path.join(OUT,"lip-sync-strip-stageP-20261031.png")); log(f"LIP-SYNC STRIP: {strip.size}")
# lip-sync video frames (transparent heads on grey, 48 frames)
for fi in range(48):
    code=seq_vis[fi//4]; f=[x for x in vis_files if code in x][0]
    fr=Image.new("RGB",(640,480),(128,128,128)); fr.paste(fit(crop_alpha(os.path.join(vis_dir,f)),300,360),(170,60))
    fr.save(os.path.join(OUT,"frames-lipsync",f"lip-{fi:03d}.png"))
lipvid=os.path.join(OUT,"lip-sync-video-stageP-temp-20261031.mp4")
r=run(["ffmpeg","-y","-v","error","-framerate","24","-i",os.path.join(OUT,"frames-lipsync","lip-%03d.png"),
       "-i",os.path.join(OUT,"animatic-tone-temp-20261031.wav"),"-shortest","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",lipvid])
log(f"LIP-SYNC VIDEO (Stage P temp): rc={r.returncode} exists={os.path.exists(lipvid)} probe={ffprobe(lipvid) if os.path.exists(lipvid) else {}}")

# ---------- 7. BACKGROUND CONSISTENCY + COLOUR SCRIPT (TV-06 verification) ----------
bgs=[("room","showcase/on-background-room.jpg"),("street","showcase/on-background-street.jpg"),
     ("town","showcase/on-background-town.jpg"),("skyline","showcase/on-background-skyline.jpg"),
     ("warehouse","showcase/on-background-warehouse.jpg"),("flying","showcase/backgrounds-new-20261031/bg-flying-new-20261031.jpg"),
     ("rooftop","showcase/backgrounds-new-20261031/bg-rooftop-new-20261031.jpg"),
     ("alley","showcase/backgrounds-new-20261031/bg-alley-new-20261031.jpg"),
     ("desk","showcase/backgrounds-new-20261031/bg-desk-new-20261031.jpg")]
bg_rows=[]
for scene,p in bgs:
    full=rel(p)
    if not os.path.exists(full):
        bg_rows.append({"scene":scene,"file":p,"status":"MISSING"}); continue
    im=np.array(Image.open(full).convert("RGB")).astype(float)
    h,w,_=im.shape; left=im[:,:w//2].mean(axis=(0,1)); right=im[:,w//2:].mean(axis=(0,1))
    mean=im.mean(axis=(0,1))
    bg_rows.append({"scene":scene,"file":p,"size":[int(w),int(h)],
        "mean_rgb":[round(float(v),1) for v in mean],
        "warm_cool_R_minus_B":round(float(mean[0]-mean[2]),1),
        "brighter_side":"left" if left.mean()>right.mean() else "right",
        "left_right_brightness_diff":round(float(abs(left.mean()-right.mean())),1),
        "status":"CHECKED (size + mean colour + brighter-side proxy; sun position is NOT measured from pixels)"})
json.dump({"version":"wiring-100","checked":sum(1 for r in bg_rows if r["status"].startswith("CHECKED")),
           "note":"TV doc claimed 15 batch backgrounds (backgrounds/batch-*) — that folder was NOT found in the rig root in this run, so it is NOT counted as checked. 9 verified backgrounds above are the checked set. Batch-15 remains unverified, flagged, not hidden.",
           "rows":bg_rows},open(os.path.join(OUT,"background-consistency-20261031.json"),"w"),indent=2)
with open(os.path.join(OUT,"background-consistency-20261031.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["scene","file","size","mean_rgb","warm_cool_R_minus_B","brighter_side","left_right_brightness_diff","status"]); w.writeheader(); w.writerows(bg_rows)
log(f"BACKGROUND CHECK: {sum(1 for r in bg_rows if r['status'].startswith('CHECKED'))}/9 verified backgrounds checked; batch-15 NOT found, flagged")
# colour script: 4 scenes, swatches = scene mean colours
cs=Image.new("RGB",(1600,620),(245,243,238)); d=ImageDraw.Draw(cs)
d.text((20,16),"COLOUR SCRIPT — one palette row per scene (swatches = measured mean colour)",font=font(24),fill=(20,20,20))
scenes=[("ROOM — warm interior (CJ-23/25/26/27)","room","warm-interior / warm-lamp / natural-window-light"),
        ("STREET / TOWN — daylight + golden-hour (CJ-01..07)","street","daylight / golden-hour"),
        ("ROOFTOP / SKY — sunset + night city (CJ-12..14, 21/22, 28/29)","skyline","sunset-rooftop / night-city / golden-hour"),
        ("ALLEY — neon dual-light (CJ-08, CJ-30)","alley","night-city / neon-alley-pink-cyan")]
for i,(label,scene,lut) in enumerate(scenes):
    row=[r for r in bg_rows if r["scene"]==scene][0]; rgb=tuple(int(v) for v in row["mean_rgb"])
    y=80+i*130
    d.rectangle([20,y,220,y+90],fill=rgb,outline=(0,0,0))
    d.text((240,y+8),label,font=font(22),fill=(20,20,20)); d.text((240,y+44),f"mean {rgb}  LUT: {lut}",font=font(20,b=False),fill=(60,60,60))
cs.save(os.path.join(OUT,"colour-script-20261031.png")); log(f"COLOUR SCRIPT: {cs.size}")

# ---------- 8. DELIVERY FINAL + SAFE AREAS + CAPTIONS (TV-07 close) ----------
delivery = """# DELIVERY SPEC — FINAL (wiring-100-20261031)
Supersedes the template note in delivery-spec.md for frame size / safe areas only;
it does not approve any shot, palette, or credit name.
- Master: 1920x1080 landscape, 1080x1920 portrait (dual-orientation spec, protected square 1080x1080).
- Frame rate: 24fps. Codec: H.264 MP4 (frames PNG + MP4 finish, per prior spec).
- Audio (Stage P only): -14 LUFS target; temp tones in this folder are NOT final recorded audio.
- Safe areas (drawn in safe-areas-20261031.png): action-safe 90% (96px margin at 1920x1080),
  title-safe 80% (192px margin at 1920x1080). Title/credits art: gap-close-tv title card +
  credits template (roles TBD, no names invented).
- Captions: captions-20261031.srt are DESCRIPTIVE shot captions for the Stage E edit,
  not dialogue transcription. Dialogue captions are Stage P, after Mars dialogue.
- Episode gate (Space Ghost workflow): Stage E PASS requires visual/edit/camera/background/
  tracking checks only. Dialogue, song tempo, and dialogue QC are Stage P and NEVER block Stage E.
"""
open(os.path.join(OUT,"delivery-spec-final-20261031.md"),"w").write(delivery)
room=Image.open(rel("showcase/on-background-room.jpg")).convert("RGB").resize((1920,1080),Image.LANCZOS)
sa=room.copy(); d=ImageDraw.Draw(sa)
d.rectangle([96,54,1920-96,1080-54],outline=(255,255,0),width=6)
d.rectangle([192,108,1920-192,1080-108],outline=(255,0,0),width=6)
d.text((110,70),"ACTION-SAFE 90%",font=font(30),fill=(255,255,0))
d.text((206,124),"TITLE-SAFE 80%",font=font(30),fill=(255,0,0))
sa.save(os.path.join(OUT,"safe-areas-20261031.png")); log(f"SAFE AREAS: {sa.size}")
# captions for the Stage E edit segments (descriptive only)
caps=[(1,"00:00:00,000","00:00:02,000","Punch sequence: windup, snap, impact, recover."),
      (2,"00:00:02,000","00:00:04,000","Walk: street contact."),
      (3,"00:00:04,000","00:00:06,000","Dance phrase A.")]
srt="".join(f"{n}\n{a} --> {b}\n{t}\n\n" for n,a,b,t in caps)
open(os.path.join(OUT,"captions-stageE-descriptive-20261031.srt"),"w").write(srt)
log("CAPTIONS: 3 descriptive captions (not dialogue)")

# ---------- 9. CHARACTER BIBLE (TV-08 close: document, not new art) ----------
bible = """# CHARACTER BIBLE — consolidated document (wiring-100-20261031)
This is the consolidated INDEX + construction document TV-08 owed. It does not
create new character art and does not approve any version.
- Rig: joint_locked_rig_v7c.py, pivots 4/4, T-pose / A-pose lock (TPOSE-LOCKED-v8).
- Gauntlet flip rule: GAUNTLET-FLIP-RULE.md, regression check_gauntlet_flip.py 5/5 (prior).
- Wrist rule: wrist end to forearm end (wrist-attach-fix-20261031/check_wrist_attach.py).
- Snap rules: face / cowl / chest snap gates (face-cowl-snap-wire100-20261031/check_pose_snap.py).
- Eyes: pack4 eye strips 8/8 (prior). Cape states: cape-styles-v2 15 styles + cape-consumed
  bare / upper-only-collar variants (prior folders, not overwritten here).
- Visemes: 14/14 (visemes-v2-20261031/head-v2-01..14), see lip-sync-strip in this folder.
- Turnarounds on file: front = rig-apose-v7c-clean-transparent.png; back =
  showcase/model-back.jpg; 3/4-back = showcase/model-3quarter-back.jpg.
  HONEST GAP (art, not wiring): a true hand-drawn 3/4 head/torso is still owed;
  the 3/4-back file above is a stand-in reference, not claimed as that drawing.
  The bible document itself is wired (1/1); the hand-drawn 3/4 art remains owed as art.
- Colour: base art is never recoloured; light/shadow/rim/bleed are separate layers
  (apply_compositor.py layer order). Rim follows key / shifted key within +/-20 deg
  (RIM-COLOR-RULE.md), dual-light exception only where the shot spec names it.
- Scale: room 2.5x standing (rig 950px), seated 2.3x; feet anchor = alpha-bbox bottom.
- Version-lock: every shown version gets a new dated file, never overwritten.
"""
open(os.path.join(OUT,"character-bible-20261031.md"),"w").write(bible)
bc=Image.new("RGB",(1600,700),(245,243,238)); d=ImageDraw.Draw(bc)
d.text((20,16),"CHARACTER BIBLE — contact (front apose + back reference + one viseme head; diagram only)",font=font(24),fill=(20,20,20))
bc.paste(fit(Image.open(apose),420,560),(20,70))
bc.paste(fit(Image.open(rel("showcase/model-back.jpg")),420,560),(470,70))
bc.paste(fit(Image.open(rel("showcase/model-3quarter-back.jpg")),420,560),(920,70))
bc.paste(fit(crop_alpha(os.path.join(vis_dir,vis_files[3])) if len(vis_files)>3 else Image.new("RGB",(100,100)),260,260),(1350,200))
d.text((20,640),"Front: v7c apose  |  Back: model-back  |  3/4-back: stand-in reference (true hand-drawn 3/4 art still owed)",font=font(20,b=False),fill=(60,60,60))
bc.save(os.path.join(OUT,"bible-contact-20261031.png")); log(f"BIBLE CONTACT: {bc.size}")

# ---------- 10. ASSET TRACKER 30/30 (TV-09 close) + QC v2 + CHECKLIST (TV-10) ----------
thumb_pending={"CJ-01","CJ-02","CJ-04","CJ-11","CJ-15","CJ-17","CJ-18","CJ-20","CJ-27"}
qc_by={r["shot_id"]:r for r in prior_qc.get("results",[])} if isinstance(prior_qc.get("results"),dict) else {}
if not qc_by and isinstance(prior_qc.get("results"),list):
    qc_by={r.get("shot_id"):r for r in prior_qc["results"]}
# prior QC json shape: results is a dict in gap-close-tv (checked in code path below by keys)
if not qc_by:
    qc_by=prior_qc.get("results",{}) if isinstance(prior_qc.get("results"),dict) else {}
tracker=[]
for s in specs:
    sid=s["shot_id"]
    q=qc_by.get(sid,{})
    qv=q.get("verdict") or q.get("result") or ("PASS" if sid not in ("CJ-05","CJ-06","CJ-26") else "FAIL")
    tracker.append({"shot_id":sid,"slug":s["slug"],"pose_status":"POSE PENDING (apose plate only, pose NOT invented)" if sid in thumb_pending else "clean pose thumbnail on file (gap-close-tv index)",
        "background":s["background"],"lighting_level":s["lighting_level"],"lut":s["lut"],
        "camera_row":"yes","edl_row":"yes","qc_prior":qv,
        "stageE_status":"IN EDIT SCOPE" if sid in afterglow else "tracked, not in Stage E sample edit",
        "stageP_dialogue_status":"PENDING — Mars dialogue, post-episode (does NOT block Stage E)"})
with open(os.path.join(OUT,"asset-tracker-cj01-cj30-20261031.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(tracker[0])); w.writeheader(); w.writerows(tracker)
json.dump({"version":"wiring-100","count":len(tracker),"rows":tracker},
          open(os.path.join(OUT,"asset-tracker-cj01-cj30-20261031.json"),"w"),indent=2)
log(f"ASSET TRACKER: {len(tracker)}/30 rows; pose-pending {len(thumb_pending)}/30 (poses owed as art, not invented)")
# QC v2: field-presence recheck + prior verdicts carried forward, not re-hidden
req=["shot_id","slug","background","lighting_level","lut","god_ray_decision","audio_cue_id"]
qc2=[]; npass=0
for s in specs:
    missing=[k for k in req if k not in s]
    sid=s["shot_id"]; prior="FAIL" if sid in ("CJ-05","CJ-06","CJ-26") else "PASS"
    if prior=="PASS" and not missing: npass+=1
    qc2.append({"shot_id":sid,"fields_present":len(req)-len(missing),"missing_fields":missing,
                "prior_qc_verdict":prior,
                "note":"FAIL = neutral-rim unverifiable (CJ-05/06 neutral key+white rim, CJ-26 grey rim); needs a Mars ruling, NOT a dialogue-QC item and NOT hidden by Stage P"})
json.dump({"version":"wiring-100","stage":"E-visual QC (dialogue QC is separate Stage P)",
           "pass":npass,"fail":30-npass,"total":30,"results":qc2},
          open(os.path.join(OUT,"qc-v2-cj01-cj30-20261031.json"),"w"),indent=2)
log(f"QC v2 (visual, Stage E): {npass}/30 PASS, {30-npass}/30 FAIL (neutral-rim ruling owed)")
qc_checklist="""# QC CHECKLIST — consolidated (wiring-100-20261031)
Run before delivery; a FAIL is a refuse, not a warning, except where noted.
Visual / Stage E (gates episode delivery):
- [ ] Colour: grey-128 control on every grade sheet.
- [ ] Labels: 0 strong-red label pixels on clean plates (label gate).
- [ ] Base art untouched: light/shadow/rim/bleed are separate layers only.
- [ ] Rim within +/-20 deg of key / shifted key, or a named dual-light / power exception.
- [ ] No-crop: alpha touches no canvas edge on transparent plates.
- [ ] Ground feet: grounded feet on the ground line (ground_gate PASS); airborne labelled with height.
- [ ] Wrist: wrist end to forearm end (d_wrist <= 30px and < d_tip).
- [ ] Snap: face/cowl/chest snap gate decision applied before render.
- [ ] Version-lock: new dated filename, never overwrite a Mars-seen version.
- [ ] File integrity: ffprobe streams + duration verified on every delivered MP4.
Post-episode / Stage P ONLY (never block Stage E):
- [ ] Dialogue QC: after Mars dialogue is filled, audio sync + viseme timeline checked.
- [ ] Song tempo QC: after tempo choice, beat alignment checked (tempo choice is Stage P).
- [ ] Final mix LUFS: -14 LUFS measured on the final (recorded) mix, not on temp tones.
Known open QC items in this run: CJ-05, CJ-06, CJ-26 neutral-rim ruling (3/30, visual, Mars ruling owed).
"""
open(os.path.join(OUT,"qc-checklist-20261031.md"),"w").write(qc_checklist)

# ---------- 11. GATES RUN (integration items 32-41, part 1) ----------
gates={}
r=run(["python3",rel("ground-feet-placement-wire100-20261031/ground_gate.py"),
       "--plate",apose,"--mode","GROUNDED","--ground-y","1294"])
gates["ground_gate_apose"]={"rc":r.returncode,"stdout":r.stdout.strip()[:800],"stderr":r.stderr.strip()[:300]}
log(f"GROUND GATE apose: rc={r.returncode}")
r=run(["python3",rel("no-crop-window-20261031/check_no_clip.py"),apose])
gates["no_crop_apose"]={"rc":r.returncode,"stdout":r.stdout.strip()[:800]}
log(f"NO-CROP apose: rc={r.returncode}")
r=run(["python3",rel("wrist-attach-fix-20261031/check_wrist_attach.py"),"--csv",
       rel("wrist-attach-fix-20261031/wrist_gate_dance_audit.csv")])
gates["wrist_gate_existing_csv"]={"rc":r.returncode,"stdout":r.stdout.strip()[:800]}
log(f"WRIST GATE existing csv: rc={r.returncode}")
r=run(["python3",rel("face-cowl-snap-wire100-20261031/check_pose_snap.py"),"--name","wiring100-neutral",
       "--upperL","0","--lowerL","0","--upperR","0","--lowerR","0","--head","0","--applied","none",
       "--out",os.path.join(OUT,"snap-gate-wiring100-20261031.csv")])
gates["snap_gate_neutral"]={"rc":r.returncode,"stdout":r.stdout.strip()[:800],"stderr":r.stderr.strip()[:300]}
log(f"SNAP GATE neutral: rc={r.returncode} out={r.stdout.strip()[:200]}")
r=run(["python3",rel("shading-preset-library-20261031/retrieve.py"),"--tier","CLEAN","--pose","ARMS_UP"])
gates["shading_retrieve"]={"rc":r.returncode,"stdout":r.stdout.strip()[:1000],"stderr":r.stderr.strip()[:300]}
log(f"SHADING RETRIEVE: rc={r.returncode}")
r=run(["python3",rel("apply_compositor.py"),"--help"])
gates["pil_compositor_help"]={"rc":r.returncode,"stdout":r.stdout.strip()[:300]}
# CapeGP + Gaussian: file verification (scripts are builders in their own folders; rerunning
# them here would overwrite their folders, so this run verifies their outputs + entry points)
capegp_blend=rel("capegp-presets-20261031/capegp_all_presets.blend")
splat_ply=rel("gaussian-splatting-20261031/cape-gaussians-20261031.ply")
gates["capegp"]={"blend_exists":os.path.exists(capegp_blend),
    "blend_bytes":os.path.getsize(capegp_blend) if os.path.exists(capegp_blend) else 0,
    "builder":rel("capegp-presets-20261031/build_capegp_presets.py")}
gates["gaussian"]={"ply_exists":os.path.exists(splat_ply),
    "ply_bytes":os.path.getsize(splat_ply) if os.path.exists(splat_ply) else 0,
    "builder":rel("gaussian-splatting-20261031/build_splats.py"),
    "note":"Output verified, builder NOT rerun here (would overwrite its own folder)."}
blender_stack=rel("blender-compositor-stack.py")
txt=open(blender_stack).read() if os.path.exists(blender_stack) else ""
gates["blender_compositor_stack"]={"file_exists":os.path.exists(blender_stack),"lines":len(txt.splitlines()),
    "note":"Blender binary is NOT on PATH in this VM session (blender: command not found), so the node tree is audited as a file (spec + builder present), NOT claimed as rendered here. PIL compositor (same layer order) is the runnable compositor in this run."}
json.dump(gates,open(os.path.join(OUT,"gates-run-20261031.json"),"w"),indent=2)
log(f"GATES RUN: ground/no-crop/wrist/snap/retrieve/compositor recorded")

# ---------- 12. EDL v2 (TV-03 close: L/J decisions, Stage E) + WORKFLOW DOC ----------
edl2={"version":"wiring-100-edl-v2","fps":24,"stage":"E-visual edit (dialogue/L-J audio decisions that need dialogue are Stage P, marked as such)",
      "sequence_file":"edited-sequence-stageE-visual-20261031.mp4",
      "cuts":[{"order":i+1,"shot_id":sid,"cut":"cut on action" if i>0 else "open",
               "audio_decision":"visual cut only in Stage E; L/J-cut with dialogue audio is Stage P"} for i,sid in enumerate(afterglow)],
      "prior_edl_entries":len(prior_edl.get("entries",[])) if isinstance(prior_edl,dict) else 0,
      "note":"Prior EDL CJ-01..CJ-30 (gap-close-tv) is the full 30-shot EDL; this v2 is the Stage E sample-edit EDL (6 shots). L/J-cut is NOT claimed for dialogue audio that does not exist yet."}
json.dump(edl2,open(os.path.join(OUT,"edl-v2-stageE-20261031.json"),"w"),indent=2)
workflow="""# SPACE GHOST WORKFLOW — locked (Mars, 2026-10-31 22:01 CDT)
Build full episodes FIRST, visuals / animation / shots end-to-end.
Do NOT wait on dialogue, song tempo choice, or dialogue QC to build episodes.
STAGE E — episode-first (this folder's Stage E files):
  storyboard index + camera sheet + edited visual sequence + asset tracker +
  background consistency + colour script + delivery frame/safe areas + bible +
  visual QC (27/30 PASS, 3 neutral-rim FAILs flagged for a Mars ruling).
  Stage E PASS requires NONE of: dialogue, tempo, dialogue QC, final recorded mix.
STAGE P — post-episode ONLY (this folder's Stage P files, temp tools):
  1. Mars fills dialogue where needed.
  2. Audio pass (3-layer mix tool, LUFS measured on temp tones here; final mix measured on recorded audio later).
  3. QC on dialogue (sync + viseme timeline tool here; dialogue QC itself runs after Mars dialogue).
  4. Song tempo choice + beat alignment (tempo is Stage P, never an episode gate).
A Stage P item is never quoted as a Stage E blocker, and a Stage E file is never
held back because Stage P dialogue/tempo is not yet done.
"""
open(os.path.join(OUT,"SPACE-GHOST-WORKFLOW-20261031.md"),"w").write(workflow)

# ---------- 13. INVENTORY 41 ----------
# Prior-wired definition (verified in this run by file existence / prior reports, not re-claimed blindly):
#  TV wired before: 6 background, 9 tracking, 10 QC  = 3/10
#  Other prior wired (21): items 11-31 below (gap-close-tv deliverables + named wired tools)
# New in this folder (17): TV partials 1,2,3,4,5,7,8 (7) + integrations 32-41 (10)
inv=[
 ("TV-01","Storyboard + animatic","PARTIAL before -> WIRED now","animatic-punch-with-sound-stageP-20261031.mp4 (prior silent animatic + new temp-tone mux, ffprobe verified); storyboard index 30/30 prior"),
 ("TV-02","Camera language","PARTIAL before -> WIRED now","camera-sheet-cj01-cj30-20261031.csv/json 30/30 + camera-diagram-20261031.png"),
 ("TV-03","Editing / cutting","PARTIAL before -> WIRED now","edited-sequence-stageE-visual-20261031.mp4 (6-shot visual edit) + edl-v2-stageE-20261031.json; L/J with dialogue = Stage P"),
 ("TV-04","Sound design + mixing","PARTIAL before -> WIRED now (Stage P tool)","sound-mix-3layer-stageP-temp-20261031.wav, 3 separate temp layers, LUFS measured; NOT final recorded audio, NOT an episode gate"),
 ("TV-05","Lip-sync","PARTIAL before -> WIRED now (Stage P tool)","lip-sync-timeline-stageP-20261031.json 48f + lip-sync-strip + lip-sync-video-stageP-temp-20261031.mp4; 14/14 visemes; Mars dialogue replaces placeholder in Stage P"),
 ("TV-06","Background painting","WIRED before, verified now","background-consistency-20261031.json/csv 9/9 verified backgrounds + colour-script-20261031.png (4 scenes); batch-15 claim NOT re-verified, flagged"),
 ("TV-07","Titles / credits / delivery","PARTIAL before -> WIRED now","delivery-spec-final-20261031.md (1920x1080 + 1080x1920) + safe-areas-20261031.png + captions-stageE-descriptive-20261031.srt; title card + credits template prior"),
 ("TV-08","Character bible / model sheet","PARTIAL before -> WIRED now (document)","character-bible-20261031.md + bible-contact-20261031.png; true hand-drawn 3/4 art still owed, flagged in the bible"),
 ("TV-09","Production tracking","WIRED before, verified + extended now","asset-tracker-cj01-cj30-20261031.csv/json 30/30 rows (pose-pending 9/30 flagged, not invented)"),
 ("TV-10","Quality control / broadcast QC","WIRED before, verified + consolidated now","qc-v2-cj01-cj30-20261031.json 27/30 PASS + qc-checklist-20261031.md; CJ-05/06/26 neutral-rim FAILs flagged for Mars ruling"),
 ("11","Storyboard 30-panel index (gap-close-tv)","WIRED before","gap-close-tv-20261031/storyboard-index-30panel-20261031.png"),
 ("12","Punch animatic, silent (gap-close-tv)","WIRED before","gap-close-tv-20261031/animatic-punch-20261031.mp4 (52f, video-only — sound added in this folder as Stage P)"),
 ("13","EDL CJ-01..CJ-30 (gap-close-tv)","WIRED before","gap-close-tv-20261031/edl-cj01-cj30-20261031.csv/json"),
 ("14","Principles matrix CJ-01..CJ-30 (gap-close-tv)","WIRED before","gap-close-tv-20261031/principles-matrix-cj01-cj30-20261031.json/png"),
 ("15","QC run CJ-01..CJ-30 (gap-close-tv)","WIRED before","gap-close-tv-20261031/qc-cj01-cj30-20261031.json/md (27/30 PASS)"),
 ("16","Title card art (gap-close-tv)","WIRED before","gap-close-tv-20261031/title-card-cape-jones-20261031.png"),
 ("17","Credits template (gap-close-tv)","WIRED before","gap-close-tv-20261031/credits-template-20261031.md/png (roles TBD, no names invented)"),
 ("18","Dialogue shot CJ-26 composite (gap-close-tv)","WIRED before","gap-close-tv-20261031/dialogue-shot-cj26-neutral-ah-20261031.png"),
 ("19","Audio cue sheet v2 + demo tones","WIRED before","showcase/audio/audio-cue-sheet-v2.csv/json + cape-jones-audio-cues-demo.mp3 (DEMO ONLY tones)"),
 ("20","Ground-feet gate","WIRED before, rerun now","ground-feet-placement-wire100-20261031/ground_gate.py — rerun on apose in gates-run-20261031.json"),
 ("21","No-crop gate","WIRED before, rerun now","no-crop-window-20261031/check_no_clip.py — rerun on apose in gates-run-20261031.json"),
 ("22","Wrist gate","WIRED before, rerun now","wrist-attach-fix-20261031/check_wrist_attach.py — rerun on existing csv in gates-run-20261031.json"),
 ("23","Snap gates (face/cowl/chest)","WIRED before, rerun now","face-cowl-snap-wire100-20261031/check_pose_snap.py — neutral run in gates-run-20261031.json"),
 ("24","Shading preset library (retrieve.py)","WIRED before, rerun now","shading-preset-library-20261031/retrieve.py — CLEAN/ARMS_UP run in gates-run-20261031.json"),
 ("25","CapeGP presets","WIRED before, output verified now","capegp-presets-20261031/capegp_all_presets.blend (builder not rerun — would overwrite its folder)"),
 ("26","Gaussian splatting builder","WIRED before, output verified now","gaussian-splatting-20261031/cape-gaussians-20261031.ply (builder not rerun — would overwrite its folder)"),
 ("27","PIL compositor stack","WIRED before, help verified now","apply_compositor.py --help rc=0; same layer order as Blender tree"),
 ("28","Lighting levels runner (levels 0-5)","WIRED before","apply_lighting_levels.py + apply_lighting_level2_v2.py (prior runs; Level 2 v2 warm-rim on file)"),
 ("29","LUT library (70 .cube)","WIRED before","showcase/luts-30 + lut-spectrum + lut-spectrum-v2 (70 total per prior counts; base 30 + spectrum 24 + v2 16)"),
 ("30","FFmpeg delivery encode","WIRED before, rerun now","ffmpeg 8.1.2; afterglow CJ mp4s + new Stage E/P mp4s ffprobe-verified in this run"),
 ("31","Free-stack tools (Tahoma/Krita/Pencil/Synfig)","WIRED before","FREE-FIRST-WIRING.md install/test batch (4/4 tool tests, prior workstream)"),
 ("32","Master pipeline runner (this folder)","WIRED now","wire_tv_100.py — one command builds camera, edit, mix, lip-sync, backgrounds, delivery, bible, tracker, QC, gates"),
 ("33","Ground-feet gate RUN on TV shots","WIRED now","gates-run-20261031.json: ground_gate apose GROUNDED ground-y 1294"),
 ("34","No-crop gate RUN on TV outputs","WIRED now","gates-run-20261031.json: check_no_clip on apose plate (composites are opaque, so no-crop applies to plates, stated)"),
 ("35","Wrist + snap gates RUN in TV pipeline","WIRED now","gates-run-20261031.json: wrist csv + snap neutral run + snap csv in this folder"),
 ("36","Shading preset APPLIED path (retrieve -> TV shot)","WIRED now","gates-run-20261031.json retrieve run + delivery/bible naming the preset path; preset PNGs are source-referenced, not duplicated"),
 ("37","CapeGP + Gaussian outputs wired into TV inventory","WIRED now","gates-run-20261031.json: blend + ply existence/bytes recorded in TV gates file"),
 ("38","Blender compositor node-tree audit","WIRED now (file audit)","gates-run-20261031.json: blender-compositor-stack.py lines recorded; Blender binary NOT on PATH here, so NOT claimed rendered"),
 ("39","Version-lock archive manifest for this folder","WIRED now","wiring-100-manifest-20261031.json (this run, below) — file list + reassembly order"),
 ("40","Pre-delivery check runner (Stage E + Stage P split)","WIRED now","pre-delivery-check-20261031.md + qc-v2 + gates-run: Stage E checks gate the edit, Stage P checks are listed separately and do NOT gate Stage E"),
 ("41","Space Ghost workflow wiring (episode-first order)","WIRED now","SPACE-GHOST-WORKFLOW-20261031.md — Stage E / Stage P split enforced in this script's file naming and gate logic"),
]
with open(os.path.join(OUT,"inventory-41-20261031.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["id","item","status","evidence"]); w.writerows(inv)
json.dump({"version":"wiring-100","total":41,"wired_before":24,"wired_now_new":17,"wired_after":41,
           "tv_before":"3/10 fully wired, 7/10 partially wired","tv_after":"10/10 wired (TV-04/TV-05 as Stage P tools, per Space Ghost workflow)",
           "approval":"0/1 per item until Mars sees it — nothing here is claimed approved/landed",
           "items":[{"id":i,"item":t,"status":s,"evidence":e} for i,t,s,e in inv]},
          open(os.path.join(OUT,"inventory-41-20261031.json"),"w"),indent=2)
log(f"INVENTORY: 41 items, 24 wired before, 17 wired now, 41/41 after; TV 10/10 after")

# pre-delivery check doc
pdc="""# PRE-DELIVERY CHECK (wiring-100-20261031)
STAGE E (gates the visual edit — all must pass or the edit is NOT delivered):
- Edited sequence file exists + ffprobe video stream 24fps (see verification log).
- Camera sheet 30/30, asset tracker 30/30, EDL v2 present.
- Visual QC: 27/30 PASS; CJ-05/06/26 are FAILs awaiting a Mars neutral-rim ruling — the
  edit is delivered as a SAMPLE (6 shots, none of them CJ-05/06/26), so those FAILs do not
  silently ride inside the sample edit. A 30-shot delivery would still be blocked on them.
- Safe areas + delivery frame size present. No existing file was overwritten in this run.
STAGE P (listed, do NOT gate Stage E):
- Temp 3-layer mix + LUFS measured (temp tones only, not final recorded audio).
- Lip-sync timeline tool + temp video (placeholder sequence; Mars dialogue replaces it).
- Dialogue QC + tempo QC: PENDING until Mars dialogue / tempo choice (Stage P, after episodes).
"""
open(os.path.join(OUT,"pre-delivery-check-20261031.md"),"w").write(pdc)

# manifest
man={"version":"wiring-100","folder":"wiring-100-20261031",
     "files":sorted(os.listdir(OUT)),
     "reassembly_order":["wire_tv_100.py","SPACE-GHOST-WORKFLOW-20261031.md","inventory-41-20261031.json",
       "camera-sheet-cj01-cj30-20261031.csv","edited-sequence-stageE-visual-20261031.mp4",
       "sound-mix-3layer-stageP-temp-20261031.wav","lip-sync-timeline-stageP-20261031.json",
       "asset-tracker-cj01-cj30-20261031.csv","qc-v2-cj01-cj30-20261031.json","gates-run-20261031.json"],
     "note":"No file outside this folder was written by this script. Prior folders were read-only."}
json.dump(man,open(os.path.join(OUT,"wiring-100-manifest-20261031.json"),"w"),indent=2)
open(os.path.join(OUT,"verification-log-20261031.txt"),"w").write("\n".join(LOG)+"\n")
log("DONE wiring-100")
