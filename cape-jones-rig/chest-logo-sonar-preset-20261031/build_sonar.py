from PIL import Image, ImageDraw
import json, math, os
BASE = "/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png"
OUT = "/home/hatch/workspace/cape-jones-rig/chest-logo-sonar-preset-20261031"
CX, CY = 551, 491
base = Image.open(BASE).convert("RGBA")
W, H = base.size
# Sonar spec: 3 rings, staggered, expanding outward, cyan sonar, separate effect layer
N_FRAMES = 24
FPS = 12
MAX_R = 420
RING_COUNT = 3
COLOUR = (0, 200, 255)
frames = []
for f in range(N_FRAMES):
    # grey display background only for GIF/contact; transparent masters in frames/
    canvas = Image.new("RGBA", (W, H), (128,128,128,255))
    canvas.alpha_composite(base)
    effect = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(effect)
    # emblem pulse dot
    pulse = 0.5 + 0.5*math.sin(2*math.pi*f/N_FRAMES)
    r0 = 14 + 6*pulse
    d.ellipse([CX-r0, CY-r0, CX+r0, CY+r0], fill=(0,200,255,255))
    d.ellipse([CX-6, CY-6, CX+6, CY+6], fill=(255,255,255,255))
    for k in range(RING_COUNT):
        # phase staggered by 1/3 cycle
        t = ((f / N_FRAMES) + k/RING_COUNT) % 1.0
        r = 30 + t*(MAX_R-30)
        alpha = int(255*(1-t)**1.5)
        width = 6 if t < 0.5 else 4
        d.ellipse([CX-r, CY-r, CX+r, CY+r], outline=COLOUR+(alpha,), width=width)
        # faint second line for sonar thickness
        if r > 40:
            d.ellipse([CX-r+10, CY-r+10, CX+r-10, CY+r-10], outline=COLOUR+(max(0,alpha-80),), width=2)
    canvas.alpha_composite(effect)
    frames.append(canvas)
    # transparent master: base + effect only, no grey
    master = Image.new("RGBA", (W, H), (0,0,0,0))
    master.alpha_composite(base)
    master.alpha_composite(effect)
    master.save(f"{OUT}/frames/sonar-frame-{f:02d}.png")
frames[0].save(f"{OUT}/chest-logo-sonar-20261031.gif", save_all=True, append_images=frames[1:], duration=1000//FPS, loop=0)
# contact: frames 0, 6, 12, 18 + effect-only diagram
contact = Image.new("RGB", (W*2, H), (128,128,128))
for i, fi in enumerate([0,6,12,18]):
    pass
# simpler contact: 2x2 grid at half scale
small = [(frames[i].resize((550,750))) for i in [0,6,12,18]]
contact2 = Image.new("RGB", (1100,1500), (128,128,128))
contact2.paste(small[0], (0,0)); contact2.paste(small[1], (550,0))
contact2.paste(small[2], (0,750)); contact2.paste(small[3], (550,750))
contact2.save(f"{OUT}/chest-logo-sonar-contact-20261031.png")
# effect-only still for layer proof
effect_only = Image.new("RGBA", (W,H), (0,0,0,0))
d = ImageDraw.Draw(effect_only)
for k in range(RING_COUNT):
    t = k/RING_COUNT
    r = 30 + t*(MAX_R-30)
    d.ellipse([CX-r, CY-r, CX+r, CY+r], outline=COLOUR+(200,), width=6)
effect_only.save(f"{OUT}/chest-logo-sonar-effect-only-20261031.png")
meta = {"preset":"CHEST LOGO SONAR","origin":[CX,CY],"origin_source":"Transformation #4 measured purple emblem piece, bbox x539-562 y475-510, centroid 550.8,491.1","ring_count":RING_COUNT,"max_radius_px":MAX_R,"colour":COLOUR,"frames":N_FRAMES,"fps":FPS,"duration_ms":N_FRAMES*1000//FPS,"loop":"1 full pulse cycle, rings staggered 1/3 cycle","layer":"separate effect layer, base art never recoloured or baked","categories":["POWER (superpowers)","GADGET (cyborg + gadget costume)"]}
json.dump(meta, open(f"{OUT}/chest-logo-sonar-preset-20261031.json","w"), indent=2)
print(meta)
print("gif frames", len(frames))
