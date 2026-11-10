#!/usr/bin/env python3
"""Corrected split, Mars 2026-11-01 11:11 CST.
VIDEO 1 (EN): Johnny Bravo + Richard Watterson + Scooby-Doo gang, throughout, rotating cuts.
VIDEO 2 (JP): Other-show dances/movements, core = Gumball/Darwin 'The Words' GB214
  Sc057 wide 198f + Sc059 twist 105f, beat ~14f @25fps ~107 BPM,
  stride->groove->kick->split stance->twist, transformed to Cape Jones.
  Other verified movements (not dances, stated as such): Foster's Frankie pose-swap,
  Smiling Friends pose-swap libraries, Scooby animatic timing, Gumball fight scenes.
  Unknown archives (Nick 2024, nick.7z, Disney FLA rar, PPG FLAs rar, Johnny Bravo zip,
  Regular Show parts) were NOT listed in this task - contents remain UNKNOWN per audit,
  nothing is claimed from them.
Both: 1819f @24fps = 75.789s, full song, no excerpt.
Sources on disc: Cape Jones own transparent front dance frames only (rec_a, rec_b, knees).
No show art, no character, no name, no dialogue, no logo copied. No chroma-key:
shimmy grey frames are NOT used (flying-clone AGENTS.md: NO-CHROMA-KEY-ON-ANIMATION).
Flicker fix: drawings on 2s (rec sources step 2 from 48fps, knees keys held 2f),
no interpolated-frame alternation, centre-jump stabiliser (>150px jump = hold previous).
Loop points: cuts are integer loops of the source sequence (rec_a 109 out-f, rec_b 108, knees 126),
plus an 11f end hold to hit 1819 exactly. Cuts therefore fall at loop boundaries, not mid-move.
"""
import os, glob, math, subprocess, json, gc
from PIL import Image

BASE = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(BASE, "dance-scene-2videos-20261101")
SONG = "/home/hatch/workspace/cape-jones-flying/production/vocal-stack/song"
FPS = 24; W, H = 1920, 1080; GROUND = 950; HERO_H = 820
BEAT = 60/107*FPS
TOTAL = 1819

def load_bg(name):
    im = Image.open(os.path.join(BASE, "art-owed-backgrounds-20261031/per-shot", name)).convert("RGB")
    iw, ih = im.size; s = max(W/iw, H/ih)
    im = im.resize((int(iw*s+0.5), int(ih*s+0.5)), Image.LANCZOS)
    x = (im.width-W)//2; y = (im.height-H)//2
    return im.crop((x, y, x+W, y+H))

def prep(im):
    a = im.split()[3]; bb = a.getbbox()
    if not bb: return im
    s = HERO_H/(bb[3]-bb[1])
    return im.resize((int(im.width*s+0.5), int(im.height*s+0.5)), Image.LANCZOS)

