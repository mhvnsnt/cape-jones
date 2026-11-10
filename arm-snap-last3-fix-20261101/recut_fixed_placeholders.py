#!/usr/bin/env python3
"""Re-cut placeholders A and C from the snap-fixed successor, same timing/banner/sound.
A: stand (first frame of snapped transform) + transform segments
   successor 0-1.0, 1.5-2.5, 3.0-4.0, 4.5-5.58, banner every frame,
   original A wav (snaps 1/2/3/4 + blips), faststart.
C: stand (first frame of snapped successor 0-4.0) + that 4.0s move, banner,
   original C wav (snaps 1/2/3/4 + blips), faststart.
Originals untouched. Outputs are new dated files in this folder.
"""
import os, subprocess
SRC = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(SRC, "arm-snap-last3-fix-20261101")
WORK = os.path.join(OUT, "work"); os.makedirs(WORK, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BANNER = "TEMPLATE-PLACEHOLDER - NOT FINAL - DO NOT SHIP"
SNAP = os.path.join(OUT, "successor-pose-dialects-ARM-SNAP-FIXED-20261101.mp4")
def run(cmd): subprocess.run(cmd, check=True)
def bannered(move_mp4, wav, out_mp4):
    run(["ffmpeg","-y","-v","error","-i",move_mp4,"-vf","select=eq(n\\,0)","-vframes","1",f"{WORK}/first.png"])
    run(["ffmpeg","-y","-v","error","-loop","1","-i",f"{WORK}/first.png","-t","1",
         "-vf",f"scale=1100:750,drawtext=fontfile={FONT}:text='{BANNER}':fontsize=26:fontcolor=white:box=1:boxcolor=black@0.7:x=(w-text_w)/2:y=10",
         "-c:v","libx264","-pix_fmt","yuv420p","-r","24",f"{WORK}/stand.mp4"])
    run(["ffmpeg","-y","-v","error","-i",move_mp4,"-vf",
         f"drawtext=fontfile={FONT}:text='{BANNER}':fontsize=26:fontcolor=white:box=1:boxcolor=black@0.7:x=(w-text_w)/2:y=10",
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

# A transform, same segments as honest-audit build_corrected
segs = [(0,1.0),(1.5,2.5),(3.0,4.0),(4.5,5.58)]
parts = []
for i,(a,b) in enumerate(segs):
    p = f"{WORK}/sf-seg{i}.mp4"
    run(["ffmpeg","-y","-v","error","-ss",str(a),"-to",str(b),"-i",SNAP,"-c:v","libx264","-pix_fmt","yuv420p","-an",p]); parts.append(p)
with open(f"{WORK}/sf-concat.txt","w") as f:
    for p in parts: f.write(f"file '{p}'\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{WORK}/sf-concat.txt","-c:v","libx264","-pix_fmt","yuv420p",f"{WORK}/sf-video.mp4"])
bannered(f"{WORK}/sf-video.mp4",
         f"{SRC}/template-placeholder-20261101/TEMPLATE-PLACEHOLDER-A-SMILING-STRUCTURE-20261101.wav",
         f"{OUT}/TEMPLATE-PLACEHOLDER-A-SMILING-STRUCTURE-ARM-SNAP-FIXED-20261101.mp4")
# C move, same as original: first 4.0s of successor
run(["ffmpeg","-y","-v","error","-ss","0","-to","4.0","-i",SNAP,"-c:v","libx264","-pix_fmt","yuv420p","-an",f"{WORK}/pim-move.mp4"])
bannered(f"{WORK}/pim-move.mp4",
         f"{SRC}/template-placeholder-20261101/TEMPLATE-PLACEHOLDER-C-SMILING-5LAYER-STRUCTURE-20261101.wav",
         f"{OUT}/TEMPLATE-PLACEHOLDER-C-SMILING-5LAYER-ARM-SNAP-FIXED-20261101.mp4")
print("recut A + C fixed")
