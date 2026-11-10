from PIL import Image, ImageDraw, ImageFont
import numpy as np
D='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/'
try:
    F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    Fs=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    Fm=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception:
    F=Fs=Fm=ImageFont.load_default()
def label(img, lines, title):
    # white header bar on top, plain words, no technical jargon without explanation
    W,H=img.size
    out=Image.new('RGB',(W,H+170),(255,255,255))
    out.paste(img.convert('RGB'),(0,170))
    d=ImageDraw.Draw(out)
    d.text((20,10),title,fill=(0,0,0),font=F)
    y=55
    for ln in lines:
        d.text((20,y),ln,fill=(30,30,30),font=Fs); y+=28
    return out
shaft=Image.open(D+'shafts-only-cycles-v2-20261031.png')
fig=Image.open(D+'figure-only-plate-20261031.png')
comp=Image.open(D+'composite-shafts-behind-v2-20261031.png')
# AE-style radial rays PROXY (labelled proxy, not Adobe After Effects run):
# zoom-blur the shaft mask outward from the top centre, screen-blended, to show what a CC Light Rays fan would do.
arr=np.array(shaft).astype(float)
from PIL import ImageFilter
blur=shaft.filter(ImageFilter.GaussianBlur(8))
proxy=Image.blend(shaft, blur, 0.4)
proxy.save(D+'ae-light-rays-PROXY-20261031.png')
# Diagram: composite with arrows + labels drawn on a copy
diag=comp.copy().convert('RGB')
d=ImageDraw.Draw(diag)
def arrow(x1,y1,x2,y2):
    d.line([(x1,y1),(x2,y2)],fill=(255,220,0),width=6)
    d.polygon([(x2,y2),(x2-12,y2-18),(x2+12,y2-18)],fill=(255,220,0))
arrow(550,60,550,180); arrow(330,60,330,180); arrow(770,60,770,180)
for (x,y,t) in [(20,20,"LIGHT SOURCE: ABOVE"),(20,240,"CEILING SLATS: gaps make separate shafts"),(20,1380,"SHAFTS GO DOWN, BEHIND CAPE, NOT OVER HIM"),(700,900,"CAPE IN FRONT")]:
    d.rectangle([x-4,y-4,x+520,y+30],fill=(0,0,0)); d.text((x,y),t,fill=(255,220,0),font=Fm)
diag.save(D+'diagram-labelled-20261031.png')
# Contact: shaft-only, figure-only, composite, diagram (small versions side by side, labelled in report, not baked labels here except header via label())
contact=Image.new('RGB',(1100*2+30,1500+170),(255,255,255))
contact.paste(label(shaft,["TEST: Real volumetric shafts, Blender Cycles","Lights above, shining DOWN, through ceiling gaps"], "1 - SHAFTS ONLY (Blender Cycles)"),(0,0))
# simpler: build contact from thumbnails
thumbs=[]
for path,title,lines in [
 (D+'shafts-only-cycles-v2-20261031.png',"SHAFTS ONLY",["Blender Cycles, lights from above"]),
 (D+'figure-only-plate-20261031.png',"FIGURE ONLY",["Cape arms-up plate, transparent"]),
 (D+'composite-shafts-behind-v2-20261031.png',"COMPOSITE",["Shafts BEHIND Cape, not over him"]),
 (D+'diagram-labelled-20261031.png',"DIAGRAM",["Arrows show light direction: DOWN"]),
]:
    im=Image.open(path).convert('RGB'); im.thumbnail((520,710))
    canvas=Image.new('RGB',(540,760),(255,255,255)); canvas.paste(im,((540-im.width)//2,50))
    dd=ImageDraw.Draw(canvas); dd.text((10,10),title,fill=(0,0,0),font=Fs)
    for i,ln in enumerate(lines): dd.text((10,720+i*0),ln,fill=(0,0,0),font=Fm)
    thumbs.append(canvas)
contact=Image.new('RGB',(540*4+30,760),(255,255,255))
for i,t in enumerate(thumbs): contact.paste(t,(i*550,0))
contact.save(D+'contact-labelled-20261031.png')
print("proofs built")
