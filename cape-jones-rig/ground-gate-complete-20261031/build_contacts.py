import json, os
from PIL import Image, ImageDraw
RIG=os.path.expanduser("~/workspace/cape-jones-rig"); OUT=os.path.join(RIG,"ground-gate-complete-20261031")
gate=json.load(open(os.path.join(OUT,"gate-30-results.json")))
def tile(files, cols, thumb_w, out, label_fn):
    thumbs=[]
    for f in files:
        im=Image.open(f).convert("RGB"); im.thumbnail((thumb_w, int(thumb_w*1500/1100)))
        thumbs.append(im)
    rows=(len(thumbs)+cols-1)//cols; th=max(t.height for t in thumbs); tw=thumb_w
    sheet=Image.new("RGB",(cols*tw, rows*(th+22)),(20,20,20)); d=ImageDraw.Draw(sheet)
    for i,(im,f) in enumerate(zip(thumbs,files)):
        x=(i%cols)*tw; y=(i//cols)*(th+22); sheet.paste(im,(x,y+22)); d.text((x+4,y+4), label_fn(f), fill=(255,255,0))
    sheet.save(out); print(out, sheet.size)
tile([os.path.join(OUT,r["composite"]) for r in gate], 8, 200, os.path.join(OUT,"gate-30-contact-20261031.png"),
     lambda f: os.path.basename(f).split("-20261031")[0])
air=[r for r in gate if r["mode"]=="AIRBORNE"]
tile([os.path.join(OUT,r["composite"]) for r in air], 3, 300, os.path.join(OUT,"airborne-proof-contact-20261031.png"),
     lambda f: os.path.basename(f).split("-20261031")[0])
# blender contact
a=Image.open(os.path.join(OUT,"blender-ground-plane-20261031.png")).convert("RGB")
b=Image.open(os.path.join(OUT,"blender-depth-20261031.png")).convert("RGB").resize(a.size)
sheet=Image.new("RGB",(a.width*2+10, a.height+30),(20,20,20)); d=ImageDraw.Draw(sheet)
sheet.paste(a,(0,30)); sheet.paste(b,(a.width+10,30)); d.text((4,4),"Blender Cycles ground plane: plane z=0, proxy bottom 0.0, airborne bottom 0.5",fill=(255,255,0)); d.text((a.width+14,4),"Blender ray-cast depth: ground 7.193, grounded box 5.986, airborne box 6.066",fill=(255,255,0))
sheet.save(os.path.join(OUT,"blender-ground-depth-contact-20261031.png")); print("blender contact", sheet.size)