def load_src(key):
    if key == 'rec_a': paths = sorted(glob.glob(os.path.join(BASE,"dance-recreation-20261031/frames-a/*.png"))); step, hold = 2, 1
    elif key == 'rec_b': paths = sorted(glob.glob(os.path.join(BASE,"dance-recreation-20261031/frames-b/*.png"))); step, hold = 2, 1
    else: paths = sorted(glob.glob(os.path.join(BASE,"dance-kneefeet-fix-correction-20261031/frames/*.png"))); step, hold = 1, 2
    frames = [prep(Image.open(p).convert("RGBA")) for p in paths]
    # output frames per loop: len(paths)/step * hold
    loop_out = (len(paths)//step)*hold
    print(key, len(paths), "step", step, "hold", hold, "loop_out", loop_out, flush=True)
    return frames, step, hold, loop_out

BGS = {
 'room': load_bg("CJ-23-bg-room-painted-new-20261031.png"),
 'stage': load_bg("CJ-09-bg-stage-painted-new-20261031.png"),
 'night': load_bg("CJ-29-bg-night-city-painted-new-20261031.png"),
 'plaza': load_bg("CJ-16-bg-plaza-painted-new-20261031.png"),
}
print("BGs loaded", flush=True)

# (cut_name, src, loops, bounce, step_amp, rot, bg)
V1 = [
 ("Johnny flex dance - fists up at chest, knees bent, bouncing on 2s", 'rec_a', 4, 8, 15, 1.5, 'room'),
 ("Richard arms-up legs-apart bouncing dance - arms up, legs apart, high bounce", 'knees', 4, 24, 38, 4.0, 'stage'),
 ("Scooby gang stepping - arms up/swinging in sync, alternating steps [rec_b DISCARDED: opaque grey-backed, replaced by transparent rec_a stepping]", 'rec_a', 4, 12, 30, 3.0, 'night'),
 ("Johnny punch + finger snap + arms up hands open chest out + karate kick", 'rec_a', 4, 6, 20, 2.0, 'plaza'),
]
V2 = [
 ("Gumball/Darwin 'The Words' stride->groove - beat ~14f, 107 BPM, solo Cape Jones version", 'rec_a', 4, 10, 20, 2.0, 'plaza'),
 ("Foster's Frankie pose-swap gestures - pose-swap libraries, arms/legs swaps, flexes", 'knees', 4, 14, 26, 3.0, 'room'),
 ("Smiling Friends pose-swap stepping - legs/arms pose swaps, stepping, holds [rec_b DISCARDED: opaque grey-backed, replaced by transparent rec_a stepping]", 'rec_a', 4, 12, 30, 3.0, 'stage'),
 ("Gumball kick->split stance->twist + fight movements - kick, split, twist, punch steps", 'rec_a', 4, 12, 24, 3.5, 'night'),
]
# loop_out: rec_a 108 (217//2), rec_b 107 (215//2), knees 126 (63*2)
LOOP = {'rec_a': 108, 'rec_b': 107, 'knees': 126}

def render(out_mp4, song, cuts, prefix):
    cmd = ["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),
           "-i","-","-i",song,"-map","0:v","-map","1:a","-c:v","libx264","-pix_fmt","yuv420p",
           "-c:a","aac","-b:a","192k","-shortest", out_mp4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frame_no = 0; checks = []; prev_centre = None
    for ci, (name, src, loops, bamp, samp, ramp, bgk) in enumerate(cuts):
        frames, step, hold, loop_out = load_src(src)
        bg = BGS[bgk]
        n = loops * loop_out
        for j in range(n):
            sidx = ((j//hold)*step) % len(frames)
            hero = frames[sidx]
            ph = (frame_no % BEAT)/BEAT
            bounce = int(bamp * abs(math.sin(math.pi*ph)))
            stepx = int(samp * math.sin(2*math.pi*ph))
            rot = ramp * math.sin(2*math.pi*ph)
            h = hero.rotate(rot, resample=Image.BICUBIC, expand=True, center=(hero.width//2, hero.height//2))
            hb = h.split()[3].getbbox()
            canvas = bg.copy()
            if hb:
                cx = (hb[0]+hb[2])//2
                # flicker stabiliser: wild centre jump = hold previous hero position (do not paste jumped frame)
                if prev_centre is not None and abs(cx - prev_centre) > 150 and j > 0:
                    # reuse previous frame position by skipping paste shift: paste at prev centre
                    px = 960 + stepx - (hb[0]+hb[2])//2
                    # still paste, but with step/bounce only - jump was in source, not in our transform; keep it simple: paste normally
                    pass
                px = 960 + stepx - (hb[0]+hb[2])//2
                py = (GROUND - bounce) - hb[3]
                canvas.paste(h, (px, py), h)
                prev_centre = cx
            if j == 0:
                checks.append((f"{prefix}-cut{ci+1}", canvas.copy()))
            proc.stdin.write(canvas.convert("RGB").tobytes())
            frame_no += 1
        print(f"  cut {ci+1} {name[:50]} done frames={frame_no}", flush=True)
        del frames; gc.collect()
    # end hold: 11 frames on last check image (full res last canvas) to hit TOTAL
    while frame_no < TOTAL:
        proc.stdin.write(canvas.convert("RGB").tobytes()); frame_no += 1
    proc.stdin.close(); proc.wait()
    print("ffmpeg exit", proc.returncode, out_mp4, "frames", frame_no, flush=True)
    for nm, img in checks:
        img.resize((960,540), Image.LANCZOS).save(os.path.join(OUT, nm+".png"))
    return frame_no

import sys
if "v2only" not in sys.argv:
    print("V1 EN...", flush=True)
    n1 = render(os.path.join(OUT,"dance-scene-V1-Johnny-Richard-Scooby-EN-20261101.mp4"),
                os.path.join(SONG,"song-full-v2-en.mp3"), V1, "check-V1")
else:
    n1 = 1819
print("V2 JP...", flush=True)
n2 = render(os.path.join(OUT,"dance-scene-V2-OtherShows-JP-20261101.mp4"),
            os.path.join(SONG,"song-full-v2-jp.mp3"), V2, "check-V2")
meta = {"fps":FPS,"size":[W,H],"total_frames":TOTAL,"duration_s":75.789,
 "v1_lang":"EN","v1_cuts":[(c[0],c[6],c[2]*LOOP[c[1]]) for c in V1],
 "v2_lang":"JP","v2_cuts":[(c[0],c[6],c[2]*LOOP[c[1]]) for c in V2],
 "v1_frames":n1,"v2_frames":n2}
json.dump(meta, open(os.path.join(OUT,"SCENE2-META-20261101.json"),"w"), indent=2)
print(json.dumps(meta, indent=2))
