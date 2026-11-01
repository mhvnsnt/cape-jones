"""Separate trail + plate layers for the Blender compositor pass (punch only).
Trail layer: soft bands of previous forearm positions only, cyan, transparent bg.
Plate layer: approved v5 Arm2 flipped forearm at current position, transparent bg.
Blender then AlphaOvers: dark bg -> trail -> plate, Standard view, no Glare
(so cyan input is preserved; AgX would shift it — see color-shift study)."""
import os
from PIL import Image, ImageFilter
import numpy as np
R=os.path.expanduser("~/workspace/cape-jones-rig"); OUT=f"{R}/afterglow-videos-20261031/blender_layers_punch"
os.makedirs(OUT,exist_ok=True)
TRAIL=[0.50,0.40,0.30,0.20,0.12,0.06]; W,H=640,360
fore=Image.open(f"{R}/forearm-fist-v5-correction-20261031/forearm-v5-arm2-forward-punch-flipped-20261031.png").convert("RGBA")
fw,fh=fore.size; fore=fore.resize((200,int(fh*200/fw)),Image.LANCZOS)
d=fore.split()[3].filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(5))
band=Image.fromarray(np.clip(np.array(d,dtype=np.int16)-np.array(fore.split()[3],dtype=np.int16),0,255).astype(np.uint8),"L")
pos=[(400,150)]*3+[(350,125),(300,100),(250,75),(210,60)]+[(210,60)]*4+[(260,85),(320,115),(380,140)]+[(380,140)]*4
for fi,(x,y) in enumerate(pos):
    trail=Image.new("RGBA",(W,H),(0,0,0,0))
    for lag,f in enumerate(TRAIL,1):
        if fi-lag<0: continue
        px,py=pos[fi-lag]
        if (px,py)==(x,y): continue
        glow=Image.new("RGBA",fore.size,(0,200,255,0))
        glow.putalpha(band.point(lambda v: int(v*f)))
        trail.alpha_composite(glow,(px,py))
    trail.save(f"{OUT}/trail-{fi:02d}.png")
    plate=Image.new("RGBA",(W,H),(0,0,0,0)); plate.alpha_composite(fore,(x,y))
    plate.save(f"{OUT}/plate-{fi:02d}.png")
print("layers ok",len(pos))
