import os
from PIL import Image, ImageFilter
import numpy as np
R=os.path.expanduser("~/workspace/cape-jones-rig"); OUT=f"{R}/afterglow-videos-20261031"
BG=(18,18,28,255); TRAIL=[0.50,0.40,0.30,0.20,0.12,0.06]; W,H=640,360
fore=Image.open(f"{R}/forearm-fist-v5-correction-20261031/forearm-v5-arm2-forward-punch-flipped-20261031.png").convert("RGBA")
fw,fh=fore.size; fore=fore.resize((200,int(fh*200/fw)),Image.LANCZOS)
d=fore.split()[3].filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(5))
band=Image.fromarray(np.clip(np.array(d,dtype=np.int16)-np.array(fore.split()[3],dtype=np.int16),0,255).astype(np.uint8),"L")
pos=[(400,150)]*3+[(350,125),(300,100),(250,75),(210,60)]+[(210,60)]*4+[(260,85),(320,115),(380,140)]+[(380,140)]*10
print("frames",len(pos))
os.makedirs(f"{OUT}/blender_layers_punch24",exist_ok=True)
frames=[]
for fi,(x,y) in enumerate(pos):
    trail=Image.new("RGBA",(W,H),(0,0,0,0))
    for lag,f in enumerate(TRAIL,1):
        if fi-lag<0: continue
        px,py=pos[fi-lag]
        if (px,py)==(x,y): continue
        glow=Image.new("RGBA",fore.size,(0,200,255,0))
        glow.putalpha(band.point(lambda v: int(v*f)))
        trail.alpha_composite(glow,(px,py))
    trail.save(f"{OUT}/blender_layers_punch24/trail-{fi:02d}.png")
    plate=Image.new("RGBA",(W,H),(0,0,0,0)); plate.alpha_composite(fore,(x,y))
    plate.save(f"{OUT}/blender_layers_punch24/plate-{fi:02d}.png")
    canvas=Image.new("RGBA",(W,H),BG); canvas.alpha_composite(trail); canvas.alpha_composite(plate)
    frames.append(canvas.convert("RGB"))
    canvas.save(f"{OUT}/frames_punch/punch-frame-{fi:02d}.png")
frames[0].save(f"{OUT}/punch-limb-afterglow-20261031.gif",save_all=True,append_images=frames[1:],duration=100,loop=0)
sheet=Image.new("RGB",(640*4+30,360+40),(255,255,255))
for i,idx in enumerate([2,5,7,23]): sheet.paste(frames[idx],(i*650,20))
sheet.save(f"{OUT}/punch-limb-afterglow-contact-20261031.png")
# verify final frame has no cyan trail: count pixels that are not plate/bg
last=np.array(frames[-1])
print("final frame distinct colours", len(np.unique(last.reshape(-1,3),axis=0)))
