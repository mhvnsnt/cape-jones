#!/usr/bin/env python3
"""Clean re-renders, Mars 2026-11-01 13:55 CST correction.
No banner, no label in filenames. Same segments, timing, sound, snap fix.
Sources are Cape Jones pieces only, arranged to donor timing/structure.
No donor character art in any source."""
import os, subprocess, shutil
SRC = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(SRC, "clean-shippable-animations-20261101")
WORK = os.path.join(OUT, "work"); os.makedirs(WORK, exist_ok=True)
def run(cmd): subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
def clean(move_mp4, wav, out_mp4):
    run(["ffmpeg","-y","-v","error","-i",move_mp4,"-vf","select=eq(n\\,0)","-vframes","1",f"{WORK}/first.png"])
    run(["ffmpeg","-y","-v","error","-loop","1","-i",f"{WORK}/first.png","-t","1",
         "-vf","scale=1100:750","-c:v","libx264","-pix_fmt","yuv420p","-r","24",f"{WORK}/stand.mp4"])
    run(["ffmpeg","-y","-v","error","-i",move_mp4,"-vf","scale=1100:750",
         "-c:v","libx264","-pix_fmt","yuv420p","-an",f"{WORK}/move.mp4"])
    with open(f"{WORK}/concat.txt","w") as f:
        f.write(f"file '{WORK}/stand.mp4'\nfile '{WORK}/move.mp4'\n")
    run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{WORK}/concat.txt",
         "-c:v","libx264","-pix_fmt","yuv420p",f"{WORK}/video.mp4"])
    run(["ffmpeg","-y","-v","error","-i",f"{WORK}/video.mp4","-i",wav,"-map","0:v:0","-map","1:a:0",
         "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest","-movflags","+faststart",out_mp4])
    run(["ffmpeg","-y","-v","error","-i",out_mp4,"-vf",
         "fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse",
         out_mp4.replace(".mp4",".gif")])
    print("built", out_mp4)

# clean wav copies, no label in filename
def wavcopy(src, dst):
    shutil.copyfile(src, dst); return dst
A_WAV = wavcopy(f"{SRC}/template-placeholder-20261101/TEMPLATE-PLACEHOLDER-A-SMILING-STRUCTURE-20261101.wav", f"{OUT}/A-SMILING-STRUCTURE-20261101.wav")
B_WAV = wavcopy(f"{SRC}/template-placeholder-20261101/TEMPLATE-PLACEHOLDER-B-FOSTERS-STRUCTURE-20261101.wav", f"{OUT}/B-FOSTERS-STRUCTURE-20261101.wav")
C_WAV = wavcopy(f"{SRC}/template-placeholder-20261101/TEMPLATE-PLACEHOLDER-C-SMILING-5LAYER-STRUCTURE-20261101.wav", f"{OUT}/C-SMILING-5LAYER-STRUCTURE-20261101.wav")

# A: Smiling 9-layer structure
clean(f"{SRC}/honest-audit-20261101/04-smiling-structure-transform-20261101.mp4", A_WAV,
      f"{OUT}/A-SMILING-STRUCTURE-CLEAN-20261101.mp4")
# B: Foster's punch/walk structure - rebuild move exactly as original
run(["ffmpeg","-y","-v","error","-i",f"{SRC}/honest-audit-20261101/03-fosters-structure-transform-20261101.mp4",
     "-i",f"{SRC}/movement-library-clips-20261101/06-nick-baked-cache-walk.mp4",
     "-filter_complex","[0:v][1:v]concat=n=2:v=1:a=0[outv]","-map","[outv]",
     "-c:v","libx264","-pix_fmt","yuv420p",f"{WORK}/fosters-move.mp4"])
clean(f"{WORK}/fosters-move.mp4", B_WAV, f"{OUT}/B-FOSTERS-STRUCTURE-CLEAN-20261101.mp4")
# C: Smiling 5-layer structure - first 4.0s of original clip
run(["ffmpeg","-y","-v","error","-ss","0","-to","4.0","-i",
     f"{SRC}/movement-library-clips-20261101/04-smiling-friends-pose-swap-head.mp4",
     "-c:v","libx264","-pix_fmt","yuv420p","-an",f"{WORK}/pim-move.mp4"])
clean(f"{WORK}/pim-move.mp4", C_WAV, f"{OUT}/C-SMILING-5LAYER-STRUCTURE-CLEAN-20261101.mp4")
# Arm-snap-fixed A and C: from snap-fixed chain, same segments as arm-snap fix
SNAP = f"{SRC}/arm-snap-last3-fix-20261101/successor-pose-dialects-ARM-SNAP-FIXED-20261101.mp4"
segs = [(0,1.0),(1.5,2.5),(3.0,4.0),(4.5,5.58)]
parts = []
for i,(a,b) in enumerate(segs):
    p = f"{WORK}/sf-seg{i}.mp4"
    run(["ffmpeg","-y","-v","error","-ss",str(a),"-to",str(b),"-i",SNAP,"-c:v","libx264","-pix_fmt","yuv420p","-an",p]); parts.append(p)
with open(f"{WORK}/sf-concat.txt","w") as f:
    for p in parts: f.write(f"file '{p}'\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{WORK}/sf-concat.txt","-c:v","libx264","-pix_fmt","yuv420p",f"{WORK}/sf-video.mp4"])
clean(f"{WORK}/sf-video.mp4", A_WAV, f"{OUT}/A-SMILING-STRUCTURE-ARM-SNAP-FIXED-CLEAN-20261101.mp4")
run(["ffmpeg","-y","-v","error","-ss","0","-to","4.0","-i",SNAP,"-c:v","libx264","-pix_fmt","yuv420p","-an",f"{WORK}/pim-move-fixed.mp4"])
clean(f"{WORK}/pim-move-fixed.mp4", C_WAV, f"{OUT}/C-SMILING-5LAYER-STRUCTURE-ARM-SNAP-FIXED-CLEAN-20261101.mp4")
print("all clean built")
