"""Animatic 1/1: EDL durations at 24fps, cuts only, total 332 frames = 13.83s.
MP4 1920x1440 @24fps from panels; GIF 960x720 @12fps (half-frame counts, min 1)
from the same panels, same order, same cuts. No dialogue audio in animatic:
dialogue is post-episode per Space Ghost workflow; audio cues are listed in
captions/manifest only, not invented as sound."""
from PIL import Image
import os, json, subprocess, glob
D=os.path.expanduser("~/workspace/cape-jones-rig/storyboards-animatic-20261031")
man=json.load(open(os.path.join(D,"panels-manifest-20261031.json")))
assert len(man)==30, len(man)
frames_dir=os.path.join(D,"animatic","frames"); os.makedirs(frames_dir, exist_ok=True)
total=0; seq=[]
for m in man:
    p=os.path.join(D,"panels",m["panel"]); assert os.path.exists(p), p
    for f in range(m["duration_frames"]):
        total+=1; seq.append((m["shot"], p))
    print(m["shot"], m["duration_frames"], "cum", total)
print("total frames", total); assert total==332, total
# MP4 via ffmpeg concat of panel images repeated: write frames as pngs (downscale? keep 1920x1440)
# To keep runtime sane, write each shot's panel once per frame is 332 PNGs ~ large but ok; use jpg intermediate
jpgdir=os.path.join(D,"animatic","jpg"); os.makedirs(jpgdir, exist_ok=True)
i=0
for shot, p in seq:
    i+=1
    im=Image.open(p).convert("RGB"); im.save(os.path.join(jpgdir, f"f{i:04d}.jpg"), quality=88)
print("jpg frames", i)
subprocess.run(["ffmpeg","-y","-framerate","24","-i",os.path.join(jpgdir,"f%04d.jpg"),
  "-c:v","libx264","-pix_fmt","yuv420p","-r","24",
  os.path.join(D,"animatic","cape-jones-animatic-CJ01-CJ30-20261031.mp4")], check=True)
# GIF @12fps: every other frame (166 frames), 960x720
gif_frames=[]
for j in range(0, len(seq), 2):
    im=Image.open(seq[j][1]).convert("RGB").resize((960,720), Image.LANCZOS)
    gif_frames.append(im)
gif_frames[0].save(os.path.join(D,"animatic","cape-jones-animatic-CJ01-CJ30-20261031.gif"),
  save_all=True, append_images=gif_frames[1:], duration=83, loop=0)
print("gif frames", len(gif_frames))
json.dump({"fps_mp4":24,"fps_gif":12,"total_frames_24fps":total,"total_seconds":round(total/24,3),
 "gif_frames":len(gif_frames),"transition":"cuts only","shots":[(m["shot"],m["duration_frames"]) for m in man]},
 open(os.path.join(D,"animatic","animatic-20261031.json"),"w"), indent=1)
print("animatic done")
