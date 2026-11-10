#!/usr/bin/env python3
"""Build movement-library clips: Cape Jones only, transform only.
Sources are existing Cape Jones rig videos on disc (no show art, no show audio).
Audio is synthesized original SFX (numpy), NOT show music, NOT show SFX.
"""
import os, subprocess, wave, numpy as np, json, shutil
SRC = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(SRC, "movement-library-clips-20261101")
os.makedirs(OUT, exist_ok=True)
SR = 44100

def thump(dur, freq=70, amp=0.7):
    t = np.arange(int(SR*dur))/SR
    return amp*np.sin(2*np.pi*freq*t)*np.exp(-t*18)
def blip(dur, freq=180, amp=0.5):
    t = np.arange(int(SR*dur))/SR
    return amp*np.sin(2*np.pi*freq*t)*np.exp(-t*12)
def sweep(dur, f0=400, f1=1400, amp=0.4):
    t = np.arange(int(SR*dur))/SR
    f = f0+(f1-f0)*t/dur
    ph = 2*np.pi*np.cumsum(f)/SR
    return amp*np.sin(ph)*np.sin(np.pi*t/dur)**2
def snap(dur=0.04, amp=0.6):
    n = np.random.default_rng(7).normal(0,1,int(SR*dur))
    t = np.arange(len(n))/SR
    return amp*n*np.exp(-t*90)
def make_wav(path, dur, events):
    """events: list of (time, kind) kind in thump,blip,sweep,snap"""
    buf = np.zeros(int(SR*dur))
    for t0, kind in events:
        if kind=="thump": s=thump(0.12)
        elif kind=="blip": s=blip(0.12,180)
        elif kind=="sweep": s=sweep(0.25)
        elif kind=="snap": s=snap()
        elif kind=="impact": s=thump(0.18,55,0.9)
        else: continue
        i=int(t0*SR); j=min(len(buf), i+len(s)); buf[i:j]+=s[:j-i]
    m=np.max(np.abs(buf)) or 1
    buf=buf/m*0.85
    with wave.open(path,"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((buf*32767).astype(np.int16).tobytes())

CLIPS = [
 # id, source, duration, sound events, description
 ("01-gumball-dance-strut-twist", f"{SRC}/dance-recreation-20261031/dance-recreation-main-20261031.mp4", 4.52,
  [(t,"thump") for t in [0.0,0.56,1.12,1.68,2.24,2.80,3.36,3.92]]+[(t,"blip") for t in [0.28,0.84,1.40,1.96,2.52,3.08,3.64,4.20]],
  "Gumball Darwin dance timing, Cape Jones version"),
 ("02-gumball-fight-kick", f"{SRC}/dance-improved-20261031/dance-improved-20261031.mp4", 5.04,
  [(t,"thump") for t in [0.0,1.0,2.0,3.0,4.0]]+[(1.75,"sweep"),(1.95,"impact")],
  "Gumball fight timing, kick segment, Cape Jones version"),
 ("03-fosters-pose-swap-gesture", f"{SRC}/rig-chains-20261031/chain-punch-20261031.mp4", 3.12,
  [(0.5,"sweep"),(1.0,"impact"),(1.5,"snap"),(2.0,"sweep"),(2.5,"impact")],
  "Fosters pose-swap / gesture timing, Cape Jones version"),
 ("04-smiling-friends-pose-swap-head", f"{SRC}/rig-chains-20261031/successor-pose-dialects-20261031.mp4", 5.58,
  [(t,"snap") for t in [0.5,1.5,2.5,3.5,4.5]]+[(t,"blip") for t in [1.0,2.0,3.0,4.0,5.0]],
  "Smiling Friends frame-addressed swap libraries, Cape Jones version"),
 ("05-scooby-song-step", f"{SRC}/rig-chains-20261031/chain-dance-20261031.mp4", 3.88,
  [(t,"thump") for t in [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5]]+[(t,"blip") for t in [0.25,0.75,1.25,1.75,2.25,2.75,3.25]],
  "Scooby 607 song animatic step timing, Cape Jones version"),
 ("06-nick-baked-cache-walk", f"{SRC}/rig-chains-20261031/chain-walk-20261031.mp4", 2.79,
  [(t,"thump") for t in [0.0,0.35,0.70,1.05,1.40,1.75,2.10,2.45]],
  "Nick Maya/Alembic baked-cache walk timing, Cape Jones version"),
 ("07-johnny-bravo-flex-dance", f"{SRC}/rig-chains-20261031/chain-flex-fight-20261031.mp4", 3.12,
  [(t,"blip") for t in [0.0,0.5,1.0,1.5,2.0,2.5,3.0]]+[(0.8,"snap"),(2.2,"snap")],
  "Johnny Bravo flex/dance, Cape Jones version"),
 ("08-richard-scooby-gang-step", f"{SRC}/dance-recreation-20261031/dance-recreation-combine-20261031.mp4", 4.48,
  [(t,"thump") for t in [0.0,0.56,1.12,1.68,2.24,2.80,3.36,3.92]]+[(t,"blip") for t in [0.28,0.84,1.40,1.96,2.52,3.08,3.64]],
  "Richard arms-up + Scooby gang stepping, Cape Jones version"),
]
results=[]
for cid, src, dur, events, desc in CLIPS:
    wav=os.path.join(OUT, cid+".wav")
    mp4=os.path.join(OUT, cid+".mp4")
    gif=os.path.join(OUT, cid+".gif")
    make_wav(wav, dur, events)
    # mux: re-encode video yuv420p, audio aac, shortest, faststart
    subprocess.run(["ffmpeg","-y","-v","error","-i",src,"-i",wav,
        "-map","0:v:0","-map","1:a:0","-c:v","libx264","-pix_fmt","yuv420p",
        "-c:a","aac","-shortest","-movflags","+faststart",mp4], check=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",mp4,"-vf","fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse",gif], check=True)
    sz=os.path.getsize(mp4)
    results.append(dict(id=cid, source=os.path.relpath(src, SRC), duration=dur, mp4_bytes=sz, sound=desc))
    print(cid, sz)
json.dump(results, open(os.path.join(OUT,"CLIPS-20261101.json"),"w"), indent=2)
print("done", len(results))
