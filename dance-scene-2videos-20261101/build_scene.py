#!/usr/bin/env python3
"""2D dance scene, EN + JP, different dances per cut.
Sources: Cape Jones own front dance frames only. No show art, no hand-draw,
no piece cutting. Whole-figure transforms only: bounce, lateral step, sway rotation.
Song: repo Cape Jones Dance v2, 152 BPM. Visual grid: ~107 BPM (13.46f/beat @24fps).
Tempo mismatch stated in report, NOT silently stretched: audio is native 152 BPM,
visual stays 107 BPM, so beats do NOT land beat-for-beat.
"""
import os, glob, math, subprocess, json
from PIL import Image

BASE = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(BASE, "dance-scene-2videos-20261101")
SONG = "/home/hatch/workspace/cape-jones-flying/production/vocal-stack/song"
FPS = 24
W, H = 1920, 1080
GROUND = 950
HERO_H = 820
BEAT = 60/107*FPS  # 13.46 frames

def load_bg(name):
    im = Image.open(os.path.join(BASE, "art-owed-backgrounds-20261031/per-shot", name)).convert("RGB")
    # crop/resize to 1920x1080 centre
    iw, ih = im.size
    scale = max(W/iw, H/ih)
    im = im.resize((int(iw*scale+0.5), int(ih*scale+0.5)), Image.LANCZOS)
    x = (im.width-W)//2; y = (im.height-H)//2
    return im.crop((x, y, x+W, y+H))

def load_transparent(paths, key_grey=False):
    out = []
    for p in paths:
        im = Image.open(p).convert("RGBA")
        if key_grey:
            # exact flat grey (128,128,128) -> transparent, no other pixels touched
            px = im.load()
            # use numpy-free loop via alpha mask: build mask from colour
            import collections
            data = im.getdata()
            new = []
            for r,g,b,a in data:
                if r==128 and g==128 and b==128:
                    new.append((r,g,b,0))
                else:
                    new.append((r,g,b,a))
            im.putdata(new)
        out.append(im)
    return out

def hero_bbox(im):
    a = im.split()[3]
    return a.getbbox()

def prep_hero(im):
    """Scale so hero bbox height = HERO_H, return scaled image + bbox."""
    bb = hero_bbox(im)
    if not bb: return im, (0,0,0,0)
    h = bb[3]-bb[1]
    s = HERO_H/h
    nw, nh = int(im.width*s+0.5), int(im.height*s+0.5)
    im2 = im.resize((nw, nh), Image.LANCZOS)
    return im2, hero_bbox(im2)

SOURCE_PATHS = {
 'rec_a': (sorted(glob.glob(os.path.join(BASE,"dance-recreation-20261031/frames-a/*.png"))), False),
 'rec_b': (sorted(glob.glob(os.path.join(BASE,"dance-recreation-20261031/frames-b/*.png"))), False),
 'knees': (sorted(glob.glob(os.path.join(BASE,"dance-kneefeet-fix-correction-20261031/frames/*.png"))), False),
 'shimmy': (sorted(glob.glob(os.path.join(OUT,"frames-shimmy/*.png"))), True),
}
_PREP_CACHE = {}
def get_prep(key):
    if key in _PREP_CACHE:
        return _PREP_CACHE[key]
    _PREP_CACHE.clear()
    import gc; gc.collect()
    paths, kg = SOURCE_PATHS[key]
    frames = load_transparent(paths, key_grey=kg)
    prep = [prep_hero(f) for f in frames]
    print(key, len(frames), "first bbox", prep[0][1], flush=True)
    _PREP_CACHE[key] = prep
    return prep

BGS = {
 'room': load_bg("CJ-23-bg-room-painted-new-20261031.png"),
 'stage': load_bg("CJ-09-bg-stage-painted-new-20261031.png"),
 'night': load_bg("CJ-29-bg-night-city-painted-new-20261031.png"),
 'plaza': load_bg("CJ-16-bg-plaza-painted-new-20261031.png"),
}
print("BGs loaded")

