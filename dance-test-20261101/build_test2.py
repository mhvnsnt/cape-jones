from PIL import Image
import os
SRC="/home/hatch/workspace/cape-jones-rig/dance-recreation-20261031/frames-a"
OUT="/home/hatch/workspace/cape-jones-rig/dance-test-20261101/frames"
W,H=1920,1080; GROUND=950
ENVS=[
 ("room-painted-CJ23", "/home/hatch/workspace/cape-jones-rig/art-owed-backgrounds-20261031/per-shot/CJ-23-bg-room-painted-new-20261031.png"),
 ("stage-painted-CJ09", "/home/hatch/workspace/cape-jones-rig/art-owed-backgrounds-20261031/per-shot/CJ-09-bg-stage-painted-new-20261031.png"),
 ("nightcity-painted-CJ29", "/home/hatch/workspace/cape-jones-rig/art-owed-backgrounds-20261031/per-shot/CJ-29-bg-night-city-painted-new-20261031.png"),
]
BGS=[Image.open(p).convert("RGB").resize((W,H)) for _,p in ENVS]
files=sorted(os.listdir(SRC))
for i,fn in enumerate(files):
    seg=i*3//len(files)
    bg=BGS[seg].copy().convert("RGBA")
    hero=Image.open(os.path.join(SRC,fn)).convert("RGBA").resize((715,975))
    bbox=hero.getchannel("A").getbbox()
    bg.alpha_composite(hero,((W-hero.width)//2, GROUND-bbox[3]))
    bg.convert("RGB").save(os.path.join(OUT,f"test-f{i:03d}.png"))
    if i in (0,72,73,144,145,216):
        bg.convert("RGB").save(f"/home/hatch/workspace/cape-jones-rig/dance-test-20261101/check2-f{i:03d}-{ENVS[seg][0]}.png")
print("done", len(files), [(ENVS[s][0], s*217//3, (s+1)*217//3-1) for s in range(3)])
