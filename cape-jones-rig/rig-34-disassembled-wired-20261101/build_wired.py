"""Rebuild sit-chair figure from MANIFEST-20261101.json alone.
Usage: python3 build_wired.py [--fists on|off]  (default off = open-hand version, fists 0 drawn)
Rotation is about the saved pivot_xy, using each piece's pivot fractions and
its original display size (for forearm/fist layers, the full forearm size).
No crop, no erase: fist layers are simply not drawn when --fists off.
"""
import json, sys, os
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__))
man=json.load(open(os.path.join(HERE,"MANIFEST-20261101.json")))
fists = "on" in sys.argv or "--fists" in sys.argv and "on" in sys.argv
# simpler flag parsing
if "--fists" in sys.argv:
    fists = sys.argv[sys.argv.index("--fists")+1]=="on"
W,H=man["canvas"]
def render():
    canvas=Image.new("RGBA",(W,H),(0,0,0,0))
    # DEFS-stable: sort by (z, defs_order)
    for p in sorted(man["pieces"], key=lambda q:(q["z"], q["defs_order"])):
        if p["id"].startswith("fist") and not fists:
            continue
        if not p.get("visible",True) and not (p["id"].startswith("fist") and fists):
            continue
        im=Image.open(os.path.join(HERE,p["file"])).convert("RGBA")
        fw,fh=p["display_size"]
        px,py=p["pivot_xy"]; ox,oy=p["pivot"]
        # top offset of this file within the full piece
        top_offset=0
        if p["id"].startswith("fist"):
            top_offset=fw and (fh - im.height)  # full height - fist height = cut
            # actually cut = full - fist height
            top_offset=fh-im.height
        # rotation centre in file coords
        cx=ox*fw; cy=oy*fh-top_offset
        # paste file onto temp, rotate about centre, then place so centre lands at pivot_xy
        tmp=Image.new("RGBA",(im.width*3,im.height*3),(0,0,0,0))
        tmp.alpha_composite(im,(im.width,im.height))
        ccx,ccy=im.width+cx, im.height+cy
        rot=tmp.rotate(-p["rotation"], resample=Image.BICUBIC, center=(ccx,ccy))
        canvas.alpha_composite(rot,(int(round(px-ccx)), int(round(py-ccy))))
    return canvas
canvas=render()
canvas.save(os.path.join(HERE,"poses/sit-chair-wired-20261101.png"))
bg=Image.new("RGBA",(W,H),(126,126,126,255)); bg.alpha_composite(canvas); bg.convert("RGB").save(os.path.join(HERE,"poses/sit-chair-wired-20261101-on-grey.png"))
# contact sheet: each piece alone, labelled, 5 cols
import math
vis=[p for p in man["pieces"]]
cols=5; cellw,cellh=280,320; rows=math.ceil(len(vis)/cols)
sheet=Image.new("RGB",(cols*cellw,rows*cellh),(255,255,255))
d=ImageDraw.Draw(sheet)
for i,p in enumerate(vis):
    im=Image.open(os.path.join(HERE,p["file"])).convert("RGBA")
    thumb=im.copy(); thumb.thumbnail((260,260))
    cx=(i%cols)*cellw; cy=(i//cols)*cellh
    bgc=Image.new("RGBA",(260,260),(230,230,230,255)); bgc.alpha_composite(thumb,((260-thumb.width)//2,(260-thumb.height)//2))
    sheet.paste(bgc.convert("RGB"),(cx+10,cy+10))
    d.text((cx+10,cy+275), f"{p['id']} z{p['z']} rot{p['rotation']} {'LOCK' if p['locked'] else 'free'}", fill=(0,0,0))
    d.text((cx+10,cy+295), f"{p['x']},{p['y']} vis={p['visible']}", fill=(80,80,80))
sheet.save(os.path.join(HERE,"contacts/pieces-contact-20261101.png"))
# gates
import numpy as np
a=np.array(canvas); alpha=a[:,:,3]>0; ys,xs=np.where(alpha)
gates={"canvas":[W,H],"bbox":[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],"alpha_bottom_overall":int(ys.max()),
 "alpha_bottom_left_band_0_700":int(np.where(alpha[:,:700])[0].max()) if np.any(alpha[:,:700]) else None,
 "alpha_bottom_right_band_700_1400":int(np.where(alpha[:,700:])[0].max()) if np.any(alpha[:,700:]) else None,
 "widget_ground_y":1475,"hands_drawn":2,"fists_drawn":2 if fists else 0,"pieces_drawn":sum(1 for p in man["pieces"] if p["visible"] or (p["id"].startswith("fist") and fists)),
 "pieces_total":len(man["pieces"])}
json.dump(gates, open(os.path.join(HERE,"gates-20261101.json"),"w"), indent=2)
print(json.dumps(gates,indent=2))
