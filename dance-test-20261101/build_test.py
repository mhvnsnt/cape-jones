from PIL import Image, ImageEnhance
import os, json
SRC="/home/hatch/workspace/cape-jones-rig/dance-recreation-20261031/frames-a"
OUT="/home/hatch/workspace/cape-jones-rig/dance-test-20261101/frames"
ENVS=[
 ("room-canonical", "/home/hatch/workspace/cape-jones-rig/canonical-room-20261101.jpg", (255,220,170), 18),
 ("street", "/home/hatch/workspace/cape-jones-rig/showcase/on-background-street.jpg", None, 0),
 ("skyline-night", "/home/hatch/workspace/cape-jones-rig/showcase/on-background-skyline.jpg", (120,160,255), 28),
]
W,H=1920,1080
GROUND=950
files=sorted(os.listdir(SRC))
assert len(files)==217, len(files)
for i,fn in enumerate(files):
    seg=i*len(ENVS)//len(files)
    name,tint_path,tint,alpha=ENVS[seg]
    bg=Image.open(tint_path).convert("RGB").resize((W,H))
    if tint:
        ov=Image.new("RGB",(W,H),tint)
        bg=Image.blend(bg,ov,alpha/255.0)
    hero=Image.open(os.path.join(SRC,fn)).convert("RGBA").resize((715,975))
    # align opaque bbox bottom to GROUND
    bbox=hero.getchannel("A").getbbox()
    # paste centred, bottom at GROUND
    x=(W-hero.width)//2
    y=GROUND-bbox[3]
    canvas=bg.convert("RGBA")
    canvas.alpha_composite(hero,(x,y))
    canvas.convert("RGB").save(os.path.join(OUT,f"test-f{i:03d}.png"))
    if i in (0,71,72,143,144,216):
        canvas.convert("RGB").save(f"/home/hatch/workspace/cape-jones-rig/dance-test-20261101/check-f{i:03d}-{name}.png")
print("frames", len(files))
print(json.dumps([{"segment":n,"frames":f"{a}-{b}"} for n,(_,_,_,_) in []]))
# segment ranges
for s,(n,_,_,_) in enumerate(ENVS):
    a=s*217//3; b=(s+1)*217//3-1
    print(n, a, b)