# cuts: (dance_name, source_key, source_step, bounce_amp, step_amp, rot_amp_deg, bg_key)
EN_CUTS = [
 ("Johnny Bravo swagger - chest out, hip sway, arm flex, slow strut", 'rec_a', 2, 8, 15, 1.5, 'room'),
 ("Richard Watterson goofy bounce - loose arms, big steps, high bounce", 'knees', 1, 24, 38, 4.0, 'stage'),
 ("Scooby gang stepping - Shaggy/Freddy style, alternating steps, arm swings", 'rec_b', 2, 12, 30, 3.0, 'night'),
 ("Ghoul Shuffle + Shimmy Number One - squat, shuffle, three-quarter turn, forward face", 'shimmy', 1, 14, 20, 2.0, 'plaza'),
]
JP_CUTS = [
 ("Scooby gang stepping - Shaggy/Freddy style, alternating steps, arm swings", 'rec_b', 2, 12, 30, 3.0, 'night'),
 ("Ghoul Shuffle + Shimmy Number One - squat, shuffle, three-quarter turn, forward face", 'shimmy', 1, 14, 20, 2.0, 'plaza'),
 ("Johnny Bravo swagger - chest out, hip sway, arm flex, slow strut", 'rec_a', 2, 8, 15, 1.5, 'stage'),
 ("Richard Watterson goofy bounce - loose arms, big steps, high bounce", 'knees', 1, 24, 38, 4.0, 'room'),
]
TOTAL_FRAMES = 1819  # 75.789s @24fps

def render(video_path, song_path, cuts, checks_prefix):
    per_cut = TOTAL_FRAMES // len(cuts)
    cut_frames = [per_cut]*len(cuts)
    cut_frames[-1] += TOTAL_FRAMES - sum(cut_frames)
    cmd = ["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),
           "-i","-","-i",song_path,"-map","0:v","-map","1:a","-c:v","libx264","-pix_fmt","yuv420p",
           "-c:a","aac","-b:a","192k","-shortest", video_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frame_no = 0
    checks = []
    for ci, (dance, src, step, bamp, samp, ramp, bgk) in enumerate(cuts):
        bg = BGS[bgk]
        frames = get_prep(src)
        for j in range(cut_frames[ci]):
            # source index: step through source, looped; on 2s for 48fps sources (step=2)
            sidx = (j*step) % len(frames)
            hero, bb = frames[sidx]
            # beat phase
            ph = (frame_no % BEAT) / BEAT
            bounce = int(bamp * abs(math.sin(math.pi*ph)))  # 0..amp, per beat
            stepx = int(samp * math.sin(2*math.pi*ph)) if 'Scooby' in dance or 'Richard' in dance else int(samp*0.5*math.sin(2*math.pi*ph))
            rot = ramp * math.sin(2*math.pi*ph)
            h = hero.rotate(rot, resample=Image.BICUBIC, expand=True, center=(hero.width//2, hero.height//2))
            # paste: hero bbox bottom at GROUND-bounce, centre x 960+stepx
            # bbox of rotated hero: recompute
            hb = h.split()[3].getbbox()
            if hb is None:
                canvas = bg.copy()
            else:
                canvas = bg.copy()
                # align: original hero bbox bottom was at ... use rotated bbox bottom
                px = 960 + stepx - (hb[0]+hb[2])//2
                py = (GROUND - bounce) - hb[3]
                canvas.paste(h, (px, py), h)
            if j == 0:
                checks.append((f"{checks_prefix}-cut{ci+1}", canvas.copy()))
            proc.stdin.write(canvas.convert("RGB").tobytes())
            frame_no += 1
        print(f"  cut {ci+1} {dance[:40]}... done, frames so far {frame_no}")
    proc.stdin.close(); proc.wait()
    print("ffmpeg exit", proc.returncode, video_path)
    for name, img in checks:
        img.resize((960,540), Image.LANCZOS).save(os.path.join(OUT, name+".png"))
    return cut_frames

os.makedirs(OUT, exist_ok=True)
print("EN...")
en_cuts = render(os.path.join(OUT,"dance-scene-EN-20261101.mp4"),
                 os.path.join(SONG,"song-full-v2-en.mp3"), EN_CUTS, "check-EN")
print("JP...")
jp_cuts = render(os.path.join(OUT,"dance-scene-JP-20261101.mp4"),
                 os.path.join(SONG,"song-full-v2-jp.mp3"), JP_CUTS, "check-JP")
meta = {"fps":FPS,"size":[W,H],"total_frames":TOTAL_FRAMES,"duration_s":75.789,
        "en_cuts":[(c[0],c[6]) for c in EN_CUTS],"jp_cuts":[(c[0],c[6]) for c in JP_CUTS],
        "en_cut_frames":en_cuts,"jp_cut_frames":jp_cuts,
        "sources":{k:len(v[0]) for k,v in SOURCE_PATHS.items()}}
json.dump(meta, open(os.path.join(OUT,"SCENE-META-20261101.json"),"w"), indent=2)
print(json.dumps(meta, indent=2))
