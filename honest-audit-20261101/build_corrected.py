#!/usr/bin/env python3
"""Corrected labels + transformed builds, honest provenance.
Sources are ONLY Cape Jones rig videos already on disc. No show art, no show rig,
no show audio, no donor character, no logo, no dialogue. Donor contribution is
STRUCTURE/TIMING described in audits only, mapped in the xsheet below.
"""
import os, subprocess, wave, numpy as np, json
SRC=os.path.expanduser("~/workspace/cape-jones-rig")
OUT=os.path.join(SRC,"honest-audit-20261101")
os.makedirs(OUT,exist_ok=True)
SR=44100
def thump(dur,freq=70,amp=0.7):
    t=np.arange(int(SR*dur))/SR; return amp*np.sin(2*np.pi*freq*t)*np.exp(-t*18)
def blip(dur,freq=180,amp=0.5):
    t=np.arange(int(SR*dur))/SR; return amp*np.sin(2*np.pi*freq*t)*np.exp(-t*12)
def sweep(dur,f0=400,f1=1400,amp=0.4):
    t=np.arange(int(SR*dur))/SR; f=f0+(f1-f0)*t/dur; return amp*np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/dur)**2
def snap(dur=0.04,amp=0.6):
    n=np.random.default_rng(7).normal(0,1,int(SR*dur)); t=np.arange(len(n))/SR; return amp*n*np.exp(-t*90)
def make_wav(path,dur,events):
    buf=np.zeros(int(SR*dur))
    for t0,kind in events:
        s={"thump":thump(0.12),"blip":blip(0.12,180),"sweep":sweep(0.25),"snap":snap(),"impact":thump(0.18,55,0.9)}.get(kind)
        if s is None: continue
        i=int(t0*SR); j=min(len(buf),i+len(s)); buf[i:j]+=s[:j-i]
    m=np.max(np.abs(buf)) or 1; buf=buf/m*0.85
    with wave.open(path,"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf*32767).astype(np.int16).tobytes())
def run(cmd): subprocess.run(cmd,check=True)
# 1. Clip2 corrected: SAME dance-improved visual, NO sweep/impact, dance beat only.
#    This is a relabel, not a kick. True kick remains owed (see report).
wav=f"{OUT}/02-dance-not-kick-corrected-20261101.wav"
make_wav(wav,5.04,[(t,"thump") for t in [0,1,2,3,4]]+[(t,"blip") for t in [0.5,1.5,2.5,3.5,4.5]])
run(["ffmpeg","-y","-v","error","-i",f"{SRC}/dance-improved-20261031/dance-improved-20261031.mp4","-i",wav,"-map","0:v:0","-map","1:a:0","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest","-movflags","+faststart",f"{OUT}/02-dance-not-kick-corrected-20261101.mp4"])
run(["ffmpeg","-y","-v","error","-i",f"{OUT}/02-dance-not-kick-corrected-20261101.mp4","-vf","fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse",f"{OUT}/02-dance-not-kick-corrected-20261101.gif"])
# 2. Smiling structure transform: successor-pose-dialects re-cut on a strict swap grid.
#    Segments are Cape Jones pose-dialect holds, in source order, cut at 0.5s swap points.
#    Donor mapping (structure only): Charlie 9-layer stack -> Cape Jones layer order
#    cape_back, leg_back, leg_front, arm_back, pelvis, torso, neck, head, arm_front (front rig);
#    mouth library 25 (donor) -> 5 Cape Jones mouth pieces (Closed/Open/Shout/Smile/Teeth) - NOT 25, do not claim 25;
#    leg library 10 (donor) -> Cape Jones leg pieces Front/Back/CLEAN/GRAFTED variants, not 10.
src4=f"{SRC}/rig-chains-20261031/successor-pose-dialects-20261031.mp4"
# build segment list: take 0-1.0, 1.5-2.5, 3.0-4.0, 4.5-5.58 in order (swap grid, new edit, not original order/length)
segs=[(0,1.0),(1.5,2.5),(3.0,4.0),(4.5,5.58)]
parts=[]
for i,(a,b) in enumerate(segs):
    p=f"{OUT}/work/sf-seg{i}.mp4"
    run(["ffmpeg","-y","-v","error","-ss",str(a),"-to",str(b),"-i",src4,"-c:v","libx264","-pix_fmt","yuv420p","-an",p]); parts.append(p)
with open(f"{OUT}/work/sf-concat.txt","w") as f:
    for p in parts: f.write(f"file '{p}'\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{OUT}/work/sf-concat.txt","-c:v","libx264","-pix_fmt","yuv420p",f"{OUT}/work/sf-video.mp4"])
wav4=f"{OUT}/04-smiling-structure-transform-20261101.wav"
# swaps at 0,1.0,2.0,3.0 ; total video ~4.08s
make_wav(wav4,4.08,[(t,"snap") for t in [0,1.0,2.0,3.0]]+[(t,"blip") for t in [0.5,1.5,2.5,3.5]])
run(["ffmpeg","-y","-v","error","-i",f"{OUT}/work/sf-video.mp4","-i",wav4,"-map","0:v:0","-map","1:a:0","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest","-movflags","+faststart",f"{OUT}/04-smiling-structure-transform-20261101.mp4"])
run(["ffmpeg","-y","-v","error","-i",f"{OUT}/04-smiling-structure-transform-20261101.mp4","-vf","fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse",f"{OUT}/04-smiling-structure-transform-20261101.gif"])
# 3. Foster structure transform: chain-punch re-cut windup -> snap -> impact hold -> recover
src3=f"{SRC}/rig-chains-20261031/chain-punch-20261031.mp4"
segs3=[(0,1.0),(1.0,2.0),(2.0,3.12)]
parts3=[]
for i,(a,b) in enumerate(segs3):
    p=f"{OUT}/work/fo-seg{i}.mp4"
    run(["ffmpeg","-y","-v","error","-ss",str(a),"-to",str(b),"-i",src3,"-c:v","libx264","-pix_fmt","yuv420p","-an",p]); parts3.append(p)
with open(f"{OUT}/work/fo-concat.txt","w") as f:
    for p in parts3: f.write(f"file '{p}'\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{OUT}/work/fo-concat.txt","-c:v","libx264","-pix_fmt","yuv420p",f"{OUT}/work/fo-video.mp4"])
wav3=f"{OUT}/03-fosters-structure-transform-20261101.wav"
make_wav(wav3,3.12,[(0.5,"sweep"),(1.0,"impact"),(1.5,"snap"),(2.5,"impact")])
run(["ffmpeg","-y","-v","error","-i",f"{OUT}/work/fo-video.mp4","-i",wav3,"-map","0:v:0","-map","1:a:0","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest","-movflags","+faststart",f"{OUT}/03-fosters-structure-transform-20261101.mp4"])
run(["ffmpeg","-y","-v","error","-i",f"{OUT}/03-fosters-structure-transform-20261101.mp4","-vf","fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse",f"{OUT}/03-fosters-structure-transform-20261101.gif"])
print("built")
